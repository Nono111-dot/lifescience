#!/usr/bin/env python3
"""Materialize the two canonical task-card collections as 25 GitHub-visible files."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "task-card"
INPUTS = ROOT / "docs" / "inputs"


def sections(path: Path, heading_pattern: re.Pattern[str]) -> list[tuple[str, str]]:
    text = path.read_text(encoding="utf-8")
    matches = list(heading_pattern.finditer(text))
    result: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        result.append((match.group("task_id"), text[match.start() : end].rstrip() + "\n"))
    return result


def packaged_inputs(task_id: str) -> str:
    task_root = INPUTS / task_id
    paths = sorted(path for path in task_root.rglob("*") if path.is_file())
    if not paths:
        raise RuntimeError(f"No packaged inputs found for {task_id}")
    total = sum(path.stat().st_size for path in paths)
    lines = ["### Inputs (authoritative packaged inventory)\n"]
    for path in paths:
        relative = path.relative_to(task_root).as_posix()
        lines.append(f"- `inputs/{relative}` — {path.stat().st_size:,} bytes\n")
    lines.append(f"\n**Total:** {total:,} bytes ({total / 1024 / 1024:.2f} MiB).\n")
    return "".join(lines)


def normalize_inputs(body: str, task_id: str) -> str:
    inventory = packaged_inputs(task_id)
    rich = re.compile(r"(?ms)^### Inputs(?: \(authoritative packaged inventory\))?\s*\n.*?(?=^### Prompt|^- Prompt:)")
    if rich.search(body):
        return rich.sub(inventory + "\n", body, count=1)
    compact = re.compile(r"(?m)^- Inputs:.*$")
    if compact.search(body):
        return compact.sub(inventory.rstrip(), body, count=1)
    raise RuntimeError(f"No input section found for {task_id}")


def normalize_source(path: Path, heading_pattern: re.Pattern[str]) -> None:
    text = path.read_text(encoding="utf-8")
    matches = list(heading_pattern.finditer(text))
    for index in range(len(matches) - 1, -1, -1):
        match = matches[index]
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        section = text[match.start() : end]
        normalized = normalize_inputs(section, match.group("task_id"))
        text = text[: match.start()] + normalized + text[end:]
    path.write_text(text, encoding="utf-8")


def main() -> None:
    source_1 = ROOT / "docs" / "task-cards" / "ls01-ls05-v2.md"
    source_2 = ROOT / "docs" / "ls06-ls10-task-cards-v2.md"
    pattern_1 = re.compile(r"^## .*?`(?P<task_id>ls0[1-5]-[^`]+)`\s*$", re.MULTILINE)
    pattern_2 = re.compile(r"^## `(?P<task_id>ls(?:06|07|08|09|10)-[^`]+)`\s*$", re.MULTILINE)
    normalize_source(source_1, pattern_1)
    normalize_source(source_2, pattern_2)
    cards = sections(
        source_1,
        pattern_1,
    )
    cards += sections(
        source_2,
        pattern_2,
    )
    if len(cards) != 25 or len({task_id for task_id, _ in cards}) != 25:
        raise RuntimeError(f"Expected 25 unique task cards, found {len(cards)}")

    TARGET.mkdir(exist_ok=True)
    for task_id, body in cards:
        source = (
            "docs/task-cards/ls01-ls05-v2.md"
            if task_id.startswith(("ls01-", "ls02-", "ls03-", "ls04-", "ls05-"))
            else "docs/ls06-ls10-task-cards-v2.md"
        )
        header = (
            f"# Task card: `{task_id}`\n\n"
            f"> Canonical participant-facing card generated from `{source}`. "
            "The packaged-input inventory below is generated from the frozen task directory. "
            "Only the Prompt is pasted into a run; evaluator-only answers and outputs are never exposed.\n\n"
        )
        (TARGET / f"{task_id}.md").write_text(
            header + normalize_inputs(body, task_id), encoding="utf-8"
        )

    ordered = sorted(task_id for task_id, _ in cards)
    lines = [
        "# Task cards\n",
        "This directory is the participant-facing entry point for the 25 frozen life-science task cards. "
        "Each task has one standalone file containing an exact packaged-input inventory, paste-once Prompt, "
        "deliverables, scientific hard gates, deterministic scoring details and capability expectation.\n",
        "Evaluator-only answers, oracle fixtures, run outputs and scores are not stored in these cards "
        "and must never be copied into a participant workspace.\n",
        "## Card index\n",
    ]
    lines.extend(f"- [`{task_id}`]({task_id}.md)\n" for task_id in ordered)
    lines += [
        "\n## Controlling contracts\n",
        "- Input hashes and provenance: [`docs/inputs/SHA256SUMS.tsv`](../docs/inputs/SHA256SUMS.tsv)\n",
        "- Deterministic score allocation: [`docs/deterministic-rubrics-v2.tsv`](../docs/deterministic-rubrics-v2.tsv)\n",
        "- C0/T1 protocol: [`docs/evaluation-protocol-c0-t1-v2.md`](../docs/evaluation-protocol-c0-t1-v2.md)\n",
        "- Formal release status: [`docs/formal-eval-release-status-2026-08-17.md`](../docs/formal-eval-release-status-2026-08-17.md)\n",
    ]
    (TARGET / "README.md").write_text("".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
