from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.colors import HexColor, white

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output/pdf/japanese-hobby-items-catalogue.pdf"
W, H = landscape(A4)
M = 30
RED = HexColor("#d71920")
BLUE = HexColor("#16324a")
INK = HexColor("#22292e")
MUTED = HexColor("#6b747a")
LINE = HexColor("#d8dde1")
PAPER = HexColor("#f2f3f1")
SOURCE = "https://www.tamiya.com/english/products/archive.htm"

CATEGORIES = [
    ("Car & motorcycle models", [
        "1/24 Sports Car Series", "1/20 Grand Prix Collection", "1/12 Big Scale Racing Car",
        "Car detail-up parts", "1/24 Masterwork Collection", "Clic Loc car models",
        "1/12 Motorcycle Series", "1/6 Big Scale Motorcycle", "Motorcycle detail-up parts",
        "Motorcycle Masterwork Collection", "Racing car display model", "Classic vehicle model",
    ]),
    ("Military, aircraft & ships", [
        "1/35 Military Miniature", "1/48 Military Miniature", "1/16 World Figure Series",
        "Military detail-up parts", "1/32 Aircraft Series", "1/48 Aircraft Series",
        "1/72 War Bird Collection", "Aircraft detail-up parts", "1/350 Ship Series",
        "1/700 Water Line Series", "Ship detail-up parts", "Dinosaur Diorama Series",
    ]),
    ("R/C models & parts", [
        "Electric R/C Car Series", "Limited Edition R/C Model", "TamTech-Gear kit",
        "Star-Unit Series", "R/C Tractor Truck Series", "R/C Tank Series",
        "R/C spare parts", "R/C hop-up options", "R/C tractor truck parts",
        "R/C systems", "Batteries & chargers", "TRF racing parts",
    ]),
    ("Mini 4WD", [
        "Wild Mini 4WD Series", "Racing Mini 4WD Series", "Fully Cowled Mini 4WD",
        "Mini 4WD REV", "Mini 4WD PRO", "Mini 4WD starter set",
        "Mini 4WD batteries", "Grade-up parts", "Limited parts",
        "AO replacement parts", "Mini 4WD circuit", "Mini 4WD setup tools",
    ]),
    ("Construction & robotics", [
        "Educational construction set", "Educational construction unit", "Construction parts",
        "Craft construction kit", "Technicraft Series", "Elecraft Series",
        "Robocraft Series", "Solar mechanics", "Solar miniature",
        "Programming construction", "Gearbox & motor unit", "Mechanical experiment kit",
    ]),
    ("Tools, paints & display", [
        "Modeling side cutter", "Modeling knife", "Tweezers & pliers",
        "Screwdriver set", "Drill & engraving tools", "Modeling files",
        "Work stand & loupe", "Airbrush system", "Acrylic paint mini",
        "Enamel paint", "Color spray", "Display case & stand",
    ]),
]


def products():
    rows = []
    for category, names in CATEGORIES:
        for name in names:
            rows.append({"category": category, "name": name})
    for i, row in enumerate(rows, start=1):
        row["code"] = f"HB-{i:03d}"
    return rows


PRODUCTS = products()


def header(c, title, page):
    c.setFillColor(BLUE)
    c.rect(0, H - 46, W, 46, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 15)
    c.drawString(M, H - 29, "GUINEA PIG TRADING")
    c.setFont("Helvetica", 7)
    c.drawRightString(W - M, H - 26, "JAPANESE HOBBY ITEMS  /  DISCOVERY GUIDE")
    c.setFillColor(RED)
    c.rect(0, H - 51, W, 5, fill=1, stroke=0)
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(M, H - 82, title.upper())
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 8)
    c.drawRightString(W - M, 18, f"PAGE {page}  |  GUINEA PIG TRADING")


def icon(c, category, x, y, w, h):
    cx, cy = x + w / 2, y + h / 2
    c.setStrokeColor(BLUE)
    c.setFillColor(PAPER)
    c.rect(x, y, w, h, fill=1, stroke=0)
    c.setLineWidth(3)
    if "Car" in category:
        c.roundRect(cx - 42, cy - 13, 84, 28, 8, fill=0, stroke=1)
        c.line(cx - 25, cy + 15, cx - 10, cy + 32)
        c.line(cx - 10, cy + 32, cx + 23, cy + 32)
        c.line(cx + 23, cy + 32, cx + 39, cy + 15)
        c.circle(cx - 26, cy - 15, 9, fill=0, stroke=1)
        c.circle(cx + 27, cy - 15, 9, fill=0, stroke=1)
    elif "Military" in category:
        c.line(cx - 50, cy - 12, cx + 42, cy - 12)
        c.line(cx - 20, cy + 4, cx + 48, cy + 28)
        c.line(cx - 20, cy + 4, cx - 5, cy + 34)
        c.line(cx - 5, cy + 34, cx + 8, cy + 7)
    elif "R/C" in category:
        c.roundRect(cx - 32, cy - 35, 64, 70, 8, fill=0, stroke=1)
        c.circle(cx - 16, cy - 2, 10, fill=0, stroke=1)
        c.circle(cx + 16, cy - 2, 10, fill=0, stroke=1)
        c.line(cx, cy + 35, cx + 20, cy + 55)
    elif "Mini" in category:
        c.roundRect(cx - 48, cy - 14, 96, 28, 8, fill=0, stroke=1)
        c.circle(cx - 31, cy - 17, 8, fill=0, stroke=1)
        c.circle(cx + 31, cy - 17, 8, fill=0, stroke=1)
        c.line(cx - 52, cy + 22, cx + 52, cy + 22)
    elif "Construction" in category:
        c.circle(cx, cy, 35, fill=0, stroke=1)
        c.circle(cx, cy, 12, fill=0, stroke=1)
        for dx, dy in [(0, 47), (0, -47), (47, 0), (-47, 0)]:
            c.line(cx + dx * .75, cy + dy * .75, cx + dx, cy + dy)
    else:
        c.line(cx - 40, cy - 35, cx + 35, cy + 40)
        c.circle(cx - 40, cy - 35, 11, fill=0, stroke=1)
        c.line(cx + 10, cy - 40, cx + 45, cy - 5)
        c.line(cx + 45, cy - 5, cx + 23, cy + 17)


def cover(c):
    c.setFillColor(BLUE)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(RED)
    c.rect(0, H - 17, W, 17, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 15)
    c.drawString(55, H - 65, "GUINEA PIG TRADING")
    c.setFont("Helvetica-Bold", 48)
    c.drawString(55, H - 155, "JAPANESE")
    c.drawString(55, H - 208, "HOBBY ITEMS")
    c.setFillColor(RED)
    c.drawString(55, H - 261, "DISCOVERY GUIDE")
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(59, H - 310, "72 sourcing categories")
    c.setFont("Helvetica", 11)
    c.drawString(59, H - 336, "Model kits  /  R/C  /  Mini 4WD  /  Construction  /  Tools & paints")
    c.setFillColor(RED)
    c.circle(W - 180, H / 2, 135, fill=1, stroke=0)
    c.setStrokeColor(white)
    c.setLineWidth(6)
    c.roundRect(W - 255, H / 2 - 28, 150, 55, 15, fill=0, stroke=1)
    c.circle(W - 220, H / 2 - 34, 14, fill=0, stroke=1)
    c.circle(W - 140, H / 2 - 34, 14, fill=0, stroke=1)
    c.setFont("Helvetica", 8)
    c.drawString(59, 48, "Category guide based on official Tamiya product categories. It is not a stock or price catalogue.")
    c.showPage()


def category_page(c, category, items, page):
    header(c, category, page)
    c.setFillColor(white)
    c.setStrokeColor(LINE)
    c.roundRect(M, 75, 230, H - 180, 5, fill=1, stroke=1)
    icon(c, category, M + 12, 87, 206, H - 204)
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 8)
    c.drawString(M + 15, 58, "One category illustration. No repeated product pictures.")
    x = 285
    y = H - 115
    widths = [72, 355, 110]
    c.setFillColor(BLUE)
    c.rect(x, y - 20, sum(widths), 25, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x + 8, y - 11, "HB CODE")
    c.drawString(x + widths[0] + 8, y - 11, "HOBBY CATEGORY")
    c.drawString(x + widths[0] + widths[1] + 8, y - 11, "TYPE")
    y -= 28
    for i, product in enumerate(items):
        c.setFillColor(PAPER if i % 2 == 0 else white)
        c.rect(x, y - 20, sum(widths), 25, fill=1, stroke=0)
        c.setFillColor(RED)
        c.setFont("Helvetica-Bold", 8)
        c.drawString(x + 8, y - 12, product["code"])
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 8.5)
        c.drawString(x + widths[0] + 8, y - 12, product["name"][:48])
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 7.5)
        c.drawString(x + widths[0] + widths[1] + 8, y - 12, "Enquiry")
        c.linkURL(SOURCE, (x, y - 20, x + sum(widths), y + 5), relative=0)
        y -= 28
    c.showPage()


def notes(c, page):
    header(c, "Source & catalogue notes", page)
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(M, H - 125, "Official reference")
    c.setFillColor(BLUE)
    c.setFont("Helvetica", 10)
    c.drawString(M, H - 150, SOURCE)
    c.linkURL(SOURCE, (M, H - 157, W - M, H - 138), relative=0)
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(M, H - 205, "How to use this catalogue")
    notes = [
        "Choose a category code, then share the intended customer, budget, quantity and destination market.",
        "HB-001 to HB-072 are Guinea Pig Trading enquiry codes, not official maker item numbers.",
        "The icons are category illustrations, not photographs of a specific product.",
        "Exact kits, versions, packaging, availability, prices and resale conditions are checked before quotation.",
        "Some Tamiya categories or products may be discontinued or unavailable in certain countries.",
    ]
    y = H - 235
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 10)
    for note in notes:
        c.drawString(M + 12, y, "- " + note)
        y -= 25
    c.setFillColor(BLUE)
    c.roundRect(M, 55, W - 2 * M, 72, 4, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(M + 20, 98, "Ask for a current hobby shortlist")
    c.setFont("Helvetica", 9)
    c.drawString(M + 20, 77, "Send the HB code and I will research current products that fit the request.")
    c.showPage()


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUT), pagesize=landscape(A4), pageCompression=1)
    c.setTitle("Japanese Hobby Items Discovery Guide - Guinea Pig Trading")
    c.setAuthor("Guinea Pig Trading")
    cover(c)
    page = 2
    offset = 0
    for category, names in CATEGORIES:
        category_page(c, category, PRODUCTS[offset:offset + len(names)], page)
        page += 1
        offset += len(names)
    notes(c, page)
    c.save()
    print(OUT)


if __name__ == "__main__":
    main()
