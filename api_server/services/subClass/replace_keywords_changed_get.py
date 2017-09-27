#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: tanglingling
@contact: tanglingling@maimiaotech.com
@date: 2017-08-16 17:39
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""
import logging
logger2 = logging.getLogger("api_virtual")
import time
import copy
from datetime import datetime
from exceptions import ApiVirtualResponseException
from replace_base import ReplaceBase

KeywordChangedTestService = None
ShopInfo = None

class ReplaceKeywordsChangedGet(ReplaceBase):
    '''
    模拟：分页获取修改过的关键词ID、宝贝id、修改时间
    '''
    def replace_ret_values(self):
        global KeywordChangedTestService
        if not KeywordChangedTestService: from keyword_db.services.keywords_changed_test_service import KeywordChangedTestService
        global ShopInfo
        if not ShopInfo:from shop_db.db_models.shop_info import ShopInfo

        #参数获取
        start_time = self.ivalue["ivalue"]
        page_no = int(self.ivalue["page_no"])
        page_size = int(self.ivalue["page_size"])

        #try:
        #    start_time = datetime.strptime(start_time,"%Y-%m-%d %H:%M:%S")
        #except Exception,e:
        #    logger2.error("输入参数个数有误！请检查start_time参数：%s,nick:%s , api_name:%s " % (start_time,self.nick,self.api_name))
        #    ApiVirtualResponseException("输入参数个数有误！请检查start_time参数：%s,nick:%s , api_name:%s " % (start_time,self.nick,self.api_name))

        sid = ShopInfo.get_sid_by_nick(self.nick)
        keyword_changed_list = KeywordChangedTestService.get_keywords_changed(sid,start_time,page_no,page_size)

        #返回值结构扩展
        olen = len(keyword_changed_list)

        setattr(self.fkey,"total_item",olen)
        setattr(self.fkey,"page_no",page_no)
        setattr(self.fkey,"page_size",page_size)
        sub_fkey = self.fkey.keyword_list

        flen = len(sub_fkey)
        if olen > flen:
            sub_fkey.extend([copy.deepcopy(sub_fkey[0]) for i in range(olen-flen)])
        elif olen < flen:
            sub_fkey = sub_fkey[:olen]
        if [] == sub_fkey:
            setattr(self.fkey,"keyword_list",sub_fkey)
            return self.fkey

        #返回值替换
        fKeys = sub_fkey[0].toDict().keys()
        for i in range(olen):
            for ky in fKeys:
                setattr(sub_fkey[i],ky,keyword_changed_list[i].get(ky,None))

        logger2.info("获取分页获取修改过的关键词成功！nick:%s , start_time:%s ,api_name:%s " % (self.nick,start_time,self.api_name ))

        setattr(self.fkey,"keyword_list",sub_fkey)
        return self.fkey
