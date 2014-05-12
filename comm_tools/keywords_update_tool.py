#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Chen Ke
@contact: chenke@MaimiaoTech.com
@date: 2012-09-11 20:21
@version: 0.0.0
@license: Copyright MaimiaoTech.com
@copyright: Copyright MaimiaoTech.com

"""
import os
import datetime

from keyword_db.services.keyword_db_service import KeywordDBService
from shengyb.db_models.keywords_deleted import KeywordsDeleted 
from tao_models.simba_keywords_delete import SimbaKeywordsDelete
from tao_models.simba_keywordsvon_add import SimbaKeywordsvonAdd
from tao_models.simba_keywords_pricevon_set import SimbaKeywordsPricevonSet

def delete_keywords(keyword_delete_list, campaign_id, sid, nick):
    if len(keyword_delete_list) == 0:
        return []

    keyword_delete_dict = {}
    for e in keyword_delete_list:
       keyword_delete_dict[e['keyword_id']] = e
    
    keyword_id_delete_list = [keyword['keyword_id'] for keyword in keyword_delete_list]
    keywords_deleted = SimbaKeywordsDelete.delete_keywords(nick
            , campaign_id, keyword_id_delete_list)
    keyword_ids_deleted = [k['keyword_id'] for k in keywords_deleted]
    KeywordDBService.del_keywords_by_keyword_ids(sid, keyword_ids_deleted)

    for keyword in keywords_deleted:
        delete_info = keyword_delete_dict[keyword['keyword_id']]
        delete_info['deleted_time'] = datetime.datetime.now()
        keyword.update(delete_info)
        KeywordsDeleted.upsert_keyword(sid, nick, keyword)
    return keywords_deleted


def add_keywords(keyword_list, campaign_id, adgroup_id, sid, nick):
    if len(keyword_list) == 0:
        return []

    keywords_added_dict = SimbaKeywordsvonAdd.add_keywords(nick, adgroup_id, keyword_list)
    KeywordDBService.add_keyword_list(sid, nick, keywords_added_dict)
    return keywords_added_dict 

def update_keywords_price(keyword_list, campaign_id, sid, nick):
    if len(keyword_list) == 0:
        return []

    keyword_price_toset_list = [] 
    for keyword in keyword_list:
        keyword_price_toset_list.append((keyword['keyword_id'], keyword['data']))
    keywords_dict_list= SimbaKeywordsPricevonSet.set_price(nick, keyword_price_toset_list)
    KeywordDBService.update_keyword_list(sid, keywords_dict_list)
    return keywords_dict_list


