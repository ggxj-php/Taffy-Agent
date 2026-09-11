

## contest/common-mistakes.md

author: Estrella-Explore, H-J-Granger, orzAtalod, ksyx, Ir1d, Chrogeek, Enter-tainer, yiyangit, shuzhouliu, broken-paint, CarvingAn

本页面主要列举一些竞赛中很多人经常会出现的错误．

## 因环境不同导致的错误

-   `scanf` 或 `printf` 使用 `%I64d` 格式指示符在 Linux 下可能导致输入输出格式错误．

## 会引起 CE 的错误

这类错误多为词法、语法和语义错误，引发的原因较为简单，修复难度较低．

例：

-   `int main()` 写为 `int mian()` 之类的拼写错误．

-   写完 `struct` 或 `class` 忘记写分号．

-   数组开太大，（在 OJ 上）使用了不合法的函数（例如多线程），或者函数声明但未定义，会引起链接错误．

-   函数参数类型不匹配．

    -   示例：如使用 `<algorithm>` 头文件中的 `max` 函数时，传入了一个 `int` 类型参数和一个 `long long` 类型参数．

        ```cpp
        // query 为返回 long long 类型的自定义函数
        printf("%lld\n", max(0, query(1, 1, n, l, r));

        //错误    没有与参数列表匹配的 重载函数 "std::max" 实例
        ```

-   使用 `goto` 和 `switch-case` 的时候跳过了一些局部变量的初始化．

## 不会引起 CE 但会引起 Warning 的错误

犯这类错误时写下的程序虽然能通过编译，但大概率会得到错误的程序运行结果．这类错误会在使用 `-W{warningtype}` 参数编译时被编译器指出．

-   赋值运算符 `=` 和比较运算符 `==` 不分．

    -   示例：

        ```cpp
        std::srand(std::time(nullptr));
        int n = std::rand();
        if (n = 1)
          printf("Yes");
        else
          printf("No");

        // 无论 n 的随机所得值为多少，输出肯定是 Yes
        // 警告    运算符不正确: 在 Boolean 上下文中执行了常量赋值．应考虑改用「==」．
        ```

    -   如果确实想在原应使用 `==` 的语句里使用 `=`（比如 `while (foo = bar)`），又不想收到 Warning，可以使用 **双括号**：`while ((foo = bar))`．

-   由于运算符优先级产生的错误．

    -   示例：

        ```cpp
        // 错误
        // std::cout << (1 << 1 + 1);
        // 正确
        std::cout << ((1 << 1) + 1);

        // 警告    「<<」: 检查运算符优先级是否有可能的错误；使用括号阐明优先级
        ```

-   不正确地使用 `static` 修饰符．

-   使用 `scanf` 读入的时候没加取地址符 `&`．

-   使用 `scanf` 或 `printf` 的时候参数类型与格式指定符不符．

-   同时使用位操作和逻辑运算符 `==` 并且未加括号．
    -   示例：`(x >> j) & 3 == 2`

-   `int` 字面量溢出．

    -   示例：`long long x = 0x7f7f7f7f7f7f7f7f`，`1<<62`．

-   未初始化局部变量．

    ???+ note "未初始化变量会发生什么"
        原文：<https://loj.ac/d/3679> by @hly1204
        
        例如我们在 C++ 中声明一个 `int a;` 但不初始化，可能有时候会认为 `a` 是一个「随机」（其实可能不是真的随机）的值，但是可能将其认为是一个固定的值，但实际上并非如此．
        
        我们在简单的测试代码中
        
        <https://wandbox.org/permlink/T2uiVe4n9Hg4EyWT>
        
        代码是：
        
        ```cpp
        #include <iostream>
        
        int main() {
          int a;
          std::cout << std::boolalpha << (a < 0 || a == 0 || a > 0);
          return 0;
        }
        ```
        
        在一些编译器和环境上开启优化后，其输出为 false．
        
        有兴趣的话可以看 <https://www.ralfj.de/blog/2019/07/14/uninit.html>，尽管其是用 Rust 做的实验，但是本质是一样的．

-   局部变量与全局变量重名，导致全局变量被意外覆盖．（开 `-Wshadow` 就可检查此类错误．）

-   运算符重载后引发的输出错误．
    -   示例：

        ```cpp
        // 本意：前一个 << 为重载后的运算符，表示输出；后一个 << 为移位运算符，表示将 1
        // 左移 1 位． 但由于忘记加括号，导致编译器将后一个 <<
        // 也判作输出运算符，而导致输出的结果与预期不同． 错误 std::cout << 1 << 1; 正确
        std::cout << (1 << 1);
        ```

## 既不会引起 CE 也不会引发 Warning 的错误

这类错误无法被编译器发现，仅能自行查明．

### 会导致 WA 的错误

-   上一组数据处理完毕，读入下一组数据前，未清空数组．

-   读入优化未判断负数．

-   所用数据类型位宽不足，导致溢出．
    -   如习语「三年 OI 一场空，不开 `long long` 见祖宗」所描述的场景．选手因为没有在正确的地方开 `long long`（将整数定义为 `long long` 类型），导致得出错误的答案而失分．

-   存图时，节点编号 0 开始，而题目给的边中两个端点的编号从 1 开始，读入的时候忘记 -1．

-   大/小于号打错或打反．

-   在执行 `ios::sync_with_stdio(false);` 后混用 `scanf/printf` 和 `std::cin/std::cout` 两种 IO，导致输入/输出错乱．

    -   示例：

        ```cpp
        // 这个例子将说明关闭与 stdio 的同步后，混用两种 IO 方式的后果
        // 建议单步运行来观察效果
        #include <cstdio>
        #include <iostream>

        int main() {
          // 关闭同步后，cin/cout 将使用独立缓冲区，而不是将输出同步至 scanf/printf
          // 的缓冲区，从而减少 IO 耗时
          std::ios::sync_with_stdio(false);
          // cout 下，使用'\n'换行时，内容会被缓冲而不会被立刻输出
          std::cout << "a\n";
          // printf 的 '\n' 会刷新 printf 的缓冲区，导致输出错位
          printf("b\n");
          std::cout << "c\n";
          // 程序结束时，cout 的缓冲区才会被输出
          return 0;
        }
        ```

-   由于宏的展开，且未加括号导致的错误．

    -   示例：该宏返回的值并非 $4^2 = 16$ 而是 $2+2\times 2+2 = 8$．

        ```cpp
        #define square(x) x* x
        printf("%d", square(2 + 2));
        ```

-   哈希的时候没有使用 `unsigned` 导致的运算错误．
    -   对负数的右移运算会在最高位补 1．参见：[位操作符](../lang/op.md#位操作符)．

-   没有删除或注释掉调试输出语句．

-   误加了 `;`．

    -   示例：

        ```cpp
        /* clang-format off */
        while (1);
            printf("OI Wiki!\n");
        ```

-   哨兵值设置错误．例如，平衡树的 `0` 节点．

-   在类或结构体的构造函数中使用 `:` 初始化变量时，变量声明顺序不符合初始化时候的依赖关系．

    -   成员变量的初始化顺序与它们在类中声明的顺序有关，而与初始化列表中的顺序无关．参见：[构造函数与成员初始化器列表](https://zh.cppreference.com/w/cpp/language/constructor) 的「初始化顺序」
    -   示例：

        ```cpp
        #include <iostream>

        class Foo {
         public:
          int a, b;

          // a 将在 b 前初始化，其值不确定
          Foo(int x) : b(x), a(b + 1) {}
        };

        int main() {
          Foo bar(1, 2);
          std::cout << bar.a << ' ' << bar.b;
        }

        // 可能的输出结果：-858993459 1
        ```

-   并查集合并集合时没有把两个元素的祖先合并．

    -   示例：

        ```cpp
        f[a] = b;              // 错误
        f[find(a)] = find(b);  // 正确
        ```

-   `freopen` 使用 `a` 进行追加写
    -   CCF 的检测环境不会清空输出文件，使用 `a` 会导致上一位选手的输出也被评测机读入引发 WA

#### 换行符不同

???+ warning "Warning"
    在正式比赛中会尽量保证选手答题的环境和最终测试的环境相同．
    
    本节内容仅适用于模拟赛等情况，而我们也建议出题人尽量让数据符合 [数据格式](problemsetting.md#数据的格式)．

不同的操作系统使用不同的符号来标记换行，以下为几种常用系统的换行符：

-   LF（用 `\n` 表示）：`Unix` 或 `Unix` 兼容系统

-   CR+LF（用 `\r\n` 表示）：`Windows`

-   CR（用 `\r` 表示）：`Mac OS` 版本 9 及以前

而 C/C++ 利用转义序列 `\n` 来换行，这可能会导致我们认为输入中的换行符也一定是由 `\n` 来表示，而只读入了一个字符来代表换行符，这就会导致我们没有完全读入输入文件．

以下为解决方案：

-   多次 `getchar()`，直到读到想要的字符为止．

-   使用 `cin` 读入，**这可能会增大代码常数**．

-   使用 `scanf("%s",str)` 读入一个字符串，然后取 `str[0]` 作为读入的字符．

-   使用 `scanf(" %c",&c)` 过滤掉所有空白字符．

### 会导致未知的结果

未定义行为会导致未知的结果，可能是 WA，RE 等．编译器通常会假定你的程序不会出现未定义行为，因此出现开 O2 与不开 O2 代码行为不一致的情况．

-   除以 0（求 0 的逆元）

    ???+ warning "示例"
        ```cpp
        cout << x / 0 << endl;
        ```

-   数组（下标）越界

    例如：

    -   未正确设置循环的初值导致访问了下标为 -1 的值．

    -   无向图边表未开 2 倍．

    -   线段树未开 4 倍空间．

    -   看错数据范围，少打一个零．

    -   错误预估了算法的空间复杂度．

    -   写线段树的时候，`pushup` 或 `pushdown` 叶节点．

        正确的做法：不要越界，记得检查自己的代码，使得下标访问数 `x` 在定义的下标中．

-   除 main 外有返回值函数执行至结尾未执行任何 return 语句

    即使有一个分支有返回值，但是其他分支却没有，结果也是未定义的．

    可以向编译选项中追加 `-Wall`，检查编译器是否给出有关于函数未 return 的警告．

-   尝试修改字符串字面量

    ???+ warning "示例"
        ```cpp
        char *p = "OI-wiki";
        p[0] = 'o';
        p[1] = 'i';
        ```

    这样试图修改字符串字面量会导致 **未定义行为**，应当使用其他 **合适** 的数据类型，例如 `std::string` 和 `char[]`．

-   多次释放/非法解引用一片内存

    例如：

    -   未初始化就解引用指针．

    -   指针指向的内存区域已经释放．

        使用 `erase` 或 `delete` 或 `free` 操作应注意不要对同一地址/对象多次使用．

-   尝试释放由 `new []` 分配的整块内存的一部分

    例如：

    ```cpp
    object *pool = new object[POOL_SIZE];

    object *pointer = pool + 10;

    // 报错！
    delete pointer;
    ```

    常见于使用内存池提前分配整块内存后，试图使用 `delete` 或 `free()` 释放从内存池中获取的单个对象．

-   解引用空指针/野指针

    对于空指针：先应该判断空指针，可以用 `p == nullptr` 或 `!p`．

    对于野指针：可以释放指针的时候将其置为 `nullptr` 以规避．

-   有符号数溢出

    例如我们有一个表达式 `x+1 > x`．

    正常输出应当是 `true`，但是在 `INT_MAX` 作为 `x` 时输出 `false`，这时称为 `signed integer overflow`．

    可以使用更大的数据类型（例如 `long long` 或 `__int128`），或判断溢出．若保证无负数，亦可使用无符号整型．

    有符号整数溢出可能影响编译优化，例如代码：

    ```cpp
    int foo(int x) {
      if (x > x + 1) return 1;
      return 0;
    }
    ```

    可能被编译器直接优化为：

    ```cpp
    int foo(int x) { return 0; }
    ```

    因为编译器可以假定有符号整数永远不会溢出，因此 `x > x + 1` 永远不会成立．

-   使用未初始化的变量

    ???+ warning "示例"
        ```cpp
        int foo(int a) {
          int t; /* 没有初始化 */
          if (/* 使用 */ t > 3) return a;
          return 0;
        }
        ```

### 会导致 RE

-   没删文件操作（某些 OJ）．

-   排序时比较函数的错误 `std::sort` 要求比较函数是严格弱序：`a<a` 为 `false`；若 `a<b` 为 `true`，则 `b<a` 为 `false`；若 `a<b` 为 `true` 且 `b<c` 为 `true`，则 `a<c` 为 `true`．其中要特别注意第二点．
    如果不满足上述要求，排序时很可能会 RE．
    例如，编写莫队的奇偶性排序时，这样写是错误的：

    ```cpp
    bool operator<(const int a, const int b) {
      if (block[a.l] == block[b.l])
        return (block[a.l] & 1) ^ (a.r < b.r);
      else
        return block[a.l] < block[b.l];
    }
    ```

    上述代码中 `(block[a.l]&1)^(a.r<b.r)` 不满足上述要求的第二点．
    改成这样就正确了：

    ```cpp
    bool operator<(const int a, const int b) {
      if (block[a.l] == block[b.l])
        // 错误：不满足严格弱序的要求
        // return (block[a.l] & 1) ^ (a.r < b.r);
        // 正确
        return (block[a.l] & 1) ? (a.r < b.r) : (a.r > b.r);
      else
        return block[a.l] < block[b.l];
    }
    ```

-   Windows 下栈空间不足，导致栈空间溢出，Windows 向程序发出 SIGSEGV 信号，程序终止并返回 3221225725（即 0xC00000FD, NTSTATUS 定义为 `STATUS_STACK_OVERFLOW`）．  
    若使用 gcc 编译器，可在编译时加入命令 `-Wl,--stack=SIZE` 以指定栈空间大小限制，其中 `SIZE` 为栈空间大小字节数．

    Linux 下栈空间不足，导致栈空间溢出，Linux 会在栈堆中乱写 `head_info`，此操作绝大多数情况下会导致程序立即退出，显示 `段错误（核心已转储）/segmentation fault (core dumped)` 等字样．  
    可以在终端下使用 `ulimit -s SIZE` 修改当前终端的栈空间限制，其中 `SIZE` 为栈空间大小千字节数（KB）．  
    **请注意，如果你将栈空间限制设置过大，无穷递归可能导致递归栈过大进而导致系统崩溃．**

### 会导致 TLE

-   分治未判边界导致死递归．

-   死循环．

    -   循环变量重名．

    -   循环方向反了．

-   BFS 时不标记某个状态是否已访问过．

-   使用宏展开编写 min/max

    这种错误会大大增加程序的运行时间，甚至直接影响代码的时间复杂度．在初学者写线段树时尤为多见．

    常见的错误写法是这样的：

    ```cpp
    #define Min(x, y) ((x) < (y) ? (x) : (y))
    #define Max(x, y) ((x) > (y) ? (x) : (y))
    ```

    这样写虽然在正确性上没有问题，但是如果直接对函数的返回值取 max，如 `a = Max(func1(), func2())`，而这个函数的运行时间较长，则会大大影响程序的性能，因为宏展开后是 `a = func1() > func2() ? func1() : func2()` 的形式，调用了三次函数，比正常的 max 函数多调用了一次．注意，如果 `func1()` 每次返回的答案不一样，还会导致这种 `max` 的写法出现错误．例如 `func1()` 为 `return ++a;` 而 `a` 为全局变量的情况．

    示例：如下代码会被卡到单次查询 $\Theta(n)$ 导致 TLE．

    ```cpp
    #define max(x, y) ((x) > (y) ? (x) : (y))

    int query(int t, int l, int r, int ql, int qr) {
      if (ql <= l && qr >= r) {
        ++ti[t];  // 记录结点访问次数方便调试
        return vi[t];
      }

      int mid = (l + r) >> 1;
      if (mid >= qr) return query(lt(t), l, mid, ql, qr);
      if (mid < ql) return query(rt(t), mid + 1, r, ql, qr);
      return max(query(lt(t), l, mid, ql, qr), query(rt(t), mid + 1, r, ql, qr));
    }
    ```

-   使用 + 运算符向 `std::string` 类字符串追加字符

    这种错误会创建一个临时 `string` 变量，修改完成后再赋值给原变量．这种错误无法被编译器优化，在数据量大的情况下可能会导致时间复杂度退化．

    常见 错误写法：

    ```cpp
    std::string a;
    char b = 'c';
    a = a + b;
    ```

    当执行这段代码时，程序首先会创建一个临时 `string` 变量，随后将 `a` 的值存入临时变量，然后在末尾添加 `b` 的值，最后再存入 `a`．

    从 [汇编结果](https://godbolt.org/z/Eo9vn7or5) 可以看出，`a = a + b` 调用了三次 `std::__cxx11::basic_string` 中的功能，分别为 `operator+`、`operator=` 和创建变量．

    正确写法应该是：

    ```cpp
    std::string a;
    char b = 'c';
    a += b;
    ```

    [这种写法](https://godbolt.org/z/eGh33Grf3) 会直接将字符 `b` 附加到字符串 `a` 中，仅调用了一次 `operator+=`．更详细的性能比较可参考 [Benchmark](https://quick-bench.com/q/JNDGl7HgOszNG-bo7AgVc42owv4)．

-   没删文件操作（某些 OJ）．

-   在 `for/while` 循环中重复执行复杂度非 $O(1)$ 的函数．严格来说，这可能会引起时间复杂度的改变．

-   进行二分搜索时中点公式或终止条件错误．

### 会导致 MLE

-   数组过大．

    ??? note "Linux 下的内存占用指标详解"
        > 太长不看版：如果在 CCF 系列的考试时声明了一个特别大的全局静态数组，此时需要特别慎重．因为程序声明的数组会全部计入内存占用中（而不像大部分在线评测平台仅计算实际使用的部分），在某些情况下这甚至有可能导致整道题全部 MLE．
        
        -   关于 RSS 和 VSZ[^ref1][^ref2]
        
            1.  VSZ (Virtual Memory Size，虚拟内存大小）[^ref3]
        
                VSZ 表示进程的 **虚拟内存大小**，是进程可以访问的虚拟地址空间的总大小，通常以 KB 显示．
        
                虚拟内存是一个逻辑概念，通常会比实际内存使用大很多．
        
                在 Linux 下你可以使用 `top` 命令来查看某个进程的内存占用组成，其中 `VIRT` 这一列就代表它占用的虚拟内存．
        
                虚拟内存一般包括进程分配但未实际使用的地址空间，简而言之，申请了多少，虚拟内存就大约是多少．
        
                需要特别注意的是，常用的在线评测平台通常只统计物理内存占用．但 **CCF 的评测环境统计的是虚拟内存**，这意味着如果你声明了一个全局静态大数组，即使只使用了其中的一小部分，也会占用大量空间．
            2.  RSS（Resident Set Size，常驻集大小）[^ref4]
        
                RSS 表示进程实际占用的 **物理内存大小**，即驻留在 RAM 中的页帧大小，通常以 KB 显示．
        
                同样的，你也可以用 `top` 在 `RES` 这一列查看某个进程的物理内存．
        
                RSS 一般仅包含实际加载到物理内存的部分，也就是说，实际使用了多少就是多少．
        -   内存占用行为分析
        
            假设声明了以下数组：
        
            ```cpp
            const int SIZE = 1e8;
            int arr[SIZE];  // 占用空间：4 字节 * 1 亿 = 400 MB
            ```
        
            这是一个静态数组，分配在全局数据段．这个数组未经显式初始化，通常会被分配在 BSS 段（如果显式初始化（如全为 0 或其他值），则分配在 DATA 段）．
        
            -   当完全未使用该数组时（假定编译器不会优化掉该数组）
        
                -   物理内存：如果数组未被访问，按需分页机制（Demand Paging）会使内存页尚未加载到物理内存中．物理内存不会增加或仅略微增加一点（可能加载了一些元数据页）．
                -   虚拟内存：数组的大小会计入虚拟内存（增加 `400MB`），因为整个数组的虚拟地址空间已经被分配．
            -   部分使用该数组时
        
                假设仅使用数组的少部分元素，例如：
        
                ```cpp
                arr[0] = 1;
                arr[999999] = 2;
                ```
        
                -   虚拟内存：虚拟内存不会改变，仍为 `400MB`．
                -   物理内存：每次访问数组的一个元素，对应的虚拟页会被加载到物理内存中．假定系统分页大小为 `4KB`，那么每页包含 $4 \text{KB} ÷ 4 \text{B} = 1024$ 个 `int` 元素．访问数组两次可能加载 2 个页，即增加约 $2 \times 4 \text{KB} = 8 \text{KB}$ 的物理内存．
            -   数组被大半使用
        
                假设对数组的前 $50,000,000$ 个元素赋值：
        
                ```cpp
                for (int i = 0; i < 50000000; ++i) {
                  arr[i] = i;
                }
                ```
        
                -   虚拟内存 (VSZ)：VSZ 仍为 `400MB`，不会发生变化．
                -   物理内存 (RSS)：此时是连续访问（访问的 $50,000,000$ 个元素在内存地址上相邻），需要加载的分页数为 $\left\lceil \dfrac{50,000,000}{1024} \right\rceil = 48,828$ 页．
        
                    假设每页大小为 `4KB`，因此总计 $48,828 \times 4 \text{KB} \approx 190 \text{MB}$，物理内存增加到约 `190MB`．
        
                    注：如果对该数组赋值时下标随机，则会导致物理内存占用与预测差距较大（因为内存页加载是以地址为准，导致随机赋值时会加载大量内存页）．
        
                简要总结：随着被访问的部分占的比例增加，物理内存趋近于虚拟内存（假定不存在页面回收）．
-   STL 容器中插入了过多的元素．

    -   经常是在一个会向 STL 插入元素的循环中死循环了．

    -   也有可能被卡了．

### 会导致常数过大

-   定义模数的时候，未定义为常量．

    -   示例：

        ```cpp
        // int mod = 998244353;      // 错误
        const int mod = 998244353;  // 正确，方便编译器按常量处理
        ```

-   使用了不必要的递归（尾递归不在此列）．

-   将递归转化成迭代的时候，引入了大量额外运算．

### 只在程序在本地运行的时候造成影响的错误

-   文件操作有可能会发生的错误：

    -   对拍时未关闭文件指针 `fclose(fp)` 就又令 `fp = fopen()`．这会使得进程出现大量的文件野指针．

    -   `freopen()` 中的文件名未加 `.in`/`.out`．

-   使用堆空间后忘记 `delete` 或 `free`．

## 参考资料与注释

[^ref1]: [What is RSS and VSZ in Linux memory management - Stack Overflow](https://stackoverflow.com/questions/7880784/what-is-rss-and-vsz-in-linux-memory-management)

[^ref2]: [Need explanation on Resident Set Size/Virtual Size - Stack Overflow](https://unix.stackexchange.com/questions/35129/need-explanation-on-resident-set-size-virtual-size)

[^ref3]: [虚拟内存](https://zh.wikipedia.org/wiki/%E8%99%9A%E6%8B%9F%E5%86%85%E5%AD%98)

[^ref4]: [常驻集大小](https://zh.wikipedia.org/wiki/%E5%B8%B8%E9%A9%BB%E9%9B%86%E5%A4%A7%E5%B0%8F)


## contest/common-tricks.md

author: H-J-Granger, Ir1d, ChungZH, Marcythm, StudyingFather, billchenchina, Suyun514, Psycho7, greyqz, Xeonacid, partychicken

本页面主要列举一些竞赛中的小技巧．

## 利用局部性

局部性是指程序倾向于引用邻近于其他最近引用过的数据项的数据项，或者最近引用过的数据项本身．局部性分为时间局部性和空间局部性．

具体可参见 [循环展开 (Loop Unroll)](../lang/optimizations.md#循环展开-loop-unroll)、[代码布局优化 (Code Layout Optimizations)](../lang/optimizations.md#代码布局优化-code-layout-optimizations) 等内容

## 循环宏定义

如下代码可使用宏定义简化：

```cpp
for (int i = 0; i < N; i++) {
  // 循环内容略
}

// 使用宏简化
#define f(x, y, z) for (int x = (y), __ = (z); x < __; ++x)

// 这样写循环代码时，就可以简化成 `f(i, 0, N)` ．例如：
// a is a STL container
f(i, 0, a.size()) { ... }
```

另外推荐一个比较有用的宏定义：

```cpp
#define _rep(i, a, b) for (int i = (a); i <= (b); ++i)
```

## 善用 namespace

使用 namespace 能使程序可读性更好，便于调试．

??? note "例题：NOI 2018 屠龙勇士"
    ```cpp
    // NOI 2018 屠龙勇士 40分部分分代码
    #include <algorithm>
    #include <cmath>
    #include <cstring>
    #include <iostream>
    using namespace std;
    long long n, m, a[100005], p[100005], aw[100005], atk[100005];
    
    namespace one_game {
    // 其实namespace里也可以声明变量
    void solve() {
      for (int y = 0;; y++)
        if ((a[1] + p[1] * y) % atk[1] == 0) {
          cout << (a[1] + p[1] * y) / atk[1] << endl;
          return;
        }
    }
    }  // namespace one_game
    
    namespace p_1 {
    void solve() {
      if (atk[1] == 1) {  // solve 1-2
        sort(a + 1, a + n + 1);
        cout << a[n] << endl;
        return;
      } else if (m == 1) {  // solve 3-4
        long long k = atk[1], kt = ceil(a[1] * 1.0 / k);
        for (int i = 2; i <= n; i++)
          k = aw[i - 1], kt = max(kt, (long long)ceil(a[i] * 1.0 / k));
        cout << k << endl;
      }
    }
    }  // namespace p_1
    
    int main() {
      int T;
      cin >> T;
      while (T--) {
        memset(a, 0, sizeof(a));
        memset(p, 0, sizeof(p));
        memset(aw, 0, sizeof(aw));
        memset(atk, 0, sizeof(atk));
        cin >> n >> m;
        for (int i = 1; i <= n; i++) cin >> a[i];
        for (int i = 1; i <= n; i++) cin >> p[i];
        for (int i = 1; i <= n; i++) cin >> aw[i];
        for (int i = 1; i <= m; i++) cin >> atk[i];
        if (n == 1 && m == 1)
          one_game::solve();  // solve 8-13
        else if (p[1] == 1)
          p_1::solve();  // solve 1-4 or 14-15
        else
          cout << -1 << endl;
      }
      return 0;
    }
    ```

## 使用宏进行调试

编程者在本地测试的时候，往往要加入一些调试语句．而在需要提交到 OJ 时，为了不使调试语句的输出影响到系统对程序输出结果的判断，就要把它们全部删除，耗时较多．这种情况下，可以通过定义宏的方式来节省时间．大致的程序框架是这样的：

```cpp
#define DEBUG
#ifdef DEBUG
// do something when DEBUG is defined
#endif
// or
#ifndef DEBUG
// do something when DEBUG isn't defined
#endif
```

`#ifdef` 会检查程序中是否有 `#define` 定义的对应标识符，如果有定义，就会执行后面的语句．而 `#ifndef` 会在没有定义相应标识符的情况下执行后面的语句．

这样，只需在 `#ifdef DEBUG` 里写好调试用代码，`#ifndef DEBUG` 里写好真正提交的代码，就能方便地进行本地测试．提交程序的时候，只需要将 `#define DEBUG` 一行注释掉即可．也可以不在程序中定义标识符，而是通过 `-DDEBUG` 的编译选项在编译的时候定义 `DEBUG` 标识符．这样就可以在提交的时候不用修改程序了．

不少 OJ 都开启了 `-DONLINE_JUDGE` 这一编译选项，善用这一特性可以节约不少时间．

## 对拍

对拍是一种进行检验或调试的方法，通过对比两个程序的输出来检验程序的正确性．可以将自己程序的输出与其他程序的输出进行对比，从而判断自己的程序是否正确．

对拍过程要多次进行，因此需要通过批处理的方法来实现对拍的自动化．

具体而言，对拍需要一个 [数据生成器](../tools/testlib/generator.md) 和两个要进行输出结果比对的程序．

每运行一次数据生成器都将生成的数据写入输入文件，通过重定向的方法使两个程序读入数据，并将输出写入指定文件，最后利用 Windows 下的 `fc` 命令比对文件（Linux 下为 `diff` 命令）来检验程序的正确性．如果发现程序出错，可以直接利用刚刚生成的数据进行调试．

对拍程序的大致框架如下：

```cpp
#include <cstdio>
#include <cstdlib>

int main() {
  // For Windows
  // 对拍时不开文件输入输出
  // 当然，这段程序也可以改写成批处理的形式
  while (true) {
    system("gen > test.in");  // 数据生成器将生成数据写入输入文件
    system("test1.exe < test.in > a.out");  // 获取程序1输出
    system("test2.exe < test.in > b.out");  // 获取程序2输出
    if (system("fc a.out b.out")) {
      // 该行语句比对输入输出
      // fc返回0时表示输出一致，否则表示有不同处
      system("pause");  // 方便查看不同处
      return 0;
      // 该输入数据已经存放在test.in文件中，可以直接利用进行调试
    }
  }
}
```

## 内存池

当动态分配内存时，频繁使用 `new`/`malloc` 会占用大量的时间和空间，甚至生成大量的内存碎片从而降低程序的性能，可能会使原本正确的程序 TLE/MLE．

这时候需要使用到「内存池」这种技巧：在真正使用内存之前，先申请分配一定大小的内存作为备用．当需要动态分配时直接从备用内存中分配一块即可．

在大多数 OI 题当中，可以预先算出需要使用到的最大内存并一次性申请分配．

示例：

```cpp
// 申请动态分配 32 位有符号整数数组：
int* newarr(int sz) {
  static int pool[MAXN], *allocp = pool;
  return allocp += sz, allocp - sz;
}

// 线段树动态开点的代码：
Node* newnode() {
  static Node pool[MAXN << 1], *allocp = pool - 1;
  return ++allocp;
}
```

## 参考资料

[洛谷日报 #86](https://studyingfather.blog.luogu.org/some-coding-tips-for-oiers)

《算法竞赛入门经典 习题与解答》


## contest/dictionary.md

前置知识：[分块](../ds/decompose.md)．

朴素的打表，指的是在比赛时把所有可能的输入对应的答案都计算出来并保存下来，然后在代码里开个数组把答案放里面，直接输出即可．

注意这个技巧只适用于输入的值域不大（如，输入只有一个数，而且范围很小）的问题，否则可能会导致代码过长、MLE、打表需要的时间过长等问题．

???+ note "例题"
    规定 $f(x)$ 为整数 $x$ 的二进制表示中 $1$ 的个数．输入一个正整数 $n$($n\leq 10^9$)，输出 $\sum_{i=1}^n f^2(i)$．

如果对于每一个 $n$，都输出 $f(n)$ 的话，除了可能会 MLE 外，还有可能代码超过最大代码长度限制，导致编译不通过．

我们考虑优化这个答案表．采用 [分块](../ds/decompose.md) 的思想，我们设置一个合理的步长 $m$（这个步长一般视代码长度而定），对于第 $i$ 块，计算出：

$$
\sum_{k=\frac{n}{m}(i-1)+1}^{\frac{ni}{m}} f^2(k)
$$

的值．

然后输出答案时采用分块思想处理即可．即，整块的答案用预处理的值计算，非整块的答案暴力计算．

一般来说，这样的问题对于处理单个函数值 $f(x)$ 很快，但是需要大量函数值求和（求积或某些可以快速合并的操作），枚举会超出时间限制，在找不到标准做法的情况下，分段打表是一个不错的选择．

???+ note "注意事项"
    当上题中指数不是定值，但是范围较小，也可以考虑打表．

### 例题

[「BZOJ 3798」特殊的质数](https://hydro.ac/p/bzoj-P3798)：求 $[l,r]$ 区间内有多少个质数可以分解为两个正整数的平方和．

[「Luogu P1822」魔法指纹](https://www.luogu.com.cn/problem/P1822)


## contest/icpc.md

author: NachtgeistW, Ir1d, Xeonacid, H-J-Granger, abc1763613206, YuzhenQin

## 赛事介绍

### ICPC

**ICPC**（英文：International Collegiate Programming Contest，中文：国际大学生程序设计竞赛）由 ICPC 基金会（英文：ICPC Foundation）举办，是最具影响力的大学生计算机竞赛．由于以前 ACM 赞助这个竞赛，也有很多人习惯叫它 ACM 竞赛．

ICPC 主要分为区域赛（Regionals）和总决赛（World Finals）两部分．

官网地址：<https://icpc.global>

### CCPC

官网地址：<https://ccpc.io>

中国大学生程序设计竞赛．

和 ICPC 显著的区别是很多学校是不报销的．

## 赛制介绍

一般是三个人组成一队使用一台机器，在比赛时有多次提交机会．比赛实时评测并返回结果，如果提交的结果错误会有 20 分钟的罚时，错误次数越多，加罚的时间也越长．每个题目只有在所有数据点全部正确后才能得到分数．比赛排名根据做题数来评判，做题数相同的，根据总用时来评判．总用时是每题用时的和．每题的用时是从比赛开始到做出该题的分钟数与该题的罚时之和．

一些 ICPC 相关赛事中，比赛结束前一小时进行封榜，封榜后的提交和排名将无法被其他选手看见．

在 ICPC 相关赛事中，选手允许带一定量的纸质资料．

除 ICPC 和 CCPC 外，众多比赛也采用该赛制，如 LeetCode 周赛及全国编程大赛、牛客小白赛练习赛挑战赛等．

## 赛季赛程

-   ICPC/CCPC 网络赛（8 月底至 9 月初）
-   ICPC/CCPC 区域赛（9 月底至 11 月底）
-   ICPC EC Final/CCPC Final（12 月中旬）
-   ICPC World Finals（次年 4 月至 6 月）

## 训练指南

### 多校联合训练

暑期在 [HDU OJ](http://acm.hdu.edu.cn) 举行的训练赛．有奖金，题目质量高，历经多年积累已有丰富资源．

OJ 里查询用的关键词：`Multi-University Training Contest`．

### 国内区域赛

在 [Virtual Judge](https://vjudge.net/) 里可以搜到精选题集．

### 训练营

-   寒假的时候头条/清华/CCPC (Wannafly Camp) 举办的 Camp
-   Wannafly Camp

## 训练资源

-   QOJ：<https://qoj.ac>
-   Codeforces Gym：<https://codeforces.com/gyms>


## contest/interaction.md

author: countercurrent-time, StudyingFather

上个世纪的 IOI 就已涉及交互题．虽然交互题近年来没有在省选以下的比赛中出现，不过 2019 年里 NOI 系列比赛中连续出现《P5208\[WC2019]I 君的商店》、《P5473\[NOI2019]I 君的探险》两道交互题，这可能代表着交互题重新回到 NOI 系列比赛中．

交互题没有很高的前置算法要求，一般也没有严格的时间限制，程序的优秀程度往往仅取决于交互次数限制．所以学习交互题时，建议按照难度循序渐进．要是有意锻炼算法思维而不只是单纯地学习算法，那么完成交互题是很不错的方法．虽然交互题对选手已掌握算法的要求通常较低，但仍建议掌握一定提高和省选算法后再尝试做交互题，因为此时自己的算法思维水平和知识面已经达到了一定水平．基础的交互题介绍可以参考 **OI Wiki** 的 [题型介绍 - 交互题](./problems.md#交互题)．

交互题的特殊错误：

-   选手每一次输出后都需要刷新缓冲区，否则会引起 Idleness limit exceeded 错误．另外，如果题目含多组数据并且程序可以在未读入所有数据前就知道答案，也仍然要读入所有数据，否则同样会因为读入混乱引起 ILE（可以一次提出多次询问，一次接收所有询问的回答）．同时尽量不要使用快读．
-   如果程序查询次数过多，则在 Codeforces 上会给出 Wrong Answer 的评测结果（不过评测系统会说明 Wrong Answer 的原因），而 UVa 会给出 Protocol Limit Exceeded (PLE) 的评测结果．
-   如果程序交互格式错误，UVa 会给出 Protocol Violation (PV) 的评测结果．

由于交互题输入输出较为繁琐，所以建议分别封装输入和输出函数．

比赛时如果出题人给出了 grader 头文件（用于 grader 交互题的调试）或者 checker 程序（用于 stdio 交互题的调试），则交互题的调试比较简单，因为交互题的对拍会比普通题目的对拍困难很多．没有 `testlib.h` 的情况下．交互细节较多的题目的 stdio 交互库会一般有 3k 代码量，再加上 3k 长度的对拍器，至少需要一小时实现．但是，无论是否有调试程序，调试交互题的代码都往往需要选手模拟与程序的交互过程，因此交互题需要选手能设计出高质量的程序，尽量保证一遍做对，同时拥有较强的静态查错能力．

例题：

-   [CF679A Bear and Prime 100](https://codeforces.com/problemset/problem/679/A)
-   [CF843B Interactive LowerBound](https://codeforces.com/problemset/problem/843/B)
-   [UOJ206\[APIO2016\]Gap](http://uoj.ac/problem/206)
-   [CF750F New Year and Finding Roots](https://codeforces.com/problemset/problem/750/F)
-   [UVa12731 太空站之谜 Mysterious Space Station](https://onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&category=823&page=show_problem&problem=4584)

## CF679A Bear and Prime 100

每个质数都有且只有两个因数，所以直接枚举要猜的数的因数．由于限制最多询问 20 次，并且对于较大的数（如 92）尝试分解质因数时发现需要最多枚举到 $\lfloor\frac{n}{2}\rfloor$ 的质数．所以我们先筛出 50 以内的质数，每次把所有这些数都询问一遍．

由于本题对拍比较容易，可以直接把值域内的数都尝试一遍．我们会发现程序无法有效处理质数的平方．所以我们要把 2,3,5,7 的平方 4,9,25,49 都放进去，总共 19 个数字，符合题意．

??? note "参考代码"
    ```cpp
    #include <cstdio>
    constexpr int prime[] = {2,  3,  4,  5,  7,  9,  11, 13, 17, 19,
                             23, 25, 29, 31, 37, 41, 43, 47, 49};
    int cnt = 0;
    char res[5];
    
    int main() {
      for (int i : prime) {
        printf("%d\n", i);
        fflush(stdout);
        scanf("%s", res);
        if (res[0] == 'y' && ++cnt == 2) return printf("composite"), 0;
      }
      printf("prime");
      return 0;
    }
    ```

## CF843B Interactive LowerBound

链表最多有 $5 \times 10 ^ 4$ 个元素，但我们只能询问 $1999$ 次，并且只能获取元素的后一个元素，所以普通的遍历整个链表的方法不可用．直接设法逼近目标元素的位置只有一种方法：随机撒点．

对于 $n < 2000$ 的情况直接枚举，$n \ge 2000$ 时，我们直接撒 1000 个点，这时这些点之间的期望距离很小，我们可以直接从小于 $x$ 的最大值开始向后遍历，可以证明在到达下一个点之前我们就已得到答案．遍历的过程中一旦找到大于等于 $x$ 的元素，就可以直接推出．

虽然整体思路简单，但实际情况下，如果没有学习过模拟退火等非完美随机算法，思考起来很可能会困难一些．

同时由于 Codeforces 具有 hack 机制，很多人会刻意卡掉没有初始化随机种子的代码，所以在 `random_shuffle()` 函数前需要 `srand((size_t)new char)`．

??? note "参考代码"
    ```cpp
    #include <algorithm>
    #include <cstdio>
    #include <cstdlib>
    constexpr int N = 50005;
    int n, start, x;
    int a[N];
    
    int main() {
      scanf("%d%d%d", &n, &start, &x);
      if (n < 2000) {
        int ans = 2e9;
        for (int i = 1; i <= n; i++) {
          printf("? %d\n", i), fflush(stdout);
          int val, next;
          scanf("%d%d", &val, &next);
          if (val >= x) ans = std::min(ans, val);
        }
        if (ans == 2e9) ans = -1;
        printf("! %d", ans), fflush(stdout);
      } else {
        srand((size_t) new char);
        int p = start, ans = 0;
        for (int i = 1; i <= n; i++) a[i] = i;
        std::random_shuffle(a + 1, a + n + 1);
        for (int i = 1; i <= 1000; i++) {
          printf("? %d\n", a[i]), fflush(stdout);
          int val, next;
          scanf("%d%d", &val, &next);
          if (val < x && val > ans) p = a[i], ans = val;
        }
        while (p != -1 && ans < x) {
          printf("? %d\n", p), fflush(stdout);
          int val, next;
          scanf("%d%d", &val, &next);
          ans = val;
          p = next;
        }
        if (ans < x) ans = -1;
        printf("! %d", ans), fflush(stdout);
      }
      return 0;
    }
    ```

## UOJ206\[APIO2016]Gap

分两个子任务讨论：

1.  查询次数限制．

    我们考虑第一次查询．因为我们一开始不知道任何数，所以我们需要询问范围 $[1, 10 ^ {18}]$，获得最大最小值．

    由于查询次数限制刚好为 $\frac{N + 1}{2}$，所以考虑怎么每一次都能获取之前没有获取过的值，这样能大概在次数范围内获取序列内的所有数．方法也很简单：每次查询 $[s, t]$ 后，设获得的值为 $mn, mx$，则下一次查询 $[mn + 1, mx - 1]$．

2.  询问区间大小限制．

    由于题目要求询问区间内的数的数量之和不能超过 $3N$，所以考虑最小化询问区间．上面的方法不再可用，因为其询问区间内的数数量之和规模为 $O(N ^ 2)$．我们可以考虑二分值域，但这种方法并不可靠，最坏可能会被卡到 $O(N ^ 2)$．所以我们需要更有效的划分值域的方法，避免查询区间内的点重复查询，浪费机会．

    考虑到答案不会小于 $\lfloor\frac{a_n - a_1}{N - 1}\rfloor$，所以我们可以考虑按这个值划分值域，设 $i$ 初始为 0，$ans$ 初始为上述值，每次询问 $[i, i + ans]$ 并且更新 $ans$，之后再以 $ans$ 为步长让 $i$ 自增．

    不过这种方法也不能很好地适用于子任务 1，因为最坏可能很多询问的值域内一个数都没有．

??? note "参考代码"
    ```cpp
    #include <algorithm>
    #include <cstdio>
    
    #include "gap.h"
    
    long long findGap(int T, int N) {
      static long long a[100005] = {}, ans = 0;
      long long s = 0, t = 1e18, s1, t1;
      if (T == 1) {
        int l = 1, r = N;
        while (l <= r) {
          MinMax(s, t, &s1, &t1);
          a[l++] = s1, a[r--] = t1;
          s = s1 + 1, t = t1 - 1;
        }
        for (int i = 2; i <= N; i++) ans = std::max(ans, a[i] - a[i - 1]);
      } else if (T == 2) {
        MinMax(s, t, &s1, &t1);
        ans = (t1 - s1) / (N - 1);
        long long l = s1 + 1, r = t1, last = s1;
        for (long long i = l; i <= r;) {
          MinMax(i, i + ans, &s1, &t1);
          i += ans + 1;
          if (s1 != -1) ans = std::max(ans, s1 - last), last = t1;
        }
      }
      return ans;
    }
    ```

## CF750F New Year and Finding Roots

看到 $h \le 7$，询问次数 $\le 16$ 的严格要求，我们需要非常严格地最大化利用访问获得的信息．

$h \le 4$ 时可以直接暴力枚举．然而 $h > 4$ 时需要很高效的遍历算法．

随机撒点不是好方法，因为随机撒点无法确定自己是否足够接近根节点了，并且单纯随机撒点，至少有一次碰到根节点的概率为 $1 - (\frac{2 ^ h - 2}{2 ^ h - 1})$，即使排除重复撒点的情况后，碰到根节点的概率仍然非常小．

由于 $1 \le k \le 3$，并且我们并不知道哪一边更接近根节点，所以我们考虑最坏的情况，即如果 $k = 3$ 时，前两次我们的遍历方向都是远离根节点的，第三次遍历方向是接近根节点的．所以我们必须往三个方向都遍历．

考虑 bfs 和 dfs 两种遍历方法．由于 bfs 搜索树可能很大，所以我们优先考虑 dfs．当然，如果我们知道当前的深度，并且当前深度小到深度范围内的搜索树规模小于等于剩余次数，我们就可以直接 bfs．

知道当前节点的深度，以及当前遍历的方向会获得很大优势．然而知道当前在往根节点还是在往叶子节点遍历是非常困难的事情．如果使用 dfs，只有当遍历到根节点（$k = 2$）或者叶子节点（$k = 1$）时才知道当前方向．所以我们需要尽可能知道当前节点深度，并且不能采用类似迭代加深搜索的方法，遍历中途停下来．

考虑随机一个初始节点，从初始节点出发可能碰到上面的最坏情况．

如果 $k = 1$，我们就可以直接知道当前节点的深度．

如果 $k = 2$，那当前节点即根节点．

如果 $k = 3$，我们直接考虑往三个方向 dfs．考虑到其中两个方向是直接往叶子节点的方向，遍历路径长度相同；另一个方向是往根节点的方向，不过可能中途不小心往叶子节点的方向走了，遍历路径长度会较大．此时我们就可以计算出当前节点的深度．

当 $k = 1$ 或者 $k = 3$ 时，我们需要考虑较长的遍历路径．我们可以知道路径上深度最小的点（必定比初始节点深度小）．如果我们为访问过的节点打标记，不再遍历，此时从该节点开始就只有一条遍历路径．虽然这条路径可能还是会走向叶子节点，但是这条路径上同样必然存在深度比起点小的节点，我们就可以从这个节点开始继续重复上面的步骤．

当然，我们考虑 $h = 7$ 的最坏情况时（每次只往根节点走一步，就直接往叶子节点走），会发现如果只 dfs，最坏需要 $\frac{(1 + 7) \times 7}{2} = 28$ 次询问．不过我们已经知道初始节点的深度，所以我们可以算出所有已遍历节点的深度，并且根据我们开始时对 bfs 的讨论，判断是否可以从深度最小的点直接 bfs．

这时，我们可以算出最坏需要 17 次．所以我们考虑从搜索树上去掉一个节点（根据 dfs 只能盲目遍历的性质，我们考虑 bfs）：即当进行深度为 $k$ 的 bfs 时，搜索树节点最坏有 $2 ^ k - 1$ 个，可能需要 $2 ^ k - 1$ 次询问才能确定哪个节点的邻居恰有 2 个．不过我们如果已经对其中 $2 ^ k - 2$ 个节点询问后，可以知道最后一个节点肯定是根节点．

此时最坏情况下的最优解为：$h = 7$ 时，从叶子节点 dfs，每次都是只往根节点走一步，就直接往叶子节点走，询问 10 次后，当前已知最小深度的节点深度为 4，由于已知其父亲，直接从其父亲开始 bfs（搜索树深度为 3，节点数为 $2 ^ 3 - 1 = 7$）．在 bfs 时询问了 $2 ^ 3 - 2 = 6$ 次后，确定 bfs 搜索树上最后一个节点为根节点．

此时我们的算法可以刚好卡到最坏 16 次．

??? note "参考代码"
    ```cpp
    #include <algorithm>
    #include <cstdio>
    #include <queue>
    #include <vector>
    using namespace std;
    constexpr int N = 256 + 5;
    int T, h, chance;
    bool ok;
    vector<int> to[N], path;
    
    bool read(int x) {
      if (to[x].empty()) {
        printf("? %d\n", x), fflush(stdout);
        int k, t;
        scanf("%d", &k);
        if (k == 0) exit(0);
        for (int i = 0; i < k; i++) {
          scanf("%d", &t);
          to[x].push_back(t);
        }
        if (k == 2) {
          printf("! %d\n", x), fflush(stdout);
          return ok = true;
        }
        chance--;
      }
      return false;
    }
    
    bool dfs(int x) {
      if (to[x].empty()) path.push_back(x);
      if (read(x)) return true;
      for (int i : to[x])
        if (to[i].empty()) return dfs(i);
      return false;
    }
    
    void bfs(int s, int k) {
      queue<int> q;
      for (int i : to[s])
        if (to[i].empty()) q.push(i);
      for (int i = 1; i < k; i++) {
        int x = q.front();
        q.pop();
        if (read(x)) return;
        for (int j : to[x])
          if (to[j].empty()) q.push(j);
      }
      for (int i = 1; i < k; i++) {
        int x = q.front();
        q.pop();
        if (read(x)) return;
      }
      printf("! %d\n", q.front()), fflush(stdout);
    }
    
    int main() {
      for (scanf("%d", &T); T--;) {
        ok = false;
        for (int i = 0; i < N; i++) to[i].clear();
        chance = 16;
        scanf("%d", &h);
        if (h == 0) exit(0);
        vector<int> long_path;
        if (read(1)) continue;
        int root, dep;
        if (to[1].size() == 1)
          root = 1, dep = h;
        else {
          for (int i : to[1]) {
            path.clear();
            if (dfs(i)) break;
            if (path.size() > long_path.size()) swap(path, long_path);
          }
          if (ok) continue;
          dep = h - (path.size() + long_path.size()) / 2;
          root = long_path.at((long_path.size() - (h - dep)) - 1);
        }
        while ((1 << (dep - 1)) - 2 > chance) {
          path.clear();
          if (dfs(root)) break;
          dep = h - (h - dep + path.size()) / 2;
          root = path.at((path.size() - (h - dep)) - 1);
        }
        if (!ok) bfs(root, 1 << (dep - 2));
      }
      return 0;
    }
    ```

## UVa12731 太空站之谜 Mysterious Space Station

由于唯一的反馈是移动时是否撞墙，所以我们应该考虑在机器人不走丢的情况下，尽量接近墙边走路，这样有几个好处：

-   靠近墙边走路时，很容易知道自己会不会撞墙，获取到尽量多的信息．
-   墙边都是不会出现传送门的格子，可以避免机器人走丢．

所以，我们如果已知机器人可能在墙边的某个位置，要确定机器人是不是真的在这个位置，就可以通过 [「单手扶墙法」](https://en.wikipedia.org/wiki/Maze_solving_algorithm) 确定自己是不是真的在这个位置．根据拓扑学原理，在两边都是墙的迷宫中，如果从入口进入，并且总是用一只手扶着同一边墙，就可以保证找到出口．由于本题中的墙是闭合的，所以只需要沿着墙边的道路走，就可以保证可以回到原点而不会撞墙．另外，由于墙边的道路是地图上的最大闭合回路，所以实际代码中并不需要特意撞墙以保证机器人在墙边，可以使用标记在地图中标明墙边道路．而且一旦撞了墙，就需要赶快沿着原路返回，可以在避免机器人走丢的同时减少步数．

由上，可以推断出确定机器人是否在特定格子的试错法：将机器人在不走到未知格子或已知传送门的情况下走到墙边的道路上，然后绕着墙边道路走一圈．这个过程中如果没有撞墙，就可以确定机器人确实是在特定格子．

我们可以采用上面的方法，一开始标出图中所有未知格子，然后从上到下，从左到右依次判断每个未知格子是否是传送门．可以先走到未知格子上方，然后向下、向左走．再用上面的方法判断机器人是不是在未知格子的左侧．如果不是，说明机器人不在应该在的位置，即未知格子是传送门．

找出未知格子后就需要判断 2k 个未知格子的配对关系，实际方法也很简单：只需要暴力配对就可以了．由于 $k \le 5$，所以最多只需要 $9 + 7 + 5 + 3$ 次试错法．作为对比，判断图中全部未知格子的情况最多需要 $121 - 40$ 次试错法．

由于目前下面这一份代码只能通过 UOJ 的镜像题：[#247.【Rujia Liu's Present 7】Mysterious Space Station](http://uoj.ac/problem/247)，而无法通过 UVa 原题．修改了 UOJ 上刘汝佳的标程后还是无法通过，并且暂时无法联系到刘汝佳．所以下面的代码以 UOJ 为准．

不过刘汝佳的标程质量还是比下面这份代码质量高很多的，可以在 UOJ 上查看到 [通过了 UOJ 镜像题的标程](http://uoj.ac/submission/105789)．同一份数据下，标程使用的移动次数非常少．

??? note "参考代码"
    ```cpp
    #include <algorithm>
    #include <cstdio>
    #include <cstring>
    #include <iostream>
    #include <queue>
    #include <stack>
    
    #define Wall 0
    #define Unknown 1
    #define Space 2
    #define Gate 3
    #define Path 4
    
    const int N = 20;
    const int dir[8][2] = {{0, 1},  {1, 0}, {0, -1}, {-1, 0},
                           {-1, 1}, {1, 1}, {1, -1}, {-1, -1}};
    const char dirs[5] = "ESWN";
    int n, m, k;
    int a[N][N], id[N][N];
    
    struct point {
      int x, y;
    
      point(int x = 0, int y = 0) : x(x), y(y) {}
    
      bool operator==(const point& tmp) const { return x == tmp.x && y == tmp.y; }
    
      bool operator!=(const point& tmp) const { return !(*this == tmp); }
    
      point side(int d) const { return point(x + dir[d][0], y + dir[d][1]); }
    
      int check(int d) { return a[x + dir[d][0]][y + dir[d][1]]; }
    
      int id() { return ::id[x][y]; }
    } start;
    
    std::vector<std::pair<point, int>> path;
    std::pair<point, point> ans[N];
    std::pair<point, bool> vis[N];
    
    bool walk(int d) {
      printf("MoveRobot %c\n", dirs[d]);
      fflush(stdout);
      int ret;
      scanf("%d", &ret);
      return ret;
    }
    
    bool walk(int d, std::stack<int>& st) {
      if (walk(d)) {
        st.push(d);
        return true;
      }
      return false;
    }
    
    bool read() {
      if (scanf("%d%d%d", &n, &m, &k) != 3) return false;
      if (n == 0) return false;
      memset(a, 0, sizeof(a));
      for (int i = 0; i < n; i++)
        for (int j = 0; j < m; j++) {
          char c;
          std::cin >> c;
          if (c == 'S') start = point(i, j);
          if (c == '*')
            a[i][j] = Wall;
          else
            a[i][j] = Unknown;
        }
      return true;
    }
    
    void answer() {
      for (int i = 0; i < k; i++)
        printf("Answer %d %d\n", ans[i].first.id(), ans[i].second.id());
      fflush(stdout);
    }
    
    // 单手扶墙法，因为靠墙的 Path 是极大闭合环，所以只需要在沿着 Path
    // 走的过程中没有碰到障碍就可以了
    void wall_follower_init(point x, int last, int wallside, point s) {
      if (x == s && !path.empty()) return;
      if (x.check(wallside) == Path) {
        path.push_back(std::make_pair(x, wallside));
        wall_follower_init(x.side(wallside), wallside, last ^ 2, s);
      } else if (x.check(last) == Wall) {
        for (int i = 0; i < 4; i++)
          if (i != (last ^ 2) && x.check(i) != Wall) {
            path.push_back(std::make_pair(x, i));
            wall_follower_init(x.side(i), i, last, s);
            return;
          }
      } else {
        path.push_back(std::make_pair(x, last));
        wall_follower_init(x.side(last), last, wallside, s);
      }
    }
    
    void init() {
      int cnt = 1;
      for (int i = 0; i < n; i++)
        for (int j = 0; j < m; j++) {
          if (a[i][j] == Unknown) {
            id[i][j] = cnt++;
            for (int k = 0; k < 8; k++)
              if (point(i, j).check(k) == Wall) {
                a[i][j] = Path;
                break;
              }
          } else
            id[i][j] = 0;
        }
      path.clear();
      int wallside = 0, last = 0;
      for (int i = 0; i < 4; i++)
        if (start.check(i) == Wall) {
          wallside = i;
          break;
        }
      for (int i = 0; i < 4; i++)
        if (start.check(i) == Path && i != (wallside ^ 2)) {
          last = i;
          break;
        }
      wall_follower_init(start, last, wallside, start);
    }
    
    void undo(std::stack<int>& st) {
      while (!st.empty()) walk(st.top() ^ 2), st.pop();
    }
    
    bool wall_follower(point x) {
      std::stack<int> st;
      bool ok = true;
      int i = 0;
      while (i < path.size() && path[i].first != x) i++;
      for (int j = i; ok && j < path.size(); j++) {
        if (walk(path[j].second))
          st.push(path[j].second);
        else
          ok = false;
      }
      for (int j = 0; ok && j < i; j++) {
        if (walk(path[j].second))
          st.push(path[j].second);
        else
          ok = false;
      }
      if (!ok) undo(st);
      return ok;
    }
    
    // 确定自己当前在
    // x，使用「摸着石头过河」的方法，只需要沿着可以避开障碍、未知格子和传送门的方向走到
    // Path 就行． 在找传送门和配对传送门时使用
    void bfs(point s, point t, std::vector<int>& v) {
      static int map[N][N] = {};
      memset(map, -1, sizeof(map));
      std::queue<point> q;
      map[s.x][s.y] = 4;
      q.push(s);
      while (!q.empty()) {
        point x = q.front();
        q.pop();
        if (x == t) break;
        for (int i = 0; i < 4; i++) {
          point y = x.side(i);
          if ((x.check(i) == Path || x.check(i) == Space) && map[y.x][y.y] == -1) {
            map[y.x][y.y] = i;
            q.push(y);
          }
        }
      }
      for (point x = t; x != s; x = x.side(map[x.x][x.y] ^ 2)) {
        v.push_back(map[x.x][x.y]);
      }
      std::reverse(v.begin(), v.end());
    }
    
    bool move(point s, point t, std::stack<int>& st) {  // 在靠近传送门时使用
      static std::vector<int> v;
      v.clear();
      bfs(s, t, v);
      for (int i : v)
        if (!walk(i, st)) return false;
      return true;
    }
    
    // 尽可能快地向墙边移动
    bool make_sure(point x, int last) {
      if (a[x.x][x.y] == Path) return wall_follower(x);
      for (int i = 0; i < 4; i++)
        if ((x.check(i) == Path || x.check(i) == Space) && i != (last ^ 2)) {
          if (!walk(i)) return false;
          bool ret = make_sure(x.side(i), i);
          walk(i ^ 2);
          return ret;
        }
      return false;
    }
    
    void find_gate() {
      int cnt = 0;
      std::stack<int> st;
      for (int i = 0; i < n; i++)
        for (int j = 0; j < m; j++)
          if (cnt == k * 2 && a[i][j] == Unknown)
            a[i][j] = Space;
          else if (a[i][j] == Unknown) {
            bool ok = true;
            if (!move(start, point(i - 1, j), st))
              ok = false;
            else if (!walk(1, st))
              ok = false;
            else if (!walk(2, st))
              ok = false;
            else if (!make_sure(point(i, j - 1), -1))
              ok = false;
            if (!ok) {
              vis[cnt++] = std::make_pair(point(i, j), false);
              a[i][j] = Gate;
              for (int k = 0; k < 8; k++) {
                point y = point(i, j).side(k);
                if (point(i, j).check(k) == Unknown) a[y.x][y.y] = Space;
              }
            } else
              a[i][j] = Space;
            undo(st);
          }
    }
    
    void make_gate_pair() {
      int cnt = 0;
      std::stack<int> st;
      for (int i = 0; i < k * 2; i++)
        if (!vis[i].second)
          for (int j = 0; !vis[i].second && j < k * 2; j++)
            if (j != i && !vis[j].second) {
              bool ok = true;
              if (!move(start, vis[i].first.side(2), st))
                ok = false;
              else if (!walk(0, st))
                ok = false;
              else if (!make_sure(vis[j].first.side(0), -1))
                ok = false;
              if (ok) {
                ans[cnt++] = std::make_pair(vis[i].first, vis[j].first);
                vis[i].second = vis[j].second = true;
              }
              undo(st);
            }
    }
    
    int main() {
      while (read()) {
        init();
        find_gate();
        make_gate_pair();
        answer();
      }
      return 0;
    }
    ```

## 习题

-   [刘汝佳的交互题专场比赛 Rujia Liu's Present 7 质量非常高，推荐一做．](https://onlinejudge.org/contests/328-9976a2e2/)
-   [P5473\[NOI2019\]I 君的探险](https://www.luogu.com.cn/problem/P5473)
-   [P5208\[WC2019\]I 君的商店](https://www.luogu.com.cn/problem/P5208)

## 参考资料与拓展阅读

-   [用 Linux 管道实现 online judge 的交互题功能](https://www.cnblogs.com/tsreaper/p/pipe-interactive.html)


## contest/io.md

author: Marcythm, YZircon, Chaigidel, Tiger3018, voidge, H-J-Granger, ouuan, Enter-tainer, lcfsih, Xeonacid, Ir1d

本文将介绍如何优化基于流的 I/O 与 C 风格的 I/O．

???+ note "注意"
    基于流的 I/O 与 C 风格的 I/O 的实际速度会随环境的不同（如编译器，操作系统与硬件规格）发生一定的改变．如果想要进行更进一步的分析，请以实验结果为准．但需要注意实验中的变量控制，避免因多变量影响导致结论错误．

## 基于流的 I/O

对于基于流的 I/O（如 `std::cin` 与 `std::cout`），最常用的优化方法为关闭与 C 流的同步与解除输入输出流的关联．

### 关闭同步

使用 [`std::ios::sync_with_stdio(false)`](https://en.cppreference.com/w/cpp/io/ios_base/sync_with_stdio) 函数来关闭与 C 流的同步．C++ 为了兼容 C，也就是为了保证程序在同时使用了 `printf` 和 `std::cout` 时不发生混乱，因此对这两种流进行了同步．同步的 C++ 流保证是线程安全的．

这其实是 C++ 为了兼容而采取的保守措施．若开启同步，在每一次 I/O 操作时，C++ 流会立即将此操作应用于对应的 C 缓冲区中，而如果代码中并不涉及 C 风格的 I/O，这一操作便是多余的．因此可以在进行 I/O 操作之前关闭与 C 流的同步，但是在这样做之后要注意后续代码中不能同时使用 `std::cin` 和 `scanf`，也不能同时使用 `std::cout` 和 `printf`，但是可以同时使用 `std::cin` 和 `printf`，也可以同时使用 `scanf` 和 `std::cout`．

### 解除关联

使用 [`tie()`](https://en.cppreference.com/w/cpp/io/basic_ios/tie) 函数解除输入流与输出流的关联．

在默认的情况下 `std::cin` 关联的是 `&std::cout`，因此每次进行格式化输入的时候都要调用 `std::cout.flush()` 清空输出缓冲区，这样会增加 I/O 负担．可以通过 `std::cin.tie(nullptr)` 来解除关联，进一步加快执行效率．

???+ warning "注意"
    使用时不可以省略参数写做 `std::cin.tie()`，这样不会解除关联，而是返回与 `std::cin` 关联的输出流．并且也无需进行 `std::cout.tie(nullptr)`，因为默认情况下没有另一条输出流与 `std::cout` 关联．

### 代码实现

```cpp
std::ios::sync_with_stdio(false);
std::cin.tie(nullptr);
```

???+ note "注意"
    在同时进行了上述两个操作后，程序中必须手动 `flush` 才能确保每次 `std::cout` 展现的内容可以在 `std::cin` 前出现．这是因为这种情况下调用 `std::cin` 时 `std::cout` 不会自动刷新缓冲区．例如：
    
    ```cpp
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);
    std::cout << "Please input your name: "
              << std::flush;  // 或者: std::endl;
                              // 因为每次调用 std::endl 都会 flush 输出缓冲区，而 \n
                              // 则不会．
    // 若去掉 std::flush，则在输入姓名之前不会显示提示信息
    std::cin >> name;
    ```

## C 风格的 I/O

`scanf` 和 `printf` 依然有效率提升的空间，提升方法均基于整数与字符串之间的转化．

???+ note "注意"
    本页面中介绍的读入和输出优化均针对整型数据．浮点数的读入与输出优化十分复杂，读入相关优化可参考 [Bellerophon 算法](https://dl.acm.org/doi/10.1145/93542.93557)，输出相关优化可参考 [Ryū 算法](https://dl.acm.org/doi/10.1145/3192366.3192369)．

### 实现设计

???+ note "注意"
    当前的优化方法着重于进行更快的 I/O，而在数据转换过程中均采用朴素方法，并未充分利用硬件特性．现如今绝大多数 x86 架构 CPU 均支持 AVX2 指令集，可以利用 SIMD 加速整数与字符串之间的转换．标准库函数并未利用 SIMD 优化，如 libstdc++ 的 [实现](https://github.com/gcc-mirror/gcc/blob/releases/gcc-14.3.0/libstdc%2B%2B-v3/include/bits/charconv.h#L81) 为一次转化连续两位，并通过查表的方式转化为字符，因此优化数据转换过程也可能会带来收益．但在竞赛范畴，本文中提到的优化方法已足够应对绝大多数场景．

#### 读入优化

每个整数由符号和数字两部分组成，并且符号一定在数字部分之前，因此首先会读入符号部分．对于符号部分，正整数的 `+` 通常是省略的，且不会对后面数字所代表的值产生影响，而 `-` 不可省略，因此要进行判定．如果输入不包含负整数，这部分的判定可以省略．对于数字部分，仅包含 0 至 9 的数字，因此在读入不应存在于整数中的字符（通常为空格）时，就可以判定此整数已经读入结束．

在读入时，由于是从左向右读入数字，恰好可以利用秦九韶算法进行整数转换．因此整个转换过程可以结合输入进行．

在读入数字部分的过程中，需要判断读入的字符是否为十进制数字字符．可简单采用 `ch >= '0' && ch <= '9'` 条件进行判断，也可利用 [`isdigit()`](https://en.cppreference.com/w/cpp/string/byte/isdigit) 函数．

#### 输出优化

输出时需要将整数转化为字符串，一般采取朴素算法，即直接从低到高计算出整数的每一位，转化为字符后逆序输出．

### 实现细节

#### 整型溢出问题

在实现中需要注意整型溢出的问题．如输出优化中不恰当地取相反数会导致整型最小值变为相反数后超出此整型能表示的最大值，这可能导致输出错误．读入整型最小值时也可能发生类似的溢出，但这种情况下可能并不会导致读入数据错误，这是由于溢出得到的值可能与实际输入的值相等．

有符号整型溢出是未定义行为，在实现时可以借助 C 语言中负整数除法计算向零取整的性质来避免上述问题．但如果无需输入输出负数，或不可能输入输出此整型的最小值，则这一问题将不会出现．

#### 提升实现的通用性

如果程序中使用了多个类型的整型变量，那么可能需要实现多个类型不同但逻辑相同的输入输出函数．此时可以使用 C++ 中的 [`template`](https://en.cppreference.com/w/cpp/language/templates.html) 实现对于所有整数类型的输入输出优化．例如在 C++11 标准下使用

```cpp
template <typename T>
typename std::enable_if<std::is_integral<T>::value &&
                        std::is_signed<T>::value>::type
read(T &x);
```

或在 C++20 标准下使用

```cpp
template <std::signed_integral T>
void read(T &x);
```

定义函数．

为了方便阅读，后文中的实现假定仅需读入 `int` 类型的整数，这些实现已足够应对大部分题目的需要．

### 实现

主流实现仅在使用的读入输出函数上有区别，在整数转换部分逻辑均相同．下面按照各实现使用的读入输出函数进行介绍．

#### 使用 `getchar` 与 `putchar` 实现

核心代码如下．

```cpp
--8<-- "docs/contest/code/io/io_1.cpp:core"
```

#### 使用 `fread` 与 `fwrite` 实现

通过 `fread` 与 `fwrite` 可以实现更快的读入输出．其函数签名如下．

```cpp
std::size_t fread(void* buffer, std::size_t size, std::size_t count,
                  std::FILE* stream);
std::size_t fwrite(const void* buffer, std::size_t size, std::size_t count,
                   std::FILE* stream);
```

如 `fread(Buf, 1, SIZE, stdin)`，表示从标准输入中读入 `SIZE` 个大小为 1 字节的数据块到 `Buf` 中．返回值表示成功读入了多少字节的数据．

由于 `fread` 与 `fwrite` 是整段读取和写入，因此速度相较 `getchar()` 与 `putchar()` 有优势．如果缓冲区足够大，可以一次性读入整个文件．但如果缓冲区不够大，则需要多次读取以确保读取输入的所有内容．为了实现这个功能，只需要重定义一下 `getchar`．

```cpp
char buf[1 << 20], *p1, *p2;
#define gc()                                                               \
  (p1 == p2 && (p2 = (p1 = buf) + fread(buf, 1, 1 << 20, stdin), p1 == p2) \
       ? EOF                                                               \
       : *p1++)
```

输出类似于读入，先将输出内容放入一个缓冲区中，最后通过 `fwrite` 一次性将缓冲区的内容输出即可．

核心代码如下．

```cpp
--8<-- "docs/contest/code/io/io_2.cpp:core"
```

使用此方法时需要注意：

-   关闭调试开关时使用 `fread()`，`fwrite()`，退出时自动析构执行 `fwrite()`．开启调试开关时使用 `getchar()`，`putchar()`，便于调试．
-   若要进行文件读写，需在所有读写进行之前加入 `freopen()`．

#### 使用 `mmap` 实现

`mmap` 是 Linux 系统调用，可以将文件一次性地映射到内存中，类似于可以指针引用的内存区域，在一些场景下有更优的速度．其函数签名如下：

```c
void *mmap(void addr[.length], size_t length, int prot, int flags, int fd,
           off_t offset);
```

???+ warning "注意"
    `mmap` 不能在 Windows 环境下使用（例如 CodeForces 与 HDU 的评测机系统），同时也不建议在正式赛场上使用．实际上使用 `fread` 已经足够快了，且如果用 `mmap` 反复读取一小块文件，做一次内存映射并且内核处理缺页的开销会远比使用 `fread` 的开销大．

首先需获取文件描述符 `fd`，然后通过 `fstat` 获取文件大小，此后通过 `mmap` 获得文件映射到内存的指针 `*pc`．之后可以直接用 `*pc++` 替代 `getchar()` 进行文件读取．

如果需要从标准输入中读入时，可以将 `fd` 设为 `0`．**但是，对标准输入使用 mmap 是极其危险的行为，同时不能在终端输入，可以选择将文件重定向到标准输入．**

???+ note "例题：[洛谷 P10815【模板】快速读入](https://www.luogu.com.cn/problem/P10815)"
    读入 $n$ 个范围在 $[-n, n]$ 的整数，求和并输出．其中 $n \leq 10^8$．数据保证对于序列的任何前缀，这个前缀的和在 $32$ 位有符号整形的存储范围内．

参考代码如下．

```cpp
--8<-- "docs/contest/code/io/io_3.cpp"
```

## 参考

[cin.tie 与 sync\_with\_stdio 加速输入输出 - 码农场](https://www.hankcs.com/program/cpp/cin-tie-with-sync_with_stdio-acceleration-input-and-output.html)

[C++ 高速化 - Heavy Watal](https://heavywatal.github.io/cxx/speed.html)

['Re: mmap/mlock performance versus read' - MARC](https://marc.info/?l=linux-kernel&m=95496636207616&w=2)


## contest/oi.md

author: Ir1d, Planet6174, abc1763613206, StudyingFather, cjsoft, Marcythm, luoguyuntianming, ChungZH, Xeonacid, YZircon, i-Yirannn, H-J-Granger, NachtgeistW, YuzhenQin, Andycode3759, HHH2309, shigengxin123456, Re-Ori, hcx1204

## 赛事简介

**信息学奥林匹克竞赛**（英语：Olympiad in Informatics，简称：OI）是一门在中学生中广泛开展的学科竞赛，和物理、数学等竞赛性质相同．OI 考察的内容是参赛者运用算法、数据结构和数学知识，通过编写计算机程序解决实际问题的能力．

OI 竞赛种类繁多，仅中国就包括：

-   全国青少年信息学奥林匹克联赛（NOIP）
-   全国青少年信息学奥林匹克竞赛（NOI）
-   全国青少年信息学奥林匹克竞赛冬令营（WC）
-   国际信息学奥林匹克竞赛中国队选拔赛（CTSC）

国际性的 OI 竞赛包括：

-   国际信息学奥林匹克（IOI）
-   美国计算机奥林匹克竞赛（USACO）
-   日本信息学奥林匹克（JOI）
-   亚太地区信息学奥林匹克（APIO）

    ……

对于大部分选手而言，每年的新赛季从 9 月的 CSP-J/S 第一轮开始．

在中国，OI 竞赛允许使用的语言只有 C++（曾经也开放过 C 和 Pascal 语言，但都已停止支持）．其中，不同的竞赛对 C++ 的版本有不同的规定．考试题目一般为算法或者数据结构相关的内容，题目形式包括传统题（最常见的规定输入和输出到文件的题目）和非传统题（提交答案题、交互题、补全代码题……等等）．

## 赛制介绍

### OI 赛制

选手仅有一次提交机会．比赛时无法看到评测结果，评分会在赛后公布．每道题都有多个测试点，根据每道题通过的测试点的数量获得相应的分数；每个测试点还可能会有部分分，即使只有部分数据通过也能拿到分数．

???+ note "自评测工具 selfEval"
    现如今，在一些 NOI 系列赛中，提供了 selfEval 自评测工具．selfEval 内置于全国赛定制版 NOI Linux 中．自 NOI2023 正式公布并投入使用后，selfEval 陆续用于其后的 NOI 全国赛、APIO（中国区）和 NOI 冬令营等．选手可以使用 selfEval 在一组测试数据（称为预测试数据）上测试自己的程序，并得到反馈结果．选手在每场比赛中的自测次数有指定上限（NOI2024 自测次数上限为 50 次，NOI2025 自测次数上限为 30 次），而且预测试数据也是选手不可见的．由于预测试数据不同于正式测试数据，因此自测结果仅用于调试，不能被视作正式评测成绩．选手在同一题目上多次进行预测试，所使用的预测试数据是相同的．

CSP-J/S 第二轮、NOIP、省选、NOI 都是 OI 赛制．

### IOI 赛制

选手在比赛时有多次提交机会．比赛实时评测并返回结果，如果提交的结果是错误的，不会有任何惩罚．每道题都有多个测试点，根据每道题通过的测试点的数量获得相应的分数．

APIO、IOI 都是 IOI 赛制．目前国内比赛也在逐渐向 IOI 赛制靠拢．

### Codeforces (CF) 赛制

[Codeforces](https://codeforces.com) 是一个在线评测系统，会定期举办比赛．

它的比赛特点是在比赛过程中只测试一部分数据（Pretests），而在比赛结束后返回完整的所有测试点的测试结果（System Tests）．比赛时可以多次提交，允许 Hack 别人的代码（此处 Hack 的意思是提交一个测试数据，使得别人的代码无法给出正确答案）．如果想要 Hack，选手必须要锁定自己的代码（换言之，比赛时无法重新提交该题）．Hack 时不允许将选手程序拷贝到本地进行测试，源代码会被转换成图片．

Codeforces 同时提供另外一种赛制，称作扩展 ICPC（Extended ICPC 或 ICPC+）．在这一赛制中，在比赛过程中会测试全部数据，但比赛结束以后会有 12 小时的全网 Hack 时间．Hack 时允许将选手程序拷贝到本地进行测试．

## 主要比赛

### CSP-J/S

**CSP-J/S**（英文：Certified Software Professional Junior/Senior）是 NOIP 在 2019 年被取消之后，CCF 开设的非专业级软件能力认证测试，在 2025 年以前面向全年龄段，[后改为 12 周岁以上](https://www.noi.cn/xw/2025-02-13/837984.shtml)．

CSP-J/S 分为入门级（Junior，简写为 CSP-J）与提高级（Senior，简写为 CSP-S）两组，赛程分为第一轮（一般在每年 9 月）和第二轮（一般在每年 10 月）两场．第一轮为笔试，考察计算机理论和操作常识和基本的算法与数学知识；第二轮为上机考试，入门组与提高组都为 4 题，其中入门组考试时间 3.5 个小时，提高组 4 个小时（CSP-S 2019 除外，该场比赛使用旧 NOIP 提高组赛制，赛程分为两天，一天 3 题 3.5 小时）．第一轮面向社会全体 12 周岁以上学生报名，经过一定的排名筛选后成绩优秀者有机会参加第二轮．

报名参加第一/二轮、第二轮后进行题目申诉等都需要向 CCF 缴费．

两轮测试都会以省为单位按照排名对选手成绩进行评级认证，分为一、二、三等．

### NOIP

**NOIP**（英语：National Olympiad in Informatics in Provinces，中文：全国青少年信息学奥林匹克联赛）是中华人民共和国组织的、面向中国（含港澳）中学生的信息学竞赛．

2018 年及以前的旧赛制：NOIP 按参赛对象分为普及组和提高组，2018 年于上海试点入门组；按阶段分为初赛和复赛两个阶段．初赛会考察一些计算机基础知识和算法基础，复赛为上机考试．时间上一般是 11 月的第二个周末，周六上午提高组一试 8:30-12:00（3.5 小时，共 3 题），下午 14:30-18:00 普及组（3.5 小时，共 4 题），周日上午提高组二试 8:30-12:00（3.5 小时，共 3 题）．全国使用同一套试卷，但是评奖规则按照省内情况由 CCF（中国计算机学会）统一指定，并于赛后在 [NOI 官方网站](http://www.noi.cn) 上公布．各省的一等奖分数线略有不同．

NOIP 于 2019 年 8 月 16 日 [被 CCF 暂停](http://www.noi.cn/xw/2019-08-16/715365.shtml)，于 2020 年 1 月 21 日 [被宣布恢复](http://www.noi.cn/xw/2020-01-21/715520.shtml)．2020 年起的 NOIP 赛制与以往有所不同，具体如下：

-   取消初赛，由 CSP-J/S 第一轮替代；
-   取消普及组，由 CSP-J 替代，此后 NOIP 仅有一个组别，面向提高组水平选手；
-   赛程由以往的两天共 6 题、每天 3.5 个小时，缩减为一天 4 题、共 4.5 个小时．
-   选手需要在 CSP-S 第二轮中取得一定名次才能获得 NOIP 参赛资格，具体名额各省有所差异．NOIP 省级参赛资格由该省在去年赛季中的参赛人数和成绩等有关．

报名参加 NOIP 和进行题目申诉不需要额外缴费．

NOIP 以省为单位排名评奖．截至 2019 年，大部分高校的选手获得提高组省一等奖可以得到自主招生资格．

> 2020 年 1 月，中华人民共和国教育部发布 [关于在部分高校开展基础学科招生改革试点工作的意见](http://www.moe.gov.cn/srcsite/A15/moe_776/s3258/202001/t20200115_415589.html)．意见指出，2020 年起，不再组织开展高校自主招生工作，并在部分一流大学建设高校开展基础学科招生改革试点（强基计划）．

### 省队选拔赛

**省队选拔赛**（简称：省选）用于选拔各省参加全国赛的代表队，一般举行于每年的 1\~4 月．赛程上一般分为两天，每天 3 题 4.5 小时．

省选题目由各个省自行决定，目前的趋势是很多省份选择联合命题．

各个省队的名额有复杂的计算公式，一般和之前的成绩和参赛人数有关．通常来讲，NOIP 分数需要在省选的指标中占一定比例．根据规则，初中选手只能被选拔为 E 类选手，不能参加 A、B 类选拔．A 类选手有 5 人（[至少 1 女](https://www.noi.cn/xw/2024-08-26/829152.shtml)），其他选手根据给定名额和所得分数依次进入 B 队．一个学校参加 NOI 的名额不超过本省 A、B 名额总数的三分之一（四舍五入），得分最高且入选 A 队的女选手不占该比例（简称 1/3 限制或 1/3 淘汰，详见 [CCF 官方说明](https://www.noi.cn/xw/2022-12-14/781364.shtml)）．

自 2020 年起，NOI 省队选拔由 CCF 统一命题和评测，有能力命题的省可自行命题，但选拔方式需得到 CCF 的批准．自 2024 年起，NOI 省队选拔恢复各省自主命题，有需求的省份可组织联考或使用他省试题，但具体方案需要得到 CCF 的批准．

### NOI

**NOI**（英文：National Olympiad in Informatics，中文：全国信息学奥林匹克竞赛）是国内包括港澳在内的省级代表队最高水平的大赛．

NOI 一般在七月份举行，选手分为正式选手与夏令营选手两类．正式选手又分为三类，其中 A、B 类为省队正式选手，C 类选手为邀请赛选手．A、B 类对应省队的 A、B 类选手（其中 A 类在计算成绩时会有 5 分加分）；C 类名义上是学校对 CCF 做出突出贡献后的奖励名额．夏令营选手分为 D、E 类，分别对应以非正式选手身份参赛的高中组与初中组选手．夏令营选手如果成绩超过分数线的话，只有成绩证明而没有奖牌（同等分数含金量要低一些）．排名前 50 的正式选手组成国家集训队，获得保送资格．

在国际平台上，为了与其他同样称作 NOI 的比赛区分，有时会被称作 CNOI．

### CTT

**CTT**（英文：China Team Training，中文：国际信息学奥林匹克国家集训队培训）是每年冬天为 IOI 国家集训队选手举办的集训与选拔活动，由 3-4 场测试组成．除国家集训队外，部分在当年 NOI 中取得优异成绩的选手也可以「精英集训」的名义参加 CTT．

CTT 与平时作业等其他流程共同组成了国家队选拔的第一阶段．自 2021 年起，在第一阶段排名前 30 的选手将成为国家候选队，进入第二阶段的选拔（WC）．

### WC

**WC**（英文：Winter Camp，中文：全国青少年信息学奥林匹克竞赛冬令营）是每年冬天在当年 NOI 举办地进行的一项活动．虽然该活动主要用于集训队培训与国家队选拔，但是前一年 NOIP 与 CSP-S 第二轮取得较好成绩的选手也可作为非正式营员参加．

WC 的内容包括若干天的培训和测试，测试成绩将和先前阶段的成绩汇总，算出集训队选手的综合排名．在 2020 年前，测试仅有一场，且集训队与非正式营员的测试题目相同，集训队综合成绩前 15 的选手将成为国家候选队，参与最后阶段的选拔（CTS 等）；而自 2021 年起，随着 CTS 的国家队选拔功能并入到 WC 中，国家候选队的测试变为两场，而非正式营员的测试仍为一场，且非正式营员的测试题目和候选队测试题目有部分重合．候选队中综合排名前 6 的选手将进入到最终的面试，并选出 4 名正式选手和 2 名替补选手参与当年的 IOI 比赛．

### APIO

**APIO**（英文：Asia-Pacific Informatics Olympiad，中文：亚太地区信息学奥林匹克竞赛）是一个面向亚太地区在校中学生的信息学学科竞赛．CCF 每年会在五月初举办中国赛区镜像赛．在比赛日前后会有培训活动．

APIO 参赛选手可分为 A 类和 B 类，A 类选手中的前六名（含并列）可参与 APIO 的国际奖项评选；而 B 类选手只能参与中国赛区的奖项评选．

### CTS

**CTS**（旧称：CTSC, 英文：China Team Selection Competition，中文：国际信息学奥林匹克竞赛中国队选拔赛）用来从国家候选队（15 人）中选拔国家队（6 人）准备参加当年夏天的 IOI 比赛，其中正式选手 4 人，替补选手 2 人．与 WC 一样，前一年 NOIP 取得较好成绩的选手也可以参加（不参与选拔）．

APIO 和 CTS 都以省为单位报名，一般按照 NOIP 的成绩排序来确定参加 APIO 和 CTS 的人员（二者一般时间上非常接近）．

2020 年的 CTS 因为疫情而停办，当年的国家集训队通过 NOI 选出；2021 年起，CTS 的选拔流程被 WC 取代．

### IOI

**IOI**（英文：International Olympiad in Informatics，中文：国际信息学奥林匹克竞赛）是一年一度的面向全球中学生的信息学科竞赛．每个国家有四人参赛，比赛一般会有直播．IOI 赛制中每个题目会有 Subtask（子任务），每个子任务对应一定的分数．

### 学科营

#### 北京大学（PKU）

-   北京大学信息学冬季体验营（PKUWC）：在冬令营前后举行．
-   北京大学信息学体验营（PKUSC）：一般在六月份在校内举行．由于在学校机房比赛，机房环境是 Windows，比赛系统是 OpenJudge．
-   北京大学中学生暑期课堂（信息学）：在暑假举行，面向高二年级理科学生．

#### 清华大学（THU）

-   计算机系 "大中衔接" 冬季研讨与教学活动：相当于信息学冬令营，有时也会用英文简写为 THUWC．一般共两天，上午为竞赛（第一天是标准 OI 竞赛，第二天为清华独创的 "工程题" 竞赛），下午为课程培训．

## 其他国家和地区的 OI 竞赛

### 美国：USACO

官网地址：<http://www.usaco.org/>

USACO 或许是国内选手最熟悉的外国 OI 竞赛（可能也是中文题解最多的外国 OI 竞赛）．

每年冬季到初春，USACO 会每月举办一场网络赛．一场比赛持续 3\~5 个小时．

根据官网的介绍，USACO 的比赛分成这 4 档难度（2015\~2016 学年之前为 3 档）：

-   铜牌组，适合编程初学者，尤其是只学了最最基础的算法（如：排序，二分查找）的学生；
-   银牌组，适合开始学习基本的算法技巧（如：递归，搜索，贪心算法）和基础数据结构的学生；
-   金牌组，学生会遇到更复杂的算法（如：最短路径，DP）和更高级的数据结构；
-   铂金组，适合有着扎实的算法设计能力的选手，铂金组可以帮助他们以复杂且更开放的问题来挑战自我．

在国内，目前 USACO 题目最齐全的 OJ 平台是洛谷．

### 波兰：POI

官网地址：<https://oi.edu.pl/>

官方提交地址：<https://szkopul.edu.pl/p/default/problemset/>

POI 是不少省选选手最常刷的外国 OI 比赛．

根据 [POI 官网](https://oi.edu.pl/l/42/) 的描述，POI 的流程如下：

-   第一轮：六题（第 31 届及以前为五题），网络赛；
-   第二轮：包含一场练习赛，和两场正式赛，其中练习赛一题，正式赛每场两题；
-   第三轮：包含一场练习赛，和两场正式赛，其中练习赛一题，正式赛每场三题．

在部分年份，曾举办名为 ONTAK 的比赛，其正式名称为 POI 训练营，对标国内的国家集训队集训赛（CTT）．

另外，波兰国内还举办名为 PA 的公开比赛，大意为「算法大战」，其官网地址是：<https://potyczki.mimuw.edu.pl/>．

目前在国内 OJ 中，POI 题目最全的是 BZOJ．

### 克罗地亚：COCI

官网地址（英文）：<http://www.hsin.hr/coci/>

官网地址（克罗地亚语）：<http://www.hsin.hr/honi/>

难度跨度很大的比赛，大约是从普及 - 到省选 -．

以往 COCI 所有的题目均提供题目、数据、题解和标程．2017 年底起，COCI 的题解和标程停止了更新．2019-2020 赛季重新开始更新题解和标程．

洛谷、BZOJ 和 LibreOJ 都有少量的 COCI 题目．

### 日本：JOI

官网地址：<https://www.ioi-jp.org/>

JOI（日文：日本情報オリンピック，中文：日本信息学奥赛）所有的题目都提供题目、数据、题解和标程．近两年的 JOI 决赛和春训营提供了英语题面，但并没有英语题解．历年的 JOI Open 都提供了英语版题面和题解．

JOI 的流程：

-   预赛（予選）
-   决赛（本選/JOI Final）
-   春训营（春季トレーニング合宿/JOI Spring Camp/JOISC）
-   公开赛（通信教育/JOI Open Contest）

预赛难度较低，自 2019/2020 赛季起，预赛分为多轮．JOI Final 的难度从提高 - 到 提高 + 左右．JOISC 和 JOI Open 的题目的难度从提高到 NOI - 不等．

绝大部分 JOI 题可以前往 [AtCoder](https://atcoder.jp/) 提交．你可以在 JOI 官网或者 AtCoder 上找到更多的 JOI 题（日文题面）．

目前 LibreOJ 和 BZOJ 有近些年的 JOI Final、JOISC 和 JOI Open 的题目．

### 俄罗斯：ROI

官网地址：<http://neerc.ifmo.ru/school/archive/index.html>

在线提交地址：<https://contest.yandex.ru/roiarchive/> 和 Codeforces（部分）．

ROI（俄文：олимпиадная информатика，中文：俄罗斯信息学奥赛）是俄罗斯的信息学竞赛．

流程：

-   市级比赛（Municipal Stage/Муниципальный этап）
-   州级比赛（Regional Stage/Региональный этап）
-   决赛（Final Stage/Заключительный этап）

目前 LibreOJ 有近几年的 ROI 决赛题的译文．

除此之外，俄罗斯较大型的、面向中学生的比赛还有：

-   信息学网络奥赛（俄文：Интернет-олимпиады по информатике）
    -   官网地址：<http://neerc.ifmo.ru/school/io/index.html>
    -   该比赛由 ROI 出题人举办．
-   全国中学生团队信息学竞赛（俄文：Всероссийской командной олимпиады школьников）
    -   官网地址：<http://neerc.ifmo.ru/school/russia-team/index.html>
    -   该比赛的预选赛 Moscow Team Olympiad 可以在 Codeforces 上提交．
-   Innopolis Open
    -   官网地址 <https://olymp.innopolis.ru/en/ooui/information/>
-   中学生编程公开赛（Открытая олимпиада школьников по программированию）
    -   官网地址：<https://olympiads.ru/zaoch/>
    -   官网称该比赛对标 ROI．

### 加拿大：CCC & CCO

CCC（英文：Canadian Computing Competition），CCO（英文：Canadian Computing Olympiad），可在其 [官网](https://cemc.math.uwaterloo.ca/contests/past_contests.html#ccc) 查询历届的信息和试题等．

在 DMOJ 上可以提交 [CCC](https://dmoj.ca/problems/?category=4) 和 [CCO](https://dmoj.ca/problems/?category=24)，该 OJ 上还有 CCC 题解．

CCC Junior/Senior 贴近 NOIP 普及组/提高组难度．CCO 想要拿到金牌可能得有 NOI 银牌的水平．

### 新加坡：NOI SG

官网地址：<https://noisg.comp.nus.edu.sg/noi/>

全称 Singapore National Olympiad in Informatics，在新加坡国内语境且不引起歧义的情况下也作 NOI．赛制上分为 Online Qualification Contest（在线资格赛）和 Final Contest（全国决赛）．在线资格赛以学校为单位报名参加，选手在本校参赛，通过网络进行远程提交．资格赛成绩只在校内排名，前 5 名且非零分选手有资格作为校代表队参加全国决赛．

目前国内 OJ 对于 NOI SG 的题目收录比较匮乏，可以在 [官方的 GitHub 账号](https://github.com/noisg) 上找到历年题面、测试数据和官方标准程序．

### 台湾地区：資訊奧林匹亞競賽

台湾地区把 OI 中的 informatics 翻译成「資訊」而非大陆通用的翻译「信息」．

台湾地区的选手如果想参加 IOI，需要经过这几轮比赛：

-   區域資訊學科能力競賽
-   全國資訊學科能力競賽
-   資訊研習營（TOI）

### 其他国家

-   澳大利亚：AIO：<https://orac.amt.edu.au/hub/aio/>

    -   难度与 NOI 类似．

-   英国：British Informatics Olympiad：<https://www.olympiad.org.uk/>

    -   难度太低．

-   捷克：Matematická olympiáda–kategorie P：<http://mo.mff.cuni.cz/p/archiv.html>

-   罗马尼亚：Olimpiada Nationala de Informatica：<http://olimpiada.info/>
    -   题面、测试数据、题解请在含有 Subiecte 字样的标签页中寻找．

## 其它国际 OI 竞赛

### BalticOI

**BalticOI** 面向的是波罗的海周边各国．BalticOI 2018 的参赛国有立陶宛、波兰、爱沙尼亚、芬兰等 9 国．题目难度大．

除了 2017 年，BalticOI 每年都公开题面、测试数据和题解．BalticOI 没有一个固定的官网，每年的主办方都会新建一个网站．历年的官网地址见 [帖子](https://loj.ac/article/416)．

目前 LibreOJ 有近十年的 BalticOI 题．

### BalkanOI

**BalkanOI** 面向巴尔干地区周边各国．BalkanOI 2018 的参赛国有罗马尼亚、希腊、保加利亚、塞尔维亚等 12 国．题目难度大．

BalkanOI 只有某几年公开题面、测试数据和题解，官网地址见 [帖子](https://loj.ac/article/416)．

### CEOI

CEOI 2018 的参赛国与上面两个比赛有部分重叠，包括波兰、罗马尼亚、格鲁吉亚、克罗地亚等国．题目难度大．

CEOI 每年都公开题面、测试数据和题解，官网地址见 [帖子](https://loj.ac/article/416)．

### eJOI

**eJOI** 全名 European Junior Olympiad in Informatics．参赛国包含俄罗斯、亚美尼亚、保加利亚、波兰等国．题目难度较大．

eJOI 每年都公开题面、测试数据和题解，官网地址见 [帖子](https://loj.ac/article/416)．

### NOI

???+ warning "Warning"
    此处介绍的不是「全国信息学奥林匹克竞赛」．

**NOI** 全名 Nordic Olympiads in Informatics．

官网地址：<http://nordic.progolymp.se>

近两年才开始举办的比赛，面向北欧各国．

## 参考资料

-   [ICPC/CCPC 赛事与赛制](./icpc.md)
-   [「翻译组」一些大洲级 OI 比赛的地址](https://loj.ac/article/416)


## contest/problems.md

author: StudyingFather, NachtgeistW, countercurrent-time, Ir1d, H-J-Granger, Chrogeek, sshwy, Suyun514, hsfzLZH1, CBW2007, Xeonacid, kawa-yoiko, Konano

在算法竞赛中，有多种多样的问题类型．

## 传统题

**传统题** 是目前算法竞赛中较为常见的题型．

选手需要提交源代码，评测系统会使用事先准备好一些输入数据和相应的输出数据作为测试点[^note1]，将选手提交的源代码编译后[^note2]，让选手程序读入输入数据，通过将选手输出与事先准备好的输出比较，来判断选手程序是否正确．这种评测方式被称之为 **黑盒评测**[^note3]．

对于一个测试点，往往还会设置时间限制和空间限制．

时间限制，指的是程序运行时间的限制[^note4]．选手程序在一个测试点上的运行时间不能超过给定的时间限制．

空间限制，指的是程序使用的内存量的限制．选手程序在运行时占用的最大空间不能超过给定的空间限制．

在程序正常运行结束后，选手的输出会和测试点输出进行比对．这种比对一般采用过滤文末换行和行末空格之后，进行全文比对的方式．对于某些特殊的题目，会使用 [Special Judge](../tools/special-judge.md) 来进行比对．

这一过程结束后，评测系统会根据程序的运行状态，给出不同的 **评测结果**[^note5]：

-   Accepted（AC）：选手程序被接受．
-   Compile Error（CE）：选手程序无法正常编译．
-   Wrong Answer（WA）：选手程序正常结束，但是选手程序的输出与测试点输出不符．
-   Presentation Error（PE）：选手程序正常结束，但是格式不符合要求[^note6]．
-   Runtime Error（RE）：选手程序非正常结束（选手程序结束时的返回值不为零）．
-   Time Limit Exceeded（TLE）：选手程序运行的时间超过了给定的时间限制．
-   Memory Limit Exceeded（MLE）：选手程序占用的最大空间超过了给定的空间限制．
-   Output Limit Exceeded（OLE）：选手程序输出的内容的量超过了最大限制．

在 ICPC 赛事中，你的程序需要在一道题目的所有测试点上都取得 AC 状态，才能视为通过相应的题目．在 OI 赛事中，在一个测试点中取得 AC 状态，即可拿到该测试点的分数[^note7]．

## 提交答案题

**提交答案题** 是直接提交答案的题目．该种题目一般会给出输入文件，要求提交包含有 `XXX1.out`、`XXX2.out`、`XXX3.out`…`XXXn.out` 的压缩包、文件夹或纯文件．

提交答案后，评测系统会比较答案文件与标准答案，根据选手答案的优劣情况和任务完成度，给予一定的分数．

因为提交答案题不需要运行源程序，故提交答案题不存在时间和空间限制．

做这种题目一般有两种方法：

-   手玩．这种方法简单粗暴，但是遇到较大的数据就没辙了．
-   编写一个程序来获得答案文件．

## 交互题

**交互题** 是需要选手程序与测评程序交互来完成任务的题目．一类常见的情形是，选手程序向测评程序发出询问，并得到其反馈．测评程序可能对选手的询问作出限制，或调整应答策略来尽可能增加询问次数，这也给题目带来了更多变化．

更详细的交互题讲解可以看 [交互题](./interaction.md)．

交互方式主要有如下两种．虽然技术上有不小的差异，但在考察算法的本质上它们并没有实际区别．

### STDIO 交互

STDIO 交互（标准 I/O 交互）是 Codeforces、AtCoder 等在线平台的交互手段，也是 ICPC 系列赛事中的标准．Codeforces 提供了一个更加简要的 [说明（英文）](https://codeforces.com/blog/entry/45307)．

???+ note "例题 [LOJ #559.「LibreOJ Round #9」ZQC 的迷宫](https://loj.ac/problem/559)"
    请注意最下方添加内容．
    
    本题是一道交互题．
    
    位于 $n \times m$ 个方格组成的黑暗迷宫的你，需要走到这个迷宫的终点，以完成迷宫挑战．
    
    最开始，你位于迷宫的起点即 $(1,1)$ 处，且面向右侧，终点位于 $(n,m)$ 处．迷宫中任意两个方格之间均连通，且仅有唯一的一条路径，两个相邻（即上、下、左、右四连通）方格间长度为一个单位长度．两个相邻方格之间可能会有墙壁，墙壁厚度相对于方格而言非常小，粗略不计．迷宫的边界均有墙壁，且每一堵墙壁均与边界连通．迷宫是完全黑暗的，这意味着，你无法得到除 $(n,m)$ 以外的任何信息．
    
    为了在黑暗条件下尽量不迷路，每次前进时你只能从当前格子出发，沿着左侧或右侧墙壁，左手或右手扶着墙壁前进，并且使扶着墙壁的手移动距离恰好为一个单位长度．需要注意的是，若左侧或右侧墙壁不存在，则沿该侧方向无法前进．
    
    在黑暗中过久的你会感到恐惧，因此你需要在你尽早走出迷宫．如果你没有在限定步数内走出迷宫，挑战将会失败．

对于这类题目，选手只需像往常一样将询问写到标准输出，**刷新输出缓冲** 后从标准输入读取结果．选手程序刷新输出缓冲后，通过管道连接它的测评程序（称为交互器）才能立刻接收到这些数据．在 C/C++ 中，`fflush(stdout)` 和 `std::cout << std::flush` 可以实现这个操作（使用 `std::cout << std::endl` 换行时也会自动刷新缓冲区，但是 `std::cout << '\n'` 不会）；Pascal 则是 `flush(output)`．

### Grader 交互

Grader 交互方式常见于 IOI、APIO 等国际 OI 赛事（特别是 CMS 平台的竞赛）．

???+ note "例题 [UOJ #206.【APIO2016】Gap](https://uoj.ac/problem/206)"
    有 $N$ 个严格递增的非负整数 $a_1,a_2,\cdots,a_N (0\leq a_1<a2<\cdots<a_N\leq 10^{18})$．你需要找出 $a_{i+1}−a_i (0\leq i\leq N−1)$ 里的最大的值．
    
    你的程序不能直接读入这个整数序列，但是你可以通过给定的函数来查询该序列的信息．关于查询函数的细节，请根据你所使用的语言，参考下面的实现细节部分．
    
    你需要实现一个函数，该函数返回 $a_{i+1}−a_i (0\leq i\leq N−1)$ 中的最大值．

对于这类题目，选手只需编写一个特定的函数完成某项任务，它通过调用给定的若干辅助函数来进行交互．为了便于选手在本地测试，题目会下发一个头文件与一个参考测评程序 `grader.cpp`（对于 Pascal 语言是一个库 `graderlib`），选手将自己的程序与 `grader.cpp` 一同编译方可得到可执行文件．

```sh
g++ grader.cpp my_solution.cpp -o my_solution -Wall -O2
./my_solution   # 执行程序
```

编译得到的程序表现与传统题程序类似．它会打开固定的文件，以固定的格式读取数据，调用选手编写的函数，并将结果和若干信息（例如询问的次数、答案正确性）显示在标准输出上．

实际测评时，选手的程序会与一个不同的 `grader.cpp` 编译．这个 `grader.cpp` 将以类似的方式调用选手编写的函数，并记录其得分．一般来说，这个版本的 `grader.cpp` 所有全局符号都会设为 `static`，也即不能通过冲突命名的方式破解它，但是任何尝试突破 grader 限制的行为都会被判失格 (disqualification)．

### 差别

STDIO 交互的一个明显优势在于它可以支持任何编程语言，但是输入输出的耗时容易成为问题设计的瓶颈，导致有时无法区分程序的时间效率差别；Grader 交互则恰好相反，由于函数调用的开销不大，常常可以允许 $10^6$ 数量级的询问次数，但是语言的限制是其短板．

如果自己设计题目或举办比赛，需要对二者认真权衡和比较．

## 通信题

**通信题** 是需要两个选手程序进行通信，合作完成某项任务的题目．第一个程序接收问题的输入，并产生某些输出；第二个程序的输入会与第一个的输出相关（有时是原封不动地作为一个参数，有时会由评测端处理得到），它需要产生问题的解．

通信题的例子有：[UOJ #178. 新年的贺电](https://uoj.ac/problem/178)，[#454.【UER #8】打雪仗](https://uoj.ac/problem/454) 等．

本地测试的方法由于题目设定的不同而多种多样，常用的形式如：

-   手工输入
-   编写一个辅助程序，转换第一个程序的输出到第二个程序的输入
-   用双向管道将两个程序的标准输入/输出连接起来

由于评测平台对于通信题的支持有限，因而目前为止，通信题只常见于 IOI 系列赛和 UOJ 等少数在线平台举办的比赛．它仍是一个有待探索的领域．

## 函数补全题

**函数补全题** 是需要选手补全程序的题目．可以理解为在一道交互题中，题目给定了选手代码，要求编写辅助函数．

通常有以下几种形式：

-   给定一个程序，并告知要求补全的代码块将被嵌入在哪里．
-   不给出程序，而将输入信息作为待提交函数的参数．

这种题在 [LeetCode](https://leetcode.com/) 和 [PTA - 拼题 A](https://pintia.cn/problem-sets) 上比较多见．

## 其他类型

???+ note "例题 [Quine](https://loj.ac/problem/4)"
    写一个程序，使其能输出自己的源代码．
    
    代码中必须至少包含十个可见字符．

题目很经典，但是在绝大多数 OJ 上都很难实现．

??? note "参考代码"
    **注意**：源代码不包含下方第一行（即 `// clang-format off`）．
    
    ```cpp
    // clang-format off
    #include<cstdio>
    
    char *s={"#include<cstdio>%cchar *s={%c%s%c};%cint main(){printf(s,10,34,s,34,10);return 0;}"};
    
    int main(){printf(s,10,34,s,34,10);return 0;}
    ```

## 参考资料与注释

[^note1]: 因为技术上和资源上的限制，一道题目的测试点大多数情况下不能覆盖满足数据范围的全部数据．

[^note2]: 对于 Python 这样的解释性语言则直接由解释器解释运行程序．

[^note3]: 事实上评测系统的实现远比这个复杂，这里只是大概介绍了评测系统的评测过程．

[^note4]: 准确来说，一般是程序的用户态时间．

[^note5]: 这里的评测结果大多也适用于其他类型题目．

[^note6]: 大多数评测系统会将 PE 状态归到 WA 状态当中．

[^note7]: 一些测试点可能会有部分分，选手在完成一个测试点的部分任务，或者选手的输出正确但不够优的情况下，可以获得一定比例的分数．


## contest/problemsetting.md

author: ouuan, Henry-ZHR, StudyingFather, ChungZH, xyf007, Cryflmind, oierlinch, xk2013awa

## 出题前的准备

### 具备一定的水平

一方面，一个人自己出题，很难出出难度大于自身水平的题目，一定的 OI 水平有助于想到更加优质的 idea 并想出优秀的做法；另一方面，OI 水平在一定程度上代表着 OI 资历，见识过更多的题目的选手也会对「好题」拥有自己的见解．

### 抱有认真负责的态度

出题是给别人做的，比起展示自己，更多是为了是服务他人．算法竞赛是选手之间的竞赛，而不是出题人与做题人之间的较量．因此，出题不应以考倒选手为目标（当然，适当的防 AK 与良好的区分度也是非常重要的），而应当让选手能在比赛中有所收获．花费足够的时间精力去学习如何出题并认真负责地出题非常重要．

### 做好耗费大量时间的准备

如果想要认真地出题，就必然要花费大量的时间．如果不做好心理准备，可能导致比赛准备匆忙，质量不过关，也可能在事后由于没有将时间花费在学习上而懊悔．但出题也可以带来很多美好的回忆，如果真的对出题抱有兴趣，并做好了充分的心理准备，出题带来的收获也能够弥补那些花费的时间．

### 认真阅读本文的内容

本文从如何出题、如何把题出好两个方面对整个出题流程进行了介绍．对于想要出题的人来说，认真阅读本文一定能够受益匪浅．

## 题目内容

出一道题，idea，即题目本质的内容，是题目的灵魂，也是出题的第一步．

### idea 的来源

1.  受到已有题目的启发（但不能照搬或无意义地加强，如：序列题目搬到仙人掌上）．
2.  受到学过的知识点的启发（但不能毫无联系地拼凑知识点）．
3.  从生活/游戏中受到启发（但注意不要把游戏出成大模拟）．
4.  不知道为什么，就是想到了一道题．

### 什么样的 idea 是不好的

#### 关于原题

原题大致可分为完全一致、几乎一致和做法一致三种．

-   完全一致：使用一题的 AC 代码可以 AC 另一题．
-   几乎一致：由一题的 AC 代码改动至另一题的 AC 代码可以由一个不会该题的人完成．
-   做法一致：核心思路、做法一致，但代码实现上、不那么关键的细节上有差异．

这三种原题自下而上为包含关系．

以下情况不应出现：

1.  在明知有「几乎一致」的原题的情况下出原题．
2.  由于未使用搜索引擎查找导致自己不清楚有原题，从而出了「几乎一致」的原题．
3.  在「做法一致」的原题广为人知（如：NOIP、NOI 原题）时出原题．
4.  在带有选拔性的考试的非送分题中出现「做法一致」的原题．

以下情况最好不要出现：

1.  在明知有至少为「做法一致」的原题的情况下出原题．
2.  由于未使用搜索引擎查找导致自己不清楚有原题，从而出了「做法一致」的原题．
3.  在任何情况下出「几乎一致」的原题．

可以放宽要求的例外情况：

1.  校内模拟赛．
2.  以专题训练为目的的模拟赛．
3.  难度较低的比赛，或是定位为送分题的题目．

#### 关于毒瘤题

「毒瘤题」是一个非常模糊而主观的观念，在这只是引用一些前人关于此的探讨，加以自己的一些理解．这个话题是非常开放的，欢迎大家来发表自己的观点．

> 一道好题不应该是两道题拼在一起，一道好题会有自己的 idea——而它应该不加过多包装地突出这个 idea．
>
> 一道好题应该新颖．真正的好题，应该是能让人脑洞出新的好题的好题．
>
> ——[vfk《UOJ 精神之源流》][1]

例子：[「XR-1」柯南家族](https://www.luogu.com.cn/problem/P5346)，做法的前后两部分完全割裂，前半部分为 [「模板」树上后缀排序](https://www.luogu.com.cn/problem/P5353)，后半部分是经典树上问题．就算是随意输入树的点权，依然可以做第二部分，前后部分没有联系．

> 一类 OI 题以数学为主，无论是题目描述还是做法都是数学题的特征，并且解法中不含算法相关的知识点，这类 OI 题目统称为纯数学题．
>
> ——[王天懿《论偏题的危害》][2]

经典例子：[NOIP2017 小凯的疑惑](https://uoj.ac/problem/329)

OI 中的数学题与其它数学题的区别，也是体现 OI 本质的一个特点，是 OI 中的数学题往往重点不在答案 **是什么**，而在如何 **加快** 答案的计算．如果一道题考察的重点是「怎么算」而非「怎么快速计算」，这样的数学题一般都是不适合出在 OI 中的．

> 一部分偏题中牵涉到了大学物理的内容，导致选手在面对这些从未接触过物理知识点时变得不知所措，造成了知识上的隔膜．
>
> ——[王天懿《论偏题的危害》][2]

经典例子：[「清华集训 2015」多边形下海](https://uoj.ac/problem/159)

不止是物理，OI 题目中不应过多涉及到其它学科的知识，如果涉及应当给予详细的解释，不应使其它学科的知识作为解题的重大障碍．

> 一道好题无论难度如何，都应该具有自己的思维难度，需要选手去思考并发现一些性质．
>
> 一道好题的代码可以长，但一定不是通过强行嵌套或者增加条件而让代码变长，而是长得自然，让人感觉这个题的代码就应该是这么长．
>
> ——[王天懿《论偏题的危害》][2]

经典例子：[「SDOI2010」猪国杀](https://loj.ac/problem/2885)，[「集训队互测 2015」未来程序·改](https://uoj.ac/problem/98)

在一般的 OI 比赛中，思维难度应占主要部分．当然，如 THUWC/THUSC 的 Day 2+ 那样的工程题也有其存在的道理——毕竟体验营的目的除了考察选手的算法设计能力，还有和大学学习对接的工程代码以及文档学习能力．但在一般的 OI 比赛中，考察更多的应当还是算法设计与思维能力．

## 题面

### 使用 LaTeX 书写公式

网上有很多 LaTeX 的教程，如：

-   [LaTeX 入门](../tools/latex.md#图表)
-   [LaTeX 数学公式大全](https://www.luogu.com.cn/blog/IowaBattleship/latex-gong-shi-tai-quan)
-   [LaTeX 各种命令，符号](https://blog.csdn.net/anxiaoxi45/article/details/39449445)

使用时请注意 [LaTeX 公式的格式要求](../intro/format.md)．

### 题目背景

题目背景最好尽量简短．在题目背景较长时，应当与题目描述分开．

需要绝对避免题目背景严重影响题意的理解．

必要时，可以提供与背景结合的题目描述与简洁的题目描述两个版本．

### 题目描述

简而言之，题目描述需要 **清晰易懂**．

题面中的每个可能不被理解的定义都应得到解释，不应凭空冒出未加定义的概念．例如：在 [CF1172D Nauuo and Portals](https://codeforces.com/problemset/problem/1172/D) 中，你必须在题面中解释什么是「传送门」．

题面中涉及到的每个概念应当使用单一的词汇来描述．例如：不应一会儿说「费用」，一会儿说「代价」．

不应不加说明地使用与原义、常见义不同的词汇．例如：不应不加说明地用「路径」代指一条边．

你需要保证你的题面不会自相矛盾．例如：在 [CF1173A Nauuo and Votes](https://codeforces.com/problemset/problem/1173/A) 中，没有把 "?" 作为一种 "result"，是因为 "?" 的含义是 "there are more than one possible results"．

你需要保证你的题面不能被错误理解而自圆其说，即使这种理解是反常识、没有人会这么去想的．例如：在 [CF1172D Nauuo and Portals](https://codeforces.com/problemset/problem/1172/D) 中，之所以要繁琐地定义 "walk into" 并与 "teleport" 区分，是为了防止这种理解：通过传送门可以到另一个传送门，而到了传送门会传送，因此会反复横跳．

顺着读题目描述应当能看懂每一句话，并理解题目的任务与要求．至少在紧接着的下一段话中疑惑能够得到解释，而不是需要在若干段后才能得到解释，或者要看了输入输出格式才能明白题意，甚至需要根据样例来猜题意．例如：在 [「GuOJ Round #1」琪露诺的冰雪宴会](https://github.com/OI-wiki/problemset/blob/master/contest/online/GuOJ/OI%20Archive%20-%20GuOJ1171.pdf) 中，在输出格式才第一次出现了题目的目标「雾之湖最终能接收到的最大水量」，再加上「灵梦当然能很快算出来清理完全部小溪的总费用是多少」这句带有误解性质的话，更容易使人读错题意，这是不可取的，应当在题目描述中就对题目的目标进行说明．（在这个例子中还存在题目背景严重影响题意理解的问题．）相同的错误还出现在 [CF1423(4)N Bubblesquare Tokens](https://codeforces.com/problemset/problem/1423/N) 中，在输出格式才第一次出现了题目的目标 "friend pairs and number of tokens each of them gets on behalf of their friendship"．

### 输入输出格式

输入输出格式清晰 **完整** 即可，没有死板的要求，个人建议参照 CF 的题目来写输入输出格式，具体可以参考[CF 出题人须知][3]．

为了方便选手做题，输入输出格式中最好说明每个变量的具体含义，除非变量的意义非常长，没法一句话说清楚（这时可以说「意义见题目描述」）．

需要特别注意的是，如果输出中含有小数，请尽量使用 [SPJ](#special-judge) 来对误差的大小进行限制，而非要求「保留 x 位小数」．

「保留 x 位小数」对精度的要求可能是无限的．例如：要求保留三位小数，实际答案为 $0.0015$，此时只要有任意大小的误差导致计算出的答案小于 $0.0015$，即使计算出的答案是 $0.00149999\cdots$ 也会输出错误的答案．

如果无法使用 SPJ，请保证对精度的要求是有限的，例如：请输出答案四舍五入后保留小数点后三位的结果．令标准答案为 $ans$，数据保证对于任意满足 $\frac{|x-ans|}{\max(1,ans)}<10^{-9}$ 的 $x$，四舍五入后结果与 $ans$ 四舍五入后相同．

可以参考的一些句子：

```latex
输入的第一行包含三个正整数 $n$, $m$, $k$ ($1\le n,m\le 2\cdot 10^5$, $1\le k\le 100$) — $n$ 表示数列的长度，$m$ 表示操作个数，$k$ 的意义见题目描述．
```

```latex
输入的第二行包含 $n$ 个非负整数 $a_1,a_2,\ldots,a_n$ ($1\le a_i\le 10^9$) — 题目给出的数列．
```

```latex
接下来的 $m$ 行中的第 $i$ 行包含两个正整数 $l_i$ 和 $r_i$ ($1\le l_i\le r_i\le n$)，表示第 $i$ 次操作在区间 $[l_i,r_i]$ 上进行．
```

```latex
接下来的 $n-1$ 行，每行包含两个正整数 $u$ 和 $v$ ($1\le u,v\le n$)，表示 $u$ 和 $v$ 之间由一条边相连．

数据保证给出的边能构成一棵树．
```

```latex
输入的唯一一行包含一个由小写英文字母构成的非空字符串，其长度不超过 $10^6$．
```

```latex
输入的第二行包含一个小数点后不超过三位的实数 $x$ ($-10^6\le x\le 10^6$)，意义见题目描述．
```

```latex
输出包含一个实数，当你的输出与标准答案之间的绝对误差或相对误差小于 $10^{-6}$ 时视作正确．
```

```latex
输出的第二行包含 $n$ 个正整数，表示你构造的一组方案 — 其中第 $i$ 个数表示你打出的第 $i$ 张牌的编号．

如果有多组合法的答案，可以任意输出其中一组．
```

???+ note "在选手代码内由随机数生成器生成输入数据"
    有的题目会因为输入数据过大，为了防止读入用时过长，而要求选手在代码内通过给定的数据生成器生成数据，代替通过标准输入或文件输入来读入数据．
    
    采用这种做法需要谨慎考虑，因为它有很多缺点：
    
    -   可能引入了正解所不需要的数据随机性，或者使得构造数据变得困难
    -   可能增大了理解输入格式的难度
    -   如果随机数生成器封装的不好，可能理解数据生成器本身的使用方法就有难度
    -   如果选手没有使用出题者推荐的语言，可能需要自己写一个数据生成器
    
    采用这种做法一般是为了防止读入数据用时过长，所以一个可能的替代方案是下发一个性能足够好的 [读入、输出优化](./io.md) 模板，以尽量保证所有人的读入用时一致，这样的话即使读入用时很久也不会影响不同选手用时的差异．另一个解决方案是将题目包装成函数调用式（而非 IO 式）交互题，即使算法过程中没有交互，交互题也可以起到统一读入用时的作用，IOI 就采用了所有题目都是交互题的方案．但是，这两种方案都对选手使用的语言有限制，需要出题者手动支持每种允许选手使用的语言．
    
    回到问题的本源，还可以考虑一下过大的输入数据是否是必要的，有没有可能使用较小的输入数据达到目的，以及比正解复杂度稍劣的做法是否有卡掉的必要．

### 数据范围

按照 CF 的要求，数据范围要写在输入格式里，但在国内，数据范围往往是写在题目的最后的．

数据范围中最容易犯的错误就是不完整．输入中的每一个数、每一个字符串都应该有清晰的界定．在上文所给出的输入输出格式示例中就有一些数据范围的正确写法．

数据范围的常见遗漏：

1.  「整数」中的「整」．
2.  题面中只说了是「整数」没说是「正整数」，并且数据范围中只有上限没有下限．
3.  字符串没说字符集．
4.  实数没说小数点后位数．
5.  某些变量没有给范围．

你需要保证标程可以通过满足题面所述数据范围的 **任何一组数据**．

???+ note "关于「保证数据随机生成」"
    有的题目中会「保证数据随机生成」，很多时候这样的限制并不是最优的解决方案，因为「随机生成」对数据的限制并不明确，会给判断具体数据范围、提供 hack 数据带来困难．
    
    一般来说，「保证数据随机生成」可以换成解法所需要的数据性质．例如，随机生成一棵树往往可以换成限制树的高度．
    
    如果一定要保证数据随机生成，应当指定随机生成的具体操作．例如，生成一棵树是随机选择父亲节点还是随机生成 Prüfer 序列．
    
    需要注意的是，非确定性算法和依赖于数据随机性的算法是不同的．前者可以对于任意数据都有很高的概率得到正解，而后者是对于大部分的数据能得到正解，对于某些特定的数据则不可能得到正解．

### 样例

样例应当有一定的强度，能够查出一些简单的错误．读错题意的人应当能够通过样例发现自己读错了题意．

有多种操作的题，每种操作都应在样例中出现．

有多种输出的题（如 [CF1173A Nauuo and Votes](https://codeforces.com/problemset/problem/1173/A)），每种输出都应在样例中出现．例外：实际上不可能无解，但要求判断是否有解的题目．

### 样例解释

题目描述越复杂、越不易理解就越应当有详细的样例解释．

题目难度越简单就越应当有详细的样例解释．

详细的样例解释可以选择配上图片．

较大的样例可以没有样例解释．

为了照顾色觉障碍者，最好不要使颜色成为理解样例解释所必备的．可以用彩色图片来美化样例解释，但如果一定要用颜色传递一些必要的信息，最好不要同时出现红黄或者红绿．

## 时限、空间限制与部分分

时限与空间限制的目的是卡掉复杂度错误的做法．（当然，也是为了防止评测用时过长，如：只对交互次数有限制而对时间复杂度没有限制的交互题也有时间限制．）

因此，原则上时间限制应当选取不使错误做法通过的尽量大的值．

一般地，时限应满足以下要求：

1.  至少为 std 在最坏情况下用时的两倍．
2.  如果比赛允许使用 Java，应使 Java 能够通过．
3.  不应使错误做法通过（实在卡不掉、想放某种错解过除外）．

为了更好地在放大常数做法过的同时卡掉错解，一般可以采用同时增大数据范围和时限的方法．但要注意，有时正解（由于缓存等玄学问题）会在数据范围增大时有极大的常数增加，此时增大数据范围不一定能够增大正解与错解之间用时的差距．

在有部分分的赛制中，还可以通过设置有梯度的数据、数据范围稍小的数据来使较为优秀的错解和大常数正解不能通过，同时使其获得较高的部分分．

需要注意的是，在数据范围小于 $5\cdot 10^5$ 时，应当考虑是否能使用 [指令集](https://ouuan.github.io/post/n方过百万-暴力碾标算——指令集优化的基础使用) 通过．

一般情况下空间限制应当设置的足够大，除非空间复杂度更优的做法的确十分巧妙，值得卡掉空间复杂度大的做法．这种情况下可以考虑设置空间限制较松的部分分．值得注意的是，如果不想卡掉空间消耗较大的做法，数据结构题一般需要设置较大的空间限制．

> 一道好题应该具有它的选拔性质，具有足够的区分度．应该至少 4 档部分分，让新手可以拿到分，让高手能够展示自己的实力．
>
> ——vfk《UOJ 精神之源流》

部分分一般分为较小数据范围与特殊性质两种．

较小数据范围一般要设置多档，即使你想不到某种复杂度的做法，也可以考虑给这种复杂度一档分．一般来说，为了避免卡常，可以设置一档极限数据除以二的部分分．

「数据有梯度」最好用多档部分分替代．

特殊性质部分分的设置要依具体题目而定．理想的特殊性质部分分应当是能够引导选手思考正解的．与较小数据范围部分分不同，在你不会针对某种特殊性质的做法时，最好不要给这种特殊性质一档分．例如：[「CTS2019」随机立方体](https://loj.ac/problem/3119) 的 $k=1$ 这档部分分在讲题时就被很多人吐槽，称这档部分分妨碍了思考正解．

如果题目给分方式与默认方式不同（如：在一般的 OI 赛制比赛中绑 subtask 测试），一定要在题面中说明．

不推荐使用「百分之 XX 的数据满足 XX」的说法，尤其是数据范围有多个变量时．例如，「$30\%$ 的数据满足 $n \le 1000$」和「$40\%$ 的数据满足 $m \le 100$」可能描述了 $70\%$ 的数据的性质，也可能只描述了 $40\%$ 数据的性质．一般来说，subtask 或数据范围表格是更好的选择．

## 造数据

数据生成是出题过程中必要的一步，也是对拍时所必需的，掌握一些生成数据的技巧，就能使造数据的过程更加轻松，造出来的数据强度更高．

### 生成随机数据

#### 生成随机数

请参考 [随机函数](../misc/random.md) 页面．

需要特别提醒的是，在生成值域比随机函数返回值更大的数时，请 **不要** 使用 `rand() * rand()` 之类的写法，这样的写法生成的随机数非常不均匀．

另外，出题时推荐使用 [testlib](../tools/testlib/generator.md) 来造数据，可以保证在不同平台上同一个种子生成的随机数相同，并且种子会依据命令行参数自动生成．

#### 生成随机排列

可以使用 STL 中的 `std::shuffle` 函数，形如 `std::shuffle(a, a + n, rng)`，这里 `rng` 是一个随机数生成器，比如 `std::mt19937 rng(std::chrono::steady_clock::now().time_since_epoch().count())`．

请 **不要** 使用 `std::random_shuffle`，它在 C++14 中弃用，C++17 中被移除．

#### 生成随机区间

常见错误方法：在 $[1,n]$ 中随机生成左端点 $l$，再在 $[l, n]$ 中随机生成右端点 $r$．这样的话生成的区间会比较靠右．

较为正确的方法（推荐做法）：在 $[1, n]$ 中随机生成两个数，取较小的作为左端点，较大的作为右端点．

真正均匀随机的方法：在 $[0, n]$ 中生成一个随机数 $x$，若 $x = 0$，再在 $[1, n]$ 中生成一个随机数 $y$，区间为 $[y, y]$；否则按「较为正确的方法」生成．

#### 生成随机树

常用方法是为 $2\sim n$ 的每个节点 $i$ 从 $[1,i-1]$ 中随机选择一个父亲．这样做的话生成的树不是均匀随机的，期望高度为 $O(\log n)$．

还有一种随机方法：从 $[i\cdot low, i\cdot high]$ 中随机选择 $i$ 的父亲．若 $low$ 和 $high$ 设置得当，可以造出强度较高的树．

真正均匀随机的方法是利用 [Prüfer 序列](../graph/prufer.md)，先生成一个随机 Prüfer 序列，再通过序列生成树．这样做的话，树的期望高度为 $O(\sqrt n)$．

除此之外，可以随机一个排列来给节点重编号/打乱边的顺序．

### 构造数据

#### 区间相关的题目

常用构造：长度特别小（特殊地，全部为单点）、长度特别大（特殊地，全部为整个序列）．

#### 需要分解因数的题目

可重质因数个数尽量多：$2$ 的幂．

去重后质因数个数尽量多：最小的若干个质数相乘．

约数尽量多：可以参考 OEIS 上的 [A002182](http://oeis.org/A002182) 数列．

#### 需要求最大公因数的题目

让需要求最大公因数的两个数为 [斐波那契数列](../math/combinatorics/fibonacci.md) 的相邻两项，可以让欧几里得算法达到最坏时间复杂度．

#### 树上问题

常用构造：

-   链
-   菊花
-   完全二叉树
-   将完全二叉树的每个节点替换为一条长为 $\sqrt n$ 的链
-   菊花上挂一条链
-   链上挂一些单点
-   一棵高度为 $d$ 且 $d>1$ 的树的根节点有两个儿子，左子树是一条长为 $d-1$ 的链，右子树是一棵高度为 $d-1$ 的这样的树．

如果不是在考场上，还可以使用 [Tree-Generator](https://github.com/ouuan/Tree-Generator) 来生成各种各样的树．

### 批量生成数据

笔者推荐使用命令行参数 + bat/sh 的方法．

例如：

`gen.cpp`:

```cpp
#include "testlib.h"

using namespace std;

int n, m, k;
vector<int> p;

int main(int argc, char* argv[]) {
  registerGen(argc, argv, 1);

  int i;

  n = atoi(argv[1]);
  m = atoi(argv[2]);
  k = rnd.next(1, n);

  for (i = 1; i <= n; ++i) p.push_back(i);

  shuffle(p.begin(), p.end());
  // 使用 rnd.next() 进行 shuffle

  printf("%d %d %d\n", n, m, k);
  for (i = 0; i < n; ++i) {
    printf("%d%c", p[i], " \n"[i == n - 1]);
    // 把字符串当作数组用，中间空格，末尾换行，是一个造数据时常用的技巧
  }

  return 0;
}
```

`gen_scripts.bat`:

```bat
gen 10 10 > 1.in
gen 1 1 > 2.in
gen 100 200 > 3.in
gen 2000 1000 > 4.in
gen 100000 100000 > 5.in
```

这样做的好处是，对于不同的数据只需要写一个 generator，并且可以方便地修改某个测试点的参数．

### 造数据的要求

数据应当包含各个参数的最小值和最大值．

数据应当包含各种边角情况．

在使用 subtask 时，数据（包括输入、输出）最好覆盖到值域中的各个范围，而不是只有数据范围的最大值．

为了防止针对特殊构造的特判过掉，可以将不同的构造结合在一个测试点中，或者数据的大部分是构造，掺杂小部分的随机．

数据中应当包含各种各样的构造，即使你不知道什么错解会挂在这组构造上．（在按测试点给分的赛制中需要酌情处理．）

当然，如果你已知一个（正常人能想的到、写的出的）正确性有问题的错解，要尽量卡掉它．

需要特别提醒的是，如果有整型溢出的可能，一定要卡掉会溢出的做法．在有部分分的赛制中，不应使不开 long long 的人得到和暴力一样甚至更低的分数．

如果有 pretests，pretests 应尽量强，（同时尽量少）．换言之，你需要在 pretests 中（用尽量少的数据组数）包含该题的所有已知叉点．

如果你希望出现少量而非没有 FST，仍然应当保证 pretests 的强度，因为实际比赛中很可能出现你意想不到的错误，导致远远高出预期的 FST 数量．

### 数据的格式

这里提供一些通常情况下输入数据的格式要求，可作为一般情况下的参考：

> 1.  使用测试环境下的换行格式．
> 2.  文件最后一行的末尾有换行符，即整个文件的最后一个字符需要是 `\n`．
> 3.  任何一行的开头和末尾都没有空白字符．
> 4.  连续的空格不超过 1 个．

在 Windows 环境下生成的数据，其换行格式通常为 `\r\n`，而主流测评系统均在 Linux 环境下运行，其换行格式为 `\n`．若在 Linux 环境下读入 Windows 格式的换行数据，可能会导致读入字符串时换行处理异常，进而导致不同环境下程序运行结果不同；若在 Linux 环境下比较 Linux 环境下生成的输出和 Windows 环境下生成的标准输出，可能由于换行格式不同而导致比较存在差异．为了保持程序行为一致，所有数据的换行格式必须转换为程序运行环境下的换行格式．

一般可以通过如下方式生成 Linux 格式换行的数据：

1.  直接使用 Linux 环境生成数据．
2.  通过 [`dos2unix`](https://dos2unix.sourceforge.io/) 工具对输入输出文件进行转换，此工具包含于 Cygwin, MinGW 等工具链中．
3.  使用二进制方式打开输出文件，并且使用 `\n` 换行格式．
4.  参考 [此页面](https://help.luogu.com.cn/manual/luogu/problem/testcase-format#附录windows-环境下造数据注意事项) 中 `dos2unix.cpp` 代码自行编写工具．

## Special Judge

[SPJ 编写教程](../tools/special-judge.md)

输出方案题和输出浮点数题是两种较为常见的需要使用 SPJ 的题型，其它题目视情况也需要使用 SPJ．在 CF 上，所有题目都必须使用基于 testlib 的 checker，例如：题目要求输出若干个整数时，使用 testlib 自带的 ncmp checker，选手可以任意输出空白字符（既可以空格也可以换行）．

checker 一般使用 testlib 编写．由于 checker 要应对各种各样的不合法输出，需要极强的鲁棒性，不使用 testlib 是很难写好 checker 的．

编写 checker 需要注意以下两点：

1.  你需要应对各种不合法的输出，因此，请检查读入的每个变量是否在合法范围中（`readInt(minvalue, maxvalue)`）．例如：读入一个在 check 过程中会作为数组下标的变量时必须检查其范围，否则可能引发数组越界，有时这会导致 RE，有时则可能判为 AC．
2.  原则上 checker 中不应检查空白字符（即，不应使用 `readSpace()`、`readEoln()`、`readEof()`，值得一提的是，testlib 会自动检查是否有多余的输出）．

## 题解

题解的目标是让预计会来参加比赛的人都能看懂．所以官方题解详细程度的要求会比一般的题解高．

### 关于部分分

在有部分分的题目中，题解里可以考虑写一写部分分的做法．

### 关于知识点

解题中用到的知识点应当明确指出．对于一些难度和题目难度相当的知识点，最好给出学习该知识点的资料（比如一篇博客的地址）．

### 关于定义

题解中不要凭空冒出来一些概念．

例如：dp 的题解要解释清楚状态的定义．

### 关于细节

具体的实现细节如果比较巧妙最好写出来，否则的话「详见代码」也是可以的．如果「详见代码」的话，最好在代码中加上一定的注释．

### 标程

标程中最好去掉冗余部分．比如，有的题解中保留了完整的 define 模板（为了提高做题速度，包含大量 define 与常用函数，常用于 CF 等在线比赛），并且其中很大一部分都没有用到，这是不好的．

如果涉及到一些题解中没有详细说明的实现细节，最好加上适量的注释．

## 比赛

### 比赛通知中的题目难度需真实

> Remember that authors tend to underestimate the difficulty of their problems.
>
> ——Codeforces PROPOSE A PROBLEM 页面的提醒

出题人很可能错误估计题目的难度，因此，如果要在比赛通知中写上比赛难度，需要谨慎考虑，最好提前请人来验题并进行评估．

### 题目难度的分配

在类国内 OI 的模拟赛中，往往是三道题的整体难度与比赛难度相当即可．

在类 CF/ATC 这种线上赛的比赛中，需要尽量保证难度的递增（虽然由于对难度的误估很多时候都并不能真正做到），并且尽量避免出现大的 difficulty gap．可以通过把一题分为难易两题（两个 subtask）来减少 difficulty gap，但是分 subtask 需要谨慎考虑，也有很多人不喜欢 CF 赛制中的 subtask（[Are subtasks evil?](https://codeforces.com/blog/entry/71700)），原因包括但不限于：

-   由于赛制原因，可能先做 easy version 再做 hard version 罚时更少而总分更高
-   subtask 的赋分往往与题目难度不成正比
-   很多时候 easy version 的题目并不是一道合格的题目（不有趣）
-   很多时候 easy version 的解法对于思考 hard version 的正解没有帮助

### 题目知识点的分配

一场比赛应尽量涵盖较广的知识点（专题训练赛当然除外）．

经典反例：涵盖了动态规划、期望、组合计数、容斥原理、多项式等多种知识点的 CTS2019．

> 我要从五道题里选六道，我也很无奈啊．
>
> ——CTS2019 组题人给出的理由，没有收到足够多的题目投稿

## 出题平台

### Polygon

Polygon 是一个功能非常强大的多人合作出题平台，可以作为在任何网站（使用 package 功能导出到不支持 Polygon 的网站）多人合作出题的首选方案，单人出题（尤其是在不同设备上出题）时也是很不错的选择，使用方法参见 [Polygon 简介](../tools/polygon.md)．

### Codeforces

Codeforces 是全球最著名的算法竞赛网站之一，题目质量较高，非常适合有一定出题经验并且想进一步提升出题水平、想要出一套高质量题目的出题人．不足之处是审核速度较慢（一般要几个月），但你也可以在审核期间就开始题目的准备（虽然有题目被否掉导致准备白费了的风险）．

#### 出题资格

-   蓝名且参加过至少 25 场 rated 比赛；
-   紫名且参加过至少 15 场 rated 比赛；
-   橙名且参加过至少 5 场 rated 比赛；
-   红名或黑红名．

#### 提交比赛申请

有了出题资格后，在侧边栏可以看到 [Propose a contest/problems](http://codeforces.com/proposals/new-contest) 按钮．

点进去之后，先写一份 contest proposal（在 PROPOSE A CONTEST 里写），然后再写 problem proposal 并添加进比赛里．

题目决定好之后，就可以将 contest proposal open to review（提交审核）了．

#### 在 Polygon 上准备题目

参考 [Polygon 简介](../tools/polygon.md)．

#### 与管理之间的联系

与管理联系有两个作用：

1.  加快审核速度．
2.  进入准备阶段后管理会提供建议和帮助．

正规的联系方式是在 proposal system 中以 proposal 的形式提交申请，管理开始审核之后以 comment 的形式在 proposal 的下方进行讨论．

实际上，如果 proposal 长时间没有过审，可以考虑私信联系管理（其实 CF 上写了 "Don't send private messages or emails to coordinators"，但 300iq 在 [评论](http://codeforces.com/blog/entry/64077#comment-478933) 中表示可以私信他）．

### Comet OJ

[Comet OJ 链接](https://www.cometoj.com/)

已经不再活跃（截至 2021 年 11 月，最后一场比赛是 2020 年 1 月的）．

出题申请：<https://info.cometoj.com/contests/Questionnaire_IssuerInfo/>

### CodeChef

印度的算法竞赛平台，有三种赛制：10 天且带 challenge 的 Long Challenge，2.5h 类 ICPC 的 Cook-Off，3h 类 IOI 的 LunchTime．

出题 FAQ：<https://www.codechef.com/wiki/faq-problem-setters>

出题指南：<https://www.codechef.com/problemsetting>

### AtCoder

日本的算法竞赛平台，出题联系方式：<contest@atcoder.jp>．

### UOJ & LOJ

比赛不多的国内 OJ．

### 洛谷

参与出题工作人员需要有一定的奖项认证等级，创建比赛后由负责人在 [工单系统](https://www.luogu.com.cn/ticket) 中提交申请．

公开赛规范：<https://help.luogu.com.cn/rules/academic/opencontest-standard>

## 参考资料

1.  [vfk《UOJ 精神之源流》][1]

2.  [王天懿《论偏题的危害》][2]

3.  [CF 出题人须知][3]（[国内可访问的图片版](https://github.com/OI-wiki/libs/blob/master/topic/rules.jpg)）

4.  [CF 出题人的自我修养][4]

本文由作者本人自 [ouuan 的出题规范](https://ouuan.github.io/post/ouuan-的出题规范/) 搬运而来并有所修改、补充．

[1]: https://vfleaking.blog.uoj.ac/blog/909 "vfk《UOJ 精神之源流》"

[2]: https://github.com/OI-wiki/libs/blob/master/topic/7-%E7%8E%8B%E5%A4%A9%E6%87%BF-%E8%AE%BA%E5%81%8F%E9%A2%98%E7%9A%84%E5%8D%B1%E5%AE%B3.ppt "王天懿《论偏题的危害》"

[3]: https://docs.google.com/document/d/e/2PACX-1vRhazTXxSdj7JEIC7dp-nOWcUFiY8bXi9lLju-k6vVMKf4IiBmweJoOAMI-ZEZxatXF08I9wMOQpMqC/pub "CF 出题人须知"

[4]: https://github.com/OI-wiki/libs/blob/master/topic/CF%E5%87%BA%E9%A2%98%E4%BA%BA%E7%9A%84%E8%87%AA%E6%88%91%E4%BF%AE%E5%85%BB.md "CF 出题人的自我修养"


## contest/resources.md

author: Suyun514, ChungZH, Enter-tainer, StudyingFather, Konano, JulieSigtuna, GldHkkowo, SukkaW, Rapiz1, Henry-ZHR, H-J-Granger, countercurrent-time, fouzhe, Ir1d, abc1763613206, EndlessCheng, Plaaant6, LUTLJS, ZsgsDesign, CB-X2-Jun, tallnutliu

本页面主要列举了一些与算法竞赛有关的在线评测网站、题目合集、书籍、工具等资源．

## 在线评测平台

在线评测平台（英语：Online Judging System，简称：OJ），一般用于刷题训练，参与和组织比赛，以及用户之间的交流分享．

### 国内

-   [51Nod](https://www.51nod.com/)：有许多值得尝试的数学题和思维题．
-   [Comet OJ](https://www.cometoj.com)：始于 2018 年，旨在为广大算法爱好者提供一个竞技、练习、交流的平台，经常举办原创性的高质量比赛，有丰富的题库．
-   [HDU Online Judge](http://acm.hdu.edu.cn/) 始于 2005 年，杭州电子科技大学在线评测系统，有多校训练的题目．
-   [HydroOJ](https://hydro.ac/)：始于 2021 年，为开源项目 [Hydro](https://hydro.js.org/) 的官方站．用户可以创建自己的 [域](https://hydro.ac/discuss/6087cc44e098b0cd7dde1a0c)，域中可以使用题库、比赛、讨论等主站可以使用的功能．
-   [Judge Duck Online](https://duck.ac/) 基于 [松松松](https://github.com/wangyisong1996) 开发的开源项目 [JudgeDuck](https://github.com/JudgeDuck)，可以将评测程序的运行时间精确到微秒．（题目较少）
-   [LibreOJ](https://loj.ac/)：始于 2017 年．基于开源项目 [Lyrio](https://github.com/lyrio-dev/lyrio)，Libre 取自由之意．题目所有测试数据以及提交的代码均对所有用户开放．目前由 [Menci](https://github.com/Menci) 维护．
-   [CDOJ](https://cdoj.site/d/lutece/)：电子科技大学在线评测系统，始于 2012 年．
-   [洛谷](https://www.luogu.com.cn/)：始于 2013 年，社区群体庞大，各类 OI 的真题和习题较全．提供有偿教育服务．
-   [牛客网](https://www.nowcoder.com/)：始于 2014 年，提供技术类求职备考、社群交流、企业招聘等服务．
-   [OpenJudge](http://openjudge.cn/)：始于 2005 年，由 POJ 团队开发的小组评测平台．
-   [POJ](http://poj.org/)：北京大学在线评测系统，始于 2003 年，国内历史最悠久的 OJ 之一．内有很多英文题，既有基础题，也有值得一试的好题．可以在 [百练](http://bailian.openjudge.cn/practice/) 题库提交 POJ 的题目．
-   [PTA（拼题 A）](https://pintia.cn/)：始于 2016 年，浙江大学衍生的杭州百腾教育科技有限公司产品．
-   [QOJ](https://qoj.ac/)：收集了很多国内外 OI 和 ICPC 竞赛题目，具有训练价值．
-   [Universal Online Judge](https://uoj.ac/)：始于 2014 年，Universal 取通用之意，[项目开源](https://github.com/UniversalOJ/UOJ-System)；[VFK](https://github.com/vfleaking) 的 OJ：多原创比赛题和 CCF/THU 题，难度较高．
-   [Vijos](https://vijos.org/)：始于 2005 年．[服务端](https://github.com/vijos/vj4) 和 [评测机](https://github.com/vijos/jd4) 等项目开源．
-   [WZOI](https://wzoi.cn)：始于 2017 年，由浙江省温州中学维护的 [开源](https://github.com/massimodong/wzoj) 评测系统．
-   [ZOJ](https://zoj.pintia.cn/home)：浙江大学在线评测系统，始于 2001 年．

### 国外

-   [AizuOJ](https://onlinejudge.u-aizu.ac.jp)：日本会津大学在线评测系统，始于 2004 年．包含日本若干高中和大学编程比赛的题目，自带编程/数据结构/算法的入门课程．
-   [AtCoder](https://atcoder.jp/)：日本 OJ，日文版里会有日本高校的比赛，英文内不会显示．题目有趣，质量较高．
-   [CodeChef](https://codechef.com/)：印度 OJ，周期举办比赛．系统基于 SPOJ 的 Sphere Engine．
-   [Codeforces](https://codeforces.com/)：俄罗斯 OJ，始于 2010 年，创始人是 [Mike Mirzayanov](https://www.linkedin.com/in/mike-mirzayanov-31772a93/)．有多种系列的比赛，并支持个人出题、申请组织比赛．题目质量较高．
-   [CSES](https://cses.fi/problemset/)(Code Submission Evaluation System)，按专题划分的题库，[旨在](https://cses.fi/problemset/text/2433) 成为综合的高质量题库，主要由 [Competitive Programmer’s Handbook](https://cses.fi/book/book.pdf) 作者 Antti Laaksonen 开发，始于 2013 年．
-   [CS Academy](https://csacademy.com/)
-   [DMOJ](https://dmoj.ca/) 加拿大开源的 OJ，语言支持广；题库是各大比赛的存档，也有定期自行举办的比赛．
-   [HackerRank](https://www.hackerrank.com/) 有很多比赛
-   [Kattis](https://open.kattis.com/) 题库主要包含类似 ICPC 比赛的题目；根据用户解题情况评定用户等级，推荐适合该用户水平的 trivial/easy/medium/hard 四类难度的题目，其中题目难度采用类 [ELO 等级分](https://zh.wikipedia.org/wiki/%E7%AD%89%E7%BA%A7%E5%88%86) 系统来评估．
-   [LeetCode](https://leetcode.com/) 码农面试刷题网站，有中文分站：[LeetCode China](https://leetcode.cn)．
-   [Light OJ](https://lightoj.com)
-   [Open Trains](https://opentrains.opencup.org/) 俄罗斯 Open Cup 比赛的训练平台，基于 [ejudge](https://ejudge.ru/) 开源系统搭建，支持虚拟比赛；题库包含历年 Open Cup 赛题以及 Petrozavodsk 训练营的题目．
-   [SPOJ](http://www.spoj.com) 始于 2003 年，其后台系统 [Sphere Engine](https://sphere-engine.com/) 于 2008 年商业化；支持题目点赞和标签功能．
-   [TopCoder](https://www.topcoder.com/) 始于 2001 年，其 [竞技编程社区](https://www.topcoder.com/community/competitive-programming/) 有很多比赛；目前主营业务是技术众包．
-   [TimusOJ](http://acm.timus.ru/) 始于 2000 年，由 Ural Federal University 开发，拥有俄罗斯最大的在线评测题库，题目主要来自乌拉尔联邦大学校赛、乌拉尔锦标赛、ICPC 乌拉尔区域赛、以及 Petrozavodsk 训练营．
-   Online Judge（前 [UVaOJ](https://uva.onlinejudge.org/)）始于 1995 年，国际成名最早的 OJ，创始人是西班牙 University of Valladolid (UVa) 的 Miguel Ángel Revilla 教授；由于 [Revilla 教授于 2018 年不幸离世](https://www.elnortedecastilla.es/valladolid/muere-profesor-miguel-20180402225739-nt.html)，且 Valladolid 大学终止维护，UVaOJ 自 2019 年 7 月起更名为 Online Judge．现在该平台的维护者 [正在 GitHub 上构建新的评测平台](https://github.com/TheOnlineJudge/ojudge)．
-   [Yandex](https://contest.yandex.ru/) 存档了近几年的全俄罗斯信息学奥赛．

## 教程资料

-   [**OI Wiki**](https://oi-wiki.org)
-   [Codeforces 上网友整理的一份教程合集](https://codeforces.com/blog/entry/125623)
-   [英文版 E-Maxx 算法教程](https://cp-algorithms.com/)
-   [演算法筆記](https://web.ntnu.edu.tw/~algo/)：台湾师范大学总结的教程
-   [如何为 ACM-ICPC 做准备？- geeksforgeeks](https://www.geeksforgeeks.org/how-to-prepare-for-acm-icpc/)
-   [Topcoder 整理的教程](https://www.topcoder.com/community/competitive-programming/tutorials/)
-   [校招面试指南](https://github.com/jwasham/coding-interview-university)
-   [由 hzwer 收集整理自互联网的课件](https://github.com/hzwer/shareOI)
-   [Trinkle23897 的课件](https://github.com/Trinkle23897/oi_slides)
-   [huzecong 的课件](https://github.com/huzecong/oi-slides)
-   [Open Data Structure](https://opendatastructures.org/)：内含众多数据结构讲稿
-   [IOI Syllabus (2020)](https://ioinformatics.org/files/ioi-syllabus-2020.pdf)

## 书籍

本列表内注明了书籍作者，译者未列其中．因无重名书籍且易于寻找，故不标明 ISBN．

-   刘汝佳系列
    -   《算法竞赛入门经典》（紫）
        -   [第一版 配套资源仓库（镜像）](https://github.com/sukhoeing/aoapc-book/)
        -   [第二版 配套资源仓库](https://github.com/aoapc-book/aoapc-bac2nd)
        -   [第二版 习题选解](https://github.com/sukhoeing/aoapc-bac2nd-keys)
    -   《算法竞赛入门经典 - 训练指南》（白/蓝）- 陈锋 合著
    -   《算法艺术与信息学竞赛》（蓝/黑）
-   《算法竞赛进阶指南》- 李煜东
    -   [配套资源仓库](https://github.com/lydrainbowcat/tedukuri)
-   《啊哈算法》- 纪磊
    -   面向初学者或有初步兴趣的人群，有幽默配图．
-   CCF 中学生计算机程序设计系列
    -   《CCF 中学生计算机程序设计 - 入门篇》- 陈颖，邱桂香，朱全民
        -   [建议配合勘误使用．](https://zhuanlan.zhihu.com/p/85215961)
    -   《CCF 中学生计算机程序设计 - 基础篇》- 江涛，宋新波，朱全民
    -   《CCF 中学生计算机程序设计 - 提高篇》- 徐先友，朱全民
    -   《CCF 中学生计算机程序设计 - 专业篇》（未出）
-   深入浅出系列
    -   《深入浅出程序设计竞赛 - 基础篇》- 洛谷网校教研组
-   一本通系列
    -   《信息学奥赛一本通》- 董永建
    -   《信息学奥赛一本通 - 提高篇》- 黄新军，董永建
        -   [建议选择性阅读．](https://www.zhihu.com/question/292926937)
    -   《信息学奥赛一本通 - 高手训练》- 黄新军，董永建
-   其他由国内著名 OI 教练写的教材
    -   《信息学奥赛课课通》- 林厚从
    -   《聪明人的游戏：信息学探秘 - 提高篇》- 江涛，陈茂贤
    -   《计算概论：C++ 编程与信息学竞赛入门》- 金靖
    -   《算法竞赛宝典》- 张新华
-   ACM 国际大学生程序设计竞赛系列
    -   《ACM 国际大学生程序设计竞赛系列 知识与入门》- 俞勇
    -   《ACM 国际大学生程序设计竞赛系列 算法与实现》- 俞勇
    -   《ACM 国际大学生程序设计竞赛系列 题目与解读》- 俞勇
-   《算法竞赛入门到进阶》- 罗勇军，郭卫斌
-   《算法导论》第三版 - Thomas H.Cormen/Charles E.Leiserson/Ronald L.Rivest/Clifford Stein  
    黑书，大学经典教材．英文版原名*Introduction to Algorithms*
    -   [答案解析 (English)](https://github.com/walkccc/CLRS)
-   《具体数学》第二版 - Ronald L. Graham/Donald E. Knuth/Oren Patashnik  
    英文版原名*Concrete Mathematics*
-   《组合数学》第五版 - Richard A.Brualdi  
    英文版原名*Introductory Combinatorics*
-   《挑战程序设计竞赛》全套 - 秋叶拓哉，岩田阳一，北川宜稔
    通俗易懂．
-   《算法概论》- Sanjoy Dasgupta/Christos Papadimitriou/Umesh Vazirani
    -   提纲挚领，但内容较少．
-   [Legend-K 的数据结构与算法的笔记](http://web.archive.org/web/20180826111306/http://www.legend-k.com/Algorithm/Algorithm.pdf)
-   [acm-cheat-sheet](https://github.com/soulmachine/acm-cheat-sheet)
-   [Competitive Programmer’s Handbook](https://cses.fi/book/book.pdf)- Antti Laaksonen
    -   作者花了三年个人时间完成．面向算法竞赛，覆盖面广，详略得当．
-   [《挑战编程：程序设计竞赛训练手册》](http://acm.cs.buap.mx/downloads/Programming_Challenges.pdf)- Steven S. Skiena/Miguel A. Revilla
    -   由西班牙 University of Valladolid 的两位教授编写．
    -   阅读 [经过翻译的在线电子版图书](http://www.tup.com.cn/upload/books/yz/030502-01.pdf)
    -   购买 [纸质版图书](http://www.tup.tsinghua.edu.cn/booksCenter/book_03050201.html)
-   《C++，挑战编程——程序设计竞赛进阶训练指南》- 邱秋
    -   [作者博客的介绍页](https://blog.csdn.net/metaphysis/article/details/90288252)
-   [《数据结构（C++ 语言版 第 3 版）》- 邓俊辉](https://dsa.cs.tsinghua.edu.cn/~deng/ds/dsacpp/index.htm)
    -   建议随配套课程、配套课件和习题解析一起使用．
-   《计算几何：算法与应用》- 伯格（Berg,M.D.）著，邓俊辉 译  
    英文版原名*Computational Geometry: Algorithms and Applications*
-   [《Handbook of Data Structures and Applications, 2nd Edition》](https://www.routledge.com/Handbook-of-Data-Structures-and-Applications/Mehta-Sahni/p/book/9780367572006)
    -   由许多著名教授如 Sartaj Sahni、Hanan Samet、Weiss 等合著，内容较多，建议有一定基础的数据结构爱好者阅读．
-   [算法详解 系列](https://www.algorithmsilluminated.org/)
    -   面向有语言基础的初学者的教材，建议同配套课程一起使用
    -   《Algorithms Illuminated, Part 1: The Basics》- Tim Roughgarden
    -   《算法详解，卷 1：算法基础》- 徐波 译
    -   《Algorithms Illuminated, Part 2: Graph Algorithms and Data Structures》- Tim Roughgarden
    -   《算法详解，卷 2：图算法和数据结构》- 徐波 译
    -   《Algorithms Illuminated, Part 3: Greedy Algorithms and Dynamic Programming》- Tim Roughgarden
    -   《Algorithms Illuminated, Part 4: Algorithms for NP-Hard Problems》- Tim Roughgarden

## 课程

-   [CMU 15-295 (2025)](https://contest.cs.cmu.edu/295/)
-   [LSU: CSC 2700 (2024)](http://isaac.lsu.edu/class/)
-   [NUS: CS 3233 (2021)](https://www.comp.nus.edu.sg/~stevenha/cs3233.html)
-   [Reykjavik: T-414-ÁFLV (2016)](https://algo.is/)
-   [Stanford: CS 97SI (2015)](https://web.stanford.edu/class/cs97si/)
-   [Stonybrook: CSE 392 (2012)](https://www3.cs.stonybrook.edu/~skiena/392/)
-   [UBC: CPSC 490 (2021)](https://www.students.cs.ubc.ca/~cs-490/2019W2/problem-solving/)
-   [UCF: COP 4516 (2025)](https://www.cs.ucf.edu/~dmarino/progcontests/cop4516/spr2025/)
-   [THU: 数据结构](https://www.xuetangx.com/course/THU08091000384/)
-   [THU: 计算几何](https://www.xuetangx.com/course/THU08091000327/)
-   [StanfordOnline: Algorithms: Design and Analysis](https://www.algorithmsilluminated.org/)

## 工具

-   [《100 个 gdb 小技巧》](https://github.com/hellogcc/100-gdb-tips)
-   [Algorithm Visualizer](http://algorithm-visualizer.org)
-   [cppreference](https://zh.cppreference.com/w/)：一个全面的 C 和 C++ 语言及其标准库的在线参考资料
-   [Compiler Explorer](https://godbolt.org)：在线查看编译后代码块对应的汇编语句，支持选择不同的编译器
-   [C++ Insights](https://cppinsights.io/)：以编译器的视角去查看你的 C++ 源码
-   [Inverse Symbolic Calculator](http://wayback.cecm.sfu.ca/projects/ISC/ISCmain.html)：实数反查表达式，适用于反推常数
-   [$\rm\LaTeX$ 手写符号识别](http://detexify.kirelabs.org/classify.html)
-   [$\rm\LaTeX$ 数学公式参考](http://www.mohu.org/info/symbols/symbols.htm)
-   [Mathpix](https://mathpix.com/)：截图转 $\rm\LaTeX{}$
-   [OEIS](https://oeis.org)：整数数列搜索引擎
-   [Python Tutor](https://pythontutor.com/): 代码执行过程可视化
-   [Quick C++ Benchmark](https://quick-bench.com/)：在线比较两个及以上函数的运行速度
-   [Try It Online](https://tio.run)：在线运行 600+ 种语言的代码，支持 IO 交互，超时 60s，可以分享代码
-   [图论画板](https://csacademy.com/app/graph_editor/) 与 [GraphViz](http://www.graphviz.org/)
-   [uDebug](https://www.udebug.com)：提供一些 OJ 题目的调试辅助
-   [USF](https://www.cs.usfca.edu/~galles/visualization/) 与 [VisuAlgo](https://visualgo.net/zh)：算法可视化
-   [Wandbox](https://wandbox.org/): 在线代码运行，支持 30+ 种语言，可以分享代码，支持不同编译器版本
-   [Wolfram Alpha](https://www.wolframalpha.com/)：可以计算包括数学、科学技术、社会文化……等多个主题的问题

## 题集和资源

-   [POJ 训练计划](https://blog.csdn.net/skywalkert/article/details/46594541)
-   [USACO](http://train.usaco.org/usacogate)
-   [洛谷题单](https://www.luogu.com.cn/training/list)
-   [-Morass- 贴在 Codeforces 上的一份题单](https://codeforces.com/blog/entry/55274)
-   Codeforces 社区高质量算法文章合集 [之一](https://codeforces.com/blog/entry/57282)  [之二](https://codeforces.com/blog/entry/13529)
-   [北京大学 ICPC 暑期课课件例题](https://vjudge.net/article/446)
-   [北京大学 ICPC 暑期课课件](https://lib-pku.github.io/#acm-icpc%E6%9A%91%E6%9C%9F%E8%AF%BE)
-   [GitHub.com:OI-wiki/libs](https://github.com/OI-wiki/libs)
-   [多校联合训练](http://acm.hdu.edu.cn) 关键词：`Multi-University Training Contest`
-   [Vjudge](https://vjudge.net/)
-   [Project Euler](https://projecteuler.net/)
-   [Junior Training Sheet](https://goo.gl/unDETI)：对新手友好的训练计划
-   [USACO Guide](https://usaco.guide/)：针对 USACO 的各个级别分类的训练资源


## contest/roadmap.md

???+ note "提示"
    本文章正在编辑讨论中，欢迎补充更进一步的学习路线或在评论区提出你的想法！

本文将会介绍算法竞赛的学习路线．

该学习路线既是新手学习算法竞赛知识的指南，也是一份复习清单．

## 1 C++ 语言基础

先从 C++ 语法学起，一步一步来．

### 1.1 Hello, World!

以一句 `Hello, World!`，开始算法竞赛之旅吧！

同时了解一下 C++ 的源程序的大致框架是什么样子的．

-   [Hello, World!](../lang/helloworld.md)
-   [C++ 语法基础](../lang/basic.md)

### 1.2 变量与运算

计算机出现的最初目的就是计算．因此我们先学习如何完成一些简单的运算任务吧．

-   [变量](../lang/var.md)
-   [运算](../lang/op.md)

### 1.3 流程控制

#### 1.3.1 分支结构

有的时候，我们需要在不同的条件下，选择执行不同的语句，这时候我们就需要借助分支语句．

-   [分支](../lang/branch.md)

分支语句包括下面几种：

-   if 语句
-   if-else 语句
-   if-elif-else 语句
-   switch 语句

#### 1.3.2 循环结构

将若干条语句重复执行多次，就需要用到循环语句．

-   [循环](../lang/loop.md)

循环语句包括下面几种：

-   for 语句
-   while 语句
-   do-while 语句

### 1.4 数组与结构体

数组用于存储大量相同类型的数据．而结构体则可以将若干变量捆绑起来．

-   [数组](../lang/array.md)
-   [结构体](../lang/struct.md)

### 1.5 函数与递归

使用函数来让程序变得模块化，降低实现成本．

递归则是新手入门的一道坎，「自己调用自己」听起来并不是那么容易理解，不过仔细深究根本，就会发现「自己调用自己」和「自己调用别人」并没有本质差别．

-   [函数](../lang/func.md)
-   [递归 & 分治](../basic/divide-and-conquer.md)

## 2 CSP-J 入门级

### 2.1 枚举与模拟

从现在开始，你已经会使用 C++ 语言完成一些简单的任务了，但是这远远不够．

为了做对一些简单的题目，你需要学会通过枚举或模拟脑海中的逻辑，来实现代码．这看起来并不是很高效，但有的时候很管用．

-   [枚举](../basic/enumerate.md)
-   [模拟](../basic/simulate.md)

### 2.2 递归与分治

递归是指函数定义中不断调用自己的方法；而分治则是不断将这一个问题分解为若干子问题，求解后合并的操作．

-   [递归 & 分治](../basic/divide-and-conquer.md)

### 2.3 字符串

在做信息学题目时，经常会碰到的一个数据类型就是字符串，你需要学习一些用于操作字符串的 STL 函数．当然，模拟也是解决字符串问题的好方法．

-   [字符串基础](../string/basic.md)
-   [STL 函数](../string/lib-func.md)

### 2.4 排序

当你获得了一组数据时，如何将他们从无序变成有序也是个很重要的问题．在你没有思路的时候，不妨考虑一下将数组排个序吧．这也是接下来的很多算法的基础．

排序的方法有点多，但理解后记住它们并不难．

-   [排序简介](../basic/sort-intro.md)
-   [选择排序](../basic/selection-sort.md)
-   [冒泡排序](../basic/bubble-sort.md)
-   [插入排序](../basic/insertion-sort.md)
-   [计数排序](../basic/counting-sort.md)
-   [基数排序](../basic/radix-sort.md)
-   [快速排序](../basic/quick-sort.md)
-   [归并排序](../basic/merge-sort.md)
-   [堆排序](../basic/heap-sort.md)
-   [桶排序](../basic/bucket-sort.md)
-   [排序相关 STL](../basic/stl-sort.md)

NOI 大纲中入门级只要求学习选择、冒泡、插入排序，共三个排序算法，但是其余的难度也并不大，且初赛中可能涉及，故一并列出．

### 2.5 二分与倍增

二分查找，本质上是运用分治的思想，不断减少查找范围的大小，直至找到答案．但是需要注意，这个查找方式必须应用在有序的数据结构中．

-   [二分](../basic/binary.md)

而倍增则不同，它是不断翻倍，以把线性范畴内的处理转化为对数级，大大优化时间复杂度．（这个知识点需要一点数学基础，暂时跳过也问题不大）

-   [倍增](../basic/binary-lifting.md)

### 2.6 搜索

在入门组，搜索的题目常常会在迷宫类题目中出现，一般会有地图类的数据；此外，搜索也十分常用于高效地枚举构造合法解的情况，亦可用于骗分．

#### 2.6.1 深度优先搜索（DFS）

深度优先搜索指利用递归函数方便地实现暴力枚举的算法，与图论中的 DFS 算法有一定相似之处，但并不完全相同．

-   [DFS（搜索）](../search/dfs.md)

#### 2.6.2 广度优先搜索（BFS）

将每一个状态设计为图中的一个点，可以展开地毯式搜索．

-   [BFS（搜索）](../search/bfs.md)

#### 2.6.3 搜索优化

很多题目都可以用 DFS 来解决，而这个算法的复杂度显然是无法通过的．因此，需要一些优化使它跑得更快．这样的优化能够减少不可能成功的尝试，称为「剪枝」．BFS 相关的优化就要更加灵活了，但是基本思路和这里是一样的．

-   [DFS 剪枝优化](../search/opt.md)

### 2.7 数据结构入门

#### 2.7.1 线性数据结构

数组，链表，队列，栈，都是线性结构．巧用这些结构可以做出不少方便的事情．

-   [栈](../ds/stack.md)
-   [队列](../ds/queue.md)
-   [链表](../ds/linked-list.md)

#### 2.7.2 复杂数据结构

-   [树及二叉树](../graph/tree-basic.md)
-   [图的概念](../graph/concept.md)
-   [图的存储](../graph/save.md)

### 2.8 动态规划入门

动态规划（Dynamic Programming, DP）是一种通过把原问题分解为相对简单的子问题的方式求解复杂问题的方法．

由于动态规划并不是某种具体的算法，而是一种解决特定问题的方法，因此它会出现在各式各样的数据结构中，与之相关的题目种类也更为繁杂．

-   [动态规划简介](../dp/index.md)

#### 2.8.1 背包问题

即给出一个有限制容量的背包，选择放入若干有容量和价值的物品，求解如何放置能使得价值总和最大．这是阻挡很多 OIer 的第一道坎，从这里开始，算法就有些难以理解．

-   [背包 DP](../dp/knapsack.md)

#### 2.8.2 线性动态规划

在动态规划中，最难的部分之一就是设计状态，需要用到构造相关技巧．当你写出了状态和状态转移方程之后，完成一道动态规划的题目就不难了．

-   [构造](../basic/construction.md)
-   [动态规划基础](../dp/basic.md)

记忆化搜索是一种通过记录已经遍历过的状态的信息，从而避免对同一状态重复遍历的搜索实现方式．有的题目也可以使用记忆化搜索来降低思维难度．

因为记忆化搜索确保了每个状态只访问一次，它也是一种常见的动态规划实现方式．

-   [记忆化搜索](../dp/memo.md)

#### 2.8.3 复杂动态规划

区间类动态规划是线性动态规划的扩展，它在分阶段地划分问题时，与阶段中元素出现的顺序和由前一阶段的哪些元素合并而来有很大的关系．

-   [区间 DP](../dp/interval.md)

### 2.9 数学

#### 2.9.1 高精度算法

就算是 long long（或 int64）还不够怎么办？用高精度算法．本质上就是模拟了四则运算．

-   [高精度计算](../math/bignum.md)

#### 2.9.2 进制转换

在计算机中，除了二进制，比较常用的还有八进制和十六进制．有的时候学会运用正确的进制对解题也有很大帮助．

-   [进位制](../math/numeral-sys/base.md)

#### 2.9.3 位操作

位操作就是基于整数的二进制表示进行的运算．由于计算机内部就是以二进制来存储数据，位操作是相当快的．

基本的位操作共 6 种，分别为按位与、按位或、按位异或、按位取反、左移和右移．

-   [位操作](../math/bit.md)

#### 2.9.4 数论

-   [数论基础](../math/number-theory/basic.md)
-   [素数](../math/number-theory/prime.md)
-   [筛法](../math/number-theory/sieve.md)
-   [最大公因数](../math/number-theory/gcd.md)
-   [欧拉函数](../math/number-theory/euler-totient.md)
-   [分解质因数](../math/number-theory/pollard-rho.md)

#### 2.9.5 组合计数

-   [排列组合](../math/combinatorics/combination.md)
-   [抽屉原理](../math/combinatorics/drawer-principle.md)
-   [容斥原理](../math/combinatorics/inclusion-exclusion-principle.md)

***

至此，你就学习完了入门组范畴内的所有算法，但是想要掌握它们，你需要继续进行足够数量的刷题，以巩固你所学到的知识点．
