import os
import uuid
from flask import Flask
from flask import request
from optparse import OptionParser

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello"

@app.route("/port_scan",methods=["POST","GET"])
def port_scan():
    try:
        ID = str(uuid.uuid4())
        rate = "10000"
        data=request.args
        if ("&" in str(data.get('host'))) or (";" in str(data.get('host'))) or ("`" in str(data.get('host'))) or ("|" in str(data.get('host'))) or ("\\" in str(data.get('host'))) or ("\"" in str(data.get('host'))):
            return "非法操作"
            exit()
        if ("&" in str(data.get('port'))) or (";" in str(data.get('port'))) or ("`" in str(data.get('port'))) or ("|" in str(data.get('port'))) or ("\\" in str(data.get('port'))) or ("\"" in str(data.get('port'))):
            return "非法操作"
            exit()

        if "/" in data.get('host'):
                rate = "50000"
        elif "," in data.get('host'):
            if data.get('host').count(",") < 10:
                rate = "50000"
            else:
                rate = "10000"
        port_scan_shell = "masscan " + data.get('host') + " -p " + data.get('port') + " --rate " + rate + " -oJ " + ID + ".json" + " && mv -f " + ID + ".json PORT_SCAN_JSON" + " > " + ID + ".file 2>&1 &"
        os.popen(port_scan_shell)
        X = "send" + "  目标：" + data.get('host')+ "  端口：" +data.get('port') + "  ID：" + ID
        return X
    except:
        return "异常访问"

if __name__ == '__main__':
    parser = OptionParser('./app.py [-p <Port>]')
    parser.add_option('-p','--port',type='int',help='port')
    (options,args)=parser.parse_args()
    app.run(host="0.0.0.0",port=options.port,debug=True)
