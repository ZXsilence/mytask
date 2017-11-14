#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: tanglingling
@contact: tanglingling@maimiaotech.com
@date: 2017-09-26 13:19
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

class ReplaceSimbaRtrptAdgroupGet(ReplaceBase):
    '''
    推广组实时报表，从样本库中抽样进行api封装返回
    ps:
        调试前涉及到假数据，所以存在db_campaign_ids和api_campaign_ids的映射。实际通过nick、campaign_id取样本库数据时，映射过程可以省略
    '''
    def replace_ret_values(self):
        from tao_models.simba_adgroupsbycampaignid_get import SimbaAdgroupsbycampaignidGet
        #输入参数判断
        rt_date =str( self.ivalue)
        if datetime.combine(datetime.now(),dt.time()).strftime("%Y-%m-%d") != str(rt_date):
           logger2.error("输入参数有误，实时时间传入不对！")
           raise ApiVirtualResponseException("输入参数有误，实时时间传入不对！")
        from report_db.db_models_sample.rpt_adgrouprealtime import RptAdgroupRealTimeSample
        from shop_db.db_models.shop_info import ShopInfo
        sid = ShopInfo.get_sid_by_nick(self.nick)
        try:
            adgroups = SimbaAdgroupsbycampaignidGet.get_adgroup_list_by_campaign(self.nick,self.campaign_id)
        except Exception,e:
            logger.error("调用simba_adgroupsbycampaignid_get出错！",exec_info=True)
            raise ApiVirtualResponseException("调用simba_adgroupsbycampaignid_get出错！")

        adgroup_ids = [k['adgroup_id'] for k in adgroups]
        try:
            db_adgroup_rpt_list = RptAdgroupRealTimeSample.get_rpt_list_by_adgroup_ids(rt_date,rt_date,self.nick,sid,adgroup_ids,False)
        except Exception,e:
            logger.error("获取推广组实时报表失败！",exc_info=True)
            raise ApiVirtualResponseException("获取推广组实时报表失败！")

        #根据最终rpt，对api返回rpt条数进行扩充
        len_api = len(self.fkey)
        len_db = len(db_adgroup_rpt_list)
        if len_db > len_api:
            self.fkey.extend([copy.deepcopy(self.fkey[0]) for i in range(len_db-len_api)])
        elif len_db < len_api:
            self.fkey = self.fkey[:(len_api - len_db)]
        if self.fkey == []:
            return self.fkey

        #对api返回值进行封装
        db_keys = db_adgroup_rpt_list[0].keys()
        for i ,rpt in enumerate(db_adgroup_rpt_list):
            for key in db_keys:
                setattr(self.fkey[i],key,rpt.get(key,'0'))
        
        logger2.info("获取推广组实时报表成功！nick:%s,campaign_id:%s,adgroup_ids:%s " % (self.nick,self.campaign_id,",".join([str(k) for k in adgroup_ids])))
        for k in self.fkey:
            print k.toDict()
        return self.fkey
