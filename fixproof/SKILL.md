---
name: fixproof
description: Use when the user says an appliance or device is broken, leaking, not working or showing an error code, or asks whether something is still under warranty or which warranties expire soon. Reads the error code and serial from photos the user just took, finds the purchase receipt, warranty card, protection plan and user manual already stored on the NAS, gives a dated coverage verdict with the source file for every fact, pulls the manual's steps for that exact error code, and drafts a warranty claim that is saved to the NAS only after the user approves. Read-only otherwise; nothing is sent outside the NAS.
---

# Fixproof

Turn "my dishwasher is doing this" plus a phone photo of the blinking display into three answers, each backed by the user's own files:

1. **Am I covered?** A coverage verdict with the exact end date and the document it comes from, including protection plans bought separately and then forgotten.
2. **What can I try now?** The manual's steps for this error code or symptom, safety warning first.
3. **What do I send?** A claim draft filled in with model, serial, purchase proof and fault, saved only after the user approves.

A second mode, the **warranty sweep**, answers "what is about to run out?" for every appliance the NAS has paperwork for, with the purchase value that loses cover.

# Goal

Give the user a correct, evidence-backed answer about a broken appliance in one conversation, using only photos and documents that already exist on their NAS. Every date, model, serial, term and repair step in the answer comes from a named file. When a document is missing, the skill says which one and continues with what it has instead of guessing.

# Required input

Establish these before the first delegation:

- **Mode.** Fault mode when the user describes a problem or asks about one product. Sweep mode when the user asks which warranties are expiring or wants an overview.
- **Product** (fault mode): the appliance type, such as dishwasher, washing machine, fridge, TV or router, plus brand and model if given. A photo found in Step 0 can supply it.
- **Symptom** (fault mode): the user's own words, plus any error code (for example E15, F21, or a blinking light pattern). A photo found in Step 0 can supply the code.
- **Window** (sweep mode): default 90 days. When the user names months ("next three months"), use calendar months from today.
- **Today's date and time**, from the system clock. All coverage arithmetic uses the date.

If the product is still unknown after Step 0, ask one short question ("Which appliance is it?"), report status `waiting_user`, and stop until the user replies. Do not guess the product.

How values move between steps: every `{slot}` in a delegate instruction below is replaced with the real value from an upstream result (a path, model number or date that an expert actually returned) or from the user's words before the delegation is sent. Never send a slot unfilled, and never write "the file from before" inside an instruction. If a slot has no real value, leave that part of the instruction out and say what is missing.

**Model series.** Manuals often cover a series. Derive `{series}` from the real model number: keep the letters and the first two digits and replace the remaining digits with x (ADW-4820 becomes ADW-48xx). Search for both the model and the series.

# Supported capabilities

| Step | Expert agent | CLI capability | Effect |
|---|---|---|---|
| Read the error display and rating plate the user just photographed | photo-agent | `ug-photo` search-picture, vision-ocr | read |
| Find receipts, warranty cards, plans and manuals by name, folder and type | file-agent | `ug-filesystem` find | read |
| Detect duplicate copies of the same document | file-agent | `ug-filesystem` stat, sha256sum | read |
| Extract purchase data | document-agent | `ug-document` extract, schema receipt, then invoice | read |
| Confirm which files mention the model, read terms and manual rows | document-agent | `ug-document` qa, intents locate_content, period, condition | read |
| Cross-check model, serial and dates across documents | document-agent | `ug-document` reconcile | read |
| Save the claim draft or warranty calendar | knowledge-agent | `ug-knowledge` save-text | write, needs approval |

The parent orchestrates through `delegate` only and must never use cli.invoke directly. Coverage arithmetic, verdict labels and the final answer are composed by the parent from the experts' real results, using [references/coverage-rules.md](references/coverage-rules.md).

When an expert result reports partial coverage or lists files it could not read, name those files in Notes and never give a Covered verdict that rests on an unread file.

# Workflow

Keep an **evidence list** for the whole conversation: every file used, with its path and what was taken from it. The final answer cites it.

## Fault mode

### Step 0. Read what the user just photographed

People photograph the blinking display and the rating plate before they ask. Phone backup puts those photos on the NAS.

- delegate --target photo-agent --instruction 'Search photos taken in the last 48 hours, up to {now}, for pictures of an appliance control panel or display showing an error code, or of an appliance rating plate or serial label. For each photo found, run text recognition and return the photo path, the time taken and the recognised text. If there are no results, say zero matches.'

From the recognised text, take the error code, brand, model and serial if present, and add the photos to the evidence list. Text that does not name an appliance counts as no match. If the user's words and the photo disagree (the user says dishwasher, the plate says washing machine), ask which one, report `waiting_user`, and stop until the user replies. An empty result is normal: continue with the user's words.

### Step 1. Find the purchase record

file-agent find matches names, folders, types and dates, not document text, so search by name patterns:

- delegate --target file-agent --instruction 'Find files whose names contain any of: receipt, invoice, order, purchase, quittung, {brand}, {model}, {product}. Search folders whose names contain Receipts, Invoices, Purchases, Orders, Documents, Scans or Downloads first, then all user files. File types: documents and images. Return full path, file name, type, size and modified date for each, up to 50. If there are no results, say zero matches.'

Many paper receipts exist only as phone photos:

- delegate --target photo-agent --instruction 'Search the photo library for photos of a paper receipt or till slip that mention {product} or {brand}. For each photo found, run text recognition and return the photo path, the date taken and the recognised text. If there are no results, say zero matches.'

Then extract purchase data from the real document paths returned by file-agent:

- delegate --target document-agent --instruction 'Extract purchase details with the receipt schema from these files: {receipt paths}. If a file returns no data with the receipt schema, try the invoice schema. For each file return store, order number, purchase date exactly as printed, product description, brand, model number, serial number if printed, price, and every other line item, especially any protection plan, extended warranty or care plan with its plan number and term. Report any file you could not read.'

For a receipt that exists only as a photo, use the photo-agent's recognised text as the purchase record and say so in the evidence list. Receipts and photos that name a different product count as no match.

If no purchase record is found in either result, tell the user "I couldn't find a receipt for your {product} on the NAS. Do you know roughly when you bought it?", report `waiting_user`, and stop until the user replies. If they give a date, label the verdict "based on the date you gave". If they do not know, skip the verdict and continue from Step 4. Never invent a purchase date.

**Choosing between candidates:**

- A model or serial from the user, from a Step 0 photo, or from a rating-plate photo that matches exactly one receipt settles it. Mention the other purchase in Notes.
- If two purchases of the same product type remain (for example a 2019 and a 2024 dishwasher), list both with dates, ask which one, report `waiting_user`, and stop until the user replies. The most recent purchase is the suggested default, not an assumption.

### Step 2. Find warranty and protection plan documents

First by name:

- delegate --target file-agent --instruction 'Find files whose names contain any of: warranty, guarantee, garantie, protection, plan, care, extended, registration, certificate, {brand}, {model}, {series}. Search folders whose names contain Warranty, Receipts, Scans, Documents, Home or Appliances first, then all user files. File types: documents and images. Return full path, file name, size and modified date for each, up to 50. If there are no results, say zero matches.'

Then confirm by content, because a file named "scan_0042.pdf" can be the plan terms:

- delegate --target document-agent --instruction 'With intent locate_content and evidence mode focused, check these files: {candidate paths from file-agent}. List only the files that are a warranty, guarantee, protection plan or warranty registration for {brand} {model} or the series {series}, or a plan bought with order {order number}. For each, quote the line that shows it. If none match, say zero matches.'

Then read the terms from the confirmed files only:

- delegate --target document-agent --instruction 'Answer from these files only: {confirmed warranty and plan paths}. With intent period and answer mode table, return for each document: the provider, each coverage (full parts and labour, parts only, or named components such as motor, compressor or panel) with its term, how the start date is defined, and any printed start or end date. With intent condition, return the exclusions and the claim procedure (phone, email or web form exactly as written, required attachments). Also return any plan number, registration number and serial number written on it. Quote the page or section for each answer.'

If no warranty document is confirmed, check whether the receipt or the manual states a warranty term and label it "stated on the receipt" or "stated in the manual". If nothing states a term, say so. Do not assume a typical term.

### Step 3. Coverage verdict and cross-checks

Whenever a receipt and at least one warranty document exist, cross-check them:

- delegate --target document-agent --instruction 'Reconcile these files and report every difference in brand, model number, serial number, purchase date, plan start or end date, or owner name: {receipt path}, {confirmed warranty and plan paths}. For each difference give both values and the file each came from. If they all agree, say no differences found.'

If a rating-plate photo of this product exists (Step 0 or Step 1), compare its serial and model with the reconciled values too.

Then the parent computes each end date from the real purchase date and term with [references/coverage-rules.md](references/coverage-rules.md), compares it with today, and picks one label: **Covered**, **Partly covered**, **Not covered** or **Unclear**, using the label table in that file. Show the reasoning in one line, for example: "Bought 14 Mar 2024 + 2-year warranty = ended 14 Mar 2026. Protection plan EPP-3Y-90417733 runs to 14 Mar 2029, so covered by the plan."

Report every mismatch plainly with both values and both files. Never hide one to make the answer neater.

### Step 4. Troubleshooting from the manual

- delegate --target file-agent --instruction 'Find files whose names contain any of: manual, guide, instructions, handbook, quick start, {model}, {series}, {brand}. Search folders whose names contain Manuals, Documents, Downloads, Home or Appliances first, then all user files. File type: documents. Return full path, file name, size and modified date, up to 20. If there are no results, say zero matches.'

If two results share a name stem and size, ask file-agent for the sha256sum of both; if they are identical, keep the copy in the more specific folder and note that a duplicate exists. Then confirm which file is the manual for this model with the same locate_content check as Step 2.

If no manual is confirmed, tell the user "There is no manual for {brand} {model} on your NAS", give only the universal safety advice from the coverage rules (switch off at the wall; for a leak, also close the water supply), and offer to save the claim draft or a reminder in Step 5. Do not improvise repair steps.

Otherwise ask the real manual found upstream:

- delegate --target document-agent --instruction 'Using only {manual path}, with intent locate_content and answer mode table, find what the manual says about error code {code} and about the symptom "{symptom}". Return the matching rows of the error-code and troubleshooting tables (problem, cause, what to do) in the order printed, the safety warnings that apply to those steps, any steps that need a qualified technician, and any statement that user repairs affect the warranty. Give the page or section for each item.'

Present the steps as a short numbered checklist in the manual's order, safety warning first. Mark technician-only steps, and say when a do-it-yourself step could affect the warranty.

### Step 5. Claim draft and approval

Only when the label is Covered, Partly covered or Unclear, compose a claim draft with [references/answer-format.md](references/answer-format.md): the claim contact exactly as written, product, brand, model, serial, purchase date, store, order number, plan number, the fault with its error code, "Already tried: none confirmed", and the attachments the procedure asks for, listed by their real paths. If the plate serial and the registered serial differ, use the plate value, show the registered value beside it, and mark it to be checked.

Show the draft and ask: "Which of the steps above have you already tried? Then say yes to save this draft to your NAS, or no." Report `waiting_approval`. Add the tried steps the user names to "Already tried". Only after a clear yes:

- delegate --target knowledge-agent --instruction 'Save this text as a new note with filename hint "Warranty claim {brand} {model} {today} {time}". Text: {claim draft text}'

Report the saved file path the knowledge-agent returns. If the user says no, report `completed` with "not saved" and keep the draft in chat. The skill never sends, emails or shares the claim; the user does that.

### Step 6. Answer

Reply in the order set out in [references/answer-format.md](references/answer-format.md): safety line when it must lead, product line, coverage label with one-line reasoning, checklist, claim line, evidence list, and Notes for mismatches, exclusions, duplicates and missing documents. Leave out lines that do not apply.

## Sweep mode

### Step S1. Collect paperwork

- delegate --target file-agent --instruction 'Find files whose names contain any of: receipt, invoice, order, purchase, warranty, guarantee, protection, plan, registration, manual, guide. Search folders whose names contain Receipts, Invoices, Purchases, Orders, Warranty, Manuals, Scans, Documents, Home or Appliances first, then all user files. File types: documents and images. Return full path, file name, size and modified date for each, up to 200. If there are no results, say zero matches.'
- delegate --target photo-agent --instruction 'Search the photo library for photos of paper receipts or till slips for appliances or electronics. For each photo found, run text recognition and return the photo path, the date taken and the recognised text. If there are no results, say zero matches.'

If both results are empty, say "I found no receipts, warranty documents or manuals on the NAS", report `completed` with nothing to list, and stop.

### Step S2. Extract products and terms

- delegate --target document-agent --instruction 'Extract with the receipt schema from these files: {receipt and invoice paths from S1}. Return one row per purchased appliance or device: store, purchase date as printed, brand, product, model, serial, price, and any protection plan line with its term. Skip groceries, services and consumables. Report any file you could not read.'
- delegate --target document-agent --instruction 'With intent period and answer mode table, answer from these files only: {warranty, plan and registration paths from S1}. For each document return the brand, model or series it covers, each coverage term (base, component such as motor or compressor, protection plan), how the start date is defined, and any printed end date.'
- delegate --target document-agent --instruction 'With intent extraction and answer mode table, answer from these files only: {manual paths from S1}. For each manual return the brand, product type and model or series it covers.'

Add the photo-agent's receipt text as purchase rows. Match warranties and manuals to purchases by brand and model or series, then sort every product into the calendar groups in [references/coverage-rules.md](references/coverage-rules.md): a warranty with no receipt gets "purchase date unknown", a receipt with no term gets "term unknown", a manual alone gets "no receipt found".

### Step S3. Calendar

List, soonest first, coverage ending within the window, then active coverage beyond it, then unknowns. Under "Ending soon", add the total purchase price of those products, from the receipts, as "value losing cover". For each item ending soon, add one practical line drawn from its documents, for example "claims need the receipt and a rating-plate photo".

Offer to save the calendar, report `waiting_approval`, and only after a clear yes:

- delegate --target knowledge-agent --instruction 'Save this text as a new note with filename hint "Warranty calendar {today} {time}". Text: {calendar text}'

# Completion and failure

| Status | When | What the user sees |
|---|---|---|
| `completed` | The answer is delivered, whether or not a note was saved | The answer in the format of [references/answer-format.md](references/answer-format.md), the evidence list, and "saved to {path}" or "not saved" |
| `waiting_user` | The product is unclear, two purchases match, a photo contradicts the user, or a purchase date is needed | One short question; nothing else runs until the user replies |
| `waiting_approval` | A claim draft or calendar is ready to save | The full text and a yes/no question |
| `cancelled` | The user stops the conversation or says to drop the task while the skill is waiting | Confirmation that nothing was written |
| `failed` | An expert returns an error twice for a step | Which step failed, which file, and what the answer still covers without it |

Failure rules:

- **Empty result.** When a search returns zero matches, say what was not found and continue with the parts that do not depend on it. Never substitute a document for a different model or product.
- **Unreadable file.** If an expert cannot read a file (a blurred photo, a scan with no text), name the file, mark its facts unknown, and suggest re-scanning it.
- **Expert error.** If a delegation reports `failed`, retry once with the same real values. If it fails again, report `failed` for that step and deliver the rest of the answer, marked as partial.
- **Conflicting documents.** Never pick the convenient value. Show both values and their files, and apply the conflict rules in [references/coverage-rules.md](references/coverage-rules.md).
- **Safety.** For gas, a burning smell, smoke, sparks, or any leak from an appliance connected to mains power, the first line of the answer tells the user to switch off at the wall, close the water or gas supply if relevant, and call a qualified technician if it persists, before any coverage detail.

# Safety and data handling

- Read-only except for the two approved saves. The skill never deletes, moves, renames or overwrites files.
- Nothing leaves the NAS. No document, serial number or claim is sent, uploaded or shared; the user sends the claim.
- Every fact in the answer comes from a file in the evidence list.
- Each save needs its own clear yes, even if the user approved a save earlier in the conversation.

Worked examples are in [references/examples.md](references/examples.md). Third-party components, licences and AI-tool disclosure are in [references/disclosure.md](references/disclosure.md). A plain-language guide is in [references/user-guide.md](references/user-guide.md).

# Generation-time capability evidence

- `ug-filesystem` → `file-agent`
- `ug-photo` → `photo-agent`
- `ug-document` → `document-agent`
- `ug-knowledge` → `knowledge-agent`
