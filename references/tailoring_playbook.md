# Tailoring Playbook

How to turn `master_cv.md` into `resume.md` for one job. The master is a floor, not a ceiling: archetype sections are the starting point, and the process reshapes them to the job description without inventing anything.

## Step 0: Select

Filter the master by `[ALL]` plus the approved archetype tag from `roast.md`. Read `preferences.md` and any files in `knowledge/`. Note the market's page limit from `profile.yaml`.

## Step 1: Keyword extraction

Take the 10 to 15 keywords and phrases already listed in `roast.md` section 4 (job title terms, required skills, tools, methods, metrics). These are the personalisation targets.

## Step 2: Linguistic mirroring, light touch

Use the JD's exact wording where the master says the same thing differently. If they say "stakeholder management", do not say "stakeholder orchestration".

Restraint rule: pick the top three to five JD phrases and use each once or twice, not in every section. Heavy repetition of the JD's pet words reads as mocking, not alignment. Master phrasing stays the default; JD wording is seasoning.

## Step 3: Content prioritisation

Every line must earn its place within the page limit.
* Promote: bullets that directly address JD requirements move up or get expanded.
* Compress: relevant but secondary bullets get shortened (merge two into one, cut qualifiers).
* Remove: bullets with no connection to this JD are dropped.
* Add: if the JD asks for something that is in `knowledge/` or came up in conversation but is not in the master, add it. Offer to save new facts to `knowledge/` for reuse. Ask first.

## Step 4: Section order

Default: Profile, Expertise, Achievements, Experience, Education, Projects (or the order in `profile.yaml`).
* Outcomes-heavy JD: Achievements right after Profile.
* Skills or tools-heavy JD: Expertise first.
* Experience-heavy JD: Work Experience first.
Put the strongest match in the top third of page one.

## Step 5: Profile rewrite

Rewrite the summary so the opening lines echo the JD's top three or four requirements. Open with the lead differentiator from `preferences.md`. Write in the first person, in the number of short paragraphs the style asks for, bolding the top keywords. Strictly grounded: storytelling is allowed, fabrication is not. Check every sentence against `## Experience Claims` and `## Fabrication Traps`.

## Step 6: Brevity pass

Recruiters skim. Shorten every sentence: cut trailing clauses that restate the point, stacked adjectives, qualifiers. One concept per bullet, at most two lines. Lead achievements with the thing, then the number. Extra pages buy room for more roles, never more words per bullet.

## Optional enhancements (light touch)

* Seniority tone: "Defined the strategy" for director-level, "Owned and executed" for senior IC. Wording shifts, substance does not.
* Company mission alignment: one or two subtle references if there is a real link. Public sources only, and confirm with the user before including.
* Scale calibration: B2C roles, frame numbers as users; B2B roles, as customers or organisations.

## Pre-submission checklist

- [ ] Header title closely matches the posted job title.
- [ ] Every extracted keyword appears at least once; the top three to five appear at most twice.
- [ ] Page count within the market limit (render and check `PAGES:`).
- [ ] Every claim can be defended in an interview.
- [ ] No fabrication-trap or banned phrase (`check_style.py` clean).
- [ ] No em or en dashes.
- [ ] Section order maximises first-impression relevance.
- [ ] Contact line correct for the market (location, work rights).
