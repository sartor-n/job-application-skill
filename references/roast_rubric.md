# Roast Rubric

The roast is a candid assessment before tailoring. Assess both the employer's requirements and whether this role serves the candidate's goals, hopes and preferred work. Be direct and evidence-based, without ridicule. Its job is to support an informed decision and identify an honest positioning.

## Inputs
Read job_description.md, master_cv.md, archetypes.yaml, preferences.md (including goals), relevant knowledge, profile readiness and applicable application learnings. Follow [readiness.md](readiness.md) before interpreting absent evidence as a gap.

## Unknown versus confirmed gap

Classify material requirements as supported, transferable, confirmed_gap or unknown. Ask about unknown material experience or preferences. A missing item in an imported CV is not proof the person lacks it. An interim roast with unknowns is provisional: show the questions and avoid a definitive score/recommendation until they are resolved. A nonmaterial nice-to-have can remain explicitly unknown and omitted from claims.

## Archetype choice
Match the JD signals in `archetypes.yaml`. State the primary tag and, if the role blends two, the secondary in one line. Pick one to tailor with.

## Fit score (out of 100)
When material evidence is sufficiently understood, score assessed requirements 0 to 10 for directness of evidence, weight must-haves double, and scale. This is a disclosed heuristic, not a hiring probability. Do not score unresolved unknowns as zero. State any excluded nonmaterial unknowns. Then adjust:
* Minus 10 to 20 for a confirmed must-have gap.
* Minus 5 to 10 for a location, work-rights or seniority mismatch that the CV cannot fix.
* Plus 5 if the lead differentiator is the core of the role.

Rough bands: 85 and above is a strong fit, 70 to 84 is a real fit with work to do, 55 to 69 is a stretch, below 55 is usually a no.

## Alignments
Three to six. Each one names the JD line, the evidence (product, company, number), and a score out of 10. Evidence must be quotable from the master or `knowledge/`.

Use fewer alignments if that is all the evidence supports. Quantitative or specific qualitative outcomes are valid, and confirmed application-local evidence can be cited from learning.json. Do not turn participation into ownership.

## Gaps and mitigations
Every gap gets an honest mitigation or the words "no mitigation". Common gap types: named tools or stacks, domain, scale, people management, location.

## Keywords to mirror
List JD terms that have evidence, without a quota. Mark transferable terms with their limits. Unsupported terms stay in gaps/unknowns and must not be inserted to meet a keyword checklist. The tailoring playbook consumes only supported wording.

## Fit with the candidate's goals

Report aligned, tradeoff or mismatch separately from the employer-fit score. Compare actual remit, seniority, IC/management balance, growth, environment and constraints against the person's stated preferences. Name what the role offers, what it would cost, and any unanswered employer-side questions. Do not invent company culture from marketing copy. A strong capability match can still be the wrong next move.

## Recommendation
* PROCEED: score 70 or above, no unmitigated must-have gap, and goals aligned.
* PROCEED WITH CAVEATS: 55 to 69, or a must-have gap with a credible mitigation. State the caveat in one line.
* DO NOT APPLY: below 55, a hard requirement mismatch, or a conflict with a stated dealbreaker.

For a goals tradeoff, use PROCEED WITH CAVEATS even if capability fit is high. Explain the judgment; scores do not override the person's priorities. The user may choose to apply despite a recommendation, but must understand the known gap or tradeoff and all claims remain truthful.

End with one paragraph: what the tailored CV will lead with and what the honest risk is.

## Gate
Present archetype, score/uncertainty, top alignment, top gap, goals fit and recommendation. Record the user's decision in metadata.tailoring_approved. Do not tailor before both readiness and the informed proceed decision; reuse an already-given decision unless material new facts change the assessment.
