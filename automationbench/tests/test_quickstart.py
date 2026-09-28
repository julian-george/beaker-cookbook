"""Check the real quickstart selection without uploading a dataset."""

from __future__ import annotations

import importlib.util
from collections import Counter
from pathlib import Path

import pytest

from automationbench_skills.data import PUBLIC_DOMAINS, load_quickstart, load_split, quickstart


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("upload_splits", ROOT / ".beaker/upload_splits.py")
assert SPEC is not None and SPEC.loader is not None
upload = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(upload)


def test_quickstart_matches_reviewed_selection_and_preserves_source() -> None:
    excluded = set(quickstart._read_names(quickstart.EXCLUDED_CASES))
    assert len(excluded) == 91
    original = {split: load_split(split) for split in ("train", "test")}
    assert excluded <= {sample.task_name for samples in original.values() for sample in samples}
    selected: dict[str, set[str]] = {}
    for split, per_domain, replaced in (("train", 6, 14), ("test", 3, 9)):
        samples = load_quickstart(split)
        rows = upload._quickstart_rows(split)
        assert [sample.task_name for sample in samples] == [row["id"] for row in rows]
        ids = [row["id"] for row in rows]
        selected[split] = set(ids)
        assert ids == quickstart._read_names(quickstart.QUICKSTART_DIR / f"{split}.txt")
        assert len(ids) == len(set(ids)) == 6 * per_domain
        assert not set(ids) & excluded
        by_name = {sample.task_name: sample for sample in original[split]}
        assert set(ids) <= by_name.keys()
        assert Counter(row["group_key"] for row in rows) == dict.fromkeys(PUBLIC_DOMAINS, per_domain)
        initial = {
            sample.task_name
            for domain in PUBLIC_DOMAINS
            for sample in [s for s in original[split] if s.domain == domain][:per_domain]
        }
        assert len(initial - set(ids)) == replaced
        for row in rows:
            sample = by_name[row["id"]]
            assert row["input"] == {"task_name": sample.task_name, "prompt": upload._user_prompt(sample)}
            assert row["expected"] == {"assertions": sample.info["assertions"]}
            assert row["metadata"] == {"domain": sample.domain, "source_split": split}
        assert rows == upload._quickstart_rows(split)
    assert selected["train"].isdisjoint(selected["test"])


@pytest.mark.parametrize("problem", ["duplicate", "excluded", "wrong_split", "missing_quota"])
def test_quickstart_rejects_invalid_selection(problem: str, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    names = quickstart._read_names(quickstart.QUICKSTART_DIR / "train.txt")
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
    assert train_support <= set(quickstart._read_names(quickstart.QUICKSTART_DIR / "train.txt"))
    assert test_support <= set(quickstart._read_names(quickstart.QUICKSTART_DIR / "test.txt"))


def test_quickstart_rejects_unknown_split() -> None:
    with pytest.raises(ValueError, match="Unknown quickstart split"):
        load_quickstart("simple")
