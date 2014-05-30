#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wulingping
@contact: wulingping@maimiaotech.com
@date: 2013-09-25 14:04
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""
import sys
import urllib
import urllib2
import time
import hashlib 
import simplejson as json
import datetime

class OpenTaobao:
    def __init__(self,app_key,sercet_code):
        self.app_key = app_key
        self.sercet_code = sercet_code
    def get_time(self):
        t = time.localtime()
        return time.strftime('%Y-%m-%d %X', t)
    def get_sign(self,params):
        params['format'] = 'json' 
        params.update({'app_key':self.app_key,'timestamp':self.get_time(),'v':'2.0'})
        src = self.sercet_code + ''.join(["%s%s" % (k, v) for k, v in sorted(params.iteritems())])
        return hashlib.md5(src).hexdigest().upper()
    def get_result(self,params):
        params['sign'] = self.get_sign(params)
        form_data = urllib.urlencode(params)
        #return urllib2.urlopen('http://223.5.20.253:8002/router/rest', form_data).read()
        return urllib2.urlopen('http://gw.api.taobao.com/router/rest', form_data).read()


op = OpenTaobao('12685542','6599a8ba3455d0b2a043ecab96dfa6f9')
# the smallest taobao api python sdk
#
###############################################
#
# Usage:

def decode_clouddata(str_res):
    dict_res = json.loads(str_res)
    list_res = []
    columns = dict_res.get('clouddata_mbp_data_get_response', {}).get('column_list', {}).get('string', [])
    rows = dict_res.get('clouddata_mbp_data_get_response', {}).get('row_list',{}).get('query_row', []) 
    elements = []
    for row in rows:
        values = row.get('values', {}).get('string', [])
        element = {}
        for i in range(len(values)):
            element[columns[i]] = values[i]
        elements.append(element)
    return elements
    
def _get_data_list_by_sid(sid, sql_id,sub_offset,sub_limit):
    n = datetime.datetime.now()
    elements = []
    
    dt = n-datetime.timedelta(days=1)
    sdate = dt-datetime.timedelta(days=90)
    edate = dt
    dt_str = dt.strftime("%Y%m%d")
    sdate_str = sdate.strftime("%Y%m%d")
    edate_str = edate.strftime("%Y%m%d")
    parameter = "shop_id="+str(sid)+",sdate="+sdate_str+",edate="+edate_str+",dt="+dt_str+",sub_offset="+str(sub_offset)+",sub_limit="+str(sub_limit)

    print parameter
    params = {
        'method':'taobao.clouddata.mbp.data.get',
        'session':"620151603c6d2a15d18f0996ZZ0e51a14d1d47350f7c375520500325",
        'sql_id' : sql_id,
        'parameter' : parameter 
    }

    str_res = op.get_result(params)
    elements.extend(decode_clouddata(str_res))

    return elements

class ClouddataMbpDataGet(object):

    @classmethod
    def get_query_list_by_sid(cls, sid):
        elements = []
        elements.extend(_get_data_list_by_sid(sid, '3378'))
        elements_uniq = []
        signatures = {}
        for e in elements:
            signature = e['auction_id']+'|'+e['query']+'|'+e['thedate']
            if signatures.has_key(signature):
                continue
            signatures[signature] = 1
            elements_uniq.append(e)
        print len(elements),len(elements_uniq)
        return elements_uniq

    @classmethod
    def get_shop_rpt_hour(cls,sid):
        rpt_list = _get_data_list_by_sid(sid,'3939')
        return rpt_list
    
    @classmethod
    def get_shop_rpt_hour_30d(cls,sid,sub_offset,sub_limit):
        rpt_list = _get_data_list_by_sid(sid,'3971',sub_offset,sub_limit)
        return rpt_list

    @classmethod
    def get_shop_rpt_region(cls,sid):
        rpt_list = _get_data_list_by_sid(sid,'3941')
        return rpt_list

    @classmethod
    def get_shop_rpt_region_30d(cls,sid,sub_offset,sub_limit):
        rpt_list = _get_data_list_by_sid(sid,'3973',sub_offset,sub_limit)
        return rpt_list


if __name__ == "__main__":
    sid = int(sys.argv[1])
    #query_list = ClouddataMbpDataGet.get_query_list_by_sid(sid)
    #print len(query_list)
    #for e in query_list:
        #if int(e['alipay_trade_num']) >= 1:
            #res = "%s\t%s\t%s\t%s\t%s" % (e['query'], e['auction_id'], e['click'], e['alipay_trade_num'], e['thedate'])
            #print res
    ###############################################


    rpt_list_hour = ClouddataMbpDataGet.get_shop_rpt_hour_30d(sid,0,5000)
    date_list = []
    for item in rpt_list_hour:
        if item['thedate'] not in date_list:
            date_list.append(item['thedate'])
    print len(date_list)

