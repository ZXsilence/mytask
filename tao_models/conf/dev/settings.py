#encoding=utf8
import os, sys

currDir = os.path.normpath(os.path.dirname(__file__))
#
APISDK = os.path.normpath(os.path.join(currDir,'../../../TaobaoOpenPythonSDK'))
BACKENDS = os.path.normpath(os.path.join(currDir,'../../../backends/'))
#
sys.path.append(APISDK)
sys.path.append(BACKENDS)

#taobao open platform info
SERVER_URL = "http://223.5.20.253:8002/router/rest"
import inspect
from  TaobaoSdk import  TaobaoClient
taobao_client = None
def set_taobao_client(app_key, app_secret):
    global taobao_client
    taobao_client = TaobaoClient(SERVER_URL, app_key, app_secret)




