# Fixproof tabletop validation, results

Run date in scenario: 2026-11-20 08:40. Skill: project/fixproof/ (SKILL.md and references/). Library: project/testdata/home-library/. Experts were played from the real files: pdftotext for document-agent, the actual images (Read tool) and EXIF DateTimeOriginal for photo-agent, name-substring matching only for file-agent, and a successful save for knowledge-agent. The README "Expected answers" section was read only after all eight transcripts were written. Neither the skill nor the test data was edited. Transcripts are in project/validation/dryrun-A.md to dryrun-H.md.

## Scenario table

| Scenario | Expected | Got | Pass/fail | Notes |
|---|---|---|---|---|
| A "The dishwasher is doing this again." | Covered. Base warranty ended 2026-03-14, plan EPP-3Y-90417733 to 2029-03-14. Plate photo settles ADW-4820, 2024 receipt used. E15 steps, safety first. Duplicate manual noted. Claim to protect@brightline-services.example, "Already tried: none confirmed" then saved after "I checked the hoses, yes save it". Status completed. | Covered, same dates and files, safety line first, "If E15 returns, call service" first in the checklist because the user said "again", gasket excluded and internal leak covered, duplicate noted (same sha256), draft to the plan contact, saved with "checked the hoses". completed. | Pass | 2019 receipt in Notes. Photo used because "doing this again" points to it. |
| B "Washing machine shows F21. Is it still under warranty?" | Not covered, photo receipt 06/02/2023 read as 2 June 2023, ended 2025-06-02, F21 drain steps, no draft. completed. | Not covered, ended 2 Jun 2025, date reading justified by US store, order number HH-230602, photo date. F21 steps from WM-7 manual. No draft. completed. | Pass | Today's E15 photo ignored (different code). No extraction sent because every receipt PDF is named for another product. |
| C "The fridge stopped cooling." | Unclear, general ended 2023-01-10, partly covered to 2027-01-10 once serial confirmed (30847 vs 30647), not-cooling steps, draft with plate value marked to check. | Unclear with exactly those dates and serials, six manual steps with technician-only 5 and 6, draft uses plate serial and marks it. waiting_approval. | Pass | Scenario ends at the approval question. Today's E15 photo ignored. |
| D "The TV has sound but no picture." (declines save) | Covered to 2026-12-01, 11 days, if panel/board/PSU fault. No manual, universal safety only. Draft to care@lumora-tv.example. Declined: completed, not saved. | Same. Rear-label photo listed as not on the NAS. completed, not saved. | Pass | |
| E "Which warranties run out in the next three months?" | Window 2026-11-20 to 2027-02-20. Ending soon, $2,527: TV 12-01, soundbar 12-18, fridge compressor 2027-01-10. Active later: plan 2029-03-14, motor 2034-03-14. Unknown: router. 2 older out of warranty. waiting_approval. | Identical, $2,527 from item prices, fridge marked "serial to check before claiming". waiting_approval. | Pass | |
| F "Is my coffee machine under warranty?" | Nothing found, asks roughly when bought, waiting_user, no dishwasher documents used. | Same, after 3 delegations. waiting_user. | Pass | |
| G "My washing machine is showing E15." | Product and brand not changed by today's dishwasher E15 photo. Washer receipt from photo, Not covered, ended 2 Jun 2025. WM-7 manual has no E15 entry: say so, universal safety advice only. completed. | Photo ignored, brand Nordvik taken from the washer receipt photo only. Not covered, ended 2 Jun 2025. "The manual for Nordvik WM-7 has no entry for E15", universal safety advice only, the dishwasher manual's E15 row not used. completed. | Pass | Passes only through the literal reading of "points to it" (defect 1). |
| H "When does the dishwasher warranty run out?" | ADW-4820 chosen by plate photo. Base ended 14 Mar 2026, plan to 14 Mar 2029, motor to 14 Mar 2034. No checklist, no draft, manual offered in one line. completed. | Same three dates, one-line manual offer, no draft, no save question. completed. | Pass | 2019 ADW-3100 in Notes. |

Pass count: 8 of 8.

## Delegations per scenario

| Scenario | Total | photo-agent | file-agent | document-agent | knowledge-agent |
|---|---|---|---|---|---|
| A | 13 | 2 | 4 | 6 | 1 |
| B | 9 | 2 | 3 | 4 | 0 |
| C | 11 | 2 | 3 | 6 | 0 |
| D | 9 | 2 | 3 | 4 | 0 |
| E | 5 | 1 | 1 | 3 | 0 |
| F | 3 | 2 | 1 | 0 | 0 |
| G | 9 | 2 | 3 | 4 | 0 |
| H | 8 | 2 | 2 | 4 | 0 |

Total: 67 delegations. No expert failed. Every slot was filled with a real value or the phrase was left out, as the skill requires.

## Skill defects found

No high-severity defects: no wrong verdict, missed fact or rule violation occurred in any of the eight runs.

Medium:

1. Step 0 photo gate (affects G, C, D, F, H). "The user's words point to it" is judged against example phrases only. In G the user typed the same code E15 that the unrelated dishwasher photo shows. The skill passes only if the reader decides that naming a code does not point at the photo. Fix: add a sentence that a code typed by the user, even one equal to the photo's, does not count as pointing to the photo; only words like "this", "doing this", "see the photo" do.
2. Step 2 content-check candidates (all fault runs). The rule "names suggest warranty, plan, terms or registration, or name no product" does not say to drop warranty files named for another product, although Step 1 does. Read literally, the washer run would send the dishwasher, fridge and TV warranties too. Fix: add "drop files whose names point to a different product" to the candidate rule.
3. Coverage-only path (H). Step 3 says "list each coverage with its end date", but answer-format.md only has a single "Coverage: {label}" line and no coverage-only layout, so the layout is improvised. Fix: add a short coverage-only template to answer-format.md (one line per coverage with its end date, then the one-line manual offer).
4. Sweep "value losing cover" (E). "Total purchase price of those products, from the receipts" does not say item price or receipt total. The receipts also hold delivery, installation and accessories; $2,527 is only reached with item prices. Fix: say "item price only, excluding delivery, installation, accessories and plan fees".

Low:

5. Step 1 extraction slot "{receipt paths}" is ambiguous because the find result also lists warranty cards and manuals (brand and model terms). Fix: say "only the files that are receipts, orders or invoices".
6. Step 0 runs in coverage-only questions (H, and F with no symptom) and finds nothing useful. Fix: skip Step 0 when the user reports no fault and gives no code, unless the product is unknown.
7. Short names such as FR, WM and DW in the photo-agent instruction (C, B, G, H) are noise for a vision search; they only make sense in file-name matching. Fix: use short names in the file-agent instruction only.
8. Rule 4 in coverage-rules.md says a plan starts "on the day the base warranty ends", but the plan text says "the day after" and rule "active on the end date itself" makes the two overlap by one day (A, H). The skill handles it with a note. Fix: define a "starts when the warranty ends" plan as beginning the next day, and keep the one-day-gap note.
9. Step 5 says list the attachments "the procedure asks for", while the draft template always shows a plan path (A, plan procedure wants plan number, receipt and serial). Fix: state that the plan terms path is listed only when the procedure asks for it, otherwise give the plan number in the body.
10. G: when a product is out of warranty and its manual has no entry for the code, the answer ends with only safety lines and no next step, although the manual prints a support contact on page 1. Fix: allow quoting the manual's own support contact in that case.
11. "Universal safety advice" (D, G) lists leak and valve lines that do not apply to a TV, and says these are the only lines allowed. Fix: say to include only the lines that fit the appliance.

Observations (not defects): the sweep clause "also list every document in folders named Receipts, Warranty..." is essential, because the soundbar receipt's name matches none of the name terms. The skill's name-based search reliably found everything once short names and series were derived as the skill describes.
