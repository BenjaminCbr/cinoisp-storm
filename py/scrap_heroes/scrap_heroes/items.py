# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HeroesItem(scrapy.Item):

    description = scrapy.Field()
    french_name = scrapy.Field()
    skins = scrapy.Field()
    slug_name = scrapy.Field()
    subtitle = scrapy.Field()
    role = scrapy.Field()
