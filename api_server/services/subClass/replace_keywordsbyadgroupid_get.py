#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: tanglingling
@contact: tanglingling@maimiaotech.com
@date: 2017-08-08 11:28
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""
import os,sys,copy
import logging
logger2 = logging.getLogger("api_virtual")
from replace_base import ReplaceBase

KeywordDBService = None
ShopInfo = None

class ReplaceKeywordsByAdgroupidGet(ReplaceBase):
    '''
    根据推广组id获取关键词列表接口
    api_name:taobao.simba.keywordsbyadgroupid.get
    '''
    def replace_ret_values(self):
        global KeywordDBService
        if not KeywordDBService:from keyword_db.services.keyword_db_service_new import KeywordDBService
        global ShopInfo
        if not ShopInfo:from shop_db.db_models.shop_info import ShopInfo
        '''
        fkey：返回结构。fkey如果是对象引用可以不返回，但是如果是非对象（如整型），需要返回。为格式统一，都返回。
        返回结构[]里面元素长度不够的，需要对其扩展
        '''
        adgroup_id = self.ivalue
        sid = ShopInfo.get_sid_by_nick(self.nick)

        #根据推广组id从虚拟库找出关键词列表
        keywords_list = KeywordDBService.get_keywords_by_adgroup_id(sid,adgroup_id)

        inputLen = len(keywords_list)
        outputLen = len(self.fkey)
        if inputLen > outputLen:
            self.fkey.extend([copy.deepcopy(self.fkey[0]) for i in range(inputLen-outputLen)])
        elif inputLen < outputLen:
            self.fkey = self.fkey[:(outputLen-inputLen)]

        #根据返回结构里的键，进行返回值替换
        rkeys = self.fkey[0].toDict().keys()
        n_change_keys = []
        try:
            for i in range(len(keywords_list)):
                keyword = keywords_list[i].toDict()
                item = self.fkey[i] #不能直接item=self.fkey[i].toDict()这样直接item是另外一个对象，不能修改原对象;所以只能setattr
                for k in rkeys:
                    if keyword.get(k,None):
                        v = keyword.get(k,None)
                        setattr(item,k,v)
                    else:
                        n_change_keys.append(k)
        except Exception,e:
            logger2.exception("错误：返回值替换失败！%s,e:%s " % self.api_name, e)
            return None
        return self.fkey
