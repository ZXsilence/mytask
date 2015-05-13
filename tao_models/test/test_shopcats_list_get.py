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

from shopcats_list_get import ShopcatsListGet
from tao_models.common.exceptions import InvalidAccessTokenException
@unittest.skipUnless('regression' in settings.RUNTYPE, "Regression Test Case")
class TestShopcatsListGet(unittest.TestCase):
    '''
    taobao.shopcats.list.get
    获取淘宝面向买家的浏览导航类目（跟后台卖家商品管理的类目有差异）
    '''
    @classmethod
    def setUpClass(cls):
        set_api_source('SDK_TEST')
        cls.tcinfo = 'API Test - taobao.shopcats.list.get'
        cls.itemFields = 'cid,name,is_parent,parent_cid'.split(',')
        cls.valueType = {'returnValue':list, 'item':dict}

    def setUp(self):
        pass

    def test_get_shopcats_list(self):
        returnValue = ShopcatsListGet.get_shopcats_list()
        self.assertTrue(type(returnValue) == self.valueType['returnValue'], self.tcinfo)
        for item in returnValue:
            self.assertTrue(type(item) == self.valueType['item'], self.tcinfo)
            itemKeys = item.keys()
            for field in self.itemFields:
                self.assertTrue(field in itemKeys, self.tcinfo)


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
alltests = unittest.TestLoader().loadTestsFromTestCase(TestShopcatsListGet)
