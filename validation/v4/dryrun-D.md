# Dry run D: "The TV has sound but no picture." (user declines the save)

Today 2026-11-20 08:40. Paths relative to project/testdata/home-library/. Mode: fault. Product: TV. Symptom: "sound but no picture". No code, brand or model from the user.

## Step 0

DELEGATE photo-agent:
'Search photos taken in the last 48 hours, up to 2026-11-20 08:40, for pictures of an appliance control panel or display showing an error code, or of an appliance rating plate or serial label. If the search cannot filter by time, take the 20 newest photos instead. For each photo found, up to 20, run text recognition and return the photo path, the time taken, the recognised text, and which kind of appliance the photo shows. If there are no results, say zero matches.'
Result: 1 photo, IMG_20261120_083012.jpg, 2026-11-20 08:30:12, "NORDVIK", "E15", buttons POWER/CYCLE/DELAY/START; kind not visible. Ignored: no positive match with a TV, and the buttons and the Nordvik name do not suggest a TV (D1).

## Step 1

DELEGATE file-agent:
'Find files whose names contain any of: receipt, invoice, order, purchase, quittung, TV. Search folders whose names contain Receipts, Invoices, Purchases, Orders, Documents, Scans or Downloads first, then all user files. File types: documents and images. Return full path, file name, type, size and modified date for each, up to 50. If there are no results, say zero matches.'
Result, 6 files: the five Receipts-folder PDFs (one is Documents/Receipts/2025/Brightline_order_TV_Lumora.pdf) and Scans/Lumora_TV_warranty.pdf (name contains TV).

DELEGATE photo-agent:
'Search the photo library for photos of a paper receipt or till slip that mention TV, and for photos of any appliance rating plate or serial label. Newest first, up to 20 of each. For each photo found, run text recognition and return the photo path, the date taken, whether it is a receipt or a rating plate, and the recognised text. If there are no results, say zero matches.'
Result: no TV receipt photo. Plates returned: IMG_20240316_190455.jpg (NORDVIK, ADW-4820, NV48-2203-1187) and IMG_20220115_101233.jpg (HomeHub, FR-560, HH56-2201-30647). Neither names a TV: ignored. No TV rear-label photo exists on the NAS.

DELEGATE document-agent (only the TV-named receipt; the warranty card is not a receipt, other receipts name other products):
'Extract purchase details with the receipt schema from these files: Documents/Receipts/2025/Brightline_order_TV_Lumora.pdf. If a file returns no data with the receipt schema, try the invoice schema. For each file return store, order number, purchase date exactly as printed, product description, brand, model number, serial number if printed, price, and every other line item, especially any protection plan, extended warranty or care plan with its plan number and term. Report any file you could not read.'
Result: Brightline Electronics; BL-2025-1201-77420; 2025-12-01; "Lumora 55Q8 55 in. QLED TV"; brand Lumora; model 55Q8; serial LU55-2511-90233; $699.00; other line: wall mount, tilt $39.99; no protection plan.

## Step 2

Series: 55Q8 does not start with letters, so left out.

DELEGATE file-agent:
'Find files whose names contain any of: warranty, guarantee, garantie, protection, plan, care, extended, registration, certificate, terms, conditions, Lumora, 55Q8, Brightline. Search folders whose names contain Warranty, Receipts, Scans, Documents, Home or Appliances first, then all user files. File types: documents and images. Return full path, file name, size and modified date for each, up to 50. If there are no results, say zero matches.'
Result: Scans/Lumora_TV_warranty.pdf; Documents/Receipts/2025/Brightline_order_TV_Lumora.pdf; Documents/Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf; Documents/Receipts/2025/Brightline_soundbar_2025-12-18.pdf; Scans/2024/Brightline_EPP_terms_scan.pdf; Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf; Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf; Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf.
(No scan fallback: the TV receipt has no plan.)

DELEGATE document-agent:
'With intent locate_content and evidence mode focused, check these files: Scans/Lumora_TV_warranty.pdf, Documents/Receipts/2025/Brightline_order_TV_Lumora.pdf, Documents/Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf, Documents/Receipts/2025/Brightline_soundbar_2025-12-18.pdf, Scans/2024/Brightline_EPP_terms_scan.pdf, Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf, Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf, Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf. List only the files that are a warranty, guarantee, protection plan or warranty registration for Lumora 55Q8, or a plan bought with order BL-2025-1201-77420. For each, quote the line that shows it. If none match, say zero matches.'
Result: 1 file: Scans/Lumora_TV_warranty.pdf, "Product: 55Q8 QLED Television". (The EPP plan belongs to order BL-2024-0314-55871 and a dishwasher.)

DELEGATE document-agent:
'Answer from these files only: Scans/Lumora_TV_warranty.pdf. With intent period and answer mode table, return for each document: the provider, each coverage (full parts and labour, parts only, or named components such as motor, compressor or panel) with its term, how the start date is defined, and any printed start or end date. With intent condition, return the exclusions and the claim procedure (phone, email or web form exactly as written, required attachments). Also return any plan number, registration number and serial number written on it. Quote the page or section for each answer.'
Result (page 1): Lumora; limited warranty 1 year, "Panel, board and power supply defects from the original purchase date"; "counted from the retail purchase date shown on the receipt"; no printed dates. Exclusions: burn-in, cracked screens, physical damage, power surge, unauthorized repair, wall-mount damage. Claim: "Email care@lumora-tv.example or call 1-800-555-0166. Attach receipt and a photo of the rear label showing the serial number." No plan, registration or serial number.

## Step 3

DELEGATE document-agent:
'Reconcile these files and report every difference in brand, model number, serial number, purchase date, plan start or end date, or owner name: Documents/Receipts/2025/Brightline_order_TV_Lumora.pdf, Scans/Lumora_TV_warranty.pdf. For each difference give both values and the file each came from. If they all agree, say no differences found.'
Result: no differences found (Lumora, 55Q8; the card prints no serial or dates).

Arithmetic: bought 1 Dec 2025 + 1 year = 1 Dec 2026, active on the end date. Today 20 Nov 2026, so 11 days left. "Sound but no picture" points to the panel, board or power supply (a listed component), so Covered "if the technician confirms a panel, board or power supply fault".

## Step 4

DELEGATE file-agent:
'Find files whose names contain any of: manual, guide, instructions, handbook, quick start, Lumora, 55Q8. Search folders whose names contain Manuals, Documents, Downloads, Home or Appliances first, then all user files. File type: documents. Return full path, file name, size and modified date, up to 20. If there are no results, say zero matches.'
Result: Scans/Lumora_TV_warranty.pdf; Documents/Receipts/2025/Brightline_order_TV_Lumora.pdf (both by Lumora); manuals by name: Manuals/Zentro_AX3000_Router_Manual.pdf, Manuals/Nordvik_ADW-48xx_UserManual.pdf, Downloads/ADW-48xx_manual (1).pdf, Home/Appliances/Washer/WM-7_manual.pdf, Home/Appliances/Fridge/FR-560_owner_manual.pdf.
Parent: no result is named both a manual and Lumora or 55Q8, so zero matches. No content check. "There is no manual for Lumora 55Q8 on your NAS."

## Step 5

Draft shown with the question "Save this draft to your NAS? (yes / no)" (no checklist). Status waiting_approval.

    To: Email care@lumora-tv.example or call 1-800-555-0166
    Subject: Warranty claim, Lumora 55Q8, serial LU55-2511-90233
    Product: Lumora 55Q8, serial LU55-2511-90233
    Purchased: 2025-12-01 at Brightline Electronics, order BL-2025-1201-77420
    Coverage: Lumora 1-year limited warranty (panel, board, power supply), valid until 2026-12-01
    Fault: sound but no picture, error code none
    Already tried: none confirmed
    Attachments: Documents/Receipts/2025/Brightline_order_TV_Lumora.pdf, Scans/Lumora_TV_warranty.pdf; photo of the rear label showing the serial: none on the NAS, user to take one
    Contact:

User declines ("no"). No knowledge-agent call. Status completed, "not saved".

## Final answer (status completed)

    Product: Lumora 55Q8 (TV), bought 1 Dec 2025 at Brightline Electronics
    Coverage: Covered until 1 Dec 2026, 11 days left, if the technician confirms a panel, board or power supply fault. Bought 1 Dec 2025 + 1-year warranty = 1 Dec 2026.
    Safety first: There is no manual for Lumora 55Q8 on your NAS. Switch the TV off at the wall or unplug it. If you smell burning or see smoke or sparks, leave it off and call a qualified technician.
    Claim: draft ready for care@lumora-tv.example or 1-800-555-0166 (not saved). It needs the receipt and a photo of the rear label with the serial number; take that photo before 1 Dec 2026.
    Evidence:
      - Documents/Receipts/2025/Brightline_order_TV_Lumora.pdf: 2025-12-01, order BL-2025-1201-77420, Lumora 55Q8, serial LU55-2511-90233
      - Scans/Lumora_TV_warranty.pdf: 1 year panel, board, power supply; exclusions; claim contact
    Notes: No manual found, so no repair steps are given. No TV rear-label photo on the NAS. Warranty exclusions include burn-in, cracked screens, physical damage, power surge, unauthorized repair and wall-mount damage. The recent E15 photo was ignored (it does not show a TV). Draft not saved; kept in this chat.

Delegations: 9 = photo-agent 2, file-agent 3, document-agent 4 (extract, locate, terms, reconcile). No knowledge-agent call.
