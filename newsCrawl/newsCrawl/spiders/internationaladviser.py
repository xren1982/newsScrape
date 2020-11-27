import scrapy
from ..items import NewscrawlItem
import pandas as pd
from configparser import ConfigParser
import os

class internationaladviser(scrapy.Spider):
    name = 'internationaladviser'
    start_urls = ['https://international-adviser.com/category/industry/people-moves/']
    
    def getContent(self,response):
        spiderItem = NewscrawlItem()
        spiderItem['dates'] = response.xpath('.//p[@class="article-date"]/text()').extract()[1].split(',')[1].strip()
        spiderItem['site'] = "International adviser : HOME / INDUSTRY / PEOPLE MOVES"
        spiderItem['headlines'] = response.xpath('.//h1[@class="title-single"]/text()').extract_first()
        spiderItem['links'] = response.request.url
        li = response.xpath('.//div[@class="after-image text-content"]/p/text()').extract()
        spiderItem['content'] = ' '.join(li)

        return spiderItem

    
    def parse(self, response):
        
        work_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(work_dir,'spiders.cfg')
        print(filepath)
        config_raw = ConfigParser()
        config_raw.read(filepath)
        pageNumberToScrapyForOldPost  = int(config_raw.get('internationaladviser', 'pageNumberToScrapy').strip())
        
        for div in response.css('.loop-list-load'):
            for div2 in div.css('.content-des'):
                urls = div2.xpath('.//a/@href').extract()
                if len(urls) > 1:
                    url = urls[1]
                else:
                    url = urls[0]
                request = response.follow(url, callback = self.getContent)
                yield request
            
        
        otherPageURLTemplate = 'https://international-adviser.com/category/industry/people-moves/page/'
        
        for pagenumber in range(2,pageNumberToScrapyForOldPost+1):
            otherPageURL = otherPageURLTemplate + str(pagenumber)+'/'
            request = response.follow(otherPageURL, callback = self.parseRecursion)
            yield request
    
    def parseRecursion(self, response):
        for div in response.css('content-des'):
            url = div.xpath('.//a/@href').extract_first()
            request = response.follow(url, callback = self.getContent)
            yield request
        