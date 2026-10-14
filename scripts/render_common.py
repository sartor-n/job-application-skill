"""Theme, contact line and filename helpers shared by the HTML and DOCX renderers."""
import re

DEFAULT_THEME = {
    "page_size": "A4",
    "margins_mm": [16, 14, 16, 14],
    "font_family": "Segoe UI, Calibri, Arial, sans-serif",
    "body_pt": 10,
    "line_spacing": 1.25,
    "para_after_pt": 6,
    "accent": "#0284c7",
    "heading_colour": "#0369a1",
    "text_colour": "#1e293b",
    "filename_pattern": "{name} - {company} - {position} {doc}",
}

PAGE_SIZES_MM = {"A4": (210, 297), "LETTER": (215.9, 279.4)}


def theme_from_profile(profile):
    theme = dict(DEFAULT_THEME)
    if profile and isinstance(profile.get("render"), dict):
        for k, v in profile["render"].items():
            if v not in (None, ""):
                theme[k] = v
    theme["page_size"] = str(theme["page_size"]).upper()
    if theme["page_size"] not in PAGE_SIZES_MM:
        theme["page_size"] = "A4"
    m = theme["margins_mm"]
    if not (isinstance(m, (list, tuple)) and len(m) == 4):
        theme["margins_mm"] = DEFAULT_THEME["margins_mm"]
    return theme


def pick_market(profile, code=None):
    markets = (profile or {}).get("markets") or []
    if code:
        for m in markets:
            if str(m.get("code", "")).upper() == str(code).upper():
                return m
    return markets[0] if markets else {"code": "DEFAULT", "page_limit": None, "show_work_rights": True}


def contact_parts(profile, cv, market):
    """Ordered list of (text, href) for the contact line under the name."""
    contact = (profile or {}).get("contact") or {}
    meta = cv.get("meta") or {}
    parts = []
    if market.get("show_work_rights", True) and contact.get("work_rights_line"):
        parts.append((contact["work_rights_line"], None))
    location = meta.get("location_line") or market.get("location_line") or contact.get("location_line")
    if location:
        parts.append((location, None))
    if contact.get("email"):
        parts.append((contact["email"], "mailto:" + contact["email"]))
    if contact.get("linkedin"):
        url = contact["linkedin"]
        if not url.startswith("http"):
            url = "https://" + url.lstrip("/")
        parts.append((re.sub(r"^https?://(www\.)?", "", url).rstrip("/"), url))
    if contact.get("portfolio"):
        url = contact["portfolio"]
        if not url.startswith("http"):
            url = "https://" + url
        parts.append((re.sub(r"^https?://(www\.)?", "", url).rstrip("/"), url))
    if contact.get("show_phone") and contact.get("phone"):
        parts.append((str(contact["phone"]), None))
    return parts


def display_name(profile, cv):
    return cv.get("name") or ((profile or {}).get("identity") or {}).get("name") or "Candidate"


def display_title(profile, cv):
    return cv.get("target_title") or ((profile or {}).get("identity") or {}).get("headline") or ""


def sanitize_filename(text):
    text = re.sub(r'[\\/:*?"<>|]+', "-", text)
    text = re.sub(r"\s+", " ", text).strip(" .")
    return text[:180]


def build_filename(pattern, name, company, position, doc, ext):
    base = pattern.format(name=name or "CV", company=company or "Company", position=position or "Role", doc=doc)
    return sanitize_filename(base) + ext
