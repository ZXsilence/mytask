#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: liumc
@contact: liumingchao@maimiaotech.com
@date: 2014-07-21 16:32
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""
class BidWord(object):
    __slots__ = ('data',)
    def __init__(self,data):
        self.data = data


    def update(self,keyword):
        for field in dir(self):
            if field.startswith('__'):
                continue
            if not keyword.has_key(field):
                continue
            if not keyword[field]:
                continue
            index = self.__get_index_by_field(field)
            self.data[index] = keyword[field]

    def has_key(self):
        pass

    def get(self,key,value):
        index = self.__get_index_by_field(key)
        if index == None:
            return value
        else:
            return self.data[index]

    def __getitem__(self, key):
        index = self.__get_index_by_field(key)
        return self.data[index]

    def toDict(self):
        return {'word':self.data[0],
                'pv':self.data[1],
                'click':self.data[2],
                'avg_price':self.data[3],
                'compete':self.data[4],
                'score':self.data[5]
                }

    def __get_index_by_field(self,field):
        if field == 'word':
            return 0
        elif field == 'pv':
            return 1
        elif field == 'click':
            return 2
        elif field == 'avg_price':
            return 3
        elif field == 'compete':
            return 4
        elif field == 'score':
            return 5

if __name__ == '__main__':
    data  = ('test',100,230,2.5)
