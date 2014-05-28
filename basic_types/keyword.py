#encoding=utf8
__author__ = 'chenke'

import datetime

class Keyword(object):
    __slots__ = ['data']

    def __init__(self, kwd_data):
        self.data = kwd_data

    def update(self,keyword):
        for field in dir(self):
            if field.startswith('__'):
                continue
            if not keyword[field]:
                continue
            index = self.__get_index_by_field(field)
            self.data[index] = keyword[field]

    def has_key(self):
        pass

    def get(self,key,value):
        index = self.__get_index_by_field(key)
        if not self.data[index]:
            return value
        else:
            return self.data[index]

    def __getitem__(self, key):
        index = self.__get_index_by_field(key)
        return self.data[index]

    #def __setitem__(self, key,val):
    #    index = self.__get_index_by_field(key)
    #    self.data[index] = val

    def __get_index_by_field(self,key):
        if key == "keyword_id":
            return 0
        if key == "adgroup_id":
            return 1
        if key == "campaign_id":
            return 2
        if key == "sid":
            return 3
        if key == "nick":
            return 4
        if key == "word":
            return 5
        if key == "audit_status":
            return 6
        if key == "qscore":
            return 7
        if key == "match_scope":
            return 8
        if key == "max_price":
            return 9 
        if key == "is_default_price":
            return 10
        if key == "is_garbage":
            return 11
        if key == "create_time":
            return 12
        if key == "modified_time":
            return 13

if __name__== '__main__':
    keyword = Keyword((53508752000, 303723495, 13313745, 66463677, u'\u4e9a\u4f50\u670d\u9970\u4e13\u8425\u5e97', u'\u5e03 \u88e4', 'audit_pass', 5, '4', 70, False, False, datetime.datetime(2014, 2, 9, 16, 54, 57), datetime.datetime(2014, 5, 5, 5, 6, 47)))
    print keyword['word']
    print keyword['audit_status']

