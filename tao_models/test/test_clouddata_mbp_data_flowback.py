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
from clouddata_mbp_data_flowback import ClouddataMbpDataFlowback

@unittest.skipUnless('regression' in settings.RUNTYPE, "Regression Test Case")
class TestClouddataMBPDataFlowback(unittest.TestCase):
    '''
    taobao.clouddata.mbp.data.flowback
    用户通过此接口向上传表上传数据
    '''
    @classmethod
    def setUpClass(cls):
        set_api_source('SDK_TEST')
        cls.tcinfo = 'API Test - taobao.clouddata.mbp.data.flowback'
        cls.testInputDatas = [{'table_name':'','input_data':[],'responseStatus':None,'popException':True, 'exceptionClass':None, 'expect_result':'list index out of range'},
                              {'table_name':'pri_upload.shop_id_sld_new','input_data':[{'shop_id': 57501318, 'resv':''}],'responseStatus':0, 'popException':False, 'exceptionClass':None,'expect_result':None}
                              ]
        cls.valueType = {'returnValue':''}

    def setUp(self):
        pass

    def testFlowback(self):
        for inputdata in self.testInputDatas:
            is_poped = False
            try:
                returnValue = ClouddataMbpDataFlowback.flowback_data(inputdata['table_name'], inputdata['input_data'])
                self.assertEqual(returnValue, inputdata['responseStatus'], self.tcinfo)
            except Exception, e:
                is_poped = True
                self.assertEqual(e.message, inputdata['expect_result'], self.tcinfo)
            finally:
                self.assertEqual(inputdata['popException'], is_poped, self.tcinfo)


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
alltests = unittest.TestLoader().loadTestsFromTestCase(TestClouddataMBPDataFlowback)
