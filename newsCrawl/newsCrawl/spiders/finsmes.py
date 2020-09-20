import scrapy
from ..items import NewscrawlItem
import pandas as pd

class FinsmesSpider(scrapy.Spider):
    name = 'finsmes'
    #allowed_domains = ['https://www.finsmes.com/']
    start_urls = ['https://www.finsmes.com/']

    def getContent(self, response, data):
        spiderItem = NewscrawlItem()
        spiderItem['site'] = "FINSMES : Real Time VC & Private Equity Deals and News"
        spiderItem['headlines'] = data['headline']
        spiderItem['dates'] = data['date']
        spiderItem['links'] = data['link']
        li = response.css('.entry-content').xpath('.//p/text()').extract()
        spiderItem['content'] = ' '.join(li)
        return spiderItem

    def parse(self, response):
        headline = response.xpath('//div[@class="post-module-content"]/header/h2/a/text()').extract()
        link = response.xpath('//div[@class="post-module-content"]/header/h2/a/@href').extract()
        date = response.css('.published::text').extract()


        dt = list(zip(headline, link, date))
        df = pd.DataFrame(dt, columns=['headline', 'link', 'date'])

        for i in df.index:
            #data['site'] = "FINSMES : Real Time VC & Private Equity Deals and News"
            data = df.iloc[i]
            request = response.follow(df['link'][i], callback = self.getContent)
            request.cb_kwargs['data'] = data
            yield request

