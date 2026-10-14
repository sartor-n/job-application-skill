"""Validate the profile directory. Exit 1 on errors, 0 on success (warnings allowed).

Usage: python check_profile.py [--data-dir D | --profile-dir P]
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from paths import load_profile, load_yaml  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

TAG_RE = re.compile(r"\[([A-Z][A-Z0-9_]*(?:\s*,\s*[A-Z][A-Z0-9_]*)*)\]")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir")
    ap.add_argument("--profile-dir")
    args = ap.parse_args()

    errors, warnings = [], []
    profile, pdir = load_profile(args.profile_dir, args.data_dir)
    if profile is None:
        print("ERROR: profile.yaml not found in " + pdir)
        return 1

    for key in ("identity", "contact", "markets", "style", "render"):
        if key not in profile:
            errors.append("profile.yaml: missing top-level key '" + key + "'")
    ident = profile.get("identity") or {}
    if not ident.get("name") or "{{" in str(ident.get("name")):
        errors.append("profile.yaml: identity.name is empty or still a placeholder")
    contact = profile.get("contact") or {}
    if not contact.get("email") or "{{" in str(contact.get("email")):
        errors.append("profile.yaml: contact.email is empty or still a placeholder")
    markets = profile.get("markets") or []
    if not markets:
        errors.append("profile.yaml: at least one market is required")
    for m in markets:
        code = m.get("code", "?")
        if not isinstance(m.get("page_limit"), int):
            errors.append("profile.yaml: market " + str(code) + " needs an integer page_limit")
        if m.get("english") not in (None, "british", "american"):
            warnings.append("profile.yaml: market " + str(code) + " english should be british or american")
    pattern = (profile.get("render") or {}).get("filename_pattern", "")
    if pattern and "{doc}" not in pattern:
        errors.append("profile.yaml: render.filename_pattern must contain {doc}")

    # archetypes
    tags = {"ALL"}
    apath = os.path.join(pdir, "archetypes.yaml")
    if os.path.exists(apath):
        arch = load_yaml(apath).get("archetypes") or []
        if not arch:
            errors.append("archetypes.yaml: no archetypes defined")
        for a in arch:
            tag = str(a.get("tag", "")).strip()
            if not re.fullmatch(r"[A-Z][A-Z0-9_]*", tag):
                errors.append("archetypes.yaml: tag '" + tag + "' must be UPPER_CASE letters, digits or underscores")
            tags.add(tag)
            if "{{" in str(a.get("target_titles", "")):
                warnings.append("archetypes.yaml: " + tag + " target_titles still contain placeholders")
    else:
        errors.append("archetypes.yaml missing")

    # master cv
    mpath = os.path.join(pdir, "master_cv.md")
    if os.path.exists(mpath):
        with open(mpath, "r", encoding="utf-8") as f:
            master = f.read()
        if not re.search(r"^read_only:\s*true", master, flags=re.M):
            errors.append("master_cv.md: frontmatter must contain 'read_only: true'")
        placeholders = re.findall(r"\{\{[^}]+\}\}", master)
        if placeholders:
            errors.append("master_cv.md: " + str(len(placeholders)) + " placeholders left, e.g. " + placeholders[0])
        used = set()
        for m in TAG_RE.finditer(master):
            for t in m.group(1).split(","):
                used.add(t.strip())
        unknown = sorted(t for t in used if t not in tags)
        if unknown:
            errors.append("master_cv.md: tags not defined in archetypes.yaml: " + ", ".join(unknown))
        for t in sorted(tags - {"ALL"}):
            if t not in used:
                warnings.append("master_cv.md: archetype " + t + " has no tagged content")
        if "# WORK EXPERIENCE" not in master.upper() and "# EXPERIENCE" not in master.upper():
            warnings.append("master_cv.md: no WORK EXPERIENCE section found")
    else:
        errors.append("master_cv.md missing")

    ppath = os.path.join(pdir, "preferences.md")
    if os.path.exists(ppath):
        with open(ppath, "r", encoding="utf-8") as f:
            prefs = f.read()
        left = re.findall(r"\{\{[^}]+\}\}", prefs)
        if left:
            warnings.append("preferences.md: " + str(len(left)) + " placeholders left, e.g. " + left[0])
    else:
        errors.append("preferences.md missing")

    for w in warnings:
        print("WARN: " + w)
    for e in errors:
        print("ERROR: " + e)
    if errors:
        print("FAIL: " + str(len(errors)) + " error(s) in " + pdir)
        return 1
    print("OK: profile valid in " + pdir + " (" + str(len(warnings)) + " warning(s))")
    print("onboarding_complete: " + str(profile.get("onboarding_complete", False)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
