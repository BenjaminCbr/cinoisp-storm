from __future__ import unicode_literals

import logging
import scrapy

from documents.hero import Hero
from scrap_heroes.items import HeroTalentItem

from scrap_heroes import settings


class TalentHeroesSpider(scrapy.Spider):

    name = "talent_heroes"

    BASE_URL = settings.TALENT["BASE_URL"]
    start_urls = settings.TALENT["START_URLS"]


    def parse(self, response):
        hero_list = response.xpath('//div[@id="liste_heros_wrapper"]//div[contains(@class, "hero ")]')
        for hero_container in hero_list:
            hero_name = hero_container.xpath('.//span[@class="nom"]/text()').extract()[0]
            hero_href = hero_container.xpath('./a/@href').extract()[0]
            hero_url = self.BASE_URL + hero_href
            self.log("Found Hero {}".format(hero_name))
            mongo_hero = Hero.find_hero_from_french_name(hero_name)
            if mongo_hero:
                self.log("Found Hero in mongo {}".format(mongo_hero.official_slug))
            else:
                logging.warning("No HERO FOUND")
                continue
            meta = {
                "mongo_hero": mongo_hero,
            }
            yield scrapy.Request(hero_url, callback=self.parse_hero, meta=meta)
            break

    def parse_hero(self, response):
        pass
