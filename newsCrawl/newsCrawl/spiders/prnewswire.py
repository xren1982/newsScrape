import scrapy
from ..items import NewscrawlItem
import pandas as pd

class PrnewswireSpider(scrapy.Spider):
    name = 'prnewswire'
    start_urls = ['http://www.prnewswire.com/news-releases/']

    def getContent(self, response, data):
        spiderItem = NewscrawlItem()
        spiderItem['site'] = "CISION PR Newswire"
        spiderItem['headlines'] = data[0]
        spiderItem['dates'] = response.css('.mb-no::text').extract_first()
        spiderItem['links'] = data[1]
        li = response.css('.release-body').xpath('.//p/text()').extract()
        content = ''.join(li).replace('/PRNewswire/','')
        spiderItem['content'] = content
        return spiderItem

    def parse(self, response):
        for i in response.css('.col-sm-12'):
            data = []
            data.append(i.xpath('.//h3/a/text()').extract_first())
            data.append('https://www.prnewswire.com'+str(i.xpath('.//h3/a/@href').extract_first()))
            if data[0] != None and data[1] != None:
                #print(data)
                request = response.follow(data[1], callback = self.getContent)
                request.cb_kwargs['data'] = data
                yield request
