#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: tanglingling
@contact: tanglingling@maimiaotech.com
@date: 2015-04-08 11:00
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
from vas_subscribe_get import VasSubscribeGet

@unittest.skipUnless('regression' in settings.RUNTYPE, "Regression Test Case")
class TestVasSubscribeGet(unittest.TestCase):
    '''
    订单关系查询
    用于ISV根据登录进来的淘宝会员名查询该为该会员开通哪些收费项目，ISV只能查询自己名下的应用及收费项目的订购情况
    '''
    @classmethod
    def setUpClass(cls):
        set_api_source('SDK_TEST')
        cls.testData = [{'nick':'麦苗科技001','soft_code':'SYB','popException':False,'exceptClass':None},
                        {'nick':'','soft_code':'SYB','popException':True,'exceptClass':ErrorResponseException},
                        {'nick':'_nick_not_exists_','soft_code':'','popException':True,'exceptClass':InvalidAccessTokenException},
                        {'nick':'麦苗科技001','soft_code':'','popException':True,'exceptClass':KeyError},
                        {'nick':'麦苗科技001','soft_code':'ZZ','popException':True,'exceptClass':KeyError},
                        ]
        cls.errs={'type_error':'assert return type error','value_error':'assert return value error','assert_error':'assert exception'}
    
    def seUp(self):
        pass
    def test_get_vas_subscribe(self):
        for inputdata in self.testData:
            is_popped = False
            try:
                res = VasSubscribeGet.get_vas_subscribe(inputdata['nick'], inputdata['soft_code'])
                self.assertEqual(type(res),list,self.errs['type_error'])
                self.assertGreaterEqual(len(res),0,self.errs['value_error'])
            except Exception, e:
                is_popped = True
                self.assertRaises(inputdata['exceptClass'])
            finally:
                self.assertEqual(is_popped,inputdata['popException'],self.errs['assert_error'])


    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == '__main__':                                                       
    unittest.main()

alltests = unittest.TestLoader().loadTestsFromTestCase(TestVasSubscribeGet)
