import scrapy
from ..items import NewscrawlItem


class BuyoutsinsiderSpider(scrapy.Spider):
    name = 'buyoutsinsider'
    start_urls = ['https://www.buyoutsinsider.com/tag/fundraising/']

    def parse(self, response):
        spiderItem = NewscrawlItem()
        spiderItem['site'] = "Buyouts"

        for i in response.css('.td-block-span6'):
            spiderItem['headlines'] = i.css('.entry-title').xpath('.//a/text()').extract_first()
            spiderItem['dates'] = i.css('.td-post-date').xpath('.//time/@datetime').extract()[0].split('T')[0]
            spiderItem['links'] = i.css('.entry-title').xpath('.//a/@href').extract_first()
            yield spiderItem
