"""Validate recorded career coverage and a job-specific tailoring decision.

This checks evidence references and missing/stale decisions, not the truth or semantic
sufficiency of a claim. The agent must review sources as described in references/readiness.md.
Exit 1 on missing/invalid information. --fingerprints is a read-only utility.
"""
import argparse
import hashlib
import json
import re
import sys
from datetime import date
from pathlib import Path

from paths import load_yaml, profile_dir

AREAS = (
    "career_history", "experience_and_outcomes", "strengths", "career_direction",
    "preferences_and_constraints", "claim_boundaries",
)


def substantive(value):
    return (isinstance(value, str) and bool(value.strip()) and "{{" not in value
            and not re.fullmatch(r"(?i)\s*(?:unknown|none|n/a|tbd|todo|ready|complete)\s*", value))


def dated(value):
    try:
        date.fromisoformat(str(value))
        return True
    except (TypeError, ValueError):
        return False


def read_json(path):
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(str(path) + " must contain an object")
    return value


def normalized(text):
    return " ".join(text.split())


def evidence_errors(refs, pdir, application=None):
    if not isinstance(refs, list) or not refs:
        return ["needs at least one actual source excerpt"]
    errors = []
    for ref in refs:
        if not isinstance(ref, dict) or not substantive(ref.get("quote")):
            errors.append("evidence needs a substantive quote")
            continue
        local = "application_path" in ref
        relative = ref.get("application_path" if local else "path")
        root = Path(application if local and application else pdir).resolve()
        if (not isinstance(relative, str) or not relative
                or (local and (application is None or relative != "learning.json"))
                or (local and "path" in ref)):
            errors.append("evidence has an invalid source path")
            continue
        path = (root / relative).resolve()
        permitted = local or relative in ("master_cv.md", "preferences.md") or (
            relative.startswith("knowledge/") and relative.endswith(".md"))
        if not permitted or not path.is_relative_to(root) or not path.is_file():
            errors.append("evidence source is missing or outside allowed candidate sources: " + relative)
            continue
        try:
            if local:
                records = read_json(path).get("entries", [])
                if not isinstance(records, list):
                    raise ValueError("learning entries must be a list")
                text = "\n".join(str(item.get(key, "")) for item in records
                                 if isinstance(item, dict) and not item.get("superseded_by")
                                 for key in ("statement", "source", "details"))
            else:
                text = path.read_text(encoding="utf-8")
            if normalized(ref["quote"]) not in normalized(text):
                errors.append("quoted evidence not found in " + relative)
        except (OSError, ValueError, UnicodeError) as exc:
            errors.append(str(exc))
    return errors


def background_errors(pdir):
    path = Path(pdir) / "readiness.yaml"
    if not path.is_file():
        return ["readiness.yaml missing: review career history, outcomes, strengths, goals, preferences and claim boundaries"]
    try:
        record = load_yaml(path)
    except (OSError, ValueError) as exc:
        return [str(exc)]
    errors = []
    if record.get("schema_version") != 2:
        errors.append("readiness.yaml must use schema_version: 2")
    if not dated(record.get("reviewed_at")):
        errors.append("readiness.yaml needs a reviewed_at date (YYYY-MM-DD)")
    if record.get("blocking_questions") != []:
        errors.append("background has unresolved blocking questions (or is missing the question list)")
    areas = record.get("areas")
    if not isinstance(areas, dict):
        return errors + ["readiness.yaml needs an areas mapping"]
    for area in AREAS:
        entry = areas.get(area)
        if not isinstance(entry, dict) or entry.get("status") != "ready":
            errors.append(area + ": background is not ready")
            continue
        if not substantive(entry.get("summary")):
            errors.append(area + ": explain what is understood")
        errors.extend(area + ": " + error for error in evidence_errors(entry.get("evidence"), pdir))
    return errors


def digest_files(root, files):
    digest = hashlib.sha256()
    for path in sorted(files):
        relative = path.relative_to(root).as_posix()
        digest.update(relative.encode("utf-8") + b"\0")
        digest.update(path.read_bytes() + b"\0")
    return digest.hexdigest()


def fingerprints(pdir, application=None):
    root = Path(pdir)
    files = [root / name for name in (
        "profile.yaml", "master_cv.md", "preferences.md", "archetypes.yaml", "readiness.yaml")
        if (root / name).is_file()]
    files.extend((root / "knowledge").rglob("*.md"))
    result = {"profile_fingerprint": digest_files(root, files)}
    if application:
        folder = Path(application)
        job_files = [folder / name for name in ("job_description.md", "learning.json")
                     if (folder / name).is_file()]
        meta = read_json(folder / "metadata.json")
        target = {key: meta.get(key) for key in ("company", "position", "market", "archetype", "source_url")}
        raw = digest_files(folder, job_files) + json.dumps(target, sort_keys=True, ensure_ascii=False)
        result["job_fingerprint"] = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    return result


def application_errors(pdir, application):
    folder = Path(application)
    try:
        record = load_yaml(folder / "readiness.yaml")
        meta = read_json(folder / "metadata.json")
        expected = fingerprints(pdir, folder)
    except (OSError, ValueError, UnicodeError) as exc:
        return ["application assessment: " + str(exc)]
    errors = []
    if record.get("schema_version") != 2 or not dated(record.get("reviewed_at")):
        errors.append("application readiness needs schema_version: 2 and reviewed_at: YYYY-MM-DD")
    for key, value in expected.items():
        if record.get(key) != value:
            errors.append(key + ": missing or stale; review changed sources before refreshing")
    for name in ("job_description.md", "roast.md"):
        path = folder / name
        if not path.is_file() or not substantive(path.read_text(encoding="utf-8")):
            errors.append(name + " must contain the completed intake/assessment")
    if meta.get("tailoring_approved") is not True or meta.get("status") == "declined":
        errors.append("user's decision to proceed after the fit assessment has not been recorded")
    if not substantive(meta.get("archetype")):
        errors.append("select a supported archetype before tailoring")
    if record.get("blocking_questions") != []:
        errors.append("application has unresolved blocking questions (or is missing the question list)")
    goals = record.get("goals_fit")
    if (not isinstance(goals, dict) or goals.get("status") not in ("aligned", "tradeoff", "mismatch")
            or not substantive(goals.get("summary"))):
        errors.append("assess whether the role serves the user's goals and wishes")
    requirements = record.get("requirements")
    if not isinstance(requirements, list) or not requirements:
        return errors + ["assess the material job requirements before tailoring"]
    for index, item in enumerate(requirements, 1):
        label = "requirement " + str(index) + ": "
        if not isinstance(item, dict):
            errors.append(label + "must be a mapping")
            continue
        if not substantive(item.get("requirement")) or not substantive(item.get("note")):
            errors.append(label + "needs the actual requirement and an evidence/gap explanation")
        if item.get("importance") not in ("must_have", "nice_to_have"):
            errors.append(label + "specify must_have or nice_to_have")
        status = item.get("status")
        if status in ("supported", "transferable"):
            errors.extend(label + error for error in evidence_errors(item.get("evidence"), pdir, folder))
        elif status == "unknown":
            if item.get("importance") != "nice_to_have" or item.get("omit_from_claims") is not True:
                errors.append(label + "resolve material unknowns; omit any unverified nonmaterial claim")
        elif status != "confirmed_gap":
            errors.append(label + "invalid evidence status")
    return errors


def tailoring_errors(pdir, application):
    # Imported lazily to keep check_profile usable without a circular import.
    from check_profile import validate_profile
    errors, _ = validate_profile(pdir)
    return errors + application_errors(pdir, application)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir")
    parser.add_argument("--profile-dir")
    parser.add_argument("--application")
    parser.add_argument("--fingerprints", action="store_true")
    args = parser.parse_args()
    pdir = profile_dir(args.data_dir, args.profile_dir)
    try:
        if args.fingerprints:
            print(json.dumps(fingerprints(pdir, args.application), indent=2))
            return 0
        if args.application:
            errors = tailoring_errors(pdir, args.application)
        else:
            from check_profile import validate_profile
            errors, _ = validate_profile(pdir)
        for error in errors:
            print("BLOCKED: " + error)
        if errors:
            return 1
        print("READY: recorded background" + (" and application assessment" if args.application else "") + " validated")
        return 0
    except (OSError, ValueError, UnicodeError) as exc:
        print("BLOCKED: " + str(exc))
        return 1


if __name__ == "__main__":
    sys.exit(main())
