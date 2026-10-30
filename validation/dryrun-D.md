# Dry run D (v8): "The TV has sound but no picture." (user declines the save)

Today 2026-11-20 08:40. Paths relative to testdata/home-library/. v8 SKILL.md, experts played from the real files (method as in dryrun-A).

## Intake
Fault mode. Product: TV (file-agent: TV, television; photo-agent: TV). Symptom "sound but no picture". Step 0 runs.

Description check (new, shorter frontmatter): the old text listed "broken, leaking, not working or showing an error code" and "appliance or device"; the new one says "broken appliance" and "broken, leaking or showing an error code". "Sound but no picture" on a TV is a not-working device. In this tabletop the skill is invoked directly, so the result is unaffected, but routing on a real NAS may be weaker (defect V8-2).

## Step 0
**1. photo-agent** (v8 Step 0 text). Result: E15 Nordvik panel photo. Ignored.

## Step 1
**2. file-agent**
> Read only; do not change any file. Find files whose names contain any of: receipt, invoice, order, purchase, quittung, TV, television. Search folders whose names contain Receipts, Invoices, Purchases, Orders, Documents, Scans or Downloads first, then the rest of the home folder and the shared folders this user can access. File types: documents and images. [...]

Result (matcher): 5. Documents/Receipts/2025/Brightline_order_TV_Lumora.pdf; Scans/Lumora_TV_warranty.pdf; three other receipts (dishwasher x2, fridge).

**3. photo-agent** (receipts mentioning TV; plates). Result: receipts zero; plates ADW-4820, FR-560 (ignored later).

**4. document-agent**
> Read only; do not change any file. Extract the purchase details from these receipts and invoices: Documents/Receipts/2025/Brightline_order_TV_Lumora.pdf. [...]

Result: Brightline Electronics, BL-2025-1201-77420, 2025-12-01, Lumora 55Q8 55 in. QLED TV, serial LU55-2511-90233, $699.00, "Lumora 1-year limited warranty applies from the date of purchase."; wall mount $39.99. No plan. Series left out (55Q8).

## Step 2
**5. file-agent** (warranty terms + Lumora, 55Q8, Brightline). Result: 8 (Lumora TV warranty, EPP terms scan, three Brightline receipts, ADW-4820 card, WM-7 card, FR-560 registration).

**6. document-agent**
> Read only; do not change any file. Read the contents of these files: Scans/Lumora_TV_warranty.pdf, Scans/2024/Brightline_EPP_terms_scan.pdf. List only the files that are a warranty [...] for Lumora 55Q8, or a plan bought with order BL-2025-1201-77420. [...]

Result: Lumora_TV_warranty.pdf, "Product: 55Q8 QLED Television". EPP scan no.

**7. document-agent** (terms). Result p.1: Lumora limited warranty 1 year, "Panel, board and power supply defects from the original purchase date"; counted from the retail purchase date on the receipt; no printed dates. Exclusions burn-in, cracked screens, physical damage, power surge, unauthorized repair, wall-mount damage. Claim "Email care@lumora-tv.example or call 1-800-555-0166. Attach receipt and a photo of the rear label showing the serial number."

## Step 3
**8. document-agent** (reconcile TV order + Lumora warranty). Result: no differences found. 1 Dec 2025 + 1 y = 1 Dec 2026, 11 days left. Covered, if the technician confirms a panel, board or power supply fault.

## Step 4
**9. file-agent** (manual terms + 55Q8, Lumora). Result (matcher): 7, none named both as a manual and with Lumora or 55Q8. Zero matches, no content check. No manual: universal safety advice only, water line dropped for a TV.

## Step 5
Draft (no checklist, so "Save this draft to your NAS? (yes / no)"), `waiting_approval`:
```
To: Email care@lumora-tv.example or call 1-800-555-0166
Subject: Warranty claim, Lumora 55Q8, serial LU55-2511-90233
Product: Lumora 55Q8, serial LU55-2511-90233
Purchased: 1 Dec 2025 at Brightline Electronics, order BL-2025-1201-77420
Coverage: Lumora 1-year limited warranty, valid until 1 Dec 2026
Fault: sound but no picture
Already tried: none confirmed
Attachments: Documents/Receipts/2025/Brightline_order_TV_Lumora.pdf; photo of the rear label: not on the NAS, take one before sending
Contact:
```
User: "No." Not saved, no knowledge-agent delegation.

## Final answer
```
Product: Lumora 55Q8 (TV), bought 1 Dec 2025 at Brightline Electronics
Coverage: Covered. Bought 1 Dec 2025 + 1-year warranty = runs to 1 Dec 2026, 11 days left, if the technician confirms a panel, board or power supply fault.
Safety first: There is no manual for Lumora 55Q8 on your NAS.
  - Switch the appliance off at the wall or unplug it.
  - If you smell gas or burning, or see smoke or sparks, leave it off and call a qualified technician.
Claim: draft ready for care@lumora-tv.example (or 1-800-555-0166).
  Claim draft not saved; it stays in this chat.
Evidence:
  - Documents/Receipts/2025/Brightline_order_TV_Lumora.pdf: purchase 1 Dec 2025, 55Q8, serial LU55-2511-90233
  - Scans/Lumora_TV_warranty.pdf: 1 year panel, board and power supply, exclusions, claim contact
Notes: The claim needs a photo of the rear label showing the serial; there is none on the NAS. Exclusions include burn-in, cracked screens and unauthorized repair. The warranty ends in 11 days.
```
Status `completed`, not saved. Delegations: 9 (photo 2, file 3, document 4).

## Check
Covered to 2026-12-01, 11 days, panel/board/PSU; no manual, universal safety only; draft to care@lumora-tv.example; declined, completed, not saved. PASS. Same as v6.
