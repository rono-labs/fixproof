# Dry run A: "The dishwasher is doing this again."

Today 2026-11-20 08:40. Paths are relative to project/testdata/home-library/. All file modified dates on the library are 2026-10-29 (copy date, never used as purchase date). Follow-up user turn: "I checked the hoses, yes save it".

Mode: fault. Product: dishwasher. Symptom: "doing this again" (vague). No code, brand or model from the user.

## Step 0

DELEGATE photo-agent:
'Search photos taken in the last 48 hours, up to 2026-11-20 08:40, for pictures of an appliance control panel or display showing an error code, or of an appliance rating plate or serial label. If the search cannot filter by time, take the 20 newest photos instead. For each photo found, up to 20, run text recognition and return the photo path, the time taken, the recognised text, and which kind of appliance the photo shows. If there are no results, say zero matches.'

Result (image actually read): 1 photo at or after 2026-11-18 08:40. Photos/Phone/2026-11/IMG_20261120_083012.jpg, EXIF 2026-11-20 08:30:12. Text: "NORDVIK", display "E15", button labels POWER, CYCLE, DELAY, START. Kind of appliance: a control panel with a red display; the image does not show whether it is a dishwasher or a washing machine.

Parent: code E15, brand Nordvik. The "kind of appliance matches the product" gate cannot be applied because the photo shows no kind. Judgment call (not in the skill): the user said "this" about a photo just taken and named only a dishwasher, so the photo is accepted and the doubt is noted. See defect D1.

## Step 1

DELEGATE file-agent ({model} unknown, so left out):
'Find files whose names contain any of: receipt, invoice, order, purchase, quittung, Nordvik, dishwasher. Search folders whose names contain Receipts, Invoices, Purchases, Orders, Documents, Scans or Downloads first, then all user files. File types: documents and images. Return full path, file name, type, size and modified date for each, up to 50. If there are no results, say zero matches.'

Result (names and folders only), 8 files: Documents/Receipts/2019/receipt_dishwasher_old.pdf; Documents/Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf; Documents/Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf; Documents/Receipts/2025/Brightline_order_TV_Lumora.pdf; Documents/Receipts/2025/Brightline_soundbar_2025-12-18.pdf (matched through its Receipts folder); Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf; Manuals/Nordvik_ADW-48xx_UserManual.pdf; Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf.

DELEGATE photo-agent:
'Search the photo library for photos of a paper receipt or till slip that mention dishwasher or Nordvik, and for photos of any appliance rating plate or serial label. Newest first, up to 20 of each. For each photo found, run text recognition and return the photo path, the date taken, whether it is a receipt or a rating plate, and the recognised text. If there are no results, say zero matches.'

Result (images read):
- Photos/Phone/2024-03/IMG_20240316_190455.jpg, taken 2024-03-16 19:04:55, rating plate: "NORDVIK MODEL: ADW-4820 SERIAL: NV48-2203-1187 120V 60Hz 15A 1800W MFD 2023-12".
- Photos/Phone/2022-01/IMG_20220115_101233.jpg, taken 2022-01-15 10:12:33, rating plate: "HomeHub MODEL: FR-560 SERIAL: HH56-2201-30647 VOLTS 115V 60Hz AMPS 6.5 REFRIGERANT R600a 38 g MADE FOR HomeHub Appliances Compressor: sealed system".
- Photos/Phone/2023-06/IMG_20230602_181404.jpg, taken 2023-06-02 18:14:04, receipt: "HOMEHUB APPLIANCES, 77 Harbor Road, Port Alder OR, Date: 06/02/2023, Order HH-230602-1187, Cust: Alex Rivera, Nordvik WM-7 Front Load Washer, SN NV7-2305-60912 $899.00, Delivery $59.00, TOTAL $958.00, Paid: CARD ****4417, Warranty: see manufacturer card".

Parent: the washer receipt names a different product (no match). The FR-560 plate names neither Nordvik nor dishwasher (ignored). The ADW-4820 plate names Nordvik (kept).

DELEGATE document-agent (receipt paths whose names do not point to another product: the fridge, TV and soundbar files are dropped):
'Extract purchase details with the receipt schema from these files: Documents/Receipts/2019/receipt_dishwasher_old.pdf, Documents/Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf. If a file returns no data with the receipt schema, try the invoice schema. For each file return store, order number, purchase date exactly as printed, product description, brand, model number, serial number if printed, price, and every other line item, especially any protection plan, extended warranty or care plan with its plan number and term. Report any file you could not read.'

Result from pdftotext of the two files:
- 2019: Brightline Electronics, BL-2019-0822-20318, 2019-08-22, Nordvik ADW-3100 Dishwasher, serial NV31-1905-0342, $529.00; other: haul-away $25.00; no plan. (Printed: manufacturer warranty 1 year, no extended plan.)
- 2024: Brightline Electronics, BL-2024-0314-55871, 2024-03-14, Nordvik ADW-4820 Dishwasher, serial NV48-2203-1187, $849.00; 3-Year Extended Protection Plan, plan no. EPP-3Y-90417733, $129.00 ("Covers ADW-4820 after the manufacturer warranty ends. Terms provided separately."); installation kit $24.99. Total $1,002.99.

Choice: plate model ADW-4820 and serial NV48-2203-1187 match exactly the 2024 receipt, so no question to the user. The 2019 ADW-3100 purchase goes in Notes. Model ADW-4820, series ADW-48xx.

## Step 2

DELEGATE file-agent:
'Find files whose names contain any of: warranty, guarantee, garantie, protection, plan, care, extended, registration, certificate, terms, conditions, Nordvik, ADW-4820, ADW-48xx, Brightline. Search folders whose names contain Warranty, Receipts, Scans, Documents, Home or Appliances first, then all user files. File types: documents and images. Return full path, file name, size and modified date for each, up to 50. If there are no results, say zero matches.'

Result, 10 files: Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf; Scans/2024/Brightline_EPP_terms_scan.pdf; Scans/Lumora_TV_warranty.pdf; Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf; Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf; Manuals/Nordvik_ADW-48xx_UserManual.pdf; Downloads/ADW-48xx_manual (1).pdf; Documents/Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf; Documents/Receipts/2025/Brightline_order_TV_Lumora.pdf; Documents/Receipts/2025/Brightline_soundbar_2025-12-18.pdf.
The scan-folder fallback is skipped: a result names terms and Brightline and sits in Scans.

DELEGATE document-agent:
'With intent locate_content and evidence mode focused, check these files: Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf, Scans/2024/Brightline_EPP_terms_scan.pdf, Scans/Lumora_TV_warranty.pdf, Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf, Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf, Manuals/Nordvik_ADW-48xx_UserManual.pdf, Downloads/ADW-48xx_manual (1).pdf, Documents/Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf, Documents/Receipts/2025/Brightline_order_TV_Lumora.pdf, Documents/Receipts/2025/Brightline_soundbar_2025-12-18.pdf. List only the files that are a warranty, guarantee, protection plan or warranty registration for Nordvik ADW-4820 or the series ADW-48xx, or a plan bought with order BL-2024-0314-55871. For each, quote the line that shows it. If none match, say zero matches.'

Result: 2 files. Nordvik_ADW-4820_warranty_card.pdf: "LIMITED WARRANTY CARD, Product: ADW-4820 Dishwasher". Brightline_EPP_terms_scan.pdf: "Covered product Nordvik ADW-4820 Dishwasher, serial NV48-2203-1187 ... Purchased 2024-03-14 (Brightline order BL-2024-0314-55871)".

DELEGATE document-agent:
'Answer from these files only: Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf, Scans/2024/Brightline_EPP_terms_scan.pdf. With intent period and answer mode table, return for each document: the provider, each coverage (full parts and labour, parts only, or named components such as motor, compressor or panel) with its term, how the start date is defined, and any printed start or end date. With intent condition, return the exclusions and the claim procedure (phone, email or web form exactly as written, required attachments). Also return any plan number, registration number and serial number written on it. Quote the page or section for each answer.'

Result:
- Nordvik card (page 1): parts and labor 2 years; drive motor 10 years (parts only after year 2); start "date of original retail purchase", dated receipt required; no printed dates. Exclusions: misuse, improper installation, power surges, frozen pipes, commercial use, cosmetic damage, consumables (filters, racks, gaskets), repairs by anyone other than an authorized provider; owner repairs beyond the manual's steps void it. Claim: "Email claims@nordvik-support.example or call 1-800-555-0188 (Mon-Fri 8:00-18:00 Pacific)"; receipt copy and serial plate photo required. No plan, registration or serial number.
- Brightline plan (page 1, sections 1-5): plan EPP-3Y-90417733; administrator Brightline Protection Services; parts and labor for mechanical and electrical failure, "including leaks from internal components, drain pump, heater, control board and sensors"; plan start 2026-03-14 "the day after the 2-year manufacturer warranty ends", plan end 2029-03-14; serial NV48-2203-1187. Exclusions: cosmetic damage, racks, filters and gaskets, misuse or improper installation, pre-existing conditions, commercial use, repairs by unapproved parties; owner repairs beyond the manual's steps void the plan. Claim: "Email protect@brightline-services.example or call 1-800-555-0199"; plan number, original receipt and serial number; no deductible. While the manufacturer warranty is in force, claims go to the manufacturer.

## Step 3

DELEGATE document-agent:
'Reconcile these files and report every difference in brand, model number, serial number, purchase date, plan start or end date, or owner name: Documents/Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf, Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf, Scans/2024/Brightline_EPP_terms_scan.pdf. For each difference give both values and the file each came from. If they all agree, say no differences found.'

Result: no differences found (brand Nordvik, model ADW-4820, serial NV48-2203-1187 on receipt and plan, purchase 2024-03-14, owner Alex Rivera). The warranty card prints no serial or dates.
Parent: plate photo serial NV48-2203-1187 equals receipt and plan serial.

Arithmetic: bought 14 Mar 2024 + 2 years = ended 14 Mar 2026. Plan printed 14 Mar 2026 to 14 Mar 2029 (the printed start equals the manufacturer end date while the text says "the day after"; a one-day difference, printed date kept, noted). Today 20 Nov 2026 is inside the plan. Motor 10 years = 14 Mar 2034 (parts only). Label: Covered.

## Step 4

DELEGATE file-agent:
'Find files whose names contain any of: manual, guide, instructions, handbook, quick start, ADW-4820, ADW-48xx, Nordvik. Search folders whose names contain Manuals, Documents, Downloads, Home or Appliances first, then all user files. File type: documents. Return full path, file name, size and modified date, up to 20. If there are no results, say zero matches.'

Result: Manuals/Nordvik_ADW-48xx_UserManual.pdf (17516); Downloads/ADW-48xx_manual (1).pdf (17516); Manuals/Zentro_AX3000_Router_Manual.pdf (6029); Home/Appliances/Washer/WM-7_manual.pdf (9774); Home/Appliances/Fridge/FR-560_owner_manual.pdf (9127); Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf (2960); Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf (2681).
Parent: named both as a manual and with brand or series: the first two. Others dropped.

DELEGATE document-agent:
'With intent locate_content, check these files: Manuals/Nordvik_ADW-48xx_UserManual.pdf, Downloads/ADW-48xx_manual (1).pdf. List only the files that are the user manual or guide for Nordvik ADW-4820 or the series ADW-48xx, and quote the line that shows it. If none match, say zero matches.'
Result: both; "Nordvik Dishwasher, Model series ADW-48xx, User Manual and Care Guide".

Same size 17516, so:
DELEGATE file-agent:
'Return the sha256sum of each of these files: Manuals/Nordvik_ADW-48xx_UserManual.pdf, Downloads/ADW-48xx_manual (1).pdf.'
Result: both 2858e0506bfc17fb3076623c5b917c28c11cb91b4650cc02af821eb6bfde3b7d. Identical: keep Manuals/ copy, note the duplicate.

DELEGATE document-agent (code alone, since "doing this again" is vague):
'Using only Manuals/Nordvik_ADW-48xx_UserManual.pdf, with intent locate_content and answer mode table, find what the manual says about error code E15. Return the matching rows of the error-code and troubleshooting tables (problem, cause, what to do) in the order printed, the safety warnings that apply to those steps, any steps that need a qualified technician, and any statement that user repairs affect the warranty. Give the page or section for each item.'

Result:
- Section 7 Error codes, p.9: E15, "Water detected in the base pan. Leak protection has stopped the unit." Action: turn off water, unplug, tilt unit slightly to drain base pan only if instructed, check door gasket and hose connections. If E15 returns, call service. Do not open the base.
- Section 8, p.10: "Puddle under unit, E15 shown"; cause water in base pan: loose hose, door gasket, or internal leak; solution: stop the unit, check hose clamps and gasket; service call if the leak persists.
- Safety, p.3: "Do not operate a dishwasher that is leaking. Turn off the water supply and unplug the unit."
- Technician: call service if E15 returns; do not open the base.
- Warranty: p.3 and p.10, user repair beyond the listed steps (opening the base, replacing parts, bypassing sensors) voids the manufacturer warranty and any extended protection plan.

Exclusion check: manual lists several causes (hose, gasket, internal leak); gaskets are excluded in both documents, internal leak is covered by the plan. Keep Covered, add a Note.

## Step 5

Claim draft shown, checklist shown, so the question is: "Which of these steps have you already tried? Say yes to save the draft to your NAS, or no." Status waiting_approval.

    To: Email protect@brightline-services.example or call 1-800-555-0199
    Subject: Warranty claim, Nordvik ADW-4820, serial NV48-2203-1187
    Product: Nordvik ADW-4820, serial NV48-2203-1187
    Purchased: 2024-03-14 at Brightline Electronics, order BL-2024-0314-55871
    Coverage: Brightline 3-Year Extended Protection Plan EPP-3Y-90417733, valid until 2029-03-14
    Fault: leak protection stopped the unit, water in base pan, error code E15
    Already tried: none confirmed
    Attachments: Documents/Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf, Scans/2024/Brightline_EPP_terms_scan.pdf, Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf
    Contact: (blank)

User: "I checked the hoses, yes save it". "Already tried" becomes "Checked the hoses". Clear yes.

DELEGATE knowledge-agent:
'Save this text as a new note in a folder named Warranty claims in the user home folder, or in the default notes location if that folder cannot be used, with filename hint "Warranty claim Nordvik ADW-4820 2026-11-20 08:40". Text: To: Email protect@brightline-services.example or call 1-800-555-0199 / Subject: Warranty claim, Nordvik ADW-4820, serial NV48-2203-1187 / Product: Nordvik ADW-4820, serial NV48-2203-1187 / Purchased: 2024-03-14 at Brightline Electronics, order BL-2024-0314-55871 / Coverage: Brightline 3-Year Extended Protection Plan EPP-3Y-90417733, valid until 2029-03-14 / Fault: leak protection stopped the unit, water in base pan, error code E15 / Already tried: Checked the hoses / Attachments: Documents/Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf, Scans/2024/Brightline_EPP_terms_scan.pdf, Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf / Contact:'
(Real send has the draft's line breaks.) Result: saved, path "Warranty claims/Warranty claim Nordvik ADW-4820 2026-11-20 08.40.md" (simulated path).

## Final answer (status completed)

    Safety first: Do not operate a dishwasher that is leaking. Turn off the water supply and unplug the unit (manual p.3). If water keeps appearing, call a qualified technician.
    Product: Nordvik ADW-4820 (dishwasher), bought 14 Mar 2024 at Brightline Electronics
    Coverage: Covered. Bought 14 Mar 2024 + 2-year warranty = ended 14 Mar 2026. Protection plan EPP-3Y-90417733 runs 14 Mar 2026 to 14 Mar 2029, so covered by the plan.
    Try this (manual section 7, p.9, and section 8, p.10):
      1. Turn off the water and unplug the unit.
      2. Check the door gasket and the hose connections and clamps (you did the hoses).
      3. Tilt the unit slightly to drain the base pan only if instructed.
      Technician only: if E15 returns, call service. Do not open the base. Opening the base or other repairs void the warranty and the plan (p.3, p.10).
    Claim: draft saved to Warranty claims/Warranty claim Nordvik ADW-4820 2026-11-20 08.40.md. Send it to protect@brightline-services.example or 1-800-555-0199 yourself.
    Evidence:
      - IMG_20261120_083012.jpg: E15 on a Nordvik panel, taken 2026-11-20 08:30
      - IMG_20240316_190455.jpg: plate ADW-4820, NV48-2203-1187
      - Documents/Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf: purchase 2024-03-14, order BL-2024-0314-55871, serial, plan line
      - Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf: 2 years, motor 10 years, exclusions, claim contact
      - Scans/2024/Brightline_EPP_terms_scan.pdf: plan 2026-03-14 to 2029-03-14, claim contact
      - Manuals/Nordvik_ADW-48xx_UserManual.pdf: E15, safety, warranty note
    Notes: A worn door gasket is excluded by both documents; an internal leak is covered by the plan. Plan start printed 14 Mar 2026 versus "the day after" the 2-year end: one day, printed date kept. A duplicate manual exists at Downloads/ADW-48xx_manual (1).pdf (same sha256). Another purchase, the 2019 Nordvik ADW-3100 (Documents/Receipts/2019/receipt_dishwasher_old.pdf), was not used. The photo's appliance kind was not visible; accepted because you said "this" and the plate settled the model.

Delegations: 13 = photo-agent 2, file-agent 4, document-agent 6 (extract, locate, terms, reconcile, manual confirm, E15), knowledge-agent 1.
