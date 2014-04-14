from urlparse import urljoin

from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request

from pycon_speakers.loaders import SpeakerLoader


class RmRubySpider(Spider):
    name = 'rockymtnruby.com'
    
    def start_requests(self):
        scraping_dict = {2010: [('http://confreaks.com/events/mountainrb2010', self._parse_video)],
                        2011: [('http://confreaks.com/events/rockymtnruby2011', self._parse_video)],
                        2012: [("http://rockymtnruby.com/{0}", self._parse_2012),
                                ("http://rockymtnruby.com/{0}/workshop", self._parse_workshop_2012)
                                ],
                        2013: [("http://rockymtnruby.com/{0}", self._parse_2013),
                                ("http://rockymtnruby.com/{0}/workshops", self._parse_workshop_2013)
                                ]
                        }

        for year in scraping_dict.keys():
            meta = {'year': year}
            for (url, callback) in scraping_dict[year]:
                yield Request(url.format(year), meta=meta,
                              callback=callback)

    def _parse_video(self, response):
        for section in Selector(response).xpath("//div[@class = 'videos']//div[@class = 'presenters']/a"):
            il = SpeakerLoader(selector=section)
            il.add_xpath('name', ".")
            il.add_value('year', str(response.meta['year']))
            yield il.load_item()

    def _parse_2012(self, response):
        for section in Selector(response).xpath("//div[contains(@class,'speaker')]"):
            il = SpeakerLoader(selector=section)
            il.add_xpath('name', "./a/p")
            il.add_value('year', str(response.meta['year']))
            yield il.load_item()

    def _parse_workshop_2012(self, response):
        for section in Selector(response).xpath("//div[contains(@class,'speaker')]"):
            for name in section.xpath(".//p/text()").extract():
                il = SpeakerLoader(selector=section)
                il.add_value('name', name)
                il.add_value('year', str(response.meta['year']))
                yield il.load_item()  

    def _parse_2013(self, response):
        for section in Selector(response).xpath("//div[contains(@class,'speaker')]"):
            il = SpeakerLoader(selector=section)
            il.add_xpath('name', "./a[@class='name']")
            il.add_value('year', str(response.meta['year']))
            yield il.load_item()

    def _parse_workshop_2013(self, response):
        for section in Selector(response).xpath("//div[contains(@id,'workshop')]"):
            names = section.xpath(".//h2/text()").extract()[0]
            for name in self._split_names(names):
                il = SpeakerLoader(selector=section)
                il.add_value('name', name)
                il.add_value('year', str(response.meta['year']))
                yield il.load_item()        

    def _split_names(self, names):
        name_list = []
        for name in names.split(','):
            name_list.extend(name.split(' with '))
        return name_list