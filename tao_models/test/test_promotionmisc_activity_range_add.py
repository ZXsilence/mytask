#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: tanglingling
@contact: tanglingling@maimiaotech.com
@date: 2015-03-26 11:36
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
from tao_models.common.exceptions import W2securityException, InvalidAccessTokenException#导入异常类

@unittest.skipUnless('regression' in settings.RUNTYPE, "Regression Test Case")
class TestPromotionmiscActivityRangeAdd(unittest.TestCase):
    '''
    增加活动参与的商品，部分商品参与的活动，最大支持指定150个商品。
    '''
    @classmethod
    def setUpClass(cls):
        set_api_source('SDK_TEST')
        cls.tcinfo = 'API Test - taobao.PromotionmiscActivityRangeAdd'
        cls.testInputDatas_add = [{'nick':'chinchinstyle','soft_code':'SYB','activity_id':654062470,'num_iid_list': [7794896442],'popException':False, 'exceptionClass':None},
                                  {'nick':'chinchinstyle','soft_code':'SYB','activity_id':0,'num_iid_list': [7794896442],'popException':True, 'exceptionClass':W2securityException}, #activty_id not exists
                                  {'nick':'chinchinstyle','soft_code':'SYB','activity_id':654062470,'num_iid_list':[123],'popException':True, 'exceptionClass':W2securityException}, #num_id not exists
                                  {'nick':'','soft_code':'SYB','activity_id':654062470,'num_iid_list':[7794896442],'popException':True, 'exceptionClass':W2securityException}, #nick is None
                                  {'nick':'_nick_not_exists_','soft_code':'SYB','activity_id':654062470,'num_iid_list':[7794896442],'popException':True, 'exceptionClass':InvalidAccessTokenException}, # nick is not invalid/未认证
                                  ]
        
    def setUp(self):
        pass

    def test_add_promotionm_activity_items(self):
        for inputdata in self.testInputDatas_add:
            is_poped = False
            try:
                #商品数目+1
                res = PromotionmiscActivityRangeRemove.remove_promotionm_activity_range(inputdata['nick'],inputdata['activity_id'],inputdata['num_iid_list'])
                self.assertEqual(res,True,'assert remove_item')

                goods_list = PromotionmiscActivityRangeListGet.get_promotionm_activity_range(inputdata['nick'],inputdata['activity_id'])
                before_len = len(goods_list)

                PromotionmiscActivityRangeAdd.add_promotionm_activity_items(inputdata['nick'],inputdata['activity_id'],inputdata['num_iid_list'],inputdata['soft_code'])
                goods_list=  PromotionmiscActivityRangeListGet.get_promotionm_activity_range(inputdata['nick'],inputdata['activity_id'])
                after_len = len(goods_list)
                self.assertEqual(after_len,before_len+1,"after_len doesnot equals before_len+1")
            except Exception, e:
                is_poped = True
                self.assertRaises(inputdata['exceptionClass'])
            finally:
                self.assertEqual(inputdata['popException'],is_poped,"assert exception")

    
    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == '__main__':                                                       
    unittest.main()

alltests = unittest.TestLoader().loadTestsFromTestCase(TestPromotionmiscActivityRangeAdd)
