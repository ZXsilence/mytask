#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: tanglingling
@contact: tanglingling@maimiaotech.com
@date: 2017-07-27 15:52
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""
'''
功能：
1，和远端主分支更新
2，输入仓库名，和对应的分支名，将该仓库下的分支合并到本地分支
3，自动重启apache（需要修改sudo用户的密码）
用户：测试机预发布一套流程建立
'''
import commands,os,sys,time,signal

OSC = "git pull git@git.oschina.net:mmtech/"
JD = ['JdWeb','JdBackend','JDAlgorithm','JdApi']
ERROR = ['error', 'Connection refused', 'Please tell me who you are', 'Connection timed out', 'Access denied', 'Connection closed', 'hung up unexpectedly','fatal: Not a git repository',\
         'Pull is not possible because you have unmerged files']
OK = ['Already up-to-date.']
NO_INSTALL = ['TaobaoOpenPythonSDK','AutoTests']

PDIR = os.path.abspath(os.path.dirname(os.curdir))

class TimeOutException(Exception):
    def __init__(self,msg):
        self.msg = msg
    def __str__(self):
        return "TimeOutException:%s" % self.msg

def handler(signum,frame):
    raise TimeOutException("函数执行超时，请确认该分支是否存在，或网络是否畅通！")

def merge(wares,brs):
    ###将测试分支拉到本地
    ###将本地分支合并2016，保持最新
    print "\033[1;32;40m开始合并代码 ...\033[0m"
    time.sleep(1)
    totalError = 0
    if len(wares) != len(brs):
        print "\033[1;31;40m仓库名和分支名个数不一，退出！"+"\033[0m"
        exit(0)

    results = {}
    for i in range (len(wares)):
        repo = wares[i]
        br = brs[i]

        os.chdir(PDIR)
        cur = PDIR+"/"+repo
        if not os.path.exists(cur):
            print "\033[1;31;40m"+cur+" 目录不存在!忽略!"+"\033[0m"
            continue
        else:
            os.chdir(cur)
        cur1 = os.path.abspath(os.path.dirname(os.curdir))
        print "\n"+cur1

        main_repo = 'jd' if repo in JD else '2016'

        pull1 = "%s%s %s 2>&1" % (OSC,repo,br)
        pull2 = "%s%s %s 2>&1" % (OSC,repo,main_repo)

        print "pull \033[1;36;40m" +repo+" "+br+" \033[0m"+" to local..."
        ###假设输入的分支名不存在，程序会卡死不动，限定拉取远端分支超时时间为15s
        signal.signal(signal.SIGALRM,handler)
        signal.alarm(15)
        status1,output1 = commands.getstatusoutput(pull1)
        signal.alarm(0)
        errorCnt1,warning_Cnt1 = error(output1)

        print "pull \033[1;36;40m" +repo+" "+main_repo+" \033[0m "+"to local..."
        status2,output2 = commands.getstatusoutput(pull2)
        errorCnt2,warning_Cnt2 = error(output2)

        results[repo] ={}
        if errorCnt1 or errorCnt2:
            results[repo].update({"Error":True})
        if warning_Cnt1 or warning_Cnt2:
            results[repo].update({"Warning":True})

        totalError += errorCnt2 + errorCnt1
    print "\n(ok成功 failed失败 warning代码合并)\n"
    for  k in wares:
        res = results[k]
        if res.get("Error",None):
            print k+"\t"+"\033[1;31;40mError\033[0m"
        elif res.get("Warning",None):
            print k+"\t"+"\033[1;33;40mWarning\033[0m"
        else:
            print k+"\t"+"\033[1;36;40mOK\033[0m"
    return totalError

def error(output):
    error_Cnt = 0 
    warning_Cnt = 0
    for k in ERROR:
        if k in output:
            error_Cnt += 1
        elif OK[0] not in output and "Auto" in output:
            warning_Cnt += 1
    output = output.split("\n")
    if error_Cnt:
        print "\033[1;31;40m"
    for k in output:print k
    if error_Cnt:
        print "\033[0m"
    return error_Cnt,warning_Cnt

def install(wares):
    print "\n\033[1;32;40m开始建立软链 ...\033[0m"
    time.sleep(1)
    for i in range (len(wares)):
        repo = wares[i]
        if repo in NO_INSTALL:
            continue
        os.chdir(PDIR)
        cur = PDIR+"/"+repo
        if not os.path.exists(cur):
            print "\033[1;31;40m"+cur+" 目录不存在!忽略!\033[0m" 
            continue
        else:
            os.chdir(cur)
        cur1 = os.path.abspath(os.path.dirname(os.curdir))
        print  "\033[1;36;40m"+cur1+"\033[0m"
        print "sh install.sh clean ..."
        status1,output1 = commands.getstatusoutput("sh install.sh clean")
        if repo != "Webpage":
            print "sh install.sh test ..."
            status2,output2 = commands.getstatusoutput("sh install.sh test")
        else:
            print "sh install.sh test syb..."
            status2,output2 = commands.getstatusoutput("sh install.sh test syb")

    return 0

def restartApache():
    print "\033[1;32;40m开始启动apache ...\033[0m"
    time.sleep(1)
    status,output = commands.getstatusoutput("echo food_choppy=flick|sudo -S /etc/init.d/apache2 restart")
    for k in output.split("\n"):print k
    if "failed" in output:
        print "\033[1;31;40m启动apache失败，请查看apache日志！"+"\033[0m"
    elif "incorrect password attempts" in output:
        print "\033[1;31;40msudo密码错误，启动apache失败！"+"\033[0m"
    else:
        print "\033[1;36;40m启动apache成功！"+"\033[0m"

def mergeInstallOther(wares):
    print "\033[1;32;40m开始合并远端主分支 ...\033[0m"
    os.chdir(PDIR)
    dirs = os.listdir(PDIR)
    results={}
    pwares = []
    totalError = 0
    for d in dirs:
        os.chdir(PDIR)
        if not d.startswith(".") and d not in wares and os.path.isdir(os.path.join(PDIR,d)):
            cur = PDIR+"/"+d
            os.chdir(cur)
            pwares.append(d)
            main_repo = 'jd' if d in JD else '2016'
            pull1 = "%s%s %s 2>&1" % (OSC,d,main_repo)
            print "pull \033[1;36;40m" +d+" "+main_repo+" \033[0m"+" to local..."
            status1,output1 = commands.getstatusoutput(pull1)
            errorCnt1,warning_Cnt1 = error(output1)

            results[d] ={}
            if errorCnt1:
                results[d].update({"Error":True})
            if warning_Cnt1:
                results[d].update({"Warning":True})
            totalError += errorCnt1
    print "\n(ok成功 failed失败 warning代码合并)\n"
    for  k in pwares:
        res = results[k]
        if res.get("Error",None):
            print k+"\t"+"\033[1;31;40mError\033[0m"
        elif res.get("Warning",None):
            print k+"\t"+"\033[1;33;40mWarning\033[0m"
        else:
            print k+"\t"+"\033[1;36;40mOK\033[0m"

    if totalError:
        return totalError
    return install(pwares)

def useage():
    f = sys.argv[0]
    print  "\033[1;36;40mpython %s all\033[0m（所有仓库与线上主分支进行pull、install）" % f
    print  "\033[1;36;40mpython %s other\033[0m（输入线上仓库名、分支名进行pull、install）" % f
    print  "\033[1;36;40mpython %s other 1\033[0m（输入线上仓库名、分支名进行pull、install，重启apache）" % f
    print  "\033[1;36;40mpython %s apache\033[0m（仅启动apahce）" % f

if __name__ == "__main__":
    print "\033[0m"

    len_argv = len(sys.argv)

    if len_argv <= 1 or len_argv > 3 :
        useage()
    elif (len_argv == 2 or len_argv ==3 ) and sys.argv[1]=="other":
        ###交互输入仓库 和 测试分支 ，用语合并到preOnline 预上线分支
        valid_wares = ['Webpage','JdWeb',\
                    'backends','JdBackend',\
                    'comm_lib','TaobaoOpenPythonSDK','Stuff','JdApi',\
                    'Algorithm','JDAlgorithm','ZZAlgorithm' ]
        breakWare = False
        breakBrach = False

        print "\033[1;32;40m开始输入参数 ...\033[0m"
        while(not breakWare):
            warehouses = raw_input("输入仓库名，以空格分隔(删除请按Ctrl+Backspace),退出按q：")
            if warehouses.lower() == 'q':
                exit(0)
            wares = warehouses.split(" ")
            not_valid_name = []
            for ware in wares:
                if ware not in valid_wares:
                    not_valid_name.append(ware)
            if not_valid_name:
                print "以下仓库名不合法，请重试!"
                print "\033[1;31;40m"+">>> %s" % ','.join(not_valid_name) +"\033[0m"
                breakWare = False
                continue
            else:
                breakWare=True
                #sure = raw_input( "你输入的仓库名顺序为:\033[1;36;40m"+','.join(wares)+"\033[0m"+"\n确请按y，重新输入请按n，其他键退出: " )
                #if sure.lower() == 'y':
                #    breakWare=True
                #elif sure.lower() == 'n':
                #    continue
                #else:
                #    exit(0)

        while(not breakBrach):
            ware2br_str = ""
            branches = raw_input("按输入的仓库名顺序输入测试分支(删除请按Ctrl+Backspace)：")
            brs = branches.split(" ")
            if len(wares) != len(brs):
                print "输入的仓库名和分支名个数不一，请重试！"
                breakBrach = False
                continue
            for i in range(len(wares)):
                ware2br_str += "\n%s:%s"%(wares[i],brs[i])
            breakBrach = True
            print "你输入的仓库名-分支名的对应关系是：\033[1;36;40m" + ware2br_str + "\033[0m"
            time.sleep(1)
            #sure = raw_input("确认你输入的仓库名-分支名的对应关系：\033[1;36;40m"+ware2br_str+"\033[0m"+"\n确认请输入y，重新输入请按n，其他键退出：")
            #if sure.lower()== 'y':
            #    breakBrach = True
            #elif sure.lower() == 'n':
            #    breakBrach = False
            #else:
            #    exit(0)

        if not wares or not brs:
            print "\033[1;31;40m输入仓库名or分支名有误，退出！"+"\033[0m"
            exit(0)
        
        ###调用func进行preOnline分支合并
        totalError1 = merge(wares,brs)
        totalError2 = install(wares)
        totalError3 = mergeInstallOther(wares)

        if len_argv ==3 and int(sys.argv[2])==1:
            if totalError1:
                print "\033[1;31;40m有仓库拉取代码失败，不能自动重启apache。请解决错误后重新执行！"+"\033[0m"
                exit(0)
            if totalError2:
                print "\033[1;31;40minstall 操作失败，不能自动重启apache。请解决错误后重新执行！"+"\033[0m"
                exit(0)
            if totalError3:
                print "\033[1;31;40m自动合并其他仓库失败，不能自动重启apache。请解决错误后重新执行！"+"\033[0m"
                exit(0)
            restartApache()
        print "\033[0m"
    elif len_argv ==2:
        if sys.argv[1] == "all":
            mergeInstallOther([])
        elif sys.argv[1] == "apache":
            restartApache()
    else:
        useage()
