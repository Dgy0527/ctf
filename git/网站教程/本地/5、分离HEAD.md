# HEAD :当前所在位置的指示器

# `git switch --detach C1` :让git当前工作区(HEAD指针)切换到C1的特定提交(Commit)上
## --detach :分离
## C1 :其中的一个提交

```
如果想看 HEAD 指向，可以通过 cat .git/HEAD 查看， 如果 HEAD 指向的是一个符号引用（即分支名而非提交的哈希值），还可以用 git symbolic-ref HEAD 查看它的指向。但是该程序不支持这两个命令

HEAD -> main -> C1
HEAD -> C1
```
