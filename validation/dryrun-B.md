# Dry run B: "Washing machine shows F21. Is it still under warranty?"

Today = 2026-11-20 08:40. Intake: mode fault. Product washing machine. Symptom "shows F21", code F21. Brand and model unknown.

## Step 0

delegate --target photo-agent --instruction 'Search photos taken in the last 48 hours, up to 2026-11-20 08:40, for pictures of an appliance control panel or display showing an error code, or of an appliance rating plate or serial label. For each photo found, run text recognition and return the photo path, the time taken and the recognised text. If there are no results, say zero matches.'

Result: 1 photo, `Photos/Phone/2026-11/IMG_20261120_083012.jpg`, taken 2026-11-20 08:30:12. Text: "NORDVIK E15 POWER CYCLE DELAY START".

Parent: the text names no appliance type, and the user gave a different code (F21) for a washing machine. Nothing ties the photo to the washer. Treated as no match; brand not taken from it (D3). Continue with the user's words.

## Step 1

delegate --target file-agent --instruction 'Find files whose names contain any of: receipt, invoice, order, purchase, quittung, washing machine. Search folders whose names contain Receipts, Invoices, Purchases, Orders, Documents, Scans or Downloads first, then all user files. File types: documents and images. Return full path, file name, type, size and modified date for each, up to 50. If there are no results, say zero matches.'

Result, 5 PDFs, all in Documents/Receipts: 2019/receipt_dishwasher_old.pdf, 2022/HomeHub_receipt_fridge_Jan2022.pdf, 2024/Brightline_Receipt_2024-03-14_dishwasher.pdf, 2025/Brightline_order_TV_Lumora.pdf, 2025/Brightline_soundbar_2025-12-18.pdf. No washer receipt by name.

delegate --target photo-agent --instruction 'Search the photo library for photos of a paper receipt or till slip that mention washing machine. For each photo found, run text recognition and return the photo path, the date taken and the recognised text. If there are no results, say zero matches.'

Result: `Photos/Phone/2023-06/IMG_20230602_181404.jpg`, date taken 2023-06-02. Text: "HOMEHUB APPLIANCES / 77 Harbor Road, Port Alder OR / Date: 06/02/2023 Order HH-230602-1187 / Cust: Alex Rivera / Nordvik WM-7 Front Load Washer / SN NV7-2305-60912 $899.00 / Delivery $59.00 / TOTAL $958.00 / Paid: CARD ****4417 / Warranty: see manufacturer card". All of it legible.

delegate --target document-agent --instruction 'Extract purchase details with the receipt schema from these files: Documents/Receipts/2019/receipt_dishwasher_old.pdf, Documents/Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf, Documents/Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf, Documents/Receipts/2025/Brightline_order_TV_Lumora.pdf, Documents/Receipts/2025/Brightline_soundbar_2025-12-18.pdf. If a file returns no data with the receipt schema, try the invoice schema. For each file return store, order number, purchase date exactly as printed, product description, brand, model number, serial number if printed, price, and every other line item, especially any protection plan, extended warranty or care plan with its plan number and term. Report any file you could not read.'

Result: all read: Nordvik ADW-3100 dishwasher (2019), HomeHub FR-560 fridge (2022), Nordvik ADW-4820 dishwasher with protection plan (2024), Lumora 55Q8 TV (2025), Lumora S2 soundbar (2025). No washing machine. (Wasted call: no path could be a washer receipt, D7.)

Parent: the only washer purchase is the photo. Brand Nordvik, model WM-7, serial NV7-2305-60912, $899.00, HomeHub Appliances, order HH-230602-1187, "Warranty: see manufacturer card". Evidence list: the photo, stated as the purchase record. No protection plan on it.

Date reading (coverage-rules, "Reading dates"): 06/02/2023 can be 2 June or 6 February. Store country: HomeHub, Port Alder OR (US), so month first; order number HH-230602 reads 2023-06-02; photo date taken 2023-06-02. Settled: 2 June 2023. Stated in Notes.

Delegations so far: 4.

## Step 2

Series: WM-7 has one digit, so there is nothing to replace with x; series = WM-7 (D8).

delegate --target file-agent --instruction 'Find files whose names contain any of: warranty, guarantee, garantie, protection, plan, care, extended, registration, certificate, Nordvik, WM-7. Search folders whose names contain Warranty, Receipts, Scans, Documents, Home or Appliances first, then all user files. File types: documents and images. Return full path, file name, size and modified date for each, up to 50. If there are no results, say zero matches.'

Result, 6 PDFs: Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf; Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf; Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf; Home/Appliances/Washer/WM-7_manual.pdf; Manuals/Nordvik_ADW-48xx_UserManual.pdf; Scans/Lumora_TV_warranty.pdf.

delegate --target document-agent --instruction 'With intent locate_content and evidence mode focused, check these files: Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf, Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf, Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf, Home/Appliances/Washer/WM-7_manual.pdf, Manuals/Nordvik_ADW-48xx_UserManual.pdf, Scans/Lumora_TV_warranty.pdf. List only the files that are a warranty, guarantee, protection plan or warranty registration for Nordvik WM-7 or the series WM-7, or a plan bought with order HH-230602-1187. For each, quote the line that shows it. If none match, say zero matches.'

Result: 1 file. Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf: "Product: WM-7 Front Load Washing Machine".

delegate --target document-agent --instruction 'Answer from these files only: Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf. With intent period and answer mode table, return for each document: the provider, each coverage (full parts and labour, parts only, or named components such as motor, compressor or panel) with its term, how the start date is defined, and any printed start or end date. With intent condition, return the exclusions and the claim procedure (phone, email or web form exactly as written, required attachments). Also return any plan number, registration number and serial number written on it. Quote the page or section for each answer.'

Result: Nordvik; parts and labor 2 years; "Warranty starts on the date of original retail purchase"; no printed dates; "This warranty has no extended components." Exclusions: misuse, installation faults, hoses, cosmetic damage, repairs by unauthorized persons, commercial use. Claim: claims@nordvik-support.example or 1-800-555-0188, receipt and serial plate photo. No plan, registration or serial number.

Delegations so far: 7.

## Step 3

delegate --target document-agent --instruction 'Reconcile these files and report every difference in brand, model number, serial number, purchase date, plan start or end date, or owner name: Photos/Phone/2023-06/IMG_20230602_181404.jpg, Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf. For each difference give both values and the file each came from. If they all agree, say no differences found.'

Result: could not read the .jpg (image file, not a document); read only the warranty card (Nordvik, WM-7); no comparison possible. Parent names the photo as unreadable by document-agent in Notes; its text came from photo-agent (D7). No plate photo in hand.

Arithmetic: bought 2023-06-02 + 2 years = ended 2025-06-02. No other coverage (card: no extended components; no plan on the receipt). Today 2026-11-20 is after it. Label: Not covered, ended 2 Jun 2025.

Delegations so far: 8.

## Step 4

delegate --target file-agent --instruction 'Find files whose names contain any of: manual, guide, instructions, handbook, quick start, WM-7, Nordvik. Search folders whose names contain Manuals, Documents, Downloads, Home or Appliances first, then all user files. File type: documents. Return full path, file name, size and modified date, up to 20. If there are no results, say zero matches.'

Result, 7: Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf; Downloads/ADW-48xx_manual (1).pdf (17516 B); Home/Appliances/Fridge/FR-560_owner_manual.pdf; Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf; Home/Appliances/Washer/WM-7_manual.pdf; Manuals/Nordvik_ADW-48xx_UserManual.pdf (17516 B); Manuals/Zentro_AX3000_Router_Manual.pdf. No two share a name stem and size for this product, so no checksum call.

delegate --target document-agent --instruction 'With intent locate_content and evidence mode focused, check these files: Home/Appliances/Washer/WM-7_manual.pdf, Manuals/Nordvik_ADW-48xx_UserManual.pdf, Downloads/ADW-48xx_manual (1).pdf, Home/Appliances/Fridge/FR-560_owner_manual.pdf, Manuals/Zentro_AX3000_Router_Manual.pdf. List only the files that are the user manual for Nordvik WM-7 or the series WM-7. For each, quote the line that shows it. If none match, say zero matches.'

Result: Home/Appliances/Washer/WM-7_manual.pdf: "WM-7 User Manual".

delegate --target document-agent --instruction 'Using only Home/Appliances/Washer/WM-7_manual.pdf, with intent locate_content and answer mode table, find what the manual says about error code F21 and about the symptom "shows F21". Return the matching rows of the error-code and troubleshooting tables (problem, cause, what to do) in the order printed, the safety warnings that apply to those steps, any steps that need a qualified technician, and any statement that user repairs affect the warranty. Give the page or section for each item.'

Result:
- Error codes, p. 6: F21 "Drain fault: water not draining." Action: "Pause, power off, clean the drain pump filter behind the lower right panel (have a towel ready), check the drain hose for kinks, restart."
- Troubleshooting, p. 7: "Water left in drum, F21": cause "Blocked pump filter or hose"; solution "Clean pump filter, check hose".
- Safety, p. 3: "Disconnect power before any cleaning near electrical parts." "Do not open the door while the drum is turning."
- No technician-only steps. No statement on user repairs and warranty (p. 8 only says see the warranty card).

Delegations: 11 (Step 0: 1, Step 1: 3, Step 2: 3, Step 3: 1, Step 4: 3). No claim draft (Not covered), no save. Status `completed`.

## Final answer

    Product: Nordvik WM-7 (washing machine), bought 2 Jun 2023 at HomeHub Appliances
    Coverage: Not covered. Bought 2 Jun 2023 + 2-year warranty = ended 2 Jun 2025. The warranty card says it has no extended components and the receipt shows no protection plan.
    Safety first: Disconnect power before any cleaning near electrical parts. (WM-7 manual, p. 3)
    Try this (manual p. 6 and p. 7):
      1. Pause the machine and power it off.
      2. Clean the drain pump filter behind the lower right panel (have a towel ready).
      3. Check the drain hose for kinks.
      4. Restart.
    Evidence:
      - Photos/Phone/2023-06/IMG_20230602_181404.jpg: purchase date 06/02/2023, model WM-7, serial NV7-2305-60912, $899.00 (receipt exists only as a photo)
      - Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf: 2 years parts and labour, no extended components
      - Home/Appliances/Washer/WM-7_manual.pdf: troubleshooting for F21
    Notes: The receipt is a phone photo, so the date was read as 2 June 2023 (US store, order number HH-230602, date taken 2023-06-02), not 6 February. document-agent could not read the photo, so the receipt and warranty card were not cross-checked by it. A photo taken today of a Nordvik display showing E15 was not used (a different appliance and code).
