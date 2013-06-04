#encoding=utf8
__author__ = 'lym liyangmin@maimiaotech.com'

import sys
import os
import  copy
import logging
import logging.config

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from tao_models.conf import set_env
    set_env.getEnvReady()
    from tao_models.conf.settings import set_taobao_client
    #set_taobao_client('12685542', '6599a8ba3455d0b2a043ecab96dfa6f9')
    set_taobao_client('21065688', '74aecdce10af604343e942a324641891')

from TaobaoSdk import SimbaKeywordsbykeywordidsGetRequest
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf import settings as tao_model_settings
from tao_models.common.decorator import  tao_api_exception


logger = logging.getLogger(__name__)

class SimbaKeywordsbykeywordidsGet(object):
    """
    """

    @classmethod
    @tao_api_exception()
    def _sub_get_keyword_list_by_keyword_ids(cls, access_token, nick, sub_keyword_id_list):
        req = SimbaKeywordsbykeywordidsGetRequest()
        req.nick = nick
        req.keyword_ids = ",".join([str(k) for k in sub_keyword_id_list])
        logger.debug("get keyword info keyword_id_length:%s, nick:%s"%(len(sub_keyword_id_list), nick))
        rsp = tao_model_settings.taobao_client.execute(req, access_token)[0]
        if not rsp.isSuccess():
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_msg, sub_msg=rsp.sub_msg)
        return rsp.keywords


    @classmethod
    def get_keyword_list_by_keyword_ids(cls, access_token, nick, keyword_id_list):
        """
        get keyword list given by keyword ids
        """

        keyword_id_list = copy.deepcopy(keyword_id_list)
        MAX_KEYWORD_IDS = 200 


        total_keyword_list = []
        while keyword_id_list:
            sub_keyword_id_list = keyword_id_list[:MAX_KEYWORD_IDS]
            keyword_id_list = keyword_id_list[MAX_KEYWORD_IDS:]
            sub_keywords = cls._sub_get_keyword_list_by_keyword_ids(access_token, nick, sub_keyword_id_list)
            total_keyword_list.extend(sub_keywords)

        return total_keyword_list


def test():
    #access_token = '6201c01b4ZZdb18b1773873390fe3ff66d1a285add9c10c520500325'
    access_token = '620181005f776f4b1bdfd5952ec7cfa172e008384c567a2520500325'
    nick = 'chinchinstyle'
    keyword_ids = [24497482994, 24497482990]
    keywords = SimbaKeywordsbykeywordidsGet.get_keyword_list_by_keyword_ids(access_token, nick, keyword_ids)
    for keyword in keywords:
        print keyword.toDict()


if __name__ == '__main__':
    test()
