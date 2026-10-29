# Fixproof tabletop dry run: results

Skill: project/fixproof/ (SKILL.md and references/). Library: project/testdata/home-library/. Today 2026-11-20 08:40. I played Uliya and the four experts myself. Photos were read as images (EXIF DateTimeOriginal as date taken), PDFs through pdftotext, file-agent by file names and folders only, document-agent only on the files named in each instruction. The expected-answers section of the README was read only after all seven transcripts were written. Transcripts are dryrun-A.md to dryrun-G.md in this folder. Older runs are archived in v1 to v4 and were not used.

Pass means the label, the dates, the key files and the status token match. Result: 7 of 7 pass. Two passes (F and G) depend on a judgment call the skill does not spell out (defects 1 and 2).

## Results

| Scenario | Expected | Got | Pass/fail | Notes |
|---|---|---|---|---|
| A dishwasher "doing this again" | Covered; warranty ended 14 Mar 2026, plan EPP-3Y-90417733 to 14 Mar 2029; 2024 receipt not 2019; gasket excluded, internal leak covered; E15 steps with safety first; duplicate manual noted; draft to protect@brightline-services.example, "none confirmed", saved after the yes; completed | Same. Plate ADW-4820 settled the model, sha256 equal, draft to protect@brightline-services.example, "Already tried: checked the hoses" after the yes, saved to Warranty claims/Warranty claim Nordvik ADW-4820 2026-11-20 0840.md, completed | Pass | The E15 photo was accepted only because the user said "doing this". Choosing the plan contact over the manufacturer's needed an unstated judgment (defect 3). |
| B washer F21 | Not covered, ended 2 Jun 2025; receipt photo read as 2 June; F21 drain steps; no draft | Same, completed | Pass | The E15 photo was ignored because the user gave F21. Extraction and reconcile skipped correctly. |
| C fridge not cooling | Unclear; general ended 10 Jan 2023; partly covered to 10 Jan 2027 once serial confirmed (30847 vs 30647); steps; draft with plate serial marked to check | Same, 51 days left on the sealed system; draft to service@homehub-care.example; stops at waiting_approval | Pass | No user reply was given, so no save. |
| D TV sound but no picture | Covered to 1 Dec 2026, 11 days left, if technician confirms panel, board or power supply; no manual, universal safety only; draft to care@lumora-tv.example; declined: completed, not saved | Same | Pass | Rear-label photo is not on the NAS, listed as "take one before sending". |
| E sweep, 3 months | Window 20 Nov 2026 to 20 Feb 2027; ending soon $2,527: 1 Dec TV, 18 Dec soundbar, 10 Jan 2027 fridge compressor; later: plan 14 Mar 2029, motor 14 Mar 2034; unknown: router; 2 older out of warranty; waiting_approval | Same | Pass | The sweep never reads rating plates, so the fridge serial mismatch is not visible (defect 4). |
| F coffee machine | Nothing found; asks when bought; waiting_user; no other appliance documents used | Same | Pass | Passed only after the display-only E15 photo was admitted by the "no symptom" branch of the Step 0 gate and brand Nordvik leaked into the searches (defect 1). |
| G washer E15 (task-defined) | Dishwasher E15 photo must not change product or brand; receipt from photo; Not covered, ended 2 Jun 2025; WM-7 manual has no E15, say so, universal safety advice only; completed | Same. Manual has no E15 row (codes F21, E03, E10 only); no steps given; completed | Pass | Photo rejected only because "showing E15" was read as a named symptom and not as pointing at the photo (defect 1). The skill has no rule for a manual that lacks the code (defect 2). |

## Delegations per scenario

| Scenario | Total | Breakdown |
|---|---|---|
| A | 13 | photo 2, file 4 (receipts, warranty, manuals, sha256), document 6 (extract, locate, terms, reconcile, manual confirm, E15 rows), knowledge 1 |
| B | 9 | photo 2, file 3, document 4 (locate, terms, manual confirm, F21 rows); extract and reconcile not sent |
| C | 11 | photo 2, file 3, document 6 (extract, locate, terms, reconcile, manual confirm, not-cooling rows); no knowledge call yet |
| D | 9 | photo 2, file 3, document 4 (extract, locate, terms, reconcile); no manual, so no content check; no knowledge call (user declined) |
| E | 5 | photo 1, file 1, document 3 (receipts, warranty terms, manuals); no knowledge call yet |
| F | 3 | photo 2, file 1; no extraction because every receipt name points to another product |
| G | 9 | photo 2, file 3, document 4 (locate, terms, manual confirm, E15 lookup); extract and reconcile not sent |

## Skill defects found

High (wrong verdict, missed fact or rule violation)

1. High. Step 0 gate admits a photo of unknown kind through the "names no symptom" branch. In F the Nordvik E15 display photo was accepted for a coffee machine, Nordvik went into the file and photo searches and the photo into the evidence list; in G the photo is rejected only by reading "showing E15" as a named symptom. The end results were right, but a wrong brand or code can reach the search of any warranty-only question. Fix: when no appliance kind is visible, use the photo only if the user's words point at it ("this", "it", "again", "see the photo") and no other product or code is named, and never take a brand or model from a photo for a product the user named differently.

Medium (misleading or relies on unstated judgment)

2. Medium. Step 4 has no rule for a manual that exists but has no row for the code (G). The skill covers "no manual" only, so the universal-advice-only behaviour had to be inferred. Fix: add "If the confirmed manual has no row for the code or symptom, say so, give only the universal safety advice, and do not use another model's manual".
3. Medium. Step 5 does not say which claim contact to use when the manufacturer warranty has ended and a plan is active (A has two contacts). Fix: add "use the contact of the coverage that is active today; the manufacturer's only while its warranty is in force".
4. Medium. The sweep never reads rating plates, so a serial mismatch like the fridge's (plate 30647 against registered 30847) goes unreported on the calendar line that sends the user to claim. Fix: in S1 add a photo-agent rating-plate search and in S3 add "if a plate serial differs from the registered serial, say so on that line".
5. Medium. The Step 1 keep rule "plates whose text names {brand}" would keep another product's plate from the same brand (the Nordvik ADW-4820 plate for the Nordvik WM-7 in B and G). Fix: "keep a plate only if its model matches the receipt or the named model; use the brand alone only when no model is known".

Low (wording or efficiency)

6. Low. No dishwasher or coffee machine short names are listed, so "DW" and "espresso" were guesses. Fix: add a short-names table or say "type plus short names you are sure of".
7. Low. Step 4 does not say which candidates go to the manual content check (all manual-named files, or only those also named with the brand, model or series). Fix: "send only files named as a manual and with the brand, model or series".
8. Low. Step 2 content check sends the receipt and the manuals too, since only other-product names are filtered. Fix: "send only files whose names suggest warranty, plan, terms or registration, or name no product".
9. Low. Step 1 does not say to skip the receipt extraction when every receipt name points to another product (B, F, G). Fix: add "if no receipt file remains, send no extraction".
10. Low. Name search is by substring, so "washer" returns the two dishwasher receipts and the photo search returns unrelated rating plates every time. Fix: note that product matches are filtered by name afterwards, or search plates only for the product type.
11. Low. When the user says "again" (A) and the manual says "call service if E15 returns", the skill does not tell the parent to lead with that. Fix: add "if the user says the fault is a repeat and the manual says to call service on a repeat, put that first in the checklist".
