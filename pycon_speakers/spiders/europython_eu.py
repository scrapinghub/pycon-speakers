from urlparse import urljoin

from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request

from pycon_speakers.loaders import SpeakerLoader


class EuroPython(Spider):
    name = 'europython.eu'
    years = '2006,2008,2009,2010,2011,2012,2013,2014'
    start_url = 'http://lanyrd.com/{0}/europython/speakers/'

    def start_requests(self):
        years = [int(x) for x in self.years.split(',')]
        for year in years:
            yield Request(self.start_url.format(year), meta={'cookiejar': year})

    def parse(self, response):
        sel = Selector(response)
        speakers = sel.css('div.mini-profile')
        for speaker in speakers:
            il = SpeakerLoader(selector=speaker)
            il.add_css('name', ".name > a::text")
            il.add_css('image_urls', "img::attr(src)")
            il.add_value('year', str(response.meta['cookiejar']))
            yield il.load_item()
        # pagination
        pages = sel.css('.pagination a::attr(href)').extract()
        for page in pages:
            yield Request(urljoin(response.url, page), meta=response.meta)
