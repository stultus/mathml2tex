"""Command-line entry point for mathml2tex.

Reads MathML (or HTML with inline <math> blocks) from stdin or a file
and prints the converted text to stdout.
"""
from __future__ import annotations

import argparse
import sys

from .converter import Mathml2TexError, convert_mathml2tex, sanitize_statement


def _looks_like_standalone_math(text: str) -> bool:
    return text.lstrip().startswith("<math")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="mathml2tex",
        description="Convert MathML to LaTeX.",
    )
    parser.add_argument(
        "file",
        nargs="?",
        help="Input file; reads from stdin if omitted.",
    )
    parser.add_argument(
        "--html",
        action="store_true",
        help="Treat input as HTML with inline <math> and sanitize the output.",
    )
    args = parser.parse_args(argv)

    if args.file:
        with open(args.file, encoding="utf-8") as fh:
            data = fh.read()
    else:
        data = sys.stdin.read()

    try:
        if args.html or not _looks_like_standalone_math(data):
            sys.stdout.write(sanitize_statement(data))
        else:
            sys.stdout.write(convert_mathml2tex(data))
    except Mathml2TexError as exc:
        print(f"mathml2tex: {exc}", file=sys.stderr)
        return 1
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
