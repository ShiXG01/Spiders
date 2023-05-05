import scrapy


class ByzwwSpider(scrapy.Spider):
    name = "byzww"
    allowed_domains = ["81zw.cc"]
    start_urls = ["https://www.81zw.cc/book/75072/37101656.html"]  # 要爬取的小说的开始位置

    def parse(self, response):
        title = response.xpath('//*[@id="book"]/div[2]/h1/text()').extract_first()
        content = ''.join(response.xpath('//*[@id="content"]/text()').extract()).replace('        ', '').replace('\r\r','\n')

        yield {
            'title': title,
            'content': content
        }

        next_url = response.xpath('//*[@id="book"]/div[2]/div[4]/ul/li[3]/a/@href').extract_first()
        # base_url = 'https://www.81zw.cc{}'.format(next_url)

        if next_url.find('.html') != -1:
            yield scrapy.Request(response.urljoin(next_url), callback=self.parse)
