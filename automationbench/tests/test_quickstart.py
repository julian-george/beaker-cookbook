"""Check the real quickstart selection without uploading a dataset."""

from __future__ import annotations

import importlib.util
from collections import Counter
from pathlib import Path

import pytest

from automationbench_skills.data import PUBLIC_DOMAINS, load_quickstart, load_split, quickstart
from automationbench_skills.data.tasks import read_case_names


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("upload_splits", ROOT / ".beaker/upload_splits.py")
assert SPEC is not None and SPEC.loader is not None
upload = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(upload)


def test_reviewed_selection_preserves_split_membership_and_quotas() -> None:
    excluded = set(read_case_names(quickstart.EXCLUDED_CASES))
    original = {split: load_split(split) for split in ("train", "test")}
    assert len(excluded) == 91
    assert excluded <= {sample.task_name for samples in original.values() for sample in samples}
    selected: dict[str, set[str]] = {}
    for split, per_domain in (("train", 6), ("test", 3)):
        samples = load_quickstart(split)
        names = [sample.task_name for sample in samples]
        selected[split] = set(names)
        assert names == read_case_names(quickstart.QUICKSTART_DIR / f"{split}.txt")
        assert len(names) == len(set(names)) == 6 * per_domain
        assert not set(names) & excluded
        assert set(names) <= {sample.task_name for sample in original[split]}
        assert Counter(sample.domain for sample in samples) == dict.fromkeys(PUBLIC_DOMAINS, per_domain)
    assert selected["train"].isdisjoint(selected["test"])


def test_upload_preserves_reviewed_samples() -> None:
    for split in ("train", "test"):
        samples = load_quickstart(split)
        rows = upload._quickstart_rows(split)
        assert len(rows) == len(samples)
        for row, sample in zip(rows, samples, strict=True):
            assert row == {
                "id": sample.task_name,
                "input": {
                    "task_name": sample.task_name,
                    "prompt": "\n\n".join(
                        str(message.get("content") or "") for message in sample.prompt if message.get("role") == "user"
                    ).strip(),
                },
                "expected": {"assertions": sample.info["assertions"]},
                "metadata": {"domain": sample.domain, "source_split": split},
                "group_key": sample.domain,
            }


@pytest.mark.parametrize("problem", ["duplicate", "excluded", "wrong_split", "missing_quota"])
def test_quickstart_rejects_invalid_selection(problem: str, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    names = read_case_names(quickstart.QUICKSTART_DIR / "train.txt")
    if problem == "duplicate":
        names[0] = names[1]
        message = "Duplicate train"
    elif problem == "excluded":
        names[0] = "sales.recency_selection"
        message = "Excluded train"
    elif problem == "wrong_split":
        names[0] = "sales.calendar_crm_meeting"
        message = "absent from frozen train"
    else:
        names.pop()
        message = "exactly 6 cases per domain"
    (tmp_path / "train.txt").write_text("\n".join(names) + "\n")
    monkeypatch.setattr(quickstart, "QUICKSTART_DIR", tmp_path)
    with pytest.raises(ValueError, match=message):
        load_quickstart("train")


@pytest.mark.parametrize(
    ("train_support", "test_support"),
    [
        (
            {"sales.mark_vip_emails_read", "support.zendesk_freshdesk_sync"},
            {"support.intercom_freshdesk_escalation", "hr.salary_band_audit"},
        ),
        (
            {"support.helpcrunch_engagement_scoring", "support.zendesk_hubspot_churn_risk"},
            {"support.helpscout_hubspot_deal_alerts"},
        ),
    ],
)
def test_reviewed_reporting_rules_keep_training_and_test_support(
    train_support: set[str], test_support: set[str]
) -> None:
    # These supporting tasks were identified by source review, not by model scores.
    assert train_support <= set(read_case_names(quickstart.QUICKSTART_DIR / "train.txt"))
    assert test_support <= set(read_case_names(quickstart.QUICKSTART_DIR / "test.txt"))


def test_quickstart_rejects_unknown_split() -> None:
    with pytest.raises(ValueError, match="Unknown quickstart split"):
        load_quickstart("simple")
