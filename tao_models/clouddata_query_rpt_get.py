import os
import sys
import json
from datetime import datetime


if __name__ == "__main__":
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))   

from tao_models.clouddata_mbp_data_get import OpenTaobao


class ClouddataQueryRptGet(object):
    """
    """
     
    @classmethod
    def _get_query_rpt(cls, sid, sdate, edate, offset, limit):
        params = {
            'method':'taobao.clouddata.mbp.data.get',
            'session':"620151603c6d2a15d18f0996ZZ0e51a14d1d47350f7c375520500325",
            'sql_id':'3472' ,
            'parameter':'shop_id=%s,sdate=%s,edate=%s,sub_offset=%s,sub_limit=%s' % (sid, edate, edate, offset, limit)
	}

        op = OpenTaobao('12685542','6599a8ba3455d0b2a043ecab96dfa6f9')
        ret = json.loads(op.get_result(params))
        column_list = ret["clouddata_mbp_data_get_response"]["column_list"]["string"]
        query_rows = ret["clouddata_mbp_data_get_response"]["row_list"]
        rpt_list = []
        if "query_row" not in query_rows:
            return rpt_list
        query_rows =query_rows["query_row"]
        for query_row in query_rows:
            row = query_row["values"]["string"]
            rpt = dict(zip(column_list, row))
            cls._conv_query_rpt(rpt)
            rpt_list.append(rpt)

    	return rpt_list

    @classmethod
    def _conv_query_rpt(cls, rpt):
        int_fields = ["shop_id", "seller_id", "auction_id", "impressions", "click", "uv", "alipay_winner_num", "alipay_auction_num", "alipay_trade_num"]
        date_fields = ["thedate", "dt"]
        float_fields = ["alipay_trade_amt"]
        for key in rpt.keys():
            if key in int_fields:
                rpt[key] = int(rpt[key])
            elif key in date_fields:
                rpt[key] = datetime.strptime(rpt[key], "%Y%m%d") 
            elif key in float_fields:
                rpt[key] = float(rpt[key])
         

     

    @classmethod
    def get_query_rpt(cls, sid, sdate, edate):
        sdate = sdate.strftime("%Y%m%d")
        edate = edate.strftime("%Y%m%d")
        limit = 5000
        offset = 0
        rpt_list = []
        while True:
            sub_rpt_list = cls._get_query_rpt(sid, sdate, edate, offset, limit)
            rpt_list.extend(sub_rpt_list)
            if len(sub_rpt_list) < limit:
                break

            offset += limit

        return rpt_list


if __name__ == "__main__":
    sid = 103535615
    sdate = datetime(2014, 3, 10) 
    edate = datetime(2014, 3, 26) 
    rpt_list = ClouddataQueryRptGet.get_query_rpt(sid, sdate, edate)
    print rpt_list
