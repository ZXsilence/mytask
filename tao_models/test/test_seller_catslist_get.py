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

from seller_catslist_get import SellercatsListGet
from tao_models.common.exceptions import InvalidAccessTokenException
@unittest.skipUnless('regression' in settings.RUNTYPE, "Regression Test Case")
class TestSellercatsListGet(unittest.TestCase):
    '''
    taobao.sellercats.list.get
    获取前台展示的店铺内卖家自定义商品类目 
    '''
    @classmethod
    def setUpClass(cls):
        set_api_source('SDK_TEST')
        cls.tcinfo = 'API Test - taobao.sellercats.list.get'
        cls.testInputDatas = [{'nick':'chinchinstyle','popException':False, 'exceptionClass':None},
                              {'nick':'chinchinstyle','popException':True, 'exceptionClass':InvalidAccessTokenException},
                              ]
        cls.itemFields = 'name,cid,sort_order,parent_cid,type,pic_url'.split(',')
        cls.valueType = {'returnValue':list, 'item':dict}

    def setUp(self):
        pass

    def test_get_seller_cats_list(self):
        for inputdata in self.testInputDatas:
            returnValue = SellercatsListGet.get_seller_cats_list(inputdata['nick'])
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
alltests = unittest.TestLoader().loadTestsFromTestCase(TestSellercatsListGet)
