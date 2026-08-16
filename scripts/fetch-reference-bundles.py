#!/usr/bin/env python3
"""Fetch auditable chromosome FASTA bundles from indexed public references.

The script deliberately downloads only named sequences with a single HTTP byte
range computed from the remote FASTA index. It writes one gzip member per sequence so repository inputs
remain below GitHub's single-file limit and records content hashes in a manifest.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import gzip
import hashlib
import json
from pathlib import Path
import urllib.request


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_remote_fai(url: str) -> dict[str, tuple[int, int, int, int]]:
    with urllib.request.urlopen(url + ".fai") as response:
        text = response.read().decode("ascii")
    result = {}
    for line in text.splitlines():
        name, length, offset, line_bases, line_width = line.split("\t")[:5]
        result[name] = tuple(map(int, (length, offset, line_bases, line_width)))
    return result


def fetch_one(
    url: str,
    index: dict[str, tuple[int, int, int, int]],
    sequence: str,
    destination: Path,
) -> dict[str, object]:
    destination.mkdir(parents=True, exist_ok=True)
    path = destination / f"{sequence}.fa.gz"
    length, offset, line_bases, line_width = index[sequence]
    byte_span = ((length - 1) // line_bases) * line_width + ((length - 1) % line_bases) + 1
    request = urllib.request.Request(
        url,
        headers={"Range": f"bytes={offset}-{offset + byte_span - 1}"},
    )
    with urllib.request.urlopen(request) as response:
        raw = response.read()
    bases = raw.replace(b"\n", b"").replace(b"\r", b"").decode("ascii").upper()
    if len(bases) != length:
        raise ValueError(f"{sequence}: expected {length} bases, received {len(bases)}")
    with gzip.open(path, "wt", encoding="ascii", newline="\n", compresslevel=6) as handle:
        handle.write(f">{sequence}\n")
        for offset in range(0, len(bases), 60):
            handle.write(bases[offset : offset + 60] + "\n")
    return {
        "sequence": sequence,
        "length": len(bases),
        "file": path.name,
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    parser.add_argument("--sequences", nargs="+", required=True)
    parser.add_argument("--destination", type=Path, required=True)
    parser.add_argument("--source-name", required=True)
    parser.add_argument("--source-version", required=True)
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    index = read_remote_fai(args.url)
    missing = sorted(set(args.sequences) - set(index))
    if missing:
        parser.error(f"sequences absent from remote FASTA index: {missing}")

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        records = list(
            pool.map(
                lambda sequence: fetch_one(args.url, index, sequence, args.destination),
                args.sequences,
            )
        )
    records.sort(key=lambda item: args.sequences.index(str(item["sequence"])))
    manifest = {
        "source_name": args.source_name,
        "source_version": args.source_version,
        "download_url": args.url,
        "retrieval_method": "single HTTP byte range computed from the remote FASTA index",
        "sequences": records,
    }
    manifest_path = args.destination / "reference_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
