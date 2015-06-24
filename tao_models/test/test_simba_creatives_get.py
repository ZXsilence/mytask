#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: luxiaowen
@contact: luxiaowen@maimiaotech.com
@date: 2015-04-21 14:03
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
from tao_models.simba_creatives_get import SimbaCreativesGet 
from TaobaoSdk.Exceptions import ErrorResponseException
from tao_models.common.exceptions import InvalidAccessTokenException

class test_simba_creatives_get(unittest.TestCase):
    maxDiff = None
    @classmethod
    def setUpClass(cls):
        pass
    
    def setUp(self):
        pass
    
    def test_get_creative_list_by_adgroup(self):
        data = [{'nick':'晓迎','adgroup_id':422902816,
                 'expect_result':[{'title': u'\u978b\u5b50', 
                                   'creative_id': 541059005, 
                                   'campaign_id': 10528974, 
                                   'nick': u'\u9ea6\u82d7\u79d1\u6280001', 
                                   'audit_status': 'audit_pass', 
                                   'img_url': 'http://img.taobaocdn.com/bao/uploaded/i3/19527055333310215/TB2cFtZaVXXXXXCXXXXXXXXXXXX_!!31119527-0-saturn_solar.jpg_sum.jpg', 
                                   'adgroup_id': 488978842}]},
                {'nick':'晓迎','adgroup_id':417982550,
                 'expect_result':[{'title': u'\u978b\u5b50', 
                                   'creative_id': 541059005, 
                                   'campaign_id': 10528974, 
                                   'nick': u'\u9ea6\u82d7\u79d1\u6280001', 
                                   'audit_status': 'audit_pass', 
                                   'img_url': 'http://img.taobaocdn.com/bao/uploaded/i3/19527055333310215/TB2cFtZaVXXXXXCXXXXXXXXXXXX_!!31119527-0-saturn_solar.jpg_sum.jpg', 
                                   'adgroup_id': 488978842}]},
                {'nick':'晓迎1','adgroup_id':69533299980,
                 'expect_result':{'exception':'access session expired or invalid'}}]
               # {'cat_id_list':[5.1111582],'start_date_offset':8,'end_date_offset':1,
               #  'expect_result':{'code':15,'msg':'Remote service error','sub_code':'isv.missing-parameter','sub_msg':'date.must.lt.one.month'}}]
        for item in data:
            nick = item['nick']
            adgroup_id = item['adgroup_id']
            expect_result = item['expect_result']
            try:
                actual_result = SimbaCreativesGet.get_creative_list_by_adgroup(nick, adgroup_id)
                #actual_result = SimbaKeywordsbyadgroupidGet.get_keyword_list_by_adgroup(nick, adgroup_id)
                self.assertEqual(type(actual_result),list)
                if len(actual_result) == 0:
                    self.assertEqual(actual_result,expect_result)
                for index in range(len(actual_result)):
                    self.assertEqual(actual_result[index].keys().sort(),expect_result[0].keys().sort())
                    self.assertEqual(actual_result[index]['adgroup_id'],adgroup_id)
            except InvalidAccessTokenException,e:
                self.assertEqual(e.msg,expect_result['exception'])
            except ErrorResponseException,e:
                self.assertEqual(e.code,expect_result['code'])
                self.assertEqual(e.msg,expect_result['msg'])
                self.assertEqual(e.sub_code,expect_result['sub_code'])
    def test_get_creative_list_by_creative_ids(self):
        data = [{'nick':'晓迎','creative_id':[453953583],
                 'expect_result':[{'title': u'\u73ab\u7470\u91d1\u6212\u6307 \u60c5\u4fa3\u6c42\u5a5a\u6212\u6307\u94bb\u77f3\u6212\u6307', 
                                   'creative_id': 512842527, 
                                   'campaign_id': 2256914, 
                                   'nick': u'\u6653\u8fce', 
                                   'audit_status': 'audit_pass', 
                                   'img_url': 'http://img.taobaocdn.com/bao/uploaded/i2/TB18jn2FXXXXXcvcXXXXXXXXXXX_!!0-item_pic.jpg_sum.jpg', 
                                   'adgroup_id': 417982550}]},
                {'nick':'晓迎','creative_id':[453953583,512842527],
                 'expect_result':[{'title': u'\u73ab\u7470\u91d1\u6212\u6307 \u60c5\u4fa3\u6c42\u5a5a\u6212\u6307\u94bb\u77f3\u6212\u6307', 
                                   'creative_id': 512842527, 
                                   'campaign_id': 2256914, 
                                   'nick': u'\u6653\u8fce', 
                                   'audit_status': 'audit_pass', 
                                   'img_url': 'http://img.taobaocdn.com/bao/uploaded/i2/TB18jn2FXXXXXcvcXXXXXXXXXXX_!!0-item_pic.jpg_sum.jpg', 
                                   'adgroup_id': 417982550}]},
                {'nick':'晓迎1','creative_id':[453953583],
                 'expect_result':{'exception':'access session expired or invalid'}}]
               # {'cat_id_list':[5.1111582],'start_date_offset':8,'end_date_offset':1,
               #  'expect_result':{'code':15,'msg':'Remote service error','sub_code':'isv.missing-parameter','sub_msg':'date.must.lt.one.month'}}]
        for item in data:
            nick = item['nick']
            creative_id  = item['creative_id']
            expect_result = item['expect_result']
            try:
                actual_result = SimbaCreativesGet.get_creative_list_by_creative_ids(nick, creative_id)
                #actual_result = SimbaKeywordsbyadgroupidGet.get_keyword_list_by_adgroup(nick, adgroup_id)
                self.assertEqual(type(actual_result),list)
                if len(actual_result) == 0:
                    self.assertEqual(actual_result,expect_result)
                for index in range(len(actual_result)):
                    self.assertEqual(actual_result[index].keys().sort(),expect_result[0].keys().sort())
                    self.assertIn(actual_result[index]['creative_id'],creative_id)
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
alltests = unittest.TestLoader().loadTestsFromTestCase(test_simba_creatives_get)
