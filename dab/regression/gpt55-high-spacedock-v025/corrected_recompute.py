#!/usr/bin/env python3
"""Corrected stratified pass@1 for regr-sd0250: overlay the 15 str()-coerced
re-grades onto per-query rewards and recompute per-draw stratified mean."""
import json, statistics as st
from collections import defaultdict

import os
JOB = "/home/kent/.local/share/razorback/runs/regr-sd0250-gpt55-high/3a67e091dc4b2d5f"
SCR = os.path.dirname(os.path.abspath(__file__))  # regrade_results.json committed beside

trials = json.load(open(JOB + "/per_trial_outcomes.json"))["trials"]
regrade = json.load(open(SCR + "/regrade_results.json"))
# corrected reward map: (trial_name, qkey) -> reward
corr = {(r["trial"], f"q{r['q']}"): r["corrected_reward"] for r in regrade}

# gather per-query rewards per trial, RAW and CORRECTED
def trial_reward(trial_name, apply_corr):
    rpq = json.load(open(f"{JOB}/{trial_name}/steps/main/verifier/reward_per_query.json"))
    rs = []
    for q, v in rpq.items():
        r = v["reward"]
        if apply_corr and (trial_name, q) in corr:
            r = corr[(trial_name, q)]
        rs.append(r)
    return st.mean(rs) if rs else 0.0

# build per-draw per-dataset reward, raw and corrected
raw_draw = defaultdict(dict)
cor_draw = defaultdict(dict)
for t in trials:
    tn = t["trial_name"]; di = t["trial_index"]; ds = t["dataset"]
    raw_draw[di][ds] = trial_reward(tn, False)
    cor_draw[di][ds] = trial_reward(tn, True)

# sanity: raw recompute must match per_trial_outcomes reward
for t in trials:
    exp = t["reward"]; got = raw_draw[t["trial_index"]][t["dataset"]]
    assert abs(exp - got) < 1e-9, f"raw mismatch {t['trial_name']}: {exp} vs {got}"

def strat(draw_map):
    s = {k: st.mean(v.values()) for k, v in sorted(draw_map.items())}
    vals = list(s.values())
    return s, st.mean(vals), st.stdev(vals)

rs, rm, rsd = strat(raw_draw)
cs, cm, csd = strat(cor_draw)

print("draw |   raw    corrected   delta")
for d in range(5):
    print(f"  {d}  | {rs[d]:.4f}   {cs[d]:.4f}   {cs[d]-rs[d]:+.4f}")
print(f"\nRAW       mean={rm:.4f} sd={rsd:.4f}")
print(f"CORRECTED mean={cm:.4f} sd={csd:.4f}")
print(f"delta corrected - raw     = {cm-rm:+.4f}")
print(f"delta corrected - v0.22(0.7433) = {cm-0.7433:+.4f}")
print(f"delta raw       - v0.22(0.7433) = {rm-0.7433:+.4f}")
nflip = sum(1 for r in regrade if r["corrected_reward"] == 1.0)
print(f"\n15 crashed cells: {nflip} flipped to PASS, {15-nflip} stay 0")
