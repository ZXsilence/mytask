#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: xieguanfu
@contact: xieguanfu@maimiaotech.com
@date: 2015-12-30 13:43
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""
from service_server.conf import *
from service_server.services.client_service import ClientService

class ApiDataService(object):

    @classmethod
    def __get_rpts(cls,nick,start_date,end_date,rpt_type):
        start_date_str = start_date.strftime('%Y-%m-%d')
        end_date_str = end_date.strftime('%Y-%m-%d')
        params = {'rpt_type':rpt_type,'nick':nick,'start_date':start_date_str,'end_date':end_date_str}
        data = ClientService.execute(params,nick)
        return data

    @classmethod
    def get_account_rpts(cls,nick,start_date,end_date):
        '''钻展账户报表'''
        return cls.__get_rpts(nick,start_date,end_date,'account')

    @classmethod
    def get_campaign_rpts(cls,nick,start_date,end_date):
        '''钻展计划报表'''
        return cls.__get_rpts(nick,start_date,end_date,'campaign')

    @classmethod
    def get_trans_rpts(cls,nick,start_date,end_date):
        '''推广组报表'''
        return cls.__get_rpts(nick,start_date,end_date,'trans')

    @classmethod
    def get_keywords_rpts(cls,nick,start_date,end_date):
        '''关键词报表'''
        return cls.__get_rpts(nick,start_date,end_date,'keyword')

    @classmethod
    def get_adboard_rpts(cls,nick,start_date,end_date):
        '''创意报表'''
        return cls.__get_rpts(nick,start_date,end_date,'adboard')

    @classmethod
    def get_dest_rpts(cls,nick,start_date,end_date):
        '''定向报表'''
        return cls.__get_rpts(nick,start_date,end_date,'dest')
    
    @classmethod
    def get_dest_rpts(cls,nick,start_date,end_date):
        '''资源位词报表'''
        return cls.__get_rpts(nick,start_date,end_date,'adzone')

    @classmethod
    def get_category_rpts(cls,nick,start_date,end_date):
        '''类目词报表'''
        return cls.__get_rpts(nick,start_date,end_date,'category')

