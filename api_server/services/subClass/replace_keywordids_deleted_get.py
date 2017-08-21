#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: tanglingling
@contact: tanglingling@maimiaotech.com
@date: 2017-08-21 09:46
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

class ReplaceKeywordidsDeletedGet(ReplaceBase):
    '''
    获取已经删除的关键词id
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

        sid = ShopInfo.get_sid_by_nick(self.nick)
        delete_ids = KeywordChangedTestService.get_keywordids_deleted(sid,start_time,page_no,page_size)

        #返回值替换
        self.fkey = delete_ids
        logger2.info("获取已经删除的关键词成功！nick:%s,delete_ids:%s" % (self.nick,delete_ids))

        return self.fkey

