---
name: deploy-site
description: Build and deploy kishoreprakash.in to Hostinger, including the checks that catch a broken deploy. Use when Kishore wants to publish changes.
---

# Deploying

Deployment is manual: upload the **contents** of `dist/` into `public_html/` via
Hostinger hPanel or FTP. Full steps are in DEPLOY.md.

## Before uploading

```bash
npm run build
ls dist/app-ads.txt dist/apple-app-site-association dist/stotramaala/
```

All four must exist. They are linked from outside the site and break silently:

| File | Who reads it | Breaks if |
|---|---|---|
| `app-ads.txt` | Google AdMob | not at the domain root |
| `apple-app-site-association` | Apple universal links | renamed, given an extension, or not served as `application/json` |
| `stotramaala/privacy-policy.html`, `tnc.html` | the Stotramaala App Store listing | moved |

`.htaccess` is a hidden file. Confirm it actually uploaded — it carries the
`ForceType` for the association file and the `/portfolio/* → /` 301.

The resumes are **not** published. They live in `resume/`, outside `public/`,
so they never reach `dist/`.

## After uploading

```bash
curl -I https://kishoreprakash.in/
curl -s https://kishoreprakash.in/app-ads.txt
curl -I https://kishoreprakash.in/apple-app-site-association   # application/json
curl -I https://kishoreprakash.in/portfolio/                   # 301 to /
```

Then open a Stotramaala universal link on a real device — that is the only real
test of the association file.
