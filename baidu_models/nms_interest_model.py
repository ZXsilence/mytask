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


class NmsInterestModel(object):
    baiduApiObj = BaiduApiClient('nms', 'InterestService')
    
    @classmethod
    def get_interest(cls, username, access_token):
        cls.baiduApiObj.set_authheader(username, access_token)
        client = cls.baiduApiObj.client

        client.service.getInterest()
        res = client.last_received()
        res_dict, failure_dict = parse_soap_response(res)
        if failure_dict:
            raise 
        return res_dict
        
    @classmethod
    def get_all_custom_interest(cls, username, access_token):
        cls.baiduApiObj.set_authheader(username, access_token)
        client = cls.baiduApiObj.client

        client.service.getAllCustomInterest()
        res = client.last_received()
        res_dict, failure_dict = parse_soap_response(res)
        if failure_dict:
            raise 
        return res_dict
        
    @classmethod
    def get_custom_interest(cls, username, access_token, cids):
        cls.baiduApiObj.set_authheader(username, access_token)
        client = cls.baiduApiObj.client

        client.service.getCustomInterest(cids)
        res = client.last_received()
        res_dict, failure_dict = parse_soap_response(res)
        if failure_dict:
            raise 
        return res_dict
        


        
if __name__ == "__main__":
    access_token = "9ec0a581-cc6b-4de0-87a6-d7bc78010c06"
    username = "xh麦苗"
    res_dict = NmsInterestModel.get_interest(username, access_token)
    #print res_dict['body']
    print res_dict['response']

    res_dict = NmsInterestModel.get_all_custom_interest(username, access_token)
    #print res_dict['body']
    print res_dict['response']







