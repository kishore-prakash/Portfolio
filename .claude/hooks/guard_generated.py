#!/usr/bin/env python3
"""PreToolUse: refuse edits to generated output.

Everything matched here is rebuilt from src/ or from src/data/resume.json, so
an edit made directly to it is silently thrown away on the next build.
Exit 2 blocks the tool call and hands the message back to Claude.
"""

import json
import re
import sys

RULES = [
    (r"/dist/", "dist/ is build output. Edit src/ and run `npm run build`."),
    (r"/resume/[^/]+\.(docx|pdf)$",
     "The resume files are generated. Edit src/data/resume.json and run "
     "`npm run resume:all`."),
    (r"/node_modules/", "node_modules/ is vendored. Change package.json instead."),
    (r"/\.astro/", ".astro/ is Astro's cache and is rebuilt on every run."),
]


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0
    path = payload.get("tool_input", {}).get("file_path", "")
    if not path:
        return 0
    for pattern, message in RULES:
        if re.search(pattern, path):
            print(f"Blocked edit to {path}\n{message}", file=sys.stderr)
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
