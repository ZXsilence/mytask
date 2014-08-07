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


class NmsGroupModel(object):
    baiduApiObj = BaiduApiClient('nms', 'GroupService')
    
    @classmethod
    def add_group(cls, username, access_token, campaign_id, group_name, price, type, status):
        cls.baiduApiObj.set_authheader(username, access_token)
        client = cls.baiduApiObj.client

        request = client.factory.create('addGroupRequest')
        group = client.factory.create('addGroupRequest.groupTypes')
        group.campaignId = campaign_id 
        group.groupName = group_name 
        group.price = price 
        group.type = type 
        group.status = status 
        request.groupTypes = []
        request.groupTypes.append(group)

        client.service.addGroup(request.groupTypes)
        res = client.last_received()
        
        res_dict, failure_dict = parse_soap_response(res)
        if failure_dict:
            logger.error("error info: %s", str(failure_dict))
            raise 
        return res_dict

    @classmethod
    def get_group_by_campaign_id(cls, username, access_token, campaign_id):
        cls.baiduApiObj.set_authheader(username, access_token)
        client = cls.baiduApiObj.client

        client.service.getGroupByCampaignId(campaign_id)
        res = client.last_received()

        res_dict, failure_dict = parse_soap_response(res)
        if failure_dict:
            logger.error("error info: %s", str(failure_dict))
            raise 
        return res_dict

    @classmethod
    def get_group_ids(cls, username, access_token, group_ids):
        cls.baiduApiObj.set_authheader(username, access_token)
        client = cls.baiduApiObj.client

        client.service.getGroupByGroupId(group_ids)
        res = client.last_received()

        res_dict, failure_dict = parse_soap_response(res)
        if failure_dict:
            logger.error("error info: %s", str(failure_dict))
            raise 
        return res_dict
        
        

if __name__ == "__main__":
    access_token = "a2a8e353-33e8-473a-a0f3-7eafc0eebdaf"
    username = "xh麦苗"
    #res_dict = NmsGroupModel.get_group_ids(username, access_token)
    #print res_dict['body']
    #print res_dict['response']
    #res_dict = NmsGroupModel.get_group_by_group_ids(username, access_token, [2501797, 2501789])
    #print "=========="
    #print res_dict['body']
    #print res_dict['response']
    #print "++++++++++"




