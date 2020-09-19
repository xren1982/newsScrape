import scrapy
from ..items import NewscrawlItem
import re

class VccirclePeSpider(scrapy.Spider):
    name = 'vccircle'
    start_urls = ['https://www.vccircle.com/deal-type/pe/','https://www.vccircle.com/deal-type/venture-capital/']

    def parse(self, response):
        spiderItem = NewscrawlItem()
        spiderItem['site'] = "VCCiRCLE : "+response.css('.page-title::text').get()
        for i in response.css('.article-details'):
            t = i.xpath('.//div[@class="title"]/a/text()').extract()
            d = i.xpath('.//span[@class="publish-time"]/text()').extract()
            for x in t:
                if re.search('[a-zA-Z]+',x) is not None:
                    spiderItem['headlines'] = str(x).strip("\n").strip(" ")
            for x in d:
                if re.search('[a-zA-Z]+',x) is not None:
                    spiderItem['dates'] = str(x).strip("\n").strip(" ")
            spiderItem['links'] = i.xpath('.//div[@class="title"]/a/@href').extract_first()
            yield spiderItem

#response.css('.card-body').css('.card-title::text').extract()
# response.css('.card-body').xpath('.//a/@href').extract()
