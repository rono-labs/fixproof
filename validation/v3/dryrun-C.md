# Dry run C: "The fridge stopped cooling."

Today 2026-11-20 08:40. Paths relative to `project/testdata/home-library/`. Mode: fault. Product: fridge. Symptom: "not cooling". No code from the user.

## D1 photo-agent (Step 0)
Instruction: `Search photos taken in the last 48 hours, up to 2026-11-20 08:40, for pictures of an appliance control panel or display showing an error code, or of an appliance rating plate or serial label. For each photo found, run text recognition and return the photo path, the time taken and the recognised text. If there are no results, say zero matches.`
Result: 1 photo, `Photos/Phone/2026-11/IMG_20261120_083012.jpg`, 2026-11-20 08:30:12, text "NORDVIK  E15  POWER  CYCLE  DELAY  START".

Parent, applying the skill literally: the text shows an error code and a brand, the user named no brand, and the text names no product type, so nothing disqualifies it. Tentatively take brand Nordvik and code E15. (This is wrong for a fridge; see defects. The skill gives no way to catch it at this point.)

## D2 file-agent (Step 1, names)
Instruction: `Find files whose names contain any of: receipt, invoice, order, purchase, quittung, Nordvik, fridge. Search folders whose names contain Receipts, Invoices, Purchases, Orders, Documents, Scans or Downloads first, then all user files. File types: documents and images. Return full path, file name, type, size and modified date for each, up to 50. If there are no results, say zero matches.`
Result, 10 files: the five Receipts PDFs (2019 dishwasher, 2022 fridge, 2024 dishwasher, 2025 TV, 2025 soundbar), Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf, Home/Appliances/Fridge/FR-560_owner_manual.pdf, Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf (the two Fridge files match the folder name), Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf, Manuals/Nordvik_ADW-48xx_UserManual.pdf.

## D3 photo-agent (Step 1)
Instruction: `Search the photo library for photos of a paper receipt or till slip, and for photos of an appliance rating plate or serial label, that mention fridge or Nordvik. For each photo found, run text recognition and return the photo path, the date taken, whether it is a receipt or a rating plate, and the recognised text. If there are no results, say zero matches.`
Result, 3 photos (the fridge plate shows "REFRIGERANT" and a compressor line, so a semantic search ranks it; a literal word match on "fridge" would miss it):
1. `Photos/Phone/2022-01/IMG_20220115_101233.jpg`, 2022-01-15 10:12:33, rating plate: "HomeHub MODEL: FR-560 SERIAL: HH56-2201-30647 VOLTS 115V 60Hz AMPS 6.5 REFRIGERANT R600a 38 g MADE FOR HomeHub Appliances Compressor: sealed system".
2. `Photos/Phone/2024-03/IMG_20240316_190455.jpg`, 2024-03-16, plate: "NORDVIK MODEL: ADW-4820 SERIAL: NV48-2203-1187 ...".
3. `Photos/Phone/2023-06/IMG_20230602_181404.jpg`, 2023-06-02, receipt: Nordvik WM-7 washer, HomeHub order HH-230602-1187.

Parent: photos 2 and 3 name other products, no match. Photo 1 is the fridge plate, brand HomeHub, model FR-560, serial HH56-2201-30647.

## D4 document-agent (Step 1, extract)
Only the fridge receipt is not named for another product.
Instruction: `Extract purchase details with the receipt schema from these files: Documents/Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf. If a file returns no data with the receipt schema, try the invoice schema. For each file return store, order number, purchase date exactly as printed, product description, brand, model number, serial number if printed, price, and every other line item, especially any protection plan, extended warranty or care plan with its plan number and term. Report any file you could not read.`
Result: HomeHub Appliances, order HH-220110-3318, 2022-01-10, HomeHub FR-560 French Door Refrigerator (Stainless, 25 cu ft), serial HH56-2201-30847, $1,649.00; Delivery and setup $79.00; total $1,728.00; no protection plan.

Parent: the E15 photo names Nordvik, but the only fridge on the NAS is HomeHub. The photo is therefore a different brand and is dropped, along with code E15 (retroactive application of the Step 0 filter; the skill does not say to re-check). One purchase of this product, no disambiguation. Series: FR-560 has 3 digits, so none.

## D5 file-agent (Step 2)
Instruction: `Find files whose names contain any of: warranty, guarantee, garantie, protection, plan, care, extended, registration, certificate, terms, conditions, HomeHub, FR-560. Search folders whose names contain Warranty, Receipts, Scans, Documents, Home or Appliances first, then all user files. File types: documents and images. Return full path, file name, size and modified date for each, up to 50. If there are no results, say zero matches.`
Result, 7 files: Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf, Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf, Home/Appliances/Fridge/FR-560_owner_manual.pdf, Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf, Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf, Scans/2024/Brightline_EPP_terms_scan.pdf, Scans/Lumora_TV_warranty.pdf. (Receipt lists no plan, so no Scans listing.)

## D6 document-agent (Step 2, confirm)
Instruction: `With intent locate_content and evidence mode focused, check these files: [the 7 paths above]. List only the files that are a warranty, guarantee, protection plan or warranty registration for HomeHub FR-560, or a plan bought with order HH-220110-3318. For each, quote the line that shows it. If none match, say zero matches.`
Result: 1 match, Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf: "LIMITED WARRANTY CARD / Product: FR-560 Refrigerator" and "Registered serial no.: HH56-2201-30847".

## D7 document-agent (Step 2, terms)
Instruction: `Answer from these files only: Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf. With intent period and answer mode table, return for each document: the provider, each coverage (full parts and labour, parts only, or named components such as motor, compressor or panel) with its term, how the start date is defined, and any printed start or end date. With intent condition, return the exclusions and the claim procedure (phone, email or web form exactly as written, required attachments). Also return any plan number, registration number and serial number written on it. Quote the page or section for each answer.`
Result (p.1): HomeHub. General parts and labor 1 year "from the original purchase date". Sealed system / compressor 5 years (compressor, condenser, evaporator, refrigerant lines; parts and labor in years 1-5), no separate start rule. Printed: registered purchase date 2022-01-10, registered owner Alex Rivera, registered serial HH56-2201-30847. Exclusions: food loss, damage from power outage, water filters, door bins, cosmetic damage, unauthorized repair. Claims: "Email service@homehub-care.example or call 1-800-555-0123"; receipt, registration and photo of the serial plate; "The serial must match the registration."

## D8 document-agent (Step 3, reconcile)
Instruction: `Reconcile these files and report every difference in brand, model number, serial number, purchase date, plan start or end date, or owner name: Documents/Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf, Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf. For each difference give both values and the file each came from. If they all agree, say no differences found.`
Result: no differences found (FR-560, serial HH56-2201-30847, 2022-01-10, Alex Rivera).

Parent plate check: plate photo reads HH56-2201-30647, receipt and registration read HH56-2201-30847. One character differs (30647 vs 30847). Cross-check rule: Unclear.
Dates: general warranty 2022-01-10 + 1 year = ended 2023-01-10. Sealed system 2022-01-10 + 5 years = 2027-01-10, active (no separate start rule, so purchase date; the registration prints the same date). Not cooling may or may not be the compressor. Would be Partly covered, but the serial mismatch makes the label Unclear: "Would be partly covered (sealed system and compressor, to 10 Jan 2027) once the serial is confirmed."

## D9 file-agent (Step 4)
Instruction: `Find files whose names contain any of: manual, guide, instructions, handbook, quick start, FR-560, HomeHub. Search folders whose names contain Manuals, Documents, Downloads, Home or Appliances first, then all user files. File type: documents. Return full path, file name, size and modified date, up to 20. If there are no results, say zero matches.`
Result, 7 files: Documents/Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf, Downloads/ADW-48xx_manual (1).pdf, Home/Appliances/Fridge/FR-560_owner_manual.pdf, Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf, Home/Appliances/Washer/WM-7_manual.pdf, Manuals/Nordvik_ADW-48xx_UserManual.pdf, Manuals/Zentro_AX3000_Router_Manual.pdf.

## D10 document-agent (Step 4, confirm manual; wording adapted)
Instruction: `With intent locate_content and evidence mode focused, check these files: [the 7 paths above]. List only the files that are the user manual for HomeHub FR-560. For each, quote the line that shows it. If none match, say zero matches.`
Result: 1 match, Home/Appliances/Fridge/FR-560_owner_manual.pdf: "HomeHub French Door Refrigerator / Model series FR-560". No duplicate check needed.

## D11 document-agent (Step 4, manual)
No code (E15 dropped), so only the symptom.
Instruction: `Using only Home/Appliances/Fridge/FR-560_owner_manual.pdf, with intent locate_content and answer mode table, find what the manual says about the symptom "not cooling". Return the matching rows of the error-code and troubleshooting tables (problem, cause, what to do) in the order printed, the safety warnings that apply to those steps, any steps that need a qualified technician, and any statement that user repairs affect the warranty. Give the page or section for each item.`
Result: s.4 p.6, 6 steps in order: 1 Power (plug seated, outlet works, breaker); 2 Temperature setting (fridge 37 F, freezer 0 F, wait 24 hours); 3 Door seals and airflow (close doors fully, do not block vents, remove ice buildup); 4 Condenser coils (unplug, vacuum coils at base or rear); 5 Condenser fan (listen; if silent, call service); 6 Compressor (does not run or clicks repeatedly: call service, "Do not attempt repair"). "Allow 24 hours after any change. Food safety: discard perishables above 40 F for more than 2 hours." Safety (s.1 p.3): "Unplug before cleaning the condenser coils." No statement that user repairs affect the warranty (s.5 p.7 only says compressor and sealed system carry an extended warranty).

## Reply (status waiting_approval)

```
Product: HomeHub FR-560 (fridge), bought 10 Jan 2022 at HomeHub Appliances
Coverage: Unclear. The 1-year general warranty ended 10 Jan 2023. The 5-year sealed system and compressor warranty runs to 10 Jan 2027, but the serial on your plate photo (HH56-2201-30647) differs from the registered serial (HH56-2201-30847). Would be partly covered (sealed system and compressor, to 10 Jan 2027, if the technician confirms a compressor or sealed-system fault) once the serial is confirmed. Please read the plate on the fridge.
Safety first: Unplug before cleaning the condenser coils. Food safety: discard perishables above 40 F for more than 2 hours. (manual s.1 p.3, s.4 p.6)
Try this (manual s.4 p.6), allow 24 hours after any change:
  1. Check the plug is seated, the outlet works and the breaker is on.
  2. Set fridge to 37 F and freezer to 0 F, wait 24 hours.
  3. Close doors fully, do not block vents, remove ice buildup.
  4. Unplug and vacuum the condenser coils at the base or rear.
  Technician only: condenser fan silent (call service); compressor not running or clicking (call service, do not attempt repair). Unauthorized repair is a warranty exclusion on the card.
Claim: draft ready for Email service@homehub-care.example or call 1-800-555-0123.

To: Email service@homehub-care.example or call 1-800-555-0123
Subject: Warranty claim, HomeHub FR-560, serial HH56-2201-30647
Product: HomeHub FR-560, serial HH56-2201-30647 (plate photo; registered serial HH56-2201-30847, to be checked)
Purchased: 2022-01-10 at HomeHub Appliances, order HH-220110-3318
Coverage: HomeHub limited warranty, sealed system and compressor 5 years, valid until 2027-01-10 (subject to the serial check)
Fault: not cooling, no error code
Already tried: none confirmed
Attachments: Documents/Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf, Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf, Photos/Phone/2022-01/IMG_20220115_101233.jpg
Contact: (blank)

Which of the steps above have you already tried? Then say yes to save this draft to your NAS, or no.
Evidence:
  - Documents/Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf: purchase date, model, serial HH56-2201-30847, order, price
  - Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf: terms 1 year and 5 years sealed system, exclusions, claim contact, registered serial
  - Photos/Phone/2022-01/IMG_20220115_101233.jpg: plate, model FR-560, serial HH56-2201-30647
  - Home/Appliances/Fridge/FR-560_owner_manual.pdf: not-cooling steps
Notes: Serial mismatch: plate photo HH56-2201-30647 vs receipt and registration HH56-2201-30847 (third digit of the last group, 6 vs 8). The card says the serial must match the registration. Exclusions: food loss, power outage damage, unauthorized repair. Today's photo (IMG_20261120_083012.jpg, Nordvik, E15) belongs to another appliance and was not used.
```

Status: waiting_approval. Delegations: 11 (photo 2, file 3, document 6).
