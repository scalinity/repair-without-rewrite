"""Preselected real training/calibration pairs from the qualified narrow source."""
import hashlib
import importlib.metadata
import json
import os
import platform
from pathlib import Path
import shutil
import subprocess
import tarfile
import time

from src.data.development_reader import load_targets
from src.data.parakeet_source import transcribe_development, RUNTIME_ID


def sha(p):
    return hashlib.file_digest(Path(p).open("rb"),"sha256").hexdigest()


def main():
    out=Path("exports/foundation-repair/development-asr-pairs-attempt01")
    out.mkdir(parents=True,exist_ok=False)
    roles="experiments/manifests/public_lspc_training_roles.development.jsonl"
    supply="experiments/manifests/public_lspc_training_supply_qualification.json"
    rows=load_targets(roles,supply,allowed_roles={"train","calibration","hpo_development"})
    selections=[]
    # Selection uses only stable source IDs and admitted manifest duration. The
    # original twelve DEV clips remain unchanged, not redrawn by output quality.
    for role,limit in (("train",1024),("calibration",96)):
        eligible=[r for r in rows if r["role"]==role and r["official_split"]=="train-clean-100"
                  and 2<=float(r["manifest_duration_seconds"])<=12]
        chosen=sorted(eligible,key=lambda r:hashlib.sha256(("development-real-pairs-120101:"+r["id"]).encode()).hexdigest())[:limit]
        selections.extend(chosen)
    manifest=[{k:r[k] for k in ("id","role","source_group_id","families","text_sha256","text_raw_sha256","manifest_duration_seconds")}
              for r in selections]
    (out/"selection.json").write_text(json.dumps(manifest,indent=2)+"\n")
    archive=Path("exports/foundation-repair/train-clean-100-acquisition-attempt01/train-clean-100.tar.gz")
    receipt=json.loads(archive.with_name("receipt.json").read_text())
    if receipt["status"]!="PASS" or sha(archive)!=receipt["sha256"]:
        raise ValueError("official audio archive not verified")
    selected={"LibriSpeech/"+r["audio_filepath"]:r for r in selections}
    acquired={}
    with tarfile.open(archive,"r:gz") as tar:
        for member in tar:
            if member.name not in selected:
                continue
            r=selected[member.name]
            audio=out/"audio"/(r["id"]+".flac")
            audio.parent.mkdir(exist_ok=True)
            with tar.extractfile(member) as source,audio.open("wb") as f:
                shutil.copyfileobj(source,f)
            acquired[r["id"]]=str(audio)
    if acquired.keys()!={r["id"] for r in selections}:
        raise ValueError("missing selected native recordings")
    cfgpath="experiments/manifests/asr_tts_probe/asr_book_closed_config.json"
    cfg=json.loads(Path(cfgpath).read_text())
    for a in cfg["parakeet"]["assets"]:
        if sha(a["path"])!=a["sha256"]:
            raise ValueError("changed pinned model")
    provenance={"head":subprocess.check_output(["git","rev-parse","HEAD"],text=True).strip(),
        "dirty_status":subprocess.check_output(["git","status","--porcelain"],text=True),
        "dirty_diff":subprocess.check_output(["git","diff","--binary"],text=True),
        "source_runtime":RUNTIME_ID,"selection_sha256":sha(out/"selection.json"),"roles_sha256":sha(roles),
        "supply_sha256":sha(supply),"audio_archive":receipt,"config_sha256":sha(cfgpath),
        "code_hashes":{p:sha(p) for p in (__file__,"src/data/parakeet_source.py","src/data/development_reader.py")},
        "seed":"hash namespace120101", "tokenizer_sha256":sha("configs/tokenizer_development/tokenizer.json"),
        "runtime":{"python":platform.python_version(),"platform":platform.platform(),
            "packages":{p:importlib.metadata.version(p) for p in ("mlx","parakeet-mlx","numpy","soundfile")},
            "MLX_ENABLE_TF32":os.environ.get("MLX_ENABLE_TF32"),"model_working_dtype":"bfloat16",
            "waveform_and_features":"float32", "concurrent_accelerator_work":False}}
    (out/"provenance.json").write_text(json.dumps(provenance,indent=2)+"\n")
    import mlx.core as mx
    import soundfile as sf
    from parakeet_mlx import from_pretrained
    model=from_pretrained(cfg["parakeet"]["snapshot"],dtype=mx.bfloat16)
    mx.eval(model.parameters())
    begin=time.perf_counter();failures=0
    with (out/"pairs.jsonl").open("w",buffering=1) as f:
        for index,r in enumerate(selections):
            path=Path(acquired[r["id"]]); info=sf.info(path)
            if info.samplerate!=16000 or info.channels!=1 or not 2<=info.frames/16000<=12:
                raise ValueError("decoded waveform outside selected runtime contract")
            start=time.perf_counter()
            row={**r,"audio_sha256":sha(path),"audio_seconds":info.frames/16000,"source_runtime":RUNTIME_ID}
            try:
                result=transcribe_development(model,path)
                row.update(source=result.text,source_sha256=hashlib.sha256(result.text.encode()).hexdigest(),status="COMPLETED")
            except Exception as error:
                row.update(source=None,source_sha256=None,status="FAILED",error_type=type(error).__name__,error=str(error))
                failures+=1
            mx.synchronize();row["seconds"]=time.perf_counter()-start
            f.write(json.dumps(row,sort_keys=True,allow_nan=False)+"\n")
            if index%100==0:
                print(json.dumps({"completed":index+1,"failures":failures}),flush=True)
    (out/"summary.json").write_text(json.dumps({"selected":len(selections),"failed":failures,"seconds":time.perf_counter()-begin,
        "pairs_sha256":sha(out/"pairs.jsonl"),"peak_mlx_bytes":mx.get_peak_memory(),"runtime":RUNTIME_ID},indent=2)+"\n")


if __name__=="__main__":
    main()
