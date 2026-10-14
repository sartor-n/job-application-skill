# Installation and technical reference

This file is for the AI agent (Claude Code or Codex) that installs and runs the skill. The user should not need to read it. Do the technical work yourself, ask before installing system software, and report back in plain, non-technical language.

## Install

1. **Pick the skills folder for the host you are running in.** The folder must be named `job-application`.
   * Claude Code: `~/.claude/skills/job-application/` (user-wide). Use a project `.claude/skills/job-application/` only if the user asks for a project install.
   * Codex: `~/.codex/skills/job-application/`, or the configured Codex skills directory.
2. **Get the files.** Clone the repository there:
   ```
   git clone https://github.com/sartor-n/job-application-skill.git ~/.claude/skills/job-application
   ```
   If git is unavailable, download the repository ZIP from GitHub and extract its contents into that folder. If the folder already exists, it is an update: run `git pull` inside it instead (see "Updating").
3. **Python 3.9 or newer.** Check with `python --version`, `python3 --version` or `py -3 --version`. If none is available, ask the user before installing it (python.org, the Microsoft Store, `winget install Python.Python.3.12`, or `brew install python` on macOS). Use the same interpreter for every step below and for later script calls.
4. **Python packages.** From the skill folder:
   ```
   python -m pip install -r requirements.txt
   ```
   PyYAML is required. On Windows the `pywin32` line lets the PDF be exported through Microsoft Word.
5. **A DOCX to PDF converter.** Run `python scripts/render_pdf.py`. Microsoft Word (Windows, via pywin32) or LibreOffice is needed for a PDF that matches the Word file. If neither is found, explain to the user that it is needed to create PDFs and ask before installing LibreOffice (free: libreoffice.org, `winget install TheDocumentFoundation.LibreOffice`, or `brew install --cask libreoffice`). Without a converter the Word files are still produced.
6. **Verify.** Run:
   ```
   python -m unittest discover -s tests -p 'test_*.py' -v
   ```
   Tests write only to temporary folders. Fix or report any failure before telling the user the install worked.
7. **Tell the user** in plain words: the skill is installed, start a new conversation so it is picked up, then say something like "help me apply for this job" with a link or pasted ad. The first use starts a one-off setup conversation (roughly 20 to 40 minutes). Do not start onboarding during the install unless the user asks.

## Updating

Run `git pull` in the skill folder, then repeat steps 4 and 6. User data lives outside the skill folder, so updates never touch it.

## Invoking

`/job-application` in Claude Code, `$job-application` in Codex, or plain-language requests when the host selects skills automatically. Operating instructions for the agent are in [SKILL.md](SKILL.md). Both hosts can share the same data directory; avoid editing the same application from two sessions at once.

## Where user data goes

`~/job-applications/` by default. `JOB_APPLICATIONS_DIR` overrides it, and a `job-applications/` folder in the current working directory is used if present.

```
job-applications/
  profile/
    profile.yaml       identity, contact, markets, style, render theme
    master_cv.md       complete CV content, tagged by archetype (read only for the assistant)
    preferences.md     goals, narrative rules, scoped learnings and fabrication traps
    archetypes.yaml    the versions of the person that jobs call for
    readiness.yaml     career coverage with actual source excerpts
    knowledge/         extra facts captured during tailoring
  applications/
    2026-03-02_company_role/
      job_description.md, roast.md, resume.md, cover_letter.md, metadata.json
      readiness.yaml, learning.json
      Your Name - Company - Role CV.pdf / .docx
```

## Commands

* A job URL or pasted job description: save it, resolve missing background, assess fit and record the user's decision before tailoring.
* `render <folder>` after edits to `resume.md`.
* Hand-edited DOCX: re-export the PDF from the document with `--from-docx`. The markdown is left alone.
* `prep <stage> <folder>`, stages `recruiter`, `hiring_manager`, `panel`, `final`, `reference`, `offer`, `debrief`.
* `profile edit preferences` to change a rule. `profile reonboard` starts over, with a backup.

## Readiness and learning

`python scripts/check_profile.py --data-dir D` checks profile structure and recorded evidence. `python scripts/check_readiness.py --data-dir D --application F` checks the job-specific assessment and proceed decision. The agent must also judge the meaning and adequacy of the evidence; these scripts cannot prove a claim is true. New tailoring uses `render_cv.py --tailoring` to repeat the gate before output. Formatting an existing document can use the plain render command.

Every tailoring or revision session loads prior learning and processes new corrections. Durable rules and concise fact or correction records go in `preferences.md`, longer evidence under `knowledge/`. Role and market preferences keep their scope. One-off and pending feedback stays in the application's `learning.json`. See [learning.md](references/learning.md).

Schema 1 profiles are upgraded by targeted discovery that preserves existing answers and the protected master. Do not use `--force` for migration. See [readiness.md](references/readiness.md).

## The example

`examples/` holds a fictional schema 1 profile and finished application, including rendered PDF and DOCX, to show layout and serve as a migration example. Never copy its career facts into a real profile.

## How the DOCX and PDF relate

The DOCX holds the layout and the PDF is exported from it, so they cannot drift apart. Editing the DOCX and re-exporting gives exactly what was seen in Word.

## Troubleshooting

* "No DOCX to PDF converter found": install LibreOffice, or on Windows `pip install pywin32` if Word is installed. The DOCX is written either way.
* Word export picks up an old version: close the document in Word first, since the export reads the saved file.
* `OVERFLOW` from the renderer: the CV exceeds the market's page limit. Do a brevity pass.
* Force an engine with `CV_PDF_ENGINE=word` or `CV_PDF_ENGINE=libreoffice`.
