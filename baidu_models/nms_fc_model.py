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


class NmsFcModel(object):
    baiduApiObj = BaiduApiClient('nms', 'FCService')
    
    @classmethod
    def get_fc_campaignid(cls, username, access_token):
        cls.baiduApiObj.set_authheader(username, access_token)
        client = cls.baiduApiObj.client

        client.service.getFCCampaignId()
        res = client.last_received()
        res_dict, failure_dict = parse_soap_response(res)
        if failure_dict:
            raise 
        return res_dict
        
if __name__ == "__main__":
    access_token = "a2a8e353-33e8-473a-a0f3-7eafc0eebdaf"
    username = "xh麦苗"
    res_dict = NmsFcModel.get_fc_campaignid(username, access_token)
    #print res_dict['body']
    print res_dict['response']
