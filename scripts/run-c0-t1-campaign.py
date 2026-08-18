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
DEFAULT_CODEX = Path(os.environ.get("CODEX_BIN", shutil.which("codex") or "/Applications/ChatGPT.app/Contents/Resources/codex"))
DEFAULT_CODEX_HOME = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
SKILLS = {
    "ITEM-035": ("JimLiu/science-skills", "fb309c32ee9a54dad169fa845638057d1cfac77f", "skills/scgpt", "scgpt", "7af27c91d22afd7bd465d2d84b5fbe6702792d9233fa81ab75cbfa00818cf55e"),
    "ITEM-036": ("JimLiu/science-skills", "fb309c32ee9a54dad169fa845638057d1cfac77f", "skills/scvi-tools", "scvi-tools", "5b206bb329a8953264333f757a0360f635d45486a5e8cc167b54205c9ded9bda"),
    "KDENSE-pydeseq2": ("K-Dense-AI/claude-scientific-skills", "336c4f838a6c21b54e1e1f58cbbeae143d151fe2", "skills/pydeseq2", "pydeseq2", "9c4f27a73a151f8bb97f323bf509c5f1860398858b2eb6374f3e37004e76d31b"),
    "KDENSE-bulk-rnaseq": ("K-Dense-AI/claude-scientific-skills", "336c4f838a6c21b54e1e1f58cbbeae143d151fe2", "skills/bulk-rnaseq", "bulk-rnaseq", "b39c5999e482c178f4659885126dad7f10b21133d24d0f78a1a206377d6e9067"),
    "KDENSE-pathway-enrichment": ("K-Dense-AI/claude-scientific-skills", "336c4f838a6c21b54e1e1f58cbbeae143d151fe2", "skills/pathway-enrichment", "pathway-enrichment", "efffb28aebf448a26160660fcb962b264f40b92e2c3c42ee19ae644a5e63fa94"),
    "KDENSE-genomic-coordinates": ("K-Dense-AI/claude-scientific-skills", "336c4f838a6c21b54e1e1f58cbbeae143d151fe2", "skills/genomic-coordinates", "genomic-coordinates", "afc6c6f220a860e9aaba29eb64abccf35d7f5957b81e703ebdaa326b90a6ba2f"),
    "KDENSE-pysam": ("K-Dense-AI/claude-scientific-skills", "336c4f838a6c21b54e1e1f58cbbeae143d151fe2", "skills/pysam", "pysam", "ee5596b06cbbb3e95e906d448511217659e0e141dc8d30817714d1edd64dfac2"),
    "KDENSE-deeptools": ("K-Dense-AI/claude-scientific-skills", "336c4f838a6c21b54e1e1f58cbbeae143d151fe2", "skills/deeptools", "deeptools", "2724906bdf23e60fe15aa5e7bb9af2bf36cab82d9e8640de847a69523c0a334a"),
    "KDENSE-exploratory-data-analysis": ("K-Dense-AI/claude-scientific-skills", "336c4f838a6c21b54e1e1f58cbbeae143d151fe2", "skills/exploratory-data-analysis", "exploratory-data-analysis", "ed1c66ba8de6add4af4a19423ff6c43fc5dafb56a0a8e142992ebae907c1b194"),
    "KDENSE-statsmodels": ("K-Dense-AI/claude-scientific-skills", "336c4f838a6c21b54e1e1f58cbbeae143d151fe2", "skills/statsmodels", "statsmodels", "bf67fe14237de502151a33ed62c77a4716cc096ede7f501adbeab46179774054"),
    "KDENSE-statistical-analysis": ("K-Dense-AI/claude-scientific-skills", "336c4f838a6c21b54e1e1f58cbbeae143d151fe2", "skills/statistical-analysis", "statistical-analysis", "2bc90ee5c35a820eabb0304447dabc8fee5c140bee12bc534521e21649d3cea2"),
    "KDENSE-biopython": ("K-Dense-AI/claude-scientific-skills", "336c4f838a6c21b54e1e1f58cbbeae143d151fe2", "skills/biopython", "biopython", "81eab1bd7db605635dc94bfc97e7264657325db5b220b40edf48ec178392c668"),
    "KDENSE-matplotlib": ("K-Dense-AI/claude-scientific-skills", "336c4f838a6c21b54e1e1f58cbbeae143d151fe2", "skills/matplotlib", "matplotlib", "3558028333b2b9838eea455cf74a248b8825c8d8b0d2ab7830dd1520df879cca"),
    "KDENSE-pylabrobot": ("K-Dense-AI/claude-scientific-skills", "336c4f838a6c21b54e1e1f58cbbeae143d151fe2", "skills/pylabrobot", "pylabrobot", "b71caf1fe017a80fbb898f1e33de4a0ef1ff1940f17b682d34f1f79021034322"),
    "KDENSE-scanpy": ("K-Dense-AI/claude-scientific-skills", "336c4f838a6c21b54e1e1f58cbbeae143d151fe2", "skills/scanpy", "scanpy", "3ca2db22fb47dff7f49504816dba3f4600e1290c4731459b44355837955ed9ba"),
    "KDENSE-scvi-tools": ("K-Dense-AI/claude-scientific-skills", "336c4f838a6c21b54e1e1f58cbbeae143d151fe2", "skills/scvi-tools", "scvi-tools", "6be01b41da9cbbcd9a83a072b1dddb7717efc0fbc8dad1627de497eb8b20b2b6"),
    "KDENSE-deepspot-m": ("K-Dense-AI/claude-scientific-skills", "336c4f838a6c21b54e1e1f58cbbeae143d151fe2", "skills/deepspot-m", "deepspot-m", "854cad4fea6fcdab967809052ffd4216c489fa957a4a023b95ece2f565a273c6"),
    "KDENSE-uncertainty-and-units": ("K-Dense-AI/claude-scientific-skills", "336c4f838a6c21b54e1e1f58cbbeae143d151fe2", "skills/uncertainty-and-units", "uncertainty-and-units", "064ef574c85d7f4c472261ccab166e1e3a189b2baded27ecc523c64c8bfc1240"),
}


def set_python_runtime(python_executable: Path, wrapper_bin: Path, log_dir: Path) -> None:
    """Expose one pinned Python through the stable PATH used by fresh Codex shells."""
    target = python_executable.resolve()
    wrapper = f"#!/bin/sh\nexec '{target}' \"$@\"\n"
    wrapper_bin.mkdir(parents=True, exist_ok=False)
    for name in ("python", "python3"):
        path = wrapper_bin / name
        path.write_text(wrapper, encoding="utf-8")
        path.chmod(0o755)
    probe = subprocess.run([str(wrapper_bin / "python"), "-c", "import sys; print(sys.executable); print(sys.version)"], capture_output=True, text=True, check=False)
    (log_dir / "python_runtime.txt").write_text(f"target={target}\nexit_code={probe.returncode}\n{probe.stdout}{probe.stderr}", encoding="utf-8")
    if probe.returncode:
        raise RuntimeError("pinned Python wrapper smoke failed")


def utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha(path: Path) -> str:
    h = hashlib.sha256(); h.update(path.read_bytes()); return h.hexdigest()


def prompt_for(task_id: str) -> str:
    path = ROOT / "task-card" / f"{task_id}.md"
    text = path.read_text(encoding="utf-8")
    inline = re.search(r"(?m)^- Prompt: \*\*(.+)\*\*$", text)
    if inline:
        return inline.group(1).strip()
    marker = re.search(r"(?mi)^#{0,3}[^\n]*Prompt[^\n]*$", text)
    if marker:
        tail = text[marker.end():]
        lines = []
        started = False
        for line in tail.splitlines():
            match = re.match(r"\s*>\s?(.*)", line)
            if match:
                started = True
                lines.append(match.group(1))
            elif started and line.strip():
                break
        if lines:
            return "\n\n".join(line for line in lines if line.strip())
    raise ValueError(f"prompt not found: {task_id}")


def selected_items(task_id: str) -> list[str]:
    with (ROOT / "docs/task-skill-plan-codex-t1-v1.tsv").open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            if row["task_id"] == task_id:
                return [] if row["selected_catalog_item_ids"] == "NONE" else row["selected_catalog_item_ids"].split(",")
    raise ValueError(task_id)


def install_skills(profile: Path, items: list[str], log_dir: Path, installer: Path) -> list[dict]:
    records = []
    for item in items:
        repo, ref, skill_path, name, expected = SKILLS[item]
        command = [sys.executable, str(installer), "--repo", repo, "--ref", ref, "--path", skill_path, "--dest", str(profile / "skills"), "--method", "git"]
        started = utc(); run = subprocess.run(command, capture_output=True, text=True, check=False)
        installed = profile / "skills" / name / "SKILL.md"
        observed = sha(installed) if installed.is_file() else None
        record = {"item": item, "name": name, "repo": repo, "ref": ref, "path": skill_path, "started_at": started, "finished_at": utc(), "exit_code": run.returncode, "expected_sha256": expected, "observed_sha256": observed, "hash_match": observed == expected, "stdout": run.stdout, "stderr": run.stderr}
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
    parser.add_argument("--codex-bin", type=Path, default=DEFAULT_CODEX)
    parser.add_argument("--codex-home", type=Path, default=DEFAULT_CODEX_HOME)
    parser.add_argument("--skill-installer", type=Path)
    parser.add_argument("--python-executable", type=Path, default=Path(sys.executable))
    parser.add_argument("--opentrons-python-executable", type=Path, default=Path(sys.executable))
    args = parser.parse_args(); campaign = args.campaign.resolve()
    skill_installer = args.skill_installer or args.codex_home / "skills/.system/skill-installer/scripts/install-skill-from-github.py"
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
        auth = args.codex_home / "auth.json"
        if not auth.is_file():
            raise FileNotFoundError(f"Codex authentication file not found: {auth}")
        os.symlink(auth, profile / "auth.json")
        items = selected_items(task_id) if condition == "T1" else []
        install_skills(profile, items, log_dir, skill_installer)
        inventory = sorted((p.relative_to(profile).as_posix(), sha(p)) for p in profile.rglob("SKILL.md"))
        (log_dir / "capability_inventory.json").write_text(json.dumps({"condition": condition, "selected_items": items, "skills": inventory}, indent=2) + "\n", encoding="utf-8")
        final_message = log_dir / "codex_final.txt"
        command = [str(args.codex_bin), "--search", "-s", "workspace-write", "-a", "never", "-m", args.model, "-c", f'model_reasoning_effort="{args.reasoning}"', "-c", 'shell_environment_policy.inherit="all"', "exec", "--ephemeral", "--ignore-user-config", "--skip-git-repo-check", "--json", "-o", str(final_message), "-"]
        env = {**os.environ, "CODEX_HOME": str(profile), "PYTHONHASHSEED": "0"}
        python_executable = args.opentrons_python_executable if task_id == "ls09-opentrons-sop" else args.python_executable
        wrapper_bin = profile / "bin"
        set_python_runtime(python_executable, wrapper_bin, log_dir)
        env["PATH"] = str(wrapper_bin) + os.pathsep + env.get("PATH", "")
        started = time.monotonic(); status = "completed"
        with (log_dir / "codex_events.jsonl").open("w", encoding="utf-8") as stdout, (log_dir / "codex_stderr.txt").open("w", encoding="utf-8") as stderr:
            try:
                completed = subprocess.run(command, cwd=workspace, input=prompt, text=True, stdout=stdout, stderr=stderr, timeout=95 * 60, check=False, env=env)
                exit_code = completed.returncode
                if exit_code: status = "client_error"
            except subprocess.TimeoutExpired:
                exit_code = 124; status = "timeout"
        execution = {"run_id": run_id, "task_id": task_id, "condition": condition, "model": args.model, "reasoning": args.reasoning, "client_version": subprocess.check_output([str(args.codex_bin), "--version"], text=True).strip(), "started_at": utc(), "duration_seconds": time.monotonic() - started, "exit_code": exit_code, "status": status, "items": items}
        (log_dir / "execution.json").write_text(json.dumps(execution, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        if status != "completed":
            # A transport/auth/client failure is not a model submission.  Preserve the
            # one-use workspace and logs for infrastructure adjudication, but never
            # freeze/score an empty or partial output as a deterministic zero.
            print(
                f"ABORT {seq}/50 {run_id} status={status} exit_code={exit_code} {utc()}",
                flush=True,
            )
            return 2
        repro_python = str(python_executable)
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
