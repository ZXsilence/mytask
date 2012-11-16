#encoding=utf8
import os, sys

#currDir = os.path.normpath(os.path.dirname(__file__))
#PROJECT_ROOT = os.path.normpath(os.path.join(currDir,os.path.pardir))
#
#APISDK = os.path.normpath(os.path.join(PROJECT_ROOT,'../../TaobaoOpenPythonSDK'))
#
##def getEnvReady():
##    sys.path.insert(0,PROJECT_ROOT)
##    sys.path.append(APISDK)
#
#trigger_envReady = getEnvReady()


#taobao open platform info
SERVER_URL = "http://gw.api.taobao.com/router/rest"

from  TaobaoSdk import  TaobaoClient
taobao_client = None
def set_taobao_client(app_key, app_secret):
    global taobao_client
    taobao_client = TaobaoClient(SERVER_URL, app_key, app_secret)




