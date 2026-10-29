# Dry run E: "Which warranties run out in the next three months?"

Today 2026-11-20 08:40. Paths are relative to the library root; all files modified 2026-10-29. Skill followed literally.

## Intake
Mode: sweep. Window: three calendar months from today = 2026-11-20 to 2027-02-20. No Step 0 (fault mode only).

## Step S1
### Delegation 1 to file-agent
Instruction as sent:
> Find files whose names contain any of: receipt, invoice, order, purchase, warranty, guarantee, protection, plan, registration, terms, conditions, manual, guide. Also list every document in folders whose names contain Receipts, Warranty, Manuals, Scans or Appliances. File types: documents and images. Return full path, file name, size and modified date for each, up to 200. If there are no results, say zero matches.

Result (file-agent): 15 matches.
  - Documents/Receipts/2019/receipt_dishwasher_old.pdf (2794)
  - Documents/Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf (2733)
  - Documents/Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf (2969)
  - Documents/Receipts/2025/Brightline_order_TV_Lumora.pdf (2762)
  - Documents/Receipts/2025/Brightline_soundbar_2025-12-18.pdf (2694, in a Receipts folder)
  - Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf (2960)
  - Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf (2737)
  - Home/Appliances/Fridge/FR-560_owner_manual.pdf (9127)
  - Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf (2681)
  - Home/Appliances/Washer/WM-7_manual.pdf (9774)
  - Manuals/Nordvik_ADW-48xx_UserManual.pdf (17516)
  - Manuals/Zentro_AX3000_Router_Manual.pdf (6029)
  - Downloads/ADW-48xx_manual (1).pdf (17516)
  - Scans/Lumora_TV_warranty.pdf (2560)
  - Scans/2024/Brightline_EPP_terms_scan.pdf (3271)

### Delegation 2 to photo-agent
Instruction as sent:
> Search the photo library for photos of paper receipts or till slips for appliances or electronics, and for photos of appliance rating plates or serial labels, newest first, up to 30 of each. For each photo found, say whether it is a receipt or a rating plate, run text recognition and return the photo path, the date taken and the recognised text. If there are no results, say zero matches.

Result (photo-agent): 3 photos.
  - Rating plate: Photos/Phone/2024-03/IMG_20240316_190455.jpg, 2024-03-16 19:04:55. NORDVIK / MODEL: ADW-4820 / SERIAL: NV48-2203-1187 / 120V 60Hz 15A 1800W / MFD 2023-12.
  - Receipt: Photos/Phone/2023-06/IMG_20230602_181404.jpg, 2023-06-02 18:14:04. HOMEHUB APPLIANCES / Date: 06/02/2023  Order HH-230602-1187 / Nordvik WM-7 Front Load Washer / SN NV7-2305-60912 $899.00 / Delivery $59.00 / TOTAL $958.00 / Warranty: see manufacturer card.
  - Rating plate: Photos/Phone/2022-01/IMG_20220115_101233.jpg, 2022-01-15 10:12:33. HomeHub / MODEL: FR-560 / SERIAL: HH56-2201-30647.

## Step S2
### Delegation 3 to document-agent
Instruction as sent:
> Extract with the receipt schema and max files 200 from these files: Documents/Receipts/2019/receipt_dishwasher_old.pdf, Documents/Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf, Documents/Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf, Documents/Receipts/2025/Brightline_order_TV_Lumora.pdf, Documents/Receipts/2025/Brightline_soundbar_2025-12-18.pdf. Return one row per purchased appliance or device: store, purchase date as printed, brand, product, model, serial, price, any warranty term printed on the receipt, and any protection plan line with its term. Skip groceries, services and consumables. Report any file you could not read.

Result (document-agent): 5 rows, all read.
  - Brightline Electronics, 2019-08-22, Nordvik, dishwasher ADW-3100, serial NV31-1905-0342, $529.00, "1 year parts and labor", no plan.
  - HomeHub Appliances, 2022-01-10, HomeHub, refrigerator FR-560, serial HH56-2201-30847, $1,649.00, no term printed, no plan.
  - Brightline Electronics, 2024-03-14, Nordvik, dishwasher ADW-4820, serial NV48-2203-1187, $849.00, no term printed; plan "3-Year Extended Protection Plan" EPP-3Y-90417733, 3 years, $129.00.
  - Brightline Electronics, 2025-12-01, Lumora, 55Q8 QLED TV, serial LU55-2511-90233, $699.00, "1-year limited warranty from the date of purchase", no plan.
  - Brightline Electronics, 2025-12-18, Lumora, S2 Soundbar, serial LU-S2-2512-04418, $179.00, "1-year limited warranty from the date of purchase", no plan.
  (Skipped as services or accessories: haul-away, delivery and setup, installation kit, wall mount.)

### Delegation 4 to document-agent
Instruction as sent:
> With intent period, answer mode table and max files 200, answer from these files only: Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf, Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf, Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf, Scans/Lumora_TV_warranty.pdf, Scans/2024/Brightline_EPP_terms_scan.pdf. For each document return the brand, model or series it covers, each coverage term (base, component such as motor or compressor, protection plan), how the start date is defined, and any printed end date.

Result (document-agent):
  - Nordvik ADW-4820: parts and labor 2 years; drive motor 10 years (wash motor and circulation pump motor, parts only after year 2); starts on date of original retail purchase; no printed end.
  - HomeHub FR-560: general parts and labor 1 year; sealed system and compressor 5 years; from original purchase date (registered purchase date 2022-01-10); no printed end.
  - Nordvik WM-7: parts and labor 2 years from original retail purchase; no extended components.
  - Lumora 55Q8: limited warranty 1 year on panel, board and power supply, counted from the retail purchase date on the receipt.
  - Brightline plan EPP-3Y-90417733 for Nordvik ADW-4820 serial NV48-2203-1187: plan start 2026-03-14, plan end 2029-03-14 (printed), begins when the manufacturer warranty ends.

### Delegation 5 to document-agent
Instruction as sent:
> With intent extraction and answer mode table, answer from these files only: Downloads/ADW-48xx_manual (1).pdf, Home/Appliances/Fridge/FR-560_owner_manual.pdf, Home/Appliances/Washer/WM-7_manual.pdf, Manuals/Nordvik_ADW-48xx_UserManual.pdf, Manuals/Zentro_AX3000_Router_Manual.pdf. For each manual return the brand, product type and model or series it covers.

Result (document-agent): ADW-48xx (both copies): Nordvik dishwasher, series ADW-48xx. FR-560: HomeHub refrigerator, FR-560. WM-7: Nordvik washing machine, WM-7. AX3000: Zentro Wi-Fi router, AX3000.

Parent matching: the photo receipt (2 Jun 2023, date read as 2 June: US store, order HH-230602, photo date) is the washing machine purchase, brand Nordvik WM-7, matched to the WM-7 card: 2 years = 2 Jun 2025, ended. The soundbar has no warranty document (the TV card is for the 55Q8), so its term comes from the receipt. Router: manual only, "no receipt found". The plate for the fridge differs from the registration serial (30647 vs 30847): "serial to check before claiming". The ADW plate matches its receipt.

## Step S3 calendar
Window end 2027-02-20. Arithmetic: TV 1 Dec 2025 + 1 year = 1 Dec 2026; soundbar 18 Dec 2025 + 1 year = 18 Dec 2026; fridge compressor 10 Jan 2022 + 5 years = 10 Jan 2027 (general ended 10 Jan 2023); ADW-4820 base ended 14 Mar 2026, plan to 14 Mar 2029, motor to 14 Mar 2034; WM-7 ended 2 Jun 2025; ADW-3100 ended 22 Aug 2020. Value losing cover: $699.00 + $179.00 + $1,649.00 = $2,527 (item prices from the receipts, excluding delivery and accessories).

Offer to save. Status `waiting_approval`. The scenario ends here (no reply, nothing saved, no knowledge-agent call).

## Final answer

```
Warranty calendar, 2026-11-20, next 3 months (to 2027-02-20)
Ending soon (value losing cover: $2,527):
  - 2026-12-01: Lumora 55Q8 TV, limited warranty on panel, board and power supply (Scans/Lumora_TV_warranty.pdf; receipt Documents/Receipts/2025/Brightline_order_TV_Lumora.pdf). Claims need the receipt and a photo of the rear label with the serial; no such photo is on the NAS.
  - 2026-12-18: Lumora S2 Soundbar, 1-year limited warranty stated on the receipt (Documents/Receipts/2025/Brightline_soundbar_2025-12-18.pdf). No warranty card on the NAS, so the receipt is your proof.
  - 2027-01-10: HomeHub FR-560 compressor and sealed system, 5 years (Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf; receipt Documents/Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf). Serial to check before claiming: registration 30847, plate photo 30647. Claims need the receipt, the registration and a plate photo whose serial matches.
Active later:
  - 2029-03-14: Nordvik ADW-4820 protection plan EPP-3Y-90417733 (Scans/2024/Brightline_EPP_terms_scan.pdf)
  - 2034-03-14: Nordvik ADW-4820 drive motor, 10 years, parts only after year 2 (Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf)
Unknown:
  - Zentro AX3000: no receipt found, manual Manuals/Zentro_AX3000_Router_Manual.pdf
2 older appliances are out of warranty (the washing machine, from a receipt photo, and the 2019 dishwasher).
Save this calendar to your NAS? (yes / no)
```

Status: `waiting_approval`

Delegations: 5 (file-agent x1, photo-agent x1, document-agent x3).
