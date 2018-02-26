# -*- coding: utf-8 -*-
"""
项目测试入口，正式环境建议用scrapyd等部署
"""

from scrapy import cmdline


def test():
    # cmdline.execute("scrapy crawl index".split())
    cmdline.execute("scrapy crawl category".split())


if __name__ == "__main__":
    test()
