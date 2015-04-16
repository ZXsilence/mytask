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

from simba_campaign_areaoptions_get import SimbaCampaignAreaoptionsGet
from tao_models.common.exceptions import TaoApiMaxRetryException
from tao_models.common.exceptions import InvalidAccessTokenException
from TaobaoSdk.Exceptions import ErrorResponseException
@unittest.skipUnless('regression' in settings.RUNTYPE, "Regression Test Case")
class TestSimbaCampaignAreaoptionsGet(unittest.TestCase):
    '''
    taobao.simba.campaign.areaoptions.get
    取得推广计划的可设置投放地域列表
    '''
    @classmethod
    def setUpClass(cls):
        set_api_source('SDK_TEST')
        cls.tcinfo = 'API Test - taobao.simba.campaign.areaoptions.get'
        cls.valueType = {'returnValue':list}
        cls.itemFields = 'parent_id,area_id,name,level'.split(',')

    def setUp(self):
        pass

    def test_get_campaign_area(self):
        is_poped = False
        try:
            returnValue = SimbaCampaignAreaoptionsGet.get_campaign_areaoptions()
            self.assertTrue(type(returnValue) == self.valueType['returnValue'], self.tcinfo)
            for itemValue in returnValue:
                itemKeys = itemValue.keys()
                for item in itemKeys:
                    self.assertTrue(item in self.itemFields, self.tcinfo)
        except Exception,e:
            is_poped =  True
        finally:
            self.assertFalse(is_poped,self.tcinfo)

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
alltests = unittest.TestLoader().loadTestsFromTestCase(TestSimbaCampaignAreaoptionsGet)
