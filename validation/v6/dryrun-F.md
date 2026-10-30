# Dry run F (v6): "Is my coffee machine under warranty?"

Today 2026-11-20 08:40. Paths relative to the library root. Skill followed literally, v6 text. Round 1.

## Intake
Mode: fault mode (asks about one product), coverage question. Product: coffee machine. No short names known, so none added. No fault, no code, no brand or model.

## Step 0
Skipped (v6 fix 6): no fault, no code, product known. In v5 this step returned only the unrelated E15 photo.

## Step 1
### Delegation 1 to file-agent
> Find files whose names contain any of: receipt, invoice, order, purchase, quittung, coffee machine. Search folders whose names contain Receipts, Invoices, Purchases, Orders, Documents, Scans or Downloads first, then all user files. File types: documents and images. Return full path, file name, type, size and modified date for each, up to 50. If there are no results, say zero matches.

Result: 4: Documents/Receipts/2019/receipt_dishwasher_old.pdf; Documents/Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf; Documents/Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf; Documents/Receipts/2025/Brightline_order_TV_Lumora.pdf.

### Delegation 2 to photo-agent
> Search the photo library for photos of a paper receipt or till slip that mention coffee machine, and for photos of any appliance rating plate or serial label. Newest first, up to 20 of each. For each photo found, run text recognition and return the photo path, the date taken, whether it is a receipt or a rating plate, and the recognised text. If there are no results, say zero matches.

Result: receipts: zero matches. Plates: ADW-4820 (2024-03-16) and FR-560 (2022-01-15).

Parent: every file name points to a dishwasher, fridge or TV, so no file remains and no extraction is sent. Neither plate matches a model the user gave or an extracted receipt; both ignored. No purchase record.

## Answer
```
I couldn't find a receipt for your coffee machine on the NAS. Do you know roughly when you bought it?
```

Status: `waiting_user`. No dishwasher, fridge or TV document was used.

Delegations: 2 (file-agent 1, photo-agent 1). v5: 3.

## Check against expected
Nothing found, asks roughly when bought, waiting_user, no dishwasher documents used. PASS.
