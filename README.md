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
| `npm run resume` | Regenerate the two-page `resume/Kishore-Prakash-Resume.docx` |
| `npm run resume:detailed` | Regenerate `resume/Kishore-Prakash-Resume-Detailed.docx` |
| `npm run resume:all` | Regenerate both |

Deployment steps are in [DEPLOY.md](DEPLOY.md).

## Layout

```
src/data/resume.json     content: basics, experience, projects, skills, awards
src/components/          Nav, Hero, Section, Timeline, ProjectGrid, Footer
src/layouts/Base.astro   head, SEO, JSON-LD, theme bootstrap
src/pages/               index.astro, 404.astro
scripts/resume_common.py resume.json loading, placeholder stripping, grouping
scripts/build-resume.py  -> two-page ATS .docx
scripts/build-resume-detailed.py  -> designed, human-facing .docx
resume/                  generated .docx files (default + detailed) — NOT published
public/                  static passthrough — see DEPLOY.md for the files
                         that must stay at the domain root
```

## Metrics placeholders

Some bullets in `resume.json` contain `[[...]]` markers where a real number
belongs but has not been confirmed. `build-resume.py` strips the marker and
ships the bullet qualitatively rather than guessing a figure, and prints a list
of what it dropped. Fill the real numbers into `resume.json` and rerun
`npm run resume` — nothing else needs to change.

## Two resumes, one dataset

`resume.json` feeds two documents, built by two scripts, for two audiences:

| | `Kishore-Prakash-Resume.docx` | `Kishore-Prakash-Resume-Detailed.docx` |
|---|---|---|
| Built by | `scripts/build-resume.py` | `scripts/build-resume-detailed.py` |
| Length | 2 pages | ~9 pages |
| Audience | ATS, job portals, recruiters | hiring managers, interview panels, internal profiles |
| ATS-safe | yes | **no — by design** |

The default build is a single linear text flow: no tables, no colour, no
header or footer, bullets capped by `BULLET_CAP`, projects condensed. Those are
exactly the constraints that keep a parser from dropping content.

The detailed build is designed for a human reader, so it spends what the ATS
build cannot: Georgia display type against Calibri body copy, the site's blue
(`#0055D4`) on zinc ink, letter-spaced section labels over hairline rules,
soft-filled competency chips, and project cards with an accent edge. It also
carries everything the two-page build holds back — every bullet, company
context lines, all ten skill groups, all 22 projects with highlights, tech,
role and link, and every award with its citation.

Because it uses tables, shading and a footer, **do not upload the detailed
build to a job portal.** Send it to people.

Both read the same `src/data/resume.json` and share `scripts/resume_common.py`,
so they cannot disagree about the facts — only about how much of them to show.

## Resume length and `BULLET_CAP`

The website shows every bullet in `resume.json`. The default `.docx` does not —
it is held to two pages, so `BULLET_CAP` in `scripts/build-resume.py` caps how
many bullets each role prints:

```python
BULLET_CAP = [7, 4, 3, 3, 2, 2, 2]
```

One entry per role, newest first, so the current JLL role gets 7 bullets and
the oldest roles get 2. Roles beyond the end of the list reuse the last value.
This is recency weighting — recent work carries the detail, older work carries
only its headline achievements.

Bullets are taken in the order they appear in `resume.json`, so **put the
strongest ones first**; anything past the cap simply does not print.

`npm run resume` reports what it held back — all of which still prints in the
`--detailed` build:

```
Trimmed for length (still in resume.json, on the website and in the --detailed build):
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

There is no download link and the files live outside `public/`, so they never
ship to `dist/`. To publish again, point `OUT` (and `OUT_DETAILED`) in
`scripts/build-resume.py` back at `public/` and add a link in
`src/components/Hero.astro`.

## Resume constraints

The `.docx` is built for ATS parsers, which is why it has no tables, no text
boxes, no columns, no images and nothing in the header or footer. Dates sit on
a right-aligned tab stop rather than in a table cell. Keep it that way; those
are the exact features that cause parsers to drop content.
