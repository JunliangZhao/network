### 本次大项目分为两个部分——networkip文件结构说明

### 第一部分是ping活跃ip 并且通过tracert 追踪活跃ip获得一个扇贝图，将图的信息保存在tracert.txt的文件下

追踪ip信息保存为  个人ip+追踪无掩码ip+ip段+tracert.txt

ping ip信息保存为 个人ip+追踪无掩码ip+ip段+online.txt

实现代码文件为  ipfind.py文件

### 第二部分是进行tracert.txt的文件阅读，之后构造出获取节点之间的追踪关系，构造出map图进行构造网络拓扑结构

采用neo4j数据库，读取追踪ip信息 进行主干节点提取 获取网络拓扑图

实现代码文件为 ReadAndMap.py文件

