import scrapy
from ..items import NewscrawlItem
import pandas as pd
from configparser import ConfigParser
import os

class lawasia(scrapy.Spider):
    name = 'lawasia'
    start_urls = ['https://law.asia/category/asia-business-law-journal/as/news/']
    
    def getContent(self,response):
        spiderItem = NewscrawlItem()
        spiderItem['dates'] = response.css('.td-post-header').xpath('.//header/div[@class="td-module-meta-info"]/div/time/text()').extract_first()
        spiderItem['site'] = "Lawasia : ASIA Business Law Journal"
        spiderItem['headlines'] = response.css('.td-post-header').xpath('.//header/h1/text()').extract_first()
        spiderItem['links'] = response.request.url
        li = response.css('.td-post-content').xpath('.//p/text()').extract()
        spiderItem['content'] = ' '.join(li)
        return spiderItem

    
    def parse(self, response):
        
        work_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(work_dir,'spiders.cfg')
        print(filepath)
        config_raw = ConfigParser()
        config_raw.read(filepath)
        pageNumberToScrapyForOldPost  = int(config_raw.get('lawasia', 'pageNumberToScrapy').strip())
        
        for div in response.css('.td_module_1'):
            url = div.xpath(".//h3/a/@href").extract_first()
            print(url)
            request = response.follow(url, callback = self.getContent)
            yield request            
        
        otherPageURLTemplate = 'https://law.asia/category/asia-business-law-journal/as/news/page/'
        
        for pagenumber in range(2,pageNumberToScrapyForOldPost+1):
            otherPageURL = otherPageURLTemplate + str(pagenumber)
            request = response.follow(otherPageURL, callback = self.parseRecursion)
            yield request
    
    def parseRecursion(self, response):
        for div in response.css('.td_module_1'):
            url = div.xpath(".//h3/a/@href").extract_first()
            request = response.follow(url, callback = self.getContent)
            yield request
        