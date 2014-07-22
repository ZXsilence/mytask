#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: liumc
@contact: liumingchao@maimiaotech.com
@date: 2014-07-21 17:09
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""
class DeleteWord(object):
    
    def __init__(self,data):
        self.data = data

    def __get_index_by_field(self,field):
        if field == 'keyword_id':
            return 0
        elif field == 'code':
            return 1
        elif field == 'priority':
            return 2

    def __getitem__(self,field):
        index = self.__get_index_by_field(field)
        return self.data[index]



