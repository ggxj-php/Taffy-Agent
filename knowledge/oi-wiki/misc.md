

## misc/15-puzzle.md

## 简介

**15 - 拼图**（英文：15-puzzle, 又名 Gem Puzzle，Boss Puzzle，Game of 15，Mystic Square，N-puzzle, etc）是一个滑块类游戏（英文：sliding puzzle）．滑块方盘的长宽均为 $4\times 4$ 个方块，其中 15 个位置放序号打乱的方块，剩下一个为空位．与空位同行或同列的方块可以通过水平或垂直滑动来移动．拼图的目标是按编号顺序排列方块．

15 - 拼图常见别称为 **n - 拼图**，其中数字 $n$ 指的是方盘中的方块总数．15 - 拼图的不同尺寸变体亦使用了类似的名称，例如 $8$ 拼图指的是置于 $3\times3$ 方盘中的 $8$ 个方块．但 $15$ 拼图也可以称为 $16$ 拼图，此处的 16 指的是方块容量．它的扩展问题有时也包括了 $n \times m$ 的滑动方盘．

15 - 拼图是涉及 [启发式算法](../search/heuristic.md) 建模的经典问题．此问题的常见形式是 [曼哈顿距离](../geometry/distance.md#曼哈顿距离) 和错位方块的数量计算，二者都是可接受启发（英文：admissible heuristic），即它们永远不会高估剩余的移动次数，这确保了某些搜索算法（例如 [A \* 算法](../search/astar.md)）的最优性．

???+ note "注释"
    **滑块游戏** 是一类在平面上滑动方块以组成特定排列的智力游戏．常见的滑块游戏包括数字拼图、华容道和塞车时间．其中 15 - 拼图是最古老的滑块类游戏，发明者是 Noyes Chapman，该游戏风靡于 1880 年代．不像其它 tour 类的解谜游戏，滑块游戏禁止任何一个方块离开盘面，这个特性区别于重新排列类的解谜游戏．

## 定义

给定一个 $4 \times 4$ 的方盘，其中 $15$ 个方块随意排列．我们需要将它按照序号排列成下图所示的样子．移动规则为每次只能交换空方块和其相邻一个方块的位置．常见问题为找到可解决此问题的最少步骤，计算错位方位的个数，或找出是否能得到最终的有序排列．

![](./images/15puzzle-1.svg)

## 可解性证明

Johnson & Story (1879) 证明，如果 $m$ 和 $n$ 都至少为 $2$，则逆向适用于大小为 $m\times n$ 的棋盘：通过从 $m=n=2$ 开始对 $m$ 和 $n$ 进行归纳证明，所有偶数排列都是可解的．Archer (1999) 给出了另一个证明，基于通过汉密尔顿路径定义等价类．

## 算法

寻找数字滑盘游戏的一个解相对容易，但寻找 **最优解** 是一个 **NP 困难** 问题．15-Puzzle 的最优解至多有 80 步；而 8-Puzzle 的最优解至多有 31 步．

N-Puzzle 支持常见的基于图的搜索算法，如广度优先搜索和深度优先搜索，同样我们也可以用 [A \* 搜索](../search/astar.md) 算法寻找最优解．启发式函数 $h(n)$ 可以是

-   放错的方块的数量．
-   所有放错的方块到各自目标位置的欧几里得距离之和．
-   所有放错的方块到各自目标位置的曼哈顿距离之和．

### 群理论

因为 15 块的数字推盘游戏组合可以由「3 循环」（英文：3-cycles）产生，所以可以证明 15 块的数字推盘游戏可以用交错群 $A_{15}$ 表示．事实上，任何使用 $2\times k-1$ 块相同面积正方形方块的数字滑盘游戏皆可以以交错群 $A_{2k-1}$ 表示．

## 习题

-   [N Puzzle](https://www.hackerrank.com/challenges/n-puzzle)
-   [A. Amity Assessment](https://codeforces.com/problemset/problem/645/A)
-   [Sliding Puzzle](https://leetcode.com/problems/sliding-puzzle/)
-   [POJ 1077 - Eight](http://poj.org/problem?id=1077)

## 参考资料与拓展阅读

1.  [15 puzzle - Wikipedia](https://en.wikipedia.org/wiki/15_puzzle)
2.  jrdnjacobson,[How to Solve the 15 Puzzle - instructables](https://www.instructables.com/How-To-Solve-The-15-Puzzle/)
3.  Korf, R. E. (2000),["Recent Progress in the Design and Analysis of Admissible Heuristic Functions"](https://www.researchgate.net/publication/2604757_Recent_Progress_in_the_Design_and_Analysis_of_Admissible_Heuristic_Functions), in Choueiry, B. Y.; Walsh, T. (eds.), Abstraction, Reformulation, and Approximation (PDF), SARA 2000. Lecture Notes in Computer Science, vol. 1864, Springer, Berlin, Heidelberg, pp. 45–55, doi:10.1007/3-540-44914-0\_3, ISBN 978-3-540-67839-7, retrieved 2010-04-26
4.  [Welcome to N-Puzzle - web demo](https://tristanpenman.com/demos/n-puzzle/)


## misc/cc-basic.md

本部分将介绍基础的计算理论的知识．这部分内容在 OI 中作用不大（但还是略有作用：如果你遇到了一个 NP-hard 问题，你可以认为它是不存在多项式复杂度的解法的），可以作为兴趣了解，或者为以后的学习做准备．

本文中许多结论都是不加证明的，如果有兴趣的话可以自行查阅相关证明．

前置知识：[时间复杂度](../basic/complexity.md)．

## 问题

### 语言

一个 **字母表（alphabet）** 是一个非空有限集合，该集合中的元素称为 **符号/字符（symbol）**．

令 $\Sigma^\ast$ 表示非负整数个 $\Sigma$ 中的字符连接而成的串，字母表 $\Sigma$ 上的一个 **语言（language）** 是 $\Sigma^\ast$ 的一个子集．

需要注意的是，这里的「语言」是一个抽象的概念，通常意义上的字符串是语言，所有的有向无环图也可以是一个语言（01 串与有向图之间可以建立双射，具体方式无需了解）．

由于任何语言都可以转化成 01 串的形式，所以在下文中不加说明时 $\Sigma=\{0, 1\}$．

### 判定问题

判定问题就是只能用 YES/NO 回答的问题，本质上是判定一个串是否属于一个语言，即：$f:\Sigma^\ast\rightarrow\{0, 1\}, f(x)=1\iff x\in L$ 是一个关于字母表 $\Sigma$ 和语言 $L$ 的判定问题．如，「判定一张图是不是一个有向无环图」就是一个判定问题．

判定问题由于其简洁性而常常被作为计算理论研究的对象．本文中不加说明时，「问题」都指「判定问题」，当然，有时一些命题也能简单地推广到其它问题上．

一个语言也可以代指「判定一个串是否属于这个语言」这个判定问题，因此，「语言」和「问题」可以视作同义词．

### 功能性问题

功能性问题的回答不止 YES/NO，可以是一个数或是其它．如，「求两个数的和」就是一个功能性问题．

任何功能性问题都可以转化为一个判定问题，如，「求两个数的和」可以转化为「判定两个数的和是否等于第三个数」．

判定问题也可以转化为一个功能性问题：求这个判定问题的指示函数，即上文中判定问题定义里的 $f$．

## 图灵机

### 确定性图灵机

不加说明时，「图灵机」往往指「确定性图灵机」，本文中也是如此．

图灵机有很多不同的定义，这里选取其中一种，其它定义下的图灵机往往与下面这种定义的图灵机计算能力等价．

图灵机是一个在一条可双向无限延伸且被划分为若干格子的纸带上进行操作的机器，其有内部状态，还有一个可以在纸带上进行修改与移动的磁针．

正式地说，图灵机是一个七元组 $M=\langle Q,\Gamma,b,\Sigma,\delta,q_0,F\rangle$，其中：

-   $Q$ 是一个有限非空的 **状态集合**；
-   $\Gamma$ 是一个有限非空的 **磁带字母表**；
-   $b\in\Gamma$ 是 **空字符**，它是唯一一个在计算过程中可以在磁带上无限频繁地出现的字符；
-   $\Sigma\subseteq(\Gamma\setminus\{b\})$ 是 **输入符号集**，是可以出现在初始磁带（即输入）上的字符；
-   $q_0\in Q$ 是 **初始状态**；
-   $F\subseteq Q$ 是 **接受状态**，如果一个图灵机在某个接受状态停机，则称初始磁带上的内容被这个图灵机 **接受**．
-   $\delta :(Q\setminus F)\times \Gamma \not \to Q\times \Gamma \times \{L,R\}$ 是一个被称作 **转移函数** 的 partial function（即只对定义域的一个子集有定义的函数）．如果 $\delta$ 在当前状态下没有定义，则图灵机停机．

图灵机从初始状态与纸带起点起，每次根据当前的内部状态 $x$ 和当前磁针指向的纸带上的单元格中的字符 $y$ 进行操作：若 $\delta(x, y)$ 没有定义则停机，否则若 $\delta(x, y)=(a, b, c)$，则将内部状态修改为 $a$，将磁针指向的格子中的字符修改为 $b$，若 $c$ 为 $L$ 则向左移动一格，为 $R$ 则向右移动一格．

其实，知道图灵机的工作细节是不必要的，只需建立直观理解即可．

图灵机 $M$ 在输入 $x$ 下的输出记作 $M(x)$（$M(x)=1$ 当且仅当 $M$ 接受 $x$，$M(x)=0$ 当且仅当 $M$ 在输入 $x$ 下在有限步骤内停机且 $M$ 不接受 $x$），也可以在括号内包含多个参数，用逗号隔开，具体实现时可以向字母表中添加一个元素表示逗号来隔开各个参数．

图灵机与冯·诺依曼计算机解决问题的时间复杂度差别在多项式级别内，所以研究复杂度类时可以使用图灵机作为计算模型．

### 非确定性图灵机

非确定型图灵机是图灵机的一种，它与确定型图灵机的不同在于：确定型图灵机的每一步只能转移到一个状态，而非确定型图灵机可以「同时」转移到多个状态，从而在多个「分支」并行计算，一旦这些「分支」中有一个在接受状态停机，则此非确定性图灵机接受这个输入．

事实上，任何确定型图灵机都可以用类似于迭代加深搜索的方式在指数级时间内模拟一台非确定型图灵机多项式时间内的行为．

在现实生活中，确定型图灵机相当于单核处理器，只支持串行处理；而非确定型图灵机相当于理想的多核处理器，支持无限大小的并行处理．

### 多带图灵机

标准的图灵机只能在一条纸带上进行操作，但为了方便，本文中研究多带图灵机．对于一个 $k$ 带图灵机，其中一条纸带是只读的输入带，而剩下的 $k-1$ 条纸带可以进行读写，并且这 $k-1$ 条纸带中还有一条纸带用作输出．

多带图灵机的纸带数必须是有限的．

对于一个多带图灵机，它使用的空间是磁头在除输入带外的其它纸带上所访问过的单元格数目．

### 图灵机的编码

图灵机可以被自然数编码，即存在满射函数 $f:\mathbb{N}\to\mathbb{M}$，使得每个自然数都对应一个图灵机，而每个图灵机都有无数个编码．因此，由若干图灵机构成的集合可以是一个语言．

记由自然数 $\alpha$ 编码的图灵机为 $M_{\alpha}$．

### 通用图灵机

存在一台图灵机 $\mathcal U$ 满足：

1.  若 $M_{\alpha}$ 在输入 $x$ 下在有限时间内停机，则 $\mathcal{U}(x, \alpha)=M_{\alpha}(x)$，否则 $\mathcal{U}(x, \alpha)$ 不会在有限时间内停机；
2.  如果对于任意 $x\in\{0, 1\}^\ast$，$M_\alpha$ 在输入 $x$ 下在 $T(|x|)$ 时间内停机，则对于任意 $x\in\{0, 1\}^\ast$，$\mathcal{U}(x, \alpha)$ 在 $O(T(|x|)\log T(|x|))$ 时间内停机．

即：存在一台通用图灵机，它能模拟任何一台图灵机，且花费的时间只会比这台被模拟的图灵机慢其运行时间的对数．

## 可计算性

### 不可计算问题

对于一个判定问题，若存在一个总是在有限步内停机且能够正确进行判定的图灵机，则这个问题是一个 **图灵可计算** 的问题，否则这个问题是一个 **图灵不可计算** 的问题．

由于图灵机可以被自然数编码，所以图灵机的个数是可数无穷，而语言（即二进制串的集合）的个数是不可数无穷，而每个图灵机最多判定一个语言，所以一定存在图灵不可计算的问题．

### 停机问题

停机问题是一个经典的图灵不可计算问题：给定 $\alpha$ 和 $x$，判定 $M_{\alpha}$ 在输入为 $x$ 时是否会在有限步内停机．

??? note "停机问题是图灵不可计算的证明"
    定义函数 $\mathsf{UC}:\{0,1\}^\ast\to\{0,1\}$ 为：
    
    $$
    \mathsf{UC}(\alpha)=\begin{cases}0&M_\alpha(\alpha)=1\\1&\text{otherwise}\end{cases}
    $$
    
    我们先证明 $\mathsf{UC}$ 函数是图灵不可计算的：
    
    假设存在一台图灵机 $M_{\beta}$ 能够计算 $\mathsf{UC}$，那么根据 $\mathsf{UC}$ 的定义可以得到 $\mathsf{UC}(\beta)=1\iff M_\beta(\beta)\neq 1$，而根据 $M_{\beta}$ 能够计算 $\mathsf{UC}$ 可以得到 $M_{\beta}(\beta)=\mathsf{UC}(\beta)$，产生了矛盾，所以假设不成立，不存在可以计算 $\mathsf{UC}$ 的图灵机．
    
    令 $M_{\mathsf{HALT}}$ 是一个可以解决停机问题的图灵机，$M_{\mathsf{HALT}}(x,\alpha)$ 的值是判定问题 $M_\alpha$ 在输入为 $x$ 时是否会在有限步内停机的解，那么我们可以构造出一台能够计算 $\mathsf{UC}$ 函数的图灵机 $M_{\mathsf{UC}}$：
    
    $M_\mathsf{UC}$ 首先调用 $M_\mathsf{HALT}(α,α)$, 如果它输出 $0$, 则 $M_\mathsf{UC}(α)=1$；否则，$M_\mathsf{UC}$ 使用通用图灵机模拟计算得到答案．
    
    由于 $\mathsf{UC}$ 函数是图灵不可计算的，所以 $M_\mathsf{HALT}$ 不存在，也就是说停机问题是图灵不可计算的．

## 丘奇 - 图灵论题

丘奇 - 图灵论题称，若一类问题有一个有效的方法解决，则这类问题可以被某个图灵机解决．

其中，「有效的方法」需要满足：

1.  包含有限条清晰的指令；
2.  当用其解决这类问题的其中一个时，这个方法需要在有限步骤内结束，且得到正确的答案．

这个论题没有被证明，但其是计算理论的一条基本公理．

## 复杂度类

复杂度类有很多，本文只会介绍其中较为常见的一小部分．

### R 和 RE

对于语言 $L$ 和图灵机 $M$，若 $M$ 在任何输入下都能在有限步骤内停机，且 $M(x)=1\iff x\in L$，则称 $M$ 能够 **判定**  $L$．

对于语言 $L$ 和图灵机 $M$，若对于任何属于 $L$ 的输入，$M$ 都在有限步骤内停机，且 $M(x)=1\iff x\in L$，则称 $M$ 能够 **识别**  $L$．

复杂度类 $\mathsf R$ 表示那些可以被某台图灵机判定的语言的集合，即所有图灵可计算的语言．

复杂度类 $\mathsf{RE}$ 表示那些可以被某台图灵机识别的语言的集合．$\mathsf{RE}$ 也被称作递归可枚举语言．

由定义可以得到 $\mathsf{R}\subseteq\mathsf{RE}$．

### DTIME

如果存在一台确定性图灵机能够判定一个语言，且对于任何输入 $x$，这台图灵机可以在 $O(f(|x|))$ 的时间内停机，那么这个语言属于 $\mathsf{DTIME}(f(n))$ 类．

### P

复杂度类 $\mathsf P$ 表示可以由确定性图灵机在多项式时间内解决的判定问题，即：

$$
\mathsf{P}=\bigcup\limits_{k\in\mathbb{N}}\mathsf{DTIME}(n^k)
$$

线性规划、计算最大公约数、求图的最大匹配的判定版本都是 $\mathsf P$ 类问题．

### EXPTIME

复杂度类 $\mathsf{EXPTIME}$ 表示可以由确定性图灵机在指数级时间内解决的判定问题，即：

$$
\mathsf{EXPTIME}=\bigcup\limits_{k\in\mathbb{N}}\mathsf{DTIME}(2^{n^k})
$$

停机问题的弱化版——给定一个图灵机的编码以及一个正整数 $k$，判定这个图灵机是否在 $k$ 步内停机，是一个 $\mathsf{EXPTIME}$ 类的问题．因为这个问题的解法需要 $O(k)$ 的时间，而数字 $k$ 可以被编码为长度为 $O(\log k)$ 的二进制串．

### NTIME

如果存在一台非确定性图灵机能够判定一个语言，且对于任何输入 $x$，这台图灵机可以在 $O(f(|x|))$ 的时间内停机，那么这个语言属于 $\mathsf{NTIME}(f(n))$ 类．

### NP

复杂度类 $\mathsf{NP}$ 表示可以由非确定性图灵机在多项式时间内解决的判定问题，即：

$$
\mathsf{NP}=\bigcup\limits_{k\in\mathbb{N}}\mathsf{NTIME}(n^k)
$$

所有 $\mathsf P$ 类问题都是 $\mathsf{NP}$ 类问题．更多 $\mathsf{NP}$ 类问题请参见下文中的 NPC 问题以及 NP-intermediate 问题．

#### NP-hard

如果所有 $\mathsf{NP}$ 类问题都可以在多项式时间内规约到问题 $H$，那么问题 $H$ 是 NP-hard 的．

换句话说，如果可以在一单位的时间内解决 NP-hard 的问题 $H$，那么所有 $\mathsf{NP}$ 类问题都可以在多项式单位的时间内解决．

#### NP-complete

如果一个问题既是 $\mathsf{NP}$ 类问题又是 NP-hard 的，那么这个问题是 NP 完全 (NP-complete) 的，或者说这是一个 NPC 问题．

一些经典的 NPC 问题：旅行商问题的判定版本、最大独立集问题的判定版本、最小点覆盖问题的判定版本、最长路问题的判定版本、0-1 整数规划问题的判定版本、集合覆盖问题、图着色问题、背包问题、三维匹配问题、最大割问题的判定版本．

NPC 问题的功能性版本往往是 NP-hard 的，例如：「判定一张图中是否存在大小为 $k$ 的团」既是一个 $\mathsf{NP}$ 类问题又是 NP-hard 的，从而它是一个 NPC 问题，而它的功能性版本「求一张图的最大团」不是 NPC 问题，但这个功能性版本依然是 NP-hard 的．

类似地，其它复杂度类也会有「XX-complete」，如所有 $\mathsf{EXPTIME}$ 类的问题都能在多项式时间内规约到 EXPTIME-complete 的问题．

#### co-NP

一个问题是 $\mathsf{co-NP}$ 类问题，当且仅当它的补集是 $\mathsf{NP}$ 类问题．如果将「问题」理解为「语言」，而「语言」是 $\Sigma^\ast$ 的子集，就能理解「补集」了．

例如：「给定 $n$ 个子集，判断是否能够从中选取 $k$ 个，覆盖整个集合」是一个 NPC 问题，而其补集「给定 $n$ 个子集，判断是否从中任取 $k$ 个都不能覆盖整个集合」是一个 $\mathsf{co-NP}$ 类问题．如果第一个问题的答案是「是」，那么相当于找到了第二个问题的一组反例，从而第二个问题的答案是「否」．

#### NP-intermediate

如果一个问题是 $\mathsf{NP}$ 类问题，但它既不是 $\mathsf{P}$ 类问题也不是 NPC 问题，则称其为 NP-intermediate 问题．

就人们目前的了解，图同构问题、离散对数问题和因数分解问题可能是 NP-intermediate 的．

Ladner 定理指出，如果 $\mathsf{P}\ne\mathsf{NP}$，则一定存在问题是 NP-intermediate 的．

### NEXPTIME

复杂度类 $\mathsf{NEXPTIME}$ 表示可以由非确定性图灵机在指数级时间内解决的判定问题，即：

$$
\mathsf{NEXPTIME}=\bigcup\limits_{k\in\mathbb{N}}\mathsf{NTIME}(2^{n^k})
$$

### #P

$\mathsf{\#P}$ 类问题不是判定问题，而是关于 $\mathsf{NP}$ 类问题的计数问题：数一个 $\mathsf{NP}$ 类问题的解的个数是一个 $\mathsf{\#P}$ 类的问题．换句话说，数一个串在一个总是在多项式时间内停机的非确定性图灵机的多少个分支处被接受是一个 $\mathsf{\#P}$ 类的问题．

求一张普通图或二分图的匹配或完美匹配个数都是 #P 完全的，对应的判定问题为「判定一张图是否存在（完美）匹配」．

### DSPACE

如果存在一台确定性图灵机能够在输入为 $x$ 时在 $O(f(|x|))$ 的空间内判定一个语言，那么这个语言属于 $\mathsf{DSPACE}(f(n))$ 类．

-   $\mathsf{REG}=\mathsf{DSPACE}(O(1))$，即正则语言，也就是自动机能够判定的语言．

-   $\mathsf{L}=\mathsf{DSPACE}(O(\log n))$，需要注意的是图灵机使用的空间不包括输入占用的空间．

-   $\mathsf{PSPACE}=\bigcup\limits_{k\in\mathbb N}\mathsf{DSPACE}(n^k)$

-   $\mathsf{EXPSPACE}=\bigcup\limits_{k\in\mathbb N}\mathsf{DSPACE}(2^{n^k})$

### NSPACE

如果存在一台非确定性图灵机能够在输入为 $x$ 时在 $O(f(|x|))$ 的空间内判定一个语言，那么这个语言属于 $\mathsf{NSPACE}(f(n))$ 类．

-   $\mathsf{REG}=\mathsf{DSPACE}(O(1))=\mathsf{NSPACE}(O(1))$

-   $\mathsf{NL}=\mathsf{NSPACE}(O(\log n))$

-   $\mathsf{CSL}=\mathsf{NSPACE}(O(n))$，即上下文相关语言．

-   $\mathsf{PSPACE}=\mathsf{NPSPACE}=\bigcup\limits_{k\in\mathbb N}\mathsf{NSPACE}(n^k)$

-   $\mathsf{EXPSPACE}=\mathsf{NEXPSPACE}=\bigcup\limits_{k\in\mathbb N}\mathsf{NSPACE}(2^{n^k})$

## 多项式时间

简单来说，如果存在正数 $k$ 使得一个算法的时间复杂度为 $O(n^k)$（注意，不是 $\Theta(n^k)$），其中 $n$ 为问题规模（输入的长度），则称这个算法是 **多项式时间** 的．如果一个问题有（确定性图灵机上的）多项式时间的算法来解决，则这个问题属于复杂度类 $\mathsf{P}$．

多项式时间可分为强多项式时间和弱多项式时间，除此之外还有伪多项式时间．

### Strongly polynomial time 强多项式时间

我们先定义一个计算模型，称作算术模型．在算术模型中，数字之间的算术运算（加减乘除、比较大小）可以在单位时间内完成（即 $O(1)$ 时间内完成，与数字大小无关）．

如果一个算法在算术模型下的操作数是输入中的数字个数的多项式，并且空间复杂度是输入规模（而非数字个数）的多项式，则这个算法是 **强多项式时间** 的．由于算术操作在一般的计算模型下可以在输入规模（即数字大小的对数）的多项式时间内完成，强多项式时间的算法一定是多项式时间的．

一般来说，强多项式时间的算法的时间复杂度与值域无关．

### Weakly polynomial time 弱多项式时间

如果一个算法是多项式时间的但不是强多项式时间的，则它是 **弱多项式时间** 的．

例如，计算最大公约数的欧几里得算法，时间复杂度为 $O(\log a + \log b)$（$a$ 和 $b$ 为输入的数的大小），是弱多项式时间的．

### Pseudo-polynomial time 伪多项式时间

如果一个算法的用时是值域的多项式，则称它是 **伪多项式时间** 的．伪多项式时间的算法可能是多项式时间的也可能不是，可能不是多项式时间是因为表示一个大小为 $n$ 的正整数一般只需要 $O(\log n)$ 个二进制位，所以关于值域多项式时间的算法往往关于输入长度是指数级时间的．虽然从定义上来说伪多项式时间也可能是多项式时间，但当我们说一个算法是伪多项式时间的，一般都是说这个算法不是多项式时间的．

例如，背包问题是 NP-hard 问题，但它有基于动态规划的伪多项式时间的解法．

如果一个 NPC/NP-hard 问题有伪多项式时间的解法，则称这个问题是 **弱 NPC**/**弱 NP-hard** 问题．如果一个 NPC/NP-hard 问题在 $\mathsf{P} \ne \mathsf{NP}$ 的前提下没有伪多项式时间的解法，则称这个问题是 **强 NPC**/**强 NP-hard** 问题．

## 可构造函数

### 时间可构造函数

有时，我们想让图灵机知道自己用了多长的时间，例如，强制图灵机在进行 $T(n)$ 步计算后停机．但如果计算 $T(n)$ 的用时就超过了 $T(n)$，这便是不可做到的．为此，定义了时间可构造函数，来避免这样的麻烦．

如果存在图灵机 $M$，使得输入为 $1^n$($n$ 个 1) 时 $M$ 能在 $O(f(n))$ 的时间内停机并且输出 $f(n)$ 的二进制表示（注意，这里的图灵机的输出不是接受/不接受，而是一个串，输出可以在纸带上进行），则 $f(n)$ 是一个 **时间可构造函数**．

由于读入需要 $O(n)$ 的时间，$o(n)$ 的非常值函数都不是时间可构造函数．

### 空间可构造函数

类似地可以定义空间可构造函数．

如果存在图灵机 $M$，使得输入为 $1^n$($n$ 个 1) 时 $M$ 能在 $O(f(n))$ 的空间内停机并且输出 $f(n)$ 的二进制表示，则 $f(n)$ 是一个 **空间可构造函数**．

## 复杂度类之间的关系

### 时间谱系定理

#### 确定性时间谱系定理

若 $f(n)$ 是一个时间可构造函数，则：

$$
\mathsf {DTIME}\left(o\left({\frac {f(n)}{\log f(n)}}\right)\right)\subsetneq \mathsf {DTIME}(f(n))
$$

由确定性时间谱系定理可以得到 $\mathsf{P}\subsetneq\mathsf{EXPTIME}$．

??? note "确定性时间谱系定理的证明"
    定义语言 $L=\{(x, y)|\mathcal{U}((x, y), x)\text{ 在 }f(|x|+|y|)\text{ 时间内停机并拒绝}\}$，由于 $f(n)$ 是一个时间可构造函数，可以根据定义进行计算来判定 $L$，用时为 $O(f(|x|+|y|))$，所以 $L\in\mathsf{DTIME}(f(n))$．
    
    现在假设 $L\in\mathsf{DTIME}(o\left({\dfrac {f(n)}{\log f(n)}}\right))$，设 $M_z$ 就是那台在 $o\left({\dfrac {f(n)}{\log f(n)}}\right)$ 的时间内判定 $L$ 的图灵机．
    
    令通用图灵机 $\mathcal{U}(x, z)$ 关于 $x$ 的用时为 $g(|x|)$，由上文关于通用图灵机的介绍可以得到 $g(n)=o(f(n))$，所以，当 $y$ 足够大时，$g(|z|+|y|)<f(|z|+|y|)$．
    
    令 $y'$ 是一个足够大的 $y$，那么 $\mathcal{U}((z, y'), z)$ 一定能在 $f(|z|+|y'|)$ 时间内停机，从而 $M_z(z, y')\ne M_z(z, y')$，产生矛盾，所以假设不成立，确定性时间谱系定理证毕．

#### 非确定性时间谱系定理

若 $g(n)$ 是一个时间可构造函数，并且 $f(n+1)=o(g(n))$，则 $\mathsf{NTIME}(f(n))\subsetneq\mathsf{NTIME}(g(n))$．

由非确定性时间谱系定理可以得到 $\mathsf{NP}\subsetneq\mathsf{NEXPTIME}$．

### 空间谱系定理

若 $f(n)$ 是一个空间可构造函数且 $f(n)=\Omega(\log n)$，则 $\mathsf{SPACE}(o(f(n)))\subsetneq\mathsf{SPACE}(f(n))$．

其中 $\mathsf{SPACE}$ 可以代指 $\mathsf{DSPACE}$ 或 $\mathsf{NSPACE}$．

由空间谱系定理可以得到 $\mathsf{PSPACE}\subsetneq\mathsf{EXPSPACE}$．

### 萨维奇定理

一台确定性图灵机可以在一台非确定性图灵机所消耗空间的平方内模拟它（尽管消耗的时间可能多很多），即：

若 $f(n)=\Omega(\log n)$，则：

$$
\mathsf{NSPACE}\left(f\left(n\right)\right)\subseteq \mathsf {DSPACE}\left(\left(f\left(n\right)\right)^2\right)
$$

推论：$\mathsf{PSPACE}=\mathsf{NPSPACE}$，$\mathsf{EXPSPACE}=\mathsf{NEXPSPACE}$．

### P?=NP

复杂度类 $\mathsf{P}$ 与 $\mathsf{NP}$ 是否相等是计算复杂度理论中一个著名的尚未解决的问题．

若 $\mathsf{P}=\mathsf{NP}$，可以得到 $\mathsf{NP}=\mathsf{co-NP}$，但反之不行（目前没有基于 $\mathsf{NP}=\mathsf{co-NP}$ 证明 $\mathsf{P}=\mathsf{NP}$ 的方法）．

???+ note "为什么 NP?=co-NP 不是显然的？"
    由于 $\mathsf{NP}$ 问题和与其对应的 $\mathsf{co-NP}$ 问题答案相反，很容易有这种想法：对于一个 $\mathsf{co-NP}$ 问题，我只要将解决其补集的非确定性图灵机的输出反过来，就解决了该 $\mathsf{co-NP}$ 问题，所以 $\mathsf{NP}=\mathsf{co-NP}$．
    
    实际上，上面所说的这种方法确实能够解决该 $\mathsf{co-NP}$ 问题，但并没有找到一个非确定性图灵机来解决它：如果一个图灵机所做的事情是将一个非确定性图灵机的输出反过来，该图灵机并不是一个非确定性图灵机．因为，非确定性图灵机接受是在某个分支处接受，而拒绝是在所有分支处拒绝；而将其输出反过来，就变成了接受是在所有分支处，而拒绝是在一个分支处，而这样就不符合非确定性图灵机的定义了，所以能用该图灵机解决这个 $\mathsf{co-NP}$ 问题并不能使这个 $\mathsf{co-NP}$ 问题变成一个 $\mathsf{NP}$ 问题．

若 $\mathsf{P}=\mathsf{NP}$，还可以得到 $\mathsf{EXPTIME}=\mathsf{NEXPTIME}$．

若 $\mathsf{P}\ne\mathsf{NP}$，可以得到 NP-intermediate 不为空．

## 参考资料

1.  [计算复杂性（1）自动机与正则语言](https://lingerois.com/p/%E8%AE%A1%E7%AE%97%E5%A4%8D%E6%9D%82%E6%80%A71-%E8%87%AA%E5%8A%A8%E6%9C%BA%E4%B8%8E%E6%AD%A3%E5%88%99%E8%AF%AD%E8%A8%80/)；

2.  [计算复杂性（2）图灵机与可计算性](https://lingerois.com/p/%E8%AE%A1%E7%AE%97%E5%A4%8D%E6%9D%82%E6%80%A72-%E5%9B%BE%E7%81%B5%E6%9C%BA%E4%B8%8E%E5%8F%AF%E8%AE%A1%E7%AE%97%E6%80%A7/)；

3.  [Wikipedia](https://en.wikipedia.org/) 的相关词条以及这些词条的参考资料．


## misc/cdq-divide.md

本页面将介绍 CDQ 分治．

## 简介

CDQ 分治是一种思想而不是具体的算法，与 [动态规划](../dp/index.md) 类似．目前这个思想的拓展十分广泛，依原理与写法的不同，大致分为三类：

-   解决和点对有关的问题．
-   1D 动态规划的优化与转移．
-   通过 CDQ 分治，将一些动态问题转化为静态问题．

CDQ 分治的思想最早由 IOI2008 金牌得主陈丹琦在高中时整理并总结，它也因此得名．[^ref1]

## 解决和点对有关的问题

这类问题多数类似于「给定一个长度为 $n$ 的序列，统计有一些特性的点对 $(i,j)$ 的数量」或「给定一个长度为 $n$ 的序列，找到一对点 $(i,j)$ 使得一些函数的值最大」．

CDQ 分治解决这类问题的算法流程如下：

1.  找到这个序列的中点 $mid$；

2.  将所有点对 $(i,j)$ 划分为 3 类：

    1.  $1 \leq i \leq mid,1 \leq j \leq mid$ 的点对；
    2.  $1  \leq i \leq mid ,mid+1 \leq j \leq n$ 的点对；
    3.  $mid+1 \leq  i \leq n,mid+1 \leq j \leq n$ 的点对．

3.  将 $(1,n)$ 这个序列拆成两个序列 $(1,mid)$ 和 $(mid+1,n)$．此时第一类点对和第三类点对都在这两个序列之中；

4.  递归地处理这两类点对；

5.  设法处理第二类点对．

可以看到 CDQ 分治的思想就是不断地把点对通过递归的方式分给左右两个区间．

在实际应用时，我们通常使用一个函数 `solve(l,r)` 处理 $l \leq i \leq r,l \leq j \leq r$ 的点对．上述算法流程中的递归部分便是通过 `solve(l,mid)` 与 `solve(mid+1,r)` 来实现的．剩下的第二类点对则需要额外设计算法解决．

### 例题

???+ example "[三维偏序](https://www.luogu.com.cn/problem/P3810)"
    给定一个序列，每个点有 $a_i,b_i,c_i$ 三个属性，试求：这个序列里有多少对点对 $(i,j)$ 满足 $a_j \leq a_i$ 且 $b_j \leq b_i$ 且 $c_j \leq c_i$ 且 $j \ne i$．

??? note "解题思路"
    三维偏序是 CDQ 分治的经典问题．
    
    题目要求统计序列里点对的个数，那试一下用 CDQ 分治．
    
    首先将序列按 $a$ 排序．
    
    假设我们现在写好了 `solve(l,r)`，并且通过递归搞定了 `solve(l,mid)` 和 `solve(mid+1,r)`．现在我们要做的，就是统计满足 $l \leq i \leq mid$，$mid+1 \leq j \leq r$ 的点对 $(i,j)$ 中，有多个点对还满足 $a_{i} \leq a_{j}$，$b_{i} \leq b_{j}$，$c_{i} \leq c_{j}$ 的限制条件．
    
    稍微思考一下就会发现，那个 $a_{i} \leq a_{j}$ 的限制条件没啥用了：既然 $i$ 比 $mid$ 小，$j$ 比 $mid$ 大，那 $i$ 肯定比 $j$ 要小；已经将序列按 $a$ 排序，就一定有 $a_{i} \leq a_{j}$．现在还剩下两个限制条件：$b_{i} \leq b_{j}$ 与 $c_{i} \leq c_{j}$．根据这个限制条件我们就可以枚举 $j$, 求出有多少个满足条件的 $i$．
    
    为了方便枚举，我们把 $(l,mid)$ 和 $(mid+1,r)$ 中的点全部按照 $b$ 的值从小到大排个序．之后我们依次枚举每一个 $j$, 把所有 $b_{i} \leq b_{j}$ 的点 $i$ 全部插入到某种数据结构里（这里我们选择 [树状数组](../ds/fenwick.md)）．此时只要查询树状数组里有多少个点的 $c$ 值是小于等于 $c_{j}$ 的，我们就求出了对于这个点 $j$，有多少个 $i$ 可以合法匹配它了．
    
    当我们插入一个 $c$ 值等于 $x$ 的点时，我们就令树状数组的 $x$ 这个位置单点加一，而查询树状数组里有多少个点小于 $x$ 的操作实际上就是在求 [前缀和](../basic/prefix-sum.md)，只要我们事先对于所有的 $c$ 值做了 [离散化](../misc/discrete.md)，我们的复杂度就是对的．
    
    对于每一个 $j$，我们都需要将所有 $b_{i} \leq b_{j}$ 的点 $i$ 插入树状数组中．由于所有的 $i$ 和 $j$ 都已事先按照 $b$ 值排好序，这样的话只要以双指针的方式在树状数组里插入点，则对树状数组的插入操作就能从 $O(n^2)$ 次降到 $O(n)$ 次．
    
    通过这样一个算法流程，我们就用 $O(n\log n)$ 的时间处理完了关于第二类点对的信息了．此时算法的时间复杂度是 $T(n)=T(\lfloor \frac{n}{2} \rfloor)+T(\lceil \frac{n}{2} \rceil)+O(n\log n)=O(n\log^2n)$．

??? note "示例代码"
    ```cpp
    --8<-- "docs/misc/code/cdq-divide/cdq-divide_1.cpp"
    ```

???+ example "[CQOI2011 动态逆序对](https://www.luogu.com.cn/problem/P3157)"
    对于序列 $a$，它的逆序对数定义为集合 $\{(i,j)| i < j \wedge a_i > a_j \}$ 中的元素个数．
    
    现在给出 $1\sim n$ 的一个排列，按照某种顺序依次删除 $m$ 个元素，你的任务是在每次删除一个元素之前统计整个序列的逆序对数．

??? note "示例代码"
    ```cpp
    --8<-- "docs/misc/code/cdq-divide/cdq-divide_2.cpp"
    ```

## CDQ 分治优化 1D/1D 动态规划的转移

相关内容：[CDQ 分治优化 DP](../dp/opt/dp-opt.md#cdq-分治优化-dp)

1D/1D 动态规划指的是一类特定的 DP 问题，该类题目的特征是 DP 数组是一维的，转移是 $O(n)$ 的．如果条件良好的话，有时可以通过 CDQ 分治来把它们的时间复杂度由 $O(n^2)$ 降至 $O(n\log^2n)$．

例如，给定一个序列，每个元素有两个属性 $a$，$b$．我们希望计算一个 DP 式子的值，它的转移方程如下：

$dp_{i}=1+ \max_{j=1}^{i-1}dp_{j}[a_{j} < a_{i}][b_{j} < b_{i}]$

这是一个二维最长上升子序列的 DP 方程，即只有 $j < i,a_{j} < a_{i},b_{j} < b_{i}$ 的点 $j$ 可以更新点 $i$ 的 DP 值．

直接转移显然是 $O(n^2)$ 的．以下是使用 CDQ 分治优化转移过程的讲解．

我们发现 $dp_{j}$ 转移到 $dp_{i}$ 这种转移关系也是一种点对间的关系，所以我们用类似 CDQ 分治处理点对关系的方式来处理它．

这个转移过程相对来讲比较套路．假设现在正在处理的区间是 $(l,r)$，算法流程大致如下：

1.  如果 $l=r$，说明 $dp_{r}$ 值的 $\max$ 部分已经被计算好了，直接令 $dp_{r} \gets dp_{r} + 1$ 然后返回即可；
2.  递归使用 `solve(l,mid)`；
3.  处理所有 $l \leq j \leq mid$，$mid+1 \leq i \leq r$ 的转移关系；
4.  递归使用 `solve(mid+1,r)`．

第三步的做法与 CDQ 分治求三维偏序差不多．处理 $l \leq j \leq mid$，$mid+1 \leq i \leq r$ 的转移关系的时候，我们会发现已经不用管 $j < i$ 这个限制条件了．因此，我们依然先将所有的点 $i$ 和点 $j$ 按 $a$ 值进行排序处理，然后用双指针的方式将 $j$ 点插入到树状数组里，最后查一下前缀最大值更新一下 $dp_{i}$ 就可以了．

### 转移过程的正确性证明

该 CDQ 写法和处理点对间关系的 CDQ 写法最大的不同就是处理 $l \leq j \leq mid$，$mid+1 \leq i \leq r$ 的点对这一部分．处理点对间关系的 CDQ 写法中，这一部分放到哪里都是可以的．但是，在用 CDQ 分治优化 DP 的时候，这个流程却必须夹在 $solve(l,mid)$,$solve(mid+1,r)$ 的中间．原因是 DP 的转移是 **有序的**，它必须满足两个条件，否则就是不对的：

1.  用来计算 $dp_{i}$ 的所有 $dp_{j}$ 值都必须是已经计算完毕的，不能存在「半成品」；

2.  用来计算 $dp_{i}$ 的所有 $dp_{j}$ 值都必须能更新到 $dp_{i}$，不能存在没有更新到的 $dp_{j}$ 值．

上述两个条件可能在 $O(n^2)$ 暴力的时候是相当容易满足的，但是使用 CDQ 分治后，转移顺序很显然已经乱掉了，所以有必要考察转移的正确性．

CDQ 分治的递归树如下所示．

![CDQ 分治的递归树](./images/cdq-divide.svg)

执行刚才的算法流程的话，以 $8$ 这个点为例，它的 DP 值是在 `solve(1,8)`、`solve(5,8)`、`solve(7,8)` 这 3 个函数中更新完成的，而三次用来更新它的点分别是 $(1,4)$、$(5,6)$、$(7,7)$ 这三个不相交的区间；又以 $5$ 这个点为例，它的 DP 值是在 `solve(1,4)` 函数中解决的，更新它的区间是 $(1,4)$．仔细观察就会发现，一个 $i$ 点的 DP 值被更新了 $\log$ 次，而且，更新它的区间刚好是 $(1,i)$ 在线段树上被拆分出来的 $\log$ 个区间．因此，我们的确保证了所有合法的 $j$ 都更新过点 $i$，满足第 2 个条件．

接着分析我们算法的执行流程：

1.  第一个结束的函数是 `solve(1,1)`．此时我们发现 $dp_{1}$ 的值已经计算完毕了；
2.  第一个执行转移过程的函数是 `solve(1,2)`．此时我们发现 $dp_{2}$ 的值已经被转移好了；
3.  第二个结束的函数是 `solve(2,2)`．此时我们发现 $dp_{2}$ 的值已经计算完毕了；
4.  接下来 `solve(1,2)` 结束，$(1,2)$ 这段区间的 $dp$ 值均被计算好；
5.  下一个执行转移流程的函数是 `solve(1,4)`．这次转移结束之后我们发现 $dp_{3}$ 的值已经被转移好了；
6.  接下来结束的函数是 `solve(3,3)`．我们会发现 $dp_{3}$ 的 dp 值被计算好了；
7.  接下来执行的转移是 `solve(3,4)`．此时 $dp_{4}$ 在 `solve(1,4)` 中被 $(1,2)$ 转移了一次，这次又被 $(3,3)$ 转移了，因此 $dp_{4}$ 的值也被转移好了；
8.  `solve(4,4)` 结束，$dp_{4}$ 的值计算完毕；
9.  `solve(3,4)` 结束，$(3,4)$ 的值计算完毕；
10. `solve(1,4)` 结束，$(1,4)$ 的值计算完毕．
11. ……

通过模拟函数流程，我们发现一件事：每次 `solve(l,r)` 结束的时候，$(l,r)$ 区间的 DP 值会被全部计算好．由于我们每一次执行转移函数的时候，`solve(l,mid)` 已经结束，因此我们每一次执行的转移过程都是合法的，满足第 1 个条件．

在刚才的过程我们发现，如果将 CDQ 分治的递归树看成一颗线段树，那么 CDQ 分治就是这个线段树的 **中序遍历函数**，因此我们相当于按顺序处理了所有的 DP 值，只是转移顺序被拆开了而已，所以算法是正确的．

### 例题

???+ example "[SDOI2011 拦截导弹](https://www.luogu.com.cn/problem/P2487)"
    某国为了防御敌国的导弹袭击，发展出一种导弹拦截系统．但是这种导弹拦截系统有一个缺陷：虽然它的第一发炮弹能够到达任意的高度、并且能够拦截任意速度的导弹，但是以后每一发炮弹都不能高于前一发的高度，其拦截的导弹的飞行速度也不能大于前一发．某天，雷达捕捉到敌国的导弹来袭．由于该系统还在试用阶段，所以只有一套系统，因此有可能不能拦截所有的导弹．
    
    在不能拦截所有的导弹的情况下，我们当然要选择使国家损失最小、也就是拦截导弹的数量最多的方案．但是拦截导弹数量的最多的方案有可能有多个，如果有多个最优方案，那么我们会随机选取一个作为最终的拦截导弹行动蓝图．
    
    我方间谍已经获取了所有敌军导弹的高度和速度，你的任务是计算出在执行上述决策时，每枚导弹被拦截掉的概率．

??? note "示例代码"
    ```cpp
    --8<-- "docs/misc/code/cdq-divide/cdq-divide_3.cpp"
    ```

## 将动态问题转化为静态问题

前两种情况使用 CDQ 分治的目的是将序列折半之后递归处理点对间的关系，来获得良好的复杂度．不过在本节中，折半的不是一般的序列，而是时间序列．

它适用于一些「需要支持做 xxx 修改然后做 xxx 询问」的数据结构题．该类题目有两个特点：

-   如果把询问 [离线](offline.md)，所有操作会按照时间自然地排成一个序列．
-   每一个修改均与之后的询问操作息息相关．而这样的「修改 - 询问」关系一共会有 $O(n^2)$ 对．

我们可以使用 CDQ 分治对于这个操作序列进行分治，处理修改和询问之间的关系．

与处理点对关系的 CDQ 分治类似，假设正在分治的序列是 $(l,r)$, 我们先递归地处理 $(l,mid)$ 和 $(mid,r)$ 之间的修改 - 询问关系，再处理所有 $l \leq i \leq mid$，$mid+1 \leq j \leq r$ 的修改 - 询问关系，其中 $i$ 是一个修改，$j$ 是一个询问．

注意，如果各个修改之间是 **独立** 的话，我们无需处理 $l \leq i \leq mid$ 和 $mid+1 \leq j \leq r$，以及 `solve(l,mid)` 和 `solve(mid+1,r)` 之间的时序关系（比如普通的加减法问题）．但是如果各个修改之间并不独立（比如说赋值操作），做完这个修改后，序列长什么样可能依赖于之前的序列．此时处理所有跨越 mid 的修改 - 询问关系的步骤就必须放在 `solve(l,mid)` 和 `solve(mid+1,r)` 之间．理由和 CDQ 分治优化 1D/1D 动态规划的原因是一样的：按照中序遍历序进行分治才能保证每一个修改都是严格按照时间顺序执行的．

### 例题

???+ example "矩形加矩形求和"
    维护一个二维数组，支持在一个矩形区域内加一个数字，每次询问一个矩形区域的和．

??? note "解题思路"
    对于这个问题的无修版本，即「给定一个二维数组，多次询问一个矩形区域的和」，有一个扫描线配合线段树的经典做法．具体的做法是先将每个矩形拆成插入和删除两个操作，接着将每个询问拆成二维前缀和相减的形式，最后离线．然而，原题目是带修改的，不能直接使用这种做法．
    
    尝试对其使用 CDQ 分治．我们将所有的询问和修改操作全部离线．这些操作形成了一个序列，并且有 $O(N^2)$ 对修改 - 询问的关系．依然使用 CDQ 分治的一般流程，将所有的关系分成三类，在这一层分治过程当中只处理跨越 $mid$ 的修改 - 询问关系，剩下的修改 - 询问关系通过递归的方式来解决．
    
    我们发现，所有的修改在询问之前就已完成．这时，原问题等价于「平面上有静态的一些矩形，不停地询问一个矩形区域的和」．
    
    使用一个扫描线在 $O(n\log n)$ 的时间内处理好所有跨越 $mid$ 的修改 - 询问关系，剩下的事情就是递归地分治左右两侧的修改 - 询问关系了．
    
    在这样实现的 CDQ 分治中，同一个询问被处理了 $O(\log n)$ 次．不过没有关系，因为每次贡献这个询问的修改是互不相交的．全套流程的时间复杂度为 $T(n)=T(\lfloor \frac{n}{2} \rfloor)+T(\lceil \frac{n}{2} \rceil)+ O(n\log n)=O(n\log^2n)$．
    
    观察上述的算法流程，我们发现一开始我们只能解决静态的矩形加矩形求和问题，但只是简单地使用 CDQ 分治后，我们就可以离线地解决一个动态的矩形加矩形求和问题了．将动态问题转化为静态问题的精髓就在于 CDQ 分治每次仅仅处理跨越某一个点的修改和询问关系，这样的话我们就只需要考虑「所有询问都在修改之后」这个简单的问题了．也正是因为这一点，CDQ 分治被称为「动态问题转化为静态问题的工具」．

???+ example "[\[Ynoi2016\] 镜中的昆虫](https://www.luogu.com.cn/problem/P4690)"
    维护一个长为 $n$ 的序列 $a_i$，有 $m$ 次操作．
    
    1.  将区间 $[l,r]$ 的值修改为 $x$；
    2.  询问区间 $[l,r]$ 出现了多少种不同的数，也就是说同一个数出现多次只算一个．
    
    一句话题意：区间赋值区间数颜色．

??? note "解题思路"
    维护一下每个位置左侧第一个同色点的位置，记为 $pre_{i}$，此时区间数颜色就被转化为了一个经典的二维数点问题．
    
    通过将连续的一段颜色看成一个点的方式，可以证明 $pre$ 的变化量是 $O(n+m)$ 的，即单次操作仅仅引起 $O(1)$ 的 $pre$ 值变化，那么我们可以用 CDQ 分治来解决动态的单点加矩形求和问题．
    
    $pre$ 数组的具体变化可以使用 `std::set` 来进行处理．这个用 set 维护连续的区间的技巧也被称为 [old driver tree](./odt.md)．

??? note "示例代码"
    ```cpp
    --8<-- "docs/misc/code/cdq-divide/cdq-divide_4.cpp"
    ```

???+ example "[\[HNOI2010\] 城市建设](https://www.luogu.com.cn/problem/P3206)"
    PS 国是一个拥有诸多城市的大国．国王 Louis 为城市的交通建设可谓绞尽脑汁．Louis 可以在某些城市之间修建道路，在不同的城市之间修建道路需要不同的花费．
    
    Louis 希望建造最少的道路使得国内所有的城市连通．但是由于某些因素，城市之间修建道路需要的花费会随着时间而改变．Louis 会不断得到某道路的修建代价改变的消息．他希望每得到一条消息后能立即知道使城市连通的最小花费总和．Louis 决定求助于你来完成这个任务．
    
    一句话题意：给定一张图支持动态的修改边权，要求在每次修改边权之后输出这张图的最小生成树的最小代价和．

??? note "解题思路"
    事实上，有一个线段树分治套 lct 的做法可以解决这个问题，但是这个实现方式的常数过大，可能需要精妙的卡常技巧才可以通过本题，因此不妨考虑 CDQ 分治来解决这个问题．
    
    和一般的 CDQ 分治解决的问题不同，此时使用 CDQ 分治的时候并没有修改和询问的关系来让我们进行分治，因为无法单独考虑「修改一个边对整张图的最小生成树有什么贡献」．传统的 CDQ 分治思路似乎不是很好使．
    
    通过刚才的例题可以发现，一般的 CDQ 分治和线段树有着特殊的联系：我们在 CDQ 分治的过程中其实隐式地建了一棵线段树出来（因为 CDQ 分治的递归树就是一颗线段树）．通常的 CDQ 是考虑线段树左右儿子之间的联系．而对于这道题，我们需要考虑的是父亲和孩子之间的关系；换句话来讲，我们在 `$solve(l,r)$` 这段区间的时候，如果可以想办法使图的规模变成和区间长度相关的一个变量的话，就可以解决这个问题了．
    
    那么具体来讲如何设计算法呢？
    
    假设我们正在构造 $(l,r)$ 这段区间的最小生成树边集，并且我们已知它父亲最小生成树的边集．我们将在 $(l,r)$ 这段区间中发生变化的边分别赋与 $+ \infty$ 和 $-\infty$ 的边权，并各跑一边 kruskal，求出在最小生成树里的那些边．
    
    对于一条边来讲：
    
    -   如果最小生成树里所有被修改的边权都被赋成了 $+\infty$，而它未出现在树中，则证明它不可能出现在 $(l,r)$ 这些询问的最小生成树当中．所以我们仅仅在 $(l,r)$ 的边集中加入最小生成树的树边．
    -   如果最小生成树里所有被修改的边权都被赋成了 $-\infty$，而它出现在树中，则证明它一定会出现 $(l,r)$ 这段的区间的最小生成树当中．这样的话我们就可以使用并查集将这些边对应的点缩起来，并且将答案加上这些边的边权．
    
    这样我们就将 $(l,r)$ 这段区间的边集构造出来了．用这些边求出来的最小生成树和直接求原图的最小生成树等价．
    
    那么为什么我们的复杂度是对的呢？
    
    首先，修改过的边一定会加进我们的边集，这些边的数目是 $O(len)$ 级别的．
    
    接下来我们需要证明边集当中不会有过多的未被修改的边．我们只会加入所有边权取 $+\infty$ 最小生成树的树边，因此我们加入的边数目不会超过当前图的点数．
    
    现在我们只需证明每递归一层图的点数是 $O(len)$ 级别的，就可以说明图的边数是 $O(len)$ 级别的了．
    
    证明点数是 $O(len)$ 几倍就变得十分简单了．我们每次向下递归的时候缩掉的边是在 $-\infty$ 生成树中出现的未被修改边，反过来想就是，我们割掉了出现在 $-\infty$ 生成树当中的所有的被修改边．显然我们最多割掉 $len$ 条边，整张图最多分裂成 $O(len)$ 个连通块，这样的话新图点数就是 $O(len)$ 级别的了．所以我们就证明了每次我们用来跑 kruskal 的图都是 $O(len)$ 级别的了，从而每一层的时间复杂度都是 $O(n\log n)$ 了．
    
    时间复杂度是 $T(n)=T(\lfloor \frac{n}{2} \rfloor)+T(\lceil \frac{n}{2} \rceil)+ O(n\log n)=O(n\log^2n)$．
    
    代码实现上可能会有一些难度．需要注意的是并查集不能使用路径压缩，否则就不支持回退操作了．执行缩点操作的时候也没有必要真的执行，而是每一层的 kruskal 都在上一层的并查集里直接做就可以了．

??? note "示例代码"
    ```cpp
    --8<-- "docs/misc/code/cdq-divide/cdq-divide_5.cpp"
    ```

## 参考资料与注释

[^ref1]: [从《Cash》谈一类分治算法的应用](https://www.cs.princeton.edu/~danqic/papers/divide-and-conquer.pdf)


## misc/discrete.md

author: GavinZhengOI, PlanariaIce

## 简介

离散化是一种数据处理的技巧，本质上可以看成是一种 [哈希](../string/hash.md#hash-的思想)，其保证数据在哈希以后仍然保持原来的 [全/偏序](../math/order-theory.md#偏序集) 关系．

通俗地讲就是当有些数据因为本身很大或者类型不支持，自身无法作为数组的下标来方便地处理，而影响最终结果的只有元素之间的相对大小关系时，我们可以将原来的数据按照排名来处理问题，即离散化．

用来离散化的可以是大整数、浮点数、字符串等等．

## 实现

将一个数组离散化，并进行查询是比较常用的应用场景．

### 方法一

通常原数组中会有重复的元素，一般把相同的元素离散化为相同的数据．

方法如下：

1.  创建原数组的副本．

2.  将副本中的值从小到大排序．

3.  将排序好的副本去重．

4.  查找原数组的每一个元素在副本中的位置，位置即为排名，将其作为离散化后的值．

```cpp
// arr[i] 为初始数组,下标范围为 [1, n]

for (int i = 1; i <= n; ++i)  // step 1
  tmp[i] = arr[i];
std::sort(tmp + 1, tmp + n + 1);                          // step 2
int len = std::unique(tmp + 1, tmp + n + 1) - (tmp + 1);  // step 3
for (int i = 1; i <= n; ++i)                              // step 4
  arr[i] = std::lower_bound(tmp + 1, tmp + len + 1, arr[i]) - tmp;
```

参考实现中使用的 STL 算法可参考 [STL 算法](../lang/csl/algorithm.md)．

同样地，我们也可以对 [std::vector](../lang/csl/sequence-container.md#vector) 进行离散化：

```cpp
// std::vector<int> arr;
std::vector<int> tmp(arr);  // tmp 是 arr 的一个副本
std::sort(tmp.begin(), tmp.end());
tmp.erase(std::unique(tmp.begin(), tmp.end()), tmp.end());
for (int i = 0; i < n; ++i)
  arr[i] = std::lower_bound(tmp.begin(), tmp.end(), arr[i]) - tmp.begin();
```

### 方法二

根据题目要求，有时候会把相同的元素根据输入顺序离散化为不同的数据．

此时再用 `std::lower_bound()` 函数实现就有些困难了，需要换一种思路：

1.  创建原数组的副本，同时记录每个元素出现的位置．

2.  将副本按值从小到大排序，当值相同时，按出现顺序从小到大排序．

3.  将离散化后的数字放回原数组．

```cpp
struct Data {
  int idx, val;

  bool operator<(const Data& o) const {
    if (val == o.val)
      return idx < o.idx;  // 当值相同时，先出现的元素离散化后的值更小
    return val < o.val;
  }
} tmp[MAXN];  // 也可以使用 std::pair

for (int i = 1; i <= n; ++i) tmp[i] = Data{i, arr[i]};
std::sort(tmp + 1, tmp + n + 1);
for (int i = 1; i <= n; ++i) arr[tmp[i].idx] = i;
```

### 复杂度

对于方法一，去重复杂度为 $O(n)$，排序复杂度为 $O(n \log n)$，最后的 $n$ 次查找复杂度为 $O(n \log n)$．

对于方法二，排序复杂度为 $O(n \log n)$．

故两种方法的总时间复杂度都为 $O(n \log n)$．

空间复杂度为 $O(n)$．

## 习题

-   [\[HAOI2014\] 贴海报](https://www.luogu.com.cn/problem/P3740)
-   [\[NOI2015\] 程序自动分析](https://www.luogu.com.cn/problem/P1955)


## misc/endianness.md

本页面将简要介绍字节顺序的概念和分类．

## 简介

字节顺序是跨越多字节的程序对象的存储规则，表示一个对象的字节的排列方法．

## 分类

字节顺序有两种，分为小端序（little endian）和大端序（big endian）．

为方便介绍，接下来以一个位于 `0x100` 处，类型为 `int`，十六进制值为 `0x01234567` 的变量为例．其中 `0x01` 是最高位有效字节，`0x67` 是最低位有效字节．

### 小端序

小端序是指机器选择在内存中按照从 **最低** 有效字节到 **最高** 有效字节的顺序存储对象．

上文提到的变量表示如下：

| .... | 0x100 | 0x101 | 0x102 | 0x103 | .... |
| ---- | ----- | ----- | ----- | ----- | ---- |
| .... | 67    | 45    | 23    | 01    | .... |

### 大端序

大端序是指机器选择在内存中按照从 **最高** 有效字节到 **最低** 有效字节的顺序存储对象．

上文提到的变量表示如下：

| .... | 0x100 | 0x101 | 0x102 | 0x103 | .... |
| ---- | ----- | ----- | ----- | ----- | ---- |
| .... | 01    | 23    | 45    | 67    | .... |

### 两种顺序的区别

事实上，这两种字节顺序没有孰优孰劣之分．这两种顺序的名字「小端」和「大端」，正是出自《格列佛游记》一书．书中，小人国里两个派别交战不休的原因是无法就从小端还是大端剥鸡蛋达成一致．就和剥鸡蛋的争论一样，选择何种字节顺序的争论是非技术性的．

当然，字节顺序的不一致会导致二进制数据在不同类型的机器之间进行传输时被反序．为了避免这件事情，网络应用程序建立了一套标准，保证发送过程中是使用约定好的网络标准，而不是不同机器的内部表示．

## 顺序选择惯例

-   小端序：x86, ARM processors running Android, iOS, and Windows

-   大端序：Sun, PPC Mac, Internet


## misc/expression.md

author: Ir1d, Anguei, hsfzLZH1, siger-young, HeRaNO, c8ef

表达式求值要解决的问题一般是输入一个字符串表示的表达式，要求输出它的值．当然也有变种比如表达式中是否包含括号，指数运算，含多少变量，判断多个表达式是否等价，等等．

表达式一般需要先进行语法分析（grammer parsing）再求值，也可以边分析边求值，语法分析的作用是检查输入的字符串是否是一个合法的表达式，一般使用语法分析器（parser）解决．

表达式包含两类字符：运算数和运算符．对于长度为 $n$ 的表达式，借助合适的分析方法，可以在 $O(n)$ 的时间复杂度内完成分析与求值．

## 表达式树与逆波兰表达式

一种递归分析表达式的方法是，将表达式当成普通的语法规则进行分析，分析后拆分成如图所示的表达式树，然后在树结构上自底向上进行运算．![](./images/bet.png)

表达式树上进行 [树的遍历](../graph/tree-basic.md#树的遍历) 可以得到不同类型的表达式．算术表达式分为三种，分别是前缀表达式、中缀表达式、后缀表达式．中缀表达式是日常生活中最常用的表达式；后缀表达式是计算机容易理解的表达式．

-   前序遍历对应前缀表达式（波兰式）
-   中序遍历对应中缀表达式
-   后序遍历对应后缀表达式（逆波兰式）

逆波兰表达式（后缀表达式）是书写数学表达式的一种形式，其中运算符位于其操作数之后．例如，以下表达式：

$$
a+b*c*d+(e-f)*(g*h+i)
$$

可以用逆波兰表达式书写：

$$
abc*d*+ef-gh*i+*+
$$

因此，逆波兰表达式与表达式树一一对应．逆波兰表达式不需要括号表示，它的运算顺序是唯一确定的．

逆波兰表达式的方便之处在于很容易在线性时间内计算．举个例子：在逆波兰表达式 $3~2~*~1~-$ 中，首先计算 $3 \times 2 = 6$（使用最后一个运算符，即栈顶运算符），然后计算 $6 - 1 = 5$．可以看到：对于一个逆波兰表达式，只需要 **维护一个数字栈，每次遇到一个运算符，就取出两个栈顶元素，将运算结果重新压入栈中**．最后，栈中唯一一个元素就是该逆波兰表达式的运算结果．该算法拥有 $O(n)$ 的时间复杂度．

采用递归的办法分析表达式是否成功，依赖于语法规则的设计是否合理，即，是否能够成功地得到指定的表达式树．例如：

$$
a+b*c
$$

根据加号与乘号的运算优先级不同，该中缀表达式可能转化为两种不同的表达式树．可见，语法规则的设计高度依赖于运算符的优先级．借助运算符的优先级设计相应递归的语法规则，事实上是一件不容易的事情．

下文介绍的办法将运算符与它的优先级视为一个整体，采用非递归的办法，直接根据运算符的优先级来分析与计算表达式．

## 只含左结合的二元运算符的含括号表达式

考虑简化的问题．假设所有运算符都是二元的：所有运算符都有两个参数．并且所有运算符都是左结合的：如果运算符的优先级相等，则从左到右执行．允许使用括号．

对于这种类型的中缀表达式的计算，可以将其转化为后缀表达式再进行计算．定义两个 [栈](../ds/stack.md) 来分别存储运算符和运算数，每当遇到一个数直接放进运算数栈．每个运算符块对应于一对括号，运算符栈只对于运算符块的内部单调．每当遇到一个操作符时，要查找运算符栈中最顶部运算符块中的元素，在运算符块的内部保持运算符按照优先级降序进行适当的弹出操作，弹出的同时求出对应的子表达式的值．

以下部分用「输出」表示输出到后缀表达式，即将该数字放在运算数栈上，或者弹出运算符和两个操作数，运算后再将结果压回运算数栈上．从左到右扫描该中缀表达式：

1.  如果遇到数字，直接输出该数字．
2.  如果遇到左括号，那么将其放在运算符栈上．
3.  如果遇到右括号，不断输出栈顶元素，直至遇到左括号，左括号出栈．换句话说，执行一对括号内的所有运算符．
4.  如果遇到其他运算符，不断输出所有运算优先级大于等于当前运算符的运算符．最后，新的运算符入运算符栈．
5.  在处理完整个字符串之后，一些运算符可能仍然在堆栈中，因此把栈中剩下的符号依次输出，表达式转换结束．

以下是四个运算符 $+$、$-$、$*$、$/$ 的此方法的实现：

??? note "示例代码"
    ```cpp
    
    bool delim(char c) { return c == ' '; }
    
    bool is_op(char c) { return c == '+' || c == '-' || c == '*' || c == '/'; }
    
    int priority(char op) {
      if (op == '+' || op == '-') return 1;
      if (op == '*' || op == '/') return 2;
      return -1;
    }
    
    void process_op(stack<int>& st, char op) {  // 也可以用于计算后缀表达式
      int r = st.top();                         // 取出栈顶元素，注意顺序
      st.pop();
      int l = st.top();
      st.pop();
      switch (op) {
        case '+':
          st.push(l + r);
          break;
        case '-':
          st.push(l - r);
          break;
        case '*':
          st.push(l * r);
          break;
        case '/':
          st.push(l / r);
          break;
      }
    }
    
    int evaluate(string& s) {  // 也可以改造为中缀表达式转换后缀表达式
      stack<int> st;
      stack<char> op;
      for (int i = 0; i < (int)s.size(); i++) {
        if (delim(s[i])) continue;
    
        if (s[i] == '(') {
          op.push('(');  // 2. 如果遇到左括号，那么将其放在运算符栈上
        } else if (s[i] == ')') {  // 3. 如果遇到右括号，执行一对括号内的所有运算符
          while (op.top() != '(') {
            process_op(st, op.top());
            op.pop();  // 不断输出栈顶元素，直至遇到左括号
          }
          op.pop();                // 左括号出栈
        } else if (is_op(s[i])) {  // 4. 如果遇到其他运算符
          char cur_op = s[i];
          while (!op.empty() && priority(op.top()) >= priority(cur_op)) {
            process_op(st, op.top());
            op.pop();  // 不断输出所有运算优先级大于等于当前运算符的运算符
          }
          op.push(cur_op);  // 新的运算符入运算符栈
        } else {            // 1. 如果遇到数字，直接输出该数字
          int number = 0;
          while (i < (int)s.size() && isalnum(s[i]))
            number = number * 10 + s[i++] - '0';
          --i;
          st.push(number);
        }
      }
    
      while (!op.empty()) {
        process_op(st, op.top());
        op.pop();
      }
      return st.top();
    }
    
    ```

这种隐式使用逆波兰表达式计算表达式的值的算法的时间复杂度为 $O(n)$．通过稍微修改上述实现，还可以以显式形式获得逆波兰表达式．

### 一元运算符与右结合的运算符

现在假设表达式还包含一元运算符，即只有一个参数的运算符．一元加号和一元减号是一元运算符的常见示例．

这种情况的一个区别是，需要确定当前运算符是一元运算符还是二元运算符．

注意到，在一元运算符之前一般有另一个运算符或开括号，如果一元运算符位于表达式的最开头则没有．在二元运算符之前，总是有一个运算数或右括号．因此，可以标记下一个运算符是否一元运算符．

此外，需要以不同的方式执行一元运算符和二元运算符，让一元运算符的优先级高于所有二元运算符．应注意，一些一元运算符，例如一元加号和一元减号，实际上是右结合的．

右结合意味着，每当优先级相等时，必须从右到左计算运算符．

如上所述，一元运算符通常是右结合的．右结合运算符的另一个示例是求幂运算符．对于 $a \wedge b \wedge c$，通常被视为 $a^{b^c}$，而不是 $(a^b)^c$．

为了正确地处理这类运算符，相应的改动是，如果优先级相等，将推迟运算符的出栈操作．

需要改动的代码如下．将：

```cpp

while (!op.empty() && priority(op.top()) >= priority(cur_op)) 
```

换成

```cpp

while (!op.empty() &&
       ((left_assoc(cur_op) && priority(op.top()) >= priority(cur_op)) ||
        (!left_assoc(cur_op) && priority(op.top()) > priority(cur_op))))

```

其中 left\_assoc 是一个函数，它决定运算符是否为左结合的．

这里是二进制运算符 $+$、$-$、$*$、$/$ 和一元运算符 $+$ 和 $-$ 的实现：

??? note "示例代码"
    ```cpp
    
    bool delim(char c) { return c == ' '; }
    
    bool is_op(char c) { return c == '+' || c == '-' || c == '*' || c == '/'; }
    
    bool is_unary(char c) { return c == '+' || c == '-'; }
    
    int priority(char op) {
      if (op < 0)  // unary operator
        return 3;
      if (op == '+' || op == '-') return 1;
      if (op == '*' || op == '/') return 2;
      return -1;
    }
    
    void process_op(stack<int>& st, char op) {
      if (op < 0) {
        int l = st.top();
        st.pop();
        switch (-op) {
          case '+':
            st.push(l);
            break;
          case '-':
            st.push(-l);
            break;
        }
      } else {  // 取出栈顶元素，注意顺序
        int r = st.top();
        st.pop();
        int l = st.top();
        st.pop();
        switch (op) {
          case '+':
            st.push(l + r);
            break;
          case '-':
            st.push(l - r);
            break;
          case '*':
            st.push(l * r);
            break;
          case '/':
            st.push(l / r);
            break;
        }
      }
    }
    
    int evaluate(string& s) {
      stack<int> st;
      stack<char> op;
      bool may_be_unary = true;
      for (int i = 0; i < (int)s.size(); i++) {
        if (delim(s[i])) continue;
    
        if (s[i] == '(') {
          op.push('(');  // 2. 如果遇到左括号，那么将其放在运算符栈上
          may_be_unary = true;
        } else if (s[i] == ')') {  // 3. 如果遇到右括号，执行一对括号内的所有运算符
          while (op.top() != '(') {
            process_op(st, op.top());
            op.pop();  // 不断输出栈顶元素，直至遇到左括号
          }
          op.pop();  // 左括号出栈
          may_be_unary = false;
        } else if (is_op(s[i])) {  // 4. 如果遇到其他运算符
          char cur_op = s[i];
          if (may_be_unary && is_unary(cur_op)) cur_op = -cur_op;
          while (!op.empty() &&
                 ((cur_op >= 0 && priority(op.top()) >= priority(cur_op)) ||
                  (cur_op < 0 && priority(op.top()) > priority(cur_op)))) {
            process_op(st, op.top());
            op.pop();  // 不断输出所有运算优先级大于等于当前运算符的运算符
          }
          op.push(cur_op);  // 新的运算符入运算符栈
          may_be_unary = true;
        } else {  // 1. 如果遇到数字，直接输出该数字
          int number = 0;
          while (i < (int)s.size() && isalnum(s[i]))
            number = number * 10 + s[i++] - '0';
          --i;
          st.push(number);
          may_be_unary = false;
        }
      }
    
      while (!op.empty()) {
        process_op(st, op.top());
        op.pop();
      }
      return st.top();
    }
    
    ```

## 参考资料

**本页面主要译自博文 [Разбор выражений. Обратная польская нотация](https://e-maxx.ru/algo/expressions_parsing) 与其英文翻译版 [Expression parsing](https://cp-algorithms.com/string/expression_parsing.html)．其中俄文版版权协议为 Public Domain + Leave a Link；英文版版权协议为 CC-BY-SA 4.0．**

## 延申阅读

1.  [Operator-precedence\_parser](https://en.wikipedia.org/wiki/Operator-precedence_parser)
2.  [Shunting yard algorithm](https://en.wikipedia.org/wiki/Shunting_yard_algorithm)

## 习题

1.  [NOIP2013 普及组 表达式求值](https://www.luogu.com.cn/problem/P1981)
2.  [后缀表达式](https://www.luogu.com.cn/problem/P1449)
3.  [Transform the Expression](https://www.spoj.com/problems/ONP/)


## misc/frac-programming.md

author: greyqz, Ir1d, hsfzLZH1, huaruoji, banglee13

分数规划用来求一个分式的极值．其形式化表述是，给出 $a_i$ 和 $b_i$，求一组 $w_i\in\{0,1\}$，最小化或最大化

$$
\displaystyle\frac{\sum\limits_{i=1}^na_i\times w_i}{\sum\limits_{i=1}^nb_i\times w_i}
$$

通俗来讲，这类问题类似于：每种物品有两个权值 $a$ 和 $b$，选出若干个物品使得 $\displaystyle\frac{\sum a}{\sum b}$ 最小或最大．

一般分数规划问题还会有一些特殊的限制，比如「分母至少为 $W$」．

## 求解

### 二分法

分数规划问题的通用方法是二分答案法．假设当前二分到的答案为 $\textit{mid}$，则一组满足条件的 $\{w_i\}$ 会让权值大于等于 $\textit{mid}$．根据这一条件列不等式并变形

$$
\displaystyle
\begin{aligned}
&\frac{\sum a_i\times w_i}{\sum b_i\times w_i}\ge mid\\
\Longrightarrow&\sum a_i\times w_i-mid\times \sum b_i\cdot w_i\ge 0\\
\Longrightarrow&\sum w_i\times(a_i-mid\times b_i)\ge 0
\end{aligned}
$$

那么只要求出不等号左边的式子的最大值就行了．如果最大值比 $0$ 要大，说明 $mid$ 是可行的，否则不可行．分数规划的主要难点就在于如何求 $\displaystyle \sum w_i\times(a_i-mid\times b_i)$ 的最大值或最小值．

### Dinkelbach 算法

Dinkelbach 算法[^note1]的大概思想是每次用上一轮的答案当做新的 $L$ 来输入，不断地迭代，直至答案收敛．

## 例题

???+ example "[LOJ 149 01 分数规划](https://loj.ac/p/149)"
    有 $n$ 个物品，每个物品有两个权值 $a$ 和 $b$．求一组 $w_i\in\{0,1\}$，满足 $w_i$ 中恰好有 $k$ 个 $1$，最大化 $\displaystyle\frac{\sum a_i\times w_i}{\sum b_i\times w_i}$ 的值．

??? note "解法"
    把 $a_i-mid\times b_i$ 作为第 $i$ 个物品的权值，贪心地选权值前 $k$ 大的物品．若权值和大于 $0$ 则可行，否则不可行．

??? note "参考代码"
    ```cpp
    --8<-- "docs/misc/code/frac-programming/frac-1.cpp"
    ```

???+ example "[洛谷 4377 Talent Show G](https://www.luogu.com.cn/problem/P4377)"
    有 $n$ 个物品，每个物品有两个权值 $a$ 和 $b$．
    
    你需要确定一组 $w_i\in\{0,1\}$，使得 $\displaystyle\frac{\sum w_i\times a_i}{\sum w_i\times b_i}$ 最大．
    
    要求 $\displaystyle\sum w_i\times b_i \geq W$．

??? note "解法"
    本题多了分母至少为 $W$ 的限制，因此无法再使用上一题的贪心算法．
    
    可以考虑 01 背包．把 $b_i$ 作为第 $i$ 个物品的重量，$a_i-mid\times b_i$ 作为第 $i$ 个物品的价值，然后问题就转化为背包了．那么 $dp[n][W]$ 就是最大值．
    
    在 DP 过程中，物品重量和可能超过 $W$，此时直接视为 $W$ 即可．

??? note "参考代码"
    ```cpp
    --8<-- "docs/misc/code/frac-programming/frac-2.cpp"
    ```

???+ example "[POJ2728 Desert King](http://poj.org/problem?id=2728)"
    每条边有两个权值 $a_i$ 和 $b_i$，求一棵生成树 $T$ 使得 $\displaystyle\frac{\sum_{e\in T}a_e}{\sum_{e\in T}b_e}$ 最小．

??? note "解法"
    把 $a_i-mid\times b_i$ 作为每条边的权值，那么最小生成树就是最小值．本题中需要求解一个完全图中的最小生成树，应利用 Prim 算法求解．

??? note "参考代码"
    ```cpp
    --8<-- "docs/misc/code/frac-programming/frac-3.cpp"
    ```

???+ example "[\[HNOI2009\] 最小圈](https://www.luogu.com.cn/problem/P3199)"
    每条边的边权为 $w$，求一个环 $C$ 使得 $\displaystyle\frac{\sum_{e\in C}w}{|C|}$ 最小．

??? note "解法"
    把 $a_i-mid$ 作为边权，那么权值最小的环就是最小值．
    
    因为我们只需要判最小值是否小于 $0$，所以只需要判断图中是否存在负环即可．
    
    另外本题存在一种复杂度 $O(nm)$ 的算法，如果有兴趣可以阅读 [这篇文章](https://www.cnblogs.com/y-clever/p/7043553.html)．

??? note "参考代码"
    ```cpp
    --8<-- "docs/misc/code/frac-programming/frac-4.cpp"
    ```

## 习题

-   [JSOI2016 最佳团体](https://loj.ac/problem/2071)
-   [SDOI2017 新生舞会](https://loj.ac/problem/2003)
-   [UVa1389 Hard Life](https://onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&category=24&page=show_problem&problem=4135)
-   [洛谷 P2868 \[USACO07DEC\] Sightseeing Cows G](https://www.luogu.com.cn/problem/P2868)
-   [AtCoder Beginner Contest 324 F - Beautiful Path](https://atcoder.jp/contests/abc324/tasks/abc324_f)

## 参考资料与注释

[^note1]: [Dinkelbach, Werner. "On nonlinear fractional programming." Management science 13.7 (1967): 492-498.](https://doi.org/10.1287/mnsc.13.7.492)


## misc/fsm.md

author: CCXXXI, countercurrent-time, Enter-tainer, FFjet, H-J-Granger, Ir1d, mgt, NachtgeistW, orzAtalod, ouuan, SukkaW

前置知识：[语言和判定问题](./cc-basic.md#问题)

**有限状态自动机**（Finite State Machine，FSM，以下也简称自动机）是最简单的一类计算模型，体现在它的描述能力与资源都极其有限．自动机广泛应用在 OI、计算机科学中，其思想在许多字符串算法中都有涉及，因此推荐在学习一些字符串算法（[KMP](../string/kmp.md)、[AC 自动机](../string/ac-automaton.md)、[SAM](../string/sam.md)）前先完成自动机的学习．

## 自动机入门

首先，我们来理解自动机是用来做什么的：自动机是一种判断一个信号序列是否满足某种特定模式或规则的数学模型．

这句话中的一些术语可以具体解释一下．「信号序列」指的是一个按顺序排列的信号，例如字符串从前到后的每一个字符、数组从 $1$ 到 $n$ 的每一个数、数从高到低的每一位等．「判断是否满足某种规则」，可以理解为：我们关心这个序列是否属于某个特定的集合．这个集合由我们事先设定好的规则来定义，例如「所有长度为偶数的二进制串」或「所有回文串」．

有时我们需要回答这类问题：一个给定的序列，是否满足某种特性？例如，一个二进制数是否是奇数，一个字符串是否是回文，或是否是另一个字符串的子序列等等．自动机就是用来解决这类问题的数学工具．

自动机的工作原理和流程图很类似．假设你想要在外卖平台点购一杯奶茶，你的所有选择就构成了一个序列．以下这个流程图是一个例子：

![order fsm](./images/fsm1.svg)

例如，你的选择序列是「打开点单界面 -> 选择奶茶 -> 有奶茶的钱」，那你按顺序经过的状态可能是「外卖平台 -> 点单界面 -> 支付奶茶的钱 -> 买到奶茶」．就这样，我们的这个「奶茶自动机」根据我们的选择，帮我们判定了我们是否买到了奶茶．我们还可以发现，到达一个状态的方法可能不止一条．同样没有买到奶茶，你可能是在点单界面直接退出，或者没有奶茶的钱以至于没有买到奶茶．

我们通过这个自动机，将信号序列分成了两类：一类是买到了奶茶的信号序列，一类是没有买到奶茶的信号序列．根据最后位于的状态的不同，我们就完成了一个判定问题．

虽然我们刚才用流程图来类比自动机的工作过程，但流程图本身只是一个直观的可视化工具，并不构成对自动机的数学定义．为了更准确地刻画自动机的结构，我们需要对流程图中的元素进行抽象．抽象之后，我们发现流程图的结构其实可以简化为一个有向图，其中每个结点表示一种状态，每条有向边表示状态之间的转换．

因此，自动机的核心结构可以形式化地看作是一张有向图，我们称之为 **状态图**．

自动机的工作方式和流程图类似，不同的是：自动机的每一个结点都是一个判定结点；自动机的结点只是一个单纯的状态而非任务；自动机的边可以接受多种字符（不局限于 `T` 或 `F`）．

举个例子，完成「判断一个二进制数是不是偶数」的自动机如下：

![example fsm](./images/fsm2.svg)

从起始结点开始，从高到低接受这个数的二进制序列，然后看最终停在哪里．如果最终停在红圈结点，就是偶数；否则不是．

在这里，我们需要强调，下文中我们会多次提到「字符」、「字符集」之类的名词，这不代表自动机只能应用于字符串领域，字符不一定是 $\tt abc\cdots z$ 之类的字母，也可以是一种选择．

如果需要判定一个有限的信号序列和另外一个信号序列的关系（例如另一个信号序列是不是某个信号序列的子序列），那么常用的方法是针对那个有限的信号序列构建一个自动机．这个在学习 KMP 的时候会讲到．

需要注意的是，自动机只是一个 **数学模型**，而 **不是算法**，也 **不是数据结构**．实现同一个自动机的方法有很多种，可能会有不一样的时空复杂度．

接下来你可以选择在本页面继续进一步研究自动机，也可以去学习 [KMP](../string/kmp.md)、[AC 自动机](../string/ac-automaton.md) 或 [SAM](../string/sam.md) 等具体的例子．

FSM 分为两类：确定性有限状态自动机、非确定性有限状态自动机．

## 确定性有限状态自动机

**确定性有限状态自动机**（Deterministic Finite Automaton，DFA）体现在它的判定过程是确定性的．以「奶茶自动机」为例子，你只要打开点单界面，就会进入点单界面，不会出现网络崩溃打不开、手机没电黑屏了之类的意外情况．

???+ abstract "DFA"
    DFA 是一个五元组 $(Q,\Sigma,\delta,q_0,F)$，包括：
    
    1.  **有限状态集合**  $Q$．如果把一个 DFA 看成一张有向图，那么 DFA 中的状态就相当于图上的顶点．
    2.  **字符集** $\Sigma$．该自动机只能输入这些字符．
    3.  **转移函数** $\delta:Q\times \Sigma \to Q$ 是一个接受两个参数返回一个值的函数，其中第一个参数和返回值都是一个状态，第二个参数是字符集中的一个字符．如果把一个 DFA 看成一张有向图，那么 DFA 中的转移函数就相当于顶点间的边，而每条边上都有一个字符．
    4.  **起始状态**  $q_0\in Q$ 是一个特殊的状态．在不同文章中，起始状态一般用 $s$、$\textit{start}$、$q_0$ 表示，本文中选择使用 $q_0$ 表示．
    5.  **接受状态集合**  $F\subseteq Q$ 是一组特殊的状态．

DFA 可以简单地用以下结构体表示：

???+ example "参考实现"
    ```cpp
    --8<-- "docs/misc/code/fsm/dfa.hpp:dfa"
    ```

求出输入串 $w$ 在 DFA 中的状态序列，并判断它是否被接受的过程称为 **计算**．

???+ abstract "DFA 的计算流程"
    设 $M=(Q,\Sigma,\delta,q_0,F)$ 是一个 DFA，$w=w_1w_2\cdots w_n\in\Sigma^*$ 是一个串．若存在 $Q$ 中的状态序列 $r_0,r_1,\cdots,r_n$ 满足
    
    -   $r_0=q_0$，
    -   $\delta(r_i,w_{i+1})=r_{i+1}$ 对于任何 $i=0,1,\cdots,n-1$ 都成立，
    -   $r_n\in F$，
    
    则称 $M$  **接受**（accepts）$w$．反之，则称 $M$  **不接受**  $w$．

当一个 DFA 读入一个字符串时，从初始状态起按照转移函数一个一个字符地转移．如果读入完一个字符串的所有字符后位于一个接受状态，那么我们称这个 DFA **接受** 这个字符串，反之我们称这个 DFA **不接受** 这个字符串．

???+ abstract "形式语言"
    字符集合 $\Sigma$ 上的一个 **形式语言**（language），或简称 **语言**，是 $\Sigma$ 上字符串的一个集合 $L$．

???+ abstract "自动机识别的语言"
    对于一个自动机 $M$，它识别的语言 $L(M)$ 就定义为它接受的全部子串的集合 $\{w\mid M\text{ accepts }w\}$．

并非所有的语言都可以通过 DFA 识别．

???+ abstract "正则语言"
    如果一个语言能由某个 DFA 识别，则称它为 **正则语言**（regular language），也称为正规语言．

上文提到过，一个自动机可以由状态图表示出来．如下是一个接受且仅接受字符串 $\tt a$、$\tt ab$、$\tt aac$ 的 DFA：

![](./images/fsm3.svg)

（图中省略了失配状态，所有未画出的转移均指向该失配状态）

## 非确定性有限状态自动机

**非确定性有限状态自动机**[^nfa-and-nfaepsilon]（Nondeterministic Finite Automaton，NFA）是 DFA 的自然推广．在 NFA 中，对于任意状态和任意字符，都可能存在零个、一个或多个后继状态．同时，本节讨论的 NFA 允许接受空字符，也就是说，可以在不消耗任何字符的情况下，由一个状态转移到它的某个后继状态．

举个例子，还是「奶茶自动机」．下单后，尽管有奶茶的钱，却有可能因为网络不佳从而没有买到奶茶，这是存在多个后继；也有可能因为手速慢了，尽管输入的串（即操作序列）是一样的，却因为奶茶售完从而没有买到奶茶，这就是空字符的存在，空字符可走可不走．对前文的自动机稍加修改即可实现上述功能：

![order nfa](./images/fsm4.svg)

显然，所有的 DFA 都是一个 NFA，所以 NFA 至少可以识别所有正则语言．但是，作为 DFA 的一个扩展，NFA 是否能够识别更多的语言呢？其实不然，我们之后将探讨 DFA 与 NFA 的等价性．

???+ abstract "NFA"
    令 $\mathcal{P}(Q)$ 表示 $Q$ 的幂集．令 $\varepsilon\notin\Sigma$ 表示空串，并记 $\Sigma_\varepsilon = \Sigma\cup\{\varepsilon\}$．NFA 是一个五元组 $(Q,\Sigma,\delta,q_0,F)$，包括：
    
    1.  **有限状态集合**  $Q$，
    2.  **字符集** $\Sigma$，
    3.  **转移函数** $\delta:Q\times \Sigma_{\varepsilon} \to \mathcal{P}(Q)$，一个接受两个参数返回一个 **状态集合** 的函数，其中第一个参数是一个状态，第二个参数是字符集中的一个字符，而返回值则是所有可能的后继状态形成的集合（可能为空），
    4.  **起始状态**  $q_0\in Q$，
    5.  **接受状态集合**  $F\subseteq Q$．

NFA 的计算过程，相当于同时运行多个 DFA．每一步操作都穷举所有的可能性，最后，只要有一条分支到达了接受状态，NFA 就接受整个串．

???+ abstract "NFA 的计算流程"
    设 $N=(Q,\Sigma,\delta,q_0,F)$ 是一个 NFA，串 $w$ 可以表示为 $y_1y_2\cdots y_m\in\Sigma^*_\varepsilon$．若存在 $Q$ 中的状态序列 $r_0,r_1,\cdots,r_m$ 满足
    
    -   $r_0=q_0$，
    -   $r_{i+1}\in\delta(r_i,y_{i+1})$ 对于任何 $i=0,1,\cdots,m-1$ 都成立，
    -   $r_m\in F$，
    
    则称 $N$  **接受**  $w$．反之，则称 $N$  **不接受**  $w$．

由于允许空字符，将串 $w$ 表示为 $y_1y_2\cdots y_m\in\Sigma^*_\varepsilon$ 时，可以插入任意多的空字符．例如，字符串 $\texttt{abc}$ 可以表示为 $\texttt{a}\varepsilon\texttt{bc}\varepsilon\varepsilon\in\Sigma^*_\varepsilon$．相较于 DFA 的每一次输入只对应一个结果，而 NFA 的每次输入可能对应多个结果，形成一个结果集．

## DFA 与 NFA 的等价性

我们称两个自动机等价，当且仅当它们能识别的语言相同．DFA 与 NFA 是等价的，即每一个 NFA 都等价于某一个 DFA；因此，NFA 识别的语言类也是全体正则语言．每个 DFA 都可以直接看作一个 NFA；反过来，可以通过 **幂集构造**（powerset construction）的方法将一个 NFA 转换为 DFA．

???+ abstract "幂集构造"
    假设 NFA 为 $N = (Q, \Sigma, \delta, q_0, F)$．定义 $E(q)$ 表示从状态 $q$ 出发，只沿 $\varepsilon$ 转移能到达的状态集合．
    
    构造 DFA 为 $M = (Q', \Sigma, \delta', E(q_0), F')$，其中：
    
    -   **有限状态集合**  $Q' = \mathcal{P}(Q)$，
    -   **转移函数** $\delta' : Q' \times \Sigma \to Q'$ 满足 $\delta'(S, c) = \bigcup_{q \in S,~q' \in \delta(q, c)} E(q')$，
    -   **接受状态集合**  $F' = \{ S \subseteq Q \mid S \cap F \neq \varnothing \}$．
    
    显然，计算的每一步中，$M$ 所在的状态都对应 $N$ 可能处于的状态集合．

虽然 NFA 与 DFA 识别语言的能力相同，但 NFA 仍然是有用的．这是因为对于某些正则语言，用 NFA 表示所需的状态数远小于 DFA 所需的状态数．例如，可以构造出一个状态数为 $n$ 的 NFA 使得它对应的最小 DFA 状态数是 $\Theta(2^n)$ 的．此时直接计算 NFA 的时间复杂度是更优的．

## 计算 DFA 与 NFA 的时间复杂度

设给定的串长为 $n$，自动机状态数为 $s$，字符集大小为常数．那么显然地，DFA 计算的时间复杂度为 $O(n)$，只需要模拟上述的过程即可．

朴素计算 NFA 的时间复杂度为 $O(ns^2)$，这是因为需要考虑到每一种后继，以及状态的合并所需的复杂度．当然，可以使用 bitset 或者 Method of Four Russians 将计算的复杂度优化到 $O\left(\dfrac{ns^2}{w}\right)$ 或 $O\left(\dfrac{ns^2}{w\cdot \log n}\right)$．

## 正则表达式与正则语言

本节将讨论正则表达式和正则语言的定义、性质，并研究正则表达式与 FSM 的关系．

### 正则表达式

**正则表达式**（regular expression）是另一种常用的正则语言的描述方法．尽管我们可以在许多现代语言（例如 Python）中看到这个名字，但实际上这些语言实现的是正则表达式的一个超集．

???+ abstract "正则表达式"
    给定一个字符集 $\Sigma$，正则表达式是由以下规则归纳定义的符号串：
    
    1.  任意字符 $c \in \Sigma$ 是一个正则表达式；
    2.  空串符号 $\varepsilon$ 是正则表达式；
    3.  空语言符号 $\varnothing$ 是正则表达式；
    4.  如果 $R_1$ 和 $R_2$ 是正则表达式，那么 $(R_1 + R_2)$、$(R_1 R_2)$（也记作 $(R_1 \cdot R_2)$）、$(R_1^\ast)$ 都是正则表达式．

正则表达式的目标是通过这些符号描述一个语言．每个正则表达式都有一个对应的形式语言．

???+ abstract "正则表达式所表示的语言"
    设每个正则表达式 $R$ 对应的形式语言为 $L(R)$，则有：
    
    1.  若 $R = c$，其中 $c \in \Sigma$，则 $L(R) = \{c\}$；
    2.  若 $R = \varepsilon$，则 $L(R) = \{\varepsilon\}$；
    3.  若 $R = \varnothing$，则 $L(R) = \varnothing$；
    4.  若 $R = (R_1 + R_2)$，则 $L(R) = L(R_1) \cup L(R_2)$；
    5.  若 $R = (R_1 R_2) = (R_1\cdot R_2)$，则 $L(R) = \{ uv \mid u \in L(R_1),~ v \in L(R_2) \}$，其中，$uv$ 指将两个串前后拼接在一起；
    6.  若 $R = (R_1^\ast)$，则 $L(R) = \{u_1 u_2 \cdots u_n \mid u_i \in L(R_1),\ n \in \mathbf{N}_+\}\cup\{\varepsilon\}$，也称为 **Kleene 星号**（Kleene 星号）或 **Kleene closure**（Kleene 闭包），简称闭包．

当然，规定了运算的优先级后，这些小括号在不引起混淆时可以省略．

???+ example "例子"
    设 $L(R_1) = \{0,\ 01\}$，$L(R_2) = \{\varepsilon,\ 1,\ 11,\ 111,\ \dots\}$，则有：
    
    -   $L(R_1R_2) = \{0,\ 01,\ 011,\ 0111,\ \dots\}$，
    -   $R_2^\ast = R_2$，
    -   $L(R_1 + R_2) = \{0,\ 01,\ \varepsilon,\ 1,\ 11,\ 111,\ \dots\}$．

每个正则表达式都可以通过 [Thompson 构造法](https://zh.wikipedia.org/wiki/%E6%B1%A4%E6%99%AE%E6%A3%AE%E6%9E%84%E9%80%A0%E6%B3%95)（Thompson's construction）转换为一个 NFA，每个 DFA 也都可以通过状态消除法[^state-elimination-method]（State Elimination Method）转换为一个正则表达式．所以，正则表达式与 FSM 是等价的．

### 正则语言

在本小节中，我们不考虑具体的正则表达式，转而考虑以变量为参数的正则表达式（变量可以为任意正则语言）．运用正则表达式的代数定律有助于化简正则表达式．

???+ note "正则语言的代数性质"
    1.  并的交换律：$L + M = M + L$
    2.  并的结合律：$(L + M) + N = L + (M + N)$
    3.  连接的结合律：$(LM)N = L(MN)$
    4.  $\varnothing$ 是并运算的单位元：$\varnothing + L = L + \varnothing = L$
    5.  $\varepsilon$ 是连接运算的单位元：$\varepsilon L = L \varepsilon = L$
    6.  $\varnothing$ 是连接运算的零因子：$\varnothing L = L \varnothing = \varnothing$
    7.  分配律：$L(M + N) = LM + LN$，$(M + N)L = ML + NL$
    8.  并的幂等律：$L + L = L$
    9.  闭包相关的定律：$(L^\ast)^\ast = L^\ast$，$\varnothing^\ast = \varepsilon$，$\varepsilon^\ast = \varepsilon$

正则语言的 **封闭性** 也是重要的性质．这些性质允许我们从一些简单的自动机出发，通过一定的运算，构造能够识别另一些语言的有限状态机（FSM）．简而言之，封闭性可以作为构造复杂 FSM 的工具．

关于正则语言的封闭性，我们有：

???+ note "正则语言的封闭性"
    设 $L,M$ 为字符集 $\Sigma$ 上的两个正则语言，且映射 $h:\Sigma\to\Sigma^*$．定义字符串 $s=s_1s_2\cdots s_n$ 的同态为 $h(s)=h(s_1)h(s_2)\cdots h(s_n)$．那么，
    
    1.  两个正则语言的并 $L + M$ 是正则的，
    2.  两个正则语言的连接 $LM$ 是正则的，
    3.  正则语言的闭包 $L^*$ 是正则的，
    4.  正则语言的补 $\Sigma^*\setminus L$ 是正则的，
    5.  两个正则语言的交 $L\cap M$ 是正则的，
    6.  两个正则语言的差 $L\setminus M$ 是正则的，
    7.  正则语言的反转 $L^R=\{s_n\cdots s_2s_1 \mid s=s_1s_2\cdots s_n\in L\}$ 是正则的，
    8.  正则语言的同态 $h(L)=\{h(s)\mid s\in L\}$ 是正则的，
    9.  正则语言的逆同态 $h^{-1}(L) = \{ s \in \Sigma^\ast \mid h(s) \in L \}$ 是正则的．

一个简单的推论是，所有的有限语言都是正则语言．实际上，[字典树 Trie](../string/trie.md) 就是一个识别它们的自动机．

## Myhill–Nerode 定理

Myhill–Nerode 定理给出了一个语言是否是正则语言的判定标准．该定理通过等价类的概念描述了正则语言的结构特征．

???+ abstract "Nerode 等价关系"
    对于一个语言 $L$ 和任意串 $x,y\in \Sigma^\ast$，如果对于任意 $z\in\Sigma^*$，都有 $xz\in L\iff yz\in L$，那么，称字符串 $x$ 和 $y$ 关于 $L$ 是等价的，记作 $x\equiv_L y$．

也就是说，如果对于两个串 $x$ 与 $y$，在 $x$ 和 $y$ 后面拼上相同的任意串 $z$（包括空串），它们总是要么同时属于 $L$ 或者同时不属于 $L$ 的，则我们说 $x$ 与 $y$ 关于 $L$ 等价．

根据上述定义，我们把所有有限字符串的集合划分成一个或多个等价类．当且仅当这些等价类的数目只有有限多个时，可以利用这些等价类构造一个识别该语言的 DFA．这个 DFA 的状态数目就等于等价类的数目．而且，这个状态数目是所有能够识别该语言的 DFA 中最小的．这就是 Myhill–Nerode 定理．

???+ note "Myhill–Nerode 定理"
    一个语言 $L$ 是正则的，当且仅当 $\Sigma^\ast$ 通过等价关系 $\equiv_L$ 划分成的等价类数量是有限的．
    
    对于任何能识别语言 $L$ 的 DFA，任意两个能驱使它走到同一个状态的串 $x$ 和 $y$ 必在同一个等价类中．
    
    进而，等价类的数量就是可以识别 $L$ 的最小 DFA 的状态数量．每个等价类都恰好对应最小 DFA 里的一个状态．这个最小 DFA 在同构意义下是唯一的．

这个定理提供了一种方法，能够利用等价关系构造 DFA：

-   状态集合，就是根据等价关系划分得到的所有等价类．每个等价类都随意选定一个代表字符串（例如某个串长最小的串）．
-   要构造转移函数，只需要将选定的代表字符串后面添加转移中的字符，并找到得到的字符串所在等价类对应的状态，就是相应的转移的后继状态．因为同一等价类中，所有字符串都是等价的，所以任意选定的代表字符串并不会影响转移的结果．
-   初始状态，就是空字符串 $\varepsilon$ 对应的等价类．
-   接受状态集合，就是代表字符串属于所给语言的等价类的集合．

作为一个经典的例子，[后缀自动机](../string/sam.md) 就是利用 Myhill–Nerode 定理构造出的最小 DFA．

Myhill–Nerode 定理通常应用于一些无限大的正则语言对应的 DFA 的构造．很多时候，问题的条件比较简单，只需要考察长度不太长的字符串的集合，就可以构造出识别整个语言的自动机．

### 例题

本节通过一道例题介绍如何实际应用 Myhill–Nerode 定理．

???+ example "[P12294 \[THUPC 2025 决赛\] 一个 01 串，n 次三目运算符，最后值为 1（加强版）](https://www.luogu.com.cn/problem/P12294)"
    关于 $a,b,c$ 的三目运算表 $s_0s_1\cdots s_7$（$s$ 仅由 $0,1$ 组成）的含义是，如果 $s$ 的第 $a+2b+4c$ 位为 $1$，那么返回 $1$，否则返回 $0$．
    
    给定运算表 $s$ 以及 $q$ 个长为 $2n+1$ 的 $01$ 串，你需要对于对每个 $01$ 串分别回答：
    
    能否操作 $n$ 次，每次将三位连续的数字替换为所对应的运算值，使得运算的结果为 $1$，给出方案，或判断无解．
    
    $1\le 2n+1\le 10^5,~\sum(2n+1)\le 3\times 10^5$．

??? note "题解"
    能够合成出 $1$ 的 $01$ 串集合是一个正则语言（也就是存在一个 DFA 能够判定一个 $01$ 串能否合成出 $1$）[^prove-regular-language]．故考虑使用 Myhill–Nerode 定理．因为条件比较简单，经过实验，我们只需要对于长度 $\le 9$ 的 $01$ 串进行等价类划分；判定两个串等价时，只需要往后枚举长度 $\le 6$ 的后缀进行判定．只要两个串，接上长度 $\le 6$ 的任意后缀，它们要么能够同时合成出我们想要的串，要么两个都不能合成我们想要的串，那么这两个串就是等价的．
    
    每次转移都相当于在当前串后面添加一个新的 $01$ 字符，然后将这个新串变为这个新串所在等价类中串长最小的串．根据上述转移设计一个自动机．该自动机能够在 $O(n)$ 复杂度内判定一个长度为 $n$ 的串是否存在一种运算方式使得结果为 $1$．同时自动机的状态数非常少．
    
    为了方便，我们会建 $6$ 个自动机，这 $6$ 个自动机分别表示能否通过一种运算方式使得结果为 $0,1,00,01,10,11$．对于所有可能的运算表，自动机的最大状态数目为 $47$．
    
    利用自动机，通过适当的预处理，可以考虑使用倍增或者猫树实现静态区间查询区间是否存在一种运算方式使得结果为 $1$，前者查询一次是 $O(\log n)$，后者查询一次是 $O(1)$ 的．
    
    考虑使用分治解决构造问题．设 $f(l,r,t)$ 表示区间 $[l,r]$ 合并出 $t\in\{{0,1,00,01,10,11}\}$ 的方案．此时使用启发式分裂，维护两个指针 $i,j$ 一个从左到右扫，一个从右往左扫，以枚举断点 $\textit{mid}$ 为 $i$ 或 $j$．对于 $t\in\{{0,1}\}$，则枚举 $t$ 是怎么分为左右两个部分的，其中一个部分的 $t$ 长度为 $2$，另一个部分 $t$ 长度为 $1$．（例如对于中位数的运算表 $s=00010111$，$1$ 可以分为 $01$ 和 $1$．）对于 $t\in\{{00,01,10,11}\}$，则 $type$ 直接分为左右两个部分．
    
    如果此时分为的左右两个部分分别为 $t_1$ 与 $t_2$，则进一步判断 $[l,mid]$ 能否生成 $t_1$ 和 $[\textit{mid}+1,r]$ 能否生成 $t_2$，如果能则直接分治下去．如果使用 $O(1)$ 猫树判定，这么启发式分裂构造的复杂度是 $O(n\log n)$；否则，利用倍增判定，构造的复杂度就是 $O(n\log^2n)$ 的．
    
    如果使用了猫树，总复杂度是 $O(n|Q|\log n+n\log n)$，其中，$|Q|\le 47$．参考代码为了方便，使用了倍增，并且通过底层分块减小常数，对应的总复杂度为 $O(n|Q|\log n+n\log^2 n)$．

??? note "参考代码"
    ```cpp
    --8<-- "docs/misc/code/fsm/fsm_1.cpp:main"
    ```

### 习题

-   [Median Replace Hard](https://qoj.ac/problem/12010)
-   [JOISC 2024 卡牌收集](https://www.luogu.com.cn/problem/P10436)（通过 Myhill–Nerode 定理建立自动机，本题可以做到多次区间查询）

## DFA 最小化

前文提到，两个 DFA 等价当且仅当它们识别相同的正则语言．根据识别的语言不同，全体 DFA 划分为无穷多个等价类．在进行 DP 套 DP 之类的算法时，建立出来的 DFA 的 $|Q|$ 可能过大，使得外层 DP 转移复杂度过大．因此，往往需要找到 DFA 所属等价类中的最小 DFA，以减少外层 DP 转移复杂度．

上一节的 Myhill–Nerode 定理就提供了一种构造方法．但是，对于一些比较复杂的问题，直接通过 Myhill–Nerode 定理构造需要遍历相当长的字符串的集合，花费大量时间．因此，我们需要一种方法，可以从已经构造出来的 DFA（通常较为容易）出发，直接构造一个最小 DFA．这就称为 **DFA 最小化**（DFA minimization）问题．

DFA 最小化常用的算法是 **Hopcroft 算法**．由于 Myhill–Nerode 定理指出，对于任意一个可以识别某语言的 DFA，能够驱使它到达同一状态的字符串都必然是 Nerode 等价的．所有 Nerode 等价的字符串对应着最小 DFA 中的同一个状态，所以，最小 DFA 的状态一定是当前 DFA 中若干个状态的集合．我们可以从已有的 DFA 的状态集合出发，将它们划分为若干个等价类，而无需考察具体的字符串．Hopcroft 算法从最粗糙的划分 $\{F,Q\setminus F\}$ 开始，利用一系列证据 $A$，改进这个划分，直到无法进一步改进为止．这就是 Hopcroft 算法的核心想法．

所谓 **证据**  $A$，就是一个状态集合，而且它和它的补集 $Q\setminus A$ 一定对应着不同的 Nerode 等价类．也就是说，存在某个字符串 $s\in\Sigma^*$，使得分别从 $A$ 和 $Q\setminus A$ 中的状态出发，读入字符串 $s$ 后，$A$ 中的状态全部处于接受状态，而 $Q\setminus A$ 中的状态全部属于非接受状态，或者反过来．因此，如果有两个状态 $u,v\in Q$，它们在某个字符 $c$ 下恰好一个转移到证据 $A$ 中，一个转移到证据 $A$ 外，即 $\delta(u,c)\in A$ 和 $\delta(v,c)\in A$ 成立且仅成立一个，那么，$u,v$ 同样不属于一个 Nerode 等价类——状态 $\delta(u,cs)$ 和 $\delta(v,cs)$ 中有且只有一个位于接受状态．因此，利用是否成立 $\delta(u,c)\in A$ 这一点，就可以改进划分．具体地，设

$$
S_x = \{u\mid u\in P_x,~\delta(u,c)\in A\}.
$$

如果 $S_x$ 和 $P_x\setminus S_x$ 均不是空集，那么，当前的划分中状态集合 $P_x$ 就可以改进为 $S_x$ 和 $P_x\setminus S_x$．

最开始时，将接受状态集合 $F$ 作为一个证据塞入证据集合 $W$，即 $W\gets\{F\}$，并维护当前的划分为 $P\gets\{F,~Q\setminus F\}$．初始证据是显然成立的：$F$ 和 $Q\setminus F$ 中的状态绝不可能等价．每次都从证据集合 $W$ 中随意取出一个集合 $A$ 用于改进当前的划分．枚举所有的字符 $c\in\Sigma$．对当前划分 $P$ 中的每个状态集合 $P_x$ 都求出前文描述的 $S_x$．如果 $S_x\neq\varnothing$ 且 $|S_x|\neq|P_x|$，就意味着 $P_x$ 可以进一步分为两个集合 $S_x$ 和 $P_x\setminus S_x$，直接用它们替换掉 $P$ 中的 $P_x$．

每当获得更细致的划分时，就意味着获得了新的证据．原则上，可以将新得到的 $S_x$ 和 $P_x\setminus S_x$ 都塞进证据集合 $W$，等待后续进一步验证．但是，这样做并不是必要的．容易理解，对于三个证据 $P_x,S_x,P_x\setminus S_x$，只需要验证其中任意两个，就可以保证结果的正确性：因为结果只有 $\delta(u,c)\in S_x$、$\delta(u,c)\in P_x\setminus S_x$ 和 $\delta(u,c)\notin P_x$ 三种，而将集合划分成三部分只需要两次判断．因此，将 $P_x$ 划分为 $S_x$ 和 $P_x\setminus S_x$ 时，如果 $P_x$ 仍处于证据集合 $W$ 中，这说明还没有检验过证据 $P_x$，就需要将证据集合 $W$ 中的 $P_x$ 替换为 $S_x$ 和 $P_x\setminus S_x$ 两个；否则，当前的划分一定相当于[^smaller-evidence]已经检验过 $P_x$ 的结果，所以，只需要将 $S_x$ 和 $P_x\setminus S_x$ 中较小的那个塞入证据集合 $W$ 中．类似于启发式分裂，这样做可以得到优秀的复杂度．

将上述过程写成伪代码就是：

$$
\begin{array}{l}
\textbf{Algorithm } \text{Hopcroft's Algorithm}(Q, \Sigma, \delta, q_0, F): \\
\textbf{Input. } \text{DFA } A=(Q, \Sigma, \delta, q_0, F). \\
\textbf{Output. } \text{A partition of } Q \text{ into equivalence classes of the minimal DFA.} \\
\textbf{Method. } \\
\begin{array}{ll}
1 & P \gets \{F,\; Q \setminus F\} \\
2 & W \gets \{F\} \\
3 & \textbf{while } W \ne \varnothing \\
4 & \quad \text{choose and remove any } A \in W \\
5 & \quad \textbf{for each } c \in \Sigma \\
6 & \quad \quad S \gets \{ q \in Q \mid \delta(q,c) \in A \} \\
7 & \quad \quad \textbf{for each } Y \in P \text{ such that } S \cap Y \ne \varnothing \text{ and } Y \setminus S \ne \varnothing \\
8 & \quad \quad \quad Y_1 \gets S \cap Y,~Y_2 \gets Y \setminus S \\
9 & \quad \quad \quad P \gets (P \setminus \{Y\}) \cup \{Y_1, Y_2\} \\
10 & \quad \quad \quad \textbf{if } Y \in W \\
11 & \quad \quad \quad \quad W \gets (W \setminus \{Y\}) \cup \{Y_1, Y_2\} \\
12 & \quad \quad \quad \textbf{else} \\
13 & \quad \quad \quad \quad \text{add the smaller of } Y_1 \text{ and } Y_2 \text{ to } W \\
14 & \textbf{return } P
\end{array}
\end{array}
$$

算法实现时，复杂度的瓶颈在于 $S$ 的计算．直接遍历所有 $q\in Q$ 进而判断 $\delta(q,c)\in A$ 是否成立是不可行的．因此，需要在算法运行前，预处理反向转移边 $\{q\in Q\mid \delta(q,c)=a\}$，从而，利用这些反向转移，遍历 $a\in A$，就可以得到集合 $S$．这样做可以保证每条转移 $\delta(q,c)=a$ 只会在 $a$ 属于某个证据时才会遍历到；而前文的证据筛选方法保证了，算法中实际用到的包含 $a$ 的证据序列 $A_1\supset A_2\supset\cdots\supset A_k$ 中，前一个至少是后一个的两倍大小，因此，$k\in O(\log n)$．也就是说，每条转移边至多只会遍历 $O(\log n)$ 次，而总的转移数目是 $n|\Sigma|$ 的，因此，总的复杂度就是 $O(n|\Sigma|\log n)$ 的．

参考实现如下：[^detail]

??? example "参考实现"
    ```cpp
    --8<-- "docs/misc/code/fsm/dfa.hpp:hopcroft"
    ```

这一参考实现允许自动机的状态带有任何整数取值的标签，而并非简单的「接受」与「不接受」的二元标签．从参考实现可以看出，与基础 Hopcroft 算法的唯一不同就在于初始划分和证据集合的构造．这种拓展的自动机也称为 [Moore 机](https://en.wikipedia.org/wiki/Moore_machine)．它的一个应用可以看本节的第二个例题．

### 例题

本节通过两道例题介绍如何实际应用 DFA 最小化的技巧．

???+ example "例题"
    给定一个长度为 $n$ 的 $01?$ 串 $a$，初始变量 $x = 0$，我们按顺序遍历每一位 $a_i$ 并执行如下操作：
    
    1.  若 $a_i = 0$，令 $x \gets x - \text{lowbit}(x)$；
    2.  若 $a_i = 1$，令 $x \gets x + \text{lowbit}(2^k - 1 - x)$；
    3.  若 $a_i = ?$，可任选 $0$ 或 $1$，对应上述两种操作之一．
    
    最终若 $x \in [0, r]$，则称该操作序列是好的．
    
    现在需要对每个 $j = 1 \ldots n$，求在强制 $a_j = 0$ 的前提下，有多少「好的」完整序列．特别地，$a_j = 1$ 时，答案为 $0$．
    
    $1\le n\le 10^5,~1\le k\le 20,~0\le r<2^k$．输出对 $998244353$ 取模．

??? note "题解"
    考虑朴素 DP．设 $f_{i,j}$ 表示从 $x=0$ 开始，经过 $[1,i]$ 的操作，当前数为 $j$ 的方案数．设 $g_{i,j}$ 表示从 $x=j$ 开始，经过 $[i,n]$ 的操作，最终 $x \in [0, r]$ 的方案数．强制 $a_i=0$ 的答案，就是 $\sum_j f_{i-1,j}g_{i+1,j - \text{lowbit}(j)}$．复杂度是 $O(n2^k)$．
    
    考虑直接将 $j$ 的转移建成 DFA，然后跑 DFA 最小化，再 DP 就可以了．

??? note "参考代码"
    ```cpp
    --8<-- "docs/misc/code/fsm/fsm_2.cpp:main"
    ```

???+ example "[Minimal Subset Difference](https://codeforces.com/contest/956/problem/F)"
    定义 $f(n)$ 表示将十进制数 $n$ 所有数码之间填入加号或者减号，最终得到的值的绝对值最小值．
    
    $T$ 组询问．每组询问给定 $l, r, k$，求满足 $l \le m \le r$ 且 $f(m) \le k$ 的 $m$ 的个数．
    
    $1 \le T \le 5\times 10^4$，$1 \le l \le r \le 10^{18}$，$0 \le k \le 9$．

??? note "题解"
    先给出一种贪心地计算 $f(n)$ 的方法．从高位向低位考虑一个数，最开始，设得到的数的和是 $0$．计算到某一数位，如果当前合成出的数如果是负数就加上当前数位，如果是正数就减去当前数位．这么处理，贪心计算出的 $f(n)$ 的绝对值一定小于等于 $9$．所以真实的 $f(n)$ 的绝对值一定小于等于 $9$．
    
    我们进一步思考，要合成出最终的答案，中间过程中能够合成出来的数最大能是多少．因为答案一定是小于等于 $9$ 的，而且数位只有 $18$ 位，每次最多只能加减 $9$．过程中能够合成出来的数肯定是小于等于 $90$ 的，否则最后减不回来．实际上，这个上限还能够更低[^upper-bound]．
    
    考虑朴素 DP 套 DP．首先，思考内层 DP 怎么判定一个数的答案：定义 $g_{i,c}$ 表示这个数只根据前 $i$ 位，能否合成出 $c$．根据前文，$c$ 只用保留小于等于 $90$ 的数．如果当前这一位填的是 $v$，那么，有转移：
    
    $$
    g_{i+1,c+v}\gets g_{i,c},~
    g_{i+1,|c-v|}\gets g_{i,c}.
    $$
    
    外层 DP 考虑数位 DP．将询问差分．设状态为 $f_{\textit{len},\textit{lim},\textit{sta}}$，它的下标分别表示已经考虑到第 $\textit{len}$ 位，是否有上界限制，当前自动机的状态位于 $\textit{sta}$ 等．
    
    与普通的 DFA 不同，我们需要对自动机的每个状态记录对应的答案．跑一次暴力搜索，会发现内层 DP 的状态数只有 $19564$．然后接下来直接跑 DFA 最小化，可以将状态数优化到 $715$．
    
    此时我们将 $\textit{lim}=0$ 的数位 DP 答案都预处理出来，在多测时就只需要跑 $\textit{lim}=1$ 的情况，可以很快地求出答案．
    
    时间复杂度 $O(|S||\Sigma|\log |S|+(|Q||\Sigma|+T)|\Sigma|\log_{10} V)$（$|S|=19564$，$|Q|=715$）．

??? note "参考代码"
    ```cpp
    --8<-- "docs/misc/code/fsm/fsm_3.cpp:main"
    ```

### 习题

-   [Language Recognition](http://poj.org/problem?id=3576)
-   [Equanimous](https://qoj.ac/problem/7083)

## 自动机常见应用

本节列举了一些算法竞赛中常见的自动机的应用[^is-dfa]．

### 字典树

[字典树](../string/trie.md) 是大部分 OIer 接触到的第一个自动机，接受且仅接受指定的字符串集合中的元素．转移函数就是 Trie 上的边，接受状态是将每个字符串插入到 Trie 时到达的那个状态．

### KMP 自动机

[KMP 算法](../string/kmp.md) 可以视作自动机，基于字符串 $s$ 的 KMP 自动机接受且仅接受以 $s$ 为后缀的字符串，其接受状态为 $|s|$．

转移函数：

$$
\delta(i, c)=
\begin{cases}
i+1&s[i+1]=c\\
0&s[1]\ne c\land i=0\\
\delta(\pi(i),c)&s[i+1]\ne c\land i>0
\end{cases}
$$

### AC 自动机

[AC 自动机](../string/ac-automaton.md) 接受且仅接受以指定的字符串集合中的某个元素为后缀的字符串．也就是 Trie + KMP．

### 后缀自动机

[后缀自动机](../string/sam.md) 接受且仅接受指定字符串的后缀．

### 广义后缀自动机

[广义后缀自动机](../string/general-sam.md) 接受且仅接受指定的字符串集合中的某个元素的后缀．也就是 Trie + SAM．

广义 SAM 与 SAM 的关系就是 AC 自动机与 KMP 自动机的关系．

### 回文自动机

[回文自动机](../string/pam.md) 比较特殊，它不能非常方便地定义为自动机．

如果需要定义的话，它接受且仅接受某个字符串的所有回文子串的 **中心及右半部分**．

「中心及右边部分」在奇回文串中就是字面意思，在偶回文串中定义为一个特殊字符加上右边部分．这个定义看起来很奇怪，但它能让 PAM 真正成为一个自动机，而不仅是两棵树．

### 序列自动机

[序列自动机](../string/seq-automaton.md) 接受且仅接受指定字符串的子序列．

### DP 套 DP

[DP 套 DP](../dp/dp-of-dp.md) 是自动机的一个应用，可以看作是先通过内层 DP 建出自动机，再在外层通过自动机上的 DP 实现计数、最优化任务的技巧．

## 后缀链接

由于自动机和匹配有着密不可分的关系，而匹配的一个基本思想是「这个串不行，就试试它的后缀可不可以」，所以在很多自动机（KMP、AC 自动机、SAM、PAM）中，都有后缀链接的概念．

一个状态会对应若干字符串．它的后缀链接，就指向自动机上该状态对应的字符串的公共真后缀中，最长的那个对应的状态．一般地，后缀链接会形成一棵树，并且不同自动机的后缀链接树有着一些相同的性质，学习时可以加以注意．

## 拓展阅读

-   [计算复杂性（1）Warming Up: 自动机模型](https://lingeros-tot.github.io/2019/03/05/Warming-Up-自动机模型/)
-   [国家集训队 2021 论文 徐哲安 浅谈有限状态自动机及其应用](https://github.com/OIerTFX/IOI/blob/master/%E5%9B%BD%E5%AE%B6%E9%9B%86%E8%AE%AD%E9%98%9F2021%E8%AE%BA%E6%96%87%E9%9B%86/pdf-files/%E5%BE%90%E5%93%B2%E5%AE%89%20%E6%B5%85%E8%B0%88%E6%9C%89%E9%99%90%E7%8A%B6%E6%80%81%E8%87%AA%E5%8A%A8%E6%9C%BA%E5%8F%8A%E5%85%B6%E5%BA%94%E7%94%A8.pdf)
-   [Myhill–Nerode theorem - Wikipedia](https://en.wikipedia.org/wiki/Myhill%E2%80%93Nerode_theorem)
-   Knuutila, Timo. "Re-describing an algorithm by Hopcroft." Theoretical Computer Science 250, no. 1-2 (2001): 333-363.
-   Hopcroft, John E., Rajeev Motwani, and Jeffrey D. Ullman. "Introduction to automata theory, languages, and computation." Acm Sigact News 32, no. 1 (2001): 60-65.

[^nfa-and-nfaepsilon]: 这个定义中我们允许状态之间通过空字符（$\varepsilon$）转移，因此更准确地说，这是一个带 $\varepsilon$ 转移的非确定有限自动机（NFA-$\varepsilon$）．有些教材中将它直接称为 NFA，为简洁起见，本文采用这一用法．在理论上 NFA 与 NFA-$\varepsilon$ 是有所区分的，但是实际上它们的计算能力是一致的．

[^state-elimination-method]: 详见 [国家集训队 2021 论文 徐哲安 浅谈有限状态自动机及其应用](https://github.com/OIerTFX/IOI/blob/master/%E5%9B%BD%E5%AE%B6%E9%9B%86%E8%AE%AD%E9%98%9F2021%E8%AE%BA%E6%96%87%E9%9B%86/pdf-files/%E5%BE%90%E5%93%B2%E5%AE%89%20%E6%B5%85%E8%B0%88%E6%9C%89%E9%99%90%E7%8A%B6%E6%80%81%E8%87%AA%E5%8A%A8%E6%9C%BA%E5%8F%8A%E5%85%B6%E5%BA%94%E7%94%A8.pdf) 中 3.2 节．

[^prove-regular-language]: 详见 [官方题解](https://qoj.ac/download.php?type=attachments&id=2079&r=1)．

[^smaller-evidence]: 此处的「相当于」指的是，尽管实际上 $P_x$ 可能并没有实际检验过，但是，即使对当前划分进行 $P_x$ 的检验，也不会有任何改进．简单理解，就是在集合分裂得到的证据集合的树上，它的某个祖先和路径上的所有旁支都已经得到了检验，因此，可以归纳地说明，就相当于它也已经检验过了．

[^detail]: 算法实现中有一处细节：对于一个证据 $A$，有可能检验完一部分字符后，这个证据集合就已经分裂为 $B$ 和 $C$ 了．不妨设 $|B|\ge |C|$．由于参考实现中，较小的集合 $C$ 插入到了证据队列的末尾，而较大的证据集合 $B$ 替换到了集合 $A$ 原来的位置．算法继续运行时，实际只是利用证据 $B$ 检验剩余的字符．这样做是正确的．这是因为对于已经检验完的字符，至少验证了 $A$ 和 $C$ 两个集合；而对于尚未检验的字符，至少验证了 $B$ 和 $C$ 两个集合．

[^upper-bound]: 详见 [国家集训队 2021 论文 徐哲安 浅谈有限状态自动机及其应用](https://github.com/OIerTFX/IOI/blob/master/%E5%9B%BD%E5%AE%B6%E9%9B%86%E8%AE%AD%E9%98%9F2021%E8%AE%BA%E6%96%87%E9%9B%86/pdf-files/%E5%BE%90%E5%93%B2%E5%AE%89%20%E6%B5%85%E8%B0%88%E6%9C%89%E9%99%90%E7%8A%B6%E6%80%81%E8%87%AA%E5%8A%A8%E6%9C%BA%E5%8F%8A%E5%85%B6%E5%BA%94%E7%94%A8.pdf) 中的例题 5.2．

[^is-dfa]: 本文对自动机的定义要求它是完备的，即任一状态在任一字符下都必须有转移．对这些字符串相关的自动机的描述中，通常会忽略失配状态．Trie、SAM 等都是这样的例子．为了与本文提供的定义相适应，需要在这些自动机的描述中显式地添加失配状态．


## misc/garsia-wachs.md

## 简介

**Garsia–Wachs 算法**（Garsia–Wachs Algorithm）是计算机用来在 **线性时间** 内构建 **最优二叉查找树** 和 **字母霍夫曼码** 的有效算法．它以 Adriano Garsia 和 Michelle L. Wachs 的名字命名，他们于 1977 年发表了相关论文．

## 问题描述

一个整数 $n$，对于 $n+1$ 个非负权值 $w_{0},w_{1},\dots ,w_{n}$，构造一棵有根且 $n$ 个内部节点都有两个子节点的二叉树，这意味着这棵二叉树有 $n+1$ 个叶节点．我们将 $n+1$ 的输入序列与二叉树结点顺序一一映射，目标是在所有具有 $n$ 个内部节点的可能的树结构中找到一棵树，使外部从根到每个叶子的路径长度的权重和最小．

### 最优二叉查找树

这个问题可以理解为 $n$ 个有序键构造二叉查找树的问题，假设树将仅用于搜索树中不存在的值．在这种情况下，$n$ 个键将搜索值的空间划分为 $n+1$ 个区间，并且这些区间之一的权重可以作为搜索值落在那个区间的概率．外部路径长度的加权和控制了查找的预期时间．

### 字母霍夫曼码

这个问题也可以用作构建霍夫曼码．这是一种通过使用二进制值的可变长度序列明确编码 $n+1$ 给定值的方法．在这种解释中，值的代码由从树中的根到叶子的路径上从父到子的左步和右步序列给出（例如，左为 $0$，右为 $1$）．与标准霍夫曼码不同，以这种方式构造的霍夫曼码是按字母顺序排列的，也就是说这些二进制码的排序顺序与值的输入顺序相同．如果一个值的权重是它在编码消息中的频率，那么 Garsia–Wachs 算法的输出是将消息长度压缩到最短的，按字母顺序排列的霍夫曼代码．

## 过程

Garsia–Wachs 算法一般包括三个阶段：

1.  构建一个值位于叶子的二叉树，注意顺序可能错误．
2.  计算树中根到每个叶子的距离．
3.  构建另一个二叉树，叶子的距离相同，但顺序正确．

![](./images/garsia-wachs.png)

如上图所示，在算法的第一阶段，通过查找合并输入序列的无序三元组构建的二叉树（左侧），和算法输出的正确排序的二叉树，其中叶子高度与另一棵树一样．

如果输入在序列的开始和结束处增加了两个标记值 $\infty$（或任何足够大的有限值），则算法的第一阶段更容易描述．所以在竞赛题解中使用 Garsia–Wachs 算法时，对于一个长度为 $n$ 的数组 $\mathit{num}$，我们一般定义 $\mathit{num}[0] = \mathit{num}[n+1] = \infty$．

第一阶段维护了一个由最初为每个非标志（non-sentinel）输入权重创建的单节点树组成的森林．每棵树都与一个值相关联，其叶子的权重之和为每个非标志输入权重构成一个树节点．为了维护这些值的序列，每端会有两个标记值．初始序列只是叶权重作为输入的顺序．然后重复执行以下步骤，每一步都减少输入序列的长度，直到只有一棵树包含了所有叶子：

-   在序列中找到前三个连续的权重值 $x$，$y$，$z$ 使得 $x \leq z$．因为序列结尾的标志值大于之前的任意两个有限值，所以总是存在这样的三元组．
-   从序列中移除 $x$ 和 $y$，并创建一个新的树节点作为 $x$ 和 $y$ 节点的父节点，值为 $x+y$．
-   在原来 $x$ 的位置以前大于或等于 $x+y$ 且距 $x$ 最近的值的右边重新插入新节点．因为左标志值的存在，所以总是存在这样的位置．

为了有效地实现这一阶段，该算法可以在任何平衡二叉查找树结构中维护当前值序列．这样的结构允许我们在对数时间内移除 $x$ 和 $y$，并重新插入它们的新父节点．在每一步中，数组中位于偶数索引上直到 $y$ 值的权重形成了一个递减序列，位于奇数索引位的权重形成另一个递减序列．因此，重新插入 $x+y$ 的位置可以通过在对数时间内对这两个递减序列使用平衡树执行两次二分查找找到．通过从前一个三元组 $z$ 值开始的线性顺序搜索，我们可以在总线性时间复杂度内执行对满足 $x \leq z$ 的第一个位置的搜索．

Garsia–Wachs 算法的第三阶段的证明，即存在另一棵具有相同距离的树并且这棵树提供了问题的最优解，是很重要的．但是由于其证明方式有多种且过于复杂，此处略去．在第三阶段为正确的前提下，第二和第三阶段很容易在线性时间内实现．因此，在长度为 $n$ 的输入序列上，Garsia–Wachs 算法的总时间复杂度为 $O(n\log n)$．

## 应用

函数性编程语言 Haskell 的 [garsia-wachs package](https://hackage.haskell.org/package/garsia-wachs) 对 Garsia–Wachs 算法做了函数性实现．它主要用于构建最佳搜索表，或者以最优复杂度平衡 [rope](https://hackage.haskell.org/package/rope) 数据结构．

???+ note "注释"
    **rope** 是 Haskell 语言中用于操作带有可选注释的字节串（bytestring）[手指树](../ds/finger-tree.md) 的工具．

## 例题

???+ note "[POJ 1738 An old Stone Game](http://poj.org/problem?id=1738)"
    有一个古老的石头游戏．在游戏开始时，玩家将 $n$($1 \leq n \leq 50000$) 堆石头排成一行．目标是将石头合并成一堆，规则如下：在游戏的每一步，玩家可以将相邻的两个堆合并成一个新的堆．分数是新堆的石头总数．请计算总分中的最小值．

??? note "解题思路"
    石子合并的题目很经典，一般我们可以用区间 DP 解答，但是当数据量很大，例如此题中的 $n$($1 \leq n \leq 50000$) 时，用 Garsia–Wachs 算法求解更高效：第一步，初始化一个大小为 $n$ 的数组 $\mathit{num}[n]$，其中 $\mathit{num}[0] = \mathit{num}[n+1] = \infty$．第二步，每次找到一个最小的 $i$ 使 $\mathit{num}[i-1] \leq \mathit{num}[i+1]$，并将 $\mathit{num}[i-1], \mathit{num}[i]$ 合并为 $\mathit{temp}$; 找到前面一个最大的 $j$ 使得 $\mathit{num}[j] > \mathit{temp}$, 将 $\mathit{temp}$ 移到 $j$ 后面．重复这一步直到剩余堆数为 $1$．
    关于每次只能合并相邻石子堆的要求，因为 $\mathit{num}[j]\geq \mathit{num}[i-1] + \mathit{num}[i]$，我们可以将 $\mathit{num}[j+1]$ 到 $\mathit{num}[i-2]$ 看成一个 $\mathit{num}[mid]$ 的整体，所以一定是先合并 $\mathit{sum}$．因此没有违背题目要求．

???+ note "[ATCODER N-Slimes](https://atcoder.jp/contests/dp/tasks/dp_n)"
    $N$ 个史莱姆排成一排．最初左边第 $i$ 个史莱姆的大小为 $a_{i}$．Taro 试图将所有史莱姆组合成一个更大的史莱姆．他会反复执行以下操作，直到只有一个史莱姆：
    选择两个相邻的史莱姆，并将它们组合成一个新的史莱姆．新的史莱姆的大小为 $x+y$，其中 $x$ 和 $y$ 是组合之前史莱姆的大小．这一步骤有产生 $x+y$ 的成本．合成史莱姆时史莱姆的位置关系不会改变．找出可能发生的最小总成本．

## 参考资料与拓展阅读

1.  [Garsia–Wachs algorithm - Wikipedia](https://en.wikipedia.org/wiki/Garsia%E2%80%93Wachs_algorithm)
2.  [Data.Algorithm.GarsiaWachs - Hackage Haskell](https://hackage.haskell.org/package/garsia-wachs-1.2/docs/Data-Algorithm-GarsiaWachs.html)
3.  [garsia-wachs: A Functional Implementation of the Garsia-Wachs Algorithm](https://hackage.haskell.org/package/garsia-wachs)
4.  [Sentinel value - Wikipedia](https://en.wikipedia.org/wiki/Sentinel_value)
5.  [A new proof of the Garsia-Wachs algorithm](https://www.sciencedirect.com/science/article/abs/pii/0196677488900090)


## misc/hill-climbing.md

## 简介

爬山算法是一种局部择优的方法，采用启发式方法，是对深度优先搜索的一种改进，它利用反馈信息帮助生成解的决策．

直白地讲，就是当目前无法直接到达最优解，但是可以判断两个解哪个更优的时候，根据一些反馈信息生成一个新的可能解．

因此，爬山算法每次在当前找到的最优方案 $x$ 附近寻找一个新方案．如果这个新的解 $x'$ 更优，那么转移到 $x'$，否则不变．

这种算法对于单峰函数显然可行．

Q：都知道是单峰函数了为什么不三分呢？

A：爬山算法的优势在于当正解的写法你并不了解（常见于毒瘤计算几何和毒瘤数学题），或者本身状态维度很多，无法容易地写分治（例 2 就可以用二分完成合法正解）时，可以通过非常暴力的计算得到最优解．

但是对于多数需要求解的函数，爬山算法很容易进入一个局部最优解，如下图（最优解为 $\color{green}{\Uparrow}$，而爬山算法可能找到的最优解为 $\color{red}{\Downarrow}$）．

![](./images/hill-climbing.png)

## 具体实现

爬山算法一般会引入温度参数（类似模拟退火）．类比地说，爬山算法就像是一只兔子喝醉了在山上跳，它每次都会朝着它所认为的更高的地方（这往往只是个不准确的趋势）跳，显然它有可能一次跳到山顶，也可能跳过头翻到对面去．不过没关系，兔子翻过去之后还会跳回来．显然这个过程很没有用，兔子永远都找不到出路，所以在这个过程中兔子冷静下来并在每次跳的时候更加谨慎，少跳一点，以到达合适的最优点．

兔子逐渐变得清醒的过程就是降温过程，即温度参数在爬山的时候会不断减小．

关于降温：降温参数是略小于 $1$ 的常数，一般在 $[0.985, 0.999]$ 中选取．

## 例题

???+ example "[「JSOI2008」球形空间产生器](https://www.luogu.com.cn/problem/P4035)"
    给出 $n$ 维空间中的 $n + 1$ 个点，已知它们在同一个 $n$ 维球面上，求出球心．$n \leq 10$，坐标绝对值不超过 $20000$．

??? note "解答"
    很明显的单峰函数，可以使用爬山解决．本题算法流程：
    
    1.  初始化球心为各个给定点的重心（即其各维坐标均为所有给定点对应维度坐标的平均值），以减少枚举量．
    2.  对于当前的球心，求出每个已知点到这个球心欧氏距离的平均值．
    3.  遍历所有已知点．记录一个改变值 $\textit{cans}$（分开每一维度记录）对于每一个点的欧氏距离，如果大于平均值，就把改变值加上差值，否则减去．实际上并不用判断这个大小问题，只要不考虑绝对值，直接用坐标计算即可．这个过程可以形象地转化成一个新的球心，在空间里推来推去，碰到太远的点就往点的方向拉一点，碰到太近的点就往点的反方向推一点．
    4.  将我们记录的 $\textit{cans}$ 乘上温度，更新球心，回到步骤 2
    5.  在温度小于某个给定阈值的时候结束．
    
    因此，我们在更新球心的时候，不能直接加上改变值，而是要加上改变值与温度的乘积．
    
    并不是每一道爬山题都可以具体地用温度解决，这只是一个例子．

??? note "参考代码"
    ```cpp
    --8<-- "docs/misc/code/hill-climbing/hill-climbing_1.cpp"
    ```

???+ example "[「BZOJ 3680」吊打 XXX](https://hydro.ac/p/bzoj-P3680)"
    求 $n$ 个点的带权类费马点．

??? note "解答"
    框架类似，用了点物理知识．

??? note "参考代码"
    ```cpp
    --8<-- "docs/misc/code/hill-climbing/hill-climbing_2.cpp"
    ```

## 优化

很容易想到的是，为了尽可能获取优秀的答案，我们可以多次爬山．方法有修改初始状态/修改降温参数/修改初始温度等，然后开一个全局最优解记录答案．每次爬山结束之后，更新全局最优解．

这样处理可能会存在的问题是超时，在正式考试时请手造大数据测试调参．

## 劣势

其实爬山算法的劣势上文已经提及：它容易陷入一个局部最优解．当目标函数不是单峰函数时，这个劣势是致命的．因此我们要引进 [**模拟退火**](./simulated-annealing.md)．


## misc/hoverline.md

author: mwsht, sshwy, ouuan, Ir1d, Henry-ZHR, hsfzLZH1

## 引入

悬线法的适用范围是单调栈的子集．具体来说，悬线法可以应用于满足以下条件的题目：

-   需要在扫描序列时维护单调的信息；
-   可以使用单调栈解决；
-   不需要在单调栈上二分．

看起来悬线法可以被替代，用处不大，但是悬线法概念比单调栈简单，更适合初学 OI 的选手理解并解决最大子矩阵等问题．

## 例题

???+ note "[SPOJ HISTOGRA - Largest Rectangle in a Histogram](https://www.spoj.com/problems/HISTOGRA)"
    大意：在一条水平线上有 $n$ 个宽为 $1$ 的矩形，求包含于这些矩形的最大子矩形面积．

悬线，就是一条竖线，这条竖线有初始位置和高度两个性质，可以在其上端点不超过当前位置的矩形高度的情况下左右移动．

对于一条悬线，我们在这条上端点不超过当前位置的矩形高度且不移出边界的前提下，将这条悬线左右移动，求出其最多能向左和向右扩展到何处，此时这条悬线扫过的面积就是包含这条悬线的尽可能大的矩形．容易发现，最大子矩形必定是包含一条初始位置为 $i$，高度为 $h_i$ 的悬线．枚举实现这个过程的时间复杂度为 $O(n ^ 2)$，但是我们可以用悬线法将其优化到 $O(n)$．

我们考虑如何快速找到悬线可以到达的最左边的位置．

### 过程

定义 $l_i$ 为当前找到的 $i$ 位置的悬线能扩展到的最左边的位置，容易得到 $l_i$ 初始为 $i$，我们需要进一步判断还能不能进一步往左扩展．

-   如果当前 $l_i = 1$，则已经扩展到了边界，不可以．
-   如果当前 $a_i > a_{l_i - 1}$，则从当前悬线扩展到的位置不能再往左扩展了．
-   如果当前 $a_i \le a_{l_i - 1}$，则从当前悬线还可以往左扩展，并且 $l_i - 1$ 位置的悬线能向左扩展到的位置，$i$ 位置的悬线一定也可以扩展到，于是我们将 $l_i$ 更新为 $l_{l_i - 1}$，并继续执行判断．

通过摊还分析，可以证明每个 $l_i$ 最多会被其他的 $l_j$ 遍历到一次，因此时间复杂度为 $O(n)$．

### 实现

??? note "参考代码"
    ```cpp
    --8<-- "docs/misc/code/hoverline/hoverline_1.cpp"
    ```

???+ note "[UVa1619 感觉不错 Feel Good](https://onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&category=24&page=show_problem&problem=4494)"
    对于一个长度为 $n$ 的数列，找出一个子区间，使子区间内的最小值与子区间内元素和的乘积最大，要求在满足舒适值最大的情况下最小化长度，最小化长度的情况下最小化左端点序号．

本题中我们可以考虑枚举最小值，将每个位置的数 $a_i$ 当作最小值，并考虑从 $i$ 向左右扩展，找到满足 $\min\limits _ {j = l} ^ r a_j = a_i$ 的尽可能向左右扩展的区间 $[l, r]$．这样本题就被转化成了悬线法模型．

??? note "参考代码"
    ```cpp
    --8<-- "docs/misc/code/hoverline/hoverline_2.cpp"
    ```

## 最大子矩形

???+ note "[P4147 玉蟾宫](https://www.luogu.com.cn/problem/P4147)"
    给定一个 $n \times m$ 的包含 `'F'` 和 `'R'` 的矩阵，求其面积最大的子矩阵的面积 $\times 3$，使得这个子矩阵中的每一位的值都为 `'F'`．

我们会发现本题的模型和第一题的模型很像．仔细分析，发现如果我们每次只考虑某一行的所有元素，将位置 $(x, y)$ 的元素尽可能向上扩展的距离作为该位置的悬线长度，那最大子矩阵一定是这些悬线向左右扩展得到的尽可能大的矩形中的一个．

??? note "参考代码"
    ```cpp
    --8<-- "docs/misc/code/hoverline/hoverline_3.cpp"
    ```

## 习题

-   [P1169「ZJOI2007」棋盘制作](https://www.luogu.com.cn/problem/P1169)


## misc/job-order.md

你有 $n$ 个任务，要求你找到一个代价最小的顺序执行他们．第 $i$ 个任务花费的时间是 $t_i$，而第 $i$ 个任务等待 $t$ 的时间会花费 $f_i(t)$ 的代价．

形式化地说，给出 $n$ 个函数 $f_i$ 和 $n$ 个数 $t_i$，求一个排列 $p$，最小化

$$
F(p)=\sum_{i=1}^nf_{p_i}\left(\sum_{j=1}^{i-1}t_{p_j}\right)
$$

## 特殊的代价函数

### 线性代价函数

首先我们考虑所有的函数是线性的函数，即 $f_i(x)=c_ix+d_i$，其中 $c_i$ 是非负整数．显然我们可以事先把常数项加起来，因此函数就转化为了 $f_i(x)=c_ix$ 的形式．

考虑两个排列 $p$ 和 $p'$，其中 $p'$ 是把 $p$ 的第 $i$ 个位置上的数和 $i+1$ 个位置上的数交换得到的排列．则

$$
\begin{aligned}
F(p')-F(p)&=c_{p'_i}\sum_{j=1}^{i-1}t_{p'_j}+c_{p'_{i+1}}\sum_{j=1}^{i}t_{p'_j}
-\left(c_{p_i}\sum_{j=1}^{i-1}t_{p_j}+c_{p_{i+1}}\sum_{j=1}^{i}t_{p_j}\right)\\
&=c_{p_i}t_{p_{i+1}}-c_{p_{i+1}}t_{p_i}
\end{aligned}
$$

于是我们使用如果 $c_{p_i}t_{p_{i+1}}-c_{p_{i+1}}t_{p_i}<0$ 就交换的策略做一下排序就可以了．写成 $\dfrac{c_{p_i}}{t_{p_i}}<\dfrac{c_{p_{i+1}}}{t_{p_{i+1}}}$ 的形式，就可以理解为将排列按 $\dfrac{c_i}{t_i}$ 降序排序．

处理这个问题，我们的思路是考虑微扰后的变换情况，贪心地选取最优解．

### 指数代价函数

考虑代价函数的形式为 $f_i(x)=c_i\mathrm{e}^{ax}$，其中 $c_i\ge 0,a>0$．

我们沿用之前的思路，考虑将 $i$ 和 $i+1$ 的位置上的数交换引起的代价变化．最终得到的算法是将排列按照 $\dfrac{1-\mathrm{e}^{at_i}}{c_i}$ 升序排序．

### 相同的单增函数

我们考虑所有的 $f_i(x)$ 是同一个单增函数．那么显然我们将排列按照 $t_i$ 升序排序即可．

## Livshits–Kladov 定理

Livshits–Kladov 定理成立，当且仅当代价函数是以下三种情况：

-   线性函数：$f_i(t) = c_it + d_i$，其中 $c_i\ge 0$；
-   指数函数：$f_i(t) = c_i \mathrm{e}^{a t} + d_i$，其中 $c_i,a>0$；
-   相同的单增函数：$f_i(t) = \phi(t)$，其中 $\phi(t)$ 是一个单增函数．

定理是在假设代价函数足够平滑（存在三阶导数）的条件下证明的．在这三种情况下，问题的最优解可以通过简单的排序在 $O(n\log n)$ 的时间内解决．

**本页面主要译自博文 [Задача Джонсона с одним станком](http://e-maxx.ru/algo/johnson_problem_1) 与其英文翻译版 [Scheduling jobs on one machine](https://cp-algorithms.com/schedules/schedule_one_machine.html)．其中俄文版版权协议为 Public Domain + Leave a Link；英文版版权协议为 CC-BY-SA 4.0．**


## misc/josephus.md

约瑟夫问题由来已久，而这个问题的解法也在不断改进，只是目前仍没有一个极其高效的算法（log 以内）解决这个问题．

## 问题描述

> n 个人标号 $0,1,\cdots, n-1$．逆时针站一圈，从 $0$ 号开始，每一次从当前的人逆时针数 $k$ 个，然后让这个人出局．问最后剩下的人是谁．

这个经典的问题由约瑟夫于公元 1 世纪提出，尽管他当时只考虑了 $k=2$ 的情况．现在我们可以用许多高效的算法解决这个问题．

## 过程

### 朴素算法

最朴素的算法莫过于直接枚举．用一个环形链表枚举删除的过程，重复 $n-1$ 次得到答案．复杂度 $\Theta (n^2)$．

### 简单优化

寻找下一个人的过程可以用线段树优化．具体地，开一个 $0,1,\cdots, n-1$ 的线段树，然后记录区间内剩下的人的个数．寻找当前的人的位置以及之后的第 $k$ 个人可以在线段树上二分做．

### 线性算法

设 $J_{n,k}$ 表示规模分别为 $n,k$ 的约瑟夫问题的答案．我们有如下递归式

$$
J_{n,k}=(J_{n-1,k}+k)\bmod n
$$

这个也很好推．你从 $0$ 开始数 $k$ 个，让第 $k-1$ 个人出局后剩下 $n-1$ 个人，你计算出在 $n-1$ 个人中选的答案后，再加一个相对位移 $k$ 得到真正的答案．这个算法的复杂度显然是 $\Theta (n)$ 的．

???+ note "实现"
    ```cpp
    int josephus(int n, int k) {
      int res = 0;
      for (int i = 1; i <= n; ++i) res = (res + k) % i;
      return res;
    }
    ```

### 对数算法

对于 $k$ 较小 $n$ 较大的情况，本题还有一种复杂度为 $\Theta (k\log n)$ 的算法．

考虑到我们每次走 $k$ 个删一个，那么在一圈以内我们可以删掉 $\left\lfloor\frac{n}{k}\right\rfloor$ 个，然后剩下了 $n-\left\lfloor\frac{n}{k}\right\rfloor$ 个人．这时我们在第 $\left\lfloor\frac{n}{k}\right\rfloor\cdot k$ 个人的位置上．而你发现它等于 $n-n\bmod k$．于是我们继续递归处理，算完后还原它的相对位置．还原相对位置的依据是：每次做一次删除都会把数到的第 $k$ 个人删除，他们的编号被之后的人逐个继承，也即用 $n-\left\lfloor\frac{n}{k}\right\rfloor$ 人环算时每 $k$ 个人即有 $1$ 个人的位置失算，因此在得数小于 $0$ 时，用还没有被删去 $k$ 倍数编号的 $n$ 人环的 的 $n$ 求模，在得数大于等于 $0$ 时，即可以直接乘 $\frac{k}{k-1}$, 于是得到如下的算法：

???+ note "实现"
    ```cpp
    int josephus(int n, int k) {
      if (n == 1) return 0;
      if (k == 1) return n - 1;
      if (k > n) return (josephus(n - 1, k) + k) % n;  // 线性算法
      int res = josephus(n - n / k, k);
      res -= n % k;
      if (res < 0)
        res += n;  // mod n
      else
        res += res / (k - 1);  // 还原位置
      return res;
    }
    ```

可以证明这个算法的复杂度是 $\Theta (k\log n)$ 的．我们设这个过程的递归次数是 $x$，那么每一次问题规模会大致变成 $\displaystyle n\left(1-\frac{1}{k}\right)$，于是得到

$$
n\left(1-\frac{1}{k}\right)^x=1
$$

解这个方程得到

$$
x=-\frac{\ln n}{\ln\left(1-\frac{1}{k}\right)}
$$

下面我们证明该算法的复杂度是 $\Theta (k\log n)$ 的．

???+ note "证明"
    考虑 $\displaystyle \lim _{k \rightarrow \infty} k \log \left(1-\frac{1}{k}\right)$，我们有
    
    $$
    \begin{aligned}
    \lim _{k \rightarrow \infty} k \log \left(1-\frac{1}{k}\right)&=\lim _{k \rightarrow \infty} \frac{\log \left(1-\frac{1}{k}\right)}{1 / k}\\
    &=\lim _{k \rightarrow \infty} \frac{\frac{\mathrm d}{\mathrm d k} \log \left(1-\frac{1}{k}\right)}{\frac{\mathrm d}{\mathrm d k}\left(\frac{1}{k}\right)}\\
    &=\lim _{k \rightarrow \infty} \frac{\frac{1}{k^{2}\left(1-\frac{1}{k}\right)}}{-\frac{1}{k^{2}}}\\
    &=\lim _{k \rightarrow \infty}-\frac{k}{k-1}\\
    &=-\lim _{k \rightarrow \infty} \frac{1}{1-\frac{1}{k}}\\
    &=-1
    \end{aligned}
    $$
    
    所以 $x \sim k \ln n, k\to \infty$，即 $-\dfrac{\ln n}{\ln\left(1-\frac{1}{k}\right)}= \Theta (k\log n)$

**本页面主要译自博文 [Задача Иосифа](https://e-maxx.ru/algo/joseph_problem) 与其英文翻译版 [Josephus Problem](https://cp-algorithms.com/others/josephus_problem.html)．其中俄文版版权协议为 Public Domain + Leave a Link；英文版版权协议为 CC-BY-SA 4.0．**


## misc/kahan-summation.md

## 引入

**Kahan 求和** 算法，又名补偿求和或进位求和算法，是一个用来 **降低有限精度浮点数序列累加值误差** 的算法．它主要通过保持一个单独变量用来累积误差（常用变量名为 $c$）来完成的．

该算法主要由 William Kahan 于 1960s 发现．因为 Ivo Babuška 也曾独立提出了一个类似的算法，Kahan 求和算法又名为 Kahan–Babuška 求和算法．

## 舍入误差

在计算机程序中，我们需要用有限位数对实数做近似表示，如今的大多数计算机都使用 [IEEE-754](https://en.wikipedia.org/wiki/IEEE_754) 规定的浮点数来作为这个近似表示．对于 $\frac{1}{3}$，由于我们不能在有限位数内对它进行精准表示，因此在使用 IEEE-754 表示法时，必须四舍五入一部分数值（truncate）．这种 **舍入误差**（Rounding off error）是浮点计算的一个特征．

在浮点加法计算中，交换律（commutativity）成立，但结合律（associativity）不成立．也就是说，$a+b = b+a$ 但 $(a+b)+c \neq a+(b+c)$．因此在浮点序列加法计算中，我们可以从左到右一个个累加，也可以在原有顺序上，将他们两两分成一对．第二种算法会相对较慢并需要更多内存，也常被一些语言的特定求和函数使用，但相对结果更准确．

为了得到更准确的浮点累加结果，我们需要使用 Kahan 求和算法．

在计算 $S_{new}=S_{old}+a$（$a$ 为浮点序列的一个数值）时，定义实际计算加入 $S$ 的值为 $a_{eff}=S_{new}-S_{old}$, 如果 $a_{eff}$ 比 $a$ 大，则证明有向上舍入误差；如果 $a_{eff}$ 比 $a$ 小，则证明有向下舍入误差．则舍入误差定义为 $E_{roundoff} = a_{eff} - a$．那么用来纠正这部分舍入误差的值就为 $a-a_{eff}$, 即 $E_{roundoff}$ 的负值．定义 $c$ 是对丢失的低位进行运算补偿的变量，就可以得到 $c_{new} = c_{old} + (a - a_{eff})$．

## 过程

Kahan 求和算法主要通过一个单独变量用来累积误差．如下方参考代码所示，$sum$ 为最终返回的累加结果．$c$ 是对丢失的低位进行运算补偿的变量（其被舍去的部分），也是 Kahan 求和算法中的必要变量．

因为 $sum$ 大，$y$ 小，所以 $y$ 的低位数丢失．$(t - sum)$ 抵消了 $y$ 的高阶部分，减去 $y$ 则会恢复负值（$y$ 的低价部分）．因此代数值中 $c$ 始终为零．在下一轮迭代中，丢失的低位部分会被更新添加到 $y$．

## 实现

??? note "参考代码"
    ```cpp
    float kahanSum(vector<float> nums) {
      float sum = 0.0f;
      float c = 0.0f;
      for (auto num : nums) {
        float y = num - c;
        float t = sum + y;
        c = (t - sum) - y;
        sum = t;
      }
      return sum;
    }
    ```

## 习题

在 OI 中，Kahan 求和主要作为辅助工具存在，为计算结果提供误差更小的值．

???+ note "例题 [CodeForces Contest 800 Problem A. Voltage Keepsake](https://codeforces.com/contest/800/problem/A)"
    有 $n$ 个同时使用的设备．第 $i$ 个设备每秒使用 $a_{i}$ 单位的功率．这种用法是连续的．也就是说，在 $\lambda$ 秒内，设备将使用 $\lambda \times a_{i}$ 单位的功率．第 $i$ 个设备当前存储了 $b_{i}$ 单位的电力．所有设备都可以存储任意数量的电量．有一个可以插入任何单个设备的充电器．充电器每秒会为设备增加 $p$ 个单位的电量．这种充电是连续的．也就是说，如果将设备插入 $\lambda$ 秒，它将获得 $\lambda \times p$ 单位的功率．我们可以在任意时间单位内（包括实数）切换哪个设备正在充电（切换所需时间忽略不计）．求其中一个设备达到 $0$ 单位功率前，可以使用这些设备的最长时间．

???+ note "例题 [CodeForces Contest 504 Problem B. Misha and Permutations Summation](https://codeforces.com/problemset/problem/504/B)"
    定义数字 $0, 1, \cdots, (n - 1)$ 的两个排列 $p$ 和 $q$ 的和为 $Perm((Ord(p)+Ord(q))\bmod n!)$，其中 $Perm(x)$ 是数字 $0, 1, \cdots, (n-1)$ 的第 $x$ 个字典排列（从零开始计数），$Ord(p)$ 是字典序排列 $p$ 的个数．例如，$Perm(0) = (0, 1, \cdots , n - 2, n - 1)$，$Perm(n! - 1) = (n - 1, n-2,\cdots, 1,0))$．Misha 有两个排列 $p$ 和 $q$，找到它们的总和．

## 编程语言的求和

Python 的标准库指定了精确舍入求和的 [fsum](https://docs.python.org/3/library/math.html#math.fsum) 函数可用于返回可迭代对象中值的准确浮点总和，它通过使用 Shewchuk 算法跟踪多个中间部分和来避免精度损失．

Julia 语言中，[sum](https://docs.julialang.org/en/v1/base/collections/#Base.sum) 函数的默认实现是成对求和，以获得高精度和良好的性能．同时外部库函数 [sum\_kbn](http://www.jlhub.com/julia/manual/en/function/sum_kbn) 为需要更高精度的情况提供了 Neumaier 变体的实现，具体可见 [KahanSummation.jl](https://github.com/JuliaMath/KahanSummation.jl)．

## 参考资料与注释

1.  [Kahan\_summation\_algorithm - Wikipedia](https://en.wikipedia.org/wiki/Kahan_summation_algorithm)
2.  [Kahan summation - Rosetta Code](https://rosettacode.org/wiki/Kahan_summation)
3.  [VK Cup Round 2 + Codeforces Round 409 Announcement](https://codeforces.com/blog/entry/51577)
4.  [Rounding off errors in Java - GeeksforGeeks](https://www.geeksforgeeks.org/rounding-off-errors-java/)


## misc/main-element.md

author: SDLTF, Ethkuil

## 问题介绍

给一个有 $n$ 个元素的序列，保证有一个元素 $a$ 出现的次数 **严格大于**  $n/2$，求这个元素．

## 做法

### 离线算法

若一开始就可以知道整个序列，一个自然的思路是统计序列中各元素的出现次数，出现次数大于 $n/2$ 的就是主元素．可以创建一个桶来统计每种元素的出现次数，输出出现次数大于 $n/2$ 的元素即可．

但上述方案引入了桶进行统计，空间效率并不优．显然，若序列存在主元素，那么在排序后，序列的第 $\lfloor n/2\rfloor+1$ 个元素一定是主元素，利用 [`nth_element`](https://en.cppreference.com/w/cpp/algorithm/nth_element.html) 就可以找到这个元素．这样我们就在不引入额外空间的情况下，以线性时间复杂度求得主元素了．

### 在线算法

在一些情况下，我们需要在线处理流式数据，此时我们需要一种不需要预知全体数据，而是只利用当前给出的数据逐步求得答案的算法．**多数投票算法** [^ref1]就是一种可以在线解决主元素问题的算法．

由于主元素的出现的次数超过 $n/2$，那么对于一个完整的序列，在不断消掉一个主元素和一个与主元素不同的元素之后，最后一定剩下主元素．借助这个观察，我们可以设计一个在线算法进行这样的消除操作．设 `val` 和 `cnt` 两个变量分别代表当前的主元素候选和目前如果进行了这样的消除操作后主元素候选会剩多少个．初始时 `cnt` 置为 $0$．每次从数据流中取出一个元素，如果当前 `cnt` 为 $0$，则代表主元素候选已经被消除完了，当前记录的 `val` 一定不是主元素，因此设置当前元素为主元素候补．之后检查当前元素是否是主元素候补，如果是，则 `cnt` 增加 $1$，如果不是，则该元素应与一个主元素候补一起消除，`cnt` 减少 $1$．重复上述操作直到数据流读取完成，`val` 即为主元素．

???+ warning "注意"
    当原数据中不存在主元素时，此算法给出的结果是错误的．如要判断序列中是否存在主元素，需要再次读入数据流，统计 `val` 出现次数，判断其是否超过 $n/2$．
    
    为了再次读入数据流，可以选择重置输入位置指示器，可利用 [`std::basic_istream<CharT,Traits>::seekg`](https://en.cppreference.com/w/cpp/io/basic_istream/seekg)（流式输入）或 [`rewind`](https://en.cppreference.com/w/c/io/rewind)、[`fseek`](https://en.cppreference.com/w/c/io/fseek)（C 风格输入）等库函数．

## 例题

???+ example "[洛谷 P2397 yyy loves Maths VI (mode)](https://www.luogu.com.cn/problem/P2397)"
    求给定序列的主元素．

??? note "参考代码"
    ```cpp
    --8<-- "docs/misc/code/main-element/main-element_1.cpp"
    ```

???+ example "[LeetCode 229. 多数元素 II](https://leetcode.cn/problems/majority-element-ii)"
    给定一个大小为 $n$ 的整数数组，找出其中所有出现超过 $\lfloor n/3\rfloor$ 次的元素．

??? note "参考代码"
    ```cpp
    --8<-- "docs/misc/code/main-element/main-element_2.cpp:core"
    ```

## 参考资料

[^ref1]: [多数投票算法 - 维基百科](https://zh.wikipedia.org/zh-cn/%E5%A4%9A%E6%95%B0%E6%8A%95%E7%A5%A8%E7%AE%97%E6%B3%95)


## misc/mo-algo-2dimen.md

二维莫队，顾名思义就是每个状态有四个方向可以扩展．

二维莫队每次移动指针要操作一行或者一列的数，具体实现方式与普通的一维莫队类似，这里不再赘述．这里重点讲块长选定部分．

## 块长选定

记询问次数为 $q$，当前矩阵的左上角坐标为 $(x_1,\ y_1)$，右下角坐标为 $(x_2,\ y_2)$，取块长为 $B$．

那么指针 $x_1$ 移动了 $\Theta(q\cdot B)$ 次，而指针 $y_2$ 移动了 $\Theta(n^4\cdot B^{-3})$ 次．

所以只需令 $q\cdot B=n^4\cdot B^{-3}$，即 $B=n\cdot q^{-\frac 14}$ 即可．

注意这样计算 $B$ 的结果 **可能为 $0$**，**注意特判**．

最终，计算部分时间复杂度是 $\Theta(n^2\cdot q^{\frac 34})$，加上对询问的排序过程，总时间复杂度为 $\Theta(n^2\cdot q^{\frac 34}+q\log q)$．

## 例题 1

???+ note "[BZOJ 2639 矩形计算](https://hydro.ac/p/bzoj-P2639)"
    输入一个 $n\times m$ 的矩阵，矩阵的每一个元素都是一个整数，然后有 $q$ 个询问，每次询问一个子矩阵的权值．矩阵的权值是这样定义的，对于一个整数 $x$，如果它在该矩阵中出现了 $p$ 次，那么它给该矩阵的权值就贡献 $p^2$．
    
    数据范围：$1\leq n,\ m\leq 200$，$0\leq q\leq 10^5$，$|$ 矩阵元素大小 $| \leq 2\times 10^9$．

??? note "解题思路"
    先离散化，二维莫队时用一个数组记录每个数当前出现的次数即可．

??? note "示例代码"
    ```cpp
    --8<-- "docs/misc/code/mo-algo-2dimen/mo-algo-2dimen_1.cpp"
    ```

## 例题 2

???+ note "[洛谷 P1527 \[国家集训队\] 矩阵乘法](https://www.luogu.com.cn/problem/P1527)"
    给你一个 $n\times n$ 的矩阵，$q$ 次询问，每次询问一个子矩形的第 $k$ 小数．
    
    数据范围：$1\leq n\leq 500$，$1\leq q\leq 6\times 10^4$，$0\leq a_{i,j}\leq 10^9$．

首先和上一题一样，需要离散化整个矩阵．但是需要注意，本题除了需要对数值进行分块，还需要对数值的值域进行分块，才能求出答案．

这里还需要用到奇偶化排序进行优化，具体内容请见 [普通莫队算法](../misc/mo-algo.md#普通莫队的优化)．

对于本题而言，时间限制不那么宽，注意代码常数的处理．取的块长计算值普遍较小，$n,\ q$ 都取最大值时块长大约在 $11$ 左右，可以直接设定为常数来节约代码耗时．

??? note "示例代码"
    ```cpp
    --8<-- "docs/misc/code/mo-algo-2dimen/mo-algo-2dimen_2.cpp"
    ```


## misc/mo-algo-intro.md

author: StudyingFather, Backl1ght, countercurrent-time, Ir1d, greyqz, MicDZ, ouuan

莫队算法是由莫涛提出的算法．在莫涛提出莫队算法之前，莫队算法已经在 Codeforces 的高手圈里小范围流传，但是莫涛是第一个对莫队算法进行详细归纳总结的人．莫涛提出莫队算法时，只分析了普通莫队算法，但是经过 OIer 和 ACMer 的集体智慧改造，莫队有了多种扩展版本．

莫队算法可以解决一类离线区间询问问题，适用性极为广泛．同时将其加以扩展，便能轻松处理树上路径询问以及支持修改操作．


## misc/mo-algo-on-tree.md

author: StudyingFather, Backl1ght, countercurrent-time, Ir1d, greyqz, MicDZ, ouuan, Linky, yinqf

## 括号序树上莫队

一般的莫队只能处理线性问题，我们要把树强行压成序列．

我们可以将树的括号序跑下来，把括号序分块，在括号序上跑莫队．

具体怎么做呢？

### 过程

我们通过 DFS 维护树的括号序列（进入节点 $x$ 时向序列加入 $x$，离开节点 $x$ 时再次向序列加入 $x$，序列总长为 $2N$）．

我们令 $st_x$ 为 $x$ 进入的时间，$ed_x$ 为 $x$ 离开的时间．

根据括号序列的性质，对于树上路径 $u \to v$（不妨设 $st_u \le st_v$）：

-   若 $\text{LCA}(u, v) = u$，路径上的节点恰好在区间 $[st_u, st_v]$ 中出现 1 次；不在路径上的节点出现 0 次或 2 次．
-   若 $\text{LCA}(u, v) \neq u$，路径上除 $\text{LCA}(u, v)$ 外的节点恰好在区间 $[ed_u, st_v]$ 中出现 1 次；不在路径上的节点出现 0 次或 2 次．注意特殊考虑 $\text{LCA}(u, v)$，它出现次数为 0．

因此，进行莫队时，无论遇到的节点是入栈还是出栈，其本质都是改变了该节点在当前区间的出现次数．我们只需要维护每个节点 $x$ 出现了几次，出现次数为 0 或 2 的不在当前维护的路径集合中，出现次数为 1 的在当前维护的路径集合中．因此莫队指针卡到 $[st_u, st_v]$ 时就几乎是我们树上路径 $u \to v$ 的节点集合．

实际实现中，我们可以考虑维护每个节点 $x$ 出现次数对 2 取模的结果，这个就可以指示这个节点 $x$ 有没有出现．那么我们移动指针的时候，无论是加入还是删除更新就相当于翻转这个节点 $x$ 的出现状态．

注意在处理 $\text{LCA} \neq u$ 的查询时，莫队指针移动到位后，我们需要临时手动将 $\text{LCA}(u, v)$ 加入集合（状态翻转），计算并记录该查询的答案，然后再将 $\text{LCA}(u, v)$ 移出集合（再次翻转），以保证不干扰后续指针的移动．

### 例题

???+ note "例题 [「WC2013」糖果公园](https://uoj.ac/problem/58)"
    题意：给你一棵树，树上第 $i$ 个点颜色为 $c_i$，每次询问一条路径 $u_i$,$v_i$, 求这条路径上的
    
    $\sum_{c}val_c\sum_{i=1}^{cnt_c}w_i$
    
    其中：$val$ 表示该颜色的价值，$cnt$ 表示颜色出现的次数，$w$ 表示该颜色出现 $i$ 次后的价值

#### 过程

先把树变成序列，然后每次添加/删除一个点，这个点的对答案的贡献是可以在 $O(1)$ 时间内获得的，即 $val_c\times w_{cnt_{c+1}}$

发现因为他会把起点的子树也扫了一遍，产生多余的贡献，怎么办呢？

因为扫的过程中起点的子树里的点肯定会被扫两次，但贡献为 0．

所以可以开一个 $vis$ 数组，每次扫到点 x，就把 $vis_x$ 异或上 1．

如果 $vis_x=0$，那这个点的贡献就可以不计．

所以可以用树上莫队来求．

修改的话，加上一维时间维即可，变成带修改树上莫队．

然后因为所包含的区间内可能没有 LCA，对于没有的情况要将多余的贡献删除，然后就完事了．

#### 实现

??? note "参考代码"
    ```cpp
    #include <algorithm>
    #include <cmath>
    #include <cstdio>
    using namespace std;
    
    constexpr int MAXN = 200010;
    
    int f[MAXN], g[MAXN], id[MAXN], head[MAXN], cnt, last[MAXN], dep[MAXN],
        fa[MAXN][22], v[MAXN], w[MAXN];
    int block, index, n, m, q;
    int pos[MAXN], col[MAXN], app[MAXN];
    bool vis[MAXN];
    long long ans[MAXN], cur;
    
    struct edge {
      int to, nxt;
    } e[MAXN];
    
    int cnt1 = 0, cnt2 = 0;  // 时间戳
    
    struct query {
      int l, r, t, id;
    
      bool operator<(const query &b) const {
        return (pos[l] < pos[b.l]) || (pos[l] == pos[b.l] && pos[r] < pos[b.r]) ||
               (pos[l] == pos[b.l] && pos[r] == pos[b.r] && t < b.t);
      }
    } a[MAXN], b[MAXN];
    
    void addedge(int x, int y) {
      e[++cnt] = edge{y, head[x]};
      head[x] = cnt;
    }
    
    void dfs(int x) {
      id[f[x] = ++index] = x;
      for (int i = head[x]; i; i = e[i].nxt) {
        if (e[i].to != fa[x][0]) {
          fa[e[i].to][0] = x;
          dep[e[i].to] = dep[x] + 1;
          dfs(e[i].to);
        }
      }
      id[g[x] = ++index] = x;  // 括号序
    }
    
    int lca(int x, int y) {
      if (dep[x] < dep[y]) swap(x, y);
      if (dep[x] != dep[y]) {  // 爬到同一高度
        int dis = dep[x] - dep[y];
        for (int i = 20; i >= 0; i--)
          if (dis >= (1 << i)) dis -= 1 << i, x = fa[x][i];
      }
      if (x == y) return x;
      for (int i = 20; i >= 0; i--) {
        if (fa[x][i] != fa[y][i]) x = fa[x][i], y = fa[y][i];
      }
      return fa[x][0];
    }
    
    void add(int x) {
      if (vis[x])
        cur -= (long long)v[col[x]] * w[app[col[x]]--];
      else
        cur += (long long)v[col[x]] * w[++app[col[x]]];
      vis[x] ^= 1;
    }
    
    // 在时间维上移动
    void modify(int x, int t) {
      if (vis[x]) {
        add(x);
        col[x] = t;
        add(x);
      } else
        col[x] = t;
    }
    
    int main() {
      scanf("%d%d%d", &n, &m, &q);
      for (int i = 1; i <= m; i++) scanf("%d", &v[i]);
      for (int i = 1; i <= n; i++) scanf("%d", &w[i]);
      for (int i = 1; i < n; i++) {
        int x, y;
        scanf("%d%d", &x, &y);
        addedge(x, y);
        addedge(y, x);
      }
      for (int i = 1; i <= n; i++) {
        scanf("%d", &last[i]);
        col[i] = last[i];
      }
      dfs(1);
      for (int j = 1; j <= 20; j++)
        for (int i = 1; i <= n; i++)
          fa[i][j] = fa[fa[i][j - 1]][j - 1];  // 预处理祖先
      int block = pow(index, 2.0 / 3);
      for (int i = 1; i <= index; i++) {
        pos[i] = (i - 1) / block;
      }
      while (q--) {
        int opt, x, y;
        scanf("%d%d%d", &opt, &x, &y);
        if (opt == 0) {
          b[++cnt2].l = x;
          b[cnt2].r = last[x];
          last[x] = b[cnt2].t = y;
        } else {
          if (f[x] > f[y]) swap(x, y);
          a[++cnt1] = query{lca(x, y) == x ? f[x] : g[x], f[y], cnt2, cnt1};
        }
      }
      sort(a + 1, a + cnt1 + 1);
      int L, R, T;  // 指针坐标
      L = R = 0;
      T = 1;
      for (int i = 1; i <= cnt1; i++) {
        while (T <= a[i].t) {
          modify(b[T].l, b[T].t);
          T++;
        }
        while (T > a[i].t) {
          modify(b[T].l, b[T].r);
          T--;
        }
        while (L > a[i].l) {
          L--;
          add(id[L]);
        }
        while (L < a[i].l) {
          add(id[L]);
          L++;
        }
        while (R > a[i].r) {
          add(id[R]);
          R--;
        }
        while (R < a[i].r) {
          R++;
          add(id[R]);
        }
        int x = id[L], y = id[R];
        int llca = lca(x, y);
        if (x != llca && y != llca) {
          add(llca);
          ans[a[i].id] = cur;
          add(llca);
        } else
          ans[a[i].id] = cur;
      }
      for (int i = 1; i <= cnt1; i++) {
        printf("%lld\n", ans[i]);
      }
      return 0;
    }
    ```

## 真·树上莫队

上面的树上莫队只是将树转化成了链，下面的才是真正的树上莫队．

由于莫队相关的问题都是模板题，因此实现部分不做太多解释

### 询问的排序

首先我们知道莫队的是基于分块的算法，所以我们需要找到一种树上的分块方法来保证时间复杂度．

条件：

-   属于同一块的节点之间的距离不超过给定块的大小
-   每个块中的节点不能太多也不能太少
-   每个节点都要属于一个块
-   编号相邻的块之间的距离不能太大

了解了这些条件后，我们看到这样一道题 [「SCOI2005」王室联邦](https://loj.ac/problem/2152)．

在这道题的基础上我们只要保证最后一个条件就可以解决分块的问题了．

??? note "思路"
    令 lim 为希望块的大小，首先，对于整个树 dfs，当子树的大小大于 lim 时，就将它们分在一块，容易想到：对于根，可能会剩下一些点，于是将这些点分在最后一个块里．

做法：用栈维护当前节点作为父节点访问它的子节点，当从栈顶到父节点的距离大于希望块的大小时，弹出这部分元素分为一块，最后剩余的一块单独作为一块．

最后的排序方法：若第一维时间戳大于第二维，交换它们，按第一维所属块为第一关键字，第二维时间戳为第二关键字排序．

### 指针的移动

#### 过程

容易想到，我们可以标记被计入答案的点，让指针直接向目标移动，同时取反路径上的点．

但是，这样有一个问题，若指针一开始都在 x 上，显然 x 被标记，当两个指针向同一子节点移动（还有许多情况）时，x 应该不被标记，但实际情况是 x 被标记，因为两个指针分别标记了一次，抵消了．

如何解决呢？

有一个很显然的性质：这些点肯定是某些 LCA，因为 LCA 处才有可能被重复撤销导致撤销失败．

所以我们每次不标记 LCA，到需要询问答案时再将 LCA 标记，然后再撤销．

#### 实现

```cpp
// 取反路径上除LCA以外的所有节点
void move(int x, int y) {
  if (dp[x] < dp[y]) swap(x, y);
  while (dp[x] > dp[y]) update(x), x = fa[x];
  while (x != y) update(x), update(y), x = fa[x], y = fa[y];
  // x!=y保证LCA没被取反
}
```

对于求 LCA，我们可以用树剖，然后我们就可以把分块的步骤放到树剖的第一次 dfs 里面，时间戳也可以直接用第二次 dfs 的 dfs 序．

```cpp
int bl[100002], bls = 0;  // 属于的块，块的数量
unsigned step;            // 块大小
int fa[100002], dp[100002], hs[100002] = {0}, sz[100002] = {0};
// 父节点，深度，重儿子，大小
stack<int> sta;

void dfs1(int x) {
  sz[x] = 1;
  unsigned ss = sta.size();
  for (int i = head[x]; i; i = nxt[i])
    if (ver[i] != fa[x]) {
      fa[ver[i]] = x;
      dp[ver[i]] = dp[x] + 1;
      dfs1(ver[i]);
      sz[x] += sz[ver[i]];
      if (sz[ver[i]] > sz[hs[x]]) hs[x] = ver[i];
      if (sta.size() - ss >= step) {
        bls++;
        while (sta.size() != ss) bl[sta.top()] = bls, sta.pop();
      }
    }
  sta.push(x);
}

// main
if (!sta.empty()) {
  bls++;  // 这一行可写可不写
  while (!sta.empty()) bl[sta.top()] = bls, sta.pop();
}
```

### 时间复杂度

重点到了，这里关系到块的大小取值．

设块的大小为 $unit$：

-   对于 x 指针，由于每个块中节点的距离在 $unit$ 左右，每个块中 x 指针移动 $unit^2$ 次（$unit\times dis_{\max}$），共计 $n\times unit$ 次（$unit^2 \times (\frac{n}{unit})$）；
-   对于 y 指针，每个块中最多移动 $O(n)$ 次，共计 $\frac{n^2}{unit}$ 次（$n \times (\frac{n}{unit})$）．

加起来大概在根号处取得最小值（由于树上莫队块的大小不固定，所以不一定要严格按照）．

### 例题「WC2013」糖果公园

由于多了时间维，块的大小取到 $n^{0.6}$ 的样子就差不多了．

??? note "参考代码"
    ```cpp
    #include <algorithm>
    #include <cmath>
    #include <cstdio>
    #include <stack>
    using namespace std;
    
    int gi() {
      int x, c, op = 1;
      while (c = getchar(), c < '0' || c > '9')
        if (c == '-') op = -op;
      x = c ^ 48;
      while (c = getchar(), c >= '0' && c <= '9')
        x = (x << 3) + (x << 1) + (c ^ 48);
      return x * op;
    }
    
    int head[100002], nxt[200004], ver[200004], tot = 0;
    
    void add(int x, int y) {
      ver[++tot] = y, nxt[tot] = head[x], head[x] = tot;
      ver[++tot] = x, nxt[tot] = head[y], head[y] = tot;
    }
    
    int bl[100002], bls = 0;
    unsigned step;
    int fa[100002], dp[100002], hs[100002] = {0}, sz[100002] = {0}, top[100002],
                                id[100002];
    stack<int> sta;
    
    void dfs1(int x) {
      sz[x] = 1;
      unsigned ss = sta.size();
      for (int i = head[x]; i; i = nxt[i])
        if (ver[i] != fa[x]) {
          fa[ver[i]] = x, dp[ver[i]] = dp[x] + 1;
          dfs1(ver[i]);
          sz[x] += sz[ver[i]];
          if (sz[ver[i]] > sz[hs[x]]) hs[x] = ver[i];
          if (sta.size() - ss >= step) {
            bls++;
            while (sta.size() != ss) bl[sta.top()] = bls, sta.pop();
          }
        }
      sta.push(x);
    }
    
    int cnt = 0;
    
    void dfs2(int x, int hf) {
      top[x] = hf, id[x] = ++cnt;
      if (!hs[x]) return;
      dfs2(hs[x], hf);
      for (int i = head[x]; i; i = nxt[i])
        if (ver[i] != fa[x] && ver[i] != hs[x]) dfs2(ver[i], ver[i]);
    }
    
    int lca(int x, int y) {
      while (top[x] != top[y]) {
        if (dp[top[x]] < dp[top[y]]) swap(x, y);
        x = fa[top[x]];
      }
      return dp[x] < dp[y] ? x : y;
    }
    
    struct qu {
      int x, y, t, id;
    
      bool operator<(const qu a) const {
        return bl[x] == bl[a.x] ? (bl[y] == bl[a.y] ? t < a.t : bl[y] < bl[a.y])
                                : bl[x] < bl[a.x];
      }
    } q[100001];
    
    int qs = 0;
    
    struct ch {
      int x, y, b;
    } upd[100001];
    
    int ups = 0;
    long long ans[100001];
    int b[100001] = {0};
    int a[100001];
    long long w[100001];
    long long v[100001];
    long long now = 0;
    bool vis[100001] = {false};
    
    void back(int t) {
      if (vis[upd[t].x]) {
        now -= w[b[upd[t].y]--] * v[upd[t].y];
        now += w[++b[upd[t].b]] * v[upd[t].b];
      }
      a[upd[t].x] = upd[t].b;
    }
    
    void change(int t) {
      if (vis[upd[t].x]) {
        now -= w[b[upd[t].b]--] * v[upd[t].b];
        now += w[++b[upd[t].y]] * v[upd[t].y];
      }
      a[upd[t].x] = upd[t].y;
    }
    
    void update(int x) {
      if (vis[x])
        now -= w[b[a[x]]--] * v[a[x]];
      else
        now += w[++b[a[x]]] * v[a[x]];
      vis[x] ^= 1;
    }
    
    void move(int x, int y) {
      if (dp[x] < dp[y]) swap(x, y);
      while (dp[x] > dp[y]) update(x), x = fa[x];
      while (x != y) update(x), update(y), x = fa[x], y = fa[y];
    }
    
    int main() {
      int n = gi(), m = gi(), k = gi();
      step = (int)pow(n, 0.6);
      for (int i = 1; i <= m; i++) v[i] = gi();
      for (int i = 1; i <= n; i++) w[i] = gi();
      for (int i = 1; i < n; i++) add(gi(), gi());
      for (int i = 1; i <= n; i++) a[i] = gi();
      for (int i = 1; i <= k; i++)
        if (gi())
          q[++qs].x = gi(), q[qs].y = gi(), q[qs].t = ups, q[qs].id = qs;
        else
          upd[++ups].x = gi(), upd[ups].y = gi();
      for (int i = 1; i <= ups; i++) upd[i].b = a[upd[i].x], a[upd[i].x] = upd[i].y;
      for (int i = ups; i; i--) back(i);
      fa[1] = 1;
      dfs1(1), dfs2(1, 1);
      if (!sta.empty()) {
        bls++;
        while (!sta.empty()) bl[sta.top()] = bls, sta.pop();
      }
      for (int i = 1; i <= n; i++)
        if (id[q[i].x] > id[q[i].y]) swap(q[i].x, q[i].y);
      sort(q + 1, q + qs + 1);
      int x = 1, y = 1, t = 0;
      for (int i = 1; i <= qs; i++) {
        if (x != q[i].x) move(x, q[i].x), x = q[i].x;
        if (y != q[i].y) move(y, q[i].y), y = q[i].y;
        int f = lca(x, y);
        update(f);
        while (t < q[i].t) change(++t);
        while (t > q[i].t) back(t--);
        ans[q[i].id] = now;
        update(f);
      }
      for (int i = 1; i <= qs; i++) printf("%lld\n", ans[i]);
      return 0;
    }
    ```


## misc/mo-algo-secondary-offline.md

author: Lyccrius, AtomAlpaca

## 综述

有时我们会遇见一些题目，这些题目看起来很适合使用莫队算法处理，但是他们的单次转移并非是 $O(1)$ 的，这时直接使用莫队即使调整块长，也会导致复杂度不正确．

此时，如果每次转移对答案的贡献可以进行差分，我们就可以将这些转移拆开离线下来，使用其它算法批量处理．

我们用 $f(x, l, r)$ 表示 $x$ 关于 $[l, r]$ 产生的贡献．

如我们在将当前区间 $[l, r]$ 扩展到 $[l, r + 1]$ 时，我们要求的是 $f(a_{r + 1}, l, r)$．如果可以差分，我们可以将其写成 $f(a_{r + 1}, 1, r) - f(a_{r + 1}, 1, l - 1)$，其中第一项我们可以对于每个 $r$ 都预处理出来，后一项我们可以把每个这样的项都离线存到对应的 $l - 1$ 上，然后从小到大枚举并扫描线处理．其它几个转移的方向也都可以类似地处理．

这一在莫队这个离线算法上，将转移再次离线处理的算法叫做莫队二次离线．

我们结合实际题目来理解．

## 例题

???+ note "[Luogu P5047 \[Ynoi2019 模拟赛\] Yuno loves sqrt technology II](https://www.luogu.com.cn/problem/P5047)"
    给你一个长为 $n$ 的序列 $a$，$m$ 次询问，每次查询一个区间的逆序对数．
    
    数据范围：$1 \leq n,m \leq 10^5$，$0 \leq a_i \leq 10^9$．

直接莫队每次转移至少是 $O(\log n)$ 的，观察可以发现我们每次转移要求的信息是「一个数在某个区间内的排名」，而这一信息关于区间可以差分，因此考虑二次离线．

我们将 $[l, r]$ 拓展到 $[l, r + 1]$，要求的是 在 $[l, r]$ 区间内有多少比 $a_{r + 1}$ 大的数．
我们用 $f(x, r)$ 表示 $[1, r]$ 区间内比 $a_x$ 大的数，$g(x, r)$ 表示 $[1, r]$ 区间内比 $a_x$ 小的数．则答案的变化量可以写作 $f(r + 1, r) - f(r + 1, l - 1)$．

同理 $[l, r]$ 缩小至 $[l, r - 1]$ 的变化量可以写作 $-f(r, r - 1) + f(r, l - 1)$；$[l, r]$ 拓展到 $[l - 1, r]$ 可以写作 $g(l - 1, r) - g(l - 1, l - 2)$,$[l, r]$ 缩小至 $[l + 1, r]$ 可以写作 $- g(l, r) + g(l, l - 1)$．

对于这些式子中的 $f(x, x - 1)$ 和 $g(x, x - 1)$，我们可以使用树状数组提前 $O(n \log n)$ 预处理出来；对于其余的 $f(x, p)$ 和 $g(x, p)$ 项，我们将 $x$ 离线存在 $l$ 进行批量处理．

这里有一个优化空间的技巧：我们发现处理每个询问时，离线到 $p$ 上的 $x$ 都是连续的一段，因此我们不需要把每次移动都存下，只需要存下调整的一段即可．这样我们的空间可以从总次数 $O(n\sqrt{m})$ 下降到询问数 $O(m)$．

现在我们来处理我们二次离线下来的问题：向一个集合中加入数，查询一个数在集合中的排名．莫队总共移动端点的次数是 $O(n\sqrt{m})$ 的，而数组总共只有 $O(n)$ 的长度，因此我们考虑使用 $O(\sqrt{n})$ 插入、$O(1)$ 查询的值域分块解决这个问题．

至此，我们在 $O(n \sqrt{m} + n \sqrt{n})$ 的时间复杂度和 $O(n + m)$ 的空间复杂度下解决了此题．

最后值得注意的是，我们求得的是每次的答案变化量而非答案本身，需要对其进行前缀和才能得到最终的答案．

??? note "示例代码"
    ```cpp
    --8<-- "docs/misc/code/mo-algo-secondary-offline/mo-algo-secondary-offline_1.cpp"
    ```

???+ note "[Luogu P5501 \[LnOI2019\] 来者不拒，去者不追](https://www.luogu.com.cn/problem/P5501)"
    多次询问区间中 $[l, r]$ 中所有数的「Abbi 值」之和．
    
    Abbi 值定义为：若 $a_i$ 在询问区间 $[l,r]$ 中是第 $k$ 小，那么它的「Abbi 值」等于 $ka_i$．

我们不妨令 $f(x,r)$ 是 $[1,r]$ 中比 $a_x$ 大的数之和，$g(x,r)$ 是 $[1,r]$ 中比 $a_x$ 大的数的数量，那么我们向右移动右端点时，产生的贡献为 $f(r,r-1)-f(r,l-1) + a_r(r-l+ 1-(g(r,r-1)-g(r,l-1)))$，其它几个方向可同理写出，在此不加赘述．

上式中的 $f(r, r - 1)$ 和 $g(r, r - 1)$ 依旧可以进行预处理，其余的离线到另一端点上，进行扫描线处理．不难发现我们要处理的依然是 $O(n)$ 次插入、$O(n\sqrt{m})$ 次询问排名的问题，因此同样使用值域分块解决．

??? note "示例代码"
    ```cpp
    --8<-- "docs/misc/code/mo-algo-secondary-offline/mo-algo-secondary-offline_2.cpp"
    ```


## misc/mo-algo-with-bitset.md

author: StudyingFather, Backl1ght, countercurrent-time, Ir1d, greyqz, MicDZ, ouuan

bitset 常用于常规数据结构难以维护的判定、统计问题，而莫队可以维护常规数据结构难以维护的区间信息．把两者结合起来使用可以同时利用两者的优势．

## 例题 [「Ynoi2016」掉进兔子洞](https://www.luogu.com.cn/problem/P4688)

本题刚好符合上面提到的莫队配合 bitset 的特征．不难想到我们可以分别用 bitset 存储每一个区间内的出现过的所有权值，一组询问的答案即所有区间的长度和减去三者的并集元素个数 $\times 3$．

但是在莫队中使用 bitset 也需要针对 bitset 的特性调整算法：

1.  bitset 不能很好地处理同时出现多个权值的情况．我们可以把当前元素离散化后的权值与当前区间的出现次数之和作为往 bitset 中插入的对象．
2.  我们平常使用莫队时，可能会不注意 4 种移动指针的方法顺序，所以指针移动的过程中可能会出现区间的左端点在右端点右边，区间长度为负值的情况，导致元素的个数为负数．这在其他情况下并没有什么影响，但是本题中在 bitset 中插入的元素与元素个数有关，所以我们需要注意 4 种移动指针的方法顺序，将左右指针分别往左边和右边移动的语句写在前面，避免往 bitset 中插入负数．
3.  虽然 bitset 用空间小，但是仍然难以承受 $10 ^ 5 \times 10 ^ 5$ 的数据规模．所以我们需要将询问划分成常数块分别处理，保证空间刚好足够的情况下时间复杂度不变．

??? note "参考代码"
    ```cpp
    --8<-- "docs/misc/code/mo-algo-with-bitset/mo-algo-with-bitset_1.cpp"
    ```

## 习题

-   [小清新人渣的本愿](https://www.luogu.com.cn/problem/P3674)
-   [「Ynoi2017」由乃的玉米田](https://www.luogu.com.cn/problem/P5355)
-   [「Ynoi2011」WBLT](https://www.luogu.com.cn/problem/P5313)


## misc/mo-algo.md

author: StudyingFather, Backl1ght, countercurrent-time, Ir1d, greyqz, MicDZ, ouuan

## 形式

假设 $n=m$，那么对于序列上的区间询问问题，如果从 $[l,r]$ 的答案能够 $O(1)$ 扩展到 $[l-1,r],[l+1,r],[l,r+1],[l,r-1]$（即与 $[l,r]$ 相邻的区间）的答案，那么可以在 $O(n\sqrt{n})$ 的复杂度内求出所有询问的答案．

## 解释

离线后排序，顺序处理每个询问，暴力从上一个区间的答案转移到下一个区间答案（一步一步移动即可）．

## 排序方法

对于区间 $[l,r]$, 以 $l$ 所在块的编号为第一关键字，$r$ 为第二关键字从小到大排序．

## 实现

```cpp
void move(int pos, int sign) {
  // update nowAns
}

void solve() {
  BLOCK_SIZE = int(ceil(pow(n, 0.5)));
  sort(querys, querys + m);
  for (int i = 0; i < m; ++i) {
    const query &q = querys[i];
    while (l > q.l) move(--l, 1);
    while (r < q.r) move(++r, 1);
    while (l < q.l) move(l++, -1);
    while (r > q.r) move(r--, -1);
    ans[q.id] = nowAns;
  }
}
```

## 复杂度分析

以下的情况在 $n$ 和 $m$ 同阶的前提下讨论．

首先是分块这一步，这一步的时间复杂度是 $O(\sqrt{n}\cdot\sqrt{n}\log\sqrt{n}+n\log n)=O(n\log n)$．

接着就到了莫队算法的精髓了，下面我们用通俗易懂的初中方法来证明它的时间复杂度是 $O(n\sqrt{n})$．

???+ note "证明"
    证：令每一块中 $L$ 的最大值为 $\max_1,\max_2,\max_3, \cdots , \max_{\lceil\sqrt{n}\rceil}$．
    
    由第一次排序可知，$\max_1 \le \max_2 \le \cdots \le \max_{\lceil\sqrt{n}\rceil}$．
    
    显然，对于每一块暴力求出第一个询问的时间复杂度为 $O(n)$．
    
    考虑最坏的情况，在每一块中，$R$ 的最大值均为 $n$，每次修改操作均要将 $L$ 由 $\max_{i - 1}$ 修改至 $\max_i$ 或由 $\max_i$ 修改至 $\max_{i - 1}$．
    
    考虑 $R$：因为 $R$ 在块中已经排好序，所以在同一块修改完它的时间复杂度为 $O(n)$．对于所有块就是 $O(n\sqrt{n})$．
    
    重点分析 $L$：因为每一次改变的时间复杂度都是 $O(\max_i-\max_{i-1})$ 的，所以在同一块中时间复杂度为 $O(\sqrt{n}\cdot(\max_i-\max_{i-1}))$．
    
    将每一块 $L$ 的时间复杂度合在一起，可以得到：
    
    对于 $L$ 的总时间复杂度为
    
    $$
    \begin{aligned}
    & O(\sqrt{n}(\max{}_1-1)+\sqrt{n}(\max{}_2-\max{}_1)+\sqrt{n}(\max{}_3-\max{}_2)+\cdots+\sqrt{n}(\max{}_{\lceil\sqrt{n}\rceil}-\max{}_{\lceil\sqrt{n}\rceil-1))} \\
    = \phantom{} & O(\sqrt{n}\cdot(\max{}_1-1+\max{}_2-\max{}_1+\max{}_3-\max{}_2+\cdots+\max{}_{\lceil\sqrt{n}\rceil-1}-\max{}_{\lceil\sqrt{n}\rceil-2}+\max{}_{\lceil\sqrt{n}\rceil}-\max{}_{\lceil\sqrt{n}\rceil-1)}) \\
    = \phantom{} & O(\sqrt{n}\cdot(\max{}_{\lceil\sqrt{n}\rceil}-1))\\
    \end{aligned}
    $$
    
    （裂项求和）
    
    由题可知 $\max_{\lceil\sqrt{n}\rceil}$ 最大为 $n$，所以 $L$ 的总时间复杂度最坏情况下为 $O(n\sqrt{n})$．

综上所述，莫队算法的时间复杂度为 $O(n\sqrt{n})$．

但是对于 $m$ 的其他取值，如 $m<n$，分块方式需要改变才能变的更优．

怎么分块呢？

我们设块长度为 $S$，那么对于任意多个在同一块内的询问，挪动的距离就是 $n$，一共 $\displaystyle \frac{n}{S}$ 个块，移动的总次数就是 $\displaystyle \frac{n^2}{S}$，移动可能跨越块，所以还要加上一个 $mS$ 的复杂度，总复杂度为 $\displaystyle O\left(\frac{n^2}{S}+mS\right)$，我们要让这个值尽量小，那么就要将这两个项尽量相等，发现 $S$ 取 $\displaystyle \frac{n}{\sqrt{m}}$ 是最优的，此时复杂度为 $\displaystyle O\left(\frac{n^2}{\displaystyle \frac{n}{\sqrt{m}}}+m\left(\frac{n}{\sqrt{m}}\right)\right)=O(n\sqrt{m})$．

事实上，如果块长度的设定不准确，则莫队的时间复杂度会受到很大影响．例如，如果 $m$ 与 $\sqrt n$ 同阶，并且块长误设为 $\sqrt n$，则可以很容易构造出一组数据使其时间复杂度为 $O(n \sqrt n)$ 而不是正确的 $O(n^{5/4})$．

莫队算法看起来十分暴力，很大程度上是因为莫队算法的分块排序方法看起来很粗糙．我们会想到通过看上去更精细的排序方法对所有区间排序．一种方法是把所有区间 $[l, r]$ 看成平面上的点 $(l, r)$，并对所有点建立曼哈顿最小生成树，每次沿着曼哈顿最小生成树的边在询问之间转移答案．这样看起来可以改善莫队算法的时间复杂度，但是实际上对询问分块排序的方法的时间复杂度上界已经是最优的了．

假设 $n, m$ 同阶且 $n$ 是完全平方数．我们考虑形如 $[a \sqrt n, b \sqrt n](1 \le a, b \le \sqrt n)$ 的区间，这样的区间一共有 $n$ 个．如果把所有的区间看成平面上的点，则两点之间的曼哈顿距离恰好为两区间的转移代价，并且任意两个区间之间的最小曼哈顿距离为 $\sqrt n$，所以处理所有询问的时间复杂度最小为 $O(n \sqrt n)$．其它情况的数据构造方法与之类似．

莫队算法还有一个特点：当 $n$ 不变时，$m$ 越大，处理每次询问的平均转移代价就越小．一些其他的离线算法也具有同样的特点（如求 LCA 的 Tarjan 算法），但是莫队算法的平均转移代价随 $m$ 的变化最明显．

## 例题 & 代码

???+ note "例题 [「国家集训队」小 Z 的袜子](https://www.luogu.com.cn/problem/P1494)"
    题目大意：
    
    有一个长度为 $n$ 的序列 $\{c_i\}$．现在给出 $m$ 个询问，每次给出两个数 $l,r$，从编号在 $l$ 到 $r$ 之间的数中随机选出两个不同的数，求两个数相等的概率．

### 过程

思路：莫队算法模板题．

对于区间 $[l,r]$，以 $l$ 所在块的编号为第一关键字，$r$ 为第二关键字从小到大排序．

然后从序列的第一个询问开始计算答案，第一个询问通过直接暴力算出，复杂度为 $O(n)$，后面的询问在前一个询问的基础上得到答案．

具体做法：

对于区间 $[i,i]$，由于区间只有一个元素，我们很容易就能知道答案．然后一步一步从当前区间（已知答案）向下一个区间靠近．

我们设 $col[i]$ 表示当前颜色 $i$ 出现了多少次，$ans$ 表示当前共有多少种可行的配对方案（有多少种可以选到一双颜色相同的袜子）．然后每次移动的时候更新答案：设当前颜色为 $k$，如果是增长区间就是 $ans$ 加上 $\dbinom{col[k]+1}{2}-\dbinom{col[k]}{2}$；如果是缩短就是 $ans$ 减去 $\dbinom{col[k]}{2}-\dbinom{col[k]-1}{2}$．这个询问的答案就是 $\displaystyle \frac{ans}{\dbinom{r-l+1}{2}}$．

这里有个优化：$\displaystyle \dbinom{a}{2}=\frac{a (a-1)}{2}$．

所以 $\displaystyle \dbinom{a+1}{2}-\dbinom{a}{2}=\frac{(a+1) a}{2}-\frac{a (a-1)}{2}=\frac{a}{2}\cdot (a+1-a+1)=\frac{a}{2}\cdot 2=a$．

所以 $\dbinom{col[k]+1}{2}-\dbinom{col[k]}{2}=col[k]$．

算法总复杂度：$O(n\sqrt{n} )$

下面的代码中 `deno` 表示答案的分母 (denominator)，`nume` 表示分子 (numerator)，`sqn` 表示块的大小：$\sqrt{n}$，`arr` 是输入的数组，`node` 是存储询问的结构体，`tab` 是询问序列（排序后的），`col` 同上所述．

**注意：由于 `++l` 和 `--r` 的存在，下面代码中的移动区间的 4 个 while 循环的位置很关键，不能随意改变它们之间的位置关系．**

??? note "关于四个循环位置的讨论"
    莫队区间的移动过程，就相当于加入了 $[1,r]$ 的元素，并删除了 $[1,l-1]$ 的元素．因此，
    
    -   对于 $l\le r$ 的情况，$[1,l-1]$ 的元素相当于被加入了一次又被删除了一次，$[l,r]$ 的元素被加入一次，$[r+1,+\infty)$ 的元素没有被加入．这个区间是合法区间．
    -   对于 $l=r+1$ 的情况，$[1,r]$ 的元素相当于被加入了一次又被删除了一次，$[r+1,+\infty)$ 的元素没有被加入．这时这个区间表示空区间．
    -   对于 $l>r+1$ 的情况，那么 $[r+1,l-1]$（这个区间非空）的元素被删除了一次但没有被加入，因此这个元素被加入的次数是负数．
    
    因此，如果某时刻出现 $l>r+1$ 的情况，那么会存在一个元素，它的加入次数是负数．这在某些题目会出现问题，例如我们如果用一个 `set` 维护区间中的所有数，就会出现「需要删除 `set` 中不存在的元素」的问题．
    
    代码中的四个 while 循环一共有 $4!=24$ 种排列顺序．不妨设第一个循环用于操作左端点，就有以下 $12$ 种排列（另外 $12$ 种是对称的）．下表列出了这 12 种写法的正确性，还给出了错误写法的反例．
    
    | 循环顺序              | 正确性 | 反例或注释       |
    | ----------------- | --- | ----------- |
    | `l--,l++,r--,r++` | 错误  | $l<r<l'<r'$ |
    | `l--,l++,r++,r--` | 错误  | $l<r<l'<r'$ |
    | `l--,r--,l++,r++` | 错误  | $l<r<l'<r'$ |
    | `l--,r--,r++,l++` | 正确  | 证明较繁琐       |
    | `l--,r++,l++,r--` | 正确  |             |
    | `l--,r++,r--,l++` | 正确  |             |
    | `l++,l--,r--,r++` | 错误  | $l<r<l'<r'$ |
    | `l++,l--,r++,r--` | 错误  | $l<r<l'<r'$ |
    | `l++,r++,l--,r--` | 错误  | $l<r<l'<r'$ |
    | `l++,r++,r--,l--` | 错误  | $l<r<l'<r'$ |
    | `l++,r--,l--,r++` | 错误  | $l<r<l'<r'$ |
    | `l++,r--,r++,l--` | 错误  | $l<r<l'<r'$ |
    
    全部 24 种排列中只有 6 种是正确的，其中有 2 种的证明较繁琐，这里只给出其中 4 种的证明．
    
    这 4 种正确写法的共同特点是，前两步先扩大区间（`l--` 或 `r++`），后两步再缩小区间（`l++` 或 `r--`）．这样写，前两步是扩大区间，可以保持 $l\le r+1$；执行完前两步后，$l\le l'\le r'\le r$ 一定成立，再执行后两步只会把区间缩小到 $[l',r']$，依然有 $l\le r+1$，因此这样写是正确的．

### 实现

??? note "参考代码"
    ```cpp
    --8<-- "docs/misc/code/mo-algo/mo-algo_1.cpp"
    ```

## 普通莫队的优化

### 过程

我们看一下下面这组数据

```text
// 设块的大小为 2 (假设)
1 1
2 100
3 1
4 100
```

手动模拟一下可以发现，r 指针的移动次数大概为 300 次，我们处理完第一个块之后，$l = 2, r = 100$，此时只需要移动两次 l 指针就可以得到第四个询问的答案，但是我们却将 r 指针移动到 1 来获取第三个询问的答案，再移动到 100 获取第四个询问的答案，这样多了九十几次的指针移动．我们怎么优化这个地方呢？这里我们就要用到奇偶化排序．

什么是奇偶化排序？奇偶化排序即对于属于奇数块的询问，r 按从小到大排序，对于属于偶数块的排序，r 从大到小排序，这样我们的 r 指针在处理完这个奇数块的问题后，将在返回的途中处理偶数块的问题，再向 n 移动处理下一个奇数块的问题，优化了 r 指针的移动次数，一般情况下，这种优化能让程序快 30% 左右．

### 实现

排序代码：

=== "压行"
    ```cpp
    // clang-format off
    // 这里有个小细节等下会讲
    int unit; // 块的大小
    struct node {
      int l, r, id;
      bool operator < (const node &x) const {
        return l / unit == x.l / unit ? (r == x.r ? 0 : ((l / unit) & 1) ^ (r < x.r)) : l < x.l;
      }
    };
    ```

=== "不压行"
    ```cpp
    struct node {
      int l, r, id;
    
      bool operator<(const node &x) const {
        if (l / unit != x.l / unit) return l < x.l;
        // 注意下面两行不能写小于（大于）等于，否则会出错（详见下面的小细节）
        if ((l / unit) & 1) return r < x.r;
        return r > x.r;
      }
    };
    ```

???+ warning "小细节"
    如果使用 `sort` 比较两个结构体，不能出现 $a < b$ 和 $b < a$ 同时为真的情况，否则会运行错误，详见 [常见错误](../contest/common-mistakes.md#会导致-re)．

对于压行版，如果没有 `r == x.r` 的特判，当 l 属于同一奇数块且 r 相等时，会出现上面小细节中的问题（自己手动模拟一下），对于不压行版，如果写成小于（大于）等于，则也会出现同样的问题．

## 参考资料

-   [莫队算法学习笔记 | Sengxian's Blog](https://blog.sengxian.com/algorithms/mo-s-algorithm)


## misc/modifiable-mo-algo.md

author: StudyingFather, Backl1ght, countercurrent-time, Ir1d, greyqz, MicDZ, ouuan, renbaoshuo, Lixuannan

请确保您已经会普通莫队算法了．如果您还不会，请先阅读前面的 [普通莫队算法](./mo-algo.md)．

## 特点

普通莫队是不能带修改的．

我们可以强行让它可以修改，就像 DP 一样，可以强行加上一维 **时间维**, 表示这次操作的时间．

时间维表示经历的修改次数．

即把询问 $[l,r]$ 变成 $[l,r,\text{time}]$．

那么我们的坐标也可以在时间维上移动，即 $[l,r,\text{time}]$ 多了一维可以移动的方向，可以变成：

-   $[l-1,r,\text{time}]$
-   $[l+1,r,\text{time}]$
-   $[l,r-1,\text{time}]$
-   $[l,r+1,\text{time}]$
-   $[l,r,\text{time}-1]$
-   $[l,r,\text{time}+1]$

这样的转移也是 $O(1)$ 的，但是我们排序又多了一个关键字，再搞搞就行了．

可以用和普通莫队类似的方法排序转移，做到 $O(n^{5/3})$．

这一次我们排序的方式是以 $n^{2/3}$ 为一块，分成了 $n^{1/3}$ 块，第一关键字是左端点所在块，第二关键字是右端点所在块，第三关键字是时间．

???+ note "最优块长以及时间复杂度分析"
    我们设序列长为 $n$，$m$ 个询问，$t$ 个修改．
    
    带修莫队排序的第二关键字是右端点所在块编号，不同于普通莫队．
    
    想一想，如果不把右端点分块：
    
    -   乱序的右端点对于每个询问会移动 $n$ 次．
    -   有序的右端点会带来乱序的时间，每次询问会移动 $t$ 次．
    
    无论哪一种情况，带来的时间开销都无法接受．
    
    接下来分析时间复杂度．
    
    设块长为 $s$，则有 $\dfrac{n}{s}$ 个块．对于块 $i$ 和块 $j$，记有 $q_{i,j}$ 个询问的左端点位于块 $i$，右端点位于块 $j$．
    
    每「组」左右端点不换块的询问 $(i,j)$，端点每次移动 $O(s)$ 次，时间单调递增，$O(t)$．
    
    左右端点换块的时间忽略不计．
    
    表示一下就是：
    
    $$
    \begin{aligned}
    &\sum_{i=1}^{n/s}\sum_{j=i+1}^{n/s}(q_{i,j}\cdot s+t)\\
    =&ms+\left(\dfrac{n}{s}\right)^2t\\
    =&ms+\dfrac{n^2t}{s^2}
    \end{aligned}
    $$
    
    考虑求导求此式极小值．设 $f(s)=ms+\dfrac{n^2t}{s^2}$．那 $f'(s)=m-\dfrac{2n^2t}{s^3}=0$．
    
    得 $s=\sqrt[3]{\dfrac{2n^2t}{m}}=\dfrac{2^{1/3}n^{2/3}t^{1/3}}{m^{1/3}}=s_0$．
    
    也就是当块长取 $\dfrac{n^{2/3}t^{1/3}}{m^{1/3}}$ 时有最优时间复杂度 $O\left(n^{2/3}m^{2/3}t^{1/3}\right)$．
    
    常说的 $O\left(n^{5/3}\right)$ 便是把 $n,m,t$ 当做同数量级的时间复杂度．
    
    实际操作中还是推荐设定 $n^{2/3}$ 为块长．

## 例题

???+ note "例题 [「国家集训队」数颜色/维护队列](https://www.luogu.com.cn/problem/P1903)"
    题目大意：给你一个序列，M 个操作，有两种操作：
    
    1.  修改序列上某一位的数字
    2.  询问区间 $[l,r]$ 中数字的种类数（多个相同的数字只算一个）

我们不难发现，如果不带操作 1（修改）的话，我们就能轻松用普通莫队解决．

但是题目还带单点修改，所以用 **带修改的莫队**．

### 过程

先考虑普通莫队的做法：

-   每次扩大区间时，每加入一个数字，则统计它已经出现的次数，如果加入前这种数字出现次数为 $0$，则说明这是一种新的数字，答案 $+1$．然后这种数字的出现次数 $+1$．
-   每次减小区间时，每删除一个数字，则统计它删除后的出现次数，如果删除后这种数字出现次数为 $0$，则说明这种数字已经从当前的区间内删光了，也就是当前区间减少了一种颜色，答案 $-1$．然后这种数字的出现次数 $-1$．

现在再来考虑修改：

-   单点修改，把某一位的数字修改掉．假如我们是从一个经历修改次数为 $i$ 的询问转移到一个经历修改次数为 $j$ 的询问上，且 $i<j$ 的话，我们就需要把第 $i+1$ 个到第 $j$ 个修改强行加上．
-   假如 $j<i$ 的话，则需要把第 $i$ 个到第 $j+1$ 个修改强行还原．

怎么强行加上一个修改呢？假设一个修改是修改第 $pos$ 个位置上的颜色，原本 $pos$ 上的颜色为 $a$，修改后颜色为 $b$，还假设当前莫队的区间扩展到了 $[l,r]$．

-   加上这个修改：我们首先判断 $pos$ 是否在区间 $[l,r]$ 内．如果是的话，我们等于是从区间中删掉颜色 $a$，加上颜色 $b$，并且当前颜色序列的第 $pos$ 项的颜色改成 $b$．如果不在区间 $[l,r]$ 内的话，我们就直接修改当前颜色序列的第 $pos$ 项为 $b$．
-   还原这个修改：等于加上一个修改第 $pos$ 项、把颜色 $b$ 改成颜色 $a$ 的修改．

因此这道题就这样用带修改莫队轻松解决啦！

### 实现

??? note "参考代码"
    ```cpp
    --8<-- "docs/misc/code/modifiable-mo-algo/modifiable-mo-algo_1.cpp"
    ```


## misc/odt.md

## 简介

珂朵莉树（Chtholly Tree），又名老司机树 ODT（Old Driver Tree）．起源自 [CF896C](https://codeforces.com/problemset/problem/896/C)．

这个名称指代的是一种「使用平衡树（`std::set`、`std::map` 等）或链表（`std::list`、手写链表等）维护颜色段均摊」的技巧，而不是一种特定的数据结构．其核心思想是将值相同的一段区间合并成一个结点处理．相较于传统的线段树等数据结构，对于含有区间覆盖的操作的问题，珂朵莉树可以更加方便地维护每个被覆盖区间的值．

## 实现（std::set）

### 结点类型

```cpp
struct Node_t {
  int l, r;
  mutable int v;

  Node_t(const int &il, const int &ir, const int &iv) : l(il), r(ir), v(iv) {}

  bool operator<(const Node_t &o) const { return l < o.l; }
};
```

其中，`int v` 是你自己指定的附加数据．

???+ note "`mutable` 关键字的含义是什么？"
    `mutable` 的意思是「可变的」，让我们可以在后面的操作中修改 `v` 的值．在 C++ 中，mutable 是为了突破 const 的限制而设置的．被 mutable 修饰的变量（mutable 只能用于修饰类中的非静态数据成员），将永远处于可变的状态，即使在一个 const 函数中．
    
    这意味着，我们可以直接修改已经插入 `set` 的元素的 `v` 值，而不用将该元素取出后重新加入 `set`．

### 结点存储

我们希望维护所有结点，使得这些结点所代表的区间左端点单调增加且两两不交，最好可以保证所有区间的并是一个极大的连续范围．此处以 `std::set` 为例，用一个 `set<Node_t> odt;` 维护所有结点．

初始化时，向珂朵莉树中插入一个极长区间（如题目要求维护位置 $1$ 到 $n$ 的信息，插入区间 $[1,n+1]$）．

### split 操作

`split` 操作是珂朵莉树的核心．它接受一个位置 $x$，将原本包含点 $x$ 的区间（设为 $[l, r]$）分裂为两个区间 $[l, x)$ 和 $[x, r]$，并返回指向后者的迭代器．

参考代码如下：

```cpp
auto split(int x) {
  auto it = odt.lower_bound(Node_t(x, 0, 0));
  if (it != odt.end() && it->l == x) return it;
  --it;
  int l = it->l, r = it->r, v = it->v;
  odt.erase(it);
  odt.insert(Node_t(l, x - 1, v));
  return odt.insert(Node_t(x, r, v)).first;
}
```

在不支持使用 `auto` 进行返回类型推导的编译器上，可以将函数的返回类型改为 `set<Node_t>::iterator`．

### assign 操作

另外一个重要的操作：`assign`．用于对一段区间进行赋值．设将要对区间 $[l,r]$ 赋值为 $v$．

首先，将区间 $[l, r]$ 截取出来．依次调用 `split(r + 1), split(l)`，将此两者返回的迭代器记作 $itr, itl$，那么 $[itl, itr)$ 这个迭代器范围就指向了珂朵莉树中 $[l,r]$ 包含的所有区间．

然后，将原有的信息删除．`std::set` 有成员方法 `erase`，签名如同 `iterator erase( const_iterator first, const_iterator last );`，可以移除范围 `[first; last)` 中的元素．于是我们调用 `odt.erase(itl, itr);` 以删除原有的信息．

最后，插入区间 $[l,r]$ 的新值．调用 `odt.insert(Node_t(l, r, v))` 即可．

参考代码如下：

```cpp
void assign(int l, int r, int v) {
  auto itr = split(r + 1), itl = split(l);
  odt.erase(itl, itr);
  odt.insert(Node_t(l, r, v));
}
```

???+ note "为什么需要先 `split(r + 1)` 再 `split(l)`？"
    1.  `std::set::erase` 方法将使指向被擦除元素的引用和迭代器失效．而其他引用和迭代器不受影响．
    2.  `std::set::insert` 方法不会使任何迭代器或引用失效．
    3.  `split` 操作会将区间拆开．调用 `split(r + 1)` 之后 $r + 1$ 会成为两个新区间中右边区间的左端点，此时 `split` 左区间，必然不会访问到 $r + 1$ 为左端点的那个区间，也就不会将其拆开，删去 $r + 1$ 为左端点的区间，使迭代器失效．反之，先 `split(l)`，再 `split(r + 1)`，可能会把 $l$ 为左端点的区间删去，使迭代器失效．

### perform 操作

将珂朵莉树上的一段区间提取出来并进行操作．与 `assign` 操作类似，只不过是将删除区间改为遍历区间．

参考代码如下：

```cpp
void perform(int l, int r) {
  auto itr = split(r + 1), itl = split(l);
  for (; itl != itr; ++itl) {
    // Perform Operations here
  }
}
```

注意不应该滥用这样的提取操作，可能使得时间复杂度错误．见下文「复杂度分析」一栏．

## 实现（std::map）

相较于 `std::set` 的实现，`std::map` 的实现的 `split` 操作写法更简单．除此之外，其余操作与 `std::set` 并无二异．

### 结点存储

由于珂朵莉树存储的区间是连续的，我们不一定要记下右端点是什么．不妨使用一个 `map<int, int> mp;` 存储所有区间，其键维护左端点，其值维护其对应的左端点到下一个左端点之前的值．

初始化时，如题目要求维护位置 $1$ 到 $n$ 的信息，则调用 `mp[1] = -1, mp[n + 1] = -1` 表示将 $[1,n+1)$ 即 $[1, n]$ 都设为特殊值 $-1$，$[n+1, +\infty)$ 这个区间当作哨兵使用，也可以对它进行初始化．

### split 操作

参考代码：（第一份）

```cpp
void split(int x) {
  auto it = prev(mp.upper_bound(x));  // 找到左端点小于等于 x 的区间．
  mp[x] = it->second;  // 设立新的区间，并将上一个区间储存的值复制给本区间．
}
```

参考代码：（第二份）

```cpp
auto split(int pos) {
  auto it = prev(mp.upper_bound(pos));  // 找到左端点小于等于 x 的区间．
  return mp.insert(it, make_pair(pos, it->second));
  // 设立新的区间，并将上一个区间储存的值复制给本区间．
}
```

这里使用了 `std::map::insert` 的重载 `iterator insert( const_iterator pos, const value_type& value );`，其插入 `value` 到尽可能接近正好在 `pos` 之前的位置．如果插入恰好发生在正好在 `pos` 之前的位置，那么复杂度是均摊常数，否则复杂度与容器大小成对数．

### assign 操作

对于 assign 操作，我们需要把 $[l,r−1]$ 内所有区间左端点删除，再建立新的区间．

```cpp
void assign(int l, int r, int v) {  // 注意，这里的r是区间右端点+1
  split(l);
  split(r);
  auto it = mp.find(l);
  while (it->first != r) {
    it = mp.erase(it);
  }
  mp[l] = v;
}
```

### perform 操作

```cpp
void perform(int l, int r) {  // 注意，这里的r是区间右端点+1
  split(l);
  split(r);
  auto it = mp.find(l);
  while (it->first != r) {
    // Perform Operations here
    it = next(it);
  }
}
```

## 实现（链表）

目前主流的实现是基于 `set` 来维护节点，但由于平均维护的区间个数很小，`set` 的优势并不明显．相比之下，链表（或数组）能更简洁地维护分裂与合并操作．

### 结点存储

```cpp
using i64 = int64_t;

struct Block {
  Block *next;  // 链表下一节点
  int l, r;     // 区间范围
  i64 val;      // 区间上的值

  Block(Block *next, int l, int r, i64 val)
      : next(next), l(l), r(r), val(val) {}

  bool operator<(const Block &b) const { return val < b.val; }
} *root;
```

### split 操作

```cpp
// 返回左端点为 mid+1 的区间
Block *split(int mid) {
  for (Block *b = root; b; b = b->next) {  // 遍历链表
    if (b->l == mid + 1) {                 // 左端点为 mid+1
      return b;
    }
    // 寻找能包含 mid 和 mid+1 的区间 [l, r]，将其被拆分成 [l, mid] 和 [mid+1,
    // r]
    if (b->l <= mid && mid + 1 <= b->r) {
      b->next = new Block(b->next, mid + 1, b->r, b->val);
      b->r = mid;
      return b->next;
    }
  }
  return nullptr;  // 未找到，返回空
}
```

在操作区间时，由于不能只维护区间的一部分，所以下面的操作进行之前都需要预先分裂区间，再完成相应操作．

```cpp
Block *lb, *rb;

// 预分裂，保证后续操作在 [l, r] 内部
void prepare(int l, int r) {
  lb = split(l - 1);
  rb = split(r);
}
```

### assign 操作

```cpp
void assign(int l, int r, i64 val) {
  prepare(l, r);
  lb->r = r;  // 将区间 [lb.l, lb.r] 修改成 [lb.l, r]
  lb->val = val;
  lb->next = rb;  // 将 [lb.l, r] 链至其右侧相邻区间
}

// 注：这里没有释放被删除节点的内存，若有需要可自行添加
```

### perform 操作

```cpp
void perform(int l, int r) {
  prepare(l, r);
  for (Block *b = lb; b != rb; b = b->next) {
    // Perform Operations here
  }
}
```

## 复杂度分析

### perform 以后立即对同一区间调用 assign

此时观察发现，两次 `split` 操作至多增加两个区间；一次 `assign` 将删除范围内的所有区间并增加一个区间，同时遍历所删除的区间．所以，我们所遍历的区间与所删除的区间数量成线性，而每次操作都只会增加 $O(1)$ 个区间，所以我们操作的区间数量关于操作次数（包括初始化）成线性，时间复杂度为均摊 $O(m\log n)$，其中 $m$ 为操作次数，$n$ 为珂朵莉树中最大区间个数（可以认为 $n\leq m$）．

### perform 以后不进行 assign

如果允许特殊构造数据，这样一定是能被卡掉的，只需要使珂朵莉树中有足够多的不同区间并反复遍历，就能使珂朵莉树的复杂度达到甚至高于平方级别．

如果要保证复杂度正确，必须保证数据随机．详见 [Codeforces 上关于珂朵莉树的复杂度的证明](http://codeforces.com/blog/entry/56135?#comment-398940)．更详细的严格证明见 [珂朵莉树的复杂度分析](https://zhuanlan.zhihu.com/p/102786071)．证明的结论是：用 `std::set` 实现的珂朵莉树的复杂度为 $O(n \log \log n)$，而用链表实现的复杂度为 $O(n \log n)$．

## 习题

-   [「Luogu 1840」Color the Axis](https://www.luogu.com.cn/problem/P1840)
-   ~~[「SCOI2010」序列操作](https://www.luogu.com.cn/problem/P2572)~~（该题目来源已添加 Hack 数据）
-   [「SHOI2015」脑洞治疗仪](https://loj.ac/problem/2037)
-   [「Luogu 4979」矿洞：坍塌](https://www.luogu.com.cn/problem/P4979)
-   [「Luogu 8146」risrqnis](https://www.luogu.com.cn/problem/P8146)

## 扩展阅读

[ODT 的映射思想的推广 - 洛谷专栏 (luogu.com.cn)](https://www.luogu.com.cn/article/0mys9qkh)

## 参考资料和注释

-   [Problem - 896C - Codeforces](https://codeforces.com/problemset/problem/896/C)（珂朵莉树的起源）
-   [CF896C Willem, Chtholly and Seniorious 题解 - 洛谷专栏 (luogu.com.cn)](https://www.luogu.com.cn/article/gyxbe23s)（`std::set` 实现参考）
-   [珂朵莉树的 map 实现 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/469794466)（`std::map` 实现参考）
-   [题解 CF896C【Willem, Chtholly and Seniorious】- 洛谷专栏 (luogu.com.cn)](https://www.luogu.com.cn/article/umiw1fwp)（链表实现参考）
-   [Codeforces Round #449 Editorial - Codeforces](https://codeforces.com/blog/entry/56135?#comment-398940)（关于珂朵莉树的复杂度的证明）
-   [珂朵莉树的复杂度分析 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/102786071)（珂朵莉树的复杂度分析）


## misc/offline.md

本章将介绍离线算法（Offline Algorithm）的思想、常见算法及优化．

离线算法是基于「**求解前已知所有数据**」这一假设来设计的，适用于有多组询问的题目．相对的还有 [在线算法](https://en.wikipedia.org/wiki/Online_algorithm)（Online Algorithm）．

例如 [选择排序](../basic/selection-sort.md) 必须知道数组的全局最小元素才能执行，所以是离线算法，而 [插入排序](../basic/insertion-sort.md) 可以动态接收数据进行排序，不强制要求执行前已知全部数据，所以是在线算法．

对于相同的问题，在设计难度等方面，离线算法往往优于在线算法．为了阻止选手使用离线算法，有时题目会使用「强制在线」的方式，常见的有需要前一个询问的答案才能得到下一个询问的参数（[交互题](../contest/problems.md#交互题) 与 [通信题](../contest/problems.md#通信题) 也属于此类）．

离线算法的常见思路包括将询问统一求解（如 [CDQ 分治](./cdq-divide.md)）、通过一个询问的答案求出另外相似询问的答案（如 [整体二分](./parallel-binsearch.md) 和 [莫队算法](./mo-algo-intro.md)）等．

由于离线算法是一种思想而并不是某种具体的算法，因此它会搭配各种各样的数据结构或算法一起使用，与之相关的题目种类也更为繁杂．


## misc/parallel-binsearch.md

## 引入

在信息学竞赛中，有一部分题目可以使用二分的办法来解决．但是当这种题目有多次询问且我们每次查询都直接二分可能导致 TLE 时，就会用到整体二分．整体二分的主体思路就是把多个查询一起解决．（所以这是一个离线算法）

可以使用整体二分解决的题目需要满足以下性质[^ref1]：

1.  询问的答案具有可二分性
2.  **修改对判定答案的贡献互相独立**，修改之间互不影响效果
3.  修改如果对判定答案有贡献，则贡献为一确定的与判定标准无关的值
4.  贡献满足交换律，结合律，具有可加性
5.  题目允许使用离线算法

## 解释

记 $[l,r]$ 为答案的值域，$[L,R]$ 为答案的定义域．（也就是说求答案时仅考虑下标在区间 $[L,R]$ 内的操作和询问，这其中询问的答案在 $[l,r]$ 内）

-   我们首先把所有操作 **按时间顺序** 存入数组中，然后开始分治．
-   在每一层分治中，利用数据结构（常见的是树状数组）统计当前查询的答案和 $mid$ 之间的关系．
-   根据查询出来的答案和 $mid$ 间的关系（小于等于 $mid$ 和大于 $mid$）将当前处理的操作序列分为 $q1$ 和 $q2$ 两份，并分别递归处理．
-   当 $l=r$ 时，找到答案，记录答案并返回即可．

需要注意的是，在整体二分过程中，若当前处理的值域为 $[l,r]$，则此时最终答案范围不在 $[l,r]$ 的询问会在其他时候处理．

## 过程

???+ tip "注"
    1.  为可读性，文中代码或未采用实际竞赛中的常见写法．
    2.  若觉得某段代码有难以理解之处，请先参考之前题目的解释，因为节省篇幅解释过的内容不再赘述．

从普通二分说起：

### 查询全局第 k 小

???+ note "题 1"
    在一个数列中查询第 $k$ 小的数．

??? note "解法"
    当然可以直接排序．如果用二分法呢？可以用数据结构记录每个大小范围内有多少个数，然后用二分法猜测，利用数据结构检验．

???+ note "题 2"
    在一个数列中多次查询第 $k$ 小的数．

??? note "解法"
    可以对于每个询问进行一次二分；但是，也可以把所有的询问放在一起二分．
    
    先考虑二分的本质：假设要猜一个 $[l,r]$ 之间的数，猜测之后会知道是猜大了，猜小了还是刚好．当然可以从 $l$ 枚举到 $r$，但更优秀的方法是二分：猜测答案是 $m = \lfloor\frac{l + r}{2}\rfloor$，然后去验证 $m$ 的正确性，再调整边界．这样做每次询问的复杂度为 $O(\log n)$，若询问次数为 $q$，则时间复杂度为 $O(q\log n)$．
    
    回过头来，对于当前的所有询问，可以去猜测所有询问的答案都是 $mid$，然后去依次验证每个询问的答案应该是小于等于 $mid$ 的还是大于 $mid$ 的，并将询问分为两个部分（不大于/大于），对于每个部分继续二分．注意：如果一个询问的答案是大于 $mid$ 的，则在将其划至右侧前需更新它的 $k$，即，如果当前数列中小于等于 $mid$ 的数有 $t$ 个，则将询问划分后实际是在右区间询问第 $k - t$ 小数．如果一个部分的 $l = r$ 了，则结束这个部分的二分．利用线段树的相关知识，我们每次将整个答案可能在的区间 $[1,n]$（假设已经离散化）划分成了若干个部分，这样的划分共进行了 $O(\log n)$ 次，一次划分会将整个操作序列操作一次．若对整个序列进行操作，并支持对应的查询的时间复杂度为 $O(T)$，则整体二分的时间复杂度为 $O(T\log n)$．

??? note "参考代码"
    ```cpp
    struct Query {
      int id, k;  // 这个询问的编号, 这个询问的 k
    };
    
    int ans[N], a[N];  // ans[i] 表示编号为i的询问的答案，a 为原数列
    int val[N], cnt[N];  // 离散化后，记录对应的值及其计数（假设已经处理好）
    
    // 返回原数列中值域在 [l,r] 中的数的个数
    int check(int l, int r) {
      int res = 0;
      for (int i = l; i <= r; i++) {
        res += cnt[i];
      }
      return res;
    }
    
    // 整体二分
    void solve(int l, int r, vector<Query> q) {
      int m = (l + r) / 2;
      if (l == r) {
        for (unsigned i = 0; i < q.size(); i++) ans[q[i].id] = val[l];
        return;
      }
      vector<Query> q1, q2;
      int t = check(l, m);
      for (unsigned i = 0; i < q.size(); i++) {
        if (q[i].k <= t)
          q1.push_back(q[i]);
        else
          q[i].k -= t, q2.push_back(q[i]);
      }
      solve(l, m, q1), solve(m + 1, r, q2);
      return;
    }
    ```

### 查询区间第 k 小

???+ note "题 3"
    在一个数列中多次查询区间第 $k$ 小的数．

??? note "解法"
    涉及到给定区间的查询，再按之前的方法进行二分就会导致 `check` 函数的时间复杂度爆炸．仍然考虑询问与值域中点 $m$ 的关系：若询问区间内小于等于 $m$ 的数有 $t$ 个，询问的是区间内的 $k$ 小数，则当 $k \leq t$ 时，答案应小于等于 $m$；否则，答案应大于 $m$．（注意边界问题）此处需记录一个区间小于等于指定数的数的数量，即单点加，求区间和，可用树状数组快速处理．为提高效率，只对数列中值在值域区间 $[l,r]$ 的数进行统计，即，在进一步递归之前，不仅将询问划分，将当前处理的数按值域范围划为两半．

??? note "参考代码（关键部分）"
    ```cpp
    struct Num {
      int p, x;
    };  // 位于数列中第 p 项的数的值为 x
    
    struct Query {
      int l, r, k, id;
    };  // 一个编号为 id, 询问 [l,r] 中第 k 小数的询问
    
    int ans[N];
    void add(int p, int x);  // 树状数组, 在 p 位置加上 x
    int query(int p);        // 树状数组, 求 [1,p] 的和
    void clear();            // 树状数组, 清空
    
    void solve(int l, int r, vector<Num> a, vector<Query> q)
    // a中为给定数列中值在值域区间 [l,r] 中的数
    {
      int m = (l + r) / 2;
      if (l == r) {
        for (unsigned i = 0; i < q.size(); i++) ans[q[i].id] = l;
        return;
      }
      vector<Num> a1, a2;
      vector<Query> q1, q2;
      for (unsigned i = 0; i < a.size(); i++)
        if (a[i].x <= m)
          a1.push_back(a[i]), add(a[i].p, 1);
        else
          a2.push_back(a[i]);
      for (unsigned i = 0; i < q.size(); i++) {
        int t = query(q[i].r) - query(q[i].l - 1);
        if (q[i].k <= t)
          q1.push_back(q[i]);
        else
          q[i].k -= t, q2.push_back(q[i]);
      }
      clear();
      solve(l, m, a1, q1), solve(m + 1, r, a2, q2);
      return;
    }
    ```

下面提供 [【模板】可持久化线段树 2](https://www.luogu.com.cn/problem/P3834) 一题使用整体二分的，偏向竞赛风格的写法．

??? note "参考代码"
    ```cpp
    --8<-- "docs/misc/code/parallel-binsearch/parallel-binsearch_1.cpp"
    ```

### 带修区间第 k 小

???+ note "题 4（[Dynamic Rankings](https://www.luogu.com.cn/problem/P2617)）"
    给定一个数列，要支持单点修改，区间查第 $k$ 小．

??? note "解法"
    修改操作可以直接理解为从原数列中删去一个数再添加一个数，为方便起见，将询问和修改统称为「操作」．因后面的操作会依附于之前的操作，不能如题 3 一样将统计和处理询问分开，故可将所有操作存于一个数组，用标识区分类型，依次处理每个操作．为便于处理树状数组，修改操作可分拆为擦除操作和插入操作．
    
    **优化**
    
    1.  注意到每次对于操作进行分类时，只会更改操作顺序，故可直接在原数组上操作．具体实现，在二分时将记录操作的 $q, a$ 数组换为一个大的全局数组，二分时记录信息变为 $L, R$，即当前处理的操作是全局数组上的哪个区间．利用临时数组记录当前的分类情况，进一步递归前将临时数组信息写回原数组．
    2.  树状数组每次清空会导致时间复杂度爆炸，可采用每次使用树状数组时记录当前修改位置（这已由 1 中提到的临时数组实现），本次操作结束后在原位置加 $-1$ 的方法快速清零．
    3.  一开始对于数列的初始化操作可简化为插入操作．

??? note "参考代码（关键部分）"
    ```cpp
    struct Opt {
      int x, y, k, type, id;
      // 对于询问, type = 1, x, y 表示区间左右边界, k 表示询问第 k 小
      // 对于修改, type = 0, x 表示修改位置, y 表示修改后的值,
      // k 表示当前操作是插入(1)还是擦除(-1), 更新树状数组时使用.
      // id 记录每个操作原先的编号, 因二分过程中操作顺序会被打散
    };
    
    Opt q[N], q1[N], q2[N];
    // q 为所有操作,
    // 二分过程中, 分到左边的操作存到 q1 中, 分到右边的操作存到 q2 中.
    int ans[N];
    void add(int p, int x);
    int query(int p);  // 树状数组函数, 含义见题3
    
    void solve(int l, int r, int L, int R)
    // 当前的值域范围为 [l,r], 处理的操作的区间为 [L,R]
    {
      if (l > r || L > R) return;
      int cnt1 = 0, cnt2 = 0, m = (l + r) / 2;
      // cnt1, cnt2 分别为分到左边, 分到右边的操作数
      if (l == r) {
        for (int i = L; i <= R; i++)
          if (q[i].type == 1) ans[q[i].id] = l;
        return;
      }
      for (int i = L; i <= R; i++)
        if (q[i].type == 1) {  // 是询问: 进行分类
          int t = query(q[i].y) - query(q[i].x - 1);
          if (q[i].k <= t)
            q1[++cnt1] = q[i];
          else
            q[i].k -= t, q2[++cnt2] = q[i];
        } else
          // 是修改: 更新树状数组 & 分类
          if (q[i].y <= m)
            add(q[i].x, q[i].k), q1[++cnt1] = q[i];
          else
            q2[++cnt2] = q[i];
      for (int i = 1; i <= cnt1; i++)
        if (q1[i].type == 0) add(q1[i].x, -q1[i].k);  // 清空树状数组
      for (int i = 1; i <= cnt1; i++) q[L + i - 1] = q1[i];
      for (int i = 1; i <= cnt2; i++)
        q[L + cnt1 + i - 1] = q2[i];  // 将临时数组中的元素合并回原数组
      solve(l, m, L, L + cnt1 - 1), solve(m + 1, r, L + cnt1, R);
      return;
    }
    ```

### 针对静态序列的优化

???+ note "题 5（[【模板】可持久化线段树 2](https://www.luogu.com.cn/problem/P3834)）"
    给定一个序列，区间查询第 $k$ 小．

??? note "解法"
    树套树和整体二分实现带修区间第 $k$ 小问题的复杂度都为 $O(n \log^2 n)$，但静态区间第 $k$ 小问题可以使用可持久化线段树在 $O(n \log n)$ 时间复杂度内解决，而几乎所有整体二分实现的静态区间第 $k$ 小问题代码时间复杂度都是 $O(n \log^2 n)$，面对大数据范围时存在 TLE 的风险．（这里默认值域与序列长度同阶，值域与序列长不同阶的情况可以通过离散化转化为同阶情况）
    
    **优化**
    
    1.  对于每一轮划分，如果当前数列中小于等于 $mid$ 的数有 $t$ 个，则将询问划分后实际是在右区间询问第 $k - t$ 小数，因此对划分到右区间的询问做出了修改．如果答案的原始值域为 $[L,R]$，某次划分的答案值域为 $[l,r]$，那么对于参与此次划分的询问，$[L,l)$ 中所有数值对它们的影响已经在之前被消除了．
    2.  由于需要使每轮划分都仅和当前答案值域 $[l,r]$ 有关，树状数组需要多次载入和清空．
    
    如果划分不仅仅和当前答案值域有关呢？
    
    由此可以得到一个与全局序列有关的优化方法：维护一个指针 $pos$ 追踪每轮划分的 $mid$（分治中心），将所有 $\leq pos$ 的元素对应的下标在树状数组中置为 $1$，树状数组的其余位置置为 $0$．每次划分之前移动 $pos$ 并更新树状数组．指针 $pos$ 移动的次数与 $n \log n$ 同阶．划分时对每一个询问查询树状数组中对应区间的值，满足则划分至左区间，否则划分至右区间，**不需要对询问做出修改**．
    
    由于要追踪分治中心，需要让 $pos$ 准确地更新树状数组．在整体二分之前将序列按元素大小排序并记录元素对应下标，指针移动时在树状数组中对下标进行相应修改．对于绝大多数 **可以用整体二分解决并且不带修改的问题**，都可以应用此种优化以大幅降低数据结构的使用次数．
    
    由于减少了很多树状数组的载入和清空操作，应用这种优化通常情况下会明显提升整体二分的效率（即使只是常数优化），对于静态区间第 $k$ 小值问题而言效率完全不差于时间复杂度更优的可持久化线段树．值得注意的是，对于静态区间第 $k$ 小值问题也存在时间复杂度 $O(n \log n)$ 的整体二分实现．

??? note "参考代码（关键部分）"
    ```cpp
    struct Query {
      int i, l, r, k;
    };  // 第 i 次询问查询区间 [l,r] 的第 k 小值
    
    Query s[200005], t1[200005], t2[200005];
    int n, m, cnt, pos, p[200005], ans[200005];
    pair<int, int> a[200005];
    
    void add(int x, int y);  // 树状数组 位置 x 加 y
    int sum(int x);          // 树状数组 [1,x] 前缀和
    
    // 当前处理的询问为 [l,r],答案值域为 [ql,qr]
    void overall_binary(int l, int r, int ql, int qr) {
      if (l > r) return;
      if (ql == qr) {
        for (int i = l; i <= r; i++) ans[s[i].i] = ql;
        return;
      }
      int cnt1 = 0, cnt2 = 0, mid = (ql + qr) >> 1;
      // 追踪分治中心,认为 [1,pos] 的值已经载入树状数组
      while (pos <= n - 1 && a[pos + 1].first <= mid)
        add(a[pos + 1].second, 1), ++pos;
      while (pos >= 1 && a[pos].first > mid) add(a[pos].second, -1), --pos;
    
      for (int i = l; i <= r; i++) {
        int now = sum(s[i].r) - sum(s[i].l - 1);
        if (s[i].k <= now)
          t1[++cnt1] = s[i];
        else
          t2[++cnt2] = s[i];  // 注意 不应修改询问信息
      }
      for (int i = 1; i <= cnt1; i++) s[l + i - 1] = t1[i];
      for (int i = 1; i <= cnt2; i++) s[l + cnt1 + i - 1] = t2[i];
    
      overall_binary(l, l + cnt1 - 1, ql, mid);
      overall_binary(l + cnt1, r, mid + 1, qr);
    }
    
    int main() {
      scanf("%d%d", &n, &m);
      for (int i = 1; i <= n; i++) {
        scanf("%d", &a[i].first);
        a[i].second = i;
        p[++cnt] = a[i].first;
      }
      sort(a + 1, a + n + 1);  // 对序列排序 离散化
      sort(p + 1, p + n + 1);
      cnt = unique(p + 1, p + n + 1) - p - 1;
      for (int i = 1; i <= n; i++)
        a[i].first = lower_bound(p + 1, p + cnt + 1, a[i].first) - p;
      // 省略读入询问
      overall_binary(1, m, 1, cnt);
      for (int i = 1; i <= n; i++) printf("%d\n", p[ans[i]]);
      return 0;
    }
    ```

### 区间前驱后继

???+ note "题 6"
    在一个数列中多次查询 $k$ 在区间中的前驱（严格小于 $k$，且最大的数）或后继（严格大于 $k$，且最小的数），保证存在这样的数．

??? note "解法"
    以前驱为例，使用数据结构解决此种问题的方法一般是先查询区间内有多少严格小于 $k$ 的数（设它们的数量为 $x$），再查询区间第 $x$ 小的数．后继则是查询区间内有多少不大于 $k$ 的数（数量为 $x$），然后查询区间第 $x+1$ 小的数．
    
    考虑使用整体二分解决这个问题：整体二分是一种高效求解区间第 $k$ 小的离线算法，而 [CDQ 分治](./cdq-divide.md) 可以离线高效求解区间内的排名．先跑一遍 CDQ 分治求出排名就可以使用整体二分得到区间内部的前驱和后继了．
    
    此问题还可以用 CDQ 分治套线段树离线一遍解决，但效率远低于跑两遍的 CDQ 分治 + 整体二分．

### 构造单调性序列

???+ note "题 7（[Sequence](https://www.luogu.com.cn/problem/P4597)）"
    给定一个序列，每次操作可以把某个数 $+1$ 或 $−1$．要求把序列变成单调不降的，并且修改后的数列只能出现修改前的数，输出最小操作次数．

??? note "解法"
    此类题目也可以使用动态规划或反悔贪心解决．
    
    在满足操作次数最小化的前提下，一定存在一种方案使得最后序列中的每个数都是序列修改前存在的，这个结论可以使用数学归纳法证明．由于题目并不需要最终序列的信息，问题转化为求出最小操作次数．
    
    由于要求最终的序列单调不降，可以使用整体二分．每轮整体二分判定最终序列区间 $[l,r]$ 的值域，此时答案的值域为 $[ql,qr]$．令 $mid=\lfloor\frac{ql + qr}{2}\rfloor$，每轮二分开始时默认将所有数划分至 $[mid+1,qr]$（要划分到 $[ql,mid]$ 的数设为 $0$ 个），初始代价设为将序列区间 $[l,r]$ 全部置为 $mid+1$ 的操作次数．依次枚举区间 $[l,r]$ 中的数 $i$ 并且计算将 $[l,i]$ 置为 $mid$、将 $[i+1,r]$ 置为 $mid+1$ 的操作次数之和，如果优于之前的操作次数则更新最少操作次数和要划分到 $[ql,mid]$ 的数的个数．
    
    划分时已经保证了最终序列的单调性不被破坏，同时因为每次都取最小操作次数，最终被划分至左区间的数取 $mid$ 一定比取 $mid+1$ 更优，故整体二分得到的序列一定是单调不降且操作次数最小的．计算操作次数输出即可．

??? note "参考代码（关键部分）"
    ```cpp
    int a[500005], ans[500005];  // a:原序列 ans:构造的序列
    
    void overall_binary(int l, int r, int ql, int qr) {
      if (l > r) return;
      if (ql == qr) {
        for (int i = l; i <= r; i++) ans[i] = ql;
        return;
      }
      int cnt = 0,
          mid = ql + ((qr - ql) >> 1);  // 默认开始都填 mid+1 全部划分到右区间
      long long res = 0ll, sum = 0ll;
      for (int i = l; i <= r; i++) sum += abs(a[i] - (mid + 1));
      res = sum;
      for (int i = l; i <= r;
           i++) {  // 尝试把 [l,i] 从 mid+1 换成 mid 并且划分到左区间
        sum -= abs(a[i] - (mid + 1));
        sum += abs(a[i] - mid);
        if (sum < res) cnt = i - l + 1, res = sum;  // 发现 [l,i] 取 mid 更优,更新
      }
      overall_binary(l, l + cnt - 1, ql, mid);
      overall_binary(l + cnt, r, mid + 1, qr);
    }
    ```

### 参考习题

-   [「国家集训队」矩阵乘法](https://www.luogu.com.cn/problem/P1527)
-   [「POI2011 R3 Day2」流星 Meteors](https://loj.ac/p/2169)
-   [二逼平衡树](https://loj.ac/p/106)
-   [\[BalticOI 2004\] Sequence 数字序列](https://www.luogu.com.cn/problem/P4331)

## 参考资料与注释

-   许昊然．浅谈数据结构题的几个非经典解法．[2013 年信息学奥林匹克中国国家队侯选队员论文集](https://github.com/OI-wiki/libs/blob/master/%E9%9B%86%E8%AE%AD%E9%98%9F%E5%8E%86%E5%B9%B4%E8%AE%BA%E6%96%87/%E5%9B%BD%E5%AE%B6%E9%9B%86%E8%AE%AD%E9%98%9F2013%E8%AE%BA%E6%96%87%E9%9B%86.pdf)．

[^ref1]: 许昊然．浅谈数据结构题的几个非经典解法．[2013 年信息学奥林匹克中国国家队侯选队员论文集](https://github.com/OI-wiki/libs/blob/master/%E9%9B%86%E8%AE%AD%E9%98%9F%E5%8E%86%E5%B9%B4%E8%AE%BA%E6%96%87/%E5%9B%BD%E5%AE%B6%E9%9B%86%E8%AE%AD%E9%98%9F2013%E8%AE%BA%E6%96%87%E9%9B%86.pdf)．


## misc/rand-technique.md

author: Ir1d, partychicken, ouuan, Marcythm, TianyiQ

## 概述

前置知识：[随机函数](../misc/random.md) 和 [概率初步](../math/probability/basic-conception.md)

本文将对 OI/ICPC 中的随机化相关技巧做一个简单的分类，并对每个分类予以介绍．本文也将介绍一些在 OI/ICPC 中很少使用，但与 OI/ICPC 在风格等方面较为贴近的方法，这些内容前将用 `(*)` 标注．

这一分类并不代表广泛共识，也必定不能囊括所有可能性，因此仅供参考．

**记号和约定**：

-   $\mathrm{Pr}[A]$ 表示事件 $A$ 发生的概率．
-   $\mathrm{E}[X]$ 表示随机变量 $X$ 的期望．
-   赋值号 $:=$ 表示引入新的量，例如 $Y:=1926$ 表示引入值为 $1926$ 的量 $Y$．

## 用随机集合覆盖目标元素

庞大的解空间中有一个（或多个）解是我们想要的．我们可以尝试进行多次撒网，只要有一次能够网住目标解就能成功．

### 例：三部图的判定

???+ note "问题"
    给定一张 $n$ 个结点、$m$ 条边的简单无向图，用 RGB 三种颜色给每个结点染色 满足任意一对邻居都不同色，或者报告无解．

对每个点 $v$，从 $\{R,G,B\}$ 中等概率独立随机地选一种颜色 $C_v$，并钦定 $v$  **不** 被染成 $C_v$．最优解恰好符合这些限制的概率，显然是 $\big(\frac 23\big)^n$．

在这些限制下，对于一对邻居 $(u,v)$，「$u,v$ 不同色」的要求等价于以下这条「推出」关系：

-   对于所有异于 $C_u,C_v$ 的颜色 $X$，若 $u$ 被染成 $X$，则 $v$ 被染成 $\{R,G,B\}\setminus\{X,C_v\}$．

于是我们可以对每个 $v$ 设置布尔变量 $B_v$，其取值表示 $v$ 被染成两种剩余的颜色中的哪一种．借助 2-SAT 模型即可以 $O(n+m)$ 的复杂度解决这个问题．

这样做，单次的正确率是 $\big(\frac 23\big)^n$．将算法重复运行 $-\big(\frac 32\big)^n\log \epsilon$ 次，只要有一次得到解就输出，这样即可保证 $1-\epsilon$ 的正确率．（详见后文中「概率上界的分析」）

***

**回顾**：本题中「解空间」就是集合 $\{R,G,B\}^n$，我们每次通过随机施加限制来在一个缩小的范围内搜寻「目标解」——即合法的染色方案．

### 例：[CodeChef SELEDGE](https://www.codechef.com/problems/SELEDGE)

???+ note "简要题意"
    给定一张点、边都有非负权值的无向图，找到一个大小 $\leq K$ 的边集合 $S$，以最大化与 $S$ 相连的点的权值和减去 $S$ 的边权和．一个点的权值只被计算一次．

观察：如果选出的边中有三条边构成一条链，则删掉中间的那条一定不劣；如果选出的边中有若干条构成环，则删掉任何一条一定不劣．

推论：最优解选出的边集，一定构成若干个不相交的菊花图（即直径不超过 2 的树）．

推论：最优解选出的边集，一定构成一张二分图．

我们对每个点等概率独立随机地染上黑白两种颜色之一，并要求这一染色方案，恰好也是最优解所对应的二分图的黑白染色方案．

尝试计算最优解符合这一要求的概率：

-   考虑一张 $n$ 个点的菊花图，显然它有 2 种染色方案，所以它被染对颜色的概率是 $\dfrac 2{2^n}=2^{1-n}$．
-   假设最优解中每个菊花的结点数分别为 $a_1,\cdots,a_l$，则一定有 $(a_1-1)+\cdots+(a_l-1)\leq K$，其中 $K$ 表示最多能够选出的边数．
-   从而所有菊花都被染对颜色的概率是 $2^{1-a_1}\cdots 2^{1-a_l}\geq 2^{-K}$．

在上述要求下，尝试建立费用流模型计算最优答案：

-   建立二分图，白点在左侧并与 $S$ 相连，黑点在右侧并与 $T$ 相连．
    -   对于白点 $v$，从 $S$ 向它连一条容量为 1、费用为 $-A_v$ 的边，和一条容量为 $\infty$、费用为 0 的边．
    -   对于黑点 $v$，从它向 $T$ 连一条容量为 1、费用为 $-A_v$ 的边，和一条容量为 $\infty$、费用为 0 的边．
-   对于原图中的边 $(u,v,B)$ 满足 $u$ 为白色、$v$ 为黑色，连一条从 $u$ 到 $v$ 的边，容量为 1，费用为 $B$．
-   在该图中限制流量不超过 $K$，则最小费用的相反数就是答案．

用 SPFA 费用流求解的话，复杂度是 $O\big(K^2(n+m)\big)$，证明：

-   首先，显然 SPFA 的运行次数 $\leq K$．
-   然后，在一次 SPFA 中，任何一个结点至多入队 $O(K)$ 次．这是因为：
    -   任意时刻有流量的边不会超过 $3K$ 条，否则就意味着在原图中选了超过 $K$ 条边．
    -   对于任何一条长为 $L$ 的增广路，其中至少有 $\dfrac L2-2$ 条边是某条有流量的边的反向边，因为正向边都是从图的左侧指向右侧，只有这些反向边才会从右侧指向左侧．
    -   综合以上两条，得到任意一条增广路的长度不超过 $6K+4$．
-   综上，复杂度是 $O\big(K^2(n+m)\big)$．

和上一题类似，我们需要把整个过程重复 $-2^K \log\epsilon$ 次以得到 $1-\epsilon$ 的正确率．总复杂度 $O\big(2^KK^2(n+m)\cdot -\log\epsilon\big)$．

## 用随机元素命中目标集合

我们需要确定一个集合中的任意一个元素，为此我们随机选取元素，以期能够恰好命中这一集合．

### 例：[Gym 101550I](https://codeforces.com/gym/101550/attachments)

???+ note "简要题意"
    有一张图形如：两条平行的链，加上连接两链的两条平行边．给定这张图上的若干条简单路径（每条路径表示一次通话），请你选择尽量少的边放置窃听器，以使得每条给定的路径上都有至少一个窃听器．

整张图可以拆分为一个环加上四条从环伸出去的链．对于这四条链中的任何一条（记作 $C$），考虑在这条链上如何放置窃听器，容易通过贪心算法得到满足以下条件的方案：

-   在拦截所有 $C$ 内部进行的通话的前提下，用的窃听器数量最少．
-   在上一条的前提下，使得 $C$ 上的窃听器离环的最短距离尽可能小．
    -   作这一要求的目的是尽可能地拦截恰有一个端点在 $C$ 内部的通话．

接着考虑链与环相接处的共计 4 条边，我们暴力枚举这些边上有没有放窃听器．显然，如果想要拦截跨越链和环的通话，在这 4 条边上放窃听器一定是最优的．现在，我们可以把通话线路分为以下几种：

1.  完全在链上的通话线路．这些线路一定已经被拦截，故可以忽略．
2.  跨越链和环，且已经被拦截的通话线路．它们可以忽略．
3.  跨越链和环，且未被拦截的通话线路．我们可以直接截掉它在链上的部分（因为链上的窃听器放置方案已经固定了），只保留环上的部分．
4.  完全在环上的通话线路．

至此，问题转化成了环上的问题．

设最优解中在环上的边集 $S$ 上放置了窃听器，如果我们已经确定了 $S$ 中的任何一个元素 $e$，就可以：

-   先在 $e$ 处断环为链．
-   然后从 $e$ 开始贪心，不断找到下一个放置窃听器的边．注意到如果经过合适的预处理，贪心的每一步可以做到 $O(1)$ 的复杂度．
-   从而以 $O(|S|)$ 的复杂度解决问题．

我们考虑随机选取环上的一条边 $e'$，并钦定 $e'\in S$ 再执行上述过程，重复多次取最优．

分析单次复杂度：

-   观察：记 $S'$ 表示所有选取了 $e'$ 的方案中的最优解，则 $|S'|\leq |S|+1$．
-   从而单次复杂度 $O(|S'|)=O(|S|)$．

分析正确率：

-   显然单次正确率 $\dfrac {|S|}n$，其中 $n$ 表示环长．
-   所以需要重复 $-\dfrac n{|S|}\log\epsilon$ 次以得到 $1-\epsilon$ 的正确率．

综上，该算法的复杂度 $O\big(|S|\cdot -\dfrac n{|S|}\log\epsilon\big)=O(-n\log\epsilon)$．

### 例：[CSES 1685 New Flight Routes](https://cses.fi/problemset/task/1685)

???+ note "简要题意"
    给定一张有向图，请你加最少的边使得该图强连通，需 **输出方案**．

先对原图进行强连通缩点．我们的目标显然是使每个汇点能到达每个源点．

不难证明，我们一定只会从汇点到源点连边，因为任何其他的连边，都能对应上一条不弱于它的、从汇点到源点的连边．

我们的一个核心操作是，取汇点 $t$ 和源点 $s$（它们不必在同一个弱连通分量里），连边 $t\to s$ 以 **使得 $s$ 和 $t$ 都不再是汇点或源点**（记作目标 I）．理想情况下这种操作每次能减少一个汇点和一个源点，那我们不断操作直到只剩一个汇点或只剩一个源点，而这样的情形就很平凡了．由此，我们猜测答案是源点个数与汇点个数的较大值．

不难发现，上述操作能够达到目标 I 的充要条件是：$t$ 拥有 $s$ 以外的前驱、且 $s$ 拥有 $t$ 以外的后继．可以证明（等会会给出证明），对于任意一张有着至少两个源点和至少两个汇点的 DAG，都存在这样的 $(s,t)$；但存在性的结论无法帮助我们构造方案，还需做其他分析．

-   有了这个充要条件还难以直接得到算法，主要的原因是连边 $t\to s$ 后可能影响其他 $(s',t')$ 二元组的合法性，这个比较难处理．

注意到我们关于源汇点间的关系知之甚少（甚至连快速查询一对 $s-t$ 间是否可达都需要 dfs + bitset 预处理，而时限并不允许这么做），这提示我们需要某种非常一般和强大的性质．

观察：不满足目标 I 的 $(s,t)$ 至多有 $n+m-1$ 对，其中 $n$ 表示源点个数，$m$ 表示汇点个数．

-   理由：对于每一对这样的 $(s,t)$，若把它看成 $s,t$ 间的一条边，则所有这些边构成的图形如若干条不相交的链，于是边数不超过点数减一．
-   作出这一观察的动机是，要想将存在性结论应用于算法，前置步骤往往是把定性的结果加强为定量的结果．

推论：等概率随机选取 $(s,t)$，满足前述要求的概率 $\geq \dfrac {(n-1)(m-1)}{nm}$．

-   注意到这个结论严格强于先前给出的存在性结论．

推论：等概率独立随机地连续选取 $\dfrac {\min(n,m)}2$ 对不含公共元素的 $(s,t)$，并对它们 **依次** 操作（即连边 $t\to s$），则这些操作全部满足目标 I 的概率 $\geq \dfrac 14$．

-   理由：

$$
\begin{aligned}
&\phantom{=\ }\dfrac {(n-1)(m-1)}{nm}\cdot\dfrac{(n-2)(m-2)}{(n-1)(m-1)}\cdots\dfrac{(n-k)(m-k)}{(n-k+1)(m-k+1)}\\
&=\dfrac{(n-k)(m-k)}{nm}\\
&\geq \dfrac 14
\end{aligned}
$$

而连续选完 $k$ 对 $(s,t)$ 后判断它们是否全部满足目标 I 很简单，只要再跑一遍强连通缩点，判断一下 $n,m$ 是否都减小了 $k$ 即可．注意到若每次减少 $k=\dfrac{\min(n,m)}2$，则 $\min(n,m)$ 必在 $O\big(\log(n+m)\big)$ 轮内变成 1，也就转化到了平凡的情况．

???+ note "算法伪代码"
    ```text
    while(n>1 and m>1):
        randomly choose k=min(n,m)/2 pairs (s,t)
        add edge t->s for all these pairs
        if new_n>n-k or new_m>m-k:
            roll_back()
    solve_trivial()
    ```

复杂度 $O\big((|V|+|E|) \log |V|\big)$．

***

**回顾**：我们需要确定任意一对能够实现目标 I 的二元组 $(s,t)$，为此我们随机选择 $(s,t)$．

## 用随机化获得随机数据的性质

如果一道题的数据随机生成，我们可能可以利用随机数据的性质解决它．而在有些情况下，即使数据并非随机生成，我们也可以通过随机化来给其赋予随机数据的某些特性，从而帮助解决问题．

### 例：随机增量法

随机生成的元素序列可能具有「前缀最优解变化次数期望下很小」等性质，而随机增量法就通过随机打乱输入的序列来获得这些性质．

详见 [随机增量法](../geometry/random-incremental.md)．

### 例：[TopCoder MagicMolecule](https://archive.topcoder.com/ProblemStatement/pm/11705) 随机化解法

???+ note "简要题意"
    给定一张 $n$ 个点、带点权的无向图，在其中所有大小不小于 $\dfrac {2n}3$ 的团中，找到点权和最大的那个．
    
    $n\leq 50$

不难想到折半搜索．把点集均匀分成左右两半 $V_L,V_R$（大小都为 $\dfrac n2$），计算数组 $f_{L,k}$ 表示点集 $L\subseteq V_L$ 中的所有 $\geq k$ 元团的最大权值和．接着我们枚举右半边的每个团 $C_R$，算出左半边有哪些点与 $C_R$ 中的所有点相连（这个点集记作 $N_L$），并用 $f_{N_L,\frac 23 n-|C_R|}+\textit{value}(C_R)$ 更新答案．

-   注意到可以 $O(1)$ 转移每一个 $f_{L,k}$．具体地说，取 $d$ 为 $L$ 中的任意一个元素，然后分类讨论：
    -   假设最优解中 $d$ 不在团中，则从 $f_{L\setminus \{d\},k}$ 转移而来．
    -   假设最优解中 $d$ 在团中，则从 $f_{L\cap N(d),k}+\textit{value}(d)$ 转移而来，其中 $N(d)$ 表示 $d$ 的邻居集合．
    -   别忘了还要用 $f_{L,k+1}$ 来更新 $f_{L,k}$．

这个解法会超时．尝试优化：

-   平分点集时均匀随机地划分．这样的话，最优解的点集 $C_{res}$ 以可观的概率也被恰好平分（即 $|C_{res}\cap V_L|=|C_{res}\cap V_R|$）．
    -   当然，$|C_{res}|$ 可能是奇数．简单起见，这里假设它是偶数；奇数的情况对解法没有本质改变．
    -   实验发现，随机尝试约 20 次就能以很大概率有至少一次满足该性质．也就是说，如果我们的算法依赖于「$C_{res}$ 被平分」这一性质，则将算法重复执行 20 次取最优，同样也能保证以很大概率得到正确答案．
-   有了这一性质，我们就可以直接钦定左侧团 $L$、右侧团 $C_R$ 的大小都 $\geq \dfrac n3$．这会对复杂度带来两处改进：
    -   $f$ 可以省掉记录大小的维度．
    -   因为只需考虑大小 $\geq \dfrac n3$ 的团，所以需要考虑的左侧团 $L$ 和 右侧团 $C_R$ 的数量也大大减少至约 $1.8\cdot 10^6$．
-   现在的瓶颈变成了求单侧的某一子集的权值和，因为这需要 $O\big(2^{|V_L|}+2^{|V_R|}\big)$ 的预处理．
    -   解决方案：在 $V_L,V_R$ 内部再次折半；当查询一个子集的权值和时，将这个子集分成左右两半查询，再把答案相加．
-   这样即可通过本题．

***

**回顾**：一个随机的集合有着「在划分出的两半的数量差距不会太悬殊」这一性质，而我们通过随机划分获取了这个性质．

## 随机化用于哈希

### 例：[UOJ #207 共价大爷游长沙](https://uoj.ac/problem/207)

???+ note "简要题意"
    维护一棵动态变化的树，和一个动态变化的结点二元组集合．你需要支持：
    
    -   删边、加边．保证得到的还是一棵树．
    -   加入/删除某个结点二元组．
    -   给定一条边 $e$，判断是否对于集合中的每个结点二元组 $(s,t)$，$e$ 都在 $s,t$ 间的简单路径上．

对图中的每条边 $e$，我们定义集合 $S_e$ 表示经过该边的关键路径（即题中的 $(a,b)$）集合．考虑对每条边动态维护集合 $S_e$ 的哈希值，这样就能轻松判定 $S_e$ 是否等于全集（即 $e$ 是否是「必经之路」）．

哈希的方式是，对每个 $(a,b)$ 赋予 $2^{64}$ 以内的随机非负整数 $H_{(a,b)}$，然后一个集合的哈希值就是其中元素的 $H$ 值的异或和．

这样的话，任何一个固定的集合的哈希值一定服从 $R:=\left\{0,1,\cdots,2^{64}-1\right\}$ 上的均匀分布（换句话说，哈希值的取值范围为 $R$，且取每一个值的概率相等）．这是因为：

1.  单个 $H_{(a,b)}$ 显然服从均匀分布．
2.  两个独立且服从 $R$ 上的均匀分布的随机变量的异或和，一定也服从 $R$ 上的均匀分布．自证不难．

从而该算法的正确率是有保障的．

至于如何维护这个哈希值，使用 LCT 即可．

### 例：[CodeChef PANIC](https://www.codechef.com/problems/PANIC) 及其错误率分析

本题的大致解法：

1.  可以证明[^ref1] $S(N)$ 服从一个关于 $N$ 的 $O(K)$ 阶线性递推式．
2.  用 BM 算法求出该递推式．
3.  借助递推式，用凯莱哈密顿定理计算出 $S(N)$．

这里仅关注第二部分，即如何求一个矩阵序列的递推式．所以我们只需考虑下述问题：

???+ note "问题"
    给定一个矩阵序列，该序列在模 $P:=998244353$ 意义下服从一个齐次线性递推式（递推式中的数乘和加法运算定义为矩阵的数乘和加法），求出最短递推式．

如果一系列矩阵服从一个递推式 $F$，那么它的每一位也一定服从 $F$．然而，如果对某一位求出最短递推式 $F'$，则 $F'$ 可能会比 $F$ 更短，从而产生问题．

解决方案：给矩阵的每一位 $(i,j)$ 赋予一个 $<P$ 的随机权值 $x_{i,j}$，然后对于序列中每个矩阵计算其所有位的加权和模 $P$ 的结果，再把每个矩阵算出的这个数连成一个数列，最后我们对所得数列运行 BM 算法．

错误率分析：

-   假设上述做法求得了不同于 $F$（且显然也不长于 $F$）的 $l$ 阶递推式 $F'$．
-   因为矩阵序列不服从 $F'$，所以一定存在矩阵中的某个位置 $(i,j)$，满足该位置对应的数列 $S_{i,j}$ 在某个 $N$ 处不服从 $F'$．也就是说：

$$
S(N)_{i,j}-F'_1S(N-1)_{i,j}-\cdots-F'_lS(N-l)_{i,j}\not\equiv 0\pmod {P}
$$

-   假设 $(i,j)$ 是唯一的不服从的位置，则一定有：

$$
T_{i,j}:=\Big(x_{i,j}\cdot\big(S(N)_{i,j}-F'_1S(N-1)_{i,j}-\cdots-F'_lS(N-l)_{i,j}\big)\bmod P\Big)=0
$$

-   显然这仅当 $x_{i,j}=0$ 时才成立，概率 $P^{-1}$．
-   如果有多个不服从的位置呢？
    -   对每个这样的位置 $(i,j)$，易证 $T_{i,j}$ 服从 $R:=\{0,1,\cdots,P-1\}$ 上的均匀分布．
    -   若干个互相独立的、服从 $R$ 上的均匀分布的随机变量，它们在模意义下的和，依然服从 $R$ 上的均匀分布．自证不难．
    -   从而这种情况下的错误率也是 $P^{-1}$．

### 例：[UOJ #552 同构判定鸭](https://uoj.ac/problem/552) 及其错误率分析

???+ note "简要题意"
    给定两张边权为小写字母的有向图 $G_0,G_1$，你要对这两张图分别算出「所有路径对应的字符串构成的多重集」（可能是无穷集），并判断这两个多重集是否相等．如果不相等，你要给出一个最短的串，满足它在两个多重集中的出现次数不相等．

令 $f_{K,i,j}$ 表示图 $G_K$ 中从点 $i$ 开始的所有长为 $j$ 的路径，这些路径对应的所有字符串构成的多重集的哈希值．按照 $j$ 升序考虑每个状态，转移时枚举 $i$ 的出边并钦定该边为路径上的第一条边．

要判断是否存在长度 $=L$ 的坏串，只需把 $\{f_{0,*,L}\}$ 和 $\{f_{1,*,L}\}$ 各自「整合」起来再比较即可（通配符 `*` 这里表示每一个结点，例如 $\{f_{0,*,L}\}$ 表示全体 $f_{0,i,L}$ 构成的集合，其中 $i$ 取遍所有结点）．官方题解[^ref2]中证明了最短坏串（如果存在的话）长度一定不超过 $n_1+n_2$，所以这个解法的复杂度是可靠的．

接下来考虑具体的哈希方式．注意到常规的哈希方法——即把串 $a_1a_2\cdots a_k$ 映射到 $\big(a_1+Pa_2+P^2a_3+\cdots+P^{k-1}a_k\big)\bmod Q$ 上、再把多重集的哈希值定为其中元素的哈希值之和模 $Q$——在这里是行不通的．一个反例是，集合 `{"ab","cd"}` 与集合 `{"cb","ad"}` 的哈希值是一样的，不论 $P,Q$ 如何取值．

上述做法的问题在于，一个串的哈希值是一个和式，从而其中的每一项可以拆出来并重组．为避免这一问题，我们考虑把哈希值改为一个连乘式．此外，乘法交换律会使得不同的位不可区分，为避免这一点我们要为不同的位赋予不同的权值．

对每一个二元组 $(c,j)$（其中 $c$ 为字符，$j$ 为整数表示 $c$ 在某个串中的第几位）我们都预先生成一个随机数 $x_{c,j}$．然后我们把串 $a_1a_2\cdots a_k$ 映射到 $x_{a_1,1}x_{a_2,2}\cdots x_{a_k,k}\bmod Q$ 上（其中 $Q$ 为 **随机选取** 的质数）、再把多重集的哈希值定为其中元素的哈希值之和模 $Q$．接下来分析它的错误率．

???+ note "(*)Schwartz–Zippel 引理"
    令 $f\in F[z_1,\cdots,z_k]$ 为域 $F$ 上的 $k$ 元 $d$ 次非零多项式，令 $S$ 为 $F$ 的有限子集，则至多有 $d\cdot |S|^{k-1}$ 组 $(z_1,\cdots,z_k)\in S^k$ 满足 $f(z_1,\cdots,z_k)=0$．
    
    ??? note "如果你不知道域是什么"
        你只需记得这两样东西都是域：
        
        1.  模质数的剩余系，以及其上的各种运算．
        2.  实数集，以及其上的各种运算．
    
    推论：若 $z_1,\cdots,z_k$ 都在 $S$ 中等概率独立随机选取，则 $\mathrm{Pr}\big[f(z_1,\cdots,z_k)=0\big]\leq \dfrac d{|S|}$．

记 $F$ 为模 $Q$ 的剩余系所对应的域，则对于一个 $L\leq n_1+n_2$，$\sum\limits_i f_{0,i,L}$ 和 $\sum\limits_i f_{1,i,L}$ 就分别对应着一个 $F$ 上关于变元集合 $\{x_{*,*}\}$ 的 $L$ 次多元多项式，不妨将这两个多项式记为 $P_0,P_1$．

假如两个不同的字符串多重集的哈希值相同，则有两种可能：

1.  $P_0\equiv P_1\pmod {Q}$，即 $P_0,P_1$ 的每一项系数在模 $Q$ 意义下都对应相等．
2.  $P_0\not\equiv P_1\pmod {Q}, P_0(x_{*,*})\equiv P_1(x_{*,*})\pmod {Q}$，即 $P_0,P_1$ 虽然不恒等，但我们选取的这一组 $\{x_{*,*}\}$ 恰好使得它们在此处的点值相等．

分析前者发生的概率：

-   观察：对于任意的 $A\neq B; A,B\leq N$ 和随机选取的质数 $Q\leq Q_{\max}$，一定有：

$$
\mathrm{Pr}\big[A\equiv B\pmod {Q}\big]=O\Big(\dfrac{\log N \log Q_{max}}{Q_{max}}\Big)
$$

-   这是因为：使 $A\equiv B$ 成立的 $Q$ 一定满足 $Q\big|(A-B)$，这样的 $Q$ 有 $\omega(A-B)\leq \log_2 N$ 个；而由质数定理，$Q_{\max}$ 以内不同的质数又有 $\Theta\Big(\dfrac {Q_{\max}}{\log Q_{\max}}\Big)$ 个．将两者相除即可得到上式．
-   在上述观察中取 $A,B$（满足 $A\neq B$）为某一特定项在 $P_0,P_1$ 中的系数（也就等于该项对应的串在 $G_0,G_1$ 中的出现次数），则易见 $A,B\leq (m_1+m_2)^{L}$，得到：

$$
\mathrm{Pr}\big[A\equiv B\pmod {Q}\big]=O\Big(\dfrac{L\log (m_1+m_2) \log Q_{max}}{Q_{max}}\Big)
$$

-   所以取 $Q_{\max}\approx 10^{12}$ 就绰绰有余．如果机器无法支持这么大的整数运算，可以用双哈希代替．

分析后者发生的概率：

-   在 Schwartz–Zippel 引理中：
    -   取域 $F$ 为模 $Q$ 的剩余系对应的域
    -   取 $f(x_{*,*})=P_0(x_{*,*})-P_1(x_{*,*})$ 为 $L$ 次非零多项式
    -   取 $S=F$
-   得到：所求概率 $\leq \dfrac LQ$．

注意到我们需要对每个 $L$ 都能保证正确性，所以要想保证严谨的话还需用 Union Bound（见后文）说明一下．

实践上我们不必随机选取模数，因为——比如说——用自己的生日做模数的话，实际上已经相当于随机数了．

### 例：（\*）子矩阵不同元素个数

???+ note "问题"
    给定 $n\times m$ 的矩阵，$q$ 次询问一个连续子矩阵中不同元素的个数，要求在线算法．
    
    允许 $\epsilon$ 的相对误差和 $\delta$ 的错误率，换句话说，你要对至少 $(1-\delta)q$ 个询问给出离正确答案相对误差不超过 $\epsilon$ 的回答．
    
    $n\cdot m\leq 2\cdot10^5;q\leq 10^6;\epsilon=0.5,\delta=0.2$

引理：令 $X_{1\cdots k}$ 为互相独立的随机变量，且取值在 $[0,1]$ 中均匀分布，则 $\mathrm{E}\big[\min\limits_i X_i\big]=\dfrac 1{k+1}$．

-   证明：考虑一个单位圆，其上分布着 **相对位置** 均匀随机的 $k+1$ 个点，分别在位置 $0,X_1,X_2,\cdots,X_k$ 处．那么 $\min\limits_i X_i$ 就等于 $k+1$ 段空隙中特定的一段的长度．而因为这些空隙之间是「对称」的，所以其中任何一段特定空隙的期望长度都是 $\dfrac 1{k+1}$．

我们取 $k$ 为不同元素的个数，并借助上述引理来从 $\min\limits_i X_i$ 反推得到 $k$．

考虑采用某个哈希函数，将矩阵中每个元素都均匀、独立地随机映射到 $[0,1]$ 中的实数上去，且相等的元素会映射到相等的实数．这样的话，一个子矩阵中的所有元素对应的那些实数，在去重后就恰好是先前的集合 $\{X_1,\cdots,X_k\}$ 的一个实例，其中 $k$ 等于子矩阵中不同元素的个数．

于是我们得到了算法：

1.  给矩阵中元素赋 $[0,1]$ 中的哈希值．为保证随机性，哈希函数可以直接用 `map` 和随机数生成器实现，即每遇到一个新的未出现过的值就给它随机一个哈希值．
2.  回答询问时设法求出子矩阵中哈希值的最小值 $M$，并输出 $\dfrac 1M-1$．

然而，这个算法并不能令人满意．它的输出值的期望是 $\mathrm{E}\Big[\dfrac 1{\min\limits_i X_i}-1\Big]$，但事实上这个值并不等于 $\dfrac 1{\mathrm{E}\big[\min\limits_i X_i\big]}-1=k$，而（可以证明）等于 $\infty$．

也就是说，我们不能直接把 $\min\limits_i X_i$ 的单次取值放在分母上，而要先算得它的期望，再把期望值放在分母上．

怎么算期望值？多次随机取平均．

我们用 $C$ 组不同的哈希函数分别执行前述过程，回答询问时计算出 $C$ 个不同的 $M$ 值，并算出其平均数 $\overline M$，然后输出 $\big(\overline M\big)^{-1}-1$．

实验发现取 $C\approx 80$ 即可满足要求．严格证明十分繁琐，在此略去．

最后，怎么求子矩阵最小值？用二维 S-T 表即可，预处理 $O(nm\log n\log m)$，回答询问 $O(1)$．

## 随机化在算法中的其他应用

随机化的其他作用还包括：

-   防止被造数据者用针对性数据卡掉．例如在搜索时随机打乱邻居的顺序．
-   保证算法过程中进行的「操作」具有（某种意义上的）均匀性．例如 [模拟退火](../misc/simulated-annealing.md) 算法．

在这些场景下，随机化常常（但并不总是）与乱搞、骗分等做法挂钩．

### 例：[「TJOI2015」线性代数](https://loj.ac/problem/2100)

本题的标准算法是网络流，但这里我们采取这样的乱搞做法：

-   每次随机一个位置，把这个位置取反，判断大小并更新答案．

??? note "代码"
    ```cpp
    #include <algorithm>
    #include <cstdlib>
    #include <iostream>
    
    int n;
    
    int a[510], b[510], c[510][510], d[510];
    int p[510], q[510];
    
    int maxans = 0;
    
    void check() {
      memset(d, 0, sizeof d);
      int nowans = 0;
      for (int i = 1; i <= n; i++)
        for (int j = 1; j <= n; j++) d[i] += a[j] * c[i][j];
      for (int i = 1; i <= n; i++) nowans += (d[i] - b[i]) * a[i];
      maxans = std::max(maxans, nowans);
    }
    
    int main() {
      srand(19260817);
      std::cin >> n;
      for (int i = 1; i <= n; i++)
        for (int j = 1; j <= n; j++) std::cin >> c[i][j];
      for (int i = 1; i <= n; i++) std::cin >> b[i];
      for (int i = 1; i <= n; i++) a[i] = 1;
      check();
      for (int T = 1000; T; T--) {
        int tmp = rand() % n + 1;
        a[tmp] ^= 1;
        check();
      }
      std::cout << maxans << '\n';
    }
    ```

### 例：（\*）随机堆[^ref3]

可并堆最常用的写法应该是左偏树了，通过维护树高让树左偏来保证合并的复杂度．然而维护树高有点麻烦，我们希望尽量避开．

那么可以考虑使用随机堆，即不按照树高来交换儿子，而是随机交换．

???+ note "代码"
    ```cpp
    struct Node {
      int child[2];
      long long val;
    } nd[100010];
    
    int root[100010];
    
    int merge(int u, int v) {
      if (!(u && v)) return u | v;
      int x = rand() & 1, p = nd[u].val > nd[v].val ? u : v;
      nd[p].child[x] = merge(nd[p].child[x], u + v - p);
      return p;
    }
    
    void pop(int &now) { now = merge(nd[now].child[0], nd[now].child[1]); }
    ```

随机堆对堆的形态没有任何硬性或软性的要求，合并操作的期望复杂度对任何两个堆（作为 `merge` 函数的参数）都成立．下证．

???+ note "期望复杂度的证明"
    将证，对于任意的堆 $A$，从根节点开始每次随机选左或者右走下去（直到无路可走），路径长度（即路径上的结点数）的期望值 $h(A)\leq\log_2 (|A|+1)$．
    
    -   注意到在前述过程中合并堆 $A,B$ 的期望复杂度是 $O\big(h(A)+h(B)\big)$ 的，所以上述结论可以保证随机堆的期望复杂度．
    
    证明采用数学归纳．边界情况是 $A$ 为空图，此时显然．下设 $A$ 非空．
    
    假设 $A$ 的两个子树分别为 $L,R$，则：
    
    $$
    \begin{align} h(A)
    &=1+\frac{h(L)+h(R)}2
    \\&\leq1+\frac{\log_2(|L|+1)+\log_2(|R|+1)}2
    \\&=\log_2{2\sqrt{(|L|+1)(|R|+1)}}
    \\&\leq\log_2{\frac{2\big((|L|+1)+(|R|+1)\big)}2}
    \\&=\log_2{(|A|+1)} \end{align}
    $$
    
    证毕．

## 与随机性有关的证明技巧

以下列举几个比较有用的技巧．

自然，这寥寥几项不可能就是全部；如果你了解某种没有列出的技巧，那么欢迎补充．

### 概率上界的分析

详见 [概率不等式](../math/probability/concentration-inequality.md) 页面．

除了上述页面中提到的各种不等式外，推导过程中还经常会用到以下结论：

**自然常数的使用**：$\Big(1-\dfrac{1}{n}\Big)^n\leq \dfrac{1}{\mathrm{e}},\forall n\geq1$

-   左式关于 $n\geq 1$ 单调递增且在 $+\infty$ 处的极限是 $\dfrac{1}{\mathrm{e}}$，因此有这个结论．
-   这告诉我们，如果 $n$ 个互相独立的事件，每个的发生概率为 $1-\dfrac 1n$，则它们全部发生的概率至多为 $\dfrac{1}{\mathrm{e}}$．

### 「耦合」思想

「耦合」思想常用于同时处理超过一个有随机性的对象，或者同时处理随机的对象和确定性的对象．

#### 引子：随机图的连通性

???+ note "问题"
    对于 $n \in \mathbf{N}^*; p,q\in [0,1]$ 且 $q\leq p$，求证：随机图 $G_1(n,p)$ 的连通分量个数的期望值不超过随机图 $G_2(n,q)$ 的连通分量个数的期望值．这里 $G(n,\alpha)$ 表示一张 $n$ 个结点的简单无向图 $G$，其中 $\dfrac {n(n-1)}2$ 条可能的边中的每一条都有 $\alpha$ 的概率出现，且这些概率互相独立．

这个结论看起来再自然不过，但严格证明却并不那么容易．

???+ note "证明思路"
    我们假想这两张图分别使用了一个 01 随机数生成器来获知每条边存在与否，其中 $G_1$ 的生成器 $T_1$ 每次以 $p$ 的概率输出 1，$G_2$ 的生成器 $T_2$ 每次以 $q$ 的概率输出 1．这样，要构造一张图，就只需把对应的生成器运行 $\dfrac {n(n-1)}2$ 遍即可．
    
    现在我们把两个生成器合二为一．考虑随机数生成器 $T$，每次以 $q$ 的概率输出 0，以 $p-q$ 的概率输出 1，以 $1-p$ 的概率输出 2．如果我们将这个 $T$ 运行 $\dfrac {n(n-1)}2$ 遍，就能同时构造出 $G_1$ 和 $G_2$．具体地说，如果输出是 0，则认为 $G_1$ 和 $G_2$ 中都没有当前考虑的边；如果输出是 1，则认为只有 $G_1$ 中有当前考虑的边；如果输出是 2，则认为 $G_1$ 和 $G_2$ 中都有当前考虑的边．
    
    容易验证，这样生成的 $G_1$ 和 $G_2$ 符合其定义，而且在每个实例中，$G_2$ 的边集都是 $G_1$ 边集的子集．因此在每个实例中，$G_2$ 的连通分量个数都不小于 $G_1$ 的连通分量个数；那么期望值自然也满足同样的大小关系．

这一段证明中用到的思想被称为「耦合」，可以从字面意思来理解这种思想．本例中它体现为把两个本来独立的随机过程合二为一．

#### 应用：[NERC 2019 Problem G: Game Relics](https://codeforces.com/contest/1267/problem/G)

???+ note "简要题意"
    有若干个物品，每个物品有一个价格 $c_i$．你想要获得所有物品，为此你可以任意地进行两种操作：
    
    1.  选择一个未拥有的物品 $i$，花 $c_i$ 块钱买下来．
    2.  花 $x$ 块钱从所有物品（包括已经拥有的）中等概率随机抽取一个．如果尚未拥有该物品，则直接获得它；否则一无所获，但是会返还 $\dfrac x2$ 块钱．$x$ 为输入的常数．
    
    问最优策略下的期望花费．

观察：如果选择抽物品，就一定会一直抽直到获得新物品为止．

-   理由：如果抽一次没有获得新物品，则新的局面和抽物品之前的局面一模一样，所以如果旧局面的最优行动是「抽一发」，则新局面的最优行动一定也是「再抽一发」．

我们可以计算出 $f_k$ 表示：如果当前已经拥有 $k$ 个不同物品，则期望要花多少钱才能抽到新物品．根据刚才的观察，我们可以直接把 $f_k$ 当作一个固定的代价，即转化为「每次花 $f_k$ 块钱随机获得一个新物品」．

???+ note "期望代价的计算"
    显然 $f_k=\dfrac x2 \cdot (R-1)+x$，其中 $R$ 表示要得到新物品期望的抽取次数．
    
    引理：如果一枚硬币有 $p$ 的概率掷出正面，则首次掷出正面所需的期望次数为 $\dfrac 1p$．
    
    -   感性理解：$\dfrac 1p \cdot p = 1$，所以扔这么多次期望得到 1 次正面，看起来就比较对．
    -   这种感性理解可以通过 [大数定律](https://en.wikipedia.org/wiki/Law_of_large_numbers) 严谨化，即考虑 $n\to \infty$ 次「不断抛硬币直到得到正面」的实验．推导细节略．
    -   另一种可行的证法是，直接把期望的定义带进去暴算．推导细节略．
    
    显然抽一次得到新物品的概率是 $\dfrac {n-k}n$，那么 $R=\dfrac n{n-k}$．

结论：最优策略一定是先抽若干次，再买掉所有没抽到的物品．

这个结论符合直觉，因为 $f_k$ 是关于 $k$ 递增的，早抽似乎确实比晚抽看起来好一点．

???+ note "证明"
    先考虑证明一个特殊情况．将证：
    
    -   随机过程 $A$：先买物品 $x$，然后不断抽直到得到所有物品
    -   ……一定不优于……
    -   随机过程 $B$：不断抽直到得到 $x$ 以外的所有物品，然后如果还没有 $x$ 则买下来
    
    考虑让随机过程 $A$ 和随机过程 $B$ 使用同一个随机数生成器．即，$A$ 的第一次抽取和 $B$ 的第一次抽取会抽到同一个元素，第二次、第三次……也是一样．
    
    显然，此时 $A$ 和 $B$ 抽取的次数必定相等．对于一个被 $A$ 抽到的物品 $y\neq x$，观察到：
    
    -   $A$ 中抽到 $y$ 时已经持有的物品数，一定大于等于 $B$ 中抽到 $y$ 时已经持有的物品数．
    
    因此 $B$ 的单次抽取代价不高于 $A$ 的单次抽取代价，进而抽取的总代价也不高于 $A$．
    
    显然 $B$ 的购买代价同样不高于 $A$．综上，$B$ 一定不劣于 $A$．
    
    然后可以通过数学归纳把这一结论推广到一般情况．具体地说，每次我们找到当前策略中的最后一次购买，然后根据上述结论，把这一次购买移到最后一定不劣．细节略．

基于这个结论，我们再次等价地转化问题：把「选一个物品并支付对应价格购买」的操作，改成「随机选一个未拥有的物品并支付对应价格购买」．等价性的理由是，既然购买只是用来扫尾的，那选到哪个都无所谓．

现在我们发现，「抽取」和「购买」，实质上已经变成了相同的操作，区别仅在于付出的价格不同．选择购买还是抽取，对于获得物品的顺序毫无影响，而且每种获得物品的顺序都是等可能的．

观察：在某一时刻，我们应当选择买，当且仅当下一次抽取的代价（由已经抽到的物品数确定）大于剩余物品的平均价格（等于的话则任意）．

-   可以证明，随着时间的推移，抽取代价的增速一定不低于剩余物品均价的增速．这说明从抽到买的「临界点」只有一个，进一步验证了先前结论．

最后，我们枚举所有可能的局面（即已经拥有的元素集合），算出这种局面出现的概率（已有元素的排列方案数除以总方案数），乘上当前局面最优决策的代价（由拥有元素个数和剩余物品总价确定），再加起来即可．这个过程可以用背包式的 DP 优化，即可通过本题．

***

**回顾**：可以看到，耦合的技巧在本题中使用了两次．第一次是在证明过程中，令两个随机过程使用同一个随机源；第二次是把购买转化成随机购买（即引入随机源），从而使得购买和抽取这两种操作实质上「耦合」为同一种操作（即令抽取和购买操作共享一个随机源）．

## 参考资料

[^ref1]: [PANIC - Editorial](https://discuss.codechef.com/t/panic-editorial/80145)

[^ref2]: [UOJ NOI Round #4 Day2 题解](https://peehs-moorhsum.blog.uoj.ac/blog/6375)

[^ref3]: [Anna Gambin and Adam Malinowski, Randomized Meldable Priority Queues](https://www.researchgate.net/publication/2801527_Randomized_Meldable_Priority_Queues)


## misc/random.md

## 概述

要想使用随机化技巧，前提条件是能够快速生成随机数．本文将介绍生成随机数的常见方法．

### 随机数与伪随机数

说一个单独的数是「随机数」是无意义的，所以以下我们都默认讨论「随机数列」，即使提到「随机数」，指的也是「随机数列中的一个元素」．

现有的计算机的运算过程都是确定性的，因此，仅凭借算法来生成真正 **不可预测**、**不可重复** 的随机数列是不可能的．

然而在绝大部分情况下，我们都不需要如此强的随机性，而只需要所生成的数列在统计学上具有随机数列的种种特征（比如均匀分布、互相独立等等）．这样的数列即称为 **伪随机数** 序列．

随机数与伪随机数在实际生活和算法中的应用举例：

-   抽样调查时往往只需使用伪随机数．这是因为我们本就只关心统计特征．
-   网络安全中往往要用到（比刚刚提到的伪随机数）更强的随机数．这是因为攻击者可能会利用可预测性做文章．
-   OI/ICPC 中用到的随机算法，基本都只需要伪随机数．这是因为，这些算法往往是通过引入随机数来把概率引入复杂度分析，从而降低复杂度．这本质上依然只利用了随机数的统计特征．
-   某些随机算法（例如 [Moser 算法](https://en.wikipedia.org/wiki/Algorithmic_Lov%C3%A1sz_local_lemma)）用到了随机数的熵相关的性质，因此必须使用真正的随机数．

## 随机数生成方法

### `rand`

用于生成伪随机数，缺点是比较慢，使用时需要 `#include<cstdlib>`．

调用 `rand()` 函数会返回一个 `[0,RAND_MAX]` 中的随机非负整数，其中 `RAND_MAX` 是标准库中的一个宏，在 Linux 系统下 `RAND_MAX` 等于 $2^{31}-1$．可以用取模来限制所生成的数的大小．

使用 `rand()` 需要一个随机数种子，可以使用 `srand(seed)` 函数来将随机种子更改为 `seed`，当然不初始化也是可以的．

同一程序使用相同的 `seed` 两次运行，在同一机器、同一编译器下，随机出的结果将会是相同的．

有一个选择是使用当前系统时间来作为随机种子：`srand(time(nullptr))`．

??? warning "Warning"
    在 `Windows` 系统下 `rand()` 返回值的取值范围为 $\left[0,2^{15}\right)$（即 `RAND_MAX` 等于 $2^{15}-1$），当需要生成的数不小于 $2^{15}$ 时建议使用 `(rand() << 15 | rand())` 来生成更大的随机数．

关于 `rand()` 和 `rand()%n` 的随机性：

-   C/C++ 标准并未关于 `rand()` 所生成随机数的任何方面的质量做任何规定．
-   GCC 对 `rand()` 所采用的实现方式，保证了分布的均匀性等基本性质，但具有低位周期长度短等明显缺陷．（例如在笔者的机器上，`rand()%2` 所生成的序列的周期长约 $2\cdot 10^6$）
-   即使假设 `rand()` 是均匀随机的，`rand()%n` 也不能保证均匀性，因为 `[0,n)` 中的每个数在 `0%n,1%n,...,RAND_MAX%n` 中的出现次数可能不相同．严格保证均匀性的做法可参考 [Daniel Lemire, Fast Random Integer Generation in an Interval](https://arxiv.org/abs/1805.10941)．

### 预定义随机数生成器

定义了数个特别的流行算法．如没有特别说明，均定义于头文件 `<random>`．

??? warning "Warning"
    预定义随机数生成器于 C++11 标准[^ref2]开始使用．

#### 梅森缠绕器

梅森缠绕器（Mersenne Twister）由松本与西村于 1998 年提出[^ref3]，因其中一种实现 MT19937 具有梅森素数 $M_{19937} = 2^{19937} - 1$ 这么长的周期而得名．

从 C++11 开始，模板类 `std::mersenne_twister_engine` 实现基于如上方法的随机数生成器．因其使用起来十分复杂，通常实际使用的是该模板类的特化：`std::mt19937` 和 `std::mt19937_64`．其优点是随机数质量高，且速度比 `rand()` 快很多．

`mt19937` 基于 32 位梅森缠绕器，由松本与西村于 1998 年提出[^ref3]，是一个随机数生成器类，效用同 `rand()`，随机数的范围同 `unsigned int` 类型的取值范围．使用时用其定义一个随机数生成器即可：`mt19937 myrand(seed)`，`seed` 可不填，不填 `seed` 则会使用默认随机种子．其重载了 `operator()`，需要生成随机数时调用 `myrand()` 即可返回一个随机数．

另一个类似的生成器是 `mt19937_64`，基于 64 位梅森缠绕器，由松本与西村于 2000 年提出，使用方式同 `mt19937`，但随机数范围扩大到了 `unsigned long long` 类型的取值范围．

??? note "代码示例"
    ```cpp
    --8<-- "docs/misc/code/random/random_1.cpp:core"
    ```

#### 线性同余随机数生成器

线性同余随机数生成器（简称 LCG）由 Thomson 和 Rotenberg 于 1958 年提出．其计算公式如下，其中 $A, C, M$ 为预定义常数：

$$
s_i \equiv \begin{cases}
\operatorname{seed} & i = 0 \\
s_{i-1} \times A + C & i \ge 1
\end{cases}\pmod{M}
$$

从 C++11 开始，模板类 `std::linear_congruential_engine` 实现基于如上方法的随机数生成器，模板参数如下：

```cpp
template <class UIntType, UIntType A, UIntType C, UIntType M>
class linear_congruential_engine;
```

这里 `UIntType` 表示 $s$ 的类型，随后是三个常数．

随后 Lewis、Goodman 及 Miller 于 1969 提出，取 $A = 7^{5} = 16807$、$C = 0$、$M = 2^{31} - 1 = 2147483647$ 时，此算法可以达到该模数下近乎最大的周期 $2^{31} - 2$（因为 $16807$ 是该模数下的 [原根](../math/number-theory/primitive-root.md)）且具有相对不错的统计特征．

之后于 1988 年，该参数的 LCG 由 Park 与 Miller 采纳为「最小标准」，只因其实现极其简单、易懂、高效、且质量相对不错．最后于 1993 年，Park、Miller 和 Stockmeyer 将参数 $A$ 改为 $48271$，成为较新的「最小标准」．两个版本的「最小标准」作为 `linear_congruential_engine` 的特化，也都于 C++11 中预定义，分别为 `minstd_rand0` 和 `minstd_rand`．具体而言：

-   对于 `minstd_rand0`，$s_i$ 的类型为 `std::uint_fast32_t`，$A$ 取 $16807$，$C$ 取 $0$，$M$ 取 $2147483647$．

-   对于 `minstd_rand`，$s_i$ 的类型为 `std::uint_fast32_t`，$A$ 取 $48271$，$C$ 取 $0$，$M$ 取 $2147483647$．

使用方法也很简单．首先定义 `std::minstd_rand myrand(seed);`，其中 `seed` 为种子，不填时默认为 $1$．然后调用 `myrand()` 即可获得一个随机数．

如果需要自定义该形式的随机数生成器，且 $A, C, M$ 不是常数，则还可以考虑手写实现．该方法实现难度低，但生成的随机序列周期长度较短（周期最大为 $M$，但大多数情况下都会比 $M$ 短）．

??? note "参考实现"
    ```cpp
    --8<-- "docs/misc/code/random/random_2.cpp"
    ```

### 随机数引擎适配器

在预定义随机数生成器的基础上，可以对其进行二次封装得到新的随机数生成器．具体类名和使用方法请参见 [伪随机数生成——随机数引擎适配器](https://zh.cppreference.com/cpp/numeric/random#.E9.9A.8F.E6.9C.BA.E6.95.B0.E5.BC.95.E6.93.8E.E9.80.82.E9.85.8D.E5.99.A8) 的列表．

下面的代码使用 `std::independent_bits_engine` 包装 `std::minstd_rand` 的输出．

```cpp
--8<-- "docs/misc/code/random/random_3.cpp"
```

### 非确定随机数的均匀分布整数随机数生成器

`random_device` 是一个基于硬件的均匀分布随机数生成器，**在熵池耗尽** 前可以高速生成随机数．该类在 C++11 定义，需要 `random` 头文件．由于熵池耗尽后性能急剧下降，所以建议用此方法生成 `mt19937` 等伪随机数的种子，而不是直接生成．

`random_device` 是非确定的均匀随机位生成器，尽管若不支持非确定随机数生成，则允许实现用伪随机数引擎实现．目前笔者尚未接到报告称 NOIP 评测机不支持基于硬件的均匀分布随机数生成．但出于保守考虑，建议使用该算法生成随机数种子．

参考代码如下．

```cpp
--8<-- "docs/misc/code/random/random_4.cpp"
```

可能的输出如下．

```plain
0 : ********************
1 : *******************
2 : ********************
3 : ********************
4 : ********************
5 : *******************
6 : ********************
7 : ********************
8 : *******************
9 : ********************
```

### 随机数分布

这里介绍的是要求生成的随机数遵从某一分布的随机数生成器，如 [离散均匀分布](https://en.wikipedia.org/wiki/Discrete_uniform_distribution)，[伯努利分布](https://en.wikipedia.org/wiki/Bernoulli_distribution)，[二项分布](https://en.wikipedia.org/wiki/Binomial_distribution)，[几何分布](https://en.wikipedia.org/wiki/Geometric_distribution)，[标准正态（高斯）分布](https://en.wikipedia.org/wiki/Normal_distribution)．

具体类名请参见 [伪随机数生成——随机数分布](https://zh.cppreference.com/w/cpp/numeric/random#.E9.9A.8F.E6.9C.BA.E6.95.B0.E5.88.86.E5.B8.83) 的列表．

下面的程序模拟了一个六面体骰子．

```cpp
--8<-- "docs/misc/code/random/random_5.cpp:header"
--8<-- "docs/misc/code/random/random_5.cpp:real-using"
--8<-- "docs/misc/code/random/random_5.cpp:fake-using"
--8<-- "docs/misc/code/random/random_5.cpp:main"
```

### 其他实现方法

有的时候我们需要实现自己的随机数生成器．下面是一些常用的随机数生成方法．

#### Xorshift

Xorshift 系列随机数生成器由 George Marsaglia 于 2003 年提出，其主要基于异或一个数的移位这一种操作．在算法竞赛中常用的版本有 `xorshift32` 和 `xorshift64` 两种：

```cpp
--8<-- "docs/misc/code/random/random_6.cpp:core"
```

使用方法与前面介绍的大多数随机数生成器类似：首先定义随机数生成器 `xorshift32 rng32(seed)` 或 `xorshift64 rng64(seed)`，其中 `seed` 为种子，不填时使用默认种子；之后调用 `rng32()` 或 `rng64()` 即可获得随机数．这两个随机数生成器在种子不为 $0$ 时分别具有 $2^{32} - 1$ 和 $2^{64} - 1$ 的周期，因其实现极其简单，常将其和种子下发给选手生成大范围的数据以减少 I/O 开销．

#### SplitMix

SplitMix 系列随机数生成器由 Stelle，Lee 和 Flood 于 2014 年提出，并应用于 Java 8 的 `java.util.SplittableRandom` 类中．在算法竞赛界最常用的版本为 `splitmix64`：

```cpp
--8<-- "docs/misc/code/random/random_7.cpp:core"
```

其最主要的用途是对一个已经求出的哈希值进行二次哈希，以防止被人通过精心构造的数据卡哈希表卡到超时：

```cpp
--8<-- "docs/misc/code/random/random_8.cpp:core"
```

其亦可用于生成随机数：首先定义 `splitmix64 rng64(seed)`，其中 `seed` 为种子，不填时使用默认种子；之后调用 `rng64()` 即可获得随机数．此时较为显然的，该函数具有 $2^{64}$ 的周期（因为所有的大数都是奇数，所以 $x$ 具有 $2^{64}$ 的周期，且后面对 $z$ 的所有操作都是完全可逆的）．这也意味着即使你记不住如上的大参数，你也可以直接随便写几个足够大的奇数结合异或右移来达到相近的效果．

#### 时滞斐波那契随机数生成器

利用下式来生成随机数序列 $\{R_i\}$（其中 $0 < j < k$）：

$$
R_i \equiv R_{i-j} \star R_{i-k} \bmod P
$$

这里的 $P$ 通常取 $2$ 的幂（常用 $2^{32}$ 或 $2^{64}$），$\star$ 表示二元运算符，可以使用加法，减法，乘法，异或．

该方法较传统的线性同余随机数生成器而言，拥有更长的周期，但随机性受初始条件影响较大．

??? note "参考实现"
    ```cpp
    --8<-- "docs/misc/code/random/random_9.cpp:core"
    ```

值得一提的是，在 C++11 中，`std::subtract_with_carry_engine` 是这一类随机数生成器的其中一种实现，而 `std::ranlux24_base` 和 `std::ranlux48_base` 是该模板类的特化，`std::ranlux24` 和 `std::ranlux48` 则是在前者的基础上再套上一个适配器 `std::discard_block_engine` 得到．不过现在通常不再推荐使用它们．

## 随机算法

下面介绍在 C++ 标准中定义的一些依赖随机数生成的随机算法．

### `random_shuffle`

`std::random_shuffle` 于 C++98 引入，用于随机打乱指定序列．使用时需要 `#include<algorithm>`，常用实现方法为 [Fisher-Yates 算法](https://en.wikipedia.org/wiki/Fisher%E2%80%93Yates_shuffle)．

使用时传入指定区间的首尾指针或迭代器（左闭右开）即可：`std::random_shuffle(first, last)` 或 `std::random_shuffle(first, last, myrand)`．

内部使用的随机数生成器默认为 `rand()`．当然也可以传入自定义的随机数生成器．

关于 `random_shuffle` 的随机性：

-   C++ 标准中要求 `random_shuffle` 在所有可能的排列中 **等概率** 随机选取，但 GCC[^note1]的默认标准库 libstdc++**并未** 严格执行．
-   GCC 中 `random_shuffle` 随机性上的缺陷的原因之一，是它使用了 `rand()%n` 这样的写法．如先前所述，这样生成的不是均匀随机的整数．
-   原因之二，是 `rand()` 的值域有限．如果所传入的区间长度超过 `RAND_MAX`，将存在某些排列 **不可能** 被产生[^ref1]．

??? warning "Warning"
    `random_shuffle` 已于 C++14 标准中被弃用，于 C++17 标准中被移除．

### `shuffle`

`std::shuffle` 于 C++11 引入，效用同 `random_shuffle`．使用时需要 `#include<algorithm>`．

区别在于必须使用自定义的随机数生成器：`std::shuffle(first, last, myrand)`．

GCC[^note1]实现的 `shuffle` 符合 C++ 标准的要求，即在所有可能的排列中等概率随机选取．

下面是用 `rand()` 及 `random_shuffle()` 编写的一个数据生成器．生成数据为 [「ZJOI2012」灾难](https://www.luogu.com.cn/problem/P2597) 的随机小数据．

```cpp
--8<-- "docs/misc/code/random/random_10.cpp:header"
--8<-- "docs/misc/code/random/random_10.cpp:real-using"
--8<-- "docs/misc/code/random/random_10.cpp:fake-using"
--8<-- "docs/misc/code/random/random_10.cpp:main"
```

下面是用 `mt19937` 及 `shuffle()` 编写的同一个数据生成器．

```cpp
--8<-- "docs/misc/code/random/random_11.cpp:header"
--8<-- "docs/misc/code/random/random_11.cpp:real-using"
--8<-- "docs/misc/code/random/random_11.cpp:fake-using"
--8<-- "docs/misc/code/random/random_11.cpp:main"
```

下面是随机排列前十个正整数的一个实现．

```cpp
--8<-- "docs/misc/code/random/random_12.cpp:header"
--8<-- "docs/misc/code/random/random_12.cpp:real-using"
--8<-- "docs/misc/code/random/random_12.cpp:fake-using"
--8<-- "docs/misc/code/random/random_12.cpp:main"
```

### `sample`

`std::sample` 于 C++17 引入，用于从序列里随机选择其中 $n$ 个元素，与 `shuffle` 后提取前 $n$ 个元素的主要区别在于选出来的元素输出后仍保持相对顺序．常用实现方法为 [蓄水池抽样法](https://en.wikipedia.org/wiki/Reservoir_sampling)．

使用方法为 `std::sample(first, last, dest, n, myrand)`，其中 `[first, last)` 表示要采样的范围，`[dest, dest + n)` 表示要输出到的地方，`myrand` 是指定的随机数生成器．

下面是从 11 个大写字母里随机抽取 4 个的实现．

```cpp
--8<-- "docs/misc/code/random/random_13.cpp:header"
--8<-- "docs/misc/code/random/random_13.cpp:real-using"
--8<-- "docs/misc/code/random/random_13.cpp:fake-using"
--8<-- "docs/misc/code/random/random_13.cpp:main"
```

## 参考资料与注释

[^ref1]: [Don't use rand(): a guide to random number generators in C++](https://codeforces.com/blog/entry/61587)

[^ref2]: [伪随机数生成 - cppreference.com](https://zh.cppreference.com/w/cpp/numeric/random#%E9%A2%84%E5%AE%9A%E4%B9%89%E9%9A%8F%E6%9C%BA%E6%95%B0%E7%94%9F%E6%88%90%E5%99%A8)

[^ref3]: [Mersenne Twister algorithm](https://en.wikipedia.org/wiki/Mersenne_Twister)

[^note1]: 版本号为 GCC 9.2.0


## misc/rollback-mo-algo.md

author: StudyingFather, Backl1ght, countercurrent-time, Ir1d, greyqz, MicDZ, ouuan, YOYO-UIAT

## 引入

有些题目在区间转移时，可能会出现增加或者删除无法实现的问题．在只有增加不可实现或者只有删除不可实现的时候，就可以使用回滚莫队在 $O(n \sqrt m)$ 的时间内解决问题．回滚莫队的核心思想就是：既然只能实现一个操作，那么就只使用一个操作，剩下的交给回滚解决．

回滚莫队分为只使用增加操作的回滚莫队和只使用删除操作的回滚莫队．以下仅介绍只使用增加操作的回滚莫队，只使用删除操作的回滚莫队和只使用增加操作的回滚莫队只在算法实现上有一点区别，故不再赘述．

## 例题 [JOISC 2014 Day1 历史研究](https://loj.ac/problem/2874)

给你一个长度为 $n$ 的数组 $A$ 和 $m$ 个询问 $(1 \leq n, m \leq 10^5)$，每次询问一个区间 $[L, R]$ 内重要度最大的数字，要求 **输出其重要度**．一个数字 $i$ 重要度的定义为 $i$ 乘上 $i$ 在区间内出现的次数．

在这个问题中，在增加的过程中更新答案是很好实现的，但是在删除的过程中更新答案是不好实现的．因为如果增加会影响答案，那么新答案必定是刚刚增加的数字的重要度，而如果删除过后区间重要度最大的数字改变，我们很难确定新的重要度最大的数字是哪一个．所以，普通的莫队很难解决这个问题．

## 过程

-   对原序列进行分块，对询问按以左端点所属块编号升序为第一关键字，右端点升序为第二关键字的方式排序．
-   按顺序处理询问：
    -   如果询问左端点所属块 $B$ 和上一个询问左端点所属块的不同，那么将莫队区间的左端点初始化为 $B$ 的右端点加 $1$, 将莫队区间的右端点初始化为 $B$ 的右端点；
    -   如果询问的左右端点所属的块相同，那么直接扫描区间回答询问；
    -   如果询问的左右端点所属的块不同：
        -   如果询问的右端点大于莫队区间的右端点，那么不断扩展右端点直至莫队区间的右端点等于询问的右端点；
        -   不断扩展莫队区间的左端点直至莫队区间的左端点等于询问的左端点；
        -   回答询问；
        -   撤销莫队区间左端点的改动，使莫队区间的左端点回滚到 $B$ 的右端点加 $1$．

## 复杂度证明

假设回滚莫队的分块大小是 $b$：

-   对于左、右端点在同一个块内的询问，可以在 $O(b)$ 时间内计算；
-   对于其他询问，考虑左端点在相同块内的询问，它们的右端点单调递增，移动右端点的时间复杂度是 $O(n)$，而左端点单次询问的移动不超过 $b$，因为有 $\frac{n}{b}$ 个块，所以总复杂度是 $O(mb+\frac{n^2}{b})$，取 $b=\frac{n}{\sqrt{m}}$ 最优，时间复杂度为 $O(n\sqrt{m})$．

## 实现

??? note "参考代码"
    ```cpp
    --8<-- "docs/misc/code/rollback-mo-algo/rollback-mo-algo_1.cpp"
    ```

## 参考资料

-   [回滚莫队及其简单运用 | Parsnip's Blog](https://www.cnblogs.com/Parsnip/p/10969989.html)


## misc/simulated-annealing.md

## 引入

模拟退火是一种随机化算法．当一个问题的方案数量极大（甚至是无穷的）而且不是一个单峰函数时，我们常使用模拟退火求解．

## 解释

根据 [爬山算法](./hill-climbing.md) 的过程，我们发现：对于一个当前最优解附近的非最优解，爬山算法直接舍去了这个解．而很多情况下，我们需要去接受这个非最优解从而跳出这个局部最优解，即为模拟退火算法．

??? note "什么是退火？（选自 [百度百科](https://baike.baidu.com/item/%E9%80%80%E7%81%AB/1039313)）"
    退火是一种金属热处理工艺，指的是将金属缓慢加热到一定温度，保持足够时间，然后以适宜速度冷却．目的是降低硬度，改善切削加工性；消除残余应力，稳定尺寸，减少变形与裂纹倾向；细化晶粒，调整组织，消除组织缺陷．准确的说，退火是一种对材料的热处理工艺，包括金属材料、非金属材料．而且新材料的退火目的也与传统金属退火存在异同．

由于退火的规律引入了更多随机因素，那么我们得到最优解的概率会大大增加．于是我们可以去模拟这个过程，将目标函数作为能量函数．

### 过程

先用一句话概括：如果新状态的解更优则修改答案，否则以一定概率接受新状态．

我们定义当前温度为 $T$，新状态 $S'$ 与已知状态 $S$（新状态由已知状态通过随机的方式得到）之间的能量（值）差为 $\Delta E$（$\Delta E\geqslant 0$），则发生状态转移（修改最优解）的概率为

$$
P(\Delta E)=
\begin{cases}
1,                              & S' \text{ is better than } S,\\
\mathrm{e}^\frac{-\Delta E}{T}, & \text{otherwise}.
\end{cases}
$$

**注意**：我们有时为了使得到的解更有质量，会在模拟退火结束后，以当前温度在得到的解附近多次随机状态，尝试得到更优的解（其过程与模拟退火相似）．

### 如何退火（降温）

模拟退火时我们有三个参数：初始温度 $T_0$，降温系数 $d$，终止温度 $T_k$．其中 $T_0$ 是一个比较大的数，$d$ 是一个非常接近 $1$ 但是小于 $1$ 的数，$T_k$ 是一个接近 $0$ 的正数．

首先让温度 $T=T_0$，然后按照上述步骤进行一次转移尝试，再让 $T=d\cdot T$．当 $T<T_k$ 时模拟退火过程结束，当前最优解即为最终的最优解．

注意为了使得解更为精确，我们通常不直接取当前解作为答案，而是在退火过程中维护遇到的所有解的最优值．

引用一张 [Simulated annealing - Wikipedia](https://en.wikipedia.org/wiki/Simulated_annealing) 的图片（随着温度的降低，跳跃越来越不随机，最优解也越来越稳定）．

![](./images/simulated-annealing.gif)

## 实现

此处代码以 [「BZOJ 3680」吊打 XXX](https://hydro.ac/p/bzoj-P3680)（求 $n$ 个点的带权类费马点）为例．

```cpp
--8<-- "docs/misc/code/simulated-annealing/simulated-annealing_1.cpp"
```

## 一些技巧

### 分块模拟退火

有时函数的峰很多，模拟退火难以跑出最优解．

此时可以把整个值域分成几段，每段跑一遍模拟退火，然后再取最优解．

### 卡时

有一个 `clock()` 函数，返回程序运行时间．

可以把主程序中的 `simulateAnneal();` 换成 `while ((double)clock()/CLOCKS_PER_SEC < MAX_TIME) simulateAnneal();`．这样子就会一直跑模拟退火，直到用时即将超过时间限制．

这里的 `MAX_TIME` 是一个自定义的略小于时限的数（单位：秒）．

## 习题

-   [「BZOJ 3680」吊打 XXX](https://hydro.ac/p/bzoj-P3680)
-   [「JSOI 2016」炸弹攻击](https://loj.ac/problem/2076)
-   [「HAOI 2006」均分数据](https://www.luogu.com.cn/problem/P2503)


## misc/space-optimization.md

空间优化相关技巧在算法竞赛中不太常见，但仍有讨论价值．

## 信息熵

信息熵描述了存储数据所占用的空间下限，若实际可用的空间低于这个下限则必然损失信息．

???+ note "定义"
    对随机变量 $X$，定义信息熵为
    
    $$
    H(X)=-\sum_{x}P(X=x)\log_2 P(X=x).
    $$

定义中对数底数为 $2$ 是因为计算机中存储的信息每位只有 $2$ 种取值：$0$ 和 $1$．

例如设 $X$ 服从 $\{1,2,\dots,n\}$ 上的均匀分布，则其信息熵为

$$
H(X)=-\sum_{i=1}^n\frac{1}{n}\log_2\frac{1}{n}=\log_2 n,
$$

所以我们至少需要 $\log_2 n$ 位来存储 $1$ 到 $n$ 的整数．

### 例题

???+ note "[\[WC2022\] 猜词](https://www.luogu.com.cn/problem/P8079)"
    交互题，你需要在有限次数内猜一个 5 个字母的单词．每次猜测都需要猜一个词库中存在的单词．如果猜对了，游戏结束；在每次猜错后，交互库会返回哪些字母的位置是正确的，以及哪些字母在待猜单词中出现了但位置是错误的．
    
    ??? note "解法"
        参见 [用信息论解 Wordle 谜题 - 3Blue1Brown](https://www.bilibili.com/video/BV1zZ4y1k7Jw)．
        
        考虑计算信息熵，显然每次猜词时选择信息熵高的词可使得期望猜词次数尽可能小．
        
        由于本题在猜测之前给出了答案首字母，所以我们可以预处理出每种首字母的最优猜测．
        
        另外若剩余的词很少的话，我们可以考虑优先输出可能是答案的词，从而减小次数．

## 常见技巧

### 避免存储不必要的数据

例如：

-   在 [可持久化线段树](../ds/persistent-seg.md) 中，由于单次修改只会产生 $O(\log n)$ 个新结点，所以我们不需要把每个版本的线段树都完整地存储下来，只需要记录新结点即可．
-   考虑 [图的存储](../graph/save.md)，对稀疏图来说，若使用邻接矩阵则会存储大量无用的 $0$，所以一般使用邻接表存稀疏图．
-   `bool` 数组的每个元素均会占用一个字节的空间，必要时可用每个元素只占用一位的 `std::vector<bool>` 或 [bitset](../lang/csl/bitset.md) 代替．
-   在 [背包 DP](../dp/knapsack.md) 中，对 01 背包而言，每次计算 DP 值只会用到上一次计算时的数据，所以我们可以用滚动数组优化空间，只需要记录当前 DP 值即可．

### 利用数据特性

考虑支持路径压缩和启发式合并的 [并查集](../ds/dsu.md)，传统做法需要两个数组，分别记录父结点编号和子树大小．

注意到：

1.  在应用了路径压缩后，对于并查集中的一棵树，我们只需要记录根结点对应的子树大小．
2.  根结点的父亲一定是自己．

我们可以利用有符号整数的特性，用负数表示根结点，正数表示非根结点，所以我们只需一个数组即可实现支持路径压缩和启发式合并的并查集．

???+ note "实现"
    ```cpp
    --8<-- "docs/misc/code/space-optimization/space-optimization_1.cpp"
    ```

## 习题

-   [QOJ 6669 Mapa](https://qoj.ac/problem/6669)
-   [\[SDOI/SXOI2022\] 无处存储](https://www.luogu.com.cn/problem/P8353)

## 参考资料与拓展阅读

1.  陈知轩．《浅谈信息学竞赛中的空间优化问题》．2022 国家集训队论文
2.  [Information theory - Wikipedia](https://en.wikipedia.org/wiki/Information_theory)
3.  [浅谈信息论 - 洛谷专栏](https://www.luogu.com.cn/article/i65ca8i5)


## misc/two-pointer.md

本页面将简要介绍双指针．

## 引入

双指针是一种简单而又灵活的技巧和思想，单独使用可以轻松解决一些特定问题，和其他算法结合也能发挥多样的用处．

双指针顾名思义，就是同时使用两个指针，在序列、链表结构上指向的是位置，在树、图结构中指向的是节点，通过或同向移动，或相向移动来维护、统计信息．

接下来我们来看双指针的几个具体使用方法．

## 维护区间信息

如果不和其他数据结构结合使用，双指针维护区间信息的最简单模式就是维护具有一定单调性，新增和删去一个元素都很方便处理的信息，就比如正数的和、正整数的积等等．

### 例题 1

???+ note "例题 1 [leetcode 713. 乘积小于 K 的子数组](https://leetcode-cn.com/problems/subarray-product-less-than-k/)"
    给定一个长度为 $n$ 的正整数数组 $\mathit{nums}$ 和整数 $k$，找出该数组内乘积小于 $k$ 的连续子数组的个数．
    
    其中，$1 \leq n \leq 3 \times 10^4, 1 \leq nums[i] \leq 1000, 0 \leq k \leq 10^6$．

#### 过程

设两个指针分别为 $l,r$，另外设置一个变量 $\mathit{tmp}$ 记录 $[l,r]$ 内所有数的乘积．最开始 $l,r$ 都在最左面，先向右移动 $r$，直到第一次发现 $\mathit{tmp}\geq k$，这时就固定 $r$，右移 $l$，直到 $\mathit{tmp}\lt k$．那么对于每个 $r$，$l$ 是它能延展到的左边界，由于正整数乘积的单调性，此时以 $r$ 为右端点的满足题目条件的区间个数为 $r-l+1$ 个．

#### 实现

```cpp
int numSubarrayProductLessThanK(vector<int>& nums, int k) {
  long long ji = 1ll, ans = 0;
  int l = 0;
  for (int i = 0; i < nums.size(); ++i) {
    ji *= nums[i];
    while (l <= i && ji >= k) ji /= nums[l++];
    ans += i - l + 1;
  }
  return ans;
}
```

使用双指针维护区间信息也可以与其他数据结构比如差分、单调队列、线段树、主席树等等结合使用．另外将双指针技巧融入算法的还有莫队，莫队中将询问离线排序后，一般也都是用两个指针记录当前要处理的区间，随着指针一步步移动逐渐更新区间信息．

### 例题 2

接下来看一道在树上使用双指针并结合树上差分的例题：

???+ note "例题 2 [luogu P3066 Running Away From the Barn G](https://www.luogu.com.cn/problem/P3066)"
    给定一颗 $n$ 个点的有根树，边有边权，节点从 1 至 $n$ 编号，1 号节点是这棵树的根．再给出一个参数 $t$，对于树上的每个节点 $u$，请求出 $u$ 的子树中有多少节点满足该节点到 $u$ 的距离不大于 $t$．数据范围：$1\leq n \leq 2\times 10^5,1 \leq t \leq 10^{18},1 \leq p_i \lt i,1 \leq w_i \leq 10^{12}$

#### 过程

从根开始用 dfs 遍历整棵树，使用一个栈来记录根到当前节点的树链，设一个指针 $u$ 指向当前节点，另一个指针 $p$ 指向与 $u$ 距离不大于 $t$ 的节点中深度最小的节点．记录到根的距离，每次二分查找确定 $p$．此时 $u$ 对 $p$ 到 $u$ 路径上的所有节点都有一个贡献，可以用树上差分来记录．  
注意不能直接暴力移动 $p$，否则时间复杂度可能会退化至 $O(n^2)$．

### 习题

[leetcode 1438. 绝对差不超过限制的最长连续子数组](https://leetcode-cn.com/problems/longest-continuous-subarray-with-absolute-diff-less-than-or-equal-to-limit/)

## 子序列匹配

???+ note "例题 3 [leetcode 524. 通过删除字母匹配到字典里最长单词](https://leetcode-cn.com/problems/longest-word-in-dictionary-through-deleting/)"
    给定一个字符串 $s$ 和一个字符串数组 $\mathit{dictionary}$ 作为字典，找出并返回字典中最长的字符串，该字符串可以通过删除 $s$ 中的某些字符得到．

### 过程

此类问题需要将字符串 $s$ 与 $t$ 进行匹配，判断 $t$ 是否为 $s$ 的子序列．解决这种问题只需先将两个指针一个 $i$ 放在 $s$ 开始位置，一个 $j$ 放在 $t$ 开始位置，如果 $s[i]=t[j]$ 说明 $t$ 的第 $j$ 位已经在 $s$ 中找到了第一个对应，可以进而检测后面的部分了，那么 $i$ 和 $j$ 同时加一．如果上述等式不成立，则 $t$ 的第 $j$ 位仍然没有被匹配上，所以只给 $i$ 加一，在 $s$ 的后面部分再继续寻找．最后，如果 $j$ 已经移到了超尾位置，说明整个字符串都可以被匹配上，也就是 $t$ 是 $s$ 的一个子序列，否则不是．

### 实现

```cpp
string findLongestWord(string s, vector<string>& dictionary) {
  sort(dictionary.begin(), dictionary.end());
  int mx = 0, r = 0;
  string ans = "";
  for (int i = dictionary.size() - 1; i >= 0; i--) {
    r = 0;
    for (int j = 0; j < s.length(); ++j) {
      if (s[j] == dictionary[i][r]) r++;
    }
    if (r == dictionary[i].length()) {
      if (r >= mx) {
        mx = r;
        ans = dictionary[i];
      }
    }
  }
  return ans;
}
```

这种两个指针指向不同对象然后逐步进行比对的方法还可以用在一些 dp 中．

## 利用序列有序性

很多时候在序列上使用双指针之所以能够正确地达到目的，是因为序列的某些性质，最常见的就是利用序列的有序性．

???+ note "例题 4 [leetcode 167. 两数之和 II - 输入有序数组](https://leetcode-cn.com/problems/two-sum-ii-input-array-is-sorted/)"
    给定一个已按照 **升序排列** 的整数数组 `numbers`，请你从数组中找出两个数满足相加之和等于目标数 `target`．

### 过程

这种问题也是双指针的经典应用了，虽然二分也很方便，但时间复杂度上多一个 $\log{n}$，而且代码不够简洁．

接下来介绍双指针做法：既然要找到两个数，且这两个数不能在同一位置，那其位置一定是一左一右．由于两数之和固定，那么两数之中的小数越大，大数越小．考虑到这些性质，那我们不妨从两边接近它们．

首先假定答案就是 1 和 n，如果发现 $num[1]+num[n]\gt \mathit{target}$，说明我们需要将其中的一个元素变小，而 $\mathit{num}[1]$ 已经不能再变小了，所以我们把指向 $n$ 的指针减一，让大数变小．

同理如果发现 $num[1]+num[n]\lt \mathit{target}$，说明我们要将其中的一个元素变大，但 $\mathit{num}[n]$ 已经不能再变大了，所以将指向 1 的指针加一，让小数变大．

推广到一般情形，如果此时我们两个指针分别指在 $l,r$ 上，且 $l\lt r$, 如果 $num[l]+num[r]\gt \mathit{target}$，就将 $r$ 减一，如果 $num[l]+num[r]\lt \mathit{target}$，就将 $l$ 加一．这样 $l$ 不断右移，$r$ 不断左移，最后两者各逼近到一个答案．

### 实现

```cpp
vector<int> twoSum(vector<int>& numbers, int target) {
  int r = numbers.size() - 1, l = 0;
  vector<int> ans;
  ans.clear();
  while (l < r) {
    if (numbers[l] + numbers[r] > target)
      r--;
    else if (numbers[l] + numbers[r] == target) {
      ans.push_back(l + 1), ans.push_back(r + 1);
      return ans;
    } else
      l++;
  }
  return ans;
}
```

在归并排序中，在 $O(n+m)$ 时间内合并两个有序数组，也是保证数组的有序性条件下使用的双指针法．

### 习题

[leetcode 15. 三数之和](https://leetcode-cn.com/problems/3sum/)

## 在单向链表中找环

### 过程

在单向链表中找环也是有多种办法，不过快慢双指针方法是其中最为简洁的方法之一，接下来介绍这种方法．

首先两个指针都指向链表的头部，令一个指针一次走一步，另一个指针一次走两步，如果它们相遇了，证明有环，否则无环，时间复杂度 $O(n)$．

如果有环的话，怎么找到环的起点呢？

我们列出式子来观察一下，设相遇时，慢指针一共走了 $k$ 步，在环上走了 $l$ 步（快慢指针在环上相遇时，慢指针一定没走完一圈）．快指针走了 $2k$ 步，设环长为 $C$，则有

$$
\begin{align}
& \ 2 k=n \times C+l+(k-l) \\
& \ k=n \times C \\
\end{align}
$$

第一次相遇时 $n$ 取最小正整数 1．也就是说 $k=C$．那么利用这个等式，可以在两个指针相遇后，将其中一个指针移到表头，让两者都一步一步走，再度相遇的位置即为环的起点．

### 实现

```cpp
--8<-- "docs/misc/code/two-pointer/two-pointer_1.cpp:core"
```

时间复杂度 $O(n)$．
