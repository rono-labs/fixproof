#!/usr/bin/env python3
"""Generate the fictional fixproof test library into ./home-library/ (deterministic).
Run: .venv/bin/python project/testdata/make_library.py
All brands, stores, people and addresses are invented."""
import random, shutil, io
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak

OUT = Path(__file__).parent / "home-library"
SEED = 2026
if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir(parents=True)
SS = getSampleStyleSheet()
B = SS["BodyText"]; B.fontSize = 10; B.leading = 14
H1 = ParagraphStyle("h1", parent=SS["Heading1"], fontSize=18, spaceAfter=8)
H2 = ParagraphStyle("h2", parent=SS["Heading2"], fontSize=13, spaceBefore=8, spaceAfter=4)
SM = ParagraphStyle("sm", parent=B, fontSize=8, leading=10)
CUST = ["Alex Rivera", "48 Larkspur Lane, Maple Hollow, OR 97000"]
BRAND_COL = {"Nordvik": colors.HexColor("#1f4e79"), "Lumora": colors.HexColor("#6a1b9a"),
             "Brightline Electronics": colors.HexColor("#e65100"), "HomeHub Appliances": colors.HexColor("#2e7d32"),
             "HomeHub": colors.HexColor("#2e7d32"), "Zentro": colors.HexColor("#00838f"),
             "Maple Hollow Elementary": colors.HexColor("#b71c1c"), "Valley Power & Water": colors.HexColor("#37474f")}

def P(t, s=B): return Paragraph(t, s)
def tbl(rows, widths=None, header=True, col=colors.HexColor("#444444")):
    t = Table(rows, colWidths=widths, repeatRows=1 if header else 0)
    st = [("GRID", (0, 0), (-1, -1), 0.4, colors.grey), ("FONTSIZE", (0, 0), (-1, -1), 9),
          ("VALIGN", (0, 0), (-1, -1), "TOP")]
    if header: st += [("BACKGROUND", (0, 0), (-1, 0), col), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white)]
    t.setStyle(TableStyle(st))
    # wrap strings in Paragraphs for line breaking
    t._cellvalues = [[Paragraph(str(c), SM) if isinstance(c, str) and not (header and i == 0) else c
                      for c in r] for i, r in enumerate(rows)]
    return t

def make_pdf(rel, title, brand, story, footer=""):
    path = OUT / rel; path.parent.mkdir(parents=True, exist_ok=True)
    col = BRAND_COL.get(brand, colors.HexColor("#444444"))
    def deco(c, d):
        c.saveState()
        c.setFillColor(col); c.rect(0.6*inch, 10.15*inch, 0.35*inch, 0.35*inch, fill=1, stroke=0)
        c.setFillColor(colors.white); c.circle(0.775*inch, 10.325*inch, 0.09*inch, fill=1, stroke=0)
        c.setFillColor(col); c.setFont("Helvetica-Bold", 14); c.drawString(1.05*inch, 10.25*inch, brand)
        c.setFillColor(colors.grey); c.setFont("Helvetica", 8)
        c.drawRightString(7.9*inch, 10.25*inch, title)
        c.setStrokeColor(col); c.line(0.6*inch, 10.05*inch, 7.9*inch, 10.05*inch)
        c.drawString(0.6*inch, 0.5*inch, footer or brand)
        c.drawRightString(7.9*inch, 0.5*inch, f"Page {d.page}")
        c.restoreState()
    doc = SimpleDocTemplate(str(path), pagesize=letter, leftMargin=0.6*inch, rightMargin=0.6*inch,
                            topMargin=1.2*inch, bottomMargin=0.8*inch, title=title, author=brand, invariant=1)
    doc.build(story, onFirstPage=deco, onLaterPages=deco)

# ---------------- receipts ----------------
def receipt(rel, store, addr, date, order, items, payment, notes=(), extra_lines=()):
    sub = sum(p for _, _, p in items); tax = round(sub * 0.0, 2)
    rows = [["Item", "Details", "Price"]] + [[a, b, f"${p:,.2f}"] for a, b, p in items]
    rows += [["", "Subtotal", f"${sub:,.2f}"], ["", "Sales tax", f"${tax:,.2f}"], ["", "<b>Total</b>", f"<b>${sub+tax:,.2f}</b>"]]
    s = [P("SALES RECEIPT", H1), P(f"{store}<br/>{addr}<br/>Tel 555-0142"), Spacer(1, 8),
         tbl([["Date", date], ["Order no.", order], ["Customer", f"{CUST[0]}, {CUST[1]}"], ["Payment", payment]],
             [1.3*inch, 5.9*inch], header=False), Spacer(1, 10),
         tbl(rows, [2.3*inch, 3.7*inch, 1.2*inch]), Spacer(1, 10)]
    for n in notes: s.append(P(n, SM))
    s.append(P("Keep this receipt as proof of purchase for warranty claims. Returns within 30 days with original packaging.", SM))
    make_pdf(rel, "Receipt " + order, store.split(" - ")[0], s, footer=store)

BL = "Brightline Electronics"; BLA = "1200 Commerce Way, Port Alder, OR 97001"
HH = "HomeHub Appliances"; HHA = "77 Harbor Road, Port Alder, OR 97001"

receipt("Documents/Receipts/2024/Brightline_Receipt_2024-03-14_dishwasher.pdf", BL, BLA, "2024-03-14", "BL-2024-0314-55871",
        [("Nordvik ADW-4820 Dishwasher", "Stainless, 24 in. Serial no. NV48-2203-1187", 849.00),
         ("3-Year Extended Protection Plan", "Plan no. EPP-3Y-90417733. Covers ADW-4820 after the manufacturer warranty ends. Terms provided separately.", 129.00),
         ("Installation kit", "Water supply line and drain hose", 24.99)],
        "Card ending 4417", ["Delivery to 48 Larkspur Lane. Items are non-refundable once installed."])
receipt("Documents/Receipts/2019/receipt_dishwasher_old.pdf", BL, BLA, "2019-08-22", "BL-2019-0822-20318",
        [("Nordvik ADW-3100 Dishwasher", "White, 24 in. Serial no. NV31-1905-0342", 529.00),
         ("Haul-away of old unit", "", 25.00)], "Card ending 2260",
        ["Manufacturer warranty: 1 year parts and labor. No extended plan purchased."])
receipt("Documents/Receipts/2025/Brightline_order_TV_Lumora.pdf", BL, BLA, "2025-12-01", "BL-2025-1201-77420",
        [("Lumora 55Q8 55 in. QLED TV", "Serial no. LU55-2511-90233", 699.00), ("Wall mount, tilt", "", 39.99)],
        "Card ending 4417", ["Lumora 1-year limited warranty applies from the date of purchase."])
receipt("Documents/Receipts/2025/Brightline_soundbar_2025-12-18.pdf", BL, BLA, "2025-12-18", "BL-2025-1218-80031",
        [("Lumora S2 Soundbar", "Serial no. LU-S2-2512-04418", 179.00)], "Card ending 4417",
        ["Lumora 1-year limited warranty applies from the date of purchase."])
receipt("Documents/Receipts/2022/HomeHub_receipt_fridge_Jan2022.pdf", HH, HHA, "2022-01-10", "HH-220110-3318",
        [("HomeHub FR-560 French Door Refrigerator", "Stainless, 25 cu ft. Serial no. HH56-2201-30847", 1649.00),
         ("Delivery and setup", "", 79.00)], "Card ending 2260")

# ---------------- warranty cards ----------------
def warranty(rel, brand, product, summary_rows, body, contact, extra=()):
    s = [P("LIMITED WARRANTY CARD", H1), P(f"<b>Product:</b> {product}"), Spacer(1, 6),
         tbl([["Coverage", "Term", "What is covered"]] + summary_rows, [1.6*inch, 1.2*inch, 4.4*inch]),
         P("Terms and conditions", H2)] + [P(x) for x in body] + list(extra) + [
         P("How to make a claim", H2), P(contact)]
    make_pdf(rel, f"{brand} warranty card", brand, s)

CLAIM_NV = ("Email <b>claims@nordvik-support.example</b> or call <b>1-800-555-0188</b> (Mon-Fri 8:00-18:00 Pacific). "
            "Provide a copy of the dated purchase receipt and a clear photo of the serial plate. Claims without both cannot be processed.")
warranty("Documents/Warranty/Nordvik_ADW-4820_warranty_card.pdf", "Nordvik", "ADW-4820 Dishwasher",
         [["Parts and labor", "2 years", "Repair or replacement of defective parts, and labor, from the original purchase date."],
          ["Drive motor", "10 years", "Wash motor and circulation pump motor (parts only after year 2)."]],
         ["Warranty starts on the date of original retail purchase. A dated receipt is required.",
          "<b>Exclusions:</b> damage from misuse, improper installation, power surges, frozen pipes, commercial use, cosmetic damage, consumables (filters, racks, gaskets), and any repair attempted by anyone other than a Nordvik authorized service provider.",
          "Repairs made by the owner beyond the steps listed in the user manual void this warranty.",
          "Serial no. is printed on the plate inside the door frame. Keep a photo of it."], CLAIM_NV)
warranty("Home/Appliances/Washer/Nordvik_WM-7_warranty_card.pdf", "Nordvik", "WM-7 Front Load Washing Machine",
         [["Parts and labor", "2 years", "Defective parts and labor from the original purchase date."]],
         ["Warranty starts on the date of original retail purchase. A dated receipt is required.",
          "<b>Exclusions:</b> misuse, installation faults, hoses, cosmetic damage, repairs by unauthorized persons, commercial use.",
          "This warranty has no extended components."], CLAIM_NV)
warranty("Scans/Lumora_TV_warranty.pdf", "Lumora", "55Q8 QLED Television",
         [["Limited warranty", "1 year", "Panel, board and power supply defects from the original purchase date."]],
         ["<b>Exclusions:</b> burn-in, cracked screens, physical damage, power surge, unauthorized repair, wall-mount damage.",
          "Warranty period is counted from the retail purchase date shown on the receipt."],
         "Email <b>care@lumora-tv.example</b> or call <b>1-800-555-0166</b>. Attach receipt and a photo of the rear label showing the serial number.")
warranty("Home/Appliances/Fridge/HomeHub_FR-560_warranty_registration.pdf", "HomeHub", "FR-560 Refrigerator",
         [["General parts and labor", "1 year", "Defective parts and labor from the original purchase date."],
          ["Sealed system / compressor", "5 years", "Compressor, condenser, evaporator and refrigerant lines (parts and labor in years 1-5)."]],
         ["Registered serial no.: <b>HH56-2201-30847</b>. Registered owner: Alex Rivera. Purchase date: 2022-01-10.",
          "<b>Exclusions:</b> food loss, damage from power outage, water filters, door bins, cosmetic damage, unauthorized repair.",
          "Claims require receipt, registration and a photo of the serial plate. The serial must match the registration."],
         "Email <b>service@homehub-care.example</b> or call <b>1-800-555-0123</b>.")

# ---------------- protection plan ----------------
pp = [P("3-Year Extended Protection Plan: Terms", H1),
      tbl([["Plan no.", "EPP-3Y-90417733"], ["Plan holder", "Alex Rivera"], ["Covered product", "Nordvik ADW-4820 Dishwasher, serial NV48-2203-1187"],
           ["Purchased", "2024-03-14 (Brightline order BL-2024-0314-55871)"], ["Plan start", "2026-03-14, the day after the 2-year manufacturer warranty ends"],
           ["Plan end", "2029-03-14"], ["Administrator", "Brightline Protection Services"]], [1.6*inch, 5.6*inch], header=False),
      P("1. What the plan covers", H2),
      P("Parts and labor for mechanical and electrical failure from normal household use, including leaks from internal components, drain pump, heater, control board and sensors. Replacement may be offered if repair is not practical."),
      P("2. What the plan does not cover", H2),
      P("Cosmetic damage, racks, filters and gaskets, damage from misuse or improper installation, pre-existing conditions, commercial use, and repairs by anyone not approved by the administrator. Owner repairs beyond the user manual's listed steps void the plan."),
      P("3. Making a claim", H2),
      P("Email <b>protect@brightline-services.example</b> or call <b>1-800-555-0199</b>. Have your plan number, the original receipt, and the product serial number ready. A technician visit is scheduled within 5 business days. No deductible applies."),
      P("4. Cancellation", H2),
      P("Cancel within 30 days for a full refund. After that, a prorated refund applies for unused months, less any claims paid."),
      P("5. Relationship to the manufacturer warranty", H2),
      P("This plan begins when the manufacturer warranty ends and does not overlap with it. While the manufacturer warranty is in force, claims go to the manufacturer.")]
make_pdf("Scans/2024/Brightline_EPP_terms_scan.pdf", "Protection Plan Terms EPP-3Y", BL, pp)

# ---------------- manuals ----------------
LOREM = ["Read all instructions before using the appliance.", "Keep this manual for future reference and for any later owner.",
         "Installation must follow local plumbing and electrical codes.", "Do not allow children to operate the appliance unsupervised.",
         "Use only genuine Nordvik parts and accessories.", "Disconnect power before any cleaning near electrical parts.",
         "Wipe up spills promptly to prevent staining and slipping.", "Check supply hoses for wear once a year."]
def filler(rng, n=3): return [P(" ".join(rng.sample(LOREM, 4))) for _ in range(n)]

def manual(rel, brand, model, title, sections, seed):
    rng = random.Random(seed)
    s = [P(title, ParagraphStyle("t", parent=H1, fontSize=26, spaceBefore=120)), P(f"Model series {model}", H2),
         P("User Manual and Care Guide"), Spacer(1, 40), P(f"{brand}  |  Support: support@nordvik-support.example  |  1-800-555-0188" if brand == "Nordvik" else f"{brand} support"), PageBreak(),
         P("Contents", H1)]
    s += [P(f"{i+1}. {name}") for i, (name, _) in enumerate(sections)] + [PageBreak()]
    for i, (name, content) in enumerate(sections):
        s.append(P(f"{i+1}. {name}", H1)); s += content(rng) if callable(content) else content
        if i < len(sections) - 1: s.append(PageBreak())
    make_pdf(rel, f"{model} User Manual", brand, s)

def dw_sections():
    def safety(r): return [P("Warning: risk of electric shock or injury. Follow these rules."),
        *[P("&bull; " + x) for x in LOREM], P("Do not operate a dishwasher that is leaking. Turn off the water supply and unplug the unit."),
        P("<b>Important:</b> any user repair beyond the steps listed in this manual (for example opening the base, replacing internal parts, or bypassing sensors) will void the manufacturer warranty and any extended protection plan.")]
    def install(r): return [P("Installation overview", H2), *filler(r, 4), tbl([["Connection", "Requirement"], ["Water supply", "Cold or hot, 0.1-0.8 MPa"], ["Drain hose", "Max height 40 in., no kinks"], ["Electrical", "120 V, 60 Hz, 15 A dedicated"]], [2*inch, 4*inch])]
    def controls(r): return [tbl([["Button", "Function"], ["Power", "Turns the unit on or off"], ["Cycle", "Cycles through Auto, Heavy, Eco, Quick"], ["Delay", "Delays start 1-12 hours"], ["Start/Cancel", "Starts a cycle; hold 3 s to cancel and drain"]], [1.5*inch, 5*inch]), *filler(r, 3)]
    def loading(r): return [*filler(r, 3), P("Do not block the spray arms. Load sharp items pointing down. Do not overload the lower rack.")]
    def cycles(r): return [tbl([["Cycle", "Duration", "Water", "Best for"], ["Auto", "120 min", "12 L", "Mixed loads"], ["Heavy", "165 min", "15 L", "Pots and pans"], ["Eco", "210 min", "9 L", "Everyday loads"], ["Quick", "45 min", "10 L", "Light soil"]], [1.2*inch, 1.2*inch, 1*inch, 3*inch]), *filler(r, 2)]
    def maint(r): return [P("Cleaning the filter", H2),
        P("Clean the filter assembly once a month, or when water remains in the tub after a cycle."),
        P("1. Turn off and unplug the dishwasher."), P("2. Remove the lower rack."), P("3. Twist the cylindrical filter counter-clockwise and lift it out."),
        P("4. Separate the coarse filter and the fine mesh filter."), P("5. Rinse under running water with a soft brush. Do not use abrasive pads."),
        P("6. Reassemble and lock the filter with a clockwise twist until it clicks."), P("7. Check the spray arms for blocked holes."),
        P("Run a cleaning cycle with dishwasher cleaner every three months."), *filler(r, 2)]
    def errors(r): return [P("When the control detects a fault it shows a code and stops the cycle."),
        tbl([["Code", "Meaning", "Action"],
             ["E15", "Water detected in the base pan. Leak protection has stopped the unit.", "Turn off water, unplug, tilt unit slightly to drain base pan only if instructed, check door gasket and hose connections. If E15 returns, call service. Do not open the base."],
             ["E24", "Drain fault. Water not draining within 5 minutes.", "Clean the filter, check drain hose for kinks and the sink air gap, restart."],
             ["E09", "Heater or temperature sensor fault.", "Cancel the cycle, power off for 5 minutes, restart. If it repeats, call service."],
             ["E11", "Fill fault. Insufficient water inlet.", "Open the supply valve, check the inlet screen."],
             ["E31", "Door latch not detected.", "Close the door firmly and restart."]], [0.6*inch, 2.6*inch, 4*inch])]
    def trouble(r): return [tbl([["Symptom", "Possible cause", "Solution"],
             ["Water leaks from door", "Dirty gasket, overloading, too much detergent", "Wipe gasket, reload, use less detergent"],
             ["Puddle under unit, E15 shown", "Water in base pan: loose hose, door gasket, or internal leak", "Stop the unit, check hose clamps and gasket. Service call if the leak persists"],
             ["Dishes not clean", "Blocked spray arm or filter", "Clean filter and spray arms"],
             ["Cloudy glassware", "Hard water, too much detergent", "Use rinse aid, reduce detergent"],
             ["Does not start", "Door open or power off", "Close door, check breaker"]], [1.8*inch, 2.5*inch, 2.9*inch]),
        Spacer(1, 8), P("<b>Note:</b> repairs by the user beyond the steps listed above void the warranty. Contact Nordvik Support for service.")]
    def specs(r): return [tbl([["Item", "Value"], ["Capacity", "14 place settings"], ["Noise", "44 dB"], ["Dimensions", "24 x 24 x 34 in."], ["Power", "1800 W"]], [2*inch, 4*inch]), *filler(r, 2)]
    def warr(r): return [P("The product is covered by the Nordvik Limited Warranty supplied separately. Keep your receipt and take a photo of the serial plate inside the door frame."), *filler(r, 2)]
    return [("Safety", safety), ("Installation", install), ("Controls", controls), ("Loading", loading), ("Wash cycles", cycles),
            ("Care and filter cleaning", maint), ("Error codes", errors), ("Troubleshooting", trouble), ("Specifications", specs), ("Service and warranty", warr)]
manual("Manuals/Nordvik_ADW-48xx_UserManual.pdf", "Nordvik", "ADW-48xx", "Nordvik Dishwasher", dw_sections(), 1)
shutil.copy(OUT / "Manuals/Nordvik_ADW-48xx_UserManual.pdf", OUT / "Downloads/ADW-48xx_manual (1).pdf") if (OUT/"Downloads").mkdir(exist_ok=True) is None else None

def wm_sections():
    return [("Safety", lambda r: [*[P("&bull; " + x) for x in LOREM], P("Do not open the door while the drum is turning.")]),
            ("Operation", lambda r: [*filler(r, 4)]),
            ("Care", lambda r: [P("Clean the detergent drawer monthly and wipe the door seal after use."), *filler(r, 2)]),
            ("Error codes", lambda r: [tbl([["Code", "Meaning", "Action"],
                ["F21", "Drain fault: water not draining.", "Pause, power off, clean the drain pump filter behind the lower right panel (have a towel ready), check the drain hose for kinks, restart."],
                ["E03", "Water inlet fault.", "Check the tap and inlet screen."], ["E10", "Door lock fault.", "Close door firmly."]], [0.6*inch, 2.4*inch, 4.2*inch])]),
            ("Troubleshooting", lambda r: [tbl([["Symptom", "Cause", "Solution"], ["Water left in drum, F21", "Blocked pump filter or hose", "Clean pump filter, check hose"],
                ["Loud spin", "Unbalanced load", "Redistribute laundry"], ["Does not start", "Door open", "Close door"]], [1.8*inch, 2.4*inch, 3*inch])]),
            ("Service and warranty", lambda r: [P("See the warranty card supplied. Keep your receipt."), *filler(r, 1)])]
manual("Home/Appliances/Washer/WM-7_manual.pdf", "Nordvik", "WM-7", "Nordvik Washing Machine", wm_sections(), 2)

def fr_sections():
    return [("Safety", lambda r: [*[P("&bull; " + x) for x in LOREM[:6]], P("Unplug before cleaning the condenser coils.")]),
            ("Setup", lambda r: [*filler(r, 3), P("Leave 2 in. clearance behind and at the sides. Wait 4 hours after moving before plugging in.")]),
            ("Controls", lambda r: [tbl([["Setting", "Recommended"], ["Fridge", "37 F"], ["Freezer", "0 F"]], [2*inch, 3*inch]), *filler(r, 2)]),
            ("Troubleshooting: not cooling", lambda r: [P("If the refrigerator is not cooling, try these steps in order."),
                tbl([["Step", "Check", "Action"],
                     ["1", "Power", "Confirm the plug is seated and the outlet works. Check the breaker."],
                     ["2", "Temperature setting", "Set fridge to 37 F, freezer to 0 F. Wait 24 hours."],
                     ["3", "Door seals and airflow", "Close doors fully; do not block vents; remove ice buildup."],
                     ["4", "Condenser coils", "Unplug, vacuum the coils at the base or rear."],
                     ["5", "Condenser fan", "Listen for the fan; if silent, call service."],
                     ["6", "Compressor", "If the compressor does not run or clicks repeatedly, call service. Do not attempt repair."]], [0.6*inch, 2*inch, 4.6*inch]),
                P("Allow 24 hours after any change. Food safety: discard perishables above 40 F for more than 2 hours.")]),
            ("Service and warranty", lambda r: [P("The compressor and sealed system carry an extended warranty. See the warranty card and register your serial number."), *filler(r, 1)])]
manual("Home/Appliances/Fridge/FR-560_owner_manual.pdf", "HomeHub", "FR-560", "HomeHub French Door Refrigerator", fr_sections(), 3)

def rt_sections():
    return [("Setup", lambda r: [*filler(r, 3)]), ("Lights and status", lambda r: [tbl([["LED", "Meaning"], ["Solid green", "Online"], ["Blinking amber", "No internet"], ["Red", "Fault"]], [2*inch, 4*inch])]),
            ("Troubleshooting", lambda r: [P("Power-cycle for 30 seconds. Hold reset for 10 seconds to restore factory settings."), *filler(r, 2)])]
manual("Manuals/Zentro_AX3000_Router_Manual.pdf", "Zentro", "AX3000", "Zentro Wi-Fi Router", rt_sections(), 4)

# ---------------- noise PDFs ----------------
make_pdf("Documents/School/Elementary_Newsletter_Oct2026.pdf", "Newsletter", "Maple Hollow Elementary",
         [P("Fall Newsletter, October 2026", H1), P("Dear families, the autumn book fair runs 4-8 November in the library. Picture retake day is 12 November."),
          tbl([["Date", "Event"], ["Nov 4-8", "Book fair"], ["Nov 12", "Picture retakes"], ["Nov 26-28", "No school"]], [1.5*inch, 5*inch]),
          P("Volunteers are welcome at the front office.")])
make_pdf("Downloads/utility_bill_oct.pdf", "Statement", "Valley Power & Water",
         [P("Monthly Statement", H1), P(f"Account holder: {CUST[0]}, {CUST[1]}"),
          tbl([["Service", "Usage", "Charge"], ["Electric", "612 kWh", "$91.80"], ["Water", "8 kgal", "$44.10"], ["Total due", "", "$135.90"]], [2.5*inch, 2*inch, 2*inch]),
          P("Due date: 2026-11-10")])
make_pdf("Documents/Misc/recipe_collection.pdf", "Recipes", "Family Kitchen",
         [P("Family Recipes", H1), *[P(f"Recipe {i}: combine ingredients and cook until done.") for i in range(1, 8)]])

# ---------------- photos ----------------
rng = np.random.default_rng(SEED); prng = random.Random(SEED)
def font(sz):
    for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", "/usr/share/fonts/dejavu/DejaVuSansMono.ttf"):
        try: return ImageFont.truetype(p, sz)
        except OSError: pass
    return ImageFont.load_default(sz)

def phone_photo(rel, lines, size=(1200, 1600), angle=-3.0, plate=False):
    W, H = size
    bg = Image.new("RGB", (W + 400, H + 400), (92, 84, 74))  # table surface
    paper = Image.new("RGB", (W - 200, H - 200), (244, 241, 232) if not plate else (196, 198, 202))
    d = ImageDraw.Draw(paper); y = 70
    for txt, sz, bold in lines:
        d.text((60, y), txt, font=font(sz), fill=(30, 30, 30) if not plate else (20, 20, 20)); y += int(sz * 1.5)
    paper = paper.rotate(angle, expand=True, fillcolor=(92, 84, 74), resample=Image.BICUBIC)
    bg.paste(paper, ((bg.width - paper.width) // 2, (bg.height - paper.height) // 2))
    arr = np.asarray(bg).astype(np.float32)
    yy, xx = np.mgrid[0:arr.shape[0], 0:arr.shape[1]]
    arr *= (1.0 - 0.25 * (xx / arr.shape[1]))[..., None]  # lighting gradient
    arr += rng.normal(0, 9, arr.shape)
    img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8))
    img = img.resize((img.width * 3 // 4, img.height * 3 // 4))
    p = OUT / rel; p.parent.mkdir(parents=True, exist_ok=True); img.save(p, quality=82)

phone_photo("Photos/Phone/2023-06/IMG_20230602_181404.jpg", [
    ("HOMEHUB APPLIANCES", 44, 1), ("77 Harbor Road, Port Alder OR", 28, 0), ("", 28, 0),
    ("Date: 06/02/2023   Order HH-230602-1187", 28, 0), ("Cust: Alex Rivera", 28, 0), ("-" * 40, 28, 0),
    ("Nordvik WM-7 Front Load Washer", 28, 0), ("  SN NV7-2305-60912        $899.00", 28, 0),
    ("Delivery                     $59.00", 28, 0), ("-" * 40, 28, 0), ("TOTAL                       $958.00", 32, 1),
    ("Paid: CARD ****4417", 28, 0), ("Warranty: see manufacturer card", 24, 0)], angle=-2.6)
phone_photo("Photos/Phone/2022-01/IMG_20220115_101233.jpg", [
    ("HomeHub", 40, 1), ("MODEL: FR-560", 36, 0), ("SERIAL: HH56-2201-30647", 36, 0), ("VOLTS 115V  60Hz  AMPS 6.5", 30, 0),
    ("REFRIGERANT R600a  38 g", 30, 0), ("MADE FOR HomeHub Appliances", 26, 0), ("Compressor: sealed system", 26, 0)],
    size=(1200, 800), angle=3.4, plate=True)
phone_photo("Photos/Phone/2024-03/IMG_20240316_190455.jpg", [
    ("NORDVIK", 44, 1), ("MODEL: ADW-4820", 36, 0), ("SERIAL: NV48-2203-1187", 36, 0), ("120V 60Hz 15A  1800W", 30, 0),
    ("MFD 2023-12", 28, 0)], size=(1200, 800), angle=-4.1, plate=True)

def scenic(rel, seed, size=(1600, 1200)):
    r = np.random.default_rng(seed); W, H = size
    y = np.linspace(0, 1, H)[:, None, None]
    c1, c2 = r.integers(40, 220, 3), r.integers(40, 220, 3)
    arr = c1 * (1 - y) + c2 * y + r.normal(0, 6, (H, W, 3))
    img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)); d = ImageDraw.Draw(img)
    for _ in range(6):
        x0, y0 = int(r.integers(0, W)), int(r.integers(H // 3, H)); rad = int(r.integers(60, 260))
        d.ellipse([x0 - rad, y0 - rad, x0 + rad, y0 + rad], fill=tuple(int(v) for v in r.integers(30, 230, 3)))
    p = OUT / rel; p.parent.mkdir(parents=True, exist_ok=True); img.filter(ImageFilter.GaussianBlur(3)).save(p, quality=80)
for i, rel in enumerate(["Photos/Phone/2024-03/IMG_20240309_142210.jpg", "Photos/Phone/2024-03/IMG_20240322_093001.jpg",
                         "Photos/Phone/2023-06/IMG_20230610_201145.jpg", "Photos/Vacation_2025/DSC_0041.jpg",
                         "Photos/Vacation_2025/DSC_0042.jpg", "Downloads/wallpaper_final.jpg"]):
    scenic(rel, SEED + i)

n = sum(1 for f in OUT.rglob("*") if f.is_file())
print(n, "files,", round(sum(f.stat().st_size for f in OUT.rglob("*") if f.is_file()) / 1e6, 2), "MB")
