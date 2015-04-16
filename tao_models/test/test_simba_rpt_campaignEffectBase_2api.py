#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: tanglingling
@contact: tanglingling@maimiaotech.com
@date: 2015-04-08 13:22
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
from tao_models.common.exceptions import W2securityException, InvalidAccessTokenException#导入异常类
from simba_rpt_campaignbase_get import SimbaRptCampaignbaseGet
from simba_rpt_campaigneffect_get import SimbaRptCampaigneffectGet


@unittest.skipUnless('regression' in settings.RUNTYPE, "Regression Test Case")
class TestSimbaRptCampaigneffectbaseGet(unittest.TestCase):
    '''
    effet:推广计划效果报表数据对象 
    base:推广计划报表基础数据对象 
    '''
    @classmethod
    def setUpClass(cls):
        set_api_source('SDK_TEST')
        cls.testDataBase = [{'nick':'zhangyu_xql','campaign_id':6765909,'search_type':'SEARCH,CAT','source':'1,2','start':datetime.datetime(2015,4,5),'end':datetime.datetime(2015,4,8),'popException':False,'exceptClass':None},
                            {'nick':'','campaign_id':6765909,'search_type':'SEARCH,CAT','source':'1,2','start':datetime.datetime(2015,4,5),'end':datetime.datetime(2015,4,8),'popException':True,'exceptClass':ErrorResponseException},
                            {'nick':'zhangyu_xql','campaign_id':0,'search_type':'SEARCH,CAT','source':'1,2','start':datetime.datetime(2015,4,5),'end':datetime.datetime(2015,4,8),'popException':False,'exceptClass':None},
                            ]
        cls.errs={'effet_error':'error found in API: simba_rpt_campaigneffect_get',
                  'base_error':'error found in API: simba_rpt_campaignbase_get',
                  'assert_error':'assert exception',
                  }
    
    def seUp(self):
        pass
    def test_get_user_seller(self):
        for inputdata in self.testDataBase:
            is_popped = False
            try:
                res =  SimbaRptCampaignbaseGet.get_camp_rpt_list_by_date(inputdata['nick'], inputdata['campaign_id'],inputdata['search_type'], inputdata['source'], inputdata['start'],inputdata['end'])
                self.assertEqual(type(res), list ,self.errs['base_error'])
                if inputdata['campaign_id'] == 0:
                    self.assertEqual( len(res) , 0 , self.errs['base_error'])
                else:
                    self.assertGreater( len(res) , 0 , self.errs['base_error'])

                res = SimbaRptCampaigneffectGet.get_campaign_effect_accumulate(inputdata['nick'], inputdata['campaign_id'],inputdata['search_type'], inputdata['source'], inputdata['start'],inputdata['end'])
                self.assertEqual( type(res), dict , self.errs['effet_error'])
                if inputdata['campaign_id'] ==0:
                    self.assertEqual( res['pay'],0,self.errs['effet_error'])
                    self.assertEqual( res['fav'],0,self.errs['effet_error'])
                    self.assertEqual( res['pay_count'],0,self.errs['effet_error'])
                else:
                    self.assertNotEqual( res['pay'],0,self.errs['effet_error'])
                    self.assertNotEqual( res['fav'],0,self.errs['effet_error'])
                    self.assertNotEqual( res['pay_count'],0,self.errs['effet_error'])

            except Exception, e:
                is_popped = True
                self.assertRaises(inputdata['exceptClass'])
            finally:
                self.assertEqual(is_popped,inputdata['popException'],self.errs['assert_error'])


    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == '__main__':
    unittest.main()

alltests = unittest.TestLoader().loadTestsFromTestCase(TestSimbaRptCampaigneffectbaseGet)
