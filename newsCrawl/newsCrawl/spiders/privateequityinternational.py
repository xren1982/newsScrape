import scrapy
from ..items import NewscrawlItem
import pandas as pd

class PrivateequityinternationalSpider(scrapy.Spider):
    name = 'privateequityinternational'
    start_urls = ['https://www.privateequityinternational.com/news-analysis/fundraising/']

    def parse(self, response):
        spiderItem = NewscrawlItem()
        spiderItem['site'] = "Private Equity International"
        for i in response.xpath('//div[@class="item-details"]'):
            h = i.xpath('.//div[@class="item-header"]/h2/a/text()').extract()
            if len(h) > 0:
                spiderItem['headlines'] = h[0]
                spiderItem['dates'] = i.xpath('.//div/span/time/text()').extract_first()
                spiderItem['links'] = i.xpath('.//div[@class="item-header"]/h2/a/@href').extract_first()
                yield spiderItem
