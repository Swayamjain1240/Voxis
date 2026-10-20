from __future__ import annotations

from collections.abc import Iterable

from src.contracts.label_map import load_label_map


def audit_avatar_coverage(available_glosses: Iterable[str]) -> dict[str, list[str]]:
    canonical = set(load_label_map().gloss_to_label)
    available = {
        str(gloss).strip().upper()
        for gloss in available_glosses
        if str(gloss).strip()
    }
    return {
        "supported": sorted(canonical & available),
        "missing": sorted(canonical - available),
        "unexpected": sorted(available - canonical),
    }
