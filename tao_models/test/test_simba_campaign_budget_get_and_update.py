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

from simba_campaign_budget_get import SimbaCampaignBudgetGet
from simba_campaign_budget_update import SimbaCampaignBudgetUpdate
from tao_models.common.exceptions import TaoApiMaxRetryException
from tao_models.common.exceptions import InvalidAccessTokenException
from TaobaoSdk.Exceptions import ErrorResponseException
@unittest.skipUnless('regression' in settings.RUNTYPE, "Regression Test Case")
class TestSimbaCampaignBudgetGetAndUpdate(unittest.TestCase):
    '''
    taobao.simba.campaign.budget.get
    取得一个推广计划的日限额
    taobao.simba.campaign.budget.update
    更新一个推广计划的日限额
    '''
    @classmethod
    def setUpClass(cls):
        set_api_source('SDK_TEST')
        cls.tcinfo_get = 'API Test - taobao.simba.campaign.budget.get'
        cls.tcinfo_update = 'API Test - taobao.simba.campaign.budget.update'
        cls.testInputDatas_get = [{'nick': '__NotExistNick__','campaign_id':3328400,'popException':True, 'exceptionClass':InvalidAccessTokenException},
                                  {'nick': 'chinchinstyle','campaign_id':3328400,'popException':False, 'exceptionClass':None}
                                  ]
        cls.testInputDatas_update = [{'nick': '__NotExistNick__','campaign_id':None,'budget':None,'use_smooth':None,'popException':True, 'exceptionClass':InvalidAccessTokenException},
                                     {'nick': 'chinchinstyle','campaign_id':3328400,'budget':None,'use_smooth':'false','popException':False, 'exceptionClass':None},
                                     {'nick': 'chinchinstyle','campaign_id':3328400,'budget':33,'use_smooth':'true','popException':False, 'exceptionClass':None}
                                     ]
        cls.valueType = {'returnValue_get':dict, 'returnValue_update':dict}
        cls.itemFields_get = ['budget', 'modified_time', 'campaign_id', 'nick', 'create_time', 'is_smooth']#'nick,is_smooth,budget,modified_time,campaign_id'.split(',')
        cls.itemFields_update = 'nick,is_smooth,budget,campaign_id,modified_time,create_time'.split(',')

    def setUp(self):
        pass

    def test_campaign_budget_get(self):
        for inputdata in self.testInputDatas_get:
            self.tcinfo_get = 'API Test - taobao.simba.campaign.budget.get'
            self.tcinfo_update += str(inputdata)
            is_poped = False
            try:
                returnValue = SimbaCampaignBudgetGet.campaign_budget_get(inputdata['nick'], inputdata['campaign_id'])
                self.assertTrue(type(returnValue) == self.valueType['returnValue_get'], self.tcinfo_get)
                itemKeys = returnValue.keys()
                for key in itemKeys:
                    self.assertTrue(key in self.itemFields_get, self.tcinfo_get)
            except Exception, e:
                is_poped = True
                self.assertRaises(inputdata['exceptionClass'])
            finally:
                self.assertEqual(inputdata['popException'],is_poped,self.tcinfo_get)

    def test_campaign_budget_update(self):
        for inputdata in self.testInputDatas_update:
            self.tcinfo_update = 'API Test - taobao.simba.campaign.budget.update'
            self.tcinfo_update += str(inputdata)
            is_poped = False
            try:
                returnValue = SimbaCampaignBudgetUpdate.campaign_budget_update(inputdata['nick'], inputdata['campaign_id'], inputdata['budget'], inputdata['use_smooth'])
                self.assertTrue(type(returnValue) == self.valueType['returnValue_update'], self.tcinfo_update)
                itemKeys = returnValue.keys()
                for key in itemKeys:
                    self.assertTrue(key in self.itemFields_update, self.tcinfo_update)
            except Exception, e:
                is_poped = True
                self.assertRaises(inputdata['exceptionClass'])
            finally:
                self.assertEqual(inputdata['popException'],is_poped,self.tcinfo_update)

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
alltests = unittest.TestLoader().loadTestsFromTestCase(TestSimbaCampaignBudgetGetAndUpdate)
