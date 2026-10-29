# Dry run B: "Washing machine shows F21. Is it still under warranty?"

Today 2026-11-20 08:40. Paths relative to project/testdata/home-library/. Mode: fault. Product: washing machine. Code: F21. No brand or model from the user.

## Step 0

DELEGATE photo-agent:
'Search photos taken in the last 48 hours, up to 2026-11-20 08:40, for pictures of an appliance control panel or display showing an error code, or of an appliance rating plate or serial label. If the search cannot filter by time, take the 20 newest photos instead. For each photo found, up to 20, run text recognition and return the photo path, the time taken, the recognised text, and which kind of appliance the photo shows. If there are no results, say zero matches.'

Result: 1 photo. Photos/Phone/2026-11/IMG_20261120_083012.jpg, EXIF 2026-11-20 08:30:12, text "NORDVIK", "E15", buttons POWER, CYCLE, DELAY, START; appliance kind not visible.
Parent: user named F21, photo shows E15, a different code, so the photo is ignored. Brand and model stay unknown.

## Step 1

DELEGATE file-agent ({brand}, {model} left out):
'Find files whose names contain any of: receipt, invoice, order, purchase, quittung, washing machine. Search folders whose names contain Receipts, Invoices, Purchases, Orders, Documents, Scans or Downloads first, then all user files. File types: documents and images. Return full path, file name, type, size and modified date for each, up to 50. If there are no results, say zero matches.'

Result, 5 files (all through "receipt" or "order"): Documents/Receipts/2019/receipt_dishwasher_old.pdf; Documents/Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf; Documents/Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf; Documents/Receipts/2025/Brightline_order_TV_Lumora.pdf; Documents/Receipts/2025/Brightline_soundbar_2025-12-18.pdf. None names a washing machine.

DELEGATE photo-agent:
'Search the photo library for photos of a paper receipt or till slip that mention washing machine, and for photos of any appliance rating plate or serial label. Newest first, up to 20 of each. For each photo found, run text recognition and return the photo path, the date taken, whether it is a receipt or a rating plate, and the recognised text. If there are no results, say zero matches.'

Result (images read):
- Photos/Phone/2023-06/IMG_20230602_181404.jpg, taken 2023-06-02 18:14:04, receipt: "HOMEHUB APPLIANCES, 77 Harbor Road, Port Alder OR, Date: 06/02/2023, Order HH-230602-1187, Cust: Alex Rivera, Nordvik WM-7 Front Load Washer, SN NV7-2305-60912 $899.00, Delivery $59.00, TOTAL $958.00, Paid: CARD ****4417, Warranty: see manufacturer card".
- Plates: Photos/Phone/2024-03/IMG_20240316_190455.jpg (NORDVIK, ADW-4820, NV48-2203-1187) and Photos/Phone/2022-01/IMG_20220115_101233.jpg (HomeHub, FR-560, HH56-2201-30647).
Parent: keep the washer receipt photo (names a washing machine). Plates name neither washing machine nor model WM-7: ignored.

Document extract: every PDF receipt name points to a different product (dishwasher, fridge, TV, soundbar), so none is sent. The photo text is the purchase record (stated in the evidence list).
Date reading: 06/02/2023 is ambiguous. US store (Port Alder OR), order number HH-230602-1187 (YYMMDD 230602) and photo date taken 2023-06-02 all give 2 June 2023.
Brand Nordvik, model WM-7, serial NV7-2305-60912, store HomeHub Appliances, order HH-230602-1187, $899.00. One washer purchase, no choice to make.

## Step 2

Series: WM-7 has fewer than four digits, so left out.

DELEGATE file-agent:
'Find files whose names contain any of: warranty, guarantee, garantie, protection, plan, care, extended, registration, certificate, terms, conditions, Nordvik, WM-7, HomeHub. Search folders whose names contain Warranty, Receipts, Scans, Documents, Home or Appliances first, then all user files. File types: documents and images. Return full path, file name, size and modified date for each, up to 50. If there are no results, say zero matches.'

Result, 9 files: Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf; Home/Appliances/Washer/WM-7_manual.pdf; Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf; Manuals/Nordvik_ADW-48xx_UserManual.pdf; Scans/Lumora_TV_warranty.pdf; Scans/2024/Brightline_EPP_terms_scan.pdf; Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf; Documents/Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf; Photos/Phone/2023-06/ is not matched (name IMG_...). The receipt has no protection plan, so no scan-folder fallback.

DELEGATE document-agent:
'With intent locate_content and evidence mode focused, check these files: Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf, Home/Appliances/Washer/WM-7_manual.pdf, Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf, Manuals/Nordvik_ADW-48xx_UserManual.pdf, Scans/Lumora_TV_warranty.pdf, Scans/2024/Brightline_EPP_terms_scan.pdf, Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf, Documents/Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf. List only the files that are a warranty, guarantee, protection plan or warranty registration for Nordvik WM-7, or a plan bought with order HH-230602-1187. For each, quote the line that shows it. If none match, say zero matches.'
Result: 1 file. Nordvik_WM-7_warranty_card.pdf: "Product: WM-7 Front Load Washing Machine".

DELEGATE document-agent:
'Answer from these files only: Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf. With intent period and answer mode table, return for each document: the provider, each coverage (full parts and labour, parts only, or named components such as motor, compressor or panel) with its term, how the start date is defined, and any printed start or end date. With intent condition, return the exclusions and the claim procedure (phone, email or web form exactly as written, required attachments). Also return any plan number, registration number and serial number written on it. Quote the page or section for each answer.'
Result (page 1): Nordvik; parts and labor 2 years, "from the original purchase date", "Warranty starts on the date of original retail purchase. A dated receipt is required."; no printed dates; "This warranty has no extended components." Exclusions: misuse, installation faults, hoses, cosmetic damage, repairs by unauthorized persons, commercial use. Claim: "Email claims@nordvik-support.example or call 1-800-555-0188 (Mon-Fri 8:00-18:00 Pacific)", receipt copy and serial plate photo. No plan, registration or serial number.

## Step 3

Reconcile skipped: only one document path (the receipt is a photo). Parent check: receipt photo says Nordvik WM-7; the card is for WM-7 Nordvik: consistent. No plate photo of this washer.
Arithmetic: bought 2 Jun 2023 + 2 years = ended 2 Jun 2025. No other coverage. Label: Not covered, ended 2 Jun 2025.

## Step 4

DELEGATE file-agent:
'Find files whose names contain any of: manual, guide, instructions, handbook, quick start, WM-7, Nordvik. Search folders whose names contain Manuals, Documents, Downloads, Home or Appliances first, then all user files. File type: documents. Return full path, file name, size and modified date, up to 20. If there are no results, say zero matches.'
Result: Home/Appliances/Washer/WM-7_manual.pdf (9774); Manuals/Nordvik_ADW-48xx_UserManual.pdf (17516); Downloads/ADW-48xx_manual (1).pdf (17516); Manuals/Zentro_AX3000_Router_Manual.pdf; Home/Appliances/Fridge/FR-560_owner_manual.pdf; Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf; Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf.
Parent: named both a manual and brand or model: WM-7_manual.pdf (WM-7) and Nordvik_ADW-48xx_UserManual.pdf (Nordvik).

DELEGATE document-agent:
'With intent locate_content, check these files: Home/Appliances/Washer/WM-7_manual.pdf, Manuals/Nordvik_ADW-48xx_UserManual.pdf. List only the files that are the user manual or guide for Nordvik WM-7, and quote the line that shows it. If none match, say zero matches.'
Result: WM-7_manual.pdf only ("Nordvik Washing Machine, Model series WM-7"). The ADW manual is a dishwasher manual.

DELEGATE document-agent (code alone, user gave no description):
'Using only Home/Appliances/Washer/WM-7_manual.pdf, with intent locate_content and answer mode table, find what the manual says about error code F21. Return the matching rows of the error-code and troubleshooting tables (problem, cause, what to do) in the order printed, the safety warnings that apply to those steps, any steps that need a qualified technician, and any statement that user repairs affect the warranty. Give the page or section for each item.'
Result: Section 4 Error codes, p.6: F21 "Drain fault: water not draining." Action: pause, power off, clean the drain pump filter behind the lower right panel (have a towel ready), check the drain hose for kinks, restart. Section 5, p.7: "Water left in drum, F21": blocked pump filter or hose; clean pump filter, check hose. Safety p.3: "Disconnect power before any cleaning near electrical parts"; "Do not open the door while the drum is turning." No technician-only step. No statement on user repairs (the card, not the manual, excludes unauthorized repairs).
Safety lead rule: F21 is a drain fault without a leak, so the safety line does not move above the product line.

## Final answer (status completed)

    Product: Nordvik WM-7 (washing machine), bought 2 Jun 2023 at HomeHub Appliances
    Coverage: Not covered. Bought 2 Jun 2023 + 2-year warranty = ended 2 Jun 2025. The card has no extended components.
    Safety first: Disconnect power before any cleaning near electrical parts (manual p.3). Do not open the door while the drum is turning.
    Try this (manual section 4, p.6, and section 5, p.7):
      1. Pause the machine and switch it off.
      2. Clean the drain pump filter behind the lower right panel; have a towel ready.
      3. Check the drain hose for kinks.
      4. Restart.
    Evidence:
      - Photos/Phone/2023-06/IMG_20230602_181404.jpg (receipt photo): 06/02/2023, HomeHub Appliances, order HH-230602-1187, Nordvik WM-7, serial NV7-2305-60912, $899.00
      - Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf: 2 years parts and labor from purchase, exclusions, claim contact
      - Home/Appliances/Washer/WM-7_manual.pdf: F21 drain fault
    Notes: Date 06/02/2023 read as 2 June (US store, order number 230602, photo taken 2 Jun 2023). The receipt exists only as a photo. The recent E15 photo was ignored because you named F21. No claim draft because nothing is covered.

Delegations: 9 = photo-agent 2, file-agent 3, document-agent 4 (locate, terms, manual confirm, F21). No knowledge-agent call.
