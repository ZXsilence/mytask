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
    #set_taobao_client('12685542', '6599a8ba3455d0b2a043ecab96dfa6f9')
    set_taobao_client('21065688', '74aecdce10af604343e942a324641891')

from TaobaoSdk import SimbaAdgroupsbycampaignidGetRequest
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf.settings import  taobao_client
from tao_models.common.decorator import  tao_api_exception

logger = logging.getLogger(__name__)

class SimbaAdgroupsbycampaignidGet(object):
    """
    """

    PAGE_SIZE = 200

    @classmethod
    @tao_api_exception()
    def get_adgroup_list_by_campaign(cls, access_token, nick, campaign_id, max_pages=30):
        """
        given a campaign_id, get the adgroup list in this campaign
        """

        adgroup_list = []

        req = SimbaAdgroupsbycampaignidGetRequest()
        req.page_size = cls.PAGE_SIZE
        req.nick = nick
        req.campaign_id = campaign_id
        req.page_no = 1

        #first_call
        rsp = taobao_client.execute(req, access_token)[0]
        if not rsp.isSuccess():
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_msg, sub_msg=rsp.sub_msg)
        logger.debug("[%s] adgroups in campaign_id [%s]"%(rsp.adgroups.total_item,campaign_id))
        if not rsp.adgroups.total_item:
            logger.debug("no adgroup in campaign:%i"%(campaign_id))
            return adgroup_list
        adgroup_list.extend(rsp.adgroups.adgroup_list)
        # continue to call if more than one page
        if not rsp.adgroups.total_item%cls.PAGE_SIZE:
            total_pages = rsp.adgroups.total_item/cls.PAGE_SIZE
        else:
            total_pages = rsp.adgroups.total_item/cls.PAGE_SIZE + 1
        if total_pages > max_pages:
            total_pages = max_pages

        for page_no in range(2,total_pages+1):
            req.page_no = page_no
            rsp = taobao_client.execute(req, access_token)[0]
            if not rsp.isSuccess():
                raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_msg, sub_msg=rsp.sub_msg)
            adgroup_list.extend(rsp.adgroups.adgroup_list)

        logger.debug("actually get [%i] adgroups in campaign_id [%i]"%(len(adgroup_list), campaign_id))
        return adgroup_list


    @classmethod
    @tao_api_exception(8)
    def get_adgroup_count(cls, access_token, nick, campaign_id):
        """
        given a campaign_id, get the adgroup list in this campaign
        """
        req = SimbaAdgroupsbycampaignidGetRequest()
        req.page_size = cls.PAGE_SIZE
        req.nick = nick
        req.campaign_id = campaign_id
        req.page_no = 1 
        try:
            rsp = taobao_client.execute(req, access_token)[0]
        except Exception, data:
            raise ApiExecuteException

        if not rsp.isSuccess():
            logger.error("get_adgroup_count error nick [%s] msg [%s] sub_msg [%s]" %(nick, rsp.msg, rsp.sub_msg))
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_msg, sub_msg=rsp.sub_msg)
        return rsp.adgroups.total_item


    @classmethod
    @tao_api_exception()
    def get_adgroup_list_by_campaign_with_overview(cls, access_token, nick, campaign_id, max_pages=1):
        """
        given a campaign_id, get the adgroup list in this campaign
        """

        adgroup_list = []

        req = SimbaAdgroupsbycampaignidGetRequest()
        req.page_size = cls.PAGE_SIZE
        req.nick = nick
        req.campaign_id = campaign_id
        req.page_no = 1

        #first_call
        rsp = taobao_client.execute(req, access_token)[0]
        if not rsp.isSuccess():
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_msg, sub_msg=rsp.sub_msg)
        logger.debug("[%s] adgroups in campaign_id [%s]"%(rsp.adgroups.total_item,campaign_id))
        if not rsp.adgroups.total_item:
            logger.debug("no adgroup in campaign:%i"%(campaign_id))
            return {'total_item':0, 'adgroup_list':adgroup_list}
        adgroup_list.extend(rsp.adgroups.adgroup_list)
        # continue to call if more than one page
        if not rsp.adgroups.total_item%cls.PAGE_SIZE:
            total_pages = rsp.adgroups.total_item/cls.PAGE_SIZE
        else:
            total_pages = rsp.adgroups.total_item/cls.PAGE_SIZE + 1
        if total_pages > max_pages:
            total_pages = max_pages

        for page_no in range(2,total_pages+1):
            req.page_no = page_no
            rsp = taobao_client.execute(req, access_token)[0]
            if not rsp.isSuccess():
                raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_msg, sub_msg=rsp.sub_msg)
            adgroup_list.extend(rsp.adgroups.adgroup_list)

        logger.debug("actually get [%i] adgroups in campaign_id [%i]"%(len(adgroup_list), campaign_id))
        return {'total_item':rsp.adgroups.total_item, 'adgroup_list':adgroup_list}


def test():
    #access_token = '6201c01b4ZZdb18b1773873390fe3ff66d1a285add9c10c520500325'
    access_token = '620181005f776f4b1bdfd5952ec7cfa172e008384c567a2520500325'
    nick = 'chinchinstyle'
    campaign_id = 3367690 
    adgroups = SimbaAdgroupsbycampaignidGet.get_adgroup_list_by_campaign(access_token, nick, campaign_id)
    for adgroup in adgroups:
        print adgroup.toDict()

    print SimbaAdgroupsbycampaignidGet.get_adgroup_count(access_token, nick, campaign_id)
    print SimbaAdgroupsbycampaignidGet.get_adgroup_list_by_campaign_with_overview(access_token, nick, campaign_id)

if __name__ == '__main__':
    test()
