#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set ts=4 sts=4 sw=4 et:
"""
@author: Wu Liang
@authors:
@date: 8:31:46 PM Jun 6, 2012
@contact: wuliang@maimiaotech.com
@version: 0.0.0
@deprecated:
@license:
@copyright:
"""

import xmltodict

def change_xml_to_dict_deeply(obj):
    result_dict = {}
    if type(obj) == type([]):
        #列表转换
        return [change_xml_to_dict_deeply(sub_obj) for sub_obj in obj]
    elif isinstance(obj,xmltodict.OrderedDict):
        result_dict = dict(obj) 
    elif type(obj) == type({}):
        result_dict = obj
    else:
        #基本类型，无需转换
        return obj
    keys = obj.keys()
    for key in keys:
        #迭代转换
        if isinstance(result_dict[key],object) and isinstance(result_dict[key],xmltodict.OrderedDict):
            result_dict[key] = change_xml_to_dict_deeply(result_dict[key])
        elif type(result_dict[key]) == type([]):
            result_dict[key] = [change_xml_to_dict_deeply(obj) for obj in result_dict[key]]
    return result_dict

