#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wulingping
@contact: wulingping@maimiaotech.com
@date: 2013-10-30 16:54
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""
from datetime import datetime
from tao_models.conf import settings 

class AppcallStatus(object):

    _conn = settings.mongoConn
    
    @classmethod
    def _get_coll_by_software(cls,software):
        return cls._conn[software]['appcall_status']

    @classmethod
    #@mongo_exception
    def upsert_appcall_status(cls, software,api_method ,is_limited):
        curr_time = datetime.now()
        coll = cls._get_coll_by_software(software)
        coll.update({'_id':api_method,'api_method':api_method,'is_limited':is_limited,'modified_time':curr_time})

    @classmethod
    #@mongo_exception
    def get_appcall_status(cls,software,api_method):
        coll = cls._get_coll_by_software(software)
        return coll.find_one({'_id':api_method})

