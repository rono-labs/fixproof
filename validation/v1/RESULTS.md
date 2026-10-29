# Dry-run results: fixproof

Date of run: scenario date 2026-11-20. Method: tabletop run of SKILL.md against `project/testdata/home-library/`. Experts were emulated with `find`, `grep`, `pdftotext` and by viewing the photos. Expected answers were read only after the six transcripts were written. Transcripts: `dryrun-A.md` to `dryrun-F.md` in this folder.

Caveats on the method: the library PDFs all have a text layer, so `pdftotext` works on the "scans" too; a real scan may need OCR. Every file in the library has the upload date (2026-10-29) as its modified date, so any rule that uses modified dates could not be tested properly. The photo-agent and knowledge-agent behaviour is my guess of a reasonable agent, not a recording.

## Results

| Scenario | Expected (README) | Got | Pass/fail | Notes |
|---|---|---|---|---|
| A dishwasher, E15, user approves | Covered by plan EPP-3Y-90417733 to 2029-03-14; manual E15 checklist; claim draft to protect@brightline-services.example with receipt, plan number, serial; warn base opening voids coverage; use 2024 receipt | Covered by the plan to 2029-03-14; checklist from manual p. 9 and p. 10; draft to protect@brightline-services.example with receipt, card, plan, plate photo; saved after "yes"; `waiting_approval` then `completed` | Pass | Read strictly, SKILL.md would have asked which dishwasher first (two receipts, user gave no model). The run followed examples.md instead (D1). The warning says "any repair beyond these steps voids the warranty and the plan" and "do not open the base"; it does not say "opening the base voids coverage" in one sentence. |
| B washer, F21, warranty? | Not covered, ended 2025-06-02; no plan; F21 steps; mention receipt came from a photo | Not covered, ended 2 Jun 2025; F21 steps (pump filter, drain hose); receipt photo noted; `completed` | Pass | Works only because the photo-agent returns the receipt text. The extract step has no photo path to read (D4). Date on the photo reads 06/02/2023 (D5). |
| C fridge, not cooling | Partly covered; general ended 2023-01-10; compressor to 2027-01-10; steps; flag serial 30847 vs 30647; re-photograph plate or fix registration | Unclear (rule for serial mismatch); same dates and steps; mismatch shown with both values and files; user told to read the plate; draft offered, `waiting_approval` | Pass on substance, label differs | coverage-rules.md and examples.md scenario 3 both say a serial mismatch makes the verdict Unclear. README says Partly covered. The skill is consistent with itself; README is the outlier (D8, D12). |
| D TV, sound but no picture, user declines | Covered until 2026-12-01, 11 days left, file soon; no manual found; offer generic checks; care@lumora-tv.example | Partly covered until 2026-12-01 (card covers panel, board, power supply only; cause unknown); 11 days left stated; no manual stated; only "switch off and unplug"; claim to care@lumora-tv.example; `waiting_approval` then `cancelled` | Fail | Verdict label differs (Partly covered vs Covered) and no generic checks were given, because SKILL.md forbids improvising repair steps. Dates, contact and urgency are right. Cause: the named-component rule gives "may be covered", and no rule maps that to a label (D8). README's "generic checks" conflicts with Step 4 (D12). |
| E sweep, three months | TV 2026-12-01, soundbar 2026-12-18, fridge compressor 2027-01-10; dishwasher plan and motor not in the window; washer and old dishwasher expired; router has no date | Same three in "Ending soon" in that order; plan 2029-03-14 and motor 2034-03-14 under "Active later"; old dishwasher left out; washer listed under "Term unknown" (wrong, it is expired); router missing; `waiting_approval` | Pass on the core list, with two gaps | The ending-soon list is correct. The washer is listed as unknown because its receipt is a photo the sweep never searches (D10). The router is missing because S1 never searches manuals (D11). |
| F coffee machine | Not in README. examples.md: nothing found, ask for purchase date, do not use other documents | Both searches empty, one short question, `waiting_user`, no other appliance used | Pass | Wording differs from examples.md (D13). SKILL.md has two instructions that conflict on whether to run Step 4 while waiting (D13). |

Pass count: 5 of 6 (A, B, C on substance, E on the core list, F). D fails on the verdict label. C and D both turn on verdict-label rules that README and the skill do not agree on.

## Skill defects found

Each item: where, what went wrong, one-line fix.

D1. SKILL.md Step 1, "Choosing between candidates". Two dishwasher purchases and no model from the user; the text says ask "unless the user's details settle it", but a rating-plate photo is not a user detail, so a literal reader asks. examples.md scenario 1 says the plate settles it. Fix: say that a rating-plate photo whose model matches one receipt counts as settling it, and the other receipt goes in Notes.

D2. SKILL.md Step 2, "any file in the same folder as {receipt path} with a modified date within 30 days of {purchase date}". Modified dates on a NAS are copy or upload dates, so this clause returned nothing here, and on a real NAS it can pull unrelated files from a busy folder (for a photo receipt, the whole Phone folder of that month). Fix: drop the clause, or replace it with "files in the same folder whose name contains the brand or model".

D3. coverage-rules.md "Exclusions" versus Step 3 "Unclear". For E15 the manual lists three causes (loose hose, door gasket, internal leak); gaskets and improper installation are excluded, internal leaks are covered. Read strictly, "a match makes the verdict Unclear" turns almost every leak into Unclear. Fix: say Unclear only when the manual names one cause and it matches an exclusion; when several causes are listed, keep the verdict and add a Notes line quoting the exclusion.

D4. SKILL.md Step 1 extract instruction takes "{receipt paths from file-agent}" only. When the only receipt is a photo (washer), that list is empty and the step says nothing about sending the photo path to document-agent. Fix: say the document-agent extract may take photo paths, or say to use the photo-agent text as the purchase record when no file-agent receipt exists.

D5. coverage-rules.md has no rule for ambiguous printed dates. The washer receipt prints 06/02/2023 (2 June or 6 February). Fix: add "if a printed date can be read two ways, use the order number, file name or photo date to choose, and state the reading in Notes".

D6. SKILL.md Step 4 file-agent instruction uses "{series}", but no upstream result supplies it (receipts and plates show ADW-4820, manuals say ADW-48xx). Fix: either drop {series}, or say "series = model with its last two digits replaced by xx when the model has four digits".

D7. SKILL.md Step 5 does not say which serial goes in a claim when receipt/registration and plate photo differ (fridge). examples.md says the plate value with a note. Fix: state "use the plate value, list the registered value beside it, and mark it to be checked".

D8. SKILL.md Step 3 and coverage-rules.md. "May be covered if the technician confirms a {component} fault" has no verdict label. The TV card covers only panel, board and power supply; the receipt says just "1-year limited warranty", so the card and receipt differ in scope. Fix: map it to a label (suggest: Covered when the symptom plausibly fits a listed component, with the "if the technician confirms" wording; Partly covered only when part of the fault is clearly outside the listed parts).

D9. SKILL.md status table. A declined save fits both `completed` ("with or without a saved note") and `cancelled` ("user declines the save"). Fix: reserve `cancelled` for stopping the conversation, and report `completed` with "not saved" when the user only declines the save, or the reverse, but say which.

D10. SKILL.md sweep S1 searches only files by name and text. A receipt that exists only as a phone photo (washer) is never found, so a washer with a card and no receipt ends up as "term unknown" instead of "ended 2 Jun 2025". Fix: add a photo-agent search for receipts to S1, and add a sweep rule for "warranty card with no receipt".

D11. SKILL.md sweep S1/S2 never looks at manuals, so a product with only a manual (router) is not listed. README expects "router, no date"; examples.md scenario 5 lists it. Fix: add to S1 a search for user manuals and list products found only there as "no receipt found".

D12. references/examples.md does not match the library or the manual:
- Scenario 1 says "do not tilt the appliance (technician only)"; the manual says tilt "only if instructed" and "Do not open the base".
- Scenario 1 lists "check the filter for blockage" for E15; the E15 row has no filter step (the filter is the E24 fix).
- Scenario 1 gives the plan as 15 Mar 2026 to 14 Mar 2029; the plan document and README say start 2026-03-14.
- Scenario 3 says fridge "2 years general, general ended 10 Jan 2024"; the registration says 1 year, ended 2023-01-10.
- Scenario 3 verdict is Unclear while README expects Partly covered.
- README D expects "generic checks" for the TV; Step 4 forbids improvised steps.
Fix: correct these in examples.md, and make README's expected C and D agree with coverage-rules.md.

D13. SKILL.md Step 1 "If both searches return an empty result" and the status rules. (a) The photo-agent cannot tell which appliance a plate belongs to, so it returns every plate and receipt photo; the skill does not say that irrelevant photos count as empty. (b) Step 1 says "continue with Step 4 if they do not [know the date]" while the status table says nothing runs until the user replies. (c) The message differs from examples.md scenario 6. Fix: say "photos whose text names a different product count as no match", say the run stops at `waiting_user`, and align the message with the example.

D14. SKILL.md "Safety" and answer-format.md. "Water near electrics" moves the safety line to the top; a leaking dishwasher with water in the base pan is close to electrics but the user did not say so. Unclear whether E15 should lead with the safety line. Fix: list "any appliance leak with an electrical supply" explicitly as a safety-first case, or say it is not.

D15. SKILL.md has no step to deduplicate. `Downloads/ADW-48xx_manual (1).pdf` is a byte-identical copy of the manual in Manuals; the file-agent returns both and the evidence list could cite either. Fix: add "if two matches have the same size and name stem, keep the one in the most specific folder and say a duplicate exists".

D16. coverage-rules.md "Start date" rule 1 versus rule 3. The plan prints "Plan start 2026-03-14, the day after the 2-year manufacturer warranty ends", but the warranty ends on 2026-03-14 and counts as active that day, so the day after is 2026-03-15. The documents conflict by one day. Fix: say a printed plan start date wins, and note a one-day overlap or gap as a Note rather than an Unclear verdict.

D17. SKILL.md sweep "Window" has only "default 90 days". "Three months" has no conversion rule (90 days ends 2027-02-18, three calendar months ends 2027-02-20). Fix: say "use calendar months when the user names months, days otherwise".

D18. SKILL.md Step 3 cross-check condition "receipt, the warranty documents and any rating-plate photo all exist". Unclear whether it runs for the washer and TV (no plate photo for them) or when the verdict is Not covered. This run skipped it in B and D. Fix: say "run it whenever a receipt and a warranty document exist; add the plate comparison only if a plate photo of this product exists".

D19. answer-format.md "Safety first: {one warning quoted from the manual}" cannot be filled when no manual exists (TV). Fix: allow the Step 4 universal advice (switch off and unplug) in that line when there is no manual.

D20. SKILL.md Step 5 draft has "Already tried: the troubleshooting steps the user confirms they already tried" but no step asks the user. Fix: add "ask which of the steps the user has tried before showing the draft" or default to "none confirmed".
