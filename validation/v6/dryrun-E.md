# Dry run E (v6): "Which warranties run out in the next three months?"

Today 2026-11-20 08:40. Paths relative to the library root. Skill followed literally, v6 text. Round 1.

## Intake
Mode: sweep. The user names months, so calendar months: window 2026-11-20 to 2027-02-20.

## Step S1
### Delegation 1 to file-agent
> Find files whose names contain any of: receipt, invoice, order, purchase, warranty, guarantee, protection, plan, registration, terms, conditions, manual, guide. Also list every document in folders whose names contain Receipts, Warranty, Manuals, Scans or Appliances. File types: documents and images. Return full path, file name, size and modified date for each, up to 200. If there are no results, say zero matches.

Result: 15. By name: Documents/Receipts/2019/receipt_dishwasher_old.pdf; Documents/Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf; Documents/Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf; Documents/Receipts/2025/Brightline_order_TV_Lumora.pdf; Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf; Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf; Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf; Scans/Lumora_TV_warranty.pdf; Scans/2024/Brightline_EPP_terms_scan.pdf; Manuals/Nordvik_ADW-48xx_UserManual.pdf; Manuals/Zentro_AX3000_Router_Manual.pdf; Home/Appliances/Washer/WM-7_manual.pdf; Home/Appliances/Fridge/FR-560_owner_manual.pdf; Downloads/ADW-48xx_manual (1).pdf. By folder only: Documents/Receipts/2025/Brightline_soundbar_2025-12-18.pdf.

### Delegation 2 to photo-agent
> Search the photo library for photos of paper receipts or till slips for appliances or electronics, and for photos of appliance rating plates or serial labels, newest first, up to 30 of each. For each photo found, say whether it is a receipt or a rating plate, run text recognition and return the photo path, the date taken and the recognised text. If there are no results, say zero matches.

Result: receipt: Photos/Phone/2023-06/IMG_20230602_181404.jpg (2023-06-02; HomeHub Appliances, Date 06/02/2023, Order HH-230602-1187, Nordvik WM-7 Front Load Washer, SN NV7-2305-60912, $899.00, Delivery $59.00, "Warranty: see manufacturer card"). Plates: IMG_20240316_190455.jpg (Nordvik ADW-4820, NV48-2203-1187); IMG_20220115_101233.jpg (HomeHub FR-560, HH56-2201-30647).

## Step S2
### Delegation 3 to document-agent
> Extract with the receipt schema and max files 200 from these files: Documents/Receipts/2019/receipt_dishwasher_old.pdf, Documents/Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf, Documents/Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf, Documents/Receipts/2025/Brightline_order_TV_Lumora.pdf, Documents/Receipts/2025/Brightline_soundbar_2025-12-18.pdf. Return one row per purchased appliance or device: store, purchase date as printed, brand, product, model, serial, price, any warranty term printed on the receipt, and any protection plan line with its term. Skip groceries, services and consumables. Report any file you could not read.

Result (5 rows):
- Brightline, 2019-08-22, Nordvik dishwasher ADW-3100, NV31-1905-0342, $529.00, "1 year parts and labor", no plan.
- HomeHub Appliances, 2022-01-10, HomeHub refrigerator FR-560, HH56-2201-30847, $1,649.00, no term, no plan.
- Brightline, 2024-03-14, Nordvik dishwasher ADW-4820, NV48-2203-1187, $849.00, no term; plan "3-Year Extended Protection Plan" EPP-3Y-90417733, covers ADW-4820 after the manufacturer warranty ends.
- Brightline, 2025-12-01, Lumora 55Q8 TV, LU55-2511-90233, $699.00, "Lumora 1-year limited warranty applies from the date of purchase."
- Brightline, 2025-12-18, Lumora S2 soundbar, LU-S2-2512-04418, $179.00, "Lumora 1-year limited warranty applies from the date of purchase."
Services (haul-away, delivery) and accessories (installation kit, wall mount) skipped.

### Delegation 4 to document-agent
> With intent period, answer mode table and max files 200, answer from these files only: Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf, Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf, Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf, Scans/Lumora_TV_warranty.pdf, Scans/2024/Brightline_EPP_terms_scan.pdf. For each document return the brand, model or series it covers, each coverage term (base, component such as motor or compressor, protection plan), how the start date is defined, and any printed end date.

Result:
- Nordvik ADW-4820: parts and labor 2 years, drive motor 10 years, from purchase. No printed dates.
- Nordvik WM-7: parts and labor 2 years from purchase, no extended components.
- HomeHub FR-560: general 1 year, sealed system / compressor 5 years, from purchase; registered serial HH56-2201-30847.
- Lumora 55Q8: limited warranty 1 year (panel, board, power supply), from the retail purchase date.
- Brightline EPP-3Y-90417733 for Nordvik ADW-4820: printed start 2026-03-14, printed end 2029-03-14.

### Delegation 5 to document-agent
> With intent extraction and answer mode table, answer from these files only: Manuals/Nordvik_ADW-48xx_UserManual.pdf, Downloads/ADW-48xx_manual (1).pdf, Home/Appliances/Washer/WM-7_manual.pdf, Home/Appliances/Fridge/FR-560_owner_manual.pdf, Manuals/Zentro_AX3000_Router_Manual.pdf. For each manual return the brand, product type and model or series it covers.

Result: Nordvik dishwasher ADW-48xx (two files); Nordvik washing machine WM-7; HomeHub refrigerator FR-560; Zentro Wi-Fi router AX3000.

Parent matching and arithmetic:
- Lumora 55Q8 TV: 1 Dec 2025 + 1 year = 1 Dec 2026. In window.
- Lumora S2 soundbar: no warranty document; term from the receipt: 18 Dec 2025 + 1 year = 18 Dec 2026. In window.
- HomeHub FR-560: general ended 10 Jan 2023; compressor and sealed system 10 Jan 2022 + 5 years = 10 Jan 2027. In window. Plate serial HH56-2201-30647 differs from the receipt and registration: "serial to check before claiming".
- Nordvik ADW-4820: base ended 14 Mar 2026; plan to 14 Mar 2029 (printed); motor to 14 Mar 2034. Active later.
- Nordvik WM-7 (receipt photo, 06/02/2023 read as 2 Jun 2023 from the US store, order number and photo date): 2 years, ended 2 Jun 2025. Ended.
- Nordvik ADW-3100: 22 Aug 2019 + 1 year = ended 22 Aug 2020. Ended.
- Zentro AX3000: manual only: "no receipt found".
Value losing cover, item prices only: $699.00 + $179.00 + $1,649.00 = $2,527.00.

## Step S3, calendar shown
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

Status: `waiting_approval`.

Delegations: 5 (file-agent 1, photo-agent 1, document-agent 3).

## Check against expected
Window 2026-11-20 to 2027-02-20. Ending soon $2,527: TV 12-01, soundbar 12-18, fridge compressor 2027-01-10. Active later: plan 2029-03-14, motor 2034-03-14. Unknown: router. 2 older out of warranty. waiting_approval. PASS.
