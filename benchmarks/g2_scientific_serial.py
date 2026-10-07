"""Serial fixed-order campaign; only one identical numerical replay is allowed."""
import argparse
import datetime
import json
import os
import signal
import subprocess
import sys
import time

from benchmarks.g2_scientific_campaign import ORDER, execution_outcomes, write
from src.data.g2_artifacts import ArtifactRoot


def run(binding):
    root = ArtifactRoot(binding); active = None; stopped = []
    def interrupt(signum, frame):
        stopped.append(signum)
        if active is not None and active.poll() is None:
            active.send_signal(signal.SIGTERM)
    for sig in (signal.SIGINT, signal.SIGTERM): signal.signal(sig, interrupt)
    for name in ORDER:
        while True:
            root.preflight(); outcomes = execution_outcomes(name)
            latest = outcomes[-1] if outcomes else None
            if latest and latest["status"] in ("COMPLETED", "FAILED_NUMERICAL"): break
            if latest and latest["status"] not in ("NUMERICAL_FAILURE", "INTERRUPTED"):
                raise RuntimeError("GENERATION_2_EXECUTION_REPAIR_REQUIRED")
            if stopped: raise InterruptedError("serial campaign stopped between scientific jobs")
            attempt = 1 if latest is None else latest["attempt"] + 1
            args = [sys.executable, "-m", "benchmarks.g2_scientific_campaign", "run",
                    "--artifact-binding", binding, "--recipe", name, "--attempt", str(attempt)]
            if latest:
                resume = latest["latest_verified_checkpoint"]
                if not resume: raise RuntimeError("GENERATION_2_EXECUTION_REPAIR_REQUIRED: no verified replay state")
                args += ["--resume", resume]
            logfile = root.path(f"logs-v1/scientific-{name}.attempt{attempt:02d}.log")
            print(json.dumps({"phase": "scientific-launch", "recipe_id": name, "attempt": attempt}), flush=True)
            with logfile.open("x") as stream:
                active = subprocess.Popen(args, stdout=stream, stderr=subprocess.STDOUT,
                    env={**os.environ, "MLX_ENABLE_TF32": "0"})
                while active.poll() is None:
                    time.sleep(30)
                    print(json.dumps({"phase": "scientific-process-active", "recipe_id": name,
                                      "attempt": attempt, "pid": active.pid}), flush=True)
            returncode = active.returncode; active = None
            outcome = execution_outcomes(name)
            if not outcome or outcome[-1]["attempt"] != attempt:
                raise RuntimeError("GENERATION_2_EXECUTION_REPAIR_REQUIRED: child has no retained outcome")
            record = outcome[-1]
            print(json.dumps({"phase": "scientific-attempt-finished", "recipe_id": name,
                              "attempt": attempt, "status": record["status"], "returncode": returncode}), flush=True)
            if stopped: raise InterruptedError("serial campaign interrupted after verified checkpoint")
            if record["status"] in ("COMPLETED", "FAILED_NUMERICAL"): break
            if record["status"] != "NUMERICAL_FAILURE": raise RuntimeError("GENERATION_2_EXECUTION_REPAIR_REQUIRED")
    print(json.dumps({"phase": "seven-prescribed-outcomes-exist", "scientific_outcomes": 7}), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(); parser.add_argument("--artifact-binding", required=True)
    args = parser.parse_args(); run(args.artifact_binding)
