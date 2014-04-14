PyCon Speakers Spider
=====================

This project will:

1.  scrape speakers' names from archived conference websites,
2.  use [SexMachine](https://pypi.python.org/pypi/SexMachine/) to infer gender, and
3.  plot gender ratios for different conferences over time.

The Scrapy team have built a spider that scrapes information about speakers at Python conferences since 2011;
please see the [Scrapy installation guide](http://doc.scrapy.org/en/latest/intro/install.html) for installation instructions.

Please send us pull requests with scrapers for other conferences and time periods
(we'll figure out a naming convention first thing at the sprint).

Running
-------

List available spiders:

    scrapy list

Run a spider:

    scrapy crawl us.pycon.org

Scrapy Cloud Test Project
-------------------------

See https://dash.scrapinghub.com/p/2878/

    username: pycon2014
    password: pycon2014

