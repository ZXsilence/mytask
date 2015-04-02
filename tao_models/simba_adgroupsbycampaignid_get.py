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

from TaobaoSdk import SimbaAdgroupsbycampaignidGetRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply
from TaobaoSdk.Exceptions import ErrorResponseException 

logger = logging.getLogger(__name__)

class SimbaAdgroupsbycampaignidGet(object):

    PAGE_SIZE = 200

    @classmethod
    @tao_api_exception()
    def get_adgroup_list_by_campaign(cls, nick, campaign_id, max_pages=30):

        adgroup_list = []

        req = SimbaAdgroupsbycampaignidGetRequest()
        req.page_size = cls.PAGE_SIZE
        req.nick = nick
        req.campaign_id = campaign_id
        req.page_no = 1

        soft_code = None
        try:
            rsp = ApiService.execute(req,nick,soft_code)
        except ErrorResponseException,e:
            if e.sub_code == 'isp.internal-error' and e.sub_msg == 'getADGroupsByCampaignId':
                return adgroup_list
            raise e
        logger.debug("[%s] adgroups in campaign_id [%s]"%(rsp.adgroups.total_item,campaign_id))
        if not rsp.adgroups.total_item:
            logger.debug("no adgroup in campaign:%i"%(campaign_id))
            return adgroup_list
        adgroup_list.extend(rsp.adgroups.adgroup_list)
        if not rsp.adgroups.total_item%cls.PAGE_SIZE:
            total_pages = rsp.adgroups.total_item/cls.PAGE_SIZE
        else:
            total_pages = rsp.adgroups.total_item/cls.PAGE_SIZE + 1
        if total_pages > max_pages:
            total_pages = max_pages

        for page_no in range(2,total_pages+1):
            req.page_no = page_no
            soft_code = None
            rsp = ApiService.execute(req,nick,soft_code)
            adgroup_list.extend(rsp.adgroups.adgroup_list)

        logger.debug("actually get [%i] adgroups in campaign_id [%i]"%(len(adgroup_list), campaign_id))
        return change_obj_to_dict_deeply(adgroup_list)


    @classmethod
    @tao_api_exception(8)
    def get_adgroup_count(cls, nick, campaign_id):
        req = SimbaAdgroupsbycampaignidGetRequest()
        req.page_size = cls.PAGE_SIZE
        req.nick = nick
        req.campaign_id = campaign_id
        req.page_no = 1 
        soft_code = None
        #rsp = ApiService.execute(req,nick,soft_code)
        try:
            rsp = ApiService.execute(req,nick,soft_code)
        except ErrorResponseException,e:
            if e.sub_code == 'isp.internal-error' and e.sub_msg == 'getADGroupsByCampaignId':
                return 0
            raise e
        total_item = rsp.adgroups.total_item
        if not total_item:
            return 0
        return change_obj_to_dict_deeply(total_item)

    @classmethod
    @tao_api_exception()
    def get_adgroup_list_by_campaign_with_overview(cls, nick, campaign_id, max_pages=1):
        adgroup_list = []
        req = SimbaAdgroupsbycampaignidGetRequest()
        req.page_size = cls.PAGE_SIZE
        req.nick = nick
        req.campaign_id = campaign_id
        req.page_no = 1
        soft_code = None
        #rsp = ApiService.execute(req,nick,soft_code)
        try:
            rsp = ApiService.execute(req,nick,soft_code)
        except ErrorResponseException,e:
            if e.sub_code == 'isp.internal-error' and e.sub_msg == 'getADGroupsByCampaignId':
                return {'total_item':0, 'adgroup_list':adgroup_list}
            raise e
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
            soft_code = None
            rsp = ApiService.execute(req,nick,soft_code)
            adgroup_list.extend(rsp.adgroups.adgroup_list)

        logger.debug("actually get [%i] adgroups in campaign_id [%i]"%(len(adgroup_list), campaign_id))
        return {'total_item':change_obj_to_dict_deeply(rsp.adgroups.total_item), 'adgroup_list':change_obj_to_dict_deeply(adgroup_list)}

    @classmethod
    @tao_api_exception()
    def get_adgroup_count_by_campaign_id(cls, nick, campaign_id):
        req = SimbaAdgroupsbycampaignidGetRequest()
        req.page_size = 1
        req.nick = nick
        req.campaign_id = campaign_id
        req.page_no = 1
        soft_code = None
        count = 0
        try:
            rsp = ApiService.execute(req,nick,soft_code)
        except ErrorResponseException,e:
            if e.sub_code == 'isp.internal-error' and e.sub_msg == 'getADGroupsByCampaignId':
                return count
            raise e
        if not rsp.adgroups.total_item:
            logger.debug("no adgroup in campaign:%i"%(campaign_id))
            return count
        return rsp.adgroups.total_item


def test():
    nick = '美之雅家具'
    campaign_id =3075359 
    nick = 'tmmly5520'
    campaign_id = 3432596
    #nick = 'chinchinstyle'
    #campaign_id = 3328400
    adgroups = SimbaAdgroupsbycampaignidGet.get_adgroup_list_by_campaign(nick, campaign_id)
    ids = [obj['adgroup_id'] for obj in adgroups]
    #open('/tmp/a','w').write(str(ids))
    print len(adgroups)

    print SimbaAdgroupsbycampaignidGet.get_adgroup_count_by_campaign_id(nick, campaign_id)

if __name__ == '__main__':
    test()
