# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class DetailItem(scrapy.Item):
    name = scrapy.Field()       # 项目名称
    url = scrapy.Field()
    desc = scrapy.Field()       # 项目简介
    market = scrapy.Field()     # 市场分析
    image_urls = scrapy.Field()
    images = scrapy.Field()
    images_path = scrapy.Field()
