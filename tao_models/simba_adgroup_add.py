#encoding=utf8
__author__ = 'lym liyangmin@maimiaotech.com'

import sys
import os
import logging
import logging.config

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('normal_test')

from TaobaoSdk import SimbaAdgroupAddRequest 
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class SimbaAdgroupAdd(object):
    """
    """

    PAGE_SIZE = 200

    @classmethod
    @tao_api_exception(20)
    def add_adgroup(cls, nick, campaign_id, item_id, default_price, title, img_url):
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
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.adgroup)


if __name__ == '__main__':

    nick = '惠童米奇专卖店'
    campaign_id = 20285952
    default_price = 3
    title = '新款水壶 米奇不锈钢水壶  办公直饮用杯'
    item_id = 2254142062
    img_url = 'http://img02.taobaocdn.com/bao/uploaded/i2/TB11ewBGpXXXXXyXFXXXXXXXXXX_!!0-item_pic.jpg'
    print SimbaAdgroupAdd.add_adgroup(nick, campaign_id, item_id, default_price, title, img_url)
    
