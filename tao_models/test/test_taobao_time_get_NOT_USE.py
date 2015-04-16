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
from taobao_time_get import TimeGet

@unittest.skipUnless('regression' in settings.RUNTYPE, "Regression Test Case")
class TestTimeGet(unittest.TestCase):
    '''
    获取淘宝系统当前时间
    '''
    @classmethod
    def setUpClass(cls):
        set_api_source('SDK_TEST')
    
    def seUp(self):
        pass

    @unittest.skip("Unconditionally skip the decorated test")
    def test_get_time(self):
        res =  TimeGet.get_time()
        self.assertEqual(type(res),datetime,'error find in API:taobao_time_get')
    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == '__main__':
    unittest.main()

alltests = unittest.TestLoader().loadTestsFromTestCase(TestTimeGet)
