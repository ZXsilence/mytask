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
        #输入参数判断
        rt_date = self.ivalue
        if datetime.combine(datetime.now(),dt.time()).strftime("%Y-%m-%d") != str(rt_date):
           logger2.error("输入参数有误，实时时间传入不对！")
           raise ApiVirtualResponseException("输入参数有误，实时时间传入不对！")
        db_adgroup_rpt_list = [{'impression': '1389', 'adgroupid': '722979883', 'cpm': '181.43', 'ctr': '0.07', 'campaignid': '16448401', 'cpc': '252.00', 'search_type': '0', 'source': '1', 'thedate': '2017-09-26', 'cost': '252', 'click': '1'}, {'impression': '1601', 'adgroupid': '722979883', 'roi': '0.00', 'cpm': '0.00', 'ctr': '0.00', 'campaignid': '16448401', 'cpc': '0.00', 'search_type': '2', 'source': '1', 'thedate': '2017-09-26', 'cost': '0', 'coverage': '0.00', 'click': '0'}, {'impression': '25', 'adgroupid': '722979883', 'roi': '0.00', 'cpm': '0.00', 'ctr': '0.00', 'campaignid': '16448401', 'cpc': '0.00', 'search_type': '0', 'source': '2', 'thedate': '2017-09-26', 'cost': '0', 'coverage': '0.00', 'click': '0'}, {'impression': '324', 'adgroupid': '722979883', 'roi': '0.00', 'directtransactionshipping': '0', 'cost': '5', 'directtransaction': '0', 'favshoptotal': '0', 'click': '1', 'transactiontotal': '0', 'indirecttransactionshipping': '0', 'source': '2', 'indirecttransaction': '0', 'thedate': '2017-09-26', 'transactionshippingtotal': '0', 'coverage': '0.00', 'directcarttotal': '1', 'favtotal': '0', 'cpm': '15.43', 'ctr': '0.31', 'campaignid': '16448401', 'cpc': '5.00', 'search_type': '2', 'indirectcarttotal': '0', 'carttotal': '1', 'favitemtotal': '0'}, {'impression': '4384', 'adgroupid': '722979883', 'roi': '5.71', 'directtransactionshipping': '1', 'cost': '77125', 'directtransaction': '218000', 'favshoptotal': '0', 'click': '163', 'transactiontotal': '440000', 'indirecttransactionshipping': '2', 'source': '4', 'indirecttransaction': '222000', 'thedate': '2017-09-26', 'transactionshippingtotal': '3', 'coverage': '1.84', 'directcarttotal': '3', 'favtotal': '2', 'cpm': '17592.38', 'ctr': '3.72', 'campaignid': '16448401', 'cpc': '473.16', 'search_type': '0', 'indirectcarttotal': '11', 'carttotal': '14', 'favitemtotal': '2'}, {'impression': '5069', 'adgroupid': '722979883', 'roi': '0.00', 'directtransactionshipping': '0', 'cost': '6488', 'directtransaction': '0', 'favshoptotal': '1', 'click': '21', 'transactiontotal': '0', 'indirecttransactionshipping': '0', 'source': '4', 'indirecttransaction': '0', 'thedate': '2017-09-26', 'transactionshippingtotal': '0', 'coverage': '0.00', 'directcarttotal': '2', 'favtotal': '3', 'cpm': '1279.94', 'ctr': '0.41', 'campaignid': '16448401', 'cpc': '308.95', 'search_type': '2', 'indirectcarttotal': '0', 'carttotal': '2', 'favitemtotal': '2'}, {'impression': '73', 'adgroupid': '791982654', 'roi': '0.00', 'cpm': '0.00', 'ctr': '0.00', 'campaignid': '16448401', 'cpc': '0.00', 'search_type': '0', 'source': '1', 'thedate': '2017-09-26', 'cost': '0', 'coverage': '0.00', 'click': '0'}, {'impression': '85', 'adgroupid': '791982654', 'roi': '0.00', 'directtransactionshipping': '0', 'cost': '848', 'directtransaction': '0', 'favshoptotal': '0', 'click': '3', 'transactiontotal': '0', 'indirecttransactionshipping': '0', 'source': '4', 'indirecttransaction': '0', 'thedate': '2017-09-26', 'transactionshippingtotal': '0', 'coverage': '0.00', 'directcarttotal': '0', 'favtotal': '0', 'cpm': '9976.47', 'ctr': '3.53', 'campaignid': '16448401', 'cpc': '282.67', 'search_type': '0', 'indirectcarttotal': '5', 'carttotal': '5', 'favitemtotal': '0'}]
        db_keys = self.fkey[0].toDict().keys()
        #获取该用户的计划id
        from tao_models.simba_campaigns_get import SimbaCampaignsGet
        campaign_list = SimbaCampaignsGet.get_campaign_list(self.nick)
        api_campaign = [k for k in campaign_list if k['campaign_id'] == self.campaign_id]
        try:
            api_campaign = api_campaign[0]
        except Exception ,e :
            logger2.error("%s 不存在campaign_id=%s的计划！" % (self.nick,self.campaign_id))
            raise ApiVirtualResponseException("%s 不存在campaign_id=%s的计划！" % (self.nick,self.campaign_id))
        #campaign级别：db->api 映射关系建立
        db_campaign_ids = list(set([k['campaignid'] for k in db_adgroup_rpt_list]))
        if len(db_campaign_ids) > 1:
            db_campaign_ids = db_campaign_ids[:1]
        db2api_campaign_ids_dict = dict(zip(db_campaign_ids,[self.campaign_id]))
        #db报表重新筛选
        db_adgroup_rpt_list = [k for k in db_adgroup_rpt_list if k['campaignid'] in db_campaign_ids ]
        #对api返回rpt条数进行扩充
        len_api = len(self.fkey)
        len_db = len(db_adgroup_rpt_list)
        if len_db > len_api:
            self.fkey.extend([copy.deepcopy(self.fkey[0]) for i in range(len_db-len_api)])
        elif len_db < len_api:
            self.fkey = self.fkey[:(len_api - len_db)]
        if self.fkey == []:
            return self.fkey

        #获取该用户的推广组id
        from tao_models.simba_adgroupsbycampaignid_get import SimbaAdgroupsbycampaignidGet
        adgroup_list = SimbaAdgroupsbycampaignidGet.get_adgroup_list_by_campaign(self.nick,self.campaign_id)
        api_adgroup_ids = [int(k['adgroup_id']) for k in adgroup_list if k['online_status'] == "online" and k['offline_type']=="online"]
        db_adgroup_ids = list(set([k['adgroupid'] for k in db_adgroup_rpt_list] ))
        #to_delete_adgroup_rpt_ids = db_adgroup_ids - api_adgroup_ids
        ##删除已删除推广组的rpt
        #下架商品对应推广组不进行api封装
        from tao_models.items_onsale_get import ItemsOnsaleGet
        items_list = ItemsOnsaleGet.get_item_list(self.nick)
        online_num_iids = [k['num_iid'] for k in items_list]
        api_adgroup_ids = [int(k['adgroup_id']) for k in adgroup_list if k['online_status'] == "online" and k['offline_type']=="online" and int(k['num_iid']) in online_num_iids]

        #adgroup级别：db-api 映射关系建立
        db_adgroup_ids = db_adgroup_ids[:len(api_adgroup_ids)]
        db2api_adgroup_ids_dict = dict(zip(db_adgroup_ids,api_adgroup_ids))

        #对api返回值进行封装
        wrap_adgroup_ids = []
        for i ,rpt in enumerate(db_adgroup_rpt_list):
            for key in db_keys:
                if key == "thedate":
                    setattr(self.fkey[i],key,rt_date)
                elif key == "campaignid":
                    setattr(self.fkey[i],key,db2api_campaign_ids_dict[rpt[key]])
                elif key == "adgroupid":
                    setattr(self.fkey[i],key,db2api_adgroup_ids_dict[rpt[key]])
                    wrap_adgroup_ids.append(db2api_adgroup_ids_dict[rpt[key]])
                else:
                    setattr(self.fkey[i],key,rpt.get(key,'0'))
        wrap_adgroup_ids = list(set(wrap_adgroup_ids))
        logger2.info("获取推广组实时报表成功！nick:%s,campaign_id:%s,adgroup_ids:%s " % (self.nick,self.campaign_id,",".join([str(k) for k in wrap_adgroup_ids])))
        for k in self.fkey:
            print k.toDict()
        return self.fkey
