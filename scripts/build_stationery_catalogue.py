from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.colors import HexColor, white
from reportlab.lib.utils import ImageReader
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output/pdf/japanese-stationery-catalogue.pdf"
ASSETS = ROOT / "assets/catalog/retail"
W, H = landscape(A4)
M = 30
NAVY = HexColor("#152f45")
RED = HexColor("#d8232a")
INK = HexColor("#20262b")
MUTED = HexColor("#68757b")
LINE = HexColor("#d7dde0")
PAPER = HexColor("#f4f4f1")
GREEN = HexColor("#497a62")


def p(code, category, name, price, asset, shop_code, benefit):
    return {
        "code": code, "category": category, "name": name, "price": price,
        "asset": asset, "shop_code": shop_code, "benefit": benefit,
        "url": f"https://shop.delfonics.com/c/brands/original/cat701/{shop_code}",
    }


PRODUCTS = [
    p("GP-001", "Notebooks & storage", "Rollbahn Extra #1 Double Pages L", "JPY 1,650", "rb-extra-1.png", "501432", "Extra page capacity for long projects."),
    p("GP-002", "Notebooks & storage", "Rollbahn Extra #2 50 Pockets L", "JPY 1,430", "rb-extra-2.png", "501433", "Pocket-heavy format for collected material."),
    p("GP-003", "Notebooks & storage", "Rollbahn Extra #4 Water-Repellent L", "JPY 2,200", "rb-extra-4.png", "501435", "A practical feature for travel and field use."),
    p("GP-004", "Notebooks & storage", "Rollbahn Extra #7 Fragrance L", "JPY 2,640", "rb-extra-7.png", "501438", "A distinctive sensory product for gifting."),
    p("GP-005", "Notebooks & storage", "Rollbahn Extra #8 Paper Bundle L", "JPY 1,100", "rb-paper-l.png", "501439", "A compact loose-paper format in L size."),
    p("GP-006", "Notebooks & storage", "Rollbahn Extra #8 Paper Bundle A5", "JPY 1,430", "rb-paper-a5.png", "501440", "A familiar A5 size for broad customer appeal."),
    p("GP-007", "Notebooks & storage", "Rollbahn Extra #8 Paper Bundle B5", "JPY 1,760", "rb-paper-b5.png", "501441", "More writing space for work and study."),
    p("GP-008", "Notebooks & storage", "Rollbahn Extra #8 Paper Bundle A4", "JPY 2,090", "rb-paper-a4.png", "501442", "Large-format paper for planning and display."),
    p("GP-009", "Notebooks & storage", "Rollbahn Extra #9 Storage Box 505", "JPY 1,980", "rb-box-505.png", "501443", "A branded storage add-on for desk displays."),
    p("GP-010", "Notebooks & storage", "American Sweets Rollbahn Pocket Memo Mini", "JPY 605", "rb-american-mini.png", "501427", "Low-price illustrated gift and impulse item."),
    p("GP-011", "Notebooks & storage", "American Sweets Rollbahn Pocket Memo M", "JPY 715", "rb-american-m.png", "501428", "A practical gift size with a playful cover."),
    p("GP-012", "Accessories", "Rollbahn Bookmark", "JPY 418", "rb-bookmark.png", "501446", "An easy add-on beside notebooks and diaries."),
    p("GP-013", "Accessories", "Rollbahn Seal Re:Limited", "JPY 385", "rb-seal-relimited.png", "601630", "Direct-store limited customization detail."),
    p("GP-014", "Accessories", "Rollbahn Seal", "JPY 385", "rb-seal.png", "501449", "Simple notebook customization at entry price."),
    p("GP-015", "Accessories", "Rollbahn Seal gyunyuya", "JPY 440", "rb-seal-gyunyuya.png", "501450", "Illustrated collaboration with collectable appeal."),
    p("GP-016", "Accessories", "Rollbahn Custom Charm Re:Limited", "JPY 660", "rb-charm-relimited.png", "601631", "Limited personalization for gift-led displays."),
    p("GP-017", "Accessories", "Rollbahn Custom Charm", "JPY 660", "rb-charm.png", "501451", "A visible add-on that encourages bundling."),
    p("GP-018", "Accessories", "Rollbahn Custom Charm gyunyuya", "JPY 715", "rb-charm-gyunyuya.png", "501452", "Illustrated charm for playful collections."),
    p("GP-019", "Diary & planning", "Rollbahn Bookmark Calendar 2027", "JPY 770", "rb-bookmark-calendar.png", "170117", "Calendar function in a compact bookmark format."),
    p("GP-020", "Diary & planning", "Pocket Memo L Protector Calendar 2027", "JPY 495", "rb-protector-calendar.png", "170116", "Protective cover and calendar in one accessory."),
    p("GP-021", "Diary & planning", "Flexible Diary Monthly Refill L", "JPY 880", "rb-refill-l.png", "170114", "A refill purchase for existing flexible users."),
    p("GP-022", "Diary & planning", "Flexible Diary Monthly Refill A5", "JPY 990", "rb-refill-a5.png", "170115", "A5 monthly planning refill for desk use."),
    p("GP-023", "Diary & planning", "Direct-Store Rollbahn Diary M 2027", "JPY 1,540", "rb-diary-m.png", "601606", "A limited diary size suited to seasonal display."),
]


def fit_image(c, filename, x, y, w, h):
    path = ASSETS / filename
    with Image.open(path) as im:
        iw, ih = im.size
    scale = min(w / iw, h / ih)
    dw, dh = iw * scale, ih * scale
    c.drawImage(ImageReader(path), x + (w - dw) / 2, y + (h - dh) / 2, dw, dh, mask="auto")


def wrap(c, text, x, y, width, font, size, leading, color):
    words, lines, line = text.split(), [], ""
    for word in words:
        candidate = (line + " " + word).strip()
        if c.stringWidth(candidate, font, size) <= width:
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


def header(c, title, page):
    c.setFillColor(NAVY)
    c.rect(0, H - 43, W, 43, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(M, H - 27, "GUINEA PIG TRADING")
    c.setFont("Helvetica", 7)
    c.drawRightString(W - M, H - 25, "BUYER-READY JAPANESE STATIONERY  /  23 PRODUCTS")
    c.setFillColor(RED)
    c.rect(0, H - 48, W, 5, fill=1, stroke=0)
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 19)
    c.drawString(M, H - 77, title.upper())
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 7.5)
    c.drawRightString(W - M, 16, f"PAGE {page}  |  PRICE CHECK: 11 OCTOBER 2026")


def card(c, item, x, y, w, h):
    c.setFillColor(white)
    c.setStrokeColor(LINE)
    c.roundRect(x, y, w, h, 4, fill=1, stroke=1)
    image_h = h - 92
    c.setFillColor(PAPER)
    c.rect(x + 1, y + h - image_h - 1, w - 2, image_h, fill=1, stroke=0)
    fit_image(c, item["asset"], x + 7, y + h - image_h + 5, w - 14, image_h - 10)
    c.setFillColor(RED)
    c.setFont("Helvetica-Bold", 7)
    c.drawString(x + 8, y + 79, f'{item["code"]}  /  SHOP {item["shop_code"]}')
    wrap(c, item["name"], x + 8, y + 64, w - 16, "Helvetica-Bold", 8.4, 10, INK)
    c.setFillColor(GREEN)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(x + 8, y + 32, item["price"])
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 6.7)
    c.drawString(x + 8, y + 20, "No out-of-stock notice when checked")
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 6.8)
    c.drawString(x + 8, y + 8, "OPEN OFFICIAL PRODUCT PAGE")
    c.linkURL(item["url"], (x, y, x + w, y + h), relative=0)


def cover(c):
    c.setFillColor(NAVY)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(RED)
    c.rect(0, H - 16, W, 16, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(54, H - 62, "GUINEA PIG TRADING")
    c.setFont("Helvetica-Bold", 43)
    c.drawString(54, H - 145, "23 products")
    c.drawString(54, H - 195, "worth showing.")
    c.setFillColor(RED)
    c.setFont("Helvetica-Bold", 19)
    c.drawString(58, H - 239, "BUYER-READY STATIONERY SHORTLIST")
    c.setFillColor(white)
    c.setFont("Helvetica", 11)
    c.drawString(58, H - 270, "Different real photos. Exact public prices. Official links. Clear next steps.")
    c.setFillColor(white)
    c.roundRect(W - 335, 112, 260, 300, 8, fill=1, stroke=0)
    fit_image(c, "rb-extra-1.png", W - 310, 135, 210, 250)
    c.setFont("Helvetica", 8)
    c.drawString(58, 48, "Public prices and availability signals were observed on the official Delfonics shop on 11 October 2026.")
    c.showPage()


def buying_notes(c):
    header(c, "How to buy from this catalogue", 2)
    steps = [
        ("1", "Choose", "Send the GP codes that fit your shop."),
        ("2", "Add details", "Tell me quantity, budget and destination."),
        ("3", "Current check", "I confirm stock, source access and shipping."),
        ("4", "Quotation", "You receive the current landed-cost estimate."),
    ]
    for i, (num, title, body) in enumerate(steps):
        x = 35 + i * 200
        c.setFillColor(PAPER)
        c.roundRect(x, 210, 178, 210, 6, fill=1, stroke=0)
        c.setFillColor(RED)
        c.circle(x + 32, 380, 18, fill=1, stroke=0)
        c.setFillColor(white)
        c.setFont("Helvetica-Bold", 13)
        c.drawCentredString(x + 32, 375, num)
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 15)
        c.drawString(x + 18, 337, title)
        wrap(c, body, x + 18, 307, 140, "Helvetica", 10, 15, MUTED)
    c.setFillColor(NAVY)
    c.roundRect(M, 70, W - 2 * M, 72, 5, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(M + 18, 111, "Important: the displayed JPY price is a public retail reference, not your final quotation.")
    c.setFont("Helvetica", 9)
    c.drawString(M + 18, 88, "Wholesale access, tax treatment, domestic freight, international shipping and service fees are checked separately.")
    c.showPage()


def product_page(c, title, items, page):
    header(c, title, page)
    cols, rows, gap = 3, 2, 11
    top, bottom = H - 92, 34
    cw = (W - 2 * M - gap * (cols - 1)) / cols
    ch = (top - bottom - gap) / rows
    for i, item in enumerate(items):
        col, row = i % cols, i // cols
        x = M + col * (cw + gap)
        y = top - (row + 1) * ch - row * gap
        card(c, item, x, y, cw, ch)
    c.showPage()


def notes(c, page):
    header(c, "Source, status & next step", page)
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(M, H - 125, "What is verified")
    verified = [
        "Every item has a different official product photograph.",
        "Names, public JPY prices and product links came from the official Delfonics web shop.",
        "Selected items showed no out-of-stock notice when checked on 11 October 2026.",
    ]
    y = H - 155
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 10)
    for line in verified:
        c.drawString(M + 12, y, "- " + line)
        y -= 25
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(M, y - 12, "What still needs confirmation")
    y -= 42
    pending = [
        "Current stock and available colors at the time of order.",
        "Quantity limits, wholesale access, resale conditions and lead time.",
        "Domestic and international shipping, duties and service fees.",
    ]
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 10)
    for line in pending:
        c.drawString(M + 12, y, "- " + line)
        y -= 25
    c.setFillColor(NAVY)
    c.roundRect(M, 55, W - 2 * M, 74, 5, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 17)
    c.drawString(M + 20, 98, "Ready to shortlist?")
    c.setFont("Helvetica", 10)
    c.drawString(M + 20, 76, "Send the GP codes, quantities and destination market through the website contact form.")
    c.showPage()


def main():
    c = canvas.Canvas(str(OUT), pagesize=landscape(A4), pageCompression=1)
    c.setTitle("Buyer-Ready Japanese Stationery Shortlist - Guinea Pig Trading")
    c.setAuthor("Guinea Pig Trading")
    cover(c)
    buying_notes(c)
    page = 3
    for category in ["Notebooks & storage", "Accessories", "Diary & planning"]:
        group = [item for item in PRODUCTS if item["category"] == category]
        for start in range(0, len(group), 6):
            product_page(c, category, group[start:start + 6], page)
            page += 1
    notes(c, page)
    c.save()
    print(OUT)


if __name__ == "__main__":
    main()
