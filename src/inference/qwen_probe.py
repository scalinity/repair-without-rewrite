"""Exact BF16 Qwen paper-identity native path probe, synthetic DEV only."""
from __future__ import annotations
import argparse
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import resource
import subprocess
import time

from src.inference.byt5_probe import digest


def strict_bytelevel_text(tokens, byte_decoder, special_tokens):
    # Reuse the installed official tokenizer's byte alphabet; do not accept its
    # default errors='replace' when a capped output ends inside a UTF-8 scalar.
    pieces=[]
    for token in tokens:
        pieces.append(token.encode('utf-8') if token in special_tokens
                      else bytes(byte_decoder[c] for c in token))
    return b''.join(pieces).decode('utf-8','strict')


def validate_config(config, rows):
    if config['repository']!='Qwen/Qwen3-4B-Instruct-2507' or config['revision']!='cdbee75f17c01a7cc42f958dc650907174af0554':
        raise ValueError('exact task checkpoint required')
    if config['scope']!='SYNTHETIC_DEVELOPMENT_PATH_ONLY' or config['precision']!='BF16' or config['device']!='mps':
        raise ValueError('registered native BF16 development path required')
    if not 1<=len(rows)<=2 or any(r['role']!='hpo_development' for r in rows):
        raise ValueError('at most two synthetic DEV cases required')
    if not 1<=config['max_new_tokens']<=64 or not 1<=config['input_token_cap']<=512:
        raise ValueError('bounded native context/decode required')
    if config['do_sample'] is not False or config['num_beams']!=1:
        raise ValueError('greedy decode required')


def run(config_path:Path,weights:Path,output:Path):
    started=time.time();phase='validate';report={'scope':'SYNTHETIC_DEVELOPMENT_PATH_ONLY','status':'RUNNING','decoding':[]}
    output.parent.mkdir(parents=True,exist_ok=True)
    try:
        config=json.loads(config_path.read_text());data=Path(config['data_path']);rows=json.loads(data.read_text())
        report.update(config=config,config_sha256=digest(config_path),data_sha256=digest(data),code_sha256=digest(Path(__file__)),
            repository_head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
            repository_status=subprocess.check_output(['git','status','--porcelain'],text=True),
            platform=platform.platform(),machine=platform.machine(),start_unix_seconds=started,
            versions={p:importlib.metadata.version(p) for p in ('torch','transformers','tokenizers','safetensors')})
        validate_config(config,rows)
        if report['data_sha256']!=config['data_sha256']:raise ValueError('data integrity mismatch')
        report['assets_sha256']={name:digest(weights/name) for name in config['assets_sha256']}
        if report['assets_sha256']!=config['assets_sha256']:raise ValueError('pinned asset integrity mismatch')
        if os.environ.get('PYTORCH_ENABLE_MPS_FALLBACK') not in (None,'0'):
            raise ValueError('silent CPU fallback must be disabled')
        import torch
        from transformers import AutoTokenizer,AutoModelForCausalLM
        from transformers.models.qwen2.tokenization_qwen2 import bytes_to_unicode
        if not torch.backends.mps.is_available():raise RuntimeError('Metal backend unavailable')
        torch.manual_seed(config['development_seed']);torch.set_num_threads(2)
        phase='tokenizer';tokenizer=AutoTokenizer.from_pretrained(str(weights),local_files_only=True,trust_remote_code=False)
        byte_decoder={v:k for k,v in bytes_to_unicode().items()}
        special_tokens=set(tokenizer.get_added_vocab())
        phase='native_load';tick=time.monotonic()
        model=AutoModelForCausalLM.from_pretrained(str(weights),local_files_only=True,trust_remote_code=False,
            use_safetensors=True,torch_dtype=torch.bfloat16,attn_implementation='eager').to('mps').eval()
        torch.mps.synchronize();report['cold_load_and_transfer_seconds']=time.monotonic()-tick
        report['parameters']=sum(p.numel() for p in model.parameters())
        report['parameter_dtype_counts']={str(d):sum(p.numel() for p in model.parameters() if p.dtype==d)
                                          for d in {p.dtype for p in model.parameters()}}
        if any(p.dtype!=torch.bfloat16 for p in model.parameters()):raise ValueError('unexpected non-BF16 model parameter')
        report['model_config_max_positions']=model.config.max_position_embeddings
        eos_ids=config['eos_token_ids'];phase='greedy_decode'
        for ordinal,row in enumerate(rows):
            messages=[{'role':'system','content':config['system_prompt']},{'role':'user','content':row['source']}]
            framed=tokenizer.apply_chat_template(messages,tokenize=False,add_generation_prompt=True)
            encoded=tokenizer(framed,return_tensors='pt',add_special_tokens=False)
            length=int(encoded['input_ids'].shape[1])
            if length>config['input_token_cap'] or length+config['max_new_tokens']>model.config.max_position_embeddings:
                raise ValueError('native context admission failed; do not truncate')
            encoded={k:v.to('mps') for k,v in encoded.items()};torch.mps.synchronize();tick=time.monotonic()
            with torch.no_grad():
                ids=model.generate(**encoded,do_sample=False,num_beams=1,max_new_tokens=config['max_new_tokens'],
                    eos_token_id=eos_ids,pad_token_id=151643,use_cache=True)[0,length:].tolist()
            torch.mps.synchronize();seconds=time.monotonic()-tick
            complete=bool(ids and ids[-1] in eos_ids);content=ids[:-1] if complete else ids
            try:
                text=strict_bytelevel_text(tokenizer.convert_ids_to_tokens(content),byte_decoder,special_tokens)
                status='complete' if complete else 'capped';reason=None if complete else 'missing_eos_at_cap'
            except (UnicodeError,KeyError):text=None;status='invalid_utf8';reason='strict_bytelevel_decode_failed'
            from src.scoring.records import prepare_source,score_output,Output
            scored=score_output(prepare_source(row['reference'],row['source']),Output(text,status))
            report['decoding'].append(dict(id=row['id'],ordinal=ordinal,native_input_tokens=length,
                native_new_tokens=len(ids),generated_ids=ids,text=text,status=status,failure_reason=reason,
                request_seconds=seconds,request_timing_scope='materialized native generate; load/tokenization separately retained',
                complete_valid=scored['complete_valid'],eS=scored['eS'],eO=scored['eO'],
                repair=scored['completed_repair'],introduced=scored['introduced'],
                process_peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                mps_allocated_bytes=torch.mps.current_allocated_memory(),mps_driver_allocated_bytes=torch.mps.driver_allocated_memory()))
            output.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
        report.update(status='NATIVE_BF16_GREEDY_PATH_EXECUTED_SYNTHETIC_ONLY',task_adequacy='NOT_ESTABLISHED',prompt_frozen=False)
    except Exception as error:
        report.update(status='FAILED',failure_phase=phase,failure_type=type(error).__name__,failure_message=str(error))
    finally:
        report.update(elapsed_seconds=time.time()-started,peak_process_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
        output.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    return report


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--config',type=Path,required=True)
    parser.add_argument('--weights',type=Path,required=True);parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();result=run(args.config,args.weights,args.output)
    print(json.dumps({k:result[k] for k in ('status','elapsed_seconds','peak_process_rss_bytes')}))
    if result['status']=='FAILED':raise SystemExit(1)


if __name__=='__main__':main()
