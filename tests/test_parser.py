import os
import sys

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))

from cv_parser import parse_markdown_cv, parse_inline, clean_markdown, get_section  # noqa: E402

EXAMPLE = os.path.join(HERE, "..", "examples", "applications",
                       "2026-03-02_harbourline_health_senior_pm_data", "resume.md")


def test_example_resume_structure():
    cv = parse_markdown_cv(EXAMPLE)
    assert cv["name"] == "Sam Okafor"
    assert cv["target_title"].startswith("Senior Product Manager")
    assert cv["meta"]["market"] == "UK"
    keys = [s["key"] for s in cv["sections"]]
    assert keys[:4] == ["PROFILE", "EXPERTISE", "ACHIEVEMENTS", "EXPERIENCE"]
    assert "EDUCATION" in keys
    prof = get_section(cv, "PROFILE")
    assert prof["kind"] == "paragraphs" and len(prof["paragraphs"]) == 3
    assert len(get_section(cv, "EXPERTISE")["items"]) == 5
    assert len(get_section(cv, "ACHIEVEMENTS")["items"]) == 4
    exp = get_section(cv, "EXPERIENCE")
    assert exp["kind"] == "blocks" and len(exp["blocks"]) == 3
    first = exp["blocks"][0]
    assert first["role"] == "Senior Product Manager" and first["org"] == "Larkspur Systems"
    assert first["date"] == "03/2022 - Present"
    assert len(first["items"]) >= 3
    edu = get_section(cv, "EDUCATION")
    assert len(edu["blocks"]) == 2 and edu["blocks"][0]["date"]


def test_custom_all_caps_section_and_date_forms():
    content = """# Jane Doe
**Engineer**

# CERTIFICATIONS
* AWS Solutions Architect

# WORK EXPERIENCE
## Engineer | Acme
Jan 2020 - Present
* Did things

### Analyst | Beta Corp
2018 - 2019
* Other things
"""
    cv = parse_markdown_cv(content=content)
    assert cv["name"] == "Jane Doe" and cv["target_title"] == "Engineer"
    cert = get_section(cv, "CERTIFICATIONS")
    assert cert["kind"] == "bullets" and cert["items"] == ["AWS Solutions Architect"]
    exp = get_section(cv, "EXPERIENCE")
    assert [b["date"] for b in exp["blocks"]] == ["Jan 2020 - Present", "2018 - 2019"]
    assert exp["blocks"][1]["org"] == "Beta Corp"


def test_inline_runs():
    runs = parse_inline("**Bold**: plain *it* [link](https://x.y) 40\\%")
    assert runs[0] == {"text": "Bold", "bold": True, "italic": False, "href": None}
    assert any(r["italic"] and r["text"] == "it" for r in runs)
    assert any(r["href"] == "https://x.y" and r["text"] == "link" for r in runs)
    assert clean_markdown("* **Bold**: text \\- [l](u)") == "Bold: text - l"
