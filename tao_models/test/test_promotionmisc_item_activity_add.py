#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: tanglingling
@contact: tanglingling@maimiaotech.com
@date: 2015-03-27 14:26
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
from tao_models.common.exceptions import TaoApiMaxRetryException
from TaobaoSdk.Exceptions import ErrorResponseException

from promotionmisc_item_activity_add import PromotionmiscItemActivityAdd #导入测试类
import datetime

@unittest.skipUnless('regression' in settings.RUNTYPE, "Regression Test Case")
class TestPromotionmiscItemActivityAdd(unittest.TestCase):
    '''
    创建无条件单品优惠活动。
    1,可以选择是全店参加或者部分商品参加：participate_range：0表示全部参与； 1表示部分商品参与。
    2,如果是部分商品参加，则需要通过taobao.promotionmisc.activity.range.add接口来指定需要参加的商品。
    3,该接口创建的优惠受店铺最低折扣限制，如优惠不生效，请让卖家检查该优惠是否低于店铺的最低折扣设置。
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

        cls.testInputData = [{'nick':'chinchinstyle','name':'run_Case创建','participate_range':0, 'start_time':dnow, 'end_time':dafter,'decrease_amount':None, 'discount_rate':900,'popException':False,'exceptionClass':None},
                             {'nick':'','name':'run_Case创建','participate_range':0, 'start_time':dnow, 'end_time':dafter,'decrease_amount':None, 'discount_rate':900,'popException':True,'exceptionClass':W2securityException},# nick invalid
                             {'nick':'chinchinstyle','name':'','participate_range':0, 'start_time':dnow, 'end_time':dafter,'decrease_amount':None, 'discount_rate':900,'popException':True,'exceptionClass':ErrorResponseException},# name is none 
                             {'nick':'chinchinstyle','name':'run_Case创建','participate_range':0, 'start_time':old_time1, 'end_time':old_time2,'decrease_amount':None, 'discount_rate':900,'popException':True,'exceptionClass':ErrorResponseException},# start_time & end_time invalid
                             ]
    def setUp(self):
        pass 
    def test_add_promotionm_item_activity(self):
        for inputdata in self.testInputData:
            is_poped = False
            try:
                # 新增1个促销活动 返回id
                res = PromotionmiscItemActivityAdd.add_promotionm_item_activity(inputdata['nick'],inputdata['name'],inputdata['participate_range'],inputdata['start_time'],inputdata['end_time'],inputdata['decrease_amount'],inputdata['discount_rate'])
                self.assertEquals(type(res),int,'return type is error!')
            except Exception, e:
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

alltests = unittest.TestLoader().loadTestsFromTestCase(TestPromotionmiscItemActivityAdd)

