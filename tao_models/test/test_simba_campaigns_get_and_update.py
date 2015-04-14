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

from simba_campaigns_get import SimbaCampaignsGet
from simba_campaign_update import SimbaCampaignUpdate
from tao_models.common.exceptions import TaoApiMaxRetryException
from tao_models.common.exceptions import InvalidAccessTokenException
from TaobaoSdk.Exceptions import ErrorResponseException
@unittest.skipUnless('regression' in settings.RUNTYPE, "Regression Test Case")
class TestSimbaCampaignsGet(unittest.TestCase):
    '''
    taobao.simba.campaigns.get
    取得一个客户的推广计划
    taobao.simba.campaign.update
    更新一个推广计划，可以设置推广计划名字，修改推广计划上下线状态
    '''
    @classmethod
    def setUpClass(cls):
        set_api_source('SDK_TEST')
        cls.tcinfo = 'API Test - taobao.simba.campaigns.get'
        cls.tcinfo_update = 'API Test - taobao.simba.campaign.update'
        cls.testInputDatas_get = [{'nick': '__NotExistNick__','popException':True, 'exceptionClass':InvalidAccessTokenException},
                                  {'nick': 'chinchinstyle','popException':False, 'exceptionClass':None}
                                  ]
        cls.testInputDatas_update = [{'nick': '__NotExistNick__','campaign_id':None,'title':None,'online_status':None,'popException':True, 'exceptionClass':InvalidAccessTokenException},
                                     {'nick': 'chinchinstyle','campaign_id':9214487,'title':None,'online_status':None,'popException':True, 'exceptionClass':ErrorResponseException},
                                     {'nick': 'chinchinstyle','campaign_id':None,'title':'API测试','online_status':'offline','popException':False, 'exceptionClass':None}
                                     ]
        cls.valueType = {'returnValue':list, 'returnValue_item':dict,'returnValue_update':dict}
        cls.itemFields = ['online_status','title', 'settle_status', 'campaign_id', 'modified_time', 'nick' ,'create_time', 'settle_reason']

    def setUp(self):
        pass

    def test_get_campaign(self):
        for inputdata in self.testInputDatas_get:
            self.tcinfo = 'API Test - taobao.simba.campaigns.get'
            self.tcinfo += str(inputdata)
            is_poped = False
            try:
                returnValue = SimbaCampaignsGet.get_campaign_list(inputdata['nick'])
                self.assertTrue(type(returnValue) == self.valueType['returnValue'], self.tcinfo)
                for item in returnValue:
                    self.assertTrue(type(item) == self.valueType['returnValue_item'], self.tcinfo)
                    itemKeys = item.keys()
                    for key in itemKeys:
                        self.assertTrue(key in self.itemFields, self.tcinfo)
                    self.campaign_id = item['campaign_id']
            except Exception, e:
                is_poped = True
                self.assertRaises(inputdata['exceptionClass'])
            finally:
                self.assertEqual(inputdata['popException'],is_poped,self.tcinfo)

        for inputdata in self.testInputDatas_update:
            self.tcinfo_update = 'API Test - taobao.simba.campaign.update'
            self.tcinfo_update += str(inputdata)
            is_poped = False
            try:
                if inputdata['campaign_id'] == None:
                    campaign_id = self.campaign_id
                else:
                    campaign_id = inputdata['campaign_id']
                returnValue = SimbaCampaignUpdate.update_campaign(inputdata['nick'], campaign_id,inputdata['title'], inputdata['online_status'])
                self.assertTrue(type(returnValue) == self.valueType['returnValue_update'], self.tcinfo_update)
                itemKeys = returnValue.keys()
                for key in itemKeys:
                    self.assertTrue(key in self.itemFields, self.tcinfo_update)
                self.campaign_id = item['campaign_id']
            except Exception, e:
                is_poped = True
                self.assertRaises(inputdata['exceptionClass'])
            finally:
                self.assertEqual(inputdata['popException'],is_poped,self.tcinfo_update)

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
alltests = unittest.TestLoader().loadTestsFromTestCase(TestSimbaCampaignsGet)
