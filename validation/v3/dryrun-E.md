# Dry run E: "Which warranties run out in the next three months?"

Today 2026-11-20 08:40. Paths relative to `project/testdata/home-library/`. Mode: sweep. Window: three calendar months from today, to 2027-02-20 (92 days).

## D1 file-agent (S1)
Instruction: `Find files whose names contain any of: receipt, invoice, order, purchase, warranty, guarantee, protection, plan, registration, manual, guide. Search folders whose names contain Receipts, Invoices, Purchases, Orders, Warranty, Manuals, Scans, Documents, Home or Appliances first, then all user files. File types: documents and images. Return full path, file name, size and modified date for each, up to 200. If there are no results, say zero matches.`
Result, 14 files:
- Receipts: 2019/receipt_dishwasher_old.pdf, 2022/HomeHub_receipt_fridge_Jan2022.pdf, 2024/Brightline_Receipt_2024-03-14_dishwasher.pdf, 2025/Brightline_order_TV_Lumora.pdf, 2025/Brightline_soundbar_2025-12-18.pdf
- Warranty: Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf, Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf, Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf, Scans/Lumora_TV_warranty.pdf
- Manuals: Manuals/Nordvik_ADW-48xx_UserManual.pdf, Downloads/ADW-48xx_manual (1).pdf, Home/Appliances/Fridge/FR-560_owner_manual.pdf, Home/Appliances/Washer/WM-7_manual.pdf, Manuals/Zentro_AX3000_Router_Manual.pdf

Not returned: Scans/2024/Brightline_EPP_terms_scan.pdf. Its name contains none of the S1 terms ("terms" and "scan" are not listed), and the sweep has no step that opens Scans folders. Parent does not know it exists.

## D2 photo-agent (S1)
Instruction: `Search the photo library for photos of paper receipts or till slips for appliances or electronics. For each photo found, run text recognition and return the photo path, the date taken and the recognised text. If there are no results, say zero matches.`
Result, 1 photo: `Photos/Phone/2023-06/IMG_20230602_181404.jpg`, taken 2023-06-02 18:14:04, text "HOMEHUB APPLIANCES ... Date: 06/02/2023 Order HH-230602-1187 ... Nordvik WM-7 Front Load Washer SN NV7-2305-60912 $899.00 Delivery $59.00 TOTAL $958.00 ... Warranty: see manufacturer card".

## D3 document-agent (S2, receipts)
Instruction: `Extract with the receipt schema from these files: Documents/Receipts/2019/receipt_dishwasher_old.pdf, Documents/Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf, Documents/Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf, Documents/Receipts/2025/Brightline_order_TV_Lumora.pdf, Documents/Receipts/2025/Brightline_soundbar_2025-12-18.pdf. Return one row per purchased appliance or device: store, purchase date as printed, brand, product, model, serial, price, and any protection plan line with its term. Skip groceries, services and consumables. Report any file you could not read.`
Result, 5 rows:
1. Brightline, 2019-08-22, Nordvik, dishwasher ADW-3100, NV31-1905-0342, $529.00, no plan ("Manufacturer warranty: 1 year parts and labor").
2. HomeHub Appliances, 2022-01-10, HomeHub, refrigerator FR-560, HH56-2201-30847, $1,649.00, no plan.
3. Brightline, 2024-03-14, Nordvik, dishwasher ADW-4820, NV48-2203-1187, $849.00, plan: 3-Year Extended Protection Plan EPP-3Y-90417733, $129.00, "Covers ADW-4820 after the manufacturer warranty ends. Terms provided separately."
4. Brightline, 2025-12-01, Lumora, 55 in. QLED TV 55Q8, LU55-2511-90233, $699.00, no plan ("1-year limited warranty from the date of purchase").
5. Brightline, 2025-12-18, Lumora, S2 Soundbar, LU-S2-2512-04418, $179.00, no plan ("1-year limited warranty from the date of purchase").
(Wall mount, installation kit, delivery and haul-away skipped as services or accessories.)
Photo row added: HomeHub, 2023-06-02 (US store, order HH-230602, photo date; read as 2 June), Nordvik, washer WM-7, NV7-2305-60912, $899.00, no plan.

## D4 document-agent (S2, warranties)
Instruction: `With intent period and answer mode table, answer from these files only: Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf, Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf, Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf, Scans/Lumora_TV_warranty.pdf. For each document return the brand, model or series it covers, each coverage term (base, component such as motor or compressor, protection plan), how the start date is defined, and any printed end date.`
Result:
- Nordvik ADW-4820: parts and labor 2 years, drive motor 10 years (parts only after year 2), from original retail purchase, no printed end.
- HomeHub FR-560: general 1 year, sealed system and compressor 5 years, general from original purchase date, registered purchase date 2022-01-10, no printed end.
- Nordvik WM-7: parts and labor 2 years from original retail purchase, no extended components.
- Lumora 55Q8: 1 year, panel, board and power supply, from retail purchase date on the receipt, no printed end.

## D5 document-agent (S2, manuals)
Instruction: `With intent extraction and answer mode table, answer from these files only: Manuals/Nordvik_ADW-48xx_UserManual.pdf, Downloads/ADW-48xx_manual (1).pdf, Home/Appliances/Fridge/FR-560_owner_manual.pdf, Home/Appliances/Washer/WM-7_manual.pdf, Manuals/Zentro_AX3000_Router_Manual.pdf. For each manual return the brand, product type and model or series it covers.`
Result: Nordvik dishwasher ADW-48xx (two identical-looking files); HomeHub refrigerator FR-560; Nordvik washing machine WM-7; Zentro Wi-Fi router AX3000.

## Matching and arithmetic (parent)
- Dishwasher ADW-3100 (2019): 1 year from receipt, ended 2020-08-22. Out of warranty.
- Washer WM-7: 2023-06-02 + 2 years = ended 2025-06-02. Out of warranty.
- Dishwasher ADW-4820: base 2024-03-14 + 2 years = ended 2026-03-14. Receipt plan line says the 3-year plan covers it after the manufacturer warranty ends, so by the plan-start rule it starts 2026-03-14 and runs 3 years to 2029-03-14. No plan terms document was collected, so this end date is calculated from the receipt line and not verified. Drive motor 10 years to 2034-03-14 (parts only after year 2).
- TV 55Q8: 2025-12-01 + 1 year = 2026-12-01. In window.
- Soundbar S2: 2025-12-18 + 1 year = 2026-12-18 (term stated on the receipt, no warranty document). In window.
- Fridge FR-560: general ended 2023-01-10; sealed system 2022-01-10 + 5 years = 2027-01-10. In window (before 2027-02-20).
- Router Zentro AX3000: manual only, no receipt.
Value losing cover: 699.00 + 179.00 + 1,649.00 = $2,527.00 (product prices from receipts, excluding mount and delivery).

## Final answer (status waiting_approval)

```
Warranty calendar, 2026-11-20, next 3 months (92 days, to 2027-02-20)
Ending soon (value losing cover: $2,527.00):
  - 2026-12-01: Lumora 55Q8 TV, 1-year limited warranty on panel, board and power supply (Scans/Lumora_TV_warranty.pdf). Claims need the receipt and a photo of the rear label showing the serial number.
  - 2026-12-18: Lumora S2 soundbar, 1-year limited warranty stated on the receipt (Documents/Receipts/2025/Brightline_soundbar_2025-12-18.pdf). No warranty card on the NAS; the claim needs the receipt.
  - 2027-01-10: HomeHub FR-560 fridge, 5-year sealed system and compressor warranty (Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf). Claims need the receipt, the registration and a photo of the serial plate, and the serial must match the registration.
Active later:
  - 2029-03-14: Nordvik ADW-4820 dishwasher, 3-year protection plan EPP-3Y-90417733 (receipt Documents/Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf; calculated from the receipt line, plan terms not found in this search)
  - 2034-03-14: Nordvik ADW-4820 drive motor, 10 years, parts only after year 2 (Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf)
Unknown:
  - Zentro AX3000 router: no receipt found, manual Manuals/Zentro_AX3000_Router_Manual.pdf
2 older appliances are out of warranty.
Save this calendar to your NAS? (yes / no)
Notes: the washer receipt exists only as a photo (Photos/Phone/2023-06/IMG_20230602_181404.jpg), date 06/02/2023 read as 2 June 2023 (US store, order number, photo date). The Nordvik washer (ended 2025-06-02) and the 2019 dishwasher (ended 2020-08-22) are the two out of warranty.
```

Delegations: 5 (photo 1, file 1, document 3). No save (waiting for the user).
