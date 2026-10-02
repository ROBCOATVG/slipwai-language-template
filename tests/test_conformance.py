"""This package against the conformance suite of the slipwai it is tested with (FR-030, D81).

The language directory is the one this package sits in, so a copy under `~/.slipwai/languages` is checked against
that directory, and this repository's own checkout against its parent. Each check is one test, failing with what is
missing: `python -m slipwai.conformance <language-dir> toy` prints the same report. Rename `package` with the
directory.
"""
from __future__ import annotations

from pathlib import Path

from slipwai import conformance


class Conformance(conformance.ConformanceCase):
    language_dir = Path(__file__).resolve().parents[2]
    package = "toy"
