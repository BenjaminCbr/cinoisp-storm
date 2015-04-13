from __future__ import unicode_literals

import json
import re
import scrapy

from scrap_heroes.items import HeroesItem


class BlizHeroesSpider(scrapy.Spider):

    name = "bliz_heroes"
    start_urls = [
        "http://eu.battle.net/heroes/fr/heroes/"
    ]

    def parse(self, response):
        heroes_js = response.xpath('//script[contains(text(), "window.heroes")]/text()').extract()[0]
        heroes_regex = r"(?<=window.heroes = ).*(?=;)"
        heroes_json = json.loads(re.search(heroes_regex, heroes_js).group())
        
        for hero_dict in heroes_json:
            self.log('Found Hero {name}, slug is {slug}'.format(
                name=hero_dict['name'],
                slug=hero_dict['slug']
            ))
