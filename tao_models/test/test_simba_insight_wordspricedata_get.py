#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: luxiaowen
@contact: luxiaowen@maimiaotech.com
@date: 2015-04-13 11:01
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
from tao_models.simba_insight_wordspricedata_get import SimbaInsightWordspricedataGet 
from TaobaoSdk.Exceptions import ErrorResponseException
#from tao_models.common.exceptions import InvalidAccessTokenException

class test_simba_insight_wordspricedata_get(unittest.TestCase):
    maxDiff = None
    @classmethod
    def setUpClass(cls):
        pass
    
    def setUp(self):
        pass
    
    def test_get_words_price_data(self):
        '''
        校验实际返回的词数目是否一致（可能不足），权重是够降序
        '''
        data = [{'bidword':u'连衣裙','start_date_offset':2,'end_date_offset':1,
                 'expect_result':[{'impression': 230295, 
                                   'cpc': '28.25', 
                                   'transactiontotal': 112859, 
                                   'ctr': '0.53', 
                                   'roi': '3.23', 
                                   'directtransactionshipping': 10, 
                                   'indirecttransactionshipping': 4, 
                                   'competition': 541, 
                                   'click': 1353, 
                                   'cost': 35761, 
                                   'directtransaction': 90092, 
                                   'indirecttransaction': 23925, 
                                   'coverage': '0.89', 
                                   'favshoptotal': 11, 
                                   'transactionshippingtotal': 13, 
                                   'bidword': u'\u8fde\u8863\u88d9', 
                                   'favitemtotal': 30, 
                                   'price': 5, 
                                   'favtotal': 41}]} ]
        
        for item in data:
            bidword = item['bidword']
            sdate = datetime.datetime.now() - datetime.timedelta(days=item['start_date_offset'])
            edate = datetime.datetime.now() - datetime.timedelta(days=item['end_date_offset'])
            expect_result = item['expect_result']
            try:
                actual_result = SimbaInsightWordspricedataGet.get_words_price_data(bidword,sdate,edate)
                self.assertEqual(type(actual_result),list)
                if len(actual_result)==0:
                    self.assertEqual(actual_result,expect_result)
                    continue
                self.assertEqual(type(actual_result[0]),dict)
                for index in range(len(actual_result)):
                    self.assertEqual(actual_result[index]['bidword'],expect_result[0]['bidword'])
                    if actual_result[index].get('price',None):
                        self.assertEqual(actual_result[index].keys().sort(),expect_result[0].keys().sort())
                        #self.assertEqual(actual_result[index]['provincename'],actual_result[index]['cityname'])
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





