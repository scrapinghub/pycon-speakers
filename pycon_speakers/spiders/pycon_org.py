from urlparse import urljoin

from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request

from pycon_speakers.loaders import SpeakerLoader


class PyConSpider(Spider):
    name = 'us.pycon.org'
    years = '2010,2011,2012,2013,2014'

    def start_requests(self):
        years = [int(x) for x in self.years.split(',')]
        for year in years:
            meta = {'year': year}
            if 2011 <= year <= 2014:
                yield Request("https://us.pycon.org/{0}/schedule/".format(year), meta=meta)
            elif year == 2010:
                yield Request('https://web.archive.org/web/20101213081713/http://us.pycon.org/2010/conference/talks/',
                              callback=self.parse_2010, meta=meta)
            elif year == 2009:
                yield Request('https://web.archive.org/web/20091223043735/http://us.pycon.org/2009/conference/talks',
                              callback=self.parse_2010, meta=meta)
            elif year == 2008:
                yield Request('https://web.archive.org/web/20081216074155/http://us.pycon.org/2008/conference/talks/',
                              callback=self.parse_2010, meta=meta)

    def parse(self, response):
        sel = Selector(response)
        for link in sel.xpath("//a[contains(@href, '/presentation/') "
                              "or contains(@href, '/presentations/')]/@href").extract():
            yield Request(urljoin(response.url, link),
                          callback=self.scrape_speakers,
                          meta=response.meta)

    def scrape_speakers(self, response):
        il = SpeakerLoader(response=response)
        il.add_xpath('name', "//a[contains(@href, '/speaker/profile/')]")
        il.add_value('year', str(response.meta['year']))
        yield il.load_item()

    def parse_2010(self, response):
        for section in Selector(response).xpath('//div[@class="proposal_list_summary"]'):
            il = SpeakerLoader(selector=section)
            il.add_xpath('name', './span[1]')
            il.add_value('year', str(response.meta['year']))
            yield il.load_item()
