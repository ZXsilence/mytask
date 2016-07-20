#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: luxiaowen
@contact: luxiaowen@maimiaotech.com
@date: 2015-04-15 10:44
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
from tao_models.simba_keywordsbyadgroupid_get import  SimbaKeywordsbyadgroupidGet
from TaobaoSdk.Exceptions import ErrorResponseException
from tao_models.common.exceptions import InvalidAccessTokenException

class test_simba_keywordsbyadgroupid_get(unittest.TestCase):
    maxDiff = None
    @classmethod
    def setUpClass(cls):
        pass
    
    def setUp(self):
        pass
    
    def test_get_words_cats_data(self):
        data = [{'nick':'晓迎','adgroup_id':407771771,
                 'expect_result':[{'qscore': '10', 
                                   'word': u'\u94bb\u6212\u4eff\u771f\u94bb', 
                                   'match_scope': '4', 
                                   'campaign_id': 7155359, 
                                   'modified_time': datetime.datetime(2015, 4, 14, 16, 36, 5), 
                                   'nick': u'\u6653\u8fce', 
                                   'create_time': datetime.datetime(2015, 4, 14, 16, 36, 5), 
                                   'is_default_price': False, 
                                   'adgroup_id': 407771771, 
                                   'keyword_id': 105291664764, 
                                   'audit_status': 'audit_pass', 
                                   'max_price': 64, 
                                   'is_garbage': False,
                                   'max_mobile_price':100,
                                   'mobile_is_default_price':1}]},
                {'nick':'chinchinstyle','adgroup_id':111111,
                 'expect_result':[]},
                {'nick':'晓迎1','adgroup_id':69533299980,
                 'expect_result':{'exception':'access session expired or invalid'}}]
               # {'cat_id_list':[5.1111582],'start_date_offset':8,'end_date_offset':1,
               #  'expect_result':{'code':15,'msg':'Remote service error','sub_code':'isv.missing-parameter','sub_msg':'date.must.lt.one.month'}}]
        for item in data:
            nick = item['nick']
            adgroup_id = item['adgroup_id']
            expect_result = item['expect_result']
            try:
                actual_result = SimbaKeywordsbyadgroupidGet.get_keyword_list_by_adgroup(nick, adgroup_id)
                self.assertEqual(type(actual_result),list)
                if len(actual_result) == 0:
                    self.assertEqual(actual_result,expect_result)
                bb = expect_result[0].keys()
                bb.sort()
                for index in range(len(actual_result)):
                    aa = actual_result[index].keys()
                    aa.sort()
                    self.assertEqual(aa,bb)
                    self.assertEqual(actual_result[index]['adgroup_id'],adgroup_id)
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
alltests = unittest.TestLoader().loadTestsFromTestCase(test_simba_keywordsbyadgroupid_get)
