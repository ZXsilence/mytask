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
        cls.testData = [
                        {'nick':'chinchinstyle','soft_code':'SYB','campaign_id':3367748,'time_slot':'7DAY', # normal case, goes well
                                    'effect_get_except':{'popException':False,'exceptClass':None},
                                    'base_get_except':{'popException':False,'exceptClass':None},
                                    'result_get_except':{'popException':False,'exceptClass':None},
                                    'delete_task_except':{'popException':False,'exceptClass':None},'case':1},
                        {'nick':'','soft_code':'SYB','campaign_id':3367748,'time_slot':'7DAY',
                                    'effect_get_except':{'popException':False,'exceptClass':None},
                                    'base_get_except':{'popException':False,'exceptClass':None},
                                    'result_get_except':{'popException':True,'exceptClass':TaoApiMaxRetryException},  # nick is None, result_get got exception
                                    'delete_task_except':{'popException':False,'exceptClass':None},'case':2},
                        {'nick':'chinchinstyle','soft_code':'','campaign_id':3367748,'time_slot':'7DAY', #soft_code is None, everything is ok
                                    'effect_get_except':{'popException':False,'exceptClass':None},
                                    'base_get_except':{'popException':False,'exceptClass':None},
                                    'result_get_except':{'popException':False,'exceptClass':None},
                                    'delete_task_except':{'popException':False,'exceptClass':None},'case':3},
                        {'nick':'chinchinstyle','soft_code':'SYB','campaign_id':0,'time_slot':'7DAY', #campaign_id=0 , everything is ok
                                    'effect_get_except':{'popException':False,'exceptClass':None},
                                    'base_get_except':{'popException':False,'exceptClass':None},
                                    'result_get_except':{'popException':False,'exceptClass':None},
                                    'delete_task_except':{'popException':False,'exceptClass':None},'case':4},
                        #{'nick':'chinchinstyle','soft_code':'SYB','campaign_id':3367748,'time_slot':'', #time_slot is None, effect_get got exception;   cost time!!,so comment out
                        #            'effect_get_except':{'popException':False,'exceptClass':None},
                        #            'base_get_except':{'popException':False,'exceptClass':None},
                        #            'result_get_except':{'popException':True,'exceptClass':TaoApiMaxRetryException},
                        #            'delete_task_except':{'popException':False,'exceptClass':None},'case':5},
                        ]
        cls.assertKeys=['status', 'method', 'task_id', 'created']
    def seUp(self):
        pass
    def test_topat_apis(self):
        for inputdata in self.testData:
            task_id_list=[]
            try:
                # test topats_simba_campkeywordeffect_get
                task_id = TopatsSimbaCampkeywordeffectGet.get_camp_keywordeffect_task(inputdata['nick'], inputdata['campaign_id'], inputdata['time_slot'], inputdata['soft_code'])
                task_id_list.append(task_id)
                self.assertEqual( type(task_id), int )
                self.assertGreater(task_id,0)
                
                #topats_simba_campkeywordbase_get
                task_id2 = TopatsSimbaCampkeywordbaseGet.get_camp_keywordbase_task(inputdata['nick'], inputdata ['campaign_id'], inputdata['time_slot'], inputdata['soft_code'])
                task_id_list.append(task_id2)
                self.assertEqual(  type(task_id2) , int)
                self.assertGreater(task_id2, 0)
                
                # test topats_result_get  
                res = TopatsResultGet.get_task_result(task_id,inputdata['soft_code'],inputdata['nick'])
                self.assertEqual( type(res) , dict )
                self.assertEqual(res['task_id'], task_id)
                self.assertEqual(sorted(res.keys()),sorted(self.assertKeys))
                
            except TaoApiMaxRetryException , e :
                if inputdata['case'] not in [2,5]:
                    import traceback;traceback.print_exc()
                    raise e
                else:
                    pass
            except Exception ,e :
                if inputdata['effect_get_except']['popException']==False \
                        or inputdata['base_get_except']['popException'] == False \
                        or inputdata['result_get_except']['popException'] == False\
                        or inputdata['delete_task_except']['popException'] == False:
                    import traceback; traceback.print_exc()
                    raise e
                else:
                    pass
            finally:
                # test topats_task_delete
                for task_id in task_id_list:
                    TopatsTaskDelete.delete_task(task_id,inputdata['nick'],inputdata['soft_code'])

    @classmethod
    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == '__main__':
    unittest.main()

alltests = unittest.TestLoader().loadTestsFromTestCase(TestTopatsTask4APIs)
