#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: luxiaowen
@contact: luxiaowen@maimiaotech.com
@date: 2015-04-09 16:09
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
from tao_models.simba_insight_catsdata_get import SimbaInsightCatsdataGet 
from TaobaoSdk.Exceptions import ErrorResponseException
#from tao_models.common.exceptions import InvalidAccessTokenException

class test_simba_insight_catsdata_get(unittest.TestCase):
    maxDiff = None
    @classmethod
    def setUpClass(cls):
        pass
    
    def setUp(self):
        pass
    
    def test_get_cats_data(self):
        '''
        校验实际返回的cat_id是否一致，其他只检查键是否一样
        '''
        data = [{'cat_id_list':[50023582], 'start_date_offset':8,'end_date_offset':1,
                 'expect_result':[{'impression': 5013, 
                                   'cpc': '57.4', 
                                   'transactiontotal': 50506, 
                                   'ctr': '0.96', 
                                   'roi': '21.11', 
                                   'directtransactionshipping': 2,
                                   'indirecttransactionshipping': 1, 
                                   'competition': 0, 
                                   'click': 48,
                                   'cost': 2543, 
                                   'directtransaction': 7827, 
                                   'indirecttransaction': 43109, 
                                   'coverage': '5.77', 
                                   'favshoptotal': 0, 
                                   'transactionshippingtotal': 3,
                                   'favitemtotal': 2, 
                                   'cat_id': 50023582,
                                   'favtotal': 2}] }]
        for item in data:
            cat_id_list = item['cat_id_list']
            start_date  = datetime.datetime.now() - datetime.timedelta(days = item['start_date_offset'])
            end_date    = datetime.datetime.now() - datetime.timedelta(days = item['end_date_offset'])
            actual_result = SimbaInsightCatsdataGet.get_cats_data(cat_id_list,start_date,end_date)
            expect_result = item['expect_result']
            self.assertEqual(type(actual_result),list)
            self.assertEqual(type(actual_result[0]),dict)
            for index in range(len(actual_result)):
                self.assertEqual(actual_result[index]['cat_id'],expect_result[index]['cat_id'])
                self.assertEqual(actual_result[index].keys().sort(),expect_result[index].keys().sort())
    
    def tearDown(self):
        pass
    
    @classmethod
    def tearDownClass(cls):
        pass
if __name__ == "__main__":
    unittest.main()
