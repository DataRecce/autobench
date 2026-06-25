# Codex SWE-bench-Pro Solver Workflow

Work in the task workspace as delivered by the benchmark harness. The benchmark
instruction is appended below these workflow instructions. This is a
**code-repair** task: a real software repository is checked out at a specific
base commit, the instruction describes a bug or a required behavior change (an
issue), and you fix it by EDITING THE REPOSITORY SOURCE. The graded artifact is
the **repository working tree** — a hidden test suite is run against it. There is
no answer file to write.

## THE GRADING CONTRACT (load-bearing — this is how the task is graded)

After you finish, the verifier applies a **hidden test patch** to the repo and
runs two named test sets:

- **FAIL_TO_PASS** — tests that fail on the unmodified base commit and MUST pass
  after your change. These encode the fix the instruction asks for.
- **PASS_TO_PASS** — tests that already pass on the base commit and MUST STILL
  pass after your change. These guard against regressions.

The reward is **all-or-nothing**: you score 1.0 only if every FAIL_TO_PASS test
flips to passing AND every PASS_TO_PASS test stays passing. A fix that solves the
issue but breaks unrelated behavior scores zero. This drives the whole strategy:

1. **Make the SMALLEST change that fixes the issue.** Touch only the code paths
   the issue concerns. Do not refactor, reformat, restyle, bump dependencies, or
   "clean up" surrounding code — every unrelated edit risks a PASS_TO_PASS
   regression for no FAIL_TO_PASS gain.
2. **Fix the ROOT CAUSE, generally.** The hidden FAIL_TO_PASS tests are NOT shown
   to you, so do not special-case the one scenario named in the issue. Fix the
   underlying defect so the corrected behavior holds for the whole class of
   inputs the issue describes — that is what an unseen test will probe.
3. **Preserve public behavior and signatures.** Keep existing function/class
   signatures, return types, error types, and side effects unless the issue
   explicitly requires changing them; PASS_TO_PASS depends on them.
4. **Edit source, not tests.** The verifier supplies its own tests. Do not edit,
   add, or delete the repo's existing test files to make things "pass" — your
   test edits are overwritten/ignored by the hidden test patch and only risk
   breaking the build. Write any throwaway reproduction OUTSIDE the repo's tracked
   test paths (or delete it before finishing).

## Leak-guard (off-limits inputs)

The gold patch, the hidden test patch, and the FAIL_TO_PASS / PASS_TO_PASS test
lists are deliberately WITHHELD from your workspace. Do not search for them,
reconstruct them, or try to discover which tests will be run. Solve from the
issue text and the repository alone.

Do not fetch external material while solving. This includes `curl`, `wget`,
`git clone`, `git ls-remote`, `git fetch`, browsing the upstream project or its
issue tracker / pull requests, package-index installs from the network
(`pip install`, `npm install`, `apt-get`, etc.), and any web search for the
published fix. The repository's dependencies are already installed in the task
image — use what is present. If something genuinely required for setup is
missing, prefer the repo's own offline tooling; do not reach to the network.

Treat the repository's git history as a working tool, not an oracle: you may
inspect the checked-out tree and run local commands, but do not mine remote
branches/tags or upstream commits for the answer.

## Stage: Exploration

Read the issue (instruction) carefully and restate, for yourself, the exact
defect and the expected correct behavior. Then locate it in the code:

- Orient in the repo: language, layout, build/test runner (`pytest`, `tox`,
  `make test`, `npm test`, `go test`, etc.), and how to run a single test file.
- Find the relevant module(s) by the symbols, error messages, or APIs the issue
  names — grep for them. Read the implicated functions and their callers.
- **Reproduce the bug first.** Write a minimal local reproduction (a scratch
  script outside the tracked test dirs, or an interactive run) that exhibits the
  wrong behavior at the base commit. A confirmed repro is your stand-in for the
  hidden FAIL_TO_PASS test — without it you are guessing.
- Run a cheap slice of the EXISTING test suite near the affected area to learn
  the baseline (what already passes) and the test conventions.

## Stage: Implementation

Make the minimal, root-cause fix in the repository source, following the local
code style and patterns. Keep the change tightly scoped to the issue. Prefer
fixing shared logic over duplicating a patch at each call site. Add a code
comment only where the fix is non-obvious and the surrounding code is commented;
do not narrate.

After editing, re-run your reproduction — it must now show the corrected
behavior. Then run the existing tests covering the files you touched to catch
obvious regressions early.

## Stage: Validation

Beyond "my repro passes":

- Re-run the repository's existing test suite as broadly as time/budget allow,
  at least every module you changed and its neighbors. Investigate any test that
  your change turned red — a regression here is a PASS_TO_PASS failure and zeroes
  the score.
- Re-read the issue and confirm the fix addresses the GENERAL behavior, not just
  the single example — think about edge cases an unseen test might check
  (empty/None inputs, boundaries, error paths, the negative case).
- Confirm you changed only source files, left the repo's test files as the
  harness expects, and introduced no stray tracked files.

## Stage: Finalization

Leave the working tree as a clean, minimal fix: only the source edits that
deliver the change. Remove any scratch reproduction scripts and generated
artifacts you created. Do not revert or stash legitimate fix edits. Finish with a
short summary — the files changed, the root cause, and the validation you ran
(your repro result + which existing tests you re-ran and that they passed).
