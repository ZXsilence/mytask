#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: liumc
@contact: liumingchao@maimiaotech.com
@date: 2014-07-01 11:39
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""
import datetime
class DataList(object):
    def __init__(self,data,id_name):
        self.data = data
        self.id_name = id_name
        self.id_list = [item[self.id_name]for item in data]
        self.num = len(self.data)
    
    def __getitem__(self,id):
        index = self.id_list.index(id)
        return self.data[index]

if __name__ == '__main__':
    data = [{'relevance_mode': 0L, 'cpc_max': 53L, 'extra_infos': [], 'campaign_id': 3328400L, 'adgroup_id': 414820184L, 'last_handle_time': datetime.datetime(2014, 6, 16, 19, 19), 'handle_status': 1L, 'num_iid': 7794896442L, 'nick': u'chinchinstyle', 'filter_words': [], 'sid': 62847885L, 'non_settings': {u'11': 0, 'handle_status': True, 'relevance_mode': False, 'cpc_max': True, 'extra_infos': False, 'num_iid': True, 'campaign_id': True, 'nick': True, 'filter_words': False, 'sid': True, 'non_settings': True, 'adgroup_id': True, 'last_handle_time': True}}, {'relevance_mode': 0L, 'cpc_max': 55L, 'extra_infos': [], 'campaign_id': 3328400L, 'adgroup_id': 414826425L, 'last_handle_time': datetime.datetime(2014, 6, 16, 19, 19, 35), 'handle_status': 1L, 'num_iid': 15493508084L, 'nick': u'chinchinstyle', 'filter_words': [], 'sid': 62847885L, 'non_settings': {u'11': 0, u'handle_status': True, u'relevance_mode': False, u'cpc_max': True, u'21': 1, u'extra_infos': False, u'0': 1, u'num_iid': True, u'campaign_id': True, u'nick': True, u'filter_words': False, u'sid': True, u'non_settings': True, u'adgroup_id': True, u'last_handle_time': True}}]
    id_name = 'adgroup_id'
    obj = DataList(data,id_name)
    print obj[414826425L]

