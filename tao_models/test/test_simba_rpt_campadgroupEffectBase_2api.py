#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: tanglingling
@contact: tanglingling@maimiaotech.com
@date: 2015-04-09 13:42
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
from TaobaoSdk.Exceptions import ErrorResponseException,SDKRetryException

from tao_models.common.exceptions import W2securityException, InvalidAccessTokenException#导入异常类
from simba_rpt_campadgroupbase_get import   SimbaRptCampadgroupBaseGet
from simba_rpt_campadgroupeffect_get import SimbaRptCampadgroupEffectGet
from tao_models.test.getCampaignAdgroup import GetCampaignAdgroup

@unittest.skipUnless('regression' in settings.RUNTYPE, "Regression Test Case")
class TestSimbaRptCampadgroupBaseEffectGet(unittest.TestCase):
    '''
    simba_rpt_campadgroupbase_get推广计划下的推广组报表基础数据查询(只有汇总数据，无分类类型) 
    simba_rpt_campadgroupeffect_get推广计划下的推广组报表效果数据查询(只有汇总数据，无分类类型) 
    '''
    @classmethod
    def setUpClass(cls):
        set_api_source('SDK_TEST')
        nick,campaign_id = GetCampaignAdgroup.get_has_adgroup_rpt_nick()
        print 'Test nick:',nick
        start = datetime.datetime.now()-datetime.timedelta(days=7)
        end = datetime.datetime.now()-datetime.timedelta(days=1)
        cls.testData = [{'nick':nick,'campaign_id':campaign_id,'search_type':'SEARCH,CAT','source':'1,2,4,5','start':start,'end':end,'popException':False,'exceptClass':None},
                        {'nick':'','campaign_id':campaign_id,'search_type':'SEARCH,CAT','source':'1,2,4,5','start':start,'end':end,'popException':False,'exceptClass':None},
                        {'nick':nick,'campaign_id':0,'search_type':'SEARCH,CAT','source':'1,2,4,5','start':start,'end':end,'popException':False,'exceptClass':None},
                        ]
        cls.errs={'effect_error':'error find in API: simba_rpt_campadgroupeffect_get',
                  'base_error':'error find in API: simba_rpt_campadgroupbase_get',
                  'assert_error':'assert exception',
                  }
        #如果click=0，不返回cpc
        cls.assertDefaultBase=['avgpos','ctr','adgroupid','cpm','searchtype','campaignid','nick','cost','source','date','impressions','click'] 
        cls.assertHasRPT=['favshopcount', 'directpay', 'indirectpay', 'favitemcount', 'indirectcarttotal', 'indirectpaycount', 'carttotal', 'directpaycount',                'directcarttotal']
        cls.assertDefaultEffect=['adgroupid','searchtype','source','campaignid','nick','date']
    def seUp(self):
        pass
    def test_get_rpt_adgroupbase_list(self):
        for inputdata in self.testData:
            is_popped = False
            try:
                res = SimbaRptCampadgroupBaseGet.get_rpt_adgroupbase_list(inputdata['nick'], inputdata['campaign_id'],inputdata['start'], inputdata['end'], inputdata['search_type'],inputdata['source'])
                self.assertEqual(type(res), list,"预期返回类型为list，api却返回%s类型"%(type(res),) )
                if len(res)>0:
                    for res0 in res:
                        #如果点击>0会返回cpc
                        if res0.get('click')>0:
                            self.assertTrue(res0.has_key('cpc'),'click=%s>0,但是返回值却不包含cpc'%(res0['click'],))
                        for k in self.assertDefaultBase:
                            self.assertTrue(res0.has_key(k),self.errs['base_error'])
                res =  SimbaRptCampadgroupEffectGet.get_rpt_adgroupeffect_list(inputdata['nick'], inputdata['campaign_id'],inputdata['start'],inputdata['end'],inputdata['search_type'],inputdata['source'])
                self.assertEqual(type(res), list, "预期返回类型为list，api却返回%s类型"%(type(res),))
                if len(res)>0:
                    for res0 in res:
                        #如果有有效数据时，会返回这些
                        if len(res0.keys())>6:
                            for k in self.assertHasRPT:
                                self.assertTrue(res0.has_key(k),'返回值不包含%s'%(k,))
                        for k in self.assertDefaultEffect:
                            self.assertTrue(res0.has_key(k),self.errs['effect_error'])
            except Exception, e:
                is_popped = True
                try:
                    self.assertRaises(inputdata['exceptClass'])
                except Exception, e:
                    print e
            finally:
                self.assertEqual(is_popped,inputdata['popException'],self.errs['assert_error'])


    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == '__main__':
    unittest.main()

alltests = unittest.TestLoader().loadTestsFromTestCase(TestSimbaRptCampadgroupBaseEffectGet)
