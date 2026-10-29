# Dry run B: "Washing machine shows F21. Is it still under warranty?"

Today 2026-11-20 08:40. Paths relative to `project/testdata/home-library/`. Mode: fault. Product: washing machine. Code: F21 (from the user).

## D1 photo-agent (Step 0)
Instruction: `Search photos taken in the last 48 hours, up to 2026-11-20 08:40, for pictures of an appliance control panel or display showing an error code, or of an appliance rating plate or serial label. For each photo found, run text recognition and return the photo path, the time taken and the recognised text. If there are no results, say zero matches.`
Result: 1 photo, `Photos/Phone/2026-11/IMG_20261120_083012.jpg`, taken 2026-11-20 08:30:12, text "NORDVIK  E15  POWER  CYCLE  DELAY  START".

Parent: the user's code is F21, the photo shows E15. The skill has no rule for a photo code that differs from the user's code. Judgment call: the user's own words win, the photo is treated as another appliance and ignored for code and brand (see defect). Not placed in the evidence list.

## D2 file-agent (Step 1, names)
Brand and model unknown, so left out.
Instruction: `Find files whose names contain any of: receipt, invoice, order, purchase, quittung, washing machine. Search folders whose names contain Receipts, Invoices, Purchases, Orders, Documents, Scans or Downloads first, then all user files. File types: documents and images. Return full path, file name, type, size and modified date for each, up to 50. If there are no results, say zero matches.`
Result, 5 files (all in Receipts folders): 2019/receipt_dishwasher_old.pdf, 2022/HomeHub_receipt_fridge_Jan2022.pdf, 2024/Brightline_Receipt_2024-03-14_dishwasher.pdf, 2025/Brightline_order_TV_Lumora.pdf, 2025/Brightline_soundbar_2025-12-18.pdf. No name says washer (the washer files are named WM-7).

## D3 photo-agent (Step 1)
Instruction: `Search the photo library for photos of a paper receipt or till slip, and for photos of an appliance rating plate or serial label, that mention washing machine. For each photo found, run text recognition and return the photo path, the date taken, whether it is a receipt or a rating plate, and the recognised text. If there are no results, say zero matches.`
Result, 1 photo: `Photos/Phone/2023-06/IMG_20230602_181404.jpg`, taken 2023-06-02 18:14:04, receipt. Text: "HOMEHUB APPLIANCES, 77 Harbor Road, Port Alder OR; Date: 06/02/2023  Order HH-230602-1187; Cust: Alex Rivera; Nordvik WM-7 Front Load Washer, SN NV7-2305-60912 $899.00; Delivery $59.00; TOTAL $958.00; Paid: CARD ****4417; Warranty: see manufacturer card".

Parent: all five receipt PDFs name other products, so no document is sent to the document-agent (no real path to fill the extract instruction). The photo text is the purchase record. Brand Nordvik, model WM-7 (fewer than four digits, no series), store HomeHub Appliances, order HH-230602-1187, serial NV7-2305-60912, price $899.00.
Date reading: 06/02/2023 is ambiguous. US store (Port Alder OR), order number HH-230602 (YYMMDD) and photo date taken 2023-06-02 all give 2 June 2023.

## D4 file-agent (Step 2)
Slots: brand Nordvik, model WM-7, store HomeHub (series omitted); receipt lists no plan.
Instruction: `Find files whose names contain any of: warranty, guarantee, garantie, protection, plan, care, extended, registration, certificate, terms, conditions, Nordvik, WM-7, HomeHub. Search folders whose names contain Warranty, Receipts, Scans, Documents, Home or Appliances first, then all user files. File types: documents and images. Return full path, file name, size and modified date for each, up to 50. If there are no results, say zero matches.`
Result, 8 files: Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf, Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf, Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf, Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf, Home/Appliances/Washer/WM-7_manual.pdf, Manuals/Nordvik_ADW-48xx_UserManual.pdf, Scans/2024/Brightline_EPP_terms_scan.pdf, Scans/Lumora_TV_warranty.pdf.

## D5 document-agent (Step 2, confirm)
Instruction: `With intent locate_content and evidence mode focused, check these files: Documents/Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf, Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf, Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf, Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf, Home/Appliances/Washer/WM-7_manual.pdf, Manuals/Nordvik_ADW-48xx_UserManual.pdf, Scans/2024/Brightline_EPP_terms_scan.pdf, Scans/Lumora_TV_warranty.pdf. List only the files that are a warranty, guarantee, protection plan or warranty registration for Nordvik WM-7, or a plan bought with order HH-230602-1187. For each, quote the line that shows it. If none match, say zero matches.`
Result: 1 match, Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf: "Product: WM-7 Front Load Washing Machine". (The ADW-4820 card is a different model.)

## D6 document-agent (Step 2, terms)
Instruction: `Answer from these files only: Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf. With intent period and answer mode table, return for each document: the provider, each coverage (full parts and labour, parts only, or named components such as motor, compressor or panel) with its term, how the start date is defined, and any printed start or end date. With intent condition, return the exclusions and the claim procedure (phone, email or web form exactly as written, required attachments). Also return any plan number, registration number and serial number written on it. Quote the page or section for each answer.`
Result (p.1): Nordvik. Parts and labor 2 years. "Warranty starts on the date of original retail purchase. A dated receipt is required." No printed dates, no serial or plan number. "This warranty has no extended components." Exclusions: misuse, installation faults, hoses, cosmetic damage, repairs by unauthorized persons, commercial use. Claim: "Email claims@nordvik-support.example or call 1-800-555-0188 (Mon-Fri 8:00-18:00 Pacific)", dated receipt and serial plate photo required.

Step 3: no reconcile call. The receipt is a photo, only one document path exists, and the skill says to send only document paths and compare photo text myself. My comparison: brand Nordvik and model WM-7 agree on the receipt photo and the card. No plate photo of the washer is on the NAS.
Coverage: 2023-06-02 + 2 years = ended 2025-06-02, about 17 months ago. No extended component, no plan on the receipt. Label Not covered. No claim draft (Step 5 only for Covered, Partly covered, Unclear).

## D7 file-agent (Step 4)
Instruction: `Find files whose names contain any of: manual, guide, instructions, handbook, quick start, WM-7, Nordvik. Search folders whose names contain Manuals, Documents, Downloads, Home or Appliances first, then all user files. File type: documents. Return full path, file name, size and modified date, up to 20. If there are no results, say zero matches.`
Result, 7 files: Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf, Downloads/ADW-48xx_manual (1).pdf, Home/Appliances/Fridge/FR-560_owner_manual.pdf, Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf, Home/Appliances/Washer/WM-7_manual.pdf, Manuals/Nordvik_ADW-48xx_UserManual.pdf, Manuals/Zentro_AX3000_Router_Manual.pdf.

## D8 document-agent (Step 4, confirm manual; wording adapted)
Instruction: `With intent locate_content and evidence mode focused, check these files: [the 7 paths above]. List only the files that are the user manual for Nordvik WM-7. For each, quote the line that shows it. If none match, say zero matches.`
Result: 1 match, Home/Appliances/Washer/WM-7_manual.pdf: "Nordvik Washing Machine / Model series WM-7". One confirmed file, no duplicate check.

## D9 document-agent (Step 4, manual)
Instruction: `Using only Home/Appliances/Washer/WM-7_manual.pdf, with intent locate_content and answer mode table, find what the manual says about error code F21. Return the matching rows of the error-code and troubleshooting tables (problem, cause, what to do) in the order printed, the safety warnings that apply to those steps, any steps that need a qualified technician, and any statement that user repairs affect the warranty. Give the page or section for each item.`
Result: s.4 p.6: "F21 | Drain fault: water not draining. | Pause, power off, clean the drain pump filter behind the lower right panel (have a towel ready), check the drain hose for kinks, restart." s.5 p.7: "Water left in drum, F21 | Blocked pump filter or hose | Clean pump filter, check hose". Safety s.1 p.3: "Disconnect power before any cleaning near electrical parts."; "Do not open the door while the drum is turning." No technician-only steps. No statement about user repairs affecting the warranty.

## Final answer (status completed)

```
Product: Nordvik WM-7 (washing machine), bought 2 Jun 2023 at HomeHub Appliances
Coverage: Not covered. Bought 2 Jun 2023 + 2-year Nordvik parts and labor warranty = ended 2 Jun 2025. The card has no extended components and the receipt lists no protection plan.
Safety first: Disconnect power before any cleaning near electrical parts. (manual s.1 p.3)
Try this (manual s.4 p.6, s.5 p.7):
  1. Pause the machine and power it off.
  2. Clean the drain pump filter behind the lower right panel (have a towel ready).
  3. Check the drain hose for kinks.
  4. Restart.
  Technician only: none stated in the manual.
Evidence:
  - Photos/Phone/2023-06/IMG_20230602_181404.jpg: purchase date 2 Jun 2023, model WM-7, serial NV7-2305-60912, order HH-230602-1187, $899.00 (receipt exists only as this photo)
  - Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf: 2 years parts and labor from purchase, no extended components, exclusions, claim contact
  - Home/Appliances/Washer/WM-7_manual.pdf: F21 drain fault steps
Notes: The receipt date 06/02/2023 is read as 2 June 2023 (US store, order number HH-230602, photo taken 2023-06-02). No rating-plate photo of the washer is on the NAS. Today's photo (IMG_20261120_083012.jpg) shows E15, not F21, so I did not use it.
```
No claim draft because the label is Not covered.

Delegations: 9 (photo 2, file 3, document 4). The receipt-extract and reconcile calls were skipped for lack of document paths.
