from email.policy import default
from django.db import models
import datetime

default_gen_times = 5

# Create your models here.

# user
class User(models.Model):
    uid = models.AutoField(primary_key=True)
    wx_openid = models.CharField(max_length=256)
    session_key = models.CharField(max_length=256, db_index=True) # wx_openid的hash
    username = models.CharField(max_length=256, db_index=True)
    password_hash = models.CharField(max_length=256)
    credits = models.FloatField(default=5.0)
    credits_updated_at = models.DateField(default=datetime.date.today()) # 改为手动保存
    extra = models.TextField(null=True)


# api path run time
class ApiCount(models.Model):
    path = models.CharField(max_length=256)
    gen_times = models.IntegerField(default=10)
    extra = models.TextField(null=True)
