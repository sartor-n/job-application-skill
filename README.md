# job-application skill

A Claude Code skill that runs your job applications: fit analysis, tailored CV, cover letter, PDF and DOCX output, interview prep. Your data stays in a folder you own; the skill folder holds only logic and templates.

## Install

1. Python 3.9 or newer on your PATH.
2. From this folder:
   ```
   pip install -r requirements.txt
   ```
3. A DOCX to PDF converter: Microsoft Word (on Windows the `pywin32` line in `requirements.txt` wires it up) or LibreOffice, which is free. Check what you have with `python scripts/render_pdf.py`.
4. Copy this folder to `~/.claude/skills/job-application/` (user-wide) or `<your-project>/.claude/skills/job-application/`.
5. Start Claude Code and type `/job-application`. Onboarding starts on its own the first time.

## Where your data goes

`~/job-applications/` by default. Set `JOB_APPLICATIONS_DIR` to put it elsewhere, or create a `job-applications/` folder inside a project to keep it there.

```
job-applications/
  profile/
    profile.yaml       identity, contact, markets, style, render theme
    master_cv.md       your complete CV content, tagged by archetype (read only for the assistant)
    preferences.md     narrative rules and fabrication traps
    archetypes.yaml    the versions of you that jobs call for
    knowledge/         extra facts captured during tailoring
  applications/
    2026-03-02_company_role/
      job_description.md, roast.md, resume.md, cover_letter.md, metadata.json
      Your Name - Company - Role CV.pdf / .docx
```

## Daily use

* Share a job URL or paste a job description: the skill creates the folder, writes a blunt fit analysis, and stops for your go-ahead before tailoring.
* `/job-application render <folder>` after you edit `resume.md`.
* Edited the DOCX in Word instead? Ask to re-export the PDF from the document. The PDF is exported from the DOCX, so your hand edits carry through and the markdown is left alone.
* `/job-application prep recruiter <folder>` (also `hiring_manager`, `panel`, `final`, `reference`, `offer`, `debrief`).
* `/job-application profile edit preferences` to change a rule. `profile reonboard` starts over (with a backup).

## Look at the example

`examples/` holds a fictional profile and one finished application, including rendered PDF and DOCX, so you can see the target shape before onboarding.

## How the two files relate

The DOCX holds the layout. The PDF is exported from it, so they cannot drift apart, and editing the DOCX and re-exporting gives you exactly what you saw in Word.

## Troubleshooting

* "No DOCX to PDF converter found": install LibreOffice, or on Windows `pip install pywin32` if you have Word. The DOCX is written either way, so you can export a PDF yourself.
* Word export picks up an old version: close the document in Word first, since the export reads the saved file.
* `OVERFLOW` from the renderer: the CV exceeds the market's page limit. Ask for a brevity pass.
* Force an engine with `CV_PDF_ENGINE=word` or `CV_PDF_ENGINE=libreoffice`.
