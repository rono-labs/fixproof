# Dry-run results v2: fixproof

Scenario date 2026-11-20 08:40. Tabletop run of `project/fixproof/SKILL.md` against `project/testdata/home-library/` (28 files, now including the 2026-11-20 display photo). Transcripts: `dryrun-A.md` to `dryrun-F.md` in this folder. Expected answers (`project/testdata/README.md`, matching `references/examples.md`) were read only after all six transcripts were written. The v1 run is archived in `v1/`.

Method and limits:
- file-agent was emulated as a case-insensitive substring match of the instruction's name terms against the file name and its folder names, never file contents. Under this rule `Documents/Receipts/2025/Brightline_soundbar_2025-12-18.pdf` matches "receipt" through its folder, but `Scans/2024/Brightline_EPP_terms_scan.pdf` matches nothing.
- photo-agent: images were viewed with the Read tool; the 48-hour window used the EXIF date taken (cutoff 2026-11-18 08:40, so only the new display photo qualifies). It returns what the instruction asks for, so a rating plate is not returned by a receipt search.
- document-agent: `pdftotext` of only the files named in each instruction. knowledge-agent: save succeeds. Every file has the upload date (2026-10-29) as modified date.
- The user reply "the newer one" in A is invented; the script gives none.

## Results

| Scenario | Expected | Got | Pass/fail | Notes |
|---|---|---|---|---|
| A dishwasher, "doing this again", user saves | Starts from the photo (E15, Nordvik); the plate settles the model, so no question; Covered, ended 2026-03-14, plan EPP-3Y-90417733 to 2029-03-14; claim to protect@brightline-services.example; notes duplicate manual and excluded gasket; saved after "yes" | Photo used. Stopped to ask which dishwasher (2019 or 2024). After the reply: Unclear, plan terms not found; no plan claim contact; gasket and duplicate manual noted; saved; `completed` | Fail | The plate photo is never searched (D1) and the EPP scan is never found by name (D2). Wrong label and wrong claim contact. |
| B washer F21, warranty? | Not covered, ended 2025-06-02; F21 steps; receipt from a photo; no draft | Not covered, ended 2 Jun 2025; pump filter and drain hose steps; 06/02/2023 read as 2 June and receipt-from-photo noted; no draft; `completed` | Pass | Reconcile cannot read the photo receipt (D7). The Nordvik E15 photo had to be set aside by judgement (D3). |
| C fridge, not cooling | Unclear; would be partly covered (compressor, to 2027-01-10) once the serial is confirmed (registration 30847, plate 30647); claim uses plate value | Partly covered, general ended 2023-01-10, compressor to 2027-01-10; no mismatch seen; draft with serial 30847; `waiting_approval` | Fail | The plate photo (serial ...30647) is never retrieved (D1), so the mismatch rule never fires. Dates and steps are right. |
| D TV, no picture, user declines | Covered until 2026-12-01 if a technician confirms a panel, board or power supply fault; no manual; only universal safety advice; care@lumora-tv.example; not saved | Same; 11 days left; no manual stated; only "switch off at the wall or unplug"; draft to care@lumora-tv.example; user said no, `completed` with "not saved" | Pass | One wasted manual-confirm call (D9). |
| E sweep, three months | Window to 2027-02-20; value $2,527; TV 12-01, soundbar 12-18, fridge compressor 2027-01-10; active later plan and motor; router Unknown; 2 older appliances out of warranty; `waiting_approval` | Exactly that; the plan date comes from the receipt line only | Pass | The EPP terms scan was not found (D2) but the receipt line is enough for the date. The soundbar was found only through its folder name. |
| F coffee machine | "I couldn't find a receipt for your coffee machine on the NAS. Do you know roughly when you bought it?"; `waiting_user`; no other appliance used | Same wording; `waiting_user`; nothing borrowed | Pass | Three of four calls could not find anything (D7). |

Pass count: 4 of 6 (B, D, E, F). A and C fail on the verdict or flow, both from the same root cause (D1), with D2 on top for A.

## Delegation count per scenario

| Scenario | Delegations | Breakdown |
|---|---|---|
| A | 13 | Step 0: 1, Step 1: 3, Step 2: 3, Step 3: 1, Step 4: 4 (including a checksum call), save: 1 |
| B | 11 | 1, 3, 3, 1, 3 |
| C | 11 | 1, 3, 3, 1, 3 (save pending) |
| D | 10 | 1, 3, 3, 1, 2 (save declined) |
| E | 5 | S1: 2, S2: 3 (save pending) |
| F | 4 | 1, 3 |

User questions: A asked one that examples.md says is not needed; the rest asked none before the answer.

## Skill defects found

Severity: high = wrong verdict or rule violation, medium = misleading or an unneeded stop, low = wording.

D1 (high). SKILL.md Step 1 photo-agent instruction asks only for paper receipts, yet "Choosing between candidates" and Step 3 rely on a rating-plate photo "from Step 0 or Step 1". Older plate photos are never fetched, so A asks an unneeded question and C misses the serial mismatch and says Partly covered instead of Unclear. Fix: add "or an appliance rating plate or serial label that mentions {product} or {brand}" to the Step 1 photo-agent instruction.

D2 (high). Step 2 file-agent matches names only, and the content check only sees what file-agent returned, so a plan terms scan with a generic name (`Scans/2024/Brightline_EPP_terms_scan.pdf`) is never confirmed; A cannot compute coverage from the plan and lacks its claim contact. Fix: add the store from the receipt, "EPP", "terms" and "scan" to the Step 2 name terms, and have file-agent also list every document in folders named Scans so document-agent can confirm by content.

D3 (medium). Step 0 says "Text that does not name an appliance counts as no match", but example 1 uses a photo that reads only "E15" and "Nordvik", and a recent photo of another appliance is returned in B, C, D and F with no rule for ignoring it (its brand would corrupt every later search). Fix: say a photo's code and brand are used only when its text names the product type or the user gave no code, and otherwise count it as unrelated.

D4 (medium). No rule covers a protection plan that the receipt names but whose terms document is not found: Covered, Unclear and "partly" are all arguable, and Step 5 has no fallback for a missing claim contact. Fix: say a plan known only from the receipt gives Unclear with "would be Covered to {date} once the plan terms are confirmed", and the draft's To line says the contact was not found.

D5 (medium). Step 4 triggers the checksum only for results that "share a name stem and size"; the two ADW manuals have the same size but different names, so a literal reader skips it. Fix: trigger on equal size, or on two files both confirmed as the manual for the model.

D6 (low). Step 4 `{symptom}` is the user's own words, which can be unsearchable ("doing this again"). Fix: say to build the symptom from the code's meaning or, if unknown, ask once what the appliance is doing.

D7 (low). Step 1 sends every receipt path to document-agent whatever the product (4 to 5 files for B, C, D, F), and Step 3 reconcile gets a photo path it cannot read in B. Fix: filter receipts by product from file names before extracting, and say that for a photo receipt the reconcile uses the photo-agent text.

D8 (low). `{series}` is undefined for models with one digit (WM-7) or leading digits (55Q8). Fix: "if the model does not fit the pattern, leave the series out".

D9 (low). Step 4 runs a confirm call over manuals of other brands when none can match (D). Fix: skip the confirm when no candidate name contains the brand or model.

D10 (low). Safety-first for a leak is decided from the manual's E15 meaning, but the user never said "leak". Fix: say the safety line leads when the manual row for the code mentions water, gas, smoke or sparks.
