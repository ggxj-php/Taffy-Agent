

## lang/array.md

数组是存放相同类型对象的容器，数组中存放的对象没有名字，而是要通过其所在的位置访问．数组的大小是固定的，不能随意改变数组的长度．

## 定义数组

数组的声明形如 `a[d]`，其中，`a` 是数组的名字，`d` 是数组中元素的个数．在编译时，`d` 应该是已知的，也就是说，`d` 应该是一个整型的常量表达式．

```cpp
unsigned int d1 = 42;
const int d2 = 42;
int arr1[d1];  // 错误：d1 不是常量表达式
int arr2[d2];  // 正确：arr2 是一个长度为 42 的数组
```

不能将一个数组直接赋值给另一个数组：

```cpp
int arr1[3];
int arr2 = arr1;  // 错误
arr2 = arr1;      // 错误
```

应该尽量将较大的数组定义为全局变量．因为局部变量会被创建在栈区中，过大（大于栈的大小）的数组会爆栈，进而导致 RE．如果将数组声明在全局作用域中，就会在静态区中创建数组．

## 访问数组元素

可以通过下标运算符 `[]` 来访问数组内元素，数组的索引（即方括号中的值）从 0 开始．以一个包含 10 个元素的数组为例，它的索引为 0 到 9，而非 1 到 10．但在 OI 中，为了使用方便，我们通常会将数组开大一点，不使用数组的第一个元素，从下标 1 开始访问数组元素．

例 1：从标准输入中读取一个整数 $n$，再读取 $n$ 个数，存入数组中．其中，$n\leq 1000$．

```cpp
#include <iostream>
using namespace std;

int arr[1001];  // 数组 arr 的下标范围是 [0, 1001)

int main() {
  int n;
  cin >> n;
  for (int i = 1; i <= n; ++i) {
    cin >> arr[i];
  }
}
```

例 2：（接例 1）求和数组 `arr` 中的元素，并输出和．满足数组中所有元素的和小于等于 $2^{31} - 1$

```cpp
#include <iostream>
using namespace std;

int arr[1001];

int main() {
  int n;
  cin >> n;
  for (int i = 1; i <= n; ++i) {
    cin >> arr[i];
  }

  int sum = 0;
  for (int i = 1; i <= n; ++i) {
    sum += arr[i];
  }

  printf("%d\n", sum);
  return 0;
}
```

### 越界访问下标

数组的下标 $\mathit{idx}$ 应当满足 $0\leq \mathit{idx}< \mathit{size}$，如果下标不在这个范围内，则是未定义行为，会产生不可预料的后果，如段错误（Segmentation Fault），或者修改预期以外的变量等等．

## 多维数组

多维数组的实质是「数组的数组」，即外层数组的元素是数组．一个二维数组需要两个维度来定义：数组的长度和数组内元素的长度．访问二维数组时需要写出两个索引：

```cpp
int arr[3][4];  // 一个长度为 3 的数组，它的元素是「元素为 int 的长度为的 4
                // 的数组」
arr[2][1] = 1;  // 访问二维数组
```

我们经常使用嵌套的 for 循环来处理二维数组．

例：从标准输入中读取两个数 $n$ 和 $m$，分别表示黑白图片的高与宽，满足 $n,m\leq 1000$．对于接下来的 $n$ 行数据，每行有用空格分隔开的 $m$ 个数，代表这一位置的亮度值．现在我们读取这张图片，并将其存入二维数组中．

```cpp
const int MAXN = 1001;
int pic[MAXN][MAXN];
int n, m;

cin >> n >> m;
for (int i = 1; i <= n; ++i)
  for (int j = 1; j <= m; ++j) cin >> pic[i][j];
```

同样地，你可以定义三维、四维，以及更高维的数组．


## lang/basic.md

## 代码框架

如果你不想深究背后的原理，初学时可以直接将这个「框架」背下来：

```cpp
#include <cstdio>
#include <iostream>

int main() {
  // do something...
  return 0;
}
```

??? note "什么是 include？"
    `#include` 其实是一个预处理命令，意思为将一个文件「放」在这条语句处，被「放」的文件被称为头文件．也就是说，在编译时，编译器会「复制」头文件 `iostream` 中的内容，「粘贴」到 `#include <iostream>` 这条语句处．这样，你就可以使用 `iostream` 中提供的 `std::cin`、`std::cout`、`std::endl` 等对象了．
    
    如果你学过 C 语言，你会发现目前我们接触的 C++ 中的头文件一般都不带 `.h` 后缀，而那些 C 语言中的头文件 `xx.h` 都变成了 `cxx`，如 `stdio.h` 变成了 `cstdio`．因为 C++ 为了和 C 保持兼容，都直接使用了 C 语言中的头文件，为了区分 C++ 的头文件和 C 的头文件，使用了 `c` 前缀．
    
    一般来说，应当根据你需要编写的 C++ 程序的需要来确定你要 `#include` 哪些头文件．但如果你 `#include` 了多余的头文件，只会增加编译时间，几乎不会对运行时间造成影响．目前我们只接触到了 `iostream` 和 `cstdio` 两个头文件，如果你只需要 `scanf` 和 `printf`，就可以不用 `#include <iostream>`．
    
    可以 `#include` 自己写的头文件吗？答案是，可以．
    
    你可以自己写一个头文件，如：`myheader.h`．然后，将其放到和你的代码相同的目录里，再 `#include "myheader.h"` 即可．需要注意的是，自定义的头文件需要使用引号而非尖括号．当然，你也可以使用编译命令 `-I <header_file_path>` 来告诉编译器在哪找头文件，就不需要将头文件放到和代码相同的目录里了．

??? note "什么是 `main()`？"
    可以理解为程序运行时就会执行 `main()` 中的代码．
    
    实际上，`main` 函数是由系统或外部程序调用的．如，你在命令行中调用了你的程序，也就是调用了你程序中的 `main` 函数（在此之前先完成了全局 [变量](./var.md) 的构造）．
    
    最后的 `return 0;` 表示程序运行成功．默认情况下，程序结束时返回 0 表示一切正常，否则返回值表示错误代码（在 Windows 下这个错误代码的十六进制可以通过 [Windows Error Codes 网站](https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-erref/) 进行查询）．这个值返回给谁呢？其实就是调用你写的程序的系统或外部程序，它会在你的程序结束时接收到这个返回值．如果不写 `return` 语句的话，程序正常结束默认返回值也是 0．
    
    在 C 或 C++ 中，程序的返回值不为 0 会导致运行时错误（RE）．

## 注释

在 C++ 代码中，注释有两种写法：

1.  行内注释

    以 `//` 开头，行内位于其后的内容全部为注释．

2.  注释块

    以 `/*` 开头，`*/` 结尾，中间的内容全部为注释，可以跨行．

注释对程序运行没有影响，可以用来解释程序的意思，还可以在让某段代码不执行（但是依然保留在源文件里）．

在工程开发中，注释可以便于日后维护、他人阅读．

在 OI 中，很少有人写许多注释，但注释可以便于在写代码的时候理清思路，或者便于日后复习．而且，如果要写题解、教程的话，适量的注释可以便于读者阅读，理解代码的意图．希望各位同学能养成写注释的好习惯．

## 输入与输出

### `cin` 与 `cout`

```cpp
#include <iostream>

int main() {
  int x, y;                          // 声明变量
  std::cin >> x >> y;                // 读入 x 和 y
  std::cout << y << std::endl << x;  // 输出 y，换行，再输出 x
  return 0;                          // 结束主函数
}
```

???+ note "什么是变量？"
    可以参考 [变量](./var.md) 页面．

???+ note "什么是 `std`？"
    std 是 C++ 标准库所使用的 **命名空间**．使用命名空间是为了避免重名．
    
    关于命名空间的详细知识，可以参考 [命名空间](./namespace.md) 页面．

### `scanf` 与 `printf`

`scanf` 与 `printf` 其实是 C 语言提供的函数．大多数情况下，它们的速度比 `cin` 和 `cout` 更快，并且能够方便地控制输入输出格式．

???+ note "读入输出优化"
    `cin`/`cout` 和 `scanf`/`prinf` 的具体差别和读入输出优化，请参考 [读入、输出优化](../contest/io.md) 页面．

```cpp
#include <cstdio>

int main() {
  int x, y;
  scanf("%d%d", &x, &y);   // 读入 x 和 y
  printf("%d\n%d", y, x);  // 输出 y，换行，再输出 x
  return 0;
}
```

其中，`%d` 表示读入/输出的变量是一个有符号整型（`int` 型）的变量．

类似地：

1.  `%s` 表示字符串．
2.  `%c` 表示字符．
3.  `%lf` 表示双精度浮点数 (`double`)．
4.  `%lld` 表示长整型 (`long long`)．根据系统不同，也可能是 `%I64d`．
5.  `%u` 表示无符号整型  (`unsigned int`)．
6.  `%llu` 表示无符号长整型 (`unsigned long long`)，也可能是 `%I64u`．

除了类型标识符以外，还有一些控制格式的方式．许多都不常用，选取两个常用的列举如下：

1.  `%1d` 表示长度为 1 的整型．在读入时，即使没有空格也可以逐位读入数字．在输出时，若指定的长度大于数字的位数，就会在数字前用空格填充．若指定的长度小于数字的位数，就没有效果．
2.  `%.6lf`，用于输出，保留六位小数．

这两种运算符的相应地方都可以填入其他数字，例如 `%.3lf` 表示保留三位小数．

??? note "「双精度浮点数」，「长整型」是什么"
    这些表示变量的类型．和上面一样，会留到 [变量](./var.md) 中统一讲解．

??? note "为什么 `scanf` 中有 `&` 运算符？"
    在这里，`&` 实际上是取址运算符，返回的是变量在内存中的地址．而 scanf 接收的参数就是变量的地址．具体可能要在 [指针](./pointer.md) 才能完全清楚地说明，现在只需要记下来就好了．

??? note "什么是 `\n`？"
    `\n` 是一种 **转义字符**，表示换行．
    
    转义字符用来表示一些无法直接输入的字符，如由于字符串字面量中无法换行而无法直接输入的换行符，由于有特殊含义而无法输入的引号，由于表示转义字符而无法输入的反斜杠．
    
    常用的转义字符有：
    
    1.  `\t` 表示制表符．
    
    2.  `\\` 表示 `\`．
    
    3.  `\"` 表示 `"`．
    
    4.  `\0` 表示空字符，用来表示 C 风格字符串的结尾．
    
    5.  `\r` 表示回车．Linux 中换行符为 `\n`，Windows 中换行符为 `\r\n`．在 OI 中，如果输出需要换行，使用 `\n` 即可．但读入时，如果使用逐字符读入，可能会由于换行符造成一些问题，需要注意．例如，`gets` 将 `\n` 作为字符串结尾，这时候如果换行符是 `\r\n`，`\r` 就会留在字符串结尾．
    
    6.  特殊地，`%%` 表示 `%`，只能用在 `printf` 或 `scanf` 中，在其他字符串字面量中只需要简单使用 `%` 就好了．
    
    ??? note "什么是字面量？"
        「字面量」是在代码里直接作为一个值的程序段，例如 `3` 就是一个 `int` 字面量，`'c'` 就是一个 char 字面量．我们上面写的程序中的 `"hello world"` 也是一个字符串字面量．
        
        不加解释、毫无来由的字面量又被称为「魔术数」（magic number），如果代码需要被人阅读的话，这是一种十分不被推荐的行为．

## 一些扩展内容

### C++ 中的空白字符

在 C++ 中，所有空白字符（空格、制表符、换行），多个或是单个，都被视作是一样的．（当然，引号中视作字符串的一部分的不算．）

因此，你可以自由地使用任何代码风格（除了行内注释、字符串字面量与预处理命令必须在单行内），例如：

```cpp
--8<-- "docs/lang/code/basic/basic_1.cpp:main"
```

当然，这么做是不被推荐的．

一种也被广泛使用但与 **OI Wiki** 要求的码风不同的代码风格：

```cpp
--8<-- "docs/lang/code/basic/basic_2.cpp:main"
```

### `#define` 命令

`#define` 是一种预处理命令，用于定义宏，本质上是文本替换．例如：

```cpp
#include <iostream>
#define n 233

// n 不是变量，而是编译器会将代码中所有 n 文本替换为 233，但是作为标识符一部分的
// n 的就不会被替换，如 fn 不会被替换成 f233，同样，字符串内的也不会被替换

int main() {
  std::cout << n;  // 输出 233
  return 0;
}
```

??? note "什么是标识符？"
    标识符就是可以用作变量名的一组字符．例如，`abcd` 和 `abc1` 都是合法的标识符，而 `1a` 和 `c+b` 都不是合法的标识符．
    
    标识符由英文字母、下划线开头，中间只允许出现英文字母、下划线和数字．值得注意的是，关键字（如 `int`,`for`,`if`）不能用作标识符．

??? note "什么是预处理命令？"
    预处理命令就是预处理器所接受的命令，用于对代码进行初步的文本变换，比如 文件包含操作 `#include` 和 处理宏 `#define` 等，对 GCC 而言，默认不会保留预处理阶段的输出 `.i` 文件．可以用 `-E` 选项保留输出文件．

宏可以带参数，带参数的宏可以像函数一样使用：

```cpp
#include <iostream>
#define sum(x, y) ((x) + (y))
#define square(x) ((x) * (x))

int main() {
  std::cout << sum(1, 2) << ' ' << 2 * sum(3, 5) << std::endl;  // 输出 3 16
}
```

但是带参数的宏和函数有区别．因为宏是文本替换，所以会引发许多问题．如：

```cpp
#include <iostream>
#define sum(x, y) x + y
// 这里应当为 #define sum(x, y) ((x) + (y))
#define square(x) ((x) * (x))

int main() {
  std::cout << sum(1, 2) << ' ' << 2 * sum(3, 5) << std::endl;
  // 输出为 3 11，因为 #define 是文本替换，后面的语句被替换为了 2 * 3 + 5
  int i = 1;
  std::cout << square(++i) << ' ' << i;
  // 输出未定义，因为 ++i 被执行了两遍
  // 而同一个语句中多次修改同一个变量是未定义行为（有例外）
}
```

使用 `#define` 是有风险的（由于 `#define` 作用域是整个程序，因此可能导致文本被意外地替换，需要使用 `#undef` 及时取消定义），因此应谨慎使用．较为推荐的做法是：使用 `const` 限定符声明常量，使用函数代替宏．

但是，在 OI 中，`#define` 依然有用武之处（以下两种是不被推荐的用法，会降低代码的规范性）：

1.  `#define int long long`+`signed main()`．通常用于避免忘记开 long long 导致的错误，或是调试时排除忘开 long long 导致错误的可能性．（也可能导致增大常数甚至 TLE，或者因为爆空间而 MLE）
2.  `#define For(i, l, r) for (int i = (l); i <= (r); ++i)`、`#define pb push_back`、`#define mid ((l + r) / 2)`，用于减短代码长度．

不过，`#define` 也有优点，比如结合 `#ifdef` 等预处理指令有奇效，比如：

```cpp
#ifdef LINUX
// code for linux
#else
// code for other OS
#endif
```

可以在编译的时候通过 `-DLINUX` 来控制编译出的代码，而无需修改源文件．这还有一个优点：通过 `-DLINUX` 编译出的可执行文件里并没有其他操作系统的代码，那些代码在预处理的时候就已经被删除了．

`#define` 还能使用 `#`、`##` 运算符，极大地方便调试．


## lang/branch.md

一个程序默认是按照代码的顺序执行下来的，有时我们需要选择性的执行某些语句，这时候就需要分支的功能来实现．选择合适的分支语句可以提高程序的效率．

## if 语句

### 基本 if 语句

以下是基本 if 语句的结构．

```cpp
if (条件) {
  主体;
}
```

if 语句通过对条件进行求值，若结果为真（非 0），执行语句，否则不执行．

如果主体中只有单个语句的话，花括号可以省略．

### if...else 语句

```cpp
if (条件) {
  主体1;
} else {
  主体2;
}
```

if...else 语句和 if 语句类似，else 不需要再写条件．当 if 语句的条件满足时会执行 if 里的语句，if 语句的条件不满足时会执行 else 里的语句．同样，当主体只有一条语句时，可以省略花括号．

### else if 语句

```cpp
if (条件1) {
  主体1;
} else if (条件2) {
  主体2;
} else if (条件3) {
  主体3;
} else {
  主体4;
}
```

else if 语句是 if 和 else 的组合，对多个条件进行判断并选择不同的语句分支．在最后一条的 else 语句不需要再写条件．例如，若条件 1 为真，执行主体 1，条件 3 为真而条件 1 和条件 2 都为假，执行主体 3，所有的条件都为假才执行主体 4．

实际上，这一个语句相当于第一个 if 的 else 分句只有一个 if 语句，就将花括号省略之后放在一起了．如果条件相互之间是并列关系，这样写可以让代码的逻辑更清晰．

在逻辑上，大约相当于这一段话：

> 解一元二次方程的时候，方程的根与判别式的关系：
>
> -   如果 ($\Delta<0$)
>     方程无解；
> -   否则，如果 ($\Delta=0$)
>     方程有两个相同的实数解；
> -   否则
>     方程有两个不相同的实数解；

## switch 语句

```cpp
switch (选择句) {
  case 标签1:
    主体1;
  case 标签2:
    主体2;
  default:
    主体3;
}
```

switch 语句执行时，先求出选择句的值，然后根据选择句的值选择相应的标签，从标签处开始执行．其中，选择句必须是一个整数类型表达式，而标签都必须是整数类型的常量．例如：

```cpp
int i = 1;  // 这里的 i 的数据类型是整型 ，满足整数类型的表达式的要求

switch (i) {
  case 1:
    cout << "OI WIKI" << endl;
}
```

```cpp
char i = 'A';

// 这里的 i 的数据类型是字符型 ，但 char
// 也是属于整数的类型，满足整数类型的表达式的要求
switch (i) {
  case 'A':
    cout << "OI WIKI" << endl;
}
```

switch 语句中还要根据需求加入 break 语句进行中断，否则在对应的 case 被选择之后接下来的所有 case 里的语句和 default 里的语句都会被运行．具体例子可看下面的示例．

```cpp
char i = 'B';

switch (i) {
  case 'A':
    cout << "OI" << endl;
    break;

  case 'B':
    cout << "WIKI" << endl;

  default:
    cout << "Hello World" << endl;
}
```

以上代码运行后输出的结果为 `WIKI` 和 `Hello World`，如果不想让下面分支的语句被运行就需要 break 了，具体例子可看下面的示例．

```cpp
char i = 'B';

switch (i) {
  case 'A':
    cout << "OI" << endl;
    break;

  case 'B':
    cout << "WIKI" << endl;
    break;

  default:
    cout << "Hello World" << endl;
}
```

以上代码运行后输出的结果为 WIKI，因为 break 的存在，接下来的语句就不会继续被执行了．最后一个语句不需要 break，因为下面没有语句了．

处理入口编号不能重复，但可以颠倒．也就是说，入口编号的顺序不重要．各个 case（包括 default）的出现次序可任意．例如：

```cpp
char i = 'B';

switch (i) {
  case 'B':
    cout << "WIKI" << endl;
    break;

  default:
    cout << "Hello World" << endl;
    break;

  case 'A':
    cout << "OI" << endl;
}
```

switch 的 case 分句中也可以选择性的加花括号．不过要注意的是，如果需要在 switch 语句中定义变量，花括号是必须要加的．例如：

```cpp
char i = 'B';

switch (i) {
  case 'A': {
    int i = 1, j = 2;
    cout << "OI" << endl;
    ans = i + j;
    break;
  }

  case 'B': {
    int qwq = 3;
    cout << "WIKI" << endl;
    ans = qwq * qwq;
    break;
  }

  default: {
    cout << "Hello World" << endl;
  }
}
```

??? note "如何理解 switch"
    在上文中，用了大量「case 分句」，「case 子句」等用语，实际上，在底层实现中，switch 相当于一组跳转语句．也因此，有 Duff's Device 这种奇技淫巧，希望了解的人可以自行学习．


## lang/class.md

author: Ir1d, cjsoft, Lans1ot, JasonkayZK
类（class）是结构体的拓展，不仅能够拥有成员元素，还拥有成员函数．

在面向对象编程（OOP）中，对象就是类的实例，也就是变量．

C++ 中 `struct` 关键字定义的也是类，上文中的 **结构体** 的定义来自 C．因为某些历史原因，C++ 保留并拓展了 `struct`．

## 定义类

类使用关键字 `class` 或者 `struct` 定义，下文以 `class` 举例．

```cpp
class ClassName {
  ...
};

// Example:
class Object {
 public:
  int weight;
  int value;
} e[array_length];

const Object a;
Object b, B[array_length];
Object *c;
```

与使用 `struct` 大同小异．该例定义了一个名为 `Object` 的类．该类拥有两个成员元素，分别为 `weight,value`；并在 `}` 后使用该类型定义了一个数组 `e`．

定义类的指针形同 [`struct`](./struct.md)．

### 访问说明符

不同于 [`struct`](./struct.md) 中的举例，本例中出现了 `public`，这属于访问说明符．

-   `public`：该访问说明符之后的各个成员都可以被公开访问，简单来说就是无论 **类内** 还是 **类外** 都可以访问．
-   `protected`：该访问说明符之后的各个成员可以被 **类内**、派生类或者友元的成员访问，但类外 **不能访问**．
-   `private`：该访问说明符之后的各个成员 **只能** 被 **类内** 成员或者友元的成员访问，**不能** 被从类外或者派生类中访问．

对于 `struct`，它的所有成员都是默认 `public`．对于 `class`，它的所有成员都是默认 `private`．

??? note "关于友元以及派生类的基本概念"
    友元（`friend`）：使用 `friend` 关键字修饰某个函数或者类．可以使得在 **被修饰者** 在不成为成员函数或者成员类的情况下，访问该类的私有（`private`）或者受保护（`protected`）成员．简单来说就是只要带有这个类的 `friend` 标记，就可以访问私有或受保护的成员元素．
    
    派生类（`derived class`）：C++ 允许使用一个类作为 **基类**，并通过基类 **派生** 出 **派生类**．其中派生类（根据特定规则）继承基类中的成员变量和成员函数．可以提高代码的复用率．
    
    派生类似 "is" 的关系．如猫（派生类）"is" 哺乳动物（基类）．
    
    对于上面 `private` 和 `protected` 的区别，可以看做派生类可以访问基类的 `protected` 的元素（`public` 同），但不能访问 `private` 元素．

## 访问与修改成员元素的值

方法形同 [`struct`](./struct.md)

-   对于变量，使用 `.` 符号．
-   对于指针，使用 `->` 符号．

## 成员函数

成员函数，顾名思义．就是类中所包含的函数．

??? note "常见成员函数举例"
    ```cpp
    vector.push_back();
    set.insert();
    queue.empty();
    ```

```cpp
class Class_Name {
  ... type Function_Name(...) { ... }
};

// Example:
class Object {
 public:
  int weight;
  int value;

  void print() {
    cout << weight << endl;
    return;
  }

  void change_w(int);
};

void Object::change_w(int _weight) { weight = _weight; }

Object var;
```

该类有一个打印 `Object` 成员元素的函数，以及更改成员元素 `weight` 的函数．

和函数类似，对于成员函数，也可以先声明，在定义，如第十四行（声明处）以及十七行后（定义处）．

如果想要调用 `var` 的 `print` 成员函数，可以使用 `var.print()` 进行调用．

### 重载运算符

??? note "何为重载"
    C++ 允许编写者为名称相同的函数或者运算符指定不同的定义．这称为 **重载**（overload）．
    
    如果同名函数的参数种类、数量中的一者或多者两两不相同，则这些同名函数被看做是不同的．
    
    需要注意的是：如果两个同名函数的区别仅仅是返回值的类型不同则无法进行重载，此时编译器会拒绝编译！
    
    如果在调用时不会出现混淆（指调用某些同名函数时，无法根据所填参数种类和数量唯一地判断出被调用函数．常发生在具有默认参数的函数中），则编译器会根据调用时所填参数判断应调用函数．
    
    而上述过程被称作重载解析．

重载运算符，可以部分程度上代替函数，简化代码．

下面给出重载运算符的例子．

```cpp
class Vector {
 public:
  int x, y;

  Vector() : x(0), y(0) {}

  Vector(int _x, int _y) : x(_x), y(_y) {}

  int operator*(const Vector& other) const { return x * other.x + y * other.y; }

  Vector operator+(const Vector&) const;
  Vector operator-(const Vector&) const;
};

Vector Vector::operator+(const Vector& other) const {
  return Vector(x + other.x, y + other.y);
}

Vector Vector::operator-(const Vector& other) const {
  return Vector(x - other.x, y - other.y);
}

// 关于4,5行表示为x,y赋值，具体实现参见后文．
```

该例定义了一个向量类，并重载了 `* + -` 运算符，并分别代表向量内积，向量加，向量减．

重载运算符的模板大致可分为下面几部分．

```text
/*类定义内重载*/ 返回类型 operator符号(参数){...}

/*类定义内声明，在外部定义*/ 返回类型 类名称::operator符号(参数){...}
```

对于自定义的类，如果重载了某些运算符（一般来说只需要重载 `<` 这个比较运算符），便可以使用相应的 STL 容器或算法，如 [`sort`](../basic/stl-sort.md)．

如要了解更多，可参见「参考资料」第四条．

??? note "可以被重载的运算符"
    ```text
    +       -       *       /       %       ^       &
    |       ~       !       =       <       >       +=
    -=      *=      /=      %=      ^=      &=      |=
    <<      >>      >>=     <<=     ==      !=      <=
    >=      &&      ||      ++      --      ,       ->*
    ->      ()      []      new     new []  delete  delete []
    ```

### 在实例化变量时设定初始值

为完成这种操作，需要定义 **默认构造函数**(Default constructor)．

```cpp
class ClassName {
  ... ClassName(...)... { ... }
};

// Example:
class Object {
 public:
  int weight;
  int value;

  Object() {
    weight = 0;
    value = 0;
  }
};
```

该例定义了 `Object` 的默认构造函数，该函数能够在我们实例化 `Object` 类型变量时，将所有的成员元素初始化为 `0`．

若无显式的构造函数，则编译器认为该类有隐式的默认构造函数．换言之，若无定义任何构造函数，则编译器会自动生成一个默认构造函数，并会根据成员元素的类型进行初始化（与定义 内置类型 变量相同）．

在这种情况下，成员元素都是未初始化的，访问未初始化的变量的结果是未定义的（也就是说并不知道会返回何值）．

如果需要自定义初始化的值，可以再定义（或重载）构造函数．

??? note "关于定义（或重载）构造函数"
    一般来说，默认构造函数是不带参数的，这区别于构造函数．构造函数和默认构造函数的定义大同小异，只是参数数量上的不同．
    
    构造函数可以被重载（当然首次被叫做定义）．需要注意的是，如果已经定义了构造函数，那么编译器便不会再生成无参数的默认构造函数．这会可能会使试图以默认方法构造变量的行为编译失败（指不填入初始化参数）．

使用 C++11 或以上时，可以使用 `{}` 进行变量的初始化．

??? note "关于 `{}`"
    使用 `{}` 进行初始化，会用到 std::initializer\_list 这一个轻量代理对象进行初始化．
    
    初始化步骤大概如下
    
    1.  尝试寻找参数中有 `std::initializer_list` 的默认构造函数，如果有则调用（调用完后不再进行下面的查找，下同）．
    2.  尝试将 `{}` 中的元素填入其他构造参数，如果能将参数按照顺序填满（默认参数也算在内），则调用该默认构造函数．
    3.  若无 `private` 成员元素，则尝试在 **类外** 按照元素定义顺序或者下标顺序依次赋值．
    
    *上述过程只是完整过程的简化版本，详细内容参见 "参考资料九"*

```cpp
class Object {
 public:
  int weight;
  int value;

  Object() {
    weight = 0;
    value = 0;
  }

  Object(int _weight = 0, int _value = 0) {
    weight = _weight;
    value = _value;
  }

  // the same as
  // Object(int _weight,int _value):weight(_weight),value(_value) {}
};

// the same as
// Object::Object(int _weight,int _value){
//   weight = _weight;
//   value = _value;
// }
//}

Object A;        // ok
Object B(1, 2);  // ok
Object C{1, 2};  // ok,(C++11)
```

??? note "关于隐式类型转换"
    有时候会写出如下的代码
    
    ```cpp
    class Node {
     public:
      int var;
    
      Node(int _var) : var(_var) {}
    };
    
    Node a = 1;
    ```
    
    看上去十分不符合逻辑，一个 `int` 类型不可能转化为 `node` 类型．但是编译器不会进行 `error` 提示．
    
    原因是在进行赋值时，首先会将 `1` 作为参数调用 `node::node(int)`，然后调用默认的复制函数进行赋值．
    
    但大多数情况下，编写者会希望编译器进行报错．这时便可以在构造函数前追加 `explicit` 关键字．这会告诉编译器必须显式进行调用．
    
    ```cpp
    class Node {
     public:
      int var;
    
      explicit Node(int _var) : var(_var) {}
    };
    ```
    
    也就是说 `node a=1` 将会报错，但 `node a=node(1)` 不会．因为后者显式调用了构造函数．当然大多数人不会写出后者的代码，但此例足以说明 explicit 的作用．
    
    *不过在算法竞赛中，为了避免此类情况常用的是 "加强对代码的规范程度"，从源头上避免*

### 销毁

这是不可避免的问题．每一个变量都将在作用范围结束走向销毁．

但对于已经指向了动态申请的内存的指针来说，该指针在销毁时不会自动释放所指向的内存，需要手动释放动态内存．

如果结构体的成员元素包含指针，同样会遇到这种问题．需要用到析构函数来手动释放动态内存．

**析构** 函数（Destructor）将会在该变量被销毁时被调用．重载的方法形同构造函数，但需要在前加 `~`

*默认定义的析构函数通常对于算法竞赛已经足够使用，通常我们只有在成员元素包含指针时才会重载析构函数．*

```cpp
class Object {
 public:
  int weight;
  int value;
  int* ned;

  Object() {
    weight = 0;
    value = 0;
  }

  ~Object() { delete ned; }
};
```

### 为类变量赋值

默认情况下，赋值时会按照对应成员元素赋值的规则进行．也可以使用 `类名称()` 或 `类名称{}` 作为临时变量来进行赋值．

前者只是调用了复制构造函数（copy constructor），而后者在调用复制构造函数前会调用默认构造函数．

另外默认情况下，进行的赋值都是对应元素间进行 **浅拷贝**，如果成员元素中有指针，则在赋值完成后，两个变量的成员指针具有相同的地址．

```cpp
// A,tmp1,tmp2,tmp3类型为Object
tmp1 = A;
tmp2 = Object(...);
tmp3 = {...};
```

如需解决指针问题或更多操作，需要重载相应的构造函数．

*更多 构造函数（constructor）内容，参见「参考资料」第六条．*

## 参考资料

1.  [cppreference class](https://zh.cppreference.com/w/cpp/language/class)
2.  [cppreference access](https://zh.cppreference.com/w/cpp/language/access)
3.  [cppreference default\_constructor](https://zh.cppreference.com/w/cpp/language/default_constructor)
4.  [cppreference operator](https://zh.cppreference.com/w/cpp/language/operators)
5.  [cplusplus Data structures](http://www.cplusplus.com/doc/tutorial/structures/)
6.  [cplusplus Special members](http://www.cplusplus.com/doc/tutorial/classes2/)
7.  [C++11 FAQ](http://www.stroustrup.com/C++11FAQ.html)
8.  [cppreference Friendship and inheritance](http://www.cplusplus.com/doc/tutorial/inheritance/)
9.  [cppreference value initialization](https://zh.cppreference.com/w/cpp/language/value_initialization)


## lang/const.md

C++ 定义了一套完整的只读量定义方法，被 `const` 修饰的变量都是只读量，编译器会在编译期进行冲突检查，避免对只读量的修改，同时可能会执行一些优化．

在通常情况下，应该尽可能使用 `const` 修饰变量、参数，提高代码健壮性．

## `const` 类型限定符

### 常量

const 修饰的变量在初始化后不可改变值

```cpp
const int a = 0;  // a 的类型为 const int

// a = 1; // 不能修改常量
```

### 常量引用、常量指针

常量引用和常量指针均限制了对指向的值的修改

```cpp
int a = 0;
const int b = 0;

int *p1 = &a;
*p1 = 1;
const int *p2 = &a;
// *p2 = 2; // 不能通过常量指针修改变量
// int *p3 = &b; // 不能用 int* 指向 const int 变量
const int *p4 = &b;

int &r1 = a;
r1 = 1;
const int &r2 = a;
// r2 = 2; // 不能通过常量引用修改变量
// int &p3 = b; // 不能用 int& 引用 const int变量
const int &r4 = b;
```

另外需要区分开的是常量指针（`const t*`）和指针常量（`t* const`），例如下列声明

```cpp
int* const p1;  // 指针常量，初始化后指向地址不可改，可更改指向的值
const int* p2;  // 常量指针，解引用的值不可改，可指向其他 int 变量
const int* const p3;  // 常量指针常量，值不可改，指向地址不可改

// 使用别名能更好提高可读性
using const_int = const int;
using ptr_to_const_int = const_int*;
using const_ptr_to_const_int = const ptr_to_const_int;
```

在函数参数里使用 `const` 限定参数类型，可以避免变量被错误地修改，同时增加代码可读性

```cpp
void sum(const std::vector<int> &data, int &total) {
  for (auto iter = data.begin(); iter != data.end(); ++iter)
    total += *iter;  // iter 是迭代器，解引用后的类型是 const int
}
```

## `const` 成员函数

类型中 `const` 限定的成员函数，可以用来限制对成员的修改．

```cpp
#include <iostream>

struct ConstMember {
  int s = 0;

  void func() { std::cout << "General Function" << std::endl; }

  void constFunc1() const { std::cout << "Const Function 1" << std::endl; }

  void constFunc2(int ss) const {
    // func(); // const 成员函数不能调用非 const 成员函数
    constFunc1();

    // s = ss; // const 成员函数不能修改成员变量
  }
};

int main() {
  int b = 1;
  ConstMember c{};
  const ConstMember d = c;
  // d.func(); // 常量不能调用非 const 成员函数
  d.constFunc2(b);
  return 0;
}
```

## 常量表达式 `constexpr`（C++11）

常量表达式是指编译时能计算出结果的表达式，`constexpr` 则要求编译器能在编译时求得函数或变量的值．

编译时计算能允许更好的优化，比如将结果硬编码到汇编中，消除运行时计算开销．与 `const` 的带来的优化不同，当 `constexpr` 修饰的变量满足常量表达式的条件，就强制要求编译器在编译时计算出结果而非运行时．

???+ note "更直观的理解是把 `const` 理解成「只读」，`constexpr` 理解成「不可变」"
    ```cpp
    constexpr int a = 10;  // 直接定义常量
    
    constexpr int FivePlus(int x) { return 5 + x; }
    
    void test(const int x) {
      std::array<int, x> c1;            // 错误，x在编译时不可知
      std::array<int, FivePlus(6)> c2;  // 可行，FivePlus编译时可知
    }
    ```

以下例子很好说明了 `const` 和 `constexpr` 的区别，代码使用递归实现计算斐波那契数列，并用控制流输出．

???+ note "实现"
    ```cpp
    #include <iostream>
    
    using namespace std;
    
    constexpr unsigned fib0(unsigned n) {
      return n <= 1 ? 1 : (fib0(n - 1) + fib0(n - 2));
    }
    
    unsigned fib1(unsigned n) { return n <= 1 ? 1 : (fib1(n - 1) + fib1(n - 2)); }
    
    int main() {
      constexpr auto v0 = fib0(9);
      const auto v1 = fib1(9);
    
      cout << v0;
      cout << ' ';
      cout << v1;
    }
    ```

???+ note "编译后的可能的汇编代码（使用 Compiler Explorer，Clang 19）"
    ```nasm
    fib1(unsigned int):
            push    r14
            push    rbx
            push    rax
            mov     ebx, 1
            cmp     edi, 2
            jb      .LBB0_4
            mov     r14d, edi
            xor     ebx, ebx
    .LBB0_2:
            lea     edi, [r14 - 1]
            call    fib1(unsigned int)
            add     r14d, -2
            add     ebx, eax
            cmp     r14d, 1
            ja      .LBB0_2
            inc     ebx
    .LBB0_4:
            mov     eax, ebx
            add     rsp, 8
            pop     rbx
            pop     r14
            ret
    
    main:
            push    r14
            push    rbx
            push    rax
            mov     edi, 9
            call    fib1(unsigned int) # `v1` 的初始化进行了函数调用
            mov     ebx, eax
            mov     r14, qword ptr [rip + std::__1::cout@GOTPCREL]
            mov     rdi, r14
            mov     esi, 55 # `v0` 被最终计算结果替代
            call    std::__1::basic_ostream<char, std::__1::char_traits<char>>::operator<<(unsigned int)@PLT
            mov     byte ptr [rsp + 7], 32
            lea     rsi, [rsp + 7]
            mov     edx, 1
            mov     rdi, r14
            call    std::__1::basic_ostream<char, std::__1::char_traits<char>>& std::__1::__put_character_sequence[abi:ne200000]<char, std::__1::char_traits<char>>(std::__1::basic_ostream<char, std::__1::char_traits<char>>&, char const*, unsigned long)
            mov     rdi, r14
            mov     esi, ebx # 读取了变量值
            call    std::__1::basic_ostream<char, std::__1::char_traits<char>>::operator<<(unsigned int)@PLT
            xor     eax, eax
            add     rsp, 8
            pop     rbx
            pop     r14
            ret
    ```

`constexpr` 修饰的 `fib0` 函数在唯一的调用处用了常量参数，使得整个函数仅在编译期运行．由于函数没有运行时执行，编译器也就判断不需要生成汇编代码．

在同时注意到汇编中，`v0` 没有初始化代码，在调用 `cout` 输出 `v0` 的代码中，`v0` 已被最终结算结果替代，说明变量值已在编译时求出，优化掉了运行时运算．
而 `v1` 的初始化还是普通的 `fib1` 递归调用．

所以 `constexpr` 可以用来替换宏定义的常量，规避 [宏定义的风险](./basic.md#define-命令)．

算法题中可以使用 `constexpr` 存储数据规模较小的变量，以消除对应的运行时计算开销．尤为常见在「[打表](../contest/dictionary.md)」技巧中，使用 `constexpr` 修饰的数组等容器存储答案．

???+ note "编译时计算量过大会导致编译错误"
    编译器会限制编译时计算的开销，如果计算量过大会导致无法通过编译，应该考虑使用 `const`．
    
    ```cpp
    #include <iostream>
    
    using namespace std;
    
    constexpr unsigned long long fib(unsigned long long i) {
      return i <= 2 ? i : fib(i - 2) + fib(i - 1);
    }
    
    int main() {
      // constexpr auto v = fib(32); evaluation exceeded maximum depth
      const auto v = fib(32);
      cout << v;
      return 0;
    }
    ```

???+ note "使用 constexpr 时 Clang 给出的编译错误"
    ```text
    <source>:10:20: error: constexpr variable 'v' must be initialized by a constant expression
        10 |     constexpr auto v = fib(32);
        |                    ^   ~~~~~~~~~~~~
    <source>:6:25: note: constexpr evaluation exceeded maximum depth of 512 calls
        6 |     return i <= 2 ? i : fib(i - 2) + fib(i - 1);
        |                         ^
    <source>:6:25: note: in call to 'fib(32)'
        6 |     return i <= 2 ? i : fib(i - 2) + fib(i - 1);
        |                         ^~~~~~~~~~
    <source>:6:25: note: in call to ...
    ```

## 参考资料

-   [C++ 关键字——const](https://zh.cppreference.com/w/cpp/keyword/const)
-   [C++ 关键字——constexpr](https://zh.cppreference.com/w/cpp/keyword/constexpr)


## lang/cpp-other-langs.md

本文介绍 C++ 与其他常用语言的区别，重点介绍 C 与 C++ 之间重要的或者容易忽略的区别．尽管 C++ 几乎是 C 的超集，C/C++ 代码混用一般也没什么问题，但是了解 C/C++ 间比较重要的区别可以避免碰到一些奇怪的 bug．如果你是以 C 为主力语言的 OIer，那么本文也能让你更顺利地上手 C++．C++ 相比 C 增加的独特特性可以阅读 [C++ 进阶](./class.md) 部分的教程．此外，本文也简要介绍了 Python, Java 和 C++ 的区别．

## C 与 C++ 的区别

### 宏与模板

C++ 的模板在设计之初的一个用途就是用来替换宏定义．学会模板编程是从 C 迈向 C++ 的重要一步．模板不同于宏的文字替换，在编译时会得到更全面的编译器检查，便于编写更健全的代码．模板特性在 C++11 后支持了可变长度的模板参数表，可以用来替代 C 中的可变长度函数并保证类型安全．

### 指针与引用

C++ 中你仍然可以使用 C 风格的指针，但是对于变量传递而言，更推荐使用 C++ 的 [引用](./reference.md) 特性来实现类似的功能．由于引用指向的对象不能为空，因此可以避免一些空地址访问的问题．不过指针由于其灵活性，也仍然有其用武之地．值得一提的是，C 中的 `NULL` 空指针在 C++11 起有类型安全的替代品 `nullptr`．引用和指针之间可以通过 [`*` 和 `&` 运算符](./op.md) 相互转换．

### bool

另请参阅 [布尔类型](var.md#布尔类型)．

与 C++ 不同的是，C 语言最初并没有布尔类型．

C99 标准加入了 `_Bool` 关键字（以及等效的 `bool` 宏）以及 `true` 和 `false` 两个宏．如果需要使用 `bool`，`true`，`false` 这三个宏，需要在程序中引入 `stdbool.h` 头文件．而使用 `_Bool` 则不需要引入任何额外头文件．

```c
bool x = true;  // 需要引入 stdbool.h
_Bool x = 1;    // 不需要引入 stdbool.h
```

C23 起，`true`,`false` 和 `bool` 成为 C 语言中的关键字，使用它们不需要再引入 `stdbool.h` 头文件，同时保留 `_Bool` 作为 `bool` 的替代拼写形式[^boolean-keyword]．

下表展示了 C 语言不同标准下，bool 类型支持的变化情况（作为对照，加入了 C++ 的支持情况）：

| 语言标准         | `bool`                            | `true`/`false`                                        | `_Bool`                   |
| ------------ | --------------------------------- | ----------------------------------------------------- | ------------------------- |
| C89          | /                                 | /                                                     | 保留[^reserved-identifiers] |
| C99 起，C23 以前 | 宏，与 `_Bool` 等价，需要 `stdbool.h` 头文件 | 宏，`true` 与 `1` 等价，`false` 与 `0` 等价，需要 `stdbool.h` 头文件 | 关键字                       |
| C23 起        | 关键字                               | 关键字                                                   | 关键字 `bool` 的替代拼写形式        |
| C++          | 关键字                               | 关键字                                                   | 保留[^reserved-identifiers] |

### struct

尽管在 C 和 C++ 中都有 struct 的概念，但是他们对应的东西是不能混用的！C 中的 struct 用来描述一种固定的内存组织结构，而 C++ 中的 struct 就是一种类，**它与类唯一的区别就是它的成员和继承行为默认是 public 的**，而一般类的默认成员是 private 的．这一点在写 C/C++ 混合代码时尤其致命．

另外，声明 struct 时 C++ 也不需要像 C 那么繁琐，C 版本：

```c
typedef struct Node_t {
  struct Node_t *next;
  int key;
} Node;
```

C++ 版本

```cpp
struct Node {
  Node *next;
  int key;
};
```

### const

const 在 C 中只有限定变量不能修改的功能，而在 C++ 中，由于大量新特性的出现，const 也被赋予的更多用法．C 中的 const 在 C++ 中的继任者是 constexpr，而 C++ 中的 const 的用法请参见 [常值](./const.md) 页面的说明．

### 内存分配

C++ 中新增了 `new` 和 `delete` 关键字用来在「自由存储区」上分配空间，这个自由存储区可以是堆也可以是静态存储区，他们是为了配合「类」而出现的．其中 `delete[]` 还能够直接释放动态数组的内存，非常方便．`new` 和 `delete` 关键字会调用类型的构造函数和析构函数，相比 C 中的 `malloc()`、`realloc()`、`free()` 函数，他们对类型有更完善的支持，但是效率不如 C 中的这些函数．

简而言之，如果你需要动态分配内存的对象是基础类型或他们的数组，那么你可以使用 `malloc()` 进行更高效的内存分配；但如果你新建的对象是非基础的类型，那么建议使用 `new` 以获得安全性检查．值得注意的是尽管 `new` 和 `malloc()` 都是返回指针，但是 `new` 出来的指针 **只能** 用 `delete` 回收，而 `malloc()` 出来的指针也只能用 `free()` 回收，否则会有内存泄漏的风险．

### 变量声明

C99 前，C 的变量声明必须位于语句块开头，C++ 和 C99 后无此限制．

### 可变长数组

C99 后 C 语言支持 VLA（可变长数组），C++ 始终不支持．

### 结构体初始化

C99 后 C 语言支持结构体的 [指派符初始化](https://en.cppreference.com/w/c/language/struct_initialization)（但是在 C11 中为可选特性），C++ 直到 C++20 才支持有顺序要求的指派符初始化，且 C 语言支持的乱序、嵌套、与普通初始化器混用、数组的指派符初始化特性 C++ 都不支持[^cpp-designated-init]．

### 注释语法

C++ 风格单行注释 `//`，C 于 C99 前不支持．

## Python 与 C++ 的区别

Python 是目前机器学习界最常用的语言．相比于 C++，Python 的优势在于易于学习，易于实践．Python 有着更加简单直接的语法，比如在定义变量时，不需要提前声明变量类型．但是，这样的简单也是有代价的．Python 相比于 C++ 牺牲了性能．C++ 几乎适用于包括嵌入式系统的所有平台，并且有着更快的执行速度，但是 Python 只可以在某些支持高级语言的平台上使用．C++ 更接近底层，所以可以用来进行编写操作系统．

## Java 与 C++ 的区别

Java 与 C++ 都是面向对象的语言，都使用了面向对象的思想（封装、继承、多态），由于面向对象有许多非常好的特性（继承、组合等），因此二者有很好的可重用性．所以相比于 Python，Java 和 C++ 更加类似．

二者最大的区别在于 Java 有 JVM 的机制．JVM 全称是 Java Virtual Machine，中文意为 Java 虚拟机．Java 语言的一个非常重要的特点就是与平台的无关性．而使用 Java 虚拟机是实现这一特点的关键．一般的高级语言如果要在不同的平台上运行，至少需要编译成不同的目标代码．而引入 Java 语言虚拟机后，Java 语言在不同平台上运行时不需要重新编译．Java 语言使用 Java 虚拟机屏蔽了与具体平台相关的信息，使得 Java 语言编译程序只需生成在 Java 虚拟机上运行的目标代码（字节码），就可以在多种平台上不加修改地运行．

因为这个特点，Java 经常被用于需要移植到不同平台程序的开发．但是也由于编译 Java 程序时需要从字节码开始，所以 Java 的性能没有 C++ 好．

## 参考资料

[^cpp-designated-init]: <https://en.cppreference.com/w/cpp/language/aggregate_initialization>

[^boolean-keyword]: <https://www.open-std.org/jtc1/sc22/wg14/www/docs/n3054.pdf>．

[^reserved-identifiers]: C 和 C++ 均规定，以一个下划线跟着一个大写字母开头的标识符是被保留的，详见 <https://en.cppreference.com/w/c/language/identifier>．


## lang/csl/algorithm.md

STL 提供了大约 100 个实现算法的模版函数，基本都包含在 `<algorithm>` 之中，还有一部分包含在 `<numeric>` 和 `<functional>`．完备的函数列表请 [参见参考手册](https://zh.cppreference.com/w/cpp/algorithm)，排序相关的可以参考 [排序内容的对应页面](../../basic/stl-sort.md)．

-   `find`：顺序查找．`find(v.begin(), v.end(), value)`，其中 `value` 为需要查找的值．

-   `reverse`：翻转数组、字符串．`reverse(v.begin(), v.end())` 或 `reverse(a + begin, a + end)`．

-   `unique`：去除容器中相邻的重复元素．`unique(ForwardIterator first, ForwardIterator last)`，返回值为指向 **去重后** 容器结尾的迭代器，原容器大小不变．与 `sort` 结合使用可以实现完整容器去重．

-   `random_shuffle`：随机地打乱数组．`random_shuffle(v.begin(), v.end())` 或 `random_shuffle(v + begin, v + end)`．

    ???+ warning "`random_shuffle` 函数在最新 C++ 标准中已被移除"
        `random_shuffle` 自 C++14 起被弃用，C++17 起被移除．
        
        在 C++11 以及更新的标准中，您可以使用 `shuffle` 函数代替原来的 `random_shuffle`．使用方法为 `shuffle(v.begin(), v.end(), rng)`（最后一个参数传入的是使用的随机数生成器，一般情况使用以真随机数生成器 [`random_device`](https://zh.cppreference.com/w/cpp/numeric/random/random_device) 播种的梅森旋转伪随机数生成器 [`mt19937`](https://zh.cppreference.com/w/cpp/numeric/random/mersenne_twister_engine)）．
        
        ```cpp
        // #include <random>
        std::mt19937 rng(std::random_device{}());
        std::shuffle(v.begin(), v.end(), rng);
        ```

-   `sort`：排序．`sort(v.begin(), v.end(), cmp)` 或 `sort(a + begin, a + end, cmp)`，其中 `end` 是排序的数组最后一个元素的后一位，`cmp` 为自定义的比较函数．

-   `stable_sort`：稳定排序，用法同 `sort()`．

-   `nth_element`：按指定范围进行分类，即找出序列中第 $n$ 大的元素，使其左边均为小于它的数，右边均为大于它的数．`nth_element(v.begin(), v.begin() + n, v.end(), cmp)` 或 `nth_element(a + begin, a + begin + n, a + end, cmp)`．

-   `binary_search`：二分查找．`binary_search(v.begin(), v.end(), value)`，其中 `value` 为需要查找的值．

-   `merge`：将两个（已排序的）序列 **有序合并** 到第三个序列的 **插入迭代器** 上．`merge(v1.begin(), v1.end(), v2.begin(), v2.end() ,back_inserter(v3))`．

-   `inplace_merge`：将两个（已按小于运算符排序的）：`[first,middle), [middle,last)` 范围 **原地合并为一个有序序列**．`inplace_merge(v.begin(), v.begin() + middle, v.end())`．

-   `lower_bound`：在一个有序序列中进行二分查找，返回指向第一个 **大于等于**  $x$ 的元素的位置的迭代器．如果不存在这样的元素，则返回尾迭代器．`lower_bound(v.begin(),v.end(),x)`．

-   `upper_bound`：在一个有序序列中进行二分查找，返回指向第一个 **大于**  $x$ 的元素的位置的迭代器．如果不存在这样的元素，则返回尾迭代器．`upper_bound(v.begin(),v.end(),x)`．

    ???+ warning "`lower_bound` 和 `upper_bound` 的时间复杂度"
        在一般的数组里，这两个函数的时间复杂度均为 $O(\log n)$，但在 `set` 等关联式容器中，直接调用 `lower_bound(s.begin(),s.end(),val)` 的时间复杂度是 $O(n)$ 的．
        
        `set` 等关联式容器中已经封装了 `lower_bound` 等函数（像 `s.lower_bound(val)` 这样），这样调用的时间复杂度是 $O(\log n)$ 的．

-   `next_permutation`：将当前排列更改为 **全排列中的下一个排列**．如果当前排列已经是 **全排列中的最后一个排列**（元素完全从大到小排列），函数返回 `false` 并将排列更改为 **全排列中的第一个排列**（元素完全从小到大排列）；否则，函数返回 `true`．`next_permutation(v.begin(), v.end())` 或 `next_permutation(v + begin, v + end)`．

-   `prev_permutation`：将当前排列更改为 **全排列中的上一个排列**．用法同 `next_permutation`．

-   `partial_sum`：求前缀和．设源容器为 $x$，目标容器为 $y$，则令 $y[i]=x[0]+x[1]+\dots+x[i]$．`partial_sum(src.begin(), src.end(), back_inserter(dst))`．

### 使用样例

-   使用 `next_permutation` 生成 $1$ 到 $9$ 的全排列．例题：[Luogu P1706 全排列问题](https://www.luogu.com.cn/problem/P1706)

    ???+ note "实现"
        ```cpp
        int N = 9, a[] = {1, 2, 3, 4, 5, 6, 7, 8, 9};
        do {
          for (int i = 0; i < N; i++) cout << a[i] << " ";
          cout << endl;
        } while (next_permutation(a, a + N));
        ```
-   使用 `lower_bound` 与 `upper_bound` 查找有序数组 $a$ 中小于 $x$，等于 $x$，大于 $x$ 元素的分界线．

    ???+ note "实现"
        ```cpp
        int N = 10, a[] = {1, 1, 2, 4, 5, 5, 7, 7, 9, 9}, x = 5;
        int i = lower_bound(a, a + N, x) - a, j = upper_bound(a, a + N, x) - a;
        // a[0] ~ a[i - 1] 为小于x的元素， a[i] ~ a[j - 1] 为等于x的元素，
        // a[j] ~ a[N - 1] 为大于x的元素
        cout << i << " " << j << endl;
        ```
-   使用 `partial_sum` 求解 $src$ 中元素的前缀和，并存储于 $dst$ 中．

    ???+ note "实现"
        ```cpp
        vector<int> src = {1, 2, 3, 4, 5}, dst;
        // 求解src中元素的前缀和，dst[i] = src[0] + ... + src[i]
        // back_inserter 函数作用在 dst 容器上，提供一个迭代器
        partial_sum(src.begin(), src.end(), back_inserter(dst));
        for (unsigned int i = 0; i < dst.size(); i++) cout << dst[i] << " ";
        ```
-   使用 `lower_bound` 查找有序数组 $a$ 中最接近 $x$ 的元素．例题：[UVa10487 Closest Sums](https://onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&category=16&page=show_problem&problem=1428)

    ???+ note "实现"
        ```cpp
        int N = 10, a[] = {1, 1, 2, 4, 5, 5, 8, 8, 9, 9}, x = 6;
        // lower_bound将返回a中第一个大于等于x的元素的地址，计算出的i为其下标
        int i = lower_bound(a, a + N, x) - a;
        // 在以下两种情况下，a[i] (a中第一个大于等于x的元素) 即为答案：
        // 1. a中最小的元素都大于等于x；
        // 2. a中存在大于等于x的元素，且第一个大于等于x的元素 (a[i])
        // 相比于第一个小于x的元素 (a[i - 1]) 更接近x；
        // 否则，a[i - 1] (a中第一个小于x的元素) 即为答案
        if (i == 0 || (i < N && a[i] - x < x - a[i - 1]))
          cout << a[i];
        else
          cout << a[i - 1];
        ```
-   使用 `sort` 与 `unique` 查找数组 $a$ 中 **第 $k$ 小的值**（注意：重复出现的值仅算一次，因此本题不是求解第 $k$ 小的元素）．例题：[Luogu P1138 第 k 小整数](https://www.luogu.com.cn/problem/P1138)

    ???+ note "实现"
        ```cpp
        int N = 10, a[] = {1, 3, 3, 7, 2, 5, 1, 2, 4, 6}, k = 3;
        sort(a, a + N);
        // unique将返回去重之后数组最后一个元素之后的地址，计算出的cnt为去重后数组的长度
        int cnt = unique(a, a + N) - a;
        cout << a[k - 1];
        ```


## lang/csl/associative-container.md

## `set`

`set` 是关联容器，含有键值类型对象的已排序集，搜索、移除和插入拥有对数复杂度．`set` 内部通常采用 [红黑树](../../ds/rbtree.md) 实现．[平衡二叉树](../../ds/bst.md) 的特性使得 `set` 非常适合处理需要同时兼顾查找、插入与删除的情况．

和数学中的集合相似，`set` 中不会出现值相同的元素．如果需要有相同元素的集合，需要使用 `multiset`．`multiset` 的使用方法与 `set` 的使用方法基本相同．

### 插入与删除操作

-   `insert(x)` 当容器中没有等价元素的时候，将元素 x 插入到 `set` 中．
-   `erase(x)` 删除值为 x 的 **所有** 元素，返回删除元素的个数．
-   `erase(pos)` 删除迭代器为 pos 的元素，要求迭代器必须合法．
-   `erase(first,last)` 删除迭代器在 $[first,last)$ 范围内的所有元素．
-   `clear()` 清空 `set`．

???+ note "insert 函数的返回值"
    insert 函数的返回值类型为 `pair<iterator, bool>`，其中 iterator 是一个指向所插入元素（或者是指向等于所插入值的原本就在容器中的元素）的迭代器，而 bool 则代表元素是否插入成功，由于 `set` 中的元素具有唯一性质，所以如果在 `set` 中已有等值元素，则插入会失败，返回 false，否则插入成功，返回 true；`map` 中的 insert 也是如此．

### 迭代器

`set` 提供了以下几种迭代器：

1.  `begin()/cbegin()`   
    返回指向首元素的迭代器，其中 `*begin = front`．
2.  `end()/cend()`   
    返回指向数组尾端占位符的迭代器，注意是没有元素的．
3.  `rbegin()/crbegin()`   
    返回指向逆向数组的首元素的逆向迭代器，可以理解为正向容器的末元素．
4.  `rend()/crend()`   
    返回指向逆向数组末元素后一位置的迭代器，对应容器首的前一个位置，没有元素．

以上列出的迭代器中，含有字符 `c` 的为只读迭代器，你不能通过只读迭代器去修改 `set` 中的元素的值．如果一个 `set` 本身就是只读的，那么它的一般迭代器和只读迭代器完全等价．只读迭代器自 C++11 开始支持．

### 查找操作

-   `count(x)` 返回 `set` 内键为 x 的元素数量．
-   `find(x)` 在 `set` 内存在键为 x 的元素时会返回该元素的迭代器，否则返回 `end()`．
-   `lower_bound(x)` 返回指向首个不小于给定键的元素的迭代器．如果不存在这样的元素，返回 `end()`．
-   `upper_bound(x)` 返回指向首个大于给定键的元素的迭代器．如果不存在这样的元素，返回 `end()`．
-   `empty()` 返回容器是否为空．
-   `size()` 返回容器内元素个数．

???+ warning "`lower_bound` 和 `upper_bound` 的时间复杂度"
    `set` 自带的 `lower_bound` 和 `upper_bound` 的时间复杂度为 $O(\log n)$．
    
    但使用 `algorithm` 库中的 `lower_bound` 和 `upper_bound` 函数对 `set` 中的元素进行查询，时间复杂度为 $O(n)$．

???+ warning "`nth_element` 的时间复杂度"
    `set` 没有提供自带的 `nth_element`．使用 `algorithm` 库中的 `nth_element` 查找第 $k$ 大的元素时间复杂度为 $O(n)$．
    
    如果需要实现平衡二叉树所具备的 $O(\log n)$ 查找第 $k$ 大元素的功能，需要自己手写平衡二叉树或权值线段树，或者选择使用 pb\_ds 库中的平衡二叉树．

### 使用样例

#### `set` 在贪心中的使用

在贪心算法中经常会需要出现类似 **找出并删除最小的大于等于某个值的元素**．这种操作能轻松地通过 `set` 来完成．

```cpp
// 现存可用的元素
set<int> available;
// 需要大于等于的值
int x;

// 查找最小的大于等于x的元素
set<int>::iterator it = available.lower_bound(x);
if (it == available.end()) {
  // 不存在这样的元素，则进行相应操作……
} else {
  // 找到了这样的元素，将其从现存可用元素中移除
  available.erase(it);
  // 进行相应操作……
}
```

## `map`

`map` 是有序键值对容器，它的元素的键是唯一的．搜索、移除和插入操作拥有对数复杂度．`map` 通常实现为 [红黑树](../../ds/rbtree.md)．

设想如下场景：现在需要存储一些键值对，例如存储学生姓名对应的分数：`Tom 0`，`Bob 100`，`Alan 100`．但是由于数组下标只能为非负整数，所以无法用姓名作为下标来存储，这个时候最简单的办法就是使用 STL 中的 `map`．

`map` 重载了 `operator[]`，可以用任意定义了 `operator <` 的类型作为下标（在 `map` 中叫做 `key`，也就是索引）：

```cpp
map<Key, T> yourMap;
```

其中，`Key` 是键的类型，`T` 是值的类型，下面是使用 `map` 的实例：

```cpp
map<string, int> mp;
```

`map` 中不会存在键相同的元素，`multimap` 中允许多个元素拥有同一键．`multimap` 的使用方法与 `map` 的使用方法基本相同．

??? warning "Warning"
    正是因为 `multimap` 允许多个元素拥有同一键的特点，`multimap` 并没有提供给出键访问其对应值的方法．

### 插入与删除操作

-   可以直接通过下标访问来进行查询或插入操作．例如 `mp["Alan"]=100`．
-   通过向 `map` 中插入一个类型为 `pair<Key, T>` 的值可以达到插入元素的目的，例如 `mp.insert(pair<string,int>("Alan",100));`；
-   `erase(key)` 函数会删除键为 `key` 的 **所有** 元素．返回值为删除元素的数量．
-   `erase(pos)`: 删除迭代器为 pos 的元素，要求迭代器必须合法．
-   `erase(first,last)`: 删除迭代器在 $[first,last)$ 范围内的所有元素．
-   `clear()` 函数会清空整个容器．

???+ note "下标访问中的注意事项"
    在利用下标访问 `map` 中的某个元素时，如果 `map` 中不存在相应键的元素，会自动在 `map` 中插入一个新元素，并将其值设置为默认值（对于整数，值为零；对于有默认构造函数的类型，会调用默认构造函数进行初始化）．
    
    当下标访问操作过于频繁时，容器中会出现大量无意义元素，影响 `map` 的效率．因此一般情况下推荐使用 `find()` 函数来寻找特定键的元素．

### 查询操作

-   `count(x)`: 返回容器内键为 x 的元素数量．复杂度为 $O(\log(size)+ans)$（关于容器大小对数复杂度，加上匹配个数）．
-   `find(x)`: 若容器内存在键为 x 的元素，会返回该元素的迭代器；否则返回 `end()`．
-   `lower_bound(x)`: 返回指向首个不小于给定键的元素的迭代器．
-   `upper_bound(x)`: 返回指向首个大于给定键的元素的迭代器．若容器内所有元素均小于或等于给定键，返回 `end()`．
-   `empty()`: 返回容器是否为空．
-   `size()`: 返回容器内元素个数．

### 使用样例

#### `map` 用于存储复杂状态

在搜索中，我们有时需要存储一些较为复杂的状态（如坐标，无法离散化的数值，字符串等）以及与之有关的答案（如到达此状态的最小步数）．`map` 可以用来实现此功能．其中的键是状态，而值是与之相关的答案．下面的示例展示了如何使用 `map` 存储以 `string` 表示的状态．

```cpp
// 存储状态与对应的答案
map<string, int> record;

// 新搜索到的状态与对应答案
string status;
int ans;
// 查找对应的状态是否出现过
map<string, int>::iterator it = record.find(status);
if (it == record.end()) {
  // 尚未搜索过该状态，将其加入状态记录中
  record[status] = ans;
  // 进行相应操作……
} else {
  // 已经搜索过该状态，进行相应操作……
}
```

## 遍历容器

可以利用迭代器来遍历关联式容器的所有元素．

```cpp
set<int> s;
using si = set<int>::iterator;
for (si it = s.begin(); it != s.end(); it++) cout << *it << endl;
```

需要注意的是，对 `map` 的迭代器解引用后，得到的是类型为 `pair<Key, T>` 的键值对．

在 C++11 中，使用范围 for 循环会让代码简洁很多：

```cpp
set<int> s;
for (auto x : s) cout << x << endl;
```

对于任意关联式容器，使用迭代器遍历容器的时间复杂度均为 $O(n)$．

## 自定义比较方式

`set` 在默认情况下的比较函数为 `<`（如果是非内置类型需要 [重载 `<` 运算符](../op-overload.md#比较运算符)）．然而在某些特殊情况下，我们希望能自定义 `set` 内部的比较方式．

这时候可以通过传入自定义比较器来解决问题．

具体来说，我们需要定义一个类，并在这个类中 [重载 `()` 运算符](../op-overload.md#函数调用运算符)．

例如，我们想要维护一个存储整数，且较大值靠前的 `set`，可以这样实现：

```cpp
struct cmp {
  bool operator()(int a, int b) const { return a > b; }
};

set<int, cmp> s;
```

对于其他关联式容器，可以用类似的方式实现自定义比较，这里不再赘述．


## lang/csl/bitset.md

author: i-Yirannn, Xeonacid, ouuan

## 介绍

`std::bitset` 是标准库中的一个存储 `0/1` 的大小不可变容器．严格来讲，它并不属于 STL．

??? note "bitset 与 STL"
    > The C++ standard library provides some special container classes, the so-called container adapters (stack, queue, priority queue). In addition, a few classes provide a container-like interface (for example, strings, bitsets, and valarrays). All these classes are covered separately.1 Container adapters and bitsets are covered in Chapter 12.
    >
    > The C++ standard library provides not only the containers for the STL framework but also some containers that fit some special needs and provide simple, almost self-explanatory, interfaces. You can group these containers into either the so-called container adapters, which adapt standard STL containers to fit special needs, or a bitset, which is a containers for bits or Boolean values. There are three standard container adapters: stacks, queues, and priority queues. In priority queues, the elements are sorted automatically according to a sorting criterion. Thus, the "next" element of a priority queue is the element with the "highest" value. A bitset is a bitfield with an arbitrary but fixed number of bits. Note that the C++ standard library also provides a special container with a variable size for Boolean values: vector.
    
    ——摘自《The C++ Standard Library 2nd Edition》
    
    由此看来，`bitset` 并不属于 STL，而是一种标准库中的 "Special Container"．事实上，它作为一种容器，也并不满足 STL 容器的要求．说它是适配器，它也并不依赖于其它 STL 容器作为底层实现．

由于内存地址是按字节即 `byte` 寻址，而非比特 `bit`，一个 `bool` 类型的变量，虽然只能表示 `0/1`, 但是也占了 1 byte 的内存．

`bitset` 就是通过固定的优化，使得一个字节的八个比特能分别储存 8 位的 `0/1`．

对于一个 4 字节的 `int` 变量，在只存 `0/1` 的意义下，`bitset` 占用空间只是其 $\frac{1}{32}$，计算一些信息时，所需时间也是其 $\frac 1{32}$．

在某些情况下通过 `bitset` 可以优化程序的运行效率．至于其优化的是复杂度还是常数，要看计算复杂度的角度．一般 `bitset` 的复杂度有以下几种记法：（设原复杂度为 $O(n)$）

1.  $O(n)$，这种记法认为 `bitset` 完全没有优化复杂度．
2.  $O(\frac n{32})$，这种记法不太严谨（复杂度中不应出现常数），但体现了 `bitset` 能将所需时间优化至 $\frac 1{32}$．
3.  $O(\frac n w)$，其中 $w=32$（计算机的位数），这种记法较为普遍接受．
4.  $O(\frac n {\log w})$，其中 $w$ 为计算机一个整型变量的大小．

另外，`vector` 的一个特化 `vector<bool>` 的储存方式同 `bitset` 一样，区别在于其支持动态开空间，`bitset` 则和我们一般的静态数组一样，是在编译时就开好了的．然而，`bitset` 有一些好用的库函数，不仅方便，而且有时可以实现 SIMD 进而减小常数．另外，`vector<bool>` 的部分表现和 `vector` 不一致（如对 `std::vector<bool> vec` 来说，`&vec[0] + i` 不等于 `&vec[i]`）．因此，一般不使用 `vector<bool>`．

## 使用

参见 [std::bitset - cppreference.com](https://en.cppreference.com/w/cpp/utility/bitset)．

### 头文件

```cpp
#include <bitset>
```

### 指定大小

```cpp
std::bitset<1000> bs;  // a bitset with 1000 bits
```

### 构造函数

-   `bitset()`: 每一位都是 `false`．
-   `bitset(unsigned long val)`: 设为 `val` 的二进制形式．
-   `bitset(const string& str)`: 设为 $01$ 串 `str`．

### 运算符

-   `operator []`: 访问其特定的一位．

-   `operator ==`/`operator !=`: 比较两个 `bitset` 内容是否完全一样．

-   `operator &`/`operator &=`/`operator |`/`operator |=`/`operator ^`/`operator ^=`/`operator ~`: 进行按位与/或/异或/取反操作．

    注意：**`bitset` 只能与 `bitset` 进行位运算**，若要和整型进行位运算，要先将整型转换为 `bitset`．

-   `operator <<`/`operator >>`/`operator <<=`/`operator >>=`: 进行二进制左移/右移．

此外，`bitset` 还提供了 C++ 流式 IO 的支持，这意味着你可以通过 `cin/cout` 进行输入输出．

### 成员函数

-   `count()`: 返回 `true` 的数量．
-   `size()`: 返回 `bitset` 的大小．
-   `test(pos)`: 它和 `vector` 中的 `at()` 的作用是一样的，和 `[]` 运算符的区别就是越界检查．
-   `any()`: 若存在某一位是 `true` 则返回 `true`，否则返回 `false`．
-   `none()`: 若所有位都是 `false` 则返回 `true`，否则返回 `false`．
-   `all()`: 若所有位都是 `true` 则返回 `true`，否则返回 `false`．
-   1.  `set()`: 将整个 `bitset` 设置成 `true`．
    2.  `set(pos, val = true)`: 将某一位设置成 `true`/`false`．
-   1.  `reset()`: 将整个 `bitset` 设置成 `false`．
    2.  `reset(pos)`: 将某一位设置成 `false`．相当于 `set(pos, false)`．
-   1.  `flip()`: 翻转每一位．（$0\leftrightarrow1$，相当于异或一个全是 $1$ 的 `bitset`）
    2.  `flip(pos)`: 翻转某一位．
-   `to_string()`: 返回转换成的字符串表达．
-   `to_ulong()`: 返回转换成的 `unsigned long` 表达（`long` 在 NT 及 32 位 POSIX 系统下与 `int` 一样，在 64 位 POSIX 下与 `long long` 一样）．
-   `to_ullong()`:（**C++11** 起）返回转换成的 `unsigned long long` 表达．

另外，libstdc++ 中有一些较为实用的内部成员函数[^bitset1]：

-   `_Find_first()`: 返回 `bitset` 第一个 `true` 的下标，若没有 `true` 则返回 `bitset` 的大小．
-   `_Find_next(pos)`: 返回 `pos` 后面（下标严格大于 `pos` 的位置）第一个 `true` 的下标，若 `pos` 后面没有 `true` 则返回 `bitset` 的大小．

## 应用

### [「LibreOJ β Round #2」贪心只能过样例](https://loj.ac/problem/515)

这题可以用 dp 做，转移方程很简单：

$f(i,j)$ 表示前 $i$ 个数的平方和能否为 $j$，那么 $f(i,j)=\bigvee\limits_{k=a}^bf(i-1,j-k^2)$（或起来）．

但如果直接做的话是 $O(n^5)$ 的，（看起来）过不了．

发现可以用 `bitset` 优化，左移再或起来就好了：

??? note "提交记录：[std::bitset](https://loj.ac/submission/395274)"
    ```cpp
    #include <bitset>
    #include <cstdio>
    #include <iostream>
    
    using namespace std;
    
    constexpr int N = 101;
    
    int n, a[N], b[N];
    bitset<N * N * N> f[N];
    
    int main() {
      int i, j;
    
      cin >> n;
    
      for (i = 1; i <= n; ++i) cin >> a[i] >> b[i];
    
      f[0][0] = 1;
    
      for (i = 1; i <= n; ++i) {
        for (j = a[i]; j <= b[i]; ++j) {
          f[i] |= (f[i - 1] << (j * j));
        }
      }
    
      cout << f[n].count();
    
      return 0;
    }
    ```

由于 libstdc++ 的实现为压 `__CHAR_BIT__ * sizeof(unsigned long)` 位的[^bitset2]，在一些平台中其为 $32$．所以，可以手写 `bitset`（只需要支持左移后或起来这一种操作）压 $64$ 位（`__CHAR_BIT__ * sizeof(unsigned long long)`）来进一步优化：

??? note "提交记录：[手写 bitset](https://loj.ac/submission/395619)"
    ```cpp
    #include <cstdio>
    #include <iostream>
    
    using namespace std;
    
    constexpr int N = 101;
    constexpr int W = 64;
    
    struct Bitset {
      unsigned long long a[N * N * N >> 6];
    
      void shiftor(const Bitset &y, int p, int l, int r) {
        int t = p - p / W * W;
        int tt = (t == 0 ? 0 : W - t);
        int to = (r + p) / W;
        int qaq = (p + W - 1) / W;
    
        for (int i = (l + p) / W; i <= to; ++i) {
          if (i - qaq >= 0) a[i] |= y.a[i - qaq] >> tt;
    
          a[i] |= ((y.a[i - qaq + 1] & ((1ull << tt) - 1)) << t);
        }
      }
    } f[N];
    
    int main() {
      int n, a, b, l = 0, r = 0, ans = 0;
    
      scanf("%d", &n);
    
      f[0].a[0] = 1;
    
      for (int i = 1; i <= n; ++i) {
        scanf("%d%d", &a, &b);
    
        for (int j = a; j <= b; ++j) f[i].shiftor(f[i - 1], j * j, l, r);
    
        l += a * a;
        r += b * b;
      }
    
      for (int i = l / W; i <= r / W; ++i)
        ans += __builtin_popcount(f[n].a[i] & 0xffffffffu) +
               __builtin_popcount(f[n].a[i] >> 32);
    
      printf("%d", ans);
    
      return 0;
    }
    ```

另外，加了几个剪枝的暴力也能过：

??? note "提交记录：[加了几个剪枝的暴力](https://loj.ac/submission/395673)"
    ```cpp
    #include <cstdio>
    #include <iostream>
    
    using namespace std;
    
    constexpr int N = 101;
    constexpr int W = 64;
    
    bool f[N * N * N];
    
    int main() {
      int n, i, j, k, a, b, l = 0, r = 0, ans = 0;
    
      scanf("%d", &n);
    
      f[0] = true;
    
      for (i = 1; i <= n; ++i) {
        scanf("%d%d", &a, &b);
        l += a * a;
        r += b * b;
    
        for (j = r; j >= l; --j) {
          f[j] = false;
    
          for (k = a; k <= b; ++k) {
            if (j - k * k < l - a * a) break;
    
            if (f[j - k * k]) {
              f[j] = true;
              break;
            }
          }
        }
      }
    
      for (i = l; i <= r; ++i) ans += f[i];
    
      printf("%d", ans);
    
      return 0;
    }
    ```

### [CF1097F Alex and a TV Show](https://codeforces.com/contest/1097/problem/F)

#### 题意

给你 $n$ 个可重集，四种操作：

1.  把某个可重集设为一个数．
2.  把某个可重集设为另外两个可重集加起来．
3.  把某个可重集设为从另外两个可重集中各选一个数的 $\gcd$．即：$A=\{\gcd(x,y)|x\in B,y\in C\}$．
4.  询问某个可重集中某个数的个数，**在模 2 意义下**．

可重集个数 $10^5$，操作个数 $10^6$，值域 $7000$．

#### 做法

看到「在模 $2$ 意义下」，可以想到用 `bitset` 维护每个可重集．

这样的话，操作 $1$ 直接设，操作 $2$ 就是异或（因为模 $2$），操作 $4$ 就是直接查，但 .. 操作 $3$ 怎么办？

我们可以尝试维护每个可重集的所有约数构成的可重集，这样的话，操作 $3$ 就是直接按位与．

我们可以把值域内每个数的约数构成的 `bitset` 预处理出来，这样操作 $1$ 就解决了．操作 $2$ 仍然是异或．

现在的问题是，如何通过一个可重集的约数构成的可重集得到该可重集中某个数的个数．

令原可重集为 $A$，其约数构成的可重集为 $A'$，我们要求 $A$ 中 $x$ 的个数，用 [莫比乌斯反演](../../math/number-theory/mobius.md) 推一推：

$$
\begin{aligned}&\sum\limits_{i\in A}[\frac i x=1]\\=&\sum\limits_{i\in A}\sum\limits_{d|\frac i x}\mu(d)\\=&\sum\limits_{d\in A',x|d}\mu(\frac d x)\end{aligned}
$$

由于是模 $2$ 意义下，$-1$ 和 $1$ 是一样的，只用看 $\frac d x$ 有没有平方因子即可．所以，可以对值域内每个数预处理出其倍数中除以它不含平方因子的位置构成的 `bitset`，求答案的时候先按位与再 `count()` 就好了．

这样的话，单次询问复杂度就是 $O(\frac v w)$（$v=7000,\,w=32$）．

至于预处理的部分，$O(v\sqrt v)$ 或者 $O(v^2)$ 预处理比较简单，$\log$ 预处理就如下面代码所示，复杂度为调和级数，所以是 $O(v\log v)$．

??? note "参考代码"
    ```cpp
    #include <bitset>
    #include <cctype>
    #include <cmath>
    #include <cstdio>
    #include <iostream>
    
    using namespace std;
    
    int read() {
      int out = 0;
      char c;
      while (!isdigit(c = getchar()));
      for (; isdigit(c); c = getchar()) out = out * 10 + c - '0';
      return out;
    }
    
    constexpr int N = 100005;
    constexpr int M = 1000005;
    constexpr int V = 7005;
    
    bitset<V> pre[V], pre2[V], a[N], mu;
    int n, m, tot;
    char ans[M];
    
    int main() {
      int i, j, x, y, z;
    
      n = read();
      m = read();
    
      mu.set();
      for (i = 2; i * i < V; ++i) {
        for (j = 1; i * i * j < V; ++j) {
          mu[i * i * j] = 0;
        }
      }
      for (i = 1; i < V; ++i) {
        for (j = 1; i * j < V; ++j) {
          pre[i * j][i] = 1;
          pre2[i][i * j] = mu[j];
        }
      }
    
      while (m--) {
        switch (read()) {
          case 1:
            x = read();
            y = read();
            a[x] = pre[y];
            break;
          case 2:
            x = read();
            y = read();
            z = read();
            a[x] = a[y] ^ a[z];
            break;
          case 3:
            x = read();
            y = read();
            z = read();
            a[x] = a[y] & a[z];
            break;
          case 4:
            x = read();
            y = read();
            ans[tot++] = ((a[x] & pre2[y]).count() & 1) + '0';
            break;
        }
      }
    
      printf("%s", ans);
    
      return 0;
    }
    ```

### 与埃氏筛结合

由于 `bitset` 快速的连续读写效率，使得它非常适合用于与 [埃氏筛](../../math/number-theory/sieve.md#埃拉托斯特尼筛法) 结合打质数表．

使用的方式也很简单，只需要将埃氏筛中的布尔数组替换成 `bitset` 即可．

??? note "速度测试"
    使用 [Quick C++ Benchmarks](https://quick-bench.com) 进行测试，编译器采用 `GCC 13.2`，编译参数为 `-std=c++20 -O2`．
    
    | 算法                            | 函数名                      |
    | ----------------------------- | ------------------------ |
    | 埃氏筛 + C 风格布尔数组，不存储筛出来的素数      | `Eratosthenes_CArray`    |
    | 埃氏筛 +`vector<bool>`，不存储筛出来的素数 | `Eratosthenes_vector`    |
    | 埃氏筛 +`bitset`，不存储筛出来的素数       | `Eratosthenes_bitset`    |
    | 埃氏筛 + C 风格布尔数组，存储筛出来的素数       | `Eratosthenes_CArray_sp` |
    | 埃氏筛 +`vector<bool>`，存储筛出来的素数  | `Eratosthenes_vector_sp` |
    | 埃氏筛 +`bitset`，存储筛出来的素数        | `Eratosthenes_bitset_sp` |
    | 欧拉筛 + C 风格布尔数组                | `Euler_CArray`           |
    | 欧拉筛 +`vector<bool>`           | `Euler_vector`           |
    | 欧拉筛 +`bitset`                 | `Euler_bitset`           |
    
    -   当埃氏筛 **存储** 筛出来的素数时：
    
        -   $N=5 \times 10^7 + 1$ 时的 [测试结果](https://quick-bench.com/q/iQL9FhsZ6PVV81HKABsidRw8hB8)：
    
            ![](./images/bitset-5e7sp.png)
        -   $N=10^8 + 1$ 时的 [测试结果](https://quick-bench.com/q/pwEamEFUW-6nXeXEALRsYPd8FWI)：
    
            ![](./images/bitset-1e8sp.png)
    -   当埃氏筛 **不存储** 筛出来的素数时：
    
        -   $N=5 \times 10^7 + 1$ 时的 [测试结果](https://quick-bench.com/q/rg2mCUxT02a44w9fWvHtZoNTJyU)：
    
            ![](./images/bitset-5e7.png)
        -   $N=10^8 + 1$ 时的 [测试结果](https://quick-bench.com/q/lusNWxWsR0VXoRBof7uBtqfvJuY)：
    
            ![](./images/bitset-1e8.png)
    
    从测试结果中可知：
    
    1.  时间复杂度 $O(n \log \log n)$ 的埃氏筛在使用 `bitset` 或 `vector<bool>` 优化后，性能甚至超过时间复杂度 $O(n)$ 的欧拉筛；
    2.  欧拉筛使用 `bitset` 或 `vector<bool>` 后的优化效果在大多数情况下均不明显；
    3.  `bitset` 的优化效果略强于 `vector<bool>`．

??? note "参考代码"
    需安装 [google/benchmark](https://github.com/google/benchmark)．
    
    ```cpp
    #include <benchmark/benchmark.h>
    #include <bits/stdc++.h>
    using namespace std;
    using u32 = uint32_t;
    using u64 = uint64_t;
    
    #define ERATOSTHENES_STORAGE_PRIME
    #define ENABLE_EULER
    constexpr u32 N = 5e7 + 1;
    
    #ifndef ERATOSTHENES_STORAGE_PRIME
    
    void Eratosthenes_CArray(benchmark::State &state) {
      static bool is_prime[N];
      for (auto _ : state) {
        fill(is_prime, is_prime + N, true);
        is_prime[0] = is_prime[1] = false;
        for (u32 i = 2; (u64)i * i < N; ++i)
          if (is_prime[i])
            for (u32 j = i * i; j < N; j += i) is_prime[j] = false;
        benchmark::DoNotOptimize(0);
      }
    }
    
    BENCHMARK(Eratosthenes_CArray);
    
    void Eratosthenes_vector(benchmark::State &state) {
      static vector<bool> is_prime(N);
      for (auto _ : state) {
        fill(is_prime.begin(), is_prime.end(), true);
        is_prime[0] = is_prime[1] = false;
        for (u32 i = 2; (u64)i * i < N; ++i)
          if (is_prime[i])
            for (u32 j = i * i; j < N; j += i) is_prime[j] = false;
        benchmark::DoNotOptimize(0);
      }
    }
    
    BENCHMARK(Eratosthenes_vector);
    
    void Eratosthenes_bitset(benchmark::State &state) {
      static bitset<N> is_prime;
      for (auto _ : state) {
        is_prime.set();
        is_prime.reset(0);
        is_prime.reset(1);
        for (u32 i = 2; (u64)i * i < N; ++i)
          if (is_prime[i])
            for (u32 j = i * i; j < N; j += i) is_prime.reset(j);
        benchmark::DoNotOptimize(0);
      }
    }
    
    BENCHMARK(Eratosthenes_bitset);
    
    #else
    
    void Eratosthenes_CArray_sp(benchmark::State &state) {
      static bool is_prime[N];
      for (auto _ : state) {
        vector<u32> prime;
        fill(is_prime, is_prime + N, true);
        is_prime[0] = is_prime[1] = false;
        for (u32 i = 2; (u64)i * i < N; ++i)
          if (is_prime[i])
            for (u32 j = i * i; j < N; j += i) is_prime[j] = false;
        for (u32 i = 2; i < N; ++i)
          if (is_prime[i]) prime.push_back(i);
        benchmark::DoNotOptimize(prime);
      }
    }
    
    BENCHMARK(Eratosthenes_CArray_sp);
    
    void Eratosthenes_vector_sp(benchmark::State &state) {
      static vector<bool> is_prime(N);
      for (auto _ : state) {
        vector<u32> prime;
        fill(is_prime.begin(), is_prime.end(), true);
        is_prime[0] = is_prime[1] = false;
        for (u32 i = 2; (u64)i * i < N; ++i)
          if (is_prime[i])
            for (u32 j = i * i; j < N; j += i) is_prime[j] = false;
        for (u32 i = 2; i < N; ++i)
          if (is_prime[i]) prime.push_back(i);
        benchmark::DoNotOptimize(prime);
      }
    }
    
    BENCHMARK(Eratosthenes_vector_sp);
    
    void Eratosthenes_bitset_sp(benchmark::State &state) {
      static bitset<N> is_prime;
      for (auto _ : state) {
        vector<u32> prime;
        is_prime.set();
        is_prime.reset(0);
        is_prime.reset(1);
        for (u32 i = 2; (u64)i * i < N; ++i)
          if (is_prime[i])
            for (u32 j = i * i; j < N; j += i) is_prime.reset(j);
        for (u32 i = 2; i < N; ++i)
          if (is_prime[i]) prime.push_back(i);
        benchmark::DoNotOptimize(prime);
      }
    }
    
    BENCHMARK(Eratosthenes_bitset_sp);
    
    #endif
    
    #ifdef ENABLE_EULER
    
    void Euler_CArray(benchmark::State &state) {
      static bool not_prime[N];
      for (auto _ : state) {
        vector<u32> prime;
        fill(not_prime, not_prime + N, false);
        not_prime[0] = not_prime[1] = true;
        for (u32 i = 2; i < N; ++i) {
          if (!not_prime[i]) prime.push_back(i);
          for (u32 pri_j : prime) {
            if (i * pri_j >= N) break;
            not_prime[i * pri_j] = true;
            if (i % pri_j == 0) break;
          }
        }
        benchmark::DoNotOptimize(prime);
      }
    }
    
    BENCHMARK(Euler_CArray);
    
    void Euler_vector(benchmark::State &state) {
      static vector<bool> not_prime(N);
      for (auto _ : state) {
        vector<u32> prime;
        fill(not_prime.begin(), not_prime.end(), false);
        not_prime[0] = not_prime[1] = true;
        for (u32 i = 2; i < N; ++i) {
          if (!not_prime[i]) prime.push_back(i);
          for (u32 pri_j : prime) {
            if (i * pri_j >= N) break;
            not_prime[i * pri_j] = true;
            if (i % pri_j == 0) break;
          }
        }
        benchmark::DoNotOptimize(prime);
      }
    }
    
    BENCHMARK(Euler_vector);
    
    void Euler_bitset(benchmark::State &state) {
      static bitset<N> not_prime;
      for (auto _ : state) {
        vector<u32> prime;
        not_prime.reset();
        not_prime.set(0);
        not_prime.set(1);
        for (u32 i = 2; i < N; ++i) {
          if (!not_prime[i]) prime.push_back(i);
          for (u32 pri_j : prime) {
            if (i * pri_j >= N) break;
            not_prime.set(i * pri_j);
            if (i % pri_j == 0) break;
          }
        }
        benchmark::DoNotOptimize(prime);
      }
    }
    
    BENCHMARK(Euler_bitset);
    
    #endif
    
    static void Noop(benchmark::State &state) {
      for (auto _ : state) benchmark::DoNotOptimize(0);
    }
    
    BENCHMARK(Noop);
    BENCHMARK_MAIN();
    ```

### 与树分块结合

`bitset` 与树分块结合可以解决一类求树上多条路径信息并的问题，详见 [数据结构/树分块](../../ds/tree-decompose.md)．

### 与莫队结合

详见 [杂项/莫队配合 bitset](../../misc/mo-algo-with-bitset.md)．

### 计算高维偏序

详见 [FHR 课件](https://github.com/OI-wiki/libs/blob/master/lang/csl/FHR-分块bitset求高维偏序.pdf)．

## 参考资料与注释

[^bitset1]: [libstdc++: SGI STL extensions](https://gcc.gnu.org/onlinedocs/libstdc++/libstdc++-html-USERS-4.4/a00994.html#g32541eb0d6581b915af48b5a51006dff)

[^bitset2]: [libstdc++: std::bitset<\_Nb> Class Template Reference](https://gcc.gnu.org/onlinedocs/libstdc++/libstdc++-html-USERS-4.4/a00219.html)


## lang/csl/container-adapter.md

author: Xeonacid, ksyx, Early0v0

## 栈

STL [栈](../../ds/stack.md)(`std::stack`) 是一种后进先出 (Last In, First Out) 的容器适配器，仅支持查询或删除最后一个加入的元素（栈顶元素），不支持随机访问，且为了保证数据的严格有序性，不支持迭代器．

### 头文件

```cpp
#include <stack>
```

### 定义

```cpp
std::stack<TypeName> s;  // 使用默认底层容器 deque，数据类型为 TypeName
std::stack<TypeName, Container> s;  // 使用 Container 作为底层容器
std::stack<TypeName> s2(s1);        // 将 s1 复制一份用于构造 s2
```

### 成员函数

**以下所有函数均为常数复杂度**

-   `top()` 访问栈顶元素（如果栈为空，此处会出错）
-   `push(x)` 向栈中插入元素 x
-   `pop()` 删除栈顶元素
-   `size()` 查询容器中的元素数量
-   `empty()` 询问容器是否为空

### 简单示例

```cpp
std::stack<int> s1;
s1.push(2);
s1.push(1);
std::stack<int> s2(s1);
s1.pop();
std::cout << s1.size() << " " << s2.size() << std::endl;  // 1 2
std::cout << s1.top() << " " << s2.top() << std::endl;    // 2 1
s1.pop();
std::cout << s1.empty() << " " << s2.empty() << std::endl;  // 1 0
```

## 队列

STL [队列](../../ds/queue.md)(`std::queue`) 是一种先进先出 (First In, First Out) 的容器适配器，仅支持查询或删除第一个加入的元素（队首元素），不支持随机访问，且为了保证数据的严格有序性，不支持迭代器．

### 头文件

```cpp
#include <queue>
```

### 定义

```cpp
std::queue<TypeName> q;  // 使用默认底层容器 deque，数据类型为 TypeName
std::queue<TypeName, Container> q;  // 使用 Container 作为底层容器

std::queue<TypeName> q2(q1);  // 将 q1 复制一份用于构造 q2
```

### 成员函数

**以下所有函数均为常数复杂度**

-   `front()` 访问队首元素（如果队列为空，此处会出错）
-   `push(x)` 向队列中插入元素 x
-   `pop()` 删除队首元素
-   `size()` 查询容器中的元素数量
-   `empty()` 询问容器是否为空

### 简单示例

```cpp
std::queue<int> q1;
q1.push(2);
q1.push(1);
std::queue<int> q2(q1);
q1.pop();
std::cout << q1.size() << " " << q2.size() << std::endl;    // 1 2
std::cout << q1.front() << " " << q2.front() << std::endl;  // 1 2
q1.pop();
std::cout << q1.empty() << " " << q2.empty() << std::endl;  // 1 0
```

## 优先队列

优先队列 `std::priority_queue` 是一种 [堆](../../ds/heap.md)，一般为 [二叉堆](../../ds/binary-heap.md)．

### 头文件

```cpp
#include <queue>
```

### 定义

```cpp
std::priority_queue<TypeName> q;             // 数据类型为 TypeName
std::priority_queue<TypeName, Container> q;  // 使用 Container 作为底层容器
std::priority_queue<TypeName, Container, Compare> q;
// 使用 Container 作为底层容器，使用 Compare 作为比较类型

// 默认使用底层容器 vector
// 比较类型 less<TypeName>（此时为它的 top() 返回为最大值）
// 若希望 top() 返回最小值，可令比较类型为 greater<TypeName>
// 注意：不可跳过 Container 直接传入 Compare

// 从 C++11 开始，如果使用 lambda 函数自定义 Compare
// 则需要将其作为构造函数的参数代入，如：
auto cmp = [](const std::pair<int, int> &l, const std::pair<int, int> &r) {
  return l.second < r.second;
};
std::priority_queue<std::pair<int, int>, std::vector<std::pair<int, int>>,
                    decltype(cmp)>
    pq(cmp);
```

### 成员函数

**以下所有函数均为常数复杂度**

-   `top()` 访问堆顶元素（此时优先队列不能为空）
-   `empty()` 询问容器是否为空
-   `size()` 查询容器中的元素数量

**以下所有函数均为对数复杂度**

-   `push(x)` 插入元素，并对底层容器排序
-   `pop()` 删除堆顶元素（此时优先队列不能为空）

### 简单示例

```cpp
std::priority_queue<int> q1;
std::priority_queue<int, std::vector<int>> q2;
// C++11 后空格可省略
std::priority_queue<int, std::deque<int>, std::greater<int>> q3;
// q3 为小根堆
for (int i = 1; i <= 5; i++) q1.push(i);
// q1 中元素 :  [1, 2, 3, 4, 5]
std::cout << q1.top() << std::endl;
// 输出结果 : 5
q1.pop();
// 堆中元素 : [1, 2, 3, 4]
std::cout << q1.size() << std::endl;
// 输出结果 ：4
for (int i = 1; i <= 5; i++) q3.push(i);
// q3 中元素 :  [1, 2, 3, 4, 5]
std::cout << q3.top() << std::endl;
// 输出结果 : 1
```


## lang/csl/container.md

## 分类

![](images/container1.png)

### 序列式容器

-   **向量**(`vector`) 后端可高效增加元素的顺序表．
-   **数组**(`array`)**C++11**，定长的顺序表，C 风格数组的简单包装．
-   **双端队列**(`deque`) 双端都可高效增加元素的顺序表．
-   **列表**(`list`) 可以沿双向遍历的链表．
-   **单向列表**(`forward_list`) 只能沿一个方向遍历的链表．

### 关联式容器

-   **集合**(`set`) 用以有序地存储 **互异** 元素的容器．其实现是由节点组成的红黑树，每个节点都包含着一个元素，节点之间以某种比较元素大小的谓词进行排列．
-   **多重集合**(`multiset`) 用以有序地存储元素的容器．允许存在相等的元素．
-   **映射**(`map`) 由 {键，值} 对组成的集合，以某种比较键大小关系的谓词进行排列．
-   **多重映射**(`multimap`) 由 {键，值} 对组成的多重集合，亦即允许键有相等情况的映射．

???+ note "什么是谓词 ([**Predicate**](https://en.wikipedia.org/wiki/Predicate_%28mathematical_logic%29))？"
    谓词就是返回值为真或者假的函数．STL 容器中经常会使用到谓词，用于模板参数．

### 无序（关联式）容器

-   **无序（多重）集合**(`unordered_set`/`unordered_multiset`)**C++11**，与 `set`/`multiset` 的区别在于元素无序，只关心「元素是否存在」，使用哈希实现．
-   **无序（多重）映射**(`unordered_map`/`unordered_multimap`)**C++11**，与 `map`/`multimap` 的区别在于键 (key) 无序，只关心 "键与值的对应关系"，使用哈希实现．

### 容器适配器

容器适配器其实并不是容器．它们不具有容器的某些特点（如：有迭代器、有 `clear()` 函数……）．

> 「适配器是使一种事物的行为类似于另外一种事物行为的一种机制」，适配器对容器进行包装，使其表现出另外一种行为．

-   **栈**(`stack`) 后进先出 (LIFO) 的容器，默认是对双端队列（`deque`）的包装．
-   **队列**(`queue`) 先进先出 (FIFO) 的容器，默认是对双端队列（`deque`）的包装．
-   **优先队列**(`priority_queue`) 元素的次序是由作用于所存储的值对上的某种谓词决定的一种队列，默认是对向量（`vector`）的包装．

## 共同点

### 容器声明

都是 `containerName<typeName,...> name` 的形式，但模板参数（`<>` 内的参数）的个数、形式会根据具体容器而变．

本质原因：STL 就是「标准模板库」，所以容器都是模板类．

### 迭代器

请参考 [迭代器](./iterator.md)．

### 共有函数

`=`：有赋值运算符以及复制构造函数．

`begin()`：返回指向开头元素的迭代器．

`end()`：返回指向末尾的下一个元素的迭代器．`end()` 不指向某个元素，但它是末尾元素的后继．

`size()`：返回容器内的元素个数．

`max_size()`：返回容器 **理论上** 能存储的最大元素个数．依容器类型和所存储变量的类型而变．

`empty()`：返回容器是否为空．

`swap()`：交换两个容器．

`clear()`：清空容器．

`==`/`!=`/`<`/`>`/`<=`/`>=`：按 **字典序** 比较两个容器的大小．（比较元素大小时 `map` 的每个元素相当于 `set<pair<key, value>>`，无序容器不支持 `<`/`>`/`<=`/`>=`．）


## lang/csl/index.md

## C++ 标准

首先需要介绍的是 C++ 本身的版本．由于 C++ 本身只是一门语言，而不同的编译器对 C++ 的实现方法各不一致，因此需要标准化来约束编译器的实现，使得 C++ 代码在不同的编译器下表现一致．C++ 自 1985 年诞生以来，一共由国际标准化组织（ISO）发布了 7 个正式的 C++ 标准，依次为 C++98、C++03、C++11（亦称 C++0x）、C++14（亦称 C++1y）、C++17（亦称 C++1z）、C++20（亦称 C++2a）、C++23（亦称 C++2b）．C++ 标准草案在 [open-std](http://www.open-std.org/jtc1/sc22/wg21/docs/papers/) 网站上，最新标准的制定进度可以在 [Current Status : Standard C++](https://isocpp.org/std/status) 查看．此外还有一些补充标准，例如 C++ TR1．

每一个版本的 C++ 标准不仅规定了 C++ 的语法、语言特性，还规定了一套 C++ 内置库的实现规范，这个库便是 C++ 标准库．C++ 标准库中包含大量常用代码的实现，如输入输出、基本数据结构、内存管理、多线程支持等．掌握 C++ 标准库是编写更现代的 C++ 代码必要的一步．C++ 标准库的详细文档在 [cppreference](https://zh.cppreference.com/) 网站上，文档对标准库中的类型函数的用法、效率、注意事项等都有介绍，请善用．

需要指出的是，不同的 OJ 平台对 C++ 版本均不相同，例如 [最新的 ICPC 比赛规则](https://docs.icpc.global/worldfinals-programming-environment/) 支持 C++20 标准．根据 NOI 科学委员会决议，自 2021 年 9 月 1 日起 [NOI Linux 2.0](https://www.noi.cn/gynoi/jsgz/2021-07-16/732450.shtml) 作为 NOI 系列比赛和 CSP-J/S 等活动的标准环境使用．NOI Linux 2.0 中指定的 g++ 9.3.0 [默认支持标准](https://gcc.gnu.org/projects/cxx-status.html#cxx14) 为 C++14，并支持 C++17 标准，可以满足绝大部分竞赛选手的需求．因此在学习 C++ 时要注意比赛支持的标准，避免在赛场上时编译报错．

## 标准模板库（STL）

STL 即标准模板库（Standard Template Library），是 C++ 标准库的一部分，里面包含了一些模板化的通用的数据结构和算法．由于其模板化的特点，它能够兼容自定义的数据类型，避免大量的造轮子工作．NOI 和 ICPC 赛事都支持 STL 库的使用，因此合理利用 STL 可以避免编写无用算法，并且充分利用编译器对模板库优化提高效率．STL 库的详细介绍请参见对应的页面：[STL 容器](./container.md) 和 [STL 算法](./algorithm.md)．

??? note "什么是造轮子"
    造轮子（[Reinventing\_the\_wheel](https://en.wikipedia.org/wiki/Reinventing_the_wheel)）指的是重复发明已有的算法，或者重复编写现成优化过的代码．造轮子通常耗时耗力，同时效果还没有别人好．但若是为了学习或者练习，造轮子则是必要的．

## Boost 库

[Boost](https://www.boost.org/) 是除了标准库外，另一个久副盛名的开源 C++ 工具库，其代码具有可移植、高质量、高性能、高可靠性等特点．Boost 中的模块数量非常之大，功能全面，并且拥有完备的跨平台支持，因此被看作 C++ 的准标准库．C++ 标准中的不少特性也都来自于 Boost，如智能指针、元编程、日期和时间等．尽管在 OI 中无法使用 Boost，但是 Boost 中有不少轮子可以用来验证算法或者对拍，如 Boost.Geometry 有 R 树的实现，Boost.Graph 有图的相关算法，Boost.Intrusive 则提供了一套与 STL 容器用法相似的侵入式容器．有兴趣的读者可以自行在网络搜索教程．

## 参考资料

1.  [C++ reference](https://en.cppreference.com/)
2.  [C++ 参考手册](https://zh.cppreference.com/)
3.  [维基百科 - C++](https://zh.wikipedia.org/wiki/C%2B%2B)
4.  [Boost 官方网站](https://www.boost.org/)
5.  [Boost 教程网站](https://theboostcpplibraries.com/)


## lang/csl/iterator.md

在 STL 中，迭代器（Iterator）用来访问和检查 STL 容器中元素的对象，它的行为模式和指针类似，但是它封装了一些有效性检查，并且提供了统一的访问格式．类似的概念在其他很多高级语言中都存在，如 Python 的 `__iter__` 函数，C# 的 `IEnumerator`．

## 基础使用

迭代器听起来比较晦涩，其实迭代器本身可以看作一个数据指针．迭代器主要支持两个运算符：自增 (`++`) 和解引用（单目 `*` 运算符），其中自增用来移动迭代器，解引用可以获取或修改它指向的元素．

指向某个 [STL 容器](./container.md)  `container` 中元素的迭代器的类型一般为 `container::iterator`．

迭代器可以用来遍历容器，例如，下面两个 for 循环的效果是一样的：

```cpp
vector<int> data(10);

for (int i = 0; i < data.size(); i++)
  cout << data[i] << endl;  // 使用下标访问元素

for (vector<int>::iterator iter = data.begin(); iter != data.end(); iter++)
  cout << *iter << endl;  // 使用迭代器访问元素
// 在C++11后可以使用 auto iter = data.begin() 来简化上述代码
```

???+ tip "`auto` 在竞赛中的使用"
    大部分选手都喜欢使用 `auto` 来代替繁琐的迭代器声明．根据 2021 年 9 月发布的 [关于 NOI 系列活动中编程语言使用限制的补充说明](https://www.noi.cn/xw/2021-09-01/735729.shtml)，NOI 系列比赛（包括 CSP J/S）在评测时将使用 **C++14**，这个版本已经支持了 `auto` 关键字．

## 分类

在 STL 的定义中，迭代器根据其支持的操作依次分为以下几类：

-   InputIterator（输入迭代器）：只要求支持拷贝、自增和解引访问．
-   OutputIterator（输出迭代器）：只要求支持拷贝、自增和解引赋值．
-   ForwardIterator（前向迭代器）：在 InputIterator 的基础上支持多次遍历迭代器解引访问，且保证多次访问的结果一致．
-   BidirectionalIterator（双向迭代器）：在 ForwardIterator 的基础上支持自减（即反向访问）．
-   RandomAccessIterator（随机访问迭代器）：在 BidirectionalIterator 的基础上支持加减运算和比较运算（即随机访问）．
-   ContiguousIterator（连续迭代器）：在 RandomAccessIterator 的基础上要求对可解引用的迭代器 `a + n` 满足 `*(a + n)` 与 `*(std::address_of(*a) + n)` 等价（即连续存储，其中 `a` 为连续迭代器、`n` 为整型值）．

    ContiguousIterator 于 C++17 中正式引入．

???+ tip "为什么输入迭代器叫输入迭代器？"
    「输入」指的是「可以从迭代器中获取输入」，而「输出」指的是「可以输出到迭代器」．
    
    「输入」和「输出」的施动者是程序的其它部分，而不是迭代器自身．

迭代器的这些分类并不互斥．实际上，除了输出迭代器之外，列表中排在前面的迭代器都包含着排在后面的迭代器．例如，在要求使用前向迭代器的地方，同样可以使用双向迭代器．从前向迭代器开始，如果这些迭代器还实现了输出迭代器的功能（即允许写操作），就称它们是可变迭代器．由此，可以衍生出诸如「可变随机访问迭代器」这样的类别．

不同的 [STL 容器](./container.md) 支持的迭代器类型不同，在使用时需要留意．

数组指针满足连续迭代器（或随机访问迭代器，对于 C++14 及以前的版本）的所有要求，可以当作连续迭代器使用．

## 相关函数

很多 [STL 函数](./algorithm.md) 都使用迭代器作为参数．

可以使用 `std::advance(it, n)` 将迭代器 `it` 向后移动 `n` 步；若 `n` 为负数，则对应向前移动，此时迭代器必须满足双向迭代器，否则行为未定义．

在 C++11 以后可以使用 `std::next(it)` 获得前向迭代器 `it` 的后继（此时迭代器 `it` 不变），`std::next(it, n)` 获得前向迭代器 `it` 的第 `n` 个后继．

在 C++11 以后可以使用 `std::prev(it)` 获得双向迭代器 `it` 的前驱（此时迭代器 `it` 不变），`std::prev(it, n)` 获得双向迭代器 `it` 的第 `n` 个前驱．

[STL 容器](./container.md) 一般支持从一端或两端开始的访问，以及对 [const 修饰符](../const.md) 的支持．例如容器的 `begin()` 函数可以获得指向容器第一个元素的迭代器，`rbegin()` 函数可以获得指向容器最后一个元素的反向迭代器，`cbegin()` 函数可以获得指向容器第一个元素的 const 迭代器，`end()` 函数可以获得指向容器尾端（「尾端」并不是最后一个元素，可以看作是最后一个元素的后继；「尾端」的前驱是容器里的最后一个元素，其本身不指向任何一个元素）的迭代器．

可在 [Iterator library - cppreference.com](https://en.cppreference.com/w/cpp/iterator) 查看更多用法．


## lang/csl/pair.md

author: sbofgayschool

`std::pair` 是标准库中定义的一个类模板．用于将两个变量关联在一起，组成一个「对」，而且两个变量的数据类型可以是不同的．

??? note "类模板"
    类模板（class template）本身不是一个类，而是可以根据 **不同数据类型** 产生 **不同类** 的「模板」．
    
    在使用时，编译器会根据传入的数据类型产生对应的类，再创建对应实例．
    
    模板属于 C++ 较为高级的语言特性，在信息学竞赛中几乎不会出现．如果对此感兴趣，可以进一步阅读《C++ Primer》以学习更深层次的 C++ 知识．

通过灵活使用 `pair`，可以轻松应对 **需要将关联数据捆绑存储、处理** 的场景．

??? note "Struct"
    与自定义的 `struct` 相比，`pair` 不需要额外定义结构与重载运算符，因此使用起来更加简便．
    
    然而，自定义 `struct` 的变量命名往往更加清晰（`pair` 只能使用 `first` 与 `second` 访问包含的两个变量）．同时，如果需要将两个以上的变量进行关联，自定义 `struct` 会更加合适．

## 使用

### 初始化

可以在定义时直接完成 `pair` 的初始化．

```cpp
pair<int, double> p0(1, 2.0);
```

也可以使用先定义，后赋值的方法完成 `pair` 的初始化．

```cpp
pair<int, double> p1;
p1.first = 1;
p1.second = 2.0;
```

还可以使用 `std::make_pair` 函数．该函数接受两个变量，并返回由这两个变量组成的 `pair`．

```cpp
pair<int, double> p2 = make_pair(1, 2.0);
```

一种常用的方法是使用宏定义 `#define mp make_pair`，将有些冗长的 `make_pair` 化简为 `mp`．

在 C++11 以及之后的版本中，`make_pair` 可以配合 `auto` 使用，以避免显式声明数据类型．

```cpp
auto p3 = make_pair(1, 2.0);
```

关于 `auto` 的在信息学竞赛中的使用，参见 [迭代器](./iterator.md) 部分的说明．

### 访问

通过成员函数 `first` 与 `second`，可以访问 `pair` 中包含的两个变量．

```cpp
int i = p0.first;
double d = p0.second;
```

也可以对其进行修改．

```cpp
p1.first++;
```

### 比较

`pair` 已经预先定义了所有的比较运算符，包括 `<`、`>`、`<=`、`>=`、`==`、`!=`．当然，这需要组成 `pair` 的两个变量所属的数据类型定义了 `==` 和/或 `<` 运算符．

其中，`<`、`>`、`<=`、`>=` 四个运算符会先比较两个 `pair` 中的第一个变量，在第一个变量相等的情况下再比较第二个变量．

```cpp
if (p2 >= p3) {
  cout << "do something here" << endl;
}
```

由于 `pair` 定义了 STL 中常用的 `<` 与 `==`，使得其能够很好的与其他 STL 函数或数据结构配合．比如，`pair` 可以作为 `priority_queue` 的数据类型．

```cpp
priority_queue<pair<int, double>> q;
```

### 赋值与交换

可以将 `pair` 的值赋给另一个类型一致的 `pair`．

```cpp
p0 = p1;
```

也可以使用 `swap` 函数交换 `pair` 的值．

```cpp
swap(p0, p1);
p2.swap(p3);
```

## 应用举例

### 离散化

`pair` 可以轻松实现离散化．

我们可以创建一个 `pair` 数组，将原始数据的值作为每个 `pair` 第一个变量，将原始数据的位置作为第二个变量．在排序后，将原始数据值的排名（该值排序后所在的位置）赋给该值原本所在的位置即可．

```cpp
// a为原始数据
pair<int, int> a[MAXN];
// ai为离散化后的数据
int ai[MAXN];
for (int i = 0; i < n; i++) {
  // first为原始数据的值，second为原始数据的位置
  scanf("%d", &a[i].first);
  a[i].second = i;
}
// 排序
sort(a, a + n);
for (int i = 0; i < n; i++) {
  // 将该值的排名赋给该值原本所在的位置
  ai[a[i].second] = i;
}
```

### Dijkstra

如前所述，`pair` 可以作为 `priority_queue` 的数据类型．

那么，在 Dijkstra 算法的堆优化中，可以使用 `pair` 与 `priority_queue` 维护节点，将节点当前到起点的距离作为第一个变量，将节点编号作为第二个变量．

```cpp
priority_queue<pair<int, int>, std::vector<pair<int, int>>,
               std::greater<pair<int, int>>>
    q;
... while (!q.empty()) {
  // dis为入堆时节点到起点的距离，i为节点编号
  int dis = q.top().first, i = q.top().second;
  q.pop();
  ...
}
```

### pair 与 map

`map` 的是 C++ 中存储键值对的数据结构．很多情况下，`map` 中存储的键值对通过 `pair` 向外暴露．

```cpp
map<int, double> m;
m.insert(make_pair(1, 2.0));
```

关于 `map` 更多的内容，请见 [关联式容器](./associative-container.md) 与 [无序关联式容器](./unordered-container.md) 中相关部分．


## lang/csl/sequence-container.md

author: MingqiHuang, Xeonacid, greyqz, i-Yirannn, ChenZ01

## `vector`

`std::vector` 是 STL 提供的 **内存连续的**、**可变长度** 的数组（亦称列表）数据结构．能够提供线性复杂度的插入和删除，以及常数复杂度的随机访问．

### 为什么要使用 `vector`

作为 OIer，对程序效率的追求远比对工程级别的稳定性要高得多，而 `vector` 由于其对内存的动态处理，时间效率在部分情况下低于静态数组，并且在 OJ 服务器不一定开全优化的情况下更加糟糕．所以在正常存储数据的时候，通常不选择 `vector`．下面给出几个 `vector` 优秀的特性，在需要用到这些特性的情况下，`vector` 能给我们带来很大的帮助．

#### `vector` 可以动态分配内存

很多时候我们不能提前开好那么大的空间（eg：预处理 1\~n 中所有数的约数）．尽管我们能知道数据总量在空间允许的级别，但是单份数据还可能非常大，这种时候我们就需要 `vector` 来把内存占用量控制在合适的范围内．`vector` 还支持动态扩容，在内存非常紧张的时候这个特性就能派上用场了．

#### `vector` 重写了比较运算符及赋值运算符

`vector` 重载了六个比较运算符，以字典序实现，这使得我们可以方便的判断两个容器是否相等（复杂度与容器大小成线性关系）．例如可以利用 `vector<char>` 实现字符串比较（当然，还是用 `std::string` 会更快更方便）．另外 `vector` 也重载了赋值运算符，使得数组拷贝更加方便．

#### `vector` 便利的初始化

由于 `vector` 重载了 `=` 运算符，所以我们可以方便地进行 `vector` 的整体赋值操作．此外从 C++11 起 `vector` 还支持 [列表初始化](https://zh.cppreference.com/w/cpp/language/list_initialization)，例如 `vector<int> data {1, 2, 3};`．

### `vector` 的使用方法

以下介绍常用用法，详细内容 [请参见 C++ 文档](https://zh.cppreference.com/w/cpp/container/vector)．

#### 构造函数

用例参见如下代码（假设你已经 `using` 了 `std` 命名空间相关类型）：

```cpp
// 1. 创建空vector; 常数复杂度
vector<int> v0;
// 1+. 这句代码可以使得向vector中插入前3个元素时，保证常数时间复杂度
v0.reserve(3);
// 2. 创建一个初始空间为3的vector，其元素的默认值是0; 线性复杂度
vector<int> v1(3);
// 3. 创建一个初始空间为3的vector，其元素的默认值是2; 线性复杂度
vector<int> v2(3, 2);
// 4. 创建一个初始空间为3的vector，其元素的默认值是1，
// 并且使用v2的空间配置器; 线性复杂度
vector<int> v3(3, 1, v2.get_allocator());
// 5. 创建一个v2的拷贝vector v4， 其内容元素和v2一样; 线性复杂度
vector<int> v4(v2);
// 6. 创建一个v4的拷贝vector v5，其内容是{v4[1], v4[2]}; 线性复杂度
vector<int> v5(v4.begin() + 1, v4.begin() + 3);
// 7. 移动v2到新创建的vector v6，不发生拷贝; 常数复杂度; 需要 C++11
vector<int> v6(std::move(v2));  // 或者 v6 = std::move(v2);
```

??? note "测试代码"
    ```cpp
    // 以下是测试代码，有兴趣的同学可以自己编译运行一下本代码．
    cout << "v1 = ";
    copy(v1.begin(), v1.end(), ostream_iterator<int>(cout, " "));
    cout << endl;
    cout << "v2 = ";
    copy(v2.begin(), v2.end(), ostream_iterator<int>(cout, " "));
    cout << endl;
    cout << "v3 = ";
    copy(v3.begin(), v3.end(), ostream_iterator<int>(cout, " "));
    cout << endl;
    cout << "v4 = ";
    copy(v4.begin(), v4.end(), ostream_iterator<int>(cout, " "));
    cout << endl;
    cout << "v5 = ";
    copy(v5.begin(), v5.end(), ostream_iterator<int>(cout, " "));
    cout << endl;
    cout << "v6 = ";
    copy(v6.begin(), v6.end(), ostream_iterator<int>(cout, " "));
    cout << endl;
    ```

可以利用上述的方法构造一个 `vector`，足够我们使用了．

#### 元素访问

`vector` 提供了如下几种方法进行元素访问

1.  `at()`

    `v.at(pos)` 返回容器中下标为 `pos` 的引用．如果数组越界抛出 `std::out_of_range` 类型的异常．

2.  `operator[]`

    `v[pos]` 返回容器中下标为 `pos` 的引用．不执行越界检查．

3.  `front()`

    `v.front()` 返回首元素的引用．

4.  `back()`

    `v.back()` 返回末尾元素的引用．

5.  `data()`

    `v.data()` 返回 `v` 内部存储数据使用的连续内存空间中首元素的指针．

#### 迭代器

vector 提供了如下几种 [迭代器](./iterator.md)

1.  `begin()/cbegin()`

    返回指向首元素的迭代器，其中 `*begin = front`．

2.  `end()/cend()`

    返回指向容器尾端占位符的迭代器，注意是没有元素的．

3.  `rbegin()/crbegin()`

    返回指向逆向数组的首元素的逆向迭代器，可以理解为正向容器的末元素．

4.  `rend()/crend()`

    返回指向逆向数组末元素后一位置的迭代器，对应容器首的前一个位置，没有元素．

以上列出的迭代器中，含有字符 `c` 的为只读迭代器，你不能通过只读迭代器去修改 `vector` 中的元素的值．如果一个 `vector` 本身就是只读的，那么它的一般迭代器和只读迭代器完全等价．只读迭代器自 C++11 开始支持．

#### 长度和容量

`vector` 有以下几个与容器长度和容量相关的函数．注意，`vector` 的长度（size）指有效元素数量，而容量（capacity）指其实际分配的内存长度，相关细节请参见后文的实现细节介绍．

**与长度相关**：

-   `empty()` 返回一个 `bool` 值，即 `v.begin() == v.end()`，`true` 为空，`false` 为非空．

-   `size()` 返回容器长度（元素数量），即 `std::distance(v.begin(), v.end())`．

-   `resize(n)` 改变 `vector` 的长度为 `n`．如果 `n` 大于当前长度，则会补充元素，如果参数中提供了要补充的元素，则使用参数，否则使用默认值；如果 `n` 小于当前长度，则保留前 `n` 个元素，后续元素删除．

-   `max_size()` 返回容器的最大可能长度．

    **与容量相关**：

-   `reserve()` 使得 `vector` 预留一定的内存空间，避免不必要的内存分配与拷贝．

-   `capacity()` 返回容器的容量，即当前 `vector` 已经为多少个元素分配了空间．

-   `shrink_to_fit()` 使得 `vector` 的容量与长度一致，去除该 `vector` 没有用到的容量．

### 元素增删及修改

-   `clear()` 清除所有元素
-   `insert()` 支持在某个迭代器位置插入元素、可以插入多个．**复杂度与 `pos` 距离末尾长度成线性而非常数的**
-   `erase()` 删除某个迭代器或者区间的元素，返回最后被删除的迭代器．复杂度与 `insert` 一致．
-   `push_back()` 在末尾插入一个元素，均摊复杂度为 **常数**，最坏为线性复杂度．
-   `pop_back()` 删除末尾元素，常数复杂度．
-   `swap()` 与另一个容器进行交换，此操作是 **常数复杂度** 而非线性的．

### `vector` 的实现细节

`vector` 的底层其实仍然是定长数组，它能够实现动态扩容的原因是增加了避免数量溢出的操作．首先需要指明的是 `vector` 中元素的数量（长度）$n$ 与它已分配内存最多能包含元素的数量（容量）$N$ 是不一致的，`vector` 会分开存储这两个量．当向 `vector` 中添加元素时，如发现 $n>N$，那么容器会分配一个尺寸为 $2N$ 的数组，然后将旧数据从原本的位置拷贝到新的数组中，再将原来的内存释放．尽管这个操作的渐近复杂度是 $O(n)$，但是可以证明其均摊复杂度为 $O(1)$．而在末尾删除元素和访问元素则都仍然是 $O(1)$ 的开销．
因此，只要对 `vector` 的尺寸估计得当并善用 `resize()` 和 `reserve()`，就能使得 `vector` 的效率与定长数组不会有太大差距．

### `vector<bool>`

标准库特别提供了对 `bool` 的 `vector` 特化，每个「`bool`」只占 1 bit，且支持动态增长．但是其 `operator[]` 的返回值的类型不是 `bool&` 而是 `vector<bool>::reference`．因此，使用 `vector<bool>` 使需谨慎，可以考虑使用 `deque<bool>` 或 `vector<char>` 替代．而如果你需要节省空间，请直接使用 [`bitset`](./bitset.md)．

## `array`(C++11)

`std::array` 是 STL 提供的 **内存连续的**、**固定长度** 的数组数据结构．其本质是对原生数组的直接封装．

### 为什么要用 `array`

`array` 实际上是 STL 对数组的封装．它相比 `vector` 牺牲了动态扩容的特性，但是换来了与原生数组几乎一致的性能（在开满优化的前提下）．因此如果能使用 C++11 特性的情况下，能够使用原生数组的地方几乎都可以直接把定长数组都换成 `array`，而动态分配的数组可以替换为 `vector`．

### 成员函数

#### 隐式定义的成员函数

| 函数          | 作用                                  |
| ----------- | ----------------------------------- |
| `operator=` | 以来自另一 `array` 的每个元素重写 `array` 的对应元素 |

#### 元素访问

| 函数           | 作用                   |
| ------------ | -------------------- |
| `at`         | 访问指定的元素，同时进行越界检查     |
| `operator[]` | 访问指定的元素，**不** 进行越界检查 |
| `front`      | 访问第一个元素              |
| `back`       | 访问最后一个元素             |
| `data`       | 返回指向内存中数组第一个元素的指针    |

`at` 若遇 `pos >= size()` 的情况会抛出 `std::out_of_range`．

#### 容量

| 函数         | 作用          |
| ---------- | ----------- |
| `empty`    | 检查容器是否为空    |
| `size`     | 返回容纳的元素数    |
| `max_size` | 返回可容纳的最大元素数 |

由于每个 `array` 都是固定大小容器，`size()` 返回的值等于 `max_size()` 返回的值．

### 操作

| 函数     | 作用       |
| ------ | -------- |
| `fill` | 以指定值填充容器 |
| `swap` | 交换内容     |

**注意，交换两个 `array` 是 $\Theta(\text{size})$ 的，而非与常规 STL 容器一样为 $O(1)$．**

### 非成员函数

| 函数             | 作用                  |
| -------------- | ------------------- |
| `operator==` 等 | 按照字典序比较 `array` 中的值 |
| `std::get`     | 访问 `array` 的一个元素    |
| `std::swap`    | 特化的 `std::swap` 算法  |

下面是一个 `array` 的使用示例：

```cpp
// 1. 创建空array，长度为3; 常数复杂度
std::array<int, 3> v0;
// 2. 用指定常数创建array; 常数复杂度
std::array<int, 3> v1{1, 2, 3};

v0.fill(1);  // 填充数组

// 访问数组
for (int i = 0; i != arr.size(); ++i) cout << arr[i] << " ";
```

## `deque`

`std::deque` 是 STL 提供的 [双端队列](../../ds/queue.md#双端队列) 数据结构．能够提供线性复杂度的插入和删除，以及常数复杂度的随机访问．

### `deque` 的使用方法

以下介绍常用用法，详细内容 [请参见 C++ 文档](https://zh.cppreference.com/w/cpp/container/deque)．`deque` 的迭代器函数与 `vector` 相同，因此不作详细介绍．

#### 构造函数

参见如下代码（假设你已经 `using` 了 `std` 命名空间相关类型）：

```cpp
// 1. 定义一个int类型的空双端队列 v0
deque<int> v0;
// 2. 定义一个int类型的双端队列 v1，并设置初始大小为10; 线性复杂度
deque<int> v1(10);
// 3. 定义一个int类型的双端队列 v2，并初始化为10个1; 线性复杂度
deque<int> v2(10, 1);
// 4. 复制已有的双端队列 v1; 线性复杂度
deque<int> v3(v1);
// 5. 创建一个v2的拷贝deque v4，其内容是v4[0]至v4[2]; 线性复杂度
deque<int> v4(v2.begin(), v2.begin() + 3);
// 6. 移动v2到新创建的deque v5，不发生拷贝; 常数复杂度; 需要 C++11
deque<int> v5(std::move(v2));
```

#### 元素访问

与 `vector` 一致，但无法访问底层内存．其高效的元素访问速度可参考实现细节部分．

-   `at()` 返回容器中指定位置元素的引用，执行越界检查，**常数复杂度**．
-   `operator[]` 返回容器中指定位置元素的引用．不执行越界检查，**常数复杂度**．
-   `front()` 返回首元素的引用．
-   `back()` 返回末尾元素的引用．

#### 迭代器

与 `vector` 一致．

#### 长度

与 `vector` 一致，但是没有 `reserve()` 和 `capacity()` 函数．（仍然有 `shrink_to_fit()` 函数）

#### 元素增删及修改

与 `vector` 一致，并额外有向队列头部增加元素的函数．

-   `clear()` 清除所有元素
-   `insert()` 支持在某个迭代器位置插入元素、可以插入多个．**复杂度与 `pos` 与两端距离较小者成线性**．
-   `erase()` 删除某个迭代器或者区间的元素，返回最后被删除的迭代器．复杂度与 `insert` 一致．
-   `push_front()` 在头部插入一个元素，**常数复杂度**．
-   `pop_front()` 删除头部元素，**常数复杂度**．
-   `push_back()` 在末尾插入一个元素，**常数复杂度**．
-   `pop_back()` 删除末尾元素，**常数复杂度**．
-   `swap()` 与另一个容器进行交换，此操作是 **常数复杂度** 而非线性的．

### `deque` 的实现细节

`deque` 通常的底层实现是多个不连续的缓冲区，而缓冲区中的内存是连续的．而每个缓冲区还会记录首指针和尾指针，用来标记有效数据的区间．当一个缓冲区填满之后便会在之前或者之后分配新的缓冲区来存储更多的数据．更详细的说明可以参考 [《STL 源码剖析》deque 实现原理](https://www.cnblogs.com/q1076452761/p/16903229.html)．

## `list`

`std::list` 是 STL 提供的 [双向链表](../../ds/linked-list.md) 数据结构．能够提供线性复杂度的随机访问，以及常数复杂度的插入和删除．

### `list` 的使用方法

`list` 的使用方法与 `deque` 基本相同，但是增删操作和访问的复杂度不同．详细内容 [请参见 C++ 文档](https://zh.cppreference.com/w/cpp/container/list)．`list` 的迭代器、长度、元素增删及修改相关的函数与 `deque` 相同，因此不作详细介绍．

#### 元素访问

由于 `list` 的实现是链表，因此它不提供随机访问的接口．若需要访问中间元素，则需要使用迭代器．

-   `front()` 返回首元素的引用．
-   `back()` 返回末尾元素的引用．

#### 操作

`list` 类型还提供了一些针对其特性实现的 STL 算法函数．由于这些算法需要 [随机访问迭代器](./iterator.md)，因此 `list` 提供了特别的实现以便于使用．这些算法有 `splice()`、`remove()`、`sort()`、`unique()`、`merge()` 等．

## `forward_list`（C++11）

`std::forward_list` 是 STL 提供的 [单向链表](../../ds/linked-list.md) 数据结构，相比于 `std::list` 减小了空间开销．

### `forward_list` 的使用方法

`forward_list` 的使用方法与 `list` 几乎一致，但是迭代器只有单向的，因此其具体用法不作详细介绍．详细内容 [请参见 C++ 文档](https://zh.cppreference.com/w/cpp/container/forward_list)


## lang/csl/string.md

author: johnvp22, Ir1d

## `string` 是什么

`std::string` 是在标准库 `<string>`（注意不是 C 语言中的 `<string.h>` 库）中提供的一个类，本质上是 `std::basic_string<char>` 的别称．

## 为什么要使用 `string`

在 C 语言中，提供了字符串的操作，但只能通过字符数组的方式来实现字符串．而 `string` 则是一个简单的类，使用简单，在 OI 竞赛中被广泛使用．并且相较于其他 STL 容器，`string` 的常数可以算是非常优秀的，基本与字符数组不相上下．

### `string` 可以动态分配空间

和许多 STL 容器相同，`string` 能动态分配空间，这使得我们可以直接使用 `std::cin` 来输入，但其速度则同样较慢．这一点也同样让我们不必为内存而烦恼．

### `string` 重载了加法运算符和比较运算符

`string` 的加法运算符可以直接拼接两个字符串或一个字符串和一个字符．和 `std::vector` 类似，`string` 重载了比较运算符，同样是按字典序比较的，所以我们可以直接调用 `std::sort` 对若干字符串进行排序．

## 使用方法

下面介绍 `string` 的基本操作，具体可看 [C++ 文档](https://zh.cppreference.com/w/cpp/string/basic_string)．

### 声明

```cpp
std::string s;
```

### 转 char 数组

在 C 语言里，也有很多字符串的函数，但是它们的参数都是 char 指针类型的，为了方便使用，`string` 有两个成员函数能够将自己转换为 char 指针——`data()`/`c_str()`（在 C++11 之前，`c_str()` 保证末尾有空字符，而 `data()` 不保证；C++11 后两者行为一致[^string1]），如：

```cpp
printf("%s", s);          // 不能保证编译通过，行为未定义
printf("%s", s.data());   // C++11 前行为未定义，C++11 后正确输出
printf("%s", s.c_str());  // 一定能够正确输出
```

### 获取长度

很多函数都可以返回 string 的长度：

```cpp
printf("s 的长度为 %zu", s.size());
printf("s 的长度为 %zu", s.length());
printf("s 的长度为 %zu", strlen(s.c_str()));
```

???+ note "这些函数的复杂度"
    `strlen()` 的复杂度一定是与字符串长度线性相关的．
    
    `size()` 和 `length()` 的复杂度在 C++98 中没有指定，在 C++11 中被指定为常数复杂度．但在常见的编译器上，即便是 C++98，这两个函数的复杂度也是常数．

???+ warning "Warning"
    这三个函数（以及下面将要提到的 `find` 函数）的返回值类型都是 `size_t`（`unsigned long`）．因此，这些返回值不支持直接与负数比较或运算，建议在需要时进行强制转换．

### 寻找某字符（串）第一次出现的位置

`find(str,pos)` 函数可以用来查找字符串中一个字符/字符串在 `pos`（含）之后第一次出现的位置（若不传参给 `pos` 则默认为 `0`）．如果没有出现，则返回 `string::npos`（被定义为 `-1`，但类型仍为 `size_t`/`unsigned long`）．

示例：

```cpp
string s = "OI Wiki", t = "OI", u = "i";
int pos = 5;
printf("字符 I 在 s 的 %lu 位置第一次出现\n", s.find('I'));
printf("字符 a 在 s 的 %lu 位置第一次出现\n", s.find('a'));
printf("字符 a 在 s 的 %d 位置第一次出现\n", s.find('a'));
printf("字符串 t 在 s 的 %lu 位置第一次出现\n", s.find(t));
printf("在 s 中自 pos 位置起字符串 u 第一次出现在 %lu 位置", s.find(u, pos));
```

输出：

```text
字符 I 在 s 的 1 位置第一次出现
字符 a 在 s 的 18446744073709551615 位置第一次出现 // 即为 size_t(-1)，具体数值与平台有关．
字符 a 在 s 的 -1 位置第一次出现 // 强制转换为 int 类型则正常输出 -1
字符串 t 在 s 的 0 位置第一次出现
在 s 中自 pos 位置起字符串 u 第一次出现在 6 位置
```

### 截取子串

`substr(pos, len)` 函数返回从 `pos` 位置开始截取最多 `len` 个字符组成的字符串（如果从 `pos` 开始的后缀长度不足 `len` 则截取这个后缀）．

示例：

```cpp
string s = "OI Wiki", t = "OI";
printf("从字符串 s 的第四位开始的最多三个字符构成的子串是 %s\n",
       s.substr(3, 3).c_str());
printf("从字符串 t 的第二位开始的最多三个字符构成的子串是 %s",
       t.substr(1, 3).c_str());
```

输出：

```text
从字符串 s 的第四位开始的最多三个字符构成的子串是 Wik
从字符串 t 的第二位开始的最多三个字符构成的子串是 I
```

### 插入/删除字符（串）

`insert(index,count,ch)` 和 `insert(index,str)` 是比较常见的插入函数．它们分别表示在 `index` 处连续插入 `count` 次字符串 `ch` 和插入字符串 `str`．

`erase(index,count)` 函数将字符串 `index` 位置开始（含）的 `count` 个字符删除（若不传参给 `count` 则表示删去 `index` 位置及以后的所有字符）．

示例：

```cpp
string s = "OI Wiki", t = " Wiki";
char u = '!';
s.erase(2);
printf("从字符串 s 的第三位开始删去所有字符后得到的字符串是 %s\n", s.c_str());
s.insert(2, t);
printf("在字符串 s 的第三位处插入字符串 t 后得到的字符串是 %s\n", s.c_str());
s.insert(7, 3, u);
printf("在字符串 s 的第八位处连续插入 3 次字符串 u 后得到的字符串是 %s",
       s.c_str());
```

输出：

```text
从字符串 s 的第三位开始删去所有字符后得到的字符串是 OI
在字符串 s 的第三位处插入字符串 t 后得到的字符串是 OI Wiki
在字符串 s 的第八位处连续插入 3 次字符串 u 后得到的字符串是 OI Wiki!!!
```

### 替换字符（串）

`replace(pos,count,str)` 和 `replace(first,last,str)` 是比较常见的替换函数．它们分别表示将从 `pos` 位置开始 `count` 个字符的子串替换为 `str` 以及将以 `first` 开始（含）、`last` 结束（不含）的子串替换为 `str`，其中 `first` 和 `last` 均为迭代器．

示例：

```cpp
string s = "OI Wiki";
s.replace(2, 5, "");
printf("将字符串 s 的第 3~7 位替换为空串后得到的字符串是 %s\n", s.c_str());
s.replace(s.begin(), s.begin() + 2, "NOI");
printf("将字符串 s 的前两位替换为 NOI 后得到的字符串是 %s", s.c_str());
```

输出：

```text
将字符串 s 的第 3~7 位替换为空串后得到的字符串是 OI
将字符串 s 的前两位替换为 NOI 后得到的字符串是 NOI
```

## 参考资料与注释

[^string1]: [C++ 标准草案 \[basic.string\]](https://eel.is/c++draft/basic.string#general-3)


## lang/csl/unordered-container.md

## 概述

自 C++11 标准起，四种基于 [哈希](../../ds/hash.md) 实现的无序关联式容器正式纳入了 C++ 的标准模板库中，分别是：`unordered_set`，`unordered_multiset`，`unordered_map`，`unordered_multimap`．

??? note "编译器不支持 C++11 的使用方法"
    在 C++11 之前，无序关联式容器属于 C++ 的 TR1 扩展．所以，如果编译器不支持 C++11，在使用时需要在头文件的名称中加入 `tr1/` 前缀，并且使用 `std::tr1` 命名空间．如 `#include <unordered_map>` 需要改成 `#include <tr1/unordered_map>`；`std::unordered_map` 需要改为 `std::tr1::unordered_map`（如果使用 `using namespace std;`，则为 `tr1::unordered_map`）．

它们与相应的关联式容器在功能，函数等方面有诸多共同点，而最大的不同点则体现在普通的关联式容器一般采用红黑树实现，内部元素按特定顺序进行排序；而这几种无序关联式容器则采用哈希方式存储元素，内部元素不以任何特定顺序进行排序，所以访问无序关联式容器中的元素时，访问顺序也没有任何保证．

采用哈希存储的特点使得无序关联式容器 **在平均情况下** 大多数操作（包括查找，插入，删除）都能在常数时间复杂度内完成，相较于关联式容器与容器大小成对数的时间复杂度更加优秀．

??? warning "Warning"
    在最坏情况下，对无序关联式容器进行插入、删除、查找等操作的时间复杂度会 **与容器大小成线性关系**！这一情况往往在容器内出现大量哈希冲突时产生．
    
    同时，由于无序关联式容器的操作时通常存在较大的常数，其效率有时并不比普通的关联式容器好太多．
    
    因此应谨慎使用无序关联式容器，尽量避免滥用（例如懒得离散化，直接将 `unordered_map<int, int>` 当作空间无限的普通数组使用）．

由于无序关联式容器与相应的关联式容器在用途和操作中有很多共同点，这里不再介绍无序关联式容器的各种操作，这些内容读者可以参考 [关联式容器](./associative-container.md)．

## 制造哈希冲突

上文中提到了，在最坏情况下，对无序关联式容器进行一些操作的时间复杂度会与容器大小成线性关系．

在哈希函数确定的情况下，可以构造出数据使得容器内产生大量哈希冲突，导致复杂度达到上界．

在标准库实现里，每个元素的散列值是将值对一个质数取模得到的，更具体地说，是 [这个列表](https://github.com/gcc-mirror/gcc/blob/releases/gcc-8.1.0/libstdc%2B%2B-v3/src/shared/hashtable-aux.cc) 中的质数（g++ 6 及以前版本的编译器，这个质数一般是 $126271$，g++ 7 及之后版本的编译器，这个质数一般是 $107897$）．

因此可以通过向容器中插入这些模数的倍数来达到制造大量哈希冲突的目的．

## 自定义哈希函数

使用自定义哈希函数可以有效避免构造数据产生的大量哈希冲突．

要想使用自定义哈希函数，需要定义一个结构体，并在结构体中重载 `()` 运算符，像这样：

```cpp
struct my_hash {
  size_t operator()(int x) const { return x; }
};
```

当然，为了确保哈希函数不会被迅速破解（例如 Codeforces 中对使用无序关联式容器的提交进行 hack），可以试着在哈希函数中加入一些随机化函数（如时间）来增加破解的难度．

例如，在 [这篇博客](https://codeforces.com/blog/entry/62393) 中给出了如下哈希函数：

```cpp
struct my_hash {
  static uint64_t splitmix64(uint64_t x) {
    x += 0x9e3779b97f4a7c15;
    x = (x ^ (x >> 30)) * 0xbf58476d1ce4e5b9;
    x = (x ^ (x >> 27)) * 0x94d049bb133111eb;
    return x ^ (x >> 31);
  }

  size_t operator()(uint64_t x) const {
    static const uint64_t FIXED_RANDOM =
        chrono::steady_clock::now().time_since_epoch().count();
    return splitmix64(x + FIXED_RANDOM);
  }

  // 针对 std::pair<int, int> 作为主键类型的哈希函数
  size_t operator()(pair<uint64_t, uint64_t> x) const {
    static const uint64_t FIXED_RANDOM =
        chrono::steady_clock::now().time_since_epoch().count();
    return splitmix64(x.first + FIXED_RANDOM) ^
           (splitmix64(x.second + FIXED_RANDOM) >> 1);
  }
};
```

写完自定义的哈希函数后，就可以通过 `unordered_map<int, int, my_hash> my_map;` 或者 `unordered_map<pair<int, int>, int, my_hash> my_pair_map;` 的定义方式将自定义的哈希函数传入容器了．


## lang/file-op.md

author: Ir1d, cqnuljs, akakw1, MingqiHuang, Chrogeek, henrytbtrue, Planet6174, StudyingFather

## 文件的概念

文件是根据特定的目的而收集在一起的有关数据的集合．C/C++ 把每一个文件都看成是一个有序的字节流，每个文件都是以 **文件结束标志**（EOF）结束，如果要操作某个文件，程序应该首先打开该文件，每当一个文件被打开后（请记得关闭打开的文件），该文件就和一个流关联起来，这里的流实际上是一个字节序列．

C/C++ 将文件分为文本文件和二进制文件．文本文件就是简单的文本文件（重点），另外二进制文件就是特殊格式的文件或者可执行代码文件等．

## 文件的操作步骤

1、打开文件，将文件指针指向文件，决定打开文件类型；  
2、对文件进行读、写操作（比赛中主要用到的操作，其他一些操作暂时不写）；  
3、在使用完文件后，关闭文件．

## `freopen` 函数

### 函数简介

函数用于将指定输入输出流以指定方式重定向到文件，包含于头文件 `stdio.h (cstdio)` 中，该函数可以在不改变代码原貌的情况下改变输入输出环境，但使用时应当保证流是可靠的．

函数主要有三种方式：读、写和附加．

### 命令格式

```cpp
FILE* freopen(const char* filename, const char* mode, FILE* stream);
```

### 参数说明

-   `filename`: 要打开的文件名
-   `mode`: 文件打开的模式，表示文件访问的权限
-   `stream`: 文件指针，通常使用标准文件流 (`stdin/stdout`) 或标准错误输出流 (`stderr`)
-   返回值：文件指针，指向被打开文件

### 文件打开格式（选读）

-   `r`：以只读方式打开文件，文件必须存在，只允许读入数据 **（常用）**
-   `r+`：以读/写方式打开文件，文件必须存在，允许读/写数据
-   `rb`：以只读方式打开二进制文件，文件必须存在，只允许读入数据
-   `rb+`：以读/写方式打开二进制文件，文件必须存在，允许读/写数据
-   `rt+`：以读/写方式打开文本文件，允许读/写数据
-   `w`：以只写方式打开文件，文件不存在会新建文件，否则清空内容，只允许写入数据 **（常用）**
-   `w+`：以读/写方式打开文件，文件不存在将新建文件，否则清空内容，允许读/写数据
-   `wb`：以只写方式打开二进制文件，文件不存在将会新建文件，否则清空内容，只允许写入数据
-   `wb+`：以读/写方式打开二进制文件，文件不存在将新建文件，否则清空内容，允许读/写数据
-   `a`：以只写方式打开文件，文件不存在将新建文件，写入数据将被附加在文件末尾（保留 EOF 符）
-   `a+`：以读/写方式打开文件，文件不存在将新建文件，写入数据将被附加在文件末尾（不保留 EOF 符）
-   `at+`：以读/写方式打开文本文件，写入数据将被附加在文件末尾
-   `ab+`：以读/写方式打开二进制文件，写入数据将被附加在文件末尾

### 使用方法

读入文件内容：

```cpp
freopen("data.in", "r", stdin);
// data.in 就是读取的文件名，要和可执行文件放在同一目录下
```

输出到文件：

```cpp
freopen("data.out", "w", stdout);
// data.out 就是输出文件的文件名，和可执行文件在同一目录下
```

关闭标准输入/输出流

```cpp
fclose(stdin);
fclose(stdout);
```

??? note "注"
    `printf/scanf/cin/cout` 等函数默认使用 `stdin/stdout`，将 `stdin/stdout` 重定向后，这些函数将输入/输出到被定向的文件

### 模板

```cpp
#include <cstdio>
#include <iostream>

int main(void) {
  freopen("data.in", "r", stdin);
  freopen("data.out", "w", stdout);
  /*
  中间的代码不需要改变，直接使用 cin 和 cout 即可
  */
  fclose(stdin);
  fclose(stdout);
  return 0;
}
```

## `fopen` 函数（选读）

函数大致与 `freopen` 相同，函数将打开指定文件并返回打开文件的指针

### 函数原型

```cpp
FILE* fopen(const char* path, const char* mode)
```

各项参数含义同 `freopen`

### 可用读写函数（基本）

-   `fread/fwrite`
-   `fgetc/fputc`
-   `fscanf/fprintf`
-   `fgets/fputs`

### 使用方式

```cpp
FILE *in, *out;  // 定义文件指针
in = fopen("data.in", "r");
out = fopen("data.out", "w");
/*
do what you want to do
*/
fclose(in);
fclose(out);
```

## C++ 的 `ifstream/ofstream` 文件输入输出流

### 使用方法

读入文件内容：

```cpp
ifstream fin("data.in");
// data.in 就是读取文件的相对位置或绝对位置
```

输出到文件：

```cpp
ofstream fout("data.out");
// data.out 就是输出文件的相对位置或绝对位置
```

关闭标准输入/输出流

```cpp
fin.close();
fout.close();
```

### 模板

```cpp
#include <fstream>
using namespace std;  // 两个类型都在 std 命名空间里

ifstream fin("data.in");
ofstream fout("data.out");

int main(void) {
  /*
  中间的代码改变 cin 为 fin ，cout 为 fout 即可
  */
  fin.close();
  fout.close();
  return 0;
}
```

## 参考资料

1.  信息学奥赛一本通


## lang/func.md

author: Ir1d, tsagaanbar, yang-lile

## 函数的声明

编程中的函数（function）一般是若干语句的集合．我们也可以将其称作「**子过程**（subroutine）」．在编程中，如果有一些重复的过程，我们可以将其提取出来，形成一个函数．函数可以接收若干值，这叫做函数的参数．函数也可以返回某个值，这叫做函数的返回值．

声明一个函数，我们需要返回值类型、函数的名称，以及参数列表．

```cpp
// 返回值类型 int
// 函数的名称 some_function
// 参数列表 int, int
int some_function(int, int);
```

如上图，我们声明了一个名为 `some_function` 的函数，它需要接收两个 `int` 类型的参数，返回值类型也为 `int`．可以认为，这个函数将会对传入的两个整数进行一些操作，并且返回一个同样类型的结果．

## 实现函数：编写函数的定义

只有函数的声明（declaration）还不够，他只能让我们在调用时能够得知函数的 **接口** 类型（即接收什么数据、返回什么数据），但其缺乏具体的内部实现，也就是函数的 **定义**（definition）．我们可以在 **声明之后的其他地方** 编写代码 **实现**（implement）这个函数（也可以在另外的文件中实现，但是需要将分别编译后的文件在链接时一并给出）．

如果函数有返回值，则需要通过 `return` 语句，将值返回给调用方．函数一旦执行到 `return` 语句，则直接结束当前函数，不再执行后续的语句．

```cpp
int some_function(int, int);  // 声明

/* some other code here... */

int some_function(int x, int y) {  // 定义
  int result = 2 * x + y;
  return result;
  result = 3;  // 这条语句不会被执行
}
```

在定义时，我们给函数的参数列表的变量起了名字．这样，我们便可以在函数定义中使用这些变量了．

如果是同一个文件中，我们也可以直接将 **声明和定义合并在一起**，换句话说，也就是在声明时就完成定义．

```cpp
int some_function(int x, int y) { return 2 * x + y; }
```

如果函数不需要有返回值，则将函数的返回值类型标为 `void`；如果函数不需要参数，则可以将参数列表置空．同样，无返回值的函数执行到 `return;` 语句也会结束执行．

```cpp
void say_hello() {
  cout << "hello!\n";
  cout << "hello!\n";
  cout << "hello!\n";
  return;
  cout << "hello!\n";  // 这条语句不会被执行
}
```

## 函数的调用

和变量一样，函数需要先被声明，才能使用．使用函数的行为，叫做「调用（call）」．我们可以在任何函数内部调用其他函数，包括这个函数自身．函数调用自身的行为，称为 **递归**（recursion）．

在大多数语言中，调用函数的写法，是 **函数名称加上一对括号** `()`，如 `foo()`．如果函数需要参数，则我们将其需要的参数按顺序填写在括号中，以逗号间隔，如 `foo(1, 2)`．函数的调用也是一个表达式，**函数的返回值** 就是 **表达式的值**．

函数声明时候写出的参数，可以理解为在函数 **当前次调用的内部** 可以使用的变量，这些变量的值由调用处传入的值初始化．看下面这个例子：

```cpp
void foo(int, int);

/* ... */

void foo(int x, int y) {
  x = x * 2;
  y = y + 3;
}

/* ... */

a = 1;
b = 1;
// 调用前：a = 1, b = 1
foo(a, b);  // 调用 foo
            // 调用后：a = 1, b = 1
```

在上面的例子中，`foo(a, b)` 是一次对 `foo` 的调用．调用时，`foo` 中的 `x` 和 `y` 变量，分别由调用处 `a` 和 `b` 的值初始化．因此，在 `foo` 中对变量 `x` 和 `y` 的修改，**并不会影响到调用处的变量的值**．

如果我们需要在函数（子过程）中修改变量的值，则需要采用「传引用」的方式．

```cpp
void foo(int& x, int& y) {
  x = x * 2;
  y = y + 3;
}

/* ... */

a = 1;
b = 1;
// 调用前：a = 1, b = 1
foo(a, b);  // 调用 foo
            // 调用后：a = 2, b = 4
```

上述代码中，我们看到函数参数列表中的「`int`」后面添加了一个「`&`（and 符号）」，这表示对于 `int` 类型的 **引用**（reference）．在调用 `foo` 时，调用处 `a` 和 `b` 变量分别初始化了 `foo` 中两个对 `int` 类型的引用 `x` 和 `y`．在 `foo` 中的 `x` 和 `y`，可以理解为调用处 `a` 和 `b` 变量的「别名」，即 `foo` 中对 `x` 和 `y` 的操作，就是对调用处 `a` 和 `b` 的操作．

## `main` 函数

特别的，每个 C/C++ 程序都需要有一个名为 `main` 的函数．任何程序都将从 `main` 函数开始运行．

> `main` 函数也可以有参数，通过 `main` 函数的参数，我们可以获得外界传给这个程序的指令（也就是「命令行参数」），以便做出不同的反应．

下面是一段调用了函数（子过程）的代码：

```cpp
// hello_subroutine.cpp

#include <iostream>

void say_hello() {
  std::cout << "hello!\n";
  std::cout << "hello!\n";
  std::cout << "hello!\n";
}

int main() {
  say_hello();
  say_hello();
}
```


## lang/helloworld.md

disqus:

## 环境配置

工欲善其事，必先利其器．

### 集成开发环境

IDE 操作较为简单，一般入门玩家会选用 IDE 来编写代码．在竞赛中最常见的是 [Dev-C++](../tools/editor/devcpp.md)（如果考试环境是 Windows 系统，一般也会提供这一 IDE）．

### 编译器

#### Windows

推荐使用 GNU 编译器．需要去 [MinGW Distro](https://nuwen.net/mingw.html) 下载 MinGW 并安装．此外 Windows 下也可以选择 [Microsoft Visual C++ 编译器](https://docs.microsoft.com/en-us/cpp/build/projects-and-build-systems-cpp)，需要去 [Visual Studio 页面](https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2019) 下载安装．

#### macOS

在终端中执行：

```bash
xcode-select --install
```

#### Linux

使用 `g++ -v` 来检查是否安装过 `g++`．

使用如下命令可以安装：

```bash
sudo apt update && sudo apt install g++
```

#### 在命令行中编译代码

熟练之后也有玩家会使用更灵活的命令行来编译代码，这样就不依赖 IDE 了，而是使用自己熟悉的文本编辑器编写代码．

```bash
g++ test.cpp -o test -lm
```

`g++` 是 C++ 语言的编译器（C 语言的编译器为 `gcc`），`-o` 用于指定可执行文件的文件名，编译选项 `-lm` 用于链接数学库 `libm`，从而使得使用 `math.h` 的代码可以正常编译运行．

注：C++ 程序不需要 `-lm` 即可正常编译运行．历年 NOI/NOIP 试题的 C++ 编译选项中都带着 `-lm`，故这里也一并加上．

## 第一份代码

通过这样一个示例程序来展开 C++ 入门之旅吧～

注：请在编写前注意开启英文输入法．

C++ 语言

```cpp
#include <iostream>  // 引用头文件

int main() {                     // 定义 main 函数
  std::cout << "Hello, world!";  // 使用标准命名空间中的 cout 函数
  return 0;  // 返回 0，结束 main 函数．编译器一般会自动加上这一行，一般可以省略
}
```

C 语言

```c
#include <stdio.h>  // 引用头文件

int main() {                // 定义 main 函数
  printf("Hello, world!");  // 输出 Hello, world!
  return 0;                 // 返回 0，结束 main 函数
}
```

注意：C 语言在这里仅做参考，C++ 基本兼容 C 语言，并且拥有许多新的功能，可以让选手在赛场上事半功倍．具体请见 [C++ 与其他常用语言区别](./cpp-other-langs.md)


## lang/java-pro.md

???+ warning "注意"
    以下内容均基于 Java JDK 8 版本编写，不排除在更高版本中有部分改动的可能性．

## 更高速的输入输出

`Scanner` 和 `System.out.print` 在最开始会工作得很好，但是在处理更大的输入的时候会降低效率，因此我们会需要使用一些方法来提高 IO 速度．

### 使用 Kattio + StringTokenizer 作为输入

最常用的方法之一是使用来自 Kattis 的 [Kattio.java](https://github.com/Kattis/kattio/blob/master/Kattio.java) 来提高 IO 效率．[^ref1]这个方法会将 `StringTokenizer` 与 `PrintWriter` 包装在一个类中方便使用．而在具体进行解题的时候（假如赛会/组织方允许）可以直接使用这个模板．

下方即为应包含在代码中的 IO 模板，由于 Kattis 的原 Kattio 包含一些并不常用的功能，下方的模板经过了一些调整（原 Kattio 使用 MIT 作为协议）．

```java
class Kattio extends PrintWriter {
    private BufferedReader r;
    private StringTokenizer st;
    // 标准 IO
    public Kattio() { this(System.in, System.out); }
    public Kattio(InputStream i, OutputStream o) {
        super(o);
        r = new BufferedReader(new InputStreamReader(i));
    }
    // 文件 IO
    public Kattio(String intput, String output) throws IOException {
        super(output);
        r = new BufferedReader(new FileReader(intput));
    }
    // 在没有其他输入时返回 null
    public String next() {
        try {
            while (st == null || !st.hasMoreTokens())
                st = new StringTokenizer(r.readLine());
            return st.nextToken();
        } catch (Exception e) {}
        return null;
    }
    public int nextInt() { return Integer.parseInt(next()); }
    public double nextDouble() { return Double.parseDouble(next()); }
    public long nextLong() { return Long.parseLong(next()); }
}
```

而下方代码简单展示了 Kattio 的使用：

```java
class Test {
    public static void main(String[] args) {
        Kattio io = new Kattio();
        // 字符串输入
        String str = io.next();
        // int 输入
        int num = io.nextInt();
        // 输出
        io.println("Result");
        // 请确保关闭 IO 流以确保输出被正确写入
        io.close();
    }
}
```

### 使用 StreamTokenizer 作为输入

在某些情况使用 `StringTokenizer` 会导致 MLE（Memory Limit Exceeded，超过内存上限），此时我们需要使用 `StreamTokenizer` 作为输入．

```java
import java.io.*;
public class Main {
    // IO 代码
    public static StreamTokenizer in = new StreamTokenizer(new BufferedReader(new InputStreamReader(System.in), 32768));
    public static PrintWriter out = new PrintWriter(new OutputStreamWriter(System.out));
    public static double nextDouble() throws IOException { in.nextToken(); return in.nval; }
    public static float nextFloat() throws IOException { in.nextToken(); return (float)in.nval; }
    public static int nextInt() throws IOException { in.nextToken(); return (int)in.nval; }
    public static String next() throws IOException { in.nextToken(); return in.sval; }
    public static long nextLong() throws Exception { in.nextToken(); return (long)in.nval;}
    
    // 使用示例
    public static void main(String[] args) throws Exception {
        int n = nextInt();
        out.println(n);
        out.close();
    }
}
```

### Kattio + StringTokenizer 的方法与 StreamTokenizer 的方法之间的分析与对比

1.  `StreamTokenizer` 相较于 `StringTokenizer` 使用的内存较少，当 Java 标程 MLE 时可以尝试使用 `StreamTokenizer`，但是 `StreamTokenizer` 会丢失精度，读入部分数据时会出现问题；
    -   `StreamTokenizer` 源码存在 `Type`，该 `Type` 根据输入内容来决定类型，如果输入类似于 `123oi` 以 **数字开头** 的字符串，他会强制认为的类型是 `double` 类型，因此在读入中以 `double` 类型去读 `String` 类型便会抛出异常；
    -   `StreamTokenizer` 在读入 `1e14` 以上大小的数字会丢失精度；
2.  在使用 `PrintWriter` 情况下，需注意在程序结束最后 `close()` 关闭输出流或在需要输出的时候使用 `flush()` 清除缓冲区，否则内容将不会被写入到控制台/文件中．
3.  `Kattio` 是继承自 `PrintWriter` 类，自身对象具有了 `PrintWriter` 的功能，因此可以直接调用 `PrintWriter` 类的函数输出，同时将 `StringTokenizer` 作为了自身的成员变量来修改．而第二种 `Main` 是同时将 `StreamTokenizer` 与 `PrintWriter` 作为了自身的成员变量，因此在使用上有些许差距．

综上所述，在大部分情况下，`StringTokenizer` 的使用处境要优越于 `StreamTokenizer`，在极端 MLE 的情况下可以尝试 `StreamTokenizer`，同时 `int` 范围以上的数据 `StreamTokenizer` 处理是无能为力的．

## BigInteger 与数论

`BigInteger` 是 Java 提供的高精度计算类，可以很方便地解决高精度问题．

### 初始化

`BigInteger` 常用创建方式有如下二种：

```java
import java.io.PrintWriter;
import java.math.BigInteger;

class Main {
    static PrintWriter out = new PrintWriter(System.out);
    public static void main(String[] args) {
        BigInteger a = new BigInteger("12345678910");  // 将字符串以十进制的形式创建 BigInteger 对象
        out.println(a);  // a 的值为 12345678910 
        BigInteger b = new BigInteger("1E", 16);  // 将字符串以指定进制的形式创建 BigInteger 对象
        out.println(b);  // b 的值为 30 
        out.close();
    }
}

```

### 基本运算

以下均用 `this` 代替当前 `BigIntger`:

|             函数名             |               功能               |
| :-------------------------: | :----------------------------: |
|           `abs()`           |         返回 `this` 的绝对值         |
|          `negate()`         |         返回 `this` 的相反数         |
|    `add(BigInteger val)`    |      返回 `this` 和 `val` 的和      |
|  `subtract(BigInteger val)` |      返回 `this` 和 `val` 的差      |
|  `multiply(BigInteger val)` |      返回 `this` 和 `val` 的积      |
|   `divide(BigInteger val)`  |      返回 `this` 和 `val` 的商      |
| `remainder(BigInteger val)` |     返回 `this` 除以 `val` 的余数     |
|    `mod(BigInteger val)`    |     返回 `this` 对 `val` 取模的值     |
|        `pow(int val)`       |      返回 `this` 的 `val` 次方      |
|    `and(BigInteger val)`    |     返回 `this` 和 `val` 的按位与     |
|     `or(BigInteger val)`    |     返回 `this` 和 `val` 的按位或     |
|           `not()`           |         返回 `this` 的按位取反        |
|    `xor(BigInteger val)`    |     返回 `this` 和 `val` 的按位异或    |
|      `shiftLeft(int n)`     |       返回 `this` 左移 `n` 位       |
|     `shiftRight(int n)`     |       返回 `this` 右移 `n` 位       |
|    `max(BigInteger val)`    |     返回 `this` 与 `val` 的较大值     |
|    `min(BigInteger val)`    |     返回 `this` 与 `val` 的较小值     |
|         `bitCount()`        | 返回 `this` 的二进制中不包括符号位的 `1` 的个数 |
|        `bitLength()`        |    返回 `this` 的二进制中不包括符号位的长度    |
|     `getLowestSetBit()`     |      返回 `this` 的二进制中最右边的位置     |
| `compareTo(BigInteger val)` |      比较 `this` 和 `val` 值大小     |
|         `toString()`        |      返回 `this` 的十进制字符串表示形式     |
|    `toString(int radix)`    |  返回 `this` 的 `raidx` 进制字符串表示形式 |

使用案例如下：

```java
import java.io.PrintWriter;
import java.math.BigInteger;

public class Main {
    static PrintWriter out = new PrintWriter(System.out);
    static BigInteger a, b;
    
    static void abs() {
        out.println("abs:");
        a = new BigInteger("-123");
        out.println(a.abs());  // 输出 123 
        a = new BigInteger("123");
        out.println(a.abs());  // 输出 123 
    }
    
    static void negate() {
        out.println("negate:");
        a = new BigInteger("-123");
        out.println(a.negate());  // 输出 123 
        a = new BigInteger("123");
        out.println(a.negate());  // 输出 -123 
    }
    
    static void add() {
        out.println("add:");
        a = new BigInteger("123");
        b = new BigInteger("123");
        out.println(a.add(b));  // 输出 246 
    }
    
    static void subtract() {
        out.println("subtract:");
        a = new BigInteger("123");
        b = new BigInteger("123");
        out.println(a.subtract(b));  // 输出 0 
    }
    
    static void multiply() {
        out.println("multiply:");
        a = new BigInteger("12");
        b = new BigInteger("12");
        out.println(a.multiply(b));  // 输出 144 
    }
    
    static void divide() {
        out.println("divide:");
        a = new BigInteger("12");
        b = new BigInteger("11");
        out.println(a.divide(b));  // 输出 1 
    }
    
    static void remainder() {
        out.println("remainder:");
        a = new BigInteger("12");
        b = new BigInteger("10");
        out.println(a.remainder(b));  // 输出 2 
        a = new BigInteger("-12");
        b = new BigInteger("10");
        out.println(a.remainder(b));  // 输出 -2 
    }
    
    static void mod() {
        out.println("mod:");
        a = new BigInteger("12");
        b = new BigInteger("10");
        out.println(a.mod(b));  // 输出 2 
        a = new BigInteger("-12");
        b = new BigInteger("10");
        out.println(a.mod(b));  // 输出 8 
    }
    
    static void pow() {
        out.println("pow:");
        a = new BigInteger("2");
        out.println(a.pow(10));  // 输出 1024 
    }
    
    static void and() {
        out.println("and:");
        a = new BigInteger("3");  // 11 
        b = new BigInteger("5");  // 101 
        out.println(a.and(b));  // 输出 1 
    }
    
    static void or() {
        out.println("or:");
        a = new BigInteger("2");  // 10 
        b = new BigInteger("5");  // 101 
        out.println(a.or(b));  // 输出 7 
    }
    
    static void not() {
        out.println("not:");
        a = new BigInteger("2147483647");  // 01111111 11111111 11111111 11111111 
        out.println(a.not());  // 输出 -2147483648 二进制为：10000000 00000000 00000000 00000000 
    }
    
    static void xor() {
        out.println("xor:");
        a = new BigInteger("6");  // 110 
        b = new BigInteger("5");  // 101 
        out.println(a.xor(b));  // 011 输出 3 
    }
    
    static void shiftLeft() {
        out.println("shiftLeft:");
        a = new BigInteger("1");
        out.println(a.shiftLeft(10));  // 输出 1024 
    }
    
    static void shiftRight() {
        out.println("shiftRight:");
        a = new BigInteger("1024");
        out.println(a.shiftRight(8));  // 输出 4 
    }
    
    static void max() {
        out.println("max:");
        a = new BigInteger("6");
        b = new BigInteger("5");
        out.println(a.max(b));  // 输出 6 
    }
    
    static void min() {
        out.println("min:");
        a = new BigInteger("6");
        b = new BigInteger("5");
        out.println(a.min(b));  // 输出 5 
    }
    
    static void bitCount() {
        out.println("bitCount:");
        a = new BigInteger("6");  // 110 
        out.println(a.bitCount());  // 输出 2 
    }
    
    static void bitLength() {
        out.println("bitLength:");
        a = new BigInteger("6");  // 110 
        out.println(a.bitLength());  // 输出 3 
    }
    
    static void getLowestSetBit() {
        out.println("getLowestSetBit:");
        a = new BigInteger("8");  // 1000 
        out.println(a.getLowestSetBit());  // 输出 3 
    }
    
    static void compareTo() {
        out.println("compareTo:");
        a = new BigInteger("8");
        b = new BigInteger("9");
        out.println(a.compareTo(b));  // 输出 -1 
        a = new BigInteger("8");
        b = new BigInteger("8");
        out.println(a.compareTo(b));  // 输出 0 
        a = new BigInteger("8");
        b = new BigInteger("7");
        out.println(a.compareTo(b));  // 输出 1 
    }
    
    static void toStringTest() {
        out.println("toString:");
        a = new BigInteger("15");
        out.println(a.toString());  // 输出 15 
        out.println(a.toString(16));  // 输出 f 
    }
    
    public static void main(String[] args) {
        abs();
        negate();
        add();
        subtract();
        multiply();
        divide();
        remainder();
        mod();
        pow();
        and();
        or();
        not();
        xor();
        shiftLeft();
        shiftRight();
        max();
        min();
        bitCount();
        bitLength();
        getLowestSetBit();
        compareTo();
        toStringTest();
        out.close();
    }
}
```

### 数学运算

以下均用 `this` 代替当前 `BigIntger`:

|                  函数名                 |                功能                |
| :----------------------------------: | :------------------------------: |
|         `gcd(BigInteger val)`        | 返回 `this` 的绝对值与 `val` 的绝对值的最大公约数 |
|      `isProbablePrime(int val)`      |      返回一个表示 `this` 是否是素数的布尔值     |
|         `nextProbablePrime()`        |        返回第一个大于 `this` 的素数        |
| `modPow(BigInteger b, BigInteger p)` |    返回 `this` 的 `b` 次方模 `p` 的值    |
|      `modInverse(BigInteger p)`      |     返回 `this` 在模 `p` 意义下的乘法逆元    |

使用案例如下：

```java
import java.io.PrintWriter;
import java.math.BigInteger;

public class Main {
    static PrintWriter out = new PrintWriter(System.out);
    static BigInteger a, b, p;
    
    static void gcd() {  // 最大公约数 
        a = new BigInteger("120032414321432144212100");
        b = new BigInteger("240231431243123412432140");
        out.println(String.format("gcd(%s,%s)=%s", a.toString(), b.toString(), a.gcd(b).toString()));  // gcd(120032414321432144212100,240231431243123412432140)=20 
    }
    
    static void isPrime() {  // 基于米勒罗宾判定该数是否是素数，参数越大准确性越高，复杂度越高．准确性为 (1-1/(val*2)) 
        a = new BigInteger("1200324143214321442127");
        out.println("a:" + a.toString());
        out.println(a.isProbablePrime(10) ? "a is prime" : "a is not prime");  // a is not prime 
    }
    
    static void nextPrime() {  // 找出该数的下一个素数 
        a = new BigInteger("1200324143214321442127");
        out.println("a:" + a.toString());
        out.println(String.format("a nextPrime is %s", a.nextProbablePrime().toString()));  // a nextPrime is 1200324143214321442199 
    }
    
    static void modPow() {  // 快速幂，比正常版本要快，内部有数学优化 
        a = new BigInteger("2");
        b = new BigInteger("10");
        p = new BigInteger("1000");
        out.println(String.format("a:%s b:%s p:%s", a, b, p));
        out.println(String.format("a^b mod p:%s", a.modPow(b, p).toString()));//  24 
    }
    
    static void modInverse() {  // 逆元 
        a = new BigInteger("10");
        b = new BigInteger("3");
        out.println(a.modInverse(b));  // a ^ (p-2) mod p = 1 
    }
    
    public static void main(String[] args) {
        gcd();
        isPrime();
        nextPrime();
        modPow();
        modInverse();
        out.close();
    }
}
```

关于米勒罗宾相关知识可以查阅 [Miller–Rabin 素性测试](../math/number-theory/prime.md#millerrabin-素性测试)．

## 基本数据类型与包装数据类型

### 简介

由于基本类型没有面向对象的特征，为了他们参加到面向对象的开发中，Java 为八个基本类型提供了对应的包装类，分别是 `Byte`、`Double`、`Float`、`Integer`、`Long`、`Short`、`Character` 和 `Boolean`．两者之间的对应关系如下：

|   基本数据类型  |    包装数据类型   |
| :-------: | :---------: |
|   `byte`  |    `Byte`   |
|  `short`  |   `Short`   |
| `boolean` |  `Boolean`  |
|   `char`  | `Character` |
|   `int`   |  `Integer`  |
|   `long`  |    `Long`   |
|  `float`  |   `Float`   |
|  `double` |   `Double`  |

### 区别

此处以 `int` 与 `Integer` 举例：

1.  `Integer` 是 `int` 的包装类，`int` 则是 Java 的一种基本类型数据．
2.  `Integer` 类型实例后才能使用，而 `int` 类型不需要．
3.  `Integer` 实际对应的引用，当 `new` 一个 `Integer` 时，实际上生成了一个对象，而 `int` 则是直接存储数据．
4.  `Integer` 的默认值是 `null`，可接受 `null` 和 `int` 类型的数据，`int` 默认值是 0，不能接受 `null` 类型的数据．
5.  `Integer` 判定二个变量是否相同使用 `==` 可能会导致不正确的结果，只能使用 `equals()`，而 `int` 可以直接使用 `==`．

### 装箱与拆箱

此处以 `int` 与 `Integer` 举例：

`Integer` 的本质是对象，`int` 是基本类型，两个类型之间是不能直接赋值的．需要转换时，应将基础类型转换为包装类型，这种做法称为装箱，反过来则称为拆箱．

```java
// 基本类型
int value1 = 1;
// 装箱转换为包装类型
Integer integer = Integer.valueOf(value1);
// 拆箱转换为基本类型
int value2 = integer.intValue();
```

Java 5 引入了自动装箱拆箱机制：

```java
Integer integer = 1;
int value = integer;
```

???+ warning "注意"
    虽然 JDK 增加了自动装箱拆箱的机制，但在声明变量时请选择合适的类型，因为包装类型 `Integer` 可以接受 `null`，而基本类型 `int` 不能接受 `null`．因此，对使用 `null` 值的包装类型进行拆箱操作时，会抛出异常．如下代码展示了这一行为．
    
    ```java
    Integer integer = Integer.valueOf(null);
    integer.intValue();  // 抛出 java.lang.NumberFormatException 异常
    
    Integer integer = null;
    integer.intValue();  // 抛出 java.lang.NullPointerException 异常
    ```

## 继承

基于已有的设计创造新的设计，就是面向对象程序设计中的继承．在继承中，新的类不是凭空产生的，而是基于一个已经存在的类而定义出来的．通过继承，新的类自动获得了基础类中所有的成员，包括成员变量和方法，包括各种访问属性的成员，无论是 `public` 还是 `private`．显然，通过继承来定义新的类，远比从头开始写一个新的类要简单快捷和方便．继承是支持代码重用的重要手段之一．

在 Java 中，继承的关键字为 `extends`，且 Java 只支持单继承，但可以实现多接口．

在 Java 中，所有类都是 `Object` 类的子类．

子类继承父类，所有的父类的成员，包括变量和方法，都成为了子类的成员，除了构造方法．构造方法是父类所独有的，因为它们的名字就是类的名字，所以父类的构造方法在子类中不存在．除此之外，子类继承得到了父类所有的成员．

每个成员有不同的访问属性，子类继承得到了父类所有的成员，但是不同的访问属性使得子类在使用这些成员时有所不同：有些父类的成员直接成为子类的对外的界面，有些则被深深地隐藏起来，即使子类自己也不能直接访问．

下表列出了不同访问属性的父类成员在子类中的访问属性：

|    父类成员访问属性   |      在父类中的含义      |                     在子类中的含义                    |
| :-----------: | :---------------: | :--------------------------------------------: |
|    `public`   |       对所有类开放      |                     对所有类开放                     |
|  `protected`  | 只有包内其它类、自己和子类可以访问 |                只有包内其它类、自己和子类可以访问               |
| 缺省（`default`） |    只有包内其它类可以访问    | 如果子类与父类在同一个包内，只有包内其它类可以访问；否则相当于 `private`，不能访问 |
|   `private`   |      只有自己可以访问     |                      不能访问                      |

## 多态

在 Java 中当把一个对象赋值给一个变量时，对象的类型必须与变量的类型相匹配．但由于 Java 有继承的概念，便可重新定义为 **一个变量可以保存其所声明的类型或该类型的任何子类型**．

如果一个类型实现了接口，也可以称之为该接口的子类型．

Java 中保存对象类型的变量是多态变量．「多态」这个术语（字面意思是许多形态）是指一个变量可以保存不同类型（即其声明的类型或任何子类型）的对象．

多态变量：

1.  Java 的对象变量是多态的，它们能保存不止一种类型的对象．
2.  它们可以保存的是声明类型的对象，或声明类型子类的对象．
3.  当把子类的对象赋给父类的变量的时候，就发生了向上转型．

## 泛型

泛型指在类定义时不设置类中的属性或方法参数的具体类型，而是在使用（或创建对象）时再进行类型的定义．泛型本质是参数化类型，即所操作的数据类型被指定为一个参数．

泛型提供了编译时类型安全检测的机制，该机制允许编译时检测非法类型．

## 接口

### 简介

接口（Interface）在 Java 中是一个抽象类型，是抽象方法的集合，通常以 `interface` 来声明．一个类通过实现接口的方式，从而来继承接口的抽象方法．

接口并不是类，编写接口的方式和类很相似，但是它们属于不同的概念．类描述对象的属性和方法．接口则包含类要实现的方法．

除非实现接口的类是抽象类，否则该类要定义接口中的所有方法．

接口无法被实例化，但是可以被实现．一个实现接口的类，必须实现接口内所描述的所有方法，否则就必须声明为抽象类．另外，在 Java 中，接口类型可用来声明一个变量，他们可以成为一个空指针，或是被绑定在一个以此接口实现的对象．

### 与类的区别

1.  接口不能用于实例化对象．
2.  接口没有构造方法．
3.  接口中所有的方法必须是抽象方法，Java 8 之后接口中可以使用 `default` 关键字修饰的非抽象方法．
4.  接口不能包含成员变量，除了 static 和 final 变量．
5.  接口不是被类继承了，而是要被类实现．
6.  接口支持多继承，类不支持多继承．

### 声明

```java
[可见度] interface 接口名称 [extends 其他的接口名] {
        // 声明变量
        // 抽象方法
}
```

### 实现

```java
...implements 接口名称[, 其他接口名称, 其他接口名称..., ...] ...
```

## Lambda 表达式

### 简介

lambda 表达式也可称为闭包，是 Java 8 的最重要的新特性．

lambda 表达式允许把函数作为一个方法的参数（函数作为参数传递进方法中）．

使用 lambda 表达式可以使代码变的更加简洁紧凑．

### 语法

-   可选类型声明：不需要声明参数类型，编译器可以统一识别参数值．
-   可选的参数圆括号：一个参数无需定义圆括号，但多个参数需要定义圆括号．
-   可选的大括号：如果主体包含了一个语句，就不需要使用大括号．
-   可选的返回关键字：如果主体只有一个表达式返回值则编译器会自动返回值，大括号需要指定表达式返回了一个数值．

lambda 表达式声明方式如下：

```java
// 1. 不需要参数，返回值为 5
() -> 5

// 2. 接收一个参数（数字类型），返回其 2 倍的值
x -> 2 * x

// 3. 接受 2 个参数（数字）并返回他们的差值
(x, y) -> x – y

// 4. 接收 2 个 int 类型整数并返回他们的和
(int x, int y) -> x + y

// 5. 接受一个 String 对象并在控制台打印，不返回任何值（看起来像是返回 void）
(String s) -> System.out.print(s)
```

以字符串数组按长度排序的自定义比较器为例，lambda 表达式可以按如下形式应用．

```java
import java.util.Arrays;

public class Main {
    static PrintWriter out = new PrintWriter(System.out);
    
    public static void main(String[] args) {
        String[] plants = {"Mercury", "venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"};
        Arrays.sort(plants, (String first, String second) -> (first.length() - second.length()));
        for (String word : plants) {
            out.print(word + " ");
        }
        out.close();
    }
}
```

也可以类似下面的例子在 lambda 表达式中使用多条语句．

```java
import java.io.PrintWriter;
import java.util.Arrays;

public class Main {
    static PrintWriter out = new PrintWriter(System.out);
    
    public static void main(String[] args) {
        String[] plants = {"Mercury", "venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"};
        Arrays.sort(plants, (first, second) ->
        {
            // 形参不写类型，可以从上下文判断出
            int result = first.length() - second.length();
            return result;
        });
        for (String word : plants) {
            out.print(word + " ");
        }
        out.close();
    }
}
```

其中，`->` 是一个推导符号，表示前面的括号接收到参数，推导后面的返回值（其实就是传递了方法）．

### 函数式接口

1.  是一个接口，符合 Java 接口定义．
2.  只包含一个抽象方法的接口．
3.  因为只有一个未实现的方法，所以 lambda 表达式可以自动填上去．

函数式接口使用方式如下：

???+ example "输出长度为 2 的倍数的字符串"
    ```java
    import java.io.PrintWriter;
    
    public class Main {
        static PrintWriter out = new PrintWriter(System.out);
        
        public static void main(String[] args) {
            String[] plants = {"Mercury", "venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"};
            Test test = s -> {  // lambda 表达式作为函数式接口的实例
                if (s.length() % 2 == 0) {
                    return true;
                }
                return false;
            };
            for (String word : plants) {
                if (test.check(word)) {
                    out.print(word + " ");
                }
            }
            out.close();
        }
    }
    
    interface Test {
        public boolean check(String s);
    }
    ```

???+ example "实现加减乘除四则运算"
    ```java
    import java.io.PrintWriter;
    
    public class Main {
        static PrintWriter out = new PrintWriter(System.out);
        
        public static double calc(double a, double b, Calculator util) {
            return util.operation(a, b);
        }
        
        public static void main(String[] args) {
            Calculator util[] = new Calculator[4];  // 定义函数式接口数组
            util[0] = (a, b) -> a + b;
            util[1] = (a, b) -> a - b;
            util[2] = (a, b) -> a * b;
            util[3] = (a, b) -> a / b;
            double a = 20, b = 15;
            for (Calculator c : util) {
                System.out.println(calc(a, b, c));
            }
            out.close();
        }
    }
    
    interface Calculator {
        public double operation(double a, double b);
    }
    ```

## Collection

`Collection` 是 Java 中的接口，被多个泛型容器接口所实现．在这里，`Collection` 是指代存放对象类型的数据结构．

Java 中的 `Collection` 元素类型定义时必须为对象，不能为基本数据类型．

以下内容用法均基于 Java 里多态的性质，均是以实现接口的形式出现．

常用的接口包括 `List`、`Queue`、`Set` 和 `Map`．

### 容器定义

当定义泛型容器类时，需要在定义时指定数据类型．如果不指定数据类型，而当成 `Object` 类型随意添加数据，在 Java 8 中虽能编译通过，但会有很多警告风险．

例如，如下定义方式是安全的，容器中只接受 `Integer` 类型．

```java
List<Integer> list1 = new LinkedList<>();
```

而如下定义方式会出现警告．

```java
List list = new ArrayList<>();
list.add(1);
list.add(true);
list.add(1.01);
list.add(1L);
list.add("I am String");
```

因此，如果没有特殊需求的话不推荐第 2 种行为，编译器无法帮忙检查存入的数据是否安全．`list.get(index)` 取值时无法明确数据的类型（取到的数据类型都为 `Object`），需要手动转回原来的类型，稍有不慎可能出现误转型异常．

如果是明确了类型如 `List<Integer>`，此时编译器会检查放入的数据类型，只能放入整数的数据．声明集合变量时只能使用包装类型 `List<Integer>` 或者自定义的 `Class`，而不能是基本类型如 `List<int>`．

### List

#### ArrayList

`ArrayList` 是支持可以根据需求动态生长的数组，初始长度默认为 10．如果超出当前长度便扩容 $\dfrac{3}{2}$．

##### 初始化

```java
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.List;

public class Main {
    static PrintWriter out = new PrintWriter(System.out);
    
    public static void main(String[] args) {
        List<Integer> list1 = new ArrayList<>();  // 创建一个名字为 list1 的可自增数组，初始长度为默认值（10）
        List<Integer> list2 = new ArrayList<>(30);  // 创建一个名字为list2的可自增数组，初始长度为 30
        List<Integer> list3 = new ArrayList<>(list2);  // 创建一个名字为 list3 的可自增数组，使用 list2 里的元素和 size 作为自己的初始值
    }
}
```

#### LinkedList

`LinkedList` 是双链表．

##### 初始化

```java
import java.io.PrintWriter;
import java.util.LinkedList;
import java.util.List;

public class Main {
    static PrintWriter out = new PrintWriter(System.out);
    
    public static void main(String[] args) {
        List<Integer> list1 = new LinkedList<>();  // 创建一个名字为 list1 的双链表 
        List<Integer> list2 = new LinkedList<>(list1);  // 创建一个名字为 list2 的双链表，将 list1 内所有元素加入进来 
    }
}
```

#### 常用方法

以下均用 `this` 代替当前 `List<Integer>`：

|            函数名            |                功能                |
| :-----------------------: | :------------------------------: |
|          `size()`         |           返回 `this` 的长度          |
|     `add(Integer val)`    |      在 `this` 尾部插入 `val` 元素      |
| `add(int idx, Integer e)` |   在 `this` 的 `idx` 位置插入 `e` 元素   |
|       `get(int idx)`      | 返回 `this` 中第 `idx` 位置的值，若越界则抛出异常 |
| `set(int idx, Integer e)` |   修改 `this` 中第 `idx` 位置的值为 `e`   |

使用案例及区别对比：

```java
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;

public class Main {
    static PrintWriter out = new PrintWriter(System.out);
    static List<Integer> array = new ArrayList<>();
    static List<Integer> linked = new LinkedList<>();
    
    static void add() {
        array.add(1);  // 时间复杂度为 O(1) 
        linked.add(1);  // 时间复杂度为 O(1) 
    }
    
    static void get() {
        array.get(10);  // 时间复杂度为 O(1) 
        linked.get(10);  // 时间复杂度为 O(11) 
    }
    
    static void addIdx() {
        array.add(0, 2);  // 最坏情况下时间复杂度为 O(n)
        linked.add(0, 2);  // 最坏情况下时间复杂度为 O(n)
    }
    
    static void size() {
        array.size();  // 时间复杂度为 O(1)
        linked.size();  // 时间复杂度为 O(1)
    }
    
    static void set() {  // 该方法返回值为原本该位置元素的值
        array.set(0, 1);  // 时间复杂度为 O(1)
        linked.set(0, 1);  // 最坏时间复杂度为 O(n)
    }

}
```

#### 遍历

```java
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.List;

public class Main {
    static PrintWriter out = new PrintWriter(System.out);
    static List<Integer> array = new ArrayList<>();
    static List<Integer> linked = new LinkedList<>();
    
    static void function1() {  // 朴素遍历
        for (int i = 0; i < array.size(); i++) {
            out.println(array.get(i));  // 遍历自增数组，复杂度为 O(n)
        }
        for (int i = 0; i < linked.size(); i++) {
            out.println(linked.get(i));  // 遍历双链表，复杂度为 O(n^2)，因为 LinkedList 的 get(i) 复杂度是 O(i)
        }
    }
    
    static void function2() {  // 增强 for 循环遍历 
        for (int e : array) {
            out.println(e);
        }
        for (int e : linked) {
            out.println(e);  // 复杂度均为 O(n) 
        }
    }
    
    static void function3() {  // 迭代器遍历 
        Iterator<Integer> iterator1 = array.iterator();
        Iterator<Integer> iterator2 = linked.iterator();
        while (iterator1.hasNext()) {
            out.println(iterator1.next());
        }
        while (iterator2.hasNext()) {
            out.println(iterator2.next());
        }  // 复杂度均为 O(n) 
    }

}
```

???+ warning "注意"
    不要在 `for` 或 `foreach` 遍历 `List` 的过程中删除其中的元素，否则会抛出异常．
    
    原因也很简单，`list.size()` 改变了，但在循环中已循环的次数却是没有随之变化．原来预计在下一个 `index` 的数据因为删除的操作变成了当前 `index` 的数据，运行下一个循环时操作的会变为原来预计在下下个 `index` 的数据，最终会导致操作的数据不符合预期．

### Queue

#### LinkedList

可以使用 `LinkedList` 实现普通队列，底层是链表模拟队列．

##### 初始化

```java
Queue<Integer> q = new LinkedList<>();
```

`LinkedList` 底层实现了 `List` 接口与 `Deque` 接口，而 `Deque` 接口继承自 `Queue` 接口，所以 `LinkedList` 可以同时实现 `List` 与 `Queue`．

#### ArrayDeque

可以使用 `ArrayDeque` 实现普通队列，底层是数组模拟队列．

##### 初始化

```java
Queue<Integer> q = new ArrayDeque<>();
```

`ArrayDeque` 底层实现了 `Deque` 接口，而 `Deque` 接口继承自 `Queue` 接口，所以 `ArrayDeque` 可以实现 `Queue`．

#### LinkedList 与 ArrayDeque 在实现 Queue 接口上的区别

1.  数据结构：在数据结构上，`ArrayDeque` 和 `LinkedList` 都实现了 Java Deque 双端队列接口．但 `ArrayDeque` 没有实现了 Java List 列表接口，所以不具备根据索引位置操作的行为．
2.  线程安全：`ArrayDeque` 和 `LinkedList` 都不考虑线程同步，不保证线程安全．
3.  底层实现：在底层实现上，`ArrayDeque` 是基于动态数组的，而 `LinkedList` 是基于双向链表的．
4.  在遍历速度上：`ArrayDeque` 是一块连续内存空间，基于局部性原理能够更好地命中 CPU 缓存行，而 `LinkedList` 是离散的内存空间对缓存行不友好．
5.  在操作速度上：`ArrayDeque` 和 `LinkedList` 的栈和队列行为都是 $O(1)$ 时间复杂度，`ArrayDeque` 的入栈和入队有可能会触发扩容，但从均摊分析上看依然是 $O(1)$ 时间复杂度．
6.  额外内存消耗上：`ArrayDeque` 在数组的头指针和尾指针外部有闲置空间，而 `LinkedList` 在节点上增加了前驱和后继指针．

#### PriorityQueue

`PriorityQueue` 是优先队列，默认是小根堆．

##### 初始化

```java
Queue<Integer> q1 = new PriorityQueue<>();  // 小根堆
Queue<Integer> q2 = new PriorityQueue<>((x, y) -> {return y - x;});  // 大根堆
```

#### 常用方法

下表中队列定义为 `Queue<Integer>`．

|          函数名         |                     功能                     |
| :------------------: | :----------------------------------------: |
|       `size()`       |                  返回当前队列长度                  |
|  `add(Integer val)`  |     将 `val` 插入队列，如果插入时违反了队列的容量限制，将抛出异常     |
| `offer(Integer val)` | 将 `val` 插入队列，如果插入时违反了队列的容量限制，则插入失败，但不会抛出异常 |
|      `isEmpty()`     |            判断队列是否为空，为空则返回 `true`           |
|       `peek()`       |            返回队头元素，若队列为空返回 `null`           |
|       `poll()`       |          返回并删除队头元素，若队列为空返回 `null`          |

使用案例及区别对比：

```java
import java.io.PrintWriter;
import java.util.LinkedList;
import java.util.PriorityQueue;
import java.util.Queue;

public class Main {
    static PrintWriter out = new PrintWriter(System.out);
    static Queue<Integer> q1 = new LinkedList<>();
    static Queue<Integer> q2 = new PriorityQueue<>();
    
    static void add() {  // add 和 offer 功能上没有差距，区别是是否会抛出异常 
        q1.add(1);  // 时间复杂度为 O(1) 
        q2.add(1);  // 时间复杂度为 O(logn) 
    }
    
    static void isEmpty() {
        q1.isEmpty();  // 时间复杂度为 O(1) 
        q2.isEmpty();  // 空间复杂度为 O(1) 
    }
    
    static void size() {
        q1.size();  // 时间复杂度为 O(1) 
        q2.size();  // 返回 q2 的长度 
    }
    
    static void peek() {
        q1.peek();  // 时间复杂度为 O(1) 
        q2.peek();  // 时间复杂度为 O(logn) 
    }
    
    static void poll() {
        q1.poll();  // 时间复杂度为 O(1) 
        q2.poll();  // 时间复杂度为 O(logn) 
    }
}
```

#### 遍历

```java
import java.io.PrintWriter;
import java.util.LinkedList;
import java.util.PriorityQueue;
import java.util.Queue;

public class Main {
    static PrintWriter out = new PrintWriter(System.out);
    static Queue<Integer> q1 = new LinkedList<>();
    static Queue<Integer> q2 = new PriorityQueue<>();
    
    static void test() {
        while (!q1.isEmpty()) {  // 复杂度为 O(n) 
            out.println(q1.poll());
        }
        while (!q2.isEmpty()) {  // 复杂度为 O(nlogn) 
            out.println(q2.poll());
        }
    }

}
```

### Deque

`Deque` 是 `Java` 中的双端队列，我们通常用其进行队列的操作以及栈的操作．

#### 主要函数

下表中队列定义为 `Deque<Integer>`．

|            函数名            |                     功能                     |
| :-----------------------: | :----------------------------------------: |
|  `addFirst(Integer val)`  |     将 `val` 插入队头，如果插入时违反了队列的容量限制，将抛出异常     |
| `offerFirst(Integer val)` | 将 `val` 插入队头，如果插入时违反了队列的容量限制，则插入失败，但不会抛出异常 |
|      `removeFirst()`      |           返回并删除队头元素，如果队列为空，将抛出异常           |
|       `pollFirst()`       |         返回并删除队头元素，如果队列为空，则返回 `null`        |
|       `peekFirst()`       |          返回队头元素，如果队列为空，则返回 `null`          |
|    `push(Integer val)`    |         将 `val` 插入队头，等效于 `addFirst`        |
|          `pop()`          |         返回并删除队头元素，等效于 `removeFirst`        |
|         `remove()`        |          删除队头元素，等效于 `removeFirst`          |
|          `poll()`         |           删除队头元素，等效于 `pollFirst`           |
|   `addLast(Integer val)`  |     将 `val` 插入队尾，如果插入时违反了队列的容量限制，将抛出异常     |
|  `offerLast(Integer val)` | 将 `val` 插入队尾，如果插入时违反了队列的容量限制，则插入失败，但不会抛出异常 |
|       `removeLast()`      |           返回并删除队尾元素，如果队列为空，将抛出异常           |
|        `pollLast()`       |         返回并删除队尾元素，如果队列为空，则返回 `null`        |
|        `peekLast()`       |          返回队尾元素，如果队列为空，则返回 `null`          |
|     `add(Integer val)`    |         将 `val` 插入队尾，等效于 `addLast`         |
|    `offer(Integer val)`   |        将 `val` 插入队尾，等效于 `offerLast`        |

#### 栈的操作

```java
import java.util.ArrayDeque;
import java.util.Deque;

public class Main {
    static Deque<Integer> stack = new ArrayDeque<>();
    static int[] a = {1, 2, 3, 4, 5};
    
    public static void main(String[] args) {
        for (int v : a) {
            stack.push(v);
        }
        while (!stack.isEmpty()) { //输出 5 4 3 2 1
            System.out.println(stack.pop()); 
        }
    }
}

```

#### 双端队列的操作

```java
import java.util.ArrayDeque;
import java.util.Deque;

public class Main {
    static Deque<Integer> deque = new ArrayDeque<>();
    
    static void insert() {
        deque.addFirst(1);
        deque.addFirst(2);
        deque.addLast(3);
        deque.addLast(4);
    }
    
    public static void main(String[] args) {
        insert();
        while (!deque.isEmpty()) { //输出 2 1 3 4
            System.out.println(deque.poll());
        }
        insert();
        while (!deque.isEmpty()) { //输出 4 3 1 2
            System.out.println(deque.pollLast());
        }
    }
}
```

### Set

`Set` 是保持容器中的元素不重复的一种数据结构．

#### HashSet

随机位置插入的 `Set`．

##### 初始化

```java
Set<Integer> s1 = new HashSet<>();
```

#### LinkedHashSet

保持插入顺序的 `Set`．

##### 初始化

```java
Set<Integer> s2 = new LinkedHashSet<>();
```

#### TreeSet

保持容器中元素有序的 `Set`，默认为升序．

##### 初始化

```java
Set<Integer> s3 = new TreeSet<>();
Set<Integer> s4 = new TreeSet<>((x, y) -> {return y - x;});  // 降序 
```

##### TreeSet 的更多使用

这些方法是 `TreeSet` 新创建并实现的，我们无法使用 `Set` 接口调用以下方法，因此我们创建方式如下：

```java
TreeSet<Integer> s3 = new TreeSet<>();
TreeSet<Integer> s4 = new TreeSet<>((x, y) -> {return y - x;});  // 降序 
```

下表中均用 `this` 代替当前 `TreeSet<Integer>`．

|           函数名          |                    功能                    |
| :--------------------: | :--------------------------------------: |
|        `first()`       |       返回 `this` 中第一个元素，无则返回 `null`       |
|        `last()`        |       返回 `this` 中最后一个元素，无则返回 `null`      |
|  `floor(Integer val)`  | 返回 `this` 中小于等于 `val` 的第一个元素，无则返回 `null` |
| `ceiling(Integer val)` | 返回 `this` 中大于等于 `val` 的第一个元素，无则返回 `null` |
|  `higher(Integer val)` |  返回 `this` 中大于 `val` 的第一个元素，无则返回 `null`  |
|  `lower(Integer val)`  |  返回 `this` 中小于 `val` 的第一个元素，无则返回 `null`  |
|      `pollFirst()`     |      返回并删除 `this` 中第一个元素，无则返回 `null`     |
|      `pollLast()`      |     返回并删除 `this` 中最后一个元素，无则返回 `null`     |

代码示例：

```java
import java.util.TreeSet;

public class Main {
    static int[] a = {4,7,1,2,3,6};
    
    public static void main(String[] args) {
        TreeSet<Integer> set = new TreeSet<>();
        for(int v:a) {
            set.add(v);
        }
        Integer a2 = set.first();
        System.out.println(a2); //返回 1
        Integer a3 = set.last();
        System.out.println(a3); //返回 7
        Integer a4 = set.floor(5);
        System.out.println(a4); //返回 4
        Integer a5 = set.ceiling(6);
        System.out.println(a5); //返回 6
        Integer a6 = set.higher(7);
        System.out.println(a6); //返回 null
        Integer a7 = set.lower(2);
        System.out.println(a7); //返回 1
        Integer a8 = set.pollFirst();
        System.out.println(a8); //返回 1
        Integer a9 = set.pollLast();
        System.out.println(a9); //返回 7
    }
}
```

#### Set 常用方法

|            函数名            |                   功能                   |
| :-----------------------: | :------------------------------------: |
|          `size()`         |                返回当前集合的大小               |
|     `add(Integer val)`    |              将 `val` 插入集合              |
|  `contains(Integer val)`  |            判断集合中是否有元素 `val`            |
|   `addAll(Collection e)`  |          将容器 `e` 里的所有元素添加进当前集合         |
| `retainAll(Collection e)` | 删除当前集合中未出现在容器 `e` 中的元素，即求当前集合与 `e` 的交集 |
| `removeAll(Collection e)` |  删除当前集合中出现在容器 `e` 中的元素，即求当前集合与 `e` 的差集 |

```java
import java.io.PrintWriter;
import java.util.HashSet;
import java.util.LinkedHashSet;
import java.util.Set;

public class Main {
    static PrintWriter out = new PrintWriter(System.out);
    static Set<Integer> s1 = new HashSet<>();
    static Set<Integer> s2 = new LinkedHashSet<>();
    
    static void add() {
        s1.add(1);
    }
    
    static void contains() {  // 判断 set 中是否有元素值为 2，有则返回 true，否则返回 false 
        s1.contains(2);
    }
    
    static void test1() {  // s1 与 s2 的并集 
        Set<Integer> res = new HashSet<>();
        res.addAll(s1);
        res.addAll(s2);
    }
    
    static void test2() {  // s1 与 s2 的交集 
        Set<Integer> res = new HashSet<>();
        res.addAll(s1);
        res.retainAll(s2);
    }
    
    static void test3() {  // 差集：s1 - s2 
        Set<Integer> res = new HashSet<>();
        res.addAll(s1);
        res.removeAll(s2);
    }
}
```

#### 遍历

```java
import java.io.PrintWriter;
import java.util.HashSet;
import java.util.LinkedHashSet;
import java.util.Set;

public class Main {
    static PrintWriter out = new PrintWriter(System.out);
    static Set<Integer> s1 = new HashSet<>();
    static Set<Integer> s2 = new LinkedHashSet<>();
    
    static void test() {
        for (int key : s1) {
            out.println(key);
        }
        out.close();
    }
}
```

### Map

`Map` 是维护键值对 `<Key, Value>` 的一种数据结构，其中 `Key` 唯一．

#### HashMap

随机位置插入的 `Map`．

##### 初始化

```java
Map<Integer, Integer> map1 = new HashMap<>();
```

#### LinkedHashMap

保持插入顺序的 `Map`．

##### 初始化

```java
Map<Integer, Integer> map2 = new LinkedHashMap<>();
```

#### TreeMap

保持 `key` 有序的 `Map`，默认升序．

##### 初始化

```java
Map<Integer, Integer> map3 = new TreeMap<>();
Map<Integer, Integer> map4 = new TreeMap<>((x, y) -> {return y - x;});  // 降序
```

#### 常用方法

以下均用 `this` 代替当前 `Map<Integer, Integer>`：

|                函数名                |               功能              |
| :-------------------------------: | :---------------------------: |
| `put(Integer key, Integer value)` |   将 `<key, value>` 插入 `this`  |
|              `size()`             |         返回 `this` 的大小         |
|     `containsKey(Integer key)`    | 判断 `this` 中是否有存在某个元素的键为 `key` |
|         `get(Integer key)`        |  返回 `this` 中键为 `key` 的元素对应的值  |
|             `keySet()`            |     将 `this` 中所有元素的键作为集合返回    |

使用案例：

```java
import java.io.PrintWriter;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.TreeMap;

public class Main {
    static PrintWriter out = new PrintWriter(System.out);
    
    static Map<Integer, Integer> map1 = new HashMap<>();
    static Map<Integer, Integer> map2 = new LinkedHashMap<>();
    static Map<Integer, Integer> map3 = new TreeMap<>();
    static Map<Integer, Integer> map4 = new TreeMap<>((x,y)->{return y-x;});
    
    static void put(){  // 将 key 为 1、value 为 1 的元素返回
        map1.put(1, 1);
    }
    static void get(){  // 将 key 为 1 的 value 返回
        map1.get(1);
    }
    static void containsKey(){  // 判断是否有 key 为 1 的键值对
        map1.containsKey(1);
    }
    static void KeySet(){
        map1.keySet();
    }
}
```

#### 遍历

```java
import java.io.PrintWriter;
import java.util.HashMap;
import java.util.Map;

public class Main {
    static PrintWriter out = new PrintWriter(System.out);
    
    static Map<Integer, Integer> map1 = new HashMap<>();
    
    static void print() {
        for (int key : map1.keySet()) {
            out.println(key + " " + map1.get(key));
        }
    }
}
```

当然，键值的类型也可以更改．例如 `Map` 也可以定义为：

```java
Map<String, Set<Integer>> map = new HashMap<>();
```

## Arrays

`Arrays` 是 `java.util` 中对数组操作的一个工具类．方法均为静态方法，可使用类名直接调用．

### Arrays.sort()

`Arrays.sort()` 是对数组进行的排序的方法，主要重载方法如下：

```java
import java.util.Arrays;
import java.util.Comparator;

public class Main {
    static int[] a = new int[10];
    static Integer[] b = new Integer[10];
    static int firstIdx, lastIdx;
    
    public static void main(String[] args) {
        Arrays.sort(a);  // 1 
        Arrays.sort(a, firstIdx, lastIdx);  // 2 
        Arrays.sort(b, new Comparator<Integer>() {  // 3 
            @Override
            public int compare(Integer o1, Integer o2) {
                return o2 - o1;
            }
        });
        Arrays.sort(b, firstIdx, lastIdx, new Comparator<Integer>() {  // 4 
            @Override
            public int compare(Integer o1, Integer o2) {
                return o2 - o1;
            }
        });
        // 由于 Java 8 后有 Lambda 表达式，第三个重载及第四个重载亦可写为 
        Arrays.sort(b, (x, y) -> {  // 5 
            return y - x;
        });
        Arrays.sort(b, (x, y) -> {  // 6 
            return y - x;
        });
    }
}
```

序号所对应的重载方法含义：

1.  对数组 `a` 进行排序，默认升序．
2.  对数组 `a` 的指定位置进行排序，默认升序，排序区间为左闭右开 `[firstIdx, lastIdx)`．
3.  对数组 `a` 以自定义的形式排序，第二个参数 `-` 第一个参数为降序，第一个参数 `-` 第二个参数为升序，当自定义排序比较器时，数组元素类型必须为对象类型．
4.  对数组 `a` 的指定位置进行自定义排序，排序区间为左闭右开 `[firstIdx, lastIdx)`，当自定义排序比较器时，数组元素类型必须为对象类型．
5.  和 3 同理，用 Lambda 表达式优化了代码长度．
6.  和 4 同理，用 Lambda 表达式优化了代码长度．

???+ note "`Arrays.sort()` 底层函数"
    1.  当 `Arrays.sort` 的参数数组元素类型为基本数据类型（`byte`、`short`、`char`、`int`、`long`、`double`、`float`）时，默认为 `DualPivotQuicksort`（双轴快排），复杂度最坏可以达到 $O(n^2)$．
    2.  当 `Arrays.sort` 的参数数组元素类型为非基本数据类型时，则默认为 `legacyMergeSort` 和 `TimSort`（归并排序），复杂度为 $O(n\log n)$．

可以通过如下代码验证：

???+ example "[Codeforces 1646B - Quality vs Quantity](https://codeforces.com/problemset/problem/1646/B)"
    有 $n$ 个整数，你需要将其分为两组，是否能存在某一组的长度小于另一组，同时和大于它．

??? note "例题代码"
    ```java
    import java.io.BufferedReader;
    import java.io.IOException;
    import java.io.InputStreamReader;
    import java.io.PrintWriter;
    import java.util.Arrays;
    import java.util.StringTokenizer;
    
    public class Main {
        static class FastReader {
            StringTokenizer st;
            BufferedReader br;
            
            public FastReader() {
                br = new BufferedReader(new InputStreamReader(System.in));
            }
            
            String next() {
                while (st == null || !st.hasMoreElements()) {
                    try {
                        st = new StringTokenizer(br.readLine());
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                }
                return st.nextToken();
            }
            
            int nextInt() {
                return Integer.parseInt(next());
            }
            
            long nextLong() {
                return Long.parseLong(next());
            }
            
            double nextDouble() {
                return Double.parseDouble(next());
            }
            
            String nextLine() {
                String str = "";
                try {
                    str = br.readLine();
                } catch (IOException e) {
                    e.printStackTrace();
                }
                return str;
            }
        }
        
        static PrintWriter out = new PrintWriter(System.out);
        static FastReader in = new FastReader();
        
        static void solve() {
            int n = in.nextInt();
            // 此处数组类型由 Integer 修改为 int 会导致 TLE
            Integer[] a = new Integer[n + 10];
            for (int i = 1; i <= n; i++) {
                a[i] = in.nextInt();
            }
            Arrays.sort(a, 1, n + 1);
            long left = a[1];
            long right = 0;
            int x = n;
            for (int i = 2; i < x; i++, x--) {
                left = left + a[i];
                right = right + a[x];
                if (right > left) {
                    out.println("YES");
                    return;
                }
            }
            out.println("NO");
        }
        
        public static void main(String[] args) {
            int t = in.nextInt();
            while (t-- > 0) {
                solve();
            }
            out.close();
        }
    }
    ```

### Arrays.binarySearch()

`Arrays.binarySearch()` 是对数组连续区间进行二分搜索的方法，前提是数组必须有序，时间复杂度为 $O(\log_n)$，主要重载方法如下：

```java
import java.util.Arrays;

public class Main {
    static int[] a = new int[10];
    static Integer[] b = new Integer[10];
    static int firstIdx, lastIdx;
    static int key;
    
    public static void main(String[] args) {
        Arrays.binarySearch(a, key);  // 1 
        Arrays.binarySearch(a, firstIdx, lastIdx, key);  // 2 
    }
}
```

源码如下：

```java
private static int binarySearch0(int[] a, int fromIndex, int toIndex, int key) {
    int low = fromIndex;
    int high = toIndex - 1;
    
    while (low <= high) {
        int mid = (low + high) >>> 1;
        int midVal = a[mid];
        
        if (midVal < key)
            low = mid + 1;
        else if (midVal > key)
            high = mid - 1;
        else
            return mid; // key found
    }
    return -(low + 1);  // key not found.
}
```

序号所对应的重载方法含义：

1.  从数组 a 中二分查找是否存在 `key`，如果存在，便返回其下标．若不存在，则返回一个负数．
2.  从数组 a 中二分查找是否存在 `key`，如果存在，便返回其下标，搜索区间为左闭右开 `[firstIdx,lastIdx)`．若不存在，则返回一个负数．

### Arrays.fill()

`Arrays.fill()` 方法将数组中连续位置的元素赋值为统一元素．其接受的参数为数组、`fromIndex`、`toIndex` 和需要填充的数．方法执行后，数组左闭右开区间 `[firstIdx,lastIdx)` 内的所有元素的值均为需要填充的数．

## Collections

`Collections` 是 `java.util` 中对集合操作的一个工具类．方法均为静态方法，可使用类名直接调用．

### Collections.sort()

`Collections.sort()` 底层原理为将其中所有元素转化为数组调用 `Arrays.sort()`，完成排序后再赋值给原本的集合．又因为 Java 中 `Collection` 的元素类型均为对象类型，所以始终是归并排序去处理．

该方法无法对集合指定区间排序．

底层源码：

```java
default void sort(Comparator<? super E> c) {
    Object[] a = this.toArray();
    Arrays.sort(a, (Comparator) c);
    ListIterator<E> i = this.listIterator();
    for (Object e : a) {
        i.next();
        i.set((E) e);
    }
}
```

### Collections.binarySearch()

`Collections.binarySearch()` 是对集合中指定区间进行二分搜索，功能与 `Arrays.binarySearch()` 相同．

```java
Collections.binarySearch(list, key);
```

该方法无法对指定区间进行搜索．

### Collections.swap()

`Collections.swap()` 的功能是交换集合中指定二个位置的元素．

```java
 Collections.swap(list, i, j);
```

## 其他

### 数值比较问题

在 Java 中，如果单纯是数值类型，`-0.0 = 0.0`．若是对象类型，则 `-0.0 != 0.0`．如果尝试用 `Set` 统计斜率数量时，这个问题就会带来麻烦．提供的解决方式是在所有的斜率加入 `Set` 前将值增加 `0.0`．

```java
import java.io.PrintWriter;

public class Main {
    static PrintWriter out = new PrintWriter(System.out);
    
    static void A() {
        Double a = 0.0;
        Double b = -0.0;
        out.println(a.equals(b));  // false 
    }
    
    static void B() {
        Double a = 0.0;
        Double b = -0.0 + 0.0;
        out.println(a.equals(b));  // true 
    }
    
    static void C() {
        double a = 0.0;
        double b = -0.0;
        out.println(a == b);  // true 
    }
    
    
    public static void main(String[] args) {
        A();
        B();
        C();
        out.close();
    }
}
```

## 参考资料

[^ref1]: [Input & Output - USACO Guide](https://usaco.guide/general/input-output?lang=java#method-3---io-template)


## lang/java.md

## 关于 Java

Java 是一种广泛使用的计算机编程语言，拥有 **跨平台**、**面向对象**、**泛型编程** 的特性，广泛应用于企业级 Web 应用开发和移动应用开发．

## 环境安装

参见 [JDK](../tools/compiler.md#jdk)．

## 基本语法

### 主函数

Java 类似 C/C++ 语言，需要一个函数（在面向对象中，这被称为方法）作为程序执行的入口点．

Java 的主函数的格式是固定的，形如：

```java
class Test {
    public static void main(String[] args) {
        // 程序的代码
    }
}
```

一个打包的 Java 程序（名称一般是 `*.jar`）中可以有很多个类似的函数，但是当运行这个程序的时候，只有其中一个函数会被运行，这是定义在 `Jar` 的 `Manifest` 文件中的，在 OI 比赛中一般用不到关于它的知识．

### 注释

和 C/C++ 一样，Java 使用 `//` 和 `/* */` 分别注释单行和多行．

### 基本数据类型

|   类型名   |   意义  |
| :-----: | :---: |
| boolean |  布尔类型 |
|   byte  |  字节类型 |
|   char  |  字符型  |
|  double | 双精度浮点 |
|  float  | 单精度浮点 |
|   int   |   整型  |
|   long  |  长整型  |
|  short  |  短整型  |
|   null  |   空   |

### 声明变量

```java
int a = 12; // 设置 a 为整数类型,并给 a 赋值为 12
String str = "Hello, OI-wiki"; // 声明字符串变量 str
char ch = 'W';
double PI = 3.1415926;
```

### final 关键字

`final` 含义是这是最终的、不可更改的结果，被 `final` 修饰的变量只能被赋值一次，赋值后不再改变．

```java
final double PI = 3.1415926;
```

### 数组

```java
// 有十个元素的整数类型数组
// 其语法格式为 数据类型[] 变量名 = new 数据类型[数组大小]
int[] ary = new int[10];
```

### 字符串

-   字符串是 Java 一个内置的类．

```java
// 最为简单的构造一个字符串变量的方法如下
String a = "Hello";

// 还可以使用字符数组构造一个字符串变量
char[] stringArray = { 'H', 'e', 'l', 'l', 'o' };
String s = new String(stringArray);
```

### 包和导入包

Java 中的类（`Class`）都被放在一个个包（`package`）里面．在一个包里面不允许有同名的类．在类的第一行通常要说明这个类是属于哪个包的．例如：

```java
package org.oi-wiki.tutorial;
```

包的命名规范一般是：`项目所有者的顶级域.项目所有者的二级域.项目名称`．

通过 `import` 关键字来导入不在本类所属的包下面的类．例如下面要用到的 `Scanner`：

```java
import java.util.Scanner;
```

如果想要导入某包下面所有的类，只需要把这个语句最后的分号前的类名换成 `*`．

### 输入

可以通过 `Scanner` 类来处理命令行输入．

```java
package org.oiwiki.tutorial;

import java.util.Scanner;

class Test {
    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in); // System.in 是输入流
        int a = scan.nextInt();
        double b = scan.nextDouble();
        String c = scan.nextLine();
    }
}
```

### 输出

可以对变量进行格式化输出．

|  符号  |   意义  |
| :--: | :---: |
| `%f` |  浮点类型 |
| `%s` | 字符串类型 |
| `%d` |  整数类型 |
| `%c` |  字符类型 |

```java
class Test {
    public static void main(String[] args) {
        int a = 12;
        char b = 'A';
        double s = 3.14;
        String str = "Hello world";
        System.out.printf("%f\n", s);
        System.out.printf("%d\n", a);
        System.out.printf("%c\n", b);
        System.out.printf("%s\n", str);
    }
}
```

### 控制语句

Java 的流程控制语句与 C++ 是基本相同的．

#### 选择

-   if

```java
class Test {
    public static void main(String[] args) {
        if ( /* 判断条件 */ ){
            // 条件成立时执行这里面的代码
        }
    }
}
```

-   if...else

```java
class Test {
    public static void main(String[] args) {
        if ( /* 判断条件 */ ) {
            // 条件成立时执行这里面的代码
        } else {
            // 条件不成立时执行这里面的代码
        }
    }
}
```

-   if...else if...else

```java
class Test {
    public static void main(String[] args) {
        if ( /* 判断条件 */ ) {
            //判断条件成立执行这里面的代码
        } else if ( /* 判断条件2 */ ) {
            // 判断条件2成立执行这里面的代码
        } else {
          // 上述条件都不成立执行这里面的代码
        }
    }
}
```

-   switch...case

```java
class Test {
    public static void main(String[] args) {
        switch ( /* 表达式 */ ){
          case /* 值 1 */:
              // 当表达式取得的值符合值 1 执行此段代码
              break; // 如果不加上 break 语句,会让程序按顺序往下执行直到 break
          case /* 值 2 */:
              // 当表达式取得的值符合值 2 执行此段代码
              break;
          default:
              // 当表达式不符合上面列举的值的时候执行这里面的代码
        }
    }
}
```

#### 循环

-   for

`for` 关键字有两种使用方法，其中第一种是普通的 `for` 循环，形式如下：

```java
class Test {
    public static void main(String[] args) {
        for ( /* 初始化 */; /* 循环的判断条件 */; /* 每次循环后执行的步骤 */ ) {
            // 当循环的条件成立执行循环体内代码
        }
    }
}
```

第二种是类似 C++ 的 `foreach` 使用方法，用于循环数组或者集合中的数据，相当于把上一种方式中的循环变量隐藏起来了，形式如下：

```java
class Test {
    public static void main(String[] args) {
        for ( /* 元素类型X */ /* 元素名Y */ : /* 集合Z */ ) {
            // 这个语句块的每一次循环时，元素Y分别是集合Z中的一个元素．
        }
    }
}
```

-   while

```java
class Test {
    public static void main(String[] args) {
        while ( /* 判定条件 */ ) {
            // 条件成立时执行循环体内代码
        }
    }
}
```

-   do...while

```java
class Test {
    public static void main(String[] args) {
        do {
          // 需要执行的代码
        } while ( /* 循环判断条件 */ );
    }
}
```

## 注意事项

### 类名与文件名一致

创建  Java 源程序需要类名和文件名一致才能编译通过，否则编译器会提示找不到类．通常该文件名会在具体 OJ 中指定．

例：

`Add.java`

```java
class Add {
    public static void main(String[] args) {
        // ...
    }
}
```

在该文件中需使用 `Add` 为类名方可编译通过．


## lang/lambda.md

**注意**：考虑到算法竞赛的实际情况，本文将不会全面研究语法，只会讲述在算法竞赛中可能会应用到的部分．

本文语法参照 **C++11** 标准，其他高版本的标准语法视情况提及并会特别标注．

## Lambda 表达式

Lambda 表达式因数学中的 $\lambda$ 演算得名，直接对应于其中的 lambda 抽象．编译器在编译时会根据语法生成一个匿名的 [**函数对象**](./new.md#函数对象)，以捕获的变量作为其成员，参数和函数体用于实现 `operator()` 重载．

??? note "函数对象（Function Object）"
    函数对象是一种类对象，一般通过重载 `operator()` 实现，所以能像函数一样调用．相较于使用普通的函数，函数对象有很多优点，例如可以保存状态，可以作为参数传递给其他函数等．

以下是 lambda 的一种语法：

```text
[capture] (parameters) mutable -> return-type {statement}
```

Lambda 表达式本身是一个类，展开后如以下形式：

<!-- scripts.linter.preprocess.fix_details off -->

```text
class Lambda_1 {
 private:
  Lambda_1() : capture-list(init-value) { }

 public:
  return-type operator()(parameters) const { statement }

 private:
  mutable capture-list
};
```

<!-- scripts.linter.preprocess.fix_details on -->

空的 capture 可以隐式转换为函数指针，例如：

```cpp
void (*f)(int, int) = [](int, int) -> void {};
```

下面我们分别对语法中的各部分进行介绍．

### statement 函数体

Lambda 表达式的函数体与普通函数的函数体类似，除了能访问参数和全局变量等，还可访问 [捕获](#capture-捕获子句) 的变量．

### capture 捕获子句

lambda 以 capture 子句开头，它指定哪些变量被捕获，捕获列表可为空，或指定捕获方式：有 `&` 符号前缀的变量通过 [引用](./reference.md) 访问，没有该前缀的变量通过值访问．

我们也可以使用默认捕获模式，捕获 Lambda 中提及的所有变量：`&` 表示捕获到的所有变量都通过引用访问，`=` 表示捕获到的所有变量都通过值访问．

在默认捕获之后，仍然可以为特定的变量 **显式** 指定捕获模式．

如果需要引用访问外部变量 `a`，并通过值访问外部变量 `b`，那么以下捕获子句都可以做到：

-   `[&a, b]`
-   `[b, &a]`
-   `[&, b]`
-   `[b, &]`
-   `[=, &a]`

同时捕获列表也可以用于声明变量，类型由初始化器推导，类似于使用 `auto` 声明变量．

以下是一些常见的例子：

```cpp
int a = 0;
auto f0 = []() { return a * 9; };   // Error, 无法访问 'a'
auto f1 = [a]() { return a * 9; };  // OK, 'a' 被值「捕获」
auto f2 = [&a]() { return a++; };   // OK, 'a' 被引用「捕获」
auto f3 = [v = a + 1]() {
  return v + 1;
};  // OK, 使用初始化器声明变量 v，类型与 a 相同

// 注意，使用引用捕获时，请保证被调用时 a 没有被销毁
auto b = f2();  // f2 从捕获列表里获得 a 的值，无需通过参数传入 a
```

#### generalized capture 带初始化的捕获（C++14）

自 C++14 起，capture 不仅可以用来捕获外部变量，还可用于声明新的变量并初始化，例如：

```cpp
auto f1 = [val = 520]() {
  return val;
};  // OK, 定义 val 类型为 int，初始值为 520，返回值类型 int

auto f2 = [val = 520LL]() {
  return val;
};  // OK, 定义 val 类型为 long long，初始值为 520，返回值类型 long long

auto f3 = [val = "520"]() {
  return val;
};  // OK, 定义 val 类型为 const char*，初始值为 "520"，返回值类型 const char*

auto f4 = [val = "520"s]() {
  return val;
};  // OK, C++14 起，需要 using namespace std; 或 using namespace std::literals;
    // 定义 val 类型为 std::string，初始值为 std::string("520")，返回值类型
    // std::string

auto f5 = [val = std::string("520")]() {
  return val;
};  // OK, 定义 val 类型为 std::string，初始值为 std::string("520")，返回值类型
    // std::string

auto f6 = [val = std::vector<int>(3, 6)]() {
  return val;
};  // OK, 定义 val 类型为 std::vector<int>，大小为 3，元素填充 6，返回值类型
    // std::vector<int>

auto f7 = [val = 520]() -> int {
  return val;
};  // OK, 定义 val 类型为 int，初始值为 520，返回值类型 int

auto f8 = [val = 520]() -> long long {
  return val;
};  // OK, 定义 val 类型为 int，初始值为 520，返回值类型 long long
```

定义新的变量不可以省略初始值，变量的类型由初始值的类型决定，相当于：

```text
auto val = init-value;
```

以下是错误的写法：

```cpp
auto f = [val]() { return val; };  // Error: 'val' was not declared in this
                                   // scope, identifier "val" is undefined
```

初始化值也可以是外部变量，例如：

```cpp
int value = 520;
auto f = [val = value]() { return val; };
std::cout << f();  // Output: 520
```

`val` 也可以是一个引用类型，可以引用一个外部变量，通过这种方式可以为通过引用捕获的外部变量取个别名，例如：

```cpp
int value = 520;

auto f = [&val = value]() {
  return val;
};  // OK, 定义 val 类型为 int&，返回值类型 int，相当于 int& val = value;

std::cout << f() << '\n';  // Output: 520

value = 1314;

std::cout << f() << '\n';  // Output: 1314
```

捕获外部变量和定义新变量可以同时使用．

如果你想在 Lambda 表达式内修改 capture 中定义的新变量，需要使用 `mutable` 关键字，如果是引用则不需要，例如：

```cpp
int value = 520;

{
  auto f = [val = value]() mutable -> int {
    return val = 1314;
  };  // 需要 mutable
  auto val_f = f();
  std::cout << value << ' ' << val_f << std::endl;  // Output: 520 1314
}

{
  auto f = [&val = value]() -> int { return val = 1314; };  // 不需要 mutable
  auto val_f = f();
  std::cout << value << ' ' << val_f << std::endl;  // Output: 1314 1314
}
```

详见 [mutable 可变规范](#mutable-可变规范)．

在 capture 中定义的变量的生命周期跟随 Lambda 表达式的接收方，在以上几个示例中为变量 $f$，因为 Lambda 本身其实是一个类，capture 中的所有内容都是这个类的 `private` 成员变量，例如：

```cpp
int main() {
  auto f = [val = 0]() mutable -> int { return ++val; };  // val 被构造和初始化

  std::cout << f() << '\n';  // Output: 1
  std::cout << f() << '\n';  // Output: 2
  std::cout << f() << '\n';  // Output: 3
}  // val 跟随 f 被销毁
```

### parameters 参数列表

大多数情况下类似于函数的参数列表，例如：

```cpp
int x[] = {5, 1, 7, 6, 1, 4, 2};
std::sort(x, x + 7, [](int a, int b) { return (a > b); });
for (auto i : x) std::cout << i << " ";
```

这将打印出 `x` 数组从大到小排序后的结果．

由于 **parameters 参数列表** 是可选的，如果不将参数传递给 lambda，并且其声明不包含 [mutable](#mutable-可变规范)，且没有后置返回值类型，则可以省略空括号．

??? note "使用 `auto` 声明的参数"
    **C++14** 后，若参数使用 `auto` 声明类型，那么会构造一个 [泛型 Lambda 表达式](#泛型-lambdac14)．

#### 显式对象形参（C++23）

**C++23** 起，[显式对象形参](https://zh.cppreference.com/w/cpp/language/function#.E5.BD.A2.E5.8F.82.E5.88.97.E8.A1.A8) 可以在 lambda 的参数中使用．

```cpp
auto nth_fibonacci = [](this auto self, unsigned n) -> unsigned {
  return n < 2 ? n : self(n - 1) + self(n - 2);
};

cout << nth_fibonacci(10u);
```

### mutable 可变规范

使得函数体可以修改通过值捕获的变量．

```cpp
int a = 0;
auto by_value = [a]() mutable { ++a; };
auto by_ref = [&a] { ++a; };

by_value();
by_ref();
```

在执行完 `by_value()` 后，`by_value` 的捕获成员 `a` 为 1，但外部的变量 `a` 依然为 0．
而在执行完 `by_ref()` 后，外部 `a` 的值变为 1．

### return-type 返回类型

用于指定 lambda 表达式的返回类型．如果省略，则返回类型将被自动推断（行为与用 `auto` 声明返回值的函数一致）．

多个 `return` 语句且推导类型不一致时，将产生编译错误．

```cpp
auto lam = [](int a, int b) -> int { return 0; };

auto x1 = [](int i) { return i; };

auto x2 = [](bool condition) {
  if (condition) return 1;
  return 1.0;
};  // Error, 推导类型不一致
```

### 泛型 Lambda（C++14）

使用 `auto` 作为参数类型，可以构造泛型 lambda．

```cpp
auto add = [](auto a, auto b) { return a + b; };
```

在 [cpp insights](https://cppinsights.io) 中可以观察到编译器生成的 `lambda` 类定义：

```cpp
class add_lambda {
 public:
  template <class T, class U>
  auto operator()(T a, U b) const {
    return a + b;
  }
};

add_lambda add{};
```

`add` 两个参数声明均使用了 `auto`，对应为 `add_lambda` 类的 `operator()` 函数模板的两个模板参数 `T` 和 `U`．

### Lambda 中的递归

先来看一个编译失败的例子：

```cpp
int n = 10;

auto dfs = [&](int i) -> void {
  if (i == n)
    return;
  else
    dfs(i + 1);  // Error: a variable declared with an auto type specifier
                 // cannot appear in its own initializer
};
```

我们这里尝试在捕获列表中捕获 $dfs$，但是有一个问题，$dfs$ 的类型为 `auto`，要等待等号右边的类型推导完成后才会推导出 $dfs$ 的类型，而 Lambda 要捕获 $dfs$ 就必须要确定 $dfs$ 的类型后才能创建它的引用变量，好，这会陷入了一个套娃过程．

怎么解决这个问题呢？

1.  显式指定 $dfs$ 的类型，可以使用 `std::function` 替代．

    ???+ example "修改如上代码为："
        ```cpp
        int n = 10;
        
        std::function<void(int)> dfs = [&](int i) -> void {
          if (i == n)
            return;
          else
            dfs(i + 1);  // OK
        };
        
        dfs(1);
        ```

    ??? warning "不建议使用 [`std::function`](./new.md#stdfunction) 实现的递归"
        `std::function` 的类型擦除通常需要分配额外内存，同时间接调用带来的寻址操作会进一步降低性能．
        
        在 [Benchmark](https://quick-bench.com/q/U5qf_dHHKsSyVU83jmt0p_U541c) 测试中，使用 Clang 17 编译器，libc++ 作为标准库，`std::function` 实现比 lambda 实现的递归慢了约 2.5 倍．
        
        ??? note "测试代码"
            ```cpp
            #include <algorithm>
            #include <functional>
            #include <numeric>
            #include <random>
            
            using namespace std;
            
            const auto& nums = [] {
              random_device rd;
              mt19937 gen{rd()};
              array<unsigned, 32> arr{};
            
              std::iota(arr.begin(), arr.end(), 0u);
              ranges::shuffle(arr, gen);
            
              return arr;
            }();
            
            static void std_function_fib(benchmark::State& state) {
              std::function<int(int)> fib;
            
              fib = [&](int n) { return n <= 2 ? 1 : fib(n - 1) + fib(n - 2); };
            
              unsigned i = 0;
            
              for (auto _ : state) {
                auto res = fib(nums[i]);
                benchmark::DoNotOptimize(res);
            
                ++i;
            
                if (i == nums.size()) i = 0;
              }
            }
            
            BENCHMARK(std_function_fib);
            
            static void template_lambda_fib(benchmark::State& state) {
              auto n_fibonacci = [](const auto& self, int n) -> int {
                return n <= 2 ? 1 : self(self, n - 1) + self(self, n - 2);
              };
            
              unsigned i = 0;
            
              for (auto _ : state) {
                auto res = n_fibonacci(n_fibonacci, nums[i]);
                benchmark::DoNotOptimize(res);
            
                ++i;
            
                if (i == nums.size()) i = 0;
              }
            }
            
            BENCHMARK(template_lambda_fib);
            ```
2.  不通过捕获的方式获取 $dfs$，而是通过函数传参的方式．

    ???+ example "修改如上代码为："
        ```cpp
        int n = 10;
        
        // 参数列表中有参数类型为 auto，则这个 Lambda 类中的 operator()
        // 函数将被定义为模板函数，模板函数可以在稍后被调用时再进行实例化
        auto dfs = [&](auto& self,
                       int i) -> void  // [&] 只会捕获用到的变量，所以不会捕获 auto dfs
        {
          if (i == n)
            return;
          else
            self(self, i + 1);  // OK
        };
        
        dfs(dfs, 1);
        ```

    ???+ note "`auto self`、`auto& self` 和 `auto&& self` 的区别："
        `auto& self` 和 `auto&& self` 理论上都只会使用 $8$ 个字节（指针的大小）用作传参，不会发生其他的拷贝．具体要看编译器对 Lambda 的实现方式和对应的优化．
        而使用 `auto self` 会发生对象拷贝，拷贝的大小取决于捕获列表中的元素，因为它们都是这个 Lambda 类中的私有成员变量．
3.  可以通过手动展开 Lambda 类，或使用类似写法，这样可以直接声明 $dfs$ 的类型．

    ???+ example "修改如上代码为："
        ```cpp
        int n = 10;
        
        class Lambda_1 {
         public:
          auto operator()(int i) const -> void {
            if (i == n)
              return;
            else
              (*this)(i + 1);  // OK
          }
        
          explicit Lambda_1(int& __n) : n(__n) {}
        
         private:
          int& n;
        } dfs(n);
        
        dfs(1);
        ```
4.  如果 lambda 没有捕获任何变量，我们也可以利用函数指针．

    如果 lambda 没有捕获任何变量，那么它可以隐式转换为函数指针．同时 lambda 此时也可以声明为 `static`，函数指针类型也可以声明为 `static`．如此依赖，lambda 可以不需要捕获就能访问函数指针，从而实现递归．

    ???+ example "示例"
        ```cpp
        static unsigned (*fptr)(unsigned);
        
        static const auto lambda = [](const unsigned a) {
          return a < 2 ? a : (*fptr)(a - 2) + (*fptr)(a - 1);
        };
        
        static auto init = [] {
          fptr = +lambda;
          // Or
          // fptr = static_cast<unsigned (*)(unsigned)>(lambda);
          return 0;
        }();
        
        cout << lambda(10);
        ```

### Lambda 表达式的应用

#### 作为标准库算法的 Predicate（谓词）

从大到小排序：

```cpp
std::vector<int> v = {1, 2, 3, 4, 5};
std::sort(v.begin(), v.end(), [](int a, int b) { return a > b; });
```

使用 [std::find\_if](https://zh.cppreference.com/w/cpp/algorithm/find) 查找第一个大于 3 的元素：

```cpp
std::vector<int> v = {1, 2, 3, 4, 5};
auto it = std::find_if(v.begin(), v.end(), [](int a) { return a > 3; });
```

#### 控制中间变量的生命周期

在算法竞赛中，我们会遇到这样的场景：一个变量的初始化需要使用之前声明的变量，其初始化过程又生成占用空间较大的中间变量．

我们希望能尽快析构这些中间变量，以降低内存消耗．此时，我们可以使用 lambda 来控制这些中间变量的生命周期．

```cpp
void solution(const vector<int>& input) {
  int b = [&] {
    vector<int> large_objects(input.size());
    int c = 0;

    for (int i = 0; i < large_objects.size(); ++i)
      large_objects[i] = i + input[i];

    for (int i = 0; i < input.size(); ++i) c += large_objects[input[i]];

    return c;
  }();

  // ...
}
```

相较于使用块作用域，lambda 可以允许我们使用返回值，使得代码更加简洁；相较于函数，我们不需要额外起名和声明被捕获的各种参数，使得代码更加紧凑．

## 参考文献

-   [cppreference-lambda](https://en.cppreference.com/w/cpp/language/lambda)
-   [Stackoverflow: Overhead with std::function](https://stackoverflow.com/a/33881130/11120338)


## lang/loop.md

有时，我们需要做一件事很多遍，为了不写过多重复的代码，我们需要循环．

有时，循环的次数不是一个常量，那么我们无法将代码重复多遍，必须使用循环．

## for 语句

以下是 for 语句的结构：

```cpp
for (初始化; 判断条件; 更新) {
  循环体;
}
```

执行顺序：

![](images/for-loop.svg)

e.g. 读入 n 个数：

```cpp
for (int i = 1; i <= n; ++i) {
  cin >> a[i];
}
```

for 语句的三个部分中，任何一个部分都可以省略．其中，若省略了判断条件，相当于判断条件永远为真．

## while 语句

以下是 while 语句的结构：

```cpp
while (判断条件) {
  循环体;
}
```

执行顺序：

![](images/while-loop.svg)

e.g. 验证 3x+1 猜想：

```cpp
while (x > 1) {
  if (x % 2 == 1) {
    x = 3 * x + 1;
  } else {
    x = x / 2;
  }
}
```

## do...while 语句

以下是 do...while 语句的结构：

```cpp
do {
  循环体;
} while (判断条件);
```

执行顺序：

![](images/do-while-loop.svg)

与 while 语句的区别在于，do...while 语句是先执行循环体再进行判断的．

e.g. 枚举排列：

```cpp
do {
  // do someting...
} while (next_permutation(a + 1, a + n + 1));
```

## 三种语句的联系

```cpp
// for 语句

for (statement1; statement2; statement3) {
  statement4;
}

// while 语句

statement1;
while (statement2) {
  statement4;
  statement3;
}
```

在 statement4 中没有 `continue` 语句（见下文）的时候是等价的，但是下面一种方法很少用到．

```cpp
// while 语句

statement1;
while (statement2) {
  statement1;
}

// do...while 语句

do {
  statement1;
} while (statement2);
```

在 statement1 中没有 `continue` 语句的时候这两种方式也是等价的．

```cpp
while (1) {
  // do something...
}

for (;;) {
  // do something...
}
```

这两种方式都是永远循环下去．（可以使用 `break`（见下文）退出．）

可以看出，三种语句可以彼此代替，但一般来说，语句的选用遵守以下原则：

1.  循环过程中有个固定的增加步骤（最常见的是枚举）时，使用 for 语句；
2.  只确定循环的终止条件时，使用 while 语句；
3.  使用 while 语句时，若要先执行循环体再进行判断，使用 do...while 语句．一般很少用到，常用场景是用户输入．

## break 与 continue 语句

break 语句的作用是退出循环．

continue 语句的作用是跳过循环体的余下部分．下面以 continue 语句在 do...while 语句中的使用为例：

```cpp
do {
  // do something...
  continue;  // 等价于 goto END;
// do something...
END:;
} while (statement);

```

break 与 continue 语句均可在三种循环语句的循环体中使用．

一般来说，break 与 continue 语句用于让代码的逻辑更加清晰，例如：

```cpp
// 逻辑较为不清晰，大括号层次复杂

for (int i = 1; i <= n; ++i) {
  if (i != x) {
    for (int j = 1; j <= n; ++j) {
      if (j != x) {
        // do something...
      }
    }
  }
}

// 逻辑更加清晰，大括号层次简单明了

for (int i = 1; i <= n; ++i) {
  if (i == x) continue;
  for (int j = 1; j <= n; ++j) {
    if (j == x) continue;
    // do something...
  }
}
```

```cpp
// for 语句判断条件复杂，没有体现「枚举」的本质

for (int i = l; i <= r && i % 10 != 0; ++i) {
  // do something...
}

// for 语句用于枚举，break 用于「到何时为止」

for (int i = l; i <= r; ++i) {
  if (i % 10 == 0) break;
  // do something...
}
```

```cpp
// 语句重复，顺序不自然

statement1;
while (statement3) {
  statement2;
  statement1;
}

// 没有重复语句，顺序自然

while (1) {
  statement1;
  if (!statement3) break;
  statement2;
}
```


## lang/namespace.md

## 概述

C++ 的 **命名空间** 机制可以用来解决复杂项目中名字冲突的问题．

举个例子：C++ 标准库的所有内容均定义在 `std` 命名空间中，如果你定义了一个叫 `cin` 的变量，则可以通过 `cin` 来访问你定义的 `cin` 变量，通过 `std::cin` 访问标准库的 `cin` 对象，而不用担心产生冲突．

## 声明

下面的代码声明了一个名字叫 `A` 的命名空间：

```cpp
namespace A {
int cnt;

void f(int x) { cnt = x; }
}  // namespace A
```

声明之后，在这个命名空间外部，你可以通过 `A::f(x)` 来访问命名空间 `A` 内部的 `f` 函数，也可以通过 `A::cnt` 来访问命名空间 `A` 内部的 `cnt` 变量．

命名空间的声明是可以嵌套的，因此下面这段代码也是允许的：

```cpp
namespace A {
namespace B {
void f() { ... }
}  // namespace B

void f() {
  B::f();  // 实际访问的是 A::B::f()，由于当前位于命名空间 A
           // 内，所以可以省略前面的 A::
}
}  // namespace A

void f()  // 这里定义的是全局命名空间的 f 函数，与 A::f 和 A::B::f
          // 都不会产生冲突
{
  A::f();
  A::B::f();
}
```

## `using` 指令

声明了命名空间之后，如果在命名空间外部访问命名空间内部的成员，需要在成员名前面加上 `命名空间::`．

有没有什么比较方便的方法能让我们直接通过成员名访问命名空间内的成员呢？答案是肯定的．我们可以使用 `using` 指令．

`using` 指令有如下两种形式：

1.  `using 命名空间::成员名;`：这条指令可以让我们省略某个成员名前的命名空间，直接通过成员名访问成员，相当于将这个成员导入了当前的作用域．
2.  `using namespace 命名空间;`：这条指令可以直接通过成员名访问命名空间中的 **任何** 成员，相当于将这个命名空间的所有成员导入了当前的作用域．

因此，如果执行了 `using namespace std;`，就会在当前作用域将 `std` 中的所有名字引入到全局命名空间当中．这样，我们就可以用 `cin` 代替 `std::cin`，用 `cout` 代替 `std::cout`．

??? warning "`using` 指令可能会导致命名冲突！"
    由于 `using namespace std;` 会将 `std` 中的 **所有名字** 引入，因此如果声明了与 `std` 重名的变量或函数，就可能会因为命名冲突而导致编译错误．
    
    因此在工程中，并不推荐使用 `using namespace 命名空间;` 的指令．

有了 `using` 指令，[C++ 语法基础](./basic.md#cin-与-cout) 中的代码可以有这两种等价写法：

```cpp
#include <iostream>

using std::cin;
using std::cout;
using std::endl;

int main() {
  int x, y;
  cin >> x >> y;
  cout << y << endl << x;
  return 0;
}
```

```cpp
#include <iostream>

using namespace std;

int main() {
  int x, y;
  cin >> x >> y;
  cout << y << endl << x;
  return 0;
}
```

## 无名命名空间

当我们在一个作用域里只定义了一个用于防止名字冲突的命名空间时，其定义和使用将可以变得非常简洁．我们可以使用无名命名空间．

形如 `namespace { /* something ... */ } `（省略命名空间的名字）定义的命名空间被称为无名命名空间．一个文件里的无名命名空间会被视为拥有独有的名字，和其他命名空间都不同，但同一个作用域内多个无名命名空间被视为相同的命名空间．在无名命名空间定义后，其中的名字在其外的作用域内可以在使用时被查找到，如同在无名命名空间定义后加入了一条 `using namespace` 指令．

## 应用

### 防止子任务间名字冲突

在一些具有多个子任务的问题中，我们可以对每个子任务各定义一个命名空间，在其中定义我们解决该子任务所需要的变量与函数，这样即使两个子任务的实现中即使声明了相同名字也不会冲突，从而使各个子任务间互不干扰，会在一定程度上方便调试，也会改善程序的可读性．

### 防止与标准库以及环境引入的名字冲突

同时，使用命名空间也可以防止一些算法竞赛中常用的名字与标准冲突，如下例：

```cpp
#include <math.h>

#include <vector>

using namespace std;

namespace Sol {
int end;  // std::end 被 using namespace std; 引入

int y1;  // y1 是 POSIX 定义的第二类 Bessel 函数

// 因此通常情况下，在 Linux 下会有冲突而在 Windows 下没有

void solve() {
  // 在 Sol::solve() 里无限定（不用 ::）地使用我们声明的 end 以及 y1
  // 并不会导致名字冲突； 而若以上代码在全局命名空间中，将会导致冲突： 其中 end
  // 只会在名字查找（即编译使用它的代码）时与 std::end 冲突，而 y1
  // 在声明时就会冲突； 并且 y1 的冲突因为与环境有关甚至在 Windows
  // 下不会被发现，却会在 Linux 的评测环境下造成编译错误．
}
}  // namespace Sol

int main() { Sol::solve(); }
```

## 参考

-   [Namespaces - cppreference.com](https://en.cppreference.com/w/cpp/language/namespace)


## lang/new.md

**注意**：考虑到算法竞赛的实际情况，本文将不会全面研究语法，只会讲述在算法竞赛中可能会应用到的部分．

本文语法参照 **C++11** 标准．语义不同的将以 **C++11** 作为标准，C++14、C++17 等语法视情况提及并会特别标注．

## `auto` 类型说明符

`auto` 类型说明符用于自动推导变量等的类型．例如：

```cpp
auto a = 1;        // a 是 int 类型
auto b = a + 0.1;  // b 是 double 类型
```

注意 `auto` 会去除引用，如果不希望出现拷贝开销，需要手动指定：

```cpp
int a = 1;
int& b = a;
auto c = b;   // c 是 int 类型，有拷贝开销
auto& e = a;  // e 是 int& 类型，没有拷贝开销
```

## decltype 说明符

`decltype` 可以根据 **实体** 或 **表达式** 推断类型，注意二者推导类型的方式不同，错误使用可能造成悬垂引用．竞赛中不常用，此处仅粗略介绍．

```cpp
#include <iostream>
#include <vector>

int main() {
  int a = 1926;
  decltype(a) b;                 // 根据实体推断， b 是 int 类型
  decltype(1 + 1) c;             // 根据表达式推断，c 是 int 类型
  decltype((a)) d = a;           // 根据表达式推断，d 是 int& 类型！
  std::vector<decltype(b)> vec;  // 根据实体推断，vec 是 std::vector <int> 类型
  return 0;
}
```

## constexpr

> 另请参阅 [常量表达式 constexpr（C++11）](const.md#常量表达式-constexprc11)

## 基于范围的 `for` 循环

使用范围 for 遍历可迭代对象，与使用迭代器遍历的效率相同．上述二者的效率一般优于索引遍历，因为不需要根据索引寻址．

下面是一种简单的基于范围的 `for` 循环的语法：

```cpp
for (item_declaration : range_initializer) statement
```

比如：

```cpp
std::array<int, 4> arr = {1, 2, 3, 4};
for (int x : arr) {
  std::cout << x << std::endl;
}
```

上述语法产生的代码效果等价于下列代码：

```cpp
std::array<int, 4> arr = {1, 2, 3, 4};
for (auto px = arr.begin(), ed = arr.end(); px != ed; ++px) {
  std::cout << *px << std::endl;
}
```

### item-declaration 项声明

声明一个变量用于接受右侧容器中的元素，变量类型要与容器内子元素类型一致．可以用 `auto` 自动推导类型，复杂类型常用 `auto&` 防止拷贝开销．

### range-initializer 范围初始化器

范围初始化器可以是任何一种可迭代的对象（比如数组，或定义了 `begin` 和 `end` 成员函数的类对象）．如果放入表达式，表达式也只会计算一次．

例子：

```cpp
int a[] = {1, 1, 4, 5, 1, 4};
std::vector<int> b{1, 1, 4, 5, 1, 4};
std::map<std::string, int> c{{"114", 114}, {"514", 514}};
for (int i : a) std::cout << i;
for (auto i : b) std::cout << i;
// 下方 i 的类型是 std::pair<const std::string, int>&
for (auto& i : c) std::cout << i.first << i.second;
for (auto i : {1, 1, 4, 5, 1, 4}) std::cout << i;
```

### 自定义类型支持范围 for

只需提供 `begin` 和 `end` 成员函数，返回类型需要支持比较、自增和解引用（`*` 运算符）．

这里有一个例子：

```cpp
#include <iostream>

struct C {
  int a[4];

  int* begin() { return a; }

  int* end() { return a + 4; }
};

int main() {
  C c = {1, 9, 2, 6};
  for (auto i : c) std::cout << i << " ";
  std::cout << std::endl;
  // output: 1 9 2 6
  return 0;
}
```

### 初始化语句（C++20）

在 C++20 中还可以使用初始化语句实现一些功能，例如循环计数器：

```cpp
#include <iostream>
#include <vector>

int main() {
  std::vector<int> v = {0, 1, 2, 3, 4, 5};

  for (int counter = 0; auto i : v)  // the init-statement (C++20)
    std::cout << counter++ << ' ' << i << std::endl;
}
```

## 结构化绑定（C++17）

结构化绑定（Structured binding）是 C++17 提供的一种语法糖，可以方便的提取子元素或子元素的引用，像这样：

```cpp
struct C {
  int x{1}, y{2};
};

int arr[]{4, 5, 6};

auto [c1, c2] = C{};       // c1=1,c2=2; int 类型
auto& [a1, a2, a3] = arr;  // a1=arr[0],a2=arr[1],a3=arr[2]; int& 类型
```

注意以下几点：

-   左侧声明的变量数和右侧对象的子元素数必须一致
-   类型声明需要使用 `auto`
-   可以使用 `&` 修饰获取引用

你可以在遍历 `map` 容器时这样写：

```cpp
std::map<std::string, int> m = {{"k1", 1}, {"k2", 2}};

// 使用 "auto&" ，没有拷贝开销
for (auto& [k, v] : m) {
  // k 的类型是 const std::string& ，因为键自带 const 修饰
  // v 的类型是 int&
  std::cout << k << ' ' << v << std::endl;
}
```

## std::tuple 元组

[元组](https://zh.cppreference.com/w/cpp/utility/tuple) 定义于头文件 `<tuple>`，是 `std::pair` 的推广，可以存储多个不同类型的值．下面来看一个例子：

```cpp
#include <iostream>
#include <tuple>
#include <vector>

constexpr auto expr = 4 - 1;  // expr = 3

int main() {
  std::vector<int> vec = {1, 9, 2, 6, 0};
  std::tuple<int, int, std::string, std::vector<int>> tup =
      std::make_tuple(817, 114, "514", vec);

  // 使用 get<> 获取子元素，尖括号内必须是整型常量表达式
  for (auto i : std::get<expr>(tup)) std::cout << i << " ";
  // 首元素编号为 0，故我们 std::get<3> 得到了一个 std::vector<int>
  return 0;
}
```

在 C++17 之后可以使用结构化绑定提取值，像这样：

```cpp
std::vector<int> vec = {1, 9, 2, 6, 0};
std::tuple<int, int, std::string, std::vector<int>> tup =
    std::make_tuple(817, 114, "514", vec);

auto& [a, b, c, d] = tup;  // C++17 Structured binding
std::cout << a << ' ' << b << c << std::endl;
std::cout << d.size() << ' ' << d[2] << std::endl;
```

### 成员函数

| 函数          | 作用                   |
| ----------- | -------------------- |
| `operator=` | 赋值一个 `tuple` 的内容给另一个 |
| `swap`      | 交换两个 `tuple` 的内容     |

例子：

```cpp
constexpr std::tuple<int, int> tup = {1, 2};
std::tuple<int, int> tupA = {2, 3}, tupB;
tupB = tup;
tupB.swap(tupA);
```

### 非成员函数

| 函数             | 作用                           |
| -------------- | ---------------------------- |
| `make_tuple`   | 创建一个 `tuple` 对象，其类型根据各实参类型定义 |
| `std::get`     | 元组式访问指定的元素                   |
| `std::tie`     | 将元组中的值赋值到已有变量                |
| `operator==` 等 | 按字典顺序比较 `tuple` 中的值          |
| `std::swap`    | 特化的 `std::swap` 算法           |

例子：

```cpp
std::tuple<int, int> tupA = {2, 3}, tupB;
tupB = std::make_tuple(1, 2);
std::swap(tupA, tupB);
std::cout << std::get<1>(tupA) << std::endl;
int x;
std::tie(x, std::ignore) = tupB;
std::cout << x << std::endl;
```

`std::tie` 将元组元素赋值给已有变量，可以使用 `std::ignore` 跳过不需要的元素．结构化绑定直接声明新变量（支持值/引用绑定），必须接受所有元素．

## 函数对象

可以使用函数调用运算符 `operator()` 的对象，称为函数对象（FunctionObject）．

它不是一种语言特性，而是一种 [概念或者要求](https://zh.cppreference.com/w/cpp/named_req/FunctionObject)，在标准库中广泛应用．

函数对象大致可以分成两类：

1.  函数指针
2.  重载了 `operator()` 运算符的类对象

[lambda](./lambda.md) 就是典型的第二类函数对象，它将捕获的内容存放在成员变量中，并重载了函数调用运算符．

## Lambda 表达式

> 请参考 [Lambda 表达式](lambda.md) 页面．

## std::function

???+ warning "请注意性能开销"
    `std::function` 会引入一定的性能开销，经 [Benchmark](./lambda.md#lambda-中的递归) 测试，通常会造成 2 到 3 倍以上的性能损失．
    
    因为它使用了类型擦除的技术，而这通常借由虚函数机制实现，调用虚函数会引入额外的 [开销](https://stackoverflow.com/questions/5057382/what-is-the-performance-overhead-of-stdfunction)．
    
    请考虑使用 [**Lambda 表达式**](./lambda.md) 或者 [**函数对象**](#函数对象) 代替．

`std::function` 是通用函数封装器，定义于头文件 `<functional>`．

`std::function` 的实例能存储、复制及调用任何 [**可调用**](https://zh.cppreference.com/w/cpp/named_req/Callable) 对象，这包括 [**Lambda 表达式**](./lambda.md)、成员函数指针或其他 [**函数对象**](#函数对象)．

若 `std::function` 不含任何可调用对象（比如默认构造），调用时将抛出 [`std::bad_function_call`](https://zh.cppreference.com/w/cpp/utility/functional/bad_function_call) 异常．

```cpp
#include <functional>
#include <iostream>

struct Foo {
  Foo(int num) : num_(num) {}

  void print_add(int i) const { std::cout << num_ + i << '\n'; }

  int num_;
};

void print_num(int i) { std::cout << i << '\n'; }

struct PrintNum {
  void operator()(int i) const { std::cout << i << '\n'; }
};

int main() {
  // 存储自由函数
  std::function<void(int)> f_display = print_num;
  f_display(-9);

  // 存储 Lambda
  std::function<void()> f_display_42 = []() { print_num(42); };
  f_display_42();

  // 存储到成员函数的调用
  std::function<void(const Foo&, int)> f_add_display = &Foo::print_add;
  const Foo foo(314159);
  f_add_display(foo, 1);
  f_add_display(314159, 1);

  // 存储到数据成员访问器的调用
  std::function<int(Foo const&)> f_num = &Foo::num_;
  std::cout << "num_: " << f_num(foo) << '\n';

  // 存储到函数对象的调用
  std::function<void(int)> f_display_obj = PrintNum();
  f_display_obj(18);
}
```

## 可变参数函数模板

在 C++11 之前，类模板和函数模板都只能接受固定数目的模板参数．C++11 允许 **任意个数、任意类型** 的模板参数．

这里仅简要介绍可变参数 **函数** 模板．

下列代码声明的函数模板 `fun` 可以接受任意个数、任意类型的模板参数作为它的模板形参．

```cpp
template <typename... Clazz>
void fun(Clazz... paras) {}
```

`paras` 是一个函数参数包（function parameter pack），接受 0 个或多个函数实参．`Clazz` 是一个模板参数包（template parameter pack），接受 0 个或多个模板实参（非类型、类型或模板），以 `typename` 标记时只接受类型．

可以简单理解如下：

-   模板参数包通常是一些类型名（但也可以使用编译期常量或模板名）
-   函数参数包通常是一些变量名

现在可以这么调用 `fun` 函数：

```cpp
fun();
fun(1);
fun(1, 2, 3);
fun(1, 0.0, "abc");
```

### 参数包展开

#### 参数包展开语法

参数包展开非常简单，使用 `...` 即可，将自动使用 `,` 分隔．比如：

```cpp
template <class A, class... C>
void func(A arg1, C... arg2) {
  // C 是 模板参数包
  tuple<A, C...>();  // 展开成 tuple<int, int, double, bool>();

  // arg2 是函数参数包
  func(arg2...);  // 展开成 func( 2, 1.1, true );
}

func(1, 2, 1.1, true);
```

参数包展开时还可以附带需要的运算，比如：

```cpp
template <class A, class... C>
void func(A arg1, C... arg2) {
  func((arg2 + 1)...);
  // 展开成 func( (2+1) , (1.1+1), (2.1f+1) );
}

func(1, 2, 1.1, 2.1f);
```

#### 终止函数

上面的函数无法运行，因为参数数量不断减少，最后变为空参并报错．

我们需要指定终止条件，可以提供一个普通函数，像这样：

```cpp
void func() {}

template <class A, class... C>
void func(A arg1, C... arg2) {
  std::cout << arg1 << std::endl;
  func((arg2 + 1)...);
}

func(1, 2, 1.1, 2.1f);
```

这样，参数数量不为 0 时会调用模板，空参时会调用普通函数，就能正常运行了．

### 折叠表达式（C++17）

C++17 提供了一种简便的语法处理 **函数参数包**，他的语法是这样的（必须用小括号包裹）：

1.  `( pack op ... )`，会变成 `(E1 op (... op (EN-1 op EN)))`
2.  `( ... op pack )`，会变成 `(((E1 op E2) op ...) op EN)`
3.  `( pack op ... op init )`，会变成 `(E1 op (... op (EN−1 op (EN op I))))`
4.  `( init op ... op pack )`，会变成 `((((I op E1) op E2) op ...) op EN)`

简单演示一下就好理解了：

```cpp
template <class... C>
void func(C... args) {
  (std::cout << ... << args) << std::endl;
  // 语法 4, 等价于 ↓
  // ( ( ( std::cout << 1 ) << 2.1 ) << true ) << std::endl;
  // 输出: 12.11  注意true输出成了1，因为这里没有指定boolalpha

  std::cout << (args && ...) << std::endl;
  // 语法 1, 等价于 ↓
  // std::cout << ( 1 && ( 2.1 && true ) ) ) << std::endl;
  // 输出: 1
}

func(1, 2.1, true);
```

### 缩写函数模板（C++20）

C++20 起可以直接使用 `auto ...` 作为参数类型，实现函数模板的缩写：

```cpp
void func(auto... args) { (std::cout << ... << args) << std::endl; }
```

注意它本质上仍然是函数模板，与下面的写法等价：

```cpp
template <class... T>
void func(T... args) {
  (std::cout << ... << args) << std::endl;
}
```

## 范围库（C++20）

> 范围库是对迭代器和泛型算法库的一个扩展，使得迭代器和算法可以通过组合变得更强大，并且减少错误．

范围即可遍历的序列，包括数组、容器、视图等．

在需要对容器等范围进行复杂操作时，[范围库](https://zh.cppreference.com/w/cpp/ranges) 可以使得算法编写更加容易和清晰．

### View 视图

视图是一种轻量对象，通过特定机制（如自定义迭代器）来实现一些算法，给范围提供了更多的遍历方式以满足需求．

范围库中已实现了一些常用的视图，大致分为两种：

1.  **范围工厂**，用于构造一些特殊的范围，使用这类工厂可以省去手动构造容器的步骤，降低开销，直接生成一个范围．
2.  **范围适配器**，提供多种多样的遍历支持，既能像函数一样调用，也可以通过管道运算符 `|` 连接，实现链式调用．

**范围适配器** 作为 [**范围适配器闭包对象**](https://zh.cppreference.com/w/cpp/named_req/RangeAdaptorClosureObject)，也属于 [**函数对象**](#函数对象)，它们重载了 `operator|`，使得它们能够像管道一样拼装起来．

??? note "管道运算符"
    此处的 `|` 应该理解成管道运算符，而非按位或运算符，这个用法来自于 Linux 中的 [管道](https://zh.wikipedia.org/wiki/%E7%AE%A1%E9%81%93_%28Unix%29)．

在复杂操作下，也能保持良好可读性，有以下特性：

若 A、B、C 为一些范围适配器闭包对象，R 为某个范围，其他字母为可能的有效参数，表达式

    R | A(a) | B(b) | C(c, d)

等价于

    C(B(A(R, a), b), c, d)

下面以 `ranges::take_view` 与 `ranges::iota_view` 为例：

```cpp
#include <iostream>
#include <ranges>

int main() {
  const auto even = [](int i) { return 0 == i % 2; };

  for (int i : std::views::iota(0, 6) | std::views::filter(even))
    std::cout << i << ' ';
}
```

1.  范围工厂 `std::views::iota(0, 6)` 生成了从 0 到 5 的整数序列的范围
2.  范围适配器 `std::views::filter(even)` 过滤前一个范围，生成了一个只剩下偶数的范围
3.  两个操作使用管道运算符链接

上述代码不需要额外分配堆空间存储每步生成的范围，实际的生成和过滤运算发生在遍历操作中（更具体而言，内部的迭代器构造、自增和解引用），也就是零开销（Zero Overhead）．

同时，外部输入的范围生命周期，等同于 **范围适配器** 的内部元素的生命周期．如果外部范围（比如容器、范围工厂）已经销毁，那么再对这些的视图遍历，其效果与解引用悬垂指针一致，属于未定义行为．

为了避免上述情况，应该严格要求适配器的生命周期位于其使用的任何范围的生命周期内．

???+ note "范围被销毁时，视图内元素均悬垂"
    ```cpp
    #include <iostream>
    #include <ranges>
    #include <vector>
    
    using namespace std;
    
    int main() {
      auto view = [] {
        vector<int> vec{1, 2, 3, 4, 5};
        return vec | std::views::filter([](int i) { return 0 == i % 2; });
      }();
    
      for (int i : view) cout << i << ' ';  // runtime undefined behavior
    
      return 0;
    }
    ```

### Constrained Algorithm 受约束的算法

> C++20 在命名空间 std::ranges 中提供大多数算法的受约束版本，可以用迭代器 - 哨位对或单个 range 作为实参来指定范围，并且支持投影和指向成员指针可调用对象．另外还更改了大多数算法的返回类型，以返回算法执行过程中计算的所有潜在有用信息．

这些算法可以理解成旧标准库算法的改良版本，均为函数对象，提供更友好的重载和入参类型检查（基于 [`concept`](https://zh.cppreference.com/w/cpp/language/constraints)），让我们先以 `std::sort` 和 `ranges::sort` 的对比作为例子

```cpp
#include <algorithm>
#include <iostream>
#include <vector>

using namespace std;

int main() {
  vector<int> vec{4, 2, 5, 3, 1};

  sort(vec.begin(), vec.end());  // {1, 2, 3, 4, 5}

  for (const int i : vec) cout << i << ", ";
  cout << '\n';

  ranges::sort(vec, ranges::greater{});  // {5, 4, 3, 2, 1}

  for (const int i : vec) cout << i << ", ";

  return 0;
}
```

`ranges::sort` 和 `sort` 的算法实现相同，但提供了基于范围的重载，使得传参更为简洁．其他的 `std` 命名空间下的算法，多数也有对应的范围重载版本位于 `ranges` 命名空间中．

使用这些范围入参，再结合使用上节视图，能允许我们在进行复杂操作的同时，保持代码可读性，让我们看一个例子：

```cpp
#include <algorithm>
#include <array>
#include <iostream>
#include <ranges>

using namespace std;

int main() {
  const auto& inputs = views::iota(0u, 9u);  // 生产 0 到 8 的整数序列
  const auto& chunks = inputs | views::chunk(3);  // 将序列分块，每块 3 个元素
  const auto& cartesian_product =
      views::cartesian_product(chunks, chunks);  // 计算对块自身进行笛卡尔积

  for (const auto [l_chunk, r_chunk] : cartesian_product)
    // 计算笛卡尔积下的两个块整数的和
    cout << ranges::fold_left(l_chunk, 0u, plus{}) +
                ranges::fold_left(r_chunk, 0u, plus{})
         << ' ';
}
```

???+ note "输出："
    6 15 24 15 24 33 24 33 42

## 参考

1.  [C++ 参考手册](https://zh.cppreference.com/)


## lang/op-overload.md

重载运算符是通过对运算符的重新定义，使得其支持特定数据类型的运算操作．重载运算符是重载函数的特殊情况．

> 当一个运算符出现在一个表达式中，并且运算符的至少一个操作数具有一个类或枚举的类型时，则使用重载决议（overload resolution）确定应该调用哪个满足相应声明的用户定义函数．[^ref1]

通俗的讲，如果把使用「运算符」看作一个调用特殊的函数（如将 `1+2` 视作调用 `add(1, 2)`），并且这个函数的参数（操作数）至少有一个是 `class`、`struct` 或 `enum` 的类型，编译器就需要根据操作数的类型决定应当调用哪个自定义函数．

在 C++ 中，我们可以重载几乎所有可用的运算符．

???+ note "一些可重载运算符的列举"
    一元运算：`+`（正号）；`-`（负号）；`~`（按位取反）；`++`；`--`；`!`（逻辑非）；`*`（取指针对应值）；`&`（取地址）；`->`（类成员访问运算符）等．
    
    二元运算：`+`；`-`；`&`（按位与）；`[]`（取下标）；`==`；`=`（赋值）等．
    
    其它：`()`（函数调用）；`""`（后缀标识符[^ref1]，C++11 起）；`new`（内存分配）；`,`（逗号运算符）；`<=>`（三路比较[^ref2]，C++20 起）等．

## 限制

重载运算符存在如下限制：

-   只能对现有的运算符进行重载，不能自行定义新的运算符．
-   以下运算符不能被重载：`::`（作用域解析），`.`（成员访问），`.*`（通过成员指针的成员访问），`?:`（三目运算符）．
-   重载后的运算符，其运算优先级，运算操作数，结合方向不得改变．
-   对 `&&`（逻辑与）和 `||`（逻辑或）的重载失去短路求值．

## 实现

重载运算符分为两种情况，重载为成员函数或非成员函数．

当重载为成员函数时，因为隐含一个指向当前成员的 `this` 指针作为参数，此时函数的参数个数与运算操作数相比少一个．

而当重载为非成员函数时，函数的参数个数与运算操作数相同．

其基本格式为（假设需要被重载的运算符为 `@`）：

```cpp
class Example {
  // 成员函数的例子
  返回值 operator@(除本身外的参数) { /* ... */ }
};

// 非成员函数的例子
返回值 operator@(所有参与运算的参数) { /* ... */ }
```

下面将给出几个重载运算符的示例．

### 基本算数运算符

下面定义了一个二维向量结构体 `Vector2D` 并实现了相应的加法和内积的重载．

??? note "重载算数运算符的例子"
    ```cpp
    struct Vector2D {
      double x, y;
    
      Vector2D(double a = 0, double b = 0) : x(a), y(b) {}
    
      Vector2D operator+(Vector2D v) const { return Vector2D(x + v.x, y + v.y); }
    
      // 注意返回值的类型可以不是这个类
      double operator*(Vector2D v) const { return x * v.x + y * v.y; }
    };
    ```

### 自增自减运算符

自增自减运算符分为两类，前置（`++a`）和后置（`a++`）．为了区分前后置运算符，重载后置运算时需要添加一个类型为 `int` 的空置形参．

可以将前置自增理解为调用 `operator++(a)` 或 `a.operator++()`，后置自增理解为调用 `operator++(a, 0)` 或 `a.operator++(0)`．

??? note "分别重载前后置自增运算符的例子"
    ```cpp
    struct MyInt {
      int x;
    
      // 前置，对应 ++a
      MyInt &operator++() {
        x++;
        return *this;
      }
    
      // 后置，对应 a++
      MyInt operator++(int) {
        MyInt tmp;
        tmp.x = x;
        x++;
        return tmp;
      }
    };
    ```

另外一点是，内置的自增自减运算符中，前置的运算符返回的是引用，而后置的运算符返回的是值．虽然重载后的运算符不必遵循这一限制，不过在语义上，仍然期望重载的运算符与内置的运算符在返回值的类型上保持一致．

对于类型 T，典型的重载自增运算符的定义如下：

| 重载定义（以 `++` 为例） | 成员函数                    | 非成员函数                      |
| --------------- | ----------------------- | -------------------------- |
| 前置              | `T& T::operator++();`   | `T& operator++(T& a);`     |
| 后置              | `T T::operator++(int);` | `T operator++(T& a, int);` |

### 函数调用运算符

函数调用运算符 `()` 只能重载为成员函数．通过对一个类重载 `()` 运算符，可以使该类的对象能像函数一样调用．

重载 `()` 运算符的一个常见应用是，将重载了 `()` 运算符的结构体作为自定义比较函数传入优先队列等 STL 容器中．

下面就是一个例子：给出 $n$ 个学生的姓名和分数，按分数降序排序，分数相同者按姓名字典序升序排序，输出排名最靠前的人的姓名和分数．

下面定义了一个比较结构体，实现自定义优先队列的排序方式．

??? note "重载函数调用运算符的例子"
    ```cpp
    struct student {
      string name;
      int score;
    };
    
    struct cmp {
      bool operator()(const student& a, const student& b) const {
        return a.score < b.score || (a.score == b.score && a.name > b.name);
      }
    };
    
    // 注意传入的模板参数为结构体名称而非实例
    priority_queue<student, vector<student>, cmp> pq;
    ```

### 比较运算符

在 `std::sort` 和一些 STL 容器中，需要用到 `<` 运算符．在使用自定义类型时，我们需要手动重载．

下面是一个例子，实现了和上一节相同的功能

??? note "重载比较运算符的例子"
    ```cpp
    struct student {
      string name;
      int score;
    
      // 重载 < 号运算符
      bool operator<(const student& a) const {
        return score < a.score || (score == a.score && name > a.name);
        // 上面省略了 this 指针，完整表达式如下：
        // this->score<a.score||(this->score==a.score&&this->name>a.name);
      }
    };
    
    priority_queue<student> pq;
    ```

上面的代码将小于号重载为了成员函数，当然重载为非成员函数也是可以的．

??? note "重载为非成员函数"
    ```cpp
    struct student {
      string name;
      int score;
    };
    
    bool operator<(const student& a, const student& b) {
      return a.score < b.score || (a.score == b.score && a.name > b.name);
    }
    
    priority_queue<student> pq;
    ```

事实上，只要有了 `<` 运算符，则其他五个比较运算符的重载也可以很容易实现．

```cpp
/* clang-format off */

// 下面的几种实现均将小于号重载为非成员函数

bool operator<(const T& lhs, const T& rhs) { /* 这里重载小于运算符 */ }
bool operator>(const T& lhs, const T& rhs) { return rhs < lhs; }
bool operator<=(const T& lhs, const T& rhs) { return !(lhs > rhs); }
bool operator>=(const T& lhs, const T& rhs) { return !(lhs < rhs); }
bool operator==(const T& lhs, const T& rhs) { return !(lhs < rhs) && !(lhs > rhs); }
bool operator!=(const T& lhs, const T& rhs) { return !(lhs == rhs); }
```

??? note "关于 C++20 下的三路比较运算符"
    如果使用 C++20 或更高版本，我们可以直接使用默认三路比较运算符简化代码．[^ref3]
    
    ```cpp
    auto operator<=>(const T &lhs, const T &rhs) = default;
    ```
    
    默认比较的顺序按照成员变量声明的顺序逐个比较．[^ref4]
    
    也可以使用自定义三路比较．此时要求选择比较内含的序关系（`std::strong_ordering`、`std::weak_ordering` 或 `std::partial_ordering`），或者返回一个对象，使得：
    
    -   若 `a < b`，则 `(a <=> b) < 0`；
    -   若 `a > b`，则 `(a <=> b) > 0`；
    -   若 `a` 和 `b` 相等或等价，则 `(a <=> b) == 0`．
    
    具体实现细节请参考 [比较运算符 #三路比较 - cppreference](https://zh.cppreference.com/w/cpp/language/operator_comparison#Three-way_comparison)．

参考资料与注释：

[^ref1]: [运算符重载 - cppreference](https://zh.cppreference.com/w/cpp/language/operators)

[^ref2]: [用户定义字面量 - cppreference](https://zh.cppreference.com/w/cpp/language/user_literal)

[^ref3]: [比较运算符 #三路比较 - cppreference](https://zh.cppreference.com/w/cpp/language/operator_comparison#.E4.B8.89.E8.B7.AF.E6.AF.94.E8.BE.83)

[^ref4]: [默认比较 - cppreference](https://zh.cppreference.com/w/cpp/language/default_comparisons)


## lang/op.md

author: aofall, greyqz, Ir1d, Link-cute, Marcythm, ouuan, Shen-Linwood, sshwy, StudyingFather

## 算术运算符

| 运算符       | 功能  |
| --------- | --- |
|  `+` （单目） | 正   |
|  `-` （单目） | 负   |
|  `*` （双目） | 乘法  |
|  `/`      | 除法  |
|  `%`      | 取模  |
|  `+` （双目） | 加法  |
|  `-` （双目） | 减法  |

??? note "单目与双目运算符"
    单目运算符（又称一元运算符）指被操作对象只有一个的运算符，而双目运算符（又称二元运算符）的被操作对象有两个．例如 `1 + 2` 中加号就是双目运算符，它有 `1` 和 `2` 两个被操作数．此外 C++ 中还有唯一的一个三目运算符 `?:` ．

算术运算符中有两个单目运算符（正、负）以及五个双目运算符（乘法、除法、取模、加法、减法），其中单目运算符的优先级最高．

其中取模运算符 `%` 意为计算两个整数相除得到的余数，即求余数．

而 `-` 为双目运算符时做减法运算符，如 `2-1` ；为单目运算符时做负值运算符，如 `-1` ．

使用方法如下

 `op=x-y*z` 

得到的 `op` 的运算值遵循数学中加减乘除的优先规律，首先进行优先级高的运算，同优先级按运算的结合性运算，括号提高优先级．

### 算术运算中的类型转换

对于双目算术运算符，当参与运算的两个变量类型相同时，不发生 [类型转换](./var.md#类型转换)，运算结果将会用参与运算的变量的类型容纳，否则会发生类型转换，以使两个变量的类型一致．转换的规则参见 [类型转换](./var.md#类型转换)．

例如，对于一个整型（`int`）变量 $x$ 和另一个双精度浮点型（`double`）类型变量 $y$：

-  `x/3` 的结果将会是整型；
-  `x/3.0` 的结果将会是双精度浮点型；
-  `x/y` 的结果将会是双精度浮点型；
-  `x*1/3` 的结果将会是整型；
-  `x*1.0/3` 的结果将会是双精度浮点型；

## 位操作符

另请参阅：[位运算](../math/bit.md#位运算)．

| 运算符       | 功能   |
| --------- | ---- |
|  `~`      | 逐位非  |
|  `&` （双目） | 逐位与  |
|  `|`      | 逐位或  |
|  `^`      | 逐位异或 |
|  `<<`     | 逐位左移 |
|  `>>`     | 逐位右移 |

位操作的意义请参考 [位操作](../math/bit.md) 页面．需要注意的是，位操作的优先级低于算术运算符（除了取反），而按位与、按位或及异或低于比较运算符（详见 [C++ 运算符优先级总表](#c-运算符优先级总表)），所以使用时需多加注意，在必要时添加括号．

移位运算中如果出现如下情况，则其行为未定义：

1.  右操作数（即移位数）为负值；
2.  右操作数大于等于左操作数的位数；

例如，对于 `int32_t` 类型的变量 `a`，`a<<-1` 和 `a<<32` 都是未定义的．

对于带符号非负数的左移操作，需要确保移位后的结果能被原数的类型容纳，否则行为也是未定义的．[^note1]对一个负数执行左移操作也未定义．[^note2]

对于右移操作，右侧多余的位将会被舍弃，而左侧较为复杂：对于无符号数，会在左侧补 $0$[^note3]；而对于有符号数，则会用最高位的数（其实就是符号位，非负数为 $0$，负数为 $1$）补齐[^note4]．

## 自增/自减 运算符

有时我们需要让变量进行增加 1（自增）或者减少 1（自减），这时自增运算符 `++` 和自减运算符 `--` 就派上用场了．

自增/自减运算符可放在变量前或变量后面，在变量前称为前缀，在变量后称为后缀，单独使用时前缀后缀无需特别区别，如果需要用到表达式的值则需注意，具体可看下面的例子．详细情况可参考 [引用](./reference.md) 介绍的例子部分．

```cpp
i = 100;

op1 = i++;  // op1 = 100，先 op1 = i，然后 i = i + 1

i = 100;

op2 = ++i;  // op2 = 101，先 i = i + 1，然后赋值 op2

i = 100;

op3 = i--;  // op3 = 100，先赋值 op3，然后 i = i - 1

i = 100;

op4 = --i;  // op4 = 99，先 i = i - 1，然后赋值 op4
```

## 复合赋值运算符

复合赋值运算符实际上是表达式的缩写形式．可分为复合算术运算符 `+=`、`-=`、`*=`、`/=`、`%=` 和复合位操作符 `&=`、`|=`、`^=`、`<<=`、`>>=`．

例如，`op = op + 2` 可写为 `op += 2`，`op = op - 2` 可写为 `op -= 2`，`op= op * 2` 可写为 `op *= 2`．

## 条件运算符

条件运算符可以看作 `if` 语句的简写，`a ? b : c` 中如果表达式 `a` 成立，那么这个条件表达式的结果是 `b`，否则条件表达式的结果是 `c`．
## 比较运算符

| 运算符    | 功能   |
| ------ | ---- |
|  `>`   | 大于   |
|  `>=`  | 大于等于 |
|  `<`   | 小于   |
|  `<=`  | 小于等于 |
|  `==`  | 等于   |
|  `!=`  | 不等于  |

其中特别需要注意的是要将等于运算符 `==` 和赋值运算符 `=` 区分开来，这在判断语句中尤为重要．

 `if (op=1)` 与 `if (op==1)` 看起来类似，但实际功能却相差甚远．第一条语句是在对 op 进行赋值，若赋值为非 0 时为真值，表达式的条件始终是满足的，无法达到判断的作用；而第二条语句才是对 `op` 的值进行判断．

## 逻辑运算符

| 运算符    | 功能  |
| ------ | --- |
|  `&&`  | 逻辑与 |
|  `||`  | 逻辑或 |
|  `!`   | 逻辑非 |

```cpp
Result = op1 && op2;  // 当 op1 与 op2 都为真时则 Result 为真

Result = op1 || op2;  // 当 op1 或 op2 其中一个为真时则 Result 为真

Result = !op1;  // 当 op1 为假时则 Result 为真
```

**内建的**运算符 `&&` 和 `||` 进行短路求值（若在求值第一个操作数后结果已知，则不求值第二个），重载的运算符无此特性，并始终对两个操作数都进行求值．

## 逗号运算符

逗号运算符可将多个表达式分隔开来，被分隔开的表达式按从左至右的顺序依次计算，整个表达式的值是最后的表达式的值．逗号表达式的优先级在所有运算符中的优先级是 **最低** 的．

```cpp
exp1, exp2, exp3;  // 最后的值为 exp3 的运算结果．

Result = 1 + 2, 3 + 4, 5 + 6;
//得到 Result 的值为 3 而不是 11，因为赋值运算符 "="
//的优先级比逗号运算符高，先进行了赋值运算才进行逗号运算．

Result = (1 + 2, 3 + 4, 5 + 6);

// 若要让 Result 的值得到逗号运算的结果则应将整个表达式用括号提高优先级，此时
// Result 的值才为 11．
```

## 成员访问运算符

| 运算符       | 功能       |
| --------- | -------- |
|  `[]`     | 数组下标     |
|  `.`      | 对象成员     |
|  `&` （单目） | 取地址/获取引用 |
|  `*` （单目） | 间接寻址/解引用 |
|  `->`     | 指针成员     |

这些运算符用来访问对象的成员或者内存，除了最后一个运算符外上述运算符都可被重载．与 `&` ， `*` 和 `->` 相关的内容请阅读 [指针](./pointer.md) 和 [引用](./reference.md) 教程．这里还省略了两个很少用到的运算符 `.*` 和 `->*` ，其具体用法可以参见 [C++ 语言手册](https://zh.cppreference.com/w/cpp/language/operator_member_access) ．

```cpp
auto result1 = v[1];  // 获取v中下标为2的对象
auto result2 = p.q;   // 获取p对象的q成员
auto result3 = p -> q;  // 获取p指针指向的对象的q成员，等价于 (*p).q
auto result4 = &v;      // 获取指向v的指针
auto result5 = *v;      // 获取v指针指向的对象
```

## C++ 运算符优先级总表

来自 [C++ 运算符优先级 - cppreference](https://zh.cppreference.com/w/cpp/language/operator_precedence) ，有修改．

|          运算符         |    描述    |                              例子                              | 可重载性 |
| :------------------: | :------: | :----------------------------------------------------------: | :--: |
|       **第一级别**       |          |                                                              |      |
|         `::`         |  作用域解析符  |                       `Class::age = 2;`                      | 不可重载 |
|       **第二级别**       |          |                                                              |      |
|         `++`         |  后自增运算符  |           `for (int i = 0; i < 10; i++) cout << i;`          |  可重载 |
|         `--`         |  后自减运算符  |           `for (int i = 10; i > 0; i--) cout << i;`          |  可重载 |
|   `type()  type{}`   |  强制类型转换  |           `unsigned int a = unsigned(3.14);`                | 可重载 |
|         `()`         |   函数调用   |                        `isdigit('1')`                        |  可重载 |
|         `[]`         |  数组数据获取  |                        `array[4] = 2;`                       |  可重载 |
|          `.`         |  对象型成员调用 |                        `obj.age = 34;`                       | 不可重载 |
|         `->`         |  指针型成员调用 |                       `ptr->age = 34;`                       |  可重载 |
|   **第三级别** （从右向左结合）  |          |                                                              |      |
|         `++`         |  前自增运算符  |             `for (i = 0; i < 10; ++i) cout << i;`            |  可重载 |
|         `--`         |  前自减运算符  |             `for (i = 10; i > 0; --i) cout << i;`            |  可重载 |
|          `+`         |    正号    |                         `int i = +1;`                        |  可重载 |
|          `-`         |    负号    |                         `int i = -1;`                        |  可重载 |
|          `!`         |   逻辑取反   |                        `if (!done) …`                       |  可重载 |
|          `~`         |   按位取反   |                       `flags = ~flags;`                      |  可重载 |
|       `(type)`       |  C 风格强制类型转换  |                 `int i = (int) floatNum;`             |  可重载 |
|          `*`         |   指针取值   |                     `int data = *intPtr;`                    |  可重载 |
|          `&`         |   值取指针   |                    `int *intPtr = &data;`                    |  可重载 |
|       `sizeof`       |  返回类型内存  |    `int size = sizeof floatNum; int size = sizeof(float);`   | 不可重载 |
|         `new`        | 动态元素内存分配 |  `long *pVar = new long; MyClass *ptr = new MyClass(args);`  |  可重载 |
|       `new []`       | 动态数组内存分配 |                 `long *array = new long[n];`                 |  可重载 |
|       `delete`       | 动态析构元素内存 |                        `delete pVar;`                        |  可重载 |
|      `delete []`     | 动态析构数组内存 |                      `delete [] array;`                      |  可重载 |
|       **第四级别**    |          |                                                              |      |
|         `.*`         |  类对象成员引用 |                       `obj.*var = 24;`                       | 不可重载 |
|         `->*`        |  类指针成员引用 |                       `ptr->*var = 24;`                      |  可重载 |
|       **第五级别**    |          |                                                              |      |
|          `*`         |    乘法    |                       `int i = 2 * 4;`                       |  可重载 |
|          `/`         |    除法    |                    `float f = 10.0 / 3.0;`                   |  可重载 |
|          `%`         | 取余数（模运算） |                      `int rem = 4 % 3;`                      |  可重载 |
|       **第六级别**    |          |                                                              |      |
|          `+`         |    加法    |                       `int i = 2 + 3;`                       |  可重载 |
|          `-`         |    减法    |                       `int i = 5 - 1;`                       |  可重载 |
|       **第七级别**    |          |                                                              |      |
|         `<<`         |    位左移   |                    `int flags = 33 << 1;`                    |  可重载 |
|         `>>`         |    位右移   |                    `int flags = 33 >> 1;`                    |  可重载 |
|       **第八级别**     |          |                                                              |      |
|         `<=>`         | 三路比较运算符  |                `if ((i <=> 42) < 0) ...`                      |  可重载 |
|       **第九级别**     |          |                                                              |      |
|          `<`         |    小于    |                      `if (i < 42) ...`                      |  可重载 |
|         `<=`         |   小于等于   |                      `if (i <= 42) ...`                     |  可重载 |
|          `>`         |    大于    |                      `if (i > 42) ...`                      |  可重载 |
|         `>=`         |   大于等于   |                      `if (i >= 42) ...`                     |  可重载 |
|       **第十级别**       |          |                                                              |      |
|         `==`         |    等于    |                      `if (i == 42) ...`                     |  可重载 |
|         `!=`         |    不等于   |                      `if (i != 42) ...`                     |  可重载 |
|       **第十一级别**      |          |                                                              |      |
|          `&`         |   位与运算   |                     `flags = flags & 42;`                    |  可重载 |
|       **第十二级别**      |          |                                                              |      |
|          `^`         |   位异或运算  |                     `flags = flags ^ 42;`                    |  可重载 |
|       **第十三级别**      |          |                                                              |      |
|          `|`         |   位或运算   |                     `flags = flags | 42;`                    |  可重载 |
|       **第十四级别**      |          |                                                              |      |
|         `&&`         |   逻辑与运算  |              `if (conditionA && conditionB) ...`             |  可重载 |
|   **第十五级别**         |          |                                                              |      |
|         `||`         |   逻辑或运算  |              `if (conditionA || conditionB) ...`             |  可重载 |
|   **第十六级别** （从右向左结合） |          |                                                              |      |
|         `? :`        |   条件运算符  |                   `int i = a > b ? a : b;`                   | 不可重载 |
|        `throw`       |   异常抛出   |                  `throw EClass("Message");`                  | 不可重载 |
|          `=`         |    赋值    |                         `int a = b;`                         |  可重载 |
|         `+=`         |   加赋值运算  |                           `a += 3;`                          |  可重载 |
|         `-=`         |   减赋值运算  |                           `b -= 4;`                          |  可重载 |
|         `*=`         |   乘赋值运算  |                           `a *= 5;`                          |  可重载 |
|         `/=`         |   除赋值运算  |                           `a /= 2;`                          |  可重载 |
|         `%=`         |   模赋值运算  |                           `a %= 3;`                          |  可重载 |
|         `<<=`        |  位左移赋值运算 |                        `flags <<= 2;`                        |  可重载 |
|         `>>=`        |  位右移赋值运算 |                        `flags >>= 2;`                        |  可重载 |
|         `&=`         |  位与赋值运算  |                     `flags &= new_flags;`                    |  可重载 |
|         `^=`         |  位异或赋值运算 |                     `flags ^= new_flags;`                    |  可重载 |
|         `|=`         |  位或赋值运算  |                     `flags |= new_flags;`                    |  可重载 |
|       **第十七级别**      |          |                                                              |      |
|          `,`         |   逗号分隔符  |          `for (i = 0, j = 0; i < 10; i++, j++) ...`          |  可重载 |

需要注意的是，表中并未列出 `const_cast`、`static_cast`、`dynamic_cast`、`reinterpret_cast`、`typeid`、`sizeof...`、`noexcept` 及 `alignof` 等运算符，因为它们的使用形式与函数调用相同，不会出现歧义．

## 参考资料与注释

[^note1]: C++20 前，若原值为带符号类型，且移位后的结果能被原类型的无符号版本容纳，则将该结果 [转换](../lang/var.md#类型转换) 为相应的带符号值，否则行为未定义；无符号数的左移则舍弃移出结果类型的位．C++20 起，规定 `a << b` 为 $a\cdot 2^b$ 在模 $2^N$ 下的值（$N$ 为结果类型的位宽），即无论是带符号数还是无符号数，左移均直接舍弃移出结果类型的位（即 [算术左移/逻辑左移](../math/bit.md#移位)）．

[^note2]: C++20 前．C++20 起的行为参见[^note1]．

[^note3]: 即 [逻辑右移](../math/bit.md#移位)．

[^note4]: 即 [算术右移](../math/bit.md#移位)．C++20 前，带符号的右移是依实现定义的，在大多数实现中，均采用算术右移．C++20 起，规定 `a >> b` 为 $\lfloor a/2^b\rfloor$，所以带符号数右移运算是算术右移．


## lang/optimizations.md

author: inclyc

OI 界的常用编程语言是 C++．既然使用了这门语言，就注定要和编译器、语言标准打交道了．众所周知，C++ 非常混乱邪恶，本文旨在给出实用的编译器相关知识，足够竞赛使用．

## 编译器优化简介

### 什么是优化 (Optimization)

根据 [如同规则](https://en.cppreference.com/w/cpp/language/as_if)（The as-if Rule），在保持语义不变的情况下，对程序运行速度、程序可执行文件大小作出改进．

<!-- ### 开优化的比赛有哪些？ -->

<!-- TODO: 开 O2 的比赛 -->

## 常见的编译器优化

### 常量折叠 (Constant Folding)

常量折叠，又称常量传播 (Constant Propagation)，如果一个表达式可以确定为常量，在他的下一个定义 (Definition) 前，可以进行常量传播．

```cpp
int x = 1;
int y = x;  // x = 1, => y = 1
x = 3;
int z = 2 * y;   // z => 2 * y = 2 * 1 = 2
int y2 = x * 2;  // x = 3, => y2 = 6
```

这段代码在编译期间即可被转换为：

```cpp
int x = 1;
int y = 1;
x = 3;
int z = 2;
int y2 = 6;
```

实例：<https://godbolt.org/z/oEfY35TTd>

### 死代码消除 (Deadcode Elimination)

故名思义，就是一段代码没用上就会被删去．

```cpp
int test() {
  int a = 233;
  int b = a * 2;
  int c = 234;
  return c;
}
```

将被转换为

```cpp
int test() { return 234; }
```

注意，这个代码首先进行了常量折叠，使得返回值可以确定为 234，a, b 为不活跃变量，因此删除．

### 循环旋转 (Loop Rotate)

将循环从 "for" 形式，转换为 "do-while" 形式，前面再多加一个条件判断．这个变换主要为其他变换做准备．

```cpp
for (int i = 0; i < n; ++i) {
  auto v = *p;
  use(v);
}
```

变换为

```cpp
if (0 < n) {
  do {
    auto v = *p;
    use(v);
    ++i;
  } while (i < n);
}
```

### 循环不变量外提 (Loop Invariant Code Motion)

基于别名分析 (Alias Analysis)，将循环中被证明是不变量（可能包含内存访问，load/store，因此依赖别名分析）的代码外提出循环体，这样可以让循环体内部少一些代码．

```cpp
for (int i = 0; i < n; ++i) {
  auto v = *p;
  use(v);
}
```

这个代码直观来看可以外提为：

```cpp
auto v = *p;
for (int i = 0; i < n; ++i) {
  use(v);
}
```

但实际上，如果 `n <= 0`，这个循环永远不会被进入，但我们又执行了一条多的指令（可能有副作用！）．因此，循环通常被 Rotate 为 do-while 形式，这样可以方便插入一个 "loop guard"．之后再进行循环不变量外提．

```cpp
if (0 < n) {  // loop guard
  auto v = *p;
  do {
    use(v);
    ++i;
  } while (i < n);
}
```

### 循环展开 (Loop Unroll)

循环包含循环体和各类分支语句，需要现代 CPU 进行一定的分支预测．直接把循环展开，用一定的代码大小来换取运行时间．

```cpp
for (int i = 0; i < 3; i++) {
  a[i] = i;
}
```

变换为：

```cpp
a[0] = 0;
a[1] = 1;
a[2] = 2;
```

### 循环判断外提 (Loop Unswitching)

循环判断外提将循环中的条件式移到循环之外，然后在外部的两个条件各放置两个循环，这样可以增加循环向量化、并行化的可能性（通常简单循环更容易被向量化）．

```cpp
// clang-format off
void before(int x) {
  for(;/* i in some range */;) {
    /* A */;
    if (/* condition */ x % 2) {
      /* B */;
    }
    /* C */;
  }
}

void after(int x) {
  if (/* condition */ x % 2) {
    for(;/* i in some range */;) {
      /* A */;
      /* B */; // 直接执行 B ，不进行循环判断
      /* C */;
    }
  } else {
     for(;/* i in some range */;) {
      /* A */; 
               // 不执行 B
      /* C */;
    }
  }
}
```

### 代码布局优化 (Code Layout Optimizations)

程序在执行时，可以将执行的路径分为冷热路径 (cold/hot path)．CPU 跳转执行，绝大多数情况下没有直接顺序执行快，后者通常被编译器作者称为 "fallthrough"．与之对应的，经常被执行到的代码成为热代码，与之相对的成为冷代码．OI 代码中，如果有一段是循环中的特判边界条件，或者异常处理，类似的逻辑，则此部分代码为冷代码．

基本块 (Basic Block)，是控制流的基本结构，一个过程 (Procedure) 由若干个基本块组成，形成一个有向图．生成可执行文件的过程中，编译器需要安排一个放置基本块的布局 (Layout)，而如何编排布局，是此优化的重点．

原则上，应该更偏好与将热代码放在一起，而将冷代码隔开．原因是这样能够更好地利用指令缓存，热代码的局部性会更好．

```cpp
// clang-format off
int hotpath; // <-- 热！
if (/* 边界条件 */ false) {
    // <-- 冷！
}
int hotpath_again;  // <-- 热！
```

#### 基本块放置 (Basic Block Placement)

我们用 label 来表达一种「伪机器码」，这个 C++ 程序有两种翻译方法：

???+ note "布局 1"
    ```cpp
    // clang-format off
    hotblock1:
        Stmts; // <-- 热！
        if (/* 边界条件不成立 */ true)
            goto hotblock2; // 经常发生！ ------+
    coldblock:                           /*   |   */
        Stmt; // <- 冷                        |
        Stmt; // <- 冷                        |
        Stmt; // <- 冷                        |  跨越了大量指令，代价高昂！
        Stmt; // <- 冷                        |
        Stmt; // <- 冷                        |
        Stmt; // <- 冷                        |
        Stmt; // <- 冷                        |
    hotblock2:                          /*    |   */
        Stmts; // <- 热！           <----------+
    ```

另一种布局为：

???+ note "布局 2"
    ```cpp
    // clang-format off
    hotblock1:
        Stmts; // <-- 热！
        if (/* 边界条件 */ false)
            goto coldblock; // 很少发生
    hotblock2:                         /*   |  低代价！  */
        Stmts; // <- 热！  <-----------------+
    coldblock:
        Stmt; // <- 冷
        Stmt; // <- 冷
        Stmt; // <- 冷
        Stmt; // <- 冷
        Stmt; // <- 冷
    ```

我们看到后一种布局中，两个热代码块被放到了一起，执行效率更优秀．

为了告诉编译器分支是否容易被执行，可以使用 C++20 `[[likely]]` 和 `[[unlikely]]`:<https://en.cppreference.com/w/cpp/language/attributes/likely>

如果比赛没有采用 C++20 以上标准，则可以利用 `__builtin_expect`(GNU Extension)．

```cpp
#define likely(x) __builtin_expect(!!(x), 1)
#define unlikely(x) __builtin_expect(!!(x), 0)

if (unlikely(/* 一些边界条件检查 */ false)) {
  // 冷代码
}
```

#### 冷热代码分离 (Hot Cold Splitting)

一个过程 (Procedure) 包含同时包含冷热路径，而冷代码较长，更好的做法是让冷代码作为函数调用，而不是阻断热路径．这同时也提示我们不要自作聪明的让所有函数 `inline`．冷代码对执行速度的阻碍比函数调用要多得多．

???+ note "不好的代码布局"
    ```cpp
    // clang-format off
    void foo() {
          // clang-format off
    hotblock1:
        Stmts; // <-- 热！
        if (/* 边界条件不成立 */ true)
            goto hotblock2; // 经常发生！ ------+
    coldblock:                           /*   |   */
        Stmt; // <- 冷                        |
        Stmt; // <- 冷                        |
        Stmt; // <- 冷                        |  跨越了大量指令，代价高昂！
        Stmt; // <- 冷                        |
        Stmt; // <- 冷                        |
        Stmt; // <- 冷                        |
        Stmt; // <- 冷                        |
    hotblock2:                          /*    |   */
        Stmts; // <- 热！           <----------+
    }
    ```

???+ note "好的代码布局"
    ```cpp
    // clang-format off
    void foo() {
    hotblock1:
      Stmts;  // <-- 热！
      if (/* 边界条件 */ false)
        coldBlock();  // 将冷代码分离出，使得热路径对 cache 更友好
    hotblock2:
      Stmts;  // <- 热！
    }
    
    void coldBlock() {
      Stmt;  // <- 冷
      Stmt;  // <- 冷
      Stmt;  // <- 冷
      Stmt;  // <- 冷
      Stmt;  // <- 冷
      Stmt;  // <- 冷
      Stmt;  // <- 冷
    }
    ```

冷热代码分离，其实就是函数内联 (Function Inlining) 的反向操作，这一优化的存在启示我们，函数内联不一定会让程序跑的更快．甚至如果内联代码是冷代码，反而会让程序跑的更慢！一些编译器存在强制内联的编译选项，但不推荐使用．编译器内部有一个静态分析过程，计算每个基本块、分支的概率，以及一个函数调用相关的代价模型，以此决定是否内联，自己决定是否内联不一定比编译器的决策好．

事实上，在没有额外信息的情况下，编译器通常会假设分支跳转与不跳转的概率一致，以此为依据传播各个控制流路径的冷热程度．PGO (Profile Guided Optimization) 的一部分便是通过若干次性能测试与实验得出真正环境下的程序分支概率，这些信息可以让代码布局更加优秀．

### 函数内联 (Function Inlining)

函数调用通常需要寄存器和栈传递参数，调用者 (caller) 和被调用者 (callee) 都需要保存一定的寄存器状态，这个过程通常被叫做调用约定 (calling convention)．一个函数调用因此会引起一些时间损耗，而内联函数就是指将函数直接写在调用方过程中，不进行真正的函数调用．

```cpp
int add(int x) { return x + 1; }

int foo() {
  int a = 1;
  a = add(a);
}
```

`add()` 可以被内联到 `foo()` 当中：

```cpp
int foo() {
  int a = 1;
  a = a + 1;  // <-- add() 的函数体，未经过传参
}
```

#### `always_inline`,`__force_inline`

<https://clang.llvm.org/docs/AttributeReference.html#always-inline-force-inline>

一些编译器提供了手动内联函数调用的方法，在函数前加 `__attribute__((always_inline))`．这样使用不一定会比函数调用快，编译器在这个时候相信程序员有足够好的判断能力．

### 尾调用优化 (Tail Call Optimization)

当一个函数调用位于函数体尾部的位置时，这种函数调用被成为尾调用 (Tail Call)．对于这种特殊形式的调用，可以进行一些特别的优化．绝大多数体系结构拥有 Frame Pointer (a.k.a FP) 和 Stack Pointer (a.k.a SP)，维护者函数的调用帧 (Frame)，而如果调用位于函数尾部，则我们可以不保留外层函数的调用记录，直接用内层函数取代．

#### 用跳转指令代替函数调用

函数调用在绝大多数体系结构下，需要保存当前程序计数器 `$pc` 的位置，保存若干 caller saved register，以便回到现场．而尾调用不需要此过程，将被直接翻译为跳转指令，因为尾递归永远不会返回到函数运行的位置．

一个简单的例子：<https://godbolt.org/z/e7b1safaW>

```cpp
int test(int a);

int tailCall(int x) { return test(x); }
```

```nasm
tailCall(int):                           ; @tailCall(int)
        jmp     test(int)@PLT                    ; TAILCALL
```

#### 自动尾递归改写

如果一个函数的尾调用是自身，则此函数是尾递归的．广义来讲，间接递归（由两个函数 以上共同形成递归）形成递归，且都是尾调用的，也属于尾递归的范畴．尾递归可以被编译器优化为非递归的形式，减小额外的栈开销和函数调用代价．许多算法竞赛选手热衷于写非递归的代码，在不开优化下这样可以极大优化代码的常数，然而如果开优化，递归代码生成的二进制质量和手写的代码没有什么区别．

```cpp
int fac(int n) {
  if (n < 2) return 1;
  return /* 使用 */ n * fac(n - 1); /* 使用了变量 n ，无法直接做尾递归优化！*/
}
```

注意到这个函数并不是尾递归的，但可以改写为：

```cpp
int fac(int acc, int n) {
  if (n < 2) return acc;
  return fac(acc * n, n - 1);
}
```

新的代码即是尾递归的．

现代编译器可以自动帮你完成这个过程，如果你的代码有机会被改写为尾递归，则编译器可以识别出这种形式，然后完成改写．

#### 尾递归消除 -Rpass=tailcallelim

既然函数已经尾递归，那就可以直接删除递归语句，通过一定的静态分析，将函数直接转换为非递归的形式．我们此处并不去深究编译器作者如何做到这一点，从实际体验来看，绝大多数 OI 代码，如果存在递归版本和非递归版本，则此代码一般可自动优化为非递归版本．这里给读者一些具体的例子：

???+ note "[GCD](https://godbolt.org/z/8Wb6WEnzv)"
    ```cpp
    int gcd(int a, int b) { return b ? gcd(b, a % b) : a; }
    ```

???+ note "[斐波那契数列](https://godbolt.org/z/4enof6Wcb)"
    ```cpp
    // 展开 fib(n - 2) 这一项
    // fib(n - 1) 不能变换为非递归，优化后的代码依然是指数级别的
    int fib(int n) {
      if (n < 2) return 1;
      return fib(n - 1) + fib(n - 2);
    }
    ```

???+ note "[阶乘](https://godbolt.org/z/n64e75xrf)"
    ```cpp
    // 展开成标量循环，然后执行自动向量化，生成的代码是 SIMD 的
    unsigned fac(unsigned n) {
      if (n < 2) return 1;
      return n * fac(n - 1);
    }
    ```

这些函数被优化后的汇编和非递归版完全相同，递归将被直接消除．对于 OI 选手而言，可以在开 O2 的情况下放心写递归版本的各种算法，和非递归版不会有什么区别．如果你写的函数本身无法被改写成非递归的形式，那么编译器也无能为力．

### 强度削减 (Strength Reduction)

常见的编译优化．最简单的例子是 `x * 2` 变为 `x << 1`，第二种写法在 OI 中相当常见．编译器会自动做类似的优化，在打开优化开关的情况下，`x * 2` 和 `x << 1` 是完全等价的．强度削减 (Strength Reduction) 将高开销的指令转换为低开销的指令．

#### 标量运算符变换

##### 移位代替乘法

```cpp
int a;
a = x * 2;   // bad!
a = x << 1;  // good!
```

需要注意的是有符号数和无符号数在移位 (shifting) 和类型提升 (promotion) 层面有明显的差异．符号位在移位时有着特别的处理，包括算术移位和逻辑移位两种类型．这在编写二分查找/线段树等含有大量除二操作的时候表现突出，有符号整数除法不能直接优化为一步右移位运算．

```cpp
int l, r;
/* codes */
int mid = (l + r) / 2; /* 如果编译器不能假定 l, r 非负，则会生成较差的代码 */
                       // 不能优化为
                       // mid = (l + r) >> 1
                       // 反例：
                       // mid = -127
                       // mid / 2 = -63
                       // mid >> 1 = -64
```

```cpp
int mid = (l + r);
int sign = mid >> 31; /* 逻辑右移, 得到符号位 */
mid += sign;
mid >>= 1; /* 算术右移 */
```

可行的解决方案：

-   用 `unsigned l, r;`，下标本来就应该是无符号的
-   在源代码中使用移位

##### 乘法代替除法

```cpp
int x = a / 3;
```

此过程可以被变换为 `x = a * 0x55555556 >> 32`，具体可以看 [这篇知乎回答](https://zhuanlan.zhihu.com/p/151038723) 或者 [原始论文](https://dl.acm.org/doi/10.1145/773473.178249)．

#### 索引变量强度削减 (IndVars)

编译器自动识别出循环中的索引变量，并将相关的高开销过程转换为低开销

```cpp
int a = 0;
for (int i = 1; i < 10; i++) {
  a = 3 * i;  // bad!
  a = a + 3;  // good!
}
```

此处如果直接使用 `a = 3 * i` 在 OI 中很常见，而编译器可以自动分析出，等价的变换为 `a = a + 3`，用代价更低的加法代替乘法．分析循环变量的迭代过程，被称为 SCEV (Scalar Evolution)．

SCEV 还可以做到优化一些循环：

```cpp
int test(int n) {
  int ans = 1;
  for (int i = 0; i < n; i++) {
    ans += i * (i + 1);
  }
  return ans;
}
```

此函数会被优化为 $O(1)$ 公式求和，参考 <https://godbolt.org/z/ET8d89vvK>．这个行为目前仅有基于 LLVM 的编译器会出现，GCC 编译器更加保守．

```nasm
test(int):                               # @test(int)
        test    edi, edi
        jle     .LBB0_1
        lea     eax, [rdi - 1]
        lea     ecx, [rdi - 2]
        imul    rcx, rax
        lea     eax, [rdi - 3]
        imul    rax, rcx
        shr     rax
        imul    eax, eax, 1431655766
        and     ecx, -2
        lea     eax, [rax + 2*rcx]
        lea     eax, [rax + 2*rdi]
        dec     eax
        ret
.LBB0_1:
        mov     eax, 1
        ret
```

### 自动向量化 (Auto-Vectorization)

单指令流多数据流是很好的提供单核并行的方法．使用这种指令，可以利用 CPU 的 SIMD 寄存器，比通用寄存器更宽，例如一次放 4 个整数然后计算．OI 选手不需要了解自动向量化的细节，通常而言，Clang 编译器会做比 GCC 更激进的自动向量化：

```cpp
// https://godbolt.org/z/h1hx5sWoE
void test(int *a, int *b, int n) {
  for (int i = 0; i < n; i++) {
    a[i] += b[i];
  }
}
```

#### `__restrict` type specifier (GNU, MSVC)

两个任意指针对应的区域可能出现重叠 (overlap)，此时需要特判是否可以使用向量代码．下图展示了一个指针重叠的例子：

![](./images/overlap.png)

`__restrict` 作为一种约定使编译器假定两个指针所指向的内存区域永远不会重叠．

```cpp
void test(int* __restrict a, int* __restrict b, int n) {
  for (int i = 0; i < n; i++) {
    a[i] += b[i];
  }
}
```

`__restrict` 并非 C++ 标准的一部分，但各大编译器都可以使用．此关键字影响自动向量化的代码生成质量，极端卡常的情况下可以使用．

## 和编译优化相关的常见语言误用

### inline - 内联

函数内联在开 O2 的情况下通常由编译器自动完成．结构体定义中的 `inline` 完全是多余的，如果准备的比赛开 O2 优化，则完全不必声明为内联．如果不开 O2 则使用 `inline` 也不会让编译器真正内联．

`inline` 关键字在现代 C++ 被当作是一种链接、与导出符号的语义行为，而不是做函数内联．

### register - 虚假的寄存器建议

现代编译器会直接忽略你的 `register` 关键字，你自己认为的寄存器分配一般没有编译器直接跑寄存器分配算法来的聪明．此关键字于 C++11 被弃用，于 C++17 被删除[^p0001r1]．

<https://en.cppreference.com/w/cpp/keyword/register>

## 未定义行为（Undefined Behavior）与编译优化

编译器可以认为 C++ 程序不存在 [未定义行为](https://en.cppreference.com/w/cpp/language/ub)（undefined behavior，UB），因此在编译存在 UB 的程序时，编译器可能会产生意想不到的结果．同时，编译器也可以在假定不存在 UB 的情况下进行更加激进而自由的优化．

常见的 UB 有：

1.  [有符号溢出](https://users.cs.utah.edu/~regehr/papers/overflow12.pdf)；
2.  使用未初始化的变量；
3.  访问越界；
4.  空指针解引用；
5.  无副作用的无限循环．

其他 UB 和示例等可通过扩展阅读详细了解．

### 有符号溢出

```cpp
int f(int x) { return x * 2 / 2; }
```

编译器可以假定程序不存在有符号溢出的行为，进而此函数可能被优化为

```cpp
int f(int x) { return x; }
```

示例：<https://godbolt.org/z/WKv3W5hvM>、<https://godbolt.org/z/qqE9nxP1j>．

可通过 [`-fwrapv`](https://gcc.gnu.org/onlinedocs/gcc-13.2.0/gcc/Code-Gen-Options.html#index-fwrapv) 选项禁用该假设．示例：<https://godbolt.org/z/5x3K5KGnr>、<https://godbolt.org/z/4r4a4EzMW>．

### 使用未初始化的变量

```cpp
int f(int x) {
  int a;
  if (x)  // either x nonzero or UB
    a = 42;
  return a;
}
```

编译器可以假定程序不存在使用未初始化变量的行为，所以 `a` 一定会被初始化，进而此函数可能被优化为

```cpp
int f(int) { return 42; }
```

示例：<https://godbolt.org/z/8WYMYYjdG>、<https://godbolt.org/z/qvGd1nvv9>．

### 访问越界

```cpp
int table[4] = {};

bool exists_in_table(int v) {
  // return true in one of the first 4 iterations or UB due to out-of-bounds
  // access
  for (int i = 0; i <= 4; i++)
    if (table[i] == v) return true;
  return false;
}
```

编译器可以假定程序不存在访问越界的行为，所以该函数一定会在发生访问越界之前返回，进而此函数可能被优化为

```cpp
bool exists_in_table(int) { return true; }
```

示例：<https://godbolt.org/z/xfePeYsE3>．

### 空指针解引用

```cpp
int f(int* p) {
  int x = *p;
  if (!p)
    return x;  // Either UB above or this branch is never taken
  else
    return 0;
}
```

编译器可以假定程序不存在空指针解引用的行为，从而 `!p` 恒为 `false`，进而此函数可能被优化为

```cpp
int f(int*) { return 0; }
```

示例：<https://godbolt.org/z/GY1jvsrb5>、<https://godbolt.org/z/4ronPsnxf>．

### 无副作用的无限循环

???+ note "验证 Fermat 大定理"
    由 [Fermat 大定理](https://en.wikipedia.org/wiki/Fermat%27s_Last_Theorem) 可知，不定方程 $a^3=b^3+c^3$ 没有正整数解．下面的程序试图枚举 $[1,1000]$ 内的整数验证该方程是否成立，若返回 `true` 则说明在 $[1,1000]$ 范围内找到了一组整数解，从而 Fermat 大定理不成立．
    
    ```cpp
    #include <iostream>
    
    bool fermat() {
      const int max_value = 1000;
    
      // Endless loop with no side effects is UB
      for (int a = 1, b = 1, c = 1; true;) {
        if (((a * a * a) == ((b * b * b) + (c * c * c))))
          return true;  // disproved :()
        a++;
        if (a > max_value) {
          a = 1;
          b++;
        }
        if (b > max_value) {
          b = 1;
          c++;
        }
        if (c > max_value) c = 1;
      }
    
      return false;  // not disproved
    }
    
    int main() {
      std::cout << "Fermat's Last Theorem ";
      fermat() ? std::cout << "has been disproved!\n"
               : std::cout << "has not been disproved.\n";
    }
    ```

编译器可以假定程序不存在无副作用的无限循环，从而认为 `fermat()` 函数中的 for 循环一定会在某一时刻终止并返回 `true`，最终程序可能输出：

```text
Fermat's Last Theorem has been disproved!
```

示例：<https://godbolt.org/z/d834MK7bz>、<https://godbolt.org/z/Eov9nsKqf>．

## Sanitizer

理智保证器．在运行时检查你的程序是否有未定义行为、数组越界、空指针，等等功能．
在本地调试模式下，建议开启一些 sanitizer，可以极大缩短你的 Debug 时间．这些 sanitizer 由 Google 开发，绝大多数可以在 GCC 和 Clang 中使用．sanitizer 在 LLVM 中更加成熟，因此推荐选手本地使用 Clang 编译器进行相关除错．

### Address Sanitizer -fsanitize=address

<https://clang.llvm.org/docs/AddressSanitizer.html>

GCC 和 Clang 都支持这个 Sanitizer．包括如下检查项：

-   越界
-   释放后使用 (use-after-free)
-   返回后使用 (use-after-return)
-   重复释放 (double-free)
-   内存泄漏 (memory-leaks)
-   离开作用域后使用  (use-after-scope)

应用这项检查会让你的程序慢 2x 左右．

### Undefined Behavior Sanitizer -fsanitize=undefined

<https://clang.llvm.org/docs/UndefinedBehaviorSanitizer.html>

Undefined Behavior Sanitizer (a.k.a UBSan) 用于检查代码中的未定义行为．GCC 和 Clang 都支持这个 Sanitizer．自动检查你的程序有无未定义行为．UBSan 的检查项目包括：

-   移位溢出，例如 32 位整数左移 72 位
-   有符号整数溢出
-   浮点数转换到整数数据溢出

UBSan 的检查项可选，对程序的影响参考提供的网页地址．

## 杂项

### Compiler Explorer

在这里观察各个编译器的行为和汇编代码：<https://godbolt.org>

## 扩展阅读

1.  [The LLVM Project Blog: What Every C Programmer Should Know About Undefined Behavior #1/3](https://blog.llvm.org/2011/05/what-every-c-programmer-should-know.html)
2.  [The LLVM Project Blog: What Every C Programmer Should Know About Undefined Behavior #2/3](https://blog.llvm.org/2011/05/what-every-c-programmer-should-know_14.html)
3.  [The LLVM Project Blog: What Every C Programmer Should Know About Undefined Behavior #3/3](https://blog.llvm.org/2011/05/what-every-c-programmer-should-know_21.html)

## 参考资料与注释

[^p0001r1]: [Remove Deprecated Use of the register Keyword (open-std.org)](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2015/p0001r1.html)


## lang/pas-cpp.md

author: kexplorning, Ir1d, lvneg1

## C++ 快速安装与环境配置

以下过程均在 Windows 系统中操作．

### 使用 IDE

可以参考如下页面中内容：

-   [Dev-C++](../tools/editor/devcpp.md)
-   [Code::Blocks](../tools/editor/codeblocks.md)

### 使用 代码编辑器 + 编译器 + 调试器

可以参考 [VS Code](../tools/editor/vscode.md) 页面中内容．Visual Studio Code 官方网站上有文档解释如何进行 C++ 的配置．一般而言 VS Code 搭配插件使用更方便，见 [VS Code 的官方网站](https://code.visualstudio.com/)．

## C++ 语法快速提要

C++ 程序都是从 `main` 这个部分开始运行的．

大括号表示块语句的开始与结束：`{` 就相当于 Pascal 里面的 `begin`，而 `}` 就相当于 `end`．

注意，和 Pascal 一样，C++ 每句话结束要加分号 `;`，不过大括号结尾不需要有分号，而且程序结束末尾不用打句号 `.`．

对于注释，`//` 表示行内注释，`/* */` 表示块注释．

按照惯例，看看 Hello World 吧．

### Hello World：第一个 C++ 程序

```cpp
#include <iostream>  // 导入 iostream 库

int main()  // main 部分
{
  std::cout << "Hello World!" << std::endl;

  return 0;
}
```

然后编译运行一下，看看结果．

#### 简要解释

第一行，`#include <iostream>` 的意思是，导入 `iostream` 这个库．

??? note "Pascal 的库文件"
    Pascal 其实是有库文件的，只不过，很多同学从来都没有用过……

看到第三行的 `main` 吗？程序从 `main` 开始执行．

接下来最重要的一句话是

```cpp
std::cout << "Hello World!" << std::endl;
```

`std::cout` 是输出命令．你可能看过有些 C++ 程序中直接写的是 `cout`．

??? note "有关 std:: 前缀"
    有关 `std::` 这个前缀的问题，请见 [这节](basic.md#cin-与-cout) 底下的注释「什么是 std？」．

中间的 `<<` 很形象地表示流动，其实它就是表示输出怎么「流动」的．这句代码的意思就是，`"Hello World!"` 会先被推到输出流，之后 `std::endl` 再被推到输出流．

而 `std::endl` 是 **输出** 换行命令，这与 Pascal 的 `writeln` 类似，不过 C++ 里面可没有 `coutln`．Pascal 与 C++ 的区别在于，`write('Hello World!')` 等价于 `std::cout << "Hello World!"`，而 `writeln('Hello World!')` 等价于 `std::cout << "Hello World!" << std::endl`．

此处 `"Hello World!"` 是字符串，Pascal 中字符串都是用单引号 `'` 不能用双引号，而 C++ 的字符串必须用双引号．C++ 中单引号包围的字符会有别的含义，后面会再提及的．

好了，到这里 Hello World 应该解释的差不多了．

可能有同学会问，后面那个 `return 0` 是什么意思？那个 `int main()` 是啥意思？**先别管它**，一开始写程序的时候先把它当作模板来写吧（这里也是用模板写的）．因为入门时并不会用到 `main` 中参数，所以不需要写成 `int main(int argc, char const *argv[])`．

#### 简单练习

1.  试着换个字符串输出．
2.  试着了解转义字符．

### A+B Problem：第二个 C++ 程序

经典的 A+B Problem．

```cpp
#include <iostream>

int main() {
  int a, b, c;

  std::cin >> a >> b;

  c = a + b;

  std::cout << c << std::endl;

  return 0;
}
```

注：代码空行较多，若不习惯可去掉空行．

#### 简要解释

`std::cin` 是读入（`cin` 即 C-in），`>>` 也与输出语法的类似．

这里多出来的语句中最重要的是两个，一个是变量声明语句．

```cpp
int a, b, c;
```

你可能习惯于 Pascal 里面的声明变量：

```pas
var
a, b, c: integer;
```

C++ 的声明是直接以数据类型名开头的，在这里，`int`（整型）开头表示接下来要声明变量．

接着一个最重要的语句就是赋值语句．

```cpp
c = a + b;
```

这是 Pascal 与 C++ 语法较大的不同：Pascal 的赋值是 `:=`，C++ 是 `=`；而 C++ 判断相等是 `==`．

C++ 也可直接在声明时进行变量初始化赋值．

```cpp
int a = 0, b = 0, c = 0;
```

#### 简单练习

1.  重写一遍代码，提交到 OJ 上，并且 AC．
2.  更多的输入输出语法参考 [这节内容](basic.md#scanf-与-printf)，并试着了解 C++ 的格式化输出．

### 结束语与下一步

好了，到现在为止，你已经掌握了一些最基本的东西了，剩下就是找 Pascal 和 C++ 里面对应的语法和不同的特征．

不过在此之前，强烈建议先看 [变量作用域：全局变量与局部变量](#变量作用域全局变量与局部变量)．

请善用<kbd>Alt</kbd>+<kbd>←</kbd>与<kbd>Alt</kbd>+<kbd>→</kbd>返回跳转．

## 语法

### 变量

#### 基本数据类型

C++ 与 Pascal 基本上差不多，常见的有

-   `bool`：布尔类型
-   `int`：整型
-   `float`：单精度浮点型
-   `double`：双精度浮点型
-   `char`：字符型
-   `void`：无类型

C++ 的单引号是专门用于表示单个字符的（字符型），比如 `'a'`，而字符串（字符型数组）必须要用双引号．

C++ 还要很多额外的数据类型，请参考 [基础类型 - cppreference.com](https://zh.cppreference.com/w/cpp/language/types)．

#### 常量声明

```cpp
const double PI = 3.1415926;
```

若不清楚有关宏展开的问题，建议使用常量，而不用宏定义．

### 运算符

请直接参考 [运算](./op.md) 一文中内容．附录中也提供了运算符与数学函数语法对比表．

### 条件

#### `if` 语句

```pas
if (a = b) and (a > 0) and (b > 0) then
    begin
        b := a;
    end
else
    begin
        a := b;
    end;
```

```cpp
if (a == b && a > 0 && b > 0) {
  b = a;
} else {
  a = b;
}
```

布尔运算与比较

-   `and -> &&`
-   `or -> ||`
-   `not -> !`
-   `= -> ==`
-   `<> -> !=`

注释：

1.  Pascal 中 `and` 与 C++ 中 `&&` 优先级不同，C++ 不需要给判断条件加括号．
2.  Pascal 中判断相等是 `=`，赋值是 `:=`；C++ 中判断相等是 `==`，赋值是 `=`．
3.  如果在 `if` 语句的括号内写了 `a = b` 而不是 `a == b`，程序不会报错，而是会把 `b` 赋值给 `a`，并使赋值表达式 `a = b` 整体具有 `a` 在赋值操作完成后的值．
4.  C++ 不需要思考到底要不要在 `end` 后面加分号．
5.  C++ 布尔运算中，非布尔值可以自动转化为布尔值．

???+ warning "易错提醒"
    特别注意：**不要把 `==` 写成 `=`！**
    
    由于 C/C++ 比 Pascal 语法灵活，如果在判断语句中写了 `if (a=b)`，那么程序会顺利运行下去，因为 C++ 中 `a=b` 是有返回值的．

#### `case` 与 `switch`

用到得不多，此处不详细展开．

需要注意：C++ 没有 `1..n`，也没有连续不等式（比如 `1 < x < 2`）．

### 循环

以下三种循环、六份代码实现的功能是一样的．

#### `while` 循环

`while` 很相似．（C++ 此处并非完整程序，省略一些框架模板，后同）

```pas
var i: integer;

begin
    i := 1;
    while i <= 10 do
        begin
            write(i,' ');
            inc(i); // 或者 i := i + 1;
        end;
end.
```

```cpp
int i = 1;
while (i <= 10) {
  std::cout << i << " ";
  i++;
}
```

#### `for` 循环

C++ 的 `for` 语句非常不同．

```pas
var i: integer;

begin
    for i:= 1 to 10 do
        begin
            write(i, ' ');
        end;
end.
```

```cpp
for (int i = 1; i <= 10; i++) {
  std::cout << i << " ";
}
```

注释：

1.  `for (int i = 1; i <= 10; i++){` 这一行语句很多，`for` 中有三个语句．
2.  第一个语句 `int i = 1;` 此时声明一局部变量 `i` 并初始化．（这个设计比 Pascal 要合理得多．）
3.  第二个语句 `i <= 10;` 作为判断循环是否继续的标准．
4.  第三个语句 `i++`，在每次循环结尾执行，意思大约就是 Pascal 中的 `inc(i)`，此处写成 `++i` 也是一样的．`i++` 与 `++i` 的区别请参考其他资料．

#### `repeat until` 与 `do while` 循环

注意，`repeat until` 与 `do while` 是不同的，请对比以下代码

```pas
var i: integer;

begin
    i := 1;
    repeat
        write(i, ' ');
        inc(i);
    until i = 11;
end.
```

```cpp
int i = 1;
do {
  std::cout << i << " ";
  i++;
} while (i <= 10);
```

#### 循环控制

C++ 中 `break` 的作用与 Pascal 是一样的，退出循环．

而 `continue` 也是一样的，跳过当前循环，进入下一次循环（回到开头）．

### 数组与字符串

#### 不定长数组：标准库类型 Vector

请参考 [序列式容器](csl/sequence-container.md) 页面中内容．

C++ 标准库中提供了 `vector`，相当于不定长数组，调用前需导入库文件．

```cpp
#include <iostream>
#include <vector>  // 导入 vector 库

int main() {
  std::vector<int> a;  // 声明 vector a 并定义 a 为空 vector 对象
  int n;

  std::cin >> n;
  // 读取 a
  for (int i = 0; i < n; i++) {
    int t;
    std::cin >> t;
    a.push_back(t);  // 将读入的数字 t，放到 vector a 的末尾；该操作复杂度 O(1)
    /* 这里不能使用下标访问来赋值，因为声明时，a 大小依然为空，
    此处使用 `a[i] = t;` 是错误做法．
    */
  }

  // 将读入到 a 中的所有数打印出
  for (int i = 0; i < n; i++) {
    std::cout << a[i] << ", ";  // !注意，a 中第一个数是 a[0]；
    // 如果下标越界，它会返回一个未知的值（溢出），而不会报错
  }
  std::cout << std::endl;

  return 0;
}
```

C++ 访问数组成员，与 Pascal 类似，不过有很重要的区别：数组的第一项是 `a[0]`，而 Pascal 中是可以自行指定的．

#### 字符串：标准库类型 String

请参考 [string](csl/string.md) 页面中内容．

C++ 标准库中提供了 `string`，与 `vector` 可以进行的操作有些相同，同样需要导入库文件．

```cpp
#include <iostream>
#include <string>

int main() {
  std::string s;  // 声明 string s

  std::cin >> s;  // 读入 s；
  // 读入时会忽略开头所有空格符（空格、换行符、制表符），读入的字串直到下一个空格符为止．

  std::cout << s << std::endl;

  return 0;
}
```

#### C 风格数组

请参考 [数组](array.md) 页面中内容．

如果要用不定长的数组请用 `vector`，不要用 C 风格的数组．

C 风格的数组与指针有密切关系，所以此处不多展开．

## 重要不同之处

### 变量作用域：全局变量与局部变量

C++ 几乎可以在 **任何地方** 声明变量．请参考 [变量作用域](var.md#变量作用域)．

在写 Pascal 过程/函数时，容易忘记声明局部变量 `i` 或者 `j`，而一般主程序里会有循环，于是大部分情况下 `i` 与 `j` 都是全局变量，于是，在这种情况下，过程/函数中对 `i` 操作极易出错．更要命的是，如果忘记声明这种局部变量，编译器编译不报错，程序可以运行．（有很多难找的 bug 就是这么来的．）

所以，在使用 C++ 时，声明变量，比如循环中使用的 `i`，**不要用全局变量，能用局部变量就用局部变量**．如果这么做，不用担心函数中变量名（比如 `i`）冲突．

??? note "额外注"
    Pascal 可在某种程度上避免这个问题，仿照 C++ 的方法，主程序只有调用过程/函数，不声明 `i`，`j` 这类极易名称冲突的全局变量，如果需要循环，另写一个过程进行调用．

### C++ 可以自动转换类型

```cpp
int i = 2;
if (i) {  // i = 0 会返回 false，其余返回 true
  std::cout << "true";
} else {
  std::cout << "false";
}
```

不光是 `int` 转成 `bool`，还有 `int` 与 `float` 相互转换．在 Pascal 中可以把整型赋给浮点型，但不能反过来．C++ 没有这个问题．

```cpp
int a;
a = 3.2;      // 此时 a = 3
float b = a;  // 此时 b = 3.0
```

区分 `/` 是整除还是浮点除法，是通过除数与被除数的类型判断的

```cpp
float a = 32 / 10;    // 32/10 的结果是 3（整除）；a = 3.0
float b = 32.0 / 10;  // 32.0/10 的结果是 3.2；b = 3.2
```

`pow(a, b)` 计算 $a^b$，该函数返回的是浮点型，如果直接用来计算整数的幂，由于有自动转换，不需要担心它会报错

```cpp
int a = pow(2, 3);  // 计算 2^3
```

还有 `char` 与 `int` 之间相互转换．

```cpp
char a = 48;              // ASCII 48 是 '0'
int b = a + 1;            // b = 49
std::cout << (a == '0');  // true 输出 1
```

其实 C++ 中的 `char` 与 `bool` 本质上是整型．

详细内容请参考 [隐式转换 - cppreference.com](https://zh.cppreference.com/w/cpp/language/implicit_conversion) 一文．

### C++ 很多语句有返回值：以如何实现读取数量不定数据为例

有些时候需要读取到数据结束，比如，求一组不定数量的数之和（数据可以多行），直到文件末尾，实现方式是

??? note "文件末尾 EOF"
    EOF，文件末尾标识符，在命令行中 Windows 上以<kbd>Ctrl</kbd>+<kbd>Z</kbd>输入（还需按<kbd>Enter</kbd>），Unix-like 系统以<kbd>Ctrl</kbd>+<kbd>D</kbd>输入．

```cpp
#include <iostream>

int main() {
  int sum = 0, a = 0;

  while (std::cin >> a) {
    sum += a;
  }
  std::cout << sum << std::endl;

  return 0;
}
```

实现原理：`while (std::cin >> a)` 中 `std::cin >> a` 若在输入有问题或遇到文件结尾时，会返回 `false`，使得循环中断．

### 函数

C++ 只有函数没有过程但有 `void`，没有函数值变量但有 `return`．

Pascal 函数与 C++ 函数对比示例：

```pas
function abs(x:integer):integer;
begin
    if x < 0 then
        begin
            abs := -x;
        end
    else
        begin
            abs := x;
        end;
end;
```

```cpp
int abs(int x) {
  if (x < 0) {
    return -x;
  } else {
    return x;
  }
}
```

C++ 中函数声明 `int abs`，就定义了 `abs()` 函数且返回值为 `int` 型（整型），函数的返回值就是 `return` 语句给出的值．

如果不想有返回值（即 Pascal 的「过程」），就用 `void`．`void` 即「空」，什么都不返回．

```pas
var ans: integer;

procedure printAns(ans:integer);
begin
    writeln(ans);
end;

begin
    ans := 10;
    printAns(ans);
end.
```

```cpp
#include <iostream>

void printAns(int ans) {
  std::cout << ans << std::endl;

  return;
}

int main() {
  int ans = 10;
  printAns(ans);

  return 0;
}
```

C++ 的 `return` 与 Pascal 中给函数变量赋值有一点非常大的不同．C++ 的 `return` 即返回一个值，执行完这个语句，函数就执行结束了；而 Pascal 中给函数变量赋值并不会跳出函数本身，而是继续执行．于是，如果 Pascal 需要某处中断函数/过程，就需要一个额外的命令，即 `exit`．而 C++ 则不需要，如果需要在某处中断，可以直接使用 `return`．比如（由于实在想不出来简短且实用的代码，所以就先这样）

```cpp
#include <iostream>

void printWarning(int x) {
  if (x >= 0) {
    return;  // 该语句在此处相当于 Pascal 中的 `exit;`
  }
  std::cout << "Warning: input a negative number.";
}

int main() {
  int a;

  std::cin >> a;
  printWarning(a);

  return 0;
}
```

而在某种意义上，前面的 `abs` 函数，这样才是严格等效的

```pas
function abs(x:integer):integer;
begin
    if x < 0 then
        begin
            abs := -x; exit; // !注意此处
        end
    else
        begin
            abs := x;  exit; // !注意此处
        end;
end;
```

```cpp
int abs(int x) {
  if (x < 0) {
    return -x;
  } else {
    return x;
  }
}
```

???+ note "特别提醒"
    C++ 中 `exit` 是退出程序；不要顺手把 `exit` 打上去，要用 `return`！

C++ 把函数和过程统统视作函数，连 `main` 都不放过，比如写 `int main`，C++ 视 `main` 为一个整型的函数，这里返回值是 `0`．它是一种习惯约定，返回 `0` 代表程序正常退出．

也许你已经猜到了，`main(int argc, char const *argv[])` 中的参数就是 `int argc` 与 `char const *argv[]`，不过意义请参考其他资料．

### 在函数中传递参数

C++ 中没有 Pascal 的 `var` 关键字可以改变传递的参数，但是 C++ 可以使用引用和指针达到同样的效果．

```pas
var a, b: integer;

procedure swap(var x,y:integer);
var temp:integer;
begin
    temp := x;
    x := y;
    y := temp;
end;

begin
    a := 10; b:= 20;    
    swap(a, b);
    writeln(a, ' ', b);
end.
```

```cpp
// 使用指针的代码
#include <iostream>

void swap(int* x, int* y) {
  int temp;
  temp = *x;
  *x = *y;
  *y = temp;
}

int main() {
  int a = 10, b = 20;
  swap(&a, &b);
  std::cout << a << " " << b;

  return 0;
}
```

注意，此处 C++ 代码 **涉及指针问题**．指针问题还是很麻烦的，建议去阅读相关资料．

```cpp
// 使用引用的代码
#include <iostream>

void swap(int& x, int& y) {
  int temp;
  temp = x;
  x = y;
  y = temp;
}

int main(int argc, char const* argv[]) {
  int a = 10, b = 20;
  swap(a, b);
  std::cout << a << " " << b;

  return 0;
}
```

注意，此处 C++ 代码涉及 **引用相关类型问题**．在用引用调用一些 STL 库、模板库的时候可能会遇到一些问题，这时候需要手动声明别类型．具体资料可以在《C++ Primer》第五版或者网络资料中自行查阅．

C++ 中函数传递参数还有其他方法，其中一种是 **直接使用全局变量传递参数**，如果不会用指针，可以先用这种方法．但是这种方法的缺陷是没有栈保存数据，**没有办法在递归函数中传参**．（除非手写栈，注意，手写栈也是一种突破系统栈限制的方法．）

## C++ 标准库与参考资料

千万不要重复造轮子（除非为了练习），想要自己动手写一个功能出来之前，先去看看有没有这个函数或者数据结构．

### C++ 标准库

C++ 标准库中 `<algorithm>` 有很多有用的函数比如快排、二分查找等，可以直接调用．请参考 [STL 算法](csl/algorithm.md) 页面．

还有 STL 容器，比如数组、向量（可变大小的数组）、队列、栈等，附带很多函数．请参考 [STL 容器简介](csl/container.md) 页面．

如果要找关于字符串操作的函数见

-   [std::basic\_string - cppreference.com](https://zh.cppreference.com/w/cpp/string/basic_string)
-   [`<string>`- C++ Reference](https://www.cplusplus.com/reference/string/)

C/C++ 的指针是很灵活的东西，可以参考 [指针](pointer.md) 页面．如果想要彻底理解指针，建议找本书或者参考手册仔细阅读．

### 错误排查与技巧

-   [常见错误](../contest/common-mistakes.md)
-   [常见技巧](../contest/common-tricks.md)

### C++ 语言资料

-   [学习资源](../contest/resources.md)
-   [cppreference.com](https://zh.cppreference.com/)：最重要的 C/C++ 参考资料
-   [C++ 教程 - 菜鸟教程](https://www.runoob.com/cplusplus/cpp-tutorial.html)
-   [C++ Language - C++ Tutorials](https://www.cplusplus.com/doc/tutorial/)
-   [Reference - C++ Reference](https://www.cplusplus.com/reference/)
-   [C++ Standard Library - Wikipedia](https://en.wikipedia.org/wiki/C%2B%2B_Standard_Library)
-   [The Ultimate Question of Programming, Refactoring, and Everything](https://www.gitbook.com/book/alexastva/the-ultimate-question-of-programming-refactoring-/details)
-   [Google C++ Style Guide](https://google.github.io/styleguide/cppguide.html)

## 后记

写到这里，很多同学会觉得这一点都不急救啊，有很多东西没有提到啊．那也是没办法的事情．

虽然是为了急救，但很多东西像怎么把字符串转化为数字，怎么搜索字符串中的字符，这些东西也不适合一篇精悍短小的急救帖，如果把这些都写出来，那就是 C++ 入门教程，所以请充分利用本 Wiki、参考手册与搜索引擎．

需要指出的一点是，上面说 C++ 的语法，其实有很多语法是从 C 语言来的，标题这么写比较好——《Pascal 转 C/C++ 急救帖》．

Pascal 在上个世纪后半叶是门很流行的语言，它早于 C 语言，不过随着 UNIX 系统的普及，微软使用 C 语言，现在 Pascal 已经成为历史了．Pascal 后期发展也是有的，比如 Free Pascal 这个开源编译器项目，增加面向对象的特性（Delphi 语言）．Pascal 目前的用处除了在信息竞赛外，有一个特点是其他语言没有的——编译支持非常非常多老旧机器，比如 Gameboy 这种上个世纪的任天堂游戏机，还有一个用处就是以伪代码的形式（Pascal 风格的伪代码）出现在各种教科书中．

最后，Pascal 的圈子其实很小，C/C++ 的圈子很大，帮助手册与教程很多很全，一定要掌握好英语．世界上还有很多很多编程语言，而计算机这门学科与技术不光是信息竞赛和编程语言．

### 本文 Pascal 语言的参考文献

-   [Lazarus wiki](https://wiki.freepascal.org/)
-   [Free Pascal Reference guide](https://freepascal.org/docs-html/current/ref/ref.html)

## 附录：Pascal 与 C++ 运算符与数学函数语法对比表

仅包括最常用的运算符与函数．

### 基本算术

|      | Pascal    | C++     |
| ---- | --------- | ------- |
| 加法   | `a + b`   | `a + b` |
| 减法   | `a - b`   | `a - b` |
| 乘法   | `a * b`   | `a * b` |
| 整除   | `a div b` | `a / b` |
| 浮点除法 | `a / b`   | `a / b` |
| 取模   | `a mod b` | `a % b` |

### 逻辑

|   | Pascal    | C++                   |
| - | --------- | --------------------- |
| 非 | `not(a)`  | `!a`                  |
| 且 | `a and b` | `a && b`              |
| 或 | `a or b`  | <code>a \|\| b</code> |

### 比较

|      | Pascal   | C++      |
| ---- | -------- | -------- |
| 相等   | `a = b`  | `a == b` |
| 不等   | `a <> b` | `a != b` |
| 大于   | `a > b`  | `a > b`  |
| 小于   | `a < b`  | `a < b`  |
| 大于等于 | `a >= b` | `a >= b` |
| 小于等于 | `a <= b` | `a <= b` |

### 赋值

| Pascal                        | C++      |
| ----------------------------- | -------- |
| `a := b`                      | `a = b`  |
| `a := a + b`                  | `a += b` |
| `a := a - b`                  | `a -= b` |
| `a := a * b`                  | `a *= b` |
| `a := a div b` 或 `a := a / b` | `a /= b` |
| `a := a mod b`                | `a %= b` |

### 自增/自减

|    | Pascal   | C++   |
| -- | -------- | ----- |
| 自增 | `inc(a)` | `a++` |
| 自增 | `inc(a)` | `++a` |
| 自减 | `dec(a)` | `a--` |
| 自减 | `dec(a)` | `--a` |

### 数学函数

使用需要导入 `<cmath>` 库．

|       | Pascal     | C++            |
| ----- | ---------- | -------------- |
| 绝对值   | `abs(a)`   | `abs(a)`（整数）   |
| 绝对值   | `abs(a)`   | `fabs(a)`（浮点数） |
| $a^b$ | N/A[^ref1] | `pow(a, b)`    |
| 截断取整  | `trunc(a)` | `trunc(a)`     |
| 近似取整  | `round(a)` | `round(a)`     |

[^ref1]: Extended Pascal 中有 `a**b`，不过需要导入 `Math` 库．

其他函数请参考：

-   [常用数学函数 - cppreference.com](https://zh.cppreference.com/w/cpp/numeric/math)


## lang/pb-ds/index.md

author: HeRaNO, Xeonacid, saffahyjp

pb\_ds 库全称 Policy-Based Data Structures．

pb\_ds 库封装了很多数据结构，比如哈希（Hash）表，平衡二叉树，字典树（Trie 树），堆（优先队列）等．

就像 `vector`、`set`、`map` 一样，其组件均符合 STL 的相关接口规范．部分（如优先队列）包含 STL 内对应组件的所有功能，但比 STL 功能更多．

pb\_ds 只在使用 libstdc++ 为标准库的编译器下可以用．

可以使用 `begin()` 和 `end()` 来获取 `iterator` 从而遍历

可以 `increase_key`,`decrease_key` 以及删除单个元素

由于 pb\_ds 库的主要内容在以下划线开头的 `__gnu_pbds` 命名空间中，在 NOI 系列活动中的合规性一直没有确定．2021 年 9 月 1 日，根据 [《关于 NOI 系列活动中编程语言使用限制的补充说明》](https://www.noi.cn/xw/2021-09-01/735729.shtml)，允许使用以下划线开头的库函数或宏（但具有明确禁止操作的库函数和宏除外），在 NOI 系列活动中使用 pb\_ds 库的合规性有了文件上的依据．

**参考资料：[《C++ 的 pb\_ds 库在 OI 中的应用》](https://github.com/OI-Wiki/libs/blob/master/lang/pb-ds/C%2B%2B的pb_ds库在OI中的应用.pdf)**


## lang/pb-ds/pq.md

author: Xeonacid, ouuan, Ir1d, WAAutoMaton, Chrogeek, abc1763613206, Planet6174, i-Yirannn, opsiff, GoodCoder666

## `__gnu_pbds::priority_queue`

附：[官方文档地址——复杂度及常数测试](https://gcc.gnu.org/onlinedocs/libstdc++/ext/pb_ds/pq_performance_tests.html#std_mod1)

```cpp
#include <ext/pb_ds/priority_queue.hpp>
using namespace __gnu_pbds;
__gnu_pbds::priority_queue<T, Compare, Tag, Allocator>
```

## 模板形参

-   `T`: 储存的元素类型
-   `Compare`: 提供严格的弱序比较类型
-   `Tag`: 是 `__gnu_pbds` 提供的不同的五种堆，Tag 参数默认是 `pairing_heap_tag` 五种分别是：
    -   `pairing_heap_tag`：配对堆
        官方文档认为在非原生元素（如自定义结构体/`std::string`/`pair`）中，配对堆表现最好
    -   `binary_heap_tag`：二叉堆
        官方文档认为在原生元素中二叉堆表现最好，不过笔者测试的表现并没有那么好
    -   `binomial_heap_tag`：二项堆
        二项堆在合并操作的表现要优于二叉堆，但是其取堆顶元素操作的复杂度比二叉堆高
    -   `rc_binomial_heap_tag`：冗余计数二项堆
    -   `thin_heap_tag`：除了合并的复杂度都和 Fibonacci 堆一样的一个 tag
-   `Allocator`：空间配置器，由于 OI 中很少出现，故这里不做讲解

由于本篇文章只是提供给学习算法竞赛的同学们，故对于后四个 tag 只会简单的介绍复杂度，第一个会介绍成员函数和使用方法．

经作者本机 Core i5 @3.1 GHz On macOS 测试堆的基础操作，结合 GNU 官方的复杂度测试，Dijkstra 测试，都表明：
至少对于 OIer 来讲，除了配对堆的其他四个 tag 都是鸡肋，要么没用，要么常数大到不如 `std` 的，且有可能造成 MLE，故这里只推荐用默认的配对堆．同样，配对堆也优于 `algorithm` 库中的 `make_heap()`．

## 构造方式

要注明命名空间因为和 `std` 的类名称重复．

```cpp
// __gnu_pbds::priority_queue<int>;
// __gnu_pbds::priority_queue<int, greater<int>>;
// __gnu_pbds::priority_queue<int, greater<int>, pairing_heap_tag>;
__gnu_pbds::priority_queue<int>::point_iterator id;  // 点类型迭代器
// 在 modify 和 push 的时候都会返回一个 point_iterator，下文会详细的讲使用方法
id = q.push(1);
```

## 成员函数

-   `push()`: 向堆中压入一个元素，返回该元素位置的迭代器．
-   `pop()`: 将堆顶元素弹出．
-   `top()`: 返回堆顶元素．
-   `size()` 返回元素个数．
-   `empty()` 返回是否非空．
-   `modify(point_iterator, const key)`: 把迭代器位置的 `key` 修改为传入的 `key`，并对底层储存结构进行排序．
-   `erase(point_iterator)`: 把迭代器位置的键值从堆中擦除．
-   `join(__gnu_pbds::priority_queue &other)`: 把 `other` 合并到 `*this` 并把 `other` 清空．

使用的 tag 决定了每个操作的时间复杂度：

|                        | push                                | pop                                 | modify                              | erase                               | Join              |
| ---------------------- | ----------------------------------- | :---------------------------------- | ----------------------------------- | ----------------------------------- | ----------------- |
| `pairing_heap_tag`     | $O(1)$                              | 最坏 $\Theta(n)$ 均摊 $\Theta(\log(n))$ | 最坏 $\Theta(n)$ 均摊 $\Theta(\log(n))$ | 最坏 $\Theta(n)$ 均摊 $\Theta(\log(n))$ | $O(1)$            |
| `binary_heap_tag`      | 最坏 $\Theta(n)$ 均摊 $\Theta(\log(n))$ | 最坏 $\Theta(n)$ 均摊 $\Theta(\log(n))$ | $\Theta(n)$                         | $\Theta(n)$                         | $\Theta(n)$       |
| `binomial_heap_tag`    | 最坏 $\Theta(\log(n))$ 均摊 $O(1)$      | $\Theta(\log(n))$                   | $\Theta(\log(n))$                   | $\Theta(\log(n))$                   | $\Theta(\log(n))$ |
| `rc_binomial_heap_tag` | $O(1)$                              | $\Theta(\log(n))$                   | $\Theta(\log(n))$                   | $\Theta(\log(n))$                   | $\Theta(\log(n))$ |
| `thin_heap_tag`        | $O(1)$                              | 最坏 $\Theta(n)$ 均摊 $\Theta(\log(n))$ | 最坏 $\Theta(\log(n))$ 均摊 $O(1)$      | 最坏 $\Theta(n)$ 均摊 $\Theta(\log(n))$ | $\Theta(n)$       |

## 示例

```cpp
#include <algorithm>
#include <cstdio>
#include <ext/pb_ds/priority_queue.hpp>
#include <iostream>
using namespace __gnu_pbds;
// 由于面向OIer, 本文以常用堆 : pairing_heap_tag作为范例
// 为了更好的阅读体验，定义宏如下 ：
using pair_heap = __gnu_pbds::priority_queue<int>;
pair_heap q1;  // 大根堆, 配对堆
pair_heap q2;
pair_heap::point_iterator id;  // 一个迭代器

int main() {
  id = q1.push(1);
  // 堆中元素 ： [1];
  for (int i = 2; i <= 5; i++) q1.push(i);
  // 堆中元素 :  [1, 2, 3, 4, 5];
  std::cout << q1.top() << std::endl;
  // 输出结果 : 5;
  q1.pop();
  // 堆中元素 : [1, 2, 3, 4];
  id = q1.push(10);
  // 堆中元素 : [1, 2, 3, 4, 10];
  q1.modify(id, 1);
  // 堆中元素 :  [1, 1, 2, 3, 4];
  std::cout << q1.top() << std::endl;
  // 输出结果 : 4;
  q1.pop();
  // 堆中元素 : [1, 1, 2, 3];
  id = q1.push(7);
  // 堆中元素 : [1, 1, 2, 3, 7];
  q1.erase(id);
  // 堆中元素 : [1, 1, 2, 3];
  q2.push(1), q2.push(3), q2.push(5);
  // q1中元素 : [1, 1, 2, 3], q2中元素 : [1, 3, 5];
  q2.join(q1);
  // q1中无元素，q2中元素 ：[1, 1, 1, 2, 3, 3, 5];
}
```

## \_\_gnu\_pbds 迭代器的失效保证（invalidation\_guarantee）

在上述示例以及一些实践中（如使用本章的 pb-ds 堆来编写单源最短路等算法），常常需要保存并使用堆的迭代器（如 `__gnu_pbds::priority_queue<int>::point_iterator` 等）．

可是例如对于 `__gnu_pbds::priority_queue` 中不同的 Tag 参数，其底层实现并不相同，迭代器的失效条件也不一样，根据\_\_gnu\_pbds 库的设计，以下三种由上至下派生的情况：

1.  基本失效保证（basic\_invalidation\_guarantee）：即不修改容器时，点类型迭代器（point\_iterator）、指针和引用（key/value）**保持** 有效．

2.  点失效保证（point\_invalidation\_guarantee）：即 **修改** 容器后，点类型迭代器（point\_iterator）、指针和引用（key/value）只要对应在容器中没被删除 **保持** 有效．

3.  范围失效保证（range\_invalidation\_guarantee）：即 **修改** 容器后，除（2）的特性以外，任何范围类型的迭代器（包括 `begin()` 和 `end()` 的返回值）是正确的，具有范围失效保证的 Tag 有 `rb_tree_tag` 和 适用于 `__gnu_pbds::tree` 的 `splay_tree_tag`，以及 适用于 `__gnu_pbds::trie` 的 `pat_trie_tag`．

从运行下述代码中看出，除了 `binary_heap_tag` 为 `basic_invalidation_guarantee` 在修改后迭代器会失效，其余的均为 `point_invalidation_guarantee` 可以实现修改后点类型迭代器 (point\_iterator) 不失效的需求．

```cpp
#include <iostream>
using namespace std;
#include <ext/pb_ds/assoc_container.hpp>
#include <ext/pb_ds/priority_queue.hpp>
using namespace __gnu_pbds;
#include <cxxabi.h>

template <typename T>
void print_invalidation_guarantee() {
  using gute = __gnu_pbds::container_traits<T>::invalidation_guarantee;
  cout << abi::__cxa_demangle(typeid(gute).name(), 0, 0, 0) << endl;
}

int main() {
  using pairing =
      __gnu_pbds::priority_queue<int, greater<int>, pairing_heap_tag>;
  using binary = __gnu_pbds::priority_queue<int, greater<int>, binary_heap_tag>;
  using binomial =
      __gnu_pbds::priority_queue<int, greater<int>, binomial_heap_tag>;
  using rc_binomial =
      __gnu_pbds::priority_queue<int, greater<int>, rc_binomial_heap_tag>;
  using thin = __gnu_pbds::priority_queue<int, greater<int>, thin_heap_tag>;
  print_invalidation_guarantee<pairing>();
  print_invalidation_guarantee<binary>();
  print_invalidation_guarantee<binomial>();
  print_invalidation_guarantee<rc_binomial>();
  print_invalidation_guarantee<thin>();
  return 0;
}
```


## lang/pb-ds/tree.md

## `__gnu_pbds::tree`

附：[官方文档地址](https://gcc.gnu.org/onlinedocs/libstdc++/ext/pb_ds/tree_based_containers.html)

```cpp
#include <ext/pb_ds/assoc_container.hpp>  // 因为 tree 定义在这里 所以需要包含这个头文件
#include <ext/pb_ds/tree_policy.hpp>
using namespace __gnu_pbds;
__gnu_pbds::tree<Key, Mapped, Cmp_Fn = std::less<Key>, Tag = rb_tree_tag,
                 Node_Update = null_tree_node_update,
                 Allocator = std::allocator<char>>
```

## 模板形参

-   `Key`: 储存的元素类型，如果想要存储多个相同的 `Key` 元素，则需要使用类似于 `std::pair` 和 `struct` 的方法，并配合使用 `lower_bound` 和 `upper_bound` 成员函数进行查找
-   `Mapped`: 映射规则（Mapped-Policy）类型，如果要指示关联容器是 **集合**，类似于存储元素在 `std::set` 中，此处填入 `null_type`，低版本 `g++` 此处为 `null_mapped_type`；如果要指示关联容器是 **带值的集合**，类似于存储元素在 `std::map` 中，此处填入类似于 `std::map<Key, Value>` 的 `Value` 类型
-   `Cmp_Fn`: 关键字比较函子，例如 `std::less<Key>`
-   `Tag`: 选择使用何种底层数据结构类型，默认是 `rb_tree_tag`．`__gnu_pbds` 提供不同的三种平衡树，分别是：
    -   `rb_tree_tag`：红黑树，一般使用这个，后两者的性能一般不如红黑树
    -   `splay_tree_tag`：splay 树
    -   `ov_tree_tag`：有序向量树，只是一个由 `vector` 实现的有序结构，类似于排序的 `vector` 来实现平衡树，性能取决于数据想不想卡你
-   `Node_Update`：用于更新节点的策略，默认使用 `null_node_update`，若要使用 `order_of_key` 和 `find_by_order` 方法，需要使用 `tree_order_statistics_node_update`
-   `Allocator`：空间分配器类型

## 构造方式

```cpp
__gnu_pbds::tree<std::pair<int, int>, __gnu_pbds::null_type,
                 std::less<std::pair<int, int>>, __gnu_pbds::rb_tree_tag,
                 __gnu_pbds::tree_order_statistics_node_update>
    trr;
```

## 成员函数

-   `insert(x)`：向树中插入一个元素 `x`，返回 `std::pair<point_iterator, bool>`，其中第一个元素代表插入位置的迭代器，第二个元素代表是否插入成功．
-   `erase(x)`：从树中删除一个元素/迭代器 `x`．如果 `x` 是迭代器，则返回指向 `x` 下一个的迭代器（如果 `x` 是 `end()` 则返回 `end()`）；如果 `x` 是 `Key`，则返回是否删除成功（如果不存在则删除失败）．
-   `order_of_key(x)`：返回严格小于 `x` 的元素个数（以 `Cmp_Fn` 作为比较逻辑），即从 $0$ 开始的排名．
-   `find_by_order(x)`：返回 `Cmp_Fn` 比较的排名所对应元素的迭代器．
-   `lower_bound(x)`：返回第一个不小于 `x` 的元素所对应的迭代器（以 `Cmp_Fn` 作为比较逻辑）．
-   `upper_bound(x)`：返回第一个严格大于 `x` 的元素所对应的迭代器（以 `Cmp_Fn` 作为比较逻辑）．
-   `join(x)`：将 `x` 树并入当前树，`x` 树被清空（必须确保两树的 **比较函数** 和 **元素类型** 相同）．
-   `split(x,b)`：以 `Cmp_Fn` 比较，小于等于 `x` 的属于当前树，其余的属于 `b` 树．
-   `empty()`：返回是否为空．
-   `size()`：返回大小．

???+ warning "注意"
    `join(x)` 函数需要保证并入树的键的值域与被并入树的键的值域 **不相交**（也就是说并入树内所有值必须全部大于/小于当前树内的所有值），否则会抛出 `join_error` 异常．
    
    如果要合并两棵值域有交集的树，需要将一棵树的元素一一插入到另一棵树中．

## 示例

```cpp
// Common Header Simple over C++11
#include <iostream>
using namespace std;
using ll = long long;
using ull = unsigned long long;
using ld = long double;
using pii = pair<int, int>;
#include <ext/pb_ds/assoc_container.hpp>
#include <ext/pb_ds/tree_policy.hpp>
__gnu_pbds::tree<pair<int, int>, __gnu_pbds::null_type, less<pair<int, int>>,
                 __gnu_pbds::rb_tree_tag,
                 __gnu_pbds::tree_order_statistics_node_update>
    trr;

int main() {
  int cnt = 0;
  trr.insert(make_pair(1, cnt++));
  trr.insert(make_pair(5, cnt++));
  trr.insert(make_pair(4, cnt++));
  trr.insert(make_pair(3, cnt++));
  trr.insert(make_pair(2, cnt++));
  // 树上元素 {(1,0), (2,4), (3,3), (4,2), (5,1)}

  auto it = trr.lower_bound(make_pair(2, 0));
  trr.erase(it);
  // 树上元素 {(1,0), (3,3), (4,2), (5,1)}

  // 输出排名 0 1 2 3 中的排名 1 的元素的 first
  auto it2 = trr.find_by_order(1);
  cout << (*it2).first << endl;  // 输出：3

  // 输出其排名
  int pos = trr.order_of_key(*it2);
  cout << pos << endl;  // 输出：1

  // 按照 it2 分裂 trr
  decltype(trr) newtr;
  trr.split(*it2, newtr);
  for (auto i = newtr.begin(); i != newtr.end(); ++i) {
    cout << (*i).first << ' ';  // 输出：4 5
  }
  cout << endl;

  // 将 newtr 树并入 trr 树，newtr 树被清空．
  trr.join(newtr);
  for (auto i = trr.begin(); i != trr.end(); ++i) {
    cout << (*i).first << ' ';  // 输出：1 3 4 5
  }
  cout << endl;
  cout << newtr.size() << endl;  // 输出：0

  return 0;
}
```

## 参考资料

-   [Tree-Based Containers](https://gcc.gnu.org/onlinedocs/libstdc++/ext/pb_ds/tree_based_containers.html)
-   [`join` 函数在 GCC 14.1.0 中的实现](https://gcc.gnu.org/onlinedocs/gcc-14.1.0/libstdc++/api/a18391_source.html#l00043)
-   [`erase` 函数在 GCC 14.1.0 中的实现](https://gcc.gnu.org/onlinedocs/gcc-14.1.0/libstdc++/api/a18211_source.html#l00043)


## lang/pointer.md

author: tsagaanbar, Enter-tainer, Xeonacid

## 变量的地址、指针

在程序中，我们的数据都有其存储的地址．在程序每次的实际运行过程中，变量在物理内存中的存储位置不尽相同．不过，我们仍能够在编程时，通过一定的语句，来取得数据在内存中的地址．

地址也是数据．存放地址所用的变量类型有一个特殊的名字，叫做「指针变量」，有时也简称做「指针」．

???+ note "指针变量的大小"
    指针变量的大小在不同环境下有差异．在 32 位机上，地址用 32 位二进制整数表示，因此一个指针的大小为 4 字节．而 64 位机上，地址用 64 位二进制整数表示，因此一个指针的大小就变成了 8 字节．

地址只是一个刻度一般的数据，为了针对不同类型的数据，「指针变量」也有不同的类型，比如，可以有 `int` 类型的指针变量，其中存储的地址（即指针变量存储的数值）对应一块大小为 32 位的空间的起始地址；有 `char` 类型的指针变量，其中存储的地址对应一块 8 位的空间的起始地址．

事实上，用户也可以声明指向指针变量的指针变量．

假如用户自定义了一个结构体：

```cpp
struct ThreeInt {
  int a;
  int b;
  int c;
};
```

则 `ThreeInt` 类型的指针变量，对应着一块 3 × 32 = 96 bit 的空间．

## 指针的声明与使用

C/C++ 中，指针变量的类型为类型名后加上一个星号 `*`．比如，`int` 类型的指针变量的类型名即为 `int*`．

我们可以使用 `&` 符号取得一个变量的地址．

要想访问指针变量地址所对应的空间（又称指针所 **指向** 的空间），需要对指针变量进行 **解引用**（dereference），使用 `*` 符号．

```cpp
int main() {
  int a = 123;  // a: 123
  int* pa = &a;
  *pa = 321;  // a: 321
}
```

对结构体变量也是类似．如果要访问指针指向的结构中的成员，需要先对指针进行解引用，再使用 `.` 成员关系运算符．不过，更推荐使用「箭头」运算符 `->` 这一更简便的写法．

```cpp
struct ThreeInt {
  int a;
  int b;
  int c;
};

int main() {
  ThreeInt x{1, 2, 3}, y{6, 7, 8};
  ThreeInt* px = &x;
  (*px) = y;    // x: {6,7,8}
  (*px).a = 4;  // x: {4,7,8}
  px->b = 5;    // x: {4,5,8}
}
```

## 指针的偏移

指针变量也可以 **和整数** 进行加减操作．对于 `int` 型指针，每加 1（递增 1），其指向的地址偏移 32 位（即 4 个字节）；若加 2，则指向的地址偏移 2 × 32 = 64 位．同理，对于 `char` 型指针，每次递增，其指向的地址偏移 8 位（即 1 个字节）．

### 使用指针偏移访问数组

我们前面说过，数组是一块连续的存储空间．而在 C/C++ 中，直接使用数组名，得到的是数组的起始地址．

```cpp
int main() {
  int a[3] = {1, 2, 3};
  int* p = a;  // p 指向 a[0]
  *p = 4;      // a: [4, 2, 3]
  p = p + 1;   // p 指向 a[1]
  *p = 5;      // a: [4, 5, 3]
  p++;         // p 指向 a[2]
  *p = 6;      // a: [4, 5, 6]
}
```

当通过指针访问数组中的元素时，往往需要用到「指针的偏移」，换句话说，即通过一个基地址（数组起始的地址）加上偏移量来访问．

我们常用 `[]` 运算符来访问数组中某一指定偏移量处的元素．比如 `a[3]` 或者 `p[4]`．这种写法和对指针进行运算后再引用是等价的，即 `p[4]` 和 `*(p + 4)` 是等价的两种写法．

## 空指针

在 C++11 之前，C++ 和 C 一样使用 `NULL` 宏表示空指针常量，C++ 中 `NULL` 的实现一般如下：

```cpp
// C++11 前
#define NULL 0
```

???+ note "C 语言对 `NULL` 的定义"
    C 语言在 C23 前有两个 `NULL` 的定义，只有类型不同：一个是整型常量表达式，一个是转换为 `void *` 类型的常量表达式，但其值都为 0，编译器可任选一个实现．

空指针和整数 `0` 的混用在 C++ 中会导致许多问题，比如：

```cpp
int f(int x);
int f(int* p);
```

在调用 `f(NULL)` 时，实际调用的函数的类型是 `int(int)` 而不是 `int(int *)`.

???+ note "`NULL` 在 C 语言中造成的问题"
    比起在 C++ 中，因为有两个定义，在 C 语言中 `NULL` 造成的问题更为严重：如果在一个传递可变参数的函数中，函数编写者想要接受一个指针，但是函数调用者传递了一个定义为整型的 `NULL`，则会造成未定义行为，因在函数内使用传入的可变参数时，要进行类型转换，而从整型到指针类型的转换是未定义行为．[^note1]

为了解决这些问题，C++11 引入了 `nullptr` 关键字作为空指针常量．

C++ 规定 `nullptr` 可以隐式转换为任何指针类型，这种转换结果是该类型的空指针值．

`nullptr` 的类型为 `std::nullptr_t`, 称作空指针类型，可能的实现如下：

```cpp
namespace std {
typedef decltype(nullptr) nullptr_t;
}
```

另外，C++11 起 `NULL` 宏的实现也被修改为了：

```cpp
// C++11 起
#define NULL nullptr
```

???+ note "C 语言对空指针常量的改进"
    基于类似的原因，C23 也引入了 `nullptr` 作为空指针常量，同时引入了 `nullptr_t` 作为其类型[^note1]．

## 指针的进阶使用

使用指针，使得程序编写者可以操作程序运行时中各处的数据，而不必局限于作用域．

### 指针类型参数的使用

在 C/C++ 中，调用函数（过程）时使用的参数，均以拷贝的形式传入子过程中（引用除外，会在后续介绍）．默认情况下，函数仅能通过返回值，将结果返回到调用处．但是，如果某个函数希望修改其外部的数据，或者某个结构体/类的数据量较为庞大、不宜进行拷贝，这时，则可以通过向其传入外部数据的地址，便得以在其中访问甚至修改外部数据．

下面的 `my_swap` 方法，通过接收两个 `int` 型的指针，在函数中使用中间变量，完成对两个 `int` 型变量值的交换．

```cpp
void my_swap(int *a, int *b) {
  int t;
  t = *a;
  *a = *b;
  *b = t;
}

int main() {
  int a = 6, b = 10;
  my_swap(&a, &b);
  // 调用后，main 函数中 a 变量的值变为 10，b 变量的值变为 6
}
```

C++ 中引入了引用的概念，相对于指针来说，更易用，也更安全．详情可以参见 [C++：引用](./reference.md) 以及 [C 与 C++ 的区别：指针与引用](./cpp-other-langs.md#指针与引用)．

### 动态实例化

除此之外，程序编写时往往会涉及到动态内存分配，即，程序会在运行时，向操作系统动态地申请或归还存放数据所需的内存．当程序通过调用操作系统接口申请内存时，操作系统将返回程序所申请空间的地址．要使用这块空间，我们需要将这块空间的地址存储在指针变量中．

在 C++ 中，我们使用 `new` 运算符来获取一块内存，使用 `delete` 运算符释放某指针所指向的空间．

```cpp
int* p = new int(1234);
/* ... */
delete p;
```

上面的语句使用 `new` 运算符向操作系统申请了一块 `int` 大小的空间，将其中的值初始化为 1234，并声明了一个 `int` 型的指针 `p` 指向这块空间．

同理，也可以使用 `new` 开辟新的对象：

```cpp
class A {
  int a;

 public:
  A(int a_) : a(a_) {}
};

int main() {
  A* p = new A(1234);
  /* ... */
  delete p;
}
```

如上，「`new` 表达式」将尝试开辟一块对应大小的空间，并尝试在这块空间上构造这一对象，并返回这一空间的地址．

```cpp
struct ThreeInt {
  int a;
  int b;
  int c;
};

int main() {
  ThreeInt* p = new ThreeInt{1, 2, 3};
  /* ... */
  delete p;
}
```

???+ note "列表初始化"
    `{}` 运算符可以用来初始化没有构造函数的结构．除此之外，使用 `{}` 运算符可以使得变量的初始化形式变得统一．详见「[list initialization (since C++11)](https://en.cppreference.com/w/cpp/language/list_initialization)」．

需要注意，当使用 `new` 申请的内存不再使用时，需要使用 `delete` 释放这块空间．不能对一块内存释放两次或以上．而对空指针 `nullptr` 使用 `delete` 操作是合法的．

### 动态创建数组

也可以使用 `new[]` 运算符创建数组，这时 `new[]` 运算符会返回数组的首地址，也就是数组第一个元素的地址，我们可以用对应类型的指针存储这个地址．释放时，则需要使用 `delete[]` 运算符．

```cpp
size_t element_cnt = 5;
int *p = new int[element_cnt];
delete[] p;
```

数组中元素的存储是连续的，即 `p + 1` 指向的是 `p` 的后继元素．

### 二维数组

在存放矩阵形式的数据时，可能会用到「二维数组」这样的数据类型．从语义上来讲，二维数组是一个数组的数组．而计算机内存可以视作一个很长的一维数组．要在计算机内存中存放一个二维数组，便有「连续」与否的说法．

所谓「连续」，即二维数组的任意一行（row）的末尾与下一行的起始，在物理地址上是毗邻的，换言之，整个二维数组可以视作一个一维数组；反之，则二者在物理上不一定相邻．

对于「连续」的二维数组，可以仅使用一个循环，借由一个不断递增的指针即可遍历数组中的所有数据．而对于非连续的二维数组，由于每一行不连续，则需要先取得某一行首的地址，再访问这一行中的元素．

???+ note "二维数组的存储方式"
    这种按照「行（row）」存储数据的方式，称为行优先存储；相对的，也可以按照列（column）存储数据．由于计算机内存访问的特性，一般来说，访问连续的数据会得到更高的效率．因此，需要按照数据可能的使用方式，选择「行优先」或「列优先」的存储方式．

### 动态创建二维数组

在 C/C++ 中，我们可以使用类似下面这样的语句声明一个 N 行（row）M 列（column）的二维数组，其空间在物理上是连续的．

???+ note "描述数组的维度"
    更通用的方式是使用第 n 维（dimension）的说法．对于「行优先」的存储形式，数组的第一维长度为 N，第二维长度为 M．

```cpp
int a[N][M];
```

这种声明方式要求 N 和 M 为在编译期即可确定的常量表达式．

在 C/C++ 中，数组的第一个元素下标为 0，因此 `a[r][c]` 这样的式子代表二维数组 a 中第 r + 1 行的第 c + 1 个元素，我们也称这个元素的下标为 `(r,c)`．

不过，实际使用中，（二维）数组的大小可能不是固定的，需要动态内存分配．

常见的方式是声明一个长度为 N × M 的 **一维数组**，并通过下标 `r * M + c` 访问二维数组中下标为 `(r, c)` 的元素．

```cpp
int* a = new int[N * M];
```

这种方法可以保证二维数组是 **连续的**．

???+ note "数组在物理层面上的线性存储"
    实际上，数据在内存中都可以视作线性存放的，因此在一定的规则下，通过动态开辟一维数组的空间，即可在其上存储 n 维的数组．

此外，亦可以根据「数组的数组」这一概念来进行内存的获取与使用．对于一个存放的若干数组的数组，实际上为一个存放的若干数组的首地址的数组，也就是一个存放若干指针变量的数组．

我们需要一个变量来存放这个「数组的数组」的首地址——也就是一个指针的地址．这个变量便是一个「指向指针的指针」，有时也称作「二重指针」，如：

```cpp
int** a = new int*[5];
```

接着，我们需要为每一个数组申请空间：

```cpp
for (int i = 0; i < 5; i++) {
  a[i] = new int[5];
}
```

至此，我们便完成了内存的获取．而对于这样获得的内存的释放，则需要进行一个逆向的操作：即先释放每一个数组，再释放存储这些数组首地址的数组，如：

```cpp
for (int i = 0; i < 5; i++) {
  delete[] a[i];
}
delete[] a;
```

需要注意，这样获得的二维数组，不能保证其空间是连续的．

还有一种方式，需要使用到「指向数组的指针」．

???+ note "数组名和数组首元素地址的区别"
    我们之前说到，在 C/C++ 中，直接使用数组名，值等于数组首元素的地址．但是数组名表示的这一变量的类型实际上是整个数组，而非单个元素．
    
    ```cpp
    int main() { int a[5] = {1, 2, 3, 4, 5}; }
    ```
    
    从概念上说，代码中标识符 `a` 的类型是 `int[5]`；从实际上来说，`a + 1` 所指向的地址相较于 `a` 指向的地址的偏移量为 5 个 `int` 型变量的长度．

```cpp
int main() {
  int(*a)[5] = new int[5][5];
  int* p = a[2];
  a[2][1] = 1;
  delete[] a;
}
```

这种方式获得到的也是连续的内存，但是可以直接使用 `a[n]` 的形式获得到数组的第 n + 1 行（row）的首地址，因此，使用 `a[r][c]` 的形式即可访问到下标为 `(r, c)` 的元素．

由于指向数组的指针也是一种确定的数据类型，因此除数组的第一维外，其他维度的长度均须为一个能在编译器确定的常量．不然，编译器将无法翻译如 `a[n]` 这样的表达式（`a` 为指向数组的指针）．

## 指向函数的指针

关于函数的介绍请参见 [C++ 函数](./func.md) 章节．

简单地说，要调用一个函数，需要知晓该函数的参数类型、个数以及返回值类型，这些也统一称作接口类型．

可以通过函数指针调用函数．有时候，若干个函数的接口类型是相同的，使用函数指针可以根据程序的运行 **动态地** 选择需要调用的函数．换句话说，可以在不修改一个函数的情况下，仅通过修改向其传入的参数（函数指针），使得该函数的行为发生变化．

假设我们有若干针对 `int` 类型的二元运算函数，则函数的参数为 2 个 `int`，返回值亦为 `int`．下边是一个使用了函数指针的例子：

```cpp
#include <iostream>

int (*binary_int_op)(int, int);

int foo1(int a, int b) { return a * b + b; }

int foo2(int a, int b) { return (a + b) * b; }

int main() {
  int choice;
  std::cin >> choice;
  if (choice == 1) {
    binary_int_op = foo1;
  } else {
    binary_int_op = foo2;
  }

  int m, n;
  std::cin >> m >> n;
  std::cout << binary_int_op(m, n);
}
```

???+ note "`&`、`*` 和函数指针"
    在 C 语言中，诸如 `void (*p)() = foo;`、`void (*p)() = &foo;`、`void (*p)() = *foo;`、`void (*p)() = ***foo` 等写法的结果是一样的．
    
    因为函数（如 `foo`）是能够被隐式转换为指向函数的指针的，因此 `void (*p)() = foo;` 的写法能够成立．
    
    使用 `&` 运算符可以取得到对象的地址，这对函数也是成立的，因此 `void (*p)() = &foo;` 的写法仍然成立．
    
    对函数指针使用 `*` 运算符可以取得指针指向的函数，而对于 `**foo` 这样的写法来说，`*foo` 得到的是 `foo` 这个函数，紧接着又被隐式转换为指向 `foo` 的指针．如此类推，`**foo` 得到的最终还是指向 `foo` 的函数指针；用户尽可以使用任意多的 `*`，结果也是一样的．
    
    同理，在调用时使用类似 `(*p)()` 和 `p()` 的语句是一样的，可以省去 `*` 运算符．
    
    参考资料：[Why do function pointer definitions work with any number of ampersands '&' or asterisks '\*'? - stackoverflow.com](https://stackoverflow.com/questions/6893285/why-do-function-pointer-definitions-work-with-any-number-of-ampersands-or-as)

可以使用 `typedef` 关键字声明函数指针的类型．

```cpp
typedef int (*p_bi_int_op)(int, int);
```

这样我们就可以在之后使用 `p_bi_int_op` 这种类型，即指向「参数为 2 个 `int`，返回值亦为 `int`」的函数的指针．

可以通过使用 `std::function` 来更方便的引用函数．（未完待续）

使用函数指针，可以实现「回调函数」．（未完待续）

## 参考资料与注释

[^note1]: 参见 [Introduce the nullptr constant](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n3042.htm)


## lang/python.md

author: cmpute, Henry-ZHR, ranwen, abc1763613206, billchenchina, chinggg, ChungZH, CoelacanthusHex, countercurrent-time, Dong Tsing-hsuen, Early0v0, Enter-tainer, F1shAndCat, Great-designer, hensier, HeRaNO, Hszzzx, imba-tjd, Ir1d, ksyx, lingxier, LovelyBuggies, Marcythm, mgt, Mooos-MoSheng, NachtgeistW, ouuan, Rottenwooood, shawlleyw, shuzhouliu, sshwy, SukkaW, Suyun514, Tiphereth-A, tLLWtG, wineee, wxh06, Xeonacid, yusancky, zyouxam, zzjjbb, jiangmuran, CuriosityQiu

## 关于 Python

Python 是一门已在世界上广泛使用的解释型语言．它提供了高效的高级数据结构，还能简单有效地面向对象编程，也可以在算法竞赛．

### Python 的优点

-   Python 是一门 **解释型** 语言：Python 不需要编译和链接，可以在一定程度上减少操作步骤．
-   Python 是一门 **交互式** 语言：Python 解释器实现了交互式操作，可以直接在终端输入并执行指令．
-   Python **易学易用**：Python 提供了大量的数据结构，也支持开发大型程序．
-   Python **兼容性强**：Python 同时支持 Windows、macOS 和 Unix 操作系统．
-   Python **实用性强**：从简单的输入输出到科学计算甚至于大型 WEB 应用，都可以写出适合的 Python 程序．
-   Python **程序简洁、易读**：Python 代码通常比实现同种功能的其他语言的代码短．
-   Python **支持拓展**：Python 会开发 C 语言程序（即 CPython），支持把 Python 解释器和用 C 语言开发的应用链接，用 Python 扩展和控制该应用．

### 学习 Python 的注意事项

-   目前主要使用的 Python 版本是 Python 3.7 及以上的版本，Python 2 和 Python 3.6 及以前的 Python 3 已经 [不被支持](https://devguide.python.org/versions/#unsupported-versions)，但仍被一些老旧系统与代码所使用．本文将 **介绍较新版本的 Python**．如果遇到 Python 2 代码，可以尝试 [`2to3`](https://docs.python.org/zh-cn/3/library/2to3.html) 程序将 Python 2 代码转换为 Python 3 代码．
-   Python 的设计理念和语法结构 **与一些其他语言的差异较大**，隐藏了许多底层细节，所以呈现出实用而优雅的风格．
-   Python 是高度动态的解释型语言，因此其 **程序运行速度相对较慢**，尤其在使用其内置的 `for` 循环语句时．在使用 Python 时，应尽量使用 `filter`、`map` 等内置函数，或使用 [列表生成](https://www.pythonforbeginners.com/basics/list-comprehensions-in-python) 语法的手段来提高程序性能．

## 环境搭建

参见 [Python 3](../tools/compiler.md#python-3)．或者：

-   Windows：也可以在 Microsoft Store 中免费而快捷地获取 Python．

-   macOS/Linux：通常情况下，大部分的 Linux 发行版中已经自带了 Python．如果只打算学习 Python 语法，并无其它开发需求，不必另外安装 Python．

    ???+ warning "注意"
        在一些默认安装（指使用软件包管理器安装）Python 的系统（如 Unix 系统）中，应在终端中运行 `python3` 打开 Python 3 解释器．[^ref1]

此外，也可以通过 venv、conda、Nix 等工具管理 Python 工具链和 Python 软件包，创建隔离的虚拟环境，避免出现依赖问题．

作为一种解释型语言，Python 的执行方式和 C++ 有所不同，这种差异在使用 IDE 编程时往往得不到体现，因此这里需要强调一下运行程序的不同方式．

当在命令行中键入 `python3` 或刚刚打开 IDLE 时，你实际进入了一种交互式的编程环境，也称「REPL」（「读取 - 求值 - 输出」循环），初学者可以在这里输入语句并立即看到结果，这让验证一些语法变得极为容易，我们也将在后文中大量使用这种形式．

但若要编写完整的程序，你最好还是新建一个文本文件（通常后缀为 `.py`），然后在命令行中执行 `python3 filename.py`，就能够运行代码看到结果了．

### 一些平台提供的 Python 版本

| 系统名/版本           | python 版本               |
| ---------------- | ----------------------- |
| Noi Linux 2.0    | 3.8.0, Include requests |
| Luogu 评测机        | 3.11.5, NumPy 1.25.2    |
| 基于 Hydro 的 OJ    | 3.8.0+ Include NumPy    |
| Ubuntu 22.04（内置） | 3.10.4                  |
| 微软商店             | 最新正式版                   |

???+ warning "注意"
    本表格在本文撰写时（2025/01/15）时有效，建议前往相关平台重新查证．

目前国内关于 **源码** 的镜像缓存主要是 [北京交通大学自由与开源软件镜像站](https://mirror.bjtu.edu.cn/python/) 和 [华为开源镜像站](https://repo.huaweicloud.com/python/)，可以到那里尝试下载 Python 安装文件．

## 使用 `pip` 安装第三方库

Python 的生命力很大程度上来自于丰富的第三方库，编写一些实用程序时「调库」是常规操作，`pip` 是首选的安装第三方库的程序．自 Python 3.4 版本起，它被默认包含在 Python 二进制安装程序中．

`pip` 中的第三方库主要存储在 [Python 包索引（PyPI）](https://pypi.org/) 上，用户也可以指定其它第三方库的托管平台．使用方法可参照 [pypi 镜像使用帮助 - 清华大学开源软件镜像站](https://mirrors.tuna.tsinghua.edu.cn/help/pypi/) 等使用帮助．你可以在 [MirrorZ](https://mirrorz.org/list/pypi) 上获取更多 PyPI 镜像源．

???+ info "使用清华大学开源镜像站安装一个包"
    ```sh
    pip install -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple <some-package>
    ```

## 基本语法

Python 的语法简洁而易懂，也有许多官方和第三方文档与教程．这里仅介绍一些对 OIer 比较实用的语言特性，你可以在 [Python 文档](https://docs.python.org/zh-cn/3/) 和 [Python Wiki](https://wiki.python.org/moin/) 等网页上了解更多关于 Python 的教程．

### 注释

加入注释并不会对代码的运行产生影响，但加入注释可以使代码更加易懂易用．

```python
# 用 # 字符开头的是单行注释

"""
跨多行字符串会用三引号
（即三个单引号或三个双引号）
包裹，但也通常被用于注释
"""
```

加入注释代码并不会对代码产生影响．我们鼓励加入注释来使代码更加易懂易用．

### 基本数据类型

#### 一切皆对象

在 Python 中，你无需事先声明变量名及其类型，直接赋值即可创建各种类型的变量：

```pycon
>>> x = -3  # 语句结尾不用加分号
>>> x
-3
>>> f = 3.1415926535897932384626; f  # 实在想加分号也可以，这里节省了一行
3.141592653589793
>>> s1 = "O"
>>> s1  # 在 Python 中双引号和单引号的作用相同
'O'
>>> b = 'A' == 65  # 'A' 和 65 不是一个数据类型，所以不相等
>>> b  # True, False 首字母均大写
False
>>> True + 1 == 2 and not False != 0  # Python 中的表达式中大多使用单词，但是也支持符号
True
```

但这不代表 Python 没有类型的概念，实际上解释器会根据赋值或运算自动推断变量类型，你可以使用内置函数 `type()` 查看这些变量的类型：

```pycon
>>> type(x)
<class 'int'>
>>> type(f)
<class 'float'>
>>> type(s1)  # 请注意，不要给字符串起名为 str，否则 str 对象会被篡改
<class 'str'>
>>> type(b)
<class 'bool'>
```

???+ note "[**内置函数**](https://docs.python.org/zh-cn/3/library/functions.html) 是什么？"
    在 C/C++ 中，很多常用函数都分散在不同的头文件中，但 Python 的解释器内置了许多实用且通用的函数，你可以直接使用而无需注意它们的存在，但这也带来了小问题，这些内置函数的名称多为常见单词，你需要注意避免给自己的变量起相同的名字，否则可能会产生奇怪的结果．

正如我们所看到的，Python 内置有整数、浮点数、字符串和布尔类型，可以类比为 C++ 中的 `int`，`float`，`string` 和 `bool`．但有一些明显的不同之处，比如没有 `char` 字符类型，也没有 `double` 类型（但 `float` 其实对应 C 中的双精度），如果需要更精确的浮点运算，可以使用标准库中的 [decimal](https://docs.python.org/zh-cn/3/library/decimal.html) 模块，如果需要用到复数，Python 还内置了 `complex` 类型（而这也意味着最好不要给变量起名为 `complex`）．
可以看到这些类型都以 `class` 开头，而这正是 Python 不同于 C++ 的关键之处，Python 程序中的所有数据都是由对象或对象间关系来表示的，函数是对象，类型本身也是对象：

```pycon
>>> type(int)
<class 'type'>
>>> type(pow)  # 求幂次的内置函数，后文会介绍
<class 'builtin_function_or_method'>
>>> type(type)  # type() 也是内置函数，但有些特殊，感兴趣可自行查阅
<class 'type'>
```

你或许会觉得这些概念一时难以理解且没有用处，所以我们暂时不再深入，在后文的示例中你或许能慢慢体会到，Python 的对象提供了强大的方法，我们在编程时应当优先考虑围绕对象而不是过程进行操作，这会让我们的代码显得更加紧凑明晰．

#### 数字运算

有人说，你可以把你系统里装的 Python 当作一个多用计算器，这是事实．  
在交互模式下，你可以在提示符 `>>>` 后面输入一个表达式，就像其他大部分语言（如 C++）一样使用运算符 `+`、`-`、`*`、`/`、`%` 来对数字进行运算，也可以使用 `()` 来进行符合结合律的分组，读者可以自行试验，在这里我们仅展示与 C++ 差异较大的部分：

```pycon
>>> 5.0 * 6  # 浮点数的运算结果是浮点数
30.0
>>> 15 / 3  # 与 C/C++ 不同，除法永远返回浮点 float 类型
5.0
>>> 5 / 100000  # 位数太多，结果显示成科学计数法形式
5e-05
>>> 5 // 3 # 使用整数除法（地板除）则会向下取整，输出整数类型
1
>>> -5 // 3 # 符合向下取整原则，注意这与 C/C++ 不同
-2
>>> 5 % 3 # 取模
2
>>> -5 % 3 # 负数取模结果一定是非负数，这点也与 C/C++ 不同，不过都满足 (a//b)*b+(a%b)==a 
1
>>> x = abs(-1e4)  # 求绝对值的内置函数
>>> x += 1  # 没有自增/自减运算符
>>> x  # 科学计数法默认为 float
10001.0
```

在上面的实践中可以发现，除法运算（`/`）永远返回浮点类型（在 Python 2 中返回整数）．如果你想要整数或向下取整的结果的话，可以使用整数除法（`//`）．同样的，你也可以像 C++ 中一样，使用模（`%`）来计算余数，科学计数法的形式也相同．

特别地，Python 用 `**` 即可进行幂运算，还通过内置的 `pow(a, b, mod)` 提供了 [快速幂](../math/binary-exponentiation.md) 的高效实现．

```pycon
>>> 3 ** 4 # 幂运算
81
>>> 2 ** 512
13407807929942597099574024998205846127479365820592393377723561443721764030073546976801874298166903427690031858186486050853753882811946569946433649006084096
>>> pow(2, 512, int(1e4)) # 即 2**512 % 10000 的快速实现, 1e4 是 float 所以要转 int
4096
>>> 2048 ** 2048 # 在IDLE里试试大整数？
>>> 0.1 + 0.1 + 0.1 - 0.3 == 0.  # 和 C/C++ 一样需要注意浮点数不能直接判相等
False
```

#### 数据类型判断

对于一个变量，可以使用 `type(object)` 返回变量的类型，例如 `type(8)` 和 `type('a')` 的值分别为 `<class 'int'>` 和 `<class 'str'>`．

#### [基本输入输出](https://docs.python.org/zh-cn/3/tutorial/inputoutput.html)

Python 中的输入输出主要通过内置函数 `input()` 和 `print()` 完成，`print()` 的用法十分符合直觉：

```pycon
>>> a = [1,2,3]; print(a[-1])  # 打印时默认末尾换行
3
>>> print(ans[0], ans[1])  # 可以输出任意多个变量，默认以空格间隔
1 2
>>> print(a[0], a[1], end='')  # 令 end='', 使末尾不换行
1 2>>>
>>> print(a[0], a[1], sep=', ')  # 令 sep=', '，改变间隔样式
1, 2
>>> print(str(a[0]) + ', ' + str(a[1]))  # 输出同上，但是手动拼接成一整个字符串
```

`input()` 函数的行为接近 C++ 中的 `getline()`，即将一整行作为字符串读入，且末尾没有换行符．

```pycon
>>> s = input('请输入一串数字: '); s  # 自己调试时可以向 input() 传入字符串作为提示
请输入一串数字: 1 2 3 4 5 6
'1 2 3 4 5 6'
```

#### 字符串

Python 3 提供了强大的基于 [Unicode](https://docs.python.org/zh-cn/3/howto/unicode.html#unicode-howto) 的字符串类型，使用起来和 C++ 中的 `string` 类似，一些概念如转义字符也都相通，除了加号拼接和索引访问，还额外支持数乘 `*` 重复字符串，和 `in` 操作符．

```pycon
>>> s1 = "O"  # 单引号和双引号都能包起字符串，有时可节省转义字符
>>> s1 += 'I-Wiki'  # 为和 C++ 同步建议使用双引号 
>>> 'OI' in s1  # 检测子串很方便
True
>>> len(s1)  # 类似 C++ 的 s.length()，但更通用
7
>>> s2 = """ 感谢你的阅读
... 欢迎参与贡献!
"""   # 使用三重引号的字符串可以跨越多行
>>> s1 + s2 
'OI-Wiki 感谢你的阅读\n欢迎参与贡献!'
>>> print(s1 + s2)  # 这里使用了 print() 函数打印字符串
OI-Wiki 感谢你的阅读
欢迎参与贡献!
>>> s2[2] * 2 + s2[3] + s2[-1]  # 负数索引从右开始计数，加上 len(s)，相当于模 n 的剩余类环
'谢谢你!'
>>> s1[0] = 'o'  # str 是不可变类型，不能原地修改，其实 += 也是创建了新的对象
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'str' object does not support item assignment
```

Python 支持多种复合数据类型，可将不同值组合在一起．最常用的 `list`，类型是用方括号标注、逗号分隔的一组值．例如，`[1, 2, 3]` 和 `['a','b','c']` 都是列表．

除了索引，字符串还支持*切片*，它的设计非常精妙，格式为 `s[左闭索引:右开索引:步长]`：

```pycon
>>> s = 'OI-Wiki 感谢你的阅读\n欢迎参与贡献!'
>>> s[:8]  # 省略左闭索引则从头开始
'OI-Wiki '
>>> s[8:14]  # 左闭右开设计的妙处，长度为 14-8=6，还和上一个字符串无缝衔接
'感谢你的阅读'
>>> s[-4:]  # 省略右开索引则直到结尾
'与贡献!'
>>> s[8:14:2]  # 步长为2
'感你阅'
>>> s[::-1]  # 步长为 -1 时，获得了反转的字符串
'!献贡与参迎欢\n读阅的你谢感 ikiW-IO'
>>> s  # 但原来的字符串并未改变
'OI-Wiki 感谢你的阅读\n欢迎参与贡献!'
```

在最新的 Python 3 版本中，字符串是以 Unicode 编码的，也就是说，Python 的字符串支持多语言．[^ref2]在 Python 中，可以对一个 Unicode 字符使用内置函数 `ord()` 将其转换为对应的 Unicode 编码，逆向的转换使用内置函数 `chr()`．C/C++ 中 `char` 类型也可以和 对应的 ASCII 码互转．

如果想把数字转换成对应的字符串，可以使用内置函数 `str()`，反之可以使用 `int()` 和 `float()`，你可以类比为 C/C++ 中的强制类型转换，但括号不是加在类型上而是作为函数的一部分括住参数．

Python 的字符串类型提供了许多强大的方法，包括计算某字符的索引与出现次数，转换大小写等等，这里就不一一列举，强烈建议查看 [官方文档](https://docs.python.org/zh-cn/3/library/stdtypes.html#text-sequence-type-str) 熟悉常用方法，遇到字符串操作应当首先考虑使用这些方法而非自力更生．

### 创建数组

从 C++ 转过来的同学可能很迷惑怎么在 Python 中创建数组，这里就介绍在 Python 开「数组」的语法，需要强调我们介绍的其实是几种 [序列类型](https://docs.python.org/zh-cn/3/library/stdtypes.html#iterator-types)，和 C 的数组有着本质区别，而更接近 C++ 中的 `vector`．

#### 使用 `list`

列表（`list`）大概是 Python 中最常用也最强大的序列类型，列表中可以存放任意类型的元素，包括嵌套的列表，这符合数据结构中「广义表」的定义．请注意不要将其与 C++ STL 中的双向链表 [`list`](./csl/sequence-container.md#list) 混淆，故本文将使用「列表」而非 `list` 以免造成误解．

```pycon
>>> []  # 创建空列表，注意列表使用方括号
[]
>>> nums = [0, 1, 2, 3, 5, 8, 13]; nums  # 初始化列表，注意整个列表可以直接打印
[0, 1, 2, 3, 5, 8, 13]
>>> nums[0] = 1; nums  # 支持索引访问，支持修改元素
[1, 1, 2, 3, 5, 8, 13]
>>> nums.append(nums[-2]+nums[-1]); nums  # append() 同 vector 的 push_back()，也都没有返回值
[1, 1, 2, 3, 5, 8, 13, 21]
>>> nums.pop()  # 弹出并返回末尾元素，可以当栈使用；其实还可指定位置，默认是末尾
21
>>> nums.insert(0, 1); nums  # 同 vector 的 insert(position, val)
[1, 1, 1, 2, 3, 5, 8, 13]
>>> nums.remove(1); nums  # 按值移除元素（只删第一个出现的），若不存在则抛出错误
[1, 1, 2, 3, 5, 8, 13]
>>> len(nums)  # 求列表长度，类似 vector 的 size()，但 len() 是内置函数
7
>>> nums.reverse(); nums  # 原地逆置
[13, 8, 5, 3, 2, 1, 1]
>>> sorted(nums)  # 获得排序后的列表
[1, 1, 2, 3, 5, 8, 13]
>>> nums  # 但原来的列表并未排序
[13, 8, 5, 3, 2, 1, 1]
>>> nums.sort(); nums  # 原地排序，可以指定参数 key 作为排序标准
[1, 1, 2, 3, 5, 8, 13]
>>> nums.count(1)  # 类似 std::count()
2
>>> nums.index(1)  # 返回值首次出现项的索引号，若不存在则抛出错误
0
>>> nums.clear(); nums  # 同 vector 的 clear()
```

以上示例展现了列表与 `vector` 的相似之处，`vector` 中常用的操作一般也都能在列表中找到对应方法，不过某些方法如 `len()`,`sorted()` 会以内置函数的面目出现，而 STL 算法中的函数如 `find()`,`count()`,`max_element()`,`sort()`,`reverse()` 在 Python 中又成了对象的方法，使用时需要注意区分，更多方法请参见官方文档的 [列表详解](https://docs.python.org/zh-cn/3/tutorial/datastructures.html#more-on-lists)．下面将展示列表作为 Python 的基本序列类型的一些强大功能：

Python 支持多种复合数据类型，可将不同值组合在一起．最常用的 `list`，类型是用方括号标注、逗号分隔的一组值．例如，`[1, 2, 3]` 和 `['a','b','c']` 都是列表．

```pycon
>>> lst = [1, '1'] + ["2", 3.0]  # 列表直接相加生成一个新列表
>>> lst  # 这里存放不同的类型只是想说明可以这么做，但这不是好的做法
[1, '1', '2', 3.0]
>>> 3 in lst  # 实用的成员检测操作，字符串也有该操作且还支持子串检测
True
>>> [1, '1'] in lst  # 仅支持单个成员检测，不会发现「子序列」
False
>>> lst[1:3] = [2, 3]; lst  # 切片并赋值，原列表被修改
[1, 2, 3, 3.0]
>>> lst[::-1]  # 获得反转后的新列表
[3.0, 3, 2, 1]
>>> lst *= 2; lst  # 数乘拼接
[1, 2, 3, 3.0, 1, 2, 3, 3.0]
>>> del lst[4:]; lst  # 也可写 lst[4:] = []，del 语句不止可以用于删除序列中元素
[1, 2, 3, 3.0]
```

以上示例展现了列表作为序列的一些常用操作，可以看出许多操作如切片是与字符串相通的，但字符串是「不可变序列」而列表是「可变序列」，故可以通过切片灵活地修改列表．在 C/C++ 中我们往往会通过循环处理字符数组，下面将展示如何使用 [「列表推导式」](https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions) 在字符串和列表之间转换：

```pycon
>>> # 建立一个 [65, 70) 区间上的整数数组，range 也是一种类型，可看作左闭右开区间，第三个参数为步长可省略
>>> nums = list(range(65,70))  # 记得 range 外面还要套一层 list()
[65, 66, 67, 68, 69]
>>> lst = [chr(x) for x in nums]  # 列表推导式的典型结构，[exp for var in iterable if cond]
>>> lst  # 上两句可以合并成 [chr(x) for x in range(65,70)]
['A', 'B', 'C', 'D', 'E']
>>> s = ''.join(lst); s # 用空字符串 '' 拼接列表中的元素生成新字符串
'ABCDE'
>> list(s)  # 字符串生成字符列表
['A', 'B', 'C', 'D', 'E']
>>> # 如果你不知道有 s.lower() 方法就可能写出下面这样新瓶装旧酒的表达式
>>> ''.join([chr(ord(ch) - 65 + 97) for ch in s if ch >= 'A' and ch <= 'Z'])  
'abcde'
```

下面演示一些在 OI 中更常见的场景，比如二维「数组」：

```pycon
>>> vis = [[0] * 3] * 3  # 开一个 3*3 的全 0 数组
>>> vis 
[[0, 0, 0], [0, 0, 0], [0, 0, 0]]
>>> vis[0][0] = 1; vis  # 怎么会把其他行也修改了？
[[1, 0, 0], [1, 0, 0], [1, 0, 0]]
>>> # 先来看下一维列表的赋值
>>> a1 = [0, 0, 0]; a2 = a1; a3 = a1[:]  # 列表也可以直接被赋给新的变量
>>> a1[0] = 1; a1  # 修改列表 a1，似乎正常
[1, 0, 0]
>>> a2  # 怎么 a2 也被改变了
[1, 0, 0]
>>> a3  # a3 没有变化
[0, 0, 0]
>>> id(a1) == id(a2) and id(a1) != id(a3)  # 内置函数 id() 给出对象的「标识值」，可类比为地址，地址相同说明是一个对象
True
>>> vis2 = vis[:]  # 拷贝一份二维列表
>>> vis[0][1] = 2; vis  # vis 会被批量修改
>>> [[1, 2, 0], [1, 2, 0], [1, 2, 0]]
>>> vis2  # 但 vis2 是切片拷贝还是被改了
>>> [[1, 2, 0], [1, 2, 0], [1, 2, 0]]
>>> id(vis) != id(vis2)  # vis 和 vis2 不是一个对象
True
>>> # vis2 虽然不是 vis 的引用，但其中对应行都指向相同的对象
>>> [id(vis[i]) == id(vis2[i]) for i in range(3)]
[True, True, True]
>>> # 回看二维列表自身
>>> [id(x) for x in vis]  # 具体数字和这里不一样但三个值一定相同，说明是三个相同对象
[139760373248192, 139760373248192, 139760373248192]
```

其实有一个重要的事实，Python 中赋值只传递了引用而非创建新值，你可以创建不同类型的变量并赋给新变量，验证发现二者的标识值是相同的，只不过直到现在我们才介绍了列表这一种可变类型，而给数字、字符串这样的不可变类型赋新值时实际上创建了新的对象，故而前后两个变量互不干扰．但列表是可变类型，所以我们修改一个列表的元素时，另一个列表由于指向同一个对象所以也被修改了．创建二维数组也是类似的情况，示例中用乘法创建二维列表相当于把 `[0]*3` 这个一维列表重复了 3 遍，所以涉及其中一个列表的操作会同时影响其他两个列表．更不幸的是，在将二维列表赋给其他变量的时候，就算用切片来拷贝，也只是「浅拷贝」，其中的元素仍然指向相同的对象，解决这个问题需要使用标准库中的 [`deepcopy`](https://docs.python.org/3/library/copy.html)，或者尽量避免整个赋值二维列表．不过还好，创建二维列表时避免创建重复的列表还是比较简单，只需使用「列表推导式」：

```pycon
>>> vis1 = [[0] * 3 for _ in range(3)]  # 把用不到的循环计数变量设为下划线 _ 是一种惯例
>>> # 但在 REPL 中 _ 默认指代上一个表达式输出的结果，故也可使用双下划线
>>> vis1
[[0, 0, 0], [0, 0, 0], [0, 0, 0]]
>>> [id(x) for x in vis1]  # 具体数字和这里不一样但三个值一定不同，说明是三个不同对象
[139685508981248, 139685508981568, 139685508981184]
>>> vis1[0][0] = 1
[[1, 0, 0], [0, 0, 0], [0, 0, 0]]
>>> a2[0][0] = 10  # 访问和赋值二维数组
```

我们未讲循环的用法就先介绍了列表推导式，这是由于 Python 是高度动态的解释型语言，因此其程序运行有大量的额外开销．尤其是 **for 循环在 Python 中运行的奇慢无比**．因此在使用 Python 时若想获得高性能，尽量使用列表推导式，或者 `filter`,`map` 等内置函数直接操作整个序列来避免循环，当然这还是要根据具体问题而定．

#### 使用 NumPy

??? note "什么是 NumPy"
    [NumPy](https://numpy.org/) 是著名的 Python 科学计算库，提供高性能的数值及矩阵运算．在测试算法原型时可以利用 NumPy 避免手写排序、求最值等算法．NumPy 的核心数据结构是 `ndarray`，即 n 维数组，它在内存中连续存储，是定长的．此外 NumPy 核心是用 C 编写的，运算效率很高．不过需要注意，它不是标准库的一部分，可以使用 `pip install numpy` 安装，但不保证 OI 考场环境中可用（参见文首 [Python 版本](#一些平台提供的-python-版本)）．

下面的代码将介绍如何利用 NumPy 建立多维数组并进行访问．

```pycon
>>> import numpy as np  # 请自行搜索 import 的意义和用法
>>> np.empty(3) # 开容量为 3 的空数组，注意没有初始化为 0
array([0.00000000e+000, 0.00000000e+000, 2.01191014e+180])
>>> np.zeros((3, 3)) # 开 3*3 的数组，并初始化为 0
array([[0., 0., 0.],
       [0., 0., 0.],
       [0., 0., 0.]])
>>> a1 = np.zeros((3, 3), dtype=int) # 开 3×3 的整数数组
>>> a1[0][0] = 1 # 访问和赋值
>>> a1[0, 0] = 1 # 更友好的语法
>>> a1.shape # 数组的形状
(3, 3)

>>> a1[:2, :2] # 取前两行、前两列构成的子阵，无拷贝
array([[1, 0],
       [0, 0]])

>>> a1[:, [0, 2]] # 获取第 1、3 列，无拷贝
array([[1, 0],
       [0, 0],
       [0, 0]])
>>> np.max(a1) # 获取数组最大值
1
>>> a1.flatten() # 将数组展平
array([1, 0, 0, 0, 0, 0, 0, 0, 0])

>>> np.sort(a1, axis = 1) # 沿行方向对数组进行排序，返回排序结果
array([[0, 0, 1],
       [0, 0, 0],
       [0, 0, 0]])
>>> a1.sort(axis = 1) # 沿行方向对数组进行原地排序
```

#### 使用 `array`

[`array`](https://docs.python.org/zh-cn/3/library/array.html) 是 Python 标准库提供的一种高效数值数组，可以紧凑地表示基本类型值的数组，但不支持数组嵌套，也很少见到有人使用它，这里只是顺便提一下．

若无特殊说明，后文出现「数组」一般指「列表」．

### [输入输出](https://docs.python.org/zh-cn/3/tutorial/inputoutput.html)

Python 中的输入输出主要通过内置函数 `input()` 和 `print()` 完成．前文已经介绍过，下面介绍进阶用法．

#### 格式化输出

算法竞赛中通常只涉及到基本的数值和字符串输出，`print()` 已基本足够，只有当涉及到浮点数位数时需要用到格式化字符串输出．格式化有三种方法，第一种也是最老旧的方法是使用 `printf()` 风格的 `%` 操作符；另一种是利用 [`format` 函数](https://docs.python.org/3/library/string.html#formatstrings)；第三种是 Python 3.6 新增的 [f-string](https://docs.python.org/zh-cn/3/tutorial/inputoutput.html#formatted-string-literals)，最为简洁，但不保证考场中的 Python 版本足够新．详细丰富的说明可以参考 [这个网页](https://www.python-course.eu/python3_formatted_output.php)，尽管更推荐使用 `format()` 方法，但为了获得与 C 接近的体验，下面仅演示与 `printf()` 类似的老式方法：

```pycon
>>> pi = 3.1415926; print('%.4f' % pi)   # 格式为 %[flags][width][.precision]type
3.1416
>>> '%.4f - %8f = %d' % (pi, 0.1416, 3)  # 右边多个参数用 () 括住，后面会看到其实是「元组」 
'3.1416 - 0.141600 = 3'
```

#### `split()` 函数

`input()` 函数的行为接近 C++ 中的 `getline()`，即将一整行作为字符串读入，且末尾没有换行符，但在算法竞赛中，常见的输入形式是一行输入多个数值，因此就需要使用字符串的 `split()` 方法并搭配列表推导式得到存放数值类型的列表，下面以输入 n 个数求平均值为例演示输入 n 个数得到「数组」的方法：

```pycon
>>> s = input('请输入一串数字: '); s  # 自己调试时可以向 input() 传入字符串作为提示
请输入一串数字: 1 2 3 4 5 6
'1 2 3 4 5 6'
>>> a = s.split(); a
['1', '2', '3', '4', '5', '6']
>>> a = [int(x) for x in a]; a
[1, 2, 3, 4, 5, 6]
>>> # 以上输入过程可写成一行 a = [int(x) for x in input().split()]
>>> sum(a) / len(a)  # sum() 是内置函数
3.5
```

有时题目会在每行输入固定几个数，比如边的起点、终点、权重，如果只用上面提到的方法就只能每次读入数组然后根据下标赋值，这时可以使用 Python 的「拆包」特性一次赋值多个变量：

```pycon
>>> u, v, w = [int(x) for x in input().split()]
1 2 4
>>> print(u,v,w)
1 2 4
```

题目中经常遇到输入 N 行的情况，可我们还没有讲最基本的循环语句，但 Python 强大的序列操作能在不使用循环的情况下应对多行输入，下面假设将各条边的起点、终点、权值分别读入三个数组：

```pycon
>>> N = 4; mat = [[int(x) for x in input().split()] for i in range(N)]
1 3 3 
1 4 1 
2 3 4 
3 4 1 
>>> mat  # 先按行读入二维数组
[[1, 3, 3], [1, 4, 1], [2, 3, 4], [3, 4, 1]]
>>> u, v, w = map(list, zip(*mat))   
# *将 mat 解包得到里层的多个列表
# zip() 将多个列表中对应元素聚合成元组，得到一个迭代器
# map(list, iterable) 将序列中的元素（这里为元组）转成列表
>>> print(u, v, w)  # 直接将 map() 得到的迭代器拆包，分别赋值给 u, v, w
[1, 1, 2, 3] [3, 4, 3, 4] [3, 1, 4, 1]
```

上述程序实际上相当于先读入一个 N 行 3 列的矩阵，然后将其转置成 3 行 N 列的矩阵，也就是外层列表中嵌套了 3 个列表，最后将代表这起点、终点、权值的 3 个列表分别赋值给 u, v, w．内置函数 [`zip()`](https://docs.python.org/zh-cn/3/library/functions.html#zip) 可以将多个等长序列中的对应元素拼接在「元组」内，得到新序列．而 `map()` 其实是函数式编程的一种操作，它将一个给定函数作用于 `zip()` 所产生序列的元素，这里就是用 `list()` 将元组变成列表．你可以自行练习使用 `*` 和 [`zip()`](https://docs.python.org/zh-cn/3/library/functions.html#zip)，[`map()`](https://docs.python.org/zh-cn/3/library/functions.html#map) 以理解其含义．需要注意的是 Python 3 中 `zip()` 和 `map()` 创建的不再返回列表而是返回迭代器，这里暂不解释它们之间的异同，你可以认为迭代器可以产生列表中的各个元素，用 `list()` 套住迭代器就能生成列表．

#### [文件读写](https://docs.python.org/3/reference/compound_stmts.html#the-with-statement)

Python 内置函数 [`open()`](https://docs.python.org/3/library/functions.html#open) 用于文件读写，为了防止读写过程中出错导致文件未被正常关闭，这里只介绍使用 [`with`](https://docs.python.org/3/reference/compound_stmts.html#the-with-statement) 语句的安全读写方法：

```python
a = []
with open("in.txt") as f:
    N = int(f.readline())  # 读入第一行的 N
    a[len(a) :] = [[int(x) for x in f.readline().split()] for i in range(N)]

with open("out.txt", "w") as f:
    f.write("1\n")
```

关于文件读写的函数有很多，分别适用于不同的场景，由于 OI 赛事尚不支持使用 Python，这里从略．

### [控制流程](https://docs.python.org/zh-cn/3/tutorial/controlflow.html)

尽管我们已经学习了 Python 的许多特性，但到目前为止我们展示的 Python 代码都是单行语句，这掩盖了 Python 和 C 在代码风格上的重大差异：首先，Python 中不用 `{}` 而是用缩进表示块结构，如果缩进没有对齐会直接报错，如果 tab 和 空格混用也会报错；其次，块结构开始的地方比如 `if` 和 `for` 语句的行末要有冒号 `:`．这有助于代码的可读性，但你也可能怀念 C 那种自由的体验，毕竟如果复制粘贴时因为丢失缩进而不得不手动对齐是很恼人的．

#### 循环结构

列表推导式能在一行内高效地完成批量操作，但有时为了压行我们已经显得过分刻意，许多场景下还是只能使用循环结构，所以我们再以读入多行数据为例展示 Python 中的循环是如何编写的：

```python
# 请注意从现在开始我们不再使用 REPL，请自行复制多行数据
u, v, w = ([] for i in range(3))  # 多变量赋值
for i in range(4):  # 这里假设输入 4 行数据
    _u, _v, _w = [int(x) for x in input().split()]
    u.append(_u), v.append(_v), w.append(_w)
    # 不可进行类似 cin >> u[i] >> v[i] >> w[i] 的操作，因为必定超出列表当前的长度
    # 当然你可以选择初始化长度为 MAXN 的全 0 列表，不过需要记住真实长度并删掉多余元素
print(u, v, w)
```

需要注意，Python 中的 for 循环和 C/C++ 有较大的差别，其作用类似 C++ 11 引入的 [「基于范围的循环」](./new.md#基于范围的-for-循环)，实质是迭代序列中的元素，比如编写循环遍历数组下标需要迭代 `range(len(lst))`，而非真正定义起始和终止条件，所以使用起来并没有 C/C++ 灵活．

下面再用 while 循环展示行数不定的情况下如何输入：

```python
u, v, w = [], [], []  # 多变量赋值，其实同上
s = input()  # 注意 Python 中赋值语句不能放在条件表达式中
while s:  # 不能像 C 那样 while(!scanf())
    # 用切片拼接避免了 append()，注意列表推导式中又嵌套了列表
    u[len(u) :], v[len(v) :], w[len(w) :] = [[int(x)] for x in s.split()]
    s = input()
# Python 3.8 引入了 walrus operator 海象运算符后，你可以节省两行，但考场环境很可能不支持
while s := input():
    u[len(u) :], v[len(v) :], w[len(w) :] = [[int(x)] for x in s.split()]
print(u, v, w)
```

#### 选择结构

和 C/C++ 大同小异，一些形式上的差别都在下面的示例中有所展示，此外还需注意条件表达式中不允许使用赋值运算符（Python 3.8 以上可用 [`:=`](https://www.python.org/dev/peps/pep-0572/)），以及 [没有 switch 语句](https://docs.python.org/zh-cn/3/faq/design.html#why-isn-t-there-a-switch-or-case-statement-in-python)．

```python
# 条件表达式两侧无括号
if 4 >= 3 > 2 and 3 != 5 == 5 != 7:
    print("关系运算符可以连续使用")
    x = None or [] or -2
    print("&&  ||  !", "与  或  非", "and or not", sep="\n")
    print("善用 and/or 可节省行数")
    if not x:
        print("负数也是 True，不执行本句")
    elif x & 1:
        print("用 elif 而不是 else if\n" "位运算符与 C 相近，偶数&1 得 0，不执行本句")
    else:
        print("也有三目运算符") if x else print("注意结构")
```

#### 异常处理

尽管 C++ 中有 [try 块](https://zh.cppreference.com/w/cpp/language/try_catch) 用于异常处理，但竞赛中一般从不使用，而 Python 中常见的是 [EAFP](https://docs.python.org/zh-cn/3/glossary.html#term-eafp) 风格，故而代码中可能大量使用 [`try-except`](https://docs.python.org/zh-cn/3/reference/compound_stmts.html#the-try-statement) 语句，在后文介绍 `dict` 这一结构时还会用到，这里展示：

```python
s = "OI-wiki"
pat = "NOIP"
x = s.find(pat)  # find() 找不到返回 -1
try:
    y = s.index(pat)  # index() 找不到则抛出错误
    print(y)  # 这句被跳过
except ValueError:
    print("没找到")
    try:
        print(y)  # 此时 y 并没有定义，故又会抛出错误
    except NameError as e:
        print("无法输出 y")
        print("原因:", e)
```

### 内置容器

Python 内置了许多强大的容器类型，只有熟练使用并了解其特点才能真正让 Python 在算法竞赛中有用武之地，除了上面详细介绍的 `list`（列表），还有 `tuple`（元组）、[`dict`](https://docs.python.org/zh-cn/3/library/stdtypes.html#mapping-types-dict)（字典）和 `set`（集合）这几种类型．

元组可以简单理解成不可变的列表，不过还需注意「不可变」的内涵，如果元组中的某元素是可变类型比如列表，那么仍可以修改该列表的值，元组中存放的是对列表的引用所以元组本身并没有改变．元组的优点是开销较小且「[可哈希](https://docs.python.org/zh-cn/3/glossary.html)」，后者在创建字典和集合时非常有用．

```python
tup = tuple([[1, 2], 4])  # 由列表得到元组
# 等同于 tup = ([1,2], 4)
tup[0].append(3)
print(tup)
a, b = 0, "I-Wiki"  # 多变量赋值其实是元组拆包
print(id(a), id(b))
b, a = a, b
print(id(a), id(b))  # 你应该会看到 a, b 的 id 值现在互换了
# 这更说明 Python 中，变量更像是名字，赋值只是让其指代对象
```

字典就像 C++ STL 中的 [`map`](./csl/associative-container.md#map)（请注意和 Python 中内置函数 [`map()`](https://docs.python.org/zh-cn/3/library/functions.html#map) 区分）用于存储键值对，形式类似 [JSON](https://docs.python.org/3/library/json.html)，但 JSON 中键必须是字符串且以双引号括住，字典则更加灵活强大，可哈希的对象都可作为字典的键．需要注意 Python 几次版本更新后字典的特性有了较多变化，包括其中元素的顺序等，请自行探索．

```python
dic = {"key": "value"}  # 基本形式
dic = {chr(i): i for i in range(65, 91)}  # 大写字母到对应 ASCII 码的映射，注意断句
dic = dict(zip([chr(i) for i in range(65, 91)], range(65, 91)))  # 效果同上
dic = {dic[k]: k for k in dic}  # 将键值对逆转，for k in dic 迭代其键
dic = {v: k for k, v in dic.items()}  # 和上行作用相同，dic.items() 以元组存放单个键值对
dic = {
    k: v for k, v in sorted(dic.items(), key=lambda x: -x[1])
}  # 字典按值逆排序，用到了 lambda 表达式

print(dic["A"])  # 返回 dic 中 以 'A' 为键的项，这里值为65
dic["a"] = 97  # 将 d[key] 设为 value，字典中原无 key 就是直接插入
if "b" in dic:  # LBYL(Look Before You Leap) 风格
    print(dic["b"])  # 若字典中无该键则会出错，故先检查
else:
    dic["b"] = 98

# 经典场景 统计出现次数
# 新键不存在于原字典，需要额外处理
try:  # EAFP (Easier to Ask for Forgiveness than Permission) 风格
    cnter[key] += 1
except KeyError:
    cnter[key] = 1
```

集合就像 C++ STL 中的 [`set`](./csl/associative-container.md#set)，不会保存重复的元素，可以看成只保存键的字典．需要注意集合和字典都用 `{}` 括住，不过单用 `{}` 会创建空字典而不是空集合，这里就不再给出示例．

### 编写函数

Python 中定义函数无需指定参数类型和返回值类型，无形中为 OI 选手减少了代码量

```python
def add(a, b):
    return a + b  # 动态类型的优势，a 和 b 也可以是字符串


def add_no_swap(a, b):
    print("in func #1:", id(a), id(b))
    a += b
    b, a = a, b
    print("in func #2:", id(a), id(b))  # a, b 已交换
    return a, b  # 返回多个值，其实就是返回元组，可以拆包接收


lst1 = [1, 2]
lst2 = [3, 4]
print("outside func #1:", id(lst1), id(lst2))
add_no_swap(lst1, lst2)
# 函数外 lst1, lst2 并未交换
print("outside func #2:", id(lst1), id(lst2))
# 不过值确实已经改变
print(lst1, lst2)
```

#### 默认参数

Python 中函数的参数非常灵活，有关键字参数、可变参数等，但在算法竞赛中这些特性的用处并不是很大，这里只介绍一下默认参数，因为 C++ 中也有默认参数，且在 Python 中使用默认参数很有可能遇到坑．例如如下代码．

```python
def append_to(element, to=[]):
    to.append(element)
    return to


lst1 = append_to(12)
lst2 = append_to(42)
print(lst1, lst2)

# 你可能以为输出是 [12] [42]
# 但运行结果其实是 [12, 42] [12, 42]
```

之所以出现以上的运行结果，是因为默认参数的值仅仅在函数定义的时候赋值一次，对于可变对象（如列表、字典、集合），所有调用会共享同一个对象，`lst1` 和 `lst2` 实际上都指向内存中同一个默认列表对象．因此，第二次调用后，这个共享列表的内容被修改为 `[12, 42]`．所以函数的默认参数的值应该设为不可变对象，使用 `None` 占位是一种最佳实践：

```python
def append_to(element, to=None):
    if to is None:
        to = []
    to.append(element)
    return to


lst1 = append_to(12)
lst2 = append_to(42)
print(lst1, lst2)

# 运行结果为 [12] [42]
```

#### 类型标注

Python 是一个动态类型检查的语言，以灵活但隐式的方式处理类型，Python 解释器仅仅在运行时检查类型是否正确，并且允许在运行时改变变量类型，俗话说「动态类型一时爽，代码重构火葬场」，程序中的一些错误可能在运行时才会暴露：

```pycon
>>> if False:
...     1 + "two"  # This line never runs, so no TypeError is raised
... else:
...     1 + 2
...
3

>>> 1 + "two"  # Now this is type checked, and a TypeError is raised
TypeError: unsupported operand type(s) for +: 'int' and 'str'
```

Python 3.5 后引入了类型标注，允许设置函数参数和返回值的类型，但只是作为提示，并没有实际的限制作用，需要静态检查工具才能排除这类错误（例如 [PyCharm](https://www.jetbrains.com/pycharm/) 和 [Mypy](http://mypy-lang.org/)），所以显得有些鸡肋，对于 OIer 来说更是只需了解，可按如下方式对函数的参数和返回值设置类型标注：

```python
def headline(
    text,  # type: str
    width=80,  # type: int
    fill_char="-",  # type: str
):  # type: (...) -> str
    return f"{text.title()}".center(width, fill_char)


print(headline("type comments work", width=40))
```

除了函数参数，变量也是可以类型标注的，你可以通过调用 `__annotations__` 来查看函数中所有的类型标注．变量类型标注赋予了 Python 静态语言的性质，即声明与赋值分离：

```pycon
>>> nothing: str
>>> nothing
NameError: name 'nothing' is not defined

>>> __annotations__
{'nothing': <class 'str'>}
```

## 装饰器

装饰器是一个函数，接受一个函数或方法作为其唯一的参数，并返回一个新函数或方法，其中整合了修饰后的函数或方法，并附带了一些额外的功能．简而言之，可以在不修改函数代码的情况下，增加函数的功能．相关知识可以参考 [官方文档](https://docs.python.org/3/glossary.html#term-decorator)．

部分装饰器在竞赛中非常实用，比如 [`lru_cache`](https://docs.python.org/3/library/functools.html#functools.lru_cache)，可以为函数自动增加记忆化的能力，在递归算法中非常实用：

`@lru_cache(maxsize=128,typed=False)`

-   传入的参数有 2 个：`maxsize` 和 `typed`，如果不传则 `maxsize` 的默认值为 128，`typed` 的默认值为 `False`．
-   其中 `maxsize` 参数表示的是 LRU 缓存的容量，即被装饰的方法的最大可缓存结果的数量．如果该参数值为 128，则表示被装饰方法最多可缓存 128 个返回结果；如果 `maxsize` 传入为 `None` 则表示可以缓存无限个结果．
-   如果 `typed` 设置为 `True`，不同类型的函数参数将被分别缓存，例如，`f(3)` 和 `f(3.0)` 会缓存两次．

以下是使用 `lru_cache` 优化计算斐波那契数列的例子：

```python
@lru_cache(maxsize=None)
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)
```

## 常用内置库

在这里介绍一些写算法可能用得到的内置库，具体用法可以自行搜索或者阅读 [官方文档](https://docs.python.org/3/library/index.html)．

| 库名                                                                  | 用途             |
| ------------------------------------------------------------------- | -------------- |
| [`array`](https://docs.python.org/3/library/array.html)             | 定长数组           |
| [`argparse`](https://docs.python.org/3/library/argparse.html)       | 命令行参数处理        |
| [`bisect`](https://docs.python.org/3/library/bisect.html)           | 二分查找           |
| [`collections`](https://docs.python.org/3/library/collections.html) | 有序字典、双端队列等数据结构 |
| [`fractions`](https://docs.python.org/3/library/fractions.html)     | 有理数            |
| [`heapq`](https://docs.python.org/3/library/heapq.html)             | 基于堆的优先级队列      |
| [`io`](https://docs.python.org/3/library/io.html)                   | 文件流、内存流        |
| [`itertools`](https://docs.python.org/3/library/itertools.html)     | 迭代器            |
| [`math`](https://docs.python.org/3/library/math.html)               | 数学函数           |
| [`os.path`](https://docs.python.org/3/library/os.html)              | 系统路径等          |
| [`random`](https://docs.python.org/3/library/random.html)           | 随机数            |
| [`re`](https://docs.python.org/3/library/re.html)                   | 正则表达式          |
| [`struct`](https://docs.python.org/3/library/struct.html)           | 转换结构体和二进制数据    |
| [`sys`](https://docs.python.org/3/library/sys.html)                 | 系统信息           |

## 从例题对比 C++ 与 Python

??? note "[例题 洛谷 P4779【模板】单源最短路径（标准版）](https://www.luogu.com.cn/problem/P4779)"
    给定一个 $n(1 \leq n \leq 10^5)$ 个点、$m(1 \leq m \leq 2\times 10^5)$ 条有向边的带非负权图，请你计算从 $s$ 出发，到每个点的距离．数据保证能从 $s$ 出发到任意点．

### 声明常量

=== "C++"
    ```cpp
    #include <cstdio>
    #include <cstring>
    #include <queue>
    #include <vector>
    using namespace std;
    constexpr int N = 1e5 + 5, M = 2e5 + 5;
    ```

=== "Python"
    ```python
    try:  # 引入优先队列模块
        import Queue as pq  # python version < 3.0
    except ImportError:
        import queue as pq  # python3.*
    
    N = int(1e5 + 5)
    M = int(2e5 + 5)
    INF = 0x3F3F3F3F
    ```

### 声明前向星结构体和其它变量

=== "C++"
    ```cpp
    struct qxx {
      int nex, t, v;
    };
    
    qxx e[M];
    int h[N], cnt;
    
    void add_path(int f, int t, int v) { e[++cnt] = qxx{h[f], t, v}, h[f] = cnt; }
    
    using pii = pair<int, int>;
    priority_queue<pii, vector<pii>, greater<pii>> q;
    int dist[N];
    ```

=== "Python"
    ```python
    class qxx:  # 前向星类（结构体）
        def __init__(self):
            self.nex = 0
            self.t = 0
            self.v = 0
    
    
    e = [qxx() for i in range(M)]  # 链表
    h = [0 for i in range(N)]
    cnt = 0
    
    dist = [INF for i in range(N)]
    q = pq.PriorityQueue()  # 定义优先队列，默认第一元小根堆
    
    
    def add_path(f, t, v):  # 在前向星中加边
        # 如果要修改全局变量，要使用 global 来声明
        global cnt, e, h
        # 调试时的输出语句，多个变量使用元组
        # print("add_path(%d,%d,%d)" % (f,t,v))
        cnt += 1
        e[cnt].nex = h[f]
        e[cnt].t = t
        e[cnt].v = v
        h[f] = cnt
    ```

### Dijkstra 算法

=== "C++"
    ```cpp
    void dijkstra(int s) {
      memset(dist, 0x3f, sizeof(dist));
      dist[s] = 0, q.push(make_pair(0, s));
      while (q.size()) {
        pii u = q.top();
        q.pop();
        if (dist[u.second] < u.first) continue;
        for (int i = h[u.second]; i; i = e[i].nex) {
          const int &v = e[i].t, &w = e[i].v;
          if (dist[v] <= dist[u.second] + w) continue;
          dist[v] = dist[u.second] + w;
          q.push(make_pair(dist[v], v));
        }
      }
    }
    ```

=== "Python"
    ```python
    def nextedgeid(u):  # 生成器，可以用在 for 循环里
        i = h[u]
        while i:
            yield i
            i = e[i].nex
    
    
    def dijkstra(s):
        dist[s] = 0
        q.put((0, s))
        while not q.empty():
            u = q.get()  # get 函数会顺便删除堆中对应的元素
            if dist[u[1]] < u[0]:
                continue
            for i in nextedgeid(u[1]):
                v = e[i].t
                w = e[i].v
                if dist[v] <= dist[u[1]] + w:
                    continue
                dist[v] = dist[u[1]] + w
                q.put((dist[v], v))
    ```

### 主函数

=== "C++"
    ```cpp
    int n, m, s;
    
    int main() {
      scanf("%d%d%d", &n, &m, &s);
      for (int i = 1; i <= m; i++) {
        int u, v, w;
        scanf("%d%d%d", &u, &v, &w);
        add_path(u, v, w);
      }
      dijkstra(s);
      for (int i = 1; i <= n; i++) printf("%d ", dist[i]);
      return 0;
    }
    ```

=== "Python"
    ```python
    if __name__ == "__main__":
        # 一行读入多个整数．注意它会把整行都读进来
        n, m, s = map(int, input().split())
        for i in range(m):
            u, v, w = map(int, input().split())
            add_path(u, v, w)
    
        dijkstra(s)
    
        for i in range(1, n + 1):
            print(dist[i], end=" ")
    
        print()
    ```

### 完整代码

=== "C++"
    ```cpp
    #include <cstdio>
    #include <cstring>
    #include <queue>
    #include <vector>
    using namespace std;
    constexpr int N = 1e5 + 5, M = 2e5 + 5;
    
    struct qxx {
      int nex, t, v;
    };
    
    qxx e[M];
    int h[N], cnt;
    
    void add_path(int f, int t, int v) { e[++cnt] = qxx{h[f], t, v}, h[f] = cnt; }
    
    using pii = pair<int, int>;
    priority_queue<pii, vector<pii>, greater<pii>> q;
    int dist[N];
    
    void dijkstra(int s) {
      memset(dist, 0x3f, sizeof(dist));
      dist[s] = 0, q.push(make_pair(0, s));
      while (q.size()) {
        pii u = q.top();
        q.pop();
        if (dist[u.second] < u.first) continue;
        for (int i = h[u.second]; i; i = e[i].nex) {
          const int &v = e[i].t, &w = e[i].v;
          if (dist[v] <= dist[u.second] + w) continue;
          dist[v] = dist[u.second] + w;
          q.push(make_pair(dist[v], v));
        }
      }
    }
    
    int n, m, s;
    
    int main() {
      scanf("%d%d%d", &n, &m, &s);
      for (int i = 1; i <= m; i++) {
        int u, v, w;
        scanf("%d%d%d", &u, &v, &w);
        add_path(u, v, w);
      }
      dijkstra(s);
      for (int i = 1; i <= n; i++) printf("%d ", dist[i]);
      return 0;
    }
    ```

=== "Python"
    ```python
    try:  # 引入优先队列模块
        import Queue as pq  # python version < 3.0
    except ImportError:
        import queue as pq  # python3.*
    
    N = int(1e5 + 5)
    M = int(2e5 + 5)
    INF = 0x3F3F3F3F
    
    
    class qxx:  # 前向星类（结构体）
        def __init__(self):
            self.nex = 0
            self.t = 0
            self.v = 0
    
    
    e = [qxx() for i in range(M)]  # 链表
    h = [0 for i in range(N)]
    cnt = 0
    
    dist = [INF for i in range(N)]
    q = pq.PriorityQueue()  # 定义优先队列，默认第一元小根堆
    
    
    def add_path(f, t, v):  # 在前向星中加边
        # 如果要修改全局变量，要使用 global 来声名
        global cnt, e, h
        # 调试时的输出语句，多个变量使用元组
        # print("add_path(%d,%d,%d)" % (f,t,v))
        cnt += 1
        e[cnt].nex = h[f]
        e[cnt].t = t
        e[cnt].v = v
        h[f] = cnt
    
    
    def nextedgeid(u):  # 生成器，可以用在 for 循环里
        i = h[u]
        while i:
            yield i
            i = e[i].nex
    
    
    def dijkstra(s):
        dist[s] = 0
        q.put((0, s))
        while not q.empty():
            u = q.get()
            if dist[u[1]] < u[0]:
                continue
            for i in nextedgeid(u[1]):
                v = e[i].t
                w = e[i].v
                if dist[v] <= dist[u[1]] + w:
                    continue
                dist[v] = dist[u[1]] + w
                q.put((dist[v], v))
    
    
    # 如果你直接运行这个 Python 代码（不是模块调用什么的）就执行命令
    if __name__ == "__main__":
        # 一行读入多个整数．注意它会把整行都读进来
        n, m, s = map(int, input().split())
        for i in range(m):
            u, v, w = map(int, input().split())
            add_path(u, v, w)
    
        dijkstra(s)
    
        for i in range(1, n + 1):
            # 两种输出语法都是可以用的
            print("{}".format(dist[i]), end=" ")
            # print("%d" % dist[i],end=' ')
    
        print()  # 结尾换行
    ```

## 参考文档

1.  [Python Documentation](https://www.python.org/doc/)
2.  [Python 官方中文教程](https://docs.python.org/zh-cn/3/tutorial/)
3.  [Learn Python3 In Y Minutes](https://learnxinyminutes.com/docs/python3/)
4.  [Real Python Tutorials](https://realpython.com/)
5.  [廖雪峰的 Python 教程](https://www.liaoxuefeng.com/wiki/1016959663602400/)
6.  [GeeksforGeeks: Python Tutorials](https://www.geeksforgeeks.org/python-programming-language/)

## 参考资料和注释

[^ref1]: [2. Python 解释器—Python 3 文档](https://docs.python.org/zh-cn/3/tutorial/interpreter.html#id1)

[^ref2]: [Unicode 指南—Python 3 文档](https://docs.python.org/zh-cn/3/howto/unicode.html#the-string-type)


## lang/reference.md

> 声明具名变量为引用，即既存对象或函数的别名．

引用可以看成是 C++ 封装的非空指针，可以用来传递它所指向的对象，在声明时必须指向对象．

引用不是对象，因此不存在引用的数组、无法获取引用的指针，也不存在引用的引用．

??? note "引用类型不属于对象类型"
    如果想让引用能完成一般的复制、赋值等操作，比如作为容器元素，则需要 [`reference_wrapper`](https://zh.cppreference.com/w/cpp/utility/functional/reference_wrapper)，通常维护一个非空指针实现．

引用主要分为两种，左值引用和右值引用．

??? note "左值和右值"
    对左值和右值的讲解，请参考 [值类别](./value-category.md) 页面．

## 左值引用 T&

通常我们会接触到的引用为左值引用，即绑定到左值的引用，同时 `const` 限定的左值引用可以绑定右值．以下是来自 [参考手册](https://zh.cppreference.com/w/cpp/language/reference) 的一段示例代码．

```cpp
#include <iostream>
#include <string>

int main() {
  std::string s = "Ex";
  std::string& r1 = s;
  const std::string& r2 = s;

  r1 += "ample";  // 修改 r1，即修改了 s
  // r2 += "!"; // 错误：不能通过到 const 的引用修改
  std::cout << r2 << '\n';  // 打印 r2，访问了s，输出 "Example"
}
```

左值引用最常用的地方是函数参数，用于避免不需要的拷贝．

```cpp
#include <iostream>
#include <string>

// 参数中的 s 是引用，在调用函数时不会发生拷贝
char& char_number(std::string& s, std::size_t n) {
  s += s;  // 's' 与 main() 的 'str'
           // 是同一对象，此处还说明左值也是可以放在等号右侧的
  return s.at(n);  // string::at() 返回 char 的引用
}

int main() {
  std::string str = "Test";
  char_number(str, 1) = 'a';  // 函数返回是左值，可被赋值
  std::cout << str << '\n';   // 此处输出 "TastTest"
}
```

## 右值引用 T&&（C++ 11）

右值引用是绑定到右值的引用，用于移动对象，也可以用于 **延长临时对象生存期**．

```cpp
#include <iostream>
#include <string>

using namespace std;

int main() {
  string s1 = "Test";
  // string&& r1 = s1; // 错误：不能绑定到左值，需要 std::move 或者 static_cast

  const string& r2 = s1 + s1;  // 可行：到常量的左值引用延长生存期
  // r2 += "Test"; // 错误：不能通过到常量的引用修改
  cout << r2 << '\n';

  string&& r3 = s1 + s1;  // 可行：右值引用延长生存期
  r3 += "Test";
  cout << r3 << '\n';

  const string& r4 = r3;  // 右值引用可以转换到 const 限定的左值
  cout << r4 << '\n';

  string& r5 = r3;  // 右值引用可以转换到左值
  cout << r5 << '\n';
}
```

## 悬垂引用

当引用指代的对象已经销毁，引用就会变成悬垂引用，访问悬垂引用这是一种未定义行为，可能会导致程序崩溃．

以下为常见的悬垂引用的例子：

-   引用局部变量

    ```cpp
    #include <iostream>

    int& foo() {
      int a = 1;
      return a;
    }

    int main() {
      int& b = foo();
      std::cout << b << std::endl;  // 未定义行为
    }
    ```

-   解分配导致的悬垂引用

    ```cpp
    #include <iostream>

    int main() {
      int* ptr = new int(10);
      int& ref = *ptr;
      delete ptr;

      std::cout << ref << std::endl;  // 未定义行为
    }
    ```

-   内存重分配导致的悬垂引用

    ```cpp
    #include <iostream>

    int main() {
      std::string str = "hello";

      const char& ref = str.front();

      str.append("world");  // 可能会重新分配内存，导致 ref 指向的内存被释放

      std::cout << ref << std::endl;  // 未定义行为
    }
    ```

    类似 `std::vector`，`std::unordered_map` 等容器的插入操作，均有可能导致内存重新分配．

使用引用时，应时刻关注引用指向的对象的生命周期，避免造成悬垂引用．

通常静态检查工具和良好的代码习惯能让我们避免悬垂引用的问题．

## 引用相关的优化技巧

### 消除非轻量对象入参的拷贝开销

常见的 **非轻量对象** 有：

-   容器 `vector`，`array`，`map` 等
-   `string`
-   其他实现了或继承了自定义拷贝构造、移动构造等特殊函数的类型

而对 **轻量对象** 使用引用不能带来任何好处，引用类型作为参数的空间占用大小，甚至可能会比类型本身还大．

这可能会带来些的性能负担，同时可能会阻止编译器优化．

以下属于 **轻量对象**

-   基本类型 `int`，`float` 等
-   较小的 [聚合体类型](https://zh.cppreference.com/w/cpp/language/aggregate_initialization)
-   标准库容器的迭代器

### 将左值转换为右值

使用 `std::move` [转移](./value-category.md#stdmove) 对象的所有权．这通常见于局部变量之间，或参数与局部变量之间：

```cpp
#include <iostream>
#include <string>
#include <vector>

using namespace std;

string world(string str) { return std::move(str) += " world!"; }

int main() {
  // 1
  cout << world("hello") << '\n';

  vector<string> vec0;

  // 2
  {
    string&& size = to_string(vec0.size());

    size += ", " + to_string(size.size());

    vec0.emplace_back(std::move(size));
  }

  cout << vec0.front();
}
```

但不是所有时候都需要这么做，比如 [函数返回值优化](./value-category.md#常见误区)．

### 右值延长临时量生命期

从语义上，临时量可能会带来的额外的复制或移动，尽管多数情况下编译器能通过 [复制消除](./value-category.md#复制消除) 进行优化，但引用能强制编译器不进行这些多余操作，避免不确定性．

## 参考内容

1.  [C++ 语言文档——引用声明](https://zh.cppreference.com/w/cpp/language/reference)
2.  [C++ 语言文档——值类别](https://zh.cppreference.com/w/cpp/language/value_category)
3.  [Does const ref lvalue to non-const func return value specifically reduce copies?](https://stackoverflow.com/questions/38909228/does-const-ref-lvalue-to-non-const-func-return-value-specifically-reduce-copies)


## lang/struct.md

author: Ir1d, cjsoft, Lans1ot

**结构体**（struct），可以看做是一系列称为成员元素的组合体．

可以看做是自定义的数据类型．

???+ note "Note"
    本页描述的 `struct` 不同于 C 中 `struct`，在 C++ 中 `struct` 被扩展为类似 [`class`](./class.md) 的类说明符．

## 定义结构体

```cpp
struct Object {
  int weight;
  int value;
} e[array_length];

const Object a;
Object b, B[array_length], tmp;
Object *c;
```

上例中定义了一个名为 `Object` 的结构体，两个成员元素 `value, weight`，类型都为 `int`．

在 `}` 后，定义了数据类型为 `Object` 的常量 `a`，变量 `b`，变量 `tmp`，数组 `B`，指针 `c`．对于某种已经存在的类型，都可以使用这里的方法进行定义常量、变量、指针、数组等．

*关于指针：不必强求掌握．*

### 定义指针

如果是定义内置类型的指针，则与平常定义指针一样．

如果是定义结构体指针，在定义中使用 `StructName*` 进行定义．

```cpp
struct Edge {
  /*
  ...
  */
  Edge* nxt;
};
```

上例仅作举例，不必纠结实际意义．

## 访问/修改成员元素

可以使用 `变量名.成员元素名` 进行访问．例如可以使用 `cout << var.v` 来输出 `var` 的 `v` 成员．

也可以使用 `指针名->成员元素名` 或者 使用 `(*指针名).成员元素名` 进行访问．例如使用 `(*ptr).v = tmp` 或者 `ptr->v = tmp` 可以将结构体指针 `ptr` 指向的结构体的成员元素 `v` 赋值为 `tmp`：．

## 为什么需要结构体？

首先，条条大路通罗马，可以不使用结构体达到相同的效果．但是结构体能够显式地将成员元素（在算法竞赛中通常是变量）捆绑在一起，如本例中的 `Object` 结构体，便将 `value,weight` 放在了一起（定义这个结构体的实际意义是表示一件物品的重量与价值）．这样的好处边是限制了成员元素的使用．  
想象一下，如果不使用结构体而且有两个数组 `value[], Value[]`，很容易写混淆．但如果使用结构体，能够减轻出现使用变量错误的几率．

并且不同的结构体（结构体类型，如 `Object` 这个结构体）或者不同的结构体变量（结构体的实例，如上方的 `e` 数组）可以拥有相同名字的成员元素（如 `tmp.value,b.value`），同名的成员元素相互独立（拥有独自的内存，比如说修改 `tmp.value` 不会影响 `b.value` 的值）．  
这样的好处是可以使用尽可能相同或者相近的变量去描述一个物品．比如说 `Object` 里有 `value` 这个成员变量；我们还可以定义一个 `Car` 结构体，同时也拥有 `value` 这个成员；如果不使用结构体，或许我们就需要定义 `valueOfObject[],valueOfCar[]` 等不同名称的数组来区分．

*如果想要更详细的描述一种事物，还可以定义成员函数．请参考 [类](./class.md) 获取详细内容．*

## 更多的操作？

详见 [类](./class.md)．

## 注意事项

为了访问内存的效率更高，编译器在处理结构中成员的实际存储情况时，可能会将成员对齐在一定的字节位置，也就意味着结构中有空余的地方．因此，该结构所占用的空间可能大于其中所有成员所占空间的总和．

## 参考资料

1.  [Class - zh.cppreference.com](https://zh.cppreference.com/w/cpp/language/class)
2.  [Data structures - cplusplus.com](http://www.cplusplus.com/doc/tutorial/structures/)
3.  [对齐方式 - Microsoft Docs](https://docs.microsoft.com/zh-cn/cpp/cpp/alignment-cpp-declarations)


## lang/union.md

**联合体**（union）是特殊的类类型，它在一个时刻只能保有其一个非静态数据成员．

联合体在 2023 年正式被加入 NOI 大纲入门级中．

## 定义联合体

联合体声明的类说明符与类或 [结构体](./struct.md) 的声明相似：

```cpp
union MyUnion {
  int x;
  long long y;
} x;
```

联合体的定义与结构体类似．按照上述定义，`MyUnion` 同样可以当作一种自定义类型使用．名称 `MyUnion` 可以省略．

## 访问/修改成员元素

与结构体类似，同样可以使用 `变量名.成员名` 进行访问．

联合体所占用的内存空间大小 **不小于** 其最大的成员的大小，所有成员 **共用内存空间与地址**．当一个成员被赋值，由于内存共享，该联合体中的其他成员都会被覆盖．即同一时刻联合体中只能保存一个成员的值．

联合体的更多用法可以参见 [cppreference：联合体声明](https://zh.cppreference.com/w/cpp/language/union)．


## lang/value-category.md

值类别是 C++ 中一个非常重要的概念，虽然在算法竞赛中可能用处不大，但了解它可以帮助我们发现并避免不必要的复制，从而提高代码的效率和性能．

值类别的概念在 C 语言、C++98、C++11 和 C++17 中经历了多次发展，逐渐成为一个较为复杂的概念．

## 不必要的复制

我们考虑将字符串塞入 vector 这一过程：

```cpp
int main() {
  std::vector<std::string> vec;
  vec.reserve(3);
  for (int i = 0; i < 3; ++i) {
    std::string str;
    std::cin >> str;
    vec.push_back(str);
  }
  return 0;
}
```

可以发现字符串在转移的过程中，在 `str` 和 `vec` 中各保存了一份，内存占用加倍．

如果非要省下这一部分的内存，我们可以实现一个简陋的移动操作：自定义 `MyString` 结构体，内有一指针指向我们的字符串，即我们只需要把指针复制过去，并小心地清理原对象的指针，防止被错误析构．

```cpp
struct MyString {
  char *beg, *end;
  // ...
};

void move_to(MyString &src, MyString &dst) {
  dst.beg = src.beg;
  dst.end = src.end;
  src.beg = src.end = nullptr;
}
```

由于这种高效转移对象的需求较为常见，且与 C++ 的构造、析构等操作交互困难，C++11 将移动语义引入了语言核心．

## C 语言中的值类别

在 C 语言标准中，对象是一个比变量更为一般化的概念，它指代一块内存区域，具有内存地址．对象的主要属性包括：大小、有效类型、值和标识符．标识符即变量名，值是该内存以其类型解释时的含义．例如，`int` 和 `float` 类型虽然都占用 4 字节，但对于同一块内存，我们会解释出不同的含义．

C 语言中每个表达式都具有类型和值类别．值类别主要分为三类：

-   左值（lvalue）：隐含指代一个对象的表达式．即我们可以对该表达式取地址．
-   右值（rvalue）：不指代对象的表达式，即指代没有存储位置的值，我们无法取该值的地址．
-   函数指代符：函数类型的表达式．

因此，只有可修改的左值（没有 `const` 修饰且非数组的左值）可以位于赋值表达式左侧．

对于某个要求右值作为它的操作数的运算符，每当左值被用作操作数，都会对该表达式应用左值到右值，数组到指针，或者函数到指针标准转换以将它转换成右值．

常见误区：

-   右值表达式继续运算可能是左值．例如 `int *a`，表达式 `a + 1` 是右值，但 `*(a + 1)` 是左值．
-   表达式才有值类别，变量没有．例如 `int *a`，不能说变量 `a` 是左值，可以说其在表达式 `a` 中做左值．

## C++98 中的值类别

C++98 在值类别方面与 C 语言几乎一致，但增加了一些新的规则：

-   函数为左值，因为可以取地址．
-   左值引用（T&）是左值，因为可以取地址．
-   仅有 `const T&` 可绑定到右值．

### 复制消除

C++ 允许编译器执行复制消除（Copy Elision），可以减少临时对象的创建和销毁．

例如下面的代码，就触发了复制消除中的返回值优化（Return Value Optimization，RVO），你只会看到一次构造和一次复制构造，即便构造与析构有副作用．

```cpp
struct X {
  X() { std::puts("X::X()"); }

  X(const X &) { std::puts("X::X(const X &)"); }

  ~X() { std::puts("X::~X()"); }
};

X get() {
  X x;
  return x;
}

int main() {
  X x = get();
  X y = X(X(X(X(x))));
  return 0;
}
```

## C++11 中的值类别

C++11 引入了移动语义和右值引用（`T&&`），包括移动构造、移动赋值函数．这给了我们利用临时对象的方法．

我们上面的 `move_to` 可以改写如下：

```cpp
struct MyString {
  // ...
  MyString(MyString&& other) {
    beg = other.beg;
    end = other.end;
    other.beg = other.end = nullptr;
  }
};
```

我们现在关注的表达式特性增加了一点：

-   是否具有身份：是否指代一个对象，即是否有地址．
-   是否可被移动：是否具有移动构造、移动赋值等函数，让我们有办法利用这些临时对象．

因此我们有三种值类别：

-   有身份，不可移动：左值（lvalue）．
-   有身份，可被移动：亡值（xvalue）．
-   无身份，可被移动：纯右值（prvalue）．
-   无身份，不可移动：此类表达式无法使用．

另外 C++11 还引入了两个复合类别：

-   具有身份：泛左值（glvalue），即左值和亡值．
-   可被移动：右值（rvalue），即纯右值和亡值．

### std::move

为了配合移动语义，C++11 还引入了一个工具函数 `std::move`，其作用是将左值强制转换为右值，以便触发移动语义．

```cpp
int main() {
  std::vector<int> a = {1, 2, 3};
  std::cout << "a: " << a.data() << std::endl;
  std::vector<int> b = a;
  std::cout << "b: " << b.data() << std::endl;
  std::vector<int> c = std::move(b);
  std::cout << "c: " << c.data() << std::endl;
}
```

因此我们只需将 `push_back(str)` 改为 `push_back(std::move(str))` 即可避免复制．

```cpp
int main() {
  std::vector<std::string> vec;
  vec.reserve(3);
  for (int i = 0; i < 3; ++i) {
    std::string str;
    std::cin >> str;
    vec.push_back(std::move(str));
    // 另一种巧妙的写法，需要 C++17
    // std::cin >> vec.emplace_back();
  }
  return 0;
}
```

> 由于 `std::string` 有小对象优化（Small String Optimization，SSO），短字符串直接存储于结构体内，你可能得输入较长的字符串才能观察到 `data` 指针的不变性．

## C++17 中的值类别

C++17 进一步简化了值类别：

-   左值（lvalue）：有身份，不可移动．
-   亡值（xvalue）：有身份，可以移动．
-   纯右值（prvalue）：对象的初始化．

C++11 将复制消除扩展到了移动上，下面的代码中 `urvo` 在编译器启用 RVO 的情况下是没有移动的．

C++17 要求纯右值非必须不实质化，直接构造到其最终目标的存储中，在构造之前对象尚不存在．因此在 C++17 中我们就没有返回这一步，也就不必依赖 RVO．也可以理解为强制了 URVO（Unnamed RVO），但对于 NRVO（Named RVO）还是非强制的．

```cpp
std::string urvo() { return std::string("123"); }

std::string nrvo() {
  std::string s;
  s = "123";
  std::cout << s;
  return s;
}

int main() {
  std::string str = urvo();  // 直接构造
  std::string str = nrvo();  // 不一定直接构造，依赖于优化
}
```

同时 C++17 引入了临时量实质化的机制，当我们需要访问成员变量、调用成员函数等需要泛左值的情形时，可以隐式转换为亡值．

### 常见误区

下面的例子中：

-   在 `f1` 中返回 `std::move(x)` 是多余的，并不会带来性能上的提升，反而会干扰编译器进行 NRVO 优化．
-   在 `f2` 中返回 `std::move(x)` 是危险的，函数返回右值引用指向了已被销毁的局部变量 `s`，出现了悬空引用问题．

```cpp
std::string f1() {
  std::string s = "123";
  // 等价于 return std::string(std::move(s))
  return std::move(s);
}

std::string&& f2() {
  std::string s = "123";
  return std::move(s);
}
```

## 参考文献与推荐阅读

1.  [Value categories](https://en.cppreference.com/w/cpp/language/value_category)
2.  [Wording for guaranteed copy elision through simplified value categories](http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2016/p0135r1.html)
3.  [C++ 中的值类别](https://paul.pub/cpp-value-category/)
4.  [C++ 的右值引用、移动和值类别系统，你所需要的一切](https://zclll.com/index.php/cpp/value_category.html)
5.  [Copy elision](https://en.cppreference.com/w/cpp/language/copy_elision)


## lang/var.md

## 数据类型

C++ 的类型系统由如下几部分组成：

1.  基础类型（括号内为代表关键词/代表类型）
    1.  无类型/`void` 型 (`void`)
    2.  （C++11 起）空指针类型 (`std::nullptr_t`)
    3.  算术类型
        1.  整数类型 (`int`)
        2.  布尔类型/`bool` 型 (`bool`)
        3.  字符类型 (`char`)
        4.  浮点类型 (`float`,`double`)
2.  复合类型[^note11]

### 布尔类型

一个 `bool` 类型的变量取值只可能为两种：`true` 和 `false`．

一般情况下，一个 `bool` 类型变量占有 $1$ 字节（一般情况下，$1$ 字节 =$8$ 位）的空间．

???+ tip "Tip"
    可通过头文件 `<climits>`(C++)/`<limits.h>`(C) 中的宏常量 `CHAR_BIT` 获取字节的位数．

???+ note "C 语言的布尔类型"
    另请参阅 [C++ 与其他常用语言的区别 - bool](./cpp-other-langs.md#bool)．
    
    C 语言最初是没有布尔类型的，直到 C99 时才引入 `_Bool` 关键词作为布尔类型，其被视作无符号整数类型．
    
    ???+ note "Note"
        C 语言的 `bool` 类型从 C23 起不再使用整型的零与非零值定义，而是定义为足够储存 `true` 和 `false` 两个常量的类型．
    
    为方便使用，`stdbool.h` 中提供了 `bool`,`true`,`false` 三个宏，定义如下：
    
    ```c
    #define bool _Bool
    #define true 1
    #define false 0
    ```
    
    这些宏于 C23 中移除，并且 C23 起引入 `true`,`false` 和 `bool` 作为关键字，同时保留 `_Bool` 作为替代拼写形式[^note10]．
    
    另外，C23 起还可以通过 `<limits.h>` 中的宏常量 `BOOL_WIDTH` 获取布尔类型的位宽．

### 整数类型

用于存储整数．最基础的整数类型是 `int`.

???+ warning "注意"
    由于历史原因，C++ 中布尔类型和字符类型会被视作特殊的整型．
    
    在几乎所有的情况下都 **不应该** 将除 `signed char` 和 `unsigned char` 之外的字符类型作为整型使用．

整数类型一般按位宽有 5 个梯度：`char`,`short`,`int`,`long`,`long long`.

C++ 标准保证 `1 == sizeof(char) <= sizeof(short) <= sizeof(int) <= sizeof(long) <= sizeof(long long)`

由于历史原因，整数类型的位宽有多种流行模型，为解决这一问题，C99/C++11 引入了 [定宽整数类型](#定宽整数类型)．

???+ note "`int` 类型的大小"
    在 C++ 标准中，规定 `int` 的位数 **至少** 为 $16$ 位．
    
    事实上在现在的绝大多数平台，`int` 的位数均为 $32$ 位．

对于 `int` 关键字，可以使用如下修饰关键字进行修饰：

符号性：

-   `signed`：表示带符号整数（默认）；
-   `unsigned`：表示无符号整数．

大小：

-   `short`：表示 **至少**  $16$ 位整数；
-   `long`：表示 **至少**  $32$ 位整数；
-   （C++11 起）`long long`：表示 **至少**  $64$ 位整数．

下表给出在 **一般情况下**，各整数类型的位宽和表示范围大小（少数平台上一些类型的表示范围可能与下表不同）：

| 类型名                                                                   | 等价类型                     | 位宽（C++ 标准） | 位宽（常见） | 位宽（较罕见）                    |
| --------------------------------------------------------------------- | ------------------------ | ---------- | ------ | -------------------------- |
| `signed char`                                                         | `signed char`            | $8$        | -      | -                          |
| `unsigned char`                                                       | `unsigned char`          | $8$        | -      | -                          |
| `short`,`short int`,`signed short`,`signed short int`                 | `short int`              | $\geq 16$  | $16$   | -                          |
| `unsigned short`,`unsigned short int`                                 | `unsigned short int`     | $\geq 16$  | $16$   | -                          |
| `int`,`signed`,`signed int`                                           | `int`                    | $\geq 16$  | $32$   | $16$（常见于 Win16 API）        |
| `unsigned`,`unsigned int`                                             | `unsigned int`           | $\geq 16$  | $32$   | $16$（常见于 Win16 API）        |
| `long`,`long int`,`signed long`,`signed long int`                     | `long int`               | $\geq 32$  | $32$   | $64$（常见于 64 位 Linux、macOS） |
| `unsigned long`,`unsigned long int`                                   | `unsigned long int`      | $\geq 32$  | $32$   | $64$（常见于 64 位 Linux、macOS） |
| `long long`,`long long int`,`signed long long`,`signed long long int` | `long long int`          | $\geq 64$  | $64$   | -                          |
| `unsigned long long`,`unsigned long long int`                         | `unsigned long long int` | $\geq 64$  | $64$   | -                          |

当位宽为 $x$ 时，有符号类型的表示范围为 $-2^{x-1}\sim 2^{x-1}-1$[^note16], 无符号类型的表示范围为 $0 \sim 2^x-1$. 具体而言，有下表：

| 位宽   | 表示范围                                              |
| ---- | ------------------------------------------------- |
| $8$  | 有符号：$-2^{7}\sim 2^{7}-1$, 无符号：$0 \sim 2^{8}-1$    |
| $16$ | 有符号：$-2^{15}\sim 2^{15}-1$, 无符号：$0 \sim 2^{16}-1$ |
| $32$ | 有符号：$-2^{31}\sim 2^{31}-1$, 无符号：$0 \sim 2^{32}-1$ |
| $64$ | 有符号：$-2^{63}\sim 2^{63}-1$, 无符号：$0 \sim 2^{64}-1$ |

???+ note "等价的类型表述"
    在不引发歧义的情况下，允许省略部分修饰关键字，或调整修饰关键字的顺序．这意味着同一类型会存在多种等价表述．
    
    例如 `int`，`signed`，`int signed`，`signed int` 表示同一类型，而 `unsigned long` 和 `unsigned long int` 表示同一类型．

另外，一些编译器实现了扩展整数类型，如 GCC 实现了 128 位整数：有符号版的 `__int128_t` 和无符号版的 `__uint128_t`，如果您在比赛时想使用这些类型，**请仔细阅读比赛规则** 以确定是否允许或支持使用扩展整数类型．

???+ warning "注意"
    STL 不一定对扩展整数类型有足够的支持，故使用扩展整数类型时需格外小心．
    
    ???+ note "示例代码"
        ```cpp
        #include <cmath>
        #include <iostream>
        
        int f1(int n) {
          return abs(n);  // Good
        }
        
        int f2(int n) {
          return std::abs(n);  // Good
        }
        
        __int128_t f3(__int128_t n) {
          return abs(n);  // Bad
        }
        
        // Wrong
        // __int128_t f4(__int128_t n) {
        //   return std::abs(n);
        // }
        
        int main() {
          std::cout << "f1: " << f1(-42) << std::endl;
          std::cout << "f2: " << f2(-42) << std::endl;
          // std::cout << "f3: " << f3(-42) << std::endl; // Wrong
          // std::cout << "f4: " << f4(-42) << std::endl; // Wrong
          return 0;
        }
        ```
    
    以上示例代码存在如下问题：
    
    1.  `__int128_t f3(__int128_t)` 中使用的是 C 风格的绝对值函数，其签名为 `int abs(int)`，故 `n` 首先会强制转换为 `int`，然后才会调用 `abs` 函数．
    2.  `__int128_t f4(__int128_t)` 中使用的是 C++ 风格的绝对值函数，其并没有签名为 `__int128_t std::abs(__int128_t)` 的函数重载，所以无法通过编译．
    3.  C++ 的流式输出不支持 `__int128_t` 与 `__uint128_t`．
    
    以下是一种解决方案：
    
    ??? note "修正后的代码"
        ```cpp
        #include <cmath>
        #include <iostream>
        
        __int128_t abs(__int128_t n) { return n < 0 ? -n : n; }
        
        std::ostream &operator<<(std::ostream &os, __uint128_t n) {
          if (n > 9) os << n / 10;
          os << (int)(n % 10);
          return os;
        }
        
        std::ostream &operator<<(std::ostream &os, __int128_t n) {
          if (n < 0) {
            os << '-';
            n = -n;
          }
          return os << (__uint128_t)n;
        }
        
        int f1(int n) { return abs(n); }
        
        int f2(int n) { return std::abs(n); }
        
        __int128_t f3(__int128_t n) { return abs(n); }
        
        int main() {
          std::cout << "f1: " << f1(-42) << std::endl;
          std::cout << "f2: " << f2(-42) << std::endl;
          std::cout << "f3: " << f3(-42) << std::endl;
        }
        ```

### 字符类型

分为「窄字符类型」和「宽字符类型」，由于算法竞赛几乎不会用到宽字符类型，故此处仅介绍窄字符类型．

窄字符型位数一般为 $8$ 位，实际上底层存储方式仍然是整数，一般通过 [ASCII 编码](http://www.asciitable.com/) 实现字符与整数的一一对应，有如下三种：

-   `signed char`：有符号字符表示的类型，表示范围在 $-128 \sim 127$ 之间．
-   `unsigned char`：无符号字符表示的类型，表示范围在 $0 \sim 255$ 之间．
-   `char` 拥有与 `signed char` 或 `unsigned char` 之一相同的表示和对齐，但始终是独立的类型．

    `char` 的符号性取决于编译器和目标平台：ARM 和 PowerPC 的默认设置通常没有符号，而 x86 与 x64 的默认设置通常有符号．

    GCC 可以在编译参数中添加 `-fsigned-char` 或 `-funsigned-char` 指定将 `char` 视作 `signed char` 或 `unsigned char`，其他编译器请参照文档．需要注意指定与架构默认值不同的符号有可能会破坏 ABI，造成程序无法正常工作．

???+ warning "注意"
    与其他整型不同，`char`、`signed char`、`unsigned char` 是 **三种不同的类型**．
    
    一般来说 `signed char`,`unsigned char` 不应用来存储字符，绝大多数情况下，这两种类型均被视作整数类型．

### 浮点类型

用于存储「实数」（注意并不是严格意义上的实数，而是实数在一定规则下的近似），包括以下三种：

-   `float`：单精度浮点类型．如果支持就会匹配 IEEE-754 binary32 格式．
-   `double`：双精度浮点类型．如果支持就会匹配 IEEE-754 binary64 格式．
-   `long double`：扩展精度浮点类型．如果支持就会匹配 IEEE-754 binary128 格式，否则如果支持就会匹配 IEEE-754 binary64 扩展格式，否则匹配某种精度优于 binary64 而值域至少和 binary64 一样好的非 IEEE-754 扩展浮点格式，否则匹配 IEEE-754 binary64 格式．

| 浮点格式                   | 位宽        | 最大正数                       | 精度位数             |
| ---------------------- | --------- | -------------------------- | ---------------- |
| IEEE-754 binary32 格式   | $32$      | $3.4\times 10^{38}$        | $6\sim 9$        |
| IEEE-754 binary64 格式   | $64$      | $1.8\times 10^{308}$       | $15\sim 17$      |
| IEEE-754 binary64 扩展格式 | $\geq 80$ | $\geq 1.2\times 10^{4932}$ | $\geq 18\sim 21$ |
| IEEE-754 binary128 格式  | $128$     | $1.2\times 10^{4932}$      | $33\sim 36$      |

> IEEE-754 浮点格式的最小负数是最大正数的相反数．

因为 `float` 类型表示范围较小，且精度不高，实际应用中常使用 `double` 类型表示浮点数．

另外，浮点类型可以支持一些特殊值：

-   无穷（正或负）：`INFINITY`.
-   负零：`-0.0`，例如 `1.0 / 0.0 == INFINITY`,`1.0 / -0.0 == -INFINITY`.
-   非数（NaN）：`std::nan`,`NAN`，一般可以由 `0.0 / 0.0` 之类的运算产生．它与任何值（包括自身）比较都不相等，C++11 后可以 使用 `std::isnan` 判断一个浮点数是不是 NaN.

### 无类型

`void` 类型为无类型，与上面几种类型不同的是，不能将一个变量声明为 `void` 类型．但是函数的返回值允许为 `void` 类型，表示该函数无返回值．

### 空指针类型

请参阅指针的 [对应章节](./pointer.md#空指针)

## 定宽整数类型

C++11 起提供了定宽整数的支持，具体如下：

-   `<cstdint>`：提供了若干定宽整数的类型和各定宽整数类型最大值、最小值等的宏常量．
-   `<cinttypes>`：为定宽整数类型提供了用于 `std::fprintf` 系列函数和 `std::fscanf` 系列函数的格式宏常量．

定宽整数有如下几种：

-   `intN_t`: 宽度 **恰为**  $N$ 位的有符号整数类型，如 `int32_t`.
-   `int_fastN_t`: 宽度 **至少** 有 $N$ 位的 **最快的** 有符号整数类型，如 `int_fast32_t`.
-   `int_leastN_t`: 宽度 **至少** 有 $N$ 位的 **最小的** 有符号整数类型，如 `int_least32_t`.

无符号版本只需在有符号版本前加一个字母 u 即可，如 `uint32_t`,`uint_least8_t`.

标准规定必须实现如下 16 种类型：

`int_fast8_t`,`int_fast16_t`,`int_fast32_t`,`int_fast64_t`,

`int_least8_t`,`int_least16_t`,`int_least32_t`,`int_least64_t`,

`uint_fast8_t`,`uint_fast16_t`,`uint_fast32_t`,`uint_fast64_t`,

`uint_least8_t`,`uint_least16_t`,`uint_least32_t`,`uint_least64_t`.

绝大多数编译器在此基础上都实现了如下 8 种类型：

`int8_t`,`int16_t`,`int32_t`,`int64_t`,

`uint8_t`,`uint16_t`,`uint32_t`,`uint64_t`.

在实现了对应类型的情况下，C++ 标准规定必须实现表示对应类型的最大值、最小值、位宽的宏常量，格式为将类型名末尾的 `_t` 去掉后转大写并添加后缀：

-   `_MAX` 表示最大值，如 `INT32_MAX` 即为 `int32_t` 的最大值．
-   `_MIN` 表示最小值，如 `INT32_MIN` 即为 `int32_t` 的最小值．

???+ warning "注意"
    定宽整数类型本质上是普通整数类型的类型别名，所以混用定宽整数类型和普通整数类型可能会影响跨平台编译，例如：
    
    ???+ note "示例代码"
        ```cpp
        #include <algorithm>
        #include <cstdint>
        #include <iostream>
        
        int main() {
          long long a;
          int64_t b;
          std::cin >> a >> b;
          std::cout << std::max(a, b) << std::endl;
          return 0;
        }
        ```
    
    `int64_t` 在 64 位 Windows 下一般为 `long long int`, 而在 64 位 Linux 下一般为 `long int`, 所以这段代码在使用 64 位 Linux 下的 GCC 时不能通过编译，而使用 64 位 Windows 下的 MSVC 时可以通过编译，因为 `std::max` 要求输入的两个参数类型必须相同．

此外，C++17 起在 `<limits>` 中提供了 `std::numeric_limits` 类模板，用于查询各种算数类型的属性，如最大值、最小值、是否是整形、是否有符号等．

```cpp
#include <cstdint>
#include <limits>

std::numeric_limits<int32_t>::max();  // int32_t 的最大值, 2'147'483'647
std::numeric_limits<int32_t>::min();  // int32_t 的最小值, -2'147'483'648

std::numeric_limits<double>::min();  // double 的最小值, 约为 2.22507e-308
std::numeric_limits<double>::epsilon();  // 1.0 与 double 的下个可表示值的差,
                                         // 约为 2.22045e-16
```

## 类型转换

在一些时候（比如某个函数接受 `int` 类型的参数，但传入了 `double` 类型的变量），我们需要将某种类型，转换成另外一种类型．

C++ 中类型的转换机制较为复杂，这里主要介绍对于基础数据类型的两种转换：数值提升和数值转换．

### 数值提升

数值提升过程中，值本身保持不变．

???+ note "Note"
    C 风格的可变参数域在传值过程中会进行默认参数提升．如：
    
    ???+ note "示例代码"
        ```c
        #include <stdarg.h>
        #include <stdio.h>
        
        void test(int tot, ...) {
          va_list valist;
          int i;
        
          // 初始化可变参数列表
          va_start(valist, tot);
        
          for (i = 0; i < tot; ++i) {
            // 获取第 i 个变量的值
            double xx = va_arg(valist, double);  // Correct
            // float xx = va_arg(valist, float); // Wrong
        
            // 输出第 i 个变量的底层存储内容
            printf("i = %d, value = 0x%016llx\n", i, *(long long *)(&xx));
          }
        
          // 清理可变参数列表的内存
          va_end(valist);
        }
        
        int main() {
          float f;
          double fd, d;
          f = 123.;   // 0x42f60000
          fd = 123.;  // 0x405ec00000000000
          d = 456.;   // 0x407c800000000000
          test(3, f, fd, d);
        }
        ```
    
    在调用 `test` 时，`f` 提升为 `double`，从而底层存储内容和 `fd` 相同，输出为
    
    ```text
    i = 0, value = 0x405ec00000000000
    i = 1, value = 0x405ec00000000000
    i = 2, value = 0x407c800000000000
    ```
    
    若将 `double xx = va_arg(valist, double);` 改为 `float xx = va_arg(valist, float);`，GCC 应该给出一条类似下文的警告：
    
    ```text
    In file included from test.c:2:
    test.c: In function 'test':
    test.c:14:35: warning: 'float' is promoted to 'double' when passed through '...'
      14 |         float xx = va_arg(valist, float);
         |                                   ^
    test.c:14:35: note: (so you should pass 'double' not 'float' to 'va_arg')
    test.c:14:35: note: if this code is reached, the program will abort
    ```
    
    此时的程序将会在输出前终止．
    
    这一点也能解释为什么 `printf` 的 `%f` 既能匹配 `float` 也能匹配 `double`．

#### 整数提升

小整数类型（如 `char`）的纯右值可转换成较大整数类型（如 `int`）的纯右值．

具体而言，算术运算符不接受小于 `int` 的类型作为它的实参，而在左值到右值转换后，如果适用就会自动实施整数提升．

具体地，有如下规则：

-   源类型为 `signed char`、`signed short / short` 时，可提升为 `int`．
-   源类型为 `unsigned char`、`unsigned short` 时，若 `int` 能保有源类型的值范围，则可提升为 `int`，否则可提升为 `unsigned int`．（`C++20` 起 `char8_t` 也适用本规则）
-   `char` 的提升规则取决于其底层类型是 `signed char` 还是 `unsigned char`．
-   `bool` 类型可转换到 `int`：`false` 变为 `0`，`true` 变为 `1`．
-   若目标类型的值范围包含源类型，且源类型的值范围不能被 `int` 和 `unsigned int` 包含，则源类型可提升为目标类型．[^note12]

???+ warning "注意"
    `char`->`short` 不是数值提升，因为 `char` 要优先提升为 `int / unsigned int`，之后是 `int / unsigned int`->`short`，不满足数值提升的条件．

如（以下假定 `int` 为 32 位，`unsigned short` 为 16 位，`signed char` 和 `unsigned char` 为 8 位，`bool` 为 1 位）

-   `(signed char)'\0' - (signed char)'\xff'` 会先将 `(signed char)'\0'` 提升为 `(int)0`、将 `(signed char)'\xff'` 提升为 `(int)-1`, 再进行 `int` 间的运算，最终结果为 `(int)1`．
-   `(unsigned char)'\0' - (unsigned char)'\xff'` 会先将 `(unsigned char)'\0'` 提升为 `(int)0`、将 `(unsigned char)'\xff'` 提升为 `(int)255`, 再进行 `int` 间的运算，最终结果为 `(int)-255`．
-   `false - (unsigned short)12` 会先将 `false` 提升为 `(int)0`、将 `(unsigned short)12` 提升为 `(int)12`, 再进行 `int` 间的运算，最终结果为 `(int)-12`．

#### 浮点提升

位宽较小的浮点数可以提升为位宽较大的浮点数（例如 `float` 类型的变量和 `double` 类型的变量进行算术运算时，会将 `float` 类型变量提升为 `double` 类型变量），其值不变．

### 数值转换

数值转换过程中，值可能会发生改变．

???+ warning "注意"
    数值提升优先于数值转换．如 `bool`->`int` 时是数值提升而非数值转换．

#### 整数转换

<!-- scripts.linter.preprocess.fix_details off -->

-   如果目标类型为位宽为 $x$ 的无符号整数类型，则转换结果是原值 $\bmod 2^x$ 后的结果．

    -   若目标类型位宽大于源类型位宽：

        -   若源类型为有符号类型，一般情况下需先进行符号位扩展再转换．

            如

            -   将 `(short)-1`（`(short)0b1111'1111'1111'1111`）转换为 `unsigned int` 类型时，先进行符号位扩展，得到 `0b1111'1111'1111'1111'1111'1111'1111'1111`，再进行整数转换，结果为 `(unsigned int)4'294'967'295`（`(unsigned int)0b1111'1111'1111'1111'1111'1111'1111'1111`）．
            -   将 `(short)32'767`（`(short)0b0111'1111'1111'1111`）转换为 `unsigned int` 类型时，先进行符号位扩展，得到 `0b0000'0000'0000'0000'0111'1111'1111'1111`，再进行整数转换，结果为 `(unsigned int)32'767`（`(unsigned int)0b0000'0000'0000'0000'0111'1111'1111'1111`）．

        -   若源类型为无符号类型，则需先进行零扩展再转换．

            如将 `(unsigned short)65'535`（`(unsigned short)0b1111'1111'1111'1111`）转换为 `unsigned int` 类型时，先进行零扩展，得到 `0b0000'0000'0000'0000'1111'1111'1111'1111`，再进行整数转换，结果为 `(unsigned int)65'535`（`(unsigned int)0b0000'0000'0000'0000'1111'1111'1111'1111`）．

    -   若目标类型位宽不大于源类型位宽，则需先截断再转换．

        如将 `(unsigned int)4'294'967'295`（`(unsigned int)0b1111'1111'1111'1111'1111'1111'1111'1111`）转换为 `unsigned short` 类型时，先进行截断，得到 `0b1111'1111'1111'1111`，再进行整数转换，结果为 `(unsigned short)65'535`（`(unsigned short)0b1111'1111'1111'1111`）．

-   如果目标类型为位宽为 $x$ 的带符号整数类型，则 **一般情况下**，转换结果可以认为是原值 $\bmod 2^x$ 后的结果．[^note13]

    例如将 `(unsigned int)4'294'967'295`（`(unsigned int)0b1111'1111'1111'1111'1111'1111'1111'1111`）转换为 `short` 类型时，结果为 `(short)-1`（`(short)0b1111'1111'1111'1111`）．

-   如果目标类型是 `bool`，则是 [布尔转换](#布尔转换)．

-   如果源类型是 `bool`，则 `false` 转为对应类型的 0，`true` 转为对应类型的 1．

<!-- scripts.linter.preprocess.fix_details on -->

#### 浮点转换

位宽较大的浮点数转换为位宽较小的浮点数，会将该数舍入到目标类型下最接近的值．

#### 浮点整数转换

-   浮点数转换为整数时，会舍弃浮点数的全部小数部分．

    如果目标类型是 `bool`，则是 [布尔转换](#布尔转换)．

-   整数转换为浮点数时，会舍入到目标类型下最接近的值．

    如果该值不能适应到目标类型中，那么行为未定义．

    如果源类型是 `bool`，那么 `false` 转换为零，而 `true` 转换为一．

#### 布尔转换

将其他类型转换为 `bool` 类型时，零值转换为 `false`，非零值转换为 `true`．

## 定义变量

简单地说[^note14]，定义一个变量，需要包含类型说明符（指明变量的类型），以及要定义的变量名．

例如，下面这几条语句都是变量定义语句．

```cpp
int oi;
double wiki;
char org = 'c';
```

在目前我们所接触到的程序段中，定义在花括号包裹的地方的变量是局部变量，而定义在没有花括号包裹的地方的变量是全局变量．实际有例外，但是现在不必了解．

定义时没有初始化值的全局变量会被初始化为 $0$．而局部变量没有这种特性，需要手动赋初始值，否则可能引起难以发现的 bug．

## 变量作用域

作用域是变量可以发挥作用的代码块．

全局变量的作用域，自其定义之处开始[^note15]，至文件结束位置为止．

局部变量的作用域，自其定义之处开始，至代码块结束位置为止．

由一对大括号括起来的若干语句构成一个代码块．

```cpp
int g = 20;  // 定义全局变量

int main() {
  int g = 10;         // 定义局部变量
  printf("%d\n", g);  // 输出 g
  return 0;
}
```

如果一个代码块的内嵌块中定义了相同变量名的变量，则内层块中将无法访问外层块中相同变量名的变量．

例如上面的代码中，输出的 $g$ 的值将是 $10$．因此为了防止出现意料之外的错误，请尽量避免局部变量与全局变量重名的情况．

## 常量

常量是固定值，在程序执行期间不会改变．

常量的值在定义后不能被修改．定义时加一个 `const` 关键字即可．

```cpp
const int a = 2;
a = 3;
```

如果修改了常量的值，在编译环节就会报错：`error: assignment of read-only variable 'a'`．

## 参考资料与注释

1.  [Working Draft, Standard for Programming Language C++](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2022/n4917.pdf)
2.  [类型 - cppreference.com](https://zh.cppreference.com/w/cpp/language/type)
3.  C 语言的 [算术类型 - cppreference.com](https://zh.cppreference.com/w/c/language/arithmetic_types)
4.  [基础类型 - cppreference.com](https://zh.cppreference.com/w/cpp/language/types)
5.  [定宽整数类型（C++11 起）- cppreference.com](https://zh.cppreference.com/w/cpp/types/integer)
6.  William Kahan (1 October 1997).["Lecture Notes on the Status of IEEE Standard 754 for Binary Floating-Point Arithmetic"](https://people.eecs.berkeley.edu/~wkahan/ieee754status/IEEE754.PDF).
7.  [隐式转换 - cppreference.com](https://zh.cppreference.com/w/cpp/language/implicit_conversion)
8.  [声明 - cppreference](https://zh.cppreference.com/w/cpp/language/declarations)
9.  [作用域 - cppreference.com](https://zh.cppreference.com/w/cpp/language/scope)

[^note10]: 参见 <https://www.open-std.org/jtc1/sc22/wg14/www/docs/n3054.pdf>

[^note11]: 包括数组类型、引用类型、指针类型、类类型、函数类型等．由于本篇文章是面向初学者的，故不在本文做具体介绍．具体请参阅 [类型 - cppreference.com](https://zh.cppreference.com/w/cpp/language/type)

[^note12]: 不包含宽字符类型、位域和枚举类型，详见 [整型转换 - cppreference](https://zh.cppreference.com/w/cpp/language/implicit_conversion#.E6.95.B4.E5.9E.8B.E8.BD.AC.E6.8D.A2)．

[^note13]: 自 C++20 起生效．C++20 前结果是实现定义的．详见 [整型转换 - cppreference](https://zh.cppreference.com/w/cpp/language/implicit_conversion#.E6.95.B4.E5.9E.8B.E8.BD.AC.E6.8D.A2)．

[^note14]: 定义一个变量时，除了类型说明符之外，还可以包含其他说明符．详见 [声明 - cppreference](https://zh.cppreference.com/w/cpp/language/declarations)．

[^note15]: 更准确的说法是 [声明点](https://zh.cppreference.com/w/cpp/language/scope#.E5.A3.B0.E6.98.8E.E7.82.B9)．

[^note16]: C++20 前规定有符号整数至少要覆盖 [反码](../math/bit.md#整数与位序列) 的表示范围（即 $-2^{x-1}+1\sim 2^{x-1}-1$），但实际上绝大多数实现中均采用 [补码](../math/bit.md#整数与位序列) 实现；C++20 起进一步规定有符号整数必须使用补码实现．详见 [Range of values - cppreference](https://en.cppreference.com/w/cpp/language/types.html#Range_of_values)．
