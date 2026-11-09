"""Resolve repo root and base Ante Bellum path. Shared by the ABA helper scripts.

AB path order: --ab argument > AB_PATH env var (set per user in .claude/settings.local.json) > sibling ../ab folder.
"""
import os
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
SCAN_DIRS = ["common", "events", "missions", "decisions", "localisation", "customizable_localization",
             "interface", "history"]


def ab_path(explicit=None):
    for cand in (explicit, os.environ.get("AB_PATH"), str(REPO.parent / "ab")):
        if cand and (Path(cand) / "descriptor.mod").exists():
            return Path(cand)
    return None


def need_ab(explicit=None):
    p = ab_path(explicit)
    if p is None:
        raise SystemExit("Base Ante Bellum not found. Set AB_PATH in .claude/settings.local.json "
                         '({"env": {"AB_PATH": "D:/path/to/ab"}}) or pass --ab <path>.')
    return p
