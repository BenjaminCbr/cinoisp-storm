from __future__ import unicode_literals

import json
import re
import scrapy

from scrap_heroes.items import HeroesItem
import scrap_heroes.settings as settings


class BlizHeroesSpider(scrapy.Spider):

    name = "bliz_heroes"
    BASE_URL = settings.BLIZ["BASE_URL"]
    start_urls = settings.BLIZ["START_URLS"]

    def parse(self, response):
        heroes_js = response.xpath('//script[contains(text(), "window.heroes")]/text()').extract()[0]
        heroes_regex = r"(?<=window.heroes = ).*(?=;)"
        heroes_json = json.loads(re.search(heroes_regex, heroes_js).group())

        for hero_dict in heroes_json:
            self.log('Found Hero {name}, slug is {slug}'.format(
                name=hero_dict['name'],
                slug=hero_dict['slug']
            ))
            meta = {
                "franchise": hero_dict["franchise"],
                "type": hero_dict["type"]["slug"]
            }
            yield scrapy.Request("{base}{hero}/".format(
                    base=self.start_urls[0],
                    hero=hero_dict['slug'],
                ),
                callback=self.parse_heroe,
                meta=meta
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
        heroes_item['franchise'] = response.meta['franchise']
        heroes_item['type_'] = response.meta['type']
        for attr, xpath in self.XPATH_LOCATIONS.iteritems():
            heroes_item[attr] = response.xpath(xpath).extract()[0]
        # Retrieving skin values
        heroes_item["skins"] = self.extract_skins(response)
        heroes_item["subtitle"] = (skin["french_name"] for skin in heroes_item["skins"] if skin["main"]).next()
        # Retrieving abilities
        heroes_item["abilities"] = self.extract_abilities(response, heroes_item['slug_name'])
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

    def extract_abilities(self, response, hero_slug):
        ability_dict = {
            "regular": [],
            "heroic": [],
            "trait": [],
        }
        # 1. Heroic abilities
        heroic_xpath = response.xpath(
            '//div[contains(@class, "heroic-abilities-container")]'
            '//div[contains(@class, "ability-box__icon-wrapper")]'
        )
        for ability_xp in heroic_xpath:
            ability_dict["heroic"].append(self.single_ability_extractor(ability_xp, hero_slug))

        # 2. Regular abilities
        regular_ability_xpath = response.xpath(
            '//div[@class="abilities-summary"]//div[contains(@class, "ability-box__icon-wrapper")]'
        )
        for ability_xp in regular_ability_xpath:
            ability_dict["regular"].append(self.single_ability_extractor(ability_xp, hero_slug))

        # 3. Hero trait
        trait_ability_xpath = response.xpath(
            '//div[@class="abilities-summary"]//div[contains(@class, "trait-icon-container")]'
        )
        ability_dict["trait"] = self.single_ability_extractor(trait_ability_xpath, hero_slug)

        return ability_dict

    def single_ability_extractor(self, current_xpath, hero_slug):
        """
        :param current_xpath:       The current xpath containing an ability
                                    information
        """
        relative_picture_link = current_xpath.xpath(".//img/@src").extract()[0]
        return {
            "slug": re.search(r"(?<={}_).+(?=.jpg)".format(hero_slug), relative_picture_link).group(),
            "description": current_xpath.xpath('.//span[contains(@class, "ability-tooltip__description")]/text()').extract()[0],
            "fr_name": current_xpath.xpath('.//span[contains(@class, "ability-tooltip__title")]/text()').extract()[0],
            "picture_link": self.BASE_URL + relative_picture_link,
        }
