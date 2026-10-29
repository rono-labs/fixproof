# Fixproof tabletop dry run results

Date of run: scenario clock 2026-11-20 08:40. Skill: `project/fixproof/` (SKILL.md plus references). Library: `project/testdata/home-library/`. Transcripts: `dryrun-A.md` to `dryrun-F.md` in this folder. The expected answers in `project/testdata/README.md` were read only after all six transcripts were written. Neither the skill nor the test data was edited.

Method notes. File-agent find matched terms against file and folder names only. Photo-agent output came from viewing each image and from EXIF DateTimeOriginal. Document-agent output came from `pdftotext` of only the named files. Knowledge-agent save succeeded and returned a path.

## Results

| Scenario | Expected | Got | Pass/fail | Notes |
|---|---|---|---|---|
| A dishwasher, then "I checked the hoses, yes save it" | Covered; base warranty ended 2026-03-14; plan EPP-3Y-90417733 to 2029-03-14; 2024 receipt not 2019; gasket exclusion note; E15 steps with safety first; duplicate manual noted; claim to protect@brightline-services.example; saved; completed | Covered; same dates and plan; 2024 receipt settled by the plate photo; gasket note; safety line led; duplicate confirmed by sha256sum; claim to the plan administrator; draft saved with "Already tried: Checked the hoses"; waiting_approval then completed | Pass | Two extra delegations (Scans listing, sha256) wording had to be invented |
| B washer F21 | Not covered; receipt is a photo, 06/02/2023 read as 2 June 2023; warranty ended 2025-06-02; F21 drain steps; no claim draft | Not covered; 2 June 2023 settled by US store, order number HH-230602 and date taken; ended 2025-06-02; F21 steps given; no draft; completed | Pass | Today's E15 photo had to be ignored by judgment; skill is silent |
| C fridge not cooling | Unclear; general ended 2023-01-10; would be partly covered (compressor, sealed system) to 2027-01-10 once serial confirmed; HH56-2201-30847 vs HH56-2201-30647; not-cooling steps; draft uses plate serial marked to be checked | Unclear; same dates and both serials; steps given; draft uses plate serial HH56-2201-30647 with the registered one beside it; waiting_approval | Pass | Passed only because the photo-agent found the plate through a semantic match and the E15 photo was dropped by improvisation |
| D TV sound, no picture, declined save | Covered to 2026-12-01 (11 days) if panel, board or power supply fault; no manual, universal safety only; draft to care@lumora-tv.example; completed, not saved | Covered to 2026-12-01 (11 days left, if technician confirms a panel or board fault); "There is no manual for Lumora 55Q8 on your NAS"; universal safety line; draft to care@lumora-tv.example; waiting_approval then completed, not saved | Pass | No rear-label serial photo exists, noted as missing attachment |
| E sweep, three months | Window to 2027-02-20; ending soon $2,527: TV 2026-12-01, soundbar 2026-12-18, fridge compressor 2027-01-10; later: plan 2029-03-14, motor 2034-03-14; unknown: Zentro router; 2 older appliances out of warranty; waiting_approval | Identical list, $2,527.00, same dates, router unknown, "2 older appliances", waiting_approval | Pass | Plan end 2029-03-14 was only calculated from the receipt line; the plan terms file was never found by the sweep |
| F coffee machine | Could not find a receipt for the coffee machine; asks roughly when bought; waiting_user; no use of dishwasher documents | Exact question asked; waiting_user; no other product's file used | Pass | |

Pass count: 6 of 6.

## Delegations per scenario

| Scenario | photo-agent | file-agent | document-agent | knowledge-agent | Total |
|---|---|---|---|---|---|
| A | 2 | 4 (Step 1, Step 2, Scans listing, Step 4) plus 1 sha256 = 5 | 6 (extract, confirm plan, terms, reconcile, confirm manual, manual qa) | 1 | 14 |
| B | 2 | 3 | 4 (confirm warranty, terms, confirm manual, manual qa) | 0 | 9 |
| C | 2 | 3 | 6 (extract, confirm, terms, reconcile, confirm manual, manual qa) | 0 | 11 |
| D | 2 | 3 | 5 (extract, confirm, terms, reconcile, confirm manual) | 0 | 10 |
| E | 1 | 1 | 3 | 0 | 5 |
| F | 2 | 1 | 0 | 0 | 3 |

Total 52. Check A counts: photo 2, file 5, document 6, knowledge 1 = 14.

## Skill defects found

No high severity defects: every verdict, date and status matched. Two medium defects show the passes rely on judgment the skill does not give.

### Medium

1. Step 0 accepts an unrelated photo. The rule keeps any photo that shows a code or brand and does not "name a different product type or brand". Today's Nordvik E15 dishwasher photo therefore qualifies for a fridge (C), a TV (D) and a coffee machine (F) when the user names no brand, and it puts brand Nordvik and code E15 into later searches and, in C, would reach the manual query and the claim draft. In B it conflicts with the user's F21 and the skill has no rule for that. I dropped it by judgment once the receipt brand differed. Fix: after Step 1, discard any Step 0 photo whose brand or model differs from the purchase record, and ignore a photo code that differs from the user's code or does not appear in the manual.
2. The Step 1 plate search depends on the photo text "mentioning" the product or brand. The fridge plate says HomeHub FR-560 and REFRIGERANT, not "fridge"; a literal match misses it, and then the serial mismatch that decides scenario C (Unclear, not Covered or Partly covered) is never seen. Fix: after the receipt gives brand and model, run a second plate search by brand and model (for example "HomeHub FR-560"), and say so in the Step 1 wording.
3. Sweep S1 never finds plan terms filed under other names. `Scans/2024/Brightline_EPP_terms_scan.pdf` has none of the S1 name terms, and the sweep has no Scans or content-check step like Step 2. The plan end date (2029-03-14) was only derived from the receipt line, and the plan's exclusions and claim contact were not read. If the receipt text had not described the start rule, the ADW-4820 would have been counted as out of warranty. Fix: add terms, scan, certificate and the receipt's plan number to the S1 file search, or run the Step 2 Scans listing and content check whenever a receipt row has a plan line.

### Low

4. Step 4 says to confirm the manual "with the same locate_content check as Step 2", but that instruction lists warranty documents, so used verbatim it returns zero manuals. Fix: give an explicit manual-confirmation instruction ("List only the files that are the user manual for {brand} {model} or the series {series}").
5. No instruction text is given for the extra Scans listing (Step 2) or the sha256sum request (Step 4). Fix: add both as exact one-line instructions.
6. Step 2's Scans-listing trigger is "no candidate name mentions a plan". In A the terms file was already a candidate, so the extra call was redundant. Fix: skip it when any candidate sits in a Scans folder or has "terms" in its name.
7. Step 4 says to confirm by content unless no name contains the brand, model or series. In D the receipt and warranty files contain "Lumora", so the check fired and returned zero. Fix: apply the name test only to names that also contain a manual term (manual, guide, instructions, handbook, quick start).
8. Step 5 asks "Which of the steps above have you already tried?" even when there is no checklist (D, no manual) and duplicates the "Save it to your NAS? (yes / no)" line in the answer format. Fix: ask the tried-steps question only when a checklist was shown, and keep one save question.
9. The safety trigger "an error code whose manual row mentions water in the appliance" is ambiguous for drain faults (F21 "water not draining"). I read it as not a leak and did not lead with safety. Fix: say that drain and fill faults without a leak do not trigger the leading safety line.
10. Sweep header says "next {window} days" but the window is given in calendar months. Fix: print "next 3 months (to 2027-02-20)".
11. Step 3 does not say what to do when the receipt is a photo and only one document remains for reconcile (B). I skipped the call. Fix: state that reconcile runs only with two or more document paths.
12. The sweep never reads plate photos, so the fridge serial mismatch is not shown on a fridge item that ends in seven weeks. Fix: add a note line "serial not checked in sweep mode" for items that need a serial photo to claim.
