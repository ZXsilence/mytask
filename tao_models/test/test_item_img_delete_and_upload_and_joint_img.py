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

from item_img_delete import ItemImgDelete
from item_img_upload import ItemImgUpload
from item_joint_img import ItemJointImg
from tao_models.common.exceptions import TaoApiMaxRetryException
from TaobaoSdk.Exceptions import ErrorResponseException
@unittest.skipUnless('regression' in settings.RUNTYPE, "Regression Test Case")
class TestItemImgDelete(unittest.TestCase):
    '''
    taobao.item.img.delete
    删除itemimg_id 所指定的商品图片 传入的num_iid所对应的商品必须属于当前会话的用户 itemimg_id对应的图片需要属于num_iid对应的商品
    taobao.item.img.upload
    添加一张商品图片到num_iid指定的商品中 传入的num_iid所对应的商品必须属于当前会话的用户 如果更新图片需要设置itemimg_id，且该itemimg_id的图片记录需要属于传入的num_iid对应的商品。如果新增图片则不用设置 商品图片有数量和大小上的限制，根据卖家享有的服务（如：卖家订购了多图服务等），商品图片数量限制不同
    当前只测试新增图片，不测试更改图片
    taobao.item.joint.img
    关联一张商品图片到num_iid指定的商品中
    .传入的num_iid所对应的商品必须属于当前会话的用户 
    .商品图片关联在卖家身份和图片来源上的限制，卖家要是B卖家或订购了多图服务才能关联图片，并且图片要来自于卖家自己的图片空间才行
    .商品图片数量有限制。不管是上传的图片还是关联的图片，他们的总数不能超过一定限额
    '''
    @classmethod
    def setUpClass(cls):
        set_api_source('SDK_TEST')
        cls.tcinfo_delete = 'API Test - taobao.item.img.delete'
        cls.tcinfo_upload = 'API Test - taobao.item.img.upload'
        cls.tcinfo_joint_img = 'API Test - taobao.item.joint.img'
        cls.testInputDatas_delete = [{'nick':'麦苗科技001','num_iid':35402689713,'popException':True, 'exceptionClass':ErrorResponseException},
                                     {'nick':'chinchinstyle','num_iid':35402689713,'popException':False, 'exceptionClass':None}
                                     ]
        cls.testInputDatas_upload = [{'nick':'麦苗科技001','num_iid':35402689713,'image_path':'/alidata1/sdk_test/test.jpg','popException':True, 'exceptionClass':ErrorResponseException},
                                     {'nick':'chinchinstyle','num_iid':35402689713,'image_path':'/alidata1/sdk_test/test.jpg','popException':False, 'exceptionClass':None}
                                     ]
        cls.testInputDatas_joint_img = [{'nick':'麦苗科技001','num_iid':8000023898,'image_path':'i1/520500325/T2ZBhTXXNbXXXXXXXX_!!520500325.jpg','popException':True, 'exceptionClass':ErrorResponseException},
                                     {'nick':'chinchinstyle','num_iid':8000023898,'image_path':'/i1/52055/T2ZBhTXXNbXXXXXX_!!5205025.jpg','popException':True, 'exceptionClass':ErrorResponseException},
                                     {'nick':'麦苗科技001','num_iid':21579352934,'image_path':'i1/871727117/TB2eaLvsFXXXXaEXpXXXXXXXXXX_!!871727117.jpg','popException':False, 'exceptionClass':None}
                                     ]
        cls.valueType = {'returnValue':dict}
        cls.itemFields_delete = 'created,id'.split(',')
        cls.itemFields_upload = ['item_img']
        cls.itemFields_upload_item = 'url,id,created'.split(',')
        cls.img_id = 0

    def setUp(self):
        pass

    def test_delete_and_upload_img(self):
        for inputdata in self.testInputDatas_upload:
            is_poped = False
            try:
                returnValue = ItemImgUpload.upload_img(inputdata['nick'],inputdata['num_iid'],inputdata['image_path'])
                self.assertTrue(type(returnValue) == self.valueType['returnValue'], self.tcinfo_upload)
                itemKeys = returnValue['item_img'].keys()
                for item in itemKeys:
                    self.assertTrue(item in self.itemFields_upload_item, self.tcinfo_upload)
                self.img_id = returnValue['item_img']['id']
            except Exception, e:
                is_poped = True
                self.assertRaises(inputdata['exceptionClass'])
            finally:
                self.assertEqual(inputdata['popException'],is_poped,self.tcinfo_upload)
        for inputdata in self.testInputDatas_delete:
            is_poped = False
            try:
                returnValue = ItemImgDelete.delete_item_img(inputdata['nick'],inputdata['num_iid'], self.img_id)
                self.assertTrue(type(returnValue) == self.valueType['returnValue'], self.tcinfo_delete)
                itemKeys = returnValue.keys()
                for item in itemKeys:
                    self.assertTrue(item in self.itemFields_delete, self.tcinfo_delete)
            except Exception, e:
                is_poped = True
                self.assertRaises(inputdata['exceptionClass'])
            finally:
                self.assertEqual(inputdata['popException'],is_poped,self.tcinfo_delete)


    def test_joint_img(self):
        for inputdata in self.testInputDatas_joint_img:
            is_poped = False
            try:
                returnValue = ItemJointImg.joint_img(inputdata['nick'],inputdata['num_iid'],inputdata['image_path'])
                self.assertTrue(type(returnValue) == self.valueType['returnValue'], self.tcinfo_joint_img)
                itemKeys = returnValue.keys()
                for item in itemKeys:
                    self.assertTrue(item in self.itemFields_upload_item, self.tcinfo_joint_img)
                self.img_id = returnValue['id']
                try:
                    returnValue = ItemImgDelete.delete_item_img(inputdata['nick'],inputdata['num_iid'], self.img_id)
                except Exception, e:
                    self.assertTrue(False, "Delete joint_img img file")
            except Exception, e:
                is_poped = True
                self.assertRaises(inputdata['exceptionClass'])
            finally:
                self.assertEqual(inputdata['popException'],is_poped,self.tcinfo_joint_img)
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
alltests = unittest.TestLoader().loadTestsFromTestCase(TestItemImgDelete)
