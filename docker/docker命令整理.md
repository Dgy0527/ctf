# 进入root权限的命令:
1、sudo su 2、sudo -i 3、sudo su i

# apt update:从你配置的国内源（清华、中科大等）下载最新的软件包列表,不会安装或升级任何软件

# apt install -y docker.io:安装docker

# docker version:查看docker的版本

# docker info:查看docker详细系统信息

# docker ps:查看当前正在运行的容器

# docker ps -a:查看所有容器,包括已停止的

# docker pull 镜像名 :拉取镜像

# docker images:查看本地已有镜像

# docker rmi 镜像名 :删除指定镜像

# docker start 镜像名 :启动容器

# systemctl stop docker.socket:停止容器
# systemctl stop docker.service

# docker run -dit(-d) --name=容器名 -p 8080:80 镜像名
## 1、-dit(-d) :后台运行,不占用终端
## 2、--name :给容器起个名字
## 3、-p 8080:80 :端口映射,把kali的8080端口映射到容器内部的80端口

# docker stop 容器名(或容器ID) :停止运行中的容器

# docker restart 容器名 :重启容器
# systemctl rstart docker

# docker kill 容器名 :强制停止容器

# docker rm 容器名 :删除已停止的容器
# docker rm -f 容器名

# docker exec -it 容器名 :进入正在进行的容器
## -it :开启交互式终端
## exec:在运行的容器里执行命令,退出容器后不会停止
## 退出容器:exit

# docker logs 容器名 :查看容器日志
# docker logs -f 容器名
## -f :可以实时滚动查看

# docker system df:查看磁盘占用

# docker system prung -a:一键清理所有停止的容器、未使用的网络和悬空镜像
