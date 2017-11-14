#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: tanglingling
@contact: tanglingling@maimiaotech.com
@date: 2017-09-26 15:46
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""
import logging
logger2 = logging.getLogger("api_virtual")
import time
import copy
from datetime import datetime
import datetime as dt
from exceptions import ApiVirtualResponseException
from replace_base import ReplaceBase
import operator

#导入db_model
class ReplaceSimbaRtrptBidwordGet(ReplaceBase):
    '''
    关键词实时报表
    '''
    def replace_ret_values(self):
        #输入参数判断
        rt_date = str(self.ivalue)
        if datetime.combine(datetime.now(),dt.time()).strftime("%Y-%m-%d") != str(rt_date):
           logger2.error("输入参数有误，实时时间传入不对！")
           raise ApiVirtualResponseException("输入参数有误，实时时间传入不对！")
        from report_db.db_models_sample.rpt_keywordrealtime import RptKeywordRealTimeSample
        from shop_db.db_models.shop_info import ShopInfo
        sid = ShopInfo.get_sid_by_nick(self.nick)
        try:
            db_bidword_rpt_list = RptKeywordRealTimeSample.get_rpt_list_by_adgroup_ids(rt_date,rt_date,self.nick,sid,[self.adgroup_id],False)
        except Exception,e:
            logger2.error("获取关键词实时报表失败！",exc_info=True)
            raise ApiVirtualResponseException(e.msg or "获取关键词实时报表失败！")

        #api返回值长度扩展
        rpt_len = len(db_bidword_rpt_list)
        fkey_len = len(self.fkey)
        if rpt_len > fkey_len:
            self.fkey.extend([ copy.deepcopy(self.fkey[0]) for i in range(rpt_len-fkey_len)])
        elif rpt_len < fkey_len:
            self.fkey = self.fkey[:(fkey_len-rpt_len)]

        #api返回值封装
        db_keys = db_bidword_rpt_list[0].keys()
        for i , rpt in enumerate(db_bidword_rpt_list):
            for key in db_keys:
                setattr(self.fkey[i],key,rpt.get(key,'0'))

        logger2.info("获取关键词实时报表成功！nick:%s , campaign_id:%s, adgroup_id:%s " % (self.nick, self.campaign_id, self.adgroup_id))
        return self.fkey
