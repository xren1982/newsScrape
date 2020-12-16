 # -*- coding: utf-8 -*-
import scrapy
from scrapy import FormRequest,Request
from ..items import NewscrawlItem
from configparser import ConfigParser
import os
 
class avcjSpider(scrapy.Spider):
    name = "avcj"
    allowed_domains = ["www.avcj.com"]
    start_urls = ['https://www.avcj.com/type/news']
    login_url = 'https://www.avcj.com/userlogin'
    
    def getContent(self, response):
        
        spiderItem = NewscrawlItem()
        spiderItem['site'] = "avcj : News"
        spiderItem['headlines'] = response.xpath('.//header[@class="article-header"]').xpath('.//h1[@class="article-title"]/text()').extract_first()
        spiderItem['dates'] =  response.xpath('.//li[@class="author-dateline-time"]/time/text()').extract_first()
        spiderItem['links'] = response.request.url
        li = response.css('.article-page-body-content').xpath('.//p/text()').extract()
        spiderItem['content'] = ' '.join(li)
        return spiderItem
    
    def parse(self, response):
        
        work_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(work_dir,'spiders.cfg')
        print(filepath)
        config_raw = ConfigParser()
        config_raw.read(filepath)
        pageNumberToScrapyForOldPost  = int(config_raw.get('avcj', 'pageNumberToScrapy').strip())
        
        newsURLlist = response.xpath('.//div[@class="list-view"]/article/div[@class="image-text-group-b"]/h5/a/@href').extract()
        for url in newsURLlist:
            request = response.follow(url, callback = self.getContent)
            yield request
        
        otherPageURLTemplate = 'https://www.avcj.com/type/news/page/'
        
        for pagenumber in range(2,pageNumberToScrapyForOldPost+2):
            otherPageURL = otherPageURLTemplate + str(pagenumber)
            request = response.follow(otherPageURL, callback = self.parseRecursion)
            yield request
    
    def parseRecursion(self, response):
        
        newsURLlist = response.xpath('.//div[@class="list-view"]/article/div[@class="image-text-group-b"]/h5/a/@href').extract()
        for url in newsURLlist:
            request = response.follow(url, callback = self.getContent)
            yield request
        
        
    def start_requests(self):
        yield scrapy.Request(self.login_url,callback=self.login)

    def login(self,response):
        unicornHeader = {
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://www.avcj.com/userlogin',
        }
        formdata = {'redirect_url':'https://www.avcj.com/','subscriber_with_institution_loggedin_as_individual':'true','subscriber[email_id]':'prasad.deshmukh@acuris.com','subscriber[password]':'February@1986','myTime':'Yes'}
        yield FormRequest(url = 'https://www.avcj.com/home/verify_subscription_login',headers = unicornHeader,formdata=formdata,callback=self.parse_login)
    

    def parse_login(self,response):
        yield from super().start_requests()
