#! /usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
from BaiduApiClient import BaiduApiClient
from BaiduApiClient import parse_soap_response 
import suds
import time,datetime

if __name__ == "__main__":
    import logging.config
    curr_path = os.path.dirname(__file__)
    logging.config.fileConfig(os.path.join(curr_path,'./consolelogger.conf'))

logger = logging.getLogger(__name__)


class NmsReportModel(object):
    baiduApiObj = BaiduApiClient('nms', 'ReportService')
    REPORT_OK_STATUS = 3
    
    @classmethod
    def get_report_ids(cls, username, access_token, performance_data, start_date, end_date, id_only, report_type, stat_range, stat_ids):
        cls.baiduApiObj.set_authheader(username, access_token)
        client = cls.baiduApiObj.client

        request = client.factory.create('getReportIdRequest')
        reportType = client.factory.create('getReportIdRequest.reportRequestType')
        reportType.performanceData = performance_data 
        reportType.startDate = start_date 
        reportType.endDate = end_date 
        reportType.idOnly = id_only 
        reportType.reportType = report_type
        request.statRange = stat_range 
        request.statIds = stat_ids 
        request.reportRequestType = reportType
        
        report_ids = client.service.getReportId(request.reportRequestType)
        res = client.last_received()

        res_dict, failure_dict = parse_soap_response(res)
        if failure_dict:
            logger.error("error info: %s", str(failure_dict))
            raise 
        return res_dict
        
    @classmethod
    def get_report_by_report_ids(cls, username, access_token, report_ids):
        cls.baiduApiObj.set_authheader(username, access_token)
        client = cls.baiduApiObj.client

        status = None
        retry = 1
        
        while(status != cls.REPORT_OK_STATUS): # 3 means report generated successfully
            if retry > 3:
                break
            time.sleep(5)
            status = client.service.getReportState(report_ids)
            retry += 1
        if status != cls.REPORT_OK_STATUS:
            raise
        
        res = client.last_received()

        res_dict, failure_dict = parse_soap_response(res)
        if failure_dict:
            logger.error("error info: %s", str(failure_dict))
            raise 
        return res_dict
        
    @classmethod
    def get_report_file_url(cls, username, access_token, report_id):
        cls.baiduApiObj.set_authheader(username, access_token)
        client = cls.baiduApiObj.client

        fileUrl = client.service.getReportFileUrl(report_id)
        
        res = client.last_received()

        res_dict, failure_dict = parse_soap_response(res)
        if failure_dict:
            logger.error("error info: %s", str(failure_dict))
            raise 
        return res_dict

if __name__ == "__main__":
    access_token = "0191f3e1-b059-4571-a190-db5aa166f1d3"
    username = "xh麦苗"
    performance_data = ['srch','click','cost','ctr','cpm','acp']
    start_date = datetime.datetime(int(2014),int(8),int(1))
    end_date = datetime.datetime(int(2014),int(8),int(4))
    id_only = False
    report_type = 2
    stat_range = 2
    stat_ids = [757446,757447,757448]
    res_dict = NmsReportModel.get_report_ids(username, access_token, performance_data, start_date, end_date, id_only, report_type, stat_range, stat_ids)
    #print res_dict['body']
    print res_dict['response']

    report_id = res_dict['response'].values()[0].values()[0] 
    res_dict = NmsReportModel.get_report_file_url(username, access_token, report_id)
    print res_dict

    res_dict = NmsReportModel.get_report_by_report_ids(username, access_token, [report_id])
    print res_dict
