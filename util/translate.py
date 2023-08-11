import requests
import json
import hashlib
import time
import random

def translate_baidu(text, src_lang='zh', target_lang='en'):
    api = "https://fanyi-api.baidu.com/api/trans/vip/translate?q={}&from={}&to={}&appid={}&salt={}&sign={}"
    app_id = "20221020001403182"
    app_secret = "OIkZOEMkNImju9Xta1h0"
    lts = str(round(time.time() * 1000))
    salt = lts + str(random.randint(1, 10))
    sign = hashlib.md5((app_id + text + salt + app_secret).encode('utf-8')).hexdigest()
    req = api.format(text,src_lang,target_lang,app_id,salt,sign)
    resp = requests.get(req)
    if resp.status_code != 200:
        print("status code not 200")
        return ""
    # print(resp.content)
    resp_data = json.loads(resp.content)
    if "error_code" in resp_data.keys():
        print("get error: ", resp_data["error_msg"], resp_data)
        return ""
    else:
        return resp_data["trans_result"][0]["dst"]