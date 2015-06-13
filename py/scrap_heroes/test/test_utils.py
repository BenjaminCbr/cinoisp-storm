from __future__ import unicode_literals

from django.test import TestCase

from scrap_heroes.utils import partial_dict_equals


class DictUtilsTest(TestCase):

    def test_partial_dict_equals__regular_case(self):
        small_dict = {
            "a": 1,
            "b": [2, 3, 6],
            "d": False
        }
        big_dict = {
            "aa": 123,
            "fdsg": 2,
            "a": 1,
            "b": [2, 6, 3],
        }
        self.assertTrue(partial_dict_equals(small_dict, big_dict))

    def test_partial_dict_equals__irregular_case(self):
        small_dict = {
            "a": 1,
            "b": [2, 6],
            "d": False
        }
        big_dict = {
            "aa": 123,
            "fdsg": 2,
            "a": 1,
            "b": [2, 6, 3],
        }
        self.assertFalse(partial_dict_equals(small_dict, big_dict))
