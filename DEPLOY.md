# Deploying kishoreprakash.in

The site is a static Astro build hosted on Hostinger. There is no CI step — you
build locally and upload the `dist/` folder.

## Build

```bash
npm install          # first time only
npm run resume       # regenerates resume/Kishore-Prakash-Resume.docx
npm run build        # writes dist/
```

The resume is **not published**. It is written to `resume/` rather than
`public/`, so it never reaches `dist/` and is not downloadable from the site.
Send it to people directly.

`npm run resume` needs `python-docx`:

```bash
python3 -m pip install --user python-docx
```

The PDF is exported from the `.docx` so the two always match. With Microsoft
Word installed:

```bash
osascript -e 'tell application "Microsoft Word"
  open POSIX file "'$PWD'/resume/Kishore-Prakash-Resume.docx"
  set d to active document
  save as d file name "'$PWD'/resume/Kishore-Prakash-Resume.pdf" file format format PDF
  close d saving no
end tell'
```

## Upload

The site now serves from the **domain root**, not `/portfolio/`.

1. Open hPanel → Files → File Manager, or connect over FTP.
2. Go to `public_html/`.
3. Delete the old `portfolio/` directory and any stale files at the root.
4. Upload **the contents of `dist/`** — not the `dist` folder itself — into
   `public_html/`.

`dist/` includes a `.htaccess` that 301s `/portfolio/*` to `/`, so old links
keep working. File managers often hide dotfiles: turn on "show hidden files"
and confirm `.htaccess` actually uploaded, otherwise the redirect and the
`apple-app-site-association` content type will both be missing.

## Verify after upload

```bash
curl -I https://kishoreprakash.in/                        # 200, no redirect
curl -I https://kishoreprakash.in/portfolio/              # 301 -> /
curl    https://kishoreprakash.in/app-ads.txt             # publisher line
curl -I https://kishoreprakash.in/apple-app-site-association   # application/json
curl -I https://kishoreprakash.in/stotramaala/privacy-policy.html   # 200
```

Then open the Stotramaala universal link on a real device and confirm it still
opens the app rather than Safari.

## Files that must stay at the root

These are served to third parties and break silently if they move:

| File | Who reads it |
|---|---|
| `app-ads.txt` | AdMob — only crawls the domain root. It was previously under `/portfolio/`, where AdMob could not see it. |
| `apple-app-site-association` | Apple, for Stotramaala universal links. Must be extensionless and served as `application/json`. |
| `stotramaala/privacy-policy.html`, `stotramaala/tnc.html` | Linked from the App Store listing. |

They live in `public/`, so Astro copies them to `dist/` untouched on every build.
