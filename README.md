# 项目开发

## 开发目录
```
- manage.py
- v1
   |
   |--urls.py // 注册path和对应的handler
   |--handler.py // 存放handler的处理函数
   |--models.py // 存放sql表定义
   |--dal/ // 操作sql表
- util
   |
   |--token_secret.json // 存放token
   |--token_store.py // 加载token
```

### 开发简介
handler中解析request和返回json response：
```py
from django.http import JsonResponse

def get_user_session(request):
   # 解析request
    wx_code = request.POST.get("code")
    session_key = request.POST.get("session_key")
    # response
    resp = {
        "data": session_key,
    }
    return JsonResponse(resp)
```

## 本地调试

1. 安装依赖

- 安装python3、pip
- `pip install -r requirements.txt`

2. 开始调试

在包含`manage.py`的目录下，打开命令行输入`python3 manage.py runserver`，然后访问输出的网址+对应的path即可访问域名，或者用postman测试请求

## Ubuntu服务器安装

1. 依赖包
```sh
sudo apt-get update
sudo apt-get install python3-pip
sudo apt-get install python3-venv
sudo apt-get install apache2
sudo apt-get install libapache2-mod-wsgi-py3
```

2. 将项目文件放到`/var/www`文件夹下，然后进入项目目录运行`pip3 install -r requirements.txt`

3. apache权限设置
```sh
cd /var/www
sudo cp rpbg-server/tti.conf /etc/apache2/sites-available/tti.conf
sudo chgrp -R www-data rpbg-server
sudo chmod -R 644 rpbg-server
sudo find rpbg-server -type d | xargs chmod 755
sudo chmod g+w rpbg-server
sudo chmod g+w rpbg-server/db.sqlite3
```

4. 激活网站
```sh
sudo service apache2 reload 
sudo a2dissite 000-default && sudo a2ensite tti
sudo service apache2 restart
```

5. 之后可以通过http协议，输入服务器IP地址进行访问

## 已有path

- `/`: hello world页面
- `/api/test`: 测试json返回