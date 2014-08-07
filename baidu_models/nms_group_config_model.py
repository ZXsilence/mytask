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


class NmsGroupConfigModel(object):
    baiduApiObj = BaiduApiClient('nms', 'GroupConfigService')
    
    @classmethod
    def set_target_info(cls, username, access_token, request_data):
        cls.baiduApiObj.set_authheader(username, access_token)
        client = cls.baiduApiObj.client

        client.service.setTargetInfo(request_data)

        res = client.last_received()
        
        res_dict, failure_dict = parse_soap_response(res)
        if failure_dict:
            logger.error("error info: %s", str(failure_dict))
            raise 
        return res_dict

    @classmethod
    def get_target_info(cls, username, access_token, group_ids):
        cls.baiduApiObj.set_authheader(username, access_token)
        client = cls.baiduApiObj.client

        client.service.getTargetInfo(group_ids)
        res = client.last_received()

        res_dict, failure_dict = parse_soap_response(res)
        if failure_dict:
            logger.error("error info: %s", str(failure_dict))
            raise 
        return res_dict
        
    @classmethod
    def get_keyword_by_keywordids(cls, username, access_token, keyword_ids):
        cls.baiduApiObj.set_authheader(username, access_token)
        client = cls.baiduApiObj.client

        keyword = client.service.getKeyword(keyword_ids)
        res = client.last_received()

        res_dict, failure_dict = parse_soap_response(res)
        if failure_dict:
            logger.error("error info: %s", str(failure_dict))
            raise 
        return res_dict
        
    @classmethod
    def add_keywords(cls, username, access_token, keywords):
        cls.baiduApiObj.set_authheader(username, access_token)
        client = cls.baiduApiObj.client

        client.service.addKeyword(keywords)
        res = client.last_received()

        res_dict, failure_dict = parse_soap_response(res)
        if failure_dict:
            logger.error("error info: %s", str(failure_dict))
            raise 
        return res_dict
        
    @classmethod
    def delete_keyword(cls, username, access_token, keywords):
        cls.baiduApiObj.set_authheader(username, access_token)
        client = cls.baiduApiObj.client

        client.service.deleteKeyword(keywords)
        res = client.last_received()

        res_dict, failure_dict = parse_soap_response(res)
        if failure_dict:
            logger.error("error info: %s", str(failure_dict))
            raise 
        return res_dict
        
    @classmethod
    def set_interest_info(cls, username, access_token, interest_info):
        cls.baiduApiObj.set_authheader(username, access_token)
        client = cls.baiduApiObj.client

        client.service.setInterestInfo(interest_info)
        res = client.last_received()

        res_dict, failure_dict = parse_soap_response(res)
        if failure_dict:
            logger.error("error info: %s", str(failure_dict))
            raise 
        return res_dict
        # send request

    @classmethod
    def get_interest_info(cls, username, access_token, group_ids):
        cls.baiduApiObj.set_authheader(username, access_token)
        client = cls.baiduApiObj.client

        client.service.getInterestInfo(group_ids)
        res = client.last_received()

        res_dict, failure_dict = parse_soap_response(res)
        if failure_dict:
            logger.error("error info: %s", str(failure_dict))
            raise 
        return res_dict


    @classmethod
    def add_interest_infos(cls, username, access_token, interest_infos):
        cls.baiduApiObj.set_authheader(username, access_token)
        client = cls.baiduApiObj.client

        client.service.addInterestInfo(interest_infos)
        res = client.last_received()

        res_dict, failure_dict = parse_soap_response(res)
        if failure_dict:
            logger.error("error info: %s", str(failure_dict))
            raise 
        return res_dict

    @classmethod
    def delete_interest_infos(cls, username, access_token, interest_infos):
        cls.baiduApiObj.set_authheader(username, access_token)
        client = cls.baiduApiObj.client

        client.service.deleteInterestInfo(interest_infos)
        res = client.last_received()

        res_dict, failure_dict = parse_soap_response(res)
        if failure_dict:
            logger.error("error info: %s", str(failure_dict))
            raise 
        return res_dict


    @classmethod
    def set_exclude_ips(cls, username, access_token, group_id, exclude_ips):
        cls.baiduApiObj.set_authheader(username, access_token)
        client = cls.baiduApiObj.client

        request = client.factory.create('setExcludeIpRequest')
        excludeIp = client.factory.create('setExcludeIpRequest.excludeIp')
        excludeIp.groupId = group_id 
        excludeIp.excludeIp = exclude_ips 
        request.excludeIp = excludeIp
        
        # send request
        client.service.setExcludeIp(request.excludeIp)
        res = client.last_received()

        res_dict, failure_dict = parse_soap_response(res)
        if failure_dict:
            logger.error("error info: %s", str(failure_dict))
            raise 
        return res_dict




if __name__ == "__main__":
    access_token = "c15e6769-e204-4b4e-86ef-e4f8c5eed498"
    username = "xh麦苗"

