import requests
from bs4 import BeautifulSoup
import random

HEADERS_LIST = [
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }
]

def scrape_amazon_product(url):
    headers = random.choice(HEADERS_LIST)
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch page: {response.status_code}")

    soup = BeautifulSoup(response.content, "html.parser")

    # Product title
    title = soup.find(id="productTitle")
    title_text = title.get_text(strip=True) if title else None

    # Price
    price = soup.select_one(".a-offscreen")
    price_text = price.get_text(strip=True) if price else None

    # Rating (broader selector for main product page)
    rating_text = None
    for elem in soup.select("span.a-icon-alt"):
        text = elem.get_text(strip=True)
        if "out of 5 stars" in text:
            rating_text = text
            break

    # First review (may still fail on JS-loaded pages)
    review_element = soup.select_one("div.reviewText.review-text-content")
    review_text = review_element.get_text(strip=True) if review_element else None

    # About this item (if present)
    about_this_item = None
    about_section = soup.find("div", id="feature-bullets")
    if about_section:
        bullet_items = about_section.select("ul.a-unordered-list li span")
        about_this_item = [
                              b.get_text(strip=True) for b in bullet_items if b.get_text(strip=True)
                          ] or None

    return {
        "product_title": title_text,
        "price": price_text,
        "rating": rating_text,
        "first_review": review_text,
        "about_this_item": about_this_item
    }

# Example usage
if __name__ == "__main__":
    url = "https://www.amazon.com/dp/B0F5H8JRJD"
    product_data = scrape_amazon_product(url)
    print(product_data)
