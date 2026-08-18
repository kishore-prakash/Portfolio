---
name: deploy-site
description: Build and deploy kishoreprakash.in to Hostinger, including the checks that catch a broken deploy. Use when Kishore wants to publish changes.
---

# Deploying

There are two paths, and they behave differently:

1. **Hostinger, manual** — upload the **contents** of `dist/` into `public_html/`
   via hPanel or FTP. Full steps in DEPLOY.md.


Check which host actually serves `kishoreprakash.in` before assuming a push
deployed anything.

## Before uploading

```bash
npm run build
```

The resumes are **not** published. They live in `resume/`, outside `public/`,
so they never reach `dist/`.

## After uploading

```bash
curl -I https://kishoreprakash.in/
```
