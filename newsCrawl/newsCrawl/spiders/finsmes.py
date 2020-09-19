import scrapy
from ..items import NewscrawlItem
import pandas as pd

class FinsmesSpider(scrapy.Spider):
    name = 'finsmes'
    #allowed_domains = ['https://www.finsmes.com/']
    start_urls = ['https://www.finsmes.com/']

    def parse(self, response):
        headline = response.xpath('//div[@class="post-module-content"]/header/h2/a/text()').extract()
        link = response.xpath('//div[@class="post-module-content"]/header/h2/a/@href').extract()
        date = response.css('.published::text').extract()
        spiderItem = NewscrawlItem()

        dt = list(zip(headline, link, date))
        df = pd.DataFrame(dt, columns=['headline', 'link', 'date'])

        for i in df.index:
            spiderItem['site'] = "FINSMES : Real Time VC & Private Equity Deals and News"
            spiderItem['headlines'] = df['headline'][i]
            spiderItem['dates'] = df['date'][i]
            spiderItem['links'] = df['link'][i]

            yield spiderItem


