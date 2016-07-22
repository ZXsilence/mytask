#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: tanglingling
@contact: tanglingling@maimiaotech.com
@date: 2015-06-15 11:15
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""

import sys
import os
if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../../'))
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('normal_test')

import datetime as dt
from datetime import datetime
sys.path.append('../../../backends/')
from adgroup_db.db_models.adgroups import Adgroups
from campaign_db.db_models.campaigns import Campaigns
from shop_db.db_models.shop_info import ShopInfo
from tao_models.simba_adgroupsbycampaignid_get import SimbaAdgroupsbycampaignidGet
from tao_models.simba_keywordsbyadgroupid_get import  SimbaKeywordsbyadgroupidGet

from tao_models.simba_rpt_campadgroupbase_get import   SimbaRptCampadgroupBaseGet
from tao_models.simba_rpt_campadgroupeffect_get import SimbaRptCampadgroupEffectGet
from user_center.db_models.join_query import JoinQuery

from tao_models.simba_campaigns_get import SimbaCampaignsGet 


class GetCampaignAdgroup(object):  
    @classmethod
    def get_a_valid_shop(cls,soft_code="SYB",test=False):
        testShop=[{'nick':'chinchinstyle','sid':62847885,'soft_code':"SYB"},{'nick':'麦苗科技001','sid':101240238,'soft_code':"SYB"}]
        if test:
            return testShop[1]
        all_shops = ShopInfo.get_shop_infos_by_num(50,False,soft_code)
        for shop in all_shops:
            if shop:
                nick = shop['nick']
                soft_code = shop['soft_code']
                sid = shop['sid']
                campaign = GetCampaignAdgroup.get_a_valid_campaign(nick,soft_code)
                if campaign:
                    campaign_id = campaign['campaign_id']
                    adgroup = GetCampaignAdgroup.get_a_valid_adgroup(nick,[campaign_id],soft_code,sid)
                    if adgroup:
                        return shop
        return testShop[0]

    @classmethod
    def get_a_valid_campaign(cls,nick,soft_code='SYB'):
        campaigns = Campaigns.get_all_online_campaigns_by_nick(nick)
        if len(campaigns)==0:
            return []
        return  campaigns[0]

    @classmethod
    def get_a_valid_adgroup(cls,nick,campaign_ids,soft_code='SYB',sid=None):
        if None==sid:
            shop_info = ShopInfo.get_shop_info_by_nick(soft_code,nick)
            sid = shop_info['sid']
        if type(campaign_ids) == dict:
            campaign_ids=[campaign_ids]
        for campaign_id in campaign_ids:
            adgroups = SimbaAdgroupsbycampaignidGet.get_adgroup_list_by_campaign(nick,campaign_id)
            for adgroup in adgroups:
                if adgroup['online_status'] == 'online':
                    return adgroup
        return []
    
    @classmethod
    def get_adgroup_has_keyword(cls,nick,campaign_id):
        adgroups = SimbaAdgroupsbycampaignidGet.get_adgroup_list_by_campaign(nick,campaign_id)
        for adgroup in adgroups:
            kw_list = SimbaKeywordsbyadgroupidGet.get_keyword_list_by_adgroup(nick, adgroup['adgroup_id'])
            if len(kw_list)!=0:
                return adgroup['adgroup_id']
        return []
    @classmethod
    def get_has_adgroup_rpt_nick(cls):
        #
        # 无脑遍历，耗时.暂时没找到其他方法，返回一个有报表的推广组
        #

        #1,找出有效nick
        deadline_start=datetime.now()
        start = datetime.now()-dt.timedelta(days=7)
        end = datetime.now()-dt.timedelta(days=1)
        from user_center.services.crm_db_service import CrmDBService
        customers = CrmDBService.get_customer_list_by_deadline_start(deadline_start)
        for customer in customers:
            nick = customer['nick']
            #2,找出该nick有效campaign
            campaigns = SimbaCampaignsGet.get_campaign_list(nick)
            if len(campaigns)==0:
                continue
            campaign_ids = [k['campaign_id'] for k in campaigns]
            for campaign_id in campaign_ids:
                #3,找出计划下的有效adgroup
                adgroups = SimbaAdgroupsbycampaignidGet.get_adgroup_list_by_campaign(nick,campaign_id)
                if len(adgroups)==0:
                    continue
                #4,找出有报表的推广组
                res =SimbaRptCampadgroupEffectGet.get_rpt_adgroupeffect_list(nick,campaign_id,start ,end,'SEARCH,CAT', '1,2,4,5')
                if not res:
                    continue
                return (nick,campaign_id)
        return (None,None)






if __name__=='__main__':
    soft_code = "SYB"
    shop = GetCampaignAdgroup.get_a_valid_shop(soft_code,False)
    nick =  shop['nick']
    print nick
    campaign = GetCampaignAdgroup.get_a_valid_campaign(nick)
    print campaign
    adgroup = GetCampaignAdgroup.get_a_valid_adgroup(nick,campaign)
    print adgroup


