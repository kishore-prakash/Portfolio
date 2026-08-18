# kishoreprakash.in

Personal portfolio and resume for Kishore Prakash. Static Astro site plus a
generated ATS-friendly resume.

## The one rule

**`src/data/resume.json` is the only place content lives.** The website reads
it, and `scripts/build-resume.py` turns it into the `.docx`. Edit the JSON, then
rebuild both. Nothing is duplicated between the site and the resume, so they
cannot drift apart.

## Commands

| Command | What it does |
|---|---|
| `npm run dev` | Dev server on http://localhost:4321 |
| `npm run build` | Static build into `dist/` |
| `npm run preview` | Serve `dist/` locally |
| `npm run resume` | Regenerate `resume/Kishore-Prakash-Resume.docx` |

Deployment steps are in [DEPLOY.md](DEPLOY.md).

## Layout

```
src/data/resume.json     content: basics, experience, projects, skills, awards
src/components/          Nav, Hero, Section, Timeline, ProjectGrid, Footer
src/layouts/Base.astro   head, SEO, JSON-LD, theme bootstrap
src/pages/               index.astro, 404.astro
scripts/build-resume.py  resume.json -> ATS .docx
resume/                  generated .docx and .pdf — NOT published
public/                  static passthrough — see DEPLOY.md for the files
                         that must stay at the domain root
```

## Metrics placeholders

Some bullets in `resume.json` contain `[[...]]` markers where a real number
belongs but has not been confirmed. `build-resume.py` strips the marker and
ships the bullet qualitatively rather than guessing a figure, and prints a list
of what it dropped. Fill the real numbers into `resume.json` and rerun
`npm run resume` — nothing else needs to change.

## Resume length and `BULLET_CAP`

The website shows every bullet in `resume.json`. The `.docx` does not — it is
held to two pages, so `BULLET_CAP` in `scripts/build-resume.py` caps how many
bullets each role prints:

```python
BULLET_CAP = [7, 4, 3, 3, 2, 2, 2]
```

One entry per role, newest first, so the current JLL role gets 7 bullets and
the oldest roles get 2. Roles beyond the end of the list reuse the last value.
This is recency weighting — recent work carries the detail, older work carries
only its headline achievements.

Bullets are taken in the order they appear in `resume.json`, so **put the
strongest ones first**; anything past the cap simply does not print.

`npm run resume` reports what it held back:

```
Trimmed for length (still in resume.json and on the website):
  - Mindtree / Senior Software Engineer: 3 bullet(s) held back for length
```

To print more, raise the numbers and re-check the page count — the two-page
budget is roughly 94 lines. Word will tell you:

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

Other levers on length, in the order worth reaching for: mark fewer projects
`"resumeFeature": true` in `resume.json` (each one costs two lines), shorten
the longest bullets, then adjust `BODY_SIZE` and the margins in
`setup_styles()`. Three pages is defensible for a lead with this much history
if you would rather keep the content.

## The resume is not on the website

There is no download link and the file lives outside `public/`, so it never
ships to `dist/`. To publish it again, point `OUT` in `scripts/build-resume.py`
back at `public/` and add a link in `src/components/Hero.astro`.

## Resume constraints

The `.docx` is built for ATS parsers, which is why it has no tables, no text
boxes, no columns, no images and nothing in the header or footer. Dates sit on
a right-aligned tab stop rather than in a table cell. Keep it that way; those
are the exact features that cause parsers to drop content.
