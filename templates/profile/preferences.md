# Narrative Preferences

Rules the assistant follows every time it writes about you. Filled during onboarding, edit any time. Each heading is explained in `references/preferences_schema.md`.

## Career Direction and Hopes
<!-- Separate desired future work from historical experience. Exploration is a valid direction. -->
{{DESIRED_POSITION_SCOPE_AND_SENIORITY}}
{{WHY_CHANGE_AND_LONG_TERM_HOPES}}
{{WORK_TO_DO_MORE_AND_LESS_OF}}
{{GROWTH_AND_LEARNING_PRIORITIES}}

## Working Preferences and Tradeoffs
<!-- Priorities, environment, acceptable tradeoffs and dealbreakers; optional private details can be declined. -->
{{PREFERRED_WORK_AND_ENVIRONMENT}}
{{PRIORITIES_TRADEOFFS_AND_DEALBREAKERS}}
{{PRACTICAL_CONSTRAINTS_OR_DECLINED_DETAILS}}

## Lead Differentiator
<!-- The one thing few candidates can truthfully claim that you can. Whether the profile summary should open with it. -->
{{LEAD_DIFFERENTIATOR}}

## Experience Claims
<!-- How many years you claim in total, since when in your current discipline, and which phrasing would be a fabrication. -->
* Total professional experience: {{YEARS}} years.
* In {{DISCIPLINE}} since {{YEAR}}. Never attach the total years to {{DISCIPLINE}} specifically.

## Title Rules
<!-- Roles whose title must never be upscaled, with the exact title to use. -->
* {{ROLE_AT_COMPANY}}: always "{{EXACT_TITLE}}".

## Naming Rules
<!-- Products or projects with a public name that must replace an internal one. Spelling rules. -->
* Use "{{PUBLIC_NAME}}", never "{{INTERNAL_NAME}}".

## Themes to Promote in Every Archetype
<!-- Two or three themes that must appear in every version, at varying strength. -->
* {{THEME_1}}
* {{THEME_2}}

## Framing Rules (say this, not that)
<!-- Topics with a preferred framing and a framing to avoid. -->
* {{TOPIC}}: say "{{PREFERRED_FRAMING}}", not "{{AVOIDED_FRAMING}}".

## Fabrication Traps
<!-- Claims that sound plausible for someone like you but are false. check_style.py flags these phrases. One per bullet, exact phrase in backticks. -->
* `{{FALSE_PHRASE}}`: false because {{REASON}}.

## Banned Phrases
<!-- Words or phrases you never want in your documents. Exact phrase in backticks. -->
* `{{PHRASE}}`

## Bullet Style
* Every experience bullet covers one concept, at most two lines, no filler.
* Lead achievements with the product or thing name, then a defensible outcome. Use numbers only when verified and meaningful.
* Enforce hardest on the current role.

## Summary Format
* {{N}} short paragraphs separated by blank lines, first person, no "I am a".
* Bold the top three to four job description keywords in the summary.

## Target Title Placement
* Use the target job title in the header and the cover letter only. Work history titles stay factual.

## Contact Rules
<!-- Derived from profile.yaml. Add anything market-specific here, e.g. when to show the work-rights line. -->
* {{CONTACT_RULE}}

## Location and Relocation Facts
<!-- Where you are, where you are going and when, and what must never be implied. -->
* {{LOCATION_FACT}}

## Early Career Handling
<!-- Which early roles to keep in long-format markets and which to drop in short-format markets. -->
* {{EARLY_CAREER_RULE}}

## Learning Scope

Record each new reusable preference, fact or correction with its intended scope. Ask only when scope is unclear. Application-only and pending feedback stays in the application's learning.json. Remembered facts are available evidence, not mandatory content for every CV.
