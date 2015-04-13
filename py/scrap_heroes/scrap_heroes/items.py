# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HeroesItem(scrapy.Item):
    core_name = scrapy.Field()
    french_name = scrapy.Field()
