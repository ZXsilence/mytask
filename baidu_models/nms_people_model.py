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


class NmsPeopleModel(object):
    baiduApiObj = BaiduApiClient('nms', 'PeopleService')
    
    @classmethod
    def get_all_people(cls, username, access_token):
        cls.baiduApiObj.set_authheader(username, access_token)
        client = cls.baiduApiObj.client

        client.service.getAllPeople()
        res = client.last_received()
        res_dict, failure_dict = parse_soap_response(res)
        if failure_dict:
            raise 
        return res_dict
        
    @classmethod
    def get_people(cls, username, access_token, pids):
        cls.baiduApiObj.set_authheader(username, access_token)
        client = cls.baiduApiObj.client

        client.service.getPeople(pids)
        res = client.last_received()
        res_dict, failure_dict = parse_soap_response(res)
        if failure_dict:
            raise 
        return res_dict
        


        
if __name__ == "__main__":
    access_token = "9ec0a581-cc6b-4de0-87a6-d7bc78010c06"
    username = "xh麦苗"
    res_dict = NmsPeopleModel.get_all_people(username, access_token)
    #print res_dict['body']
    print res_dict['response']

