from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request

from pycon_speakers.loaders import SpeakerLoader


class DjangoConEU(Spider):

	name = 'djangocon.eu'
	years = '2014,2013,2012,2011'

	def start_requests(self):
		years = [int(x) for x in self.years.split(',')]
		for year in years:
			if year == 2014:
				url = 'http://{0}.djangocon.eu/talks/'
				callback = self.parse_2014
				yield Request(url.format(year), callback=callback, meta={'cookiejar': year})
			elif year == 2013:
				url = 'http://{0}.djangocon.eu/speakers/'
				callback = self.parse_2013
				yield Request(url.format(year), callback=callback, meta={'cookiejar': year})
			elif year == 2012:
				url = 'http://{0}.djangocon.eu/schedule/'
				callback = self.parse_2012
				yield Request(url.format(year), callback=callback, meta={'cookiejar': year}) 
			elif year == 2011:
				url = 'http://{0}.djangocon.eu/schedule/'
				callback = self.parse_2011
				yield Request(url.format(year), callback=callback, meta={'cookiejar': year})

	def parse_2014(self, response):
		sel = Selector(response)
		speakers = sel.css('.bio')
		for speaker in speakers:
			il = SpeakerLoader(selector=speaker)
			il.add_css('name', '.bio > h3::text')
			il.add_value('year', str(response.meta['cookiejar']))
			yield il.load_item()

	def parse_2013(self, response):
		sel = Selector(response)
		speakers = sel.css(".header")
		for speaker in speakers:
			il = SpeakerLoader(selector=speaker)
			il.add_css('name', '.header::text')
			il.add_value('year', str(response.meta['cookiejar']))
			yield il.load_item()

	def parse_2012(self, response):
		sel = Selector(response)
		speakers = sel.css(".right")
		for speaker in speakers:
			il = SpeakerLoader(selector=speaker)
			il.add_css('name', '.right::text')
			il.add_value('year', str(response.meta['cookiejar']))
			yield il.load_item()

	def parse_2011(self, response):
		sel = Selector(response)
		speakers = sel.css('.speakers')
		for speaker in speakers:
			il = SpeakerLoader(selector=speaker)
			il.add_css('name', '.speakers::text')
			il.add_value('year', str(response.meta['cookiejar']))
			yield il.load_item()