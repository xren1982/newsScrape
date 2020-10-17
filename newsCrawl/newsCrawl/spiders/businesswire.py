import scrapy
from ..items import NewscrawlItem
import pandas as pd

class BusinesswireSpider(scrapy.Spider):
    name = 'businesswire'
    start_urls = ['http://www.businesswire.com/portal/site/home/news/']

    def getContent(self, response, data):
        spiderItem = NewscrawlItem()
        spiderItem['site'] = "businesswire : A BERKSHIRE HATHAWAY COMPANY"
        spiderItem['headlines'] = data[0]
        spiderItem['dates'] = response.css('.bw-release-timestamp').xpath('.//time/@datetime').extract()
        spiderItem['links'] = data[1]
        li = response.css('.bw-release-story').xpath('.//p/text()').extract()
        spiderItem['content'] = ' '.join(li)
        return spiderItem

    def parse(self, response):
        for i in response.xpath('.//div[@itemscope="itemscope"]/a'):
            data = []
            data.append(i.xpath('.//text()').extract_first())
            data.append('https://www.businesswire.com'+str(i.xpath('.//@href').extract_first()))
            if data[0] != None and data[1] != None:
                request = response.follow(data[1], callback = self.getContent)
                request.cb_kwargs['data'] = data
                yield request
