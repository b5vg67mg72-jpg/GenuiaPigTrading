from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.colors import HexColor, white
from reportlab.lib.utils import ImageReader
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output/pdf/customer-stationery-lookbook.pdf"
ASSETS = ROOT / "assets/catalog"
W, H = landscape(A4)
CREAM = HexColor("#f7f1e6")
INK = HexColor("#152a31")
CORAL = HexColor("#df6a55")
MINT = HexColor("#8ab7aa")
SUN = HexColor("#e8b95c")
MUTED = HexColor("#68777a")

FEATURES = [
    ("Color that feels easy", "Zebra Mildliner", "zebra-mildliner.jpg", CORAL,
     "Soft colors, simple sets and an instantly understandable gift. A natural fit for study, journaling and creative displays.",
     ["Easy color story", "Compact shelf footprint", "Strong repeat-purchase potential"]),
    ("A small tool with character", "Tombow MONO Graph", "tombow-mono-graph.png", MINT,
     "A familiar pencil made more interesting through useful Japanese design details and a recognizable MONO look.",
     ["Useful everyday item", "Good demonstration product", "Multiple model and color enquiries"]),
    ("Paper people remember", "MD Notebook", "md-notebook.webp", SUN,
     "Quiet design, tactile paper and a calm presentation. It works as a premium notebook without feeling formal.",
     ["Minimal shelf presence", "Paper-focused story", "Multiple sizes and page formats"]),
    ("Bright, practical, collectable", "Delfonics Rollbahn", "delfonics-rollbahn.jpg", CORAL,
     "A bold cover, strong ring binding and everyday usefulness make Rollbahn easy to merchandise by size and color.",
     ["Recognizable Japanese design", "Color-led display", "Gift and personal-use appeal"]),
    ("A little fun for every page", "PLUS Deco Rush", "plus-deco-rush.jpg", MINT,
     "A compact decoration tool for planners, cards and notebooks. Motif-led assortments invite customers to choose more than one.",
     ["Impulse-friendly format", "Seasonal motif opportunities", "Easy add-on purchase"]),
    ("Desk storage that transforms", "Kokuyo NeoCritz", "kokuyo-neocritz.webp", SUN,
     "A pencil case that becomes a standing holder. The transformation is simple, useful and easy to show in store.",
     ["Clear product demonstration", "Useful for school and work", "Color and size options"]),
]


def fit_image(c, filename, x, y, w, h):
    path = ASSETS / filename
    with Image.open(path) as im:
        iw, ih = im.size
    scale = min(w / iw, h / ih)
    dw, dh = iw * scale, ih * scale
    c.drawImage(ImageReader(path), x + (w - dw) / 2, y + (h - dh) / 2, dw, dh, mask="auto")


def wrap(c, text, x, y, max_width, leading, font="Helvetica", size=11, color=MUTED):
    words = text.split()
    lines, line = [], ""
    for word in words:
        candidate = (line + " " + word).strip()
        if c.stringWidth(candidate, font, size) <= max_width:
            line = candidate
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    c.setFillColor(color)
    c.setFont(font, size)
    for current in lines:
        c.drawString(x, y, current)
        y -= leading
    return y


def footer(c, page):
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 7.5)
    c.drawString(36, 20, "GUINEA PIG TRADING  /  JAPAN SOURCING")
    c.drawRightString(W - 36, 20, f"LOOKBOOK  /  {page}")


def cover(c):
    c.setFillColor(INK)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(CORAL)
    c.circle(W - 95, H - 90, 150, fill=1, stroke=0)
    c.setFillColor(SUN)
    c.circle(W - 270, 75, 95, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(54, H - 64, "GUINEA PIG TRADING")
    c.setFont("Helvetica-Bold", 48)
    c.drawString(54, H - 160, "Small things.")
    c.drawString(54, H - 214, "Good feeling.")
    c.setFillColor(CREAM)
    c.setFont("Helvetica", 17)
    c.drawString(58, H - 258, "Japanese stationery for memorable retail displays.")
    c.setFillColor(white)
    c.roundRect(W - 350, 125, 255, 255, 8, fill=1, stroke=0)
    fit_image(c, "delfonics-rollbahn.jpg", W - 325, 150, 205, 205)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(58, 62, "CUSTOMER LOOKBOOK  /  2026")
    c.showPage()


def intro(c):
    c.setFillColor(CREAM)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 35)
    c.drawString(50, H - 90, "A shelf customers want to explore.")
    wrap(c, "The strongest stationery displays mix useful products with color, texture and a small moment of surprise. This lookbook shows six product families that can work together without making the shelf feel crowded.", 52, H - 130, 470, 18, size=12, color=MUTED)
    cards = [("COLOR", "Give customers an easy first choice.", CORAL), ("USE", "Make every product simple to understand.", MINT), ("DISCOVERY", "Leave room for one delightful detail.", SUN)]
    for i, (label, body, color) in enumerate(cards):
        x = 52 + i * 250
        c.setFillColor(white)
        c.roundRect(x, 105, 220, 190, 8, fill=1, stroke=0)
        c.setFillColor(color)
        c.circle(x + 36, 250, 18, fill=1, stroke=0)
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(x + 22, 210, label)
        wrap(c, body, x + 22, 180, 175, 18, font="Helvetica-Bold", size=14, color=INK)
    footer(c, 2)
    c.showPage()


def feature_page(c, feature, page):
    headline, name, image, accent, body, bullets = feature
    c.setFillColor(CREAM)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(accent)
    c.rect(0, 0, 24, H, fill=1, stroke=0)
    c.setFillColor(white)
    c.roundRect(50, 72, 350, H - 112, 10, fill=1, stroke=0)
    fit_image(c, image, 78, 102, 294, H - 172)
    c.setFillColor(accent)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(440, H - 82, name.upper())
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 27)
    c.drawString(438, H - 127, headline)
    y = wrap(c, body, 440, H - 170, 335, 18, size=11.5, color=MUTED)
    y -= 16
    for bullet in bullets:
        c.setFillColor(accent)
        c.circle(448, y + 3, 4, fill=1, stroke=0)
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(462, y, bullet)
        y -= 30
    c.setFillColor(INK)
    c.setFont("Helvetica", 8)
    c.drawString(440, 78, "Ask for current colors, formats, quantities and sourcing availability.")
    footer(c, page)
    c.showPage()


def closing(c):
    c.setFillColor(INK)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(CORAL)
    c.rect(0, H - 16, W, 16, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 36)
    c.drawString(54, H - 110, "Build a stationery mix")
    c.drawString(54, H - 153, "that feels like your shop.")
    c.setFillColor(CREAM)
    c.setFont("Helvetica", 13)
    c.drawString(58, H - 193, "Choose references from the 200-item catalogue and request a current sourcing check.")
    steps = ["1. Share the GP item codes", "2. Add quantity and budget", "3. Confirm current options"]
    for i, step in enumerate(steps):
        x = 58 + i * 245
        c.setFillColor([CORAL, MINT, SUN][i])
        c.roundRect(x, 160, 215, 90, 7, fill=1, stroke=0)
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(x + 16, 200, step)
    c.setFillColor(white)
    c.setFont("Helvetica", 8)
    c.drawString(58, 70, "Photographs are from official maker or official shop pages. Availability and terms are checked before quotation.")
    c.showPage()


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUT), pagesize=landscape(A4), pageCompression=1)
    c.setTitle("Customer Stationery Lookbook - Guinea Pig Trading")
    c.setAuthor("Guinea Pig Trading")
    cover(c)
    intro(c)
    for page, feature in enumerate(FEATURES, start=3):
        feature_page(c, feature, page)
    closing(c)
    c.save()
    print(OUT)


if __name__ == "__main__":
    main()
