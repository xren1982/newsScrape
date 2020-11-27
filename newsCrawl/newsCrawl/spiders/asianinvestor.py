import scrapy
from ..items import NewscrawlItem
import pandas as pd
from configparser import ConfigParser
import os


class asianinvestor(scrapy.Spider):
    name = 'asianinvestor'
    start_urls = ['https://www.asianinvestor.net/category/moves/113']
    
    def getContent(self, response):
        spiderItem = NewscrawlItem()
        spiderItem['site'] = "Asianinvestor : Moves"
        spiderItem['headlines'] = response.xpath('.//h1[@class="header"]/text()').extract_first()
        spiderItem['dates'] =  response.xpath('.//div[@class="date"]/text()').extract_first()
        spiderItem['links'] = response.request.url
        li = response.css('.articleBody').xpath('.//p/text()').extract()
        spiderItem['content'] = ' '.join(li)
        return spiderItem
    
    def parse(self, response):
        
        work_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(work_dir,'spiders.cfg')
        print(filepath)
        config_raw = ConfigParser()
        config_raw.read(filepath)
        pageNumberToScrapyForOldPost  = int(config_raw.get('asianinvestor', 'pageNumberToScrapy').strip())
        
        for h3 in response.xpath('.//h3[@class="header"]'):
            url = h3.xpath('.//a/@href').extract_first()
            url = 'https://www.asianinvestor.net' + url 
            print(url)
            request = response.follow(url, callback = self.getContent)
            yield request
        
        
        
        otherPageURLTemplate = 'https://www.asianinvestor.net/category/getcontent/113?pageNumber=pageNumberToScrapy&pageSize=20'
        
        for pagenumber in range(2,pageNumberToScrapyForOldPost+2):
            otherPageURL = otherPageURLTemplate.replace('pageNumberToScrapy', str(pagenumber))
            request = response.follow(otherPageURL, callback = self.parseRecursion)
            request.headers["Referer"] = 'https://www.asianinvestor.net/category/moves/113'
            request.headers["X-Requested-With"] = 'XMLHttpRequest'
            yield request
    
    def parseRecursion(self, response):
        

        for h3 in response.xpath('.//h3[@class="header"]'):
            url = h3.xpath('.//a/@href').extract_first()
            url = 'https://www.asianinvestor.net' + url 
            print(url)
            request = response.follow(url, callback = self.getContent)
            yield request
        