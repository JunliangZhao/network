from os import link, pipe
import re
from py2neo import Graph,Node, Relationship
from ipfind import infoname,myip
mymap=[]
with open(infoname,'r') as f:
    data=f.read()
    data=data.replace('(',"")
    alltracrtinfo=data.split(")")
    endip=[]
    for i in alltracrtinfo:
        #过滤保存的tracert信息 构造出map图
        i=i.replace("[","")
        i=i.replace("]","")
        i=i.replace("'","")
        i=i.replace("\\n","")
        templist=i.split(",")
        if len(templist)<=1:
            continue
        sour=myip
        if sour=="":
            continue
        flag=0
        toendip=dict()
        for j in templist:
            templist1=j.split(" ")
            for l in templist1:
                #正则匹配ip信息
                if re.match(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", l):
                    if flag>=2:
                        if l!=sour:
                            mymap.append((sour,l))
                            sour=l
                    else:
                        flag+=1
                        endip.append(l)
    endip=set(endip)
    #采用neo4j  进行一个tracert追踪图构建
    for i in mymap:
        print(i)

    print("尝试连接neo4j 请稍等")
    graph = Graph('http://localhost:7474',username='neo4j',password='zjl123...')#连接neo4j图形数据库
    try:
        print('成功连接neo4j 并构造拓扑图')
        allnode=[]
        #把所有的节点都写入
        for i in mymap:
            allnode.append(i[0])
            allnode.append(i[1])
        #去粗重复节点
        allnode=set(allnode)
        #进行主干节点的搜索，删除叶子节点
        allnode1=[]
        for i in allnode:
            for j in mymap:
                if i in j[0]:
                    allnode1.append(i)
        #进行结束节点的寻找
        for i in endip:
            for j in mymap:
                if i in j[1]:
                    temp=i.split(".")
                    toendip[j[0]]=temp[0]+"."+temp[1]+"/16"
        print(toendip)
        allnode1=set(allnode1)
        print(allnode1)
        #进行主干节点的构造
        for i in allnode1:
            node1 = graph.nodes.match("pc").where("_.name='"+i+"'").first()
            if not node1:
                tempnode=Node("pc",name=i)
                graph.create(tempnode)
        #主干节点之间构造关系
        for i in mymap: #再map图中找寻主干节点 并且添加追踪关系
            if i[0] in allnode1 and i[1] in allnode1:
                node1 = graph.nodes.match("pc").where("_.name='"+i[0]+"'").first()
                node2 = graph.nodes.match("pc").where("_.name='"+i[1]+"'").first()
                mylink=Relationship(node1,'ping',node2)
                graph.create(mylink)
        
        #修改锚点节点 进行标记
        node1 = graph.nodes.match("pc").where("_.name='"+myip+"'").first()
        node1.remove_label("pc")
        node1.add_label("sourcepc")
        graph.push(node1)

        #进行叶子节点的统一标记 从主干节点到各个终端设备节点的一个ping
        for i in toendip:
            node1= graph.nodes.match("pc").where("_.name='"+i+"'").first()
            node2=Node("despc",name=toendip[i])
            mylink=Relationship(node1,'ping',node2)
            graph.create(mylink)
    except Exception:
        print('neo4j未连接 显示图序列') 


