# fixproof tabletop validation

Eight scenarios run against the fictional library in `testdata/home-library/`, with "today" set to 2026-11-20 08:40. The parent followed `fixproof/SKILL.md` and its references literally. Each expert agent was played from the real files: pdftotext for document-agent, the images plus EXIF DateTimeOriginal for photo-agent, case-insensitive file-name matching for file-agent, sha256sum for duplicate checks, and a successful save for knowledge-agent. Expected answers are in `testdata/README.md`. Transcripts: `dryrun-A.md` to `dryrun-H.md`.

This is a tabletop simulation with fictional data, not a run on a NAS.

## Scenario table

| Scenario | Expected | Got | Pass/fail | Delegations |
|---|---|---|---|---|
| A "The dishwasher is doing this again." | Covered. Base ended 2026-03-14, plan EPP-3Y-90417733 to 2029-03-14. Plate photo settles ADW-4820, 2024 receipt used. E15 steps, safety first. Duplicate manual noted. Claim to protect@brightline-services.example, "Already tried: none confirmed", saved after "I checked the hoses, yes save it". completed. | Same. "If E15 returns, call service" first; attachments only the receipt; one-day plan gap noted; saved path reported after completed + verified. | Pass | 13 (photo 2, file 4, document 6, knowledge 1) |
| B "Washing machine shows F21. Is it still under warranty?" | Not covered, receipt photo 06/02/2023 read as 2 June 2023, ended 2025-06-02, F21 drain steps, no draft. completed. | Same. No PDF extraction (no PDF receipt for a washer). | Pass | 9 (photo 2, file 3, document 4) |
| C "The fridge stopped cooling." | Unclear, general ended 2023-01-10, partly covered to 2027-01-10 once serial confirmed (30847 vs 30647), not-cooling steps, draft with plate value marked. | Same. waiting_approval. | Pass | 11 (photo 2, file 3, document 6) |
| D "The TV has sound but no picture." (declines save) | Covered to 2026-12-01, 11 days, if panel/board/PSU. No manual, universal safety only. Draft to care@lumora-tv.example. Declined: completed, not saved. | Same. Water line left out for a TV. | Pass | 9 (photo 2, file 3, document 4) |
| E "Which warranties run out in the next three months?" | Window to 2027-02-20. Ending soon $2,527: TV 12-01, soundbar 12-18, fridge compressor 2027-01-10. Active later: plan 2029-03-14, motor 2034-03-14. Unknown: router. 2 older out of warranty. waiting_approval. | Identical. | Pass | 5 (file 1, photo 1, document 3) |
| F "Is my coffee machine under warranty?" | Nothing found, asks roughly when bought, waiting_user, no dishwasher documents used. | Same. Step 0 skipped. | Pass | 2 (file 1, photo 1) |
| G "My washing machine is showing E15." | Not changed by today's dishwasher E15 photo. Receipt photo, Not covered, ended 2 Jun 2025. WM-7 manual has no E15 entry: say so, universal safety only. completed. | Same, with the WM-7 support contact (page 1). One round. | Pass | 9 (photo 2, file 3, document 4) |
| H "When does the dishwasher warranty run out?" | ADW-4820 by plate photo. Base ended 14 Mar 2026, plan to 14 Mar 2029, motor to 14 Mar 2034. No checklist, no draft, manual offered in one line. completed. | Same, coverage-only template. Step 0 skipped. | Pass | 7 (photo 1, file 2, document 4) |

Pass count: 8 of 8. Total delegations: 65. No expert failed. Every slot was filled with a real value or left out.

## Defects found in this run

Four low-severity wording defects came out of this run. All four are fixed in the shipped `fixproof/SKILL.md`: the doubled "Read only" prefix, the trigger line now names devices and "not working", the save instruction no longer claims the user saw the exact saved text, and both save steps say what to do when a save is not verified.
