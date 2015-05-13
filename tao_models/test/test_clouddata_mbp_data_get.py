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
from datetime import datetime,timedelta
import logging
import logging.config
import unittest
from api_server.conf import set_env
set_env.getEnvReady()
from simba_adgroup_add import SimbaAdgroupAdd
from simba_adgroupsbycampaignid_get import SimbaAdgroupsbycampaignidGet
from api_server.conf.settings import set_api_source
from clouddata_mbp_data_get import ClouddataMbpDataGet

@unittest.skipUnless('regression' in settings.RUNTYPE, "Regression Test Case")
class TestClouddataMbpDataGet(unittest.TestCase):
    '''
    taobao.clouddata.mbp.data.get
    '''
    @classmethod
    def setUpClass(cls):
        set_api_source('SDK_TEST')
        cls.nick = 'chinchinstyle'
        cls.campaign_id = 3328400
        cls.item_id = 7794896442
        cls.title = '创意API测试'
        cls.img_url = 'http://img02.taobaocdn.com/bao/uploaded/i2/10325023735715939/T1SF40XyNaXXXXXXXX_!!0-item_pic.jpg'
        cls.tcinfo = 'API Test - taobao.clouddata.mbp.data.get'
        cls.testInputDatas = [{'sid':62847885,'sdate':3,'edate':1,'popException':False, 'exceptionClass':None},
                              ]
        cls.valueType = {'returnValue':list}

    def setUp(self):
        pass

    def test_get_items_rpt_by_sid(self):
        now = datetime.now()
        for inputdata in self.testInputDatas:
            is_poped = False
            sdate = now - timedelta(days=inputdata['sdate'])
            edate = now - timedelta(days=inputdata['edate'])
            try:
                returnValue = ClouddataMbpDataGet.get_items_rpt_by_sid(inputdata['sid'],sdate,edate)
                self.assertEqual(type(returnValue), list, self.tcinfo)
            except Exception, e:
                is_poped = True
                self.assertRaises(inputdata['exceptionClass'])
            finally:
                self.assertEqual(inputdata['popException'], is_poped, self.tcinfo)


    def test_get_item_rpt(self):
        try:
            self.adgroup_id = None
            adgroups = SimbaAdgroupsbycampaignidGet.get_adgroup_list_by_campaign(self.nick, self.campaign_id)
            for adgroup in adgroups:
                if adgroup['num_iid'] == self.item_id:
                    self.adgroup_id = adgroup['adgroup_id']
                    break
            if not self.adgroup_id:
                returnValue = SimbaAdgroupAdd.add_adgroup(self.nick,self.campaign_id,self.item_id,1000,self.title,self.img_url)
                self.adgroup_id = returnValue['adgroup_id']
        except Exception,e:
            self.assertTrue(False, "准备数据出错，无法执行")
        now = datetime.now()
        for inputdata in self.testInputDatas:
            is_poped = False
            sdate = now - timedelta(days=inputdata['sdate'])
            edate = now - timedelta(days=inputdata['edate'])
            try:
                returnValue = ClouddataMbpDataGet.get_item_rpt(self.item_id,sdate,edate)
                self.assertEqual(type(returnValue), list, self.tcinfo)
            except Exception, e:
                is_poped = True
                self.assertRaises(inputdata['exceptionClass'])
            finally:
                self.assertEqual(inputdata['popException'], is_poped, self.tcinfo)

            try:
                returnValue = ClouddataMbpDataGet.get_item_rpt_sum(self.item_id)
                self.assertEqual(type(returnValue), list, self.tcinfo)
            except Exception, e:
                is_poped = True
                self.assertRaises(inputdata['exceptionClass'])
            finally:
                self.assertEqual(inputdata['popException'], is_poped, self.tcinfo)

            try:
                returnValue = ClouddataMbpDataGet.get_item_rpt_sum(self.item_id)
                self.assertEqual(type(returnValue), list, self.tcinfo)
            except Exception, e:
                is_poped = True
                self.assertRaises(inputdata['exceptionClass'])
            finally:
                self.assertEqual(inputdata['popException'], is_poped, self.tcinfo)


            try:
                returnValue = ClouddataMbpDataGet.get_items_page_pc_rpt_by_sid(inputdata['sid'],sdate,edate)
                self.assertEqual(type(returnValue), dict, self.tcinfo)
            except Exception, e:
                is_poped = True
                self.assertRaises(inputdata['exceptionClass'])
            finally:
                self.assertEqual(inputdata['popException'], is_poped, self.tcinfo)

            try:
                returnValue = ClouddataMbpDataGet.get_item_page_pc_rpt(self.item_id,sdate,edate)
                self.assertEqual(type(returnValue), list, self.tcinfo)
            except Exception, e:
                is_poped = True
                self.assertRaises(inputdata['exceptionClass'])
            finally:
                self.assertEqual(inputdata['popException'], is_poped, self.tcinfo)
            
            try:
                returnValue = ClouddataMbpDataGet.get_query_rpt(inputdata['sid'],sdate,edate)
                self.assertEqual(type(returnValue), list, self.tcinfo)
            except Exception, e:
                is_poped = True
                self.assertRaises(inputdata['exceptionClass'])
            finally:
                self.assertEqual(inputdata['popException'], is_poped, self.tcinfo)

            try:
                returnValue = ClouddataMbpDataGet.get_query_list_by_sid(inputdata['sid'])
                self.assertEqual(type(returnValue), list, self.tcinfo)
            except Exception, e:
                is_poped = True
                self.assertRaises(inputdata['exceptionClass'])
            finally:
                self.assertEqual(inputdata['popException'], is_poped, self.tcinfo)

            try:
                returnValue = ClouddataMbpDataGet.get_query_list_by_sid(inputdata['sid'])
                self.assertEqual(type(returnValue), list, self.tcinfo)
            except Exception, e:
                is_poped = True
                self.assertRaises(inputdata['exceptionClass'])
            finally:
                self.assertEqual(inputdata['popException'], is_poped, self.tcinfo)
            
            try:
                returnValue = ClouddataMbpDataGet.get_shop_plot_data(inputdata['sid'],sdate,edate)
                self.assertEqual(type(returnValue), list, self.tcinfo)
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
