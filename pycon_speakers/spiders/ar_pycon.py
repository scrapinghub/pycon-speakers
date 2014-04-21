from scrapy.spider import Spider
from scrapy.http import Request
from scrapy.selector import Selector

from pycon_speakers.items import Speaker

from datetime import date
import re


class ArPyconSpider(Spider):
    """A spider to crawl Argentinian Pycon conference speakers.
    """
    name = 'ar.pycon.org'
    from_year = 2009
    base_url = 'http://ar.pycon.org/{year}/activity/speakers'

    def start_requests(self):
        current_year = date.today().year
        for year in range(self.from_year, current_year):
            url = self.base_url.format(year=year)
            yield Request(url)

    def parse(self, response):
        selector = Selector(response)
        year = re.search('/(\d+)/', response.url).group(1)

        return [Speaker(name=speaker,
                        conference=self.name,
                        year=year)
                for speaker in selector.xpath(
                '//div[@id="content"]/h2/text() | '
                '(//div[@id="content"]/div[@class="frame"] | '
                '//div[@class="frame"])/h3/text()').extract()]
