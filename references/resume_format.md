# resume.md Format

The grammar `cv_parser.py` accepts. Keep to it and both renderers produce the same document.

```markdown
---
company: "Harbourline Health"        # used in filenames and metadata
position: "Senior Product Manager"   # used in filenames
market: UK                           # picks page limit, location line, work-rights display
target_title: "Senior Product Manager, Data"   # printed under the name; defaults to the bold line below
# location_line: "Leeds, UK (relocating to Amsterdam, Q2 2027)"   # optional override
---

# Full Name
**Target Title**

---

# PROFILE

First short paragraph, first person, **bold** the top keywords.

Second paragraph.

# EXPERTISE

* **Area**: one sentence.

# ACHIEVEMENTS

* **Thing**: result with a number.

# WORK EXPERIENCE

## Role | Company
MM/YYYY - Present

Optional one-line context paragraph.

* **Topic**: what you did and the result.

## Role | Company
MM/YYYY - MM/YYYY

* ...

# EDUCATION

### Degree | Institution
MM/YYYY - MM/YYYY

# PROJECTS

* **Project**: one sentence.
```

## Rules
* The first `# ` heading that is not a section name is the candidate's name. The bold line after it is the target title.
* Section headings are `# ` lines whose text is a known alias (PROFILE, PROFESSIONAL SUMMARY, EXPERTISE, SKILLS, ACHIEVEMENTS, WORK EXPERIENCE, EXPERIENCE, EDUCATION, PROJECTS, CERTIFICATIONS, LANGUAGES, PUBLICATIONS, VOLUNTEERING) or any ALL CAPS text. Sections render in file order, so reorder freely.
* Blocks (a role, a degree) are `## ` or `### ` headings inside a section, written `Role | Company`. The next line is the date if it looks like one: `MM/YYYY - MM/YYYY`, `Mon YYYY - Present`, `YYYY`.
* Bullets start with `* ` or `- `. Blank lines separate paragraphs.
* Inline: `**bold**`, `*italic*`, `[text](url)`. Escape a literal asterisk or hyphen with a backslash.
* `---` separators are ignored.
* The contact line is not written in resume.md. It comes from `profile.yaml` (contact, market) so it stays consistent across applications.
* Check the parse with `python render_cv.py --resume <file> --dry-run`.
