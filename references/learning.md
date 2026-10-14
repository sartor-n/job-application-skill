# Learning from feedback

This workflow is mandatory for every tailoring or substantive revision session, including corrections arriving after an earlier delivery. Read `preferences.md`, knowledge and `record_learning.py show` for the selected archetype, market and application before drafting. Apply prior learning, then process new feedback as it arrives.

## Interpret the feedback

Separate three things: the truth of a fact, permission to retain it, and when it should influence a future document. A real achievement can be reusable evidence without belonging in every CV. A fact used only here can still be recorded locally without promoting it into the career profile. Silence is not permission to make a local instruction global.

Classify each meaningful item:

| Scope | Meaning |
|---|---|
| global | An explicitly reusable rule, goal, fact or correction across applications |
| archetype | Applies to a named tag, such as LEAD; requires `scope_value` |
| market | Applies to a market code, such as UK; requires `scope_value` |
| application | Explicitly for this application; stays in its `learning.json` |
| pending | Reuse scope is unresolved; stays local until clarified |

Ask only when needed: "Should I remember this for future applications, or keep it specific to this one?" Offer a narrower role/market scope when the feedback suggests one. Explicit "always", "never", "from now on", "for leadership applications" or "just this application" supplies the answer. Reuse existing authorization; do not ask again because a script needs `confirmed: true`.

Facts and corrections explicitly stated by the user can inform this application while their future reuse remains pending. For an unclear name, number, date or contradictory claim, clarify the truth before using it. Do not preserve an unverified interpretation as a confirmed fact. Corrections to factual accuracy must replace the inaccurate claim immediately in the current work; clarify their future retention scope if the user's intent is not already clear.

## Record and read

Write one JSON input per learning using the host's file editor, then run:

```text
python "<skill_dir>/scripts/record_learning.py" record --entry "<entry.json>" --application "<folder>"
python "<skill_dir>/scripts/record_learning.py" show --application "<folder>" --archetype LEAD --market UK
```

Input fields:

```json
{
  "id": "mentoring-lead-2026-09-25",
  "date": "2026-09-25",
  "kind": "preference",
  "scope": "archetype",
  "scope_value": "LEAD",
  "statement": "Emphasise mentoring when applying for leadership roles.",
  "source": "For leadership applications, emphasise mentoring.",
  "confirmed": true,
  "details": "",
  "supersedes": []
}
```

Kinds: `preference`, `fact`, `correction`. `source` is the actual user wording or a precise user-confirmed statement with conversational context. Never fabricate it. `confirmed` records clear scope or the user's scope decision; pending entries use false. `details` can hold a longer evidence story. `supersedes` lists previous learning IDs being explicitly corrected or resolved, including a pending entry promoted after clarification. Use a new ID for a changed statement. The helper is idempotent for an identical repeated ID, refuses conflicting reuse of an ID, and retains superseded entries for history.

The helper stores a managed, readable JSON block under Confirmed Learnings in `preferences.md`. Global/role/market facts and corrections also create a linked file under `knowledge/`. Application and pending entries stay only in `<folder>/learning.json`. The `show` command returns applicable durable entries, application entries, and pending entries separately. It never treats an unmatched scope or pending entry as a global rule. Read the rest of preferences too; the managed block does not replace established narrative rules.

If feedback changes an existing prose preference or master claim, update the relevant preference to remove the contradiction once scope is clear. For an outdated protected master, add a confirmed correction with the exact superseded claim in its details; the correction takes precedence in future drafting. Edit the master only if explicitly requested. A one-off preference may override style/selection locally, but cannot make a false factual claim true.

## Save during the work and close the loop

Record confirmed reusable feedback when resolved, before the session ends. Do not wait for a final draft to save it. Re-read the saved records and relevant source files; refresh affected readiness and fingerprints. Verify an entry expected to be local did not enter profile preferences/knowledge. If a write fails, report the failure and keep the item visibly pending; never claim memory without a successful save.

At the end of each tailoring/revision turn, briefly state what was remembered and its scope, what stayed specific to this application, and any unanswered scope question. If there was no new reusable information, no new durable record is needed. On the next session, load and apply the same records so a corrected claim is not regenerated.
