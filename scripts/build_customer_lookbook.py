from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.colors import HexColor, white
from reportlab.lib.utils import ImageReader
from PIL import Image
from build_stationery_catalogue import PRODUCTS

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output/pdf/customer-stationery-lookbook.pdf"
ASSETS = ROOT / "assets/catalog/retail"
W, H = landscape(A4)
CREAM = HexColor("#f7f1e7")
INK = HexColor("#142b33")
CORAL = HexColor("#df6755")
MINT = HexColor("#83aea2")
SUN = HexColor("#e9b955")
MUTED = HexColor("#667579")

FEATURE_CODES = ["GP-001", "GP-003", "GP-004", "GP-009", "GP-010", "GP-012", "GP-015", "GP-017", "GP-019", "GP-023"]
FEATURES = [next(p for p in PRODUCTS if p["code"] == code) for code in FEATURE_CODES]


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


def footer(c, page):
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 7)
    c.drawString(34, 18, "GUINEA PIG TRADING  /  CUSTOMER LOOKBOOK")
    c.drawRightString(W - 34, 18, f"{page}  /  PRICE CHECKED 11 OCTOBER 2026")


def cover(c):
    c.setFillColor(INK)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(CORAL)
    c.circle(W - 90, H - 75, 160, fill=1, stroke=0)
    c.setFillColor(SUN)
    c.circle(W - 270, 70, 100, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(54, H - 60, "GUINEA PIG TRADING")
    c.setFont("Helvetica-Bold", 45)
    c.drawString(54, H - 150, "Useful.")
    c.drawString(54, H - 202, "Giftable.")
    c.drawString(54, H - 254, "Easy to identify.")
    c.setFillColor(CREAM)
    c.setFont("Helvetica", 14)
    c.drawString(58, H - 292, "A focused Japanese stationery story for real customers.")
    c.setFillColor(white)
    c.roundRect(W - 345, 120, 260, 285, 8, fill=1, stroke=0)
    fit_image(c, FEATURES[0]["asset"], W - 320, 145, 210, 235)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(58, 54, "10 FEATURED PRODUCTS  /  PUBLIC PRICES  /  OFFICIAL SHOP LINKS")
    c.showPage()


def intro(c):
    c.setFillColor(CREAM)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 34)
    c.drawString(50, H - 85, "Why this shortlist is easier to sell")
    points = [
        ("CLEAR", "Every item is visibly different."),
        ("REAL", "Names, photos and prices come from the official shop."),
        ("USEFUL", "Each product has a simple reason to exist on the shelf."),
        ("ACTIONABLE", "Customers can identify an exact GP code."),
    ]
    for i, (head, body) in enumerate(points):
        x = 52 + (i % 2) * 380
        y = 325 - (i // 2) * 150
        c.setFillColor(white)
        c.roundRect(x, y, 340, 120, 7, fill=1, stroke=0)
        c.setFillColor([CORAL, MINT, SUN, CORAL][i])
        c.setFont("Helvetica-Bold", 10)
        c.drawString(x + 18, y + 86, head)
        wrap(c, body, x + 18, y + 58, 290, "Helvetica-Bold", 14, 18, INK)
    footer(c, 2)
    c.showPage()


def feature_page(c, pair, page):
    c.setFillColor(CREAM)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    accents = [CORAL, MINT]
    for i, item in enumerate(pair):
        x = 36 + i * 405
        c.setFillColor(white)
        c.roundRect(x, 58, 370, H - 90, 8, fill=1, stroke=0)
        c.setFillColor(accents[i])
        c.rect(x, H - 62, 370, 15, fill=1, stroke=0)
        fit_image(c, item["asset"], x + 24, H - 300, 322, 215)
        c.setFillColor(accents[i])
        c.setFont("Helvetica-Bold", 8)
        c.drawString(x + 24, 260, f'{item["code"]}  /  SHOP {item["shop_code"]}')
        wrap(c, item["name"], x + 24, 240, 320, "Helvetica-Bold", 14, 17, INK)
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 13)
        c.drawString(x + 24, 187, item["price"])
        wrap(c, item["benefit"], x + 24, 160, 315, "Helvetica", 10, 14, MUTED)
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 7)
        c.drawString(x + 24, 78, "CLICK THIS CARD FOR THE OFFICIAL PRODUCT PAGE")
        c.linkURL(item["url"], (x, 58, x + 370, H - 32), relative=0)
    footer(c, page)
    c.showPage()


def closing(c):
    c.setFillColor(INK)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(CORAL)
    c.rect(0, H - 16, W, 16, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 37)
    c.drawString(54, H - 115, "Start with five products,")
    c.drawString(54, H - 160, "not fifty guesses.")
    c.setFillColor(CREAM)
    c.setFont("Helvetica", 13)
    c.drawString(58, H - 200, "Send the GP codes, expected quantity, budget and destination market.")
    steps = ["1. Choose codes", "2. Confirm current stock", "3. Receive a quotation"]
    for i, step in enumerate(steps):
        x = 58 + i * 245
        c.setFillColor([CORAL, MINT, SUN][i])
        c.roundRect(x, 155, 215, 95, 7, fill=1, stroke=0)
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 13)
        c.drawString(x + 18, 196, step)
    c.setFillColor(white)
    c.setFont("Helvetica", 8)
    c.drawString(58, 66, "Displayed prices are public retail references. Final availability, shipping, fees and commercial terms require a current check.")
    c.showPage()


def main():
    c = canvas.Canvas(str(OUT), pagesize=landscape(A4), pageCompression=1)
    c.setTitle("Customer Stationery Lookbook - Guinea Pig Trading")
    c.setAuthor("Guinea Pig Trading")
    cover(c)
    intro(c)
    page = 3
    for start in range(0, len(FEATURES), 2):
        feature_page(c, FEATURES[start:start + 2], page)
        page += 1
    closing(c)
    c.save()
    print(OUT)


if __name__ == "__main__":
    main()
