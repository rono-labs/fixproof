# Dry run H (v8): "When does the dishwasher warranty run out?"

Today 2026-11-20 08:40. Paths relative to testdata/home-library/. v8 SKILL.md, experts played from the real files (method as in dryrun-A).

## Intake
Fault mode, coverage-only path. Product: dishwasher (file-agent: DW; photo-agent: dishwasher). No fault, no code.

## Step 0
Skipped (no fault, no code, product known). See observation O1 on the delegation-order line.

## Step 1
**1. file-agent**
> Read only; do not change any file. Find files whose names contain any of: receipt, invoice, order, purchase, quittung, dishwasher, DW. Search folders whose names contain Receipts, Invoices, Purchases, Orders, Documents, Scans or Downloads first, then the rest of the home folder and the shared folders this user can access. File types: documents and images. Return full path, file name, type, size and modified date for each, up to 50. If there are no results, say zero matches.

Result (matcher): 7. 2024 and 2019 dishwasher receipts, fridge receipt, TV order, Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf, Manuals/Nordvik_ADW-48xx_UserManual.pdf, Downloads/ADW-48xx_manual (1).pdf ("DW" inside "ADW").

**2. photo-agent** (receipts mentioning dishwasher; plates). Result: receipts zero; plates IMG_20240316_190455.jpg (EXIF 2024:03:16 19:04:55, NORDVIK ADW-4820, NV48-2203-1187), IMG_20220115_101233.jpg (FR-560).

**3. document-agent**
> Read only; do not change any file. Extract the purchase details from these receipts and invoices: Documents/Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf, Documents/Receipts/2019/receipt_dishwasher_old.pdf. [...]

Result: as run A (ADW-4820 2024-03-14, NV48-2203-1187, plan EPP-3Y-90417733; ADW-3100 2019-08-22). Plate settles the 2024 unit; 2019 to Notes.

## Step 2
**4. file-agent** (warranty terms + Nordvik, ADW-4820, ADW-48xx, Brightline). Result: same 10 as A.

**5. document-agent** (content check, ADW-4820 card + EPP scan, v8 "Read the contents" wording). Result: both match.

**6. document-agent** (terms). Result: card 2 y parts and labor, motor 10 y, from purchase; plan printed 2026-03-14 to 2029-03-14.

## Step 3
**7. document-agent** (reconcile receipt, card, plan). Result: no differences found. Base ended 14 Mar 2026; plan to 14 Mar 2029 (printed start kept, one-day gap noted); motor to 14 Mar 2034. Coverage-only: skip Steps 4 and 5.

## Final answer
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
Status `completed`. Delegations: 7 (photo 1, file 2, document 4).

## Check
ADW-4820 by plate; base ended 14 Mar 2026, plan to 14 Mar 2029, motor to 14 Mar 2034; no checklist, no draft, manual offered in one line; completed. PASS.
