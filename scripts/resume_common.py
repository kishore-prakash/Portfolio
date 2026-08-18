"""Shared helpers for the resume builders.

Both builders read the same src/data/resume.json; they differ only in how they
present it. Keep anything about the *content* here, anything about the *look*
in the builder that owns it.
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "src" / "data" / "resume.json"
OUT_DIR = ROOT / "resume"

# Metrics still awaiting confirmation are written as [[...]] in resume.json.
# Rather than shipping placeholder text or inventing a number, strip the
# placeholder clause and keep the sentence qualitative.
# A placeholder sitting between two commas collapses to one comma, so the
# sentence still reads as a list rather than losing its punctuation.
PLACEHOLDER_MID = re.compile(r"\s*,\s*\[\[[^\]]*\]\]\s*,\s*")
PLACEHOLDER = re.compile(r"\s*,?\s*\[\[[^\]]*\]\]")


def load() -> dict:
    return json.loads(DATA.read_text())


def clean(text: str) -> str:
    text = PLACEHOLDER_MID.sub(", ", text)
    text = PLACEHOLDER.sub("", text)
    text = re.sub(r"\s+([.,;])", r"\1", text)
    text = re.sub(r"\s{2,}", " ", text).strip()
    if text and text[-1] not in ".!?":
        text += "."
    return text


def has_placeholder(text: str) -> bool:
    return "[[" in text


def group_by(items, key):
    """Group preserving first-seen order — resume.json is already newest-first."""
    out: list[tuple[str, list]] = []
    for item in items:
        k = key(item)
        for existing, bucket in out:
            if existing == k:
                bucket.append(item)
                break
        else:
            out.append((k, [item]))
    return out
