# bripe-standards

Versioned, lightweight engineering standards and local conformance tooling for Bripe projects.
It is an adoption contract, not an application framework or shared runtime.

```bash
uv run bripe-standards check /path/to/project
```

Start with the [standards contract](docs/standards-contract.md), then follow the
[manifest reference](docs/manifest.md), [Python profile](docs/python-profile.md),
and [adoption guide](docs/adoption.md). Copyable starting points live in
[templates](templates/).

## Development

Requires Python 3.11+ and [uv](https://docs.astral.sh/uv/).

```bash
uv sync --dev
uv run ruff check .
uv run pytest
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for change and release guidance.
