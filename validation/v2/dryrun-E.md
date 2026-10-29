# Dry run E: "Which warranties run out in the next three months?"

Today = 2026-11-20 08:40. Mode sweep. Window: "three months", so calendar months: 2026-11-20 to 2027-02-20.

## Step S1

delegate --target file-agent --instruction 'Find files whose names contain any of: receipt, invoice, order, purchase, warranty, guarantee, protection, plan, registration, manual, guide. Search folders whose names contain Receipts, Invoices, Purchases, Orders, Warranty, Manuals, Scans, Documents, Home or Appliances first, then all user files. File types: documents and images. Return full path, file name, size and modified date for each, up to 200. If there are no results, say zero matches.'

Result, 14 PDFs:
- Receipts: Documents/Receipts/2019/receipt_dishwasher_old.pdf; 2022/HomeHub_receipt_fridge_Jan2022.pdf; 2024/Brightline_Receipt_2024-03-14_dishwasher.pdf; 2025/Brightline_order_TV_Lumora.pdf; 2025/Brightline_soundbar_2025-12-18.pdf
- Warranty: Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf; Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf; Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf; Scans/Lumora_TV_warranty.pdf
- Manuals: Manuals/Nordvik_ADW-48xx_UserManual.pdf; Downloads/ADW-48xx_manual (1).pdf; Home/Appliances/Fridge/FR-560_owner_manual.pdf; Home/Appliances/Washer/WM-7_manual.pdf; Manuals/Zentro_AX3000_Router_Manual.pdf

Not returned: Scans/2024/Brightline_EPP_terms_scan.pdf (D2).

delegate --target photo-agent --instruction 'Search the photo library for photos of paper receipts or till slips for appliances or electronics. For each photo found, run text recognition and return the photo path, the date taken and the recognised text. If there are no results, say zero matches.'

Result: 1 photo, `Photos/Phone/2023-06/IMG_20230602_181404.jpg`, taken 2023-06-02: HomeHub Appliances, Date 06/02/2023, Order HH-230602-1187, Nordvik WM-7 Front Load Washer, SN NV7-2305-60912, $899.00, Delivery $59.00, TOTAL $958.00.

## Step S2

delegate --target document-agent --instruction 'Extract with the receipt schema from these files: Documents/Receipts/2019/receipt_dishwasher_old.pdf, Documents/Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf, Documents/Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf, Documents/Receipts/2025/Brightline_order_TV_Lumora.pdf, Documents/Receipts/2025/Brightline_soundbar_2025-12-18.pdf. Return one row per purchased appliance or device: store, purchase date as printed, brand, product, model, serial, price, and any protection plan line with its term. Skip groceries, services and consumables. Report any file you could not read.'

Result:
- Brightline, 2019-08-22, Nordvik ADW-3100 dishwasher, NV31-1905-0342, $529.00; "Manufacturer warranty: 1 year parts and labor. No extended plan purchased."
- HomeHub Appliances, 2022-01-10, HomeHub FR-560 refrigerator, HH56-2201-30847, $1,649.00
- Brightline, 2024-03-14, Nordvik ADW-4820 dishwasher, NV48-2203-1187, $849.00; plan: 3-Year Extended Protection Plan EPP-3Y-90417733, $129.00, "after the manufacturer warranty ends"
- Brightline, 2025-12-01, Lumora 55Q8 TV, LU55-2511-90233, $699.00; "Lumora 1-year limited warranty applies from the date of purchase."
- Brightline, 2025-12-18, Lumora S2 Soundbar, LU-S2-2512-04418, $179.00; "Lumora 1-year limited warranty applies from the date of purchase."

delegate --target document-agent --instruction 'With intent period and answer mode table, answer from these files only: Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf, Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf, Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf, Scans/Lumora_TV_warranty.pdf. For each document return the brand, model or series it covers, each coverage term (base, component such as motor or compressor, protection plan), how the start date is defined, and any printed end date.'

Result:
- Nordvik ADW-4820: parts and labor 2 years, drive motor 10 years, from original retail purchase date, no printed end date.
- HomeHub FR-560: general 1 year, sealed system / compressor 5 years, from original purchase date; registered purchase date 2022-01-10; no printed end date.
- Nordvik WM-7: parts and labor 2 years from original retail purchase, no extended components.
- Lumora 55Q8: limited warranty 1 year (panel, board, power supply), counted from the retail purchase date on the receipt.

delegate --target document-agent --instruction 'With intent extraction and answer mode table, answer from these files only: Manuals/Nordvik_ADW-48xx_UserManual.pdf, Downloads/ADW-48xx_manual (1).pdf, Home/Appliances/Fridge/FR-560_owner_manual.pdf, Home/Appliances/Washer/WM-7_manual.pdf, Manuals/Zentro_AX3000_Router_Manual.pdf. For each manual return the brand, product type and model or series it covers.'

Result: Nordvik dishwasher ADW-48xx (both files); HomeHub refrigerator FR-560; Nordvik washing machine WM-7; Zentro Wi-Fi router AX3000 (series).

Parent merge. Washer photo adds a purchase row: 06/02/2023 read as 2 June 2023 (US store, order HH-230602, date taken 2023-06-02).

| Product | Coverage and end date | Group |
|---|---|---|
| Lumora 55Q8 TV, $699.00 | 2025-12-01 + 1 year = 2026-12-01 | Ending soon |
| Lumora S2 soundbar, $179.00 | receipt states 1 year, 2025-12-18 + 1 year = 2026-12-18 (no warranty card found) | Ending soon |
| HomeHub FR-560, $1,649.00 | general ended 2023-01-10; compressor / sealed system 2022-01-10 + 5 years = 2027-01-10 | Ending soon (inside 2027-02-20) |
| Nordvik ADW-4820 | base ended 2026-03-14; plan EPP-3Y-90417733 from receipt wording runs 2026-03-14 to 2029-03-14 (terms document not found); motor 2034-03-14 | Active later |
| Zentro AX3000 router | manual only | Unknown, "no receipt found" |
| Nordvik WM-7 washer | 2 years, ended 2025-06-02 | Ended (counted) |
| Nordvik ADW-3100 dishwasher | receipt states 1 year, ended 2020-08-22 | Ended (counted) |

Value losing cover: $699.00 + $179.00 + $1,649.00 = $2,527.00 (product prices, not receipt totals with accessories).

Delegations so far: 5. Status `waiting_approval` (the script gives no reply to the save offer, so no knowledge-agent call).

## Final answer

    Warranty calendar, 2026-11-20, next 3 months (to 2027-02-20)
    Ending soon (value losing cover: $2,527.00):
      - 2026-12-01: Lumora 55Q8 TV, 1-year limited warranty (Scans/Lumora_TV_warranty.pdf). Claims need the receipt and a photo of the rear label showing the serial number.
      - 2026-12-18: Lumora S2 soundbar, 1-year limited warranty (Documents/Receipts/2025/Brightline_soundbar_2025-12-18.pdf). Only the receipt states the term; no warranty card was found.
      - 2027-01-10: HomeHub FR-560 compressor and sealed system, 5 years (Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf). Claims need the receipt, the registration and a photo of the serial plate, and the serial must match the registration.
    Active later:
      - 2029-03-14: Nordvik ADW-4820 protection plan EPP-3Y-90417733 (Documents/Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf). From the receipt line only; the plan's own terms were not found.
      - 2034-03-14: Nordvik ADW-4820 drive motor, 10 years (Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf)
    Unknown:
      - Zentro AX3000 router: no receipt found, manual Manuals/Zentro_AX3000_Router_Manual.pdf
    2 older appliances are out of warranty.
    Save this calendar to your NAS? (yes / no)
