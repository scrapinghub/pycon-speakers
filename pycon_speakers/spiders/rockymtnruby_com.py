from urlparse import urljoin

from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request

from pycon_speakers.loaders import SpeakerLoader


class RmRubySpider(Spider):
    name = 'rockymtnruby.com'
    year = 2013

    def start_requests(self):
        meta = {'year': self.year}
        if self.year == 2013:
            url = "http://rockymtnruby.com/{0}"
            yield Request(url.format(self.year), meta=meta,
                          callback=self._parse_2013)
            workshop_url =  "http://rockymtnruby.com/{0}/workshops"
            yield Request(workshop_url.format(self.year), meta=meta,
                          callback=self._parse_workshop_2013)

    def _parse_2013(self, response):
        for section in Selector(response).xpath("//div[contains(@class,'speaker')]"):
            il = SpeakerLoader(selector=section)
            il.add_xpath('name', "./a[@class='name']")
            il.add_value('year', str(response.meta['year']))
            yield il.load_item()

    def _parse_workshop_2013(self, response):
        for section in Selector(response).xpath("//div[contains(@id,'workshop')]"):
            for name in section.xpath(".//h2/text()").extract()[0].split(','):
                il = SpeakerLoader(selector=section)
                il.add_value('name', name)
                il.add_value('year', str(response.meta['year']))
                yield il.load_item()        