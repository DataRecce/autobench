# Group-3 Phase 2 — stronger-solver-model/runtime scoping (NOT launched; captain greenlights)

**Premise:** the multi-step reachable group-3 cells (xero001/xero_new001/xero_new002, synthea001, provider001,
asana001, social_media001) were handed their exact recipe via README (spd0021/27/28/29) and ALL went NO-GO —
the wall is *execution*, not knowledge: gpt-5.5 can't reliably build the multi-step dbt. The leaderboard
top-1 (65%) proves a stronger method exists. The one substrate lever we've NEVER varied is the solver model.

## What's available (from razorback `spacedock_solver`)
- `agent.runtime` accepts **`claude | codex | pi`** (spacedock_solver.py:145). All 76 of our specs used
  `runtime: codex, model: gpt-5.5`. So two untested directions:
  1. **Stronger codex model** — swap `model: gpt-5.5` → a stronger codex-family model (if one is provisioned
     for the codex CLI in Harbor). Lowest-friction (one spec field).
  2. **`runtime: claude` + a strong Claude model (e.g. Opus 4.8)** — bigger change: different auth
     (`ANTHROPIC_API_KEY` xor `CLAUDE_CODE_OAUTH_TOKEN`, see spacedock_solver.py:177-180), different plugin
     staging, different solving behavior. Highest ceiling.

## Open questions to resolve BEFORE a run (captain + infra)
1. **Which stronger model is actually provisioned** for the Harbor solver container (codex side) — need to
   confirm a concrete model id exists and is authed; gpt-5.5 may already be the strongest codex option.
2. **Auth for runtime:claude** — is an ANTHROPIC_API_KEY / OAuth token available to the solver container
   without violating the no-public-lookup guard? (razorback proxies are locked down.)
3. **Cost/credit** — a stronger model + the Jul-2 codex window. A model-swap re-baselines EVERYTHING (new
   solver substrate), so it needs its own champion re-baseline full board after, not just a smoke.

## Proposed cheap first test (once a model is confirmed available)
Hold the README = new champion spd0038; vary ONLY the model/runtime; smoke a 5-cell sample of the
multi-step reachable cells that README couldn't crack + 2 rock-solid canaries, trials=1:
- targets: xero001, synthea001, provider001, asana001, social_media001
- canaries: mrr001, quickbooks002
**Signal:** if a stronger model flips ≥2-3 of these (that gpt-5.5 never passed), the model IS the lever to
65% → then full re-baseline + promote. If it flips 0, the wall is deeper (scaffold/benchmark) and model-swap
alone isn't the answer.

## Status
SCOPING ONLY. Blocked on Q1/Q2 (what model is available + auth). Captain: confirm a concrete stronger model
id + auth path, then this becomes a fireable hypothesis (spd00xx). Phase 1 (single-mechanism README cells,
spd0039) proceeds in parallel now.
