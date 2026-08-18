# Deploying kishoreprakash.in

The site is a static Astro build. Two ways to serve it: upload `dist/` to
Hostinger (manual, no CI step), or run it under pm2 behind Caddy on a server
you control.

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

## Upload (Hostinger)

The site now serves from the **domain root**, not `/portfolio/`.

1. Open hPanel → Files → File Manager, or connect over FTP.
2. Go to `public_html/`.
3. Delete the old `portfolio/` directory and any stale files at the root.
4. Upload **the contents of `dist/`** — not the `dist` folder itself — into
   `public_html/`.

## Verify after upload

```bash
curl -I https://kishoreprakash.in/                        # 200, no redirect
```

## Ubuntu server (pm2 + Caddy)

`ecosystem.config.cjs` runs `dist/` through the `serve` package (a
devDependency) and pm2 keeps that process alive.

```bash
git pull                        # or clone the repo onto the box
npm ci
npm run build                   # writes dist/
npm run pm2:start               # pm2 start ecosystem.config.cjs, serves :4321
pm2 save                        # persist across reboot
pm2 startup                     # first time only — run the printed command
```

Redeploy: `git pull && npm ci && npm run build && npm run pm2:restart`.
Check it: `pm2 status`, `npm run pm2:logs`.

Caddy reverse-proxies the domain to that port — `.htaccess`-only rules
(Apache) do not apply here, so anything Apache used to handle (redirects,
headers) needs doing directly in the Caddyfile instead.

### Caddy config

`/etc/caddy/Caddyfile` on the server (not part of this repo):

```
kishoreprakash.in {
	reverse_proxy localhost:4321
}
```

Caddy handles TLS automatically (Let's Encrypt) — no separate cert setup
needed. After editing:

```bash
sudo caddy validate --config /etc/caddy/Caddyfile
sudo systemctl reload caddy
```

Verify:

```bash
curl -I https://kishoreprakash.in/                        # 200, from Caddy
```
