#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: luxiaowen
@contact: luxiaowen@maimiaotech.com
@date: 2015-04-12 22:31
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
from tao_models.simba_insight_wordsareadata_get import SimbaInsightWordsareadataGet 
from TaobaoSdk.Exceptions import ErrorResponseException
#from tao_models.common.exceptions import InvalidAccessTokenException

class test_simba_insight_wordsareadata_get(unittest.TestCase):
    maxDiff = None
    @classmethod
    def setUpClass(cls):
        pass
    
    def setUp(self):
        pass
    
    def test_get_cats_data(self):
        '''
        校验实际返回的词数目是否一致（可能不足），权重是够降序
        '''
        data = [{'bidword':u'牙刷','start_date_offset':7,'end_date_offset':1,
                 'expect_result':[{'impression': 39101, 
                                   'cpc': '139.45', 
                                   'provincename': u'\u5b89\u5fbd', 
                                   'ctr': '1.03', 
                                   'roi': '0.89', 
                                   'directtransactionshipping': 27, 
                                   'indirecttransactionshipping': 1, 
                                   'cityname': u'\u5b89\u5fbd', 
                                   'competition': 0, 
                                   'transactiontotal': 49947, 
                                   'cost': 55892, 
                                   'directtransaction': 48453, 
                                   'indirecttransaction': 1633, 
                                   'coverage': '5.99', 
                                   'favshoptotal': 4, 
                                   'transactionshippingtotal': 28, 
                                   'bidword': u'牙刷', 
                                   'favitemtotal': 11, 
                                   'click': 442, 
                                   'favtotal': 15}]} ]
        
        for item in data:
            bidword = item['bidword']
            sdate = datetime.datetime.now() - datetime.timedelta(days=item['start_date_offset'])
            edate = datetime.datetime.now() - datetime.timedelta(days=item['end_date_offset'])
            expect_result = item['expect_result']
            try:
                actual_result = SimbaInsightWordsareadataGet.get_words_area_data(bidword,sdate,edate)
                self.assertEqual(type(actual_result),list)
                if len(actual_result)==0:
                    self.assertEqual(actual_result,expect_result)
                    continue
                self.assertEqual(type(actual_result[0]),dict)
                for index in range(len(actual_result)):
                    self.assertEqual(actual_result[index]['bidword'],expect_result[0]['bidword'])
                    if actual_result[index].get('provincename',None):
                        self.assertEqual(actual_result[index].keys().sort(),expect_result[0].keys().sort())
                        self.assertEqual(actual_result[index]['provincename'],actual_result[index]['cityname'])
                    else:
                        self.assertIn(len(actual_result[index]),[15,18])
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



