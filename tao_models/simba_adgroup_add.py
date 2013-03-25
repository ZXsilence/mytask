#encoding=utf8
__author__ = 'lym liyangmin@maimiaotech.com'

import sys
import os
import logging
import logging.config

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from tao_models.conf import set_env
    set_env.getEnvReady()
    from tao_models.conf.settings import set_taobao_client
    set_taobao_client('12685542', '6599a8ba3455d0b2a043ecab96dfa6f9')

from TaobaoSdk import SimbaAdgroupAddRequest 
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf import settings as tao_model_settings
from tao_models.common.decorator import  tao_api_exception
from tao_models.common.exceptions import ItemForbiddenException

logger = logging.getLogger(__name__)

class SimbaAdgroupAdd(object):
    """
    """

    PAGE_SIZE = 200

    @classmethod
    @tao_api_exception(3)
    def add_adgroup(cls, access_token, nick, campaign_id, item_id, default_price, title, img_url):
        """
        add adgroup to campaign
        """

        req = SimbaAdgroupAddRequest()
        req.nick = nick
        req.campaign_id = campaign_id
        req.item_id = item_id 
        req.default_price = default_price
        req.title = title
        req.img_url = img_url

        #first_call
        try:
            rsp = tao_model_settings.taobao_client.execute(req, access_token)[0]
        except Exception, data:
            raise ApiExecuteException

        if not rsp.isSuccess():
            logger.error("nick [%s] add adgroup failed, msg [%s] sub_msg [%s]", nick, rsp.msg, rsp.sub_msg) 
            if "类目" in rsp.sub_msg or "商品" in rsp.sub_msg or "推广" in rsp.sub_msg or "创意" in rsp.sub_msg \
                    or "宝贝" in rsp.sub_msg or "knowledge" in rsp.sub_msg:
                raise ItemForbiddenException(msg=rsp.msg, sub_msg=rsp.sub_msg)
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_msg, sub_msg=rsp.sub_msg)

        return rsp.adgroup


if __name__ == '__main__':

    access_token = '6201d21d3bfa761000e15d6f4c1d3ZZ2331a6010d1ab4a8520500325'
    nick = 'chinchinstyle'
    campaign_id = '3328400'
    default_price = '10'
    title = '清仓 淘金币女士/男士围巾'
    #item_id = '7795118696'
    #img_url = 'http://img01.taobaocdn.com/bao/uploaded/i1/T1PEYUXd4nXXaK2CkT_012736.jpg'
    item_id = '7794896442'
    img_url = 'http://img01.taobaocdn.com/bao/uploaded/i1/T14oadXa8mXXXhDvA1_041135.jpg'

    adgroup = SimbaAdgroupAdd.add_adgroup(access_token, nick, campaign_id, item_id, default_price, title, img_url)
    
    print adgroup.toDict()
