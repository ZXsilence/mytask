#encoding=utf8
'''
Created on 2012-8-10

@author: dk
'''
import sys
import os
import logging
import logging.config
import json
import datetime
from copy import deepcopy


if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('normal_test')

from TaobaoSdk import DmpTagsGetRequest 
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply
from tao_models.num_tools import change2num
from TaobaoSdk.Exceptions import ErrorResponseException
from tao_models.common.date_tools import  split_date

logger = logging.getLogger(__name__)

class DmpTagsGet(object):

    page_size = 200
    __params = ('campaign_id','status','name','page_size','adgroup_id_list','page_num')
    
    @classmethod
    @tao_api_exception()
    def get_dmp_tags(cls, nick, tag_name = '', soft_code = 'YZB'):
        req = DmpTagsGetRequest()
        req.tag_name = tag_name
        rsp = ApiService.execute(req,nick,soft_code)
        result = json.loads(rsp.responseBody)
        result = result['dmp_tags_get_response']['result']['tags']['tag_d_t_o']
        return result

if __name__ == '__main__':
    nick = '优美妮旗舰店'
    try_list = DmpTagsGet.get_dmp_tags(nick)
    keys_list = ['id','tag_name', 'tag_desc','tag_share','valid_date']
    print ','.join(keys_list)

    for tag in try_list:
        line = str(tag['id'])
        for key in keys_list[1:]:
            line += ',%s' %  tag.get(key,'')
        print line 
