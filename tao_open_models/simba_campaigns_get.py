#encoding=utf8
__author__ = 'lym liyangmin@maimiaotech.com'

import sys
import os
import logging
import logging.config

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from xuanciw.settings import  trigger_envReady
    logging.config.fileConfig('../xuanciw/consolelogger.conf')

from TaobaoSdk import SimbaCampaignsGetRequest
from TaobaoSdk.Exceptions import  ErrorResponseException

from xuanciw.settings import  taobao_client
from common.decorator import  tao_api_exception


logger = logging.getLogger(__name__)


class SimbaCampaignsGet(object):

    """

    campaign_format:
    {
	"online_status" : "online",
	"settle_status" : "online",
	"campaign_id" : 7295832,
	"modified_time" : ISODate("2012-06-29T09:18:55Z"),
	"nick" : "密多帮巴",
	"create_time" : ISODate("2012-06-16T22:35:08Z"),
	"title" : "喜宝计划201206290918"
    }

    """

    @classmethod
    @tao_api_exception
    def get_campaign_list(cls, access_token, nick):
        """
        get campaign list for a shop.

        return: campaign _list (type:http://api.taobao.com/apidoc/dataStruct.htm?path=cid:46-dataStructId:10141-apiId:10557-invokePath:campaigns)
        """
        req = SimbaCampaignsGetRequest()
        req.nick = nick

        rsp = taobao_client.execute(req, access_token)[0]
        if not rsp.isSuccess():
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_code, sub_msg=rsp.sub_msg)
        return rsp.campaigns

