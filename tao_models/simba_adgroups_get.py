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

from TaobaoSdk import SimbaAdgroupsGetRequest
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf.settings import  taobao_client
from tao_models.common.decorator import  tao_api_exception

logger = logging.getLogger(__name__)

class SimbaAdgroupsGet(object):
    """
    {
	"_id" : 119919205,
	"default_price" : 21,
	"online_status" : "online",
	"nonsearch_max_price" : 21,
	"num_iid" : NumberLong("18866976333"),
	"campaign_id" : 7266464,
	"modified_time" : ISODate("2012-07-30T22:10:07Z"),
	"category_ids" : "30 50011153",
	"nick" : "密多帮巴",
	"create_time" : ISODate("2012-07-25T16:13:55Z"),
	"is_nonsearch_default_price" : false,
	"offline_type" : "online",
	"adgroup_id" : 119919205
    }
    """

    PAGE_SIZE = 200

    @classmethod
    @tao_api_exception()
    def get_adgroup_list_by_campaign(cls, access_token, nick, campaign_id):
        """
        given a campaign_id, get the adgroup list in this campaign
        """

        adgroup_list = []

        req = SimbaAdgroupsGetRequest()
        req.page_size = cls.PAGE_SIZE
        req.nick = nick
        req.campaign_id = campaign_id
        req.page_no = 1

        #first_call
        rsp = taobao_client.execute(req, access_token)[0]
        if not rsp.isSuccess():
            print "campaign_id:", campaign_id, "sub_code:", rsp.sub_msg
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

        for page_no in range(2,total_pages+1):
            req.page_no = page_no
            rsp = taobao_client.execute(req, access_token)[0]
            if not rsp.isSuccess():
                print "sub_code:", rsp.sub_msg
                raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_msg, sub_msg=rsp.sub_msg)
            adgroup_list.extend(rsp.adgroups.adgroup_list)

        logger.debug("actually get [%i] adgroups in campaign_id [%i]"%(len(adgroup_list), campaign_id))
        return adgroup_list

    @classmethod
    @tao_api_exception()
    def get_adgroup_list_by_adgroup_ids(cls, access_token, nick, adgroup_id_list):

        MAX_ADGROUP_IDS = 200

        req = SimbaAdgroupsGetRequest()
        req.nick = nick
        #useless page_size, page_no, but required when post the request
        req.page_size = 200
        req.page_no = 1

        total_adgroup_list = []
        while adgroup_id_list:
            sub_adgroup_id_list = adgroup_id_list[:MAX_ADGROUP_IDS]
            adgroup_id_list = adgroup_id_list[MAX_ADGROUP_IDS:]

            req.adgroup_ids = ",".join([str(k) for k in sub_adgroup_id_list])
            logger.debug("get adgroup info adgroup_length:%s nick:%s"%(len(sub_adgroup_id_list), nick))
            rsp = taobao_client.execute(req, access_token)[0]
            if not rsp.isSuccess():
                raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_msg, sub_msg=rsp.sub_msg)

            total_adgroup_list.extend(rsp.adgroups.adgroup_list)

        return total_adgroup_list

    @classmethod
    @tao_api_exception(8)
    def get_adgroup_count(cls, access_token, nick, campaign_id):
        """
        given a campaign_id, get the adgroup list in this campaign
        """
        req = SimbaAdgroupsGetRequest()
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




if __name__ == '__main__':
    SimbaAdgroupsGet.PAGE_SIZE = 200
    adgroup_list = SimbaAdgroupsGet.get_adgroup_list_by_campaign('6200b26ad6dde0735bc63c45618ca4f8bdfhfc1dfd08854100160612', '密多帮巴', 7214875)
    adgroup_id_list = []
    for adgroup in adgroup_list:
        adgroup_id_list.append(adgroup.adgroup_id)

    print len(adgroup_id_list)

    new_adgroup_list = SimbaAdgroupsGet.get_adgroup_list_by_adgroup_ids('6200b26ad6dde0735bc63c45618ca4f8bdfhfc1dfd08854100160612', '密多帮巴', adgroup_id_list)
    print len(new_adgroup_list)
