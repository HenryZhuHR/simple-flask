```bash
scp -r ../simple-flask ubuntu@1.116.121.100:~/project/
scp -r ../simple-flask zhr@192.168.1.161:~/project/
```
```bash
sudo apt install -y uwsgi nginx
sudo apt install -y nginx 
```

# uwsig

配置文件
```ini

[uwsgi]

http            = 127.0.0.1:2021     # uWSGI 的监听端口 启动程序时所使用的地址和端口，通常在本地运行flask项目，
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

daemonize       = uwsgi.log
```



uwsgi启动/停止
```bash
# 启动
/usr/bin/uwsgi --ini uwsgi.ini&
# 重启
uwsgi --reload uwsgi.pid
# 停止
uwsgi --stop uwsgi.pid
```

# nginx

uwsgi --http-socket :2021 --wsgi-file server.py


`/etc/nginx/nginx.conf`

配置文件 `/etc/nginx/sites-enabled/default`
```bash
ls -l /etc/nginx/site-enabled
sudo vim /etc/nginx/sites-enabled/default
sudo vim /etc/nginx/sites-enabled/flask.config
```


```
server {
    listen 80;
    server_name 192.168.1.161;  # 监听ip 换成服务器公网IP

    access_log  /home/ubuntu/project/simple-flask/log/nginx/access.log;
    error_log  /home/ubuntu/project/simple-flask/log/nginx/error.log;

    location / {  
        include uwsgi_params;       # 导入uwsgi配置     
        uwsgi_pass 127.0.0.1:2021;  # 转发端口，需要和uwsgi配置当中的监听端口一致
        uwsgi_param UWSGI_PYTHON /usr/bin/python3;  # Python解释器所在的路径
        uwsgi_param UWSGI_CHDIR /home/ubuntu/project/simple-flask;  # 项目根目录
        uwsgi_param UWSGI_SCRIPT server:app;   # 项目的主程序
        }
}
```
```
server {
    listen 80;
    server_name 1.116.121.100;  # 监听ip 换成服务器公网IP

    access_log  /home/ubuntu/project/simple-flask/log/nginx/access.log;
    error_log  /home/ubuntu/project/simple-flask/log/nginx/error.log;

    location / {  
        include uwsgi_params;       # 导入uwsgi配置     
        uwsgi_pass 127.0.0.1:2021;  # 转发端口，需要和uwsgi配置当中的监听端口一致
        uwsgi_param UWSGI_PYTHON python3;  # Python解释器所在的路径，如果有虚拟环境可将路径设置为虚拟环境
        uwsgi_param UWSGI_CHDIR /home/ubuntu/project/simple-flask;  # 项目根目录
        uwsgi_param UWSGI_SCRIPT server:app;   # 项目的主程序
        }

    location /media  {
        alias /home/ubuntu/project/simple-flask/media;  
        }

    location /static  {
        alias /home/ubuntu/project/simple-flask/static;  
        }
}
```


启动 nginx
```bash
sudo /etc/init.d/nginx start
# or
sudo systemctl status nginx.service
ps -ef|grep nginx
```


nginx启动/停止
```bash
# 启动
sudo nginx
# 停止
sudo nginx -s stop
sudo nginx -s quit
# 重启加载配置
sudo nginx -s reload

sudo pkill -9 nginx
```


查看nginx接入日志 
```
tail -f /var/log/nginx/access.log
```

查看nginx错误日志 
```
tail -f /var/log/nginx/error.log
```


检查配置
```
nginx -t
```


