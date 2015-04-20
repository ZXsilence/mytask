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

from items_onsale_get import ItemsOnsaleGet
from shop_db.services.shop_info_service import SyopInfoService
from tao_models.common.exceptions import TaoApiMaxRetryException
from tao_models.common.exceptions import InvalidAccessTokenException
from TaobaoSdk.Exceptions import ErrorResponseException
@unittest.skipUnless('regression' in settings.RUNTYPE, "Regression Test Case")
class TestItemsOnsaleGet(unittest.TestCase):
    '''
    taobao.items.onsale.get
    获取当前用户作为卖家的出售中的商品列表，并能根据传入的搜索条件对出售中的商品列表进行过滤 只能获得商品的部分信息
    '''
    @classmethod
    def setUpClass(cls):
        set_api_source('SDK_TEST')
        cls.tcinfo = 'API Test - taobao.items.onsale.get'
        cls.testInputDatas_list = [{'nick':'麦苗科技001','popException':False, 'exceptionClass':None},
                                   {'nick':'__NotExistedNick__','popException':True, 'exceptionClass':InvalidAccessTokenException}
                                   ]
        cls.testInputDatas_with_overview = [{'nick':'麦苗科技001','popException':False, 'exceptionClass':None},
                                   {'nick':'__NotExistedNick__','popException':True, 'exceptionClass':InvalidAccessTokenException}
                                   ]
        cls.testInputDatas_with_access_token = [{'nick':'麦苗科技001','soft_code':'SYB','popException':False, 'exceptionClass':None},
                                     ]
        cls.valueType_list = {'returnValue':list}
        cls.valueType_with_overview = {'returnValue':dict}
        cls.itemFields_list = 'price,num_iid,pic_url,title'.split(',')
        cls.itemFields_with_overview = 'total_results,item_list'.split(',')
        cls.itemFields_with_overview_list = 'price,num_iid,pic_url,title'.split(',')
        cls.itemFields_upload = ['item_img']
        cls.itemFields_upload_item = 'url,id,created'.split(',')
        cls.img_id = 0

    def setUp(self):
        pass

    def test_get_item_list(self):
        for inputdata in self.testInputDatas_list:
            is_poped = False
            try:
                returnValue = ItemsOnsaleGet.get_item_list(inputdata['nick'])
                self.assertTrue(type(returnValue) == self.valueType_list['returnValue'], self.tcinfo)
                for i in range(len(returnValue)):
                    itemKeys = returnValue[i].keys()
                    for item in itemKeys:
                        self.assertTrue(item in self.itemFields_list, self.tcinfo)
            except Exception, e:
                is_poped = True
                self.assertRaises(inputdata['exceptionClass'])
            finally:
                self.assertEqual(inputdata['popException'],is_poped,self.tcinfo)

    def test_get_item_list_with_overview(self):
        for inputdata in self.testInputDatas_with_overview:
            is_poped = False
            try:
                returnValue = ItemsOnsaleGet.get_item_list_with_overview(inputdata['nick'])
                self.assertTrue(type(returnValue) == self.valueType_with_overview['returnValue'], self.tcinfo)
                self.assertTrue(returnValue.keys() == self.itemFields_with_overview, self.tcinfo)
                for i in range(len(returnValue['item_list'])):
                    itemKeys = returnValue['item_list'][i].keys()
                    for item in itemKeys:
                        self.assertTrue(item in self.itemFields_with_overview_list, self.tcinfo)
            except Exception, e:
                is_poped = True
                self.assertRaises(inputdata['exceptionClass'])
            finally:
                self.assertEqual(inputdata['popException'],is_poped,self.tcinfo)

    def test_get_item_list(self):
        for inputdata in self.testInputDatas_list:
            is_poped = False
            try:
                returnValue = ItemsOnsaleGet.get_item_list(inputdata['nick'])
                self.assertTrue(type(returnValue) == self.valueType_list['returnValue'], self.tcinfo)
                for i in range(len(returnValue)):
                    itemKeys = returnValue[i].keys()
                    for item in itemKeys:
                        self.assertTrue(item in self.itemFields_list, self.tcinfo)
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
alltests = unittest.TestLoader().loadTestsFromTestCase(TestItemsOnsaleGet)
