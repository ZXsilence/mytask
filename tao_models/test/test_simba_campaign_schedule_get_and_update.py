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

from simba_campaign_schedule_get import SimbaCampaignScheduleGet
from simba_campaign_schedule_update import SimbaCampaignScheduleUpdate
from tao_models.common.exceptions import TaoApiMaxRetryException
from tao_models.common.exceptions import InvalidAccessTokenException
from TaobaoSdk.Exceptions import ErrorResponseException
@unittest.skipUnless('regression' in settings.RUNTYPE, "Regression Test Case")
class TestSimbaCampaignScheduleGetAndUpdate(unittest.TestCase):
    '''
    taobao.simba.campaign.schedule.get
    取得一个推广计划的分时折扣设置
    taobao.simba.campaign.schedule.update
    更新一个推广计划的分时折扣设置
    '''
    @classmethod
    def setUpClass(cls):
        set_api_source('SDK_TEST')
        cls.tcinfo_get = 'API Test - taobao.simba.campaign.schedule.get'
        cls.tcinfo_update = 'API Test - taobao.simba.campaign.schedule.update'
        cls.testInputDatas_get = [{'nick': '__NotExistNick__','campaign_id':3328400,'popException':True, 'exceptionClass':InvalidAccessTokenException},
                                  {'nick': 'chinchinstyle','campaign_id':9214487,'popException':True, 'exceptionClass':ErrorResponseException},
                                  {'nick': 'chinchinstyle','campaign_id':3328400,'popException':False, 'exceptionClass':None}
                                  ]
        cls.testInputDatas_update = [{'nick': '__NotExistNick__','campaign_id':None,'schedule':None,'popException':True, 'exceptionClass':InvalidAccessTokenException},
                                     {'nick': 'chinchinstyle','campaign_id':9214487,'schedule':None,'popException':True, 'exceptionClass':ErrorResponseException},
                                     {'nick': 'chinchinstyle','campaign_id':3328400,'schedule':'00:00-07:30:100;00:00-24:00:100;00:00-24:00:100;00:00-24:00:100;00:00-07:30:100;00:00-07:30:100;00:00-24:00:100','popException':False, 'exceptionClass':None},
                                     ]
        cls.valueType = {'returnValue_get':dict, 'returnValue_update':dict}
        cls.itemFields_get = 'nick,campaign_id,schedule'.split(',')
        cls.itemFields_update = 'nick,campaign_id,schedule'.split(',')

    def setUp(self):
        pass

    def test_get_campaign_schedule(self):
        for inputdata in self.testInputDatas_get:
            self.tcinfo_get = 'API Test - taobao.simba.campaign.schedule.get'
            self.tcinfo_get += str(inputdata)
            is_poped = False
            try:
                returnValue = SimbaCampaignScheduleGet.get_campaign_schedule(inputdata['nick'], inputdata['campaign_id'])
                self.assertTrue(type(returnValue) == self.valueType['returnValue_get'], self.tcinfo_get)
                itemKeys = returnValue.keys()
                for key in itemKeys:
                    self.assertTrue(key in self.itemFields_get, self.tcinfo_get)
            except Exception, e:
                is_poped = True
                self.assertRaises(inputdata['exceptionClass'])
            finally:
                self.assertEqual(inputdata['popException'],is_poped,self.tcinfo_get)

    def test_update_campaign_schedule(self):
        for inputdata in self.testInputDatas_update:
            self.tcinfo_update = 'API Test - taobao.simba.campaign.schedule.update'
            self.tcinfo_update += str(inputdata)
            is_poped = False
            try:
                returnValue = SimbaCampaignScheduleUpdate.update_campaign_schedule(inputdata['nick'], inputdata['campaign_id'], inputdata['schedule'])
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
alltests = unittest.TestLoader().loadTestsFromTestCase(TestSimbaCampaignScheduleGetAndUpdate)
