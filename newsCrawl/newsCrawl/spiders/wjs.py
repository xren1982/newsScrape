import scrapy
from ..items import NewscrawlItem
import pandas as pd
from scrapy.http import FormRequest
from scrapy.shell import inspect_response


class wjs(scrapy.Spider):
    name = 'wjs'
    # allowed_domains = ['example.com']
    start_urls = ['https://www.wsj.com/']

    def parse(self, response):
        headline = response.css('.typography--serif-display--ZXeuhS5E').xpath('//h3/a/text()').extract()
        link = response.css('.typography--serif-display--ZXeuhS5E').xpath('//h3/a/@href').extract()
        spiderItem = NewscrawlItem()

        dt = list(zip(headline, link))
        df = pd.DataFrame(dt, columns=['headline', 'link'])
        df.drop_duplicates(inplace=True)
        df.sort_values("headline", inplace=True)

        for i in df.index:
            spiderItem['site'] = "The Wall Street Journal."
            spiderItem['headlines'] = df['headline'][i]
            spiderItem['dates'] = pd.Timestamp("today").strftime("%m/%d/%Y")
            spiderItem['links'] = df['link'][i]

            yield spiderItem
