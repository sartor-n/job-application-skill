# Tailoring Playbook

How to turn `master_cv.md` into `resume.md` for one job. The master is a floor, not a ceiling: archetype sections are the starting point, and the process reshapes them to the job description without inventing anything.

## Step 0: Select

Before drafting or substantively revising, run check_profile.py and check_readiness.py --application F and resolve blockers per [readiness.md](readiness.md). A completed onboarding flag or user urgency does not supply missing background. Inspect evidence quality as well as passing the scripts.

Filter the master by `[ALL]` plus the approved archetype tag from `roast.md`. Read preferences, relevant knowledge, the user's goals, and scoped learnings using [learning.md](learning.md). Apply confirmed corrections before old wording. Note the market's page limit and any explicit application-only preferences.

## Step 1: Keyword extraction

Take the relevant keywords and phrases in roast.md section 4 that have candidate evidence. Unsupported keywords remain gaps, not personalisation targets. There is no required count.

## Step 2: Linguistic mirroring, light touch

Use the JD's exact wording where the master says the same thing differently. If they say "stakeholder management", do not say "stakeholder orchestration".

Restraint rule: pick the top three to five JD phrases and use each once or twice, not in every section. Heavy repetition of the JD's pet words reads as mocking, not alignment. Master phrasing stays the default; JD wording is seasoning.

## Step 3: Content prioritisation

Every line must earn its place within the page limit.
* Promote: bullets that directly address JD requirements move up or get expanded.
* Compress: relevant but secondary bullets get shortened (merge two into one, cut qualifiers).
* Remove: bullets with no connection to this JD are dropped.
* Add: use relevant confirmed evidence from knowledge or the current conversation. Record and resolve its reuse scope through learning.md. Ask if unclear; explicit reuse/local instructions already settle scope. A fact retained only for this application stays in learning.json.

During every revision, classify new corrections and preferences, persist confirmed reusable entries, and reload applicable learning. Do not wait for final output. Reassess changed evidence/goals and refresh readiness only after reviewing those changes.

## Step 4: Section order

Default: Profile, Expertise, Achievements, Experience, Education, Projects (or the order in `profile.yaml`).
* Outcomes-heavy JD: Achievements right after Profile.
* Skills or tools-heavy JD: Expertise first.
* Experience-heavy JD: Work Experience first.
Put the strongest match in the top third of page one.

## Step 5: Profile rewrite

Rewrite the summary so the opening lines echo the JD's top three or four requirements. Open with the lead differentiator from `preferences.md`. Write in the first person, in the number of short paragraphs the style asks for, bolding the top keywords. Strictly grounded: storytelling is allowed, fabrication is not. Check every sentence against `## Experience Claims` and `## Fabrication Traps`.

## Step 6: Brevity pass

Shorten every sentence: cut trailing clauses that restate the point, stacked adjectives, qualifiers. One concept per bullet, at most two lines. Lead achievements with the thing, then a verified outcome. A specific qualitative result is valid; never manufacture numbers for a pattern. Extra pages buy room for relevant roles and evidence.

## Optional enhancements (light touch)

* Seniority tone must reflect actual authority. Do not turn a contribution into ownership or strategy definition to match a senior title.
* Company mission alignment: one or two subtle references if there is a real link. Public sources only, and confirm with the user before including.
* Preserve measurement units: users, customers and organisations are not interchangeable.

## Pre-submission checklist

- [ ] Header title closely matches the posted job title.
- [ ] Keywords used as candidate claims are supported by evidence; unsupported terms are omitted or explicitly identified as gaps, never implied expertise.
- [ ] Page count within the market limit (render and check `PAGES:`).
- [ ] Every claim can be defended in an interview.
- [ ] No fabrication-trap or banned phrase (`check_style.py` clean).
- [ ] No em or en dashes.
- [ ] Section order maximises first-impression relevance.
- [ ] Contact line correct for the market (location, work rights).
- [ ] The role's fit with the user's hopes, desired responsibilities and constraints was assessed.
- [ ] New feedback was classified, confirmed reusable learning saved and read back, one-off instructions kept local, and pending scope decisions reported.
- [ ] Profile and application readiness still match the current sources before rendering with --tailoring.
