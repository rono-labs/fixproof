# Dry run D: "The TV has sound but no picture." (user declines the save)

Today = 2026-11-20. Paths are relative to `project/testdata/home-library/` (written `home-library/`). Expert results are emulated from `find`, `grep`, `pdftotext` and by viewing the photos.

## Intake
Mode: fault. Product: TV. Symptom: "sound but no picture". No error code, brand or model given.

## Step 1. Purchase record

delegate --target file-agent --instruction 'Find documents that look like receipts, invoices or order confirmations for a TV. Search folders whose names contain Receipts, Invoices, Purchases, Orders, Documents, Scans or Downloads first, then all of the user files. Include PDF, image and office document types. For each match return the full path, file name, type and modified date, up to 30 matches. If there are no results, say zero matches.'

file-agent result (1 match; "TV" is in the file name):
- home-library/Documents/Receipts/2025/Brightline_order_TV_Lumora.pdf, PDF, modified 2026-10-29

delegate --target photo-agent --instruction 'Search the photo library for photos of a paper receipt or of an appliance rating plate or serial label for a TV. For each photo found, run text recognition and return the photo path, the date taken and the recognised text. If there are no results, say zero matches.'

photo-agent result: no photo of a TV receipt or a TV rear label. It reports the three paper/plate photos it does have (dishwasher plate, fridge plate, washer receipt, texts as in runs A to C), none of which mentions a TV. Parent treats the photo search as zero matches for the TV.

delegate --target document-agent --instruction 'Extract purchase details with the receipt schema from these files: home-library/Documents/Receipts/2025/Brightline_order_TV_Lumora.pdf. For each file return store, order number, purchase date, product description, brand, model number, serial number if printed, price, and every other line item, especially any protection plan, extended warranty or care plan with its plan number and term.'

document-agent result: Brightline Electronics, order BL-2025-1201-77420, 2025-12-01, "Lumora 55Q8 55 in. QLED TV", brand Lumora, model 55Q8, serial LU55-2511-90233, $699.00. Other line: wall mount, tilt, $39.99. No protection plan. Printed text: "Lumora 1-year limited warranty applies from the date of purchase."

One TV purchase. No question to the user needed.

## Step 2. Warranty documents

delegate --target file-agent --instruction 'Find documents that mention 55Q8 or Lumora TV together with any of these words: warranty, guarantee, protection plan, extended, care plan, certificate, registration. Also return any file in the same folder as home-library/Documents/Receipts/2025/Brightline_order_TV_Lumora.pdf with a modified date within 30 days of 2025-12-01. Return full path, file name and modified date for each, up to 30. If there are no results, say zero matches.'

file-agent result:
- home-library/Scans/Lumora_TV_warranty.pdf (55Q8, warranty)
- home-library/Documents/Receipts/2025/Brightline_order_TV_Lumora.pdf (55Q8, warranty line)
- home-library/Documents/Receipts/2025/Brightline_soundbar_2025-12-18.pdf (Lumora, warranty line; a soundbar, not the TV)
Same-folder clause: on a NAS with original dates the soundbar receipt (2025-12-18) would also qualify; here upload dates make it empty. Parent ignores the soundbar receipt: different product.

delegate --target document-agent --instruction 'Answer from these files only: home-library/Scans/Lumora_TV_warranty.pdf. For each document return: who provides it, what it covers (full parts and labour, parts only, or named components such as motor or compressor) with the term for each, whether the term starts at purchase, delivery or when another warranty ends, the exclusions, the claim procedure (phone, email or web form exactly as written, and required attachments), and any plan or registration number with any serial number written on it. Quote the page or section for each answer.'

document-agent result (page 1): provider Lumora. Limited warranty 1 year, "Panel, board and power supply defects from the original purchase date." Counted "from the retail purchase date shown on the receipt." Exclusions: burn-in, cracked screens, physical damage, power surge, unauthorized repair, wall-mount damage. Claim: care@lumora-tv.example or 1-800-555-0166; "Attach receipt and a photo of the rear label showing the serial number." No plan, registration or serial number printed.

## Step 3. Verdict
2025-12-01 + 1 year = 2026-12-01. Today 2026-11-20 is before it, 11 days left; the end date itself still counts as active.
Which coverage applies: the card covers named parts (panel, board, power supply). "Sound but no picture" can be a panel, board or power supply fault, but there is no manual to name the cause. Rule for an unclear component: "may be covered if the technician confirms a panel, board or power supply fault". The verdict labels in SKILL.md do not say which label goes with that wording (defect D8). This run uses Partly covered ("only some parts of the fault are covered").
Cross-check delegation not sent: no TV rear-label photo exists, so the three-way condition in Step 3 is not met.
Verdict: Partly covered, until 2026-12-01.

## Step 4. Manual

delegate --target file-agent --instruction 'Find user manuals, installation guides or quick start guides for Lumora 55Q8. Search folders whose names contain Manuals, Documents, Downloads or Home first, then all user files. Return full path, file name and modified date, up to 10. If there are no results, say zero matches.'

file-agent result: zero matches. (Manuals/ holds only the Nordvik dishwasher manual and the Zentro router manual.)

Parent: "There is no manual for Lumora 55Q8 on your NAS." Only the universal advice is given: switch off and unplug the TV. No repair steps are invented. Because the TV is in a Covered/Partly covered state the claim route is open.

## Step 5. Claim draft (turn 1)
Draft shown and "Save this claim draft to your NAS?" asked. Status `waiting_approval`.

## Step 6. Final answer, turn 1

    Product: Lumora 55Q8 (TV), bought 2025-12-01 at Brightline Electronics
    Coverage: Partly covered. Bought 1 Dec 2025 + 1-year limited warranty = runs to 1 Dec 2026, 11 days from today. It covers panel, board and power supply defects only, so a no-picture fault may be covered if the technician confirms one of those.
    Safety first: no manual on the NAS to quote. Universal advice: switch the TV off and unplug it at the wall.
    Try this: there is no manual for Lumora 55Q8 on your NAS, so I have no model-specific steps and will not guess any.
    Claim: draft ready for care@lumora-tv.example or 1-800-555-0166. Save it to your NAS? (yes / no)
    Evidence:
      - home-library/Documents/Receipts/2025/Brightline_order_TV_Lumora.pdf: purchase 2025-12-01, order BL-2025-1201-77420, 55Q8, serial LU55-2511-90233, 1-year warranty line
      - home-library/Scans/Lumora_TV_warranty.pdf: 1 year panel, board and power supply, exclusions, claim contact, rear-label photo required
    Notes: The warranty ends in 11 days, so send the claim soon. The claim needs a photo of the rear label showing the serial number; there is none on the NAS, so take one. Exclusions include wall-mount damage and unauthorized repair. No Lumora 55Q8 manual was found.

Claim draft shown with it:

    To: care@lumora-tv.example or 1-800-555-0166
    Subject: Warranty claim, Lumora 55Q8, serial LU55-2511-90233
    Product: Lumora 55Q8, serial LU55-2511-90233
    Purchased: 2025-12-01 at Brightline Electronics, order BL-2025-1201-77420
    Coverage: Lumora 1-year limited warranty (panel, board and power supply), valid until 2026-12-01
    Fault: TV has sound but no picture
    Already tried: none confirmed yet
    Attachments: home-library/Documents/Receipts/2025/Brightline_order_TV_Lumora.pdf, home-library/Scans/Lumora_TV_warranty.pdf, photo of the rear label showing the serial number (not on the NAS yet)
    Contact: (left blank)

## Turn 2. User: "no"
No knowledge-agent call is made. Parent: "Nothing was saved. The draft stays in this chat; copy it if you want it." Status `cancelled`. (SKILL.md also defines `completed` as "answer delivered, with or without a saved note", so a declined save fits two statuses; defect D9.)

Status tokens: `waiting_approval` (turn 1), then `cancelled` (turn 2).
