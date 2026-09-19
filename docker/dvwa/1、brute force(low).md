# 暴力破解low

# 目录源码
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

1、` $id = $_REQUEST[ 'id' ]; `:没有对输入做任何过滤或转义

2、`$query  = "SELECT first_name, last_name FROM users WHERE user_id = '$id';";`:构造sql查询语句,但是$id被直接放入单引号,如果用户输入`' OR '1'='1`则变成
   `SELECT first_name, last_name FROM users WHERE user_id = '' OR '1'='1';`:返回用所有用户信息

3、`$GLOBALS["__MYSQLI_STON"]`:全局MySQLi数据库连接对象

4、`mysqli_query(连接,查询)`:发送查询到数据库,成功返回结果集对象,失败返回false

5、`{$id}`:直接输出用户输入的id,未经过HTML转义,可能存在XSS漏洞

6、`<pre>`:HTML标签,全称是preformatted text(预格式化文本);作用:保留原代码里的空白、空格、换行、缩进、原样展示文本

7、`mysqli_close($GLOBALS["___mysqli_ston"]);`:关闭之前打开的数据库连接



# 页面源码
```
<?php

if( isset( $_GET[ 'Login' ] ) ) {
    // Get username
    $user = $_GET[ 'username' ];

    // Get password
    $pass = $_GET[ 'password' ];
    $pass = md5( $pass );

    // Check the database
    $query  = "SELECT * FROM `users` WHERE user = '$user' AND password = '$pass';";
    $result = mysqli_query($GLOBALS["___mysqli_ston"],  $query ) or die( '<pre>' . ((is_object($GLOBALS["___mysqli_ston"])) ? mysqli_error($GLOBALS["___mysqli_ston"]) : (($___mysqli_res = mysqli_connect_error()) ? $___mysqli_res : false)) . '</pre>' );

    if( $result && mysqli_num_rows( $result ) == 1 ) {
        // Get users details
        $row    = mysqli_fetch_assoc( $result );
        $avatar = $row["avatar"];

        // Login successful
        echo "<p>Welcome to the password protected area {$user}</p>";
        echo "<img src=\"{$avatar}\" />";
    }
    else {
        // Login failed
        echo "<pre><br />Username and/or password incorrect.</pre>";
    }

    ((is_null($___mysqli_res = mysqli_close($GLOBALS["___mysqli_ston"]))) ? false : $___mysqli_res);
}

?> 
```

1、`$pass=md5[$pass];`:这里MD5没有加盐,容易受到彩虹表攻击
   `彩虹表攻击`:一种针对哈希密码的预计算破解技术,用提前算好的巨大哈希对照表,快速反推明文密码,不用在线暴力逐个哈希计算;缺点:对加盐哈希 (salt)基本失效

2、`$query  = "SELECT * FROM `users` WHERE user = '$user' AND password = '$pass';";`:`$user`未转义直接拼接到SQL中,攻击者可以在用户名中输入`' OR '1'='1 --`等payload,改变查询逻辑,从而绕过密码验证;由于`$pass`被MD5成固定格式,注入点主要在`$user`

3、`if( $result && mysqli_num_rows( $result ) == 1 ) {`:如果查询成功,并且返回的结果集行数恰好为1,则认为登录成功

4、`mysqli_fetch_assoc()`:从SQL查询结果集中取出一行数据,返回一个关联数组,key是字段明,value是字段值

5、`echo "<p>Welcome to the password protected area {$user}</p>";`:直接插入`$user`未经过HTML转义,存在XSS漏洞,攻击者可以直接在用户名中注入脚本