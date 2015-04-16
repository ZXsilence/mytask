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

from item_get import ItemGet
from tao_models.common.exceptions import TaoApiMaxRetryException
from TaobaoSdk.Exceptions import ErrorResponseException
@unittest.skipUnless('regression' in settings.RUNTYPE, "Regression Test Case")
class TestItemGet(unittest.TestCase):
    '''
    taobao.item.get
    获取单个商品的详细信息 卖家未登录时只能获得这个商品的公开数据，卖家登录后可以获取商品的所有数据
    '''
    @classmethod
    def setUpClass(cls):
        set_api_source('SDK_TEST')
        cls.tcinfo = 'API Test - taobao.item.get'
        cls.testInputDatas_cid = [{'num_iid': 0,'popException':True, 'exceptionClass':ErrorResponseException},
                                  {'num_iid': 36036924301,'popException':False, 'exceptionClass':None}
                                  ]
        cls.testInputDatas_info = [{'num_iid': 0,'popException':True, 'exceptionClass':ErrorResponseException},
                                  {'num_iid': 36036924301,'popException':False, 'exceptionClass':None}
                                  ]
        cls.valueType = {'returnValue_cid':int, 'returnValue_info':dict}
        cls.itemFields = 'created,num_iid,title,list_time,price,item_img,pic_url,seller_cids,cid,freight_payer,props_name'.split(',')

    def setUp(self):
        pass

    @unittest.skip("Unconditionally skip the No Use test")
    def test_get_cid(self):
        for inputdata in self.testInputDatas_cid:
            self.tcinfo = 'API Test - taobao.item.get'
            self.tcinfo += str(inputdata)
            is_poped = False
            try:
                returnValue = ItemGet.get_cid(inputdata['num_iid'])
                self.assertTrue(type(returnValue) == self.valueType['returnValue_cid'], self.tcinfo)
            except Exception, e:
                is_poped = True
                self.assertRaises(inputdata['exceptionClass'])
            finally:
                self.assertEqual(inputdata['popException'],is_poped,self.tcinfo)
    @unittest.skip("Unconditionally skip the No Use test")
    def test_get_item_info(self):
        for inputdata in self.testInputDatas_info:
            self.tcinfo = 'API Test - taobao.item.get'
            self.tcinfo += str(inputdata)
            is_poped = False
            try:
                returnValue = ItemGet.get_item_info(inputdata['num_iid'])
                self.assertTrue(type(returnValue) == self.valueType['returnValue_info'], self.tcinfo)
                itemKeys = returnValue.keys()
                for item in self.itemFields:
                    self.assertTrue(item in itemKeys, self.tcinfo)
            except Exception, e:
                is_poped = True
                self.assertRaises(inputdata['exceptionClass'])
            finally:
                self.assertEqual(inputdata['popException'],is_poped,self.tcinfo)
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
alltests = unittest.TestLoader().loadTestsFromTestCase(TestItemGet)
