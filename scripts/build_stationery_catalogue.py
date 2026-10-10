from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.colors import HexColor, white
from reportlab.lib.utils import ImageReader
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output/pdf/japanese-stationery-catalogue.pdf"
ASSETS = ROOT / "assets/catalog"

W, H = landscape(A4)
M = 30
RED = HexColor("#d71920")
NAVY = HexColor("#16324a")
INK = HexColor("#20262b")
MUTED = HexColor("#66717a")
LINE = HexColor("#d8dde1")
PAPER = HexColor("#f4f4f1")

sources = {
    "Zebra": "https://www.zebra.co.jp/pro/mildliner/",
    "PLUS": "https://bungu.plus.co.jp/product/deco/decoration_tape/decorush/",
    "MD PAPER": "https://md.midori-japan.co.jp/en/products/mdnote/",
    "Delfonics": "https://shop.delfonics.com/c/brands/original/cat701",
    "Tombow": "https://www.tombow.com/en/products/mono_graph/",
    "Kokuyo": "https://www.kokuyo.com/en/stationery/series/neocritz/",
}

products = [
    # Pens and markers
    ("GP-001", "Mildliner 5-color set", "Fluorescent", "Zebra", "zebra-mildliner.jpg"),
    ("GP-002", "Mildliner 5-color set", "Cool", "Zebra", "zebra-mildliner.jpg"),
    ("GP-003", "Mildliner 5-color set", "Warm", "Zebra", "zebra-mildliner.jpg"),
    ("GP-004", "Mildliner 5-color set", "Friendly", "Zebra", "zebra-mildliner.jpg"),
    ("GP-005", "Mildliner 5-color set", "Natural", "Zebra", "zebra-mildliner.jpg"),
    ("GP-006", "Mildliner 5-color set", "Neutral", "Zebra", "zebra-mildliner.jpg"),
    ("GP-007", "MONO graph pencil", "Standard", "Tombow", "tombow-mono-graph.png"),
    ("GP-008", "MONO graph pencil", "Fine", "Tombow", "tombow-mono-graph.png"),
    ("GP-009", "MONO graph pencil", "Lite", "Tombow", "tombow-mono-graph.png"),
    ("GP-010", "MONO graph pencil", "Grip", "Tombow", "tombow-mono-graph.png"),
    # Paper and notebooks
    ("GP-011", "MD Notebook A5", "Blank", "MD PAPER", "md-notebook.webp"),
    ("GP-012", "MD Notebook A5", "Ruled", "MD PAPER", "md-notebook.webp"),
    ("GP-013", "MD Notebook A5", "Grid", "MD PAPER", "md-notebook.webp"),
    ("GP-014", "MD Notebook A6", "Blank", "MD PAPER", "md-notebook.webp"),
    ("GP-015", "MD Notebook A6", "Ruled", "MD PAPER", "md-notebook.webp"),
    ("GP-016", "Rollbahn Pocket Memo", "M size", "Delfonics", "delfonics-rollbahn.jpg"),
    ("GP-017", "Rollbahn Pocket Memo", "L size", "Delfonics", "delfonics-rollbahn.jpg"),
    ("GP-018", "Rollbahn Pocket Memo", "A5 size", "Delfonics", "delfonics-rollbahn.jpg"),
    ("GP-019", "LIFE Noble Note", "Notebook", "Delfonics", "delfonics-life-noble.jpg"),
    ("GP-020", "Artist-cover ring memo", "Assorted cover", "Delfonics", "delfonics-ring-memo.jpg"),
    # Decoration and desk accessories
    ("GP-021", "Deco Rush", "Regular motif", "PLUS", "plus-deco-rush.jpg"),
    ("GP-022", "Deco Rush", "Wide motif", "PLUS", "plus-deco-rush.jpg"),
    ("GP-023", "Deco Rush", "Refill", "PLUS", "plus-deco-rush.jpg"),
    ("GP-024", "Deco Rush", "Assorted motif", "PLUS", "plus-deco-rush.jpg"),
    ("GP-025", "Rollbahn correction tape", "Desk accessory", "Delfonics", "delfonics-correction-tape.jpg"),
    ("GP-026", "Rollbahn zip organizer", "Black", "Delfonics", "delfonics-zip-organizer.jpg"),
    ("GP-027", "NeoCritz pencil case", "Standard", "Kokuyo", "kokuyo-neocritz.webp"),
    ("GP-028", "NeoCritz pencil case", "Flat", "Kokuyo", "kokuyo-neocritz.webp"),
    ("GP-029", "NeoCritz pencil case", "Mini", "Kokuyo", "kokuyo-neocritz.webp"),
    ("GP-030", "NeoCritz pencil case", "Assorted color", "Kokuyo", "kokuyo-neocritz.webp"),
]

sections = [
    ("PENS & MARKERS", products[:10]),
    ("NOTEBOOKS & PAPER", products[10:20]),
    ("DECORATION & DESK ACCESSORIES", products[20:]),
]


def fit_image(c, path, x, y, w, h):
    with Image.open(path) as im:
        iw, ih = im.size
    scale = min(w / iw, h / ih)
    dw, dh = iw * scale, ih * scale
    c.drawImage(ImageReader(path), x + (w - dw) / 2, y + (h - dh) / 2, dw, dh, mask="auto")


def header(c, section, page_no):
    c.setFillColor(NAVY)
    c.rect(0, H - 46, W, 46, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 15)
    c.drawString(M, H - 29, "GUINEA PIG TRADING")
    c.setFont("Helvetica", 7)
    c.drawRightString(W - M, H - 26, "JAPANESE STATIONERY CATALOGUE  /  2026")
    c.setFillColor(RED)
    c.rect(0, H - 51, W, 5, fill=1, stroke=0)
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(M, H - 81, section)
    c.setFont("Helvetica", 8)
    c.setFillColor(MUTED)
    c.drawRightString(W - M, 18, f"PAGE {page_no}  |  GUINEAPIG TRADING")


def card(c, p, x, y, w, h):
    code, name, variant, brand, filename = p
    c.setFillColor(white)
    c.setStrokeColor(LINE)
    c.roundRect(x, y, w, h, 3, fill=1, stroke=1)
    photo_h = h - 57
    c.setFillColor(PAPER)
    c.rect(x + 1, y + h - photo_h - 1, w - 2, photo_h, fill=1, stroke=0)
    fit_image(c, ASSETS / filename, x + 8, y + h - photo_h + 6, w - 16, photo_h - 13)
    c.setFillColor(RED)
    c.setFont("Helvetica-Bold", 7.5)
    c.drawString(x + 8, y + 43, code)
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 9.5)
    c.drawString(x + 8, y + 29, name[:34])
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 7.5)
    c.drawString(x + 8, y + 16, f"{variant}  /  {brand}")
    c.linkURL(sources[brand], (x, y, x + w, y + h), relative=0)


def draw_section(c, title, items, page_no):
    header(c, title, page_no)
    cols, rows = 5, 2
    gap = 10
    top = H - 96
    bottom = 34
    cw = (W - 2 * M - gap * (cols - 1)) / cols
    ch = (top - bottom - gap) / rows
    for i, p in enumerate(items):
        col, row = i % cols, i // cols
        x = M + col * (cw + gap)
        y = top - (row + 1) * ch - row * gap
        card(c, p, x, y, cw, ch)
    c.showPage()


def source_page(c, page_no):
    header(c, "PRODUCT SOURCES & NOTES", page_no)
    y = H - 112
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(M, y, "Official maker / official shop pages")
    y -= 24
    for brand, url in sources.items():
        c.setFillColor(RED)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(M, y, brand)
        c.setFillColor(NAVY)
        c.setFont("Helvetica", 8)
        c.drawString(M + 90, y, url)
        c.linkURL(url, (M + 88, y - 4, W - M, y + 8), relative=0)
        y -= 22
    y -= 8
    c.setStrokeColor(LINE)
    c.line(M, y, W - M, y)
    y -= 28
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(M, y, "Catalogue notes")
    notes = [
        "Product photographs are from the official maker or official shop pages listed above.",
        "Catalogue codes GP-001 to GP-030 are Guinea Pig Trading reference codes, not maker item numbers.",
        "Models, colors, packaging, availability, wholesale access and prices must be checked before quotation.",
        "Images may show a product family; the exact requested variant will be confirmed before purchase.",
    ]
    y -= 23
    c.setFont("Helvetica", 9)
    c.setFillColor(MUTED)
    for note in notes:
        c.drawString(M + 12, y, "- " + note)
        y -= 19
    c.setFillColor(NAVY)
    c.roundRect(M, 50, W - 2 * M, 64, 3, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 15)
    c.drawString(M + 18, 89, "Request a sourcing check")
    c.setFont("Helvetica", 9)
    c.drawString(M + 18, 71, "Send the GP code, preferred variant, quantity and destination market through the website contact form.")
    c.showPage()


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUT), pagesize=landscape(A4), pageCompression=1)
    c.setTitle("Japanese Stationery Catalogue - Guinea Pig Trading")
    c.setAuthor("Guinea Pig Trading")
    for page_no, (title, items) in enumerate(sections, start=1):
        draw_section(c, title, items, page_no)
    source_page(c, 4)
    c.save()
    print(OUT)


if __name__ == "__main__":
    main()
