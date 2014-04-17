from scrapy.spider import Spider
from scrapy.http import Request
from scrapy.selector import Selector

from pycon_speakers.items import Speaker


class PythonBrazilSpider(Spider):
    name = 'pythonbrazil'

    def __init__(self):
        self.conferences = {
            '9': {
                'conference_name': 'Python Brazil [9]',
                'url': 'http://2013.pythonbrasil.org.br/program/confirmed-talks',
                'callback': self.parse_2013,
                'callback_talk': self.parse_talk_2013,
                'year': '2013',
            },
        }

    def start_requests(self):
        for year in self.conferences:
            conference = self.conferences[year]
            yield Request(conference['url'], meta={'conference': conference},
                                             callback=conference['callback'])

    def parse_2013(self, response):
        hxs = Selector(response)
        conference = response.meta['conference']
        for talk in hxs.xpath('//table[contains(@class, "listing")]/tbody/'
                                                               'tr/td[1]/a'):
            url = ''.join(talk.xpath('./@href').extract())
            yield Request(url, meta={'conference': conference},
                               callback=conference['callback_talk'])

    def parse_talk_2013(self, response):
        hxs = Selector(response)
        speaker = Speaker()
        conference = response.meta['conference']
        speaker['name'] = ''.join(hxs.xpath('//span[contains(@class,'
                                            '"speaker_name")]/text()')
                                                                     .extract())
        speaker['conference'] = conference['conference_name']
        speaker['year'] = conference['year']
        yield speaker

