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

from TaobaoSdk import SimbaKeywordsbyadgroupidGetRequest
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf import settings as tao_model_settings
from tao_models.common.decorator import  tao_api_exception
import traceback


logger = logging.getLogger(__name__)

class SimbaKeywordsbyadgroupidGet(object):
    """
    """
    
    @classmethod
    @tao_api_exception()
    def get_keyword_list_by_adgroup(cls, access_token, nick, adgroup_id):
        """
        get keyword list for some specific adgroup id
        """

        #try:
        #    i = 0
        #    stack = traceback.extract_stack()
        #    for line in stack:
        #        if 'celery' in line or '/usr/lib' in line:
        #            continue
        #        #logger.info('STACK:%s [%s]'%(line,cls))
        #        #print 'STACK:%s [%s]'%(cls,line)
        #        logger.info('STACK:%s %s'%(cls,line))
        #except Exception,e:
        #    print '>>>>>>>>>>>>>>>>>.'
        #    logger.info('%s is error ...'%cls)
        req = SimbaKeywordsbyadgroupidGetRequest()
        req.nick = nick
        req.adgroup_id = adgroup_id
        print "adgroup_id:", adgroup_id

        rsp = tao_model_settings.taobao_client.execute(req, access_token)[0]
        if not rsp.isSuccess():
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_code, sub_msg=rsp.sub_msg)
        logger.info('TARGET get keywords info by adgroup_id nick:%s adgroup_id:%s access_token:%s'%(nick, adgroup_id, access_token))
        return rsp.keywords


def test():
    #access_token = '6201c01b4ZZdb18b1773873390fe3ff66d1a285add9c10c520500325'
    access_token = '620181005f776f4b1bdfd5952ec7cfa172e008384c567a2520500325'
    nick = 'chinchinstyle'
    adgroup_id = 169462953 
    keywords = SimbaKeywordsbyadgroupidGet.get_keyword_list_by_adgroup(access_token, nick, adgroup_id)
    for keyword in keywords:
        print keyword.toDict()


if __name__ == '__main__':
    test()
