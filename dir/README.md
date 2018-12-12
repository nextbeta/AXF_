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

## Nginx
Nginx高性能的HTTP和反向代理服务器! Nginx使用资源少，支持更多并发，