# bripe-standards

Versioned, lightweight engineering standards and local conformance tooling for Bripe projects.
It is an adoption contract, not an application framework or shared runtime.

From a local checkout of this repository, validate any project without adding a
runtime dependency to it:

```bash
uv run --directory /path/to/bripe-standards bripe-standards check /path/to/project
```

The target project may use Python, npm, another toolchain, or contain no runtime
code. Its manifest selects the contract, while the command source is a local or
CI choice.

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
