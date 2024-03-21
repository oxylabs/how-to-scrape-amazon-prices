# How to Scrape Amazon Prices

[![Oxylabs promo code](https://user-images.githubusercontent.com/129506779/250792357-8289e25e-9c36-4dc0-a5e2-2706db797bb5.png)](https://oxylabs.go2cloud.org/aff_c?offer_id=7&aff_id=877&url_id=112)

Here's the process of scraping best-selling items, search results, and currently available deals from Amazon using Python and Oxylabs [E-Commerce Scraper API](https://oxylabs.io/products/scraper-api/ecommerce) (**1-week free trial**).

For a detailed walkthrough with explanations and visuals, check our [blog post](https://oxylabs.io/blog/scraping-amazon-prices).

## The complete code

```python
import requests
import pandas as pd

USERNAME = "USERNAME"
PASSWORD = "PASSWORD"


def parse_price_results(results):
    return [
        {
            "price": result["price"],
            "title": result["title"],
            "currency": result["currency"],
        }
        for result in results
    ]


def get_best_seller_results(category_id):
    payload = {
        "source": "amazon_bestsellers",
        "domain": "com",
        "query": category_id,
        "start_page": 1,
        "parse": True,
    }
    response = requests.post(
        "https://realtime.oxylabs.io/v1/queries",
        auth=(USERNAME, PASSWORD),
        json=payload,
    )
    response.raise_for_status()
    results = response.json()["results"][0]["content"]["results"]
    return parse_price_results(results)


def get_search_results(query):
    payload = {
        "source": "amazon_search",
        "domain": "com",
        "query": query,
        "start_page": 1,
        "parse": True,
    }
    response = requests.post(
        "https://realtime.oxylabs.io/v1/queries",
        auth=(USERNAME, PASSWORD),
        json=payload,
    )
    response.raise_for_status()
    results = response.json()["results"][0]["content"]["results"]["organic"]
    return parse_price_results(results)


def get_deals_results(url):
    payload = {
        "source": "amazon",
        "url": url,
        "parse": True,
    }
    response = requests.post(
        "https://realtime.oxylabs.io/v1/queries",
        auth=(USERNAME, PASSWORD),
        json=payload,
    )
    response.raise_for_status()
    results = response.json()["results"][0]["content"]["results"]["organic"]
    return parse_price_results(results)


dog_food_category_id = "2975359011"

best_seller_results = get_best_seller_results(dog_food_category_id)
best_seller_df = pd.DataFrame(best_seller_results)
best_seller_df.to_csv("best_seller.csv")

search_results = get_search_results("couch")
search_df = pd.DataFrame(search_results)
search_df.to_csv("search.csv")

deal_url = "https://www.amazon.com/s?i=sporting&rh=n%3A3400371%2Cp_n_deal_type%3A23566064011&s=exact-aware-popularity-rank&pf_rd_i=10805321&pf_rd_m=ATVPDKIKX0DER&pf_rd_p=bf702ff1-4bf6-4c17-ab26-f4867bf293a9&pf_rd_r=ER3N9MGTCESZPZ0KRV8R&pf_rd_s=merchandised-search-3&pf_rd_t=101&ref=s9_acss_bw_cg_SODeals_3e1_w"

deal_results = get_deals_results(deal_url)
deal_df = pd.DataFrame(deal_results)
deal_df.to_csv("deals.csv")
```

## Final word

Check our [documentation](https://developers.oxylabs.io/scraper-apis/e-commerce-scraper-api/amazon) for all of the API parameters found in this guide.

If you have any questions, feel free to contact us at support@oxylabs.io or via the live chat on our [homepage](https://oxylabs.io/).
