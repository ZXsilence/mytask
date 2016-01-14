namespace java com.maimiaotech.thrift

service HandlerService {
        string execute(1:string nick, 2:string params)
        string getShopInfo(1:string nick)
}