from __future__ import annotations

import argparse
from pathlib import Path

from src.datasets.manifest import load_manifest, write_split_manifests
from src.datasets.splitter import signer_wise_split


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create signer-isolated train, validation, and test manifests."
    )
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    rows = load_manifest(args.manifest)
    split = signer_wise_split(rows)
    paths = write_split_manifests(split, args.output)
    print(f"Train manifest: {paths['train']}")
    print(f"Validation manifest: {paths['validation']}")
    print(f"Test manifest: {paths['test']}")


if __name__ == "__main__":
    main()
