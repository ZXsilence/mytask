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

sys.path.append('../../../backends/')
from adgroup_db.db_models.adgroups import Adgroups
from campaign_db.db_models.campaigns import Campaigns
from shop_db.db_models.shop_info import ShopInfo

class GetCampaignAdgroup(object):
    @classmethod
    def get_a_valid_shop(cls,soft_code="SYB",test=False):
        testShop=[{'nick':'chinchinstyle','sid':62847885,'soft_code':"SYB"},{'nick':'麦苗科技001','sid':101240238,'soft_code':"SYB"}]
        if test:
            return testShop[1]
        all_shops = ShopInfo.get_valid_shop_infos_list(soft_code)
        for shop in all_shops:
            if shop:
                nick = shop['nick']
                soft_code = shop['soft_code']
                sid = shop['sid']
                campaign = GetCampaignAdgroup.get_a_valid_campaign(nick,soft_code)
                if campaign:
                    adgroup = GetCampaignAdgroup.get_a_valid_adgroup(nick,campaign,soft_code,sid)
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
    def get_a_valid_adgroup(cls,nick,campaign_list,soft_code='SYB',sid=None):
        if None==sid:
            shop_info = ShopInfo.get_shop_info_by_nick(soft_code,nick)
            sid = shop_info['sid']
        if type(campaign_list) == dict:
            campaign_list=[campaign_list]
        for campaign in campaign_list:
            campaign_id = campaign['campaign_id']
            adgroups = Adgroups.get_adgroups_by_campaign_id(sid,campaign_id)
            for adgroup in adgroups:
                if adgroup['online_status'] == 'online':
                    return adgroup
        return []


if __name__=='__main__':
    soft_code = "SYB"
    shop = GetCampaignAdgroup.get_a_valid_shop(soft_code,False)
    nick =  shop['nick']
    print nick
    campaign = GetCampaignAdgroup.get_a_valid_campaign(nick)
    print campaign
    adgroup = GetCampaignAdgroup.get_a_valid_adgroup(nick,campaign)
    print adgroup


