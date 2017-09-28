#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: tanglingling
@contact: tanglingling@maimiaotech.com
@date: 2017-08-11 10:45
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""

def get_corresponding_key(ikey):
    '''
    将是大写字母变成下划线+小写字母形式。
    如：mobileIsDefaultPrice -> mobile_is_default_price
    '''
    rkey = ""
    for c in ikey:
        if c.isupper():
            c = "_"+c.lower()
        rkey += c
    return rkey


