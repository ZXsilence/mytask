#encoding=utf8
__author__ = "xieguanfu"

import sys
import os
import copy
import logging
import logging.config

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from tao_models.conf.settings import set_taobao_client
    set_taobao_client('21065688', '74aecdce10af604343e942a324641891')

from TaobaoSdk import LogisticsAddressSearchRequest 
from TaobaoSdk.Exceptions import  ErrorResponseException
from tao_models.conf import    settings as tao_model_settings
from tao_models.common.decorator import  tao_api_exception

logger = logging.getLogger(__name__)


class LogisticsAddressSearch(object):
    """
        获取卖家地址库
    """

    @classmethod
    @tao_api_exception()
    def get_logistics_address(cls, access_token):
        req =LogisticsAddressSearchRequest()
        rsp = tao_model_settings.taobao_client.execute(req, access_token)[0]
        if not rsp.isSuccess():
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg,sub_code=rsp.sub_code,sub_msg =rsp.sub_msg)
        return rsp.addresses
   
if __name__=="__main__":
    access_token="62001221e2ef7018e141da64620191ZZ7c7fa4d6a7ccadb871727117"
    addresses=LogisticsAddressSearch.get_logistics_address(access_token)
    for address in addresses:
        print address.toDict()
