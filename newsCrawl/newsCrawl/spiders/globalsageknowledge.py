import scrapy
from ..items import NewscrawlItem
import pandas as pd
from configparser import ConfigParser
import os

class GlobenewswireSpider(scrapy.Spider):
    name = 'globalsageknowledge'
    start_urls = ['http://globalsageknowledge.com/category/daily-moves/']
    
    def parse(self, response):
        
        work_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(work_dir,'spiders.cfg')
        print(filepath)
        config_raw = ConfigParser()
        config_raw.read(filepath)
        pageNumberToScrapyForOldPost  = int(config_raw.get('globalsageknowledge', 'pageNumberToScrapy').strip())
        
        spiderItem = NewscrawlItem()
        spiderItem['dates'] = response.xpath('.//time/text()').extract_first()
        spiderItem['site'] = "Globalsage Knowledge : CATEGORY: DAILY PEOPLE MOVES"
        spiderItem['headlines'] = response.xpath('.//h2[@class="entry-title"]/a/text()').extract_first()
        spiderItem['links'] =  response.xpath('.//h2[@class="entry-title"]/a/@href').extract_first()
        spiderItem['content'] =  response.xpath('.//div[@class="entry-content"]').extract_first()
        spiderItem['content'] = spiderItem['content'].replace('<div class="entry-content">','').replace('</div>','').replace('<p>','').replace('</p>','').replace('<strong>','').replace('</strong>','')
        yield spiderItem
        
        otherPageURLTemplate = 'http://globalsageknowledge.com/category/daily-moves/page/'
        
        for pagenumber in range(2,pageNumberToScrapyForOldPost+1):
            otherPageURL = otherPageURLTemplate + str(pagenumber)+'/'
            request = response.follow(otherPageURL, callback = self.parseRecursion)
            yield request
    
    def parseRecursion(self, response):
        
        spiderItem = NewscrawlItem()
        spiderItem['dates'] = response.xpath('.//time/text()').extract_first()
        spiderItem['site'] = "Globalsage Knowledge : CATEGORY: DAILY PEOPLE MOVES"
        spiderItem['headlines'] = response.xpath('.//h2[@class="entry-title"]/a/text()').extract_first()
        spiderItem['links'] =  response.xpath('.//h2[@class="entry-title"]/a/@href').extract_first()
        spiderItem['content'] =  response.xpath('.//div[@class="entry-content"]').extract_first()
        spiderItem['content'] = spiderItem['content'].replace('<div class="entry-content">','').replace('</div>','').replace('<p>','').replace('</p>','').replace('<strong>','').replace('</strong>','')
      

        
        yield spiderItem
        