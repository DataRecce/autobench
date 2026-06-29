# Publishing This Workflow Template

Publish this directory at a stable public URL so users can reference it when
commissioning a new Spacedock workflow.

## Recommended Public URL

Use a raw URL for the workflow README:

```text
https://raw.githubusercontent.com/<org>/<repo>/<branch>/docs/workflow-gallery/general-science-experiment-research/README.md
```

If the workflow gallery has a documentation site, also publish a human-readable
page, but keep the raw README URL available. The raw URL is easiest for agents to
fetch and adapt.

## What to Publish

Minimum:

- `README.md` - the Spacedock workflow template.
- `_gatekeeper/propose-review-guideline.md` - reusable proposal-review checklist.
- `_artifacts/self-learning.md` - learning-log starter.
- `_artifacts/WORKFLOW-REFINE.md` - workflow-refinement log starter.
- `EXECUTOR.md` - how projects plug in pilot/full execution commands.
- `EXAMPLE-USE-CASE.md` - narrative example showing how a researcher adapts the template.

For raw-URL commissioning, publish companion raw URLs for every file:

```text
README: <PUBLIC_RAW_README_URL>
EXECUTOR: <PUBLIC_RAW_EXECUTOR_URL>
GATEKEEPER: <PUBLIC_RAW_GATEKEEPER_URL>
SELF_LEARNING: <PUBLIC_RAW_SELF_LEARNING_URL>
WORKFLOW_REFINE: <PUBLIC_RAW_WORKFLOW_REFINE_URL>
EXAMPLE_USE_CASE: <PUBLIC_RAW_EXAMPLE_USE_CASE_URL>
```

## User Prompt

Users can paste a prompt like this when invoking Spacedock commission:

```text
Commission a new Spacedock workflow for my academic research project using this
general science experiment workflow as the template:

README: <PUBLIC_RAW_README_URL>
EXECUTOR: <PUBLIC_RAW_EXECUTOR_URL>
GATEKEEPER: <PUBLIC_RAW_GATEKEEPER_URL>
SELF_LEARNING: <PUBLIC_RAW_SELF_LEARNING_URL>
WORKFLOW_REFINE: <PUBLIC_RAW_WORKFLOW_REFINE_URL>
EXAMPLE_USE_CASE: <PUBLIC_RAW_EXAMPLE_USE_CASE_URL>

Adapt it to my project. Keep the concept -> ideate -> hypothesis -> propose ->
pilot -> full -> analyze -> conclude shape, the one-independent-variable rule,
proposal review, pilot gate, artifact-level attribution, and durable learning
logs. Also generate a project-specific pilot/full executor contract based on the
published EXECUTOR file. My research area is: <brief description>. Put the
generated workflow in: docs/research.
```

For a more specific request:

```text
Commission a workflow from these public template files for academic research on
<topic>:

README: <PUBLIC_RAW_README_URL>
EXECUTOR: <PUBLIC_RAW_EXECUTOR_URL>
GATEKEEPER: <PUBLIC_RAW_GATEKEEPER_URL>
SELF_LEARNING: <PUBLIC_RAW_SELF_LEARNING_URL>
WORKFLOW_REFINE: <PUBLIC_RAW_WORKFLOW_REFINE_URL>
EXAMPLE_USE_CASE: <PUBLIC_RAW_EXAMPLE_USE_CASE_URL>

Each entity should be a research hypothesis. I want captain approval at the
protocol-review and pilot-result gates. Include the gatekeeper checklist,
executor contract, and artifact logs from the template. Generate it under
docs/research.
```

## Maintainer Notes

- Keep the published README free of repo-local paths, private benchmark names,
  or machine-specific commands.
- Prefer stable branch or versioned tag URLs over moving local paths.
- If the template changes incompatibly, publish a new versioned URL instead of
  silently changing old behavior.
- The URL should point to trusted content. Users should not commission workflows
  from arbitrary unknown templates without reviewing the README first.
