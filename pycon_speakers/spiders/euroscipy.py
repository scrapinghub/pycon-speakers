import urllib

from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.spider import Spider

from pycon_speakers.loaders import SpeakerLoader


class EuroSciPySpider(Spider):
    """A spider to crawl EuroSciPy's conference speakers.
    """
    name = 'euroscipy.org'
    # Available years, even thought 2013 is not available at the moment.
    year_list = map(str, range(2008, 2014))
    # The site uses a nice web framework (CubicWeb) which allows to query
    # the data directly.
    talk_rql = 'Any X,AA WHERE X is_instance_of Conference, X modification_date AA, X url_id "euroscipy{year}"'
    # TODO: find a 'fname' value that return a machine format output.
    list_url = 'http://archive.euroscipy.org/ajax?rql={rql}&vid=talkslist&__force_display=1&fname=view'

    def start_requests(self):
        for year in self.year_list:
            rql = self.talk_rql.format(year=year)
            url = self.list_url.format(rql=urllib.quote(rql))
            yield Request(url, meta={'year': year})

    def parse(self, response):
        # The parameter __force_display allows to return all talks without
        # pagination.
        sel = Selector(response)
        for author in sel.xpath('//tr/td[2]/text()').extract():
            sl = SpeakerLoader(selector=sel, response=response)
            # TODO: handle/remove affiliation value and possibly multiple
            # authors.
            sl.add_value('conference', 'EuroSciPy')
            sl.add_value('name', author)
            sl.add_value('year', response.meta['year'])
            yield sl.load_item()
