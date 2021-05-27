from scrapy import Spider, crawler

process = crawler.CrawlerProcess({
# "USER_AGENT": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)"
    "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:56.0) Gecko/201001"
                  "01 Firefox/56.0",
    "ACCEPT": "text/html,application/xhtml+xml,application/xml;q=0.9,"
              "image/webp,*/*;q=0.8",
    "ACCEPT-LANGUAGE": "en-US,en;q=0.8,pt;q=0.6", "Accept-Encoding": "",
    "COOKIE": "TSPD_101=083d5cd761ab2800868418783bae1aae57b70ab4786a216e0a49ce2368f8493bef8fa66c2d7700038a933a760994d668:083d5cd761ab2800868418783bae1aae57b70ab4786a216e0a49ce2368f8493bef8fa66c2d7700038a933a760994d66808f6323285063800d41c249b3650f2c69da754fd26b6920235807ee44b3441f2f1a1a78d8b5c9c9d708c1cb8c21657e7a362a8bb537c7de84aa23c3b5c49648a; ASP.NET_SessionId=nznykhke4p5dv5cyxufw40he; __AntiXsrfToken=ee00d3fa9bcc446991baa9d7c56f1b24; TS0119cd6b=01bbddaca7d9841c3078ccf1d3395b99ed3b7eed875943c0b956ec3d98153cde3858cc421311e805e2dfde352a3f73b227e9bcba972d30d8e4eb50dd4c88e17fbce83e2fcfce615b6162ead6ae439466373b0a9dcf4c4130e2a5b4336549342baf12e62f9c2093374d8e0b4544d8843a6b09cb0d42cf4f75692e7b432a985a1fb31f96dc48; f5avr2092907947aaaaaaaaaaaaaaaa=OIJODOACAJGHJDGMCEOMFPLBPOACNEKELOJMNNFMGDEEIJHLAGKJFIFPADLCDABDDAHEOHHKENACMNOEIBBNPMOPIBLAIIAKEKFFCKBHGDIHLPAIBKDNGKNBHMMEECNH"
})  # User-Agent / Accept / Accept-Language
quotes = []


def store_quotes(value):
    quotes.append(value)


def store_to_file(filename, info):
    with open(filename, "w") as file:
        file.write(str(info))
        file.close()


class QuotesSpider(Spider):
    name = "quotes_spider"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/"]

    def parse(self, response):
        quotes = response.xpath(
            "//div[@class='quote']//span[@class='text']/text()").extract()
        store_quotes(quotes)
        # store_to_file("quotes.txt", quotes)
        yield {"quotes": quotes}


if __name__ == "__main__":
    process.crawl(QuotesSpider)
    process.start()

    print(quotes)
