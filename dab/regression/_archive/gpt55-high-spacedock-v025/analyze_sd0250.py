#!/usr/bin/env python3
"""One-off analysis for regr-sd0250-gpt55-high (5 attempts in one harbor job).

Reuses extract_benchmark_data.py's harbor token/duration/timeout functions
(unmodified import), and computes the per-draw stratified split the extractor
cannot do for a multi-attempt job.
"""
import json, sys, statistics as st
from collections import defaultdict

sys.path.insert(0, "/home/kent/autobench/dab/docs/benchmark-artifact")
import extract_benchmark_data as ex

CFG = "/home/kent/.local/share/razorback/runs/regr-sd0250-gpt55-high"
JOB = CFG + "/3a67e091dc4b2d5f"

trials = json.load(open(JOB + "/per_trial_outcomes.json"))["trials"]

# ---- per-draw stratified pass@1 (draw = trial_index = harbor attempt) ----
draws = defaultdict(dict)
name_by = {}
for t in trials:
    draws[t["trial_index"]][t["dataset"]] = t["reward"]
    name_by[(t["trial_index"], t["dataset"])] = t["trial_name"]
assert len(draws) == 5 and all(len(v) == 12 for v in draws.values())

strat = {k: st.mean(v.values()) for k, v in sorted(draws.items())}
vals = list(strat.values())
print("== per-draw stratified pass@1 ==")
for k, v in strat.items():
    print(f"draw {k}: {v:.4f}")
print(f"mean={st.mean(vals):.4f} sd={st.stdev(vals):.4f} "
      f"min={min(vals):.4f} max={max(vals):.4f}")

# ---- validator-crash census + substitution sensitivity ----
# crashed query -> substitute mean of same query's reward in non-crashed draws
crash = defaultdict(list)   # (dataset, q) -> [draw,...]
qrew = defaultdict(dict)    # (dataset, q) -> {draw: reward}
for t in trials:
    rpq = json.load(open(f"{JOB}/{t['trial_name']}/steps/main/verifier/reward_per_query.json"))
    for q, v in rpq.items():
        qrew[(t["dataset"], q)][t["trial_index"]] = v["reward"]
        if "validator error" in v.get("reason", "").lower():
            crash[(t["dataset"], q)].append(t["trial_index"])

print("\n== validator crashes (dataset,q -> draws) ==")
ncrash_q = 0
for (ds, q), ds_draws in sorted(crash.items()):
    clean = [qrew[(ds, q)][d] for d in range(5) if d not in ds_draws]
    ncrash_q += len(ds_draws)
    print(f"{ds} {q}: draws {sorted(ds_draws)} | clean-draw rewards {clean}")
print(f"total crashed query-cells: {ncrash_q} / {sum(len(v) for v in qrew.values())}")

# substituted per-draw stratified
sub_strat = {}
for d in range(5):
    ds_scores = []
    for ds in draws[d]:
        qs = [q for (dds, q) in qrew if dds == ds]
        rs = []
        for q in sorted(qs):
            if d in crash.get((ds, q), []):
                clean = [qrew[(ds, q)][dd] for dd in range(5)
                         if dd not in crash.get((ds, q), [])]
                rs.append(st.mean(clean) if clean else 0.0)
            else:
                rs.append(qrew[(ds, q)][d])
        ds_scores.append(st.mean(rs))
    sub_strat[d] = st.mean(ds_scores)
sv = list(sub_strat.values())
print("\n== crash-substituted sensitivity (clean-draw-mean substitution) ==")
for k, v in sub_strat.items():
    print(f"draw {k}: {v:.4f}  (raw {strat[k]:.4f})")
print(f"substituted mean={st.mean(sv):.4f} sd={st.stdev(sv):.4f}")

# ---- tokens / durations / timeouts via extractor harbor paths ----
print("\n== tokens (harbor sessions/ rollouts) ==")
print(ex.tokens_harbor(CFG))
durs = ex.durations_harbor(CFG)
print(f"\n== durations ==\nn={len(durs)} meanSec={round(st.mean(durs))} "
      f"p50={round(ex._quantile(durs,0.5))} max={max(durs)}")
print("\n== timeouts/failed sessions ==")
print(ex.timeouts_harbor(CFG) or "none")
