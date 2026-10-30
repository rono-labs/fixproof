# Dry run G (v8): "My washing machine is showing E15."

Today 2026-11-20 08:40. Paths relative to project/testdata/home-library/. v8 SKILL.md, experts played from the real files (method as in dryrun-A). Trap: today's photo shows E15 on a Nordvik dishwasher panel.

## Intake
Fault mode. Product: washing machine (file-agent: washer, WM; photo-agent: washing machine). Code E15 (typed). Step 0 runs.

## Step 0
**1. photo-agent** (v8 Step 0 text). Result: IMG_20261120_083012.jpg (EXIF 2026:11:20 08:30:12), "NORDVIK" "E15", kind not visible.

Parent: not a washing machine; display only, and a typed code equal to the photo's does not count as pointing to it; no "this" wording. Ignored; brand Nordvik not taken.

## Step 1
**2. file-agent** (same terms as run B, v8 scope wording). Result (matcher): same 6 as B.

**3. photo-agent** (receipts mentioning washing machine; plates). Result: WM-7 receipt photo IMG_20230602_181404.jpg (HomeHub, 06/02/2023, HH-230602-1187, Nordvik WM-7, NV7-2305-60912, $899.00); plates ADW-4820, FR-560.

Parent: no PDF receipt remains, no extraction. Purchase record from the receipt photo; 2 June 2023 reading. Brand and model from the washer receipt only.

## Step 2
**4. file-agent** (warranty terms + Nordvik, WM-7, HomeHub). Result: same 8 as B.

**5. document-agent**
> Read only; do not change any file. Read the contents of these files: Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf, Scans/2024/Brightline_EPP_terms_scan.pdf. List only the files that are a warranty, guarantee, protection plan or warranty registration for Nordvik WM-7, or a plan bought with order HH-230602-1187. [...]

Result: WM-7 card only.

**6. document-agent** (terms, WM-7 card). Result: 2 years parts and labor from purchase, no extended components, no printed dates.

## Step 3
One document path, no reconcile. Ended 2 Jun 2025. Not covered.

## Step 4
**7. file-agent** (manual terms + WM-7, Nordvik). Result: 7; sent WM-7_manual.pdf and Manuals/Nordvik_ADW-48xx_UserManual.pdf.

**8. document-agent** (content check for Nordvik WM-7). Result: WM-7_manual.pdf only.

**9. document-agent**
> Read only; do not change any file. Using only Home/Appliances/Washer/WM-7_manual.pdf, find what the manual says about error code E15. Return, as a table, the matching rows of the error-code and troubleshooting tables (problem, cause, what to do) in the order printed, the safety warnings that apply to those steps, any steps that need a qualified technician, and any statement that user repairs affect the warranty. If there is no entry for the code or symptom, return the support or service contact printed in the manual. Give the page or section for each item.

Result (pdftotext): no E15 entry. Error-code table s.4 p.6 lists F21, E03, E10; troubleshooting p.7 has no E15 row. Support p.1: "Nordvik | Support: support@nordvik-support.example | 1-800-555-0188".

Parent: say the manual has no entry, universal safety only (all three lines fit a washer), Not covered so give the support contact. Never the dishwasher manual's E15 row.

## Step 5
Not covered, no draft.

## Final answer
```
Product: Nordvik WM-7 (washing machine), bought 2 Jun 2023 at HomeHub Appliances
Coverage: Not covered. Bought 2 Jun 2023 + 2-year warranty = ended 2 Jun 2025.
Safety first: The manual for Nordvik WM-7 has no entry for E15.
  - Switch the appliance off at the wall or unplug it.
  - If it is leaking, close the water supply valve.
  - If you smell gas or burning, or see smoke or sparks, leave it off and call a qualified technician.
Support: support@nordvik-support.example, 1-800-555-0188 (WM-7 manual, page 1)
Evidence:
  - Photos/Phone/2023-06/IMG_20230602_181404.jpg: receipt photo, date 06/02/2023, WM-7, serial NV7-2305-60912
  - Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf: 2 years parts and labor from purchase
  - Home/Appliances/Washer/WM-7_manual.pdf: error-code table has no E15 (page 6); support contact (page 1)
Notes: 06/02/2023 is read as 2 June 2023 (US store, order HH-230602, photo date). Today's photo of an E15 display was not used: it does not show a washing machine.
```
Status `completed`. Delegations: 9 (photo 2, file 3, document 4). One round.

## Check
Not changed by the dishwasher E15 photo; receipt photo; Not covered, ended 2 Jun 2025; no E15 entry stated, universal safety only, support contact given; completed. PASS. Same as v6 round 2. Open v6 note N2 (word "gas" kept for a washer) unchanged.
