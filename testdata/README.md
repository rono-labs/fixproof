# fixproof test library

A fictional family NAS for testing the fixproof skill. Every brand, store, person and address is invented (owner "Alex Rivera", 48 Larkspur Lane). Scenario date is 2026-11-20. Regenerate with `.venv/bin/python project/testdata/make_library.py`; output goes to `project/testdata/home-library/` and is byte-identical on each run. About 28 files, under 1 MB. Upload the `home-library` folder to the NAS as is.

## What each file tests

Dishwasher Nordvik ADW-4820 (bought 2024-03-14):
- `Documents/Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf`: receipt, serial NV48-2203-1187, order BL-2024-0314-55871, plan line EPP-3Y-90417733.
- `Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf`: 2 years parts and labor, 10 years motor, exclusions, claim contact. Needs receipt and serial photo.
- `Scans/2024/Brightline_EPP_terms_scan.pdf`: separate protection plan terms, 2026-03-14 to 2029-03-14.
- `Manuals/Nordvik_ADW-48xx_UserManual.pdf`: 12 pages, error codes (E15 leak, E24 drain, E09 heater), troubleshooting, filter cleaning, void-warranty note.
- `Photos/Phone/2024-03/IMG_20240316_190455.jpg`: serial plate photo, matches the receipt.
- `Downloads/ADW-48xx_manual (1).pdf`: exact duplicate of the manual (dedupe test).
- `Photos/Phone/2026-11/IMG_20261120_083012.jpg`: phone photo of the control panel taken 2026-11-20 08:30, showing a blinking E15 on a small display and the Nordvik name. No model number on it, so the rating plate photo settles the model. All phone photos carry EXIF DateTimeOriginal matching the date in the file name.

Old dishwasher: `Documents/Receipts/2019/receipt_dishwasher_old.pdf`, ADW-3100, 2019-08-22. Tests model disambiguation. It must not be used for scenario A.

Washing machine Nordvik WM-7 (bought 2023-06-02): receipt exists only as the phone photo `Photos/Phone/2023-06/IMG_20230602_181404.jpg` (tests image reading). Warranty card and manual (F21 drain fault) are in `Home/Appliances/Washer/`.

TV Lumora 55Q8 (bought 2025-12-01): receipt `Documents/Receipts/2025/Brightline_order_TV_Lumora.pdf`, warranty `Scans/Lumora_TV_warranty.pdf`. No manual anywhere.

Soundbar Lumora S2 (bought 2025-12-18): receipt only, 1 year, so it expires 2026-12-18. Extra sweep item.

Fridge HomeHub FR-560 (bought 2022-01-10): receipt in `Documents/Receipts/2022/`, warranty and registration plus manual (not cooling steps) in `Home/Appliances/Fridge/`. Registered serial is HH56-2201-30847. The serial plate photo `Photos/Phone/2022-01/IMG_20220115_101233.jpg` reads HH56-2201-30647 (one character differs).

Router Zentro AX3000: `Manuals/Zentro_AX3000_Router_Manual.pdf` only. No receipt, so coverage is unknown and the skill should say so.

Noise: school newsletter, utility bill, recipes, vacation and wallpaper photos, other phone photos.

## Expected answers

These match `project/fixproof/references/examples.md`. Today is 2026-11-20.

A. "The dishwasher is doing this again." The skill starts from the new photo, which reads E15 and Nordvik. The rating plate photo (ADW-4820, serial NV48-2203-1187) settles the model, so it does not ask. Use the 2024 receipt, not the 2019 one (noted in Notes). Verdict: Covered. The manufacturer warranty ended 2026-03-14, and protection plan EPP-3Y-90417733 runs to 2029-03-14. Note that a worn door gasket is excluded and an internal leak is covered. Give the manual's E15 steps with safety first (turn off water, unplug, check gasket and hose connections, do not open the base, service if it returns). Note that the manual exists twice (Manuals and Downloads, same checksum) and one copy was used. The claim draft goes to protect@brightline-services.example with the plan number, receipt and serial, and shows "Already tried: none confirmed". After the user says "I checked the hoses, yes save it", the note is saved and the status is completed.

B. "Washing machine shows F21. Is it still under warranty?" Not covered. The only receipt is a phone photo (WM-7, 06/02/2023); the US store format and the date taken settle it as 2 June 2023. The 2-year warranty ended 2025-06-02. Still give the F21 drain steps (power off, clean the drain pump filter, check the drain hose). No claim draft.

C. "The fridge stopped cooling." Unclear. The general warranty ended 2023-01-10. It would be partly covered (compressor and sealed system, to 2027-01-10) once the serial is confirmed: the registration says HH56-2201-30847 and the plate photo says HH56-2201-30647. Give the not-cooling steps. The claim draft uses the plate value and marks it to be checked, because the claim procedure requires the serial to match the registration.

D. "The TV has sound but no picture." Covered until 2026-12-01 (11 days left) if a technician confirms a panel, board or power supply fault. There is no manual for Lumora 55Q8 on the NAS, so give only universal safety advice. The draft goes to care@lumora-tv.example. If the user declines to save, the status is completed with "not saved".

E. "Which warranties run out in the next three months?" The window is three calendar months, 2026-11-20 to 2027-02-20. Ending soon, value losing cover $2,527: 2026-12-01 Lumora 55Q8 TV, 2026-12-18 Lumora S2 soundbar, 2027-01-10 HomeHub FR-560 compressor. Active later: Nordvik ADW-4820 protection plan to 2029-03-14, motor to 2034-03-14. Unknown: Zentro AX3000 router, no receipt found. Closing line: 2 older appliances are out of warranty (the washing machine, from a receipt photo, and the 2019 dishwasher). The calendar is offered for saving and the status is waiting_approval.

F. "Is my coffee machine under warranty?" Nothing found. The skill says it could not find a receipt for the coffee machine on the NAS and asks roughly when it was bought, then stops at waiting_user. It does not use the dishwasher's documents instead.
