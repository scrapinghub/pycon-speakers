from urlparse import urljoin

from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request

from pycon_speakers.items import Speaker

class PyConSpider(Spider):
    name = 'us.pycon.org'
    base_url = 'http://us.pycon.org/%s/schedule/talks/list/'

    def __init__(self, *args, **kwargs):
        self.years = kwargs.get('years', '').split(',')

    def start_requests(self):
        for year in self.years or [2014, 2013, 2012, 2011]:
            yield Request("https://us.pycon.org/%s/schedule/" % str(year), callback=self.follow_presentation_links, meta={'conf_year': year})

    def follow_presentation_links(self, response):
        sel = Selector(response)
        for link in sel.xpath("//a[contains(@href, '/presentation/') or contains(@href, '/presentations/')]/@href").extract():
            yield Request(urljoin(response.url, link), callback=self.scrape_speakers, meta=response.meta)

    def scrape_speakers(self, response):
        sel = Selector(response)
        conf_year = response.meta['conf_year']
        speaker =  sel.xpath("//a[contains(@href, '/speaker/profile/')]/text()").extract()[0]
        yield Speaker(name=speaker, year=conf_year)


