# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class LianjiaPipeline:
    def open_spider(self, spider):
        self.file = open('house.txt', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        info = str({
            '标题': item['title'],
            '房租': item['price'],
            '组凭方法': item['leasingMethod'],
            '房屋类型': item['houseType'],
            '楼层': item['Floor'],
            '朝向': item['Face'],
            '面积': item['Area']
        }) + '\n'
        self.file.write(info)
        return item

    def close_spider(self, spider):
        self.file.close()
