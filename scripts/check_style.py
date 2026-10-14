"""Lint generated markdown against the user's style rules and fabrication traps.

Usage: python check_style.py <file.md> [more files] [--data-dir D | --profile-dir P]
Checks: em/en dashes (if style.no_dashes), leftover placeholders, banned phrases and fabrication
traps from preferences.md, phone numbers (if contact.show_phone is false), third person in resume
summaries and cover letters, leftover HTML comments in cover letters.
Prints file:line: message. Exit 1 if anything is found.
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from paths import load_profile  # noqa: E402
from cv_parser import parse_markdown_cv, get_section  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PHONE_RE = re.compile(r"(?<![\w/])\+?\d[\d\s().-]{8,}\d(?![\w/])")
THIRD_PERSON_RE = re.compile(r"\b(he|she|they)\s+(is|has|owns|leads|led|built|manages|managed|drives|drove)\b", re.I)


def load_phrases(pdir):
    """Backticked phrases under '## Fabrication Traps' and '## Banned Phrases' in preferences.md."""
    path = os.path.join(pdir, "preferences.md")
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    phrases = []
    for heading in ("Fabrication Traps", "Banned Phrases"):
        m = re.search(r"^##\s+" + re.escape(heading) + r"\s*$(.*?)(?=^##\s|\Z)", text, flags=re.M | re.S)
        if not m:
            continue
        for phrase in re.findall(r"`([^`]+)`", m.group(1)):
            phrase = phrase.strip()
            if phrase and "{{" not in phrase:
                phrases.append((heading, phrase))
    return phrases


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--data-dir")
    ap.add_argument("--profile-dir")
    args = ap.parse_args()

    profile, pdir = load_profile(args.profile_dir, args.data_dir)
    profile = profile or {}
    style = profile.get("style") or {}
    contact = profile.get("contact") or {}
    first_name = (((profile.get("identity") or {}).get("name") or "").split() or [""])[0]
    no_dashes = style.get("no_dashes", True)
    phrases = load_phrases(pdir)
    name_third_person = re.compile(r"\b" + re.escape(first_name) + r"\s+(is|has|owns|leads|led|built|manages|drives)\b", re.I) if first_name else None

    findings = 0

    def report(path, lineno, msg):
        nonlocal findings
        findings += 1
        print(os.path.abspath(path) + ":" + str(lineno) + ": " + msg)

    for path in args.files:
        if not os.path.exists(path):
            report(path, 0, "file not found")
            continue
        with open(path, "r", encoding="utf-8") as f:
            lines = f.read().split("\n")
        base = os.path.basename(path).lower()
        if base == "preferences.md":
            print(os.path.abspath(path) + ":0: skipped (preferences.md defines the phrases the linter looks for)")
            continue
        is_resume = base == "resume.md"
        is_letter = base == "cover_letter.md"
        in_comment = False
        for i, line in enumerate(lines, 1):
            if "<!--" in line:
                in_comment = True
            if in_comment:
                if "-->" in line:
                    in_comment = False
                if is_letter and not line.strip().startswith("<!--") and "-->" not in line:
                    pass
                continue
            if no_dashes and ("\u2014" in line or "\u2013" in line):
                report(path, i, "em or en dash; use a comma, colon, parentheses or hyphen")
            if "{{" in line and "}}" in line:
                report(path, i, "placeholder left in text")
            low = line.lower()
            for heading, phrase in phrases:
                if phrase.lower() in low:
                    report(path, i, heading + ": '" + phrase + "'")
            if not contact.get("show_phone", False) and (is_resume or is_letter) and PHONE_RE.search(line) and not re.search(r"\d{2}/\d{4}", line):
                report(path, i, "looks like a phone number; profile says show_phone is false")
            if (is_resume or is_letter) and THIRD_PERSON_RE.search(line):
                report(path, i, "third person; write in the first person")
            if (is_resume or is_letter) and name_third_person and name_third_person.search(line):
                report(path, i, "third person by name; write in the first person")
        if is_letter and any("<!--" in l for l in lines):
            # comments are stripped from renders, but a leftover template comment usually means an unfinished letter
            print(os.path.abspath(path) + ":0: note: template comment block still present (ignored by renderers)")
        if is_resume:
            cv = parse_markdown_cv(path)
            prof = get_section(cv, "PROFILE")
            want = style.get("summary_paragraphs")
            if prof and want and len(prof["paragraphs"]) > int(want):
                report(path, 0, "profile has " + str(len(prof["paragraphs"])) + " paragraphs; style says " + str(want))
            for sec in cv["sections"]:
                for b in sec["blocks"]:
                    for item in b["items"]:
                        if len(item) > 260:
                            report(path, 0, "bullet over 260 characters in " + b["role"][:30] + ": '" + item[:50] + "...'")

    if findings:
        print("STYLE: " + str(findings) + " finding(s)")
        return 1
    print("STYLE: clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())
