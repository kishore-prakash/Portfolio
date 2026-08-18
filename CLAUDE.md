# kishoreprakash.in — working notes

Personal portfolio and resume for Kishore Prakash. Astro 7 + Tailwind v4 static
site, plus two generated `.docx` resumes (PDFs alongside them, both tracked).

Two deploy paths exist: the manual Hostinger upload documented in DEPLOY.md, and
`.github/workflows/deploy.yml`, which builds on push to `master` and publishes to
GitHub Pages. **They are not equivalent** — see below.

## The one rule

`src/data/resume.json` is the only place content lives. The website reads it and
both resume builders generate from it. Editing a `.docx` or hard-coding copy in a
component means the next build throws the change away.

```
src/data/resume.json  ─┬─→  Astro site            → dist/
                       ├─→  build-resume.py       → 2-page ATS .docx
                       └─→  build-resume-detailed.py → designed .docx
```

## Never invent a figure

Every number must trace to something Kishore confirmed or a document that already
records it. Unconfirmed metrics are written `[[like this]]`; both builders strip
the clause and ship the sentence qualitatively rather than guessing. Marketing
numbers from a JLL App Store listing are product claims, not Kishore's measured
impact, and must not appear as personal achievements.

## Two resumes, two audiences

| | `Kishore-Prakash-Resume.docx` | `Kishore-Prakash-Resume-Detailed.docx` |
|---|---|---|
| Script | `scripts/build-resume.py` | `scripts/build-resume-detailed.py` |
| Length | 2 pages (~94 lines is the budget) | ~9 pages |
| For | ATS, portals, recruiters | hiring managers, panels, internal profiles |
| ATS-safe | yes — no tables, shapes, header or footer | **no, by design** — tables, shading, footer |

The detailed build's use of tables is deliberate. Do not "fix" it, and do not
send it to a job portal.

Shared loading, placeholder stripping and grouping live in
`scripts/resume_common.py`.

## Files that must stay at the domain root

These are linked from outside the site and fail silently when moved:
`public/app-ads.txt` (AdMob only crawls the root), `public/apple-app-site-association`
(Apple universal links — extensionless, served as `application/json` via `.htaccess`),
and `public/stotramaala/{privacy-policy,tnc}.html` (linked from the App Store listing).

They have gone missing from the working tree twice. A `SessionStart` hook checks
for them; if it reports any as missing, restore with `git checkout HEAD -- <path>`.
Suspect an external sync process on `~/Documents`, not the build.

## GitHub Pages cannot do everything Hostinger does

`.htaccess` is Apache-only, so on GitHub Pages the `/portfolio/* → /` 301 and the
`ForceType application/json` for `apple-app-site-association` are both inert.
Apple requires that file to be served as `application/json`, so universal links
into Stotramaala can break on a Pages deploy even though the file uploads fine.
Confirm which host is authoritative for `kishoreprakash.in` before assuming a
push deployed anything.

## Commands

```bash
npm run dev             # localhost:4321
npm run build           # → dist/
npm run resume          # two-page .docx
npm run resume:detailed # designed .docx
npm run resume:all      # both
```

Astro's preview server keeps a pid file that can go stale; `npx astro preview stop`
then start again, and read the port from the startup line rather than assuming it.

## Verifying, not assuming

- Design changes to the detailed resume must be **looked at**: export to PDF via
  Word AppleScript, render with `pdftoppm` (`brew install poppler`), read the PNGs.
  Headless Chromium cannot render PDFs; `qlmanage` gives page one only.
- Site changes: Playwright is already in `node_modules`. Check 0px horizontal
  overflow at 375/768/1440, no `pageerror`, no responses ≥400, no broken images.
- LinkedIn returns HTTP 999 and nxp.com returns 404 to every automated client,
  including for their own root domains. That is bot protection, not a dead link.
  Verify with headless Chromium before removing a URL.

## Conventions

- British spelling in copy ("optimisation", "standardised").
- Awards are newest first; the two-page build uses each award's `short` name.
- A project may set `appId` **or** `image`, never both — `ProjectGrid.astro`
  resolves `appId` first, so the `image` would be dead.
- Icons resolve by slug: `public/img/apps/<slug>.jpg`.

## Skills in this repo

`.claude/skills/` — `resume-content`, `resume-verify`, `add-project`, `deploy-site`.
Deployment detail is in [DEPLOY.md](DEPLOY.md); how the builds work is in [README.md](README.md).
