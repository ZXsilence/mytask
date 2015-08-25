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

from simba_adgroup_onlineitemsvon_get import SimbaAdgroupOnlineitemsvonGet
from tao_models.common.exceptions import TaoApiMaxRetryException
from tao_models.common.exceptions import InvalidAccessTokenException
from TaobaoSdk.Exceptions import ErrorResponseException
@unittest.skipUnless('regression' in settings.RUNTYPE, "Regression Test Case")
class TestSimbaAdgroupOnlineitemsvonGet(unittest.TestCase):
    '''
    taobao.simba.adgroup.onlineitemsvon.get
    获取用户上架在线销售的全部宝贝
    '''
    @classmethod
    def setUpClass(cls):
        set_api_source('SDK_TEST')
        cls.tcinfo = 'API Test - taobao.simba.adgroup.onlineitemsvon.get'
        cls.testInputDatas = [{'nick': '__NotExistNick__','popException':True, 'exceptionClass':InvalidAccessTokenException},
                                  {'nick': 'chinchinstyle','popException':False, 'exceptionClass':None}
                                  ]
        cls.valueType = {'returnValue':dict, 'item_list':list,'total_item':int,'returnValue_list_item':dict}
        cls.itemFields = ['item_list','total_item']
        cls.itemFields_list_item = ['extra_attributes','price','num_id','title','img_url']

    def setUp(self):
        pass

    def test_get_adgroups_changed(self):
        for inputdata in self.testInputDatas:
            self.tcinfo = 'API Test - taobao.simba.adgroup.onlineitemsvon.get'
            self.tcinfo += str(inputdata)
            is_poped = False
            try:
                returnValue = SimbaAdgroupOnlineitemsvonGet.get_items_online_with_overview(inputdata['nick'])
                self.assertTrue(type(returnValue) == self.valueType['returnValue'], self.tcinfo)
                itemKeys = returnValue.keys()
                for item in itemKeys:
                    self.assertTrue(item in self.itemFields, self.tcinfo)
                    self.assertTrue(type(returnValue[item]) == self.valueType[item], self.tcinfo)
                item_list = returnValue['item_list']
                for item in item_list:
                    self.assertTrue(type(item) == self.valueType['returnValue_list_item'], self.tcinfo)
                    itemKeys = item.keys()
                    for key in itemKeys:
                        self.assertTrue(key in self.itemFields_list_item, self.tcinfo)
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
alltests = unittest.TestLoader().loadTestsFromTestCase(TestSimbaAdgroupOnlineitemsvonGet)
