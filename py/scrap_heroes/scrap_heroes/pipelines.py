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
        """
        An item must have an associeted slug_name
        """
        official_slug = item["slug_name"]

        tentative_doc = Hero.objects(official_slug=official_slug).first()
        if tentative_doc:
            logging.info("Hero with slug {} already exist in database".format(official_slug))
            if not utils.partial_dict_equals(dict(item), tentative_doc.data):
                logging.info(
                    "Items has key in tentative_doc.data, that are different from mongo object."
                    "aborting save (for now)"
                )
            data_to_save = {
                key: value for key, value in item.iteritems() if key not in tentative_doc.data
            }
        else:
            tentative_doc = Hero(official_slug=official_slug)
            data_to_save = dict(item)
        tentative_doc.data = data_to_save

        if spider.name == "bliz_heroes":  # Adding French Name if we come from BliBli
            tentative_doc.french_name = item["french_name"]

        tentative_doc.save()
        return item
