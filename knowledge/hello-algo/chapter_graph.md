

## chapter_graph / exercises

# 练习

## 知识巩固

### 用两种方式表示同一张图

一个无向图有 4 个顶点 `A、B、C、D`，边为
`A-B、A-C、B-C、C-D`。

<!-- numbered-subquestions -->

1. 写出它的邻接表；
2. 填写只含 0 和 1 的邻接矩阵；
3. 如果要判断 `A` 和 `D` 是否直接相连，哪种图的表示方法只需查看一个存储条目？
4. 如果图的顶点很多但边很少，哪种表示通常更节省空间？

??? success "参考答案"

    1. 邻接表为：

        ```text
        A: B, C
        B: A, C
        C: A, B, D
        D: C
        ```

    2. 邻接矩阵为：

        | | A | B | C | D |
        | --- | --- | --- | --- | --- |
        | A | 0 | 1 | 1 | 0 |
        | B | 1 | 0 | 1 | 0 |
        | C | 1 | 1 | 0 | 1 |
        | D | 0 | 0 | 1 | 0 |

    3. 邻接矩阵可直接查看第 `A` 行、第 `D` 列，因此很适合判断任意两点是否直接相连。

    4. 顶点很多但边很少时，邻接表只记录实际存在的边，通常比为每一对顶点都预留位置的邻接矩阵更节省空间。

### 广度优先与深度优先访问顺序

一个无向图的顶点为 `A、B、C、D、E`，边为
`A-B、A-C、B-D、C-D、D-E`。

从 A 出发，并规定遇到多个未访问邻接顶点时按字母顺序选择：

<!-- numbered-subquestions -->

1. 写出广度优先遍历（BFS）的访问顺序；
2. 写出递归深度优先遍历（DFS）的访问顺序；
3. 为什么两种遍历都需要记录已经访问过的顶点？

??? success "参考答案"

    1. BFS 的访问顺序为 `A, B, C, D, E`。它先访问离 A 一条边的 B、C，
        再访问更远的 D、E。

    2. DFS 的访问顺序为 `A, B, D, C, E`。它依次进入当前顶点的未访问邻接顶点，
        因此先走过 `A → B → D → C`；C 没有新的邻接顶点时回到 D，再访问 E。

    3. 图中存在环，例如 `A-B-D-C-A`。如果不记录已访问顶点，
        遍历可能反复沿环访问同一批顶点，无法正常结束。

### 一次 BFS 能访问整张图吗

一个无向图有顶点 `A、B、C、D、E、F`，边只有
`A-B、B-C、D-E`。

<!-- numbered-subquestions -->

1. 从 A 开始进行一次 BFS，可以访问哪些顶点？
2. 根据第 1 问，这一次 BFS 是否已经访问图中的所有顶点？为什么？
3. 若按字母顺序扫描所有顶点，每遇到一个未访问顶点就重新开始 BFS，
    各次 BFS 的起点是什么？这个图被分成几个互不连通的部分（连通分量）？

??? success "参考答案"

    1. 从 A 出发只能访问 `A、B、C`。

    2. 没有访问所有顶点。`D、E` 组成另一个互相连通的部分，F 是单独的顶点；
        它们与 A 之间都没有路径，因此从 A 出发无法到达。

    3. 三次 BFS 的起点依次为 `A、D、F`，分别访问
        `{A, B, C}`、`{D, E}` 和 `{F}`。因此这个图有 3 个连通分量。

## 编程练习

### 判断无向图中是否存在路径

给定一个含有 $n$ 个顶点的无向图，顶点编号为 $0$ 到 $n-1$。数组 `edges` 中的每一项 `[u, v]` 表示顶点 `u` 和 `v` 之间有一条无向边。

再给定起点 `source` 和终点 `destination`。请先根据 `edges` 建立邻接表，再使用 BFS 或 DFS
判断是否存在一条从 `source` 到 `destination` 的路径：存在则返回 `true`，否则返回 `false`。
图中可能有环，也可能不连通。

??? tip "解题提示"

    1. 每条无向边需要同时加入两个方向
    2. 图中可能有环，必须记录已经访问过的节点
    3. 从 source 出发，遇到 destination 返回 true，遍历结束仍未遇到则返回 false

[LeetCode](https://leetcode.cn/problems/find-if-path-exists-in-graph/){ .rounded-button .exercise-button target="_blank" rel="noopener noreferrer" }


## chapter_graph / graph

# 图

<u>图（graph）</u>是一种非线性数据结构，由<u>顶点（vertex）</u>和<u>边（edge）</u>组成。我们可以将图 $G$ 抽象地表示为一组顶点 $V$ 和一组边 $E$ 的集合。以下示例展示了一个包含 5 个顶点和 7 条边的图。

$$
\begin{aligned}
V & = \{ 1, 2, 3, 4, 5 \} \newline
E & = \{ (1,2), (1,3), (1,5), (2,3), (2,4), (2,5), (4,5) \} \newline
G & = \{ V, E \} \newline
\end{aligned}
$$

如果将顶点看作节点，将边看作连接各个节点的引用（指针），我们就可以将图看作一种从链表拓展而来的数据结构。如下图所示，**相较于线性关系（链表）和分治关系（树），网络关系（图）的自由度更高**，因而更为复杂。

![链表、树、图之间的关系](graph.assets/linkedlist_tree_graph.png)

## 图的常见类型与术语

根据边是否具有方向，可分为<u>无向图（undirected graph）</u>和<u>有向图（directed graph）</u>，如下图所示。

- 在无向图中，边表示两顶点之间的“双向”连接关系，例如微信或 QQ 中的“好友关系”。
- 在有向图中，边具有方向性，即 $A \rightarrow B$ 和 $A \leftarrow B$ 两个方向的边是相互独立的，例如微博或抖音上的“关注”与“被关注”关系。

![有向图与无向图](graph.assets/directed_graph.png)

根据所有顶点是否连通，可分为<u>连通图（connected graph）</u>和<u>非连通图（disconnected graph）</u>，如下图所示。

- 对于连通图，从某个顶点出发，可以到达其余任意顶点。
- 对于非连通图，从某个顶点出发，至少有一个顶点无法到达。

![连通图与非连通图](graph.assets/connected_graph.png)

我们还可以为边添加“权重”变量，从而得到如下图所示的<u>有权图（weighted graph）</u>。例如在《王者荣耀》等手游中，系统会根据共同游戏时间来计算玩家之间的“亲密度”，这种亲密度网络就可以用有权图来表示。

![有权图与无权图](graph.assets/weighted_graph.png)

图数据结构包含以下常用术语。

- <u>邻接（adjacency）</u>：当两顶点之间存在边相连时，称这两顶点“邻接”。在上图中，顶点 1 的邻接顶点为顶点 2、3、5。
- <u>路径（path）</u>：从顶点 A 到顶点 B 经过的边构成的序列被称为从 A 到 B 的“路径”。在上图中，边序列 1-5-2-4 是顶点 1 到顶点 4 的一条路径。
- <u>度（degree）</u>：一个顶点拥有的边数。对于有向图，<u>入度（in-degree）</u>表示有多少条边指向该顶点，<u>出度（out-degree）</u>表示有多少条边从该顶点指出。

## 图的表示

图的常用表示方式包括“邻接矩阵”和“邻接表”。以下使用无向图进行举例。

### 邻接矩阵

设图的顶点数量为 $n$ ，<u>邻接矩阵（adjacency matrix）</u>使用一个 $n \times n$ 大小的矩阵来表示图，每一行（列）代表一个顶点，矩阵元素代表边，用 $1$ 或 $0$ 表示两个顶点之间是否存在边。

如下图所示，设邻接矩阵为 $M$、顶点列表为 $V$ ，那么矩阵元素 $M[i, j] = 1$ 表示顶点 $V[i]$ 到顶点 $V[j]$ 之间存在边，反之 $M[i, j] = 0$ 表示两顶点之间无边。

![图的邻接矩阵表示](graph.assets/adjacency_matrix.png)

邻接矩阵具有以下特性。

- 在简单图中，顶点不能与自身相连，此时邻接矩阵主对角线元素没有意义。
- 对于无向图，两个方向的边等价，此时邻接矩阵关于主对角线对称。
- 将邻接矩阵的元素从 $1$ 和 $0$ 替换为权重，则可表示有权图。

使用邻接矩阵表示图时，我们可以直接访问矩阵元素以获取边，因此增删查改操作的效率很高，时间复杂度均为 $O(1)$ 。然而，矩阵的空间复杂度为 $O(n^2)$ ，内存占用较多。

### 邻接表

<u>邻接表（adjacency list）</u>使用 $n$ 个链表来表示图，链表节点表示顶点。第 $i$ 个链表对应顶点 $i$ ，其中存储了该顶点的所有邻接顶点（与该顶点相连的顶点）。下图展示了一个使用邻接表存储的图的示例。

![图的邻接表表示](graph.assets/adjacency_list.png)

邻接表仅存储实际存在的边，而边的总数通常远小于 $n^2$ ，因此它更加节省空间。然而，在邻接表中需要通过遍历链表来查找边，因此其时间效率不如邻接矩阵。

观察上图，**邻接表结构与哈希表中的“链式地址”非常相似，因此我们也可以采用类似的方法来优化效率**。比如当链表较长时，可以将链表转化为 AVL 树或红黑树，从而将时间效率从 $O(n)$ 优化至 $O(\log n)$ ；还可以把链表转换为哈希表，从而将时间复杂度降至 $O(1)$ 。

## 图的常见应用

如下表所示，许多现实系统可以用图来建模，相应的问题也可以约化为图计算问题。

<p align="center"> 表 <id> &nbsp; 现实生活中常见的图 </p>

|          | 顶点 | 边                   | 图计算问题   |
| -------- | ---- | -------------------- | ------------ |
| 社交网络 | 用户 | 好友关系             | 潜在好友推荐 |
| 地铁线路 | 站点 | 站点间的连通性       | 最短路线推荐 |
| 太阳系   | 星体 | 星体间的万有引力作用 | 行星轨道计算 |


## chapter_graph / graph_operations

# 图的基础操作

图的基础操作可分为对“边”的操作和对“顶点”的操作。在“邻接矩阵”和“邻接表”两种表示方法下，实现方式有所不同。

## 基于邻接矩阵的实现

给定一个顶点数量为 $n$ 的无向图，则各种操作的实现方式如下图所示。

- **添加或删除边**：直接在邻接矩阵中修改指定的边即可，使用 $O(1)$ 时间。而由于是无向图，因此需要同时更新两个方向的边。
- **添加顶点**：在邻接矩阵的尾部添加一行一列，并全部填 $0$ 即可，使用 $O(n)$ 时间。
- **删除顶点**：在邻接矩阵中删除一行一列。当删除首行首列时达到最差情况，需要将 $(n-1)^2$ 个元素“向左上移动”，从而使用 $O(n^2)$ 时间。
- **初始化**：传入 $n$ 个顶点，初始化长度为 $n$ 的顶点列表 `vertices` ，使用 $O(n)$ 时间；初始化 $n \times n$ 大小的邻接矩阵 `adjMat` ，使用 $O(n^2)$ 时间。

=== "<1>"
    ![邻接矩阵的初始化、增删边、增删顶点](graph_operations.assets/adjacency_matrix_step1_initialization.png)

=== "<2>"
    ![adjacency_matrix_add_edge](graph_operations.assets/adjacency_matrix_step2_add_edge.png)

=== "<3>"
    ![adjacency_matrix_remove_edge](graph_operations.assets/adjacency_matrix_step3_remove_edge.png)

=== "<4>"
    ![adjacency_matrix_add_vertex](graph_operations.assets/adjacency_matrix_step4_add_vertex.png)

=== "<5>"
    ![adjacency_matrix_remove_vertex](graph_operations.assets/adjacency_matrix_step5_remove_vertex.png)

以下是基于邻接矩阵表示图的实现代码：

```src
[file]{graph_adjacency_matrix}-[class]{graph_adj_mat}-[func]{}
```

## 基于邻接表的实现

设无向图的顶点总数为 $n$、边总数为 $m$ ，则可根据下图所示的方法实现各种操作。

- **添加边**：在顶点对应链表的末尾添加边即可，使用 $O(1)$ 时间。因为是无向图，所以需要同时添加两个方向的边。
- **删除边**：在顶点对应链表中查找并删除指定边，使用 $O(m)$ 时间。在无向图中，需要同时删除两个方向的边。
- **添加顶点**：在邻接表中添加一个链表，并将新增顶点作为链表头节点，使用 $O(1)$ 时间。
- **删除顶点**：需遍历整个邻接表，删除包含指定顶点的所有边，使用 $O(n + m)$ 时间。
- **初始化**：在邻接表中创建 $n$ 个顶点和 $2m$ 条边，使用 $O(n + m)$ 时间。

=== "<1>"
    ![邻接表的初始化、增删边、增删顶点](graph_operations.assets/adjacency_list_step1_initialization.png)

=== "<2>"
    ![adjacency_list_add_edge](graph_operations.assets/adjacency_list_step2_add_edge.png)

=== "<3>"
    ![adjacency_list_remove_edge](graph_operations.assets/adjacency_list_step3_remove_edge.png)

=== "<4>"
    ![adjacency_list_add_vertex](graph_operations.assets/adjacency_list_step4_add_vertex.png)

=== "<5>"
    ![adjacency_list_remove_vertex](graph_operations.assets/adjacency_list_step5_remove_vertex.png)

以下是邻接表的代码实现。对比上图，实际代码有以下不同。

- 为了方便添加与删除顶点，以及简化代码，我们使用列表（动态数组）来代替链表。
- 使用哈希表来存储邻接表，`key` 为顶点实例，`value` 为该顶点的邻接顶点列表（链表）。

另外，我们在邻接表中使用 `Vertex` 类来表示顶点，这样做的原因是：如果与邻接矩阵一样，用列表索引来区分不同顶点，那么假设要删除索引为 $i$ 的顶点，则需遍历整个邻接表，将所有大于 $i$ 的索引全部减 $1$ ，效率很低。而如果每个顶点都是唯一的 `Vertex` 实例，删除某一顶点之后就无须改动其他顶点了。

```src
[file]{graph_adjacency_list}-[class]{graph_adj_list}-[func]{}
```

## 效率对比

设图中共有 $n$ 个顶点和 $m$ 条边，下表对比了邻接矩阵和邻接表的时间效率和空间效率。请注意，邻接表（链表）对应本文实现，而邻接表（哈希表）专指将所有链表替换为哈希表后的实现。

<p align="center"> 表 <id> &nbsp; 邻接矩阵与邻接表对比 </p>

|              | 邻接矩阵 | 邻接表（链表） | 邻接表（哈希表） |
| ------------ | -------- | -------------- | ---------------- |
| 判断是否邻接 | $O(1)$   | $O(n)$         | $O(1)$           |
| 添加边       | $O(1)$   | $O(1)$         | $O(1)$           |
| 删除边       | $O(1)$   | $O(n)$         | $O(1)$           |
| 添加顶点     | $O(n)$   | $O(1)$         | $O(1)$           |
| 删除顶点     | $O(n^2)$ | $O(n + m)$     | $O(n)$           |
| 内存空间占用 | $O(n^2)$ | $O(n + m)$     | $O(n + m)$       |

观察上表，似乎邻接表（哈希表）的时间效率与空间效率最优。但实际上，在邻接矩阵中操作边的效率更高，只需一次数组访问或赋值操作即可。综合来看，邻接矩阵体现了“以空间换时间”的原则，而邻接表体现了“以时间换空间”的原则。


## chapter_graph / graph_traversal

# 图的遍历

树代表的是“一对多”的关系，而图则具有更高的自由度，可以表示任意的“多对多”关系。因此，我们可以把树看作图的一种特例。显然，**树的遍历操作也是图的遍历操作的一种特例**。

图和树都需要应用搜索算法来实现遍历操作。图的遍历方式也可分为两种：<u>广度优先遍历</u>和<u>深度优先遍历</u>。

## 广度优先遍历

**广度优先遍历是一种由近及远的遍历方式，从某个节点出发，始终优先访问距离最近的顶点，并一层层向外扩张**。如下图所示，从左上角顶点出发，首先遍历该顶点的所有邻接顶点，然后遍历下一个顶点的所有邻接顶点，以此类推，直至所有顶点访问完毕。

![图的广度优先遍历](graph_traversal.assets/graph_bfs.png)

### 算法实现

BFS 通常借助队列来实现，代码如下所示。队列具有“先入先出”的性质，这与 BFS 的“由近及远”的思想异曲同工。

1. 将遍历起始顶点 `startVet` 加入队列，并开启循环。
2. 在循环的每轮迭代中，弹出队首顶点并记录访问，然后将该顶点的所有邻接顶点加入到队列尾部。
3. 循环步骤 `2.` ，直到所有顶点被访问完毕后结束。

为了防止重复遍历顶点，我们需要借助一个哈希集合 `visited` 来记录哪些节点已被访问。

!!! tip

    哈希集合可以看作一个只存储 `key` 而不存储 `value` 的哈希表，它可以在 $O(1)$ 时间复杂度下进行 `key` 的增删查改操作。根据 `key` 的唯一性，哈希集合通常用于数据去重等场景。

```src
[file]{graph_bfs}-[class]{}-[func]{graph_bfs}
```

代码相对抽象，建议对照下图来加深理解。

=== "<1>"
    ![图的广度优先遍历步骤](graph_traversal.assets/graph_bfs_step1.png)

=== "<2>"
    ![graph_bfs_step2](graph_traversal.assets/graph_bfs_step2.png)

=== "<3>"
    ![graph_bfs_step3](graph_traversal.assets/graph_bfs_step3.png)

=== "<4>"
    ![graph_bfs_step4](graph_traversal.assets/graph_bfs_step4.png)

=== "<5>"
    ![graph_bfs_step5](graph_traversal.assets/graph_bfs_step5.png)

=== "<6>"
    ![graph_bfs_step6](graph_traversal.assets/graph_bfs_step6.png)

=== "<7>"
    ![graph_bfs_step7](graph_traversal.assets/graph_bfs_step7.png)

=== "<8>"
    ![graph_bfs_step8](graph_traversal.assets/graph_bfs_step8.png)

=== "<9>"
    ![graph_bfs_step9](graph_traversal.assets/graph_bfs_step9.png)

=== "<10>"
    ![graph_bfs_step10](graph_traversal.assets/graph_bfs_step10.png)

=== "<11>"
    ![graph_bfs_step11](graph_traversal.assets/graph_bfs_step11.png)

!!! question "广度优先遍历的序列是否唯一？"

    不唯一。广度优先遍历只要求按“由近及远”的顺序遍历，**而多个相同距离的顶点的遍历顺序允许被任意打乱**。以上图为例，顶点 $1$、$3$ 的访问顺序可以交换，顶点 $2$、$4$、$6$ 的访问顺序也可以任意交换。

### 复杂度分析

**时间复杂度**：所有顶点都会入队并出队一次，使用 $O(|V|)$ 时间；在遍历邻接顶点的过程中，由于是无向图，因此所有边都会被访问 $2$ 次，使用 $O(2|E|)$ 时间；总体使用 $O(|V| + |E|)$ 时间。

**空间复杂度**：列表 `res` ，哈希集合 `visited` ，队列 `que` 中的顶点数量最多为 $|V|$ ，使用 $O(|V|)$ 空间。

## 深度优先遍历

**深度优先遍历是一种优先走到底、无路可走再回头的遍历方式**。如下图所示，从左上角顶点出发，访问当前顶点的某个邻接顶点，直到走到尽头时返回，再继续走到尽头并返回，以此类推，直至所有顶点遍历完成。

![图的深度优先遍历](graph_traversal.assets/graph_dfs.png)

### 算法实现

这种“走到尽头再返回”的算法范式通常基于递归来实现。与广度优先遍历类似，在深度优先遍历中，我们也需要借助一个哈希集合 `visited` 来记录已被访问的顶点，以避免重复访问顶点。

```src
[file]{graph_dfs}-[class]{}-[func]{graph_dfs}
```

深度优先遍历的算法流程如下图所示。

- **直虚线代表向下递推**，表示开启了一个新的递归方法来访问新顶点。
- **曲虚线代表向上回溯**，表示此递归方法已经返回，回溯到了开启此方法的位置。

为了加深理解，建议将下图与代码结合起来，在脑中模拟（或者用笔画下来）整个 DFS 过程，包括每个递归方法何时开启、何时返回。

=== "<1>"
    ![图的深度优先遍历步骤](graph_traversal.assets/graph_dfs_step1.png)

=== "<2>"
    ![graph_dfs_step2](graph_traversal.assets/graph_dfs_step2.png)

=== "<3>"
    ![graph_dfs_step3](graph_traversal.assets/graph_dfs_step3.png)

=== "<4>"
    ![graph_dfs_step4](graph_traversal.assets/graph_dfs_step4.png)

=== "<5>"
    ![graph_dfs_step5](graph_traversal.assets/graph_dfs_step5.png)

=== "<6>"
    ![graph_dfs_step6](graph_traversal.assets/graph_dfs_step6.png)

=== "<7>"
    ![graph_dfs_step7](graph_traversal.assets/graph_dfs_step7.png)

=== "<8>"
    ![graph_dfs_step8](graph_traversal.assets/graph_dfs_step8.png)

=== "<9>"
    ![graph_dfs_step9](graph_traversal.assets/graph_dfs_step9.png)

=== "<10>"
    ![graph_dfs_step10](graph_traversal.assets/graph_dfs_step10.png)

=== "<11>"
    ![graph_dfs_step11](graph_traversal.assets/graph_dfs_step11.png)

!!! question "深度优先遍历的序列是否唯一？"

    与广度优先遍历类似，深度优先遍历序列的顺序也不是唯一的。给定某顶点，先往哪个方向探索都可以，即邻接顶点的顺序可以任意打乱，都是深度优先遍历。
    
    以树的遍历为例，“根 $\rightarrow$ 左 $\rightarrow$ 右”“左 $\rightarrow$ 根 $\rightarrow$ 右”“左 $\rightarrow$ 右 $\rightarrow$ 根”分别对应前序、中序、后序遍历，它们展示了三种遍历优先级，然而这三者都属于深度优先遍历。

### 复杂度分析

**时间复杂度**：所有顶点都会被访问 $1$ 次，使用 $O(|V|)$ 时间；所有边都会被访问 $2$ 次，使用 $O(2|E|)$ 时间；总体使用 $O(|V| + |E|)$ 时间。

**空间复杂度**：列表 `res` ，哈希集合 `visited` 顶点数量最多为 $|V|$ ，递归深度最大为 $|V|$ ，因此使用 $O(|V|)$ 空间。


## chapter_graph / summary

# 小结

### 重点回顾

- 图由顶点和边组成，可以表示为一组顶点和一组边构成的集合。
- 相较于线性关系（链表）和分治关系（树），网络关系（图）具有更高的自由度，因而更为复杂。
- 有向图的边具有方向性，连通图中的任意顶点均可达，有权图的每条边都包含权重变量。
- 邻接矩阵利用矩阵来表示图，每一行（列）代表一个顶点，矩阵元素代表边，用 $1$ 或 $0$ 表示两个顶点之间有边或无边。邻接矩阵在增删查改操作上效率很高，但空间占用较多。
- 邻接表使用多个链表来表示图，第 $i$ 个链表对应顶点 $i$ ，其中存储了该顶点的所有邻接顶点。邻接表相对于邻接矩阵更加节省空间，但由于需要遍历链表来查找边，因此时间效率较低。
- 当邻接表中的链表过长时，可以将其转换为红黑树或哈希表，从而提升查询效率。
- 从算法思想的角度分析，邻接矩阵体现了“以空间换时间”，邻接表体现了“以时间换空间”。
- 图可用于建模各类现实系统，如社交网络、地铁线路等。
- 树是图的一种特例，树的遍历也是图的遍历的一种特例。
- 图的广度优先遍历是一种由近及远、层层扩张的搜索方式，通常借助队列实现。
- 图的深度优先遍历是一种优先走到底、无路可走时再回溯的搜索方式，常基于递归来实现。

### Q & A

**Q**：路径的定义是顶点序列还是边序列？

维基百科上不同语言版本的定义不一致：英文版是“路径是一个边序列”，而中文版是“路径是一个顶点序列”。以下是英文版原文：In graph theory, a path in a graph is a finite or infinite sequence of edges which joins a sequence of vertices.

在本文中，路径被视为一个边序列，而不是一个顶点序列。这是因为两个顶点之间可能存在多条边连接，此时每条边都对应一条路径。

**Q**：非连通图中是否会有无法遍历到的点？

在非连通图中，从某个顶点出发，至少有一个顶点无法到达。遍历非连通图需要设置多个起点，以遍历到图的所有连通分量。

**Q**：在邻接表中，“与该顶点相连的所有顶点”的顶点顺序是否有要求？

可以是任意顺序。但在实际应用中，可能需要按照指定规则来排序，比如按照顶点添加的次序，或者按照顶点值大小的顺序等，这样有助于快速查找“带有某种极值”的顶点。
