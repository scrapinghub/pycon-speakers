from scrapy.spider import Spider
from scrapy.http import Request

from pycon_speakers.items import Speaker


class FosdemSpider(Spider):
    """A spider to crawl Fosdem conference speakers.
    """
    name = 'fosdem.org'

    def start_requests(self):
        yield Request('https://fosdem.org/2015/schedule/events/')

    def parse(self, response):
        for speaker in response.xpath('//tr/td[2]/a/text()').extract():
            yield Speaker(
                name=speaker,
                conference=self.name,
                year=2015)
