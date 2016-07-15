#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: luxiaowen
@contact: luxiaowen@maimiaotech.com
@date: 2015-04-10 13:58
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
from tao_models.simba_insight_catsforecastnew_get import SimbaInsightCatsforecastnewGet 
from TaobaoSdk.Exceptions import ErrorResponseException
#from tao_models.common.exceptions import InvalidAccessTokenException

class test_simba_insight_catsforecastnew_get(unittest.TestCase):
    #maxDiff = None
    @classmethod
    def setUpClass(cls):
        pass
    
    def setUp(self):
        pass
    
    def test_get_words_forecast_cats(self):
        '''
        获取词的相关类目预测数据
        '''
        data = [{'words_list':[u'连衣裙'],
                 'expect_result':[{"bidword":"连衣裙",
                                   "cat_path_id":"16 50010850",
                                   "cat_path_name":"女装\/女士精品 > 连衣裙",
                                   "score":"1"}]},
                #{'words_list':[],
                # 'expect_result':{'code':40,'msg':'Missing required arguments:bidword_list'}},
                {'words_list':[u'asskfhksahfash'],
                 'expect_result':[{"bidword":"asskfhksahfash",
                                   "cat_path_id":"",
                                   "cat_path_name":"",
                                   "score":""}]}
                ]
               # {'cat_id_list':[5.1111582],'start_date_offset':8,'end_date_offset':1,
               #  'expect_result':{'code':15,'msg':'Remote service error','sub_code':'isv.invalid-parameter','sub_msg':'类目id错误！'}}]
        for item in data:
            words_list = item['words_list']
            expect_result = item['expect_result']
            try:
                actual_result = SimbaInsightCatsforecastnewGet.get_words_forecast_cats(words_list)
                self.assertEqual(type(actual_result),list)
                bb = expect_result[0].keys()
                bb.sort()
                for index in range(len(actual_result)):
                    aa = actual_result[index].keys()
                    aa.sort()
                    self.assertEqual(aa,bb)
                    self.assertEqual(type(actual_result[index]),dict)
                    self.assertEqual(actual_result[index]['bidword'],expect_result[0]['bidword'])
            except ErrorResponseException,e:
                self.assertEqual(e.code,expect_result['code'])
                self.assertEqual(e.msg,expect_result['msg'])

    def tearDown(self):
        pass
    
    @classmethod
    def tearDownClass(cls):
        pass
if __name__ == "__main__":
    unittest.main()
alltests = unittest.TestLoader().loadTestsFromTestCase(test_simba_insight_catsforecastnew_get)
