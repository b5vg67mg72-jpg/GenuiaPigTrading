#!/usr/bin/env python3
"""Build the Guinea Pig Trading Gunpla and figure catalogue PDFs."""

from pathlib import Path
from urllib.request import Request, urlopen
import io
import re

from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import Paragraph
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "pdf"
ASSETS = ROOT / "assets" / "catalog" / "collectibles"
TMP = ROOT / "tmp" / "pdfs" / "collectibles"

INK = colors.HexColor("#172126")
MUTED = colors.HexColor("#69777C")
PAPER = colors.HexColor("#F5F2EA")
RED = colors.HexColor("#B73C2F")
BLUE = colors.HexColor("#355D72")
LINE = colors.HexColor("#D8D4CB")
WHITE = colors.white


GUNPLA = [
    ("Entry Grade", "Entry Grade RX-78F00/E Gundam", "$16.95", "https://www.gundamplanet.com/products/entry-grade-rx-78f00-e-gundam", "https://cdn.shopify.com/s/files/1/0671/4769/4277/files/entry-grade-rx-78f00-e-gundam-base.jpg?v=1763661592"),
    ("Entry Grade", "Entry Grade Wing Gundam", "$12.95", "https://www.gundamplanet.com/products/entry-grade-wing-gundam", "https://cdn.shopify.com/s/files/1/0671/4769/4277/files/entry-grade-wing-gundam-base.jpg?v=1760370118"),
    ("High Grade", "HG MS-09 Rick Dom — Gaia / Ortega Custom", "$40.95", "https://www.gundamplanet.com/products/hg-ms-09-rick-dom-gaia-ortega-custom", "https://cdn.shopify.com/s/files/1/0671/4769/4277/files/hg-ms-09-rick-dom-gaia-ortega-custom-base.jpg?v=1758835208"),
    ("High Grade", "HGCE ZGMF-X666S Legend Gundam", "$36.95", "https://www.gundamplanet.com/products/hgce-zgmf-x666s-legend-gundam", "https://cdn.shopify.com/s/files/1/0671/4769/4277/files/hgce-zgmf-x666s-legend-gundam-base.jpg?v=1769453714"),
    ("High Grade", "HG GQuuuuuuX — Endymion Unit Awakened", "$30.95", "https://www.gundamplanet.com/products/hg-gms-%CF%89-gquuuuuux-endymion-unit-awakened", "https://cdn.shopify.com/s/files/1/0671/4769/4277/files/hg-gquuuuuux-endymion-unit-awakened-base.jpg?v=1767661272"),
    ("High Grade", "HGUC Gustav Karl Type-00", "$36.95", "https://www.gundamplanet.com/products/hguc-fd-03-00-gustav-karl-type-00", "https://cdn.shopify.com/s/files/1/0671/4769/4277/files/hguc-fd-03-00-gustav-karl-type-00-base.jpg?v=1770067607"),
    ("High Grade", "HGAC Gundam Sandrock Custom — EW Ver.", "$46.95", "https://www.gundamplanet.com/products/hgac-xxxg-01sr2-gundam-sandrock-custom-ew-ver", "https://cdn.shopify.com/s/files/1/0671/4769/4277/files/hgac-xxxg-01sr2-gundam-sandrock-custom-ew-ver-base.jpg?v=1780335427"),
    ("High Grade", "HG ORX-139 Hambrabi — GQ Ver.", "$30.95", "https://www.gundamplanet.com/products/hg-orx-139-hambrabi-gq-ver", "https://cdn.shopify.com/s/files/1/0671/4769/4277/files/hg-orx-139-hambrabi-gq-ver-base.jpg?v=1782594312"),
    ("High Grade", "HGCE GOUF Ignited — Heine Custom", "$34.95", "https://www.gundamplanet.com/products/hgce-zgmf-2000-gouf-ignited-heine-westenfluss-custom", "https://cdn.shopify.com/s/files/1/0671/4769/4277/files/hgce-zgmf-2000-gouf-ignited-heine-westenfluss-base.jpg?v=1783961827"),
    ("High Grade", "HGAW Gundam Leopard", "$30.95", "https://www.gundamplanet.com/products/hgaw-gt-9600-gundam-leopard", "https://cdn.shopify.com/s/files/1/0671/4769/4277/files/hgaw-gt-9600-gundam-leopard-base.jpg?v=1785789540"),
    ("High Grade", "HGUC Messer Type-M01 — Gawman Use", "$46.95", "https://www.gundamplanet.com/products/hguc-me02r-m01-messer-type-m01-gawman-use", "https://cdn.shopify.com/s/files/1/0671/4769/4277/files/hguc-me02r-m01-messer-type-m01-gawman-use-base.jpg?v=1779736258"),
    ("High Grade", "HGUC RX-105 Xi Gundam", "$92.95", "https://www.gundamplanet.com/products/hguc-rx-105-xi-gundam-the-sorcery-of-nymph-circe", "https://cdn.shopify.com/s/files/1/0671/4769/4277/files/hguc-rx-105-xi-gundam-the-sorcery-of-nymph-circe-base.jpg?v=1776699876"),
    ("High Grade", "HG MS-06S Char's Zaku — GQ Ver.", "$26.95", "https://www.gundamplanet.com/products/hg-ms-06s-chars-zaku-gq-ver", "https://cdn.shopify.com/s/files/1/0671/4769/4277/files/hg-ms-06s-chars-zaku-gq-ver-base.jpg?v=1764626966"),
    ("High Grade", "HG RX-78-02 White Gundam", "$26.95", "https://www.gundamplanet.com/products/hg-rx-78-02-white-gundam", "https://cdn.shopify.com/s/files/1/0671/4769/4277/files/hg-rx-78-02-white-gundam-base_859b37e0-e443-4052-bd81-fa2dbee0d190.jpg?v=1764626591"),
    ("High Grade", "HG IBO Gundam Zagan", "$36.95", "https://www.gundamplanet.com/products/hg-ibo-gundam-zagan", "https://cdn.shopify.com/s/files/1/0671/4769/4277/files/hg-ibo-gundam-zagan-base2.jpg?v=1764627317"),
    ("Real Grade", "RG Akatsuki Gundam — Oowashi Unit", "$88.95", "https://www.gundamplanet.com/products/rg-orb-01-oowashi-akatsuki-gundam", "https://cdn.shopify.com/s/files/1/0671/4769/4277/files/rg-orb-01-oowashi-akatsuki-gundam-gp.jpg?v=1737741968"),
    ("Master Grade", "MG Full Armor ZZ Gundam Ver.Ka", "$144.95", "https://www.gundamplanet.com/products/mg-fa-010s-full-armor-zz-gundam-ver-ka", "https://cdn.shopify.com/s/files/1/0671/4769/4277/files/mg-full-armor-zz-gundam-base.jpg?v=1771440060"),
    ("Master Grade", "MGSD Destiny Gundam", "$54.95", "https://www.gundamplanet.com/products/mgsd-destiny-gundam", "https://cdn.shopify.com/s/files/1/0671/4769/4277/files/mgsd-destiny-gundam-base.jpg?v=1771440407"),
    ("Master Grade", "MG Gundam Avalanche Exia Dash", "$84.95", "https://www.gundamplanet.com/products/mg-gn-001-hs-a01-gundam-avalanche-exia-dash", "https://cdn.shopify.com/s/files/1/0671/4769/4277/files/mg-gn-001-hs-a01-gundam-avalanche-exia-dash-gp.jpg?v=1737672247"),
    ("Master Grade", "MG Hyaku-Shiki — HD Color", "$55.95", "https://www.gundamplanet.com/products/mg-msn-00100-hyaku-shiki-hd-color", "https://cdn.shopify.com/s/files/1/0671/4769/4277/files/mg-msn-00100-hyaku-shiki-hd-color-01.jpg?v=1780681762"),
    ("Master Grade", "MG Zeta Gundam Ver. 2.0 — HD Color", "$55.95", "https://www.gundamplanet.com/products/mg-msz-006-zeta-gundam-ver-2-0-hd-color", "https://cdn.shopify.com/s/files/1/0671/4769/4277/files/mg-msz-006-zeta-gundam-ver-2-0-hd-color-01.jpg?v=1780681220"),
    ("Master Grade", "MG Gundam Mk-II Titans Ver. 2.0", "$48.95", "https://www.gundamplanet.com/products/mg-rx-178-gundam-mk-ii-titans-ver-2-0-hd-color", "https://cdn.shopify.com/s/files/1/0671/4769/4277/files/mg-rx-178-gundam-mk-ii-titans-ver-2-0-hd-color-01.jpg?v=1780680129"),
    ("Master Grade", "MG Gundam Barbatos Lupus", "$84.95", "https://www.gundamplanet.com/products/mg-asw-g-08-gundam-barbatos-lupus", "https://cdn.shopify.com/s/files/1/0671/4769/4277/files/mg-asw-g-08-gundam-barbatos-lupus-base.jpg?v=1763409928"),
    ("Master Grade", "MG GM Sniper II — White Dingo Ver.", "$84.95", "https://www.gundamplanet.com/products/mg-rgm-79sp-gm-sniper-ii-white-dingo-ver", "https://cdn.shopify.com/s/files/1/0671/4769/4277/files/mg-gm-sniper-ii-white-dingo-00.jpg?v=1737665409"),
]


FIGURES = [
    ("S.H.Figuarts", "Volcancer & Kamen Rider Scissors Option Set", "¥13,200", "Apr 2027", "https://tamashiiweb.com/item/16194/", "https://tamashiiweb.com/storage/images/products/thumbnail/d3b95f99-fb90-41af-87e6-4b6ad2dfffd1.webp"),
    ("S.H.Figuarts", "Kamen Rider Scissors — Shinkocchou Seihou", "¥11,000", "Apr 2027", "https://tamashiiweb.com/item/16193/", "https://tamashiiweb.com/storage/images/products/thumbnail/14ee2416-97d8-44eb-861d-b077aa3767ff.webp"),
    ("S.H.Figuarts", "Izuku Midoriya & Katsuki Bakugo — Childhood Set", "¥11,000", "May 2027", "https://tamashiiweb.com/item/16190/", "https://tamashiiweb.com/storage/images/products/thumbnail/24e0f819-4eae-4754-88f9-4532b274e7d6.webp"),
    ("S.H.Figuarts", "Son Goku — Return to Earth", "¥8,800", "Jun 2027", "https://tamashiiweb.com/item/16189/", "https://tamashiiweb.com/storage/images/products/thumbnail/d3b1d969-2c34-4b2d-a78d-218a9150c0fe.webp"),
    ("S.H.Figuarts", "Antlar — 60th Anniversary Edition", "¥11,000", "May 2027", "https://tamashiiweb.com/item/16167/", "https://tamashiiweb.com/storage/images/products/thumbnail/7688b957-216e-4b28-b0ca-759d109d6e90.webp"),
    ("S.H.Figuarts", "Ultraman Max", "¥9,350", "Apr 2027", "https://tamashiiweb.com/item/16037/", "https://tamashiiweb.com/storage/images/products/thumbnail/89294758-0c56-41e6-9df9-907e2b66b9b1.webp"),
    ("Figuarts ZERO", "Uzumaki Naruto — NARUTO 72 Series 29", "¥11,000", "Mar 2027", "https://tamashiiweb.com/item/16036/", "https://tamashiiweb.com/storage/images/products/thumbnail/6d1abc07-aa84-46d2-871a-4888c35a30a9.webp"),
    ("Figuarts ZERO", "Kamen Rider vs. Cobra Man", "¥24,200", "Feb 2027", "https://tamashiiweb.com/item/16014/", "https://tamashiiweb.com/storage/images/products/thumbnail/4458eac3-d28b-4c6e-92a1-4269239ef680.webp"),
    ("Figuarts ZERO", "STARTune Monkey D. Luffy — Departure", "¥8,250", "Dec 2026", "https://tamashiiweb.com/item/15908/", "https://tamashiiweb.com/storage/images/products/thumbnail/11af71b5-9934-45d5-ac22-abea0edaa078.webp"),
    ("Figuarts ZERO", "STARTune Uzumaki Naruto — Will of the Hokage", "¥8,250", "Jan 2027", "https://tamashiiweb.com/item/15910/", "https://tamashiiweb.com/storage/images/products/thumbnail/9ebf0f65-0379-462a-89b2-64dde9b8c333.webp"),
    ("Figuarts ZERO", "STARTune Son Goku — Arrival at the Battlefield", "¥8,250", "Feb 2027", "https://tamashiiweb.com/item/15909/", "https://tamashiiweb.com/storage/images/products/thumbnail/1ff0dfaa-0309-47f0-8b59-c95a7cede7db.webp"),
    ("Figuarts ZERO", "Monkey D. Luffy Gear 5 — ONE PIECE BASE Limited", "¥11,000", "Jul 2026", "https://tamashiiweb.com/item/15900/", "https://tamashiiweb.com/storage/images/products/thumbnail/e8a7f8b7-3ca6-43fc-be44-548f3b8771cd.webp"),
    ("METAL BUILD", "Strike Gundam — Engineering Edition", "¥19,800", "Jan 2027", "https://tamashiiweb.com/item/16166/", "https://tamashiiweb.com/storage/images/products/thumbnail/4e368361-6ce6-4fd7-8a66-6b778d402e11.webp"),
    ("METAL BUILD", "Strike Noir Gundam — 20th Memorial Color", "¥39,600", "Mar 2027", "https://tamashiiweb.com/item/16139/", "https://tamashiiweb.com/storage/images/products/thumbnail/dd069f91-5c8c-4a31-9e6c-415497ac5679.webp"),
    ("METAL BUILD", "God Gundam — Meikyo Shisui", "¥39,600", "Nov 2026", "https://tamashiiweb.com/item/16062/", "https://tamashiiweb.com/storage/images/products/thumbnail/71ab1016-d098-40d8-811a-27c46f70b1bd.webp"),
    ("METAL BUILD", "METEOR", "¥88,000", "Feb 2027", "https://tamashiiweb.com/item/16006/", "https://tamashiiweb.com/storage/images/products/thumbnail/da57b975-5bf7-4ebd-bb0b-00bc6e578ced.webp"),
    ("METAL BUILD", "Kämpfer — METAL BUILD EXPO Edition", "¥44,000", "Dec 2026", "https://tamashiiweb.com/item/15864/", "https://tamashiiweb.com/storage/images/products/thumbnail/528ef6d4-8dea-4059-b1e2-67d8dcb89bf3.webp"),
    ("METAL BUILD", "Hi-ν Gundam HWS Option Set", "¥19,800", "Nov 2026", "https://tamashiiweb.com/item/15862/", "https://tamashiiweb.com/storage/images/products/thumbnail/f9339e33-edfe-40fc-a7d1-bc1f1b8f8bb9.webp"),
]


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:70]


def fetch_image(url, filename):
    ASSETS.mkdir(parents=True, exist_ok=True)
    out = ASSETS / filename
    if out.exists():
        return out
    req = Request(url, headers={"User-Agent": "Mozilla/5.0", "Referer": url})
    with urlopen(req, timeout=45) as response:
        raw = response.read()
    image = PILImage.open(io.BytesIO(raw)).convert("RGB")
    image.thumbnail((1400, 1400), PILImage.Resampling.LANCZOS)
    image.save(out, "JPEG", quality=91, optimize=True)
    return out


def draw_fitted_image(c, path, x, y, w, h):
    image = PILImage.open(path)
    iw, ih = image.size
    scale = min(w / iw, h / ih)
    dw, dh = iw * scale, ih * scale
    c.drawImage(str(path), x + (w - dw) / 2, y + (h - dh) / 2, dw, dh, preserveAspectRatio=True, mask="auto")


def para(c, text, x, y_top, width, style):
    p = Paragraph(text, style)
    _, h = p.wrap(width, 80 * mm)
    p.drawOn(c, x, y_top - h)
    return h


def footer(c, page, total):
    w, _ = A4
    c.setStrokeColor(LINE)
    c.line(15 * mm, 14 * mm, w - 15 * mm, 14 * mm)
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 6.8)
    c.drawString(15 * mm, 9.5 * mm, "SELECT GP CODES  •  EMAIL XIAOYUELIU111@GMAIL.COM  •  APPROVE THE QUOTE BEFORE PURCHASE")
    c.drawRightString(w - 15 * mm, 9.5 * mm, f"{page} / {total}")


def cover(c, title, subtitle, count, groups, note):
    w, h = A4
    c.setFillColor(PAPER)
    c.rect(0, 0, w, h, fill=1, stroke=0)
    c.setFillColor(RED)
    c.rect(0, h - 10 * mm, w, 10 * mm, fill=1, stroke=0)
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(18 * mm, h - 31 * mm, "GUINEA PIG TRADING")
    c.setFont("Helvetica-Bold", 35)
    y = h - 68 * mm
    for line in title.split("\n"):
        c.drawString(18 * mm, y, line)
        y -= 13 * mm
    c.setFillColor(BLUE)
    c.setFont("Helvetica-Bold", 15)
    c.drawString(18 * mm, y - 3 * mm, subtitle)
    c.setFillColor(WHITE)
    c.roundRect(18 * mm, 43 * mm, w - 36 * mm, 96 * mm, 5 * mm, fill=1, stroke=0)
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 25)
    c.drawString(27 * mm, 119 * mm, f"{count} real products")
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 10)
    c.drawString(27 * mm, 107 * mm, "Every item has its own photo, product code and source link.")
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(RED)
    c.drawString(27 * mm, 94 * mm, "SORTED BY KIND")
    c.setFillColor(INK)
    c.setFont("Helvetica", 9)
    c.drawString(27 * mm, 85 * mm, "  •  ".join(groups))
    c.setFillColor(RED)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(27 * mm, 72 * mm, "HOW TO REQUEST A CURRENT QUOTE")
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(27 * mm, 63 * mm, "1  Pick GP codes     2  Send quantity + destination     3  Review the written total")
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 7.4)
    text = c.beginText(27 * mm, 53 * mm)
    text.setLeading(8)
    for line in note:
        text.textLine(line)
    c.drawText(text)


def build_catalogue(filename, title, subtitle, prefix, items, source_name, source_note):
    OUT.mkdir(parents=True, exist_ok=True)
    grouped = []
    for item in items:
        if item[0] not in grouped:
            grouped.append(item[0])
    pages = 1 + (len(items) + 3) // 4
    path = OUT / filename
    c = canvas.Canvas(str(path), pagesize=A4, pageCompression=1)
    c.setTitle(title.replace("\n", " "))
    c.setAuthor("Guinea Pig Trading")
    cover(c, title, subtitle, len(items), grouped, source_note)
    footer(c, 1, pages)
    c.showPage()

    name_style = ParagraphStyle("name", fontName="Helvetica-Bold", fontSize=9.1, leading=11, textColor=INK)
    link_style = ParagraphStyle("link", fontName="Helvetica-Bold", fontSize=7.2, leading=8.4, textColor=BLUE)
    card_w = 85 * mm
    card_h = 122 * mm
    xs = [15 * mm, 110 * mm]
    ys = [A4[1] - 20 * mm - card_h, 20 * mm]
    page_no = 2
    for start in range(0, len(items), 4):
        c.setFillColor(PAPER)
        c.rect(0, 0, *A4, fill=1, stroke=0)
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 14)
        page_categories = []
        for product in items[start:start + 4]:
            if product[0] not in page_categories:
                page_categories.append(product[0])
        page_label = " / ".join(page_categories)
        c.drawString(15 * mm, A4[1] - 13 * mm, page_label)
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 7.3)
        c.drawRightString(A4[0] - 15 * mm, A4[1] - 13 * mm, "Pick the GP codes you want quoted")
        for pos, item in enumerate(items[start:start + 4]):
            category, name, price, *rest = item
            if len(rest) == 2:
                release = None
                url, image_url = rest
            else:
                release, url, image_url = rest
            idx = start + pos
            x = xs[pos % 2]
            y = ys[pos // 2]
            c.setFillColor(WHITE)
            c.setStrokeColor(LINE)
            c.roundRect(x, y, card_w, card_h, 3 * mm, fill=1, stroke=1)
            c.setFillColor(RED)
            c.roundRect(x + 5 * mm, y + card_h - 13 * mm, 31 * mm, 7 * mm, 2 * mm, fill=1, stroke=0)
            c.setFillColor(WHITE)
            c.setFont("Helvetica-Bold", 6.6)
            c.drawCentredString(x + 20.5 * mm, y + card_h - 10.7 * mm, category.upper()[:26])
            code = f"{prefix}-{idx + 1:03d}"
            c.setFillColor(MUTED)
            c.setFont("Helvetica-Bold", 7)
            c.drawRightString(x + card_w - 5 * mm, y + card_h - 10.5 * mm, code)
            image_path = fetch_image(image_url, f"{prefix.lower()}-{idx + 1:03d}-{slug(name)}.jpg")
            draw_fitted_image(c, image_path, x + 6 * mm, y + 50 * mm, card_w - 12 * mm, 52 * mm)
            para(c, name, x + 6 * mm, y + 45 * mm, card_w - 12 * mm, name_style)
            c.setFillColor(INK)
            c.setFont("Helvetica-Bold", 11)
            c.drawString(x + 6 * mm, y + 20 * mm, price)
            c.setFillColor(MUTED)
            c.setFont("Helvetica", 6.8)
            label = "Reference retail price"
            if release:
                label += f"  •  Release {release}"
            c.drawString(x + 6 * mm, y + 15 * mm, label)
            para(c, f'<link href="{url}">View {source_name} product source →</link>', x + 6 * mm, y + 11 * mm, card_w - 12 * mm, link_style)
            c.linkURL(url, (x, y, x + card_w, y + card_h), relative=0)
        footer(c, page_no, pages)
        page_no += 1
        c.showPage()
    c.save()
    return path


def main():
    TMP.mkdir(parents=True, exist_ok=True)
    gunpla = build_catalogue(
        "japanese-gunpla-catalogue.pdf",
        "GUNPLA\nCATALOGUE",
        "Models worth asking us to source",
        "GP-G",
        GUNPLA,
        "retailer",
        [
            "Product photos and reference prices: Gundam Planet product listings.",
            "Prices shown in USD for comparison only; Guinea Pig Trading quotes in JPY after checking Japan stock.",
            "Gunpla is a trademark of Bandai. This is an independent sourcing shortlist, not an official Bandai catalogue.",
        ],
    )
    figures = build_catalogue(
        "japanese-figure-catalogue.pdf",
        "FIGURE\nCATALOGUE",
        "Character pieces and premium display collectibles",
        "GP-F",
        FIGURES,
        "official",
        [
            "Product photos, Japanese reference prices and release information: Tamashii Nations.",
            "Price and availability must be reconfirmed before purchase; shipping and sourcing fees are not included.",
            "This is an independent Guinea Pig Trading shortlist, not an official Bandai Spirits publication.",
        ],
    )
    print(gunpla)
    print(figures)


if __name__ == "__main__":
    main()
