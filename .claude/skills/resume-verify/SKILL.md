---
name: resume-verify
description: Verify the generated resumes — ATS safety, page count, and visual rendering of the designed detailed build. Use after any change to resume.json or either builder script.
---

# Verifying the resumes

## 1. Rebuild

```bash
npm run resume:all
```

Read the output. It reports bullets held back by `BULLET_CAP` and any
`[[placeholder]]` metric that was stripped.

## 2. ATS check — the two-page build only

`Kishore-Prakash-Resume.docx` must have zero tables, zero shapes, an empty
header and footer, and no placeholders. These are exactly the features that
make parsers drop content.

```bash
python3 - <<'PY'
from docx import Document
d = Document("resume/Kishore-Prakash-Resume.docx")
txt = "\n".join(p.text for p in d.paragraphs)
print("tables", len(d.tables), "| shapes", len(d.inline_shapes),
      "| header", repr("".join(p.text for p in d.sections[0].header.paragraphs)),
      "| footer", repr("".join(p.text for p in d.sections[0].footer.paragraphs)),
      "| placeholders", txt.count("[["))
PY
```

Expect `tables 0 | shapes 0 | header '' | footer '' | placeholders 0`.

The **detailed build is intentionally not ATS-safe** — it uses tables, shading
and a footer by design. Do not "fix" it.

## 3. Page count

```bash
osascript -e 'tell application "Microsoft Word"
  open POSIX file "'$PWD'/resume/Kishore-Prakash-Resume.docx"
  set d to active document
  set pg to (compute statistics d statistic statistic pages)
  set ln to (compute statistics d statistic statistic lines)
  close d saving no
  return "pages=" & pg & " lines=" & ln
end tell'
```

Two-page build: must be `pages=2`. The budget is roughly 94 lines. If it spills,
see the length levers in README.md.

## 4. Look at the detailed build

Design changes must be seen, not assumed. Export and render:

```bash
osascript -e 'tell application "Microsoft Word"
  open POSIX file "'$PWD'/resume/Kishore-Prakash-Resume-Detailed.docx"
  set d to active document
  save as d file name "/tmp/detailed.pdf" file format format PDF
  close d saving no
end tell'
pdftoppm -png -r 100 /tmp/detailed.pdf /tmp/pg
```

Then read the `/tmp/pg-*.png` files. `pdftoppm` comes from `brew install poppler`.
Headless Chromium cannot render PDFs and `qlmanage` only gives you page one.

Check for: cards split across a page break, a section header stranded at the
bottom of a page, page numbers landing centre instead of right, and chip rows
running together into a solid block.
