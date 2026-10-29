# Dry run E: "Which warranties run out in the next three months?"

Today 2026-11-20 08:40. Paths relative to project/testdata/home-library/. Mode: sweep. Window: three calendar months, 2026-11-20 to 2027-02-20. No Step 0 (fault mode only).

## Step S1

DELEGATE file-agent:
'Find files whose names contain any of: receipt, invoice, order, purchase, warranty, guarantee, protection, plan, registration, terms, conditions, manual, guide. Also list every document in folders whose names contain Receipts, Warranty, Manuals, Scans or Appliances. File types: documents and images. Return full path, file name, size and modified date for each, up to 200. If there are no results, say zero matches.'
Result, 15 files:
- Receipts: Documents/Receipts/2019/receipt_dishwasher_old.pdf; Documents/Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf; Documents/Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf; Documents/Receipts/2025/Brightline_order_TV_Lumora.pdf; Documents/Receipts/2025/Brightline_soundbar_2025-12-18.pdf
- Warranty, plan, registration, scans: Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf; Scans/Lumora_TV_warranty.pdf; Scans/2024/Brightline_EPP_terms_scan.pdf; Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf; Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf
- Manuals: Manuals/Nordvik_ADW-48xx_UserManual.pdf; Manuals/Zentro_AX3000_Router_Manual.pdf; Downloads/ADW-48xx_manual (1).pdf; Home/Appliances/Washer/WM-7_manual.pdf; Home/Appliances/Fridge/FR-560_owner_manual.pdf

DELEGATE photo-agent:
'Search the photo library for photos of paper receipts or till slips for appliances or electronics, newest first, up to 30. For each photo found, run text recognition and return the photo path, the date taken and the recognised text. If there are no results, say zero matches.'
Result (image read): 1 photo. Photos/Phone/2023-06/IMG_20230602_181404.jpg, taken 2023-06-02 18:14:04: "HOMEHUB APPLIANCES, 77 Harbor Road, Port Alder OR, Date: 06/02/2023, Order HH-230602-1187, Cust: Alex Rivera, Nordvik WM-7 Front Load Washer, SN NV7-2305-60912 $899.00, Delivery $59.00, TOTAL $958.00, Paid: CARD ****4417, Warranty: see manufacturer card". The other phone and vacation photos are abstract pictures with no text and are not receipts.

## Step S2

DELEGATE document-agent:
'Extract with the receipt schema and max files 200 from these files: Documents/Receipts/2019/receipt_dishwasher_old.pdf, Documents/Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf, Documents/Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf, Documents/Receipts/2025/Brightline_order_TV_Lumora.pdf, Documents/Receipts/2025/Brightline_soundbar_2025-12-18.pdf. Return one row per purchased appliance or device: store, purchase date as printed, brand, product, model, serial, price, and any protection plan line with its term. Skip groceries, services and consumables. Report any file you could not read.'
Result (only the requested fields are returned; the printed manufacturer-warranty sentence on three receipts is not a requested field and is not returned):
1. Brightline Electronics, 2019-08-22, Nordvik, dishwasher, ADW-3100, NV31-1905-0342, $529.00, no plan.
2. HomeHub Appliances, 2022-01-10, HomeHub, French door refrigerator, FR-560, HH56-2201-30847, $1,649.00, no plan.
3. Brightline Electronics, 2024-03-14, Nordvik, dishwasher, ADW-4820, NV48-2203-1187, $849.00, plan: 3-Year Extended Protection Plan EPP-3Y-90417733, $129.00.
4. Brightline Electronics, 2025-12-01, Lumora, 55 in. QLED TV, 55Q8, LU55-2511-90233, $699.00, no plan.
5. Brightline Electronics, 2025-12-18, Lumora, soundbar, S2, LU-S2-2512-04418, $179.00, no plan.
Parent adds the photo row: HomeHub Appliances, 06/02/2023 read as 2 June 2023 (US store, order number 230602, date taken 2023-06-02), Nordvik, front load washer, WM-7, NV7-2305-60912, $899.00, no plan.

DELEGATE document-agent:
'With intent period, answer mode table and max files 200, answer from these files only: Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf, Scans/Lumora_TV_warranty.pdf, Scans/2024/Brightline_EPP_terms_scan.pdf, Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf, Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf. For each document return the brand, model or series it covers, each coverage term (base, component such as motor or compressor, protection plan), how the start date is defined, and any printed end date.'
Result:
- Nordvik ADW-4820: parts and labor 2 years; drive motor 10 years (parts only after year 2); start = original retail purchase date; no printed end date.
- Lumora 55Q8: limited warranty 1 year (panel, board, power supply); start = retail purchase date on the receipt; no printed end date.
- Brightline plan, Nordvik ADW-4820, plan EPP-3Y-90417733: 3 years; starts 2026-03-14 when the manufacturer warranty ends; printed end 2029-03-14.
- Nordvik WM-7: parts and labor 2 years; start = original retail purchase date; no extended components; no printed end date.
- HomeHub FR-560: general 1 year; sealed system and compressor 5 years; start = original purchase date (printed 2022-01-10); no printed end date.

DELEGATE document-agent:
'With intent extraction and answer mode table, answer from these files only: Manuals/Nordvik_ADW-48xx_UserManual.pdf, Manuals/Zentro_AX3000_Router_Manual.pdf, Downloads/ADW-48xx_manual (1).pdf, Home/Appliances/Washer/WM-7_manual.pdf, Home/Appliances/Fridge/FR-560_owner_manual.pdf. For each manual return the brand, product type and model or series it covers.'
Result: Nordvik, dishwasher, series ADW-48xx (twice, one file in Manuals and one in Downloads); Nordvik, washing machine, series WM-7; HomeHub, refrigerator, series FR-560; Zentro, Wi-Fi router, series AX3000.

Matching and arithmetic (today 2026-11-20, window end 2027-02-20):
- Lumora 55Q8, bought 1 Dec 2025 + 1 year = 1 Dec 2026: ending soon, $699.00.
- HomeHub FR-560, general ended 10 Jan 2023; compressor and sealed system 10 Jan 2022 + 5 years = 10 Jan 2027: ending soon, $1,649.00.
- Nordvik ADW-4820, base ended 14 Mar 2026; plan to 14 Mar 2029; motor 14 Mar 2034: active later.
- Nordvik WM-7, 2 Jun 2023 + 2 years = ended 2 Jun 2025: out of warranty.
- Lumora S2 soundbar: receipt found, no warranty document and no term in the extract, so "term unknown" (S2 rule).
- Nordvik ADW-3100 (2019): receipt found, no warranty document for ADW-3100 and no term in the extract, so "term unknown".
- Zentro AX3000: manual only, "no receipt found".

## Step S3 (status waiting_approval)

Value losing cover: $699.00 + $1,649.00 = $2,348.00.

    Warranty calendar, 2026-11-20, next 3 months (to 2027-02-20)
    Ending soon (value losing cover: $2,348.00):
      - 2026-12-01: Lumora 55Q8 limited warranty, panel, board and power supply (Scans/Lumora_TV_warranty.pdf; receipt Documents/Receipts/2025/Brightline_order_TV_Lumora.pdf). Claims need the receipt and a photo of the rear label showing the serial number.
      - 2027-01-10: HomeHub FR-560 compressor and sealed system (Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf). Claims need the receipt, the registration and a photo of the serial plate, and the serial must match the registration.
    Active later:
      - 2029-03-14: Nordvik ADW-4820 Brightline protection plan EPP-3Y-90417733 (Scans/2024/Brightline_EPP_terms_scan.pdf)
      - 2034-03-14: Nordvik ADW-4820 drive motor, parts only after year 2 (Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf)
    Unknown:
      - Lumora S2 soundbar: term unknown, receipt Documents/Receipts/2025/Brightline_soundbar_2025-12-18.pdf, no warranty document found
      - Nordvik ADW-3100 dishwasher (2019): term unknown, receipt Documents/Receipts/2019/receipt_dishwasher_old.pdf, no warranty document found
      - Zentro AX3000: no receipt found, manual Manuals/Zentro_AX3000_Router_Manual.pdf
    1 older appliance is out of warranty.
    Save this calendar to your NAS? (yes / no)

No reply, so no knowledge-agent call.

Observed gap: the soundbar receipt says "Lumora 1-year limited warranty applies from the date of purchase" (it ends 18 Dec 2026, inside the window, $179) and the 2019 receipt says "1 year parts and labor" (ended 22 Aug 2020), but the S2 instruction never asks for the receipt's printed warranty line, so both land in Unknown and the value is understated by $179.00. See D2.

Delegations: 5 = photo-agent 1, file-agent 1, document-agent 3.
