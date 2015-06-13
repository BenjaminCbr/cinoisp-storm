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
