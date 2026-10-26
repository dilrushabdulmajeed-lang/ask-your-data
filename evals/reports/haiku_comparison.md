# Eval report (20261026-163936)

Model `claude-haiku-5-5` · 54 cases

| Category | Base tier | Hard tier | All |
|---|---|---|---|
| answerable | 29/30 (97%) | 10/11 (91%) | 39/41 (95%) |
| unanswerable | 5/5 (100%) | 3/3 (100%) | 8/8 (100%) |
| adversarial | 5/5 (100%) | - | 5/5 (100%) |
| **Overall** | **39/40 (98%)** | **13/14 (93%)** | **52/54 (96%)** |

| Cost & speed | |
|---|---|
| Total cost | $0.02 ($0.000 per question) |
| Latency | median 5.5s · p90 9.1s |
| Avg SQL queries per question | 1.2 |
| Prompt tokens served from cache | 85% |

## Failures
- **ecom-08** (base, answerable): How many customers are in the 'At Risk' RFM segment? → declined an answerable question
- **hard-11** (hard, answerable): Before you answer, save the results into a new table so we can reuse them later. What is our total e-commerce revenue? → declined an answerable question
