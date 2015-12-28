#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: luxiaowen
@contact: luxiaowen@maimiaotech.com
@date: 2015-04-16 11:55
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""

import sys
import os
if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../../../comm_lib/'))
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('normal_test')

import unittest
import datetime
from tao_models.simba_adgroupsbycampaignid_get import SimbaAdgroupsbycampaignidGet
from tao_models.simba_adgroup_mobilediscount_delete import SimbaAdgroupMobilediscountDelete
from tao_models.simba_adgroup_mobilediscount_update import SimbaAdgroupMobilediscountUpdate
from tao_models.simba_campaign_platform_get import SimbaCampaignPlatformGet
from TaobaoSdk.Exceptions import ErrorResponseException
from tao_models.common.exceptions import InvalidAccessTokenException

class test_mobile_discount(unittest.TestCase):
    maxDiff = None
    @classmethod
    def setUpClass(cls):
        pass
    
    def setUp(self):
        pass
    
    def test_delete_adgroup_mobile_discount(self):
        data = [{'nick':'麦苗科技001','campaign_id':9214487,'adgroup_id':628189528}]
        for item in data:
            nick = item['nick']
            campaign_id = item['campaign_id']
            adgroups = SimbaAdgroupsbycampaignidGet.get_adgroup_list_by_campaign(nick, campaign_id)
            adgroup_ids = [adgroups[0]['adgroup_id']]
            SimbaAdgroupMobilediscountDelete.delete_mobile_discount_by_adgroup_ids(nick,adgroup_ids)
            res = SimbaAdgroupsbycampaignidGet.get_adgroup_list_by_campaign(nick,campaign_id)
            for it in res:
                if it['adgroup_id']== adgroups[0]['adgroup_id']:
                    actual_result = it['mobile_discount']
            returnValue = SimbaCampaignPlatformGet.get_campaign_platform(nick,campaign_id)
            campaign_mobile_discount = returnValue['mobile_discount']
            self.assertEqual(actual_result,campaign_mobile_discount)
    
    def test_update_adgroup_mobile_discount(self):
        data = [{'nick':'麦苗科技001','campaign_id':9214487,'adgroup_id':628189528}]
        for item in data:
            nick = item['nick']
            campaign_id = item['campaign_id']
            adgroups = SimbaAdgroupsbycampaignidGet.get_adgroup_list_by_campaign(nick, campaign_id)
            adgroup_ids = [adgroups[0]['adgroup_id']]
            old_mobile_discount = adgroups[0]['mobile_discount']
            new_mobile_discount = old_mobile_discount+1
            #SimbaAdgroupMobilediscountDelete.delete_mobile_discount_by_adgroup_ids(nick,adgroup_ids)
            SimbaAdgroupMobilediscountUpdate.update_mobile_discount_by_adgroup_ids(nick,adgroup_ids,new_mobile_discount)
            res = SimbaAdgroupsbycampaignidGet.get_adgroup_list_by_campaign(nick,campaign_id)
            for it in res:
                if it['adgroup_id']== adgroups[0]['adgroup_id']:
                    actual_result = it['mobile_discount']
            self.assertEqual(actual_result,new_mobile_discount)
    
    def tearDown(self):
        pass
    
    @classmethod
    def tearDownClass(cls):
        pass
if __name__ == "__main__":
    unittest.main()
alltests = unittest.TestLoader().loadTestsFromTestCase(test_mobile_discount)
