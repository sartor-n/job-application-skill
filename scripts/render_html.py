"""Parsed CV (or a simple markdown document) -> HTML using templates/render/cv.html + cv.css."""
import html
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from cv_parser import parse_inline, HEADER_RE, BULLET_RE, SEPARATOR_RE, split_frontmatter  # noqa: E402
from render_common import contact_parts, display_name, display_title, PAGE_SIZES_MM  # noqa: E402
from paths import TEMPLATES_DIR  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def _read(name):
    with open(os.path.join(TEMPLATES_DIR, "render", name), "r", encoding="utf-8") as f:
        return f.read()


def runs_to_html(runs):
    out = []
    for r in runs:
        t = html.escape(r["text"])
        if r["bold"]:
            t = "<strong>" + t + "</strong>"
        if r["italic"]:
            t = "<em>" + t + "</em>"
        if r["href"]:
            t = '<a href="' + html.escape(r["href"], quote=True) + '">' + t + "</a>"
        out.append(t)
    return "".join(out)


def inline(text):
    return runs_to_html(parse_inline(text))


def css_vars(theme):
    m = theme["margins_mm"]
    size = theme["page_size"]
    return "\n".join([
        "  --page-size: " + ("A4" if size == "A4" else "Letter") + ";",
        "  --margin-top: " + str(m[0]) + "mm;",
        "  --margin-right: " + str(m[1]) + "mm;",
        "  --margin-bottom: " + str(m[2]) + "mm;",
        "  --margin-left: " + str(m[3]) + "mm;",
        "  --font-family: " + theme["font_family"] + ";",
        "  --body-pt: " + str(theme["body_pt"]) + "pt;",
        "  --line-spacing: " + str(theme["line_spacing"]) + ";",
        "  --para-after: " + str(theme["para_after_pt"]) + "pt;",
        "  --accent: " + theme["accent"] + ";",
        "  --heading-colour: " + theme["heading_colour"] + ";",
        "  --text-colour: " + theme["text_colour"] + ";",
    ])


def wrap(title, body, theme, body_class=""):
    page = _read("cv.html")
    return (page.replace("{{TITLE}}", html.escape(title))
                .replace("{{VARS}}", css_vars(theme))
                .replace("{{CSS}}", _read("cv.css"))
                .replace("{{BODY_CLASS}}", body_class)
                .replace("{{BODY}}", body))


def header_html(profile, cv, market):
    name = display_name(profile, cv)
    title = display_title(profile, cv)
    parts = []
    for text, href in contact_parts(profile, cv, market):
        t = html.escape(text)
        parts.append('<a href="' + html.escape(href, quote=True) + '">' + t + "</a>" if href else t)
    out = ['<div class="header">', "<h1>" + html.escape(name) + "</h1>"]
    if title:
        out.append('<div class="target-title">' + inline(title) + "</div>")
    if parts:
        out.append('<div class="contact">' + '<span class="sep">|</span>'.join(parts) + "</div>")
    out.append("</div>")
    return "\n".join(out)


def section_html(sec):
    out = ["<h2>" + html.escape(sec["title"]) + "</h2>"]
    for p in sec["paragraphs"]:
        out.append("<p>" + inline(p) + "</p>")
    if sec["items"]:
        out.append("<ul>" + "".join("<li>" + inline(i) + "</li>" for i in sec["items"]) + "</ul>")
    for b in sec["blocks"]:
        out.append('<div class="block">')
        head = '<span class="block-role">' + inline(b["role"]) + "</span>"
        if b["org"]:
            head += ' <span class="block-org">| ' + inline(b["org"]) + "</span>"
        date = '<span class="block-date">' + html.escape(b["date"]) + "</span>" if b["date"] else ""
        out.append('<div class="block-header"><span>' + head + "</span>" + date + "</div>")
        for p in b["paragraphs"]:
            out.append("<p>" + inline(p) + "</p>")
        if b["items"]:
            out.append("<ul>" + "".join("<li>" + inline(i) + "</li>" for i in b["items"]) + "</ul>")
        out.append("</div>")
    return "\n".join(out)


def render_cv_html(cv, profile, theme, market):
    body = [header_html(profile, cv, market)]
    for sec in cv["sections"]:
        body.append(section_html(sec))
    title = display_name(profile, cv) + " CV"
    return wrap(title, "\n".join(body), theme)


def markdown_doc_to_html_body(md_text):
    """Small markdown subset: headings, bullets, paragraphs, separators, inline runs."""
    _, body = split_frontmatter(md_text)
    out, in_list, para = [], False, []

    def flush():
        nonlocal para
        if para:
            out.append("<p>" + inline(" ".join(para)) + "</p>")
            para = []

    def close_list():
        nonlocal in_list
        if in_list:
            out.append("</ul>")
            in_list = False

    for raw in body.split("\n"):
        line = raw.strip()
        if not line:
            flush()
            close_list()
            continue
        if SEPARATOR_RE.match(line):
            flush()
            close_list()
            continue
        if line.startswith("<!--") or line.endswith("-->"):
            continue
        hm = HEADER_RE.match(line)
        if hm:
            flush()
            close_list()
            lvl = min(len(hm.group(1)), 3)
            out.append("<h" + str(lvl) + ">" + inline(hm.group(2)) + "</h" + str(lvl) + ">")
            continue
        bm = BULLET_RE.match(line)
        if bm:
            flush()
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append("<li>" + inline(bm.group(1)) + "</li>")
            continue
        para.append(line)
    flush()
    close_list()
    return "\n".join(out)


def render_doc_html(md_text, profile, cv, theme, market, title):
    body = header_html(profile, cv, market) + '\n<div class="content">\n' + markdown_doc_to_html_body(md_text) + "\n</div>"
    return wrap(title, body, theme, body_class="doc")


def strip_html_comments(text):
    return re.sub(r"<!--.*?-->", "", text, flags=re.S)
