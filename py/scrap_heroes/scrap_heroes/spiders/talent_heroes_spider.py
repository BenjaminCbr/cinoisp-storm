from __future__ import unicode_literals

from datetime import datetime

import logging
import os
import re
import scrapy

from documents.hero import Hero
from scrap_heroes.items import HeroStatsItem, HeroTalentItem, PriceItem

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

    def parse_hero(self, response):
        talent_heroes_item = HeroTalentItem()
        talent_heroes_item["talents"], talent_jpg_queries = self.get_talents(response)
        talent_heroes_item["slug_name"] = response.meta["mongo_hero"].official_slug
        for jpg_request in talent_jpg_queries:
            yield scrapy.Request(jpg_request, callback=self.download_talent_picture)
        yield talent_heroes_item
        price_item = PriceItem()
        price_item["slug_name"] = response.meta["mongo_hero"].official_slug
        price_item["price"] = self.parse_price(response)
        yield price_item
        stat_item = self.parse_stats(response)
        stat_item["slug_name"] = response.meta["mongo_hero"].official_slug
        yield stat_item


    # Talent part

    def get_talents(self, response):
        talents = []
        talent_tree = response.xpath('//div[@class="abre_talents_wrapper"]')
        jpg_request_set = set()
        for talent_level in talent_tree.xpath('.//div[@class="niveau_wrapper"]'):
            level_dict = self.parse_talent_level(talent_level)
            jpg_request_set |= level_dict.pop("jpg_request_set")
            talents.append(level_dict)
        return talents, jpg_request_set

    def parse_talent_level(self, talent_level):
        level_number = talent_level.xpath('.//div[@class="niveau"]/span/text()').extract()[0]
        talent_list = []
        jpg_request_set = set()
        for talent in talent_level.xpath('./div[@class="talent"]'):
            talent_dict = self.parse_single_talent(talent)
            talent_request = talent_dict.pop("jpg_request")
            talent_list.append(talent_dict)
            jpg_request_set.add(talent_request)

        return {
            "level": level_number,
            "talent_list": talent_list,
            "jpg_request_set": jpg_request_set,
        }

    def parse_single_talent(self, talent):
        bound_ability = talent.xpath('./input[@class="touche"]/@value').extract()[0]
        talent_url = talent.xpath('./input[@class="image"]/@value').extract()[0]
        return {
            "french_name": talent.xpath('./input[@class="nom_vf"]/@value').extract()[0],
            "description": talent.xpath('./input[@class="description"]/@value').extract()[0],
            "cooldown": talent.xpath('./input[@class="cooldown"]/@value').extract()[0],
            "bound_ability": bound_ability if bound_ability != "0" else None,
            "talent_href": talent_url.split("/")[-1],
            "jpg_request": self.BASE_URL + talent_url,
        }

    _path_to_static = None

    def _initialize_static_folder_if_needed(self):
        if self._path_to_static:
            return

        self._path_to_static = os.path.join(
            "../..", "temp", "talent_crawl", datetime.now().strftime("%B_%d__%H_%M")
        )
        os.makedirs(self._path_to_static)

    def download_talent_picture(self, response):
        self._initialize_static_folder_if_needed()
        with open(os.path.join(self._path_to_static, response.url.split("/")[-1]), "wb") as f:
            f.write(response.body)

    # END talent part

    def parse_price(self, response):
        return {
            "gold": int(response.xpath(
                '//div[@id="informations-heros"]//span[@class="icone or"]/text()'
            ).extract()[0].replace(" ", "")),
            "euros":  float(response.xpath(
                '//div[@id="informations-heros"]//strong[text()="Prix"]/../span[contains(text(), "\u20ac")]/text()'
            ).extract()[0].replace("\u20ac", "")),
        }

    def parse_stats(self, response):
        stat_item = HeroStatsItem()
        left_stats_panel = '//h4[text()="Statistiques"]/following-sibling::div/div/text()'
        right_stats_panel = '//h4[text()="Statistiques"]/following-sibling::div/div[2]/text()'
        stat_item["level_1"] = {
            "health": int(re.search(
                r"\d+", response.xpath(left_stats_panel).extract()[1]
            ).group()),
            "regen_health": float(re.search(
                r"[\d\.]+", response.xpath(left_stats_panel).extract()[3]
            ).group()),
            "mana": int(re.search(
                r"\d+", response.xpath(left_stats_panel).extract()[5]
            ).group()),
            "regen_mana": float(re.search(
                r"[\d\.]+", response.xpath(left_stats_panel).extract()[7]
            ).group()),
            "damage": int(re.search(
                r"[\d\.]+", response.xpath(right_stats_panel).extract()[1]
            ).group()),
            "attack_speed": float(re.search(
                r"[\d\.]+", response.xpath(right_stats_panel).extract()[3]
            ).group()),
            "attack_range": float(re.search(
                r"[\d\.]+", response.xpath(right_stats_panel).extract()[5]
            ).group()),
        }

        left_stats_panel_per_level = ('//h4[text()="Statistiques"]/following-sibling::'
                                      'div/div/span[@class="par_niveau"]/text()')
        right_stats_panel_per_level = ('//h4[text()="Statistiques"]/following-sibling::'
                                      'div/div[2]/span[@class="par_niveau"]/text()')
        stat_item["per_level"] = {
            "health": int(re.search(
                r"\d+", response.xpath(left_stats_panel_per_level
            ).extract()[0]).group()),
            "regen_health": float(re.search(
                r"[\d\.]+", response.xpath(left_stats_panel_per_level
            ).extract()[1]).group()),
            "mana": int(re.search(
                r"\d+", response.xpath(left_stats_panel_per_level
            ).extract()[2]).group()),
            "regen_mana": float(re.search(
                r"[\d\.]+", response.xpath(left_stats_panel_per_level
            ).extract()[3]).group()),
            "damage": float(re.search(
                r"[\d\.]+", response.xpath(right_stats_panel_per_level
            ).extract()[0]).group()),
        }
        return stat_item
