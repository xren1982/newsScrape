import scrapy
from ..items import NewscrawlItem
import pandas as pd

class CityamSpider(scrapy.Spider):
    name = 'cityam'
    start_urls = ['https://www.cityam.com/latest-news/']
    #

    def getContent(self, response, data):
        spiderItem = NewscrawlItem()
        spiderItem['site'] = "CITY A.M."
        spiderItem['headlines'] = data[0]
        spiderItem['dates'] = pd.Timestamp("today").strftime("%m/%d/%Y")
        spiderItem['links'] = data[1]
        li = response.css('.single-post-content').xpath('.//p/text()').extract()
        spiderItem['content'] = ' '.join(li)
        return spiderItem

    def parse(self, response):
        for i in response.css('.card-body'):
            data = []
            data.append(i.css('.card-title::text').extract_first())
            data.append(i.xpath('.//a/@href').extract_first())
            print(data)
            request = response.follow(data[1], callback = self.getContent)
            request.cb_kwargs['data'] = data
            yield request