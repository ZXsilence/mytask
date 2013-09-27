#encoding=utf8
__author__ = 'chenke'




class WordDeleteType(object):
    AUDIT_UNPASS = 1
    LOW_QSCORE = 2
    LOW_PV_OLD = 3
    SPECIAL_FILTER = 4
    DELETE_PERCENT = 5
    LOW_CLICK_OLD = 6
    IS_GARBAGE = 7

    USER_DELETE = 10
    LOW_PV_MAX_PRICE = 11
    LOW_PV_BEST_POSITION = 12
    
    FILTER_WORDS = 13
    LOW_RELEVANCE = 14
