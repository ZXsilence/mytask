#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: tanglingling
@contact: tanglingling@maimiaotech.com
@date: 2017-09-25 16:27
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

class ReplaceSimbaRtrptCampaignGet(ReplaceBase):
    '''
    计划实时报表，从样本库中取样，然后对api进行封装返回
    报表类型（搜索：0,类目出价：1, 单品定向：2, 店铺定向:3）
    流量来源( PC站内:1， PC站外:2 , 移动站内:4，移动站外:5)
    ps:
        调试前涉及到假数据，所以存在db_campaign_ids和api_campaign_ids的映射。实际通过nick、campaign_id取样本库数据时，映射过程可以省略
    '''
    def replace_ret_values(self):
        from tao_models.simba_campaigns_get import SimbaCampaignsGet
        campaign_list = SimbaCampaignsGet.get_campaign_list(self.nick)
        api_campaign_ids = [k['campaign_id'] for k in campaign_list]
        #输入参数判断
        rt_date = str(self.ivalue)
        if datetime.combine(datetime.now(),dt.time()).strftime("%Y-%m-%d") != str(rt_date):
           logger2.error("输入参数有误，实时时间传入不对！")
           raise ApiVirtualResponseException("输入参数有误，实时时间传入不对！")

        #从样本库获取campaign的样本报表
        from report_db.db_models_sample.rpt_campaignrealtime import RptCampaignRealTimeSample
        from shop_db.db_models.shop_info import ShopInfo
        sid = ShopInfo.get_sid_by_nick(self.nick)
        try:
            db_campaign_rpt_list = []
            for campaign_id in api_campaign_ids:
                db_campaign_rpt_list.extend(RptCampaignRealTimeSample.get_rpt_list(rt_date,rt_date,self.nick,sid,campaign_id,False))
        except Exception ,e:
            logger2.error("获取计划实时报表失败！",exec_info=True)
            raise ApiVirtualResponseException("获取计划实时报表失败！")
        #api返回键的扩充；因为1个计划有条分平台rpt。所以按db_campaign_rpt_list长度进行扩充
        db_rpt_len = len(db_campaign_rpt_list)
        ret_rpt_len = len(self.fkey)
        if db_rpt_len > ret_rpt_len:
            self.fkey.extend([copy.deepcopy(self.fkey[0]) for i in range(db_rpt_len-ret_rpt_len)])
        elif db_rpt_len < ret_rpt_len:
            self.fkey = self.fkey[:(ret_rpt_len-db_rpt_len)]
        if self.fkey == []:
            return self.fkey

        #api返回值封装
        db_keys = db_campaign_rpt_list[0].keys()
        for i , rpt in enumerate(db_campaign_rpt_list):
            for key in db_keys:
                setattr(self.fkey[i],key,rpt.get(key,'0'))

        logger2.info("获取计划实时报表成功！nick:%s,campaign_ids:%s " % (self.nick, ",".join([str(k) for k in api_campaign_ids])))
        return self.fkey
