# Dry run C: "The fridge stopped cooling."

Today = 2026-11-20 08:40. Intake: mode fault. Product fridge. Symptom "stopped cooling". No code.

## Step 0

delegate --target photo-agent --instruction 'Search photos taken in the last 48 hours, up to 2026-11-20 08:40, for pictures of an appliance control panel or display showing an error code, or of an appliance rating plate or serial label. For each photo found, run text recognition and return the photo path, the time taken and the recognised text. If there are no results, say zero matches.'

Result: 1 photo, `Photos/Phone/2026-11/IMG_20261120_083012.jpg`, 2026-11-20 08:30:12, text "NORDVIK E15 POWER CYCLE DELAY START".

Parent: no product type in the text, and the user has already named a fridge and a symptom. Nothing ties a Nordvik panel to the fridge. Treated as no match (D3). If the brand had been taken, `{brand}` would have been Nordvik, and every search below would have gone to the wrong manufacturer.

## Step 1

delegate --target file-agent --instruction 'Find files whose names contain any of: receipt, invoice, order, purchase, quittung, fridge. Search folders whose names contain Receipts, Invoices, Purchases, Orders, Documents, Scans or Downloads first, then all user files. File types: documents and images. Return full path, file name, type, size and modified date for each, up to 50. If there are no results, say zero matches.'

Result, 7 PDFs: the five in Documents/Receipts (2019 dishwasher, 2022 HomeHub fridge, 2024 dishwasher, 2025 TV order, 2025 soundbar), Home/Appliances/Fridge/FR-560_owner_manual.pdf, Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf.

delegate --target photo-agent --instruction 'Search the photo library for photos of a paper receipt or till slip that mention fridge. For each photo found, run text recognition and return the photo path, the date taken and the recognised text. If there are no results, say zero matches.'

Result: zero matches (the one receipt photo is a washer). The 2022 fridge rating plate photo is not a receipt and is not returned (D1).

delegate --target document-agent --instruction 'Extract purchase details with the receipt schema from these files: Documents/Receipts/2019/receipt_dishwasher_old.pdf, Documents/Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf, Documents/Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf, Documents/Receipts/2025/Brightline_order_TV_Lumora.pdf, Documents/Receipts/2025/Brightline_soundbar_2025-12-18.pdf. If a file returns no data with the receipt schema, try the invoice schema. For each file return store, order number, purchase date exactly as printed, product description, brand, model number, serial number if printed, price, and every other line item, especially any protection plan, extended warranty or care plan with its plan number and term. Report any file you could not read.'

Result: the fridge row: HomeHub Appliances, HH-220110-3318, 2022-01-10, HomeHub FR-560 French Door Refrigerator, serial HH56-2201-30847, $1,649.00; delivery and setup $79.00; no protection plan. The other four are other products.

One fridge purchase, no choice to make. Delegations so far: 4.

## Step 2

Series for FR-560: letters FR, first two digits 56, last replaced by x: FR-56x.

delegate --target file-agent --instruction 'Find files whose names contain any of: warranty, guarantee, garantie, protection, plan, care, extended, registration, certificate, HomeHub, FR-560, FR-56x. Search folders whose names contain Warranty, Receipts, Scans, Documents, Home or Appliances first, then all user files. File types: documents and images. Return full path, file name, size and modified date for each, up to 50. If there are no results, say zero matches.'

Result, 6 PDFs: Documents/Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf; Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf; Home/Appliances/Fridge/FR-560_owner_manual.pdf; Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf; Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf; Scans/Lumora_TV_warranty.pdf.

delegate --target document-agent --instruction 'With intent locate_content and evidence mode focused, check these files: Documents/Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf, Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf, Home/Appliances/Fridge/FR-560_owner_manual.pdf, Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf, Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf, Scans/Lumora_TV_warranty.pdf. List only the files that are a warranty, guarantee, protection plan or warranty registration for HomeHub FR-560 or the series FR-56x, or a plan bought with order HH-220110-3318. For each, quote the line that shows it. If none match, say zero matches.'

Result: 1 file. Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf: "LIMITED WARRANTY CARD / Product: FR-560 Refrigerator".

delegate --target document-agent --instruction 'Answer from these files only: Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf. With intent period and answer mode table, return for each document: the provider, each coverage (full parts and labour, parts only, or named components such as motor, compressor or panel) with its term, how the start date is defined, and any printed start or end date. With intent condition, return the exclusions and the claim procedure (phone, email or web form exactly as written, required attachments). Also return any plan number, registration number and serial number written on it. Quote the page or section for each answer.'

Result: HomeHub. General parts and labor 1 year "from the original purchase date". Sealed system / compressor 5 years: "Compressor, condenser, evaporator and refrigerant lines (parts and labor in years 1-5)". Printed: "Registered serial no.: HH56-2201-30847. Registered owner: Alex Rivera. Purchase date: 2022-01-10." Exclusions: food loss, damage from power outage, water filters, door bins, cosmetic damage, unauthorized repair. Claim: "Email service@homehub-care.example or call 1-800-555-0123"; "Claims require receipt, registration and a photo of the serial plate. The serial must match the registration."

Delegations so far: 7.

## Step 3

delegate --target document-agent --instruction 'Reconcile these files and report every difference in brand, model number, serial number, purchase date, plan start or end date, or owner name: Documents/Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf, Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf. For each difference give both values and the file each came from. If they all agree, say no differences found.'

Result: no differences found (serial HH56-2201-30847 both, purchase 2022-01-10 both, owner Alex Rivera both, model FR-560 both).

No rating-plate photo of the fridge is in hand (Step 0 matched nothing, Step 1 only looks for receipts), so there is no plate comparison and the one-character serial mismatch is never seen (D1).

Arithmetic: bought 2022-01-10 + 1 year = general warranty ended 2023-01-10. Sealed system 5 years = 2027-01-10, active (51 days left). "Not cooling" has several causes in the manual; only the compressor/sealed system is covered. Label: Partly covered.

Delegations so far: 8.

## Step 4

delegate --target file-agent --instruction 'Find files whose names contain any of: manual, guide, instructions, handbook, quick start, FR-560, FR-56x, HomeHub. Search folders whose names contain Manuals, Documents, Downloads, Home or Appliances first, then all user files. File type: documents. Return full path, file name, size and modified date, up to 20. If there are no results, say zero matches.'

Result, 7: Documents/Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf; Downloads/ADW-48xx_manual (1).pdf; Home/Appliances/Fridge/FR-560_owner_manual.pdf; Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf; Home/Appliances/Washer/WM-7_manual.pdf; Manuals/Nordvik_ADW-48xx_UserManual.pdf; Manuals/Zentro_AX3000_Router_Manual.pdf. No duplicates for the fridge.

delegate --target document-agent --instruction 'With intent locate_content and evidence mode focused, check these files: Home/Appliances/Fridge/FR-560_owner_manual.pdf, Home/Appliances/Washer/WM-7_manual.pdf, Manuals/Nordvik_ADW-48xx_UserManual.pdf, Manuals/Zentro_AX3000_Router_Manual.pdf. List only the files that are the user manual for HomeHub FR-560 or the series FR-56x. For each, quote the line that shows it. If none match, say zero matches.'

Result: Home/Appliances/Fridge/FR-560_owner_manual.pdf: "FR-560 User Manual".

delegate --target document-agent --instruction 'Using only Home/Appliances/Fridge/FR-560_owner_manual.pdf, with intent locate_content and answer mode table, find what the manual says about the symptom "stopped cooling". Return the matching rows of the error-code and troubleshooting tables (problem, cause, what to do) in the order printed, the safety warnings that apply to those steps, any steps that need a qualified technician, and any statement that user repairs affect the warranty. Give the page or section for each item.'

(No error code, so that part of the instruction is left out.)

Result, section 4 "Troubleshooting: not cooling", p. 6, in order: 1 Power: plug seated, outlet works, check breaker. 2 Temperature setting: fridge 37 F, freezer 0 F, wait 24 hours. 3 Door seals and airflow: close doors fully, do not block vents, remove ice buildup. 4 Condenser coils: unplug, vacuum the coils at the base or rear. 5 Condenser fan: listen for the fan; if silent, call service. 6 Compressor: if it does not run or clicks repeatedly, call service, do not attempt repair. Also "Allow 24 hours after any change. Food safety: discard perishables above 40 F for more than 2 hours." Safety, p. 3: "Unplug before cleaning the condenser coils." Technician: steps 5 and 6. Warranty: p. 7 "The compressor and sealed system carry an extended warranty. See the warranty card and register your serial number."

Delegations so far: 11.

## Step 5

Draft (label Partly covered).

    To: service@homehub-care.example
    Subject: Warranty claim, HomeHub FR-560, serial HH56-2201-30847
    Product: HomeHub FR-560, serial HH56-2201-30847
    Purchased: 2022-01-10 at HomeHub Appliances, order HH-220110-3318
    Coverage: HomeHub sealed system / compressor warranty, 5 years, valid until 2027-01-10
    Fault: fridge stopped cooling, no error code
    Already tried: none confirmed
    Attachments: Documents/Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf, Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf. Rating plate photo: none found, the card requires one.
    Contact: (blank)

Parent to user: answer plus "Which of the steps above have you already tried? Then say yes to save this draft to your NAS, or no." Status `waiting_approval`. The script gives no user reply, so the run stops here with no save.

Total delegations: 11 (Step 0: 1, Step 1: 3, Step 2: 3, Step 3: 1, Step 4: 3). No knowledge-agent call.

## Final answer

    Product: HomeHub FR-560 (fridge), bought 10 Jan 2022 at HomeHub Appliances
    Coverage: Partly covered. Bought 10 Jan 2022 + 1-year general warranty = ended 10 Jan 2023. The compressor and sealed system warranty (5 years) runs to 10 Jan 2027, so only a fault in the compressor, condenser, evaporator or refrigerant lines is covered.
    Safety first: Unplug before cleaning the condenser coils. (FR-560 manual, p. 3)
    Try this (manual p. 6):
      1. Check the plug, outlet and breaker.
      2. Set fridge 37 F, freezer 0 F, wait 24 hours.
      3. Close doors fully, keep vents clear, remove ice buildup.
      4. Unplug and vacuum the condenser coils.
      5. Listen for the fan.
      Technician only: if the fan is silent, or the compressor does not run or clicks repeatedly, call service. Do not attempt repair.
      Discard perishables above 40 F for more than 2 hours.
    Claim: draft ready for service@homehub-care.example. Save it to your NAS? (yes / no)
    Evidence:
      - Documents/Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf: purchase date, model, serial HH56-2201-30847
      - Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf: 1 year general, 5 years sealed system, exclusions, claim contact, registered serial HH56-2201-30847
      - Home/Appliances/Fridge/FR-560_owner_manual.pdf: troubleshooting for not cooling
    Notes: The card requires a photo of the serial plate that matches the registration. None was found, so the serial was not checked against the plate. A photo of a Nordvik display taken today was ignored as unrelated.
