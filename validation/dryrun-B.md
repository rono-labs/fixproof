# Dry run B (v8): "Washing machine shows F21. Is it still under warranty?"

Today 2026-11-20 08:40. Paths relative to testdata/home-library/. v8 SKILL.md, experts played from the real files (method as in dryrun-A).

## Intake
Fault mode. Product: washing machine (file-agent: washer, WM; photo-agent: washing machine). Code F21. No brand or model. Code given, Step 0 runs.

## Step 0
**1. photo-agent** (v8 Step 0 text, now = 2026-11-20 08:40)
Result: IMG_20261120_083012.jpg, "NORDVIK" "E15", kind not visible. Parent: not a washing machine, words do not point to it, code differs from F21. Ignored.

## Step 1
**2. file-agent**
> Read only; do not change any file. Find files whose names contain any of: receipt, invoice, order, purchase, quittung, washing machine, washer, WM. Search folders whose names contain Receipts, Invoices, Purchases, Orders, Documents, Scans or Downloads first, then the rest of the home folder and the shared folders this user can access. File types: documents and images. Return full path, file name, type, size and modified date for each, up to 50. If there are no results, say zero matches.

Result (matcher): 6. Four receipts (2019 and 2024 dishwasher via "washer" substring, 2022 fridge, 2025 TV order), Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf, Home/Appliances/Washer/WM-7_manual.pdf.

**3. photo-agent**
> Read only; do not change any photo. Search the photo library for photos of a paper receipt or till slip that mention washing machine, and for photos of any appliance rating plate or serial label. Newest first, up to 20 of each. [...]

Result: receipt Photos/Phone/2023-06/IMG_20230602_181404.jpg (EXIF 2023:06:02 18:14:04): "HOMEHUB APPLIANCES 77 Harbor Road, Port Alder OR / Date: 06/02/2023 Order HH-230602-1187 / Nordvik WM-7 Front Load Washer SN NV7-2305-60912 $899.00 / Delivery $59.00 / TOTAL $958.00 / Warranty: see manufacturer card". Plates ADW-4820 and FR-560.

Parent: every PDF receipt names another product; the WM-7 card and manual are not receipts. No extraction sent. Purchase record is the receipt photo. 06/02/2023 read as 2 June 2023 (Oregon store, order HH-230602, photo date). Series left out (WM-7). Plates do not match WM-7.

## Step 2
**4. file-agent**
> Read only; do not change any file. Find files whose names contain any of: warranty, guarantee, garantie, protection, plan, care, extended, registration, certificate, terms, conditions, Nordvik, WM-7, HomeHub. Search folders whose names contain Warranty, Receipts, Scans, Documents, Home or Appliances first, then the rest of the home folder and the shared folders this user can access. [...]

Result: 8 (WM-7 card, WM-7 manual, ADW-4820 card, FR-560 registration, Lumora TV warranty, EPP terms scan, HomeHub fridge receipt, Nordvik ADW-48xx manual). No plan on the receipt, no Scans listing.

**5. document-agent**
> Read only; do not change any file. Read the contents of these files: Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf, Scans/2024/Brightline_EPP_terms_scan.pdf. List only the files that are a warranty, guarantee, protection plan or warranty registration for Nordvik WM-7, or a plan bought with order HH-230602-1187. For each, quote the line that shows it. If none match, say zero matches.

Result: WM-7 card only, "Product: WM-7 Front Load Washing Machine". EPP scan covers ADW-4820, order BL-2024-0314-55871.

**6. document-agent**
> Read only; do not change any file. Answer from these files only: Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf. Return a table with one row per document: [...] If a file has no warranty terms, say so for that file. Report any file you could not read.

Result p.1: Nordvik, parts and labor 2 years from original purchase date, "This warranty has no extended components", no printed dates; exclusions misuse, installation faults, hoses, cosmetic, unauthorized repairs, commercial use; claim claims@nordvik-support.example / 1-800-555-0188.

## Step 3
One document path, no reconcile. 2 Jun 2023 + 2 y = ended 2 Jun 2025 (the 6 Feb reading also ends in 2025). Not covered.

## Step 4
**7. file-agent** (manual search, terms manual, guide, instructions, handbook, quick start, WM-7, Nordvik; v8 scope wording)
Result: 7. Named as manual and with brand/model: WM-7_manual.pdf, Manuals/Nordvik_ADW-48xx_UserManual.pdf.

**8. document-agent**
> Read only; do not change any file. Read the contents of these files: Home/Appliances/Washer/WM-7_manual.pdf, Manuals/Nordvik_ADW-48xx_UserManual.pdf. List only the files that are the user manual or guide for Nordvik WM-7, and quote the line that shows it. If none match, say zero matches.

Result: WM-7_manual.pdf only, "Nordvik Washing Machine Model series WM-7 User Manual and Care Guide" (p.1).

**9. document-agent**
> Read only; do not change any file. Using only Home/Appliances/Washer/WM-7_manual.pdf, find what the manual says about error code F21. Return, as a table, the matching rows [...]

Result: s.4 p.6 F21 "Drain fault: water not draining." / "Pause, power off, clean the drain pump filter behind the lower right panel (have a towel ready), check the drain hose for kinks, restart." s.5 p.7 "Water left in drum, F21" / "Blocked pump filter or hose" / "Clean pump filter, check hose". Safety p.3 "Do not open the door while the drum is turning." No technician-only step; no user-repair statement.

Parent: drain fault without leak, safety does not lead.

## Step 5
Not covered, no draft.

## Final answer
```
Product: Nordvik WM-7 (washing machine), bought 2 Jun 2023 at HomeHub Appliances
Coverage: Not covered. Bought 2 Jun 2023 + 2-year warranty = ended 2 Jun 2025.
Safety first: "Do not open the door while the drum is turning." (manual page 3)
Try this (manual section 4 page 6, section 5 page 7):
  1. Pause and power off.
  2. Clean the drain pump filter behind the lower right panel. Have a towel ready.
  3. Check the drain hose for kinks.
  4. Restart.
Evidence:
  - Photos/Phone/2023-06/IMG_20230602_181404.jpg: receipt photo, date 06/02/2023, WM-7, serial NV7-2305-60912, order HH-230602-1187
  - Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf: 2 years parts and labor from purchase
  - Home/Appliances/Washer/WM-7_manual.pdf: F21 rows, safety
Notes: The receipt exists only as a phone photo. 06/02/2023 is read as 2 June 2023 (US store in Oregon, order HH-230602, photo taken 2 Jun 2023). Today's E15 photo shows a different code and was not used.
```
Status `completed`. Delegations: 9 (photo 2, file 3, document 4).

## Check
Not covered, 2 June 2023 reading, ended 2025-06-02, F21 drain steps, no draft, completed. PASS. Same as v6.
