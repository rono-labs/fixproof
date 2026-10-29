# Dry run H: "When does the dishwasher warranty run out?"

Today 2026-11-20 08:40. Paths are relative to the library root; all files modified 2026-10-29. Skill followed literally. Coverage-only question: no fault reported.

## Intake
Mode: fault mode, coverage-only path (Step 3 note). Product: dishwasher (short names: DW). No symptom, code, brand or model.

## Step 0
### Delegation 1 to photo-agent
Instruction as sent:
> Search photos taken in the last 48 hours, up to 2026-11-20 08:40, for pictures of an appliance control panel or display showing an error code, or of an appliance rating plate or serial label. If the search cannot filter by time, take the 20 newest photos instead. For each photo found, up to 20, run text recognition and return the photo path, the time taken, the recognised text, and which kind of appliance the photo shows. If there are no results, say zero matches.

Result (photo-agent played from the real image):
1 match: Photos/Phone/2026-11/IMG_20261120_083012.jpg, taken 2026-11-20 08:30:12. Text: "NORDVIK", "E15", buttons POWER, CYCLE, DELAY, START. Appliance type not visible.

Parent: display only and the user's words ("When does the dishwasher warranty run out?") do not point to it. Ignored, so brand is still unknown.

## Step 1
### Delegation 2 to file-agent
Instruction as sent:
> Find files whose names contain any of: receipt, invoice, order, purchase, quittung, dishwasher, DW. Search folders whose names contain Receipts, Invoices, Purchases, Orders, Documents, Scans or Downloads first, then all user files. File types: documents and images. Return full path, file name, type, size and modified date for each, up to 50. If there are no results, say zero matches.

Result (file-agent): 7 matches (DW also matches inside "ADW"): Documents/Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf (2969); Documents/Receipts/2019/receipt_dishwasher_old.pdf (2794); Documents/Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf (2733); Documents/Receipts/2025/Brightline_order_TV_Lumora.pdf (2762); Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf (2960); Manuals/Nordvik_ADW-48xx_UserManual.pdf (17516); Downloads/ADW-48xx_manual (1).pdf (17516).

### Delegation 3 to photo-agent
Instruction as sent:
> Search the photo library for photos of a paper receipt or till slip that mention dishwasher, DW, and for photos of any appliance rating plate or serial label. Newest first, up to 20 of each. For each photo found, run text recognition and return the photo path, the date taken, whether it is a receipt or a rating plate, and the recognised text. If there are no results, say zero matches.

Result (photo-agent): receipts mentioning a dishwasher: zero matches. Rating plates: 2.
  - Photos/Phone/2024-03/IMG_20240316_190455.jpg, 2024-03-16 19:04:55. NORDVIK / MODEL: ADW-4820 / SERIAL: NV48-2203-1187 / 120V 60Hz 15A 1800W / MFD 2023-12. The label does not show what appliance it is on.
  - Photos/Phone/2022-01/IMG_20220115_101233.jpg, 2022-01-15 10:12:33. HomeHub / MODEL: FR-560 / SERIAL: HH56-2201-30647 / refrigerant R600a.

### Delegation 4 to document-agent
Parent: fridge and TV receipts are named for other products, dropped; warranty and manual files are not receipts.

Instruction as sent:
> Extract purchase details with the receipt schema from these files: Documents/Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf, Documents/Receipts/2019/receipt_dishwasher_old.pdf. If a file returns no data with the receipt schema, try the invoice schema. For each file return store, order number, purchase date exactly as printed, product description, brand, model number, serial number if printed, price, any warranty term printed on the receipt, and every other line item, especially any protection plan, extended warranty or care plan with its plan number and term. Report any file you could not read.

Result (document-agent):
  - 2024: Brightline Electronics; BL-2024-0314-55871; 2024-03-14; Nordvik ADW-4820 Dishwasher; serial NV48-2203-1187; $849.00; no term printed. Other lines: "3-Year Extended Protection Plan", plan EPP-3Y-90417733, "Covers ADW-4820 after the manufacturer warranty ends. Terms provided separately.", $129.00; Installation kit $24.99.
  - 2019: Brightline Electronics; BL-2019-0822-20318; 2019-08-22; Nordvik ADW-3100 Dishwasher; serial NV31-1905-0342; $529.00; "Manufacturer warranty: 1 year parts and labor. No extended plan purchased."; Haul-away $25.00.

Parent, choosing: two dishwasher purchases. The ADW-4820 plate photo (serial NV48-2203-1187) matches exactly one receipt (2024). The FR-560 plate matches no dishwasher receipt and is dropped. The 2024 unit is chosen without asking, the 2019 unit goes in Notes. Brand Nordvik, model ADW-4820, series ADW-48xx, order BL-2024-0314-55871.

## Step 2
### Delegation 5 to file-agent
Instruction as sent:
> Find files whose names contain any of: warranty, guarantee, garantie, protection, plan, care, extended, registration, certificate, terms, conditions, Nordvik, ADW-4820, ADW-48xx, Brightline. Search folders whose names contain Warranty, Receipts, Scans, Documents, Home or Appliances first, then all user files. File types: documents and images. Return full path, file name, size and modified date for each, up to 50. If there are no results, say zero matches.

Result (file-agent): 10 matches: Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf (2960); Scans/2024/Brightline_EPP_terms_scan.pdf (3271); Documents/Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf (2969); Documents/Receipts/2025/Brightline_order_TV_Lumora.pdf (2762); Documents/Receipts/2025/Brightline_soundbar_2025-12-18.pdf (2694); Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf (2681); Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf (2737); Scans/Lumora_TV_warranty.pdf (2560); Manuals/Nordvik_ADW-48xx_UserManual.pdf (17516); Downloads/ADW-48xx_manual (1).pdf (17516).

Parent: "terms" and the store name appear in results, so no extra Scans listing.

### Delegation 6 to document-agent
Instruction as sent:
> With intent locate_content and evidence mode focused, check these files: Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf, Scans/2024/Brightline_EPP_terms_scan.pdf. List only the files that are a warranty, guarantee, protection plan or warranty registration for Nordvik ADW-4820 or the series ADW-48xx, or a plan bought with order BL-2024-0314-55871. For each, quote the line that shows it. If none match, say zero matches.

Result (document-agent): both match. Warranty card: "Product: ADW-4820 Dishwasher". Plan scan: "Covered product  Nordvik ADW-4820 Dishwasher, serial NV48-2203-1187" and "Purchased 2024-03-14 (Brightline order BL-2024-0314-55871)".

### Delegation 7 to document-agent
Instruction as sent:
> Answer from these files only: Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf, Scans/2024/Brightline_EPP_terms_scan.pdf. With intent period and answer mode table, return for each document: the provider, each coverage (full parts and labour, parts only, or named components such as motor, compressor or panel) with its term, how the start date is defined, and any printed start or end date. With intent condition, return the exclusions and the claim procedure (phone, email or web form exactly as written, required attachments). Also return any plan number, registration number and serial number written on it. Quote the page or section for each answer.

Result (document-agent):
  - Nordvik card, page 1: parts and labor 2 years from the original purchase date; drive motor 10 years (wash motor and circulation pump motor, parts only after year 2); starts on the date of original retail purchase, dated receipt required; no printed dates. Exclusions include misuse, improper installation, consumables (filters, racks, gaskets) and repairs by anyone other than a Nordvik authorized provider; owner repairs beyond the manual void the warranty. Claim: "Email claims@nordvik-support.example or call 1-800-555-0188 (Mon-Fri 8:00-18:00 Pacific)", with receipt and serial plate photo.
  - Brightline plan terms, page 1: Brightline Protection Services, plan EPP-3Y-90417733, serial NV48-2203-1187. Parts and labor, including leaks from internal components, drain pump, heater, control board and sensors. "Plan start 2026-03-14, the day after the 2-year manufacturer warranty ends"; "Plan end 2029-03-14". Exclusions: cosmetic damage, racks, filters and gaskets, misuse or improper installation, pre-existing conditions, commercial use, unapproved repairs; owner repairs beyond the manual void the plan. Claim: "Email protect@brightline-services.example or call 1-800-555-0199", with plan number, receipt and serial.

## Step 3
### Delegation 8 to document-agent
Instruction as sent:
> Reconcile these files and report every difference in brand, model number, serial number, purchase date, plan start or end date, or owner name: Documents/Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf, Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf, Scans/2024/Brightline_EPP_terms_scan.pdf. For each difference give both values and the file each came from. If they all agree, say no differences found.

Result (document-agent): No differences found (brand, model ADW-4820, serial NV48-2203-1187, order, purchase date 2024-03-14, owner Alex Rivera agree; the card prints no serial or owner).

Parent: plate photo matches the receipt serial. Arithmetic: 14 Mar 2024 + 2 years = 14 Mar 2026, ended. Plan printed 14 Mar 2026 to 14 Mar 2029, active (printed date wins; the plan wording "day after" is a one-day gap, noted). Motor 14 Mar 2034, parts only after year 2. Label: Covered (by the plan and the motor warranty).

Coverage-only question: list each coverage with its end date, skip Steps 4 and 5, offer the manual lookup in one line. No checklist, no claim draft, no save question. Status `completed`.

## Final answer

```
Product: Nordvik ADW-4820 (dishwasher), bought 14 Mar 2024 at Brightline Electronics
Coverage: Covered today, by the protection plan and the motor warranty. Bought 14 Mar 2024:
  - Nordvik parts and labor warranty, 2 years: ended 14 Mar 2026.
  - Brightline protection plan EPP-3Y-90417733, 3 years: runs 14 Mar 2026 to 14 Mar 2029 (dates printed on the plan).
  - Nordvik drive motor warranty (wash motor and circulation pump motor), 10 years: runs to 14 Mar 2034, parts only after year 2.
I can also look up the manual steps for an error code if you tell me what the dishwasher is doing.
Evidence:
  - Documents/Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf: purchase 14 Mar 2024, ADW-4820, serial NV48-2203-1187, order BL-2024-0314-55871, plan EPP-3Y-90417733
  - Photos/Phone/2024-03/IMG_20240316_190455.jpg: rating plate ADW-4820, serial NV48-2203-1187 (matches the receipt)
  - Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf: 2 years parts and labor, motor 10 years, exclusions
  - Scans/2024/Brightline_EPP_terms_scan.pdf: plan 14 Mar 2026 to 14 Mar 2029
Notes: A 2019 Nordvik ADW-3100 (receipt 22 Aug 2019, 1 year, ended 22 Aug 2020) also exists; the plate photo matches only the 2024 ADW-4820, so that one is used. The plan says it starts "the day after" the warranty ends but prints 14 Mar 2026; the printed date is kept. Repairs by the owner beyond the manual's steps void the warranty and the plan.
```

Status: `completed`

Delegations: 8 (photo-agent x2, file-agent x2, document-agent x4).
