"""Rebuild the case-study table in README.md from cases.json.

The table sits between <!-- cases:start --> and <!-- cases:end --> in README.md.
Everything outside those markers is left untouched.

Checks before writing (the run fails, and README is not changed, if any fails):
- every visible case has id, readme_title, question, check and case_url;
- ids are unique;
- a case_url pointing into this repo points to a file that exists.

Usage: python .github/scripts/build_readme.py [--check]
  --check  only report whether README.md is up to date (exit 1 if not).
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
README = ROOT / "README.md"
CASES = ROOT / "cases.json"
START, END = "<!-- cases:start -->", "<!-- cases:end -->"
REPO_BLOB = "https://github.com/meemoprasad/meeba-brain/blob/main/"
REQUIRED = ("id", "readme_title", "question", "check", "case_url")


def cell(text):
    # A table cell must stay on one line, and a bare | would split the cell.
    return " ".join(str(text).split()).replace("|", "\\|")


def build_table(cases):
    errors, seen, rows = [], set(), []
    for i, c in enumerate(cases):
        if c.get("show") is False:
            continue
        name = c.get("id") or f"case #{i + 1}"
        missing = [k for k in REQUIRED if not c.get(k)]
        if missing:
            errors.append(f"{name}: missing {', '.join(missing)}")
            continue
        if c["id"] in seen:
            errors.append(f"{name}: duplicate id")
        seen.add(c["id"])
        link = c["case_url"]
        if link.startswith(REPO_BLOB):
            link = link[len(REPO_BLOB):]
            if not (ROOT / link).is_file():
                errors.append(f"{name}: {link} does not exist in the repo")
        rows.append(f"| [{cell(c['readme_title'])}]({link}) | {cell(c['question'])} | {cell(c['check'])} |")
    if not rows and not errors:
        errors.append("no visible case in cases.json")
    table = "\n".join(["| Case | Question | What to check |", "|---|---|---|", *rows])
    return table, errors


def main():
    check_only = "--check" in sys.argv
    data = json.loads(CASES.read_text(encoding="utf-8"))
    table, errors = build_table(data.get("cases", []))
    if errors:
        print("cases.json has problems, README.md not changed:")
        for e in errors:
            print("  -", e)
        sys.exit(1)

    readme = README.read_text(encoding="utf-8")
    pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.S)
    if not pattern.search(readme):
        print(f"README.md has no {START} ... {END} block")
        sys.exit(1)
    updated = pattern.sub(lambda _: f"{START}\n{table}\n{END}", readme, count=1)

    if updated == readme:
        print("README.md is up to date.")
        return
    if check_only:
        print("README.md is out of date with cases.json.")
        sys.exit(1)
    README.write_text(updated, encoding="utf-8")
    print("README.md case table rebuilt.")


if __name__ == "__main__":
    main()
