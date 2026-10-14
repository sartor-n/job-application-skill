# Readiness before writing

Two decisions are required: is the person's background sufficiently understood, and is there enough information to tailor for this particular job? Readiness is not the same as job fit. Confirmed gaps may remain; material unknowns need questions.

## Profile coverage

Maintain `profile/readiness.yaml` using `templates/profile/readiness.yaml`. For each area record `status: ready` only after understanding it, a concise `summary`, and one or more `evidence` references `{path, quote}`. Paths are relative to `profile/` and point into `master_cv.md`, `preferences.md` or `knowledge/*.md`. Quotes must be actual excerpts; never invent them or use fictional examples. Multiple areas can reference a good source without duplicating the story.

| Area | What sufficient coverage means |
|---|---|
| career_history | Relevant progression, roles/projects and dates, with context. Early-career projects count. |
| experience_and_outcomes | Personal contributions, authority, collaboration, scope and defensible outcomes for the claims likely to be used. Qualitative evidence counts. |
| strengths | Strengths grounded in examples, including transferable skills where appropriate. |
| career_direction | Expected positions/scope, hopes, motivation for change and learning/growth direction. Exploration can be an explicit goal. |
| preferences_and_constraints | Desired work and environment, priorities, tradeoffs, dealbreakers and relevant practical limits. Optional/private answers may be declined. |
| claim_boundaries | Accurate titles, ownership and experience claims; uncertainties and what must not be implied. |

`blocking_questions` lists only unanswered questions that materially affect truthfulness or positioning. Missing irrelevant contact data, unshared salary or an absent numeric metric is not automatically a blocker. Do not invent quotas for years, stories, employers or figures.

Run `check_profile.py` before a baseline or application. It validates structure and coverage, including source excerpts. The script cannot decide whether an excerpt proves a claim; the agent must inspect it and ask follow-ups when needed. A user-facing "not enough background yet" response should identify the specific missing areas and ask the next useful question, not simply report a failed script.

## Application assessment

`new_application.py` creates `<application>/readiness.yaml` and `learning.json`. Fill readiness after extracting requirements and resolving material questions:

- `reviewed_at`: date of this assessment.
- `profile_fingerprint` and `job_fingerprint`: current values from `check_readiness.py --application F --fingerprints`. Refresh only after reviewing changes, not just to silence a stale check. The job fingerprint includes the JD, target identity, selected archetype/market and local learning record.
- `goals_fit`: `status` is `aligned`, `tradeoff` or `mismatch`, with a substantive `summary`. A mismatch may proceed only after the user sees it and chooses to apply.
- `requirements`: every extracted material JD requirement with its wording, `importance` (`must_have` or `nice_to_have`), `status`, `note`, and relevant `evidence` references.
- `blocking_questions`: outstanding material questions; must be empty before tailoring.

Requirement states:

- `supported`: concrete candidate evidence addresses it.
- `transferable`: real but indirect evidence; state the limit, never imply direct experience.
- `confirmed_gap`: the user confirmed a lack or mismatch; state it accurately. This is allowed through the gate after the fit decision.
- `unknown`: not yet established. Must-haves block tailoring. A genuinely nonmaterial nice-to-have may remain unknown with an explicit note that it will be omitted, not implied in the CV. Anything material belongs in blocking questions.

Evidence references for an application use `{path, quote}` relative to the profile. Use `{application_path, quote}` for actual user evidence retained only in `learning.json`. Do not reference the JD as proof of the candidate's capabilities. All claimed experience must have a source; a factual clarification may be used locally before the user chooses its reuse scope.

Present the roast before setting `metadata.json tailoring_approved: true`. This boolean records the user's informed decision, not the agent's recommendation. Run `check_readiness.py --application F` after that decision and immediately before composing/revising application text. Changes to evidence, goals, target, JD or local learnings invalidate the previous fingerprint and require a focused reassessment, not a new full interview. Reuse an existing proceed decision unless the new assessment materially changes the tradeoff the user approved.

`render_cv.py --tailoring` repeats this preflight before output. Ordinary render-only work and `--from-docx` do not infer new career claims and can preserve existing artifacts even when onboarding is incomplete. Do not use render-only mode as a way to present a newly tailored document without readiness.

## Schema 1 migration

Never rerun `init_profile.py --force` to upgrade. Preserve user data and the protected master. Add only the missing `readiness.yaml`, onboarding progress fields and goal/preference sections. Existing confirmed evidence can populate references; absent goals or unverified claims require targeted questions. An old completed flag does not certify the new coverage. Set schema 2 when the new structure is in place and reviewed, keeping onboarding incomplete if substantive gaps remain. Existing application documents remain usable; a new substantive rewrite gets its own assessment. Bundled schema 1 examples illustrate layout and can be used to test this migration, never copied as user facts.
