# Dry run F: "Is my coffee machine under warranty?"

Today 2026-11-20 08:40. Paths relative to project/testdata/home-library/. Mode: fault (one product asked about). Product: coffee machine. No code, brand or model.

## Step 0

DELEGATE photo-agent:
'Search photos taken in the last 48 hours, up to 2026-11-20 08:40, for pictures of an appliance control panel or display showing an error code, or of an appliance rating plate or serial label. If the search cannot filter by time, take the 20 newest photos instead. For each photo found, up to 20, run text recognition and return the photo path, the time taken, the recognised text, and which kind of appliance the photo shows. If there are no results, say zero matches.'
Result: 1 photo, IMG_20261120_083012.jpg, 2026-11-20 08:30:12, "NORDVIK", "E15", POWER/CYCLE/DELAY/START; kind not visible.
Parent: nothing shows a coffee machine. Ignored (D1: if the "kind" gate were read loosely, this Nordvik photo would be taken as the coffee machine's brand).

## Step 1

DELEGATE file-agent:
'Find files whose names contain any of: receipt, invoice, order, purchase, quittung, coffee machine. Search folders whose names contain Receipts, Invoices, Purchases, Orders, Documents, Scans or Downloads first, then all user files. File types: documents and images. Return full path, file name, type, size and modified date for each, up to 50. If there are no results, say zero matches.'
Result: 5 files, all through the Receipts folder or the word "receipt"/"order": the 2019 dishwasher, 2022 fridge, 2024 dishwasher, 2025 TV and 2025 soundbar receipts. None names a coffee machine.

DELEGATE photo-agent:
'Search the photo library for photos of a paper receipt or till slip that mention coffee machine, and for photos of any appliance rating plate or serial label. Newest first, up to 20 of each. For each photo found, run text recognition and return the photo path, the date taken, whether it is a receipt or a rating plate, and the recognised text. If there are no results, say zero matches.'
Result: no receipt photo mentions a coffee machine. Plates returned: IMG_20240316_190455.jpg (NORDVIK ADW-4820, NV48-2203-1187) and IMG_20220115_101233.jpg (HomeHub FR-560, HH56-2201-30647). Neither is a coffee machine: ignored.

Parent: every receipt name points to a different product (dishwasher, fridge, TV, soundbar), so no document-agent extraction is sent. Receipts that name a different product count as no match. No purchase record for a coffee machine.

## Reply (status waiting_user)

"I couldn't find a receipt for your coffee machine on the NAS. Do you know roughly when you bought it?"

Nothing else runs. No dishwasher, TV or other documents are used. No verdict, no claim, no knowledge-agent call.

Delegations: 3 = photo-agent 2, file-agent 1.
