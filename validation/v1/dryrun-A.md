# Dry run A: dishwasher leaking, E15 (user approves the save)

Today = 2026-11-20. User: "My dishwasher is leaking and showing E15."
Library root below: `home-library/` = `project/testdata/home-library/`. Expert results are emulated from `find`, `grep` and `pdftotext` output, and from viewing the photos.

## Intake
Mode: fault. Product: dishwasher. Symptom: leaking, code E15. Brand and model: not given by the user, so those slots are left out of the instructions (SKILL.md, "If a slot has no real value, leave that part out").

## Step 1. Purchase record

delegate --target file-agent --instruction 'Find documents that look like receipts, invoices or order confirmations for a dishwasher. Search folders whose names contain Receipts, Invoices, Purchases, Orders, Documents, Scans or Downloads first, then all of the user files. Include PDF, image and office document types. For each match return the full path, file name, type and modified date, up to 30 matches. If there are no results, say zero matches.'

file-agent result (2 matches, both PDF, modified date 2026-10-29 for every file because that is the upload date):
- home-library/Documents/Receipts/2019/receipt_dishwasher_old.pdf
- home-library/Documents/Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf

delegate --target photo-agent --instruction 'Search the photo library for photos of a paper receipt or of an appliance rating plate or serial label for a dishwasher. For each photo found, run text recognition and return the photo path, the date taken and the recognised text. If there are no results, say zero matches.'

photo-agent result (3 photos; the vision search cannot tell which appliance a plate belongs to, so it returns every receipt or plate photo; text read from the images):
- Photos/Phone/2024-03/IMG_20240316_190455.jpg, 2024-03-16: "NORDVIK / MODEL: ADW-4820 / SERIAL: NV48-2203-1187 / 120V 60Hz 15A 1800W / MFD 2023-12"
- Photos/Phone/2022-01/IMG_20220115_101233.jpg, 2022-01-15: "HomeHub / MODEL: FR-560 / SERIAL: HH56-2201-30647 / ... R600a 38 g / Compressor: sealed system"
- Photos/Phone/2023-06/IMG_20230602_181404.jpg, 2023-06-02: receipt "HOMEHUB APPLIANCES ... Order HH-230602-1187 ... Nordvik WM-7 Front Load Washer SN NV7-2305-60912 ... $899.00"

Parent: the fridge plate and the washer receipt are other products; the Nordvik ADW-4820 plate is the only dishwasher plate. Two dishwasher purchases exist (2019 ADW-3100, 2024 ADW-4820). SKILL.md says to ask which one "unless the user's details settle it". The user gave no model. Read literally this would stop with `waiting_user`. This run follows examples.md, scenario 1: the only dishwasher rating plate on the NAS reads ADW-4820, so the 2024 purchase is used and the 2019 receipt is named in Notes. See defect D1 in RESULTS.md.

delegate --target document-agent --instruction 'Extract purchase details with the receipt schema from these files: home-library/Documents/Receipts/2019/receipt_dishwasher_old.pdf, home-library/Documents/Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf. For each file return store, order number, purchase date, product description, brand, model number, serial number if printed, price, and every other line item, especially any protection plan, extended warranty or care plan with its plan number and term.'

document-agent result:
- 2019 receipt: Brightline Electronics, order BL-2019-0822-20318, 2019-08-22, Nordvik ADW-3100 Dishwasher, serial NV31-1905-0342, $529.00. Other lines: haul-away $25.00. Text: "Manufacturer warranty: 1 year parts and labor. No extended plan purchased."
- 2024 receipt: Brightline Electronics, order BL-2024-0314-55871, 2024-03-14, Nordvik ADW-4820 Dishwasher, serial NV48-2203-1187, $849.00. Other lines: "3-Year Extended Protection Plan, Plan no. EPP-3Y-90417733, covers ADW-4820 after the manufacturer warranty ends, terms provided separately" $129.00; installation kit $24.99.

Parent merges: plate serial NV48-2203-1187 equals the 2024 receipt serial. Chosen purchase: 2024-03-14.

## Step 2. Warranty and plan documents

delegate --target file-agent --instruction 'Find documents that mention ADW-4820 or Nordvik dishwasher together with any of these words: warranty, guarantee, protection plan, extended, care plan, certificate, registration. Also return any file in the same folder as home-library/Documents/Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf with a modified date within 30 days of 2024-03-14. Return full path, file name and modified date for each, up to 30. If there are no results, say zero matches.'

file-agent result (modified 2026-10-29 on all, so the same-folder clause returns nothing and the folder holds only the receipt anyway; see defect D2):
- home-library/Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf (mentions ADW-4820, warranty)
- home-library/Scans/2024/Brightline_EPP_terms_scan.pdf (mentions ADW-4820, protection plan)
- home-library/Documents/Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf (protection plan line)
- home-library/Documents/Receipts/2019/receipt_dishwasher_old.pdf (Nordvik dishwasher, warranty line)
- home-library/Manuals/Nordvik_ADW-48xx_UserManual.pdf and home-library/Downloads/ADW-48xx_manual (1).pdf (Nordvik dishwasher, warranty note)

Parent keeps the two warranty-type documents: Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf and Scans/2024/Brightline_EPP_terms_scan.pdf.

delegate --target document-agent --instruction 'Answer from these files only: home-library/Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf, home-library/Scans/2024/Brightline_EPP_terms_scan.pdf. For each document return: who provides it, what it covers (full parts and labour, parts only, or named components such as motor or compressor) with the term for each, whether the term starts at purchase, delivery or when another warranty ends, the exclusions, the claim procedure (phone, email or web form exactly as written, and required attachments), and any plan or registration number with any serial number written on it. Quote the page or section for each answer.'

document-agent result:
- Warranty card (Nordvik, page 1): parts and labor 2 years from original retail purchase date; drive motor 10 years (wash motor and circulation pump motor, parts only after year 2). Starts on date of original retail purchase, dated receipt required. Exclusions: misuse, improper installation, power surges, frozen pipes, commercial use, cosmetic damage, consumables (filters, racks, gaskets), repairs by anyone other than an authorized provider; owner repairs beyond the manual void it. Claim: email claims@nordvik-support.example or call 1-800-555-0188 (Mon-Fri 8:00-18:00 Pacific); needs dated receipt and a clear photo of the serial plate. No serial or plan number printed.
- Plan terms (Brightline Protection Services, page 1): plan EPP-3Y-90417733, product Nordvik ADW-4820, serial NV48-2203-1187. Plan start 2026-03-14 "the day after the 2-year manufacturer warranty ends"; plan end 2029-03-14. Covers parts and labor for mechanical and electrical failure, "including leaks from internal components, drain pump, heater, control board and sensors" (section 1). Not covered: cosmetic damage, racks, filters, gaskets, misuse or improper installation, pre-existing conditions, commercial use, unapproved repairs; owner repairs beyond the manual's steps void the plan (section 2). Claim: email protect@brightline-services.example or call 1-800-555-0199, with plan number, original receipt, product serial; technician visit within 5 business days; no deductible (section 3). Claims go to the manufacturer while the manufacturer warranty is in force (section 5).

## Step 3. Verdict and cross-check

delegate --target document-agent --instruction 'Compare these files and report every difference in model number, serial number, purchase date, owner name or store: home-library/Documents/Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf, home-library/Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf, home-library/Scans/2024/Brightline_EPP_terms_scan.pdf. For each difference give both values and the file each came from. If they all agree, say no differences found.'

document-agent result: no differences found. Model ADW-4820 in all three; serial NV48-2203-1187 on receipt and plan (warranty card prints none); purchase date 2024-03-14 on receipt and plan; owner Alex Rivera on receipt and plan; store Brightline on receipt and plan. The plate photo serial (photo-agent text) is also NV48-2203-1187.

Parent arithmetic (coverage-rules.md):
- Manufacturer warranty: start 2024-03-14 (purchase, per card) + 2 years = ends 2026-03-14. Today 2026-11-20 is after it. Ended.
- Drive motor: + 10 years = 2034-03-14, active, but E15 (water in base pan) does not point to a motor.
- Protection plan: written start 2026-03-14 (rule 3 would give 2026-03-15), end 2029-03-14. Active today.
- Exclusion check: the manual's causes for E15 are "loose hose, door gasket, or internal leak". Gaskets and improper installation are excluded, "internal leak" is covered. The manual does not say which cause it is, so the verdict stays Covered with a note. A strict reader of coverage-rules.md "A match makes the verdict Unclear" could land on Unclear here (defect D3).
Verdict: Covered by the protection plan.

## Step 4. Manual

delegate --target file-agent --instruction 'Find user manuals, installation guides or quick start guides for Nordvik ADW-4820. Search folders whose names contain Manuals, Documents, Downloads or Home first, then all user files. Return full path, file name and modified date, up to 10. If there are no results, say zero matches.'
(The {series} slot has no real value in any upstream result, so that part is left out; see defect D6.)

file-agent result (2 matches; neither file contains the string "ADW-4820", but the brand and folder match):
- home-library/Manuals/Nordvik_ADW-48xx_UserManual.pdf
- home-library/Downloads/ADW-48xx_manual (1).pdf (byte-identical text; the skill has no step to dedupe)

delegate --target document-agent --instruction 'Using only home-library/Manuals/Nordvik_ADW-48xx_UserManual.pdf, find what the manual says about error code E15 and about the symptom "leaking". Return the matching rows of the troubleshooting or error-code table (problem, cause, what to do) in the order printed, the safety warnings that apply to those steps, any steps the manual says need a qualified technician, and any statement that user repairs affect the warranty. Give the page or section for each item.'

document-agent result:
- Section 7 Error codes, p. 9: E15 "Water detected in the base pan. Leak protection has stopped the unit." Action: "Turn off water, unplug, tilt unit slightly to drain base pan only if instructed, check door gasket and hose connections. If E15 returns, call service. Do not open the base."
- Section 8 Troubleshooting, p. 10: "Water leaks from door" cause dirty gasket, overloading, too much detergent; solution wipe gasket, reload, use less detergent. "Puddle under unit, E15 shown" cause water in base pan (loose hose, door gasket, or internal leak); solution stop the unit, check hose clamps and gasket, service call if the leak persists.
- Safety, section 1, p. 3: "Do not operate a dishwasher that is leaking. Turn off the water supply and unplug the unit."
- Warranty effect: section 1 p. 3 and section 8 p. 10, user repairs beyond the listed steps void the manufacturer warranty and any extended protection plan.
- Technician: service call if E15 returns or the leak persists; do not open the base.

## Step 5. Claim draft (turn 1 of the conversation ends here)

Parent shows the final answer below and asks to save. Status: `waiting_approval`.

## Step 6. Final answer, turn 1

    Product: Nordvik ADW-4820 (dishwasher), bought 2024-03-14 at Brightline Electronics
    Coverage: Covered by the protection plan. Bought 14 Mar 2024 + 2-year warranty = ended 14 Mar 2026. Protection plan EPP-3Y-90417733 runs 14 Mar 2026 to 14 Mar 2029, so claims go to the plan.
    Safety first: "Do not operate a dishwasher that is leaking. Turn off the water supply and unplug the unit." (manual section 1, p. 3)
    Try this (manual section 7, p. 9 and section 8, p. 10):
      1. Turn off the water and unplug the unit.
      2. Check the door gasket and the hose connections and clamps.
      3. If E15 returns, call service.
      Technician only: do not open the base. Tilt the unit to drain the base pan only if instructed.
      Warranty note: any repair beyond these steps voids the warranty and the protection plan.
    Claim: draft ready for protect@brightline-services.example, 1-800-555-0199. Save it to your NAS? (yes / no)
    Evidence:
      - home-library/Documents/Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf: purchase 2024-03-14, order BL-2024-0314-55871, ADW-4820, serial NV48-2203-1187, plan line EPP-3Y-90417733
      - home-library/Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf: 2 years parts and labor, 10 years drive motor, exclusions, Nordvik claim contact
      - home-library/Scans/2024/Brightline_EPP_terms_scan.pdf: plan 2026-03-14 to 2029-03-14, leaks from internal components covered, gaskets and improper installation excluded, claim contact
      - home-library/Photos/Phone/2024-03/IMG_20240316_190455.jpg: rating plate, ADW-4820, serial NV48-2203-1187
      - home-library/Manuals/Nordvik_ADW-48xx_UserManual.pdf: E15 steps, p. 9 and p. 10
    Notes: Serial matches on receipt, plan and plate photo. The manual lists a loose hose or door gasket as possible causes of E15. The plan excludes gaskets and improper installation, so the plan administrator decides if the technician finds one of those. An older dishwasher (Nordvik ADW-3100, 2019, home-library/Documents/Receipts/2019/receipt_dishwasher_old.pdf) is also on the NAS and was not used.

Claim draft shown with it:

    To: protect@brightline-services.example or 1-800-555-0199 (Brightline Protection Services)
    Subject: Warranty claim, Nordvik ADW-4820, serial NV48-2203-1187
    Product: Nordvik ADW-4820, serial NV48-2203-1187
    Purchased: 2024-03-14 at Brightline Electronics, order BL-2024-0314-55871
    Coverage: 3-Year Extended Protection Plan EPP-3Y-90417733, valid until 2029-03-14
    Fault: dishwasher leaking, water in base pan, error code E15
    Already tried: none confirmed yet
    Attachments: home-library/Documents/Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf, home-library/Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf, home-library/Scans/2024/Brightline_EPP_terms_scan.pdf, home-library/Photos/Phone/2024-03/IMG_20240316_190455.jpg
    Contact: (left blank)

## Turn 2. User: "yes"

delegate --target knowledge-agent --instruction 'Save this text as a new note titled "Warranty claim - Nordvik ADW-4820 - 2026-11-20". Do not overwrite an existing note; if the title exists, add a number to the title. Text: To: protect@brightline-services.example or 1-800-555-0199 (Brightline Protection Services) / Subject: Warranty claim, Nordvik ADW-4820, serial NV48-2203-1187 / Product: Nordvik ADW-4820, serial NV48-2203-1187 / Purchased: 2024-03-14 at Brightline Electronics, order BL-2024-0314-55871 / Coverage: 3-Year Extended Protection Plan EPP-3Y-90417733, valid until 2029-03-14 / Fault: dishwasher leaking, water in base pan, error code E15 / Already tried: none confirmed yet / Attachments: home-library/Documents/Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf, home-library/Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf, home-library/Scans/2024/Brightline_EPP_terms_scan.pdf, home-library/Photos/Phone/2024-03/IMG_20240316_190455.jpg / Contact: (left blank)'

knowledge-agent result (simulated, no title clash): saved "Notes/Warranty claim - Nordvik ADW-4820 - 2026-11-20.md".

Parent: "Saved to Notes/Warranty claim - Nordvik ADW-4820 - 2026-11-20.md. Nothing was sent; you send the claim yourself."

Status tokens: `waiting_approval` (turn 1), then `completed` (turn 2).
