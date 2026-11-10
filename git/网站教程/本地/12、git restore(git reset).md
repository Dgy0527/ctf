# `git restore` :撤销修改
## `git reset`、`git checkout`的升级

# `git restore --staged 文件` :取消暂存文件

# `git restore 文件` :彻底丢弃文件修改

```
每个人偶尔都会把工作区弄乱一点：可能暂存了不该暂存的文件，也可能开始了一项后来想要丢弃的实验。git restore 是专门为工作区和暂存区设计的现代撤销工具。

它有两种用法：

git restore --staged <file>：取消暂存文件（将文件移出暂存区，但保留你的修改）
git restore <file>：彻底丢弃文件修改（请小心，这会删除这些修改！）
(它们取代了旧式的 git reset HEAD <file> 和 git checkout -- <file> 用法。作用相同，但名称清晰得多。)
```