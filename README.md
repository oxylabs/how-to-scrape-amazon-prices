# How to Scrape Amazon Prices

[![Oxylabs promo code](https://user-images.githubusercontent.com/129506779/250792357-8289e25e-9c36-4dc0-a5e2-2706db797bb5.png)](https://oxylabs.go2cloud.org/aff_c?offer_id=7&aff_id=877&url_id=112)

### Free Amazon Prices Scraper

A free tool used to get Amazon product prices for a provided Amazon department page.

### Prerequisites

To run this tool, you need to have Python 3.11 installed in your system.

### Installation

Open up a terminal window, navigate to this repository and run this command:

```make install```

### Retrieving the URL of an Amazon page to scrape prices from

First off, open up Amazon and select a department from which you want to scrape prices for products. 

For this example, we'll be using the `Camera & Photo` department.

<img width="993" alt="image" src="https://github.com/user-attachments/assets/0ee1f37b-d99a-4cb7-b699-9b6f6c95bfff" />


After the page loads, simply copy the URL in the browser and save it. We'll need it for scraping price data.

### Scraping Amazon prices

To get prices from products listed on the department page you chose, simply run this command in your terminal:

```make scrape URL="<amazon_department_page_url>"```

With the URL we retrieved earlier, the command would look like this:

```make scrape URL="https://www.amazon.com/s?i=specialty-aps&bbn=16225009011&rh=n%3A%2116225009011%2Cn%3A502394&ref=nav_em__nav_desktop_sa_intl_camera_and_photo_0_2_6_3"```

Make sure to surround the URL with quotation marks, otherwise the tool might have trouble parsing it.

After running the command, your terminal should look something like this:

<img width="1163" alt="image" src="https://github.com/user-attachments/assets/eb0e83f9-d995-4c48-8cc8-db7635c55feb" />

If a listed product is out of stock, the tool will notify you with a dedicated message. The product will be skipped if that is the case.

### Retrieved data

After the tool has finished running, you should see a file named `amazon_prices.csv` in your directory.

The generated CSV file contains data with these columns inside it:

- `title` - The title of the product.
- `url` - The URL pointing to the product's Amazon page.
- `price` - The price of the product.
- `currency` - The currency that the product is sold in.

The data should look something like this:

<img width="717" alt="image" src="https://github.com/user-attachments/assets/4e00fecc-8176-4248-9b63-0bc6dd382905" />


### Notes

In case the code doesn't work or your project is of bigger scale, please refer to the second part of the tutorial. There, we showcase how to scrape public data with Oxylabs Scraper API.

### Scraping with Oxylabs API

Here's the process of scraping best-selling items, search results, and currently available deals from Amazon using Python and Oxylabs [E-Commerce Scraper API](https://oxylabs.io/products/scraper-api/ecommerce) (a part of Web Scraper API). You can claim a **1-week free trial** by registering on the [dashboard](https://dashboard.oxylabs.io/).

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

Check our [documentation](https://developers.oxylabs.io/scraper-apis/web-scraper-api/amazon) for all of the API parameters found in this guide.

If you have any questions, feel free to contact us at support@oxylabs.io or via the live chat on our [homepage](https://oxylabs.io/).

Looking to scrape more other Amazon data? [Amazon Review Scraper](https://github.com/oxylabs/amazon-review-scraper), [Amazon ASIN Scraper](https://github.com/oxylabs/amazon-asin-scraper), [Bypass Amazon CAPTCHA](https://github.com/oxylabs/how-to-bypass-amazon-captcha), [Scraping Amazon Product Data](https://github.com/oxylabs/how-to-scrape-amazon-product-data)
