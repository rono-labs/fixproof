# Dry run D: "The TV has sound but no picture." (user declines the save)

Today 2026-11-20 08:40. Paths relative to `project/testdata/home-library/`. Mode: fault. Product: TV. Symptom: "sound but no picture". No code from the user.

## D1 photo-agent (Step 0)
Instruction: `Search photos taken in the last 48 hours, up to 2026-11-20 08:40, for pictures of an appliance control panel or display showing an error code, or of an appliance rating plate or serial label. For each photo found, run text recognition and return the photo path, the time taken and the recognised text. If there are no results, say zero matches.`
Result: 1 photo, `Photos/Phone/2026-11/IMG_20261120_083012.jpg`, 2026-11-20 08:30:12, text "NORDVIK  E15  POWER  CYCLE  DELAY  START".
Parent (literal rule): shows a code and a brand, user named no brand, text names no product type. Tentatively keep: brand Nordvik, code E15.

## D2 file-agent (Step 1, names)
Instruction: `Find files whose names contain any of: receipt, invoice, order, purchase, quittung, Nordvik, TV. Search folders whose names contain Receipts, Invoices, Purchases, Orders, Documents, Scans or Downloads first, then all user files. File types: documents and images. Return full path, file name, type, size and modified date for each, up to 50. If there are no results, say zero matches.`
Result, 9 files: the five Receipts PDFs, Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf, Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf, Manuals/Nordvik_ADW-48xx_UserManual.pdf, Scans/Lumora_TV_warranty.pdf (name has "TV").

## D3 photo-agent (Step 1)
Instruction: `Search the photo library for photos of a paper receipt or till slip, and for photos of an appliance rating plate or serial label, that mention TV or Nordvik. For each photo found, run text recognition and return the photo path, the date taken, whether it is a receipt or a rating plate, and the recognised text. If there are no results, say zero matches.`
Result, 2 photos: `Photos/Phone/2024-03/IMG_20240316_190455.jpg` (Nordvik ADW-4820 plate, serial NV48-2203-1187) and `Photos/Phone/2023-06/IMG_20230602_181404.jpg` (HomeHub receipt for a Nordvik WM-7 washer). Both name other products: no match. No TV photos.

## D4 document-agent (Step 1, extract)
Only Brightline_order_TV_Lumora.pdf is not named for another product (the soundbar receipt names a soundbar).
Instruction: `Extract purchase details with the receipt schema from these files: Documents/Receipts/2025/Brightline_order_TV_Lumora.pdf. If a file returns no data with the receipt schema, try the invoice schema. For each file return store, order number, purchase date exactly as printed, product description, brand, model number, serial number if printed, price, and every other line item, especially any protection plan, extended warranty or care plan with its plan number and term. Report any file you could not read.`
Result: Brightline Electronics, order BL-2025-1201-77420, 2025-12-01, Lumora 55Q8 55 in. QLED TV, serial LU55-2511-90233, $699.00; Wall mount, tilt $39.99; total $738.99; "Lumora 1-year limited warranty applies from the date of purchase." No protection plan.

Parent: brand Lumora, not Nordvik, so the E15 photo is dropped (same retroactive check as in C). One TV purchase.

## D5 file-agent (Step 2)
Slots: brand Lumora, model 55Q8 (starts with digits, so no series), store Brightline.
Instruction: `Find files whose names contain any of: warranty, guarantee, garantie, protection, plan, care, extended, registration, certificate, terms, conditions, Lumora, 55Q8, Brightline. Search folders whose names contain Warranty, Receipts, Scans, Documents, Home or Appliances first, then all user files. File types: documents and images. Return full path, file name, size and modified date for each, up to 50. If there are no results, say zero matches.`
Result, 8 files: Brightline_Receipt_2024-03-14_dishwasher.pdf, Brightline_order_TV_Lumora.pdf, Brightline_soundbar_2025-12-18.pdf, Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf, Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf, Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf, Scans/2024/Brightline_EPP_terms_scan.pdf, Scans/Lumora_TV_warranty.pdf. (No plan on the receipt, so no Scans listing.)

## D6 document-agent (Step 2, confirm)
Instruction: `With intent locate_content and evidence mode focused, check these files: [the 8 paths above]. List only the files that are a warranty, guarantee, protection plan or warranty registration for Lumora 55Q8, or a plan bought with order BL-2025-1201-77420. For each, quote the line that shows it. If none match, say zero matches.`
Result: 1 match, Scans/Lumora_TV_warranty.pdf: "LIMITED WARRANTY CARD / Product: 55Q8 QLED Television".

## D7 document-agent (Step 2, terms)
Instruction: `Answer from these files only: Scans/Lumora_TV_warranty.pdf. With intent period and answer mode table, return for each document: the provider, each coverage (full parts and labour, parts only, or named components such as motor, compressor or panel) with its term, how the start date is defined, and any printed start or end date. With intent condition, return the exclusions and the claim procedure (phone, email or web form exactly as written, required attachments). Also return any plan number, registration number and serial number written on it. Quote the page or section for each answer.`
Result (p.1): Lumora. Limited warranty 1 year, "Panel, board and power supply defects from the original purchase date." Start: "counted from the retail purchase date shown on the receipt". No printed dates, no serial or plan number. Exclusions: burn-in, cracked screens, physical damage, power surge, unauthorized repair, wall-mount damage. Claim: "Email care@lumora-tv.example or call 1-800-555-0166. Attach receipt and a photo of the rear label showing the serial number."

## D8 document-agent (Step 3, reconcile)
Instruction: `Reconcile these files and report every difference in brand, model number, serial number, purchase date, plan start or end date, or owner name: Documents/Receipts/2025/Brightline_order_TV_Lumora.pdf, Scans/Lumora_TV_warranty.pdf. For each difference give both values and the file each came from. If they all agree, say no differences found.`
Result: no differences found (Lumora 55Q8 on both; the card prints no serial or date).

Coverage: 2025-12-01 + 1 year = 2026-12-01. Today 2026-11-20, 11 days left, active. Named components (panel, board, power supply): no picture with sound points to the panel or board, so Covered, "if the technician confirms a panel or board fault". No rear-label photo of the TV is on the NAS to compare.

## D9 file-agent (Step 4)
Instruction: `Find files whose names contain any of: manual, guide, instructions, handbook, quick start, 55Q8, Lumora. Search folders whose names contain Manuals, Documents, Downloads, Home or Appliances first, then all user files. File type: documents. Return full path, file name, size and modified date, up to 20. If there are no results, say zero matches.`
Result, 7 files: Documents/Receipts/2025/Brightline_order_TV_Lumora.pdf, Downloads/ADW-48xx_manual (1).pdf, Home/Appliances/Fridge/FR-560_owner_manual.pdf, Home/Appliances/Washer/WM-7_manual.pdf, Manuals/Nordvik_ADW-48xx_UserManual.pdf, Manuals/Zentro_AX3000_Router_Manual.pdf, Scans/Lumora_TV_warranty.pdf. Two names contain "Lumora" (receipt, warranty), so the skill says to confirm by content.

## D10 document-agent (Step 4, confirm manual; wording adapted)
Instruction: `With intent locate_content and evidence mode focused, check these files: [the 7 paths above]. List only the files that are the user manual for Lumora 55Q8. For each, quote the line that shows it. If none match, say zero matches.`
Result: zero matches (the Lumora files are a receipt and a warranty card; the manuals cover Nordvik ADW-48xx, HomeHub FR-560, Nordvik WM-7 and Zentro AX3000).

No manual: "There is no manual for Lumora 55Q8 on your NAS". Only the universal safety line. No improvised repair steps.

## Reply 1 (status waiting_approval)

```
Product: Lumora 55Q8 (TV), bought 1 Dec 2025 at Brightline Electronics
Coverage: Covered. Bought 1 Dec 2025 + 1-year Lumora limited warranty (panel, board and power supply) = runs to 1 Dec 2026, 11 days from today. Covered if the technician confirms a panel or board fault.
Safety first: There is no manual for Lumora 55Q8 on your NAS. Switch the TV off at the wall or unplug it. If you smell burning or see smoke or sparks, leave it off and call a qualified technician.
Claim: draft ready for Email care@lumora-tv.example or call 1-800-555-0166. Save it to your NAS? (yes / no)

To: Email care@lumora-tv.example or call 1-800-555-0166
Subject: Warranty claim, Lumora 55Q8, serial LU55-2511-90233
Product: Lumora 55Q8, serial LU55-2511-90233
Purchased: 2025-12-01 at Brightline Electronics, order BL-2025-1201-77420
Coverage: Lumora 1-year limited warranty, valid until 2026-12-01
Fault: sound but no picture, no error code
Already tried: none confirmed
Attachments: Documents/Receipts/2025/Brightline_order_TV_Lumora.pdf, Scans/Lumora_TV_warranty.pdf, photo of the rear label showing the serial number (none on the NAS, please take one)
Contact: (blank)

Which of the steps above have you already tried? Then say yes to save this draft to your NAS, or no.
Evidence:
  - Documents/Receipts/2025/Brightline_order_TV_Lumora.pdf: purchase date, model, serial, order, price
  - Scans/Lumora_TV_warranty.pdf: 1 year panel, board and power supply, exclusions, claim contact
Notes: Warranty ends 1 Dec 2026, so claim before then. Exclusions: burn-in, cracked screens, physical damage, power surge, unauthorized repair, wall-mount damage. No manual and no rear-label photo of the TV are on the NAS. Today's photo (IMG_20261120_083012.jpg, Nordvik, E15) belongs to another appliance and was not used.
```

## User: "No."
No knowledge-agent call. Final status completed, "not saved", draft kept in chat.

Delegations: 10 (photo 2, file 3, document 5). No save.
