# Examples

All names, brands, stores and numbers are fictional. Today is 20 Nov 2026 in every example.

## 1. Covered by a protection plan the user forgot about

User: "The dishwasher is doing this again" (a photo of the display was taken 10 minutes ago).

1. Step 0: photo-agent finds the new photo. Its text reads "E15" and "Nordvik". `waiting_user` is not needed, because the product and code are known.
2. Step 1: file-agent finds two dishwasher receipts, a 2019 Nordvik ADW-3100 and a 2024 Nordvik ADW-4820. photo-agent finds a 2024 rating-plate photo that reads ADW-4820, serial NV48-2203-1187. The plate matches exactly one receipt, so the skill does not ask. The 2019 purchase goes in Notes.
3. document-agent extracts the 2024 receipt: Brightline Electronics, 14 Mar 2024, $849.00, serial NV48-2203-1187, and a second line item, "3-Year Extended Protection Plan", plan EPP-3Y-90417733, $129.00.
4. Step 2: file-agent returns the Nordvik warranty card by name, plus `Scans/2024/Brightline_EPP_terms_scan.pdf`. document-agent confirms both by content and reports: 2 years parts and labour, 10 years on the motor; the plan begins when the manufacturer warranty ends, printed as 14 Mar 2026 to 14 Mar 2029; claims go to protect@brightline-services.example with the plan number, receipt and serial.
5. Step 3: reconcile finds no differences. Verdict: "Covered. Bought 14 Mar 2024 + 2-year warranty = ended 14 Mar 2026. Protection plan EPP-3Y-90417733 runs to 14 Mar 2029." Note: a worn door gasket is excluded; an internal leak is covered.
6. Step 4: file-agent returns the manual twice, from Manuals and Downloads. The sha256sum values match, so one copy is used and the duplicate is noted. The E15 row: water in the base pan. Turn off the water, unplug, check the door gasket and hose connections. Tilt to drain only if instructed. Do not open the base. Call service if E15 returns. Safety leads because it is a leak on mains power.
7. Step 5: the draft is shown with "Already tried: none confirmed", and the status is `waiting_approval`. The user says "I checked the hoses, yes save it". knowledge-agent saves the note and returns its path. Status `completed`.

## 2. Not covered, still helpful

User: "Washing machine shows F21. Is it still under warranty?"

The only receipt is a phone photo. photo-agent reads Nordvik WM-7 and the date 06/02/2023. The US store format and the photo's date taken (2 Jun 2023) settle it as 2 June. The warranty card in `Home/Appliances/Washer/` gives 2 years. Verdict: "Not covered. Warranty ended 2 Jun 2025." The manual's F21 row (drain fault) still gives the checklist: power off, clean the drain pump filter, check the drain hose. No claim draft. Status `completed`.

## 3. Serial mismatch makes it Unclear

User: "The fridge stopped cooling."

Receipt 10 Jan 2022, HomeHub FR-560, serial HH56-2201-30847. The registration gives 1 year general and 5 years on the compressor and sealed system. The rating-plate photo reads HH56-2201-30647. Verdict: "Unclear. General warranty ended 10 Jan 2023. It would be partly covered (compressor and sealed system, to 10 Jan 2027) once the serial is confirmed: the registration says 30847, the plate photo says 30647." The manual's not-cooling steps follow. The claim draft uses the plate value and marks it to be checked. The claim procedure says the serial must match the registration.

## 4. No manual on the NAS

User: "The TV has sound but no picture."

Receipt 1 Dec 2025, Lumora 55Q8. The warranty card gives 1 year on the panel, board and power supply. Verdict: "Covered until 1 Dec 2026, 11 days left, if the technician confirms a panel, board or power supply fault." file-agent finds no Lumora manual, so the skill says "There is no manual for Lumora 55Q8 on your NAS" and gives only the universal safety advice. The draft goes to care@lumora-tv.example. The user says no, so the status is `completed` with "not saved".

## 5. Warranty sweep

User: "Which warranties run out in the next three months?"

The window is 20 Nov 2026 to 20 Feb 2027 (three calendar months). Ending soon, value losing cover $2,527: 1 Dec 2026 Lumora 55Q8 TV; 18 Dec 2026 Lumora S2 soundbar; 10 Jan 2027 HomeHub FR-560 compressor. Active later: Nordvik ADW-4820 protection plan to 14 Mar 2029, motor to 14 Mar 2034. Unknown: Zentro AX3000 router, no receipt found. Closing line: 2 older appliances are out of warranty (the washing machine, from a receipt photo, and the 2019 dishwasher). The calendar is offered for saving. Status `waiting_approval`.

## 6. Nothing found

User: "Is my coffee machine under warranty?"

file-agent and photo-agent return zero matches for a coffee machine. The skill says "I couldn't find a receipt for your coffee machine on the NAS. Do you know roughly when you bought it?" and stops at `waiting_user`. It does not use the dishwasher's documents instead.
