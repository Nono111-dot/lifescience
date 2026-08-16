#!/usr/bin/env python3
"""Execute the frozen 50-row Codex C0/T1 queue serially and resumably."""
from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent.parent
CODEX = Path("/Applications/ChatGPT.app/Contents/Resources/codex")
INSTALLER = Path("/Users/mac/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py")
DEFAULT_CODEX_HOME = Path("/Users/mac/.codex")
BASE_PYTHON_BIN = Path("/Users/mac/Documents/ChatGPT/测吧测吧厕不明白啊/reference_staging/oracle-env/bin")
OPENTRONS_PYTHON_BIN = Path("/Users/mac/Documents/ChatGPT/测吧测吧厕不明白啊/reference_staging/opentrons-env/bin")
SKILLS = {
    "ITEM-035": ("scgpt", "7af27c91d22afd7bd465d2d84b5fbe6702792d9233fa81ab75cbfa00818cf55e"),
    "ITEM-036": ("scvi-tools", "5b206bb329a8953264333f757a0360f635d45486a5e8cc167b54205c9ded9bda"),
}


def utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha(path: Path) -> str:
    h = hashlib.sha256(); h.update(path.read_bytes()); return h.hexdigest()


def prompt_for(task_id: str) -> str:
    candidates = [
        ROOT / "docs/task-cards/ls01-ls05-v2.md",
        ROOT / "docs/task-cards/ls07-v2.md" if task_id.startswith("ls07-") else Path("/nonexistent"),
        ROOT / "docs/task-cards/ls09-v2.md" if task_id.startswith("ls09-") else Path("/nonexistent"),
        ROOT / "docs/ls06-ls10-task-cards-v2.md",
    ]
    for path in candidates:
        if not path.is_file(): continue
        text = path.read_text(encoding="utf-8")
        heading = re.search(rf"(?m)^##[^\n]*`{re.escape(task_id)}`[^\n]*$", text)
        if not heading: continue
        end = re.search(r"(?m)^## ", text[heading.end():])
        section = text[heading.end(): heading.end() + (end.start() if end else len(text))]
        inline = re.search(r"(?m)^- Prompt: \*\*(.+)\*\*$", section)
        if inline: return inline.group(1).strip()
        marker = re.search(r"(?mi)^#{0,3}[^\n]*Prompt[^\n]*$", section)
        if marker:
            tail = section[marker.end():]
            lines = []
            started = False
            for line in tail.splitlines():
                match = re.match(r"\s*>\s?(.*)", line)
                if match:
                    started = True; lines.append(match.group(1))
                elif started and line.strip():
                    break
            if lines: return "\n\n".join(line for line in lines if line.strip())
    raise ValueError(f"prompt not found: {task_id}")


def selected_items(task_id: str) -> list[str]:
    with (ROOT / "docs/task-skill-plan-codex-t1-v1.tsv").open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            if row["task_id"] == task_id:
                return [] if row["selected_catalog_item_ids"] == "NONE" else row["selected_catalog_item_ids"].split(",")
    raise ValueError(task_id)


def install_skills(profile: Path, items: list[str], log_dir: Path) -> list[dict]:
    records = []
    for item in items:
        name, expected = SKILLS[item]
        command = [sys.executable, str(INSTALLER), "--repo", "JimLiu/science-skills", "--ref", "fb309c32ee9a54dad169fa845638057d1cfac77f", "--path", f"skills/{name}", "--dest", str(profile / "skills")]
        started = utc(); run = subprocess.run(command, capture_output=True, text=True, check=False)
        installed = profile / "skills" / name / "SKILL.md"
        observed = sha(installed) if installed.is_file() else None
        record = {"item": item, "name": name, "started_at": started, "finished_at": utc(), "exit_code": run.returncode, "expected_sha256": expected, "observed_sha256": observed, "hash_match": observed == expected, "stdout": run.stdout, "stderr": run.stderr}
        records.append(record)
        if run.returncode or observed != expected: raise RuntimeError(f"skill install verification failed: {record}")
    (log_dir / "capability_install.json").write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return records


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--campaign", type=Path, required=True)
    parser.add_argument("--start-sequence", type=int, default=1)
    parser.add_argument("--end-sequence", type=int, default=50)
    parser.add_argument("--model", default="gpt-5.4")
    parser.add_argument("--reasoning", default="xhigh")
    args = parser.parse_args(); campaign = args.campaign.resolve()
    queue = list(csv.DictReader((ROOT / "docs/formal-run-queue-c0-t1-2026-08-16.tsv").open(encoding="utf-8"), delimiter="\t"))
    for row in queue:
        seq = int(row["sequence"])
        if not args.start_sequence <= seq <= args.end_sequence: continue
        run_id, task_id, condition = row["run_id"], row["task_id"], row["condition"]
        run_dir = campaign / "runs" / run_id; log_dir = run_dir / "logs"; grading = run_dir / "grading"
        done = grading / "oracle.json"
        if done.is_file():
            print(f"SKIP completed {seq}/50 {run_id}", flush=True); continue
        print(f"START {seq}/50 {run_id} {utc()}", flush=True)
        workspace = run_dir / "workspace"
        prep = [sys.executable, str(ROOT / "scripts/prepare-c0-t1-run.py"), "--repo", str(ROOT), "--campaign", str(campaign), "--run-id", run_id, "--task-id", task_id, "--condition", condition]
        subprocess.run(prep, check=True)
        log_dir.mkdir(parents=True, exist_ok=True); grading.mkdir(parents=True, exist_ok=True)
        prompt = prompt_for(task_id); (log_dir / "prompt.txt").write_text(prompt + "\n", encoding="utf-8")
        profile = campaign / "profiles" / run_id; profile.mkdir(parents=True, exist_ok=False)
        os.symlink(DEFAULT_CODEX_HOME / "auth.json", profile / "auth.json")
        items = selected_items(task_id) if condition == "T1" else []
        install_skills(profile, items, log_dir)
        inventory = sorted((p.relative_to(profile).as_posix(), sha(p)) for p in profile.rglob("SKILL.md"))
        (log_dir / "capability_inventory.json").write_text(json.dumps({"condition": condition, "selected_items": items, "skills": inventory}, indent=2) + "\n", encoding="utf-8")
        final_message = log_dir / "codex_final.txt"
        command = [str(CODEX), "--search", "-s", "workspace-write", "-a", "never", "-m", args.model, "-c", f'model_reasoning_effort="{args.reasoning}"', "-c", 'shell_environment_policy.inherit="all"', "exec", "--ephemeral", "--ignore-user-config", "--skip-git-repo-check", "--json", "-o", str(final_message), "-"]
        env = {**os.environ, "CODEX_HOME": str(profile), "PYTHONHASHSEED": "0"}
        python_bin = OPENTRONS_PYTHON_BIN if task_id == "ls09-opentrons-sop" else BASE_PYTHON_BIN
        env["PATH"] = str(python_bin) + os.pathsep + env.get("PATH", "")
        started = time.monotonic(); status = "completed"
        with (log_dir / "codex_events.jsonl").open("w", encoding="utf-8") as stdout, (log_dir / "codex_stderr.txt").open("w", encoding="utf-8") as stderr:
            try:
                completed = subprocess.run(command, cwd=workspace, input=prompt, text=True, stdout=stdout, stderr=stderr, timeout=95 * 60, check=False, env=env)
                exit_code = completed.returncode
                if exit_code: status = "client_error"
            except subprocess.TimeoutExpired:
                exit_code = 124; status = "timeout"
        execution = {"run_id": run_id, "task_id": task_id, "condition": condition, "model": args.model, "reasoning": args.reasoning, "client_version": subprocess.check_output([str(CODEX), "--version"], text=True).strip(), "started_at": utc(), "duration_seconds": time.monotonic() - started, "exit_code": exit_code, "status": status, "items": items}
        (log_dir / "execution.json").write_text(json.dumps(execution, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        repro_python = str(OPENTRONS_PYTHON_BIN / "python") if task_id == "ls09-opentrons-sop" else str(BASE_PYTHON_BIN / "python")
        subprocess.run([sys.executable, str(ROOT / "scripts/check-reproducibility.py"), "--workspace", str(workspace), "--task-id", task_id, "--python", repro_python], stdout=(log_dir / "reproducibility_stdout.txt").open("w"), stderr=(log_dir / "reproducibility_stderr.txt").open("w"), check=False)
        subprocess.run([sys.executable, str(ROOT / "scripts/freeze-c0-t1-run.py"), "--campaign", str(campaign), "--run-id", run_id], check=True)
        frozen = run_dir / "frozen"
        oracle = ROOT / "docs/oracles" / task_id / "oracle.py"
        with (grading / "oracle_stdout.txt").open("w", encoding="utf-8") as out, (grading / "oracle_stderr.txt").open("w", encoding="utf-8") as err:
            subprocess.run([sys.executable, str(oracle), "--workspace", str(frozen), "--json-out", str(done)], stdout=out, stderr=err, check=False)
        print(f"DONE {seq}/50 {run_id} status={status} {utc()}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
