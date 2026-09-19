# Bripe standards contract

Contract version: **1.0.0**. This document is the versioned agreement adopted
by repositories that declare it in `bripe-standards.toml`. The validator and
this contract use semantic versioning: incompatible contract changes require a
new major version.

## Universal requirements

Every adopting repository, regardless of language or profile, must:

- make ownership boundaries explicit: identify the responsible maintainer or
  team and keep project-local decisions discoverable;
- distinguish supported public APIs, commands, and data formats from internal
  implementation details, and avoid accidental public surface area;
- keep dependencies pointed toward stable, lower-level abstractions; do not
  make shared utilities depend on application or domain layers;
- run focused, repeatable verification appropriate to its changes before
  merging, and retain an automated baseline where practical;
- document non-obvious invariants, operational constraints, and decisions that
  a future maintainer could otherwise violate; and
- handle state, secrets, and personally identifiable information safely:
  never commit credentials or private data, minimize collection and retention,
  and make storage/cleanup expectations explicit.

These are outcome requirements, not a mandated architecture. Repositories may
use any language, framework, database, deployment model, or test runner.

## Opt-in profiles

Profiles add narrowly scoped expectations. A project enables only the profiles
that help it. Version 1 provides `python`, which expects `pyproject.toml`, an
isolated `tests/` directory, and Ruff configuration when its corresponding
checks are enabled. It recommends typed public boundaries and reserves Tach for
projects whose import graph is substantial enough to benefit from enforcement.

The manifest's `checks` field controls which deterministic checks run locally.
Checks are intentionally not a package manager or CI description.

## Boundaries and non-goals

This repository is not a runtime kernel, plugin runtime, universal architecture
framework, secret manager, or replacement for project-local architecture docs.
It contains no business or domain logic.

Graduate shared runtime code into a separate package only when at least two real
consumers need the same stable behavior and can share a small, well-tested,
versioned contract. Keep that package independent from these standards.
