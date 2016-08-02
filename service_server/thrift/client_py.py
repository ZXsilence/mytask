#encoding=utf-8
if __name__ == "__main__":
    import sys,os
    currDir = os.path.normpath(os.path.dirname(__file__))
    API_GEN = os.path.normpath(os.path.join(currDir, './gen-py/'))
    sys.path.append(API_GEN)
from thrift.protocol import TBinaryProtocol  
from thrift.transport import TTransport
from thrift.transport import TSocket
from javaApi import HandlerService

class JavaApiClient(object):
    def __init__(self,host,port,timeout = 60000):
        self.host = host
        self.port = int(port)
        transport = TSocket.TSocket(self.host, self.port)
        transport.setTimeout(timeout)
        transport = TTransport.TBufferedTransport(transport)
        self.transport = transport
        protocol = TBinaryProtocol.TBinaryProtocol(transport)
        self.client = HandlerService.Client(protocol)
        transport.open()
        
    def query_rpts(self,nick,params):
        result = self.client.execute(nick,params)
        self.transport.close()
        return result
    
    def get_shop_info(self,nick):
        result = self.client.getShopInfo(nick)
        self.transport.close()
        return result
    
if __name__ == "__main__":
    import simplejson
    host = "192.168.0.126"
    host = "183.131.0.206"
    host = "10.117.3.35"
    port = 9999
    client = JavaApiClient(host,port)
    nick = "飞利浦鼎盛年华专卖店"
    nick = "凯络上海"
    client.get_shop_info("麦苗科技营销")
    #计划报表
    client = JavaApiClient(host,port)
    params = {"start_date":"2016-05-01","end_date":"2016-05-01","rpt_type":"campaign"}
    params= simplejson.dumps(params)
    res = client.query_rpts(nick,params)
    tt = simplejson.loads(res)
    print tt['data'][0]['gmtModify']
    print "rpt:",res
        
