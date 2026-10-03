# Adoption guide

Adopt the contract without a disruptive rewrite.

1. Add `bripe-standards.toml` from the template and run the validator locally.
   Start with only checks your repository already satisfies.
2. Add the reusable workflow in advisory mode. It reports drift but does not
   block pull requests.
3. Correct the reported gaps and remove advisory mode to enforce the selected
   checks.
4. Enable stronger, selective practices only when useful. For Python projects,
   add the `python` profile; add Tach (and, for same-layer couplings, Import Linter) only after imports span meaningful layers. Treat Vulture as an advisory report.

For an existing repository, preserve its working architecture. First map its
public interfaces and critical invariants in existing docs, then make the
manifest truthful. Introduce tests and linting around changed areas rather than
requiring a wholesale reorganization. The contract is a maintenance aid, not a
migration mandate.

## Run from a local standards checkout

The standards repository is a development/CI tool, never a runtime dependency.
If a project and this repository are both available locally, run the validator
from the standards checkout while targeting the project:

```bash
cd /path/to/project-a
uv run --directory /path/to/bripe-standards bripe-standards check .
```

The target can be a Python project, an npm project, another language, or a
documentation-only repository. Its `bripe-standards.toml` does not include the
machine path to the standards checkout.

### npm project

An npm project can expose the same local command through its own familiar
script, without adding an npm dependency or changing its lockfile:

```json
{
  "scripts": {
    "standards": "uv run --directory ../bripe-standards bripe-standards check ."
  }
}
```

Run `npm run standards`. Adjust the relative path for the local checkout. This
requires `uv` on the developer or CI machine because the validator is Python;
it does not make the checked project a Python project. If that host requirement
becomes a burden, a future standalone binary is a distribution improvement—not
a reason to put package-manager configuration in the manifest.

### No-runtime repository

Run the same command directly from a shell or task runner. Use an empty profile
list and the `manifest` check, then add only checks that make sense for the
repository's content.

## Calling reusable CI

Copy [the caller template](../templates/standards.yml) to
`.github/workflows/standards.yml`. The caller grants only `contents: read` and
can set `advisory: true` while rolling out. The reusable workflow runs the local
validator; `python-checks` additionally runs Ruff and pytest in the caller.
Set `validator-source` to the tagged standards repository, such as
`YOUR_GITHUB_OWNER/bripe-standards@v1`, so the reusable workflow always runs an
intentional validator version.

For a CI system that has a local mirror or needs an explicit checkout instead,
check out this repository at a tag beside the target repository and run:

```yaml
- uses: actions/checkout@v4
  with:
    repository: YOUR_GITHUB_OWNER/bripe-standards
    ref: v1
    path: .tools/bripe-standards
- uses: astral-sh/setup-uv@v5
- run: uv run --directory .tools/bripe-standards bripe-standards check .
```

For a private checkout or mirror, configure that checkout according to the
hosting system's normal read-only access rules. The validator does not need
write permission to the target repository.
