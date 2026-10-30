# Dry run C (v6): "The fridge stopped cooling."

Today 2026-11-20 08:40. Paths relative to the library root. Skill followed literally, v6 text. Round 1.

## Intake
Mode: fault mode. Product: fridge (file-agent: refrigerator, FR; photo-agent: fridge). Symptom: "stopped cooling", written as "not cooling". No code, brand or model. A fault is reported, so Step 0 runs.

## Step 0
### Delegation 1 to photo-agent
> Search photos taken in the last 48 hours, up to 2026-11-20 08:40, for pictures of an appliance control panel or display showing an error code, or of an appliance rating plate or serial label. If the search cannot filter by time, take the 20 newest photos instead. For each photo found, up to 20, run text recognition and return the photo path, the time taken, the recognised text, and which kind of appliance the photo shows. If there are no results, say zero matches.

Result: 1 match, Photos/Phone/2026-11/IMG_20261120_083012.jpg, "NORDVIK", "E15", panel buttons. Kind not visible.

Parent: does not match "fridge"; display only and the user's words do not point to it. Ignored; no code or brand taken.

## Step 1
### Delegation 2 to file-agent
> Find files whose names contain any of: receipt, invoice, order, purchase, quittung, fridge, refrigerator, FR. Search folders whose names contain Receipts, Invoices, Purchases, Orders, Documents, Scans or Downloads first, then all user files. File types: documents and images. Return full path, file name, type, size and modified date for each, up to 50. If there are no results, say zero matches.

Result: 6: Documents/Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf; Documents/Receipts/2019/receipt_dishwasher_old.pdf; Documents/Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf; Documents/Receipts/2025/Brightline_order_TV_Lumora.pdf; Home/Appliances/Fridge/FR-560_owner_manual.pdf; Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf.

### Delegation 3 to photo-agent
> Search the photo library for photos of a paper receipt or till slip that mention fridge, and for photos of any appliance rating plate or serial label. Newest first, up to 20 of each. For each photo found, run text recognition and return the photo path, the date taken, whether it is a receipt or a rating plate, and the recognised text. If there are no results, say zero matches.

Result: receipts: zero matches (the only receipt photo is for a washer). Plates: IMG_20240316_190455.jpg (NORDVIK ADW-4820, NV48-2203-1187); Photos/Phone/2022-01/IMG_20220115_101233.jpg, taken 2022-01-15 10:12:33: "HomeHub MODEL: FR-560 SERIAL: HH56-2201-30647 VOLTS 115V 60Hz AMPS 6.5 REFRIGERANT R600a 38 g MADE FOR HomeHub Appliances Compressor: sealed system".

### Delegation 4 to document-agent
Kept: the fridge receipt. Dishwasher and TV receipts name other products; the FR-560 manual and registration are not receipts (v6 rule 5).

> Extract purchase details with the receipt schema from these files: Documents/Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf. If a file returns no data with the receipt schema, try the invoice schema. For each file return store, order number, purchase date exactly as printed, product description, brand, model number, serial number if printed, price, any warranty term printed on the receipt, and every other line item, especially any protection plan, extended warranty or care plan with its plan number and term. Report any file you could not read.

Result: HomeHub Appliances, order HH-220110-3318, 2022-01-10, HomeHub FR-560 French Door Refrigerator, serial HH56-2201-30847, $1,649.00, no warranty term printed, no plan. Delivery and setup $79.00.

Parent: one fridge purchase, no choice needed. The FR-560 plate matches the receipt model and is kept; the ADW-4820 plate is ignored. Brand HomeHub, model FR-560. Series: FR-560 has three digits, left out. Store HomeHub.

## Step 2
### Delegation 5 to file-agent
> Find files whose names contain any of: warranty, guarantee, garantie, protection, plan, care, extended, registration, certificate, terms, conditions, HomeHub, FR-560. Search folders whose names contain Warranty, Receipts, Scans, Documents, Home or Appliances first, then all user files. File types: documents and images. Return full path, file name, size and modified date for each, up to 50. If there are no results, say zero matches.

(The store is also HomeHub, so the term appears once.)

Result: 7: Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf; Home/Appliances/Fridge/FR-560_owner_manual.pdf; Documents/Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf; Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf; Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf; Scans/Lumora_TV_warranty.pdf; Scans/2024/Brightline_EPP_terms_scan.pdf.

Parent: no plan on the receipt, no Scans listing. Candidates: the FR-560 registration and the EPP terms scan (names no product).

### Delegation 6 to document-agent
> With intent locate_content and evidence mode focused, check these files: Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf, Scans/2024/Brightline_EPP_terms_scan.pdf. List only the files that are a warranty, guarantee, protection plan or warranty registration for HomeHub FR-560, or a plan bought with order HH-220110-3318. For each, quote the line that shows it. If none match, say zero matches.

Result: the registration only: "Product: FR-560 Refrigerator". The EPP scan is for Nordvik ADW-4820.

### Delegation 7 to document-agent
> Answer from these files only: Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf. With intent period and answer mode table, return for each document: the provider, each coverage (full parts and labour, parts only, or named components such as motor, compressor or panel) with its term, how the start date is defined, and any printed start or end date. With intent condition, return the exclusions and the claim procedure (phone, email or web form exactly as written, required attachments). Also return any plan number, registration number and serial number written on it. Quote the page or section for each answer.

Result (page 1): HomeHub. General parts and labor 1 year from the original purchase date. Sealed system / compressor 5 years (compressor, condenser, evaporator, refrigerant lines; parts and labor years 1-5). Printed purchase date 2022-01-10; no printed end dates. Registered serial HH56-2201-30847, registered owner Alex Rivera. Exclusions: food loss, power outage damage, water filters, door bins, cosmetic damage, unauthorized repair. Claim: "Email service@homehub-care.example or call 1-800-555-0123." "Claims require receipt, registration and a photo of the serial plate. The serial must match the registration."

## Step 3
### Delegation 8 to document-agent
> Reconcile these files and report every difference in brand, model number, serial number, purchase date, plan start or end date, or owner name: Documents/Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf, Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf. For each difference give both values and the file each came from. If they all agree, say no differences found.

Result: no differences found (FR-560, serial HH56-2201-30847, 2022-01-10, Alex Rivera on both).

Parent, plate check: the plate photo reads HH56-2201-30647; receipt and registration read HH56-2201-30847. Serial differs: label Unclear (cross-check table), ask the user to read the plate. Dates: 10 Jan 2022 + 1 year = ended 10 Jan 2023. Compressor and sealed system: 10 Jan 2022 + 5 years = 10 Jan 2027, active. "Not cooling" may or may not be the compressor, so once the serial is confirmed it would be Partly covered.

## Step 4
### Delegation 9 to file-agent
> Find files whose names contain any of: manual, guide, instructions, handbook, quick start, FR-560, HomeHub. Search folders whose names contain Manuals, Documents, Downloads, Home or Appliances first, then all user files. File type: documents. Return full path, file name, size and modified date, up to 20. If there are no results, say zero matches.

Result: 7: Home/Appliances/Fridge/FR-560_owner_manual.pdf (9127); Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf; Documents/Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf; Manuals/Nordvik_ADW-48xx_UserManual.pdf; Manuals/Zentro_AX3000_Router_Manual.pdf; Home/Appliances/Washer/WM-7_manual.pdf; Downloads/ADW-48xx_manual (1).pdf.

Parent: named as a manual and with the model: FR-560_owner_manual.pdf only.

### Delegation 10 to document-agent
> With intent locate_content, check these files: Home/Appliances/Fridge/FR-560_owner_manual.pdf. List only the files that are the user manual or guide for HomeHub FR-560, and quote the line that shows it. If none match, say zero matches.

Result: match, "HomeHub French Door Refrigerator Model series FR-560 User Manual and Care Guide" (page 1).

### Delegation 11 to document-agent
> Using only Home/Appliances/Fridge/FR-560_owner_manual.pdf, with intent locate_content and answer mode table, find what the manual says about the symptom "not cooling". Return the matching rows of the error-code and troubleshooting tables (problem, cause, what to do) in the order printed, the safety warnings that apply to those steps, any steps that need a qualified technician, and any statement that user repairs affect the warranty. If there is no entry for the code or symptom, return the support or service contact printed in the manual. Give the page or section for each item.

Result: section 4, page 6, steps 1-6: power (plug, outlet, breaker); temperature setting (fridge 37 F, freezer 0 F, wait 24 hours); door seals and airflow; condenser coils (unplug, vacuum); condenser fan (if silent, call service); compressor (if it does not run or clicks repeatedly, call service, do not attempt repair). "Allow 24 hours after any change. Food safety: discard perishables above 40 F for more than 2 hours." Safety page 3: "Unplug before cleaning the condenser coils." Technician: steps 5 and 6. Warranty: page 7 refers to the warranty card; the registration excludes unauthorized repair.

Parent: no leak, gas or burning, so the safety line does not lead.

## Step 5
Unclear, so draft. Procedure asks for receipt, registration and a serial-plate photo. Plate serial used, registered value beside it, marked to check.

Draft shown:
```
To: Email service@homehub-care.example or call 1-800-555-0123
Subject: Warranty claim, HomeHub FR-560, serial HH56-2201-30647 (to check)
Product: HomeHub FR-560 refrigerator, serial HH56-2201-30647 per rating plate (registered as HH56-2201-30847, check before sending)
Purchased: 10 Jan 2022 at HomeHub Appliances, order HH-220110-3318
Coverage: HomeHub sealed system / compressor warranty, valid until 10 Jan 2027
Fault: not cooling
Already tried: none confirmed
Attachments: Documents/Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf, Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf, Photos/Phone/2022-01/IMG_20220115_101233.jpg
Contact:
```

## Final answer (scenario ends at the approval question)
```
Product: HomeHub FR-560 (fridge), bought 10 Jan 2022 at HomeHub Appliances
Coverage: Unclear. General warranty: 10 Jan 2022 + 1 year = ended 10 Jan 2023. Would be partly covered (compressor and sealed system, to 10 Jan 2027) once the serial is confirmed: the registration says HH56-2201-30847, the plate photo says HH56-2201-30647. Please read the plate inside the fridge.
Safety first: "Unplug before cleaning the condenser coils." (manual page 3)
Try this (manual section 4, page 6):
  1. Check the plug is seated, the outlet works, and the breaker.
  2. Set the fridge to 37 F and the freezer to 0 F. Wait 24 hours.
  3. Close the doors fully, do not block vents, remove ice buildup.
  4. Unplug and vacuum the condenser coils at the base or rear.
  Technician only: 5. If the condenser fan is silent, call service. 6. If the compressor does not run or clicks repeatedly, call service. Do not attempt repair.
  Allow 24 hours after any change. Discard perishables above 40 F for more than 2 hours.
Claim: draft ready for service@homehub-care.example (or 1-800-555-0123). Which of these steps have you already tried? Say yes to save the draft to your NAS, or no.
Evidence:
  - Documents/Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf: purchase 10 Jan 2022, FR-560, serial HH56-2201-30847
  - Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf: 1 year general, 5 years compressor and sealed system, registered serial HH56-2201-30847, claim contact
  - Photos/Phone/2022-01/IMG_20220115_101233.jpg: rating plate FR-560, serial HH56-2201-30647
  - Home/Appliances/Fridge/FR-560_owner_manual.pdf: not-cooling steps, safety
Notes: Serial mismatch: plate HH56-2201-30647 vs receipt and registration HH56-2201-30847. The claim procedure says the serial must match the registration. Exclusions include food loss and unauthorized repair.
```

Status: `waiting_approval`.

Delegations: 11 (photo-agent 2, file-agent 3, document-agent 6).

## Check against expected
Unclear, general ended 2023-01-10, partly covered to 2027-01-10 once serial confirmed (30847 vs 30647), not-cooling steps, draft with plate value marked to check. PASS.
