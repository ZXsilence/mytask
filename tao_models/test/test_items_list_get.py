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

from items_list_get import ItemsListGet
from tao_models.common.exceptions import TaoApiMaxRetryException
from TaobaoSdk.Exceptions import ErrorResponseException
@unittest.skipUnless('regression' in settings.RUNTYPE, "Regression Test Case")
class TestItemsListGet(unittest.TestCase):
    '''
    taobao.items.list.get
    查看非公开属性时需要用户登录
    '''
    @classmethod
    def setUpClass(cls):
        set_api_source('SDK_TEST')
        cls.tcinfo = 'API Test - taobao.items.list.get'
        cls.testInputDatas = [{'nick':'麦苗科技001','num_iid':[35402689713],'popException':False, 'exceptionClass':None},
                              {'nick':'chinchinstyle','num_iid':[35402689713],'popException':False, 'exceptionClass':None},
                              {'nick':'chinchinstyle','num_iid':[35402689713,8000023898],'popException':False, 'exceptionClass':None}
                              ]
        cls.valueType = {'returnValue':list}
        cls.itemFields = 'newprepay,title,price,pic_url,num_iid,detail_url,props_name,cid,delist_time,list_time,property_alias,seller_cids,freight_payer'

    def setUp(self):
        pass

    def test_joint_img(self):
        for inputdata in self.testInputDatas:
            is_poped = False
            try:
                returnValue = ItemsListGet.get_item_list(inputdata['nick'],inputdata['num_iid'])
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
alltests = unittest.TestLoader().loadTestsFromTestCase(TestItemsListGet)
