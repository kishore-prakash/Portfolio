---
name: resume-content
description: Change what the resume and website say — bullets, summary, skills, awards, education, job history. Use for any wording or content edit to Kishore's resume or portfolio.
---

# Editing resume content

## The one rule

`src/data/resume.json` is the only place content lives. The website reads it,
and both `.docx` builds are generated from it. Never edit a `.docx`, never
hard-code text in an `.astro` component.

After any edit:

```bash
npm run resume:all   # both .docx files
npm run build        # the site
```

## Never invent a number

Every figure must trace to a source Kishore confirmed or a document that
already records it. Confirmed so far: login time −50%, screen load −80%,
CI/CD −30%, JioAICloud app size −25%, team sizes 15/6/3/2/1, 7,000+ stotras,
19 languages (App Store listing), 11+ years (Oct 2014 onward).

If a bullet wants a number nobody has confirmed, write it as `[[what is the
number?]]`. Both builders strip the placeholder clause and ship the sentence
qualitatively. Ask Kishore for the value; do not estimate, and do not use
product-marketing figures from a JLL App Store page as personal impact.

## Where things go

| Change | Field |
|---|---|
| Job history | `experience[].roles[]` — newest first, `bullets` strongest first |
| Company one-liner | `experience[].context` — detailed build only |
| A shipped app or library | `projects[]` — see the `add-project` skill |
| Award | `awards[]` — newest first; add `short` for the two-page build |
| Skill | `skills[].items` — the two-page build merges 10 groups into 6 |
| Headline stats on the site | computed in `Hero.astro`, not stored |

Bullet style: past tense for past roles, present for the current one, one
achievement each, ~110 characters, action first. British spelling
("optimisation", "standardised") — the existing copy is consistent about it.

## Bullet order matters

The two-page build caps bullets per role via `BULLET_CAP` in
`scripts/build-resume.py` (`[7, 4, 3, 3, 2, 2, 2]`, newest role first).
Anything past the cap prints in the detailed build and on the website, but not
in the two-page one. Put the strongest bullets first.

## After editing

Run the `resume-verify` skill. The two-page build must stay at 2 pages and stay
free of tables; the detailed build has no page budget.
