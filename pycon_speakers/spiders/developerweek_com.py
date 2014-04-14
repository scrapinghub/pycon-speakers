

from urlparse import urljoin

from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request

from pycon_speakers.loaders import SpeakerLoader


class PyConSpider(Spider):
    name = 'developerweek.com'
    base_url = "http://confreaks.com/"

    def start_requests(self):
        # url = "http://developerweek2014conferenceexpo.sched.org/directory/speakers"
        # meta = {'year': '2014', 'conference': self.name}
        # yield Request(url, meta=meta,
        #               callback=self._parse_2014)

        url = "http://www.developerweek.com/2013-sf/index/allspeakers"
        meta = {'year': '2013', 'conference': self.name}
        yield Request(url, meta=meta,
                      callback=self._parse_2013)

    def _parse_2013(self, response):
        for section in Selector(response).xpath("//div[@class='data-mid2']/h2[1]/a[1]"):
            il = SpeakerLoader(selector=section)
            il.add_xpath('name', ".")
            il.add_value('conference', str(response.meta['conference']))
            il.add_value('year', str(response.meta['year']))
            yield il.load_item()

    def _parse_2014(self, response):
        for section in Selector(response).xpath("//div[@class='sched-person']"):
            il = SpeakerLoader(selector=section)
            il.add_xpath('name', "./h2/a")
            il.add_value('conference', str(response.meta['conference']))
            il.add_value('year', str(response.meta['year']))
            yield il.load_item()