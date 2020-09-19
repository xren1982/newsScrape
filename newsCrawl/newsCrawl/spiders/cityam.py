import scrapy
from ..items import NewscrawlItem
import pandas as pd

class CityamSpider(scrapy.Spider):
    name = 'cityam'
    start_urls = ['https://www.cityam.com/latest-news/']

    def parse(self, response):
        spiderItem = NewscrawlItem()
        spiderItem['site'] = "CITY A.M."

        for i in response.css('.card-body'):
            spiderItem['headlines'] = i.css('.card-title::text').extract_first()
            spiderItem['dates'] = pd.Timestamp("today").strftime("%m/%d/%Y")
            spiderItem['links'] = i.xpath('.//a/@href').extract_first()
            yield spiderItem