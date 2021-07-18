# -*- coding: utf-8 -*-
import platform
import os
import time
import threading
import socket
import re
allipOnline=[]
alltracertinfo=[]

#下列四个参数是用来控制追踪对象  本机ip   追踪段
myip="10.19.107.35"  #本机ip说明
addr="10.208"  #追踪ip的非掩码部分
tempstart=192   #追踪ip的ip段开始
tempend=193  #追踪ip的ip段结束


infoname=myip+" "+addr+" "+str(tempstart)+"-"+str(tempend)+"tracert.txt"  #追踪信息保存到txt中再进行处理
def get_os():#判断操作系统
    myos = platform.system()
    if myos == "Windows":
        return "n"
    else:
        return "c"
 
 
def ping_ip(ip_str):  #调用ping程序 获取活跃ip  主要通过cmd的ping实现
    mycmd = ["ping", "-{op}".format(op=get_os()),
           "1", ip_str]
    output = os.popen(" ".join(mycmd)).readlines()
    for line in output:
        if str(line).upper().find("TTL") >= 0:
            global allipOnline
            allipOnline.append(ip_str)
            break
 
 
def find_ip(ip_prefix):  #扫描所有ip段  采用多线程扫描
    '''''
    给出当前的ip地址段 ，然后扫描整个段所有地址
    '''
    threads = []
    for i in range(1, 256):
        ip = '%s.%s' % (ip_prefix, i)
        threads.append(threading.Thread(target=ping_ip, args={ip, }))
    for i in threads:
        i.start()
    for i in threads:
        i.join()
 
def tracert_allip(desip): #追踪所有ip  采用多线程追踪加速
    '''''
    给出当前的ip地址段 ，然后扫描整个段所有地址
    '''
    threads = []
    for i in desip:
        print(i+"追踪开始")
        threads.append(threading.Thread(target=tracert_ip, args={i, }))
    for i in threads:
        i.start()
    for i in threads:
        i.join()

def find_local_ip(): #找到本地ip
    addrs = socket.getaddrinfo(socket.gethostname(),None)
    allmyip=[]
    for item in addrs:
        if re.match(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", item[4][0]):
            allmyip.append(item[4][0])
    print(allmyip)
    return allmyip
 
 
def tracert_ip(ip):  #追踪某个ip 
    mycmd="tracert -d "+ip
    output = os.popen(mycmd).readlines()
    global alltracertinfo
    alltracertinfo.append((ip,output))


if __name__ == "__main__":
    print("开始扫描时间: %s" % time.ctime())
    #addr = find_local_ip()
    pre=""
    for j in range(tempstart,tempend):
        tempip_pre=addr+"."+str(j)
        print("扫描接口 ip地址为：%s 请等待" %tempip_pre)
        find_ip(tempip_pre)
        for l in allipOnline:
            if tempip_pre in l:
                print("ip：%s 在线" %l)
    with open(myip+" "+addr+" "+str(tempstart)+"-"+str(tempend)+"online.txt",'w') as f:
        f.write(str(allipOnline))
    #打印ip扫描信息
    for i in allipOnline:
        print("ip：%s 在线" %i)
    print("扫描结束时间 %s" % time.ctime())
    print('本次扫描共检测到本网络存在%s台设备' % len(allipOnline))
    print("开始追踪时间：%s" % time.ctime())
    tracert_allip(allipOnline)#调用追踪函数
    #打印追踪信息
    for i in alltracertinfo:
        print("**************************")
        print("追踪"+i[0])
        for j in i[1]:
            print(j,end="")
        print("**************************")
    print("追踪结束时间 %s" % time.ctime())
    with open(infoname,"w") as f:
        f.write(str(alltracertinfo))
 