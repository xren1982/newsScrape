import scrapy
from ..items import NewscrawlItem


class VenturecapitaljournalSpider(scrapy.Spider):
    name = 'venturecapitaljournal'
    start_urls = ['https://www.venturecapitaljournal.com/tag/fundraising/']

    def parse(self, response):
        spiderItem = NewscrawlItem()
        spiderItem['site'] = "Venture Capital Journal"

        for i in response.css('.td-block-span6'):
            spiderItem['headlines'] = i.css('.entry-title').xpath('.//a/text()').extract_first()
            spiderItem['dates'] = i.css('.td-post-date').xpath('.//time/@datetime').extract()[0].split('T')[0]
            spiderItem['links'] = i.css('.entry-title').xpath('.//a/@href').extract_first()
            yield spiderItem
