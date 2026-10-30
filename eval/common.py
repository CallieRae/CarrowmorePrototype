"""Shared helpers for the evaluation scripts."""
import re


def norm(text):
    """Collapse templated variants: case, numbers, punctuation and spacing.

    'Isolated No.1 transformer' and 'isolated no 2 transformer' become the same
    sentence, so each is graded once.
    """
    s = text.lower()
    s = re.sub(r"\d+(\.\d+)?", "#", s)
    s = re.sub(r"[^a-z# ]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()
