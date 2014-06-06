#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Chen Ke
@contact: chenke@MaimiaoTech.com
@date: 2012-09-11 20:21
@version: 0.0.0
@license: Copyright MaimiaoTech.com
@copyright: Copyright MaimiaoTech.com

"""
import os
import datetime

def hash_query_func(query):
    t_list = sorted(query)
    t_list_e = []
    for t in t_list:
        if t == " ":
            continue
        t_list_e.append(t)
    return hash(",".join(t_list_e))
