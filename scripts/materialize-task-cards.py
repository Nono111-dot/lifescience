#!/usr/bin/env python3
"""Materialize the two canonical task-card collections as 25 GitHub-visible files."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "task-card"


def sections(path: Path, heading_pattern: re.Pattern[str]) -> list[tuple[str, str]]:
    text = path.read_text(encoding="utf-8")
    matches = list(heading_pattern.finditer(text))
    result: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        result.append((match.group("task_id"), text[match.start() : end].rstrip() + "\n"))
    return result


def main() -> None:
    source_1 = ROOT / "docs" / "task-cards" / "ls01-ls05-v2.md"
    source_2 = ROOT / "docs" / "ls06-ls10-task-cards-v2.md"
    cards = sections(
        source_1,
        re.compile(r"^## .*?`(?P<task_id>ls0[1-5]-[^`]+)`\s*$", re.MULTILINE),
    )
    cards += sections(
        source_2,
        re.compile(r"^## `(?P<task_id>ls(?:06|07|08|09|10)-[^`]+)`\s*$", re.MULTILINE),
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
            f"> Canonical individual task card materialized from `{source}`. "
            "The Prompt is the only instruction pasted into an evaluated run; oracle-only "
            "answers and evaluation outputs are never exposed to the agent.\n\n"
        )
        (TARGET / f"{task_id}.md").write_text(header + body, encoding="utf-8")

    ordered = sorted(task_id for task_id, _ in cards)
    lines = [
        "# Task cards\n",
        "This directory is the GitHub-facing entry point for the 25 frozen life-science task cards. "
        "Each task has one standalone file containing its metadata, paste-once Prompt, deliverables, "
        "scientific hard gates, deterministic scoring details, and ablation/skill expectation.\n",
        "Gold answers, hidden reference artifacts, run outputs, and evaluation scores are intentionally "
        "not stored in these participant-visible cards.\n",
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
