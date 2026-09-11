

## search/alpha-beta.md

本页面将简要介绍 Minimax 算法和 Alpha–Beta 剪枝．

## Minimax 算法

Minimax 算法又叫极小化极大算法，是一种最小化最差（即最大损失）情境下的潜在损失的算法．

### 过程

在局面确定的双人零和对弈中，常需要进行对抗搜索，构建一棵每个节点都为一个确定状态的搜索树．奇数层为己方先手，偶数层为对方先手．搜索树上每个叶子节点都会被赋予一个估值，估值越大代表我方赢面越大．我方追求更大的赢面，而对方会设法降低我方的赢面；体现在搜索树上就是，奇数层节点（我方节点）总是会选择赢面最大的子节点状态，而偶数层（对方节点）总是会选择（我方）赢面最小的子节点状态．

Minimax 算法中，会从上到下遍历搜索树，回溯时利用子树信息更新答案，最后得到根节点的值——这就是我方在双方都采取最优策略下能获得的最大分数．

### 示例

来看一个简单的例子．

称我方为 MAX，对方为 MIN，图示如下：

![](images/minimax-1.svg)

例如，对于如下的局势，假设从左往右搜索，根节点的数值为我方赢面：

![](images/minimax-2.svg)

我方应选择中间的路线．因为，如果选择左边的路线，最差的赢面是 $3$；如果选择中间的路线，最差的赢面是 $15$；如果选择右边的路线，最差的赢面是 $1$．虽然选择右边的路线可能有 $22$ 的赢面，但足够理性的对方将会使我方只有 $1$ 的赢面．那么，经过权衡，显然选择中间的路线更优．

![](images/minimax-3.svg)

实际上，在看右边的路线时，当发现赢面可能为 $1$ 后就不必再去看赢面为 $12$、$20$、$22$ 的分支了．因为相较于左侧两条路线的赢面，已经可以确定右边的路线不是最好的．

朴素的 Minimax 算法常常需要构建一棵庞大的搜索树，时间和空间复杂度都将不能承受．而 Alpha–Beta 剪枝就是利用搜索树每个节点双方分数的上下界来对 Minimax 进行剪枝优化的一种方法．

需要注意的是，对于不同的问题，搜索树每个节点上的值有着不同的含义，它可以是估值、分数、赢的概率等等．为方便起见，下文统一用分数来称呼．

## Alpha–Beta 剪枝

Alpha–Beta 剪枝是针对 Minimax 算法的搜索剪枝．

### 过程

Minimax 算法中，若已知某节点的所有子节点的分数，则可以算出该节点的分数：对于 MAX 节点，取最大分数；对于 MIN 节点，取最小分数．

在搜索进行到某节点但尚未完成时，虽然不能算出该节点的分数，但是可以算出 **目前已经搜索过的节点中**，双方分数的取值范围．搜索时，维护两个变量 $\alpha$ 和 $\beta$，分别表示局面进行到该节点时，**考虑所有已经搜索过的节点**，Alpha 玩家（即寻求最大分数的一方）和 Beta 玩家（即寻求最小分数的一方）能够保证取得的分数的下界和上界．

Alpha–Beta 剪枝的剪枝策略依赖于搜索当前节点时 $\alpha$ 和 $\beta$ 的取值．如果当前节点是 MAX 节点，那么，Alpha 可以继续搜索它的子节点来提高分数下界 $\alpha$．但是，如果某次搜索后已经有 $\alpha\ge\beta$ 了，那么这个节点就不可能出现在一次对弈中：只要到达该节点处，Alpha 玩家就能够保证分数至少是 $\alpha$；可是 Beta 玩家已经知道存在一种（偏离当前路径的）策略，能够保证分数不超过 $\beta\le\alpha$，那么，Beta 玩家自然不会任由局面发展到 **当前节点** 处．同理，如果当前节点是 MIN 节点，且搜索它的某个子节点后已经发现该节点处有 $\beta\le\alpha$ 成立，那么，同样无需继续搜索其他子节点，因为 Alpha 玩家不会让局面进入 **当前节点**．总结两种情形可以发现：当 $\alpha \geq \beta$ 时，该节点剩余的分支就不必继续搜索了（也就是可以进行剪枝了）．注意，当 $\alpha = \beta$ 时，也需要剪枝，这是因为不会有更好的结果了，但可能有更差的结果．

搜索过程中，无需维护节点分数，只需要维护 $\alpha$ 和 $\beta$ 即可．初始时，令 $\alpha=-\infty,~\beta=+\infty$．向下搜索时，需要一并下传 $\alpha$ 和 $\beta$ 的信息，以记录两名玩家的备选方案．

搜索完子节点时，需要更新当前节点处的信息．不妨假设当前节点 $X$ 是 MAX 节点，且刚刚搜索完它的子节点 $Y$．那么，节点 $X$ 处的 $\beta$ 值不会改变，只有 $\alpha$ 值需要与子节点 $Y$ 的分数取最大值．如果子节点 $Y$ 是叶子节点，直接用子节点 $Y$ 的分数更新当前节点 $X$ 处的 $\alpha$ 值；否则，只需要用子节点 $Y$ 的 $\beta$ 值更新当前节点 $X$ 的 $\alpha$ 值．此时，有三种可能性：

1.  子节点 $Y$ 的 $\beta$ 值严格位于节点 $X$ 的 $\alpha$ 值和 $\beta$ 值之间．因为子节点 $Y$ 继承了节点 $X$ 的 $\alpha$ 值且不会更新它，所以，搜索子节点 $Y$ 完后仍然有 $\beta > \alpha$，就说明搜索子节点 $Y$ 时没有发生剪枝．子节点 $Y$ 最终的 $\beta$ 值，就等于它继承的节点 $X$ 的 $\beta$ 值和它（指子节点 $Y$）的所有子节点的分数中，最小的那个．既然这个最小值严格小于节点 $X$ 的 $\beta$ 值，就说明它一定是子节点 $Y$ 的所有子节点的分数最小值．因此，作为 MIN 节点，子节点 $Y$ 的分数就是这个 $\beta$ 值．用它更新节点 $X$ 的 $\alpha$ 值是合理的．
2.  子节点 $Y$ 的 $\beta$ 值就等于节点 $X$ 的 $\beta$ 值．如上文所述，这说明子节点 $Y$ 的所有子节点的分数均不小于节点 $X$ 的 $\beta$ 值．这进一步说明 Beta 玩家不会任由局面进入节点 $X$：因为 Alpha 玩家只要选择了子节点 $Y$，Beta 玩家就不能取得比 $\beta$ 更低的分数．因此，此时使用子节点 $Y$ 的 $\beta$ 值更新节点 $X$ 的 $\alpha$ 值，是为了使得节点 $X$ 处 $\alpha=\beta$，以触发剪枝条件．它的效果与使用 $Y$ 处实际分数——一个大于等于节点 $X$ 处 $\beta$ 值的数字——更新节点 $X$ 的 $\alpha$ 值的效果是一样的．
3.  子节点 $Y$ 的 $\beta$ 值小于等于节点 $X$ 的 $\alpha$ 值．此时，子节点 $Y$ 触发了剪枝条件，它的实际分数不会超过子节点 $Y$ 的 $\beta$ 值，更不会超过节点 $X$ 的 $\alpha$ 值．用子节点 $Y$ 的实际分数更新节点 $X$ 的 $\alpha$ 值不会改变 $\alpha$ 值．这与使用子节点 $Y$ 的 $\beta$ 值更新节点 $X$ 的 $\alpha$ 值的效果是一样的．

这一分析说明，当某个子节点搜索完成后，只有它的分数处于第一种情形时，$\alpha$（或 $\beta$）才准确记录了这个子节点作为一个 MAX 节点（或 MIN 节点）的实际分数．对于其他情形，虽然它未必是准确的分数，但是它提供的信息足以保证剪枝的正确进行，从而不影响根节点处的分数记录．

### 示例

本节通过分析一个例子，来展示如何在搜索过程中更新各个节点处的 $\alpha$ 和 $\beta$ 值．过程中，也一并计算了所涉及的节点处的分数．由此，就可以观察每个节点处的实际分数与所记录的 $\alpha$ 和 $\beta$ 值的关系．但应注意，实现这一算法时，并不会计算这些节点的实际分数．

对于如下的局势，假设从左往右搜索：

![](images/alpha-beta-1.svg)

初始化时，令 $\alpha = -\infty,~\beta = +\infty$，并将这一信息沿着搜索路径下传．

![](images/alpha-beta-2.svg)

搜索到节点 A 时，由于左子节点的分数为 $3$，而节点 A 是 MIN 节点，试图找分数小的走法，于是将 $\beta$ 值修改为 $3$，这是因为 $3$ 小于当前的 $\beta$ 值（$\beta = +\infty$）．然后节点 A 的右子节点的分数为 $17$，此时不修改节点 A 的 $\beta$ 值，这是因为 $17$ 大于当前的 $\beta$ 值（$\beta = 3$）．此时，节点 A 的所有子节点已搜索完毕，即可计算出节点 A 的分数为 $3$，这与该节点处记录的 $\beta$ 值一致（前文的情形 1）．

![](images/alpha-beta-3.svg)

节点 A 是节点 B 的子节点，计算出节点 A 的分数后，可以更新节点 B 的 $\alpha$ 和 $\beta$ 值．由于节点 B 是 MAX 节点，试图找分数大的走法，于是将 $\alpha$ 值修改为 $3$，这是因为子节点 A 处的 $\beta$ 值（$\beta=3$）大于当前的 $\alpha$ 值（$\alpha = -\infty$）．之后，搜索节点 B 的右子节点 C，并将节点 B 的 $\alpha$ 和 $\beta$ 值传递给节点 C．

![](images/alpha-beta-4.svg)

对于节点 C，由于左子节点的分数为 $2$，而节点 C 是 MIN 节点，于是将 $\beta$ 值修改为 $2$．此时 $\alpha \geq \beta$，故节点 C 的剩余子节点就不必搜索了，因为可以确定，Alpha 玩家不会允许局面发展到节点 C．此时，节点 C 是 MIN 节点，它的分数就是 $2$，不超过记录的 $\beta$ 值（前文的情形 3）．由于节点 B 的所有子节点搜索完毕，即可计算出节点 B 的分数为 $3$，与记录的 $\alpha$ 值相同（前文的情形 1）．

![](images/alpha-beta-5.svg)

计算出节点 B 的分数后，节点 B 是节点 D 的一个子节点，故可以更新节点 D 的 $\alpha$ 和 $\beta$ 值．由于节点 D 是 MIN 节点，于是将 $\beta$ 值修改为 $3$．然后节点 D 将 $\alpha$ 和 $\beta$ 值传递给节点 E，节点 E 又传递给节点 F．对于节点 F，它只有一个分数为 $15$ 的子节点，由于 $15$ 大于当前的 $\beta$ 值，而节点 F 为 MIN 节点，所以不更新其 $\beta$ 值，然后可以计算出节点 F 的分数为 $15$，大于记录的 $\beta$ 值（前文的情形 2）．

![](images/alpha-beta-6.svg)

计算出节点 F 的分数后，节点 F 是节点 E 的一个子节点，故可以更新节点 E 的 $\alpha$ 和 $\beta$ 值．节点 E 是 MAX 节点，更新 $\alpha$ 值，此时 $\alpha \geq \beta$，故可以剪去节点 E 的余下分支（即节点 G）．然后，节点 E 是 MAX 节点，将节点 E 的分数设为 $15$，严格大于记录的 $\alpha$ 值（前文的情形 3）．利用节点 E 的 $\alpha$ 值更新节点 D 的 $\beta$ 值，仍然是 $3$．此时，节点 D 的所有子节点搜索完毕，即可计算出节点 D 的分数为 $3$，等于记录的 $\beta$ 值（前文的情形 1）．

![](images/alpha-beta-7.svg)

计算出节点 D 的分数后，节点 D 是节点 H 的一个子节点，故可以更新节点 H 的 $\alpha$ 和 $\beta$ 值．节点 H 是 MAX 节点，更新 $\alpha$．然后，按搜索顺序，将节点 H 的 $\alpha$ 和 $\beta$ 值依次传递给节点 I、J、K．对于节点 K，其左子节点的分数为 $2$，而节点 K 是 MIN 节点，更新 $\beta$，此时 $\alpha \geq \beta$，故可以剪去节点 K 的余下分支．然后，将节点 K 的分数设为 $2$，小于等于记录的 $\beta$ 值（前文的情形 3）．

![](images/alpha-beta-8.svg)

计算出节点 K 的分数后，节点 K 是节点 J 的一个子节点，故可以更新节点 J 的 $\alpha$ 和 $\beta$ 值．节点 J 是 MAX 节点，更新 $\alpha$，但是，由于节点 K 的分数小于 $\alpha$，所以节点 J 的 $\alpha$ 值维持 $3$ 不变．然后，将节点 J 的 $\alpha$ 和 $\beta$ 值传递给节点 L．由于节点 L 是 MIN 节点，更新 $\beta = 3$，此时 $\alpha \geq \beta$，故可以剪去节点 L 的余下分支．由于节点 L 没有余下分支，所以此处并没有实际剪枝．然后，将节点 L 的分数设为 $3$，它小于等于记录的 $\beta$ 值（前文的情形 3）．

![](images/alpha-beta-9.svg)

计算出节点 L 的分数后，节点 L 是节点 J 的一个子节点，故可以更新节点 J 的 $\alpha$ 和 $\beta$ 值．节点 J 是 MAX 节点，更新 $\alpha$，但是，由于节点 L 的分数小于等于 $\alpha$，所以节点 J 的 $\alpha$ 值维持 $3$ 不变．此时，节点 J 的所有子节点搜索完毕，即可计算出节点 J 的分数为 $3$，它等于记录的 $\alpha$ 值（前文的情形 2）．

计算出节点 J 的分数后，节点 J 是节点 I 的一个子节点，故可以更新节点 I 的 $\alpha$ 和 $\beta$ 值．节点 I 是 MIN 节点，更新 $\beta$，此时 $\alpha \geq \beta$，故可以剪去节点 I 的余下分支．值得注意的是，由于右子节点的存在，节点 I 的实际分数是 $2$，小于记录的 $\beta$ 值（前文的情形 3）．

计算出节点 I 的分数后，节点 I 是节点 H 的一个子节点，故可以更新节点 H 的 $\alpha$ 和 $\beta$ 值．节点 H 是 MAX 节点，更新 $\alpha$，但是，由于节点 I 的分数小于等于 $\alpha$，所以节点 H 的 $\alpha$ 值维持 $3$ 不变．此时，节点 H 的所有子节点搜索完毕，即可计算出节点 H 的分数为 $3$，它等于记录的 $\alpha$ 值（前文的情形 1）．

![](images/alpha-beta-10.svg)

这就是最终结果．

### 实现

???+ example "参考代码"
    ```cpp
    int alpha_beta(int u, int alph, int beta, bool is_max) {
      if (!son_num[u]) return val[u];
      if (is_max) {
        for (int i = 0; i < son_num[u]; ++i) {
          int d = son[u][i];
          alph = max(alph, alpha_beta(d, alph, beta, !is_max));
          if (alph >= beta) break;
        }
        return alph;
      } else {
        for (int i = 0; i < son_num[u]; ++i) {
          int d = son[u][i];
          beta = min(beta, alpha_beta(d, alph, beta, !is_max));
          if (alph >= beta) break;
        }
        return beta;
      }
    }
    ```

## 参考资料与注释

-   [Minimax Algorithm - Wikipedia](https://en.wikipedia.org/wiki/Minimax#Minimax_algorithm_with_alternate_moves)
-   [Alpha–beta pruning - Wikipedia](https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning)

**本文部分引用自博文 [详解 Minimax 算法与α-β剪枝\_文剑木然](https://blog.csdn.net/wenjianmuran/article/details/90633418)，遵循 CC 4.0 BY-SA 版权协议．内容有改动．**


## search/astar.md

本文介绍 A\* 搜索算法．

A\* 搜索算法（A\* search algorithm，A\* 读作 A-star），简称 A\* 算法，是一种在带权有向图上，找到给定起点与终点之间的最短路径的算法．它属于图遍历（graph traversal）和最佳优先搜索算法（best-first search），亦是 [BFS](./bfs.md) 的改进．

## 过程

A\* 算法的目标是找到有向图上从起点 $s$ 到终点 $t$ 的最短路径．设 $d(x,y)$ 为结点 $x$ 与 $y$ 之间的距离，也就是它们之间最短路径的长度．记 $g(x)=d(s,x)$ 为从起点 $s$ 到结点 $x$ 的距离函数，$h^*(x)$ 为从结点 $x$ 到终点 $t$ 的距离函数，$h(x)$ 为 $h^*(x)$ 的一个估计[^note1]．最后，记从 $s$ 出发经由 $x$ 到达 $t$ 的最短路径长度的估计为

$$
f(x) = g(x) + h(x).
$$

搜索时，A\* 算法每次从优先队列中取出一个 $f$ 最小的结点．然后，将它的所有后继结点 $x$ 都推入优先队列中，并利用实际记录的 $g(x)$ 和估计的 $h(x)$ 更新 $f(x)$．

## 性质

由于 $h^*(x)$ 的实际值在搜索的时候是未知的，所以，需要使用容易计算的 $h(x)$ 作为它的估计．A\* 搜索的实际复杂度就取决于这一估计函数 $h(x)$ 的性质．容易想象，如果 $h\equiv h^*$，也就是说，估计是精确的，那么，搜索过程就会严格按照最短路径前进．而如果 $h\equiv 0$，那么，A\* 算法就退化为 [Dijkstra 算法](./../graph/shortest-path.md#dijkstra-算法)；当 $h\equiv 0$ 并且边权为 $1$ 时，这就是 [BFS](./bfs.md)．

假设图没有负权边．如果估计 $h(x)$ 永远不超过实际距离 $h^*(x)$，即 $0\le h\le h^*$，那么，A\* 算法就一定能够找到最优解．满足这一条件的估计函数 $h(x)$ 称为 **可采纳的**（admissible）．根据前文的讨论，$h$ 越接近 $h^*$，相应的 A\* 算法效率就越高．一般来说，在最差情形中，算法会经过所有满足

$$
f(x) = g(x) + h(x) \le C^*
$$

的结点，其中，$C^*$ 是起点 $s$ 和终点 $t$ 之间的最短距离．直觉上，$h$ 越接近 $h^*$，每次扩展时，能够满足该条件的后继结点就越少，因此，算法搜索到的分支就越少．所以，A\* 算法可以看作是对搜索算法的一种「剪枝」优化．

如果 $h$ 不仅是可采纳的，还是 **一致的**（consistent），即

$$
h(x) \le h(y) + d(x, y),
$$

那么，A\* 算法不会将已经弹出队列的结点再次加入队列．一致性条件，可以理解为结点 $x,y,t$ 之间的三角形不等式．

## 例题

A\* 算法的一个经典应用是解决 k 短路问题．关于该问题的描述、A\* 做法，以及复杂度更优的可持久化可并堆做法，请移步 [k 短路问题](./../graph/kth-path.md) 页面．

本节介绍一个可以用 A\* 算法解决的经典问题．

???+ example "[八数码](https://www.luogu.com.cn/problem/P1379)"
    在 $3\times 3$ 的棋盘上，摆有八个棋子，每个棋子上标有 $1$ 至 $8$ 的某一数字．棋盘中留有一个空格，空格用 $0$ 来表示．空格周围的棋子可以移到空格中，这样原来的位置就会变成空格．给出一种初始布局和目标布局（为了使题目简单，设目标状态如下），找到一种从初始布局到目标布局最少步骤的移动方法．
    
    $$
    \begin{aligned}
    123\\
    804\\
    765
    \end{aligned}
    $$

??? note "解题思路"
    $h$ 函数可以定义为，不在应该在的位置的棋子个数．容易发现，$h$ 既是可采纳的，也是一致的．此题可以使用 A\* 算法求解．

??? note "参考代码"
    ```cpp
    --8<-- "docs/search/code/astar/astar_1.cpp"
    ```

## 参考资料与注释

-   [A\* search algorithm - Wikipedia](https://en.wikipedia.org/wiki/A*_search_algorithm)

[^note1]: 此处的 $h$ 意为 heuristic．详见 [启发式搜索 - 维基百科](https://zh.wikipedia.org/wiki/%E5%90%AF%E5%8F%91%E5%BC%8F%E6%90%9C%E7%B4%A2) 和 [A\* search algorithm - Wikipedia](https://en.wikipedia.org/wiki/A*_search_algorithm#Bounded_relaxation) 的 Bounded relaxation 一节．


## search/backtracking.md

本页面将简要介绍回溯法的概念和应用．

## 简介

回溯法是一种经常被用在 [深度优先搜索（DFS）](./dfs.md) 和 [广度优先搜索（BFS）](./bfs.md) 的技巧．

其本质是：走不通就回头．

## 过程

1.  构造空间树；

2.  进行遍历；

3.  如遇到边界条件，即不再向下搜索，转而搜索另一条链；

4.  达到目标条件，输出结果．

## 例题

???+ example "[USACO 1.5.4 Checker Challenge](https://www.luogu.com.cn/problem/P1219)"
    现在有一个如下的 $6 \times 6$ 的跳棋棋盘，有六个棋子被放置在棋盘上，使得每行，每列，每条对角线（包括两条主对角线的所有对角线）上都至多有一个棋子．
    
    ```plain
    0   1   2   3   4   5   6
      -------------------------
    1 |   | O |   |   |   |   |
      -------------------------
    2 |   |   |   | O |   |   |
      -------------------------
    3 |   |   |   |   |   | O |
      -------------------------
    4 | O |   |   |   |   |   |
      -------------------------
    5 |   |   | O |   |   |   |
      -------------------------
    6 |   |   |   |   | O |   |
      -------------------------
    ```
    
    上面的布局可以用序列 $\{2,4,6,1,3,5\}$ 来描述，第 $i$ 个数字表示在第 $i$ 行的第 $a_i$ 列有一个棋子，如下所示
    
    行号 $i$：$\{1,2,3,4,5,6\}$
    
    列号 $a_i$：$\{2,4,6,1,3,5\}$
    
    这只是跳棋放置的一个方案．请编一个程序找出所有方案并把它们以上面的序列化方法输出，按字典顺序排列．你只需输出前 $3$ 个解并在最后一行输出解的总个数．特别注意：你需要优化你的程序以保证在更大棋盘尺寸下的程序效率．

??? note "参考代码"
    ```cpp
    --8<-- "docs/search/code/backtracking/backtracking_1.cpp"
    ```

???+ example "[迷宫](https://www.luogu.com.cn/problem/P1605)"
    现有一个尺寸为 $N \times M$ 的迷宫，迷宫里有 $T$ 处障碍，障碍处不可通过．给定起点坐标和终点坐标，且每个方格最多经过一次，问有多少种从起点坐标到终点坐标的方案．在迷宫中移动有上、下、左、右四种移动方式，每次只能移动一个方格．数据保证起点上没有障碍．

??? note "参考代码"
    ```cpp
    --8<-- "docs/search/code/backtracking/backtracking_2.cpp"
    ```


## search/bfs.md

## 引入

BFS（广度优先搜索）为图论中的基础算法，详见 [BFS（图论）](../graph/bfs.md) 页面．在 **搜索算法** 中，该算法通常指利用队列结构逐层扩展状态的搜索方式，与图论中的 BFS 算法思想一致，特别适合求解 **最短路径** 或 **最少步骤** 类问题．

## 解释

BFS 的核心思想是 **按层扩展**，从起点开始逐层扫描可到达的位置．首次遇到终点时的路径长度即为最短路径．这种方式保证了搜索的层次性与最优性．

在实际执行中，BFS 会从起点出发，先访问起点的所有直接可到达结点，这些可到达结点构成了搜索的第一层；接着，再以这些可到达结点为新的起点，依次访问它们的邻居，形成第二层；以此类推，不断向外扩展，直至找到目标结点或遍历完所有可达结点．这个过程中，算法会借助队列和访问数组，将每一层新发现的结点（访问数组中还没有记录过的）依次入队，确保同一层的结点按照访问顺序依次被处理，从而严格遵循「按层扩展」的逻辑．

BFS 非常擅于快速求解 **最短路径** 或 **最少步骤**．当算法在某一层首次遇到目标时，此时经过的路径长度（步骤数）必然是最短的．这是因为 BFS 算法的「按层扩展」机制保证了每个结点都是通过最少的步数被访问到：就像从起点出发，沿着最直接的路径不断搜索，直到抵达终点，不会出现绕路或走多余步骤的情况．在这类问题中，BFS 通常也比 DFS 的效率更高．

但是，相较于 DFS，BFS 也有其缺点．通常情况下，BFS 需要更大的内存，缺乏天然的回溯过程，且深度剪枝相对没有 DFS 灵活．

## 例题

???+ example "例题 [Luogu B3625 迷宫寻路](https://www.luogu.com.cn/problem/B3625)"
    在一个 $n \times m$ 的迷宫矩阵中，`.` 表示可通行区域，`#` 表示障碍物．从起点 $(1,1)$ 出发，每次可向上下左右四个方向移动，问是否能到达终点 $(n,m)$．

??? note "解答"
    实现时需要维护一个队列来存储待处理的坐标，并配合访问标记数组避免重复计算．一个结点扩展可到达结点的时候，需要向上下左右拓展，这四个方向分别为 $(x, y + 1)$，$(x, y - 1)$，$(x + 1, y)$，$(x - 1, y)$，在代码中使用了方向数组．注意判断不能拓展到有障碍物的位置．

??? note "参考实现"
    ```cpp
    --8<-- "docs/search/code/bfs/bfs-1.cpp"
    ```

???+ example "例题 [Luogu P1135 奇怪的电梯](https://www.luogu.com.cn/problem/P1135)"
    有 $n$ 层楼和一架电梯．电梯位于第 $i$ 层楼时，向上或向下移动的层数等于一个固定的数字 $k_i$．如果到达的层数不合法，即不在 $1$ 和 $n$ 之间，相应的操作就无法进行．问：从第 $a$ 楼到第 $b$ 楼至少操作几次电梯？如果无法到达，输出 $-1$．

??? note "解答"
    本题需要计算最短路径，这正是 BFS 擅长解决的问题．实现时，需要在队列中同时维护需要处理的楼层位置和从起点 $a$ 出发到达当前楼层的最短距离，并配合访问标记数组避免重复加入同一个元素．一个结点 $i$ 扩展可到达结点的时候，需要向 $i + k_i$ 和 $i - k_i$ 扩展，注意不能到达非法楼层．当扩展到尚未到达的合法楼层时，需要将它加入队列，并记录到达该楼层的最短距离为到达当前所在楼层的最短距离加一．当首次到达结点 $b$ 时，记录的最短距离就是最终答案．
    
    代码中，直接记录距离数组，并利用距离是否为默认值（即 $-1$）来判断结点是否尚未访问．

??? note "参考实现"
    ```cpp
    --8<-- "docs/search/code/bfs/bfs-2.cpp"
    ```

## 习题

-   [Luogu P1443 马的遍历](https://www.luogu.com.cn/problem/P1443)
-   [Luogu P3956 \[NOIP 2017 普及组\] 棋盘](https://www.luogu.com.cn/problem/P3956)
-   [Luogu P1126 机器人搬重物](https://www.luogu.com.cn/problem/P1126)


## search/bidirectional.md

author: FFjet, ChungZH, frank-xjh, hsfzLZH1, Xarfa, AndrewWayne, hcx1204

本页面将简要介绍两种双向搜索算法：「双向同时搜索」和「Meet in the middle」．

## 双向同时搜索

### 定义

双向同时搜索的基本思路是从状态图上的起点和终点同时开始进行 [广搜](./bfs.md) 或 [深搜](./dfs.md)．

如果发现搜索的两端相遇了，那么可以认为是获得了可行解．

### 过程

双向广搜的步骤：

```text
将开始结点和目标结点加入队列 q
标记开始结点为 1
标记目标结点为 2
while (队列 q 不为空)
{
  从 q.front() 扩展出新的 s 个结点
  
  如果 新扩展出的结点已经被其他数字标记过
    那么 表示搜索的两端碰撞
    那么 循环结束
  
  如果 新的 s 个结点是从开始结点扩展来的
    那么 将这个 s 个结点标记为 1 并且入队 q 
  
  如果 新的 s 个结点是从目标结点扩展来的
    那么 将这个 s 个结点标记为 2 并且入队 q
}
```

### 例题

???+ note "例题 [八数码难题](https://www.luogu.com.cn/problem/P1379)"
    在 $3\times 3$ 的棋盘上，摆有八个棋子，每个棋子上标有 $1$ 至 $8$ 的某一数字．棋盘中留有一个空格，空格用 $0$ 来表示．空格周围的棋子可以移到空格中．要求解的问题是：给出一种初始布局（初始状态）和目标布局（为了使题目简单，设目标状态为 $123804765$），找到一种最少步骤的移动方法，实现从初始布局到目标布局的转变．

??? note "解题思路"
    很好想出暴力 bfs．本题使用暴力 bfs 也不会超时．但是这里把它作为双向同时搜索的例题．我们可以使用两个 bfs，一个从起点状态开始正着搜，一个从终点状态开始反着搜，交替使用两个 bfs，搜索树的大小会大大减小．当其中一个 bfs 搜出另一个 bfs 已经搜出的状态，即可得到答案．

??? note "参考代码"
    ```cpp
    --8<-- "docs/search/code/bidirectional/bidirectional_1.cpp"
    ```

## Meet in the middle

???+ warning "Warning"
    本节要介绍的不是 [**二分搜索**](../basic/binary.md)（二分搜索的另外一个译名为「折半搜索」）．

### 引入

Meet in the middle 算法没有正式译名，常见的翻译为「折半搜索」、「双向搜索」或「中途相遇」．

它适用于输入数据较小，但还没小到能直接使用暴力搜索的情况．

### 过程

Meet in the middle 算法的主要思想是将整个搜索过程分成两半，分别搜索，最后将两半的结果合并．

### 性质

暴力搜索的复杂度往往是指数级的，而改用 meet in the middle 算法后复杂度的指数可以减半，即让复杂度从 $O(a^b)$ 降到 $O(a^{b/2})$．

### 例题

???+ note "例题 [「USACO09NOV」灯 Lights](https://www.luogu.com.cn/problem/P2962)"
    有 $n$ 盏灯，每盏灯与若干盏灯相连，每盏灯上都有一个开关，如果按下一盏灯上的开关，这盏灯以及与之相连的所有灯的开关状态都会改变．一开始所有灯都是关着的，你需要将所有灯打开，求最小的按开关次数．
    
    $1\le n\le 35$．

??? note "解题思路"
    如果这道题暴力 DFS 找开关灯的状态，时间复杂度就是 $O(2^{n})$, 显然超时．不过，如果我们用 meet in middle 的话，时间复杂度可以优化至 $O(n2^{n/2})$．meet in middle 就是让我们先找一半的状态，也就是找出只使用编号为 $1$ 到 $\mathrm{mid}$ 的开关能够到达的状态，再找出只使用另一半开关能到达的状态．如果前半段和后半段开启的灯互补，将这两段合并起来就得到了一种将所有灯打开的方案．具体实现时，可以把前半段的状态以及达到每种状态的最少按开关次数存储在 map 里面，搜索后半段时，每搜出一种方案，就把它与互补的第一段方案合并来更新答案．

??? note "参考代码"
    ```cpp
    --8<-- "docs/search/code/bidirectional/bidirectional_2.cpp"
    ```

## 外部链接

-   [What is meet in the middle algorithm w.r.t. competitive programming? - Quora](https://www.quora.com/What-is-meet-in-the-middle-algorithm-w-r-t-competitive-programming)
-   [Meet in the Middle Algorithm - YouTube](https://www.youtube.com/watch?v=57SUNQL4JFA)


## search/dfs.md

## 引入

DFS 为图论中的概念，详见 [DFS（图论）](../graph/dfs.md) 页面．在 **搜索算法** 中，该词常常指利用递归函数方便地实现暴力枚举的算法，与图论中的 DFS 算法有一定相似之处，但并不完全相同．

## 解释

考虑这个例子：

???+ note "例题"
    把正整数 $n$ 分解为 $3$ 个正整数，如 $6=1+2+3$，排在后面的数必须大于等于前面的数，输出所有方案．

对于这个问题，如果不知道搜索，应该怎么办呢？当然是三重循环，参考代码如下：

???+ note "实现"
    === "C++"
        ```cpp
        for (int i = 1; i <= n; ++i)
          for (int j = i; j <= n; ++j)
            for (int k = j; k <= n; ++k)
              if (i + j + k == n) printf("%d = %d + %d + %d\n", n, i, j, k);
        ```
    
    === "Python"
        ```python
        for i in range(1, n + 1):
            for j in range(i, n + 1):
                for k in range(j, n + 1):
                    if i + j + k == n:
                        print("%d = %d + %d + %d" % (n, i, j, k))
        ```
    
    === "Java"
        ```Java
        for (int i = 1; i < n + 1; i++) {
            for (int j = i; j < n + 1; j++) {
                for (int k = j; k < n + 1; k++) {
                    if (i + j + k == n) System.out.printf("%d = %d + %d + %d%n", n, i, j, k);
                }
            }
        }
        ```

那如果是分解成四个整数呢？再加一重循环？那分解成小于等于 $m$ 个整数呢？

这时候就需要用到递归搜索了．该类搜索算法的特点在于，将要搜索的目标分成若干「层」，每层基于前几层的状态进行决策，直到达到目标状态．

考虑上述问题，即将正整数 $n$ 分解成不超过 $m$ 个正整数之和，且排在后面的数必须大于等于前面的数，并输出所有方案．

设一组方案将正整数 $n$ 分解成 $k$ 个正整数 $a_1, a_2, \ldots, a_k$ 的和．将问题分层，第 $i$ 层决定 $a_i$．则为了进行第 $i$ 层决策，我们需要记录三个状态变量：$n-\sum_{j=1}^i{a_j}$，表示后面所有正整数的和；$a_{i-1}$，表示前一层的正整数，以确保正整数递增；以及 $i$，确保我们最多输出 $m$ 个正整数．为了记录方案，我们用 `arr` 数组，第 $i$ 项表示 $a_i$. 注意到 `arr` 实际上是一个长度为 $i$ 的栈．

代码如下：

???+ note "实现"
    === "C++"
        ```cpp
        int m, arr[103];  // arr 用于记录方案
        
        void dfs(int n, int i, int a) {
          if (n == 0) {
            for (int j = 1; j <= i - 1; ++j) printf("%d ", arr[j]);
            printf("\n");
          }
          if (i <= m) {
            for (int j = a; j <= n; ++j) {
              arr[i] = j;
              dfs(n - j, i + 1, j);  // 请仔细思考该行含义．
            }
          }
        }
        
        // 主函数
        scanf("%d%d", &n, &m);
        dfs(n, 1, 1);
        ```
    
    === "Python"
        ```python
        arr = [0] * 103  # arr 用于记录方案
        
        
        def dfs(n, i, a):
            if n == 0:
                print(arr[1:i])
            if i <= m:
                for j in range(a, n + 1):
                    arr[i] = j
                    dfs(n - j, i + 1, j)  # 请仔细思考该行含义．
        
        
        # 主函数
        n, m = map(int, input().split())
        dfs(n, 1, 1)
        ```
    
    === "Java"
        ```Java
        static int m;
        
        // arr 用于记录方案
        static int[] arr = new int[103];
        
        public static void dfs(int n, int i, int a) {
            if (n == 0) {
                for (int j = 1; j <= i - 1; j++) System.out.printf("%d ", arr[j]);
                System.out.println();
            }
            if (i <= m) {
                for (int j = a; j <= n; ++j) {
                    arr[i] = j;
                    dfs(n - j, i + 1, j); // 请仔细思考该行含义．
                }
            }
        }
        
        // 主函数
        final int N = new Scanner(System.in).nextInt();
        m = new Scanner(System.in).nextInt();
        dfs(N, 1, 1);
        ```

## 例题

???+ note "[Luogu P1706 全排列问题](https://www.luogu.com.cn/problem/P1706)"
    ```cpp
    --8<-- "docs/search/code/dfs/dfs_1.cpp"
    ```


## search/dlx.md

author: LeverImmy, 383494

本页面将介绍精确覆盖问题、重复覆盖问题，解决这两个问题的算法「X 算法」，以及用来优化 X 算法的双向十字链表 Dancing Link．本页也将介绍如何在建模的配合下使用 DLX 解决一些搜索题．

## 精确覆盖问题

### 定义

精确覆盖问题（英文：Exact Cover Problem）是指给定许多集合 $S_i (1 \le i \le n)$ 以及一个集合 $X$，求满足以下条件的无序多元组 $(T_1, T_2, \cdots , T_m)$：

1.  $\forall i, j \in [1, m],T_i\bigcap T_j = \varnothing (i \neq j)$
2.  $X = \bigcup\limits_{i = 1}^{m}T_i$
3.  $\forall i \in[1, m], T_i \in \{S_1, S_2, \cdots, S_n\}$

### 解释

例如，若给出

$$
\begin{aligned}
  & S_1 = \{5, 9, 17\} \\
  & S_2 = \{1, 8, 119\} \\
  & S_3 = \{3, 5, 17\} \\
  & S_4 = \{1, 8\} \\
  & S_5 = \{3, 119\} \\
  & S_6 = \{8, 9, 119\} \\
  & X = \{1, 3, 5, 8, 9, 17, 119\}
\end{aligned}
$$

则 $(S_1, S_4, S_5)$ 为一组合法解．

### 问题转化

将 $\bigcup\limits_{i = 1}^{n}S_i$ 中的所有数离散化，可以得到这么一个模型：

> 给定一个 01 矩阵，你可以选择一些行（row），使得最终每列（column）[^note1]都恰好有一个 1．
> 举个例子，我们对上文中的例子进行建模，可以得到这么一个矩阵：

$$
\begin{pmatrix}
0 & 0 & 1 & 0 & 1 & 1 & 0 \\
1 & 0 & 0 & 1 & 0 & 0 & 1 \\
0 & 1 & 1 & 0 & 0 & 1 & 0 \\
1 & 0 & 0 & 1 & 0 & 0 & 0 \\
0 & 1 & 0 & 0 & 0 & 0 & 1 \\
0 & 0 & 0 & 1 & 1 & 0 & 1
\end{pmatrix}
$$

> 其中第 $i$ 行表示着 $S_i$，而这一行的每个数依次表示 $[1 \in S_i],[3 \in S_i],[5 \in S_i],\cdots,[119 \in S_i]$．

### 实现

#### 暴力 1

一种方法是枚举选择哪些行，最后检查这个方案是否合法．

因为每一行都有选或者不选两种状态，所以枚举行的时间复杂度是 $O(2^n)$ 的；

而每次检查都需要 $O(nm)$ 的时间复杂度．所以总的复杂度是 $O(nm\cdot2^n)$．

??? note "实现"
    ```cpp
    int ok = 0;
    for (int state = 0; state < 1 << n; ++state) {  // 枚举每行是否被选
      for (int i = 1; i <= n; ++i)
        if ((1 << i - 1) & state)
          for (int j = 1; j <= m; ++j) a[i][j] = 1;
      int flag = 1;
      for (int j = 1; j <= m; ++j)
        for (int i = 1, bo = 0; i <= n; ++i)
          if (a[i][j]) {
            if (bo)
              flag = 0;
            else
              bo = 1;
          }
      if (!flag)
        continue;
      else {
        ok = 1;
        for (int i = 1; i <= n; ++i)
          if ((1 << i - 1) & state) printf("%d ", i);
        puts("");
      }
      memset(a, 0, sizeof(a));
    }
    if (!ok) puts("No solution.");
    ```

#### 暴力 2

考虑到 01 矩阵的特殊性质，每一行都可以看做一个 $m$ 位二进制数．

因此原问题转化为

> 给定 $n$ 个 $m$ 位二进制数，要求选择一些数，使得任意两个数的与都为 0，且所有数的或为 $2^m - 1$．`tmp` 表示的是截至目前被选中的二进制数的或．

因为每一行都有选或者不选两种状态，所以枚举行的时间复杂度为 $O(2^n)$；

而每次计算 `tmp` 都需要 $O(n)$ 的时间复杂度．所以总的复杂度为 $O(n\cdot2^n)$．

??? note "实现"
    ```cpp
    int ok = 0;
    for (int i = 1; i <= n; ++i)
      for (int j = m; j >= 1; --j) num[i] = num[i] << 1 | a[i][j];
    for (int state = 0; state < 1 << n; ++state) {
      int tmp = 0;
      bool flag = true;
      for (int i = 1; i <= n; ++i)
        if ((1 << i - 1) & state) {
          if (tmp & num[i]) {
            flag = false;
            break;
          }
          tmp |= num[i];
        }
      if (flag && tmp == (1 << m) - 1) {
        ok = 1;
        for (int i = 1; i <= n; ++i)
          if ((1 << i - 1) & state) printf("%d ", i);
        puts("");
      }
    }
    if (!ok) puts("No solution.");
    ```

## 重复覆盖问题

重复覆盖问题与精确覆盖问题类似，但没有对元素相似性的限制．下文介绍的 [X 算法](#x-算法) 原本针对精确覆盖问题，但经过一些修改和优化（已标注在其中）同样可以高效地解决重复覆盖问题．

## X 算法

Donald E. Knuth 提出了 X 算法 (Algorithm X)，其思想与刚才的暴力差不多，但是方便优化．

### 过程

继续以上文中中提到的例子为载体，得到一个这样的 01 矩阵：

$$
\begin{pmatrix}
  0 & 0 & 1 & 0 & 1 & 1 & 0 \\
  1 & 0 & 0 & 1 & 0 & 0 & 1 \\
  0 & 1 & 1 & 0 & 0 & 1 & 0 \\
  1 & 0 & 0 & 1 & 0 & 0 & 0 \\
  0 & 1 & 0 & 0 & 0 & 0 & 1 \\
  0 & 0 & 0 & 1 & 1 & 0 & 1
\end{pmatrix}
$$

1.  此时第一行有 $3$ 个 $1$，第二行有 $3$ 个 $1$，第三行有 $3$ 个 $1$，第四行有 $2$ 个 $1$，第五行有 $2$ 个 $1$，第六行有 $3$ 个 $1$．选择第一行，将它删除，并将所有 $1$ 所在的列打上标记；

    $$
    \begin{pmatrix}
      \color{Blue}0 & \color{Blue}0 & \color{Blue}1 & \color{Blue}0 & \color{Blue}1 & \color{Blue}1 & \color{Blue}0 \\
      1 & 0 & \color{Red}0 & 1 & \color{Red}0 & \color{Red}0 & 1 \\
      0 & 1 & \color{Red}1 & 0 & \color{Red}0 & \color{Red}1 & 0 \\
      1 & 0 & \color{Red}0 & 1 & \color{Red}0 & \color{Red}0 & 0 \\
      0 & 1 & \color{Red}0 & 0 & \color{Red}0 & \color{Red}0 & 1 \\
      0 & 0 & \color{Red}0 & 1 & \color{Red}1 & \color{Red}0 & 1
      \end{pmatrix}
    $$

2.  选择所有被标记的列，将它们删除，并将这些列中含 $1$ 的行打上标记（重复覆盖问题无需打标记）；

    $$
    \begin{pmatrix}
      \color{Blue}0 & \color{Blue}0 & \color{Blue}1 & \color{Blue}0 & \color{Blue}1 & \color{Blue}1 & \color{Blue}0 \\
      1 & 0 & \color{Blue}0 & 1 & \color{Blue}0 & \color{Blue}0 & 1 \\
      \color{Red}0 & \color{Red}1 & \color{Blue}1 & \color{Red}0 & \color{Blue}0 & \color{Blue}1 & \color{Red}0 \\
      1 & 0 & \color{Blue}0 & 1 & \color{Blue}0 & \color{Blue}0 & 0 \\
      0 & 1 & \color{Blue}0 & 0 & \color{Blue}0 & \color{Blue}0 & 1 \\
      \color{Red}0 & \color{Red}0 & \color{Blue}0 & \color{Red}1 & \color{Blue}1 & \color{Blue}0 & \color{Red}1
    \end{pmatrix}
    $$

3.  选择所有被标记的行，将它们删除；

    $$
    \begin{pmatrix}
      \color{Blue}0 & \color{Blue}0 & \color{Blue}1 & \color{Blue}0 & \color{Blue}1 & \color{Blue}1 & \color{Blue}0 \\
      1 & 0 & \color{Blue}0 & 1 & \color{Blue}0 & \color{Blue}0 & 1 \\
      \color{Blue}0 & \color{Blue}1 & \color{Blue}1 & \color{Blue}0 & \color{Blue}0 & \color{Blue}1 & \color{Blue}0 \\
      1 & 0 & \color{Blue}0 & 1 & \color{Blue}0 & \color{Blue}0 & 0 \\
      0 & 1 & \color{Blue}0 & 0 & \color{Blue}0 & \color{Blue}0 & 1 \\
      \color{Blue}0 & \color{Blue}0 & \color{Blue}0 & \color{Blue}1 & \color{Blue}1 & \color{Blue}0 & \color{Blue}1
    \end{pmatrix}
    $$

    **这表示这一行已被选择，且这一行的所有 $1$ 所在的列不能有其他 $1$ 了**．

    于是得到一个新的小 01 矩阵：

    $$
    \begin{pmatrix}
      1 & 0 & 1 & 1 \\
      1 & 0 & 1 & 0 \\
      0 & 1 & 0 & 1
    \end{pmatrix}
    $$

4.  此时第一行（原来的第二行）有 $3$ 个 $1$，第二行（原来的第四行）有 $2$ 个 $1$，第三行（原来的第五行）有 $2$ 个 $1$．选择第一行（原来的第二行），将它删除，并将所有 $1$ 所在的列打上标记；

    $$
    \begin{pmatrix}
      \color{Blue}1 & \color{Blue}0 & \color{Blue}1 & \color{Blue}1 \\
      \color{Red}1 & 0 & \color{Red}1 & \color{Red}0 \\
      \color{Red}0 & 1 & \color{Red}0 & \color{Red}1
    \end{pmatrix}
    $$

5.  选择所有被标记的列，将它们删除，并将这些列中含 $1$ 的行打上标记；

    $$
    \begin{pmatrix}
      \color{Blue}1 & \color{Blue}0 & \color{Blue}1 & \color{Blue}1 \\
      \color{Blue}1 & \color{Red}0 & \color{Blue}1 & \color{Blue}0 \\
      \color{Blue}0 & \color{Red}1 & \color{Blue}0 & \color{Blue}1
    \end{pmatrix}
    $$

6.  选择所有被标记的行，将它们删除；

    $$
    \begin{pmatrix}
      \color{Blue}1 & \color{Blue}0 & \color{Blue}1 & \color{Blue}1 \\
      \color{Blue}1 & \color{Blue}0 & \color{Blue}1 & \color{Blue}0 \\
      \color{Blue}0 & \color{Blue}1 & \color{Blue}0 & \color{Blue}1
    \end{pmatrix}
    $$

    这样就得到了一个空矩阵．但是上次删除的行 `1 0 1 1` 不是全 $1$ 的，说明选择有误；

    $$
    \begin{pmatrix}
    \end{pmatrix}
    $$

7.  回溯到步骤 4，考虑选择第二行（原来的第四行），将它删除，并将所有 $1$ 所在的列打上标记；

    $$
    \begin{pmatrix}
      \color{Red}1 & 0 & \color{Red}1 & 1 \\
      \color{Blue}1 & \color{Blue}0 & \color{Blue}1 & \color{Blue}0 \\
      \color{Red}0 & 1 & \color{Red}0 & 1
    \end{pmatrix}
    $$

8.  选择所有被标记的列，将它们删除，并将这些列中含 $1$ 的行打上标记；

    $$
    \begin{pmatrix}
      \color{Blue}1 & \color{Red}0 & \color{Blue}1 & \color{Red}1 \\
      \color{Blue}1 & \color{Blue}0 & \color{Blue}1 & \color{Blue}0 \\
      \color{Blue}0 & 1 & \color{Blue}0 & 1
    \end{pmatrix}
    $$

9.  选择所有被标记的行，将它们删除；

    $$
    \begin{pmatrix}
      \color{Blue}1 & \color{Blue}0 & \color{Blue}1 & \color{Blue}1 \\
      \color{Blue}1 & \color{Blue}0 & \color{Blue}1 & \color{Blue}0 \\
      \color{Blue}0 & 1 & \color{Blue}0 & 1
      \end{pmatrix}
    $$

    于是我们得到了这样的一个矩阵：

    $$
    \begin{pmatrix}
      1 & 1
    \end{pmatrix}
    $$

10. 此时第一行（原来的第五行）有 $2$ 个 $1$，将它们全部删除，得到一个空矩阵：

    $$
    \begin{pmatrix}
    \end{pmatrix}
    $$

11. 上一次删除的时候，删除的是全 $1$ 的行，因此成功，算法结束．

    答案即为被删除的三行：$1, 4, 5$．

强烈建议自己模拟一遍矩阵删除、还原与回溯的过程后，再接着阅读下文．

通过上述步骤，可将 X 算法的流程概括如下：

1.  对于现在的矩阵 $M$，选择并标记一行 $r$，将 $r$ 添加至 $S$ 中；
2.  如果尝试了所有的 $r$ 却无解，则算法结束，输出无解；
3.  标记与 $r$ 相关的行 $r_i$ 和 $c_i$（相关的行和列与 [X 算法](#过程) 中第 2 步定义相同，下同）；
4.  删除所有标记的行和列，得到新矩阵 $M'$；
5.  如果 $M'$ 为空，且 $r$ 为全 $1$，则算法结束，输出被删除的行组成的集合 $S$；

    如果 $M'$ 为空，且 $r$ 不全为 $1$，则恢复与 $r$ 相关的行 $r_i$ 以及列 $c_i$，跳转至步骤 1；

    如果 $M'$ 不为空，则跳转至步骤 1．

不难看出，X 算法需要大量的「删除行」、「删除列」和「恢复行」、「恢复列」的操作．

一个朴素的想法是，使用一个二维数组存放矩阵，再用四个数组分别存放每一行与之相邻的行编号，每次删除和恢复仅需更新四个数组中的元素．但由于一般问题的矩阵中 0 的数量远多于 1 的数量，这样做的空间复杂度难以接受．

Donald E. Knuth 想到了用双向十字链表来维护这些操作．

而在双向十字链表上不断跳跃的过程被形象地比喻成「跳跃」，因此被用来优化 X 算法的双向十字链表也被称为「Dancing Links」．

## Dancing Links 优化的 X 算法

### 预编译命令

```cpp
#define IT(i, A, x) for (i = A[x]; i != x; i = A[i])
```

### 定义

双向十字链表中存在四个指针域，分别指向上、下、左、右的元素；且每个元素 $i$ 在整个双向十字链表系中都对应着一个格子，因此还要表示 $i$ 所在的列和所在的行，如图所示：

![dlx-1.svg](./images/dlx-1.svg)

大型的双向链表则更为复杂：

![dlx-2.svg](./images/dlx-2.svg)

每一行都有一个行首指示，每一列都有一个列指示．

行首指示为 `first[]`，列指示是我们新建的 $c + 1$ 个哨兵结点．值得注意的是，**行首指示并非是链表中的哨兵结点**．它是虚拟的，类似于邻接表中的 `first[]` 数组，**直接指向** 这一行中的首元素．

同时，每一列都有一个 `siz[]` 表示这一列的元素个数．

特殊地，$0$ 号结点无右结点等价于这个 Dancing Links 为空．

```cpp
constexpr int MS = 1e5 + 5;
int n, m, idx, first[MS], siz[MS];
int L[MS], R[MS], U[MS], D[MS];
int col[MS], row[MS];
```

### 过程

#### remove 操作

`remove(c)` 表示在 Dancing Links 中删除第 $c$ 列以及与其相关的行和列．

先将 $c$ 删除，此时：

-   $c$ 左侧的结点的右结点应为 $c$ 的右结点．
-   $c$ 右侧的结点的左结点应为 $c$ 的左结点．

即 `L[R[c]] = L[c], R[L[c]] = R[c];`．

![dlx-3.svg](./images/dlx-3.svg)

然后顺着这一列往下走，把走过的每一行都删掉．

如何删掉每一行呢？枚举当前行的指针 $j$，此时：

-   $j$ 上方的结点的下结点应为 $j$ 的下结点．
-   $j$ 下方的结点的上结点应为 $j$ 的上结点．

注意要修改每一列的元素个数．

即 `U[D[j]] = U[j], D[U[j]] = D[j], --siz[col[j]];`．

![dlx-4.svg](./images/dlx-4.svg)

`remove` 函数的代码实现如下：

???+ note "实现"
    ```cpp
    void remove(const int &c) {
      int i, j;
      L[R[c]] = L[c], R[L[c]] = R[c];
      // 顺着这一列从上往下遍历
      IT(i, D, c)
      // 顺着这一行从左往右遍历
      IT(j, R, i)
      U[D[j]] = U[j], D[U[j]] = D[j], --siz[col[j]];
    }
    ```

#### recover 操作

`recover(c)` 表示在 Dancing Links 中还原第 $c$ 列以及与其相关的行和列．

`recover(c)` 即 `remove(c)` 的逆操作，这里不再赘述．

**值得注意的是，** `recover(c)` **的所有操作的顺序与**  `remove(c)` **的操作恰好相反．**

`recover(c)` 的代码实现如下：

???+ note "实现"
    ```cpp
    void recover(const int &c) {
      int i, j;
      IT(i, U, c) IT(j, L, i) U[D[j]] = D[U[j]] = j, ++siz[col[j]];
      L[R[c]] = R[L[c]] = c;
    }
    ```

#### build 操作

`build(r, c)` 表示新建一个大小为 $r \times c$，即有 $r$ 行，$c$ 列的 Dancing Links．

新建 $c + 1$ 个结点作为列指示．

第 $i$ 个点的左结点为 $i - 1$，右结点为 $i + 1$，上结点为 $i$，下结点为 $i$．特殊地，$0$ 结点的左结点为 $c$，$c$ 结点的右结点为 $0$．

于是我们得到了一个环状双向链表：

![dlx-5.svg](./images/dlx-5.svg)

这样就初始化了一个 Dancing Links．

`build(r, c)` 的代码实现如下：

???+ note "实现"
    ```cpp
    void build(const int &r, const int &c) {
      n = r, m = c;
      for (int i = 0; i <= c; ++i) {
        L[i] = i - 1, R[i] = i + 1;
        U[i] = D[i] = i;
      }
      L[0] = c, R[c] = 0, idx = c;
      memset(first, 0, sizeof(first));
      memset(siz, 0, sizeof(siz));
    }
    ```

#### insert 操作

`insert(r, c)` 表示在第 $r$ 行，第 $c$ 列插入一个结点．

插入操作分为两种情况：

-   如果第 $r$ 行没有元素，那么直接插入一个元素，并使 `first[r]` 指向这个元素．

    这可以通过 `first[r] = L[idx] = R[idx] = idx;` 来实现．

-   如果第 $r$ 行有元素，那么将这个新元素用一种特殊的方式与 $c$ 和 $first(r)$ 连接起来．

    设这个新元素为 $idx$，然后：

    -   把 $idx$ 插入到 $c$ 的正下方，此时：

        -   $idx$ 下方的结点为原来 $c$ 的下结点；
        -   $idx$ 下方的结点（即原来 $c$ 的下结点）的上结点为 $idx$;
        -   $idx$ 的上结点为 $c$；
        -   $c$ 的下结点为 $idx$．

        注意记录 $idx$ 的所在列和所在行，以及更新这一列的元素个数．

        ```cpp
        col[++idx] = c, row[idx] = r, ++siz[c];
        U[idx] = c, D[idx] = D[c], U[D[c]] = idx, D[c] = idx;
        ```

        **强烈建议读者完全掌握这几步的顺序后再继续阅读本文．**

    -   把 $idx$ 插入到 $first(r)$ 的正右方，此时：

        -   $idx$ 右侧的结点为原来 $first(r)$ 的右结点；
        -   原来 $first(r)$ 右侧的结点的左结点为 $idx$；
        -   $idx$ 的左结点为 $first(r)$；
        -   $first(r)$ 的右结点为 $idx$．

        ```cpp
        L[idx] = first[r], R[idx] = R[first[r]];
        L[R[first[r]]] = idx, R[first[r]] = idx;
        ```

        **强烈建议读者完全掌握这几步的顺序后再继续阅读本文．**

`insert(r, c)` 这个操作可以通过图片来辅助理解：

![dlx-6.svg](./images/dlx-6.svg)

留心曲线箭头的方向．

`insert(r, c)` 的代码实现如下：

???+ note "实现"
    ```cpp
    void insert(const int &r, const int &c) {
      row[++idx] = r, col[idx] = c, ++siz[c];
      U[idx] = c, D[idx] = D[c], U[D[c]] = idx, D[c] = idx;
      if (!first[r])
        first[r] = L[idx] = R[idx] = idx;
      else {
        L[idx] = first[r], R[idx] = R[first[r]];
        L[R[first[r]]] = idx, R[first[r]] = idx;
      }
    }
    ```

#### dance 操作

`dance()` 即为递归地删除以及还原各个行列的过程．

1.  如果 $0$ 号结点没有右结点，那么矩阵为空，记录答案并返回；
2.  选择列元素个数最少的一列，并删掉这一列；
3.  遍历这一列所有有 $1$ 的行，枚举它是否被选择；
4.  递归调用 `dance()`，如果可行，则返回；如果不可行，则恢复被选择的行；
5.  如果无解，则返回．

`dance()` 的代码实现如下：

???+ note "实现"
    ```cpp
    bool dance(int dep) {
      int i, j, c = R[0];
      if (!R[0]) {
        ans = dep;
        return true;
      }
      IT(i, R, 0) if (siz[i] < siz[c]) c = i;
      remove(c);
      IT(i, D, c) {
        stk[dep] = row[i];
        IT(j, R, i) remove(col[j]);
        if (dance(dep + 1)) return true;
        IT(j, L, i) recover(col[j]);
      }
      recover(c);
      return false;
    }
    ```

其中 `stk[]` 用来记录答案．

注意我们每次优先选择列元素个数最少的一列进行删除，这样能保证程序具有一定的启发性，使搜索树分支最少．

对于重复覆盖问题，在搜索时可以用估价函数（与 [A\*](astar.md) 中类似）进行剪枝：若当前最好情况下所选行数超过目前最优解，则可以直接返回．

## 模板

??? note "[模板代码](https://www.luogu.com.cn/problem/P4929)"
    ```cpp
    --8<-- "docs/search/code/dlx/dlx_1.cpp"
    ```

## 性质

DLX 递归及回溯的次数与矩阵中 $1$ 的个数有关，与矩阵的 $r, c$ 等参数无关．因此，它的时间复杂度是 **指数级** 的，理论复杂度大概在 $O(c^n)$ 左右，其中 $c$ 为某个非常接近于 $1$ 的常数，$n$ 为矩阵中 $1$ 的个数．

但实际情况下 DLX 表现良好，一般能解决大部分的问题．

## 建模

DLX 的难点，不全在于链表的建立，而在于建模．

请确保已经完全掌握 DLX 模板后再继续阅读本文．

我们每拿到一个题，应该考虑行和列所表示的意义：

-   行表示*决策*，因为每行对应着一个集合，也就对应着选/不选；

-   列表示*状态*，因为第 $i$ 列对应着某个条件 $P_i$．

对于某一行而言，由于不同的列的值不尽相同，我们 **由不同的状态，定义了一个决策**．

### 例题 1 [P1784 数独](https://www.luogu.com.cn/problem/P1784)

??? note "解题思路"
    先考虑决策是什么．
    
    在这一题中，每一个决策可以用形如 $(r, c, w)$ 的有序三元组表示．
    
    注意到「宫」并不是决策的参数，因为它 **可以被每个确定的 $(r, c)$ 表示**．
    
    因此有 $9 \times 9 \times 9 = 729$ 行．
    
    再考虑状态是什么．
    
    我们思考一下 $(r, c, w)$ 这个决策将会造成什么影响．记 $(r, c)$ 所在的宫为 $b$．
    
    1.  第 $r$ 行用了一个 $w$（用 $9 \times 9 = 81$ 列表示）；
    2.  第 $c$ 列用了一个 $w$（用 $9 \times 9 = 81$ 列表示）；
    3.  第 $b$ 宫用了一个 $w$（用 $9 \times 9 = 81$ 列表示）；
    4.  $(r, c)$ 中填入了一个数（用 $9 \times 9 = 81$ 列表示）．
    
    因此有 $81 \times 4 = 324$ 列，共 $729 \times 4 = 2916$ 个 $1$．
    
    至此，我们成功地将 $9 \times 9$ 的数独问题转化成了一个 **有 $729$ 行，$324$ 列，共 $2916$ 个 $1$** 的精确覆盖问题．

??? note "参考代码"
    ```cpp
    --8<-- "docs/search/code/dlx/dlx_2.cpp"
    ```

### 例题 2 [靶形数独](https://www.luogu.com.cn/problem/P1074)

??? note "解题思路"
    这一题与 [数独](https://www.luogu.com.cn/problem/P1784) 的模型构建 **一模一样**，主要区别在于答案的更新．
    
    这一题可以开一个权值数组，每次找到一组数独的解时，
    
    每个位置上的数乘上对应的权值计入答案即可．

??? note "参考代码"
    ```cpp
    --8<-- "docs/search/code/dlx/dlx_3.cpp"
    ```

### 例题 3 [「NOI2005」智慧珠游戏](https://www.luogu.com.cn/problem/P4205)

??? note "解题思路"
    定义：题中给我们的智慧珠的形态，称为这个智慧珠的*标准形态*．
    
    显然，我们可以通过改变两个参数 $d$（表示顺时针旋转 $90^{\circ}$ 的次数）和 $f$（是否水平翻转）来改变这个智慧珠的形态．
    
    仍然，我们先考虑决策是什么．
    
    在这一题中，每一个决策可以用形如 $(v, d, f, i)$ 的有序五元组表示．
    
    表示第 $i$ 个智慧珠的*标准形态*的左上角的位置，序号为 $v$，经过了 $d$ 次顺时针转 $90^{\circ}$．
    
    巧合的是，我们可以令 $f = 1$ 时不水平翻转，$f = -1$ 时水平翻转，从而达到简化代码的目的．
    
    因此有 $55 \times 4 \times 2 \times 12 = 5280$ 行．
    
    需要注意的是，因为一些不合法的填充，如 $(1, 0, 1, 4)$，
    
    所以 **在实际操作中，空的智慧珠棋盘也只需要建出 $2730$ 行．**
    
    再考虑状态是什么．
    
    这一题的状态比较简单．
    
    我们思考一下，$(v, d, f, i)$ 这个决策会造成什么影响．
    
    1.  某些格子被占了（用 $55$ 列表示）；
    2.  第 $i$ 个智慧珠被用了（用 $12$ 列表示）．
    
    因此有 $55 + 12 = 67$ 列，共 $5280 \times (5 + 1) = 31680$ 个 $1$．
    
    至此，我们成功地将智慧珠游戏转化成了一个 **有 $5280$ 行，$67$ 列，共 $31680$ 个 $1$** 的精确覆盖问题．

??? note "参考代码"
    ```cpp
    --8<-- "docs/search/code/dlx/dlx_4.cpp"
    ```

## 习题

-   [SUDOKU - Sudoku](https://www.spoj.com/problems/SUDOKU/)
-   [「kuangbin 带你飞」专题三 Dancing Links](https://vjudge.net/contest/65998#overview)

## 外部链接

-   [跳跃的舞者，舞蹈链（Dancing Links）算法——求解精确覆盖问题 - 万仓一黍](https://www.cnblogs.com/grenet/p/3145800.html)
-   [搜索：DLX 算法 - 静听风吟．](https://www.cnblogs.com/aininot260/p/9629926.html)
-   [《算法竞赛入门经典 - 训练指南》](https://book.douban.com/subject/35431537/)

## 注释

[^note1]: （两岸用语差异）台灣：直行（column）、橫列（row）


## search/heuristic.md

本页面将简要介绍启发式搜索及其用法．

## 定义

启发式搜索（英文：heuristic search）是一种在普通搜索算法的基础上引入了启发式函数的搜索算法．

启发式函数的作用是基于已有的信息对搜索的每一个分支选择都做估价，进而选择分支．简单来说，启发式搜索就是对取和不取都做分析，从中选取更优解或删去无效解．

## 例题

由于概念过于抽象，这里使用例题讲解．

???+ note "[「NOIP2005 普及组」采药](https://www.luogu.com.cn/problem/P1048)"
    题目大意：有 $N$ 种物品和一个容量为 $W$ 的背包，每种物品有重量 $w_i$ 和价值 $v_i$ 两种属性，要求选若干个物品（每种物品只能选一次）放入背包，使背包中物品的总价值最大，且背包中物品的总重量不超过背包的容量．

??? note "解题思路"
    我们写一个估价函数 $f$，可以剪掉所有无效的 $0$ 枝条（就是剪去大量无用不选枝条）．
    
    估价函数 $f$ 的运行过程如下：
    
    我们在取的时候判断一下是不是超过了规定体积（可行性剪枝）；在不取的时候判断一下不取这个时，剩下的药所有的价值 + 现有的价值是否大于目前找到的最优解（最优性剪枝）．

??? note "示例代码"
    ```cpp
    --8<-- "docs/search/code/heuristic/heuristic_1.cpp"
    ```


## search/idastar.md

前置知识：[A\* 算法](./astar.md)、[迭代加深搜索](./iterative.md)

本页面将简要介绍 IDA\* 算法．IDA\* 就是采用了迭代加深算法的 A\* 算法．

## 过程

IDA\* 算法是迭代加深搜索的一种变形．迭代加深搜索在每次 DFS 中限制搜索深度，而 IDA\* 则限制单次 DFS 的路径成本．

在一次迭代中，算法从起点 $s$ 开始进行 DFS，记录到达当前结点 $x$ 的实际成本 $g(x)$，并利用它到终点的最小成本估计 $h(x)$ 进行剪枝．如果沿着当前路径到达终点的总成本估计

$$
f(x) = g(x) + h(x)
$$

超过阈值 $C$，则停止对该分支的搜索．

阈值 $C$ 在迭代间动态更新．初始阈值取为起点的总成本估计值 $h(s)$．在一次迭代中，每当因超过阈值而停止时，就记录所有尚未访问的后继结点的总成本估计的最小值．迭代结束后，将阈值更新为这一最小值，继续下一轮搜索．

## 性质

由于使用了和 A\* 算法一样的剪枝策略，所以对 A\* 算法性质的讨论对 IDA\* 算法也适用．

和 A\* 算法相比，IDA\* 算法有如下优点：

-   不需要判重，不需要排序，利于深度剪枝．
-   空间需求减少．每次迭代都是一个深度优先搜索，但是对搜索中的路径成本有限制，使用 DFS 可以减小空间消耗．

同时，它也有缺点：

-   重复搜索．即使前后两次搜索相差微小，每次放宽限制都要再次从头搜索．

## 实现

设 $h$ 是一个合适的估价函数，$s$ 为搜索起点．完整的算法流程大致如下所示：

$$
\begin{array}{l}
\textbf{Algorithm. }\textrm{IdaStar}():\\
\textbf{Output. }\text{The shortest path, }\textit{path}\text{, and its cost, }C\text{, if a path exists,}\\
\quad \text{and }\textrm{NOT}\_\textrm{FOUND}\text{, otherwise.}\\
\textbf{Method.}\\
\begin{array}{ll}
1  & C \gets h(s) \\
2  & path \gets [s] \\
3  & \textbf{while }\text{true}\\
4  & \quad t \gets \textrm{Search}(\textit{path},0,C)\\
5  & \quad \textbf{if } t=\text{FOUND}\textbf{ then return }(\textit{path},C) \\
6  & \quad \textbf{if } t=\infty\textbf{ then return }\textrm{NOT}\_\textrm{FOUND} \\
7  & \quad C \gets t
\end{array}\\
\\
\textbf{Sub-Algorithm. }\textrm{Search}(\textit{path},g,C):\\
\textbf{Input. }\text{The current path, }\textit{path}\text{, its cost, }g\text{, and search limit }C.\\
\textbf{Output. }\text{FOUND, if the target node has been reached; }\infty\text{, if all}\\
\quad \text{reachable nodes have been explored; otherwise, the minimum}\\
\quad \text{total cost, }t\text{, among nodes not yet explored.}\\
\textbf{Method.}\\
\begin{array}{ll}
1  & \textit{node} \gets \text{the last element in }\textit{path}\\
2  & f \gets g + h(\textit{node}) \\
3  & \textbf{if } f > C \textbf{ then return } f \\
4  & \textbf{if }\textit{node}\text{ is the target }\textbf{then return }\text{FOUND}\\
5  & \textit{min} \gets \infty \\
6  & \textbf{for }\text{each }\textit{child}\text{ of }\textit{node }\textbf{do}\\
7  & \quad \textbf{if }\textit{child}\text{ not in }\textit{path}\textbf{ then}\\
8  & \quad \quad \text{append }\textit{child}\text{ to }\textit{path}\\
9  & \quad \quad t \gets \text{Search}(\textit{path}, g + \text{Cost}(\textit{node},\textit{child}), C)\\
10 & \quad \quad \textbf{if }t = \text{FOUND}\textbf{ then return }\text{FOUND}\\
11 & \quad \quad \textbf{if }t < \textit{min}\textbf{ then }\textit{min}\gets t\\
12 & \quad \quad \text{remove the last element of }\textit{path}\\
13 & \textbf{return }\textit{min}
\end{array}
\end{array}
$$

## 例题

???+ example "[埃及分数](https://www.luogu.com.cn/problem/P1763)"
    在古埃及，人们使用互不相同的单位分数（即 $1/a$，$a\in\mathbf{N}_+$）的和表示一切有理数．例如，$\dfrac{2}{3}=\dfrac{1}{2}+\dfrac{1}{6}$，但不允许 $\dfrac{2}{3}=\dfrac{1}{3}+\dfrac{1}{3}$，因为在加数中不允许有相同的单位分数．
    
    对于一个分数 $\dfrac{a}{b}$，表示方法有很多种．规定：同一个分数的不同表示方法中，加数少的比加数多的好；如果加数个数相同，则最小的分数越大越好．例如，$\dfrac{19}{45}=\dfrac{1}{5}+\dfrac{1}{6}+\dfrac{1}{18}$ 是最佳方案．
    
    输入整数 $a,b$（$0<a<b<1000$），试编程计算最佳表达式．

??? note "解题思路"
    这道题目理论上可以用回溯法求解，但是解答树会非常「恐怖」——不仅深度没有明显的上界，而且加数的选择理论上也是无限的．换句话说，如果用宽度优先遍历，连一层都扩展不完，因为每一层都是无限大的．
    
    解决方案是采用迭代加深搜索：从小到大枚举深度上限 $C$，每次搜索只考虑深度不超过 $C$ 的结点．这样，只要解的深度有限，则一定可以在有限时间内枚举到．
    
    深度上限 $C$ 还可以用来剪枝．按照分母递增的顺序来进行扩展，如果扩展到 $i$ 层时，前 $i$ 个分数之和为 $\dfrac{c}{d}$，而第 $i$ 个分数为 $\dfrac{1}{e}$，则接下来至少还需要
    
    $$
    h = \left(\dfrac{a}{b}-\dfrac{c}{d}\right)/\left(\dfrac{1}{e+1}\right)
    $$
    
    个分数，总和才能达到 $\dfrac{a}{b}$．例如，当前搜索到 $\dfrac{19}{45}=\dfrac{1}{5}+\dfrac{1}{100}+\cdots$，则后面的分数每个最大为 $\dfrac{1}{101}$，至少需要 $\left({\dfrac{19}{45}-\dfrac{1}{5}}\right)/\left({\dfrac{1}{101}}\right)=23$ 项总和才能达到 $\dfrac{19}{45}$，因此前 $22$ 次迭代是根本不会考虑这棵子树的．这里的关键在于：可以估计至少还要多少步才能出解．
    
    注意，这里使用「至少」一词表示估计是「乐观的」．和 A\* 算法一样，好的估计函数都需要是「乐观的」，也就是说，它不能高估实际成本．将迭代加深搜索中的深度限制 $g\le C$ 替换为更严格的限制 $g + h \le C$，就得到了本页面所讨论的 IDA\* 算法．因为本文中的路径成本就是它的长度，所以，IDA\* 算法同样是对路径长度进行限制，只是加上了对于还需要多少步的估计．更一般的问题中，根据具体要最小化的成本不同，还可以设计出其他的估计函数．
    
    在实现中，对 IDA\* 算法进一步剪枝优化：
    
    1.  扩展结点时，下一个要考虑的分母至少是 $\left(\dfrac{a}{b}-\dfrac{c}{d}\right)^{-1}$，可以以此改进枚举 $e$ 的起点．
    2.  IDA\* 的路径成本限制可以变形为
    
        $$
        e \le \left(\dfrac{a}{b}-\dfrac{c}{d}\right)^{-1}(C-g) - 1.
        $$
    
        所以，不必枚举所有的后续分母再逐个判断，只需要枚举到这个上界即可．
    3.  在搜索到最后两个分数时，直接利用二次方程计算是否可行，而非继续搜索．具体地，要找到 $e<x<y\le E_\text{max}$ 使得
    
        $$
        \dfrac{1}{x} + \dfrac{1}{y} = \dfrac{p}{q} := \dfrac{a}{b}-\dfrac{c}{d},
        $$
    
        只需要求解二元二次方程组
    
        $$
        \begin{cases}
        x + y = kp,\\
        xy = kq
        \end{cases}
        $$
    
        即可，其中，$k\in\mathbf N_+$．由二次方程的知识可知，方程组在
    
        $$
        \Delta = k^2p^2-4kq > 0 \iff k > \dfrac{4q}{p^2}
        $$
    
        时，才有两个不同的实根
    
        $$
        x = \dfrac{kp - \sqrt{\Delta}}{2},~ y = \dfrac{kp + \sqrt{\Delta}}{2}.
        $$
    
        因此，可以直接枚举所有可行的 $k$，判断是否存在这样一组整数解．枚举 $k$ 时，上界通过 $y < E_\text{max}$ 判断．
    4.  每次得到一组答案时，都将分母的上界 $M_e$ 调整到当前答案中的最大分母减一．
    
    另外，实现中，直接记录了 $\dfrac{a}{b}-\dfrac{c}{d}$ 和 $C-g$ 的取值，前者的分子和分母分别存储在变量 `a` 和 `b` 中，后者则存储为变量 `d`．

??? note "示例代码"
    ```cpp
    --8<-- "docs/search/code/idastar/idastar_1.cpp"
    ```

## 习题

-   [UVa1343 旋转游戏](https://onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&category=24&page=show_problem&problem=4089)


## search/index.md

搜索，也就是对状态空间进行枚举，通过穷尽所有的可能来找到最优解，或者统计合法解的个数．

搜索有很多优化方式，如减小状态空间，更改搜索顺序，剪枝等．

搜索是一些高级算法的基础．在 OI 中，纯粹的搜索往往也是得到部分分的手段，但可以通过纯粹的搜索拿到满分的题目非常少．

## 习题

-   [「kuangbin 带你飞」专题一 简单搜索](https://vjudge.net/contest/65959)
-   [「kuangbin 带你飞」专题二 搜索进阶](https://vjudge.net/contest/65997)
-   [洛谷搜索题单](https://www.luogu.com.cn/training/112#problems)
-   [openjudge 搜索题单](http://noi.openjudge.cn/ch0205/)


## search/iterative.md

## 定义

迭代加深是一种 **每次限制搜索深度的** 深度优先搜索．

## 解释

迭代加深搜索的本质还是深度优先搜索，只不过在搜索的同时带上了一个深度 $d$，当 $d$ 达到设定的深度时就返回，一般用于找最优解．如果一次搜索没有找到合法的解，就让设定的深度加一，重新从根开始．

既然是为了找最优解，为什么不用 BFS 呢？我们知道 BFS 的基础是一个队列，队列的空间复杂度很大，当状态比较多或者单个状态比较大时，使用队列的 BFS 就显出了劣势．事实上，迭代加深就类似于用 DFS 方式实现的 BFS，它的空间复杂度相对较小．

当搜索树的分支比较多时，每增加一层的搜索复杂度会出现指数级爆炸式增长，这时前面重复进行的部分所带来的复杂度几乎可以忽略，这也就是为什么迭代加深是可以近似看成 BFS 的．

## 过程

首先设定一个较小的深度作为全局变量，进行 DFS．每进入一次 DFS，将当前深度加一，当发现 $d$ 大于设定的深度 $\textit{limit}$ 就返回．如果在搜索的途中发现了答案就可以回溯，同时在回溯的过程中可以记录路径．如果没有发现答案，就返回到函数入口，增加设定深度，继续搜索．

???+ note "实现（伪代码）"
    ```text
    IDDFS(u,d)
        if d>limit
            return
        else
            for each edge (u,v)
                IDDFS(v,d+1)
    return
    ```

## 注意事项

在大多数的题目中，广度优先搜索还是比较方便的，而且容易判重．当发现广度优先搜索在空间上不够优秀，而且要找最优解的问题时，就应该考虑迭代加深．


## search/opt.md

author: CBW2007, ChungZH, Marcythm, abc1763613206, Ir1d

## 前言

DFS（深度优先搜索）是一种常见的算法，大部分的题目都可以用 DFS 解决，但是大部分情况下，这都是骗分算法，很少会有爆搜为正解的题目．因为 DFS 的时间复杂度特别高．（没学过 DFS 的请自行补上这一课）

既然不能成为正解，那就多骗一点分吧．那么这一篇文章将介绍一些实用的优化算法（俗称「剪枝」）．

先来一段深搜模板，之后的模板将在此基础上进行修改．

```cpp
int ans = 最坏情况, now;  // now 为当前答案

void dfs(传入数值) {
  if (到达目的地) ans = 从当前解与已有解中选最优;
  for (遍历所有可能性)
    if (可行) {
      进行操作;
      dfs(缩小规模);
      撤回操作;
    }
}
```

其中的 ans 可以是解的记录，那么从当前解与已有解中选最优就变成了输出解．

## 剪枝方法

最常用的剪枝有三种，记忆化搜索、最优性剪枝、可行性剪枝．

### 记忆化搜索

因为在搜索中，相同的传入值往往会带来相同的解，那我们就可以用数组来记忆，详见 [记忆化搜索](../dp/memo.md)．

**模板：**

```cpp
int g[MAXN];  // 定义记忆化数组
int ans = 最坏情况, now;

void dfs f(传入数值) {
  if (g[规模] != 无效数值) return;  // 或记录解，视情况而定
  if (到达目的地) ans = 从当前解与已有解中选最优;  // 输出解，视情况而定
  for (遍历所有可能性)
    if (可行) {
      进行操作;
      dfs(缩小规模);
      撤回操作;
    }
}

int main() {
  // ...
  memset(g, 无效数值, sizeof(g));  // 初始化记忆化数组
  // ...
}
```

### 最优性剪枝

在搜索中导致运行慢的原因还有一种，就是在当前解已经比已有解差时仍然在搜索，那么我们只需要判断一下当前解是否已经差于已有解．

**模板：**

```cpp
int ans = 最坏情况, now;

void dfs(传入数值) {
  if (now比ans的答案还要差) return;
  if (到达目的地) ans = 从当前解与已有解中选最优;
  for (遍历所有可能性)
    if (可行) {
      进行操作;
      dfs(缩小规模);
      撤回操作;
    }
}
```

### 可行性剪枝

在搜索过程中当前解已经不可用了还继续搜索下去也是运行慢的原因．

**模板：**

```cpp
int ans = 最坏情况, now;

void dfs(传入数值) {
  if (当前解已不可用) return;
  if (到达目的地) ans = 从当前解与已有解中选最优;
  for (遍历所有可能性)
    if (可行) {
      进行操作;
      dfs(缩小规模);
      撤回操作;
    }
}
```

## 剪枝思路

剪枝思路有很多种，大多需要对于具体问题来分析，在此简要介绍几种常见的剪枝思路．

-   极端法：考虑极端情况，如果最极端（最理想）的情况都无法满足，那么肯定实际情况搜出来的结果不会更优了．

-   调整法：通过对子树的比较剪掉重复子树和明显不是最有「前途」的子树．

-   数学方法：比如在图论中借助连通分量，数论中借助模方程的分析，借助不等式的放缩来估计下界等等．

## 例题

???+ note "工作分配问题"
    有 $n$（$1 \leq n \leq  15$）份工作要分配给 $n$ 个人来完成，每个人完成一份．第 $i$ 个人完成第 $k$ 份工作所用的时间为一个正整数 $t_{i,k}$（$1 \leq t_{i,k} \leq 10^4$），其中 $1 \leq i, k \leq n$．试确定一个分配方案，使得完成这 $n$ 份工作的时间总和最小．

由于每个人都必须分配到工作，在这里可以建一个二维数组 `time[i][j]`，用以表示 $i$ 个人完成 $j$ 号工作所花费的时间．给定一个循环，从第 1 个人开始循环分配工作，直到所有人都分配到．为第 $i$ 个人分配工作时，再循环检查每个工作是否已被分配，没有则分配给 $i$ 个人，否则检查下一个工作．可以用一个一维数组 `is_working[j]` 来表示第 $j$ 号工作是否已被分配，未分配则 `is_working[j]=0`，否则 `is_working[j]=1`．利用回溯思想，在工人循环结束后回到上一工人，取消此次分配的工作，而去分配下一工作直到可以分配为止．这样，一直回溯到第 1 个工人后，就能得到所有的可行解．

检查工作分配，其实就是判断取得可行解时的二维数组的第一维下标各不相同并且第二维下标各不相同．而我们是要得到完成这 $n$ 份工作的最小时间总和，即可行解中时间总和最小的一个，故需要再定义一个全局变量 `cost_time_total_min` 表示目前找到的解中最小的时间总和，初始 `cost_time_total_min` 为 `time[i][i]` 之和，即对角线工作时间相加之和．在所有人分配完工作时，比较 `count` 与 `cost_time_total_min` 的大小，如果 `count` 小于 `cost_time_total_min`，说明找到了一个最优解，此时就把 `count` 赋给 `cost_time_total_min`．

但考虑到算法的效率，这里还有一个剪枝优化的工作可以做．就是在每次计算局部费用变量 `count` 的值时，如果判断 `count` 已经大于 `cost_time_total_min`，就没必要再往下分配了，因为这时得到的解必然不是最优解．

??? note "参考代码"
    ```cpp
    --8<-- "docs/search/code/opt/opt_1.cpp"
    ```
