- [](#)
- [uwsig](#uwsig)
- [nginx](#nginx)



# Update
```bash
scp -r ../simple-flask ubuntu@1.116.121.100:~/project/
```
```bash
sudo apt install -y uwsgi nginx
sudo apt install uwsgi-plugin-python3
```


# uwsig

配置文件
```ini
[uwsgi]
uid             = ubuntu
gid             = ubuntu
socket          = 127.0.0.1:2021 # uWSGI 的监听端口 启动程序时所使用的地址和端口，通常在本地运行flask项目，
chdir           = /home/ubuntu/project/simple-flask # 指向网站目录
wsgi-file       = /home/ubuntu/project/simple-flask/server.py# python 启动程序文件
callable        = app# python 程序内用以启动的 application 变量名
processes       = 1 # 处理器数
threads         = 2 # 线程数
stats           = 127.0.0.1:2022 #状态检测地址
logto           = /home/ubuntu/project/simple-flask/log/flask.log #项目flask日志文件
vacuum          = true  # 退出、重启时清理文件
master          = true  # 主进程

stats           = /home/ubuntu/project/simple-flask/log/uwsgi.status
pidfile         = /home/ubuntu/project/simple-flask/log/uwsgi.pid

daemonize       = /home/ubuntu/project/simple-flask/log/uwsgi.log
plugins         = python3
```

uwsgi 启动
```bash
# 启动
uwsgi --ini uwsgi.ini

# 重启
uwsgi --reload uwsgi.pid

# 停止
uwsgi --stop uwsgi.pid

# 重启uWSGI服务器
sudo service uwsgi restart

# 查看所有uWSGI进程
ps aux | grep uwsgi

# 查看是否启动
netstat -anp | grep 2021

# 停止所有uWSGI进程
sudo pkill -f uwsgi -9
```

教程：
- [uWSGI的安装及配置详解](https://pythondjango.cn/python/tools/6-uwsgi-configuration/)



# nginx
> 全局配置文件 `/etc/nginx/nginx.conf`

修改配置文件 `/etc/nginx/sites-enabled/default`
```bash
sudo vim /etc/nginx/sites-enabled/default
```

```
server {
    listen 80;
    server_name 1.116.121.100;  # 监听ip 换成服务器公网IP
    charset utf-8;

    access_log /home/ubuntu/project/simple-flask/log/access.log;
    error_log /home/ubuntu/project/simple-flask/log/error.log;

    location / {  
        include /etc/nginx/uwsgi_params;        # 导入uwsgi配置     
        uwsgi_pass 127.0.0.1:2021;              # 转发端口，需要和uwsgi配置当中的监听端口一致
        uwsgi_param UWSGI_PYTHON python3;       # Python解释器所在的路径，如果有虚拟环境可将路径设置为虚拟环境
        uwsgi_param UWSGI_CHDIR /home/ubuntu/project/simple-flask;  # 项目根目录
        uwsgi_param UWSGI_SCRIPT server:app;    # 项目的主程序
        }

    location /media  {
        alias /home/ubuntu/project/simple-flask/media;  
        }

    location /static  {
        alias /home/ubuntu/project/simple-flask/static;  
        }
}
```


nginx 启动/停止
```bash
# 启动
sudo nginx
sudo nginx -c /etc/nginx/nginx.conf
sudo systemctl status nginx.service

# 停止
sudo service nginx stop
sudo nginx -s stop
sudo nginx -s quit

# 检查配置
sudo nginx -t

# 重启加载配置
sudo nginx -s reload

# 查看nginx接入日志 
tail -f /var/log/nginx/access.log

# 查看nginx错误日志 
tail -f /var/log/nginx/error.log


sudo service nginx restart
ps -ef|grep nginx
sudo pkill -9 nginx
```