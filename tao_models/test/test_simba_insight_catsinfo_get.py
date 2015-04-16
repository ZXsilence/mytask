#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: luxiaowen
@contact: luxiaowen@maimiaotech.com
@date: 2015-04-10 11:27
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""

import sys
import os
if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../../../comm_lib/'))
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('normal_test')

import unittest
import datetime
from tao_models.simba_insight_catsinfo_get import SimbaInsightCatsinfoGet 
from TaobaoSdk.Exceptions import ErrorResponseException
#from tao_models.common.exceptions import InvalidAccessTokenException

class test_simba_insight_catsinfo_get(unittest.TestCase):
    maxDiff = None
    @classmethod
    def setUpClass(cls):
        pass
    
    def setUp(self):
        pass
    
    def test_get_cats_info(self):
        '''
        0表示请求所有顶级类目的信息，这时可以忽略第二个参数，1表示获取给定的类目id的详细信息，2表示获取给定类目id的所有子类目的详细信息
        '''
        data = [{'cat_id_list':[50023582], 'type':1,
                 'expect_result':[{'parent_cat_id': 50012374, 
                                   'cat_name': '防辐射卡', 
                                   'cat_path_name': '孕妇装/孕产妇用品/营养防辐射防辐射卡', 
                                   'cat_level': 3, 
                                   'cat_id': 50023582, 
                                   'last_sync_time': datetime.datetime(2011, 5, 19, 16, 26, 25), 
                                   'cat_path_id': '50022517 50012374 50023582'}]},
                {'cat_id_list':[50023582],'type':2,
                 'expect_result':[]},
                {'cat_id_list':[50012374],'type':2,
                 'expect_result':[{'parent_cat_id': 50012374, 
                                   'cat_name': '防辐射卡', 
                                   'cat_path_name': '孕妇装/孕产妇用品/营养防辐射防辐射卡', 
                                   'cat_level': 3, 
                                   'cat_id': 50023582, 
                                   'last_sync_time': datetime.datetime(2011, 5, 19, 16, 26, 25), 
                                   'cat_path_id': '50022517 50012374 50023582'}]} ,
                {'cat_id_list':[1.2],'type':1,
                 'expect_result':[]},
                {'cat_id_list':[1.2],'type':2,
                 'expect_result':[]},
                {'cat_id_list':[1.2],'type':0,
                 'expect_result':[{'parent_cat_id': 0, 
                                   'cat_name': '无线生活服务', 
                                   'cat_path_name': '无线生活服务', 
                                   'cat_level': 1, 
                                   'cat_id': 50690010, 
                                   'last_sync_time': datetime.datetime(2013, 8, 19, 8, 0, 9), 
                                   'cat_path_id': '50690010'}]}
                ]
               # {'cat_id_list':[5.1111582],'start_date_offset':8,'end_date_offset':1,
               #  'expect_result':{'code':15,'msg':'Remote service error','sub_code':'isv.invalid-parameter','sub_msg':'类目id错误！'}}]
        for item in data:
            cat_id_list = item['cat_id_list']
            t_type =  item['type']
            expect_result = item['expect_result']
            try:
                actual_result = SimbaInsightCatsinfoGet.get_cats_info(t_type,cat_id_list)
                self.assertEqual(type(actual_result),list)
                if len(actual_result)==0:
                    self.assertEqual(actual_result,expect_result)
                    continue
                if t_type == 1:
                    for index in range(len(actual_result)):
                        self.assertEqual(type(actual_result[index]),dict)
                        self.assertEqual(actual_result[index]['cat_id'],expect_result[index]['cat_id'])
                        self.assertEqual(actual_result[index].keys().sort(),expect_result[index].keys().sort())
                elif t_type==2:
                    for index in range(len(actual_result)):
                        self.assertEqual(type(actual_result[index]),dict)
                        self.assertEqual(actual_result[index]['parent_cat_id'],expect_result[0]['parent_cat_id'])
                        self.assertEqual(actual_result[index].keys().sort(),expect_result[0].keys().sort())
                elif t_type==0:
                    for index in range(len(actual_result)):
                        self.assertEqual(type(actual_result[index]),dict)
                        self.assertEqual(actual_result[index]['parent_cat_id'],expect_result[0]['parent_cat_id'])
                        self.assertEqual(actual_result[index]['cat_level'],expect_result[0]['cat_level'])
                        self.assertEqual(actual_result[index].keys().sort(),expect_result[0].keys().sort())
                    

            except ErrorResponseException,e:
                self.assertEqual(e.code,expect_result['code'])
                self.assertEqual(e.msg,expect_result['msg'])
                self.assertEqual(e.sub_code,expect_result['sub_code'])

    
    def tearDown(self):
        pass
    
    @classmethod
    def tearDownClass(cls):
        pass
if __name__ == "__main__":
    unittest.main()
alltests = unittest.TestLoader().loadTestsFromTestCase(test_simba_insight_catsinfo_get)
