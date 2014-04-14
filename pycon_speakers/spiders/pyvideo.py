import re

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from pycon_speakers.items import Speaker


class PyVideoSpider(CrawlSpider):
    name = 'pyvideo.org'
    allowed_domains = ['pyvideo.org']
    start_urls = ['http://www.pyvideo.org/speaker/']

    rules = (
        # Extract links matching speakers
        Rule(SgmlLinkExtractor(allow=('/speaker/\d+/', )), callback='parse_speaker'),
    )

    def parse_speaker(self, response):
        sel = Selector(response)
        name = sel.xpath('//h1/text()').extract()[0].strip()
        for conf in sel.xpath('//div[@class="video-summary-data"]'):
            speaker = Speaker()
            speaker['name'] = name
            conf_text = conf.select('.//a/text()')[1].extract()
            speaker['conference'] = re.sub('\s20\d\d$','', conf_text)
            speaker['year'] = conf.re('20\d\d')[0]
            yield speaker
