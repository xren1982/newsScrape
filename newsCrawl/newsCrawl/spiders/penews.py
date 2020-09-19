import scrapy
from ..items import NewscrawlItem


class PenewsSpider(scrapy.Spider):
    name = 'penews'
    start_urls = ['https://www.penews.com/funds/']

    def parse(self, response):
        spiderItem = NewscrawlItem()
        spiderItem['site'] = "PRIVATE EQUITY NEWS"

        for i in response.xpath('//article'):
            spiderItem['headlines'] = i.xpath('.//div/h2/a/text()').extract_first()
            spiderItem['dates'] = i.xpath('.//div/p/text()').extract_first()
            spiderItem['links'] = i.xpath('.//div/h2/a/@href').extract_first()
            yield spiderItem
