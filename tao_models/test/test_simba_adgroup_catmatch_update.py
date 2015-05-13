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

from areas_get import AreasGet

@unittest.skipUnless('regression' in settings.RUNTYPE, "Regression Test Case")
class TestSimbaAdgroupCatmatchUpdate(unittest.TestCase):
    '''
    taobao.simba.adgroup.catmatch.update
    更新一个推广组的类目出价，可以设置类目出价、是否使用默认出价、是否打开类目出价
    '''
    @classmethod
    def setUpClass(cls):
        set_api_source('SDK_TEST')
        cls.tcinfo = 'API Test - taobao.simba.adgroup.catmatch.update'

    def setUp(self):
        pass


    @unittest.skip("Unconditionally skip the No Use test")
    def test_update_adgroup_catmatch(self):
        """No Use"""
        pass

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
alltests = unittest.TestLoader().loadTestsFromTestCase(TestSimbaAdgroupCatmatchUpdate)
