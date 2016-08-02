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
        cls.assertKeys=[u'deadline',u'item_code']
    def seUp(self):
        pass
    def test_get_vas_subscribe(self):
        for inputdata in self.testData:
            try:
                res = VasSubscribeGet.get_vas_subscribe(inputdata['nick'], inputdata['soft_code'])
                self.assertEqual(type(res),list)
                for res0 in res:
                    self.assertEqual(sorted(res0.keys()),sorted(self.assertKeys))
            except ErrorResponseException,e:
                self.assertTrue(inputdata['popException'])
            except InvalidAccessTokenException, e:
                self.assertTrue(inputdata['popException'])
            except KeyError, e:
                self.assertTrue(inputdata['popException'])
            except Exception, e:
                if inputdata['popException'] ==False:
                    import traceback;traceback.print_exc() 
                    raise e
                else :
                    self.assertRaises(inputdata['exceptClass'])

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == '__main__':                                                       
    unittest.main()

alltests = unittest.TestLoader().loadTestsFromTestCase(TestVasSubscribeGet)
