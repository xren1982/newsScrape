import scrapy


class Non(scrapy.Spider):
    name = 'none'
    allowed_domains = ['example.com']
    start_urls = ['https://www.altassets.net/category/private-equity-news/by-news-type/fund-news']

    def parse(self, response):
        pass

