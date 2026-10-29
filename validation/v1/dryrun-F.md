# Dry run F: "Is my coffee machine under warranty?"

Today = 2026-11-20. Paths are relative to `project/testdata/home-library/`. Expert results are emulated from `find`, `grep`, `pdftotext` and by viewing every photo in the library.

## Intake
Mode: fault (the user asks about one product). Product: coffee machine. Symptom: none, only a warranty question. No brand or model.

## Step 1. Purchase record

delegate --target file-agent --instruction 'Find documents that look like receipts, invoices or order confirmations for a coffee machine. Search folders whose names contain Receipts, Invoices, Purchases, Orders, Documents, Scans or Downloads first, then all of the user files. Include PDF, image and office document types. For each match return the full path, file name, type and modified date, up to 30 matches. If there are no results, say zero matches.'

file-agent result: zero matches. No file name contains "coffee", "espresso" or "brew", and no document text mentions a coffee machine (checked with a text search over all 18 PDFs; the recipe collection and the newsletter do not mention one either).

delegate --target photo-agent --instruction 'Search the photo library for photos of a paper receipt or of an appliance rating plate or serial label for a coffee machine. For each photo found, run text recognition and return the photo path, the date taken and the recognised text. If there are no results, say zero matches.'

photo-agent result: the same three paper/plate photos as in the other runs (dishwasher plate Nordvik ADW-4820, fridge plate HomeHub FR-560, washer receipt Nordvik WM-7). None mentions a coffee machine. The other six images (vacation, wallpaper, three phone snapshots) are abstract colour pictures with no text. Parent judges the three as other products and treats the photo search as empty. SKILL.md says "both searches return an empty result" and does not say whether a list of irrelevant photos counts as empty (defect D13).

## Decision
Both searches are empty for a coffee machine. SKILL.md Step 1 says: tell the user "I could not find a receipt for your {product} on the NAS", ask whether they know the purchase date, report `waiting_user`, and "continue with Step 4 if they do not". The status table says that while waiting "nothing else runs until the user replies". This run follows the status table and sends no further delegations. The dishwasher, washer, fridge and TV documents are not used for a coffee machine.

## Final answer

    I could not find a receipt for your coffee machine on the NAS. Do you know roughly when you bought it? If you do, I can work out the warranty end date from that, based on the date you gave, but I will need to know the brand and the warranty term too.

Status token: `waiting_user`.

Note on the wording: SKILL.md gives the receipt-only message above. examples.md scenario 6 uses "I could not find a receipt, warranty or manual for a coffee machine on your NAS", which assumes warranty and manual searches that SKILL.md does not run at this point (defect D13).
