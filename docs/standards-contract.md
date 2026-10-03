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

## Recommended practices

These are optional and not checked by the validator. Adopt them when a
repository's size makes them pay off.

- **Ratchets.** Make reviewed exceptions (dependency allowlists, scanner
  allowlists) shrink-only: widening one requires a recorded baseline change and
  an explicit trailer or note in the same commit.
- **Artifact lifecycle.** Give plans, orchestration directories, and decision
  notes a status, and treat "implemented" as transient: delete the artifact once
  its durable content lives in docs or issues.
- **Freshness.** Record perishable facts (version pins, tool behavior) with a
  checked date and a recheck-by date, and cite them from the comment beside the
  pin.
- **Release pipeline.** Use per-change changelog fragments and one atomic,
  verified version bump that also rewrites lockfiles that record the project's own
  version. Small repositories may use curated release notes instead.
- **Local-first CI.** Run the full suite locally and let hosted CI confirm a
  clean merge, gating paid runner time on a passing local receipt for the exact
  commit when minutes are scarce.
- **Small boundary scanners.** Prefer a short scanner with an `--all` mode and a
  reviewed allowlist over prose for a rule that has regressed more than once.
