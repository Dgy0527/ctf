# 暴力破解medium

# 目录源码
```
<?php                                                                         
                                                                              
if( isset( $_POST[ 'Submit' ] ) ) {                                           
        // Get input                                                          
        $id = $_POST[ 'id' ];                                                 
                                                                              
        $id = mysqli_real_escape_string($GLOBALS["___mysqli_ston"], $id);     
                                                                              
        $query  = "SELECT first_name, last_name FROM users WHERE user_id = $id;";                                                                           
        $result = mysqli_query($GLOBALS["___mysqli_ston"], $query) or die( '<pre>' . mysqli_error($GLOBALS["___mysqli_ston"]) . '</pre>' );                 
                                                                              
        // Get results                                                        
        while( $row = mysqli_fetch_assoc( $result ) ) {                       
                // Display values                                             
                $first = $row["first_name"];                                  
                $last  = $row["last_name"];                                   
                                                                              
                // Feedback for end user
                $html .= "<pre>ID: {$id}<br />First name: {$first}<br />Surname: {$last}</pre>";
        }

}

// This is used later on in the index.php page
// Setting it here so we can close the database connection in here like in the rest of the source scripts
$query  = "SELECT COUNT(*) FROM users;";
$result = mysqli_query($GLOBALS["___mysqli_ston"],  $query ) or die( '<pre>' . ((is_object($GLOBALS["___mysqli_ston"])) ? mysqli_error($GLOBALS["___mysqli_ston"]) : (($___mysqli_res = mysqli_connect_error()) ? $___mysqli_res : false)) . '</pre>' );
$number_of_rows = mysqli_fetch_row( $result )[0];

mysqli_close($GLOBALS["___mysqli_ston"]);
?>
```

1、`if( isset( $_POST[ 'Submit' ] ) )`:检查是否通过POST请求提交名为Submit的参数(通常对应表单提交按钮)

2、`$id = $_POST[ 'id' ];`:从POST请求中获取id参数的值,使用POST比GET稍安全,但仍需过滤

3、`mysqli_real_escape_string()`:对字符串中的特殊字符进行转义,用来防御SQL注入,转义MySQL里有特殊含义的字符(如:'、''、\、NUL、\r、\n);但是这个函数只对字符串上下文有效,如果SQL语句里没有引号包裹变量,仍可注入(转义不会改变空格和字母);数字型注入

4、`$query  = "SELECT COUNT(*) FROM users;";`:构造查询,统计users表中总行数



# 页面源码
```
<?php

if( isset( $_GET[ 'Login' ] ) ) {
    // Sanitise username input(清理用户名输入)
    $user = $_GET[ 'username' ];
    $user = ((isset($GLOBALS["___mysqli_ston"]) && is_object($GLOBALS["___mysqli_ston"])) ? mysqli_real_escape_string($GLOBALS["___mysqli_ston"],  $user ) : ((trigger_error("[MySQLConverterToo] Fix the mysql_escape_string() call! This code does not work.", E_USER_ERROR)) ? "" : ""));

    // Sanitise password input(清理密码输入)
    $pass = $_GET[ 'password' ];
    $pass = ((isset($GLOBALS["___mysqli_ston"]) && is_object($GLOBALS["___mysqli_ston"])) ? mysqli_real_escape_string($GLOBALS["___mysqli_ston"],  $pass ) : ((trigger_error("[MySQLConverterToo] Fix the mysql_escape_string() call! This code does not work.", E_USER_ERROR)) ? "" : ""));
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
        sleep( 2 );
        echo "<pre><br />Username and/or password incorrect.</pre>";
    }

    ((is_null($___mysqli_res = mysqli_close($GLOBALS["___mysqli_ston"]))) ? false : $___mysqli_res);
}

?> 
```

1、`? "" : ""`:无论真假都返回空字符串,这是代码生成器的冗余写法

2、`$query  = "SELECT * FROM `users` WHERE user = '$user' AND password = '$pass';";`:从users表中选择所有列;'*'在select查询语句中叫做通配符,代表所有列(表里的全部字段)

3、`$query  = "SELECT * FROM `users` WHERE user = '$user' AND password = '$pass';";`:`$user`和`$pass`都被单引号包裹,且之前已用`mysqli_real_escape_string`转义,SQL注入风险降低(仍需注意宽字节注入等特殊情况)

4、`if( $result && mysqli_num_rows( $result ) == 1 ) {`:如果查询成功且返回恰好一行,则认为登陆成功

5、`sleep( 2 );`:睡眠2秒,增加暴力破解的时间成本,减缓攻击速度