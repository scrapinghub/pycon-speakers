from urlparse import urljoin

from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request

from pycon_speakers.loaders import SpeakerLoader

class StrangeLoopSpider(Spider):
    name = 'strangeloop.com'
    start_urls = ['https://thestrangeloop.com/']

    def parse(self, response):
        sel = Selector(response)
        xp_links = sel.xpath("//ul/li/a[contains(@href, '/archive/')]/@href")
        for link in set(xp_links.extract()):
            year = link.rpartition('/')[2]
            yield Request(urljoin(response.url, link),
                    callback=self.parse_speakers, meta={'year': year})

    def parse_speakers(self, response):
        sel = Selector(response)
        for speaker_div in sel.xpath("//div[contains(@class, 'speaker')]"):
            loader = SpeakerLoader(selector=speaker_div)
            loader.add_xpath('name', ".//h5/a[@target='_blank']/text()")
            loader.add_value('year', str(response.meta['year']))
            yield loader.load_item()
            

