# Dry run C: "The fridge stopped cooling."

Today 2026-11-20 08:40. Paths relative to project/testdata/home-library/. Mode: fault. Product: fridge. Symptom: "not cooling". No code, brand or model from the user. No user follow-up is given, so the run ends at waiting_approval.

## Step 0

DELEGATE photo-agent:
'Search photos taken in the last 48 hours, up to 2026-11-20 08:40, for pictures of an appliance control panel or display showing an error code, or of an appliance rating plate or serial label. If the search cannot filter by time, take the 20 newest photos instead. For each photo found, up to 20, run text recognition and return the photo path, the time taken, the recognised text, and which kind of appliance the photo shows. If there are no results, say zero matches.'

Result: 1 photo, IMG_20261120_083012.jpg, EXIF 2026-11-20 08:30:12, "NORDVIK", "E15", POWER/CYCLE/DELAY/START; appliance kind not visible.
Parent: the kind does not positively match "fridge" and the brand Nordvik would send every later search to the wrong brand, so the photo is ignored. (D1: the skill gives no rule for a photo whose kind is not visible.)

## Step 1

DELEGATE file-agent:
'Find files whose names contain any of: receipt, invoice, order, purchase, quittung, fridge. Search folders whose names contain Receipts, Invoices, Purchases, Orders, Documents, Scans or Downloads first, then all user files. File types: documents and images. Return full path, file name, type, size and modified date for each, up to 50. If there are no results, say zero matches.'
Result, 5 files: the five Receipts-folder PDFs (2019 dishwasher, HomeHub_receipt_fridge_Jan2022, 2024 dishwasher, order_TV_Lumora, soundbar). Only Documents/Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf names a fridge.

DELEGATE photo-agent:
'Search the photo library for photos of a paper receipt or till slip that mention fridge, and for photos of any appliance rating plate or serial label. Newest first, up to 20 of each. For each photo found, run text recognition and return the photo path, the date taken, whether it is a receipt or a rating plate, and the recognised text. If there are no results, say zero matches.'
Result: no receipt mentions a fridge (the washer receipt photo is not returned). Plates: IMG_20240316_190455.jpg (taken 2024-03-16 19:04:55): "NORDVIK MODEL: ADW-4820 SERIAL: NV48-2203-1187 ..."; IMG_20220115_101233.jpg (taken 2022-01-15 10:12:33): "HomeHub MODEL: FR-560 SERIAL: HH56-2201-30647 VOLTS 115V 60Hz AMPS 6.5 REFRIGERANT R600a 38 g MADE FOR HomeHub Appliances Compressor: sealed system".

DELEGATE document-agent (only the fridge-named receipt):
'Extract purchase details with the receipt schema from these files: Documents/Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf. If a file returns no data with the receipt schema, try the invoice schema. For each file return store, order number, purchase date exactly as printed, product description, brand, model number, serial number if printed, price, and every other line item, especially any protection plan, extended warranty or care plan with its plan number and term. Report any file you could not read.'
Result: HomeHub Appliances; order HH-220110-3318; 2022-01-10; "HomeHub FR-560 French Door Refrigerator, Stainless, 25 cu ft"; brand HomeHub; model FR-560; serial HH56-2201-30847; $1,649.00; other line: delivery and setup $79.00; no protection plan.

Parent: plate model FR-560 matches the receipt model, so the FR-560 plate is kept (ADW-4820 plate ignored). The plate serial HH56-2201-30647 differs from the receipt serial HH56-2201-30847 (checked in Step 3). Only one fridge purchase. (The keep rule is written before the extraction runs, so the match was done after it; defect D8.)

## Step 2

Series: FR-560 has three digits, so left out.

DELEGATE file-agent:
'Find files whose names contain any of: warranty, guarantee, garantie, protection, plan, care, extended, registration, certificate, terms, conditions, HomeHub, FR-560. Search folders whose names contain Warranty, Receipts, Scans, Documents, Home or Appliances first, then all user files. File types: documents and images. Return full path, file name, size and modified date for each, up to 50. If there are no results, say zero matches.'
Result: Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf; Home/Appliances/Fridge/FR-560_owner_manual.pdf; Documents/Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf; Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf; Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf; Scans/Lumora_TV_warranty.pdf; Scans/2024/Brightline_EPP_terms_scan.pdf.
(The scan-folder fallback is not needed: the receipt has no plan.) Note: the template has {store} too; the store HomeHub is already in the list.

DELEGATE document-agent:
'With intent locate_content and evidence mode focused, check these files: Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf, Home/Appliances/Fridge/FR-560_owner_manual.pdf, Documents/Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf, Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf, Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf, Scans/Lumora_TV_warranty.pdf, Scans/2024/Brightline_EPP_terms_scan.pdf. List only the files that are a warranty, guarantee, protection plan or warranty registration for HomeHub FR-560, or a plan bought with order HH-220110-3318. For each, quote the line that shows it. If none match, say zero matches.'
Result: 1 file: HomeHub_FR-560_warranty_registration.pdf, "Product: FR-560 Refrigerator", "Registered serial no.: HH56-2201-30847. Registered owner: Alex Rivera. Purchase date: 2022-01-10."

DELEGATE document-agent:
'Answer from these files only: Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf. With intent period and answer mode table, return for each document: the provider, each coverage (full parts and labour, parts only, or named components such as motor, compressor or panel) with its term, how the start date is defined, and any printed start or end date. With intent condition, return the exclusions and the claim procedure (phone, email or web form exactly as written, required attachments). Also return any plan number, registration number and serial number written on it. Quote the page or section for each answer.'
Result (page 1): HomeHub; general parts and labor 1 year from the original purchase date; sealed system/compressor 5 years, "compressor, condenser, evaporator and refrigerant lines (parts and labor in years 1-5)"; printed purchase date 2022-01-10, no printed end date. Exclusions: food loss, damage from power outage, water filters, door bins, cosmetic damage, unauthorized repair. Claim: "Email service@homehub-care.example or call 1-800-555-0123"; claims require receipt, registration and a photo of the serial plate; "The serial must match the registration." Registered serial HH56-2201-30847; no registration number.

## Step 3

DELEGATE document-agent:
'Reconcile these files and report every difference in brand, model number, serial number, purchase date, plan start or end date, or owner name: Documents/Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf, Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf. For each difference give both values and the file each came from. If they all agree, say no differences found.'
Result: no differences found (HomeHub, FR-560, HH56-2201-30847, 2022-01-10, Alex Rivera).
Parent: plate photo reads HH56-2201-30647 against 30847 on the receipt and registration. Mismatch in the last digits.

Arithmetic: bought 10 Jan 2022 + 1 year general = ended 10 Jan 2023. Compressor and sealed system + 5 years = 10 Jan 2027, active. Not cooling may or may not be the sealed system. The serial mismatch forces Unclear: "would be partly covered (compressor and sealed system, to 10 Jan 2027) once the serial is confirmed".

## Step 4

DELEGATE file-agent:
'Find files whose names contain any of: manual, guide, instructions, handbook, quick start, FR-560, HomeHub. Search folders whose names contain Manuals, Documents, Downloads, Home or Appliances first, then all user files. File type: documents. Return full path, file name, size and modified date, up to 20. If there are no results, say zero matches.'
Result: Home/Appliances/Fridge/FR-560_owner_manual.pdf (9127); Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf; Documents/Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf; and the other manuals by "manual" (Zentro, ADW x2, WM-7).
Parent: named both as a manual and with the model: FR-560_owner_manual.pdf.

DELEGATE document-agent:
'With intent locate_content, check these files: Home/Appliances/Fridge/FR-560_owner_manual.pdf. List only the files that are the user manual or guide for HomeHub FR-560, and quote the line that shows it. If none match, say zero matches.'
Result: confirmed, "HomeHub French Door Refrigerator, Model series FR-560, User Manual and Care Guide".

DELEGATE document-agent:
'Using only Home/Appliances/Fridge/FR-560_owner_manual.pdf, with intent locate_content and answer mode table, find what the manual says about the symptom "not cooling". Return the matching rows of the error-code and troubleshooting tables (problem, cause, what to do) in the order printed, the safety warnings that apply to those steps, any steps that need a qualified technician, and any statement that user repairs affect the warranty. Give the page or section for each item.'
(No error code, so the code part of the template is left out.)
Result: Section 4 "Troubleshooting: not cooling", p.6, steps in order: 1 power (plug, outlet, breaker); 2 temperature setting (fridge 37 F, freezer 0 F, wait 24 hours); 3 door seals and airflow (close doors, do not block vents, remove ice); 4 condenser coils (unplug, vacuum at base or rear); 5 condenser fan (listen; if silent, call service); 6 compressor (does not run or clicks repeatedly: call service, do not attempt repair). "Allow 24 hours after any change. Food safety: discard perishables above 40 F for more than 2 hours." Safety p.3: "Unplug before cleaning the condenser coils." Technician: steps 5 and 6. No statement on user repairs affecting the warranty (p.7 only says the compressor and sealed system carry an extended warranty).

## Step 5 (status waiting_approval)

Draft (the plate serial is used, the registered one beside it, marked to be checked):

    To: Email service@homehub-care.example or call 1-800-555-0123
    Subject: Warranty claim, HomeHub FR-560, serial HH56-2201-30647 (plate; registered HH56-2201-30847, to be checked)
    Product: HomeHub FR-560, serial HH56-2201-30647 (plate; registered HH56-2201-30847, to be checked)
    Purchased: 2022-01-10 at HomeHub Appliances, order HH-220110-3318
    Coverage: HomeHub limited warranty, sealed system/compressor 5 years, valid until 2027-01-10, once the serial is confirmed
    Fault: fridge stopped cooling, error code none
    Already tried: none confirmed
    Attachments: Documents/Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf, Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf, Photos/Phone/2022-01/IMG_20220115_101233.jpg
    Contact:

Question asked: "Which of these steps have you already tried? Say yes to save the draft to your NAS, or no." No reply in this scenario, so nothing is saved.

## Final answer (status waiting_approval)

    Product: HomeHub FR-560 (fridge), bought 10 Jan 2022 at HomeHub Appliances
    Coverage: Unclear. General warranty ended 10 Jan 2023. It would be partly covered (compressor and sealed system, to 10 Jan 2027) once the serial is confirmed: the registration and receipt say HH56-2201-30847, the plate photo says HH56-2201-30647.
    Safety first: Unplug before cleaning the condenser coils (manual p.3). Discard perishables above 40 F for more than 2 hours.
    Try this (manual section 4, p.6):
      1. Check the plug, outlet and breaker.
      2. Set fridge 37 F and freezer 0 F; wait 24 hours.
      3. Close doors fully, keep vents clear, remove ice buildup.
      4. Unplug and vacuum the condenser coils at the base or rear.
      Technician only: 5. Condenser fan silent: call service. 6. Compressor not running or clicking: call service, do not attempt repair.
    Claim: draft ready for service@homehub-care.example or 1-800-555-0123 (serial marked to be checked). Which of these steps have you already tried? Say yes to save the draft to your NAS, or no.
    Evidence:
      - Documents/Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf: 2022-01-10, FR-560, serial HH56-2201-30847
      - Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf: 1 year general, 5 years sealed system, registered serial, claim contact
      - Photos/Phone/2022-01/IMG_20220115_101233.jpg: plate FR-560, serial HH56-2201-30647
      - Home/Appliances/Fridge/FR-560_owner_manual.pdf: not cooling steps
    Notes: Serial mismatch between the plate photo and the receipt and registration; the claim procedure says the serial must match the registration, so please read the plate again. The recent E15 photo of a Nordvik panel was ignored.

Delegations: 11 = photo-agent 2, file-agent 3, document-agent 6 (extract, locate, terms, reconcile, manual confirm, manual query). No knowledge-agent call yet.
