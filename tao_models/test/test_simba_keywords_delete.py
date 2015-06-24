#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: luxiaowen
@contact: luxiaowen@maimiaotech.com
@date: 2015-04-16 11:55
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
from tao_models.simba_keywords_delete import SimbaKeywordsDelete 
from tao_models.simba_keywordsbyadgroupid_get import SimbaKeywordsbyadgroupidGet
from TaobaoSdk.Exceptions import ErrorResponseException
from tao_models.common.exceptions import InvalidAccessTokenException

class test_simba_keywords_delete(unittest.TestCase):
    maxDiff = None
    @classmethod
    def setUpClass(cls):
        pass
    
    def setUp(self):
        pass
    #需要删除的关键词id动态获取
    def test_delete_keywords(self):
        data = [{'nick':'麦苗科技001','campaign_id':9214487,'adgroup_id':610409323,
                 'expect_result':[{'word': u'\u679a\u7ea2\u8272\u62d6\u978b', 
                                   'campaign_id': 9214487, 
                                   'modified_time': datetime.datetime(2015, 4, 16, 11, 51, 33), 
                                   'nick': u'\u9ea6\u82d7\u79d1\u6280001', 
                                   'create_time': datetime.datetime(2015, 4, 16, 11, 51, 33),
                                   'is_default_price': False, 
                                   'adgroup_id': 610409323, 
                                   'keyword_id': 105677384979, 
                                   'audit_status': 'audit_pass',
                                   'max_price': 38, 
                                   'is_garbage': False}]} ]
               # {'cat_id_list':[5.1111582],'start_date_offset':8,'end_date_offset':1,
               #  'expect_result':{'code':15,'msg':'Remote service error','sub_code':'isv.missing-parameter','sub_msg':'date.must.lt.one.month'}}]
        for item in data:
            nick = item['nick']
            campaign_id = item['campaign_id']
            adgroup_id = item['adgroup_id']
            expect_result = item['expect_result']
            keywords_list = SimbaKeywordsbyadgroupidGet.get_keyword_list_by_adgroup(nick, adgroup_id)
            keyword_id_list = [keywords_list[0]['keyword_id'],keywords_list[1]['keyword_id']]
            try:
                actual_result = SimbaKeywordsDelete.delete_keywords(nick, campaign_id, keyword_id_list)
                self.assertEqual(type(actual_result),list)
                if len(actual_result) == 0:
                    self.assertEqual(actual_result,expect_result)
                for index in range(len(actual_result)):
                    self.assertEqual(actual_result[index].keys().sort(),expect_result[0].keys().sort())
                    self.assertEqual(actual_result[index]['nick'],nick)
                    self.assertEqual(actual_result[index]['campaign_id'],campaign_id)
                    self.assertEqual(actual_result[index]['adgroup_id'],adgroup_id)
                    self.assertIn(actual_result[index]['keyword_id'],keyword_id_list)
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
alltests = unittest.TestLoader().loadTestsFromTestCase(test_simba_keywords_delete)
