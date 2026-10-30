# Dry run F (v8): "Is my coffee machine under warranty?"

Today 2026-11-20 08:40. Paths relative to project/testdata/home-library/. v8 SKILL.md, experts played from the real files (method as in dryrun-A).

## Intake
Fault mode, coverage question. Product: coffee machine (no short names added). No fault, no code.

## Step 0
Skipped: no fault, no code, product known. The new delegation-order line starts with photo-agent (recent photos) without saying it is conditional; the Step 0 skip rule is explicit, so it was followed (observation O1).

## Step 1
**1. file-agent**
> Read only; do not change any file. Find files whose names contain any of: receipt, invoice, order, purchase, quittung, coffee machine. Search folders whose names contain Receipts, Invoices, Purchases, Orders, Documents, Scans or Downloads first, then the rest of the home folder and the shared folders this user can access. File types: documents and images. Return full path, file name, type, size and modified date for each, up to 50. If there are no results, say zero matches.

Result (matcher): 4. The 2019 and 2024 dishwasher receipts, the 2022 fridge receipt, the 2025 TV order.

**2. photo-agent**
> Read only; do not change any photo. Search the photo library for photos of a paper receipt or till slip that mention coffee machine, and for photos of any appliance rating plate or serial label. Newest first, up to 20 of each. [...]

Result: receipts zero matches (the only receipt photo is for a WM-7 washer). Plates ADW-4820, FR-560.

Parent: every file names another product; no file remains, no extraction. Plates match no model. No purchase record.

## Answer
```
I couldn't find a receipt for your coffee machine on the NAS. Do you know roughly when you bought it?
```
Status `waiting_user`. Delegations: 2 (file 1, photo 1). No dishwasher, fridge or TV document used.

## Check
Nothing found, asks when bought, waiting_user, no dishwasher documents. PASS. Same as v6.
