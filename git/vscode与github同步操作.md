# 1、先 git fetch origin 获取远程最新状态 (不会覆盖本地的修改)
## 执行后没有任何输出说明本地与远程完全同步

# 2、再在终端输入 git status 查看状态
## 如果提示 Your branch is up to date with 'origin/main'.（你的分支与远程 main 一致），那就说明同步成功，没有新内容

# 3、最后输入 git pull origin main (或 git pull)
## 执行完 git pull 后，你的代码就和另一台电脑上的完全一致了