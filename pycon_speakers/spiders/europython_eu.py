from urlparse import urljoin

from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request

from pycon_speakers.loaders import SpeakerLoader


class EuroPython(Spider):
    name = 'europython.eu'
    years = '2006,2008,2009,2010,2011,2012,2013,2014'

    def start_requests(self):
        years = [int(x) for x in self.years.split(',')]
        for year in years:
            url = 'http://lanyrd.com/{0}/europython/speakers/'
            callback = self.parse
            if year >= 2011:
                url = 'https://ep2013.europython.eu/ep{0}'
                callback = self.parse_new
            yield Request(url.format(year), callback=callback, meta={'cookiejar': year})

    def parse(self, response):
        sel = Selector(response)
        speakers = sel.css('div.mini-profile')
        for speaker in speakers:
            il = SpeakerLoader(selector=speaker)
            il.add_css('name', ".name > a::text")
            il.add_css('image_urls', "img::attr(src)")
            il.add_value('year', str(response.meta['cookiejar']))
            il.add_value('conference', 'EuroPython')
            yield il.load_item()
        # pagination
        pages = sel.css('.pagination a::attr(href)').extract()
        for page in pages:
            yield Request(urljoin(response.url, page), meta=response.meta)

    def parse_new(self, response):
        sel = Selector(response)
        speakers = sel.css('.archive .talk .speakers > .speaker')
        for speaker in speakers:
            il = SpeakerLoader(selector=speaker)
            il.add_value('conference', 'EuroPython')
            il.add_css('name', "span::text")
            il.add_css('image_urls', "a > img::attr(src)", lambda x:
                        [urljoin(response.url, y) for y in x])
            il.add_value('year', str(response.meta['cookiejar']))
            yield il.load_item()

