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

@unittest.skipUnless('regression' in settings.RUNTYPE, "Regression Test Case")
class TestSimbaRptCampadgroupBaseEffectGet(unittest.TestCase):
    '''
    simba_rpt_campadgroupbase_get推广计划下的推广组报表基础数据查询(只有汇总数据，无分类类型) 
    simba_rpt_campadgroupeffect_get推广计划下的推广组报表效果数据查询(只有汇总数据，无分类类型) 
    '''
    @classmethod
    def setUpClass(cls):
        set_api_source('SDK_TEST')
        start = datetime.datetime(2015,4,1)
        end = datetime.datetime(2015,4,8)
        cls.testData = [{'nick':'zhangyu_xql','campaign_id':6765909,'adgroup_id':368440092,'search_type':'SEARCH,CAT','source':'1,2','start':start,'end':end,'popException':False,'exceptClass':None},
                        {'nick':'','campaign_id':6765909,'adgroup_id':368440092,'search_type':'SEARCH,CAT','source':'1,2','start':start,'end':end,'popException':True,'exceptClass':SDKRetryException},
                        ]
        cls.errs={'effect_error':'error find in API: simba_rpt_campadgroupeffect_get',
                  'base_error':'error find in API: simba_rpt_campadgroupbase_get',
                  'assert_error':'assert exception',
                  }
    
    def seUp(self):
        pass
    def test_get_rpt_adgroupbase_list(self):
        for inputdata in self.testData:
            is_popped = False
            try:
                res = SimbaRptCampadgroupBaseGet.get_rpt_adgroupbase_list(inputdata['nick'], inputdata['campaign_id'],inputdata['start'], inputdata['end'], inputdata['search_type'],inputdata['source'])
                self.assertEqual(type(res), list, self.errs['base_error'])
                self.assertGreater(len(res),0,self.errs['base_error'])

                res =  SimbaRptCampadgroupEffectGet.get_rpt_adgroupeffect_list(inputdata['nick'], inputdata['campaign_id'],inputdata['start'],inputdata['end'],inputdata['search_type'],inputdata['source'])
                self.assertEqual(type(res), list, self.errs['effect_error'])
                self.assertGreater(len(res), 0 , self.errs['effect_error'])

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

alltests = unittest.TestLoader().loadTestsFromTestCase(TestSimbaRptCampadgroupBaseEffectGet)
