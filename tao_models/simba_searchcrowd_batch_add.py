# -*- coding: utf-8 -*-
'''
Created on 2012-11-3

@author: dk
'''
import sys
import os
import logging
import logging.config
import simplejson as json
if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('normal_test')

from TaobaoSdk.Request.SimbaSearchcrowdBatchAddRequest import SimbaSearchcrowdBatchAddRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class SearchcrowdBatchAdd(object):

    @classmethod
    @tao_api_exception()
    def searchcrowdbatch_add(cls, nick, adgroup_id, adgroup_targeting_tags, soft_code):
        req = SimbaSearchcrowdBatchAddRequest()
        req.nick = nick
        req.adgroup_id = adgroup_id
        req.adgroup_targeting_tags = json.dumps(adgroup_targeting_tags)
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.adgrouptargetingtags)


if __name__ == '__main__':
    nick = "麦苗科技001"
    adgroup_id = 700403273 
    #adgroup_targeting_tags = [{"crowdDTO":{"templateId":"28","name":"浏览未购买店内商品的访客","tagList":[{"dimId":"100012","tagId":"",\
    #"tagName":"浏览未购买店内商品的访客","optionGroupId":"1012"}]},"isDefaultPrice":0,"discount":101},{"crowdDTO":{"templateId":"34",\
    #"name":"领用618购物券的访客","tagList":[{"dimId":"100150","tagId":"1","tagName":"领用618购物券的访客","optionGroupId":"2000"}]},\
    #"isDefaultPrice":0,"discount":101}]     
    adgroup_targeting_tags = [{"crowdDTO":{"templateId":"28","name":"浏览未购买店内商品的访客","tagList":[{"dimId":"100012","tagId":"",\
    "tagName":"浏览未购买店内商品的访客","optionGroupId":"1012"},{"dimId":"100150","tagId":"1","tagName":"领用618购物券的访客","optionGroupId":"2000"}]},"isDefaultPrice":0,"discount":101}]
    soft_code = 'SYB'
    print SearchcrowdBatchAdd.searchcrowdbatch_add(nick, adgroup_id, adgroup_targeting_tags, soft_code)
