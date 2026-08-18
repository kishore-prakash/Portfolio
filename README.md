# kishoreprakash.in

Personal portfolio and résumé for Kishore Prakash. Static Astro site plus a
generated ATS-friendly résumé.

## The one rule

**`src/data/resume.json` is the only place content lives.** The website reads
it, and `scripts/build-resume.py` turns it into the `.docx`. Edit the JSON, then
rebuild both. Nothing is duplicated between the site and the résumé, so they
cannot drift apart.

## Commands

| Command | What it does |
|---|---|
| `npm run dev` | Dev server on http://localhost:4321 |
| `npm run build` | Static build into `dist/` |
| `npm run preview` | Serve `dist/` locally |
| `npm run resume` | Regenerate `public/Kishore-Prakash-Resume.docx` |

Deployment steps are in [DEPLOY.md](DEPLOY.md).

## Layout

```
src/data/resume.json     content: basics, experience, projects, skills, awards
src/components/          Nav, Hero, Section, Timeline, ProjectGrid, Footer
src/layouts/Base.astro   head, SEO, JSON-LD, theme bootstrap
src/pages/               index.astro, 404.astro
scripts/build-resume.py  resume.json -> ATS .docx
public/                  static passthrough — see DEPLOY.md for the files
                         that must stay at the domain root
```

## Metrics placeholders

Some bullets in `resume.json` contain `[[...]]` markers where a real number
belongs but has not been confirmed. `build-resume.py` strips the marker and
ships the bullet qualitatively rather than guessing a figure, and prints a list
of what it dropped. Fill the real numbers into `resume.json` and rerun
`npm run resume` — nothing else needs to change.

## Résumé constraints

The `.docx` is built for ATS parsers, which is why it has no tables, no text
boxes, no columns, no images and nothing in the header or footer. Dates sit on
a right-aligned tab stop rather than in a table cell. Keep it that way; those
are the exact features that cause parsers to drop content.
