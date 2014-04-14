from urlparse import urljoin

from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request

from pycon_speakers.loaders import SpeakerLoader


class PyConSpider(Spider):
    name = 'confoo.ca'
    years = '2010,2011,2012,2013,2014'

    def start_requests(self):
        url = "http://confoo.ca/en/{0}/speakers"
        years = [int(x) for x in self.years.split(',')]
        for year in years:
            meta = {'year': year}
            yield Request(url.format(year), meta=meta,
                              callback=self._parse)

    def _parse(self, response):
        for section in Selector(response).xpath('//div[@class="speakers"]//div[@class="name"]'):
            il = SpeakerLoader(selector=section)
            il.add_xpath('name', '.')
            il.add_value('year', str(response.meta['year']))
            yield il.load_item()


