# 要先在包含了`docker-compose.yml`的文件/目录下

# `docker compose -d` :一键启动;会自动下载镜像、创建网络并启动所有容器
## -d :后台运行
## `docker compose down` :一键停止并删除所有相关的容器和网络(但保留镜像)
## `docker compose ps` :查看当前编排中所有容器的运行状态
## `docker compose logs -f` :实时查看所有容器的日志
## `docker compose restart` :重启所有容器