#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wangying
@contact: wangying@maimiaotech.com
@date: 2014-09-25 14:07
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""
import sys
sys.path.append('../')
sys.path.append('../../')
import settings
import datetime
import logging
import logging.config
import unittest
from api_server.conf import set_env
set_env.getEnvReady()
from api_server.conf.settings import set_api_source

from mm_simba_tools_items_top_get import MMSimbaToolsItemsTopGet
from tao_models.common.exceptions import InvalidAccessTokenException
from tao_models.common.exceptions import TaoApiMaxRetryException
from TaobaoSdk.Exceptions import ErrorResponseException
@unittest.skipUnless('regression' in settings.RUNTYPE, "Regression Test Case")
class TestMMSimbaToolsItemsTopGet(unittest.TestCase):
    '''
    taobao.simba.tools.items.top.get
    取得一个关键词的推广组排名列表
    '''
    @classmethod
    def setUpClass(cls):
        set_api_source('SDK_TEST')
        cls.tcinfo = 'API Test - taobao.simba.tools.items.top.get'
        cls.testInputDatas = [{'nick':'麦苗科技001','soft_code':'SYB','keyword':'elle 女包','popException':False, 'exceptionClass':None},
                              {'nick':'__NOTEXISTEDNICK__','soft_code':'SYB','keyword':'elle 女包','popException':True, 'exceptionClass':InvalidAccessTokenException},
                              {'nick':'chinchinstyle','soft_code':'SYB','keyword':'','popException':True, 'exceptionClass':ErrorResponseException},
                              ]
        cls.valueType = {'returnValue':list}
        cls.itemFields = 'link_url,order,title,rank_score,max_price'

    def setUp(self):
        pass

    def test_get_top_items_by_keyword(self):
        for inputdata in self.testInputDatas:
            is_poped = False
            try:
                returnValue = MMSimbaToolsItemsTopGet.get_top_items_by_keyword(inputdata['nick'],inputdata['keyword'],inputdata['soft_code'])
                self.assertTrue(type(returnValue) == self.valueType['returnValue'], self.tcinfo)
                for i in range(len(returnValue)):
                    itemKeys = returnValue[i].keys()
                    for item in itemKeys:
                        self.assertTrue(item in self.itemFields.split(','), self.tcinfo)
            except Exception, e:
                is_poped = True
                self.assertRaises(inputdata['exceptionClass'])
            finally:
                self.assertEqual(inputdata['popException'],is_poped,self.tcinfo)


    #@unittest.skip("Unconditionally skip the decorated test")
    #def test_skip(self):
    #    """test"""
    #    pass

    #@unittest.expectedFailure
    #def test_expectedFailure(self):
    #    """test"""
    #    print self.testdata

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == '__main__':                                                       
    unittest.main()

#custtests = unittest.TestSuite(map(TestReportService, ['test_rpt_cust_1']))
alltests = unittest.TestLoader().loadTestsFromTestCase(TestMMSimbaToolsItemsTopGet)
