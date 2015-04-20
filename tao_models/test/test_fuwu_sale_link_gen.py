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

from fuwu_sale_link_gen import FuwuSaleLinkGen
from tao_models.common.exceptions import TaoApiMaxRetryException
from TaobaoSdk.Exceptions import ErrorResponseException
@unittest.skipUnless('regression' in settings.RUNTYPE, "Regression Test Case")
class TestFuwuSaleLinkGen(unittest.TestCase):
    '''
    taobao.fuwu.sale.link.gen
    服务平台营销链接生成接口
    '''
    @classmethod
    def setUpClass(cls):
        set_api_source('SDK_TEST')
        cls.tcinfo = 'API Test - taobao.fuwu.sale.link.gen'
        cls.testInputDatas = [{'nick':'chinchinstyle','soft_code':'SYB','param_str':'','popException':True, 'exceptionClass':ErrorResponseException, 'exceptInfo':{'msg':'Missing required arguments:param_str'}},
                              {'nick':'chinchinstyle','soft_code':'SYB','param_str':'{"param":{"aCode":"ACT_847721042_130517115127","itemList":["ts-1796606-3"],"promIds":[10058712],"type":2},"sign":"E2D1E94845D1B82FFE9FBF8A9D18E"}','popException':True, 'exceptionClass':TaoApiMaxRetryException,'exceptInfo':{'msg':'times ,but still failed. reason'}},
                              {'nick':'chinchinstyle','soft_code':'SYB','param_str':'{"param":{"aCode":"ACT_847721042_140701125528","itemList":["ts-1796606-3:12*2"],"promIds":[10379425],"type":1},"sign":"413A07570D5B3115D7D44003FF7D7E38"}','popException':False, 'exceptionClass':None,'exceptInfo':{'msg':'times ,but still failed. reason'}}
                              ]
        cls.valueType = {'returnValue':str}

    def setUp(self):
        pass

    def testAreasGet(self):
        for inputdata in self.testInputDatas:
            is_poped = False
            try:
                returnValue = FuwuSaleLinkGen.fuwu_sale_link_gen(inputdata['nick'],inputdata['param_str'],inputdata['soft_code'])
                self.assertTrue(type(returnValue) == self.valueType['returnValue'], self.tcinfo)
            except Exception, e:
                is_poped = True
                self.assertRaises(inputdata['exceptionClass'])
            finally:
                self.assertEqual(inputdata['popException'],is_poped,self.tcinfo)

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
alltests = unittest.TestLoader().loadTestsFromTestCase(TestFuwuSaleLinkGen)
