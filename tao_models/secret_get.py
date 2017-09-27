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

from TaobaoSdk import TopSecretGetRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply
from TaobaoSdk import TaobaoClient
from TaobaoSdk.Exceptions import ErrorResponseException
from api_server.services.api_record_service import ApiRecordService
from api_server.conf.settings import APP_SETTINGS,SERVER_URL,API_NEED_SUBWAY_TOKEN,API_SOURCE

logger = logging.getLogger(__name__)


class SecretGet(object):

    @classmethod
    @tao_api_exception()
    def get_secret(cls,nick,soft_code = 'SYB',random_num = 'hzKfynCNH4ao35/Ks6xmSEUWr0fv3n4Z6KRd7OzlZA8='):
        req = TopSecretGetRequest()
        req.random_num = random_num
        rsp = ApiService.execute(req,nick,soft_code)
        data = {}
        if rsp.isSuccess():
            data = {'secret':rsp.secret,'interval':rsp.interval,'secret_version':rsp.secret_version,'max_interval':rsp.max_interval}
        return data


if __name__ == '__main__':
    nick = '麦苗科技001'
    SecretGet.get_secret(nick)
