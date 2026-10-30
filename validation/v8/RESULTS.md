# Fixproof tabletop validation, results (v8, regression after the wording edit)

Run date in scenario: 2026-11-20 08:40. Skill: project/fixproof/SKILL.md as in the working tree (uncommitted wording edit, see `git diff HEAD -- project/fixproof/SKILL.md`); references/ unchanged. Library: project/testdata/home-library/. Method as in v6: the parent followed SKILL.md and its references literally; experts were played from the real files (pdftotext for document-agent; the images via the Read tool plus EXIF DateTimeOriginal for photo-agent; case-insensitive name-substring matching only for file-agent, checked with a small matcher script over the real file names; sha256sum for duplicates; a successful save for knowledge-agent). User replies as in v6: A "I checked the hoses, yes save it", D "No". Test data and skill were not edited. Transcripts: project/validation/v8/dryrun-A.md to dryrun-H.md.

This is a tabletop simulation with fictional data, not a NAS run.

## What was changed since v6 and what it did

| Change | Effect in the runs |
|---|---|
| Shorter description | No effect in the tabletop (skill invoked directly). Trigger wording lost "not working" and "or device" (V8-2). |
| Parameter jargon replaced (receipt/invoice schema, intent locate_content/period/condition/extraction, answer mode table, evidence mode, max files) | No expert result changed. Each instruction still names the document type ("receipts and invoices"), the files and the fields, and asks for a table where v6 asked for answer mode table. Extraction rows, confirmations, terms and manual rows are identical to v6. "max files 200" became "up to 200 files", so the cap is kept. |
| "Read only; do not change any ..." prefixes | Present on every photo, file and document instruction. Doubled on the checksum instruction (V8-1), harmless. |
| Delegation-order lines | Match the step order in all eight runs. The fault-mode line does not say Step 0 is conditional (O1); F and H still skip it under the explicit Step 0 rule. |
| "Expert states" failure rule | Every expert returned `completed`; rule satisfied, not otherwise exercised. |
| Save: "Do not overwrite", return path and verification | A: save returned path and verified=yes, path reported. The instruction's "this exact text" claim is slightly off (V8-3); a "not verified" result has no handling (V8-4). |
| Sweep "on no" | Not reached (E ends at `waiting_approval`, as expected). |
| Apostrophe rule for slots | No slot value in A to H contains a single quote; no effect. |
| Search scope "rest of the home folder and the shared folders this user can access" (was "all user files") | No effect: every file in the library sits under the one home tree, and the matcher returned exactly the v6 result sets for every find (A 8/10/7, B and G 6/8/7, C 6/7/7, D 5/8/7, E 15, F 4, H 7/10). |
| Language line | English throughout, no effect. |

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

Pass count: 8 of 8. Total delegations 65, same as v6, same split per agent. No expert failed. Every slot was filled with a real value or left out.

## Defects found in v8

| ID | Severity | SKILL.md line | Finding | Suggested fix |
|---|---|---|---|---|
| V8-1 | Low | 142 | The checksum instruction starts with "Read only; do not change any file." twice. Harmless, but looks like an editing slip in a judged file. | Replace the instruction with: `'Read only; do not change any file. Return the SHA-256 checksum of each of these files: {paths of the same-size manuals}. Report any file you could not read.'` |
| V8-2 | Low | 3 | The shorter description dropped "not working" and "or device". C ("stopped cooling") and D (TV "sound but no picture") are not-working faults, and a TV or router is a device more than an appliance. No effect in the tabletop, where the skill is invoked directly; may weaken routing on the NAS. | `description: Checks whether a broken appliance or device is still covered, finds the manual's steps for its error code or symptom and drafts a warranty claim, using the receipts, warranty cards, protection plans, manuals and photos already on the NAS. Also lists warranties that expire soon. Use when the user says an appliance or device is broken, not working, leaking or showing an error code, or asks about warranty cover.` |
| V8-3 | Low | 160 | The save instruction tells knowledge-agent "The user approved saving this exact text", but Step 5 (line 158) adds the user's tried steps to "Already tried" after the draft was shown, so the user never saw the exact saved text (A). | In line 160 replace "The user approved saving this exact text." with "The user approved saving this claim draft, with the steps they named added under Already tried." |
| V8-4 | Low | 162 and 193 | Both save instructions now ask "whether the save was verified", but nothing says what to do when knowledge-agent returns `completed` with a path that is not verified. Not reached in A (verified). | After "report that path." in lines 162 and 193 add: "If the save is not verified, say \"The save could not be confirmed; check {path}\" and keep the text in chat." |

Observation (not scored as a defect):

- O1, line 55. The fault-mode delegation-order line begins with "`photo-agent` (recent photos)" with no condition, while Step 0 is skipped for a coverage-only question with no code (F, H). The explicit Step 0 rule won in both runs. Optional fix: write "`photo-agent` (recent photos, when Step 0 runs)".

Open from v6, unchanged: N2 (low), the universal "gas or burning" line is kept whole for a washing machine (G).
