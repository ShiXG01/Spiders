import scrapy

import sys
sys.path.append("..")
from items import AnjukeItem  # 从items.py中引入MyItem对象


class AnjukeSpider(scrapy.Spider):
    name = "anjuke"
    # allowed_domains = ["zu.anjuke.com"]
    start_urls = ["https://gz.zu.anjuke.com/fangyuan/"]

    page = 1
    num = 1

    def parse(self, response):
        urls = response.xpath('/html/body/div[5]/div[3]/div[1]/div/div[1]/h3/a/@href')
        for url in urls:
            yield scrapy.Request(url.root, callback=self.detail_parse)

        if self.page < self.num:
            self.page += 1
            next_url = response.xpath('/html/body/div[5]/div[3]/div[3]/div/a[4]/@href').extract_first()
            yield scrapy.Request(next_url, callback=self.parse)

    def detail_parse(self, response):
        items = AnjukeItem()
        items['title'] = response.xpath('/html/body/div[3]/h1/div/text()').extract_first()
        items['price'] = response.xpath('/html/body/div[3]/div[1]/span[1]/em/b/text()').extract_first() + '元/月'
        items['leasingMethod'] = response.xpath('/html/body/div[3]/div[1]/ul/li[1]/text()').extract_first()
        items['houseType'] = response.xpath('/html/body/div[3]/div[2]/div[1]/ul[1]/li[2]/span[2]/b/text()')[0].root + '室' + \
                             response.xpath('/html/body/div[3]/div[2]/div[1]/ul[1]/li[2]/span[2]/b/text()')[1].root + '厅' + \
                             response.xpath('/html/body/div[3]/div[2]/div[1]/ul[1]/li[2]/span[2]/b/text()')[2].root + '卫'
        items['Floor'] = response.xpath('/html/body/div[3]/div[2]/div[1]/ul[1]/li[5]/span[2]/text()').extract_first()
        items['Face'] = response.xpath('/html/body/div[3]/div[2]/div[1]/ul[1]/li[4]/span[2]/text()').extract_first()
        items['Area'] = response.xpath('/html/body/div[3]/div[2]/div[1]/ul[1]/li[3]/span[2]/b/text()').extract_first()
        # items['Subdivision'] = response.xpath('/html/body/div[3]/div[2]/div[1]/ul[1]/li[8]/a/text()').extract_first()
        items['Subdivision'] = response.xpath('/html/body/div[3]/div[2]/div[1]/ul[1]/li[8]/a/text()')[0].root + '/' +\
                                response.xpath('/html/body/div[3]/div[2]/div[1]/ul[1]/li[8]/a/text()')[1].root + '/' +\
                                response.xpath('/html/body/div[3]/div[2]/div[1]/ul[1]/li[8]/a/text()')[2].root
        yield items
