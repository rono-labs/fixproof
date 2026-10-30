# Dry run A (v8): "The dishwasher is doing this again."

Today 2026-11-20 08:40. Paths relative to testdata/home-library/. Skill: fixproof/SKILL.md (v8); references unchanged. Experts played from the real files: pdftotext for document-agent, the image itself plus EXIF DateTimeOriginal for photo-agent, case-insensitive name-substring matching (script over the real file names) for file-agent, sha256sum for duplicates, a successful save for knowledge-agent.

## Intake
Fault mode. Product: dishwasher (file-agent short name DW; photo-agent gets "dishwasher"). Symptom "doing this again" (vague, repeat). No code, brand or model typed. Fault reported, so Step 0 runs. Delegation order line (new) followed: photo-agent, then file-agent and photo-agent, then document-agent, and so on.

## Step 0
**1. photo-agent**
> Read only; do not change any photo. Search photos taken in the last 48 hours, up to 2026-11-20 08:40, for pictures of an appliance control panel or display showing an error code, or of an appliance rating plate or serial label. If the search cannot filter by time, take the 20 newest photos instead. For each photo found, up to 20, run text recognition and return the photo path, the time taken, the recognised text, and which kind of appliance the photo shows. If there are no results, say zero matches.

Result (completed): 1 match. Photos/Phone/2026-11/IMG_20261120_083012.jpg, EXIF 2026:11:20 08:30:12. Text "NORDVIK", "E15", POWER, CYCLE, DELAY, START. Appliance kind not visible (panel only).

Parent: display only, the user's words "doing this" point to it. Code E15 and brand Nordvik taken. Evidence added.

## Step 1
**2. file-agent**
> Read only; do not change any file. Find files whose names contain any of: receipt, invoice, order, purchase, quittung, Nordvik, dishwasher, DW. Search folders whose names contain Receipts, Invoices, Purchases, Orders, Documents, Scans or Downloads first, then the rest of the home folder and the shared folders this user can access. File types: documents and images. Return full path, file name, type, size and modified date for each, up to 50. If there are no results, say zero matches.

Result (matcher): 8. Documents/Receipts/2019/receipt_dishwasher_old.pdf (2794); Documents/Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf (2733); Documents/Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf (2969); Documents/Receipts/2025/Brightline_order_TV_Lumora.pdf (2762); Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf (2960); Downloads/ADW-48xx_manual (1).pdf (17516); Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf (2681); Manuals/Nordvik_ADW-48xx_UserManual.pdf (17516).; the scope wording does not change it (every file sits under the one home library).

**3. photo-agent**
> Read only; do not change any photo. Search the photo library for photos of a paper receipt or till slip that mention dishwasher or Nordvik, and for photos of any appliance rating plate or serial label. Newest first, up to 20 of each. For each photo found, run text recognition and return the photo path, the date taken, whether it is a receipt or a rating plate, and the recognised text. If there are no results, say zero matches.

Result: receipt: Photos/Phone/2023-06/IMG_20230602_181404.jpg (2023-06-02 18:14:04), HomeHub Appliances, Date 06/02/2023, Order HH-230602-1187, "Nordvik WM-7 Front Load Washer SN NV7-2305-60912 $899.00". Plates: IMG_20240316_190455.jpg (2024-03-16, NORDVIK MODEL ADW-4820 SERIAL NV48-2203-1187 MFD 2023-12); IMG_20220115_101233.jpg (2022-01-15, HomeHub FR-560 SERIAL HH56-2201-30647). Parent: receipt photo names a washer, dropped.

**4. document-agent** (fridge and TV receipts dropped by name; cards and manuals are not receipts)
> Read only; do not change any file. Extract the purchase details from these receipts and invoices: Documents/Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf, Documents/Receipts/2019/receipt_dishwasher_old.pdf. For each file return store, order number, purchase date exactly as printed, product description, brand, model number, serial number if printed, price, any warranty term printed on the receipt, and every other line item, especially any protection plan, extended warranty or care plan with its plan number and term. Report any file you could not read.

Result (pdftotext): 2024: Brightline Electronics, BL-2024-0314-55871, 2024-03-14, Nordvik ADW-4820 Dishwasher, serial NV48-2203-1187, $849.00, no term; "3-Year Extended Protection Plan Plan no. EPP-3Y-90417733. Covers ADW-4820 after the manufacturer warranty ends. Terms provided separately." $129.00; installation kit $24.99. 2019: Brightline, BL-2019-0822-20318, 2019-08-22, Nordvik ADW-3100, NV31-1905-0342, $529.00, "1 year parts and labor. No extended plan purchased." No unreadable files.

Removing "receipt schema / invoice schema" changes nothing: the instruction still names the files as receipts and lists the same fields, and the result is identical.

Parent: ADW-4820 plate matches only the 2024 receipt. Settled; 2019 to Notes. Series ADW-48xx, store Brightline.

## Step 2
**5. file-agent**
> Read only; do not change any file. Find files whose names contain any of: warranty, guarantee, garantie, protection, plan, care, extended, registration, certificate, terms, conditions, Nordvik, ADW-4820, ADW-48xx, Brightline. Search folders whose names contain Warranty, Receipts, Scans, Documents, Home or Appliances first, then the rest of the home folder and the shared folders this user can access. File types: documents and images. Return full path, file name, size and modified date for each, up to 50. If there are no results, say zero matches.

Result: 10 (ADW-4820 card, EPP terms scan, Lumora TV warranty, WM-7 card, FR-560 registration, three Brightline receipts, two ADW-48xx manuals). A "terms" name and a Scans result exist, so no extra Scans listing.

**6. document-agent**
> Read only; do not change any file. Read the contents of these files: Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf, Scans/2024/Brightline_EPP_terms_scan.pdf. List only the files that are a warranty, guarantee, protection plan or warranty registration for Nordvik ADW-4820 or the series ADW-48xx, or a plan bought with order BL-2024-0314-55871. For each, quote the line that shows it. If none match, say zero matches.

Result: both. Card "Product: ADW-4820 Dishwasher"; scan "Covered product Nordvik ADW-4820 Dishwasher, serial NV48-2203-1187", "Purchased 2024-03-14 (Brightline order BL-2024-0314-55871)".

**7. document-agent**
> Read only; do not change any file. Answer from these files only: Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf, Scans/2024/Brightline_EPP_terms_scan.pdf. Return a table with one row per document: the provider, each coverage (full parts and labour, parts only, or named components such as motor, compressor or panel) with its term, how the start date is defined, and any printed start or end date. Also return the exclusions and the claim procedure (phone, email or web form exactly as written, required attachments). Also return any plan number, registration number and serial number written on it. Quote the page or section for each answer. If a file has no warranty terms, say so for that file. Report any file you could not read.

Result: card p.1: parts and labor 2 years; drive motor 10 years (parts only after year 2); "Warranty starts on the date of original retail purchase"; exclusions incl. gaskets; claim "Email claims@nordvik-support.example or call 1-800-555-0188 ...". Scan p.1: plan EPP-3Y-90417733, serial NV48-2203-1187, "Plan start 2026-03-14, the day after the 2-year manufacturer warranty ends", "Plan end 2029-03-14"; s.1 covers "leaks from internal components"; s.2 excludes "racks, filters and gaskets"; s.3 "Email protect@brightline-services.example or call 1-800-555-0199. Have your plan number, the original receipt, and the product serial number ready."

## Step 3
**8. document-agent**
> Read only; do not change any file. Reconcile these files and report every difference in brand, model number, serial number, purchase date, plan start or end date, or owner name: Documents/Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf, Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf, Scans/2024/Brightline_EPP_terms_scan.pdf. For each difference give both values and the file each came from. If they all agree, say no differences found.

Result: no differences found. Plate serial agrees. Base: 14 Mar 2024 + 2 y = ended 14 Mar 2026. Plan printed 14 Mar 2026 to 14 Mar 2029 (calculated start 15 Mar, one-day gap noted, printed kept). Motor to 14 Mar 2034. Label Covered; gasket exclusion goes to Notes.

## Step 4
**9. file-agent**
> Read only; do not change any file. Find files whose names contain any of: manual, guide, instructions, handbook, quick start, ADW-4820, ADW-48xx, Nordvik. Search folders whose names contain Manuals, Documents, Downloads, Home or Appliances first, then the rest of the home folder and the shared folders this user can access. File type: documents. Return full path, file name, size and modified date, up to 20. If there are no results, say zero matches.

Result: 7 (two ADW-48xx manuals, Zentro, WM-7 and FR-560 manuals, two Nordvik warranty cards). Named as a manual and with brand/model/series: the two ADW-48xx files.

**10. document-agent**
> Read only; do not change any file. Read the contents of these files: Manuals/Nordvik_ADW-48xx_UserManual.pdf, Downloads/ADW-48xx_manual (1).pdf. List only the files that are the user manual or guide for Nordvik ADW-4820 or the series ADW-48xx, and quote the line that shows it. If none match, say zero matches.

Result: both, "Nordvik Dishwasher Model series ADW-48xx User Manual and Care Guide" (p.1).

**11. file-agent** (same size 17516)
> Read only; do not change any file. Read only; do not change any file. Return the SHA-256 checksum of each of these files: Manuals/Nordvik_ADW-48xx_UserManual.pdf, Downloads/ADW-48xx_manual (1).pdf. Report any file you could not read.

Result: both 2858e0506bfc17fb3076623c5b917c28c11cb91b4650cc02af821eb6bfde3b7d. Keep Manuals/, note duplicate. The doubled "Read only" prefix (defect V8-1) is harmless here.

**12. document-agent** (vague symptom, code alone)
> Read only; do not change any file. Using only Manuals/Nordvik_ADW-48xx_UserManual.pdf, find what the manual says about error code E15. Return, as a table, the matching rows of the error-code and troubleshooting tables (problem, cause, what to do) in the order printed, the safety warnings that apply to those steps, any steps that need a qualified technician, and any statement that user repairs affect the warranty. If there is no entry for the code or symptom, return the support or service contact printed in the manual. Give the page or section for each item.

Result: s.7 p.9 E15 "Water detected in the base pan. Leak protection has stopped the unit." / "Turn off water, unplug, tilt unit slightly to drain base pan only if instructed, check door gasket and hose connections. If E15 returns, call service. Do not open the base." s.8 p.10 "Puddle under unit, E15 shown" / "loose hose, door gasket, or internal leak" / "Stop the unit, check hose clamps and gasket. Service call if the leak persists". Safety p.3 "Do not operate a dishwasher that is leaking. Turn off the water supply and unplug the unit." Warranty p.3 and p.10: user repair beyond listed steps voids warranty and plan.

Parent: water collecting inside a mains appliance, safety leads. Repeat fault: "If E15 returns, call service" first.

## Step 5
Covered; plan contact; plan terms not an attachment (procedure does not ask), plan number in body. Draft:
```
To: Email protect@brightline-services.example or call 1-800-555-0199
Subject: Warranty claim, Nordvik ADW-4820, serial NV48-2203-1187
Product: Nordvik ADW-4820, serial NV48-2203-1187
Purchased: 14 Mar 2024 at Brightline Electronics, order BL-2024-0314-55871
Coverage: 3-Year Extended Protection Plan EPP-3Y-90417733, valid until 14 Mar 2029
Fault: water in the base pan, leak protection stopped the unit, error code E15, returned after an earlier occurrence
Already tried: none confirmed
Attachments: Documents/Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf
Contact:
```
Asked: "Which of these steps have you already tried? Say yes to save the draft to your NAS, or no." `waiting_approval`.

User: "I checked the hoses, yes save it." Already tried becomes "checked the hose connections".

**13. knowledge-agent** (no single quote in any slot value, so the new apostrophe rule changes nothing)
> Save this text as a new note in a folder named Warranty claims in the user home folder, or in the default notes location if that folder cannot be used, with filename hint "Warranty claim Nordvik ADW-4820 2026-11-20 0840", with time written as four digits such as 0840. The user approved saving this exact text. Do not overwrite an existing file. Return the saved file path and whether the save was verified. Text: (draft above with "Already tried: checked the hose connections")

Result (simulated success): `completed`, path /home/alex/Warranty claims/Warranty claim Nordvik ADW-4820 2026-11-20 0840.md, verified yes. Expert-states rule satisfied (completed, path returned), so the path is reported.

Observation: "this exact text" is not quite true here: the user approved the shown draft plus their tried step, and never saw the amended line (defect V8-3).

## Final answer
```
Safety first: Water in the base pan is a leak on a mains appliance. Switch the dishwasher off at the wall, close the water supply, and call a qualified technician if it persists. Manual: "Do not operate a dishwasher that is leaking. Turn off the water supply and unplug the unit." (page 3)
Product: Nordvik ADW-4820 (dishwasher), bought 14 Mar 2024 at Brightline Electronics
Coverage: Covered. Bought 14 Mar 2024 + 2-year warranty = ended 14 Mar 2026. Protection plan EPP-3Y-90417733 runs 14 Mar 2026 to 14 Mar 2029, so covered by the plan.
Try this (manual section 7 page 9, section 8 page 10):
  1. E15 has come back. The manual says: "If E15 returns, call service."
  2. Turn off the water and unplug the unit.
  3. Check the door gasket and the hose connections and clamps. You have checked the hoses.
  4. Tilt the unit slightly to drain the base pan only if instructed.
  Technician only: do not open the base. A repair beyond these steps voids the warranty and the protection plan (page 3).
Claim: draft ready for protect@brightline-services.example (or 1-800-555-0199).
  Claim draft saved to /home/alex/Warranty claims/Warranty claim Nordvik ADW-4820 2026-11-20 0840.md. Nothing was sent.
Evidence:
  - Photos/Phone/2026-11/IMG_20261120_083012.jpg: E15 and Nordvik, taken 20 Nov 2026 08:30
  - Documents/Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf: purchase 14 Mar 2024, ADW-4820, serial NV48-2203-1187, order, plan EPP-3Y-90417733
  - Photos/Phone/2024-03/IMG_20240316_190455.jpg: rating plate ADW-4820, serial NV48-2203-1187
  - Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf: 2 years parts and labor, motor 10 years (to 14 Mar 2034), exclusions
  - Scans/2024/Brightline_EPP_terms_scan.pdf: plan 14 Mar 2026 to 14 Mar 2029, exclusions, claim contact
  - Manuals/Nordvik_ADW-48xx_UserManual.pdf: E15 rows, safety, warranty warning
Notes: A 2019 Nordvik ADW-3100 (receipt 22 Aug 2019) also exists; the plate photo matches only the 2024 unit. Duplicate manual at Downloads/ADW-48xx_manual (1).pdf (same checksum). The plan says it starts the day after the warranty ends (15 Mar 2026) but prints 14 Mar 2026; printed date kept, one-day gap. The plan excludes gaskets: a worn door gasket is excluded, an internal leak is covered.
```
Status `completed`, saved. Delegations: 13 (photo 2, file 4, document 6, knowledge 1).

## Check
Expected outcome met in every item. PASS.
