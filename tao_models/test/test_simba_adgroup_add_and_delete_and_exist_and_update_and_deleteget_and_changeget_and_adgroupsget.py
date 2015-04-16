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
#from MTextTestRunner import TextTestRunner

from api_server.conf import set_env
set_env.getEnvReady()
from api_server.conf.settings import set_api_source

from simba_adgroup_add import SimbaAdgroupAdd
from simba_adgroup_delete import SimbaAdgroupDelete
from simba_adgroups_item_exist import SimbaAdgroupsItemExist
from simba_adgroup_update import SimbaAdgroupUpdate
from simba_adgroupsbycampaignid_get import SimbaAdgroupsbycampaignidGet
from simba_adgroupids_deleted_get import SimbaAdgroupidsDeletedGet
from simba_adgroups_changed_get import SimbaAdgroupsChangedGet
from simba_adgroupsbyadgroupids_get import SimbaAdgroupsbyadgroupidsGet
from tao_models.common.exceptions import InvalidAccessTokenException
from TaobaoSdk.Exceptions import ErrorResponseException
@unittest.skipUnless('regression' in settings.RUNTYPE, "Regression Test Case")
class TestSimbaAdgroupAddandDeleteandExistandUpdate(unittest.TestCase):
    '''
    taobao.simba.adgroup.add
    创建一个推广组
    taobao.simba.adgroup.delete
    删除一个推广组
    taobao.simba.adgroups.item.exist
    判断在一个推广计划中是否已经推广了一个商品
    taobao.simba.adgroup.update
    更新一个推广组的信息
    taobao.simba.adgroupids.deleted.get
    获取删除的推广组ID
    taobao.simba.adgroups.changed.get
    分页获取修改的推广组ID和修改时间
    taobao.simba.adgroupsbyadgroupids.get
    批量得到推广组
    '''
    @classmethod
    def setUpClass(cls):
        set_api_source('SDK_TEST')
        cls.tcinfo_add = 'API Test - taobao.simba.adgroup.add'
        cls.tcinfo_delete = 'API Test - taobao.simba.adgroup.delete'
        cls.tcinfo_delete_get = 'API Test - taobao.simba.adgroupids.deleted.get'
        cls.tcinfo_exist = 'API Test - taobao.simba.adgroups.item.exist'
        cls.tcinfo_update = 'API Test - taobao.simba.adgroup.update'
        cls.tcinfo_change_get = 'API Test - taobao.simba.adgroups.changed.get'
        cls.tcinfo_adgroups_get = 'API Test - taobao.simba.adgroupsbyadgroupids.get'
        cls.testInputDatas_add = [{'nick': '__NotExistNick__','campaign_id':3328400,'item_id':7794896442,'default_price':1000,'title':'__API__Test_Title__','img_url':'http://img02.taobaocdn.com/bao/uploaded/i2/10325023735715939/T1SF40XyNaXXXXXXXX_!!0-item_pic.jpg','popException':True, 'exceptionClass':InvalidAccessTokenException},
                               {'nick': 'chinchinstyle','campaign_id':9214487,'item_id':7794896442,'default_price':1000,'title':'__API__Test_Title__','img_url':'http://img02.taobaocdn.com/bao/uploaded/i2/10325023735715939/T1SF40XyNaXXXXXXXX_!!0-item_pic.jpg','popException':True, 'exceptionClass':ErrorResponseException},
                               {'nick': 'chinchinstyle','campaign_id':3328400,'item_id':7794896442,'default_price':1000,'title':'__API__Test_Title__','img_url':'http://img02.taobaocdn.com/bao/uploaded/i2/10325023735715939/T1SF40XyNaXXXXXXXX_!!0-item_pic.jpg','popException':False, 'exceptionClass':None},
                               {'nick': 'chinchinstyle','campaign_id':3328400,'item_id':7794896442,'default_price':1000,'title':'__API__Test_Title__','img_url':'http://img02.taobaocdn.com/bao/uploaded/i2/10325023735715939/T1SF40XyNaXXXXXXXX_!!0-item_pic.jpg','popException':True, 'exceptionClass':ErrorResponseException},
                                ]
        cls.testInputDatas_exist = [{'nick':'__NotExistNick__','campaign_id':3328400,'item_id':7794896442,'returnValue':True,'popException':True,'exceptionClass':InvalidAccessTokenException},
                                    {'nick':'chinchinstyle','campaign_id':3328400, 'item_id':7794896442,'returnValue':True,'popException':False,'exceptionClass':None},
                                    {'nick':'chinchinstyle','campaign_id':3328400, 'item_id':26807528089,'returnValue':False,'popException':False,'exceptionClass':None},
                                    ]
        cls.testInputDatas_update = [{'nick': '__NotExistNick__','adgroup_id':3328400,'default_price':1000,'online_status':'online','popException':True, 'exceptionClass':InvalidAccessTokenException},
                                     {'nick': 'chinchinstyle','adgroup_id':3328,'default_price':1000,'online_status':'online','popException':True, 'exceptionClass':ErrorResponseException},
                                     {'nick': 'chinchinstyle','adgroup_id':None,'default_price':1000,'online_status':'online','popException':False, 'exceptionClass':None},
                                     {'nick': 'chinchinstyle','adgroup_id':None,'default_price':1000,'online_status':'offline','popException':False, 'exceptionClass':None},
                                     ]
        cls.testInputDatas_adgroups_get = [{'nick': '__NotExistNick__','adgroup_ids':[3328400],'popException':True, 'exceptionClass':InvalidAccessTokenException},
                                           {'nick': 'chinchinstyle','adgroup_ids':[11],'popException':False, 'exceptionClass':None},
                                           {'nick': 'chinchinstyle','adgroup_ids':[None],'popException':False, 'exceptionClass':None},
                                           {'nick': 'chinchinstyle','adgroup_ids':[11,11],'popException':False,'exceptionClass':None},
                                           ]
        cls.testInputDatas_delete = [{'nick':'__NotExistNick__','adgroup_id':0,'popException':True, 'exceptionClass':InvalidAccessTokenException},
                                     {'nick':'chinchinstyle', 'adgroup_id':484009681,'popException':True,'exceptionClass':ErrorResponseException},
                                     {'nick':'chinchinstyle', 'adgroup_id':None,'popException':False,'exceptionClass':None},
                                     {'nick':'chinchinstyle', 'adgroup_id':None,'popException':True,'exceptionClass':ErrorResponseException},
                                     ]
        cls.testInputDatas_deleted_get = [{'nick':'__NotExistNick__','start_time':1,'popException':True, 'exceptionClass':InvalidAccessTokenException},
                                          {'nick':'chinchinstyle','start_time':33,'popException':True, 'exceptionClass':ErrorResponseException},
                                          {'nick':'chinchinstyle','start_time':1,'popException':False, 'exceptionClass':None},
                                          ]
        cls.testInputDatas_change_get = [{'nick':'__NotExistNick__','start_time':1,'popException':True, 'exceptionClass':InvalidAccessTokenException},
                                          {'nick':'chinchinstyle','start_time':33,'popException':True, 'exceptionClass':ErrorResponseException},
                                          {'nick':'chinchinstyle','start_time':1,'popException':False, 'exceptionClass':None},
                                         ]
        cls.valueType = {'AddandDelete':dict,'exist':bool,'deleted_get':list,'deleted_get_item':int,'changed_get':list, 'changed_get_item':dict,'adgroups_get':list,'adgroups_get_item':dict}
        cls.itemFields = 'default_price,online_status,num_iid,campaign_id,modified_time,category_ids,nick,create_time,offline_type,adgroup_id'.split(',')
        cls.itemFields_update = ['default_price','nick','adgroup_id','online_status']
        cls.itemFields_changed_get = ['nick','adgroup_id','modified_time']
        cls.itemFields_adgrouops_get = ['nick','adgroup_id','modified_time','default_price','online_status','num_iid','campaign_id','category_ids','create_time','offline_type']

    def setUp(self):
        pass

    def test_simba_adgroup_add_delete_exist_update(self):
        for inputdata in self.testInputDatas_add:
            is_poped = False
            self.tcinfo_add = 'API Test - taobao.simba.adgroup.add'
            self.tcinfo_add = self.tcinfo_add+str(inputdata)
            try:
                try:
                    if not inputdata['popException']:
                        adgroups = SimbaAdgroupsbycampaignidGet.get_adgroup_list_by_campaign(inputdata['nick'],inputdata['campaign_id'])
                        for adgroup in adgroups:
                            if adgroup['num_iid'] == inputdata['item_id']:
                                SimbaAdgroupDelete.delete_adgroup(inputdata['nick'],adgroup['adgroup_id'])
                                break
                except Exception,e:
                    self.assertTrue(False, "准备数据出错，无法执行")
                finally:
                    self.assertTrue(True, "准备数据完成")
                returnValue = SimbaAdgroupAdd.add_adgroup(inputdata['nick'],inputdata['campaign_id'],inputdata['item_id'],inputdata['default_price'],inputdata['title'],inputdata['img_url'])
                self.assertTrue(type(returnValue) == self.valueType['AddandDelete'], self.tcinfo_add)
                itemKeys = returnValue.keys()
                for item in self.itemFields:
                    self.assertTrue(item in itemKeys, self.tcinfo_add)
                self.adgroup_id = returnValue['adgroup_id']
                print "add adgroup success! adgroup_id is : "+str(self.adgroup_id)
            except Exception, e:
                is_poped = True
                self.assertRaises(inputdata['exceptionClass'])
            finally:
                self.assertEqual(is_poped, inputdata['popException'], self.tcinfo_add)

        for inputdata in self.testInputDatas_exist:
            is_poped = False
            self.tcinfo_exist = 'API Test - taobao.simba.adgroups.item.exist'
            self.tcinfo_exist = self.tcinfo_exist+str(inputdata)
            try:
                returnValue = SimbaAdgroupsItemExist.is_adgroup_item_exist(inputdata['nick'],inputdata['campaign_id'],inputdata['item_id'])
                self.assertTrue(type(returnValue) == self.valueType['exist'], self.tcinfo_exist)
            except Exception, e:
                is_poped = True
                self.assertRaises(inputdata['exceptionClass'])
            finally:
                self.assertEqual(is_poped, inputdata['popException'], self.tcinfo_exist)

        for inputdata in self.testInputDatas_update:
            is_poped = False
            self.tcinfo_update = 'API Test - taobao.simba.adgroup.update'
            self.tcinfo_update = self.tcinfo_update+str(inputdata)
            try:
                if inputdata['adgroup_id']:
                    adgroup_id = inputdata['adgroup_id']
                else:
                    adgroup_id = self.adgroup_id
                returnValue = SimbaAdgroupUpdate.update_adgroup(inputdata['nick'],adgroup_id,inputdata['default_price'], inputdata['online_status'])
                self.assertTrue(type(returnValue) == self.valueType['AddandDelete'], self.tcinfo_update)
                itemKeys = returnValue.keys()
                for item in self.itemFields_update:
                    self.assertTrue(item in itemKeys, self.tcinfo_update)
            except Exception, e:
                is_poped = True
                self.assertRaises(inputdata['exceptionClass'])
            finally:
                self.assertEqual(is_poped, inputdata['popException'], self.tcinfo_update)

        for inputdata in self.testInputDatas_adgroups_get:
            is_poped = False
            index  = 0
            self.tcinfo_adgroups_get = 'API Test - taobao.simba.adgroupsbyadgroupids.get'
            self.tcinfo_adgroups_get = self.tcinfo_adgroups_get+str(inputdata)
            adgroup_ids = inputdata['adgroup_ids']
            adgroup_ids_list = []
            try:
                for adgroup_id in adgroup_ids:
                    if adgroup_id == None:
                        adgroup_id = self.adgroup_id
                    adgroup_ids_list.append(adgroup_id)
                returnValue = SimbaAdgroupsbyadgroupidsGet.get_adgroup_list_by_adgroup_ids(inputdata['nick'],adgroup_ids_list)
                self.assertTrue(type(returnValue) == self.valueType['changed_get'], self.tcinfo_adgroups_get)
                for item in returnValue:
                    if item == None:
                        self.assertFalse(adgroup_ids_list[index] == self.adgroup_id, self.tcinfo_adgroups_get)
                    else:
                        self.assertTrue(type(item) == self.valueType['changed_get_item'], self.tcinfo_adgroups_get)
                        itemKeys = item.keys()
                        for key in itemKeys:
                            self.assertTrue(key in self.itemFields_adgrouops_get, self.tcinfo_adgroups_get)
            except Exception, e:
                is_poped = True
                self.assertRaises(inputdata['exceptionClass'])
            finally:
                self.assertEqual(is_poped, inputdata['popException'], self.tcinfo_adgroups_get)

        for inputdata in self.testInputDatas_delete:
            is_poped = False
            self.tcinfo_delete = 'API Test - taobao.simba.adgroup.delete'
            self.tcinfo_delete = self.tcinfo_delete+str(inputdata)
            try:
                if inputdata['adgroup_id']:
                    adgroup_id = inputdata['adgroup_id']
                else:
                    adgroup_id = self.adgroup_id
                returnValue = SimbaAdgroupDelete.delete_adgroup(inputdata['nick'],adgroup_id)
                self.assertTrue(type(returnValue) == self.valueType['AddandDelete'], self.tcinfo_delete)
                itemKeys = returnValue.keys()
                for item in self.itemFields:
                    self.assertTrue(item in itemKeys, self.tcinfo_delete)
                self.adgroup_id = returnValue['adgroup_id']
            except Exception, e:
                is_poped = True
                self.assertRaises(inputdata['exceptionClass'])
            finally:
                self.assertEqual(is_poped, inputdata['popException'], self.tcinfo_delete)

        for inputdata in self.testInputDatas_deleted_get:
            is_poped = False
            self.tcinfo_delete_get = 'API Test - taobao.simba.adgroup.delete'
            self.tcinfo_delete_get = self.tcinfo_delete_get+str(inputdata)
            now = datetime.now()
            start_time = now - timedelta(days=inputdata['start_time'])
            try:
                returnValue = SimbaAdgroupidsDeletedGet.get_adgroupids_deleted(inputdata['nick'],start_time)
                self.assertTrue(type(returnValue) == self.valueType['deleted_get'], self.tcinfo_delete_get)
                for item in returnValue:
                    self.assertTrue(type(item) == self.valueType['deleted_get_item'], self.tcinfo_delete_get)
            except Exception, e:
                is_poped = True
                self.assertRaises(inputdata['exceptionClass'])
            finally:
                self.assertEqual(is_poped, inputdata['popException'], self.tcinfo_delete_get)

        for inputdata in self.testInputDatas_change_get:
            is_poped = False
            self.tcinfo_change_get = 'API Test - taobao.simba.adgroups.changed.get'
            self.tcinfo_change_get = self.tcinfo_change_get+str(inputdata)
            now = datetime.now()
            start_time = now - timedelta(days=inputdata['start_time'])
            try:
                returnValue = SimbaAdgroupsChangedGet.get_adgroups_changed(inputdata['nick'],start_time)
                self.assertTrue(type(returnValue) == self.valueType['changed_get'], self.tcinfo_change_get)
                for item in returnValue:
                    itemKeys = item.keys()
                    self.assertTrue(type(item) == self.valueType['changed_get_item'], self.tcinfo_change_get)
                    for key in itemKeys:
                        self.assertTrue(key in self.itemFields_changed_get, self.tcinfo_change_get)
            except Exception, e:
                is_poped = True
                self.assertRaises(inputdata['exceptionClass'])
            finally:
                self.assertEqual(is_poped, inputdata['popException'], self.tcinfo_delete_get)

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
alltests = unittest.TestLoader().loadTestsFromTestCase(TestSimbaAdgroupAddandDeleteandExistandUpdate)
