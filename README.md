PyCon Speakers Spider
=====================

This project will:

1.  scrape speakers' names from archived conference websites,
2.  use [SexMachine](https://pypi.python.org/pypi/SexMachine/) to infer gender, and
3.  plot gender ratios for different conferences over time.

The Scrapy team have built a spider that scrapes information about speakers at Python conferences since 2011;
please see the [Scrapy installation guide](http://doc.scrapy.org/en/latest/intro/install.html) for installation instructions.

To get started with the sprint:

1.  Pick a currently-active conference website that *isn't* PyCon:
    Strange Loop, OSCON, an academic conference like ICSE, or anything else.

2.  Create a sub-directory named something like pycon-2014 or icse-2013 (i.e., conference dash year).
    We'll worry about scrapers that work for multiple years of a conference later.

3.  Create a program called `scraper.py`
    that can be run without any command-line arguments to get speakers' names for just that site.
    You can use the code that is already in this repository,
    or start from scratch:
    we'll figure out how to refactor things after we have half a dozen.

4.  The output of the scraper should look something like this:

        Event Name,Year,URL
        Personal Name 1,Family Name 1,Num Appearances,Gender
        Personal Name 2,Family Name 2,Num Appearances,Gender
        ...,...,...

    The first row is metadata; each row after that is information about a single speaker.
    The personal names are what we (probably) use to infer gender,
    the family name is there for completeness,
    "Num Appearances" is how many times they appeared to be a speaker
    (some people give multiple talks at a single conference),
    and the gender is M, F, or U (unknown).

5.  Send a pull request.

Running the Scrapy Code
-----------------------

List available spiders:

    scrapy list

Run a spider:

    scrapy crawl us.pycon.org

Scrapy Cloud Test Project
-------------------------

See https://dash.scrapinghub.com/p/2878/

    username: pycon2014
    password: pycon2014

