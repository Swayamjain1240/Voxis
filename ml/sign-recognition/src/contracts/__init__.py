"""Versioned contracts shared by offline sign-recognition tooling."""

from .label_map import CanonicalLabelMap, load_label_map

__all__ = ["CanonicalLabelMap", "load_label_map"]
