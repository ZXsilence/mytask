#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: tanglingling
@contact: tanglingling@maimiaotech.com
@date: 2015-04-10 10:00
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""

import sys
sys.path.append('../')
sys.path.append('../../')
import settings
import datetime
import logging
import logging.config
import unittest
from api_server.conf import set_env
set_env.getEnvReady()
from api_server.conf.settings import set_api_source
from item_get import ItemGet
from tao_models.common.exceptions import TaoApiMaxRetryException
from TaobaoSdk.Exceptions import ErrorResponseException,SDKRetryException

from tao_models.common.exceptions import W2securityException, InvalidAccessTokenException#导入异常类
from simba_rpt_adgroupnonsearchbase_get import SimbaRptAdgroupnonsearchBaseGet
from simba_rpt_adgroupnonsearcheffect_get import SimbaRptAdgroupnonsearchEffectGet
from tao_models.common.getCampaignAdgroup import GetCampaignAdgroup
@unittest.skipUnless('regression' in settings.RUNTYPE, "Regression Test Case")
class TestSimbaRptAdgroupnonsearchBaseGet(unittest.TestCase):
    '''
    simba_rpt_adgroupnonsearchbase_get 推广组下的定向推广基础数据查询
    simba_rpt_adgroupnonsearcheffect_get 推广组下的定向推广效果数据查询
    '''
    @classmethod
    def setUpClass(cls):
        set_api_source('SDK_TEST')
        
        shop = GetCampaignAdgroup.get_a_valid_shop()
        nick=shop['nick']
        campaign=GetCampaignAdgroup.get_a_valid_campaign(nick)
        campaign_id = campaign['campaign_id']
        adgroup = GetCampaignAdgroup.get_a_valid_adgroup(nick,campaign,"SYB",shop['sid'])
        adgroup_id = adgroup['adgroup_id']    
        start = datetime.datetime.now()-datetime.timedelta(days=7)
        end = datetime.datetime.now()-datetime.timedelta(days=1)

        cls.testData = [{'nick':nick,'campaign_id':campaign_id,'adgroup_id':adgroup_id,'start':start,'end':end,'popException':False,'exceptClass':None},
                        #{'nick':'','campaign_id':campaign_id,'adgroup_id':adgroup_id,'start':start,'end':end,'popException':True,'exceptClass':TypeError},
                        {'nick':nick,'campaign_id':0,'adgroup_id':0,'start':start,'end':end,'popException':False,'exceptClass':None},
                        ]
        cls.errs={'effect_error':'error find in API: simba_rpt_adgroupnonsearcheffect_get',
                  'base_error':'error find in API: simba_rpt_adgroupnonsearchbase_get',
                  'assert_error':'assert exception',
                  }
        cls.effectKeys=['adgroupid','campaignid','date','directpay','directpaycount','favitemcount','favshopcount','indirectpay','indirectpaycount','nick','placeid','roi']
        cls.baseKeys=['adgroupid','campaignid','click','cost','cpc','cpm','ctr','date','impressions','nick','placeid']
    
    def seUp(self):
        pass
    def test_get_rpt_adgroupbase_list(self):
        pass
        '''
        for inputdata in self.testData:
            is_popped = False
            try:
                res = SimbaRptAdgroupnonsearchBaseGet.get_rpt_adgroupnonsearchbase_list(inputdata['nick'], inputdata['campaign_id'],inputdata['adgroup_id'],inputdata['start'], inputdata['end'])
                self.assertEqual(type(res), list, self.errs['base_error'])
                if len(res)>0:
                    for k in self.baseKeys:
                        self.assertTrue(res[0].has_key(k), self.errs['base_error'])

                res =  SimbaRptAdgroupnonsearchEffectGet.get_rpt_adgroupnonsearcheffect_list(inputdata['nick'], inputdata['campaign_id'],inputdata['adgroup_id'],inputdata['start'],inputdata['end'])
                self.assertEqual(type(res), list, self.errs['effect_error'])
                if len(res)>0:
                    for k in self.effectKeys:
                        self.assertTrue(res[0].has_key(k), self.errs['effect_error'])

            except Exception, e:
                is_popped = True
                self.assertRaises(inputdata['exceptClass'])
            finally:
                self.assertEqual(is_popped,inputdata['popException'],self.errs['assert_error'])
        '''

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == '__main__':
    unittest.main()

alltests = unittest.TestLoader().loadTestsFromTestCase(TestSimbaRptAdgroupnonsearchBaseGet)
