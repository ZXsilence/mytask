#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: luxiaowen
@contact: luxiaowen@maimiaotech.com
@date: 2015-04-13 11:33
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
from tao_models.simba_insight_catsworddata_get import SimbaInsightCatsworddataGet 
from TaobaoSdk.Exceptions import ErrorResponseException
#from tao_models.common.exceptions import InvalidAccessTokenException

class test_simba_insight_catsworddata_get(unittest.TestCase):
    maxDiff = None
    @classmethod
    def setUpClass(cls):
        pass
    
    def setUp(self):
        pass
    
    def test_get_words_cats_data(self):
        data = [{'bidword_list':['连衣裙'],'cat_id':50000852,'start_date_offset':7,'end_date_offset':1,
                'expect_result':[{'impression': 190663, 
                                  'cpc': '120.9', 
                                  'transactiontotal': 8598, 
                                  'ctr': '0.14', 
                                  'roi': '0.25', 
                                  'directtransactionshipping': 2, 
                                  'indirecttransactionshipping': 0, 
                                  'competition': 1844, 
                                  'cost': 32854, 
                                  'directtransaction': 8598, 
                                  'indirecttransaction': 0, 
                                  'coverage': '0.6', 
                                  'favshoptotal': 2, 
                                  'transactionshippingtotal': 2, 
                                  'bidword': u'连衣裙', 
                                  'favitemtotal': 5, 
                                  'click': 299, 
                                  'cat_id': 50000852, 
                                  'favtotal': 7}] } ]
               # {'cat_id_list':[5.1111582],'start_date_offset':8,'end_date_offset':1,
               #  'expect_result':{'code':15,'msg':'Remote service error','sub_code':'isv.invalid-parameter','sub_msg':'类目id错误！'}}]
        for item in data:
            bidword_list = item['bidword_list']
            cat_id = item['cat_id']
            sdate = datetime.datetime.now() - datetime.timedelta(days=item['start_date_offset'])
            edate = datetime.datetime.now() - datetime.timedelta(days=item['end_date_offset'])
            expect_result = item['expect_result']
            try:
                actual_result = SimbaInsightCatsworddataGet.get_words_cats_data(cat_id,bidword_list,sdate,edate)
                self.assertEqual(type(actual_result),list)
                if len(actual_result)==0:
                    self.assertEqual(actual_result,expect_result)
                    continue
                self.assertEqual(type(actual_result[0]),dict)
                for index in range(len(actual_result)):
                    self.assertIn(actual_result[index]['bidword'],bidword_list)
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
