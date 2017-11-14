#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: tanglingling
@contact: tanglingling@maimiaotech.com
@date: 2017-10-30 13:24
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""
import logging
logger2 = logging.getLogger("api_virtual")
import time
import copy
import json
from exceptions import ApiVirtualResponseException
from replace_base import ReplaceBase

class ReplaceSimbaRptAdgroupkeywordbaseGet(ReplaceBase):
    '''
    关键词基础报表替换
    '''
    def replace_ret_values(self):
        is_summary = True if self.source=='SUMMARY' else False
        #call virtual db_model
        from report_db.db_models_sample.rpt_keywordbase import RptKeywordbaseSample
        from shop_db.db_models.shop_info import ShopInfo
        sid = ShopInfo.get_sid_by_nick(self.nick)
        rpt_list = []
        try:
            rpt_list = RptKeywordbaseSample.get_rpt_list_by_adgroup_ids(self.start_time,self.end_time,self.nick,sid,[self.adgroup_id],is_summary)
        except Exception,e :
            logger2.error("获取关键词基础报表失败！",exc_info=True)
            raise ApiVirtualResponseException("获取关键词基础报表失败！")
        if rpt_list == []:
            self.fkey = []
            return json.dumps(self.fkey)
        #返回结构长度扩展
        self.fkey = json.loads(self.fkey)
        len_fkey = len(self.fkey)
        len_rpt_list = len(rpt_list)
        if len_rpt_list > len_fkey:
            self.fkey.extend([ copy.deepcopy(self.fkey[0]) for i in range(len_rpt_list-len_fkey)])
        elif len_rpt_list < len_fkey:
            self.fkey = self.fkey[:(len_fkey-len_rpt_list)]
        #返回值替换
        rpt_keys = rpt_list[0].keys()
        for i,rpt in enumerate(rpt_list):
            for key in rpt_keys:
                if key == "date":
                    self.fkey[i][key] = rpt[key].strftime("%Y-%m-%d")
                else:
                    self.fkey[i][key] = unicode(rpt[key])

        logger2.info("获取关键词基础报表成功！start_time:%s,end_time:%s,nick:%s,campaign_id:%s,adgroup_id:%s" % (self.start_time,self.end_time,self.nick,self.campaign_id,self.adgroup_id))
        return json.dumps(self.fkey)
