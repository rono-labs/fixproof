# Dry run C: "The fridge stopped cooling."

Today = 2026-11-20. Paths are relative to `project/testdata/home-library/` (written `home-library/`). Expert results are emulated from `find`, `grep`, `pdftotext` and by viewing the photos.

## Intake
Mode: fault. Product: fridge. Symptom: "The fridge stopped cooling." No error code, no brand, no model.

## Step 1. Purchase record

delegate --target file-agent --instruction 'Find documents that look like receipts, invoices or order confirmations for a fridge. Search folders whose names contain Receipts, Invoices, Purchases, Orders, Documents, Scans or Downloads first, then all of the user files. Include PDF, image and office document types. For each match return the full path, file name, type and modified date, up to 30 matches. If there are no results, say zero matches.'

file-agent result (1 match; "fridge" is in the file name):
- home-library/Documents/Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf, PDF, modified 2026-10-29

delegate --target photo-agent --instruction 'Search the photo library for photos of a paper receipt or of an appliance rating plate or serial label for a fridge. For each photo found, run text recognition and return the photo path, the date taken and the recognised text. If there are no results, say zero matches.'

photo-agent result (same three paper/plate photos; text read from the images):
- Photos/Phone/2022-01/IMG_20220115_101233.jpg, 2022-01-15: "HomeHub / MODEL: FR-560 / SERIAL: HH56-2201-30647 / VOLTS 115V 60Hz AMPS 6.5 / REFRIGERANT R600a 38 g / MADE FOR HomeHub Appliances / Compressor: sealed system"
- Photos/Phone/2024-03/IMG_20240316_190455.jpg (dishwasher plate) and Photos/Phone/2023-06/IMG_20230602_181404.jpg (washer receipt): other products, ignored.

delegate --target document-agent --instruction 'Extract purchase details with the receipt schema from these files: home-library/Documents/Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf. For each file return store, order number, purchase date, product description, brand, model number, serial number if printed, price, and every other line item, especially any protection plan, extended warranty or care plan with its plan number and term.'

document-agent result: HomeHub Appliances, order HH-220110-3318, 2022-01-10, "HomeHub FR-560 French Door Refrigerator, Stainless, 25 cu ft", brand HomeHub, model FR-560, serial HH56-2201-30847, $1,649.00. Other line: delivery and setup $79.00. No protection plan, no warranty term printed on the receipt.

One fridge purchase, matches the plate model. No question to the user needed.

## Step 2. Warranty documents

delegate --target file-agent --instruction 'Find documents that mention FR-560 or HomeHub fridge together with any of these words: warranty, guarantee, protection plan, extended, care plan, certificate, registration. Also return any file in the same folder as home-library/Documents/Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf with a modified date within 30 days of 2022-01-10. Return full path, file name and modified date for each, up to 30. If there are no results, say zero matches.'

file-agent result:
- home-library/Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf (FR-560, warranty, registration)
- home-library/Home/Appliances/Fridge/FR-560_owner_manual.pdf (FR-560, "extended warranty")
- home-library/Documents/Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf (FR-560, "warranty claims")
Same-folder clause: nothing (upload dates are all 2026-10-29).

delegate --target document-agent --instruction 'Answer from these files only: home-library/Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf. For each document return: who provides it, what it covers (full parts and labour, parts only, or named components such as motor or compressor) with the term for each, whether the term starts at purchase, delivery or when another warranty ends, the exclusions, the claim procedure (phone, email or web form exactly as written, and required attachments), and any plan or registration number with any serial number written on it. Quote the page or section for each answer.'

document-agent result (page 1): provider HomeHub. General parts and labor 1 year from original purchase date. Sealed system / compressor 5 years: "Compressor, condenser, evaporator and refrigerant lines (parts and labor in years 1-5)". "Registered serial no.: HH56-2201-30847. Registered owner: Alex Rivera. Purchase date: 2022-01-10." Exclusions: food loss, damage from power outage, water filters, door bins, cosmetic damage, unauthorized repair. Claims require receipt, registration and a photo of the serial plate, and "The serial must match the registration." Claim: service@homehub-care.example or 1-800-555-0123. No separate registration number.

## Step 3. Verdict and cross-check

delegate --target document-agent --instruction 'Compare these files and report every difference in model number, serial number, purchase date, owner name or store: home-library/Documents/Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf, home-library/Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf. For each difference give both values and the file each came from. If they all agree, say no differences found.'

document-agent result: no differences found. Model FR-560 on both; serial HH56-2201-30847 on both; purchase date 2022-01-10 on both; owner Alex Rivera on both; the registration prints no store.

Parent compares the photo-agent text: plate serial HH56-2201-30647 versus receipt and registration HH56-2201-30847. They differ in one character (30647 vs 30847). Shown plainly, not hidden. A 6 and an 8 are easy to confuse in text recognition, so the parent also tells the user to read the plate.

Arithmetic (coverage-rules.md):
- General warranty: 2022-01-10 + 1 year = ended 2023-01-10.
- Sealed system / compressor: 2022-01-10 + 5 years = 2027-01-10, active today (51 days left).
- Which coverage applies: the compressor warranty applies only if the manual's cause points to the compressor. The manual's not-cooling table lists power, setting, door seals, coils, fan and compressor, and does not name one cause, so the wording is "may be covered if the technician confirms a sealed system fault".
- Cross-check table: serial differs between registration/receipt and plate photo, so the verdict is Unclear until the user reads the plate. The registration also says "The serial must match the registration."
Verdict: Unclear (compressor warranty active to 2027-01-10, general warranty ended 2023-01-10; serial mismatch).

## Step 4. Manual

delegate --target file-agent --instruction 'Find user manuals, installation guides or quick start guides for HomeHub FR-560. Search folders whose names contain Manuals, Documents, Downloads or Home first, then all user files. Return full path, file name and modified date, up to 10. If there are no results, say zero matches.'

file-agent result: 1 match, home-library/Home/Appliances/Fridge/FR-560_owner_manual.pdf, modified 2026-10-29.

delegate --target document-agent --instruction 'Using only home-library/Home/Appliances/Fridge/FR-560_owner_manual.pdf, find what the manual says about the symptom "The fridge stopped cooling". Return the matching rows of the troubleshooting or error-code table (problem, cause, what to do) in the order printed, the safety warnings that apply to those steps, any steps the manual says need a qualified technician, and any statement that user repairs affect the warranty. Give the page or section for each item.'
(No error code was given, so the error-code clause is left out.)

document-agent result:
- Section 4 "Troubleshooting: not cooling", p. 6, in order: 1 Power: confirm plug seated, outlet works, check breaker. 2 Temperature setting: fridge 37 F, freezer 0 F, wait 24 hours. 3 Door seals and airflow: close doors fully, do not block vents, remove ice buildup. 4 Condenser coils: unplug, vacuum the coils at the base or rear. 5 Condenser fan: listen for the fan; if silent, call service. 6 Compressor: if it does not run or clicks repeatedly, call service; "Do not attempt repair." "Allow 24 hours after any change." "Food safety: discard perishables above 40 F for more than 2 hours."
- Safety, section 1, p. 3: "Unplug before cleaning the condenser coils."
- Technician: steps 5 and 6 (call service).
- Warranty effect of user repairs: not stated in the manual. Section 5, p. 7: "The compressor and sealed system carry an extended warranty. See the warranty card and register your serial number." (The warranty card lists "unauthorized repair" as an exclusion.)

## Step 5. Claim draft
Verdict is Unclear, so a draft is offered. The draft carries both serial values because SKILL.md does not say which one to use (defect D7); examples.md uses the plate value with a note. Status `waiting_approval`; the scenario ends here with no user reply, so no knowledge-agent call.

## Step 6. Final answer

    Product: HomeHub FR-560 (fridge), bought 2022-01-10 at HomeHub Appliances
    Coverage: Unclear. General warranty: 10 Jan 2022 + 1 year = ended 10 Jan 2023. Sealed system and compressor warranty: 10 Jan 2022 + 5 years = runs to 10 Jan 2027, so it may be covered if the technician confirms a sealed system fault. The serial on the plate photo does not match the registration (see Notes), so please read the plate before claiming.
    Safety first: "Unplug before cleaning the condenser coils." (manual section 1, p. 3)
    Try this (manual section 4, p. 6):
      1. Confirm the plug is seated and the outlet works; check the breaker.
      2. Set fridge to 37 F and freezer to 0 F, then wait 24 hours.
      3. Close doors fully, do not block vents, remove ice buildup.
      4. Unplug and vacuum the condenser coils at the base or rear.
      5. Listen for the condenser fan; if it is silent, call service.
      6. If the compressor does not run or clicks repeatedly, call service.
      Technician only: do not attempt compressor repair (manual step 6).
      Food safety: discard perishables above 40 F for more than 2 hours (manual p. 6).
    Claim: draft ready for service@homehub-care.example or 1-800-555-0123. Save it to your NAS? (yes / no)
    Evidence:
      - home-library/Documents/Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf: purchase 2022-01-10, order HH-220110-3318, FR-560, serial HH56-2201-30847
      - home-library/Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf: 1 year general, 5 years sealed system and compressor, exclusions, registered serial HH56-2201-30847, claim contact
      - home-library/Photos/Phone/2022-01/IMG_20220115_101233.jpg: rating plate, FR-560, serial read as HH56-2201-30647
      - home-library/Home/Appliances/Fridge/FR-560_owner_manual.pdf: not-cooling steps, p. 6
    Notes: Serial mismatch. Receipt and registration: HH56-2201-30847. Plate photo: HH56-2201-30647. One character differs (30847 vs 30647); text recognition can confuse 6 and 8. The registration says the serial must match for a claim. The manual does not name a cause, so the compressor warranty depends on the technician's finding.

Claim draft shown with it:

    To: service@homehub-care.example or 1-800-555-0123
    Subject: Warranty claim, HomeHub FR-560, serial HH56-2201-30847 (plate photo reads HH56-2201-30647, to be checked)
    Product: HomeHub FR-560, serial per receipt and registration HH56-2201-30847; serial read from plate photo HH56-2201-30647
    Purchased: 2022-01-10 at HomeHub Appliances, order HH-220110-3318
    Coverage: sealed system and compressor warranty, 5 years, valid until 2027-01-10 (applies only if the technician confirms a sealed system fault)
    Fault: fridge stopped cooling
    Already tried: none confirmed yet
    Attachments: home-library/Documents/Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf, home-library/Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf, home-library/Photos/Phone/2022-01/IMG_20220115_101233.jpg
    Contact: (left blank)

Status token: `waiting_approval`.
