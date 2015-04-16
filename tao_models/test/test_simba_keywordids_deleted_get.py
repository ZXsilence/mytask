#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: luxiaowen
@contact: luxiaowen@maimiaotech.com
@date: 2015-04-14 20:01
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
from tao_models.simba_keywordids_deleted_get import SimbaKeywordidsDeletedGet 
from TaobaoSdk.Exceptions import ErrorResponseException
from tao_models.common.exceptions import InvalidAccessTokenException

class test_simba_keywordids_deleted_get(unittest.TestCase):
    maxDiff = None
    @classmethod
    def setUpClass(cls):
        pass
    
    def setUp(self):
        pass
    
    def test_get_words_cats_data(self):
        data = [{'nick':'chinchinstyle','start_date_offset':7,
                 'expect_result':[97225580319, 97225580318, 97225580317, 97225580316, 97225580315, 97225580314, 97225580313, 97225580312, 
                                  97225568410, 97225568409, 97225568408, 97225568407, 97225568406, 97225568405, 97225568403, 97225568402]},
                {'nick':'chinchinstyle','start_date_offset':0,
                 'expect_result':[]},
                {'nick':'chinchinstyle','start_date_offset':100,
                 'expect_result':{'code':15,'msg':'Remote service error','sub_code':'isv.missing-parameter','sub_msg':'date.must.lt.one.month'}},
                {'nick':'chin1chinstyle','start_date_offset':100,                 
                 'expect_result':{'exception':'access session expired or invalid'}}]
               # {'cat_id_list':[5.1111582],'start_date_offset':8,'end_date_offset':1,
               #  'expect_result':{'code':15,'msg':'Remote service error','sub_code':'isv.missing-parameter','sub_msg':'date.must.lt.one.month'}}]
        for item in data:
            nick = item['nick']
            start_time = datetime.datetime.now()-datetime.timedelta(days=item['start_date_offset'])
            expect_result = item['expect_result']
            try:
                actual_result = SimbaKeywordidsDeletedGet.get_keywordids_deleted(nick,start_time)
                self.assertEqual(type(actual_result),list)
                for actual_res in actual_result:
                    self.assertEqual(type(actual_res),int)
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
alltests = unittest.TestLoader().loadTestsFromTestCase(test_simba_keywordids_deleted_get)






