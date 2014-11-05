import json

from scrapy.spider import Spider
from scrapy.http import Request

from pycon_speakers.items import Speaker


class EsPyconSpider(Spider):
    """A spider to crawl Spanish Pycon conference speakers.
    """
    name = 'es.pycon.org'

    def start_requests(self):
        # 2013 (api based)
        yield Request(
            'http://2013.es.pycon.org/api/v1/speakers/?format=json',
            headers={'Accept': 'application/json'},
            callback=self.parse_2013)

        # 2014
        yield Request(
            'http://2014.es.pycon.org/talks#horarios',
            callback=self.parse_2014)

    def parse_2013(self, response):
        json_data = json.loads(response.body_as_unicode())
        for speaker in json_data:
            yield Speaker(
                name=speaker['name'],
                conference=self.name,
                year=2013)

    def parse_2014(self, response):
        for speaker in response.xpath('//h1[@class="text-center"]'):
            yield Speaker(
                name=speaker.xpath('text()')[0].extract().strip(),
                conference=self.name,
                year=2014)
