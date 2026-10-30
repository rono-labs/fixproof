# Dry run A (v6): "The dishwasher is doing this again."

Today 2026-11-20 08:40. Paths are relative to the library root (project/testdata/home-library/). Skill text followed literally, as edited in v6. Experts played from the real files: pdftotext for documents, the image itself plus EXIF DateTimeOriginal for photos, case-insensitive name-substring matching for file-agent find. Round 1.

## Intake
Mode: fault mode. Product: dishwasher. File-agent short name: DW (photo-agent gets the type alone, v6 rule). Symptom: "doing this again" (vague, repeat fault). No code, brand or model typed. The user reports a fault, so Step 0 runs.

## Step 0
### Delegation 1 to photo-agent
> Search photos taken in the last 48 hours, up to 2026-11-20 08:40, for pictures of an appliance control panel or display showing an error code, or of an appliance rating plate or serial label. If the search cannot filter by time, take the 20 newest photos instead. For each photo found, up to 20, run text recognition and return the photo path, the time taken, the recognised text, and which kind of appliance the photo shows. If there are no results, say zero matches.

Result: 1 match. Photos/Phone/2026-11/IMG_20261120_083012.jpg, taken 2026-11-20 08:30:12. Text: "NORDVIK", "E15", buttons POWER, CYCLE, DELAY, START. Kind of appliance: not visible (control panel only).

Parent: the photo shows a code and a brand, shows only a display, and the user's words "doing this" point to it. Used. Code E15 (the user gave none), brand Nordvik. Added to evidence.

## Step 1
### Delegation 2 to file-agent
> Find files whose names contain any of: receipt, invoice, order, purchase, quittung, Nordvik, dishwasher, DW. Search folders whose names contain Receipts, Invoices, Purchases, Orders, Documents, Scans or Downloads first, then all user files. File types: documents and images. Return full path, file name, type, size and modified date for each, up to 50. If there are no results, say zero matches.

Result: 8 matches: Documents/Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf (2969); Documents/Receipts/2019/receipt_dishwasher_old.pdf (2794); Documents/Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf (2733); Documents/Receipts/2025/Brightline_order_TV_Lumora.pdf (2762); Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf (2960); Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf (2681); Manuals/Nordvik_ADW-48xx_UserManual.pdf (17516); Downloads/ADW-48xx_manual (1).pdf (17516). All PDF, modified 2026-10-29.

### Delegation 3 to photo-agent
> Search the photo library for photos of a paper receipt or till slip that mention dishwasher or Nordvik, and for photos of any appliance rating plate or serial label. Newest first, up to 20 of each. For each photo found, run text recognition and return the photo path, the date taken, whether it is a receipt or a rating plate, and the recognised text. If there are no results, say zero matches.

Result: receipts: 1, Photos/Phone/2023-06/IMG_20230602_181404.jpg (2023-06-02 18:14:04), receipt, "HOMEHUB APPLIANCES ... Date: 06/02/2023 Order HH-230602-1187 ... Nordvik WM-7 Front Load Washer SN NV7-2305-60912 $899.00 ...". It mentions Nordvik. Rating plates: 2. Photos/Phone/2024-03/IMG_20240316_190455.jpg (2024-03-16 19:04:55): "NORDVIK MODEL: ADW-4820 SERIAL: NV48-2203-1187 120V 60Hz 15A 1800W MFD 2023-12". Photos/Phone/2022-01/IMG_20220115_101233.jpg (2022-01-15 10:12:33): "HomeHub MODEL: FR-560 SERIAL: HH56-2201-30647 ...".

Parent: the receipt photo names a washer, a different product. Dropped.

### Delegation 4 to document-agent
Parent, choosing files (v6 rule: receipts, orders and invoices only, never warranty cards or manuals; drop names pointing to a different product): fridge receipt and TV order dropped; the two warranty cards and two manuals are not receipts. Kept: the two dishwasher receipts.

> Extract purchase details with the receipt schema from these files: Documents/Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf, Documents/Receipts/2019/receipt_dishwasher_old.pdf. If a file returns no data with the receipt schema, try the invoice schema. For each file return store, order number, purchase date exactly as printed, product description, brand, model number, serial number if printed, price, any warranty term printed on the receipt, and every other line item, especially any protection plan, extended warranty or care plan with its plan number and term. Report any file you could not read.

Result:
- 2024 file: Brightline Electronics, order BL-2024-0314-55871, date 2024-03-14, Nordvik ADW-4820 Dishwasher, serial NV48-2203-1187, $849.00, no warranty term printed. Other lines: "3-Year Extended Protection Plan", plan no. EPP-3Y-90417733, "Covers ADW-4820 after the manufacturer warranty ends. Terms provided separately.", $129.00; Installation kit $24.99.
- 2019 file: Brightline Electronics, order BL-2019-0822-20318, date 2019-08-22, Nordvik ADW-3100 Dishwasher, serial NV31-1905-0342, $529.00, "Manufacturer warranty: 1 year parts and labor. No extended plan purchased."; haul-away $25.00.
No unreadable files.

Parent: two dishwasher purchases. The ADW-4820 plate (serial NV48-2203-1187) matches exactly one receipt, the 2024 one. Settled without asking; 2019 purchase to Notes. FR-560 plate matches no extracted receipt, ignored. Model ADW-4820, series ADW-48xx, store Brightline, order BL-2024-0314-55871.

## Step 2
### Delegation 5 to file-agent
> Find files whose names contain any of: warranty, guarantee, garantie, protection, plan, care, extended, registration, certificate, terms, conditions, Nordvik, ADW-4820, ADW-48xx, Brightline. Search folders whose names contain Warranty, Receipts, Scans, Documents, Home or Appliances first, then all user files. File types: documents and images. Return full path, file name, size and modified date for each, up to 50. If there are no results, say zero matches.

Result: 10 matches: Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf; Scans/2024/Brightline_EPP_terms_scan.pdf; Scans/Lumora_TV_warranty.pdf; Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf; Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf; Documents/Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf; Documents/Receipts/2025/Brightline_order_TV_Lumora.pdf; Documents/Receipts/2025/Brightline_soundbar_2025-12-18.pdf; Manuals/Nordvik_ADW-48xx_UserManual.pdf; Downloads/ADW-48xx_manual (1).pdf.

Parent: the receipt lists a plan, and results include "terms" and the store name, and one sits in Scans. No extra Scans listing.

### Delegation 6 to document-agent
Candidates (names suggest warranty, plan, terms or registration and name no other product, or name no product): the ADW-4820 card and the EPP terms scan. TV, washer and fridge warranty files name other products and are dropped.

> With intent locate_content and evidence mode focused, check these files: Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf, Scans/2024/Brightline_EPP_terms_scan.pdf. List only the files that are a warranty, guarantee, protection plan or warranty registration for Nordvik ADW-4820 or the series ADW-48xx, or a plan bought with order BL-2024-0314-55871. For each, quote the line that shows it. If none match, say zero matches.

Result: both. Card: "Product: ADW-4820 Dishwasher". Scan: "Covered product Nordvik ADW-4820 Dishwasher, serial NV48-2203-1187" and "Purchased 2024-03-14 (Brightline order BL-2024-0314-55871)".

### Delegation 7 to document-agent
> Answer from these files only: Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf, Scans/2024/Brightline_EPP_terms_scan.pdf. With intent period and answer mode table, return for each document: the provider, each coverage (full parts and labour, parts only, or named components such as motor, compressor or panel) with its term, how the start date is defined, and any printed start or end date. With intent condition, return the exclusions and the claim procedure (phone, email or web form exactly as written, required attachments). Also return any plan number, registration number and serial number written on it. Quote the page or section for each answer.

Result:
- Nordvik card, page 1: parts and labor 2 years; drive motor 10 years (wash motor and circulation pump motor, parts only after year 2). "Warranty starts on the date of original retail purchase." No printed dates, no serial. Exclusions: misuse, improper installation, power surges, frozen pipes, commercial use, cosmetic damage, consumables (filters, racks, gaskets), repairs by anyone other than a Nordvik authorized provider; owner repairs beyond the manual's steps void the warranty. Claim: "Email claims@nordvik-support.example or call 1-800-555-0188 (Mon-Fri 8:00-18:00 Pacific)", with dated receipt and serial-plate photo.
- Brightline plan terms, page 1: Brightline Protection Services; plan EPP-3Y-90417733; serial NV48-2203-1187. Section 1: parts and labor for mechanical and electrical failure, "including leaks from internal components, drain pump, heater, control board and sensors". "Plan start 2026-03-14, the day after the 2-year manufacturer warranty ends"; "Plan end 2029-03-14". Section 2 exclusions: cosmetic damage, racks, filters and gaskets, misuse or improper installation, pre-existing conditions, commercial use, unapproved repairs; owner repairs beyond the manual void the plan. Section 3: "Email protect@brightline-services.example or call 1-800-555-0199. Have your plan number, the original receipt, and the product serial number ready."

## Step 3
### Delegation 8 to document-agent
> Reconcile these files and report every difference in brand, model number, serial number, purchase date, plan start or end date, or owner name: Documents/Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf, Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf, Scans/2024/Brightline_EPP_terms_scan.pdf. For each difference give both values and the file each came from. If they all agree, say no differences found.

Result: no differences found.

Parent: plate serial NV48-2203-1187 equals the receipt. Arithmetic: 14 Mar 2024 + 2 years = 14 Mar 2026, active on that day only, so ended. Plan: v6 rule 4 gives a calculated start of 15 Mar 2026 (the day after the base warranty ends). The plan prints 14 Mar 2026, one day earlier: printed date kept, one-day gap noted, not a conflict. Plan end printed 14 Mar 2029: active. Motor: 14 Mar 2034, parts only after year 2. Label: Covered. Exclusions: the manual's E15 causes (below) are loose hose, door gasket or internal leak; gaskets are excluded, internal leaks covered, so the label stays and a Note quotes the exclusion.

## Step 4
### Delegation 9 to file-agent
> Find files whose names contain any of: manual, guide, instructions, handbook, quick start, ADW-4820, ADW-48xx, Nordvik. Search folders whose names contain Manuals, Documents, Downloads, Home or Appliances first, then all user files. File type: documents. Return full path, file name, size and modified date, up to 20. If there are no results, say zero matches.

Result: 7: Manuals/Nordvik_ADW-48xx_UserManual.pdf (17516); Downloads/ADW-48xx_manual (1).pdf (17516); Manuals/Zentro_AX3000_Router_Manual.pdf (6029); Home/Appliances/Washer/WM-7_manual.pdf (9774); Home/Appliances/Fridge/FR-560_owner_manual.pdf (9127); Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf (2960); Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf (2681).

Parent: named as a manual and with brand, model or series: the two ADW-48xx files only.

### Delegation 10 to document-agent
> With intent locate_content, check these files: Manuals/Nordvik_ADW-48xx_UserManual.pdf, Downloads/ADW-48xx_manual (1).pdf. List only the files that are the user manual or guide for Nordvik ADW-4820 or the series ADW-48xx, and quote the line that shows it. If none match, say zero matches.

Result: both, "Nordvik Dishwasher Model series ADW-48xx User Manual and Care Guide" (page 1).

### Delegation 11 to file-agent
> Return the sha256sum of each of these files: Manuals/Nordvik_ADW-48xx_UserManual.pdf, Downloads/ADW-48xx_manual (1).pdf.

Result: both 2858e0506bfc17fb3076623c5b917c28c11cb91b4650cc02af821eb6bfde3b7d. Parent keeps Manuals/ (more specific folder), notes the duplicate.

### Delegation 12 to document-agent
Symptom words are vague, so the code is sent alone.

> Using only Manuals/Nordvik_ADW-48xx_UserManual.pdf, with intent locate_content and answer mode table, find what the manual says about error code E15. Return the matching rows of the error-code and troubleshooting tables (problem, cause, what to do) in the order printed, the safety warnings that apply to those steps, any steps that need a qualified technician, and any statement that user repairs affect the warranty. If there is no entry for the code or symptom, return the support or service contact printed in the manual. Give the page or section for each item.

Result:
- Section 7, page 9: E15, "Water detected in the base pan. Leak protection has stopped the unit." Action: "Turn off water, unplug, tilt unit slightly to drain base pan only if instructed, check door gasket and hose connections. If E15 returns, call service. Do not open the base."
- Section 8, page 10: "Puddle under unit, E15 shown", cause "Water in base pan: loose hose, door gasket, or internal leak", solution "Stop the unit, check hose clamps and gasket. Service call if the leak persists".
- Safety, page 3: "Do not operate a dishwasher that is leaking. Turn off the water supply and unplug the unit."
- Technician: "call service", "Do not open the base". Warranty: page 3 "any user repair beyond the steps listed in this manual ... will void the manufacturer warranty and any extended protection plan"; page 10 same.
- Entry exists, so no support contact returned.

Parent: E15 describes water collecting inside a mains appliance, so the safety line leads. The user says "again" and the manual says "If E15 returns, call service": that line goes first.

## Step 5
Label Covered, so draft. Base warranty has ended, so the plan's contact. The plan procedure asks for plan number, receipt and serial; it does not ask for the plan terms, so (v6) the plan terms path is not an attachment and the plan number goes in the body.

Draft shown:
```
To: Email protect@brightline-services.example or call 1-800-555-0199
Subject: Warranty claim, Nordvik ADW-4820, serial NV48-2203-1187
Product: Nordvik ADW-4820 dishwasher, serial NV48-2203-1187
Purchased: 14 Mar 2024 at Brightline Electronics, order BL-2024-0314-55871
Coverage: 3-Year Extended Protection Plan EPP-3Y-90417733, valid until 14 Mar 2029
Fault: water in the base pan, leak protection stops the unit, error code E15, returned after an earlier occurrence
Already tried: none confirmed
Attachments: Documents/Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf
Contact:
```
Asked: "Which of these steps have you already tried? Say yes to save the draft to your NAS, or no." Status `waiting_approval`.

User: "I checked the hoses, yes save it". Already tried becomes "checked the hose connections". Clear yes.

### Delegation 13 to knowledge-agent
> Save this text as a new note in a folder named Warranty claims in the user home folder, or in the default notes location if that folder cannot be used, with filename hint "Warranty claim Nordvik ADW-4820 2026-11-20 0840", with time written as four digits such as 0840. Text: (the draft above, with "Already tried: checked the hose connections")

Result: saved, path /home/alex/Warranty claims/Warranty claim Nordvik ADW-4820 2026-11-20 0840.md (simulated success).

## Final answer
```
Safety first: Water in the base pan is a leak on a mains appliance. Switch the dishwasher off at the wall, close the water supply, and call a qualified technician if it persists. Manual: "Do not operate a dishwasher that is leaking. Turn off the water supply and unplug the unit." (page 3)
Product: Nordvik ADW-4820 (dishwasher), bought 14 Mar 2024 at Brightline Electronics
Coverage: Covered. Bought 14 Mar 2024 + 2-year warranty = ended 14 Mar 2026. Protection plan EPP-3Y-90417733 runs 14 Mar 2026 to 14 Mar 2029, so covered by the plan.
Try this (manual section 7 page 9, section 8 page 10):
  1. E15 has come back. The manual says: "If E15 returns, call service."
  2. Turn off the water and unplug the unit.
  3. Check the door gasket and the hose connections and clamps. You have checked the hoses.
  4. Tilt the unit slightly to drain the base pan only if instructed.
  Technician only: do not open the base. A repair beyond these steps voids the warranty and the protection plan (page 3).
Claim: draft ready for protect@brightline-services.example (or 1-800-555-0199).
  Claim draft saved to /home/alex/Warranty claims/Warranty claim Nordvik ADW-4820 2026-11-20 0840.md. Nothing was sent.
Evidence:
  - Photos/Phone/2026-11/IMG_20261120_083012.jpg: E15 and Nordvik, taken 20 Nov 2026 08:30
  - Documents/Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf: purchase 14 Mar 2024, ADW-4820, serial NV48-2203-1187, order, plan EPP-3Y-90417733
  - Photos/Phone/2024-03/IMG_20240316_190455.jpg: rating plate ADW-4820, serial NV48-2203-1187
  - Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf: 2 years parts and labor, motor 10 years (to 14 Mar 2034), exclusions
  - Scans/2024/Brightline_EPP_terms_scan.pdf: plan 14 Mar 2026 to 14 Mar 2029, exclusions, claim contact
  - Manuals/Nordvik_ADW-48xx_UserManual.pdf: E15 rows, safety, warranty warning
Notes: A 2019 Nordvik ADW-3100 (receipt 22 Aug 2019) also exists; the plate photo matches only the 2024 unit. Duplicate manual at Downloads/ADW-48xx_manual (1).pdf (same checksum). The plan says it starts the day after the warranty ends (15 Mar 2026) but prints 14 Mar 2026; the printed date is kept, a one-day gap. The plan excludes gaskets: a worn door gasket is excluded, an internal leak is covered.
```

Status: `completed`, saved.

Delegations: 13 (photo-agent 2, file-agent 4, document-agent 6, knowledge-agent 1).

## Check against expected
Covered, base ended 2026-03-14, plan to 2029-03-14: yes. Plate settles ADW-4820, 2024 receipt, 2019 in Notes: yes. E15 steps, safety first: yes. Duplicate noted: yes. Claim to protect@brightline-services.example, "Already tried: none confirmed", saved after the user's reply: yes. Completed: yes. PASS.

v6 effects seen: fix 5 kept the warranty cards and manuals out of the extraction (they were in the find result through "Nordvik" and "DW"). Fix 7: photo-agent got "dishwasher", not "DW". Fix 8: calculated plan start is now 15 Mar 2026, the one-day-gap note still applies. Fix 9: the attachments line lists only the receipt, which matches what the plan procedure asks for.
