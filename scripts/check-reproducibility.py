#!/usr/bin/env python3
"""Run submission code in a copied workspace and write evaluator-owned evidence."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

from importlib.util import module_from_spec, spec_from_file_location

ROOT = Path(__file__).resolve().parent.parent
spec = spec_from_file_location("oracle_common", ROOT / "docs/oracles/_shared/oracle_common.py")
common = module_from_spec(spec); assert spec.loader; spec.loader.exec_module(common)


def semantic(path: Path):
    if path.suffix == ".json":
        return json.loads(path.read_text(encoding="utf-8"))
    if path.suffix in {".csv", ".tsv"}:
        delimiter = "\t" if path.suffix == ".tsv" else ","
        with path.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle, delimiter=delimiter)
            return reader.fieldnames, list(reader)
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--python", default=os.environ.get("PYTHON", "python3"))
    parser.add_argument("--timeout", type=int, default=900)
    args = parser.parse_args()
    workspace = args.workspace.resolve(); original = workspace / "output"
    required = common.REQUIRED_OUTPUTS[args.task_id]
    record = {"task_id": args.task_id, "clean_run_exit_code": None, "required_outputs_reproduced": False, "semantic_equivalence_pass": False, "compared_artifacts": [], "stderr_tail": ""}
    with tempfile.TemporaryDirectory(prefix=f"rerun-{args.task_id}-") as raw:
        clean = Path(raw); shutil.copytree(workspace / "inputs", clean / "inputs"); (clean / "output").mkdir()
        # The root input manifest is part of every public one-use workspace and
        # submission scripts may legitimately validate it. Preserve it in the
        # isolated rerun just as faithfully as the read-only inputs directory.
        manifest = workspace / "INPUT_MANIFEST.sha256.tsv"
        if manifest.is_file():
            shutil.copy2(manifest, clean / manifest.name)
        if args.task_id == "ls09-opentrons-sop":
            shutil.copy2(original / "protocol.py", clean / "output/protocol.py")
            command = [args.python, "-m", "opentrons.simulate", "output/protocol.py"]
        else:
            shutil.copy2(original / "analysis.py", clean / "output/analysis.py")
            command = [args.python, "output/analysis.py"]
        try:
            run = subprocess.run(command, cwd=clean, capture_output=True, text=True, timeout=args.timeout, check=False, env={**os.environ, "PYTHONHASHSEED": "0"})
            record["clean_run_exit_code"] = run.returncode
            record["stderr_tail"] = run.stderr[-4000:]
            if args.task_id == "ls09-opentrons-sop":
                record["required_outputs_reproduced"] = run.returncode == 0
                record["semantic_equivalence_pass"] = run.returncode == 0
                record["compared_artifacts"] = ["protocol.py:simulator_exit_0"]
            else:
                compare = [name for name in required if name not in {"analysis.py", "report.md"}]
                present = run.returncode == 0 and all((clean / "output" / name).is_file() for name in compare)
                record["required_outputs_reproduced"] = present
                matches = present
                if present:
                    for name in compare:
                        try:
                            ok = semantic(original / name) == semantic(clean / "output" / name)
                        except Exception:
                            ok = False
                        record["compared_artifacts"].append(f"{name}:{'match' if ok else 'mismatch'}")
                        matches &= ok
                record["semantic_equivalence_pass"] = matches
        except Exception as exc:
            record["stderr_tail"] = f"{type(exc).__name__}: {exc}"
    target = workspace / ".evaluator" / "reproducibility.json"; target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(record, ensure_ascii=False, indent=2))
    return 0 if record["semantic_equivalence_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
