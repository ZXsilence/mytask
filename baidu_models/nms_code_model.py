#! /usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
from BaiduApiClient import BaiduApiClient
from BaiduApiClient import parse_soap_response 
import suds

if __name__ == "__main__":
    import logging.config
    curr_path = os.path.dirname(__file__)
    logging.config.fileConfig(os.path.join(curr_path,'./consolelogger.conf'))

logger = logging.getLogger(__name__)


class NmsCodeModel(object):
    baiduApiObj = BaiduApiClient('nms', 'CodeService')
    
    @classmethod
    def get_all_category(cls, username, access_token):
        cls.baiduApiObj.set_authheader(username, access_token)
        client = cls.baiduApiObj.client

        client.service.getAllCategory()
        res = client.last_received()

        res_dict, failure_dict = parse_soap_response(res)
        if failure_dict:
            logger.error("error info: %s", str(failure_dict))
            raise 
        return res_dict
        
    @classmethod
    def get_all_region(cls, username, access_token):
        cls.baiduApiObj.set_authheader(username, access_token)
        client = cls.baiduApiObj.client

        client.service.getAllRegion()
        res = client.last_received()

        res_dict, failure_dict = parse_soap_response(res)
        if failure_dict:
            logger.error("error info: %s", str(failure_dict))
            raise 
        return res_dict
        
if __name__ == "__main__":
    access_token = "a2a8e353-33e8-473a-a0f3-7eafc0eebdaf"
    username = "xh麦苗"
    res_dict = NmsCodeModel.get_all_category(username, access_token)
    print res_dict['body']
    print res_dict['response']
    res_dict = NmsCodeModel.get_all_region(username, access_token)
    print "=========="
    print res_dict['body']
    print res_dict['response']
    print "++++++++++"
