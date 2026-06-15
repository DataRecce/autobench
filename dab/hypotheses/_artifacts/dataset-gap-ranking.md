# Dataset gap ranking — Opus incumbent (`@baseline`)

Concept/ideate selection input — which dataset+queries to target. Lower
`dataset_pass_at_1` = more headroom = higher research priority.

Source: `dab/runs/opus-4-8-baseline/e14e49869e6412de/summary.json` (converted Opus-4.8 xhigh
+hints incumbent; 54 queries across 12 datasets; stratified Pass@1 = 0.6535866910866911).
Sorted ASCENDING by `dataset_pass_at_1` (lowest first). Failing query ids = the per-query
`pass_at_1: 0.0` entries; task ids are `{dataset}-q{n}`.

| dataset | dataset_pass_at_1 | n_queries | failing query ids |
|---------|-------------------|-----------|-------------------|
| PATENTS | 0.0 | 3 | PATENTS-q1, PATENTS-q2, PATENTS-q3 |
| GITHUB_REPOS | 0.25 | 4 | GITHUB_REPOS-q1, GITHUB_REPOS-q2, GITHUB_REPOS-q4 |
| agnews | 0.25 | 4 | agnews-q2, agnews-q3, agnews-q4 |
| DEPS_DEV_V1 | 0.5 | 2 | DEPS_DEV_V1-q1 |
| PANCANCER_ATLAS | 0.6666666666666666 | 3 | PANCANCER_ATLAS-q1 |
| googlelocal | 0.75 | 4 | googlelocal-q2 |
| crmarenapro | 0.7692307692307693 | 13 | crmarenapro-q2, crmarenapro-q3, crmarenapro-q8 |
| stockmarket | 0.8 | 5 | stockmarket-q4 |
| yelp | 0.8571428571428571 | 7 | yelp-q6 |
| bookreview | 1.0 | 3 | — (all pass) |
| music_brainz_20k | 1.0 | 3 | — (all pass) |
| stockindex | 1.0 | 3 | — (all pass) |

**Highest-headroom targets:** PATENTS (0/3, whole dataset failing), then agnews and
GITHUB_REPOS (both 0.25). The three perfect datasets (bookreview, music_brainz_20k,
stockindex) are the natural sentinel/canary pool — pick currently-passing queries from them
to guard against regression in a generative lever's smoke set.
