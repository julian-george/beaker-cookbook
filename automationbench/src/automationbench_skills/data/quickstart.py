"""Reviewed quickstart selection, shared by dataset consumers and uploaders."""

from __future__ import annotations

from collections import Counter
from pathlib import Path

from automationbench_skills.data.tasks import PUBLIC_DOMAINS, Sample, load_split, read_case_names


QUICKSTART_DIR = Path(__file__).parent / "quickstart_cases"
EXCLUDED_CASES = QUICKSTART_DIR / "excluded_cases.txt"
CASES_PER_DOMAIN = {"train": 6, "test": 3}


def load_quickstart(split: str) -> list[Sample]:
    """Load the reviewed selection; never substitute unreviewed cases."""
    if split not in CASES_PER_DOMAIN:
        raise ValueError(f"Unknown quickstart split: {split!r}")
    per_domain = CASES_PER_DOMAIN[split]
    names = read_case_names(QUICKSTART_DIR / f"{split}.txt")
    if len(names) != len(set(names)):
        raise ValueError(f"Duplicate {split} quickstart cases")
    excluded = set(names) & set(read_case_names(EXCLUDED_CASES))
    if excluded:
        raise ValueError(f"Excluded {split} quickstart cases: {sorted(excluded)}")
    by_name = {sample.task_name: sample for sample in load_split(split)}
    missing = set(names) - by_name.keys()
    if missing:
        raise ValueError(f"Quickstart cases absent from frozen {split} split: {sorted(missing)}")
    samples = [by_name[name] for name in names]
    counts = Counter(sample.domain for sample in samples)
    if counts != dict.fromkeys(PUBLIC_DOMAINS, per_domain):
        raise ValueError(f"Quickstart {split} needs exactly {per_domain} cases per domain: {dict(counts)}")
    return samples
