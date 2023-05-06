# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    leasingMethod = scrapy.Field()
    houseType = scrapy.Field()
    Floor = scrapy.Field()
    Face = scrapy.Field()
    Area = scrapy.Field()
    # houseNumber = scrapy.Field()
