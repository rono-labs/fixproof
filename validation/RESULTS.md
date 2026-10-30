# Fixproof tabletop validation, results (v6)

Run date in scenario: 2026-11-20 08:40. Skill: project/fixproof/ (SKILL.md and references/), as edited for v6. Library: project/testdata/home-library/. Experts were played from the real files: pdftotext for document-agent, the actual images (Read tool) and EXIF DateTimeOriginal for photo-agent, case-insensitive name-substring matching only for file-agent (checked with a small matcher over the real file names), sha256sum for duplicate checks, and a successful save for knowledge-agent. The skill text was followed literally; where it left a choice open, the transcript says so. Test data was not edited. Transcripts are in project/validation/v6/dryrun-A.md to dryrun-H.md. Earlier runs: project/validation/dryrun-*.md (v5 final) and project/validation/v1 to v5.

This is a tabletop simulation with fictional data, not a NAS run.

## Scenario table

| Scenario | Expected | Got | Pass/fail | Notes |
|---|---|---|---|---|
| A "The dishwasher is doing this again." | Covered. Base ended 2026-03-14, plan EPP-3Y-90417733 to 2029-03-14. Plate photo settles ADW-4820, 2024 receipt used. E15 steps, safety first. Duplicate manual noted. Claim to protect@brightline-services.example, "Already tried: none confirmed", saved after "I checked the hoses, yes save it". completed. | Same. "If E15 returns, call service" first (repeat fault). Attachments list only the receipt, as the plan procedure asks; plan number in the body. Plan one-day gap noted (calculated start 15 Mar, printed 14 Mar kept). | Pass | 13 delegations. |
| B "Washing machine shows F21. Is it still under warranty?" | Not covered, receipt photo 06/02/2023 read as 2 June 2023, ended 2025-06-02, F21 drain steps, no draft. completed. | Same. No PDF extraction: every receipt PDF names another product, and the WM-7 card and manual are not receipts. | Pass | 9 delegations. |
| C "The fridge stopped cooling." | Unclear, general ended 2023-01-10, partly covered to 2027-01-10 once serial confirmed (30847 vs 30647), not-cooling steps, draft with plate value marked. | Same. Steps 5 and 6 technician only. Draft attaches receipt, registration and plate photo. waiting_approval. | Pass | 11 delegations. Ends at the approval question. |
| D "The TV has sound but no picture." (declines save) | Covered to 2026-12-01, 11 days, if panel/board/PSU. No manual, universal safety only. Draft to care@lumora-tv.example. Declined: completed, not saved. | Same. The water valve line is now left out for a TV. Rear-label photo listed as not on the NAS. | Pass | 9 delegations. |
| E "Which warranties run out in the next three months?" | Window to 2027-02-20. Ending soon $2,527: TV 12-01, soundbar 12-18, fridge compressor 2027-01-10. Active later: plan 2029-03-14, motor 2034-03-14. Unknown: router. 2 older out of warranty. waiting_approval. | Identical. Fridge marked "serial to check before claiming". | Pass | 5 delegations. |
| F "Is my coffee machine under warranty?" | Nothing found, asks roughly when bought, waiting_user, no dishwasher documents used. | Same. Step 0 skipped. | Pass | 2 delegations (v5: 3). |
| G "My washing machine is showing E15." | Not changed by today's dishwasher E15 photo. Receipt photo, Not covered, ended 2 Jun 2025. WM-7 manual has no E15 entry: say so, universal safety advice only. completed. | Same, now by the explicit typed-code rule. Also gives the WM-7 manual's own support contact (page 1). | Pass (2 rounds) | 9 delegations. Round 1 had no template line for the support contact (new defect N1); fixed, final answer recomposed in round 2. |
| H "When does the dishwasher warranty run out?" | ADW-4820 by plate photo. Base ended 14 Mar 2026, plan to 14 Mar 2029, motor to 14 Mar 2034. No checklist, no draft, manual offered in one line. completed. | Same, in the coverage-only template. Step 0 skipped. | Pass | 7 delegations (v5: 8). 2019 ADW-3100 in Notes. |

Pass count: 8 of 8.

## Rounds

- Round 1: all eight scenarios. All passed on outcome. In G the final answer needed a line the answer format did not have (N1).
- Fix after round 1: answer-format.md gained a "Support:" line, the "Safety first" line now also covers "no entry for the code", and SKILL.md Step 6 lists the support contact in the answer order.
- Round 2: G's final answer recomposed under the fixed format. The delegations do not depend on this change, so they were reused. Pass. No other scenario uses the new line, so none was re-run.

## Delegations per scenario

| Scenario | Total | photo-agent | file-agent | document-agent | knowledge-agent |
|---|---|---|---|---|---|
| A | 13 | 2 | 4 | 6 | 1 |
| B | 9 | 2 | 3 | 4 | 0 |
| C | 11 | 2 | 3 | 6 | 0 |
| D | 9 | 2 | 3 | 4 | 0 |
| E | 5 | 1 | 1 | 3 | 0 |
| F | 2 | 1 | 1 | 0 | 0 |
| G | 9 | 2 | 3 | 4 | 0 |
| H | 7 | 1 | 2 | 4 | 0 |

Total: 65 delegations (v5: 67; the difference is the skipped Step 0 in F and H). No expert failed. Every slot was filled with a real value or left out.

## Skill defects from v5, status

1. Step 0 photo gate, typed code does not point to the photo. Already applied before v6; confirmed in G.
2. Step 2 content-check candidates drop files named for another product. Already applied; confirmed in A to D, G, H.
3. Coverage-only template in answer-format.md. Already applied; used in H.
4. Sweep value uses item prices only. Already applied; $2,527 in E.
5. Extraction sends only receipts, orders and invoices. Was only partly applied (the rule dropped other products but not warranty cards and manuals). Fixed in v6; in A, B, C, H the cards and manuals in the find result were not sent.
6. Skip Step 0 when no fault and no code, unless the product is unknown. Fixed in v6; F and H skip it.
7. Short names in file-agent instructions only. Was only implied ("for name searches"). Fixed in v6: photo-agent gets the type alone.
8. A plan that starts when the warranty ends begins the next day; one-day-gap note kept. Fixed in v6 (coverage-rules.md rule 4); A and H note the gap.
9. Plan terms path listed only when the claim procedure asks for it. Fixed in v6 (SKILL.md Step 5 and the draft template); A attaches only the receipt.
10. Out of warranty and no manual entry: quote the manual's own support contact. Fixed in v6 (Step 4 instruction and text); G gives it.
11. Universal safety advice: only lines that fit the appliance. Fixed in v6 (coverage-rules.md); D drops the valve line for the TV.

Also in v6: the phrase "never write 'the file from before' inside an instruction" in SKILL.md became "never refer to an earlier result without its real value". SKILL.md now links references/validation.md.

## New defects found in v6

N1 (low, fixed in round 2). G: answer-format.md had no line for the manual's support contact that fix 10 allows, so round 1 improvised a "Next step" line. Fix: a "Support:" line in the fault-mode format and in the Step 6 order.

N2 (low, open). G: the universal line "If you smell gas or burning, or see smoke or sparks..." is kept whole for a washing machine, which has no gas supply. Fix 11 works at line level, so the word "gas" stays. Harmless; could be split into a gas line and a burning line.

Observations (not defects): in A, the Step 1 photo search for receipts mentioning "Nordvik" also returns the washer receipt photo, which the parent drops by product. The sweep clause "also list every document in folders named Receipts..." is still the only way the soundbar receipt is found.
