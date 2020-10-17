import scrapy
from ..items import NewscrawlItem
import pandas as pd

class PrwebSpider(scrapy.Spider):
    name = 'prweb'
    start_urls = ['http://www.prweb.com/recentnews/index.htm?/']

    def getContent(self, response, data):
        spiderItem = NewscrawlItem()
        spiderItem['site'] = "CISION : PRWeb"
        spiderItem['headlines'] = data[0]
        spiderItem['dates'] = response.css('.article-date').xpath('.//span[@itemprop="datePublished"]/text()').extract()
        spiderItem['links'] = data[1]
        li = response.xpath('.//p[@class="responsiveNews"]/text()').extract()
        spiderItem['content'] = ' '.join(li)
        return spiderItem

    def parse(self, response):
        for i in response.css('.article-box-cont'):
            data = []
            data.append(i.xpath('.//a/h1/text()').extract_first())
            data.append('https://www.prweb.com'+str(i.xpath('.//a/@href').extract_first()))
            if data[0] != None and data[1] != None:
                request = response.follow(data[1], callback = self.getContent)
                request.cb_kwargs['data'] = data
                yield request
