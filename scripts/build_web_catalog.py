#!/usr/bin/env python3
"""Build three 100-item customer catalogues from Japanese product listings."""

from concurrent.futures import ThreadPoolExecutor
from html import unescape
from pathlib import Path
import json
import math
import re
import urllib.parse
import urllib.request


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "assets" / "catalog" / "data"
IMAGE_DIR = ROOT / "assets" / "catalog" / "web"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"


def fetch(url):
    request = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def clean(value):
    return re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", "", value))).strip()


def customer_price(value, minimum=4.95):
    """Turn a JPY listing price into a competitive customer-facing USD price."""
    digits = re.sub(r"[^0-9]", "", str(value))
    if not digits:
        return "Price on request"
    usd = max(minimum, math.ceil(int(digits) / 120) - 0.05)
    return f"${usd:.2f}"


def stationery():
    products = []
    seen = set()
    for page in range(1, 9):
        url = f"https://shop.delfonics.com/c/brands/original/cat701?page={page}&sort=latest"
        text = fetch(url).decode("utf-8", "replace")
        for article in re.findall(
            r'<article class="fs-c-productList__list__item[\s\S]*?</article>', text
        ):
            path = re.search(r'<a href="([^"]+)">\s*<img data-layzr=', article)
            image = re.search(r'data-layzr="([^"]+)"', article)
            analytics = re.search(
                r'data-product-url="([^"]+)"[^>]*data-eec="([^"]+)"', article
            )
            if not (path and image and analytics):
                continue
            payload = json.loads(unescape(analytics.group(2)))
            code = str(payload["id"])
            if code in seen:
                continue
            seen.add(code)
            products.append(
                {
                    "id": f"ST-{len(products) + 1:03d}",
                    "name": payload["name"],
                    "brand": "Rollbahn · DELFONICS",
                    "price": customer_price(payload["price"]),
                    "source": "https://shop.delfonics.com" + path.group(1),
                    "image_url": unescape(image.group(1)).split("?")[0],
                    "image": f"assets/catalog/web/stationery/{code}.jpg",
                }
            )
            if len(products) == 100:
                return products
    raise RuntimeError(f"Only found {len(products)} stationery products")


def figures():
    products = []
    seen = set()
    for page in range(1, 9):
        url = (
            "https://tamashiiweb.com/api/site-item/search_item.php?sort=1&per_page=100"
            f"&current_page={page}&area=japan"
        )
        payload = json.loads(fetch(url))
        for item in payload["data"]:
            title = item.get("title", "")
            brand = item.get("mainBrandName") or "TAMASHII NATIONS"
            blocked = f"{title} {brand}".lower()
            if item["tamashiiWebId"] in seen or any(
                word in blocked for word in ("gundam", "ガンダム", "metal build", "gunpla")
            ):
                continue
            seen.add(item["tamashiiWebId"])
            image_url = "https://tamashiiweb.com" + item["thumbnailImg"]
            products.append(
                {
                    "id": f"FG-{len(products) + 1:03d}",
                    "name": title,
                    "brand": brand,
                    "price": customer_price(item.get("priceTaxStr"), minimum=14.95),
                    "source": "https://tamashiiweb.com/item/" + item["tamashiiWebId"] + "/",
                    "image_url": image_url,
                    "image": f"assets/catalog/web/figures/{item['tamashiiWebId']}.webp",
                }
            )
            if len(products) == 100:
                return products
    raise RuntimeError(f"Only found {len(products)} non-Gundam figure products")


def gashapon():
    text = fetch("https://gashapon.jp/products/result.php").decode("utf-8", "replace")
    products = []
    cards = re.findall(
        r'<a href="(detail\.php\?jan_code=[^"]+)" class="c-card__link">([\s\S]*?)</a>',
        text,
    )
    for href, card in cards:
        image = re.search(r'<img[^>]+src="([^"]+)"', card)
        name = re.search(r'<p class="c-card__name">([\s\S]*?)</p>', card)
        price = re.search(r'c-card__price--main">([^<]+)', card)
        category = re.search(r'<i class="c-card__category[^>]*>([^<]+)</i>', card)
        if not all((image, name, price)):
            continue
        product_name = clean(name.group(1))
        if any(word in product_name.lower() for word in ("gundam", "ガンダム")):
            continue
        code_match = re.search(r"jan_code=(\d+)", href)
        if not code_match:
            continue
        code = code_match.group(1)
        products.append(
            {
                "id": f"GC-{len(products) + 1:03d}",
                "name": product_name,
                "brand": clean(category.group(1)) if category else "Bandai Gashapon",
                "price": customer_price(clean(price.group(1))),
                "source": urllib.parse.urljoin("https://gashapon.jp/products/", href),
                "image_url": unescape(image.group(1)),
                "image": f"assets/catalog/web/gashapon/{code}.jpg",
            }
        )
        if len(products) == 100:
            return products
    raise RuntimeError(f"Only found {len(products)} non-Gundam gashapon products")


def download(product):
    output = ROOT / product["image"]
    if output.exists() and output.stat().st_size > 1000:
        return
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(fetch(product["image_url"]))


def main():
    categories = {
        "figures": figures(),
        "stationery": stationery(),
        "gashapon": gashapon(),
    }
    all_products = [item for items in categories.values() for item in items]
    with ThreadPoolExecutor(max_workers=12) as pool:
        list(pool.map(download, all_products))
    for items in categories.values():
        for item in items:
            item.pop("image_url", None)
            item.pop("source", None)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "catalog.json").write_text(
        json.dumps(categories, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )
    print("Built " + ", ".join(f"{name}: {len(items)}" for name, items in categories.items()))


if __name__ == "__main__":
    main()
