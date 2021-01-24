import re
import argparse
import logging
from time import sleep

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

driver = webdriver.Safari()  # Allow Remote Automation On Safari Develop Tab
driver.implicitly_wait(5)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_soup(url: str) -> BeautifulSoup:
    # return BeautifulSoup(requests.get(url).text, "html.parser")
    driver.get(url)
    sleep(3)
    return BeautifulSoup(driver.page_source, "html.parser")


def get_price(value: str) -> float:
    price_match = re.match(r".*?€ +(?P<price>\d+,\d+).*", value)
    return float(price_match["price"].replace(",", "."))


def clean_name_soup(soup: list) -> list:
    """Can be either 'title', 'image' or 'buttonAnchor'"""
    clean_soup = []
    for x in soup:
        if x.parent.get("class") == ["title"]:
            clean_soup.append(x.text.strip())
    return clean_soup


def clean_price_soup(soup: list) -> list:
    """Can be either 'standardPriceContainer-selector' or 'priceWasRows'"""
    clean_soup = []
    for x in soup:
        if x.parent.get("class") == ["standardPriceContainer-selector"]:
            clean_soup.append(get_price(x.text))
    return clean_soup


def build_dict(keys: list, values: list, values2: list) -> dict:
    items = {}
    for position, key in enumerate(keys):
        items[key] = values[position]
    return items


def search_continente(category: str, page: int, limit: int) -> dict:
    base_url = "https://www.continente.pt/stores/continente/pt-pt/public/Pages/" \
               "category.aspx?cat={}#/?page={}&pl={}"
    soup = get_soup(base_url.format(category, page, limit))
    # print(soup.prettify())
    # print(soup.title.parent.name, soup.title.name, soup.title.text.strip())

    name_soup = clean_name_soup(soup.find_all("a", "ecsf_QuerySuggestions"))
    price_soup = clean_price_soup(soup.find_all("div", "priceFirstRow"))
    price2_soup = clean_price_soup(soup.find_all("div", "priceSecondRow"))

    names, prices, prices2 = len(name_soup), len(price_soup), len(price2_soup)
    if names > limit:
        logger.error("Too many keys ({} for limit {})".format(names, limit))
        raise ValueError
    if names != prices or names != prices2:
        logger.error("Keys and values dont match: {}, {}, {}".format(names, prices,
                                                                     prices2))
        raise ValueError
    if names != limit:
        logger.warning("{} is the last page ?!".format(page))

    return build_dict(name_soup, price_soup, price2_soup)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--category", '-c', choices=[
        "Bio-Saudável", "Mercearia", "Frescos", "Bebidas", "Latícinios", "Congelados",
        "Bebé", "Higiene-Beleza", "Limpeza", "Animais", "Casa"], required=True)
    parser.add_argument("--page", '-p', type=int, required=False)
    parser.add_argument("--limit", '-l', choices=[20, 40, 80], default=80)
    parser.add_argument("--max_pages", '-m', type=int, default=3)
    args = parser.parse_args()

    if args.page:
        result = search_continente(args.category, args.page, args.limit)
    else:
        result = {}
        for page in range(args.max_pages):
            new_result = search_continente(args.category, page + 1, args.limit)
            result = {**result, **new_result}
            if not new_result:
                break

    if len(result) < args.limit:
        logger.warning("Not handling items with same name but different sizes !!")

    logger.info(result)
    driver.quit()
    driver.stop_client()
