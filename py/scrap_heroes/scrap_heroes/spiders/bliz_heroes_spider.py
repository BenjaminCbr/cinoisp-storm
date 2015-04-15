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
            yield scrapy.Request("{base}{hero}/".format(
                    base=self.start_urls[0],
                    hero=hero_dict['slug'],
                ), 
                callback=self.parse_heroe
            )

    XPATH_LOCATIONS = {
        "french_name": '//div[contains(@class, "hero-info")]'
                     '//h1[contains(@class, "hero-identity__name")]/text()',
        "description": '//div[contains(@class, "hero-info")]'
                     '//div[contains(@class, "hero-description")]/text()',
        "role": '//div[@id="hero-summary"]'
                '//div[contains(@class, "hero-role") and contains(@class, "paragraph")]/text()'
    }
    
    def parse_heroe(self, response):
        # Retrieving single values
        heroes_item = HeroesItem()
        heroes_item['slug_name'] = response.url.split("/")[-2]
        for attr, xpath in self.XPATH_LOCATIONS.iteritems():
            heroes_item[attr] = response.xpath(xpath).extract()[0]
        # Retrieving skin values
        heroes_item["skins"] = self.extract_skins(response)
        heroes_item["subtitle"] = (skin["french_name"] for skin in heroes_item["skins"] if skin["main"]).next()
        yield heroes_item

    def extract_skins(self, response):
        skin_js = response.xpath('//script[contains(text(), "window.heroSkins")]/text()').extract()[0]
        skins_regex = r"(?<=window.heroSkins = ).*](?=;)"
        skin_json = json.loads(re.search(skins_regex, skin_js, re.DOTALL).group()) 
        return [
            {
                "en_name": skin["enName"],
                "french_name": skin["name"],
                "main": i == 0,
                "slug_name": skin["slug"],
            }
            for i, skin in enumerate(skin_json)
        ]
