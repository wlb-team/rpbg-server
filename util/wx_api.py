import requests
import json
import time
from v1.util.token_store import wx_app_secret

# wx login 参考：https://juejin.cn/post/6922253355725111309
wx_app_id = "wxd59b81252c883ccc"


class accessToken:
    def __init__(self) -> None:
        self.token = ""
        self.expire = 0
    def getToken(self) -> str:
        # https://developers.weixin.qq.com/miniprogram/dev/OpenApiDoc/mp-access-token/getAccessToken.html
        if len(self.token) > 0 and self.expire > int(time.time()):
            return self.token
        api = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}".format(wx_app_id, wx_app_secret)
        resp = requests.get(api, timeout=5)
        if resp.status_code != 200:
            print("wx token status code not 200")
            return ""
        resp_json = json.loads(resp.content)
        if "access_token" not in resp_json.keys():
            print("wx token api error, resp: ", resp.content)
            return ""
        self.token = resp_json["access_token"]
        self.expire = int(time.time()) + int(resp_json["expires_in"])
        return self.token

wxToken = accessToken()

def get_openid_by_code(wx_code):
    api = "https://api.weixin.qq.com/sns/jscode2session?appid={}&secret={}&js_code={}&grant_type=authorization_code".format(wx_app_id, wx_app_secret, wx_code)
    resp = requests.get(api, timeout=5)
    if resp.status_code != 200:
        print("wx login api status code not 200")
        return ""
    resp_json = json.loads(resp.content)
    if "openid" not in resp_json.keys():
        print("wx login api error, resp: ", resp.content)
        return ""
    return resp_json["openid"]

def tns_check(openid, content: str):
    # https://developers.weixin.qq.com/miniprogram/dev/OpenApiDoc/sec-center/sec-check/msgSecCheck.html#%E8%BF%94%E5%9B%9E%E5%8F%82%E6%95%B0
    if len(openid) <= 0 or len(content) <= 0:
        return False
    token = wxToken.getToken()
    if len(token) <= 0:
        return False
    api = "https://api.weixin.qq.com/wxa/msg_sec_check?access_token={}".format(token)
    form_data = {
        "content": content,
        "version": 2,
        "scene": 2,
        "openid": openid
    }
    # 很坑的一点，如果requests传json=XXX，里面默认打包成json之后是Unicode编码，而如果想要body是utf-8，则需要用这种形式，手动json
    body = json.dumps(form_data, ensure_ascii=False).encode('utf-8')
    resp = requests.post(api, data=body)
    if resp.status_code != 200:
        print("wx tns api status code not 200")
        return ""
    resp_json = json.loads(resp.content)
    if "errcode" not in resp_json.keys():
        print("wx tns api error, resp: ", resp.content)
        return False
    if resp_json["errcode"] != 0 or "result" not in resp_json.keys():
        print("wx tns api errcode not 0, resp: ", resp.content)
        return False
    if resp_json["result"]["suggest"] == "pass" and resp_json["result"]["label"] == 100:
        return True
    return False
