#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: tanglingling
@contact: tanglingling@maimiaotech.com
@date: 2017-08-15 11:41
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""
import logging
logger2 = logging.getLogger("api_virtual")
import simplejson
import hashlib
import time
import copy
from datetime import datetime
from exceptions import ApiVirtualResponseException
from common import get_corresponding_key

KeywordDBService = None
ShopInfo = None

class ReplaceKeywordsbykeywordidsGet(object):
    '''
    根据关键词id获取关键词列表
    '''
    def __init__(self,api_name,nick,fkey,ivalue,campaign_id=None,adgroup_id=None):
        self.api_name = api_name
        self.nick = nick
        self.fkey = fkey
        self.ivalue = ivalue
        self.campaign_id = campaign_id
        self.adgroup_id = adgroup_id

    def replace_ret_values(self):
        global KeywordDBService
        if not KeywordDBService:from keyword_db.services.keyword_db_service_new import KeywordDBService
        global ShopInfo
        if not ShopInfo:from shop_db.db_models.shop_info import ShopInfo

        sid = ShopInfo.get_sid_by_nick(self.nick)
        #异常校验
        if not self.ivalue:
            logger2.error("入参参数异常！nick:%s , api_name:%s " % (self.nick, self.api_name))
            ApiVirtualResponseException("入参参数异常！nick:%s , api_name:%s " % (self.nick, self.api_name))

        r_keyword_ids = []
        if isinstance(self.ivalue,int): 
            r_keyword_ids = [self.ivalue]
        elif type(self.ivalue) in [str,unicode]:
            r_keyword_ids =[ int(k) for k in  self.ivalue.split(",")]
        else:
            logger2.error("输入参数个数有误，请校验keyword_ids:%s " % self.ivalue)
            ApiVirtualResponseException("输入参数个数有误，请校验keyword_ids:%s " % self.ivalue)

        r_keyword_lists = KeywordDBService.get_keywords_by_keyword_ids(sid,r_keyword_ids,has_none=False)
        r_keyword_lists = [ k.toDict() for k in r_keyword_lists ]

        if [] == r_keyword_lists:
            self.fkey = []
            return self.fkey

        #返回值替换
        klen = len(r_keyword_lists)
        olen = len(self.fkey)
        if klen > olen:
            self.fkey.extend([ copy.deepcopy(self.fkey[0]) for i in range(klen-olen)])
        elif klen < olen:
            self.fkey = self.fkey[:(olen-klen)]

        keys = r_keyword_lists[0].keys()
        for i in range(klen):
            for k in keys:
                setattr(self.fkey[i],k,r_keyword_lists[i][k])
        logger2.info("返回值替换成功！nick:%s,api_name:%s" % (self.nick,self.api_name))

        return self.fkey
