#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: luxiaowen
@contact: luxiaowen@maimiaotech.com
@date: 2015-04-15 13:36
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
from tao_models.simba_keywordsbykeywordids_get import SimbaKeywordsbykeywordidsGet 
from TaobaoSdk.Exceptions import ErrorResponseException
from tao_models.common.exceptions import InvalidAccessTokenException

class test_simba_keywordsbykeywordids_get(unittest.TestCase):
    maxDiff = None
    @classmethod
    def setUpClass(cls):
        pass
    
    def setUp(self):
        pass
    
    def test_sub_get_keyword_list_by_keyword_ids(self):
        data = [{'nick':'晓迎','keywordids_list':[96000635553,101461016943,99975482757],
                 'expect_result':{'audit_desc': None, 
                                  'qscore': '10', 
                                  'word': u'\u94bb\u6212 \u4eff\u771f', 
                                  '_Keyword__kargs': {'qscore': '10', 
                                                      'word': u'\u94bb\u6212 \u4eff\u771f', 
                                                      'nick': u'\u6653\u8fce', 
                                                      'campaign_id': 7155359, 
                                                      'modified_time': '2015-03-21 18:48:53', 
                                                      'match_scope': '4', 
                                                      'create_time': '2015-02-06 12:56:30', 
                                                      'is_default_price': False, 
                                                      'is_garbage': False, 
                                                      'keyword_id': 96000635553, 
                                                      'audit_status': 'audit_pass', 
                                                      'max_price': 50, 
                                                      'adgroup_id': 407767758}, 
                                  'nick': u'\u6653\u8fce', 
                                  'campaign_id': 7155359, 
                                  'modified_time': datetime.datetime(2015, 3, 21, 18, 48, 53), 
                                  'match_scope': '4', 
                                  'create_time': datetime.datetime(2015, 2, 6, 12, 56, 30), 
                                  'is_default_price': False, 
                                  'is_garbage': False, 
                                  'keyword_id': 96000635553, 
                                  'audit_status': 'audit_pass', 
                                  'max_price': 50, 
                                  'adgroup_id': 407767758}},
                {'nick':'晓迎','keywordids_list':[96000635553,101461016943,99975482757]*100,
                 'expect_result':{'code':41,'msg':'Invalid arguments:keyword_ids','sub_code':None,'sub_msg':None}},
                {'nick':'晓迎','keywordids_list':[122],
                 'expect_result':{'code':15,'msg':'Remote service error','sub_code':'isv.entity-not-exist','sub_msg':'推广组未找到'}},
                {'nick':'晓迎','keywordids_list':[],
                 'expect_result':{'code':41,'msg':'Invalid arguments:keyword_ids','sub_code':None,'sub_msg':None}}]
                #{'nick':'晓迎1','adgroup_id':69533299980,
                # 'expect_result':{'exception':'access session expired or invalid'}}]
               # {'cat_id_list':[5.1111582],'start_date_offset':8,'end_date_offset':1,
               #  'expect_result':{'code':15,'msg':'Remote service error','sub_code':'isv.missing-parameter','sub_msg':'date.must.lt.one.month'}}]
        for item in data:
            nick = item['nick']
            keywordids_list = item['keywordids_list']
            expect_result = item['expect_result']
            try:
                actual_result = SimbaKeywordsbykeywordidsGet._sub_get_keyword_list_by_keyword_ids(nick,keywordids_list)
                self.assertEqual(type(actual_result),list)
                if len(actual_result) == 0:
                    self.assertEqual(actual_result,expect_result)
                    continue
                self.assertEqual(len(actual_result),len(keywordids_list))
                for index in range(len(actual_result)):
                    actual_res =  actual_result[index].__dict__
                    #self.assertEqual(type(actual_result[index]),<class 'Domain.Keyword.Keyword'>)
                    self.assertEqual(actual_res.keys().sort(),expect_result.keys().sort())
                    self.assertIn(actual_res['keyword_id'],keywordids_list)
                    #self.assertEqual(actual_result[index]['adgroup_id'],adgroup_id)
            except InvalidAccessTokenException,e:
                self.assertEqual(e.msg,expect_result['exception'])
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
