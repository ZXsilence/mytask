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
from tao_models.items_seller_list_get import ItemsSellerListGet  
from TaobaoSdk.Exceptions import ErrorResponseException
from tao_models.common.exceptions import InvalidAccessTokenException

class test_items_seller_list_get(unittest.TestCase):
    maxDiff = None
    @classmethod
    def setUpClass(cls):
        pass
    
    def setUp(self):
        pass
    def test_get_item_list(self):
        data = [{'nick':'chinchinstyle','num_iids':[7794896442],'type':1,
                 'expect_result':['seller_cids', 'title', 'num_iid', 'price', 'cid', 'newprepay', 'pic_url', 'freight_payer', 'property_alias', 'list_time', 
                                  'detail_url', 'delist_time', 'props_name']},
                {'nick':'chinchinstyle','num_iids':[7794896442,15493508084],'type':1,
                 'expect_result':['seller_cids', 'title', 'num_iid', 'price', 'cid', 'newprepay', 'pic_url', 'freight_payer', 'property_alias', 'list_time', 
                                  'detail_url', 'delist_time', 'props_name']},
                {'nick':'chinchinstyle','num_iids':[7794896442,15493508084],'type':2,'fields':'desc_modules,desc',
                 'expect_result':['desc_modules','desc']}]
        for item in data:
            nick = item['nick']
            num_iids = item['num_iids']
            expect_result = item['expect_result']
            try:
                if item['type']==1:
                    actual_result = ItemsSellerListGet.get_item_list(nick,num_iids)
                elif item['type']==2:
                    actual_result = ItemsSellerListGet.get_item_list(nick,num_iids,item['fields'])
                expect_result.sort()
                for item in range(len(actual_result)):
                    self.assertEqual(type(item),dict)
                    aa = item.keys()
                    aa.sort()
                    self.assertEqual(aa,expect_result)
            except:
                pass
    def tearDown(self):
        pass
    
    @classmethod
    def tearDownClass(cls):
        pass
if __name__ == "__main__":
    unittest.main()
alltests = unittest.TestLoader().loadTestsFromTestCase(test_simba_keyword_rankingforecast_get)
