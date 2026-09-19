# Python profile

Enable `python` when a repository ships or maintains Python code. The profile
recommends modern packaging through `pyproject.toml`, isolated tests in `tests/`,
Ruff for fast baseline linting, and explicit typed boundaries for public modules.
Keep implementation modules private by convention and document the supported
imports, commands, and data contracts.

The validator's `profile-files` check requires `pyproject.toml`; `python-layout`
requires `tests/` and a `[tool.ruff]` table. It deliberately does not prescribe a
test framework, dependency manager, source layout, web framework, or type checker.

## Tach

Use [the starter](../templates/tach.toml) only when a project has several import
layers, multiple packages, or repeated boundary regressions that need mechanical
enforcement. Replace its illustrative module names with the repository's own
namespace and encode only real dependency rules.

Omit Tach for small scripts, a single cohesive package, or codebases whose import
relationships are obvious and inexpensive to review. A configuration with no
meaningful boundaries is ceremony, not protection. Add it later when the import
graph earns it; the standards validator does not require it.
