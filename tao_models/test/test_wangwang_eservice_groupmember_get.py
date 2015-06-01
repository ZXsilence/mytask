#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: tanglingling
@contact: tanglingling@maimiaotech.com
@date: 2015-04-02 10:54
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
from api_server.conf import set_env
set_env.getEnvReady()
from api_server.conf.settings import set_api_source

from wangwang_eservice_groupmember_get import WangwangEserviceGroupmemberGet
from tao_models.common.exceptions import TaoApiMaxRetryException
from TaobaoSdk.Exceptions import ErrorResponseException

@unittest.skipUnless('regression' in settings.RUNTYPE, "Regression Test Case")
class TestWangwangEserviceGroupmemberGet(unittest.TestCase):
    '''用某个组管理员账号查询，返回该组组名、和该组所有组成员ID（E客服的分流设置）。
    用旺旺主帐号查询，返回所有组的组名和该组所有组成员ID。 返回的组成员ID可以是多个，用 "," 隔开。 
    被查者ID只能传入一个。 组成员中排名最靠前的ID是组管理员ID'''
    @classmethod
    def setUpClass(cls):
        set_api_source('SDK_TEST')
        cls.testInputdata = [{'nick':'麦苗科技001','popException':False,'exceptionClass':None},
                             {'nick':'','popException':True,'exceptionClass':ErrorResponseException},
                             {'nick':'_nick_not_exsits_','popException':True,'exceptionClass':ErrorResponseException}
                             ]
        cls.errs = {'type_error':'return type error','value_error':'return value error','except':'assert except'}
    def test_get_group_member_list(self):
        for inputdata in self.testInputdata:
            is_poped = False
            try:
                activity_list = WangwangEserviceGroupmemberGet.get_group_member_list(inputdata['nick'])
                self.assertEqual(type(activity_list), list, self.errs['type_error'])
                self.assertGreaterEqual(len(activity_list), 1, self.errs['value_error'])
            except Exception , e:
                is_poped = True
                self.assertRaises(inputdata['exceptionClass'])
            finally:
                self.assertEqual(is_poped , inputdata['popException'],self.errs['except'])

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == '__main__':                                                       
    unittest.main()
alltests = unittest.TestLoader().loadTestsFromTestCase(TestWangwangEserviceGroupmemberGet)
