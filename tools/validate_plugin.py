#!/usr/bin/env python3
from __future__ import annotations

import ast
import json
import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MARKETPLACE_PATH = REPO_ROOT / ".agents" / "plugins" / "marketplace.json"
SEMVER_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")


def load_json(path: Path) -> dict:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"Cannot read valid JSON from {path}: {error}") from error
    if not isinstance(payload, dict):
        raise ValueError(f"Expected a JSON object in {path}")
    return payload


def require_string(payload: dict, field: str, context: str) -> str:
    value = payload.get(field)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{context}.{field} must be a non-empty string")
    return value


def resolve_inside_repo(relative_path: str) -> Path:
    target = (REPO_ROOT / relative_path).resolve()
    try:
        target.relative_to(REPO_ROOT.resolve())
    except ValueError as error:
        raise ValueError(f"Path escapes repository: {relative_path}") from error
    return target


def validate_skill(skill_root: Path) -> None:
    skill_md = skill_root / "SKILL.md"
    content = skill_md.read_text(encoding="utf-8")
    frontmatter = re.match(r"\A---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if frontmatter is None:
        raise ValueError(f"Missing YAML frontmatter in {skill_md}")
    header = frontmatter.group(1)
    if not re.search(r"(?m)^name:\s*\S+", header):
        raise ValueError(f"Missing skill name in {skill_md}")
    if not re.search(r"(?m)^description:\s*.+", header):
        raise ValueError(f"Missing skill description in {skill_md}")

    required_resources = [
        "scripts/md2docx.py",
        "scripts/docx2md.py",
        "templates/template_标题不编号-列表第二行顶格.docx",
        "markdown-to-docx.lua",
    ]
    for resource in required_resources:
        if not (skill_root / resource).is_file():
            raise ValueError(f"Missing bundled skill resource: {resource}")

    for script in sorted((skill_root / "scripts").glob("*.py")):
        ast.parse(script.read_text(encoding="utf-8"), filename=str(script))


def validate() -> None:
    marketplace = load_json(MARKETPLACE_PATH)
    marketplace_name = require_string(marketplace, "name", "marketplace")
    plugins = marketplace.get("plugins")
    if not isinstance(plugins, list) or len(plugins) != 1:
        raise ValueError("marketplace.plugins must contain exactly one plugin")

    entry = plugins[0]
    if not isinstance(entry, dict):
        raise ValueError("marketplace.plugins[0] must be an object")
    entry_name = require_string(entry, "name", "marketplace.plugins[0]")
    source = entry.get("source")
    if not isinstance(source, dict) or source.get("source") != "local":
        raise ValueError("marketplace plugin source must be local")
    source_path = require_string(source, "path", "marketplace.plugins[0].source")
    if not source_path.startswith("./"):
        raise ValueError("marketplace plugin source.path must start with ./")

    plugin_root = resolve_inside_repo(source_path)
    manifest = load_json(plugin_root / ".codex-plugin" / "plugin.json")
    manifest_name = require_string(manifest, "name", "plugin")
    if manifest_name != entry_name or plugin_root.name != manifest_name:
        raise ValueError("Plugin name must match marketplace entry and plugin folder")
    version = require_string(manifest, "version", "plugin")
    if SEMVER_RE.fullmatch(version) is None:
        raise ValueError(f"Invalid semantic version: {version}")

    skills_path = require_string(manifest, "skills", "plugin")
    skills_root = (plugin_root / skills_path).resolve()
    try:
        skills_root.relative_to(plugin_root.resolve())
    except ValueError as error:
        raise ValueError("plugin.skills escapes plugin root") from error
    skill_roots = sorted(path.parent for path in skills_root.glob("*/SKILL.md"))
    if not skill_roots:
        raise ValueError("Plugin does not contain any skills")
    for skill_root in skill_roots:
        validate_skill(skill_root)

    print(f"Marketplace valid: {marketplace_name}")
    print(f"Plugin valid: {manifest_name}@{version}")
    print(f"Skills valid: {len(skill_roots)}")


def main() -> int:
    try:
        validate()
    except (OSError, SyntaxError, ValueError) as error:
        print(f"Validation failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
