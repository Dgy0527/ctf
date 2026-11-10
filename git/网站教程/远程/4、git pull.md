# `git pull` :从远程仓库拉取最新的代码并直接合并到当前所在的分支上
## git pull=git fetch + git merge

# `git pull origin main` :指定远程仓库和分支

# `git pull --rebase` :让提交历史干净漂亮

```
Git Pull
既然我们已经知道了如何用 git fetch 获取远程的数据, 现在我们学习如何将这些变化更新到我们的工作当中。

其实有很多方法的 —— 当远程分支中有新的提交时，你可以像合并本地分支那样来合并远程分支。也就是说就是你可以执行以下命令:

git cherry-pick o/main
git rebase o/main
git merge o/main
等等
实际上，由于先抓取更新再合并到本地分支这个流程很常用，因此 Git 提供了一个专门的命令来完成这两个操作。它就是我们要讲的 git pull。

注意： 在 Git 2.34 或更高版本中，如果本地和远程分支已经分叉，并且没有配置 pull 策略，单纯的 git pull 会停止并要求你选择如何整合。使用 git pull --no-rebase 进行合并，或使用 git pull --rebase 进行变基。在本模拟器中，git pull 默认使用合并行为
```