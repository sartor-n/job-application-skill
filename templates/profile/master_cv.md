---
read_only: true
purpose: Single source of truth for all CV content. Never modified by the assistant unless the user explicitly asks.
---

# Master CV: {{FULL_NAME}}

Every section is tagged. `[ALL]` content appears in every version. `[IC]`, `[LEAD]`, `[HYBRID]` (or your own tags from `archetypes.yaml`) mark content for one archetype. A section can carry several tags: `[IC, HYBRID]`.

The master is a floor, not a ceiling. Tailoring reshapes this content to a job description. It never invents claims that are not here or in `knowledge/`.

---

# PROFILE

### [IC] Profile
<!-- 2 or 3 short paragraphs, first person. Open with your lead differentiator (see preferences.md). -->
{{IC_PROFILE}}

### [LEAD] Profile
{{LEAD_PROFILE}}

### [HYBRID] Profile
{{HYBRID_PROFILE}}

---

# EXPERTISE

### [IC] Expertise
<!-- 5 bullets. "**Area**: one sentence of what you actually do in it." -->
* **{{AREA}}**: {{ONE_SENTENCE}}

### [LEAD] Expertise
* **{{AREA}}**: {{ONE_SENTENCE}}

### [HYBRID] Expertise
* **{{AREA}}**: {{ONE_SENTENCE}}

---

# ACHIEVEMENTS

### [IC] Achievements
<!-- 4 bullets. Lead with the product or thing, then the result with a number. -->
* **{{THING}}**: {{RESULT_WITH_NUMBER}}

### [LEAD] Achievements
* **{{THING}}**: {{RESULT_WITH_NUMBER}}

### [HYBRID] Achievements
* **{{THING}}**: {{RESULT_WITH_NUMBER}}

---

# WORK EXPERIENCE

## {{ROLE}} | {{COMPANY}} [ALL]
{{MM/YYYY}} - {{MM/YYYY or Present}}
<!-- Optional one-line context about the company or your scope. -->

### [ALL]
* **{{TOPIC}}**: {{WHAT_YOU_DID_AND_THE_RESULT}}

### [IC]
* **{{TOPIC}}**: {{WHAT_YOU_DID_AND_THE_RESULT}}

### [LEAD]
* **{{TOPIC}}**: {{WHAT_YOU_DID_AND_THE_RESULT}}

### [HYBRID]
* **{{TOPIC}}**: {{WHAT_YOU_DID_AND_THE_RESULT}}

## {{ROLE}} | {{COMPANY}} [ALL]
{{MM/YYYY}} - {{MM/YYYY}}

### [ALL]
* **{{TOPIC}}**: {{WHAT_YOU_DID_AND_THE_RESULT}}

---

# EDUCATION [ALL]

### {{DEGREE}} | {{INSTITUTION}}
{{MM/YYYY}} - {{MM/YYYY}}

---

# PROJECTS

### [IC, HYBRID] Projects
* **{{PROJECT}}**: {{ONE_SENTENCE}}

---

# CERTIFICATIONS [ALL]
<!-- Optional. Delete the section if empty. -->
* {{CERTIFICATION}}
