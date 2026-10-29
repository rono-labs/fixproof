# Dry run A: "The dishwasher is doing this again."

Today = 2026-11-20 08:40. Library = `project/testdata/home-library/`. Expert results come from real files: file-agent from a name and folder-name match, photo-agent from viewing the images, document-agent from `pdftotext`. All files have modified date 2026-10-29 (upload date).

Intake: mode fault. Product dishwasher. Symptom: only "doing this again". Brand, model, code unknown before Step 0.

## Step 0

delegate --target photo-agent --instruction 'Search photos taken in the last 48 hours, up to 2026-11-20 08:40, for pictures of an appliance control panel or display showing an error code, or of an appliance rating plate or serial label. For each photo found, run text recognition and return the photo path, the time taken and the recognised text. If there are no results, say zero matches.'

Result (cutoff 2026-11-18 08:40, EXIF date taken): 1 photo. `Photos/Phone/2026-11/IMG_20261120_083012.jpg`, taken 2026-11-20 08:30:12. Text read: "NORDVIK", "E15" (large red display digits), "POWER", "CYCLE", "DELAY", "START". No model, no serial.

Parent: the rule says "Text that does not name an appliance counts as no match". The text names a brand and a code but no appliance type. Judgement call (defect D3): used it, because the user's product is a dishwasher and nothing contradicts it. Taken: code E15, brand Nordvik. Evidence list: the photo.

## Step 1

delegate --target file-agent --instruction 'Find files whose names contain any of: receipt, invoice, order, purchase, quittung, Nordvik, dishwasher. Search folders whose names contain Receipts, Invoices, Purchases, Orders, Documents, Scans or Downloads first, then all user files. File types: documents and images. Return full path, file name, type, size and modified date for each, up to 50. If there are no results, say zero matches.'

(`{model}` has no real value, so it is left out.) Result, 8 PDFs: Receipts/2019/receipt_dishwasher_old.pdf; Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf; Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf; Receipts/2025/Brightline_order_TV_Lumora.pdf; Receipts/2025/Brightline_soundbar_2025-12-18.pdf; Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf; Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf; Manuals/Nordvik_ADW-48xx_UserManual.pdf.

delegate --target photo-agent --instruction 'Search the photo library for photos of a paper receipt or till slip that mention dishwasher or Nordvik. For each photo found, run text recognition and return the photo path, the date taken and the recognised text. If there are no results, say zero matches.'

Result: 1 photo. `Photos/Phone/2023-06/IMG_20230602_181404.jpg`, taken 2023-06-02. Text: HOMEHUB APPLIANCES, Date 06/02/2023, Order HH-230602-1187, Nordvik WM-7 Front Load Washer, SN NV7-2305-60912, $899.00, Delivery $59.00, TOTAL $958.00. (The 2024 rating plate photo is not returned: it is not a receipt. See D1.)

delegate --target document-agent --instruction 'Extract purchase details with the receipt schema from these files: Documents/Receipts/2019/receipt_dishwasher_old.pdf, Documents/Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf, Documents/Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf, Documents/Receipts/2025/Brightline_order_TV_Lumora.pdf, Documents/Receipts/2025/Brightline_soundbar_2025-12-18.pdf. If a file returns no data with the receipt schema, try the invoice schema. For each file return store, order number, purchase date exactly as printed, product description, brand, model number, serial number if printed, price, and every other line item, especially any protection plan, extended warranty or care plan with its plan number and term. Report any file you could not read.'

Result: all 5 read.
- 2019: Brightline Electronics, BL-2019-0822-20318, 2019-08-22, Nordvik ADW-3100 Dishwasher, serial NV31-1905-0342, $529.00; haul-away $25.00; "Manufacturer warranty: 1 year parts and labor. No extended plan purchased."
- 2022: HomeHub FR-560 refrigerator (other product).
- 2024: Brightline Electronics, BL-2024-0314-55871, 2024-03-14, Nordvik ADW-4820 Dishwasher, serial NV48-2203-1187, $849.00; "3-Year Extended Protection Plan, Plan no. EPP-3Y-90417733. Covers ADW-4820 after the manufacturer warranty ends. Terms provided separately." $129.00; installation kit $24.99.
- 2025 TV order and soundbar: other products.

Parent: the washer receipt photo and the three other receipts name other products, so they are no match. Two dishwasher purchases remain (2019 ADW-3100, 2024 ADW-4820). No user model, no plate photo in hand. Rule: list both, ask which, `waiting_user`.

Parent to user (status `waiting_user`): "I found two Nordvik dishwasher receipts: 22 Aug 2019 (ADW-3100) and 14 Mar 2024 (ADW-4820). Which one is it? The newest is my guess."
User (invented, the script gives no reply here): "The newer one."

Delegations so far: 4.

## Step 2

delegate --target file-agent --instruction 'Find files whose names contain any of: warranty, guarantee, garantie, protection, plan, care, extended, registration, certificate, Nordvik, ADW-4820, ADW-48xx. Search folders whose names contain Warranty, Receipts, Scans, Documents, Home or Appliances first, then all user files. File types: documents and images. Return full path, file name, size and modified date for each, up to 50. If there are no results, say zero matches.'

Result, 6 PDFs: Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf; Downloads/ADW-48xx_manual (1).pdf; Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf; Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf; Manuals/Nordvik_ADW-48xx_UserManual.pdf; Scans/Lumora_TV_warranty.pdf.

`Scans/2024/Brightline_EPP_terms_scan.pdf` is NOT returned: its name has none of the terms and none of its folder names match (D2).

delegate --target document-agent --instruction 'With intent locate_content and evidence mode focused, check these files: Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf, Downloads/ADW-48xx_manual (1).pdf, Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf, Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf, Manuals/Nordvik_ADW-48xx_UserManual.pdf, Scans/Lumora_TV_warranty.pdf. List only the files that are a warranty, guarantee, protection plan or warranty registration for Nordvik ADW-4820 or the series ADW-48xx, or a plan bought with order BL-2024-0314-55871. For each, quote the line that shows it. If none match, say zero matches.'

Result: 1 file. Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf: "LIMITED WARRANTY CARD / Product: ADW-4820 Dishwasher". (The manuals are manuals, the others are other products.)

delegate --target document-agent --instruction 'Answer from these files only: Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf. With intent period and answer mode table, return for each document: the provider, each coverage (full parts and labour, parts only, or named components such as motor, compressor or panel) with its term, how the start date is defined, and any printed start or end date. With intent condition, return the exclusions and the claim procedure (phone, email or web form exactly as written, required attachments). Also return any plan number, registration number and serial number written on it. Quote the page or section for each answer.'

Result: Nordvik. Parts and labor 2 years; drive motor 10 years ("parts only after year 2"). Start: "date of original retail purchase", dated receipt required. No printed dates. Exclusions: "misuse, improper installation, power surges, frozen pipes, commercial use, cosmetic damage, consumables (filters, racks, gaskets), and any repair attempted by anyone other than a Nordvik authorized service provider"; owner repairs beyond the manual void the warranty. Claim: "Email claims@nordvik-support.example or call 1-800-555-0188 (Mon-Fri 8:00-18:00 Pacific)", attach dated receipt and a clear photo of the serial plate. No plan number, no serial.

Delegations so far: 7.

## Step 3

delegate --target document-agent --instruction 'Reconcile these files and report every difference in brand, model number, serial number, purchase date, plan start or end date, or owner name: Documents/Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf, Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf. For each difference give both values and the file each came from. If they all agree, say no differences found.'

Result: no differences found (brand Nordvik and model ADW-4820 agree; the card prints no serial, date or owner).

No rating-plate photo of this product is in hand (D1), so no plate comparison.

Parent arithmetic: bought 2024-03-14 + 2 years = ended 2026-03-14. Motor 10 years = 2034-03-14, active, but E15 (water in the base pan) does not point to the motor. The receipt shows a 3-year protection plan "after the manufacturer warranty ends", so by rule 4 it would run 2026-03-14 to 2029-03-14. Its terms document was not found, so what it covers, its exclusions and its claim contact are unknown. No rule fits (D4). Label chosen: Unclear, with what would make it definite.

Delegations so far: 8.

## Step 4

delegate --target file-agent --instruction 'Find files whose names contain any of: manual, guide, instructions, handbook, quick start, ADW-4820, ADW-48xx, Nordvik. Search folders whose names contain Manuals, Documents, Downloads, Home or Appliances first, then all user files. File type: documents. Return full path, file name, size and modified date, up to 20. If there are no results, say zero matches.'

Result, 7: Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf (2960 B); Downloads/ADW-48xx_manual (1).pdf (17516 B); Home/Appliances/Fridge/FR-560_owner_manual.pdf (9127 B); Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf (2681 B); Home/Appliances/Washer/WM-7_manual.pdf (9774 B); Manuals/Nordvik_ADW-48xx_UserManual.pdf (17516 B); Manuals/Zentro_AX3000_Router_Manual.pdf (6029 B).

Duplicate rule: "share a name stem and size". The two ADW manuals have the same size but different names (D5). Parent asked for the checksum anyway.

delegate --target file-agent --instruction 'Return the sha256sum of these two files: Downloads/ADW-48xx_manual (1).pdf, Manuals/Nordvik_ADW-48xx_UserManual.pdf.'

Result: both 2858e0506bfc17fb3076623c5b917c28c11cb91b4650cc02af821eb6bfde3b7d. Identical. Keep Manuals/Nordvik_ADW-48xx_UserManual.pdf, note the duplicate in Downloads.

delegate --target document-agent --instruction 'With intent locate_content and evidence mode focused, check these files: Manuals/Nordvik_ADW-48xx_UserManual.pdf, Home/Appliances/Fridge/FR-560_owner_manual.pdf, Home/Appliances/Washer/WM-7_manual.pdf, Manuals/Zentro_AX3000_Router_Manual.pdf. List only the files that are the user manual for Nordvik ADW-4820 or the series ADW-48xx. For each, quote the line that shows it. If none match, say zero matches.'

Result: Manuals/Nordvik_ADW-48xx_UserManual.pdf: "Nordvik Dishwasher / Model series ADW-48xx / User Manual and Care Guide".

delegate --target document-agent --instruction 'Using only Manuals/Nordvik_ADW-48xx_UserManual.pdf, with intent locate_content and answer mode table, find what the manual says about error code E15 and about the symptom "blinking error E15, doing this again". Return the matching rows of the error-code and troubleshooting tables (problem, cause, what to do) in the order printed, the safety warnings that apply to those steps, any steps that need a qualified technician, and any statement that user repairs affect the warranty. Give the page or section for each item.'

(The user's own words "doing this again" are not searchable, so the code was added to the symptom; D6.)

Result:
- Error codes, p. 9: E15 "Water detected in the base pan. Leak protection has stopped the unit." Action: "Turn off water, unplug, tilt unit slightly to drain base pan only if instructed, check door gasket and hose connections. If E15 returns, call service. Do not open the base."
- Troubleshooting, p. 10: "Puddle under unit, E15 shown": cause "Water in base pan: loose hose, door gasket, or internal leak"; solution "Stop the unit, check hose clamps and gasket. Service call if the leak persists."
- Safety, p. 3: "Do not operate a dishwasher that is leaking. Turn off the water supply and unplug the unit."
- Technician: service call if E15 returns or the leak persists; do not open the base.
- Warranty: p. 3 "any user repair beyond the steps listed in this manual (for example opening the base, replacing internal parts, or bypassing sensors) will void the manufacturer warranty and any extended protection plan." p. 10 similar.

Exclusions vs causes: causes are loose hose, door gasket, internal leak; the card excludes gaskets (consumables). Only some are excluded, so keep the label and add a Note.

Delegations so far: 12.

## Step 5

Draft (label Unclear, so a draft is made). Plan claim contact not found, so the contact is left out and said to be missing.

    To: (not found. The Nordvik warranty card gives claims@nordvik-support.example for the manufacturer warranty, which ended 2026-03-14. The plan's own claim contact is in terms I could not find.)
    Subject: Warranty claim, Nordvik ADW-4820, serial NV48-2203-1187
    Product: Nordvik ADW-4820, serial NV48-2203-1187
    Purchased: 2024-03-14 at Brightline Electronics, order BL-2024-0314-55871
    Coverage: Nordvik Limited Warranty (ended 2026-03-14); 3-Year Extended Protection Plan EPP-3Y-90417733, listed on the receipt, runs to 2029-03-14 if its terms apply (terms not found)
    Fault: dishwasher shows a blinking error, water in base pan, error code E15
    Already tried: none confirmed
    Attachments: Documents/Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf, Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf, Photos/Phone/2026-11/IMG_20261120_083012.jpg (display photo). Rating plate photo: none found, the card asks for one.
    Contact: (blank)

Parent to user: shows the draft and the answer below, asks "Which of the steps above have you already tried? Then say yes to save this draft to your NAS, or no." Status `waiting_approval`.

User: "I checked the hoses, yes save it"

"Already tried" becomes "checked the hoses (user confirmed)".

delegate --target knowledge-agent --instruction 'Save this text as a new note with filename hint "Warranty claim Nordvik ADW-4820 2026-11-20 08:40". Text: To: (not found; see note) / Subject: Warranty claim, Nordvik ADW-4820, serial NV48-2203-1187 / Product: Nordvik ADW-4820, serial NV48-2203-1187 / Purchased: 2024-03-14 at Brightline Electronics, order BL-2024-0314-55871 / Coverage: Nordvik Limited Warranty (ended 2026-03-14); 3-Year Extended Protection Plan EPP-3Y-90417733 on the receipt, to 2029-03-14 if its terms apply / Fault: dishwasher shows a blinking error, water in base pan, error code E15 / Already tried: checked the hoses (user confirmed) / Attachments: Documents/Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf, Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf, Photos/Phone/2026-11/IMG_20261120_083012.jpg / Contact: (blank)'

Result (save succeeds): `/Notes/Warranty claim Nordvik ADW-4820 2026-11-20 08:40.md`. Status `completed`.

Total delegations: 13 (Step 0: 1, Step 1: 3, Step 2: 3, Step 3: 1, Step 4: 4, Step 5: 1). Questions to the user: 1 extra (which dishwasher).

## Final answer

    Safety first: Do not operate a dishwasher that is leaking. Turn off the water supply and unplug the unit. (ADW-48xx manual, p. 3)
    Product: Nordvik ADW-4820 (dishwasher), bought 2024-03-14 at Brightline Electronics
    Coverage: Unclear. Bought 14 Mar 2024 + 2-year warranty = ended 14 Mar 2026. The receipt lists a 3-Year Extended Protection Plan EPP-3Y-90417733 that would run to 14 Mar 2029, so it would be covered once the plan's terms are confirmed, but I found no terms document for it, so I cannot tell what it covers or whom to claim from.
    Try this (manual p. 9 and p. 10):
      1. Turn off the water and unplug the unit.
      2. Check the door gasket and the hose connections and clamps. Tilt the unit slightly to drain the base pan only if instructed.
      Technician only: do not open the base. If E15 returns or the leak persists, call service. Opening the base or other repairs beyond these steps void the warranty and any extended protection plan.
    Claim: draft ready (contact for the plan not found). Saved to /Notes/Warranty claim Nordvik ADW-4820 2026-11-20 08:40.md
    Evidence:
      - Photos/Phone/2026-11/IMG_20261120_083012.jpg: E15 and the Nordvik name on the display, taken 2026-11-20 08:30
      - Documents/Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf: purchase date, model, serial NV48-2203-1187, plan line EPP-3Y-90417733
      - Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf: 2 years parts and labour, 10 years motor, exclusions, claim contact
      - Manuals/Nordvik_ADW-48xx_UserManual.pdf: troubleshooting for E15
    Notes: A worn door gasket is excluded by the card; an internal leak is not. The 2019 purchase (ADW-3100, receipt_dishwasher_old.pdf) was not used. The same manual exists in Downloads/ADW-48xx_manual (1).pdf (identical checksum). The plan terms were not found, so the plan's scope and claim contact are unconfirmed. No rating plate photo was found; the card requires one for a claim.
