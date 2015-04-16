#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: luxiaowen
@contact: luxiaowen@maimiaotech.com
@date: 2015-04-15 18:59
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
from tao_models.simba_keywords_changed_get import SimbaKeywordsChangedGet 
from TaobaoSdk.Exceptions import ErrorResponseException
from tao_models.common.exceptions import InvalidAccessTokenException
from TaobaoSdk import  SimbaKeywordsChangedGetRequest
class test_simba_keywords_changed_get(unittest.TestCase):
    maxDiff = None
    @classmethod
    def setUpClass(cls):
        pass
    
    def setUp(self):
        pass
    
    def test_get_words_cats_data(self):
        data = [{'nick':'晓迎','start_date_offset':7,'page_size':200,'page_no':1,
                 'expect_result':{}},
                {'nick':'晓迎1','start_date_offset':7,'page_size':200,'page_no':1,
                 'expect_result':{'exception':'access session expired or invalid'}}]
                #{'nick':'chinchinstyle','adgroup_id':111111,
                # 'expect_result':[]},
                #{'nick':'晓迎1','adgroup_id':69533299980,
                # 'expect_result':{'exception':'access session expired or invalid'}}]
               # {'cat_id_list':[5.1111582],'start_date_offset':8,'end_date_offset':1,
               #  'expect_result':{'code':15,'msg':'Remote service error','sub_code':'isv.missing-parameter','sub_msg':'date.must.lt.one.month'}}]
        for item in data:
            req = SimbaKeywordsChangedGetRequest()
            req.nick = item['nick']
            start_time = datetime.datetime.now() - datetime.timedelta(days=item['start_date_offset'])
            req.start_time = start_time.strftime("%Y-%m-%d %H:%M:%S")
            req.page_size = item['page_size']
            req.page_no = item['page_no']
            expect_result = item['expect_result']
            try:
                actual_result = SimbaKeywordsChangedGet._get_sub_keywords_changed(item['nick'],req)
                total_item = actual_result.keywords.total_item
                self.assertEqual(type(total_item),int)
                print total_item
                if total_item>0:
                    keyword_id = actual_result.keywords.keyword_list[0].keyword_id
                    adgroup_id = actual_result.keywords.keyword_list[0].adgroup_id
                    nick = actual_result.keywords.keyword_list[0].nick
                    self.assertEqual(type(keyword_id),int)
                    self.assertEqual(type(adgroup_id),int)
                    self.assertEqual(nick,req.nick)
                #if len(actual_result) == 0:
                #    self.assertEqual(actual_result,expect_result)
                #for index in range(len(actual_result)):
                #    self.assertEqual(actual_result[index].keys().sort(),expect_result[0].keys().sort())
                #    self.assertEqual(actual_result[index]['adgroup_id'],adgroup_id)
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
