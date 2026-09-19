# 暴力破解(impossible)

# 目录源码
```
<?php

if( isset( $_GET[ 'Submit' ] ) ) {
        // Check Anti-CSRF token
        checkToken( $_REQUEST[ 'user_token' ], $_SESSION[ 'session_token' ], 'index.php' );

        // Get input
        $id = $_GET[ 'id' ];

        // Was a number entered?
        if(is_numeric( $id )) {
                // Check the database
                $data = $db->prepare( 'SELECT first_name, last_name FROM users WHERE user_id = (:id) LIMIT 1;' );
                $data->bindParam( ':id', $id, PDO::PARAM_INT );
                $data->execute();
                $row = $data->fetch();

                // Make sure only 1 result is returned
                if( $data->rowCount() == 1 ) {
                        // Get values
                        $first = $row[ 'first_name' ];
                        $last  = $row[ 'last_name' ];

                        // Feedback for end user
                        $html .= "<pre>ID: {$id}<br />First name: {$first}<br />Surname: {$last}</pre>";
                }
        }
}

// Generate Anti-CSRF token
generateSessionToken();

?>

```

1、`if(is_numeric( $id )) {`:`使用is_numeric()`检查`$id`是否为数字(整数或浮点数),如果不是数字则跳过整个数据库查询块;这是第一层防护:防止字符串型注入

2、`$data = $db->prepare( 'SELECT first_name, last_name FROM users WHERE user_id = (:id) LIMIT 1;' );`:
使用PDO的prepare()方法准备一条SQL语句;`$db`是PDO数据库连接对象;使用命名占位符`:id`,而不是直接拼接变量;`limit 1`:限制最多返回一行;这是第二层防护:预处理语句将sql逻辑与数据分离,防止注入

POD prepare():预处理sql语句,把sql结构和用户输入数据分开,输入只被当成数据,不会被解析成sql代码,防止sql注入
占位符:(1)命令占位符`:id`,可读性好;(2)问号占位符`?`

3、`$data->bindParam( ':id', $id, PDO::PARAM_INT );`:指定参数类型为`PDO::PARAM_INT`(整数),确保`$id`被当作整数处理,即使输入包含恶意内容也会被强制转化为整数,进一步防止注入

4、`$data->execute();`:执行预处理语句
`execute()`:只把用户数据单独传给数据库

5、`$row = $data->fetch();`:从结果集中获取一行数据,默认获取模式为关联数组(取决于PDO设置)

6、`if( $data->rowCount() == 1 ) {`:检查受影响的行数是否恰好为1,如果是,说明找到了匹配的用户

7、`generateSessionToken()`:为下一次请求生成新的会话token,确保每次请求都使用新的token,防止CSRF攻击



# 页面源码
```
 <?php

if( isset( $_POST[ 'Login' ] ) && isset ($_POST['username']) && isset ($_POST['password']) ) {
    // Check Anti-CSRF token
    checkToken( $_REQUEST[ 'user_token' ], $_SESSION[ 'session_token' ], 'index.php' );

    // Sanitise username input
    $user = $_POST[ 'username' ];
    $user = stripslashes( $user );
    $user = ((isset($GLOBALS["___mysqli_ston"]) && is_object($GLOBALS["___mysqli_ston"])) ? mysqli_real_escape_string($GLOBALS["___mysqli_ston"],  $user ) : ((trigger_error("[MySQLConverterToo] Fix the mysql_escape_string() call! This code does not work.", E_USER_ERROR)) ? "" : ""));

    // Sanitise password input
    $pass = $_POST[ 'password' ];
    $pass = stripslashes( $pass );
    $pass = ((isset($GLOBALS["___mysqli_ston"]) && is_object($GLOBALS["___mysqli_ston"])) ? mysqli_real_escape_string($GLOBALS["___mysqli_ston"],  $pass ) : ((trigger_error("[MySQLConverterToo] Fix the mysql_escape_string() call! This code does not work.", E_USER_ERROR)) ? "" : ""));
    $pass = md5( $pass );

    // Default values
    $total_failed_login = 3;
    $lockout_time       = 15;
    $account_locked     = false;

    // Check the database (Check user information)
    $data = $db->prepare( 'SELECT failed_login, last_login FROM users WHERE user = (:user) LIMIT 1;' );
    $data->bindParam( ':user', $user, PDO::PARAM_STR );
    $data->execute();
    $row = $data->fetch();

    // Check to see if the user has been locked out.
    if( ( $data->rowCount() == 1 ) && ( $row[ 'failed_login' ] >= $total_failed_login ) )  {
        // User locked out.  Note, using this method would allow for user enumeration!
        //echo "<pre><br />This account has been locked due to too many incorrect logins.</pre>";

        // Calculate when the user would be allowed to login again
        $last_login = strtotime( $row[ 'last_login' ] );
        $timeout    = $last_login + ($lockout_time * 60);
        $timenow    = time();

        /*
        print "The last login was: " . date ("h:i:s", $last_login) . "<br />";
        print "The timenow is: " . date ("h:i:s", $timenow) . "<br />";
        print "The timeout is: " . date ("h:i:s", $timeout) . "<br />";
        */

        // Check to see if enough time has passed, if it hasn't locked the account
        if( $timenow < $timeout ) {
            $account_locked = true;
            // print "The account is locked<br />";
        }
    }

    // Check the database (if username matches the password)
    $data = $db->prepare( 'SELECT * FROM users WHERE user = (:user) AND password = (:password) LIMIT 1;' );
    $data->bindParam( ':user', $user, PDO::PARAM_STR);
    $data->bindParam( ':password', $pass, PDO::PARAM_STR );
    $data->execute();
    $row = $data->fetch();

    // If its a valid login...
    if( ( $data->rowCount() == 1 ) && ( $account_locked == false ) ) {
        // Get users details
        $avatar       = $row[ 'avatar' ];
        $failed_login = $row[ 'failed_login' ];
        $last_login   = $row[ 'last_login' ];

        // Login successful
        echo "<p>Welcome to the password protected area <em>{$user}</em></p>";
        echo "<img src=\"{$avatar}\" />";

        // Had the account been locked out since last login?
        if( $failed_login >= $total_failed_login ) {
            echo "<p><em>Warning</em>: Someone might of been brute forcing your account.</p>";
            echo "<p>Number of login attempts: <em>{$failed_login}</em>.<br />Last login attempt was at: <em>${last_login}</em>.</p>";
        }

        // Reset bad login count
        $data = $db->prepare( 'UPDATE users SET failed_login = "0" WHERE user = (:user) LIMIT 1;' );
        $data->bindParam( ':user', $user, PDO::PARAM_STR );
        $data->execute();
    } else {
        // Login failed
        sleep( rand( 2, 4 ) );

        // Give the user some feedback
        echo "<pre><br />Username and/or password incorrect.<br /><br/>Alternative, the account has been locked because of too many failed logins.<br />If this is the case, <em>please try again in {$lockout_time} minutes</em>.</pre>";

        // Update bad login count
        $data = $db->prepare( 'UPDATE users SET failed_login = (failed_login + 1) WHERE user = (:user) LIMIT 1;' );
        $data->bindParam( ':user', $user, PDO::PARAM_STR );
        $data->execute();
    }

    // Set the last login time
    $data = $db->prepare( 'UPDATE users SET last_login = now() WHERE user = (:user) LIMIT 1;' );
    $data->bindParam( ':user', $user, PDO::PARAM_STR );
    $data->execute();
}

// Generate Anti-CSRF token
generateSessionToken();

?>

```

1、`$total_failed_login = 3;`:允许的最大失败登录次数
   `$lockout_time =15;`:锁定时长(分钟)
   `$account_locked = false;`:账户锁定标志,初始为未锁定

2、`$data = $db->prepare( 'SELECT failed_login, last_login FROM users WHERE user = (:user) LIMIT 1;' );`:使用PDO预处理语句查询数据库中该用户的`failed_login`(失败次数)和`last_login`(最后登录时间)

3、`$data->bindParam( ':user', $user, PDO::PARAM_STR );`:bindParam()将`$user`绑定到占位符,指定类型为字符串

4、`$row = $data->fetch();`:fetch()获取一行结果

5、` if( ( $data->rowCount() == 1 ) && ( $row[ 'failed_login' ] >= $total_failed_login ) )  {`:如果查询到该用户`(rowCount()==1)`且其`failed_login`次数大于等于3,则检查是否处于锁定期

6、`$last_login = strtotime( $row[ 'last_login' ] );`:`strtotime()`:将最后登录时间字符串转换为Unix时间戳
   `$timeout    = $last_login + ($lockout_time * 60);`:最后登录时间加上15分钟
   `$timenow = time()`:当前时间戳

7、`sleep( rand( 2, 4 ) )`:随机睡眠2-4秒,增加暴力破解的时间成本