# Dry run A: "The dishwasher is doing this again."

Today 2026-11-20 08:40. Paths are relative to `project/testdata/home-library/`. Modified date of every file is the copy date 2026-10-29 (never used as a purchase date). File-agent matching: search terms against file and folder names only.

Mode: fault. Product: dishwasher. Symptom: vague ("doing this again"). Code: none yet.

## D1 photo-agent (Step 0)
Instruction: `Search photos taken in the last 48 hours, up to 2026-11-20 08:40, for pictures of an appliance control panel or display showing an error code, or of an appliance rating plate or serial label. For each photo found, run text recognition and return the photo path, the time taken and the recognised text. If there are no results, say zero matches.`

Result (window starts 2026-11-18 08:40, EXIF DateTimeOriginal): 1 photo. `Photos/Phone/2026-11/IMG_20261120_083012.jpg`, taken 2026-11-20 08:30:12, text: "NORDVIK  E15  POWER  CYCLE  DELAY  START". (A still image cannot show blinking; no model or serial visible.)

Parent: code E15, brand Nordvik. User said dishwasher, photo names no other product or brand. Photo kept. Model unknown, so it stays out of instructions.

## D2 file-agent (Step 1, names)
Instruction: `Find files whose names contain any of: receipt, invoice, order, purchase, quittung, Nordvik, dishwasher. Search folders whose names contain Receipts, Invoices, Purchases, Orders, Documents, Scans or Downloads first, then all user files. File types: documents and images. Return full path, file name, type, size and modified date for each, up to 50. If there are no results, say zero matches.`

Result, 8 files: Receipts/2019/receipt_dishwasher_old.pdf (2794), Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf, Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf (2969), Receipts/2025/Brightline_order_TV_Lumora.pdf, Receipts/2025/Brightline_soundbar_2025-12-18.pdf, Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf, Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf, Manuals/Nordvik_ADW-48xx_UserManual.pdf.

## D3 photo-agent (Step 1, receipt photos and plates)
Instruction: `Search the photo library for photos of a paper receipt or till slip, and for photos of an appliance rating plate or serial label, that mention dishwasher or Nordvik. For each photo found, run text recognition and return the photo path, the date taken, whether it is a receipt or a rating plate, and the recognised text. If there are no results, say zero matches.`

Result, 2 photos:
1. `Photos/Phone/2024-03/IMG_20240316_190455.jpg`, 2024-03-16 19:04:55, rating plate: "NORDVIK MODEL: ADW-4820 SERIAL: NV48-2203-1187 120V 60Hz 15A 1800W MFD 2023-12".
2. `Photos/Phone/2023-06/IMG_20230602_181404.jpg`, 2023-06-02 18:14:04, receipt: "HOMEHUB APPLIANCES ... Date: 06/02/2023 Order HH-230602-1187 ... Nordvik WM-7 Front Load Washer SN NV7-2305-60912 $899.00 Delivery $59.00 TOTAL $958.00 ... Warranty: see manufacturer card".

Parent: photo 2 names a washing machine, so no match. Photo 1 is the plate for this dishwasher.

## D4 document-agent (Step 1, extract)
Files kept by name: the two dishwasher receipts (fridge, TV and soundbar receipts name other products).
Instruction: `Extract purchase details with the receipt schema from these files: Documents/Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf, Documents/Receipts/2019/receipt_dishwasher_old.pdf. If a file returns no data with the receipt schema, try the invoice schema. For each file return store, order number, purchase date exactly as printed, product description, brand, model number, serial number if printed, price, and every other line item, especially any protection plan, extended warranty or care plan with its plan number and term. Report any file you could not read.`

Result:
- 2024 receipt: Brightline Electronics, order BL-2024-0314-55871, 2024-03-14, Nordvik ADW-4820 Dishwasher, serial NV48-2203-1187, $849.00; 3-Year Extended Protection Plan, plan no. EPP-3Y-90417733, $129.00, "Covers ADW-4820 after the manufacturer warranty ends. Terms provided separately."; installation kit $24.99; total $1,002.99.
- 2019 receipt: Brightline, order BL-2019-0822-20318, 2019-08-22, Nordvik ADW-3100, serial NV31-1905-0342, $529.00; "No extended plan purchased".

Choosing: two dishwasher purchases. The plate photo (ADW-4820, NV48-2203-1187) matches exactly the 2024 receipt, which settles it. 2019 purchase goes to Notes. No question to the user needed.

## D5 file-agent (Step 2, names)
Slots: brand Nordvik, model ADW-4820, series ADW-48xx, store Brightline.
Instruction: `Find files whose names contain any of: warranty, guarantee, garantie, protection, plan, care, extended, registration, certificate, terms, conditions, Nordvik, ADW-4820, ADW-48xx, Brightline. Search folders whose names contain Warranty, Receipts, Scans, Documents, Home or Appliances first, then all user files. File types: documents and images. Return full path, file name, size and modified date for each, up to 50. If there are no results, say zero matches.`

Result, 10 files: Brightline_Receipt_2024-03-14_dishwasher.pdf, Brightline_order_TV_Lumora.pdf, Brightline_soundbar_2025-12-18.pdf, Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf, Downloads/ADW-48xx_manual (1).pdf, Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf, Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf, Manuals/Nordvik_ADW-48xx_UserManual.pdf, Scans/2024/Brightline_EPP_terms_scan.pdf, Scans/Lumora_TV_warranty.pdf.

Parent check: the receipt lists a plan, and no candidate name contains "plan" (EPP_terms does not). Per the skill, also list Scans folders.

## D6 file-agent (Step 2, Scans listing; no template in skill, wording mine)
Instruction: `Find every file in folders whose names contain Scans. File types: documents. Return full path, file name, size and modified date for each, up to 50. If there are no results, say zero matches.`
Result: Scans/2024/Brightline_EPP_terms_scan.pdf (3271), Scans/Lumora_TV_warranty.pdf (2560). Both already candidates.

## D7 document-agent (Step 2, confirm by content)
Instruction: `With intent locate_content and evidence mode focused, check these files: Documents/Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf, Documents/Receipts/2025/Brightline_order_TV_Lumora.pdf, Documents/Receipts/2025/Brightline_soundbar_2025-12-18.pdf, Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf, Downloads/ADW-48xx_manual (1).pdf, Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf, Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf, Manuals/Nordvik_ADW-48xx_UserManual.pdf, Scans/2024/Brightline_EPP_terms_scan.pdf, Scans/Lumora_TV_warranty.pdf. List only the files that are a warranty, guarantee, protection plan or warranty registration for Nordvik ADW-4820 or the series ADW-48xx, or a plan bought with order BL-2024-0314-55871. For each, quote the line that shows it. If none match, say zero matches.`

Result: 2 matches. Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf: "LIMITED WARRANTY CARD / Product: ADW-4820 Dishwasher". Scans/2024/Brightline_EPP_terms_scan.pdf: "Covered product: Nordvik ADW-4820 Dishwasher, serial NV48-2203-1187" and "Purchased 2024-03-14 (Brightline order BL-2024-0314-55871)". The receipt and manuals are not warranty documents.

## D8 document-agent (Step 2, terms)
Instruction: `Answer from these files only: Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf, Scans/2024/Brightline_EPP_terms_scan.pdf. With intent period and answer mode table, return for each document: the provider, each coverage (full parts and labour, parts only, or named components such as motor, compressor or panel) with its term, how the start date is defined, and any printed start or end date. With intent condition, return the exclusions and the claim procedure (phone, email or web form exactly as written, required attachments). Also return any plan number, registration number and serial number written on it. Quote the page or section for each answer.`

Result:
- Warranty card (p.1): Nordvik. Parts and labor 2 years; drive motor 10 years (wash motor and circulation pump motor, parts only after year 2). Start: "Warranty starts on the date of original retail purchase. A dated receipt is required." No printed dates. Exclusions: misuse, improper installation, power surges, frozen pipes, commercial use, cosmetic damage, consumables (filters, racks, gaskets), repairs by anyone other than a Nordvik authorized provider; owner repairs beyond the manual's steps void it. Claim: "Email claims@nordvik-support.example or call 1-800-555-0188 (Mon-Fri 8:00-18:00 Pacific)", needs dated receipt and clear serial plate photo. No serial or plan number.
- Plan terms (p.1): Administrator Brightline Protection Services. Plan no. EPP-3Y-90417733. Parts and labor for mechanical and electrical failure, "including leaks from internal components, drain pump, heater, control board and sensors". Printed: Plan start 2026-03-14, "the day after the 2-year manufacturer warranty ends"; Plan end 2029-03-14. Serial NV48-2203-1187. Exclusions (s.2): cosmetic damage, racks, filters and gaskets, misuse or improper installation, pre-existing conditions, commercial use, repairs by anyone not approved; owner repairs beyond the manual's steps void the plan. Claim (s.3): "Email protect@brightline-services.example or call 1-800-555-0199"; have plan number, original receipt and serial ready; no deductible. S.5: while the manufacturer warranty is in force, claims go to the manufacturer.

## D9 document-agent (Step 3, reconcile)
Instruction: `Reconcile these files and report every difference in brand, model number, serial number, purchase date, plan start or end date, or owner name: Documents/Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf, Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf, Scans/2024/Brightline_EPP_terms_scan.pdf. For each difference give both values and the file each came from. If they all agree, say no differences found.`
Result: No differences found (model ADW-4820, serial NV48-2203-1187 on receipt and plan, order and date 2024-03-14, owner Alex Rivera). The warranty card prints no serial or date, so nothing to compare there.

Parent plate check: plate photo model ADW-4820 and serial NV48-2203-1187 equal the receipt and plan. Match.

Coverage: 2024-03-14 + 2 years = ended 2026-03-14 (drive motor to 2034-03-14, parts only, not relevant to a leak). Printed plan 2026-03-14 to 2029-03-14 wins; the plan start says "day after" the base warranty ends while the calculation gives the same day, a one-day gap, not a conflict. Today is inside the plan. Label Covered. Manual cause list for E15: loose hose, door gasket, internal leak. Gaskets are excluded, an internal leak is covered, so the label stays and a Note quotes the exclusion.

## D10 file-agent (Step 4)
Instruction: `Find files whose names contain any of: manual, guide, instructions, handbook, quick start, ADW-4820, ADW-48xx, Nordvik. Search folders whose names contain Manuals, Documents, Downloads, Home or Appliances first, then all user files. File type: documents. Return full path, file name, size and modified date, up to 20. If there are no results, say zero matches.`
Result, 7 files: Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf, Downloads/ADW-48xx_manual (1).pdf (17516), Home/Appliances/Fridge/FR-560_owner_manual.pdf, Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf, Home/Appliances/Washer/WM-7_manual.pdf, Manuals/Nordvik_ADW-48xx_UserManual.pdf (17516), Manuals/Zentro_AX3000_Router_Manual.pdf.
Names contain brand or series, so confirm by content.

## D11 document-agent (Step 4, confirm manual; wording adapted, Step 2 wording would ask for warranty documents)
Instruction: `With intent locate_content and evidence mode focused, check these files: Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf, Downloads/ADW-48xx_manual (1).pdf, Home/Appliances/Fridge/FR-560_owner_manual.pdf, Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf, Home/Appliances/Washer/WM-7_manual.pdf, Manuals/Nordvik_ADW-48xx_UserManual.pdf, Manuals/Zentro_AX3000_Router_Manual.pdf. List only the files that are the user manual for Nordvik ADW-4820 or the series ADW-48xx. For each, quote the line that shows it. If none match, say zero matches.`
Result: 2 matches, Manuals/Nordvik_ADW-48xx_UserManual.pdf and Downloads/ADW-48xx_manual (1).pdf, both "Model series ADW-48xx / User Manual and Care Guide".

## D12 file-agent (duplicate check; wording mine, same size 17516)
Instruction: `Return the size and the sha256sum of each of these two files and say whether they are identical: Manuals/Nordvik_ADW-48xx_UserManual.pdf, Downloads/ADW-48xx_manual (1).pdf.`
Result: both 17516 bytes, sha256 2858e0506bfc17fb3076623c5b917c28c11cb91b4650cc02af821eb6bfde3b7d. Identical. Keep Manuals/ copy, note the Downloads duplicate.

## D13 document-agent (Step 4, manual)
Instruction: `Using only Manuals/Nordvik_ADW-48xx_UserManual.pdf, with intent locate_content and answer mode table, find what the manual says about error code E15. Return the matching rows of the error-code and troubleshooting tables (problem, cause, what to do) in the order printed, the safety warnings that apply to those steps, any steps that need a qualified technician, and any statement that user repairs affect the warranty. Give the page or section for each item.`
Result: s.7 p.9 E15: "Water detected in the base pan. Leak protection has stopped the unit." Action: "Turn off water, unplug, tilt unit slightly to drain base pan only if instructed, check door gasket and hose connections. If E15 returns, call service. Do not open the base." s.8 p.10: "Puddle under unit, E15 shown | Water in base pan: loose hose, door gasket, or internal leak | Stop the unit, check hose clamps and gasket. Service call if the leak persists". Safety s.1 p.3: "Do not operate a dishwasher that is leaking. Turn off the water supply and unplug the unit." Technician: service call if E15 returns or leak persists; do not open the base. Warranty: s.1 p.3 and s.8 p.10, user repairs beyond the listed steps void the warranty and any extended protection plan.

## Reply 1 (status waiting_approval; E15 row mentions water, so safety leads)

```
Safety first: Do not operate a dishwasher that is leaking. Turn off the water supply and unplug the unit (switch off at the wall). If E15 returns or the leak persists, call a qualified technician. (manual p.3, p.9)
Product: Nordvik ADW-4820 (dishwasher), bought 14 Mar 2024 at Brightline Electronics
Coverage: Covered. Bought 14 Mar 2024 + 2-year Nordvik warranty = ended 14 Mar 2026. Protection plan EPP-3Y-90417733 runs 14 Mar 2026 to 14 Mar 2029, so covered by the plan today (20 Nov 2026).
Try this (manual s.7 p.9, s.8 p.10):
  1. Turn off the water supply and unplug the dishwasher.
  2. Check the door gasket and the hose connections and clamps.
  3. Tilt the unit slightly to drain the base pan only if the manual's service instruction says so.
  4. Restart. If E15 returns, call service.
  Technician only: any internal leak; do not open the base. A repair beyond these steps voids the warranty and the protection plan.
Claim: draft ready for Email protect@brightline-services.example or call 1-800-555-0199.

To: Email protect@brightline-services.example or call 1-800-555-0199
Subject: Warranty claim, Nordvik ADW-4820, serial NV48-2203-1187
Product: Nordvik ADW-4820, serial NV48-2203-1187
Purchased: 2024-03-14 at Brightline Electronics, order BL-2024-0314-55871
Coverage: Brightline 3-Year Extended Protection Plan EPP-3Y-90417733, valid until 2029-03-14
Fault: water in the base pan, leak protection stopped the unit, error code E15
Already tried: none confirmed
Attachments: Documents/Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf, Scans/2024/Brightline_EPP_terms_scan.pdf
Contact: (blank)

Which of the steps above have you already tried? Then say yes to save this draft to your NAS, or no.
Evidence:
  - Photos/Phone/2026-11/IMG_20261120_083012.jpg: error code E15, Nordvik name (taken 2026-11-20 08:30)
  - Photos/Phone/2024-03/IMG_20240316_190455.jpg: plate, model ADW-4820, serial NV48-2203-1187
  - Documents/Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf: purchase date, model, serial, order, plan line
  - Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf: 2 years parts and labor, 10 years motor, exclusions, claim contact
  - Scans/2024/Brightline_EPP_terms_scan.pdf: plan dates 2026-03-14 to 2029-03-14, exclusions, claim contact
  - Manuals/Nordvik_ADW-48xx_UserManual.pdf: E15 rows, safety, void-warranty note
Notes: The plan's claim contact is used because the manufacturer warranty has ended. Plan exclusion "racks, filters and gaskets, damage from misuse or improper installation": a worn door gasket or installation fault is excluded, an internal leak is covered. Plate and receipt serials match; the 2019 ADW-3100 receipt (Documents/Receipts/2019/receipt_dishwasher_old.pdf) was not used. Duplicate manual at Downloads/ADW-48xx_manual (1).pdf is identical. Plan start is printed as the day after the base warranty ends; calculated end of the base warranty is 14 Mar 2026, a one-day gap, printed date kept. The photo has no model number; the plate photo supplied it.
```

## User: "I checked the hoses, yes save it"
"Already tried" becomes "Checked the hoses (told by user)". A clear yes.

## D14 knowledge-agent (Step 5 save)
Instruction: `Save this text as a new note with filename hint "Warranty claim Nordvik ADW-4820 2026-11-20 08:40". Text: [claim draft above with "Already tried: Checked the hoses (told by user)"]`
Result: saved to `Notes/Warranty claim Nordvik ADW-4820 2026-11-20 08:40.md`.

## Reply 2 (status completed)
Draft saved to Notes/Warranty claim Nordvik ADW-4820 2026-11-20 08:40.md, with "Already tried: Checked the hoses". Nothing was sent; you send it to protect@brightline-services.example or call 1-800-555-0199 with the receipt and plan terms attached. Since the hoses are fine, the likely remaining causes are the door gasket or an internal leak: do not open the base, and let the technician handle it. Evidence and Notes as above.

Delegations: 14 (13 before approval, 1 save).
