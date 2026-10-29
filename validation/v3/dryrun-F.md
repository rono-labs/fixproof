# Dry run F: "Is my coffee machine under warranty?"

Today 2026-11-20 08:40. Paths relative to `project/testdata/home-library/`. Mode: fault (one product, warranty question). Product: coffee machine. No symptom, no code.

## D1 photo-agent (Step 0)
Instruction: `Search photos taken in the last 48 hours, up to 2026-11-20 08:40, for pictures of an appliance control panel or display showing an error code, or of an appliance rating plate or serial label. For each photo found, run text recognition and return the photo path, the time taken and the recognised text. If there are no results, say zero matches.`
Result: 1 photo, `Photos/Phone/2026-11/IMG_20261120_083012.jpg`, 2026-11-20 08:30:12, text "NORDVIK  E15  POWER  CYCLE  DELAY  START".
Parent (literal rule): code and brand present, user named no brand, no product type in the text. Tentatively keep brand Nordvik, code E15. (A coffee machine with a Nordvik E15 panel is not ruled out by the skill.)

## D2 file-agent (Step 1, names)
Instruction: `Find files whose names contain any of: receipt, invoice, order, purchase, quittung, Nordvik, coffee machine. Search folders whose names contain Receipts, Invoices, Purchases, Orders, Documents, Scans or Downloads first, then all user files. File types: documents and images. Return full path, file name, type, size and modified date for each, up to 50. If there are no results, say zero matches.`
Result, 8 files: the five Receipts PDFs (2019 dishwasher, 2022 fridge, 2024 dishwasher, 2025 TV, 2025 soundbar), Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf, Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf, Manuals/Nordvik_ADW-48xx_UserManual.pdf. No name mentions a coffee machine.

## D3 photo-agent (Step 1)
Instruction: `Search the photo library for photos of a paper receipt or till slip, and for photos of an appliance rating plate or serial label, that mention coffee machine or Nordvik. For each photo found, run text recognition and return the photo path, the date taken, whether it is a receipt or a rating plate, and the recognised text. If there are no results, say zero matches.`
Result, 2 photos: `Photos/Phone/2024-03/IMG_20240316_190455.jpg` (Nordvik ADW-4820 plate) and `Photos/Phone/2023-06/IMG_20230602_181404.jpg` (HomeHub receipt for a Nordvik WM-7 washer). Both name other products. No coffee machine photo.

## Step 1 decision
All five receipt names point to other products (dishwasher, fridge, TV, soundbar), and both photos name other products. Per the skill these count as no match. No path is left for the extract instruction, so the document-agent is not called. No purchase record in either result.

## Reply (status waiting_user)
"I couldn't find a receipt for your coffee machine on the NAS. Do you know roughly when you bought it?"

Nothing else runs until the user replies. If the user gives a date, the verdict would be labelled "based on the date you gave"; if not, the verdict is skipped and the skill continues from Step 4 (which still needs a brand or model it does not have).

Delegations: 3 (photo 2, file 1). No save, nothing written.
