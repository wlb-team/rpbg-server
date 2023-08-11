from v1.models import User
from v1.models import default_gen_times
import hashlib
import time, datetime

def get_user_by_session(session_key):
    user = User.objects.get(session_key=session_key)
    return user

def get_user_by_openid(wx_openid):
    # get or create
    try:
        user = User.objects.get(wx_openid=wx_openid)
    except User.DoesNotExist:
        session_key = hashlib.md5(wx_openid.encode('utf-8')).hexdigest()
        user = User(wx_openid=wx_openid, gen_times=default_gen_times, credits_updated_at = datetime.date.today(), session_key = session_key, extra = "")
        user.save()
    else:
        pass
    return user

def update_gen_time(wx_openid, new_gen_time):
    user = User.objects.get(wx_openid=wx_openid)
    user.gen_times = new_gen_time
    user.gen_times_updated_at_v2 = datetime.date.today()
    user.save()
    return
    #UserV4.objects.filter(wx_openid=wx_openid).update(gen_times=new_gen_time, gen_times_updated_at_v2 = datetime.date.today())
