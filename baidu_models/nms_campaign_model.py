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


class NmsCampaignModel(object):
    baiduApiObj = BaiduApiClient('nms', 'CampaignService')
    
    @classmethod
    def add_campaign(cls, username, access_token, campaign_name, budget, status):
        cls.baiduApiObj.set_authheader(username, access_token)
        client = cls.baiduApiObj.client

        request = client.factory.create('addCampaignRequest')
        campaign = client.factory.create('addCampaignRequest.campaignTypes')
        campaign.campaignName = campaign_name 
        campaign.budget = budget 
        campaign.status = status 
        request.campaignTypes = []
        request.campaignTypes.append(campaign)

        client.service.addCampaign(request.campaignTypes)
        res = client.last_received()
        
        res_dict, failure_dict = parse_soap_response(res)
        if failure_dict:
            logger.error("error info: %s", str(failure_dict))
            raise 
        return res_dict

    @classmethod
    def get_campaign_ids(cls, username, access_token):
        cls.baiduApiObj.set_authheader(username, access_token)
        client = cls.baiduApiObj.client

        client.service.getCampaignId()
        res = client.last_received()

        res_dict, failure_dict = parse_soap_response(res)
        if failure_dict:
            logger.error("error info: %s", str(failure_dict))
            raise 
        return res_dict
        
    @classmethod
    def get_campaign_by_campaign_ids(cls, username, access_token, campaign_ids):
        cls.baiduApiObj.set_authheader(username, access_token)
        client = cls.baiduApiObj.client

        client.service.getCampaignByCampaignId(campaign_ids)
        res = client.last_received()

        res_dict, failure_dict = parse_soap_response(res)
        if failure_dict:
            logger.error("error info: %s", str(failure_dict))
            raise 
        return res_dict
        

if __name__ == "__main__":
    access_token = "1738eac6-6fa2-4b29-a205-50a3335c8702"
    username = "xh麦苗"
    res_dict = NmsCampaignModel.get_campaign_ids(username, access_token)
    print res_dict['body']
    print res_dict['response']
    res_dict = NmsCampaignModel.get_campaign_by_campaign_ids(username, access_token, [2501797, 2501789])
    print "=========="
    print res_dict['body']
    print res_dict['response']
    print "++++++++++"
