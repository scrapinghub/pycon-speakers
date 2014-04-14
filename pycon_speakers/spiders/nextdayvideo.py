import json, re
from scrapy.spider import Spider
from pycon_speakers.items import Speaker


class NextDayVideoSpider(Spider):
    name = 'nextdayvideo.com'
    start_urls = ['http://veyepar.nextdayvideo.com/api/csp/?format=json']

    def parse(self, response):
        for conference in json.loads(response.body_as_unicode()):
            conference_name = conference['name']
            for show_set in conference['show_set']:
                set_name = show_set['name']
                year_match = re.search('20\d\d', set_name)
                if not year_match:
                    self.log("skipping %s, set %s: missing year" %
                        (conference_name, set_name))
                    continue
                year = year_match.group()
                for episode in show_set['episode_set']:
                    authors = episode.get('authors')
                    if not authors:
                        # lightning talks, panels, etc.
                        continue
                    yield Speaker(
                        name=authors,
                        conference=conference_name,
                        year=year
                    )
