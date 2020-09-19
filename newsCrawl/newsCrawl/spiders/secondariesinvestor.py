import scrapy
from ..items import NewscrawlItem
import pandas as pd


class SecondariesinvestorSpider(scrapy.Spider):
    name = 'secondariesinvestor'
    start_urls = ['https://www.secondariesinvestor.com/news/fundraising/']

    def parse(self, response):
        spiderItem = NewscrawlItem()
        spiderItem['site'] = "Secondaries Investor"

        for i in response.css('.item-details'):
            spiderItem['headlines'] = i.css('.entry-title').xpath('.//a/text()').extract_first()
            d = i.css('.td-post-date').xpath('.//time/@datetime').extract()
            if len(d) == 0:
                spiderItem['dates'] = pd.Timestamp("today").strftime("%m/%d/%Y")
            else:
                spiderItem['dates'] = d[0].split('T')[0]
            spiderItem['links'] = i.css('.entry-title').xpath('.//a/@href').extract_first()
            yield spiderItem
