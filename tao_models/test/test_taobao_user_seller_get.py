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
        cls.assertKeys=['has_more_pic', 'is_golden_seller', 'item_img_num', 'magazine_subscribe', 'sex', 'liangpin', 'sign_food_seller_promise', 'promoted_type', 'prop_img_size', 'seller_credit', 'user_id', 'item_img_size', 'online_gaming', 'nick', 'is_lightning_consignment', 'type', 'status', 'consumer_protection', 'has_sub_stock', 'auto_repost', 'vip_info', 'avatar', 'vertical_market', 'alipay_bind', 'prop_img_num']
        cls.hasNick=['sex']
    def seUp(self):
        pass
    def test_get_user_seller(self):
        import copy
        for inputdata in self.testData:
            try:
                res = UserSellerGet.get_user_seller(inputdata['nick'])
                self.assertEqual(type(res),dict)
                preKeys=copy.deepcopy(self.assertKeys)
                if inputdata.get('nick'):
                    preKeys = list(set(preKeys)-set(self.hasNick))
                self.assertEqual(sorted(res.keys()),sorted(preKeys))
            except InvalidAccessTokenException , e:
                self.assertTrue(inputdata['popException'])
            except Exception, e:
                if inputdata['popException'] ==False:
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

alltests = unittest.TestLoader().loadTestsFromTestCase(TestUserSellerGet)
