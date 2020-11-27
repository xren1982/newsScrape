import scrapy
from ..items import NewscrawlItem
import pandas as pd
from configparser import ConfigParser
import os

class realdeals(scrapy.Spider):
    name = 'realdeals'
    start_urls = ['https://realdeals.eu.com/articles/category/lp-gp-moves','https://realdeals.eu.com/articles/category/advisory-moves']
    
    def parse(self, response):
        
        for div in response.css('.article__details'):
            url = div.xpath('.//h2/a/@href').extract_first()
            request = response.follow(url, callback = self.parseRecursion)
            yield request
            
    
    def parseRecursion(self, response):
        
        spiderItem = NewscrawlItem()
        spiderItem['dates'] = response.css('.single__article')[0].xpath('.//p/span/text()').extract_first()
        spiderItem['site'] = "realdeals.eu.com"
        spiderItem['headlines'] = response.css('.single__article')[0].xpath('.//h1/text()').extract_first()
        spiderItem['links'] =  response.request.url
        spiderItem['content'] =  response.css('.single__article')[0].xpath('.//h2/text()').extract_first()
       
        yield spiderItem
        