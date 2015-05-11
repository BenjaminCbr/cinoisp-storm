"""
This module contain utils class liable to be used by any spider
"""
from __future__ import unicode_literals
import logging
import re


def compare_dicts(dict_a, dict_b):
    """
    Compare dicts and produce the list of keys that are not similar
    as
    """
    if dict_a != dict_b:
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
        if dict_a[key] != dict_b[key]:
            logging.info("For Key {}, elements are unequal => {} vs {}".format(
                key, dict_a[key], dict_b[key]
            ))
            comparison = False

    return comparison

def clean_name(input_string):
    return re.sub(r"\W", "", input_string).lower()
