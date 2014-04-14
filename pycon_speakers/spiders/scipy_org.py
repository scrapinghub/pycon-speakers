import re

from scrapy.spider import Spider
from scrapy.selector import Selector

from pycon_speakers.loaders import SpeakerLoader


class SciPySpider(Spider):
    """A spider to crawl SciPy's conference speakers.

    At the time, it only extracts talks and not lightning talks or tutorials.

    TODO:

        - Store talk title for further reference because an author might show
          up multiple times in a conference..
        - Store conference name to tell which conference the author
          participated in the same year.

    """
    name = 'scipy.org'
    # These are the links directly to the conference schedule. It was not worth
    # to write the code to crawl those links from the site compared to hardcode
    # them here.
    start_urls = [
        'http://conference.scipy.org/SciPy2008/conference.html',
        'http://conference.scipy.org/SciPy2009/schedule.html',
        'http://conference.scipy.org/scipy2010/schedule.html',
        'http://conference.scipy.org/scipy2011/talks.php',
        'http://conference.scipy.org/scipy2012/schedule/conf_schedule_1.php',
        'http://conference.scipy.org/scipy2012/schedule/conf_schedule_2.php',
        'http://conference.scipy.org/scipy2013/conference_talks_schedule.php',
    ]
    year_re = re.compile('/scipy(\d{4})/', re.I)

    def parse(self, response):
        year = self.year_re.search(response.url).group(1)
        response.meta['year'] = year
        callback = getattr(self, 'parse_%s' % year, None)
        if callback:
            return callback(response)

    def parse_2008(self, response):
        sel = Selector(response)
        talk_author_re = re.compile('^(?P<title>.+) \((?P<authors>.+?)\)$')
        for event in sel.css('.section > p::text').extract():
            # For some reason, some entries have the character '\n' between the
            # talk name/author.
            event = event.replace('\n', ' ').strip()
            m = talk_author_re.search(event)
            if m:
                data = talk_author_re.search(event).groupdict()
                for author in data['authors'].split(','):
                    sl = SpeakerLoader(selector=sel, response=response)
                    sl.add_value('name', author)
                    sl.add_value('year', response.meta['year'])
                    sl.add_value('conference', 'SciPy')
                    yield sl.load_item()

    def parse_2009(self, response):
        sel = Selector(response)
        author_re = '<strong>.+</strong>.+\((.+)\)<'
        for authors in sel.css('.section > p').re(author_re):
            # There are few multiple authors entries, some of them separated by
            # '&' and others with comma. The problem comes from entires with
            # author plus institution, i.e.: "Armando Sole, ESRF, France".
            # For now, we extract only the first author.
            author = authors.partition(',')[0]
            sl = SpeakerLoader(selector=sel, response=response)
            sl.add_value('name', author)
            sl.add_value('year', response.meta['year'])
            sl.add_value('conference', 'SciPy')
            yield sl.load_item()

    def parse_2010(self, response):
        sel = Selector(response)
        for authors in sel.css('ul > li > em::text').extract():
            for author in authors.split(','):
                sl = SpeakerLoader(selector=sel, response=response)
                sl.add_value('name', author)
                sl.add_value('year', response.meta['year'])
                sl.add_value('conference', 'SciPy')
                yield sl.load_item()

    def parse_2011(self, response):
        # The 2011 version is highly similar to 2010 layout.
        return self.parse_2010(response)

    def parse_2012(self, response):
        sel = Selector(response)
        # Here we take a pure-regex approach as the layout varies between the
        # entries a little and the authors text have a fair uniform pattern.
        for author in sel.css('#registrants_table').re('>\s*-\s*(.+?)\s*(?:$|<)'):
            if author == '--':  # No author.
                continue
            sl = SpeakerLoader(selector=sel, response=response)
            sl.add_value('name', author)
            sl.add_value('year', response.meta['year'])
            sl.add_value('conference', 'SciPy')
            yield sl.load_item()

    def parse_2013(self, response):
        sel = Selector(response)
        # Probably this is the nicest layout of all versions.
        for authors in sel.css('.authors::text').extract():
            # FIXME: few entries miss the multiple-author separator ';'.
            for author in authors.split(';'):
                sl = SpeakerLoader(selector=sel, response=response)
                # FIXME: most author entry have the institution at the end.
                sl.add_value('name', author)
                sl.add_value('year', response.meta['year'])
                sl.add_value('conference', 'SciPy')

                yield sl.load_item()
