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
#from MTextTestRunner import TextTestRunner

from api_server.conf import set_env
set_env.getEnvReady()
from api_server.conf.settings import set_api_source

from itemcats_get import ItemcatsGet
@unittest.skipUnless('regression' in settings.RUNTYPE, "Regression Test Case")
class TestItemcatsGet(unittest.TestCase):
    '''
    taobao.itemcats.get
    获取后台供卖家发布商品的标准商品类目。
    '''
    @classmethod
    def setUpClass(cls):
        set_api_source('SDK_TEST')
        cls.tcinfo = 'API Test - taobao.itemcats.get'
        cls.testInputDatas_cids = [{'cid':[-1], 'is_None': True},
                                   {'cid':[50006842], 'is_None': False}
                                   ]
        cls.testInputDatas_cats = [{'cid':-1, 'is_None': True},
                                   {'cid':0, 'is_None': False}
                                   ]
        cls.itemFields = ['cid','name','is_parent','parent_cid']
        cls.valueType = {'returnValue':list, 'item': dict}

    def setUp(self):
        pass

    def test_get_cats_by_cids(self):
        for inputdata in self.testInputDatas_cids:
            returnValue = ItemcatsGet.get_cats_by_cids(inputdata['cid'])
            if inputdata['is_None']:
                self.assertIsNone(returnValue, self.tcinfo)
            else:
                self.assertTrue(type(returnValue) == self.valueType['returnValue'], self.tcinfo)
                for item in returnValue:
                    self.assertTrue(type(item) == self.valueType['item'], self.tcinfo)
                    itemKeys = item.keys()
                    for field in self.itemFields:
                        self.assertTrue(field in itemKeys, self.tcinfo)

    def test_get_child_cats(self):
        for inputdata in self.testInputDatas_cats:
            returnValue = ItemcatsGet.get_child_cats(inputdata['cid'])
            if inputdata['is_None']:
                self.assertIsNone(returnValue, self.tcinfo)
            else:
                self.assertTrue(type(returnValue) == self.valueType['returnValue'], self.tcinfo)
                for item in returnValue:
                    self.assertTrue(type(item) == self.valueType['item'], self.tcinfo)
                    itemKeys = item.keys()

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
alltests = unittest.TestLoader().loadTestsFromTestCase(TestItemcatsGet)
