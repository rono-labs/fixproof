# Dry run C: "The fridge stopped cooling."

Today 2026-11-20 08:40. Paths are relative to the library root; all files modified 2026-10-29. Skill followed literally.

## Intake
Mode: fault. Product: fridge (short names: refrigerator, FR). Symptom: "not cooling". No code, brand or model given.

## Step 0
### Delegation 1 to photo-agent
Instruction as sent:
> Search photos taken in the last 48 hours, up to 2026-11-20 08:40, for pictures of an appliance control panel or display showing an error code, or of an appliance rating plate or serial label. If the search cannot filter by time, take the 20 newest photos instead. For each photo found, up to 20, run text recognition and return the photo path, the time taken, the recognised text, and which kind of appliance the photo shows. If there are no results, say zero matches.

Result (photo-agent played from the real image):
1 match: Photos/Phone/2026-11/IMG_20261120_083012.jpg, taken 2026-11-20 08:30:12. Text: "NORDVIK", "E15", buttons POWER, CYCLE, DELAY, START. Appliance type not visible.

Parent: display only, but the user's words ("stopped cooling") do not point to it. Ignored: no brand, no code.

## Step 1
### Delegation 2 to file-agent
Instruction as sent:
> Find files whose names contain any of: receipt, invoice, order, purchase, quittung, fridge, refrigerator, FR. Search folders whose names contain Receipts, Invoices, Purchases, Orders, Documents, Scans or Downloads first, then all user files. File types: documents and images. Return full path, file name, type, size and modified date for each, up to 50. If there are no results, say zero matches.

Result (file-agent):
6 matches: Documents/Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf (2733); Documents/Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf (2969); Documents/Receipts/2019/receipt_dishwasher_old.pdf (2794); Documents/Receipts/2025/Brightline_order_TV_Lumora.pdf (2762); Home/Appliances/Fridge/FR-560_owner_manual.pdf (9127); Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf (2737).

### Delegation 3 to photo-agent
Instruction as sent:
> Search the photo library for photos of a paper receipt or till slip that mention fridge, refrigerator, FR, and for photos of any appliance rating plate or serial label. Newest first, up to 20 of each. For each photo found, run text recognition and return the photo path, the date taken, whether it is a receipt or a rating plate, and the recognised text. If there are no results, say zero matches.

Result (photo-agent):
2 photos, both rating plates, no fridge receipt photo (the one receipt photo is for a washer).
  - Rating plate: Photos/Phone/2024-03/IMG_20240316_190455.jpg, 2024-03-16 19:04:55. NORDVIK / MODEL: ADW-4820 / SERIAL: NV48-2203-1187 / 120V 60Hz 15A 1800W / MFD 2023-12.
  - Rating plate: Photos/Phone/2022-01/IMG_20220115_101233.jpg, 2022-01-15 10:12:33. HomeHub / MODEL: FR-560 / SERIAL: HH56-2201-30647 / VOLTS 115V 60Hz AMPS 6.5 / REFRIGERANT R600a 38 g / MADE FOR HomeHub Appliances / Compressor: sealed system.

Parent: PDFs named for a dishwasher or a TV are dropped; only the fridge receipt remains.

### Delegation 4 to document-agent
Instruction as sent:
> Extract purchase details with the receipt schema from these files: Documents/Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf. If a file returns no data with the receipt schema, try the invoice schema. For each file return store, order number, purchase date exactly as printed, product description, brand, model number, serial number if printed, price, any warranty term printed on the receipt, and every other line item, especially any protection plan, extended warranty or care plan with its plan number and term. Report any file you could not read.

Result (document-agent): HomeHub Appliances; order HH-220110-3318; date 2022-01-10; "HomeHub FR-560 French Door Refrigerator", Stainless, 25 cu ft; brand HomeHub; model FR-560; serial HH56-2201-30847; $1,649.00; no warranty term printed; other line: Delivery and setup $79.00; no protection plan. Total $1,728.00. File read.

Parent: rating plate FR-560 matches the receipt model, kept (serial HH56-2201-30647). The ADW-4820 plate matches nothing for a fridge, ignored. Series: FR-560 has fewer than four digits, so no series.

## Step 2
### Delegation 5 to file-agent
Instruction as sent:
> Find files whose names contain any of: warranty, guarantee, garantie, protection, plan, care, extended, registration, certificate, terms, conditions, HomeHub, FR-560. Search folders whose names contain Warranty, Receipts, Scans, Documents, Home or Appliances first, then all user files. File types: documents and images. Return full path, file name, size and modified date for each, up to 50. If there are no results, say zero matches.

(brand and store are both HomeHub, written once; no series.)

Result (file-agent): 7 matches: Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf (2737); Documents/Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf (2733); Home/Appliances/Fridge/FR-560_owner_manual.pdf (9127); Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf (2960); Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf (2681); Scans/Lumora_TV_warranty.pdf (2560); Scans/2024/Brightline_EPP_terms_scan.pdf (3271).

Parent: no plan on the receipt, so no Scans listing. Candidates for content check: the registration and the plan scan (names no product).

### Delegation 6 to document-agent
Instruction as sent:
> With intent locate_content and evidence mode focused, check these files: Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf, Scans/2024/Brightline_EPP_terms_scan.pdf. List only the files that are a warranty, guarantee, protection plan or warranty registration for HomeHub FR-560, or a plan bought with order HH-220110-3318. For each, quote the line that shows it. If none match, say zero matches.

Result (document-agent): 1 match, HomeHub_FR-560_warranty_registration.pdf: "Product: FR-560 Refrigerator" and "Registered serial no.: HH56-2201-30847". The plan scan is for a Nordvik ADW-4820 dishwasher, no match.

### Delegation 7 to document-agent
Instruction as sent:
> Answer from these files only: Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf. With intent period and answer mode table, return for each document: the provider, each coverage (full parts and labour, parts only, or named components such as motor, compressor or panel) with its term, how the start date is defined, and any printed start or end date. With intent condition, return the exclusions and the claim procedure (phone, email or web form exactly as written, required attachments). Also return any plan number, registration number and serial number written on it. Quote the page or section for each answer.

Result (document-agent): HomeHub, page 1. General parts and labor 1 year, "from the original purchase date". Sealed system / compressor 5 years: "Compressor, condenser, evaporator and refrigerant lines (parts and labor in years 1-5)". Printed in the terms: "Registered serial no.: HH56-2201-30847. Registered owner: Alex Rivera. Purchase date: 2022-01-10." No printed end date. Exclusions: "food loss, damage from power outage, water filters, door bins, cosmetic damage, unauthorized repair". Claim: "Email service@homehub-care.example or call 1-800-555-0123." Required: receipt, registration and a photo of the serial plate; "The serial must match the registration." No registration number as such.

## Step 3
### Delegation 8 to document-agent
Instruction as sent:
> Reconcile these files and report every difference in brand, model number, serial number, purchase date, plan start or end date, or owner name: Documents/Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf, Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf. For each difference give both values and the file each came from. If they all agree, say no differences found.

Result (document-agent): No differences found. Model FR-560, serial HH56-2201-30847, purchase date 2022-01-10 and owner Alex Rivera agree.

Parent compares the plate photo myself: plate HH56-2201-30647, registered and receipt HH56-2201-30847. One character differs (30647 vs 30847): serial mismatch. Rule: Unclear.
Arithmetic: general 1 year from 10 Jan 2022 = ended 10 Jan 2023. Sealed system and compressor 5 years = 10 Jan 2027, active (51 days left). It would be partly covered once the serial is confirmed. Label: Unclear.

## Step 4
### Delegation 9 to file-agent
Instruction as sent:
> Find files whose names contain any of: manual, guide, instructions, handbook, quick start, FR-560, HomeHub. Search folders whose names contain Manuals, Documents, Downloads, Home or Appliances first, then all user files. File type: documents. Return full path, file name, size and modified date, up to 20. If there are no results, say zero matches.

Result (file-agent): 7 matches: Home/Appliances/Fridge/FR-560_owner_manual.pdf (9127); Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf (2737); Documents/Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf (2733); Manuals/Nordvik_ADW-48xx_UserManual.pdf (17516); Downloads/ADW-48xx_manual (1).pdf (17516); Home/Appliances/Washer/WM-7_manual.pdf (9774); Manuals/Zentro_AX3000_Router_Manual.pdf (6029).

Parent: named both as a manual and with brand or model: FR-560_owner_manual.pdf only.

### Delegation 10 to document-agent
Instruction as sent:
> With intent locate_content, check these files: Home/Appliances/Fridge/FR-560_owner_manual.pdf. List only the files that are the user manual or guide for HomeHub FR-560, and quote the line that shows it. If none match, say zero matches.

Result (document-agent): 1 match: "HomeHub French Door Refrigerator  Model series FR-560  User Manual and Care Guide" (page 1).

### Delegation 11 to document-agent
Instruction as sent:
> Using only Home/Appliances/Fridge/FR-560_owner_manual.pdf, with intent locate_content and answer mode table, find what the manual says about the symptom "not cooling". Return the matching rows of the error-code and troubleshooting tables (problem, cause, what to do) in the order printed, the safety warnings that apply to those steps, any steps that need a qualified technician, and any statement that user repairs affect the warranty. Give the page or section for each item.

(no error code, so that part is left out.)

Result (document-agent): Section 4 "Troubleshooting: not cooling", page 6, in order: 1 Power: plug seated, outlet works, check breaker. 2 Temperature setting: fridge 37 F, freezer 0 F, wait 24 hours. 3 Door seals and airflow: close doors fully, do not block vents, remove ice buildup. 4 Condenser coils: unplug, vacuum the coils at the base or rear. 5 Condenser fan: listen for the fan; if silent, call service. 6 Compressor: if it does not run or clicks repeatedly, call service, "Do not attempt repair." Also "Allow 24 hours after any change. Food safety: discard perishables above 40 F for more than 2 hours." Safety (page 3): "Unplug before cleaning the condenser coils." "Disconnect power before any cleaning near electrical parts." Technician: steps 5 and 6. Warranty statement (page 7): "The compressor and sealed system carry an extended warranty. See the warranty card and register your serial number." No statement on user repairs in the manual.

## Step 5
Label Unclear, so a draft is composed. Contact is the registration's. Serial: plate value, registered value beside it, marked to check.

```
To: Email service@homehub-care.example or call 1-800-555-0123
Subject: Warranty claim, HomeHub FR-560, serial HH56-2201-30647 (to be checked)
Product: HomeHub FR-560, serial HH56-2201-30647 on the rating plate (registered serial HH56-2201-30847, to be checked)
Purchased: 10 Jan 2022 at HomeHub Appliances, order HH-220110-3318
Coverage: HomeHub warranty registration, sealed system / compressor 5 years, valid until 10 Jan 2027 (subject to the serial check)
Fault: fridge stopped cooling, error code none
Already tried: none confirmed
Attachments: Documents/Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf, Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf, Photos/Phone/2022-01/IMG_20220115_101233.jpg
Contact: (left blank for you to fill in)
```

Question asked: "Which of these steps have you already tried? Say yes to save the draft to your NAS, or no." Status `waiting_approval`. The scenario ends here (no user reply, nothing saved).

## Final answer

```
Product: HomeHub FR-560 (fridge), bought 10 Jan 2022 at HomeHub Appliances
Coverage: Unclear. General warranty (1 year) ended 10 Jan 2023. It would be partly covered (compressor and sealed system, to 10 Jan 2027, 51 days left) once the serial is confirmed: the registration and receipt say HH56-2201-30847, the plate photo says HH56-2201-30647. Please read the number on the plate. Not cooling may or may not be a compressor or sealed-system fault.
Safety first: Unplug the fridge before cleaning the condenser coils (manual page 3). Food safety: discard perishables above 40 F for more than 2 hours.
Try this (manual section 4 "Troubleshooting: not cooling", page 6; allow 24 hours after any change):
  1. Check the plug is seated, the outlet works and the breaker is on.
  2. Set the fridge to 37 F and the freezer to 0 F, then wait 24 hours.
  3. Close the doors fully, keep vents clear and remove ice buildup.
  4. Unplug, then vacuum the condenser coils at the base or rear.
  5. Listen for the condenser fan. If it is silent, call service.
  6. If the compressor does not run or clicks repeatedly, call service. Do not attempt repair.
  Technician only: steps 5 and 6.
Claim: draft ready for Email service@homehub-care.example or call 1-800-555-0123. Which of these steps have you already tried? Say yes to save the draft to your NAS, or no.
Evidence:
  - Documents/Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf: purchase 10 Jan 2022, FR-560, serial HH56-2201-30847, order HH-220110-3318
  - Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf: 1 year general, 5 years compressor and sealed system, exclusions, claim contact, registered serial
  - Photos/Phone/2022-01/IMG_20220115_101233.jpg: rating plate FR-560, serial HH56-2201-30647
  - Home/Appliances/Fridge/FR-560_owner_manual.pdf: not-cooling steps (page 6)
Notes: Serial mismatch (registration and receipt 30847, plate 30647); the registration says the serial must match, so confirm it before claiming. The draft uses the plate value and marks it to check. Exclusions: food loss, power-outage damage and unauthorized repair are not covered. Draft not yet saved.
```

Status: `waiting_approval`

Delegations: 11 (photo-agent x2, file-agent x3, document-agent x6).
