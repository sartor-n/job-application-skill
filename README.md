# job-application skill

A portable skill for **Claude Code and Codex**: career discovery, candid fit analysis, tailored CV and cover letter, PDF/DOCX output and interview prep. Version 1.1.0 adds evidence-based readiness and scoped learning. Your data stays in a folder you own; the skill folder holds only logic and templates. No app-specific APIs, hooks or UI controls are required.

## Install

1. Python 3.9 or newer on your PATH.
2. From this folder:
   ```
   pip install -r requirements.txt
   ```
3. A DOCX to PDF converter: Microsoft Word (on Windows the `pywin32` line in `requirements.txt` wires it up) or LibreOffice, which is free. Check what you have with `python scripts/render_pdf.py`.
4. Copy the same job-application folder to the host's skills directory:
   * Claude Code: `~/.claude/skills/job-application/` or a project `.claude/skills/job-application/`.
   * Codex: `~/.codex/skills/job-application/` (or the configured Codex skills directory).
5. Invoke `/job-application` in Claude Code or `$job-application` in Codex. Natural-language requests matching the skill also work when the host supports automatic selection.

Use the same Python interpreter for installation and commands (`python`, `python3` or `py -3` depending on the environment). PyYAML is required; a missing dependency now reports an error instead of silently discarding nested profile fields. Both hosts can share the same data directory. Avoid simultaneous edits to the same application/profile from two sessions.

## What the process looks like

Career story, strengths, hopes and desired work come first. An existing CV helps but does not replace discovery. The skill recommends voice input with a visual microphone cue when the host/device supports it; typing is always supported. It then accepts the JD, checks material background gaps, assesses both employer fit and personal goals, and waits for the decision to proceed before tailoring. Review, verified rendering and scoped learning complete each application.

The agent must refuse tailoring when important background is missing and ask focused follow-ups. No numerical achievement quota is required. A confirmed experience gap can still support an honest application; an unexplored gap needs clarification.

## Where your data goes

`~/job-applications/` by default. Set `JOB_APPLICATIONS_DIR` to put it elsewhere, or create a `job-applications/` folder inside a project to keep it there.

```
job-applications/
  profile/
    profile.yaml       identity, contact, markets, style, render theme
    master_cv.md       your complete CV content, tagged by archetype (read only for the assistant)
    preferences.md     goals, narrative rules, scoped learnings and fabrication traps
    archetypes.yaml    the versions of you that jobs call for
    readiness.yaml     career coverage with actual source excerpts
    knowledge/         extra facts captured during tailoring
  applications/
    2026-03-02_company_role/
      job_description.md, roast.md, resume.md, cover_letter.md, metadata.json
      readiness.yaml, learning.json
      Your Name - Company - Role CV.pdf / .docx
```

## Daily use

* Share a job URL or paste a job description: the skill saves it, resolves missing material background, assesses fit and records your decision before tailoring.
* `/job-application render <folder>` after you edit `resume.md`.
* Edited the DOCX in Word instead? Ask to re-export the PDF from the document. The PDF is exported from the DOCX, so your hand edits carry through and the markdown is left alone.
* `/job-application prep recruiter <folder>` (also `hiring_manager`, `panel`, `final`, `reference`, `offer`, `debrief`).
* `/job-application profile edit preferences` to change a rule. `profile reonboard` starts over (with a backup).

The examples above use Claude's slash command. In Codex use `$job-application` with the same arguments, or ask in ordinary language. Scripts use relative skill paths and the same data format in either host.

## Readiness and learning

`python scripts/check_profile.py --data-dir D` checks profile structure and recorded evidence. `python scripts/check_readiness.py --data-dir D --application F` checks the job-specific assessment and proceed decision. The agent must also evaluate the meaning and adequacy of the evidence; these scripts cannot prove that a claim is true. Newly tailored content uses `render_cv.py --tailoring` to repeat the gate before output. Formatting an existing document can still use the original render command.

Every tailoring/revision session loads prior learning and processes new corrections. Durable rules and concise fact/correction records are saved in preferences.md, with longer evidence under knowledge/. Role/market preferences retain their scope. One-off and pending feedback stays in the application's learning.json. The skill asks when scope is ambiguous, then reads back saved records. Retaining a fact does not force it into every CV. See [learning workflow](references/learning.md).

Schema 1 profiles are upgraded by targeted discovery, preserving existing answers and the protected master. Do not use --force for migration. See [readiness and migration](references/readiness.md). Previously rendered artifacts remain usable; new tailoring must satisfy the new checks.

## Look at the example

`examples/` holds a fictional schema 1 profile and finished application, including rendered PDF and DOCX, to show document layout and provide a legacy migration example. It does not claim to satisfy version 1.1 discovery. Never copy its career facts into a real user's profile.

## Verification

Run `python -m unittest discover -s tests -p 'test_workflow.py' -v` for readiness, scoped learning, migration preservation and portable CLI checks. Existing parser checks in test_parser.py also run with that suite. Only temporary fixture directories are written.

## How the two files relate

The DOCX holds the layout. The PDF is exported from it, so they cannot drift apart, and editing the DOCX and re-exporting gives you exactly what you saw in Word.

## Troubleshooting

* "No DOCX to PDF converter found": install LibreOffice, or on Windows `pip install pywin32` if you have Word. The DOCX is written either way, so you can export a PDF yourself.
* Word export picks up an old version: close the document in Word first, since the export reads the saved file.
* `OVERFLOW` from the renderer: the CV exceeds the market's page limit. Ask for a brevity pass.
* Force an engine with `CV_PDF_ENGINE=word` or `CV_PDF_ENGINE=libreoffice`.
