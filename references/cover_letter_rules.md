# Cover Letter Rules

The cover letter is a requirement-to-evidence map, not a letter.

1. **Structure**: a straight list of the JD's requirements, each mapped to evidence. No salutation, no introduction, no closing paragraph.
2. **First person**: "I own the pricing roadmap", never "Sam owns" or "Owns". The same rule applies to the CV summary.
3. **One sentence per requirement, maximum.** Two to three lines is fine if the sentence earns it.
4. **Evidence, not claims**: name the product, company, number or concrete situation that proves the requirement. "Owns the analytics roadmap at Larkspur, prioritised against demand from four squads" beats "manages roadmaps".
5. **Thin evidence**: where the proof is weak, at least tie the point to the target company's own context rather than padding.
6. **Marker**: each requirement is followed by the marker from `profile.yaml style.checkmark` (default a plain check mark; empty string means none). Keep it a plain text glyph, not a colour emoji, which would inflate the PDF past most portals' upload limits.
7. **Order**: follow the JD's own order of importance, must-haves first.
8. **Format**:
   ```
   * **Requirement in the JD's words**: ✅ One sentence of evidence.
   ```
9. **Style**: no em or en dashes, short sentences, English variant from the market.
10. **Render**: `render_cv.py --cover-letter` produces the PDF and DOCX with the same header as the CV. The HTML comment block at the top of the template is stripped from renders.
