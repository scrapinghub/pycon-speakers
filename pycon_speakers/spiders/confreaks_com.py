

from urlparse import urljoin

from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request

from pycon_speakers.loaders import SpeakerLoader


class PyConSpider(Spider):
    name = 'confreak.com'
    base_url = "http://confreaks.com/"

    def start_requests(self):
        url = "http://confreaks.com/events"
        yield Request(url, callback=self._parse_events)


    def _parse_events(self, response):
        for event in Selector(response).xpath("//div[@class = 'event-box-inner']"):
            eventname = event.xpath('./span/strong/a/text()').extract()[0]
            year = eventname[-4:]
            if year.isdigit():
                conf_name = eventname[:-4]
                video_url = event.xpath('./a/@href').extract()[0]
                meta = {'year': year, 'conference': conf_name}
                yield Request(self.base_url + video_url, meta=meta,
                              callback=self._parse_video)


    def _parse_video(self, response):
        for section in Selector(response).xpath("//div[@class = 'videos']//div[@class = 'presenters']/a"):
            il = SpeakerLoader(selector=section)
            il.add_xpath('name', ".")
            il.add_value('conference', str(response.meta['conference']))
            il.add_value('year', str(response.meta['year']))
            yield il.load_item()