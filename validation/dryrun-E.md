# Dry run E (v8): "Which warranties run out in the next three months?"

Today 2026-11-20 08:40. Paths relative to testdata/home-library/. v8 SKILL.md, experts played from the real files (method as in dryrun-A).

## Intake
Sweep mode. Calendar months: window 2026-11-20 to 2027-02-20. Delegation order (new line): file-agent and photo-agent, then document-agent, then knowledge-agent after approval.

## Step S1
**1. file-agent**
> Read only; do not change any file. Find files whose names contain any of: receipt, invoice, order, purchase, warranty, guarantee, protection, plan, registration, terms, conditions, manual, guide. Also list every document in folders whose names contain Receipts, Warranty, Manuals, Scans or Appliances. File types: documents and images. Return full path, file name, size and modified date for each, up to 200. If there are no results, say zero matches.

Result (matcher): 15. By name: 4 receipts (2019, 2022, 2024, 2025 TV order), ADW-4820 card, WM-7 card, FR-560 registration, Lumora TV warranty, EPP terms scan, 5 manuals (two ADW-48xx, WM-7, FR-560, Zentro). By folder only: Documents/Receipts/2025/Brightline_soundbar_2025-12-18.pdf.

**2. photo-agent**
> Read only; do not change any photo. Search the photo library for photos of paper receipts or till slips for appliances or electronics, and for photos of appliance rating plates or serial labels, newest first, up to 30 of each. [...]

Result: receipt IMG_20230602_181404.jpg (Nordvik WM-7, NV7-2305-60912, 06/02/2023, $899.00); plates ADW-4820 (NV48-2203-1187), FR-560 (HH56-2201-30647).

## Step S2
**3. document-agent**
> Read only; do not change any file. Extract the purchase details from these receipts and invoices, up to 200 files: Documents/Receipts/2019/receipt_dishwasher_old.pdf, Documents/Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf, Documents/Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf, Documents/Receipts/2025/Brightline_order_TV_Lumora.pdf, Documents/Receipts/2025/Brightline_soundbar_2025-12-18.pdf. Return one row per purchased appliance or device: [...] Skip groceries, services and consumables. Report any file you could not read.

Result: ADW-3100 2019-08-22 $529.00 (1 year); FR-560 2022-01-10 $1,649.00 (HH56-2201-30847, no term); ADW-4820 2024-03-14 $849.00 + plan EPP-3Y-90417733; Lumora 55Q8 2025-12-01 $699.00 (1 year); Lumora S2 soundbar 2025-12-18 $179.00 (LU-S2-2512-04418, 1 year). "receipt schema" and "max files 200" wording removed; "up to 200 files" keeps the cap. Same rows as v6.

**4. document-agent**
> Read only; do not change any file. Answer from these files only, up to 200: Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf, Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf, Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf, Scans/Lumora_TV_warranty.pdf, Scans/2024/Brightline_EPP_terms_scan.pdf. Return a table with one row per document: [...] Skip files that hold no warranty terms. Report any file you could not read.

Result: ADW-4820 2 y / motor 10 y; WM-7 2 y; FR-560 general 1 y, compressor 5 y; Lumora 55Q8 1 y; EPP printed 2026-03-14 to 2029-03-14. None skipped (all hold terms).

**5. document-agent**
> Read only; do not change any file. Answer from these files only: Manuals/Nordvik_ADW-48xx_UserManual.pdf, Downloads/ADW-48xx_manual (1).pdf, Home/Appliances/Washer/WM-7_manual.pdf, Home/Appliances/Fridge/FR-560_owner_manual.pdf, Manuals/Zentro_AX3000_Router_Manual.pdf. Return a table with one row per manual: the brand, product type and model or series it covers. If a file is not a manual, leave it out. Report any file you could not read.

Result: Nordvik dishwasher ADW-48xx (x2), Nordvik washing machine WM-7, HomeHub refrigerator FR-560, Zentro router AX3000.

Parent: TV 1 Dec 2026; soundbar 18 Dec 2026 (term from receipt); fridge compressor 10 Jan 2027, serial to check; ADW-4820 plan 14 Mar 2029, motor 14 Mar 2034; WM-7 ended 2 Jun 2025; ADW-3100 ended 22 Aug 2020; Zentro: no receipt found. Value: 699 + 179 + 1,649 = $2,527.

## Step S3
```
Warranty calendar, 20 Nov 2026, next 3 months (to 20 Feb 2027)
Ending soon (value losing cover: $2,527):
  - 1 Dec 2026: Lumora 55Q8 TV, 1-year limited warranty (Scans/Lumora_TV_warranty.pdf). Claims need the receipt and a photo of the rear label showing the serial.
  - 18 Dec 2026: Lumora S2 soundbar, 1-year warranty stated on the receipt (Documents/Receipts/2025/Brightline_soundbar_2025-12-18.pdf). No warranty card on the NAS; keep the receipt.
  - 10 Jan 2027: HomeHub FR-560 fridge, compressor and sealed system (Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf). Serial to check before claiming: plate HH56-2201-30647, registration HH56-2201-30847. Claims need receipt, registration and a serial-plate photo.
Active later:
  - 14 Mar 2029: Nordvik ADW-4820 dishwasher, protection plan EPP-3Y-90417733 (Scans/2024/Brightline_EPP_terms_scan.pdf)
  - 14 Mar 2034: Nordvik ADW-4820 dishwasher, drive motor (Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf)
Unknown:
  - Zentro AX3000 router: no receipt found, manual Manuals/Zentro_AX3000_Router_Manual.pdf
2 older appliances are out of warranty.
Save this calendar to your NAS? (yes / no)
```
Status `waiting_approval`. Delegations: 5 (file 1, photo 1, document 3). The new "on no" line (report `completed`, "not saved") is not reached in this scenario.

## Check
Window to 2027-02-20; ending soon $2,527: TV 12-01, soundbar 12-18, fridge compressor 2027-01-10; active later plan 2029-03-14, motor 2034-03-14; unknown router; 2 older; waiting_approval. PASS. Identical to v6.
