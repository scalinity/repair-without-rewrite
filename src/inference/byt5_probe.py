"""Bounded native ByT5 development path probe; never a final comparator result."""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import math
import os
from pathlib import Path
import platform
import resource
import subprocess
import time

from src.data.comparator_interfaces import byt5_batch, byt5_complete_text


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as file:
        while block := file.read(4 * 1024 * 1024): h.update(block)
    return h.hexdigest()


def validate_config(config: dict, rows: list[dict]) -> None:
    if config['scope'] != 'SYNTHETIC_DEVELOPMENT_PATH_ONLY':
        raise ValueError('development-only scope required')
    if not 1 <= config['updates'] <= 50 or not 1 <= config['batch_size'] <= 4:
        raise ValueError('bounded update/batch limit exceeded')
    if not 1 <= config['source_capacity'] <= 128 or not 1 <= config['target_capacity'] <= 128:
        raise ValueError('bounded native byte capacities required')
    if not 1 <= config['decode_max_new_tokens'] <= 128:
        raise ValueError('bounded greedy decode capacity required')
    if config['device'] not in {'cpu', 'mps'}:
        raise ValueError('only coordinated local CPU/Metal probe is allowed')
    if len(rows) > 8 or sum(r['role'] == 'hpo_development' for r in rows) > 2:
        raise ValueError('bounded development panel limit exceeded')
    if not 1 <= config['training_wall_seconds_cap'] <= 180:
        raise ValueError('bounded training window required')
    for row in rows:
        if row['role'] not in {'train', 'hpo_development'}:
            raise ValueError('reserved/final role forbidden')
        byt5_batch([row['source']], [row['reference']],
                   source_capacity=config['source_capacity'], target_capacity=config['target_capacity'])
    if len({r['id'] for r in rows}) != len(rows):
        raise ValueError('duplicate development ID')


def decode_ids(ids: list[int]) -> dict:
    """ByT5 generation includes decoder-start PAD; failure never receives repair."""
    if not ids or ids[0] != 0:
        return {'text': None, 'status': 'invalid_utf8', 'reason': 'missing_decoder_start'}
    emitted = ids[1:]
    if 1 in emitted:
        end = emitted.index(1)
        if any(v != 0 for v in emitted[end + 1:]):
            return {'text': None, 'status': 'invalid_utf8', 'reason': 'nonpad_after_eos'}
        try:
            text = byt5_complete_text(emitted[:end + 1])
        except (UnicodeError, ValueError):
            return {'text': None, 'status': 'invalid_utf8', 'reason': 'nonbyte_or_invalid_utf8'}
        return {'text': text, 'status': 'complete', 'reason': None}
    try:
        text = byt5_complete_text(emitted + [1])
    except (UnicodeError, ValueError):
        return {'text': None, 'status': 'invalid_utf8', 'reason': 'nonbyte_or_invalid_utf8_prefix'}
    return {'text': text, 'status': 'capped', 'reason': 'missing_eos_at_cap'}


def native_batch(rows, config, device):
    import torch
    batch = byt5_batch([r['source'] for r in rows], [r['reference'] for r in rows],
        source_capacity=config['source_capacity'], target_capacity=config['target_capacity'])
    result = {k: torch.tensor(batch[k], dtype=torch.long, device=device)
              for k in ('input_ids', 'attention_mask', 'labels', 'decoder_input_ids')}
    # BOS is PAD=0 but is a real decoder position. Derive mask from labels.
    result['decoder_attention_mask'] = (result['labels'] != -100).long()
    return result, sum(batch['valid_target_counts'])


def run(config_path: Path, weights: Path, output: Path) -> dict:
    started = time.time(); phase = 'validate'; report = {'status': 'RUNNING', 'scope': 'SYNTHETIC_DEVELOPMENT_PATH_ONLY'}
    output.parent.mkdir(parents=True, exist_ok=True)
    try:
        config = json.loads(config_path.read_text()); data_path = Path(config['data_path'])
        report.update(config=config, config_sha256=digest(config_path), data_sha256=digest(data_path),
            code_sha256=digest(Path(__file__)), repository_head=subprocess.check_output(['git', 'rev-parse', 'HEAD'],text=True).strip(),
            repository_status=subprocess.check_output(['git', 'status', '--porcelain'], text=True),
            platform=platform.platform(), machine=platform.machine(), start_unix_seconds=started,
            versions={name: importlib.metadata.version(name) for name in ('torch','transformers','numpy')},
            losses=[], decoding=[], native_supervised_tokens=0, native_source_tokens=0, updates_completed=0)
        rows = json.loads(data_path.read_text()); validate_config(config, rows)
        if report['data_sha256'] != config['data_sha256']: raise ValueError('development data checksum mismatch')
        report['weight_sha256']=digest(weights / 'pytorch_model.bin')
        if report['weight_sha256'] != config['weight_sha256']:
            raise ValueError('official weight checksum mismatch')
        report['model_config_sha256']=digest(weights / 'config.json')
        if report['model_config_sha256'] != config['model_config_sha256']:
            raise ValueError('official model config checksum mismatch')
        report['observed_native_byte_lengths']={name:{'min':min(len(r[name].encode())+1 for r in rows),
            'max':max(len(r[name].encode())+1 for r in rows)} for name in ('source','reference')}
        if os.environ.get('PYTORCH_ENABLE_MPS_FALLBACK') not in (None, '0'):
            raise ValueError('silent Metal-to-CPU fallback must be disabled for native qualification')
        import torch
        from transformers import T5ForConditionalGeneration
        torch.manual_seed(config['development_seed']); torch.set_num_threads(2)
        if config['device'] == 'mps' and not torch.backends.mps.is_available():
            raise RuntimeError('requested Metal backend unavailable; no silent CPU fallback')
        device = torch.device(config['device'])
        def sync():
            if device.type == 'mps': torch.mps.synchronize()
        phase = 'load'; tick = time.monotonic()
        model = T5ForConditionalGeneration.from_pretrained(str(weights), local_files_only=True,
            weights_only=True, trust_remote_code=False, attn_implementation='eager', torch_dtype=torch.float32)
        sync(); report['cpu_cold_load_seconds'] = time.monotonic()-tick
        report['parameters'] = sum(p.numel() for p in model.parameters())
        report['parameter_dtype_counts'] = {str(dtype):sum(p.numel() for p in model.parameters() if p.dtype == dtype)
                                           for dtype in {p.dtype for p in model.parameters()}}
        training = [r for r in rows if r['role'] == 'train']; development = [r for r in rows if r['role'] == 'hpo_development']
        if len(training) < config['batch_size'] or not development: raise ValueError('insufficient declared development data')
        phase='cpu_native_forward';model.eval()
        cpu_batch,_=native_batch(training[:config['batch_size']],config,'cpu');tick=time.monotonic()
        with torch.no_grad(): cpu_prediction=model(**cpu_batch,use_cache=False)
        cpu_logits=cpu_prediction.logits.detach().cpu();cpu_loss=float(cpu_prediction.loss)
        report['cpu_forward_seconds']=time.monotonic()-tick
        del cpu_prediction
        phase='native_forward_parity';model.to(device);sync();tick=time.monotonic()
        native,_=native_batch(training[:config['batch_size']],config,device)
        with torch.no_grad(): native_prediction=model(**native,use_cache=False)
        native_logits=native_prediction.logits.detach().cpu();native_loss=float(native_prediction.loss.detach().cpu());sync()
        report['native_first_forward_seconds']=time.monotonic()-tick
        report['forward_parity']={'cpu_loss':cpu_loss,'native_loss':native_loss,
            'logits_max_absolute_error':float((cpu_logits-native_logits).abs().max()),
            'atol':0.001,'rtol':0.0002,'status':'PENDING'}
        torch.testing.assert_close(cpu_logits,native_logits,atol=0.001,rtol=0.0002)
        if not math.isclose(cpu_loss,native_loss,abs_tol=0.001,rel_tol=0.0002):
            raise ValueError('native loss differs from CPU reference beyond registered tolerance')
        report['forward_parity']['status']='PASS'
        del cpu_logits,native_logits,native_prediction,cpu_batch,native
        def decode_panel(label):
            model.eval()
            for row in development:
                batch, _ = native_batch([row], config, device); sync(); tick=time.monotonic()
                with torch.no_grad():
                    ids=model.generate(input_ids=batch['input_ids'], attention_mask=batch['attention_mask'],
                        do_sample=False, num_beams=1, max_new_tokens=config['decode_max_new_tokens'], use_cache=True,
                        eos_token_id=1, pad_token_id=0, decoder_start_token_id=0)[0].tolist()
                sync(); seconds=time.monotonic()-tick
                decoded=decode_ids(ids)
                from src.scoring.records import prepare_source, score_output, Output
                scored=score_output(prepare_source(row['reference'],row['source']),Output(decoded['text'],decoded['status']))
                report['decoding'].append(dict(panel=label,id=row['id'],ids=ids,decoded=decoded,seconds=seconds,
                    native_source_tokens=int(batch['attention_mask'].sum().item()),
                    generated_native_tokens=len(ids)-1,complete_valid=scored['complete_valid'],
                    eS=scored['eS'],eO=scored['eO'],repair=scored['completed_repair'],introduced=scored['introduced']))
        phase='pre_decode'; decode_panel('before')
        optimizer=torch.optim.AdamW(model.parameters(),lr=config['learning_rate'],weight_decay=0.01)
        model.train();phase='adaptation'; tick=time.monotonic()
        for step in range(config['updates']):
            if time.monotonic()-tick > config['training_wall_seconds_cap']:
                raise TimeoutError('bounded training window exceeded; completed steps retained')
            selected=[training[(step*config['batch_size']+j)%len(training)] for j in range(config['batch_size'])]
            batch, supervised=native_batch(selected,config,device);optimizer.zero_grad(set_to_none=True)
            step_start=time.monotonic();prediction=model(**batch,use_cache=False);loss=prediction.loss
            value=float(loss.detach().cpu());
            if not math.isfinite(value):raise FloatingPointError('nonfinite native loss')
            loss.backward();gradient=float(torch.nn.utils.clip_grad_norm_(model.parameters(),1.0))
            if not math.isfinite(gradient):raise FloatingPointError('nonfinite native gradient')
            optimizer.step();sync()
            report['losses'].append(dict(step=step+1,loss=value,gradient_norm=gradient,seconds=time.monotonic()-step_start,
                                        valid_target_tokens=supervised))
            report['updates_completed']=step+1;report['native_supervised_tokens']+=supervised
            report['native_source_tokens']+=int(batch['attention_mask'].sum().item())
            if step==0:
                report['gradient_dtypes']=sorted({str(p.grad.dtype) for p in model.parameters() if p.grad is not None})
                report['optimizer_state_dtypes']=sorted({str(v.dtype) for state in optimizer.state.values() for v in state.values() if torch.is_tensor(v)})
            report['peak_process_rss_bytes']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            output.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
        report['adaptation_seconds']=time.monotonic()-tick
        del optimizer
        phase='post_decode';decode_panel('after')
        report.update(status='NATIVE_PATH_EXECUTED_SYNTHETIC_ONLY',credible_natural_adaptation='NOT_ESTABLISHED')
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
