#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: luxiaowen
@contact: luxiaowen@maimiaotech.com
@date: 2015-04-12 15:44
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
from tao_models.simba_insight_catstopwordnew_get import SimbaInsightCatstopwordnewGet 
from TaobaoSdk.Exceptions import ErrorResponseException
from tao_models.common.exceptions import TaoApiMaxRetryException
#from tao_models.common.exceptions import InvalidAccessTokenException

class test_simba_insight_catstopwordnew_get(unittest.TestCase):
    maxDiff = None
    @classmethod
    def setUpClass(cls):
        pass
    
    def setUp(self):
        pass
    
    def test_get_cats_top_words(self):
        '''
        获取制定类目在某个维度下的热门关键词
        '''
        data = [{'cat_id':50023582,'start_date_offset':7,'end_date_offset':1,'dimension':'click',
                 'expect_result':[{'impression': 1537, 
                                   'cpc': '64.53', 
                                   'transactiontotal': 13982, 
                                   'ctr': '1.9', 
                                   'roi': '7.74', 
                                   'directtransactionshipping': 3, 
                                   'indirecttransactionshipping': 0, 
                                   'competition': 51, 
                                   'cost': 1881, 
                                   'directtransaction': 13982, 
                                   'indirecttransaction': 0, 
                                   'coverage': '8.82', 
                                   'favshoptotal': 0, 
                                   'transactionshippingtotal': 3, 
                                   'bidword': u'\u9632\u5361\u8f90\u5c04', 
                                   'favitemtotal': 0, 
                                   'click': 32, 
                                   'cat_id': 50023582, 
                                   'favtotal': 0}]},
                {'cat_id':50023582,'start_date_offset':7,'end_date_offset':1,'dimension':'click','page_size':10,
                 'expect_result':[{'impression': 1537, 
                                   'cpc': '64.53', 
                                   'transactiontotal': 13982, 
                                   'ctr': '1.9', 
                                   'roi': '7.74', 
                                   'directtransactionshipping': 3, 
                                   'indirecttransactionshipping': 0, 
                                   'competition': 51, 
                                   'cost': 1881, 
                                   'directtransaction': 13982, 
                                   'indirecttransaction': 0, 
                                   'coverage': '8.82', 
                                   'favshoptotal': 0, 
                                   'transactionshippingtotal': 3, 
                                   'bidword': u'\u9632\u5361\u8f90\u5c04', 
                                   'favitemtotal': 0, 
                                   'click': 32, 
                                   'cat_id': 50023582, 
                                   'favtotal': 0}]},
                {'cat_id':50023582,'start_date_offset':9,'end_date_offset':1,'dimension':'click',
                 'expect_result':{'code':15,
                                  'msg':'Remote service error',
                                  'sub_code':'param_is_invalid',
                                  'sub_msg':'时间范围超出限制'}}]
        for item in data:
            cat_id = item['cat_id']
            dimension = item['dimension']
            page_size = item.get('page_size',0)
            sdate = datetime.datetime.now() - datetime.timedelta(days=item['start_date_offset'])
            edate = datetime.datetime.now() - datetime.timedelta(days=item['end_date_offset'])
            expect_result = item['expect_result']
            try:
                if page_size==0:
                    actual_result = SimbaInsightCatstopwordnewGet.get_cats_top_words(cat_id,sdate,edate,dimension)
                else:
                    actual_result = SimbaInsightCatstopwordnewGet.get_cats_top_words(cat_id,sdate,edate,dimension,page_size)
                self.assertEqual(type(actual_result),list)
                if page_size!=0:
                    self.assertEqual(len(actual_result),page_size)
                for index in range(len(actual_result)):
                    self.assertEqual(type(actual_result[index]),dict)
                    self.assertEqual(actual_result[index].keys().sort(),expect_result[0].keys().sort())
                    self.assertEqual(actual_result[index]['cat_id'],expect_result[0]['cat_id'])
                    if index > 0:
                        self.assertLessEqual(actual_result[index][dimension],actual_result[index-1][dimension])
            except TaoApiMaxRetryException,e:
                self.assertIn(expect_result['sub_msg'],e.msg)
            except ErrorResponseException,e:
                self.assertEqual(e.code,expect_result['code'])
                self.assertEqual(e.msg,expect_result['msg'])
                self.assertEqual(e.sub_code,expect_result['sub_code'])
                self.assertEqual(e.sub_msg,expect_result['sub_msg'])

    def tearDown(self):
        pass
    
    @classmethod
    def tearDownClass(cls):
        pass
if __name__ == "__main__":
    unittest.main()
alltests = unittest.TestLoader().loadTestsFromTestCase(test_simba_insight_catstopwordnew_get)
