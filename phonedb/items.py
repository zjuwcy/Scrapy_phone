# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

"""
class BrandItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    count = scrapy.Field()
    url = scrapy.Field()
"""
class ModelItem(scrapy.Item):
    name = scrapy.Field()
    content = scrapy.Field()
    url = scrapy.Field()

    image_urls = scrapy.Field()
    images = scrapy.Field()
    image_paths = scrapy.Field()


