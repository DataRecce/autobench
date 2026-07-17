import json, sys, importlib.util
from pathlib import Path

DATA = Path('/home/kent/dataagentbench/data')
sys.path.insert(0, str(DATA))  # makes `common_scaffold` importable (namespace pkg)

# recovered answer values live in ./regrade_data beside this script (committed)
SCR = Path(__file__).resolve().parent / 'regrade_data'

# dataset dir name -> query_<dir>
DSDIR = {
    'GITHUB_REPOS':'query_GITHUB_REPOS',
    'music_brainz_20k':'query_music_brainz_20k',
    'PANCANCER_ATLAS':'query_PANCANCER_ATLAS',
    'PATENTS':'query_PATENTS',
}

# crashed cells: (trial_dir, dataset, [q-numbers])
CELLS = [
    ('GITHUB_REPOS__naR27Bq','GITHUB_REPOS',[1,3,4]),
    ('music_brainz_20k__GWkSAqQ','music_brainz_20k',[1]),
    ('music_brainz_20k__qpXdM35','music_brainz_20k',[1]),
    ('PANCANCER_ATLAS__RQG9mgJ','PANCANCER_ATLAS',[1,2,3]),
    ('PANCANCER_ATLAS__twXnPRq','PANCANCER_ATLAS',[1,2,3]),
    ('PATENTS__gyJU8bk','PATENTS',[1]),
    ('PATENTS__vxdxuQ6','PATENTS',[1,2,3]),
]

def load_validate(dataset, q):
    vp = DATA / DSDIR[dataset] / f'query{q}' / 'validate.py'
    spec = importlib.util.spec_from_file_location(f'val_{dataset}_{q}', str(vp))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m.validate

def load_answers(trial):
    p = SCR / f'answers_{trial}.json'
    txt = ''.join(l for l in open(p) if not l.startswith('#'))
    return json.loads(txt)

def regrade_value(dataset, q, raw):
    validate = load_validate(dataset, q)
    # confirm raw crashes (mirror batch path: validate_fn(raw) with no coercion)
    crash = None
    try:
        validate(raw)
    except Exception as e:
        crash = f'{type(e).__name__}: {e}'
    # corrected: str-coerce like verify.py line 33
    coerced = str(raw)
    try:
        ok, reason = validate(coerced)
    except Exception as e:
        ok, reason = False, f'STILL-CRASHES {type(e).__name__}: {e}'
    return crash, (1.0 if ok else 0.0), reason

def main():
    override = {}
    if len(sys.argv) > 1:  # optional override file for gyJU8bk full list
        override = json.load(open(sys.argv[1]))
    rows = []
    for trial, dataset, qs in CELLS:
        try:
            ans = load_answers(trial)
        except Exception as e:
            for q in qs:
                rows.append((trial,dataset,q,'NO_ANSWERS',0.0,str(e)))
            continue
        for q in qs:
            key = f'q{q}'
            if (trial,key) in override:
                raw = override[(trial,key)]
            elif trial in override and key in override.get(trial,{}):
                raw = override[trial][key]
            else:
                raw = ans[key]
            crash, reward, reason = regrade_value(dataset, q, raw)
            rows.append((trial,dataset,q,crash,reward,reason[:80]))
    print(f'{"trial":28} {"q":3} {"crash?":6} {"corr":4} reason')
    npass=0
    for trial,dataset,q,crash,reward,reason in rows:
        c = 'YES' if crash else 'no'
        if reward==1.0: npass+=1
        print(f'{trial:28} q{q}  {c:6} {reward:.0f}    {reason}')
    print(f'\nCrashed cells re-graded: {len(rows)}; flipped to PASS: {npass}; stay 0: {len(rows)-npass}')
    # dump machine-readable
    json.dump([{'trial':t,'dataset':d,'q':q,'crashed':bool(cr),'crash':cr,'corrected_reward':rw,'reason':rs}
               for t,d,q,cr,rw,rs in rows], open(SCR/'regrade_results.json','w'), indent=2)

if __name__=='__main__':
    main()
