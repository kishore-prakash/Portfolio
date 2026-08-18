#!/usr/bin/env python3
"""PostToolUse: validate src/data/resume.json after any edit.

resume.json feeds the website and both .docx builds, so one broken edit breaks
three outputs at once. Exit 2 on anything structurally wrong; otherwise print
reminders, which Claude sees as context.
"""

import json
import pathlib
import sys

REQUIRED = ["basics", "competencies", "experience", "projects", "skills",
            "education", "certifications", "awards", "languages"]


def main() -> int:
    path = pathlib.Path("src/data/resume.json")
    if not path.exists():
        return 0
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as e:
        print(f"src/data/resume.json is not valid JSON: {e}", file=sys.stderr)
        return 2

    missing = [k for k in REQUIRED if k not in data]
    if missing:
        print(f"src/data/resume.json is missing top-level keys: {missing}",
              file=sys.stderr)
        return 2

    notes = []
    # meta.note documents the [[...]] convention, so it is not a live placeholder
    content = {k: v for k, v in data.items() if k != "meta"}
    placeholders = json.dumps(content).count("[[")
    if placeholders:
        notes.append(f"{placeholders} unconfirmed [[metric]] placeholder(s) still "
                     f"present. They are stripped from every output, never guessed.")
    for p in data["projects"]:
        if p.get("appId") and p.get("image"):
            notes.append(f"project '{p['slug']}' has both appId and image; "
                         f"ProjectGrid resolves appId first, so image never renders")
    notes.append("resume.json changed — run `npm run resume:all` and `npm run build`.")
    print("\n".join(notes))
    return 0


if __name__ == "__main__":
    sys.exit(main())
