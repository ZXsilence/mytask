#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: tanglingling
@contact: tanglingling@maimiaotech.com
@date: 2015-04-08 19:32
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
from taobao_fuwu_scores_get import FuwuScoresGet


@unittest.skipUnless('regression' in settings.RUNTYPE, "Regression Test Case")
class TestFuwuScoresGet(unittest.TestCase):
    '''
    服务平台评价查询接口
    根据日期、查询appkey对应服务评价，每次调用只能查询某一天服务评价信息，
    可设置分页查询，页大小最大为100，非实时接口，延迟时间为30分钟
    '''
    @classmethod
    def setUpClass(cls):
        set_api_source('SDK_TEST')
        cls.testData = [{'d':datetime.datetime.today(),'soft_code':'SYB','popException':False,'excepClass':None},
                        {'d':'2015-04-08','soft_code':'SYB','popException':False,'excepClass':None},
                        {'d':datetime.datetime.today(),'soft_code':'ZZK','popException':True,'excepClass':InvalidAccessTokenException},
                        ]
        cls.errs={'type_error':'return type error',
                  'value_error':'return value error',
                  'assert_error':'assert exception',
                  }
    def seUp(self):
        pass
    def test_get_time(self):
        for inputdata in self.testData:
            is_popped  = False
            try:
                suggest_list = FuwuScoresGet.get_all_fuwu_scores(inputdata['d'],inputdata['soft_code'])
                self.assertEqual( type(suggest_list), list , self.errs['type_error'])
                self.assertGreaterEqual( len(suggest_list), 0 , self.errs['value_error'])
            except Exception, e:
                is_popped = True
                self.assertRaises(inputdata['excepClass'])
            finally:
                self.assertEqual(is_popped,inputdata['popException'])
    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == '__main__':
    unittest.main()

alltests = unittest.TestLoader().loadTestsFromTestCase(TestFuwuScoresGet)
