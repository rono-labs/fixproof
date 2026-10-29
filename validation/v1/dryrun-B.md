# Dry run B: washing machine F21, "Is it still under warranty?"

Today = 2026-11-20. Paths are relative to `project/testdata/home-library/` (written `home-library/`). Expert results are emulated from `find`, `grep`, `pdftotext` and by viewing the photos.

## Intake
Mode: fault. Product: washing machine. Symptom: "shows F21", code F21. Brand and model not given, so those slots are left out.

## Step 1. Purchase record

delegate --target file-agent --instruction 'Find documents that look like receipts, invoices or order confirmations for a washing machine. Search folders whose names contain Receipts, Invoices, Purchases, Orders, Documents, Scans or Downloads first, then all of the user files. Include PDF, image and office document types. For each match return the full path, file name, type and modified date, up to 30 matches. If there are no results, say zero matches.'

file-agent result: zero matches. No file name contains "washer" or "washing" in those folders, no receipt PDF mentions a washing machine, and the receipt photo is named IMG_20230602_181404.jpg, which a name search cannot link to a washer (file-agent find/stat does not read image text).

delegate --target photo-agent --instruction 'Search the photo library for photos of a paper receipt or of an appliance rating plate or serial label for a washing machine. For each photo found, run text recognition and return the photo path, the date taken and the recognised text. If there are no results, say zero matches.'

photo-agent result (same three paper/plate photos as in run A; text read from the images):
- Photos/Phone/2023-06/IMG_20230602_181404.jpg, 2023-06-02: "HOMEHUB APPLIANCES, 77 Harbor Road, Port Alder OR / Date: 06/02/2023  Order HH-230602-1187 / Cust: Alex Rivera / Nordvik WM-7 Front Load Washer, SN NV7-2305-60912 $899.00 / Delivery $59.00 / TOTAL $958.00 / Paid: CARD ****4417 / Warranty: see manufacturer card"
- Photos/Phone/2024-03/IMG_20240316_190455.jpg: dishwasher plate, Nordvik ADW-4820, NV48-2203-1187 (other product, ignored)
- Photos/Phone/2022-01/IMG_20220115_101233.jpg: fridge plate, HomeHub FR-560, HH56-2201-30647 (other product, ignored)

Parent: the file-agent returned no receipt paths, so the document-agent extract step has nothing to read ("{receipt paths from file-agent}" is empty). SKILL.md says to merge the photo-agent's recognised text, so the OCR text is used as the purchase record and no extract delegation is sent (defect D4: the step never says whether a photo path may go to document-agent).
Date reading: the printed date "06/02/2023" could be 2 June or 6 February. The order number HH-230602-1187 and the photo date taken (2023-06-02) both point to 2 June 2023, and the store is in Oregon. coverage-rules.md has no rule for ambiguous date formats (defect D5). Used: 2023-06-02. Even the other reading (6 Feb 2023 + 2 years = 6 Feb 2025) is in the past, so the verdict would not change.

## Step 2. Warranty documents

delegate --target file-agent --instruction 'Find documents that mention WM-7 or Nordvik washing machine together with any of these words: warranty, guarantee, protection plan, extended, care plan, certificate, registration. Also return any file in the same folder as home-library/Photos/Phone/2023-06/IMG_20230602_181404.jpg with a modified date within 30 days of 2023-06-02. Return full path, file name and modified date for each, up to 30. If there are no results, say zero matches.'

file-agent result:
- home-library/Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf (WM-7, warranty), modified 2026-10-29
- home-library/Home/Appliances/Washer/WM-7_manual.pdf (WM-7, "Service and warranty" section), modified 2026-10-29
Same-folder clause: nothing, because every file in this library carries the upload date 2026-10-29. On a NAS that kept original dates it would return the unrelated IMG_20230610_201145.jpg, which is harmless.

delegate --target document-agent --instruction 'Answer from these files only: home-library/Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf. For each document return: who provides it, what it covers (full parts and labour, parts only, or named components such as motor or compressor) with the term for each, whether the term starts at purchase, delivery or when another warranty ends, the exclusions, the claim procedure (phone, email or web form exactly as written, and required attachments), and any plan or registration number with any serial number written on it. Quote the page or section for each answer.'

document-agent result (page 1): provider Nordvik; parts and labor 2 years, "Defective parts and labor from the original purchase date"; starts at original retail purchase, dated receipt required; "This warranty has no extended components." Exclusions: misuse, installation faults, hoses, cosmetic damage, repairs by unauthorized persons, commercial use. Claim: claims@nordvik-support.example or 1-800-555-0188 (Mon-Fri 8:00-18:00 Pacific), with the dated receipt and a photo of the serial plate. No plan, registration or serial number printed.

## Step 3. Verdict
2023-06-02 + 2 years = ended 2025-06-02. No extended component, no protection plan found (receipt photo has no plan line). Today 2026-11-20 is after the end date. Verdict: Not covered, ended 2 Jun 2025.
Cross-check delegation not sent: it is required only when receipt, warranty documents and a rating-plate photo for this product all exist, and no washer plate photo exists. The verdict could not change either way.

## Step 4. Manual

delegate --target file-agent --instruction 'Find user manuals, installation guides or quick start guides for Nordvik WM-7. Search folders whose names contain Manuals, Documents, Downloads or Home first, then all user files. Return full path, file name and modified date, up to 10. If there are no results, say zero matches.'

file-agent result: 1 match, home-library/Home/Appliances/Washer/WM-7_manual.pdf, modified 2026-10-29. ({series} left out: no upstream value, and the series equals the model here.)

delegate --target document-agent --instruction 'Using only home-library/Home/Appliances/Washer/WM-7_manual.pdf, find what the manual says about error code F21 and about the symptom "shows F21". Return the matching rows of the troubleshooting or error-code table (problem, cause, what to do) in the order printed, the safety warnings that apply to those steps, any steps the manual says need a qualified technician, and any statement that user repairs affect the warranty. Give the page or section for each item.'

document-agent result:
- Section 4 Error codes, p. 6: F21 "Drain fault: water not draining." Action: "Pause, power off, clean the drain pump filter behind the lower right panel (have a towel ready), check the drain hose for kinks, restart."
- Section 5 Troubleshooting, p. 7: "Water left in drum, F21", cause "Blocked pump filter or hose", solution "Clean pump filter, check hose".
- Safety, section 1, p. 3: "Disconnect power before any cleaning near electrical parts." and "Do not open the door while the drum is turning."
- Technician steps: none stated. Warranty effect of user repairs: none stated in the manual (section 6 only says "See the warranty card supplied. Keep your receipt.").

## Step 5. Claim draft
Not offered: verdict is Not covered (SKILL.md Step 5 applies only to covered, partly covered or unclear).

## Step 6. Final answer

    Product: Nordvik WM-7 (washing machine), bought 2023-06-02 at HomeHub Appliances
    Coverage: Not covered. Bought 2 Jun 2023 + 2-year parts and labor warranty = ended 2 Jun 2025. The card says it has no extended components, and no protection plan was found.
    Safety first: "Disconnect power before any cleaning near electrical parts." (manual section 1, p. 3)
    Try this (manual section 4, p. 6 and section 5, p. 7):
      1. Pause the machine and power it off.
      2. Clean the drain pump filter behind the lower right panel (have a towel ready).
      3. Check the drain hose for kinks.
      4. Restart.
      Technician only: none stated in the manual.
    Evidence:
      - home-library/Photos/Phone/2023-06/IMG_20230602_181404.jpg: receipt, HomeHub Appliances, order HH-230602-1187, Nordvik WM-7, serial NV7-2305-60912, date read as 06/02/2023
      - home-library/Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf: 2 years parts and labor from purchase, no extended components, exclusions, claim contact
      - home-library/Home/Appliances/Washer/WM-7_manual.pdf: F21 steps, p. 6 and p. 7
    Notes: The only receipt is a phone photo; its date reads 06/02/2023 and I took it as 2 June 2023 because the order number and the photo date agree. Either reading puts the warranty end in the past. No claim draft is offered because nothing is covered.

Status token: `completed`.
