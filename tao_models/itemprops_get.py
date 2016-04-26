#encoding=utf8
__author__ = 'zhoujiebing@maimiaotech.com'

import sys
import os
import logging
import logging.config
import datetime

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('normal_test')

from TaobaoSdk import ItempropsGetRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class ItempropsGet(object):

    @classmethod
    @tao_api_exception()
    def get_cat_propvalues(cls, cid):
        req = ItempropsGetRequest()
        req.fields = 'pid,name,must,multi,prop_values'
        req.cid = cid
        nick = None
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        if rsp.item_props:
            return change_obj_to_dict_deeply(rsp.item_props)
        else:
            return []

if __name__ == '__main__':
    result = ItempropsGet.get_cat_propvalues(int(sys.argv[1]))
    for prop in result:
        value_list = prop.get('prop_values', [])
        line_len = min(len(value_list), 3)
        line_list = []
        for i in range(line_len):
            line_list.append('%s|%d' % (value_list[i]['name'], value_list[i]['vid']))
        print '%d,%s:%s' % (prop['pid'],prop['name'],' '.join(line_list))
