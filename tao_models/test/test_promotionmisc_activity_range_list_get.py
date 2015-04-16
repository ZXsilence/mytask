#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: tanglingling
@contact: tanglingling@maimiaotech.com
@date: 2015-03-27 11:03
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
from promotionmisc_activity_range_add import PromotionmiscActivityRangeAdd  #增加1个商品
from promotionmisc_activity_range_remove import PromotionmiscActivityRangeRemove # 删除1个商品
from tao_models.common.exceptions import W2securityException, InvalidAccessTokenException, TaoApiMaxRetryException#导入异常类
from TaobaoSdk.Exceptions import ErrorResponseException

@unittest.skipUnless('regression' in settings.RUNTYPE, "Regression Test Case")
class TestPromotionmiscActivityRangeListGet(unittest.TestCase):
    '''
    返回指定活动id的参加活动的商品列表
    '''
    @classmethod
    def setUpClass(cls):
        set_api_source('SDK_TEST')
        cls.TestInputdata = [{'nick':'chinchinstyle','activity_id':654062470,'soft_code':'SYB','popException':False,'exceptionClass':None},
                         {'nick':'_nick_not_exists_','activity_id':654062470,'soft_code':'SYB','popException':True,'exceptionClass':InvalidAccessTokenException},#nick not exists
                         {'nick':'chinchinstyle','activity_id':0,'soft_code':'SYB','popException':True,'exceptionClass': ErrorResponseException},# activity_id is not invalid
                         {'nick':'chinchinstyle','activity_id':654062470,'soft_code':'ZZ','popException':True,'exceptionClass':InvalidAccessTokenException},#soft_code invalid
                         ]
        cls.num_iid_list = [7794896442] # 
    def setUp(self):
        pass
    def test_get_promotionm_activity_range(self):
        for inputdata in self.TestInputdata:
            is_poped = False
            add_except = True
            try:
                PromotionmiscActivityRangeAdd.add_promotionm_activity_items(self.TestInputdata[0]['nick'],self.TestInputdata[0]['activity_id'],self.num_iid_list) #添加1个商品
                add_except = False
                res_list = PromotionmiscActivityRangeListGet.get_promotionm_activity_range(inputdata['nick'],inputdata['activity_id'],inputdata['soft_code']) 
                get_success = False
                for item in res_list :
                    if item['item_id'] ==  self.num_iid_list[0]:
                        get_success = True
                self.assertTrue(get_success,'get product failed !') # 获取刚添加商品失败
                
            except Exception, e:
                if add_except: # 添加商品API出错
                    print 'Exception found in taobao api: promotionmisc_activity_range_add '
                    raise  # raise the most recent exception
                else:
                    is_poped = True
                    self.assertRaises(inputdata['exceptionClass'])
            finally:
                self.assertEqual(inputdata['popException'], is_poped, 'assert exceptions')

    def tearDown(self):
        pass
    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == "__main__":
    unittest.main()

alltests = unittest.TestLoader().loadTestsFromTestCase( TestPromotionmiscActivityRangeListGet )


