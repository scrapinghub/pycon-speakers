PyCon Speakers Spider
=====================

This project will:

1.  scrape speakers' names from archived conference websites,
2.  use [SexMachine](https://pypi.python.org/pypi/SexMachine/) to infer gender, and
3.  plot gender ratios for different conferences over time.

The Scrapy team have built a spider that scrapes information about speakers at Python conferences since 2011;
please see the [Scrapy installation guide](http://doc.scrapy.org/en/latest/intro/install.html) for installation instructions.

To get started with the sprint:

1.  Pick a currently-active conference that hasn't yet been scraped and write a Scrapy Spider for that conference. You can see conferences that have been scraped already by typing `scrapy list`.

2.  Create a Scrapy Spider for the conference you wish to scrape, in the pycon_speakers/spiders/ directory. It should crawl as many years of the conference as possible and extract Speaker items.

3.  Test your spider

4. Submit a pull request

Other tasks:

1.  Improve the gender identification in pycon_speakers/pipelines.py
2.  Review crawled data and fix spiders when the data is incorrect
3.  Chart results

Here what we have for now:
![Gender Bar Chart](/gender_plot.png)

Running the Scrapy Code
-----------------------

List available spiders:

    scrapy list

Run a spider:

    scrapy crawl us.pycon.org

Run all spiders and generate a data.csv file:

    run.sh

Scrapy Cloud Test Project
-------------------------

See https://dash.scrapinghub.com/p/2878/

    username: pycon2014
    password: pycon2014

