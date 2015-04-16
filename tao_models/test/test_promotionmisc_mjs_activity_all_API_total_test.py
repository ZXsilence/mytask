#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: tanglingling
@contact: tanglingling@maimiaotech.com
@date: 2015-03-31 14:03
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
from tao_models.common.exceptions import W2securityException, InvalidAccessTokenException#导入异常类
from tao_models.common.exceptions import TaoApiMaxRetryException
from TaobaoSdk.Exceptions import ErrorResponseException
from TaobaoSdk import PromotionmiscMjsActivityDeleteResponse

from promotionmisc_mjs_activity_add import PromotionmiscMjsActivityAdd #创建满就送促销活动
from promotionmisc_mjs_activity_delete import PromotionmiscMjsActivityDelete #删除满就送活动
from promotionmisc_mjs_activity_get import PromotionmiscMjsActivityGet #获得1个活动
from promotionmisc_mjs_activity_list_get import PromotionmiscMjsActivityListGet #活动列表
from promotionmisc_mjs_activity_update import PromotionmiscMjsActivityUpdate #更新活动

@unittest.skipUnless('regression' in settings.RUNTYPE, "Regression Test Case")
class TestPromotionmiscMjsActivity_All_API(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        set_api_source('SDK_TEST')
        dnow = datetime.datetime.now()
        _10day = datetime.timedelta(days=10)
        now_add_10day =  dnow + _10day
        dafter = datetime.datetime(now_add_10day.year,now_add_10day.month,now_add_10day.day,0,0,0)
        dnow = dnow.strftime("%Y-%m-%d %H:%M:%S")
        dafter = dafter.strftime("%Y-%m-%d %H:%M:%S")

        old_time1 = '2013-03-27 00:00:00'
        old_time2 = '2013-05-27 00:00:00'

        cls.testInputdata_add = [{'nick':'chinchinstyle','name':'tstName','participate_range':1,'start_time':dnow,'end_time':dafter,'decrease_amount':None,'discount_rate':900,'popException':False,'exceptionClass':None},
                                 {'nick':'','name':'tstName','participate_range':1,'start_time':dnow,'end_time':dafter,'decrease_amount':None,'discount_rate':900,'popException':True,'exceptionClass':W2securityException},
                                 {'nick':'_nick_not_exists_','name':'tstName','participate_range':1,'start_time':dnow,'end_time':dafter,'decrease_amount':None,'discount_rate':900,'popException':True,'exceptionClass':InvalidAccessTokenException},
                             ]
        cls.errs = {'add_error':'Error find in API: promotionmisc_mjs_activity_add',
                    'get_error':'Error find in API: promotionmisc_mjs_activity_get',
                    'get_list_error':'Error find in API: promotionmisc_mjs_activity_list_get',
                    'update_error':'Error find in API: promotionmisc_mjs_activity_delete',
                    'delete_error':'Error find in API: promotionmisc_mjs_activity_delete',
                    'raise':'assert_raise meetes error',
                    'finally':'finally assert meetes error',
                    }

    def test_promotionmisc_mjs_activity_all_api(self):
        for inputdata in self.testInputdata_add:
            is_poped = False
            try:
                # 测试接口 promotionmisc_mjs_activity_list_get 获取活动列表
                activity_list = PromotionmiscMjsActivityListGet.get_mjs_promotion_list(inputdata['nick'])
                self.assertEqual(type(activity_list), list , self.errs['get_list_error'])
                len_1 = len(activity_list)

                # 测试接口：promotionmisc_mjs_activity_add新增1个促销活动
                factory = PromotionmiscMjsActivityAdd.MjsPromotionActivityFactory.create_mjs_promotion_add()
                factory.add_mjs_base_condition(inputdata['name'],inputdata['start_time'],inputdata['end_time'],1,1)
                factory.add_mjs_item_condition(1,'true')
                factory.decrease_money_condition(1000)
                factory.add_gift_condition('true','dog-dog')
                req = factory.build_promotion_request()
                activity_id = PromotionmiscMjsActivityAdd.add_promotionm_mjs_activity(inputdata['nick'],req)
                self.assertEqual(type(activity_id), int , self.errs['add_error'])

                # 测试接口:promotionmisc_mjs_activity_get 查看指定id的促销活动明细
                activity= PromotionmiscMjsActivityGet.get_promotionm_mjs_activity(inputdata['nick'],activity_id)
                self.assertEqual(type(activity), dict, self.errs['get_error'])
                self.assertEqual(activity['activity_id'], activity_id,self.errs['get_error'])

                # 测试接口：promotionmisc_mjs_activity_update 修改某促销活动
                factory = PromotionmiscMjsActivityUpdate.MjsPromotionActivityFactory.create_mjs_promotion_update()
                factory.add_mjs_base_condition(activity_id,inputdata['name'],inputdata['start_time'],inputdata['end_time'],inputdata['participate_range'],1)
                factory.add_mjs_item_condition(1,'true')
                factory.decrease_money_condition(1000)
                factory.add_gift_condition('true','小狗狗')
                req = factory.build_promotion_request()
                res_bool = PromotionmiscMjsActivityUpdate.update_promotionm_mjs_activity(inputdata['nick'],req)
                self.assertEqual(type(res_bool), bool , self.errs['update_error'])
                self.assertTrue(res_bool,self.errs['update_error'])

                # 测试接口:promotionmisc_mjs_activity_list_get获取活动列表
                activity_list = PromotionmiscMjsActivityListGet.get_mjs_promotion_list(inputdata['nick'])
                self.assertEqual(type(activity_list), list, self.errs['get_list_error'])
                len_2 = len(activity_list)
                self.assertEqual(len_1+1 , len_2, self.errs['get_list_error'])

                #测试接口:promotionmisc_mjs_activity_delete删除活动
                obj = PromotionmiscMjsActivityDelete.delete_mjs_activity(inputdata['nick'],activity_id)
                self.assertEqual(type(obj), PromotionmiscMjsActivityDeleteResponse,self.errs['delete_error'])
                self.assertTrue(obj.isSuccess(),self.errs['delete_error'])

            except Exception, e:
                is_poped = True
                self.assertRaises(inputdata['exceptionClass'])
            finally:
                self.assertEqual(inputdata['popException'],is_poped,self.errs['finally'])

    def setUp(self):
        pass 
    def tearDown(self):
        pass
    @classmethod
    def tearDownClass(cls):
        pass
if __name__ == "__main__":
    unittest.main()

alltests = unittest.TestLoader().loadTestsFromTestCase(TestPromotionmiscMjsActivity_All_API)
