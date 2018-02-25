# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from spider.sqlHelper import SqlHelper


class SpiderPipeline(object):

    def __init__(self):
        self.sqlHelper = SqlHelper()

    @classmethod
    def from_crawler(cls, crawler):
        return cls()

    def process_item(self, item, spider):
        item['images_path'] = "|".join(
            [each['path'] for each in item['images']]
        )
        self.sqlHelper.insert((
            item['name'],
            item['url'],
            item['desc'],
            item['market'],
            item['images_path']
        ))
        return item