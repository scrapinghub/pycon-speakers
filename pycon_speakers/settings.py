# Scrapy settings for pycon_speakers project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'pycon_speakers'

SPIDER_MODULES = ['pycon_speakers.spiders']
NEWSPIDER_MODULE = 'pycon_speakers.spiders'

HTTPCACHE_ENABLED = True

# Crawl responsibly by identifying yourself (and your website) on the user-agent
ITEM_PIPELINES = {
    'pycon_speakers.pipelines.GenderPipeline': 20,
}
#USER_AGENT = 'pycon_speakers (+http://www.yourdomain.com)'
