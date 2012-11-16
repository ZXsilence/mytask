#encoding=utf8
__author__ = 'lym liyangmin@maimiaotech.com'

import sys
import os
import  copy
import logging
import logging.config

#if __name__ == '__main__':
#    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
#    from xuanciw.settings import  trigger_envReady
#    logging.config.fileConfig('../xuanciw/consolelogger.conf')

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from tao_models.conf import set_env
    set_env.getEnvReady()
    logging.config.fileConfig('conf/consolelogger.conf')

from TaobaoSdk import SimbaKeywordsGetRequest
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf.settings import taobao_client
from tao_models.common.decorator import  tao_api_exception





logger = logging.getLogger(__name__)

class SimbaKeywordsGet(object):
    """

    keyword format:
    {
	"qscore" : "3",
	"word" : "男装t桖",
	"nick" : "密多帮巴",
	"campaign_id" : 7266464,
	"modified_time" : ISODate("2012-08-02T12:25:36Z"),
	"match_scope" : "4",
	"create_time" : ISODate("2012-07-29T16:00:29Z"),
	"is_default_price" : false,
	"is_garbage" : false,
	"keyword_id" : NumberLong("15504039924"),
	"audit_status" : "audit_pass",
	"max_price" : 26,
	"adgroup_id" : 119919947
    }
    """

    @classmethod
    @tao_api_exception
    def get_keyword_list_by_adgroup(cls, access_token, nick, adgroup_id):
        """
        get keyword list for some specific adgroup id
        """

        req = SimbaKeywordsGetRequest()
        req.nick = nick
        req.adgroup_id = adgroup_id

        rsp = taobao_client.execute(req, access_token)[0]
        if not rsp.isSuccess():
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_msg, sub_msg=rsp.sub_msg)

        return rsp.keywords


    @classmethod
    @tao_api_exception
    def get_keyword_list_by_keyword_ids(cls, access_token, nick, keyword_id_list):
        """
        get keyword list given by keyword ids
        """

        keyword_id_list = copy.deepcopy(keyword_id_list)
        MAX_KEYWORD_IDS = 200

        req = SimbaKeywordsGetRequest()
        req.nick = nick

        total_keyword_list = []
        while keyword_id_list:
            sub_keyword_id_list = keyword_id_list[:MAX_KEYWORD_IDS]
            keyword_id_list = keyword_id_list[MAX_KEYWORD_IDS:]

            req.keyword_ids = ",".join([str(k) for k in sub_keyword_id_list])
            logger.debug("get keyword info keyword_id_length:%s, nick:%s"%(len(sub_keyword_id_list), nick))
            rsp = taobao_client.execute(req, access_token)[0]
            if not rsp.isSuccess():
                raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_msg, sub_msg=rsp.sub_msg)

            total_keyword_list.extend(rsp.keywords)

        return total_keyword_list




def test():
    access_token = "6200b26ad6dde0735bc63c45618ca4f8bdfhfc1dfd08854100160612"
    sid = 71506259
    nick = '密多帮巴'
    keyword_id_list = [15749115197,15749115194, 15749114792, 15749114788]
    keyword_list = SimbaKeywordsGet.get_keyword_list_by_keyword_ids(access_token, nick, keyword_id_list)
    for keyword in keyword_list:
        print keyword.toDict()



if __name__ == '__main__':
    test()
