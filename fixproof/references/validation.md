# Validation

This was a tabletop simulation with fictional data, not a run on a NAS. The skill text was followed literally while each expert agent was played strictly from real test files: document text for document-agent, the photos and their dates for photo-agent, and file-name matching for file-agent.

Scenario date: 20 Nov 2026, 08:40. Test library: 28 fictional files (receipts, warranty cards, a protection plan scan, manuals, phone photos and unrelated documents), including traps such as a duplicate manual, an old dishwasher, a mismatched fridge serial and an unrelated error-code photo.

| Scenario | User says | Expected | Result |
|---|---|---|---|
| A | "The dishwasher is doing this again." | Covered by plan EPP-3Y-90417733 to 14 Mar 2029; base ended 14 Mar 2026; E15 steps, safety first; duplicate manual noted; claim draft saved after yes | Pass |
| B | "Washing machine shows F21. Is it still under warranty?" | Not covered, ended 2 Jun 2025 (receipt photo 06/02/2023 read as 2 June); F21 drain steps; no draft | Pass |
| C | "The fridge stopped cooling." | Unclear: serial 30847 vs 30647; would be partly covered to 10 Jan 2027; not-cooling steps; draft marks the serial | Pass |
| D | "The TV has sound but no picture." | Covered to 1 Dec 2026 if panel, board or power supply; no manual, universal safety only; draft declined, not saved | Pass |
| E | "Which warranties run out in the next three months?" | TV 1 Dec, soundbar 18 Dec, fridge compressor 10 Jan 2027, $2,527 losing cover; router unknown; 2 older out of warranty | Pass |
| F | "Is my coffee machine under warranty?" | Nothing found; asks when it was bought; no other product's documents used | Pass |
| G | "My washing machine is showing E15." | Not covered; today's dishwasher E15 photo ignored; WM-7 manual has no E15 entry, universal safety and the manual's support contact only | Pass |
| H | "When does the dishwasher warranty run out?" | Base ended 14 Mar 2026, plan to 14 Mar 2029, motor to 14 Mar 2034; no checklist, no draft | Pass |

Result: 8 of 8 passed in the final run. Earlier runs found wording gaps in the skill, which were fixed before this run.

Limits: the expert agents were simulated, so this does not show how the real NAS search, OCR or extraction behave. Saves to the NAS were simulated as successful.
