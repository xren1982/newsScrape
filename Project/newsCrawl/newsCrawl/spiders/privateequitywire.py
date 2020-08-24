import scrapy
from ..items import NewscrawlItem
import pandas as pd

class PrivateequitywireSpider(scrapy.Spider):
    name = 'privateequitywire'
    #allowed_domains = ['www.privateequitywire.co.uk/news']
    start_urls = ['http://www.privateequitywire.co.uk/news/']

    def parse(self, response):
        headline =  response.css('.node--view-mode-preview').xpath('//div/section/h2/a/text()').extract()
        link = response.css('.node--view-mode-preview').xpath('//div/section/h2/a/@href').extract()
        spiderItem = NewscrawlItem()

        dt = list(zip(headline, link))
        df = pd.DataFrame(dt, columns=['headline', 'link'])
        df.drop_duplicates(inplace=True)
        print(df.shape)
        df1 = df[~df.link.str.contains('http', case=False)]
        df1['fullLink'] = df1['link'].apply(lambda x: 'https://www.privateequitywire.co.uk'+str(x))
        print(df1)
        print(df1.shape)

        for i in df1.index:
            spiderItem['site'] = "Private Equity Wire"
            spiderItem['headlines'] = df1['headline'][i]
            spiderItem['dates'] = pd.Timestamp("today").strftime("%m/%d/%Y")
            spiderItem['links'] = df1['fullLink'][i]

            yield spiderItem
