"""Deterministic, read-only checks for bripe-standards.toml."""

from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

CONTRACT_MAJOR = 1
KNOWN_PROFILES = {"python"}
KNOWN_CHECKS = {"manifest", "profile-files", "python-layout"}
PROJECT_TYPES = {"application", "library", "utility", "documentation", "infrastructure"}


@dataclass(frozen=True)
class Manifest:
    version: str
    profiles: list[str]
    project_type: str
    checks: list[str]


def validate(root: Path) -> list[str]:
    """Return actionable conformance errors without changing *root*."""
    manifest, errors = _load_manifest(root)
    if manifest is None:
        return errors
    if "profile-files" in manifest.checks:
        errors.extend(_check_profile_files(root, manifest))
    if "python-layout" in manifest.checks:
        errors.extend(_check_python_layout(root, manifest))
    return errors


def _load_manifest(root: Path) -> tuple[Manifest | None, list[str]]:
    path = root / "bripe-standards.toml"
    if not path.is_file():
        return None, [
            "bripe-standards.toml: missing manifest "
            "(copy templates/bripe-standards.toml)"
        ]
    try:
        with path.open("rb") as handle:
            raw: Any = tomllib.load(handle)
    except tomllib.TOMLDecodeError as error:
        return None, [f"bripe-standards.toml: invalid TOML: {error}"]
    standards = raw.get("standards") if isinstance(raw, dict) else None
    if not isinstance(standards, dict):
        return None, ["bripe-standards.toml: add a [standards] table"]

    errors: list[str] = []
    version = standards.get("version")
    profiles = standards.get("profiles")
    project_type = standards.get("project_type")
    checks = standards.get("checks")
    if not isinstance(version, str) or not version:
        errors.append(
            "bripe-standards.toml: standards.version must be a non-empty string"
        )
    elif _major(version) != CONTRACT_MAJOR:
        errors.append(
            f"bripe-standards.toml: standards.version {version!r} "
            "is unsupported; use 1.x.y"
        )
    if not _strings(profiles):
        errors.append(
            "bripe-standards.toml: standards.profiles must be an array of strings"
        )
    elif unknown := set(profiles) - KNOWN_PROFILES:
        errors.append(
            f"bripe-standards.toml: unknown profiles: {', '.join(sorted(unknown))}"
        )
    if not isinstance(project_type, str) or project_type not in PROJECT_TYPES:
        errors.append(
            "bripe-standards.toml: standards.project_type must be one of: "
            + ", ".join(sorted(PROJECT_TYPES))
        )
    if not _strings(checks):
        errors.append(
            "bripe-standards.toml: standards.checks must be an array of strings"
        )
    elif unknown := set(checks) - KNOWN_CHECKS:
        errors.append(
            f"bripe-standards.toml: unknown checks: {', '.join(sorted(unknown))}"
        )
    elif "manifest" not in checks:
        errors.append("bripe-standards.toml: standards.checks must include 'manifest'")
    if errors:
        return None, errors
    return Manifest(version, profiles, project_type, checks), []


def _check_profile_files(root: Path, manifest: Manifest) -> list[str]:
    if "python" in manifest.profiles and not (root / "pyproject.toml").is_file():
        return ["python profile: missing pyproject.toml"]
    return []


def _check_python_layout(root: Path, manifest: Manifest) -> list[str]:
    if "python" not in manifest.profiles:
        return []
    errors: list[str] = []
    if not (root / "tests").is_dir():
        errors.append("python profile: missing tests/ directory for isolated tests")
    pyproject = root / "pyproject.toml"
    if pyproject.is_file():
        try:
            with pyproject.open("rb") as handle:
                data = tomllib.load(handle)
        except tomllib.TOMLDecodeError:
            errors.append("python profile: pyproject.toml is not valid TOML")
        else:
            if not isinstance(data.get("tool", {}).get("ruff"), dict):
                errors.append(
                    "python profile: configure Ruff in pyproject.toml ([tool.ruff])"
                )
    return errors


def _major(version: str) -> int | None:
    first, _, _rest = version.partition(".")
    try:
        return int(first)
    except ValueError:
        return None


def _strings(value: object) -> bool:
    return isinstance(value, list) and all(isinstance(item, str) for item in value)
