#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: luxiaowen
@contact: luxiaowen@maimiaotech.com
@date: 2015-04-16 12:59
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
from tao_models.simba_keywords_qscore_get import SimbaKeywordsQscoreGet 
from TaobaoSdk.Exceptions import ErrorResponseException
from tao_models.common.exceptions import InvalidAccessTokenException
#from TaobaoSdk import  SimbaKeywordsChangedGetRequest
class test_simba_keywords_qscore_get(unittest.TestCase):
    maxDiff = None
    @classmethod
    def setUpClass(cls):
        pass
    
    def setUp(self):
        pass
    
    def test_get_keywords_qscore(self):
        data = [{'nick':'麦苗科技001','campaign_id':10528974,'adgroup_id':606180775,
                 'expect_result':[{'qscore': '6', 
                                   'word': u'\u5973\u5f0f\u6dbc\u62d6\u978b', 
                                   'campaign_id': 10528974, 
                                   'rele_score': '5', 
                                   'cust_score': '4', 
                                   'cvr_score': '5', 
                                   'keyword_id': 105734547011, 
                                   'creative_score': '4', 
                                   'adgroup_id': 488978842}]} ]
                #{'nick':'chinchinstyle','adgroup_id':111111,
                # 'expect_result':[]},
                #{'nick':'晓迎1','adgroup_id':69533299980,
                # 'expect_result':{'exception':'access session expired or invalid'}}]
               # {'cat_id_list':[5.1111582],'start_date_offset':8,'end_date_offset':1,
               #  'expect_result':{'code':15,'msg':'Remote service error','sub_code':'isv.missing-parameter','sub_msg':'date.must.lt.one.month'}}]
        for item in data:
            nick = item['nick']
            campaign_id = item['campaign_id']
            adgroup_id = item['adgroup_id']
            expect_result = item['expect_result']
            try:
                actual_result = SimbaKeywordsQscoreGet.get_keywords_qscore(nick,adgroup_id)
                self.assertEqual(type(actual_result),list)
                if len(actual_result)==0:
                    self.assertEqual(actual_result,expect_result)
                    continue
                self.assertEqual(type(actual_result[0]),dict)
                for index in range(len(actual_result)):
                    self.assertEqual(actual_result[index].keys().sort(),expect_result[0].keys().sort())
                    self.assertEqual(actual_result[index]['campaign_id'],campaign_id)
                    self.assertEqual(actual_result[index]['adgroup_id'],adgroup_id)
            except InvalidAccessTokenException,e:
                self.assertEqual(e.msg,expect_result['exception'])
            except ErrorResponseException,e:
                pass
                #self.assertEqual(e.code,expect_result['code'])
                #self.assertEqual(e.msg,expect_result['msg'])
                #self.assertEqual(e.sub_code,expect_result['sub_code'])
    def tearDown(self):
        pass
    
    @classmethod
    def tearDownClass(cls):
        pass
if __name__ == "__main__":
    unittest.main()
alltests = unittest.TestLoader().loadTestsFromTestCase(test_simba_keywords_qscore_get)


