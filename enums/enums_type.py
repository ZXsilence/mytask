#encoding=utf8
__author__ = 'chenke'


class ExtendType(object):
    DEFAULT = 0
    PV_FIRST = 1
    CONV_FIRST = 2
    MONEY_FIRST = 3
    REL_AND_PV = 4

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

    USER_DELETE_TAOBAO = 15

class OperationType(object):

    DELETE_AUDIT_UNPASS = 1
    DELETE_LOW_QSCORE = 2
    DELETE_LOW_PV_OLD = 3
    DELETE_DELETE_PERCENT = 4
    DELETE_LOW_CLICK_OLD = 5
    #DELETE_IS_GARGABE = 6
    DELETE_IS_GARBAGE = 6
    DELETE_USER_DELETE = 7
    DELETE_LOW_PV_MAX_PRICE = 8
    DELETE_LOW_PV_BEST_POSITION = 9
    DELETE_FILTER_WORDS = 10
    DELETE_LOW_RELEVANCE = 11
    DELETE_DIRECTOR = 12
    DELETE_HISTORY_NORMAL = 13
    DELETE_LOW_PV_BY_ADGROUP_CPC = 15
    DELETE_USER_DELETE_TAOBAO = 16

    UPDATE_PRICE_ROI_GOOD_INCRE_PRICE = 101
    UPDATE_PRICE_ROI_PREDICT_GOOD_INCRE_PRICE = 102
    UPDATE_PRICE_ROI_BAD_DECRE_PRICE = 103
    UPDATE_PRICE_COST_SUFF_INCRE_PRICE = 104
    UPDATE_PRICE_COST_FULL_DECRE_PRICE = 105
    UPDATE_PRICE_GARBAGE_INCRE_PRICE = 106
    UPDATE_PRICE_MINIMIZE_CPC_MAX = 107
    UPDATE_PRICE_TO_INCREASE_COST = 108
    UPDATE_PRICE_TO_DECREASE_COST = 109
    UPDATE_PRICE_TO_APPROVE_ROI = 110
    UPDATE_PRICE_DIRECTOR = 111
    UPDATE_PRICE_HISTORY_NORMAL = 112 
    UPDATE_PRICE_COST_LESS_THAN_LIMIT_INCRE_PRICE = 113 
    UPDATE_PRICE_CUSTOM = 114 

    
    KEEP_NORMAL = 201

    IGNORE_KEYWORD_NOT_EXIST = 301
    IGNORE_KEYWORD_NOT_HANDLE = 302
    IGNORE_NOT_MANAGE_BY_SOFT = 303
    IGNORE_CREATE_TIME_SHORT = 304
    IGNORE_MODIFIED_TIME_SHORT = 305
    IGNORE_KEYWORD_REPORT_NONE = 306
    IGNORE_CAMPAIGN_REPORT_NONE = 307
    IGNORE_CAMPAIGN_STOPPED = 308

    ADD_NORMAL = 401
    ADD_KEYWORD_NORMAL = 402 
    ADD_KEYWORD_INITIAL = 403
    ADD_KEYWORD_DIRECTOR = 404
    ADD_KEYWORD_HISTORY_NORMAL = 405
    
    ADD_ADGROUP_NORMAL = 501
    DELETE_ADGROUP_NORMAL = 502
    DELETE_ADGROUP_INITIAL = 503
    DELETE_ADGROUP_HISTORY_NORMAL = 504

    ALL_DELETE_TYPES = [
        DELETE_AUDIT_UNPASS,
        DELETE_LOW_QSCORE,
        DELETE_LOW_PV_OLD,
        DELETE_DELETE_PERCENT,
        DELETE_LOW_CLICK_OLD,
        DELETE_IS_GARBAGE,
        DELETE_USER_DELETE,
        DELETE_LOW_PV_MAX_PRICE,
        DELETE_LOW_PV_BEST_POSITION,
        DELETE_FILTER_WORDS,
        DELETE_LOW_RELEVANCE,
        DELETE_DIRECTOR,
        DELETE_HISTORY_NORMAL,
        DELETE_LOW_PV_BY_ADGROUP_CPC,
        DELETE_USER_DELETE_TAOBAO 
    ]

    ALL_UPDATE_TYPES = [
        UPDATE_PRICE_ROI_GOOD_INCRE_PRICE,
        UPDATE_PRICE_ROI_PREDICT_GOOD_INCRE_PRICE,
        UPDATE_PRICE_ROI_BAD_DECRE_PRICE,
        UPDATE_PRICE_COST_SUFF_INCRE_PRICE, 
        UPDATE_PRICE_COST_FULL_DECRE_PRICE,
        UPDATE_PRICE_GARBAGE_INCRE_PRICE,
        UPDATE_PRICE_MINIMIZE_CPC_MAX,
        UPDATE_PRICE_TO_INCREASE_COST,
        UPDATE_PRICE_TO_DECREASE_COST,
        UPDATE_PRICE_TO_APPROVE_ROI,
        UPDATE_PRICE_DIRECTOR,
        UPDATE_PRICE_HISTORY_NORMAL,
        UPDATE_PRICE_COST_LESS_THAN_LIMIT_INCRE_PRICE,
        UPDATE_PRICE_CUSTOM
    ]


    ALL_ADD_TYPES = [
        ADD_NORMAL,
        ADD_KEYWORD_NORMAL,
        ADD_KEYWORD_INITIAL,
        ADD_KEYWORD_DIRECTOR,
        ADD_KEYWORD_HISTORY_NORMAL
    ]

OPTTYPE_COMMENT = {
    OperationType.DELETE_AUDIT_UNPASS: "关键词审核未通过，已经删除"
    , OperationType.DELETE_LOW_QSCORE : "关键词质量分过低，已经删除"
    , OperationType.DELETE_LOW_PV_OLD : "关键词最近一段时间展现量过低，已经删除"
    , OperationType.DELETE_DELETE_PERCENT : "关键词在计划中相对表现较差，已经删除"
    , OperationType.DELETE_LOW_CLICK_OLD : "关键词最近一段时间点击量过低，已经删除"
    , OperationType.DELETE_IS_GARBAGE : "关键词被淘宝判断为垃圾词，已经删除"
    , OperationType.DELETE_USER_DELETE : "关键词被用户手工删除"
    , OperationType.DELETE_USER_DELETE_TAOBAO : "关键词被用户在直通车手工删除"
    
    , OperationType.DELETE_LOW_PV_MAX_PRICE : "关键词已经达到用户设置的最高出价，仍然没有展现，已经删除"
    , OperationType.DELETE_LOW_PV_BEST_POSITION : "关键词已经排在首页，仍然没有展现，已经删除"
    
    , OperationType.DELETE_FILTER_WORDS : "根据用户设置的过滤词，关键词已经删除"
    , OperationType.DELETE_LOW_RELEVANCE : "由于关键词相关性不佳，已经删除"
    , OperationType.DELETE_DIRECTOR : "加力计划优化，发现关键词表现不佳，已经删除"
    , OperationType.DELETE_HISTORY_NORMAL : "关键词已经被删除(历史记录未区分类型)"
    , OperationType.DELETE_LOW_PV_BY_ADGROUP_CPC : "关键词已经超出推广组cpc较多，仍然没有展现，已经删除"

    , OperationType.UPDATE_PRICE_ROI_GOOD_INCRE_PRICE : "关键词最近一段时间效果好于计划整体，加大投入"
    , OperationType.UPDATE_PRICE_ROI_PREDICT_GOOD_INCRE_PRICE : "系统预估关键词ROI潜力较大，适当加大投入"
    , OperationType.UPDATE_PRICE_ROI_BAD_DECRE_PRICE : "关键词最近一段时间效果低于计划整体，减小投入"
    , OperationType.UPDATE_PRICE_COST_SUFF_INCRE_PRICE : "计划花费过低，根据报表，关键词加大投入"
    , OperationType.UPDATE_PRICE_COST_FULL_DECRE_PRICE : "计划花费过高，根据报表，关键词减小投入"
    , OperationType.UPDATE_PRICE_GARBAGE_INCRE_PRICE : "关键词被淘宝判定为无展现词，加大投入"
    , OperationType.UPDATE_PRICE_MINIMIZE_CPC_MAX : "关键词超出设置的最高点击单价，降低出价"
    , OperationType.UPDATE_PRICE_TO_INCREASE_COST : "为了加大计划投入，关键词进行价格调整"
    , OperationType.UPDATE_PRICE_TO_DECREASE_COST : "为了减小计划投入，关键词进行价格调整"
    , OperationType.UPDATE_PRICE_TO_APPROVE_ROI : "为了提高计划效果，关键词价格进行调整"
    , OperationType.UPDATE_PRICE_DIRECTOR : "为了优化加力计划效果，关键词价格进行调整"
    , OperationType.UPDATE_PRICE_HISTORY_NORMAL: "关键词价格进行调整(历史记录未区分类型)"
    , OperationType.UPDATE_PRICE_COST_LESS_THAN_LIMIT_INCRE_PRICE: "计划花费未达到最低花费设置，关键词加大投入"
    , OperationType.UPDATE_PRICE_CUSTOM: "在一定出价范围内，关键词价格进行调整"
    
    , OperationType.KEEP_NORMAL : "关键词表现正常，保持出价稳定，继续观察"
    
    , OperationType.IGNORE_KEYWORD_NOT_EXIST: "关键词不存在"
    , OperationType.IGNORE_KEYWORD_NOT_HANDLE : "关键词未托管，无需处理"
    , OperationType.IGNORE_NOT_MANAGE_BY_SOFT : "关键词价格超出设置价格，无需处理"
    , OperationType.IGNORE_CREATE_TIME_SHORT : "关键词创建时间太短，无需处理"
    , OperationType.IGNORE_MODIFIED_TIME_SHORT : "关键词修改时间太短，无需处理"
    , OperationType.IGNORE_KEYWORD_REPORT_NONE : "关键词报表未能获取，无需处理"
    , OperationType.IGNORE_CAMPAIGN_REPORT_NONE : "关键词所在计划报表未能获取，无需处理"
    , OperationType.IGNORE_CAMPAIGN_STOPPED: "关键词所在计划展现过低，无需处理"
    
    , OperationType.ADD_NORMAL: "新增关键词"
    , OperationType.ADD_KEYWORD_NORMAL: "新增关键词"
    , OperationType.ADD_KEYWORD_INITIAL: "新增关键词"
    , OperationType.ADD_KEYWORD_DIRECTOR: "新增关键词"
    , OperationType.ADD_KEYWORD_HISTORY_NORMAL: "新增关键词(历史记录未区分类型)"
    
    , OperationType.ADD_ADGROUP_NORMAL: "新增推广组"
    , OperationType.DELETE_ADGROUP_NORMAL: "用户删除推广组"
    , OperationType.DELETE_ADGROUP_INITIAL: "计划初始化，删除推广组"
    , OperationType.DELETE_ADGROUP_HISTORY_NORMAL: "删除推广组(历史记录未区分类型)"
}

class LoginFailType(object):
    UN_BUY = 1
    USER_NOT_EXIST = 2
    MERCHANT_TEST = 3
    DRAWBACK = 4
    SUBWAY_TOKEN_ERROR = 5
    NO_ITEM_CODE = 6
    NEED_MANAGER = 7
    ACCESS_TOKEN_ERROR = 8
    HTTP_ERROR = 9


LOGFAILTYPE_COMMENT = {
        LoginFailType.UN_BUY:'授权失败，当前用户未购买该软件，请切换淘宝帐号并重新登录，<a href="http://login.taobao.com/member/logout.jhtml?spm=1.1000386.5982201.5.qQ0uFL&f=top&out=true&redirectURL=http%3A%2F%2Fwww.taobao.com%2F">退出当前淘宝帐号</a>'
        ,LoginFailType.USER_NOT_EXIST:'用户不存在'
        ,LoginFailType.MERCHANT_TEST:'商家测试帐号无法登录'
        ,LoginFailType.DRAWBACK:'对不起, 该账户已经后台退款，不能继续使用软件'
        ,LoginFailType.SUBWAY_TOKEN_ERROR:'亲，无法查询到您的直通车帐号信息，请核对您的直通车帐号名和淘宝帐号名是否一致'
        ,LoginFailType.NO_ITEM_CODE:'系统暂时查不到您的订购记录，请尝试重新登录'
        ,LoginFailType.NEED_MANAGER:'进入后台失败，请先登录管理员账户'
        ,LoginFailType.ACCESS_TOKEN_ERROR:'授权失败，淘宝的access_token解析错误，请尝试重新登录'
        ,LoginFailType.HTTP_ERROR:'授权失败，与淘宝通信出错，请尝试重新登录'
        
}
