# fixproof

A Skill for Uliya, the assistant on UGREEN AI NAS. When an appliance breaks, it finds the receipt, warranty card, protection plan and user manual already stored on the NAS. It tells you whether you are covered and until when, shows the manual's steps for your exact error code, and drafts the warranty claim.

    "My dishwasher is leaking and showing E15."

    Coverage: Covered. The 2-year warranty ended 14 Mar 2026, but protection plan
    EPP-3Y-90417733 runs to 14 Mar 2029 and covers this fault.
    Safety first: unplug the dishwasher and close the water tap.
    Try this (manual section 7.2): ...
    Claim: draft ready for the Brightline plan claims line. Save it to your NAS? (yes / no)

A second mode lists every warranty that runs out in the next 90 days.

## Layout

| Path | What |
|---|---|
| `fixproof/` | The Skill package: `SKILL.md` plus linked `references/*.md`. This folder is what gets zipped and installed. |
| `testdata/` | A fictional family NAS library (28 files) and the expected answer for 6 scenarios. |
| `validation/` | Dry-run transcripts of the skill against the test library. |
| `tools/` | Package checker, zip builder, proposal PDF builder. |

## Use

Install: copy `fixproof/` into the Uliya skills location on the NAS, or upload the zip from `submission/fixproof.zip`, then ask Uliya something like "Is my washing machine still under warranty?"

Check and package (Python 3.10+, no dependencies):

    python3 project/tools/check_skill.py project/fixproof
    python3 project/tools/package_skill.py project/fixproof submission/fixproof.zip

Official check, with the UGREEN kit (uliya-skill-kit-0.7.3-en.zip, Node 18+) unzipped next to the repo:

    node ../uliya-skill-kit/scripts/check-skill.mjs project/fixproof

It reports `"status": "static-pass"` with 0 errors and 0 warnings.

Regenerate the test library (needs reportlab, Pillow, numpy):

    .venv/bin/python project/testdata/make_library.py

## How it works

1. file-agent and photo-agent find receipts, including phone photos of paper receipts and rating plates.
2. document-agent extracts the purchase with the receipt schema: date, store, model, serial, and any protection plan line.
3. file-agent searches for warranty and plan documents using the real model number. document-agent reads terms, components, exclusions and the claim procedure.
4. The skill computes each end date, then cross-checks model and serial across the receipt, the warranty registration and the plate photo.
5. file-agent finds the manual for the model series. document-agent returns only the rows for this error code, with the safety warnings.
6. The claim draft is shown in chat and saved by knowledge-agent only after the user says yes.

The skill never deletes, moves or sends anything. Every fact in the answer is linked to the file it came from.
