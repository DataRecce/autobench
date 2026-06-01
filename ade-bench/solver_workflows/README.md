# Solver workflows

Each subdirectory is one solver-workflow README the spacedock-solver agent loads at
trial start. `codex-ade-dbt-minimal/` is the baseline solver (the current `@baseline`'s
solver); hypothesis variants are forks of it. The authoritative authoring flow lives in
`../hypotheses/README.md` (the `propose` stage).

```bash
$ cp -r solver_workflows/codex-ade-dbt-minimal solver_workflows/h0001-<slug>
$ ${EDITOR:-vi} solver_workflows/h0001-<slug>/README.md       # the one variable
$ cp specs/baseline.yaml specs/h0001-<slug>.yaml              # set experiment: + solver_workflow:
$ rk freeze --allow-missing specs/h0001-<slug>.yaml
```

Keep each solver README's **no-external-reference / leak-guard prose** intact (no public
fetches — `curl`/`wget`/`git clone`, HuggingFace lookups, web search). `rk audit
--policy strict` and the matrix driver's `captured > 0` gate are the backstops.
