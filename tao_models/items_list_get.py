#encoding=utf8
__author__ = 'lym liyangmin@maimiaotech.com'

import sys
import os
import copy
import logging
import logging.config

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('normal_test')

from TaobaoSdk import ItemsListGetRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)


class ItemsListGet(object):

    DEFAULT_FIELDS = 'title,price,pic_url,num_iid,detail_url,props_name,cid,delist_time,list_time,property_alias,seller_cids,freight_payer'
    MAX_NUM_IIDS = 20

    @classmethod
    def __reverse_props_name(cls, props_name, property_alias):
        alias_kvs = property_alias.split(';')
        if len(alias_kvs) == 0:
            return props_name

        alias_dict = {}
        for kv in alias_kvs:
            spliter = kv.split(':')
            if len(spliter) != 3:
                continue
            keyid = spliter[0]
            valueid = spliter[1]
            value = spliter[2]
            if not alias_dict.has_key(keyid):
                alias_dict[keyid] = {}
            alias_dict[keyid][valueid] = value

        props_kvs = props_name.split(';')
        props_name_alias = ''
        for props_kv in props_kvs:
            spliter = props_kv.split(':')
            if len(spliter) != 4:
                continue
            keyid = spliter[0]
            valueid = spliter[1]
            key = spliter[2]
            value = spliter[3]
            if alias_dict.has_key(keyid) and alias_dict[keyid].has_key(valueid):
                value = alias_dict[keyid][valueid]
            props_name_alias += keyid + ":" + valueid + ":" + key + ":" + value + ";"

        if len(props_name_alias) >= 1:
            props_name_alias = props_name_alias[:-1]
        return props_name_alias

    @classmethod
    @tao_api_exception()
    def _get_sub_items(cls,nick,sub_num_iid_list,fields):
        req = ItemsListGetRequest()
        req.fields = fields
        req.num_iids = ",".join([str(num_iid) for num_iid in sub_num_iid_list])
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        if rsp.items is None:
            logger.info("get item info, expect %s, actually return: %s"%(len(sub_num_iid_list), 0))
            return None 
        return rsp

    @classmethod
    @tao_api_exception()
    def get_item_list(cls, nick, num_iids, fields=DEFAULT_FIELDS):
        if 'props_name' in fields and not 'property_alias' in fields:
            fields += ',property_alias'

        num_iid_list = copy.deepcopy(num_iids)
        total_item_list = []

        while num_iid_list:
            sub_num_iid_list = num_iid_list[:cls.MAX_NUM_IIDS]
            num_iid_list = num_iid_list[cls.MAX_NUM_IIDS:]
            try:
                rsp = ItemsListGet._get_sub_items(nick,sub_num_iid_list,fields)
            except Exception,e:
                if 'isp.top-remote-connection-timeout-tmall' in str(e) or 'isp.top-remote-service-unavailable-tmall' in str(e):
                    print 'continue!',str(e)
                    continue
                else:
                    raise e
            if rsp is None:
                continue
            logger.debug("get item info, expect %s, actually return: %s"%(len(sub_num_iid_list), len(rsp.items)))
            total_item_list.extend(rsp.items)

        if 'props_name' in fields and 'property_alias' in fields:
            for item in total_item_list:
                props_name_alias = ItemsListGet.__reverse_props_name(item.props_name, item.property_alias)
                item.props_name = props_name_alias

        return change_obj_to_dict_deeply(total_item_list)


def test():
    nick = 'chinchinstyle'
    num_iids = [26796368149]
    ItemsListGet.MAX_NUM_IIDS = 20
    fields = 'title,price,pic_url,num_iid,detail_url,props_name,cid,list_time,delist_time,modified,freight_payer'
    total_item_list = ItemsListGet.get_item_list(num_iids, fields)


if __name__ == '__main__':
    test()
