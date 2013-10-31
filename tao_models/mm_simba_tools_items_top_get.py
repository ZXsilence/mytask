#! /usr/bin/env python
#! coding: utf-8 
# author = xieguanfu 
# date = 13-10-31

import sys
import os
import logging
import logging.config

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from tao_models.conf import set_env
    set_env.getEnvReady()
    from tao_models.conf.settings import set_taobao_client
    set_taobao_client('21065688', '74aecdce10af604343e942a324641891')

from TaobaoSdk import SimbaToolsItemsTopGetRequest 
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf import    settings as tao_model_settings
from tao_models.common.decorator import  tao_api_exception
from tao_models.common.app_key_info import  SYB_APP
from  TaobaoSdk import  TaobaoClient

logger = logging.getLogger(__name__)

class MMSimbaToolsItemsTopGet(object):
    """
    TODO
    """

    @classmethod
    @tao_api_exception()
    def get_top_items_by_keyword(cls, nick, access_token, keyword, app_key,app_secret,ip='183.129.237.217'):
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
        #client = TaobaoClient("http://gw.api.taobao.com/router/rest",SYB_APP["APP_KEY"] ,SYB_APP["APP_SECRET"]) 
        client = TaobaoClient("http://gw.api.taobao.com/router/rest",app_key ,app_secret) 
        rsp = client.execute(req, access_token)[0]
        if not rsp.isSuccess():
            logger.debug("get_top_item_by_keyword failed, msg [%s] sub_msg [%s]", rsp.msg, rsp.sub_msg) 
            raise ErrorResponseException(code=rsp.code,msg=rsp.msg, sub_msg=rsp.sub_msg, sub_code=rsp.sub_code)

        for item in rsp.rankeditems:
            items_list.append(item.toDict())
        return items_list

if __name__ == '__main__':
    nick = '时尚衣芭'
    access_token = '6201330d6b3c8bf9cec0abcb062bf7e59289fegi9ca6031520500325'
    keyword = 'elle 女包'
    items = MMSimbaToolsItemsTopGet.get_top_items_by_keyword(nick, access_token, keyword)
    for item in items:
        print item
