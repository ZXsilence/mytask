#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: tanglingling
@contact: tanglingling@maimiaotech.com
@date: 2015-04-08 14:33
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

from topats_task_delete import TopatsTaskDelete
from topats_simba_campkeywordbase_get import TopatsSimbaCampkeywordbaseGet
from topats_result_get import TopatsResultGet
from topats_simba_campkeywordeffect_get import TopatsSimbaCampkeywordeffectGet


@unittest.skipUnless('regression' in settings.RUNTYPE, "Regression Test Case")
class TestTopatsTask4APIs(unittest.TestCase):
    '''
    可用于取消已经创建的异步任务。 条件限制： 1)一次只可以取消一个任务 2）只能取消自己创建的任务
    '''
    @classmethod
    def setUpClass(cls):
        set_api_source('SDK_TEST')
        cls.testData = [{'nick':'chinchinstyle','soft_code':'SYB','campaign_id':3367748,'time_slot':'7DAY','popException':False,'exceptClass':None},
                        #{'nick':'','soft_code':'SYB','campaign_id':3367748,'time_slot':'7DAY','popException':True,'exceptClass':TaoApiMaxRetryException}, # nick is none , result_get throw exception
                        {'nick':'chinchinstyle','soft_code':'','campaign_id':3367748,'time_slot':'7DAY','popException':False,'exceptClass':None}, # soft_code is none 
                        {'nick':'chinchinstyle','soft_code':'SYB','campaign_id':3367748,'time_slot':'','popException':True,'exceptClass':ErrorResponseException}, # time_slot is none, effect_get throw exception
                        ]

        cls.errs = {'task_delete':'error find in API: topats_task_delete',
                      'base_get':'error find in API: topats_simba_campkeywordbase_get',
                      'effect_get':'error find in API: topats_simba_campkeywordeffect_get',
                      'result_get':'error find in API: topats_result_get',
                      'assert_error':'assert exception',
                      }
    
    def seUp(self):
        pass
    def test_topat_apis(self):
        for inputdata in self.testData:
            is_popped = False
            try:
                # test topats_simba_campkeywordeffect_get
                task_id = TopatsSimbaCampkeywordeffectGet.get_camp_keywordeffect_task(inputdata['nick'], inputdata['campaign_id'], inputdata['time_slot'], inputdata['soft_code'])
                self.assertEqual( type(task_id), int , self.errs['effect_get'])
                self.assertGreater(task_id,0,self.errs['effect_get'])

                #topats_simba_campkeywordbase_get
                task_id2 = TopatsSimbaCampkeywordbaseGet.get_camp_keywordbase_task(inputdata['nick'], inputdata ['campaign_id'], inputdata['time_slot'], inputdata['soft_code'])
                self.assertEqual(  type(task_id2) , int , self.errs['base_get'])
                self.assertGreater(task_id2, 0 , self.errs['base_get'])

                # test topats_result_get  
                res = TopatsResultGet.get_task_result(task_id,inputdata['soft_code'],inputdata['nick'])
                self.assertEqual( type(res) , dict , self.errs['result_get'])
                self.assertEqual(res['task_id'], task_id, self.errs['result_get'])

                # test topats_task_delete
                TopatsTaskDelete.delete_task(task_id,inputdata['nick'],inputdata['soft_code'])
                TopatsTaskDelete.delete_task(task_id2,inputdata['nick'],inputdata['soft_code'])

            except Exception, e:
                is_popped = True
                self.assertRaises(inputdata['exceptClass'])
            finally:
                self.assertEqual(is_popped,inputdata['popException'],self.errs['assert_error'])


    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == '__main__':
    unittest.main()

alltests = unittest.TestLoader().loadTestsFromTestCase(TestTopatsTask4APIs)
