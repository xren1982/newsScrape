import scrapy
from ..items import NewscrawlItem
import pandas as pd
from configparser import ConfigParser
import os


class fundselectorasia(scrapy.Spider):
    name = 'fundselectorasia'
    start_urls = ['https://fundselectorasia.com/category/news/people-moves/']
    
    def getContent(self, response):
        spiderItem = NewscrawlItem()
        spiderItem['site'] = "Fundselectorasia : Moves"
        spiderItem['headlines'] = response.xpath('.//h1[@class="title-single"]/text()').extract_first()
        spiderItem['dates'] =  response.xpath('.//p[@class="article-date"]/text()').extract()[1].split(',')[1].strip()
        spiderItem['links'] = response.request.url
        li = response.css('.article-body').xpath('.//p/text()').extract()
        spiderItem['content'] = ' '.join(li)
        return spiderItem
    
    def parse(self, response):
        
        work_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(work_dir,'spiders.cfg')
        print(filepath)
        config_raw = ConfigParser()
        config_raw.read(filepath)
        pageNumberToScrapyForOldPost  = int(config_raw.get('fundselectorasia', 'pageNumberToScrapy').strip())
        
        for div in response.xpath('.//div[@class="content-des"]'):
            urls = div.xpath('.//a/@href').extract()
            if len(urls) > 1:
                url = urls[1]
            else:
                url = urls[0]
            request = response.follow(url, callback = self.getContent)
            yield request
        
        
        
        otherPageURLTemplate = 'https://fundselectorasia.com/category/news/people-moves/page/'
        
        for pagenumber in range(2,pageNumberToScrapyForOldPost+2):
            otherPageURL = otherPageURLTemplate + str(pagenumber) + '/'
            request = response.follow(otherPageURL, callback = self.parseRecursion)
            yield request
    
    def parseRecursion(self, response):
        
        for div in response.xpath('.//div[@class="content-des"]'):
            urls = div.xpath('.//a/@href').extract()
            if len(urls) > 1:
                url = urls[1]
            else:
                url = urls[0]
            request = response.follow(url, callback = self.getContent)
            yield request
        