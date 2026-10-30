# Dry run C (v8): "The fridge stopped cooling."

Today 2026-11-20 08:40. Paths relative to testdata/home-library/. v8 SKILL.md, experts played from the real files (method as in dryrun-A).

## Intake
Fault mode. Product: fridge (file-agent: refrigerator, FR; photo-agent: fridge). Symptom written as "not cooling". No code, brand, model. Step 0 runs.

## Step 0
**1. photo-agent** (v8 Step 0 text). Result: the E15 Nordvik panel photo. Ignored (not a fridge, words do not point to it).

## Step 1
**2. file-agent**
> Read only; do not change any file. Find files whose names contain any of: receipt, invoice, order, purchase, quittung, fridge, refrigerator, FR. Search folders whose names contain Receipts, Invoices, Purchases, Orders, Documents, Scans or Downloads first, then the rest of the home folder and the shared folders this user can access. File types: documents and images. Return full path, file name, type, size and modified date for each, up to 50. If there are no results, say zero matches.

Result (matcher): 6. Documents/Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf; 2019 and 2024 dishwasher receipts; 2025 TV order; Home/Appliances/Fridge/FR-560_owner_manual.pdf; Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf.

**3. photo-agent** (receipts mentioning fridge; plates). Result: receipts zero matches. Plates: ADW-4820; Photos/Phone/2022-01/IMG_20220115_101233.jpg (EXIF 2022:01:15 10:12:33) "HomeHub MODEL: FR-560 SERIAL: HH56-2201-30647 ... Compressor: sealed system".

**4. document-agent**
> Read only; do not change any file. Extract the purchase details from these receipts and invoices: Documents/Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf. For each file return store, order number, purchase date exactly as printed, [...] Report any file you could not read.

Result: HomeHub Appliances, HH-220110-3318, 2022-01-10, HomeHub FR-560 French Door Refrigerator, serial HH56-2201-30847, $1,649.00, no term, no plan; delivery and setup $79.00.

Parent: one purchase. FR-560 plate kept (model matches). Series left out (three digits).

## Step 2
**5. file-agent** (warranty terms + HomeHub, FR-560; v8 scope). Result: 7 (FR-560 registration, FR-560 manual, fridge receipt, ADW-4820 card, WM-7 card, Lumora TV warranty, EPP terms scan). No plan, no Scans listing.

**6. document-agent**
> Read only; do not change any file. Read the contents of these files: Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf, Scans/2024/Brightline_EPP_terms_scan.pdf. List only the files that are a warranty, guarantee, protection plan or warranty registration for HomeHub FR-560, or a plan bought with order HH-220110-3318. [...]

Result: registration only, "Product: FR-560 Refrigerator".

**7. document-agent** (terms, registration only). Result p.1: general parts and labor 1 year; sealed system / compressor 5 years, from original purchase date; "Registered serial no.: HH56-2201-30847. Registered owner: Alex Rivera. Purchase date: 2022-01-10."; exclusions food loss, power outage, water filters, door bins, cosmetic, unauthorized repair; "Claims require receipt, registration and a photo of the serial plate. The serial must match the registration."; "Email service@homehub-care.example or call 1-800-555-0123."

## Step 3
**8. document-agent**
> Read only; do not change any file. Reconcile these files and report every difference in brand, model number, serial number, purchase date, plan start or end date, or owner name: Documents/Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf, Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf. [...]

Result: no differences found. Parent: plate HH56-2201-30647 vs receipt/registration HH56-2201-30847: Unclear, ask the user to read the plate. General ended 10 Jan 2023; compressor to 10 Jan 2027; would be Partly covered once the serial is confirmed.

## Step 4
**9. file-agent** (manual terms + FR-560, HomeHub). Result: 7; manual-named with model: FR-560_owner_manual.pdf only.

**10. document-agent** (content check, FR-560_owner_manual.pdf). Result: match, "HomeHub French Door Refrigerator Model series FR-560 User Manual and Care Guide" (p.1).

**11. document-agent**
> Read only; do not change any file. Using only Home/Appliances/Fridge/FR-560_owner_manual.pdf, find what the manual says about the symptom "not cooling". Return, as a table, [...]

Result: s.4 p.6 steps 1-6 (power; 37 F / 0 F, wait 24 h; door seals and airflow; unplug and vacuum coils; condenser fan silent: call service; compressor not running or clicking: call service, do not attempt repair). "Allow 24 hours after any change. Food safety: discard perishables above 40 F for more than 2 hours." Safety p.3 "Unplug before cleaning the condenser coils." Technician: 5, 6.

## Step 5
Unclear, so draft. Plate serial used, registered value beside it.
```
To: Email service@homehub-care.example or call 1-800-555-0123
Subject: Warranty claim, HomeHub FR-560, serial HH56-2201-30647 (to check)
Product: HomeHub FR-560, serial HH56-2201-30647 per rating plate (registered as HH56-2201-30847, check before sending)
Purchased: 10 Jan 2022 at HomeHub Appliances, order HH-220110-3318
Coverage: HomeHub sealed system / compressor warranty, valid until 10 Jan 2027
Fault: not cooling
Already tried: none confirmed
Attachments: Documents/Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf, Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf, Photos/Phone/2022-01/IMG_20220115_101233.jpg
Contact:
```

## Final answer (ends at the approval question)
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
  - Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf: 1 year general, 5 years compressor and sealed system, registered serial, claim contact
  - Photos/Phone/2022-01/IMG_20220115_101233.jpg: rating plate FR-560, serial HH56-2201-30647
  - Home/Appliances/Fridge/FR-560_owner_manual.pdf: not-cooling steps, safety
Notes: Serial mismatch: plate HH56-2201-30647 vs receipt and registration HH56-2201-30847. The claim procedure says the serial must match the registration. Exclusions include food loss and unauthorized repair.
```
Status `waiting_approval`. Delegations: 11 (photo 2, file 3, document 6).

## Check
Unclear, general ended 2023-01-10, partly covered to 2027-01-10 once serial confirmed, not-cooling steps, draft with plate value marked. PASS. Same as v6.
