---
name: add-project
description: Add a shipped app, SDK or library to the portfolio and resume, including verifying its App Store ID and fetching its icon. Use when Kishore mentions a new or missing project.
---

# Adding a project

## 1. Verify the App Store ID before writing it down

Six of the original IDs were wrong or dead. Always check:

```bash
curl -s "https://itunes.apple.com/lookup?id=<APP_ID>" | python3 -m json.tool | head -30
```

`resultCount: 0` means the app is gone. Mark it `"delisted": true` and omit
`link` — the site renders those as non-links with "no longer on the App Store".
Search by name if the ID is unknown:

```bash
curl -s "https://itunes.apple.com/search?term=<name>&entity=software&limit=5"
```

## 2. Fetch the icon

Icons live at `public/img/apps/<slug>.jpg` and are resolved by slug, not by a
path in the JSON. Download `artworkUrl512` from the lookup response with Python,
not a shell loop — a `set -e` loop once aborted midway and wrote one app's icon
under another app's name. Assert the md5s are unique afterwards.

## 3. The entry

```jsonc
{
  "slug": "kebab-case",            // must match the icon filename
  "name": "Display Name",
  "org": "Employer",               // "NXP Semiconductors (via CGI)" style for client work
  "category": "enterprise|sdk|nfc|personal",
  "featured": true,                 // site ordering only
  "resumeFeature": true,            // prints as a full entry in the two-page .docx — costs 2 lines
  "years": "2023 – present",
  "blurb": "What it is and what it does. First sentence is what the two-page resume prints.",
  "highlights": ["Short capability", "Short capability"],
  "tech": ["Swift", "NFC"],
  "teamSize": 6,
  "role": ["What Kishore actually did"],
  "link": "https://apps.apple.com/...",
  "appId": "1244213800"
}
```

Do not set both `appId` and `image` — `ProjectGrid.astro` resolves `appId`
first, so the `image` would never render. Use `image` only when there is no
App Store listing.

## 4. Verify

```bash
npm run build
```

Then check the project appears under the right filter chip and its icon loads.
Category counts are worth spot-checking; the filter uses `aria-pressed` and
hides list items.
