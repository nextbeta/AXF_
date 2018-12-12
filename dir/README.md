# 部署上线
## 一、准备工作
```
阿里云服务器
备选: 域名
```

## 二、部署基本流程
```
- 服务器环境搭建(虚拟环境)
- 数据库
- 项目上传
- 项目依赖
- 项目数据迁移

- Nginx安装
- Ngian配置

- uWSGI安装
- uWSGI配置

- Nginx和uWSGI对接
```


## 三、服务器简述
```
LAMP、LNMP....
LAMP: L(Linux) + A(Apache)　+ M(MySql) + P(PHP)
LNMP: L(Linux) + N(Nginx)　+ M(MySql) + P(PHP)
```


## 四、连接服务器
```
SSH、putty、xShell、VNC...

$ ssh root@112.74.55.3
```
> 备注: 重置密码、安全组开启!!!


## 五、虚拟环境
```
# 第一步: 安装
$ pip install virtualenv
$ pip install virtualenvwrapper

# 第二步: 查看安装目录
$ type virtualenvwrapper.sh

# 第三步: 配置
$ vi ~/.bashrc
    export WORKON_HOME=~/.virtualenvs
    # 根据自己的安装路径配置
    source /usr/local/bin/virtualenvwrapper.sh

# 第四步: 创建目录
$ mkdir ~/.virtualenvs

# 第五步: 刷新环境
$ source ~/.bashrc

# 第六步: 创建虚拟环境
$ mkvirtualenv python3 -p /usr/bin/python3.5

# 第七步: 检查是否成功(是否python3.5版本)
$ python

# 备注: ubuntu中Python2的环境默认都是全的，但是Python3的集成不够完整，有部分包是欠缺的
$ apt update
$ apt install python3-dev
```

## 六、数据库
```
# 安装
$ apt install mysql-server

# 检查是否开机自启动
$ systemctl status mysql.service

# 开机自启动
systemctl enable mysql.service

# 关闭开机启动
systemctl disable mysql.service

# 开启服务
systemctl start mysql.service

# 关闭服务
systemctl stop mysql.service

# 重启服务
systemctl restart mysql.service
```
> 备注: 测试连接数据库!!!


## 七、项目上传
```
scp命令
github
pycharm自带 【比较推荐使用】
```

## 八、安装项目依赖
```
# 客户端中 生成 依赖文件
$ pip freeze > requirements.txt

# 服务端 指定文件安装依赖
$ pip install -r requirements.txt
```

## 九、数据迁移
```
# 客户端 备份数据
$ mysqldump -u root -p  python1810axf > python1810axf.sql

# 服务端 【必须要先创建对应的数据库】 恢复数据
mysql> create database python1810axf charset=utf8;
mysql> use python1810axf
mysql> source python1810axf.sql
```

## 十、启动Django项目
保证数据库中数据没问题、项目需要依赖都有!!!
```
# 启动项目
$ python manage.py runserver 0.0.0.0:8000

# 测试外网能后访问
112.74.55.3:8000/axf/
```
> Django自带的小型服务器，只能用于开发测试使用!


## 十一、安装Nginx
```
# 安装
## key验证
$ wget http://nginx.org/keys/nginx_signing.key
$ sudo apt-key add nginx_signing.key

## 添加到 /etc/apt/sources.list 文件中
deb http://nginx.org/packages/ubuntu/ xenial nginx
deb-src http://nginx.org/packages/ubuntu/ xenial nginx

## 更新源
$ apt update

## 安装
$ apt install nginx

# 设置开机自启动
$ systemctl enable nginx.service

# 重启nginx
$ systemctl restart nginx.service

# 查看状态
$ systemctl status nginx.service

# 浏览器中访问[保证Nginx安装没问题,在浏览器中访问时，可以看到`Welcome to nginx!`]
112.74.55.3
```

## 十二、Nginx配置(静态文件)
```
# Nginx配置文件(默认)
/etc/nginx/nginx.conf

# 拷贝一个出来，进行修改(自己的配置)
cp nginx.conf my_nginx.conf

# 在/var/www/目录中添加一个Text目录
mkdir /var/www/Text

# 在Text目录添加一个文件(有内容)
echo 'hello nginx' > /var/www/Text/hello.txt

# 配置my_nginx.conf
htttp {
    server {
        location /text {
            alias /var/www/Text;
        }
    }

    #include /etc/nginx/conf.d/*.conf;
}

# 指定配置文件启动
nginx -c my_nginx.conf

# 测试能否加载静态文件
http://112.74.55.3/text/hello.txt


#### 将AXF的静态目录配置上去
# 修改配置文件my_nginx.conf
htttp {
    server {
        location /text {
            alias /var/www/Text;
        }

        location /static {
            alias /var/www/AXF/static/;
        }
    }

    #include /etc/nginx/conf.d/*.conf;
}

# 重启Nginx
pkill -9 nginx
nginx -c my_nginx.conf

# 浏览器中访问
http://112.74.55.3/static/mine/img/axf.png


####### 其他命令
# 查看进程
ps -ef | grep nginx

# 杀死服务
pkill -9 nginx
```

## 十三、uWSGI
WSGI: PythonWeb服务器网关接口（Python Web Server Gateway Interface，缩写为WSGI)是Python应用程序或框架和Web服务器之间的一种接口，已经被广泛接受, 它已基本达成它的可移植性方面的目标。
WSGI 没有官方的实现, 因为WSGI更像一个协议。
uWSGI: 是web服务器，实现了WSGI协议(uwsgi协议、http协议...)，部署分布式集群网络应用开发的一套解决方案。
```
- 安装(虚拟环境中)
pip install uwsgi

- 项目中添加uwsgi.ini配置文件


- 配置uwsgi.ini文件(测试: 直接使用uwsgi，而不对接nginx)
    # uwsgi基本使用没问题，再对接上nginx，即打开socket，关闭http
    [uwsgi]
    # 使用nginx连接时 使用
    #socket=0.0.0.0:8000
    # 直接作为web服务器使用
    http=0.0.0.0:8010
    # 配置工程目录
    chdir=/var/www/axf/Python1807AXF
    # 配置项目的wsgi目录。相对于工程目录
    wsgi-file=Python1807AXF/wsgi.py

    #配置进程，线程信息
    processes=1
    threads=1
    enable-threads=True
    master=True
    pidfile=uwsgi.pid
    daemonize=uwsgi.log

- 使用
    # 启动
    $ uwsgi --ini uwsgi.ini
    # 停止
    $ uwsgi --stop uwsgi.ini

# 访问测试(确保uswgi能够启动项目)
    http://112.74.55.3:8010/axf/
```

## 十四、Nginx和uWSGI对接
```
# uWSGI配置
#http = 0.0.0.0:8010
socket=0.0.0.0:8000

# my_nginx.conf配置
server { #虚拟主机配置
        location / {
                # uwsgi配置
                include /etc/nginx/uwsgi_params;
                # 代理(转发)
                uwsgi_pass 127.0.0.1:8000;
        }

        location /text {
                alias /var/www/Text/;
        }

        location /static {
                alias /var/www/AXF/static/;
        }
    }


# uWSGI重新启动
pkill -9 uwsgi
uwsgi --ini uwsgi.ini

# nginx重新启动
pkill -9 nginx
nginx -c my_nginx.conf
```

## 十五、支付宝集成
```
# 准备工作
- 应用秘钥公钥生成 (https://docs.open.alipay.com/291/105971)
    通过支付宝的 生成工具生成的(公钥、私钥)
- 将应用公钥设置到支付宝
- 拷贝支付宝公钥
- 支付宝的APPid
    2016091800542542
- 支付宝网关
    https://openapi.alipaydev.com/gateway.do

# 安装加密模块
    pip install pycryptodome

# 支付宝初始化配置
    appid
    支付宝公钥
    应用私钥
    app_notify_url (通知服务器的)
    return_url (客户端 支付后的页面)

# 支付宝公钥、应用私钥 处理
    -----BEGIN PRIVATE KEY-----
    钥匙串
    -----END PRIVATE KEY-----
```


## Nginx
Nginx高性能的HTTP和反向代理服务器! Nginx使用资源少，支持更多并发，