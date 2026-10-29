# Examples

All names, brands, stores and numbers are fictional. Today is 20 Nov 2026 in every example.

## 1. Covered by a protection plan the user forgot about

User: "My dishwasher is leaking and showing E15."

1. file-agent finds two dishwasher receipts: a 2019 receipt for a Nordvik ADW-3100 and a 2024 receipt for a Nordvik ADW-4820. photo-agent finds a photo of a rating plate reading ADW-4820, serial NV48-2203-1187. The plate settles which dishwasher it is, so the skill does not ask.
2. document-agent extracts the 2024 receipt: Brightline Electronics, 14 Mar 2024, serial NV48-2203-1187, plus a second line item, "3-Year Extended Protection Plan", plan PP-55120.
3. file-agent, searching by ADW-4820 and Nordvik, finds the warranty card and the plan terms. document-agent reports: 2 years parts and labour, 10 years on the motor; the plan starts when the manufacturer warranty ends and lasts 3 years; claims go to the plan's claim line, with the receipt and a rating-plate photo attached.
4. Verdict: "Bought 14 Mar 2024 + 2-year warranty = ended 14 Mar 2026. Protection plan PP-55120 runs 15 Mar 2026 to 14 Mar 2029, so covered by the plan."
5. The manual for the ADW-48xx series lists E15 as water in the base pan with leak protection triggered. Checklist: unplug and close the water tap; check the filter for blockage; check the door seal; do not tilt the appliance (technician only, per the manual).
6. Claim draft shown, status `waiting_approval`. User says yes, knowledge-agent saves "Warranty claim - Nordvik ADW-4820 - 2026-11-20", status `completed`.

## 2. Not covered, still helpful

User: "Washing machine shows F21. Is it still under warranty?"

The only receipt is a phone photo. photo-agent reads it: Nordvik WM-7, bought 2 Jun 2023. The warranty card gives 2 years. Verdict: "Not covered. Warranty ended 2 Jun 2025." The manual's F21 row (drain problem) gives the checklist anyway. No claim draft is offered. Status `completed`.

## 3. Partly covered with a serial mismatch

User: "The fridge stopped cooling."

Receipt 10 Jan 2022, HomeHub FR-560. Warranty: 2 years general, 5 years compressor. Verdict: "General warranty ended 10 Jan 2024. Compressor warranty runs to 10 Jan 2027, so partly covered if the technician confirms a compressor fault." The cross-check finds that the serial on the warranty registration differs by one character from the serial on the rating-plate photo. Both values and files are shown, the verdict is marked Unclear until the user reads the plate, and the claim draft uses the plate value with the mismatch noted.

## 4. No manual on the NAS

User: "The TV has sound but no picture."

Receipt 1 Dec 2025, Lumora 55Q8, warranty 1 year on the receipt. Verdict: covered until 1 Dec 2026. file-agent returns zero matches for a Lumora manual, so the skill says "There is no manual for Lumora 55Q8 on your NAS", gives no repair steps beyond switching off at the wall, and offers to save the claim draft. Status `waiting_approval`, then `completed` or `cancelled`.

## 5. Warranty sweep

User: "Which warranties run out in the next three months?"

Ending soon: 1 Dec 2026, Lumora 55Q8 TV, 1-year warranty; 10 Jan 2027, HomeHub FR-560 fridge, compressor warranty. Active later: Nordvik ADW-4820 dishwasher protection plan to 14 Mar 2029. Term unknown: a router with a manual but no receipt. The calendar is offered for saving. Status `waiting_approval`.

## 6. Nothing found

User: "Is my coffee machine under warranty?"

file-agent and photo-agent both return zero matches. The skill says "I could not find a receipt, warranty or manual for a coffee machine on your NAS" and asks whether the user knows the purchase date. Status `waiting_user`. It does not use the dishwasher's documents instead.
