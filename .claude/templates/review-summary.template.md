# Review Summary — {{PROJECT_NAME}}

Aggregated outputs of `/mock-4-review`. Each sub-review is a separate file in `reviews/`; this file is the creator-facing roll-up.

## Gate status

| Gate | Status | File |
|------|--------|------|
| NotebookLM typicality | {{STATUS}} | `reviews/notebooklm-review.md` |
| Spec-check | {{STATUS}} | `reviews/spec-check.md` |
| Assessment design | {{STATUS}} | `reviews/assessment-design.md` |
| Spec-examiner | {{STATUS}} | `reviews/spec-examiner.md` |
| Student-simulator | {{STATUS}} | `reviews/student-simulator.md` |
| Marking-realism | {{STATUS}} | `reviews/marking-realism.md` |
| CQI scorecard | {{SCORE}}/50 — {{PASS_FAIL}} | `reviews/cqi-scorecard.md` |

**Publish gate:** {{OPEN_OR_BLOCKED}} — cannot run `/mock-5-publish` unless all gates show `pass` and CQI ≥ 43/50.

## Critical issues (must fix before publish)

<!-- Aggregated from all sub-reviews, deduplicated, severity Critical only. -->

1. **Q{{N}}.{{P}}** — {{ISSUE}} (source: {{REVIEWER}})

## Recommended (should fix)

1. ...

## Minor (could fix)

1. ...

## Creator prompt

Next step options:
- **Apply all critical fixes now:** run `/mock-3-draft --fix Q{{N}}` for each, then re-run `/mock-4-review`.
- **Apply critical + recommended:** same, with wider scope.
- **Defer:** mark `project.json.reviews.*` as `reviewed_with_deferrals` and proceed at your own risk.
