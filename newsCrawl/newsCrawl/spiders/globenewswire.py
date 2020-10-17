import scrapy
from ..items import NewscrawlItem
import pandas as pd

class GlobenewswireSpider(scrapy.Spider):
    name = 'globenewswire'
    start_urls = ['http://www.globenewswire.com/en/Index/']

    def getContent(self, response, data):
        spiderItem = NewscrawlItem()
        spiderItem['site'] = "businesswire : A BERKSHIRE HATHAWAY COMPANY"
        spiderItem['headlines'] = data[0]
        spiderItem['dates'] = response.xpath('.//span[@itemprop="datePublished"]/em/time/@datetime').extract()
        spiderItem['links'] = data[1]
        li = response.css('.article-body').xpath('.//p/text()').extract()
        spiderItem['content'] = ' '.join(li)
        return spiderItem

    def parse(self, response):
        for i in response.css('.post-title16px'):
            data = []
            data.append(i.xpath('.//a/text()').extract_first())
            data.append('https://www.globenewswire.com'+str(i.xpath('.//a/@href').extract_first()))
            if data[0] != None and data[1] != None:
                request = response.follow(data[1], callback = self.getContent)
                request.cb_kwargs['data'] = data
                yield request
