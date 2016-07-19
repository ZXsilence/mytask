#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: tanglingling
@contact: tanglingling@maimiaotech.com
@date: 2015-04-07 15:50
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
from TaobaoSdk.Exceptions import ErrorResponseException
from tao_models.common.exceptions import W2securityException, InvalidAccessTokenException#导入异常类
from vas_order_search import VasOrderSearch
@unittest.skipUnless('regression' in settings.RUNTYPE, "Regression Test Case")
class TestVasOrderSearch(unittest.TestCase):
    '''
    订单记录导出
    '''
    @classmethod
    def setUpClass(cls):
        set_api_source('SDK_TEST')
        cls.testData_yesterday = [{'soft_code':'SYB','popException':False,'exceptClass':None},
                                  {'soft_code':'','popException':True,'exceptClass':KeyError},
                                  {'soft_code':'ZZ','popException':True,'exceptClass':InvalidAccessTokenException},
                                  ]
        cls.assertKeys= ['order_cycle_end', 'article_item_name', 'total_pay_fee', 'article_code', 'article_name', 'create', 'order_id', 'item_code', 'prom_fee', 'order_cycle', 'nick', 'biz_type', 'fee', 'order_cycle_start', 'refund_fee', 'biz_order_id']
        cls.hasActivity = ['activity_code']
    def seUp(self):
        pass
    def test_search_vas_order_yesterday(self):
        for inputdata in self.testData_yesterday:
            is_popped= False
            try:
                res = VasOrderSearch.search_vas_order_yesterday(inputdata['soft_code'])
                self.assertEqual(type(res),list )
                self.assertGreaterEqual(len(res),1)
                import copy
                preKeys = copy.deepcopy(self.assertKeys)
                for res0 in res:
                    self.assertEqual(sorted(res0.keys()),sorted(preKeys))
            except AssertionError , e :
                preKeys += self.hasActivity  #将activity_code 校验放到异常中来
                self.assertEqual(sorted(res0.keys()),sorted(preKeys))
            except InvalidAccessTokenException , e:
                if inputdata['popException']==False:
                    import traceback;traceback.print_exc()
                    raise e
            except Exception, e:
                if inputdata['popException']==False:
                    import traceback;traceback.print_exc()
                    raise e
                else:
                    self.assertRaises(inputdata['exceptClass'])
    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == '__main__':                                                       
    unittest.main()

alltests = unittest.TestLoader().loadTestsFromTestCase(TestVasOrderSearch)
