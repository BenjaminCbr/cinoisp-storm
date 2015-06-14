# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HeroesItem(scrapy.Item):

    abilities = scrapy.Field()
    description = scrapy.Field()
    franchise = scrapy.Field()
    french_name = scrapy.Field()
    skins = scrapy.Field()
    slug_name = scrapy.Field()
    subtitle = scrapy.Field()
    role = scrapy.Field()
    type_ = scrapy.Field()

class HeroTalentItem(scrapy.Item):
    talents = scrapy.Field()
    slug_name = scrapy.Field()

class PriceItem(scrapy.Item):
    slug_name = scrapy.Field()
    price = scrapy.Field()
