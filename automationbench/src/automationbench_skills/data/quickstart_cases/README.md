# Reviewed quickstart selection

The committed [training list](train.txt) and [test list](test.txt) contain the
reviewed 54-case demo: **36 train / 18 test**, with **6 train / 3 test per domain**.
`automationbench_skills.data.load_quickstart()` loads these exact IDs in order
and returns the pinned benchmark's original prompts and assertions. No task moves between the frozen full splits.

## Selection policy

The September 28, 2026 review recommends excluding 91 of the 600 public cases:
56 task/rubric mismatches, 24 grading defects, and 11 cases without enough
training examples for an implicit rule. The full-pool policy requires two
independent, consistent training tasks. The demo requires two training tasks
and at least one test task. Explicit instructions and requested calculations
need no cross-task support. Harness-only limitations remain code optimization
targets and do not, by themselves, require exclusion.

The [exclusion list](excluded_cases.txt) prevents reintroducing these 91 cases.
[Reasons and source links for all 91 exclusions](EXCLUSIONS.md) are recorded separately.
Replacement tasks must be reviewed before changing the committed lists.

## Counts

| Bucket | Full dataset (600) | Original demo train (36) | Original demo test (18) |
|---|---:|---:|---:|
| Task/rubric mismatches | 56 (9.3%) | 7 (19.4%) | 4 (22.2%) |
| Grading defects | 24 (4%) | 0 (0%) | 2 (11.1%) |
| Insufficient training support | 11 (1.8%) | 7 (19.4%) | 3 (16.7%) |
| **Excluded / replaced** | **91 (15.2%)** | **14 (38.9%)** | **9 (50%)** |

Each case is counted in one bucket; percentages use the column's original size.
The task/rubric bucket includes two demo-only instruction conflicts, and the
training-support bucket includes four demo-only coverage exclusions. These six
are outside the 91 full-pool exclusions.

The revised demo keeps 31 original tasks and replaces **23 of 54 (42.6%)**;
it still contains **36 train / 18 test** cases.

| Domain | Before | After | Train | Test |
|---|---:|---:|---:|---:|
| Finance | 9 | 9 | 6 | 3 |
| HR | 9 | 9 | 6 | 3 |
| Marketing | 9 | 9 | 6 | 3 |
| Operations | 9 | 9 | 6 | 3 |
| Sales | 9 | 9 | 6 | 3 |
| Support | 9 | 9 | 6 | 3 |
| **Total** | **54** | **54** | **36** | **18** |

## Supported reporting rules

| Rule | Training examples | Test examples |
|---|---|---|
| Report the total number processed or affected | `sales.mark_vip_emails_read`, `support.zendesk_freshdesk_sync` | `support.intercom_freshdesk_escalation`, `hr.salary_band_audit` |
| Report counts beside named outcome categories | `support.helpcrunch_engagement_scoring`, `support.zendesk_hubspot_churn_risk` | `support.helpscout_hubspot_deal_alerts` |

Use the task's classification rules and actual counts. Do not add skipped-record
counts or override explicit reporting instructions. These examples support the
reporting procedure, not shared classification thresholds across different tasks.

## Why original demo cases are replaced

| Split | Case | Reason for replacement |
|---|---|---|
| Train | [`finance.slack_receipt_capture`](https://github.com/zapier/AutomationBench/blob/4a8e1061254004d9dac807054eed33fad7d1ff14/automationbench/domains/finance/tasks.py#L1608) | Approval depends on inferring the attendee count from “client lunch”, although the meal policy requires that count for an over-limit receipt. |
| Train | [`hr.probation_review_reminder`](https://github.com/zapier/AutomationBench/blob/4a8e1061254004d9dac807054eed33fad7d1ff14/automationbench/domains/hr/tasks.py#L2198) | Exclude because the rubric requires a reminder outside the supplied 30-day notification window. |
| Train | [`marketing.campaign_launch_checklist`](https://github.com/zapier/AutomationBench/blob/4a8e1061254004d9dac807054eed33fad7d1ff14/automationbench/domains/marketing/tasks.py#L1925) | Exclude because the rubric requires an email even though the unresolved blocker means the task’s condition for sending that email is not met. |
| Train | [`operations.asana_fire_drill`](https://github.com/zapier/AutomationBench/blob/4a8e1061254004d9dac807054eed33fad7d1ff14/automationbench/domains/operations/tasks.py#L32) | The exact “Due: 2026-02-18” Slack phrase has only one training example and no matching test. |
| Train | [`operations.calendar_airtable_maintenance`](https://github.com/zapier/AutomationBench/blob/4a8e1061254004d9dac807054eed33fad7d1ff14/automationbench/domains/operations/tasks.py#L1479) | Only one matching training case. Supplied names make a passing route reasonable, but do not provide two independent training examples of the exact-copy convention. |
| Train | [`operations.drive_notion_archive`](https://github.com/zapier/AutomationBench/blob/4a8e1061254004d9dac807054eed33fad7d1ff14/automationbench/domains/operations/tasks.py#L1296) | Only one training case supports the unrequested raw-ID requirement. The folder/tool problem is a separate harness flag. |
| Train | [`sales.format_ambiguity`](https://github.com/zapier/AutomationBench/blob/4a8e1061254004d9dac807054eed33fad7d1ff14/automationbench/domains/sales/tasks.py#L1334) | Conflicting instructions—unclear which applies: the [contact record](https://github.com/zapier/AutomationBench/blob/4a8e1061254004d9dac807054eed33fad7d1ff14/automationbench/domains/sales/tasks.py#L1451) prohibits title changes, while the [HR email](https://github.com/zapier/AutomationBench/blob/4a8e1061254004d9dac807054eed33fad7d1ff14/automationbench/domains/sales/tasks.py#L1382) announces an immediate promotion. [Criterion 0](https://github.com/zapier/AutomationBench/blob/4a8e1061254004d9dac807054eed33fad7d1ff14/automationbench/domains/sales/tasks.py#L1526) requires the update. Demo-only exclusion; the HR email could reasonably resolve the earlier freeze. |
| Train | [`sales.multi_hop_lookup`](https://github.com/zapier/AutomationBench/blob/4a8e1061254004d9dac807054eed33fad7d1ff14/automationbench/domains/sales/tasks.py#L53) | Only one training case supports inherited escalation routing. Explicit parent-industry rules concern a different decision. |
| Train | [`sales.recency_selection`](https://github.com/zapier/AutomationBench/blob/4a8e1061254004d9dac807054eed33fad7d1ff14/automationbench/domains/sales/tasks.py#L788) | The supplied audit instruction does not establish these extra note requirements. This entry does not rely on the competing policy in the account description. |
| Train | [`support.helpscout_jira_bugs`](https://github.com/zapier/AutomationBench/blob/4a8e1061254004d9dac807054eed33fad7d1ff14/automationbench/domains/support/tasks.py#L706) | The required triaged tag is absent from the task and configuration. The recommendation is to supply the configured processed-tag value. Repeated tickets within this one case do not establish an independently supported convention. |
| Train | [`support.intercom_demo_scheduling`](https://github.com/zapier/AutomationBench/blob/4a8e1061254004d9dac807054eed33fad7d1ff14/automationbench/domains/support/tasks.py#L3540) | For criterion 45, the policy requires “unable to schedule a demo” while the guard prohibits “schedule”. |
| Train | [`support.zendesk_hubspot_org_sync`](https://github.com/zapier/AutomationBench/blob/4a8e1061254004d9dac807054eed33fad7d1ff14/automationbench/domains/support/tasks.py#L4948) | The success-summary wording rule lacks two training tasks and a matching test in this demo. It remains eligible in the full pool. |
| Train | [`support.zendesk_sf_case_sync`](https://github.com/zapier/AutomationBench/blob/4a8e1061254004d9dac807054eed33fad7d1ff14/automationbench/domains/support/tasks.py#L30) | The unstated skipped-ticket count has only one training example and no matching test. Processed totals support a different rule. |
| Train | [`support.zoho_sf_enrichment`](https://github.com/zapier/AutomationBench/blob/4a8e1061254004d9dac807054eed33fad7d1ff14/automationbench/domains/support/tasks.py#L2202) | Only one training case supports these unspecified phrases. |
| Test | [`hr.job_posting_distribution`](https://github.com/zapier/AutomationBench/blob/4a8e1061254004d9dac807054eed33fad7d1ff14/automationbench/domains/hr/tasks.py#L770) | Exclude for the unrecognized job-posting action. The task’s suggested tool list names `recruitee_create_offer`, which can pass; the claim is not that the supported route is impossible to discover. |
| Test | [`marketing.ad_performance_review`](https://github.com/zapier/AutomationBench/blob/4a8e1061254004d9dac807054eed33fad7d1ff14/automationbench/domains/marketing/tasks.py#L1022) | Correct CPA $165.38 is rejected; whole-dollar rounding is not specified. |
| Test | [`marketing.lead_enrichment`](https://github.com/zapier/AutomationBench/blob/4a8e1061254004d9dac807054eed33fad7d1ff14/automationbench/domains/marketing/tasks.py#L268) | A confirmation that puts the code in the required subject can fail the body-only check. |
| Test | [`operations.notion_gmail_checklist_update`](https://github.com/zapier/AutomationBench/blob/4a8e1061254004d9dac807054eed33fad7d1ff14/automationbench/domains/operations/tasks.py#L3577) | The guard cannot distinguish publishing the draft from correctly explaining its exclusion. No baseline example is asserted here. |
| Test | [`operations.trello_vendor_hold_email`](https://github.com/zapier/AutomationBench/blob/4a8e1061254004d9dac807054eed33fad7d1ff14/automationbench/domains/operations/tasks.py#L2370) | Only one matching training case. Date-only or move-only updates do not teach the requirement to combine both fields. |
| Test | [`sales.advance_opportunity_stage`](https://github.com/zapier/AutomationBench/blob/4a8e1061254004d9dac807054eed33fad7d1ff14/automationbench/domains/sales/tasks.py#L6879) | The required tie-breaker is not stated and has no supporting training example. |
| Test | [`sales.apply_project_label`](https://github.com/zapier/AutomationBench/blob/4a8e1061254004d9dac807054eed33fad7d1ff14/automationbench/domains/sales/tasks.py#L5781) | Conflicting instructions—unclear which applies: the [PM says to follow the spreadsheet exactly](https://github.com/zapier/AutomationBench/blob/4a8e1061254004d9dac807054eed33fad7d1ff14/automationbench/domains/sales/tasks.py#L5999), but a [later VP email](https://github.com/zapier/AutomationBench/blob/4a8e1061254004d9dac807054eed33fad7d1ff14/automationbench/domains/sales/tasks.py#L5982) changes its exclusions. [Criteria 6](https://github.com/zapier/AutomationBench/blob/4a8e1061254004d9dac807054eed33fad7d1ff14/automationbench/domains/sales/tasks.py#L6051) and [9](https://github.com/zapier/AutomationBench/blob/4a8e1061254004d9dac807054eed33fad7d1ff14/automationbench/domains/sales/tasks.py#L6069) still require the spreadsheet rules. Demo-only exclusion. |
| Test | [`support.freshdesk_faq_drafts`](https://github.com/zapier/AutomationBench/blob/4a8e1061254004d9dac807054eed33fad7d1ff14/automationbench/domains/support/tasks.py#L5676) | The Always Draft override does not clearly require replacing the still-accurate Low confidence label with FAQ match. |
| Test | [`support.helpscout_weekly_report`](https://github.com/zapier/AutomationBench/blob/4a8e1061254004d9dac807054eed33fad7d1ff14/automationbench/domains/support/tasks.py#L4539) | The exact “Total: N” summary format lacks the required training support in this demo. It remains eligible in the full pool. |

## Scope

Source review used benchmark commit
[`4a8e106`](https://github.com/zapier/AutomationBench/tree/4a8e1061254004d9dac807054eed33fad7d1ff14).
These are selection decisions, not claims that every excluded task is impossible
or that every retained task is defect-free. No new agent evaluation was run.
The full 450/150 split files and local `run --split` behavior are unchanged.
Existing hosted datasets change only when `.beaker/upload_splits.py` is run.
