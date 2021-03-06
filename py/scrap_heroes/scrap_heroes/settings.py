# -*- coding: utf-8 -*-

# Scrapy settings for scrap_heroes project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

from local_settings import *

BOT_NAME = 'scrap_heroes'

SPIDER_MODULES = ['scrap_heroes.spiders']
NEWSPIDER_MODULE = 'scrap_heroes.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'scrap_heroes (+http://www.yourdomain.com)'

ITEM_PIPELINES = {
    'scrap_heroes.pipelines.HeroesToMongoPipeline': 100
}

# Be nice with crawled websites, and throttling our requests
AUTOTHROTTLE_ENABLED = True
