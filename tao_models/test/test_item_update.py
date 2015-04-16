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

from item_update import ItemUpdate
from tao_models.common.exceptions import TaoApiMaxRetryException
from TaobaoSdk.Exceptions import ErrorResponseException
@unittest.skipUnless('regression' in settings.RUNTYPE, "Regression Test Case")
class TestItemUpdate(unittest.TestCase):
    '''
    taobao.item.update
    更新商品信息
    '''
    @classmethod
    def setUpClass(cls):
        set_api_source('SDK_TEST')
        cls.tcinfo = 'API Test - taobao.item.update'
        cls.testInputDatas_desc = [{'nick':'麦苗科技001','num_iid': 35402689713,'desc':'添加描述了啊dd','popException':True, 'exceptionClass':ErrorResponseException},
                                   {'nick':'chinchinstyle','num_iid': 35402689713,'desc':'添加描述', 'popException':True, 'exceptionClass':ErrorResponseException},
                                   {'nick':'chinchinstyle','num_iid': 35402689713,'desc':'添加描述了啊dd', 'popException':False, 'exceptionClass':None}
                                  ]
        #cls.testInputDatas_desc_modules = [{'nick':'麦苗科技001','num_iid': 35402689713,'desc':'添加描述了啊dd','popException':True, 'exceptionClass':ErrorResponseException},
        #                                   {'nick':'chinchinstyle','num_iid': 35402689713,'desc':'添加描述', 'popException':True, 'exceptionClass':ErrorResponseException},
        #                                   {'nick':'chinchinstyle','num_iid': 35402689713,'desc':'添加描述了啊dd', 'popException':False, 'exceptionClass':None}
        #                                   ]
        cls.valueType = {'returnValue_desc':dict, 'returnValue_info':dict}
        cls.itemFields = 'iid,num_iid,modified'.split(',')

    def setUp(self):
        pass

    def test_update_item_desc(self):
        for inputdata in self.testInputDatas_desc:
            is_poped = False
            try:
                returnValue = ItemUpdate.update_item_desc(inputdata['nick'],inputdata['num_iid'],inputdata['desc'])
                self.assertTrue(type(returnValue) == self.valueType['returnValue_desc'], self.tcinfo)
            except Exception, e:
                is_poped = True
                self.assertRaises(inputdata['exceptionClass'])
            finally:
                self.assertEqual(inputdata['popException'],is_poped,self.tcinfo)

    #def test_update_item_desc_by_desc_modules(self):
    #    for inputdata in self.testInputDatas_info:
    #        is_poped = False
    #        try:
    #            returnValue = ItemGet.get_item_info(inputdata['num_iid'])
    #            self.assertTrue(type(returnValue) == self.valueType['returnValue_info'], self.tcinfo)
    #            itemKeys = returnValue.keys()
    #            for item in self.itemFields:
    #                self.assertTrue(item in self.itemFields, self.tcinfo)
    #        except Exception, e:
    #            is_poped = True
    #            self.assertRaises(inputdata['exceptionClass'])
    #        finally:
    #            self.assertEqual(inputdata['popException'],is_poped,self.tcinfo)

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
alltests = unittest.TestLoader().loadTestsFromTestCase(TestItemUpdate)
