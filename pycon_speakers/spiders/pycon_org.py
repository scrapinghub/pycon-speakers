from urlparse import urljoin

from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request

from pycon_speakers.loaders import SpeakerLoader

ARCHIVE = {2008: '20081216074155',
           2009: '20091223043735',
           2010: '20101213081713'}

class PyConSpider(Spider):
    name = 'us.pycon.org'
    years = '2008,2009,2010,2011,2012,2013,2014'

    def start_requests(self):
        years = [int(x) for x in self.years.split(',')]
        for year in years:
            meta = {'year': year}
            if 2011 <= year <= 2014:
                url = "https://us.pycon.org/{0}/schedule/"
                yield Request(url.format(year), meta=meta)
            elif 2008 <= year <= 2010:
                url = 'https://web.archive.org/web/{0}/http://us.pycon.org/{1}/conference/talks/'
                yield Request(url.format(ARCHIVE[year], year), meta=meta,
                              callback=self._parse_2010)

    def parse(self, response):
        sel = Selector(response)
        for link in sel.xpath("//a[contains(@href, '/presentation/') or "
                              "    contains(@href, '/presentations/')]"
                              "/@href").extract():
            yield Request(urljoin(response.url, link),
                          callback=self._follow_speakers,
                          meta=response.meta)

    def _follow_speakers(self, response):
        il = SpeakerLoader(response=response)
        il.add_xpath('name', "//a[contains(@href, '/speaker/profile/')]")
        il.add_value('year', str(response.meta['year']))
        yield il.load_item()

    def _parse_2010(self, response):
        for section in Selector(response).xpath('//div[@class="proposal_list_summary"]'):
            il = SpeakerLoader(selector=section)
            il.add_xpath('name', './span[1]')
            il.add_value('year', str(response.meta['year']))
            yield il.load_item()
