from __future__ import unicode_literals

from datetime import datetime
from django.test import TestCase
from mongoengine import connect

import pymongo

from ..documents.hero import ArchivedHero, Hero

from ..scrap_heroes import settings


class HeroTest(TestCase):
    """
    Tests related to Archived Heroes
    """

    TEST_SLUG = "test_slug"

    @classmethod
    def setUpClass(cls):
        connect(
            read_preference=pymongo.ReadPreference.SECONDARY_PREFERRED,
            **settings.MONGO_DATABASES["heroes"]
        )

    def tearDown(self):
        ArchivedHero.objects(official_slug=self.TEST_SLUG).delete()
        Hero.objects(official_slug=self.TEST_SLUG).delete()

    def assertDatesAreClose(self, date_1, date_2):
        time_delta = date_1 - date_2 if date_1 > date_2 else date_2 - date_1
        self.assertAlmostEqual(0, time_delta.total_seconds(), delta=1)

    def test_archive_hero(self):
        hero = Hero(official_slug=self.TEST_SLUG, data={"a": "yolo", "b": "ok"})
        hero.save()
        archived_hero = hero.archive_hero()
        self.assertEqual(1, ArchivedHero.objects(official_slug=self.TEST_SLUG).count())
        self.assertIsInstance(archived_hero, ArchivedHero)
        self.assertIsNotNone(archived_hero.id)
        self.assertEqual(hero.data, archived_hero.data)
        self.assertDatesAreClose(datetime.now(), archived_hero.archived_at)
