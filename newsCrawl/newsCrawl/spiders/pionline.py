import scrapy
import pandas as pd
from ..items import NewscrawlItem
from scrapy.http import FormRequest
import json
from lxml import etree
import time
from configparser import ConfigParser
import os

class pionline(scrapy.Spider):
    name = 'pionline'
    start_urls = ['https://www.pionline.com/topic/pi-daily-people/']

    def getContent(self, response):
        spiderItem = NewscrawlItem()
        spiderItem['site'] = "pionline"
        spiderItem['headlines'] = response.css('.block-entity-fieldnodetitle').xpath('.//div/h1/text()').extract_first()
        spiderItem['dates'] = response.css('.article-created-date').xpath('.//text()').extract_first()
        spiderItem['links'] = response.request.url
        li = response.css('.field--name-field-paragraph-body').xpath('.//p/text()').extract()
        content = ''.join(li)
        spiderItem['content'] = content

        return spiderItem

    def parse(self, response):
        
        work_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(work_dir,'spiders.cfg')
        print(filepath)
        config_raw = ConfigParser()
        config_raw.read(filepath)
        pageNumberToScrapyForOldPost  = int(config_raw.get('pionline', 'pageNumberToScrapy').strip())
        
        
        for div in response.css('.feature-article-headline'):
            url = div.xpath('.//a/@href').extract_first()
            url = 'https://www.pionline.com'+url
            request = response.follow(url, callback = self.getContent)
            yield request
        

        
        otherPageURLTemplate = 'https://www.pionline.com/views/ajax?_wrapper_format=drupal_ajax'
        
        for pagenumber in range(1,pageNumberToScrapyForOldPost):
            formdata = {"view_name":"topic_article_listing",
                         "view_display_id":"topic_article_listing_block",
                         "view_args":"70401",
                         "view_path":'/taxonomy/term/70401',
                         "view_base_path":"topics/%",
                         "page":str(pagenumber),
                         "_drupal_ajax":"1",
                         "ajax_page_state[theme]":"cpi",
                         "ajax_page_state[theme_token]":"",
                         "ajax_page_state[libraries]":"ad_entity/provider.googletag,ad_entity/viewready,adobe_launch/adobe_launch,anchor_link/drupal.anchor_link,chartbeat/drupal_chartbeat,classy/base,classy/messages,core/html5shiv,core/normalize,cpi/cpi-style,crain_ad_entity_components/initial_load_interstitial_ads,crain_idio/crain_idio.idio_dfp,crain_misc_components/crain_misc_components.crain_moat_ads,crain_misc_components/subscription_js,crain_object/crain_login_js,crain_paywall/paywall_css,crain_paywall/paywall_js,crain_sailthru/crain_sailthru_lib,crain_swiftype_search_component/swiftype_search_config_js,crain_twi_components/crain_twi_js,crain_utility/crain_block_through_code,crain_utility/crain_clickshare_ad_targeting_js,crain_utility/crain_weekly_reporting_cybba,crain_utility/facebook_tracking_pixel,crain_utility/linkedin_partner_tracking,crain_utility/twitter_tracking_pixel,craincore/crain_analytics,craincore/global-scripting,craincore/global-styling,google_analytics/google_analytics,responsive_menu/responsive_menu.breakpoint,responsive_menu/responsive_menu.config,system/base,views/views.module,views_infinite_scroll/views-infinite-scroll"
                         }
            request = FormRequest(otherPageURLTemplate,callback=self.parseRecursion,formdata=formdata)
            yield request
        
    def parseRecursion(self, response):
        content = response.body.decode('gbk').encode('utf-8').decode("unicode-escape").replace('\/','/').replace(']</textarea>','')
        finalcontent = '{"command":"insert"'+content.split('{"command":"insert"')[1]
        
        htmlcode = finalcontent.split('"data":"')[1].replace('","settings":null}','')
        dom = etree.HTML(htmlcode)

        for div in dom.xpath('.//div[@class="feature-article-headline"]'):
            url = div.xpath('.//a/@href')[0]
            url = 'https://www.pionline.com'+url
            request = response.follow(url, callback = self.getContent)
            yield request
        


