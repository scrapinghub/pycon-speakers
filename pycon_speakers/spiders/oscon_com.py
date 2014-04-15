from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request

from pycon_speakers.loaders import SpeakerLoader

ARCHIVE = {
    2001: 'http://conferences.oreillynet.com/cs/os2001/pub/w/os2001/speakers.html',
    2002: '15',
    2003: '23',
    2004: '29',
    2005: '38',
    2006: '46',
    2007: '58',
}


class OsConSpider(Spider):
    name = 'oscon.com'
    years = (
        '2014,2013,2012,2011,2010,2009,2008,2007,2006,2005,2004,2003,2002,2001'
    )
    base_url = 'http://www.oscon.com/oscon{year}/public/schedule/speakers'
    old_base_url = (
        'http://conferences.oreillynet.com/pub/w/{code}/speakers.html')

    def start_requests(self):
        years = [int(x) for x in self.years.split(',')]
        for year in years:
            meta = {'year': year}
            if int(year) < 2008 and int(year) > 2001:
                url = self.old_base_url.format(code=ARCHIVE[year])
                yield Request(url, callback=self.parse_old_format, meta=meta)
            elif int(year) < 2002:
                url = ARCHIVE[year]
                yield Request(url, callback=self.parse_old_format, meta=meta)
            else:
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

    def parse_old_format(self, response):
        sel = Selector(response)
        speakers = sel.xpath('//div[@class="speaker-blurb"]//h3').extract()
        for speaker in speakers:
            il = SpeakerLoader(response=response)
            il.add_value('name', speaker)
            il.add_value('year', str(response.meta['year']))
            il.add_value('conference', 'OSCON')
            yield il.load_item()
        more_speakers = sel.xpath(
            '//span/a[contains(@href, "e_spkr")]//text()').extract()
        for speaker in more_speakers:
            il = SpeakerLoader(response=response)
            il.add_value('name', speaker.replace('N/A', ''))
            il.add_value('year', str(response.meta['year']))
            il.add_value('conference', 'OSCON')
            yield il.load_item()
