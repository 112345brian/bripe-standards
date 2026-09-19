# `bripe-standards.toml`

The manifest is deliberately small and language-neutral:

```toml
[standards]
version = "1.0.0"
profiles = ["python"]
project_type = "application"
checks = ["manifest", "profile-files", "python-layout"]
```

`version` selects the contract major version. `profiles` is an array of opt-in
profiles (v1 supports `python`). `project_type` is one of `application`,
`library`, `utility`, `documentation`, or `infrastructure`. `checks` chooses
the validator checks: `manifest`, `profile-files`, and `python-layout`.
`manifest` is always required in the list. The file does not declare dependencies,
commands, secrets, environments, or CI jobs.

## Python application

```toml
[standards]
version = "1.0.0"
profiles = ["python"]
project_type = "application"
checks = ["manifest", "profile-files", "python-layout"]
```

## Tiny script or utility

```toml
[standards]
version = "1.0.0"
profiles = ["python"]
project_type = "utility"
checks = ["manifest", "profile-files", "python-layout"]
```

For a genuinely trivial one-file script, retain the manifest and `pyproject.toml`
but document why a full layer policy is unnecessary. `tests/` may contain only a
small smoke test.

## Repository with no runtime code

```toml
[standards]
version = "1.0.0"
profiles = []
project_type = "documentation"
checks = ["manifest"]
```
