# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewscrawlItem(scrapy.Item):
    site = scrapy.Field()
    headlines = scrapy.Field()
    dates = scrapy.Field()
    links = scrapy.Field()
    content = scrapy.Field()

