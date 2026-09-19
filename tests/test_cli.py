from __future__ import annotations

import sys
from pathlib import Path

from bripe_standards.cli import main


def test_advisory_exits_zero(monkeypatch, tmp_path: Path, capsys) -> None:
    monkeypatch.setattr(
        sys, "argv", ["bripe-standards", "check", str(tmp_path), "--advisory"]
    )
    assert main() == 0
    assert "missing manifest" in capsys.readouterr().out
