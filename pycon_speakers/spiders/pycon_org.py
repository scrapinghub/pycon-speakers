from urlparse import urljoin

from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request

from pycon_speakers.items import Speaker


class PyConSpider(Spider):
    name = 'us.pycon.org'
    base_url = 'http://us.pycon.org/%s/schedule/talks/list/'
    years = None

    def start_requests(self):
        years = self.years.split(',') if self.years else range(2011, 2015)
        for year in years:
            yield Request("https://us.pycon.org/{0}/schedule/".format(year), meta={'year': year})

    def parse(self, response):
        sel = Selector(response)
        for link in sel.xpath("//a[contains(@href, '/presentation/') "
                              "or contains(@href, '/presentations/')]/@href").extract():
            yield Request(urljoin(response.url, link),
                          callback=self.scrape_speakers,
                          meta=response.meta)

    def scrape_speakers(self, response):
        sel = Selector(response)
        speaker =  sel.xpath("//a[contains(@href, '/speaker/profile/')]/text()").extract()[0]
        yield Speaker(name=speaker, year=response.meta['year'])
