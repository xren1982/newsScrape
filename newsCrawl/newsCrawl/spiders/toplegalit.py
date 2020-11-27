import scrapy
from ..items import NewscrawlItem
import pandas as pd
from configparser import ConfigParser
import os


class toplegalit(scrapy.Spider):
    name = 'toplegalit'
    start_urls = ['https://toplegal.it/news']
    
    def getContent(self, response):
        spiderItem = NewscrawlItem()
        spiderItem['site'] = "toplegalit :DAL 2004 IL MERCATO LEGALE"
        spiderItem['headlines'] = response.xpath('.//h1[@class="span_newstitolo"]/text()').extract_first()
        spiderItem['dates'] =  response.xpath('.//span[@class="span_datanews"]/text()').extract_first()
        spiderItem['links'] = response.request.url
        li = response.xpath('.//span[@class="resize span_newstesto"]/text()').extract()
        spiderItem['content'] = ' '.join(li)
        li = response.xpath('.//span[@class="resize span_newstesto"]/p/text()').extract()
        pcontent = ' '.join(li)
        spiderItem['content'] = spiderItem['content'] + pcontent
        return spiderItem
    
    def parse(self, response):
        
        work_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(work_dir,'spiders.cfg')
        print(filepath)
        config_raw = ConfigParser()
        config_raw.read(filepath)
        pageNumberToScrapyForOldPost  = int(config_raw.get('toplegalit', 'pageNumberToScrapy').strip())
        
        for div in response.xpath('.//a[@class="span_newsarchiviotitolo"]'):
            url = div.xpath('.//@href').extract_first()
            request = response.follow(url, callback = self.getContent)
            yield request
        
        otherPageURLTemplate = 'https://toplegal.it/news/'
        
        for pagenumber in range(2,pageNumberToScrapyForOldPost+2):
            otherPageURL = otherPageURLTemplate + str(pagenumber)
            request = response.follow(otherPageURL, callback = self.parseRecursion)
            yield request
    
    def parseRecursion(self, response):
        
        for div in response.xpath('.//a[@class="span_newsarchiviotitolo"]'):
            url = div.xpath('.//@href').extract_first()
            request = response.follow(url, callback = self.getContent)
            yield request