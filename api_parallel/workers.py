#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: liumingchao
@contact: liumingchao@maimiaotech.com
@date: 2015-12-23 17:22
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
sys.path.append('../../comm_lib/')
sys.path.append('../../TaobaoOpenPythonSDK/')
from api_server.conf import set_env
set_env.getEnvReady()
from api_server.conf.settings import set_api_source
set_api_source('normal_test')
from celery import Celery
from api_parallel import  celeryconfig_result
from celery.result import AsyncResult
#from tao_models.items_list_get import ItemsListGet
#from tao_models.items_onsale_get import ItemsOnsaleGet
#from tao_models.simba_rpt_adgroupkeywordbase_get import SimbaRptAdgroupkeywordbaseGet
#from tao_models.simba_rpt_adgroupkeywordeffect_get import SimbaRptAdgroupkeywordeffectGet
#from tao_models.simba_rpt_campadgroupbase_get import SimbaRptCampadgroupBaseGet
#from tao_models.simba_rpt_campadgroupeffect_get import SimbaRptCampadgroupEffectGet
ItemsListGet = None
ItemsOnsaleGet = None
SimbaRptAdgroupkeywordbaseGet = None
SimbaRptAdgroupkeywordeffectGet = None
SimbaRptCampadgroupBaseGet = None
SimbaRptCampadgroupEffectGet = None
SimbaKeywordsQscoreSplitGet = None
import time
celery = Celery()
celery.config_from_object(celeryconfig_result)

@celery.task(name='get_rpt_adgroupkeywordbase_list')
def get_rpt_adgroupkeywordbase_list_worker(nick,campaign_id,adgroup_id,start_time,end_time,source,search_type):
    global SimbaRptAdgroupkeywordbaseGet
    if not SimbaRptAdgroupkeywordbaseGet: from tao_models.simba_rpt_adgroupkeywordbase_get import SimbaRptAdgroupkeywordbaseGet
    res = SimbaRptAdgroupkeywordbaseGet.get_rpt_adgroupkeywordbase_list(nick,campaign_id,adgroup_id,\
    start_time,end_time,source,search_type)
    return res

@celery.task(name='get_rpt_adgroupkeywordeffect_list')
def get_rpt_adgroupkeywordeffect_list_worker(nick,campaign_id,adgroup_id,start_time,end_time,source,search_type):
    global SimbaRptAdgroupkeywordeffectGet
    if not SimbaRptAdgroupkeywordeffectGet:from tao_models.simba_rpt_adgroupkeywordeffect_get import SimbaRptAdgroupkeywordeffectGet
    res = SimbaRptAdgroupkeywordeffectGet.get_rpt_adgroupkeywordeffect_list(nick,campaign_id,adgroup_id,\
    start_time,end_time,source,search_type)
    return res

@celery.task(name='get_rpt_adgroupbase_list')
def get_rpt_adgroupbase_list_worker(nick,campaign_id,start_time,end_time,search_type,source):
    global SimbaRptCampadgroupBaseGet
    if not SimbaRptCampadgroupBaseGet:from tao_models.simba_rpt_campadgroupbase_get import SimbaRptCampadgroupBaseGet
    res = SimbaRptCampadgroupBaseGet.get_rpt_adgroupbase_list(nick,campaign_id,start_time,end_time,search_type,source)
    return res

@celery.task(name='get_rpt_adgroupeffect_list')
def get_rpt_adgroupeffect_list_worker(nick,campaign_id,start_time,end_time,search_type,source):
    global SimbaRptCampadgroupEffectGet
    if not SimbaRptCampadgroupEffectGet:from tao_models.simba_rpt_campadgroupeffect_get import SimbaRptCampadgroupEffectGet
    res = SimbaRptCampadgroupEffectGet.get_rpt_adgroupeffect_list(nick,campaign_id,start_time,end_time,search_type,source)
    return res

@celery.task(name='get_item_list_by_page')
def get_item_list_by_page_worker(nick,start_page,page_size,fields):
    global ItemsOnsaleGet
    if not ItemsOnsaleGet:from tao_models.items_onsale_get import ItemsOnsaleGet
    item_list = []
    for index in range(page_size):
        res = ItemsOnsaleGet.get_item_list_with_page_no(nick,start_page+index,fields)
        item_list.extend(res)
    return item_list

@celery.task(name='get_item_list_by_num_iids')
def get_item_list_by_num_iids_worker(nick,num_iids,fields):
    global ItemsListGet
    if not ItemsListGet:from tao_models.items_list_get import ItemsListGet
    res = ItemsListGet.get_item_list(nick,num_iids,fields)
    return res

@celery.task(name='get_keywords_split_qscore')
def get_keywords_split_qscore_worker(nick,adgroup_id,keyword_ids):
    global SimbaKeywordsQscoreSplitGet
    if not SimbaKeywordsQscoreSplitGet:from tao_models.simba_keywords_qscore_split_get import SimbaKeywordsQscoreSplitGet
    res =SimbaKeywordsQscoreSplitGet.get_keywords_split_qscore(nick,adgroup_id,keyword_ids)
    return res

def get_result_by_task_ids(task_ids):
    done_ids = []
    res = []
    total_time=0
    while 1:
        if total_time>=60:
            raise Exception('timeout error')
        time.sleep(0.1)
        total_time+=0.1
        for task_id in task_ids:
            if task_id in done_ids:
                continue
            try:
                async_result = AsyncResult(task_id,backend=celery.backend)
                if async_result.status == "SUCCESS":
                    done_ids.append(task_id)
                    res.extend(async_result.get())
                elif async_result.status == "FAILURE":
                    #done_ids.append(task_id)
                    raise Exception('task error')
            except Exception ,e:
                if "Can't connect to MySQL server on" in str(e):
                    continue
        if len(done_ids) == len(task_ids):
            break
    return res

if __name__ == '__main__':
    pass
