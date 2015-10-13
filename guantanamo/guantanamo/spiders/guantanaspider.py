import scrapy

class GuantanaSpider(scrapy.Spider):
    name = "guantanamo"
    allowed_domains = ["projects.nytimes.com"]
    start_urls = [
        "http://projects.nytimes.com/guantanamo/detainees/current"
    ]

    def parse(self, response):
        filename = response.url.split("/")[-2] + '.html'
        with open(filename, 'wb') as f:
            f.write(response.body)

