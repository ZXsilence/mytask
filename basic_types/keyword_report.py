#encoding=utf8
__author__ = 'chenke'


class KeywordReportUnit(object):
    __slots__ = ['data']

    def __init__(self, data):
        self.data = data

    def __getitem__(self, key):
        keys = ["nick"
               , "keywordid"
               , "keywordstr"
               , "adgroup_id"
               , "campaign_id"
               , "searchtype"
               , "source"
               , "date"
               , "impressions"
               , "click"
               , "cost"
               , "avgpos"
               , "directpay"
               , "indirectpay"
               , "pay"
               , "directpaycount"
               , "indirectpaycount"
               , "paycount"
               , "favitemcount"
               , "favshopcount"
               , "favcount"
               ]
        i = 0
        for k in keys:
            if k == key:
                return self.data[i]
            i += 1
        return None

class KeywordReportBase(object):
    __slots__ = ['data']

    def __init__(self, data):
        self.data = data

    def __getitem__(self, key):
        keys = ["nick"
               , "keywordid"
               , "keywordstr"
               , "adgroup_id"
               , "campaign_id"
               , "searchtype"
               , "source"
               , "date"
               , "impressions"
               , "click"
               , "cost"
               , "avgpos"
               ]
        i = 0
        for k in keys:
            if k == key:
                return self.data[i]
            i += 1
        return None

class KeywordReportEffect(object):
    __slots__ = ['data']

    def __init__(self, data):
        self.data = data

    def __getitem__(self, key):
        keys = ["nick"
               , "keywordid"
               , "keywordstr"
               , "adgroup_id"
               , "campaign_id"
               , "searchtype"
               , "source"
               , "date"
               , "directpay"
               , "indirectpay"
               , "directpaycount"
               , "indirectpaycount"
               , "favitemcount"
               , "favshopcount"
               ]
        i = 0
        for k in keys:
            if k == key:
                return self.data[i]
            i += 1
        return None

#{'searchtype': 'SEARCH', 'campaign_id': 6999088, 'cost': 0, 'date': datetime.datetime(2014, 5, 18, 0, 0), 'impressions': 4, 'click': 0, 'adgroup_id': 406914912, 'avgpos': 74.0, 'cpm': 0, 'ctr': 0, 'source': 'SUMMARY', 'cpc': 0, 'nick': '\xe5\xb0\x8f\xe8\x89\xbe\xe5\xae\xb6\xe7\x9a\x84\xe8\xa1\xa3\xe6\xa9\xb1', 'keywordid': 63518200501, 'keywordstr': '\xe5\xa5\xb3\xe5\xa4\x96\xe8\xa1\xab'}
#{'directpay': 0, 'campaign_id': 6999088, 'favitemcount': 0, 'indirectpaycount': 0, 'date': datetime.datetime(2014, 5, 18, 0, 0), 'adgroup_id': 406914912, 'favshopcount': 0, 'searchtype': 'SEARCH', 'source': 'SUMMARY', 'indirectpay': 0, 'nick': '\xe5\xb0\x8f\xe8\x89\xbe\xe5\xae\xb6\xe7\x9a\x84\xe8\xa1\xa3\xe6\xa9\xb1', 'keywordid': 63518200501, 'keywordstr': '\xe5\xa5\xb3\xe5\xa4\x96\xe8\xa1\xab', 'directpaycount': 0}
