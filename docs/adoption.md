# Adoption guide

Adopt the contract without a disruptive rewrite.

1. Add `bripe-standards.toml` from the template and run `uvx bripe-standards
   check .` (or install this repository as a tool). Start with only checks your
   repository already satisfies.
2. Add the reusable workflow in advisory mode. It reports drift but does not
   block pull requests.
3. Correct the reported gaps and remove advisory mode to enforce the selected
   checks.
4. Enable stronger, selective practices only when useful. For Python projects,
   add the `python` profile; add Tach only after imports span meaningful layers.

For an existing repository, preserve its working architecture. First map its
public interfaces and critical invariants in existing docs, then make the
manifest truthful. Introduce tests and linting around changed areas rather than
requiring a wholesale reorganization. The contract is a maintenance aid, not a
migration mandate.

## Calling reusable CI

Copy [the caller template](../templates/standards.yml) to
`.github/workflows/standards.yml`. The caller grants only `contents: read` and
can set `advisory: true` while rolling out. The reusable workflow runs the local
validator; `python-checks` additionally runs Ruff and pytest in the caller.
Set `validator-source` to the tagged standards repository, such as
`YOUR_GITHUB_OWNER/bripe-standards@v1`, so the reusable workflow always runs an
intentional validator version.
