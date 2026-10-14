# Career discovery and onboarding

Aim for sufficient understanding to write truthfully and help the person move toward the work they want. Use the groups as coverage, not a rigid questionnaire. Ask one substantial question or a small related group, listen, summarise, and follow what is missing. Do not dump every question below at once. Offer to pause and resume; save confirmed answers and open questions after each group.

## First-use orientation

Before intake, explain the journey in plain language. Example:

> First, we'll build a picture of your career, strengths and what you want next. You can then paste a job description or share its link. I'll give you a candid fit assessment, including whether the role suits your goals. If you decide to proceed, we'll tailor the CV and cover letter, review them together and produce the documents. Along the way, I'll remember the corrections and preferences you want reused. I need enough background before tailoring; we'll fill important gaps rather than guess.

Explain that discovery may take roughly 20 to 40 minutes with an existing CV, longer from scratch, and can span several sessions. A pasted JD can be saved at any point.

Recommend voice input with visual language:

> 🎙️ I recommend voice input for the career questions. If your chat has a microphone or voice button, use it to tell me the story naturally. Picture us talking through your career over coffee: take detours and don't worry about polished wording. I'll organise it and check unclear names, dates and numbers. Typing works too.

Do not claim a particular app has a control or give an unverified location or shortcut. In a terminal or a host without voice, suggest optional device dictation if available. Recommend voice again at the first substantial storytelling group if helpful, not on every question. Record `onboarding.process_explained: true` after explaining; resume rather than repeating the welcome on every turn.

## G1. Storage and existing material

Confirm the default `~/job-applications/` or use the path already accepted. Mention `JOB_APPLICATIONS_DIR` only if another location is useful. Run `init_profile.py` only for a new profile. Never run `--force` simply to resume or upgrade.

Invite an existing CV, career notes or portfolio when available. Read it to avoid re-asking known facts, but distinguish document claims from clarified ownership and current wishes. Confirm ambiguous names, dates, numbers and URLs before treating them as verified. Never infer career claims from an employer, title or sample profile.

## G2. Direction, hopes and expected position

Start with: "Picture a role you would be happy to be in two years from now. What are you doing more of, and what have you stopped doing?"

Explore desired titles and seniority, actual scope, IC versus management or a mix, domain, company type/stage, why change now, long-term hopes and skills to develop. Separate "I have done this" from "I want to do this". Ask what attracts them to a specific role if a JD is already present.

Capture priorities, acceptable tradeoffs and dealbreakers. "Still exploring" is a valid answer when accompanied by a useful direction or options to evaluate. Write confirmed goals and wishes to `preferences.md` under Career Direction and Hopes. Do not make a target title imply a historical title.

## G3. Career story, experience and evidence

Start with: "Walk me through how you got to where you are today. Which moves mattered most, and why?"

For relevant roles or projects establish title, organisation, dates, remit, actual authority, collaborators, decisions, challenges, actions and outcomes. Ask deeper about the most relevant recent work; summarise less relevant history. For someone early in their career, projects, study, volunteering or internships can provide evidence. Do not require paid employment.

Build a small, useful bank of stories. Probe: "What was the problem? What did you personally decide or deliver? Who else was involved? What changed? How do you know? What was difficult, and what did you learn?" Confirm ownership versus contribution and team versus personal results.

Numbers are welcome when accurate and meaningful, never compulsory. Use a specific qualitative outcome when metrics are unavailable. Record uncertainty rather than inventing a date, percentage or scale. If a claim seems inflated, ask: "What would you say if they asked you to prove that?"

With a CV import, use `import_cv.py`, review extracted content section by section and ask only about missing context or evidence. The import alone cannot unlock tailoring. For a new master, organise confirmed material into profile, expertise, achievements, experience, education and relevant projects. Use `read_only: true` frontmatter. Once established, do not replace or rewrite the master without an explicit user request; store additions/corrections in `knowledge/` and index them in preferences.

## G4. Strengths and preferred working life

Ask: "What do colleagues reliably come to you for? Tell me about a time that strength made a difference." Seek evidence, not a list of adjectives. Explore work that energises or drains them, their best environment, autonomy, collaboration, leadership, pace, values and what they want to avoid repeating.

Ask about practical constraints relevant to their search: locations, remote/hybrid preference, relocation, travel, timing and work authorisation. Compensation priorities may be useful; exact figures are optional. Respect declined/private information and record that boundary. Do not block drafting for an irrelevant undisclosed phone number, salary or personal detail.

Write preferences to Working Preferences and Tradeoffs. Store supporting career stories in master/knowledge. Mark the distinction between ability and desire: being good at something does not mean wanting a job centred on it.

## G5. Positioning and narrative

Reflect back the strongest evidenced themes and propose one or more useful versions of the candidate. IC, LEAD and HYBRID are optional starters, not required identities or a quota. Confirm the useful positioning before populating `archetypes.yaml`; tag evidence only where supported.

Use [preferences_schema.md](preferences_schema.md) to capture differentiator, accurate experience claims, exact titles and public names, preferred framing, false-but-plausible claims, banned phrases and tone. Ask only the unanswered questions. Keep historical facts and aspirations distinct. Explain that durable preferences can apply globally, to an archetype/market or to one application, and apply [learning.md](learning.md) whenever the scope is unclear.

## G6. Identity, contact and markets

Collect remaining administrative fields after understanding the career: printed name/headline, email, optional LinkedIn/portfolio, optional phone (default unprinted), location and any requested work-rights line. Confirm names, links and numbers in context without asking for the same confirmation twice. Do not collect a phone number if it has no purpose.

Configure markets, English variant, location/work-rights display and page limits. Offer two pages as a starting preference, not a universal hiring rule; use the user's needs and career stage. Record relocation truthfully and avoid implying current residence elsewhere. Decide what early history can be compressed without changing facts.

## G7. Style and rendering

Offer the existing typography, page size, filenames and section order as defaults. Ask about summary length, first-person voice, emphasis and cover-letter marker where it matters. No em/en dashes is a style default, not evidence that punctuation identifies machine writing. A plain check mark avoids possible font-embedding issues; do not claim every emoji creates a particular file size. Save changes to `profile.yaml` and corresponding preferences.

## G8. Readiness and baseline

Summarise career direction, evidence, strengths, priorities and claim boundaries in a short reflection; resolve substantive corrections. Populate `readiness.yaml` with coverage and actual source excerpts according to [readiness.md](readiness.md). Keep unanswered material questions visible. Do not mark an area ready just because a question was asked.

Run `check_profile.py` and resolve blocking gaps. A qualitative evidence story is valid; a blank section, title alone or arbitrary "complete" flag is not. Only after the career-background gate passes may you write a baseline from the approved primary archetype. Lint it and render with the existing renderer (no application gate is needed for a baseline). A missing PDF converter is an output issue, not missing career background; report it accurately.

Set `onboarding_complete: true` after substantive discovery is complete. Record `onboarding.last_completed_group` and open questions so returning sessions ask only what remains. Explain how to start an application: share a JD or job URL. If one is already saved, continue its role-specific discovery and fit assessment.

## Resuming and migration

For schema 1, preserve answered identity/storage/market questions and all source files. Explain the process if it was never explained, then ask only for missing direction, wishes, strengths evidence, ownership/outcomes, constraints and learning scope. Add the new readiness record without resetting data. Update `schema_version: 2` after mapping and reviewing existing material; this alone never grants readiness. See [readiness.md](readiness.md).
