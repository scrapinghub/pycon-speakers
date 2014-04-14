import sexmachine.detector as gender


class GenderPipeline(object):

    def __init__(self):
        self.detector = gender.Detector()

    def process_item(self, item, spider):
        firstname = item['name'].split()[0]
        item['gender'] = self.detector.get_gender(firstname)
        return item

class DefaultsPipeline(object):
    """
    Set default values.

    conference is set to spider name
    """

    def process_item(self, item, spider):
        item.setdefault('conference', spider.name)
        return item
