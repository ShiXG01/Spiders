import scrapy

import sys
sys.path.append("..")
from items import LianjiaItem  # 从items.py中引入MyItem对象


class LianjiaSpider(scrapy.Spider):
    name = "lianjia"
    # allowed_domains = ["gz.lianjia.com"]
    start_urls = ["https://gz.lianjia.com/zufang/"]

    num = 10
    page = 1

    def parse(self, response):
        divs = response.xpath('//*[@id="content"]/div[1]/div[1]/div/div/p[1]/a/@href')
        for url in divs:
            detail_url = response.urljoin(url.root)
            yield scrapy.Request(url=detail_url, callback=self.parse_detail)

        if self.page < self.num:
            self.page += 1
            yield scrapy.Request('https://gz.lianjia.com/zufang/pg{}/'.format(self.page), callback=self.parse)

    def parse_detail(self, response):
        items = LianjiaItem()
        items['title'] = response.xpath()
