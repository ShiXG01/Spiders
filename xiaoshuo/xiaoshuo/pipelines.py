# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class XiaoshuoPipeline:

    def open_spider(self, spider):
        self.file = open('shenxu.txt', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        title = item['title']
        content = item['content']
        info = title + '\n\n' + content + '\n\n'
        self.file.write(info)
        return item

    def close_spider(self, spider):
        self.file.close()
