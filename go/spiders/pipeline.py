__author__ = 'matan'

from scrapy import signals
from scrapy.exceptions import DropItem

class DuplicatesPipeline(object):
    '''
    Shamelessly taken/adapted from http://doc.scrapy.org/en/0.16/topics/item-pipeline.html
    TODO: check performance impact and optimize
    '''
    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['id'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['id'])
            return item

ITEM_PIPELINES = [
    'o2.pipeline.DuplicatesPipeline'
]