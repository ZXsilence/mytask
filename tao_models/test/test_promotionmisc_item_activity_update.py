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
from  promotionmisc_item_activity_add import PromotionmiscItemActivityAdd #增加1个促销活动
from promotionmisc_item_activity_update import PromotionmiscItemActivityUpdate # update优惠活动
from tao_models.common.exceptions import W2securityException, InvalidAccessTokenException#导入异常类
from tao_models.common.exceptions import TaoApiMaxRetryException
from TaobaoSdk.Exceptions import ErrorResponseException
from promotionmisc_item_activity_delete import PromotionmiscItemActivityDelete 
from promotionmisc_item_activity_update import PromotionmiscItemActivityUpdate #导入测试类
import datetime

@unittest.skipUnless('regression' in settings.RUNTYPE, "Regression Test Case")
class TestPromotionmiscItemActivityUpdate(unittest.TestCase):
    '''
    修改无条件单品优惠活动。
    '''
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

        cls.testInputData2 = {'nick':'chinchinstyle','name':'tstOldName','participate_range':0, 'start_time':dnow, 'end_time':dafter,'decrease_amount':None, 'discount_rate':900}

        cls.testInputData = [{'nick':'chinchinstyle','activity_id':-1,'name':'tstNewName','participate_range':0,'start_time':dnow,'end_time':dafter,'decrease_amount':None,'discount_rate':800,'popException':False,'exceptionClass':None},# normal_test
                             {'nick':'chinchinstyle','activity_id':0,'name':'tstNewName','participate_range':0,'start_time':dnow,'end_time':dafter,'decrease_amount':None,'discount_rate':800,'popException':True,'exceptionClass':ErrorResponseException},# activity_id is 0
                             {'nick':'chinchinstyle','activity_id':-1,'name':'','participate_range':0,'start_time':dnow,'end_time':dafter,'decrease_amount':None,'discount_rate':800,'popException':True,'exceptionClass':ErrorResponseException},# name is ''
                             {'nick':'chinchinstyle','activity_id':-1,'name':'tstNewName','participate_range':1,'start_time':old_time1,'end_time':old_time2,'decrease_amount':None,'discount_rate':800,'popException':True,'exceptionClass':ErrorResponseException},#start_time<end_time<now 
                             {'nick':'','activity_id':-1,'name':'tstNewName','participate_range':0,'start_time':dnow,'end_time':dafter,'popException':True,'exceptionClass':W2securityException},#nick is ''
                             {'nick':'_nick_not_exists_','activity_id':-1,'name':'tstNewName','participate_range':0,'start_time':dnow,'end_time':dafter,'popException':True,'exceptionClass':InvalidAccessTokenException},#nick is invalid
                             ]

    def setUp(self):
        pass 
    """
    def test_update_item_activity(self):
        for inputdata in self.testInputData:
            is_poped = False
            try:
                if -1==inputdata['activity_id']:
                    # 新增1个促销活动 返回id
                    activity_id = PromotionmiscItemActivityAdd.add_promotionm_item_activity(self.testInputData2['nick'],self.testInputData2['name'],self.testInputData2['participate_range'],self.testInputData2['start_time'],self.testInputData2['end_time'],self.testInputData2['decrease_amount'],self.testInputData2['discount_rate'])
                    self.assertEquals(type(activity_id),int,'return type is error!')
                    inputdata['activity_id'] = activity_id
                # 修改这个促销活动的内容
                res_boolean = PromotionmiscItemActivityUpdate.update_item_activity(inputdata['nick'],inputdata['activity_id'],inputdata['name'],inputdata['participate_range'],inputdata['start_time'],inputdata['end_time'],inputdata['decrease_amount'],inputdata['discount_rate'])
                self.assertEqual(type(res_boolean),bool, 'assert return type error!')
                self.assertTrue(res_boolean,'assert return value error!')

                # 删除这个促销活动
                res = PromotionmiscItemActivityDelete.delete_item_activity(inputdata['nick'],inputdata['activity_id'])
                self.assertTrue(res.isSuccess(),'assert return value error!')
            except Exception, e:
                is_poped = True
                self.assertRaises(inputdata['exceptionClass'])
            finally:
                self.assertEqual(inputdata['popException'], is_poped, 'assert exceptions')
    """

    def test_close_item_activity(self):
        for inputdata in self.testInputData:
            is_poped = False
            try:
                if -1==inputdata['activity_id']:
                    # 新增1个促销活动 返回id
                    activity_id = PromotionmiscItemActivityAdd.add_promotionm_item_activity(self.testInputData2['nick'],self.testInputData2['name'],self.testInputData2['participate_range'],self.testInputData2['start_time'],self.testInputData2['end_time'],self.testInputData2['decrease_amount'],self.testInputData2['discount_rate'])
                    self.assertEquals(type(activity_id),int,'return type is error!')
                    inputdata['activity_id'] = activity_id
                # 关闭这个促销活动的内容
                res_boolean = PromotionmiscItemActivityUpdate.update_item_activity(inputdata['nick'],inputdata['activity_id'],inputdata['name'],inputdata['participate_range'],inputdata['start_time'],inputdata['end_time'],inputdata['decrease_amount'],inputdata['discount_rate'])
                self.assertEqual(type(res_boolean),bool, 'assert return type error!')
                self.assertTrue(res_boolean,'assert return value error!')

                # 删除这个促销活动
                res = PromotionmiscItemActivityDelete.delete_item_activity(inputdata['nick'],inputdata['activity_id'])
                self.assertTrue(res.isSuccess(),'assert return value error!')
            except Exception, e:
                is_poped = True
                self.assertRaises(inputdata['exceptionClass'])
            finally:
                self.assertEqual(inputdata['popException'], is_poped , 'assert exceptions')
    
    def tearDown(self):
        pass
    
    @classmethod
    def tearDownClass(cls):
        pass
if __name__ == "__main__":
    unittest.main()

alltests = unittest.TestLoader().loadTestsFromTestCase(TestPromotionmiscItemActivityUpdate)
