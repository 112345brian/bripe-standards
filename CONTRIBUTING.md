# Contributing and releases

Keep changes small, deterministic, and free of consumer-specific policy.
Update the contract version only for contract changes, and update the validator
version for released CLI behavior. Both use semantic versioning.

Before opening a change, run:

```bash
uv sync --dev
uv run ruff check .
uv run pytest
uv run bripe-standards check .
```

For this small v1 repository, Towncrier fragments are intentionally not used:
the release surface is one contract and one small CLI, so a concise curated
release note and a Git tag are less overhead. Revisit fragments if contributor
volume or release frequency makes aggregation valuable.
