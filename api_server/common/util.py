#encoding=utf8
"""doc string for module"""
__author__ = 'lym liyangmin@maimiaotech.com'

import sys
import os
import logging

logger = logging.getLogger(__name__)

def change_obj_to_dict_deeply(obj):
    result_dict = {}
    if type(obj) == type([]):
        #列表转换
        return [change_obj_to_dict_deeply(sub_obj) for sub_obj in obj]
    elif isinstance(obj,object) and obj.__class__.__module__.startswith('Domain'):
        result_dict = obj.toDict()
    elif type(obj) == type({}):
        result_dict = obj
    else:
        #基本类型，无需转换
        return obj
    keys = result_dict.keys()
    for key in keys:
        #迭代转换
        if isinstance(result_dict[key],object) and result_dict[key].__class__.__module__.startswith('Domain'):
            result_dict[key] = change_obj_to_dict_deeply(result_dict[key])
        elif type(result_dict[key]) == type([]):
            result_dict[key] = [change_obj_to_dict_deeply(obj) for obj in result_dict[key]]
    return result_dict


def slice_list(source_list, step):
    """将列表按长度step分段"""
    for i in xrange(0, len(source_list), step):
        yield source_list[i:i+step]


def reduce_list_by_step(source_list, step):
    """
    reduce list of list by step, 每个子元素不能被拆分，新生成的列表每个子元素的长度不能超过step
    source_list: [[1,2,3], [4], [5,6,7], [8,9,10]]
    step: 5
    return [[1,2,3,4], [5,6,7], [8,9,10]]
    """
    new_list = []
    for item in source_list:
        assert len(item) <= step
        if new_list and len(new_list[-1] + item) <= step:
            new_list[-1] += item
        else:
            new_list.append(item)
    return new_list
