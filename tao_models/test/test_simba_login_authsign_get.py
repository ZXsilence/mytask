#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: luxiaowen
@contact: luxiaowen@maimiaotech.com
@date: 2015-03-11 15:53
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""

import sys
import os
if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../../../comm_lib/'))
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('normal_test')

import unittest
from tao_models.simba_login_authsign_get import SimbaLoginAuthsignGet
from TaobaoSdk.Exceptions import ErrorResponseException
from tao_models.common.exceptions import InvalidAccessTokenException
class test_simba_login_authsign_get(unittest.TestCase):
    maxDiff = None
    @classmethod
    def setUpClass(cls):
        pass
    
    def setUp(self):
        pass
    
    def test_get_subway_token_with_access_token(self):
        data = [{'soft_code':'SYB', 'nick':'麦苗科技001', 'access_token':'62004155d9841cff42d5e4ceg02aa97dc7226246da446b5871727117',
                 'expect_result':'1105022720-31119527-1426061706571-88691be3'},
                {'soft_code':'SYB', 'nick':'麦苗科技001', 'access_token':'',
                 'expect_result':{'code':27,'msg':'Invalid session:session-is-blank','sub_code':'session-is-blank',
                                  'exception':'access session expired or invalid'}},
                {'soft_code':'SYB', 'nick':'麦苗科技001', 'access_token':'62004155d9841cff42d5e4ceg02aa97dc7226246da446b5871727171',
                 'expect_result':{'code':27,'msg':'Invalid session','sub_code':'sessionkey-not-generated-by-server',
                                  'sub_msg':'sessionkey-not-generated-by-server:RealSession don&apos;t belong app and user ! appKey is : 12685542 , user id is : 871727117',
                                  'exception':'access session expired or invalid'}},
                {'soft_code':'SYB', 'nick':'麦苗科技001', 'access_token':'asdasd2222',
                 'expect_result':{'code':27,'msg':'Invalid session','sub_code':'INVALID_PARAMS','sub_msg':'INVALID_PARAMS:invalid AccessToken : asdasd2222',
                                  'exception':'access session expired or invalid'}},
                {'soft_code':'SYB', 'nick':'tester', 'access_token':'62004155d9841cff42d5e4ceg02aa97dc7226246da446b5871727117',
                 'expect_result':{'code':15,'msg':'Remote service error','sub_code':'isv.invalid-parameter','sub_msg':'无法根据nick获取直通车帐号信息'}}]
        for item in data:
            soft_code = item['soft_code']
            nick = item['nick']
            access_token = item['access_token']
            expect_result = item['expect_result']
            try:
                actual_result = SimbaLoginAuthsignGet.get_subway_token_with_access_token(soft_code,nick,access_token)
                self.assertEqual(type(actual_result),type(expect_result))
                self.assertEqual(len(actual_result),len(expect_result))
            except InvalidAccessTokenException,e:
                self.assertEqual(e.msg,expect_result['exception'])
            except ErrorResponseException,e:
                self.assertEqual(e.code,expect_result['code'])
                self.assertEqual(e.msg,expect_result['msg'])
                self.assertEqual(e.sub_code,expect_result['sub_code'])
    def tearDown(self):
        pass
    
    @classmethod
    def tearDownClass(cls):
        pass
if __name__ == "__main__":
    unittest.main()
alltests = unittest.TestLoader().loadTestsFromTestCase(test_simba_login_authsign_get)
