![alt text](./img/Easy_Extract.png)

# 考点:变量覆盖漏洞

# 1、extract():一个将数组元素导入到当前符号表(即创建变量)的函数

# 主要作用:把数组的键名变成变量名、键值变成变量名

## 例:extract($ _GET)创建了一个变量$auth=1000,从而覆盖了之前定义的$auth=100