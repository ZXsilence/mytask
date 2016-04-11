#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: liumingchao
@contact: liumingchao@maimiaotech.com
@date: 2015-12-29 10:23
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""

#报表按天以及分页api按页并发，最大并发数10

if __name__ == '__main__':
    import sys,os
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('normal_test')
import datetime
from api_parallel.workers import *

class SimbaParallelApi(object):
    MAX_TASK_NUM = 10
    DEFAULT_FIELDS_2 = 'title,price,pic_url,num_iid,detail_url,props_name,cid,delist_time,list_time,property_alias,seller_cids,freight_payer'
    DEFAULT_FIELDS_1 = 'title,price,pic_url,num_iid'
    
    @classmethod
    def get_parallel_date_list(cls,params_dict):
        time_list = []
        a_task_days = ((params_dict['end_time'] - params_dict['start_time']).days+1) / cls.MAX_TASK_NUM
        remainder_days = ((params_dict['end_time'] - params_dict['start_time']).days+1) % cls.MAX_TASK_NUM
        if a_task_days<=0:
            task_num = remainder_days
        else:
            task_num = cls.MAX_TASK_NUM
        for index in range(task_num):
            if index < remainder_days:
                days = a_task_days+1
            else:
                days = a_task_days
            start_time = params_dict['start_time']
            end_time = params_dict['start_time'] + datetime.timedelta(days=days-1)
            params_dict['start_time'] = params_dict['start_time'] + datetime.timedelta(days=days)
            time_list.append((start_time,end_time))
        return time_list
    
    @classmethod
    def get_parallel_page_list(cls,page_count):
        page_no_list = []
        a_task_pages = page_count/cls.MAX_TASK_NUM
        remainder_pages = page_count%cls.MAX_TASK_NUM
        page_start = 1
        if a_task_pages <= 0:
            task_num= remainder_pages
        else:
            task_num = cls.MAX_TASK_NUM
        for index in range(task_num):
            if index < remainder_pages:
                sub_page_count = a_task_pages + 1
            else:
                sub_page_count = a_task_pages
            page_no_list.append((page_start,sub_page_count))
            page_start = page_start + sub_page_count 
        return page_no_list
    

    @classmethod
    def get_rpt_adgroupkeywordbase_list(cls, nick, campaign_id, adgroup_id, start_time, end_time, source, search_type):
        params_dict = {'start_time':start_time,'end_time':end_time}
        time_list = cls.get_parallel_date_list(params_dict)
        task_ids = []
        for item in time_list:
            task_ids.append(get_rpt_adgroupkeywordbase_list_worker.delay(nick,campaign_id,adgroup_id,\
            item[0],item[1],source,search_type).task_id)
        return get_result_by_task_ids(task_ids)
    
    @classmethod
    def get_rpt_adgroupkeywordeffect_list(cls, nick, campaign_id, adgroup_id, start_time, end_time, source, search_type):
        params_dict = {'start_time':start_time,'end_time':end_time}
        time_list = cls.get_parallel_date_list(params_dict)
        task_ids = []
        for item in time_list: 
            task_ids.append(get_rpt_adgroupkeywordeffect_list_worker.delay(nick,campaign_id,adgroup_id,\
            item[0],item[1],source,search_type).task_id)
        return get_result_by_task_ids(task_ids)
    
    @classmethod
    def get_rpt_adgroupbase_list(cls,nick,campaign_id,start_time,end_time,search_type,source):
        params_dict = {'start_time':start_time,'end_time':end_time}
        time_list = cls.get_parallel_date_list(params_dict)
        task_ids = []
        for item in time_list:
            task_ids.append(get_rpt_adgroupbase_list_worker.delay(nick,campaign_id,item[0],item[1],search_type,source).task_id)
            #res = get_rpt_adgroupbase_list_worker(nick,campaign_id,item[0],item[1],source,search_type)
        return get_result_by_task_ids(task_ids)

    
    @classmethod
    def get_rpt_adgroupeffect_list(cls,nick,campaign_id,start_time,end_time,search_type,source):
        params_dict = {'start_time':start_time,'end_time':end_time}
        time_list = cls.get_parallel_date_list(params_dict)
        task_ids = []
        for item in time_list:
            task_ids.append(get_rpt_adgroupeffect_list_worker.delay(nick,campaign_id,item[0],item[1],search_type,source).task_id)
        return get_result_by_task_ids(task_ids)

    
    @classmethod
    def get_item_list_by_page(cls,nick,max_pages,fields=DEFAULT_FIELDS_1):
        pages = min(50,max_pages)
        page_list = cls.get_parallel_page_list(pages)
        task_ids = []
        for item in page_list:
            task_ids.append(get_item_list_by_page_worker.delay(nick,item[0],item[1],fields).task_id)
            #res = get_item_list_by_page_worker(nick,item[0],item[1],fields)
        return get_result_by_task_ids(task_ids)


    @classmethod
    def get_item_list_by_num_iids(cls,nick,num_iids,fields=DEFAULT_FIELDS_2):
        a_task_id_num = len(num_iids)/cls.MAX_TASK_NUM + 1
        task_ids = []
        while num_iids:
            task_ids.append(get_item_list_by_num_iids_worker.delay(nick,num_iids[:a_task_id_num],fields).task_id)
            num_iids  = num_iids[a_task_id_num:]
        return get_result_by_task_ids(task_ids)
   
    @classmethod
    def get_keywords_split_qscore(cls,nick,adgroup_id,keyword_ids):
        sub_ids_num = 40
        task_ids = []
        while keyword_ids:
            task_ids.append(get_keywords_split_qscore_worker.delay(nick,adgroup_id,keyword_ids[:sub_ids_num]).task_id)
            keyword_ids=keyword_ids[sub_ids_num:]
        return get_result_by_task_ids(task_ids)
        

    




if __name__ == '__main__':
    #nick = '麦苗科技001'
    #campaign_id = 9214487 
    #adgroup_id = 649128895
    '''关键词测试组'''
    nick = '等待一个永恒'
    campaign_id = 16015230 
    adgroup_id = 633847780
    '''计划获取推广组报表测试组'''
    #nick = "大雪1"
    #campaign_id = 11118425 
    #adgroup_id = 608516400
    search_type = 'SEARCH,CAT'
    source = '1,2'
    start_time = datetime.datetime.now() - datetime.timedelta(days=3)
    end_time = datetime.datetime.now() - datetime.timedelta(days=1)
    print datetime.datetime.now()
    #print len(SimbaParallelApi.get_rpt_adgroupkeywordbase_list(nick,campaign_id,adgroup_id,start_time,end_time,source,search_type))
    #print len(SimbaParallelApi.get_rpt_adgroupkeywordeffect_list(nick,campaign_id,adgroup_id,start_time,end_time,source,search_type))
    #res = SimbaParallelApi.get_rpt_adgroupbase_list(nick,campaign_id,start_time,end_time,search_type,source)
    #res = SimbaParallelApi.get_rpt_adgroupeffect_list(nick,campaign_id,start_time,end_time,search_type,source)
    #print len(res)
    print datetime.datetime.now()
    #res = SimbaParallelApi.get_item_list_by_page(nick,10)
    #num_iids = [d['num_iid'] for d in res]
    #res = SimbaParallelApi.get_item_list_by_num_iids(nick,num_iids)
    #print len(res)
    #print res[0]

