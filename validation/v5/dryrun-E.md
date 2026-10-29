# Dry run E: "Which warranties run out in the next three months?"

Today 2026-11-20 08:40. Paths are relative to the library root. Skill followed literally.

## Intake
Mode: sweep. Window: three calendar months from 20 Nov 2026, so 20 Nov 2026 to 20 Feb 2027.

## Step S1
### Delegation 1 to file-agent
Instruction as sent:
> Find files whose names contain any of: receipt, invoice, order, purchase, warranty, guarantee, protection, plan, registration, terms, conditions, manual, guide. Also list every document in folders whose names contain Receipts, Warranty, Manuals, Scans or Appliances. File types: documents and images. Return full path, file name, size and modified date for each, up to 200. If there are no results, say zero matches.

Result (file-agent played from the real files):
15 matches (name matches plus every document in the Receipts, Warranty, Manuals, Scans and Appliances folders, subfolders included):
  - Documents/Receipts/2019/receipt_dishwasher_old.pdf (pdf, 2794 bytes, modified 2026-10-29)
  - Documents/Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf (pdf, 2733 bytes, modified 2026-10-29)
  - Documents/Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf (pdf, 2969 bytes, modified 2026-10-29)
  - Documents/Receipts/2025/Brightline_order_TV_Lumora.pdf (pdf, 2762 bytes, modified 2026-10-29)
  - Documents/Receipts/2025/Brightline_soundbar_2025-12-18.pdf (pdf, 2694 bytes, modified 2026-10-29)
  - Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf (pdf, 2960 bytes, modified 2026-10-29)
  - Manuals/Nordvik_ADW-48xx_UserManual.pdf (pdf, 17516 bytes, modified 2026-10-29)
  - Manuals/Zentro_AX3000_Router_Manual.pdf (pdf, 6029 bytes, modified 2026-10-29)
  - Downloads/ADW-48xx_manual (1).pdf (pdf, 17516 bytes, modified 2026-10-29)
  - Scans/Lumora_TV_warranty.pdf (pdf, 2560 bytes, modified 2026-10-29)
  - Scans/2024/Brightline_EPP_terms_scan.pdf (pdf, 3271 bytes, modified 2026-10-29)
  - Home/Appliances/Fridge/FR-560_owner_manual.pdf (pdf, 9127 bytes, modified 2026-10-29)
  - Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf (pdf, 2737 bytes, modified 2026-10-29)
  - Home/Appliances/Washer/WM-7_manual.pdf (pdf, 9774 bytes, modified 2026-10-29)
  - Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf (pdf, 2681 bytes, modified 2026-10-29)
### Delegation 2 to photo-agent
Instruction as sent:
> Search the photo library for photos of paper receipts or till slips for appliances or electronics, newest first, up to 30. For each photo found, run text recognition and return the photo path, the date taken and the recognised text. If there are no results, say zero matches.

Result (photo-agent played from the real files):
1 photo: Photos/Phone/2023-06/IMG_20230602_181404.jpg, taken 2023-06-02 18:14:04. Text: HOMEHUB APPLIANCES, 77 Harbor Road, Port Alder OR / Date: 06/02/2023  Order HH-230602-1187 / Cust: Alex Rivera / Nordvik WM-7 Front Load Washer, SN NV7-2305-60912, $899.00 / Delivery $59.00 / TOTAL $958.00 / Paid: CARD ****4417 / Warranty: see manufacturer card.
Parent: results are not empty, so continue.

## Step S2
### Delegation 3 to document-agent
Instruction as sent:
> Extract with the receipt schema and max files 200 from these files: Documents/Receipts/2019/receipt_dishwasher_old.pdf, Documents/Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf, Documents/Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf, Documents/Receipts/2025/Brightline_order_TV_Lumora.pdf, Documents/Receipts/2025/Brightline_soundbar_2025-12-18.pdf. Return one row per purchased appliance or device: store, purchase date as printed, brand, product, model, serial, price, any warranty term printed on the receipt, and any protection plan line with its term. Skip groceries, services and consumables. Report any file you could not read.

Result (document-agent played from the real files):
5 rows, all files readable:
  1. Documents/Receipts/2019/receipt_dishwasher_old.pdf: Brightline Electronics, 2019-08-22, Nordvik ADW-3100 Dishwasher, serial NV31-1905-0342, $529.00, warranty term printed: 1 year parts and labor, no extended plan.
  2. Documents/Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf: HomeHub Appliances, 2022-01-10, HomeHub FR-560 French Door Refrigerator, serial HH56-2201-30847, $1,649.00, no term printed, no plan.
  3. Documents/Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf: Brightline Electronics, 2024-03-14, Nordvik ADW-4820 Dishwasher, serial NV48-2203-1187, $849.00, no term printed, plan line: 3-Year Extended Protection Plan, EPP-3Y-90417733, 3 years, $129.00.
  4. Documents/Receipts/2025/Brightline_order_TV_Lumora.pdf: Brightline Electronics, 2025-12-01, Lumora 55Q8 55 in. QLED TV, serial LU55-2511-90233, $699.00, term printed: 1-year limited warranty from the date of purchase.
  5. Documents/Receipts/2025/Brightline_soundbar_2025-12-18.pdf: Brightline Electronics, 2025-12-18, Lumora S2 Soundbar, serial LU-S2-2512-04418, $179.00, term printed: 1-year limited warranty from the date of purchase.
### Delegation 4 to document-agent
Instruction as sent:
> With intent period, answer mode table and max files 200, answer from these files only: Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf, Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf, Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf, Scans/Lumora_TV_warranty.pdf, Scans/2024/Brightline_EPP_terms_scan.pdf. For each document return the brand, model or series it covers, each coverage term (base, component such as motor or compressor, protection plan), how the start date is defined, and any printed end date.

Result (document-agent played from the real files):
  - Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf: Nordvik ADW-4820; parts and labor 2 years, drive motor 10 years (parts only after year 2); start = original retail purchase date; no printed end date.
  - Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf: Nordvik WM-7; parts and labor 2 years; no extended components; start = original retail purchase date; no printed end date.
  - Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf: HomeHub FR-560; general 1 year, sealed system and compressor 5 years; start = original purchase date; registration prints purchase date 2022-01-10; no printed end date.
  - Scans/Lumora_TV_warranty.pdf: Lumora 55Q8; limited warranty 1 year on panel, board and power supply; start = retail purchase date on the receipt; no printed end date.
  - Scans/2024/Brightline_EPP_terms_scan.pdf: Nordvik ADW-4820 (serial NV48-2203-1187), 3-Year Extended Protection Plan EPP-3Y-90417733; starts 2026-03-14, the day after the manufacturer warranty ends; printed end 2029-03-14.
### Delegation 5 to document-agent
Instruction as sent:
> With intent extraction and answer mode table, answer from these files only: Manuals/Nordvik_ADW-48xx_UserManual.pdf, Manuals/Zentro_AX3000_Router_Manual.pdf, Downloads/ADW-48xx_manual (1).pdf, Home/Appliances/Fridge/FR-560_owner_manual.pdf, Home/Appliances/Washer/WM-7_manual.pdf. For each manual return the brand, product type and model or series it covers.

Result (document-agent played from the real files):
  - Manuals/Nordvik_ADW-48xx_UserManual.pdf and Downloads/ADW-48xx_manual (1).pdf (identical title pages): Nordvik, dishwasher, series ADW-48xx.
  - Manuals/Zentro_AX3000_Router_Manual.pdf: Zentro, Wi-Fi router, series AX3000.
  - Home/Appliances/Fridge/FR-560_owner_manual.pdf: HomeHub, French door refrigerator, series FR-560.
  - Home/Appliances/Washer/WM-7_manual.pdf: Nordvik, washing machine, series WM-7.

Parent adds the receipt photo as a purchase row: Receipt that exists only as a photo, used as the purchase record: Photos/Phone/2023-06/IMG_20230602_181404.jpg (taken 2023-06-02 18:14:04). HomeHub Appliances, order HH-230602-1187, printed date 06/02/2023, Nordvik WM-7 Front Load Washer, serial NV7-2305-60912, $899.00, "Warranty: see manufacturer card".
Matching and arithmetic (today 20 Nov 2026, window ends 20 Feb 2027):
  - Lumora 55Q8 TV: 1 Dec 2025 + 1 year = 1 Dec 2026. In window.
  - Lumora S2 Soundbar: 18 Dec 2025 + 1 year = 18 Dec 2026, term from the receipt (no warranty card on the NAS). In window.
  - HomeHub FR-560: general 10 Jan 2022 + 1 year = 10 Jan 2023, ended; sealed system and compressor + 5 years = 10 Jan 2027. In window.
  - Nordvik ADW-4820: warranty ended 14 Mar 2026; plan to 14 Mar 2029 (printed); motor 14 Mar 2024 + 10 years = 14 Mar 2034. Active later.
  - Nordvik ADW-3100 (2019): 1 year, ended 22 Aug 2020. Out of warranty.
  - Nordvik WM-7: date 06/02/2023 is 2 Jun 2023 or 6 Feb 2023; + 2 years = 2 Jun 2025 or 6 Feb 2025, ended either way, so the reading does not change the group. Out of warranty.
  - Zentro AX3000: manual only, no receipt found.
Value losing cover: TV $699.00 + soundbar $179.00 + fridge $1,649.00 = $2,527.00.

## Step S3 (status waiting_approval)

Warranty calendar, 2026-11-20, next 3 months (to 2027-02-20)
Ending soon (value losing cover: $2,527.00):
  - 1 Dec 2026: Lumora 55Q8 TV, 1-year limited warranty on panel, board and power supply (Scans/Lumora_TV_warranty.pdf, receipt Documents/Receipts/2025/Brightline_order_TV_Lumora.pdf). Claims need the receipt and a photo of the rear label showing the serial number.
  - 18 Dec 2026: Lumora S2 Soundbar, 1-year limited warranty stated on the receipt (Documents/Receipts/2025/Brightline_soundbar_2025-12-18.pdf). No warranty document found on the NAS, so the claim contact is not found on the NAS, ask Brightline Electronics.
  - 10 Jan 2027: HomeHub FR-560 compressor and sealed system, 5 years (Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf, receipt Documents/Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf). Claims need the receipt, the registration and a photo of the serial plate, and the serial must match the registration.
Active later:
  - 14 Mar 2029: Nordvik ADW-4820 protection plan EPP-3Y-90417733 (Scans/2024/Brightline_EPP_terms_scan.pdf). Claims need the plan number, the receipt and the serial.
  - 14 Mar 2034: Nordvik ADW-4820 drive motor, 10 years, parts only after year 2 (Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf).
Unknown:
  - Zentro AX3000: no receipt found, manual Manuals/Zentro_AX3000_Router_Manual.pdf
2 older appliances are out of warranty (the 2019 Nordvik ADW-3100 dishwasher and the Nordvik WM-7 washing machine, whose receipt is a photo).
Save this calendar to your NAS? (yes / no)

Evidence list: all receipts, warranty cards, the plan terms and the manuals named above, plus Photos/Phone/2023-06/IMG_20230602_181404.jpg (receipt photo).
Notes: the WM-7 receipt is a photo dated 06/02/2023; it is out of warranty under either reading of the date. The sweep does not read rating plates, so serial numbers on photos are not compared; the fridge claim line only repeats that the registration says the serial must match. The duplicate ADW-48xx manual in Downloads is a second copy of the same manual.

Status: waiting_approval. No user reply given, so no knowledge-agent call.
