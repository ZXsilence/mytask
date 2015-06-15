#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: luxiaowen
@contact: luxiaowen@maimiaotech.com
@date: 2015-04-21 15:01
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
from tao_models.simba_customers_authorized_get import SimbaCustomersAuthorizedGet 
from TaobaoSdk.Exceptions import ErrorResponseException
#from tao_models.common.exceptions import InvalidAccessTokenException

class test_simba_customers_authorized_get(unittest.TestCase):
    maxDiff = None
    @classmethod
    def setUpClass(cls):
        pass
    
    def setUp(self):
        pass
    
    def test_get_authorized_customers(self):
        data = [{'nick':'麦苗科技001',
                 'expect_result':[u'ztc1','晓迎']},
                {'nick':'晓迎',
                 'expect_result':[]}]
                #{'cat_id_list':[501111582],'start_date_offset':8,'end_date_offset':1,
                # 'expect_result':[]},
                #{'cat_id_list':[5.1111582],'start_date_offset':8,'end_date_offset':1,
                # 'expect_result':{'code':15,'msg':'Remote service error','sub_code':'isv.invalid-parameter','sub_msg':'类目id错误！'}}]
        for item in data:
            nick = item['nick']
            expect_result = item['expect_result']
            try:
                actual_result = SimbaCustomersAuthorizedGet.get_authorized_customers(nick)
                self.assertEqual(type(actual_result),list)
                if len(actual_result)==0:
                    self.assertEqual(actual_result,expect_result)
                    continue
                #self.assertEqual(type(actual_result[0]),dict)
                for index in range(len(actual_result)):
                    self.assertIn(type(actual_result[index]),[type(u'ztc1'),type('晓迎')])
                    #self.assertEqual(actual_result[index].keys().sort(),expect_result[index].keys().sort())
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
alltests = unittest.TestLoader().loadTestsFromTestCase(test_simba_customers_authorized_get)
