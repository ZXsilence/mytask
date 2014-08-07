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


class NmsAdModel(object):
    baiduApiObj = BaiduApiClient('nms', 'AdService')
    
    @classmethod
    def add_ad(cls, username, access_token, localId, groupId, status, type, title, displayUrl, destinationUrl, description1, description2):
        cls.baiduApiObj.set_authheader(username, access_token)
        client = cls.baiduApiObj.client

        request = client.factory.create('addAdRequest')
        ad = client.factory.create('addAdRequest.adTypes')
        ad.localId = localId 
        ad.groupId = groupId 
        ad.status = status 
        ad.type = type 
        ad.title = title
        ad.displayUrl = displayUrl 
        ad.destinationUrl = destinationUrl 
        ad.description1 = description1 
        ad.description2 = description2 
        request.adTypes = []
        request.adTypes.append(ad)

        # send request
        client.service.addAd(request.adTypes)
        res = client.last_received()
        
        res_dict, failure_dict = parse_soap_response(res)
        if failure_dict:
            logger.error("error info: %s", str(failure_dict))
            raise 
        return res_dict

    @classmethod
    def update_ad(cls, username, access_token, localId, groupId, status, type, title, displayUrl, destinationUrl, description1, description2):
        cls.baiduApiObj.set_authheader(username, access_token)
        client = cls.baiduApiObj.client

        request = client.factory.create('updateAdRequest')
        ad = client.factory.create('updateAdRequest.adTypes')
        ad.localId = localId 
        ad.groupId = groupId 
        ad.status = status 
        ad.type = type 
        ad.title = title
        ad.displayUrl = displayUrl 
        ad.destinationUrl = destinationUrl 
        ad.description1 = description1 
        ad.description2 = description2 
        request.adTypes = []
        request.adTypes.append(ad)

        # send request
        client.service.updateAd(request.adTypes)
        res = client.last_received()
        
        res_dict, failure_dict = parse_soap_response(res)
        if failure_dict:
            logger.error("error info: %s", str(failure_dict))
            raise 
        return res_dict

    @classmethod
    def get_ad_by_ad_ids(cls, username, access_token, ad_ids):
        cls.baiduApiObj.set_authheader(username, access_token)
        client = cls.baiduApiObj.client

        client.service.getAdByAdId(ad_ids)
        res = client.last_received()

        res_dict, failure_dict = parse_soap_response(res)
        if failure_dict:
            logger.error("error info: %s", str(failure_dict))
            raise 
        return res_dict
        
    @classmethod
    def set_ad_status(cls, username, access_token, ad_id, status):
        cls.baiduApiObj.set_authheader(username, access_token)
        client = cls.baiduApiObj.client

        # contruct request body
        request = client.factory.create('setAdStatusRequest')
        s = client.factory.create('setAdStatusRequest.statusTypes')
        s.adId = ad_id 
        s.status = status 
        request.statusTypes = []
        request.statusTypes.append(s)
        client.service.setAdStatus(request.statusTypes)

        # receive response and print result
        res = client.last_received()
        
        res_dict, failure_dict = parse_soap_response(res)
        if failure_dict:
            logger.error("error info: %s", str(failure_dict))
            raise 
        return res_dict

if __name__ == "__main__":
    access_token = "a2a8e353-33e8-473a-a0f3-7eafc0eebdaf"
    username = "xh麦苗"
    res_dict = NmsAdModel.add_ad(username, access_token, 1, 2166166, 0, 2, "test_title1234567", "baidu.com"
                    , 'http://baidu.com/123', 'desc1234567', 'desc2345678')
    print res_dict['body']
    print res_dict['response']

