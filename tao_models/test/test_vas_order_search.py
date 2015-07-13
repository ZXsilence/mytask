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
        cls.testData_by_nick = [#{'nick':'','soft_code':'SYB','start':datetime.datetime.now() - datetime.timedelta(1),'end':datetime.datetime.now(),'popException':False,'exceptClass':None},# 拉取全部内容太耗时了
                        {'nick':'chinchinstyle','soft_code':'SYB','start':datetime.datetime.now()-datetime.timedelta(89),'end':datetime.datetime.now(),'popException':False,'exceptClass':None},
                        {'nick':'chinchinstyle','soft_code':'','start':datetime.datetime.now()-datetime.timedelta(89),'end':datetime.datetime.now(),'popException':True,'exceptClass':KeyError},
                        {'nick':'chinchinstyle','soft_code':'SYB','start':datetime.datetime.now()-datetime.timedelta(90),'end':datetime.datetime.now(),'popException':True,'exceptClass':TaoApiMaxRetryException},
                        ]

        cls.testData_yesterday = [{'soft_code':'SYB','popException':False,'exceptClass':None},
                                  {'soft_code':'','popException':True,'exceptClass':KeyError},
                                  {'soft_code':'ZZ','popException':True,'exceptClass':InvalidAccessTokenException},
                                  ]
        cls.errs={'type_error':'assert return type error','value_error':'assert return value error','assert_error':'assert exception'}
    def seUp(self):
        pass
    '''
    def test_search_vas_order_by_nick(self):
        for inputdata in self.testData_by_nick:
            is_popped = False
            try:
                res = VasOrderSearch.search_vas_order_by_nick(inputdata['start'], inputdata['end'],inputdata['soft_code'],inputdata['nick'])
                self.assertEqual(type(res),list,self.errs['type_error'])
            except Exception, e:
                is_popped = True
                self.assertRaises(inputdata['exceptClass'])
            finally:
                self.assertEqual(is_popped,inputdata['popException'],self.errs['assert_error'])
    '''
    def test_search_vas_order_yesterday(self):
        for inputdata in self.testData_yesterday:
            is_popped= False
            try:
                res = VasOrderSearch.search_vas_order_yesterday(inputdata['soft_code'])
                self.assertEqual(type(res),list ,self.errs['type_error'])
                self.assertGreaterEqual(len(res),1,self.errs['value_error'])

            except Exception, e:
                is_popped = True
                self.assertRaises(inputdata['exceptClass'])
            finally:
                self.assertEqual(is_popped,inputdata['popException'],self.errs['assert_error'])
    '''
    def itest_search_vas_order_all(self):
        for inputdata in self.testData_yesterday:
            is_popped= False
            try:
                res = VasOrderSearch.search_vas_order_all(inputdata['soft_code'])
                self.assertEqual(type(res), list ,self.errs['type_error'])
            except Exception, e:
                is_popped = True
                self.assertRaises(inputdata['exceptClass'])
            finally:
                self.assertEqual(is_popped,inputdata['popException'],self.errs['assert_error'])

    '''
    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == '__main__':                                                       
    unittest.main()

alltests = unittest.TestLoader().loadTestsFromTestCase(TestVasOrderSearch)
