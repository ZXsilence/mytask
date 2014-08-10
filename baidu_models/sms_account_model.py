#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
from BaiduApiClient import BaiduApiClient
from BaiduApiClient import parse_soap_response 

if __name__ == "__main__":
    import logging
    import logging.config
    curr_path = os.path.dirname(__file__)
    logging.config.fileConfig(os.path.join(curr_path,'./consolelogger.conf'))


class SmsAccountModel(object):
    baiduApiObj = BaiduApiClient('sms', 'AccountService')
    
    @classmethod
    def get_account_info(cls, username, access_token):
        cls.baiduApiObj.set_authheader(username, access_token)
        client = cls.baiduApiObj.client

        client.service.getAccountInfo()
        res = client.last_received()
        res_dict, failure_dict = parse_soap_response(res)
        if failure_dict:
            raise 
        return res_dict
        
    @classmethod
    def update_account_info(cls, username, access_token, account_info):
        cls.baiduApiObj.set_authheader(username, access_token)
        client = cls.baiduApiObj.client

        client.service.updateAccountInfo(account_info)
        res = client.last_received()
        res_dict, failure_dict = parse_soap_response(res)
        if failure_dict:
            raise 
        return res_dict
        
if __name__ == "__main__":
    access_token = "ad03f5fe-4380-486f-b71e-60ab55da56ea"
    username = "xh麦苗"
    res_dict = SmsAccountModel.get_account_info(username, access_token)
    #print res_dict['body']
    print res_dict['response']
