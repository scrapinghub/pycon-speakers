from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request

from pycon_speakers.loaders import SpeakerLoader

class OsConSpider(Spider):
    name = 'oscon.com'
    years = '2013,2012,2011,2010,2009,2008,2007'
    base_url = 'http://www.oscon.com/oscon{year}/public/schedule/speakers'

    def start_requests(self):
        years = [int(x) for x in self.years.split(',')]
        for year in years:
            meta = {'year': year}
            url = self.base_url.format(year=year)
            yield Request(url, meta=meta)

    def parse(self, response):
        sel = Selector(response)
        for speaker in sel.xpath('//span[@class="en_speaker_name"]').extract():
            il = SpeakerLoader(response=response)
            il.add_value('name', speaker)
            il.add_value('year', str(response.meta['year']))
            il.add_value('conference', 'OSCON')
            yield il.load_item()
