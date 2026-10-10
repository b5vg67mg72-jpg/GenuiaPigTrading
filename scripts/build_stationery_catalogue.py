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

SOURCES = {
    "Zebra": "https://www.zebra.co.jp/pro/mildliner/",
    "Tombow": "https://www.tombow.com/en/products/mono_graph/",
    "MD PAPER": "https://md.midori-japan.co.jp/en/products/mdnote/",
    "Delfonics": "https://shop.delfonics.com/c/brands/original/cat701",
    "PLUS": "https://bungu.plus.co.jp/product/deco/decoration_tape/decorush/",
    "Kokuyo": "https://www.kokuyo.com/en/stationery/series/neocritz/",
}


def build_products():
    rows = []

    def add(kind, name, option, brand, image):
        rows.append({"kind": kind, "name": name, "option": option, "brand": brand, "image": image})

    palettes = ["Fluorescent", "Cool", "Warm", "Friendly", "Natural", "Neutral", "Gentle", "Refresh"]
    formats = ["5-color set", "Single marker", "Brush set", "Assorted pack", "Gift set"]
    for palette in palettes:
        for product_format in formats:
            add("Highlighters & markers", f"Mildliner {product_format}", palette, "Zebra", "zebra-mildliner.jpg")

    models = ["Standard", "Fine", "Lite", "Grip", "Clear", "Pastel"]
    colors = ["Black", "Blue", "White", "Pink", "Assorted color"]
    for model in models:
        for color in colors:
            add("Mechanical pencils", f"MONO graph {model}", color, "Tombow", "tombow-mono-graph.png")

    md_sizes = ["A5", "A6", "B6 Slim", "A5 Cotton", "A5 Light"]
    md_formats = ["Blank", "Ruled", "Grid", "Dot grid", "Journal", "3-book pack"]
    for size in md_sizes:
        for paper_format in md_formats:
            add("Notebooks & memo", f"MD Notebook {size}", paper_format, "MD PAPER", "md-notebook.webp")

    rollbahn_sizes = ["Mini", "M", "L", "A5", "Slim", "Landscape"]
    covers = ["Orange", "Classic color", "Pastel color", "Assorted cover", "Limited cover"]
    for size in rollbahn_sizes:
        for cover in covers:
            add("Notebooks & memo", f"Rollbahn Pocket Memo {size}", cover, "Delfonics", "delfonics-rollbahn.jpg")

    motifs = [
        "Planner", "Animal", "Flower", "Food", "Seasonal", "Cafe", "Travel", "Weather", "Study", "Work",
        "Home", "Birthday", "Holiday", "Music", "Books", "Stars", "Nature", "Cats", "Dogs", "Birds",
        "Fruit", "Sweets", "Bread", "Drinks", "Cooking", "Shopping", "Health", "Exercise", "School", "Family",
        "Numbers", "Letters", "Checks", "Lines", "Frames", "Icons", "Messages", "Japanese", "Mini pattern", "Assorted",
    ]
    for motif in motifs:
        add("Decoration tape", f"Deco Rush {motif}", "Motif series", "PLUS", "plus-deco-rush.jpg")

    for style in ["Standard", "Flat", "Mini", "Wide", "Standing"]:
        for color in ["Black", "Blue", "Pink", "Assorted color"]:
            add("Pencil cases", f"NeoCritz {style}", color, "Kokuyo", "kokuyo-neocritz.webp")

    extras = [
        ("Rollbahn correction tape", "Blue", "delfonics-correction-tape.jpg"),
        ("Rollbahn correction tape", "Assorted color", "delfonics-correction-tape.jpg"),
        ("Rollbahn correction tape", "Refill enquiry", "delfonics-correction-tape.jpg"),
        ("Rollbahn zip organizer", "Black - compact", "delfonics-zip-organizer.jpg"),
        ("Rollbahn zip organizer", "Black - standard", "delfonics-zip-organizer.jpg"),
        ("Rollbahn zip organizer", "Black - large", "delfonics-zip-organizer.jpg"),
        ("LIFE Noble Note", "Ruled", "delfonics-life-noble.jpg"),
        ("LIFE Noble Note", "Grid", "delfonics-life-noble.jpg"),
        ("Artist-cover ring memo", "Cover option A", "delfonics-ring-memo.jpg"),
        ("Artist-cover ring memo", "Cover option B", "delfonics-ring-memo.jpg"),
    ]
    for name, option, image in extras:
        add("Desk accessories", name, option, "Delfonics", image)

    assert len(rows) == 200
    for i, row in enumerate(rows, start=1):
        row["code"] = f"GP-{i:03d}"
    return rows


PRODUCTS = build_products()

FAMILY_IMAGES = {
    "Highlighters & markers": ["zebra-mildliner.jpg"],
    "Mechanical pencils": ["tombow-mono-graph.png"],
    "Notebooks & memo": ["md-notebook.webp", "delfonics-rollbahn.jpg"],
    "Decoration tape": ["plus-deco-rush.jpg"],
    "Pencil cases": ["kokuyo-neocritz.webp"],
    "Desk accessories": [
        "delfonics-correction-tape.jpg", "delfonics-zip-organizer.jpg",
        "delfonics-life-noble.jpg", "delfonics-ring-memo.jpg",
    ],
}


def fit_image(c, path, x, y, w, h):
    with Image.open(path) as im:
        iw, ih = im.size
    scale = min(w / iw, h / ih)
    dw, dh = iw * scale, ih * scale
    c.drawImage(ImageReader(path), x + (w - dw) / 2, y + (h - dh) / 2, dw, dh, mask="auto")


def top_bar(c, title, page_no):
    c.setFillColor(NAVY)
    c.rect(0, H - 46, W, 46, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 15)
    c.drawString(M, H - 29, "GUINEA PIG TRADING")
    c.setFont("Helvetica", 7)
    c.drawRightString(W - M, H - 26, "JAPANESE STATIONERY CATALOGUE  /  200 ITEMS")
    c.setFillColor(RED)
    c.rect(0, H - 51, W, 5, fill=1, stroke=0)
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(M, H - 81, title.upper())
    c.setFont("Helvetica", 8)
    c.setFillColor(MUTED)
    c.drawRightString(W - M, 18, f"PAGE {page_no}  |  GUINEA PIG TRADING")


def card(c, product, x, y, w, h):
    c.setFillColor(white)
    c.setStrokeColor(LINE)
    c.roundRect(x, y, w, h, 3, fill=1, stroke=1)
    photo_h = h - 57
    c.setFillColor(PAPER)
    c.rect(x + 1, y + h - photo_h - 1, w - 2, photo_h, fill=1, stroke=0)
    fit_image(c, ASSETS / product["image"], x + 8, y + h - photo_h + 6, w - 16, photo_h - 13)
    c.setFillColor(RED)
    c.setFont("Helvetica-Bold", 7.5)
    c.drawString(x + 8, y + 43, product["code"])
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(x + 8, y + 29, product["name"][:34])
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 7.2)
    c.drawString(x + 8, y + 16, f'{product["option"][:20]}  /  {product["brand"]}')
    c.linkURL(SOURCES[product["brand"]], (x, y, x + w, y + h), relative=0)


def cover(c):
    c.setFillColor(NAVY)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(RED)
    c.rect(0, H - 16, W, 16, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 15)
    c.drawString(54, H - 65, "GUINEA PIG TRADING")
    c.setFont("Helvetica-Bold", 48)
    c.drawString(54, H - 150, "JAPANESE")
    c.drawString(54, H - 202, "STATIONERY")
    c.setFillColor(RED)
    c.drawString(54, H - 254, "CATALOGUE")
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 25)
    c.drawString(58, H - 303, "200 product options")
    c.setFont("Helvetica", 11)
    c.drawString(58, H - 329, "Sorted by kind  /  Real product photography  /  Official source links")
    c.setFillColor(RED)
    c.circle(W - 170, H / 2 + 20, 130, fill=1, stroke=0)
    c.setStrokeColor(white)
    c.setLineWidth(7)
    c.line(W - 255, H / 2 - 35, W - 105, H / 2 + 75)
    c.line(W - 240, H / 2 - 55, W - 90, H / 2 + 55)
    c.setFont("Helvetica", 8)
    c.drawString(58, 47, "Reference catalogue for sourcing enquiries. Exact current variants are confirmed before quotation.")
    c.showPage()


def contents(c):
    top_bar(c, "Contents", 2)
    groups = []
    for product in PRODUCTS:
        if not groups or groups[-1][0] != product["kind"]:
            groups.append([product["kind"], product["code"], product["code"]])
        else:
            groups[-1][2] = product["code"]
    y = H - 125
    for idx, (kind, start, end) in enumerate(groups, start=1):
        c.setFillColor(PAPER if idx % 2 else white)
        c.rect(M, y - 28, W - 2 * M, 40, fill=1, stroke=0)
        c.setFillColor(RED)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(M + 14, y - 12, f"{idx:02d}")
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 13)
        c.drawString(M + 55, y - 12, kind)
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 9)
        c.drawRightString(W - M - 14, y - 12, f"{start} - {end}")
        y -= 48
    c.showPage()


def section_opener(c, kind, items, page_no):
    top_bar(c, kind, page_no)
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 30)
    c.drawString(M, H - 145, kind)
    c.setFillColor(RED)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(M, H - 180, f'{items[0]["code"]} - {items[-1]["code"]}')
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 11)
    c.drawString(M, H - 207, f"{len(items)} sorted enquiry options")
    c.drawString(M, H - 228, "Each real product-family photo appears once.")
    images = FAMILY_IMAGES[kind]
    area_x, area_y, area_w, area_h = 365, 78, W - 395, H - 190
    gap = 10
    cell_w = (area_w - gap * (len(images) - 1)) / len(images)
    for i, filename in enumerate(images):
        x = area_x + i * (cell_w + gap)
        c.setFillColor(white)
        c.setStrokeColor(LINE)
        c.roundRect(x, area_y, cell_w, area_h, 5, fill=1, stroke=1)
        fit_image(c, ASSETS / filename, x + 10, area_y + 10, cell_w - 20, area_h - 20)
    c.showPage()


def table_page(c, items, page_no):
    top_bar(c, items[0]["kind"], page_no)
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 8)
    c.drawRightString(W - M, H - 80, f'{items[0]["code"]} - {items[-1]["code"]}')
    x = M
    y = H - 110
    widths = [72, 290, 190, 110]
    headers = ["GP CODE", "PRODUCT FAMILY", "OPTION", "BRAND"]
    c.setFillColor(BLUE if False else NAVY)
    c.rect(x, y - 20, sum(widths), 25, fill=1, stroke=0)
    pos = x
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 8)
    for label, width in zip(headers, widths):
        c.drawString(pos + 8, y - 11, label)
        pos += width
    y -= 26
    for index, product in enumerate(items):
        c.setFillColor(PAPER if index % 2 == 0 else white)
        c.rect(x, y - 17, sum(widths), 22, fill=1, stroke=0)
        values = [product["code"], product["name"], product["option"], product["brand"]]
        pos = x
        for col, (value, width) in enumerate(zip(values, widths)):
            c.setFillColor(RED if col == 0 else INK)
            c.setFont("Helvetica-Bold" if col in (0, 1) else "Helvetica", 8)
            c.drawString(pos + 8, y - 9, value[:46])
            pos += width
        y -= 22
    c.showPage()


def sources_page(c, page_no):
    top_bar(c, "Sources & catalogue notes", page_no)
    y = H - 118
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(M, y, "Official maker / official shop pages")
    y -= 25
    for brand, url in SOURCES.items():
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
    c.drawString(M, y, "Important")
    notes = [
        "Product photographs are from the official maker or official shop pages listed above.",
        "GP-001 to GP-200 are Guinea Pig Trading reference codes, not maker item numbers.",
        "Some entries are color, size, format or motif enquiries within a real product family.",
        "Exact models, packaging, availability, wholesale access and prices are checked before quotation.",
    ]
    y -= 23
    c.setFont("Helvetica", 9)
    c.setFillColor(MUTED)
    for note in notes:
        c.drawString(M + 12, y, "- " + note)
        y -= 19
    c.setFillColor(NAVY)
    c.roundRect(M, 48, W - 2 * M, 64, 3, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 15)
    c.drawString(M + 18, 87, "Request a sourcing check")
    c.setFont("Helvetica", 9)
    c.drawString(M + 18, 69, "Send the GP code, preferred option, quantity and destination market through the website contact form.")
    c.showPage()


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUT), pagesize=landscape(A4), pageCompression=1)
    c.setTitle("200-Item Japanese Stationery Catalogue - Guinea Pig Trading")
    c.setAuthor("Guinea Pig Trading")
    cover(c)
    contents(c)
    page_no = 3
    start = 0
    while start < len(PRODUCTS):
        kind = PRODUCTS[start]["kind"]
        end = start
        while end < len(PRODUCTS) and PRODUCTS[end]["kind"] == kind:
            end += 1
        group = PRODUCTS[start:end]
        section_opener(c, kind, group, page_no)
        page_no += 1
        for offset in range(0, len(group), 20):
            table_page(c, group[offset:offset + 20], page_no)
            page_no += 1
        start = end
    sources_page(c, page_no)
    c.save()
    print(OUT)


if __name__ == "__main__":
    main()
