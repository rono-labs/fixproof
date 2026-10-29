# fixproof test library

A fictional family NAS for testing the fixproof skill. Every brand, store, person and address is invented (owner "Alex Rivera", 48 Larkspur Lane). Scenario date is 2026-11-20. Regenerate with `.venv/bin/python project/testdata/make_library.py`; output goes to `project/testdata/home-library/` and is byte-identical on each run. About 27 files, under 1 MB. Upload the `home-library` folder to the NAS as is.

## What each file tests

Dishwasher Nordvik ADW-4820 (bought 2024-03-14):
- `Documents/Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf`: receipt, serial NV48-2203-1187, order BL-2024-0314-55871, plan line EPP-3Y-90417733.
- `Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf`: 2 years parts and labor, 10 years motor, exclusions, claim contact. Needs receipt and serial photo.
- `Scans/2024/Brightline_EPP_terms_scan.pdf`: separate protection plan terms, 2026-03-14 to 2029-03-14.
- `Manuals/Nordvik_ADW-48xx_UserManual.pdf`: 12 pages, error codes (E15 leak, E24 drain, E09 heater), troubleshooting, filter cleaning, void-warranty note.
- `Photos/Phone/2024-03/IMG_20240316_190455.jpg`: serial plate photo, matches the receipt.
- `Downloads/ADW-48xx_manual (1).pdf`: exact duplicate of the manual (dedupe test).

Old dishwasher: `Documents/Receipts/2019/receipt_dishwasher_old.pdf`, ADW-3100, 2019-08-22. Tests model disambiguation. It must not be used for scenario A.

Washing machine Nordvik WM-7 (bought 2023-06-02): receipt exists only as the phone photo `Photos/Phone/2023-06/IMG_20230602_181404.jpg` (tests image reading). Warranty card and manual (F21 drain fault) are in `Home/Appliances/Washer/`.

TV Lumora 55Q8 (bought 2025-12-01): receipt `Documents/Receipts/2025/Brightline_order_TV_Lumora.pdf`, warranty `Scans/Lumora_TV_warranty.pdf`. No manual anywhere.

Soundbar Lumora S2 (bought 2025-12-18): receipt only, 1 year, so it expires 2026-12-18. Extra sweep item.

Fridge HomeHub FR-560 (bought 2022-01-10): receipt in `Documents/Receipts/2022/`, warranty and registration plus manual (not cooling steps) in `Home/Appliances/Fridge/`. Registered serial is HH56-2201-30847. The serial plate photo `Photos/Phone/2022-01/IMG_20220115_101233.jpg` reads HH56-2201-30647 (one character differs).

Router Zentro AX3000: `Manuals/Zentro_AX3000_Router_Manual.pdf` only. No receipt, so coverage is unknown and the skill should say so.

Noise: school newsletter, utility bill, recipes, vacation and wallpaper photos, other phone photos.

## Expected answers

A. "Dishwasher leaking, E15". Manufacturer warranty ended 2026-03-14. The extended plan EPP-3Y-90417733 is active until 2029-03-14, so the repair is covered by the plan. Give the manual's E15 checklist (turn off water, unplug, check gasket and hose clamps, do not open the base, service if it returns) and a claim draft to protect@brightline-services.example with receipt, plan number and serial. Warn that opening the base voids coverage. Use the 2024 receipt, not the 2019 one.

B. "Washing machine F21, still under warranty?" Not covered. The 2-year warranty ended 2025-06-02. There is no extended plan. Still give the F21 steps (clean the pump filter, check the drain hose). Mention the receipt came from a photo.

C. "Fridge not cooling". Partly covered. General warranty ended 2023-01-10, but compressor and sealed system coverage runs to 2027-01-10. Give the not-cooling steps; coverage applies only if the fault is in the sealed system. Flag the serial mismatch (30847 vs 30647) and tell the user to re-photograph the plate or fix the registration before filing.

D. "TV no picture". Covered by the 1-year warranty until 2026-12-01, 11 days left, so file soon. Say no manual was found on the NAS, offer generic checks, and point to care@lumora-tv.example.

E. Sweep "what warranties expire soon?" (window 2026-11-20 to 2027-02-18): TV 2026-12-01, soundbar 2026-12-18, fridge compressor 2027-01-10. Not listed: dishwasher plan (2029), dishwasher motor (2034), washer and old dishwasher (expired). Router has no date.
