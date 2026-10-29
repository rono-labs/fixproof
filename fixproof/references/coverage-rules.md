# Coverage rules

These rules turn the real dates and terms returned by the document-agent into a verdict. The parent applies them. No expert is asked to judge coverage.

## Reading dates

- Use dates exactly as printed. If a printed date can be read two ways (06/02/2023 can be 2 June or 6 February), decide with the store's country format, the order number, the file name or the photo's date taken, in that order. State the reading in Notes. If nothing settles it, use both readings. If they give different labels, the label is Unclear.
- File modified dates are copy or upload dates. Never use them as purchase dates.

## Start date

1. A start or end date printed on the warranty or plan document wins over any calculation.
2. Otherwise use the start rule written in the document. "From delivery" uses the delivery date on the receipt or order confirmation, if one is present.
3. "From purchase", or no rule at all, uses the purchase date on the receipt.
4. A plan that "starts when the manufacturer warranty ends" with no printed date starts on the day the base warranty ends. If a printed date differs from the calculated one by a day, note it and keep the printed date. A one-day gap is not a conflict.
5. If the only purchase date is the user's own statement, use it and add "based on the date you gave" to the reasoning.

## End date

- End date = start date + term, on the same calendar day. For 29 February with a term in whole years, use 28 February.
- A term given in months adds calendar months.
- Coverage is active on the end date itself.
- If two documents give different terms for the same coverage, report both terms with their files and set the label to Unclear.

## Labels

| Label | When |
|---|---|
| Covered | An active coverage applies to the whole fault. For a named-component coverage (panel, board, motor, compressor), use Covered when the manual's cause or the symptom points to a listed component, and add "if the technician confirms a {component} fault". |
| Partly covered | An active coverage applies to only part of the likely causes. Example: the general warranty has ended, but the compressor warranty is active and "not cooling" may or may not be the compressor. Name what is and is not covered. |
| Not covered | Every coverage has ended. Say when the last one ended. Troubleshooting is still given. |
| Unclear | Documents conflict on a term or date, a serial number differs between the receipt, registration and plate photo, the warranty may belong to another appliance, or the only likely cause is an exclusion. Always add what would make the label definite. Example: "Would be partly covered (compressor, to 10 Jan 2027) once the serial is confirmed." |

## Exclusions

Compare the manual's causes for the symptom with the exclusions list. Typical exclusions: improper installation, wrong detergent, limescale, accidental damage, cosmetic damage, consumables such as filters, gaskets and bulbs.

- When the manual lists only one cause and that cause is excluded, the label is Unclear. Quote the exclusion.
- When the manual lists several causes and only some are excluded, keep the label and add a Note that quotes the exclusion, for example "a worn door gasket is excluded; an internal leak is covered".
- Only the provider decides on an exclusion, so the skill never says Not covered because of one.

## Cross-check outcomes

| Finding | Effect |
|---|---|
| Model on the receipt is in the series on the warranty or manual (ADW-4820 and ADW-48xx) | Treat as a match. Note the series. |
| Model differs in type or brand | Unclear. The document may belong to another appliance. |
| Serial on the registration differs from the receipt or the plate photo | Unclear. Show both values and files. Ask the user to read the plate. |
| Owner name differs | Note only. |
| Two byte-identical copies of a document | Use one and note the duplicate. |

## Universal safety advice

When there is no manual, these lines are the only advice allowed:

- Switch the appliance off at the wall or unplug it.
- If it is leaking, close the water supply valve.
- If you smell gas or burning, or see smoke or sparks, leave it off and call a qualified technician.

## Sweep groups

1. **Ending soon**: coverage that ends within the window, soonest first, with the sum of these products' own line-item prices as "value losing cover".
2. **Active later**: coverage that ends after the window.
3. **Unknown**: "purchase date unknown" (a warranty with no receipt), "term unknown" (a receipt with no term), "no receipt found" (a manual only).
4. **Ended**: only if the user asks for everything, most recent first. Products whose every coverage has ended are otherwise counted in one closing line, for example "3 older appliances are out of warranty".
