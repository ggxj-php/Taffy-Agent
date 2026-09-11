

## tools/cmd.md

author: StudyingFather, ayalhw, qinyihao, CoderOJ, mcendu, Libaray

虽然图形界面能做的事情越来越多，但有很多高阶操作仍然需要使用命令行来解决．

本页面将简要介绍命令行的一些使用方法．

## 基础

Windows 自带的命令行界面有两个．「命令提示符」（`cmd`）是其中较为古老的一个，功能也相对简单．PowerShell 是较新的一个命令行界面，自带的功能丰富，但相对臃肿．两个界面都可以在开始菜单中找到．

类 Unix 系统（包含 macOS 和 Linux，以下称为 Unix）分为有图形界面和无图形界面两种情况．如果系统有图形界面（如使用 macOS 或者在 Linux 下安装了 GNOME、KDE 等图形界面），则命令行一般可以通过名为「终端」（Terminal 或 Console）的程序打开．没有图形界面的系统会在启动完成后自动进入命令行．

Windows 下的命令行长这样：

```doscon
C:\Users\chtholly>
```

在命令行上输入的指令会显示在 `>` 以后．

```doscon
C:\Users\chtholly>echo "Hello World!"
```

Unix 下的命令行长这样（以 Debian/Ubuntu 为例，其它系统的命令行大体类似）：

```console
chtholly@seniorious:~$
```

在命令行上输入的指令会显示在 `$` 以后．

```console
chtholly@seniorious:~$ echo "Hello World!"
```

如果在 Unix 下使用 `root` 登录命令行，那么 `$` 会被替换成 `#`：

```console
root@seniorious:~# apt-get install gcc
```

命令行的 `>`，`$` 或 `#` 之前会显示一个路径，这个路径就是工作目录（working directory），或者当前目录．在 Unix 下当前目录有时会显示成类似 `~/folder` 的形式，最开头的 `~` 就是当前登录的用户的主目录．用户 `chtholly` 的主目录在不同系统下的位置是不同的；在 Linux 下，其主目录位于 `/home/chtholly`，而在 macOS 下，其主目录位于 `/Users/chtholly`．

## 语法和常用命令[^1]

### 文件系统相关

先介绍文件系统里描述位置的两种方式，相对路径和绝对路径．

-   相对路径：用相对当前路径的位置关系来描述位置．例如当前路径为 `~/folder`，则 `./a.cpp` 实际上指的就是 `~/folder/a.cpp` 这个文件．**随着当前路径的变化，相对路径描述的位置也可能发生改变**．

-   绝对路径：用完整的路径来描述位置．例如 `~/folder/a.cpp` 就是一个绝对路径的例子．**绝对路径描述的位置不随当前路径的变化而改变**．

    Windows/Unix 用 `.` 代表当前目录，`..` 代表当前目录的父目录．特别地，在 Unix 下，用 `~` 表示用户主目录（注意 `~` 由 shell 展开，因此在其他地方可能不可用）．

在 Unix 下，使用 `pwd` 命令可以打印当前的目录（在 Windows PowerShell 中也有此命令，但在 Windows 命令提示符中无此命令，详情见下面的提示）．在 Windows/Unix 中，`cd <目录>` 命令都可以切换当前的目录．例如，`cd folder` 会切换到当前目录的 `folder` 子目录；`cd ..` 会切换到当前目录的父目录．

???+ note "对 Windows 命令提示符的特别提示"
    在 Windows 命令提示符中并没有 `pwd` 命令，但可以用没有任何参数的 `cd` 命令近似代替．
    
    同时，需要注意的是，在 Windows 命令提示符下使用 `cd` 命令切换目录，如果 **切换到的目录的盘符与当前目录的盘符不同**，则当前目录不会改变．你可以再敲一遍切换到的路径的盘符，也可以使用 `cd /d <目录>` 命令来同时切换盘符．两种方法对应的命令行界面如下：
    
    ```doscon
    C:\Users\Libaray>cd D:\Codes
    C:\Users\Libaray>D:
    D:\Codes>
    ```
    
    ```doscon
    C:\Users\Libaray>cd /d D:\Codes
    D:\Codes>
    ```

在 Windows 下，使用 `dir` 命令可以列出当前目录的文件列表．在 Unix 下，列出文件列表的命令是 `ls`．特别的，在 PowerShell 下，可以使用与 Unix 相同的 `ls` 命令．

在 Windows 下，使用 `md <目录>` 或者 `mkdir <目录>` 命令创建一个新目录，使用 `rd <目录>` 或者 `rmdir <目录>` 命令删除一个目录．在 Unix 下，这两个命令分别是 `mkdir` 和 `rmdir`．需要注意的是，**使用 `rd` 或是 `rmdir` 删除一个目录前，这个目录必须是空的**．如果想要删除非空目录（和该目录下的所有文件）的话，Unix 下可以执行 `rm -r <目录>` 命令，Windows 下可以执行 `rd /s <目录>` 命令．

### 重定向机制

> 我编译了一个程序，它从标准输入读入，并输出到标准输出．然而输入文件和输出文件都很大，这时候能不能想办法把输入重定向到指定的输入文件，输出重定向到指定的输出文件呢？

使用如下命令即可实现．

```console
$ command < input > output
```

例如，`./prog < 1.in > 1.out` 这个命令就将让 `prog` 这个程序从当前目录下的 `1.in` 中读入数据，并将程序输出覆盖写入到 `1.out`．

???+ warning "Warning"
    `1.out` 原本的内容会被覆盖，如果想要在原输出文件末尾追加写入，请使用 `>>`，即 `./prog >> 1.out` 的方式做输出重定向

注意，PowerShell 只支持输出重定向，不支持输入重定向．

事实上，大多数 OJ 都采用了这样的重定向机制．选手提交的程序采用标准输入输出，通过重定向机制，就可以让选手的程序从给定的输入文件读入数据，输出到指定的输出文件，再进行文件比较就可以评测了．

### 执行程序

对于一个可执行程序或是批处理脚本，只需在命令行里直接输入它的文件名即可执行它．

当然，执行一个文件时，命令行并不会把所有目录下的文件都找一遍．环境变量 `PATH` 描述了命令行搜索路径的范围，命令行会在 `PATH` 中的路径寻找目标文件．

对于 Windows 系统，**当前目录也在命令行的默认搜索范围内**．例如 Windows 系统中，输入 `hello` 命令就可以执行当前目录下的 `hello.exe`．但是在 PowerShell 中，PowerShell 默认不会从当前目录寻找可执行文件（这与在 Unix 的行为一致），因而在 PowerShell 中需要使用相对路径或绝对路径调用当前目录下的可执行文件，例如 `.\hello.exe`，否则，你将看到以下报错：

```ps1con
PS> hello
hello: The term 'hello' is not recognized as a name of a cmdlet,
function, script file, or executable program.
Check the spelling of the name, or if a path was included, verify that
the path is correct and try again.

Suggestion [3,General]: The command hello was not found, but does exist
in the current location. PowerShell does not load commands from the
current location by default. If you trust this command, instead type:
".\hello". See "get-help about_Command_Precedence" for more details.
```

在 Unix 系统中，**当前目录并不在命令行的默认搜索范围内**，所以执行当前目录下的 `hello` 程序的命令就变成了 `./hello`:

```console
$ hello
hello: command not found
$ ./hello
Hello World!
```

### 总结

上面介绍的用法只是命令行命令的一小部分，还有很多命令没有涉及到．在命令行里输入帮助命令 `help`，可以查询所有基本命令以及它们的用途．

下面给出 Windows 系统和 Unix 系统的命令对照表，以供参考．

| 分类   | Windows 系统 | Unix 系统 |
| ---- | ---------- | ------- |
| 文件列表 | `dir`      | `ls`    |
| 切换目录 | `cd`       | `cd`    |
| 建立目录 | `md`       | `mkdir` |
| 删除目录 | `rd`       | `rmdir` |
| 比较文件 | `fc`       | `diff`  |
| 复制文件 | `copy`     | `cp`    |
| 移动文件 | `move`     | `mv`    |
| 文件改名 | `ren`      | `mv`    |
| 删除文件 | `del`      | `rm`    |

## 使用命令行编译/调试

参见：[命令行编译与调试](compile-debug.md)．

## 命令行使用技巧

### 自动补全

补全是 Shell 提供的基本功能之一，主要用于减少命令行使用中的输入量和 typo 概率．

一般情况下，使用补全的快捷键一般是<kbd>Tab</kbd>，按下后 Shell 会根据已输入的字符补全信息．

不同的 Shell 提供了能力不尽相同的补全能力．

以下是常见 Shell 的补全能力[^autocomplete]：

| Shell               | 补全能力（补全范围）                                               |
| ------------------- | -------------------------------------------------------- |
| cmd（Windows 的传统控制台） | 文件路径                                                     |
| PowerShell          | 文件路径、PATH 中的命令名、内建命令名、函数名、命令参数，支持模糊匹配，自动纠错               |
| Bash                | 文件路径、PATH 中的命令名、内建命令名、函数名、命令参数                           |
| Zsh                 | 文件路径、PATH 中的命令名、内建命令名、函数名、命令参数，支持模糊匹配，自动纠错和建议            |
| Fish                | 文件路径、PATH 中的命令名、内建命令名、函数名、命令参数，支持模糊匹配，补全时可显示参数功能，自动纠错和建议 |

???+ note "Note"
    PowerShell 的部分功能需要 PSReadline Module 载入或者位于 PowerShell ISE 中．  
    Bash 的补全功能一般需要一个名为 `bash-completions` 的包才能获得完整功能，部分软件的补全文件由软件包自带．  
    Zsh 完整的补全功能需要配合用户预定义的文件（一般随 Zsh 包或对应软件包安装）．  
    Fish 在默认配置下提供良好完整的补全功能，但仍有部分官方未覆盖到的软件的补全文件由软件自行提供．

### 帮助文档

一般来说，命令行下的程序都附有「帮助」，Windows 下一般使用 `command /?` 或者 `command -?` 获取，Unix-like（例如 Linux）上一般使用 `command --help` 或者 `command -h` 获取（但是 BSD 下的「帮助」往往过分简略而难以使用）．

此外，在 Unix-like 系统上，还有可通过 `man command` 获取的「手册」(manual)，相比「帮助」一般更为详细．

### built-in time 和 GNU time

测试程序运行时间时，我们通常可以使用 `time` 命令．

但是这个命令实际上在系统中有两个对应的命令：一个是部分 Shell（例如 Bash）内建的命令，一个是 GNU time（是一个单独的软件）．这两个之间存在一些差异．

一般在 Bash 中直接使用 `time` 调用的是 Bash 内建的版本，我们可以使用 `TIMEFORMAT` 环境变量控制其输出格式，例如将其设为 `%3lR` 即可输出三位精度的实际运行时间，`%3lU` 即可输出三位精度的用户空间运行时间．[^bash-time-format]

如果想要调用 GNU 版本的 time，则需使用 `\time` 或者 `/usr/bin/time` 调用，但是它的输出格式并不易读，我们可以附加 `-p` 参数（即为 `\time -p`）来获得易读的输出．

## 管道

假设我们现在有两个程序 A 和 B，都用标准输入输出，如何让 A 的输出重定向到 B 的输入？

我们可以使用上文中提到的重定向的方式，先把 A 的输出重定向到一个临时文件，在把 B 的输入重定向到这个临时文件上．

但这个方法很低效，不仅需要创建新的文件，磁盘 IO 的操作也可能成为瓶颈，而且两个程序不能同时运行，必须等 A 跑完了才能开始跑 B．有没有更好的方法？

有，那就是 **管道**，使用起来也非常简单，如下操作即可：

```console
$ A | B
```

这会在内存创建一个管道，然后两个程序被同时启动．程序 A 每次要输出被重定向到这个管道中，而这个管道本身不会存储数据（其实有一个很小的缓冲区）．在 B 读取之前，A 的输出操作会被阻塞，等到 B 把数据读入以后，A 的输出才能继续进行．这样优美地解决了上述的问题，没有磁盘 IO 操作，两份代码同时运行，也没有额外消耗很多的内存储存中间结果．

### 命名管道

有时候我们不只是要把一个程序的输出重定向到另一个的输入．比如在做 IO 交互题的时候，经常需要将 A 的输出重定向到 B 的输入，B 的输出重定向到 A 的输出，这个时候用上文提到的普通管道就无能为力了．而重定向到文件，有无法让两个程序同时运行．这个时候就需要一个长得像文件的管道——命名管道．

在 Unix 系统中，可以使用如下命令创建命名管道（以命名为 `my_pipe` 举例）：

```console
$ mkfifo my_pipe
```

这个时候使用 `ls` 命令列出当前目录下的文件，会发现多了一个 `my_pipe|` 的文件．这就创建了一个命名管道，文件名后的 `|` 代表这是一个管道文件．然后就可以像文件的重定向一样向这个管道中读写了．

通过命名管道，我们可以通过这样的方式让两个程序交互：

```console
$ mkfifo input output
$ ./checker > input < output # 这里一定要把 > input 写在前面，不然 shell 会先打开 output 管道，而这个管道现在并没有东西，会阻塞 checker 的运行．
$ ./my_code < input > output
```

使用完后，可以像普通文件一样用 `rm` 命令删除命名管道．

## 参考资料与注释

[^1]: 刘汝佳《算法竞赛入门经典（第 2 版）》附录 A 开发环境与方法

[^autocomplete]: [Comparison\_of\_command\_shells#Interactive\_features](https://en.wikipedia.org/wiki/Comparison_of_command_shells#Interactive_features)

[^bash-time-format]: <https://unix.stackexchange.com/a/70655>


## tools/compile-debug.md

author: CoelacanthusHex, qinyihao, StudyingFather, ksyx, NachtgeistW, CoderOJ, Enter-tainer, mcendu, Tiphereth-A, ayalhw, CCXXXI, Early0v0, HeRaNO, ouuan, swiftqwq, Xeonacid, xiaofu-15191

阅读本节之前，请先安装 GCC 和 gdb，具体方法参见 [编译器](compiler.md) 一文．

## 命令行使用 g++ 编译 cpp 文件

### 手动编译

在命令行下输入 `g++ a.cpp` 就可以编译 `a.cpp` 这个文件了（Windows 系统需提前把编译器所在目录加入到 `PATH` 中）．

编译过程中可以加入一些编译选项：

-   `-o <文件名>`：指定编译器输出可执行文件的文件名．
-   `-g`：在编译时添加调试信息（使用 gdb 调试时需要）．
-   `-Wall`：显示所有编译警告信息．
-   `-O1`，`-O2`，`-O3`，`-Ofast`：对编译的程序进行优化，越往后的优化级别表示采用的优化手段越多（开启优化会影响使用 gdb 调试）．
-   `-DDEBUG`：在编译时定义 `DEBUG` 符号（符号可以随意更换，例如 `-DONLINE_JUDGE` 定义了 `ONLINE_JUDGE` 符号）．
-   `-UDEBUG`：在编译时取消定义 `DEBUG` 符号．
-   `-lm`，`-lgmp`: 链接某个库（此处是 math 和 gmp，具体使用的名字需查阅库文档，但一般与库名相同）．

???+ note "Note"
    在 Unix 下，如使用了标准 C 库里的 math 库（`math.h`），则需在编译时添加 `-lm` 参数．[^have-to-link-libm-in-gcc]

???+ note "如何开大栈空间？"
    在 Windows 下，可以使用编译选项 `-Wl,--stack=536870912` 将栈空间开大到 512 MB，其中等号后面的数字为 **字节数**．
    
    在 Unix 下，使用 `ulimit -s [num]` 将 **当前终端** 的栈空间调为 `[num]` **KiB**．

### 使用 GNU Make 的内置规则[^gnu-make-built-in-rules]

对于名为 `qwq.c/cpp` 的 C/C++ 程序源代码，可以使用 `make qwq` 自动编译成对应名为 `qwq` 的程序．

如需添加额外的编译选项，可使用 `export CFLAGS="xxx"`（C 程序）或 `export CXXFLAGS="xxx"`（C++ 程序）指定．如需添加额外的预编译选项，可使用 `export CPPFLAGS="xxx"` 指定．上述设置方法也可以写做类似 `CFLAGS="xxx" CPPFLAGS="xxx" make qwq` 来指定单次命令执行中使用的环境变量．

### Sanitizers

#### 介绍

sanitizers 是一种集成于编译器中，用于调试 C/C++ 代码的工具，通过在编译过程中插入检查代码来检查代码运行时出现的内存访问越界、未定义行为等错误．

它分为以下几种：

-   AddressSanitizer[^address-sanitizer]：检测对堆、栈、全局变量的越界访问，无效的释放内存、内存泄漏（实验性）．
-   ThreadSanitizer[^thread-sanitizer]：检测多线程的数据竞争．
-   MemorySanitizer[^memory-sanitizer]：检测对未初始化内存的读取．
-   UndefinedBehaviorSanitizer[^ub-san]：检测未定义行为．

#### 使用方式

最新版本的 clang++、g++ 以及 MSVC（部分支持）均已内置 sanitizers，但功能和使用方法有所不同，这里以 clang++ 为例，它的使用方法如下：

```console
$ clang++ -fsanitize=<name> test.cc
```

其中 `<name>` 即为要启用的功能（一个 sanitizer 可理解为一些功能的集合），例如：

```console
$ clang++ -fsanitize=memory test.cc # 启用 MemorySanitizer
$ clang++ -fsanitize=signed-integer-overflow test.cc # 启用有符号整型溢出检测
```

之后直接像平常一样运行可执行文件即可，如果 sanitizer 检测到错误，则会输出到 `stderr` 流，例如：

```console
$ ./a.out
test.cc:3:5: runtime error: signed integer overflow: 2147483647 + 1 cannot be represented in type 'int'
```

???+ warning "Warning"
    Windows 下的 g++ 不支持 sanitizers，需要使用 [修改过后的 MinGW64](https://github.com/ssbssa/gcc/releases) 或使用其它编译器．
    
    MSVC 从 16.0 截至版本 17.14 仅支持 AddressSanitizer．

#### 时间/内存代价

显而易见，这些调试工具会严重拖慢代码的运行时间和增大所用内存，以下为使用它们的时间/内存代价：

| 名称                         | 所增大内存倍数 | 所增大时间倍数 |
| :------------------------- | :------ | :------ |
| AddressSanitizer           | N/A     | 2       |
| ThreadSanitizer            | 5\~15   | 5\~10   |
| MemorySanitizer            | N/A     | 3       |
| UndefinedBehaviorSanitizer | N/A     | N/A     |

## 命令行使用 gdb 调试

```console
$ g++ a.cpp -o a -g
$ gdb ./a
GNU gdb (Ubuntu 12.1-0ubuntu1~22.04.2) 12.1
Copyright (C) 2022 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
Type "show copying" and "show warranty" for details.
This GDB was configured as "x86_64-linux-gnu".
Type "show configuration" for configuration details.
For bug reporting instructions, please see:
<https://www.gnu.org/software/gdb/bugs/>.
Find the GDB manual and other documentation resources online at:
    <http://www.gnu.org/software/gdb/documentation/>.
--Type <RET> for more, q to quit, c to continue without paging--
```

按下 `c` 继续．接着提示 `Reading symbols from [filename]...`，出现 `(gdb)` 字样时，就可以输入命令调试了．

以下是按照分类列表的常用命令：

### gdb 基础命令

| 命令                | 描述                    |
| ----------------- | --------------------- |
| `help`            | 显示帮助信息                |
| `quit`            | 退出 gdb                |
| `file [filename]` | 加载要调试的程序 `[filename]` |

### 运行控制命令

| 命令                   | 描述                                         |
| -------------------- | ------------------------------------------ |
| `run`                | 运行程序，直到遇到断点或程序结束                           |
| `continue`           | 继续运行，直到遇到断点或程序结束                           |
| `next`               | 单步执行，遇到函数调用则进入函数                           |
| `step`               | 单步执行，遇到函数调用则进入函数                           |
| `finish`             | 运行到当前函数返回为止，然后停下来等待命令                      |
| `until [num]`        | 运行到指定行号 `[num]` 为止，然后停下来等待命令               |
| `break [num]`        | 在第 `[num]` 行设置断点，程序运行到该行时停下来等待命令           |
| `condition [id] [p]` | 设置编号为 `[id]` 的断点条件，只有满足表达式 `[p]` 条件时，断点被启用 |
| `ignore [id] [num]`  | 忽略前 `[num]` 次触发断点                          |
| `delete [id]`        | 删除指定编号的断点                                  |
| `disable [id]`       | 禁用指定编号的断点                                  |
| `enable [id]`        | 启用指定编号的断点                                  |
| `list`               | 列出源代码，接着上次的位置往下列，每次列 10 行                  |
| `list [num]`         | 列出以第 `[num]` 行为中间行的源代码                     |
| `list [func-name]`   | 列出某个函数为中间行的源代码                             |
| `call [function]`    | 调用函数，并打印返回值                                |

`break [num]` 会输出断点的编号，也可以使用 `break [func-name]` 设置函数断点；

你也可以使用 `break [num] [p]` 在设置断点时实现与 `condition [id] [p]` 接近的效果．

### 栈帧命令

| 命令          | 描述          |
| ----------- | ----------- |
| `info args` | 查看函数的参数     |
| `backtrace` | 查看各级函数调用及参数 |
| `frame`     | 选择栈帧        |
| `up`        | 向上移动一级栈帧    |
| `down`      | 向下移动一级栈帧    |

### 变量命令

| 命令                 | 描述                                 |
| ------------------ | ---------------------------------- |
| `print [p]`        | 打印表达式 `[p]` 的值，通过表达式可以修改变量的值       |
| `display [p]`      | 每次暂停时打印表达式 `[p]` 的值，但不进入函数         |
| `watch [var]`      | 监视变量 `[var]` 的值，当变量被写入时，会自动打印出来并暂停 |
| `rwatch [var]`     | 监视变量 `[var]` 的值，当变量被读取时，会自动打印出来    |
| `awatch [var]`     | 当变量 `[var]` 被修改或写入时，会自动打印出来并暂停     |
| `set [assignment]` | 执行赋值语句                             |

`display` 和 `print` 指令都支持控制输出格式，其方法是在命令后紧跟 `/` 与格式字符，例如 `print/display [var]`（按照十进制打印变量 `[var]` 的值），支持的格式字符有：

| 格式字符 | 对应格式          |
| ---- | ------------- |
| `d`  | 按十进制格式显示变量    |
| `x`  | 按十六进制格式显示变量   |
| `a`  | 按十六进制格式显示变量   |
| `t`  | 按二进制格式显示变量    |
| `c`  | 按字符格式显示变量     |
| `f`  | 按浮点数格式显示变量    |
| `u`  | 按十进制格式显示无符号整型 |
| `o`  | 按八进制格式显示变量    |

### 信息命令

| 命令                 | 描述          |
| ------------------ | ----------- |
| `info breakpoints` | 列出所有断点      |
| `info locals`      | 列出当前栈帧的局部变量 |
| `info args`        | 列出当前栈帧的函数参数 |
| `info threads`     | 列出所有线程      |
| `info program`     | 显示程序的当前状态   |
| `info registers`   | 显示当前寄存器的值   |
| `info frame`       | 显示当前栈帧的信息   |

### 其他命令

| 命令                            | 描述                                    |
| ----------------------------- | ------------------------------------- |
| `enable pretty-printer`       | 启用 pretty-printer，可以以人类可读的方式打印 STL 容器 |
| `checkpoint`[^checkpoint]     | 创建检查点，可以回滚到检查点                        |
| `restart [num]`[^checkpoint]  | 回滚到第 `[num]` 个检查点                     |
| `save breakpoints [filename]` | 保存断点到文件                               |
| `source [filename]`           | 导入断点文件                                |

???+ tip "提示"
    gdb 调试时的命令大多都可以被简写为可以唯一确定的字母缩写，例如 `breakpoint` 简写为 `b`，`step` 简写为 `s`，`info args` 简写为 `i ar`．详见 `help` 命令．

## 参考资料与注释

[^have-to-link-libm-in-gcc]: [Why do you have to link the math library in C?](https://stackoverflow.com/questions/1033898/why-do-you-have-to-link-the-math-library-in-c)

[^address-sanitizer]: <https://clang.llvm.org/docs/AddressSanitizer.html>

[^thread-sanitizer]: <https://clang.llvm.org/docs/ThreadSanitizer.html>

[^memory-sanitizer]: <https://clang.llvm.org/docs/MemorySanitizer.html>

[^ub-san]: <https://clang.llvm.org/docs/UndefinedBehaviorSanitizer.html>

[^gnu-make-built-in-rules]: [Catalogue of Built-In Rules](https://www.gnu.org/software/make/manual/html_node/Catalogue-of-Rules.html)

[^checkpoint]: 与检查点相关的指令仅适用于 GNU/Linux 平台．详见 [GDB 官方手册](https://sourceware.org/gdb/current/onlinedocs/gdb#Checkpoint_002fRestart)．


## tools/compiler.md

本页面主要介绍了各系统下各类编译器/解释器的安装步骤．

## GCC

### Windows

#### 手动下载安装

访问 [MinGW-w64](https://www.mingw-w64.org/downloads) 的下载页面，有多个构建版本．方便起见，我们使用由 WinLibs 提供的构建版本．

首先前往 [WinLibs](https://winlibs.com) 下载最新的安装包，选择合适的版本，本文选择了 GCC 12.3.0 + LLVM/Clang/LLD/LLDB 16.0.4 + MinGW-w64 11.0.0 (UCRT)：

默认会附带安装 LLVM Clang，如果不想安装，你也可以选择右边的 without LLVM/Clang/LLD/LLDB．

![](./images/compiler1.png)

下载好后将其解压到电脑中的某个位置，教程中将其解压到了 C 盘的根目录．目录名中最好不要包含非英文字符和空格，否则可能会在后期导致一些问题．

![](./images/compiler2.png)

接下来我们需要将编译器的可执行文件目录添加到系统环境变量中，这样在编译时就不需要指定编译器的路径了，方便使用．上方我们将 MinGW 解压到了 `C:\mingw64` 目录中，那么可执行文件所在的目录就是 `C:\mingw64\bin`．

按下 Windows 徽标 + R 组合键，输入 `rundll32.exe sysdm.cpl,EditEnvironmentVariables`，打开系统环境变量设置窗口，并在「系统变量」一节中选中名为「Path」的变量，然后点击「编辑」按钮：

![](./images/compiler3.png)

在编辑窗口中点击右侧的「新建」按钮，为「Path」变量新建一个条目，并填入上文中记录下的可执行文件所在的目录（教程中为 `C:\mingw64\bin`）．

![](./images/compiler4.png)

??? note "对部分老版本系统的提示"
    部分老版本系统只能手动修改变量的文本值，那么需要在变量的值的末尾插入一个 **半角分号**，再将可执行文件所在的目录粘贴到这个半角分号的后面，如图所示：
    
    ![](./images/compiler5.png)

完成后一路点击「确定」按钮退出即可．

接下来打开终端，输入 `g++ --version` 并按下回车，如果出现如图所示的提示则代表安装成功．

![](./images/compiler6.png)

#### Scoop 安装

打开 PowerShell，运行以下脚本：

```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
irm get.scoop.sh | iex
scoop install mingw-winlibs
```

### Linux

#### Debian/Ubuntu

首先先更新软件包列表：

```bash
sudo apt update
```

再使用命令直接安装即可：

```bash
sudo apt install g++
```

#### Arch Linux

使用命令直接安装即可：

```bash
sudo pacman -Syu gcc
```

#### openSUSE

使用命令直接安装即可：

```bash
sudo zypper in gcc-c++
```

### macOS

首先更新包管理器：

```bash
brew upgrade
brew update
```

再使用命令直接安装即可：

```bash
brew install gcc
```

## JDK

JDK 的发行版有很多，以下介绍两种：

-   OpenJDK 中的 [Eclipse Temurin](https://adoptium.net/zh-cn/)[^temurin]：参见 [Install Eclipse Temurin™ | Adoptium](https://adoptium.net/zh-CN/installation/)．
-   Oracle JDK：可参见 [JDK Installation Guide（JDK 17）](https://docs.oracle.com/en/java/javase/17/install/overview-jdk-installation.html)．

## Python 3

Python 的实现也有很多[^pythonimpl]，以 CPython 3 为例，参见 [Download Python | Python.org](https://www.python.org/downloads/)．

## LLVM

### Windows

??? note "LLVM 在 Windows 上的坑"
    由于 LLVM 在 Windows 上缺失标准库，所以你仍需安装 MSVC 或 GCC．

#### 直接安装

访问 [LLVM](https://github.com/llvm/llvm-project/releases/latest) 的下载页面，选择 LLVM-\*-win64.exe 下载．

如果你的网络质量不佳，你也可以选择访问 [清华大学开源软件镜像站](https://mirrors.tuna.tsinghua.edu.cn/github-release/llvm/llvm-project/LatestRelease/) 进行下载．

打开 .exe 文件，安装时勾选 Add LLVM to system PATH for current user，随后一直点击下一步即可安装完成．

打开终端，输入 `clang++ --version` 并回车，出现

```text
clang version 15.0.1
Target: x86_64-pc-windows-msvc
Thread model: posix
InstalledDir: <omitted>
```

类似物即代表成功．

#### Scoop 安装

打开 PowerShell，运行以下脚本：

```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
irm get.scoop.sh | iex
scoop install llvm
```

### Linux

#### openSUSE

使用命令直接安装即可：

```bash
sudo zypper in llvm clang
```

## MSVC (Visual Studio)

访问 [下载 Visual Studio](https://visualstudio.microsoft.com/zh-hans/downloads/) 页面，找到「下载」一节中的「社区」部分，点击「免费下载」．下载完成后打开安装器选择「Community 2022 安装」．在随后弹出来的窗口中仅选择「使用 C++ 的桌面开发」，然后单击安装．

如果你不想安装完整的 Visual Studio，可以滚动到下方「所有下载」一节，在「用于 Visual Studio 的工具」中找到「Visual Studio 生成工具」，点击后方的「下载」．下载完成后打开安装器，按照提示步骤选择「使用 C++ 的桌面开发」后安装即可．也可以使用 [PortableBuildTools](https://github.com/Data-Oriented-House/PortableBuildTools) 工具以仅安装 MSVC 编译器．

[^temurin]: [Eclipse Temurin](https://adoptium.net/) 即为原 [AdoptOpenJDK](https://adoptopenjdk.net/)，后者已于 2021 年 7 月移交至 [Eclipse 基金会](https://www.eclipse.org/org/foundation/)．具体可见 [本声明](https://blog.adoptopenjdk.net/2021/03/transition-to-eclipse-an-update/)．

[^pythonimpl]: [Alternative Python Implementations | Python.org](https://www.python.org/download/alternatives/)


## tools/editor/atom.md

author: ouuan, ChungZH, partychicken, Xeonacid, Find-NICK

Atom，GitHub 家的编辑器．

## 简介

Atom 是一个免费、开源、跨平台的文本编辑器，由 GitHub 开发．它是用 JavaScript 编写的，并且采用 Electron 架构．它的一个较大缺点就是性能差．

???+ warning "Warning"
    在 2022 年 6 月 8 日，[Github 宣布将放弃 Atom 编辑器](https://github.blog/2022-06-08-sunsetting-atom/)，并于 2022 年 12 月 15 日对 Atom 编辑器存档．
    如果你仍然喜欢 Atom 的界面，可以使用 [Pulsar](https://pulsar-edit.dev/) 作为替代品，它的用户界面与 Atom 基本相似，目标是让他们最喜欢的编辑器保持活力 "keep their favorite editor alive"[^1]．

## 外部链接

-   [Atom 官网](https://atom.io)
-   [Pulsar 官网](https://pulsar-edit.dev/)

## 参考资料

[^1]: 来源：<https://pulsar-edit.dev/about.html#the-team>


## tools/editor/clion.md

## 简介

CLion 是一款由 JetBrains 公司开发的功能丰富且强大的跨平台 C/C++ 集成开发环境（IDE）．

![Clion](./images/clion.png)

## 官方教程

在官方网站中给出了 [学习 CLion](https://www.jetbrains.com/clion/learn/) 的教程．

## 安装

参见 [Download CLion](https://www.jetbrains.com/clion/download/)．

## 配置

### 工具链安装

CLion 默认不带编译器，构建工具和调试工具，需要手动进行安装．

#### Windows

参见 [Tutorial: Configure CLion on Windows | CLion Documentation](https://www.jetbrains.com/help/clion/quick-tutorial-on-configuring-clion-on-windows.html)．

值得一提的是 CLion 的 Windows 版本中自带了 MinGW，所以可以不用额外安装 MinGW 工具链．

#### Linux

##### Debian/Ubuntu 及其衍生发行版

```bash
sudo apt install make cmake # build tools
sudo apt install gcc g++ gdb # compiler and debugger
sudo apt install clang clang++ llvm lldb # you can also choose to use clang toolchain
```

##### Arch Linux 及其衍生发行版

```bash
sudo pacman -S make cmake # build tools
sudo pacman -S gcc g++ gdb # compiler and debugger
sudo pacman -S clang clang++ llvm lldb # you can also choose to use clang toolchain
```

##### Fedora/RHEL/CentOS/Rocky Linux

```bash
sudo dnf install make cmake # build tools
sudo dnf install gcc g++ gdb # compiler and debugger
sudo dnf install clang clang++ llvm lldb # you can also choose to use clang toolchain
```

#### macOS

参见 [Tutorial: Configure CLion on macOS | CLion Documentation](https://www.jetbrains.com/help/clion/quick-tutorial-on-configuring-clion-on-macos.html)．

### 工具链设置

#### 手动设置工具链

新安装的 CLion 会自动检测系统中的 C/C++ 开发工具链，如果已安装的工具链无法自动检测到，可在 `Settings` 中找到 `Build, Execution, Deployment`>`Toolchains` 进行手动配置．

![Config Toolchains](./images/clion-toolchain.png)

### 编译、运行和调试

虽然 CLion 诞生之初是面向多文件的复杂 C/C++ 项目诞生的，早些时候的 CLion 默认使用 [CMake](https://cmake.org/) 作为构建工具，但是自 CLion 2022.3 版本起，CLion 已经支持 [C, C++ 单文件运行](https://www.jetbrains.com/help/clion/run-single-file.html)．

有多种方式来运行一个 C++ 程序，一个简单的流程如下：

1.  创建一个 C/C++ 项目：`New -> Project -> C++ Executable`，选择合适的地址和语言标准版本，点击 `Create`．
2.  打开项目，此时的项目目录下应当存在一个 `cmake-build-debug` 目录、一个 `CMakeLists.txt` 文件和一个 `main.cpp` 文件．因为我们不需要使用 CMake 来管理项目，因此我们可以删去 `CMakeLists.txt` 文件和 `cmake-build-debug` 目录及其内所有文件．
3.  点击打开 `main.cpp` 文件，并在编辑区右键单击，可以看到 `Run 'main.cpp'` 选项．选择此选项后，CLion 可以自动创建一个运行配置并运行程序．

![C++ Single File Execution](./images/clion-single-file-execution.png)

如需调试程序，可以编辑区打好断点，在编辑区右键单击，选择 `Debug 'main.cpp'` 选项．

### 通过 CMake 编译、运行和调试

#### 设置

CLion 也可使用 [CMake](https://cmake.org/) 作为构建工具，关于 CMake 的设置可以在 `Build, Execution, Deployment -> Toolchains -> CMake` 中修改．

![CMake Settings](./images/clion-cmake.png)

#### 编译选项

CMake 默认使用项目根目录下的 `CMakeList.txt` 作为构建项目的配置文件，可以使用 `add_compile_options` 命令来增加编译选项，例如：

```cmake
add_compile_options(-std=c++17 -DDEBUG)
```

其他 CMake 的功能请参考 [CMake 官方文档](https://cmake.org/documentation/)．

## 免费获取 CLion IDE 许可证

CLion 为付费产品，但是可以通过教育邮箱或开源项目申请特殊许可证．申请之后不仅可以免费使用正版 CLion IDE，还可以免费使用 JetBrains 公司开发的其他付费产品．

???+ note "Note"
    [自 2025 年 5 月起，CLion 对非商业用途免费．](https://blog.jetbrains.com/clion/2025/05/clion-is-now-free-for-non-commercial-use)
    
    根据 Toolbox 非商业用途订阅协议中的定义，商业产品是指有偿分发或提供或者作为您的商业活动的一部分使用的产品．但某些类别被明确排除在这一定义之外．常见的非商业用例包括学习和自我教育、任何形式的内容创作、开源代码和业余爱好开发．

### 使用教育邮箱获取

进入官网的 [Free Educational Licenses 页面](https://www.jetbrains.com/community/education/#students), 点击 `Apply` 按钮，填写相关信息即可申请．

![Educational Licenses](./images/clion-edu.png)

注意：在注册时于邮箱选项请填如 @edu.cn 后缀的教育邮箱，特殊许可证需要邮箱验证后方可拿到．

你可以到所在高校的教务中心官网去申请教育邮箱，如果申请不到需要使用 [学信网](https://www.chsi.com.cn) 进行认证（仅中国大陆）．

### 使用开源项目获取

如果您是某个开源项目的核心开发者或维护者之一，您可以尝试申请开源开发许可证 (Open Source Development License). 申请流程与教育许可证类似，但需要填写开源项目的仓库地址．

![Open Source Development License](./images/clion-oss.png)


## tools/editor/codeblocks.md

## 简介

Code::Blocks 是一个使用 C++ 开发的开源集成开发环境（IDE），采用 wxWidgets 作为图形界面库．该项目始于 2001 年，目前由官方社区维护，主要用于 C、C++ 和 Fortran 等编程语言的开发．[^ref1]

优点：

-   **轻量和高效**：Code::Blocks 资源占用少且启动迅速，适合资源有限的环境以及偏好轻量级 IDE 的开发者，也适合入门级开发者学习和使用．

-   **跨平台兼容性**：支持 Windows、Linux 和 macOS 等多种操作系统，提供了一致的用户体验，使得开发者可以无缝地在不同平台上工作．

-   **广泛的编译器支持**：支持包括 GCC、MSVC (Microsoft Visual C++)、Digital Mars 和 Borland C++ 5.5 在内的多种编译器，允许开发者根据项目需求选择最合适的编译工具．

缺点：

-   **功能范围有限**：相比于 CLion 或 Eclipse 等 IDE，内置功能和工具较为基础，可能不足以满足复杂项目的需求．

-   **插件生态较弱**：尽管支持插件扩展功能，但第三方插件数量和质量有限，插件生态相对较弱．

## 安装

参见 [Code::Blocks 官方网站](https://www.codeblocks.org/downloads/)，选择下载二进制安装程序（Binary Release），或者下载源代码编译安装（Source Code），然后根据需求和操作系统选择合适的安装程序，按照安装向导完成安装即可．

???+ note "下载包含 MinGW 的安装包"
    对于 Windows 用户，如果不希望手动配置编译器，建议下载包含 MinGW 的安装程序，例如 `codeblocks-xxxxmingw-setup.exe`，该版本已经包括了 GCC 编译器，无需额外安装和配置即可开始开发 C 和 C++ 项目．

![CodeBlocks DownLoad](./images/codeblocks-1.png)

## 配置

如果安装时选择了不包含 MinGW 的安装程序，或者需要使用其他编译器，则需要手动安装和配置编译器，然后设置 Code::Blocks 以使用该编译器．

### 工具链安装

参考本站的 [编译器](../compiler.md) 安装指南，下载并安装你需要的编译器．

### 工具链设置

当第一次启动 Code::Blocks 时，软件会自动扫描系统中已安装的编译器，如果没有找到编译器，可以通过以下步骤手动添加：

1.  打开 Code::Blocks，点击菜单栏的 `Settings -> Compiler`，打开编译器设置对话框（如下图所示）．![CodeBlocks Compiler Settings](./images/codeblocks-2.png)
2.  在 `Selected compiler` 下拉框中选择需要配置的编译器，例如 `GNU GCC Compiler`．
3.  在 `Toolchain executables` 选项卡中，单击 `Auto-detect` 按钮，Code::Blocks 将自动扫描系统中已安装的编译器．
4.  如果自动扫描失败，你可以手动设置编译器路径．在 `Compiler's installation directory` 中输入编译器的安装路径，例如 `C:\MinGW\bin`．
5.  设置完成后，点击 `OK` 保存设置，现在你可以使用该编译器来编译和运行项目．

## 使用

Code::Blocks 内置项目管理器，支持用户自定义构建项目，你可以在 `Project -> Build options` 中设置编译选项，选择编译器、编译选项、链接选项等，也可以在 `Project -> Properties` 中设置项目属性，例如项目名称、路径、文件列表等．

??? note "配置 Makefile"
    Code::Blocks 默认不需要编写 Makefile，如果需要使用自定义的 Makefile，可以在 `Project -> Properties` 中勾选 `This is a custom Makefile` 选项，然后在 `Project -> Build options` 中设置 Makefile 的路径．

### 创建项目

Code::Blocks 支持的编程语言包括 C、C++ 和 Fortran 等，当启动 Code::Blocks 后，可以通过 `File -> New -> Project` 创建新项目，选择项目类型和模板，然后按照向导的指示，设置项目名称、路径、编译器等，最后点击 `Finish` 完成项目创建．

Code::Blocks 也支持单文件的编译和运行，可以通过 `File -> New -> File` 创建新文件，编写代码并保存后，点击工具栏上的 `Build and run` 按钮，或者按下 `F9` 键，自动编译和运行当前文件．

### 构建和运行

以一个简单的 Console Application 项目为例，接下来介绍如何构建和运行项目：

1.  项目创建完成后，你会看到一个默认的 `main.cpp` 文件，你可以在该文件中编写代码，然后保存文件．
2.  编写完代码后，点击工具栏上的 `Build and run` 按钮，或者按下 `F9` 键，Code::Blocks 将自动编译和运行项目．
3.  编译和运行后，输出窗口中会显示程序的输出结果，你可以在输出窗口中查看程序的输出，根据需要调整代码．
4.  如果只需要编译项目，而不运行，可以点击工具栏上的 `Build` 按钮，或者按下 `Ctrl + F9` 键，Code::Blocks 将只编译项目，不运行程序．

### 调试

Code::Blocks 内置了调试器，你可以在 `Debug` 菜单中设置和启动调试器，帮助你定位和解决程序中的错误．

同理，以一个简单的 Console Application 项目为例，接下来介绍如何调试项目：

1.  **设置断点**：在需要调试的代码行左侧单击鼠标左键，设置断点，程序将在断点处停止执行．
2.  **启动调试器**：点击工具栏上的 `Debug` 按钮，或者按下 `F8` 键，Code::Blocks 将自动编译并启动调试器．
3.  **调试程序**：在调试器中，你可以单步执行程序，查看变量值、调用栈等，帮助你定位和解决程序中的错误．
4.  **停止调试**：调试完成后，你可以点击工具栏上的 `Stop` 按钮，或者按下 `Shift + F8`，停止调试器．

## 自定义设置

Code::Blocks 提供了丰富的设置选项，可以帮助调整编辑器的行为，以下是一些常用的设置：

### 界面设置

1.  在 `Settings -> Editor` 中，可以设置编辑器的字体、颜色、缩进、自动补全等选项．
2.  在 `Settings -> Environment` 中，可以设置 Code::Blocks 的全局行为，例如自动保存、自动备份、自动提示等．
3.  在 `View` 菜单中，可以调整编辑器的布局，例如打开/关闭文件浏览器、工具栏、状态栏、输出窗口等．

### 插件设置

Code::Blocks 支持插件来扩展功能，可以通过 `Settings -> Plugins` 查看和安装可用的插件，例如 DoxyBlocks、wxSmith 等，以下是一些常用的插件：

-   **DoxyBlocks**：著名的文档生成工具 Doxygen 的集成插件，可以直接在 Code::Blocks 中生成项目文档．
-   **wxSmith**：用于开发 wxWidgets 应用程序的插件，提供了可视化的界面设计工具，允许快速创建和布局 GUI 界面，简化开发流程．
-   **Thread Search**：支持多线程搜索的插件，可以在项目中快速搜索和替换符号和文本，适用于大型项目的开发．

插件的安装和使用方法请参考 [Code::Blocks 的插件文档](https://wiki.codeblocks.org/index.php/Code::Blocks_Plugins)，根据插件的需求和功能，选择合适的插件安装和使用．

???+ warning "注意"
    Code::Blocks 的插件相对单一和基础，且大部分插件已经集成到软件中，第三方插件的数量和质量有限，建议根据实际需求选择合适的插件．

### 快捷键设置

你可以通过 `Settings -> Editor -> Keyboard shortcuts` 选项卡查看和修改快捷键设置，根据自己的习惯调整快捷键．

以下是一些常用的快捷键：

| 功能         | 快捷键                 |
| ---------- | ------------------- |
| 新建文件       | `Ctrl + Shift + N`  |
| 打开文件       | `Ctrl + O`          |
| 保存当前文件     | `Ctrl + S`          |
| 全部保存       | `Ctrl + Shift + S`  |
| 关闭当前文件     | `Ctrl + W`          |
| 关闭所有文件     | `Ctrl + Shift + W`  |
| 构建和运行当前项目  | `F9`                |
| 只构建当前项目    | `Ctrl + F9`         |
| 只编译当前项目    | `Ctrl + Shift + F9` |
| 运行当前项目     | `Ctrl + F10`        |
| 调试：开始/继续   | `F8`                |
| 调试：停止      | `Shift + F8`        |
| 调试：下一步     | `F7`                |
| 调试：进入      | `Shift + F7`        |
| 调试：跳出      | `Ctrl + F7`         |
| 调试：切换断点    | `F5`                |
| 查找         | `Ctrl + F`          |
| 查找并替换      | `Ctrl + R`          |
| 转到指定行      | `Ctrl + G`          |
| 转到匹配的括号    | `Ctrl + B`          |
| 全屏切换       | `F11`               |
| 开关所有折叠     | `Ctrl + Shift + -`  |
| 展开所有折叠     | `Ctrl + Shift + +`  |
| 选择下一个匹配项   | `Ctrl + E`          |
| 选择跳到下一个匹配项 | `Ctrl + Shift + E`  |

## 参考资料与注释

[^ref1]: [Code::Blocks - 维基百科](https://zh.wikipedia.org/wiki/Code::Blocks)


## tools/editor/cpeditor.md

author: zarttic, xk2013

## 简介

[CP Editor](https://github.com/cpeditor/cpeditor) 专为算法竞赛设计，不像其它 IDE 主要是为了开发设计的．它可以帮助你自动化编译、运行、测试，从而让你专注于算法设计．它甚至可以从各种算法竞赛网站上获取样例，将代码提交到 [Codeforces](https://codeforces.com/) 上！

## 下载与安装

参见 [安装 | CP Editor](https://cpeditor.org/zh/docs/installation/)．

## 基础配置

> CP Editor 内部没有集成编译器，需要自己安装配置编译器，如有需要请参考本站关于编译器安装相关的文章[^compiler]，当然，如果你在下载时选择了带有 `with-gcc-<GCC 版本号>-llvm-<LLVM 版本号>` 后缀的安装包，你就可以使用 CP Editor 自带的编译器，路径在 `{安装目录}/mingw64/bin/`．

-   设置默认语言

    编辑器默认的语言为 `C++`．

    ![cp-setting-lang-1](images/cp-setting-lang-1.png)

    ![cp-setting-lang-2](images/cp-setting-lang-2.png)

-   设置 `C++` 命令

    需要设置一些必要的编译命令，这个要根据编译器来设定．

    ![cp-setting-lang-3](images/cp-setting-lang-3.png)

-   设置模板

    新建文件的时候会自动初始化的模板，需要注意的是 CP Editor 需要的是一个 `xxx.cpp` 的文件作为模板文件．

    ![cp-setting-lang-4](images/cp-setting-lang-4.png)

> 完成了以上的基本操作你就可以使用最基本的功能了．

## 基本功能

-   快捷键

    |                       命令                      |    操作   |
    | :-------------------------------------------: | :-----: |
    | <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>C</kbd> |   编译．   |
    | <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>R</kbd> |  编译并运行． |
    |          <kbd>Ctrl</kbd>+<kbd>R</kbd>         |   运行．   |
    |  <kbd>Ctrl</kbd>+<kbd>Alt</kbd>+<kbd>D</kbd>  | 在终端中运行． |
    |          <kbd>Ctrl</kbd>+<kbd>K</kbd>         | 终止所有进程． |
    | <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>I</kbd> |  格式化代码． |

    具体可以查阅 [官方文档](https://cpeditor.org/zh/docs/preferences/key-bindings/)．

-   样例测试

    可以把题面的样例复制下来，由 CP Editor 自动评测，而且还可以设置时间限制！

    ![cp-setting-limits](images/cp-setting-limits.png)

    ![cp-judge-1](images/cp-judge-1.png)

    ![cp-judge-2](images/cp-judge-2.png)

    ![cp-judge-3](images/cp-judge-3.png)

    ![cp-judge-4](images/cp-judge-4.png)

## 参考资料

[^compiler]: [编译器 - OI Wiki](../compiler.md)


## tools/editor/devcpp.md

author: topdevst, ksyx, ouuan, Doveqise, hsfzLZH1, wangqingshiyu, sshwy, NanoApe, DawnMagnet, CamberLoid, royqh1979

## 介绍

Dev-C++ 是一套用于开发 C/C++ 程序的自由的集成开发环境（IDE），并以 GPL 作为分发许可，使用 MinGW 及 GDB 作为编译系统与调试系统．Dev-C++ 运行在 Microsoft Windows 下．

Dev-C++ 的优点在于界面简洁友好，安装便捷，支持单文件编译，因此成为了许多入门 OI 选手以及 C++ 语言初学者的首选．在 NOIP 中，提供 Windows 作为比赛系统的省份一般预置 Dev-C++．

Dev-C++ 起源于 Colin Laplace 编写的 Bloodshed Dev-C++．该版本自 2005 年 2 月 22 日停止更新．2006 年，Dev-C++ 主要开发者 Colin Laplace 曾经对此作出了解释：「因忙于现实生活的事务，没有时间继续 Dev-C++ 的开发．」

Orwell Dev-C++ 是 Dev-C++ 的一个衍生版本，由独立程序员 Orwell (Johan Mes) 开发并维护．其对原版 Dev-C++ 进行了错误修正，并更新了编译器版本．一般而言，Dev-C++ 5.x 均为 Orwell Dev-C++．其最后一次更新于 2015 年，版本为 5.11．

Embarcadero Dev-C++[^ref1]是 Bloodshed Dev-C++ 和 Orwell Dev-C++ 的继任者．2020 年，Embarcadero 赞助并接手了原有的 Dev-C++ 项目，继续开发．Embarcadero Dev-C++ 加入了对高 DPI 的支持，更新了编译器以加入更新版本的 C++ 标准支持，以及暗色模式．

以上的 Dev-C++ 分发都被认为是「官方的」．此外，在 2015 年 Orwell Dev-C++ 停止更新后，因为教学需要，一位来自中国的个人开发者 [royqh1979](https://github.com/royqh1979) 决定继续开发他的 Dev-C++ 个人分支，命名为小熊猫 Dev-C++[^ref2]，集成了智能提示和高版本的 MinGW64，非常便于国内的个人使用和学习．

小熊猫 Dev-C++ 6.7.5 版本发布后，作者使用 qt5 开发了全新的小熊猫 C++[^ref3]，可在 windows、linux 和 macos 等系统下原生运行．小熊猫 C++ 的界面与 Dev-C++ 相似，除了提供和 Dev-C++ 相似但更加完善的单文件编译、调试、语法高亮、搜索/替换等功能外，还提供了诸如 **暗色主题**、**代码智能提示**、**变量/函数重命名**、**切换/自动识别文件编码** 等现代 IDE 常见的基本功能．此外小熊猫 C++ 还具备与 CP Editor 类似的试题集功能，可以自行编写或 **从常见的 OJ 竞赛网站上下载试题样例**，**自动运行和测试程序**．

## 使用教程

### 常用快捷键

#### 文件部分

-   `Ctrl + N`: 创建源代码
-   `Ctrl + O`: 打开文件
-   `Ctrl + W`: 关闭文件
-   `Ctrl + Shift + W`: 关闭所有文件
-   `Ctrl + P`: 打印文件

#### 格式部分

-   `Ctrl + /`：注释和取消注释
-   `Tab`: 缩进
-   `Shift + Tab`: 取消缩进

#### 行操作

-   `Ctrl + E`: 复制行
-   `Ctrl + D`: 删除行
-   `Ctrl + Shift + Up`: 向上移动
-   `Ctrl + Shift + Down`: 向下移动

#### 跳转部分

-   `Ctrl + F`: 搜索
-   `Ctrl + R`: 替换
-   `F3`: 搜索下一个
-   `Shift + F3`: 搜索上一个
-   `Ctrl + G`: 到指定行号
-   `Shift + Ctrl + G`: 到指定函数
-   `Ctrl + [1 ~ 9]`: 设置书签
-   `Alt + [1 ~ 9]`: 跳转书签

#### 显示部分

-   `Ctrl + 滚轮`：字号放大或缩小
-   `Ctrl + F11`: 全屏或恢复

#### 运行部分

-   `F9`: 只编译
-   `F10`: 只运行
-   `F11`: 编译并运行
-   `F12`: 全部重新编译

#### 调试部分

-   `F2`: 转到断点
-   `F4`: 设置断点或取消
-   `F5`: 调试运行
-   `F6`: 停止
-   `F7`: 逐步调试

### 调试流程

1.  将编译器配置设定为 `TDM-GCC 4.9.2 64-bit Debug`
2.  按 `F4` 设置或取消调试断点
3.  将光标放置在变量上，按 `Alt + A` 向调试窗口添加监控变量
4.  按 `F5` 启动调试
5.  按 `F7` 或 `Alt + N` 逐步调试
6.  按 `Alt + S` 跳至下一个调试断点
7.  按 `F6` 停止调试

## 扩展

### 增加编译选项

点击工具 -> 编译选项，然后选择 "代码生成/优化" 选项卡，下面介绍笔者常用的几个编译选项．

#### 开启优化

优化代码运行时间或占用空间．

选择 "代码生成" 子选项卡中的 "优化级别（-Ox）" 选项标签．

![](./images/Dev-C++-11.png)

#### 更换语言标准

使用新语言特性或试图让代码在旧标准下编译．

选择 "代码生成" 子选项卡中的 "语言标准（-std）" 选项标签．

![](./images/Dev-C++-12.png)

#### 显示最多警告信息

查错小助手．

选择 "代码警告" 子选项卡中的 "显示最多警告信息（-Wall）" 选项标签．

![](./images/Dev-C++-13.png)

#### 生成调试信息

当显示 "项目没有调试信息，您想打开项目调试选项并重新生成吗？" 点击后闪退或想使用调试功能时需开启此功能．

选择 "连接器" 子选项卡中的 "产生调试信息" 选项标签．

![](./images/Dev-C++-14.png)

### 编译小 trick

点击工具 -> 编译选项，然后选择 "编译器" 选项卡，接下来介绍几个常用 trick．

#### 开大栈

防止 DFS 爆系统栈之类的情况出现．

在 "连接器命令行加入以下命令" 中加入 `-Wl,--stack=128000000` 命令．

此命令将栈开到了约 128MB 的大小，有需要可以自行增加．

![](./images/Dev-C++-15.png)

#### 定义宏

方便本地评测使用文件输入输出或作其他用途．

在 "连接器命令行加入以下命令" 中加入 `-D[String]` 命令．

其中 `[String]` 改为你需要的宏名．

如图，当开启编译选项后便可将以下代码从 `test.in` 文件读入数据并在 `test.out` 文件中输出．

![](./images/Dev-C++-16.png)

```cpp
#ifdef LOCAL
freopen("test.in", "r", stdin);
freopen("test.out", "w", stdout);
#endif
```

#### 代码格式化

点击 Astyle-> 格式化当前文件 或 按 Ctrl+Shift+A 进行代码格式化．

![](./images/Dev-C++-17.png)

### 美化

#### 字体

点击工具 -> 编辑器选项，然后选择 "显示" 选项卡．

![](./images/Dev-C++-9.png)

#### 主题

点击工具 -> 编辑器选项，然后选择 "语法" 选项卡，可以使用预设主题，也可以自行调整．

![](./images/Dev-C++-10.png)

## 参考资料

[^ref1]: 项目源代码托管于 [GitHub](https://github.com/Embarcadero/Dev-Cpp) 和 [SourceForge](https://sourceforge.net/projects/embarcadero-devcpp/).

[^ref2]: 源代码托管于 [Github](https://github.com/royqh1979/Dev-Cpp)

[^ref3]: 项目官网位于 [小熊猫 C++](https://royqh1979.gitee.io/redpandacpp)，源代码托管于 [Github](https://github.com/royqh1979/RedPanda-CPP/)


## tools/editor/eclipse.md

author: ouuan, Doveqise, partychicken, Xeonacid, StudyingFather

## 介绍

Eclipse 是著名的跨平台开源集成开发环境（IDE）．最初主要用来 Java 语言开发，当前亦有人通过插件使其作为 C++、Python、PHP 等其他语言的开发工具．

Eclipse 的本身只是一个框架平台，但是众多插件的支持，使得 Eclipse 拥有较佳的灵活性，所以许多软件开发商以 Eclipse 为框架开发自己的 IDE．

Eclipse 最初是由 IBM 公司开发的替代商业软件 Visual Age for Java 的下一代 IDE 开发环境，2001 年 11 月贡献给开源社区，现在它由非营利软件供应商联盟 Eclipse 基金会（Eclipse Foundation）管理．[^ref1]

缺点：

-   实测这个 IDE 打开速度比 Visual Studio 慢
-   更新速度玄学，插件更新速度跟不上 IDE 的更新速度，对于经常更新的同学很不友好．

优点：

-   使用体验较好
-   能够快速上手，所以比较推荐 OIer 用这个 IDE．

## 安装 & 配置指南

安装可参照 [Eclipse/Installation - Eclipsepedia](https://wiki.eclipse.org/Eclipse/Installation)．

安装后如图填写目录信息以建造项目：

![](./images/eclipse4.png)

![](./images/eclipse5.png)

![](./images/eclipse6.png)

![](./images/eclipse7.png)

## 拓展

这个软件的帮助手册很详细，建议刚接触的同学多看帮助手册，多百度，并且这个 IDE 的使用手感与 Visual Studio 相近．

和 [VS Code](./vscode.md) 类似，Eclipse 中也提供了很多插件，这些插件可以让 Eclipse 变得更加易用．[^ref2]

## 参考资料与注释

[^ref1]: [Eclipse - 维基百科](https://zh.wikipedia.org/wiki/Eclipse)

[^ref2]: [曾经的 Java IDE 王者 Eclipse 真的没落了？21 款插件让它强大起来！](https://blog.csdn.net/csdnnews/article/details/78495979)


## tools/editor/emacs.md

author: ouuan, akakw1, Ir1d, partychicken, Xeonacid

本页面为 Emacs 的入门教程．

> 15 分钟入门 Emacs．

## 简介

Emacs 是一款非常容易上手的编辑器，只需要简短的几行配置就能使用，但是想要非常熟练地使用 Emacs 进行各项工作还是需要一定的时间．

作为入门教程，这里仅介绍 Emacs 的基本功能，以及较方便地用 Emacs 编写、调试代码的方法．

## 入门

### 命令

命令在 Emacs 中有很大的作用．

使用 Application 键[^note1]（Windows 系统下 Emacs 未指定这个键，需要手动设置）或者快捷键 M-x（<kbd>Alt</kbd>+<kbd>x</kbd>）可以打开命令输入，输入完按下回车可以执行命令．

通常使用 `es` 或者 `eshell` 命令来打开 Eshell（类似一个终端）．

输入命令通常可以用快捷键代替．

### 缓冲 (buffer)

缓冲即打开的文件和进程，在不保存的情况下，在缓冲中修改并不会修改到文件．

在缓冲区的底部点击缓冲的名字或者使用快捷键可以切换缓冲．

### 编译、调试和运行

编译和调试功能的入口在顶部菜单栏的 Tools 下拉栏．使用者也可以通过命令或者自定义快捷键使用编译和调试功能．

可以使用终端或 Eshell 运行程序．

按下 Tools 中的调试 (gud-gdb) 后，输入程序名（一般会自动输好，但如果中途将程序另存为或者打开了两个需要调试的程序，**自动输好的文件名可能会有误**）即可开始调试．

### 分屏

这个功能能让使用者同时查看各个缓冲的内容，而不需要来回切换缓冲，方便测试、调试代码．

分屏功能可以同时显示多个窗口，用鼠标拖动窗口的边缘可以缩放窗口．

几个快捷键：

-   删除分屏 "C-x 0"：将这个分屏删去
-   横向分屏 "C-x 3"：将这个分屏横向分成两半
-   纵向分屏 "C-x 2"：将这个分屏纵向分成两半

推荐的窗口布局为将窗口分为四块：先横向分，调整一块的宽度约为 3/4 屏，作为编辑窗口．将另一块横向分，一块作为调试和编译信息显示的窗口，另一块再纵向分，一块打开输入文件，一块打开输出文件．

![](./images/emacs.png)

### 快捷键

Emacs 拥有极为丰富的快捷键，可以大幅提高工作的效率．使用者可以在配置中自定义快捷键或者设置快捷键的映射．

由于快捷键过多，所以 Emacs 快捷键的使用与操作系统不同．

为了方便描述，做如下约定：

| 字符 | 键位              |
| -- | --------------- |
| C  | <kbd>Ctrl</kbd> |
| M  | <kbd>Alt</kbd>  |
| ？  | 任意键位            |

一般有以下三种：

-   `F?`、`ESC`：直接按下对应的功能键．
-   `M-?`、`C-?`、`C-M-?`：按下<kbd>Alt</kbd>或者<kbd>Ctrl</kbd>的同时按下 `?`．
-   `? ?`：先按下第一个 `?` 代表的键，松开再按下第二个 `?` 代表的键．

下面是一些常用的快捷键：

-   `C-x h`：全选
-   `C-x left`、`C-x right`：切换到上/下一个缓冲
-   `C-x d`：打开一个目录
-   `C-x C-f`：打开一个文件（如果不存在文件则新建文件）

## 个性化

刚安装好的 Emacs 外观难看且不好使用，因此需要对其进行个性化设置．

由于配置不好记，所以部分可以直接设置的部分建议不要记配置．

### 直接设置

-   Options：`Highlight Matching Parentheses` 高亮匹配括号
-   Options：`Blink Cursor` 设置光标闪烁
-   Options Show/Hide：`Tool Bar` 显示/不显示工具栏（默认显示，建议不显示）
-   Options：`Use CUA Keys` 勾选后可以使用 Ctrl + C,Ctrl + V 等快捷键进行复制粘贴
-   Options Customize-Emacs：`Custom Theme` 选择配色方案，选择完后需要点击保存
-   Options：`Save Options`  **保存配置**

### 配置

在 home 目录下显示隐藏文件（Windows 系统在 **用户目录** 的 `AppData\Roaming` 目录下），".emacs" 就是配置文件（如果没有说明之前没保存），打开修改即可．如果 Emacs 已打开，则需要重启 Emacs，配置才能生效．

考场推荐的配置如下．

```text
;;设置一键编译 可以自行添加参数 难背考场不建议使用 不建议依赖一键编译
(defun compile-file ()(interactive)(compile (format "g++ -o %s %s -g -lm -Wall" (file-name-sans-extension (buffer-name))(buffer-name))))
(global-set-key [f9] 'compile-file)
;;;;设置编译快捷键（如果设置了一键编译不要与一键编译冲突）
;;(global-set-key [f9] 'compile)

(global-set-key (kbd "C-a") 'mark-whole-buffer) ;;全选快捷键
(global-set-key (kbd "C-z") 'undo) ;;撤销快捷键
(global-set-key [f10] 'gud-gdb) ;;GDB调试快捷键
(global-set-key (kbd "RET") 'newline-and-indent) ;;换行自动缩进
(global-set-key (kbd "C-s") 'save-buffer) ;;设置保存快捷键
(setq-default kill-ring-max 65535) ;;扩大可撤销记录

;;C++ 代码风格 一般控制缩进规则
;;;"bsd" 所有大括号换行
;;;"java" 所有大括号不换行．else 接在右大括号后面
;;;"awk" 只有命名空间旁、定义类、定义函数时的大括号换行．else 接在右大括号后面
;;;"linux" 只有命名空间旁、定义类、定义函数时的大括号换行．else 接在右大括号后面．一般来说，这个风格应该有 8 格的空格缩进
(setq-default c-default-style "awk")
```

??? note "完整配置"
    ```text
    ;;设置一键编译
    (defun compile-file ()(interactive)(compile (format "g++ -o %s %s -g -lm -Wall" (file-name-sans-extension (buffer-name))(buffer-name))))
    (global-set-key [f9] 'compile-file)
    ;;;;设置编译快捷键（如果设置了一键编译不要与一键编译冲突）
    ;;(global-set-key [f9] 'compile)
    
    ;;考场必备
    (global-set-key (kbd "C-a") 'mark-whole-buffer) ;;全选快捷键
    (global-set-key (kbd "C-z") 'undo) ;;撤销快捷键
    (global-set-key [f10] 'gud-gdb) ;;GDB调试快捷键
    (global-set-key (kbd "RET") 'newline-and-indent) ;;换行自动缩进
    (global-set-key (kbd "C-s") 'save-buffer) ;;设置保存快捷键
    (setq-default kill-ring-max 65535) ;;扩大可撤销记录
    ;;(define-key key-translation-map [apps] (kbd "M-x")) ;; windows 系统下设置命令快捷键
    
    ;;设置缩进
    ;;;C++ 代码缩进长度．
    (setq-default c-basic-offset 4)
    ;;;使用 tab 缩进
    (setq-default indent-tabs-mode t)
    ;;;tab 的长度．务必和缩进长度一致
    (setq-default default-tab-width 4)
    (setq-default tab-width 4)
    
    ;;设置默认编码环境
    (set-language-environment "UTF-8")
    (set-default-coding-systems 'utf-8)
    
    ;;不显示欢迎页面
    (setq-default inhibit-startup-screen t)
    
    ;;设置标题
    (setq-default frame-title-format "")
    
    ;;显示行号
    (global-display-line-numbers-mode t)
    
    ;;高亮
    (global-hl-line-mode 1);;高亮当前行
    (show-paren-mode t);;高亮匹配括号
    (global-font-lock-mode t);;语法高亮
    
    ;;允许emacs和外部其他程序的粘贴 好像默认允许
    (setq-default x-select-enable-clipboard t)
    
    ;;设置字体是 Ubuntu Mono 的 16 号，如果字体不存在会报错
    (set-face-attribute 'default nil :font "Ubuntu Mono-16")
    ;(set-face-attribute 'default nil :font "Consolas-16") ;; windows 系统请用这条
    
    ;;鼠标滚轮支持
    (mouse-wheel-mode t)
    
    ;;设置光标形状为竖线（默认为方块）
    (setq-default cursor-type 'bar)
    
    ;;回答 yes/no 改成回答 y/n
    (fset 'yes-or-no-p 'y-or-n-p)
    
    ;;透明度
    (set-frame-parameter (selected-frame) 'alpha (list 85 60))
    (add-to-list 'default-frame-alist (cons 'alpha (list 85 60)))
    
    ;;减少页面滚动的行数，防止整页地滚动
    (setq-default scroll-margin 3 scroll-conservatively 10000)
    
    ;;优化文件树结构
    (ido-mode t)
    
    ;;配色方案
    (setq default-frame-alist
             '((vertical-scroll-bars)
               (top . 25)
               (left . 45)
               (width . 120)
               (height . 40)
               (background-color . "grey15")
               (foreground-color . "grey")
               (cursor-color . "gold1")
               (mouse-color . "gold1")
               (tool-bar-lines . 0)
               (menu-bar-lines . 1)
               (scroll-bar-lines . 0)
               (right-fringe)
               (left-fringe)))
    
    (set-face-background 'highlight "gray5")
    (set-face-foreground 'region "cyan")
    (set-face-background 'region "blue")
    (set-face-foreground 'secondary-selection "skyblue")
    (set-face-background 'secondary-selection "darkblue")
    (set-cursor-color "wheat")
    (set-mouse-color "wheat")
    
    (custom-set-variables
     '(ansi-color-faces-vector
       [default default default italic underline success warning error])
    ;;启动 Ctrl-x Ctrl-c Ctrl-v = 剪切 复制 粘贴
     '(cua-mode t nil (cua-base))
     '(show-paren-mode t)
    ;;隐藏工具栏
     '(tool-bar-mode nil))
    ;;关闭光标闪烁
     '(blink-cursor-mode nil)
    (custom-set-faces)
    ```

### 拓展阅读

要以终端模式启动 Emacs，在启动时添加参数 `-nw`．Emacs 有多种变体，如采用 native-comp 来减少延迟的 [GCC Emacs](http://akrl.sdf.org/gccemacs.html) 及其纯 GTK 版本变体、针对 macOS 优化的 Emacs Macport．

Emacs 有中心化的软件仓库，配置后可通过 `M-x package-install` 来安装插件．使用 [镜像站](https://mirrors.bfsu.edu.cn/help/elpa/) 可以加快下载速度．

Emacs 可以使用语言服务器（Language Server Protocol）来提高编辑体验，目前推荐的 C++ 后端是 [Clangd](https://clangd.llvm.org/)．前端可以采用 [Eglot](https://github.com/joaotavora/eglot) 或 [Emacs LSP](https://emacs-lsp.github.io/lsp-mode/)，参阅 [此条目](https://github.com/joaotavora/eglot#historical-differences-to-lsp-modeel) 可能对选择前端有所帮助．

拓展名为 `.org` 的 Org Mode 文档可以通过 [Pandoc](https://pandoc.org/) 转换为 Markdown 文档．

## 参考资料与注释

[^note1]: 该键的作用是调出鼠标右键菜单，一般为右<kbd>Ctrl</kbd>左边的第一个键．


## tools/editor/geany.md

author: xingjiapeng, MingqiHuang

Geany 是一个轻量、便捷的编辑器，对于 Linux 环境下的初学者较为友好．

与 Dev-C++ 一样，它可以编译运行单个文件．

不过，它可以在 Linux/Windows/macOS 下运行．

其官网为：<https://geany.org/>

## 优缺点

### 优点

1.  轻量；
2.  可以编译运行单个文件；
3.  不需要太多配置；
4.  跨平台．

### 缺点

1.  没有太多人使用；
2.  在 macOS Catalina 下有一些权限问题[^1]；
3.  新建文件时，默认不会有语法高亮，需要手动切换文件类型．

## 安装

参见 [Download | Geany](https://geany.org/download/)

## 使用技巧

### 切换文件类型

在*文档 -> 设置文件类型*中进行切换．

如 C++ 语言，点击*文档 -> 设置文件类型 -> 编程语言 -> C++ 源文件*，即可看到文件已被转换为 C++ 语言的语法高亮了．

### 设置文件模板

在配置文件目录下建立 templates/files 文件夹，建立在其中的文件即为模板文件，再次打开 Geany，就可以在*文件 -> 从模板新建*中找到它了．

配置文件目录可以通过*帮助 -> 调试信息*的第二、三行找出．

这里给出 macOS 和 Linux 下的默认模板配置文件目录：

-   系统目录：`/usr/share/geany/templates/files/`
-   用户目录：`~/.config/geany/templates/files/`[^2]

## 常见问题

### 兼容深度终端

在*首选项 -> 工具 -> 虚拟终端*，修改终端的命令为：

```bash
deepin-terminal -x "/bin/sh" %c
```

点击「应用」按钮即可．[^3]

## 参考资料与注释

[^1]: 详见：<https://github.com/geany/geany/issues/2344>

[^2]: 来源：<https://wiki.geany.org/config/templates>

[^3]: 来源：Deepin Wiki <https://wiki.deepin.org/>


## tools/editor/guide.md

GUIDE（GAIT Universal IDE）是由北航 GAIT 研究组开发的、专门为 NOI 选手设计的、支持 C/C++/Pascal 三种程序设计语言的小型集成开发环境．

???+ note "Note"
    自 2021 年 9 月 1 日起启用的 NOI Linux 2.0 不再包含 GUIDE．[^ref1]

## 安装

### Windows

参见 <https://www.noi.cn/xw/2009-03-23/714714.shtml>．

### Linux

参见 <https://www.noi.cn/xw/2009-03-23/714714.shtml> 或按照如下步骤安装．

#### 需要的动态库文件及包名

| 动态库                 | Arch 包名          | Debian 包名      | Fedora 包名  | openSUSE x86 包名   | openSUSE x86\_64 包名     |
| ------------------- | ---------------- | -------------- | ---------- | ----------------- | ----------------------- |
| libpng12.so.0       | lib32-libpng12   | libpng12       | libpng12   | libpng12-0        | libpng12-0-32bit        |
| libSM.so.6          | lib32-libsm      | libsm6         | libSM      | libSM6            | libSM6-32bit            |
| libICE.so.6         | lib32-libice     | libice6        | libICE     | libICE6           | libICE6-32bit           |
| libXi.so.6          | lib32-libxi      | libxi6         | libXi      | libXi6            | libXi6-32bit            |
| libXrender.so.1     | lib32-libxrender | libxrender1    | libXrender | libXrender1       | libXrender1-32bit       |
| libXrandr.so.2      | lib32-libxrandr  | libxrandr      | libXrandr  | libXrandr2        | libXrandr2-32bit        |
| libfreetype.so.6    | lib32-freetype2  | libfreetype6   | freetype   | libfreetype6      | libfreetype6-32bit      |
| libfontconfig.so.1  | lib32-fontconfig | libfontconfig1 | fontconfig | libfontconfig1    | libfontconfig1-32bit    |
| libXext.so.6        | lib32-libxext    | libxext6       | libXext    | libXext6          | libXext6-32bit          |
| libX11.so.6         | lib32-libx11     | libx11-6       | libX11     | libX11-6          | libX11-6-32bit          |
| libz.so.1           | lib32-zlib       | zlib1g         | zlib       | libz1             | libz1-32bit             |
| libgthread-2.0.so.0 | lib32-glib2      | libglib2.0-0   | glib2      | libgthread-2\_0-0 | libgthread-2\_0-0-32bit |
| libglib-2.0.so.0    | lib32-glib2      | libglib2.0-0   | glib2      | libglib2\_0-0     | libglib2\_0-0-32bit     |
| libstdc++.so.6      | lib32-gcc-libs   | libstdc++6     | libstdc++  | libstdc++6        | libstdc++6-32bit        |
| libgcc\_s.so.1      | lib32-gcc-libs   | lib32gcc1      | libgcc     | libgcc\_s1        | libgcc\_s1              |
| librt.so.1          | lib32-glibc      | libc6          | glibc      | glibc             | glibc-32bit             |
| libpthread.so.0     | lib32-glibc      | libc6          | glibc      | glibc             | glibc-32bit             |
| libdl.so.2          | lib32-glibc      | libc6          | glibc      | glibc             | glibc-32bit             |
| libm.so.6           | lib32-glibc      | libc6          | glibc      | glibc             | glibc-32bit             |
| libc.so.6           | lib32-glibc      | libc6          | glibc      | glibc             | glibc-32bit             |

#### 在 Debian 或 Ubuntu 安装

```bash
sudo apt install -y libpng12 libsm6 libice6 libxi6 libxrender1 libxrandr libfreetype6 libfontconfig1 libxext6 libx11-6 zlib1g libglib2.0-0 libglib2.0-0 libstdc++6 lib32gcc1 libc6
wget -c http://download.noi.cn/T/noi/GUIDE-1.0.2-ubuntu.tar
tar -xvf GUIDE-1.0.2-ubuntu.tar
cd GUIDE-1.0.2-ubuntu
echo "install:\n\tinstall -Dm755 -t /usr/bin GUIDE\n\tinstall -Dm644 -t /usr/share/ lang_en.qm\n\tmkdir -p /usr/share/apis/ && cp -r apis/* /usr/share/apis/\n\tmkdir -p /usr/share/doc/GUIDE/ && mkdir -p /usr/share/doc/GUIDE/html/ && cp -r doc/*  /usr/share/doc/GUIDE/html/" > Makefile
sudo apt install -y checkinstall
sudo checkinstall --pkgname "GUIDE" --pkgversion "1.0.2" -y
```

#### 在 openSUSE 安装

按照 [openSUSE/opi](https://github.com/openSUSE/opi#install) 给出的方式安装 opi．

然后：（32 位用户自行删去 `-32bit`）

```bash
sudo opi checkinstall
sudo zypper install -n {libpng12-0,libSM6,libICE6,libXi6,libXrender1,libXrandr2,libfreetype6,libfontconfig1,libXext6,libX11-6,libz1,libgthread-2_0-0,libglib2_0-0,libstdc++6,libgcc_s1,glibc}-32bit
wget -c http://download.noi.cn/T/noi/GUIDE-1.0.2-ubuntu.tar
tar -xvf GUIDE-1.0.2-ubuntu.tar
cd GUIDE-1.0.2-ubuntu
echo "install:\n\tinstall -Dm755 -t /usr/bin GUIDE\n\tinstall -Dm644 -t /usr/share/ lang_en.qm\n\tmkdir -p /usr/share/apis/ && cp -r apis/* /usr/share/apis/\n\tmkdir -p /usr/share/doc/GUIDE/ && mkdir -p /usr/share/doc/GUIDE/html/ && cp -r doc/*  /usr/share/doc/GUIDE/html/" > Makefile
sudo checkinstall --pkgname "GUIDE" --pkgversion "1.0.2" -y -rpmi
```

## 编辑文件

点击页面上方工具栏的「新文件」按钮（或者使用<kbd>Ctrl</kbd>+<kbd>N</kbd>快捷键）来创建一个新文件．

在默认情况下，GUIDE 的代码字体并非等宽字体，看上去非常不美观，因此需要在设置中更改字体．

在 编辑 -> 选项 -> 语法高亮设置 中，点击「全部字体」按钮，即可切换编辑器字体．

需要注意的是，对于未保存的新文件，字体仍然是默认字体．因此建议在开始编辑前先保存文件（点击工具栏的「保存」按钮，或按下<kbd>Ctrl</kbd>+<kbd>S</kbd>快捷键），再进行编辑．

## 编译与运行

在编辑完源代码后，点击工具栏的「编译」按钮（或<kbd>F7</kbd>快捷键）进行编译．

???+ note "更改编译选项"
    GUIDE 没有设置默认编译选项的功能，用户只能更改对某个文件的编译选项．
    
    右键点击想要更改编译选项的文件的标签，选择 **设置编译命令** 选项，即可更改该文件的编译选项．

如果源代码正常编译，点击工具栏的「运行」按钮（或<kbd>Ctrl</kbd>+<kbd>F5</kbd>快捷键）即可运行程序．

## 调试

GUIDE 自带的调试功能存在很多 bug（如程序中途发生崩溃等），因此不推荐直接使用 GUIDE 的调试功能．

建议直接在 [终端](../cmd.md) 下使用 gdb 来进行调试．

[^ref1]: [NOI Linux 2.0 发布，将于 9 月 1 日起正式启用！](https://www.noi.cn/gynoi/jsgz/2021-07-16/732450.shtml)


## tools/editor/kate.md

author: CoelacanthusHex

## 软件简介

Kate 是一个具有众多功能的跨平台文本编辑器．Kate 还附带了多种插件，包括一个嵌入式终端，可以让你直接从 Kate 中启动控制台命令，强大的搜索和替换插件，以及一个预览插件，可以渲染 MD、HTML 甚至 SVG 文件．支持通过交换文件在系统崩溃时恢复数据，带参数提示的自动补全，同时支持 [LSP (Language Server Protocol)](https://microsoft.github.io/language-server-protocol/) 以获得更为强大的补全．

## 下载与安装

可打开 [Kate 官网](https://kate-editor.org/)，然后进入 [获取页面](https://kate-editor.org/zh-cn/get-it/)．随后，根据你使用的系统和喜欢的安装方式进行安装．

## 用法与功能

### 交换文件防止数据丢失

与 Vim 类似，Kate 会将未保存的更改写入一个交换文件（一般是原文件名前面加点后面加 `.kate-swp`），如果遭遇断电或程序崩溃等意外，下次启动时不会丢失未保存的更改．

### 代码高亮

Kate 支持三百余种语言的语法高亮．一般来说，Kate 可以自动地选择对应的语言进行语法高亮，不过偶尔也有错误的时候，这时候可以点击最右下角的按钮，选择正确的语言．

#### 自己编写语法高亮文件

尽管 Kate 支持超过三百种语言的语法高亮，但是仍不免有语言未被覆盖到，此时可以自己动手编写语法高亮文件．
Kate 自身自带的文件位于 [Syntax Highlighting Powered By KSyntaxHighlighting Framework](https://kate-editor.org/syntax/)，语法可参照 [Working with Syntax Highlighting](https://docs.kde.org/trunk5/en/kate/katepart/highlight.html)，编写好的文件根据 [Syntax definition files](https://github.com/KDE/syntax-highlighting#syntax-definition-files) 放置．[CoelacanthusHex/dotfiles@80a913c/pam\_env.xml](https://github.com/CoelacanthusHex/dotfiles/blob/80a913cc5b90d7878eb0ed77b8df2d9b97926272/kate/.local/share/katepart5/syntax/pam_env.xml) 有笔者编写的一个配置文件可供参考．

### 切换语言

点击上方工具栏里的 `设置`/`Setting`，然后点击 `配置语言`/`Configure Language`，随后选择语言即可，注意可以选择备选语言．

### 编码与行尾符

Kate 可以自动识别当前文件使用的是什么编码，如果识别错误，可以点击右下角倒数第二个按钮，选择正确的编码．

同时，Kate 也可以自动识别当前文件使用的行尾符，如果识别错误，可以点击 `工具`→`行尾`/`Tool`→`End of line` 选择正确的行尾符．

### 查找与替换

依次单击 `编辑`→`查找`（快捷键<kbd>Ctrl</kbd>+<kbd>F</kbd>）即可打开「查找」页面．依次单击 `编辑`→`替换`（快捷键<kbd>Ctrl</kbd>+<kbd>R</kbd>）即可打开「查找与替换」页面．同时，点击左下角 `搜索与替换` 也可打开「查找与替换」页面．

具体操作和其他编辑器并无太大差别，但是支持一些额外的特性，例如：

1.  是否区分大小写
2.  支持正则表达式（包括捕获组）
3.  从当前文件到多文件再到当前工程不等的范围
4.  对查找的结果进行选择替换

### Language Server Protocol

Kate 自 19.12 起支持 LSP Client，最初仅支持 C/C++、D、Fortran、Go、Latex/BibTeX、OCaml、Python、Rust，现如今支持如下表中的语言：

|     语言     |                                       LSP Server                                      |
| :--------: | :-----------------------------------------------------------------------------------: |
|    Bash    |        [bash-language-server](https://github.com/bash-lsp/bash-language-server)       |
|    LaTeX   |                         [texlab](https://texlab.netlify.com/)                         |
|   BibTeX   |                         [texlab](https://texlab.netlify.com/)                         |
|      C     |                     [clangd](https://clang.llvm.org/extra/clangd/)                    |
|     C++    |                     [clangd](https://clang.llvm.org/extra/clangd/)                    |
|      D     |                      [serve-d](https://github.com/Pure-D/serve-d)                     |
|   Fortran  |              [fortls](https://github.com/hansec/fortran-language-server)              |
|     Go     |                       [gopls](https://golang.org/x/tools/gopls)                       |
|   Haskell  | [haskell-language-server-wrapper](https://github.com/haskell/haskell-language-server) |
| JavaScript | [typescript-language-server](https://github.com/theia-ide/typescript-language-server) |
|    OCaml   |                     [ocamllsp](https://github.com/ocaml/ocaml-lsp)                    |
|    Perl    |        [Perl-LanguageServer](https://github.com/richterger/Perl-LanguageServer)       |
|   Python   |               [pyls](https://github.com/palantir/python-language-server)              |
|    Rust    |                        [rls](https://github.com/rust-lang/rls)                        |
| TypeScript | [typescript-language-server](https://github.com/theia-ide/typescript-language-server) |
|      R     |          [RLanguageServer](https://github.com/REditorSupport/languageserver)          |
|     zig    |                         [zls](https://github.com/zigtools/zls)                        |

要启用 LSP 相关特性，需要前往菜单栏中 `设置`→`配置 Kate` 然后选择 `插件` 中 `LSP 客户端` 以启用相关特性．当打开对应语言的文件时，Kate 会自动拉起对应的 LSP Server．

#### 增加配置

此外，用户还可以手动编写配置，具体格式为：

```json
{
    "servers": {
        "bibtex": {
            "use": "latex",
            "highlightingModeRegex": "^BibTeX$"
        },
        "c": {
            "command": ["clangd", "-log=error", "--background-index"],
            "commandDebug": ["clangd", "-log=verbose", "--background-index"],
            "url": "https://clang.llvm.org/extra/clangd/",
            "highlightingModeRegex": "^(C|ANSI C89|Objective-C)$"
        },
        "cpp": {
            "use": "c",
            "highlightingModeRegex": "^(C\\+\\+|ISO C\\+\\+|Objective-C\\+\\+)$"
        },
        "haskell": {
            "command": ["haskell-language-server-wrapper", "--lsp"],
            "rootIndicationFileNames": ["*.cabal", "stack.yaml", "cabal.project", "package.yaml"],
            "url": "https://github.com/haskell/haskell-language-server",
            "highlightingModeRegex": "^Haskell$"
        },
        "latex": {
            "command": ["texlab"],
            "url": "https://texlab.netlify.com/",
            "highlightingModeRegex": "^LaTeX$"
        },
        "rust": {
            "command": ["rls"],
            "rootIndicationFileNames": ["Cargo.lock", "Cargo.toml"],
            "url": "https://github.com/rust-lang/rls",
            "highlightingModeRegex": "^Rust$"
        }
    }
}
```

其中 `server` 里的每一项代表一种语言，在这个语言里，`command` 代表启动 LSP Server 所使用的命令，`command` 是一个数组，是所需要执行的命令以空格分词的结果；`url` 是 LSP 的网址；`rootIndicationFileNames` 是用于确定项目根目录的文件；`highlightingModeRegex` 则匹配某种语法高亮的名字，以确定使用哪个 LSP；如果存在 `use` 项，则代表使用 `use` 项对应的语言的配置．

该配置项位于 `设置`→`配置 Kate`→`LSP 客户端`→`用户服务器设置`，其中 `LSP 客户端` 部分要在 `插件` 中启用 `LSP 客户端` 插件后才可见．

### 内置终端

???+ note "注意"
    内置终端依赖了 KDE 的 Konsole[^ref1]，而 Konsole 为 \* nix 独有包．也就是说，Windows 下该特性不可用．

按<kbd>F4</kbd>可打开或关闭内置终端，也可点击左下角 `终端` 按钮打开，内置终端的当前目录会自动与当前文件保持一致，并随着你选择的文件而改变．其余与一般终端并无太大不同．

### 外部工具

点击 `工具`→`外部工具` 可执行．

点击 `工具`→`外部工具`→`配置` 可以配置外部工具．

#### 添加外部工具

##### 从预置配置中添加

进入配置页面后，点击左下角 `添加`→`从默认工具添加`，然后点击对应工具即可．

##### 手写配置添加

进入配置页面后，点击左下角 `添加`→`添加工具`，然后按提示填写即可．可以参照 [此文档（英文）](https://docs.kde.org/trunk5/en/kate/kate/kate-application-plugin-external-tools.html) 来编写自己的外部工具配置．注意可点击如下标志查看可使用的变量．

![](images/kate-3-var.png)

#### 常用的外部工具

##### 编译并执行单个 C++ 文件

在 \* nix 系统下，打开任意 C++ 源文件，在外部工具里找到 `编译执行 cpp`，点击即可．

???+ note "对于 Windows 用户"
    在默认情况下，由于该工具的可执行文件为 `sh`，使得该工具在 Windows 下不可用．然而，用户可以对该工具进行修改，使其可用于 Windows 系统．
    
    要进行修改，请先确保你的系统内有一个可用的 C++ 编译器．然后从默认工具添加 `编译运行 cpp`，将其中 `可执行文件` 从 `sh` 改为 `powershell`，参数改为 `-ExecutionPolicy Bypass -Command "g++ %{Document:FilePath} -o %{Document:FileBaseName}.exe;./%{Document:FileBaseName}.exe"` [^note1][^note2]即可．

##### Git Blame

打开任意文件，在外部工具里找到 `git blame`，点击之后，会打开一个窗口，展示 git blame 的结果．

##### 格式化

格式化功能要求对应包或应用程序可用，例如，C/C++ 的格式化要求 `clang-format` 可用．对于其他语言，用户可以前往外部工具配置中查看其默认可执行文件作为参考．

打开任意源文件，在外部工具里找到 `用 xxx 格式化`，点击即可．另外，对于 C/C++ 语言的源文件，`clang-format` 可格式化选中的文本．

### Git Blame

要启用该特性，需要前往菜单栏中 `设置`→`配置 Kate` 然后选择 `插件` 中 `Git Blame`．

启用该特性后，Kate 会在每一行后面以较浅字体显示在 Git 中最后于什么时间被谁修改，将鼠标移动到文字上会出现一个悬浮窗显示 commit 的具体信息．

## 相关外部链接

-   [The Kate Handbook](https://docs.kde.org/stable5/en/kate/kate/kate.pdf)
-   [关于如何手写自己的 LSP 客户端配置（英文）](https://docs.kde.org/trunk5/en/kate/kate/kate-application-plugin-lspclient.html#Configuration)
-   [关于如何手写自己的外部工具配置（英文）](https://docs.kde.org/trunk5/en/kate/kate/kate-application-plugin-external-tools.html)

## 参考资料与脚注

[^ref1]: [Arch Linux 中对该包的描述](https://archlinux.org/packages/extra/x86_64/kate/) 中，其可选依赖了 `konsole`，描述为 `open a terminal in Kate`（在 Kate 中打开一个终端）．

[^note1]: 若 `g++` 不在 `PATH` 环境变量中，则将其改为编译器的绝对路径

[^note2]: 或者，如果使用 Clang，则将 `g++` 改为 `clang++`．


## tools/editor/npp.md

author: ouuan, CBW2007, partychicken, StudyingFather, Xeonacid, Henry-ZHR

## 软件简介

Notepad++ 是 Windows 操作系统下的文本编辑器，支持多国语言、多种编码、多种编程语言的高亮和补全．它的 logo 也十分可爱，是一只变色龙（![npp-logo](./images/npp-logo.webp)）

其功能比其他许多编辑软件强大许多，打开大文件时更加稳定，不断撤销不会出问题．关闭时也不需要保存，它会自动为你保存在缓冲区中．（可能需要配置）而且，它十分小巧，只有 10MB+，甚至可以放在 U 盘中随身携带．

## 下载与安装

参见 [Getting started | Notepad++ User Manual](https://npp-user-manual.org/docs/getting-started/)．

## 更改界面语言

![npp-lang](./images/npp-lang.gif)

语言改完了，就可以随心所欲地魔改编辑器啦！

## 初级玩法

这里主要讲一些基础和特色功能．

### 查找与替换

依次单击「（菜单栏）搜索」->「查找」（快捷键 `CTRL`+`F`）即可打开「查找」页面（如下图）．

![npp-search](./images/npp-search.png)

依次单击「（菜单栏）搜索」->「替换」（快捷键 `CTRL`+`H`）即可打开「替换」页面（如下图）．

![npp-replace](./images/npp-replace.png)

查找、替换之间其实是一个窗口，单击上面的标签页就可以完成切换．

其功能与普通编辑器大同小异，但是支持更多，如：

1.  严格匹配或大小写匹配等
2.  跨文档匹配
3.  转义字符，如'\r'，'\n'．
4.  正则表达式
5.  计数

### 定期备份

![npp-settings-1](./images/npp-settings-1.png)

有了这个功能，就可以不用费心地担心意外情况代码丢失啦！

但是，这个功能只是为你的文件拍了一个快照，并没有真正保存，所以还是建议要有良好的保存习惯．或者说可以去自带插件商店安装 "Auto Save" 插件（详见 [高级玩法 -> 插件](#插件)，下同）

### 书签功能

在你需要的行按 `Ctrl`+`F2` 即可设放置/取消书签，放置过书签的行前段有一个蓝色圆点．

按 `F2` 可以定位到下一个书签．

如果你抱怨不方便，可以去自带插件商店安装 "Bookmarks" 插件

### 代码高亮

右击左下角的 "XXX file"，可以选择许多种语言高亮，C、C++、PASCAL、Markdown 等任你挑选．你甚至可以自己定义高亮！

如果你认为每一次打开文件都要更改高亮很麻烦，可以在「设置 -> 首选项 -> 新建 -> 默认语言」中修改默认高亮．

需要渲染 Markdown 的，可以去插件商店安装 "Markdown Viewer"，还有更多类似插件等着你！

### 显示所有字符

![npp-settings-2](./images/npp-settings-2.png)

点击红框所圈的按钮，就可以非（za）常（luan）清（wu）晰（zhang）地显示出「空格」、「TAB」、「换行」等原来不可见字符．

### 自动识别文件编码与换行符

Notepad++ 可以自动识别当前文件编码是 `UTF-8` 还是 `GB2312` 甚至其他．再也不用担心被 `锟斤拷` 抡死或被 `烫烫烫` 烫死了．

如果要使用不同的编码浏览文章，请依次单击「（菜单顶栏）编码」->「使用 XXX 编码」．如果想给文件换一个字符编码，请依次单击「（菜单顶栏）编码」->「转为 XXX 编码」．

它还可以自动识别换行符是 `CR`、`LF` 或 `CRLF`．不用担心下载下来的数据被吞换行．

在底部信息栏，你可以看到 "Windows(CR LF)" 等字样，这就是当前文件的换行符．右击它，可以改变当前文件换行符．此操作配合「显示所有字符」更直观哟！

## 高级玩法

这个就适用于需求较高的用户．

### 宏

宏可以帮助你完成许多重复的工作，例如，将奇数行的「abcde」改为「afce」，需要两步．

#### 录制宏

![npp-macro-rec](./images/npp-macro-rec.gif)

#### 使用宏

![npp-macro-use](./images/npp-macro-use.gif)

#### 大量处理，重复使用

如果是更多行呢？操作就需要一点改变．

首先是录制，一定要先按键盘上的 `HOME` 或 `END` 键将光标移动到行首或行尾，然后用方向键调整横向位置，再进行更改．最后一定要用方向键将光标移动到下一个要处理的行．

比如刚刚的例子，可以先按 `END` 键，然后依次按 `←`，`Backspace`,`←`,`Backspace`,`F`，最后按两下 `↓`，最后停止录制．

然后是重播，先定位到第一个要处理的行（第 3 行），然后点击「宏」->「重复运行宏」．在弹出窗口设置要运行的宏（刚录制的一般是第一个），设置运行次数（或者直接运行到文件尾），点确定即可．

#### 保存宏

点击「宏」->「保存录制宏」，并设置名称和快捷键，即可保存，方便后续使用．

### 插件

#### 插件管理

打开功能栏的「插件」按钮，列表中会显示所有你安装过的插件．

再选择「插件管理」选项，即可管理你的插件．

#### 安装插件（商店）

1.  打开「可用」选项卡，在列表中勾选你所要的插件
2.  点击右上角的「安装」按钮，按照提示重启软件即可．

#### 安装插件（手动）

1.  下载插件（由第三方托管的官方地址：<https://sourceforge.net/projects/npp-plugins/>）注意一定要选择 **与安装 Notepad++ 时处理器架构相同** 的插件．
2.  找到一个名为 "XXX.dll" 的文件（通常以插件名命名）．
3.  在 Notepad++ 中的功能栏点插件，并在列表中点「打开插件文件夹」．
4.  将刚才找到的 DLL 文件放入文件夹中，重启 Notepad++．
5.  【可选】删除刚才拷贝的文件，**但不要删除生成的文件夹！**

Tips: 如果多次不成功，可以尝试新建一个与插件名相同的文件夹在将 ".dll" 文件放入创建的文件夹中

#### 更新插件

在插件管理中，选择「更新」选项卡，并勾选要更新的插件，然后点右上角的「更新」按钮．

#### 移除插件

同样在插件管理中，选择「已安装」选项卡，并勾选要移除的插件，然后点右上角的「移除」按钮．

### 搭建开发环境

不只是编辑器！"Notepad++" 可谓神一样的存在，它可以通过傻瓜式地编译代码，甚至代替 IDE！这里以 C++ 为例

1.  安装编译器并将其必要的文件目录添加到 PATH 环境变量中．（C++ 需要添加 %APPPATH%\bin）当你在 cmd 中输入 g++ 时不再提示'g++'不是内部或外部命令……即可（中间可能需要重启电脑）．推荐 [下载 ConsolePauser](https://sourceforge.net/projects/orwelldevcpp/files/Tools/ConsolePauser.exe/download) 然后随便放并将其目录添加到环境变量（此为 Dev-C++ 的插件，在 Dev-C++ 软件根目录也有）．

2.  在菜单栏中选择「运行」->「运行……」，打开「运行」窗口．

3.  分别输入以下命令

    ```shell
    #编译命令：
    cmd /c g++.exe -o $(CURRENT_DIRECTORY)\$(NAME_PART).exe $(FULL_CURRENT_PATH)
    #运行命令：
    cmd /c $(CURRENT_DIRECTORY)\$(NAME_PART).exe $(FULL_CURRENT_PATH) & pause
    #调试命令：
    cmd /c gdb $(CURRENT_DIRECTORY)\$(NAME_PART).exe

    #如果下载了ConsolePauser可以使用下列代码获得更好的程序运行体验！（注意添加环境变量！）

    #编译命令：
    cmd /c (start ConsolePauser "g++.exe -o $(CURRENT_DIRECTORY)\$(NAME_PART).exe $(FULL_CURRENT_PATH)")
    #运行命令：
    cmd /c (start ConsolePauser "$(CURRENT_DIRECTORY)\$(NAME_PART).exe")
    #调试命令：
    cmd /c (start ConsolePauser "gdb $(CURRENT_DIRECTORY)\$(NAME_PART).exe")
    ```

4.  单击「保存」，名字可以自己取，如 "Compile","Run" 等，然后设定好你想要的快捷键（捡好记的来，如 Dev-C++ 就分别是 `F9` 和 `F10`）．

5.  Enjoy it!

## 小彩蛋

1.  在运行安装程序时你会在下方看到这样一句话：

    > "The best things in life are free. Notepad++ is free. So Notepad++ is the best(.)"
    >
    > （生活中最好的事情都是免费的．Notepad++ 是免费的．所以 Notepad++ 是最好的．）

    这牛吹的，不得不说，很有底气．

2.  在一个新开的页面中输入 "random" 并选中，再按 `F1` 就会得到一句很有意思的话．


## tools/editor/sublime.md

## 简介

Sublime Text（以下简称 ST，后附数字作为版本区分，如无则各版本都适用）是一款轻量级的文本编辑器，支持多种语言的语法高亮及代码补全．具有高度的可拓展性以及 Vim 模式，特别的热启动模式大幅减小了文件丢失的可能．

新版 NOI Linux 中支持版本为 ST3 最后一个版本 3.2.2[^ref1]，故这里以 ST3 为主．目前 ST4 正式版已经发布[^ref2]，现在如仍使用 ST3 会提示更新．

ST4 与 ST3 的重要差别会有额外补充，在介绍中如果提及某项在 ST3 已有翻译则使用中文，否则为 ST4 中的英文．

## 安装

ST4 的安装方法参见 [Sublime Text 4 的下载页面](https://www.sublimetext.com/download)．

ST3 的安装方法参见 [Sublime Text 3 的下载页面](https://www.sublimetext.com/3)．

???+ note "提示购买"
    ST 是收费软件，但有一个无限期的试用，试用并不会带来功能上的缺失，但会不时弹出弹窗提示激活．

## 插件与自定义

### 汉化

ST 并不支持中文，如需中文需要安装汉化插件．

#### 安装插件管理器

打开 ST 后键入<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd>唤出命令框，输入 `Install` 后回车（完整命令是 `Install Package Control`，不区分大小写），此时应该会看到左下角有一个 `=` 在不停的左右移动．Package Control 安装完成（或失败）后会有弹窗提示，具体的加载时间取决于网络．

如果完成的弹窗显示安装失败（与网络有关），则需要手动下载 [Package Control](https://packagecontrol.io/Package%20Control.sublime-package) 并将下载好的文件放到 ST 的数据目录下的 `\Installed Packages` 文件夹中．稍作等待，ST 会自动识别该插件（有时需要重启 ST）．

???+ note "ST 数据目录的路径"
    Windows 下，如果在 ST 的 **安装目录** 下存在 `\data` 文件夹，会自动使用（或初始化）该文件夹作为数据目录．
    
    ST3 的路径一般为 `C:\Users\用户名\AppData\Roaming\Sublime Text 3`，ST4 一般为 `C:\Users\用户名\AppData\Roaming\Sublime Text`，ST 会先寻找对应版本的路径，如不存在则寻找更低版本的路径，如都不存在则新建并初始化．
    
    在以 NOI Linux 所使用的 Ubuntu 20.04.1 中，ST3 的数据目录为 `$HOME/.config/sublime-text-3`，ST4 的数据目录为 `$HOME/.config/sublime-text`，使用的具体规则同 Windows 环境．
    
    可以使用 `首选项->浏览插件目录...` 快速查看数据文件夹路径下的 `\Packages` 文件夹．

#### 安装汉化插件

再次按下<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd>输入 `Install` 后回车（完整命令是 `Package Contrl:Install Package`），等待加载完成，接下来应该是这个界面：

![](./images/sublime3-1.png)

输入 `Chinese` 选择 ChineseLocalizations 并回车，等待安装完毕，完成后界面会自动切换为中文（如是 ST4，因为汉化插件未更新，会少一些新增的菜单项，但一般对编辑无影响）．

### 调整字体

进入 `首选项->设置`，在右边的用户设置中的花括号中添加一行 `"font_face": "字体名",`，ST 的设置使用 JSON 格式储存．修改完成后保存，如果系统安装了对应字体会自动切换．

一般而言，如果单论对中文的显示的话，Microsoft Yahei Consolas 和 Microsoft YaHei Mono 是比较好的选择．

???+ warning "Warning"
    注意任何设置（包括插件设置）即使能也不要在左边的默认设置中修改，这是不被推荐的，如果软件（或插件）更新，默认设置会被重置．

### 安装插件与主题

安装插件与主题的方法与安装汉化插件一致．

输入<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd>输入 `Install` 后回车，然后搜索插件/主题/配色即可．

插件推荐：

-   BracketHighlighter : 对原版的括号高亮进行了增强，必备．
-   C++ Snippets : ST 自带有 C++ 代码补全，格式为大括号不换行．如果不习惯自带大括号换行的码风可以安装这个插件，同时增加了一部分补全．
-   C++ 11 : 支持 C++ 11 标准高亮（ST4 中不需要）．
-   SublimeAstyleFormatter : Astyle，用于格式化代码．
-   Diffy : 按<kbd>Ctrl</kbd>+<kbd>K</kbd>&<kbd>Ctrl</kbd>+<kbd>D</kbd>即可快速比较第一视窗与第二视窗打开的文件的不同，比较方式为逐行比较．
-   ConvertToUTF8 : 自动识别文件编码，并支持编码转换．
-   SideBarEnhancements : 侧边栏增强，较为推荐．
-   Transparency : 窗口透明化．

有其他需要可以尝试搜索．

一些主题：[^ref3]

1337（单配色方案）、3024（单配色方案）、Grandson-of-Obsidian（单配色方案）、Seti\_UI（单主题，额外包含 git 等格式的高亮，较为推荐）、Material Theme、Predawn、Agila、Materialize．

如果要编辑自己的配色方案，可以访问 [tmTheme Editor](http://tmtheme-editor.herokuapp.com/)．

如是 ST4 则可以在 `Preferences->Customize Color Scheme` 中调整配色方案或 `Preferences->Customize Scheme` 中调整主题．

### 开启 Vi Mode

ST 的开发者为 Vi 使用者提供了一个可选插件 Vintage，可模拟 Vi 的大部分功能．

#### 开启方式

Vintage 插件默认是禁用的．可以通过 `首选项->设置` 在用户设置中，将 `"ignored_packages"` 一项中的 Vintage 删除并保存（不要整个删除，只删除 Vintage），ST 的状态栏左边就会出现 `INSERT MODE`，此时 Vintage 插件已开启．

或者按<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd>，然后输入 `Enable` 选择 `Package Control: Enable Package` 并回车，选择 Vintage 即可，该方法需要 Package Control．

#### 相关配置

如果想让上下左右键失效，可以在 `首选项->快捷键设置` 中添加：

```JSON
{ "keys": ["left"], "command": ""},
{ "keys": ["right"], "command": ""},
{ "keys": ["up"], "command": ""},
{ "keys": ["down"], "command": ""},
```

如要使 ST 以命令模式启动，则可以在 `首选项->设置` 中添加：

```json
"vintage_start_in_command_mode": true,
```

也可以通过快捷键设置将进入命令模式设置成任意键（具体详见 [设置快捷键](#设置快捷键)）．

#### 与 Vi 的不同

ST 的 Vintage 插件与 Vi 有一定不同，部分列于此处：

-   在插入模式下用选中不会进入可视模式，这时输入不会被识别为命令而是直接替换文本．可视模式只有命令模式下才能进入．
-   `r`、`R`、`zA`、`za`、`zi`、`z=`、`@` 与使用<kbd>\[</kbd>、<kbd>]</kbd>或<kbd>"</kbd>键的命令不存在．
-   使用<kbd>Ctrl</kbd>、<kbd>Shift</kbd>和<kbd>Alt</kbd>键的快捷键会保留为 ST 设置的快捷键，如<kbd>Ctrl</kbd>+<kbd>V</kbd>不会进入可视模式而是正常粘贴．
-   命令行模式只保留了 `:e`、`:0`、`:$`、`:s`．
-   使用 `\` 与 `?` 命令会自动唤出搜索框，而不是直接在命令中键入单词进行搜索．同时，数字将无法生效．
-   `q` 宏录制命令会启动 ST 自带的宏录制，按<kbd>Q</kbd>后需要再按一个键启动录制，但录制的宏不会与该键绑定，需要按<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>Q</kbd>才能启动．如果需要保存，需要 `工具->保存宏`，快捷键需要设置．
-   无法使用 `数字+.` 的组合．

### 设置

#### 设置 ST

在 `首选项->设置` 中设置，这里列举部分较有用的选项：

```JSON
{
  //字体大小
  "font_size": 11,
  
  //字体，可以不设置，默认为 Consolas
  "font_face": "",
  
  //Tab自动转换为空格
  "translate_tabs_to_spaces": true,
  
  //缩进宽度
  "tab_size": 4,
  
  //行高亮
  "highlight_line": true,
  
  //保存时自动在文件尾增加换行
  "trim_trailing_white_space_on_save": true,
  
  //在选择时查找自动只查找选择范围
  "auto_find_in_selection": true,
  
  //禁用了OI中不太可能用到的插件，可以自己调整
  "ignored_packages": [
    "ActionScript", "AppleScript", "ASP", "Batch File", "C#", 
    "Clojure", "CSS", "D", "Diff", "Erlang", "Git Formats", 
    "Go", "Graphviz", "Groovy", "Haskell", "HTML", "Java", 
    "LaTeX", "Lisp", "Lua", "Makefile", "Matlab", 
    "Objective-C", "OCaml", "Perl", "PHP", "Python", 
    "R","Rails", "RestructuredText", "Ruby", "Rust", 
    "Scala", "ShellScript", "SQL", "TCL", "Textile", "XML", 
  ],
  
  //相对行号，可配合 Vintage 插件快速跳转
  "relative_line_numbers": false,
}
```

#### 设置快捷键

在 `首选项->快捷键设置` 中设置，在左边找到需要修改的功能，然后复制到右边并修改按键即可．

例如，如果要把<kbd>Ctrl</kbd>+<kbd>B</kbd>的编译改为<kbd>F9</kbd>（如果不令原有的快捷键失效，实际是增加一个触发方式），则可以在 `首选项->快捷键设置` 中添加：

```JSON
//将build命令改为f9
{ "keys": ["f9"], "command": "build" },

//将原有的f9对应的行排序功能的快捷键改为shift+f9，由于大部分时候这个功能用不到，这一行也可以不添加
{ "keys": ["shift+f9"], "command": "sort_lines", "args": {"case_sensitive": false} },
```

#### 设置插件

插件的设置可以在 `首选项->Package Setting->插件名` 中找到，做修改时请注意不要修改默认设置．

例如，这里给出 BracketHighlighter 的一些设置，在 `首选项->Package Setting->BracketHighlighter->Bracket Setting` 中修改：

```JSON
{
  //在匹配的括号之间行的行首显示一条线，可以快速找到括号的范围
  "content_highlight_bar": true,
  
  //在小地图中显示匹配的括号
  "show_in_minimap": true,
  
  //忽略匹配范围限制
  "ignore_threshold": true,
  
  //style高亮样式，bold为块高亮，underline为加粗下划线，outline为外围一圈
  //color为颜色，默认设置中已经包含了所有支持的颜色
  //icon为在侧边栏显示的标志
  "bracket_styles": {
    "default": {"icon": "dot", "color": "region.yellowish", "style": "bold",},
    "unmatched": {"icon": "question", "color": "region.redish", "style": "outline",},
    "curly": {"icon": "curly_bracket", "color": "region.purplish",},
    "round": {"icon": "round_bracket", "color": "region.yellowish",},
    "square": {"icon": "square_bracket", "color": "region.bluish",},
    "angle": {"icon": "angle_bracket", "color": "region.orangish",},
    "tag": {"icon": "tag", "color": "region.orangish",},
    "c_define": {"icon": "hash", "color": "region.yellowish",},
    "single_quote": {"icon": "single_quote", "color": "region.greenish",},
    "double_quote": {"icon": "double_quote", "color": "region.greenish",},
    "regex": {"icon": "star", "color": "region.greenish",}
  }
}
```

### 修改与添加

有时候，插件的某些地方可能并不尽如人意，或想对插件进行汉化，这时就需要对插件做一些修改．

插件存放的位置是数据目录下的 `\Installed Packages` 文件夹．

里面的文件以 `.sublime-package` 为后缀，实际上为 `.zip` 格式，可以使用解压缩软件打开．

例如，如果要修改自动补全，可以打开 ST 的 **安装目录** `\Packages\C++` 插件中的 `\Snippets\*.sublime-snippet` 文件修改，如要 **增添** 自动补全，可以安装 C++ Snippets 并在其中修改或添加文件（或新建一个插件，但不能直接添加进自带的 C++ 插件，否则无法被识别）．保存任何修改时 **必须** 关闭 ST，且请提前做好备份，否则可能出现文件丢失．

当然，任何增添都可以放在数据目录路径下的 `\Packages\User\` 下，这总是被支持的．

例如，一个文件模板的补全可以这么写：

```XML
<snippet>
  <description>template_code</description> <!-- 这里的内容是补全内容的预览 -->
  <content><![CDATA[#include <cstdio>
using namespace std;

int main() {
  freopen("${1:file name}.in", "r", stdin);
  freopen("$1.out", "w", stdout);
  ${0:/* code */}
  fclose(stdin);
  fclose(stdout);
  return 0;
}]]></content>
  <tabTrigger>code</tabTrigger> <!-- 这里的内容是补全的触发文本 -->
  <scope>source.c++</scope> <!-- 这里的内容是补全适用语言 -->
</snippet>
```

以下列出部分文件后缀以及其用途，具体的插件开发教程详见 [社区文档](https://docs.sublimetext.io/guide/extensibility/plugins/) 和 [官方文档](https://www.sublimetext.com/docs/3/)：

| 后缀名                  | 用途                             |
| -------------------- | ------------------------------ |
| .sublime-build       | 编译系统文件                         |
| .sublime-completions | 文件名补全列表（一般为头文件）                |
| .sublime-syntax      | 语法高亮文件                         |
| .sublime-settings    | 设置文件                           |
| .tmPreferences       | 首选项中的列表文件                      |
| .sublime-keymap      | 快捷键设置文件                        |
| .sublime-snippet     | 代码补全文件                         |
| .sublime-commands    | 命令定义文件                         |
| .sublime-menu        | ST UI 文件，包括侧边栏以及顶部菜单栏（汉化的主要对象） |

由于插件更新会直接覆盖原文件，所以建议备份更改的文件．

## 编辑

### 设置语法

按<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd>后输入语法即可，或者按右下角的 `Plain Text` 然后修改为需要的语言，同时在 `视图->语法` 中也可以设置．

![](images/sublime3-2.png)

### 快捷键

ST 有复合快捷键，如<kbd>Ctrl</kbd>+<kbd>K</kbd>&<kbd>Ctrl</kbd>+<kbd>Backspace</kbd>表示先按<kbd>Ctrl</kbd>+<kbd>K</kbd>再按<kbd>Ctrl</kbd>+<kbd>Backspace</kbd>．

部分快捷键：

| 按键                                                                         | 命令                                                            |
| -------------------------------------------------------------------------- | ------------------------------------------------------------- |
| <kbd>Ctrl</kbd>+<kbd>X</kbd>                                               | 剪切当前行                                                         |
| <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>K</kbd>                              | 删除行                                                           |
| <kbd>Ctrl</kbd>+<kbd>Enter</kbd>                                           | 在下方插入行                                                        |
| <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>Enter</kbd>                          | 在上方插入行                                                        |
| <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>Up</kbd>                             | 行上移                                                           |
| <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>Down</kbd>                           | 行下移                                                           |
| <kbd>Ctrl</kbd>+<kbd>L</kbd>                                               | 选择行，重复以向下选择多行                                                 |
| <kbd>Ctrl</kbd>+<kbd>D</kbd>                                               | 选择词，重复以选择多个相同词，并进入多重选择模式（用于快速批量更改）                            |
| <kbd>Ctrl</kbd>+<kbd>M</kbd>                                               | 跳转到匹配的括号                                                      |
| <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>M</kbd>                              | 选择括号内的内容（不包括括号），重复以包括括号                                       |
| <kbd>Ctrl</kbd>+<kbd>K</kbd>&<kbd>Ctrl</kbd>+<kbd>K</kbd>                  | 删至行尾（复合快捷键，建议使用 Vim 模式代替）                                     |
| <kbd>Ctrl</kbd>+<kbd>K</kbd>&<kbd>Ctrl</kbd>+<kbd>Backspace</kbd>          | 删至行首（复合快捷键，建议使用 Vim 模式代替）                                     |
| <kbd>Ctrl</kbd>+<kbd>]</kbd>                                               | 缩进当前（选择的）行                                                    |
| <kbd>Ctrl</kbd>+<kbd>\[</kbd>                                              | 取消缩进当前（选择的）行                                                  |
| <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>D</kbd>                              | 复制当前行，并插入在下一行                                                 |
| <kbd>Ctrl</kbd>+<kbd>J</kbd>                                               | 合并下一行与当前行                                                     |
| <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>V</kbd>                              | 粘贴并缩进（用于整段粘贴代码）                                               |
| <kbd>Ctrl</kbd>+<kbd>K</kbd>&<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>V</kbd> | 从历史粘贴（复合快捷键，建议修改为<kbd>Ctrl</kbd>+<kbd>Alt</kbd>+<kbd>V</kbd>） |
| <kbd>Ctrl</kbd>+<kbd>Alt</kbd>+<kbd>Down</kbd>                             | 光标下移，并保留当前行光标（进入多重选择模式）                                       |
| <kbd>Ctrl</kbd>+<kbd>Alt</kbd>+<kbd>Up</kbd>                               | 光标上移，并保留当前行光标（进入多重选择模式）                                       |
| <kbd>Ctrl</kbd>+<kbd>R</kbd>                                               | 跳至文件中的任意符号（函数或类型定义）                                           |
| <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>R</kbd>                              | 跳至项目中的任意符号（函数或类型定义）                                           |
| <kbd>Ctrl</kbd>+<kbd>P</kbd>                                               | 跳至任意文件（曾经打开过或在项目中且存在的文件）                                      |
| <kbd>\~</kbd>                                                              | 转换选择内容的大小写                                                    |

### 自动补全

ST 有丰富的补全功能，可能的补全内容会在光标下方显示，按<kbd>Tab</kbd>或<kbd>Enter</kbd>进行补全（ST4 中，如进行一个非 Snippet 类型的补全，接下来再按<kbd>Tab</kbd>可继续选择为以该补全为子串的补全）．

Snippet 类型的补全一般会有一些编辑块，补全后会自动选择为替换文本，如果是 `for` 等含有多个编辑块的复杂补全，编辑完成后再次按<kbd>Tab</kbd>完成下一个编辑块，此时要在编辑块中触发补全需要使用<kbd>Enter</kbd>（在 ST4 中可继续使用<kbd>Tab</kbd>）．

如果没有自动补全，请如下修复：

1.  检查是否切换了语言，ST 默认新建文件为 Plain Text．

2.  进入 `首选项->设置` 然后添上两行：

```JSON
"auto_complete": true,
"auto_match_enabled": true,
```

### 多重选择

按住<kbd>Ctrl</kbd>并用鼠标单击即可在屏幕上增加光标，<kbd>Ctrl</kbd>+<kbd>Alt</kbd>+<kbd>Up</kbd>或<kbd>Ctrl</kbd>+<kbd>Alt</kbd>+<kbd>Down</kbd>可以在相邻两行直接增加光标，任何编辑性质的操作会同时应用至所有光标．

### 查找与替换

<kbd>Ctrl</kbd>+<kbd>F</kbd>为查找，<kbd>F3</kbd>为查找下一个<kbd>Shift</kbd>+<kbd>F3</kbd>为查找上一个，<kbd>Ctrl</kbd>+<kbd>H</kbd>为替换．

五个查找选项分别为正则表达式匹配、大小写敏感、全字匹配、循环查找、在选段中查找．

建议在首选项中将 `"auto_find_in_selection"` 设置为 `true`．这样在选择超过一个词时使用查找会自动只在选段中查找．

## 演示

### 热启动

尝试在 ST 中键入一些内容，并直接把整个 ST 关闭，ST 会直接关闭且没有任何提示，再打开 ST 时只要不对电脑进行数据还原就不会丢失任何数据．

### 多重选择

如果要把以下代码中的所有 `bok` 改为 `book`，只需将光标放置在任意一个 `bok` 中，长按<kbd>Ctrl</kbd>+<kbd>D</kbd>即可快速选中．

```cpp
int check() {
  book[1] = 1, book[2] = 1, book[3] = 1, bok[1] = 1, bok[2] = 1, bok[3] = 1,
  bok[4] = 1, bok[5] = 1;
}
```

如果要将下列文件中的所有等号后面改成 `"good"`，只需在将光标放置于第一行的 `aaa` 前，并按五次<kbd>Ctrl</kbd>+<kbd>Alt</kbd>+<kbd>Down</kbd>，再然后按下<kbd>Ctrl</kbd>+<kbd>D</kbd>并键入 `good` 即可．

或选中 `"a` 并按住<kbd>Ctrl</kbd>+<kbd>D</kbd>，然后按<kbd>Right</kbd>、<kbd>Ctrl</kbd>+<kbd>D</kbd>，之后键入即可．

```cpp
s[1] = "aaa";
s[2] = "aab";
s[3] = "aac";
s[4] = "good";
s[5] = "aae";
s[6] = "aaf";
```

如要为下列所有 `a + b` 加上括号，只需选择一个 `a + b`，按住<kbd>Ctrl</kbd>+<kbd>D</kbd>并键入<kbd>(</kbd>即可（如选择一定区域，则任意左括号键入会为该区域两边添加匹配的括号）．

```plain
a + b*a + b*a + b
```

### 查找与替换

如果要将下列文件中的所有等号后面改成 `"good"`，也可以用<kbd>Ctrl</kbd>+<kbd>H</kbd>使用替换，打开正则，输入 `".*"`，并替换成 `"good"` 即可．

```cpp
s[1] = "aaa";
s[2] = "aab";
s[3] = "aac";
s[4] = "good";
s[5] = "aae";
s[6] = "aaf";
```

如要为以下代码添加分号，只需使用选择区域替换，打开正则，输入 `\n`，并替换成 `;\n` 即可．

```plain
int main() {  int a, b  cin >> a >> b  cout << a + b  return 0}
```

### 宏录制

如要为以下代码添加分号，可以按<kbd>Ctrl</kbd>+<kbd>q</kbd>启动宏录制接下来依次按<kbd>End</kbd>、<kbd>;</kbd>、<kbd>Down</kbd>再按<kbd>Ctrl</kbd>+<kbd>q</kbd>结束宏录制（中途左下角不会全程显示正在录制，但确实在录制），接下来重复<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>q</kbd>即可．

```plain
int main() {
  int a, b
  cin >> a >> b
  cout << a + b
  return 0
}
```

??? note "如已开启 Vintage 插件"
    执行一次<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>q</kbd>后，可以<kbd>Esc</kbd>进入命令模式，输入 `..` 即可（`.` 命令可以重复 ST3 命令）

关于宏的保存与绑定按键详见 [社区文档](https://docs.sublimetext.io/guide/extensibility/macros.html)．

## 编译与运行

ST 的编译环境已经配置好了，可以直接使用．

Windows 环境下需要将 g++ 所在目录添加到环境变量中，并重启 ST．

### 编译

直接按<kbd>Ctrl</kbd>+<kbd>B</kbd>编译，第一次使用会需要选择编译系统，选择 `C++ Single File`（编译）或 `C++ Single File - Run`（编译并运行）．

#### 修改编译选项

ST 默认的编译选项为 `g++ "${file}" -o "${file_path}/${file_base_name}"`，如果要修改编译选项，可以新建一个编译系统．

进入 `工具->编译系统->新建编译系统…` 然后在大括号中间输入：

```JSON
// 编译选项可以自己调整
// 编译并运行
"shell_cmd": "g++ -Wall \"${file}\" -o \"${file_path}/${file_base_name}.exe\" && \"${file_path}/${file_base_name}.exe\"",

// 这一行可以让ST3图形化显示报错，如果习惯了看g++返回的信息可以去掉
"file_regex": "^(..[^:]*):([0-9]+):?([0-9]+)?:? (.*)$",
```

保存后按<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>B</kbd>切换编译系统就可以使用了，这里的配置是编译并在外部 CMD 运行．

保存的文件为数据目录路径下的 `\Packages\User\编译系统名.sublime-build` 可以反复修改．

### 运行

如果编译时选择 `C++ Single File - Run`（即编译后运行）或配置了自动运行，那么在下方弹出的编译信息窗口应该不会有任何显示（除非编译错误），因为 ST 的编译信息窗口实际上是一个终端，可以直接输入数据．

运行结束后会提示程序的运行时间，其计时为从按下<kbd>Ctrl</kbd>+<kbd>B</kbd>到全部 CMD 命令运行结束的时间，也就是说包括编译的时间和输入的时间，以及如果在外部 CMD 运行还包括 CMD 开启关闭的时间．

???+ warning "Warning"
    这个窗口无法输入<kbd>F6</kbd>或<kbd>Ctrl</kbd>+<kbd>Z</kbd>，如果运行读入到文件末尾的程序请使用文件输入，或配置在外部 CMD 运行．

### 调试

可以安装插件使 ST 支持图形化 gdb 调试，但不建议依赖插件进行 gdb 调试．

更好的做法是在配置编译系统时加上相关命令启动 gdb，在外部进行命令行调试．

## 杂项

-   把文件夹拖进 ST 中并按<kbd>Ctrl</kbd>+<kbd>K</kbd>&<kbd>Ctrl</kbd>+<kbd>B</kbd>开启侧边栏，从而快速切换文件．
-   善用跳转功能，尤其是<kbd>Ctrl</kbd>+<kbd>P</kbd>进行文件间跳转与<kbd>Ctrl</kbd>+<kbd>R</kbd>进行函数跳转．
-   ST 支持 git[^ref4]．
-   ST 的所有配置储存在数据目录下，可以随意打包，但注册信息无法在多台电脑上使用．

## 外部链接

-   [使用命令行调试](../cmd.md)
-   [Sublime Text 3 官方文档](https://www.sublimetext.com/docs/3/)
-   [Sublime Text 社区文档](https://docs.sublimetext.io/)

## 参考资料与注释

[^ref1]: [NOI Linux 2.0 发布](https://www.noi.cn/gynoi/jsgz/2021-07-16/732450.shtml)

[^ref2]: [Sublime Text 4 发布](https://www.sublimetext.com/blog/articles/sublime-text-4)

[^ref3]: [便捷清新的文本编辑器 sublime](https://www.luogu.com.cn/blog/acking/sublime)

[^ref4]: [Sublime Text Git 集成](https://www.sublimetext.com/docs/git_integration.html)


## tools/editor/vim.md

author: Enter-tainer, ouuan, Xeonacid, Ir1d, partychicken, ChungZH, LuoshuiTianyi, Kewth, s0cks5, Doveqise, StudyingFather, SukkaW, SodaCris, SkyeYoung, 383494, danielqfmai

Vim - 无处不在的文本编辑器．

## 简介

Vim 是从 vi 发展出来的一个文本编辑器．其代码补完、编译及错误跳转等方便编程的功能特别丰富，在程序员群体中被广泛使用．

## 安装

Linux 系统通常自带 Vim，打开终端输入 `vim` 即可启用．

若需手动安装，Vim 的 [官方网站](https://www.vim.org/) 提供了下载的 [说明文档](https://www.vim.org/download.php)，按照需求编译安装即可．

## Vim 的模式与常用键位

Vim 的基础操作在 Vim 自带的教程里将会讲述．打开终端输入 `vimtutor` 即可进入教程．

这些操作通常需要二三十分钟来大致熟悉．

### 命令模式 (Command Mode)

进入 Vim 后的默认模式．

此状态下敲击键盘动作会被 Vim 识别为命令，而非输入字符，比如我们此时按下<kbd>i</kbd>，并不会输入一个字符，<kbd>i</kbd>被当作了一个命令．

Vim 的方向键是<kbd>↑</kbd>、<kbd>↓</kbd>、<kbd>←</kbd>、<kbd>→</kbd>，或者<kbd>h</kbd>、<kbd>j</kbd>、<kbd>k</kbd>、<kbd>l</kbd>．

```text
        ↑(k)
        ^
(h)← <     > →(l)
        v
        ↓(j)
```

以下是命令模式常用的命令：

-   `i` 切换到输入模式，在光标当前位置开始输入文本．按<kbd>Esc</kbd>键可回到普通模式．
-   `x` 用于删除光标后的一个字符．
-   `:` 切换到底线命令模式，以在最底一行输入命令．
-   `a` 切换到输入模式，在光标后开始输入文本．
-   `o` 切换到输入模式，在光标下插入新的一行；`O` 切换到输入模式，在光标上插入新的一行．
-   `p` 粘贴剪贴板内容到光标下方；`P` 粘贴剪贴板内容到光标上方．
-   `dd` 删除光标所在的一整行．
-   `d` 命令也是删除，通常配合其他键使用．
-   `u` 撤销上一次对文本的更改．
-   `y` 命令可以复制被选中的区域．需要按 `v` 进入可视模式操作．
-   `yy` 复制当前行．
-   `Ctrl + r` 重做上次撤销的操作．
-   `:w` 保存文件，常配合 q 保存退出．
-   `:q` 退出 Vim．
-   `:q!` 强制退出 Vim，不保存修改．

部分其他命令：

-   `c` 命令用于修改，相当于 `di`．
-   `=` 命令可以以默认格式对选中行应用自动缩进．
-   `==` 自动缩进当前行．
-   `.` 命令可以重复上次执行的命令．
-   `gg` 命令可跳至代码的开头；`G` 命令可跳至代码最后一行的开头；`G` 命令前加数字可跳至指定行．
-   `w` 可以跳到下个单词的开头；`e` 可以跳到当前单词或下一单词的结尾；`b` 可以跳到当前单词或上一单词的开头；`0` 可以跳至行首；`$` 可以跳至行尾．`w`、`e`、-`0`、`$` 还可以与其他命令组合，比如 `de`、`dw`、`d0` 和 `d$` 分别对应删至单词尾、删至下个单词头、删至行首和删至行尾．

命令模式下按<kbd>/</kbd>，下方即会出现查找框，输入需要查找的字符，按回车后就能查看搜索结果．如果有多个查找结果，按<kbd>n</kbd>即可跳至下一个查找结果；按<kbd>N</kbd>可跳至上一个．

命令模式下按<kbd>\*</kbd>可以查找当前光标下的单词．

在输入某个命令前，输入一个数字 n 的话，命令就会重复 n 次．

### 输入模式 (Insert Mode)

在命令模式下按下<kbd>i</kbd>就进入了输入模式，按<kbd>Esc</kbd>键可以返回到命令模式．

在输入模式中，可以使用以下按键：

-   字符按键以及<kbd>Shift</kbd>组合，输入字符
-   <kbd>ENTER</kbd>，回车键，换行
-   <kbd>BACK SPACE</kbd>，退格键，删除光标前一个字符
-   <kbd>DEL</kbd>，删除键，删除光标后一个字符
-   方向键，在文本中移动光标
-   <kbd>HOME/END</kbd>，移动光标到行首/行尾
-   <kbd>Page Up/Page Down</kbd>，上/下翻页
-   <kbd>Insert</kbd>，切换光标为输入/替换模式，光标将变成竖线/下划线
-   <kbd>ESC</kbd>，退出输入模式，切换到命令模式

在输入模式下按<kbd>Ctrl</kbd>+<kbd>o</kbd>即可进入「输入 - 命令模式」，执行完一次操作后又会自动回到输入模式．

### 底线命令行模式

命令模式下按<kbd>:</kbd>，进入底线命令模式．

底线命令模式可以输入单个或多个字符的命令，可用的命令非常多．

在底线命令模式中，基本的命令有：

-   `:help`/`:h` 查看英文版 Vim 在线帮助文档．
-   `:w` 保存文件．
-   `:q` 退出 Vim．
-   `:wq` 保存文件，退出 Vim．
-   `:q!`/`:!q` 强制退出 Vim，不保存修改．
-   `:e filename` 可以打开当前目录下的指定文件．
-   `:s` 命令是替换．

```vim
" 把当前行第一个匹配的 str1 替换成 str2
:s/str1/str2/
" 把当前行所有的 str1 替换成 str2
:s/str1/str2/g
" 把当前行所有的 str1 替换成 str2，在替换前询问
:s/str1/str2/gc
" 把第 x1 行至 x2 行中，每一行第一个匹配的 str1 替换成 str2
:x1,x2 s/str1/str2/
" 把第 x1 行至 x2 行中所有的 str1 替换成 str2
:x1,x2 s/str1/str2/g
" 第 x1 行至 x2 行中所有的 str1 替换成 str2，在替换前询问
:x1,x2 s/str1/str2/gc
" 把所有行第一个匹配的 str1 替换成 str2
:%s/str1/str2/
" 把全文件所有的 str1 替换成 str2
:%s/str1/str2/g
" 把全文件所有的 str1 替换成 str2，在替换前询问
:%s/str1/str2/gc
```

如果命令形式是 `:! command`，则命令将在 bash 终端执行．

按<kbd>Esc</kbd>键可以退出底线命令模式．

### 可视模式 (Visual mode)

按 `v` 进入可视模式，多用于选中区域．按 `V`（`Shift+v`）进入行可视模式，用于选中行．

按<kbd>Ctrl</kbd>+<kbd>v</kbd>或<kbd>Ctrl</kbd>+<kbd>q</kbd>进入块可视模式 (visual block)．

进入块可视模式后，按<kbd>I</kbd>或<kbd>A</kbd>进入插入模式（相当于 `i` 和 `a`），退出插入模式后对本行所做的改动将被应用到选中的每一行同一位置．常用于批量添加注释．

选中后输入 `y` 或 `d` 亦可执行相应命令．

三种可视模式可以通过按键相互转化．

## Vim 的快捷键

可参考 [史上最全 Vim 快捷键键位图—入门到进阶](https://cenalulu.github.io/linux/all-vim-cheatsheat/)

## 进阶知识

### `.` 命令

Vim 的使用者不可避免地会抗拒重复的文本修改，因为 Vim 注定比其他编辑器会多出两次按键——<kbd>Esc</kbd>与<kbd>i</kbd>．但是，Vim 其实提供了重复命令 `.`，它适用于重复的添加、修改、删除文本操作．

`.` 命令可以重复上次执行的命令．但是这个「命令」并不只限于单一的命令，它也可以是 `数字 + 命令` 的组合；`进入插入模式 + 输入文本 + Esc` 也是命令的一种．所以，适当使用 `.` 命令才能达到最高的效率．

例如，如下代码的每一行末尾都少了分号：

```text
int a, b
cin >> a >> b
cout << a + b
return 0
```

将 `.` 与搭配移动到行尾插入命令 `A` 使用，就能高效地补上末尾的分号．

```vim
A;<Esc>
" 重复下面的命令
j.
```

再例如，如下代码中，后面五个赋值语句的数组名全部写错了：

```cpp
int check() {
  book[1] = 1, book[2] = 1, book[3] = 1, bok[1] = 1, bok[2] = 1, bok[3] = 1,
  bok[4] = 1, bok[5] = 1;
  return 0;
}
```

一个个改过于麻烦，而命令行模式的 `s` 命令又会全部改掉．

第一种改法是搭配普通模式下的 `s` 命令（删除光标处字符并进入插入模式）使用．来到第一个错误的数组名首字母处，按下 `3s`/`cw`，输入正确的数组名并退出．之后把光标一个个移过去，再使用 `.` 命令．

第二种比较节省时间的改法是利用查找模式修改．键入 `/bok`，接着按下回车，并使用 `n` 键来到第一个错误的数组名首字母处，键入 `3s 新数组名 <Esc>`，最后重复 `n.`．

第三种改法是简易查找命令 `f`．在一行中普通模式下，`f + 单个字符` 即可查找此行中出现的这个字符并将光标移至字符处；按 `;` 查找下一个，`,` 查找上一个．所以对于上面的代码，只需键入 `fb;;;` 之后进入插入模式修改，然后 `;.` 即可．这种改法适用于只需行内移动的情况．

### 宏

Vim 的宏功能可以重复任意长的命令．

使用宏之前要先「录制」，即把一串按键操作录下来再回放，这样就达到了重复的效果．录制的方法很简单，普通模式下键入 `q` 开始录制．下一步，为录制的宏指定一个执行的命令键，可以按下 26 个字母中的任意一个来指定．这时左下方会显示 `记录中 @刚刚选择的字母`．然后就可以开始录制命令了．同理，普通模式下按 `q` 暂停录制．

使用方法为按下 `:` 进入命令行模式，键入 `@选择的记录字母`，然后之前录制的命令就被调用了．

将 `.` 和宏组合，即录制宏 → 调用宏 →`.` 重复命令 → 数字 +`.`，可以达到非常高的效率．

### normal 命令

该命令与普通模式有关，效果是在指定行重复命令．

按 `:` 进入命令行模式，输入如下命令：

```vim
:a,b normal command
```

或者：

```vim
:a,b norm command
```

以上命令的意思是在普通模式下，对 a\~b 行执行 `command` 命令．

由于 `normal` 命令可以被 `.` 命令重复调用，且其易于理解，它的使用频率甚至更高于宏．

### 数字 +`.`+ 宏 + normal

以上三种命令可以组合使用．例如：

> 我下载了一本书，我需要它的每一个章节都变成「标题」，以方便转换成 mobi 之类的格式，或者方便生成 TOC 目录跳转，怎么办呢？

以下是用 Vim 处理的过程：

1.  按下<kbd>/</kbd>调出查找框，输入正则表达式进行查找；
2.  用 `q` 命令开始录制宏；
3.  键入 `I#` 命令，然后按下<kbd>ESC</kbd>；
4.  用 `q` 命令结束宏录制；
5.  键入 `normal n@字母` 转到下一处并重复上一步操作；
6.  键入 `数字 + .` 多次重复．

## 外部链接

-   [Vim 官网](https://www.vim.org/)
-   [原作者提供的配置](https://github.com/LuoshuiTianyi/Vim-for-OIWiki)
-   [Vim 调试：termdebug 入门](https://fzheng.me/2018/05/28/termdebug/)
-   [Vim scripting cheatsheet](https://devhints.io/vimscript)
-   [Learn Vimscript the Hard Way](https://learnvimscriptthehardway.stevelosh.com)
-   [Linux vi/vim | 菜鸟教程](https://www.runoob.com/linux/linux-vim.html)


## tools/editor/vscode.md

author: NachtgeistW, Ir1d, ouuan, Enter-tainer, Xeonacid, ChungZH, keepthethink, abc1763613206, partychicken, Chrogeek, xkww3n, HeliumOI, Pinghigh, xiaofu-15191, Sekakou, fuxianhu

## 简介

Visual Studio Code（以下简称 VS Code）是一个由微软开发，同时支持 Windows、Linux 和 macOS 等操作系统且开放源代码的代码编辑器．它是用 TypeScript 编写的，并且采用 Electron 架构．它带有对 JavaScript、TypeScript 和 Node.js 的内置支持，并为其他语言（如 C、C++、Java、Python、PHP、Go）提供了丰富的扩展生态系统．

官网：[Visual Studio Code - The open source AI code editor](https://code.visualstudio.com/)

在阅读以下内容前，建议你先简单了解 VS Code 的基本使用方法：[开始使用 Get started](https://code.visualstudio.com/docs/getstarted/getting-started)．

## 使用 C/C++ Compile Run 扩展运行代码

C/C++ Compile Run 是一个专注于 C/C++ 单文件编译与运行的插件．它免去了传统 C/C++ 插件中繁琐的配置步骤，非常适合编程竞赛的需要，上手迅速，操作简单．

打开 VS Code，点击左侧边栏的「扩展」图标（或按下<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>X</kbd>），在搜索框中输入 `C++`，找到 C/C++ Compile Run，点击「安装/Install」即可．

![](./images/vscode-14.png)

安装完成后，无需额外配置，插件会根据环境变量自动适配已配置好的 MinGW 编译器．

打开需要运行的文件，点击右上角的三角图标即可运行代码．

快捷键：

-   <kbd>F6</kbd>- 编译并在 VS Code 内置集成终端中运行
-   <kbd>F7</kbd>- 以自定义参数编译并以自定义参数在 VS Code 内置集成终端运行
-   <kbd>F8</kbd>- 编译并在外部终端中运行

## 使用 Code Runner 扩展运行代码

VS Code 安装并配置扩展后可实现对 C/C++ 的支持，但配置过程比较复杂．一个简单的编译与运行 C++ 程序的方案是安装 Code Runner 扩展．

Code Runner 是一个可以一键运行代码的扩展，在工程上一般用来验证代码片段，支持 Node.js、Python、C、C++、Java、PHP、Perl、Ruby、Go 等 40 多种语言．

安装的方式是在扩展商店搜索 Code Runner 并点击 Install；或者前往 [Marketplace](https://marketplace.visualstudio.com/items?itemName=formulahendry.code-runner) 并点击 Install，浏览器会自动打开 VS Code 并进行安装．

![](./images/vscode-1.jpg)

安装完成后，打开需要运行的文件，点击右上角的小三角图标即可运行代码；按下快捷键<kbd>Ctrl</kbd>+<kbd>Alt</kbd>+<kbd>N</kbd>（在 macOS 下是<kbd>Control</kbd>+<kbd>Option</kbd>+<kbd>N</kbd>）也可以得到同样的效果．

???+ warning "Warning"
    如果安装了 VS Code 与 Code Runner 后，代码仍然无法运行，很有可能是因为系统尚未安装 C/C++ 的运行环境，参考 [Hello, World! 页面](../../lang/helloworld.md) 以安装．
    
    记得勾选设置中的 Run In Terminal 选项，如图：![](./images/vscode-7.png)

## 使用 C/C++ 扩展编译并调试/智能补全代码

### 安装扩展

在 VS Code 中打开扩展商店，在搜索栏中输入 `C++` 或者 `@category:"programming languages"`，然后找到 C/C++，点击 Install 安装扩展．

![](./images/vscode-2.png)

???+ warning "Warning"
    在配置前，请确保系统已经安装了 G++ 或 Clang，并已添加到了环境变量 `PATH` 中．请使用 CMD 或者 PowerShell，而不是 Git Bash 作为集成终端．

### 配置 GDB/LLDB 调试器

#### GDB

在 VS Code 中新建一份 C++ 代码文件，按照 C++ 语法写入一些内容（如 `int main(){}`），保存并按下<kbd>F5</kbd>，进入调试模式．
如果出现了「选择调试器」的提示，选择 `C++ (GDB/LLDB)`．在「选择配置」中，G++ 用户选择 `g++.exe - 生成和调试活动文件`；Clang 用户选择 `clang++ - 生成和调试活动文件`．

???+ warning "Warning"
    配置名称并非固定，而是可以自定义的．不同的操作系统可能具有不同的配置名称．

完成后，VS Code 将自动完成初始化操作在下方的集成终端中启动调试．至此，GDB 所有的配置流程已经完毕．

#### LLDB

如果需要采用 LLDB，需要安装另外一款扩展[^ref1]——[CodeLLDB](https://github.com/vadimcn/vscode-lldb/)．从该项目的 Release 页面下载 .vsix 文件后[^ref2]，从 VS Code 的扩展页面安装．

![](images/vscode-9.png)

先按照上文 GDB 的配置过程操作一遍，然后删除 `.vscode/launch.json`，按下<kbd>F5</kbd>，选择 `LLDB`，再把 `launch.json` 中的 `${workspaceFolder}/<executable file>` 更改为 `${fileDirname}/${fileBasenameNoExtension}` 即可．

至此，LLDB 配置完成．再次按下<kbd>F5</kbd>即可看到软件下方的调试信息．

若要在以后使用 VS Code 编译并调试代码，所有的源代码都需要保存至这个文件夹内．若要编译并调试其他文件夹中存放的代码，需要重新执行上述步骤（或将旧文件夹内的 `.vscode` 子文件夹复制到新文件夹内）．

### 开始调试代码

使用 VS Code 打开一份代码，将鼠标悬停在行数左侧的空白区域，并单击出现的红点即可为该行代码设置断点．再次单击可取消设置断点．

![](images/vscode-5.apng)

按下<kbd>F5</kbd>进入调试模式，编辑器上方会出现一个调试工具栏，四个蓝色按钮从左至右分别代表 GDB 中的 `continue`,`next`,`step` 和 `until`：

![](images/vscode-6.png)

如果编辑器未自动跳转，点击左侧工具栏中的「调试」图标进入调试窗口，即可在左侧看到变量的值．

在「监视」中，你可以输入表达式，在每一次进行 `next` 或 `step` 等操作时都会重新求值并显示．

在「调用堆栈」中，你可以看见当前函数执行的栈帧．

???+ note "Tip"
    你可以参照 [GDB 官方文档](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Arrays.html) 来查看某个数组一段区间内的内容．

在调试模式中，编辑器将以黄色底色显示下一步将要执行的代码．

### 配置 IntelliSense

用于调整 VS Code 的智能补全．

如果你使用 Clang 编译器，在「IntelliSense 模式」中选择 `clang-x64` 而非默认的 `msvc-x64`；如果你使用 G++ 编译器，选择 `gcc-x64` 以使用自动补全等功能．否则会得到「IntelliSense 模式 msvc-x64 与编译器路径不兼容．」的错误．

![](images/vscode-4.png)

## 配置 clangd

???+ warning "Warning"
    由于功能冲突，安装 clangd 扩展后 C/C++ 扩展的 IntelliSense 功能将被禁用（调试等功能仍然使用 C/C++ 扩展）．如果 clangd 扩展的功能出现问题，可以查看是否禁用了 C/C++ 扩展的 IntelliSense 功能．

### clangd 简介

LLVM 官网上对 clangd 的介绍是这样的：

> Clangd is an implementation of the Language Server Protocol leveraging Clang. Clangd’s goal is to provide language "smartness" features like code completion, find references, etc. for clients such as C/C++ Editors.

简单来说，clangd 是 Clang 对语言服务器协定（Language Server Protocol）的实现，提供了一些智能的特性，例如全项目索引、代码跳转、变量重命名、更快的代码补全、提示信息、格式化代码等，并且能利用 LSP 与 Vim、Emacs、VSCode 等编辑器协作．虽然官方给出的定义是 LSP 的实现，但 clangd 的功能更接近语言服务器（Language Server）而不仅仅只是协议本身．

VS Code 的 C/C++ 扩展也有自动补全等功能，但在提示信息的易读程度的准确度等方面与 clangd 相比稍逊一筹，所以我们有时会使用 clangd 代替 C/C++ 扩展来实现代码自动补全等功能．

### 安装

参见 [Getting started](https://clangd.llvm.org/installation)．

### VS Code 扩展

打开 VS Code 扩展商店，在搜索栏中输入 `clangd` 找到 clangd 扩展并安装

![](images/vscode-8.png)

如果下方弹出 clangd 要求关闭 Intellisense 的对话框，点击 "Disable Intellisense"，重新加载工作区，就可以享受 clangd 的自动补全等功能了．

## 编辑

### 语法设置

在新打开的编辑器中点击「选择语言」，即可打开对应的语法高亮，如图：

![](images/vscode-11.apng)

### 快捷键

官方快捷键 PDF 如下，也可以在 VS Code 中按下<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd>打开命令面板并输入命令 `> Help: Keyboard Shortcuts Reference` 打开．[^ref3]

-   [Windows 系统快捷键](https://code.visualstudio.com/shortcuts/keyboard-shortcuts-windows.pdf)
-   [Linux 系统快捷键](https://code.visualstudio.com/shortcuts/keyboard-shortcuts-linux.pdf)
-   [Mac OS 系统快捷键](https://code.visualstudio.com/shortcuts/keyboard-shortcuts-macos.pdf)

部分快捷键：

| 按键                                                            | 操作                        |
| ------------------------------------------------------------- | ------------------------- |
| <kbd>Ctrl</kbd>+<kbd>C</kbd>/<kbd>X</kbd>                     | 复制/剪切当前行（当没有选择内容时）        |
| <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>K</kbd>                 | 删除当前行                     |
| <kbd>Alt</kbd>+<kbd>Up</kbd>/<kbd>Down</kbd>                  | 行上移/下移                    |
| <kbd>Alt</kbd>+<kbd>Shift</kbd>+<kbd>Up</kbd>/<kbd>Down</kbd> | 行向上/向下复制                  |
| <kbd>Ctrl</kbd>+<kbd>/</kbd>                                  | 切换行注释                     |
| <kbd>Ctrl</kbd>+<kbd>\[</kbd>/<kbd>]</kbd>                    | 行向左/右缩进                   |
| <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>\[</kbd>/<kbd>]</kbd>   | 行折叠/展开                    |
| <kbd>Ctrl</kbd>+<kbd>P</kbd>                                  | 打开最近打开的文件                 |
| <kbd>Alt</kbd>+<kbd>Z</kbd>                                   | 切换自动折行                    |
| <kbd>Alt</kbd>+<kbd>F12</kbd>                                 | 速览定义（如函数的定义）              |
| <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>\\</kbd>                | 跳转到匹配括号                   |
| <kbd>Ctrl</kbd>+<kbd>T</kbd>                                  | 在工作区中查找符号（在文件夹中查找指定名称函数等） |

### 多光标

按住<kbd>Alt</kbd>并单击即可在编辑器中添加光标，多数编辑操作都可同时进行；按住鼠标中键并在编辑器中拖动也可添加多行光标，如图：

![](images/vscode-12.gif)

按<kbd>Ctrl</kbd>+<kbd>F2</kbd>可在编辑器中同时更改所有匹配项，也可以在右键菜单中找到 Change All Occurrences，如图：

![](images/vscode-13.gif)

注意此时在右上角会有一个工具栏，可在其中开启查找匹配项时是否开启大小写匹配、全字匹配等．

## 参考资料与注释

[^ref1]: VS Code 的 C/C++ 扩展如果选择 lldb 作调试器，则会默认采用 lldb-mi 程序，而它已经被 LLVM 开发团队从项目中分离出来，需要自己编译该程序．而它本身就有一些 bug，使用体验和方便程度都不如 CodeLLDB 扩展．

[^ref2]: 从扩展商店安装 CodeLLDB 后它会再从 GitHub 下载本体，下载速度奇慢，有时下载出错，所以最好直接下载本体然后安装．更新也可直接按照以上步骤下载安装．

[^ref3]: [VS Code 官方文档](https://code.visualstudio.com/docs/)．


## tools/editor/xcode.md

author: shenyouran, Xeonacid, StudyingFather, CoelacanthusHex

## 简介

Xcode 是一个运行在 macOS 上的集成开发工具（IDE），由 Apple Inc. 开发．

## 安装

### 方法一

打开苹果电脑自带的 App Store（或者尝试 [快捷链接](https://apps.apple.com/cn/app/xcode/id497799835?mt=12)）下载 Xcode．点击获取，然后输入苹果账号密码开始下载安装．

![](images/xcode-1.jpg)

### 方法二

访问 [苹果开发者下载页面](https://developer.apple.com/download/more/)，用苹果账号登录，然后找到 Xcode 最新的稳定版本安装包（即不含 Beta 的最新版本，此处为 11.6）：

![](images/xcode-2.jpg)

点击弹出框内蓝色的文件名即可下载．得到压缩包之后，用系统自带的工具进行解压，然后得到文件 Xcode.app．把这个文件移动到【应用程序】文件夹后即可使用．

## 基础配置

首次打开 Xcode 时，可能会遇到下列弹出窗口：

![](images/xcode-3.jpg)

这个窗口是 Xcode 元件的安装引导．点击 `Install` 并输入当前用户密码即可．

安装完毕后，界面左侧显示：

![](images/xcode-4.jpg)

点击 `Create a new Xcode project`（创建一个新的 Xcode 项目），然后选择上方 `macOS` 中的 `Command Line Tool`（命令行工具），并点击右下角的 `Next`．

![](images/xcode-5.jpg)

接下来，我们可以给项目命名，但最重要的是选择项目的语言．我们可以根据自己的需求，在最下方 `Language` 处选择 C 或者 C++：

![](images/xcode-6.jpg)

项目的目录可以根据需要选择．创建完毕后，Xcode 会自动打开这个项目，并自动创建一个 `main` 文件（C 语言的后缀为 `.c`，C++ 语言的后缀为 `.cpp`）．

点击这个文件，就可以打开编辑区域：

![](images/xcode-7.jpg)

编写代码后，可以按⌘B 编译（Build），⌘R 运行（Run）．运行后拖动，得到三个部分：

![](images/xcode-8.jpg)

一般来说我们只使用【编辑区】和【运行区】．若程序有输入，那么在【运行区】中进行输入之后，就可以得到输出．界面呈现效果：

![](images/xcode-9.jpg)

仿照这种方式，我们就可以运行任何的单个 C/C++ 程序．

## 万能头文件的使用

在编写代码过程中，我们可能会使用到很多头文件．常用的解决方法是使用万能头文件．

我们在源代码第一行引入万能头文件，然而编译过程中却提示：`'bits/stdc++.h' file not found`．即该头文件未找到．

![](images/xcode-10.jpg)

这是因为在 macOS 上默认使用 [libc++](https://libcxx.llvm.org/) 作为 C++ 标准库实现，而万能头 `bits/stdc++.h` 是 [GNU libstdc++](https://gcc.gnu.org/onlinedocs/libstdc++/) 所独有的．

不过，我们可以手动编写一个万能头文件来使用．

### 步骤 1

打开终端（Terminal.app），前往 Xcode 存储头文件的文件夹，即：

```bash
cd /Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/include/c++/v1
```

如果 Xcode 版本大于等于 12.5，那么

```bash
cd /Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX.sdk/usr/include/c++/v1/
```

### 步骤 2

创建 `bits` 文件夹并进入：

```bash
mkdir bits
cd bits
```

用 vim 创建 stdc++.h 文件：

```bash
vim stdc++.h
```

界面如下：

![](images/xcode-11.jpg)

接着，我们需要通过 vim 编辑文件．敲击 i（insert）键盘即可进入插入/编辑模式（下方出现 `-- INSERT --`）：

![](images/xcode-12.jpg)

将下面这段代码块复制并粘贴到终端中：

??? note "万能头文件代码块"
    ```cpp
    // C++ includes used for precompiling -*- C++ -*-
    
    // Copyright (C) 2003-2020 Free Software Foundation, Inc.
    //
    // This file is part of the GNU ISO C++ Library.  This library is free
    // software; you can redistribute it and/or modify it under the
    // terms of the GNU General Public License as published by the
    // Free Software Foundation; either version 3, or (at your option)
    // any later version.
    
    // This library is distributed in the hope that it will be useful,
    // but WITHOUT ANY WARRANTY; without even the implied warranty of
    // MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    // GNU General Public License for more details.
    
    // Under Section 7 of GPL version 3, you are granted additional
    // permissions described in the GCC Runtime Library Exception, version
    // 3.1, as published by the Free Software Foundation.
    
    // You should have received a copy of the GNU General Public License and
    // a copy of the GCC Runtime Library Exception along with this program;
    // see the files COPYING3 and COPYING.RUNTIME respectively.  If not, see
    // <http://www.gnu.org/licenses/>.
    
    /** @file stdc++.h
     *  This is an implementation file for a precompiled header.
     */
    
    // 17.4.1.2 Headers
    
    // C
    #ifndef _GLIBCXX_NO_ASSERT
    #include <cassert>
    #endif
    #include <cctype>
    #include <cerrno>
    #include <cfloat>
    #include <ciso646>
    #include <climits>
    #include <clocale>
    #include <cmath>
    #include <csetjmp>
    #include <csignal>
    #include <cstdarg>
    #include <cstddef>
    #include <cstdio>
    #include <cstdlib>
    #include <cstring>
    #include <ctime>
    #include <cwchar>
    #include <cwctype>
    
    #if __cplusplus >= 201103L
    #include <ccomplex>
    #include <cfenv>
    #include <cinttypes>
    #include <cstdbool>
    #include <cstdint>
    #include <ctgmath>
    /* https://stackoverflow.com/a/25892335/15125422 */
    #if defined(__GLIBCXX__) || defined(__GLIBCPP__)
    #include <cstdalign>
    #include <cuchar>
    #endif
    #endif
    
    // C++
    #include <algorithm>
    #include <bitset>
    #include <complex>
    #include <deque>
    #include <exception>
    #include <fstream>
    #include <functional>
    #include <iomanip>
    #include <ios>
    #include <iosfwd>
    #include <iostream>
    #include <istream>
    #include <iterator>
    #include <limits>
    #include <list>
    #include <locale>
    #include <map>
    #include <memory>
    #include <new>
    #include <numeric>
    #include <ostream>
    #include <queue>
    #include <set>
    #include <sstream>
    #include <stack>
    #include <stdexcept>
    #include <streambuf>
    #include <string>
    #include <typeinfo>
    #include <utility>
    #include <valarray>
    #include <vector>
    
    #if __cplusplus >= 201103L
    #include <array>
    #include <atomic>
    #include <chrono>
    #include <codecvt>
    #include <condition_variable>
    #include <forward_list>
    #include <future>
    #include <initializer_list>
    #include <mutex>
    #include <random>
    #include <ratio>
    #include <regex>
    #include <scoped_allocator>
    #include <system_error>
    #include <thread>
    #include <tuple>
    #include <type_traits>
    #include <typeindex>
    #include <unordered_map>
    #include <unordered_set>
    #endif
    
    #if __cplusplus >= 201402L
    #include <shared_mutex>
    #endif
    
    #if __cplusplus >= 201703L
    #include <any>
    #include <charconv>
    // #include <execution>
    #include <filesystem>
    #include <memory_resource>
    #include <optional>
    #include <string_view>
    #include <variant>
    #endif
    
    #if __cplusplus > 201703L
    #include <bit>
    #include <compare>
    #include <concepts>
    #include <numbers>
    #include <ranges>
    #include <span>
    #include <stop_token>
    // #include <syncstream>
    #include <version>
    #endif
    ```

该文件来源于 [10.2.0 版本的 libstdc++](https://github.com/gcc-mirror/gcc/blob/ee5c3db6c5b2c3332912fb4c9cfa2864569ebd9a/libstdc++-v3/include/precompiled/stdc++.h) 并经少许修改以兼容 libc++．

按键盘左上角的<kbd>Esc</kbd>退出编辑模式，然后直接输入 `:wq` 并换行即可保存文件．

### 步骤 3

关闭终端，回到 Xcode．重新按下 ⌘B/⌘R 进行编译，发现编译成功：

![](images/xcode-13.jpg)

## 优缺点

优点：由苹果开发，适合 Mac 用户，界面齐全、美观．

缺点：Xcode 主要用来苹果程序的开发，对于竞赛来说功能冗余，安装包大小较大，而且仅能在 Mac 端上使用．


## tools/git.md

???+ note "Note"
    本页面将着重介绍 Git 这一版本控制系统，与 GitHub 相关的内容，请参考 [GitHub 帮助](https://docs.github.com/cn) 和 [如何参与 - OI Wiki](../intro/htc.md)．

Git 是目前使用最广泛的版本控制系统之一．**OI Wiki** 也使用了 Git 作为版本控制系统．

## 安装

参见 [Git - Downloads](https://git-scm.com/downloads)．

## 配置

Git 根据配置文件的应用范围，将配置文件分为不同的等级，其中较常用的有两个级别[^note1]：

1.  适用于当前用户的全局配置文件，该用户操作本系统上的所有仓库时都会查询该配置文件．
2.  适用于当前仓库的配置文件．

当多个配置文件对同一个选项作出设置的时候，局部设置会自动覆盖全局设置．因此如果需要在某个仓库应用特定的设置的话，只需更改该仓库下的特定设置即可，不会对全局设置造成影响．

修改配置文件需要用到 `git config` 命令．

### 设置用户信息

安装 Git 后，第一件事情就是设置你的用户名和邮箱．这些信息在每次提交时都会用到．

```console
$ git config --global user.name "OI Wiki"
$ git config --global user.email oi-wiki@example.com
```

???+ note "Note"
    这里给出的用户名和邮箱仅供演示．您在根据本页面的内容配置时，请记得将这里的用户名和邮箱改成自己的信息．

这里的 `--global` 表示修改的是全局配置，即该设置对当前用户下的所有仓库均有效．如果不添加 `--global` 选项，则会默认修改当前仓库下的配置文件．

如果想要修改某个仓库的特定设置，只需在该仓库下执行不带 `--global` 的命令即可．

### 配置编辑器

```console
$ git config --global core.editor emacs
```

执行如上命令可以将编辑器更改为 [Emacs](./editor/emacs.md)．

在 Windows 下，Git 的默认编辑器可以在安装 Git 时选择（见前文）．之后若要修改，在 Git Bash 里输入如上命令，将编辑器名换成编辑器的绝对路径，运行命令即可．

### 显示配置

可以通过 `git config -l` 列出当前已经设置的所有配置参数．使用 `git config --global -l` 可以列出所有全局配置．

## 仓库操作基础

### 新建 Git 仓库

新建一个 Git 仓库非常简单，只需在想要建立仓库的文件夹输入如下命令：

```console
$ git init
```

Git 将在当前文件夹新建一个 `.git` 文件夹，一个仓库就这样建好了．

如果想把一个仓库克隆到自己的电脑上（比如将 **OI Wiki** 的代码拷贝到本地上进行编辑），采用 `git clone` 命令即可．

```console
$ git clone https://github.com/OI-wiki/OI-wiki
```

???+ note "远程仓库的链接"
    这里给出的仓库链接是 HTTP(S) 链接，也即我们采用了 HTTP(S) 方式连接到远程仓库．
    
    事实上，连接到远程仓库的方式还有多种．其中使用 ssh 连接到远程仓库的方法更为方便和安全，在「远程仓库的管理」部分我们会简单介绍使用 ssh 连接到远程仓库的方法．

这样，被克隆的仓库的内容就会被储存到当前文件夹下一个与仓库同名的新文件夹．在本例中，当前文件夹下会出现一个名为 `OI-wiki` 的新文件夹．

### 跟踪文件

在对仓库的文件做出了一些更改后，这些更改需要被纳入到版本管理当中去．

使用 `git status` 命令可以查看当前仓库文件的状态．

举个例子，在一个空仓库中新增了一个 `README.md` 文件后，执行 `git status` 命令的效果如下：

<!-- scripts.linter.preprocess.fix_details off -->

```console
$ git status
On branch master

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)

        README.md

nothing added to commit but untracked files present (use "git add" to track)
```

<!-- scripts.linter.preprocess.fix_details on -->

这里的 Untracked files 指的是 Git 之前没有纳入版本跟踪的文件．如果文件没有纳入版本跟踪，对该文件的更改不会被 Git 记录．

执行 `git add <文件>` 命令可以将指定的文件纳入到版本跟踪中．

<!-- scripts.linter.preprocess.fix_details off -->

```console
$ git add README.md # 将这个文件纳入到版本跟踪中
$ git status
On branch master

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)

        new file:   README.md
```

<!-- scripts.linter.preprocess.fix_details on -->

这时 `README.md` 已经纳入了版本跟踪，放入了暂存区．接下来只需执行 `git commit` 命令就可以提交这次更改了．

但在进行这一工作之前，让我们先对 `README.md` 做点小更改．

<!-- scripts.linter.preprocess.fix_details off -->

```console
$ vim README.md # 随便更改点东西
$ git status
On branch master

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)

        new file:   README.md

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore -- <file>..." to discard changes in working directory)

        modified:   README.md
```

<!-- scripts.linter.preprocess.fix_details on -->

你会发现 `README.md` 同时处于暂存区和非暂存区．实际上，是否处于暂存区是对于更改而言的，而不是对于文件而言的，所以对 `README.md` 的前一次更改已被纳入暂存区，而后一次更改还没有．如果这时候执行 `git commit` 命令，只有处于暂存区的更改会被提交，而非暂存区的更改，则不会被提交．

Git 给了一条提示，执行 `git add README.md` 就可以将非暂存区的更改放入暂存区了．

???+ note "一次性将所有更改放入暂存区"
    `git add` 命令会将对指定的文件的更改放入暂存区中．
    
    在多数情况下，用户更期望一次性将所有更改都放入暂存区中，这时候可以应用 `git add -A` 命令．该命令会将所有更改（包括未被纳入版本跟踪的文件，不包括被忽略的文件）放入暂存区．
    
    如果只需更新已被纳入版本跟踪的文件，而不将未纳入版本跟踪的文件加入暂存区，可以使用 `git add -u`．

???+ note "忽略文件"
    有些时候我们并不希望将一些文件（如可执行文件等）纳入到版本跟踪中．这时候可以在仓库根目录下创建 `.gitignore` 文件，在该文件里写下想要忽略的文件．Git 将不会将这些文件纳入到版本跟踪中．
    
    例如，`*.exe` 将自动忽略仓库里的所有扩展名为 `.exe` 的文件．

现在将非暂存区的文件加入暂存区，将所有更改一并提交（commit）．

```console
$ git add README.md
$ git commit # 接下来会弹出编辑器页面，你需要写下 commit 信息
[master (root-commit) f992763] initial commit
 1 file changed, 2 insertions(+)
 create mode 100644 README.md
```

现在重点观察一下这一次 commit 的信息．

`master` 表示当前位于 `master` 分支（关于分支的问题，下文将会详细介绍），`f992763` 表示本次提交的 SHA-1 校验和的前几位，后面则是本次提交的信息．

需要特别关注的是这里的 SHA-1 校验码，每个校验码都与某个时刻仓库的一个快照相对应．利用这一特性我们可以访问历史某个时刻的仓库快照，并在该快照上进行更改．

接下来两行则详细说明了本次更新涉及的文件更改．

另外，commit 过程中可以利用几个参数来简化提交过程：

-   `-a`：在提交前将所有已跟踪的文件的更改放入暂存区．需要注意的是未被跟踪的文件（新创建的文件）不会被自动加入暂存区，需要用 `git add` 命令手动添加．
-   `-m`：该参数后跟提交信息，表示以该提交信息提交本次更改．例如 `git commit -m "fix: typo"` 会创建一条标题为 `fix: typo` 的 commit．

### 查看提交记录

使用 `git log` 命令可以查看仓库的提交历史记录．

可以看到，提交历史里记录了每次提交时的 SHA-1 校验和，提交的作者，提交时间和 commit 信息．

```console
$ git log
commit ae9dd3768a405b348bc6170c7acb8b6cb5fe333e (HEAD -> master)
Author: OI Wiki <oi-wiki@example.com>
Date:   Sun Sep 13 00:30:18 2020 +0800

    feat: update README.md

commit f99276362a3c260d439364c505a7a06859f34bf9
Author: OI Wiki <oi-wiki@example.com>
Date:   Sun Sep 13 00:06:07 2020 +0800

    initial commit
```

## 分支管理

为什么版本管理中需要分支管理呢？答案主要有两点：

1.  直接更改主分支不仅会使历史记录混乱，也可能会造成一些危险的后果．
2.  通过分支，我们可以专注于当前的工作．如果我们需要完成两个不同的工作，只需开两个分支即可，两个分支间的工作互不干扰．

在 Git 中，简单来说，分支就是指向某个快照的指针．每次提交时，Git 都会为这次提交创建一个快照，并将当前分支的指针移动到该快照．

另外还有一个 HEAD 指针，它指向当前所在的分支．

切换分支的过程，简单来说就是将 HEAD 指针，从指向当前所在的分支，改为指向另外一个分支．在这一过程中，Git 会自动完成文件的更新，使得切换分支后仓库的状态与目标分支指向的快照一致．

### 分支的创建

利用 `git branch` 命令可以创建分支，`git switch` 命令可以切换分支，`git switch -c` 命令可以创建分支并切换到这个新分支．

```console
$ git switch -c dev # 创建一个叫做 dev 的新分支并切换当前分支到 dev
Switched to branch 'dev'
$ git branch # 查看分支列表
  master
* dev
```

`dev` 前面的星号代表该仓库的当前分支为 `dev`，接下来对这个仓库的更改都将记录在这个分支上．

试着创建一个新文件 `aplusb.cpp`．

```console
$ vim aplusb.cpp
$ git add aplusb.cpp
$ git commit -m "feat: add A+B Problem code"
[dev 5da093b] feat: add A+B Problem code
 1 file changed, 7 insertions(+)
 create mode 100644 aplusb.cpp
```

现在切换回 `master` 分支，这时候文件夹中没有了 `aplusb.cpp`，一切都回到了刚刚创建 `dev` 分支时的状态．这时候可以在 `master` 分支上继续完成其他的工作．

```console
$ git switch master
Switched to branch 'master'
$ vim README.md # 对 README 做些小改动
$ git commit -a -m "feat: update README.md"
[master 5ca15f0] feat: update README.md
 1 file changed, 1 insertion(+), 1 deletion(-)
```

下面用一张图来解释刚才的操作过程．

![](./images/git1.svg)

`master` 分支被标红，表明在这几次操作后，它是当前分支（即 HEAD 指向的位置）．

-   最开始时 `master` 指向 `ae9dd37` 这一快照．
-   接下来在 `master` 所在的位置创建了一个新的 dev 分支，该分支一开始和 master 指向相同位置．
-   在 `dev` 分支上作了一些更改（创建了 `aplusb.cpp`），进行了一次提交，本次提交后，`dev` 分支指向 `5da093b` 这一快照．
-   切换回 `master` 分支后，因为 `master` 分支还指向 `ae9dd37`，还没有创建 `aplusb.cpp`，因此仓库中没有这一文件．
-   接下来在 `master` 分支上进行更改（更新了 `README.md`），进行了一次提交，`master` 分支指向了 `5ca15f0` 这一快照．

### 分支的合并

当一个分支上的工作已经完成，就可以将这些工作合并到另外一个分支上去．

还是接着上面这个例子，`dev` 分支的工作已经完成，通过 `git merge` 命令可以将该分支合并到当前分支（`master`）上：

```console
$ git merge dev
Merge made by the 'recursive' strategy.
 aplusb.cpp | 7 +++++++
 1 file changed, 7 insertions(+)
 create mode 100644 aplusb.cpp
```

![](./images/git2.svg)

这次合并具体是怎么执行的呢？

在合并之前，`master` 指向 `5ca15f0`，而 `dev` 指向 `5da093b`，这两个状态并不在一条链上．

Git 会找到这两个状态的最近公共祖先（在上图中是 `ae9dd37`），并对这三个快照进行一次合并．三个快照合并的结果作为一个新的快照，并将当前分支指向这一快照．

合并过程本身也是一次提交，不过与常规提交不同的是，合并提交有不止一个前驱提交，它是多个提交状态合并后的结果．

在合并完成后，`dev` 分支就完成了它的使命，这时候可以利用下面的命令删除 `dev` 分支：

```console
$ git branch -d dev # 对于未合并的分支，可以使用 -D 参数强制删除
```

不过合并过程并非总是这么顺利，在某些情况下，合并过程可能会出现冲突，这个问题接下来会讲到．

### 解决合并冲突

如果在两个分支中，对同一个文件的同一部分进行了不同的更改，Git 就无法自动合并这两个分支，也就是发生了合并冲突．

接着上面的例子，假如你在合并后的 `master` 分支的基础上，新开了一个 `readme-refactor` 分支，准备重写一份自述文件．但因为一些疏忽，你同时更改了 `readme-refactor` 和 `master` 分支的自述文件．

刚开始自述文件是这样的：

```markdown
# This is a test repo.

This repo includes some c++ codes.
```

在 `readme-refactor` 分支下的自述文件是这样的：

```markdown
# Code Library

This repo includes some c++ codes.
```

在 `master` 分支下的自述文件是这样的：

```markdown
# This is a code library.

This repo includes some c++ codes.
```

这时候运行 `git merge readme-refactor` 命令，Git 提示出现了合并冲突．

执行一下 `git status` 命令，可以查看是哪些文件引发了冲突．

<!-- scripts.linter.preprocess.fix_details off -->

```console
$ git status
On branch master
You have unmerged paths.
  (fix conflicts and run "git commit")

Unmerged paths:
  (use "git add <file>..." to mark resolution)

    both modified:      README.md

no changes added to commit (use "git add" and/or "git commit -a")
```

<!-- scripts.linter.preprocess.fix_details on -->

如何解决冲突？对于每个发生了合并冲突的文件，Git 都会在这些文件中加入标准的冲突解决标记．比如这个例子中的 `README.md` 文件，打开后它长这个样子：

```markdown
<<<<<< HEAD
# This is a code library.
======
# Code Library
>>>>>> readme-refactor

This repo includes some c++ codes.
```

`======` 作为分界线将两个分支的内容隔开，`<<<<<< HEAD` 标记和 `======` 之间的部分是 HEAD 指针（`master` 分支）的内容，而 `======` 和 `>>>>>> readme-refactor` 标记之间的部分是 `readme-refactor` 分支的内容．

通过编辑文本来处理冲突，删除这些冲突标记，保存文件，将这些文件纳入暂存区后提交，就可以解决合并冲突了．

```console
$ git add README.md # 将发生冲突的文件纳入暂存区
$ git commit
[master fe92c6b] Merge branch readme-refactor into master
```

### 其他合并方式

默认情况下，Git 采用 Merge（合并）的方式合并两个分支．使用该方法将分支 B 并入分支 A 时，会将 B 分支的所有 commit 并入 A 分支的提交历史中．

除此以外，Git 还提供了两种合并分支的方式：Squash（压缩）和 Rebase（变基）．

#### Squash（压缩）

使用 Squash 方式将分支 B 并入分支 A 时，在 B 分支上的所有更改会被合并为一次 commit 提交到 A 分支．

在 `git merge` 中加入 `--squash` 参数即可使用 Squash 方式进行分支合并．

```console
$ git merge <branch> --squash
```

需要注意的是，在执行上述命令后，Git 只会将 B 分支的所有更改存入 A 分支的缓冲区内，接下来还需要执行一次 `git commit` 命令完成合并工作．

使用 Squash 方式合并可以简化 commit 记录，但是会丢失具体到每一次 commit 的信息（每次 commit 的提交者，每次 commit 的更改等等），只留下合并为一个整体的信息（每次 commit 的提交者会以 "Co-authored-by" 的形式在提交信息中列出）．但如果是在 GitHub 上进行 Squash and Merge，原有的信息都可以在 Pull Request 中查看．

#### Rebase（变基）

使用 Rebase 方式将分支 B 并入分支 A 时，在 B 分支上的每一次 commit 都会单独添加到 A 分支，而不再像 Merge 方式那样创建一个合并 commit 来合并两个分支的内容[^note2]．

首先，切换到 B 分支，接下来将 B 分支变基到 A 分支：

```console
$ git checkout B
$ git rebase A
```

现在切回到 A 分支，再执行一次 `git merge` 命令，即可完成将 B 分支的内容合并到 A 分支的工作．

```console
$ git checkout A
$ git merge B
```

使用 Rebase 完成合并可以让提交历史线性化，在适当的场景下正确地使用 Rebase 可以达到比 Merge 更好的效果．但是这样做会改变提交历史，在进行 Rebase 时和 Rebase 后再进行相关合并操作时都会增加出现冲突的可能，如果操作不当可能反而会使提交历史变得杂乱．因此，如果对 Rebase 操作没有充分的了解，不建议使用．

## 管理远程仓库

在本地完成更改后，你可能会需要将这些更改推送到 GitHub 等 Git 仓库托管平台上．托管在这些平台上的仓库就归属于远程仓库的范畴——你可以从这些仓库中获取信息，也可以将你作出的更改推送到远程仓库上．与其他人的协作往往离不开远程仓库，因此学会管理远程仓库很有必要．

### 远程仓库的查看

使用 `git remote` 命令可以查看当前仓库的远程仓库列表．

如果当前仓库是克隆来的，那么应该会有一个叫做 origin 的远程仓库，它的链接就是克隆时用的链接．

```console
$ git remote
origin
```

如果要查看某个远程仓库的详细信息的话，可以这样操作：

```console
$ git remote show origin
* remote origin
  Fetch URL: git@github.com:OI-wiki/OI-wiki.git
  Push  URL: git@github.com:OI-wiki/OI-wiki.git
  HEAD branch: master
  Remote branches:
    git             tracked
    master          tracked
  ...
```

### 远程仓库的配置

执行 `git remote add <name> <url>` 命令可以添加一个名字为 `name`，链接为 `url` 的远程仓库．

执行 `git remote rename <oldname> <newname>` 可以将名字为 `oldname` 的远程仓库改名为 `newname`．

执行 `git remote rm <name>` 可以删除名字为 `name` 的远程仓库．

执行 `git remote get-url <name>` 可以查看名字为 `name` 的远程仓库的链接．

执行 `git remote set-url <name> <newurl>` 可以将名字为 `name` 的远程仓库的链接更改为 `newurl`．

### 从远程仓库获取更改

在远程仓库中，其他人可能会推送一些更改，执行 `git fetch` 命令可以将这些更改获取到本地．

```console
$ git fetch <remote-name> # 获取 <remote-name> 的更改
```

需要注意的是，`git fetch` 命令只会获取远程仓库的更改，而不会将这些更改合并到本地仓库中．如果需要将这些更改进行合并，可以使用 `git pull` 命令．在默认情况下，`git pull` 相当于 `git fetch` 后 `git merge FETCH_HEAD`．

```console
$ git pull <remote-name> <branch> # 获取 <remote-name> 的更改，然后将这些更改合并到 HEAD
```

### 将更改推送到远程仓库

当你完成了一些更改之后，使用 `git push` 命令可以将这些更改推送到远程仓库．

```console
$ git push <remote> <from>:<to> # 将本地 <from> 分支的更改推送至 <remote> 的 <to> 分支
```

根据远程仓库的要求，可能会要求你输入远程仓库账户的用户名和密码．

需要注意的是，你的更改能成功推送，需要满足两个条件：你拥有向这个仓库（分支）的写入权限，且你的这个分支比远程仓库的相应分支新（可以理解为没有人在你进行更改的这段时间进行了推送）．当远程分支有当前分支没有的新更改时，可以执行 `git pull` 命令完成合并再提交．

如果你需要强制将本地分支的更改推送到远程仓库的话，可以加入 `-f` 参数．此时 **远程仓库的提交历史会被本地的提交历史覆盖**，因此该命令应谨慎使用．更好的选择是使用 `--force-with-lease` 参数，该参数仅在远程仓库没有更新时才会进行覆盖．需要注意的是，此处「更新」是相对于上一次 fetch 而言的，如果使用了 VS Code 提供的 Auto Fetch 功能，可能会没有注意到更新而使 `--force-with-lease` 和 `-f` 一样危险．

### 追踪远程分支

通过将一个本地分支设定为追踪远程分支，可以方便地查看本地分支与远程分支的差别，并能简化与远程分支交互时的操作．

在开始追踪前，你需要先执行 `git fetch <remote-name>` 将远程仓库的信息抓取到本地．

接下来执行 `git switch <remote-branch>`，会在本地自动创建名字为 `<remote-branch>` 的新分支，并设定该分支自动追踪相应的远程分支．

???+ note "Note"
    需要注意，只有当本地不存在该分支，且恰好只有一个远程分支的名字与该分支匹配时，Git 才会自动创建该分支且设定其追踪相应的远程分支．

这时候执行 `git status` 命令，会提示当前分支与远程分支之间的差别．

因为设定了本地分支追踪的远程分支，向远程分支推送的命令也被简化了．只需要执行 `git push` 命令，在本地分支上作出的更改就能被推送至其追踪的远程分支．

对于本地已有的分支，设定其对应的远程追踪分支也很容易．只需在当前分支下执行 `git branch -u <remote-name>/<remote-branch>`，就可以设定当前的本地分支追踪 `<remote-name>/<remote-branch>` 这一远程分支．

### 使用 ssh 连接

与 HTTP(S) 相比，使用 ssh 连接到远程仓库更为方便安全．

在使用 ssh 连接到远程仓库之前，需要先在本地添加 ssh 密钥．接下来需要将本地添加的 ssh 密钥的 **公钥** 上传到远程仓库账户．

考虑到本文主要是给 **OI Wiki** 的贡献者提供一个使用 Git 的教程，这里直接给出 [GitHub Docs 提供的教程](https://docs.github.com/cn/github/authenticating-to-github/connecting-to-github-with-ssh)，供各位读者参考．

完成以上步骤后，你就可以通过 ssh 连接到远程仓库了．下面就是一条通过 ssh 连接 clone **OI Wiki** 仓库的命令：

```console
$ git clone git@github.com:OI-wiki/OI-wiki.git
```

将更改推送至远程仓库的过程与使用 HTTP(S) 连接类似．但使用 ssh 连接可以免去验证远程仓库账号密码的过程．

## Git GUI Tools

对于不熟悉命令行的同学，纯命令行的 Git 的上手难度可能会偏高，而借助 GUI 工具可以一定程度上降低 Git 的上手难度．此外，相比于命令行，GUI 工具在查看 diff 以及 log 时在体验上有一定程度的提高．

Git 本身自带有 GUI，市面上也有很多优秀的 Git GUI 工具，例如针对 Windows 用户的 TortoiseGit[^note3]，支持 Windows 和 Mac 的 Sourcetree[^note4]等．

这里简单介绍一下 TortoiseGit 的使用．下载并安装好 TortoiseGit 之后，在本地仓库的目录下，单击鼠标右键，在右键菜单中就可以看到 Git 的各个功能．

![TortoiseGit Example](images/git11.png)

详细的使用方法这里不再赘述，可以参考官网里的使用文档或者通过搜索引擎学习，例如 [TortoiseGit Manual](https://tortoisegit.org/docs/tortoisegit/index.html)．

很多 GUI 工具都有官方中文支持，例如 Git Desktop 以及 TortoiseGit．但是还是会有部分翻译看起来较为变扭，推荐使用英文版本．

## 外部链接

-   [Git Reference](https://git-scm.com/docs)
-   [Pro Git Book](https://git-scm.com/book/zh/v2)
-   [Learn Git Branching](https://learngitbranching.js.org/)

## 参考资料与注释

[^note1]: 事实上 Git 还有一个针对系统上每一个用户及系统上所有仓库的通用配置文件，该配置文件覆盖范围最广，等级在用户配置文件之上．因为该配置实践中较少使用，这里不再展开．

[^note2]: [Pro Git Book](https://git-scm.com/book/zh/v2/Git-%E5%88%86%E6%94%AF-%E5%8F%98%E5%9F%BA) 中提供了可视化的 Rebase 过程图，借助图片读者可以更好地理解 Rebase 的机制．

[^note3]: [TortoiseGit](https://tortoisegit.org/)

[^note4]: [Sourcetree](https://www.sourcetreeapp.com/)


## tools/judger/arbiter.md

author: Ir1d, HeRaNO, NachtgeistW, i-Yirannn, bear-good, ranwen, CoelacanthusHex, billchenchina, Tiger3018, Xeonacid, Cryflmind

## Arbiter

**Arbiter** 为北京航空航天大学为 NOI Linux 开发的评测工具，现已用于各大 NOI 系列程序设计竞赛的评测．据吕凯风在 2016 年冬令营上的讲稿《下一代测评系统》，Arbiter 是由北京航空航天大学的团队（GAIT）在尹宝林老师的带领下开发完成的．

在 NOI Linux 更新到 2.0 版本后，Arbiter 也用 Qt 5.12.8 重新编译，并发布为 Arbiter 2.0．因为之后的测评环境均使用 NOI Linux 2.0，因此以下介绍使用的 Arbiter 版本均为 NOI Linux 2.0 中自带的 Arbiter 2.0．

此测评软件仅能在 NOI Linux 下找到．二进制文件位置为 `/usr/local/arbiter/local/arbiter_local`．

### 使用方法

#### 配置程序

配置选手源程序文件夹和选手名单．选手文件夹如 NOIP 格式创建：

```text
players/
| -- day1
|    | -- <contestant_1's ID>
|    |     | -- <problem_1>
|    |     |   `-- <problem_1>.c/cpp/pas
|    |     | -- <problem_2>
|    |     |   `-- <problem_2>.c/cpp/pas
|    |     | ...
|    |     | -- <problem_x>
|    |        `-- <problem_x>.c/cpp/pas
|    | -- <contestant_2's ID>
|    |     | -- <problem_1>
|    |     ...
|    ...
| -- day2
|    | -- <contestant_1's ID>
|    |     | -- <problem_1>
|    |     |   `-- <problem_1>.c/cpp/pas
|    |     | -- <problem_2>
|    |     |   `-- <problem_2>.c/cpp/pas
|    |     | ...
|    |     | -- <problem_x>
|    |        `-- <problem_x>.c/cpp/pas
|    | -- <contestant_2's ID>
|    |     | -- <problem_1>
|    |     ...
|    ...
...
```

其中，`day<x>` 中的 `<x>` 是场次编号，`<contestant_x's ID>` 指的是选手编号，形如 `<省份>-<编号>`，例如 HL-001，JL-125 等等；`<problem_x>` 指的是题目名称．在自测时可以使用字母、短线（即 `-`）和数字的组合作为选手编号．

选手名单格式如下：

```text
<contestant_1's ID>,<contestant_1's name>
<contestant_2's ID>,<contestant_2's name>
...
```

其中，`<contestant_x's name>` 表示选手姓名．保存这个文件为纯文本文件或 csv 文件，可以使用 `UTF-8` 编码．

选手名单也可以在启动 Arbiter 后手动添加．

接下来配置测试数据．每组数据的命名格式如下：

```text
<problem_x><y>.in <problem_x><y>.ans
```

其中，`<y>` 是数据编号，编号从 1 开始．默认测试数据后缀名是 `.ans`，选手输出的后缀名是 `.out`，不能混淆．

如果需要将之前生成的 out 格式修改为 ans 格式，在 NOI Linux 2.0 中可以使用 `rename` 命令批量修改，而在 Windows 中可以使用 `ren` 命令批量修改．我们将在后面介绍这些命令的用法．

不用将每题的测试数据放置在各题的文件夹里，只需要放在一起即可．

然后开始测评文件夹的配置．

左下角「显示应用程序」-「全部」-「Arbiter\_local」，启动 Arbiter．

![Arbiter\_Home](./images/arbiter_home.png)

点击 OPEN 可以打开已经建立的比赛，之后需选择对应比赛文件夹下的 `setup.cfg` 文件；点击 NEW 可以新建一个竞赛，并设置名称和比赛目录．注意，需要在用户 **主目录下** 新建一个文件夹，然后选择其为比赛目录，如果在桌面上建立比赛目录的话无法测评．出现这种问题很有可能是因为比赛文件夹路径中不能包含中文．

![add\_problem](./images/arbiter_addproblem.png)

在左边试题概要里「右键」-「添加考试」，再在考试标签上「右键」-「添加试题」，新建出试题即可．

单击考试左边的向下箭头即可全部显示，单击试题标签对试题名称进行修改，改为题目的英文名称，同时修改题目时间与空间限制和比较方式．比较方式十分不推荐用「全文完全直接比较」，对于 Windows 下制作的数据十分不友好．可以根据题目自主选择比较器，但是需要注意必须选择一个比较器，否则测评结果将是 `No Score.`．

![problem\_list](./images/arbiter_problem.png)

点击「文件」-「保存」．该操作不可省略，否则程序将不会生成题目配置文件．注意每一次对题目配置的修改都要保存．

此时，打开考试文件夹，会发现有如下内容．

```text
<name>/
| -- data
| -- evaldata
| -- filter
| -- final
| -- players
| -- result
| -- tmp
`-- day1.info
`-- player.info
`-- setup.cfg
`-- task1_1.info
`-- task1_2.info
`-- team.info
```

`filter` 文件夹放置了一些比较器；`result` 文件夹存放选手的测评结果；`tmp` 文件夹是测评时的缓存文件夹．其中 `day<x>.info` 为场次配置文件，`<x>` 为场次编号；`task<x>_<y>.info` 文件为题目配置文件，`<x>` 为场次编号，`<y>` 为题目序号．

把已经建好的选手程序文件夹放在 `players/` 目录下，注意最外层应按照考试日建立相应的 `day<x>` 文件夹．将所有测试数据（不放在文件夹里）放在 `evaldata` 中．如果使用了自定义校验器，则需要将自定义校验器放在 `filter` 中．

#### 正式测评

点开「试题评测」标签，会出现如下页面：

![Pretest](./images/arbiter_pretest.png)

如果选手名单已经建立了，直接选择右边的「导入名单」进行导入．如果人数较少，可以选择右边的「添加选手」进行导入．

导入后的页面如图．

![Test](./images/arbiter_test.png)

示例中的编号是 `HL-001`，程序会自动识别出「所属」一栏．如果不是 NOIP 规范的编号是识别不出来的．

把测评第 0 场变为测评第 1 场（或者其他场次）．然后选择右边的全选（或选择指定的选手），再选择下面的评测选定选手，选择要测评的题目（或全部试题），最后等待测评结束即可．

测试点详细信息需要在 `result` 文件夹下查看，文件夹下会有选手的结果文件夹，结果文件的后缀名为 `.result`，用纯文本方式查看即可．如果出现 `No score file.` 的错误，可以检查测评时是否生成了 `/tmp/_eval.score` 文件．

### 自定义校验器的编写

反编译其他校验器，可以知道运行自定义校验器的命令是 `<problem>_e <in> <out> <ans>`．后三个参数分别代表输入，选手输出和答案文件．最终的评分结果需写入 `/tmp/_eval.score` 文件中，第一行是测评信息，第二行是分数，10 分为满分．

编译后自定义校验器的名称必须为 `<problem>_e`，其中 `<problem>` 为题目名称．在配置题目时选择自定义校验器，然后选择需要的自定义校验器即可．

在试题管理中题目配置的地方将提交方式由源代码改为答案文件，然后选择自定义校验器，可以测试提交答案题．

### 注意事项

已确认需要注意的内容：

-   需要注意及时保存比赛，否则操作时可能闪退．为了确保不会闪退可以尝试多次保存比赛，或进行一次修改时就保存比赛．
-   没有进行过评测时不要点击上面的成绩统计，否则将会导致 Arbiter 直接闪退．
-   由于 Linux 运行时栈限制，如果要开无限栈，应在终端先输入 `ulimit -s unlimited` 后执行 `arbiter_local` 打开测评器，否则可能出现 `Exceeding memory limit` 的问题．
-   对于正式测评，在题目准备时需要让所有题目空间限制一致．测评时将命令中的 `unlimited` 换为题目空间限制的千字节数（KiB），如：题目空间限制为 512 MiB，则命令为 `ulimit -s $((512 * 1024))`．导致这一问题的主要原因是直接启动 Arbiter，其父进程为 GNOME，子进程继承了父进程的栈空间限制．
-   软件的工作目录不建议包含空格，若包含空格的话很可能会导致创建比赛时所有的默认校验器都无法拷贝进 filter 目录中（即 filter 目录为空）．此时进行评测会出现全部爆 0 的情况，同时生成的 result 文件中可以看到 `Compile Failed.` 的提示．
-   查看代码时提示「未找到答案文件」指的是没有找到选手的源代码．

存疑的内容：

-   很容易死机，如大量测评时移动鼠标会导致死机．
-   不定时闪退（一部分原因是没有及时保存比赛）．
-   修改比较方式后有概率会出现修改失败的情况，即比较方式修改后未被应用．
-   配置时需要注意权限问题，但确保使用同一用户建立比赛，拷贝数据和进行测评的情况下不会出现权限问题．

### 漏洞

由于长期缺乏维护，系统存在一些漏洞，如可以使用 `#pragma G++ optimize("O2")` 和 `__attribute__((__optimize__("-O2")))` 等．可以使用 [gcc-plugins-for-oi](https://github.com/xdu-icpc/gcc-plugins-for-oi) 在编译期实现对这些命令的检测．

### 评价

Arbiter 1.0.2 在开发完成后就一直没有实质性更新，导致测评体验极差，UI 脱离现代审美．在 NOI Linux 1.4.1 中，它和 NOI Linux 自带的 GUIDE 一样沦为选手与教练疯狂吐槽的对象．在 NOI Linux 2.0 中，除了比较器移除了源代码和软件整体使用 Qt 5 重新编译外，并没有很大的变化，一些稳定性问题仍未得到解决．

??? note "附：ren 和 rename 命令的使用方法"
    在 Windows 操作系统中自带了一个修改文件名称的命令：`ren`．
    
    命令语法如下：
    
    ```shell
    ren [<drive>:][<path>]<filename1> <filename2>
    ```
    
    如果我们需要对当前工作目录下的所有的文件进行修改，比如将所有的 out 文件修改为 ans 文件，可以执行如下命令：
    
    ```shell
    ren *.out *.ans
    ```
    
    如果是在 NOI Linux 2.0 环境中进行此类修改，似乎目前比较好用的是 `rename` 命令，但它不是 NOI Linux 2.0 环境内自带的命令，所以你要先进行安装：
    
    ```shell
    sudo apt install rename
    ```
    
    注：如果执行后提示 `E: Unable to locate package package_name`，你需要先执行这个命令：`sudo apt-get update`
    
    安装完成后，就可以正常使用 `rename` 命令了．`rename` 命令的使用类似于直接的文本替换，其在 NOI Linux 2.0 环境下的命令语法如下：
    
    ```shell
    rename 's/<修改前的文本>/<修改后的文本>/' <filename>
    ```
    
    其中 `<filename>` 可以使用通配符 `*`，也可以指定其中一类文件（比如 `*.out`)．
    
    请注意在引号内末尾还有一个 `/`，如果少写了一个 `/`，`rename` 命令将会报错：`Substitution replacement not terminated at (user-supplied code)`．
    
    此时如果我们需要对当前工作目录下的所有的文件进行修改，比如将所有的 out 文件修改为 ans 文件，可以这么写：
    
    ```shell
    rename 's/\.out/\.ans/' *
    ```
    
    其中 `\.` 表示对 `.` 进行转义．
    
    （温馨提示：如果少写了 `\.`，假如你的文件里有个 `outtest.out`，这条命令执行过后文件将会被修改成 `anstest.out`)
    
    类似的，如果你需要对所有名为 `atmost<x>.ans` 的文件进行统一修改（其中 `<x>` 代表测试点编号），将它们都修改为 `test<x>.ans`，不妨这么写：
    
    ```shell
    rename 's/atmost/test/' *.ans
    ```


## tools/judger/ccr-plus.md

author: Ir1d, HeRaNO, NachtgeistW, i-Yirannn, bear-good, ranwen, CoelacanthusHex, billchenchina, Tiger3018, Xeonacid

## CCR Plus

**CCR Plus** 是一款适用于 NOI 系列比赛的开源的跨平台测评环境，使用 Qt 编写，目前支持 Windows 和 Linux．

源代码托管于 [sxyzccr/CCR-Plus](https://github.com/sxyzccr/CCR-Plus)．


## tools/judger/cena.md

author: Ir1d, HeRaNO, NachtgeistW, i-Yirannn, bear-good, ranwen, CoelacanthusHex, billchenchina, Tiger3018, Xeonacid

## Cena

**Cena** 是由刘其帅和李子星使用 Pascal 语言编写的开源评测工具，是流传最广泛的本地评测工具．Cena 最初开源于 Google Code 平台，由于不明原因 Google 删除了 Cena 项目．目前可以在 [Web Archive](https://web.archive.org/web/20131023112258/http://code.google.com/p/cena/) 上找到 Cena 的官网．

Cena 对权限的限制不是很明确，测试的时候可以读测点 AC．

Cena 的源代码托管于 [oi-archive/cena](https://github.com/oi-archive/cena)．


## tools/judger/index.md

author: Ir1d, HeRaNO, NachtgeistW, i-Yirannn, bear-good, ranwen, CoelacanthusHex, billchenchina, Tiger3018, Xeonacid, renbaoshuo

**评测软件** 是用于本地测试分数的软件．使用者在将代码提交到 OJ 前，可以使用评测软件对自己的程序估分．

本部分介绍了以下几种评测软件：

-   [Arbiter](./arbiter.md)
-   [CCR Plus](./ccr-plus.md)
-   [Cena](./cena.md)
-   [Lemon](./lemon.md)


## tools/judger/lemon.md

author: Ir1d, HeRaNO, NachtgeistW, i-Yirannn, bear-good, ranwen, CoelacanthusHex, billchenchina, Tiger3018, Xeonacid

## Lemon

???+ warning "Warning"
    macOS 下 Lemon 可能会出现内存测试不准确的情况，因为 macOS 缺少部分 Linux 的监测工具，且 Lemon-Linux 也没有针对 macOS 进行优化．

**Lemon** 是 zhipeng-jia 编写的开源评测工具，源代码托管于 [zhipeng-jia/project-lemon](https://github.com/zhipeng-jia/project-lemon)．

### 可直接运行的版本

-   Ir1d 提供了一份 Linux 下编译好的版本，源代码托管于 [FreestyleOJ/Project\_lemon](https://github.com/FreestyleOJ/Project_lemon/tree/Built)．
-   （已停止维护）Menci 提供了一份更新的版本，源代码托管于 [Menci/Lemon](https://github.com/Menci/Lemon/)．
-   （已停止维护）Dust1404 维护了一份支持子文件夹和单题测试等功能的版本，源代码托管于 [Dust1404/Project\_LemonPlus](https://github.com/Dust1404/Project_LemonPlus)．
-   iotang 和 Coelacanthus 维护了一份支持子文件夹和单题测试等功能的版本，源代码托管于 [Project-LemonLime/Project\_LemonLime](https://github.com/Project-LemonLime/Project_LemonLime)．

### 自行编译

Ubuntu：

```bash
sudo apt update
sudo apt install qt5-default build-essential git -y
git clone --depth=1 https://github.com/Menci/Lemon.git
cd lemon
# 可以修改 -j 后面的数字来调整 make job 的线程数
./make -j2
sudo install -Dm755 -t /usr/bin/ Lemon
```

如要编译 LemonLime，请参阅 LemonLime 的 [编译手册](https://github.com/Project-LemonLime/Project_LemonLime/blob/master/BUILD.md)．

### 数据格式

首先打开 lemon 选择「新建试题」，然后打开新建试题的文件夹．

题目和数据应该如以下格式所示：

```text
├── data
│   ├── gendata.py
│   ├── product
│   │   ├── product100.in
│   │   ├── product100.out
│   │   ├── product10.in
│   │   ├── product10.out
│   │   ├── product11.in
...
```

当所有试题添加完成后，回到 lemon 选择「自动添加试题」．此时题目和数据点将显示在 lemon 当中．


## tools/latex.md

## 介绍

### 什么是 LaTeX

LaTeX（读作/ˈlɑːtɛx/或/ˈleɪtɛx/）是一个让你的文档看起来更专业的排版系统，而不是文字处理器．它尤其适合处理篇幅较长、结构严谨的文档，并且十分擅长处理公式表达．它是免费的软件，对大多数操作系统都适用．

LaTeX 基于 TeX（Donald Knuth 在 1978 年为数字化排版设计的排版系统）．TeX 是一种电脑能够处理的低级语言，但大多数人发现它很难使用．LaTeX 正是为了让它变得更加易用而设计的．目前 LaTeX 的版本是 LaTeX 2e．

如果你习惯于使用微软的 Office Word 处理文档，那么你会觉得 LaTeX 的工作方式让你很不习惯．Word 是典型的「所见即所得」的编辑器，你可以在编排文档的时候查看到最终的排版效果．但使用 LaTeX 时你并不能方便地查看最终效果，这使得你专注于内容而不是外观的调整．

一个 LaTeX 文档是一个以 `.tex` 结尾的文本文件，可以使用任意的文本编辑器编辑，比如 Notepad，但对于大多数人而言，使用一个合适的 LaTeX 编辑器会使得编辑的过程容易很多．在编辑的过程中你可以标记文档的结构．完成后你可以进行编译——这意味着将它转化为另一种格式的文档．它支持多种格式，但最常用的是 PDF 文档格式．

### 在开始之前

下面列出在本文中使用到的记号：

-   希望你实施的操作会被打上一个箭头 $\rightarrow$；
-   你输入的字符会被装进代码块中；
-   菜单命令与按钮的名称会被标记为 **粗体**．

### 一些概念

如果需要编写 LaTeX 文档，你需要安装一个「发行版」，常用的发行版有 [TeX Live](http://tug.org/texlive/)、[MikTeX](https://miktex.org/) 和适用于 macOS 用户的 MacTeX（实际上是 TeX Live 的 macOS 版本），至于 [CTeX](http://www.ctex.org/) 则现在不推荐使用．TeX Live 和 MacTeX 带有几乎所有的 LaTeX 宏包；而 MikTeX 只带有少量必须的宏包，其他宏包将在需要时安装．

TeX Live 和 MikTeX 都带有 TeXworks 编辑器，你也可以安装功能更多的 TeXstudio 编辑器，或者自行配置 Visual Studio Code 或 Notepad++ 等编辑器．下文所使用的编辑器是运行在 Windows 7 上的 TeXworks．

大部分发行版都带有多个引擎，如 pdfTeX 和 XeTeX．对于中文用户，推荐使用 XeTeX 以获得 Unicode 支持．

TeX 有多种格式，如 Plain TeX 和 LaTeX．现在一般使用 LaTeX 格式．所以，你需要使用与你所使用的格式打包在一起的引擎．如对于 pdfTeX，你需要使用 pdfLaTeX，对于 XeTeX 则是 XeLaTeX．

扩展阅读：[TeX 引擎、格式、发行版之介绍](https://liam.page/2018/11/26/introduction-to-TeX-engine-format-and-distribution/)．

### 环境配置

对于 Windows 用户，你需要下载 TeX Live 或 MikTeX．国内用户可以使用 [清华大学 TUNA 镜像站](https://mirrors.tuna.tsinghua.edu.cn/)，请点击页面右侧的「获取下载链接」按钮，并选择「应用软件」标签下的「TeX 排版系统」即可下载 TeX Live 或 MikTeX 的安装包，其中 TeX Live 的安装包是一个 ISO 文件，需要挂载后以管理员权限执行 `install-tl-advanced.bat`．

对于 macOS 用户，清华大学 TUNA 镜像站同样提供 MacTeX 和 macOS 版 MikTeX 的下载．

对于 Linux 用户，如果使用 TeX Live，则同样下载 ISO 文件，执行 `install-tl` 脚本；如果使用 MikTeX，则按照 [官方文档](https://miktex.org/download#unx) 进行安装．

## 文档结构

### 基本要素

$\rightarrow$ 打开 TeXworks．

一个新的文档会被自动打开．

$\rightarrow$ 进入 **Format** 菜单，选择 **Line Numbers**．

行号并不是要素，但它可以帮助你比较代码与屏幕信息，找到错误．

$\rightarrow$ 进入 **Format** 菜单，选择 **Syntax Coloring**，然后选择 **LaTeX**．

语法色彩会高亮代码，使得代码更加易读．

$\rightarrow$ 输入以下文字：

```tex
\documentclass[a4paper, 12pt]{article}

\begin{document}
  A sentence of text.
\end{document}
```

`\documentclass` 命令必须出现在每个 LaTeX 文档的开头．花括号内的文本指定了文档的类型．**article** 文档类型适合较短的文章，比如期刊文章和短篇报告．其他文档类型包括 **report**（适用于更长的多章节的文档，比如博士生论文），**proc**（会议论文集），**book** 和 **beamer**．方括号内的文本指定了一些选项——示例中它设置纸张大小为 A4，主要文字大小为 12pt．

`\begin{document}` 和 `\end{document}` 命令将你的文本内容包裹起来．任何在 `\begin{document}` 之前的文本都被视为前导命令，会影响整个文档．任何在 `\end{document}` 之后的文本都会被忽视．

空行不是必要的，但它可以让长的文档更易读．

$\rightarrow$ 按下 **Save** 按扭；$\rightarrow$ 在 **Libraries>Documents** 中新建一个名为 **LaTeX course** 文件夹；$\rightarrow$ 将你的文档命名为 **Doc1** 并将其保存为 **TeX document** 放在这个文件夹中．

将不同的 LaTeX 文档放在不同的目录下，在编译的时候组合多个文件是一个很好的想法．

$\rightarrow$ 确保 typeset 菜单设置为了 **xeLaTeX**．$\rightarrow$ 点击 **Typeset** 按扭．

这时你的源文件会被转换为 PDF 文档，这需要花费一定的时间．在编译结束后，TeXworks 的 PDF 查看器会打开并预览生成的文件．PDF 文件会被自动地保存在与 TeX 文档相同的目录下．

### 处理问题

如果在你的文档中存在错误，TeXworks 无法创建 PDF 文档时，**Typeset** 按扭会变成一个红叉，并且底部的终端输出会保持展开．这时：

$\rightarrow$ 点击 **Abort typesetting** 按扭．$\rightarrow$ 阅读终端输出的内容，最后一行可能会给出行号表示出现错误的位置．$\rightarrow$ 找到文档中对应的行并修复错误．$\rightarrow$ 再次点击 **Typeset** 按扭尝试编译源文件．

### 添加文档标题

`\maketitle` 命令可以给文档创建标题．你需要指定文档的标题．如果没有指定日期，就会使用现在的时间，作者是可选的．

$\rightarrow$ 在 `\begin{document}` 和 命令后紧跟着输入以下文本：

```tex
\title{My First Document}
\author{My Name}
\date{\today}
\maketitle
```

你的文档现在长成了这样：

```tex
\documentclass[a4paper, 12pt]{article}

\begin{document}
  \title{My First Document}
  \author{My Name}
  \date{\today}
  \maketitle

  A sentence of text.
\end{document}
```

$\rightarrow$ 点击 **Typeset** 按扭，核对生成的 PDF 文档．

要点笔记：

-   `\today` 是插入当前时间的命令．你也可以输入一个不同的时间，比如 `\date{November 2013}`．
-   **article** 文档的正文会紧跟着标题之后在同一页上排版．**report** 会将标题置为单独的一页．

### 章节

如果需要的话，你可能想将你的文档分为章（Chatpers）、节（Sections）和小节（Subsections）．下列分节命令适用于 **article** 类型的文档：

-   `\section{...}`
-   `\subsection{...}`
-   `\subsubsection{...}`
-   `\paragraph{...}`
-   `\subparagraph{...}`

花括号内的文本表示章节的标题．对于 **report** 和 **book** 类型的文档我们还支持 `\chapter{...}` 的命令．

$\rightarrow$ 将 "A sentence of text." 替换为以下文本：

```tex
\section{Introduction}
This is the introduction.

\section{Methods}

\subsection{Stage 1}
The first part of the methods.

\subsection{Stage 2}
The second part of the methods.

\section{Results}
Here are my results.
```

你的文档会变成

```tex
\documentclass[a4paper, 12pt]{article}

\begin{document}
  \title{My First Document}
  \author{My Name}
  \date{\today}
  \maketitle

  \section{Introduction}
  This is the introduction.

  \section{Methods}

  \subsection{Stage 1}
  The first part of the methods.

  \subsection{Stage 2}
  The second part of the methods.

  \section{Results}
  Here are my results.
\end{document}
```

$\rightarrow$ 点击 **Typeset** 按扭，核对 PDF 文档．应该是长这样的：

![p1](images/latex-for-beginners-1.png)

### 创建标签

你可以对任意章节命令创建标签，这样他们可以在文档的其他部分被引用．使用 `\label{labelname}` 对章节创建标签．然后输入 `\ref{labelname}` 或者 `\pageref{labelname}` 来引用对应的章节．

$\rightarrow$ 在 `\subsection{Stage 1}` 下面另起一行，输入 `\label{sec1}`．$\rightarrow$ 在 **Results** 章节输入 `Referring to section \ref{sec1} on page \pageref{sec1}`．

你的文档会变成这样：

```tex
\documentclass[a4paper, 12pt]{article}

\begin{document}
  \title{My First Document}
  \author{My Name}
  \date{\today}
  \maketitle

  \section{Introduction}
  This is the introduction.

  \section{Methods}

  \subsection{Stage 1}
  \label{sec1} The first part of the methods.

  \subsection{Stage 2}
  The second part of the methods.

  \section{Results}
  Here are my results. Referring to section \ref{sec1} on page \pageref{sec1}
\end{document}
```

$\rightarrow$ 编译并检查 PDF 文档（你可能需要连续编译两次）：

![p2](images/latex-for-beginners-2.png)

### 生成目录（TOC）

如果你使用分节命令，那么可以容易地生成一个目录．使用 `\tableofcontents` 在文档中创建目录．通常我们会在标题的后面建立目录．

你可能也想更改页码为罗马数字（i,ii,iii）．这会确保文档的正文从第 1 页开始．页码可以使用 `\pagenumbering{...}` 在阿拉伯数字和罗马数字见切换．

$\rightarrow$ 在 `\maketitle` 之后输入以下内容：

```tex
\pagenumbering{roman}
\tableofcontents
\newpage
\pagenumbering{arabic}
```

`\newpage` 命令会另起一个页面，这样我们就可以看到 `\pagenumbering` 命令带来的影响了．你的文档的前 14 行长这样：

```tex
\documentclass[a4paper, 12pt]{article}

\begin{document}

\title{My First Document}
\author{My Name}
\date{\today}
\maketitle

\pagenumbering{roman}
\tableofcontents
\newpage
\pagenumbering{arabic}
```

$\rightarrow$ 编译并核对文档（可能需要多次编译，下文不赘述）．

文档的第一页长这样：

![p3](images/latex-for-beginners-3.png)

第二页：

![p4](images/latex-for-beginners-4.png)

## 文字处理

### 中文字体支持

阅读本文学习 LaTeX 的人，首要学会的自然是 LaTeX 的中文字体支持．事实上，让 LaTeX 支持中文字体有许多方法．在此我们仅给出最 **简洁** 的解决方案：使用 CTeX 宏包．只需要在文档的前导命令部分添加：

```tex
\usepackage[UTF8]{ctex}
```

就可以了．在编译文档的时候使用 `xelatex` 命令，因为它是支持中文字体的．

### 字体效果

LaTeX 有多种不同的字体效果，在此列举一部分：

```tex
\textit{words in italics} \textsl{words slanted} \textsc{words in smallcaps} \textbf{words
in bold} \texttt{words in teletype} \textsf{sans serif words} \textrm{roman
words} \underline{underlined words}
```

效果如下：

![p5](images/latex-for-beginners-5.png)

$\rightarrow$ 在你的文档中添加更多的文本并尝试各种字体效果．

### 彩色字体

为了让你的文档支持彩色字体，你需要使用包（package）．你可以引用很多包来增强 LaTeX 的排版效果．包引用的命令放置在文档的前导命令的位置（即放在 `\begin{document}` 命令之前）．使用 `\usepackage[options]{package}` 来引用包．其中 **package** 是包的名称，而 **options** 是指定包的特征的一些参数．

使用 `\usepackage{color}` 后，我们可以调用常见的颜色：

![p6](images/latex-for-beginners-6.png)

使用彩色字体的代码为

```tex
{\color{colorname}text}
```

其中 **colorname** 是你想要的颜色的名字，**text** 是你的彩色文本内容．注意到示例效果中的黄色与白色是有文字背景色的，这个我们同样可以使用 Color 包中的 `\colorbox` 命令来达到．用法如下：

```tex
\colorbox{colorname}{text}
```

$\rightarrow$ 在 `\begin{document}` 前输入 `\usepackage{color}`．$\rightarrow$ 在文档内容中输入 `{\color{red}fire}`．$\rightarrow$ 编译并核对 PDF 文档内容．

单词 fire 应该是红色的．

你也可以添加一些参数来调用更多的颜色，甚至自定义你需要的颜色．但这部分超出了本书的内容．如果想要获取更多关于彩色文本的内容请阅读 LaTeX Wikibook 的 [Colors 章节](http://en.wikibooks.org/wiki/LaTeX/Colors)．

### 字体大小

接下来我们列举一些 LaTeX 的字体大小设定命令：

```tex
normal size words {\tiny tiny words} {\scriptsize scriptsize words}
{\footnotesize footnotesize words} {\small small words} {\large large words}
{\Large Large words} {\LARGE LARGE words} {\huge huge words}
```

效果如下：

![p7](images/latex-for-beginners-7.png)

$\rightarrow$ 尝试为你的文本调整字体大小．

### 段落缩进

LaTeX 默认每个章节第一段首行顶格，之后的段落首行缩进．如果想要段落顶格，在要顶格的段落前加 `\noindent` 命令即可．如果希望全局所有段落都顶格，在文档的某一位置使用 `\setlength{\parindent}{0pt}` 命令，之后的所有段落都会顶格．

### 列表

LaTeX 支持两种类型的列表：有序列表（enumerate）和无序列表（itemize）．列表中的元素定义为 `\item`．列表可以有子列表．

$\rightarrow$ 输入下面的内容来生成一个有序列表套无序列表：

```tex
\begin{enumerate}
  \item First thing

  \item Second thing
    \begin{itemize}
      \item A sub-thing

      \item Another sub-thing
    \end{itemize}

  \item Third thing
\end{enumerate}
```

$\rightarrow$ 编译并核对 PDF 文档．

列表长这样：

![p8](images/latex-for-beginners-8.png)

可以使用方括号参数来修改无序列表头的标志．例如，`\item[-]` 会使用一个杠作为标志，你甚至可以使用一个单词，比如 `\item[One]`．

下面的代码：

```tex
\begin{itemize}
  \item[-] First thing

  \item[+] Second thing
    \begin{itemize}
      \item[Fish] A sub-thing

      \item[Plants] Another sub-thing
    \end{itemize}

  \item[Q] Third thing
\end{itemize}
```

生成的效果为

![p9](images/latex-for-beginners-9.png)

### 注释和空格

我们使用 % 创建一个单行注释，在这个字符之后的该行上的内容都会被忽略，直到下一行开始．

下面的代码：

```tex
It is a truth universally acknowledged% Note comic irony
in the very first sentence , that a single man in possession of a good fortune,
must be in want of a wife.
```

生成的结果为

![p10](images/latex-for-beginners-10.png)

多个连续空格在 LaTeX 中被视为一个空格．多个连续空行被视为一个空行．空行的主要功能是开始一个新的段落．通常来说，LaTeX 忽略空行和其他空白字符，两个反斜杠（`\\`）可以被用来换行．

$\rightarrow$ 尝试在你的文档中添加注释和空行．

如果你想要在你的文档中添加空格，你可以使用 `\vspace{...}` 的命令．这样可以添加竖着的空格，高度可以指定．如 `\vspace{12pt}` 会产生一个空格，高度等于 12pt 的文字的高度．

### 特殊字符

下列字符在 LaTeX 中属于特殊字符：

```text
# $ % ^ & _ { } ~ \
```

为了使用这些字符，我们需要在他们前面添加反斜杠进行转义：

```tex
\# \$ \% \^{} \& \_ \{ \} \~{}
```

注意在使用 `^` 和 `~` 字符的时候需要在后面紧跟一对闭合的花括号，否则他们就会被解释为字母的上标，就像 `\^ e` 会变成 $\mathrm {\hat{e}}$．上面的代码生成的效果如下：

![p11](images/latex-for-beginners-11.png)

注意，反斜杠不能通过反斜杠转义（不然就变成了换行了），使用 `\textbackslash` 命令代替．

$\rightarrow$ 输入代码来在你的文档中生成下面内容：

![p12](images/latex-for-beginners-12.png)

询问专家或者查看本页面的 [源代码](https://github.com/OI-wiki/OI-wiki/blob/master/docs/tools/latex.md?plain=1) 获取帮助．

## 表格

表格（tabular）命令用于排版表格．LaTeX 默认表格是没有横向和竖向的分割线的——如果你需要，你得手动设定．LaTeX 会根据内容自动设置表格的宽度．下面的代码可以创一个表格：

```tex
\begin{tabular}{...}
```

省略号会由定义表格的列的代码替换：

-   `l` 表示一个左对齐的列；
-   `r` 表示一个右对齐的列；
-   `c` 表示一个向中对齐的列；
-   `|` 表示一个列的竖线；

例如，`{lll}` 会生成一个三列的表格，并且保存向左对齐，没有显式的竖线；`{|l|l|r|}` 会生成一个三列表格，前两列左对齐，最后一列右对齐，并且相邻两列之间有显式的竖线．

表格的数据在 `\begin{tabular}` 后输入：

-   `&` 用于分割列；
-   `\\` 用于换行；
-   `\hline` 表示插入一个贯穿所有列的横着的分割线；
-   `\cline{1-2}` 会在第一列和第二列插入一个横着的分割线．

最后使用 `\end{tabular}` 结束表格．举一些例子：

```tex
\begin{tabular}{|l|l|}
  Apples       & Green  \\
  Strawberries & Red    \\
  Orange       & Orange \\
\end{tabular}

\begin{tabular}{rc}
  Apples              & Green  \\
  \hline
  Strawberries        & Red    \\
  \cline{1-1} Oranges & Orange \\
\end{tabular}

\begin{tabular}{|r|l|}
  \hline
  8              & here's \\
  \cline{2-2} 86 & stuff  \\
  \hline
  \hline
  2008           & now    \\
  \hline
\end{tabular}
```

效果如下：

![p13](images/latex-for-beginners-13.png)

### 实践

尝试画出下列表格：

![p14](images/latex-for-beginners-14.png)

## 图表

本章介绍如何在 LaTeX 文档中插入图表．这里我们需要引入 **graphicx** 包．图片应当是 PDF，PNG，JPEG 或者 GIF 文件．下面的代码会插入一个名为 myimage 的图片：

```tex
\begin{figure}[h]
  \centering
  \includegraphics[width=1\textwidth]{myimage}
  \caption{Here is my image}
  \label{image-myimage}
\end{figure}
```

`[h]` 是位置参数，**h** 表示把图表近似地放置在这里（如果能放得下）．有其他的选项：**t** 表示放在页面顶端；**b** 表示放在页面的底端；**p** 表示另起一页放置图表．你也可以添加一个 **!** 参数来强制放在参数指定的位置（尽管这样排版的效果可能不太好）．

`\centering` 将图片放置在页面的中央．如果没有该命令会默认左对齐．使用它的效果是很好的，因为图表的标题也是居中对齐的．

`\includegraphics{...}` 命令可以自动将图放置到你的文档中，图片文件应当与 TeX 文件放在同一目录下．

`[width=1\textwidth]` 是一个可选的参数，它指定图片的宽度——与文本的宽度相同．宽度也可以以厘米为单位．你也可以使用 `[scale=0.5]` 将图片按比例缩小（示例相当于缩小一半）．

`\caption{...}` 定义了图表的标题．如果使用了它，LaTeX 会给你的图表添加「Figure」开头的序号．你可以使用 `\listoffigures` 来生成一个图表的目录．

`\label{...}` 创建了一个可以供你引用的标签．

### 实践

$\rightarrow$ 在你文档的前导命令中添加 `\usepackage{graphicx}`．$\rightarrow$ 找到一张图片，放置在你的 **LaTeX course** 文件夹下．$\rightarrow$ 在你想要添加图片的地方输入以下内容：

```tex
\begin{figure}[h!]
  \centering
  \includegraphics[width=1\textwidth]{ImageFilename}
  \caption{My test image}
\end{figure}
```

将 **ImageFilename** 替换为你的文件的名字（不包括后缀）．如果你的文件名有空格，就使用双引号包裹，比如 `"screen 20"`．

$\rightarrow$ 编译并核对文件．

## 公式

使用 LaTeX 的主要原因之一是它可以方便地排版公式．我们使用数学模式来排版公式．

### 插入公式

你可以使用一对 `$` 来启用数学模式，这可以用于撰写行内数学公式．例如 `$1+2=3$` 的生成效果是 $1+2=3$．

如果你想要行间的公式，可以使用 `$$...$$`（现在我们推荐使用 `\[...\]`，因为前者可能产生不良间距）．例如，`$$1+2=3$$` 的生产效果为

$$
1+2=3
$$

如果是生成带标号的公式，可以使用 `\begin{equation}...\end{equation}`．例如：

```tex
\begin{equation}
  1+2=3
\end{equation}
```

生成的效果为：

![equation](images/latex-equation.svg)

数字 6 代表的是章节的编号，仅当你的文档有设置章节时才会出现，比如 **report** 类型的文档．

使用 `\begin{eqnarray}...\end{eqnarray}` 来撰写一组带标号的公式．例如：

```tex
\begin{eqnarray}
  a & = & b + c \\
  & = & y - z
\end{eqnarray}
```

生成的效果为

![eqnarray](images/latex-eqnarray.svg)

要撰写不标号的公式就在环境标志的后面添加 `*` 字符，如 `{equation*}`，`{eqnarray*}`．

??? warning "Warning"
    可以发现，使用 `eqnarray` 时，会出现等号周围的空隙过大之类的问题．
    
    可以使用 `amsmath` 宏包中的 `align` 环境：
    
    ```tex
    \usepackage{amsmath}
    ...
    \begin{align}
      a & = b + c \\
        & = y - z
    \end{align}
    ```
    
    或在行间公式中使用 `aligned` 环境．它们的名字后面加上星号后，公式就不带标号了．
    
    详见 [更多阅读](#更多阅读) 中第一篇资料的「4.4 多行公式」．

### 数学符号

尽管一些基础的符号可以直接键入，但大多数特殊符号需要使用命令来显示．

本书只是数学符号使用的入门教程，LaTeX Wikibook 的数学符号章节是另一个更好更完整的教程．如果想要了解更多关于数学符号的内容请移步．如果你想找到一个特定的符号，可以使用 [Detexfiy](http://detexify.kirelabs.org)，它可以识别手写字符．

#### 上标和下标

上标（Powers）使用 `^` 来表示，比如 `$n^2$` 生成的效果为 $n^2$．

下标（Indices）使用 `_` 表示，比如 `$2_a$` 生成的效果为 $2_a$．

如果上标或下标的内容包含多个字符，请使用花括号包裹起来．比如 `$b_{a-2}$` 的效果为 $b_{a-2}$．

#### 分数

分数使用 `\frac{numerator}{denominator}` 命令插入．比如 `$$\frac{a}{3}$$` 的生成效果为

$$
\frac{a}{3}
$$

分数可以嵌套．比如 `$$\frac{y}{\frac{3}{x}+b}$$` 的生成效果为

$$
\frac{y}{\frac{3}{x}+b}
$$

#### 根号

我们使用 `\sqrt{...}` 命令插入根号．省略号的内容由被开根的内容替代．如果需要添加开根的次数，使用方括号括起来即可．

例如 `$$\sqrt{y^2}$$` 的生成效果为

$$
\sqrt{y^2}
$$

而 `$$\sqrt[x]{y^2}$$` 的生成效果为

$$
\sqrt[x]{y^2}
$$

#### 求和与积分

使用 `\sum` 和 `\int` 来插入求和式与积分式．对于两种符号，上限使用 `^` 来表示，而下限使用 `_` 表示．

`$$\sum_{x=1}^5 y^z$$` 的生成效果为

$$
\sum_{x=1}^5y^z
$$

而 `$$\int_a^b f(x)$$` 的生成效果为

$$
\int_a^b f(x)
$$

#### 希腊字母

我们可以使用反斜杠加希腊字母的名称来表示一个希腊字母．名称的首字母的大小写决定希腊字母的形态．例如

-   `$\alpha$`=$\alpha$
-   `$\beta$`=$\beta$
-   `$\delta, \Delta$`=$\delta, \Delta$
-   `$\pi, \Pi$`=$\pi, \Pi$
-   `$\sigma, \Sigma$`=$\sigma, \Sigma$
-   `$\phi, \Phi, \varphi$`=$\phi, \Phi, \varphi$
-   `$\psi, \Psi$`=$\psi, \Psi$
-   `$\omega, \Omega$`=$\omega, \Omega$

### 实践

$\rightarrow$ 撰写代码来生成下列公式：

![p15](images/latex-for-beginners-15.png)

如果需要帮助，可以查看本页面的 [源代码](https://github.com/OI-wiki/OI-wiki/blob/master/docs/tools/latex.md?plain=1)．

## 参考文献

### 介绍

LaTeX 可以轻松插入参考文献以及目录．本文会介绍如何使用另一个 BibTeX 文件来存储参考文献．

### BibTeX 文件类型

BibTeX 文件包含了所有你想要在你文档中引用的文献．它的文件后缀名为 `.bib`．它的名字应设置为你的 TeX 文档的名字．`.bib` 文件是文本文件．你需要将你的参考文献按照下列格式输入：

```text
@article{
    Birdetal2001,
    Author = {Bird, R. B. and Smith, E. A. and Bird, D. W.},
    Title = {The hunting handicap: costly signaling in human foraging strategies},
    Journal = {Behavioral Ecology and Sociobiology},
    Volume = {50},
    Pages = {9-19},
    Year = {2001} 
}
```

每一个参考文献先声名它的文献类型（reference type）．示例中使用的是 @article，其他的类型包括 @book，@incollection 用于引用一本书的中的章节，@inproceedings 用于引用会议论文．可以 [在此](http://en.wikibooks.org/wiki/LaTeX/Bibliography_Management) 查看更多支持的类型．

接下来的花括号内首先要列出一个引用键值（citation key）．必须保证你引用的文献的引用键值是不同的．你可以自定义键值串，不过使用第一作者名字加上年分会是一个表义清晰的选择．

接下来的若干行包括文献的若干信息，格式如下：

```text
Field name = {field contents},
```

你可以使用 LaTeX 命令来生成特殊的文字效果．比如意大利斜体可以使用 `\emph{Rattus norvegicus}`．

对于需要大写的字母，请用花括号包裹起来．BibTeX 会自动把标题中除第一个字母外所有大写字母替换为小写．比如 `Dispersal in the contemporary United States` 的生成效果为 $\text{Dispersal in the contemporary united states}$，而 `Dispersal in the contemporary {U}nited {S}tates` 的生成效果为 $\text{Dispersal in the contemporary United States}$．

你可以手写 BibTeX 文件，也可以使用软件来生成．

### 插入文献列表

使用下列命令在文档当前位置插入文献列表：

```tex
\bibliographystyle{plain}
\bibliography{references}
```

参考文献写在 `references.bib` 里．

### 参考文献标注

使用 `\cite{citationkey}` 来在你想要引用文献的地方插入一个标注．如果你不希望在正文中插入一个引用标注，但仍想要在文献列表中显示这次引用，使用 `\nocite{citationkey}` 命令．

想要在引用中插入页码信息，使用方括号：`\cite[p. 215]{citationkay}`．

要引用多个文献，使用逗号分隔：`\cite{citation01,citation02,citation03}`．

### 引用格式

#### 数字标号引用

LaTeX 包含了多种行内数字标号引用的格式：

**Plain** 方括号包裹数字的形式，如 $[1]$．文献列表按照第一作者的字母表顺序排列．每一个作者的名字是全称．

**Abbrv** 与 **plain** 是相同的，但作者的名字是缩写．

**Unsrt** 与 **plain** 是相同的，但文献列表的排序按照在文中引用的先后顺序排列．

**Alpha** 与 **plain** 一样，但引用的标注是作者的名字与年份组合在一起，不是数字，如 $[Kop10]$．

#### 作者日期引用

如果你想使用作者日期的引用，使用 **natbib** 包．它使用 `\citep{...}` 命令来生成一个方括号标注，如 $[Koppe,2010]$，使用 `\citet{...}` 来生成一个标注，只把年份放到方括号里，如 $Koppe [2010]$．[在此](http://mirror.ctan.org/macros/latex/contrib/natbib/natnotes.pdf) 查看它的更多用法．

Natbib 包也有三种格式：**plainnat**，**abbrvnat** 和 **unsrtnat**，他们与 **plain**，**abbrv** 和 **unsrt** 的效果是一样的．

#### 其他引用格式

如果你需要使用不同的格式，你需要在同一个文件夹下创建一个格式文件（`.bst` 文件），引用这个格式的时候使用它的文件名调用 `\bibliographystyle{...}` 命令实现．

### 实践

$\rightarrow$ 在同一文件夹下新建一个同名的 BibTeX 文件，用正确的格式输入参考文献的信息．$\rightarrow$ 切换到 TeX 文档，并使用 `\cite`，`\bibliographystyle` 和 `\bibliograph` 命令来引用文献．$\rightarrow$ 编译 TeX 文件．$\rightarrow$ 切换到 BibTeX 文件，并编译（点击 **Typeset** 按扭）$\rightarrow$ 切换到 TeX 文件并编译它 **两次**，然后核对 PDF 文档．

## 更多阅读

-   一份（不太）简短的 LATEX 2ε 介绍 <https://github.com/CTeX-org/lshort-zh-cn/releases/download/v6.02/lshort-zh-cn.pdf> 或 112 分钟了解 LaTeX 2ε.

-   LaTeX Project <http://www.latex-project.org/> Official website - has links to documentation, information about installing LATEX on your own computer, and information about where to look for help.

-   LaTeX Wikibook <http://en.wikibooks.org/wiki/LaTeX/> Comprehensive and clearly written, although still a work in progress. A downloadable PDF is also available.

-   Comparison of TeX Editors on Wikipedia <http://en.wikipedia.org/wiki/Comparison_of_TeX_editors> Information to help you to choose which L A TEX editor to install on your own computer.

-   TeX Live <http://www.tug.org/texlive/>"An easy way to get up and running with the TeX document production system". Available for Unix and Windows (links to MacTeX for MacOSX users). Includes the TeXworks editor.

-   Workbook Source Files <http://edin.ac/17EQPM1> Download the .tex file and other files needed to compile this workbook.

**本文译自 [http://www.docs.is.ed.ac.uk/skills/documents/3722/3722-2014.pdf](https://web.archive.org/web/20220309055041/http://www.docs.is.ed.ac.uk/skills/documents/3722/3722-2014.pdf)**, 依据其他文献略有修改．


## tools/oj-tool.md

本页面将介绍一些 OJ 工具．

## cf-tool

cf-tool 是 Codeforces 的命令行界面的跨平台（支持 Windows、Linux、macOS）工具，支持很多常用操作．

源码托管在 [xalanq/cf-tool](https://github.com/xalanq/cf-tool) 上．

![cf-tool 使用截图 1](./images/oj-tool-1.jpg)

![cf-tool 使用截图 2](./images/oj-tool-2.jpg)

### 特点

-   支持 Codeforces 中的所有编程语言．
-   支持 Contests 和 Gym．
-   提交代码．
-   动态刷新提交后的情况．
-   拉取问题的样例．
-   本地编译和测试样例．
-   拉取某人的所有代码．
-   从指定模板生成代码（包括时间戳，作者等信息）．
-   列出某场比赛的所有题目的整体信息．
-   用默认的网页浏览器打开题目页面、榜单、提交页面等．
-   丰富多彩的命令行．

### 下载

前往 [cf-tool/releases](https://github.com/xalanq/cf-tool/releases) 下载最新版．

之后的更新可以直接使用 `upgrade` 命令获取．

### 使用

将下载好的可执行文件 `cf`（或者 `cf.exe`）放置到合适的位置后（见常见问题的第二条），然后打开命令行，用 `cf config` 命令来配置一下用户名、密码和代码模板．

### 使用举例

以下简单模拟一场比赛的流程．

`cf race 1136`

要开始打 1136 这场比赛了！其中 1136 可以从比赛的链接获取，比方说这个例子的比赛链接就为 <https://codeforces.com/contest/1136>．

如果比赛还未开始，则该命令会进行倒计时．比赛已开始或倒计时完后，工具会自动用默认浏览器打开比赛的所有题目页面，并拉取样例到本地．

`cd 1136/a`

进入 A 题的目录，此时该目录下会包含该题的样例．

`cf gen`

用默认模板生成一份代码，在这里不妨设为 `a.cpp`．

`vim a.cpp`

用 Vim 写代码（或者用其他的编辑器或 IDE 进行）．

`cf test`

编译并测试样例．

`cf submit`

提交代码．

`cf list`

查看当前比赛各个题目的信息．

`cf stand`

用浏览器打开榜单，查看排名．

### 常见问题

1.  我双击了这个程序但是没啥效果

    cf-tool 是命令行界面的工具，你应该在终端里运行这个工具．

2.  我无法使用 `cf` 这个命令

    你应该将 `cf` 这个程序放到一个已经加入到系统变量 PATH 的路径里（比如说 Linux 里的 `/usr/bin/`）．

    不明白的话请直接搜索「PATH 添加路径」．

3.  如何加一个新的测试数据

    新建两个额外的测试数据文件 `inK.txt` 和 `ansK.txt`（K 是包含 0\~9 的字符串）．

4.  怎样在终端里启用 tab 补全命令

    使用这个工具 [Infinidat/infi.docopt\_completion](https://github.com/Infinidat/infi.docopt_completion) 即可．

    注意：如果有一个新版本发布（尤其是添加了新命令），你应该重新运行 `docopt-completion cf`．

## Codeforces Visualizer

官网：[Codeforces Visualizer](https://cfviz.netlify.app)

源码托管在 [sjsakib/cfviz](https://github.com/sjsakib/cfviz/) 上．

这个网站有三个功能：

-   用炫酷的图表来可视化某个用户的各种信息（比如通过题目的难度分布）．
-   对比两个用户．
-   计算一场比赛的 Rating 预测．

## Competitive Companion

这个工具是一个浏览器插件，用于解析网页里面的测例数据．它支持解析几乎所有的主流 oj 平台（比如 Codeforces、AtCoder）．使用这个插件后，再也不用手动复制任何的测例数据．

源码托管在 [jmerle/competitive-companion](https://github.com/jmerle/competitive-companion) 上．

使用方法：

-   在谷歌或者火狐浏览器上安装插件．该工具会将解析到的测例数据以 JSON 格式的形式发到指定的端口．
-   在本地安装任何可以从端口监听读取数据的工具即可，可以参考 [官方给出的示例](https://github.com/jmerle/competitive-companion-example)．

图片演示：

![Competitive Companion 使用演示](images/oj-tool-3.apng)

使用 [zqxyz73](https://github.com/zqxyz73) 同学的 [bytetools](https://github.com/zqxyz73/bytetools) 完成演示．

## ac-predictor

ac-predictor 是一个在 atcoder rating 更新前提前知道比赛 rating 变化的插件．

这个工具是一个 tampermonkey 脚本，所以你需要首先安装 [tampermonkey](https://www.tampermonkey.net/)．

完成后来到 [greasyfork](https://greasyfork.org/zh-CN/scripts/369954-ac-predictor)，点击安装即可．

安装完成后，比赛的排行榜界面会显示每个用户的 rating 变化预测．

这个工具有一个经由 [GoodCoder666](https://github.com/GoodCoder666) 汉化的版本，点击 [这里](https://greasyfork.org/zh-CN/scripts/458528-ac-predictor-cn) 以安装．


## tools/polygon.md

author: ouuan, NachtgeistW

本页面将简要介绍多人协作出题平台 Polygon．

## 简介

### 什么是 Polygon

网址：[Index Page - Polygon](https://polygon.codeforces.com)

Polygon 是一个支持多人协作的出题平台，功能非常完善．官网描述为「Polygon 的使命是为创建编程竞赛题目提供平台．」

在 Codeforces (CF) 出题必须使用 Polygon．在其它地方出题，尤其是多人合作出题时，使用 Polygon 也是不错的选择．

### 优点

-   有版本管理系统，多人合作时不会乱成一团，也不需要互相传文件．

-   出题系统完善，validator、generator、checker、solutions 环环相扣，输出自动生成．

-   可以为 solutions 设置标签，错解 AC、正解未 AC 都会警告，方便地逐一卡掉错解．

-   可以方便地对拍，拍出来的数据可以直接添加到题目数据中．

-   发现问题可以提 issue，而不会被消息刷屏却一直没有 fix．

-   为日后出 CF 做准备．

-   ……

## 题目列表

题目列表中会显示一道题目的基本信息，如题面、题解撰写情况、数据生成情况以及 std、validator 和 checker 的设置．

可以双击题目列表的 "Name" 这一栏来写上 note，比如需要提醒自己做的事（need to add more tests/need to write tutorial），或者是这道题预订的 score distribution，可以根据自己的需要随意填写，当然也可以空着．

"Rev." 中的 "x/y" 的 x 指当前题目版本，y 指 package 的版本．如果两者不一样 y 会显示为红色．

"Edit session" 中的 "Start" 是指你的账号还没有看过这道题，"Continue (x) Discard" 是指你的账号处于这个题目的第 x 个版本，点击 "Start" 或 "Continue (x)" 就会进入题目管理界面，点击 "Discard" 会 **不可恢复地** 撤销你的所有更改，回到没有看过这题的状态．

如果你的账号上有一道题的更改没有提交，题目列表中这一整行就会变红．

## 题目管理

Polygon 的大部分功能都不需要学，能看懂英文就基本能用了．

???+ warning "Warning"
    题面不能使用 Markdown，只能用 TeX．

-   Invocation 是用来测试 solution 的．

-   Stress 是用来对拍的．

-   数据在 Tests 中用 generator 造，generator 在 Files 中上传．

### General Info

在这个页面中可以设置题目的时间限制、空间限制、题目类型、题目的标签、所属比赛．

在页面的最下方的 "statement sketch" 和 "tutorial sketch" 可以编辑题面、题解的 **草稿**，注意这两项不会出现在正式的题面、题解上．

### Statement

这个页面是用来写题面和题解的．还可以通过 "Review" 按钮来查看题面、validator 与 checker，一般用于审核．

题面和题解都需要使用 TeX 的语法，不能使用 Markdown．例如，需要使用 `\textbf{text}` 而不是 `**text**`．但 Polygon 支持的实际上是 TeX 的一个非常小的子集，具体可以自己尝试．

可以通过最上方的 "In HTML" 链接查看渲染后的题面，通过 "Tutorial in HTML" 查看渲染后的题解．

如果需要在题面中添加图片，需要先在下面的 "Statement Resource Files" 中上传图片，然后在题面中加上 `\includegraphics{filename.png}`．

### Files

"Source Files" 是用来存放 **除了 solutions 外** 的其它代码的，如 validator、checker、generator，如果是 IO 式交互题还有 interactor．

如果这些代码需要 include 其它文件，例如 [Tree-Generator](https://github.com/ouuan/Tree-Generator)，需要放在 "Resource Files" 中．

grader 式交互参见 [官方教程](https://codeforces.com/blog/entry/66916)．

### Checker

testlib.h 提供了一些内置的 checker，在选择框中有简要介绍，也可以选择后再点 "View source" 查看源码．

如果需要自己编写 checker，请参考 [checker 教程](./testlib/checker.md)．

下面的 "Checker tests" 是通过 "Add test" 添加若干组输出以及对应的期望评测结果，然后点击 "Run tests" 就可以测试 checker 是否正确返回了评测结果．

### Interactor

仅 IO 式交互题需要，请参考 [interactor 教程](./testlib/interactor.md)．

### Validator

validator 用来检测数据合法性，编写请参考 [validator 教程](./testlib/validator.md)．

下面的 "Validator tests" 类似于 "Checker tests"，需要提供输入和期望是否合法，用来测试 validator．

### Tests

这个页面是用来管理数据的．

在 Polygon 上，推荐的做法是使用少量 **带命令行参数** 的 [generator](./testlib/generator.md) 来生成数据，而不是写一堆 generator 或者每生成一组数据都修改 generator．并且，只需要生成输入，输出会自动生成．

"Testset" 就是一个测试集，如果是给 CF 出题需要手动添加 "pretests" 这个 Testset，并且 "pretests" 需要是 "tests" 的子集．

"Add Test" 是手动添加一组数据，一般用于手动输入样例或较小的数据．虽然可以通过文件上传数据，但这是 **不推荐的**，数据应该要么是手动输入的要么是使用 generator 在某个参数下生成的．

如果勾选了 "Use in statements"，这组数据就会成为样例，自动加在题面里．如果需要题面里显示的不是样例的输入输出（一般用于交互题），就可以点 "If you want to specify custom content of input or output data for statements click here"，然后输入你想显示在题面中的输入输出．

Tests 页面的下方是用来输入生成数据的脚本的，如 `generator-name [params] > test-index`．可以使用 `generator-name [params] > $`，就不用手动指定测试点编号了．

可以参考 [Polygon 提供的教程](https://polygon.codeforces.com/docs/freemarker-manual) 使用 Freemarker 来批量生成脚本．

"Preview Tests" 可以预览生成的数据．

### Stresses

这个页面是用来对拍的．

点击 "Add Stress" 就可以添加一组对拍，"Script pattern" 是一个生成数据的脚本，其中可以使用 "\[10..100]" 之类的来表示在一个范围内随机选择．

然后运行对拍，如果拍出错就会显示 "Crashed"，并且可以一键把这组数据加到 Tests 中．

### Solution Files

这个页面是用来放解这道题的代码的，可以是正解也可以是错解．将错解传上来可以便捷地卡掉它们，也可以提醒自己需要卡掉它们．

### Invocations

这个页面是用来运行 solutions 的．

选择代码和测试点就可以运行了，之后可以在列表里点进去（"View"）查看详细信息．

评测状态 "FL" 表示评测出错了，一般是数据没有过 validate 或者 validator/checker/interactor 之类的 RE 了．"RJ" 有两种情况，一种是出现了 "FL"，另一种是这份代码第一个测试点就没有通过．

如果用时在时限的一半到两倍之间，会用黄色标识出来．

如果数据中存在变量没有达到最小值或最大值，会在最下方提醒．

### Issues

用来提 Issue 的地方．

### Packages

Package 包含了一道题的全部信息，在出 CF 时是 CF 评测的依据（例如，如果赛时要修锅，更新了 package 才会影响到 CF），其它时候可以用来导出．

"Verify" 是测试所有 solution 都符合标签（AC、WA、TLE），并且 checker 通过 checker tests，validator 通过 validator tests．

### Manage access

管理题目权限．

### 侧边栏

第一栏会显示一些基本信息，如果有哪里不符合规范（如 tests 没有包含 pretests、有重复的测试点）就会显示为黄色，鼠标移上去会显示具体信息．

"View changes" 可以看修改的历史记录．需要注意的是 "switch" 不能用来回退到某一个版本，只能在某个版本的基础上进行不产生冲突的修改，而这实际上是没有意义的，所以 switch 相当于是只读的．

"Update Working Copy" 是获取（他人的）更新．

"Commit Changes" 是提交你的更新．

commit 时如果有不合规范、需要警告的地方会列出来．

## 比赛管理

如果要出一场比赛，可以通过 "New Contest" 来创建比赛，就可以更加方便地管理题目．

比赛管理页面的题目列表右上角的 "Add problems?" 是把一道已有的题目加到比赛里．

侧边栏的 "New problem" 是新建一道题目加到比赛里．

上面的 "Manage problem access" 是查看每道题的权限，下面的 "Manage developers list" 是管理有这场比赛的权限的人．通过 "New problem" 创建一道题以及添加一个新的 developer 时会自动添加权限，但通过 "Add problems?" 加进来的题不会给已有的 developer 权限．

侧边栏还可以预览所有题面、所有题解、所有 validator & checker，下载整个比赛的 package，给题目重新编号．

## 冲突解决

在多人合作使用 Polygon 命题时，如果当前修改的题目版本与远程的题目版本不同，并且在从远程获取最新版本或提交更新时，修改的文件无法自动合并，就会发生冲突（Conflicted）．

发生冲突后，Polygon 会在冲突题目选项中提供 "Resolve conflicts" 选项，用户可以在里面对冲突文件进行冲突解决．


## tools/special-judge.md

author: Xeonacid, NachtgeistW, 2014CAIS01, sshwy, Chrogeek, Menci, yzy-1

本页面主要介绍部分评测工具/OJ 的 spj 编写方法．

## 简介

**Special Judge**（简称：spj，别名：checker）是当一道题有多组解时，用来判断答案合法性的程序．

???+ warning "Warning"
    spj 还应当判断文件尾是否有多余内容，及输出格式是否正确（如题目要求数字间用一个空格隔开，而选手却使用了换行）．但是，目前前者只有 Testlib 可以方便地做到这一点，而后者几乎无人去特意进行这种判断．
    
    判断浮点数时应注意 NaN．不合理的判断方式会导致输出 NaN 即可 AC 的情况．
    
    在对选手文件进行读入操作时应该要检查是否正确读入了所需的内容，防止造成 spj 的运行错误．（部分 OJ 会将 spj 的运行错误作为系统错误处理）

???+ note "Note"
    以下均以 C++ 作为编程语言，以「要求标准答案与选手答案差值小于 1e-3，文件名为 num，单个测试点满分为 10 分」为例．

## Testlib

参见：[Testlib/简介](./testlib/index.md)，[Testlib/Checker](./testlib/checker.md)

Testlib 是一个 C++ 的库，用于辅助出题人使用 C++ 编写算法竞赛题．

必须使用 Testlib 作为 spj 的 评测工具/OJ：Codeforces、洛谷、UOJ 等．

可以使用 Testlib 作为 spj 的 评测工具/OJ：LibreOJ ([Lyrio](https://github.com/lyrio-dev))、Lemon、牛客网等．

SYZOJ 2 所需的修改版 Testlib 托管于 [pastebin](https://pastebin.com/3GANXMG7)[^1]，但此修改版并未修改交互模式．[syzoj/testlib](https://github.com/syzoj/testlib) 处托管了一份可以在 SYZOJ 2 上使用交互模式的 Testlib．

Lemon 所需的修改版 Testlib 托管于 [GitHub - GitPinkRabbit/Testlib-for-Lemons](https://github.com/GitPinkRabbit/Testlib-for-Lemons)．注意此版本 Testlib 注册 checker 时应使用 `registerLemonChecker()`，而非 `registerTestlibCmd()`．此版本继承自 [matthew99 的旧版](https://paste.ubuntu.com/p/JsTspHHnmB/)，添加了一些 Testlib 的新功能．如果你使用 LemonLime，则可以使用原生的 Testlib．

DOMJudge 所需的修改版 Testlib 托管于 [cn-xcpc-tools/testlib-for-domjudge](https://github.com/cn-xcpc-tools/testlib-for-domjudge)．此版本 Testlib 同时可作为 Special Judge 的 checker 和交互题的 interactor．

Arbiter 所需的修改版 Testlib 托管于 [testlib-for-arbiter](https://github.com/HeRaNO/ChickenRibs/tree/master/testlib-for-arbiter)．

其他评测工具/OJ 大部分需要按照其 spj 编写格式修改 Testlib，并将 testlib.h 与 spj 一同上传；或将 testlib.h 置于 include 目录．

```cpp
#include "testlib.h"
//
#include <cmath>

int main(int argc, char *argv[]) {
  /*
   * inf：输入
   * ouf：选手输出
   * ans：标准输出
   */
  registerTestlibCmd(argc, argv);

  double pans = ouf.readDouble(), jans = ans.readDouble();

  if (abs(pans - jans) < 1e-3)
    quitf(_ok, "Good job\n");
  else
    quitf(_wa, "Too big or too small, expected %f, found %f\n", jans, pans);
}
```

## Lemon

???+ note "Note"
    Lemon 有现成的修改版 [Testlib](#testlib)，建议使用 Testlib．
    
    LemonLime 最新版已经支持使用原版 Testlib 编写评测器，如果你使用 LemonLime，建议使用 Testlib．

```cpp
#include <cmath>
#include <cstdio>

int main(int argc, char* argv[]) {
  /*
   * argv[1]：输入
   * argv[2]：选手输出
   * argv[3]：标准输出
   * argv[4]：单个测试点分值
   * argv[5]：输出最终得分 (0 ~ argv[4])
   * argv[6]：输出错误报告
   */
  FILE* fin = fopen(argv[1], "r");
  FILE* fout = fopen(argv[2], "r");
  FILE* fstd = fopen(argv[3], "r");
  FILE* fscore = fopen(argv[5], "w");
  FILE* freport = fopen(argv[6], "w");

  double pans, jans;
  fscanf(fout, "%lf", &pans);
  fscanf(fstd, "%lf", &jans);

  if (abs(pans - jans) < 1e-3) {
    fprintf(fscore, "%s", argv[4]);
    fprintf(freport, "Good job\n");
  } else {
    fprintf(fscore, "%d", 0);
    fprintf(freport, "Too big or too small, expected %f, found %f\n", jans,
            pans);
  }
}
```

## Cena

```cpp
#include <cmath>
#include <cstdio>

int main(int argc, char* argv[]) {
  /*
   * FILENAME.in：输入
   * FILENAME.out：选手输出
   * argv[1]：单个测试点分值
   * argv[2]：标准输出
   * score.log：输出最终得分 (0 ~ argv[1])
   * report.log：输出错误报告
   */
  FILE* fin = fopen("num.in", "r");
  FILE* fout = fopen("num.out", "r");
  FILE* fstd = fopen(argv[2], "r");
  FILE* fscore = fopen("score.log", "w");
  FILE* freport = fopen("report.log", "w");

  double pans, jans;
  fscanf(fout, "%lf", &pans);
  fscanf(fstd, "%lf", &jans);

  if (abs(pans - jans) < 1e-3) {
    fprintf(fscore, "%s", argv[1]);
    fprintf(freport, "Good job\n");
  } else {
    fprintf(fscore, "%d", 0);
    fprintf(freport, "Too big or too small, expected %f, found %f\n", jans,
            pans);
  }
}
```

## CCR

```cpp
#include <cmath>
#include <cstdio>

int main(int argc, char* argv[]) {
  /*
   * stdin：输入
   * argv[2]：标准输出
   * argv[3]：选手输出
   * stdout:L1：输出最终得分比率 (0 ~ 1)
   * stdout:L2：输出错误报告
   */
  FILE* fout = fopen(argv[3], "r");
  FILE* fstd = fopen(argv[2], "r");

  double pans, jans;
  fscanf(fout, "%lf", &pans);
  fscanf(fstd, "%lf", &jans);

  if (abs(pans - jans) < 1e-3) {
    printf("%d\n", 1);
    printf("Good job\n");
  } else {
    printf("%d\n", 0);
    printf("Too big or too small, expected %f, found %f\n", jans, pans);
  }
}
```

## Arbiter

```cpp
#include <cmath>
#include <cstdio>

int main(int argc, char* argv[]) {
  /*
   * argv[1]：输入
   * argv[2]：选手输出
   * argv[3]：标准输出
   * /tmp/_eval.score:L1：输出错误报告
   * /tmp/_eval.score:L2：输出最终得分
   */
  FILE* fout = fopen(argv[2], "r");
  FILE* fstd = fopen(argv[3], "r");
  FILE* fscore = fopen("/tmp/_eval.score", "w");

  double pans, jans;
  fscanf(fout, "%lf", &pans);
  fscanf(fstd, "%lf", &jans);

  if (abs(pans - jans) < 1e-3) {
    fprintf(fscore, "Good job\n");
    fprintf(fscore, "%d", 10);
  } else {
    fprintf(fscore, "Too big or too small, expected %f, found %f\n", jans,
            pans);
    fprintf(fscore, "%d", 0);
  }
}
```

## HUSTOJ

```cpp
#include <cmath>
#include <cstdio>

#define AC 0
#define WA 1

int main(int argc, char* argv[]) {
  /*
   * argv[1]：输入
   * argv[2]：标准输出
   * argv[3]：选手输出
   * exit code：返回判断结果
   */
  FILE* fin = fopen(argv[1], "r");
  FILE* fout = fopen(argv[3], "r");
  FILE* fstd = fopen(argv[2], "r");

  double pans, jans;
  fscanf(fout, "%lf", &pans);
  fscanf(fstd, "%lf", &jans);

  if (abs(pans - jans) < 1e-3)
    return AC;
  else
    return WA;
}
```

## QDUOJ

相较之下，QDUOJ 略为麻烦．它带 spj 的题目没有标准输出，只能把 std 写进 spj，待跑出标准输出后再判断．

```cpp
#include <cmath>
#include <cstdio>

#define AC 0
#define WA 1
#define ERROR -1

double solve(...) {
  // std
}

int main(int argc, char* argv[]) {
  /*
   * argv[1]：输入
   * argv[2]：选手输出
   * exit code：返回判断结果
   */
  FILE* fin = fopen(argv[1], "r");
  FILE* fout = fopen(argv[2], "r");

  double pans, jans;
  fscanf(fout, "%lf", &pans);

  jans = solve(...);
  if (abs(pans - jans) < 1e-3)
    return AC;
  else
    return WA;
}
```

## HDOJ

HDOJ 和 QDUOJ 的情况基本一致，也需要在 spj 中实现 std 后与选手输出比较．但与 QDUOJ 不同的是，HDOJ 会比较答案与 spj 输出在标准输出的内容后给出最终结果．因此，上传输出时仅需上传 spj 在正确时的输出即可．

HDOJ 需上传 Windows 下编译后的二进制文件，而非源代码．

```cpp
#include <cmath>
#include <cstdio>

double solve(FILE* fin) {
  // std, read input from fin
}

int main(int argc, char* argv[]) {
  /*
   * argv[1]：输入
   * stdin：选手输出
   */
  FILE* fin = fopen(argv[1], "r");

  double pans, jans;
  if (scanf("%lf", &pans) != 1) {
    printf("WA\n");
    goto finish;
  }

  jans = solve(fin);
  if (abs(pans - jans) < 1e-3)
    printf("AC\n");
  else
    printf("WA\n");

finish:
  fclose(fin);
  return 0;
}
```

对应的答案文件为：

```text
AC
```

## SYZOJ 2

???+ note "Note"
    SYZOJ 2 有现成的修改版 [Testlib](#testlib)，建议使用 Testlib．
    
    LibreOJ 的最新版本已不再基于 SYZOJ，而是基于 [Lyrio](https://github.com/lyrio-dev/lyrio)．Lyrio 支持使用原版 Testlib 编写评测器，这也是更加通用且推荐的做法．

```cpp
#include <cmath>
#include <cstdio>

int main(int argc, char* argv[]) {
  /*
   * in：输入
   * user_out：选手输出
   * answer：标准输出
   * code：选手代码
   * stdout：输出最终得分 (0 ~ 100)
   * stderr：输出错误报告
   */
  FILE* fin = fopen("input", "r");
  FILE* fout = fopen("user_out", "r");
  FILE* fstd = fopen("answer", "r");
  FILE* fcode = fopen("code", "r");

  double pans, jans;
  fscanf(fout, "%lf", &pans);
  fscanf(fstd, "%lf", &jans);

  if (abs(pans - jans) < 1e-3) {
    printf("%d", 100);
    fprintf(stderr, "Good job\n");
  } else {
    printf("%d", 0);
    fprintf(stderr, "Too big or too small, expected %f, found %f\n", jans,
            pans);
  }
}
```

## 牛客网

???+ note "Note"
    牛客网有现成的修改版 [Testlib](#testlib)，建议使用 Testlib．

参见：[如何在牛客网出 Special Judge 的编程题](https://www.nowcoder.com/discuss/84666)

```cpp
#include <cmath>
#include <cstdio>

#define AC 0
#define WA 1

int main(int argc, char* argv[]) {
  /*
   * input：输入
   * user_output：选手输出
   * output：标准输出
   * exit code：返回判断结果
   */
  FILE* fin = fopen("input", "r");
  FILE* fout = fopen("user_output", "r");
  FILE* fstd = fopen("output", "r");

  double pans, jans;
  fscanf(fout, "%lf", &pans);
  fscanf(fstd, "%lf", &jans);

  if (abs(pans - jans) < 1e-3)
    return AC;
  else
    return WA;
}
```

## DOMJudge

???+ note "Note"
    DOMJudge 支持任何语言编写的 spj，参见：[problemarchive.org output validator 格式](https://www.problemarchive.org/wiki/index.php/Output_validator)．
    
    DOMJudge 有现成的修改版 [Testlib](#testlib)，建议使用 Testlib．

DOMJudge 使用的 Testlib 及导入 Polygon 题目包方式的文档：<https://github.com/cn-xcpc-tools/testlib-for-domjudge>

DOMJudge 的 [默认比较器](https://github.com/Kattis/problemtools/blob/master/support/default_validator/) 自带了浮点数带精度比较，只需要在题目配置的 `validator_flags` 中添加 `float_tolerance 1e-3` 即可．

```cpp
#include <cmath>
#include <cstdio>

#define AC 42
#define WA 43
char reportfile[50];

int main(int argc, char* argv[]) {
  /*
   * argv[1]: 输入
   * argv[2]: 标准输出
   * argv[3]: 评测信息输出的文件夹
   * stdin: 选手输出
   */
  FILE* fin = fopen(argv[1], "r");
  FILE* fstd = fopen(argv[2], "r");
  sprintf(reportfile, "%s/judgemessage.txt", argv[3]);
  FILE* freport = fopen(reportfile, "w");

  double pans, jans;
  scanf("%lf", &pans);
  fscanf(fstd, "%lf", &jans);

  if (abs(pans - jans) < 1e-3) {
    fprintf(freport, "Good job\n");
    return AC;
  } else {
    fprintf(freport, "Too big or too small, expected %f, found %f\n", jans,
            pans);
    return WA;
  }
}
```

也可以使用 Kattis Problem Tools 提供的头文件 [validate.h](https://github.com/Kattis/problemtools/blob/master/examples/different/output_validators/different_validator/validate.h) 编写，以实现更加复杂的功能．

## 参考资料

[^1]: [LibreOJ 支持 testlib 检查器啦！](https://loj.ac/article/124)


## tools/testlib/checker.md

Checker，即 [Special Judge](../special-judge.md)，用于检验答案是否合法．使用 Testlib 可以让我们免去检验许多东西，使编写简单许多．

Checker 从命令行参数读取到输入文件名、选手输出文件名、标准输出文件名，并确定选手输出是否正确，并返回一个预定义的结果：

请在阅读下文前先阅读 [通用](./general.md)．

## 简单的例子

???+ note "题目"
    给定两个整数 $a,b$（$-1000 \le a,b \le 1000$），输出它们的和．

这题显然不需要 checker 对吧，但是如果一定要的话也可以写一个：

```cpp
#include "testlib.h"

int main(int argc, char* argv[]) {
  registerTestlibCmd(argc, argv);

  int pans = ouf.readInt(-2000, 2000, "sum of numbers");

  // 假定标准输出是正确的，不检查其范围
  // 之后我们会看到这并不合理
  int jans = ans.readInt();

  if (pans == jans)
    quitf(_ok, "The sum is correct.");
  else
    quitf(_wa, "The sum is wrong: expected = %d, found = %d", jans, pans);
}
```

## 编写 readAns 函数

假设你有一道题输入输出均有很多数，如：给定一张 DAG，求 $s$ 到 $t$ 的最长路并输出路径（可能有多条，输出任一）．

下面是一个 **不好** 的 checker 的例子．

### 不好的实现

```cpp
#include "testlib.h"
//
#include <map>
#include <vector>
using namespace std;

map<pair<int, int>, int> edges;

int main(int argc, char* argv[]) {
  registerTestlibCmd(argc, argv);
  int n = inf.readInt();  // 不需要 readSpace() 或 readEoln()
  int m = inf.readInt();  // 因为不需要在 checker 中检查标准输入合法性
                          // （有 validator）
  for (int i = 0; i < m; i++) {
    int a = inf.readInt();
    int b = inf.readInt();
    int w = inf.readInt();
    edges[make_pair(a, b)] = edges[make_pair(b, a)] = w;
  }
  int s = inf.readInt();
  int t = inf.readInt();

  // 读入标准输出
  int jvalue = 0;
  vector<int> jpath;
  int jlen = ans.readInt();
  for (int i = 0; i < jlen; i++) {
    jpath.push_back(ans.readInt());
  }
  for (int i = 0; i < jlen - 1; i++) {
    jvalue += edges[make_pair(jpath[i], jpath[i + 1])];
  }

  // 读入选手输出
  int pvalue = 0;
  vector<int> ppath;
  vector<bool> used(n);
  int plen = ouf.readInt(2, n, "number of vertices");  // 至少包含 s 和 t 两个点
  for (int i = 0; i < plen; i++) {
    int v = ouf.readInt(1, n, format("path[%d]", i + 1).c_str());
    if (used[v - 1])  // 检查每条边是否只用到一次
      quitf(_wa, "vertex %d was used twice", v);
    used[v - 1] = true;
    ppath.push_back(v);
  }
  // 检查起点终点合法性
  if (ppath.front() != s)
    quitf(_wa, "path doesn't start in s: expected s = %d, found %d", s,
          ppath.front());
  if (ppath.back() != t)
    quitf(_wa, "path doesn't finish in t: expected t = %d, found %d", t,
          ppath.back());
  // 检查相邻点间是否有边
  for (int i = 0; i < plen - 1; i++) {
    if (edges.find(make_pair(ppath[i], ppath[i + 1])) == edges.end())
      quitf(_wa, "there is no edge (%d, %d) in the graph", ppath[i],
            ppath[i + 1]);
    pvalue += edges[make_pair(ppath[i], ppath[i + 1])];
  }

  if (jvalue != pvalue)
    quitf(_wa, "jury has answer %d, participant has answer %d", jvalue, pvalue);
  else
    quitf(_ok, "answer = %d", pvalue);
}
```

这个 checker 主要有两个问题：

1.  它确信标准输出是正确的．如果选手输出比标准输出更优，它会被判成 WA，这不太妙．同时，如果标准输出不合法，也会产生 WA．对于这两种情况，正确的操作都是返回 Fail 状态．
2.  读入标准输出和选手输出的代码是重复的．在这道题中写两遍读入问题不大，只需要一个 `for` 循环；但是如果有一道题输出很复杂，就会导致你的 checker 结构混乱．重复代码会大大降低可维护性，让你在 debug 或修改格式时变得困难．

读入标准输出和选手输出的方式实际上是完全相同的，这就是我们通常编写一个用流作为参数的读入函数的原因．

### 好的实现

```cpp
// clang-format off

#include "testlib.h"
#include <map>
#include <vector>
using namespace std;

map<pair<int, int>, int> edges;
int n, m, s, t;

// 这个函数接受一个流，从其中读入
// 检查路径的合法性并返回路径长度
// 当 stream 为 ans 时，所有 stream.quitf(_wa, ...)
// 和失败的 readXxx() 均会返回 _fail 而非 _wa
// 也就是说，如果输出非法，对于选手输出流它将返回 _wa，
// 对于标准输出流它将返回 _fail
int readAns(InStream& stream) {
  // 读入输出
  int value = 0;
  vector<int> path;
  vector<bool> used(n);
  int len = stream.readInt(2, n, "number of vertices");
  for (int i = 0; i < len; i++) {
    int v = stream.readInt(1, n, format("path[%d]", i + 1).c_str());
    if (used[v - 1]) {
      stream.quitf(_wa, "vertex %d was used twice", v);
    }
    used[v - 1] = true;
    path.push_back(v);
  }
  if (path.front() != s)
    stream.quitf(_wa, "path doesn't start in s: expected s = %d, found %d", s,
                 path.front());
  if (path.back() != t)
    stream.quitf(_wa, "path doesn't finish in t: expected t = %d, found %d", t,
                 path.back());
  for (int i = 0; i < len - 1; i++) {
    if (edges.find(make_pair(path[i], path[i + 1])) == edges.end())
      stream.quitf(_wa, "there is no edge (%d, %d) in the graph", path[i],
                   path[i + 1]);
    value += edges[make_pair(path[i], path[i + 1])];
  }
  return value;
}

int main(int argc, char* argv[]) {
  registerTestlibCmd(argc, argv);
  n = inf.readInt();
  m = inf.readInt();
  for (int i = 0; i < m; i++) {
    int a = inf.readInt();
    int b = inf.readInt();
    int w = inf.readInt();
    edges[make_pair(a, b)] = edges[make_pair(b, a)] = w;
  }
  int s = inf.readInt();
  int t = inf.readInt();
  
  int jans = readAns(ans);
  int pans = readAns(ouf);
  if (jans > pans)
    quitf(_wa, "jury has the better answer: jans = %d, pans = %d\n", jans,
          pans);
  else if (jans == pans)
    quitf(_ok, "answer = %d\n", pans);
  else  // (jans < pans)
    quitf(_fail, ":( participant has the better answer: jans = %d, pans = %d\n",
          jans, pans);
}
```

注意到这种写法我们同时也检查了标准输出是否合法，这样写 checker 让程序更短，且易于理解和 debug．此种写法也适用于输出 YES（并输出方案什么的），或 NO 的题目．

???+ note "Note"
    对于某些限制的检查可以用 `InStream::ensure/ensuref()` 函数更简洁地实现．如上例第 23 至 25 行也可以等价地写成如下形式：
    
    ```cpp
    stream.ensuref(!used[v - 1], "vertex %d was used twice", v);
    ```

???+ warning "Warning"
    请在 `readAns` 中避免调用 **全局** 函数 `::ensure/ensuref()`，这会导致在某些应判为 WA 的选手输出下返回 `_fail`，产生错误．

## 建议与常见错误

-   编写 `readAns` 函数，它真的可以让你的 checker 变得很棒．

-   读入选手输出时永远限定好范围，如果某些变量忘记了限定且被用于某些参数，你的 checker 可能会判定错误或 RE 等．

    -   反面教材

    ```cpp
    // ....
    int k = ouf.readInt();
    vector<int> lst;
    for (int i = 0; i < k; i++)  // k = 0 和 k = -5 在这里作用相同（不会进入循环体）
      lst.push_back(ouf.readInt());
    // 但是我们并不想接受一个长度为 -5 的 list，不是吗？
    // ....
    int pos = ouf.readInt();
    int x = A[pos];
    // 可能会有人输出 -42, 2147483456 或其他一些非法数字导致 checker RE
    ```

    -   正面教材

    ```cpp
    // ....
    int k = ouf.readInt(0, n);  // 长度不合法会立刻判 WA 而不会继续 check 导致 RE
    vector<int> lst;
    for (int i = 0; i < k; i++) lst.push_back(ouf.readInt());
    // ....
    int pos = ouf.readInt(0, (int)A.size() - 1);  // 防止 out of range
    int x = A[pos];
    // ....
    ```

-   使用项别名．

-   和 validator 不同，checker 不用特意检查非空字符．例如对于一个按顺序比较整数的 checker，我们只需判断选手输出的整数和答案整数是否对应相等，而选手是每行输出一个整数，还是在一行中输出所有整数等格式问题，我们的 checker 不必关心．

## 使用方法

通常我们不需要本地运行它，评测工具/OJ 会帮我们做好这一切．但是如果需要的话，以以下格式在命令行运行：

```bash
./checker <input-file> <output-file> <answer-file> [<report-file> [<-appes>]]
```

## 一些预设的 checker

很多时候我们的 checker 完成的工作很简单（如判断输出的整数是否正确，输出的浮点数是否满足精度要求），[Testlib](https://github.com/MikeMirzayanov/testlib/tree/master/checkers) 已经为我们给出了这些 checker 的实现，我们可以直接使用．

一些常用的 checker 有：

-   ncmp：按顺序比较 64 位整数．
-   rcmp4：按顺序比较浮点数，最大可接受误差（绝对误差或相对误差）不超过 $10^{-4}$（还有 rcmp6，rcmp9 等对精度要求不同的 checker，用法和 rcmp4 类似）．
-   wcmp：按顺序比较字符串（不带空格，换行符等非空字符）．
-   yesno：比较 YES 和 NO，大小写不敏感．

    **本文主要翻译自 [Checkers with testlib.h - Codeforces](https://codeforces.com/blog/entry/18431)．`testlib.h` 的 GitHub 存储库为 [MikeMirzayanov/testlib](https://github.com/MikeMirzayanov/testlib)．**


## tools/testlib/general.md

本页面介绍 Testlib checker/interactor/validator 的一些通用状态/对象/函数、一些用法及注意事项．请在阅读其他页面前完整阅读本页面的内容．

## 通用状态

| 结果                 | Testlib 别名   | 含义                                                                                                                              |
| ------------------ | ------------ | ------------------------------------------------------------------------------------------------------------------------------- |
| Ok                 | `_ok`        | 答案正确．                                                                                                                           |
| Wrong Answer       | `_wa`        | 答案错误．                                                                                                                           |
| Presentation Error | `_pe`        | 答案格式错误．注意包括 Codeforces 在内的许多 OJ 并不区分 PE 和 WA．                                                                                   |
| Partially Correct  | `_pc(score)` | 答案部分正确．仅限于有部分分的测试点，其中 `score` 为一个正整数，从 $0$（没分）到 $100$（可能的最大分数）．（`quitf+_pc` 只是为了兼容旧的 pascal-testlib，如果想要输出部分分，建议使用 `quitp`[^1]） |
| Fail               | `_fail`      | validator 中表示输入不合法，不通过校验．<br>checker 中表示程序内部错误、标准输出有误或选手输出比标准输出更优，需要裁判/出题人关注．（也就是题目锅了）                                          |

通常用程序的返回值表明结果，但是也有一些其他方法：创建一个输出 xml 文件、输出信息到 stdout 或其他位置……这些都通过下方函数表中的 `quitf` 函数来完成．

## 通用对象

| 对象    | 含义    |
| ----- | ----- |
| `inf` | 输入文件流 |
| `ouf` | 选手输出流 |
| `ans` | 参考输出流 |

## 通用函数

非成员函数：

| 调用                                                                                              | 含义                                                                                                                                          |
| ----------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| `void registerTestlibCmd(int argc, char* argv[])`                                               | 注册程序为 checker                                                                                                                               |
| `void registerInteraction(int argc, char* argv[])`                                              | 注册程序为 interactor                                                                                                                            |
| `void registerValidation()`/`void registerValidation(int argc, char* argv[])`                   | 注册程序为 validator                                                                                                                             |
| `void registerGen(int argc, char* argv[], int randomGeneratorVersion)`                          | 注册程序为 generator<br>`randomGeneratorVersion` 推荐为 `1`                                                                                         |
| `void quit(TResult verdict, string message)`/`void quitf(TResult verdict, string message, ...)` | 结束程序，返回 `verdict`，输出 `message`                                                                                                              |
| `void quitif(bool condition, TResult verdict, string message, ...)`                             | 如果 `condition` 成立，调用 `quitf(verdict, message, ...)`                                                                                         |
| `void quitp(F points, string message, ...)`                                                     | 结束程序，返回部分分．大部分 OJ（如洛谷、UOJ）的 `points` 需要提供一个 $[0,1]$ 内的实数，表示得分百分比，还有部分 OJ（如 Lyrio）的 `points` 需要提供一个 $[0,100]$ 的实数（OJ 会自动舍弃小数部分），表示百分制下的测试点得分 |

流成员函数：

| 调用                                                                                                                                                                | 含义                                                                                 |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| `char readChar()`                                                                                                                                                 | 读入一个字符                                                                             |
| `char readChar(char c)`                                                                                                                                           | 读入一个字符，必须为 `c`                                                                     |
| `char readSpace()`                                                                                                                                                | 等同于 `readChar(' ')`                                                                |
| `string readToken()`/`string readWord()`                                                                                                                          | 读入一个串，到空白字符（空格、Tab、EOLN 等）停止                                                       |
| `string readToken(string regex)`/`string readWord(string regex)`                                                                                                  | 读入一个串，必须与 `regex` 匹配                                                               |
| `long long readLong()`                                                                                                                                            | 读入一个 64 位整数                                                                        |
| `long long readLong(long long L, long long R)`                                                                                                                    | 读入一个 64 位整数，必须在 $[L,R]$ 之间                                                         |
| `vector<long long> readLongs(int n, long long L, long long R)`                                                                                                    | 读入 $N$ 个 64 位整数，必须均在 $[L,R]$ 之间                                                    |
| `int readInt()`/`int readInteger()`                                                                                                                               | 读入一个 32 位整数                                                                        |
| `int readInt(int L, int R)`/`int readInteger(L, R)`                                                                                                               | 读入一个 32 位整数，必须在 $[L,R]$ 之间                                                         |
| `vector<int> readInts(int n, int L, int R)`/`vector<int> readIntegers(int n, int L, int R)`                                                                       | 读入 $N$ 个 32 位整数，必须均在 $[L,R]$ 之间                                                    |
| `double readReal()`/`double readDouble()`                                                                                                                         | 读入一个双精度浮点数                                                                         |
| `double readReal(double L, double R)`/`double readDouble(double L, double R)`                                                                                     | 读入一个双精度浮点数，必须在 $[L,R]$ 之间                                                          |
| `double readStrictReal(double L, double R, int minPrecision, int maxPrecision)`/`double readStrictDouble(double L, double R, int minPrecision, int maxPrecision)` | 读入一个双精度浮点数，必须在 $[L,R]$ 之间，小数位数必须在 $[minPrecision,maxPrecision]$ 之间，不得使用指数计数法等非正常格式 |
| `string readString()`/`string readLine()`                                                                                                                         | 读入一行（包括换行符），同时将流指针指向下一行的开头                                                         |
| `string readString(string regex)`/`string readLine(string regex)`                                                                                                 | 读入一行，必须与 `regex` 匹配                                                                |
| `void readEoln()`                                                                                                                                                 | 读入 EOLN（在 Linux 环境下读入 `LF`，在 Windows 环境下读入 `CR LF`）                                |
| `void readEof()`                                                                                                                                                  | 读入 EOF                                                                             |
| `void quit(TResult verdict, string message)`/`void quitf(TResult verdict, string message, ...)`                                                                   | 结束程序，若 `Stream` 为 `ouf` 返回 `verdict`，否则返回 `_fail`；输出 `message`                     |
| `void quitif(bool condition, TResult verdict, string message, ...)`                                                                                               | 如果 `condition` 成立，调用 `quitf(verdict, message, ...)`                                |

未完待续……

## 极简正则表达式

上面的输入函数中的一部分允许使用「极简正则表达式」特性，如下所示：

-   字符集．如 `[a-z]` 表示所有小写英文字母，`[^a-z]` 表示除小写英文字母外任何字符．
-   范围．如 `[a-z]{1,5}` 表示一个长度在 $[1,5]$ 范围内且只包含小写英文字母的串．
-   「或」标识符．如 `mike|john` 表示 `mike` 或 `john` 其一．
-   「可选」标识符．如 `-?[1-9][0-9]{0,3}` 表示 $[-9999,9999]$ 范围内的非零整数（注意那个可选的负号）．
-   「重复」标识符．如 `[0-9]*` 表示零个或更多数字，`[0-9]+` 表示一个或更多数字．
-   注意这里的正则表达式是「贪婪」的（「重复」会尽可能匹配）．如 `[0-9]?1` 将不会匹配 `1`（因为 `[0-9]?` 将 `1` 匹配上，导致模板串剩余的那个 `1` 无法匹配）．

## 首先 include testlib.h

请确保 testlib.h 是你 include 的 **第一个** 头文件，Testlib 会重写/禁用（通过名字冲突的方式）一些与随机有关的函数（如 `random()`），保证随机结果与环境无关，这对于 generator 非常重要，[generator 页面](./generator.md) 会详细说明这一点．

## 使用项别名

推荐给 `readInt/readInteger/readLong/readDouble/readWord/readToken/readString/readLine` 等的有限制调用最后多传入一个 `string` 参数，即当前读入的项的别名，使报错易读．例如使用 `inf.readInt(1, 100, "n")` 而非 `inf.readInt(1, 100)`，报错信息将为 `FAIL Integer parameter [name=n] equals to 0, violates the range [1, 100]`．

## 使用 `ensuref/ensure()`

这两个函数用于检查条件是否成立（类似于 `assert()`）．例如检查 $x_i \neq y_i$，我们可以使用

```cpp
ensuref(x[i] != y[i], "Graph can't contain loops");
```

还可以使用 C 风格占位符如

```cpp
ensuref(s.length() % 2 == 0,
        "String 's' should have even length, but s.length()=%d",
        int(s.length()));
```

它有一个简化版 `ensure()`，我们可以直接使用 `ensure(x> y)` 而不添加说明内容（也不支持添加说明内容），如果条件不满足报错将为 `FAIL Condition failed: "x > y"`．很多情况下不加额外的说明的这种报错很不友好，所以我们通常使用 `ensuref()` 并加以说明内容，而非使用 `ensure()`．

???+ warning "Warning"
    注意全局与成员 `ensuref/ensure()` 的区别
    
    全局函数 `::ensuref/ensure()` 多用于 generator 和 validator 中，如果检查失败将统一返回 `_fail`．
    
    成员函数 `InStream::ensuref/ensure()` 一般用于判断选手和参考程序的输出是否合法．当 `InStream` 为 `ouf` 时，返回 `_wa`；为 `inf`（一般不在 checker 中检查输入数据，这应当在 validator 中完成）或 `ans` 时，返回 `_fail`．详见 [Checker - 编写 readAns 函数](./checker.md#好的实现)．

**本文主要翻译并综合自 [Testlib - Codeforces](https://codeforces.com/testlib) 系列．`testlib.h` 的 GitHub 存储库为 [MikeMirzayanov/testlib](https://github.com/MikeMirzayanov/testlib)．**

[^1]: [issue 链接](https://github.com/MikeMirzayanov/testlib/issues/115#issuecomment-863414940)


## tools/testlib/generator.md

Generator，即数据生成器．当数据很大，手造会累死的时候，我们就需要它来帮助我们自动造数据．

## 简单的例子

生成两个 $[1,n]$ 范围内的整数：

```cpp
// clang-format off

#include "testlib.h"
#include <iostream>

using namespace std;

int main(int argc, char* argv[]) {
  registerGen(argc, argv, 1);
  int n = atoi(argv[1]);
  cout << rnd.next(1, n) << " ";
  cout << rnd.next(1, n) << endl;
}
```

## 为什么要使用 Testlib？

有人说写 generator 不需要用 Testlib，它在这没什么用．实际上这是个不正确的想法．一个好的 generator 应该满足这一点：**在任何环境下对于相同输入它给出相同输出**．写 generator 就避免不了生成随机值，平时我们用的 `rand()` 或 C++11 的 `mt19937/uniform_int_distribution`，当操作系统不同、使用不同编译器编译、不同时间运行等，它们的输出都可能不同（对于非常常用的 `srand(time(nullptr))`，这是显然的），而这就会给生成数据带来不确定性．

需要注意的是，一旦使用了 Testlib，就不能再使用标准库中的 `srand()`，`rand()` 等随机数函数，否则在编译时会报错．因此，**请确保所有与随机相关的函数均使用 Testlib 而非标准库提供的．**

而 Testlib 中的随机值生成函数则保证了相同调用会输出相同值，与 generator 本身或平台均无关．另外．它给生成各种要求的随机值提供了很大便利，如 `rnd.next("[a-z]{1,10}")` 会生成一个长度在 $[1,10]$ 范围内的串，每个字符为 `a` 到 `z`，很方便吧！

## Testlib 能做什么？

在一切之前，先执行 `registerGen(argc, argv, 1)` 初始化 Testlib（其中 `1` 是使用的 generator 版本，通常保持不变），然后我们就可以使用 `rnd` 对象来生成随机值．随机数种子取自命令行参数的哈希值，对于某 generator `g.cpp`，`g 100`(Unix-Like) 和 `g.exe "100"`(Windows) 将会有相同的输出，而 `g 100 0` 则与它们不同．

`rnd` 对象的类型为 `random_t`，你可以建立一个新的随机值生成对象，不过通常你不需要这么做．

该对象有许多有用的成员函数，下面是一些例子：

| 调用                                           | 含义                                                                                                                                                                                                                                                      |
| -------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `rnd.next(4)`                                | 等概率生成一个 $[0,4)$ 范围内的整数                                                                                                                                                                                                                                  |
| `rnd.next(4, 100)`                           | 等概率生成一个 $[4,100]$ 范围内的整数                                                                                                                                                                                                                                |
| `rnd.next(10.0)`                             | 等概率生成一个 $[0,10.0)$ 范围内的浮点数                                                                                                                                                                                                                              |
| <code>rnd.next("one \| two \| three")</code> | 等概率从 `one`,`two`,`three` 三个串中返回一个                                                                                                                                                                                                                       |
| `rnd.wnext(4, t)`                            | `wnext()` 是一个生成不等分布（具有偏移期望）的函数[^note1]，$t$ 表示调用 `next()` 的次数，并取生成值的最大值．例如 `rnd.wnext(3, 1)` 等同于 `max({rnd.next(3), rnd.next(3)})`；`rnd.wnext(4, 2)` 等同于 `max({rnd.next(4), rnd.next(4), rnd.next(4)})`．如果 $t<0$，则为调用 $-t$ 次，取最小值；如果 $t=0$，等同于 `next()`． |
| `rnd.any(container)`                         | 等概率返回一个具有随机访问迭代器（如 `std::vector` 和 `std::string`）的容器内的某一元素的引用                                                                                                                                                                                           |

附：关于 `rnd.wnext(i,t)` 的形式化定义：

$$
\operatorname{wnext}(i,t)=
\begin{cases}
\operatorname{next}(i) & t=0 \\
\max(\operatorname{next}(i),\operatorname{wnext}(i,t-1)) & t>0 \\
\min(\operatorname{next}(i),\operatorname{wnext}(i,t+1)) & t<0
\end{cases}
$$

另外，不要使用 `std::random_shuffle()`，请使用 Testlib 中的 `shuffle()`，它同样接受一对迭代器．它使用 `rnd` 来打乱序列，即满足如上「好的 generator」的要求．

## 示例：生成一棵树

下面是生成一棵树的主要代码，它接受两个参数——顶点数和伸展度．例如，当 $n=10,t=1000$ 时，可能会生成链；当 $n=10,t=-1000$ 时，可能会生成菊花．

```cpp
#define forn(i, n) for (int i = 0; i < int(n); i++)

registerGen(argc, argv, 1);

int n = atoi(argv[1]);
int t = atoi(argv[2]);

vector<int> p(n);

/* 为节点 1..n-1 设置父亲 */
forn(i, n) if (i > 0) p[i] = rnd.wnext(i, t);

printf("%d\n", n);

/* 打乱节点 1..n-1 */
vector<int> perm(n);
forn(i, n) perm[i] = i;
shuffle(perm.begin() + 1, perm.end());

/* 根据打乱的节点顺序加边 */
vector<pair<int, int>> edges;
for (int i = 1; i < n; i++)
  if (rnd.next(2))
    edges.push_back(make_pair(perm[i], perm[p[i]]));
  else
    edges.push_back(make_pair(perm[p[i]], perm[i]));

/* 打乱边 */
shuffle(edges.begin(), edges.end());

for (int i = 0; i + 1 < n; i++)
  printf("%d %d\n", edges[i].first + 1, edges[i].second + 1);
```

## 一次性生成多组数据

跟不使用 Testlib 编写的时候一样，每次输出前重定向输出流就好，不过 Testlib 提供了一个辅助函数 `startTest(test_index)`，它帮助你将输出流重定向到 `test_index` 文件．

## 一些注意事项

-   严格遵循题目的格式要求，如空格和换行，注意文件的末尾应有一个换行．
-   对于大数据首选 `printf` 而非 `cout`，以提高性能．（不建议在使用 Testlib 时关闭流同步）
-   不使用 UB（Undefined Behavior，未定义行为），如本文开头的那个示例，输出如果写成 `cout << rnd.next(1, n) << " " << rnd.next(1, n) << endl;`，则 `rnd.next()` 的调用顺序没有定义．

## 新特性：解析命令行参数

在之前，我们通常使用类似 `int n = atoi(argv[3]);` 的代码，但是这样并不好．有以下几点原因：

-   不存在第三个命令行参数的时候是不安全的；
-   第三个命令行参数可能不是有效的 32 位整数．

现在，你可以这样写：`int n = opt<int>(3)`．与此同时，你也可以使用 `int64_t m = opt<int64_t>(1);`，`bool t = opt<bool>(2);` 和 `string s = opt(4);` 等．

另外，testlib 同时也支持命名参数．如果有很多参数，这样 `g 10 20000 a true` 的可读性就会比 `g -n10 -m200000 -t=a -increment` 差．

在这种情况下，现在你可以在 generator 中使用以下代码：

```cpp
int n = opt<int>("n");
long long n = opt<long long>("m");
string t = opt("t");
bool increment = opt<bool>("increment");
```

你可以自由地混合使用按下标和按名称读取参数的方式．

支持的用于编写命名参数的方案有以下几种：

-   `--key=value` 或 `-key=value`；
-   `--key value` 或 `-key value`——如果 `value` 不是新参数的开头（不以连字符 `-` 开头或一个/两个连字符后没有跟随字母）；
-   `--k12345` 或 `-k12345`——如果 key `k` 是一个字母，且后面是一个数字；
-   `-prop` 或 `--prop`——启用 bool 属性．

下面是一些例子：

```text
g1 -n1
g2 --len=4 --s=oops
g3 -inc -shuffle -n=5
g4 --length 5 --total 21 -ord
```

## 更多示例

可以在 [GitHub](https://github.com/MikeMirzayanov/testlib/tree/master/generators) 中找到．

**本文主要翻译自 [Генераторы на testlib.h - Codeforces](https://codeforces.com/blog/entry/18291)．新特性翻译自 [Testlib: Opts—parsing command line options](https://codeforces.com/blog/entry/72702)．`testlib.h` 的 GitHub 存储库为 [MikeMirzayanov/testlib](https://github.com/MikeMirzayanov/testlib)．**

[^note1]: 事实上，当 `i` 为浮点数时，`rnd.wnext(i, t)` 服从 $[0,i)$ 上的 [Beta 分布](https://en.wikipedia.org/wiki/Beta_distribution)：当 $t>0$ 时，服从 $i\cdot \mathrm{Beta}(t+1,1)$；当 $t<0$ 时，服从 $i\cdot \mathrm{Beta}(1,t+1)$．


## tools/testlib/index.md

author: Xeonacid, sshwy

如果你正在使用 C++ 出一道算法竞赛题目，Testlib 是编写相关程序（generator, validator, checker, interactor）时的优秀辅助工具．它是俄罗斯和其他一些国家的出题人的必备工具，许多比赛也都在用它：ROI、ICPC 区域赛、所有 Codeforces round……

Testlib 库仅有 `testlib.h` 一个文件，使用时仅需在所编写的程序开头添加 `#include "testlib.h"` 即可．

Testlib 的具体用途：

-   编写 [Generator](./generator.md)，即数据生成器．
-   编写 [Validator](./validator.md)，即数据校验器，判断生成数据是否符合题目要求，如数据范围、格式等．
-   编写 [Interactor](./interactor.md)，即交互器，用于交互题．
-   编写 [Checker](./checker.md)，即 [Special Judge](../special-judge.md)．

Testlib 与 Codeforces 开发的 [Polygon](https://polygon.codeforces.com/) 出题平台完全兼容．

`testlib.h` 在 2005 年移植自 `testlib.pas`，并一直在更新．Testlib 与绝大多数编译器兼容，如 VC++ 和 GCC g++，并兼容 C++11．

**本文主要翻译自 [Testlib - Codeforces](https://codeforces.com/testlib)．`testlib.h` 的 GitHub 存储库为 [MikeMirzayanov/testlib](https://github.com/MikeMirzayanov/testlib)．**


## tools/testlib/interactor.md

Interactor，即交互器，用于交互题与选手程序交互．交互题的介绍见 [题型介绍 - 交互题](../../contest/problems.md#)．

???+ note "Note"
    Testlib 仅支持 Codeforces 形式交互题，即两程序交互．不支持 NOI 形式的选手编写函数与其他函数交互．

请在阅读下文前先阅读 [通用](./general.md)．

Testlib 为 interactor 提供了一个特殊的流 `std::fstream tout`，它是一个 log 流，你可以在 interactor 中向它写入，并在 checker 中用 `ouf` 读取．

在 interactor 中，我们从 `inf` 读取题目测试数据，将选手程序（和标程）的标准输入写入 `stdout`（在线），从 `ouf` 读选手输出（在线），从 `ans` 读标准输出（在线）．

如果 interactor 返回了 ok 状态，checker（如果有的话）将接管工作，检查答案合法性．

## 用法

Windows:

```bat
interactor.exe <Input_File> <Output_File> [<Answer_File> [<Result_File> [-appes]]],
```

Linux:

```bash
./interactor.out <Input_File> <Output_File> [<Answer_File> [<Result_File> [-appes]]],
```

## 简单的例子

???+ note "题目"
    interactor 随机选择一个 $[1,10^9]$ 范围内的整数，你要写一个程序来猜它，你最多可以询问 $50$ 次一个 $[1,10^9]$ 范围内的整数．
    
    interactor 将返回：
    
    `1`：询问与答案相同，你的程序应当停止询问．
    
    `0`：询问比答案小．
    
    `2`：询问比答案大．

注意在此题中我们不需要 `ans`，因为我们不需要将标准输出与其比较；而在其他题中可能需要这么做．

```cpp
int main(int argc, char** argv) {
  registerInteraction(argc, argv);
  int n = inf.readInt();  // 选数
  cout.flush();           // 刷新缓冲区
  int left = 50;
  bool found = false;
  while (left > 0 && !found) {
    left--;
    int a = ouf.readInt(1, 1000000000);  // 询问
    if (a < n)
      cout << 0 << endl;
    else if (a > n)
      cout << 2 << endl;
    else
      cout << 1 << endl, found = true;
    cout.flush();
  }
  if (!found) quitf(_wa, "couldn't guess the number with 50 questions");
  ouf.readEof();
  quitf(_ok, "guessed the number with %d questions!", 50 - left);
}
```

**本文主要翻译自 [Interactors with testlib.h - Codeforces](https://codeforces.com/blog/entry/18455)．`testlib.h` 的 GitHub 存储库为 [MikeMirzayanov/testlib](https://github.com/MikeMirzayanov/testlib)．**


## tools/testlib/validator.md

前置知识：[通用](./general.md)

本页面将简要介绍 validator 的概念与用法．

## 概述

Validator（中文：校验器）用于检验造好的数据的合法性．当造好一道题的数据，又担心数据不合法（不符合题目的限制条件：上溢、图不连通、不是树……）时，出题者通常会借助 validator 来检查．[^ref1]

因为 Coderforces 支持 hack 功能，所以所有 Codeforces 上的题目都必须要有 validator．UOJ 也如此．[Polygon](../polygon.md) 内建了对 validator 的支持．

## 使用方法

直接在命令行输入 `./val` 即可．数据通过 stdin 输入．如果想从文件输入可 `./val < a.in`．

若数据没有问题，则什么都不会输出且返回 0；否则会输出错误信息并返回一个非 0 值．

## 提示

-   写 validator 时，不能对被 validate 的数据做任何假设，因为它可能包含任何内容．因此，出题者要对各种不合法的情况进行判断（使用 Testlib 会大大简化这一流程）．
    -   例如，输入一个点数为 $n$ 的树，主要工作是判断 $n$ 是否符合范围和判断输入的是树与否．但是切不可在判断过 $n$ 范围之后就不对接下来输入的边的起点与终点的范围进行判断，否则可能会导致 validator RE．
    -   即使不会 RE 也不应该不判断，这会导致你的报错不正确．如上例，如果不判断，报错可能会是「不是一棵树」，但是正确的报错应当是「边起点/终点不在 $[1,n]$ 之间」．
-   不能对选手的读入方式做任何假设．因此，必须保证能通过 validate 的数据完全符合输入格式．
    -   例如，选手可能逐字符地读入数字，在数字与数字之间只读入一个空格．所以在编写 validator 时，数据中的每一个空白字符都要在 validator 中显式地读入（如空格和换行）．
-   结束时不要忘记 `inf.readEof()`．
-   如果题目开放 hack（或者说，validator 的错误信息会给别人看），请使报错信息尽量友好．
    -   读入变量时使用「项别名」．
    -   在判断使用的表达式不那么易懂时，使用 ensuref 而非 ensure．

## 示例

以下是 [CF Gym 100541A - Stock Market](https://codeforces.com/gym/100541/problem/A) 的 validator：

```cpp
#include "testlib.h"

int main(int argc, char* argv[]) {
  registerValidation(argc, argv);
  int testCount = inf.readInt(1, 10, "testCount");
  inf.readEoln();

  for (int i = 0; i < testCount; i++) {
    int n = inf.readInt(1, 100, "n");
    inf.readSpace();
    inf.readInt(1, 1000000, "w");
    inf.readEoln();

    for (int i = 0; i < n; ++i) {
      inf.readInt(1, 1000, "p_i");
      if (i < n - 1) inf.readSpace();
    }
    inf.readEoln();
  }

  inf.readEof();
}
```

## 外部链接

-   [Validator 的更多示例](https://github.com/MikeMirzayanov/testlib/tree/master/validators)
-   [`testlib.h` 的 GitHub 存储库 MikeMirzayanov/testlib](https://github.com/MikeMirzayanov/testlib)

## 参考资料与注释

[^ref1]: [Validators with testlib.h - Codeforces](https://codeforces.com/blog/entry/18426)


## tools/wsl.md

author: GoodCoder666, Ir1d, H-J-Granger, NachtgeistW, StudyingFather, Enter-tainer, abc1763613206, Anti-Li, shenyouran, Chrogeek, SukkaW, Henry-ZHR, Early0v0, andylizf, tootal, Marcythm, CoelacanthusHex, indevn, qinyihao, peasoft

![头图](./images/wsl-header.png)

本章主要介绍了在 Windows 系统下使用 Windows Subsystem for Linux 运行 Linux 环境的方法．

## 引言[^ref1]

现在大部分学校的竞赛练习环境都是构建在 Windows 系操作系统上，但是在 NOI 系列赛中，已经用上了 NOI Linux 这个 Ubuntu 操作系统的修改版．

NOI 竞赛（自 2021 年 9 月 1 日）的环境要求如下．[^ref2]

| 类别          | 软件或模块                     | 版本                 | 备注说明                                           |
| :---------- | :------------------------ | :----------------- | :--------------------------------------------- |
| 系统          | Linux 内核                  | `5.4.0-42-generic` | 64 位 x86 (AMD64)                               |
| 语言环境        | GCC（`gcc` 和 `g++`）        | `9.3.0`            | C 和 C++ 编译器                                    |
|             | FPC                       | `3.0.4`            | Pascal 编译器（注：自 2022 年起，NOI 系列竞赛不再支持 Pascal 语言） |
|             | Python 2                  | `2.7`              | 非竞赛语言                                          |
|             | Python 3                  | `3.8`              | 非竞赛语言                                          |
| 调试工具        | GDB                       | `9.1`              |                                                |
|             | DDD                       | `3.3.12`           | GDB 的 GUI 前端                                   |
| 集成开发环境（IDE） | Code::Blocks              | `20.03`            | C/C++ IDE                                      |
|             | Lazarus                   | `2.0.6`            | Pascal IDE                                     |
|             | Geany                     | `1.36`             | C/C++/Pascal（轻量级）IDE                           |
| 文本编辑工具      | Visual Studio Code        | `1.54.3`           |                                                |
|             | GNU Emacs                 | `26.3`             |                                                |
|             | gedit                     | `3.36.2`           |                                                |
|             | Vim                       | `8.1`              |                                                |
|             | Joe                       | `4.6`              |                                                |
|             | nano                      | `4.8`              |                                                |
|             | Sublime Text              | `3.2.2`            |                                                |
| 其它软件        | Firefox                   | `79.0`             | 浏览器                                            |
|             | Midnight Commander (`mc`) | `4.8.24`           | 文件管理器                                          |
|             | xterm (uxterm)            | `3.5.3`            | 终端                                             |
|             | Arbiter-local             | `1.02`             | 程序评测工具单机版                                      |

考场环境与一般环境会有一系列差异：

-   命令行上的操作和图形界面上的操作会有差异．
-   Linux 和 Windows 的差异，如对于大小写的敏感性差异．
-   不同编译器的行为（MSVC 和 GCC）和不同版本的编译器（Windows 上和 Linux 上的 GCC，32 位和 64 位的 Linux GCC，GCC 7 和 GCC 8 等）的行为，如对变量初始化和对数组下标越界的处理会有差异．
-   不同评测系统（洛谷和 Arbiter）的超时检查和内存限制检查会有差异．

这有可能导致一系列的尴尬情况：

-   想用<kbd>Ctrl</kbd>+<kbd>C</kbd>复制，结果退出了程序．
-   平时 AC 的程序模板到了 Linux 上就 WA．

为了防止考场上出现此类尴尬情况，我们必须要提前熟悉 Linux 系统的操作方法．

虽然 NOI 的官网已经放出了 NOI Linux 的 ISO 镜像，虚拟机的配置较为麻烦．且由于 NOI Linux 默认自带图形界面，无法保证在低配系统上流畅运行．

Windows 10 在一周年更新时推出了 Linux 子系统（WSL），在 2020 年 5 月更新中升级到了 WSL 2．截至 2020 年 6 月 1 日，WSL 已支持安装 Ubuntu、openSUSE Leap、Kali、Debian 等主流 Linux 分发版．但 WSL 并不支持 NOI 评测用的 Arbiter．

???+ note "[什么是 Linux 子系统（WSL）](https://zh.wikipedia.org/zh-cn/%E9%80%82%E7%94%A8%E4%BA%8ELinux%E7%9A%84Windows%E5%AD%90%E7%B3%BB%E7%BB%9F)"
    适用于 Linux 的 Windows 子系统（英语：Windows Subsystem for Linux，简称 WSL）是一个为在 Windows 10、Windows 11 与 Windows Server 2019 上能够原生运行 Linux 二进制可执行文件（ELF 格式）的兼容层．
    
    WSL 可让开发人员按原样运行 GNU/Linux 环境 - 包括大多数命令行工具、实用工具和应用程序 - 且不会产生虚拟机开销．
    
    WSL 仅在 64 位 Windows 10 版本 1607 及以上、Windows 11 和 Windows Server 2019/2022 中可用．

## 启用 WSL[^ref3]

### 自动安装

???+ warning "Warning"
    本部分适用于 Windows 10 版本 2004 及更高版本（内部版本 19041 及更高版本）或 Windows 11．
    
    如果你正在使用 2004 以下版本或你的电脑不支持虚拟化，请阅读下面的手动安装一节．
    
    如果你正在使用 1607 以下版本的 Windows 10，你的系统不支持 WSL．

1.  以管理员身份打开 Windows PowerShell（右击「开始」按钮，选择 Windows PowerShell（管理员）或 Windows 终端（管理员）)

2.  输入 `wsl --install`，并等待所有组件自动安装完成．期间你可能需要重启你的计算机来启用必要的 Windows 功能．

3.  安装完成后，你可以在「开始」菜单或 Windows 终端的标签页中找到你安装的发行版．

4.  接下来，请转到下面「配置分发版」一节完成其他设置．

### 手动安装[^ref4]

???+ warning "Warning"
    下面介绍手动安装 WSL 的步骤．如果你已经完成了自动安装，请跳过此部分．

#### 启用适用于 Linux 的 Windows 子系统

在安装适用于 WSL 的任何 Linux 分发版之前，必须在下述两种方法中选择一种，以确保启用「适用于 Linux 的 Windows 子系统」可选功能：

使用命令行：

1.  以管理员身份打开 PowerShell 并运行：

    ```powershell
    Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux
    # 如果你只想要使用 WSL 1 请跳过此步骤
    Enable-WindowsOptionalFeature -Online -FeatureName VirtualMachinePlatform
    ```

2.  出现提示时，重启计算机．

使用图形界面：

![Windows 功能](./images/wsl-windows-features.png)

1.  打开「控制面板」

2.  访问「程序和功能」子菜单「打开或关闭 Windows 功能」

3.  选择「适用于 Linux 的 Windows 子系统」与「虚拟机平台」

4.  点击确定

5.  重启

#### 安装内核更新包

如果你想要使用 WSL 1, 请跳过此步骤．

下载 [适用于 x64 计算机的 WSL2 Linux 内核更新包](https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi) 并安装．

#### 设置 WSL 默认版本

绝大部分情况下，建议使用 WSL 2．
WSL 1 与 WSL 2 的区别，请见 [比较 WSL 2 和 WSL 1](https://docs.microsoft.com/zh-cn/windows/wsl/compare-versions)

??? note "关于 systemd"
    WSL 1 完全不支持 systemd（这意味着一些需要 systemd 的功能无法实现或需要其他替代方案）．WSL 2 已经内建对 systemd 的支持．如果需要使用 systemd，而当前运行的发行版没有配置为启用 systemd，可参考 [WSL 中的高级设置配置](https://learn.microsoft.com/zh-cn/windows/wsl/wsl-config#systemd-support)．

```powershell
# 将 WSL 默认版本设置为 WSL 2
wsl --set-default-version 2
```

#### 安装 WSL 分发版

![搜索页](./images/wsl-search-page.png)

进入 Microsoft Store，搜索「Ubuntu」，然后选择「Ubuntu」，点击「安装」进行安装．也可打开 [Ubuntu 的商店页面](https://www.microsoft.com/zh-cn/p/ubuntu/9nblggh4msv6)．

???+ warning "Warning"
    Microsoft Store 的 Ubuntu 随着 Ubuntu 的更新而更新，因此内容可能会有所改变．如果想获取稳定的 Ubuntu 长期支持版，可以在 Microsoft Store 安装 Ubuntu 的 LTS 版本．

## 配置分发版[^ref5]

本章以 Windows 自动安装的 Ubuntu 为例．

### 运行 Ubuntu

打开「开始」菜单找到 Ubuntu 并启动，或使用 `wsl` 命令从 Windows 命令行启动．

可以为 Ubuntu 创建应用程序磁贴或固定至任务栏，以在下次方便地打开．

### 初始化

第一次运行 Ubuntu，需要完成初始化．

```console
    Installing, this may take a few minutes...
```

等待一两分钟时间，系统会提示创建新的用户账户．

```console
    Please create a default UNIX user account. The username does not need to match your Windows username.
    For more information visit: https://aka.ms/wslusers
    Enter new UNIX username: chtholly
```

输入完用户名以后会提示输入密码．在 Linux 中，输入密码时屏幕上不显示文字属于正常现象．

```console
    Enter new UNIX password:
```

设置好账户名和密码后，WSL 就安装完成了．

```console
    Installation successful!
    To run a command as administrator (user "root"), use "sudo <command>".
    See "man sudo_root" for details.
    
    chtholly@SENIORIOUS:~$
```

## 基础配置

初次安装好的系统不附带任何 C/C++ 编译器，需要手动配置环境．

```console
$ gcc
The program 'gcc' is currently not installed. You can install it by typing:
sudo apt install gcc
$ g++
The program 'g++' is currently not installed. You can install it by typing:
sudo apt install g++
```

### 更换为国内软件源

Ubuntu 默认的软件源在国外．可以换成国内的软件源以加快速度，如 [清华 TUNA 的软件源](https://mirrors.tuna.tsinghua.edu.cn/help/ubuntu/)．

???+ warning "使用与自己系统版本匹配的软件源"
    请在页面中寻找与自己系统版本相配的源（可使用 `sudo lsb_release -a` 查看 Ubuntu 版本）．
    
    除非你知道你在做什么，否则不要使用与自己的系统版本不匹配的源！

使用以下命令更新软件和软件源：

```console
$ sudo su # 执行这行指令后，终端提示符会从 $ 变成 #，执行下文的命令前注意关注提示符
[sudo] xxx 的密码：
# cp /etc/apt/sources.list /etc/apt/sources.list.bak
# vim /etc/apt/sources.list
...（按 i 之后将上文的源右键粘贴进去，编辑完后按 Esc，再输入 :wq 和回车）
# apt update
# apt upgrade -y
# exit
exit
$ 
```

### 安装中文环境

```console
# apt install language-pack-zh-hans -y
# apt install fontconfig -y
# apt install fonts-noto-cjk fonts-wqy-microhei fonts-wqy-zenhei -y # 中文字体
# dpkg-reconfigure locales
```

此时会进入一个设置菜单，不用管，直接回车．

下一个菜单中选择 `zh_CN.UTF-8` 回车．

<!-- scripts.linter.preprocess.fix_details off -->

```text
    Default locale for the system environment:

                 None
                 C.UTF-8
                 en_US.UTF-8
                [zh_CN.UTF-8]

            <Ok>            <Cancel>
```

<!-- scripts.linter.preprocess.fix_details on -->

之后关闭 WSL 并重启，系统就会变成中文．

再依次输入下列命令，把 `man` 帮助页替换为中文．[^ref6]

```console
# apt install manpages-zh
# sed -i 's|/usr/share/man|/usr/share/man/zh_CN|g' /etc/manpath.config
```

可以用 `man help` 测试．

### 安装编译环境[^ref7]

```console
# apt install -y build-essential vim ddd gdb fpc emacs gedit anjuta lazarus
```

GUIDE 的安装请参考 [Debian 或 Ubuntu 下 GUIDE 的安装](./editor/guide.md#在-debian-或-ubuntu-安装)．

这里安装的是基础 + NOI 官方要求的环境，如有需要可以用 `sudo apt install <程序名>` 来安装其它软件包．
若想安装其他版本可以参考 Debian 官方的 [包管理手册](https://www.debian.org/doc/manuals/debian-reference/ch02.zh-cn.html)．

以下为一个示例程序：

```console
$ vim cpuid.cpp
...
$ g++ -Wall cpuid.cpp -o cpuid
$ ./cpuid
AMD Ryzen 5 1400 Quad-Core Processor
```

???+ note "Note"
    Linux 环境下可执行文件可不带扩展名，运行方式参见上方命令．

## 进阶操作

### 使用 WSLg 运行 GUI 程序

如果你使用 Windows 10 19044 及以上版本或 Windows 11，则可以使用 WSL 2 提供的集成的桌面体验．该功能允许你直接安装并启动 Linux 桌面程序而无须其他配置．

参见 [在适用于 Linux 的 Windows 子系统上运行 Linux GUI 应用](https://docs.microsoft.com/zh-cn/windows/wsl/tutorials/gui-apps)

### 安装图形环境，并使用远程桌面连接

如果你使用的版本尚不支持 WSLg, 可以尝试使用以下指南开启图形界面功能．

以下以 Xfce 为例．

如果只想安装 Xfce，可以执行以下命令：

```console
$ sudo apt install xfce4 tightvncserver -y
```

如果除 Xfce 外想要更多的软件，可以执行以下命令：

```console
$ sudo apt install xubuntu-desktop -y
```

图形环境文件较大，下载解包需要一定时间．

配置 xrdp：

```console
$ sudo apt install xrdp -y
$ echo "xfce4-session" >~/.xsession
$ sudo service xrdp restart
```

为了防止和计算机原有的远程桌面冲突，需要更换默认端口．

![不换端口的结果](./images/wsl-result-of-not-changing-ports.png)

运行命令 `sudo sed -i 's/port=[0-9]\{1,5\}/port=otherport/' /etc/xrdp/xrdp.ini`，其中 `otherport` 为其他端口（如 `3390`）．

    [globals]
    ...
    port=3390

运行 `sudo service xrdp restart`，然后去开始菜单，用 `localhost:otherport` 来访问．

![](./images/wsl-login-using-non-root.png)

![](./images/wsl-first-login.png)

### 使用 Xming 连接

进入 Ubuntu 环境，安装 xterm：

```console
# apt install xterm -y
```

退出 Ubuntu．

从 [Xming X Server 下载地址](https://sourceforge.net/projects/xming/) 下载最新的 Xming Server，然后安装：

![](./images/wsl-xming-setup-wizard.png)

如果安装完后忘记勾选 Launch Xming，需在开始菜单里打开 Xming：

![别忘了！](./images/wsl-xming.png)

之后再回到 Ubuntu，键入如下指令：

```console
$ DISPLAY=:0 xterm
```

![](./images/wsl-open-xterm.png)

如果使用了 xfce4，可以在弹出的窗口中使用如下命令激活 xfce4：

```console
$ xfce4-session
```

![](./images/wsl-open-xfce4-session.png)

运行结果如图．（在 Xming 中使用<kbd>Ctrl</kbd>+<kbd>C</kbd>就可以退出该界面．）

![](./images/wsl-xfce.png)

### WSL 与 Windows 文件的互访问

Windows 下的硬盘被自动挂载至 Linux 环境下的 `/mnt` 文件夹下．
如 C 盘在 WSL 下的路径为 `/mnt/c`

```console
PS C:\Users\chtholly> bash
/mnt/c/Users/chtholly$ echo "Hello world!" > hello
/mnt/c/Users/chtholly$ exit
PS C:\Users\chtholly> cat hello
Hello world!
PS C:\Users\chtholly> echo "Welcome!" > welcome
PS C:\Users\chtholly> bash
/mnt/c/Users/chtholly$ cat welcome
Welcome!
```

另外，也可以从文件管理器访问 WSL 目录．在安装 WSL 后，可以在资源管理器的侧边栏中发现 Linux 项，在其中可以访问所有安装的发行版中的文件．

同样，也可以在资源管理器的路径或运行（Win+R）中直接输入 `\\wsl$` 来转到 WSL 的目录．

也可以直接使用诸如 `\\wsl$\Ubuntu\home\` 的路径访问其子文件夹．

### 配合 Visual Sudio Code 进行编辑

如果习惯在 Windows 环境下使用 [Visual Studio Code](./editor/vscode.md) 进行代码编辑，可以安装 VS Code 中的 `Remote - WSL` 插件，更方便地对 WSL 系统中的文件进行编辑．

通过 `Remote - WSL`，可以在 Windows 下的 VS Code 界面中直接对 WSL 子系统进行操作，更加方便地编辑子系统目录下的文件、更方便地使用终端进行调试．

通过在 WSL 中直接键入 `code .`，可以在该目录下直接唤出 Visual Studio Code，对于该目录下的文件进行编辑．

同时，可以通过类似 `code filename` 的命令，对于指定文件进行编辑．

在插件 `Remote - WSL` 的 Getting Started 页面，包含对于编辑操作的详细简介．

同时，也可以参考 Visual Studio Code 的官方文档中关于 WSL 的内容（[Remote development in WSL](https://code.visualstudio.com/docs/remote/wsl-tutorial)），这篇文章包含从 WSL 安装到配合插件使用的全流程的更详细的介绍．

## WSL1 升级为 WSL2

???+ warning "Warning"
    请确认已经完成前面 WSL1 的安装步骤．

执行命令 `wsl -l -v` 可以看到 WSL 版本号是 1，需要执行升级，才能到 2．

1.  启用「虚拟机平台」功能

    使用 PowerShell 以管理员身份运行：

    ```shell
    dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
    ```

    然后 **重启电脑**．

2.  下载 Linux 内核更新包

    -   [x64](https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi) 的内核更新包．
    -   [ARM64/AArch64](https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_arm64.msi) 的内核更新包．

3.  设置分发版版本

    执行命令：`wsl --set-version <分发版名称> <版本号>`

    如：将 Ubuntu 18.04 设置为 WSL 2 的命令为 `wsl --set-version Ubuntu-18.04 2`

    这一步比较耗时，执行完成后通过命令 `wsl -l -v` 来检查升级是否成功．

## FAQ

参见：[常见问题](https://docs.microsoft.com/zh-cn/windows/wsl/faq)，[WSL 2 常见问题解答](https://docs.microsoft.com/zh-cn/windows/wsl/wsl2-faq)

-   如何在子系统下进行 xxx？

    可以用自带命令行，或者使用图形界面．
    比如说 vim，在命令行中键入 `man vim`，会给出一份详尽的使用方法．
    亦可使用 `vim --help`．

    关于命令行，可阅读 [命令行](./cmd.md)

-   对系统资源的占用量？

    这个系统和 Windows 10 共用 Host，所以理论上是比虚拟机占用小的．

## 外部链接

-   [关于适用于 Linux 的 Windows 子系统](https://docs.microsoft.com/zh-cn/windows/wsl/about)
-   [Ubuntu 镜像使用帮助，清华 TUNA](https://mirrors.tuna.tsinghua.edu.cn/help/ubuntu/)
-   [Dev on Windows with WSL（在 Windows 上用 WSL 优雅开发）](https://dowww.spencerwoo.com)
-   [GitHub 上的 Awesome-WSL](https://github.com/sirredbeard/Awesome-WSL)
-   [排查适用于 Linux 的 Windows 子系统问题](https://docs.microsoft.com/zh-cn/windows/wsl/troubleshooting)
-   [WSL1 升级为 WSL2](https://www.cnblogs.com/stulzq/p/13926936.html)

## 参考资料与注释

[^ref1]: [洛谷日报 #6](https://www.luogu.com.cn/blog/asfr/Run-Ubuntu-On-Windows10)

[^ref2]: [NOI Linux 2.0 发布，将于 9 月 1 日起正式启用！](https://noi.cn/gynoi/jsgz/2021-07-16/732450.shtml)

[^ref3]: [安装 WSL, Microsoft Docs](https://docs.microsoft.com/zh-cn/windows/wsl/install)

[^ref4]: [旧版 WSL 的手动安装步骤](https://docs.microsoft.com/zh-cn/windows/wsl/install-manual)

[^ref5]: [WSL-Ubuntu 维基，ubuntu wiki](https://wiki.ubuntu.com/WSL)

[^ref6]: [Ubuntu 的 man 命令帮助如何设置中文版，Frank 看庐山，2017-06-09](https://blog.csdn.net/qq_14989227/article/details/72954523)

[^ref7]: [Run Bash on Ubuntu on Windows, Mike Harsh, 2016-05-30, Windows Blog](https://blogs.windows.com/buildingapps/2016/03/30/run-bash-on-ubuntu-on-windows/#cie8WdR3uSjgR5Ru.97)
