from django.shortcuts import render
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import base64
import os
from io import BytesIO
import time
import json

from v1.dal import user_dal

# Create your views here.

def temp_home(request):
    return render(request, "temp_home.html")


# ***************** wx sd *****************
@csrf_exempt
def stable_with_session(request):
    prompt = request.POST.get("prompt")
    session_key = request.POST.get("session_key")
    if session_key:
        user_info = user_dal.get_user_by_session(session_key)
    else:
        return JsonResponse({"err": "not logged in"})
    if not user_info:
        return JsonResponse({"err": "not logged in"})
    user_info = renew_gen_times(user_info)
    if user_info.gen_times <= 0:
        return JsonResponse({"err": "run out of generate times"})
    # 控制长度
    if len(prompt) > PROMPT_ZH_MAX_LEN:
        prompt = prompt[:PROMPT_ZH_MAX_LEN]
    # tns check
    tnsRes = tns_check(user_info.wx_openid, prompt)
    if not tnsRes:
        print("tns check failed, prompt: ", str(prompt))
        return JsonResponse({"err": "tns check failed"})
    # translate
    prompt_en = translate_baidu(prompt)
    if len(prompt_en) <= 0:
        return JsonResponse({"err": "translate failed"})
    else:
        print("translate res: {}, user session: {}, gen time left before gen: {}".format(prompt_en, session_key, user_info.gen_times))
    # add material to prompt
    prompt_en += PROMPT_MATERIAL
    
    # without timeout
    contents = generate(prompt_en)
    img_base64 = base64.b64encode(contents)

    new_gen_times_left = user_info.gen_times - 1
    if new_gen_times_left < 0:
        new_gen_times_left = 0
    user_dal.update_gen_time(user_info.wx_openid, new_gen_times_left)

    return HttpResponse(img_base64, content_type="image/png")

@csrf_exempt
def get_user_session(request):
    wx_code = request.POST.get("code")
    session_key = request.POST.get("session_key")
    user_info = None
    if session_key:
        user_info = user_dal.get_user_by_session(session_key)
    if not user_info and wx_code:
        # wx code & upsert
        # openid = "test_XXX_2df2343r"
        openid = get_openid_by_code(wx_code)
        user_info = user_dal.get_user_by_openid(openid)
    if not user_info:
        resp = {
            "session_key": "",
            "left_gen_times": 0,
        }
    else:
        user_info = renew_gen_times(user_info)
        resp = {
            "session_key": user_info.session_key,
            "left_gen_times": user_info.gen_times,
        }
    return JsonResponse(resp)


# 判断是否到了第二天，需要重置剩余生成次数
def renew_gen_times(user_info):
    if not user_info:
        return user_info
    if not time_util.compare_date_eq_today(user_info.gen_times_updated_at_v2):
        print("renewing gen_times for user: ", user_info.session_key)
        user_info.gen_times = default_gen_times
        user_dal.update_gen_time(user_info.wx_openid, default_gen_times)
        return user_info
    return user_info

# **************** test ***************

def json_test(request):
    data = {
        "data": 1,
    }
    return JsonResponse(data)
