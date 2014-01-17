#! /usr/bin/env python
#! coding: utf-8 
# author = zjb
# date = 12-12-21

import sys
import os
import logging
import logging.config

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from tao_models.conf import set_env
    set_env.getEnvReady()
    from tao_models.conf.settings import set_api_source
    set_api_source('api_test')

from TaobaoSdk import SimbaToolsItemsTopGetRequest 
from tao_models.common.decorator import  tao_api_exception
from tao_models.services.api_service import ApiService
from tao_models.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class SimbaToolsItemsTopGet(object):

    @classmethod
    @tao_api_exception()
    def get_top_items_by_keyword(cls, nick, keyword, ip='183.129.237.217'):
        """
        item format:
        {
        'link_url': 'http://detail.tmall.com/item.htm?id=19732900934', 
        'order': 1,
        'title':u'...'
        """
        items_list = []
        req = SimbaToolsItemsTopGetRequest()
        req.nick = nick
        req.keyword = keyword
        req.ip = ip
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        for item in rsp.rankeditems:
            items_list.append(item.toDict())
        return change_obj_to_dict_deeply(items_list)

if __name__ == '__main__':
    nick = 'chinchinstyle'
    keyword = '围巾'
    items = SimbaToolsItemsTopGet.get_top_items_by_keyword(nick, keyword)
    for item in items:
        print item
