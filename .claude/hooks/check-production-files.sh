#!/bin/bash
# SessionStart: these four files are linked from outside the site — Google
# AdMob, Apple universal links and the Stotramaala App Store listing. They have
# gone missing from the working tree before. Silent unless something is wrong.
cd "$CLAUDE_PROJECT_DIR" 2>/dev/null || exit 0
missing=()
for f in public/app-ads.txt public/apple-app-site-association \
         public/stotramaala/privacy-policy.html public/stotramaala/tnc.html; do
  [ -f "$f" ] || missing+=("$f")
done
if [ ${#missing[@]} -gt 0 ]; then
  echo "MISSING production files (restore with: git checkout HEAD -- <path>):"
  printf '  %s\n' "${missing[@]}"
fi
