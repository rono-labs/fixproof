---
name: fixproof
description: Use when the user says an appliance or device is broken, leaking, not working or showing an error code, or asks whether something is still under warranty or which warranties expire soon. Finds the purchase receipt, warranty card, protection plan and user manual already stored on the NAS, gives a dated coverage verdict with the source file for every fact, pulls the manual's troubleshooting steps for the exact symptom or error code, and drafts a warranty claim that is saved to the NAS only after the user approves. Read-only otherwise; nothing is sent outside the NAS.
---

# Fixproof

Turn "my dishwasher is leaking and shows E15" into three answers, each backed by the user's own files:

1. **Am I covered?** A coverage verdict with the exact end date and the document it comes from, including protection plans bought separately.
2. **What can I try now?** The manual's steps for this symptom or error code, safety warning first.
3. **What do I send?** A claim draft filled in with model, serial, purchase proof and symptom, saved only after the user approves.

A second mode, the **warranty sweep**, answers "what is about to run out?" for every appliance with a receipt on the NAS.

# Goal

Give the user a correct, evidence-backed answer about a broken appliance in one conversation, using only documents that already exist on their NAS. Every date, model, serial, term and repair step in the answer must come from a named file. When a document is missing, the skill says which one and keeps going with what it has, instead of guessing.

# Required input

Establish these from the user's message before the first delegation:

- **Mode.** Fault mode when the user describes a problem or asks about one product. Sweep mode when the user asks which warranties are expiring or wants an overview of all appliances.
- **Product** (fault mode): the appliance type, such as dishwasher, washing machine, fridge, TV or router, plus brand and model if the user gives them.
- **Symptom** (fault mode): the user's own words, plus any error code (for example E15, F21, or a blinking light pattern).
- **Window** (sweep mode): how far ahead to look. Default 90 days.
- **Today's date**, from the system clock. All coverage arithmetic uses it.

If the product type cannot be identified, ask one short question ("Which appliance is it?"), report status `waiting_user`, and wait. Do not guess the product.

How values move between steps: every `{slot}` in a delegate instruction below is filled with the real value from the upstream result (a path, model number or date that an expert actually returned) or from the user's words. Never send a slot unfilled, and never write "the file from before" in an instruction. If a slot has no real value, leave that part of the instruction out and say what is missing.

# Supported capabilities

| Step | Expert agent | CLI capability | Effect |
|---|---|---|---|
| Find receipts, warranty cards, plans, manuals | file-agent | `ug-filesystem` find, stat | read |
| Read photographed receipts and rating plates | photo-agent | `ug-photo` search-picture, vision-ocr | read |
| Extract purchase data | document-agent | `ug-document` extract (schema receipt or invoice) | read |
| Read warranty terms and manual sections | document-agent | `ug-document` qa | read |
| Cross-check model and serial across documents | document-agent | `ug-document` reconcile | read |
| Save the claim draft or warranty calendar | knowledge-agent | `ug-knowledge` save-text | write, needs approval |

The parent orchestrates through `delegate` only and must never use cli.invoke directly. Coverage date arithmetic and the final answer are composed by the parent from the experts' real results. Detailed decision rules are in [references/coverage-rules.md](references/coverage-rules.md).

# Workflow

Keep an **evidence list** for the whole conversation: every file used, with its path and what was taken from it. The final answer cites it.

## Fault mode

### Step 1. Find the purchase record

Search files first:

- delegate --target file-agent --instruction 'Find documents that look like receipts, invoices or order confirmations for a {product} {brand} {model}. Search folders whose names contain Receipts, Invoices, Purchases, Orders, Documents, Scans or Downloads first, then all of the user files. Include PDF, image and office document types. For each match return the full path, file name, type and modified date, up to 30 matches. If there are no results, say zero matches.'

Then search photos, because many receipts are phone photos and many serial numbers only exist on a photographed rating plate:

- delegate --target photo-agent --instruction 'Search the photo library for photos of a paper receipt or of an appliance rating plate or serial label for a {product} {brand}. For each photo found, run text recognition and return the photo path, the date taken and the recognised text. If there are no results, say zero matches.'

If both searches return an empty result, tell the user "I could not find a receipt for your {product} on the NAS", ask whether they know the purchase date, report `waiting_user`, and continue with Step 4 if they do not. Never invent a purchase date.

Otherwise read the candidates found upstream:

- delegate --target document-agent --instruction 'Extract purchase details with the receipt schema from these files: {receipt paths from file-agent}. For each file return store, order number, purchase date, product description, brand, model number, serial number if printed, price, and every other line item, especially any protection plan, extended warranty or care plan with its plan number and term.'

Merge in the model and serial text the photo-agent recognised. Choosing between candidates:

- Prefer the purchase whose product type and model match the user's words.
- If there are two purchases of the same product type (for example an old dishwasher from 2019 and a new one from 2024), list both with dates and ask which one, unless the user's details settle it. Report `waiting_user` while waiting. The most recent purchase is the suggested default, not an assumption.

### Step 2. Find warranty and protection plan documents

Search by the real model and brand from Step 1, not just the product type:

- delegate --target file-agent --instruction 'Find documents that mention {model} or {brand} {product} together with any of these words: warranty, guarantee, protection plan, extended, care plan, certificate, registration. Also return any file in the same folder as {receipt path} with a modified date within 30 days of {purchase date}. Return full path, file name and modified date for each, up to 30. If there are no results, say zero matches.'

Read the terms from the real files returned:

- delegate --target document-agent --instruction 'Answer from these files only: {warranty and plan paths}. For each document return: who provides it, what it covers (full parts and labour, parts only, or named components such as motor or compressor) with the term for each, whether the term starts at purchase, delivery or when another warranty ends, the exclusions, the claim procedure (phone, email or web form exactly as written, and required attachments), and any plan or registration number with any serial number written on it. Quote the page or section for each answer.'

If no warranty document exists, check whether the receipt or the manual states a standard warranty term and label it "stated on the receipt" or "stated in the manual". If nothing states a term, say so. Do not assume a typical term.

### Step 3. Coverage verdict and cross-checks

The parent computes each end date from the real purchase date and term, using the rules in [references/coverage-rules.md](references/coverage-rules.md), then compares it with today:

- **Covered**: today is on or before an end date, and the failing part is within that coverage.
- **Partly covered**: the base warranty has ended but a component warranty or a protection plan is still active, or only some parts of the fault are covered.
- **Not covered**: every term has ended. Say when the last one ended.
- **Unclear**: dates or terms conflict, or the symptom may fall under an exclusion. Say exactly what conflicts and what would settle it.

Show the reasoning in one line, for example: "Bought 14 Mar 2024 + 2-year warranty = ended 14 Mar 2026. Protection plan EPP-3Y-90417733 runs to 14 Mar 2029, so covered by the plan."

When the receipt, the warranty documents and any rating-plate photo all exist, cross-check them:

- delegate --target document-agent --instruction 'Compare these files and report every difference in model number, serial number, purchase date, owner name or store: {receipt path}, {warranty and plan paths}. For each difference give both values and the file each came from. If they all agree, say no differences found.'

Also compare the serial from the photo-agent's recognised text. Report every mismatch plainly; never hide one to make the answer neater. A serial mismatch makes the verdict **Unclear** until the user checks the plate.

### Step 4. Troubleshooting from the manual

- delegate --target file-agent --instruction 'Find user manuals, installation guides or quick start guides for {brand} {model} or its model series {series}. Search folders whose names contain Manuals, Documents, Downloads or Home first, then all user files. Return full path, file name and modified date, up to 10. If there are no results, say zero matches.'

If the result is empty, tell the user "There is no manual for {brand} {model} on your NAS", give only universally safe advice (switch off and unplug the appliance; if it is leaking, also close the water supply), and offer to save a reminder note in Step 5. Do not improvise repair steps.

Otherwise ask the real manual found upstream:

- delegate --target document-agent --instruction 'Using only {manual path}, find what the manual says about error code {code} and about the symptom "{symptom}". Return the matching rows of the troubleshooting or error-code table (problem, cause, what to do) in the order printed, the safety warnings that apply to those steps, any steps the manual says need a qualified technician, and any statement that user repairs affect the warranty. Give the page or section for each item.'

Present the steps as a short numbered checklist in the manual's order, safety warning first. Mark the steps reserved for a technician, and say when a do-it-yourself step could affect the warranty.

### Step 5. Claim draft and approval

Only when the verdict is covered, partly covered or unclear, compose a claim draft from the evidence list: the claim contact exactly as written in the warranty or plan, product, brand, model, serial, purchase date, store, order number, plan number, the fault in plain words with the error code, the troubleshooting steps the user confirms they already tried, and the attachments to include (the real paths of the receipt, warranty card and plan, plus anything the claim procedure asks for, such as a photo of the rating plate).

Show the draft in chat and ask: "Save this claim draft to your NAS?" Report `waiting_approval`. Only after a clear yes:

- delegate --target knowledge-agent --instruction 'Save this text as a new note titled "Warranty claim - {brand} {model} - {today}". Do not overwrite an existing note; if the title exists, add a number to the title. Text: {claim draft text}'

Report the saved file path the knowledge-agent returns. If the user says no, report `cancelled` for the save and keep the draft in chat. The skill never sends, emails or shares the claim; the user does that.

### Step 6. Answer

Reply in the order set out in [references/answer-format.md](references/answer-format.md): product line, coverage verdict with one-line reasoning, safety line, checklist, claim line, evidence list, and notes for mismatches or exclusions. Leave out lines that do not apply.

## Sweep mode

### Step S1. Collect every purchase record

- delegate --target file-agent --instruction 'Find every document that looks like a receipt, invoice, order confirmation, warranty card or protection plan in the user files. Search folders whose names contain Receipts, Invoices, Purchases, Orders, Warranty, Documents or Scans first, then all user files. Return full path, file name and modified date for each, up to 200. If there are no results, say zero matches.'

If the result is empty, say "I found no receipts or warranty documents on the NAS", report `completed` with nothing to list, and stop.

### Step S2. Extract products and terms

- delegate --target document-agent --instruction 'Extract with the receipt schema from these files: {paths from S1}. Return one row per purchased appliance or device: store, purchase date, brand, product, model, serial, and any protection plan line with its term. Skip groceries, services and consumables.'
- delegate --target document-agent --instruction 'Answer from these files only: {warranty and plan paths from S1}. For each document return the brand, model or model series it covers, each coverage term (base, component such as motor or compressor, protection plan), and how the start date is defined.'

Match each appliance to its warranty documents by brand and model. For appliances with no warranty document and no term on the receipt, list them as "term unknown".

### Step S3. Calendar

Compute every end date with [references/coverage-rules.md](references/coverage-rules.md). List, soonest first: coverages ending within the window, then active coverages beyond it, then ended ones, then unknown terms. For each ending soon, add one practical line drawn from the documents, for example "the plan requires registration within 30 days" or "check the door seal before the warranty ends".

Offer to save the calendar as a note, report `waiting_approval`, and only after a clear yes:

- delegate --target knowledge-agent --instruction 'Save this text as a new note titled "Warranty calendar - {today}". Do not overwrite an existing note; if the title exists, add a number to the title. Text: {calendar text}'

# Completion and failure

| Status | When | What the user sees |
|---|---|---|
| `completed` | The answer is delivered, with or without a saved note | The answer in the format of [references/answer-format.md](references/answer-format.md) and the evidence list |
| `waiting_user` | The product is unclear, two purchases match, or the purchase date is unknown | One short question; nothing else runs until the user replies |
| `waiting_approval` | A claim draft or calendar is ready to save | The full text and a yes/no question |
| `cancelled` | The user declines the save or stops the conversation | Confirmation that nothing was written; the draft stays in chat |
| `failed` | An expert returns an error or cannot read a file | Which step failed, which file, and what the answer still covers without it |

Failure rules:

- **Empty result.** When a search returns zero matches, say what was not found and continue with the parts that do not depend on it. Never substitute a document for a different model or product.
- **Unreadable file.** If the document-agent cannot read a file (for example a blurred photo), name the file, mark its facts unknown, and suggest re-scanning it.
- **Expert error.** If a delegation reports `failed`, retry once with the same real values. If it fails again, report `failed` for that step and deliver the rest of the answer, clearly marked as partial.
- **Conflicting documents.** Never pick the convenient value. Show both values and their files, and make the verdict Unclear.
- **Safety.** If the symptom involves gas, burning smell, smoke, sparks or water near electrics, the first line of the answer tells the user to switch off at the wall or close the supply and call a qualified technician, before any coverage detail.

# Safety and data handling

- Read-only except for the two approved saves. The skill never deletes, moves, renames or overwrites files.
- Nothing leaves the NAS. No document, serial number or claim is sent, uploaded or shared; the user sends the claim themselves.
- Evidence or nothing: every fact in the answer comes from a file in the evidence list.
- Approval prompts are never skipped, even when the user has approved a save earlier in the conversation.

Examples of full conversations are in [references/examples.md](references/examples.md). Third-party components, licences and AI-tool disclosure are in [references/disclosure.md](references/disclosure.md). A plain-language guide for users is in [references/user-guide.md](references/user-guide.md).

# Generation-time capability evidence

- `ug-filesystem` → `file-agent`
- `ug-photo` → `photo-agent`
- `ug-document` → `document-agent`
- `ug-knowledge` → `knowledge-agent`
