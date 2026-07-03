#!/usr/bin/env python3
"""Update contents.json with a new FEXCore release entry."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--contents",
        type=Path,
        default=Path("contents.json"),
        help="Path to contents.json (default: contents.json)",
    )
    parser.add_argument(
        "--version-name",
        required=True,
        help="Version suffix, e.g. 2607-abc1234",
    )
    parser.add_argument(
        "--remote-url",
        required=True,
        help="Direct download URL for the .wcp asset",
    )
    parser.add_argument(
        "--type",
        default="FEXCore",
        help="Component type (default: FEXCore)",
    )
    return parser.parse_args()


def load_contents(path: Path) -> list[dict[str, Any]]:
    if not path.exists() or path.stat().st_size == 0:
        return []

    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)

    if not isinstance(data, list):
        raise ValueError(f"{path} must contain a JSON array")

    return data


def build_entry(
    component_type: str,
    version_name: str,
    remote_url: str,
) -> dict[str, str]:
    full_name = (
        version_name
        if version_name.startswith("FEXCore-")
        else f"FEXCore-{version_name}"
    )
    return {
        "type": component_type,
        "verName": full_name,
        "verCode": "0",
        "remoteUrl": remote_url,
    }


def upsert_entry(
    contents: list[dict[str, Any]],
    entry: dict[str, str],
) -> list[dict[str, Any]]:
    filtered = [
        item
        for item in contents
        if not (
            item.get("type") == entry["type"]
            and item.get("verName") == entry["verName"]
        )
    ]
    return [entry, *filtered]


def write_contents(path: Path, contents: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(contents, handle, indent=2)
        handle.write("\n")


def main() -> int:
    args = parse_args()
    entry = build_entry(args.type, args.version_name, args.remote_url)

    try:
        contents = load_contents(args.contents)
        updated = upsert_entry(contents, entry)
        write_contents(args.contents, updated)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(f"Updated {args.contents} with {entry['verName']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
