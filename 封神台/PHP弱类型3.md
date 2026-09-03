# 1、strlen():获取字符串长度
## strlen("100"); //返回3

## strlen("abc"); //返回3

## strlen("你好"); //返回6,因为一个汉字占3个字节(UTF-8)

### 如果传入数组([]),strlen()不会报错终止,而是返回Null同时产生警告,但是警告被erro_reporting(0)屏蔽了,Null参与数值比较时会被自动转换0



# 2、strcmp():二进制安全字符串比较,即比较两个字符串
## str1<str2,返回负数

## str1>str2,返回正数

## str1=str2,返回0

## strcmp("100","100") //返回0

## strcmp("abc","abd") //返回-1,因为c<d



# 绕过关键:如果strcmp传入数组作为第一个参数strcmp([1],"100"),则返回Null,Null与0进行松散比较(==)时,Null转为0,Null==0则比较检查被绕过



 
  