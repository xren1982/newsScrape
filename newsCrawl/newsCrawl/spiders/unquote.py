import scrapy
from ..items import NewscrawlItem
import pandas as pd

class UnquoteSpider(scrapy.Spider):
    name = 'unquote'
    start_urls = ['http://www.unquote.com/category/funds/']

    def parse(self, response):
        spiderItem = NewscrawlItem()
        spiderItem['site'] = "Unquote: An Acuris Company"

        for i in response.css('article'):
            h = i.css('.listings-article-title').xpath('.//a/text()').extract()
            d = i.css('.article-meta-details').xpath('.//li/time/@datetime').extract()
            if len(h) > 0:
                spiderItem['headlines'] = h[0]
                if len(d) == 0:
                    spiderItem['dates'] = pd.Timestamp("today").strftime("%m/%d/%Y")
                else:
                    spiderItem['dates'] = d[0].split('T')[0]
                spiderItem['links'] = i.css('.listings-article-title').xpath('.//a/@href').extract_first()
                yield spiderItem
