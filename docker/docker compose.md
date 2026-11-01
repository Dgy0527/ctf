# 要先在包含了`docker-compose.yml`的文件/目录下

# `docker compose -d` :一键启动;会自动下载镜像、创建网络并启动所有容器;如果之前执行了`docker compose -d --build`这条命令想要再启动只要执行`docker compose -d`就行了
## -d(detach) :后台运行
## `docker compose down` :一键停止并删除所有相关的容器和网络(但保留镜像)
## `docker compose ps` :查看当前编排中所有容器的运行状态
## `docker compose logs -f` :实时查看所有容器的日志
## `docker compose restart` :重启所有容器
# `docker compose up -d --build 自己的服务(docker-compose.yml里应该有写)` :在后台把项目重新打包并一键启动
## -d(detach) :后台启动
## -build :强制重新构建镜像(打补丁)