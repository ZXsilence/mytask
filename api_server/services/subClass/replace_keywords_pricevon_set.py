#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: tanglingling
@contact: tanglingling@maimiaotech.com
@date: 2017-08-08 15:18
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""
import os,sys,simplejson,copy
import logging
logger2 = logging.getLogger("api_virtual")
from datetime import datetime 
KeywordDBService = None
ShopInfo = None

class ReplaceKeywordsPricevonSet(object):
    '''
    设置关键词出价，返回值替换
    set 接口，1先改db 2再改api返回值
    '''
    def __init__(self,api_name,nick,fkey,ivalue):
        self.api_name = api_name
        self.nick = nick
        self.fkey = fkey
        self.ivalue = simplejson.loads(ivalue)#入参结构ivalue是list必须json转换

    def _get_corresponding_key(self,ikey):
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

    def replace_ret_values(self):
        global KeywordDBService
        if not KeywordDBService:from keyword_db.services.keyword_db_service_new import KeywordDBService
        global ShopInfo
        if not ShopInfo:from shop_db.db_models.shop_info import ShopInfo

        #根据推广组id从虚拟库找出关键词列表
        sid = ShopInfo.get_sid_by_nick(self.nick)
        keywords_list = KeywordDBService.get_keywords(sid)

        #入参和实际关键词求交集，确定最终可以替换的关键词
        i_keyword_ids = [k['keywordId'] for k in self.ivalue]
        o_keyword_ids = [k['keyword_id'] for k in keywords_list]
        keyword_ids = list(set(i_keyword_ids).intersection(set(o_keyword_ids)))

        #返回结构长度不够的进行返回长度扩展
        ilen = (len(keyword_ids)- len(self.fkey))
        if isinstance(self.fkey,list):
            if ilen > 0 :
                items = [copy.deepcopy(self.fkey[0]) for i in range(ilen)]
                self.fkey.extend(items)
            elif ilen < 0 :
                self.fkey = self.fkey[:len(self.fkey) + ilen]
        else:
            logger2.error("错误：返回值替换失败！%s " % self.api_name)
            return None

        i_keyword_dict = {}
        for iv in self.ivalue: i_keyword_dict[iv['keywordId']] = iv
        o_keyword_dict = {}
        for ov in keywords_list: o_keyword_dict[ov['keyword_id']] = ov.toDict()

        #api返回值替换
        ikeys = self.ivalue[0].keys()
        okeys = keywords_list[0].toDict().keys()
        to_save_db_keyword_list = []
        for i in range( len(keyword_ids) ):

            keyword_id = keyword_ids[i]
            ikeyword = i_keyword_dict[keyword_id]
            okeyword = o_keyword_dict[keyword_id]

            for  k in okeys: #非修改值替换，如campaign_id、adgroup_id、create_time等值
                if hasattr(self.fkey[i],k):
                    v = okeyword[k]
                    setattr(self.fkey[i],k, v)

            for ik in ikeys:
                iv = i_keyword_dict[keyword_id][ik] #获取设置值
                ok = self._get_corresponding_key(ik)#获取返回结构对应键
                if hasattr(self.fkey[i],ok):
                    setattr(self.fkey[i],ok,iv)#替换api返回键对应值
                    okeyword[ok] = iv #替换存db的关键词列表
            if hasattr(self.fkey[i],"modified_time"):
                setattr(self.fkey[i],"modified_time",datetime.now())
                okeyword['modified_time'] = datetime.now()
            to_save_db_keyword_list.append(okeyword)

        #替换值后存虚拟库
        KeywordDBService.update_keyword_list(sid,to_save_db_keyword_list)
        logger2.info("存虚拟库成功！api_name:%s " % self.api_name)

        return self.fkey
