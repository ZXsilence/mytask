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

from simba_campaign_area_update import SimbaCampaignAreaUpdate
from tao_models.common.exceptions import TaoApiMaxRetryException
from tao_models.common.exceptions import InvalidAccessTokenException
from TaobaoSdk.Exceptions import ErrorResponseException
@unittest.skipUnless('regression' in settings.RUNTYPE, "Regression Test Case")
class TestSimbaCampaignAreaUpdate(unittest.TestCase):
    '''
    taobao.simba.campaign.area.update
    更新一个推广计划的投放地域
    '''
    @classmethod
    def setUpClass(cls):
        set_api_source('SDK_TEST')
        cls.tcinfo = 'API Test - taobao.simba.campaign.area.update'
        cls.testInputDatas = [{'nick': '__NotExistNick__','campaign_id':3328400,'area':None,'popException':True, 'exceptionClass':InvalidAccessTokenException},
                              {'nick': 'chinchinstyle','campaign_id':9214487,'area':None,'popException':True, 'exceptionClass':ErrorResponseException},
                              {'nick': 'chinchinstyle','campaign_id':3328400,'area':[19,461],'popException':False, 'exceptionClass':None},
                              {'nick': 'chinchinstyle','campaign_id':3328400,'area':'all','popException':False, 'exceptionClass':None}
                              ]
        cls.valueType = {'returnValue':dict}
        cls.itemFields = 'nick,campaign_id,area'.split(',')

    def setUp(self):
        pass

    def test_get_campaign_area(self):
        for inputdata in self.testInputDatas:
            self.tcinfo = 'API Test - taobao.simba.campaign.area.update'
            self.tcinfo += str(inputdata)
            is_poped = False
            try:
                returnValue = SimbaCampaignAreaUpdate.update_campaign_area(inputdata['nick'],inputdata['campaign_id'],inputdata['area'])
                self.assertTrue(type(returnValue) == self.valueType['returnValue'], self.tcinfo)
                itemKeys = returnValue.keys()
                for item in itemKeys:
                    self.assertTrue(item in self.itemFields, self.tcinfo)
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
alltests = unittest.TestLoader().loadTestsFromTestCase(TestSimbaCampaignAreaUpdate)
