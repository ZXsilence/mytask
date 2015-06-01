#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: tanglingling
@contact: tanglingling@maimiaotech.com
@date: 2015-03-27 13:36
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
from promotionmisc_activity_range_remove import PromotionmiscActivityRangeRemove#删除一个商品
from promotionmisc_activity_range_add import PromotionmiscActivityRangeAdd#增加一个商品
from tao_models.common.exceptions import W2securityException, InvalidAccessTokenException, TaoApiMaxRetryException #导入异常类
from TaobaoSdk.Exceptions import ErrorResponseException

@unittest.skipUnless('regression' in settings.RUNTYPE, "Regression Test Case")
class TestPromotionmiscActivityRangeRemove(unittest.TestCase):
    '''

    '''
    @classmethod
    def setUpClass(cls):
        set_api_source('SDK_TEST')
        cls.TestInputData = [{'nick':'chinchinstyle','activity_id':654062470,'num_iid_list':[7794896442],'soft_code':'SYB','popException':False, 'exceptionClass':None},
                             {'nick':'_nick_not_exists_','activity_id':654062470,'num_iid_list':[7794896442],'soft_code':'SYB','popException':True, 'exceptionClass':InvalidAccessTokenException }, # _nick_not_exists_
                             {'nick':'','activity_id':654062470,'num_iid_list':[7794896442],'soft_code':'SYB','popException':True,'exceptionClass':W2securityException},
                             {'nick':'chinchinstyle','activity_id':0,'num_iid_list':[7794896442],'soft_code':'SYB','popException':True, 'exceptionClass': W2securityException}, # activity_id Invalid 
                             {'nick':'chinchinstyle','activity_id':654062470,'num_iid_list':[],'soft_code':'SYB','popException':True, 'exceptionClass': ErrorResponseException}, # num_iid_list Invalid
                             {'nick':'chinchinstyle','activity_id':654062470,'num_iid_list':[0],'soft_code':'SYB','popException':True, 'exceptionClass': TaoApiMaxRetryException}, # num_iid_list Invalid
                             {'nick':'chinchinstyle','activity_id':654062470,'num_iid_list':[7794896442],'soft_code':'ZZ','popException':True, 'exceptionClass':InvalidAccessTokenException}, # soft_code Invalid
                             ]
    def setUp(self):
        pass
    def test_remove_promotionm_activity_range(self):
        for inputdata in self.TestInputData:
            is_poped = False
            try:
                res_boolean = PromotionmiscActivityRangeRemove.remove_promotionm_activity_range(inputdata['nick'],inputdata['activity_id'],inputdata['num_iid_list'],inputdata['soft_code'])
                self.assertTrue(res_boolean,'Exception found in API-test_promotionmisc_activity_range_remove')
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

alltests = unittest.TestLoader().loadTestsFromTestCase(TestPromotionmiscActivityRangeRemove)
