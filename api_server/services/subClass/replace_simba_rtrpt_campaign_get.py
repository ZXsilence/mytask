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
        #输入参数判断
        rt_date = self.ivalue
        if datetime.combine(datetime.now(),dt.time()).strftime("%Y-%m-%d") != str(rt_date):
           logger2.error("输入参数有误，实时时间传入不对！")
           raise ApiVirtualResponseException("输入参数有误，实时时间传入不对！")

        #从样本库获取campaign的样本报表
        db_campaign_rpt_list = [{'impression': '1909', 'roi': '10.23', 'directtransactionshipping': '1', 'cost': '1010', 'directtransaction': '10330', 'favshoptotal': '0', 'click': '14', 'transactiontotal': '10330', 'indirecttransactionshipping': '0', 'source': '1', 'indirecttransaction': '0', 'thedate': '2017-09-26', 'transactionshippingtotal': '1', 'coverage': '7.14', 'directcarttotal': '1', 'favtotal': '0', 'cpm': '529.07', 'ctr': '0.73', 'campaignid': '10745526', 'cpc': '72.14', 'search_type': '0', 'indirectcarttotal': '0', 'carttotal': '1', 'favitemtotal': '0'}, {'impression': '519', 'roi': '0.00', 'cpm': '0.00', 'ctr': '0.00', 'campaignid': '10745526', 'cpc': '0.00', 'search_type': '2', 'source': '1', 'thedate': '2017-09-26', 'cost': '0', 'coverage': '0.00', 'click': '0'}, {'impression': '3', 'roi': '0.00', 'cpm': '0.00', 'ctr': '0.00', 'campaignid': '10745526', 'cpc': '0.00', 'search_type': '2', 'source': '2', 'thedate': '2017-09-26', 'cost': '0', 'coverage': '0.00', 'click': '0'}, {'impression': '521', 'cpm': '1598.85', 'ctr': '1.92', 'campaignid': '10745526', 'cpc': '83.30', 'search_type': '0', 'source': '4', 'thedate': '2017-09-26', 'cost': '833', 'click': '10'}, {'impression': '625', 'cpm': '1107.20', 'ctr': '1.60', 'campaignid': '10745526', 'cpc': '69.20', 'search_type': '2', 'source': '4', 'thedate': '2017-09-26', 'cost': '692', 'click': '10'}, {'impression': '2', 'roi': '0.00', 'cpm': '0.00', 'ctr': '0.00', 'campaignid': '10745526', 'cpc': '0.00', 'search_type': '0', 'source': '5', 'thedate': '2017-09-26', 'cost': '0', 'coverage': '0.00', 'click': '0'}, {'impression': '989', 'cpm': '141.56', 'ctr': '0.20', 'campaignid': '10745526', 'cpc': '70.00', 'search_type': '2', 'source': '5', 'thedate': '2017-09-26', 'cost': '140', 'click': '2'}, {'impression': '762', 'roi': '0.00', 'cpm': '0.00', 'ctr': '0.00', 'campaignid': '13758630', 'cpc': '0.00', 'search_type': '0', 'source': '1', 'thedate': '2017-09-26', 'cost': '0', 'coverage': '0.00', 'click': '0'}, {'impression': '13', 'roi': '0.00', 'cpm': '0.00', 'ctr': '0.00', 'campaignid': '13758630', 'cpc': '0.00', 'search_type': '2', 'source': '1', 'thedate': '2017-09-26', 'cost': '0', 'coverage': '0.00', 'click': '0'}]
        #api获取计划id，方便对样本库中计划id进行替换
        from tao_models.simba_campaigns_get import SimbaCampaignsGet
        campaign_list = SimbaCampaignsGet.get_campaign_list(self.nick)
        api_campaign_ids = [k['campaign_id'] for k in campaign_list]
        db_campaign_ids = list(set([k['campaignid'] for k in db_campaign_rpt_list]))

        #当api_campaign_ids > db_campaign_ids 时，按db_campaign_ids封装。默认未封装的计划报表是{}
        api_ids = len(api_campaign_ids)
        db_ids = len(db_campaign_ids)
        if api_ids > db_ids:
            api_campaign_ids = api_campaign_ids[:db_ids]
        elif api_ids < db_ids:
            db_campaign_ids = db_campaign_ids[:api_ids]
        db_campaign_rpt_list = [k for k in db_campaign_rpt_list if k['campaignid'] in db_campaign_ids]
        # db中的计划id--> 实际计划id的映射关系
        db2api_campaign_ids_dict = dict(zip(db_campaign_ids,api_campaign_ids))

        #样本库报表的键值
        #db_keys = list(set(reduce(operator.add,[k.keys() for k in db_campaign_rpt_list])))
        db_keys = self.fkey[0].toDict().keys()

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
        for i , rpt in enumerate(db_campaign_rpt_list):
            for key in db_keys:
                if key == "thedate":
                    setattr(self.fkey[i],key,rt_date)
                elif key == "campaignid":
                    setattr(self.fkey[i],key,db2api_campaign_ids_dict[rpt[key]])
                else:
                    setattr(self.fkey[i],key,rpt.get(key,'0'))

        logger2.info("获取计划实时报表成功！nick:%s,campaign_ids:%s " % (self.nick, ",".join([str(k) for k in api_campaign_ids])))
        return self.fkey
