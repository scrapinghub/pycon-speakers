# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class GenderPipeline(object):

    def process_item(self, item, spider):
        item['gender'] = self._infer_gender(item)
        return item

    def _infer_gender(self, item):
        return 'unknown'
