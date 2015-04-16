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

from shop_get import ShopGet
from shop_db.services.shop_info_service import ShopInfoService
from tao_models.common.exceptions import TaoApiMaxRetryException
from tao_models.common.exceptions import InvalidAccessTokenException
from TaobaoSdk.Exceptions import ErrorResponseException
@unittest.skipUnless('regression' in settings.RUNTYPE, "Regression Test Case")
class TestShopGet(unittest.TestCase):
    '''
    taobao.shop.get
    获取卖家店铺的基本信息
    '''
    @classmethod
    def setUpClass(cls):
        set_api_source('SDK_TEST')
        cls.tcinfo = 'API Test - taobao.shop.get'
        cls.testInputDatas_get = [{'nick': '__NotExistNick__','popException':True, 'exceptionClass':ErrorResponseException},
                                  {'nick': 'chinchinstyle','popException':False, 'exceptionClass':None}
                                  ]
        cls.testInputDatas_with_access_code = [{'nick': '__NotExistNick__','access_token':'__NotExistToken__','soft_code':'SYB','popException':True, 'exceptionClass':ErrorResponseException},
                                               {'nick': 'chinchinstyle','access_token':None,'soft_code':'SYB', 'popException':False, 'exceptionClass':None}
                                               ]
        cls.valueType = {'returnValue_get':dict, 'returnValue_info':dict}
        cls.itemFields = ['shop_score', 'cid', 'created', 'modified', 'nick', 'sid', 'title', 'pic_path', 'bulletin', 'desc'] 

    def setUp(self):
        pass

    def test_get_shop(self):
        for inputdata in self.testInputDatas_get:
            is_poped = False
            try:
                returnValue = ShopGet.get_shop(inputdata['nick'])
                self.assertTrue(type(returnValue) == self.valueType['returnValue_get'], self.tcinfo)
                itemKeys = returnValue.keys()
                for item in itemKeys:
                    self.assertTrue(item in self.itemFields, self.tcinfo)
            except Exception, e:
                is_poped = True
                self.assertRaises(inputdata['exceptionClass'])
            finally:
                self.assertEqual(inputdata['popException'],is_poped,self.tcinfo)

    def test_get_shop_with_access_token(self):
        for inputdata in self.testInputDatas_with_access_code:
            is_poped = False
            try:
                if not inputdata['access_token']:
                    shop_infos = ShopInfoService.get_shop_infos(inputdata['nick'],inputdata['soft_code'],False)
                    soft_code = shop_infos[0]['soft_code']
                    access_token = shop_infos[0]['access_token']
                else:
                    access_token = inputdata['access_token']
                returnValue = ShopGet.get_shop_with_access_token(inputdata['nick'],access_token, inputdata['soft_code'])
                self.assertTrue(type(returnValue) == self.valueType['returnValue_info'], self.tcinfo)
                itemKeys = returnValue.keys()
                for item in self.itemFields:
                    self.assertTrue(item in itemKeys, self.tcinfo)
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
alltests = unittest.TestLoader().loadTestsFromTestCase(TestShopGet)
