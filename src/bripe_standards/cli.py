"""Command-line interface."""

from __future__ import annotations

import argparse
from pathlib import Path

from bripe_standards import __version__
from bripe_standards.validator import validate


def main() -> int:
    parser = argparse.ArgumentParser(prog="bripe-standards")
    parser.add_argument("--version", action="version", version=__version__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    check = subparsers.add_parser(
        "check", help="validate a repository without changing it"
    )
    check.add_argument(
        "path", nargs="?", default=".", help="repository root (default: .)"
    )
    check.add_argument(
        "--advisory", action="store_true", help="report failures but exit successfully"
    )
    args = parser.parse_args()
    errors = validate(Path(args.path).resolve())
    if not errors:
        print("bripe-standards: passed")
        return 0
    for error in errors:
        print(f"bripe-standards: error: {error}")
    return 0 if args.advisory else 1


if __name__ == "__main__":
    raise SystemExit(main())
