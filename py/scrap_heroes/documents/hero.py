from __future__ import unicode_literals

import logging

from fuzzywuzzy import fuzz

import mongoengine
import scrapy

from utils import clean_name


class Hero(mongoengine.Document):
    """
    Class storing all information about heroes
    """

    meta = {
        "db_alias": "heroes",
    }

    data = mongoengine.DictField()
    french_name = mongoengine.StringField()
    official_slug = mongoengine.StringField()  # Contains the official name of the Hero

    MIN_FUZZY_RATIO = 75

    _hero_french_name_id_dict = None

    @classmethod
    def retrieve_hero_french_name_id_dict(cls):
        if not cls._hero_french_name_id_dict:
            cls._hero_french_name_id_dict = {
                t[0] : t[1]
                for t in cls.objects().scalar("french_name", "id")
            }
        return cls._hero_french_name_id_dict

    @classmethod
    def find_hero_from_french_name(cls, french_name):
        hero_doc = cls.objects(french_name__iexact=french_name).first()
        if not hero_doc:  # If we haven't found the right hero
            cleaned_french_name = clean_name(french_name)
            scrapy.log.msg("Haven't found any matching hero directly for {}. "
                           "Going for fuzzy methods".format(french_name),
                         level=scrapy.log.WARNING)
            name_id_dict = cls.retrieve_hero_french_name_id_dict()
            hero_original_slug = max(
                name_id_dict.keys(),
                key=lambda x: fuzz.partial_ratio(cleaned_french_name, clean_name(x))
            )
            score = fuzz.partial_ratio(cleaned_french_name, clean_name(hero_original_slug))
            if score <= cls.MIN_FUZZY_RATIO:
                logging.warning("Score was {}, discarding as too low. Hero might be missing from"
                                " blibli site".format(score))
                return None
            hero_doc = cls.objects(id=name_id_dict[hero_original_slug]).get()
            scrapy.log.msg(
                "Found matching hero {} for {}, with score {}"
                    .format(hero_doc.french_name, french_name, score),
                level=scrapy.log.INFO
            )
        return hero_doc
