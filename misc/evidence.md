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

`memdump`可以提取出内存中的进程数据。许多进程在运行时，原始数据都是在进程中存储的，比较经典的例子就是 提取`lsass`进程的数据，然后利用`mimikalz`工具抓取用户的明文密码或者说还原用户认证信息。

![20210831154927](https://gitee.com/ye_xi_bai/blogimage/raw/master/blogimages20210831154927.png)

### procdump

提取进程的可执行文件。通过导出可疑进程的可执行文件来对其进行逆向分析，挖掘可能存在的后门病毒木马等。

![20210831172515](https://gitee.com/ye_xi_bai/blogimage/raw/master/blogimages20210831172515.png)

### timeliner

根据时间线列举系统行为。通过时间线的排布来对可疑程序的可疑行为进行顺藤摸瓜式的排查。

![20210831162505](https://gitee.com/ye_xi_bai/blogimage/raw/master/blogimages20210831162505.png)

### cmdline|cmdscan|consoles

这三个功能插件可以列举系统运行时由`cmd`执行过的命令。对于一些后台调用了`cmd`的程序可以看到它们的调用历史以及传入参数，遇见不常见的后台调用或者说可疑传参的时候可以结合其它功能对其进行深入分析。

![20210831145659](https://gitee.com/ye_xi_bai/blogimage/raw/master/blogimages20210831145659.png)

![20210831151149](https://gitee.com/ye_xi_bai/blogimage/raw/master/blogimages20210831151149.png)

### iehistory

此插件可以查看系统运行时的浏览记录。这个浏览记录包括本地文件记录和浏览器网络链接记录，借此可以分析攻击者进入系统后的行为。

![20210831152331](https://gitee.com/ye_xi_bai/blogimage/raw/master/blogimages20210831152331.png)

### connections|connscan

这两个插件则可以列举系统当时的网络连接情况。根据网络连接的IP和端口可以初步分析是否收到了常见的漏洞攻击。同时也可以在掌握了攻击者的攻击痕迹之后模拟现场。

![20210831152751](https://gitee.com/ye_xi_bai/blogimage/raw/master/blogimages20210831152751.png)

### notepad|editbox

这两个插件可以找出正在编辑中的文本数据。`editbox`比`notepad`适用性广一点。

![20210831153450](https://gitee.com/ye_xi_bai/blogimage/raw/master/blogimages20210831153450.png)

### filescan|dumpfiles

`filescan`可以输出系统文件列表。`dumpfiles`可以提取被加载进内存的文件数据。
比如在查看cmd命令时发现执行了可疑的可执行程序或者说脚本文件时可以直接提取出来分析其内容。

![20210831153815](https://gitee.com/ye_xi_bai/blogimage/raw/master/blogimages20210831153815.png)

### hashdump

该工具可以抓取当前系统中的用户名及其密码对应的`NTML`哈希值。如果攻击者创建了影子账户，利用该命令可直接发现。

![20210831161550](https://gitee.com/ye_xi_bai/blogimage/raw/master/blogimages20210831161550.png)

### hivelist|hivescan|hivedump

hivescan插件显示了可用的注册表配置单元的物理地址

![20210831162126](https://gitee.com/ye_xi_bai/blogimage/raw/master/blogimages20210831162126.png)

更加详细的信息可以通过hivelist命令查看，这条命令会显示虚拟地址、物理地址的细节以及更容易识别的路径等

![20210831162202](https://gitee.com/ye_xi_bai/blogimage/raw/master/blogimages20210831162202.png)

hivedump则可以导出注册表信息

![20210831172108](https://gitee.com/ye_xi_bai/blogimage/raw/master/blogimages20210831172108.png)

### printkey

查看内存加载的注册表中的键值。比如在进程分析时发现了对注册表的修改痕迹，可以直接查询对应注册表的键值判断是否是攻击行为的修改。

![20210831172139](https://gitee.com/ye_xi_bai/blogimage/raw/master/blogimages20210831172139.png)

### dlllist|dlldump

dlllist可以看到每个进程运行需要的dll，dlldump可以导出进程运行中加载的dll。
这一条针对windows系统中的dll注入。

![20210831172819](https://gitee.com/ye_xi_bai/blogimage/raw/master/blogimages20210831172819.png)

![20210831172840](https://gitee.com/ye_xi_bai/blogimage/raw/master/blogimages20210831172840.png)

### svcscan（限windows）

查看开启的windows服务。通过开启的服务可以对常见的出名的漏洞攻击做一个快速过滤。

![20210831173413](https://gitee.com/ye_xi_bai/blogimage/raw/master/blogimages20210831173413.png)

### modules|modscan|driverscan

查看系统内核驱动。隐藏的用modscan或者driverscan

![20210831173551](https://gitee.com/ye_xi_bai/blogimage/raw/master/blogimages20210831173551.png)

### screenshot

查看当前屏幕每个窗口中内容的轮廓线。属于侧信道信息分析范畴，一般用不到。

![20210831173724](https://gitee.com/ye_xi_bai/blogimage/raw/master/blogimages20210831173724.png)

![20210831173817](https://gitee.com/ye_xi_bai/blogimage/raw/master/blogimages20210831173817.png)

## 硬盘取证

硬盘取证的常见场景一般多为可疑文件数据恢复与查找

一般来说，恢复被恶意删除的文件会遇到如下四种情况。

1. **目录项未覆盖，文件数据未覆盖**
2. **目录项已覆盖，文件数据未覆盖**
3. **目录项未覆盖，文件数据已覆盖**
4. **目录项已覆盖，文件数据已覆盖**

什么是目录项呢？

    关于目录项，它是文件系统在存储数据时规定的一个固定数据格式的数据，不同的文件系统会有不同的规定内容，但必然会存在这个结构，不然文件系统自己也无法判断在一个地方放的是什么东西有多长叫什么名字。每个目录下的所有文件和文件夹的目录项都会按顺序放在同一个数据区存储。

    这个数据区中的每一条数据便对应了硬盘中存储的一个文件或者说一个文件夹，其中有着这个文件的名字大小类型位置等基础信息。

也就是说，**文件系统在寻找存储在硬盘中的文件时，是先去目录区查找对应文件的目录项，从中得知目标文件的各种信息，然后直接定位文件**。而**文件系统删除文件时之所以如此之快也正是因为它并非真正意义上的删除了文件，而是修改了文件目录项的状态值**。

现在也就可以知道以上四种情况意味着什么了。

前两种意味着文件可以被恢复，但是第一种可以简单的恢复，即利用`DiskGenius`这种工具直接提取恢复：

### 文件的数据恢复与查询——DiskGenius

`DiskGenius`这个工具其实正常多用在重装系统或者说修电脑的辅助工具。但是因为功能强大，于是在进行硬盘取证的时候也常常可以用到。

最为常见的场景便是**对于删除文件的恢复**。

![20210901115958](https://gitee.com/ye_xi_bai/blogimage/raw/master/blogimages20210901115958.png)

第二种情况只是**理论上可被恢复，实际情况根据文件本身的大小以及文件类型格式，恢复难度也不一样。因为目录项已被覆盖，以及无法简单的通过工具的方式提取。而文件系统在存储大文件时，往往会将其分块存储，所以对于被分块的大文件已经可以说是不能被恢复了。至于体积较小未能分块存储的文件则可以通过文件特征值扫描的方式尝试提取恢复**。 这里可以考虑使用`binwalk`工具自动扫描。

第三种则是可以**根据工具快速查看到删除文件“生前”的基础信息，如名字大小格式等，但已无法直接恢复**。（如上图）如果**文件数据仅仅是某些固定的格式信息区被覆盖尚有恢复可能，但如若记载的数据都已经覆盖，则可以当作无法恢复处理**。

**最后一种则意味着彻底移除，已不存在恢复可能**。**低级格式化之所以安全就是因为达到了这种效果，相反，高级格式化之所以仍有数据泄露的可能，正是因为高级格式化主要是清空了文件目录项，但对于硬盘本身存储的数据区内容为了效率原因并未做过多处理**。

### 文件系统格式损坏

除了恢复被删文件，还有另外一些常见场景，那便是文件系统格式损坏，正在运行的机械硬盘摔一下就坏了主要就是这种原因。除了目录项以外，文件系统还有其它关键性的自身基础信息，当它们被破坏后，便无法被正常识别是何系统，有哪些基础设置，从而导致操作系统无法解析该硬盘。

但是根据前文我们可以知道，文件系统的其他信息损坏并没有从根本上损坏存储介质中的数据。这个时候只要能知道原存储介质中使用的是哪种文件系统，即可采取手工恢复的方式抢救重要数据或者说取证。

这里我们用一道CTF中的例题来讲解一下硬盘取证的姿势。

#### 判断文件系统信息

这里题目文件故意抹去了文件开头0x200字节的代表着文件系统信息的数据。并在文件末尾丢了一个烟雾弹出来。

![20210902143338](https://gitee.com/ye_xi_bai/blogimage/raw/master/blogimages20210902143338.png)

![20210902143426](https://gitee.com/ye_xi_bai/blogimage/raw/master/blogimages20210902143426.png)

抹去了原本的信息，在结尾放上了一个`NTFS`文件系统的格式数据。

这里我们先不去在意这个烟雾弹，去看看其他数据有无类似特征值一般的存在。比如说第一张图中那看起来容易引人在意的`RRaA`，有经验的人就知道，这四个字节代表着原文件系统很可能是`FAT`系列的文件系统，这里我们往下看一下，发现距离`RRaA`不到`0x200`字节就有另外一个大小写相反的`rrAa`字符。

![20210902143637](https://gitee.com/ye_xi_bai/blogimage/raw/master/blogimages20210902143637.png)

简单用搜索引擎查找一下资料就可以知道，这确实就是`FAT`系列文件系统的特征值之一。
通过查询`FAT`相关的文件系统的资料。我们可以得知，FAT后跟的数字其实是类似`数据总线`宽度的存在。这也是为什么`FAT32`文件系统最大仅支持`4GB`大小的文件存储的原因，32bit的数据宽度，意味着在描述文件大小时，最大值即为`0xffffffff`byte，也即是`4GB`。

对于FAT文件系统，它一般有四个组成部分。

|DBR及其保留扇区|FAT1|FAT2|DATA|
|-|-|-|-|

DBR及其保留扇区：DBR的含义是DOS引导记录，也称为操作系统引导记录，在DBR之后往往会有一些保留扇区。这一块即为文件系统的基础信息数据。

FAT1：FAT的含义是文件分配表，FAT32一般有两份FAT，FAT1是第一份，也是主FAT。文件分配表，和前文提到的文件目录项存在对应关系。文件分配表的开头一般固定为`F8FFFF0FFFFFFF`.

FAT2：FAT2是FAT32的第二份文件分配表，也是FAT1的备份。既然是备份，自然与FAT1大小相同。

DATA：DATA也就是数据区，是FAT32文件系统的主要区域，其中包含存储目录项的区域。

另外这里简单说一下，磁盘的存储空间为方便定位，都有扇区的概念。即把**磁盘总空间平均分成固定份，一份就是一个扇区。常用的扇区大小*一般默认*使用一扇区200bytes**。然后因为现在的存储空间相对与200bytes来说太大了，所以**文件系统在扇区的基础上又引入了一个单位叫做簇，*一般默认*使用一簇对应八个扇区**。一扇区实际对应多少字节，一簇实际对应多少扇区，都直接记录在开头那被抹掉的200字节基础信息中。

**对于FAT系统而言有两个特殊簇，`data`区域前面的三个区域固定占据两个簇，无论实际规定的一簇为多大**。簇号从0开始，也就是`data`区从第 `2` 簇开始。而第 `2` 簇在`FAT`文件系统中默认分配给根目录的目录项表使用。

这里我们并不确定该硬盘镜像原本的数据分配，但我们可以先通过搜索特征值的方式找到`FAT1`和`FAT2`，如此便可以直接确认`DATA`区的起始位置，也即根目录目录项的所在。

![20210902151926](https://gitee.com/ye_xi_bai/blogimage/raw/master/blogimages20210902151926.png)

这里我们定位到了FAT1和2的位置，直接二者起始地址相减得到FAT1和2的大小，然后即可找到`DATA`的起始地址为`FE000`。

![20210902152115](https://gitee.com/ye_xi_bai/blogimage/raw/master/blogimages20210902152115.png)

#### 目录项结构

这里我们先简单介绍一下`FAT32`目录项的数据结构。
一个目录项固定为32字节。其中分为长目录项和短目录项。区分长短的原因就是因为，文件名是人为自定义的，不可能用短长度定死，所以对于名字较长的文件或者文件夹就用长目录项描述。

##### 短目录项

![20210902153407](https://gitee.com/ye_xi_bai/blogimage/raw/master/blogimages20210902153407.png)

时间的解析规则：

![20210902161537](https://gitee.com/ye_xi_bai/blogimage/raw/master/blogimages20210902161537.png)

日期的解析规则：

![20210902161600](https://gitee.com/ye_xi_bai/blogimage/raw/master/blogimages20210902161600.png)

##### 长目录项

![20210902153600](https://gitee.com/ye_xi_bai/blogimage/raw/master/blogimages20210902153600.png)

这里需要注意一点。对于FAT32中的长目录项而言，因为主要内容都用来存放文件名了，所以本身并不能存储文件或者说文件夹的其他信息，仅有名字显然不能用了当作合格的格式规定。

**另外凡是涉及整形数据存储皆为小端序**。

所以fat中的长目录项结束后必然跟着一个短目录项，长目录项主要用来存放文件名，短目录项用来存放文件的各种基础信息，这里举例说明：

![20210902153926](https://gitee.com/ye_xi_bai/blogimage/raw/master/blogimages20210902153926.png)

我们用图中第一个长目录项来解释。

0x00     ：`42`代表这是长目录项的结尾，且他是长目录项组合中的第二个。
0x01-0x0a: 用`utf-16`格式存储的部分文件名。这里为`（空格）Info`。
0x0b     : `0x0f` 代表这是长目录项。
0x0c     : 系统保留，默认为0。（扩展，可以利用系统保留位实现简单的消息隐藏，是为基于结构的隐写）
0x0d     : 通过文件名计算出来的校验值
0x0e-0x19: 用`utf-16`格式存储的部分文件名。这里为`rmatio`
0x1a-0x1b: 说是存放文件起始地址的簇号，其实完全没有用到，固定置0。这里可以结合上面那个系统保留位扩大隐写数据的大小。
0x1c-0x1f: 用`utf-16`格式存储的部分文件名。这里为`n`.(另外，若长目录项的文件名没有使用到的数据区默认用0xff填充。这里最后两字节为`0000`的原因是文件名作为字符串，需要用`00`截断，所以最后的`0000`其实是文件名的一部分，这里刚好用完，所以没有用到`0xff`填充多余空间)

往下看，第二条长目录项：

0x00     ：`01`代表这是长目录项的起始也即文件名开头。
0x01-0x0a: 用`utf-16`格式存储的部分文件名。这里为`Syste`
0x0b     : `0x0f` 代表这是长目录项。
0x0c     : 系统保留，默认为0。（扩展，可以利用系统保留位实现简单的消息隐藏，是为基于结构的隐写）
0x0d     : 通过文件名计算出来的校验值
0x0e-0x19: 用`utf-16`格式存储的部分文件名。这里为`m Volu`
0x1a-0x1b: 说是存放文件起始地址的簇号，其实完全没有用到，固定置0。这里可以结合上面那个系统保留位扩大隐写数据的大小。
0x1c-0x1f: 用`utf-16`格式存储的部分文件名。这里为`me`.(另外，若长目录项的文件名没有使用到的数据区默认用0xff填充。这里最后两字节为`0000`的原因是文件名作为字符串，需要用`00`截断，所以最后的`0000`其实是文件名的一部分，这里刚好用完，所以没有用到`0xff`填充多余空间)

再往下看，长目录项已经结束，这里是一个短目录项，用来记录上面那组长目录项记录的名字所对应的文件（夹）的基础信息。

0x00-0x07: 长文件名对应的短名。这里为`SYSTEM~1`.
0x08-0x0a: 文件扩展名，文件夹没有扩展名，故为三个空格.
0x0b     : `0x16`，代表是隐藏的系统级目录
0x0c     : 保留位。
0x0d     : 创建时间的10毫秒位
0x0e-0x0f: 文件创建时间 `68b5`，考虑小端序，实际为：`b568`，可解析出时间为：`22:43:16`
0x10-0x11: 文件创建日期 `aa52`，考虑小端序，实际为：`52aa`，可解析出日期为：`2021-05-10`
0x12-0x13: 文件最后访问日期。
0x14-0x15: 起始簇号高16位，依旧小端序。
0x16-0x17: 文件最近修改时间。
0x18-0x19: 文件最近修改日期。
0x1a-0x1b: 起始簇号高16位，依旧小端序。这里相当于 3
0x1c-0x1f: 文件长度，小端序。目录没有长度属性，故置零。

关于文件簇号和存储地址的转换，满足如下关系：

$$address_{file} = (cluster_{num} - 2) * size_{cluster} + address_{DATA}$$

$address_{file}$ 代表 文件的实际存储地址区。

$cluster_{num}$ 代表 文件目录项中的起始簇号。

$size_{cluster}$ 代表 该文件系统中，一簇占用的空间大小

$address_{DATA}$ 代表数据的起始地址

这里可以以用类对象的方式实现自动解析目录项数据

```python
    class Directory_entry():
        def __init__(self,data):
            self.data = data
            if data[0xb] == 0xf:
                self.long_filename()
                self.type = 1
            else:
                self.short_filename()
                self.type = 0

        def long_filename(self):
            self.final = (self.data[0] >> 6) & 1
            self.num = self.data[0] & 0x1f
            self.name = self.data[1:0xb].decode("utf-16")+self.data[0xe:0x1a].decode("utf-16")+self.data[-4:].decode("utf-16")
        
        def short_filename(self):
            self.name = self.data[:8].decode()
            self.typename = self.data[8:11].decode()
            self.cluster_num = struct.unpack('<I',self.data[0x1a:0x1c]+self.data[0x14:0x16])[0]
            self.length = struct.unpack('<I',self.data[-4:])[0]
```

然后便要想办法确认两个关键点，扇区大小，簇大小。

扇区大小的通过被抹去的DBR扇区数据大小以及`RRaA`对应的一个信息扇区可以确定就是200字节。
（FAT32文件系统在DBR的保留扇区中安排了一个文件系统信息扇区，用以记录数据区中空闲簇的数量及下一个空闲簇的簇号，该扇区一般在分区的1号扇区，也就是紧跟着DBR后的一个扇区，其内容如下：）

![572188-20200528151329123-2039003550](https://gitee.com/ye_xi_bai/blogimage/raw/master/blogimages572188-20200528151329123-2039003550.png)

现在只需要知道一个簇有几个扇区，重要信息就全部掌握了。
一般通过逆推的方式求簇中有几个扇区。

这里因为根目录有`flag.zip`，所以我们通过特征值搜索的方式找到它的地址。

![20210902165914](https://gitee.com/ye_xi_bai/blogimage/raw/master/blogimages20210902165914.png)

根据上述关系式代入计算。可得：

(0x1a216000-0xfe000)/（0x1a11a-2）= 4096 = 0x1000

可知，一簇为八个扇区，刚好是默认值。至此，即可通过脚本自动提取文件：

```python
    import struct
    import os

    FAT1_addr = 0x4400 # FAT1 起始地址
    FAT1_size = 999    # FAT1 占用的扇区数量
    cluster = 8        # 一簇为8扇区
    chunk_size = 0x200 # 一扇区为 200 bytes

    class Directory_entry():
        def __init__(self,data):
            self.data = data
            if data[0xb] == 0xf:
                self.long_filename()
                self.type = 1
            else:
                self.short_filename()
                self.type = 0

        def long_filename(self):
            self.final = (self.data[0] >> 6) & 1
            self.num = self.data[0] & 0x1f
            self.name = self.data[1:0xb].decode("utf-16")+self.data[0xe:0x1a].decode("utf-16")+self.data[-4:].decode("utf-16")
        
        def short_filename(self):
            self.name = self.data[:8].decode()
            self.typename = self.data[8:11].decode()
            self.cluster_num = struct.unpack('<I',self.data[0x1a:0x1c]+self.data[0x14:0x16])[0]
            self.length = struct.unpack('<I',self.data[-4:])[0]

    # 根据簇号计算地址
    def get_cluster_addr(cluster_num):
        return (cluster_num - 2) * 0x1000 + 0xfe000

    # 采用递归方式实现自动遍历目录提取文件
    def files_entry(f,files_path,cluster_num):
        f.seek(get_cluster_addr(cluster_num),0)
        addr = 0
        tmp = f.read(0x20) ; addr += 0x20
        while tmp != b'\x00'*0x20 and tmp != b'\x00':
            directory_entry = Directory_entry(tmp)
            if directory_entry.type == 1:
                tmp_num = directory_entry.num
                filename = directory_entry.name
                while tmp_num != 1:
                    tmp_directory_entry = Directory_entry(f.read(0x20))
                    addr += 0x20
                    tmp_num = tmp_directory_entry.num
                    filename = tmp_directory_entry.name + filename
                else:
                    directory_entry = Directory_entry(f.read(0x20))
                    addr += 0x20
            else:
                filename = directory_entry.name

            file_type = directory_entry.typename
            # 移除文件名中无效部分
            filename = filename.strip('\x20')
            filename = filename.strip('\x00')
            filename = filename.strip('\uffff')
            filename = filename.strip('\x20')
            filename = filename.strip('\x00')
            filename = filename.strip('\uffff')
            filename = filename.strip('\x20')
            filename = filename.strip('\x00')
            filename = filename.strip('\uffff')
            if file_type != '\x20\x20\x20' and file_type != None:
                filename += '.' + file_type

            if filename[0] == '\x2e':
                tmp = f.read(0x20) ; addr += 0x20
                continue
            elif filename[0] == '\xe5':
                filename = filename[1:] + '___deleted'
            
            if (directory_entry.data[11] >> 4) & 1 == 1:
                os.mkdir(files_path+'\\'+filename)
                files_entry(f,files_path+'\\'+filename,directory_entry.cluster_num)
                f.seek(get_cluster_addr(cluster_num)+addr,0)
            else:
                f.seek(get_cluster_addr(directory_entry.cluster_num),0)
                with open(files_path+'\\'+filename,'wb') as o:
                    o.write(f.read(directory_entry.length))
                f.seek(get_cluster_addr(cluster_num)+addr,0)
            tmp = f.read(0x20) ; addr += 0x20

    # 提取到 extra 目录下
    files_path = 'extra'
    os.mkdir(files_path)

    with open('./raw.img','rb') as f:
        addr = 0
        tmp = f.read(0x4400) ; addr += 0x4400
        FAT1 = f.read(FAT1_size*chunk_size) ; addr += FAT1_size*chunk_size
        f.read(FAT1_size*chunk_size) ; addr += FAT1_size*chunk_size
        
        files_entry(f,files_path,2)
```

## 日志分析

计算机、网络和其他IT系统生成审计跟踪记录或记录系统活动的日志。通过对这些记录的分析评估，帮助公司缓解各种风险或者发现受到的攻击行为。

日志分析主要分成两种：

+ Web日志分析

+ 系统日志分析

### Web日志分析

#### 日志格式类型

分析日志之前我们先了解一下日志的格式有哪些。

目前比较常见的WEB日志格式主要有两类：

+ Apache的NCSA日志格式，NCSA格式分为：
  + NCSA普通日志格式（CLF）
  + NCSA扩展日志格式（ECLF）
+ IIS的W3C日志格式

除了格式不同之外，一般的分析方法基本相似，下面用NCSA普通日志格式进行讲解。

首先，它的格式如下：

![20210902171847](https://gitee.com/ye_xi_bai/blogimage/raw/master/blogimages20210902171847.png)

#### 常用日志分析方法

常见的日志分析方法有两种：

1. 特征字符分析

2. 访问频率分析

##### 特征字符分析

特征字符分析法：顾名思义，就是根据攻击者利用的漏洞特征，进行判断攻击者使用的是哪一种攻击。

常见的类型有SQL注入、XSS跨站脚本攻击、恶意文件上传、一句话木马连接等。

###### SQL注入

漏洞特征：存在SQL注入语句

常见的SQL注入语句有：

+ 通过报错注入、布尔盲注、时间盲注判断是否存在注入：
  + 字符型
    + 参数后加单引号，报错：sql1.php?name=admin'
    + 参数后加' and '1'='2和' and '1'='2，访问正常：sql1.php?name=admin' and '1'='1       /sql1.php?name=admin' and '1'='2
    + 参数后加' and sleep(3)  --，是否延迟3秒打开：sql1.php?name=admin' and/or sleep(3)--
  + 数字型
    + 参数后加单引号，报错:sql2.php?id=1'
    + 参数后加and 1=1和and 1=2，访问正常：sql2.php?id=1 and 1=1/sql2.php?id=1 and 1=2
    + 参数后加and sleep(5)，是否延迟3秒打开：sql2.php?id=1 and sleep(5)
+ 通过各种注入语句进行SQL注入攻击：
  + 联合查询注入
    + union select
    + order by
  + 报错注入(常见报错注入函数)
    + floor()
    + extractvalue()
    + updatexml()
    + geometrycollection()
    + multipoint()
    + polygon()
    + multipolygon()
    + linestring()
    + multilinestring()
    + exp()
  + 常见数据库类型判断
    + ACCESS
        and (select count (*) from sysobjects)>0返回异常
        and (select count (*) from msysobjects)>0返回异常
    + SQLSERVER
        and (select count (*) from sysobjects)>0返回正常
        and (select count (*) from msysobjects)>0返回异常
        and left(version(),1)=5%23参数5也可能是4
    + MYSQL
        id=2 and version()>0返回正常
        id=2 and length(user())>0返回正常
        id=2 CHAR(97, 110, 100, 32, 49, 61, 49)返回正常
    + Oracle
        and length (select user from dual)>0返回正常

上述内容并非全部，只是举出来的部分常见例子。

###### XSS跨站脚本攻击

漏洞特征：明显的js恶意执行代码

常见的XSS跨站脚本攻击中存在的一些代码：

+ 标签
  + \<script>
  + \<body>
  + \<input>
  + \<img>
  + \<a>
  + \<svg>
  + \<BGSOUND>
  + \<LINK>
  + \<META>
  + \<TABLE>
  + \<DIV>
  + \<IFRAME>
  + \<FRAMESET>
  + \<STYLE>
  + \<OBJECT>
  + ......
+ 常用触发事件
  + oninput
  + onload
  + oncut
  + onclick
  + onerror
  + onmouseover
  + onfocus
  + onblur
  + poster
  + onscroll
  + ......
+ 常用恶意代码
  + prompt
  + confirm
  + alert
  + javascript
  + eval
  + expression
  + window.location

  + ......

这里要注意一点：**由于apache日志的特性，如果是通过Post请求，则无法准确判断出是否存在XSS跨站脚本攻击**

###### 恶意文件上传

通常存在于upload、file等出现类似字样的文件，均可能存在恶意文件上传，具体还需结合日志进行判断，一般是判断后续是否有出现Webshell等一些可以的web操作，可通过查看下图，发现在file.php页面的前后日志中，有存在一个带着日期的php页面，很可能就是利用file.php上传的文件，服务器自动生成名字，因此判断此处可能存在恶意文件上传。

![20210902173206](https://gitee.com/ye_xi_bai/blogimage/raw/master/blogimages20210902173206.png)

一般地，如果Post请求的数据未被显示出来，则需要我们通过访问的链接以及上下文的访问详情确认此处是否存在恶意文件上传

###### 一句话木马（Webshell）

一般名字可疑的文件，如带日期字样的页面(.php、.asp、.aspx、.ash、.jsp等)、一串随机值的页面等，并且是通过Post请求，同时会返回一定的数据，此时可判断可能存在一句话木马、webshell等恶意文件，有些日志可能还有post请求参数，可结合参数，更准确地判断出是否存在一句话木马、webshell等恶意文件。

##### 访问频率分析

访问频率分析：不难理解，就是通过查看攻击者访问的频率来判断攻击者使用的是哪一种攻击。
**这一特点分析法也常常用在流量分析中。**

常见的类型有有以下：SQL盲注、敏感目录爆破、账号爆破、Web扫描。

+ SQL盲注
    一般访问比较有规律，基本都包含SQL语句，并且大体都相似，有个别字符不同
+ 敏感目录爆破
    一般会有大量的探测目录，一般以Head方法为主进行探测
+ 账号爆破
    通常都是对一个登录页面进行大量post请求，并且返回值基本相似
+ Web扫描
    一般来说，访问的目标比较离散，并且来源地址相对固定，同时访问的结果大多数也都是失败的，并且在参数中有比较明显的扫描器特征字段
    常见扫描器在url上的特征：
  + AWVS 10.5或11
    acunetix-wvs-test-for-some-inexistent-file
    by_wvs
    acunetix_wvs_security_test
    acunetix
    acunetix_wvs
    acunetix_test
    wvs_test
  + Netsparker
    netsparker
    Netsparker
    ns: netsparker
  + Appscan
    Appscan
  + Webinspect
    HP404
  + Rsas
    nsfocus
  + Nessus
    nessus
    Nessus
  + Sqlmap
    sqlmap

### 系统日志分析

#### Linux操作系统

Linux的系统日志一般存放在/var/log目录下，常见的日志（列举部分）有以下：

![20210902174826](https://gitee.com/ye_xi_bai/blogimage/raw/master/blogimages20210902174826.png)

+ /var/log/messages

    用于记录系统相关信息，如执行程序、系统错误、启动信息等，一般我们会使用message进行查看可疑程序执行的可疑操作，系统在执行程序时出现错误等，

    ![20210902183453](https://gitee.com/ye_xi_bai/blogimage/raw/master/blogimages20210902183453.png)

    对应的格式：

    日期 时间 主机 执行的程序[进程ID]：具体信息

+ /var/log/boot.log

    用于记录系统启动信息的日志，一般用于查看在系统启动时所有相关信息，具体如下：

    ![20210902183424](https://gitee.com/ye_xi_bai/blogimage/raw/master/blogimages20210902183424.png)

    不难发现，该日志记录的是系统启动时的启动信息，比如开启了哪些服务、做了什么操作都能一目了然。

+ /var/log/lastlog

    用于记录了用户近期登陆情况，直接查看lastlog，可能信息不太明显，但是也可以使用lastlog命令进行查看，会比较详细：

    ![20210902183536](https://gitee.com/ye_xi_bai/blogimage/raw/master/blogimages20210902183536.png)

+ /var/log/cron

    Linux的计划任务相关信息的日志，我们也会使用它来找寻攻击者可能会写入的一些恶意计划任务，其中可能会带有一些恶意软件等相关信息。

+ /var/log/secure

    此日志是linux 的安全日志，被用于记录用户工作的安全相关问题以及登陆认证情况，

#### Windows操作系统

Windows日志一般在事件查看器中可以进行查看，通常分为五个：应用程序、安全、Setup、系统、转发事件。并且这五个中又以应用程序、安全以及系统日志较为常见。

+ 应用程序日志

    此日志顾名思义便是记录了应用程序的运行情况，包括运行出错、甚至于出错的原因，如：

    ![20210902184204](https://gitee.com/ye_xi_bai/blogimage/raw/master/blogimages20210902184204.png)

    它指出了错误应用程序名称、版本、具体时间错，并且还指出了错误的模块以及异常代码，故而，我们可以通过这些信息，进行对应的故障排查，具体如何排查可通过适当的资料等进行，这里不做过多说明，需要提的是它在Windows中保存在Application.evtx文件中，如果在CTF比赛中看到这个文件，那么可能就是让你进行应用程序日志分析了。

+ 安全日志

    此处的安全日志和Linux的安全日志相似，但是它只记录用户登陆情况、用户访问时间以及访问是否授权等，通过它我们可以轻松的发现是否存在爆破风险（一般在短时间内发现大量登陆失败，即可认为该账号被爆破了）。

    ![20210902184310](https://gitee.com/ye_xi_bai/blogimage/raw/master/blogimages20210902184310.png)

+ 系统日志

    系统日志则是记录了操作系统安装的应用程序软件相关的事件。它包括了错误、警告及任何应用程序需要报告的信息等。

    相比于Linux 的日志，Windows对于系统日志的记录，也是挺详细的，我们可以通过它来进行一些分析判断，它存在于System.evtx文件中。

    它详细到可以发现使用者信息、登陆类型、登陆失败的账户、失败信息、进程信息、内网信息以及详细身份验证信息等，十分方便。它在操作系统中保存在Security.evtx文件下，我们也可以通过双击它打开安全日志。
