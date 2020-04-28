import time
import uuid
import password
import requests
import urllib3
import json
import d
urllib3.disable_warnings()

class mrequest():

    def __init__(self):
        self.proxies = {
                "http": d.Proxy,
                "https": d.Proxy,
            }

    def sendPost(self,nurl,payload,mothed,auth=""):
            timestr=str(int(time.time()))
            url="https://picaapi.picacomic.com/"+nurl
            nonce=str(uuid.uuid1()).replace("-","")
            sign=password.password(nurl,mothed,timestr,nonce)
            headers={
                            "api-key":"C69BAF41DA5ABD1FFEDC6D2FEA56B",
                            "accept":"application/vnd.picacomic.com.v1+json",
                            "app-channel":"1",
                            "time":timestr,
                            "nonce":nonce,
                            "signature":sign,
                            "app-version":d.Version,
                            "app-uuid":"cb69a7aa-b9a8-3320-8cf1-74347e9ee970",
                            "image-quality":d.Image_quality,
                            "app-platform":"android",
                            "app-build-version":d.Build_version,
                            "Content-Type": "application/json; charset=UTF-8",
                            "User-Agent":"okhttp/3.8.1",
                    }
            if auth!="":
                    headers.update({"authorization":auth})
            if mothed=="POST":
                    r = requests.post(url,headers=headers,data=json.dumps(payload),verify=False,proxies=self.proxies)
            elif mothed=="GET":
                    getnum=0
                    headers.pop("Content-Type")
                    while True:
                        r = requests.get(url,headers=headers,verify=False,proxies=self.proxies)
                        if r.status_code == 200:
                             print('GET请求成功')
                             break
                        else:
                             print('GET请求失败')
                             print('尝试重新连接中。。。')
                             time.sleep(3)
                             getnum+=1
                             if getnum>3 :return -1
            else:
                    getnum=0
                    headers.pop("Content-Type")
                    while True:
                        try:
                            r = requests.get(nurl,headers=headers,verify=False,stream=True)
                        except requests.exceptions.ConnectionError:
                            print("连接超时")
                            continue
                        if r.status_code == 200:
                             open(payload, 'wb').write(r.content)
                             break
                        else:
                             time.sleep(3)
                             print('图片加载错误')
                             getnum+=1
                             if getnum>8 :break
            return r