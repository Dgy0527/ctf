# 暴力破解(high)

# 目录源码
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
                $html .= "<pre>ID: {$id}<br />First name: {$first}<br />Surname: {$last}</pre>";
        }

        ((is_null($___mysqli_res = mysqli_close($GLOBALS["___mysqli_ston"]))) ? false : $___mysqli_res);
}

?>
```
1、`if( isset( $_SESSION [ 'id' ] ) ) {`:输入不直接来自用户请求,而是来自服务器端的会话

2、`$id = $_SESSION[ 'id' ];`:攻击者无法直接通过URL或表单修改它

3、`$query  = "SELECT first_name, last_name FROM users WHERE user_id = '$id' LIMIT 1;";`:$id被单引号包裹,但没有经过转义,仍然存在SQL注入风险;limit 1限制最多返回一行,可以防止union注入返回多行数据,增加利用难度,但不能完全阻止注入(如通过注释符截断后续语句或用子查询)



# 页面源码
```
<?php

if( isset( $_GET[ 'Login' ] ) ) {
    // Check Anti-CSRF token
    checkToken( $_REQUEST[ 'user_token' ], $_SESSION[ 'session_token' ], 'index.php' );

    // Sanitise username input
    $user = $_GET[ 'username' ];
    $user = stripslashes( $user );
    $user = ((isset($GLOBALS["___mysqli_ston"]) && is_object($GLOBALS["___mysqli_ston"])) ? mysqli_real_escape_string($GLOBALS["___mysqli_ston"],  $user ) : ((trigger_error("[MySQLConverterToo] Fix the mysql_escape_string() call! This code does not work.", E_USER_ERROR)) ? "" : ""));

    // Sanitise password input
    $pass = $_GET[ 'password' ];
    $pass = stripslashes( $pass );
    $pass = ((isset($GLOBALS["___mysqli_ston"]) && is_object($GLOBALS["___mysqli_ston"])) ? mysqli_real_escape_string($GLOBALS["___mysqli_ston"],  $pass ) : ((trigger_error("[MySQLConverterToo] Fix the mysql_escape_string() call! This code does not work.", E_USER_ERROR)) ? "" : ""));
    $pass = md5( $pass );

    // Check database
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
        sleep( rand( 0, 3 ) );
        echo "<pre><br />Username and/or password incorrect.</pre>";
    }

    ((is_null($___mysqli_res = mysqli_close($GLOBALS["___mysqli_ston"]))) ? false : $___mysqli_res);
}

// Generate Anti-CSRF token
generateSessionToken();

?> 
```

1、`checkToken( $_REQUEST[ 'user_token' ], $_SESSION[ 'session_token' ], 'index.php' );`:验证请求中的`user_token`是否与服务器会话中的session_token匹配,如果不匹配则重定向到index.php,这是防止跨站请求伪造(CSRF)攻击,攻击者无法伪造带有正确token的请求;
checkToken():开发者自定义的函数-校验令牌,CSRF校验、接口鉴权、登录态校验、权限验证

2、`$user = stripslashes( $user );`:用`stripslashes()`去除字符串中的反斜杠

`stripslashes()`:删除字符串中的反斜杠\
`addslashes()`:给字符串加转义斜杠
`magic_quotes_gpc`:魔术引号
`magic_quotes_gpc=On`时,php自动对GPC(GET、POST、Cookie)传入的数据做addslashes()
`get_magic_quotes_gpc()`:判断魔术引号是否开启

3、`sleep( rand( 0, 3 ) )`:随机睡眠0到3秒,增加了暴力破解的时间成本

4、`generateSessionToken()`:为下一次请求生成新的会话token,这样每次登录尝试都要新的token,阻止自动化暴力破解