# Dry run G (v6): "My washing machine is showing E15."

Today 2026-11-20 08:40. Paths relative to the library root. Skill followed literally, v6 text. Round 1. Trap: today's photo shows E15 on a Nordvik dishwasher panel.

## Intake
Mode: fault mode. Product: washing machine (file-agent: washer, WM; photo-agent: washing machine). Symptom: showing E15, code E15. No brand or model. Step 0 runs.

## Step 0
### Delegation 1 to photo-agent
> Search photos taken in the last 48 hours, up to 2026-11-20 08:40, for pictures of an appliance control panel or display showing an error code, or of an appliance rating plate or serial label. If the search cannot filter by time, take the 20 newest photos instead. For each photo found, up to 20, run text recognition and return the photo path, the time taken, the recognised text, and which kind of appliance the photo shows. If there are no results, say zero matches.

Result: 1 match, Photos/Phone/2026-11/IMG_20261120_083012.jpg, 08:30:12, "NORDVIK", "E15", POWER CYCLE DELAY START. Kind: not visible.

Parent: kind not visible, so it does not match "washing machine". Display only, so the second test applies: the user typed E15, and Step 0 says a typed code equal to the photo's does not count as pointing to it; no "this", "doing this" or "see the photo". Ignored. Brand Nordvik is not taken from it.

## Step 1
### Delegation 2 to file-agent
> Find files whose names contain any of: receipt, invoice, order, purchase, quittung, washing machine, washer, WM. Search folders whose names contain Receipts, Invoices, Purchases, Orders, Documents, Scans or Downloads first, then all user files. File types: documents and images. Return full path, file name, type, size and modified date for each, up to 50. If there are no results, say zero matches.

Result: same 6 as run B (four receipts named for dishwasher, fridge, TV; WM-7 card; WM-7 manual).

### Delegation 3 to photo-agent
> Search the photo library for photos of a paper receipt or till slip that mention washing machine, and for photos of any appliance rating plate or serial label. Newest first, up to 20 of each. For each photo found, run text recognition and return the photo path, the date taken, whether it is a receipt or a rating plate, and the recognised text. If there are no results, say zero matches.

Result: receipt photo Photos/Phone/2023-06/IMG_20230602_181404.jpg (Nordvik WM-7 Front Load Washer, SN NV7-2305-60912, Date 06/02/2023, Order HH-230602-1187, HomeHub Appliances, $899.00). Plates: ADW-4820 (2024-03-16) and FR-560 (2022-01-15).

Parent: no PDF receipt remains (other products, or not receipts), so no extraction. Purchase record: the receipt photo. Brand Nordvik and model WM-7 come from the washer receipt photo only. Plates do not match WM-7. Date 06/02/2023 read as 2 June 2023 (Oregon store, order HH-230602, photo date).

## Step 2
### Delegation 4 to file-agent
> Find files whose names contain any of: warranty, guarantee, garantie, protection, plan, care, extended, registration, certificate, terms, conditions, Nordvik, WM-7, HomeHub. Search folders whose names contain Warranty, Receipts, Scans, Documents, Home or Appliances first, then all user files. File types: documents and images. Return full path, file name, size and modified date for each, up to 50. If there are no results, say zero matches.

Result: same 8 as run B.

### Delegation 5 to document-agent
> With intent locate_content and evidence mode focused, check these files: Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf, Scans/2024/Brightline_EPP_terms_scan.pdf. List only the files that are a warranty, guarantee, protection plan or warranty registration for Nordvik WM-7, or a plan bought with order HH-230602-1187. For each, quote the line that shows it. If none match, say zero matches.

Result: WM-7 card only ("Product: WM-7 Front Load Washing Machine").

### Delegation 6 to document-agent
> Answer from these files only: Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf. With intent period and answer mode table, return for each document: the provider, each coverage (full parts and labour, parts only, or named components such as motor, compressor or panel) with its term, how the start date is defined, and any printed start or end date. With intent condition, return the exclusions and the claim procedure (phone, email or web form exactly as written, required attachments). Also return any plan number, registration number and serial number written on it. Quote the page or section for each answer.

Result: as run B. 2 years parts and labor from original retail purchase, no extended components, no printed dates.

## Step 3
One document path, no reconcile. Bought 2 Jun 2023 + 2 years = ended 2 Jun 2025. Not covered.

## Step 4
### Delegation 7 to file-agent
> Find files whose names contain any of: manual, guide, instructions, handbook, quick start, WM-7, Nordvik. Search folders whose names contain Manuals, Documents, Downloads, Home or Appliances first, then all user files. File type: documents. Return full path, file name, size and modified date, up to 20. If there are no results, say zero matches.

Result: same 7 as run B. Sent for content check: WM-7_manual.pdf and Nordvik_ADW-48xx_UserManual.pdf.

### Delegation 8 to document-agent
> With intent locate_content, check these files: Home/Appliances/Washer/WM-7_manual.pdf, Manuals/Nordvik_ADW-48xx_UserManual.pdf. List only the files that are the user manual or guide for Nordvik WM-7, and quote the line that shows it. If none match, say zero matches.

Result: WM-7_manual.pdf only.

### Delegation 9 to document-agent
> Using only Home/Appliances/Washer/WM-7_manual.pdf, with intent locate_content and answer mode table, find what the manual says about error code E15. Return the matching rows of the error-code and troubleshooting tables (problem, cause, what to do) in the order printed, the safety warnings that apply to those steps, any steps that need a qualified technician, and any statement that user repairs affect the warranty. If there is no entry for the code or symptom, return the support or service contact printed in the manual. Give the page or section for each item.

Result: no entry for E15. The error-code table (section 4, page 6) lists F21, E03 and E10 only; the troubleshooting table (page 7) has no E15 row. Support contact printed on page 1: "Nordvik | Support: support@nordvik-support.example | 1-800-555-0188".

Parent: say "The manual for Nordvik WM-7 has no entry for E15", give only the universal safety advice, never use the dishwasher manual's E15 row. Label is Not covered, so (v6 fix 10) also give the manual's support contact with its page. Universal advice, lines that fit a washing machine (v6 fix 11): switch off at the wall; if leaking, close the water supply valve; burning, smoke or sparks. All three fit a washer, so all three are kept.

## Step 5
Not covered: no draft.

## Final answer, round 1
Composed with a "Next step:" line for the support contact. answer-format.md had no line for it, so the line was improvised. Delegations were correct. Logged as new defect N1 and fixed: answer-format.md now has a "Support:" line. The universal line on gas and burning was also shortened in round 1 instead of quoted; round 2 quotes it whole.

## Final answer, round 2 (after the answer-format fix; delegations reused unchanged)
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

Status: `completed`.

Delegations: 9 (photo-agent 2, file-agent 3, document-agent 4).

## Check against expected
Product and brand not changed by the dishwasher E15 photo: yes, now through the explicit typed-code rule instead of a literal reading. Washer receipt from photo, Not covered, ended 2 Jun 2025: yes. WM-7 manual has no E15 entry, said so, universal safety advice only, no dishwasher E15 steps: yes. Completed. PASS in both rounds; round 2 only changes the layout.

Change from v5: the answer now gives the manual's own support contact (fix 10). All three universal lines fit a washing machine (water supply, mains power), so none were dropped under fix 11.
