# Answer format

Use these lines in this order. Leave out a line when it does not apply. Plain text, no tables in chat.

## Fault mode

    Product: {brand} {model} ({product}), bought {purchase date} at {store}
    Coverage: {Covered | Partly covered | Not covered | Unclear}. {one-line reasoning with dates}
    Safety first: {one warning quoted from the manual, or the universal safety advice when there is no manual}
    Try this (manual {section or page}):
      1. {step}
      2. {step}
      Technician only: {steps the manual reserves}
    Claim: draft ready for {claim contact}. {save question from Step 5}
      after yes: Claim draft saved to {path}.
      after no: Claim draft not saved; it stays in this chat.
    Evidence:
      - {path}: purchase date, model, serial
      - {path}: warranty term, exclusions, claim contact
      - {path}: troubleshooting for {code}
    Notes: {mismatches, exclusions, missing documents, or "none"}

When the symptom involves gas, smoke, a burning smell, sparks, or a leak from an appliance on mains power, the safety line moves above the product line.

## Coverage question only

    Product: {brand} {model} ({product}), bought {purchase date} at {store}
    Coverage:
      - {coverage name}: {ended | runs to} {end date} ({path})
      - {coverage name}: {ended | runs to} {end date} ({path})
    Need the manual's steps for a fault? Tell me what it is doing.
    Evidence: {paths}
    Notes: {mismatches or "none"}

## Claim draft

    To: {claim contact exactly as written}
    Subject: Warranty claim, {brand} {model}, serial {serial}
    Product: {brand} {model}, serial {serial}
    Purchased: {purchase date} at {store}, order {order number}
    Coverage: {warranty or plan name and number}, valid until {end date}
    Fault: {symptom in plain words}, error code {code}
    Already tried: {steps the user confirmed, or "none confirmed"}
    Attachments: {receipt path}, {warranty path}, {plan path}, {photo of rating plate if required}
    Contact: {left blank for the user to fill in}

The draft never contains the user's address, phone or email unless the user types them in.

## Sweep mode

    Warranty calendar, {today}, next {window} (to {window end date})
    Ending soon (value losing cover: {sum of purchase prices}):
      - {date}: {brand} {model} {coverage type} ({path}). {one practical line}
    Active later:
      - {date}: ...
    Unknown:
      - {brand} {model}: term unknown, receipt {path}, no warranty document found
      - {brand} {model}: no receipt found, manual {path}
    {count} older appliances are out of warranty.
    Save this calendar to your NAS? (yes / no)
