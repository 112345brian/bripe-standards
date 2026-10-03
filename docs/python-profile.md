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

[Import Linter](https://github.com/seddonym/import-linter) complements Tach
rather than duplicating it. Tach's layer rule only forbids importing *up* the
stack, so two modules on the same layer may couple freely without a warning.
Import Linter's `forbidden` contracts name one direction between two sets of
modules that must not exist, regardless of layer. Add a contract only for a
coupling that has actually recurred, and keep each one narrow. Use Import Linter
alone when a repository needs only a handful of rules; use both once layers
exist. Run whichever tools you adopt in CI and in a pre-commit hook so the rules
cannot drift.

Omit Tach for small scripts, a single cohesive package, or codebases whose import
relationships are obvious and inexpensive to review. A configuration with no
meaningful boundaries is ceremony, not protection. Add it later when the import
graph earns it; the standards validator does not require it.

## Vulture

Vulture finds unused functions, classes, and variables. It is cheap to run and
useful as a periodic cleanup aid, but Python's dynamic features (`getattr`,
decorators, framework registration, plugin entry points) cause false positives.
Treat it as advisory, not a gate: run it with `--min-confidence 80` or higher,
keep a reviewed whitelist module for intentional dynamic use, and configure it
under `[tool.vulture]` in `pyproject.toml`. Make it a blocking CI check only in
a repository that has already cleared its backlog and whose whitelist is small.
Ruff's `F401`/`F841` rules already cover unused imports and locals, so Vulture
adds value mainly for unused module-level and public-looking code.

For a useful starting point, configure it like this:

```toml
[tool.vulture]
paths = ["src"]          # production code only, so test-only use still shows
min_confidence = 60
ignore_decorators = ["@*.command", "@*.route", "@pytest.fixture"]
```

A second pass that adds `tests/` separates code that is dead in production but
kept alive by tests from code referenced nowhere. Record reviewed, deliberate
exceptions with a reason, and report an exception as stale once it no longer
matches a finding so the list cannot rot.

## Declared dependencies

Use [deptry](https://github.com/fpgmaas/deptry) (or Tach's `check-external`) to
confirm every imported third-party package is declared and every declared one is
used. Declare a package directly when code imports it, even if another
dependency already pulls it in. Comment any upper bound with the reason and a
recheck date.

## Package and import conventions

These rules are tool-independent and cheap to follow:

- Keep `__init__.py` empty or minimal, with no import-time side effects such as
  network calls, filesystem scans, or starting processes.
- Import from the module that defines a name. Re-export only to publish a
  deliberate public API, never to shorten an import.
- Give each concept one home: a package or a flat module, never both. When you
  move a module, rewrite every importer and delete the old path; leave no shim.
- Point imports down the layer stack. If a lower layer needs something from a
  higher one, move the shared piece down or pass it in.
- Do not close a cycle with a lazy in-function import. Extract a port (a
  `typing.Protocol` in the lower layer, with the concrete adapter registered
  from above) and back it with a test or contract that fails if the edge returns.
- Return explicit result objects (changed, no-op, skipped, failed) where a caller
  must tell outcomes apart, and add a test that fails when a caller discards one.
- Keep CLI registration and orchestration at the top of the graph; a command
  need not correspond one-to-one with a module.
