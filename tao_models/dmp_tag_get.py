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

from TaobaoSdk import DmpTagGetRequest 
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply
from tao_models.num_tools import change2num
from TaobaoSdk.Exceptions import ErrorResponseException
from tao_models.common.date_tools import  split_date

logger = logging.getLogger(__name__)

class DmpTagGet(object):

    @classmethod
    @tao_api_exception()
    def get_dmp_tag(cls, nick, tag_id, soft_code = 'YZB'):
        req = DmpTagGetRequest()
        req.tag_id = tag_id
        rsp = ApiService.execute(req,nick,soft_code)
        result = json.loads(rsp.responseBody)
        result = result['dmp_tag_get_response']['result']['tag']
        result['tag_option_group_d_t_os'] = result['tag_option_group_d_t_os']['tag_option_group_dt_t_o']
        return result

if __name__ == '__main__':
    nick = '优美妮旗舰店'
    try_list = DmpTagGet.get_dmp_tag(nick, int(sys.argv[1]))
    print try_list['tag_option_group_d_t_os']
    keys_list = ['option_name','option_value','option_group_id','parent_option_id','sort_num','id']
    print ','.join(keys_list)
    for element in try_list['tag_option_group_d_t_os'][0]['tag_option_d_t_os']['tag_option_d_t_o']:
        line = str(element['option_name'])
        for key in keys_list[1:]:
            line += ',%s' % element[key]
        print line 
