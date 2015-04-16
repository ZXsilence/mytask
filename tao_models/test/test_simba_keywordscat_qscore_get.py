#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: luxiaowen
@contact: luxiaowen@maimiaotech.com
@date: 2015-04-15 16:17
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
from tao_models.simba_keywordscat_qscore_get import SimbaKeywordscatQscoreGet 
from TaobaoSdk.Exceptions import ErrorResponseException
from tao_models.common.exceptions import InvalidAccessTokenException

class test_simba_keywordscat_qscore_get(unittest.TestCase):
    maxDiff = None
    @classmethod
    def setUpClass(cls):
        pass
    
    def setUp(self):
        pass
    
    def test_get_words_cats_data(self):
        data = [{'nick':'晓迎','adgroup_id':407771771,
                 'expect_result':{'keyword_qscore_list': [{'keyword_id': 105291664764, 
                                                           'qscore': '10', 
                                                           'word': u'\u94bb\u6212\u4eff\u771f\u94bb', 
                                                           'campaign_id': 7155359, 
                                                           'adgroup_id': 407771771}]}}]

                #'expect_result':{'code':15,'msg':'Remote service error','sub_code':'isv.invalid-parameter','sub_msg':'keyword.not.found'}},
                #{'nick':'晓迎1','keyword_id':69533299980,
                # 'expect_result':{'exception':'access session expired or invalid'}}]
               # {'cat_id_list':[5.1111582],'start_date_offset':8,'end_date_offset':1,
               #  'expect_result':{'code':15,'msg':'Remote service error','sub_code':'isv.invalid-parameter','sub_msg':'类目id错误！'}}]
        for item in data:
            nick = item['nick']
            adgroup_id = item['adgroup_id']
            expect_result = item['expect_result']
            try:
                actual_result = SimbaKeywordscatQscoreGet.get_qscore_list_by_adgroup(nick, adgroup_id)
                self.assertEqual(type(actual_result),dict)
                if len(actual_result)==0:
                    self.assertEqual(actual_result,expect_result)
                    continue
                self.assertEqual(actual_result.keys(),['keyword_qscore_list'])
                for index in range(len(actual_result['keyword_qscore_list'])):
                    self.assertEqual(type(actual_result['keyword_qscore_list'][index]),dict)
                    self.assertEqual(actual_result['keyword_qscore_list'][index].keys().sort(),expect_result['keyword_qscore_list'][0].keys().sort())
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
alltests = unittest.TestLoader().loadTestsFromTestCase(test_simba_keywordscat_qscore_get)






