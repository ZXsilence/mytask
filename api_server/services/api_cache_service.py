#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: xieguanfu
@contact: xieguanfu@maimiaotech.com
@date: 2016-06-06 17:02
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""
import logging
from datetime import datetime
from api_server.db_models.api_cache import  ApiCache
from api_server.services.api_cache_config import ApiCacheConfig
logger = logging.getLogger(__name__)

class ApiCacheService(object):

    sys_keys = ('format', 'timestamp', 'app_key', 'sign', 'session', 'sign_method', 'v', 'partner_id', 'method')

    @classmethod
    def get_cache_key(cls,params_dict):
        method = params_dict['method']
        config = ApiCacheConfig.API_METHOD_CONFIG.get(method)
        #配置各个api缓存的类型参数,以及此cache的cache key 生成方式以便操作cache
        if not config:
            return
        ##update操作不是按cache_key操作,是按照cache_name + nick 进行清理
        ##因为一个update操作会对同一个cache_name下的多个api都产生影响
        if not config['is_get']:
            return
        #针对同一个get接口不同的用户与参数都对于不同的结果集,他们的cache_key肯定不能一样
        user_params = dict(itr for itr in params_dict.iteritems() if itr[0] not in cls.sys_keys)
        cache_key = '%s_%s' % (method,hash(str(user_params)))
        return cache_key

    @classmethod
    def set_api_cache(cls,cache_key,cache_data,add_info_dict):
        try:
            ApiCache.upsert_api_cache(cache_key,cache_data,add_info_dict)
        except Exception,e:
            logger.exception('set api cache error')

    @classmethod
    def get_api_cache(cls,cache_key):
        try:
            return ApiCache.get_api_cache(cache_key)
        except Exception,e:
            logger.exception('get api cache error')

    @classmethod
    def get_detail_config(cls,params_dict):
        method = params_dict['method']
        config = ApiCacheConfig.API_METHOD_CONFIG.get(method)
        cache_key_config = None
        if not config:
            return method,config,cache_key_config
        cache_name = config['cache_name']
        cache_key_config = ApiCacheConfig.API_CACHE_KEY_CONFIG.get(cache_name)
        return method,config,cache_key_config

    @classmethod
    def get_cache(cls,cache_key,params_dict):
        try:
            method,config,cache_key_config= cls.get_detail_config(params_dict)
            if not config:
                return
            doc = cls.get_api_cache(cache_key)
            if not doc:
                return
            now = datetime.now()
            #过期时间默认为分钟
            max_age = (now - doc['cache_time']).total_seconds()/60
            if 0 <= max_age <= config.get('max_age',30):
                return doc['data'] 
        except Exception,e:
            logger.warning('get api cache error: %s' % e.__str__())

    @classmethod
    def set_cache(cls,cache_key,cache_data,add_info_dict,params_dict):
        try:
            method,config,cache_key_config= cls.get_detail_config(params_dict)
            if config and 'start_cache_hour' in config:
                now = datetime.now()
                if now.hour < int(config['start_cache_hour']):
                    return
            #除了nick,cache_name 之外的其他关键系额外参数用户控制更小粒度的缓存如:campaing_id,adgroup_id
            remove_cache_filter = {}
            if cache_key_config:
                remove_cache_filter = dict((k,params_dict[k]) for k in cache_key_config['remove_keys'] if k in params_dict) if cache_key_config else {}
            remove_cache_filter.update(add_info_dict)
            cls.set_api_cache(cache_key,cache_data,remove_cache_filter)
        except Exception,e:
            logger.warning('set api cache error: %s' % e.__str__())


    @classmethod
    def clear_cache(cls,nick,params_dict):
        try:
            method = params_dict['method']
            config = ApiCacheConfig.API_METHOD_CONFIG.get(method)
            if not method:
                logger.warning('method:%s not found the cache key config for remove cache')
                return
            cache_name = config['cache_name']
            cache_key_config = ApiCacheConfig.API_CACHE_KEY_CONFIG.get(cache_name)
            remove_cache_filter = dict((k,params_dict[k]) for k in cache_key_config['remove_keys'] if k in params_dict) if cache_key_config else {}
            if len(remove_cache_filter) < len(cache_key_config['remove_keys']):
                logger.warning('清除缓存 key 数量不匹配 nick:%s,method:%s' %(nick,method))
            ApiCache.clear_cache(cache_name,nick,remove_cache_filter)
        except Exception,e:
            logger.warning('clear cache error: %s' % e.__str__())


    @classmethod
    def clear_user_cache(cls,nick):
        remove_cache_filter = {}
        cache_name_list = set(config['cache_name'] for config in ApiCacheConfig.API_METHOD_CONFIG.values())
        #公有数据可以不清理,只清理用户自己的数据
        for cache_name in cache_name_list:
            logger.warning('clean nick:%s api cache ,cache_name:%s' % (nick,cache_name))
            ApiCache.clear_cache(cache_name,nick,remove_cache_filter)
        logger.warning('clean nick:%s api cache done' % nick)
