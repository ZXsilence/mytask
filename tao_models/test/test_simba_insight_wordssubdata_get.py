#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: luxiaowen
@contact: luxiaowen@maimiaotech.com
@date: 2015-04-13 14:24
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
from tao_models.simba_insight_wordssubdata_get import SimbaInsightWordssubdataGet
from TaobaoSdk.Exceptions import ErrorResponseException
#from tao_models.common.exceptions import InvalidAccessTokenException

class test_simba_insight_wordssubdata_get(unittest.TestCase):
    maxDiff = None
    @classmethod
    def setUpClass(cls):
        pass
    
    def setUp(self):
        pass
    
    def test_get_words_sub_data(self):
        data = [{'words_list':['连衣裙','裙子'],'start_date_offset':2,'end_date_offset':1,
                'expect_result':[{'impression': 28936480, 
                                  'cpc': '137.78', 
                                  'network': 1, 
                                  'ctr': '0.25', 
                                  'roi': '1.04', 
                                  'directtransactionshipping': 1642, 
                                  'indirecttransactionshipping': 343, 
                                  'mechanism': -1, 
                                  'transactiontotal': 10383102, 
                                  'cost': 10022380, 
                                  'directtransaction': 8490862, 
                                  'indirecttransaction': 1993046, 
                                  'coverage': '2.27', 
                                  'favshoptotal': 426, 
                                  'transactionshippingtotal': 1967, 
                                  'bidword': u'\u88e4\u5b50', 
                                  'favitemtotal': 2779, 
                                  'click': 80271, 
                                  'competition': 146260, 
                                  'favtotal': 3180}] } ]
               
               # {'cat_id_list':[5.1111582],'start_date_offset':8,'end_date_offset':1,
               #  'expect_result':{'code':15,'msg':'Remote service error','sub_code':'isv.invalid-parameter','sub_msg':'类目id错误！'}}]
        for item in data:
            words_list = item['words_list']
            sdate = datetime.datetime.now() - datetime.timedelta(days=item['start_date_offset'])
            edate = datetime.datetime.now() - datetime.timedelta(days=item['end_date_offset'])
            expect_result = item['expect_result']
            try:
                actual_result = SimbaInsightWordssubdataGet.get_words_sub_data(words_list,sdate,edate)
                self.assertEqual(type(actual_result),list)
                if len(actual_result)==0:
                    self.assertEqual(actual_result,expect_result)
                    continue
                self.assertEqual(type(actual_result[0]),dict)
                for index in range(len(actual_result)):
                    self.assertIn(actual_result[index]['bidword'],words_list)
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




