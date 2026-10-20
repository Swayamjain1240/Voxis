from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from src.contracts.avatar_coverage import audit_avatar_coverage
from src.contracts.label_map import load_label_map


def load_clip_names(path: Path | None) -> list[str]:
    if path is None or not path.exists():
        return []
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if isinstance(payload, dict):
        payload = payload.get("clips", [])
    if not isinstance(payload, list):
        raise ValueError("Avatar clip registry must be a list or an object with clips.")
    names = []
    for item in payload:
        if isinstance(item, str):
            names.append(item)
        elif isinstance(item, dict) and item.get("gloss"):
            names.append(str(item["gloss"]))
        elif isinstance(item, dict) and item.get("name"):
            names.append(str(item["name"]))
    return names


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit avatar coverage for the frozen VOXIS vocabulary.")
    parser.add_argument("--registry", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    coverage = audit_avatar_coverage(load_clip_names(args.registry))
    report = {
        "vocabulary_version": load_label_map().version,
        "registry": str(args.registry) if args.registry else None,
        "available_count": len(coverage["supported"]),
        "required_count": len(load_label_map().gloss_to_label),
        **coverage,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
