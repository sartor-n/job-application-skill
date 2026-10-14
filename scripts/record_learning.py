"""Persist scoped feedback and load only the learnings relevant to an application.

Durable entries live in a managed JSON block in preferences.md; application-only and
unresolved entries live in application/learning.json. No Claude/Codex API is required.
"""
import argparse
import json
import os
import re
import sys
import tempfile
from datetime import date
from pathlib import Path

from paths import profile_dir

START = "<!-- job-application:learning:start -->"
END = "<!-- job-application:learning:end -->"
BLOCK = re.compile(re.escape(START) + r"\s*```json\s*\n(.*?)\n```\s*" + re.escape(END), re.S)
DURABLE = {"global", "archetype", "market"}


def entries_from(value):
    if not isinstance(value, dict) or value.get("schema_version") != 1:
        raise ValueError("learning records must be an object with schema_version: 1")
    entries = value.get("entries")
    if not isinstance(entries, list) or any(not isinstance(item, dict) or not item.get("id") for item in entries):
        raise ValueError("learning entries must be a list of records with IDs")
    if len({item["id"] for item in entries}) != len(entries):
        raise ValueError("duplicate learning IDs; resolve the conflict before writing")
    return entries


def read_preferences(pdir):
    text = (Path(pdir) / "preferences.md").read_text(encoding="utf-8")
    if START not in text and END not in text:
        return text, []
    match = BLOCK.search(text)
    if text.count(START) != 1 or text.count(END) != 1 or not match:
        raise ValueError("preferences.md learning block is malformed; preserve it and repair before writing")
    return text, entries_from(json.loads(match.group(1)))


def read_local(application):
    if application is None:
        return []
    path = Path(application) / "learning.json"
    if not path.is_file():
        return []
    entries = entries_from(json.loads(path.read_text(encoding="utf-8")))
    if any(item.get("scope") not in ("application", "pending") for item in entries):
        raise ValueError("application learning.json must contain only application/pending records")
    return entries


def atomic_write(path, text):
    path = Path(path)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent, delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(text)
        os.replace(temporary, path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def document(entries):
    return json.dumps({"schema_version": 1, "entries": entries}, indent=2, ensure_ascii=False) + "\n"


def normalize_entry(raw):
    keys = {"id", "date", "kind", "scope", "scope_value", "statement", "source", "confirmed", "details", "supersedes"}
    if not isinstance(raw, dict) or set(raw) - keys:
        raise ValueError("entry has unsupported fields or is not a JSON object")
    entry = dict(raw)
    entry.setdefault("scope_value", "")
    entry.setdefault("details", "")
    entry.setdefault("supersedes", [])
    if not isinstance(entry.get("id"), str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,99}", entry["id"]):
        raise ValueError("id must be a lowercase letter/digit followed by letters, digits or hyphens")
    try:
        date.fromisoformat(entry.get("date", ""))
    except (TypeError, ValueError):
        raise ValueError("date must be YYYY-MM-DD")
    if entry.get("kind") not in ("preference", "fact", "correction"):
        raise ValueError("kind must be preference, fact or correction")
    scope = entry.get("scope")
    if scope not in DURABLE | {"application", "pending"}:
        raise ValueError("scope must be global, archetype, market, application or pending")
    for key in ("statement", "source", "scope_value", "details"):
        value = entry.get(key)
        if not isinstance(value, str) or START in value or END in value or "{{" in value:
            raise ValueError(key + " must be text without placeholders or reserved block markers")
        if key in ("statement", "source") and not value.strip():
            raise ValueError(key + " must not be empty")
    if scope in ("archetype", "market"):
        if not entry["scope_value"].strip():
            raise ValueError("role/market scope requires scope_value")
    elif entry["scope_value"]:
        raise ValueError("scope_value is used only for archetype/market scopes")
    expected_confirmation = scope != "pending"
    if entry.get("confirmed") is not expected_confirmation:
        raise ValueError("resolved scopes require explicit confirmed: true; pending scope requires false")
    supersedes = entry["supersedes"]
    if not isinstance(supersedes, list) or any(not isinstance(item, str) for item in supersedes):
        raise ValueError("supersedes must be a list of earlier learning IDs")
    if entry["id"] in supersedes:
        raise ValueError("an entry cannot supersede itself")
    return entry


def record(raw, pdir, application=None):
    entry = normalize_entry(raw)
    root = Path(pdir)
    text, durable = read_preferences(root)
    if any(item.get("scope") not in DURABLE for item in durable):
        raise ValueError("preferences learning block contains a non-durable scope")
    local = read_local(application)
    all_entries = durable + local
    by_id = {item["id"]: item for item in all_entries}
    if len(by_id) != len(all_entries):
        raise ValueError("an ID exists in both profile and application records")
    if entry["id"] in by_id:
        previous = {key: value for key, value in by_id[entry["id"]].items() if key != "evidence_file"}
        if previous == entry:
            return {"status": "unchanged", "id": entry["id"], "scope": entry["scope"]}
        raise ValueError("this ID already has different content; use a new ID and supersedes")
    if any(old not in by_id for old in entry["supersedes"]):
        raise ValueError("supersedes names an unknown learning ID")
    if entry["scope"] == "pending" and entry["supersedes"]:
        raise ValueError("unresolved feedback cannot supersede a confirmed rule")

    if entry["scope"] not in DURABLE:
        if application is None or not Path(application).is_dir():
            raise ValueError("application/pending scope needs an existing application folder")
        target = Path(application) / "learning.json"
        atomic_write(target, document(local + [entry]))
    else:
        # Persist one concise record in preferences, with a linked evidence story for facts.
        if entry["kind"] in ("fact", "correction"):
            relative = "knowledge/learning-" + entry["id"] + ".md"
            path = root / relative
            entry["evidence_file"] = relative
            story = ("# " + entry["statement"] + "\n\n"
                     + "Date: " + entry["date"] + "\nScope: " + entry["scope"]
                     + (": " + entry["scope_value"] if entry["scope_value"] else "")
                     + "\nKind: " + entry["kind"] + "\n\n"
                     + "User source: " + entry["source"] + "\n\n"
                     + (entry["details"] or entry["statement"]) + "\n\n"
                     + "See [preferences](../preferences.md) for current scope and superseding corrections.\n")
            if path.exists() and path.read_text(encoding="utf-8") != story:
                raise ValueError("evidence file already exists with different content; no overwrite performed")
            path.parent.mkdir(exist_ok=True)
            atomic_write(path, story)
        block = START + "\n```json\n" + document(durable + [entry]).rstrip() + "\n```\n" + END
        if BLOCK.search(text):
            updated = BLOCK.sub(lambda _: block, text)
        else:
            updated = text.rstrip() + "\n\n## Confirmed Learnings\n\n" + block + "\n"
        target = root / "preferences.md"
        atomic_write(target, updated)
    return {"status": "saved", "id": entry["id"], "scope": entry["scope"], "path": str(target.resolve())}


def show(pdir, application=None, archetype=None, market=None):
    _, durable = read_preferences(pdir)
    local = read_local(application)
    candidates = [item for item in durable if item.get("confirmed") is True and (
        item.get("scope") == "global"
        or (item.get("scope") == "archetype" and archetype and item.get("scope_value") == archetype)
        or (item.get("scope") == "market" and market and item.get("scope_value") == market))]
    applicable_local = [item for item in local if item.get("scope") == "application" and item.get("confirmed") is True]
    superseded = {old for item in candidates + applicable_local for old in item.get("supersedes", [])}
    return {
        "durable": [item for item in candidates if item["id"] not in superseded],
        "application": [item for item in applicable_local if item["id"] not in superseded],
        "pending": [item for item in local if item.get("scope") == "pending" and item["id"] not in superseded],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("record", "show"))
    parser.add_argument("--entry")
    parser.add_argument("--application")
    parser.add_argument("--archetype")
    parser.add_argument("--market")
    parser.add_argument("--data-dir")
    parser.add_argument("--profile-dir")
    args = parser.parse_args()
    pdir = profile_dir(args.data_dir, args.profile_dir)
    try:
        if args.command == "record":
            if not args.entry:
                raise ValueError("record requires --entry FILE")
            raw = json.loads(Path(args.entry).read_text(encoding="utf-8"))
            result = record(raw, pdir, args.application)
        else:
            result = show(pdir, args.application, args.archetype, args.market)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    except (OSError, ValueError, UnicodeError) as exc:
        print("ERROR: " + str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
