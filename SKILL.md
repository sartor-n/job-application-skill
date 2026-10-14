---
name: job-application
description: Build an evidence-backed career profile, assess job fit, tailor CVs and cover letters, render PDF and DOCX, and prepare interviews. Use for career-profile setup, job applications, CV tailoring or critique, cover letters, interview prep, and offer review. Requires sufficient career background before tailoring and learns scoped preferences from feedback. Works in Claude Code and Codex.
metadata:
  version: 1.1.0
  schema_version: 2
---

# Job Application

Understand the person before writing about them. Learn their career, contributions, strengths, aspirations, desired position and working preferences. Tailor only claims supported by their own evidence. Remember reusable feedback with the scope the user intended.

## Portable operation and data

This skill works in Claude Code and Codex. Use the host's available file, shell and browsing tools; no host-specific APIs, UI controls, or subagents are required. `<skill_dir>` is the directory containing this file. Commands use `python`; choose an available Python 3.9+ interpreter (`python3` or `py -3` where appropriate). Use the same interpreter for dependency checks and scripts. Dependencies are in `requirements.txt`. If PyYAML is missing, install it through the environment's normal approved dependency workflow; do not treat a partially parsed profile as complete.

User data is separate from the skill. Resolution: `JOB_APPLICATIONS_DIR`, then `./job-applications/` if present, then `~/job-applications/`. Keep an explicitly chosen data directory consistent across commands using `--data-dir` or `--profile-dir`.

For career/application work, first run `python "<skill_dir>/scripts/paths.py"`. Read the existing profile and progress before asking questions. A request to review, install or edit the skill itself does not start personal onboarding.

Profile files: `profile.yaml` (configuration and progress), `master_cv.md` (protected source), `preferences.md` (goals, preferences and confirmed learnings), `archetypes.yaml` (candidate positioning), `readiness.yaml` (coverage with source references), and `knowledge/` (career evidence). Each application has its own JD, fit analysis, readiness assessment, learning record and documents.

## First use and returning users

On first career use, explain the entire journey before asking intake questions. Read [onboarding_questions.md](references/onboarding_questions.md): career discovery, JD intake, candid fit analysis, decision to proceed, tailoring, review, documents and reusable learning. Recommend voice input using the visual invitation there. Typing remains equally valid; do not invent microphone locations or switch modes for the user.

If the profile is absent or incomplete, resume the missing discovery areas. An imported CV is evidence to explore, not proof that discovery is finished. `onboarding_complete` is a progress marker, never permission to bypass readiness. For schema 1 profiles, follow the targeted migration in [readiness.md](references/readiness.md); preserve existing answers and the master CV.

Route by intent:

- No arguments: resume discovery, or ask for the next job once ready.
- Job URL, JD text or JD file: save the intake and assess readiness, then fit.
- CV file: import/discovery, not a new job application unless the user says so.
- `profile edit <area>`, `profile import <file>`, `profile reonboard`: update only the requested area; back up before replacing the master. Reonboarding is an explicit reset, not a migration shortcut.
- `render <folder>`: format/export existing content. Discovery is not required just to re-export, but substantive rewriting follows the tailoring gates.
- `prep <stage> <folder>`: interview workflow below.
- `status`: report saved applications and progress without forcing onboarding.

## Non-negotiable readiness before tailoring

Before composing or substantively revising a CV, cover letter or baseline, read [readiness.md](references/readiness.md). Establish coverage of career history, experience and outcomes, evidenced strengths, career direction, preferences/constraints, and claim boundaries. Ask focused follow-ups for material gaps. Confirm unclear names, dates, numbers and ownership. Do not require a numerical result for every achievement or a fixed number of stories unrelated to the person's career stage.

**Refuse to tailor while material background is missing.** Name the missing information, explain why it affects accuracy, and continue discovery. Do not produce a speculative draft as a workaround. Example: "I don't have enough background to tailor this accurately yet. I know your responsibilities, but not your personal contribution, the outcomes, or what you want next. Let's fill those gaps first."

Use `check_profile.py` for the profile and `check_readiness.py --application "<folder>"` immediately before application drafting. A zero exit code checks recorded evidence and decisions; the agent must also judge whether those sources actually support the proposed claims. Never fill readiness fields simply to make a check pass. An unknown is not a confirmed lack of experience. A known gap or weak job fit can still lead to an honest application once the user understands it and chooses to proceed.

## Learning is part of every tailoring session

Read [learning.md](references/learning.md) before handling feedback. At the start, load preferences, knowledge and learnings applicable to the current role/market. During every drafting or revision session, classify corrections and new information as global, role/market-scoped, application-only or unresolved. Persist confirmed reusable information during the conversation, not just at the end.

When scope is ambiguous, ask whether it should be remembered for future applications or kept here; keep it local and pending until answered. Explicit "always", "never", "for UK roles" or "this application only" already establishes scope. Do not request the same confirmation again. Durable preferences and concise fact/correction records live in `preferences.md`; detailed evidence lives in `knowledge/`. Application-only and pending information live in that application's `learning.json` and must never silently become global.

Use `record_learning.py` to record and read scoped entries. A factual correction takes precedence over outdated evidence; do not reuse the false claim in another application. The master remains protected: update it only when the user explicitly asks. Remembering a fact does not require including it in every CV. Before handing off, reconcile new feedback, verify saved records, and report what was remembered, kept local or still pending. If nothing reusable emerged, say so briefly without creating filler records.

## Writing rules

- Every candidate claim must trace to the master, confirmed knowledge, or confirmed evidence captured for this application. A JD or fictional example is never candidate evidence.
- Apply current confirmed corrections before older master wording. Check Experience Claims, Title Rules, Naming Rules, Framing Rules and Fabrication Traps in preferences.
- First person in the CV summary and cover letter. Short sentences, no filler, market-appropriate English. No em or en dashes by default.
- Match JD language only where the evidence supports it. Never imply a tool, qualification or ownership level just to include a keyword.
- Use verified qualitative outcomes when numbers are unavailable. Do not manufacture precision or turn team results into personal ownership.
- Run `check_style.py` on every `resume.md` and `cover_letter.md` written and fix findings.

## Application workflow

**1. Intake and discovery.** Accept a JD even if discovery is incomplete. Run `new_application.py --company "X" --role "Y" --market CODE --url "U" --location "L"` to preserve it. Fill `job_description.md` with extracted requirements, company context from public sources, and the raw JD. Resolve only missing material background. Draft no application content yet.

**2. Fit assessment.** Read the career evidence, preferences, application learnings and [roast_rubric.md](references/roast_rubric.md). Assess both employer fit and whether the role serves the person's goals. Separate supported experience, transferable evidence, confirmed gaps and unknowns. Resolve material unknowns before a definitive recommendation; mark any interim assessment provisional. Write `roast.md` and the application `readiness.yaml`; update metadata with archetype, fit score and `status: roasted`.

**3. Decision.** Present the archetype, fit, strongest alignment, main gap, goals fit and recommendation. Wait for the user's decision. Record `tailoring_approved: true` only when they choose to proceed based on that assessment; existing explicit approval need not be requested again. If declined, save `status: declined` and stop drafting.

**4. Tailor.** Run:

```text
python "<skill_dir>/scripts/check_profile.py"
python "<skill_dir>/scripts/check_readiness.py" --application "<folder>"
```

Both must pass before writing. Apply [tailoring_playbook.md](references/tailoring_playbook.md) and [resume_format.md](references/resume_format.md). Process feedback through the learning workflow, update evidence/readiness where relevant, and rerun the gate after material changes. Then:

```text
python "<skill_dir>/scripts/check_style.py" "<folder>/resume.md"
python "<skill_dir>/scripts/render_cv.py" --resume "<folder>/resume.md" --tailoring
```

Exit 2 means page overflow: shorten and render again. Exit 3 means readiness blocked: resolve the reported gaps before continuing. `--tailoring` validates the application gate before creating output; it is mandatory for new or substantively revised applications.

**5. Cover letter and review.** Follow [cover_letter_rules.md](references/cover_letter_rules.md), lint, and render with `--tailoring --cover-letter`. Review user corrections, persist their intended scope and rerun affected checks. Set `status: drafted` only once required outputs succeed. Record `submitted` only when the user says they applied.

## Re-rendering and interview prep

Rendering unchanged or user-edited source material does not perform tailoring. Use `render_cv.py --resume "<folder>/resume.md" --cover-letter` for formatting only. If the user hand-edited the DOCX, use `--from-docx --cover-letter`; explain that the Markdown may be stale and rebuilding from it would discard those edits. Never silently rebuild over hand edits. `--dry-run` inspects the parser. `--html-pdf` produces a PDF whose layout may differ from the DOCX; disclose that fallback.

For `prep <stage> <folder>`, read [interview_prep_method.md](references/interview_prep_method.md). Stages: recruiter, hiring_manager, panel, final, reference, offer, debrief. Use the matching template and the existing application evidence, goals, preferences and earlier debriefs. Ask about missing evidence relevant to that stage. Apply the same learning rules to new career facts and corrections. Named-interviewer research requires the user's go-ahead and public sources only. Append the stage to metadata.

## Reporting and helpers

When documents were produced, link their absolute paths alongside the roast and Markdown sources, report actual page count/limit and PDF engine, style result, and any failed outputs. Explain that DOCX is editable and `--from-docx` picks up hand edits. Do not invent output paths, page counts or successful renders for discovery/blocked turns. Always close a tailoring/revision turn with the learning outcome.

| Script | Use |
|---|---|
| `paths.py` | Resolve data directory and profile status |
| `init_profile.py [--data-dir D]` | Create a new profile; refuse accidental replacement |
| `check_profile.py [--profile-dir P]` | Validate structure and substantive background coverage |
| `check_readiness.py [--application F] [--fingerprints]` | Validate profile/application readiness or print current source fingerprints |
| `record_learning.py record --entry FILE --application F` | Save confirmed scoped learning or local pending feedback |
| `record_learning.py show --application F --archetype TAG --market CODE` | Read matching durable and local learnings, with pending items separate |
| `import_cv.py FILE` | Extract a source CV for review |
| `new_application.py --company X --role Y` | Scaffold an intake, including readiness and local learning records |
| `check_style.py FILE ...` | Lint generated documents |
| `render_cv.py --resume FILE [--tailoring] [--cover-letter]` | Generate DOCX/PDF; tailoring mode enforces readiness |
| `render_pdf.py` | Report available PDF converters |

Helpers needing profile data support `--data-dir` or `--profile-dir` as shown in `--help`. DOCX/PDF generation uses the existing Python dependencies and Word/LibreOffice support. Report `pdf_error` and `pdf_help` honestly if conversion is unavailable. [render_config.md](references/render_config.md) documents layout settings; [preferences_schema.md](references/preferences_schema.md) documents narrative and goal preferences. The bundled fictional example is illustrative, never the user's background.
