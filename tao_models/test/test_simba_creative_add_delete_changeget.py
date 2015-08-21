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
from api_server.conf.settings import set_api_source

from simba_adgroup_add import SimbaAdgroupAdd
from simba_adgroupsbycampaignid_get import SimbaAdgroupsbycampaignidGet
from simba_creatives_get import SimbaCreativesGet
from simba_creative_add import SimbaCreativeAdd
from simba_creative_delete import SimbaCreativeDelete
from simba_creativeids_changed_get import SimbaCreativeidsChangedGet
from tao_models.common.exceptions import TaoApiMaxRetryException
from tao_models.common.exceptions import InvalidAccessTokenException
from TaobaoSdk.Exceptions import ErrorResponseException
@unittest.skipUnless('regression' in settings.RUNTYPE, "Regression Test Case")
class TestSimbaCreativeAddAndDeleteAndChangeGet(unittest.TestCase):
    '''
    taobao.simba.creative.add
    创建一个创意
    '''
    @classmethod
    def setUpClass(cls):
        set_api_source('SDK_TEST')
        cls.nick = 'chinchinstyle'
        cls.campaign_id = 3328400
        cls.item_id = 7794896442
        cls.title = '创意API测试'
        cls.img_url = 'http://img02.taobaocdn.com/bao/uploaded/i2/10325023735715939/T1SF40XyNaXXXXXXXX_!!0-item_pic.jpg'
        cls.tcinfo_add = 'API Test - taobao.simba.creative.add'
        cls.tcinfo_delete = 'API Test - taobao.simba.creative.delete'
        cls.tcinfo_changeget = 'API Test - taobao.simba.creativeids.changed.get'
        cls.testInputDatas_add = [{'nick': '__NotExistNick__','adgroup_id':None,'title':None,'img_url':None,'popException':True, 'exceptionClass':InvalidAccessTokenException},
                                   {'nick': 'chinchinstyle','adgroup_id':11,'title':cls.title,'img_url':cls.img_url,'popException':True, 'exceptionClass':ErrorResponseException},
                                   {'nick': 'chinchinstyle','adgroup_id':None,'title':cls.title,'img_url':cls.img_url,'popException':False, 'exceptionClass':None},
                                   {'nick': 'chinchinstyle','adgroup_id':None,'title':cls.title,'img_url':cls.img_url,'popException':True, 'exceptionClass':ErrorResponseException}
                                  ]
        cls.testInputDatas_delete = [{'nick': '__NotExistNick__','creative_id':None,'popException':True, 'exceptionClass':InvalidAccessTokenException},
                                     {'nick': 'chinchinstyle','creative_id':11,'popException':True, 'exceptionClass':ErrorResponseException},
                                     {'nick': 'chinchinstyle','creative_id':None,'popException':False, 'exceptionClass':None},
                                     {'nick': 'chinchinstyle','creative_id':None,'popException':True, 'exceptionClass':ErrorResponseException}
                                     ]
        cls.testInputDatas_changeget = [{'nick': '__NotExistNick__','start_time':1,'popException':True, 'exceptionClass':InvalidAccessTokenException},
                                        {'nick': 'chinchinstyle','start_time':33,'popException':True, 'exceptionClass':ErrorResponseException},
                                        {'nick': 'chinchinstyle','start_time':1,'popException':False, 'exceptionClass':None}
                                        ]
        cls.valueType = {'returnValue_add':dict, 'returnValue_delete':dict,'returnValue_changeget':list}
        cls.itemFields_add = ['title','creative_id','nick','audit_status','img_url','adgroup_id']
        cls.itemFields_delete = ['title','creative_id','campaign_id','modified_time','nick','create_time','audit_status','img_url','adgroup_id']

    def setUp(self):
        pass

    def test_add_delete_changeget_creatives(self):
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

        try:
            creatives = SimbaCreativesGet.get_creative_list_by_adgroup(self.nick,self.adgroup_id)
        except Exception,e:
            self.assertTrue(False, "准备数据出错，无法执行")
        try:
            if len(creatives) == 4:
                SimbaCreativeDelete.delete_creative(self.nick,creatives[0]['creative_id'])
            elif len(creatives) == 2:
                SimbaCreativeAdd.add_creative(self.nick,self.adgroup_id,'add to 3',self.img_url)
            elif len(creatives) == 1:
                SimbaCreativeAdd.add_creative(self.nick,self.adgroup_id,'add to 3',self.img_url)
                SimbaCreativeAdd.add_creative(self.nick,self.adgroup_id,'add to 3',self.img_url)
        except Exception,e:
            self.assertTrue(False, "准备数据出错，无法执行")
        self.creative_id_list = []
        for inputdata in self.testInputDatas_add:
            if inputdata['adgroup_id'] == None:
                self.id = self.adgroup_id
            else:
                self.id = inputdata['adgroup_id']
            self.tcinfo_add = 'API Test - taobao.simba.creative.add'
            self.tcinfo_add += str(inputdata)
            is_poped = False
            try:
                returnValue = SimbaCreativeAdd.add_creative(inputdata['nick'],self.id,inputdata['title'],inputdata['img_url'])
                self.assertTrue(type(returnValue) == self.valueType['returnValue_add'], self.tcinfo_add)
                itemKeys = returnValue.keys()
                for key in itemKeys:
                    self.assertTrue(key in self.itemFields_add, self.tcinfo_add)
            except Exception, e:
                is_poped = True
                self.assertRaises(inputdata['exceptionClass'])
            finally:
                self.assertEqual(inputdata['popException'],is_poped,self.tcinfo_add)

        try:
            creatives = SimbaCreativesGet.get_creative_list_by_adgroup(self.nick,self.adgroup_id)
        except Exception,e:
            self.assertTrue(False, "准备数据出错，无法执行")
        for creative in creatives:
            self.creative_id_list.append(creative['creative_id'])
        for inputdata in self.testInputDatas_delete:
            if not inputdata['popException'] and inputdata['creative_id'] == None:
                self.id = self.creative_id_list.pop(0)
            else:
                self.id = inputdata['creative_id']
            self.tcinfo_delete = 'API Test - taobao.simba.creative.delete'
            self.tcinfo_delete += str(inputdata)
            is_poped = False
            try:
                returnValue = SimbaCreativeDelete.delete_creative(inputdata['nick'],self.id)
                self.assertTrue(type(returnValue) == self.valueType['returnValue_delete'], self.tcinfo_delete)
                itemKeys = returnValue.keys()
                for key in itemKeys:
                    self.assertTrue(key in self.itemFields_delete, self.tcinfo_delete)
            except Exception, e:
                is_poped = True
                self.assertRaises(inputdata['exceptionClass'])
            finally:
                self.assertEqual(inputdata['popException'],is_poped,self.tcinfo_delete)


        for inputdata in self.testInputDatas_changeget:
            self.tcinfo_changeget = 'API Test - taobao.simba.creativeids.changed.get'
            self.tcinfo_changeget += str(inputdata)
            now = datetime.now()
            start_time = now - timedelta(days=inputdata['start_time'])
            is_poped = False
            try:
                returnValue = SimbaCreativeidsChangedGet.get_creative_ids_changed(inputdata['nick'],start_time)
                self.assertTrue(type(returnValue) == self.valueType['returnValue_changeget'], self.tcinfo_changeget)
            except Exception, e:
                is_poped = True
                self.assertRaises(inputdata['exceptionClass'])
            finally:
                self.assertEqual(inputdata['popException'],is_poped,self.tcinfo_changeget)




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
alltests = unittest.TestLoader().loadTestsFromTestCase(TestSimbaCreativeAddAndDeleteAndChangeGet)
