#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: tanglingling
@contact: tanglingling@maimiaotech.com
@date: 2015-03-30 12:47
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

from promotionmisc_item_activity_delete import PromotionmiscItemActivityDelete # 删除1个促销活动
from promotionmisc_item_activity_add import PromotionmiscItemActivityAdd #增加1个促销活动
from promotionmisc_item_activity_list_get import PromotionmiscItemActivityListGet #获取促销活动列表
from TaobaoSdk import PromotionmiscItemActivityDeleteResponse # 导入返回类型类
from tao_models.common.exceptions import W2securityException, InvalidAccessTokenException#导入异常类
from tao_models.common.exceptions import TaoApiMaxRetryException
from TaobaoSdk.Exceptions import ErrorResponseException
import datetime

@unittest.skipUnless('regression' in settings.RUNTYPE, "Regression Test Case")
class TestPromotionmiscItemActivityListGet(unittest.TestCase):
    '''
    查询无条件单品优惠活动列表
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

        cls.testInputData = [{'nick':'chinchinstyle','soft_code':'SYB','popException':False,'exceptionClass':None},
                             {'nick':'','soft_code':'SYB','popException':False,'exceptionClass':None},# nick is none 这里返回0未抛出异常
                             {'nick':'_nick_is_not_exists_','soft_code':'SYB','popException':True,'exceptionClass':InvalidAccessTokenException},# nick is not authorized
                             {'nick':'chinchinstyle','soft_code':'ZZ','popException':True,'exceptionClass':InvalidAccessTokenException},# soft_code is not recognized
                             ]
    
        cls.testInputData2 = {'nick':'chinchinstyle','name':'run_Case','participate_range':1, 'start_time':dnow, 'end_time':dafter,'decrease_amount':None, 'discount_rate':900,'popException':False,'exceptionClass':None}
        cls.num_iid = {'num_iid':[7794896442]} # type is: list

    def setUp(self):
        pass 
    def test_add_promotionm_item_activity(self):
        for inputdata in self.testInputData:
            is_poped = False
            try:
                activity_list = PromotionmiscItemActivityListGet.get_item_promotion_list(inputdata['nick'],inputdata['soft_code'])
                self.assertEqual(type(activity_list),list , 'assert return type error!')
                len1 = len(activity_list)

                # 新增1个促销活动 返回id
                activity_id = PromotionmiscItemActivityAdd.add_promotionm_item_activity(self.testInputData2['nick'],self.testInputData2['name'],self.testInputData2['participate_range'],self.testInputData2['start_time'],self.testInputData2['end_time'],self.testInputData2['decrease_amount'],self.testInputData2['discount_rate'])
                print 'activity_id is ',activity_id
                self.assertEquals(type(activity_id),int,'add_promotionm_item_activity:return type is error!')
                
                activity_list = PromotionmiscItemActivityListGet.get_item_promotion_list(inputdata['nick'],inputdata['soft_code'])
                self.assertEqual(type(activity_list),list , 'assert return type error!')
                len2 = len(activity_list)
                if inputdata['nick'] == '':
                    self.assertEqual(len1,len2,'assert return value error!')
                else:
                    self.assertEqual(len2 , len1+1, 'assert return value error!')

                #删除活动
                res = PromotionmiscItemActivityDelete.delete_item_activity(self.testInputData2['nick'],activity_id,self.testInputData[0]['soft_code'])
                self.assertTrue(isinstance(res,PromotionmiscItemActivityDeleteResponse),'assert return Class type error !')
                self.assertTrue(res.isSuccess(),'assert return Value Error')
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

alltests = unittest.TestLoader().loadTestsFromTestCase(TestPromotionmiscItemActivityListGet)

