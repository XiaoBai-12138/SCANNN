import re
import time
import json
import argparse
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

api_url = "http://52.141.4.3:5000"
token_url = "http://52.141.4.3:8000"


def Port_Scan(host, port):
    try:
        time.sleep(0.5)
        print("正在通过API进行端口扫描，请耐心等待")
        print(host)
        http = requests.get(url=api_url + "/port_scan?host=" + host + "&port=" + port).text
        print(http)
        ID = re.findall('(?<=ID：).*$', http)
    except:
        print("无法连接API")
        exit()
    if "/" in host:
        s_t = 7
    elif "," in host:
        s_t = 7
    else:
        s_t = 0.3
    scale = 0
    while True:
        scale += 1
        a = '*' * scale
        b = '.' * (50 - scale)
        c = (scale / 50) * 100
        if scale > 50:
            print('\r' + "目标延迟较大或目标过多，请耐心等待")
        print('\r' + "{:^3.0f}%[{}->{}]".format(c, a, b), end='', )
        try:
            s_json = requests.get(url=token_url + "/" + ID[0] + ".json")
            code = s_json.status_code
            if code == 200:
                print("\n" + "100%["
                             "**************************************************->]" + "\n")
                data = s_json.text.split("\n")
                jsonData = []
                for i in data:
                    if "}," in i:
                        JsonList = json.loads(i.split("},")[0] + "}")
                        jsonData.append(JsonList)
                ip = []
                ports = []
                for i in jsonData:
                    for k, v in i.items():
                        if k == "ip":
                            ip.append(v)
                        elif k == "ports":
                            port = v[0]["port"]
                            ports.append(port)
                # print(ip)
                # print(ports)
                newdata = []
                for i in range(len(ip)):
                    newdata.append(ip[i] + ":" + str(ports[i]))
                return newdata
                break
            time.sleep(s_t)
        except:
            return []


def Shiro(host):
    try:
        http = requests.get(url=host, timeout=3, verify=False).headers
        if "rememberMe=deleteMe" in str(http):
            return "[+]" + host + " " * (30 - len(host)) + "存在Shiro框架"
        else:
            return "[-]" + host + " " * (30 - len(host)) + "莫得Shiro框架"
    except:
        return "[-]" + host + " " * (30 - len(host)) + "非WEB应用程序"


def Body(host, text):
    try:
        http = requests.get(url=host, timeout=3, verify=False).text
        if text in str(http):
            return "[+]" + host + " " * (30 - len(host)) + "存在" + text + "特征"
        else:
            return "[-]" + host + " " * (30 - len(host)) + "莫得" + text + "特征"
    except:
        return "[!]" + host + " " * (30 - len(host)) + "拒绝访问"


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='XiaoBai NiuBi')
    parser.add_argument('-i', required=True, help="IP地址：1.1.1.1 OR 1.1.1.1,2.2.2.2 OR 1.1.1.1/24")
    parser.add_argument('--port', default='1-65535', help="端口选项，默认1-65535")
    parser.add_argument('--head', required=False, default='', help="识别header中特征，可选：Shiro")
    parser.add_argument('--body', required=False, default='', help="检测页面中指定特征，如：登录")
    parser.add_argument('--file', required=False, default='', help="将扫描出的开放端口保存在指定文件中")
    args = parser.parse_args()
    host = args.i
    port = args.port
    head = args.head
    body = args.body
    file = args.file
    L = Port_Scan(host, port)
    for i in L:
        if file:
            file_handle = open(file, mode='a')
            file_handle.write(i + '\n')
        print("[*]" + i)
    print("[*] 本次扫描发现" + str(len(L)) + "个有效HOST")
    if head == 'Shiro':
        if not L:
            print("未发现有效HOST")
            print(L)
        else:
            print("正在进行Shiro指纹识别")
            for i in L:
                print(Shiro("http://" + i))
    if body:
        if not L:
            print("未发现有效HOST")
            print(L)
        else:
            print("正在进行特征识别")
            for i in L:
                print(Body("http://" + i, body))
