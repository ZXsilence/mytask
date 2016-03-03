#encoding=utf8
__author__ = 'zhoujiebing@maimiaotech.com'

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

import simplejson
from TaobaoSdk import TaobaoClient
from TaobaoSdk import AlibabaAliqinTaSmsNumSendRequest
from TaobaoSdk.Exceptions.ErrorResponseException import ErrorResponseException
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply
from api_server.conf.settings import APP_SETTINGS,SERVER_URL,API_HOST,API_PORT

logger = logging.getLogger(__name__)

class AliqinTaSmsNumSend(object):

    @classmethod
    @tao_api_exception(2)
    def send_sms(cls,mobiles,sms_param,sms_template_code,sign_name = '麦苗'):
        """
        暂时不要使用此方法
        """
        soft_code = 'SYB'
        req = AlibabaAliqinTaSmsNumSendRequest()
        req.sms_type='normal'
        req.sms_free_sign_name = sign_name
        req.sms_param = simplejson.dumps(sms_param)
        req.rec_num = mobiles
        req.sms_template_code = sms_template_code
        rsp = ApiService.execute(req,None,soft_code)
        return change_obj_to_dict_deeply(rsp.result)

    @classmethod
    @tao_api_exception(2)
    def send_sms_sdk(cls,mobiles,sms_param,sms_template_code,sign_name = '麦苗'):
        soft_code = 'SYB'
        app_key = APP_SETTINGS[soft_code]['app_key']
        app_secret = APP_SETTINGS[soft_code]['app_secret']
        req = AlibabaAliqinTaSmsNumSendRequest()
        req.sms_type='normal'
        req.sms_free_sign_name = sign_name
        req.sms_param = simplejson.dumps(sms_param)
        req.rec_num = mobiles
        req.sms_template_code = sms_template_code
        params = ApiService.getReqParameters(req)
        taobao_client = TaobaoClient(SERVER_URL,app_key,app_secret)
        rsp = ApiService.getResponseObj(taobao_client.execute(params, ''))
        if not rsp.isSuccess():
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_code, sub_msg=rsp.sub_msg)
        result = change_obj_to_dict_deeply(rsp.result)
        if result.get('success'):
            return True
        else:
            raise ErrorResponseException(code='send_fail', msg=result['msg'], sub_code='send_fail', sub_msg=result['msg'])

if __name__ == '__main__':
    mobile = 15068116152
    import simplejson as json
    sms_param = {'nick':u'麦苗科技','softname':u'省油宝','code':'95279'}
    #验证码模板
    sms_template_code = 'SMS_2840119'
    import pdb; pdb.set_trace()  # XXX BREAKPOINT
    AliqinTaSmsNumSend.send_sms_sdk(mobile,sms_param,sms_template_code)
