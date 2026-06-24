# spider2-dbt — unexpected-result playbook

Follow this fixed diagnostic ladder when a result is UNEXPECTED — a smoke GO that didn't translate to
full, a flip that didn't reproduce, an unexpected regression, or a score below `@baseline`. Do NOT
promote / reject / revise on the headline number alone.

1. **Match the reference + per-task diff.** Resolve `@baseline`
   (`export RAZORBACK_REGISTRY=/home/kent/autobench/spider2-dbt/razorback-registry.yaml`,
   `rk registry resolve run @baseline`). `rk runs diff` CRASHES on these run-dirs (query_id is null —
   single `default` stratum); compute the paired delta from `per_trial_outcomes.json` instead: slug-pair
   each task's reward (variant vs `@baseline`), bootstrap (10k) the paired difference. List EVERY task
   that changed verdict in BOTH directions.

2. **Read the moved cells' artifacts.** For each verdict change, open
   `runs/<experiment>/<hash>/spider2-dbt-<task>__<short>/`: the verifier stdout (missing gold table?
   which columns/values mismatched? grain off?), `reward.json` / `validation.json`, and the committed
   dbt model SQL + built table. A flip is only *lever* evidence if the README wording is why the built
   table changed.

3. **Separate infra from signal.** A build-time **preflight failure**, a packager **source-schema-align**
   crash, a missing materialized view, or a stale job-dir lock is NEVER a result — recover/relaunch.
   Goldless and postgres-backed tasks are non-signal. Strict audit (`coverage_missing`, taint) gates
   trust in the score.

4. **State causation at the honest ceiling.** `trials: 1` proves nothing about reproducibility on its
   own — a single flip can be variance even with no model-swap confound (the model is gpt-5.5 on both
   sides, but it is still nondeterministic). A flip confirmed by the committed artifact + held canaries
   is the bar; a single unexplained flip is not. If reproducibility is in doubt, a cheap same-task
   multi-draw probe (a smoke spec with the one task, `concurrency.trials: 1`, run a few times) settles
   variance vs signal.

5. **Smoke-vs-full fork drift.** If a smoke GO failed/regressed at full, name what the smoke set could
   not see (a family it didn't sample, a different model branch the rule drifted into) and feed it into
   the entity's `## Failure Review` / follow-up routing.
