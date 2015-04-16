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
from clouddata_mbp_data_get_normal import ClouddataMbpDataGet
from TaobaoSdk.Exceptions import ErrorResponseException

@unittest.skipUnless('regression' in settings.RUNTYPE, "Regression Test Case")
class TestClouddataMbpDataGet(unittest.TestCase):
    '''
    taobao.clouddata.mbp.data.get
    ISV通过该接口可以获取自己在MBP中开发的数据表中的数据
    '''
    @classmethod
    def setUpClass(cls):
        set_api_source('SDK_TEST')
        cls.tcinfo = 'API Test - taobao.clouddata.mbp.data.get'
        cls.testInputDatas = [{'sql_id':7394, 'query_dict':{},'popException':True, 'exceptionClass':ErrorResponseException},
                              {'sql_id':7394, 'query_dict':{'shop_id': 1454483},'popException':False, 'exceptionClass':None}
                              ]
        cls.valueType = {'returnValue':list}

    def setUp(self):
        pass

    def testGetDataFromClouddata(self):
        sdate = datetime.datetime.now() - datetime.timedelta(1)
        edate = datetime.datetime.now()
        sdate_str = sdate.strftime("%Y%m%d")
        edate_str = edate.strftime("%Y%m%d")
        for inputdata in self.testInputDatas:
            query_dict = inputdata['query_dict']
            query_dict.update({"dt1":sdate_str, "dt2":edate_str, "sdate":sdate_str, "edate":edate_str})
            is_poped = False
            try:
                returnValue = ClouddataMbpDataGet.get_data_from_clouddata(inputdata['sql_id'], query_dict)
                self.assertTrue(type(returnValue) == self.valueType['returnValue'], self.tcinfo)
            except Exception, e:
                is_poped = True
                self.assertRaises(inputdata['exceptionClass'])
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
alltests = unittest.TestLoader().loadTestsFromTestCase(TestClouddataMbpDataGet)
