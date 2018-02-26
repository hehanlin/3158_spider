# -*- coding: utf-8 -*-
import scrapy
from re import search
from math import ceil
from spider.items import DetailItem


class CategorySpider(scrapy.Spider):
    name = 'category'
    allowed_domains = ['www.3158.cn']
    start_urls = ['http://www.3158.cn/xiangmu/']

    def parse(self, response):
        categorys = response.xpath("//div[contains(@class, 'txtbox')]//li/a")
        for each in categorys:
            url = each.xpath("@href").get()
            num = search(r"(\d+)", each.xpath("span/text()").get()).group(1)
            pages = int(ceil(int(num)/20))
            for page in range(1, pages):
                yield scrapy.Request(url=url+"?pt=all&page=%s" % page, callback=self.parse_list)

    def parse_list(self, response):
        pids = response.xpath("//div[@class='pro-info']/h4/a/@pid").extract()
        for each in pids:
            url = "http://www.3158.cn/xiangmu/%s/xmjs.html" % each
            yield scrapy.Request(url=url, callback=self.parse_detail)

    def parse_detail(self, response):
        # 解析项目详情
        try:
            detail_node = response.xpath("//div[@class='web680']//div[@class='bd']")
            name = response.xpath("//div[@class='hd-left-info']/h2/text()").get()       # 项目名称
            url = response.url
            desc = "".join(detail_node.xpath("div[1]//text()").extract()).strip()      # 项目简介
            market = "".join(detail_node.xpath("div[2]//text()").extract()).strip()    # 市场分析
            item = DetailItem(
                name=name,
                url=url,
                desc=desc,
                market=market
            )
            img_url = response.xpath("//div[@class='item-nav']/ul/li[4]/a/@href").get()
            img_req = scrapy.Request(url=img_url, callback=self.parse_img)
            img_req.meta['item'] = item
            yield img_req
        except:
            try:
                name = response.xpath("//span[@class='itm-titbox']/text()").get()
                url = response.url
                desc_node = response.xpath("//div[@class='all-itm-info']//div[@class='bd']")
                desc = "".join(desc_node.xpath("ul[1]//text()").extract()).strip()
                market = "".join(desc_node.xpath("ul[2]//text()").extract()).strip()
                item = DetailItem(
                    name=name,
                    url=url,
                    desc=desc,
                    market=market
                )
                img_url = response.xpath("//div[@class='itm-nav']/a[4]/@href").get()
                img_req = scrapy.Request(url=img_url, callback=self.parse_img)
                img_req.meta['item'] = item
                yield img_req
            except:
                pass

    def parse_img(self, response):
        try:
            item = response.meta['item']
            item['image_urls'] = response.xpath("//div[contains(@class, 'pic-box')]//img/@src").extract()
            yield item
        except:
            pass

