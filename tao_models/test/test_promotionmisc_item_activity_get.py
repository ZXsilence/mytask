#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: tanglingling
@contact: tanglingling@maimiaotech.com
@date: 2015-03-30 11:10
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""
import sys,datetime
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

from promotionmisc_item_activity_add import PromotionmiscItemActivityAdd #增加1个促销活动
from promotionmisc_item_activity_delete import PromotionmiscItemActivityDelete # 删除1个促销活动
from TaobaoSdk import PromotionmiscItemActivityDeleteResponse # 导入返回类型类
from tao_models.common.exceptions import W2securityException, InvalidAccessTokenException#导入异常类
from promotionmisc_item_activity_get import PromotionmiscItemActivityGet
from TaobaoSdk.Exceptions import ErrorResponseException #导入异常类

@unittest.skipUnless('regression' in settings.RUNTYPE, "Regression Test Case")
class TestPromotionmiscItemActivityDelete(unittest.TestCase):
    '''
    查询无条件单品优惠活动
    '''
    @classmethod
    def setUpClass(cls):
        set_api_source('SDK_TEST')
        cls.testInputData = [{'nick':'chinchinstyle','activity_id':-1,'soft_code':'SYB','popException':False,'exceptionClass':None},#normal
                             {'nick':'','activity_id':-1,'soft_code':'SYB','popException':True,'exceptionClass':ErrorResponseException},#nick is none 
                             {'nick':'_nick_not_exists_','activity_id':-1,'soft_code':'SYB','popException':True,'exceptionClass':InvalidAccessTokenException},#nick invalid
                             {'nick':'chinchinstyle','activity_id':0,'soft_code':'SYB','popException':True,'exceptionClass':ErrorResponseException}, # activity_id is 0
                             {'nick':'chinchinstyle','activity_id':-1,'soft_code':'ZZ','popException':True,'exceptionClass':InvalidAccessTokenException}, # soft_code invalid
                             ]

        dnow = datetime.datetime.now()
        _10day = datetime.timedelta(days=10)
        now_add_10day =  dnow + _10day
        dafter = datetime.datetime(now_add_10day.year,now_add_10day.month,now_add_10day.day,0,0,0)
        dnow = dnow.strftime("%Y-%m-%d %H:%M:%S")
        dafter = dafter.strftime("%Y-%m-%d %H:%M:%S")

        cls.testInputData2 = {'nick':'chinchinstyle','name': 'run_Case创建','participate_range':0, 'start_time':dnow, 'end_time':dafter,'decrease_amount':None, 'discount_rate':900}

    def setUp(self):
        pass
    def test_PromotionmiscItemActivityDelete(self):
        for inputdata in self.testInputData:
            is_poped = False
            try:
                # add an activity
                if -1 == inputdata['activity_id']:
                    res = PromotionmiscItemActivityAdd.add_promotionm_item_activity(self.testInputData2['nick'],self.testInputData2['name'],self.testInputData2['participate_range'],self.testInputData2['start_time'],self.testInputData2['end_time'],self.testInputData2['decrease_amount'],self.testInputData2['discount_rate'])
                    self.assertEquals(type(res),int , 'reteurn type is error !')
                    print 'The activity_id to delete is:', res
                    inputdata['activity_id'] = res
                # search the activity, the checkpoint !!
                res = PromotionmiscItemActivityGet.get_promotionm_item_activity(inputdata['nick'],inputdata['activity_id'],inputdata['soft_code'])
                self.assertEqual(type(res), dict, 'assert return type error!')
                self.assertEqual(res['activity_id'], inputdata['activity_id'],'assert gete wrong activity_id!')
                # delete the activity
                res =  PromotionmiscItemActivityDelete.delete_item_activity(self.testInputData2['nick'],inputdata['activity_id'],inputdata['soft_code'])
                self.assertTrue(isinstance(res,PromotionmiscItemActivityDeleteResponse),'assert return Class type is error!')
                self.assertTrue(res.isSuccess(),'assert return Value is Error')
            except Exception, e:
                is_poped = True 
                self.assertRaises(inputdata['exceptionClass'])
            finally:
                self.assertEquals(inputdata['popException'], is_poped, 'assert exception')

    def tearDown(self):
        pass 
    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == '__main__':                                                       
    unittest.main()
alltests = unittest.TestLoader().loadTestsFromTestCase(TestPromotionmiscItemActivityDelete)
