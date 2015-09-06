#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wangying
@contact: wangying@maimiaotech.com
@date: 2014-09-25 14:07
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

from simba_adgroupsbycampaignid_get import SimbaAdgroupsbycampaignidGet
from tao_models.common.exceptions import TaoApiMaxRetryException
from tao_models.common.exceptions import InvalidAccessTokenException
from TaobaoSdk.Exceptions import ErrorResponseException
@unittest.skipUnless('regression' in settings.RUNTYPE, "Regression Test Case")
class TestSimbaAdgroupsbycampaignidGet(unittest.TestCase):
    '''
    taobao.simba.adgroupsbycampaignid.get
    批量得到推广计划下的推广组
    '''
    @classmethod
    def setUpClass(cls):
        set_api_source('SDK_TEST')
        cls.tcinfo = 'API Test - taobao.simba.adgroupsbycampaignid.get'
        cls.testInputDatas_get = [{'nick': '__NotExistNick__','campaign_id':3328400,'popException':True, 'exceptionClass':InvalidAccessTokenException},
                                  {'nick': 'chinchinstyle','campaign_id':3328400,'popException':False, 'exceptionClass':None}
                                  ]
        cls.testInputDatas_get_count = [{'nick': '__NotExistNick__','campaign_id':3328400,'popException':True, 'exceptionClass':InvalidAccessTokenException},
                                        {'nick': 'chinchinstyle','campaign_id':3328400,'popException':False, 'exceptionClass':None}
                                        ]
        cls.valueType = {'returnValue_get':list, 'returnValue_get_count':int}
        cls.itemFields = ['default_price', 'item_price', 'title', 'img_url','online_status', 'num_iid', 'campaign_id', 'modified_time', 'category_ids', 'nick', 'create_time', 'offline_type', 'adgroup_id']

    def setUp(self):
        pass

    def test_get_adgroup_list_by_campaign(self):
        for inputdata in self.testInputDatas_get:
            is_poped = False
            self.tcinfo = 'API Test - taobao.simba.adgroupsbycampaignid.get'
            self.tcinfo = self.tcinfo + str(inputdata)
            try:
                returnValue = SimbaAdgroupsbycampaignidGet.get_adgroup_list_by_campaign(inputdata['nick'],inputdata['campaign_id'])
                self.assertTrue(type(returnValue) == self.valueType['returnValue_get'], self.tcinfo)
                for returnValueItem in returnValue:
                    itemKeys = returnValueItem.keys()
                    for item in itemKeys:
                        self.assertTrue(item in self.itemFields, self.tcinfo)
            except Exception, e:
                is_poped = True
                self.assertRaises(inputdata['exceptionClass'])
            finally:
                self.assertEqual(inputdata['popException'],is_poped,self.tcinfo)

    def test_get_adgroup_count(self):
        for inputdata in self.testInputDatas_get_count:
            is_poped = False
            self.tcinfo = 'API Test - taobao.simba.adgroupsbycampaignid.get'
            self.tcinfo = self.tcinfo + str(inputdata)
            try:
                returnValue = SimbaAdgroupsbycampaignidGet.get_adgroup_count(inputdata['nick'],inputdata['campaign_id'])
                self.assertTrue(type(returnValue) == self.valueType['returnValue_get_count'], self.tcinfo)
            except Exception, e:
                is_poped = True
                self.assertRaises(inputdata['exceptionClass'])
            finally:
                self.assertEqual(inputdata['popException'],is_poped,self.tcinfo)
    #@unittest.expectedFailure
    #def test_expectedFailure(self):
    #    """test"""
    #    print self.testdata

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == '__main__':                                                       
    unittest.main()

#custtests = unittest.TestSuite(map(TestReportService, ['test_rpt_cust_1']))
alltests = unittest.TestLoader().loadTestsFromTestCase(TestSimbaAdgroupsbycampaignidGet)
