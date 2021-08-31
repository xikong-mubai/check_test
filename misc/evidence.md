# 取证

## 介绍

何为取证？

电子取证是指利用计算机软硬件技术，以符合法律规范的方式对计算机入侵、破坏、欺诈、攻击等犯罪行为进行证据获取、保存、分析和出示的过程。从技术方面看，计算机犯罪取证是一个对受侵计算机系统进行扫描和破解，对入侵事件进行重建的过程。具体而言，是指把计算机看作犯罪现场，运用先进的辨析技术，对计算机犯罪行为进行解剖，搜寻罪犯及其犯罪证据。

接下来我们从常用的取证工具入手，来讲解取证的常见内容。

之所以从工具入手，是因为取证过程中如果不依靠现有的强大工具，就需要取证的人自己对相关数据文件的数据存储格式有详细的了解乃至是掌握。
取证工具的本质其实就是对已知存储格式的数据从格式上进行自动化地解析使得使用者可以轻松提取相应的数据资料。如果以手工的方式的话则需要大篇幅的内容来讲解各种诸如硬盘系统数据文件、内存镜像数据文件一类的相关数据存储的格式。

## 内存取证——Volatility

Volatility是开源的Windows，Linux，MaC，Android的内存取证分析工具，由python编写成，命令行操作，支持各种操作系统。

并且该工具属于框架类工具。即其本身除却官方自己实现的功能插件外，用户可以根据自己需要来制作自定义插件。

通过-h参数可以列举出本地工具已经集成了的功能插件以及相关描述。

![20210831144144](https://gitee.com/ye_xi_bai/blogimage/raw/master/blogimages20210831144144.png)

这里介绍一个叫`dumpIt`的工具，它可以把当前运行的系统的内存数据导出为静态镜像文件。

### imageinfo

对于内存取证，不同版本的系统运行时的内存数据格式是不一样的，利用这一点，可以先行分析出目标内存镜像对应的系统版本。然后再根据系统版本进行下一步的分析。

功能插件为`imageinfo`，

![20210831143335](https://gitee.com/ye_xi_bai/blogimage/raw/master/blogimages20210831143335.png)

### pstree|pslist|psscan|psxview

ps插件全家桶。它们的功能如图：   对内存数据进行分析显然不能错过系统运行时的进程信息分析。而这四个命令则类似`Linux`系统中的`ps`命令，可以列举系统运行中的进程。
根据列举出的进程可以初步猜测是否受到了进程注入类的攻击。

![20210831145117](https://gitee.com/ye_xi_bai/blogimage/raw/master/blogimages20210831145117.png)

三者的详细区别：

+ pslist。不仅显示了所有正在运行的进程，而且给出了有价值的信息，比如PID、PPID、启动的时间。
+ pstree。pslist的改进版，可以识别子进程以及父进程
+ psscan。可以显示出被恶意软件比如rootkit为了躲避用户或杀毒软件而隐藏的进程
+ psxview。psscan的改进版。

![20210831151115](https://gitee.com/ye_xi_bai/blogimage/raw/master/blogimages20210831151115.png)

### memdump

`memdump`可以提取出内存中的进程数据。许多进程在运行时，原始数据都是在进程中存储的，比较经典的例子就是画图程序。memdump导出的画图程序内存数据导入图像处理程序调整长宽后可以直接恢复图像内容。

![20210831154927](https://gitee.com/ye_xi_bai/blogimage/raw/master/blogimages20210831154927.png)

### procdump

提取进程的可执行文件。通过导出可疑进程的可执行文件来对其进行逆向分析，挖掘可能存在的后面病毒木马之类的程序。

![20210831172515](https://gitee.com/ye_xi_bai/blogimage/raw/master/blogimages20210831172515.png)

### timeliner

根据时间线列举系统行为。

![20210831162505](https://gitee.com/ye_xi_bai/blogimage/raw/master/blogimages20210831162505.png)

### cmdline|cmdscan|consoles

这三个功能插件可以列举系统运行时由`cmd`执行过的命令

![20210831145659](https://gitee.com/ye_xi_bai/blogimage/raw/master/blogimages20210831145659.png)

![20210831151149](https://gitee.com/ye_xi_bai/blogimage/raw/master/blogimages20210831151149.png)

### iehistory

此插件可以查看系统运行时的浏览缓存历史。

![20210831152331](https://gitee.com/ye_xi_bai/blogimage/raw/master/blogimages20210831152331.png)

### connections|connscan

这两个插件则可以列举系统当时的网络连接情况

![20210831152751](https://gitee.com/ye_xi_bai/blogimage/raw/master/blogimages20210831152751.png)

### notepad|editbox

这两个插件可以找出正在编辑中的文本数据。`editbox`比`notepad`适用性广一点。

![20210831153450](https://gitee.com/ye_xi_bai/blogimage/raw/master/blogimages20210831153450.png)

### filescan|dumpfiles

`filescan`可以输出系统文件列表。`dumpfiles`可以提取被加载进内存的文件数据。

![20210831153815](https://gitee.com/ye_xi_bai/blogimage/raw/master/blogimages20210831153815.png)

### hashdump

该工具可以抓取当前系统中的用户名及其密码对应的`NTML`哈希值

![20210831161550](https://gitee.com/ye_xi_bai/blogimage/raw/master/blogimages20210831161550.png)

### hivelist|hivescan|hivedump

hivescan插件显示了可用的注册表配置单元的物理地址

![20210831162126](https://gitee.com/ye_xi_bai/blogimage/raw/master/blogimages20210831162126.png)

更加详细的信息可以通过hivelist命令查看，这条命令会显示虚拟地址、物理地址的细节以及更容易识别的路径等

![20210831162202](https://gitee.com/ye_xi_bai/blogimage/raw/master/blogimages20210831162202.png)

hivedump则可以导出注册表信息

![20210831172108](https://gitee.com/ye_xi_bai/blogimage/raw/master/blogimages20210831172108.png)

### printkey

查看内存加载的注册表中的键值

![20210831172139](https://gitee.com/ye_xi_bai/blogimage/raw/master/blogimages20210831172139.png)

### dlllist|dlldump

dlllist可以看到每个进程运行需要的dll，dlldump可以导出进程运行中加载的dll

![20210831172819](https://gitee.com/ye_xi_bai/blogimage/raw/master/blogimages20210831172819.png)

![20210831172840](https://gitee.com/ye_xi_bai/blogimage/raw/master/blogimages20210831172840.png)

### svcscan（限windwos）

查看开启的windows服务。

![20210831173413](https://gitee.com/ye_xi_bai/blogimage/raw/master/blogimages20210831173413.png)

### modules|modscan|driverscan

查看系统内核驱动。隐藏的用modscan或者driverscan

![20210831173551](https://gitee.com/ye_xi_bai/blogimage/raw/master/blogimages20210831173551.png)

### screenshot

查看当前屏幕每个窗口中内容的轮廓线。

![20210831173724](https://gitee.com/ye_xi_bai/blogimage/raw/master/blogimages20210831173724.png)

![20210831173817](https://gitee.com/ye_xi_bai/blogimage/raw/master/blogimages20210831173817.png)
