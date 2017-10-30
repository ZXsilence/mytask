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
    _from_sample_db = True

    def replace_ret_values(self):
        #输入参数判断
        rt_date = str(self.ivalue)
        if datetime.combine(datetime.now(),dt.time()).strftime("%Y-%m-%d") != str(rt_date):
           logger2.error("输入参数有误，实时时间传入不对！")
           raise ApiVirtualResponseException("输入参数有误，实时时间传入不对！")
        if self._from_sample_db:
            from report_db.db_models_sample.rpt_keywordrealtime import RptKeywordRealTimeSample
            from shop_db.db_models.shop_info import ShopInfo
            sid = ShopInfo.get_sid_by_nick(self.nick)
            try:
                db_bidword_rpt_list = RptKeywordRealTimeSample.get_rpt_list_by_adgroup_ids(rt_date,rt_date,self.nick,sid,[self.adgroup_id],False)
            except Exception,e:
                logger2.error("获取关键词实时报表失败！",exc_info=True)
                raise ApiVirtualResponseException(e.msg or "获取关键词实时报表失败！")

        else:
            db_bidword_rpt_list = [{'impression': '77', 'adgroupid': '722979883', 'roi': '0.0', 'directtransactionshipping': '0', 'cost': '1248', 'directtransaction': '0.0', 'favshoptotal': '0', 'click': '3', 'transactiontotal': '0.0', 'indirecttransactionshipping': '0', 'source': '4', 'indirecttransaction': '0.0', 'bidwordid': '355996751575', 'thedate': '2017-09-26', 'transactionshippingtotal': '0', 'directcarttotal': '0', 'favtotal': '2', 'cpm': '16207.79', 'ctr': '3.9', 'campaignid': '16448401', 'cpc': '416.0', 'indirectcarttotal': '0', 'carttotal': '0', 'favitemtotal': '2'},{'impression': '41', 'adgroupid': '722979883', 'campaignid': '16448401', 'source': '4', 'thedate': '2017-09-26', 'bidwordid': '355996751590'},{'impression': '100', 'adgroupid': '722979883', 'cpm': '29160.0', 'ctr': '8.0', 'campaignid': '16448401', 'cpc': '364.5', 'source': '4', 'thedate': '2017-09-26', 'cost': '2916', 'bidwordid': '368599341651', 'click': '8'}]

        db_campaign_ids = []
        db_adgroup_ids = []
        db_bidword_ids = []
        for k in db_bidword_rpt_list:
            db_campaign_ids.append(k['campaignid'])
            db_adgroup_ids.append(k['adgroupid'])
            db_bidword_ids.append(k['bidwordid'])
        db_campaign_ids = list(set(db_campaign_ids))
        db_adgroup_ids = list(set(db_adgroup_ids))
        db_bidword_ids = list(set(db_bidword_ids))

        #campaign_id映射
        #获取该用户的计划id
        from tao_models.simba_campaigns_get import SimbaCampaignsGet
        campaign_list = SimbaCampaignsGet.get_campaign_list(self.nick)
        api_campaign = [k for k in campaign_list if k['campaign_id'] == self.campaign_id]
        try:
            api_campaign = api_campaign[0]
        except Exception ,e :
            logger2.error("%s 不存在campaign_id=%s的计划！" % (self.nick,self.campaign_id))
            raise ApiVirtualResponseException("%s 不存在campaign_id=%s的计划！" % (self.nick,self.campaign_id))
        db2api_campaign_ids_dict = dict(zip(db_campaign_ids,[self.campaign_id]))

        #adgroup_id映射，过滤下架商品对应推广组
        #获取该用户的推广组id
        from tao_models.simba_adgroupsbycampaignid_get import SimbaAdgroupsbycampaignidGet
        from tao_models.items_onsale_get import ItemsOnsaleGet
        adgroup_list = SimbaAdgroupsbycampaignidGet.get_adgroup_list_by_campaign(self.nick,self.campaign_id)
        #下架商品对应推广组不进行api封装
        items_list = ItemsOnsaleGet.get_item_list(self.nick)
        online_num_iids = [k['num_iid'] for k in items_list]
        api_adgroup_ids = [int(k['adgroup_id']) for k in adgroup_list if k['online_status'] == "online" and k['offline_type']=="online" and int(k['num_iid']) in online_num_iids]

        if self._from_sample_db:
            #api有，db没有==》新增推广组
            #api没有，db有==》删除推广组   这2种都不进行封装
            only_api =set( api_adgroup_ids) - set(db_adgroup_ids)
            only_db = set(db_adgroup_ids) - set(api_adgroup_ids)
            # api和db都排除这2种情况
            api_adgroup_ids =list(set( api_adgroup_ids) - only_api - only_db)
            db_adgroup_ids = list(set(db_adgroup_ids) - only_api - only_db)
        #以最小的结果进行映射
        api_len = len(api_adgroup_ids)
        db_len = len(db_adgroup_ids)
        if api_len > db_len:
            api_adgroup_ids = api_adgroup_ids[:db_len]
        elif api_len < db_len:
            db_adgroup_ids = db_adgroup_ids[:api_len]

        db2api_adgroup_ids_dict = dict(zip(db_adgroup_ids,api_adgroup_ids))

        #bidword映射。实际样本库规则：
        # 1，api中有，db中没有的。是新增关键词。按db中封装
        # 2，api中没有，db中有。表示已删除关键词。按api中的封装
        from tao_models.simba_keywordsbyadgroupid_get import SimbaKeywordsbyadgroupidGet
        keyword_list = SimbaKeywordsbyadgroupidGet.get_keyword_list_by_adgroup(self.nick,self.adgroup_id)
        api_bidword_ids = [k['keyword_id'] for k in keyword_list ]
        if self._from_sample_db:
            #api有，db没有==》新增关键词
            #api没有，db有==》删除关键词   这2种都不进行封装
            only_api = set(api_bidword_ids) - set(db_bidword_ids)
            only_db = set(db_bidword_ids) - set( api_bidword_ids)
            # api、db排除这2种情况
            api_bidword_ids =list(set( api_bidword_ids) - only_api - only_db)
            db_bidword_ids =list(set( db_bidword_ids) - only_api - only_db)
        #以最小的结果进行映射
        api_k_len = len(api_bidword_ids)
        db_k_len = len(db_bidword_ids)
        if api_k_len > db_k_len:
            api_bidword_ids = api_bidword_ids[:db_k_len]
        elif api_k_len < db_k_len:
            db_bidword_ids = db_bidword_ids[:api_k_len]
        #关键词映射dict
        db2api_bidword_ids_dict = dict(zip(db_bidword_ids,api_bidword_ids))

        #db报表重新筛选:剔除下架推广组、删除推广组、删除关键词、新增关键词
        db_bidword_rpt_list = [k for k in db_bidword_rpt_list if k['adgroupid'] in db_adgroup_ids and k['bidwordid'] in db_bidword_ids]

        #api返回值长度扩展
        rpt_len = len(db_bidword_rpt_list)
        fkey_len = len(self.fkey)
        if rpt_len > fkey_len:
            self.fkey.extend([ copy.deepcopy(self.fkey[0]) for i in range(rpt_len-fkey_len)])
        elif rpt_len < fkey_len:
            self.fkey = self.fkey[:(fkey_len-rpt_len)]

        #api返回值封装
        db_keys = [k.keys() for k in db_bidword_rpt_list]
        if db_keys == []:
            self.fkey=[]
            return self.fkey
        db_keys = reduce(operator.add,db_keys)
        db_keys = list(set(db_keys))
        for i , rpt in enumerate(db_bidword_rpt_list):
            for key in db_keys:
                if key == "campaignid":
                    setattr(self.fkey[i],key,db2api_campaign_ids_dict[rpt[key]])
                elif key == "adgroupid":
                    setattr(self.fkey[i],key, db2api_adgroup_ids_dict[rpt[key]])
                elif key == "bidwordid":
                    setattr(self.fkey[i],key,db2api_bidword_ids_dict[rpt[key]])
                elif key == "thedate":
                    setattr(self.fkey[i],key, rt_date)
                else:
                    setattr(self.fkey[i],key,rpt.get(key,'0'))

        logger2.info("获取关键词实时报表成功！nick:%s , campaign_id:%s, adgroup_id:%s " % (self.nick, self.campaign_id, self.adgroup_id))
        return self.fkey
