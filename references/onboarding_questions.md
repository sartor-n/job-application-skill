# Onboarding Question Script

Run this when `profile.yaml` is missing or has `onboarding_complete: false`. Ask one group at a time. Write the files after each group, so a dropped session loses little. Offer defaults and accept short answers. Expect voice-to-text noise: confirm names, URLs and numbers back to the user before writing them.

Tone: a careful colleague setting up a shared system, not a form. Explain in one line why each group matters.

## G1. Storage

1. "Your CV data will live outside the skill folder so the skill can be updated freely. Default location is `~/job-applications/`. Keep the default, or give me a path?" Also mention the `JOB_APPLICATIONS_DIR` environment variable for people who want the data inside a notes repo.
2. Run `init_profile.py [--data-dir D]`. Report the paths it printed.

## G2. Identity and contact

Writes `profile.yaml: identity, contact`.

1. Full name as it should appear on the CV.
2. Default headline under the name (their current or target title), e.g. "Senior Product Manager".
3. Email.
4. LinkedIn URL. Portfolio or GitHub URL if they want it printed.
5. Phone number, and whether it should be printed. Default: not printed. Explain that recruiters get it from the application form.
6. A work-rights line, if useful in their target markets: "Right to work in the UK", "EU citizen", "Dual citizen". Empty is fine.
7. Default location line, e.g. "Leeds, UK" or "Lisbon, Portugal (relocating to Berlin, March 2027)".

## G3. Markets and relocation

Writes `profile.yaml: markets[]` and `preferences.md ## Location and Relocation Facts`, `## Early Career Handling`.

1. "Which job markets will you apply in?" Take a list (countries or regions). Ask for a short code for each (UK, NL, US, AU).
2. Per market: page limit (offer the norm: 2 pages in most of Europe and the US, 3 accepted in Australia), English variant (british or american), a location line override if it differs, whether to print the work-rights line.
3. Relocation facts: where they are now, where they are going and when, and what must never be implied (e.g. "never imply I am already in the country").
4. Early career: which early roles are kept only in long-format markets and dropped in short-format ones.

## G4. Archetypes

Writes `archetypes.yaml`.

1. Show the three starters (IC, LEAD, HYBRID) in two lines each. "Which of these versions of you do jobs call for? Rename them, drop one, or add one." Aim for two to four.
2. Per archetype: tag (UPPER_CASE), name, two or three target titles, the JD signals that indicate it, what to emphasise, what to drop from the CV.

## G5. Master CV

Writes `master_cv.md`. This is the longest group. Offer two routes.

**Route A, import**: "Do you have a current CV file (.docx, .pdf, .md)?" Run `import_cv.py <file>`, then restructure the text into the master template sections. Show the user each section as you build it and ask for the missing numbers. Tag content by archetype; ask when unsure.

**Route B, interview**: build each section by asking:
1. Profile: for each archetype, two or three short first-person paragraphs. Open with the lead differentiator (ask G6 question 1 early if needed).
2. Expertise: five areas per archetype, each with one sentence of what they actually do.
3. Achievements: four per archetype. "What is the thing, and what is the number?"
4. Experience: for each role, `Role | Company`, dates as `MM/YYYY - MM/YYYY`, then bullets. Push for one concept per bullet, with a number. Tag bullets that only matter for one archetype.
5. Education, projects, certifications.

Always: every bullet must be something they can defend in an interview. Ask "what would you say if they asked you to prove that?" when a claim sounds inflated. Write the file with `read_only: true` in the frontmatter and explain the rule: the assistant never edits it without being asked.

## G6. Narrative preferences

Writes `preferences.md`. One question per heading; see `preferences_schema.md` for what good answers look like.

1. Lead differentiator: "What is the one thing few candidates can truthfully claim that you can? Should the summary open with it?"
2. Experience claims: "How many years of professional experience do you claim in total? Since when in your current discipline? Which phrasing would be a fabrication?"
3. Title rules: "Any role whose title must never be upscaled? What exact title should we use?"
4. Naming rules: "Any products or projects with a public name that must replace an internal one? Any spelling rules?"
5. Themes: "Two or three themes that must appear in every version of your CV, at varying strength."
6. Framing rules: "Topics where you want a specific framing and a framing to avoid?" Collect as pairs.
7. Fabrication traps: "Claims that sound plausible for someone like you but are false." Exact phrases go in backticks so the linter can catch them.
8. Banned phrases: words they never want to see.
9. Bullet style and summary format: offer the defaults and let them edit.

## G7. Style and rendering

Writes `profile.yaml: style, render`.

1. English variant default (british or american).
2. Dash rule: default forbids em and en dashes. Explain why in one line (they read as machine-written).
3. Summary: number of paragraphs (default 3), bold keywords (default yes).
4. Cover letter marker (default a plain check mark, can be empty). If they ask for a colour emoji, say that one emoji makes Word embed the whole emoji font and pushes the PDF past 3 MB, over many portals' upload caps.
5. Default section order.
6. Filename pattern (default `{name} - {company} - {position} {doc}`).
7. Theme: accent colour, font, A4 or Letter. Offer to keep the defaults.

## G8. Confirm

1. Summarise what was captured in ten lines.
2. Run `check_profile.py`. Fix every ERROR; report WARNs.
3. Build a baseline: create `applications/baseline_<PRIMARY_TAG>/resume.md` from the master's primary archetype, render it with `render_cv.py`, and show the paths. This is the "gold" CV before any tailoring.
4. Set `onboarding_complete: true` in `profile.yaml`.
5. Tell the user how to start their first application: share a job URL or paste a JD.

## Re-running

* `profile edit <group>`: re-ask only that group and rewrite only its file or keys.
* `profile import <file>`: re-run G5 from a file. Ask before replacing `master_cv.md`; back it up.
* `profile reonboard`: `init_profile.py --force` (backs up first), then all groups.
* Schema migration: if `schema_version` in `profile.yaml` is lower than the skill's, ask only the groups the changelog lists.
