# DAB Self-Learning Log

Append one entry per concluded hypothesis: verdict (PASSED/REJECTED), the concrete dial it
moved or ruled out, and the transferable takeaway. Keyed to committed-artifact evidence.
- dab0009 (anti-abstention) REJECTED as board lever: real flip on googlelocal-q3 (3/3) but net -0.010 vs matched ref; generative lever perturbs 6/7-stable cells it never touches (related-not-causal per 5 Opus + 5 CAIS run-history). Lean v2 (None carve-out + failure-gated db_config) sim-cleared the 2 perturbation risks -> dab0010. Diagnostic logic codified in unexpected-result-playbook.md.
- dab0010 (anti-abstention LEAN v2) REJECTED: mechanism-cleared of causation but two STABLE cells (crmarenapro-q7/q12, 6/7+) came in 1/3 — captain bar: destabilizing stable cells is unacceptable regardless of causation. Anti-abstention family concluded (v1 net-neg, v2 cleared-but-destabilizing). Lesson: a global README lever can't PROVE stable-cell safety at low trial counts; next lever must be precondition-gated + judged vs a multi-trial no-lever baseline. -> built the multi-trial baseline artifact _artifacts/baseline-variance-6draw.md (no entity needed).
- dab0008 (gpt-5.5 @HIGH tier control) REJECTED: high 0.5733 < xhigh 0.6002 < Opus 0.6536; NO tier advantage (gap within single-trial noise + 3 stable-cell single-draw misses). dab0005 premise REFUTED — crmarenapro-q2/q8 fail clean at high (0/6 never-pass); prior gpt-high 1/1 was a single-draw phantom (same trap as dab0009/dab0010). KEEP xhigh as the no-lever tier. Two highest-EV families (anti-abstention, tier) now both closed.

## dab0012 (REJECTED, 2026-06-18) — README cannot suppress output-shape at gpt-5.5
stockmarket-q3 (gpt 0/6, computes the right ranking, fails only by decorating each row with the
company description). Two mechanism-distinct README levers both INERT by committed artifact:
cycle 1 generation-time prose rule (smoke 9eee91ea), cycle 2 executable verify-stage strip
(smoke 6884375f — discussed in transcript, not applied; clean read, canaries held). Boundary:
output-shape suppression is unreachable via the solver README — it's a generation-time "be helpful"
reflex the model doesn't perceive as wrong, the README has no enforcement under it, and self-verify
is correlated with the error. Fix is verifier-side (benchmark change), not a solver lever. Pre-empts
dab0013/dab0014 (same axis). Full reason+suggestion: _artifacts/readme-cannot-suppress-output-shape.md

## dab0015 (VALIDATED, NOT PROMOTED, 2026-06-19) — flat-string serialization works (1 cell)
First gpt-5.5 lever to GO. A `## Answers` README rule pinning flat-string (not JSON) serialization,
framed as a matcher-correctness consequence. Attributable result: googlelocal-q2 ONLY — 2/6 baseline →
adopted the flat-string committed artifact and PASS across 3 consecutive draws (smoke + full-1 + full-2).
~1 cell, ~+1.4 pts stratified (within the ±3 noise floor). Zero lever-caused regression across 54 cells
(over-flatten falsifier never fired). yelp-q6 DOWNGRADED on FO artifact re-check: 4/6 baseline, one
lever-draw, full-list form is not lever-specific, no rule-citation → not counted as lever evidence.
Captain chose validated-but-NOT-promoted: a single within-noise cell doesn't warrant a seed-README edit;
rule + knowledge recorded for future composition. KEY KNOWLEDGE: output SERIALIZATION-format is
README-steerable at gpt-5.5 (deliberated choice), whereas the DECORATION reflex is NOT (dab0012 dead-family)
— reflex-vs-deliberated distinction now empirically grounded. INFRA: full-1 PG-volume concurrency collision
(fixed, PR #18) + full-2 Mongo serverSelectionTimeout; a fully-clean 54-cell board stayed elusive (different
backend dropped each run). Detail: dab0015 entity ## Conclusion (commit 9ca5a8c).

## Workflow refit (2026-06-21) — autonomous run policy (auto-gate to full-run launch)
Added `## Autonomous run policy` to the DAB workflow README + inline auto-gate notes on propose/smoke.
Encodes the guarded auto-pipeline distilled from dab0015: automate the mechanical spine + the clean
happy path through propose → smoke → the full-run LAUNCH; HALT+escalate on judgment. Default stays
captain-gated; autonomous mode is opt-in per hypothesis (drive the FO under /loop). Key guardrails:
propose auto-APPROVE = gatekeeper APPROVE + FO reject-checks; smoke→full auto-advance = strict-audit-clean
+ 0 coverage_missing + target-flipped-by-committed-artifact + canaries-held + backend-health + LOW-BASELINE
target (the yelp-q6 4/6-trap: a single pass on a multi-pass cell is not lever evidence). Never auto:
conclude/promote/seed-README-edit, strategy (lever choice/retarget/pivot/revise-vs-reject), infra code
fixes, or an UNEXPECTED result (→ unexpected-result-playbook). Infra is NEVER counted as a result.

## dab0017 (REJECTED, 2026-06-22) — mandatory dbt-pipeline falsified, dbt-advantage unproven
Force every dataset through built+validated stg→int→mart, answer=query the mart. Stratified 0.565 untuned
/ 0.6027 tuned, both < Opus 0.654 < anchor @codex-batch-baseline 0.697; 10 canary regressions (untuned).
dbt-ADVANTAGE UNPROVEN here: crmarenapro flips (q2/q3/q8) had NO mechanism delta vs the no-dbt anchor —
variant's norm_id #-strip == anchor's lstrip('#'); the README's resolved_entity_id OR-cluster never fired;
flips came WITH a q13 regression. 2 biggest losses (yelp 7→0, GITHUB q4) were FIXABLE WRAPPER bugs (FO
re-summarization dropped the dab-mongo host; JSON-list serialization false-RED), not dbt cost. Calibration
lesson: a generative fires-everywhere lever's SMOKE is NOT predictive of the full board (~±0.07/draw,
reconfirms dab0016). Mandatory-dbt DEAD for DAB. INFRA KEPT: dbt+scanners baked into dab-agent image,
host-fix fork, verify_batch=PR#19, @codex-batch-baseline registered (0.697>Opus). Detail: dab0017 ## Verdict.

## dab0018 (REJECTED, 2026-06-22) — classifier-gated dbt; gate works, dbt int_ real but narrow+self-taxing → dbt family CLOSED
The dab0017 follow-up: one forked README with a source-count classifier (N_sources≥3 from db_config.yaml
→ Method B dbt; else Method A = verbatim @codex-batch-baseline direct). GATE MECHANISM WORKS (zero leak,
full-board): classifier routed all 12 datasets correctly, "zero regression by construction" holds — reusable
gated-composition pattern for DAB. dbt int_ cross-source derivation is REAL+STABLE on crmarenapro and reaches
the COMMITTED int_ answer not a #-strip (cures the dab0017 no-mechanism-delta trap): q3 effective_stage=
Negotiation (opp↔transcript join), q7 breach ka0Wt000000EoD3IAK (case↔order↔KB), q2 cracked a 0/6 cell. BUT
REJECTED: full3 stratified 0.6927 < anchor 0.6966 AND one real canary regression (q9, a 6/6 ROCK-STABLE band
cell, destabilized by the dbt mart re-grain = within-dataset dbt tax). Only 5 cells moved board-wide (GAINS
crmarenapro q2/q3/q7; REG q9; stockmarket-q3 = direct-path noise, 0/6 cell reverting to mean). The +2
crmarenapro signal ≈+0.013 stratified is SWAMPED by direct-path single-draw noise. Anchor is the SAME
codex/gpt-5.5 → lever genuinely isolated (gain attributable, just tiny+self-taxed). dbt family CLOSED for DAB
with full-board evidence; no per-query-method-selection follow-up (needs oracle-free derivation-vs-ranking
signal the README can't supply; solver self-false-greens ranking cells). Detail: dab0018 ## Verdict; memory
dab-gated-dbt-self-cancelling.
- dab0022 (semi-structured-data rules: parser-first/complete-list/flat-record/level-binding/graph-traversal) PASSED-validated, NOT promoted: FIRST genuinely lever-attributable multi-cell DAB result + first leaderboard submission. 2 DURABLE confound-free flips proven across draws (codex-vs-codex, high-vs-high): PATENTS-q1 (complete-list+flat-record, 4/5) and googlelocal-q2 (flat-string serialization, 4/5 — RECONFIRMS dab0015). NOT promoted: durable ~+0.04 is variance-swamped — 5-draw mean 0.7433 but MEDIAN draw 0.7058 (+0.009 over codex anchor 0.6966), spread 0.6675-0.7985 wider than the lift, inside the ±0.07 band; the confirm caught that the single full draw over-credited PATENTS-q2 (1/3, variable-band) as stable. Seed README + @baseline/@codex-batch-baseline UNCHANGED. KEY LESSON: a single full draw is NOT promotable even with airtight committed-artifact attribution — a confound-free, executed, reached-the-answer cell (PATENTS-q2) can still be variable-band; only a ≥3-draw hold-rate separates a durable flip from a lucky draw. Lever FAMILY validated-actionable at gpt-5.5/high (refutes dab0012/dab0017 "abstract prose goes inert"). Banked: 270/270 leaderboard submission (dab/leaderboard_submissions/) scored 0.7433 via DAB's own validators (>Opus 0.6536, >codex anchor 0.6966). Harness gotcha: per-cell answers.json is NOT persisted out of the container, so verbatim recovery depends on the transcript echoing the full object (PATENTS runtime-script cells often echo only truncated prefixes -> 2 cells needed a fresh-draw re-run). -> filed dab0023 (compose the 2 durable + dab0015 levers as pre-verified banked levers, h0049 gated-compose, scoped off ranking cells). Detail: dab0022 ## Verdict; memory dab-semistructured-rules-first-real-go.
- dab0023 (compose flat-string serialization + complete-list/flat-record as 2 pre-verified banked levers) REJECTED: composition FALSIFIED — did NOT bank both durable cells without regression. The distinctive new arm (complete-list KEY-COLUMN pinning) is README-INERT by 2-draw committed-artifact byte-comparison: the cycle-2 lead-field fix ("use NAME/TITLE, never a description blurb") left stockmarket-q3's answer byte-identical to cycle-1 (still blurb-led, failed both draws) — README changed, behavior didn't ("talks but doesn't do" at gpt-5.5/high). The format half (flat-string) IS steerable+durable (PATENTS-q1 banked both draws; reconfirms dab0015/dab0022 a 3rd time) but that's a reconfirmation already banked in dab0022, not a new win. KEY NEW KNOWLEDGE: a sharper boundary on the dab0012 README-output-shape dead family — README can steer answer FORMAT (flat-string) but NOT which COLUMN the solver picks as the record key (complete-list key-column choice is README-inert/draw-dependent). The same name-lead fix that *appeared* to work in dab0022 cycle-3 was a favorable single draw — dab0023's 2-draw byte-comparison shows it weakly/un-steerable. Non-banks googlelocal-q2 (row-selection) + PATENTS-q3 (CPC-subclass) = oracle-blind content variance, format fired. @codex-batch-baseline + seed README UNCHANGED; no follow-up (arm dead, flat-string already banked); dab0022 5-draw 0.7433 submission stands. Detail: dab0023 ## Verdict; memory dab-readme-cannot-suppress-output-shape (key-column boundary).
