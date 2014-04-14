from scrapy.spider import Spider
from scrapy.http import Request
from scrapy.selector import Selector

from pycon_speakers.items import Speaker


class StrataSpider(Spider):
    """A spider to crawl Strata conference speakers.
    """
    name = 'strataconf'
    year_list = range(2011, 2014)
    base_url = 'http://strataconf.com/strata{year:d}/public/schedule/speakers'

    def start_requests(self):
        for year in self.year_list:
            meta = {'year': year}
            url = self.base_url.format(year=year)
            yield Request(url, meta=meta)

    def parse(self, response):
        selector = Selector(response)
        return [Speaker(name=speaker,
                        conference=self.name,
                        year=response.meta['year'])
                for speaker in selector.css('span[class$="speaker_name"] a::text').extract()]
