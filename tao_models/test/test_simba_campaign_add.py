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

from simba_campaign_add import SimbaCampaignAdd
from tao_models.common.exceptions import TaoApiMaxRetryException
from tao_models.common.exceptions import InvalidAccessTokenException
from TaobaoSdk.Exceptions import ErrorResponseException
@unittest.skipUnless('regression' in settings.RUNTYPE, "Regression Test Case")
class TestSimbaCampaignAdd(unittest.TestCase):
    '''
    taobao.simba.campaign.add
    创建一个推广计划
    '''
    @classmethod
    def setUpClass(cls):
        set_api_source('SDK_TEST')
        cls.tcinfo = 'API Test - taobao.simba.campaign.add'
        cls.testInputDatas = [{'nick': '__NotExistNick__','title':'','popException':True, 'exceptionClass':InvalidAccessTokenException},
                              {'nick': 'chinchinstyle','title':'API测试-add','popException':True, 'exceptionClass':ErrorResponseException}
                                  ]

    def setUp(self):
        pass

    def test_get_campaign(self):
        for inputdata in self.testInputDatas:
            self.tcinfo = 'API Test - taobao.simba.campaign.add'
            self.tcinfo += str(inputdata)
            is_poped = False
            try:
                returnValue = SimbaCampaignAdd.add_campaign(inputdata['nick'])
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
alltests = unittest.TestLoader().loadTestsFromTestCase(TestSimbaCampaignAdd)
