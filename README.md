# Scannn

- 本工具是一款批量指纹/特征识别工具【联动masscan】

- 提供批量主机端口扫描并加入了WEB特征识别。

- 特点：轻量、快捷、高速、全面。

- 程序采用API制：服务端与客户端分离式逻辑。服务端负责接收客户端任务后使用masscan进行端口扫描，客户端从回调地址接受返回数据进行特征验证

## Build

#### 	Debian/Ubuntu：

​			apt install masscan python3 libpcap-dev python3-pip

#### 	Centos：

​			yum masscan python3 libpcap-dev python3-pip

#### 	PIP：

​			pip3 install requests

## API

​		接收任务API：程序目录执行：python3 run.py

​		回调API：程序目录执行：mkdir PORT_SCAN_JSON && python3 -m http.server 8000

​		设置API后去SCANNN.py修改API地址

​		PS：为防止连接断开导致API终止推荐使用screen软件创建新屏幕执行

## 示例

#### 查看Shiro

![微信图片_20210705001656](F:\微信图片_20210705001656.png)

#### 查看Body

![微信图片_20210705004546](F:\微信图片_20210705004546.png)

