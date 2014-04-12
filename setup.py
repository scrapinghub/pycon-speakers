# Automatically created by: scrapy deploy

from setuptools import setup, find_packages

setup(
    name='pycon2014-scraper',
    version='0.1',
    packages=find_packages(),
    entry_points={'scrapy': ['settings = pycon_speakers.settings']},
    install_requires=['Scrapy'],
)
