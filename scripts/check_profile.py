"""Validate profile structure AND substantive background coverage.

Exit 1 on errors. A completed flag cannot bypass missing evidence. Optional contact
fields may be blank. Use --data-dir or --profile-dir to keep the chosen storage root.
"""
import argparse
import re
import sys
from pathlib import Path

from paths import load_yaml, profile_dir
from check_readiness import background_errors, substantive

TAG_RE = re.compile(r"\[([A-Z][A-Z0-9_]*(?:\s*,\s*[A-Z][A-Z0-9_]*)*)\]")


def validate_profile(pdir):
    root = Path(pdir)
    errors, warnings = [], []
    try:
        profile = load_yaml(root / "profile.yaml")
    except (OSError, ValueError) as exc:
        return [str(exc)], warnings
    if profile.get("schema_version") != 2:
        errors.append("schema 2 coverage review required; preserve existing data and follow references/readiness.md")
    for key in ("identity", "contact", "style", "render"):
        if not isinstance(profile.get(key), dict):
            errors.append("profile.yaml: " + key + " must be a mapping")
    ident = profile.get("identity") if isinstance(profile.get("identity"), dict) else {}
    if not substantive(ident.get("name")):
        errors.append("profile.yaml: identity.name is empty or a placeholder")
    contact = profile.get("contact") if isinstance(profile.get("contact"), dict) else {}
    if "{{" in str(contact.get("email", "")):
        errors.append("profile.yaml: replace the email placeholder or leave it empty by choice")
    elif not contact.get("email"):
        warnings.append("contact.email is empty; confirm the intended contact details before submitting")
    markets = profile.get("markets")
    if not isinstance(markets, list) or not markets:
        errors.append("profile.yaml: at least one market is required")
        markets = []
    for market in markets:
        if not isinstance(market, dict):
            errors.append("each market must be a mapping")
            continue
        limit = market.get("page_limit")
        if type(limit) is not int or limit <= 0:
            errors.append("market page_limit must be a positive integer")
        if not substantive(market.get("code")):
            errors.append("each market needs a code")
        if market.get("english") not in (None, "british", "american"):
            warnings.append("market English variant should be british or american")
    render = profile.get("render") if isinstance(profile.get("render"), dict) else {}
    if render.get("filename_pattern") and "{doc}" not in str(render["filename_pattern"]):
        errors.append("render.filename_pattern must contain {doc}")

    tags = {"ALL"}
    try:
        archetypes = load_yaml(root / "archetypes.yaml").get("archetypes")
        if not isinstance(archetypes, list) or not archetypes:
            errors.append("archetypes.yaml: choose at least one evidenced candidate positioning")
            archetypes = []
        for item in archetypes:
            if not isinstance(item, dict):
                errors.append("each archetype must be a mapping")
                continue
            tag = str(item.get("tag", ""))
            if not re.fullmatch(r"[A-Z][A-Z0-9_]*", tag) or tag in tags:
                errors.append("archetype tags must be unique UPPER_CASE tags; ALL is reserved")
            tags.add(tag)
            titles = item.get("target_titles")
            if not isinstance(titles, list) or not titles or not all(substantive(title) for title in titles):
                errors.append("archetype " + tag + ": confirm target titles without placeholders")
    except (OSError, ValueError) as exc:
        errors.append(str(exc))

    try:
        master = (root / "master_cv.md").read_text(encoding="utf-8")
        if not re.search(r"\A---\s*\n.*?^read_only:\s*true\s*$.*?^---\s*$", master, re.M | re.S):
            errors.append("master_cv.md: frontmatter must contain read_only: true")
        if "{{" in master:
            errors.append("master_cv.md: unfinished placeholders remain")
        used = {tag.strip() for match in TAG_RE.finditer(master) for tag in match.group(1).split(",")}
        if used - tags:
            errors.append("master_cv.md: unknown archetype tags: " + ", ".join(sorted(used - tags)))
        for tag in sorted(tags - used - {"ALL"}):
            warnings.append("master_cv.md: no content explicitly tagged " + tag + "; check transferable/ALL evidence")
        sections = re.findall(
            r"^#\s+(?:WORK EXPERIENCE|EXPERIENCE|PROJECTS|EDUCATION|VOLUNTEERING)[^\n]*\n(.*?)(?=^#\s|\Z)",
            master, re.I | re.M | re.S)
        def has_content(section):
            clean = re.sub(r"<!--.*?-->", "", section, flags=re.S)
            return any(substantive(line.strip(" *-")) for line in clean.splitlines()
                       if not line.lstrip().startswith(("#", "[")))
        if not any(has_content(section) for section in sections):
            errors.append("master_cv.md: add actual career, project, study or volunteering evidence")
    except (OSError, UnicodeError) as exc:
        errors.append(str(exc))
    try:
        prefs = (root / "preferences.md").read_text(encoding="utf-8")
        if "{{" in prefs:
            errors.append("preferences.md: resolve placeholders or explicitly mark optional questions declined")
    except (OSError, UnicodeError) as exc:
        errors.append(str(exc))
    errors.extend(background_errors(root))
    return errors, warnings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir")
    parser.add_argument("--profile-dir")
    args = parser.parse_args()
    pdir = profile_dir(args.data_dir, args.profile_dir)
    errors, warnings = validate_profile(pdir)
    for message in warnings:
        print("WARN: " + message)
    for message in errors:
        print("ERROR: " + message)
    if errors:
        print("FAIL: " + str(len(errors)) + " error(s) in " + pdir)
        return 1
    print("OK: profile structure and recorded background validated in " + pdir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
