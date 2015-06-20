"""
This module contain utils class liable to be used by any spider
"""
from __future__ import unicode_literals

from datetime import datetime

import logging
import os
import re


def compare_dicts(dict_a, dict_b):
    """
    Compare dicts and produce the list of keys that are not similar
    as
    """
    if set(dict_a.keys()) != set(dict_b.keys()):
        logging.info("Keys in a, not in b {}.\nKeys in b, not in a".format(
            set(dict_a.keys()) - set(dict_b.keys()),
            set(dict_b.keys()) - set(dict_a.keys()),
        ))
        return False

    comparison = True
    for key in dict_a.iterkeys():
        if isinstance(dict_a[key], dict):
            current_comparison = compare_dicts(dict_a[key], dict_b[key])
            if not current_comparison:
                logging.info("For Key {}, Sub-dicts were found unequal".format(key))
                comparison &= current_comparison
        elif isinstance(dict_a[key], list):
            comparison &= (sorted(dict_a[key]) == sorted(dict_b[key]))
        elif dict_a[key] != dict_b[key]:
            logging.info("For Key {}, elements are unequal => {} vs {}".format(
                key, dict_a[key], dict_b[key]
            ))
            comparison = False

    return comparison

def partial_dict_equals(small_dict, big_dict):
    """
    Tests that all the keys that small dict and bigger dict have in common
    are equal, if they exist in the bigger dict.
    """
    big_dict_adapted =  {
        key: value for key, value in big_dict.iteritems() if key in small_dict
    }
    small_dict_adapted = {
        key: value for key, value in small_dict.iteritems() if key in big_dict_adapted
    }
    return compare_dicts(big_dict_adapted, small_dict_adapted)

def clean_name(input_string):
    return re.sub(r"\W", "", input_string).lower()

# Helper part to download pictures


class FileDownloader(object):

    def __init__(self, name):
        self._path_to_static = os.path.join(
            "..", "..", "temp", name, datetime.now().strftime("%B_%d__%H_%M")
        )
        self._initialize_static_folder_if_needed()

    def _initialize_static_folder_if_needed(self):
        if not os.path.exists(self._path_to_static):
            os.makedirs(self._path_to_static)

    def download_talent_picture(self, response):
        with open(os.path.join(self._path_to_static, response.url.split("/")[-1]), "wb") as f:
            f.write(response.body)
