#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: luxiaowen
@contact: luxiaowen@maimiaotech.com
@date: 2015-04-12 11:37
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
from tao_models.simba_insight_relatedwords_get import  SimbaInsightRelatedwordsGet
from TaobaoSdk.Exceptions import ErrorResponseException
#from tao_models.common.exceptions import InvalidAccessTokenException

class test_simba_insight_relatedwords_get(unittest.TestCase):
    maxDiff = None
    @classmethod
    def setUpClass(cls):
        pass
    
    def setUp(self):
        pass
    
    def test_get_cats_data(self):
        '''
        校验实际返回的词数目是否一致（可能不足），权重是够降序
        '''
        data = [{'bidword_list':["连衣裙"],'num':10,
                 'expect_result':[{'bidword': u'连衣裙', 
                                   'related_word_items_list': [{'related_word': u'\t\u8fde\u8863\u88d9\u957f\u8896', 'weight': '1'}, 
                                                               {'related_word': u'\u6625\u88c5\u8fde\u8863\u88d9', 'weight': '0.87'}, 
                                                               {'related_word': u'\u6625\u79cb\u8fde\u8863\u88d9', 'weight': '0.85'}, 
                                                               {'related_word': u'\u96ea\u7eba\u8fde\u8863\u88d9', 'weight': '0.69'}, 
                                                               {'related_word': u'\u857e\u4e1d\u8fde\u8863\u88d9', 'weight': '0.61'}, 
                                                               {'related_word': u'\u771f\u4e1d\u8fde\u8863\u88d9', 'weight': '0.36'}, 
                                                               {'related_word': u'\u788e\u82b1\u8fde\u8863\u88d9', 'weight': '0.36'}, 
                                                               {'related_word': u'\u8fde\u8863\u88d9\u590f', 'weight': '0.34'}, 
                                                               {'related_word': u'\u590d\u53e4 \u8fde\u8863\u88d9', 'weight': '0.3'}, 
                                                               {'related_word': u'\u79cb\u51ac\u8fde\u8863\u88d9', 'weight': '0.22'}]}]}
                ]
        
        for item in data:
            bidword_list = item['bidword_list']
            num = item['num']
            expect_result = item['expect_result']
            try:
                actual_result = SimbaInsightRelatedwordsGet._get_related_words(bidword_list,num)
                self.assertEqual(type(actual_result),list)
                if len(actual_result)==0:
                    self.assertEqual(actual_result,expect_result)
                    continue
                self.assertEqual(type(actual_result[0]),dict)
                for index in range(len(actual_result)):
                    self.assertEqual(actual_result[index]['bidword'],expect_result[index]['bidword'])
                    self.assertEqual(actual_result[index].keys().sort(),expect_result[index].keys().sort())
                    self.assertEqual(len(actual_result[index]['related_word_items_list']),num)
                    if num > 1:
                        for i in range(num):
                            if i > 0:
                                self.assertLessEqual(actual_result[index]['related_word_items_list'][i]['weight'],actual_result[index]['related_word_items_list'][i-1]['weight'])
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
alltests = unittest.TestLoader().loadTestsFromTestCase(test_simba_insight_relatedwords_get)
