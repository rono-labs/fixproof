# Dry run E: "Which warranties run out in the next three months?"

Today = 2026-11-20. Paths are relative to `project/testdata/home-library/` (written `home-library/`). Expert results are emulated from `find`, `grep`, `pdftotext`.

## Intake
Mode: sweep. Window: three months, so 2026-11-20 to 2027-02-20. SKILL.md gives only "default 90 days" and no rule for converting months, so three calendar months is used (90 days would end 2027-02-18; no item falls between the two dates).

## Step S1. Collect purchase records

delegate --target file-agent --instruction 'Find every document that looks like a receipt, invoice, order confirmation, warranty card or protection plan in the user files. Search folders whose names contain Receipts, Invoices, Purchases, Orders, Warranty, Documents or Scans first, then all user files. Return full path, file name and modified date for each, up to 200. If there are no results, say zero matches.'

file-agent result (10 matches, all modified 2026-10-29). File-agent only matches names and text of documents. The phone photo IMG_20230602_181404.jpg is a receipt but has no receipt-like name, so it is not returned (defect D10).
- home-library/Documents/Receipts/2019/receipt_dishwasher_old.pdf
- home-library/Documents/Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf
- home-library/Documents/Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf
- home-library/Documents/Receipts/2025/Brightline_order_TV_Lumora.pdf
- home-library/Documents/Receipts/2025/Brightline_soundbar_2025-12-18.pdf
- home-library/Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf
- home-library/Scans/2024/Brightline_EPP_terms_scan.pdf
- home-library/Scans/Lumora_TV_warranty.pdf
- home-library/Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf
- home-library/Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf
- home-library/Downloads/utility_bill_oct.pdf (a bill, looks like an invoice; a service, not an appliance)
Not returned and not read: the router manual (Manuals/Zentro_AX3000_Router_Manual.pdf) and every manual, because S1 does not search for manuals (defect D11).

## Step S2. Extract products and terms

delegate --target document-agent --instruction 'Extract with the receipt schema from these files: home-library/Documents/Receipts/2019/receipt_dishwasher_old.pdf, home-library/Documents/Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf, home-library/Documents/Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf, home-library/Documents/Receipts/2025/Brightline_order_TV_Lumora.pdf, home-library/Documents/Receipts/2025/Brightline_soundbar_2025-12-18.pdf, home-library/Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf, home-library/Scans/2024/Brightline_EPP_terms_scan.pdf, home-library/Scans/Lumora_TV_warranty.pdf, home-library/Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf, home-library/Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf, home-library/Downloads/utility_bill_oct.pdf. Return one row per purchased appliance or device: store, purchase date, brand, product, model, serial, and any protection plan line with its term. Skip groceries, services and consumables.'

document-agent result (5 rows; the warranty cards and plan terms are not purchases, the utility bill is a service and is skipped):
1. Brightline Electronics, 2019-08-22, Nordvik dishwasher ADW-3100, serial NV31-1905-0342, no plan. Receipt text: "Manufacturer warranty: 1 year parts and labor."
2. HomeHub Appliances, 2022-01-10, HomeHub refrigerator FR-560, serial HH56-2201-30847, no plan.
3. Brightline Electronics, 2024-03-14, Nordvik dishwasher ADW-4820, serial NV48-2203-1187, plan "3-Year Extended Protection Plan" EPP-3Y-90417733.
4. Brightline Electronics, 2025-12-01, Lumora TV 55Q8, serial LU55-2511-90233, no plan. Receipt text: "Lumora 1-year limited warranty applies from the date of purchase."
5. Brightline Electronics, 2025-12-18, Lumora S2 Soundbar, serial LU-S2-2512-04418, no plan. Receipt text: "Lumora 1-year limited warranty applies from the date of purchase."

delegate --target document-agent --instruction 'Answer from these files only: home-library/Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf, home-library/Scans/2024/Brightline_EPP_terms_scan.pdf, home-library/Scans/Lumora_TV_warranty.pdf, home-library/Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf, home-library/Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf. For each document return the brand, model or model series it covers, each coverage term (base, component such as motor or compressor, protection plan), and how the start date is defined.'

document-agent result:
- Nordvik_ADW-4820_warranty_card.pdf: Nordvik ADW-4820; parts and labor 2 years; drive motor 10 years (parts only after year 2); starts at original retail purchase.
- Brightline_EPP_terms_scan.pdf: Brightline Protection Services, ADW-4820 serial NV48-2203-1187; plan EPP-3Y-90417733, start 2026-03-14 "the day after the 2-year manufacturer warranty ends", end 2029-03-14.
- Lumora_TV_warranty.pdf: Lumora 55Q8 TV; limited warranty 1 year for panel, board and power supply defects; counted from the retail purchase date on the receipt.
- Nordvik_WM-7_warranty_card.pdf: Nordvik WM-7; parts and labor 2 years from original purchase; no extended components.
- HomeHub_FR-560_warranty_registration.pdf: HomeHub FR-560; general parts and labor 1 year; sealed system / compressor 5 years; registered purchase date 2022-01-10; starts at original purchase.

Matching by brand and model:
- Dishwasher ADW-4820: receipt + card + plan.
- Fridge FR-560: receipt + registration.
- TV 55Q8: receipt + card.
- Soundbar S2: receipt only; the term (1 year from purchase) is stated on the receipt.
- Old dishwasher ADW-3100: receipt only; term stated on receipt (1 year).
- Washer WM-7: warranty card, but no receipt was returned in S1, so there is no purchase date to count from.

## Step S3. Calendar

End dates (coverage-rules.md):
- ADW-3100 receipt term: 2019-08-22 + 1 year = 2020-08-22, ended long ago. Left out (ended coverage shown only if the user asks for everything).
- ADW-4820 manufacturer warranty: 2024-03-14 + 2 years = 2026-03-14, ended. Protection plan: runs to 2029-03-14. Drive motor: 2024-03-14 + 10 years = 2034-03-14.
- FR-560 general warranty: 2022-01-10 + 1 year = 2023-01-10, ended. Sealed system / compressor: 2022-01-10 + 5 years = 2027-01-10.
- TV 55Q8: 2025-12-01 + 1 year = 2026-12-01.
- Soundbar S2: 2025-12-18 + 1 year = 2026-12-18.
- WM-7: term 2 years, purchase date unknown to this sweep, so no end date.

Window ends 2027-02-20. In the window: TV 2026-12-01, soundbar 2026-12-18, fridge compressor 2027-01-10.

## Final answer

    Warranty calendar, 2026-11-20, next 3 months (to 2027-02-20)
    Ending soon:
      - 2026-12-01: Lumora 55Q8 TV, 1-year limited warranty on panel, board and power supply (home-library/Scans/Lumora_TV_warranty.pdf, home-library/Documents/Receipts/2025/Brightline_order_TV_Lumora.pdf). A claim needs the receipt and a photo of the rear label showing the serial number.
      - 2026-12-18: Lumora S2 Soundbar, 1-year limited warranty stated on the receipt (home-library/Documents/Receipts/2025/Brightline_soundbar_2025-12-18.pdf). No warranty card is on the NAS; keep the receipt for any claim.
      - 2027-01-10: HomeHub FR-560 fridge, sealed system and compressor warranty (home-library/Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf). A claim needs the receipt, the registration and a photo of the serial plate, and the serial must match the registration.
    Active later:
      - 2029-03-14: Nordvik ADW-4820 dishwasher, 3-Year Extended Protection Plan EPP-3Y-90417733 (home-library/Scans/2024/Brightline_EPP_terms_scan.pdf)
      - 2034-03-14: Nordvik ADW-4820 dishwasher, drive motor warranty, parts only after year 2 (home-library/Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf)
    Term unknown:
      - Nordvik WM-7 washing machine: warranty card home-library/Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf (2 years from purchase), but no receipt was found by this search, so I cannot give an end date.
    Save this calendar to your NAS? (yes / no)

The router is not mentioned: the sweep never looked at manuals, so the Zentro AX3000 was not found (defect D11).

Status token: `waiting_approval`. The scenario ends with no user reply, so no knowledge-agent call.
