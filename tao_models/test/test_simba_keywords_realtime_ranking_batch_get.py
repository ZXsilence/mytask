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
from tao_models.simba_adgroupsbycampaignid_get import SimbaAdgroupsbycampaignidGet
from tao_models.simba_keywordsbyadgroupid_get import SimbaKeywordsbyadgroupidGet
from tao_models.simba_keywords_realtime_ranking_batch_get  import SimbaKeywordsRealtimeRankingBatchGet 

class test_simba_keywords_realtime_ranking_get(unittest.TestCase):
    maxDiff = None
    @classmethod
    def setUpClass(cls):
        pass
    
    def setUp(self):
        pass
    
    def test_get_words_cats_data(self):
        data = [
            {'nick':'晓迎','type':1,'campaign_id':7155359,
                 'expect_result':{'stat': '0', 'pc_rank': '>100', 'mobile_rank': '>100', 'bidwordid': '248731629323'}},
            {'nick':'晓迎','type':2,'campaign_id':7155359,
                 'expect_result':{'stat': '0', 'pc_rank': '>100', 'mobile_rank': '>100', 'bidwordid': '248731629323'}}
                ]
        for item in data:
            nick = item['nick']
            campaign_id = item['campaign_id']
            adgroups = SimbaAdgroupsbycampaignidGet.get_adgroup_list_by_campaign(nick, campaign_id)
            adgroup_id = adgroups[0]['adgroup_id']
            keywords_list = SimbaKeywordsbyadgroupidGet.get_keyword_list_by_adgroup(nick, adgroup_id)
            keyword_ids = [keywords_list[0]['keyword_id']]
            expect_result = item['expect_result']
            try:
                if item['type']==1:
                    actual_result = SimbaKeywordsRealtimeRankingBatchGet.get_keywords_rank(nick,adgroup_id,keyword_ids)
                    self.assertEqual(type(actual_result),list)
                    aa = actual_result[0].keys()
                    bb = expect_result.keys()
                    aa.sort()
                    bb.sort()
                    self.assertEqual(aa,bb)
                elif item['type']==2:
                    actual_result = SimbaKeywordsRealtimeRankingBatchGet.get_keywords_rank(nick,adgroup_id,[11111])
            except KeyError:
                self.assertEqual(item['type'],2)
    
    def tearDown(self):
        pass
    
    @classmethod
    def tearDownClass(cls):
        pass
if __name__ == "__main__":
    unittest.main()
alltests = unittest.TestLoader().loadTestsFromTestCase(test_simba_keywords_realtime_ranking_get)
