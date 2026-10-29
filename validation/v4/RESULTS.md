# Fixproof tabletop dry run: results

Skill: project/fixproof/ (SKILL.md and references/). Library: project/testdata/home-library/. Today 2026-11-20 08:40. Experts played from the real files: photos were read as images (EXIF DateTimeOriginal as date taken), PDFs through pdftotext, file-agent by names and folders only. Expected answers were read only after all seven transcripts were written. Transcripts: dryrun-A.md to dryrun-G.md in this folder.

Pass means the label, dates, key files and status token match. Result: 6 of 7 pass (A, B, C, D, F, G). E fails.

## Results

| Scenario | Expected | Got | Pass/fail | Notes |
|---|---|---|---|---|
| A dishwasher "doing this again" | Covered; plan EPP-3Y-90417733 to 2029-03-14; 2024 receipt; E15 steps, safety first; duplicate manual noted; draft to protect@brightline-services.example, then saved, completed | Same. Plate ADW-4820 settled the model, 2019 receipt in Notes, gasket note, sha256 match, "Already tried: Checked the hoses" after the yes, completed | Pass | Accepting the E15 photo needed a judgment call (D1). Plan start printed 14 Mar 2026 vs "the day after" noted as a one-day gap. |
| B washer F21 | Not covered, ended 2 Jun 2025; receipt photo read as 2 June; F21 drain steps; no draft | Same, completed | Pass | The E15 photo was ignored because the user named F21. Reconcile and PDF extraction correctly skipped. |
| C fridge not cooling | Unclear; general ended 10 Jan 2023; partly covered to 10 Jan 2027 once serial confirmed (30847 vs 30647); steps; draft with plate serial marked to check | Same; draft to service@homehub-care.example with plate serial marked; stops at waiting_approval (no user reply given) | Pass | The Nordvik E15 photo had to be ignored (D1). |
| D TV sound but no picture | Covered to 1 Dec 2026, 11 days left, if technician confirms panel, board or power supply; no manual, universal safety only; draft to care@lumora-tv.example; declined: completed, not saved | Same | Pass | No rear-label photo exists on the NAS; skill has no rule for a missing attachment (D6). |
| E sweep, 3 months | Window 20 Nov 2026 to 20 Feb 2027. Ending soon $2,527: 1 Dec TV, 18 Dec soundbar, 10 Jan 2027 fridge compressor. Later: plan 2029-03-14, motor 2034-03-14. Unknown: router. 2 older out of warranty. waiting_approval | Ending soon $2,348 (TV, fridge only). Soundbar and 2019 dishwasher listed as "term unknown". 1 older out of warranty. Later and router correct. waiting_approval | Fail | The S2 extract instruction never asks for the warranty sentence printed on receipts, so the soundbar (ends 18 Dec 2026, $179) and the 2019 dishwasher (1 year) are misfiled (D2). A document-agent that volunteers the sentence would pass. |
| F coffee machine | Not found; asks when bought; waiting_user; no other appliance documents used | Same | Pass | Receipts-folder name matches returned five receipts for other products; all discarded by the product-name rule. |
| G washer E15 | Today's dishwasher E15 photo not used; washer receipt from photo; Not covered, ended 2 Jun 2025; WM-7 manual has no E15, say so, universal safety only; completed | Same | Pass | Passes only because the photo's kind was "not visible" and the parent read the gate strictly. A loose reading would cite the dishwasher photo (D1). |

## Delegations per scenario

| Scenario | Total | Breakdown |
|---|---|---|
| A | 13 | photo 2, file 4 (receipts, warranty, manuals, sha256), document 6 (extract, locate, terms, reconcile, manual confirm, E15), knowledge 1 |
| B | 9 | photo 2, file 3, document 4 (locate, terms, manual confirm, F21); extract and reconcile skipped |
| C | 11 | photo 2, file 3, document 6 (extract, locate, terms, reconcile, manual confirm, not-cooling); no knowledge call yet |
| D | 9 | photo 2, file 3, document 4 (extract, locate, terms, reconcile); no manual so no content check; no knowledge call |
| E | 5 | photo 1, file 1, document 3 (receipts, warranty terms, manuals); no knowledge call yet |
| F | 3 | photo 2, file 1 |
| G | 9 | photo 2, file 3, document 4 (locate, terms, manual confirm, E15) |

## Skill defects found

High (wrong verdict, missed fact or rule violation)

- D1, high. Step 0 says to use a photo only when "the kind of appliance it shows matches the product", but a control-panel photo does not show the kind: the same Nordvik E15 photo is a dishwasher in A, and must be rejected in B, C, D, F and G. Applied strictly, A loses its E15 code; applied loosely, G cites the dishwasher photo and C, D and F inherit the brand Nordvik. Fix: add "a photo that shows no appliance kind is used only when the user's words point at it ('this', 'it', 'again') and they named no other product or code; never take a brand or model from it for another product; otherwise ignore it".
- D2, high. Step S2's receipt extraction does not ask for the manufacturer-warranty sentence printed on the receipt, and S2 labels any receipt without a term "term unknown", so the Lumora S2 soundbar (ends 18 Dec 2026) drops out of Ending soon, the 2019 dishwasher is not counted as out of warranty, and "value losing cover" is $2,348 instead of $2,527. Fix: add "and any warranty term or warranty sentence printed on the receipt" to the S2 extract instruction and label such rows "stated on the receipt".

Medium (misleading or relies on unstated judgment)

- D3, medium. Step 1's extract instruction has the same omission for fault mode: Step 2 says to check whether the receipt states a warranty term, but nothing asks the document-agent for it, so the fallback cannot work when the card is missing. Fix: add "any warranty term printed on the receipt" to the Step 1 extract instruction.
- D4, medium. Product words are searched literally ({product} such as "fridge" or "washing machine"). The fridge receipt was found only because its file name says "fridge"; a file named "refrigerator" or "washer" would be missed, and the photo-agent must equate "Front Load Washer" with "washing machine" on its own. Fix: add a synonym list per product (washer, washing machine; fridge, refrigerator; TV, television) to Required input and use all of them in the name terms.
- D5, medium. file-agent matches folder names, so any product search returns every file in a Receipts folder (five receipts for a coffee machine). The skill only works because the parent then drops names pointing to other products, a rule written for the extract step, not for the "no match" decision in F. Fix: state in Step 1 that files whose names point to another product are discarded before judging whether a purchase record exists.

Low (wording or efficiency)

- D6, low. No rule for a required attachment that is not on the NAS (the TV rear-label photo, a plate photo). Fix: in Step 5, "list the attachment as 'not on the NAS, user to take one' and say so in Notes".
- D7, low. answer-format.md has no Claim line variants for the three real states (waiting for yes, saved to {path}, declined and not saved), and the Step 5 question differs from the format's line. Fix: add the three wordings to answer-format.md.
- D8, low. Step 1 says to keep rating plates whose model matches a receipt found in "this step", but extraction comes after the keep rule. Fix: move the keep sentence after the extract instruction.
- D9, low. Step 2 and Step 4 slots "{candidate paths from file-agent}" send every hit (receipts, other products' cards) to the document-agent, wasting reads. Fix: say "drop files whose names point to a different product first".
- D10, low. The filename hint contains the time with a colon ("2026-11-20 08:40"), which many file systems reject. Fix: format {time} as 0840.
- D11, low. Step 4's second file-agent template needs {store} or {series} guidance when a slot is empty; the text works, but the instruction wording varies between runs. Fix: show one worked example of an instruction with an omitted slot.
