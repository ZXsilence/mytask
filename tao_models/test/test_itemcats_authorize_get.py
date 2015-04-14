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

from itemcats_authorize_get import ItemcatsAuthorizeGet
from tao_models.common.exceptions import TaoApiMaxRetryException
from TaobaoSdk.Exceptions import ErrorResponseException
@unittest.skipUnless('regression' in settings.RUNTYPE, "Regression Test Case")
class TestItemcatsAuthorizeGet(unittest.TestCase):
    '''
    taobao.itemcats.authorize.get
    查询B商家被授权品牌列表、类目列表和 c 商家新品类目列表
    '''
    @classmethod
    def setUpClass(cls):
        set_api_source('SDK_TEST')
        cls.tcinfo = 'API Test - taobao.itemcats.authorize.get'
        cls.testInputDatas = [{'nick':'chinchinstyle','fields':'','popException':True, 'exceptionClass':ErrorResponseException, 'returnList':None},
                              {'nick':'chinchinstyle','fields':'brand.vid, brand.name, item_cat.cid, item_cat.name,xinpin_item_cat.cid, xinpin_item_cat.name','popException':False, 'exceptionClass':None,'returnList':['xinpin_item_cats']},
                              #{'nick':'','fields':'brand.vid, brand.name, item_cat.cid, item_cat.name,xinpin_item_cat.cid, xinpin_item_cat.name','popException':False, 'exceptionClass':None,'returnList':['brands','item_cats']},
                              {'nick':'','fields':'brand.vid, brand.name, item_cat.cid, item_cat.name,xinpin_item_cat.cid, xinpin_item_cat.name','popException':False, 'exceptionClass':None,'returnList':['xinpin_item_cats']},
                              ]
        cls.valueType = {'returnValue':dict}

    def setUp(self):
        pass

    def test_get_itemcats_authorize(self):
        for inputdata in self.testInputDatas:
            is_poped = False
            self.tcinfo = 'API Test - taobao.itemcats.authorize.get'
            self.tcinfo += str(inputdata)
            try:
                returnValue = ItemcatsAuthorizeGet.get_itemcats_authorize(inputdata['nick'],inputdata['fields'])
                self.assertTrue(type(returnValue) == self.valueType['returnValue'], self.tcinfo)
                returnKeys = returnValue.keys()
                for item in inputdata['returnList']:
                    self.assertTrue(item in returnKeys, self.tcinfo)
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
alltests = unittest.TestLoader().loadTestsFromTestCase(TestItemcatsAuthorizeGet)
