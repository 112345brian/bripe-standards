from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from bripe_standards.validator import validate

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.mark.parametrize("name", ["python_application", "python_utility", "no_runtime"])
def test_valid_fixtures(name: str) -> None:
    assert validate(FIXTURES / name) == []


def test_reports_python_profile_requirements(tmp_path: Path) -> None:
    shutil.copy(FIXTURES / "python_application" / "bripe-standards.toml", tmp_path)
    assert validate(tmp_path) == [
        "python profile: missing pyproject.toml",
        "python profile: missing tests/ directory for isolated tests",
    ]


def test_reports_unknown_profile(tmp_path: Path) -> None:
    (tmp_path / "bripe-standards.toml").write_text(
        "[standards]\nversion = '1.0.0'\nprofiles = ['ruby']\n"
        "project_type = 'application'\nchecks = ['manifest']\n"
    )
    assert "unknown profiles: ruby" in validate(tmp_path)[0]


def test_requires_manifest_check(tmp_path: Path) -> None:
    (tmp_path / "bripe-standards.toml").write_text(
        "[standards]\nversion = '1.0.0'\nprofiles = []\n"
        "project_type = 'documentation'\nchecks = []\n"
    )
    assert "must include 'manifest'" in validate(tmp_path)[0]
