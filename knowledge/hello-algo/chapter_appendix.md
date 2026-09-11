

## chapter_appendix / contribution

# 一起参与创作

由于笔者能力有限，书中难免存在一些遗漏和错误，请您谅解。如果您发现了笔误、链接失效、内容缺失、文字歧义、解释不清晰或行文结构不合理等问题，请协助我们进行修正，以给读者提供更优质的学习资源。

所有[撰稿人](https://github.com/krahets/hello-algo/graphs/contributors)的 GitHub ID 将在本书仓库、网页版和 PDF 版的主页上进行展示，以感谢他们对开源社区的无私奉献。

!!! success "开源的魅力"

    纸质图书的两次印刷的间隔时间往往较久，内容更新非常不方便。
    
    而在本开源书中，内容更迭的时间被缩短至数日甚至几个小时。

### 内容微调

如下图所示，每个页面的右上角都有“编辑图标”。您可以按照以下步骤修改文本或代码。

1. 点击“编辑图标”，如果遇到“需要 Fork 此仓库”的提示，请同意该操作。
2. 修改 Markdown 源文件内容，检查内容的正确性，并尽量保持排版格式的统一。
3. 在页面底部填写修改说明，然后点击“Propose file change”按钮。页面跳转后，点击“Create pull request”按钮即可发起拉取请求。

![页面编辑按键](contribution.assets/edit_markdown.png)

图片无法直接修改，需要通过新建 [Issue](https://github.com/krahets/hello-algo/issues) 或评论留言来描述问题，我们会尽快重新绘制并替换图片。

### 内容创作

如果您有兴趣参与此开源项目，包括将代码翻译成其他编程语言、扩展文章内容等，那么需要实施以下 Pull Request 工作流程。

1. 登录 GitHub ，将本书的[代码仓库](https://github.com/krahets/hello-algo) Fork 到个人账号下。
2. 进入您的 Fork 仓库网页，使用 `git clone` 命令将仓库克隆至本地。
3. 在本地进行内容创作，并进行完整测试，验证代码的正确性。
4. 将本地所做更改 Commit ，然后 Push 至远程仓库。
5. 刷新仓库网页，点击“Create pull request”按钮即可发起拉取请求。

### Docker 部署

在 `hello-algo` 根目录下，执行以下 Docker 脚本，即可在 `http://localhost:8000` 访问本项目：

```shell
docker-compose up -d
```

使用以下命令即可删除部署：

```shell
docker-compose down
```


## chapter_appendix / installation

# 编程环境安装

## 安装 IDE

推荐使用开源、轻量的 VS Code 作为本地集成开发环境（IDE）。访问 [VS Code 官网](https://code.visualstudio.com/)，根据操作系统选择相应版本的 VS Code 进行下载和安装。

![从官网下载 VS Code](installation.assets/vscode_installation.png)

VS Code 拥有强大的扩展包生态系统，支持大多数编程语言的运行和调试。以 Python 为例，安装“Python Extension Pack”扩展包之后，即可进行 Python 代码调试。安装步骤如下图所示。

![安装 VS Code 扩展包](installation.assets/vscode_extension_installation.png)

## 安装语言环境

### Python 环境

1. 下载并安装 [Miniconda3](https://docs.conda.io/en/latest/miniconda.html) ，需要 Python 3.10 或更新版本。
2. 在 VS Code 的插件市场中搜索 `python` ，安装 Python Extension Pack 。
3. （可选）在命令行输入 `pip install black` ，安装代码格式化工具。

### C/C++ 环境

1. Windows 系统需要安装 [MinGW](https://sourceforge.net/projects/mingw-w64/files/)（[配置教程](https://blog.csdn.net/qq_33698226/article/details/129031241)）；macOS 自带 Clang ，无须安装。
2. 在 VS Code 的插件市场中搜索 `c++` ，安装 C/C++ Extension Pack 。
3. （可选）打开 Settings 页面，搜索 `Clang_format_fallback Style` 代码格式化选项，设置为 `{ BasedOnStyle: Microsoft, BreakBeforeBraces: Attach }` 。

### Java 环境

1. 下载并安装 [OpenJDK](https://jdk.java.net/18/)（版本需满足 > JDK 9）。
2. 在 VS Code 的插件市场中搜索 `java` ，安装 Extension Pack for Java 。

### C# 环境

1. 下载并安装 [.NET 8.0](https://dotnet.microsoft.com/en-us/download) 。
2. 在 VS Code 的插件市场中搜索 `C# Dev Kit` ，安装 C# Dev Kit （[配置教程](https://code.visualstudio.com/docs/csharp/get-started)）。
3. 也可使用 Visual Studio（[安装教程](https://learn.microsoft.com/zh-cn/visualstudio/install/install-visual-studio?view=vs-2022)）。

### Go 环境

1. 下载并安装 [go](https://go.dev/dl/) 。
2. 在 VS Code 的插件市场中搜索 `go` ，安装 Go 。
3. 按快捷键 `Ctrl + Shift + P` 呼出命令栏，输入 go ，选择 `Go: Install/Update Tools` ，全部勾选并安装即可。

### Swift 环境

1. 下载并安装 [Swift](https://www.swift.org/download/) 。
2. 在 VS Code 的插件市场中搜索 `swift` ，安装 [Swift for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=sswg.swift-lang) 。

### JavaScript 环境

1. 下载并安装 [Node.js](https://nodejs.org/en/) 。
2. （可选）在 VS Code 的插件市场中搜索 `Prettier` ，安装代码格式化工具。

### TypeScript 环境

1. 同 JavaScript 环境安装步骤。
2. 安装 [TypeScript Execute (tsx)](https://github.com/privatenumber/tsx?tab=readme-ov-file#global-installation) 。
3. 在 VS Code 的插件市场中搜索 `typescript` ，安装 [Pretty TypeScript Errors](https://marketplace.visualstudio.com/items?itemName=yoavbls.pretty-ts-errors) 。

### Dart 环境

1. 下载并安装 [Dart](https://dart.dev/get-dart) 。
2. 在 VS Code 的插件市场中搜索 `dart` ，安装 [Dart](https://marketplace.visualstudio.com/items?itemName=Dart-Code.dart-code) 。

### Rust 环境

1. 下载并安装 [Rust](https://www.rust-lang.org/tools/install) 。
2. 在 VS Code 的插件市场中搜索 `rust` ，安装 [rust-analyzer](https://marketplace.visualstudio.com/items?itemName=rust-lang.rust-analyzer) 。


## chapter_appendix / terminology

# 术语表

下表列出了书中出现的重要术语。建议记住各个名词的英文叫法，以便阅读英文文献。

<p align="center"> 表 <id> &nbsp; 数据结构与算法的重要名词 </p>

| English                        | 简体中文       |
| ------------------------------ | -------------- |
| algorithm                      | 算法           |
| data structure                 | 数据结构       |
| code                           | 代码           |
| file                           | 文件           |
| function                       | 函数           |
| method                         | 方法           |
| variable                       | 变量           |
| asymptotic complexity analysis | 渐近复杂度分析 |
| time complexity                | 时间复杂度     |
| space complexity               | 空间复杂度     |
| loop                           | 循环           |
| iteration                      | 迭代           |
| recursion                      | 递归           |
| tail recursion                 | 尾递归         |
| recursion tree                 | 递归树         |
| big-$O$ notation               | 大 $O$ 记号    |
| asymptotic upper bound         | 渐近上界       |
| sign-magnitude                 | 原码           |
| 1’s complement                 | 反码           |
| 2’s complement                 | 补码           |
| array                          | 数组           |
| index                          | 索引           |
| linked list                    | 链表           |
| linked list node, list node    | 链表节点       |
| head node                      | 头节点         |
| tail node                      | 尾节点         |
| list                           | 列表           |
| dynamic array                  | 动态数组       |
| hard disk                      | 硬盘           |
| random-access memory (RAM)     | 内存           |
| cache memory                   | 缓存           |
| cache miss                     | 缓存未命中     |
| cache hit rate                 | 缓存命中率     |
| stack                          | 栈             |
| top of the stack               | 栈顶           |
| bottom of the stack            | 栈底           |
| queue                          | 队列           |
| double-ended queue             | 双向队列       |
| front of the queue             | 队首           |
| rear of the queue              | 队尾           |
| hash table                     | 哈希表         |
| hash set                       | 哈希集合       |
| bucket                         | 桶             |
| hash function                  | 哈希函数       |
| hash collision                 | 哈希冲突       |
| load factor                    | 负载因子       |
| separate chaining              | 链式地址       |
| open addressing                | 开放寻址       |
| linear probing                 | 线性探测       |
| lazy deletion                  | 懒删除         |
| binary tree                    | 二叉树         |
| tree node                      | 树节点         |
| left-child node                | 左子节点       |
| right-child node               | 右子节点       |
| parent node                    | 父节点         |
| left subtree                   | 左子树         |
| right subtree                  | 右子树         |
| root node                      | 根节点         |
| leaf node                      | 叶节点         |
| edge                           | 边             |
| level                          | 层             |
| degree                         | 度             |
| height                         | 高度           |
| depth                          | 深度           |
| perfect binary tree            | 完美二叉树     |
| complete binary tree           | 完全二叉树     |
| full binary tree               | 完满二叉树     |
| balanced binary tree           | 平衡二叉树     |
| binary search tree             | 二叉搜索树     |
| AVL tree                       | AVL 树         |
| red-black tree                 | 红黑树         |
| level-order traversal          | 层序遍历       |
| breadth-first traversal        | 广度优先遍历   |
| depth-first traversal          | 深度优先遍历   |
| pre-order traversal            | 前序遍历       |
| in-order traversal             | 中序遍历       |
| post-order traversal           | 后序遍历       |
| balanced binary search tree    | 平衡二叉搜索树 |
| balance factor                 | 平衡因子       |
| heap                           | 堆             |
| max heap                       | 大顶堆         |
| min heap                       | 小顶堆         |
| priority queue                 | 优先队列       |
| heapify                        | 堆化           |
| top-$k$ problem                | Top-$k$ 问题   |
| graph                          | 图             |
| vertex                         | 顶点           |
| undirected graph               | 无向图         |
| directed graph                 | 有向图         |
| connected graph                | 连通图         |
| disconnected graph             | 非连通图       |
| weighted graph                 | 有权图         |
| adjacency                      | 邻接           |
| path                           | 路径           |
| in-degree                      | 入度           |
| out-degree                     | 出度           |
| adjacency matrix               | 邻接矩阵       |
| adjacency list                 | 邻接表         |
| breadth-first search           | 广度优先搜索   |
| depth-first search             | 深度优先搜索   |
| binary search                  | 二分查找       |
| searching algorithm            | 搜索算法       |
| sorting algorithm              | 排序算法       |
| selection sort                 | 选择排序       |
| bubble sort                    | 冒泡排序       |
| insertion sort                 | 插入排序       |
| quick sort                     | 快速排序       |
| merge sort                     | 归并排序       |
| heap sort                      | 堆排序         |
| bucket sort                    | 桶排序         |
| counting sort                  | 计数排序       |
| radix sort                     | 基数排序       |
| divide and conquer             | 分治           |
| hanota problem                 | 汉诺塔问题     |
| backtracking algorithm         | 回溯算法       |
| constraint                     | 约束           |
| solution                       | 解             |
| state                          | 状态           |
| pruning                        | 剪枝           |
| permutations problem           | 全排列问题     |
| subset-sum problem             | 子集和问题     |
| $n$-queens problem             | $n$ 皇后问题   |
| dynamic programming            | 动态规划       |
| initial state                  | 初始状态       |
| state-transition equation      | 状态转移方程   |
| knapsack problem               | 背包问题       |
| edit distance problem          | 编辑距离问题   |
| greedy algorithm               | 贪心算法       |
