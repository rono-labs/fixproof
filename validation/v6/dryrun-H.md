# Dry run H (v6): "When does the dishwasher warranty run out?"

Today 2026-11-20 08:40. Paths relative to the library root. Skill followed literally, v6 text. Round 1.

## Intake
Mode: fault mode, coverage-only path. Product: dishwasher (file-agent: DW; photo-agent: dishwasher). No fault, no code, no brand or model.

## Step 0
Skipped (v6 fix 6): the user reports no fault and gives no code, and the product is known. In v5 this step returned only the unrelated E15 photo.

## Step 1
### Delegation 1 to file-agent
> Find files whose names contain any of: receipt, invoice, order, purchase, quittung, dishwasher, DW. Search folders whose names contain Receipts, Invoices, Purchases, Orders, Documents, Scans or Downloads first, then all user files. File types: documents and images. Return full path, file name, type, size and modified date for each, up to 50. If there are no results, say zero matches.

Result: 7: Documents/Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf; Documents/Receipts/2019/receipt_dishwasher_old.pdf; Documents/Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf; Documents/Receipts/2025/Brightline_order_TV_Lumora.pdf; Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf; Manuals/Nordvik_ADW-48xx_UserManual.pdf; Downloads/ADW-48xx_manual (1).pdf ("DW" matches inside "ADW").

### Delegation 2 to photo-agent
> Search the photo library for photos of a paper receipt or till slip that mention dishwasher, and for photos of any appliance rating plate or serial label. Newest first, up to 20 of each. For each photo found, run text recognition and return the photo path, the date taken, whether it is a receipt or a rating plate, and the recognised text. If there are no results, say zero matches.

Result: receipts: zero matches. Plates: Photos/Phone/2024-03/IMG_20240316_190455.jpg (2024-03-16 19:04:55, NORDVIK ADW-4820, NV48-2203-1187, MFD 2023-12); Photos/Phone/2022-01/IMG_20220115_101233.jpg (HomeHub FR-560, HH56-2201-30647).

### Delegation 3 to document-agent
Kept (v6 rule 5): the two dishwasher receipts. Fridge and TV receipts name other products; the warranty card and both manuals are not receipts.

> Extract purchase details with the receipt schema from these files: Documents/Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf, Documents/Receipts/2019/receipt_dishwasher_old.pdf. If a file returns no data with the receipt schema, try the invoice schema. For each file return store, order number, purchase date exactly as printed, product description, brand, model number, serial number if printed, price, any warranty term printed on the receipt, and every other line item, especially any protection plan, extended warranty or care plan with its plan number and term. Report any file you could not read.

Result: as run A. 2024: Brightline, BL-2024-0314-55871, 2024-03-14, Nordvik ADW-4820, NV48-2203-1187, $849.00, plan EPP-3Y-90417733 $129.00. 2019: Brightline, BL-2019-0822-20318, 2019-08-22, Nordvik ADW-3100, NV31-1905-0342, $529.00, 1 year parts and labor, no plan.

Parent: the ADW-4820 plate matches exactly one receipt. 2024 chosen, 2019 to Notes. Brand Nordvik, series ADW-48xx, store Brightline.

## Step 2
### Delegation 4 to file-agent
> Find files whose names contain any of: warranty, guarantee, garantie, protection, plan, care, extended, registration, certificate, terms, conditions, Nordvik, ADW-4820, ADW-48xx, Brightline. Search folders whose names contain Warranty, Receipts, Scans, Documents, Home or Appliances first, then all user files. File types: documents and images. Return full path, file name, size and modified date for each, up to 50. If there are no results, say zero matches.

Result: the same 10 as run A.

### Delegation 5 to document-agent
> With intent locate_content and evidence mode focused, check these files: Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf, Scans/2024/Brightline_EPP_terms_scan.pdf. List only the files that are a warranty, guarantee, protection plan or warranty registration for Nordvik ADW-4820 or the series ADW-48xx, or a plan bought with order BL-2024-0314-55871. For each, quote the line that shows it. If none match, say zero matches.

Result: both match (as run A).

### Delegation 6 to document-agent
> Answer from these files only: Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf, Scans/2024/Brightline_EPP_terms_scan.pdf. With intent period and answer mode table, return for each document: the provider, each coverage (full parts and labour, parts only, or named components such as motor, compressor or panel) with its term, how the start date is defined, and any printed start or end date. With intent condition, return the exclusions and the claim procedure (phone, email or web form exactly as written, required attachments). Also return any plan number, registration number and serial number written on it. Quote the page or section for each answer.

Result: as run A. Card: parts and labor 2 years, motor 10 years, from purchase. Plan: printed start 2026-03-14 ("the day after the 2-year manufacturer warranty ends"), end 2029-03-14.

## Step 3
### Delegation 7 to document-agent
> Reconcile these files and report every difference in brand, model number, serial number, purchase date, plan start or end date, or owner name: Documents/Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf, Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf, Scans/2024/Brightline_EPP_terms_scan.pdf. For each difference give both values and the file each came from. If they all agree, say no differences found.

Result: no differences found.

Parent: plate serial agrees. Base 14 Mar 2024 + 2 years = ended 14 Mar 2026. Plan: calculated start 15 Mar 2026 under v6 rule 4, printed 14 Mar 2026; printed kept, one-day gap noted. Plan runs to 14 Mar 2029. Motor 14 Mar 2034. Coverage-only: list each coverage, skip Steps 4 and 5, one-line manual offer, `completed`.

## Final answer (coverage-only template)
```
Product: Nordvik ADW-4820 (dishwasher), bought 14 Mar 2024 at Brightline Electronics
Coverage:
  - Manufacturer parts and labor (2 years): ended 14 Mar 2026 (Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf)
  - Brightline protection plan EPP-3Y-90417733: runs to 14 Mar 2029 (Scans/2024/Brightline_EPP_terms_scan.pdf)
  - Drive motor (10 years, parts only after year 2): runs to 14 Mar 2034 (Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf)
Need the manual's steps for a fault? Tell me what it is doing.
Evidence: Documents/Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf, Photos/Phone/2024-03/IMG_20240316_190455.jpg, Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf, Scans/2024/Brightline_EPP_terms_scan.pdf
Notes: A 2019 Nordvik ADW-3100 (receipt 22 Aug 2019) also exists; the plate photo matches the 2024 unit. The plan says it starts the day after the warranty ends (15 Mar 2026) but prints 14 Mar 2026; the printed date is kept.
```

Status: `completed`.

Delegations: 7 (photo-agent 1, file-agent 2, document-agent 4). v5: 8.

## Check against expected
ADW-4820 chosen by the plate photo, base ended 14 Mar 2026, plan to 14 Mar 2029, motor to 14 Mar 2034, no checklist, no draft, one-line manual offer, completed. PASS.
