#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: luxiaowen
@contact: luxiaowen@maimiaotech.com
@date: 2015-04-13 13:35
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
from tao_models.simba_insight_wordsdata_get import SimbaInsightWordsdataGet
from TaobaoSdk.Exceptions import ErrorResponseException
#from tao_models.common.exceptions import InvalidAccessTokenException

class test_simba_insight_wordsdata_get(unittest.TestCase):
    maxDiff = None
    @classmethod
    def setUpClass(cls):
        pass
    
    def setUp(self):
        pass
    
    def test_get_words_cats_data(self):
        data = [{'words_list':['连衣裙','裙子'],'start_date_offset':2,'end_date_offset':1,
                'expect_result':[{'impression': 177203296, 
                                  'cpc': '63.88', 
                                  'transactiontotal': 29686742, 
                                  'ctr': '0.48', 
                                  'roi': '0.52', 
                                  'directtransactionshipping': 2301, 
                                  'indirecttransactionshipping': 515, 
                                  'competition': 79909, 'cost': 55827188, 
                                  'directtransaction': 23410656, 
                                  'indirecttransaction': 6588620, 
                                  'coverage': '0.26', 
                                  'favshoptotal': 4101, 
                                  'transactionshippingtotal': 2790, 
                                  'bidword': u'连衣裙', 
                                  'favitemtotal': 29646, 
                                  'click': 949736, 
                                  'favtotal': 33502}]} ]
               # {'cat_id_list':[5.1111582],'start_date_offset':8,'end_date_offset':1,
               #  'expect_result':{'code':15,'msg':'Remote service error','sub_code':'isv.invalid-parameter','sub_msg':'类目id错误！'}}]
        for item in data:
            words_list = item['words_list']
            sdate = datetime.datetime.now() - datetime.timedelta(days=item['start_date_offset'])
            edate = datetime.datetime.now() - datetime.timedelta(days=item['end_date_offset'])
            expect_result = item['expect_result']
            try:
                actual_result = SimbaInsightWordsdataGet._get_words_data(words_list,sdate,edate)
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
alltests = unittest.TestLoader().loadTestsFromTestCase(test_simba_insight_wordsdata_get)
