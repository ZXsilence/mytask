#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: tanglingling
@contact: tanglingling@maimiaotech.com
@date: 2015-04-08 16:32
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
from user_seller_get import UserSellerGet


@unittest.skipUnless('regression' in settings.RUNTYPE, "Regression Test Case")
class TestUserSellerGet(unittest.TestCase):
    '''
    查询卖家用户信息（只能查询有店铺的用户） 只能卖家类应用调用。
    '''
    @classmethod
    def setUpClass(cls):
        set_api_source('SDK_TEST')
        cls.testData = [{'nick':'','popException':False,'exceptClass':None},
                        {'nick':'chinchinstyle','popException':False,'exceptClass':None},
                        {'nick':'_nick_not_exists_','popException':True,'exceptClass':InvalidAccessTokenException},
                        ]
        cls.errs={'type_error':'assert return type error','value_error':'assert return value error','assert_error':'assert exception'}
    
    def seUp(self):
        pass
    def test_get_user_seller(self):
        for inputdata in self.testData:
            is_popped = False
            try:
                res = UserSellerGet.get_user_seller(inputdata['nick'])
                self.assertEqual(type(res),dict,self.errs['type_error'])
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

alltests = unittest.TestLoader().loadTestsFromTestCase(TestUserSellerGet)
