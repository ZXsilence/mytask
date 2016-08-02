#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: tanglingling
@contact: tanglingling@maimiaotech.com
@date: 2015-04-08 13:22
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
    订购记录导出 
    用于ISV查询自己名下的应用及收费项目的订购记录
    '''
    @classmethod
    def setUpClass(cls):
        set_api_source('SDK_TEST')
        cls.testData = [{'nick':'麦苗科技001','popException':False,'exceptClass':None},
                        {'nick':'_nick_not_exists_','popException':True,'exceptClass':InvalidAccessTokenException},
                        ]
        cls.assertKeys=['has_more_pic', 'is_golden_seller', 'item_img_num', 'magazine_subscribe', 'sex', 'liangpin', 'sign_food_seller_promise', 'promoted_type', 'prop_img_size', 'seller_credit', 'user_id', 'item_img_size', 'online_gaming', 'nick', 'is_lightning_consignment', 'type', 'status', 'consumer_protection', 'has_sub_stock', 'auto_repost', 'vip_info', 'avatar', 'vertical_market', 'alipay_bind', 'prop_img_num']
    def seUp(self):
        pass
    def test_get_user_seller(self):
        for inputdata in self.testData:
            try:
                res = UserSellerGet.get_user_seller(inputdata['nick'])
                self.assertEqual(type(res),dict)
                import copy
                preKeys=copy.deepcopy(self.assertKeys)
                self.assertEqual(sorted(res.keys()),sorted(preKeys))
            except InvalidAccessTokenException , e:
                self.assertTrue(inputdata['popException'])
            except Exception, e:
                if inputdata['popException'] == False:
                    import traceback;traceback.print_exc()
                else:
                    self.assertRaises(inputdata['exceptClass'])
    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == '__main__':
    unittest.main()

alltests = unittest.TestLoader().loadTestsFromTestCase(TestUserSellerGet)
