#!/usr/bin/env python3

import sys
from os.path import abspath
from os.path import dirname

# 设置当前目录为工作目录
# 这一行是给 Apache 用的
# sys.path.insert(0, abspath(dirname(__file__)))

# 引入 server.py
import server

# 必须有一个叫做 application 的变量
# gunicorn 就要这个变量
# 这个变量的值必须是 Flask 实例
# 这是规定的套路(协议)
application = server.app

"""
这是把代码部署到 gunicorn 后面的套路
gunicorn wsgi_web --bind 0.0.0.0:80

"""
"""
supervisor 套路

➜  ~ cat /etc/supervisor/conf.d/xx.conf

[program:web13]
command=/usr/local/bin/gunicorn wsgi --bind 0.0.0.0:80
directory=/root/web13
autostart=true
"""
