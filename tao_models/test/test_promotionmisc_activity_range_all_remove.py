#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: tanglingling
@contact: tanglingling@maimiaotech.com
@date: 2015-03-27 09:30
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

from promotionmisc_activity_range_list_get import PromotionmiscActivityRangeListGet#获取商品数
from promotionmisc_activity_range_all_remove import PromotionmiscActivityRangeAllRemove #清空所有商品
from tao_models.common.exceptions import W2securityException, InvalidAccessTokenException #导入异常类

@unittest.skipUnless('regression' in settings.RUNTYPE, "Regression Test Case")
class TestPromotionmiscActivityRangeAllRemove(unittest.TestCase):
    '''
    清空活动参与的所有商品
    '''
    @classmethod
    def setUpClass(cls):
        set_api_source('SDK_TEST')
        cls.tcinfo='API Test - taobao.PromotionmiscActivityRangeAllRemove'
        cls.testInputData = [{'nick':'chinchinstyle','activity_id':654062470,'soft_code':'SYB','popException':False,'exceptionClass':None},
                             {'nick':'chinchinstyle','activity_id':123,'soft_code':'SYB','popException':True,'exceptionClass':W2securityException}, #activty_id  invalid
                             {'nick':'_nick_not_exists_','activity_id':654062470,'soft_code':'SYB','popException':True,'exceptionClass':InvalidAccessTokenException}, # nick invalid
                             {'nick':'','activity_id':654062470,'soft_code':'SYB','popException':True,'exceptionClass':W2securityException}, #nick not exists
                             ]

    def setUp(self):
        pass
    def test_clear_promotionm_activity_range(self):
        for inputdata in self.testInputData:
            is_poped = False
            try:
                res_boolean = PromotionmiscActivityRangeAllRemove.clear_promotionm_activity_range(inputdata['nick'],inputdata['activity_id'],inputdata['soft_code'])
                self.assertTrue(res_boolean,'Remove all products failed! Assert False!')
                res_list = PromotionmiscActivityRangeListGet.get_promotionm_activity_range(inputdata['nick'],inputdata['activity_id'])
                res_len = len(res_list)
                self.assertEqual(res_len,0,'Products number is not Zero, assert Failed !')
            except Exception, e:
                is_poped = True
                self.assertRaises(inputdata['exceptionClass'])
            finally:
                self.assertEqual(inputdata['popException'], is_poped, 'assert exception')
    def tearDown(self):
        pass 
    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == "__main__":
    unittest.main()

alltests = unittest.TestLoader().loadTestsFromTestCase(TestPromotionmiscActivityRangeAllRemove)

