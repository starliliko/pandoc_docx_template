---
name: pandoc-docx-template
description: "Use this skill when converting Markdown to Word DOCX or DOCX back to Markdown with Pandoc, especially when the output should use the bundled Chinese Word reference templates, heading numbering variants, list indentation variants, SCI paper templates, and Lua filters for HTML tags, image captions, font color, and inline code styles."
---

# Pandoc DOCX Template

## Overview

Use this skill to convert Markdown and DOCX files with Pandoc while applying the bundled Word reference templates in `templates/` and Lua filters in this folder. Prefer the scripts in `scripts/` for repeatable conversions, and call Pandoc directly when the local shell cannot run Bash scripts.

## Workflow

1. Resolve the directory containing this `SKILL.md`. Treat that directory as the skill root. Run bundled scripts with the skill root as the working directory, or use absolute paths derived from it; do not assume the user's workspace is the skill root.

2. Check that Pandoc is available:

```bash
pandoc --version
```

If Pandoc is unavailable, explain that it is an external runtime dependency. Do not install or modify system packages without the user's approval.

3. Choose the conversion direction:

- Markdown to DOCX: use `scripts/md2docx.py`.
- DOCX to Markdown: use `scripts/docx2md.py`.

4. Choose a reference DOCX template when exporting Word:

| Template | Use for |
| --- | --- |
| `templates/template_标题不编号-列表第二行顶格.docx` | Default Chinese layout, headings without numbering, wrapped list lines flush left |
| `templates/template_标题不编号-列表第二行缩进.docx` | Headings without numbering, wrapped list lines indented |
| `templates/template_标题编号-列表第二行顶格.docx` | Numbered headings, wrapped list lines flush left |
| `templates/template_标题编号-列表第二行缩进.docx` | Numbered headings, wrapped list lines indented |
| `templates/template_标题不编号-列表第二行顶格-无首行缩进.docx` | No heading numbering and no first-line paragraph indent |
| `templates/template_sci论文-标题编号.docx` | SCI-style paper layout with numbered headings |
| `templates/template_sci论文-标题不编号.docx` | SCI-style paper layout without heading numbering |

## Markdown to DOCX

Use the default template and bundled aggregate Lua filter:

```bash
python scripts/md2docx.py input.md -o output.docx
```

Choose another template:

```bash
python scripts/md2docx.py input.md -o output.docx \
  --reference "templates/template_sci论文-标题编号.docx"
```

Pass additional Pandoc options after `--`:

```bash
python scripts/md2docx.py input.md -o output.docx \
  --reference "templates/template_标题编号-列表第二行顶格.docx" \
  -- --highlight-style tango
```

If Bash is unavailable, run the equivalent Pandoc pipeline from the skill folder:

```powershell
pandoc input.md -t html | pandoc -f html -o output.docx `
  --reference-doc "templates/template_标题不编号-列表第二行顶格.docx" `
  --lua-filter "markdown-to-docx.lua"
```

The Markdown-to-DOCX workflow intentionally converts Markdown to HTML first, then HTML to DOCX. This preserves more HTML-like Markdown content than a direct Markdown-to-DOCX conversion, including common tags handled by the Lua filters.

## DOCX to Markdown

Convert Word to GitHub Flavored Markdown and extract embedded media:

```bash
python scripts/docx2md.py input.docx -o output.md --media-dir assets
```

If Bash is unavailable, run Pandoc directly:

```powershell
pandoc "input.docx" -t gfm -o output.md --extract-media=./assets --wrap=none
```

## Lua Filters

Use `markdown-to-docx.lua` as the default aggregate filter for Markdown-to-DOCX exports. Load individual filters only when a narrower conversion is needed:

- `lua/markdown-html-recognition.lua`: recognize Markdown content containing HTML tags such as `<sub>`, `<sup>`, and `<img>`.
- `lua/image-title-to-caption.lua`: use image title text as the Word caption and apply the `Figure` style.
- `lua/image-title-to-caption-add-number.lua`: add numbering for image captions.
- `lua/preserve_font_color.lua`: preserve text color from HTML spans such as `<span style="color:red">`.
- `lua/add-inline-code.lua`: apply the custom `Inline Code` style to inline code, separate from code block styling.

## Validation

After conversion, verify that the expected output file exists and that Pandoc did not report filter or reference-document errors. For DOCX output intended for final delivery, inspect it in Windows Microsoft Word because these templates were tested primarily with Windows Office and may render differently in WPS or macOS Word.
