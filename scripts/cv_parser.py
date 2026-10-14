"""Parse a resume.md into a renderer-neutral structure.

Grammar accepted (see references/resume_format.md):
  ---                  optional YAML frontmatter (market, target_title, location_line, company, position)
  # Full Name
  **Target Title**
  # SECTION            section header: any heading whose text is a known alias or all caps
  paragraphs           free text lines; a blank line separates paragraphs
  * bullet             bullets (also "- ")
  ## Role | Company    block heading inside a section (also "### ", or a bare line containing " | ")
  MM/YYYY - MM/YYYY    date line right after a block heading (also "Mon YYYY", "YYYY", "Present")

Output:
  {
    "meta": {...frontmatter...},
    "name": str, "target_title": str,
    "sections": [ {"key", "title", "kind", "paragraphs": [...], "items": [...],
                   "blocks": [{heading, role, org, date, items, paragraphs}]} ]
  }
Inline markup (**bold**, *italic*, [text](url), escaped characters) stays in the strings.
parse_inline() converts a string into runs that both renderers consume.
"""
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SECTION_ALIASES = {
    "PROFILE": ["PROFILE", "PROFESSIONAL SUMMARY", "SUMMARY", "ABOUT", "ABOUT ME"],
    "EXPERTISE": ["EXPERTISE", "CORE COMPETENCIES", "SKILLS", "CORE SKILLS", "KEY SKILLS", "AREAS OF EXPERTISE"],
    "ACHIEVEMENTS": ["ACHIEVEMENTS", "KEY ACHIEVEMENTS", "SELECTED ACHIEVEMENTS", "HIGHLIGHTS", "CAREER HIGHLIGHTS"],
    "EXPERIENCE": ["EXPERIENCE", "WORK EXPERIENCE", "RECENT WORK EXPERIENCE", "PROFESSIONAL EXPERIENCE",
                   "EMPLOYMENT", "EMPLOYMENT HISTORY", "CAREER HISTORY"],
    "EDUCATION": ["EDUCATION", "EDUCATION & TRAINING", "EDUCATION AND TRAINING", "QUALIFICATIONS"],
    "PROJECTS": ["PROJECTS", "PROJECTS I LOVED TO WORK ON", "SELECTED PROJECTS", "SIDE PROJECTS"],
    "CERTIFICATIONS": ["CERTIFICATIONS", "CERTIFICATES", "LICENCES & CERTIFICATIONS", "LICENSES & CERTIFICATIONS"],
    "PUBLICATIONS": ["PUBLICATIONS", "TALKS", "PUBLICATIONS & TALKS"],
    "LANGUAGES": ["LANGUAGES"],
    "VOLUNTEERING": ["VOLUNTEERING", "VOLUNTEER WORK", "COMMUNITY"],
}
ALIAS_TO_KEY = {alias: key for key, aliases in SECTION_ALIASES.items() for alias in aliases}
BLOCK_SECTIONS = {"EXPERIENCE", "EDUCATION"}

_MONTH = r"(?:[A-Z][a-z]{2,8}\.?\s+\d{4})"
_DATE = r"(?:\d{1,2}/\d{4}|" + _MONTH + r"|\d{4})"
_END = r"(?:" + _DATE + r"|Present|present|Current|current|now|Now|Today|today|Ongoing|ongoing)"
_DASH = "(?:-|\u2013|\u2014|to)"  # hyphen, en dash, em dash (escaped so this file holds no dash characters)
DATE_LINE_RE = re.compile(
    r"^[*_]*\s*" + _DATE + r"\s*" + _DASH + r"\s*" + _END + r"\s*[*_]*$"
    r"|^[*_]*\s*" + _DATE + r"\s*[*_]*$"
)
SEPARATOR_RE = re.compile("^[-_*\u2013\u2014\\s]{3,}$")
HEADER_RE = re.compile(r"^(#{1,6})\s+(.*)$")
BULLET_RE = re.compile(r"^[*\-+]\s+(.*)$")
INLINE_RE = re.compile(
    r"(?P<esc>\\[-.*_\\#|\[\]()])"
    r"|(?P<bold>\*\*(?P<bold_t>.+?)\*\*)"
    r"|(?P<boldu>__(?P<boldu_t>.+?)__)"
    r"|(?P<link>\[(?P<link_t>[^\]]+)\]\((?P<link_u>[^)]+)\))"
    r"|(?P<ital>(?<!\*)\*(?P<ital_t>[^*]+?)\*(?!\*))"
    r"|(?P<italu>(?<![A-Za-z0-9])_(?P<italu_t>[^_]+?)_(?![A-Za-z0-9]))"
)


def clean_markdown(text):
    """Strip markdown to plain text (headers, bullets, bold, italics, links, escapes)."""
    if not text:
        return ""
    text = re.sub(r"^#+\s*", "", text)
    text = re.sub(r"^[*\-+]\s+", "", text)
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"__(.*?)__", r"\1", text)
    text = re.sub(r"(?<!\*)\*(?!\*)(.*?)\*", r"\1", text)
    text = re.sub(r"(?<![A-Za-z0-9])_(.*?)_(?![A-Za-z0-9])", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"\\([-.*_\\#|\[\]()])", r"\1", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def parse_inline(text):
    """Convert inline markdown into runs: [{"text", "bold", "italic", "href"}]."""
    runs = []

    def add(t, bold=False, italic=False, href=None):
        if not t:
            return
        if runs and runs[-1]["bold"] == bold and runs[-1]["italic"] == italic and runs[-1]["href"] == href:
            runs[-1]["text"] += t
        else:
            runs.append({"text": t, "bold": bold, "italic": italic, "href": href})

    def walk(s, bold=False, italic=False, href=None):
        pos = 0
        for m in INLINE_RE.finditer(s):
            add(s[pos:m.start()], bold, italic, href)
            if m.group("esc"):
                add(m.group("esc")[1], bold, italic, href)
            elif m.group("bold") or m.group("boldu"):
                walk(m.group("bold_t") or m.group("boldu_t"), True, italic, href)
            elif m.group("link"):
                walk(m.group("link_t"), bold, italic, m.group("link_u"))
            elif m.group("ital") or m.group("italu"):
                walk(m.group("ital_t") or m.group("italu_t"), bold, True, href)
            pos = m.end()
        add(s[pos:], bold, italic, href)

    walk(text or "")
    return runs


def runs_to_text(runs):
    return "".join(r["text"] for r in runs)


def split_frontmatter(content):
    """Return (meta_dict, body_text). Meta is {} if there is no frontmatter."""
    if not content.startswith("---"):
        return {}, content
    parts = content.split("\n", 1)
    if len(parts) < 2:
        return {}, content
    rest = parts[1]
    end = re.search(r"^---\s*$", rest, flags=re.M)
    if not end:
        return {}, content
    raw = rest[: end.start()]
    body = rest[end.end():]
    meta = {}
    try:
        import yaml  # type: ignore
        meta = yaml.safe_load(raw) or {}
    except Exception:
        for line in raw.splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip().strip('"').strip("'")
    return meta, body


def section_key_for(text):
    """Map a heading's plain text to a canonical section key, or None if it is not a section."""
    plain = clean_markdown(text).rstrip(":")
    plain = re.sub(r"\s*\[[^\]]*\]\s*$", "", plain).strip()  # drop a trailing [TAG]
    up = plain.upper()
    if up in ALIAS_TO_KEY:
        return ALIAS_TO_KEY[up]
    if " | " in plain:
        return None
    # An all-caps heading (as written) is a custom section, e.g. "# CERTIFICATIONS"
    if plain and re.search(r"[A-Z]", plain) and plain == up and len(plain.split()) <= 5:
        return re.sub(r"[^A-Z0-9]+", "_", up).strip("_")
    return None


def _new_section(key, title):
    return {"key": key, "title": title, "kind": None, "paragraphs": [], "items": [], "blocks": []}


def _new_block(heading):
    role, org = heading, ""
    if " | " in heading:
        role, org = [p.strip() for p in heading.split(" | ", 1)]
    return {"heading": heading, "role": role, "org": org, "date": "", "items": [], "paragraphs": []}


def parse_markdown_cv(filepath=None, content=None):
    if content is None:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    meta, body = split_frontmatter(content)
    lines = body.split("\n")

    state = {"name": "", "target_title": "", "current": None, "block": None, "para": []}
    sections = []

    def flush_para():
        if state["para"]:
            text = " ".join(state["para"]).strip()
            target = state["block"] if state["block"] is not None else state["current"]
            if text and target is not None:
                target["paragraphs"].append(text)
            state["para"] = []

    for raw in lines:
        line = raw.strip()
        if not line or SEPARATOR_RE.match(line):
            flush_para()
            continue

        hm = HEADER_RE.match(line)
        if hm:
            flush_para()
            level, text = len(hm.group(1)), hm.group(2).strip()
            key = section_key_for(text)
            if not state["name"] and level == 1 and key is None:
                state["name"] = clean_markdown(text)
                continue
            if key is not None:
                sec = _new_section(key, clean_markdown(text))
                sections.append(sec)
                state["current"], state["block"] = sec, None
                continue
            if state["current"] is not None:
                blk = _new_block(clean_markdown(text))
                state["current"]["blocks"].append(blk)
                state["block"] = blk
                continue

        if state["current"] is None:
            if state["name"] and not state["target_title"] and line.startswith("*"):
                state["target_title"] = clean_markdown(line)
            elif not state["name"]:
                state["name"] = clean_markdown(line)
            continue

        bm = BULLET_RE.match(line)
        if bm:
            flush_para()
            target = state["block"] if state["block"] is not None else state["current"]
            target["items"].append(bm.group(1).strip())
            continue

        cleaned = clean_markdown(line)
        blk = state["block"]
        if blk is not None and not blk["date"] and not blk["items"] and DATE_LINE_RE.match(cleaned):
            flush_para()
            blk["date"] = cleaned
            continue
        starts_block = " | " in cleaned and (
            (blk is None and state["current"]["key"] in BLOCK_SECTIONS)
            or (blk is not None and (blk["items"] or blk["date"]))
        )
        if starts_block:
            flush_para()
            nb = _new_block(cleaned)
            state["current"]["blocks"].append(nb)
            state["block"] = nb
            continue
        state["para"].append(line)
    flush_para()

    for sec in sections:
        if sec["blocks"]:
            sec["kind"] = "blocks"
        elif sec["items"]:
            sec["kind"] = "bullets"
        else:
            sec["kind"] = "paragraphs"

    return {
        "meta": meta,
        "name": state["name"] or meta.get("name", ""),
        "target_title": state["target_title"] or meta.get("target_title", ""),
        "sections": sections,
    }


def get_section(cv, key):
    for s in cv["sections"]:
        if s["key"] == key:
            return s
    return None


def summary(cv):
    """One line per section, used by --dry-run."""
    out = ["name: " + cv["name"], "target_title: " + cv["target_title"]]
    for s in cv["sections"]:
        if s["kind"] == "blocks":
            detail = ", ".join(b["role"][:30] + " (" + str(len(b["items"])) + ")" for b in s["blocks"])
            out.append(s["key"] + ": " + str(len(s["blocks"])) + " blocks: " + detail)
        elif s["kind"] == "bullets":
            out.append(s["key"] + ": " + str(len(s["items"])) + " bullets")
        else:
            out.append(s["key"] + ": " + str(len(s["paragraphs"])) + " paragraphs")
    return "\n".join(out)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python cv_parser.py <resume.md>")
        sys.exit(1)
    print(summary(parse_markdown_cv(sys.argv[1])))
