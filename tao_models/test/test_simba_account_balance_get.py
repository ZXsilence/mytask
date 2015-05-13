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
#from MTextTestRunner import TextTestRunner

from api_server.conf import set_env
set_env.getEnvReady()
from api_server.conf.settings import set_api_source

from simba_account_balance_get import SimbaAccountBalanceGet
from tao_models.common.exceptions import InvalidAccessTokenException
@unittest.skipUnless('regression' in settings.RUNTYPE, "Regression Test Case")
class TestSimbaAccountBalanceGet(unittest.TestCase):
    '''
    taobao.simba.account.balance.get
    获取实时余额，”元”为单位
    '''
    @classmethod
    def setUpClass(cls):
        set_api_source('SDK_TEST')
        cls.testInputDatas = [{'nick': '__NotExistNick__','popException':True, 'exceptionClass':InvalidAccessTokenException},
                              {'nick': 'chinchinstyle','popException':False, 'exceptionClass':None}
                              ]
        cls.tcinfo = 'API Test - taobao.simba.account.balance.get'
        cls.valueType = {'returnValue':float}

    def setUp(self):
        pass

    def test_get_account_balance(self):
        for inputdata in self.testInputDatas:
            is_poped = False
            try:
                returnValue = SimbaAccountBalanceGet.get_account_balance(inputdata['nick'])
                self.assertTrue(type(returnValue) == self.valueType['returnValue'], self.tcinfo)
            except Exception, e:
                is_poped = True
                self.assertRaises(inputdata['exceptionClass'])
            finally:
                self.assertEqual(is_poped, inputdata['popException'], self.tcinfo)


    #@unittest.skip("Unconditionally skip the decorated test")
    #def test_skip(self):
    #    """test"""
    #    pass

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
alltests = unittest.TestLoader().loadTestsFromTestCase(TestSimbaAccountBalanceGet)
