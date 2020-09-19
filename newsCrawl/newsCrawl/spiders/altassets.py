import scrapy
import pandas as pd
from ..items import NewscrawlItem


class AltassetsSpider(scrapy.Spider):
    name = 'altassets'
    start_urls = ['https://www.altassets.net/category/private-equity-news/by-news-type/fund-news']

    def parse(self, response):
        spiderItem = NewscrawlItem()
        spiderItem['site'] = "AltAssets : The Alternative Assets Network"
        for i in response.xpath('//div[@class="item-details"]'):
            if len(i.xpath('.//div/span/time/text()').extract()) > 0:
                spiderItem['headlines'] = i.xpath('.//h3/a/text()').extract_first()
                spiderItem['dates'] = i.xpath('.//div/span/time/text()').extract_first()
                spiderItem['links'] = i.xpath('.//h3/a/@href').extract_first()
                yield spiderItem

