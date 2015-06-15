#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: luxiaowen
@contact: luxiaowen@maimiaotech.com
@date: 2015-04-13 15:04
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
from tao_models.simba_keyword_rankingforecast_get import SimbaKeywordRankingforecastGet 
from TaobaoSdk.Exceptions import ErrorResponseException
from tao_models.common.exceptions import InvalidAccessTokenException

class test_simba_keyword_rankingforecast_get(unittest.TestCase):
    maxDiff = None
    @classmethod
    def setUpClass(cls):
        pass
    
    def setUp(self):
        pass
    
    def test_get_words_cats_data(self):
        data = [{'nick':'晓迎','keyword_id':213203352285,
                'expect_result':[{'prices': [417, 90, 59, 52, 52, 45, 40, 38, 38, 38, 
                                             38, 36, 36, 34, 33, 32, 29, 29, 29, 29, 
                                             29, 28, 27, 27, 25, 25, 25, 24, 24, 24, 
                                             24, 23, 23, 22, 22, 22, 22, 22, 21, 21, 
                                             21, 21, 21, 21, 21, 21, 20, 20, 20, 20, 
                                             20, 20, 20, 19, 19, 19, 19, 19, 19, 18, 
                                             18, 18, 18, 18, 18, 18, 18, 17, 17, 17, 
                                             17, 17, 17, 17, 17, 17, 17, 17, 17, 16, 
                                             16, 16, 16, 16, 16, 15, 15, 15, 15, 15, 
                                             15, 15, 15, 14, 14, 14, 14, 14, 14, 14], 
                                  'keyword_id': 213203352285, 
                                  'nick': u'\u6653\u8fce'}] } ,
                {'nick':'晓迎','keyword_id':21113203352285,
                'expect_result':{'code':15,'msg':'Remote service error','sub_code':'isv.invalid-parameter','sub_msg':'keyword.not.found'}},
                {'nick':'晓迎1','keyword_id':213203352285,
                 'expect_result':{'exception':'access session expired or invalid'}}]
               # {'cat_id_list':[5.1111582],'start_date_offset':8,'end_date_offset':1,
               #  'expect_result':{'code':15,'msg':'Remote service error','sub_code':'isv.invalid-parameter','sub_msg':'类目id错误！'}}]
        for item in data:
            nick = item['nick']
            keyword_id = item['keyword_id']
            expect_result = item['expect_result']
            try:
                actual_result = SimbaKeywordRankingforecastGet.get_rankingforecast(keyword_id,nick)
                self.assertEqual(type(actual_result),list)
                if len(actual_result)==0:
                    self.assertEqual(actual_result,expect_result)
                    continue
                self.assertEqual(len(actual_result),1)
                self.assertEqual(type(actual_result[0]),dict)
                self.assertEqual(actual_result[0].keys().sort(),expect_result[0].keys().sort())
                self.assertEqual(actual_result[0]['keyword_id'],keyword_id)
                self.assertEqual(actual_result[0]['nick'],nick)
                self.assertEqual(len(actual_result[0]['prices']),100)
                for index in range(100):
                    self.assertEqual(type(actual_result[0]['prices'][index]),int)
                    if index > 0:
                        self.assertLessEqual(actual_result[0]['prices'][index],actual_result[0]['prices'][index-1])
            except InvalidAccessTokenException,e:
                self.assertEqual(e.msg,expect_result['exception'])
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
alltests = unittest.TestLoader().loadTestsFromTestCase(test_simba_keyword_rankingforecast_get)




