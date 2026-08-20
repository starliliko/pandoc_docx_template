#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
DEFAULT_REFERENCE = SKILL_DIR / "templates" / "template_标题不编号-列表第二行顶格.docx"
DEFAULT_FILTER = SKILL_DIR / "markdown-to-docx.lua"


def split_extra_args(argv: list[str]) -> tuple[list[str], list[str]]:
    if "--" not in argv:
        return argv, []
    index = argv.index("--")
    return argv[:index], argv[index + 1 :]


def resolve_resource(path_text: str) -> Path:
    path = Path(path_text).expanduser()
    candidates = [
        path,
        SKILL_DIR / path_text,
        SKILL_DIR / "templates" / path_text,
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return path


def run(
    cmd: list[str],
    *,
    stdin: bytes | None = None,
    capture_stdout: bool = False,
) -> subprocess.CompletedProcess[bytes]:
    try:
        return subprocess.run(
            cmd,
            input=stdin,
            stdout=subprocess.PIPE if capture_stdout else None,
            check=True,
        )
    except FileNotFoundError:
        print("Pandoc executable not found. Install Pandoc or add it to PATH.", file=sys.stderr)
        raise SystemExit(127)
    except subprocess.CalledProcessError as error:
        raise SystemExit(error.returncode)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Convert Markdown to DOCX with the bundled Pandoc reference templates and Lua filter.",
    )
    parser.add_argument("input", help="Input Markdown file")
    parser.add_argument("-o", "--output", help="Output DOCX path. Default: INPUT.docx")
    parser.add_argument(
        "-r",
        "--reference",
        "--reference-doc",
        dest="reference",
        default=str(DEFAULT_REFERENCE),
        help="Reference DOCX template. Default: templates/template_标题不编号-列表第二行顶格.docx",
    )
    parser.add_argument(
        "-f",
        "--filter",
        "--lua-filter",
        dest="lua_filter",
        default=str(DEFAULT_FILTER),
        help="Lua filter. Default: markdown-to-docx.lua",
    )
    parser.add_argument("--from", dest="from_format", default="markdown", help="Pandoc input format. Default: markdown")
    parser.add_argument(
        "--direct",
        action="store_true",
        help="Convert directly from Markdown to DOCX without the Markdown -> HTML pass",
    )
    return parser


def main(argv: list[str]) -> int:
    parser_argv, extra_args = split_extra_args(argv)
    args = build_parser().parse_args(parser_argv)

    input_path = Path(args.input).expanduser()
    if not input_path.is_file():
        print(f"Input file not found: {input_path}", file=sys.stderr)
        return 1

    output_path = Path(args.output).expanduser() if args.output else input_path.with_suffix(".docx")
    reference_path = resolve_resource(args.reference)
    lua_filter_path = resolve_resource(args.lua_filter)

    if not reference_path.is_file():
        print(f"Reference DOCX not found: {reference_path}", file=sys.stderr)
        return 1
    if not lua_filter_path.is_file():
        print(f"Lua filter not found: {lua_filter_path}", file=sys.stderr)
        return 1

    if args.direct:
        run(
            [
                "pandoc",
                str(input_path),
                "-f",
                args.from_format,
                "-o",
                str(output_path),
                "--reference-doc",
                str(reference_path),
                "--lua-filter",
                str(lua_filter_path),
                *extra_args,
            ]
        )
    else:
        html = run(
            ["pandoc", str(input_path), "-f", args.from_format, "-t", "html"],
            capture_stdout=True,
        ).stdout
        run(
            [
                "pandoc",
                "-f",
                "html",
                "-o",
                str(output_path),
                "--reference-doc",
                str(reference_path),
                "--lua-filter",
                str(lua_filter_path),
                *extra_args,
            ],
            stdin=html,
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
