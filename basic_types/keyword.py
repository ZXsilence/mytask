#encoding=utf8
__author__ = 'chenke'

import datetime

class Keyword(object):
    __slots__ = ['data']
    fields = [
         "keyword_id",
        "adgroup_id",
        "campaign_id",
        "sid",
        "nick",
        "word",
        "audit_status",
        "qscore",
        "rele_score",
        "cvr_score",
        "cust_score",
        "creative_score",
        "match_scope",
        "max_price",
        "max_mobile_price",
        "is_default_price",
        "mobile_is_default_price",
        "is_garbage",
        "create_time"
        "modified_time"
    ]

    def __init__(self, kwd_data):
        self.data = kwd_data

    def update(self,keyword):
        data_list = list(self.data)
        for  field  in  self.fields:
            if field.startswith('__'):
                continue
            if not keyword.has_key(field):
                continue
            if not keyword[field]:
                continue
            index = self.__get_index_by_field(field)
            data_list[index] = keyword[field] 
        self.data = tuple(data_list) 

    def has_key(self,key):
        if  key in self.fields:
            return True
        return False

    def get(self,key,value):
        index = self.__get_index_by_field(key)
        if index == None:
            return value
        else:
            return self.data[index]

    def __getitem__(self, key):
        index = self.__get_index_by_field(key)
        return self.data[index]

    #def __setitem__(self, key,val):
    #    index = self.__get_index_by_field(key)
    #    self.data[index] = val
    
    def toDict(self):
        return {
                'keyword_id':self.data[0],
                'adgroup_id':self.data[1],
                'campaign_id':self.data[2],
                'sid':self.data[3],
                'nick':self.data[4],
                'word':self.data[5],
                'audit_pass':self.data[6],
                'qscore':self.data[7],
                'rele_score':self.data[8],
                'cvr_score':self.data[9],
                'cust_score':self.data[10],
                'creative_score':self.data[11],
                'match_scope':self.data[12],
                'max_price':self.data[13],
                'max_mobile_price':self.data[14],
                'is_default_price':self.data[15],
                'mobile_is_default_price':self.data[16],
                'is_garbage':self.data[17],
                'create_time':self.data[18],
                'modified_time':self.data[19]
                }

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
        if key =="rele_score":
            return 8
        if key =="cvr_score":
            return 9 
        if key =="cust_score":
            return 10
        if key =="creative_score":
            return 11
        if key == "match_scope":
            return 12
        if key == "max_price":
            return 13
        if key == "max_mobile_price":
            return 14
        if key == "is_default_price":
            return 15
        if key == "mobile_is_default_price":
            return 16
        if key == "is_garbage":
            return 17
        if key == "create_time":
            return 18
        if key == "modified_time":
            return 19

if __name__== '__main__':
    keyword = Keyword((53508752000, 303723495, 13313745, 66463677, u'\u4e9a\u4f50\u670d\u9970\u4e13\u8425\u5e97', u'\u5e03 \u88e4', 'audit_pass', 5, '4', 70, False, False, datetime.datetime(2014, 2, 9, 16, 54, 57), datetime.datetime(2014, 5, 5, 5, 6, 47)))
    print  keyword.has_key("keyword_id")

