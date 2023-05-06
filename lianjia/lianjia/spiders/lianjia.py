import scrapy

import sys
sys.path.append("..")
from items import LianjiaItem  # 从items.py中引入MyItem对象


class LianjiaSpider(scrapy.Spider):
    name = "lianjia"
    # allowed_domains = ["gz.lianjia.com"]
    start_urls = ["https://gz.lianjia.com/zufang/"]

    num = 1
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
        items['title'] = response.xpath('/html/body/div[3]/div[1]/div[3]/p/text()').extract_first().split('·')[1].rstrip('                  ')
        items['price'] = response.xpath('//*[@id="aside"]/div[1]/span/text()').extract_first() + '/月'
        items['leasingMethod'] = response.xpath('//*[@id="aside"]/ul/li[1]/text()').extract_first()
        items['houseType'] = response.xpath('//*[@id="aside"]/ul/li[2]/text()').extract_first()
        items['Floor'] = response.xpath('//*[@id="info"]/ul[1]/li[8]/text()').extract_first().split('：')[1]
        items['Face'] = response.xpath('//*[@id="info"]/ul[1]/li[3]/text()').extract_first().split('：')[1]
        items['Area'] = response.xpath('//*[@id="info"]/ul[1]/li[2]/text()').extract_first().split('：')[1]
        # items['houseNumber'] = response.xpath('/html/body/div[3]/div[1]/div[3]/div[1]/i/text()').extract_first()
        yield items
