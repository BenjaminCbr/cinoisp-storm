# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging

from documents.hero import Hero
from mongoengine import connect

import pymongo
import settings
import utils


class ScrapHeroesPipeline(object):
    def process_item(self, item, spider):
        return item


class HeroesToMongoPipeline(object):

    def __init__(self):
        connect(
            read_preference=pymongo.ReadPreference.SECONDARY_PREFERRED,
            **settings.MONGO_DATABASES["heroes"]
        )

    def process_item(self, item, spider):
        official_slug = item["slug_name"]

        tentative_doc = Hero.objects(official_slug=official_slug).first()
        if tentative_doc:
            logging.info("Hero with slug {} already exist in database".format(official_slug))
            if not utils.compare_dicts(tentative_doc.data.get("blibli", {}), dict(item)):
                logging.info("Items are unequal, aborting save (for now)")
        else:
            tentative_doc = Hero(official_slug=official_slug)
        tentative_doc.data["blibli"] = item
        tentative_doc.french_name = item["french_name"]
        tentative_doc.save()
