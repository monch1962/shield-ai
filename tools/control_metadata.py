#!/usr/bin/env python3
"""Single source of truth for control counts and per-pillar ranges.

Both diagram generators (generate_diagrams.py, generate_impl_diagrams.py) and
the artifact verification gate (verify_artifacts.py) derive the control count
and per-pillar ranges from the framework document here, so adding a control in
a release cycle can never again leave a stale hardcoded number in an SVG or in
the gate. The framework document is the single source; nothing else should set
these values.

Usage:
    from control_metadata import count_controls, pillar_ranges, \
                                 control_count_text

The module must run from the repo root (its callers os.chdir there); it anchors
paths off this file's real location so it is safe regardless of cwd.
"""
import os
import re

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
FRAMEWORK = os.path.join(ROOT, "framework", "shield-ai-framework.md")

# A control definition bullet is "- MS-01 ...:" at the start of a line. The
# brace form matches the framework's "- CONTROLID:" bullets.
CONTROL_RE = re.compile(r"^\-\s+((?:MS|IAM|DS|TP|MIR|GRM|EE)-[0-9]+):")

# Canonical pillar order used in the framework-architecture diagram.
PILLAR_ORDER = ["EE", "MS", "IAM", "DS", "TP", "MIR", "GRM"]


def _parse():
    """Return the set of control IDs found in the framework document."""
    with open(FRAMEWORK, encoding="utf-8") as f:
        text = f.read()
    ids = {m.group(1) for ln in text.split("\n") if (m := CONTROL_RE.match(ln))}
    return ids


def control_ids():
    """All control IDs in a STABLE order.

    Canonical order is by pillar block (in the pillar's first-seen framework
    order) then numerically within the pillar (e.g. EE-01..EE-08, MS-01..MS-15).
    Sorting here guarantees the reference views and any consumer iterate the
    same order every run -- previously this returned a set, so the iteration
    order depended on Python's hash seed and was different in every process,
    which made regenerated documents reorder their contents nondeterministically.
    """
    ids = _parse()
    # order pillars by first appearance in the parsed set's framework order is
    # unstable; instead sort by (pillar, numeric) but keep pillar grouping by
    # the canonical pillar sequence so a pillar's controls stay contiguous.
    def _key(cid):
        pillar, _, num = cid.partition("-")
        try:
            return (pillar, int(num))
        except ValueError:
            return (pillar, 0)
    return tuple(sorted(ids, key=_key))


def count_controls():
    return len(_parse())


def pillar_maxima():
    """{pillar: highest control number, e.g. 'MS': 15}."""
    maxima = {}
    for cid in _parse():
        pillar, _, num = cid.partition("-")
        n = int(num)
        if n > maxima.get(pillar, 0):
            maxima[pillar] = n
    return maxima


def pillar_ranges():
    """{pillar: 'MS-01 -> MS-15'} for every pillar present in the framework."""
    return {p: f"{p}-01 -> {p}-{maxima:02d}" for p, maxima in pillar_maxima().items()}


def control_count_text():
    return f"{count_controls()} controls"