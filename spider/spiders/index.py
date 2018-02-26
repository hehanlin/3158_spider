# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from spider.items import DetailItem
from re import compile, S


class IndexSpider(CrawlSpider):
    name = 'index'
    allowed_domains = ['www.3158.cn']
    start_urls = ['http://www.3158.cn/']

    rules = (
        Rule(LinkExtractor(allow=r'www\.3158\.cn/corpname/.*'), callback='parse_corp', follow=True),
        Rule(LinkExtractor(allow=r'www\.3158\.cn/xiangmu/\d+/xmjs\.html'), callback='parse_detail', follow=True),
        Rule(LinkExtractor(), callback='parse_follow', follow=True)
    )

    def parse_follow(self, response):
        hrefs = response.xpath("//a/@href").extract()
        corp_reg = compile(r'www\.3158\.cn/corpname/.*', S)
        detail_reg = compile(r'www\.3158\.cn/xiangmu/\d+/xmjs\.html', S)
        for each in hrefs:
            if corp_reg.search(each):
                yield scrapy.Request(url=response.urljoin(each), callback=self.parse_corp)
            elif detail_reg.search(each):
                yield scrapy.Request(url=response.urljoin(each), callback=self.parse_detail)
            else:
                yield scrapy.Request(url=response.urljoin(each), callback=self.parse_follow)

    def parse_corp(self, response):
        # 项目详情url
        detail_url = response.xpath("//div[@id='header-info']/div[@class='subnav']/ul/li[2]/a/@href").get()
        yield scrapy.Request(url=detail_url, callback=self.parse_detail)

    def parse_detail(self, response):
        # 解析项目详情
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

    def parse_img(self, response):
        item = response.meta['item']
        item['image_urls'] = response.xpath("//div[@class='pic-box']//img/@src").extract()
        yield item

