# E0 / h0032 — instrument-validation harness

Proves each candidate INDEPENDENT downstream check is **two-sided discriminating** on a controlled
fixture: it FIRES on a known injected error and stays SILENT on a known-good. See the hypothesis body
`../../h0032-instrument-validation-gate.md` (`## Gatekeeper review`, `## Smoke result`) for verdicts.

## Reproduce

```sh
# 1. fetch the fixture DuckDBs (downloadable release artifacts; not committed)
mkdir -p dbs
gh release download databases --repo dbt-labs/ade-bench \
  --pattern "f1.duckdb" --dir dbs --clobber
# 2. run
python3 harness.py            # prints the 2x2 + adversarial probes; writes result_2x2.json
```

Requires `duckdb` Python (>=1.x). No dbt run needed: the f1 DuckDB ships the raw source tables AND the
canonical currently-PASSING @baseline model outputs in the same file, so the canonical table is the
known-good and the raw tables are the independent second path.

## Files

- `harness.py` — the harness (4 checks + 2 adversarial probes).
- `result_2x2.json` — machine-readable result (`checks[]` + `adversarial{}`); cite `E0-cleared` from it.
- `dbs/` — fixture DuckDBs (gitignored).
