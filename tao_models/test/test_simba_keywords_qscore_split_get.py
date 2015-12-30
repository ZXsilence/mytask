#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: luxiaowen
@contact: luxiaowen@maimiaotech.com
@date: 2015-04-13 15:04
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
from tao_models.simba_adgroupsbycampaignid_get import SimbaAdgroupsbycampaignidGet
from tao_models.simba_keywordsbyadgroupid_get import SimbaKeywordsbyadgroupidGet
from tao_models.simba_keywords_qscore_split_get import SimbaKeywordsQscoreSplitGet 
from TaobaoSdk.Exceptions import ErrorResponseException
from tao_models.common.exceptions import InvalidAccessTokenException
from tao_models.common.exceptions import RankKeywordNotExisitException

class test_simba_keywords_realtime_ranking_get(unittest.TestCase):
    maxDiff = None
    @classmethod
    def setUpClass(cls):
        pass
    
    def setUp(self):
        pass
    def test_get_words_cats_data(self):
        data = [
            {'nick':'晓迎','campaign_id':7155359,'type':'single',
                 'expect_result':{'pscore': '-1', 'wireless_cvrscore': '4', 'catscore': '-1', 'qscore': '7', 'word': u'\u53ef\u8c03\u5408\u91d1\u624b\u956f', 
                                  'wireless_relescore': '5','wireless_creativescore': '4', 'pc_left_flag': 0, 'plflag': 1, 'ad_type': 'tbuad', 
                                  'campaign_id': 7155359, 'wireless_custscore': '4','wireless_matchflag': 4, 'cvrscore': '4', 'keyword_id': 248731629323, 
                                  'creativescore': '3', 'kwscore': '5', 'custscore': '4', 'wireless_qscore': '7', 'adgroup_id': 407769717}},
            {'nick':'晓迎','campaign_id':7155359,'type':'multi',
                 'expect_result':{'pscore': '-1', 'wireless_cvrscore': '4', 'catscore': '-1', 'qscore': '7', 'word': u'\u53ef\u8c03\u5408\u91d1\u624b\u956f', 
                                  'wireless_relescore': '5','wireless_creativescore': '4', 'pc_left_flag': 0, 'plflag': 1, 'ad_type': 'tbuad', 
                                  'campaign_id': 7155359, 'wireless_custscore': '4','wireless_matchflag': 4, 'cvrscore': '4', 'keyword_id': 248731629323, 
                                  'creativescore': '3', 'kwscore': '5', 'custscore': '4', 'wireless_qscore': '7', 'adgroup_id': 407769717}
                }]
        for item in data:
            expect_result = item['expect_result']
            nick = item['nick']
            campaign_id = item['campaign_id']
            test_type = item['type']
            adgroups = SimbaAdgroupsbycampaignidGet.get_adgroup_list_by_campaign(nick, campaign_id)
            adgroup_id = adgroups[0]['adgroup_id']
            keywords_list = SimbaKeywordsbyadgroupidGet.get_keyword_list_by_adgroup(nick, adgroup_id)
            if test_type == 'single':
                keyword_id = keywords_list[0]['keyword_id']
                keyword_id_list = [keyword_id]
            elif test_type == 'multi':
                keyword_id_list = [item['keyword_id'] for item in keywords_list]
            try:
                actual_result = SimbaKeywordsQscoreSplitGet.get_keywords_split_qscore(nick, adgroup_id, keyword_id_list)
                self.assertEqual(type(actual_result),list)
                for index in range(len(actual_result)):
                    self.assertEqual(actual_result[index].keys().sort(),expect_result.keys().sort())
            except RankKeywordNotExisitException,e:
                pass
    def tearDown(self):
        pass
    
    @classmethod
    def tearDownClass(cls):
        pass
if __name__ == "__main__":
    unittest.main()
alltests = unittest.TestLoader().loadTestsFromTestCase(test_simba_keyword_rankingforecast_get)
