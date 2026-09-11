

## ds/aa-tree.md

AA 树是一种用于高效存储和检索有序数据的平衡树形结构，Arne Andersson 教授于 1993 年在他的论文 "Balanced search trees made simple" 中介绍，设计的目的是减少红黑树考虑的不同情况．AA 树可以在 $O(\log N)$ 的时间内做查找，插入和删除．下面是一个 AA 树的例子．

![aa-tree-1](images/aa-tree-1.jpg)

AA 树是红黑树的一种变体，与红黑树不同，AA 树上的红色节点只能作为右子节点．这导致 AA 树模拟了 2-3 树而不是 2-3-4 树，从而极大地简化了维护操作．红黑树的维护算法需要考虑七种不同的情况来正确平衡树．

![red-black tree](images/aa-tree-2.svg)

因为红色节点只能作为右子节点，AA 树只需要考虑两种情况．

![aa-tree](images/aa-tree-3.svg)

## 定义

AA 树遵循与红黑树相同的规则，但添加了一条新规则，**即红色节点不能作为左孩子出现**．

1.  每个节点都可以是红色或黑色．
2.  根节点总是黑色．
3.  叶节点（NULL）总是黑色．
4.  红色节点的两个子节点必须都是黑色，即没有两个相邻的红色节点．
5.  从根节点到 NULL 节点的每条路径都有相同数量的黑色节点．
6.  红色节点只能作为右子节点．

## 平衡维护

AA 树的每个节点维护一个 **level** 字段，类似红黑树的每个节点维护一个 color 字段 ("RED" or "BLACK")．level 的规定满足以下 5 个条件：

1、每个叶节点的 level 是 1．

2、每个左孩子的 level 是其父节点的 level 减 1．

3、每个右孩子的 level 等于其父节点的 level 或等于其父节点的 level 减 1．

4、每个右孙子的 level 严格小于其祖父节点的 level．

5、每个 level 大于 1 的节点有两个孩子．

![aa-tree-4](images/aa-tree-4.jpg)

### 水平链接（Horizontal Link）

子节点的 level 等于父节点的 level 的链接被称为 **水平链接**，类似于红黑树中的红链接．允许单独的右水平链接，但不允许连续的右水平链接；不允许左水平链接．这些限制比红黑树的限制更加严格，因此 AA 树的平衡过程比红黑树的平衡过程在程序上要简单得多．

![aa-tree-5](images/aa-tree-5.jpg)

插入和删除操作可能会暂时导致 AA 树失去平衡（即违反 AA 树的不变性）．恢复平衡只需要两种不同的操作："**skew**"（斜化）和"**split**"（分裂）．"Skew"是将一个包含左水平链接的子树进行右旋转，以替换为一个包含右水平链接的子树．"Split"是进行左旋转并增加 level，以替换一个包含两个或更多连续的右水平链接的子树，使其变为一个包含两个较少连续的右水平链接的子树．保持平衡的插入和删除的实现通过依赖"skew"和"split"操作来仅在需要时修改树，而不是由调用者决定是否进行"skew"或"split"，从而变得更加简化．

### split（左旋）

出现连续向右的水平方向链（连续三个向右的孩子属于同一 level，节点 R 和节点 X 都是红色节点）．

此时向左旋转节点*T*，把小于等于此 level 的节点看做一个子树．

1.  子树的根的右孩子变为新的子树根；
2.  原来的子树根变为新子树根的左孩子；
3.  新的子树根 level+1．

![aa-tree-split](images/aa-tree-split.svg)

???+ note "伪代码实现"
    $$
    \begin{array}{ll}
    1 & \textbf{function } \text{split}(\text{root}) \\
    2 & \qquad \textbf{if } \text{root}\rightarrow\text{right}\rightarrow\text{right}\rightarrow\text{level} == \text{root}\rightarrow\text{level} \\
    3 & \qquad\qquad \text{rotate\_left}(\text{root}) \\
    4 & \textbf{end function}
    \end{array}
    $$

### skew（右旋）

出现向左的水平方向链（连续两个向左的孩子属于同一 level）

向右旋转节点*T*，把小于等于此 level 的节点看做一个子树．

1.  子树的根的左孩子变为新的子树根；
2.  原来的子树根变为新子树根的右孩子．

![aa-tree-skew](images/aa-tree-skew.svg)

???+ note "伪代码实现"
    $$
    \begin{array}{ll}
    1 & \textbf{function } \text{skew}(\text{root}) \\
    2 & \qquad \textbf{if } \text{root}\rightarrow\text{left}\rightarrow\text{level} == \text{root}\rightarrow\text{level} \\
    3 & \qquad\qquad \text{rotate\_right}(\text{root}) \\
    4 & \textbf{end function}
    \end{array}
    $$

## AA 树的操作

AA 树本身是一棵二叉搜索树，所以搜索操作与其他二叉搜索树相同．插入和删除操作与*AVL*树相同，首先在树中将 key 插入或删除，然后沿着搜索路径回退到根，并在此过程中重构树．

### 插入

???+ note "伪代码实现"
    $$
    \begin{array}{ll}
    1 & \textbf{function } \text{insert}(\text{root}, \text{add}) \\
    2 & \qquad \textbf{if } \text{root} == \text{NULL} \\
    3 & \qquad\qquad \text{root} \gets \text{add} \\
    4 & \qquad \textbf{else if } \text{add}\rightarrow\text{key} < \text{root}\rightarrow\text{key} \qquad //如果允许重复<= \\ 
    5 & \qquad\qquad \text{insert}(\text{root}\rightarrow\text{left}, \text{add}) \\
    6 & \qquad \textbf{else if } \text{add}\rightarrow\text{key} > \text{root}\rightarrow\text{key} \\
    7 & \qquad\qquad \text{insert}(\text{root}\rightarrow\text{right}, \text{add}) \\
    8 & \qquad \textbf{end if} \\
    9 & \qquad \text{//如果不允许重复，在每一level上进行skew和split} \\
    10 & \qquad \text{skew}(\text{root}); \\
    11 & \qquad \text{split}(\text{root}); \\
    12 & \textbf{end function}
    \end{array}
    $$

### 删除

删除过程与其他二叉平衡树类似，首先将内部节点的删除转换为叶子节点的删除．具体方法是将内部节点与它最接近的前驱或后继节点替换．由于 AA 树的所有 level 大于 1 的节点都有两个子节点，前驱或后继节点将位于 level 1，删除 level 1 的节点较为简单．

???+ note "伪代码实现"
    $$
    \begin{array}{ll}
    1 &  \text{//To rebalance the tree} \\
    2 &  \textbf{if} \ \text{root->left->level} < \text{root->level} -1 \ \textbf{or} \ \text{root->right->level} < \text{root->level} -1 \\
    3 &  \{ \\
    4 & \qquad \textbf{if} \ \text{root->right->level} > \text{--root->level} \\
    5 & \qquad \{ \\
    6 & \qquad\qquad \text{root->right->level} \gets \text{root->level} \\
    7 & \qquad \} \\
    8 & \qquad \text{skew}(\text{root}) \\
    9 & \qquad \text{skew}(\text{root->right}) \\
    10 & \qquad \text{skew}(\text{root->right->right}) \\
    11 & \qquad \text{split}(\text{root}) \\
    12 & \qquad \text{split}(\text{root->right}) \\
    13 &  \} \\
    \end{array}
    $$

## 性能

AA 树的性能与红黑树的性能相当．尽管 AA 树进行的旋转操作比红黑树多，但 AA 树的算法更简单，最终导致相近的性能．红黑树的性能在各种情况下更加一致，而 AA 树往往更扁平，这使 AA 树有稍快的搜索速度．

## 参考资料

1.  [AA tree - Wikipedia](https://en.wikipedia.org/wiki/AA_tree)
2.  [Introduction to AA trees](https://iq.opengenus.org/aa-trees/)
3.  [AA tree - Visualization](https://kubokovac.eu/gnarley-trees/AAtree.html)
4.  [CMSC 420 Lecture 6: 2-3, Red-black, and AA trees](https://www.cs.umd.edu/class/fall2019/cmsc420-0201/Lects/lect06-aa.pdf)


## ds/avl.md

AVL 树，是一种平衡的二叉搜索树．由于各种算法教材上对 AVL 的介绍十分冗长，造成了很多人对 AVL 树复杂、不实用的印象．但实际上，AVL 树的原理简单，实现也并不复杂．

## 性质

1.  空二叉树是一个 AVL 树
2.  如果 T 是一棵 AVL 树，那么其左右子树也是 AVL 树，并且 $|h(ls) - h(rs)| \leq 1$，h 是其左右子树的高度
3.  树高为 $O(\log n)$

平衡因子：右子树高度 - 左子树高度

???+ note "树高的证明"
    设 $f_n$ 为高度为 $n$ 的 AVL 树所包含的最少节点数，则有
    
    $$
    f_n=
    \begin{cases}
    1&(n=1)\\
    2&(n=2)\\
    f_{n-1}+f_{n-2}+1& (n>2)
    \end{cases}
    $$
    
    根据常系数非齐次线性差分方程的解法，$\{f_n+1\}$ 是一个斐波那契数列．这里 $f_n$ 的通项为：
    
    $$
    f_n=\frac{5+2\sqrt{5}}{5}\left(\frac{1+\sqrt{5}}{2}\right)^n+\frac{5-2\sqrt{5}}{5}\left(\frac{1-\sqrt{5}}{2}\right)^n-1
    $$
    
    斐波那契数列以指数的速度增长，对于树高 $n$ 有：
    
    $$
    n<\log_{\frac{1+\sqrt{5}}{2}} (f_n+1)<\frac{3}{2}\log_2 (f_n+1)
    $$
    
    因此 AVL 树的高度为 $O(\log f_n)$，这里的 $f_n$ 为结点数．

## 过程

### 插入结点

与 BST（二叉搜索树）中类似，先进行一次失败的查找来确定插入的位置，插入节点后根据平衡因子来决定是否需要调整．

### 删除结点

删除和 BST 类似，将结点与后继交换后再删除．

删除会导致树高以及平衡因子变化，这时需要沿着被删除结点到根的路径来调整这种变化．

### 平衡的维护

插入或删除节点后，可能会造成 AVL 树的性质 2 被破坏．因此，需要沿着从被插入/删除的节点到根的路径对树进行维护．如果对于某一个节点，性质 2 不再满足，由于我们只插入/删除了一个节点，对树高的影响不超过 1，因此该节点的平衡因子的绝对值至多为 2．由于对称性，我们在此只讨论左子树的高度比右子树大 2 的情况，即下图中 $h(B)-h(E)=2$．此时，还需要根据 $h(A)$ 和 $h(C)$ 的大小关系分两种情况讨论．需要注意的是，由于我们是自底向上维护平衡的，因此对节点 D 的所有后代来说，性质 2 仍然是被满足的．

![](./images/avl1.svg)

#### 情况一：A 点树高不小于 C 点树高

设 $h(E)=x$，则有

$$
\begin{cases}
    h(B)=x+2\\
    h(A)=x+1\\
    x\leq h(C)\leq x+1
\end{cases}
$$

其中 $h(C)\geq x$ 是由于节点 B 满足性质 2，因此 $h(C)$ 和 $h(A)$ 的差不会超过 1．此时我们对节点 D 进行一次右旋操作（旋转操作与其它类型的平衡二叉搜索树相同），如下图所示．

![](./images/avl2.svg)

显然节点 A、C、E 的高度不发生变化，并且有

$$
\begin{cases}
    0\leq h(C)-h(E)\leq 1\\
    x+1\leq h'(D)=\max(h(C),h(E))+1=h(C)+1\leq x+2\\
    0\leq h'(D)-h(A)\leq 1
\end{cases}
$$

因此旋转后的节点 B 和 D 也满足性质 2．

#### 情况二：A 点树高小于 C 点树高

设 $h(E)=x$，则与刚才同理，有

$$
\begin{cases}
    h(B)=x+2\\
    h(C)=x+1\\
    h(A)=x
\end{cases}
$$

此时我们先对节点 B 进行一次左旋操作，再对节点 D 进行一次右旋操作，如下图所示．

![](./images/avl3.svg)

显然节点 A、E 的高度不发生变化，并且 B 的新右儿子和 D 的新左儿子分别为 C 原来的左右儿子，则有

$$
\begin{cases}
    x-1\leq h'(rs_B),h'(ls_D)\leq x\\
    0\leq h(A)-h'(rs_B)\leq 1\\
    0\leq h(E)-h'(ls_D)\leq 1\\
    h'(B)=\max(h(A),h'(rs_B))+1=x+1\\
    h'(D)=\max(h(E),h'(ls_D))+1=x+1\\
    h'(B)-h'(D)=0
\end{cases}
$$

因此旋转后的节点 B、C、D 也满足性质 2．

???+ note "维护平衡操作：伪代码"
    $$
    \begin{array}{ll}
    1 &  \textbf{function } \mathrm{MaintainBalance}(p) \\
    2 &  \qquad l \gets ls_p, r \gets rs_p \\
    3 &  \qquad \textbf{if } h(l)-h(r)=2 \\
    4 &  \qquad\qquad \textbf{if } h(ls_l) \ge h(rs_l) \\
    5 &  \qquad\qquad\qquad \mathrm{RightRotate}(p) \\
    6 &  \qquad\qquad \textbf{else} \\
    7 &  \qquad\qquad\qquad \mathrm{LeftRotate}(l) \\
    8 &  \qquad\qquad\qquad \mathrm{RightRotate}(p) \\
    9 &  \qquad \textbf{else if } h(l)-h(r)=-2 \\
    10 &  \qquad\qquad \textbf{if } h(ls_r) \le h(rs_r) \\
    11 &  \qquad\qquad\qquad \mathrm{LeftRotate}(p) \\
    12 &  \qquad\qquad \textbf{else} \\
    13 &  \qquad\qquad\qquad \mathrm{RightRotate}(r) \\
    14 &  \qquad\qquad\qquad \mathrm{LeftRotate}(p) \\
    \end{array}
    $$

与其他平衡二叉搜索树相同，AVL 树中节点的高度、子树大小等信息需要在旋转时进行维护．

## 其他操作

AVL 树的其他操作（Predecessor、Successor、Select、Rank 等）与普通的二叉搜索树相同．

## 参考代码

下面的代码是用 AVL 树实现的 `Map`，即有序不可重映射：

??? note "参考代码"
    ```cpp
    --8<-- "docs/ds/code/avl-tree/AvlTreeMap.hpp"
    ```

## 其他资料

在 [AVL Tree Visualization](https://www.cs.usfca.edu/~galles/visualization/AVLtree.html) 可以观察 AVL 树维护平衡的过程．

[维基百科 -- AVL 树](https://en.wikipedia.org/wiki/AVL_tree)


## ds/balanced-in-seg.md

author: Dev-jqe, HeRaNO, huaruoji

## 常见用途

在算法竞赛中，我们有时需要维护多维度信息．在这种时候，我们经常需要树套树来记录信息．当需要维护前驱，后继，第 $k$ 大，某个数的排名，或者插入删除的时候，我们通常需要使用平衡树来满足我们的需求，即线段树套平衡树．

## 过程

我们以 **二逼平衡树** 为例，来解释实现原理．

关于树套树的构建，我们对于外层线段树正常建树，对于线段树上的某一个节点，建立一棵平衡树，包含该节点所覆盖的序列．具体操作时我们可以将序列元素一个个插入，每经过一个线段树节点，就将该元素加入到该节点的平衡树中．

操作一，求某区间中某值的排名：我们对于外层线段树正常操作，对于在某区间中的节点的平衡树，我们返回平衡树中比该值小的元素个数，合并区间时，我们将小的元素个数求和即可．最后将返回值 $+1$，即为某值在某区间中的排名．

操作二，求某区间中排名为 $k$ 的值：我们可以采用二分策略．因为一个元素可能存在多个，其排名为一区间，且有些元素原序列不存在．所以我们采取和操作一类似的思路，我们用小于该值的元素个数作为参考进行二分，即可得解．

操作三，将某个数替换为另外一个数：我们只要在所有包含某数的平衡树中删除某数，然后再插入另外一个数即可．外层依旧正常线段树操作．

操作四，求某区间中某值的前驱：我们对于外层线段树正常操作，对于在某区间中的节点的平衡树，我们返回某值在该平衡树中的前驱，线段树的区间结果合并时，我们取最大值即可．

## 性质

### 空间复杂度

我们每个元素加入 $O(\log n)$ 个平衡树，所以空间复杂度为 $O((n + q)\log{n})$．

### 时间复杂度

-   对于 1，3，4 操作，我们考虑我们在外层线段树上进行 $O(\log{n})$ 次操作，每次操作会在一个内层平衡树树上进行 $O(\log{n})$ 次操作，所以时间复杂度为 $O(\log^2{n})$．
-   对于 2 操作，多一个二分过程，为 $O(\log^3{n})$．

## 经典例题

[二逼平衡树](https://loj.ac/problem/106) 外层线段树，内层平衡树．

## 实现

平衡树部分代码请参考 [Splay](./splay.md) 等其他条目．

操作一：

```cpp
int vec_rank(int k, int l, int r, int x, int y, int t) {
  if (x <= l && r <= y) {
    return spy[k].chk_rank(t);
  }
  int mid = l + r >> 1;
  int res = 0;
  if (x <= mid) res += vec_rank(k << 1, l, mid, x, y, t);
  if (y > mid) res += vec_rank(k << 1 | 1, mid + 1, r, x, y, t);
  if (x <= mid && y > mid) res--;
  return res;
}
```

操作二：

```cpp
int el = 0, er = 100000001, emid;
while (el != er) {
  emid = el + er >> 1;
  if (vec_rank(1, 1, n, tl, tr, emid) - 1 < tk)
    el = emid + 1;
  else
    er = emid;
}
printf("%d\n", el - 1);
```

操作三：

```cpp
void vec_chg(int k, int l, int r, int loc, int x) {
  int t = spy[k].find(dat[loc]);
  spy[k].dele(t);
  spy[k].insert(x);
  if (l == r) return;
  int mid = l + r >> 1;
  if (loc <= mid) vec_chg(k << 1, l, mid, loc, x);
  if (loc > mid) vec_chg(k << 1 | 1, mid + 1, r, loc, x);
}
```

操作四：

```cpp
int vec_front(int k, int l, int r, int x, int y, int t) {
  if (x <= l && r <= y) return spy[k].chk_front(t);
  int mid = l + r >> 1;
  int res = 0;
  if (x <= mid) res = max(res, vec_front(k << 1, l, mid, x, y, t));
  if (y > mid) res = max(res, vec_front(k << 1 | 1, mid + 1, r, x, y, t));
  return res;
}
```

## 相关算法

面对多维度信息的题目时，如果题目没有要求强制在线，我们还可以考虑 [CDQ 分治](../misc/cdq-divide.md)，或者 [整体二分](../misc/parallel-binsearch.md) 等分治算法，来避免使用高级数据结构，减少代码实现难度．


## ds/binary-heap.md

author: HeRaNO, Xeonacid, AzurIce

## 结构

从二叉堆的结构说起，它是一棵二叉树，并且是完全二叉树，每个结点中存有一个元素（或者说，有个权值）．

堆性质：父亲的权值不小于儿子的权值（大根堆）．同样的，我们可以定义小根堆．本文以大根堆为例．

由堆性质，树根存的是最大值（getmax 操作就解决了）．

## 过程

### 插入操作

插入操作是指向二叉堆中插入一个元素，要保证插入后也是一棵完全二叉树．

最简单的方法就是，最下一层最右边的叶子之后插入．

如果最下一层已满，就新增一层．

插入之后可能会不满足堆性质？

**向上调整**：如果这个结点的权值大于它父亲的权值，就交换，重复此过程直到不满足或者到根．

可以证明，插入之后向上调整后，没有其他结点会不满足堆性质．

向上调整的时间复杂度是 $O(\log n)$ 的．

![二叉堆的插入操作](./images/binary_heap_insert.svg)

### 删除操作

删除操作指删除堆中最大的元素，即删除根结点．

但是如果直接删除，则变成了两个堆，难以处理．

所以不妨考虑插入操作的逆过程，设法将根结点移到最后一个结点，然后直接删掉．

然而实际上不好做，我们通常采用的方法是，把根结点和最后一个结点直接交换．

于是直接删掉（在最后一个结点处的）根结点，但是新的根结点可能不满足堆性质……

**向下调整**：在该结点的儿子中，找一个最大的，与该结点交换，重复此过程直到底层．

可以证明，删除并向下调整后，没有其他结点不满足堆性质．

时间复杂度 $O(\log n)$．

### 增加某个点的权值

很显然，直接修改后，向上调整一次即可，时间复杂度为 $O(\log n)$．

## 实现

我们发现，上面介绍的几种操作主要依赖于两个核心：向上调整和向下调整．

考虑使用一个序列 $h$ 来表示堆．$h_i$ 的两个儿子分别是 $h_{2i}$ 和 $h_{2i+1}$，$1$ 是根结点：

![h 的堆结构](./images/binary-heap-array.svg)

参考代码：

```cpp
void up(int x) {
  while (x > 1 && h[x] > h[x / 2]) {
    std::swap(h[x], h[x / 2]);
    x /= 2;
  }
}

void down(int x) {
  while (x * 2 <= n) {
    t = x * 2;
    if (t + 1 <= n && h[t + 1] > h[t]) t++;
    if (h[t] <= h[x]) break;
    std::swap(h[x], h[t]);
    x = t;
  }
}
```

### 建堆

考虑这么一个问题，从一个空的堆开始，插入 $n$ 个元素，不在乎顺序．

直接一个一个插入需要 $O(n \log n)$ 的时间，有没有更好的方法？

#### 方法一：向上调整

从根开始，按 BFS 序进行．

```cpp
void build_heap_1() {
  for (i = 1; i <= n; i++) up(i);
}
```

这个做法仍然相当于一个一个插入，只是把元素提前放在了数组里，可以改善常数．故而最坏情况下，算法时间复杂度满足的递推式为 $T(n) = T(n - 1) + \Theta(\log n)$，累加得 $T(n) = \Theta(n \log n)$．

#### 方法二：向下调整

这时换一种思路，从叶子开始，逐个向下调整．

```cpp
void build_heap_2() {
  for (i = n; i >= 1; i--) down(i);
}
```

换一种理解方法，每次「合并」两个已经调整好的堆，这说明了正确性．

注意到叶节点无需调整，因此可从序列约 $n/2$ 的位置开始调整，可以改善常数．根据每次合并两个堆这一理解，可以写出算法时间复杂度的递推式 $T(n) = 2T(\dfrac{n}{2}) + O(\log n)$，由主定理可得 $T(n) = \Theta(n)$．

之所以能 $\Theta(n)$ 建堆，是因为堆性质很弱，二叉堆并不是唯一的．

要是像排序那样的强条件就难说了．

## 应用

### 对顶堆

??? note "[SPOJ RMID2 - Running Median Again](https://www.spoj.com/problems/RMID2/)"
    维护一个序列，支持两种操作：
    
    1.  向序列中插入一个元素
    2.  输出并删除当前序列的中位数（若序列长度为偶数，则输出较小的中位数）

这个问题可以被进一步抽象成：动态维护一个序列上第 $k$ 大的数，$k$ 值可能会发生变化．

对于此类问题，我们可以使用 **对顶堆** 这一技巧予以解决（可以避免写权值线段树或 BST 带来的繁琐）．

对顶堆由一个大根堆与一个小根堆组成，小根堆维护大值即前 $k$ 大的值（包含第 k 个），大根堆维护小值即比第 $k$ 大数小的其他数．

这两个堆构成的数据结构支持以下操作：

-   维护：当小根堆的大小小于 $k$ 时，不断将大根堆堆顶元素取出并插入小根堆，直到小根堆的大小等于 $k$；当小根堆的大小大于 $k$ 时，不断将小根堆堆顶元素取出并插入大根堆，直到小根堆的大小等于 $k$；
-   插入元素：若插入的元素大于等于小根堆堆顶元素，则将其插入小根堆，否则将其插入大根堆，然后维护对顶堆；
-   查询第 $k$ 大元素：小根堆堆顶元素即为所求；
-   删除第 $k$ 大元素：删除小根堆堆顶元素，然后维护对顶堆；
-   $k$ 值 $+1/-1$：根据新的 $k$ 值直接维护对顶堆．

显然，查询第 $k$ 大元素的时间复杂度是 $O(1)$ 的．由于插入、删除或调整 $k$ 值后，小根堆的大小与期望的 $k$ 值最多相差 $1$，故每次维护最多只需对大根堆与小根堆中的元素进行一次调整，因此，这些操作的时间复杂度都是 $O(\log n)$ 的．

??? note "参考代码"
    ```cpp
    --8<-- "docs/ds/code/binary-heap/binary-heap_1.cpp"
    ```

### 习题

-   [SPOJ RMID - Running Median](https://www.spoj.com/problems/RMID)
-   [洛谷 P1801 黑匣子](https://www.luogu.com.cn/problem/P1801)


## ds/bit-in-block-array.md

author: Backl1ght, Tiphereth-A, Enter-tainer, Ir1d, ksyx, leoleoasd, Xeonacid, aaron20100919

## 简介

分块套树状数组在特定条件下可以用来做一些树套树可以做的事情，但是相比起树套树，分块套树状数组代码编写更加简短，更加容易实现．

## 简单的例子

一个简单的例子就是二维平面中矩阵区域内点数的查询．

???+ note "矩形区域查询"
    给出 $n$ 个二维平面中的点 $(x_i, y_i)$，其中 $1 \le i \le n, 1 \le x_i, y_i \le n, 1 \le n \le 10^5$, 要求实现以下中操作：
    
    1.  给出 $a, b, c, d$，询问以 $(a, b)$ 为左上角，$c, d$ 为右下角的矩形区域内点的个数．
    2.  给出 $x, y$，将横坐标为 $x$ 的点的纵坐标改为 $y$．
    
    题目 **强制在线**，保证 $x_i \ne x_j(1 \le i, j \le n, i \ne j)$．

对于操作 1，可以通过矩形容斥将其转化为 4 个二维偏序的查询去解决，然后因为强制在线，CDQ 分治之类的离线算法就解决不了，于是想到了树套树，比如树状数组套 Treap．这确实可以解决这个问题，但是代码太长了，也不是特别好实现．

注意到，题目还额外保证了 $x_i \ne x_j(1 \le i, j \le n, i \ne j)$，这个时候就可以用分块套树状数组解决．

### 初始化

首先，一个 $x$ 只对应一个 $y$，所以可以用一个数组记录这个映射关系，比如令 $Y_i$ 表示横坐标为 $i$ 的点的纵坐标．

然后，以 $\sqrt n$ 为块大小对横坐标进行分块．为每个块建一棵权值树状数组．记 $T_i$ 为第 $i$ 个块对应的树状数组，$T_{i, j}$ 表示块 $i$ 里纵坐标在 $(j - lowbit(j), j]$ 内的点的个数．

### 查询

对于操作 1，将其转化为 4 个二维偏序的查询．现在只需要解决给出 $a, b$，询问有多少个点满足 $1 \le x_i \le a, 1\le y_i \le b$．

现在要查询横坐标的范围为 $[1, a]$．因为查询范围最右边可能有一段不是完整的块，所以暴力扫一遍这个段，看是否满足 $Y_i \le b$，统计出这个段满足要求的点的个数．

现在就只需要处理完整的块．暴力扫一遍前面的块，查询每个块对应的树状数组中值小于 $b$ 的个数，累加到答案上．

这就完事了？不，注意到处理完整的块的时候，其实相当于查询 $T$ 的前缀和，如果修改时也使用树状数组的技巧处理 $T$，那么查询时复杂度会更低．

### 修改

普通的做法就先找到点 $x$ 所在的块，然后一减一加两个权值树状数组单点修改，再将 $Y_x$ 置为 $y$．

如果用了上面说的优化，那就是对 $T$ 也走一个树状数组修改的流程，每次修改也是一减一加两个权值树状数组单点修改．

对上述步骤进行一定的改变，比如将一减一加改成只减，就是删点；改成只加，就是加点．但是必须要注意一个 $x$ 只能对应一个 $y$．

### 空间复杂度

分块分了 $\sqrt n$ 个块，每个块一个树状数组 $O(n)$ 的空间，所以空间复杂度为 $O(n \sqrt n)$．

### 时间复杂度

查询的话，遍历非完整块的段 $O(\sqrt n)$．然后，对 $T$ 走树状数组查询，每个经历到的 $T_i$ 也走树状数组查询，这一步是 $O(\log (\sqrt n) \log n)$ 的复杂度．所以查询的时间复杂度为 $O (\sqrt n + \log (\sqrt n) \log n)$．

修改和查询一样，复杂度为 $O (\sqrt n + \log (\sqrt n) \log n)$．

## 例题 1

???+ note "[Intersection of Permutations](https://codeforces.com/problemset/problem/1093/E)"
    给出两个排列 $a$ 和 $b$，要求实现以下两种操作：
    
    1.  给出 $l_a, r_a, l_b, r_b$，要求查询既出现在 $a[l_a ... r_a]$ 又出现在 $b[l_b ... r_b]$ 中的元素的个数．
    2.  给出 $x, y$，$swap(b_x, b_y)$．
    
    序列长度 $n$ 满足 $2 \le n \le 2 \cdot 10^5$，操作个数 $q$ 满足 $1 \le q \le 2 \cdot 10^5$．

对于每个值 $i$，记 $x_i$ 是它在排列 $b$ 中的下标，$y_i$ 是它在排列 $a$ 中的下标．这样，操作一就变成了一个矩形区域内点的个数的询问，操作 2 可以看成两个修改操作．而且因为是排列，所以满足一个 $x$ 对应一个 $y$，所以这题可以用分块套树状数组来写．

??? note "参考代码（分块套树状数组 - 1s）"
    ```cpp
    #include <cmath>
    #include <cstdio>
    using namespace std;
    constexpr int N = 2e5 + 5;
    constexpr int M = 447 + 5;  // sqrt(N) + 5
    
    int n, m, pa[N], pb[N];
    
    int nn, block_size, block_cnt, block_id[N], L[N], R[N], T[M][N];
    
    void build(int n) {
      nn = n;
      block_size = sqrt(nn);
      block_cnt = nn / block_size;
      for (int i = 1; i <= block_cnt; ++i) {
        L[i] = R[i - 1] + 1;
        R[i] = i * block_size;
      }
      if (R[block_cnt] < nn) {
        ++block_cnt;
        L[block_cnt] = R[block_cnt - 1] + 1;
        R[block_cnt] = nn;
      }
      for (int j = 1; j <= block_cnt; ++j)
        for (int i = L[j]; i <= R[j]; ++i) block_id[i] = j;
    }
    
    int lb(int x) { return x & -x; }
    
    void add(int p, int v, int d) {
      for (int i = block_id[p]; i <= block_cnt; i += lb(i))
        for (int j = v; j <= nn; j += lb(j)) T[i][j] += d;
    }
    
    int getsum(int p, int v) {
      if (!p) return 0;
      int res = 0;
      int id = block_id[p];
      for (int i = L[id]; i <= p; ++i)
        if (pb[i] <= v) ++res;
      for (int i = id - 1; i; i -= lb(i))
        for (int j = v; j; j -= lb(j)) res += T[i][j];
      return res;
    }
    
    void update(int x, int y) {
      add(x, pb[x], -1);
      add(y, pb[y], -1);
      swap(pb[x], pb[y]);
      add(x, pb[x], 1);
      add(y, pb[y], 1);
    }
    
    int query(int la, int ra, int lb, int rb) {
      int res = getsum(rb, ra) - getsum(rb, la - 1) - getsum(lb - 1, ra) +
                getsum(lb - 1, la - 1);
      return res;
    }
    
    int main() {
      scanf("%d %d", &n, &m);
      int v;
      for (int i = 1; i <= n; ++i) scanf("%d", &v), pa[v] = i;
      for (int i = 1; i <= n; ++i) scanf("%d", &v), pb[i] = pa[v];
    
      build(n);
      for (int i = 1; i <= n; ++i) add(i, pb[i], 1);
    
      int op, la, lb, ra, rb, x, y;
      for (int i = 1; i <= m; ++i) {
        scanf("%d", &op);
        if (op == 1) {
          scanf("%d %d %d %d", &la, &ra, &lb, &rb);
          printf("%d\n", query(la, ra, lb, rb));
        } else if (op == 2) {
          scanf("%d %d", &x, &y);
          update(x, y);
        }
      }
      return 0;
    }
    ```

??? note "参考代码（树状数组套 Treap—TLE）"
    ```cpp
    #include <cstdio>
    #include <random>
    using namespace std;
    constexpr int N = 2e5 + 5;
    mt19937 rng(random_device{}());
    
    int n, m, pa[N], pb[N];
    
    // Treap
    struct Treap {
      struct node {
        node *l, *r;
        int sz, rnd, v;
    
        node(int _v) : l(NULL), r(NULL), sz(1), rnd(rng()), v(_v) {}
      };
    
      int get_size(node*& p) { return p ? p->sz : 0; }
    
      void push_up(node*& p) {
        if (!p) return;
        p->sz = get_size(p->l) + get_size(p->r) + 1;
      }
    
      node* root;
    
      node* merge(node* a, node* b) {
        if (!a) return b;
        if (!b) return a;
        if (a->rnd < b->rnd) {
          a->r = merge(a->r, b);
          push_up(a);
          return a;
        } else {
          b->l = merge(a, b->l);
          push_up(b);
          return b;
        }
      }
    
      void split_val(node* p, const int& k, node*& a, node*& b) {
        if (!p)
          a = b = NULL;
        else {
          if (p->v <= k) {
            a = p;
            split_val(p->r, k, a->r, b);
            push_up(a);
          } else {
            b = p;
            split_val(p->l, k, a, b->l);
            push_up(b);
          }
        }
      }
    
      void split_size(node* p, int k, node*& a, node*& b) {
        if (!p)
          a = b = NULL;
        else {
          if (get_size(p->l) <= k) {
            a = p;
            split_size(p->r, k - get_size(p->l), a->r, b);
            push_up(a);
          } else {
            b = p;
            split_size(p->l, k, a, b->l);
            push_up(b);
          }
        }
      }
    
      void ins(int val) {
        node *a, *b;
        split_val(root, val, a, b);
        a = merge(a, new node(val));
        root = merge(a, b);
      }
    
      void del(int val) {
        node *a, *b, *c, *d;
        split_val(root, val, a, b);
        split_val(a, val - 1, c, d);
        delete d;
        root = merge(c, b);
      }
    
      int qry(int val) {
        node *a, *b;
        split_val(root, val, a, b);
        int res = get_size(a);
        root = merge(a, b);
        return res;
      }
    
      int qry(int l, int r) { return qry(r) - qry(l - 1); }
    };
    
    // Fenwick Tree
    Treap T[N];
    
    int lb(int x) { return x & -x; }
    
    void ins(int x, int v) {
      for (; x <= n; x += lb(x)) T[x].ins(v);
    }
    
    void del(int x, int v) {
      for (; x <= n; x += lb(x)) T[x].del(v);
    }
    
    int qry(int x, int mi, int ma) {
      int res = 0;
      for (; x; x -= lb(x)) res += T[x].qry(mi, ma);
      return res;
    }
    
    int main() {
      scanf("%d %d", &n, &m);
      int v;
      for (int i = 1; i <= n; ++i) scanf("%d", &v), pa[v] = i;
      for (int i = 1; i <= n; ++i) scanf("%d", &v), pb[i] = pa[v];
      for (int i = 1; i <= n; ++i) ins(i, pb[i]);
    
      int op, la, lb, ra, rb, x, y;
      for (int i = 1; i <= m; ++i) {
        scanf("%d", &op);
        if (op == 1) {
          scanf("%d %d %d %d", &la, &ra, &lb, &rb);
          printf("%d\n", qry(rb, la, ra) - qry(lb - 1, la, ra));
        } else if (op == 2) {
          scanf("%d %d", &x, &y);
          del(x, pb[x]);
          del(y, pb[y]);
          swap(pb[x], pb[y]);
          ins(x, pb[x]);
          ins(y, pb[y]);
        }
      }
      return 0;
    }
    ```

## 例题 2

???+ note "[Complicated Computations](https://codeforces.com/contest/1436/problem/E)"
    给出一个序列 $a$，将 $a$ 所有连续子序列的 MEX 构成的数组作为 $b$，问 $b$ 的 MEX．一个序列的 MEX 是序列中最小的没出现过的 **正整数**．
    
    序列的长度 $n$ 满足 $1 \le n \le 10^5$．

**观察**：一个序列的 MEX 为 $mex$，当且仅当这个序列包含 $1$ 至 $mex-1$，但不包含 $mex$．

依次判断是否存在 MEX 为 $1$ 至 $n+1$ 的连续子序列．如果没有 MEX 为 $i$ 的连续子序列，那么答案即为 $i$．如果都存在，那么答案为 $n + 2$．

在判断 $i$ 时，将序列视为由零或多个 $i$ 分隔的多个段．如果存在一个段，这个段中包含 $1$ 至 $i - 1$，但不包含 $i$，那么就说明存在值为 $i$ 的连续子序列．

用一个数组 $Y_j$ 记录上一个值为 $a_j$ 的元素的位置，以 $j$ 作为 $x$，$Y_j$ 作为 $y$，$a_j$ 作为 $z$．这样，计算段内是否包含 $1$ 至 $i - 1$ 就是一个三维偏序的问题．形式化的说，判断段 $[l, r]$ 的 MEX 值是否为 $i$，就是看满足 $l \le j \le r, Y_j \le l - 1, a_j \le i - 1$ 的点的个数是否为 $i-1$．

如果在判断完值为 $i$ 的元素之后再将对应的点插入，这时因为 $[l, r]$ 内只存在 $a_j \le i - 1$ 的元素，所以上述三维偏序问题就可以转换为二维偏序的问题．

??? note "参考代码（分块套树状数组 - 78ms）"
    ```cpp
    #include <cmath>
    #include <cstdio>
    #include <vector>
    using namespace std;
    constexpr int N = 1e5 + 5;
    constexpr int M = 316 + 5;  // sqrt(N) + 5
    
    // 分块
    int nn, b[N], block_size, block_cnt, block_id[N], L[N], R[N], T[M][N];
    
    void build(int n) {
      nn = n;
      block_size = sqrt(nn);
      block_cnt = nn / block_size;
      for (int i = 1; i <= block_cnt; ++i) {
        L[i] = R[i - 1] + 1;
        R[i] = i * block_size;
      }
      if (R[block_cnt] < nn) {
        ++block_cnt;
        L[block_cnt] = R[block_cnt - 1] + 1;
        R[block_cnt] = nn;
      }
      for (int j = 1; j <= block_cnt; ++j)
        for (int i = L[j]; i <= R[j]; ++i) block_id[i] = j;
    }
    
    int lb(int x) { return x & -x; }
    
    // d = 1: 加点(p, v)
    // d = -1: 删点(p, v)
    void add(int p, int v, int d) {
      for (int i = block_id[p]; i <= block_cnt; i += lb(i))
        for (int j = v; j <= nn; j += lb(j)) T[i][j] += d;
    }
    
    // 询问[1, r]内，纵坐标小于等于val的点有多少个
    int getsum(int p, int v) {
      if (!p) return 0;
      int res = 0;
      int id = block_id[p];
      for (int i = L[id]; i <= p; ++i)
        if (b[i] && b[i] <= v) ++res;
      for (int i = id - 1; i; i -= lb(i))
        for (int j = v; j; j -= lb(j)) res += T[i][j];
      return res;
    }
    
    // 询问[l, r]内，纵坐标小于等于val的点有多少个
    int query(int l, int r, int val) {
      if (l > r) return -1;
      int res = getsum(r, val) - getsum(l - 1, val);
      return res;
    }
    
    // 加点(p, v)
    void update(int p, int v) {
      b[p] = v;
      add(p, v, 1);
    }
    
    int n, a[N];
    vector<int> g[N];
    
    int main() {
      scanf("%d", &n);
    
      // 为了减少讨论，加了哨兵节点
      // 因为树状数组添加的时候，为0可能会死循环，所以整体往右偏移一位
      // a_1和a_{n+2}为哨兵节点
      for (int i = 2; i <= n + 1; ++i) scanf("%d", &a[i]);
      for (int i = 2; i <= n + 1; ++i) g[a[i]].push_back(i);
    
      // 分块
      build(n + 2);
    
      int ans = n + 2, lst, ok;
      for (int i = 1; i <= n + 1; ++i) {
        g[i].push_back(n + 2);
    
        lst = 1;
        ok = 0;
        for (int pos : g[i]) {
          if (query(lst + 1, pos - 1, lst) == i - 1) {
            ok = 1;
            break;
          }
          lst = pos;
        }
    
        if (!ok) {
          ans = i;
          break;
        }
    
        lst = 1;
        g[i].pop_back();
        for (int pos : g[i]) {
          update(pos, lst);
          lst = pos;
        }
      }
      printf("%d\n", ans);
      return 0;
    }
    ```

??? note "参考代码（线段树套 Treap-468ms）"
    ```cpp
    #include <cstdio>
    #include <random>
    #include <vector>
    using namespace std;
    constexpr int N = 1e5 + 5;
    
    vector<int> g[N];
    int n, a[N];
    
    mt19937 rng(random_device{}());
    
    struct Treap {
      struct node {
        node *l, *r;
        unsigned rnd;
        int sz, v;
    
        node(int _v) : l(NULL), r(NULL), rnd(rng()), sz(1), v(_v) {}
      };
    
      int get_size(node*& p) { return p ? p->sz : 0; }
    
      void push_up(node*& p) {
        if (!p) return;
        p->sz = get_size(p->l) + get_size(p->r) + 1;
      }
    
      node* root;
    
      node* merge(node* a, node* b) {
        if (!a) return b;
        if (!b) return a;
        if (a->rnd < b->rnd) {
          a->r = merge(a->r, b);
          push_up(a);
          return a;
        } else {
          b->l = merge(a, b->l);
          push_up(b);
          return b;
        }
      }
    
      void split_val(node* p, const int& k, node*& a, node*& b) {
        if (!p)
          a = b = NULL;
        else {
          if (p->v <= k) {
            a = p;
            split_val(p->r, k, a->r, b);
            push_up(a);
          } else {
            b = p;
            split_val(p->l, k, a, b->l);
            push_up(b);
          }
        }
      }
    
      void split_size(node* p, int k, node*& a, node*& b) {
        if (!p)
          a = b = NULL;
        else {
          if (get_size(p->l) <= k) {
            a = p;
            split_size(p->r, k - get_size(p->l), a->r, b);
            push_up(a);
          } else {
            b = p;
            split_size(p->l, k, a, b->l);
            push_up(b);
          }
        }
      }
    
      void insert(int val) {
        node *a, *b;
        split_val(root, val, a, b);
        a = merge(a, new node(val));
        root = merge(a, b);
      }
    
      int query(int val) {
        node *a, *b;
        split_val(root, val, a, b);
        int res = get_size(a);
        root = merge(a, b);
        return res;
      }
    
      int qry(int l, int r) { return query(r) - query(l - 1); }
    };
    
    // Segment Tree
    Treap T[N << 2];
    
    void insert(int x, int l, int r, int p, int val) {
      T[x].insert(val);
      if (l == r) return;
      int mid = (l + r) >> 1;
      if (p <= mid)
        insert(x << 1, l, mid, p, val);
      else
        insert(x << 1 | 1, mid + 1, r, p, val);
    }
    
    int query(int x, int l, int r, int L, int R, int val) {
      if (l == L && r == R) return T[x].query(val);
      int mid = (l + r) >> 1;
      if (R <= mid) return query(x << 1, l, mid, L, R, val);
      if (L > mid) return query(x << 1 | 1, mid + 1, r, L, R, val);
      return query(x << 1, l, mid, L, mid, val) +
             query(x << 1 | 1, mid + 1, r, mid + 1, R, val);
    }
    
    int query(int l, int r, int val) {
      if (l > r) return -1;
      return query(1, 1, n, l, r, val);
    }
    
    int main() {
      scanf("%d", &n);
      for (int i = 1; i <= n; ++i) scanf("%d", &a[i]);
      for (int i = 1; i <= n; ++i) g[a[i]].push_back(i);
    
      // a_0 和 a_{n+1}为哨兵节点
      int ans = n + 2, lst, ok;
      for (int i = 1; i <= n + 1; ++i) {
        g[i].push_back(n + 1);
    
        lst = 0;
        ok = 0;
        for (int pos : g[i]) {
          if (query(lst + 1, pos - 1, lst) == i - 1) {
            ok = 1;
            break;
          }
          lst = pos;
        }
    
        if (!ok) {
          ans = i;
          break;
        }
    
        lst = 0;
        g[i].pop_back();
        for (int pos : g[i]) {
          insert(1, 1, n, pos, lst);
          lst = pos;
        }
      }
      printf("%d\n", ans);
      return 0;
    }
    ```


## ds/block-array.md

## 建立块状数组

块状数组，即把一个数组分为几个块，块内信息整体保存，若查询时遇到两边不完整的块直接暴力查询．一般情况下，块的长度为 $O(\sqrt{n})$．详细分析可以阅读 2017 年国家集训队论文中徐明宽的《非常规大小分块算法初探》．

下面直接给出一种建立块状数组的代码．

???+ note "实现"
    ```cpp
    num = sqrt(n);
    for (int i = 1; i <= num; i++)
      st[i] = n / num * (i - 1) + 1, ed[i] = n / num * i;
    ed[num] = n;
    for (int i = 1; i <= num; i++) {
      for (int j = st[i]; j <= ed[i]; j++) {
        belong[j] = i;
      }
      size[i] = ed[i] - st[i] + 1;
    }
    ```

其中 `st[i]` 和 `ed[i]` 为块的起点和终点，`size[i]` 为块的大小．

## 保存与修改块内信息

### 例题 1：[教主的魔法](https://www.luogu.com.cn/problem/P2801)

两种操作：

1.  区间 $[x,y]$ 每个数都加上 $z$；
2.  查询区间 $[x,y]$ 内大于等于 $z$ 的数的个数．

我们要询问一个块内大于等于一个数的数的个数，所以需要一个 `t` 数组对块内排序，`a` 为原来的（未被排序的）数组．对于整块的修改，使用类似于标记永久化的方式，用 `delta` 数组记录现在块内整体加上的值．设 $q$ 为查询和修改的操作次数总和，则时间复杂度 $O(q\sqrt{n}\log n)$．

用 `delta` 数组记录每个块的整体赋值情况．

???+ note "实现"
    ```cpp
    void Sort(int k) {
      for (int i = st[k]; i <= ed[k]; i++) t[i] = a[i];
      sort(t + st[k], t + ed[k] + 1);
    }
    
    void Modify(int l, int r, int c) {
      int x = belong[l], y = belong[r];
      if (x == y)  // 区间在一个块内就直接修改
      {
        for (int i = l; i <= r; i++) a[i] += c;
        Sort(x);
        return;
      }
      for (int i = l; i <= ed[x]; i++) a[i] += c;     // 直接修改起始段
      for (int i = st[y]; i <= r; i++) a[i] += c;     // 直接修改结束段
      for (int i = x + 1; i < y; i++) delta[i] += c;  // 中间的块整体打上标记
      Sort(x);
      Sort(y);
    }
    
    int Answer(int l, int r, int c) {
      int ans = 0, x = belong[l], y = belong[r];
      if (x == y) {
        for (int i = l; i <= r; i++)
          if (a[i] + delta[x] >= c) ans++;
        return ans;
      }
      for (int i = l; i <= ed[x]; i++)
        if (a[i] + delta[x] >= c) ans++;
      for (int i = st[y]; i <= r; i++)
        if (a[i] + delta[y] >= c) ans++;
      for (int i = x + 1; i <= y - 1; i++)
        ans +=
            ed[i] - (lower_bound(t + st[i], t + ed[i] + 1, c - delta[i]) - t) + 1;
      // 用 lower_bound 找出中间每一个整块中第一个大于等于 c 的数的位置
      return ans;
    }
    ```

### 例题 2：寒夜方舟

两种操作：

1.  区间 $[x,y]$ 每个数都变成 $z$；
2.  查询区间 $[x,y]$ 内小于等于 $z$ 的数的个数．

用 `delta` 数组记录现在块内被整体赋值为何值．当该块未被整体赋值时，用一个特殊值（如 `0x3f3f3f3f3f3f3f3fll`）加以表示．对于边角块，查询前要 `pushdown`，把块内存的信息下放到每一个数上．赋值之后记得重新 `sort` 一遍．其他方面同上题．

???+ note "实现"
    ```cpp
    void Sort(int k) {
      for (int i = st[k]; i <= ed[k]; i++) t[i] = a[i];
      sort(t + st[k], t + ed[k] + 1);
    }
    
    void PushDown(int x) {
      if (delta[x] != 0x3f3f3f3f3f3f3f3fll)  // 用该值标记块内没有被整体赋值
        for (int i = st[x]; i <= ed[x]; i++) a[i] = t[i] = delta[x];
      delta[x] = 0x3f3f3f3f3f3f3f3fll;
    }
    
    void Modify(int l, int r, int c) {
      int x = belong[l], y = belong[r];
      PushDown(x);
      if (x == y) {
        for (int i = l; i <= r; i++) a[i] = c;
        Sort(x);
        return;
      }
      PushDown(y);
      for (int i = l; i <= ed[x]; i++) a[i] = c;
      for (int i = st[y]; i <= r; i++) a[i] = c;
      Sort(x);
      Sort(y);
      for (int i = x + 1; i < y; i++) delta[i] = c;
    }
    
    int Binary_Search(int l, int r, int c) {
      int ans = l - 1, mid;
      while (l <= r) {
        mid = (l + r) / 2;
        if (t[mid] <= c)
          ans = mid, l = mid + 1;
        else
          r = mid - 1;
      }
      return ans;
    }
    
    int Answer(int l, int r, int c) {
      int ans = 0, x = belong[l], y = belong[r];
      PushDown(x);
      if (x == y) {
        for (int i = l; i <= r; i++)
          if (a[i] <= c) ans++;
        return ans;
      }
      PushDown(y);
      for (int i = l; i <= ed[x]; i++)
        if (a[i] <= c) ans++;
      for (int i = st[y]; i <= r; i++)
        if (a[i] <= c) ans++;
      for (int i = x + 1; i <= y - 1; i++) {
        if (0x3f3f3f3f3f3f3f3fll == delta[i])
          ans += Binary_Search(st[i], ed[i], c) - st[i] + 1;
        else if (delta[i] <= c)
          ans += size[i];
      }
      return ans;
    }
    ```

## 练习

1.  [单点修改，区间查询](https://loj.ac/problem/130)
2.  [区间修改，区间查询](https://loj.ac/problem/132)
3.  [【模板】线段树 2](https://www.luogu.com.cn/problem/P3373)
4.  [「Ynoi2019 模拟赛」Yuno loves sqrt technology III](https://www.luogu.com.cn/problem/P5048)
5.  [「Violet」蒲公英](https://www.luogu.com.cn/problem/P4168)
6.  [作诗](https://www.luogu.com.cn/problem/P4135)


## ds/block-list.md

author: HeRaNO, konnyakuxzy, littlefrog

![./images/kuaizhuanglianbiao.png](./images/kuaizhuanglianbiao.png "./images/kuaizhuanglianbiao.png")

块状链表大概就长这样……

不难发现块状链表就是一个链表，每个节点指向一个数组．
我们把原来长度为 n 的数组分为 $\sqrt{n}$ 个节点，每个节点对应的数组大小为 $\sqrt{n}$．
所以我们这么定义结构体，代码见下．
其中 `sqn` 表示 `sqrt(n)` 即 $\sqrt{n}$，`pb` 表示 `push_back`，即在这个 `node` 中加入一个元素．

???+ note "实现"
    ```cpp
    struct node {
      node* nxt;
      int size;
      char d[(sqn << 1) + 5];
    
      node() { size = 0, nxt = NULL, memset(d, 0, sizeof(d)); }
    
      void pb(char c) { d[size++] = c; }
    };
    ```

块状链表应该至少支持：分裂、插入、查找．
什么是分裂？分裂就是分裂一个 `node`，变成两个小的 `node`，以保证每个 `node` 的大小都接近 $\sqrt{n}$（否则可能退化成普通数组）．当一个 `node` 的大小超过 $2\times \sqrt{n}$ 时执行分裂操作．

分裂操作怎么做呢？先新建一个节点，再把被分裂的节点的后 $\sqrt{n}$ 个值 `copy` 到新节点，然后把被分裂的节点的后 $\sqrt{n}$ 个值删掉（`size--`），最后把新节点插入到被分裂节点的后面即可．

块状链表的所有操作的复杂度都是 $\sqrt{n}$ 的．

还有一个要说的．
随着元素的插入（或删除），$n$ 会变，$\sqrt{n}$ 也会变．这样块的大小就会变化，我们难道还要每次维护块的大小？

其实不然，把 $\sqrt{n}$ 设置为一个定值即可．比如题目给的范围是 $10^6$，那么 $\sqrt{n}$ 就设置为大小为 $10^3$ 的常量，不用更改它．

```cpp
list<vector<char>> orz_list;
```

## libstdc++ 中的 `rope`

### 导入

libstdc++ 中的 `rope` 也起到块状链表的作用，它采用可持久化平衡树实现，可完成随机访问和插入、删除元素的操作．

由于 `rope` 并不是真正的用块状链表来实现，所以它的时间复杂度并不等同于块状链表，而是相当于可持久化平衡树的复杂度（即 $O(\log n)$）．

可以使用如下方法来引入：

```cpp
#include <ext/rope>
using namespace __gnu_cxx;
```

???+ warning "关于双下划线开头的库函数"
    OI 中，关于能否使用双下划线开头的库函数曾经一直不确定，2021 年 CCF 发布的 [关于 NOI 系列活动中编程语言使用限制的补充说明](https://www.noi.cn/xw/2021-09-01/735729.shtml) 中提到「允许使用以下划线开头的库函数或宏，但具有明确禁止操作的库函数和宏除外」．故 `rope` 目前可以在 OI 中正常使用．

### 基本操作

|             操作            |               作用              |
| :-----------------------: | :---------------------------: |
|       `rope<int> a`       | 初始化 `rope`（与 `vector` 等容器很相似） |
|      `a.push_back(x)`     |       在 `a` 的末尾添加元素 `x`       |
|     `a.insert(pos, x)`    |   在 `a` 的 `pos` 个位置添加元素 `x`   |
|     `a.erase(pos, x)`     |  在 `a` 的 `pos` 个位置删除 `x` 个元素  |
|     `a.at(x)` 或 `a[x]`    |       访问 `a` 的第 `x` 个元素       |
| `a.length()` 或 `a.size()` |           获取 `a` 的大小          |

## 例题

[POJ2887 Big String](http://poj.org/problem?id=2887)

题解：
很简单的模板题．代码如下：

```cpp
--8<-- "docs/ds/code/block-list/block-list_1.cpp"
```


## ds/bst.md

author: 2323122, aofall, AtomAlpaca, Bocity, CoelacanthusHex, countercurrent-time, Early0v0, Enter-tainer, fearlessxjdx, Great-designer, H-J-Granger, hsfzLZH1, iamtwz, Ir1d, ksyx, Marcythm, NachtgeistW, ouuan, Persdre, shuzhouliu, StudyingFather, SukkaW, Tiphereth-A, wsyhb, Yesphet, yuhuoji, lingkerio, bililateral, q-wind

## 定义

二叉搜索树是一种二叉树的树形数据结构，其定义如下：

1.  空树是二叉搜索树．

2.  若二叉搜索树的左子树不为空，则其左子树上所有点的附加权值均小于其根节点的值．

3.  若二叉搜索树的右子树不为空，则其右子树上所有点的附加权值均大于其根节点的值．

4.  二叉搜索树的左右子树均为二叉搜索树．

二叉搜索树上的基本操作所花费的时间与这棵树的高度成正比．对于一个有 $n$ 个结点的二叉搜索树中，这些操作的最优时间复杂度为 $O(\log n)$，最坏为 $O(n)$．随机构造这样一棵二叉搜索树的期望高度为 $O(\log n)$．

## 过程

### 二叉搜索树节点的定义

???+ note "实现"
    ```cpp
    struct TreeNode {
      int key;
      TreeNode* left;
      TreeNode* right;
      // 维护其他信息，如高度，节点数量等
      int size;   // 当前节点为根的子树大小
      int count;  // 当前节点的重复数量
    
      TreeNode(int value)
          : key(value), size(1), count(1), left(nullptr), right(nullptr) {}
    };
    ```

### 遍历二叉搜索树

由二叉搜索树的递归定义可得，二叉搜索树的中序遍历权值的序列为非降的序列．时间复杂度为 $O(n)$．

遍历一棵二叉搜索树的代码如下：

???+ note "实现"
    ```cpp
    void inorderTraversal(TreeNode* root) {
      if (root == nullptr) {
        return;
      }
      inorderTraversal(root->left);
      std::cout << root->key << " ";
      inorderTraversal(root->right);
    }
    ```

### 查找最小/最大值

由二叉搜索树的性质可得，二叉搜索树上的最小值为二叉搜索树左链的顶点，最大值为二叉搜索树右链的顶点．时间复杂度为 $O(h)$．

???+ note "实现"
    ```cpp
    int findMin(TreeNode* root) {
      if (root == nullptr) {
        return -1;
      }
      while (root->left != nullptr) {
        root = root->left;
      }
      return root->key;
    }
    
    int findMax(TreeNode* root) {
      if (root == nullptr) {
        return -1;
      }
      while (root->right != nullptr) {
        root = root->right;
      }
      return root->key;
    }
    ```

### 搜索元素

在以 `root` 为根节点的二叉搜索树中搜索一个值为 `value` 的节点．

分类讨论如下：

-   若 `root` 为空，返回 `false`．
-   若 `root` 的权值等于 `value`，返回 `true`．
-   若 `root` 的权值大于 `value`，在 `root` 的左子树中继续搜索．
-   若 `root` 的权值小于 `value`，在 `root` 的右子树中继续搜索．

时间复杂度为 $O(h)$．

???+ note "实现"
    ```cpp
    bool search(TreeNode* root, int target) {
      if (root == nullptr) {
        return false;
      }
      if (root->key == target) {
        return true;
      } else if (target < root->key) {
        return search(root->left, target);
      } else {
        return search(root->right, target);
      }
    }
    ```

插入，删除，修改都需要先在二叉搜索树中进行搜索．

### 插入一个元素

在以 `root` 为根节点的二叉搜索树中插入一个值为 `value` 的节点．

分类讨论如下：

-   若 `root` 为空，直接返回一个值为 `value` 的新节点．

-   若 `root` 的权值等于 `value`，该节点的附加域该值出现的次数自增 $1$．

-   若 `root` 的权值大于 `value`，在 `root` 的左子树中插入权值为 `value` 的节点．

-   若 `root` 的权值小于 `value`，在 `root` 的右子树中插入权值为 `value` 的节点．

时间复杂度为 $O(h)$．

???+ note "实现"
    ```cpp
    TreeNode* insert(TreeNode* root, int value) {
      if (root == nullptr) {
        return new TreeNode(value);
      }
      if (value < root->key) {
        root->left = insert(root->left, value);
      } else if (value > root->key) {
        root->right = insert(root->right, value);
      } else {
        root->count++;  // 节点值相等，增加重复数量
      }
      root->size = root->count + (root->left ? root->left->size : 0) +
                   (root->right ? root->right->size : 0);  // 更新节点的子树大小
      return root;
    }
    ```

### 删除一个元素

在以 `root` 为根节点的二叉搜索树中删除一个值为 `value` 的节点．

先在二叉搜索树中搜索权值为 `value` 的节点，分类讨论如下：

-   若该节点的附加 `count` 大于 $1$，只需要减少 `count`．

-   若该节点的附加 `count` 为 $1$：

    -   若 `root` 为叶子节点，直接删除该节点即可．

    -   若 `root` 为链节点，即只有一个儿子的节点，返回这个儿子．

    -   若 `root` 有两个非空子节点，一般是用它左子树的最大值（左子树最右的节点）或右子树的最小值（右子树最左的节点）代替它，然后将它删除．

时间复杂度 $O(h)$．

???+ note "实现"
    方法使用 `root = remove(root, 1)` 表示删除根节点为 `root` 树中值为 1 的节点，并返回新的根节点．
    
    ```cpp
    // 此处返回值为删除 value 后的新 root
    TreeNode* remove(TreeNode* root, int value) {
      if (root == nullptr) {
        return root;
      }
      if (value < root->key) {
        root->left = remove(root->left, value);
      } else if (value > root->key) {
        root->right = remove(root->right, value);
      } else {
        if (root->count > 1) {
          root->count--;  // 节点重复数量大于1，减少重复数量
        } else {
          if (root->left == nullptr) {
            TreeNode* temp = root->right;
            delete root;
            return temp;
          } else if (root->right == nullptr) {
            TreeNode* temp = root->left;
            delete root;
            return temp;
          } else {
            TreeNode* successor = findMinNode(root->right);
            root->key = successor->key;
            root->count = successor->count;  // 更新重复数量
            // 当 successor->count > 1时，也应该删除该节点，否则
            // 后续的删除只会减少重复数量
            successor->count = 1;
            root->right = remove(root->right, successor->key);
          }
        }
      }
      // 继续维护size，不写成 --root->size;
      // 是因为value可能不在树中，从而可能未发生删除
      root->size = root->count + (root->left ? root->left->size : 0) +
                   (root->right ? root->right->size : 0);
      return root;
    }
    
    // 此处以右子树的最小值为例
    TreeNode* findMinNode(TreeNode* root) {
      while (root->left != nullptr) {
        root = root->left;
      }
      return root;
    }
    ```

### 求元素的排名

排名定义为将数组元素升序排序后第一个相同元素之前的数的个数加一．

查找一个元素的排名，首先从根节点跳到这个元素，若向右跳，答案加上左儿子节点个数加当前节点重复的数个数，最后答案加上终点的左儿子子树大小加一．

时间复杂度 $O(h)$．

???+ note "实现"
    ```cpp
    int queryRank(TreeNode* root, int v) {
      if (root == nullptr) return 0;
      if (root->key == v) return (root->left ? root->left->size : 0) + 1;
      if (root->key > v) return queryRank(root->left, v);
      return queryRank(root->right, v) + (root->left ? root->left->size : 0) +
             root->count;
    }
    ```

### 查找排名为 k 的元素

在一棵子树中，根节点的排名取决于其左子树的大小．

-   若其左子树的大小大于等于 $k$，则该元素在左子树中；

-   若其左子树的大小在区间 $[k-\textit{count},k-1]$（`count` 为当前结点的值的出现次数）中，则该元素为子树的根节点；

-   若其左子树的大小小于 $k-\textit{count}$，则该元素在右子树中．

时间复杂度 $O(h)$．

???+ note "实现"
    ```cpp
    int querykth(TreeNode* root, int k) {
      if (root == nullptr) return -1;  // 或者根据需求返回其他合适的值
      if (root->left) {
        if (root->left->size >= k) return querykth(root->left, k);
        if (root->left->size + root->count >= k) return root->key;
      } else {
        if (k <= root->count) return root->key;
      }
      return querykth(root->right,
                      k - (root->left ? root->left->size : 0) - root->count);
    }
    ```

## 平衡树简介

使用搜索树的目的之一是缩短插入、删除、修改和查找（插入、删除、修改都包括查找操作）节点的时间．

关于查找效率，如果一棵树的高度为 $h$，在最坏的情况，查找一个关键字需要对比 $h$ 次，查找时间复杂度（也为平均查找长度 ASL，Average Search Length）不超过 $O(h)$．一棵理想的二叉搜索树所有操作的时间可以缩短到 $O(\log n)$（n 是节点总数）．

然而 $O(\log n)$ 的时间复杂度仅为理想情况．在最坏情况下，搜索树有可能退化为链表．想象一棵每个结点只有右孩子的二叉搜索树，那么它的性质就和链表一样，所有操作（增删改查）的时间是 $O(n)$．

可以发现操作的复杂度与树的高度 $h$ 有关．由此引出了平衡树，通过一定操作维持树的高度（平衡性）来降低操作的复杂度．

### 平衡性的定义

关于一棵搜索树是否「**平衡**」，不同的平衡树中对「**平衡**」有着不同的定义．比如以 T 为根节点的二叉搜索树，左子树和右子树的高度相差很大，或者左子树的节点个数远大于右子树的节点个数，这棵树显然不具有平衡性．

对于二叉搜索树来说，常见的平衡性的定义是指：以 T 为根节点的树，每一个结点的左子树和右子树高度差最多为 1．

-   [Splay 树](splay.md) 中，对于任意节点的访问操作（搜索、插入还是删除），都会将被访问的节点移动到树的根节点位置．

-   [AVL 树](avl.md) 每个节点 N 维护以 N 为根节点的树的高度信息．AVL 树对平衡性的定义：如果 T 是一棵 AVL 树，当且仅当左右子树也是 AVL 树，且 $|height(T->left) - height(T->right)| \leq 1$．

-   [Size Balanced Tree](sbt.md) 每个节点 N 维护以 N 为根节点的树中节点个数 `size`．对平衡性的定义：任意节点的 `size` 不小于其兄弟节点（Sibling）的所有子节点（Nephew）的 `size`．

此外，对于拥有同样元素值集合的搜索树，平衡状态可能是不唯一的．也就是说，可能两棵不同的搜索树，含有的元素值集合相同，并且都是平衡的．

### 平衡的调整过程

对不满足平衡条件的搜索树进行调整操作，可以使不平衡的搜索树重新具有平衡性．

关于二叉平衡树，平衡的调整操作分为包括 **左旋（Left Rotate 或者 zag）** 和 **右旋（Right Rotate 或者 zig）** 两种．由于二叉平衡树在调整时需要保证中序遍历序列不变．这两种操作均不改变中序遍历序列．

在这里先介绍右旋，右旋也称为「右单旋转」或「LL 平衡旋转」．对于结点 $A$ 的右旋操作是指：将 $A$ 的左孩子 $B$ 向右上旋转，代替 $A$ 成为根节点，将 $A$ 结点向右下旋转成为 $B$ 的右子树的根结点，$B$ 的原来的右子树变为 $A$ 的左子树．

![bst-rotate](images/bst-rotate.svg)

右旋操作只改变了三组结点关联，相当于对三组边进行循环置换一下，因此需要暂存一个结点再进行轮换更新．

对于右旋操作一般的更新顺序是：暂存 $B$ 结点（新的根节点），让 $A$ 的左孩子指向 $B$ 的右子树 $T2$，再让 $B$ 的右孩子指针指向 $A$，最后让 $A$ 的父结点指向暂存的 $B$．

完全同理，有对应的左旋操作，也称为「左单旋转」或「RR 平衡旋转」．左旋操作与右旋操作互为镜像．

下面给出左旋和右旋的代码．

???+ note "实现"
    ```cpp
    TreeNode* rotateLeft(TreeNode* root) {
      TreeNode* newRoot = root->right;
      root->right = newRoot->left;
      newRoot->left = root;
      // 更新相关节点的信息
      updateHeight(root);
      updateHeight(newRoot);
      return newRoot;  // 返回新的根节点
    }
    
    TreeNode* rotateRight(TreeNode* root) {
      TreeNode* newRoot = root->left;
      root->left = newRoot->right;
      newRoot->right = root;
      updateHeight(root);
      updateHeight(newRoot);
      return newRoot;
    }
    ```

对于这段示例代码，在调用时需要保存 `root` 的父节点 `pre`．方法返回指向新的根节点的指针，只需要将 `pre` 指向新的根节点即可．

#### 四种平衡性破坏的情况

虽然不同的二叉平衡树的定义有所区别，不同二叉平衡树区别只在于节点维护的信息不同，以及旋转调整后节点更新的信息不同．二叉平衡树平衡性被破坏的情况只有以下四种．进行平衡性调整的操作只包括左旋和右旋．以下先介绍四种情况，再对不同的二叉平衡树进行对比．

LL 型：T 的左孩子的左子树过长导致平衡性破坏．

调整方式：右旋节点 T．

![bst-LL](images/bst-LL.svg)

RR 型：与 LL 型类似，T 的右孩子的右子树过长导致平衡性破坏．

调整方式：左旋节点 T．

![bst-RR](images/bst-RR.svg)

LR 型：T 的左孩子的右子树过长导致平衡性破坏．

调整方式：先左旋节点 L，成为 LL 型，再右旋节点 T．

![bst-LR](images/bst-LR.svg)

RL 型：与 LR 型类似，T 的右孩子的左子树过长导致平衡性破坏．

调整方式：先右旋节点 R，成为 RR 型，再左旋节点 T．

![bst-RL](images/bst-RL.svg)


## ds/cartesian-tree.md

author: sshwy, zhouyuyang2002, StudyingFather, Ir1d, ouuan, Enter-tainer, AtomAlpaca

## 引入

笛卡尔树是一种二叉树，每一个节点由一个键值二元组 $(k,w)$ 构成．要求 $k$ 满足二叉搜索树（BST）的性质，而 $w$ 满足堆的性质．如果笛卡尔树的 $k,w$ 键值确定，且 $k$ 互不相同，$w$ 也互不相同，那么这棵笛卡尔树的结构是唯一的．如下图：

![eg](./images/cartesian-tree1.png)

（图源自维基百科）

上面这棵笛卡尔树相当于把数组元素值当作键值 $w$，而把数组下标当作键值 $k$．可以发现，这棵树的键值 $k$ 满足 BST 的性质，而键值 $w$ 满足小根堆的性质．同时根据二叉搜索树的性质，可以发现这种特殊的笛卡尔树满足一棵子树内的下标是一个连续区间．

竞赛中使用笛卡尔树时，常用数组下标作为二元组的键值 $k$，数组下标 $k$ 满足 BST 性质．

下文使用 $k,w$ 时，默认 $k$ 满足 BST 性质，$w$ 满足堆的性质．

## 单调栈构建笛卡尔树

### 过程

我们考虑将元素按 $k$ 升序依次插入到当前的笛卡尔树中．

对于一棵笛卡尔树，定义「右链」为从根节点开始一直走右儿子，直到走到一个没有右儿子的节点形成的链．则插入节点后，这个节点一定在右链上．因为是按照满足 BST 性质的 $k$ 升序插入，那么这个新插入的节点必然在树的 **最右端**．这个节点不可能是一个左儿子，也没有右儿子．

于是我们执行这样一个过程，从下往上比较右链节点与当前节点 $u$ 的 $w$，如果找到了一个右链上的节点 $x$ 满足 $w_x<w_u$，就把 $u$ 接到 $x$ 的右儿子上，而 $x$ 原本的右子树就变成 $u$ 的左子树．

图中红框部分就是我们始终维护的右链：

![build](./images/cartesian-tree2.png)

显然每个数最多进出右链一次（或者说每个点在右链中存在的是一段连续的时间）．这个过程可以用单调栈维护，栈中维护当前笛卡尔树的右链上的节点．一个点不在右链上了就把它弹掉．这样每个点最多进出一次，复杂度 $O(n)$．

???+ note "笛卡尔树与 Treap"
    实际上，Treap 是笛卡尔树的一种，只不过 Treap 中 $w$ 的值完全随机．Treap 有线性的构建算法，如果提前将键值 $k$ 排好序，是可以使用上述单调栈算法完成构建过程的，只不过很少会这么用．

### C++ 实现

```cpp
// stk 维护笛卡尔树中节点对应到序列中的下标
for (int i = 1; i <= n; i++) {
  int k = top;  // top 表示操作前的栈顶，k 表示当前栈顶
  while (k > 0 && w[stk[k]] > w[i]) k--;  // 维护右链上的节点
  if (k) rs[stk[k]] = i;  // 栈顶元素.右儿子 := 当前元素
  if (k < top) ls[i] = stk[k + 1];  // 当前元素.左儿子 := 上一个被弹出的元素
  stk[++k] = i;                     // 当前元素入栈
  top = k;
}
```

## 例题

???+ note "[HDU 1506. Largest Rectangle in a Histogram](https://acm.hdu.edu.cn/showproblem.php?pid=1506)"
    $n$ 个位置，每个位置上的高度是 $h_i$，求最大子矩形．如下图：
    
    ![eg](./images/cartesian-tree3.png)
    
    阴影部分就是图中的最大子矩阵．

??? note "解题思路"
    具体地，我们把下标作为键值 $k$，$h_i$ 作为键值 $w$ 满足小根堆性质，构建一棵 $(i,h_i)$ 的笛卡尔树．
    
    这样我们枚举每个节点 $u$，把 $w_u$（即节点 $u$ 的高度 $h$）作为最大子矩阵的高度．由于我们建立的笛卡尔树满足小根堆性质，因此 $u$ 的子树内的节点的高度都大于等于 $u$．而我们又知道 $u$ 子树内的下标是一段连续的区间．于是我们只需要知道子树的大小，然后就可以算这个区间的最大子矩阵的面积了．用每一个点计算出来的值更新答案即可．显然这个可以一次 DFS 完成，因此复杂度是 $O(n)$ 的．

??? note "参考实现"
    ```cpp
    --8<-- "docs/ds/code/cartesian-tree/cartesian-tree_1.cpp"
    ```

## 参考资料

[笛卡尔树 - 维基百科](https://zh.wikipedia.org/wiki/%E7%AC%9B%E5%8D%A1%E5%B0%94%E6%A0%91)


## ds/cat-tree.md

author: ChungZH, billchenchina, Chrogeek, Early0v0, ethan-enhe, HeRaNO, hsfzLZH1, iamtwz, Ir1d, konnyakuxzy, luoguojie, Marcythm, orzAtalod, StudyingFather, wy-luke, Xeonacid, CCXXXI, chenryang, chenzheAya, CJSoft, cjsoft, countercurrent-time, DawnMagnet, Enter-tainer, GavinZhengOI, Haohu Shen, Henry-ZHR, hjsjhn, hly1204, jaxvanyang, Jebearssica, kenlig, ksyx, megakite, Menci, moon-dim, NachtgeistW, onelittlechildawa, ouuan, shadowice1984, shawlleyw, shuzhouliu, SukkaW, Tiphereth-A, x2e6, Ycrpro, yifan0305, zeningc, hcx2012Git

## 引入

众所周知线段树可以支持高速查询某一段区间的信息和，比如区间最大子段和，区间和，区间矩阵的连乘积等等．

但是有一个问题在于普通线段树的区间询问在某些毒瘤的眼里可能还是有些慢了．

简单来说就是线段树建树的时候需要做 $O(n)$ 次合并操作，而每一次区间询问需要做 $O(\log{n})$ 次合并操作，询问区间和这种东西的时候还可以忍受，但是当我们需要询问区间线性基这种合并复杂度高达 $O(\log^2{w})$ 的信息的话，此时就算是做 $O(\log{n})$ 次合并有些时候在时间上也是不可接受的．

而所谓「猫树」就是一种不支持修改，仅仅支持快速区间询问的一种静态线段树．

构造一棵这样的静态线段树需要 $O(n\log{n})$ 次合并操作，但是此时的查询复杂度被加速至 $O(1)$ 次合并操作．

在处理线性基这样特殊的信息的时候甚至可以将复杂度降至 $O(n\log^2{w})$．

## 原理

在查询 $[l,r]$ 这段区间的信息和的时候，将线段树树上代表 $[l,l]$ 的节点和代表 $[r,r]$ 这段区间的节点在线段树上的 LCA 求出来，设这个节点 $p$ 代表的区间为 $[L,R]$，我们会发现一些非常有趣的性质：

1.  $[L,R]$ 这个区间一定包含 $[l,r]$．显然，因为它既是 $l$ 的祖先又是 $r$ 的祖先．

2.  $[l,r]$ 这个区间一定跨越 $[L,R]$ 的中点．由于 $p$ 是 $l$ 和 $r$ 的 LCA，这意味着 $p$ 的左儿子是 $l$ 的祖先而不是 $r$ 的祖先，$p$ 的右儿子是 $r$ 的祖先而不是 $l$ 的祖先．因此，$l$ 一定在 $[L,\mathit{mid}]$ 这个区间内，$r$ 一定在 $(\mathit{mid},R]$ 这个区间内．

有了这两个性质，我们就可以将询问的复杂度降至 $O(1)$ 了．

## 实现

具体来讲我们建树的时候对于线段树树上的一个节点，设它代表的区间为 $(l,r]$．

不同于传统线段树在这个节点里只保留 $[l,r]$ 的和，我们在这个节点里面额外保存 $(l,\mathit{mid}]$ 的后缀和数组和 $(\mathit{mid},r]$ 的前缀和数组．

这样的话建树的复杂度为 $T(n)=2T(n/2)+O(n)=O(n\log{n})$ 同理空间复杂度也从原来的 $O(n)$ 变成了 $O(n\log{n})$．

下面是最关键的询问了．

如果我们询问的区间是 $[l,r]$ 那么我们把代表 $[l,l]$ 的节点和代表 $[r,r]$ 的节点的 LCA 求出来，记为 $p$．

根据刚才的两个性质，$l,r$ 在 $p$ 所包含的区间之内并且一定跨越了 $p$ 的中点．

这意味这一个非常关键的事实是我们可以使用 $p$ 里面的前缀和数组和后缀和数组，将 $[l,r]$ 拆成 $[l,\mathit{mid}]+(\mathit{mid},r]$ 从而拼出来 $[l,r]$ 这个区间．

而这个过程仅仅需要 $O(1)$ 次合并操作！

不过我们好像忽略了点什么？

似乎求 LCA 的复杂度似乎还不是 $O(1)$，暴力求是 $O(\log{n})$ 的，倍增法则是 $O(\log{\log{n}})$ 的，转 ST 表的代价又太大……

## 堆式建树

具体来将我们将这个序列补成 $2$ 的整次幂，然后建线段树．

此时我们发现线段树上两个节点的 LCA 编号，就是两个节点二进制编号的最长公共前缀 LCP．

稍作思考即可发现在 $x$ 和 $y$ 的二进制下 `lcp(x,y)=x>>digits[x^y]`．（其中 `digits[x]` 表示二进制下 $x$ 的位数，即 $\lfloor \log_2 x \rfloor+1$）

所以我们预处理一个 `digits` 数组即可轻松完成求 LCA 的工作．

这样我们就构建了一个猫树．

由于建树的时候涉及到求前缀和和求后缀和，所以对于线性基这种虽然合并是 $O(\log^2{w})$ 但是求前缀和却是 $O(n\log{n})$ 的信息，使用猫树可以将静态区间线性基从 $O(n\log^2{w}+m\log^2{w}\log{n})$ 优化至 $O(n\log{n}\log{w}+m\log^2{w})$ 的复杂度．

### 参考

-   [immortalCO 的博客](https://immortalco.blog.uoj.ac/blog/2102)
-   [\[Kle77\]](http://ieeexplore.ieee.org/document/1675628/) V. Klee, "Can the Measure of be Computed in Less than O (n log n) Steps?," Am. Math. Mon., vol. 84, no. 4, pp. 284–285, Apr. 1977.
-   [\[BeW80\]](https://www.tandfonline.com/doi/full/10.1080/00029890.1977.11994336) Bentley and Wood, "An Optimal Worst Case Algorithm for Reporting Intersections of Rectangles," IEEE Trans. Comput., vol. C–29, no. 7, pp. 571–577, Jul. 1980.


## ds/decompose.md

author: Ir1d, HeRaNO, Xeonacid

## 简介

其实，分块是一种思想，而不是一种数据结构．

从 NOIP 到 NOI 到 IOI，各种难度的分块思想都有出现．

分块的基本思想是，通过对原数据的适当划分，并在划分后的每一个块上预处理部分信息，从而较一般的暴力算法取得更优的时间复杂度．

分块的时间复杂度主要取决于分块的块长，一般可以通过均值不等式求出某个问题下的最优块长，以及相应的时间复杂度．

分块是一种很灵活的思想，相较于树状数组和线段树，分块的优点是通用性更好，可以维护很多树状数组和线段树无法维护的信息．

当然，分块的缺点是渐近意义的复杂度，相较于线段树和树状数组不够好．

不过在大多数问题上，分块仍然是解决这些问题的一个不错选择．

下面是几个例子．

## 区间和

??? note "例题 [LibreOJ 6280 数列分块入门 4](https://loj.ac/problem/6280)"
    给定一个长度为 $n$ 的序列 $\{a_i\}$，需要执行 $n$ 次操作．操作分为两种：
    
    1.  给 $a_l \sim a_r$ 之间的所有数加上 $x$；
    2.  求 $\sum_{i=l}^r a_i$．
    
        $1 \leq n \leq 5 \times 10^4$

我们将序列按每 $s$ 个元素一块进行分块，并记录每块的区间和 $b_i$．

$$
\underbrace{a_1, a_2, \ldots, a_s}_{b_1}, \underbrace{a_{s+1}, \ldots, a_{2s}}_{b_2}, \dots, \underbrace{a_{(s-1) \times s+1}, \dots, a_n}_{b_{\frac{n}{s}}}
$$

最后一个块可能是不完整的（因为 $n$ 很可能不是 $s$ 的倍数），但是这对于我们的讨论来说并没有太大影响．

首先看查询操作：

-   若 $l$ 和 $r$ 在同一个块内，直接暴力求和即可，因为块长为 $s$，因此最坏复杂度为 $O(s)$．
-   若 $l$ 和 $r$ 不在同一个块内，则答案由三部分组成：以 $l$ 开头的不完整块，中间几个完整块，以 $r$ 结尾的不完整块．对于不完整的块，仍然采用上面暴力计算的方法，对于完整块，则直接利用已经求出的 $b_i$ 求和即可．这种情况下，最坏复杂度为 $O(\dfrac{n}{s}+s)$．

接下来是修改操作：

-   若 $l$ 和 $r$ 在同一个块内，直接暴力修改即可，因为块长为 $s$，因此最坏复杂度为 $O(s)$．
-   若 $l$ 和 $r$ 不在同一个块内，则需要修改三部分：以 $l$ 开头的不完整块，中间几个完整块，以 $r$ 结尾的不完整块．对于不完整的块，仍然是暴力修改每个元素的值（别忘了更新区间和 $b_i$），对于完整块，则直接修改 $b_i$ 即可．这种情况下，最坏复杂度和仍然为 $O(\dfrac{n}{s}+s)$．

利用均值不等式可知，当 $\dfrac{n}{s}=s$，即 $s=\sqrt n$ 时，单次操作的时间复杂度最优，为 $O(\sqrt n)$．

??? note "参考代码"
    ```cpp
    --8<-- "docs/ds/code/decompose/decompose_1.cpp"
    ```

## 区间和 2

上一个做法的复杂度是 $\Omega(1) , O(\sqrt{n})$．

我们在这里介绍一种 $O(\sqrt{n}) - O(1)$ 的算法．

为了 $O(1)$ 询问，我们可以维护各种前缀和．

然而在有修改的情况下，不方便维护，只能维护单个块内的前缀和．

以及整块作为一个单位的前缀和．

每次修改 $O(T+\frac{n}{T})$．

询问：涉及三部分，每部分都可以直接通过前缀和得到，时间复杂度 $O(1)$．

## 对询问分块

同样的问题，现在序列长度为 $n$，有 $m$ 个操作．

如果操作数量比较少，我们可以把操作记下来，在询问的时候加上这些操作的影响．

假设最多记录 $T$ 个操作，则修改 $O(1)$，询问 $O(T)$．

$T$ 个操作之后，重新计算前缀和，$O(n)$．

总复杂度：$O(mT+n\frac{m}{T})$．

$T=\sqrt{n}$ 时，总复杂度 $O(m \sqrt{n})$．

### 其他问题

分块思想也可以应用于其他整数相关问题：寻找零元素的数量、寻找第一个非零元素、计算满足某个性质的元素个数等等．

还有一些问题可以通过分块来解决，例如维护一组允许添加或删除数字的集合，检查一个数是否属于这个集合，以及查找第 $k$ 大的数．要解决这个问题，必须将数字按递增顺序存储，并分割成多个块，每个块中包含 $\sqrt{n}$ 个数字．每次添加或删除一个数字时，必须通过在相邻块的边界移动数字来重新分块．

一种很有名的离线算法 [莫队算法](../misc/mo-algo.md)，也是基于分块思想实现的．

## 练习题

-   [UVa - 12003 - Array Transformer](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=3154)
-   [UVa - 11990 Dynamic Inversion](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=3141)
-   [SPOJ - Give Away](http://www.spoj.com/problems/GIVEAWAY/)
-   [Codeforces - Till I Collapse](http://codeforces.com/contest/786/problem/C)
-   [Codeforces - Destiny](http://codeforces.com/contest/840/problem/D)
-   [Codeforces - Holes](http://codeforces.com/contest/13/problem/E)
-   [Codeforces - XOR and Favorite Number](https://codeforces.com/problemset/problem/617/E)
-   [Codeforces - Powerful array](http://codeforces.com/problemset/problem/86/D)
-   [SPOJ - DQUERY](https://www.spoj.com/problems/DQUERY)

    **本页面主要译自博文 [Sqrt-декомпозиция](http://e-maxx.ru/algo/sqrt_decomposition) 与其英文翻译版 [Sqrt Decomposition](https://cp-algorithms.com/data_structures/sqrt_decomposition.html)．其中俄文版版权协议为 Public Domain + Leave a Link；英文版版权协议为 CC-BY-SA 4.0．**


## ds/divide-combine.md

## 关于段的问题

我们由一个小清新的问题引入：

> 对于一个 $1-n$ 的排列，我们称一个值域连续的区间为段．问一个排列的段的个数．比如，$\{5 ,3 ,4, 1 ,2\}$ 的段有：$[1,1],[2,2],[3,3],[4,4],[5,5],[2,3],[4,5],[1,3],[2,5],[1,5]$．

看到这个东西，感觉要维护区间的值域集合，复杂度好像挺不友好的．线段树可以查询某个区间是否为段，但不太能统计段的个数．

这里我们引入这个神奇的数据结构——析合树！

## 连续段

在介绍析合树之前，我们先做一些前提条件的限定．鉴于 LCA 的课件中给出的定义不易理解，为方便读者理解，这里给出一些不太严谨（但更容易理解）的定义．

### 排列与连续段

**排列**：定义一个 $n$ 阶排列 $P$ 是一个大小为 $n$ 的序列，使得 $P_i$ 取遍 $1,2,\cdots,n$．说得形式化一点，$n$ 阶排列 $P$ 是一个有序集合满足：

1.  $|P|=n$.
2.  $\forall i,P_i\in[1,n]$.
3.  $\nexists i,j\in[1,n],P_i=P_j$.

    **连续段**：对于排列 $P$，定义连续段 $(P,[l,r])$ 表示一个区间 $[l,r]$，要求 $P_{l\sim r}$ 值域是连续的．说得更形式化一点，对于排列 $P$，连续段表示一个区间 $[l,r]$ 满足：

$$
(\nexists\ x,z\in[l,r],y\notin[l,r],\ P_x<P_y<P_z)
$$

特别地，当 $l>r$ 时，我们认为这是一个空的连续段，记作 $(P,\varnothing)$．

我们称排列 $P$ 的所有连续段的集合为 $I_P$，并且我们认为 $(P,\varnothing)\in I_P$．

### 连续段的运算

连续段是依赖区间和值域定义的，于是我们可以定义连续段的交并差的运算．

定义 $A=(P,[a,b]),B=(P,[x,y])$，且 $A,B\in I_P$．于是连续段的关系和运算可以表示为：

1.  $A\subseteq B\iff x\le a\wedge b\le y$.
2.  $A=B\iff a=x\wedge b=y$.
3.  $A\cap B=(P,[\max(a,x),\min(b,y)])$.
4.  $A\cup B=(P,[\min(a,x),\max(b,y)])$.
5.  $A\setminus B=(P,\{i|i\in[a,b]\wedge i\notin[x,y]\})$.

其实这些运算就是普通的集合交并差放在区间上而已．

### 连续段的性质

连续段的一些显而易见的性质．我们定义 $A,B\in I_P,A \cap B \neq \varnothing,A \notin B,B \notin A$，那么有 $A\cup B,A\cap B,A\setminus B,B\setminus A\in I_P$．

证明？证明的本质就是集合的交并差的运算．

## 析合树

好的，现在讲到重点了．你可能已经猜到了，析合树正是由连续段组成的一棵树．但是要知道一个排列可能有多达 $O(n^2)$ 个连续段，因此我们就要抽出其中更基本的连续段组成析合树．

### 本原段

其实这个定义全称叫作 **本原连续段**．但笔者认为本原段更为简洁．

对于排列 $P$，我们认为一个本原段 $M$ 表示在集合 $I_P$ 中，不存在与之相交且不包含的连续段．形式化地定义，我们认为 $X\in I_P$ 且满足 $\forall A\in I_P,\ X\cap A= (P,\varnothing)\vee X\subseteq A\vee A\subseteq X$．

所有本原段的集合为 $M_P$. 显而易见，$(P,\varnothing)\in M_P$．

显然，本原段之间只有相离或者包含关系．并且你发现 **一个连续段可以由几个互不相交的本原段构成**．最大的本原段就是整个排列本身，它包含了其他所有本原段，因此我们认为本原段可以构成一个树形结构，我们称这个结构为 **析合树**．更严格地说，排列 $P$ 的析合树由排列 $P$ 的 **所有本原段** 组成．

前面干讲这么多的定义，不来点图怎么行．考虑排列 $P=\{9,1,10,3,2,5,7,6,8,4\}$. 它的本原段构成的析合树如下：

![p1](./images/div-com1.png)

在图中我们没有标明本原段．而图中 **每个结点都代表一个本原段**．我们只标明了每个本原段的值域．举个例子，结点 $[5,8]$ 代表的本原段就是 $(P,[6,9])=\{5,7,6,8\}$．于是这里就有一个问题：**什么是析点合点？**

### 析点与合点

这里我们直接给出定义，稍候再来讨论它的正确性．

1.  **值域区间**：对于一个结点 $u$，用 $[u_l,u_r]$ 表示该结点的值域区间．
2.  **儿子序列**：对于析合树上的一个结点 $u$，假设它的儿子结点是一个 **有序** 序列，该序列是以值域区间为元素的（单个的数 $x$ 可以理解为 $[x,x]$ 的区间）．我们把这个序列称为儿子序列．记作 $S_u$．
3.  **儿子排列**：对于一个儿子序列 $S_u$，把它的元素离散化成正整数后形成的排列称为儿子排列．举个例子，对于结点 $[5,8]$，它的儿子序列为 $\{[5,5],[6,7],[8,8]\}$，那么把区间排序标个号，则它的儿子排列就为 $\{1,2,3\}$；类似的，结点 $[4,8]$ 的儿子排列为 $\{2,1\}$．结点 $u$ 的儿子排列记为 $P_u$．
4.  **合点**：我们认为，儿子排列为顺序或者逆序的点为合点．形式化地说，满足 $P_u=\{1,2,\cdots,|S_u|\}$ 或者 $P_u=\{|S_u|,|S_u-1|,\cdots,1\}$ 的点称为合点．**叶子结点没有儿子排列，我们也认为它是合点**．
5.  **析点**：不是合点的就是析点．

从图中可以看到，只有 $[1,10]$ 不是合点．因为 $[1,10]$ 的儿子排列是 $\{3,1,4,2\}$．

### 析点与合点的性质

析点与合点的命名来源于他们的性质．首先我们有一个非常显然的性质：对于析合树中任何的结点 $u$，其儿子序列区间的并集就是结点 $u$ 的值域区间．即 $\bigcup_{i=1}^{|S_u|}S_u[i]=[u_l,u_r]$．

对于一个合点 $u$：其儿子序列的任意 **子区间** 都构成一个 **连续段**．形式化地说，$\forall S_u[l\sim r]$，有 $\bigcup_{i=l}^rS_u[i]\in I_P$．

对于一个析点 $u$：其儿子序列的任意 **长度大于 1（这里的长度是指儿子序列中的元素数，不是下标区间的长度）** 的子区间都 **不** 构成一个 **连续段**．形式化地说，$\forall S_u[l\sim r],l<r$，有 $\bigcup_{i=l}^rS_u[i]\notin I_P$．

合点的性质不难证明．因为合点的儿子排列要么是顺序，要么是倒序，而值域区间也是首位相接，因此只要是连续的一段子序列（区间）都是一个连续段．

对于析点的性质可能很多读者就不太能理解了：为什么 **任意** 长度大于 $1$ 的子区间都不构成连续段？

使用反证法．假设对于一个点 $u$，它的儿子序列中有一个 **最长的** 区间 $S_u[l\sim r]$ 构成了连续段．那么这个 $A=\bigcup_{i=l}^rS_u[i]\in I_P$，也就意味着 $A$ 是一个本原段！（因为 $A$ 是儿子序列中最长的，因此找不到一个与它相交又不包含的连续段）于是你就没有使用所有的本原段构成这个析合树．矛盾．

### 析合树的构造

对于具体构造析合树，LCA 提供了一种线性构造算法[^ref1]，下面给出一种比较好懂的 $O(n\log n)$ 算法．

#### 增量法

我们考虑增量法．用一个栈维护前 $i-1$ 个元素构成的析合森林．在这里需要 **着重强调**，析合森林的意思是，在任何时候，栈中结点要么是析点要么是合点．现在考虑当前结点 $P_i$．

1.  我们先判断它能否成为栈顶结点的儿子，如果能就变成栈顶的儿子，然后把栈顶取出，作为当前结点．重复上述过程直到栈空或者不能成为栈顶结点的儿子．
2.  如果不能成为栈顶的儿子，就看能不能把栈顶的若干个连续的结点都合并成一个结点（判断能否合并的方法在后面），把合并后的点，作为当前结点．
3.  重复上述过程直到不能进行为止．然后结束此次增量，直接把当前结点压栈．

接下来我们仔细解释一下．

#### 具体的策略

我们认为，如果当前点能够成为栈顶结点的儿子，那么栈顶结点是一个合点．如果是析点，那么你合并后这个析点就存在一个子连续段，不满足析点的性质．因此一定是合点．

如果无法成为栈顶结点的儿子，那么我们就看栈顶连续的若干个点能否与当前点一起合并．设 $l$ 为当前点所在区间的左端点．我们计算 $L_i$ 表示右端点下标为 $i$ 的连续段中，左端点 $< l$ 的最大值．当前结点为 $P_i$，栈顶结点记为 $t$．

1.  如果 $L_i$ 不存在，那么显然当前结点无法合并；
2.  如果 $t_l=L_i$，那么这就是两个结点合并，合并后就是一个 **合点**；
3.  否则在栈中一定存在一个点 $t'$ 的左端点 ${t'}_l=L_i$，那么一定可以从当前结点合并到 $t'$ 形成一个 **析点**；

#### 判断能否合并

最后，我们考虑如何处理 $L_i$．事实上，一个连续段 $(P,[l,r])$ 等价于区间极差与区间长度 -1 相等．即

$$
\max_{l\le i\le r}P_i-\min_{l\le i\le r}P_i=r-l
$$

而且由于 P 是一个排列，因此对于任意的区间 $[l,r]$ 都有

$$
\max_{l\le i\le r}P_i-\min_{l\le i\le r}P_i\ge r-l
$$

于是我们就维护 $\max_{l\le i\le r}P_i-\min_{l\le i\le r}P_i-(r-l)$，那么要找到一个连续段相当于查询一个最小值！

有了上述思路，不难想到这样的算法．对于增量过程中的当前的 $i$，我们维护一个数组 $Q$ 表示区间 $[j,i]$ 的极差减长度．即

$$
Q_j=\max_{j\le k\le i}P_k-\min_{j\le k\le i}P_k-(i-j),\ \ 0<j<i
$$

现在我们想知道在 $1\sim i-1$ 中是否存在一个最小的 $j$ 使得 $Q_j=0$．这等价于求 $Q_{1\sim i-1}$ 的最小值．求得最小的 $j$ 就是 $L_i$．如果没有，那么 $L_i=i$．

但是当第 $i$ 次增量结束时，我们需要快速把 $Q$ 数组更新到 i+1 的情况．原本的区间从 $[j,i]$ 变成 $[j,i+1]$，如果 $P_{i+1}>\max$ 或者 $P_{i+1}<\min$ 都会造成 $Q_j$ 发生变化．如何变化？如果 $P_{i+1}>\max$，相当于我们把 $Q_j$ 先减掉 $\max$ 再加上 $P_{i+1}$ 就完成了 $Q_j$ 的更新；$P_{i+1}<\min$ 同理，相当于 $Q_j=Q_j+\min-P_{i+1}$.

那么如果对于一个区间 $[x,y]$，满足 $P_{x\sim i},P_{x+1\sim i},P_{x+2\sim i},\cdots,P_{y\sim i}$ 的区间 $\max$ 都相同呢？你已经发现了，那么相当于我们在做一个区间加的操作；同理，当 $P_{x\sim i},P_{x+1\sim i},\cdots,P_{y\sim i}$ 的区间 $\min$ 都想同时也是一个区间加的操作．同时，$\max$ 和 $\min$ 的更新是相互独立的，因此可以各自更新．

因此我们对 $Q$ 的维护可以这样描述：

1.  找到最大的 $j$ 使得 $P_{j}>P_{i+1}$，那么显然，$P_{j+1\sim i}$ 这一段数全部小于 $P_{i+1}$，于是就需要更新 $Q_{j+1\sim i}$ 的最大值．由于 $P_{i},\max(P_i,P_{i-1}),\max(P_i,P_{i-1},P_{i-2}),\cdots,\max(P_i,P_{i-1},\cdots,P_{j+1})$ 是（非严格）单调递增的，因此可以每一段相同的 $\max$ 做相同的更新，即区间加操作．
2.  更新 $\min$ 同理．
3.  把每一个 $Q_j$ 都减 $1$．因为区间长度加 $1$．
4.  查询 $L_i$：即查询 $Q$ 的最小值的所在的 **下标**．

没错，我们可以使用线段树维护 $Q$！现在还有一个问题：怎么找到相同的一段使得他们的 $\max/\min$ 都相同？使用单调栈维护！维护两个单调栈分别表示 $\max/\min$．那么显然，栈中以相邻两个元素为端点的区间的 $\max/\min$ 是相同的，于是在维护单调栈的时候顺便更新线段树即可．

具体的维护方法见代码．

讲这么多干巴巴的想必小伙伴也听得云里雾里的，那么我们就先上图吧．长图警告！

![p2](./images/div-com2.jpg)

### 实现

最后放一个实现的代码供参考．代码转自 [大米饼的博客](https://www.cnblogs.com/Paul-Guderian/p/11020708.html)，添加了一些注释．

```cpp
#include <algorithm>
#include <cstdio>
using namespace std;
constexpr int N = 200010;

int n, m, a[N], st1[N], st2[N], tp1, tp2, rt;
int L[N], R[N], M[N], id[N], cnt, typ[N], bin[20], st[N], tp;

// 本篇代码原题应为 CERC2017 Intrinsic Interval
// a 数组即为原题中对应的排列
// st1 和 st2 分别两个单调栈，tp1、tp2 为对应的栈顶，rt 为析合树的根
// L、R 数组表示该析合树节点的左右端点，M 数组的作用在析合树构造时有提到
// id 存储的是排列中某一位置对应的节点编号，typ 用于标记析点还是合点
// st 为存储析合树节点编号的栈，tp为其栈顶
struct RMQ {  // 预处理 RMQ（Max & Min）
  int lg[N], mn[N][17], mx[N][17];

  void chkmn(int& x, int y) {
    if (x > y) x = y;
  }

  void chkmx(int& x, int y) {
    if (x < y) x = y;
  }

  void build() {
    for (int i = bin[0] = 1; i < 20; ++i) bin[i] = bin[i - 1] << 1;
    for (int i = 2; i <= n; ++i) lg[i] = lg[i >> 1] + 1;
    for (int i = 1; i <= n; ++i) mn[i][0] = mx[i][0] = a[i];
    for (int i = 1; i < 17; ++i)
      for (int j = 1; j + bin[i] - 1 <= n; ++j)
        mn[j][i] = min(mn[j][i - 1], mn[j + bin[i - 1]][i - 1]),
        mx[j][i] = max(mx[j][i - 1], mx[j + bin[i - 1]][i - 1]);
  }

  int ask_mn(int l, int r) {
    int t = lg[r - l + 1];
    return min(mn[l][t], mn[r - bin[t] + 1][t]);
  }

  int ask_mx(int l, int r) {
    int t = lg[r - l + 1];
    return max(mx[l][t], mx[r - bin[t] + 1][t]);
  }
} D;

// 维护 L_i

struct SEG {  // 线段树
#define ls (k << 1)
#define rs (k << 1 | 1)
  int mn[N << 1], ly[N << 1];  // 区间加；区间最小值

  void pushup(int k) { mn[k] = min(mn[ls], mn[rs]); }

  void mfy(int k, int v) { mn[k] += v, ly[k] += v; }

  void pushdown(int k) {
    if (ly[k]) mfy(ls, ly[k]), mfy(rs, ly[k]), ly[k] = 0;
  }

  void update(int k, int l, int r, int x, int y, int v) {
    if (l == x && r == y) {
      mfy(k, v);
      return;
    }
    pushdown(k);
    int mid = (l + r) >> 1;
    if (y <= mid)
      update(ls, l, mid, x, y, v);
    else if (x > mid)
      update(rs, mid + 1, r, x, y, v);
    else
      update(ls, l, mid, x, mid, v), update(rs, mid + 1, r, mid + 1, y, v);
    pushup(k);
  }

  int query(int k, int l, int r) {  // 询问 0 的位置
    if (l == r) return l;
    pushdown(k);
    int mid = (l + r) >> 1;
    if (!mn[ls])
      return query(ls, l, mid);
    else
      return query(rs, mid + 1, r);
    // 如果不存在 0 的位置就会自动返回当前你查询的位置
  }
} T;

int o = 1, hd[N], dep[N], fa[N][18];

struct Edge {
  int v, nt;
} E[N << 1];

void add(int u, int v) {  // 树结构加边
  E[o] = Edge{v, hd[u]};
  hd[u] = o++;
}

void dfs(int u) {
  for (int i = 1; bin[i] <= dep[u]; ++i) fa[u][i] = fa[fa[u][i - 1]][i - 1];
  for (int i = hd[u]; i; i = E[i].nt) {
    int v = E[i].v;
    dep[v] = dep[u] + 1;
    fa[v][0] = u;
    dfs(v);
  }
}

int go(int u, int d) {
  for (int i = 0; i < 18 && d; ++i)
    if (bin[i] & d) d ^= bin[i], u = fa[u][i];
  return u;
}

int lca(int u, int v) {
  if (dep[u] < dep[v]) swap(u, v);
  u = go(u, dep[u] - dep[v]);
  if (u == v) return u;
  for (int i = 17; ~i; --i)
    if (fa[u][i] != fa[v][i]) u = fa[u][i], v = fa[v][i];
  return fa[u][0];
}

// 判断当前区间是否为连续段
bool judge(int l, int r) { return D.ask_mx(l, r) - D.ask_mn(l, r) == r - l; }

// 建树
void build() {
  for (int i = 1; i <= n; ++i) {
    // 单调栈
    // 在区间 [st1[tp1-1]+1,st1[tp1]] 的最小值就是 a[st1[tp1]]
    // 现在把它出栈，意味着要把多减掉的 Min 加回来．
    // 线段树的叶结点位置 j 维护的是从 j 到当前的 i 的
    // Max{j,i}-Min{j,i}-(i-j)
    // 区间加只是一个 Tag．
    // 维护单调栈的目的是辅助线段树从 i-1 更新到 i．
    // 更新到 i 后，只需要查询全局最小值即可知道是否有解

    while (tp1 && a[i] <= a[st1[tp1]])  // 单调递增的栈，维护 Min
      T.update(1, 1, n, st1[tp1 - 1] + 1, st1[tp1], a[st1[tp1]]), tp1--;
    while (tp2 && a[i] >= a[st2[tp2]])
      T.update(1, 1, n, st2[tp2 - 1] + 1, st2[tp2], -a[st2[tp2]]), tp2--;

    T.update(1, 1, n, st1[tp1] + 1, i, -a[i]);
    st1[++tp1] = i;
    T.update(1, 1, n, st2[tp2] + 1, i, a[i]);
    st2[++tp2] = i;

    id[i] = ++cnt;
    L[cnt] = R[cnt] = i;  // 这里的 L,R 是指节点所对应区间的左右端点
    int le = T.query(1, 1, n), now = cnt;
    while (tp && L[st[tp]] >= le) {
      if (typ[st[tp]] && judge(M[st[tp]], i)) {
        // 判断是否能成为儿子，如果能就做
        R[st[tp]] = i, M[st[tp]] = L[now], add(st[tp], now), now = st[tp--];
      } else if (judge(L[st[tp]], i)) {
        typ[++cnt] = 1;  // 合点一定是被这样建出来的
        L[cnt] = L[st[tp]], R[cnt] = i, M[cnt] = L[now];
        // 这里M数组是记录节点最右面的儿子的左端点，用于上方能否成为儿子的判断
        add(cnt, st[tp--]), add(cnt, now);
        now = cnt;
      } else {
        add(++cnt, now);  // 新建一个结点，把 now 添加为儿子
        // 如果从当前结点开始不能构成连续段，就合并．
        // 直到找到一个结点能构成连续段．而且我们一定能找到这样
        // 一个结点．
        do add(cnt, st[tp--]);
        while (tp && !judge(L[st[tp]], i));
        L[cnt] = L[st[tp]], R[cnt] = i, add(cnt, st[tp--]);
        now = cnt;
      }
    }
    st[++tp] = now;  // 增量结束，把当前点压栈

    T.update(1, 1, n, 1, i, -1);  // 因为区间右端点向后移动一格，因此整体 -1
  }

  rt = st[1];  // 栈中最后剩下的点是根结点
}

// 分 lca 为析或和，这里把叶子看成析的
void query(int l, int r) {
  int x = id[l], y = id[r];
  int z = lca(x, y);
  if (typ[z] & 1)
    l = L[go(x, dep[x] - dep[z] - 1)], r = R[go(y, dep[y] - dep[z] - 1)];
  // 合点这里特判的原因是因为这个合点不一定是最小的包含l，r的连续段.
  // 因为合点所代表的区间的子区间也都是连续段，而我们只需要其中的一段就够了．
  else
    l = L[z], r = R[z];
  printf("%d %d\n", l, r);
}

int main() {
  scanf("%d", &n);
  for (int i = 1; i <= n; ++i) scanf("%d", &a[i]);
  D.build();
  build();
  dfs(rt);
  scanf("%d", &m);
  for (int i = 1; i <= m; ++i) {
    int x, y;
    scanf("%d%d", &x, &y);
    query(x, y);
  }
  return 0;
}

// 20190612
// 析合树
```

## 参考文献与链接

[大米饼的博客 -【学习笔记】析合树](https://www.cnblogs.com/Paul-Guderian/p/11020708.html)

[^ref1]: 刘承奥．简单的连续段数据结构．WC2019 营员交流．


## ds/dividing.md

author: Xarfa

## 引入

划分树是一种来解决区间第 $K$ 大的一种数据结构，其常数、理解难度都要比主席树低很多．同时，划分树紧贴「第 $K$ 大」，所以是一种基于排序的一种数据结构．

前置知识：[主席树](persistent-seg.md#主席树)

## 过程

### 建树

划分树的建树比较简单，但是相对于其他树来说比较复杂．

![](./images/dividing-1.svg)

如图，每一层都有一个看似无序的数组．其实，每一个被红色标记的数字都是 **要分配到左儿子的**．而分配的规则是什么？就是与 **这一层的中位数** 做比较，如果小于等于中位数，则分到左边，否则分到右边．但是这里要注意一下：并不是严格的 **小于等于就分到左边，否则分到右边**．因为中位数可能有相同，而且与 $N$ 的奇偶有一定关系．下面的代码展示会有一个巧妙的运用，大家可以参照代码．

我们不可能每一次都对每一层排序，这样子不说常数，就算是理论复杂度也过不去．我们想，找中位数，一次排序就够了．为什么？比如，我们求 $l,r$ 的中位数，其实就是在排完序过后的 `num[mid]`．

两个关键数组：

tree\[log(N),N]: 也就是树，要存下所有的值，空间复杂度 $O(n\log n)$．
toleft\[log(N),n]: 也就是每一层 1\~i 进入左儿子的数量，这里需要理解一下，这是一个前缀和．

???+ note "实现"
    ```pascal
    procedure Build(left,right,deep:longint); // left,right 表示区间左右端点,deep是第几层
    var
      i,mid,same,ls,rs,flag:longint; // 其中 flag 是用来平衡左右两边的数量的
    begin
      if left=right then exit; // 到底层了
      mid:=(left+right) >> 1;
      same:=mid-left+1;
      for i:=left to right do 
        if tree[deep,i]<num[mid] then
          dec(same);
      
      ls:=left; // 分配到左儿子的第一个指针
      rs:=mid+1; // 分配到右儿子的第一个指针
      for i:=left to right do
      begin
        flag:=0;
        if (tree[deep,i]<num[mid])or((tree[deep,i]=num[mid])and(same>0)) then // 分配到左边的条件
        begin
          flag:=1; tree[deep+1,ls]:=tree[deep,i]; inc(ls);
          if tree[deep,i]=num[mid] then // 平衡左右个数
            dec(same);
        end
        else
        begin
          tree[deep+1,rs]:=tree[deep,i]; inc(rs);
        end;
        toleft[deep,i]:=toleft[deep,i-1]+flag;
      end;
      Build(left,mid,deep+1); // 继续
      Build(mid+1,right,deep+1);
    end;
    ```

### 查询

那我们先扯一下主席树的内容．在用主席树求区间第 $K$ 小的时候，我们以 $K$ 为基准，向左就向左，向右要减去向左的值，在划分树中也是这样子的．

查询难理解的，在于 **区间缩小** 这种东西．下图，查询的是 $3$ 到 $7$, 那么下一层就只需要查询 $2$ 到 $3$ 了．当然，我们定义 $[\text{left},\text{right}]$ 为缩小后的区间（目标区间），$[l,r]$ 还是所在节点的区间．那为什么要标出目标区间呢？因为那是 **判定答案在左边还是右边的基准**．

![](./images/dividing-2.svg)

???+ note "实现"
    ```pascal
    function Query(left,right,k,l,r,deep:longint):longint;
    var
      mid,x,y,cnt,rx,ry:longint;
    begin
      if left=right then // 写成 l=r 也无妨,因为目标区间也一定有答案
        exit(tree[deep,left]);
      mid:=(l+r) >> 1;
      x:=toleft[deep,left-1]-toleft[deep,l-1]; // l 到 left 的去左儿子的个数
      y:=toleft[deep,right]-toleft[deep,l-1]; // l 到 right 的去左儿子的个数
      ry:=right-l-y; rx:=left-l-x; // ry 是 l 到 right 去右儿子的个数,rx 则是 l 到 left 去右儿子的个数
      cnt:=y-x; // left 到 right 左儿子的个数
      if cnt>=k then // 主席树常识啦
        Query:=Query(l+x,l+y-1,k,l,mid,deep+1) // l+x 就是缩小左边界,l+y-1 就是缩小右区间．对于上图来说,就是把节点 1 和 2 放弃了．
      else
        Query:=Query(mid+rx+1,mid+ry+1,k-cnt,mid+1,r,deep+1); // 同样是缩小区间,只不过变成了右边而已．注意要将 k 减去 cnt．
    end;
    ```

## 性质

时间复杂度 : 一次查询只需要 $O(\log n)$，$m$ 次询问，就是 $O(m\log n)$．

空间复杂度 : 只需要存储 $O(n\log n)$ 个数字．

亲测结果：主席树 :$1482 \text{ms}$、划分树 :$889 \text{ms}$．（非递归，常数比较小）

## 划分树的应用

例题：[Luogu P3157\[CQOI2011\] 动态逆序对](https://www.luogu.com.cn/problem/P3157)

> 题意简述：给定一个 $n$ 个元素的排列（$n\leq 10^5$），有 m 次询问（$m\leq 5\times 10^4$），每次删去排列中的一个数，求删去这个数之后排列的逆序对个数．

这题可以使用 CDQ 在 $\Theta(n\log^2n)$ 的时间及 $\Theta(n)$ 的空间内解决，并且 CDQ 的常数也很优秀．

如果这道题改为强制在线，则一般使用树状数组 + 主席树的树套树解法解决，时间复杂度为 $\Theta(n\log^2n)$，空间复杂度为 $\Theta(n\log^2n)$，常数略大，同样可以过此题．

而使用划分树的话就可以在 $\Theta(n\log^2n)$ 的时间及 $\Theta(n\log n)$ 的空间内在线解决本题，同时常数也比树套树解法少很多．（大致与 CDQ 相当．）

???+ warning "注意"
    为了编程实现方便，本文依照位置的中间值将大数组划分为两个小数组，即下文中的划分树相当于是归并排序的过程，而非快速排序的过程．最顶层的大数组为有序数组，最底层为原数组．

对于每一个划分树中的节点，我们称他为右节点当且仅当他在下一层会被划分到右孩子，即原数组中位置比较靠后的那些数，相似的可以定义左节点．如果在建树的过程中将最顶层排为有序的，类似于归并排序求逆序对，可以发现一个数组的逆序对个数就是在每个左节点之前的右节点的个树和．

再考虑删除操作．删除一个左节点会将整个数组的逆序对减少在他之前右结点的个数，而删除一个右节点会减少在他之后的左节点个数．那么可以考虑每次动态维护「每一个左节点之前的右结点个数」和「每一个右节点之后的左节点个数」．这可以使用树状数组简单维护．

需要注意的是，在使用树状数组维护时只能计算在划分树中同一块内的贡献，而不能跳出块．对于树状数组来说有一个较为巧妙的处理方式．

考虑划分树上每一块的下标范围肯定为 $[c\times 2^k+1,(c+1)\times 2^k]$ 的形式，列举如下（由于代码中不会涉及到划分树最底层的处理，因此只枚举到倒数第二层）：

    [0001 0010] [0011 0100] [0101 0110] [0111 1000] [1001 1010] [1011 1100] [1101 1110] [1111 10000]  lev=1
    [0001 0010 0011 0100]   [0101 0110 0111 1000]   [1001 1010 1011 1100]   [1101 1110 1111 10000]    lev=2
    [0001 0010 0011 0100 0101 0110 0111 1000]       [1001 1010 1011 1100 1101 1110 1111 10000]        lev=3
    [0001 0010 0011 0100 0101 0110 0111 1000 1001 1010 1011 1100 1101 1110 1111 10000]                lev=4

回忆一下树状数组的原理，在向上跳的时候，我们每次 `x += lowbit(x)`．如果在向上跳的时候可以保证不跳出块，就可以保证只会影响到块内元素的值．向上查询也类似．

而如果要在向上跳的同时保证不跳出块，只需要保证在跳的时候满足 $lowbit(x)<2^{lev}$ 即可．

而向下跳则是完全不同的处理方式．每一块的下标如果使用 0-index 表示的话，即为 $[c\times 2^k,(c+1)\times 2^k)$ 的形式．那么，只需将某一个下标的值右位移 k，即可得出它在哪一块中．在向下跳的时候时刻判断是否跳出块即可．

需要注意的是，按这一方法实现的树状数组会访问到的最大下标是距离 n 最近的 2 的整次幂，因此数组下标不能开 n．

由于需要在 $\log n$ 层修改，在第 $k$ 层修改的时间复杂度为 $\Theta(k)$，最终时间复杂度即为 $\Theta(n\log n+m\log^2n)$．

附代码：

```cpp
--8<-- "docs/ds/code/dividing/dividing_1.cpp"
```

## 后记

参考博文 :[传送门](https://blog.csdn.net/littlewhite520/article/details/70250722)．


## ds/dsu-complexity.md

author: orzAtalod

本部分内容转载并修改自 [时间复杂度 - 势能分析浅谈](https://www.luogu.com.cn/blog/Atalod/shi-jian-fu-za-du-shi-neng-fen-xi-qian-tan)，已取得原作者授权同意．

## 定义

### 阿克曼函数

这里，先给出 $\alpha(n)$ 的定义．为了给出这个定义，先给出 $A_k(j)$ 的定义．

定义 $A_k(j)$ 为：

$$
A_k(j)=\left\{
\begin{aligned}
&j+1& &k=0&\\
&A_{k-1}^{(j+1)}(j)& &k\geq1&
\end{aligned}
\right.
$$

即阿克曼函数．

这里，$f^i(x)$ 表示将 $f$ 连续应用在 $x$ 上 $i$ 次，即 $f^0(x)=x$，$f^i(x)=f(f^{i-1}(x))$．

再定义 $\alpha(n)$ 为使得 $A_{\alpha(n)}(1)\geq n$ 的最小整数值．注意，我们之前将它描述为 $A_{\alpha(n)}(\alpha(n))\geq n$，反正他们的增长速度都很慢，值都不超过 4．

### 基础定义

每个节点都有一个 rank．这里的 rank 不是节点个数，而是深度．节点的初始 rank 为 0，在合并的时候，如果两个节点的 rank 不同，则将 rank 小的节点合并到 rank 大的节点上，并且不更新大节点的 rank 值．否则，随机将某个节点合并到另外一个节点上，将根节点的 rank 值 +1．这里根节点的 rank 给出了该树的高度．记 x 的 rank 为 $rnk(x)$，类似的，记 x 的父节点为 $fa(x)$．我们总有 $rnk(x)+1\leq rnk(fa(x))$．

为了定义势函数，需要预先定义一个辅助函数 $level(x)$．其中，$level(x)=\max(k:rnk(fa(x))\geq A_k(rnk(x)))$．当 $rnk(x)\geq1$ 的时候，再定义一个辅助函数 $iter(x)=\max(i:rnk(fa(x))\geq A_{level(x)}^i(rnk(x))$．这些函数定义的 $x$ 都满足 $rnk(x)>0$ 且 $x$ 不是某个树的根．

上面那些定义可能让你有点头晕．再理一下，对于一个 $x$ 和 $fa(x)$，如果 $rnk(x)>0$，总是可以找到一对 $i,k$ 令 $rnk(fa(x))\geq A_k^i(rnk(x))$，而 $level(x)=\max(k)$，在这个前提下，$iter(x)=\max(i)$．$level$ 描述了 $A$ 的最大迭代级数，而 $iter$ 描述了在最大迭代级数时的最大迭代次数．

对于这两个函数，$level(x)$ 总是随着操作的进行而增加或不变，如果 $level(x)$ 不增加，$iter(x)$ 也只会增加或不变．并且，它们总是满足以下两个不等式：

$$
0\leq level(x)<\alpha(n)
$$

$$
1\leq iter(x)\leq rnk(x)
$$

考虑 $level(x)$、$iter(x)$ 和 $A_k^j$ 的定义，这些很容易被证明出来，就留给读者用于熟悉定义了．

定义势能函数 $\Phi(S)=\sum\limits_{x\in S}\Phi(x)$，其中 $S$ 表示一整个并查集，而 $x$ 为并查集中的一个节点．定义 $\Phi(x)$ 为：

$$
\Phi(x)=
\begin{cases}
\alpha(n)\times \mathit{rnk}(x)& \mathit{rnk}(x)=0\ \text{或}\ x\ \text{为某棵树的根节点}\\
(\alpha(n)-\mathit{level}(x))\times \mathit{rnk}(x)-iter(x)& \text{otherwise}
\end{cases}
$$

然后就是通过操作引起的势能变化来证明摊还时间复杂度为 $\Theta(\alpha(n))$ 啦．注意，这里我们讨论的 $union(x,y)$ 操作保证了 $x$ 和 $y$ 都是某个树的根，因此不需要额外执行 $find(x)$ 和 $find(y)$．

可以发现，势能总是个非负数．另，在开始的时候，并查集的势能为 $0$．

## 证明

### union(x,y) 操作

其花费的时间为 $\Theta(1)$，因此我们考虑其引起的势能的变化．

这里，我们假设 $rnk(x)\leq rnk(y)$，即 $x$ 被接到 $y$ 上．这样，势能增加的节点仅有 $x$（从树根变成非树根），$y$（秩可能增加）和操作前 $y$ 的子节点（父节点的秩可能增加）．我们先证明操作前 $y$ 的子节点 $c$ 的势能不可能增加，并且如果减少了，至少减少 $1$．

设操作前 $c$ 的势能为 $\Phi(c)$，操作后为 $\Phi(c')$，这里 $c$ 可以是任意一个 $rnk(c)>0$ 的非根节点，操作可以是任意操作，包括下面的 find 操作．我们分三种情况讨论．

1.  $iter(c)$ 和 $level(c)$ 并未增加．显然有 $\Phi(c)=\Phi(c')$．
2.  $iter(c)$ 增加了，$level(c)$ 并未增加．这里 $iter(c)$ 至少增加一，即 $\Phi(c')\leq \Phi(c)-1$，势能函数减少了，并且至少减少 1．
3.  $level(c)$ 增加了，$iter(c)$ 可能减少．但是由于 $0<iter(c)\leq rnk(c)$，$iter(c)$ 最多减少 $rnk(c)-1$，而 $level(c)$ 至少增加 $1$．由定义 $\Phi(c)=(\alpha(n)-level(c))\times rnk(c)-iter(c)$，可得 $\Phi(c')\leq\Phi(c)-1$．
4.  其他情况．由于 $rnk(c)$ 不变，$rnk(fa(c))$ 不减，所以不存在．

所以，势能增加的节点仅可能是 $x$ 或 $y$．而 $x$ 从树根变成了非树根，如果 $rnk(x)=0$，则一直有 $\Phi(x)=\Phi(x')=0$．否则，一定有 $\alpha(x)\times rnk(x)\geq(\alpha(n)-level(x))\times rnk(x)-iter(x)$．即，$\Phi(x')\leq \Phi(x)$．

因此，唯一势能可能增加的点就是 $y$．而 $y$ 的势能最多增加 $\alpha(n)$．因此，可得 $union$ 操作均摊后的时间复杂度为 $\Theta(\alpha(n))$．

### find(a) 操作

如果查找路径包含 $\Theta(s)$ 个节点，显然其查找的时间复杂度是 $\Theta(s)$．如果由于查找操作，没有节点的势能增加，且至少有 $s-\alpha(n)$ 个节点的势能至少减少 $1$，就可以证明 $find(a)$ 操作的时间复杂度为 $\Theta(\alpha(n))$．为了避免混淆，这里用 $a$ 作为参数，而出现的 $x$ 都是泛指某一个并查集内的结点．

首先证明没有节点的势能增加．很显然，我们在上面证明过所有非根节点的势能不增，而根节点的 $rnk$ 没有改变，所以没有节点的势能增加．

接下来证明至少有 $s-\alpha(n)$ 个节点的势能至少减少 $1$．我们上面证明过了，如果 $level(x)$ 或者 $iter(x)$ 有改变的话，它们的势能至少减少 $1$．所以，只需要证明至少有 $s-\alpha(n)$ 个节点的 $level(x)$ 或者 $iter(x)$ 有改变即可．

回忆一下非根节点势能的定义，$\Phi(x)=(\alpha(n)-level(x))\times rnk(x)-iter(x)$，而 $level(x)$ 和 $iter(x)$ 是使 $rnk(fa(x))\geq A_{level(x)}^{iter(x)}(rnk(x))$ 的最大数．

所以，如果 $root_x$ 代表 $x$ 所处的树的根节点，只需要证明 $rnk(root_x)\geq A_{level(x)}^{iter(x)+1}(rnk(x))$ 就好了．根据 $A_k^i$ 的定义，$A_{level(x)}^{iter(x)+1}(rnk(x))=A_{level(x)}(A_{level(x)}^{iter(x)}(rnk(x)))$．

注意，我们可能会用 $k(x)$ 代表 $level(x)$，$i(x)$ 代表 $iter(x)$ 以避免式子过于冗长．这里，就是 $rnk(root_x)\geq A_{k(x)}(A_{k(x)}^{i(x)}(x))$．

当你看到这的时候，可能会有一种「这啥玩意」的感觉．这意味着你可能需要多看几遍，或者跳过一些内容以后再看．

这里，我们需要一个外接的 $A_{k(x)}$，意味着我们可能需要再找一个点 $y$．令 $y$ 是搜索路径上在 $x$ 之后的满足 $k(y)=k(x)$ 的点，这里「搜索路径之后」相当于「是 $x$ 的祖先」．显然，不是每一个 $x$ 都有这样一个 $y$．很容易证明，没有这样的 $y$ 的 $x$ 不超过 $\alpha(n)+2$ 个．因为只有每个 $k$ 的最后一个 $x$ 和 $a$ 以及 $root_a$ 没有这样的 $y$．

我们再强调一遍 $fa(x)$ 指的是路径压缩 **之前**  $x$ 的父节点，路径压缩 **之后**  $x$ 的父节点一律用 $root_x$ 表示．对于每个存在 $y$ 的 $x$，总是有 $rnk(y)\geq rnk(fa(x))$．同时，我们有 $rnk(fa(x))\geq A_{k(x)}^{i(x)}(rnk(x))$．由于 $k(x)=k(y)$，我们用 $k$ 来统称，即，$rnk(fa(x))\geq A_k^{i(x)}(rnk(x))$．我们需要造一个 $A_k$ 出来，所以我们可以不关注 $iter(y)$ 的值，直接使用弱化版的 $rnk(fa(y))\geq A_k(rnk(y))$．

如果我们将不等式组合起来，神奇的事情就发生了．我们发现，$rnk(fa(y))\geq A_k^{i(x)+1}(rnk(x))$．也就是说，为了从 $rnk(x)$ 迭代到 $rnk(fa(y))$，至少可以迭代 $A_k$ 不少于 $i(x)+1$ 次而不超过 $rnk(fa(y))$．

显然，有 $rnk(root_y)\geq rnk(fa(y))$，且 $rnk(x)$ 在路径压缩时不变．因此，我们可以得到 $rnk(root_x)\geq A_k^{i(x)+1}(rnk(x))$，也就是说 $iter(x)$ 的值至少增加 1，如果 $rnk(x)$ 没有增加，一定是 $level(x)$ 增加了．

所以，$\Phi(x)$ 至少减少了 1．由于这样的 $x$ 节点至少有 $s-\alpha(n)-2$ 个，所以最后 $\Phi(S)$ 至少减少了 $s-\alpha(n)-2$，均摊后的时间复杂度即为 $\Theta(\alpha(n)+2)=\Theta(\alpha(n))$．

## 为何并查集会被卡

这个问题也就是问，如果我们不按秩合并，会有哪些性质被破坏，导致并查集的时间复杂度不能保证为 $\Theta(m\alpha(n))$．

如果我们在合并的时候，$rnk$ 较大的合并到了 $rnk$ 较小的节点上面，我们就将那个 $rnk$ 较小的节点的 $rnk$ 值设为另一个节点的 $rnk$ 值加一．这样，我们就能保证 $rnk(fa(x))\geq rnk(x)+1$，从而不会出现类似于满地 compile error 一样的性质不符合．

显然，如果这样子的话，我们破坏的就是 $union(x,y)$ 函数「y 的势能最多增加 $\alpha(n)$」这一句．

存在一个能使路径压缩并查集时间复杂度降至 $\Omega(m\log_{1+\frac{m}{n}}n)$ 的结构，定义如下：

二项树（实际上和一般的二项树不太一样），其中 j 是常数，$T_k$ 为一个 $T_{k-1}$ 加上一个 $T_{k-j}$ 作为根节点的儿子．

![二项树](./images/dsu-complexity.svg)

边界条件，$T_1$ 到 $T_j$ 都是一个单独的点．

令 $rnk(T_k)=r_k$，这里我们有 $r_k=(k-1)/j$（证明略）．每轮操作，我们将它接到一个单节点上，然后查询底部的 $j$ 个节点．也就是说，我们接到单节点上的时候，单节点的势能提高了 $(k-1)/j+1$．在 $j=\lfloor\frac{m}{n}\rfloor$，$i=\lfloor\log_{j+1}\frac{n}{2}\rfloor$，$k=ij$ 的时候，势能增加量为：

$$
\alpha(n)\times((ij-1)/j+1)=\alpha(n)\times((\lfloor\log_{\lfloor\frac{m}{n}\rfloor+1}\frac{n}{2}\rfloor\times \lfloor\frac{m}{n}\rfloor-1)/\lfloor\frac{m}{n}\rfloor+1)
$$

变换一下，去掉所有的取整符号，就可以得出，势能增加量 $\geq \alpha(n)\times(\log_{1+\frac{m}{n}}n-\frac{n}{m})$，m 次操作就是 $\Omega(m\log_{1+\frac{m}{n}}n-n)=\Omega(m\log_{1+\frac{m}{n}}n)$．

## 关于启发式合并

由于按秩合并比启发式合并难写，所以很多 dalao 会选择使用启发式合并来写并查集．具体来说，则是对每个根都维护一个 $size(x)$，每次将 $size$ 小的合并到大的上面．

所以，启发式合并会不会被卡？

首先，可以从秩参与证明的性质来说明．如果 $size$ 可以代替 $rnk$ 的地位，则可以使用启发式合并．快速总结一下，秩参与证明的性质有以下三条：

1.  每次合并，最多有一个节点的秩上升，而且最多上升 1．
2.  总有 $rnk(fa(x))\geq rnk(x)+1$．
3.  节点的秩不减．

关于第二条和第三条，$siz$ 显然满足，然而第一条不满足，如果将 $x$ 合并到 $y$ 上面，则 $siz(y)$ 会增大 $siz(x)$ 那么多．

所以，可以考虑使用 $\log_2 siz(x)$ 代替 $rnk(x)$．

关于第一条性质，由于节点的 $siz$ 最多翻倍，所以 $\log_2 siz(x)$ 最多上升 1．关于第二三条性质，结论较为显然，这里略去证明．

所以说，如果不想写按秩合并，就写启发式合并好了，时间复杂度仍旧是 $\Theta(m\alpha(n))$．


## ds/dsu.md

author: HeRaNO, JuicyMio, Xeonacid, sailordiary, ouuan, Pig-Eat-Earth

![](images/disjoint-set.svg)

## 引入

并查集是一种用于管理元素所属集合的数据结构，实现为一个森林，其中每棵树表示一个集合，树中的节点表示对应集合中的元素．

顾名思义，并查集支持两种操作：

-   合并（Unite）：合并两个元素所属集合（合并对应的树）．
-   查询（Find）：查询某个元素所属集合（查询对应的树的根节点），这可以用于判断两个元素是否属于同一集合．

并查集在经过修改后可以支持单个元素的删除、移动或维护树上的边权．使用动态开点线段树还可以实现 [可持久化并查集](./persistent-seg.md#拓展基于主席树的可持久化并查集)．

???+ warning "Warning"
    并查集无法以较低复杂度实现集合的分离．

## 初始化

初始时，每个元素都位于一个单独的集合，表示为一棵只有根节点的树．方便起见，我们将根节点的父亲设为自己．

???+ example "实现"
    === "C++"
        ```cpp
        struct dsu {
          vector<size_t> pa;
        
          explicit dsu(size_t size) : pa(size) { iota(pa.begin(), pa.end(), 0); }
        };
        ```
    
    === "Python"
        ```python
        class Dsu:
            def __init__(self, size):
                self.pa = list(range(size))
        ```

## 查询

我们需要沿着树向上移动，直至找到根节点．

![](images/disjoint-set-find.svg)

???+ example "实现"
    === "C++"
        ```cpp
        size_t dsu::find(size_t x) { return pa[x] == x ? x : find(pa[x]); }
        ```
    
    === "Python"
        ```python
        def find(self, x):
            return x if self.pa[x] == x else self.find(self.pa[x])
        ```

### 路径压缩

查询过程中经过的每个元素都属于该集合，我们可以将其直接连到根节点以加快后续查询．

![](images/disjoint-set-compress.svg)

???+ example "实现"
    === "C++"
        ```cpp
        size_t dsu::find(size_t x) { return pa[x] == x ? x : pa[x] = find(pa[x]); }
        ```
    
    === "Python"
        ```python
        def find(self, x):
            if self.pa[x] != x:
                self.pa[x] = self.find(self.pa[x])
            return self.pa[x]
        ```

## 合并

要合并两棵树，我们只需要将一棵树的根节点连到另一棵树的根节点．

![](images/disjoint-set-merge.svg)

???+ example "实现"
    === "C++"
        ```cpp
        void dsu::unite(size_t x, size_t y) { pa[find(x)] = find(y); }
        ```
    
    === "Python"
        ```python
        def unite(self, x, y):
            self.pa[self.find(x)] = self.find(y)
        ```

### 启发式合并

合并时，选择哪棵树的根节点作为新树的根节点会影响未来操作的复杂度．我们可以将节点较少或深度较小的树连到另一棵，以免发生退化．

??? note "具体复杂度讨论"
    由于需要我们支持的只有集合的合并、查询操作，当我们需要将两个集合合二为一时，无论将哪一个集合连接到另一个集合的下面，都能得到正确的结果．但不同的连接方法存在时间复杂度的差异．具体来说，如果我们将一棵点数与深度都较小的集合树连接到一棵更大的集合树下，显然相比于另一种连接方案，接下来执行查找操作的用时更小（也会带来更优的最坏时间复杂度）．
    
    当然，我们不总能遇到恰好如上所述的集合——点数与深度都更小．鉴于点数与深度这两个特征都很容易维护，我们常常从中择一，作为估价函数．而无论选择哪一个，时间复杂度都为 $O (m\alpha(m,n))$，具体的证明可参见 References 中引用的论文．
    
    在算法竞赛的实际代码中，即便不使用启发式合并，代码也往往能够在规定时间内完成任务．在 Tarjan 的论文[^tarjan1984worst]中，证明了不使用启发式合并、只使用路径压缩的最坏时间复杂度是 $O (m \log n)$．在姚期智的论文[^yao1985expected]中，证明了不使用启发式合并、只使用路径压缩，在平均情况下，时间复杂度依然是 $O (m\alpha(m,n))$．
    
    如果只使用启发式合并，而不使用路径压缩，时间复杂度为 $O(m\log n)$．由于路径压缩单次合并可能造成大量修改，有时路径压缩并不适合使用．例如，在可持久化并查集、线段树分治 + 并查集中，一般使用只启发式合并的并查集．

按节点数合并的参考实现：（注意需要调整初始化方法）

???+ example "实现"
    === "C++"
        ```cpp
        struct dsu {
          vector<size_t> pa, size;
        
          explicit dsu(size_t size_) : pa(size_), size(size_, 1) {
            iota(pa.begin(), pa.end(), 0);
          }
        
          void unite(size_t x, size_t y) {
            x = find(x), y = find(y);
            if (x == y) return;
            if (size[x] < size[y]) swap(x, y);
            pa[y] = x;
            size[x] += size[y];
          }
        };
        ```
    
    === "Python"
        ```python
        class Dsu:
            def __init__(self, size):
                self.pa = list(range(size))
                self.size = [1] * size
        
            def unite(self, x, y):
                x, y = self.find(x), self.find(y)
                if x == y:
                    return
                if self.size[x] < self.size[y]:
                    x, y = y, x
                self.pa[y] = x
                self.size[x] += self.size[y]
        ```

## 参考实现

带有路径压缩、按节点数合并的并查集的完整实现如下所示：

??? example "模板题 [Luogu P3367【模板】并查集](https://www.luogu.com.cn/problem/P3367) 参考实现"
    === "C++"
        ```cpp
        --8<-- "docs/ds/code/dsu/dsu_0.cpp"
        ```
    
    === "Python"
        ```python
        --8<-- "docs/ds/code/dsu/dsu_0.py"
        ```

## 复杂度

同时使用路径压缩和启发式合并之后，并查集的每个操作平均时间仅为 $O(\alpha(n))$．其中，$\alpha$ 为阿克曼函数的反函数，增长极其缓慢．也就是说，并查集单次操作的平均运行时间可以认为是一个很小的常数．时间复杂度的证明在 [这个页面](./dsu-complexity.md) 中．

???+ info "反 Ackermann 函数"
    [Ackermann 函数](https://en.wikipedia.org/wiki/Ackermann_function)  $A(m, n)$ 的定义是这样的：
    
    $A(m, n) = \begin{cases}n+1&\text{if }m=0\\A(m-1,1)&\text{if }m>0\text{ and }n=0\\A(m-1,A(m,n-1))&\text{otherwise}\end{cases}$
    
    而反 Ackermann 函数 $\alpha(n)$ 的定义是 Ackermann 函数的反函数，即为最大的整数 $m$ 使得 $A(m, m) \leqslant n$．

并查集的空间复杂度显然为 $O(n)$．

## 拓展操作

在普通的并查集的基础上，还可以做一系列修改使之支持更多的操作或维护更复杂的信息．

### 带删除并查集

普通的并查集无法支持删除操作，是因为删除一个节点的时候，不可避免地会将以它为根的子树上所有节点都删除．为了解决这一问题，在带删除操作的并查集中，可以通过建立虚点的方法保证所有实际存储数据的节点总是叶子节点．为此，需要在初始化时，就为每个数据节点都建立一个虚点，并将数据节点的父节点设置为该虚点．由于每次合并两个集合时，都只会将两个集合的树根连接，所以，从始至终只有虚点会有子节点．这就保证了删除一个节点时，不会误删其他节点．

注意，删除单个节点后，需要重新为该节点建立一个虚点作为其父节点；否则，无法正确执行后续的合并和删除操作．

??? example "模板题 [SPOJ JMFILTER - Junk-Mail Filter](https://www.spoj.com/problems/JMFILTER/) 参考实现"
    === "C++"
        ```cpp
        --8<-- "docs/ds/code/dsu/dsu_4.cpp"
        ```
    
    === "Python"
        ```python
        --8<-- "docs/ds/code/dsu/dsu_4.py"
        ```

类似的方法还可以用于实现在集合间移动单个元素．实现细节详见例题．

### 带权并查集

我们还可以在并查集的边上定义某种权值和这种权值在路径压缩时产生的运算，从而解决更多的问题．比如对于经典的「NOI2001」食物链，我们可以在边权上维护模 $3$ 意义下的加法群．对于这类维护模意义下边权且模数很小的问题，还可以通过将并查集的单个点拆分为多个状态的方式来解决．这种特殊情形下的技巧，也称为「种类并查集」或「拓展域并查集」．后文会通过例题来说明这些做法．

为了维护并查集中的边权，需要将边权下放到子节点中存储．因此，每个节点存储的都是它到它的父节点之间的边权．只有当一个节点的父节点发生变化时，才需要相应地调整边权．一般情形中，这可能发生在路径压缩和合并两个节点时．例如，如果边权是当前节点与父节点之间的距离，那么，在路径压缩时，每次将当前节点的父节点替换为根节点，都需要将父节点到根节点的距离加到当前节点存储的边权上；类似地，在合并两个节点所在集合时，需要计算两个根节点之间新连接的边的权值．

??? example "模板题 [Library Checker - Unionfind with Potential](https://judge.yosupo.jp/problem/unionfind_with_potential) 参考实现"
    === "C++"
        ```cpp
        --8<-- "docs/ds/code/dsu/dsu_5.cpp"
        ```
    
    === "Python"
        ```python
        --8<-- "docs/ds/code/dsu/dsu_5.py"
        ```

## 例题

算法竞赛中，直接考察并查集的题目大多都需要针对题目设计特殊的结构．

???+ example "[UVa11987 Almost Union-Find](https://onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&category=229&page=show_problem&problem=3138)"
    实现类似并查集的数据结构，支持以下操作：
    
    1.  合并两个元素所属集合．
    2.  将单个元素移动到另一个元素所在的集合．
    3.  查询某个元素所属集合的大小及元素和．

??? note "解答"
    这道题目中，操作 1 和操作 3 都容易处理，难点在于操作 2．假定要将元素 $x$ 移动到元素 $y$ 所在的集合．在普通的并查集中，直接将元素 $x$ 的父亲设为元素 $y$ 所在集合的根节点是不行的，因为这样会将元素 $x$ 所在子树的元素都一起移动．针对这个问题，解决方法就是保证元素 $x$ 没有子节点．为此，在建立并查集时为每个元素 $x$ 都建立一个虚点 $\tilde x$，并将元素 $x$ 的父亲指向对应的虚点 $\tilde x$．这样，在合并两个集合的时候，因为总是将一个树根连接到另一个树根，而树根又全部是虚点，所以，只有虚点会有子节点，而所有实际存储元素的点都没有子节点．此时，要移动元素，就容易实现得多．

??? note "参考实现"
    === "C++"
        ```cpp
        --8<-- "docs/ds/code/dsu/dsu_1.cpp"
        ```
    
    === "Python"
        ```python
        --8<-- "docs/ds/code/dsu/dsu_1.py"
        ```

???+ example "[Luogu P2024「NOI2011」食物链](https://www.luogu.com.cn/problem/P2024)"
    动物王国中有三类动物 $A,B,C$，这三类动物的食物链构成了有趣的环形．$A$ 吃 $B$，$B$ 吃 $C$，$C$ 吃 $A$．
    
    现有 $N$ 个动物，以 $1 \sim N$ 编号．每个动物都是 $A,B,C$ 中的一种，但是我们并不知道它到底是哪一种．
    
    有人用两种说法对这 $N$ 个动物所构成的食物链关系进行描述：
    
    -   第一种说法是 `1 X Y`，表示 $X$ 和 $Y$ 是同类．
    -   第二种说法是 `2 X Y`，表示 $X$ 吃 $Y$．
    
    此人对 $N$ 个动物，用上述两种说法，一句接一句地说出 $K$ 句话，这 $K$ 句话有的是真的，有的是假的．当一句话满足下列三条之一时，这句话就是假话，否则就是真话．
    
    -   当前的话与前面的某些真的话冲突，就是假话；
    -   当前的话中 $X$ 或 $Y$ 比 $N$ 大，就是假话；
    -   当前的话表示 $X$ 吃 $X$，就是假话．
    
    你的任务是根据给定的 $N$ 和 $K$ 句话，输出假话的总数．

??? note "解答一"
    考虑用带权并查集维护食物链信息．如果 $x$ 和 $y$ 是同类，那么 $x\equiv y\pmod 3$；如果 $x$ 吃 $y$，那么 $x - y \equiv 1 \pmod 3$．这样就将本题转化为前文的模板题．
    
    具体地，对于每一句话，除去那些 $x>n$ 或 $y>n$ 的显然的假话外，需要判断 $x$ 和 $y$ 是否已经连接：如果已经连接，计算两者的模意义下的距离，并与这句话声称的信息进行比较；否则，将两者按照这句话提供的信息连接．除了显然的情形外，一句话是假话，当且仅当提到的两个节点已经连接，且对应的距离与这句话声称的信息矛盾．

??? note "参考实现一"
    === "C++"
        ```cpp
        --8<-- "docs/ds/code/dsu/dsu_6.cpp"
        ```
    
    === "Python"
        ```python
        --8<-- "docs/ds/code/dsu/dsu_6.py"
        ```

??? note "解答二"
    将一种生物 $x$ 拆分为三种状态．在具体实现中，我们可以直接将不同的状态当作不同的元素：
    
    -   与 $x$ 处于同一集合的状态与 $x$ 属于同一物种；
    -   与 $x+n$ 处于同一集合的状态能被 $x$ 吃；
    -   与 $x+2n$ 处于同一集合的能吃 $x$．
    
    于是，对于一句话：
    
    -   `1 x y` 为假话当且仅当：
    
        1.  $x>N$ 或 $y>N$；
        2.  $y$ 与 $x+n$ 或 $x+2n$ 中的一个处于同一集合内．
    -   `2 x y` 为假话当且仅当：
    
        1.  $x>N$ 或 $y>N$；
        2.  $y$ 与 $x$ 或 $x+2n$ 中的一个处于同一集合内．
    -   若为真话，合并对应状态．

??? note "参考实现二"
    === "C++"
        ```cpp
        --8<-- "docs/ds/code/dsu/dsu_2.cpp"
        ```
    
    === "Python"
        ```python
        --8<-- "docs/ds/code/dsu/dsu_2.py"
        ```

???+ example "[ABC396E Min of Restricted Sum](https://atcoder.jp/contests/abc396/tasks/abc396_e)"
    给定整数 $N, M$ 和长度为 $M$ 的整数序列 $X=(X_1,X_2,\ldots,X_M)$、$Y=(Y_1,Y_2,\ldots,Y_M)$、$Z=(Z_1,Z_2,\ldots,Z_M)$．其中，保证 $X$ 和 $Y$ 的所有元素均在 $1$ 至 $N$ 的范围内．
    
    定义长度为 $N$ 的非负整数序列 $A=(A_1,A_2,\ldots,A_N)$ 为 **好的整数序列**，当且仅当满足以下条件：
    
    -   对于所有满足 $1 \leq i \leq M$ 的整数 $i$，有 $A_{X_i} \oplus A_{Y_i} = Z_i$，其中 $\oplus$ 表示异或运算．
    
    请判断是否存在这样的好的整数序列．若存在，请找出使得元素总和 $\displaystyle \sum_{i=1}^N A_i$ 最小的好的整数序列，并输出该序列．

??? note "解答"
    异或就是单个二进制位上的「相同」或「不同」关系．那么，将 $A_i$ 的所有二进制位拆开，异或关系就能用带权并查集（或种类并查集）维护了．同一个连通块内的元素一定对应着 $A$ 中不同数字的同一个数位．统计答案时，同一连通块的元素通常分为两组，两组之间取值应当不同，只需要取其中较大的一组赋值为 $0$，另一组赋值为 $1$ 即可保证总权值最小．

??? note "参考实现"
    === "C++"
        ```cpp
        --8<-- "docs/ds/code/dsu/dsu_3.cpp"
        ```
    
    === "Python"
        ```python
        --8<-- "docs/ds/code/dsu/dsu_3.py"
        ```

## 习题

-   [「NOI2015」程序自动分析](https://uoj.ac/problem/127)
-   [「JSOI2008」星球大战](https://www.luogu.com.cn/problem/P1197)
-   [「NOIP2023」三值逻辑](https://www.luogu.com.cn/problem/P9869)
-   [「NOI2002」银河英雄传说](https://www.luogu.com.cn/problem/P1196)

## 其他应用

[最小生成树算法](../graph/mst.md) 中的 Kruskal 和 [最近公共祖先](../graph/lca.md) 中的 Tarjan 算法是基于并查集的算法．

相关专题见 [并查集应用](../topic/dsu-app.md)．

## 参考资料与拓展阅读

1.  [知乎回答：是否在并查集中真的有二分路径压缩优化？](https://www.zhihu.com/question/28410263/answer/40966441)
2.  Gabow, H. N., & Tarjan, R. E. (1985). A Linear-Time Algorithm for a Special Case of Disjoint Set Union. JOURNAL OF COMPUTER AND SYSTEM SCIENCES, 30, 209-221.[PDF](https://dl.acm.org/doi/pdf/10.1145/800061.808753)
3.  [CSDN：扩展域并查集 & 带权并查集](https://blog.csdn.net/qqqqqwerttwtwe/article/details/145440100)

[^tarjan1984worst]: Tarjan, R. E., & Van Leeuwen, J. (1984). Worst-case analysis of set union algorithms. Journal of the ACM (JACM), 31(2), 245-281.[ResearchGate PDF](https://www.researchgate.net/profile/Jan_Van_Leeuwen2/publication/220430653_Worst-case_Analysis_of_Set_Union_Algorithms/links/0a85e53cd28bfdf5eb000000/Worst-case-Analysis-of-Set-Union-Algorithms.pdf)

[^yao1985expected]: Yao, A. C. (1985). On the expected performance of path compression algorithms.[SIAM Journal on Computing, 14(1), 129-133.](https://epubs.siam.org/doi/abs/10.1137/0214010?journalCode=smjcat)


## ds/ett.md

author: Backl1ght

Euler Tour Tree（欧拉游览树，欧拉回路树，后文简称 ETT）是一种可以解决 **动态树** 问题的数据结构．ETT 将动态树的操作转换成了其 DFS 序列上的区间操作，再用其他数据结构来维护序列的区间操作，从而维护动态树的操作．例如，ETT 将动态树的加边操作转换成了多个序列拆分操作和序列合并操作，如果能维护序列拆分操作和序列合并操作，就能维护动态树的加边操作．

LCT 也是一种可以解决动态树问题的数据结构，相比 ETT 而言 LCT 会更加常见．LCT 其实更适用于维护树链的信息，而 ETT 更加适用于维护 **子树** 的信息．例如，ETT 可以维护子树最小值而 LCT 不能．

ETT 可以使用任意数据结构维护，只需要该数据结构支持对应的序列区间操作，以及在复杂度上满足要求．一般情况下会使用例如 Splay，Treap 等平衡二叉搜索树来维护序列，而这些数据结构维护区间操作的复杂度均为 $O(\log n)$，由此也可以在 $O(\log n)$ 的时间内维护动态树的操作．如果使用多叉平衡搜索树例如 B 树来维护区间操作，也可以做到更优的复杂度．

其实 ETT 可以理解为一种思想，就是通过维护某种和原树一一对应的序列，从而达到维护原树的目的，本文介绍的只是这个思想的一些可行的实现和应用．

## 树的欧拉回路表示

如果把一条树边看成两条有向边的话，那么就可以把一棵树表示成一个有向图的欧拉回路，称为树的欧拉回路表示（Euler tour representation，ETR）．

后面要维护的序列其实是 ETR 的一个变种，把树中的点看成了自环也加到了 ETR 中，但是由于原始论文中作者没有给它起新的名字，就还是叫它 ETR 吧．

可以通过下述算法得到树 $T$ 的 欧拉回路表示：

$$
\begin{array}{ll}
1 & \textbf{Input. } \text{A rooted tree }T\\
2 & \textbf{Output. } \text{The dfs sequence of rooted tree }T\\
3 & \operatorname{ET}(u)\\
4 & \qquad \text{visit vertex }u\\
5 & \qquad \text{for all child } v \text{ of } u\\
6 & \qquad \qquad \text{visit directed edge } u \to v\\
7 & \qquad \qquad \operatorname{ET}(v)\\
8 & \qquad \qquad \text{visit directed edge } v \to u\\
\end{array}
$$

树 $T$ 的欧拉回路表示 $\operatorname{ETR}(T)$ 初始为空，DFS 的过程中每次访问一个节点或者一条有向边时就将其加到 $\operatorname{ETR}(T)$ 的尾部，如此便可得到 $\operatorname{ETR}(T)$．

若 $T$ 中包含 $n$ 个节点，则中包含 $2n - 2$ 条有向边，而 DFS 的过程中，每个点和每条有向边都会被访问一次，所以 $\operatorname{ETR}(T)$ 的长度为 $3n - 2$．

把点 $u$ 看成是一个自环，这样 $\operatorname{ETR}(T)$ 就可以看成有向图中的一个欧拉回路．可以在欧拉回路的某处断开，将其看成是一些边的首尾相连组成的链；也可以把这样的链在断开处重新粘起来变回欧拉回路；还可以通过新增一些边把两个这样的链拼成一个新的欧拉回路．

后文中，如未说明默认维护的序列是树的欧拉回路表示．

## ETT 的基本操作

以下 3 个操作算是 ETT 的基本操作，均可以转换成常数次序列的操作，所以这 3 个操作的复杂度和序列操作同阶．

这里给出的只是一种可行的实现，只要能用常数次序列操作把修改后对应的序列拼出来即可．

### MakeRoot(u)

即换根操作．ETT 中的换根操作被转换成了 1 个序列拆分操作和 1 个序列合并操作，也可以理解成 1 个区间平移操作．

记包含点 $u$ 的树为 $T$，当前其树根为 $r$，现在要将树根换成 $u$．树 $T$ 对应的序列为 $L$，将 $L$ 在 $(u, u)$ 处拆分成序列 $L^1$ 和 $L^2$，前者包含 $L$ 中 $(u, u)$ 之前的元素以及 $(u, u)$，后者包含剩余元素．则依次将 $L^2$ 和 $L^1$ 合并得到的序列，即为换根之后树对应的序列．

这里可以理解成对一个欧拉回路进行旋转操作，欧拉回路是一个环，旋转并不会改变欧拉回路的结构，也即不会改变树的结构，只是把点 $u$ 旋转到了根的位置而已．

### Insert(u, v)

即加边操作．ETT 中加边操作被转换成了 2 个序列拆分操作和 5 个序列合并操作．

记包含点 $u$ 的树为 $T_1$，包含点 $v$ 的树为 $T_2$，加边之后两颗树合并成了一颗树 $T$．树 $T_1$ 对应的序列为 $L_1$，树 $T_2$ 对应的序列为 $L_2$．

将 $L_1$ 在 $(u, u)$ 处拆分成序列 $L_1^1$ 和 $L_1^2$，前者包含 $L_1$ 中 $(u, u)$ 之前的元素以及 $(u, u)$，后者包含剩余元素．类似地将 $L_2$ 在 $(v, v)$ 处拆分成序列 $L_2^1$ 和 $L_2^2$．则依次将 $L_1^2, L_1^1, [(u, v)], L_2^2, L_2^1,  [(v, u)]$ 合并即可得到树 $T$ 对应的序列 $L$．

这里可以理解成两次换根操作，然后把两个欧拉回路在当前根的位置处断开，再用新加的两条有向边把两个欧拉回路拼成一个新的欧拉回路．

### Delete(u, v)

即删边操作．ETT 中删边操作被转换成了 4 个序列拆分操作以及 1 个序列合并操作．

记包含边 $(u, v)$ 和边 $(v, u)$ 的树为 $T$，其对应序列为 $L$．删边之后 $T$ 分成了两颗树．

将 $L$ 拆分成 $L_1, [(u, v)], L_2, [(v, u)], L_3$，删边形成的两颗树对应的序列分别为 $L_2$ 以及 $L_1, L_3$．注意，在序列 $L$ 中 $[(u, v)]$ 有可能出现在 $[(v, u)]$ 的后面，此时可以先交换 $u$ 和 $v$ 的值然后再操作．

这里可以理解成把一个欧拉回路从两条有向边处断开形成两条链，然后两条链自己首尾相连形成两个新的欧拉回路．

## 实现

以下以非旋 Treap 为例介绍 ETT 的实现，需要读者事先了解使用非旋 Treap 维护区间操作的相关内容．

`Split` 和 `Merge` 都是非旋 Treap 的基本操作了，这里不再赘述．

### SplitUp2(u)

假设 $u$ 所在的序列为 $L$，将 $L$ 在 $u$ 处拆分成序列 $L^1$ 和 $L^2$，前者包含 $L$ 中 $u$ 之前的元素以及 $u$，后者包含剩余元素．

如果 Treap 的每个节点额外维护自己的父亲的话，就可以实现 $O(\log n)$ 的时间内计算一个 Treap 节点对应的元素在序列中的位置，再根据位置去 `Split` 就可以实现上述功能．

也可以自底向上地拆分从而实现上述功能，这样做相比上述方法会更高效．具体就是，在从 $u$ 对应的节点往根跳的过程中，根据二叉搜索树的性质就可以确定每个节点在 $L$ 中位于 $u$ 之前还是之后，根据这点就可以计算 $u$ 在序列中的位置，也可以确定每个节点属于拆分后的哪一棵树．

```cpp
/*
 * Bottom up split treap p into 2 treaps a and b.
 *   - a: a treap containing nodes with position less than or equal to p.
 *   - b: a treap containing nodes with postion greater than p.
 *
 * In the other word, split sequence containning p into two sequences, the first
 * one contains elements before p and element p, the second one contains
 * elements after p.
 */
static std::pair<Node*, Node*> SplitUp2(Node* p) {
  Node *a = nullptr, *b = nullptr;
  b = p->right_;
  if (b) b->parent_ = nullptr;
  p->right_ = nullptr;

  bool is_p_left_child_of_parent = false;
  bool is_from_left_child = false;
  while (p) {
    Node* parent = p->parent_;

    if (parent) {
      is_p_left_child_of_parent = (parent->left_ == p);
      if (is_p_left_child_of_parent) {
        parent->left_ = nullptr;
      } else {
        parent->right_ = nullptr;
      }
      p->parent_ = nullptr;
    }

    if (!is_from_left_child) {
      a = Merge(p, a);
    } else {
      b = Merge(b, p);
    }

    is_from_left_child = is_p_left_child_of_parent;
    p->Maintain();
    p = parent;
  }

  return {a, b};
}
```

### SplitUp3(u)

假设 $u$ 所在的序列为 $L$，将 $L$ 在 $u$ 处拆分成序列 $L^1$,$u$ 和 $L^2$，前者包含 $L$ 中 $u$ 之前的元素，后者包含剩余元素．

在 `SplitUp2` 的基础上稍作修改即可．

### MakeRoot(u)

基于 `SplitUp2` 以及 `Merge` 易得．

```cpp
void MakeRoot(int u) {
  Node* vertex_u = vertices_[u];
  auto [L1, L2] = Treap::SplitUp2(vertex_u);
  Treap::Merge(L2, L1);
}
```

### Insert(u, v)

基于 `SplitUp2` 以及 `Merge` 易得．

```cpp
void Insert(int u, int v) {
  Node* vertex_u = vertices_[u];
  Node* vertex_v = vertices_[v];

  Node* edge_uv = AllocateNode(u, v);
  Node* edge_vu = AllocateNode(v, u);
  tree_edges_[u][v] = edge_uv;
  tree_edges_[v][u] = edge_vu;

  auto [L11, L12] = Treap::SplitUp2(vertex_u);
  auto [L21, L22] = Treap::SplitUp2(vertex_v);

  Node* L = L12;
  L = Treap::Merge(L, L11);
  L = Treap::Merge(L, edge_uv);
  L = Treap::Merge(L, L22);
  L = Treap::Merge(L, L21);
  L = Treap::Merge(L, edge_vu);
}
```

### Delete(u, v)

基于 `SplitUp3` 以及 `Merge` 易得．

```cpp
void Delete(int u, int v) {
  Node* edge_uv = tree_edges_[u][v];
  Node* edge_vu = tree_edges_[v][u];
  tree_edges_[u].erase(v);
  tree_edges_[v].erase(u);

  int position_uv = Treap::GetPosition(edge_uv);
  int position_vu = Treap::GetPosition(edge_vu);
  if (position_uv > position_vu) {
    std::swap(edge_uv, edge_vu);
    std::swap(position_uv, position_vu);
  }

  auto [L1, uv, _] = Treap::SplitUp3(edge_uv);
  auto [L2, vu, L3] = Treap::SplitUp3(edge_vu);
  Treap::Merge(L1, L3);

  FreeNode(edge_uv);
  FreeNode(edge_vu);
}
```

## 维护连通性

点 $u$ 和点 $v$ 连通，当且仅当两个点属于同一棵树 $T$，即 $(u, u)$ 和 $(v, v)$ 属于 $\operatorname{ETR}(T)$，这可以根据点 $u$ 和点 $v$ 对应的 Treap 节点所在的 Treap 的根是否相同判断．

### 例题 [P2147\[SDOI2008\] 洞穴勘测](https://www.luogu.com.cn/problem/P2147)

维护连通性的模板题．

??? note "参考代码"
    ```cpp
    --8<-- "docs/ds/code/ett/ett_connectivity.cpp"
    ```

## 维护子树信息

下面以子树节点数量为例进行说明．

对于 $\operatorname{ETR}(T)$ 中每一个元素，如果这个元素对应的是树中的点，则令其权值为 $1$；如果这个元素对应的是树中的边，则令其权值为 $0$．现在树 $T$ 的节点数量就可以看成 $\operatorname{ETR}(T)$ 中元素的权值和，只需要再维护序列权值和即可实现维护子树节点数量．而序列权值和的维护是非旋 Treap 的经典操作了．

类似地，可以将子树最小值等操作转化成序列最小值等平衡树经典操作然后维护．

### 例题 [LOJ #2230.「BJOI2014」大融合](https://loj.ac/p/2230)

??? note "参考代码"
    ```cpp
    --8<-- "docs/ds/code/ett/ett_subtree_size.cpp"
    ```

## 维护树链信息

可以使用一个比较常见的技巧就是借助括号序的性质将树链信息转化成区间信息，然后就可以借助数据结构维护序列从而维护树链信息了．但是这个技巧要求维护的信息满足 **可减性**．

前面介绍的动态树操作对应的序列操作可能会把括号序中的右括号移动到左括号前，所以维护树链点权和之类的信息时还需要额外注意，操作时不能改变对应左右括号的先后顺序，而这可能需要重新思考动态树操作对应的序列操作，甚至重新思考维护什么 DFS 序．

此外，ETT 很难维护树链修改．

### 例题 [「星际探索」](https://hydro.ac/p/bzoj-P3786)

这题的动态树操作只有换父亲，可以看成删边再加边，但是这样可能会改变对应括号的先后顺序．

可以把点权转成边权，维护树的括号序，换父亲操作转化成把整个子树对应的括号序列平移至父亲左括号后面．

??? note "参考代码"
    ```cpp
    --8<-- "docs/ds/code/ett/ett_1.cpp"
    ```

## 参考资料

-   Dynamic trees as search trees via euler tours, applied to the network simplex algorithm - Robert E. Tarjan
-   Randomized fully dynamic graph algorithms with polylogarithmic time per operation - Henzinger et al.


## ds/fenwick.md

author: HeRaNO, Zhoier, Ir1d, Xeonacid, wangdehu, ouuan, ranwen, ananbaobeichicun, Ycrpro, dbxxx-oi, HowieHz, y-kx-b

## 引入

树状数组是一种支持 **单点修改** 和 **区间查询** 的，代码量小的数据结构．

??? note "什么是「单点修改」和「区间查询」？"
    假设有这样一道题：
    
    已知一个数列 $a$，你需要进行下面两种操作：
    
    -   给定 $x, y$，将 $a[x]$ 自增 $y$．
    -   给定 $l, r$，求解 $a[l \ldots r]$ 的和．
    
    其中第一种操作就是「单点修改」，第二种操作就是「区间查询」．
    
    类似地，还有：「区间修改」、「单点查询」．它们分别的一个例子如下：
    
    -   区间修改：给定 $l, r, x$，将 $a[l \ldots r]$ 中的每个数都分别自增 $x$；
    -   单点查询：给定 $x$，求解 $a[x]$ 的值．
    
    注意到，区间问题一般严格强于单点问题，因为对单点的操作相当于对一个长度为 $1$ 的区间操作．

普通树状数组维护的信息及运算要满足 **结合律** 且 **可差分**，如加法（和）、乘法（积）、异或等．

-   结合律：$(x \circ y) \circ z = x \circ (y \circ z)$，其中 $\circ$ 是一个二元运算符．
-   可差分：具有逆运算的运算，即已知 $x \circ y$ 和 $x$ 可以求出 $y$．

需要注意的是：

-   模意义下的乘法若要可差分，需保证每个数都存在逆元（模数为质数时一定存在）；
-   例如 $\gcd$，$\max$ 这些信息不可差分，所以不能用普通树状数组处理，但是：
    -   使用两个树状数组可以用于处理区间最值，见 [Efficient Range Minimum Queries using Binary Indexed Trees](http://history.ioinformatics.org/oi/files/volume9.pdf#page=41)．
    -   本页面也会介绍一种支持不可差分信息查询的，$\Theta(\log^2n)$ 时间复杂度的拓展树状数组．

事实上，树状数组能解决的问题是线段树能解决的问题的子集：树状数组能做的，线段树一定能做；线段树能做的，树状数组不一定可以．然而，树状数组的代码要远比线段树短，时间效率常数也更小，因此仍有学习价值．

有时，在差分数组和辅助数组的帮助下，树状数组还可解决更强的 **区间加单点值** 和 **区间加区间和** 问题．

## 树状数组

### 初步感受

先来举个例子：我们想知道 $a[1 \ldots 7]$ 的前缀和，怎么做？

一种做法是：$a_1 + a_2 + a_3 + a_4 + a_5 + a_6 + a_7$，需要求 $7$ 个数的和．

但是如果已知三个数 $A$，$B$，$C$，$A = a[1 \ldots 4]$ 的和，$B = a[5 \ldots 6]$ 的总和，$C = a[7 \ldots 7]$ 的总和（其实就是 $a[7]$ 自己）．你会怎么算？你一定会回答：$A + B + C$，只需要求 $3$ 个数的和．

这就是树状数组能快速求解信息的原因：我们总能将一段前缀 $[1, n]$ 拆成 **不多于 $\boldsymbol{\log n}$ 段区间**，使得这 $\log n$ 段区间的信息是 **已知的**．

于是，我们只需合并这 $\log n$ 段区间的信息，就可以得到答案．相比于原来直接合并 $n$ 个信息，效率有了很大的提高．

不难发现信息必须满足结合律，否则就不能像上面这样合并了．

下面这张图展示了树状数组的工作原理：

![](./images/fenwick.svg)

最下面的八个方块代表原始数据数组 $a$．上面参差不齐的方块（与最上面的八个方块是同一个数组）代表数组 $a$ 的上级——$c$ 数组．

$c$ 数组就是用来储存原始数组 $a$ 某段区间的和的，也就是说，这些区间的信息是已知的，我们的目标就是把查询前缀拆成这些小区间．

例如，从图中可以看出：

-   $c_2$ 管辖的是 $a[1 \ldots 2]$；
-   $c_4$ 管辖的是 $a[1 \ldots 4]$；
-   $c_6$ 管辖的是 $a[5 \ldots 6]$；
-   $c_8$ 管辖的是 $a[1 \ldots 8]$；
-   剩下的 $c[x]$ 管辖的都是 $a[x]$ 自己（可以看做 $a[x \ldots x]$ 的长度为 $1$ 的小区间）．

不难发现，$c[x]$ 管辖的一定是一段右边界是 $x$ 的区间总信息．我们先不关心左边界，先来感受一下树状数组是如何查询的．

举例：计算 $a[1 \ldots 7]$ 的和．

过程：从 $c_{7}$ 开始往前跳，发现 $c_{7}$ 只管辖 $a_{7}$ 这个元素；然后找 $c_{6}$，发现 $c_{6}$ 管辖的是 $a[5 \ldots 6]$，然后跳到 $c_{4}$，发现 $c_{4}$ 管辖的是 $a[1 \ldots 4]$ 这些元素，然后再试图跳到 $c_0$，但事实上 $c_0$ 不存在，不跳了．

我们刚刚找到的 $c$ 是 $c_7, c_6, c_4$，事实上这就是 $a[1 \ldots 7]$ 拆分出的三个小区间，合并得到答案是 $c_7 + c_6 + c_4$．

举例：计算 $a[4 \ldots 7]$ 的和．

我们还是从 $c_7$ 开始跳，跳到 $c_6$ 再跳到 $c_4$．此时我们发现它管理了 $a[1 \ldots 4]$ 的和，但是我们不想要 $a[1 \ldots 3]$ 这一部分，怎么办呢？很简单，减去 $a[1 \ldots 3]$ 的和就行了．

那不妨考虑最开始，就将查询 $a[4 \ldots 7]$ 的和转化为查询 $a[1 \ldots 7]$ 的和，以及查询 $a[1 \ldots 3]$ 的和，最终将两个结果作差．

![](images/fenwick-query.svg)

### 管辖区间

那么问题来了，$c[x](x \ge 1)$ 管辖的区间到底往左延伸多少？也就是说，区间长度是多少？

树状数组中，规定 $c[x]$ 管辖的区间长度为 $2^{k}$，其中：

-   设二进制最低位为第 $0$ 位，则 $k$ 恰好为 $x$ 二进制表示中，最低位的 `1` 所在的二进制位数；
-   $2^k$（$c[x]$ 的管辖区间长度）恰好为 $x$ 二进制表示中，最低位的 `1` 以及后面所有 `0` 组成的数．

举个例子，$c_{88}$ 管辖的是哪个区间？

因为 $88_{(10)}=01011000_{(2)}$，其二进制最低位的 `1` 以及后面的 `0` 组成的二进制是 `1000`，即 $8$，所以 $c_{88}$ 管辖 $8$ 个 $a$ 数组中的元素．

因此，$c_{88}$ 代表 $a[81 \ldots 88]$ 的区间信息．

我们记 $x$ 二进制最低位 `1` 以及后面的 `0` 组成的数为 $\operatorname{lowbit}(x)$，那么 $c[x]$ 管辖的区间就是 $[x-\operatorname{lowbit}(x)+1, x]$．

???+ warning "注意"
    $\operatorname{lowbit}$ 指的不是最低位 `1` 所在的位数 $k$，而是这个 `1` 和后面所有 `0` 组成的 $2^k$．

怎么计算 `lowbit`？根据位运算知识，可以得到 `lowbit(x) = x & -x`．

??? note "lowbit 的原理"
    将 `x` 的二进制所有位全部取反，再加 1，就可以得到 `-x` 的二进制编码．例如，$6$ 的二进制编码是 `110`，全部取反后得到 `001`，加 `1` 得到 `010`．
    
    设原先 `x` 的二进制编码是 `(...)10...00`，全部取反后得到 `[...]01...11`，加 `1` 后得到 `[...]10...00`，也就是 `-x` 的二进制编码了．这里 `x` 二进制表示中第一个 `1` 是 `x` 最低位的 `1`．
    
    `(...)` 和 `[...]` 中省略号的每一位分别相反，所以 `x & -x = (...)10...00 & [...]10...00 = 10...00`，得到的结果就是 `lowbit`．

???+ note "实现"
    === "C++"
        ```cpp
        int lowbit(int x) {
          // x 的二进制中，最低位的 1 以及后面所有 0 组成的数．
          // lowbit(0b01011000) == 0b00001000
          //          ~~~~^~~~
          // lowbit(0b01110010) == 0b00000010
          //          ~~~~~~^~
          return x & -x;
        }
        ```
    
    === "Python"
        ```python
        def lowbit(x):
            """
            x 的二进制中，最低位的 1 以及后面所有 0 组成的数．
            lowbit(0b01011000) == 0b00001000
                    ~~~~~^~~
            lowbit(0b01110010) == 0b00000010
                    ~~~~~~~^~
            """
            return x & -x
        ```

### 区间查询

接下来我们来看树状数组具体的操作实现，先来看区间查询．

回顾查询 $a[4 \ldots 7]$ 的过程，我们是将它转化为两个子过程：查询 $a[1 \ldots 7]$ 和查询 $a[1 \ldots 3]$ 的和，最终作差．

其实任何一个区间查询都可以这么做：查询 $a[l \ldots r]$ 的和，就是 $a[1 \ldots r]$ 的和减去 $a[1 \ldots l - 1]$ 的和，从而把区间问题转化为前缀问题，更方便处理．

事实上，将有关 $l \ldots r$ 的区间询问转化为 $1 \ldots r$ 和 $1 \ldots l - 1$ 的前缀询问再差分，在竞赛中是一个非常常用的技巧．

那前缀查询怎么做呢？回顾下查询 $a[1 \ldots 7]$ 的过程：

> 从 $c_{7}$ 往前跳，发现 $c_{7}$ 只管辖 $a_{7}$ 这个元素；然后找 $c_{6}$，发现 $c_{6}$ 管辖的是 $a[5 \ldots 6]$，然后跳到 $c_{4}$，发现 $c_{4}$ 管辖的是 $a[1 \ldots 4]$ 这些元素，然后再试图跳到 $c_0$，但事实上 $c_0$ 不存在，不跳了．
>
> 我们刚刚找到的 $c$ 是 $c_7, c_6, c_4$，事实上这就是 $a[1 \ldots 7]$ 拆分出的三个小区间，合并一下，答案是 $c_7 + c_6 + c_4$．

观察上面的过程，每次往前跳，一定是跳到现区间的左端点的左一位，作为新区间的右端点，这样才能将前缀不重不漏地拆分．比如现在 $c_6$ 管的是 $a[5 \ldots 6]$，下一次就跳到 $5 - 1 = 4$，即访问 $c_4$．

我们可以写出查询 $a[1 \ldots x]$ 的过程：

-   从 $c[x]$ 开始往前跳，有 $c[x]$ 管辖 $a[x-\operatorname{lowbit}(x)+1 \ldots x]$；
-   令 $x \gets x - \operatorname{lowbit}(x)$，如果 $x = 0$ 说明已经跳到尽头了，终止循环；否则回到第一步．
-   将跳到的 $c$ 合并．

实现时，我们不一定要先把 $c$ 都跳出来然后一起合并，可以边跳边合并．

比如我们要维护的信息是和，直接令初始 $\mathrm{ans} = 0$，然后每跳到一个 $c[x]$ 就 $\mathrm{ans} \gets \mathrm{ans} + c[x]$，最终 $\mathrm{ans}$ 就是所有合并的结果．

???+ note "实现"
    === "C++"
        ```cpp
        int getsum(int x) {  // a[1]..a[x]的和
          int ans = 0;
          while (x > 0) {
            ans = ans + c[x];
            x = x - lowbit(x);
          }
          return ans;
        }
        ```
    
    === "Python"
        ```python
        def getsum(x):  # a[1]..a[x]的和
            ans = 0
            while x > 0:
                ans = ans + c[x]
                x = x - lowbit(x)
            return ans
        ```

### 树状数组与其树形态的性质

在讲解单点修改之前，先讲解树状数组的一些基本性质，以及其树形态来源，这有助于更好理解树状数组的单点修改．

我们约定：

-   $l(x) = x - \operatorname{lowbit}(x) + 1$．即，$l(x)$ 是 $c[x]$ 管辖范围的左端点．
-   对于任意正整数 $x$，总能将 $x$ 表示成 $s \times 2^{k + 1} + 2^k$ 的形式，其中 $\operatorname{lowbit}(x) = 2^k$．
-   下面「$c[x]$ 和 $c[y]$ 不交」指 $c[x]$ 的管辖范围和 $c[y]$ 的管辖范围不相交，即 $[l(x), x]$ 和 $[l(y), y]$ 不相交．「$c[x]$ 包含于 $c[y]$」等表述同理．

**性质 $\boldsymbol{1}$：对于 $\boldsymbol{x \le y}$，要么有 $\boldsymbol{c[x]}$ 和 $\boldsymbol{c[y]}$ 不交，要么有 $\boldsymbol{c[x]}$ 包含于 $\boldsymbol{c[y]}$．**

??? note "证明"
    证明：假设 $c[x]$ 和 $c[y]$ 相交，即 $[l(x), x]$ 和 $[l(y), y]$ 相交，则一定有 $l(y) \le x \le y$．
    
    将 $y$ 表示为 $s \times 2^{k +1} + 2^k$，则 $l(y) = s \times 2^{k + 1} + 1$．所以，$x$ 可以表示为 $s \times 2^{k +1} + b$，其中 $1 \le b \le 2^k$．
    
    不难发现 $\operatorname{lowbit}(x) = \operatorname{lowbit}(b)$．又因为 $b - \operatorname{lowbit}(b) \ge 0$，
    
    所以 $l(x) = x - \operatorname{lowbit}(x) + 1 = s \times 2^{k +1} + b - \operatorname{lowbit}(b) +1 \ge s \times 2^{k +1} + 1 = l(y)$，即 $l(y) \le l(x) \le x \le y$．
    
    所以，如果 $c[x]$ 和 $c[y]$ 相交，那么 $c[x]$ 的管辖范围一定完全包含于 $c[y]$．

**性质 $\boldsymbol{2}$：$\boldsymbol{c[x]}$ 真包含于 $\boldsymbol{c[x + \operatorname{lowbit}(x)]}$．**

??? note "证明"
    证明：设 $y = x + \operatorname{lowbit}(x)$，$x = s \times 2^{k + 1} + 2^k$，则 $y = (s + 1) \times 2^{k +1}$，$l(x) = s \times 2^{k + 1} + 1$．
    
    不难发现 $\operatorname{lowbit}(y) \ge 2^{k + 1}$，所以 $l(y) = (s + 1) \times 2^{k + 1} - \operatorname{lowbit}(y) + 1 \le s \times 2^{k +1} + 1= l(x)$，即 $l(y) \le l(x) \le x < y$．
    
    所以，$c[x]$ 真包含于 $c[x + \operatorname{lowbit}(x)]$．

**性质 $3$：对于任意 $\boldsymbol{x < y < x + \operatorname{lowbit}(x)}$，有 $\boldsymbol{c[x]}$ 和 $\boldsymbol{c[y]}$ 不交．**

??? note "证明"
    证明：设 $x = s \times 2^{k + 1} + 2^k$，则 $y = x + b = s \times 2^{k + 1} + 2^k + b$，其中 $1 \le b < 2^k$．
    
    不难发现 $\operatorname{lowbit}(y) = \operatorname{lowbit}(b)$．又因为 $b - \operatorname{lowbit}(b) \ge 0$，
    
    因此 $l(y) = y - \operatorname{lowbit}(y) + 1 = x + b - \operatorname{lowbit}(b) + 1 > x$，即 $l(x) \le x < l(y) \le y$．
    
    所以，$c[x]$ 和 $c[y]$ 不交．

有了这三条性质的铺垫，我们接下来看树状数组的树形态（请忽略 $a$ 向 $c$ 的连边）．

![](./images/fenwick.svg)

事实上，树状数组的树形态是 $x$ 向 $x + \operatorname{lowbit}(x)$ 连边得到的图，其中 $x + \operatorname{lowbit}(x)$ 是 $x$ 的父亲．

注意，在考虑树状数组的树形态时，我们不考虑树状数组大小的影响，即我们认为这是一棵无限大的树，方便分析．实际实现时，我们只需用到 $x \le n$ 的 $c[x]$，其中 $n$ 是原数组长度．

这棵树天然满足了很多美好性质，下面列举若干（设 $fa[u]$ 表示 $u$ 的直系父亲）：

-   $u < fa[u]$．
-   $u$ 大于任何一个 $u$ 的后代，小于任何一个 $u$ 的祖先．
-   点 $u$ 的 $\operatorname{lowbit}$ 严格小于 $fa[u]$ 的 $\operatorname{lowbit}$．

??? note "证明"
    设 $y = x + \operatorname{lowbit}(x)$，$x = s \times 2^{k + 1} + 2^k$，则 $y = (s + 1) \times 2^{k +1}$，不难发现 $\operatorname{lowbit}(y) \ge 2^{k + 1} > \operatorname{lowbit}(x)$，证毕．

-   点 $x$ 的高度是 $\log_2\operatorname{lowbit}(x)$，即 $x$ 二进制最低位 `1` 的位数．

??? note "高度的定义"
    点 $x$ 的高度 $h(x)$ 满足：如果 $x \bmod 2 = 1$，则 $h(x) = 0$，否则 $h(x) = \max(h(y)) + 1$，其中 $y$ 代表 $x$ 的所有儿子（此时 $x$ 至少存在一个儿子 $x - 1$）．
    
    也就是说，一个点的高度恰好比它最高的那个儿子再高 $1$．如果一个点没有儿子，它的高度是 $0$．
    
    这里引出高度这一概念，是为后面解释复杂度更方便．

-   $c[u]$ 真包含于 $c[fa[u]]$（性质 $2$）．
-   $c[u]$ 真包含于 $c[v]$，其中 $v$ 是 $u$ 的任一祖先（在上一条性质上归纳）．
-   $c[u]$ 真包含 $c[v]$，其中 $v$ 是 $u$ 的任一后代（上面那条性质 $u$，$v$ 颠倒）．
-   对于任意 $v' > u$，若 $v'$ 不是 $u$ 的祖先，则 $c[u]$ 和 $c[v']$ 不交．

??? note "证明"
    $u$ 和 $u$ 的祖先中，一定存在一个点 $v$ 使得 $v < v' < fa[v]$，根据性质 $3$ 得 $c[v']$ 不相交于 $c[v]$，而 $c[v]$ 包含 $c[u]$，因此 $c[v']$ 不交于 $c[u]$．

-   对于任意 $v < u$，如果 $v$ 不在 $u$ 的子树上，则 $c[u]$ 和 $c[v]$ 不交（上面那条性质 $u$，$v'$ 颠倒）．
-   对于任意 $v > u$，当且仅当 $v$ 是 $u$ 的祖先，$c[u]$ 真包含于 $c[v]$（上面几条性质的总结）．这就是树状数组单点修改的核心原理．
-   设 $u = s \times 2^{k + 1} + 2^k$，则其儿子数量为 $k = \log_2\operatorname{lowbit}(u)$，编号分别为 $u - 2^t(0 \le t < k)$．
    -   举例：假设 $k = 3$，$u$ 的二进制编号为 `...1000`，则 $u$ 有三个儿子，二进制编号分别为 `...0111`、`...0110`、`...0100`．

??? note "证明"
    在一个数 $x$ 的基础上减去 $2^t$，$x$ 二进制第 $t$ 位会反转，而更低的位保持不变．
    
    考虑 $u$ 的儿子 $v$，有 $v + \operatorname{lowbit}(v) = u$，即 $v = u - 2^t$ 且 $\operatorname{lowbit}(v) = 2^t$．设 $u = s \times 2^{k + 1} + 2^k$．
    
    **考虑 $\boldsymbol{0 \le t < k}$**，$u$ 的第 $t$ 位及后方均为 $0$，所以 $v = u - 2^t$ 的第 $t$ 位变为 $1$，后面仍为 $0$，**满足** $\operatorname{lowbit}(v) = 2^t$．
    
    **考虑 $\boldsymbol{t = k}$**，则 $v = u - 2^k$，$v$ 的第 $k$ 位变为 $0$，**不满足** $\operatorname{lowbit}(v) = 2^t$．
    
    **考虑 $\boldsymbol{t > k}$**，则 $v = u - 2^t$，$v$ 的第 $k$ 位是 $1$，所以 $\operatorname{lowbit}(v) = 2^k$，**不满足** $\operatorname{lowbit}(v) = 2^t$．

-   $u$ 的所有儿子对应 $c$ 的管辖区间恰好拼接成 $[l(u), u - 1]$．
    -   举例：假设 $k = 3$，$u$ 的二进制编号为 `...1000`，则 $u$ 有三个儿子，二进制编号分别为 `...0111`、`...0110`、`...0100`．
    -   `c[...0100]` 表示 `a[...0001 ~ ...0100]`．
    -   `c[...0110]` 表示 `a[...0101 ~ ...0110]`．
    -   `c[...0111]` 表示 `a[...0111 ~ ...0111]`．
    -   不难发现上面是三个管辖区间的并集恰好是 `a[...0001 ~ ...0111]`，即 $[l(u), u - 1]$．

??? note "证明"
    $u$ 的儿子总能表示成 $u - 2^t(0 \le t < k)$，不难发现，$t$ 越小，$u - 2^t$ 越大，代表的区间越靠右．我们设 $f(t) = u - 2^t$，则 $f(k - 1), f(k - 2), \ldots, f(0)$ 分别构成 $u$ 从左到右的儿子．
    
    不难发现 $\operatorname{lowbit}(f(t)) = 2^t$，所以 $l(f(t)) = u - 2^t - 2^t + 1 = u - 2^{t + 1} + 1$．
    
    考虑相邻的两个儿子 $f(t + 1)$ 和 $f(t)$．前者管辖区间的右端点是 $f(t + 1) = u - 2^{t + 1}$，后者管辖区间的左端点是 $l(f(t)) = u - 2^{t + 1} + 1$，恰好相接．
    
    考虑最左面的儿子 $f(k - 1)$，其管辖左边界 $l(f(k - 1)) = u - 2^k + 1$ 恰为 $l(u)$．
    
    考虑最右面的儿子 $f(0)$，其管辖右边界就是 $u - 1$．
    
    因此，这些儿子的管辖区间可以恰好拼成 $[l(u), u - 1]$．

### 单点修改

现在来考虑如何单点修改 $a[x]$．

我们的目标是快速正确地维护 $c$ 数组．为保证效率，我们只需遍历并修改管辖了 $a[x]$ 的所有 $c[y]$，因为其他的 $c$ 显然没有发生变化．

管辖 $a[x]$ 的 $c[y]$ 一定包含 $c[x]$（根据性质 $1$），所以 $y$ 在树状数组树形态上是 $x$ 的祖先．因此我们从 $x$ 开始不断跳父亲，直到跳得超过了原数组长度为止．

设 $n$ 表示 $a$ 的大小，不难写出单点修改 $a[x]$ 的过程：

-   初始令 $x' = x$．
-   修改 $c[x']$．
-   令 $x' \gets x' + \operatorname{lowbit}(x')$，如果 $x' > n$ 说明已经跳到尽头了，终止循环；否则回到第二步．

区间信息和单点修改的种类，共同决定 $c[x']$ 的修改方式．下面给几个例子：

-   若 $c[x']$ 维护区间和，修改种类是将 $a[x]$ 加上 $p$，则修改方式则是将所有 $c[x']$ 也加上 $p$．
-   若 $c[x']$ 维护区间积，修改种类是将 $a[x]$ 乘上 $p$，则修改方式则是将所有 $c[x']$ 也乘上 $p$．

然而，单点修改的自由性使得修改的种类和维护的信息不一定是同种运算，比如，若 $c[x']$ 维护区间和，修改种类是将 $a[x]$ 赋值为 $p$，可以考虑转化为将 $a[x]$ 加上 $p - a[x]$．如果是将 $a[x]$ 乘上 $p$，就考虑转化为 $a[x]$ 加上 $a[x] \times p - a[x]$．

下面以维护区间和，单点加为例给出实现．

???+ note "实现"
    === "C++"
        ```cpp
        void add(int x, int k) {
          while (x <= n) {  // 不能越界
            c[x] = c[x] + k;
            x = x + lowbit(x);
          }
        }
        ```
    
    === "Python"
        ```python
        def add(x, k):
            while x <= n:  # 不能越界
                c[x] = c[x] + k
                x = x + lowbit(x)
        ```

### 建树

也就是根据最开始给出的序列，将树状数组建出来（$c$ 全部预处理好）．

一般可以直接转化为 $n$ 次单点修改，时间复杂度 $\Theta(n \log n)$（复杂度分析在后面）．

比如给定序列 $a = (5, 1, 4)$ 要求建树，直接看作对 $a[1]$ 单点加 $5$，对 $a[2]$ 单点加 $1$，对 $a[3]$ 单点加 $4$ 即可．

也有 $\Theta(n)$ 的建树方法，见本页面 [$\Theta(n)$ 建树](#thetan-建树) 一节．

### 复杂度分析

空间复杂度显然 $\Theta(n)$．

时间复杂度：

-   对于区间查询操作：整个 $x \gets x - \operatorname{lowbit}(x)$ 的迭代过程，可看做将 $x$ 二进制中的所有 $1$，从低位到高位逐渐改成 $0$ 的过程，拆分出的区间数等于 $x$ 二进制中 $1$ 的数量（即 $\operatorname{popcount}(x)$）．因此，单次查询时间复杂度是 $\Theta(\log n)$；
-   对于单点修改操作：跳父亲时，访问到的高度一直严格增加，且始终有 $x \le n$．由于点 $x$ 的高度是 $\log_2\operatorname{lowbit}(x)$，所以跳到的高度不会超过 $\log_2n$，所以访问到的 $c$ 的数量是 $\log n$ 级别．因此，单次单点修改复杂度是 $\Theta(\log n)$．

## 区间加区间和

前置知识：[前缀和 & 差分](../basic/prefix-sum.md)．

该问题可以使用两个树状数组维护差分数组解决．

考虑序列 $a$ 的差分数组 $d$，其中 $d[i] = a[i] - a[i - 1]$．由于差分数组的前缀和就是原数组，所以 $a_i=\sum_{j=1}^i d_j$．

一样地，我们考虑将查询区间和通过差分转化为查询前缀和．那么考虑查询 $a[1 \ldots r]$ 的和，即 $\sum_{i=1}^{r} a_i$，进行推导：

$$
\begin{aligned}
&\sum_{i=1}^{r} a_i\\=&\sum_{i=1}^r\sum_{j=1}^i d_j
\end{aligned}
$$

观察这个式子，不难发现每个 $d_j$ 总共被加了 $r - j + 1$ 次．接着推导：

$$
\begin{aligned}
&\sum_{i=1}^r\sum_{j=1}^i d_j\\=&\sum_{i=1}^r d_i\times(r-i+1)
\\=&\sum_{i=1}^r d_i\times (r+1)-\sum_{i=1}^r d_i\times i
\end{aligned}
$$

$\sum_{i=1}^r d_i$ 并不能推出 $\sum_{i=1}^r d_i \times i$ 的值，所以要用两个树状数组分别维护 $d_i$ 和 $d_i \times i$ 的和信息．

那么怎么做区间加呢？考虑给原数组 $a[l \ldots r]$ 区间加 $x$ 给 $d$ 带来的影响．

因为差分是 $d[i] = a[i] - a[i - 1]$，

-   $a[l]$ 多了 $v$ 而 $a[l - 1]$ 不变，所以 $d[l]$ 的值多了 $v$．
-   $a[r + 1]$ 不变而 $a[r]$ 多了 $v$，所以 $d[r + 1]$ 的值少了 $v$．
-   对于不等于 $l$ 且不等于 $r+1$ 的任意 $i$，$a[i]$ 和 $a[i - 1]$ 要么都没发生变化，要么都加了 $v$，$a[i] + v - (a[i - 1] + v)$ 还是 $a[i] - a[i - 1]$，所以其它的 $d[i]$ 均不变．

那就不难想到维护方式了：对于维护 $d_i$ 的树状数组，对 $l$ 单点加 $v$，$r + 1$ 单点加 $-v$；对于维护 $d_i \times i$ 的树状数组，对 $l$ 单点加 $v \times l$，$r + 1$ 单点加 $-v \times (r + 1)$．

而更弱的问题，「区间加求单点值」，只需用树状数组维护一个差分数组 $d_i$．询问 $a[x]$ 的单点值，直接求 $d[1 \ldots x]$ 的和即可．

这里直接给出「区间加区间和」的代码：

???+ note "实现"
    === "C++"
        ```cpp
        int t1[MAXN], t2[MAXN], n;
        
        int lowbit(int x) { return x & (-x); }
        
        void add(int k, int v) {
          int v1 = k * v;
          while (k <= n) {
            t1[k] += v, t2[k] += v1;
            // 注意不能写成 t2[k] += k * v，因为 k 的值已经不是原数组的下标了
            k += lowbit(k);
          }
        }
        
        int getsum(int *t, int k) {
          int ret = 0;
          while (k) {
            ret += t[k];
            k -= lowbit(k);
          }
          return ret;
        }
        
        void add1(int l, int r, int v) {
          add(l, v), add(r + 1, -v);  // 将区间加差分为两个前缀加
        }
        
        long long getsum1(int l, int r) {
          return (r + 1ll) * getsum(t1, r) - 1ll * l * getsum(t1, l - 1) -
                 (getsum(t2, r) - getsum(t2, l - 1));
        }
        ```
    
    === "Python"
        ```python
        t1 = [0] * MAXN
        t2 = [0] * MAXN
        n = 0
        
        
        def lowbit(x):
            return x & (-x)
        
        
        def add(k, v):
            v1 = k * v
            while k <= n:
                t1[k] = t1[k] + v
                t2[k] = t2[k] + v1
                k = k + lowbit(k)
        
        
        def getsum(t, k):
            ret = 0
            while k:
                ret = ret + t[k]
                k = k - lowbit(k)
            return ret
        
        
        def add1(l, r, v):
            add(l, v)
            add(r + 1, -v)
        
        
        def getsum1(l, r):
            return (
                (r) * getsum(t1, r)
                - l * getsum(t1, l - 1)
                - (getsum(t2, r) - getsum(t2, l - 1))
            )
        ```

根据这个原理，应该可以实现「区间乘区间积」，「区间异或一个数，求区间异或值」等，只要满足维护的信息和区间操作是同种运算即可，感兴趣的读者可以自己尝试．

## 二维树状数组

### 单点修改，子矩阵查询

二维树状数组，也被称作树状数组套树状数组，用来维护二维数组上的单点修改和前缀信息问题．

与一维树状数组类似，我们用 $c(x, y)$ 表示 $a(x - \operatorname{lowbit}(x) + 1, y - \operatorname{lowbit}(y) + 1) \ldots a(x, y)$ 的矩阵总信息，即一个以 $a(x, y)$ 为右下角，高 $\operatorname{lowbit}(x)$，宽 $\operatorname{lowbit}(y)$ 的矩阵的总信息．

对于单点修改，设：

$$
f(x, i) = \begin{cases}x &i = 0\\f(x, i - 1) + \operatorname{lowbit}(f(x, i - 1)) & i > 0\\\end{cases}
$$

即 $f(x, i)$ 为 $x$ 在树状数组树形态上的第 $i$ 级祖先（第 $0$ 级祖先是自己）．

则只有 $c(f(x, i), f(y, j))$ 中的元素管辖 $a(x, y)$，修改 $a(x, y)$ 时只需修改所有 $c(f(x, i), f(y, j))$，其中 $f(x, i) \le n$，$f(y, j) \le m$．

??? note "正确性证明"
    $c(p, q)$ 管辖 $a(x, y)$，求 $p$ 和 $q$ 的取值范围．
    
    考虑一个大小为 $n$ 的一维树状数组 $c_1$（对应原数组 $a_1$）和一个大小为 $m$ 的一维树状数组 $c_2$（对应原数组 $a_2$）．
    
    则命题等价为：$c_1(p)$ 管辖 $a_1[x]$ 且 $c_2(q)$ 管辖 $a_2[y]$ 的条件．
    
    也就是说，在树状数组树形态上，$p$ 是 $x$ 及其祖先中的一个点，$q$ 是 $y$ 及其祖先中的一个点．
    
    所以 $p = f(x, i)$，$q = f(y, j)$．

对于查询，我们设：

$$
g(x, i) = \begin{cases}x &i = 0\\g(x, i - 1) - \operatorname{lowbit}(g(x, i - 1)) & i, g(x, i - 1) > 0\\0&\text{otherwise.}\end{cases}
$$

则合并所有 $c(g(x, i), g(y, j))$，其中 $g(x, i), g(y, j) > 0$．

??? note "正确性证明"
    设 $\circ$ 表示合并两个信息的运算符（比如，如果信息是区间和，则 $\circ = +$）．
    
    考虑一个一维树状数组 $c_1$，$c_1[g(x, 0)] \circ c_1[g(x, 1)] \circ c_1[g(x, 2)] \circ \cdots$ 恰好表示原数组上 $[1 \ldots x]$ 这段区间信息．
    
    类似地，设 $t(x) = c(x, g(y, 0)) \circ c(x, g(y, 1)) \circ c(x, g(y, 2)) \circ \cdots$，则 $t(x)$ 恰好表示 $a(x - \operatorname{lowbit}(x) + 1, 1) \ldots a(x, y)$ 这个矩阵信息．
    
    又类似地，就有 $t(g(x, 0)) \circ t(g(x, 1)) \circ t(g(x, 2)) \circ \cdots$ 表示 $a(1, 1) \ldots a(x, y)$ 这个矩阵信息．
    
    其实这里 $t(x)$ 这个函数如果看成一个树状数组，相当于一个树状数组套了一个树状数组，这也就是「树状数组套树状数组」这个名字的来源．

下面给出单点加、查询子矩阵和的代码．

???+ note "实现"
    === "单点加"
        ```cpp
        void add(int x, int y, int v) {
          for (int i = x; i <= n; i += lowbit(i)) {
            for (int j = y; j <= m; j += lowbit(j)) {
              // 注意这里必须得建循环变量，不能像一维数组一样直接 while (x <= n) 了
              c[i][j] += v;
            }
          }
        }
        ```
    
    === "查询子矩阵和"
        ```cpp
        int sum(int x, int y) {
          int res = 0;
          for (int i = x; i > 0; i -= lowbit(i)) {
            for (int j = y; j > 0; j -= lowbit(j)) {
              res += c[i][j];
            }
          }
          return res;
        }
        
        int ask(int x1, int y1, int x2, int y2) {
          // 查询子矩阵和
          return sum(x2, y2) - sum(x2, y1 - 1) - sum(x1 - 1, y2) + sum(x1 - 1, y1 - 1);
        }
        ```

### 子矩阵加，求子矩阵和

前置知识：[前缀和 & 差分](../basic/prefix-sum.md) 和本页面 [区间加区间和](#区间加区间和) 一节．

和一维树状数组的「区间加区间和」问题类似，考虑维护差分数组．

二维数组上的差分数组是这样的：

$$
d(i, j) = a(i, j) - a(i - 1, j) - a(i, j - 1) + a(i - 1, j - 1)．
$$

??? note "为什么这么定义？"
    这是因为，理想规定状态下，在差分矩阵上做二维前缀和应该得到原矩阵，因为这是一对逆运算．
    
    二维前缀和的公式是这样的：
    
    $s(i, j) = s(i - 1, j) + s(i, j - 1) - s(i - 1, j - 1) + a(i, j)$．
    
    所以，设 $a$ 是原数组，$d$ 是差分数组，有：
    
    $a(i, j) = a(i - 1, j) + a(i, j - 1) - a(i - 1, j - 1) + d(i, j)$
    
    移项就得到二维差分的公式了．
    
    $d(i, j) = a(i, j) - a(i - 1, j) - a(i, j - 1) + a(i - 1, j - 1)$．

这样以来，对左上角 $(x_1, y_1)$，右下角 $(x_2, y_2)$ 的子矩阵区间加 $v$，相当于在差分数组上，对 $d(x_1, y_1)$ 和 $d(x_2 + 1, y_2 + 1)$ 分别单点加 $v$，对 $d(x_2 + 1, y_1)$ 和 $d(x_1, y_2 + 1)$ 分别单点加 $-v$．

至于原因，把这四个 $d$ 分别用定义式表示出来，分析一下每项的变化即可．

举个例子吧，初始差分数组为 $0$，给 $a(2, 2) \ldots a(3, 4)$ 子矩阵加 $v$ 后差分数组会变为：

$$
\begin{pmatrix}0&0&0&0&0\\0&v&0&0&-v\\0&0&0&0&0\\0&-v&0&0&v\end{pmatrix}
$$

（其中 $a(2, 2) \ldots a(3, 4)$ 这个子矩阵恰好是上面位于中心的 $2 \times 3$ 大小的矩阵．）

因此，子矩阵加的做法是：转化为差分数组上的四个单点加操作．

现在考虑查询子矩阵和：

对于点 $(x, y)$，它的二维前缀和可以表示为：

$$
\sum_{i = 1}^x\sum_{j = 1}^y\sum_{h = 1}^i\sum_{k = 1}^j d(h, k)
$$

原因就是差分的前缀和的前缀和就是原本的前缀和．

和一维树状数组的「区间加区间和」问题类似，统计 $d(h, k)$ 的出现次数，为 $(x - h + 1) \times (y - k + 1)$．

然后接着推导：

$$
\begin{aligned}
&\sum_{i = 1}^x\sum_{j = 1}^y\sum_{h = 1}^i\sum_{k = 1}^j d(h, k)
\\=&\sum_{i = 1}^x\sum_{j = 1}^y d(i, j) \times (x - i + 1) \times (y - j + 1)
\\=&\sum_{i = 1}^x\sum_{j = 1}^y d(i, j) \times (xy + x + y + 1) - d(i, j) \times i \times (y + 1) - d(i, j) \times j \times (x + 1) + d(i, j) \times i \times j
\end{aligned}
$$

所以我们需维护四个树状数组，分别维护 $d(i, j)$，$d(i, j) \times i$，$d(i, j) \times j$，$d(i, j) \times i \times j$ 的和信息．

当然了，和一维同理，如果只需要子矩阵加求单点值，维护一个差分数组然后询问前缀和就足够了．

下面给出代码：

???+ note "实现"
    ```cpp
    using ll = long long;
    ll t1[N][N], t2[N][N], t3[N][N], t4[N][N];
    
    void add(ll x, ll y, ll z) {
      for (int X = x; X <= n; X += lowbit(X))
        for (int Y = y; Y <= m; Y += lowbit(Y)) {
          t1[X][Y] += z;
          t2[X][Y] += z * x;  // 注意是 z * x 而不是 z * X，后面同理
          t3[X][Y] += z * y;
          t4[X][Y] += z * x * y;
        }
    }
    
    void range_add(ll xa, ll ya, ll xb, ll yb,
                   ll z) {  //(xa, ya) 到 (xb, yb) 子矩阵
      add(xa, ya, z);
      add(xa, yb + 1, -z);
      add(xb + 1, ya, -z);
      add(xb + 1, yb + 1, z);
    }
    
    ll ask(ll x, ll y) {
      ll res = 0;
      for (int i = x; i; i -= lowbit(i))
        for (int j = y; j; j -= lowbit(j))
          res += (x + 1) * (y + 1) * t1[i][j] - (y + 1) * t2[i][j] -
                 (x + 1) * t3[i][j] + t4[i][j];
      return res;
    }
    
    ll range_ask(ll xa, ll ya, ll xb, ll yb) {
      return ask(xb, yb) - ask(xb, ya - 1) - ask(xa - 1, yb) + ask(xa - 1, ya - 1);
    }
    ```

## 权值树状数组及应用

我们知道，普通树状数组直接在原序列的基础上构建，$c_6$ 表示的就是 $a[5 \ldots 6]$ 的区间信息．

然而事实上，我们还可以在原序列的权值数组上构建树状数组，这就是权值树状数组．

??? note "什么是权值数组？"
    一个序列 $a$ 的权值数组 $b$，满足 $b[x]$ 的值为 $x$ 在 $a$ 中的出现次数．
    
    例如：$a = (1, 3, 4, 3, 4)$ 的权值数组为 $b = (1, 0, 2, 2)$．
    
    很明显，$b$ 的大小和 $a$ 的值域有关．
    
    若原数列值域过大，且重要的不是具体值而是值与值之间的相对大小关系，常 [离散化](../misc/discrete.md) 原数组后再建立权值数组．
    
    另外，权值数组是原数组无序性的一种表示：它重点描述数组的元素内容，忽略了数组的顺序，若两数组只是顺序不同，所含内容一致，则它们的权值数组相同．
    
    因此，对于给定数组的顺序不影响答案的问题，在权值数组的基础上思考一般更直观，比如 [\[NOIP2021\] 数列](https://www.luogu.com.cn/problem/P7961)．

运用权值树状数组，我们可以解决一些经典问题．

### 单点修改，查询全局第 $k$ 小

在此处只讨论第 $k$ 小，第 $k$ 大问题可以通过简单计算转化为第 $k$ 小问题．

该问题可离散化，如果原序列 $a$ 值域过大，离散化后再建立权值数组 $b$．注意，还要把单点修改中的涉及到的值也一起离散化，不能只离散化原数组 $a$ 中的元素．

对于单点修改，只需将对原数列的单点修改转化为对权值数组的单点修改即可．具体来说，原数组 $a[x]$ 从 $y$ 修改为 $z$，转化为对权值数组 $b$ 的单点修改就是 $b[y]$ 单点减 $1$，$b[z]$ 单点加 $1$．

对于查询第 $k$ 小，考虑二分 $x$，查询权值数组中 $[1, x]$ 的前缀和，找到 $x_0$ 使得 $[1, x_0]$ 的前缀和 $< k$ 而 $[1, x_0 + 1]$ 的前缀和 $\ge k$，则第 $k$ 大的数是 $x_0 + 1$（注：这里认为 $[1, 0]$ 的前缀和是 $0$）．

这样做时间复杂度是 $\Theta(\log^2n)$ 的．

考虑用倍增替代二分．

设 $x = 0$，$\mathrm{sum} = 0$，枚举 $i$ 从 $\log_2n$ 降为 $0$：

-   查询权值数组中 $[x + 1 \ldots x + 2^i]$ 的区间和 $t$．
-   如果 $\mathrm{sum} + t < k$，扩展成功，$x \gets x + 2^i$，$\mathrm{sum} \gets \mathrm{sum} + t$；否则扩展失败，不操作．

这样得到的 $x$ 是满足 $[1 \ldots x]$ 前缀和 $< k$ 的最大值，所以最终 $x + 1$ 就是答案．

看起来这种方法时间效率没有任何改善，但事实上，查询 $[x + 1 \ldots x + 2^i]$ 的区间和只需访问 $c[x + 2^i]$ 的值即可．

原因很简单，考虑 $\operatorname{lowbit}(x + 2^i)$，它一定是 $2^i$，因为 $x$ 之前只累加过 $2^j$ 满足 $j > i$．因此 $c[x + 2^i]$ 表示的区间就是 $[x + 1 \ldots x + 2^i]$．

如此一来，时间复杂度降低为 $\Theta(\log n)$．

???+ note "实现"
    === "C++"
        ```cpp
        // 权值树状数组查询第 k 小
        int kth(int k) {
          int sum = 0, x = 0;
          for (int i = log2(n); ~i; --i) {
            x += 1 << i;                   // 尝试扩展
            if (x > n || sum + t[x] >= k)  // 如果扩展失败
              x -= 1 << i;
            else
              sum += t[x];
          }
          return x + 1;  // 找不到就返回 n + 1
        }
        ```
    
    === "Python"
        ```python
        # 权值树状数组查询第 k 小
        def kth(k):
            sum = 0
            x = 0
            i = int(log2(n))
            while ~i:
                x = x + (1 << i)  # 尝试扩展
                if x > n or sum + t[x] >= k:  # 如果扩展失败
                    x = x - (1 << i)
                else:
                    sum = sum + t[x]
                i = i - 1
            return x + 1  # 找不到就返回 n + 1
        ```

### 全局逆序对（全局二维偏序）

相关阅读和参考实现：[逆序对](../math/permutation.md#逆序数)

全局逆序对也可以用权值树状数组巧妙解决．问题是这样的：给定长度为 $n$ 的序列 $a$，求 $a$ 中满足 $i < j$ 且 $a[i] > a[j]$ 的数对 $(i, j)$ 的数量．

该问题可离散化，如果原序列 $a$ 值域过大，离散化后再建立权值数组 $b$．

我们考虑从 $n$ 到 $1$ 倒序枚举 $i$，作为逆序对中第一个元素的索引，然后计算有多少个 $j > i$ 满足 $a[j] < a[i]$，最后累计答案即可．

事实上，我们只需要这样做（设当前 $a[i] = x$）：

-   查询 $b[1 \ldots x - 1]$ 的前缀和，即为左端点为 $a[i]$ 的逆序对数量．
-   $b[x]$ 自增 $1$；

原因十分自然：出现在 $b[1 \ldots x-1]$ 中的元素一定比当前的 $x = a[i]$ 小，而 $i$ 的倒序枚举，自然使得这些已在权值数组中的元素，在原数组上的索引 $j$ 大于当前遍历到的索引 $i$．

用例子说明，$a = (4, 3, 1, 2, 1)$．

$i$ 按照 $5 \to 1$ 扫：

-   $a[5] = 1$，查询 $b[1 \ldots 0]$ 前缀和，为 $0$，$b[1]$ 自增 $1$，$b = (1, 0, 0, 0)$．
-   $a[4] = 2$，查询 $b[1 \ldots 1]$ 前缀和，为 $1$，$b[2]$ 自增 $1$，$b = (1, 1, 0, 0)$．
-   $a[3] = 1$，查询 $b[1 \ldots 0]$ 前缀和，为 $0$，$b[1]$ 自增 $1$，$b = (2, 1, 0, 0)$．
-   $a[2] = 3$，查询 $b[1 \ldots 2]$ 前缀和，为 $3$，$b[3]$ 自增 $1$，$b = (2, 1, 1, 0)$．
-   $a[1] = 4$，查询 $b[1 \ldots 3]$ 前缀和，为 $4$，$b[4]$ 自增 $1$，$b = (2, 1, 1, 1)$．

所以最终答案为 $0 + 1 + 0 + 3 + 4 = 8$．

注意到，遍历 $i$ 后的查询 $b[1 \ldots x - 1]$ 和自增 $b[x]$ 的两个步骤可以颠倒，变成先自增 $b[x]$ 再查询 $b[1 \ldots x - 1]$，不影响答案．两个角度来解释：

-   对 $b[x]$ 的修改不影响对 $b[1 \ldots x - 1]$ 的查询．
-   颠倒后，实质是在查询 $i \le j$ 且 $a[i] > a[j]$ 的数对数量，而 $i = j$ 时不存在 $a[i] > a[j]$，所以 $i \le j$ 相当于 $i < j$，所以这与原来的逆序对问题是等价的．

如果查询非严格逆序对（$i < j$ 且 $a[i] \ge a[j]$）的数量，那就要改为查询 $b[1 \ldots x]$ 的和，这时就不能颠倒两步了，还是两个角度来解释：

-   对 $b[x]$ 的修改 **影响** 对 $b[1 \ldots x]$ 的查询．
-   颠倒后，实质是在查询 $i \le j$ 且 $a[i] \ge a[j]$ 的数对数量，而 $i = j$ 时恒有 $a[i] \ge a[j]$，所以 $i \le j$  **不相当于**  $i < j$，与原问题 **不等价**．

如果查询 $i \le j$ 且 $a[i] \ge a[j]$ 的数对数量，那这两步就需要颠倒了．

另外，对于原逆序对问题，还有一种做法是正着枚举 $j$，查询有多少 $i < j$ 满足 $a[i] > a[j]$．做法如下（设 $x = a[j]$）：

-   查询 $b[x + 1 \ldots V]$（$V$ 是 $b$ 的大小，即 $a$ 的值域（或离散化后的值域））的区间和．
-   将 $b[x]$ 自增 $1$．

原因：出现在 $b[x + 1 \ldots V]$ 中的元素一定比当前的 $x = a[j]$ 大，而 $j$ 的正序枚举，自然使得这些已在权值数组中的元素，在原数组上的索引 $i$ 小于当前遍历到的索引 $j$．

此外，逆序对的计数还可以通过 [归并排序](../basic/merge-sort.md#逆序对) 解决．这一方法可以避免离散化．时间复杂度同样为 $O(n\log n)$．两种算法的参考实现都在 [逆序对](../math/permutation.md#逆序数) 章节．

## 树状数组维护不可差分信息

比如维护区间最值等．

注意，这种方法虽然码量小，但单点修改和区间查询的时间复杂度均为 $\Theta(\log^2n)$，比使用线段树的时间复杂度 $\Theta(\log n)$ 劣．

### 区间查询

我们还是基于之前的思路，从 $r$ 沿着 $\operatorname{lowbit}$ 一直向前跳，但是我们不能跳到 $l$ 的左边．

因此，如果我们跳到了 $c[x]$，先判断下一次要跳到的 $x - \operatorname{lowbit}(x)$ 是否小于 $l$：

-   如果小于 $l$，我们直接把 **$\boldsymbol{a[x]}$ 单点** 合并到总信息里，然后跳到 $c[x - 1]$．
-   如果大于等于 $l$，说明没越界，正常合并 $c[x]$，然后跳到 $c[x - \operatorname{lowbit}(x)]$ 即可．

下面以查询区间最大值为例，给出代码：

???+ note "实现"
    ```cpp
    int getmax(int l, int r) {
      int ans = 0;
      while (r >= l) {
        ans = max(ans, a[r]);
        --r;
        for (; r - lowbit(r) >= l; r -= lowbit(r)) {
          // 注意，循环条件不要写成 r - lowbit(r) + 1 >= l
          // 否则 l = 1 时，r 跳到 0 会死循环
          ans = max(ans, C[r]);
        }
      }
      return ans;
    }
    ```

可以证明，上述算法的时间复杂度是 $\Theta(\log^2n)$．

??? note "时间复杂度证明"
    考虑 $r$ 和 $l$ 不同的最高位，一定有 $r$ 在这一位上为 $1$，$l$ 在这一位上为 $0$（因为 $r \ge l$）．
    
    如果 $r$ 在这一位的后面仍然有 $1$，一定有 $r - \operatorname{lowbit}(r) \ge l$，所以下一步一定是把 $r$ 的最低位 $1$ 填为 $0$；
    
    如果 $r$ 的这一位 $1$ 就是 $r$ 的最低位 $1$，无论是 $r \gets r - \operatorname{lowbit}(r)$ 还是 $r \gets r - 1$，$r$ 的这一位 $1$ 一定会变为 $0$．
    
    因此，$r$ 经过至多 $\log n$ 次变换后，$r$ 和 $l$ 不同的最高位一定可以下降一位．所以，总时间复杂度是 $\Theta(\log^2n)$．

### 单点更新

???+ note "注"
    请先理解树状数组树形态的以下两条性质，再学习本节．
    
    -   设 $u = s \times 2^{k + 1} + 2^k$，则其儿子数量为 $k = \log_2\operatorname{lowbit}(u)$，编号分别为 $u - 2^t(0 \le t < k)$．
    -   $u$ 的所有儿子对应 $c$ 的管辖区间恰好拼接成 $[l(u), u - 1]$．
    
    关于这两条性质的含义及证明，都可以在本页面的 [树状数组与其树形态的性质](#树状数组与其树形态的性质) 一节找到．

更新 $a[x]$ 后，我们只需要更新满足在树状数组树形态上，满足 $y$ 是 $x$ 的祖先的 $c[y]$．

对于最值（以最大值为例），一种常见的错误想法是，如果 $a[x]$ 修改成 $p$，则将所有 $c[y]$ 更新为 $\max(c[y], p)$．下面是一个反例：$(1, 2, 3, 4, 5)$ 中将 $5$ 修改成 $4$，最大值是 $4$，但按照上面的修改这样会得到 $5$．将 $c[y]$ 直接修改为 $p$ 也是错误的，一个反例是，将上面例子中的 $3$ 修改为 $4$．

事实上，对于不可差分信息，不存在通过 $p$ 直接修改 $c[y]$ 的方式．这是因为修改本身就相当于是把旧数从原区间「移除」，然后加入一个新数．「移除」时对区间信息的影响，相当于做「逆运算」，而不可差分信息不存在「逆运算」，所以无法直接修改 $c[y]$．

换句话说，对每个受影响的 $c[y]$，这个区间的信息我们必定要重构了．

考虑 $c[y]$ 的儿子们，它们的信息一定是正确的（因为我们先更新儿子再更新父亲），而这些儿子又恰好组成了 $[l(y), y - 1]$ 这一段管辖区间，那再合并一个单点 $a[y]$ 就可以合并出 $[l(y), y]$，也就是 $c[y]$ 了．这样，我们能用至多 $\log n$ 个区间重构合并出每个需要修改的 $c$．

???+ note "实现"
    ```cpp
    void update(int x, int v) {
      a[x] = v;
      for (int i = x; i <= n; i += lowbit(i)) {
        // 枚举受影响的区间
        C[i] = a[i];
        for (int j = 1; j < lowbit(i); j *= 2) {
          C[i] = max(C[i], C[i - j]);
        }
      }
    }
    ```

容易看出上述算法时间复杂度为 $\Theta(\log^2n)$．

### 建树

可以考虑拆成 $n$ 个单点修改，$\Theta(n\log^2n)$ 建树．

也有 $\Theta(n)$ 的建树方法，见本页面 [$\Theta(n)$ 建树](#thetan-建树) 一节的方法一．

## Tricks

### $\Theta(n)$ 建树

以维护区间和为例．

方法一：

每一个节点的值是由所有与自己直接相连的儿子的值求和得到的．因此可以倒着考虑贡献，即每次确定完儿子的值后，用自己的值更新自己的直接父亲．

???+ note "实现"
    === "C++"
        ```cpp
        // Θ(n) 建树
        void init() {
          for (int i = 1; i <= n; ++i) {
            t[i] += a[i];
            int j = i + lowbit(i);
            if (j <= n) t[j] += t[i];
          }
        }
        ```
    
    === "Python"
        ```python
        # Θ(n) 建树
        def init():
            for i in range(1, n + 1):
                t[i] = t[i] + a[i]
                j = i + lowbit(i)
                if j <= n:
                    t[j] = t[j] + t[i]
        ```

方法二：

前面讲到 $c[i]$ 表示的区间是 $[i-\operatorname{lowbit}(i)+1, i]$，那么我们可以先预处理一个 $\mathrm{sum}$ 前缀和数组，再计算 $c$ 数组．

???+ note "实现"
    === "C++"
        ```cpp
        // Θ(n) 建树
        void init() {
          for (int i = 1; i <= n; ++i) {
            t[i] = sum[i] - sum[i - lowbit(i)];
          }
        }
        ```
    
    === "Python"
        ```python
        # Θ(n) 建树
        def init():
            for i in range(1, n + 1):
                t[i] = sum[i] - sum[i - lowbit(i)]
        ```

### 时间戳优化

对付多组数据很常见的技巧．若每次输入新数据都暴力清空树状数组，就可能会造成超时．因此使用 $\mathrm{tag}$ 标记，存储当前节点上次使用时间（即最近一次是被第几组数据使用）．每次操作时判断这个位置 $\mathrm{tag}$ 中的时间和当前时间是否相同，就可以判断这个位置应该是 $0$ 还是数组内的值．

???+ note "实现"
    === "C++"
        ```cpp
        // 时间戳优化
        int tag[MAXN], t[MAXN], Tag;
        
        void reset() { ++Tag; }
        
        void add(int k, int v) {
          while (k <= n) {
            if (tag[k] != Tag) t[k] = 0;
            t[k] += v, tag[k] = Tag;
            k += lowbit(k);
          }
        }
        
        int getsum(int k) {
          int ret = 0;
          while (k) {
            if (tag[k] == Tag) ret += t[k];
            k -= lowbit(k);
          }
          return ret;
        }
        ```
    
    === "Python"
        ```python
        # 时间戳优化
        tag = [0] * MAXN
        t = [0] * MAXN
        Tag = 0
        
        
        def reset():
            Tag = Tag + 1
        
        
        def add(k, v):
            while k <= n:
                if tag[k] != Tag:
                    t[k] = 0
                t[k] = t[k] + v
                tag[k] = Tag
                k = k + lowbit(k)
        
        
        def getsum(k):
            ret = 0
            while k:
                if tag[k] == Tag:
                    ret = ret + t[k]
                k = k - lowbit(k)
            return ret
        ```

## 例题

-   [树状数组 1：单点修改，区间查询](https://loj.ac/problem/130)
-   [树状数组 2：区间修改，单点查询](https://loj.ac/problem/131)
-   [树状数组 3：区间修改，区间查询](https://loj.ac/problem/132)
-   [二维树状数组 1：单点修改，区间查询](https://loj.ac/problem/133)
-   [二维树状数组 2：区间修改，单点查询](https://loj.ac/problem/134)
-   [二维树状数组 3：区间修改，区间查询](https://loj.ac/problem/135)


## ds/finger-tree.md

author: isdanni

???+ warning "注意"
    此章是选读内容，在阅读前请确定你对函数式编程（Functional Programming）有一定了解．

## 简介

**手指树**（Finger Tree）是一种 **纯函数式** 数据结构，由 Ralf Hinze 和 Ross Paterson 提出．

## 为什么需要手指树

在函数式编程中，列表是十分常见的数据类型．对于基于序列的操作，包括在两端添加和删除元素（双端队列操作），在任意节点插入、连接、删除，查找某个满足要求的元素，将序列拆分为子序列，几乎所有的函数型语言都支持．但是对于高效的更多操作，这些语言很难做到．即使有相对应的实现，通常也都非常复杂，实际很难使用．

而指状树提供了一种纯函数式的序列数据结构，它可以在均摊常量时间（amortized constant time）内完成访问，添加到序列的前端和末尾等操作，以及在对数时间（logarithmic time）内完成串联和随机访问．除了良好的渐近运行时边界外，手指树还非常灵活：当与元素上的幺半群标记（[monoidal tag](https://en.wikipedia.org/wiki/Monoidal_category)）结合时，指状树可用于实现高效的随机访问序列、有序序列、间隔树和优先级队列．

## 基本结构

手指树在树的「手指」（叶子）的地方存储数据，访问时间为分摊常量．手指是一个可以访问部分数据结构的点．在命令式语言（imperative language）中，这被称做指针．在手指树中，「手指」是指向序列末端或叶节点的结构．手指树还在每个内部节点中存储对其后代应用一些关联操作的结果．存储在内部节点中的数据可用于提供除树类数据结构之外的功能．

1.  手指树的深度由下到上计算．
2.  手指树的第一级，即树的叶节点，仅包含值，深度为 $0$．第二级为深度 $1$．第三级为深度 $2$，依此类推．
3.  离根越近，节点指向的原始树（在它是手指树之前的树）的子树越深．这样，沿着树向下工作就是从叶子到树的根，这与典型的树数据结构相反．为了获得这种的结构，我们必须确保原始树具有统一的深度．在声明节点对象时，必须通过子节点的类型进行参数化．深度为 $1$ 及以上的脊椎上的节点指向树，通过这种参数化，它们可以由嵌套节点表示．

### 将一棵树变成手指树

???+ note "注释"
    **2-3 树** 是一种树状数据结构，其中每个带有子节点（内部节点）的节点具有两个子节点（$2$ 节点）和一个数据元素或三个子节点（$3$ 节点）和两个数据元素．2-3 树是 $3$ 阶 B 树．树外部的节点（叶节点）没有子节点和一两个数据元素．

我们将从平衡 2-3 树开始这个过程．为了使手指树正常工作，所有的叶节点需要是水平的．如下图所示（图片取自手指树论文）：

![](./images/finger-tree-1.png)

手指是「一种结构，可以有效地访问靠近特定位置的树的节点．」要制作手指树，我们需要将手指放在树的左右两端，取树的最左边和最右边的内部节点并将它们拉起来，使树的其余部分悬在它们之间，这为我们提供了对序列末尾的均摊常量访问时间．

![](./images/finger-tree-2.png)

这种新的数据结构被称为手指树．手指树由沿其树脊（棕色线）分布的几层（下方蓝色框）组成：

![](./images/finger-tree-3.png)

```haskell
data FingerTree a = Empty
                  | Single a
                  | Deep (Digit a) (FingerTree (Node a)) (Digit a)

data Digit a = One a | Two a a | Three a a a | Four a a a a
data Node a = Node2 a a | Node3 a a a
```

示例中的数字是带有字母的节点．每个列表由树脊上每个节点的前缀或后缀划分．在转换后的 2-3 树中，顶层的数字列表似乎可以有两个或三个长度，而较低级别的长度只有一或两个．为了使手指树的某些应用程序能够如此高效地运行，手指树允许在每个级别上有 $1$ 到 $4$ 个子树．手指树的数字可以转换成一个列表，如：

```haskell
type Digit a = One a | Two a a | Three a a a | Four a a a a
```

顶层具有类型 $a$ 的元素，下一层具有类型节点 $a$ 的元素，因为树脊和叶子之间的节点，这通常意味着树的第 $n$ 层具有元素类型为 $Node^{n}$ $a$，或 2-3 个深度为 $n$ 的树．这意味着 $n$ 个元素的序列由深度为 `Θ(log n)` 的树表示．距离最近端 $d$ 的元素存储在树中 `Θ(log d)` 深度处．

### 双向队列操作

指状树也可以制作高效的双向队列．无论结构是否持久，所有操作都需要 `Θ(1)` 时间．它可以被看作是的隐式双端队列的扩展[^okasaki1999purely]：

1.  用 2-3 个节点替换对提供了足够的灵活性来支持有效的串联．（为了保持恒定时间的双端队列操作，必须将 Digit 扩展为四．）
2.  用幺半群（monoid）注释内部节点允许有效的分裂．

```haskell
data ImplicitDeque a = Empty
                     | Single a
                     | Deep (Digit a) (ImplicitDeque (a, a)) (Digit a)

data Digit a = One a | Two a a | Three a a a
```

## 时间复杂度

手指树提供了对树的「手指」（叶子）的分摊常量时间访问，这是存储数据的地方，以及在较小部分的大小中连接和拆分对数时间．它还在每个内部节点中存储对其后代应用一些关联操作的结果．存储在内部节点中的「摘要」数据可用于提供除树之外的数据结构的功能．

| 操作                            | 手指树                    | 注释 2-3 树 (annotated 2-3 tree) | 列表（list）             | 向量（vector） |
| ----------------------------- | ---------------------- | ----------------------------- | -------------------- | ---------- |
| `cons`,`snoc`                 | $O(1)$                 | $O(\log n)$                   | $O(1)$/$O(n)$        | $O(n)$     |
| `viewl`,`viewr`               | $O(1)$                 | $O(\log n)$                   | $O(1)$/$O(n)$        | $O(1)$     |
| `measure`/`length`            | $O(1)$                 | $O(1)$                        | $O(n)$               | $O(1)$     |
| `append`                      | $O(\log \min(l1, l2))$ | $O(\log n)$                   | $O(n)$               | $O(m+n)$   |
| `split`                       | $O(\log \min(n, l-n))$ | $O(\log n)$                   | $O(n)$               | $O(1)$     |
| `replicate`                   | $O(\log n)$            | $O(\log n)$                   | $O(n)$               | $O(n)$     |
| `fromList`,`toList`,`reverse` | $O(l)$/$O(l)$/$O(l)$   | $O(l)$                        | $O(1)$/$O(1)$/$O(n)$ | $O(n)$     |
| `index`                       | $O(\log \min(n, l-n))$ | $O(\log n)$                   | $O(n)$               | $O(1)$     |

## 应用

指状树可用于建造其他树．例如，优先级队列可以通过树中子节点的最小优先级标记内部节点来实现，或者索引列表/数组可以通过节点的子节点中叶子的计数来标记节点来实现．其他应用包括随机访问序列（如下所述）、有序序列和区间树．

手指树可以提供平均 $O(1)$ 的推、反转、弹出，$O(\log n)$ 追加和拆分；并且可以适应索引或排序序列．和所有函数式数据结构一样，它本质上是持久的；也就是说，始终保留旧版本的树．

对于代码实现，Haskell 核心库中的有限序列 `Seq` 的实现使用了 2-3 手指树（[Data.Sequence](https://hackage.haskell.org/package/containers-0.6.5.1/docs/Data-Sequence.html)），OCaml 中 `BatFingerTree` 模块的 [实现](https://ocaml-batteries-team.github.io/batteries-included/hdoc2/BatFingerTree.html) 也使用了通用手指树数据结构．手指树可以使用或不使用惰性求值来实现，但惰性允许更简单的实现．

## 参考资料与拓展阅读

1.  Ralf Hinze and Ross Paterson, "[Finger trees: a simple general-purpose data structure](http://www.staff.city.ac.uk/~ross/papers/FingerTree.html)", Journal of Functional Programming 16:2 (2006) pp 197-217.
2.  [Finger Tree - Wikipedia](https://en.wikipedia.org/wiki/Finger_tree)

[^okasaki1999purely]: [Purely Functional Data Structures](https://www.cambridge.org/us/academic/subjects/computer-science/programming-languages-and-applied-logic/purely-functional-data-structures), Chris Okasaki (1999)


## ds/global-bst.md

## 引入

前置知识：[树链剖分](../graph/hld.md)

由于树链剖分的时间复杂度为 $O(n\log^2 n)$，而我们熟知的 LCT 虽然时间复杂度为 $O(n\log n)$，但常数较大，可能比树链剖分还慢．那么有什么既是 $O(n\log n)$ 的，常数又相对较小的方法呢？这个时候全局平衡二叉树就出现了．

全局平衡二叉树实际上是一颗二叉树森林，其中的每颗二叉树维护一条重链．但是这个森林里的二叉树又互有联系，其中每个二叉树的根连向这个重链链头的父亲，就像 LCT 中一样．但全局平衡二叉树是静态树，区别于 LCT，建成后树的形态不变．

全局平衡二叉树是一种可以处理树上链修改/查询的数据结构，可以做到：

-   $O(\log n)$ 一条链整体修改．
-   $O(\log n)$ 一条链整体查询．
-   $O(\log n)$ 求最近公共祖先，子树修改，子树查询等，这些复杂度和重链剖分是一样的．

## 主要性质

1.  全局平衡二叉树由很多棵二叉树通过轻边连起来组成，每一棵二叉树维护了原树的一条重链，其中序遍历的顺序就是这条重链深度单调递增的顺序．每个节点都仅出现在一棵二叉树中．
2.  边分为重边和轻边，重边是包含在二叉树中的边，维护的时候就像正常维护二叉树一样，记录左右儿子和父节点．轻边从一颗二叉树的根节点指向它所对应的重链顶端节点的父节点．轻边维护的时候 "认父不认子"，即只能从子节点访问到父节点，不能反过来．注意，全局平衡二叉树中的边和原树中的边没有对应关系．
3.  算上重边和轻边，全局平衡二叉树的高度是 $O(\log n)$ 级别的．这条是保证全局平衡二叉树时间复杂度的性质．

下面是一个全局平衡二叉树建树的例子．第一张图是原树，以节点 1 为根节点．实线是重边．

![global-bst-1](images/global-bst-1.svg)

第二张图是建出来的全局平衡二叉树，其中虚线是轻边，实线是重边，每一棵二叉树用红圈表示．

![global-bst-2](images/global-bst-2.svg)

## 建树

首先是像普通重链剖分一样，一次 DFS 求出每个节点的重儿子．然后从根开始，找到根节点所在的重链，对于这些点的轻儿子递归建树，并连上轻边．然后我们需要给重链上的点建一棵二叉树．我们先把重链上的点存到数组里，求出每个点轻儿子的子树大小之和加一（即该点本身所贡献的 size）．然后我们按照这个求出这条重链的加权中点，把它作为二叉树的根，两边递归建树，并连上重边．

代码如下：

???+ note "实现"
    ```cpp
    std::vector<int> G[N];
    int n, fa[N], son[N], sz[N];
    
    void dfsS(int u) {
      sz[u] = 1;
      for (int v : G[u]) {
        dfsS(v);
        sz[u] += sz[v];
        if (sz[v] > sz[son[u]]) son[u] = v;
      }
    }
    
    int b[N], bs[N], l[N], r[N], f[N], ss[N];
    
    // 给b中[bl,br)内的点建二叉树，返回二叉树的根
    int cbuild(int bl, int br) {
      int x = bl, y = br;
      while (y - x > 1) {
        int mid = (x + y) >> 1;
        if (2 * (bs[mid] - bs[bl]) <= bs[br] - bs[bl])
          x = mid;
        else
          y = mid;
      }
      // 二分求出按bs加权的中点
      y = b[x];
      ss[y] = br - bl;  // ss：二叉树中重子树的大小
      if (bl < x) {
        l[y] = cbuild(bl, x);
        f[l[y]] = y;
      }
      if (x + 1 < br) {
        r[y] = cbuild(x + 1, br);
        f[r[y]] = y;
      }
      return y;
    }
    
    int build(int x) {
      int y = x;
      do
        for (int v : G[y])
          if (v != son[y])
            f[build(v)] =
                y;  // 递归建树并连轻边，注意要从二叉树的根连边，不是从儿子连边
      while (y = son[y]);
      y = 0;
      do {
        b[y++] = x;                              // 存放重链中的点
        bs[y] = bs[y - 1] + sz[x] - sz[son[x]];  // bs：轻儿子size和+1，求前缀和
      } while (x = son[x]);
      return cbuild(0, y);
    }
    ```

由代码可以看出建树的时间复杂度是 $O(n\log n)$．接下来我们可以证明树高是 $O(\log n)$ 的：考虑从任意一个点跳父节点到根．跳轻边就相当于在原树中跳到另一条重链，由重链剖分的性质可得跳轻边最多 $O(\log n)$ 条；因为建二叉树的时候根节点找的是算轻儿子的加权中点，那么跳一次重边算上轻儿子的 size 至少翻倍，所以跳重边最多也是 $O(\log n)$ 条．整体树高就是 $O(\log n)$ 的．

## 查询

以上就是关于全局平衡二叉树的部分．剩下关于链修改和链查询的操作方法相对简单，只需要从要操作的点出发，一直跳跃到根节点．要操作某个点所在的重链上比它深度小的所有点，本质上等同于在这条重链的二叉树中操作目标节点左侧的所有节点．这些操作可以分解成一系列子树操作，与普通二叉树的维护方法类似，其中涉及到维护子树和以及打子树标记．在这一过程中，使用的是标记永久化．也可以用 pushdown 来打标记，用 pushup 维护子树和，不过这种方式可能相对复杂，因为通常情况下，处理二叉树是自上而下进行操作，但在这里，需要首先确定跳跃路径，然后再从上到下进行 pushdown，可能导致常数较大．

代码如下：

???+ note "实现"
    ```cpp
    // a：子树加标记
    // s：子树和（不算加标记的）
    int a[N], s[N];
    
    void add(int x) {
      bool t = true;
      int z = 0;
      while (x) {
        s[x] += z;
        if (t) {
          a[x]++;
          if (r[x]) a[r[x]]--;
          z += 1 + ss[l[x]];
          s[x] -= ss[r[x]];
        }
        t = (x != l[f[x]]);
        if (t && x != r[f[x]]) z = 0;  // 跳过轻边要清空
        x = f[x];
      }
    }
    
    int query(int x) {
      int ret = 0;
      bool t = true;
      int z = 0;
      while (x) {
        if (t) {
          ret += s[x] - s[r[x]];
          ret -= 1ll * ss[r[x]] * a[r[x]];
          z += 1 + ss[l[x]];
        }
        ret += 1ll * z * a[x];
        t = (x != l[f[x]]);
        if (t && x != r[f[x]]) z = 0;  // 跳过轻边要清空
        x = f[x];
      }
      return ret;
    }
    ```

此外，对于子树操作，就是要考虑轻儿子的，需要再维护一个包括轻儿子的子树和、子树标记，可以去做 "[P3384【模板】轻重链剖分](https://www.luogu.com.cn/problem/P3384)"．

## 例题

??? note "[P4751【模板】"动态 DP"& 动态树分治（加强版）](https://www.luogu.com.cn/problem/P4751)"
    ```cpp
    #include <algorithm>
    #include <cstdio>
    #include <cstring>
    constexpr int MAXN = 1000000;
    constexpr int MAXM = 3000000;
    constexpr int INF = 0x3FFFFFFF;
    using namespace std;
    
    struct edge {
      int to;
      edge *nxt;
    } edges[MAXN * 2 + 5];
    
    edge *ncnt = &edges[0], *Adj[MAXN + 5];
    int n, m;
    
    struct Matrix {
      int M[2][2];
    
      Matrix operator*(const Matrix &B) const {
        static Matrix ret;
        for (int i = 0; i < 2; i++)
          for (int j = 0; j < 2; j++) {
            ret.M[i][j] = -INF;
            for (int k = 0; k < 2; k++)
              ret.M[i][j] = max(ret.M[i][j], M[i][k] + B.M[k][j]);
          }
        return ret;
      }
    } matr1[MAXN + 5], matr2[MAXN + 5];  // 每个点维护两个矩阵
    
    int root;
    int w[MAXN + 5], dep[MAXN + 5], son[MAXN + 5], siz[MAXN + 5], lsiz[MAXN + 5];
    int g[MAXN + 5][2], f[MAXN + 5][2], trfa[MAXN + 5], bstch[MAXN + 5][2];
    int stk[MAXN + 5], tp;
    bool vis[MAXN + 5];
    
    void AddEdge(int u, int v) {
      edge *p = ++ncnt;
      p->to = v;
      p->nxt = Adj[u];
      Adj[u] = p;
    
      edge *q = ++ncnt;
      q->to = u;
      q->nxt = Adj[v];
      Adj[v] = q;
    }
    
    void DFS(int u, int fa) {
      siz[u] = 1;
      for (edge *p = Adj[u]; p != NULL; p = p->nxt) {
        int v = p->to;
        if (v == fa) continue;
        dep[v] = dep[u] + 1;
        DFS(v, u);
        siz[u] += siz[v];
        if (!son[u] || siz[son[u]] < siz[v]) son[u] = v;
      }
      lsiz[u] = siz[u] - siz[son[u]];  // 轻儿子的siz和+1
    }
    
    void DFS2(int u, int fa) {
      f[u][1] = w[u], f[u][0] = 0;
      g[u][1] = w[u], g[u][0] = 0;
      if (son[u]) {
        DFS2(son[u], u);
        f[u][0] += max(f[son[u]][0], f[son[u]][1]);
        f[u][1] += f[son[u]][0];
      }
      for (edge *p = Adj[u]; p != NULL; p = p->nxt) {
        int v = p->to;
        if (v == fa || v == son[u]) continue;
        DFS2(v, u);
        f[u][0] += max(f[v][0], f[v][1]);  // f[][]就是正常的DP数组
        f[u][1] += f[v][0];
        g[u][0] += max(f[v][0], f[v][1]);  // g[][]数组只统计了自己和轻儿子的信息
        g[u][1] += f[v][0];
      }
    }
    
    void PushUp(int u) {
      matr2[u] = matr1[u];  // matr1是单点加上轻儿子的信息，matr2是区间信息
      if (bstch[u][0]) matr2[u] = matr2[bstch[u][0]] * matr2[u];
      // 注意转移的方向，但是如果我们的矩乘定义不同，可能方向也会不同
      if (bstch[u][1]) matr2[u] = matr2[u] * matr2[bstch[u][1]];
    }
    
    int getmx2(int u) { return max(matr2[u].M[0][0], matr2[u].M[0][1]); }
    
    int getmx1(int u) { return max(getmx2(u), matr2[u].M[1][0]); }
    
    int SBuild(int l, int r) {
      if (l > r) return 0;
      int tot = 0;
      for (int i = l; i <= r; i++) tot += lsiz[stk[i]];
      for (int i = l, sumn = lsiz[stk[l]]; i <= r; i++, sumn += lsiz[stk[i]])
        if (sumn * 2 >= tot)  // 是重心了
        {
          int lch = SBuild(l, i - 1), rch = SBuild(i + 1, r);
          bstch[stk[i]][0] = lch;
          bstch[stk[i]][1] = rch;
          trfa[lch] = trfa[rch] = stk[i];
          PushUp(stk[i]);  // 将区间的信息统计上来
          return stk[i];
        }
      return 0;
    }
    
    int Build(int u) {
      for (int pos = u; pos; pos = son[pos]) vis[pos] = true;
      for (int pos = u; pos; pos = son[pos])
        for (edge *p = Adj[pos]; p != NULL; p = p->nxt)
          if (!vis[p->to])  // 是轻儿子
          {
            int v = p->to, ret = Build(v);
            trfa[ret] = pos;  // 轻儿子的treefa[]接上来
          }
      tp = 0;
      for (int pos = u; pos; pos = son[pos]) stk[++tp] = pos;  // 把重链取出来
      int ret = SBuild(1, tp);  // 对重链进行单独的SBuild(我猜是Special Build?)
      return ret;               // 返回当前重链的二叉树的根
    }
    
    void Modify(int u, int val) {
      matr1[u].M[1][0] += val - w[u];
      w[u] = val;
      for (int pos = u; pos; pos = trfa[pos])
        if (trfa[pos] && bstch[trfa[pos]][0] != pos && bstch[trfa[pos]][1] != pos) {
          matr1[trfa[pos]].M[0][0] -= getmx1(pos);
          matr1[trfa[pos]].M[0][1] = matr1[trfa[pos]].M[0][0];
          matr1[trfa[pos]].M[1][0] -= getmx2(pos);
          PushUp(pos);
          matr1[trfa[pos]].M[0][0] += getmx1(pos);
          matr1[trfa[pos]].M[0][1] = matr1[trfa[pos]].M[0][0];
          matr1[trfa[pos]].M[1][0] += getmx2(pos);
        } else
          PushUp(pos);
    }
    
    int read() {
      int ret = 0, f = 1;
      char c = 0;
      while (c < '0' || c > '9') {
        c = getchar();
        if (c == '-') f = -f;
      }
      ret = 10 * ret + c - '0';
      while (true) {
        c = getchar();
        if (c < '0' || c > '9') break;
        ret = 10 * ret + c - '0';
      }
      return ret * f;
    }
    
    void print(int x) {
      if (x == 0) return;
      print(x / 10);
      putchar(x % 10 + '0');
    }
    
    int main() {
      scanf("%d %d", &n, &m);
      for (int i = 1; i <= n; i++) w[i] = read();
      int u, v;
      for (int i = 1; i < n; i++) {
        u = read(), v = read();
        AddEdge(u, v);
      }
      DFS(1, -1);
      // 求重儿子
      DFS2(1, -1);
      // 求初始的DP值，也可以在Build()里面求，但是这样写就和树剖的写法统一了
      for (int i = 1; i <= n; i++) {
        matr1[i].M[0][0] = matr1[i].M[0][1] = g[i][0];
        matr1[i].M[1][0] = g[i][1], matr1[i].M[1][1] = -INF;  // 初始化矩阵
      }
      root = Build(1);  // root即为根节点所在重链的重心
      int lastans = 0;
      for (int i = 1; i <= m; i++) {
        u = read(), v = read();
        u ^= lastans;  // 强制在线
        Modify(u, v);
        lastans = getmx1(root);  // 直接取值
        if (lastans == 0)
          putchar('0');
        else
          print(lastans);
        putchar('\n');
      }
      return 0;
    }
    ```

## 参考

[P4211 \[LNOI2014\] LCA | 全局平衡二叉树](https://www.luogu.com.cn/blog/nederland/globalbst)


## ds/hash.md

## 引入

![](images/hashtable.svg)

哈希表又称散列表，一种以「key-value」形式存储数据的数据结构．所谓以「key-value」形式存储数据，是指任意的键值 key 都唯一对应到内存中的某个位置．只需要输入查找的键值，就可以快速地找到其对应的 value．可以把哈希表理解为一种高级的数组，这种数组的下标可以是很大的整数，浮点数，字符串甚至结构体．

## 哈希函数

要让键值对应到内存中的位置，就要为键值计算索引，也就是计算这个数据应该放到哪里．这个根据键值计算索引的函数就叫做哈希函数，也称散列函数．举个例子，如果键值是一个人的身份证号码，哈希函数就可以是号码的后四位，当然也可以是号码的前四位．生活中常用的「手机尾号」也是一种哈希函数．在实际的应用中，键值可能是更复杂的东西，比如浮点数、字符串、结构体等，这时候就要根据具体情况设计合适的哈希函数．哈希函数应当易于计算，并且尽量使计算出来的索引均匀分布．

能为 key 计算索引之后，我们就可以知道每个键值对应的值 value 应该放在哪里了．假设我们用数组 a 存放数据，哈希函数是 f，那键值对 `(key, value)` 就应该放在 `a[f(key)]` 上．不论键值是什么类型，范围有多大，`f(key)` 都是在可接受范围内的整数，可以作为数组的下标．

在 OI 中，最常见的情况应该是键值为整数的情况．当键值的范围比较小的时候，可以直接把键值作为数组的下标，但当键值的范围比较大，比如以 $10^9$ 范围内的整数作为键值的时候，就需要用到哈希表．一般把键值模一个较大的质数作为索引，也就是取 $f(x)=x \bmod M$ 作为哈希函数．

另一种比较常见的情况是 key 为字符串的情况，由于不支持以字符串作为数组下标，并且将字符串转化成数字存储也可以避免多次进行字符串比较．所以在 OI 中，一般不直接把字符串作为键值，而是先算出字符串的哈希值，再把其哈希值作为键值插入到哈希表里．关于字符串的哈希值，我们一般采用进制的思想，将字符串想象成一个 $127$ 进制的数．那么，对于每一个长度为 $n$ 的字符串 $s$，就有：

$x = s_0 \cdot 127^0 + s_1 \cdot 127^1 + s_2 \cdot 127^2 + \dots + s_n \cdot 127^n$

我们可以将得到的 $x$ 对 $2^{64}$（即 `unsigned long long` 的最大值）取模．这样 `unsigned long long` 的自然溢出就等价于取模操作了．可以使操作更加方便．

这种方法虽然简单，但并不是完美的．可以构造数据使这种方法发生冲突（即两个字符串的 $x$ 对 $2^{64}$ 取模后的结果相同）．  
我们可以使用双哈希的方法：选取两个大质数 $a,b$．当且仅当两个字符串的哈希值对 $a$ 和对 $b$ 取模都相等时，我们才认为这两个字符串相等．这样可以大大降低哈希冲突的概率．

## 冲突

如果对于任意的键值，哈希函数计算出来的索引都不相同，那只用根据索引把 `(key, value)` 放到对应的位置就行了．但实际上，常常会出现两个不同的键值，他们用哈希函数计算出来的索引是相同的．这时候就需要一些方法来处理冲突．在 OI 中，最常用的方法是拉链法．

### 拉链法

拉链法也称开散列法（open hashing）．

拉链法是在每个存放数据的地方开一个链表，如果有多个键值索引到同一个地方，只用把他们都放到那个位置的链表里就行了．查询的时候需要把对应位置的链表整个扫一遍，对其中的每个数据比较其键值与查询的键值是否一致．如果索引的范围是 $1\ldots M$，哈希表的大小为 $N$，那么一次插入/查询需要进行期望 $O(\frac{N}{M})$ 次比较．

#### 实现

=== "C++"
    ```cpp
    constexpr int SIZE = 1000000;
    constexpr int M = 999997;
    
    struct HashTable {
      struct Node {
        int next, value, key;
      } data[SIZE];
    
      int head[M], size;
    
      int f(int key) { return (key % M + M) % M; }
    
      int get(int key) {
        for (int p = head[f(key)]; p; p = data[p].next)
          if (data[p].key == key) return data[p].value;
        return -1;
      }
    
      int modify(int key, int value) {
        for (int p = head[f(key)]; p; p = data[p].next)
          if (data[p].key == key) return data[p].value = value;
      }
    
      int add(int key, int value) {
        if (get(key) != -1) return -1;
        data[++size] = Node{head[f(key)], value, key};
        head[f(key)] = size;
        return value;
      }
    };
    ```

=== "Python"
    ```python
    M = 999997
    SIZE = 1000000
    
    
    class Node:
        def __init__(self, next=None, value=None, key=None):
            self.next = next
            self.value = value
            self.key = key
    
    
    data = [Node() for _ in range(SIZE)]
    head = [0] * M
    size = 0
    
    
    def f(key):
        return key % M
    
    
    def get(key):
        p = head[f(key)]
        while p:
            if data[p].key == key:
                return data[p].value
            p = data[p].next
        return -1
    
    
    def modify(key, value):
        p = head[f(key)]
        while p:
            if data[p].key == key:
                data[p].value = value
                return data[p].value
            p = data[p].next
    
    
    def add(key, value):
        if get(key) != -1:
            return -1
        size = size + 1
        data[size] = Node(head[f(key)], value, key)
        head[f(key)] = size
        return value
    ```

这里再提供一个封装过的模板，可以像 map 一样用，并且较短

```cpp
struct hash_map {  // 哈希表模板

  struct data {
    long long u;
    int v, nex;
  };  // 前向星结构

  data e[SZ << 1];  // SZ 是 const int 表示大小
  int h[SZ], cnt;

  int hash(long long u) { return (u % SZ + SZ) % SZ; }

  // 这里使用 (u % SZ + SZ) % SZ 而非 u % SZ 的原因是
  // C++ 中的 % 运算无法将负数转为正数

  int& operator[](long long u) {
    int hu = hash(u);  // 获取头指针
    for (int i = h[hu]; i; i = e[i].nex)
      if (e[i].u == u) return e[i].v;
    return e[++cnt] = data{u, -1, h[hu]}, h[hu] = cnt, e[cnt].v;
  }

  hash_map() {
    cnt = 0;
    memset(h, 0, sizeof(h));
  }
};
```

在这里，hash 函数是针对键值的类型设计的，并且返回一个链表头指针用于查询．在这个模板中我们写了一个键值对类型为 `(long long, int)` 的 hash 表，并且在查询不存在的键值时返回 -1．函数 `hash_map()` 用于在定义时初始化．

### 闭散列法

闭散列方法把所有记录直接存储在散列表中，如果发生冲突则根据某种方式继续进行探查．

比如线性探查法：如果在 `d` 处发生冲突，就依次检查 `d + 1`，`d + 2`……

#### 实现

```cpp
constexpr int N = 360007;  // N 是最大可以存储的元素数量

class Hash {
 private:
  int keys[N];
  int values[N];

 public:
  Hash() { memset(values, 0, sizeof(values)); }

  int& operator[](int n) {
    // 返回一个指向对应 Hash[Key] 的引用
    // 修改成不为 0 的值 0 时候视为空
    int idx = (n % N + N) % N, cnt = 1;
    while (keys[idx] != n && values[idx] != 0) {
      idx = (idx + cnt * cnt) % N;
      cnt += 1;
    }
    keys[idx] = n;
    return values[idx];
  }
};
```

## 例题

[「JLOI2011」不重复数字](https://www.luogu.com.cn/problem/P4305)


## ds/heap.md

author: ouuan, HeRaNO

堆是一棵树，其每个节点都有一个键值，且每个节点的键值都大于等于/小于等于其父亲的键值．

每个节点的键值都大于等于其父亲键值的堆叫做小根堆，否则叫做大根堆．[STL 中的 `priority_queue`](../lang/csl/container-adapter.md#优先队列) 其实就是一个大根堆．

（小根）堆主要支持的操作有：插入一个数、查询最小值、删除最小值、合并两个堆、减小一个元素的值．

一些功能强大的堆（可并堆）还能（高效地）支持 merge 等操作．

一些功能更强大的堆还支持可持久化，也就是对任意历史版本进行查询或者操作，产生新的版本．

## 堆的分类

|    操作 `\` 数据结构[^ref4]   |                                      配对堆                                     |      二叉堆     |      左偏树     |          二项堆         |        斐波那契堆       |
| :---------------------: | :--------------------------------------------------------------------------: | :----------: | :----------: | :------------------: | :----------------: |
|        插入（insert）       |                                    $O(1)$                                    |  $O(\log n)$ |  $O(\log n)$ |  $O(\log n)$[^ref1]  |       $O(1)$       |
|     查询最小值（find-min）     |                                    $O(1)$                                    |    $O(1)$    |    $O(1)$    | $O(1)$[^ref2][^ref3] |       $O(1)$       |
|    删除最小值（delete-min）    |                              $O(\log n)$[^ref3]                              |  $O(\log n)$ |  $O(\log n)$ |      $O(\log n)$     | $O(\log n)$[^ref3] |
|        合并 (merge)       |                                    $O(1)$                                    |    $O(n)$    |  $O(\log n)$ |      $O(\log n)$     |       $O(1)$       |
| 减小一个元素的值 (decrease-key) | $o(\log n)$（下界 $\Omega(\log \log n)$，上界 $O(2^{2\sqrt{\log \log n}})$）[^ref3] |  $O(\log n)$ |  $O(\log n)$ |      $O(\log n)$     |    $O(1)$[^ref3]   |
|         是否支持可持久化        |                                   $\times$                                   | $\checkmark$ | $\checkmark$ |     $\checkmark$     |      $\times$      |

[^ref1]: 单次插入的复杂度为 $O(\log n)$，但有 $k$ 次连续插入时，可创建一个只包含要插入元素的二项堆，再将此堆与原先的二项堆进行合并，均摊复杂度为 $O(1)$

[^ref2]: 可以保存一个指向最小元素的指针，在执行其他操作时修改该指针，即可在 $O(1)$ 的复杂度下进行查询了

[^ref3]: 复杂度为均摊复杂度

[^ref4]: 表格来自于 [Wikipedia](https://en.wikipedia.org/wiki/Priority_queue#Summary_of_running_times)

习惯上，不加限定提到「堆」时往往都指二叉堆．


## ds/huffman-tree.md

author: Alex-McAvoy, lingkerio, LvCGame

## 树的带权路径长度

设二叉树具有 $n$ 个带权叶结点，从根结点到各叶结点的路径长度与相应叶节点权值的乘积之和称为 **树的带权路径长度（Weighted Path Length of Tree，WPL）**．

设 $w_i$ 为二叉树第 $i$ 个叶结点的权值，$l_i$ 为从根结点到第 $i$ 个叶结点的路径长度，则 WPL 计算公式如下：

$$
WPL=\sum_{i=1}^nw_il_i
$$

![](./images/huffman-tree-1.svg)

如上图所示，其 WPL 计算过程与结果如下：

$$
WPL=2*2+3*2+4*2+7*2=4+6+8+14=32
$$

## 结构

对于给定一组具有确定权值的叶结点，可以构造出不同的二叉树，其中，**WPL 最小的二叉树** 称为 **霍夫曼树（Huffman Tree）**．

对于霍夫曼树来说，其叶结点权值越小，离根越远，叶结点权值越大，离根越近，此外其仅有叶结点的度为 $0$，其他结点度均为 $2$．

## 霍夫曼算法

霍夫曼算法用于构造一棵霍夫曼树，算法步骤如下：

1.  **初始化**：由给定的 $n$ 个权值构造 $n$ 棵只有一个根节点的二叉树，得到一个二叉树集合 $F$．
2.  **选取与合并**：从二叉树集合 $F$ 中选取根节点权值 **最小的两棵** 二叉树分别作为左右子树构造一棵新的二叉树，这棵新二叉树的根节点的权值为其左、右子树根结点的权值和．
3.  **删除与加入**：从 $F$ 中删除作为左、右子树的两棵二叉树，并将新建立的二叉树加入到 $F$ 中．
4.  重复 2、3 步，当集合中只剩下一棵二叉树时，这棵二叉树就是霍夫曼树．

![](./images/huffman-tree-2.svg)

### 正确性证明

???+ note "引理"
    最优前缀编码树（Huffman 树）中的权值最小的两个叶结点总是最深的叶结点，并且将这两个结点调整为兄弟结点至少不会破坏编码树的最优性．

??? note "证明"
    我们采用反证法来证明该命题．假设在一棵最优前缀编码树中，存在两个权值最小的叶结点，它们不是最深的叶结点．设这两个结点为 $a$ 和 $b$，且它们的深度小于某个最深的叶结点．对于这个最深的叶结点 $c$，我们可以将 $a$ 和 $c$ 交换位置，或将 $b$ 和 $c$ 交换位置．由于 Huffman 算法保证树的每一层按权值最小的叶结点合并，因此在交换后，树的带权路径长度（WPL）将减少．由此矛盾可得出假设不成立，因此权值最小的两个叶结点必须是最深的叶结点．
    
    接下来，假设这两个权值最小的叶结点分别为 $a$ 和 $b$，它们的深度相同．如果在一棵最优前缀编码树中这两个结点不是兄弟结点，假设存在其他结点 $c$ 和 $d$ 与 $a$ 和 $b$ 分别是兄弟结点（假设 $a$ 和 $c$ 是兄弟结点，$b$ 和 $d$ 是兄弟结点）．我们可以将 $a$ 和 $b$ 合并为一个子树．
    
    -   如果 $a$ 和 $b$ 合并后的权值之和小于 $c$ 或 $d$ 的权值，那么我们可以将合并后的子树与权值较大的结点（如 $c$ 或 $d$）合并，形成新的子树，WPL 会减少．
    -   如果 $a$ 和 $b$ 的权值之和不小于 $c$ 和 $d$ 的权值，我们可以直接将 $a$ 和 $b$ 调整为兄弟结点，$c$ 和 $d$ 作为另一个兄弟结点，WPL 不会增加．
    
    因此，经过这样的调整，最优性不会被破坏，得证．

???+ note "定理"
    Huffman 算法得到的前缀编码树是最优前缀编码树．

??? note "证明"
    我们使用数学归纳法来证明该定理．
    
    -   **基本情况**: 当字母数 $n = 2$ 时，显然，直接将两个字母合并成一棵树即为最优编码树．
    -   **归纳假设**: 假设对于字母数 $n = k$（$k \geq 2$）时，Huffman 算法能够得到最优前缀编码树．
    -   **归纳步骤**: 对于字母数 $n = k + 1$，我们从 $k+1$ 个字母中选出两个权值最小的字母，将它们合并为一棵子树，子树的根作为虚拟字母（虚拟结点）．根据引理可知，这一操作不会破坏前缀编码树的最优性．此时，虚拟字母与剩下的 $k$ 个字母一同构成 $k + 1$ 个字母，根据归纳假设，当字母数为 $k$ 时，Huffman 算法能够得到最优前缀编码树．
    
    因此，通过数学归纳法，Huffman 算法对于任意字母数 $n$ 都能够得到最优前缀编码树，得证．

## 霍夫曼编码

在进行程序设计时，通常给每一个字符标记一个单独的代码来表示一组字符，即 **编码**．

在进行二进制编码时，假设所有的代码都等长，那么表示 $n$ 个不同的字符需要 $\left \lceil \log_2 n \right \rceil$ 位，称为 **等长编码**．

如果每个字符的 **使用频率相等**，那么等长编码无疑是空间效率最高的编码方法，而如果字符出现的频率不同，则可以让频率高的字符采用尽可能短的编码，频率低的字符采用尽可能长的编码，来构造出一种 **不等长编码**，从而获得更好的空间效率．

在设计不等长编码时，要考虑解码的唯一性，如果一组编码中任一编码都不是其他任何一个编码的前缀，那么称这组编码为 **前缀编码**，其保证了编码被解码时的唯一性．

霍夫曼树可用于构造 **最短的前缀编码**，即 **霍夫曼编码（Huffman Code）**，其构造步骤如下：

1.  设需要编码的字符集为：$d_1,d_2,\dots,d_n$，他们在字符串中出现的频率为：$w_1,w_2,\dots,w_n$．
2.  以 $d_1,d_2,\dots,d_n$ 作为叶结点，$w_1,w_2,\dots,w_n$ 作为叶结点的权值，构造一棵霍夫曼树．
3.  规定霍夫曼编码树的左分支代表 $0$，右分支代表 $1$，则从根结点到每个叶结点所经过的路径组成的 $0$、$1$ 序列即为该叶结点对应字符的编码．

![](./images/huffman-tree-3.svg)

## 示例代码

??? note "霍夫曼树的构建"
    ```cpp
    struct HNode {
      int weight;
      HNode *lchild, *rchild;
    };
    
    using Htree = HNode *;
    
    Htree createHuffmanTree(int arr[], int n) {
      Htree forest[N];
      Htree root = NULL;
      for (int i = 0; i < n; i++) {  // 将所有点存入森林
        Htree temp;
        temp = (Htree)malloc(sizeof(HNode));
        temp->weight = arr[i];
        temp->lchild = temp->rchild = NULL;
        forest[i] = temp;
      }
    
      for (int i = 1; i < n; i++) {  // n-1 次循环建霍夫曼树
        int minn = -1, minnSub;  // minn 为最小值树根下标，minnsub 为次小值树根下标
        for (int j = 0; j < n; j++) {
          if (forest[j] != NULL && minn == -1) {
            minn = j;
            continue;
          }
          if (forest[j] != NULL) {
            minnSub = j;
            break;
          }
        }
    
        for (int j = minnSub; j < n; j++) {  // 根据 minn 与 minnSub 赋值
          if (forest[j] != NULL) {
            if (forest[j]->weight < forest[minn]->weight) {
              minnSub = minn;
              minn = j;
            } else if (forest[j]->weight < forest[minnSub]->weight) {
              minnSub = j;
            }
          }
        }
    
        // 建新树
        root = (Htree)malloc(sizeof(HNode));
        root->weight = forest[minn]->weight + forest[minnSub]->weight;
        root->lchild = forest[minn];
        root->rchild = forest[minnSub];
    
        forest[minn] = root;     // 指向新树的指针赋给 minn 位置
        forest[minnSub] = NULL;  // minnSub 位置为空
      }
      return root;
    }
    ```

??? note "计算构成霍夫曼树的 WPL"
    ```cpp
    struct HNode {
      int weight;
      HNode *lchild, *rchild;
    };
    
    using Htree = HNode *;
    
    int getWPL(Htree root, int len) {  // 递归实现，对于已经建好的霍夫曼树，求 WPL
      if (root == NULL)
        return 0;
      else {
        if (root->lchild == NULL && root->rchild == NULL)  // 叶节点
          return root->weight * len;
        else {
          int left = getWPL(root->lchild, len + 1);
          int right = getWPL(root->rchild, len + 1);
          return left + right;
        }
      }
    }
    ```

??? note "对于未建好的霍夫曼树，直接求其 WPL"
    ```cpp
    int getWPL(int arr[], int n) {  // 对于未建好的霍夫曼树，直接求其 WPL
      priority_queue<int, vector<int>, greater<int>> huffman;  // 小根堆
      for (int i = 0; i < n; i++) huffman.push(arr[i]);
    
      int res = 0;
      for (int i = 0; i < n - 1; i++) {
        int x = huffman.top();
        huffman.pop();
        int y = huffman.top();
        huffman.pop();
        int temp = x + y;
        res += temp;
        huffman.push(temp);
      }
      return res;
    }
    ```

??? note "对于给定序列，计算霍夫曼编码"
    ```cpp
    struct HNode {
      int weight;
      HNode *lchild, *rchild;
    };
    
    using Htree = HNode *;
    
    void huffmanCoding(Htree root, int len, int arr[]) {  // 计算霍夫曼编码
      if (root != NULL) {
        if (root->lchild == NULL && root->rchild == NULL) {
          printf("结点为 %d 的字符的编码为: ", root->weight);
          for (int i = 0; i < len; i++) printf("%d", arr[i]);
          printf("\n");
        } else {
          arr[len] = 0;
          huffmanCoding(root->lchild, len + 1, arr);
          arr[len] = 1;
          huffmanCoding(root->rchild, len + 1, arr);
        }
      }
    }
    ```


## ds/kdt.md

author: hsfzLZH1, Ir1d, JosephusW

k-D Tree(KDT , k-Dimension Tree) 是一种可以 **高效处理 $k$ 维空间信息** 的数据结构．

在结点数 $n$ 远大于 $2^k$ 时，应用 k-D Tree 的时间效率很好．

在算法竞赛的题目中，一般有 $k=2$．在本页面分析时间复杂度时，将认为 $k$ 是常数．

## 建树

k-D Tree 具有二叉搜索树的形态，二叉搜索树上的每个结点都对应 $k$ 维空间内的一个点．其每个子树中的点都在一个 $k$ 维的超长方体内，这个超长方体内的所有点也都在这个子树中．

假设我们已经知道了 $k$ 维空间内的 $n$ 个不同的点的坐标，要将其构建成一棵 k-D Tree，步骤如下：

1.  若当前超长方体中只有一个点，返回这个点．

2.  选择一个维度，将当前超长方体按照这个维度分成两个超长方体．

3.  选择切割点：在选择的维度上选择一个点，这一维度上的值小于这个点的归入一个超长方体（左子树），其余的归入另一个超长方体（右子树）．

4.  将选择的点作为这棵子树的根节点，递归对分出的两个超长方体构建左右子树，维护子树的信息．

为了方便理解，我们举一个 $k=2$ 时的例子．

![](./images/kdt1.jpg)

其构建出 k-D Tree 的形态可能是这样的：

![](./images/kdt2.jpg)

其中树上每个结点上的坐标是选择的分割点的坐标，非叶子结点旁的 $x$ 或 $y$ 是选择的切割维度．

这样的复杂度无法保证．对于 $2,3$ 两步，我们提出两个优化：

1.  轮流选择 $k$ 个维度，以保证在任意连续 $k$ 层里每个维度都被切割到．
2.  每次在维度上选择切割点时选择该维度上的 **中位数**，这样可以保证每次分成的左右子树大小尽量相等．

可以发现，使用优化 $2$ 后，构建出的 k-D Tree 的树高最多为 $\log n+O(1)$．

现在，构建 k-D Tree 时间复杂度的瓶颈在于快速选出一个维度上的中位数，并将在该维度上的值小于该中位数的置于中位数的左边，其余置于右边．如果每次都使用 `sort` 函数对该维度进行排序，时间复杂度是 $O(n\log^2 n)$ 的．事实上，单次找出 $n$ 个元素中的中位数并将中位数置于排序后正确的位置的复杂度可以达到 $O(n)$．

我们来回顾一下快速排序的思想．每次我们选出一个数，将小于该数的置于该数的左边，大于该数的置于该数的右边，保证该数在排好序后正确的位置上，然后递归排序左侧和右侧的值．这样的期望复杂度是 $O(n\log n)$ 的．但是由于 k-D Tree 只要求要中位数在排序后正确的位置上，所以我们只需要递归排序包含中位数的 **一侧**．可以证明，这样的期望复杂度是 $O(n)$ 的．在 `algorithm` 库中，有一个实现相同功能的函数 `nth_element()`，要找到 `s[l]` 和 `s[r]` 之间的值按照排序规则 `cmp` 排序后在 `s[mid]` 位置上的值，并保证 `s[mid]` 左边的值小于 `s[mid]`，右边的值大于 `s[mid]`，只需写 `nth_element(s+l,s+mid,s+r+1,cmp)`．

借助这种思想，构建 k-D Tree 时间复杂度是 $O(n\log n)$ 的．

## 高维空间上的操作

在查询高维矩形区域内的所有点的一些信息时，记录每个结点子树内每一维度上的坐标的最大值和最小值．如果当前子树对应的矩形与所求矩形没有交点，则不继续搜索其子树；如果当前子树对应的矩形完全包含在所求矩形内，返回当前子树内所有点的权值和；否则，判断当前点是否在所求矩形内，更新答案并递归在左右子树中查找答案．

??? note "实现"
    ```cpp
    int query(int p) {
      if (!p) return 0;
      bool flag{false};
      for (int k : {0, 1}) flag |= (!(l.x[k] <= t[p].L[k] && t[p].R[k] <= h.x[k]));
      if (!flag) return t[p].sum;
      for (int k : {0, 1})
        if (t[p].R[k] < l.x[k] || h.x[k] < t[p].L[k]) return 0;
      int ans{0};
      flag = false;
      for (int k : {0, 1}) flag |= (!(l.x[k] <= t[p].x[k] && t[p].x[k] <= h.x[k]));
      if (!flag) ans = t[p].v;
      return ans += query(t[p].l) + query(t[p].r);
    }
    ```

### 复杂度分析

先考虑二维的，在查询矩形 $R$ 时，我们将 k-D Tree 上的结点分为三类：

1.  与 $R$ 无交．
2.  完全被 $R$ 包含．
3.  部分被 $R$ 包含．

显然单次查询的复杂度是第 3 类点的个数．注意到第三类点的矩形要么完全包含 $R$，要么互不包含，而前者显然只有 $O(h)=O(\log n)$ 个，现在我们来分析后者的个数．

首先，我们不妨令矩形的所有边偏移 $\epsilon$，使得查询矩形不穿过已经有的任何点．这样显然是不影响矩形的查询所涵盖的点集的．

注意到互不包含的第 3 类点所对应的矩形，一定有 $R$ 的一条边穿过之．所以我们只需要计算 $R$ 的每条边穿过的矩形个数，即任意一条线段最多经过多少个点对应的矩形．

考虑对于某一个结点 $u$，它有四个孙子，且它到每一个孙子都在两个维度上各进行了一次划分．经过观察可以发现，按照这种方法将一个矩形划分成四个子矩形，一条与坐标轴平行的线段最多经过两个区域，即从 $u$ 出发的查询，最多向下进入两个孙子仍有第 3 类点（如果线段刚好与分割边界重合则不一定，但是我们偏移查询矩形边界的操作使得这种情况不存在）．

而因为建树的时候，每个点是其整个子树在当前划分维度上的中位数，所以子树大小必定减半．于是，设 $u$ 的子树大小为 $n$，我们能写出如下递归式：

$$
T(n)=2T(n/4)+O(1)
$$

由主定理得 $T(n)=O(\sqrt{n})$．

将递归式推广到 $k$ 维，即 $T(n)=2^{k-1}T(n/2^k)+O(1)$，于是 $T(n)=O(n^{1-\frac1k})$（将 $k$ 视为常数）．

### 插入/删除

如果维护的这个 $k$ 维点集是可变的，即可能会插入或删除一些点，此时 k-D Tree 的平衡性无法保证．由于 k-D Tree 的构造，不能支持旋转，类似与 FHQ Treap 的随机优先级也不能保证其复杂度．对此，有两种比较常见的维护方法．

???+ note "Note"
    很多选手会使用替罪羊树结构来维护．但是注意到在刚才的复杂度分析中，要求儿子的子树大小严格减半，即树高必须为严格的 $\log n+O(1)$，而替罪羊树只满足树高 $O(\log n)$，故查询复杂度无法保证．

#### 根号重构

插入的时候，先存下来要插入的点，每 $B$ 次插入进行一次重构．

删除打个标记即可．如果要求较为严格，可以维护树内有多少个被删除了，达到 $B$ 则重构．

修改复杂度均摊 $O(n\log n/B)$，查询 $O(B+n^{1-\frac1k})$，若二者数量同阶则 $B=O(\sqrt{n\log n})$ 最优（修改 $O(\sqrt{n\log n})$，查询 $O(\sqrt{n\log n}+n^{1-\frac1k})$）．

#### 二进制分组

考虑维护若干棵 $2$ 的自然数次幂的 k-D Tree，满足这些树的大小之和为 $n$．

插入的时候，新增一棵大小为 $1$ 的 k-D Tree，然后不断将相同大小的树合并（直接拍扁重构）．实现的时候可以只重构一次．

容易发现需要合并的树的大小一定从 $2^0$ 开始且指数连续．复杂度类似二进制加法，是均摊 $O(n\log^2 n)$ 的，因为重构本身带 $\log$．

查询的时候，直接分别在每棵树上查询，复杂度为 $O\left(\sum_{i\geq0} (\frac n{2^i})^{1-\frac1k}\right)=O(n^{1-\frac1k})$．

### 例题

???+ note "[洛谷 P4148 简单题](https://www.luogu.com.cn/problem/P4148)"
    在一个初始值全为 $0$ 的 $n\times n$ 的二维矩阵上，进行 $q$ 次操作，每次操作为以下两种之一：
    
    1.  `1 x y A`：将坐标 $(x,y)$ 上的数加上 $A$．
    2.  `2 x1 y1 x2 y2`：输出以 $(x1,y1)$ 为左下角，$(x2,y2)$ 为右上角的矩形内（包括矩形边界）的数字和．
    
    强制在线．内存限制 `20M`．保证答案及所有过程量在 `int` 范围内．
    
    $1\le n\le 500000 , 1\le q\le 200000$

20M 的空间卡掉了所有树套树，强制在线卡掉了 CDQ 分治，只能使用 k-D Tree．

以下是二进制分组的参考代码．

??? note "参考代码"
    ```cpp
    --8<-- "docs/ds/code/kdt/kdt_3.cpp"
    ```

## 邻域查询

???+ warning "Warning"
    使用 k-D Tree 单次查询最近点的时间复杂度最坏还是 $O(n)$ 的，但不失为一种优秀的骗分算法，使用时请注意．在这里对邻域查询的讲解仅限于加强对 k-D Tree 结构的认识．

???+ note "例题 [luogu P1429 平面最近点对（加强版）](https://www.luogu.com.cn/problem/P1429)"
    给定平面上的 $n$ 个点 $(x_i,y_i)$，找出平面上最近两个点对之间的 [欧几里得距离](../geometry/distance.md#欧氏距离)．
    
    $2\le n\le 200000 , 0\le x_i,y_i\le 10^9$

首先建出关于这 $n$ 个点的 2-D Tree．

枚举每个结点，对于每个结点找到不等于该结点且距离最小的点，即可求出答案．每次暴力遍历 2-D Tree 上的每个结点的时间复杂度是 $O(n)$ 的，需要剪枝．我们可以维护一个子树中的所有结点在每一维上的坐标的最小值和最大值．假设当前已经找到的最近点对的距离是 $ans$，如果查询点到子树内所有点都包含在内的长方形的 **最近** 距离大于等于 $ans$，则在这个子树内一定没有答案，搜索时不进入这个子树．

此外，还可以使用一种启发式搜索的方法，即若一个结点的两个子树都有可能包含答案，先在与查询点距离最近的一个子树中搜索答案．可以认为，**查询点到子树对应的长方形的最近距离就是此题的估价函数**．

??? note "参考代码"
    ```cpp
    --8<-- "docs/ds/code/kdt/kdt_1.cpp"
    ```

???+ note "例题 [「CQOI2016」K 远点对](https://loj.ac/problem/2043)"
    给定平面上的 $n$ 个点 $(x_i,y_i)$，求欧几里得距离下的第 $k$ 远无序点对之间的距离．
    
    $n\le 100000 , 1\le k\le 100 , 0\le x_i,y_i<2^{31}$

和上一道例题类似，从最近点对变成了 $k$ 远点对，估价函数改成了查询点到子树对应的长方形区域的最远距离．用一个小根堆来维护当前找到的前 $k$ 远点对之间的距离，如果当前找到的点对距离大于堆顶，则弹出堆顶并插入这个距离，同样的，使用堆顶的距离来剪枝．

由于题目中强调的是无序点对，即交换前后两点的顺序后仍是相同的点对，则每个有序点对会被计算两次，那么读入的 $k$ 要乘以 $2$．

??? note "参考代码"
    ```cpp
    --8<-- "docs/ds/code/kdt/kdt_2.cpp"
    ```

## 习题

[「SDOI2010」捉迷藏](https://www.luogu.com.cn/problem/P2479)

[「Violet」天使玩偶/SJY 摆棋子](https://www.luogu.com.cn/problem/P4169)

[「国家集训队」JZPFAR](https://www.luogu.com.cn/problem/P2093)

[「BOI2007」Mokia 摩基亚](https://www.luogu.com.cn/problem/P4390)

[luogu P4475 巧克力王国](https://www.luogu.com.cn/problem/P4475)

[「CH 弱省胡策 R2」TATT](https://www.luogu.com.cn/problem/P3769)


## ds/kinetic-tournament-tree.md

author: Jerry3128

前置知识：[线段树](./seg.md)

## 问题引入

给定单变量线性函数序列 $F=\{f_1,\dots,f_n\}$：$f_i: \mathbf{R} \rightarrow \mathbf{R}$．其中 $f_i(x)=k_ix+b_i$ 且 $k_i,b_i \in \mathbf{R}$．我们需要维护以下操作：

-   $\operatorname{QueryMax}(l,r)$：给定 $l$ 和 $r$, 返回 $\max_{i=l}^r{f_i(0)}$．
-   $\operatorname{TranslateLeft}(l,r,\delta)$：给定 $l$,$r$ 和 $\delta$, 对于所有 $i\in[l,r]$，执行操作 $f_i(x) \leftarrow f_i(x+\delta)$，这个操作等价于执行 $b_i\leftarrow b_i+k_i\delta$．其中 $\delta > 0$．

为了方便，我们假定所有函数互不相同．

一次函数区间向左平移的本质是 $b_i \leftarrow k_i\cdot \delta$，也就是对于 $b_i$ 常数项，让它加上斜率 $k_i$ 乘上横坐标的平移量 $\delta$；这种操作等价于我们在许多数据结构问题中遇到的「按位置系数加权区间加」：即对于区间 $[l, r]$ 内的每个下标 $i$，给其值加上一个固定的数 $\delta$ 乘上该位置特有的系数 $k_i$．因此本质上一次函数区间平移就是所谓的，按位置系数加权区间加法．

为了展示 KTT 独特的二叉树形分治结构，我们将直接从区间平移入手．

## Kinetic Data Structures

Kinetic Data Structures 简称 KDS．KDS 用于维护几何对象系统在连续运动过程中的属性．

### 事件队列

我们假设每一个点都有一个已知的运动计划，这个计划可以提供它的完整或者部分运动信息，例如函数 $f_i(x)$ 形成的曲线或直线能够很好的描述动点 $i$ 的运动轨迹．运动计划随时可能变化，它可能是由于碰撞，或者环境交互的原因；我们称造成运动计划更改的原因为事件．事件队列会按时间顺序给出事件．

KDS 的一个关键方面是需要拥有容易维护的事件，即事件队列中事件类型对应于可能的组合变化，这些变化涉及数量恒定且通常较少的物体．例如，在本题的维护中，我们使用的一种事件类型是「函数 $f_i(0)$ 与函数 $f_{j}(0)$ 的大小发生变化」．

事件队列可以隐式维护．

### 证书

这些事件应当可以等价于通过一系列低阶代数条件的交保证，每个代数条件都涉及有限数量的对象．我们将这些条件称为 KDS 的证书．例如 $[f_i(0) > f_j(0)]$.

## Kinetic Tournament Tree

### 简介

Kinetic Tournament Tree（简称 KTT），属于 Kinetic Data Structures，首次出现于 1999 年的 [Data Structures for Mobile Data](https://www.sciencedirect.com/science/article/pii/S0196677498909889)，用于维护连续变化的数据．更普遍地，每一个采用如下动态化策略（kinetization strategy）的结构，都可以称为 Kinetic Tournament：

-   为静态算法中的关键操作（例如比较）生成正确性证书，并将每个证书与一个全局事件队列关联，记录该证书可能失效的时间点．
-   当某个证书失效时，我们能够高效地更新算法输出并维护证书集合．

在算法竞赛社区，它兴起于 2020 年国家集训队论文《[浅谈函数最值的动态维护](https://github.com/OI-wiki/libs/blob/master/%E9%9B%86%E8%AE%AD%E9%98%9F%E5%8E%86%E5%B9%B4%E8%AE%BA%E6%96%87/IOI2020%E4%B8%AD%E5%9B%BD%E5%9B%BD%E5%AE%B6%E5%80%99%E9%80%89%E9%98%9F%E8%AE%BA%E6%96%87%E9%9B%86%20%E9%9D%9E%E6%AD%A3%E5%BC%8F%E7%89%88.pdf)》．学术界的 KTT 与算法竞赛界的 KTT 在应用领域和实现上有所不同，因此我们将介绍为算法竞赛界进行一些优化过后的 KTT．

### 基本结构

首先我们考虑设计一个线段树结构相似的数据结构用于维护静态最大值．我们将线段树的结构建立出来，对于每个非叶节点，它的权值为两个孩子节点中较大的权值．在执行了 $O(n)$ 次比较过后，我们得到根节点的权值就是全局的最大值．现在，权值开始变化．只要 KTT 能探测到每一次树上点的最大值来源改变，我们就能够维护全局最大值．

为了让 KTT 能够探测到每一次树上最大值来源变换，对于树上节点 $x$ 以及其左、右儿子提供的函数 $f_L$ 和 $f_R$，我们定义证书为「$f_L$ 和 $f_R$ 的大小关系保持不变」．当证书失效的时候，我们就需要通过树上路径走到当前证书失效的节点来更新它的信息．为了维护每个证书失效的时间，我们发现证书失效的时刻正是两个函数拥有相同值的时刻，那么问题就变成了找到两个线性函数的交点的横坐标，可以在 $O(1)$ 时间内解决．

对于每个树上的节点维护出了它在 $0$ 处取到最大值的函数，以及当前证书失效的时间和整个子树内最早失效证书的失效时间；那么对于每个节点证书失效的时刻，我们就可以在这个时刻找到它并更新它的信息．这些信息是用来记录函数本身的信息的．接下来我们考虑维护区间平移操作，因为它是可以简单累加的，我们就可以使用懒标记去处理区间平移操作．

我们定义懒标记 $\Delta_v$ 表示 $v$ 节点子树内的所有其他节点上的函数都应该向左平移 $\Delta_v$ 个单位．此时，对于树上节点 $v$，一个新的操作要将其子树内的所有函数区间向左平移 $\delta$, 即 $f(x)\leftarrow f(x+\delta)$．我们需要更新懒标记：$\Delta_v\leftarrow \Delta_v + \delta$，即将子树内所有其他节点的偏移量进行累加．同时向左平移也意味着 $0$ 点函数值的变化．我们可以发现如果证书的失效横坐标为 $t$，那么平移后的失效横坐标应为 $t-\delta$；此时，如果 $t-\delta$ 越过 $0$ 点，就代表着证书失效，我们就需要往下递归找到当前证书所在节点，更新当前节点，并将新的信息向上更新到根．这个过程可以跟随着修改一起做．

因此我们便可以得到简单实现．

???+ example "参考实现"
    ```cpp
    --8<-- "docs/ds/code/ktt/ktt_1.cpp:core"
    ```

### 复杂度分析

证明 KTT 的时间复杂度需要用到势能分析．

设 $d(x)$ 为节点 $x$ 在线段树上的深度，根节点的深度为 $1$．定义节点 $x$ 在线段树上的势能为：

$$
\alpha(x) = \begin{cases}
d(x) & \text{if the lower slope function has larger value}  \\
0    & \text{otherwise}\\
\end{cases}
$$

即在 $x$ 比较的两个函数，如果拥有较小斜率的函数的值在 $0$ 点更大，那么当前节点势能为 $d(x)$，否则为 $0$．

定义整个 KTT 的势能为所有节点势能之和：

$$
\Phi = \sum_x \alpha(x)
$$

考虑某次对于节点 $x$，和它的父亲 $p$ 的实际更新代价 $c=1$，更新前后的势能分别为 $\Phi$ 和 $\Phi'$．我们去计算更新节点 $x$ 的均摊更新代价．由于当前节点 $x$ 被更新，那么在当下它的势能一定是由 $d(x)$ 下降到 $0$．而对于 $p$，它的势能最坏情况可能由 $0$ 上升到 $d(p)$：

$$
\begin{aligned}
\hat{c} &= 1 + \Phi' - \Phi\\
    &= 1 + (\alpha'(p) + \alpha'(x)) - (\alpha(p) + \alpha(x))\\
    &= 1 + (\alpha'(p) - \alpha(p)) + (\alpha'(x) - \alpha(x))\\
    &\leq 1 + d(p) - d(x)\\
    &= 0
\end{aligned}
$$

对实际代价求和，定义初始势能 $\Phi_s$ 以及最终势能 $\Phi_t$：

$$
\begin{aligned}
\sum c  &= \sum \hat{c} + \Phi_{s} - \Phi_{t}\\
    &\leq \Phi_{s} - \Phi_{t}\\
    &=O(n\log n)
\end{aligned}
$$

这部分为 KTT 在仅存在全局修改的情况下，它将所有证书失效更新完毕的次数．

额外的，考虑区间平移对势能的影响．对于某次区间平移，我们需要考虑的节点应当为，其子树当中存在但不是所有树节点被执行区间平移操作的节点．这样的节点也就是我们在执行修改操作的时候在树上经过的节点，它的数量不超过 $O(\log n)$ 个，最坏情况下每个节点的势能上涨 $d(x)\le \log n$，因此每次操作上涨 $O(\log^2 n)$ 的势能．

为了维护区间平移，更新证书的操作将会被执行 $O(n\log n + m\log^2 n)$ 次．每次更新证书我们需要从树上沿着路径走到证书失效的节点，这部分是 $O(\log n)$ 的．因此总时间复杂度为 $O(n\log^2 n+ m\log^3 n)$．

这个方法的优秀之处在于他已经触及问题时间复杂度的下界 $O(\lambda_{s}(n)\log^2 n)$．$\lambda_{s}(n)$ 表示长度最长的 (n, s) Davenport-Schinzel 序列．其中线性函数对应 $s=1$ 的 $\lambda_1(n)=n$．这部分属于计算几何内容，本篇不在这里赘述．

### 高次情况

如果我们维护的不是线性函数而是多项式函数，或者更加复杂的函数我们如何应对．两个复杂函数之间可能拥有多个交点．给定一个连续、完全定义的单变量函数序列 $F=\{f_1,\dots,f_n\}$：$f_i: \mathbf{R} \rightarrow \mathbf{R}$．其中每对函数的图像至多相交于 $s$ 个点．具有代表性的，$s$ 次多项式函数集合符合这个要求．

对于同样的问题，我们使用势能分析．

$d(x)$ 为节点 $x$ 在线段树上的深度，根节点的深度为 $1$．定义 $I(x)$ 表示在节点 $x$ 比较的两个函数，在 $0$ 点过后有几个交点．定义节点 $x$ 在线段树上的势能为：

$$
\alpha(x)=d(x)^{\log_2(s+1)}I(x)
$$

定义整个 KTT 的势能为所有节点势能之和：

$$
\Phi = \sum_x \alpha(x)
$$

考虑某次对于节点 $x$，和它的父亲 $p$ 的实际更新代价 $c=1$，更新前后的势能分别为 $\Phi$ 和 $\Phi'$．我们去计算更新节点 $x$ 的均摊更新代价．由于当前节点 $x$ 被更新，那么在当下它的势能一定是由 $d(x)^{\log_2(s+1)}I(x)$ 下降到 $d(x)^{\log_2(s+1)}(I(x)-1)$．而对于 $p$，它的势能最坏情况可能由 $0$ 上升到 $d(p)^{\log_2(s+1)}$：

$$
\begin{aligned}
        \hat{c} &= 1 + \Phi' - \Phi\\
                &= 1 + (\alpha'(x) - \alpha(x)) + (\alpha'(p) - \alpha(p))\\
                &\leq 1 - d(x)^{\log_2{(s+1)}} + s(d(x)-1)^{\log_2{(s+1)}}\\
                &\leq 0
    \end{aligned}
$$

由第三行到第四行我们使用了 $d(x)$ 为正整数的限制．

对实际代价求和，定义初始势能 $\Phi_s$ 以及最终势能 $\Phi_t$：

$$
\begin{aligned}
    \sum c  &= \sum \hat{c} - \Phi_t + \Phi_s\\
            &\leq \Phi_s - \Phi_t\\
            &= O(ns (\log n)^{\log_2{(s+1)}})
\end{aligned}
$$

我们得到复杂度的上界 $O(ns (\log n)^{1+\log_2{(s+1)}} + ms (\log n)^{2+\log_2{(s+1)}})$．[^ref1]

### 近似情况

给定一个连续、完全定义的单变量函数序列 $F=\{f_1,\dots,f_n\}$，定义 $\mathfrak U_F(x)$，$\mathfrak L_F(x)$ 和 $\mathfrak E_F(x)$ 分别为上包络、下包络和幅度．

$$
\begin{aligned}
    \mathfrak U_F(x) & = \max\{f_i(x) \mid f_i \in F\} \\
    \mathfrak L_F(x) & = \min\{f_i(x) \mid f_i \in F\} \\
    \mathfrak E_F(x) & = \mathfrak U_F(x) - \mathfrak L_F(x)
\end{aligned}
$$

我们只要求程序返回 $\tilde{\mathfrak U}_F(x)$ 满足

$$
\mathfrak U_F(x) \geq \tilde{\mathfrak U}_F(x) \geq \mathfrak U_F(x) - \epsilon \mathfrak E_F(x)
$$

那么在复杂情况下我们可以做到 $O((1/\epsilon^2)n\log^3 n)$，与多项式次数无关，以及我们允许函数同时进行区间左移或者右移．

## 参考文献与注释

[^ref1]: 需要注意的是，这仅仅给出的是上界，复杂度的下界应为 $O(\lambda_{s}(n)\log n)$．笔者猜测这里的势能分析构造应当参考 Davenport-Schinzel 序列对应的 $\lambda_{s}(n)$ 的通项公式以获取更紧的上界．

-   P. K. Agarwal, S. Har-Peled, and K. R. Varadarajan. Approximating extent measures of points. J. ACM, 51(4):606–635, July 2004.
-   J. Basch, L. J. Guibas, and J. Hershberger. Data structures for mobile data. Journal of Algorithms, 31(1):1–28, 1999.
-   G. Alexandron, H. Kaplan, and M. Sharir. Kinetic and dynamic data structures for convex hulls and upper envelopes. Computational Geometry, 36(2):144–158, 2007.


## ds/lct.md

## 简介

Link/Cut Tree 是一种数据结构，我们用它来解决 **动态树问题**．

Link/Cut Tree 又称 Link-Cut Tree，简称 LCT，但它不叫动态树，动态树是指一类问题．

Splay Tree 是 LCT 的基础，但是 LCT 用的 Splay Tree 和普通的 Splay 在细节处不太一样（进行了一些扩展）．

## 问题引入

维护一棵树，支持如下操作：

-   修改两点间路径权值．
-   查询两点间路径权值和．
-   修改某点子树权值．
-   查询某点子树权值和．

这是一道树剖模版题．

但是再加一个操作：

-   断开并连接一些边，保证仍是一棵树．

要求在线求出上面的答案．

这就成了动态树问题，可以使用 LCT 求解．

## 动态树问题

维护一个 **森林**，支持删除某条边，加入某条边，并保证加边，删边之后仍是森林．我们要维护这个森林的一些信息．

一般的操作有两点连通性，两点路径权值和，连接两点和切断某条边、修改信息等．

### 从 LCT 的角度回顾一下树链剖分

-   对整棵树按子树大小进行剖分，并重新标号．
-   我们发现重新标号之后，在树上形成了一些以链为单位的连续区间，并且可以用线段树进行区间操作．

### 转向动态树问题

我们发现我们刚刚讲的树剖是以子树大小作为划分条件．那我们能不能重定义一种剖分，使它更适应我们的动态树问题呢？

考虑动态树问题需要什么链．

由于动态维护一个森林，显然我们希望这个链是我们指定的链，以便利用来求解．

## 实链剖分

对于一个点连向它所有儿子的边，我们自己选择一条边进行剖分，我们称被选择的边为实边，其他边则为虚边．对于实边，我们称它所连接的儿子为实儿子．对于一条由实边组成的链，我们同样称之为实链．请记住我们选择实链剖分的最重要的原因：它是我们选择的，灵活且可变．正是它的这种灵活可变性，我们采用 Splay Tree 来维护这些实链．

## LCT

我们可以简单的把 LCT 理解成用一些 Splay 来维护动态的树链剖分，以期实现动态树上的区间操作．对于每条实链，我们建一个 Splay 来维护整个链区间的信息．

## 辅助树

我们先来看一看辅助树的一些性质，再通过一张图实际了解一下辅助树的具体结构．

在本文里，你可以认为一些 Splay 构成了一个辅助树，每棵辅助树维护的是一棵树，一些辅助树构成了 LCT，其维护的是整个森林．

1.  辅助树由多棵 Splay 组成，每棵 Splay 维护原树中的一条路径，且中序遍历这棵 Splay 得到的点序列，从前到后对应原树「从上到下」的一条路径．
2.  原树每个节点与辅助树的 Splay 节点一一对应．
3.  辅助树的各棵 Splay 之间并不是独立的．每棵 Splay 的根节点的父亲节点本应是空，但在 LCT 中每棵 Splay 的根节点的父亲节点指向原树中 **这条链** 的父亲节点（即链最顶端的点的父亲节点）．这类父亲链接与通常 Splay 的父亲链接区别在于儿子认父亲，而父亲不认儿子，对应原树的一条 **虚边**．因此，每个连通块恰好有一个点的父亲节点为空．
4.  由于辅助树的以上性质，我们维护任何操作都不需要维护原树，辅助树可以在任何情况下拿出一个唯一的原树，我们只需要维护辅助树即可．

现在我们有一棵原树，如图所示．（加粗边是实边，虚线边是虚边．）

![tree](images/lct-atree-1.svg)

由刚刚的定义，辅助树的结构如图所示．

![auxtree](images/lct-atree-2.svg)

### 考虑原树和辅助树的结构关系

-   原树中的实链 : 在辅助树中节点都在一棵 Splay 中．
-   原树中的虚链 : 在辅助树中，子节点所在 Splay 的 Father 指向父节点，但是父节点的两个儿子都不指向子节点．
-   注意：原树的根不等于辅助树的根．
-   原树的 Father 指向不等于辅助树的 Father 指向．
-   辅助树是可以在满足辅助树、Splay 的性质下任意换根的．
-   虚实链变换可以轻松在辅助树上完成，这也就是实现了动态维护树链剖分．

### 接下来要用到的变量声明

-   `ch[N][2]` 左右儿子
-   `f[N]` 父亲指向
-   `sum[N]` 路径权值和
-   `val[N]` 点权
-   `tag[N]` 翻转标记
-   `laz[N]` 权值标记
-   `siz[N]` 辅助树上子树大小
-   Other\_Vars

### 函数声明

#### 一般数据结构函数（字面意思）

1.  `PushUp(x)`
2.  `PushDown(x)`

#### Splay 树的函数

下面是 Splay 树中用到的函数，具体可以查阅 [Splay 树](./splay.md)．

1.  `Get(x)` 获取 $x$ 是父亲的哪个儿子．
2.  `Splay(x)` 通过和 Rotate 操作联动实现把 $x$ 旋转到 **当前 Splay 的根**．
3.  `Rotate(x)` 将 $x$ 向上旋转一层的操作．

#### 新操作

1.  `Access(x)` 把从根到 $x$ 的所有点放在一条实链里，使根到 $x$ 成为一条实路径，并且在同一棵 Splay 里．**只有此操作是必须实现的，其他操作视题目而实现．**
2.  `IsRoot(x)` 判断 $x$ 是否是所在树的根．
3.  `Update(x)` 在 `Access` 操作之后，递归地从上到下 `PushDown` 更新信息．
4.  `MakeRoot(x)` 使 $x$ 点成为其所在树的根．
5.  `Link(x, y)` 在 $x, y$ 两点间连一条边．
6.  `Cut(x, y)` 把 $x, y$ 两点间边删掉．
7.  `Find(x)` 找到 $x$ 所在树的根节点编号．
8.  `Fix(x, v)` 修改 $x$ 的点权为 $v$．
9.  `Split(x, y)` 提取出 $x, y$ 间的路径，方便做区间操作．

### 宏定义

-   `#define ls ch[p][0]`
-   `#define rs ch[p][1]`

## 函数讲解

### `PushUp()`

```cpp
void PushUp(int p) {
  // maintain other variables
  siz[p] = siz[ls] + siz[rs] + 1;
}
```

### `PushDown()`

```cpp
void PushDown(int p) {
  if (tag[p] != std_tag) {
    // pushdown the tag
    tag[p] = std_tag;
  }
}
```

### `Splay() && Rotate()`

这里 `Splay()` 和 `Rotate()` 与 Splay 树的实现有些区别．

```cpp
#define Get(x) (ch[f[x]][1] == x)

void Rotate(int x) {
  int y = f[x], z = f[y], k = Get(x);
  if (!isRoot(y)) ch[z][ch[z][1] == y] = x;
  // 上面这句一定要写在前面，普通的 Splay 是不用的，因为 isRoot  (后面会讲)
  ch[y][k] = ch[x][!k], f[ch[x][!k]] = y;
  ch[x][!k] = y, f[y] = x, f[x] = z;
  PushUp(y), PushUp(x);
}

void Splay(int x) {
  Update(
      x);  // 马上就能看到啦．在 Splay 之前要把旋转会经过的路径上的点都 PushDown
  for (int fa; fa = f[x], !isRoot(x); Rotate(x)) {
    if (!isRoot(fa)) Rotate(Get(fa) == Get(x) ? fa : x);
  }
}
```

以上函数可以查阅 [Splay 树](./splay.md)．

下面是 LCT 独有的函数．

### `isRoot()`

```cpp
// 在前面我们已经说过，LCT 具有 如果一个儿子不是实儿子，他的父亲找不到它的性质
// 所以当一个点既不是它父亲的左儿子，又不是它父亲的右儿子，它就是当前 Splay 的根
#define isRoot(x) (ch[f[x]][0] != x && ch[f[x]][1] != x)
```

### `Access()`

```cpp
// Access 是 LCT
// 的核心操作，试想我们想求解一条路径，而这条路径恰好就是我们当前的一棵 Splay，
// 直接调用其信息即可．先来看一下代码，再结合图来看看过程
int Access(int x) {
  int p;
  for (p = 0; x; p = x, x = f[x]) {
    Splay(x), ch[x][1] = p, PushUp(x);
  }
  return p;
}
```

-   我们有这样一棵树，实线为实边，虚线为虚边．

    ![initial tree](images/lct-access-1.svg)

-   它的辅助树可能长成这样（构图方式不同可能 LCT 的结构也不同）．

    ![initial auxtree](images/lct-access-2.svg)

-   现在我们要 `Access(N)`，把 $A$ 到 $N$ 路径上的边都变为实边，拉成一棵 Splay．

    ![access tree](images/lct-access-3.svg)

-   实现的方法是从下到上逐步更新 Splay．

-   首先我们要把 $N$ 旋至当前 Splay 的根．

-   为了保证 AuxTree（辅助树）的性质，原来 $N$ 到 $O$ 的实边要更改为虚边．

-   由于认父不认子的性质，我们可以单方面的把 $N$ 的儿子改为 `NULL`．

-   于是原来的 AuxTree 就从下图变成了下下图．

    ![step 1 auxtree](images/lct-access-4.svg)

-   下一步，我们把 $N$ 指向的 Father $I$ 也旋转到 $I$ 的 Splay 树根．

-   原来的实边 $I$—$K$ 要去掉，这时候我们把 $I$ 的右儿子指向 $N$，就得到了 $I$—$L$ 这样一棵 Splay．

    ![step 2 auxtree](images/lct-access-5.svg)

-   接下来，按照刚刚的操作步骤，由于 $I$ 的 Father 指向 $H$，我们把 $H$ 旋转到他所在 Splay Tree 的根，然后把 $H$ 的 rs 设为 $I$．

-   之后的树是这样的．

    ![step 3 auxtree](images/lct-access-6.svg)

-   同理我们 `Splay(A)`，并把 $A$ 的右儿子指向 $H$．

-   于是我们得到了这样一棵 AuxTree．并且发现 $A$—$N$ 的整个路径已经在同一棵 Splay 中了．

    ![step final auxtree](images/lct-access-7.svg)

```cpp
// 回顾一下代码
int Access(int x) {
  int p;
  for (p = 0; x; p = x, x = f[x]) {
    Splay(x), ch[x][1] = p, PushUp(x);
  }
  return p;
}
```

我们发现 `Access()` 其实很容易，只有如下四步操作：

1.  把当前节点转到根．
2.  把儿子换成之前的节点．
3.  更新当前点的信息．
4.  把当前点换成当前点的父亲，继续操作．

这里提供的 Access 还有一个返回值．这个返回值相当于最后一次虚实链变换时虚边父亲节点的编号．该值有两个含义：

-   连续两次 Access 操作时，第二次 Access 操作的返回值等于这两个节点的 LCA.
-   表示 $x$ 到根的链所在的 Splay 树的根．这个节点一定已经被旋转到了根节点，且父亲一定为空．

### `Update()`

```cpp
// 从上到下一层一层 pushDown 即可
void Update(int p) {
  if (!isRoot(p)) Update(f[p]);
  pushDown(p);
}
```

### `makeRoot()`

-   `Make_Root()` 的重要性丝毫不亚于 `Access()`．我们在需要维护路径信息的时候，一定会出现路径深度无法严格递增的情况，根据 AuxTree 的性质，这种路径是不能出现在一棵 Splay 中的．
-   这时候我们需要用到 `Make_Root()`．
-   `Make_Root()` 的作用是使指定的点成为原树的根，考虑如何实现这种操作．
-   设 `Access(x)` 的返回值为 $y$，则此时 $x$ 到当前根的路径恰好构成一个 Splay，且该 Splay 的根为 $y$.
-   考虑将树用有向图表示出来，给每条边定一个方向，表示从儿子到父亲的方向．容易发现换根相当于将 $x$ 到根的路径的所有边反向（请仔细思考）．
-   因此将 $x$ 到当前根的路径翻转即可．
-   由于 $y$ 是 $x$ 到当前根的路径所代表的 Splay 的根，因此将以 $y$ 为根的 Splay 树进行区间翻转即可．

```cpp
void makeRoot(int p) {
  p = Access(p);
  swap(ch[p][0], ch[p][1]);
  tag[p] ^= 1;
}
```

### `Link()`

-   Link 两个点其实很简单，先 `Make_Root(x)`，然后把 $x$ 的父亲指向 $y$ 即可．显然，这个操作肯定不能发生在同一棵树内，所以记得先判一下．

```cpp
void Link(int x, int p) {
  makeRoot(x);
  splay(x);
  f[x] = p;
}
```

### `Split()`

-   `Split` 操作意义很简单，就是拿出一棵 Splay，维护的是 $x$ 到 $y$ 的路径．
-   先 `MakeRoot(x)`，然后 `Access(y)`．如果要 $y$ 做根，再 `Splay(y)`．
-   另外 Split 这三个操作可以直接把需要的路径拿出到 $y$ 的子树上，可以进行其他操作．

### `Cut()`

-   `Cut` 有两种情况，保证合法和不一定保证合法．
-   如果保证合法，直接 `Split(x, y)`，这时候 $y$ 是根，$x$ 一定是它的儿子，双向断开即可．就像这样：

```cpp
void Cut(int x, int p) { makeRoot(x), Access(p), Splay(p), ls = f[x] = 0; }
```

如果是不保证合法，我们需要判断一下是否有，这里选择使用 `map` 存一下，但是这里有一个利用性质的方法：

想要删边，必须要满足如下三个条件：

1.  $x,y$ 连通．
2.  $x,y$ 的路径上没有其他的链．
3.  $x$ 没有右儿子．

总结一下，上面三句话的意思就一个：$x,y$ 之间有边．

具体实现就留作一个思考题给大家．判断连通需要用到后面的 `Find`，其他两点稍作思考分析一下结构就知道该怎么判断了．

### `Find()`

-   `Find()` 查找的是 $x$ 所在的 **原树** 的根，请不要把原树根和辅助树根弄混．在 `Access(p)` 后，再 `Splay(p)`．这样根就是树里深度最小的那个，一直往左儿子走，沿途 `PushDown` 即可．
-   一直走到没有 ls，非常简单．
-   注意，每次查询之后需要把查询到的答案对应的结点 `Splay` 上去以保证复杂度．

```cpp
int Find(int p) {
  Access(p);
  Splay(p);
  pushDown(p);
  while (ls) p = ls, pushDown(p);
  Splay(p);
  return p;
}
```

### 注意事项

-   操作前一定要想一想需不需要 `PushUp` 或者 `PushDown`，LCT 由于特别灵活的原因，少 `Pushdown` 或者 `Pushup` 一次就可能把修改改到不该改的点上！
-   LCT 的 `Rotate` 和 Splay 的不太一样，`if (z)` 一定要放在前面．
-   LCT 的 `Splay` 操作就是旋转到根，没有旋转到谁儿子的操作，因为不需要．

## 时间复杂度

LCT 中的大部分操作都基于 `Access`，其余操作的时间复杂度都为常数，因此我们只需要分析 `Access` 操作的时间复杂度．

其中，`Access` 的时间复杂度主要来自于多次 splay 操作和对路径中虚边的访问，接下来分别分析这两部分的时间复杂度．

1.  splay

    -   定义 $w(x) = \log size(x)$，其中 $size(x)$ 表示以 $x$ 为根的所有虚边和实边的数量之和．

    -   定义势能函数 $\Phi = \sum_{x \in T} w(x)$，其中 $T$ 表示所有节点的集合．

    由 [Splay 的时间复杂度](./splay.md#时间复杂度) 分析易知，splay 操作的均摊时间复杂度为 $O(\log n)$．

2.  访问虚边

    参考 [重链剖分](../graph/hld.md#重链剖分)，定义两种虚边：

    -   **重虚边**：从节点 $v$ 到其父节点的虚边，其中 $size(v) > \frac{1}{2} size(parent(v))$．

    -   **轻虚边**：从节点 $v$ 到其父节点的虚边，其中 $size(v) \leq \frac{1}{2} size(parent(v))$．

    对于虚边的处理，可以使用势能分析，定义势能函数 $\Phi$ 为所有重虚边的数量，定义均摊成本 $c_i = t_i + \Delta \Phi_i$，其中 $t_i$ 为实际操作的成本，$\Delta \Phi_i$ 为势能的变化．

    -   走过重虚边后，会将重虚边转换为实边，该操作会减少 $1$ 的势能，因为它通过加强重要连接来优化树的结构．且由于其实际操作成本为 $O(1)$，抵消了势能的增加，故不会增加均摊成本，所有的均摊成本集中在轻虚边的处理上．

    -   每次 `Access` 操作最多遍历 $O(\log n)$ 条轻虚边，因此至多消耗 $O(\log n)$ 的实际操作成本，转化得到 $O(\log n)$ 条重虚边，即势能以 $O(\log n)$ 的代价增加．

    由此，最终访问虚边的均摊复杂度为实际操作成本和势能变化的和，即 $O(\log n)$．

综上所述，LCT 中 `Access` 操作的时间复杂度是 splay 和 虚边访问的复杂度之和，因此最后的均摊复杂度为 $O(\log n)$，即 n 个节点的 LCT，做 m 次 `Access` 操作的时间复杂度为 $O(n \log n + m \log n)$，从而基于 `Access` 操作的 `Cut`,`Link`,`Findroot` 等操作的均摊复杂度也为 $O(\log n)$．

## 习题

-   [「BZOJ 3282」Tree](https://hydro.ac/p/bzoj-P3282)
-   [「HNOI2010」弹飞绵羊](https://www.luogu.com.cn/problem/P3203)

## 维护树链信息

LCT 通过 `Split(x,y)` 操作，可以将树上从点 $x$ 到点 $y$ 的路径提取到以 $y$ 为根的 Splay 内，树链信息的修改和统计转化为平衡树上的操作，这使得 LCT 在维护树链信息上具有优势．此外，借助 LCT 实现的在树链上二分比树链剖分少一个 $O(\log n)$ 的复杂度．

???+ note "例题 [「国家集训队」Tree II](https://www.luogu.com.cn/problem/P1501)"
    给出一棵有 $n$ 个结点的树，每个点的初始权值为 $1$．$q$ 次操作，每次操作均为以下四种之一：
    
    1.  `- u1 v1 u2 v2`：将树上 $u_1,v_1$ 两点之间的边删除，连接 $u_2,v_2$ 两点，保证操作合法且连边后仍是一棵树．
    2.  `+ u v c`：将树上 $u,v$ 两点之间的路径上的点权都增加 $c$．
    3.  `* u v c`：将树上 $u,v$ 两点之间的路径上的点权都乘以 $c$．
    4.  `/ u v`：输出树上 $u,v$ 两点之间的路径上的点权之和对 $51061$ 取模后的值．
    
        $1\le n,q\le 10^5,0\le c\le 10^4$
    
        `-` 操作可以直接 `Cut(u1,v1),Link(u2,v2)`．

对树上 $u,v$ 两点之间的路径进行修改时，先 `Split(u,v)`．

此题要求进行在辅助树上的子树加，子树乘，子树求和操作，所以我们除了一般 LCT 需要维护的子树翻转标记，还要维护子树加法标记和子树乘法标记．处理标记的方法和在 Splay 上是一样的．

在打上和下传加法标记时，子树权值和的变化量和子树中的结点数有关，所以我们还要维护子树的大小 `siz`．

在下传标记时，需要注意顺序，先下传乘法标记再下传加法标记．子树翻转和子树加乘两种标记没有冲突．

??? note "参考代码"
    ```cpp
    #include <algorithm>
    #include <cstdio>
    #include <cstring>
    using namespace std;
    constexpr long long MAXN = 100010;
    constexpr long long mod = 51061;
    long long n, q, u, v, c;
    char op;
    
    struct Splay {
      long long ch[MAXN][2], fa[MAXN], siz[MAXN], val[MAXN], sum[MAXN], rev[MAXN],
          add[MAXN], mul[MAXN];
    
      void clear(long long x) {
        ch[x][0] = ch[x][1] = fa[x] = siz[x] = val[x] = sum[x] = rev[x] = add[x] =
            0;
        mul[x] = 1;
      }
    
      long long getch(long long x) { return (ch[fa[x]][1] == x); }
    
      long long isroot(long long x) {
        clear(0);
        return ch[fa[x]][0] != x && ch[fa[x]][1] != x;
      }
    
      void maintain(long long x) {
        clear(0);
        siz[x] = (siz[ch[x][0]] + 1 + siz[ch[x][1]]) % mod;
        sum[x] = (sum[ch[x][0]] + val[x] + sum[ch[x][1]]) % mod;
      }
    
      void pushdown(long long x) {
        clear(0);
        if (mul[x] != 1) {
          if (ch[x][0])
            mul[ch[x][0]] = (mul[x] * mul[ch[x][0]]) % mod,
            val[ch[x][0]] = (val[ch[x][0]] * mul[x]) % mod,
            sum[ch[x][0]] = (sum[ch[x][0]] * mul[x]) % mod,
            add[ch[x][0]] = (add[ch[x][0]] * mul[x]) % mod;
          if (ch[x][1])
            mul[ch[x][1]] = (mul[x] * mul[ch[x][1]]) % mod,
            val[ch[x][1]] = (val[ch[x][1]] * mul[x]) % mod,
            sum[ch[x][1]] = (sum[ch[x][1]] * mul[x]) % mod,
            add[ch[x][1]] = (add[ch[x][1]] * mul[x]) % mod;
          mul[x] = 1;
        }
        if (add[x]) {
          if (ch[x][0])
            add[ch[x][0]] = (add[ch[x][0]] + add[x]) % mod,
            val[ch[x][0]] = (val[ch[x][0]] + add[x]) % mod,
            sum[ch[x][0]] = (sum[ch[x][0]] + add[x] * siz[ch[x][0]] % mod) % mod;
          if (ch[x][1])
            add[ch[x][1]] = (add[ch[x][1]] + add[x]) % mod,
            val[ch[x][1]] = (val[ch[x][1]] + add[x]) % mod,
            sum[ch[x][1]] = (sum[ch[x][1]] + add[x] * siz[ch[x][1]] % mod) % mod;
          add[x] = 0;
        }
        if (rev[x]) {
          if (ch[x][0]) rev[ch[x][0]] ^= 1, swap(ch[ch[x][0]][0], ch[ch[x][0]][1]);
          if (ch[x][1]) rev[ch[x][1]] ^= 1, swap(ch[ch[x][1]][0], ch[ch[x][1]][1]);
          rev[x] = 0;
        }
      }
    
      void update(long long x) {
        if (!isroot(x)) update(fa[x]);
        pushdown(x);
      }
    
      void print(long long x) {
        if (!x) return;
        pushdown(x);
        print(ch[x][0]);
        printf("%lld ", x);
        print(ch[x][1]);
      }
    
      void rotate(long long x) {
        long long y = fa[x], z = fa[y], chx = getch(x), chy = getch(y);
        fa[x] = z;
        if (!isroot(y)) ch[z][chy] = x;
        ch[y][chx] = ch[x][chx ^ 1];
        fa[ch[x][chx ^ 1]] = y;
        ch[x][chx ^ 1] = y;
        fa[y] = x;
        maintain(y);
        maintain(x);
        maintain(z);
      }
    
      void splay(long long x) {
        update(x);
        for (long long f = fa[x]; f = fa[x], !isroot(x); rotate(x))
          if (!isroot(f)) rotate(getch(x) == getch(f) ? f : x);
      }
    
      void access(long long x) {
        for (long long f = 0; x; f = x, x = fa[x])
          splay(x), ch[x][1] = f, maintain(x);
      }
    
      void makeroot(long long x) {
        access(x);
        splay(x);
        swap(ch[x][0], ch[x][1]);
        rev[x] ^= 1;
      }
    
      long long find(long long x) {
        access(x);
        splay(x);
        while (ch[x][0]) x = ch[x][0];
        splay(x);
        return x;
      }
    } st;
    
    main() {
      scanf("%lld%lld", &n, &q);
      for (long long i = 1; i <= n; i++) st.val[i] = 1, st.maintain(i);
      for (long long i = 1; i < n; i++) {
        scanf("%lld%lld", &u, &v);
        if (st.find(u) != st.find(v)) st.makeroot(u), st.fa[u] = v;
      }
      while (q--) {
        scanf(" %c%lld%lld", &op, &u, &v);
        if (op == '+') {
          scanf("%lld", &c);
          st.makeroot(u), st.access(v), st.splay(v);
          st.val[v] = (st.val[v] + c) % mod;
          st.sum[v] = (st.sum[v] + st.siz[v] * c % mod) % mod;
          st.add[v] = (st.add[v] + c) % mod;
        }
        if (op == '-') {
          st.makeroot(u);
          st.access(v);
          st.splay(v);
          if (st.ch[v][0] == u && !st.ch[u][1]) st.ch[v][0] = st.fa[u] = 0;
          scanf("%lld%lld", &u, &v);
          if (st.find(u) != st.find(v)) st.makeroot(u), st.fa[u] = v;
        }
        if (op == '*') {
          scanf("%lld", &c);
          st.makeroot(u), st.access(v), st.splay(v);
          st.val[v] = st.val[v] * c % mod;
          st.sum[v] = st.sum[v] * c % mod;
          st.mul[v] = st.mul[v] * c % mod;
        }
        if (op == '/')
          st.makeroot(u), st.access(v), st.splay(v), printf("%lld\n", st.sum[v]);
      }
      return 0;
    }
    ```

### 习题

-   [luogu P3690【模板】Link Cut Tree（动态树）](https://www.luogu.com.cn/problem/P3690)
-   [「SDOI2011」染色](https://www.luogu.com.cn/problem/P2486)
-   [「SHOI2014」三叉神经树](https://loj.ac/problem/2187)

## 维护连通性质

### 判断是否连通

借助 LCT 的 `Find()` 函数，可以判断动态森林上的两点是否连通．如果有 `Find(x)==Find(y)`，则说明 $x,y$ 两点在一棵树上，相互连通．

???+ note "例题 [「SDOI2008」洞穴勘测](https://www.luogu.com.cn/problem/P2147)"
    一开始有 $n$ 个独立的点，$m$ 次操作．每次操作为以下之一：
    
    1.  `Connect u v`：在 $u,v$ 两点之间连接一条边．
    2.  `Destroy u v`：删除在 $u,v$ 两点之间的边，保证之前存在这样的一条边．
    3.  `Query u v`：询问 $u,v$ 两点是否连通．
    
    保证在任何时刻图的形态都是一个森林．
    
    $n\le 10^4, m\le 2\times 10^5$

??? note "参考代码"
    ```cpp
    #include <algorithm>
    #include <cstdio>
    #include <cstring>
    using namespace std;
    constexpr int MAXN = 10010;
    
    struct Splay {
      int ch[MAXN][2], fa[MAXN], tag[MAXN];
    
      void clear(int x) { ch[x][0] = ch[x][1] = fa[x] = tag[x] = 0; }
    
      int getch(int x) { return ch[fa[x]][1] == x; }
    
      int isroot(int x) { return ch[fa[x]][0] != x && ch[fa[x]][1] != x; }
    
      void pushdown(int x) {
        if (tag[x]) {
          if (ch[x][0]) swap(ch[ch[x][0]][0], ch[ch[x][0]][1]), tag[ch[x][0]] ^= 1;
          if (ch[x][1]) swap(ch[ch[x][1]][0], ch[ch[x][1]][1]), tag[ch[x][1]] ^= 1;
          tag[x] = 0;
        }
      }
    
      void update(int x) {
        if (!isroot(x)) update(fa[x]);
        pushdown(x);
      }
    
      void rotate(int x) {
        int y = fa[x], z = fa[y], chx = getch(x), chy = getch(y);
        fa[x] = z;
        if (!isroot(y)) ch[z][chy] = x;
        ch[y][chx] = ch[x][chx ^ 1];
        fa[ch[x][chx ^ 1]] = y;
        ch[x][chx ^ 1] = y;
        fa[y] = x;
      }
    
      void splay(int x) {
        update(x);
        for (int f = fa[x]; f = fa[x], !isroot(x); rotate(x))
          if (!isroot(f)) rotate(getch(x) == getch(f) ? f : x);
      }
    
      void access(int x) {
        for (int f = 0; x; f = x, x = fa[x]) splay(x), ch[x][1] = f;
      }
    
      void makeroot(int x) {
        access(x);
        splay(x);
        swap(ch[x][0], ch[x][1]);
        tag[x] ^= 1;
      }
    
      int find(int x) {
        access(x);
        splay(x);
        while (ch[x][0]) x = ch[x][0];
        splay(x);
        return x;
      }
    } st;
    
    int n, q, x, y;
    char op[MAXN];
    
    int main() {
      scanf("%d%d", &n, &q);
      while (q--) {
        scanf("%s%d%d", op, &x, &y);
        if (op[0] == 'Q') {
          if (st.find(x) == st.find(y))
            printf("Yes\n");
          else
            printf("No\n");
        }
        if (op[0] == 'C')
          if (st.find(x) != st.find(y)) st.makeroot(x), st.fa[x] = y;
        if (op[0] == 'D') {
          st.makeroot(x);
          st.access(y);
          st.splay(y);
          if (st.ch[y][0] == x && !st.ch[x][1]) st.ch[y][0] = st.fa[x] = 0;
        }
      }
      return 0;
    }
    ```

### 维护边双连通分量

如果要求将边双连通分量缩成点，每次添加一条边，所连接的树上的两点如果相互连通，那么这条路径上的所有点都会被缩成一个点．

???+ note "例题 [「AHOI2005」航线规划](https://www.luogu.com.cn/problem/P2542)"
    给出 $n$ 个点，初始时有 $m$ 条无向边，$q$ 次操作，每次操作为以下之一：
    
    1.  `0 u v`：删除 $u,v$ 之间的连边，保证此时存在这样的一条边．
    2.  `1 u v`：查询此时 $u,v$ 两点之间可能的所有路径必须经过的边的数量．
    
    保证图在任意时刻都连通．
    
    $1<n<3\times 10^4,1<m<10^5,0\le q\le 4\times 10^4$

可以发现，$u,v$ 两点之间的所有可能路径必须经过的边的数量为将所有边双连通分量缩成点之后 $u$ 所在点和 $v$ 所在点之间的路径上的结点数 $-1$．

由于题目中的删边操作不好进行，我们考虑离线逆向进行操作，改删边为加边．

加入一条边时，如果两点原来不连通，则在 LCT 上连接两点；否则提取出加这条边之前 LCT 上这两点之间的路径，遍历辅助树上的这个子树，相当于遍历了这条路径，将这些点合并，利用并查集维护合并的信息．

用合并后并查集的代表元素代替原来树上的路径．注意之后的每次操作都要找到操作点在并查集上的代表元素进行操作．

??? note "参考代码"
    ```cpp
    #include <algorithm>
    #include <cstdio>
    #include <cstring>
    #include <map>
    using namespace std;
    constexpr int MAXN = 200010;
    int f[MAXN];
    
    int findp(int x) { return f[x] ? f[x] = findp(f[x]) : x; }
    
    void merge(int x, int y) {
      x = findp(x);
      y = findp(y);
      if (x != y) f[x] = y;
    }
    
    struct Splay {
      int ch[MAXN][2], fa[MAXN], tag[MAXN], siz[MAXN];
    
      void clear(int x) { ch[x][0] = ch[x][1] = fa[x] = tag[x] = siz[x] = 0; }
    
      int getch(int x) { return ch[findp(fa[x])][1] == x; }
    
      int isroot(int x) {
        return ch[findp(fa[x])][0] != x && ch[findp(fa[x])][1] != x;
      }
    
      void maintain(int x) {
        clear(0);
        if (x) siz[x] = siz[ch[x][0]] + 1 + siz[ch[x][1]];
      }
    
      void pushdown(int x) {
        if (tag[x]) {
          if (ch[x][0]) tag[ch[x][0]] ^= 1, swap(ch[ch[x][0]][0], ch[ch[x][0]][1]);
          if (ch[x][1]) tag[ch[x][1]] ^= 1, swap(ch[ch[x][1]][0], ch[ch[x][1]][1]);
          tag[x] = 0;
        }
      }
    
      void print(int x) {
        if (!x) return;
        pushdown(x);
        print(ch[x][0]);
        printf("%d ", x);
        print(ch[x][1]);
      }
    
      void update(int x) {
        if (!isroot(x)) update(findp(fa[x]));
        pushdown(x);
      }
    
      void rotate(int x) {
        x = findp(x);
        int y = findp(fa[x]), z = findp(fa[y]), chx = getch(x), chy = getch(y);
        fa[x] = z;
        if (!isroot(y)) ch[z][chy] = x;
        ch[y][chx] = ch[x][chx ^ 1];
        fa[ch[x][chx ^ 1]] = y;
        ch[x][chx ^ 1] = y;
        fa[y] = x;
        maintain(y);
        maintain(x);
        if (z) maintain(z);
      }
    
      void splay(int x) {
        x = findp(x);
        update(x);
        for (int f = findp(fa[x]); f = findp(fa[x]), !isroot(x); rotate(x))
          if (!isroot(f)) rotate(getch(x) == getch(f) ? f : x);
      }
    
      void access(int x) {
        for (int f = 0; x; f = x, x = findp(fa[x]))
          splay(x), ch[x][1] = f, maintain(x);
      }
    
      void makeroot(int x) {
        x = findp(x);
        access(x);
        splay(x);
        tag[x] ^= 1;
        swap(ch[x][0], ch[x][1]);
      }
    
      int find(int x) {
        x = findp(x);
        access(x);
        splay(x);
        while (ch[x][0]) x = ch[x][0];
        splay(x);
        return x;
      }
    
      void dfs(int x) {
        pushdown(x);
        if (ch[x][0]) dfs(ch[x][0]), merge(ch[x][0], x);
        if (ch[x][1]) dfs(ch[x][1]), merge(ch[x][1], x);
      }
    } st;
    
    int n, m, q, x, y, cur, ans[MAXN];
    
    struct oper {
      int op, a, b;
    } s[MAXN];
    
    map<pair<int, int>, int> mp;
    
    int main() {
      scanf("%d%d", &n, &m);
      for (int i = 1; i <= n; i++) st.maintain(i);
      for (int i = 1; i <= m; i++)
        scanf("%d%d", &x, &y), mp[{x, y}] = mp[{y, x}] = 1;
      while (scanf("%d", &s[++q].op)) {
        if (s[q].op == -1) {
          q--;
          break;
        }
        scanf("%d%d", &s[q].a, &s[q].b);
        if (!s[q].op) mp[{s[q].a, s[q].b}] = mp[{s[q].b, s[q].a}] = 0;
      }
      reverse(s + 1, s + q + 1);
      for (map<pair<int, int>, int>::iterator it = mp.begin(); it != mp.end(); it++)
        if (it->second) {
          mp[{it->first.second, it->first.first}] = 0;
          x = findp(it->first.first);
          y = findp(it->first.second);
          if (st.find(x) != st.find(y))
            st.makeroot(x), st.fa[x] = y;
          else {
            if (x == y) continue;
            st.makeroot(x);
            st.access(y);
            st.splay(y);
            st.dfs(y);
            int t = findp(y);
            st.fa[t] = findp(st.fa[y]);
            st.ch[t][0] = st.ch[t][1] = 0;
            st.maintain(t);
          }
        }
      for (int i = 1; i <= q; i++) {
        if (s[i].op == 0) {
          x = findp(s[i].a);
          y = findp(s[i].b);
          st.makeroot(x);
          st.access(y);
          st.splay(y);
          st.dfs(y);
          int t = findp(y);
          st.fa[t] = st.fa[y];
          st.ch[t][0] = st.ch[t][1] = 0;
          st.maintain(t);
        }
        if (s[i].op == 1) {
          x = findp(s[i].a);
          y = findp(s[i].b);
          st.makeroot(x);
          st.access(y);
          st.splay(y);
          ans[++cur] = st.siz[y] - 1;
        }
      }
      for (int i = cur; i >= 1; i--) printf("%d\n", ans[i]);
      return 0;
    }
    ```

### 习题

-   [洛谷 P3950 部落冲突](https://www.luogu.com.cn/problem/P3950)
-   [BZOJ 4998 星球联盟](https://hydro.ac/p/bzoj-P4998)
-   [BZOJ 2959 长跑](https://hydro.ac/p/bzoj-P2959)

## 维护边权

LCT 并不能直接处理边权，此时需要对每条边建立一个对应点，方便查询链上的边信息．利用这一技巧可以动态维护生成树．

???+ note "例题 [luogu P4234 最小差值生成树](https://www.luogu.com.cn/problem/P4234)"
    给定一个 $n$ 个点，$m$ 条边的带权无向图，求其边权最大值和边权最小值的差值最小的生成树，输出这个差值．
    
    数据保证至少存在一棵生成树．
    
    $1\le n\le 5\times 10^4,1\le m\le 2\times 10^5,1\le w_i\le 10^4$

将边按照边权从小到大排序，枚举选择的最右边的一条边，要得到最优解，需要使边权最小边的边权最大．

每次按照顺序添加边，如果将要连接的这两个点已经连通，则删除这两点之间边权最小的一条边．如果整个图已经连通成了一棵树，则用当前边权减去最小边权更新答案．最小边权可用双指针法更新．

LCT 上没有固定的父子关系，所以不能将边权记录在点权中．

记录树链上的边的信息，可以使用 **拆边**．对每条边建立一个对应的点，从这条边向其两个端点连接一条边，原先的连边与删边操作都变成两次操作．

??? note "参考代码"
    ```cpp
    #include <algorithm>
    #include <cstdio>
    #include <cstring>
    #include <set>
    using namespace std;
    constexpr int MAXN = 5000010;
    
    struct Splay {
      int ch[MAXN][2], fa[MAXN], tag[MAXN], val[MAXN], minn[MAXN];
    
      void clear(int x) {
        ch[x][0] = ch[x][1] = fa[x] = tag[x] = val[x] = minn[x] = 0;
      }
    
      int getch(int x) { return ch[fa[x]][1] == x; }
    
      int isroot(int x) { return ch[fa[x]][0] != x && ch[fa[x]][1] != x; }
    
      void maintain(int x) {
        if (!x) return;
        minn[x] = x;
        if (ch[x][0]) {
          if (val[minn[ch[x][0]]] < val[minn[x]]) minn[x] = minn[ch[x][0]];
        }
        if (ch[x][1]) {
          if (val[minn[ch[x][1]]] < val[minn[x]]) minn[x] = minn[ch[x][1]];
        }
      }
    
      void pushdown(int x) {
        if (tag[x]) {
          if (ch[x][0]) tag[ch[x][0]] ^= 1, swap(ch[ch[x][0]][0], ch[ch[x][0]][1]);
          if (ch[x][1]) tag[ch[x][1]] ^= 1, swap(ch[ch[x][1]][0], ch[ch[x][1]][1]);
          tag[x] = 0;
        }
      }
    
      void update(int x) {
        if (!isroot(x)) update(fa[x]);
        pushdown(x);
      }
    
      void print(int x) {
        if (!x) return;
        pushdown(x);
        print(ch[x][0]);
        printf("%d ", x);
        print(ch[x][1]);
      }
    
      void rotate(int x) {
        int y = fa[x], z = fa[y], chx = getch(x), chy = getch(y);
        fa[x] = z;
        if (!isroot(y)) ch[z][chy] = x;
        ch[y][chx] = ch[x][chx ^ 1];
        fa[ch[x][chx ^ 1]] = y;
        ch[x][chx ^ 1] = y;
        fa[y] = x;
        maintain(y);
        maintain(x);
        if (z) maintain(z);
      }
    
      void splay(int x) {
        update(x);
        for (int f = fa[x]; f = fa[x], !isroot(x); rotate(x))
          if (!isroot(f)) rotate(getch(x) == getch(f) ? f : x);
      }
    
      void access(int x) {
        for (int f = 0; x; f = x, x = fa[x]) splay(x), ch[x][1] = f, maintain(x);
      }
    
      void makeroot(int x) {
        access(x);
        splay(x);
        tag[x] ^= 1;
        swap(ch[x][0], ch[x][1]);
      }
    
      int find(int x) {
        access(x);
        splay(x);
        while (ch[x][0]) x = ch[x][0];
        splay(x);
        return x;
      }
    
      void link(int x, int y) {
        makeroot(x);
        fa[x] = y;
      }
    
      void cut(int x, int y) {
        makeroot(x);
        access(y);
        splay(y);
        ch[y][0] = fa[x] = 0;
        maintain(y);
      }
    } st;
    
    constexpr int inf = 2e9 + 1;
    int n, m, ans, nww, x, y;
    
    struct Edge {
      int u, v, w;
    
      bool operator<(Edge x) const { return w < x.w; };
    } s[MAXN];
    
    multiset<int> mp;
    
    int main() {
      scanf("%d%d", &n, &m);
      for (int i = 1; i <= n; i++) st.val[i] = inf, st.maintain(i);
      for (int i = 1; i <= m; i++) scanf("%d%d%d", &s[i].u, &s[i].v, &s[i].w);
      sort(s + 1, s + m + 1);
      for (int i = 1; i <= m; i++) st.val[n + i] = s[i].w, st.maintain(n + i);
      for (int i = 1; i <= m; i++) {
        x = s[i].u;
        y = s[i].v;
        if (x == y) continue;
        if (st.find(x) != st.find(y)) {
          nww++;
          st.link(x, n + i);
          st.link(n + i, y);
          mp.insert(s[i].w);
          if (nww == n - 1) ans = s[i].w - (*(mp.begin()++));
        } else {
          st.makeroot(x);
          st.access(y);
          st.splay(y);
          int t = st.minn[y] - n;
          st.cut(s[t].u, t + n);
          st.cut(t + n, s[t].v);
          mp.erase(mp.find(s[t].w));
          st.link(x, n + i);
          st.link(n + i, y);
          mp.insert(s[i].w);
          if (nww == n - 1) ans = min(ans, s[i].w - (*(mp.begin()++)));
        }
      }
      printf("%d\n", ans);
      return 0;
    }
    ```

### 习题

-   [「WC2006」水管局长](https://www.luogu.com.cn/problem/P4172)
-   [「BJWC2010」严格次小生成树](https://www.luogu.com.cn/problem/P4180)
-   [「NOI2014」魔法森林](https://uoj.ac/problem/3)

## 维护子树信息

LCT 不擅长维护子树信息．统计一个结点所有虚子树的信息，就可以求得整棵树的信息．

???+ note "例题 [「BJOI2014」大融合](https://loj.ac/problem/2230)"
    给定 $n$ 个结点和 $q$ 次操作，每个操作为如下形式：
    
    1.  `A x y` 在结点 $x$ 和 $y$ 之间连接一条边．
    2.  `Q x y` 给定一条已经存在的边 $(x,y)$，求有多少条简单路径，其中包含边 $(x,y)$．
    
    保证在任意时刻，图的形态都是一棵森林．
    
    $1\le n,q,x,y\le 10^5$

为询问 `Q` 考虑另一种表述，我们发现答案等于边 $(x,y)$ 在 $x$ 侧的结点数与 $y$ 侧的结点数的乘积，即将边 $(x,y)$ 断开后分别包含 $x$ 和 $y$ 的树的结点数．为了消除断边的影响，在询问后我们再次连接边 $(x,y)$．

题目中的操作既有连边，又有删边，还保证在任意时刻都是一棵森林，我们不由得想到用 LCT 来维护．但是这题中 LCT 维护的是子树的大小，不像我们印象中的维护一条链的信息，而 LCT 的构造 **认父不认子**，不方便我们直接进行子树的统计．怎么办呢？

方法是统计一个结点 $x$ 所有虚儿子（即父亲为 $x$，但 $x$ 在 Splay 中的左右儿子并不包含它）所代表的子树的贡献．

定义 $siz2[x]$ 为结点 $x$ 的所有虚儿子代表的子树的结点数，$siz[x]$ 为 结点 $x$ 子树中的结点数．

不同于以往我们维护 Splay 中子树结点个数的方法，我们在计算结点 $x$ 子树中的结点数时，还要加上 $siz2[x]$，即

```cpp
void maintain(int x) {
  clear(0);
  if (x) siz[x] = siz[ch[x][0]] + 1 + siz[ch[x][1]] + siz2[x];
}
```

而且在我们 **改变 Splay 的形态**（即改变一个结点在 Splay 上的左右儿子指向时），需要及时修改 $siz2[x]$ 的值．

在 `Rotate(),Splay()` 操作中，我们都只是改变了 Splay 中结点的相对位置，没有改变任意一条边的虚实情况，所以不对 $siz2[x]$ 进行任何修改．

在 `access` 操作中，在每次 splay 完后，都会改变刚刚 splay 完的结点的右儿子，即该结点与其原右儿子的连边和该节点和新右儿子的连边的虚实情况发生了变化，我们需要加上新变成虚边所连的子树的贡献，减去刚刚变成实边所连的子树的贡献．代码如下：

```cpp
void access(int x) {
  for (int f = 0; x; f = x, x = fa[x])
    splay(x), siz2[x] += siz[ch[x][1]] - siz[f], ch[x][1] = f, maintain(x);
}
```

在 `MakeRoot(),Find()` 操作中，我们都只是调用了之前的函数或者在 Splay 上条边，并不用做任何修改．

在连接两点时，我们修改了一个结点的父亲．我们需要在父亲结点的 $siz2$ 值中加上新子结点的子树大小贡献．

```cpp
st.makeroot(x);
st.makeroot(y);
st.fa[x] = y;
st.siz2[y] += st.siz[x];
```

在断开一条边时，我们只是删除了 Splay 上的一条实边，`Maintain` 操作会维护这些信息，不需要做任何修改．

以上是代码修改的细节，最后总结一下 LCT 维护子树信息的要求与方法：

1.  维护的信息要有 **可减性**，如子树结点数，子树权值和，但不能直接维护子树最大最小值，因为在将一条虚边变成实边时要排除原先虚边的贡献．
2.  新建一个附加值存储虚子树的贡献，在统计时将其加入本结点答案，在改变边的虚实时及时维护．
3.  其余部分同普通 LCT，在统计子树信息时一定将其作为根节点．
4.  如果维护的信息没有可减性，如维护区间最值，可以对每个结点开一个平衡树维护结点的虚子树中的最值．

??? note "参考代码"
    ```cpp
    #include <algorithm>
    #include <cstdio>
    #include <cstring>
    using namespace std;
    constexpr int MAXN = 100010;
    using ll = long long;
    
    struct Splay {
      int ch[MAXN][2], fa[MAXN], siz[MAXN], siz2[MAXN], tag[MAXN];
    
      void clear(int x) {
        ch[x][0] = ch[x][1] = fa[x] = siz[x] = siz2[x] = tag[x] = 0;
      }
    
      int getch(int x) { return ch[fa[x]][1] == x; }
    
      int isroot(int x) { return ch[fa[x]][0] != x && ch[fa[x]][1] != x; }
    
      void maintain(int x) {
        clear(0);
        if (x) siz[x] = siz[ch[x][0]] + 1 + siz[ch[x][1]] + siz2[x];
      }
    
      void pushdown(int x) {
        if (tag[x]) {
          if (ch[x][0]) swap(ch[ch[x][0]][0], ch[ch[x][0]][1]), tag[ch[x][0]] ^= 1;
          if (ch[x][1]) swap(ch[ch[x][1]][0], ch[ch[x][1]][1]), tag[ch[x][1]] ^= 1;
          tag[x] = 0;
        }
      }
    
      void update(int x) {
        if (!isroot(x)) update(fa[x]);
        pushdown(x);
      }
    
      void rotate(int x) {
        int y = fa[x], z = fa[y], chx = getch(x), chy = getch(y);
        fa[x] = z;
        if (!isroot(y)) ch[z][chy] = x;
        ch[y][chx] = ch[x][chx ^ 1];
        fa[ch[x][chx ^ 1]] = y;
        ch[x][chx ^ 1] = y;
        fa[y] = x;
        maintain(y);
        maintain(x);
        maintain(z);
      }
    
      void splay(int x) {
        update(x);
        for (int f = fa[x]; f = fa[x], !isroot(x); rotate(x))
          if (!isroot(f)) rotate(getch(x) == getch(f) ? f : x);
      }
    
      void access(int x) {
        for (int f = 0; x; f = x, x = fa[x])
          splay(x), siz2[x] += siz[ch[x][1]] - siz[f], ch[x][1] = f, maintain(x);
      }
    
      void makeroot(int x) {
        access(x);
        splay(x);
        swap(ch[x][0], ch[x][1]);
        tag[x] ^= 1;
      }
    
      int find(int x) {
        access(x);
        splay(x);
        while (ch[x][0]) x = ch[x][0];
        splay(x);
        return x;
      }
    } st;
    
    int n, q, x, y;
    char op;
    
    int main() {
      scanf("%d%d", &n, &q);
      while (q--) {
        scanf(" %c%d%d", &op, &x, &y);
        if (op == 'A') {
          st.makeroot(x);
          st.makeroot(y);
          st.fa[x] = y;
          st.siz2[y] += st.siz[x];
        }
        if (op == 'Q') {
          st.makeroot(x);
          st.access(y);
          st.splay(y);
          st.ch[y][0] = st.fa[x] = 0;
          st.maintain(x);
          st.makeroot(x);
          st.makeroot(y);
          printf("%lld\n", (ll)(st.siz[x] * st.siz[y]));
          st.makeroot(x);
          st.makeroot(y);
          st.fa[x] = y;
          st.siz2[y] += st.siz[x];
        }
      }
      return 0;
    }
    ```

### 习题

-   [luogu P4299 首都](https://www.luogu.com.cn/problem/P4299)
-   [SPOJ QTREE5 - Query on a tree V](https://www.spoj.com/problems/QTREE5)


## ds/leftist-tree.md

author: JiZiQian, llleixx, firefly-zjyjoe

## 什么是左偏树？

**左偏树** 与 [**配对堆**](./pairing-heap.md) 一样，是一种 **可并堆**，具有堆的性质，并且可以快速合并．

## 左偏树的定义和性质

对于一棵二叉树，我们定义 **外节点** 为子节点数小于两个的节点，定义一个节点的 $\mathrm{dist}$ 为其到子树中最近的外节点所经过的边的数量．空节点的 $\mathrm{dist}$ 为 $0$．

???+ note "注意"
    有些资料中对 $\mathrm{dist}$ 的定义是本文中的 $\mathrm{dist}$ 减 $1$，这样定义是因为代码编写时可以省略一些判空流程，但需要注意应预先置空节点的 $\mathrm{dist}$ 为 $-1$．本文中所有代码对 $\mathrm{dist}$ 的定义 **均为空节点 $\mathrm{dist}$ 为 $-1$ 的定义**，请注意与行文间 $\mathrm{dist}$ 定义的差别．

左偏树是一棵二叉树，它不仅具有堆的性质，并且是「左偏」的：每个节点左儿子的 $\mathrm{dist}$ 都大于等于右儿子的 $\mathrm{dist}$．

因此，左偏树每个节点的 $\mathrm{dist}$ 都等于其右儿子的 $\mathrm{dist}$ 加一．

需要注意的是，$\mathrm{dist}$ 不是深度，**左偏树的深度没有保证**，一条向左的链也符合左偏树的定义．

## 核心操作：合并（merge）

合并两个堆时，由于要满足堆性质，先取值较小（为了方便，本文讨论小根堆）的那个根作为合并后堆的根节点，然后将这个根的左儿子作为合并后堆的左儿子，递归地合并其右儿子与另一个堆，作为合并后的堆的右儿子．为了满足左偏性质，合并后若左儿子的 $\mathrm{dist}$ 小于右儿子的 $\mathrm{dist}$，就交换两个儿子．

参考代码：

???+ note "实现"
    ```cpp
    int merge(int x, int y) {
      if (!x || !y) return x | y;  // 若一个堆为空则返回另一个堆
      if (t[x].val > t[y].val) swap(x, y);  // 取值较小的作为根
      t[x].rs = merge(t[x].rs, y);          // 递归合并右儿子与另一个堆
      if (t[t[x].rs].d > t[t[x].ls].d)
        swap(t[x].ls, t[x].rs);   // 若不满足左偏性质则交换左右儿子
      t[x].d = t[t[x].rs].d + 1;  // 更新dist
      return x;
    }
    ```

由于左偏性质，每递归一层，其中一个堆根节点的 $\mathrm{dist}$ 就会减小 $1$，而一棵有 $n$ 个节点的二叉树，根的 $\mathrm{dist}$ 不超过 $\left\lceil\log (n+1)\right\rceil$，所以合并两个大小分别为 $n$ 和 $m$ 的堆复杂度是 $O(\log n+\log m)$．

???+ note "关于 $\mathrm{dist}$ 性质的证明"
    一棵根的 $\mathrm{dist}$ 为 $x$ 的二叉树至少有 $x-1$ 层是满二叉树，那么就至少有 $2^x-1$ 个节点．注意这个性质是所有二叉树都具有的，并不是左偏树所特有的．

左偏树还有一种无需交换左右儿子的写法：将 $\mathrm{dist}$ 较大的儿子视作左儿子，$\mathrm{dist}$ 较小的儿子视作右儿子：

???+ note "实现"
    ```cpp
    int& rs(int x) { return t[x].ch[t[t[x].ch[1]].d < t[t[x].ch[0]].d]; }
    
    int merge(int x, int y) {
      if (!x || !y) return x | y;
      if (t[x].val < t[y].val) swap(x, y);
      int& rs_ref = rs(x);
      rs_ref = merge(rs_ref, y);
      t[x].d = t[rs(x)].d + 1;
      return x;
    }
    ```

## 左偏树的其它操作

### 插入节点

单个节点也可以视为一个堆，合并即可．

### 删除根

合并根的左右儿子即可．

### 删除任意节点

#### 做法

先将左右儿子合并，然后自底向上更新 $\mathrm{dist}$、不满足左偏性质时交换左右儿子，当 $\mathrm{dist}$ 无需更新时结束递归：

???+ note "实现"
    ```cpp
    int& rs(int x) { return t[x].ch[t[t[x].ch[1]].d < t[t[x].ch[0]].d]; }
    
    // 有了 pushup，直接 merge 左右儿子就实现了删除节点并保持左偏性质
    int merge(int x, int y) {
      if (!x || !y) return x | y;
      if (t[x].val < t[y].val) swap(x, y);
      int& rs_ref = rs(x);
      rs_ref = merge(rs_ref, y);
      t[rs_ref].fa = x;
      t[x].d = t[rs(x)].d + 1;
      return x;
    }
    
    void pushup(int x) {
      if (!x) return;
      if (t[x].d != t[rs(x)].d + 1) {
        t[x].d = t[rs(x)].d + 1;
        pushup(t[x].fa);
      }
    }
    
    void erase(int x) {
      int y = merge(t[x].ch[0], t[x].ch[1]);
      t[y].fa = t[x].fa;
      if (t[t[x].fa].ch[0] == x)
        t[t[x].fa].ch[0] = y;
      else if (t[t[x].fa].ch[1] == x)
        t[t[x].fa].ch[1] = y;
      pushup(t[y].fa);
    }
    ```

#### 复杂度证明

先考虑 `merge` 的过程，每次都会使 $x$ 或 $y$ 向下一层，也就是说最极端的情况，就是一直选择左偏树的右节点（$\mathrm{dist}$ 最小的节点）向下一层，此时 $\mathrm{dist}$ 减少了 $1$．

再考虑 `pushup` 的过程，我们令当前 `pushup` 的这个节点为 $x$，其父亲为 $y$，一个节点的「初始 $\mathrm{dist}$」为它在 `pushup` 前的 $\mathrm{dist}$．从被删除节点的父亲开始递归，有两种情况：

1.  $x$ 是 $y$ 的右儿子，此时 $y$ 的初始 $\mathrm{dist}$ 为 $x$ 的初始 $\mathrm{dist}$ 加一．
2.  $x$ 是 $y$ 的左儿子，由于节点的 $\mathrm{dist}$ 最多减一，因此只有 $y$ 的左右儿子初始 $\mathrm{dist}$ 相等时（此时左儿子 $\mathrm{dist}$ 减一会导致左右儿子互换）才会继续递归下去，因此 $y$ 的初始 $\mathrm{dist}$ 仍然是 $x$ 的初始 $\mathrm{dist}$ 加一．

所以，我们得到，每递归一层 $x$ 的初始 $\mathrm{dist}$ 就会加一，因此最多递归 $O(\log n)$ 层．

### 整个堆加上/减去一个值、乘上一个正数

其实可以打标记且不改变相对大小的操作都可以．

在根打上标记，删除根/合并堆（访问儿子）时下传标记即可：

???+ note "实现"
    ```cpp
    int merge(int x, int y) {
      if (!x || !y) return x | y;
      if (t[x].val > t[y].val) swap(x, y);
      pushdown(x);
      t[x].rs = merge(t[x].rs, y);
      if (t[t[x].rs].d > t[t[x].ls].d) swap(t[x].ls, t[x].rs);
      t[x].d = t[t[x].rs].d + 1;
      return x;
    }
    
    int pop(int x) {
      pushdown(x);
      return merge(t[x].ls, t[x].rs);
    }
    ```

## 其他可并堆

### 随机堆

???+ note "实现"
    ```cpp
    int merge(int x, int y) {
      if (!x || !y) return x | y;
      if (t[y].val < t[x].val) swap(x, y);
      if (rand() & 1)  // 随机选择是否交换左右子节点
        swap(t[x].ls, t[x].rs);
      t[x].ls = merge(t[x].ls, y);
      return x;
    }
    ```

可以看到该实现方法唯一不同之处便是采用了随机数来实现合并，这样一来便可以省去 $\mathrm{dist}$ 的相关计算．且平均时间复杂度亦为 $O(\log n)$，详细证明可参考 [Randomized Heap](https://cp-algorithms.com/data_structures/randomized_heap.html)．

### 斜堆

斜堆是左偏树的自适应形式．当合并两个堆时，它无条件交换合并路径上的所有节点，以此试图维护平衡．根据均摊分析，自顶向下斜堆（top-down skew heap）插入，合并，删除最小值的复杂度为 $O(\log n)$[^ref1]．

## 例题

### 模板题

[luogu P3377【模板】左偏树（可并堆）](https://www.luogu.com.cn/problem/P3377)

[Monkey King](https://www.luogu.com.cn/problem/P1456)

[罗马游戏](https://www.luogu.com.cn/problem/P2713)

需要注意的是：

1.  合并前要检查是否已经在同一堆中．

2.  左偏树的深度可能达到 $O(n)$，因此找一个点所在的堆顶要用并查集维护，不能直接暴力跳父亲．（虽然很多题数据水，暴力跳父亲可以过……）（用并查集维护根时要保证原根指向新根，新根指向自己．）

??? note "罗马游戏参考代码"
    ```cpp
    --8<-- "docs/ds/code/leftist-tree/leftist-tree_1.cpp"
    ```

### 树上问题

[「APIO2012」派遣](https://www.luogu.com.cn/problem/P1552)

[「JLOI2015」城池攻占](https://loj.ac/problem/2107)

这类题目往往是每个节点维护一个堆，与儿子合并，依题意弹出、修改、计算答案，有点像线段树合并的类似题目．

??? note "城池攻占参考代码"
    ```cpp
    --8<-- "docs/ds/code/leftist-tree/leftist-tree_2.cpp"
    ```

### [「SCOI2011」棘手的操作](https://loj.ac/problem/2441)

首先，找一个节点所在堆的堆顶要用并查集，而不能暴力向上跳．

再考虑单点查询，若用普通的方法打标记，就得查询点到根路径上的标记之和，最坏情况下可以达到 $O(n)$ 的复杂度．如果只有堆顶有标记，就可以快速地查询了，但如何做到呢？

可以用类似启发式合并的方式，每次合并的时候把较小的那个堆标记暴力下传到每个节点，然后把较大的堆的标记作为合并后的堆的标记．由于合并后有另一个堆的标记，所以较小的堆下传标记时要下传其标记减去另一个堆的标记．由于每个节点每被合并一次所在堆的大小至少乘二，所以每个节点最多被下放 $O(\log n)$ 次标记，暴力下放标记的总复杂度就是 $O(n\log n)$．

再考虑单点加，先删除，再更新，最后插入即可．

然后是全局最大值，可以用一个平衡树/支持删除任意节点的堆（如左偏树）/multiset 来维护每个堆的堆顶．

所以，每个操作分别如下：

1.  暴力下传点数较小的堆的标记，合并两个堆，更新 size、tag，在 multiset 中删去合并后不在堆顶的那个原堆顶．
2.  删除节点，更新值，插入回来，更新 multiset．需要分删除节点是否为根来讨论一下．
3.  堆顶打标记，更新 multiset．
4.  打全局标记．
5.  查询值 + 堆顶标记 + 全局标记．
6.  查询根的值 + 堆顶标记 + 全局标记．
7.  查询 multiset 最大值 + 全局标记．

??? note "棘手的操作参考代码"
    ```cpp
    --8<-- "docs/ds/code/leftist-tree/leftist-tree_3.cpp"
    ```

### [「BOI2004」Sequence 数字序列](https://www.luogu.com.cn/problem/P4331)

这是一道论文题，详见 [《黄源河 -- 左偏树的特点及其应用》](https://github.com/OI-wiki/libs/blob/master/%E9%9B%86%E8%AE%AD%E9%98%9F%E5%8E%86%E5%B9%B4%E8%AE%BA%E6%96%87/%E5%9B%BD%E5%AE%B6%E9%9B%86%E8%AE%AD%E9%98%9F2005%E8%AE%BA%E6%96%87%E9%9B%86/%E9%BB%84%E6%BA%90%E6%B2%B3--%E5%B7%A6%E5%81%8F%E6%A0%91%E7%9A%84%E7%89%B9%E7%82%B9%E5%8F%8A%E5%85%B6%E5%BA%94%E7%94%A8/%E9%BB%84%E6%BA%90%E6%B2%B3.pdf)．

## 参考资料

[^ref1]: [Self-Adjusting Heaps](https://epubs.siam.org/doi/10.1137/0215004)


## ds/li-chao-tree.md

## 引入

???+ note "[洛谷 4097 \[HEOI2013\]Segment](https://www.luogu.com.cn/problem/P4097)"
    要求在平面直角坐标系下维护两个操作（强制在线）：
    
    1.  在平面上加入一条线段．记第 $i$ 条被插入的线段的标号为 $i$，该线段的两个端点分别为 $(x_0,y_0)$，$(x_1,y_1)$．
    2.  给定一个数 $k$，询问与直线 $x = k$ 相交的线段中，交点纵坐标最大的线段的编号（若有多条线段与查询直线的交点纵坐标都是最大的，则输出编号最小的线段）．特别地，若不存在线段与给定直线相交，输出 $0$．
    
    数据满足：操作总数 $1 \leq n \leq 10^5$，$1 \leq k, x_0, x_1 \leq 39989$，$1 \leq y_0, y_1 \leq 10^9$．

我们发现，传统的线段树无法很好地维护这样的信息．这种情况下，**李超线段树** 便应运而生．

## 过程

我们可以把任务转化为维护如下操作：

-   加入一个一次函数，定义域为 $[l,r]$；
-   给定 $k$，求定义域包含 $k$ 的所有一次函数中，在 $x=k$ 处取值最大的那个，如果有多个函数取值相同，选编号最小的．

???+ warning "注意"
    当线段垂直于 $x$ 轴时，会出现除以零的情况．假设线段两端点分别为 $(x,y_0)$ 和 $(x,y_1)$，$y_0<y_1$，则插入定义域为 $[x,x]$ 的一次函数 $f(x)=0\cdot x+y_1$．

看到区间修改，我们按照线段树解决区间问题的常见方法，给每个节点一个懒标记．每个节点 $i$ 的懒标记都是一条线段，记为 $l_i$，表示要用 $l_i$ 更新该节点所表示的整个区间．

现在我们需要插入一条线段 $f$，考虑某个被新线段 $f$ 完整覆盖的线段树区间．若该区间无标记，直接打上用该线段更新的标记．

如果该区间已经有标记了，由于标记难以合并，只能把标记下传．但是子节点也有自己的标记，也可能产生冲突，所以我们要递归下传标记．

![](images/li-chao-tree-1.png)

如图，按新线段 $f$ 取值是否大于原标记 $g$，我们可以把当前区间分为两个子区间．其中 **肯定有一个子区间被左区间或右区间完全包含**，也就是说，在两条线段中，肯定有一条线段，只可能成为左区间的答案，或者只可能成为右区间的答案．我们用这条线段递归更新对应子树，用另一条线段作为懒标记更新整个区间，这就保证了递归下传的复杂度．当一条线段只可能成为左或右区间的答案时，才会被下传，所以不用担心漏掉某些线段．

具体来说，设当前区间的中点为 $m$，我们拿新线段 $f$ 在中点处的值与原最优线段 $g$ 在中点处的值作比较．

如果新线段 $f$ 更优，则将 $f$ 和 $g$ 交换．那么现在考虑在中点处 $f$ 不如 $g$ 优的情况：

1.  若在左端点处 $f$ 更优，那么 $f$ 和 $g$ 必然在左半区间中产生了交点，$f$ 只有在左区间才可能优于 $g$，递归到左儿子中进行下传；
2.  若在右端点处 $f$ 更优，那么 $f$ 和 $g$ 必然在右半区间中产生了交点，$f$ 只有在右区间才可能优于 $g$，递归到右儿子中进行下传；
3.  若在左右端点处 $g$ 都更优，那么 $f$ 不可能成为答案，不需要继续下传．

除了这两种情况之外，还有一种情况是 $f$ 和 $g$ 刚好交于中点，在程序实现时可以归入中点处 $f$ 不如 $g$ 优的情况，结果会往 $f$ 更优的一个端点进行递归下传．

最后将 $g$ 作为当前区间的懒标记．

下传标记：

???+ note "实现"
    ```cpp
    constexpr double eps = 1e-9;
    
    int cmp(double x, double y) {  // 因为用到了浮点数，所以会有精度误差
      if (x - y > eps) return 1;
      if (y - x > eps) return -1;
      return 0;
    }
    
    //...
    
    void upd(int root, int cl, int cr, int u) {  // 对线段完全覆盖到的区间进行修改
      int &v = s[root], mid = (cl + cr) >> 1;
      int bmid = cmp(calc(u, mid), calc(v, mid));
      if (bmid == 1 || (!bmid && u < v))  // 在此题中记得判线段编号
        swap(u, v);
      int bl = cmp(calc(u, cl), calc(v, cl)), br = cmp(calc(u, cr), calc(v, cr));
      if (bl == 1 || (!bl && u < v)) upd(root << 1, cl, mid, u);
      if (br == 1 || (!br && u < v)) upd(root << 1 | 1, mid + 1, cr, u);
      // 上面两个 if 的条件最多只有一个成立，这保证了李超树的时间复杂度
    }
    ```

拆分线段：

???+ note "实现"
    ```cpp
    void update(int root, int cl, int cr, int l, int r,
                int u) {  // 定位插入线段完全覆盖到的区间
      if (l <= cl && cr <= r) {
        upd(root, cl, cr, u);  // 完全覆盖当前区间，更新当前区间的标记
        return;
      }
      int mid = (cl + cr) >> 1;
      if (l <= mid) update(root << 1, cl, mid, l, r, u);  // 递归拆分区间
      if (mid < r) update(root << 1 | 1, mid + 1, cr, l, r, u);
    }
    ```

注意懒标记并不等价于在区间中点处取值最大的线段．

![](images/li-chao-tree-2.png)

如图，加入黄色线段后，只有红色节点的标记被更新，而绿色节点的标记还未被改变．但在第二、三、四个绿色区间的中点处显然黄色线段取值最大．

查询时，我们可以利用标记永久化思想，在包含 $x$ 的所有线段树区间（不超过 $O(\log n)$ 个）的标记线段中，比较得出最终答案．

查询：

???+ note "实现"
    ```cpp
    pdi query(int root, int l, int r, int d) {  // 查询
      if (r < d || d < l) return {0, 0};
      int mid = (l + r) >> 1;
      double res = calc(s[root], d);
      if (l == r) return {res, s[root]};
      return pmax({res, s[root]}, pmax(query(root << 1, l, mid, d),
                                       query(root << 1 | 1, mid + 1, r, d)));
    }
    ```

根据上面的描述，查询过程的时间复杂度显然为 $O(\log n)$，而插入过程中，我们需要将原线段拆分到 $O(\log n)$ 个区间中，对于每个区间，我们又需要花费 $O(\log n)$ 的时间递归下传，从而插入过程的时间复杂度为 $O(\log^2 n)$．

??? note "[\[HEOI2013\]Segment](https://www.luogu.com.cn/problem/P4097) 参考代码"
    ```cpp
    --8<-- "docs/ds/code/li-chao-tree/li-chao-tree_1.cpp"
    ```

## 合并

类似于普通线段树的合并，我们定义以下过程来将两个李超线段树节点 $u,v$ 合并，并以 $u$ 作为新的根．

1.  如果 $v$ 为空，结束过程．

2.  如果 $u$ 为空，将 $v$ 复制给 $u$．

3.  将 $v$ 对应线段插入到 $u$ 为根的子树．

4.  递归将 $u,v$ 的左右子树对应合并．

若合并若干李超线段树涉及的总点数为 $n$，则该过程的复杂度为 $O(n\log n)$：对于任意线段在树上对应的节点，每次涉及移动它时，我们要么使其深度 $+1$，要么直接从树上删除，这两个操作的代价都是 $O(1)$ 的，而每个点深度至多为 $O(\log n)$，于是复杂度如上．

???+ note "实现"
    ```cpp
    void upd(int &root, int cl, int cr,
             int u) {  // 涉及多棵李超线段树合并，使用动态开点．
      static int idx = 0;
      if (!root) {
        s[root = ++idx] = u;
        return;
      }
      int &v = s[root], mid = (cl + cr) >> 1;
      int bmid = cmp(calc(u, mid), calc(v, mid));
      if (bmid == 1 || (!bmid && u < v)) swap(u, v);
      int bl = cmp(calc(u, cl), calc(v, cl)), br = cmp(calc(u, cr), calc(v, cr));
      if (bl == 1 || (!bl && u < v)) upd(ls[root], cl, mid, u);
      if (br == 1 || (!br && u < v)) upd(rs[root], mid + 1, cr, u);
    }
    
    int merge(int &u, int &v, int l, int r) {
      if (!u || !v) {
        return u + v;
      }
      if (l == r) {
        int b = cmp(calc(s[v], l), calc(s[u], l));
        if (b == 1 || (!b && s[v] < s[u])) return v;
        return u;
      }
      upd(u, l, r, s[v]);
      int mid = (l + r) >> 1;
      ls[u] = merge(ls[u], ls[v], l, mid);
      rs[u] = merge(rs[u], rs[v], mid + 1, r);
      return u;
    }
    ```

## 习题

[「JSOI2008」Blue Mary 开公司](https://www.luogu.com.cn/problem/P4254)

[「CodeChef」TSUM2 Sum on Tree](https://www.codechef.com/problems/TSUM2)

[「USACO13MAR」Hill Walk G](https://www.luogu.com.cn/problem/P3081)

[「CF932F」Escape Through Leaf](https://codeforces.com/problemset/problem/932/F)


## ds/linked-list.md

本页面将简要介绍链表．

## 引入

链表是一种用于存储数据的数据结构，通过如链条一般的指针来连接元素．它的特点是插入与删除数据十分方便，但寻找与读取数据的表现欠佳．

## 与数组的区别

链表和数组都可用于存储数据．与链表不同，数组将所有元素按次序依次存储．不同的存储结构令它们有了不同的优势：

链表因其链状的结构，能方便地删除、插入数据，操作次数是 $O(1)$．但也因为这样，寻找、读取数据的效率不如数组高，在随机访问数据中的操作次数是 $O(n)$．

数组可以方便地寻找并读取数据，在随机访问中操作次数是 $O(1)$．但删除、插入的操作次数是 $O(n)$ 次．

## 构建链表

???+ tip "Tip"
    构建链表时，使用指针的部分比较抽象，光靠文字描述和代码可能难以理解，建议配合作图来理解．

### 单向链表

单向链表中包含数据域和指针域，其中数据域用于存放数据，指针域用来连接当前结点和下一节点．

![](images/list.svg)

???+ note "实现"
    === "C++"
        ```cpp
        struct Node {
          int value;
          Node *next;
        };
        ```
    
    === "Python"
        ```python
        class Node:
            def __init__(self, value=None, next=None):
                self.value = value
                self.next = next
        ```

### 双向链表

双向链表中同样有数据域和指针域．不同之处在于，指针域有左右（或上一个、下一个）之分，用来连接上一个结点、当前结点、下一个结点．

![](images/double-list.svg)

???+ note "实现"
    === "C++"
        ```cpp
        struct Node {
          int value;
          Node *left;
          Node *right;
        };
        ```
    
    === "Python"
        ```python
        class Node:
            def __init__(self, value=None, left=None, right=None):
                self.value = value
                self.left = left
                self.right = right
        ```

## 向链表中插入（写入）数据

### 单向链表

流程大致如下：

1.  初始化待插入的数据 `node`；
2.  将 `node` 的 `next` 指针指向 `p` 的下一个结点；
3.  将 `p` 的 `next` 指针指向 `node`．

具体过程可参考下图：

1.  ![](./images/list-insert-1.svg)
2.  ![](./images/list-insert-2.svg)
3.  ![](./images/list-insert-3.svg)

代码实现如下：

???+ note "实现"
    === "C++"
        ```cpp
        void insertNode(int i, Node *p) {
          Node *node = new Node;
          node->value = i;
          node->next = p->next;
          p->next = node;
        }
        ```
    
    === "Python"
        ```python
        def insertNode(i, p):
            node = Node()
            node.value = i
            node.next = p.next
            p.next = node
        ```

### 单向循环链表

将链表的头尾连接起来，链表就变成了循环链表．由于链表首尾相连，在插入数据时需要判断原链表是否为空：为空则自身循环，不为空则正常插入数据．

大致流程如下：

1.  初始化待插入的数据 `node`；
2.  判断给定链表 `p` 是否为空；
3.  若为空，则将 `node` 的 `next` 指针和 `p` 都指向自己；
4.  否则，将 `node` 的 `next` 指针指向 `p` 的下一个结点；
5.  将 `p` 的 `next` 指针指向 `node`．

具体过程可参考下图：

1.  ![](./images/list-insert-cyclic-1.svg)
2.  ![](./images/list-insert-cyclic-2.svg)
3.  ![](./images/list-insert-cyclic-3.svg)

代码实现如下：

???+ note "实现"
    === "C++"
        ```cpp
        void insertNode(int i, Node *p) {
          Node *node = new Node;
          node->value = i;
          node->next = NULL;
          if (p == NULL) {
            p = node;
            node->next = node;
          } else {
            node->next = p->next;
            p->next = node;
          }
        }
        ```
    
    === "Python"
        ```python
        def insertNode(i, p):
            node = Node()
            node.value = i
            node.next = None
            if p == None:
                p = node
                node.next = node
            else:
                node.next = p.next
                p.next = node
        ```

### 双向循环链表

在向双向循环链表插入数据时，除了要判断给定链表是否为空外，还要同时修改左、右两个指针．

大致流程如下：

1.  初始化待插入的数据 `node`；
2.  判断给定链表 `p` 是否为空；
3.  若为空，则将 `node` 的 `left` 和 `right` 指针，以及 `p` 都指向自己；
4.  否则，将 `node` 的 `left` 指针指向 `p`;
5.  将 `node` 的 `right` 指针指向 `p` 的右结点；
6.  将 `p` 右结点的 `left` 指针指向 `node`；
7.  将 `p` 的 `right` 指针指向 `node`．

代码实现如下：

???+ note "实现"
    === "C++"
        ```cpp
        void insertNode(int i, Node *p) {
          Node *node = new Node;
          node->value = i;
          if (p == NULL) {
            p = node;
            node->left = node;
            node->right = node;
          } else {
            node->left = p;
            node->right = p->right;
            p->right->left = node;
            p->right = node;
          }
        }
        ```
    
    === "Python"
        ```python
        def insertNode(i, p):
            node = Node()
            node.value = i
            if p == None:
                p = node
                node.left = node
                node.right = node
            else:
                node.left = p
                node.right = p.right
                p.right.left = node
                p.right = node
        ```

## 从链表中删除数据

### 单向（循环）链表

设待删除结点为 `p`，从链表中删除它时，将 `p` 的下一个结点 `p->next` 的值覆盖给 `p` 即可，与此同时更新 `p` 的下下个结点．

流程大致如下：

1.  将 `p` 下一个结点的值赋给 `p`，以抹掉 `p->value`；
2.  新建一个临时结点 `t` 存放 `p->next` 的地址；
3.  将 `p` 的 `next` 指针指向 `p` 的下下个结点，以抹掉 `p->next`；
4.  删除 `t`．此时虽然原结点 `p` 的地址还在使用，删除的是原结点 `p->next` 的地址，但 `p` 的数据被 `p->next` 覆盖，`p` 名存实亡．

具体过程可参考下图：

1.  ![](./images/list-delete-1.svg)
2.  ![](./images/list-delete-2.svg)
3.  ![](./images/list-delete-3.svg)

代码实现如下：

???+ note "实现"
    === "C++"
        ```cpp
        void deleteNode(Node *p) {
          p->value = p->next->value;
          Node *t = p->next;
          p->next = p->next->next;
          delete t;
        }
        ```
    
    === "Python"
        ```python
        def deleteNode(p):
            p.value = p.next.value
            p.next = p.next.next
        ```

### 双向循环链表

流程大致如下：

1.  将 `p` 左结点的右指针指向 `p` 的右节点；
2.  将 `p` 右结点的左指针指向 `p` 的左节点；
3.  新建一个临时结点 `t` 存放 `p` 的地址；
4.  将 `p` 的右节点地址赋给 `p`，以避免 `p` 变成悬垂指针；
5.  删除 `t`．

代码实现如下：

???+ note "实现"
    === "C++"
        ```cpp
        void deleteNode(Node *&p) {
          p->left->right = p->right;
          p->right->left = p->left;
          Node *t = p;
          p = p->right;
          delete t;
        }
        ```
    
    === "Python"
        ```python
        def deleteNode(p):
            p.left.right = p.right
            p.right.left = p.left
            p = p.right
        ```

## 技巧

### 异或链表

异或链表（XOR Linked List）本质上还是 **双向链表**，但它利用按位异或的值，仅使用一个指针的内存大小便可以实现双向链表的功能．

我们在结构 `Node` 中定义 `lr = left ^ right`，即前后两个元素地址的 **按位异或值**．正向遍历时用前一个元素的地址异
或当前节点的 `lr` 可得到后一个元素的地址，反向遍历时用后一个元素的地址异或当前节点的 `lr` 又可得到前一个的元素地址．
这样一来，便可以用一半的内存实现双向链表同样的功能．


## ds/llrbt.md

author: c-forrest, Enter-tainer, giiiiiithub, hly1204, iamtwz, Ir1d, kigawas, ksyx, luxuryspark567, mgt, orzAtalod, sandyzikun, SunsetGlow95, Tiphereth-A, current2020, untitledunrevised, yuhuoji

左偏红黑树是 [红黑树](./rbtree.md) 的一种变体，它的对红边（点）的位置做了一定限制，使得其插入与删除操作可以与 [2-3 树](https://en.wikipedia.org/wiki/2%E2%80%933_tree) 构成一一对应．

我们假设读者已经至少掌握了一种基于旋转的平衡树，因此本文不会对旋转操作进行讲解．

## 红黑树

### 性质

一棵红黑树满足如下性质：

1.  节点是红色或黑色；
2.  NIL 节点（空叶子节点）为黑色；
3.  红色的节点的所有儿子的颜色必须是黑色，即从每个叶子到根的所有路径上不能有两个连续的红色节点；
4.  从任一节点到其子树中的每个叶子的所有简单路径上都包含相同数目的黑色节点．（黑高平衡）

这保证了从根节点到任意叶子的最长路径（红黑交替）不会超过最短路径（全黑）的二倍．从而保证了树的平衡性．

维护这些性质是比较复杂的，如果我们要插入一个节点，首先，它一定会被染色成红色，否则会破坏性质 4．即使这样，我们还是有可能会破坏性质 3．因此需要进行调整．而删除节点就更加麻烦，与插入类似，我们不能删除黑色节点，否则会破坏黑高的平衡．如何方便地解决这些问题呢？

## 左偏红黑树（Left Leaning Red Black Tree）

### 解释

左偏红黑树是一种容易实现的红黑树变体．

在以下左偏红黑树示意图中，是边具有颜色而不是节点具有颜色．我们习惯用一个节点的颜色代指它的父亲边的颜色．

左偏红黑树对红黑树进行了进一步限制，一个黑色节点的左右儿子：

-   要么全是黑色；
-   要么左儿子是红色，右儿子是黑色．

符合条件的情况：

![llrbt1](./images/llrbt-1.png)

不符合条件的情况：

![llrbt2](./images/llrbt-2.png)

这是左偏树的「左偏」性质：红色边只能是左偏的．

### 过程

#### 插入

我们首先使用普通的 BST 插入方法，在树的底部插入一个红色的叶子节点，然后通过从下向上的调整，使得插入后的树仍然符合左偏红黑树的性质．下面描述调整的过程：

![llrbt3](./images/llrbt-3.png)

插入后，可能会产生一条右偏的红色边，因此需要对红边右偏的情况进行一次左旋：

![llrbt4](./images/llrbt-4.png)

考虑左旋后会产生两条连续的左偏红色边：

![llrbt5](./images/llrbt-5.png)

因此需要把它进行一次右旋．而对于右旋后的情况，我们应该对它进行 `color_flip`：即翻转该节点和它的两个儿子的颜色

![llrbt6](./images/llrbt-6.png)

从而消灭右偏的红边．

??? note "参考代码（部分）"
    ```cpp
    template <class Key, class Compare>
    typename Set<Key, Compare>::Node *Set<Key, Compare>::fix_up(
        Set::Node *root) const {
      if (is_red(root->rc) && !is_red(root->lc))  // fix right leaned red link
        root = rotate_left(root);
      if (is_red(root->lc) &&
          is_red(root->lc->lc))  // fix doubly linked left leaned red link
        // if (root->lc == nullptr), then the second expr won't be evaluated
        root = rotate_right(root);
      if (is_red(root->lc) && is_red(root->rc))
        // break up 4 node
        color_flip(root);
      root->size = size(root->lc) + size(root->rc) + 1;
      return root;
    }
    
    template <class Key, class Compare>
    typename Set<Key, Compare>::Node_Set<Key, Compare>::insert(
        Set::Node_root, const Key &key) const {
      if (root == nullptr) return new Node(key, kRed, 1);
      if (root->key == key)
        ;
      else if (cmp\_(key, root->key))  // if (key < root->key)
        root->lc = insert(root->lc, key);
      else
        root->rc = insert(root->rc, key);
      return fix_up(root);
    }
    ```

#### 删除

删除操作基于这样的思想：我们不能删除黑色的节点，因为这样会破坏黑高．所以我们需要保证我们最后删除的节点是红色的．

##### 删除最小值节点

首先来试一下删除整棵树里的最小值．

怎么才能保证最后删除的节点是红色的呢？我们需要在向下递归的过程中保证一个性质：如果当前节点是 `h`，那么需要保证 `h` 是红色，或者 `h->lc` 是红色．

考虑这样做的正确性，如果我们能够通过各种旋转和反转颜色操作成功维护这个性质，那么当我们到达最小的节点 `h_min` 的时候，有 `h_min` 是红色，或者 `h_min` 的左子树——但是 `h_min` 根本没有左子树！所以这就保证了最小值节点一定是红的，既然它是红色的，我们就可以大胆的删除它，然后用与插入操作相同的调整思路对树进行调整．

下面我们来考虑怎么满足这个性质，注意，我们会在向下递归的时候 **临时地** 破坏左偏红黑树的若干性质，但是当我们从递归中返回时还会将其恢复．

如下图所描述的，是一种较为简单的情况，此时 `h->rc->lc` 为黑色，我们只需要一次翻转颜色即可：

![llrbt-7](./images/llrbt-7.png)

并且，在如上所示的翻转之后，不会使 `h->rc` 与 `h->rc->lc` 形成连续的红边；

但如果 `h->rc->lc` 是红色，情况会比较复杂：

![llrbt-8](./images/llrbt-8.png)

如果只进行翻转颜色，会产生连续的红边，而考虑我们递归返回的时候，是无法修复这样的情况的，因此需要进行处理．

然后就可以进行删除了：

??? note "参考代码（部分）"
    ```cpp
    template <class Key, class Compare>
    typename Set<Key, Compare>::Node *Set<Key, Compare>::move_red_left(
        Set::Node *root) const {
      color_flip(root);
      if (is_red(root->rc->lc)) {
        // assume that root->rc != nullptr when calling this function
        root->rc = rotate_right(root->rc);
        root = rotate_left(root);
        color_flip(root);
      }
      return root;
    }
    
    template <class Key, class Compare>
    typename Set<Key, Compare>::Node *Set<Key, Compare>::delete_min(
        Set::Node *root) const {
      if (root->lc == nullptr) {
        delete root;
        return nullptr;
      }
      if (!is_red(root->lc) && !is_red(root->lc->lc)) {
        // make sure either root->lc or root->lc->lc is red
        // thus make sure we will delete a red node in the end
        root = move_red_left(root);
      }
      root->lc = delete_min(root->lc);
      return fix_up(root);
    }
    ```

##### 删除任意节点

我们首先考虑删除叶子：与删最小值类似，我们在删除任意值的过程中也要维护一个性质，不过这次比较特殊，因为我们不是只向左边走，而是可以向左右两个方向走，因此在删除过程中维护的性质是这样的：如果往左走，当前节点是 `h`，那么需要保证 `h` 是红色，或者 `h->lc` 是红色；如果往右走，当前节点是 `h`，那么需要保证 `h` 是红色，或者 `h->rc` 是红色．这样可以保证我们最后总会删掉一个红色节点．

下面考虑删除非叶子节点，我们只需要找到其右子树（如果有）里的最小节点，然后用右子树的最小节点的值代替该节点的值，最后删除右子树里的最小节点．

![llrbt-9](./images/llrbt-9.png)

那如果没有右子树怎么办？我们需要把左子树旋转过来，这样就不会出现这个问题了．

??? note "参考代码（部分）"
    ```cpp
    template <class Key, class Compare>
    typename Set<Key, Compare>::Node *Set<Key, Compare>::delete_arbitrary(
        Set::Node *root, Key key) const {
      if (cmp_(key, root->key)) {
        // key < root->key
        if (!is_red(root->lc) && !(is_red(root->lc->lc)))
          root = move_red_left(root);
        // ensure the invariant: either root->lc or root->lc->lc (or root and
        // root->lc after dive into the function) is red, to ensure we will
        // eventually delete a red node. therefore we will not break the black
        // height balance
        root->lc = delete_arbitrary(root->lc, key);
      } else {
        // key >= root->key
        if (is_red(root->lc)) root = rotate_right(root);
        if (key == root->key && root->rc == nullptr) {
          delete root;
          return nullptr;
        }
        if (!is_red(root->rc) && !is_red(root->rc->lc)) root = move_red_right(root);
        if (key == root->key) {
          root->key = get_min(root->rc);
          root->rc = delete_min(root->rc);
        } else {
          root->rc = delete_arbitrary(root->rc, key);
        }
      }
      return fix_up(root);
    }
    ```

## 实现

下面的代码是用左偏红黑树实现的 `Set`，即有序不可重集合：

??? note "参考代码"
    ```cpp
    #include <algorithm>
    #include <memory>
    #include <vector>
    
    template <class Key, class Compare = std::less<Key>>
    class Set {
     private:
      enum NodeColor { kBlack = 0, kRed = 1 };
    
      struct Node {
        Key key;
        Node *lc{nullptr}, *rc{nullptr};
        size_t size{0};
        NodeColor color;  // the color of the parent link
    
        Node(Key key, NodeColor color, size_t size)
            : key(key), color(color), size(size) {}
    
        Node() = default;
      };
    
      void destroyTree(Node *root) const {
        if (root != nullptr) {
          destroyTree(root->lc);
          destroyTree(root->rc);
          root->lc = root->rc = nullptr;
          delete root;
        }
      }
    
      bool is_red(const Node *nd) const {
        return nd == nullptr ? false : nd->color;  // kRed == 1, kBlack == 0
      }
    
      size_t size(const Node *nd) const { return nd == nullptr ? 0 : nd->size; }
    
      Node *rotate_left(Node *node) const {
        // left rotate a red link
        //          <1>                   <2>
        //        /    \\               //    \
        //       *      <2>    ==>     <1>     *
        //             /   \          /   \
        //            *     *        *     *
        Node *res = node->rc;
        node->rc = res->lc;
        res->lc = node;
        res->color = node->color;
        node->color = kRed;
        res->size = node->size;
        node->size = size(node->lc) + size(node->rc) + 1;
        return res;
      }
    
      Node *rotate_right(Node *node) const {
        // right rotate a red link
        //            <1>               <2>
        //          //    \           /    \\
        //         <2>     *   ==>   *      <1>
        //        /   \                    /   \
        //       *     *                  *     *
        Node *res = node->lc;
        node->lc = res->rc;
        res->rc = node;
        res->color = node->color;
        node->color = kRed;
        res->size = node->size;
        node->size = size(node->lc) + size(node->rc) + 1;
        return res;
      }
    
      NodeColor neg_color(NodeColor n) const { return n == kBlack ? kRed : kBlack; }
    
      void color_flip(Node *node) const {
        node->color = neg_color(node->color);
        node->lc->color = neg_color(node->lc->color);
        node->rc->color = neg_color(node->rc->color);
      }
    
      Node *insert(Node *root, const Key &key) const;
      Node *delete_arbitrary(Node *root, Key key) const;
      Node *delete_min(Node *root) const;
      Node *move_red_right(Node *root) const;
      Node *move_red_left(Node *root) const;
      Node *fix_up(Node *root) const;
      const Key &get_min(Node *root) const;
      void serialize(Node *root, std::vector<Key> *) const;
      void print_tree(Set::Node *root, int indent) const;
      Compare cmp_ = Compare();
      Node *root_{nullptr};
    
     public:
      using KeyType = Key;
      using ValueType = Key;
      using SizeType = std::size_t;
      using DifferenceType = std::ptrdiff_t;
      using KeyCompare = Compare;
      using ValueCompare = Compare;
      using Reference = Key &;
      using ConstReference = const Key &;
    
      Set() = default;
    
      Set(Set &) = default;
    
      Set(Set &&) noexcept = default;
    
      ~Set() { destroyTree(root_); }
    
      SizeType size() const;
    
      SizeType count(const KeyType &key) const;
    
      SizeType erase(const KeyType &key);
    
      void clear();
    
      void insert(const KeyType &key);
    
      bool empty() const;
    
      std::vector<Key> serialize() const;
    
      void print_tree() const;
    };
    
    template <class Key, class Compare>
    typename Set<Key, Compare>::SizeType Set<Key, Compare>::count(
        ConstReference key) const {
      Node *x = root_;
      while (x != nullptr) {
        if (key == x->key) return 1;
        if (cmp_(key, x->key))  // if (key < x->key)
          x = x->lc;
        else
          x = x->rc;
      }
      return 0;
    }
    
    template <class Key, class Compare>
    typename Set<Key, Compare>::SizeType Set<Key, Compare>::erase(
        const KeyType &key) {
      if (count(key) > 0) {
        if (!is_red(root_->lc) && !(is_red(root_->rc))) root_->color = kRed;
        root_ = delete_arbitrary(root_, key);
        if (root_ != nullptr) root_->color = kBlack;
        return 1;
      } else {
        return 0;
      }
    }
    
    template <class Key, class Compare>
    void Set<Key, Compare>::clear() {
      destroyTree(root_);
      root_ = nullptr;
    }
    
    template <class Key, class Compare>
    void Set<Key, Compare>::insert(const KeyType &key) {
      root_ = insert(root_, key);
      root_->color = kBlack;
    }
    
    template <class Key, class Compare>
    bool Set<Key, Compare>::empty() const {
      return size(root_) == 0;
    }
    
    template <class Key, class Compare>
    typename Set<Key, Compare>::Node *Set<Key, Compare>::insert(
        Set::Node *root, const Key &key) const {
      if (root == nullptr) return new Node(key, kRed, 1);
      if (root->key == key)
        ;
      else if (cmp_(key, root->key))  // if (key < root->key)
        root->lc = insert(root->lc, key);
      else
        root->rc = insert(root->rc, key);
      return fix_up(root);
    }
    
    template <class Key, class Compare>
    typename Set<Key, Compare>::Node *Set<Key, Compare>::delete_min(
        Set::Node *root) const {
      if (root->lc == nullptr) {
        delete root;
        return nullptr;
      }
      if (!is_red(root->lc) && !is_red(root->lc->lc)) {
        // make sure either root->lc or root->lc->lc is red
        // thus make sure we will delete a red node in the end
        root = move_red_left(root);
      }
      root->lc = delete_min(root->lc);
      return fix_up(root);
    }
    
    template <class Key, class Compare>
    typename Set<Key, Compare>::Node *Set<Key, Compare>::move_red_right(
        Set::Node *root) const {
      color_flip(root);
      if (is_red(root->lc->lc)) {  // assume that root->lc != nullptr when calling
                                   // this function
        root = rotate_right(root);
        color_flip(root);
      }
      return root;
    }
    
    template <class Key, class Compare>
    typename Set<Key, Compare>::Node *Set<Key, Compare>::move_red_left(
        Set::Node *root) const {
      color_flip(root);
      if (is_red(root->rc->lc)) {
        // assume that root->rc != nullptr when calling this function
        root->rc = rotate_right(root->rc);
        root = rotate_left(root);
        color_flip(root);
      }
      return root;
    }
    
    template <class Key, class Compare>
    typename Set<Key, Compare>::Node *Set<Key, Compare>::fix_up(
        Set::Node *root) const {
      if (is_red(root->rc) && !is_red(root->lc))  // fix right leaned red link
        root = rotate_left(root);
      if (is_red(root->lc) &&
          is_red(root->lc->lc))  // fix doubly linked left leaned red link
        // if (root->lc == nullptr), then the second expr won't be evaluated
        root = rotate_right(root);
      if (is_red(root->lc) && is_red(root->rc))
        // break up 4 node
        color_flip(root);
      root->size = size(root->lc) + size(root->rc) + 1;
      return root;
    }
    
    template <class Key, class Compare>
    const Key &Set<Key, Compare>::get_min(Set::Node *root) const {
      Node *x = root;
      // will crash as intended when root == nullptr
      for (; x->lc != nullptr; x = x->lc);
      return x->key;
    }
    
    template <class Key, class Compare>
    typename Set<Key, Compare>::SizeType Set<Key, Compare>::size() const {
      return size(root_);
    }
    
    template <class Key, class Compare>
    typename Set<Key, Compare>::Node *Set<Key, Compare>::delete_arbitrary(
        Set::Node *root, Key key) const {
      if (cmp_(key, root->key)) {
        // key < root->key
        if (!is_red(root->lc) && !(is_red(root->lc->lc)))
          root = move_red_left(root);
        // ensure the invariant: either root->lc or root->lc->lc (or root and
        // root->lc after dive into the function) is red, to ensure we will
        // eventually delete a red node. therefore we will not break the black
        // height balance
        root->lc = delete_arbitrary(root->lc, key);
      } else {
        // key >= root->key
        if (is_red(root->lc)) root = rotate_right(root);
        if (key == root->key && root->rc == nullptr) {
          delete root;
          return nullptr;
        }
        if (!is_red(root->rc) && !is_red(root->rc->lc)) root = move_red_right(root);
        if (key == root->key) {
          root->key = get_min(root->rc);
          root->rc = delete_min(root->rc);
        } else {
          root->rc = delete_arbitrary(root->rc, key);
        }
      }
      return fix_up(root);
    }
    
    template <class Key, class Compare>
    std::vector<Key> Set<Key, Compare>::serialize() const {
      std::vector<int> v;
      serialize(root_, &v);
      return v;
    }
    
    template <class Key, class Compare>
    void Set<Key, Compare>::serialize(Set::Node *root,
                                      std::vector<Key> *res) const {
      if (root == nullptr) return;
      serialize(root->lc, res);
      res->push_back(root->key);
      serialize(root->rc, res);
    }
    
    template <class Key, class Compare>
    void Set<Key, Compare>::print_tree(Set::Node *root, int indent) const {
      if (root == nullptr) return;
      print_tree(root->lc, indent + 4);
      std::cout << std::string(indent, '-') << root->key << std::endl;
      print_tree(root->rc, indent + 4);
    }
    
    template <class Key, class Compare>
    void Set<Key, Compare>::print_tree() const {
      print_tree(root_, 0);
    }
    ```

## 与 2-3 树的关系

2-3 树是 3 阶 B 树，每个结点都是 2 结点或 3 结点，存储一个或两个数据元素．非叶结点的 2 结点和 3 结点分别只能有两个或三个孩子．而且，2-3 树中存储的所有数据都是有序的．

2-3 树和左偏红黑树实质是等价的．2-3 树中一个节点可以存储 1 个元素或 2 个元素，而红黑树的一个节点只能存储一个元素．如下图所示，2-3 树的 2 节点对应一个黑色节点，3 节点对应一个红色节点和一个黑色节点（可以将 bc 视作平行）．

![2-3-tree-rbt](images/2-3-tree-rbt-1.svg)

![2-3-tree-rbt](images/2-3-tree-rbt-2.svg)

下图是一棵 2-3 树对应的左偏红黑树．

![2-3-tree-rbt](images/2-3-tree-rbt-3.svg)

2-3 树和左偏红黑树的插入与删除操作是一一对应的．[^23-vs-llrbt]

## 参考资料与拓展阅读

-   [Left-Leaning Red-Black Trees](https://sedgewick.io/wp-content/themes/sedgewick/papers/2008LLRB.pdf)-  Robert Sedgewick Princeton University
-   [Balanced Search Trees](https://algs4.cs.princeton.edu/lectures/keynote/33BalancedSearchTrees-2x2.pdf)-\_Algorithms\_Robert Sedgewick | Kevin Wayne

[^23-vs-llrbt]: [这篇博文](https://riteme.site/blog/2016-3-12/2-3-tree-and-red-black-tree.html) 提供了详细的描述．文中的「红黑树」实际上指的是「左偏红黑树」．


## ds/monotonic-queue.md

author: Link-cute, Xeonacid, ouuan, Alphnia, Lyccrius

## 引入

在学习单调队列前，让我们先来看一道例题．

???+ note "例题"
    [Sliding Window](http://poj.org/problem?id=2823)
    
    本题大意是给出一个长度为 $n$ 的数组，编程输出每 $k$ 个连续的数中的最大值和最小值．

最暴力的想法很简单，对于每一段 $i \sim i+k-1$ 的序列，逐个比较来找出最大值（和最小值），时间复杂度约为 $O(n \times k)$．

很显然，这其中进行了大量重复工作，除了开头 $k-1$ 个和结尾 $k-1$ 个数之外，每个数都进行了 $k$ 次比较，而题中 $100\%$ 的数据为 $n \le 1000000$，当 $k$ 稍大的情况下，显然会 TLE．

这时所用到的就是单调队列了．

## 定义

顾名思义，单调队列的重点分为「单调」和「队列」．

「单调」指的是元素的「规律」——递增（或递减）．

「队列」指的是元素只能从队头和队尾进行操作．

Ps. 单调队列中的 "队列" 与正常的队列有一定的区别，稍后会提到

## 例题分析

### 解释

有了上面「单调队列」的概念，很容易想到用单调队列进行优化．

要求的是每连续的 $k$ 个数中的最大（最小）值，很明显，当一个数进入所要 "寻找" 最大值的范围中时，若这个数比其前面（先进队）的数要大，显然，前面的数会比这个数先出队且不再可能是最大值．

也就是说——当满足以上条件时，可将前面的数 "弹出"，再将该数真正 push 进队尾．

这就相当于维护了一个递减的队列，符合单调队列的定义，减少了重复的比较次数，不仅如此，由于维护出的队伍是查询范围内的且是递减的，队头必定是该查询区域内的最大值，因此输出时只需输出队头即可．

显而易见的是，在这样的算法中，每个数只要进队与出队各一次，因此时间复杂度被降到了 $O(n)$．

而由于查询区间长度是固定的，超出查询空间的值再大也不能输出，因此还需要 site 数组记录第 $i$ 个队中的数在原数组中的位置，以弹出越界的队头．

### 过程

例如我们构造一个单调递增的队列会如下：

原序列为：

```text
1 3 -1 -3 5 3 6 7
```

因为我们始终要维护队列保证其 **递增** 的特点，所以会有如下的事情发生：（假设 $k = 3$）

| 操作                              | 队列状态      |
| ------------------------------- | --------- |
| 1 入队                            | `{1}`     |
| 3 比 1 大，3 入队                    | `{1 3}`   |
| -1 比队列中所有元素小，所以清空队列 -1 入队       | `{-1}`    |
| -3 比队列中所有元素小，所以清空队列 -3 入队       | `{-3}`    |
| 5 比 -3 大，直接入队                   | `{-3 5}`  |
| 3 比 5 小，5 出队，3 入队               | `{-3 3}`  |
| -3 已经在窗体外，所以 -3 出队；6 比 3 大，6 入队 | `{3 6}`   |
| 7 比 6 大，7 入队                    | `{3 6 7}` |

???+ note "例题参考代码"
    ```cpp
    --8<-- "docs/ds/code/monotonic-queue/monotonic-queue_1.cpp"
    ```

Ps. 此处的 "队列" 跟普通队列的一大不同就在于可以从队尾进行操作，STL 中有类似的数据结构 deque．

???+ note "例题 2 [Luogu P2698 Flowerpot S](https://www.luogu.com.cn/problem/P2698)"
    给出 $N$ 滴水的坐标，$y$ 表示水滴的高度，$x$ 表示它下落到 $x$ 轴的位置．每滴水以每秒 1 个单位长度的速度下落．你需要把花盆放在 $x$ 轴上的某个位置，使得从被花盆接着的第 1 滴水开始，到被花盆接着的最后 1 滴水结束，之间的时间差至少为 $D$．
    我们认为，只要水滴落到 $x$ 轴上，与花盆的边沿对齐，就认为被接住．给出 $N$ 滴水的坐标和 $D$ 的大小，请算出最小的花盆的宽度 $W$．$1\leq N \leq 100000 , 1 \leq D \leq 1000000, 0 \leq x,y\leq 10^6$

将所有水滴按照 $x$ 坐标排序之后，题意可以转化为求一个 $x$ 坐标差最小的区间使得这个区间内 $y$ 坐标的最大值和最小值之差至少为 $D$．我们发现这道题和上一道例题有相似之处，就是都与一个区间内的最大值最小值有关，但是这道题区间的大小不确定，而且区间大小本身还是我们要求的答案．

我们依然可以使用一个递增，一个递减两个单调队列在 $R$ 不断后移时维护 $[L,R]$ 内的最大值和最小值，不过此时我们发现，如果 $L$ 固定，那么 $[L,R]$ 内的最大值只会越来越大，最小值只会越来越小，所以设 $f(R) = \max[L,R]-\min[L,R]$，则 $f(R)$ 是个关于 $R$ 的递增函数，故 $f(R)\geq D \implies f(r)\geq D,R\lt r \leq N$．这说明对于每个固定的 $L$，向右第一个满足条件的 $R$ 就是最优答案．
所以我们整体求解的过程就是，先固定 $L$，从前往后移动 $R$，使用两个单调队列维护 $[L,R]$ 的最值．当找到了第一个满足条件的 $R$，就更新答案并将 $L$ 也向后移动．随着 $L$ 向后移动，两个单调队列都需及时弹出队头．这样，直到 $R$ 移到最后，每个元素依然是各进出队列一次，保证了 $O(n)$ 的时间复杂度．

???+ note "参考代码"
    ```cpp
    --8<-- "docs/ds/code/monotonic-queue/monotonic-queue_2.cpp"
    ```


## ds/monotonic-stack.md

## 引入

何为单调栈？顾名思义，单调栈即满足单调性的栈结构．与单调队列相比，其只在一端进行进出．

为了描述方便，以下举例及伪代码以维护一个整数的单调递增栈为例．

## 过程

### 插入

将一个元素插入单调栈时，为了维护栈的单调性，需要在保证将该元素插入到栈顶后整个栈满足单调性的前提下弹出最少的元素．

例如，栈中自顶向下的元素为 $\{0,11,45,81\}$．

![](images/monotonic-stack-before.svg)

插入元素 $14$ 时为了保证单调性需要依次弹出元素 $0,11$，操作后栈变为 $\{14,45,81\}$．

![](images/monotonic-stack-after.svg)

用伪代码描述如下：

???+ note "实现"
    ```text
    insert x
    while !sta.empty() && sta.top()<x
        sta.pop()
    sta.push(x)
    ```

### 使用

自然就是从栈顶读出来一个元素，该元素满足单调性的某一端．

例如举例中取出的即栈中的最小值．

## 应用

??? note "[POJ3250 Bad Hair Day](http://poj.org/problem?id=3250)"
    有 $N$ 头牛从左到右排成一排，每头牛有一个高度 $h_i$，设左数第 $i$ 头牛与「它右边第一头高度 $≥h_i$」的牛之间有 $c_i$ 头牛，试求 $\sum_{i=1}^{N} c_i$．

比较基础的应用有这一题，就是个单调栈的简单应用，记录每头牛被弹出的位置，如果没有被弹出过则为最远端，稍微处理一下即可计算出题目所需结果．

另外，单调栈也可以用于离线解决 RMQ 问题．

我们可以把所有询问按右端点排序，然后每次在序列上从左往右扫描到当前询问的右端点处，并把扫描到的元素插入到单调栈中．这样，每次回答询问时，单调栈中存储的值都是位置 $\le r$ 的、可能成为答案的决策点，并且这些元素满足单调性质．此时，单调栈上第一个位置 $\ge l$ 的元素就是当前询问的答案，这个过程可以用二分查找实现．使用单调栈解决 RMQ 问题的时间复杂度为 $O(q\log q + q\log n)$，空间复杂度为 $O(n)$．

## 习题

-   [洛谷 P5788【模板】单调栈](https://www.luogu.com.cn/problem/P5788)
-   [洛谷 P1901 发射站](https://www.luogu.com.cn/problem/P1901)


## ds/pairing-heap.md

## 引入

配对堆是一个支持插入，查询/删除最小值，合并，修改元素等操作的数据结构，是一种可并堆．有速度快和结构简单的优势，但由于其为基于势能分析的均摊复杂度，无法可持久化．

## 定义

配对堆是一棵满足堆性质的带权多叉树（如下图），即每个节点的权值都小于或等于他的所有儿子（以小根堆为例，下同）．  
![](./images/pairingheap1.jpg)

通常我们使用儿子 - 兄弟表示法储存一个配对堆（如下图），一个节点的所有儿子节点形成一个单向链表．每个节点储存第一个儿子的指针，即链表的头节点；和他的右兄弟的指针．

这种方式便于实现配对堆，也将方便复杂度分析．

![](./images/pairingheap2.jpg)

```cpp
struct Node {
  T v;  // T为权值类型
  Node *child, *sibling;
  // child 指向该节点第一个儿子，sibling 指向该节点的下一个兄弟．
  // 若该节点没有儿子/下个兄弟则指针指向 nullptr．
};
```

从定义可以发现，和其他常见的堆结构相比，配对堆不维护任何额外的树大小，深度，排名等信息（二叉堆也不维护额外信息，但它是通过维持一个严格的完全二叉树结构来保证操作的复杂度），且任何一个满足堆性质的树都是一个合法的配对堆，这样简单又高度灵活的数据结构奠定了配对堆在实践中优秀效率的基础；作为对比，斐波那契堆糟糕的常数就是因为它需要维护很多额外的信息．

配对堆通过一套精心设计的操作顺序来保证它的总复杂度，原论文[^ref1]将其称为「一种自调整的堆（Self Adjusting Heap）」．在这方面和 Splay 树（在原论文中被称作「Self Adjusting Binary Tree」）颇有相似之处．

## 过程

### 查询最小值

从配对堆的定义可看出，配对堆的根节点的权值一定最小，直接返回根节点即可．

### 合并

合并两个配对堆的操作很简单，首先令两个根节点较小的一个为新的根节点，然后将较大的根节点作为它的儿子插入进去．（见下图）

![](./images/pairingheap3.jpg)

需要注意的是，一个节点的儿子链表是按插入时间排序的，即最右边的节点最早成为父节点的儿子，最左边的节点最近成为父节点的儿子．

???+ note "实现"
    ```cpp
    Node* meld(Node* x, Node* y) {
      // 若有一个为空则直接返回另一个
      if (x == nullptr) return y;
      if (y == nullptr) return x;
      if (x->v > y->v) std::swap(x, y);  // swap后x为权值小的堆，y为权值大的堆
      // 将y设为x的儿子
      y->sibling = x->child;
      x->child = y;
      return x;  // 新的根节点为 x
    }
    ```

### 插入

合并都有了，插入就直接把新元素视为一个新的配对堆和原堆合并就行了．

### 删除最小值

首先要提及的一点是，上文的几个操作都十分偷懒，完全没有对数据结构进行维护，所以我们需要小心设计删除最小值的操作，来保证总复杂度不出问题．

根节点即为最小值，所以要删除的是根节点．考虑拿掉根节点之后会发生什么：根节点原来的所有儿子构成了一片森林；而配对堆应当是一棵树，所以我们需要通过某种顺序把这些儿子全部合并起来．

一个很自然的想法是使用 `meld` 函数把儿子们从左到右挨个并在一起，这样做的话正确性是显然的，但是会导致单次操作复杂度退化到 $O(n)$．

为了保证总的均摊复杂度，需要使用一个「两步走」的合并方法：

1.  把儿子们两两配成一对，用 `meld` 操作把被配成同一对的两个儿子合并到一起（见下图 1），
2.  将新产生的堆 **从右往左**（即老的儿子到新的儿子的方向）挨个合并在一起（见下图 2）．

![](./images/pairingheap4.jpg)

![](./images/pairingheap5.jpg)

先实现一个辅助函数 `merges`，作用是合并一个节点的所有兄弟．

???+ note "实现"
    ```cpp
    Node* merges(Node* x) {
      if (x == nullptr || x->sibling == nullptr)
        return x;  // 如果该树为空或他没有下一个兄弟，就不需要合并了，return．
      Node* y = x->sibling;                // y 为 x 的下一个兄弟
      Node* c = y->sibling;                // c 是再下一个兄弟
      x->sibling = y->sibling = nullptr;   // 拆散
      return meld(merges(c), meld(x, y));  // 核心部分
    }
    ```

最后一句话是该函数的核心，这句话分三部分：

1.  `meld(x,y)`「配对」了 x 和 y．
2.  `merges(c)` 递归合并 c 和他的兄弟们．
3.  将上面 2 个操作产生的 2 个新树合并．

需要注意到的是，上文提到了第二步时的合并方向是有要求的（从右往左合并），该递归函数的实现已保证了这个顺序，如果读者需要自行实现迭代版本的话请务必注意保证该顺序，否则复杂度将失去保证．

有了 `merges` 函数，`delete-min` 操作就显然了．

???+ note "实现"
    ```cpp
    Node* delete_min(Node* x) {
      Node* t = merges(x->child);
      delete x;  // 如果需要内存回收
      return t;
    }
    ```

### 减小一个元素的值

要实现这个操作，需要给节点添加一个「父」指针，当节点有左兄弟时，其指向左兄弟而非实际的父节点；否则，指向其父节点．

首先节点的定义修改为：

???+ note "实现"
    ```cpp
    struct Node {
      LL v;
      int id;
      Node *child, *sibling;
      Node *father;  // 新增：父指针，若该节点为根节点则指向空节点 nullptr
    };
    ```

`meld` 操作修改为：

???+ note "实现"
    ```cpp
    Node* meld(Node* x, Node* y) {
      if (x == nullptr) return y;
      if (y == nullptr) return x;
      if (x->v > y->v) std::swap(x, y);
      if (x->child != nullptr) {  // 新增：维护父指针
        x->child->father = y;
      }
      y->sibling = x->child;
      y->father = x;  // 新增：维护父指针
      x->child = y;
      return x;
    }
    ```

`merges` 操作修改为：

???+ note "实现"
    ```cpp
    Node *merges(Node *x) {
      if (x == nullptr) return nullptr;
      x->father = nullptr;  // 新增：维护父指针
      if (x->sibling == nullptr) return x;
      Node *y = x->sibling, *c = y->sibling;
      y->father = nullptr;  // 新增：维护父指针
      x->sibling = y->sibling = nullptr;
      return meld(merges(c), meld(x, y));
    }
    ```

现在我们来考虑如何实现 `decrease-key` 操作．  
首先我们发现，当我们减少节点 `x` 的权值之后，以 `x` 为根的子树仍然满足配对堆性质，但 `x` 的父亲和 `x` 之间可能不再满足堆性质．  
因此我们把整棵以 `x` 为根的子树剖出来，现在两棵树都符合配对堆性质了，然后把他们合并起来，就完成了全部操作．

???+ note "实现"
    ```cpp
    // root为堆的根，x为要操作的节点，v为新的权值，调用时需保证 v <= x->v
    // 返回值为新的根节点
    Node *decrease_key(Node *root, Node *x, LL v) {
      x->v = v;                 // 更新权值
      if (x == root) return x;  // 如果 x 为根，则直接返回
      // 把x从fa的子节点中剖出去，这里要分x的位置讨论一下．
      if (x->father->child == x) {
        x->father->child = x->sibling;
      } else {
        x->father->sibling = x->sibling;
      }
      if (x->sibling != nullptr) {
        x->sibling->father = x->father;
      }
      x->sibling = nullptr;
      x->father = nullptr;
      return meld(root, x);  // 重新合并 x 和根节点
    }
    ```

## 复杂度分析

配对堆结构与实现简单，但时间复杂度分析并不容易．

原论文[^ref1]仅将复杂度分析到 `meld` 和 `delete-min` 操作均为均摊 $O(\log n)$，但提出猜想认为其各操作都有和斐波那契堆相同的复杂度．

遗憾的是，后续发现，不维护额外信息的配对堆，在特定的操作序列下，`decrease-key` 操作的均摊复杂度下界至少为 $\Omega (\log \log n)$[^ref2]．

目前对复杂度上界比较好的估计有，Iacono 的 $O(1)$ `meld`，$O(\log n)$ `decrease-key`[^ref3]；Pettie 的 $O(2^{2 \sqrt{\log \log n}})$ `meld` 和 `decrease-key`[^ref4]．需要注意的是，前述复杂度均为均摊复杂度，因此不能对各结果分别取最小值．

## 参考文献

[^ref1]: [The pairing heap: a new form of self-adjusting heap](http://www.cs.cmu.edu/~sleator/papers/pairing-heaps.pdf)

[^ref2]: [On the efficiency of pairing heaps and related data structures](https://dl.acm.org/doi/10.1145/320211.320214)

[^ref3]: [Improved upper bounds for pairing heaps](https://arxiv.org/abs/1110.4428)

[^ref4]: [Towards a Final Analysis of Pairing Heaps](http://web.eecs.umich.edu/~pettie/papers/focs05.pdf)

-   <https://en.wikipedia.org/wiki/Pairing_heap>
-   <https://brilliant.org/wiki/pairing-heap/>


## ds/persistent-balanced.md

## 可持久化无旋转 Treap

### 前置知识

**OI 常用的可持久化平衡树** 一般就是 **可持久化无旋转 Treap** 所以推荐首先学习 [**无旋转 Treap**](./treap.md)．

### 思想/做法

对于非旋转 Treap，可通过 **Merge** 和 **Split** 操作过程中复制路径上经过的节点（一般在 **Split** 操作中复制，确保不影响以前的版本）就可完成可持久化．

对于旋转 Treap，在复制路径上经过的节点同时，还需复制受旋转影响的节点（若其已为这次操作中复制的节点，则无需再复制），对于一次旋转一般只影响两个节点，那么不会增加其时间复杂度．

上述方法一般被称为 path copying．

「一切可支持操作都可以通过 **Merge Split Newnode Build** 完成」，而 **Build** 操作只用于建造无需理会，**Newnode**（新建节点）就是用来可持久化的工具．

我们来观察一下 **Merge** 和 **Split**，我们会发现它们都是由上而下的操作！

因此我们完全可以 **参考线段树的可持久化操作** 对它进行可持久化．

### 可持久化操作

**可持久化** 是对 **数据结构** 的一种操作，即保留历史信息，使得在后面可以调用之前的历史版本．

对于 **可持久化线段树** 来说，每一次新建历史版本就是把 **沿途的修改路径** 复制出来

那么对可持久化 Treap（目前国内 OI 常用的版本）来说：

在复制一个节点 $X_{a}$（$X$ 节点的第 $a$ 个版本）的新版本 $X_{a+1}$（$X$ 节点的第 $a+1$ 个版本）以后：

-   如果某个儿子节点 $Y$ 不用修改信息，那么就把 $X_{a+1}$ 的指针直接指向 $Y_{a}$（$Y$ 节点的第 $a$ 个版本）即可．
-   反之，如果要修改 $Y$，那么就在 **递归到下层** 时 **新建**  $Y_{a+1}$（$Y$ 节点的第 $a+1$ 个版本）这个新节点用于 **存储新的信息**，同时把 $X_{a+1}$ 的指针指向 $Y_{a+1}$（$Y$ 节点的第 $a+1$ 个版本）．

### 可持久化

需要的东西：

-   一个 `struct` 数组 存 **每个节点** 的信息（一般叫做 `tree` 数组）；（当然写 **指针版** 平衡树的大佬就可以考虑不用这个数组了）

-   一个 **根节点数组**，存每个版本的*树根*，每次查询版本信息时就从 **根数组存的节点** 开始；

-   `split()` 分裂 **从树中分裂出两棵树**

-   `merge()` 合并 **把两棵树按照随机权值合并**

-   `newNode()` 新建一个节点

-   `build()` 建树

#### Split

对于 **分裂操作**，每次分裂路径时 **新建节点** 指向分出来的路径，用 `std::pair` 存新分裂出来的两棵树的根．

`split(x,k)` 返回一个 `std::pair`;

表示把 $_x$ 为根的树的前 $k$ 个元素放在 **一棵树** 中，剩下的节点构成在另一棵树中，返回这两棵树的根（first 是第一棵树的根，second 是第二棵树的）．

-   如果 $x$ 的 **左子树** 的 $key \geq k$，那么 **直接递归进左子树**，把左子树分出来的第二颗树和当前的 $x$  **右子树** 合并．
-   否则递归 **右子树**．

```cpp
static std::pair<int, int> _split(int _x, int k) {
  if (_x == 0)
    return std::make_pair(0, 0);
  else {
    int _vs = ++_cnt;  // 新建节点（可持久化的精髓）
    _trp[_vs] = _trp[_x];
    std::pair<int, int> _y;
    if (_trp[_vs].key <= k) {
      _y = _split(_trp[_vs].leaf[1], k);
      _trp[_vs].leaf[1] = _y.first;
      _y.first = _vs;
    } else {
      _y = _split(_trp[_vs].leaf[0], k);
      _trp[_vs].leaf[0] = _y.second;
      _y.second = _vs;
    }
    _trp[_vs]._update();
    return _y;
  }
}
```

#### Merge

`merge(x,y)` 返回 merge 出的树的根．

同样递归实现．如果 **x 的随机权值**>**y 的随机权值**，则 `merge(x_{rc},y)`，否则 `merge(x,y_{lc})`．

```cpp
static int _merge(int _x, int _y) {
  if (_x == 0 || _y == 0)
    return _x ^ _y;
  else {
    if (_trp[_x].fix < _trp[_y].fix) {
      _trp[_x].leaf[1] = _merge(_trp[_x].leaf[1], _y);
      _trp[_x]._update();
      return _x;
    } else {
      _trp[_y].leaf[0] = _merge(_x, _trp[_y].leaf[0]);
      _trp[_y]._update();
      return _y;
    }
  }
}
```

## 可持久化 WBLT

### 前置知识

可持久化 WBLT 由 WBLT 改动而来，所以首先学习 [WBLT](./wblt.md)．

### 思想/做法

使用 **路径复制** 的方法，将一次操作中 **修改过** 的节点复制下来，不能影响之前的节点．

### 处理懒标记

为了处理懒标记，我们这样考虑：在一棵持久化的 WBLT 上，一个点可能有多个父亲，但是儿子数量只能是 $0$ 或 $2$ 个．pushdown 的下放懒标记的操作，只会影响它的儿子，我们对一个点进行 pushdown，是没有影响的；反而是它的儿子，它的儿子可能不止它一个父亲，将它的标记下放到儿子，可能导致在别的父亲的版本上，多了一个不属于那个版本的懒标记，这就错了；除非它的儿子只有它一个父亲．所以我们应该在 pushdown 的时候，复制一遍儿子，把懒标记打到新的儿子上．

### 实现路径复制

在进行路径复制的时候，我们可以定义一个 refresh 函数，它接受一个节点 $p$ 的引用，表示把节点 $p$ 复制一下，产生一个新的节点，重新赋值给 $p$．使用 refresh 函数的原则是，如果它将要被修改，或者它拥有的儿子即将发生变动（而不是它的儿子的信息将要被修改），那么就 refresh 它，否则不需要．

对于静态的查询，除了 pushdown 之外都不用 refresh．如果保证什么操作都做路径复制，那么 pushdown 和 refresh 的顺序是无所谓的．

### 针对持久化 WBLT 的小优化

这里有一个优化．观察到 pushdown 的时候要复制两个节点，可以写标记永久化，但是刚才说了，如果它的儿子只有它一个父亲，可以不用复制．针对这一个性质，可以进行优化，以减少复制多余的节点．

考虑记录每个节点有多少个父亲（认为每个版本的根都有一个父亲），记为 $use$．每次 refresh 的时候，如果 $use\leq 1$ 则不需要重新复制节点，否则新建节点，并且 $use$ 自减 $1$，表示父亲带着这个儿子跑了，这样父亲就可以随意修改新的节点而不影响其它版本．另外每次复制节点的时候，如果节点有儿子，那么两个儿子的 $use$ 自增 $1$；合并两个子树时，返回的节点对两个儿子也有一个父亲的 $use$；删除节点时，两个子节点都丢失一个父亲：这样能优化一些时空．

### 代码实现

??? note "完整代码（可持久化文艺平衡树）"
    ```cpp
    --8<-- "docs/ds/code/persistent-balanced/persistent-wblt.cpp"
    ```

## 例题

???+ note "[洛谷 P3835【模版】可持久化平衡树](https://www.luogu.com.cn/problem/P3835)"
    你需要实现一个数据结构，要求提供如下操作（最开始时数据结构内无数据）：
    
    1.  插入 $x$ 数；
    2.  删除 $x$ 数（若有多个相同的数，应只删除一个，如果没有请忽略该操作）；
    3.  查询 $x$ 数的排名（排名定义为比当前数小的数的个数 + 1）；
    4.  查询排名为 $x$ 的数；
    5.  求 $x$ 的前驱（前驱定义为小于 $x$，且最大的数，如不存在输出 $-2\,147\,483\,647$）；
    6.  求 $x$ 的后继（后继定义为大于 $x$，且最小的数，如不存在输出 $2\,147\,483\,647$）．
    
    以上操作均基于某一个历史版本，同时生成一个新的版本（操作 3, 4, 5, 6 即保持原版本无变化）．而每个版本的编号则为操作的序号．特别地，最初的版本编号为 0．

就是 **普通平衡树** 一题的可持久化版，操作和该题类似．

只是使用了可持久化的 merge 和 split 操作．

## 推荐的练手题

1.  [「Luogu P3919」可持久化数组（模板题）](https://www.luogu.com.cn/problem/P3919)

2.  [「Codeforces 702F」T-shirt](http://codeforces.com/problemset/problem/702/F)

3.  [「Luogu P5055」可持久化文艺平衡树](https://www.luogu.com.cn/problem/P5055)

4.  [「Luogu P5350」序列](https://www.luogu.com.cn/problem/P5350)


## ds/persistent-heap.md

可持久化可并堆一般用于求解 $k$ 短路问题．

如果一种可并堆的时间复杂度不是均摊的，那么它在可持久化后单次操作的时间复杂度就保证是 $O(\log n)$ 的，即不会因为特殊数据而使复杂度退化．

## 可持久化左偏树

在学习本内容前，请先了解 [左偏树](./leftist-tree.md) 的相关内容．

### 过程

回顾左偏树的合并过程，假设我们要合并分别以 $x,y$ 为根节点的两棵左偏树，且维护的左偏树满足小根堆的性质：

1.  如果 $x,y$ 中有结点为空，返回 $x+y$．

2.  选择 $x,y$ 两结点中权值更小的结点，作为合并后左偏树的根．

3.  递归合并 $x$ 的右子树与 $y$，将合并后的根节点作为 $x$ 的右儿子．

4.  维护当前合并后左偏树的左偏性质，维护 `dist` 值，返回选择的根节点．

由于每次递归都会使 `dist[x]+dist[y]` 减少一，而 `dist[x]` 是 $O(\log n)$ 的，一次最多只会修改 $O(\log n)$ 个结点，所以这样做的时间复杂度是 $O(\log n)$ 的．

可持久化要求保留历史信息，使得之后能够访问之前的版本．要将左偏树可持久化，就要将其沿途修改的路径复制一遍．

所以可持久化左偏树的合并过程是这样的：

1.  如果 $x,y$ 中有结点为空，返回 $x+y$．

2.  选择 $x,y$ 两结点中权值更小的结点，新建该结点的一个复制 $p$，作为合并后左偏树的根．

3.  递归合并 $p$ 的右子树与 $y$，将合并后的根节点作为 $p$ 的右儿子．

4.  维护以 $p$ 为根的左偏树的左偏性质，维护其 `dist` 值，返回 $p$．

由于左偏树一次最多只会修改并新建 $O(\log n)$ 个结点，设操作次数为 $m$，则可持久化左偏树的时间复杂度和空间复杂度均为 $O(m\log n)$．

### 参考实现

```cpp
int merge(int x, int y) {
  if (!x || !y) return x + y;
  if (v[x] > v[y]) swap(x, y);
  int p = ++cnt;
  lc[p] = lc[x];
  v[p] = v[x];
  rc[p] = merge(rc[x], y);
  if (dist[lc[p]] < dist[rc[p]]) swap(lc[p], rc[p]);
  dist[p] = dist[rc[p]] + 1;
  return p;
}
```


## ds/persistent-seg.md

## 主席树

主席树全称是可持久化权值线段树，参见 [知乎讨论](https://www.zhihu.com/question/59195374)．

???+ warning "关于函数式线段树"
    **函数式线段树** 是指使用函数式编程思想的线段树．在函数式编程思想中，将计算机运算视为数学函数，并避免可改变的状态或变量．不难发现，函数式线段树是 [完全可持久化](persistent.md#完全可持久化-fully-persistent) 的．

## 引入

先引入一道题目：给定 $n$ 个整数构成的序列 $a$，将对于指定的闭区间 $[l, r]$ 查询其区间内的第 $k$ 小值．

你该如何解决？

一种可行的方案是：使用主席树．
主席树的主要思想就是：保存每次插入操作时的历史版本，以便查询区间第 $k$ 小．

怎么保存呢？简单暴力一点，每次开一棵线段树呗．  
那空间还不爆掉？

## 解释

我们分析一下，发现每次修改操作修改的点的个数是一样的．  
（例如下图，修改了 $[1,8]$ 中对应权值为 1 的结点，红色的点即为更改的点）  
![](./images/persistent-seg.png)

只更改了 $O(\log{n})$ 个结点，形成一条链，也就是说每次更改的结点数 = 树的高度．  
注意主席树不能使用堆式存储法，就是说不能用 $x\times 2$，$x\times 2+1$ 来表示左右儿子，而是应该动态开点，并保存每个节点的左右儿子编号．  
所以我们只要在记录左右儿子的基础上，保存插入每个数的时候的根节点就可以实现持久化了．

我们把问题简化一下：每次求 $[1,r]$ 区间内的 $k$ 小值．  
怎么做呢？只需要找到插入 r 时的根节点版本，然后用普通权值线段树（有的叫键值线段树/值域线段树）做就行了．

这个相信大家都能理解，回到原问题——求 $[l,r]$ 区间 $k$ 小值．  
这里我们再联系另外一个知识：**前缀和**．  
这个小东西巧妙运用了区间减法的性质，通过预处理从而达到 $O(1)$ 回答每个询问．

我们可以发现，主席树统计的信息也满足这个性质．  
所以……如果需要得到 $[l,r]$ 的统计信息，只需要用 $[1,r]$ 的信息减去 $[1,l - 1]$ 的信息就行了．

至此，该问题解决！

关于空间问题，我们分析一下：由于我们是动态开点的，所以一棵线段树只会出现 $2n-1$ 个结点．  
然后，有 $n$ 次修改，每次至多增加 $\lceil\log_2{n}\rceil+1$ 个结点．因此，最坏情况下 $n$ 次修改后的结点总数会达到 $2n-1+n(\lceil\log_2{n}\rceil+1)$．
此题的 $n \leq 10^5$，单次修改至多增加 $\lceil\log_2{10^5}\rceil+1 = 18$ 个结点，故 $n$ 次修改后的结点总数为 $2\times 10^5-1+18\times 10^5$，忽略掉 $-1$，大概就是 $20\times 10^5$．

最后给一个忠告：千万不要吝啬空间（大多数题目中空间限制都较为宽松，因此一般不用担心空间超限的问题）！大胆一点，直接上个 $2^5\times 10^5$，接近原空间的两倍（即 `n << 5`）．

## 实现

```cpp
#include <algorithm>
#include <cstdio>
#include <cstring>
using namespace std;
constexpr int MAXN = 1e5;  // 数据范围
int tot, n, m;
int sum[(MAXN << 5) + 10], rt[MAXN + 10], ls[(MAXN << 5) + 10],
    rs[(MAXN << 5) + 10];
int a[MAXN + 10], ind[MAXN + 10], len;

int getid(const int &val) {  // 离散化
  return lower_bound(ind + 1, ind + len + 1, val) - ind;
}

int build(int l, int r) {  // 建树
  int root = ++tot;
  if (l == r) return root;
  int mid = l + r >> 1;
  ls[root] = build(l, mid);
  rs[root] = build(mid + 1, r);
  return root;  // 返回该子树的根节点
}

int update(int k, int l, int r, int root) {  // 插入操作
  int dir = ++tot;
  ls[dir] = ls[root], rs[dir] = rs[root], sum[dir] = sum[root] + 1;
  if (l == r) return dir;
  int mid = l + r >> 1;
  if (k <= mid)
    ls[dir] = update(k, l, mid, ls[dir]);
  else
    rs[dir] = update(k, mid + 1, r, rs[dir]);
  return dir;
}

int query(int u, int v, int l, int r, int k) {  // 查询操作
  int mid = l + r >> 1,
      x = sum[ls[v]] - sum[ls[u]];  // 通过区间减法得到左儿子中所存储的数值个数
  if (l == r) return l;
  if (k <= x)  // 若 k 小于等于 x ，则说明第 k 小的数字存储在左儿子中
    return query(ls[u], ls[v], l, mid, k);
  else  // 否则说明在右儿子中
    return query(rs[u], rs[v], mid + 1, r, k - x);
}

void init() {
  scanf("%d%d", &n, &m);
  for (int i = 1; i <= n; ++i) scanf("%d", a + i);
  memcpy(ind, a, sizeof ind);
  sort(ind + 1, ind + n + 1);
  len = unique(ind + 1, ind + n + 1) - ind - 1;
  rt[0] = build(1, len);
  for (int i = 1; i <= n; ++i) rt[i] = update(getid(a[i]), 1, len, rt[i - 1]);
}

int l, r, k;

void work() {
  while (m--) {
    scanf("%d%d%d", &l, &r, &k);
    printf("%d\n", ind[query(rt[l - 1], rt[r], 1, len, k)]);  // 回答询问
  }
}

int main() {
  init();
  work();
  return 0;
}
```

## 拓展：基于主席树的可持久化并查集

主席树是实现可持久化并查集的便捷方式，在此也提供一个基于主席树的可持久化并查集实现示例．

```cpp
--8<-- "docs/ds/code/persistent-seg/persistent-seg_1.cpp"
```

## 参考

<https://en.wikipedia.org/wiki/Persistent_data_structure>

<https://www.cnblogs.com/zinthos/p/3899565.html>


## ds/persistent-trie.md

## 引入

可持久化 Trie 的方式和可持久化线段树的方式是相似的，即每次只修改被添加或值被修改的节点，而保留没有被改动的节点，在上一个版本的基础上连边，使最后每个版本的 Trie 树的根遍历所能分离出的 Trie 树都是完整且包含全部信息的．

大部分的可持久化 Trie 题中，Trie 都是以 [01-Trie](../string/trie.md#维护异或极值) 的形式出现的．

??? note "例题 [最大异或和](https://www.luogu.com.cn/problem/P4735)"
    对一个长度为 $n$ 的数组 $a$ 维护以下操作：
    
    1.  在数组的末尾添加一个数 $x$，数组的长度 $n$ 自增 $1$．
    2.  给出查询区间 $[l,r]$ 和一个值 $k$，求当 $l\le p\le r$ 时，$k \oplus \bigoplus^{n}_{i=p} a_i$ 的最大值．

## 过程

这个求的值可能有些麻烦，利用常用的处理连续异或的方法，记 $s_x=\bigoplus_{i=1}^x a_i$，则原式等价于 $s_{p-1}\oplus s_n\oplus k$，观察到 $s_n \oplus k$ 在查询的过程中是固定的，题目的查询变化为查询在区间 $[l-1,r-1]$ 中异或定值（$s_n\oplus k$）的最大值．

继续按类似于可持久化线段树的思路，考虑每次的查询都查询整个区间．我们只需把这个区间建一棵 Trie 树，将这个区间中的每个树都加入这棵 Trie 中，查询的时候，尽量往与当前位不相同的地方跳．

查询区间，只需要利用前缀和和差分的思想，用两棵前缀 Trie 树（也就是按顺序添加数的两个历史版本）相减即得到该区间的 Trie 树．再利用动态开点的思想，不添加没有计算过的点，以减少空间占用．

```cpp
--8<-- "docs/ds/code/persistent-trie/persistent-trie_1.cpp"
```


## ds/persistent.md

author: morris821028

## 简介

可持久化数据结构 (Persistent data structure) 总是可以保留每一个历史版本，并且支持操作的不可变特性 (immutable)．

## 可持久化分类

### 部分可持久化 (Partially Persistent)

所有版本都可以访问，但是只有最新版本可以修改．

### 完全可持久化 (Fully Persistent)

所有版本都既可以访问又可以修改．

若支持将两个历史版本合并，则又称为 Confluently Persistent

## 实际应用

### 几何计算

在几何计算中有许多离线算法，如扫描线算法一次扫过去回答所有询问，在时间复杂度分析上相当优异．但强迫在线的情况下，每一次都扫描一次，询问操作的时间复杂度就从对数时间降成线性．为了解决这一种情况，持久化技术给了另一种思维，我们将扫描线的时间轴作为一个变动依据，持久化相关的结构，只要我们能将询问在对数时间内穿梭于这个时间轴，必能动态解决先前的问题．

### 字串处理

为了达到非常高效率的合并操作，防止大量重复性字串的生成伴随的效能退化，使得各方面的操作都能远低于线性操作．如 C++ rope 就是一个持久化的数据结构．不只是字串操作，若处理类型有大量重复的情况，持久化的概念便能派上用场．

### 版本回溯

实际上就是对应大部分的应用软体中的 redo/undo．如果资料库/操作变动为了高效率操作而会配上复杂的结构（并不像 hash, set 反转操作只需要常数或对数时间），那么为了快速回推变动结果，持久化结构就是要减少 redo/undo 的花费．

资料库本身可以常数回推，纪录变动的部分情况即可．而应用层的计算，大部分实作都是砍掉快取，并且重新计算出一份新的结构，有时候回推的变动大小为 m，为了重新计算结构而消耗了 n+m，如果 n 和 m 的差距非常大，那连续回推的体感就很糟糕．

### 函数式编程

函数式编程需要特别的数据结构以符合语言特性，其中不可变的性质更为重要，以利于并行环境与除错．如面向对象编程的 Java 8 后引入 stream 类，支援写出函数式的语法设计，可提供惰性求值、无限值域等的特殊功能．

## 参考

-   <https://en.wikipedia.org/wiki/Persistent_data_structure>
-   MIT 课程 <https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-854j-advanced-algorithms-fall-2005/lecture-notes/persistent.pdf>


## ds/pq-tree.md

author: isdanni,xyf007

PQ 树是一种基于树的数据结构，代表一组元素上的一系列排列，由 Kellogg S. Booth 和 George S. Lueker 于 1976 年发现命名，用来解决以下问题

> 给出 $m$ 个集合 $S_i$，你要找到一个 $1\sim n$ 的排列，使得每个集合内的元素都相邻．

PQ 树可以在 $O(n+\sum|S_i|)$ 时间内构建．本文中介绍的构建方法时间复杂度为 $O(nm)$．

## 定义

PQ 树有三种结点：**叶子结点**、**P 结点** 和 **Q 结点**．其中叶子结点代表排列中的一个元素，P 结点表示它的子结点可以任意排列，Q 结点表示它的儿子顺序可以反转．所有非叶子结点都是 P 结点或 Q 结点中的一种．P 结点至少有 2 个儿子，Q 结点至少有 3 个儿子．  
由于结点的定义，PQ 树本身代表了 **所有的** 合法方案，其先序遍历就是其中之一．  
下图是一棵 PQ 树．  
![](https://gregable.com/2008/11/i/pq-tree.webp)  
其先序遍历 1,2,3,4,5 代表了一个合法方案．如果 P 结点的儿子重排列为 4,2,3，我们得到了另一个合法方案 1,4,2,3,5．保持 P 结点儿子顺序不变，Q 结点的儿子顺序反转，得到了另一个合法方案 5,3,2,4,1．

## 构建

**PQ 树使用儿子 - 兄弟表示法．**

我们增量构建一棵 PQ 树．

首先建立一棵树，其根为 P，总共 $n$ 个儿子，分别是 $1,2,\ldots,n$，代表没有任何限制时的 PQ 树．随着限制的不断加入，我们不断修改这棵树．

当加入一个新的限制集合 $S$ 时，我们把所有属于这个集合的叶子结点标记为 **黑色**，不在这个集合内的叶子结点标记为 **白色**．对于所有非叶子结点，如果其所有儿子均为黑色，将其也标记为黑色；如果其所有儿子均为白色，将其也标记为白色；否则将其标记为 **灰色**．在下面的图中，黑色结点、白色结点、灰色结点分别用黑色、灰色、一半黑一半灰来表示．

我们要求 PQ 树中的结点按照颜色排序．

### 自底向上法

包含所有黑色结点的最小子树被称为 **相关子树**，相关子树的根（不一定是整棵树的根）被称为 **相关根**．

添加一个限制的过程被称为 reduction．一次 reduction 分为两个阶段：冒泡阶段和减少阶段．

#### 冒泡阶段

冒泡阶段只处理相关子树．我们将相关子树中的所有结点标记为黑色或灰色，并为每个结点计算其拥有的相关子结点数量．为了高效地完成这个过程，我们从叶子往根处理相关子树．这需要记录每个点的父亲结点，但在减少阶段一个点的父亲结点经常要被修改．为了在线性时间内构造，只有 P 结点的儿子和 **Q 结点的最后一个儿子** 始终记录正确的父亲结点．对于 Q 结点的其他儿子，在冒泡阶段用最后一个儿子的父亲更新他们的父亲．

当遇到一个中间的结点时，我们看一下它的兄弟是否已经有合法的父亲结点．如果没有，将其标记为 **阻塞** 的．如果后面它的兄弟有了合法的父亲，那么修改这个结点的父亲并且取消标记．如果在冒泡阶段结束时，仍然有一段连续的阻塞结点（如下面的情况 Q3），一个没有父结点的「伪结点」成为该块的父结点，并在减少阶段时被去除．

#### 减少阶段

减少阶段用一个队列来处理结点．首先将所有限制内的叶子结点加入队列．每次取出队首的结点 $u$ 并处理．如果 $u$ 的父亲也是相关子树内的结点，那么将 $\mathit{fa}_u$ 入队．  
对于每一个结点 $u$，我们分情况讨论．如果不属于其中任何一种情况，则无解．

##### 叶子结点

将 $u$ 标记为黑色．

##### P 结点

如果所有儿子均为黑色，将 $u$ 标记为黑色．  
![](https://gregable.com/2008/11/i/p1-template.png)  
![](https://gregable.com/2008/11/i/p1-replacement.png)

如果 $u$ 有黑色儿子和白色儿子，且 $u$ 是相关根，那么新建一个 P 结点 $v$ 成为它所有黑色儿子的根．  
![](https://gregable.com/2008/11/i/p2-template.png)  
![](https://gregable.com/2008/11/i/p2-replacement.png)

如果 $u$ 有黑色儿子和白色儿子，且 $u$ 不是相关根，那么做以下操作：

-   新建一个 P 结点 $f$ 成为所有黑色儿子的根．
-   新建一个 P 结点 $e$ 成为所有白色儿子的根．
-   如果 $e$（和/或 $f$）只有一个儿子，那么不要新建结点，而是将 $e$（和/或 $f$）直接赋值成那个儿子．
-   将 $u$ 改成 Q 结点并把其儿子设为 $e$ 和 $f$，将其标记为灰色．

注意到根据之前的定义，Q 结点至少有 3 个儿子，因此这里的 $u$ 被视为一个「伪结点」，并且将在后面被继续处理．  
![](https://gregable.com/2008/11/i/p3-template.png)  
![](https://gregable.com/2008/11/i/p3-replacement.png)

如果 $u$ 有一个灰色儿子 $p$，且 $u$ 是相关根，那么新建一个 P 结点 $v$ 作为其所有黑色儿子的根，将 $v$ 的兄弟设为 $p$ 最后一个一个黑色儿子，然后把 $v$ 设为 $p$ 的最后一个儿子．  
![](https://gregable.com/2008/11/i/p4-template.png)  
![](https://gregable.com/2008/11/i/p4-replacement.png)

如果 $u$ 有一个灰色儿子 $p$，且 $u$ 不是相关根，那么进行以下操作：

-   新建一个 P 结点 $f$ 成为所有黑色儿子的根．
-   新建一个 P 结点 $e$ 成为所有白色儿子的根．
-   如果 $e$（和/或 $f$）只有一个儿子，那么不要新建结点，而是将 $e$（和/或 $f$）直接赋值成那个儿子．
-   将 $e$ 的兄弟设为 $p$ 最后一个白色儿子，然后把 $e$ 设为 $p$ 的最后一个儿子．
-   将 $f$ 的兄弟设为 $p$ 最后一个黑色儿子，然后把 $f$ 设为 $p$ 的最后一个儿子．

![](https://gregable.com/2008/11/i/p5-template.png)  
![](https://gregable.com/2008/11/i/p5-replacement.png)

如果 $u$ 恰有两个灰色儿子 $p_1,p_2$，那么进行以下操作：

-   新建一个 P 结点 $f$ 成为所有黑色儿子的根．
-   如果 $f$ 只有一个儿子，那么不要新建结点，而是将 $f$ 直接赋值成那个儿子．
-   把 $p_1$ 的最后一个黑色儿子的兄弟设为 $f$．
-   把 $f$ 的兄弟设为 $p_2$ 的最后一个黑色儿子．
-   把 $p_2$ 的最后一个儿子设为 $p_2$ 的最后一个白色儿子．

可以发现这样 $p_2$ 就被合并进了 $p_1$．  
![](https://gregable.com/2008/11/i/p6-template.png)  
![](https://gregable.com/2008/11/i/p6-replacement.png)

##### Q 结点

如果 $u$ 只有黑色儿子，那么将 $u$ 标记成黑色．（下面的图的形状错了．）  
![](https://gregable.com/2008/11/i/q1-template.png)  
![](https://gregable.com/2008/11/i/q1-replacement.png)

如果 $u$ 有一个灰色儿子 $p$，且所有标记相同的儿子均连续出现，那么进行如下操作：

-   设 $p_f$ 为 $p$ 最后一个黑色儿子，$p_e$ 为 $p$ 最后一个白色儿子，$f$ 为 $p$ 的黑色兄弟，$e$ 为 $p$ 的白色兄弟．
-   将 $f$ 的兄弟设为 $p_f$，$e$ 的兄弟设为 $p_e$．
-   如果 $p$ 没有一个白色兄弟或黑色兄弟，将 $u$ 的最后一个儿子设成 $p$ 的最后一个儿子．
-   删除 $p$．

![](https://gregable.com/2008/11/i/q2-template.png)  
![](https://gregable.com/2008/11/i/q2-replacement.png)

如果 $u$ 恰有两个灰色儿子 $p_1,p_2$，且所有标记相同的儿子均连续出现，那么对 $p_1,p_2$ 都进行上一种操作即可．  
![](https://gregable.com/2008/11/i/q3-template.png)  
![](https://gregable.com/2008/11/i/q3-replacement.png)

该构建方法是原论文中的，但是实现较为不便．

### 自顶向下法

目前 OI 中的实现大多采用该方法．其实方法类似，下面出现的情况基本都能在上面找到．

注意到根据之前的染色过程，所有黑色和白色的点都已经满足条件，因此我们 **只需要处理灰色结点**．

#### P 结点

-   如果 $u$ 有多于两个灰色儿子，无解．
-   如果 $u$ 只有一个灰色儿子，且没有黑色儿子，递归处理灰色儿子．
-   否则先清空 $u$ 的儿子，然后加入所有的白色儿子．新建一个 Q 结点 $q_1$ 并成为 $u$ 的儿子．在 $q_1$ 中加入所有的灰色儿子．新建一个 P 结点 $p$ 作为所有黑色儿子的根，将 $p$ 插入 $q_1$ 的中间．（对应了自底向上法 P 结点的所有情况．）

注意到我们会要求两个灰色节点白色全在左侧，黑色全在右侧（或相反），因此我们需要实现一个分裂函数 `split`，可以把这个子树的点分裂成黑白部分，并同时保留分裂成的子树的节点的 **所有可能**．

#### Q 结点

-   找到最左边和最右边的非白色节点位置 $l,r$．如果 $[l+1,r-1]$ 内有非黑色节点，无解．
-   如果没有黑色节点，只有一个灰色节点，递归处理这个灰色节点，否则只需要将 $l$ 和 $r$ 位置的节点分裂．

#### 分裂函数

令要分裂的点为 $u$，我们想把 $u$ 分裂成左边全是白色，右边全是黑色的森林．如果 $u$ 不是灰色结点则直接返回子树．只考虑灰色结点的情况．
如果 $u$ 是 P 类结点：

-   如果 $u$ 有至少两个灰色儿子，则无解．
-   否则左边是所有白色儿子，中间递归处理灰色儿子，右边是所有黑色儿子．注意到要保留所有的可能，因此要新建两个 P 结点分别作为白色儿子和黑色儿子的根．（对应自底向上法的 P4 情况．）
-   删除 $u$．

如果 $u$ 是 Q 类结点：

-   如果正序和反序都不满足白 - 灰 - 黑，则无解．
-   如果有至少两个灰色儿子，也无解．
-   否则递归分裂灰色儿子即可．
-   删除 $u$．

最后把所有多余的结点（只有一个儿子的结点）删除．

## 代码实现

```cpp
class PQTree {
 public:
  PQTree() {}

  void Init(int n) {
    n_ = n, rt_ = tot_ = n + 1;
    for (int i = 1; i <= n; i++) g_[rt_].emplace_back(i);
  }

  void Insert(const std::string &s) {
    s_ = s;
    Dfs0(rt_);
    Work(rt_);
    while (g_[rt_].size() == 1) rt_ = g_[rt_][0];
    Remove(rt_);
  }

  std::vector<int> ans() {
    DfsAns(rt_);
    return ans_;
  }

  ~PQTree() {}

 private:
  int n_, rt_, tot_, pool_[100001], top_, typ_[100001] /* 0-P 1-Q */,
      col_[100001] /* 0-black 1-white 2-grey */;
  std::vector<int> g_[100001], ans_;
  std::string s_;

  void Fail() {
    std::cout << "NO\n";
    std::exit(0);
  }

  int NewNode(int ty) {
    int x = top_ ? pool_[top_--] : ++tot_;
    typ_[x] = ty;
    return x;
  }

  void Delete(int u) { g_[u].clear(), pool_[++top_] = u; }

  void Dfs0(int u) {  // get color of each node
    if (u >= 1 && u <= n_) {
      col_[u] = s_[u] == '1';
      return;
    }
    bool c0 = false, c1 = false;
    for (auto &&v : g_[u]) {
      Dfs0(v);
      if (col_[v]) c1 = true;
      if (col_[v] != 1) c0 = true;
    }
    if (c0 && !c1)
      col_[u] = 0;
    else if (!c0 && c1)
      col_[u] = 1;
    else
      col_[u] = 2;
  }

  bool Check(const std::vector<int> &v) {
    int p2 = -1;
    for (int i = 0; i < static_cast<int>(v.size()); i++)
      if (col_[v[i]] == 2) {
        if (p2 != -1) return false;
        p2 = i;
      }
    if (p2 == -1)
      for (int i = 0; i < static_cast<int>(v.size()); i++)
        if (col_[v[i]]) {
          p2 = i;
          break;
        }
    for (int i = 0; i < p2; i++)
      if (col_[v[i]]) return false;
    for (int i = p2 + 1; i < static_cast<int>(v.size()); i++)
      if (col_[v[i]] != 1) return false;
    return true;
  }

  std::vector<int> Split(int u) {
    if (col_[u] != 2) return {u};
    std::vector<int> ng;
    if (typ_[u]) {  // Q
      if (!Check(g_[u])) {
        std::reverse(g_[u].begin(), g_[u].end());
        if (!Check(g_[u])) Fail();
      }
      for (auto &&v : g_[u])
        if (col_[v] != 2) {
          ng.emplace_back(v);
        } else {
          auto s = Split(v);
          ng.insert(ng.end(), s.begin(), s.end());
        }
    } else {  // P
      std::vector<int> son[3];
      for (auto &&x : g_[u]) son[col_[x]].emplace_back(x);
      if (son[2].size() > 1) Fail();
      if (!son[0].empty()) {
        int n0 = NewNode(0);
        g_[n0] = son[0];
        ng.emplace_back(n0);
      }
      if (!son[2].empty()) {
        auto s = Split(son[2][0]);
        ng.insert(ng.end(), s.begin(), s.end());
      }
      if (!son[1].empty()) {
        int n1 = NewNode(0);
        g_[n1] = son[1];
        ng.emplace_back(n1);
      }
    }
    Delete(u);
    return ng;
  }

  void Work(int u) {
    if (col_[u] != 2) return;
    if (typ_[u]) {  // Q
      int l = 1e9, r = -1e9;
      for (int i = 0; i < static_cast<int>(g_[u].size()); i++)
        if (col_[g_[u][i]]) checkmin(l, i), checkmax(r, i);
      for (int i = l + 1; i < r; i++)
        if (col_[g_[u][i]] != 1) Fail();
      if (l == r && col_[g_[u][l]] == 2) {
        Work(g_[u][l]);
        return;
      }
      std::vector<int> ng;
      for (int i = 0; i < l; i++) ng.emplace_back(g_[u][i]);
      auto s = Split(g_[u][l]);
      ng.insert(ng.end(), s.begin(), s.end());
      for (int i = l + 1; i < r; i++) ng.emplace_back(g_[u][i]);
      if (l != r) {
        s = Split(g_[u][r]);
        std::reverse(s.begin(), s.end());
        ng.insert(ng.end(), s.begin(), s.end());
      }
      for (int i = r + 1; i < static_cast<int>(g_[u].size()); i++)
        ng.emplace_back(g_[u][i]);
      g_[u] = ng;
    } else {  // P
      std::vector<int> son[3];
      for (auto &&x : g_[u]) son[col_[x]].emplace_back(x);
      if (son[1].empty() && son[2].size() == 1) {
        Work(son[2][0]);
        return;
      }
      g_[u].clear();
      if (son[2].size() > 2) Fail();
      g_[u] = son[0];
      int n1 = NewNode(1);
      g_[u].emplace_back(n1);
      if (son[2].size() >= 1) {
        auto s = Split(son[2][0]);
        g_[n1].insert(g_[n1].end(), s.begin(), s.end());
      }
      if (son[1].size()) {
        int n2 = NewNode(0);
        g_[n1].emplace_back(n2);
        g_[n2] = son[1];
      }
      if (son[2].size() >= 2) {
        auto s = Split(son[2][1]);
        std::reverse(s.begin(), s.end());
        g_[n1].insert(g_[n1].end(), s.begin(), s.end());
      }
    }
  }

  void Remove(int u) {  // remove the nodes with only one child
    for (auto &&v : g_[u]) {
      int tv = v;
      while (g_[tv].size() == 1) {
        int t = tv;
        tv = g_[tv][0];
        Delete(t);
      }
      v = tv, Remove(v);
    }
  }

  void DfsAns(int u) {
    if (u >= 1 && u <= n_) {
      ans_.emplace_back(u);
      return;
    }
    for (auto &&v : g_[u]) DfsAns(v);
  }
} T;
```

## 习题

-   [CF243E Matrix](https://codeforces.com/problemset/problem/243/E)
-   [CF1552I Organizing a Music Festival](https://codeforces.com/contest/1552/problem/I)

## 参考资料

-   Booth, Kellogg S. & Lueker, George S. (1976).["Testing for the consecutive ones property, interval graphs, and graph planarity using PQ-tree algorithms"](https://www.sciencedirect.com/science/article/pii/S0022000076800451?via%3Dihub).*[Journal of Computer and System Sciences](https://en.wikipedia.org/wiki/Journal_of_Computer_and_System_Sciences)*.**13**(3): 335–379.[doi](https://en.wikipedia.org/wiki/Doi_%28identifier%29):[10.1016/S0022-0000(76)80045-1](https://doi.org/10.1016%2FS0022-0000%2876%2980045-1).
-   [PQ Tree Algorithm and Consecutive Ones Problem](https://gregable.com/2008/11/pq-tree-algorithm.html)
-   [CF243E Matrix PQTree - RainAir's Blog](https://blog.aor.sd.cn/archives/1657/)


## ds/queue.md

本页面介绍和队列有关的数据结构及其应用．

![](./images/queue.svg)

## 引入

队列（queue）是一种具有「先进入队列的元素一定先出队列」性质的表．由于该性质，队列通常也被称为先进先出（first in first out）表，简称 FIFO 表．

## 实现

### 数组模拟队列

通常用一个数组模拟一个队列，用两个变量标记队列的首尾．

```cpp
int q[SIZE], ql = 1, qr;
```

队列操作对应的代码如下：

-   插入元素：`q[++qr] = x;`
-   删除元素：`ql++;`
-   访问队首：`q[ql]`
-   访问队尾：`q[qr]`
-   清空队列：`ql = 1; qr = 0;`

??? example "[Luogu B3616【模板】队列](https://www.luogu.com.cn/problem/B3616) 数组模拟参考实现"
    ```cpp
    --8<-- "docs/ds/code/queue/queue_1.cpp"
    ```

### 双栈模拟队列

还有一种冷门的方法是使用两个 [栈](./stack.md) 来模拟一个队列．

这种方法使用两个栈 $F$ 和 $S$ 模拟一个队列，其中 $F$ 是队尾的栈，$S$ 代表队首的栈，支持 push（在队尾插入），pop（在队首弹出）操作：

-   push：插入到栈 $F$ 中．
-   pop：如果 $S$ 非空，让 $S$ 弹栈；否则把 $F$ 的元素倒过来压到 $S$ 中（其实就是一个一个弹出插入，做完后是首尾颠倒的），然后再让 $S$ 弹栈．

容易证明，每个元素只会进入/转移/弹出一次，均摊复杂度 $O(1)$．

??? example "[Luogu B3616【模板】队列](https://www.luogu.com.cn/problem/B3616) 双栈模拟参考实现"
    ```cpp
    --8<-- "docs/ds/code/queue/queue_2.cpp"
    ```

## C++ STL 中的队列

C++ 在 STL 中提供了一个容器 `std::queue`，使用前需要先引入 `<queue>` 头文件．

???+ info "STL 中对 `queue` 的定义"
    ```cpp
    // clang-format off
    template<
        class T,
        class Container = std::deque<T>
    > class queue;
    ```
    
    `T` 为 queue 中要存储的数据类型．
    
    `Container` 为用于存储元素的底层容器类型．这个容器必须提供通常语义的下列函数：
    
    -   `back()`
    -   `front()`
    -   `push_back()`
    -   `pop_front()`
    
    STL 容器 `std::deque` 和 `std::list` 满足这些要求．如果不指定，则默认使用 `std::deque` 作为底层容器．

STL 中的 `queue` 容器提供了一众成员函数以供调用．其中较为常用的有：

-   元素访问
    -   `q.front()` 返回队首元素
    -   `q.back()` 返回队尾元素
-   修改
    -   `q.push()` 在队尾插入元素
    -   `q.pop()` 弹出队首元素
-   容量
    -   `q.empty()` 队列是否为空
    -   `q.size()` 返回队列中元素的数量

此外，`queue` 还提供了一些运算符．较为常用的是使用赋值运算符 `=` 为 `queue` 赋值，示例：

```cpp
std::queue<int> q1, q2;

// 向 q1 的队尾插入 1
q1.push(1);

// 将 q1 赋值给 q2
q2 = q1;

// 输出 q2 的队首元素
std::cout << q2.front() << std::endl;
// 输出: 1
```

## 特殊队列

### 双端队列

双端队列是指一个可以在队首/队尾插入或删除元素的队列．相当于是栈与队列功能的结合．具体地，双端队列支持的操作有 4 个：

-   在队首插入一个元素
-   在队尾插入一个元素
-   在队首删除一个元素
-   在队尾删除一个元素

数组模拟双端队列的方式与普通队列相同．

同样地，也可以使用双栈模拟队列的思想来维护双端队列，但需注意当某个栈为空时，交替查询队首和队尾将导致均摊分析失效．考虑在移动时，只将非空栈的一半元素移动到空栈中，并保持队首与队尾栈的性质，这样处理后仍可以做到均摊常数时间的插入和删除．

??? note "简要证明"
    由于插入操作只贡献常数复杂度，现在考虑弹出操作．假设初始时队列中有 $m$ 个元素，下面我们计算将所有元素全部弹出（无论首尾）的时间复杂度．则第一次平衡的复杂度是 $O(m)$ 的．然后两个栈就各有 $\frac{m}{2}$ 个元素．这时就需要 $O(\frac{m}{2})$ 的时间清空其中一个栈，然后就又可以触发一次复杂度为 $O(\frac{m}{2})$ 的平衡操作，以此类推，直到所有元素被弹出．因此，这样做的总复杂度是
    
    $$
    T(m)=T\left(\frac{m}{2}\right)+O(m)
    $$
    
    根据主定理，解得 $T(m)=O(m)$．于是，这种维护方式的总复杂度仍是均摊常数的．

??? example "[Luogu B3656【模板】双端队列 1](https://www.luogu.com.cn/problem/B3656) 参考实现"
    ```cpp
    --8<-- "docs/ds/code/queue/queue_3.cpp"
    ```

#### C++ STL 中的双端队列

C++ 在 STL 中也提供了一个容器 `std::deque`，使用前需要先引入 `<deque>` 头文件．

??? info "STL 中对 `deque` 的定义"
    ```cpp
    // clang-format off
    template<
        class T,
        class Allocator = std::allocator<T>
    > class deque;
    ```
    
    `T` 为 deque 中要存储的数据类型．
    
    `Allocator` 为分配器，此处不做过多说明，一般保持默认即可．

STL 中的 `deque` 容器提供了一众成员函数以供调用．其中较为常用的有：

-   元素访问
    -   `q.front()` 返回队首元素
    -   `q.back()` 返回队尾元素
-   修改
    -   `q.push_back()` 在队尾插入元素
    -   `q.pop_back()` 弹出队尾元素
    -   `q.push_front()` 在队首插入元素
    -   `q.pop_front()` 弹出队首元素
    -   `q.insert()` 在指定位置前插入元素（传入迭代器和元素）
    -   `q.erase()` 删除指定位置的元素（传入迭代器）
-   容量
    -   `q.empty()` 队列是否为空
    -   `q.size()` 返回队列中元素的数量

此外，`deque` 还提供了一些运算符．其中较为常用的有：

-   使用赋值运算符 `=` 为 `deque` 赋值，类似 `queue`．
-   使用 `[]` 访问元素，类似 `vector`．

`<queue>` 头文件中还提供了优先队列 `std::priority_queue`，因其与 [堆](./heap.md) 更为相似，在此不作过多介绍．

#### Python 中的双端队列

在 Python 中，双端队列的容器由 `collections.deque` 提供．

示例如下：

???+ note "实现"
    ```python
    from collections import deque
    
    # 新建一个 deque，并初始化内容为 [1, 2, 3]
    queue = deque([1, 2, 3])
    
    # 在队尾插入元素 4
    queue.append(4)
    
    # 在队首插入元素 0
    queue.appendleft(0)
    
    # 访问队列
    # >>> queue
    # deque([0, 1, 2, 3, 4])
    ```

### 循环队列

使用数组模拟队列会导致一个问题：随着时间的推移，整个队列会向数组的尾部移动，一旦到达数组的最末端，即使数组的前端还有空闲位置，再进行入队操作也会导致溢出（这种数组里实际有空闲位置而发生了上溢的现象被称为「假溢出」）．

解决假溢出的办法是采用循环的方式来组织存放队列元素的数组，即将数组下标为 0 的位置看做是最后一个位置的后继．（数组下标为 `x` 的元素，它的后继为 `(x + 1) % SIZE`）．这样就形成了循环队列．

## 参考资料

1.  [std::queue - zh.cppreference.com](https://zh.cppreference.com/w/cpp/container/queue)
2.  [std::deque - zh.cppreference.com](https://zh.cppreference.com/w/cpp/container/deque)


## ds/rbtree.md

author: 0x03A6, abc1763613206, auuuu4, CCXXXI, Conless, Enter-tainer, fanenr, happyZYM, hsfzLZH1, iamtwz, LeverImmy, leverimmy, Lhcfl, Marcythm, RIvance, Tiphereth-A, trudbot, Xeniume, Xeonacid, YBYCS, yuhuoji

红黑树是一种自平衡的二叉搜索树．每个节点额外存储了一个 color 字段 ("RED" or "BLACK")，用于确保树在插入和删除时保持平衡．

红黑树是 4 阶 B 树（[2-3-4 树](https://en.wikipedia.org/wiki/2%E2%80%933%E2%80%934_tree)）的变体．[^gilbas1978]

## 性质

一棵合法的红黑树必须遵循以下四条性质：

1.  节点为红色或黑色
2.  NIL 节点（空叶子节点）为黑色
3.  红色节点的子节点为黑色
4.  从根节点到 NIL 节点的每条路径上的黑色节点数量相同

下图为一棵合法的红黑树：

![rbtree-example](images/rbtree-example.svg)

???+ note "Note"
    部分资料中还加入了第五条性质，即根节点必须为黑色，这条性质要求完成插入操作后若根节点为红色则将其染黑，但由于将根节点染黑的操作也可以延迟至删除操作时进行，因此，该条性质并非必须满足（本文给出的代码实现中满足该性质）．为严谨起见，这里同时引用 [维基百科原文](https://en.wikipedia.org/wiki/Red%E2%80%93black_tree#Properties) 进行说明：
    
    > Some authors, e.g. Cormen & al.,[^cite_note-cormen2009-18]claim "the root is black" as fifth requirement; but not Mehlhorn & Sanders[^cite_note-mehlhorn2008-17]or Sedgewick & Wayne.[^cite_note-algs4-16]Since the root can always be changed from red to black, this rule has little effect on analysis. This article also omits it, because it slightly disturbs the recursive algorithms and proofs.

## 红黑树类的定义

```cpp
--8<-- "docs/ds/code/rbtree/rbtree.hpp:class-node1"
  // ...
--8<-- "docs/ds/code/rbtree/rbtree.hpp:class-node2"
```

???+ note "Note"
    在红黑树节点的存储中，用数组来存储子节点指针可以提高代码复用率．

## 操作

???+ note "Note"
    红黑树的插入/删除有多种实现方式，本文采用《算法导论》的实现方式，将插入后的平衡维护分为 3 种情况，删除后的平衡维护分为 4 种情况．

红黑树的遍历、查找最小/最大值、搜索元素、求元素的排名、根据排名反查元素、查找前驱/后继等操作和 [二叉搜索树](./bst.md) 一致，此处不再赘述．

另外，在下文插入/删除平衡维护的代码注释中，我们作如下约定：

-   用 `p` 表示节点 `p` 为黑色；
-   用 `[p]` 表示节点 `p` 为红色；
-   用 `{p}` 表示节点 `p` 为红色或黑色；
-   用 `|p|` 表示节点 `p` 为 NIL 节点或颜色为黑色．

### 旋转

旋转操作是多数平衡树能够维持平衡的关键，它能在不改变一棵合法 BST 中序遍历结果的情况下改变局部节点的深度．

![rbtree-rotations](images/rbtree-rotate.svg)

???+ note "实现"
    ```cpp
    --8<-- "docs/ds/code/rbtree/rbtree.hpp:rotate"
    ```

### 插入

红黑树的插入操作与普通的 BST 类似，对于红黑树来说，新插入的节点初始为红色，完成插入后需根据插入节点及相关节点的状态进行修正以满足上文提到的四条性质．

???+ note "实现"
    ```cpp
    --8<-- "docs/ds/code/rbtree/rbtree.hpp:insert"
    --8<-- "docs/ds/code/rbtree/rbtree.hpp:insert-leaf"
    --8<-- "docs/ds/code/rbtree/rbtree.hpp:insert-fixup1"
        // ...
    --8<-- "docs/ds/code/rbtree/rbtree.hpp:insert-fixup2"
    ```

### 插入后的平衡维护

???+ note "Note"
    为加深理解，请读者自行验证平衡维护后是否满足性质 4．

由于插入的节点若不为根节点则必为红色，所以插入后可能违反性质 3，需要维护平衡性．

令插入的节点为 $n$，其父节点为 $p$，祖父节点为 $g$，叔节点为 $u$．由性质 3 可知 $g$ 必为黑色．

我们从插入的位置开始向上递归维护，若 $p$ 为黑色即可终止，否则分为 3 种情况．

```cpp
--8<-- "docs/ds/code/rbtree/rbtree.hpp:insert-aux1"
      // ...
--8<-- "docs/ds/code/rbtree/rbtree.hpp:insert-aux2"
```

#### Insert case 1

$p$ 和 $u$ 均为红色．此时我们只需重新染色即可．

![](images/rbtree-insert-case1.svg)

???+ note "实现"
    ```cpp
    --8<-- "docs/ds/code/rbtree/rbtree.hpp:insert-case1"
    ```

#### Insert case 2

$p$ 为红色，$u$ 为黑色，$p$ 的方向和 $n$ 的方向不同．

此时我们需要旋转 $p$ 节点来转为第三种情况．

![](images/rbtree-insert-case2.svg)

???+ note "实现"
    ```cpp
    --8<-- "docs/ds/code/rbtree/rbtree.hpp:insert-case2"
    ```

#### Insert case 3

$p$ 为红色，$u$ 为黑色，$p$ 的方向和 $n$ 的方向相同．

此时我们需要旋转 $g$ 节点以将 $p$ 转为子树的根，之后交换 $p$ 和 $g$ 的颜色即可．

![](images/rbtree-insert-case3.svg)

???+ note "实现"
    ```cpp
    --8<-- "docs/ds/code/rbtree/rbtree.hpp:insert-case3"
    ```

### 删除

红黑树的删除操作与普通的 BST 相比要多一些步骤．具体而言：

-   若待删除的节点 $n$ 有两个子节点，则交换 $n$ 和右子树中最小节点 $s$ 的数据，并将 $n$ 设为 $s$．此时 $n$ 不可能有两个子节点．
-   若待删除的节点 $n$ 有一个子节点 $s$．由性质 4 可知 $s$ 必为红色，再由性质 3 可知 $n$ 必为黑色．所以只需将 $n$ 在父节点 $p$ 中对应的指针替换为 $s$ 的地址，以及将 $s$ 的父节点指针替换为 $p$ 的地址，之后再将 $s$ 染黑即可．
-   若待删除的节点 $n$ 没有子节点．若 $n$ 是根节点或 $n$ 是红色节点，则直接删除即可，否则直接删除会违反性质 4，需要维护平衡性．

???+ note "实现"
    ```cpp
    --8<-- "docs/ds/code/rbtree/rbtree.hpp:delete"
    --8<-- "docs/ds/code/rbtree/rbtree.hpp:delete-leaf"
    --8<-- "docs/ds/code/rbtree/rbtree.hpp:delete-fixup1"
        // ...
    --8<-- "docs/ds/code/rbtree/rbtree.hpp:delete-fixup2"
    ```

### 删除后的平衡维护

???+ note "Note"
    为加深理解，请读者自行验证平衡维护后是否满足性质 4．

由上文讨论可知 $n$ 是黑色叶子节点且不为根节点．我们设 $n$ 的父节点为 $p$，兄弟节点为 $s$，侄节点分别为 $c$ 和 $d$．

删除的维护也是从 $n$ 开始向上递归维护，若 $n$ 是根或 $n$ 为红色即可终止，否则分为 4 种情况．

```cpp
--8<-- "docs/ds/code/rbtree/rbtree.hpp:delete-aux1"
      // Delete case 1
      // ...
      // Other cases
--8<-- "docs/ds/code/rbtree/rbtree.hpp:delete-aux2"
      // ...
--8<-- "docs/ds/code/rbtree/rbtree.hpp:delete-aux3"
```

#### Delete case 1

$s$ 为红色．

此时我们旋转 $p$，将 $s$ 转为子树根节点，之后交换 $s$ 和 $p$ 的颜色来转为其余三种情况之一．

![](images/rbtree-remove-case1.svg)

???+ note "实现"
    ```cpp
    --8<-- "docs/ds/code/rbtree/rbtree.hpp:delete-case1"
    ```

#### Delete case 2

$p$ 的颜色不确定，$s$、$c$、$d$ 均为黑色．

此时只需将 $s$ 染红即可．

![](images/rbtree-remove-case2.svg)

需要注意的是，若 $p$ 为红色则会违反性质 3，但是若 $p$ 为红色则会直接退出循环，所以我们在最后将其染黑．

???+ note "实现"
    ```cpp
    --8<-- "docs/ds/code/rbtree/rbtree.hpp:delete-case2"
    ```

#### Delete case 3

$p$ 的颜色不确定，$s$、$d$ 均为黑色，$c$ 为红色．

此时需要旋转 $s$ 使 $c$ 为原来 $s$ 对应子树的根节点，并交换 $s$ 和 $c$ 的颜色转为第四种情况即可．

![](images/rbtree-remove-case3.svg)

???+ note "实现"
    ```cpp
    --8<-- "docs/ds/code/rbtree/rbtree.hpp:delete-case3"
    ```

#### Delete case 4

$p$、$c$ 的颜色不确定，$s$ 为黑色，$d$ 为红色．

此时需要旋转 $p$ 使 $s$ 为子树的根节点，交换 $s$ 和 $p$ 的颜色，并将 $d$ 染黑即可终止维护平衡．

![](images/rbtree-remove-case4.svg)

???+ note "实现"
    ```cpp
    --8<-- "docs/ds/code/rbtree/rbtree.hpp:delete-case4"
    ```

## 参考代码

下面的代码是用红黑树实现的 set：

??? note "实现"
    ```cpp
    --8<-- "docs/ds/code/rbtree/rbtree.hpp:full"
    ```

??? note "例题：[Luogu P3369【模板】普通平衡树](https://www.luogu.com.cn/problem/P3369) 与 [Luogu P6136【模板】普通平衡树（数据加强版）](https://www.luogu.com.cn/problem/P6136)"
    ```cpp
    --8<-- "docs/ds/code/rbtree/rbtree.hpp:class"
    --8<-- "docs/ds/code/rbtree/rbtree_1.cpp:main"
    ```

## 与 2-3-4 树的关系

2-3-4 树是 4 阶 B 树，与一般的 B 树一样，2-3-4 树可以实现在 $O(\log n)$ 时间内进行搜索、插入和删除操作．2-3-4 树的节点分为三种，2 节点、3 节点和 4 节点，分别包含一个、两个或三个数据元素．所有的叶子节点都处于同一深度（最底层），所有数据都有序存储．

2-3-4 树和红黑树是同构的，任意一棵红黑树都唯一对应一棵 2-3-4 树．在 2-3-4 树上的插入和删除操作导致节点的扩展、分裂和合并，相当于红黑树中的变色和旋转．下图是 2-3-4 树的 2 节点、3 节点和 4 节点对应的红黑树节点．注意到 2-3-4 树的 3 节点对应红黑树中红色节点左偏和右偏两种情况，所以一棵红黑树可能对应多棵 2-3-4 树．

![2-3-4-tree-rbt-1](images/2-3-4-tree-rbt-1.svg)

下图是一棵红黑树和与之对应的 2-3-4 树．将红黑树中的红色节点上移到父节点的左右两侧，形成一个 B 树节点，就可以得到与之对应的 2-3-4 树．可以发现，红黑树的节点数等于 2-3-4 树的节点个数．

![2-3-4-tree-rbt](images/2-3-4-tree-rbt-2.svg)

可以通过对比 2-3-4 树来理解红黑树的插入和删除操作．[^234-vs-rbt]

## 实际工程项目中的使用

由于红黑树是目前主流工业界综合效率最高的内存型平衡树，其在实际的工程项目中有着广泛的使用，这里列举几个实际的使用案例并给出相应的源码链接，以便读者进行对比学习．

### Linux

源码：

-   [`linux/lib/rbtree.c`](https://elixir.bootlin.com/linux/latest/source/lib/rbtree.c)

Linux 中的红黑树所有操作均使用循环迭代进行实现，保证效率的同时又增加了大量的注释来保证代码可读性，十分建议读者阅读学习．Linux 内核中的红黑树使用非常广泛，这里仅列举几个经典案例．

-   [CFS 非实时任务调度](https://www.kernel.org/doc/html/latest/scheduler/sched-design-CFS.html)

    Linux 的稳定内核版本在 2.6.24 之后，使用了新的调度程序 CFS，所有非实时可运行进程都以虚拟运行时间为键值用一棵红黑树进行维护，以完成更公平高效地调度所有任务．CFS 弃用 active/expired 数组和动态计算优先级，不再跟踪任务的睡眠时间和区别是否交互任务，而是在调度中采用基于时间计算键值的红黑树来选取下一个任务，根据所有任务占用 CPU 时间的状态来确定调度任务优先级．

-   [epoll](https://man7.org/linux/man-pages/man7/epoll.7.html)

    epoll 全称 event poll，是 Linux 内核实现 IO 多路复用 (IO multiplexing) 的一个实现，是原先 poll/select 的改进版．Linux 中 epoll 的实现选择使用红黑树来储存文件描述符．

### Nginx

源码：

-   [`nginx/src/core/ngx_rbtree.h`](https://github.com/nginx/nginx/blob/master/src/core/ngx_rbtree.h)
-   [`nginx/src/core/ngx_rbtree.c`](https://github.com/nginx/nginx/blob/master/src/core/ngx_rbtree.c)

nginx 中的用户态定时器是通过红黑树实现的．在 nginx 中，所有 timer 节点都由一棵红黑树进行维护，在 worker 进程的每一次循环中都会调用 `ngx_process_events_and_timers` 函数，在该函数中就会调用处理定时器的函数 `ngx_event_expire_timers`，每次该函数都不断的从红黑树中取出时间值最小的，查看他们是否已经超时，然后执行他们的函数，直到取出的节点的时间没有超时为止．

关于 nginx 中红黑树的源码分析公开资源很多，读者可以自行查找学习．

### C++

源码：

-   GNU libstdc++

    -   [`libstdc++-v3/include/bits/stl_tree.h`](https://github.com/gcc-mirror/gcc/blob/master/libstdc%2B%2B-v3/include/bits/stl_tree.h)
    -   [`libstdc++-v3/src/c++98/tree.cc`](https://github.com/gcc-mirror/gcc/blob/master/libstdc%2B%2B-v3/src/c%2B%2B98/tree.cc)

    另外，`libstdc++` 在 `<ext/rb_tree>` 中提供了 [`__gnu_cxx::rb_tree`](https://github.com/gcc-mirror/gcc/blob/master/libstdc%2B%2B-v3/include/ext/rb_tree)，其继承了 `std::_Rb_tree`，可以认为是供外部使用的类型别名．需要注意的是，该头文件 **不是** C++ 标准的一部分，所以非必要不推荐使用．

    `libstdc++` 的 [`pb_ds`](../lang/pb-ds/tree.md) 中也提供了红黑树．

-   LLVM libcxx
    -   [`libcxx/include/__tree`](https://github.com/llvm/llvm-project/blob/main/libcxx/include/__tree)

-   Microsoft STL
    -   [`stl/inc/xtree`](https://github.com/microsoft/STL/blob/main/stl/inc/xtree)

大多数 STL 中的 `std::set` 和 `std::map` 的内部数据结构就是红黑树（例如上面提到的这些）．不过值得注意的是，C++ 标准并未规定必须以红黑树实现 `std::set` 和 `std::map`，所以不应该在工程项目中直接使用 `std::set` 和 `std::map` 的内部数据结构．

### OpenJDK

源码：

-   [`java.util.TreeMap<K, V>`](https://github.com/openjdk/jdk/blob/master/src/java.base/share/classes/java/util/TreeMap.java)
-   [`java.util.TreeSet<K, V>`](https://github.com/openjdk/jdk/blob/master/src/java.base/share/classes/java/util/TreeSet.java)
-   [`java.util.HashMap<K, V>`](https://github.com/openjdk/jdk/blob/master/src/java.base/share/classes/java/util/HashMap.java)

JDK 中的 `TreeMap` 和 `TreeSet` 都是使用红黑树作为底层数据结构的．同时在 JDK 1.8 之后 `HashMap` 内部哈希表中每个表项的链表长度超过 8 时也会自动转变为红黑树以提升查找效率．

## 参考资料

-   Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022).*Introduction to algorithms*. MIT press.
-   [Red-Black Tree - Wikipedia](https://en.wikipedia.org/wiki/Red%E2%80%93black_tree)
-   [Red-Black Tree Visualization](https://www.cs.usfca.edu/~galles/visualization/RedBlack.html)

[^gilbas1978]: L. J. Guibas and R. Sedgewick, "A dichromatic framework for balanced trees,"*19th Annual Symposium on Foundations of Computer Science (sfcs 1978)*, Ann Arbor, MI, USA, 1978, pp. 8-21, doi:[10.1109/SFCS.1978.3](https://doi.org/10.1109%2FSFCS.1978.3).

[^cite_note-cormen2009-18]: <https://en.wikipedia.org/wiki/Red–black_tree#cite_note-Cormen2009-18>

[^cite_note-mehlhorn2008-17]: <https://en.wikipedia.org/wiki/Red–black_tree#cite_note-Mehlhorn2008-17>

[^cite_note-algs4-16]: <https://en.wikipedia.org/wiki/Red–black_tree#cite_note-Algs4-16>: 432–447

[^234-vs-rbt]: [这篇博文](https://www.cnblogs.com/zhenbianshu/p/8185345.html) 提供了详细的描述．


## ds/sbt.md

Size Balanced Tree (SBT) 是由中国 OI 选手陈启峰在 2007 年提出的一种自平衡二叉搜索树 (Self-Balanced Binary Search Tree, SBBST), 通过检查子树的节点数量进行自身的平衡维护．相比于红黑树，AVL 等主流自平衡二叉搜索树而言，Size Balanced Tree 支持在 $O(\log n)$ 的时间复杂度内查询某个键值在树中的排名 (rank).

## 节点定义

相比与普通二叉搜索树，SBT 的每个节点 $N$ 仅需要多维护一个整数字段 `size`, 用于储存以 $N$ 为根的子树中节点的个数．节点类型 `Node` 的具体定义如下：

| Identifier | Type    | Description     |
| ---------- | ------- | --------------- |
| `left`     | `Node*` | 左子节点引用          |
| `right`    | `Node*` | 右子节点引用          |
| `size`     | `int`   | 以该节点为根的子树中节点的个数 |

## 性质

Size Balanced Tree 中任意节点 $N$ 满足如下几条性质：

```text
size(N.left) >= size(N.right.left)
size(N.left) >= size(N.right.right)
size(N.right) >= size(N.left.left)
size(N.right) >= size(N.left.right)
```

使用自然语言可描述为：任意节点的 `size` 不小于其兄弟节点（Sibling）的所有子节点（Nephew）的 `size`.

## 平衡维护

### 旋转

SBT 主要通过旋转操作改变自身高度从而进行平衡维护．其旋转操作与绝大部分自平衡二叉搜索树类似，唯一区别在于在完成旋转之后需要对旋转过程中左右子节点发生改变的节点更新 `size`. 示例代码如下：

```cpp
void updateSize() {
  USize leftSize = this->left != nullptr ? this->left->size : 0;
  USize rightSize = this->right != nullptr ? this->right->size : 0;
  this->size = leftSize + rightSize + 1;
}

static void rotateLeft(NodePtr& node) {
  assert(node != nullptr);
  // clang-format off
  //     |                       |
  //     N                       S
  //    / \     l-rotate(N)     / \
  //   L   S    ==========>    N   R
  //      / \                 / \
  //     M   R               L   M
  // clang-format on
  NodePtr successor = node->right;
  node->right = successor->left;
  successor->left = node;

  node->updateSize();
  successor->updateSize();

  node = successor;
}

static void rotateRight(NodePtr& node) {
  assert(node != nullptr);
  // clang-format off
  //       |                   |
  //       N                   S
  //      / \   r-rotate(N)   / \
  //     S   R  ==========>  L   N
  //    / \                     / \
  //   L   M                   M   R
  // clang-format on
  NodePtr successor = node->left;
  node->left = successor->right;
  successor->right = node;

  node->updateSize();
  successor->updateSize();

  node = successor;
}
```

### 维护

#### Case 1

`size(N.left) < size(N.right.left)`

```cpp
if (size(node->right->left) > size(node->left)) {
  // clang-format off
  //     |                     |                      |
  //     N                     N                     [M]
  //    / \    r-rotate(R)    / \     l-rotate(N)    / \
  //  <L>  R   ==========>  <L> [M]   ==========>   N   R
  //      /                       \                /
  //    [M]                        R             <L>
  // clang-format on
  rotateRight(node->right);
  rotateLeft(node);
  fixBalance(node->left);
  fixBalance(node->right);
  fixBalance(node);
  return;
}
```

#### Case 2

`size(N.left) < size(N.right.right)`

```cpp
if (size(node->right->right) > size(node->left)) {
  // clang-format off
  //     |                       |
  //     N                       R
  //    / \     l-rotate(N)     / \
  //  <L>  R    ==========>    N  [M]
  //        \                 /
  //        [M]             <L>
  // clang-format on
  rotateLeft(node);
  fixBalance(node->left);
  fixBalance(node);
  return;
}
```

#### Case 3

`size(N.right) < size(N.left.left)`

```cpp
if (size(node->left->left) > size(node->right)) {
  // clang-format off
  //       |                       |
  //       N                       L
  //      / \     r-rotate(N)     / \
  //     L  <R>   ==========>   [M]  N
  //    /                             \
  //  [M]                             <R>
  // clang-format on
  rotateRight(node);
  fixBalance(node->right);
  fixBalance(node);
  return;
}
```

#### Case 4

`size(N.right) < size(N.left.right)`

```cpp
if (size(node->left->right) > size(node->right)) {
  // clang-format off
  //     |                     |                      |
  //     N                     N                     [M]
  //    / \    l-rotate(L)    / \     r-rotate(N)    / \
  //   L  <R>  ==========>  [M] <R>   ==========>   L   N
  //    \                   /                            \
  //    [M]                L                             <R>
  // clang-format on
  rotateLeft(node->left);
  rotateRight(node);
  fixBalance(node->left);
  fixBalance(node->right);
  fixBalance(node);
  return;
}
```

## 操作

### 插入

SBT 的插入操作需要在完成普通二叉搜索树的插入操作的基础上递归地进行节点 `size` 字段的更新及平衡维护．示例代码如下：

```cpp
if (compare(key, node->key)) {
  /* key < node->key */
  if (node->left == nullptr) {
    node->left = Node::from(key, value);
    node->updateSize();
  } else {
    insert(node->left, key, value, replace);
    node->updateSize();
    fixBalance(node);
  }
} else {
  /* key > node->key */
  if (node->right == nullptr) {
    node->right = Node::from(key, value);
    node->updateSize();
  } else {
    insert(node->right, key, value, replace);
    node->updateSize();
    fixBalance(node);
  }
}
```

### 删除

根据 Size Balanced Tree 的提出者陈启峰在其论文中对于删除操作的描述：

> It can result in a destroyed SBT. But with the insertion above, a BST is still kept at the height of $O(\log n)$ where $n$ is the total number of insertions, not the current size.

删除操作虽然有可能使得 SBT 的性质被打破，但并不会使树的高度增高，因此不会影响后续操作的效率．但在实际情况下，如果在一次批量插入操作后只进行大量的删除和查询操作，依然有可能由于树的失衡影响整体效率，因此本文在实现 SBT 的删除操作时依然选择加入平衡维护．参考代码如下：

```cpp
bool remove(NodePtr& node, K key, NodeConsumer action) {
  assert(node != nullptr);

  if (key != node->key) {
    if (compare(key, node->key)) {
      /* key < node->key */
      NodePtr& left = node->left;
      if (left != nullptr && remove(left, key, action)) {
        node->updateSize();
        fixBalance(node);
        return true;
      } else {
        return false;
      }
    } else {
      /* key > node->key */
      NodePtr& right = node->right;
      if (right != nullptr && remove(right, key, action)) {
        node->updateSize();
        fixBalance(node);
        return true;
      } else {
        return false;
      }
    }
  }

  assert(key == node->key);
  action(node);

  if (node->isLeaf()) {
    // Case 1: no child
    node = nullptr;
  } else if (node->right == nullptr) {
    // Case 2: left child only
    // clang-format off
    //     P
    //     |  remove(N)  P
    //     N  ========>  |
    //    /              L
    //   L
    // clang-format on
    node = node->left;
  } else if (node->left == nullptr) {
    // Case 3: right child only
    // clang-format off
    //   P
    //   |    remove(N)  P
    //   N    ========>  |
    //    \              R
    //     R
    // clang-format on
    node = node->right;
  } else if (node->right->left == nullptr) {
    // Case 4: both left and right child, right child has no left child
    // clang-format off
    //    |                 |
    //    N    remove(N)    R
    //   / \   ========>   /
    //  L   R             L
    // clang-format on
    NodePtr right = node->right;
    swapNode(node, right);
    right->right = node->right;
    node = right;
    node->updateSize();
    fixBalance(node);
  } else {
    // Case 5: both left and right child, right child is not a leaf
    // clang-format off
    //   Step 1. find the node N with the smallest key
    //           and its parent P on the right subtree
    //   Step 2. swap S and N
    //   Step 3. remove node N like Case 1 or Case 3
    //   Step 4. update size for all nodes on the path
    //           from S to P
    //     |                  |
    //     N                  S                 |
    //    / \                / \                S
    //   L  ..  swap(N, S)  L  ..  remove(N)   / \
    //       |  =========>      |  ========>  L  ..
    //       P                  P                 |
    //      / \                / \                P
    //     S  ..              N  ..              / \
    //      \                  \                R  ..
    //       R                  R
    //
    // clang-format on

    std::stack<NodePtr> path;

    // Step 1
    NodePtr successor = node->right;
    NodePtr parent = node;
    path.push(node);

    while (successor->left != nullptr) {
      path.push(successor);
      parent = successor;
      successor = parent->left;
    }

    // Step 2
    swapNode(node, successor);

    // Step 3
    parent->left = node->right;
    // Restore node
    node = successor;

    // Step 4
    while (!path.empty()) {
      path.top()->updateSize();
      path.pop();
    }
  }

  return true;
}
```

值得注意的是，在上述代码的 Case 5 中使用后继节点 $S$（也可以选择前驱节点）替换待删除节点 $N$ 并删除替换后的 $N$ 以后，需要更新替换前 $S$ 节点的父节点 $P$ 到替换后的 $S$ 节点这条路径（如代码中注释所示）上的所有节点的 `size` 字段．本文的实现选择使用栈依次记录路径上的节点，最后再按遍历的相反顺序出栈进行更新．

### 查询排名

由于 SBT 节点中储存了子树节点个数的信息，因此可以在 $O(\log n)$ 的时间复杂度下查询某个 `key` 的排名（或者大于/小于某个 `key` 的节点个数）．示例代码如下：

```cpp
USize countLess(ConstNodePtr node, K key, bool countEqual = false) const {
  if (node == nullptr) {
    return 0;
  } else if (key < node->key) {
    return countLess(node->left, key, countEqual);
  } else if (key > node->key) {
    return size(node->left) + 1 + countLess(node->right, key, countEqual);
  } else {
    return size(node->left) + (countEqual ? 1 : 0);
  }
}

USize countGreater(ConstNodePtr node, K key, bool countEqual = false) const {
  if (node == nullptr) {
    return 0;
  } else if (key < node->key) {
    return size(node->right) + 1 + countGreater(node->left, key, countEqual);
  } else if (key > node->key) {
    return countGreater(node->right, key, countEqual);
  } else {
    return size(node->right) + (countEqual ? 1 : 0);
  }
}
```

## 参考代码

下面的代码是用 SBT 实现的 `Map`，即有序不可重映射：

??? note "完整代码"
    ```cpp
    --8<-- "docs/ds/code/size-balanced-tree/SizeBalancedTreeMap.hpp"
    ```


## ds/seg-beats.md

本文讲解吉老师在 [2016 年国家集训队论文](https://github.com/OI-wiki/libs/blob/master/%E9%9B%86%E8%AE%AD%E9%98%9F%E5%8E%86%E5%B9%B4%E8%AE%BA%E6%96%87/%E5%9B%BD%E5%AE%B6%E9%9B%86%E8%AE%AD%E9%98%9F2016%E8%AE%BA%E6%96%87%E9%9B%86.pdf) 中提到的线段树处理历史区间最值的问题．

## 区间最值

笼统地说，区间最值操作指，将区间 $[l,r]$ 的数全部对 $x$ 取 $\max$ 或 $\min$，即 $a_i=\max(a_i,x)$ 或者 $a_i=\min(a_i,x)$．

???+ note "[HDU5306 Gorgeous Sequence](https://acm.hdu.edu.cn/showproblem.php?pid=5306)"
    维护一个序列 $a$，执行以下操作：
    
    1.  `0 l r t` $\forall l\le i\le r,~ a_i=\min(a_i,t)$．
    2.  `1 l r` 输出 $\max\limits_{i=l}^r a_i$．
    3.  `2 l r` 输出 $\sum\limits_{i=l}^r a_i$．
    
    多组测试数据，保证 $T\le 100,~\sum n,\sum m\le 10^6$．

区间取 $\min$，意味着只对那些大于 $t$ 的数有更改．因此这个操作的对象不再是整个区间，而是「这个区间中大于 $t$ 的数」．于是我们可以有这样的思路：每个结点维护该区间的最大值 $Max$、次大值 $Se$、区间和 $Sum$ 以及最大值的个数 $Cnt$．接下来我们考虑区间对 $t$ 取 $\min$ 的操作．

1.  如果 $Max\le t$，显然这个 $t$ 是没有意义的，直接返回；
2.  如果 $Se<t < Max$，那么这个 $t$ 就能更新当前区间中的最大值．于是我们让区间和加上 $Cnt(t-Max)$，然后更新 $Max$ 为 $t$，并打一个标记．
3.  如果 $t\le Se$，那么这时你发现你不知道有多少个数涉及到更新的问题．于是我们的策略就是，暴力递归向下操作．然后上传信息．

这个算法的复杂度如何？使用势能分析法可以得到复杂度是 $O(m\log n)$ 的．具体分析过程见论文．

```cpp
--8<-- "docs/ds/code/seg-beats/seg-beats_1.cpp"
```

???+ note "[BZOJ4695 最假女选手](https://loj.ac/p/6565)"
    维护一个序列 $a$，执行以下操作：
    
    1.  `1 l r x` $\forall l\le i\le r,~ a_i=a_i+x$．
    2.  `2 l r x` $\forall l\le i\le r,~ a_i=\max(a_i,x)$．
    3.  `3 l r x` $\forall l\le i\le r,~ a_i=\min(a_i,x)$．
    4.  `4 l r` 输出 $\sum\limits_{i=l}^r a_i$．
    5.  `5 l r` 输出 $\max\limits_{i=l}^r a_i$．
    6.  `6 l r` 输出 $\min\limits_{i=l}^r a_i$．
    
    $n,m\le 5\times 10^5,~|a_i|\le 10^8$．所有类型 $1$ 操作有 $|x|\le 10^3$，其余操作满足 $|x|\le10^8$．

同样的方法，我们维护最大、次大、最大个数、最小、次小、最小个数、区间和．除了这些信息，我们还需要维护区间 $\max$、区间 $\min$、区间加的标记．相比上一道题，这就涉及到标记下传的顺序问题了．我们采用这样的策略：

1.  我们认为区间加的标记是最优先的，其余两种标记地位平等．
2.  对一个结点加上一个 $v$ 标记，除了用 $v$ 更新卫星信息和当前结点的区间加标记外，我们用这个 v 更新区间 $\max$ 和区间 $\min$ 的标记．
3.  对一个结点取 $v$ 的 $\min$（这里忽略暴搜的过程，假定标记满足添加的条件），除了更新卫星信息，我们要与区间 $\max$ 的标记做比较．如果 $v$ 小于区间 $\max$ 的标记，则所有的数最后都会变成 v，那么把区间 $\max$ 的标记也变成 $v$．否则不管．
4.  区间取 v 的 $\max$ 同理．

在维护信息的时候，当只有一个数或两个数的时候可能发生数集重合，比如一个数既是最大值又是次小值，需要特判．

```cpp
--8<-- "docs/ds/code/seg-beats/seg-beats_2.cpp"
```

吉老师证出来这个算法的复杂度是 $O(m\log^2 n)$ 的．

???+ note "Mzl loves segment tree"
    两个序列 $A,B$，一开始 $B$ 中的数都是 $0$．维护的操作是：
    
    1.  对 $A$ 做区间取 $\min$
    2.  对 $A$ 做区间取 $\max$
    3.  对 $A$ 做区间加
    4.  询问 $B$ 的区间和
    
    每次操作完后，如果 $A_i$ 的值发生变化，就给 $B_i$ 加 $1$．$n,m\le 3\times 10^5$．

先考虑最容易的区间加操作．只要 $x\neq 0$ 那么整个区间的数都变化，所以给 B 作一次区间加即可．

对于区间取最值的操作，你发现你打标记与下传标记是与 $B$ 数组一一对应的．本质上你将序列的数分成三类：最大值、最小值、非最值．并分别维护（只不过你没有建出具体的最值集合而已，但这并不妨碍维护的操作）．因此在打标记的时候顺便给 $B$ 更新信息即可（注意不是给 $B$ 打标记！是更新信息！）．查询的时候，你在 $A$ 上查询，下传标记的时候顺便给 $B$ 更新信息．找到需要的结点后，返回 $B$ 的信息即可．这种操作本质上就是把最值的信息拿给 $B$ 去维护了．另外仍要处理数集的重复问题．

???+ note "[CTSN loves segment tree](https://www.luogu.com.cn/problem/U180387)"
    维护两个序列 $a,b$，执行以下操作：
    
    1.  `1 l r x` $\forall l\le i\le r,~ a_i=\min(a_i,x)$．
    2.  `2 l r x` $\forall l\le i\le r,~ b_i=\min(b_i,x)$．
    3.  `3 l r x` $\forall l\le i\le r,~ a_i=a_i+x$．
    4.  `4 l r x` $\forall l\le i\le r,~ b_i=b_i+x$．
    5.  `5 l r` 输出 $\max\limits_{i=l}^r (a_i+b_i)$．
    
    $n,m\le 3\times 10^5,~|a_i|,|b_i|,|x|\le 10^9$．

我们把区间 $[l,r]$ 中的备选答案 $A_i+B_i$ 分成四类：$A_i,B_i$ 均不是序列 $A,B$ 区间最大值、$A_i$ 是序列 $A$ 区间最大值但是 $B_i$ 不是序列 $B$ 区间最大值、$A_i$ 不是序列 $A$ 区间最大值但是 $B_i$ 是序列 $B$ 区间最大值、$A_i,B_i$ 均是序列 $A,B$ 区间最大值．我们不妨分别设为 $C_{0,0},C_{1,0},C_{0,1},C_{1,1}$．此外我们正常维护序列 $A,B$ 的区间最大值和次大值．下传区间加法标记和 $\min$ 标记时对 $A,B$ 最大值和次大值的处理与上述两个例题一致．对 $A$ 的 $\min$ 标记会影响到 $C_{1,1}$ 和 $C_{1,0}$，对 $B$ 的标记会影响到 $C_{1,1}$ 和 $C_{0,1}$．对 $A,B$ 的加法则会对 $C_{0,0},C_{1,0},C_{0,1},C_{1,1}$ 均产生影响．只需要注意 $C_{0,0},C_{1,0},C_{0,1}$ 不存在的边界情况即可（例如区间 $[i,i]$ 只有 $A,B$ 的最大值与 $C_{1,1}$ 存在）．

接下来需要考虑在 pushup 时如何维护 $C_{0,0},C_{1,0},C_{0,1},C_{1,1}$．我们可以考虑一下完成 $A,B$ 最大值的更新之后，讨论左右儿子的 $A,B$ 最大值是否与当前节点 $A,B$ 最大值相等．我们以左儿子为例进行讲解，右儿子类似处理：

-   当左儿子的 $A,B$ 最大值与当前节点的 $A,B$ 最大值均相等时，左儿子的 $C_{0,0},C_{1,0},C_{0,1},C_{1,1}$ 会分别对当前节点的 $C_{0,0},C_{1,0},C_{0,1},C_{1,1}$ 产生贡献．
-   当左儿子的 $A$ 最大值与当前节点 $A$ 最大值相等，但是 $B$ 最大值不相等时，左儿子的 $C_{1,0},C_{1,1}$ 会对该节点的 $C_{1,0}$ 产生贡献，$C_{0,0},C_{0,1}$ 会对该节点的 $C_{0,0}$ 产生贡献．
-   当左儿子的 $A$ 最大值与当前节点 $A$ 最大值不相等，但是 $B$ 最大值相等时，左儿子的 $C_{0,1},C_{1,1}$ 会对该节点的 $C_{0,1}$ 产生贡献，$C_{0,0},C_{1,0}$ 会对该节点的 $C_{0,0}$ 产生贡献．
-   当左儿子的 $A,B$ 最大值与当前节点的 $A,B$ 最大值均不相等时，左儿子的 $C_{0,0},C_{1,0},C_{0,1},C_{1,1}$ 仅会对该节点的 $C_{0,0}$ 产生贡献．

区间查询结果的 $\max(C_{0,0},C_{1,0},C_{0,1},C_{1,1})$ 即为所求．

由于需要同时维护区间 $\min$ 和区间加法，所以复杂度仍是 $O(m\log^2 n)$．

```cpp
--8<-- "docs/ds/code/seg-beats/seg-beats_4.cpp"
```

### 小结

在第本章节中我们给出了四道例题，分别讲解了基本区间最值操作的维护、多个标记的优先级处理、数集分类的思想以及多个分类的维护．本质上处理区间最值的基本思想就是数集信息的分类维护与高效合并．在下一章节中，我们将探讨历史区间最值的相关问题．

## 历史最值问题

### 历史最值不等于可持久化

注意，本章所讲到的历史最值问题不同于所谓的可持久化数据结构．这类特殊的问题我们将其称为历史最值问题．历史最值的问题可以分为三类．

#### 历史最大值

简单地说，一个位置的历史最大值就是当前位置下曾经出现过的数的最大值．形式化地定义，我们定义一个辅助数组 $B$，一开始与 $A$ 完全相同．在 $A$ 的每次操作后，我们对整个数组取 $\max$：

$$
\forall i\in[1,n],\ B_i=\max(B_i,A_i)
$$

这时，我们将 $B_i$ 称作这个位置的历史最大值，

#### 历史最小值

定义与历史最大值类似，在 $A$ 的每次操作后，我们对整个数组取 $\min$．这时，我们将 $B_i$ 称作这个位置的历史最小值，

#### 历史版本和

辅助数组 $B$ 一开始全部是 $0$．在每一次操作后，我们把整个 $A$ 数组累加到 $B$ 数组上

$$
\forall i\in[1,n], \ B_i=B_i+A_i
$$

我们称 $B_i$ 为 $i$ 这个位置上的历史版本和．

接下来，我们将历史最值问题分成四类讨论．

### 可以用标记处理的问题

???+ note "[CPU 监控](https://www.luogu.com.cn/problem/P4314)"
    序列 $A,B$ 一开始相同：
    
    1.  对 $A$ 做区间覆盖 $x$
    2.  对 $A$ 做区间加 $x$
    3.  询问 $A$ 的区间 $\max$
    4.  询问 $B$ 的区间 $\max$
    
    每次操作后，我们都进行一次更新，$\forall i\in [1,n],\ B_i=\max(B_i,A_i)$．$n,m\le 10^5$．

我们先不考虑操作 1．那么只有区间加的操作，我们维护标记 $Add$ 表示当前区间增加的值，这个标记可以解决区间 $\max$ 的问题．接下来考虑历史区间 $\max$．我们定义标记 $Pre$，该标记的含义是：在该标记的生存周期内，$Add$ 标记的历史最大值．

这个定义可能比较模糊．因此我们先解释一下标记的生存周期．一个标记会经历这样的过程：

1.  在结点 $u$ 被建立．
2.  在结点 $u$ 接受若干个新的标记的同时，与新的标记合并（指同类标记）
3.  结点 $u$ 的标记下传给 $u$ 的儿子，$u$ 的标记清空

我们认为在这个过程中，从 1 开始到 3 之前，都是结点 $u$ 的标记的生存周期．两个标记合并后，成为同一个标记，那么他们的生存周期也会合并（即取建立时间较早的那个做为生存周期的开始）．一个与之等价的说法是，从上次把这个结点的标记下传的时刻到当前时刻这一时间段．

为什么要定义生存周期？利用这个概念，我们可以证明：在一个结点标记的生存周期内，其子结点均不会发生任何变化，并保留在这个生存周期之前的状态．道理很简单，因为在这个期间你是没有下传标记的．

于是，你就可以保证，在当前标记生存周期内的历史 $Add$ 的最大值是可以更新到子结点的标记和信息上的．因为子结点的标记和信息在这个时间段内都没有变过．于是我们把 $u$ 的标记下传给它的儿子 $s$，不难发现

$$
Pre_s=\max(Pre_s,Pre_u+Add_s),Add_s=Add_u+Add_s
$$

那么信息的更新也是类似的，拿对应的标记更新即可．

接下来，我们考虑操作 1．

区间覆盖操作，会把所有的数变成一个数．在这之后，无论是区间加减还是覆盖，整个区间的数仍是同一个（除非你结束当前标记的生存周期，下传标记）．因此我们可以把第一次区间覆盖后的所有标记都看成区间覆盖标记．也就是说一个标记的生存周期被大致分成两个阶段：

1.  若干个加减操作标记的合并，没有接收过覆盖标记．
2.  覆盖操作的标记，没有所谓的加减标记（加减标记转化为覆盖标记）

于是我们把这个结点的 Pre 标记拆成 $(P_1,P_2)$．$P_1$ 表示第一阶段的最大加减标记；$P_2$ 表示第二阶段的最大覆盖标记．利用相似的方法，我们可以对这个做标记下传和信息更新．时间复杂度是 $O(m\log n)$ 的（这个问题并没有区间对 $x$ 取最值的操作哦～）

```cpp
--8<-- "docs/ds/code/seg-beats/seg-beats_3.cpp"
```


## ds/seg-in-bit.md

author: Ir1d, sshwy, Enter-tainer, H-J-Granger, ouuan, GavinZhengOI, hsfzLZH1, xyf007

[静态区间 k 小值（POJ 2104 K-th Number）](http://poj.org/problem?id=2104) 的问题可以用 [权值线段树](./persistent-seg.md) 在 $O(n\log n)$ 的时间复杂度内解决．

如果区间变成动态的呢？即，如果还要求支持一种操作：单点修改某一位上的值，又该怎么办呢？

??? note "例题 [二逼平衡树（树套树）](https://loj.ac/problem/106)"
    维护一个有序数列，其中需要提供以下操作：
    
    -   查询 $x$ 在区间内的排名；
    -   查询区间内排名为 $k$ 的值；
    -   修改某一位置上的数值；
    -   查询 $x$ 在区间内的前驱（前驱定义为小于 $x$，且最大的数）；
    -   查询 $x$ 在区间内的后继（后继定义为大于 $x$，且最小的数）．

??? note "例题 [洛谷 P2617 Dynamic Rankings](https://www.luogu.com.cn/problem/P2617)"
    给定一个含有 $n$ 个数的序列 $a_1,a_2 \dots a_n$，需要支持两种操作：
    
    -   `Q l r k` 表示查询下标在区间 $[l,r]$ 中的第 $k$ 小的数
    -   `C x y` 表示将 $a_x$ 改为 $y$

如果用 [线段树套平衡树](./balanced-in-seg.md) 中所论述的，用线段树套平衡树，即对于线段树的每一个节点，对于其所表示的区间维护一个平衡树，然后用二分来查找 $k$ 小值．由于每次查询操作都要覆盖多个区间，即有多个节点，但是平衡树并不能多个值一起查找，所以时间复杂度是 $O(n\log^3 n)$，并不是最优的．

优化的思路是把二分答案的操作和查询小于一个值的数的数量两种操作结合起来，使用 **线段树套动态开点权值线段树**，由于所有线段树的结构是相同的，可以在多棵树上同时进行线段树上二分．

在修改操作进行时，先在线段树上从上往下跳到被修改的点，删除所经过的点所指向的动态开点权值线段树上的原来的值，然后插入新的值，要经过 $O(\log n)$ 个线段树上的节点，在动态开点权值线段树上一次修改操作是 $O(\log n)$ 的，所以修改操作的时间复杂度为 $O(\log^2 n)$．

在查询答案时，先取出该区间覆盖在线段树上的所有点，然后用类似于静态区间 $k$ 小值的方法，将这些点一起向左儿子或向右儿子跳．如果所有这些点左儿子存储的值大于等于 $k$，则往左跳，否则往右跳．由于最多只能覆盖 $O(\log n)$ 个节点，所以最多一次只有这么多个节点向下跳，时间复杂度为 $O(\log^2 n)$．

由于线段树的常数较大，在实现中往往使用常数更小且更方便处理前缀和的 **树状数组** 实现．另外空间复杂度是 $O(n\log^2 n)$ 的，使用时 **注意空间限制**．

给出一种代码实现：

??? note "实现"
    ```cpp
    #include <algorithm>
    #include <cstdio>
    #include <cstring>
    #include <map>
    #include <set>
    #define LC o << 1
    #define RC o << 1 | 1
    using namespace std;
    constexpr int MAXN = 1000010;
    int n, m, a[MAXN], u[MAXN], x[MAXN], l[MAXN], r[MAXN], k[MAXN], cur, cur1, cur2,
        q1[MAXN], q2[MAXN], v[MAXN];
    char op[MAXN];
    set<int> ST;
    map<int, int> mp;
    
    struct segment_tree  // 封装的动态开点权值线段树
    {
      int cur, rt[MAXN * 4], sum[MAXN * 60], lc[MAXN * 60], rc[MAXN * 60];
    
      void build(int& o) { o = ++cur; }
    
      void print(int o, int l, int r) {
        if (!o) return;
        if (l == r && sum[o]) printf("%d ", l);
        int mid = (l + r) >> 1;
        print(lc[o], l, mid);
        print(rc[o], mid + 1, r);
      }
    
      void update(int& o, int l, int r, int x, int v) {
        if (!o) o = ++cur;
        sum[o] += v;
        if (l == r) return;
        int mid = (l + r) >> 1;
        if (x <= mid)
          update(lc[o], l, mid, x, v);
        else
          update(rc[o], mid + 1, r, x, v);
      }
    } st;
    
    // 树状数组实现
    namepace fenwick_impl {
      int lowbit(int o) { return (o & (-o)); }
    
      void upd(int o, int x, int v) {
        for (; o <= n; o += lowbit(o)) st.update(st.rt[o], 1, n, x, v);
      }
    
      void gtv(int o, int* A, int& p) {
        p = 0;
        for (; o; o -= lowbit(o)) A[++p] = st.rt[o];
      }
    
      int qry(int l, int r, int k) {
        if (l == r) return l;
        int mid = (l + r) >> 1, siz = 0;
        for (int i = 1; i <= cur1; i++) siz += st.sum[st.lc[q1[i]]];
        for (int i = 1; i <= cur2; i++) siz -= st.sum[st.lc[q2[i]]];
        // printf("j %d %d %d %d\n",cur1,cur2,siz,k);
        if (siz >= k) {
          for (int i = 1; i <= cur1; i++) q1[i] = st.lc[q1[i]];
          for (int i = 1; i <= cur2; i++) q2[i] = st.lc[q2[i]];
          return qry(l, mid, k);
        } else {
          for (int i = 1; i <= cur1; i++) q1[i] = st.rc[q1[i]];
          for (int i = 1; i <= cur2; i++) q2[i] = st.rc[q2[i]];
          return qry(mid + 1, r, k - siz);
        }
      }
    }
    using namespace fenwick_impl;
    
    // 线段树实现
    namespace segtree_impl {
    void build(int o, int l, int r) {
      st.build(st.rt[o]);
      if (l == r) return;
      int mid = (l + r) >> 1;
      build(LC, l, mid);
      build(RC, mid + 1, r);
    }
    
    void print(int o, int l, int r) {
      printf("%d %d:", l, r);
      st.print(st.rt[o], 1, n);
      printf("\n");
      if (l == r) return;
      int mid = (l + r) >> 1;
      print(LC, l, mid);
      print(RC, mid + 1, r);
    }
    
    void update(int o, int l, int r, int q, int x, int v) {
      st.update(st.rt[o], 1, n, x, v);
      if (l == r) return;
      int mid = (l + r) >> 1;
      if (q <= mid)
        update(LC, l, mid, q, x, v);
      else
        update(RC, mid + 1, r, q, x, v);
    }
    
    void getval(int o, int l, int r, int ql, int qr) {
      if (l > qr || r < ql) return;
      if (ql <= l && r <= qr) {
        q[++cur] = st.rt[o];
        return;
      }
      int mid = (l + r) >> 1;
      getval(LC, l, mid, ql, qr);
      getval(RC, mid + 1, r, ql, qr);
    }
    
    int query(int l, int r, int k) {
      if (l == r) return l;
      int mid = (l + r) >> 1, siz = 0;
      for (int i = 1; i <= cur; i++) siz += st.sum[st.lc[q[i]]];
      if (siz >= k) {
        for (int i = 1; i <= cur; i++) q[i] = st.lc[q[i]];
        return query(l, mid, k);
      } else {
        for (int i = 1; i <= cur; i++) q[i] = st.rc[q[i]];
        return query(mid + 1, r, k - siz);
      }
    }
    }  // namespace segtree_impl
    
    int main() {
      scanf("%d%d", &n, &m);
      for (int i = 1; i <= n; i++) scanf("%d", a + i), ST.insert(a[i]);
      for (int i = 1; i <= m; i++) {
        scanf(" %c", op + i);
        if (op[i] == 'C')
          scanf("%d%d", u + i, x + i), ST.insert(x[i]);
        else
          scanf("%d%d%d", l + i, r + i, k + i);
      }
      for (set<int>::iterator it = ST.begin(); it != ST.end(); it++)
        mp[*it] = ++cur, v[cur] = *it;
      for (int i = 1; i <= n; i++) a[i] = mp[a[i]];
      for (int i = 1; i <= m; i++)
        if (op[i] == 'C') x[i] = mp[x[i]];
      n += m;
      // build(1,1,n);
      for (int i = 1; i <= n; i++) upd(i, a[i], 1);
      // print(1,1,n);
      for (int i = 1; i <= m; i++) {
        if (op[i] == 'C') {
          upd(u[i], a[u[i]], -1);
          upd(u[i], x[i], 1);
          a[u[i]] = x[i];
        } else {
          gtv(r[i], q1, cur1);
          gtv(l[i] - 1, q2, cur2);
          printf("%d\n", v[qry(1, n, k[i])]);
        }
      }
      return 0;
    }
    ```


## ds/seg-in-seg.md

author: Chrogeek, HeRaNO, Dev-XYS, Dev-jqe

## 常见用途

在算法竞赛中，我们有时需要维护多维度信息．在这种时候，我们经常需要树套树来记录信息．

## 实现原理

我们考虑用树套树如何实现在二维平面上进行单点修改，区域查询．我们考虑外层的线段树，最底层的 $1$ 到 $n$ 个节点的子树，分别代表第 $1$ 到第 $n$ 行的线段树．那么这些底层的节点对应的父节点，就代表其两个子节点的子树所在的一片区域．

## 性质

### 空间复杂度

通常情况下，我们不可能对于外层线段树的每一个结点都建立一颗子线段树，空间需求过大．树套树一般采取动态开点的策略．单次修改，我们会涉及到外层线段树的 $\log{n}$ 个节点，且对于每个节点的子树涉及 $\log{n}$ 个节点，所以单次修改产生的空间最多为 $\log^2{n}$．

### 时间复杂度

对于询问操作，我们考虑我们在外层线段树上进行 $\log{n}$ 次操作，每次操作会在一个内层线段树上进行 $\log{n}$ 次操作，所以时间复杂度为 $\log^2{n}$．
修改操作，与询问操作复杂度相同，也为 $\log^2{n}$．

## 经典例题

[陌上花开](https://www.luogu.com.cn/problem/P3810) 将第一维排序处理，然后用树套树维护第二维和第三维．

## 示例代码

第二维查询

```cpp
int tree_query(int k, int l, int r, int x) {
  if (k == 0) return 0;
  if (1 <= l && r <= sec[x].y) return vec_query(ou_root[k], 1, p, 1, sec[x].z);
  int mid = l + r >> 1, res = 0;
  if (1 <= mid) res += tree_query(ou_ch[k][0], l, mid, x);
  if (sec[x].y > mid) res += tree_query(ou_ch[k][1], mid + 1, r, x);
  return res;
}
```

第二维修改

```cpp
void tree_insert(int &k, int l, int r, int x) {
  if (k == 0) k = ++ou_tot;
  vec_insert(ou_root[k], 1, p, sec[x].z);
  if (l == r) return;
  int mid = l + r >> 1;
  if (sec[x].y <= mid)
    tree_insert(ou_ch[k][0], l, mid, x);
  else
    tree_insert(ou_ch[k][1], mid + 1, r, x);
}
```

第三维查询

```cpp
int vec_query(int k, int l, int r, int x, int y) {
  if (k == 0) return 0;
  if (x <= l && r <= y) return data[k];
  int mid = l + r >> 1, res = 0;
  if (x <= mid) res += vec_query(ch[k][0], l, mid, x, y);
  if (y > mid) res += vec_query(ch[k][1], mid + 1, r, x, y);
  return res;
}
```

第三维修改

```cpp
void vec_insert(int &k, int l, int r, int loc) {
  if (k == 0) k = ++tot;
  data[k]++;
  if (l == r) return;
  int mid = l + r >> 1;
  if (loc <= mid) vec_insert(ch[k][0], l, mid, loc);
  if (loc > mid) vec_insert(ch[k][1], mid + 1, r, loc);
}
```

## 相关算法

面对多维度信息的题目时，如果题目没有要求强制在线，我们还可以考虑 **CDQ 分治**，或者 **整体二分** 等分治算法，来避免使用高级数据结构，减少代码实现难度．


## ds/seg-merge-split.md

author: ChungZH, billchenchina, Chrogeek, Early0v0, ethan-enhe, HeRaNO, hsfzLZH1, iamtwz, Ir1d, konnyakuxzy, luoguojie, Marcythm, orzAtalod, StudyingFather, wy-luke, Xeonacid, CCXXXI, chenryang, chenzheAya, CJSoft, cjsoft, countercurrent-time, DawnMagnet, Enter-tainer, GavinZhengOI, Haohu Shen, Henry-ZHR, hjsjhn, hly1204, jaxvanyang, Jebearssica, kenlig, ksyx, megakite, Menci, moon-dim, NachtgeistW, onelittlechildawa, ouuan, shadowice1984, shawlleyw, shuzhouliu, SukkaW, Tiphereth-A, x2e6, Ycrpro, yifan0305, zeningc

线段树的合并与分裂是线段树的常用技巧，常见于权值线段树维护可重集的场景．

例如，树上某些结点处有若干操作，如果需要自下而上地将子节点信息传递给亲节点，而单个结点处的信息又方便用线段树维护时，就可以应用线段树合并的技巧控制整体的复杂度．

## 线段树合并

### 过程

顾名思义，线段树合并是指建立一棵新的线段树，这棵线段树的每个节点都是两棵原线段树对应节点合并后的结果．它常常被用于维护树上或是图上的信息．

显然，我们不可能真的每次建满一颗新的线段树，因此我们需要使用上文的动态开点线段树．

线段树合并的过程本质上相当暴力：

假设两颗线段树为 A 和 B，我们从 1 号节点开始递归合并．

递归到某个节点时，如果 A 树或者 B 树上的对应节点为空，直接返回另一个树上对应节点，这里运用了动态开点线段树的特性．

如果递归到叶子节点，我们合并两棵树上的对应节点．

最后，根据子节点更新当前节点并且返回．

???+ note "线段树合并的复杂度"
    显然，对于两颗满的线段树，单次合并操作的复杂度是 $O(n)$ 的．但实际情况下使用的常常是权值线段树，所有需要合并的线段树的总点数和 $n$ 的规模相差并不大．并且合并时一般不会重复地合并某个线段树，所以我们最终增加的点数大致是 $n\log n$ 级别的．这样，合并所有线段树总的复杂度就是 $O(n\log n)$ 级别的．当然，在一些情况下，可并堆可能是更好的选择．

### 实现

```cpp
int merge(int a, int b, int l, int r) {
  if (!a) return b;
  if (!b) return a;
  if (l == r) {
    // do something...
    return a;
  }
  int mid = (l + r) >> 1;
  tr[a].l = merge(tr[a].l, tr[b].l, l, mid);
  tr[a].r = merge(tr[a].r, tr[b].r, mid + 1, r);
  pushup(a);
  return a;
}
```

### 例题

???+ note "[luogu P4556 \[Vani 有约会\] 雨天的尾巴/【模板】线段树合并](https://www.luogu.com.cn/problem/P4556)"
    ??? note "解题思路"
        线段树合并模板题，用差分把树上修改转化为单点修改，然后向上 dfs 线段树合并统计答案即可．
    
    ??? note "参考代码"
        ```cpp
        --8<-- "docs/ds/code/seg/seg_6.cpp"
        ```

## 线段树分裂

### 过程

线段树分裂实质上是线段树合并的逆过程．线段树分裂只适用于有序的序列，无序的序列是没有意义的，常用在动态开点的权值线段树．

注意当分裂和合并都存在时，我们在合并的时候必须回收节点，以避免分裂时会可能出现节点重复占用的问题．

从一颗区间为 $[1,N]$ 的线段树中分裂出 $[l,r]$，建一颗新的树：

从 1 号结点开始递归分裂，当节点不存在或者代表的区间 $[s,t]$ 与 $[l,r]$ 没有交集时直接回溯．

当 $[s,t]$ 与 $[l,r]$ 有交集时需要开一个新结点．

当 $[s,t]$ 包含于 $[l,r]$ 时，需要将当前结点直接接到新的树下面，并把旧边断开．

???+ note "线段树分裂的复杂度"
    可以发现被断开的边最多只会有 $\log n$ 条，所以最终每次分裂的时间复杂度就是 $O(\log⁡ n)$，相当于区间查询的复杂度．

### 实现

```cpp
void split(int &p, int &q, int s, int t, int l, int r) {
  if (t < l || r < s) return;
  if (!p) return;
  if (l <= s && t <= r) {
    q = p;
    p = 0;
    return;
  }
  if (!q) q = New();
  int m = s + t >> 1;
  if (l <= m) split(ls[p], ls[q], s, m, l, r);
  if (m < r) split(rs[p], rs[q], m + 1, t, l, r);
  push_up(p);
  push_up(q);
}
```

### 例题

???+ note "[P5494【模板】线段树分裂](https://www.luogu.com.cn/problem/P5494)"
    ??? note "解题思路"
        线段树分裂模板题，将 $[x,y]$ 分裂出来．
        
        -   将 $t$ 树合并入 $p$ 树：单次合并即可．
        
        -   $p$ 树中插入 $x$ 个 $q$：单点修改．
        
        -   查询 $[x,y]$ 中数的个数：区间求和．
        
        -   查询第 $k$ 小．
    
    ??? note "参考代码"
        ```cpp
        --8<-- "docs/ds/code/seg/seg_7.cpp"
        ```

## 习题

-   [Luogu P4556 \[Vani 有约会\] 雨天的尾巴/【模板】线段树合并](https://www.luogu.com.cn/problem/P4556)
-   [Luogu P5494【模板】线段树分裂](https://www.luogu.com.cn/problem/P5494)
-   [Luogu P1600 天天爱跑步](https://www.luogu.com.cn/problem/P1600)
-   [Luogu P4577 \[FJOI2018\] 领导集团问题](https://www.luogu.com.cn/problem/P4577)
-   [Luogu P2824 \[HEOI2016/TJOI2016\] 排序](https://www.luogu.com.cn/problem/P2824)


## ds/seg.md

author: Marcythm, Ir1d, Ycrpro, Xeonacid, konnyakuxzy, CJSoft, HeRaNO, ethan-enhe, ChungZH, Chrogeek, hsfzLZH1, billchenchina, orzAtalod, luoguojie, Early0v0, wy-luke

## 引入

线段树是算法竞赛中常用的用来维护 **区间信息** 的数据结构．

线段树可以在 $O(\log N)$ 的时间复杂度内实现单点修改、区间修改、区间查询（区间求和，求区间最大值，求区间最小值）等操作．

## 线段树的基本结构与建树

### 过程

线段树将每个长度不为 $1$ 的区间划分成左右两个区间递归求解，把整个线段划分为一个树形结构，通过合并左右两区间信息来求得该区间的信息．这种数据结构可以方便的进行大部分的区间操作．

有个大小为 $5$ 的数组 $a=\{10,11,12,13,14\}$，要将其转化为线段树，有以下做法：设线段树的根节点编号为 $1$，用数组 $d$ 来保存我们的线段树，$d_i$ 用来保存线段树上编号为 $i$ 的节点的值（这里每个节点所维护的值就是这个节点所表示的区间总和）．

我们先给出这棵线段树的形态，如图所示：

![](./images/segt1.svg)

图中每个节点中用红色字体标明的区间，表示该节点管辖的 $a$ 数组上的位置区间．如 $d_1$ 所管辖的区间就是 $[1,5]$（$a_1,a_2, \cdots ,a_5$），即 $d_1$ 所保存的值是 $a_1+a_2+ \cdots +a_5$，$d_1=60$ 表示的是 $a_1+a_2+ \cdots +a_5=60$．

通过观察不难发现，$d_i$ 的左儿子节点就是 $d_{2\times i}$，$d_i$ 的右儿子节点就是 $d_{2\times i+1}$．如果 $d_i$ 表示的是区间 $[s,t]$（即 $d_i=a_s+a_{s+1}+ \cdots +a_t$）的话，那么 $d_i$ 的左儿子节点表示的是区间 $[ s, \frac{s+t}{2} ]$，$d_i$ 的右儿子表示的是区间 $[ \frac{s+t}{2} +1,t ]$．

在实现时，我们考虑递归建树．设当前的根节点为 $p$，如果根节点管辖的区间长度已经是 $1$，则可以直接根据 $a$ 数组上相应位置的值初始化该节点．否则我们将该区间从中点处分割为两个子区间，分别进入左右子节点递归建树，最后合并两个子节点的信息．

### 实现

此处给出代码实现，可参考注释理解：

=== "C++"
    ```cpp
    void build(int s, int t, int p) {
      // 对 [s,t] 区间建立线段树,当前根的编号为 p
      if (s == t) {
        d[p] = a[s];
        return;
      }
      int m = s + ((t - s) >> 1);
      // 移位运算符的优先级小于加减法，所以加上括号
      // 如果写成 (s + t) >> 1 可能会超出 int 范围
      build(s, m, p * 2), build(m + 1, t, p * 2 + 1);
      // 递归对左右区间建树
      d[p] = d[p * 2] + d[(p * 2) + 1];
    }
    ```

=== "Python"
    ```python
    def build(s, t, p):
        # 对 [s,t] 区间建立线段树,当前根的编号为 p
        if s == t:
            d[p] = a[s]
            return
        m = s + ((t - s) >> 1)
        # 移位运算符的优先级小于加减法，所以加上括号
        # 如果写成 (s + t) >> 1 可能会超出 int 范围
        build(s, m, p * 2)
        build(m + 1, t, p * 2 + 1)
        # 递归对左右区间建树
        d[p] = d[p * 2] + d[(p * 2) + 1]
    ```

关于线段树的空间：如果采用堆式存储（$2p$ 是 $p$ 的左儿子，$2p+1$ 是 $p$ 的右儿子），若有 $n$ 个叶子结点，则 d 数组的范围最大为 $2^{\left\lceil\log{n}\right\rceil+1}$．

分析：容易知道线段树的深度是 $\left\lceil\log{n}\right\rceil$ 的，则在堆式储存情况下叶子节点（包括无用的叶子节点）数量为 $2^{\left\lceil\log{n}\right\rceil}$ 个，又由于其为一棵完全二叉树，则其总节点个数 $2^{\left\lceil\log{n}\right\rceil+1}-1$．当然如果你懒得计算的话可以直接把数组长度设为 $4n$，因为 $\frac{2^{\left\lceil\log{n}\right\rceil+1}-1}{n}$ 的最大值在 $n=2^{x}+1(x\in N_{+})$ 时取到，此时节点数为 $2^{\left\lceil\log{n}\right\rceil+1}-1=2^{x+2}-1=4n-5$．

而堆式存储存在无用的叶子节点，可以考虑使用内存池管理线段树节点，每当需要新建节点时从池中获取．自底向上考虑，必有每两个底层节点合并为一个上层节点，因此可以类似哈夫曼树地证明，如果有 $n$ 个叶子节点，这样的线段树总共有 $2n-1$ 个节点．其空间效率优于堆式存储，并且是可能的最优情况．

这样的线段树可以自底向上维护，参考「[统计的力量 - 张昆玮](https://github.com/hzwer/shareOI/blob/master/%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84/%E7%BB%9F%E8%AE%A1%E7%9A%84%E5%8A%9B%E9%87%8F%E2%80%94%E2%80%94%E7%BA%BF%E6%AE%B5%E6%A0%91%E5%85%A8%E6%8E%A5%E8%A7%A6_%E5%BC%A0%E6%98%86%E7%8E%AE.pptx)」．

## 线段树的区间查询

### 过程

区间查询，比如求区间 $[l,r]$ 的总和（即 $a_l+a_{l+1}+ \cdots +a_r$）、求区间最大值/最小值等操作．

![](./images/segt1.svg)

仍然以最开始的图为例，如果要查询区间 $[1,5]$ 的和，那直接获取 $d_1$ 的值（$60$）即可．

如果要查询的区间为 $[3,5]$，此时就不能直接获取区间的值，但是 $[3,5]$ 可以拆成 $[3,3]$ 和 $[4,5]$，可以通过合并这两个区间的答案来求得这个区间的答案．

一般地，如果要查询的区间是 $[l,r]$，则可以将其拆成最多为 $O(\log n)$ 个 **极大** 的区间，合并这些区间即可求出 $[l,r]$ 的答案．

### 实现

此处给出代码实现，可参考注释理解：

=== "C++"
    ```cpp
    int getsum(int l, int r, int s, int t, int p) {
      // [l, r] 为查询区间, [s, t] 为当前节点包含的区间, p 为当前节点的编号
      if (l <= s && t <= r)
        return d[p];  // 当前区间为询问区间的子集时直接返回当前区间的和
      int m = s + ((t - s) >> 1), sum = 0;
      if (l <= m) sum += getsum(l, r, s, m, p * 2);
      // 如果左儿子代表的区间 [s, m] 与询问区间有交集, 则递归查询左儿子
      if (r > m) sum += getsum(l, r, m + 1, t, p * 2 + 1);
      // 如果右儿子代表的区间 [m + 1, t] 与询问区间有交集, 则递归查询右儿子
      return sum;
    }
    ```

=== "Python"
    ```python
    def getsum(l, r, s, t, p):
        # [l, r] 为查询区间, [s, t] 为当前节点包含的区间, p 为当前节点的编号
        if l <= s and t <= r:
            return d[p]  # 当前区间为询问区间的子集时直接返回当前区间的和
        m = s + ((t - s) >> 1)
        sum = 0
        if l <= m:
            sum = sum + getsum(l, r, s, m, p * 2)
        # 如果左儿子代表的区间 [s, m] 与询问区间有交集, 则递归查询左儿子
        if r > m:
            sum = sum + getsum(l, r, m + 1, t, p * 2 + 1)
        # 如果右儿子代表的区间 [m + 1, t] 与询问区间有交集, 则递归查询右儿子
        return sum
    ```

## 线段树的区间修改与懒惰标记

### 过程

如果要求修改区间 $[l,r]$，把所有包含在区间 $[l,r]$ 中的节点都遍历一次、修改一次，时间复杂度无法承受．我们这里要引入一个叫做 **「懒惰标记」** 的东西．

懒惰标记，简单来说，就是通过延迟对节点信息的更改，从而减少可能不必要的操作次数．每次执行修改时，我们通过打标记的方法表明该节点对应的区间在某一次操作中被更改，但不更新该节点的子节点的信息．实质性的修改则在下一次访问带有标记的节点时才进行．

仍然以最开始的图为例，我们将执行若干次给区间内的数加上一个值的操作．我们现在给每个节点增加一个 $t_i$，表示该节点带的标记值．

最开始时的情况是这样的（为了节省空间，这里不再展示每个节点管辖的区间）：

![](./images/segt2.svg)

现在我们准备给 $[3,5]$ 上的每个数都加上 $5$．根据前面区间查询的经验，我们很快找到了两个极大区间 $[3,3]$ 和 $[4,5]$（分别对应线段树上的 $5$ 号点和 $3$ 号点）．

我们直接在这两个节点上进行修改，并给它们打上标记：

![](./images/segt3.svg)

我们发现，$3$ 号节点的信息虽然被修改了（因为该区间管辖两个数，所以 $d_3$ 加上的数是 $5 \times 2=10$），但它的两个子节点却还没更新，仍然保留着修改之前的信息．不过不用担心，虽然修改目前还没进行，但当我们要查询这两个子节点的信息时，我们会利用标记修改这两个子节点的信息，使查询的结果依旧准确．

接下来我们查询一下 $[4,4]$ 区间上各数字的和．

我们通过递归找到 $[4,5]$ 区间，发现该区间并非我们的目标区间，且该区间上还存在标记．这时候就到标记下放的时间了．我们将该区间的两个子区间的信息更新，并清除该区间上的标记．

![](./images/segt4.svg)

现在 $6$、$7$ 两个节点的值变成了最新的值，查询的结果也是准确的．

### 实现

接下来给出在存在标记的情况下，区间修改和查询操作的参考实现．

区间修改（区间加上某个值）：

=== "C++"
    ```cpp
    // [l, r] 为修改区间, c 为被修改的元素的变化量, [s, t] 为当前节点包含的区间, p
    // 为当前节点的编号
    void update(int l, int r, int c, int s, int t, int p) {
      // 当前区间为修改区间的子集时直接修改当前节点的值,然后打标记,结束修改
      if (l <= s && t <= r) {
        d[p] += (t - s + 1) * c, b[p] += c;
        return;
      }
      int m = s + ((t - s) >> 1);
      if (b[p] && s != t) {
        // 如果当前节点的懒标记非空,则更新当前节点两个子节点的值和懒标记值
        d[p * 2] += b[p] * (m - s + 1), d[p * 2 + 1] += b[p] * (t - m);
        b[p * 2] += b[p], b[p * 2 + 1] += b[p];  // 将标记下传给子节点
        b[p] = 0;                                // 清空当前节点的标记
      }
      if (l <= m) update(l, r, c, s, m, p * 2);
      if (r > m) update(l, r, c, m + 1, t, p * 2 + 1);
      d[p] = d[p * 2] + d[p * 2 + 1];
    }
    ```

=== "Python"
    ```python
    def update(l, r, c, s, t, p):
        # [l, r] 为修改区间, c 为被修改的元素的变化量, [s, t] 为当前节点包含的区间, p
        # 为当前节点的编号
        if l <= s and t <= r:
            d[p] = d[p] + (t - s + 1) * c
            b[p] = b[p] + c
            return
        # 当前区间为修改区间的子集时直接修改当前节点的值, 然后打标记, 结束修改
        m = s + ((t - s) >> 1)
        if b[p] and s != t:
            # 如果当前节点的懒标记非空, 则更新当前节点两个子节点的值和懒标记值
            d[p * 2] = d[p * 2] + b[p] * (m - s + 1)
            d[p * 2 + 1] = d[p * 2 + 1] + b[p] * (t - m)
            # 将标记下传给子节点
            b[p * 2] = b[p * 2] + b[p]
            b[p * 2 + 1] = b[p * 2 + 1] + b[p]
            # 清空当前节点的标记
            b[p] = 0
        if l <= m:
            update(l, r, c, s, m, p * 2)
        if r > m:
            update(l, r, c, m + 1, t, p * 2 + 1)
        d[p] = d[p * 2] + d[p * 2 + 1]
    ```

区间查询（区间求和）：

=== "C++"
    ```cpp
    int getsum(int l, int r, int s, int t, int p) {
      // [l, r] 为查询区间, [s, t] 为当前节点包含的区间, p 为当前节点的编号
      if (l <= s && t <= r) return d[p];
      // 当前区间为询问区间的子集时直接返回当前区间的和
      int m = s + ((t - s) >> 1);
      if (b[p]) {
        // 如果当前节点的懒标记非空,则更新当前节点两个子节点的值和懒标记值
        d[p * 2] += b[p] * (m - s + 1), d[p * 2 + 1] += b[p] * (t - m);
        b[p * 2] += b[p], b[p * 2 + 1] += b[p];  // 将标记下传给子节点
        b[p] = 0;                                // 清空当前节点的标记
      }
      int sum = 0;
      if (l <= m) sum = getsum(l, r, s, m, p * 2);
      if (r > m) sum += getsum(l, r, m + 1, t, p * 2 + 1);
      return sum;
    }
    ```

=== "Python"
    ```python
    def getsum(l, r, s, t, p):
        # [l, r] 为查询区间, [s, t] 为当前节点包含的区间, p为当前节点的编号
        if l <= s and t <= r:
            return d[p]
        # 当前区间为询问区间的子集时直接返回当前区间的和
        m = s + ((t - s) >> 1)
        if b[p]:
            # 如果当前节点的懒标记非空, 则更新当前节点两个子节点的值和懒标记值
            d[p * 2] = d[p * 2] + b[p] * (m - s + 1)
            d[p * 2 + 1] = d[p * 2 + 1] + b[p] * (t - m)
            # 将标记下传给子节点
            b[p * 2] = b[p * 2] + b[p]
            b[p * 2 + 1] = b[p * 2 + 1] + b[p]
            # 清空当前节点的标记
            b[p] = 0
        sum = 0
        if l <= m:
            sum = getsum(l, r, s, m, p * 2)
        if r > m:
            sum = sum + getsum(l, r, m + 1, t, p * 2 + 1)
        return sum
    ```

如果你是要实现区间修改为某一个值而不是加上某一个值的话，代码如下：

=== "C++"
    ```cpp
    void update(int l, int r, int c, int s, int t, int p) {
      if (l <= s && t <= r) {
        d[p] = (t - s + 1) * c, b[p] = c, v[p] = 1;
        return;
      }
      int m = s + ((t - s) >> 1);
      // 额外数组储存是否修改值
      if (v[p]) {
        d[p * 2] = b[p] * (m - s + 1), d[p * 2 + 1] = b[p] * (t - m);
        b[p * 2] = b[p * 2 + 1] = b[p];
        v[p * 2] = v[p * 2 + 1] = 1;
        v[p] = 0;
      }
      if (l <= m) update(l, r, c, s, m, p * 2);
      if (r > m) update(l, r, c, m + 1, t, p * 2 + 1);
      d[p] = d[p * 2] + d[p * 2 + 1];
    }
    
    int getsum(int l, int r, int s, int t, int p) {
      if (l <= s && t <= r) return d[p];
      int m = s + ((t - s) >> 1);
      if (v[p]) {
        d[p * 2] = b[p] * (m - s + 1), d[p * 2 + 1] = b[p] * (t - m);
        b[p * 2] = b[p * 2 + 1] = b[p];
        v[p * 2] = v[p * 2 + 1] = 1;
        v[p] = 0;
      }
      int sum = 0;
      if (l <= m) sum = getsum(l, r, s, m, p * 2);
      if (r > m) sum += getsum(l, r, m + 1, t, p * 2 + 1);
      return sum;
    }
    ```

=== "Python"
    ```python
    def update(l, r, c, s, t, p):
        if l <= s and t <= r:
            d[p] = (t - s + 1) * c
            b[p] = c
            v[p] = 1
            return
        m = s + ((t - s) >> 1)
        if v[p]:
            d[p * 2] = b[p] * (m - s + 1)
            d[p * 2 + 1] = b[p] * (t - m)
            b[p * 2] = b[p * 2 + 1] = b[p]
            v[p * 2] = v[p * 2 + 1] = 1
            v[p] = 0
        if l <= m:
            update(l, r, c, s, m, p * 2)
        if r > m:
            update(l, r, c, m + 1, t, p * 2 + 1)
        d[p] = d[p * 2] + d[p * 2 + 1]
    
    
    def getsum(l, r, s, t, p):
        if l <= s and t <= r:
            return d[p]
        m = s + ((t - s) >> 1)
        if v[p]:
            d[p * 2] = b[p] * (m - s + 1)
            d[p * 2 + 1] = b[p] * (t - m)
            b[p * 2] = b[p * 2 + 1] = b[p]
            v[p * 2] = v[p * 2 + 1] = 1
            v[p] = 0
        sum = 0
        if l <= m:
            sum = getsum(l, r, s, m, p * 2)
        if r > m:
            sum = sum + getsum(l, r, m + 1, t, p * 2 + 1)
        return sum
    ```

## 动态开点线段树

前面讲到堆式储存的情况下，需要给线段树开 $4n$ 大小的数组．为了节省空间，我们可以不一次性建好树，而是在最初只建立一个根结点代表整个区间．当我们需要访问某个子区间时，才建立代表这个区间的子结点．这样我们不再使用 $2p$ 和 $2p+1$ 代表 $p$ 结点的儿子，而是用 $\text{ls}$ 和 $\text{rs}$ 记录儿子的编号．总之，动态开点线段树的核心思想就是：**结点只有在有需要的时候才被创建**．

单次操作的时间复杂度是不变的，为 $O(\log n)$．由于每次操作都有可能创建并访问全新的一系列结点，因此 $m$ 次单点操作后结点的数量规模是 $O(m\log n)$．最多也只需要 $2n-1$ 个结点，没有浪费．

单点修改：

```cpp
// root 表示整棵线段树的根结点；cnt 表示当前结点个数
int n, cnt, root;
int sum[n * 2], ls[n * 2], rs[n * 2];

// 用法：update(root, 1, n, x, f); 其中 x 为待修改节点的编号
void update(int& p, int s, int t, int x, int f) {  // 引用传参
  if (!p) p = ++cnt;  // 当结点为空时，创建一个新的结点
  if (s == t) {
    sum[p] += f;
    return;
  }
  int m = s + ((t - s) >> 1);
  if (x <= m)
    update(ls[p], s, m, x, f);
  else
    update(rs[p], m + 1, t, x, f);
  sum[p] = sum[ls[p]] + sum[rs[p]];  // pushup
}
```

区间询问：

```cpp
// 用法：query(root, 1, n, l, r);
int query(int p, int s, int t, int l, int r) {
  if (!p) return 0;  // 如果结点为空，返回 0
  if (s >= l && t <= r) return sum[p];
  int m = s + ((t - s) >> 1), ans = 0;
  if (l <= m) ans += query(ls[p], s, m, l, r);
  if (r > m) ans += query(rs[p], m + 1, t, l, r);
  return ans;
}
```

区间修改也是一样的，不过下放标记时要注意如果缺少孩子，就直接创建一个新的孩子．或者使用标记永久化技巧．

## 一些优化

这里总结几个线段树的优化：

-   在叶子节点处无需下放懒惰标记，所以懒惰标记可以不下传到叶子节点．

-   下放懒惰标记可以写一个专门的函数 `pushdown`，从儿子节点更新当前节点也可以写一个专门的函数 `maintain`（或者对称地用 `pushup`），降低代码编写难度．

-   标记永久化：如果确定懒惰标记不会在中途被加到溢出（即超过了该类型数据所能表示的最大范围），那么就可以将标记永久化．标记永久化可以避免下传懒惰标记，只需在进行询问时把标记的影响加到答案当中，从而降低程序常数．具体如何处理与题目特性相关，需结合题目来写．这也是树套树和可持久化数据结构中会用到的一种技巧．

## C++ 模板

??? note "SegTreeLazyRangeAdd 可以区间加/求和的线段树模板"
    ```cpp
    --8<-- "docs/ds/code/seg/seg_4.hpp"
    ```

??? note "SegTreeLazyRangeSet 可以区间修改/求和的线段树模板"
    ```cpp
    --8<-- "docs/ds/code/seg/seg_5.hpp"
    ```

## 例题

???+ note "[luogu P3372【模板】线段树 1](https://www.luogu.com.cn/problem/P3372)"
    已知一个数列，你需要进行下面两种操作：
    
    -   将某区间每一个数加上 $k$．
    
    -   求出某区间每一个数的和．
    
    ??? note "参考代码"
        ```cpp
        --8<-- "docs/ds/code/seg/seg_1.cpp"
        ```

???+ note "[luogu P3373【模板】线段树 2](https://www.luogu.com.cn/problem/P3373)"
    已知一个数列，你需要进行下面三种操作：
    
    -   将某区间每一个数乘上 $x$．
    
    -   将某区间每一个数加上 $x$．
    
    -   求出某区间每一个数的和．
    
    ??? note "参考代码"
        ```cpp
        --8<-- "docs/ds/code/seg/seg_2.cpp"
        ```

???+ note "[HihoCoder 1078 线段树的区间修改](https://vjudge.net/problem/HihoCoder-1078)"
    假设货架上从左到右摆放了 $N$ 种商品，并且依次标号为 $1$ 到 $N$，其中标号为 $i$ 的商品的价格为 $Pi$．小 Hi 的每次操作分为两种可能，第一种是修改价格：小 Hi 给出一段区间 $[L, R]$ 和一个新的价格 $\textit{NewP}$，所有标号在这段区间中的商品的价格都变成 $\textit{NewP}$．第二种操作是询问：小 Hi 给出一段区间 $[L, R]$，而小 Ho 要做的便是计算出所有标号在这段区间中的商品的总价格，然后告诉小 Hi．
    
    ??? note "参考代码"
        ```cpp
        --8<-- "docs/ds/code/seg/seg_3.cpp"
        ```

???+ note "[2018 Multi-University Training Contest 5 Problem G. Glad You Came](https://acm.hdu.edu.cn/showproblem.php?pid=6356)"
    ??? note "解题思路"
        维护一下每个区间的永久标记就可以了，最后在线段树上跑一边 DFS 统计结果即可．注意打标记的时候加个剪枝优化，否则会 TLE．

## 拓展

线段树应用十分广泛，常见的拓展和变体如下：

-   [可持久化线段树](./persistent-seg.md)
-   各类树套树：
    -   [线段树套线段树](./seg-in-seg.md)
    -   [树状数组套线段树](./seg-in-bit.md)
    -   [线段树套平衡树](./balanced-in-seg.md)
    -   [平衡树套树状数组](./seg-in-balanced.md)
-   [李超线段树](./li-chao-tree.md)
-   [猫树](./cat-tree.md)
-   [吉司机线段树](./seg-beats.md)

详细内容请参阅相关页面．

## 应用：线段树优化建图

在建图连边的过程中，我们有时会碰到这种题目，一个点向一段连续的区间中的点连边或者一个连续的区间向一个点连边，如果我们真的一条一条连过去，那一旦点的数量多了复杂度就爆炸了，这里就需要用线段树的区间性质来优化我们的建图了．

下面是一个线段树．

![](./images/segt5.svg)

每个节点都代表了一个区间，假设我们要向区间 $[2, 4]$ 连边．

![](./images/segt6.svg)

在一些题目中，还会出现一个区间连向一个点的情况，则我们将上面第一张图的有向边全部反过来即可，上面的树叫做入树，下面这个叫做出树．

![](./images/segt7.svg)

???+ note "[Legacy](https://codeforces.com/problemset/problem/786/B)"
    题目大意：有 $n$ 个点、$q$ 次操作．每一种操作为以下三种类型中的一种：
    
    -   操作一：连一条 $u \rightarrow v$ 的有向边，权值为 $w$．
    -   操作二：对于所有 $i \in [l,r]$ 连一条 $u \rightarrow i$ 的有向边，权值为 $w$．
    -   操作三：对于所有 $i \in [l,r]$ 连一条 $i \rightarrow u$ 的有向边，权值为 $w$．
    
    求从点 $s$ 到其他点的最短路．
    
    $1 \le n,q \le 10^5, 1 \le w \le 10^9$．
    
    ??? note "参考代码"
        ```cpp
        --8<-- "docs/ds/code/seg/seg_8.cpp"
        ```

## 练习题目

-   [luogu P3372【模板】线段树 1](https://www.luogu.com.cn/problem/P3372)
-   [luogu P13825 线段树 1.5【动态开点线段树】](https://www.luogu.com.cn/problem/P13825)
-   [luogu P3373【模板】线段树 2](https://www.luogu.com.cn/problem/P3373)
-   [luogu P4588【TJOI2018】数学计算](https://www.luogu.com.cn/problem/P4588)
-   [luogu P5490【模板】扫描线 & 矩形面积并](https://www.luogu.com.cn/problem/P5490)
-   [luogu P1471 方差](https://www.luogu.com.cn/problem/P1471)


## ds/sgt.md

author: Ir1d, 0xis-cn

## 引入

**替罪羊树** 是一种依靠重构操作维持平衡的重量平衡树．替罪羊树会在插入、删除操作后，检测树是否发生失衡；如果失衡，将有针对性地进行重构以恢复平衡．

一般地，替罪羊树不支持区间操作，且无法完全持久化；但它具有实现简单、常数较小的优点．

## 基本结构和操作

替罪羊树的核心操作是重构、插入和删除操作．

### 节点信息

替罪羊树需要存储以下信息，用于树的自平衡操作：

-   树的结构信息：
    -   `id`：已使用节点数目；
    -   `rt`：根节点；
    -   `lc[x]`，`rc[x]`：左、右子节点；
    -   `tot[x]`：以 $x$ 为根的子树大小（每个节点计数为 $1$）[^tot-cnt]；
    -   `tot_active`：整个树中未删除（即 `cnt[x] != 0`）的节点的数目．

当使用替罪羊树实现平衡树时，还需要存储如下信息：

-   平衡树的节点信息：
    -   `val[x]`：节点存储的值；
    -   `cnt[x]`：节点存储的值的计数（可能为 $0$）；
    -   `sz[x]`：以 $x$ 为根的子树存储的值的计数．

为了维护节点信息，可以实现 `push_up` 操作：

???+ example "参考实现"
    ```cpp
    --8<-- "docs/ds/code/sgt/sgt.cpp:push-up"
    ```

应注意 `tot[x]` 和 `sz[x]` 的更新方式的不同．

### 重构操作

当树发生失衡时，需要对某个子树进行重构，使之尽可能平衡．重构分为两步：

-   对要重构的子树做中序遍历，将所有未删除节点存到序列中；
-   二分建树，即取中点为根，左右两侧递归地建子树，并更新节点信息．

参考实现如下：

???+ example "参考实现"
    ```cpp
    --8<-- "docs/ds/code/sgt/sgt.cpp:rebuild"
    ```

建树时注意维护节点信息，包括叶子节点的信息．

单次重构的复杂度是 $\Theta(|T_x|)$ 的，因此如果每次插入、删除时都进行重构，复杂度将难以接受．替罪羊树的核心思想就在于对重构时机的选择，进而实现了 $O(\log n)$ 的均摊复杂度．

### 插入操作

插入操作时，可能会引起树的失衡．为了判断树的失衡，需要引入参数 $\alpha\in(0.5,1)$，通常的选择在 $0.7\sim 0.8$ 之间．

如果新插入的节点的深度超过了 $\lfloor\log_{1/\alpha}|T|\rfloor$，其中，$|T|$ 为更新后的树的大小，就需要在回溯时寻找失衡发生的节点并进行重构．此时，需要根据如下条件判断以 $x$ 为根的子树失衡：

$$
\max\{|T_{\mathrm{left}(x)}|,|T_{\mathrm{right}(x)}|\} > \alpha\cdot |T_x|,
$$

其中，$\mathrm{left}(x)$ 和 $\mathrm{right}(x)$ 分别为 $x$ 的左、右子节点，$|T_x|$ 为以 $x$ 为根的子树大小．

插入操作的具体步骤如下：

-   首先利用二分查找树的性质向下找到插入值的位置，下探时记录深度；
-   如果已经有节点，直接修改节点信息，否则新建节点；
-   如果新建节点过深，就需要自下而上回溯到根，更新节点信息，并记录第一个（或任意一个）子树失衡的节点；
-   如果存在失衡节点，重构失衡节点的子树．

参考实现如下：

???+ example "参考实现"
    ```cpp
    --8<-- "docs/ds/code/sgt/sgt.cpp:insert"
    ```

注意，单次插入至多引起一次重构．如果没有新增节点或是新增节点并没有过深，又或是本次回溯过程中已经执行过重构，就不需要继续判断失衡了．多余的重构可能会导致效率损失[^insert-complexity]．回溯过程中的第一个失衡节点，就是所谓的「替罪羊」．

### 删除操作

删除操作的处理则非常简单．替罪羊树的删除策略是「懒删除」，即节点为空时，不移除节点，而是留待后续处理．

当然，如果树中空节点过多，树的访问效率会大大下降．因此，替罪羊树维护两个计数，整个树中未删除节点的数目和整个树实际使用的节点数目．对于选定的阈值[^threshold] $\alpha\in(0,1)$，当前者与后者的比值下降到 $\alpha$ 以下时，就对整个树做一次重构，重构时删除所有空节点．

???+ example "参考实现"
    ```cpp
    --8<-- "docs/ds/code/sgt/sgt.cpp:remove"
    ```

### 时间复杂度

大小为 $n$ 的替罪羊树的访问节点的时间复杂度为单次 $O(\log n)$ 的，$\Theta(n)$ 次插入和删除的均摊时间复杂度也是单次 $O(\log n)$ 的．

本节对替罪羊树的时间复杂度仅做简要论证，详细证明请参考原论文．

??? note "替罪羊树的时间复杂度的论证"
    由于采用懒删除的策略，未删除节点数目为 $n$ 的替罪羊树可能占用了 $\alpha^{-1}n$ 个节点．由于仅仅相差一个常数因子，本文在表述中并不区分替罪羊树的未删除节点数目和占用节点数目，而统一称为「树的大小」．
    
    1.  **访问操作**：访问操作的复杂度得以保证，是因为大小为 $n$ 的替罪羊树的树高总是 $O(\log n)$ 的．
    
        首先，区分两个概念：
    
        -   $\alpha$‑重量平衡：所有节点处，左、右子节点的子树的大小均不超过该节点处子树的大小的 $\alpha$ 倍；
        -   $\alpha$‑高度平衡：树的高度不超过 $\lfloor\log_{1/\alpha}|T|\rfloor$，其中，$T$ 是树的大小．
    
        $\alpha$‑重量平衡可以推出 $\alpha$‑高度平衡，因为子节点深度每增加一，大小就减少到原来的 $\alpha$ 倍；反过来则不一定成立．更严格地说，每次操作结束后，替罪羊树都总是 $\alpha$‑高度平衡的[^hei-bal]，这就保证了访问操作的复杂度．
    
        只有插入操作会改变树的结构，所以只需要说明每次插入操作后，替罪羊树都仍是 $\alpha$‑高度平衡的．如果新插入的节点过深，造成了整个树不再 $\alpha$‑高度平衡，那么自该节点回溯至根时，至少会碰上一个节点，即「替罪羊」，它的子树不再 $\alpha$‑重量平衡．将其重构后，子树的高度将降低至少一，故而新插入的节点将不再过深．
    2.  **插入操作**：插入操作的复杂度是均摊 $O(\log n)$ 的．
    
        设在某次插入操作后，节点 $x$ 处发生一次子树的重构，时间成本为 $\Theta(|T_x|)$．因为节点 $x$ 刚插入时，或者它刚刚经历了（自身或祖先节点的）上一次重构之后，它的左右子树至多只相差一个节点．而在这次重构之前，节点 $x$ 处必然成立
    
        $$
        \max\{|T_{\mathrm{left}(x)}|,|T_{\mathrm{right}(x)}|\} > \alpha\cdot |T_x|.
        $$
    
        这一条件保证左右子树的大小的差值至少为 $(2\alpha-1)|T_x|$ 的．因而，这两次重构之间，子树 $T_x$ 中插入了 $\Omega(|T_x|)$ 个节点．
    
        利用摊还分析可知[^alternative-analysis]，如果每次插入节点时，都在（可能的重构前）自根到该节点的路径上的每个节点都增加 $\Theta(1)$ 的势能，那么到节点 $x$ 处子树重构前，必然已经在节点 $x$ 处累积了 $\Omega(|T_x|)$ 的势能，足以用于偿还 $x$ 处子树重构的成本 $\Theta(|T_x|)$．因为树的深度都是 $O(\log n)$ 的，所以单次插入增加的势能是 $O(\log n)$ 的；这说明，$\Theta(n)$ 次插入操作中势能增加的总和是 $O(n\log n)$ 的．由此，子树重构的总成本也是 $O(n\log n)$ 的，单次插入操作（含重构）的均摊时间复杂度就是 $O(\log n)$ 的．
    
        注意，分析中没有假定在节点 $x$ 处的两次重构之间，子树 $T_x$ 内部没有发生其它的重构．因此，只要只重构满足失衡条件的节点处的子树，就能保证复杂度正确．
    3.  **删除操作**：删除操作的复杂度也是均摊 $O(\log n)$ 的．
    
        删除引起的重构会导致整个树不含空节点．而某次删除引起重构之前，整个树中已经有 $\Theta(n)$ 个空节点，这意味着至少进行了 $\Theta(n)$ 次删除操作．因为每次删除操作的寻址的复杂度是 $O(\log n)$ 的，且单次重构的复杂度是 $\Theta(n)$，所以这 $\Theta(n)$ 次删除操作的实际时间成本为
    
        $$
        \Theta(n)O(\log n)+\Theta(n)
        $$
    
        的．故而，单次删除的均摊复杂度为 $O(\log n)$ 的．

## 平衡树操作

本节介绍用替罪羊树维护可重集的方法．

除上节介绍的操作外，其余操作均为平衡树的常见操作．但是，因为替罪羊树中可能存在空节点，这些操作也需要相应调整．

### 查询排名

利用二分查找树的性质向下查找节点位置，过程中记录路径左侧存储的值的数目即可．

???+ example "参考实现"
    ```cpp
    --8<-- "docs/ds/code/sgt/sgt.cpp:find-rank"
    ```

### 根据排名查询值

利用节点记录的子树存储值的数目信息向下查找即可．注意可能存在计数为零的节点．

???+ example "参考实现"
    ```cpp
    --8<-- "docs/ds/code/sgt/sgt.cpp:find-kth"
    ```

### 查询前驱、后继

以上两种功能结合即可．

???+ example "参考实现"
    ```cpp
    --8<-- "docs/ds/code/sgt/sgt.cpp:pred-succ"
    ```

如果想直接实现，应注意处理计数为零的节点．

### 参考实现

本节的最后，给出模板题 [普通平衡树](https://loj.ac/p/104) 的参考实现．

??? example "参考实现"
    ```cpp
    --8<-- "docs/ds/code/sgt/sgt.cpp:full-text"
    ```

## 参考资料

-   Galperin, Igal, and Ronald L. Rivest. "Scapegoat trees." Proceedings of the fourth annual ACM-SIAM Symposium on Discrete algorithms. 1993.
-   [Scapegoat Tree - Wikipedia](https://en.wikipedia.org/wiki/Scapegoat_tree)
-   [替罪羊树 - riteme 的博客](https://riteme.site/blog/2016-4-6/scapegoat.html)

[^tot-cnt]: 也可以只统计未删除节点数目，此时不再需要统计 `tot_active`，而需要统计所有占用节点数目 `tot_max`，代码相应调整即可．

[^insert-complexity]: 根据后文的复杂度分析可知，这些效率损失仅意味着更大的常数因子，而复杂度依然是正确的．因为判断树深可能会涉及较多的浮点数对数运算，不判断树深只判断失衡的代码在某些数据中可能更快．

[^threshold]: 不必与上文插入操作时选取的参数相同．尽管原论文做了这样的假定，但是选取不同的参数只会导致单次操作的复杂度中常数项的变化，整体复杂度依然是正确的．

[^hei-bal]: 按原文定义，$n$ 指未删除节点的数目，故而只能保证树高不超过 $\lfloor\log_{1/\alpha}n\rfloor+1$，这称为弱 $\alpha$‑高度平衡．此处没有细究该常数项的差异．

[^alternative-analysis]: 有些文章会简单分析成 $\Omega(|T_x|)$ 次插入对应一次重构，故而均摊复杂度为 $\dfrac{\Omega(|T_x|)O(\log n)+\Theta(|T_x|)}{\Omega(|T_x|)} = O(\log n)$．这样的思路可以辅助理解均摊复杂度为什么正确，但并不严谨．这是因为，一次插入可能对应着多个祖先节点的重构，故而当节点 $x$ 发生重构时，子树内未引起重构的节点数目并不显然是 $\Omega(|T_x|)$ 的．


## ds/skiplist.md

跳表 (Skip List) 是由 William Pugh 发明的一种查找数据结构，支持对数据的快速查找，插入和删除．

跳表的期望空间复杂度为 $O(n)$，跳表的查询，插入和删除操作的期望时间复杂度都为 $O(\log n)$．

## 基本思想

顾名思义，跳表是一种类似于链表的数据结构．更加准确地说，跳表是对有序链表的改进．

为方便讨论，后续所有有序链表默认为 **升序** 排序．

一个有序链表的查找操作，就是从头部开始逐个比较，直到当前节点的值大于或者等于目标节点的值．很明显，这个操作的复杂度是 $O(n)$．

跳表在有序链表的基础上，引入了 **分层** 的概念．首先，跳表的每一层都是一个有序链表，特别地，最底层是初始的有序链表．每个位于第 $i$ 层的节点有 $p$ 的概率出现在第 $i+1$ 层，$p$ 为常数．

记在 $n$ 个节点的跳表中，期望包含 $\frac{1}{p}$ 个元素的层为第 $L(n)$ 层，易得 $L(n) = \log_{\frac{1}{p}}n$．

在跳表中查找，就是从第 $L(n)$ 层开始，水平地逐个比较直至当前节点的下一个节点大于等于目标节点，然后移动至下一层．重复这个过程直至到达第一层且无法继续进行操作．此时，若下一个节点是目标节点，则成功查找；反之，则元素不存在．这样一来，查找的过程中会跳过一些没有必要的比较，所以相比于有序链表的查询，跳表的查询更快．可以证明，跳表查询的平均复杂度为 $O(\log n)$．

## 复杂度证明

### 空间复杂度

对于一个节点而言，节点的最高层数为 $i$ 的概率为 $p^{i-1}(1 - p)$．所以，跳表的期望层数为 $\sum_{i\ge 1} ip^{i - 1}(1-p) = \frac{1}{1 - p}$，且因为 $p$ 为常数，所以跳表的 **期望空间复杂度** 为 $O(n)$．

在最坏的情况下，每一层有序链表等于初始有序链表，即跳表的 **最差空间复杂度** 为 $O(n \log n)$．

### 时间复杂度

从后向前分析查找路径，这个过程可以分为从最底层爬到第 $L(n)$ 层和后续操作两个部分．在分析时，假设一个节点的具体信息在它被访问之前是未知的．

假设当前我们处于一个第 $i$ 层的节点 $x$，我们并不知道 $x$ 的最大层数和 $x$ 左侧节点的最大层数，只知道 $x$ 的最大层数至少为 $i$．如果 $x$ 的最大层数大于 $i$，那么下一步应该是向上走，这种情况的概率为 $p$；如果 $x$ 的最大层数等于 $i$，那么下一步应该是向左走，这种情况概率为 $1-p$．

令 $C(i)$ 为在一个无限长度的跳表中向上爬 $i$ 层的期望代价，那么有：

$$
\begin{aligned}
C(0) & = 0 \\
C(i) & = (1-p)(1+C(i)) + p(1+C(i-1))
\end{aligned}
$$

解得 $C(i)=\frac{i}{p}$．

由此可以得出：在长度为 $n$ 的跳表中，从最底层爬到第 $L(n)$ 层的期望步数存在上界 $\frac{L(n) - 1}{p}$．

现在只需要分析爬到第 $L(n)$ 层后还要再走多少步．易得，到了第 $L(n)$ 层后，向左走的步数不会超过第 $L(n)$ 层及更高层的节点数总和，而这个总和的期望为 $\frac{1}{p}$．所以到了第 $L(n)$ 层后向左走的期望步数存在上界 $\frac{1}{p}$．同理，到了第 $L(n)$ 层后向上走的期望步数存在上界 $\frac{1}{p}$．

所以，跳表查询的期望查找步数为 $\frac{L(n) - 1}{p} + \frac{2}{p}$，又因为 $L(n)=\log_{\frac{1}{p}}n$，所以跳表查询的 **期望时间复杂度** 为 $O(\log n)$．

在最坏的情况下，每一层有序链表等于初始有序链表，查找过程相当于对最高层的有序链表进行查询，即跳表查询操作的 **最差时间复杂度** 为 $O(n)$．

插入操作和删除操作就是进行一遍查询的过程，途中记录需要修改的节点，最后完成修改．易得每一层至多只需要修改一个节点，又因为跳表期望层数为 $\log_{\frac{1}{p}}n$，所以插入和修改的 **期望时间复杂度** 也为 $O(\log n)$．

## 具体实现

### 获取节点的最大层数

模拟以 $p$ 的概率往上加一层，最后和上限值取最小．

```cpp
int randomLevel() {
  int lv = 1;
  // MAXL = 32, S = 0xFFFF, PS = S * P, P = 1 / 4
  while ((rand() & S) < PS) ++lv;
  return min(MAXL, lv);
}
```

### 查询

查询跳表中是否存在键值为 `key` 的节点．具体实现时，可以设置两个哨兵节点以减少边界条件的讨论．

```cpp
V& find(const K& key) {
  SkipListNode<K, V>* p = head;

  // 找到该层最后一个键值小于 key 的节点，然后走向下一层
  for (int i = level; i >= 0; --i) {
    while (p->forward[i]->key < key) {
      p = p->forward[i];
    }
  }
  // 现在是小于，所以还需要再往后走一步
  p = p->forward[0];

  // 成功找到节点
  if (p->key == key) return p->value;

  // 节点不存在，返回 INVALID
  return tail->value;
}
```

### 插入

插入节点 `(key, value)`．插入节点的过程就是先执行一遍查询的过程，中途记录新节点是要插入哪一些节点的后面，最后再执行插入．每一层最后一个键值小于 `key` 的节点，就是需要进行修改的节点．

```cpp
void insert(const K &key, const V &value) {
  // 用于记录需要修改的节点
  SkipListNode<K, V> *update[MAXL + 1];

  SkipListNode<K, V> *p = head;
  for (int i = level; i >= 0; --i) {
    while (p->forward[i]->key < key) {
      p = p->forward[i];
    }
    // 第 i 层需要修改的节点为 p
    update[i] = p;
  }
  p = p->forward[0];

  // 若已存在则修改
  if (p->key == key) {
    p->value = value;
    return;
  }

  // 获取新节点的最大层数
  int lv = randomLevel();
  if (lv > level) {
    lv = ++level;
    update[lv] = head;
  }

  // 新建节点
  SkipListNode<K, V> *newNode = new SkipListNode<K, V>(key, value, lv);
  // 在第 0~lv 层插入新节点
  for (int i = lv; i >= 0; --i) {
    p = update[i];
    newNode->forward[i] = p->forward[i];
    p->forward[i] = newNode;
  }

  ++length;
}
```

### 删除

删除键值为 `key` 的节点．删除节点的过程就是先执行一遍查询的过程，中途记录要删的节点是在哪一些节点的后面，最后再执行删除．每一层最后一个键值小于 `key` 的节点，就是需要进行修改的节点．

```cpp
bool erase(const K &key) {
  // 用于记录需要修改的节点
  SkipListNode<K, V> *update[MAXL + 1];

  SkipListNode<K, V> *p = head;
  for (int i = level; i >= 0; --i) {
    while (p->forward[i]->key < key) {
      p = p->forward[i];
    }
    // 第 i 层需要修改的节点为 p
    update[i] = p;
  }
  p = p->forward[0];

  // 节点不存在
  if (p->key != key) return false;

  // 从最底层开始删除
  for (int i = 0; i <= level; ++i) {
    // 如果这层没有 p 删除就完成了
    if (update[i]->forward[i] != p) {
      break;
    }
    // 断开 p 的连接
    update[i]->forward[i] = p->forward[i];
  }

  // 回收空间
  delete p;

  // 删除节点可能导致最大层数减少
  while (level > 0 && head->forward[level] == tail) --level;

  // 跳表长度
  --length;
  return true;
}
```

### 完整代码

下列代码是用跳表实现的 map．未经正经测试，仅供参考．

??? note "参考代码"
    ```cpp
    #include <cassert>
    #include <climits>
    #include <ctime>
    #include <iostream>
    #include <map>
    using namespace std;
    
    template <typename K, typename V>
    struct SkipListNode {
      int level;
      K key;
      V value;
      SkipListNode **forward;
    
      SkipListNode() {}
    
      SkipListNode(K k, V v, int l, SkipListNode *nxt = NULL) {
        key = k;
        value = v;
        level = l;
        forward = new SkipListNode *[l + 1];
        for (int i = 0; i <= l; ++i) forward[i] = nxt;
      }
    
      ~SkipListNode() {
        if (forward != NULL) delete[] forward;
      }
    };
    
    template <typename K, typename V>
    struct SkipList {
      static constexpr int MAXL = 32;
      static constexpr int P = 4;
      static constexpr int S = 0xFFFF;
      static constexpr int PS = S / P;
      static constexpr int INVALID = INT_MAX;
    
      SkipListNode<K, V> *head, *tail;
      int length;
      int level;
    
      SkipList() {
        srand(time(nullptr));
    
        level = length = 0;
        tail = new SkipListNode<K, V>(INVALID, 0, 0);
        head = new SkipListNode<K, V>(INVALID, 0, MAXL, tail);
      }
    
      ~SkipList() {
        delete head;
        delete tail;
      }
    
      int randomLevel() {
        int lv = 1;
        while ((rand() & S) < PS) ++lv;
        return MAXL > lv ? lv : MAXL;
      }
    
      void insert(const K &key, const V &value) {
        SkipListNode<K, V> *update[MAXL + 1];
    
        SkipListNode<K, V> *p = head;
        for (int i = level; i >= 0; --i) {
          while (p->forward[i]->key < key) {
            p = p->forward[i];
          }
          update[i] = p;
        }
        p = p->forward[0];
    
        if (p->key == key) {
          p->value = value;
          return;
        }
    
        int lv = randomLevel();
        if (lv > level) {
          lv = ++level;
          update[lv] = head;
        }
    
        SkipListNode<K, V> *newNode = new SkipListNode<K, V>(key, value, lv);
        for (int i = lv; i >= 0; --i) {
          p = update[i];
          newNode->forward[i] = p->forward[i];
          p->forward[i] = newNode;
        }
    
        ++length;
      }
    
      bool erase(const K &key) {
        SkipListNode<K, V> *update[MAXL + 1];
        SkipListNode<K, V> *p = head;
    
        for (int i = level; i >= 0; --i) {
          while (p->forward[i]->key < key) {
            p = p->forward[i];
          }
          update[i] = p;
        }
        p = p->forward[0];
    
        if (p->key != key) return false;
    
        for (int i = 0; i <= level; ++i) {
          if (update[i]->forward[i] != p) {
            break;
          }
          update[i]->forward[i] = p->forward[i];
        }
    
        delete p;
    
        while (level > 0 && head->forward[level] == tail) --level;
        --length;
        return true;
      }
    
      V &operator[](const K &key) {
        V v = find(key);
        if (v == tail->value) insert(key, 0);
        return find(key);
      }
    
      V &find(const K &key) {
        SkipListNode<K, V> *p = head;
        for (int i = level; i >= 0; --i) {
          while (p->forward[i]->key < key) {
            p = p->forward[i];
          }
        }
        p = p->forward[0];
        if (p->key == key) return p->value;
        return tail->value;
      }
    
      bool count(const K &key) { return find(key) != tail->value; }
    };
    
    int main() {
      SkipList<int, int> L;
      map<int, int> M;
    
      clock_t s = clock();
    
      for (int i = 0; i < 1e5; ++i) {
        int key = rand(), value = rand();
        L[key] = value;
        M[key] = value;
      }
    
      for (int i = 0; i < 1e5; ++i) {
        int key = rand();
        if (i & 1) {
          L.erase(key);
          M.erase(key);
        } else {
          int r1 = L.count(key) ? L[key] : 0;
          int r2 = M.count(key) ? M[key] : 0;
          assert(r1 == r2);
        }
      }
    
      clock_t e = clock();
      cout << "Time elapsed: " << (double)(e - s) / CLOCKS_PER_SEC << endl;
      // about 0.2s
    
      return 0;
    }
    ```

## 跳表的随机访问优化

访问跳表中第 $k$ 个节点，相当于访问初始有序链表中的第 $k$ 个节点，很明显这个操作的时间复杂度是 $O(n)$ 的，并不足够优秀．

跳表的随机访问优化就是对每一个前向指针，再多维护这个前向指针的长度．假设 $A$ 和 $B$ 都是跳表中的节点，其中 $A$ 为跳表的第 $a$ 个节点，$B$ 为跳表的第 $b$ 个节点 $(a < b)$，且在跳表的某一层中 $A$ 的前向指针指向 $B$，那么这个前向指针的长度为 $b - a$．

现在访问跳表中的第 $k$ 个节点，就可以从顶层开始，水平地遍历该层的链表，直到当前节点的位置加上当前节点在该层的前向指针长度大于等于 $k$，然后移动至下一层．重复这个过程直至到达第一层且无法继续行操作．此时，当前节点就是跳表中第 $k$ 个节点．

这样，就可以快速地访问到跳表的第 $k$ 个元素．可以证明，这个操作的时间复杂度为 $O(\log n)$．

## 参考资料

1.  [Skip Lists: A Probabilistic Alternative to Balanced Trees](https://15721.courses.cs.cmu.edu/spring2018/papers/08-oltpindexes1/pugh-skiplists-cacm1990.pdf)
2.  [Skip List](https://en.wikipedia.org/wiki/Skip_list)
3.  [A Skip List Cookbook](http://cglab.ca/~morin/teaching/5408/refs/p90b.pdf)


## ds/sparse-table.md

## 定义

![ST 表示意图](images/st.svg)

ST 表（Sparse Table，稀疏表）是用于解决 **可重复贡献问题** 的数据结构．

???+ note "什么是可重复贡献问题？"
    **可重复贡献问题** 是指对于运算 $\operatorname{opt}$，满足 $x\operatorname{opt} x=x$，则对应的区间询问就是一个可重复贡献问题．例如，最大值有 $\max(x,x)=x$，gcd 有 $\operatorname{gcd}(x,x)=x$，所以 RMQ 和区间 GCD 就是一个可重复贡献问题．像区间和就不具有这个性质，如果求区间和的时候采用的预处理区间重叠了，则会导致重叠部分被计算两次，这是我们所不愿意看到的．另外，$\operatorname{opt}$ 还必须满足结合律才能使用 ST 表求解．

???+ note "什么是 RMQ？"
    RMQ 是英文 Range Maximum/Minimum Query 的缩写，表示区间最大（最小）值．解决 RMQ 问题有很多种方法，可以参考 [RMQ 专题](../topic/rmq.md)．

## 引入

???+ example "[Luogu P3865【模板】ST 表 & RMQ 问题](https://www.luogu.com.cn/problem/P3865)"
    给定 $n$（$1\le n\le 10^5$）个整数，有 $m$（$1\le m\le 2\times 10^6$）个询问，对于每个询问，你需要回答区间 $[l,r]$ 中的最大值．

考虑暴力做法．每次都对区间 $[l,r]$ 扫描一遍，求出最大值．

显然，这个算法会超时．

## ST 表

ST 表基于 [倍增](../basic/binary-lifting.md) 思想，可以做到 $\Theta(n\log n)$ 预处理，$\Theta(1)$ 回答每个询问．但是不支持修改操作．

基于倍增思想，我们考虑如何求出区间最大值．可以发现，如果按照一般的倍增流程，每次跳 $2^i$ 步的话，询问时的复杂度仍旧是 $\Theta(\log n)$，并没有比线段树更优，反而预处理一步还比线段树慢．

我们发现 $\max(x,x)=x$，也就是说，区间最大值是一个具有「可重复贡献」性质的问题．即使用来求解的预处理区间有重叠部分，只要这些区间的并是所求的区间，最终计算出的答案就是正确的．

如果手动模拟一下，可以发现我们能使用至多两个预处理过的区间来覆盖询问区间，也就是说询问时的时间复杂度可以被降至 $\Theta(1)$，在处理有大量询问的题目时十分有效．

具体实现如下：

令 $f(i,j)$ 表示区间 $[i,i+2^j-1]$ 的最大值．

显然 $f(i,0)=a_i$．

根据定义式，第二维就相当于倍增的时候「跳了 $2^j-1$ 步」，依据倍增的思路，写出状态转移方程：$f(i,j)=\max(f(i,j-1),f(i+2^{j-1},j-1))$．

![](./images/st-preprocess-lift.svg)

以上就是预处理部分．而对于查询，可以简单实现如下：

对于每个询问 $[l,r]$，我们把它分成两部分：$[l,l+2^s-1]$ 与 $[r-2^s+1,r]$，其中 $s=\left\lfloor\log_2(r-l+1)\right\rfloor$．两部分的结果的最大值就是回答．

![ST 表的查询过程](./images/st-query.svg)

根据上面对于「可重复贡献问题」的论证，由于最大值是「可重复贡献问题」，重叠并不会对区间最大值产生影响．又因为这两个区间完全覆盖了 $[l,r]$，可以保证答案的正确性．

???+ example "[Luogu P3865【模板】ST 表 & RMQ 问题](https://www.luogu.com.cn/problem/P3865) 参考实现"
    === "C 风格"
        ```cpp
        --8<-- "docs/ds/code/sparse-table/sparse-table_1.cpp"
        ```
    
    === "C++ 风格"
        ```cpp
        --8<-- "docs/ds/code/sparse-table/sparse-table_2.cpp"
        ```
    
    === "Python"
        ```python
        --8<-- "docs/ds/code/sparse-table/sparse-table_1.py"
        ```

## 注意点

1.  输入输出数据一般很多，建议开启输入输出优化．

2.  在预处理 ST 表时通常需要建立一个一维大小为 $\log n$，另一维大小为 $n$ 的数组，此时应优先让大小为 $\log n$ 的维度作为第一维，以提升缓存局部性．

3.  每次用 [std::log](https://en.cppreference.com/w/cpp/numeric/math/log) 重新计算对数函数值并不值得，建议利用 `__builtin_clz` 或 `__lg` 等内建函数进行计算．如无法利用这些内建函数，也可以预处理对数函数值．预处理方式如下所示：

$$
\begin{cases}
\texttt{Logn}[1] \gets 0, \\
\texttt{Logn}\left[i\right] \gets \texttt{Logn}\left[\frac{i}{2}\right] + 1.
\end{cases}
$$

## ST 表维护其他信息

除 RMQ 以外，还有其它的「可重复贡献问题」．例如「区间按位与」、「区间按位或」、「区间 GCD」，ST 表都能高效地解决．

需要注意的是，对于「区间 GCD」，ST 表的查询复杂度并没有比线段树更优（令值域为 $w$，ST 表的查询复杂度为 $\Theta(\log w)$，而线段树为 $\Theta(\log n+\log w)$，且值域一般是大于 $n$ 的），但是 ST 表的预处理复杂度也没有比线段树更劣，而编程复杂度方面 ST 表比线段树简单很多．

如果分析一下，「可重复贡献问题」一般都带有某种类似 RMQ 的成分．例如「区间按位与」就是每一位取最小值，而「区间 GCD」则是每一个质因数的指数取最小值．

## 总结

ST 表能较好的维护「可重复贡献」的区间信息（同时也应满足结合律），时间复杂度较低，代码量相对其他算法很小．但是，ST 表能维护的信息非常有限，不能较好地扩展，并且不支持修改操作．

## 习题

-   [「SCOI2007」降雨量](https://loj.ac/p/2279)

-   [\[USACO07JAN\] 平衡的阵容 Balanced Lineup](https://www.luogu.com.cn/problem/P2880)

## 附录：ST 表求区间 GCD 的时间复杂度分析

在算法运行的时候，可能要经过 $\Theta(\log n)$ 次迭代．每一次迭代都可能会使用 GCD 函数进行递归，令值域为 $w$，GCD 函数的时间复杂度最高是 $\Omega(\log w)$ 的，所以总时间复杂度看似有 $O(n\log n\log w)$．

但是，在 GCD 的过程中，每一次递归（除最后一次递归之外）都会使数列中的某个数至少减半，而数列中的数最多减半的次数为 $\log_2 (w^n)=\Theta(n\log w)$，所以，GCD 的递归部分最多只会运行 $O(n\log w)$ 次．再加上循环部分（以及最后一层递归）的 $\Theta(n\log n)$，最终时间复杂度则是 $O(n(\log w+\log n))$，由于可以构造数据使得时间复杂度为 $\Omega(n(\log w+\log n))$，所以最终的时间复杂度即为 $\Theta(n(\log w+\log n))$．

而查询部分的时间复杂度很好分析，考虑最劣情况，即每次询问都询问最劣的一对数，时间复杂度为 $\Theta(\log w)$．因此，ST 表维护「区间 GCD」的时间复杂度为预处理 $\Theta(n(\log n+\log w))$，单次查询 $\Theta(\log w)$．

线段树的相应操作是预处理 $\Theta(n\log w)$，单次查询 $\Theta(\log n+\log w)$．

这并不是一个严谨的数学论证，更为严谨的附在下方：

??? note "更严谨的证明"
    理解本段，可能需要具备 [时间复杂度](../basic/complexity.md) 的关于「势能分析法」的知识．
    
    先分析预处理部分的时间复杂度：
    
    设「待考虑数列」为在预处理 ST 表的时候当前层循环的数列．例如，第零层的数列就是原数列，第一层的数列就是第零层的数列经过一次迭代之后的数列，即 `st[1..n][1]`，我们将其记为 $A$．
    
    而势能函数就定义为「待考虑数列」中所有数的累乘的以二为底的对数．即：$\Phi(A)=\log_2\left(\prod\limits_{i=1}^n A_i\right)$．
    
    在一次迭代中，所花费的时间相当于迭代循环所花费的时间与 GCD 所花费的时间之和．其中，GCD 花费的时间有长有短．最短可能只有两次甚至一次递归，而最长可能有 $O(\log w)$ 次递归．但是，GCD 过程中，除最开头一层与最末一层以外，每次递归都会使「待考虑数列」中的某个结果至少减半．即，$\Phi(A)$ 会减少至少 $1$，该层递归所用的时间可以被势能函数均摊．
    
    同时，我们可以看到，$\Phi(A)$ 的初值最大为 $\log_2 (w^n)=\Theta(n\log w)$，而 $\Phi(A)$ 不增．所以，ST 表预处理部分的时间复杂度为 $O(n(\log w+\log n))$．


## ds/splay.md

本页面将简要介绍如何用 Splay 维护二叉查找树．

## 定义

**Splay 树**，或 **伸展树**，是一种平衡二叉查找树，它通过 **伸展（splay）操作** 不断将某个节点旋转到根节点，使得整棵树仍然满足二叉查找树的性质，能够在均摊 $O(\log N)$ 时间内完成插入、查找和删除操作，并且保持平衡而不至于退化为链．

Splay 树由 Daniel Sleator 和 Robert Tarjan 于 1985 年发明．

## 基本结构与操作

本节讨论 Splay 树的基本结构和它的核心操作，其中最为重要的是伸展操作．

Splay 树是一棵二叉查找树，查找某个值时满足性质：左子树任意节点的值 $<$ 根节点的值 $<$ 右子树任意节点的值．

### 维护信息

本文使用数组模拟指针来实现 Splay 树，需要维护如下信息：

|   rt  |    id   | fa\[i] | ch\[i]\[0/1] | val\[i] | cnt\[i] | sz\[i] |
| :---: | :-----: | :----: | :----------: | :-----: | :-----: | :----: |
| 根节点编号 | 已使用节点个数 |   父亲   |    左右儿子编号    |   节点权值  |  权值出现次数 |  子树大小  |

初始化时，所有信息都置零即可．

### 辅助操作

首先是一些简单的辅助操作：

-   `dir(x)`：判断节点 $x$ 是父亲节点的左儿子还是右儿子；
-   `push_up(x)`：在改变节点位置后，根据子节点信息更新节点 $x$ 的信息．

???+ example "实现"
    ```cpp
    --8<-- "docs/ds/code/splay/splay-1.cpp:aux"
    ```

### 旋转操作

为了使 Splay 保持平衡，需要进行旋转操作．旋转的作用是将某个节点上移一个位置．

旋转需要保证：

-   整棵 Splay 的中序遍历不变（不能破坏二叉查找树的性质）；
-   受影响的节点维护的信息依然正确有效；
-   `rt` 必须指向旋转后的根节点．

在 Splay 中旋转分为两种：左旋和右旋．

![](./images/splay-rotate.svg)

观察图示可知，如果要通过旋转将节点 $x$（左旋时的 $1$ 和右旋时的 $2$）上移，则旋转的方向由该节点是其父节点的左节点还是右节点唯一确定．因此，实现旋转操作时，只需要将要上移的节点 $x$ 传入即可．

具体分析旋转步骤：（假设需要上移的节点为 $x$，以右旋为例）

1.  首先，记录节点 $x$ 的父节点 $y$，以及 $y$ 的父节点 $z$（可能为空），并记录 $x$ 是 $y$ 的左子节点还是右子节点；
2.  按照旋转后的树中自下向上的顺序，依次更新 $y$ 的左子节点为 $x$ 的右子节点，$x$ 的右子节点为 $y$，以及若 $z$ 非空，$z$ 的子节点为 $x$；
3.  按照同样的顺序，依次更新当前 $y$ 的左子节点（若存在）的父节点为 $y$，$y$ 的父节点为 $x$，以及 $x$ 的父节点为 $z$；
4.  自下而上维护节点信息．

???+ example "实现"
    ```cpp
    --8<-- "docs/ds/code/splay/splay-1.cpp:rotate"
    ```

在所有函数的实现时，都应注意不要修改节点 $0$ 的信息．

### 伸展操作

Splay 树要求每访问一个节点 $x$ 后都要强制将其旋转到根节点．该操作也称为伸展操作．

设刚访问的节点为 $x$．要做伸展操作，就是要对 $x$ 做一系列的 **伸展步骤**．每次对 $x$ 做一次伸展步骤，$x$ 到根节点的距离都会更近．定义 $p$ 为 $x$ 的父节点．伸展步骤有三种：

1.  **zig**: 在 $p$ 是根节点时操作．Splay 树会根据 $x$ 和 $p$ 间的边旋转．**zig** 存在是用于处理奇偶校验问题，仅当 $x$ 在伸展操作开始时具有奇数深度时作为伸展操作的最后一步执行．

    ![splay-zig](./images/splay-zig.svg)

    即直接将 $x$ 右旋或左旋（图 1, 2）．

    ![图 1](./images/splay-rotate1.svg)![图 2](./images/splay-rotate2.svg)

2.  **zig-zig**: 在 $p$ 不是根节点且 $x$ 和 $p$ 都是右侧子节点或都是左侧子节点时操作．下方例图显示了 $x$ 和 $p$ 都是左侧子节点时的情况．Splay 树首先按照连接 $p$ 与其父节点 $g$ 边旋转，然后按照连接 $x$ 和 $p$ 的边旋转．

    ![splay-zig-zig](./images/splay-zig-zig.svg)

    即首先将 $p$ 右旋或左旋，然后将 $x$ 右旋或左旋（图 3, 4）．

    ![图 3](./images/splay-rotate3.svg)![图 4](./images/splay-rotate4.svg)

3.  **zig-zag**: 在 $p$ 不是根节点且 $x$ 和 $p$ 一个是右侧子节点一个是左侧子节点时操作．Splay 树首先按 $p$ 和 $x$ 之间的边旋转，然后按 $x$ 和 $g$ 新生成的结果边旋转．

    ![splay-zig-zag](./images/splay-zig-zag.svg)

    即将 $x$ 先左旋再右旋或先右旋再左旋（图 5, 6）．

    ![图 5](./images/splay-rotate5.svg)![图 6](./images/splay-rotate6.svg)

???+ tip "Tip"
    请读者尝试自行模拟 $6$ 种旋转情况，以理解伸展操作的基本思想．

比较三种伸展步骤可知，要区分此时应使用哪种操作，关键是要判断 $x$ 是否是根节点的子节点，以及 $x$ 和它父节点是否在各自的父节点同侧．

此处提供的实现，可以指定任意根节点 $z$，并将它的子树内任意节点 $x$ 上移至 $z$ 处：

1.  首先记录根节点 $z$ 的父节点 $w$，从而可以利用 `fa[x] == w` 判断 $x$ 已经位于根结点处；
2.  记录 $x$ 当前的父节点 $y$，如果 $y$ 和 $w$ 相同，说明 $x$ 已经到达根节点；
3.  否则，利用 `fa[y] == w` 判断 $y$ 是否是根节点．如果是，直接做 zig 操作将 $x$ 旋转；如果不是，利用 `dir(x) == dir(y)` 判断使用 zig-zig 还是 zig-zag，前者先旋转 $y$ 再旋转 $x$，后者直接旋转两次 $x$．

???+ example "实现"
    ```cpp
    --8<-- "docs/ds/code/splay/splay-1.cpp:splay"
    ```

伸展操作是 Splay 树的核心操作，也是它的时间复杂度能够得到保证的关键步骤．请务必保证每次向下访问节点后，都进行一次伸展操作．

另外，伸展操作会将当前节点 $x$ 到根节点 $z$ 的路径上的所有节点信息自下而上地更新一遍．正是因为这一点，才可以修改非根节点，再通过伸展操作将它上移至根来完成整个树的信息更新．

### 时间复杂度

对大小为 $n$ 的 Splay 树做 $m$ 次伸展操作的复杂度是 $O((n+m)\log n)$ 的，单次均摊复杂度是 $O(\log n)$ 的．

??? note "基于势能分析的复杂度证明"
    为此只需分析 **zig**、**zig-zig** 和 **zig-zag** 三种操作的复杂度．为此，我们采用 **势能分析法**，通过研究势能的变化来推导操作的均摊复杂度．假设对一棵包含 $n$ 个节点的 Splay 树进行了 $m$ 次伸展操作，可以通过如下方式进行分析：
    
    **定义**：
    
    1.  **单个节点的势能**：$w(x) = \log(\text{size}(x))$，其中 $\text{size}(x)$ 表示以节点 $x$ 为根的子树大小．
    2.  **整棵树的势能**：$\varphi = \sum w(x)$，即树中所有节点势能的总和，初始势能满足 $\varphi_0 \leq n \log n$．
    3.  **第 $i$ 次操作的均摊成本**：$c_i = t_i + \varphi_i - \varphi_{i-1}$，其中 $t_i$ 为实际操作代价，$\varphi_i$ 和 $\varphi_{i-1}$ 分别为操作后和操作前的势能．
    
    **性质**：
    
    1.  如果 $p$ 是 $x$ 的父节点，则有 $w(p) \geq w(x)$，即父节点的势能不小于子节点的势能．
    
    2.  由于根节点的子树大小在操作前后保持不变，因此根节点的势能在操作过程中不变．
    
    3.  如果 $\text{size}(p)\ge\text{size}(x)+\text{size}(y)$，那么有 $2w(p) - w(x) - w(y) \geq 2$．
    
    ??? note "性质 3 的证明"
        根据均值不等式可知
        
        $$
        \begin{aligned}
        2w(p) - w(x) - w(y) 
        &= \log\dfrac{\text{size}(p)^2}{\text{size}(x)\cdot\text{size}(y)} \\
        &> \log\dfrac{\left(\text{size}(x)+\text{size}(y)\right)^2}{\text{size}(x)\cdot\text{size}(y)} \\
        &\ge \log 4 \\
        &= 2.
        \end{aligned}
        $$
    
    接下来，分别对 **zig**、**zig-zig** 和 **zig-zag** 操作进行势能分析．设操作前后的节点 $x$ 的势能分别是 $w(x)$ 和 $w'(x)$．节点的记号与 [上文](#伸展操作) 一致．
    
    **zig**：根据性质 1 和 2，有 $w(p) = w'(x)$，且 $w'(x) \geq w'(p)$．由此，均摊成本为
    
    $$
    \begin{aligned}
    c_i &= 1 + w'(x) + w'(p) - w(x) - w(p)\\
    &= 1 + w'(p) - w(x)\\
    &\leq 1 + w'(x) - w(x).
    \end{aligned}
    $$
    
    **zig-zig**：根据性质 1 和 2，有 $w(g) = w'(x)$，且 $w'(x) \geq w'(p)$，$w(x) \leq w(p)$．因为
    
    $$
    \begin{aligned}
    \text{size}'(x) 
    &= 3 + \text{size}(A) + \text{size}(B) + \text{size}(C) + \text{size}(D) \\
    &> (1 + \text{size}(A) + \text{size}(B)) + (1 + \text{size}(C) + \text{size}(D)) \\
    &= \text{size}(x) + \text{size}'(g),
    \end{aligned}
    $$
    
    根据性质 3 可得
    
    $$
    2 w'(x) - w(x) - w'(g) \geq 2.
    $$
    
    由此，均摊成本为
    
    $$
    \begin{aligned}
    c_i &= 2 + w'(x) + w'(p) + w'(g) - w(x) - w(p) - w(g) \\
    &= 2 + w'(p) + w'(g) - w(x) - w(p) \\
    &\le (2 w'(x) - w(x) - w'(g)) + w'(p) + w'(g) - w(x) - w(p) \\
    &= 2(w'(x)-w(x)) + w'(p) - w(p) \\
    &\le 3(w'(x)-w(x)).
    \end{aligned}
    $$
    
    **zig-zag**：根据性质 1 和 2，有 $w(g) = w'(x)$，且 $w(p) \geq w(x)$．因为 $\text{size}'(x)>\text{size}'(p)+\text{size}'(g)$，根据性质 3，可得
    
    $$
    2 \cdot w'(x) - w'(g) - w'(p) \geq 2.
    $$
    
    由此，均摊成本为
    
    $$
    \begin{aligned}
    c_i &= 2 + w'(x) + w'(p) + w'(g) - w(x) - w(p) - w(g) \\
    &= 2 + w'(p) + w'(g) - w(x) - w(p) \\
    &\le (2w'(x) - w'(g) - w'(p)) + w'(p) + w'(g) - w(x) - w(p) \\
    &= 2w'(x) - w(x) - w(p) \\
    &\le 2(w'(x) - w(x)).
    \end{aligned}
    $$
    
    **单次伸展操作**：
    
    令 $w^{(n)}(x)=(w^{(n-1)})'(x)$ 且 $w^{(0)}(x)=w(x)$．假设一次伸展操作依次访问了 $x_{1}, x_{2}, \cdots, x_{n}$ 等节点，最终 $x_{1}$ 成为根节点．这必然经过若干次 **zig-zig** 和 **zig-zag** 操作和至多一次 **zig** 操作，前两种操作的均摊成本均不超过 $3(w'(x)-w(x))$，而最后一次操作的均摊成本不超过 $3(w'(x) - w(x))+1$，所以总的均摊成本不超过
    
    $$
    3(w^{(n)}(x_1) - w^{(0)}(x_1)) + 1 \le 3\log n + 1.
    $$
    
    因此，一次伸展操作的均摊复杂度是 $O(\log n)$ 的．从而，基于伸展的插入、查询、删除等操作的时间复杂度也为均摊 $O(\log n)$．
    
    **结论**：
    
    在进行 $m$ 次伸展操作之后，实际成本
    
    $$
    \begin{aligned}
    \sum_{i=1}^m t_i &= \sum_{i=1}^m \left(c_i + \varphi_{i-1} - \varphi_i \right) \\
    &= \sum_{i=1}^m c_i + \varphi_0 - \varphi_m \\
    &\le m(3\log n+1) + n\log n.
    \end{aligned}
    $$
    
    因此，$m$ 次伸展操作的实际时间复杂度为 $O((m+n)\log n)$．

??? info "为什么 Splay 树的再平衡操作可以获得 $O(\log n)$ 的均摊复杂度？"
    朴素的再平衡思路就是对节点反复进行旋转操作使其上升，直到它成为根节点．这种朴素思路的问题在于，对于所有子节点都是左（右）节点的链状树来说，它相当于反复进行 **zig** 操作，因而 **zig** 操作的均摊复杂度中的常数项 $1$ 会不断累积，造成最终的均摊复杂度达到 $O(\log n+n)$ 级别．Splay 树的再平衡操作的设计，避免了连续 **zig** 的情形中的常数累积，使得一次完整的伸展操作中，至多进行一次单独的 **zig** 操作，从而优化了时间复杂度．

## 平衡树操作

本节讨论基于 Splay 树实现平衡树的常见操作的方法．其中，较为重要的是按照值或排名查找元素，它们可以将某个特定的元素找到，并上移至根节点处，以便后续处理．

作为例子，本节将讨论模板题目 [普通平衡树](https://loj.ac/problem/104) 的实现．

### 按照值查找

作为二叉查找树，可以通过值 $v$ 查找到相应的节点，只需要将待查找的值 $v$ 和当前节点的值比较即可，找到后将该元素上移至根部即可．

应注意，经常存在树中不存在相应的节点的情形．对于这种情形，要记录最后一个访问的节点（即实现中的 $y$），并将 $y$ 上移至根部．此时，节点 $y$ 存储的值必然要么是所有小于 $v$ 的元素中最大的（即 $v$ 的前驱），要么是所有大于 $v$ 的元素中最小的（即 $v$ 的后继）．这是因为查找过程保证，左子树总是存储小于 $v$ 的值，而右子树总是存储大于 $v$ 的值．

???+ example "实现"
    ```cpp
    --8<-- "docs/ds/code/splay/splay-1.cpp:find"
    ```

该实现允许指定任何节点 $z$ 作为根节点，并在它的子树内按值查找．

### 按照排名访问

因为记录了子树大小信息，所以 Splay 树还可以通过排名访问元素，即查找树中第 $k$ 小的元素．

设 $k$ 为剩余排名，具体步骤如下：

-   如果左子树非空且剩余排名 $k$ 不大于左子树的大小，那么向左子树查找；
-   否则，如果 $k$ 不大于左子树加上根的大小，那么根节点就是要寻找的；
-   否则，将 $k$ 减去左子树的和根的大小，继续向右子树查找；
-   将最终找到的元素上移至根部．

???+ example "实现"
    ```cpp
    --8<-- "docs/ds/code/splay/splay-1.cpp:loc"
    ```

该实现需要保证排名 $k$ 不超过根 $z$ 处的树大小．

模板题目中操作 $4$ 要求按照排名返回值，直接调用该方法，并返回值即可．

???+ example "实现"
    ```cpp
    --8<-- "docs/ds/code/splay/splay-1.cpp:find-kth"
    ```

### 合并操作

有些时候需要合并两棵 Splay 树．

设两棵树的根节点分别为 $x$ 和 $y$，那么为了保证结果仍是二叉查找树，需要要求 $x$ 树中的最大值小于 $y$ 树中的最小值．这条件通常都可以满足，因为两棵树往往是从更大的子树中分裂出的．

合并操作如下：

-   如果 $x$ 和 $y$ 其中之一或两者都为空树，直接返回不为空的那一棵树的根节点或空树；
-   否则，通过 `loc(y, 1)` 将 $y$ 树中的最小值上移至根 $y$ 处，再将它的左节点（此时必然为空）设置为 $x$，并更新节点信息，返回节点 $y$．

???+ example "实现"
    ```cpp
    --8<-- "docs/ds/code/splay/splay-1.cpp:merge"
    ```

分裂操作类似．因而，Splay 树可以模拟 [无旋 treap](./treap.md#无旋-treap) 的思路做各种操作，包括区间操作．[后文](#序列操作) 会介绍更具有 Splay 树风格的区间操作处理方法．

### 插入操作

插入操作是一个比较复杂的过程．具体步骤如下：（假设插入的值为 $v$）

-   类似按值查找的过程，根据 $v$ 向下查找到存储 $v$ 的节点或者空节点，过程中记录父节点 $y$；
-   如果存在存储 $v$ 的节点 $x$，直接更新信息，否则就新建节点 $x$；
-   做伸展操作，将最后一个节点 $x$ 上移至根部．

???+ example "实现"
    ```cpp
    --8<-- "docs/ds/code/splay/splay-1.cpp:insert"
    ```

该实现允许直接向空树内插入值．若不想处理空树，可以在树中提前插入哑节点．

### 删除操作

删除操作也是一个比较复杂的操作．具体步骤如下：（假设删除的值为 $v$）

-   首先按照值 $v$ 查找存储它的节点，并上移至根部；
-   如果不存在存储它的节点，直接返回；（上一步已经做了伸展操作）
-   否则，更新节点信息；
-   如果得到的根节点为空节点，就合并左右子树作为新的根节点，注意合并前需要更新两个子树的根的父节点为空．

???+ example "实现"
    ```cpp
    --8<-- "docs/ds/code/splay/splay-1.cpp:remove"
    ```

### 查询排名

直接按照值 $v$ 访问节点（并上移至根），然后返回相应的值即可．

注意，当 $v$ 不存在时，方法 `find(rt, v)` 返回的根和 $v$ 的大小关系无法确定，需要单独讨论．

???+ example "实现"
    ```cpp
    --8<-- "docs/ds/code/splay/splay-1.cpp:find-rank"
    ```

### 查询前驱

前驱定义为小于 $v$ 的最大的数．具体步骤如下：

-   按照值 $v$ 访问节点（并上移至根部）；
-   如果根部的值小于 $v$，那么它必然是最大的那个，直接返回；
-   否则，在左子树中找到最大值，并上移至根部．

最后一步相当于直接调用 `loc(ch[rt][0], sz[ch[rt][0]])`，只是省去了不必要的判断．

???+ example "实现"
    ```cpp
    --8<-- "docs/ds/code/splay/splay-1.cpp:find-prev"
    ```

该实现允许前驱不存在，此时返回 $-1$．

### 查询后继

后继定义为大于 $x$ 的最小的数．查询方法和前驱类似，只是将左子树的最大值换成了右子树的最小值，即调用 `loc(ch[rt][1], 1)`．

???+ example "实现"
    ```cpp
    --8<-- "docs/ds/code/splay/splay-1.cpp:find-next"
    ```

### 参考实现

本节的最后，给出模板题目 [普通平衡树](https://loj.ac/problem/104) 的参考实现．

??? example "参考实现"
    ```cpp
    --8<-- "docs/ds/code/splay/splay-1.cpp:full-text"
    ```

## 序列操作

Splay 树也可以运用在序列上，用于维护区间信息．与线段树对比，Splay 树常数较大，但是支持更复杂的序列操作，如区间翻转等．上文提到 Splay 树同样支持分裂和合并操作，因而可以模拟 [无旋 treap](./treap.md#无旋-treap) 进行区间操作，在此不再过多讨论．本节主要讨论基于伸展操作的区间操作实现方法．

将序列建成的 Splay 树有如下性质：

-   Splay 树的中序遍历相当于原序列从左到右的遍历；
-   Splay 树上的一个节点代表原序列的一个元素；
-   Splay 树上的一颗子树，代表原序列的一段区间．

因为有伸展操作，可以快速提取出代表某个区间的 Splay 子树．

作为例子，本节将讨论模板题目 [文艺平衡树](https://loj.ac/problem/105) 的实现．

### 根据序列建树

在操作之前，需要根据所给的序列先把 Splay 树建出来．根据 Splay 树的特性，直接建出一颗只有左儿子的链即可．时间复杂度是 $O(n)$ 的．

???+ example "参考实现"
    ```cpp
    --8<-- "docs/ds/code/splay/splay-2.cpp:build"
    ```

最后的伸展操作自下而上地更新了节点信息．为了后文区间操作方便，序列左右两侧添加了两个哨兵节点．

### 区间翻转

以区间翻转为例，可以理解区间操作的方法：（设区间为 $[L,R]$）

-   首先将节点 $L-1$ 上移到根节点，再在其右子树中，将节点 $R+1$ 上移到右子树的根节点；
-   此时，设 $x$ 为根节点的右子节点的左子节点，则以 $x$ 为根的子树就对应着区间 $[L,R]$；
-   在 $x$ 处对区间 $[L,R]$ 做操作，并打上懒标记；
-   在 $x$ 处将标记下传一次，然后利用伸展操作将 $x$ 上移到根．

第一步需要的操作就是前文平衡树操作中的「按照排名访问」，因为元素的标号就是它的排名．因为涉及懒标记的管理，它的实现与上文略有不同．

???+ example "参考实现"
    ```cpp
    --8<-- "docs/ds/code/splay/splay-2.cpp:reverse"
    ```

最后一步的伸展操作并非为了保证复杂度正确，而是为了更新节点信息．因为伸展操作涉及到节点 $x$ 的左右子节点，所以之前需要将节点 $x$ 处的标记先下传一次．当然，仅对于区间翻转操作而言，子区间的翻转不会对祖先节点产生影响，所以省去这一步骤也是正确的．此处实现保留这两行，是为了说明一般的情形下的操作方法．

### 懒标记管理

首先，需要辅助函数 `lazy_reverse(x)` 和 `push_down(x)`．前者交换左右节点，并更新懒标记；后者将标记下传．

???+ example "参考实现"
    ```cpp
    --8<-- "docs/ds/code/splay/splay-2.cpp:push-down"
    ```

然后，只需要在向下经过节点时下传标记即可．模板题要求的操作比较简单，只有按照排名寻找的操作（即 `loc`）涉及向下访问节点．注意，需要在函数每次访问一个新的节点 **前** 下传标记．

???+ example "参考实现"
    ```cpp
    --8<-- "docs/ds/code/splay/splay-2.cpp:push-down-lazy"
    ```

因为向下访问节点时已经移除了经过的路径的所有懒标记，所以利用伸展操作上移节点时不再需要处理懒标记．但是，对于区间操作的那一个节点要谨慎处理：因为它同样位于伸展操作的路径上，但是刚刚操作完，可能存在尚未下传的标记，需要首先下传再做伸展操作，正如同上文所做的那样．

### 参考实现

本节的最后，给出模板题目 [文艺平衡树](https://loj.ac/problem/105) 的参考实现．

??? example "参考实现"
    ```cpp
    --8<-- "docs/ds/code/splay/splay-2.cpp:full-text"
    ```

## 习题

这些题目都是裸的 Splay 树维护二叉查找树：

-   [【模板】普通平衡树](https://loj.ac/problem/104)
-   [【模板】文艺平衡树](https://loj.ac/problem/105)
-   [「HNOI2002」营业额统计](https://loj.ac/problem/10143)
-   [「HNOI2004」宠物收养所](https://loj.ac/problem/10144)

Splay 树还出现在更复杂的应用场景中：

-   [「Cerc2007」robotic sort 机械排序](https://www.luogu.com.cn/problem/P4402)
-   [「HNOI2011」括号修复/「JSOI2011」括号序列](https://www.luogu.com.cn/problem/P3215)
-   [二逼平衡树（树套树）](https://loj.ac/problem/106)
-   [BZOJ 2827 千山鸟飞绝](https://hydro.ac/p/bzoj-P2827)
-   [「Lydsy1706 月赛」K 小值查询](https://hydro.ac/p/bzoj-P4923)
-   [POJ3580 SuperMemo](http://poj.org/problem?id=3580)

## 参考资料与注释

本文部分内容引用于 algocode 算法博客，特别鸣谢！


## ds/sqrt-tree.md

## 引入

给你一个长度为 n 的序列 ${\left\langle a_i\right\rangle}_{i=1}^n$，再给你一个满足结合律的运算 $\circ$（比如 $\gcd,\min,\max,+,\operatorname{and},\operatorname{or},\operatorname{xor}$ 均满足结合律），然后对于每一次区间询问 $[l,r]$，我们需要计算 $a_l\circ a_{l+1}\circ\dotsb\circ a_{r}$．

Sqrt Tree 可以在 $O(n\log\log n)$ 的时间内预处理，并在 $O(1)$ 的时间内回答询问．

## 解释

### 序列分块

首先我们把整个序列分成 $O(\sqrt{n})$ 个块，每一块的大小为 $O(\sqrt{n})$．对于每个块，我们计算：

1.  $P_i$ 块内的前缀区间询问
2.  $S_i$ 块内的后缀区间询问
3.  维护一个额外的数组 $\left\langle B_{i,j}\right\rangle$ 表示第 $i$ 个块到第 $j$ 个块的区间答案．

举个例子，假设 $\circ$ 代表加法运算 $+$，序列为 $\{1,2,3,4,5,6,7,8,9\}$．

首先我们将序列分成三块，变成了 $\{1,2,3\},\{4,5,6\},\{7,8,9\}$．

那么每一块的前缀区间答案和后缀区间答案分别为

$$
\begin{aligned}
&P_1=\{1,3,6\},S_1=\{6,5,3\}\\
&P_2=\{4,9,15\},S_2=\{15,11,6\}\\
&P_3=\{7,15,24\},S_3=\{24,17,9\}\\
\end{aligned}
$$

$B$ 数组为：

$$
B=\begin{bmatrix}
6 & 21 & 45\\
0 & 15 & 39\\
0 & 0 & 24\\
\end{bmatrix}
$$

（对于 $i>j$ 的不合法的情况我们假设答案为 0）

显然我们可以在 $O(n)$ 的时间内预处理这些值，空间复杂度同样是 $O(n)$ 的．处理好之后，我们可以利用它们在 $O(1)$ 的时间内回答一些跨块的询问．但对于那些整个区间都在一个块内的询问我们仍不能处理，因此我们还需要处理一些东西．

### 构建一棵树

容易想到我们在每个块内递归地构造上述结构以支持块内的查询．对于大小为 $1$ 的块我们可以 $O(1)$ 地回答询问．这样我们就建出了一棵树，每一个结点代表序列的一个区间．叶子结点的区间长度为 $1$ 或 $2$．一个大小为 $k$ 的结点有 $O(\sqrt{k})$ 个子节点，于是整棵树的高度是 $O(\log\log n)$ 的，每一层的区间总长是 $O(n)$ 的，因此我们构建这棵树的复杂度是 $O(n\log\log n)$ 的．

??? note "树高度的证明"
    根据定义，设「控制」$n$ 个元素的结点的子树高度为 $T(n)$，可以写出递归式：
    
    $$
    T(n)=T(\sqrt n)+1
    $$
    
    作换元 $n=2^m$ 得
    
    $$
    T(2^m)=T(2^{\frac m2})+1
    $$
    
    再定义 $S(m)=T(2^m)$，代入有
    
    $$
    S(m)=S(\dfrac m2)+1
    $$
    
    根据主定理，可知 $S(m)=O(\log m)$，因此 $T(n)=S(\log n)=O(\log\log n)$.

现在我们可以在 $O(\log\log n)$ 的时间内回答询问．对于询问 $[l,r]$，我们只需要快速找到一个区间长度最小的结点 $u$ 使得 $u$ 能包含 $[l,r]$，这样 $[l,r]$ 在 $u$ 的分块区间中一定是跨块的，就可以 $O(1)$ 地计算答案了．查询一次的总体复杂度是 $O(\log\log n)$，因为树高是 $O(\log\log n)$ 的．不过我们仍可以优化这个过程．

### 优化询问复杂度

容易想到二分高度，然后可以 $O(1)$ 判断是否合法．这样复杂度就变成了 $O(\log\log\log n)$．不过我们仍可以进一步加速这一过程．

我们假设

1.  每一块的大小都是 $2$ 的整数幂次；
2.  每一层上的块大小是相同的．

为此我们需要在序列的末位补充一些 $0$ 元素，使得它的长度变成 $2$ 的整数次幂．尽管有些块可能会变成原来的两倍大小，但这样仍是 $O(\sqrt{k})$ 的，于是预处理分块的复杂度仍是 $O(n)$ 的．

现在我们可以轻松地确定一个询问区间是否被整个地包含在一个块中．对于区间 $[l,r]$（以 0 为起点），我们把端点写为二进制形式．举一个例子，对于 $k=4, l=39, r=46$，二进制表示为

$$
l = 39_{10} = 100111_2,
r = 46_{10} = 101110_2
$$

我们知道每一层的区间长度是相同的，而分块的大小也是相同的（在上述示例中 $2^k=2^4=16$）．这些块完全覆盖了整个序列，因此第一块代表的元素为 $[0,15]$（二进制表示为 $[000000_2,001111_2]$），第二个块代表的元素区间为 $[16,31]$（二进制表示为 $[010000_2,011111_2]$），以此类推．我们发现这些在同一个块内的元素的位置在二进制上只有后 $k$ 位不同（上述示例中 $k=4$）．而示例的 $l,r$ 也只有后 $k$ 位不同，因此他们在同一个块中．

因此我们需要检查区间两个端点是否只有后 $k$ 位不同，即 $l\oplus r\le 2^k-1$．因此我们可以快速找到答案区间所在的层：

1.  对于每个 $i\in [1,n]$，我们找到 $i$ 最高位上的 $1$；
2.  现在对于一个询问 $[l,r]$，我们计算 $l\oplus r$ 的最高位，这样就可以快速确定答案区间所在的层．

这样我们就可以在 $O(1)$ 的时间内回答询问啦．

## 更新元素的过程

我们可以在 Sqrt Tree 上更新元素，单点修改和区间修改都是支持的．

### 单点修改

考虑一次单点赋值操作 $a_x=val$，我们希望高效更新这个操作的信息．

#### 朴素实现

首先我们来看看在做了一次单点修改后 Sqrt Tree 会变成什么样子．

考虑一个长度为 $l$ 的结点以及对应的序列：$\left\langle P_i\right\rangle,\left\langle S_i\right\rangle,\left\langle B_{i,j}\right\rangle$．容易发现在 $\left\langle P_i\right\rangle$ 和 $\left\langle S_i \right\rangle$ 中都只有 $O(\sqrt{l})$ 个元素改变．而在 $\left\langle B_{i,j}\right\rangle$ 中则有 $O(l)$ 个元素被改变．因此有 $O(l)$ 个元素在树上被更新．因此在 Sqrt Tree 上单点修改的复杂度是 $O(n+\sqrt{n}+\sqrt{\sqrt{n}}+\dotsb)=O(n)$．

#### 使用 Sqrt Tree 替代 B 数组

注意到单点更新的瓶颈在于更新根结点的 $\left\langle B_{i,j}\right\rangle$．因此我们尝试用另一个 Sqrt Tree 代替根结点的 $\left\langle B_{i,j}\right\rangle$，称其为 $index$．它的作用和原来的二维数组一样，维护整段询问的答案．其他非根结点仍然使用 $\left\langle B_{i,j}\right\rangle$ 维护．注意，如果一个 Sqrt Tree 根结点有 $index$ 结构，称其 Sqrt Tree 是 **含有索引** 的；如果一个 Sqrt Tree 的根结点有 $\left\langle B_{i,j}\right\rangle$ 结构，称其是 **没有索引** 的．而 $index$ 这棵树本身是没有索引的．

因此我们可以这样更新 $index$ 树：

1.  在 $O(\sqrt{n})$ 的时间内更新 $\left\langle P_i\right\rangle$ 和 $\left\langle S_i\right\rangle$．
2.  更新 $index$，它的长度是 $O(n)$ 的，但我们只需要更新其中的一个元素（这个元素代表了被改变的块），这一步的时间复杂度是 $O(\sqrt{n})$ 的（使用朴素实现的算法）．
3.  进入产生变化的子节点并使用朴素实现的算法在 $O(\sqrt{n})$ 的时间内更新信息．

注意，查询的复杂度仍是 $O(1)$ 的，因为我们最多使用 $index$ 树一次．于是单点修改的复杂度就是 $O(\sqrt{n})$ 的．

### 更新一个区间

Sqrt Tree 也支持区间覆盖操作 $\operatorname{Update}(l,r,x)$，即把区间 $[l,r]$ 的数全部变成 $x$．对此我们有两种实现方式，其中一种会花费 $O(\sqrt{n}\log\log n)$ 的复杂度更新信息，$O(1)$ 的时间查询；另一种则是 $O(\sqrt{n})$ 更新信息，但查询的时间会增加到 $O(\log\log n)$．

我们可以像线段树一样在 Sqrt Tree 上打懒标记．但是在 Sqrt Tree 上有一点不同．因为下传一个结点的懒标记，复杂度可能达到 $O(\sqrt{n})$，因此我们不是在询问的时候下传标记，而是看父节点是否有标记，如果有标记就把它下传．

#### 第一种实现

在第一种实现中，我们只会给第 $1$ 层的结点（结点区间长度为 $O(\sqrt{n})$）打懒标记，在下传标记的时候直接更新整个子树，复杂度为 $O(\sqrt{n}\log\log n)$．操作过程如下：

1.  考虑第 $1$ 层上的结点，对于那些被修改区间完全包含的结点，给他们打一个懒标记；

2.  有两个块只有部分区间被覆盖，我们直接在 $O(\sqrt{n}\log\log n)$ 的时间内 **重建** 这两个块．如果它本身带有之前修改的懒标记，就在重建的时候顺便下传标记；

3.  更新根结点的 $\left\langle P_i\right\rangle$ 和 $\left\langle S_i\right\rangle$，时间复杂度 $O(\sqrt{n})$；

4.  重建 $index$ 树，时间复杂度 $O(\sqrt{n}\log\log n)$．

现在我们可以高效完成区间修改了．那么如何利用懒标记回答询问？操作如下：

1.  如果我们的询问被包含在一个有懒标记的块内，可以利用懒标记计算答案；

2.  如果我们的询问包含多个块，那么我们只需要关心最左边和最右边不完整块的答案．中间的块的答案可以在 $index$ 树中查询（因为 $index$ 树在每次修改完后会重建），复杂度是 $O(1)$．

因此询问的复杂度仍为 $O(1)$．

#### 第二种实现

在这种实现中，每一个结点都可以被打上懒标记．因此在处理一个询问的时候，我们需要考虑祖先中的懒标记，那么查询的复杂度将变成 $O(\log\log n)$．不过更新信息的复杂度就会变得更快．操作如下：

1.  被修改区间完全包含的块，我们把懒标记添加到这些块上，复杂度 $O(\sqrt{n})$；
2.  被修改区间部分覆盖的块，更新 $\left\langle P_i\right\rangle$ 和 $\left\langle S_i\right\rangle$，复杂度 $O(\sqrt{n})$（因为只有两个被修改的块）；
3.  更新 $index$ 树，复杂度 $O(\sqrt{n})$（使用同样的更新算法）；
4.  对于没有索引的子树更新他们的 $\left\langle B_{i,j}\right\rangle$；
5.  递归地更新两个没有被完全覆盖的区间．

时间复杂度是 $O(\sqrt{n}+\sqrt{\sqrt{n}}+\dotsb)=O(\sqrt{n})$．

## 实现

下面的实现在 $O(n\log\log n)$ 的时间内建树，在 $O(1)$ 的时间内回答询问，在 $O(\sqrt{n})$ 的时间内单点修改．

```cpp
SqrtTreeItem op(const SqrtTreeItem &a, const SqrtTreeItem &b);

int log2Up(int n) {
  int res = 0;
  while ((1 << res) < n) {
    res++;
  }
  return res;
}

class SqrtTree {
 private:
  int n, lg, indexSz;
  vector<SqrtTreeItem> v;
  vector<int> clz, layers, onLayer;
  vector<vector<SqrtTreeItem>> pref, suf, between;

  void buildBlock(int layer, int l, int r) {
    pref[layer][l] = v[l];
    for (int i = l + 1; i < r; i++) {
      pref[layer][i] = op(pref[layer][i - 1], v[i]);
    }
    suf[layer][r - 1] = v[r - 1];
    for (int i = r - 2; i >= l; i--) {
      suf[layer][i] = op(v[i], suf[layer][i + 1]);
    }
  }

  void buildBetween(int layer, int lBound, int rBound, int betweenOffs) {
    int bSzLog = (layers[layer] + 1) >> 1;
    int bCntLog = layers[layer] >> 1;
    int bSz = 1 << bSzLog;
    int bCnt = (rBound - lBound + bSz - 1) >> bSzLog;
    for (int i = 0; i < bCnt; i++) {
      SqrtTreeItem ans;
      for (int j = i; j < bCnt; j++) {
        SqrtTreeItem add = suf[layer][lBound + (j << bSzLog)];
        ans = (i == j) ? add : op(ans, add);
        between[layer - 1][betweenOffs + lBound + (i << bCntLog) + j] = ans;
      }
    }
  }

  void buildBetweenZero() {
    int bSzLog = (lg + 1) >> 1;
    for (int i = 0; i < indexSz; i++) {
      v[n + i] = suf[0][i << bSzLog];
    }
    build(1, n, n + indexSz, (1 << lg) - n);
  }

  void updateBetweenZero(int bid) {
    int bSzLog = (lg + 1) >> 1;
    v[n + bid] = suf[0][bid << bSzLog];
    update(1, n, n + indexSz, (1 << lg) - n, n + bid);
  }

  void build(int layer, int lBound, int rBound, int betweenOffs) {
    if (layer >= (int)layers.size()) {
      return;
    }
    int bSz = 1 << ((layers[layer] + 1) >> 1);
    for (int l = lBound; l < rBound; l += bSz) {
      int r = min(l + bSz, rBound);
      buildBlock(layer, l, r);
      build(layer + 1, l, r, betweenOffs);
    }
    if (layer == 0) {
      buildBetweenZero();
    } else {
      buildBetween(layer, lBound, rBound, betweenOffs);
    }
  }

  void update(int layer, int lBound, int rBound, int betweenOffs, int x) {
    if (layer >= (int)layers.size()) {
      return;
    }
    int bSzLog = (layers[layer] + 1) >> 1;
    int bSz = 1 << bSzLog;
    int blockIdx = (x - lBound) >> bSzLog;
    int l = lBound + (blockIdx << bSzLog);
    int r = min(l + bSz, rBound);
    buildBlock(layer, l, r);
    if (layer == 0) {
      updateBetweenZero(blockIdx);
    } else {
      buildBetween(layer, lBound, rBound, betweenOffs);
    }
    update(layer + 1, l, r, betweenOffs, x);
  }

  SqrtTreeItem query(int l, int r, int betweenOffs, int base) {
    if (l == r) {
      return v[l];
    }
    if (l + 1 == r) {
      return op(v[l], v[r]);
    }
    int layer = onLayer[clz[(l - base) ^ (r - base)]];
    int bSzLog = (layers[layer] + 1) >> 1;
    int bCntLog = layers[layer] >> 1;
    int lBound = (((l - base) >> layers[layer]) << layers[layer]) + base;
    int lBlock = ((l - lBound) >> bSzLog) + 1;
    int rBlock = ((r - lBound) >> bSzLog) - 1;
    SqrtTreeItem ans = suf[layer][l];
    if (lBlock <= rBlock) {
      SqrtTreeItem add =
          (layer == 0) ? (query(n + lBlock, n + rBlock, (1 << lg) - n, n))
                       : (between[layer - 1][betweenOffs + lBound +
                                             (lBlock << bCntLog) + rBlock]);
      ans = op(ans, add);
    }
    ans = op(ans, pref[layer][r]);
    return ans;
  }

 public:
  SqrtTreeItem query(int l, int r) { return query(l, r, 0, 0); }

  void update(int x, const SqrtTreeItem &item) {
    v[x] = item;
    update(0, 0, n, 0, x);
  }

  SqrtTree(const vector<SqrtTreeItem> &a)
      : n((int)a.size()), lg(log2Up(n)), v(a), clz(1 << lg), onLayer(lg + 1) {
    clz[0] = 0;
    for (int i = 1; i < (int)clz.size(); i++) {
      clz[i] = clz[i >> 1] + 1;
    }
    int tlg = lg;
    while (tlg > 1) {
      onLayer[tlg] = (int)layers.size();
      layers.push_back(tlg);
      tlg = (tlg + 1) >> 1;
    }
    for (int i = lg - 1; i >= 0; i--) {
      onLayer[i] = max(onLayer[i], onLayer[i + 1]);
    }
    int betweenLayers = max(0, (int)layers.size() - 1);
    int bSzLog = (lg + 1) >> 1;
    int bSz = 1 << bSzLog;
    indexSz = (n + bSz - 1) >> bSzLog;
    v.resize(n + indexSz);
    pref.assign(layers.size(), vector<SqrtTreeItem>(n + indexSz));
    suf.assign(layers.size(), vector<SqrtTreeItem>(n + indexSz));
    between.assign(betweenLayers, vector<SqrtTreeItem>((1 << lg) + bSz));
    build(0, 0, n, 0);
  }
};
```

## 习题

[CodeChef - SEGPROD](https://www.codechef.com/NOV17/problems/SEGPROD)

**本页面主要译自 [Sqrt Tree - Algorithms for Competitive Programming](https://cp-algorithms.com/data_structures/sqrt-tree.html)，版权协议为 CC-BY-SA 4.0．**


## ds/stack.md

## 引入

![](./images/stack.svg)

栈是 OI 中常用的一种线性数据结构．请注意，本文主要讲的是栈这种数据结构，而非程序运行时的系统栈/栈空间．

栈的修改与访问是按照后进先出的原则进行的，因此栈通常被称为是后进先出（last in first out）表，简称 LIFO 表．

??? warning "Warning"
    LIFO 表达的是 **当前在容器** 内最后进来的最先出去．
    
    我们考虑这样一个栈
    
    ```text
    push(1)
    pop(1)
    push(2)
    pop(2)
    ```
    
    如果从整体考虑，1 最先入栈，最先出栈，2 最后入栈，最后出栈，这样就成了一个先进先出表，显然是错误的．
    
    所以，在考虑数据结构是 LIFO 还是 FIFO 的时候，应当考虑在当前容器内的情况．

## 使用数组模拟栈

我们可以方便的使用数组来模拟一个栈，如下：

???+ note "实现"
    === "C++"
        ```cpp
        int st[N];
        // 这里使用 st[0] (即 *st) 代表栈中元素数量，同时也是栈顶下标
        
        // 压栈 ：
        st[++*st] = var1;
        // 取栈顶 ：
        int u = st[*st];
        // 弹栈 ：注意越界问题, *st == 0 时不能继续弹出
        if (*st) --*st;
        // 清空栈
        *st = 0;
        ```
    
    === "Python"
        ```python
        st = [0] * N
        # 这里使用 st[0] 代表栈中元素数量，同时也是栈顶下标
        
        # 压栈 ：
        st[st[0] + 1] = var1
        st[0] = st[0] + 1
        # 取栈顶：
        u = st[st[0]]
        # 弹栈：注意越界问题, *st == 0 时不能继续弹出
        if st[0]:
            st[0] = st[0] - 1
        # 清空栈
        st[0] = 0
        ```

## C++ STL 中的栈

C++ 中的 STL 也提供了一个容器 `std::stack`，使用前需要引入 `stack` 头文件．

???+ info "STL 中对 `stack` 的定义"
    ```cpp
    // clang-format off
    template<
        class T,
        class Container = std::deque<T>
    > class stack;
    ```
    
    `T` 为 stack 中要存储的数据类型．
    
    `Container` 为用于存储元素的底层容器类型．这个容器必须提供通常语义的下列函数：
    
    -   `back()`
    -   `push_back()`
    -   `pop_back()`
    
    STL 容器 `std::vector`、`std::deque` 和 `std::list` 满足这些要求．如果不指定，则默认使用 `std::deque` 作为底层容器．

STL 中的 `stack` 容器提供了一众成员函数以供调用，其中较为常用的有：

-   元素访问
    -   `st.top()` 返回栈顶
-   修改
    -   `st.push()` 插入传入的参数到栈顶
    -   `st.pop()` 弹出栈顶
-   容量
    -   `st.empty()` 返回是否为空
    -   `st.size()` 返回元素数量

此外，`std::stack` 还提供了一些运算符．较为常用的是使用赋值运算符 `=` 为 `stack` 赋值，示例：

```cpp
// 新建两个栈 st1 和 st2
std::stack<int> st1, st2;

// 为 st1 装入 1
st1.push(1);

// 将 st1 赋值给 st2
st2 = st1;

// 输出 st2 的栈顶元素
cout << st2.top() << endl;
// 输出: 1
```

## 使用 Python 中的 list 模拟栈

在 Python 中，你可以使用列表来模拟一个栈：

???+ note "实现"
    ```python
    st = [5, 1, 4]
    
    # 使用 append() 向栈顶添加元素
    st.append(2)
    st.append(3)
    # >>> st
    # [5, 1, 4, 2, 3]
    
    # 使用 pop 取出栈顶元素
    st.pop()
    # >>> st
    # [5, 1, 4, 2]
    
    # 使用 clear 清空栈
    st.clear()
    ```

## 参考资料

1.  [std::stack - zh.cppreference.com](https://zh.cppreference.com/w/cpp/container/stack)


## ds/top-tree.md

author:F7487

## Self-Adjusting Top Tree

### 简介

Self-Adjusting Top Tree，是 2005 年 Tarjan 和 Werneck 在他们的论文 Self-Adjusting Top Trees 中提出的一种基于 Top Tree 理论的维护完全动态森林的数据结构，简称为 SATT．

Self-Adjusting Top Tree 可以实现森林中任一棵树的链修改/查询、子树修改/查询以及非局部搜索等操作．

Splay Tree 是 SATT 的基础，但是 SATT 用的 Splay Tree 和普通的 Splay 在细节处不太一样（进行了一些扩展）．

### 问题引入

维护一个森林，支持如下操作：

-   删除，添加一条边，保证操作前后仍是一个森林．

-   修改某棵树上某条简单路径的权值．

-   修改以某个点为根的子树权值．

-   查询某棵树上的某条简单路径权值和．

-   查询以某个点为根的子树权值和．

### 树收缩

对于任意一棵树，我们都可以运用 **树收缩** 理论来将它收缩为一条边．

具体地，树收缩有两个基本操作：**Compress** 和 **Rake**，Compress 操作指定一个度数为 $2$ 的点 $x$，与点 $x$ 相邻的那两个点记为 $y$、$z$，我们连一条新边 $yz$；将点 $x$、边 $xz$、边 $xy$ 的信息放到 $yz$ 中储存，并删去它们．如图所示．

![](./images/top-tree1.svg)

Rake 操作指定一个度为 $1$ 的点 $x$，而且与点 $x$ 相邻的点 $y$ 的度数需大于 $1$，设点 $y$ 的另一个邻点为 $z$，我们将点 $x$、边 $xy$ 的信息放入边 $yz$ 中储存，并删去它们．如图所示．

![](./images/top-tree2.svg)

不难证明，任何一棵树都可以只用 Compress 操作和 Rake 操作来将它收缩为一条边，如图所示．

![](./images/top-tree3.svg)

### 簇

为了表达方便，我们记在进行任何操作之前的原树为 $T$．在对 $T$ 进行某些树收缩操作（可以不做任何操作）之后的树记为 $T_x$．

我们研究某个 $T_x$ 中某一条边所包含的信息情况．

这条边除了带有它本身的信息（当然，如果这条边在 $T$ 中不存在，这条边就没有本身的信息）之外，还可能包含其它通过 Compress/Rake 操作合并到它上面的点、边的信息．我们不妨先从下图中的树收缩过程中选取一条边，看看它所包含的信息在 $T$ 中代表哪些点、边．

![](./images/top-tree4.svg)

如图，选取的边和对应的图已用红线圈出．

可以看出，这条边所包含的信息在 $T$ 中代表的点、边是连通的．我们可以推及，对于任一 $T_x$ 中的任一条边储存的信息在 $T$ 中总体现为一个连通子图．我们将这样的连通子图称为 **簇（Cluster）**．

然而，簇是 **不完整的子图**，它包含的某些边的端点不被簇它自己包含．于是我们将这些端点称作簇的 **端点（Endpoint）**，将它包含的那些连通子图的点称作 **内点（Internal Node）**，连通子图的边称作 **内边（Internal Edge）**．

对于任意一个簇，都有以下性质：

1.  簇只存储和维护内点和内边的信息．

2.  簇有两个端点．这两个端点即为 $T_x$ 中代表那个簇的边相连的那两个点．两个端点之间的路径我们称之为 **簇路径（Cluster Path）**；记一个簇的两个端点分别为 $x$、$y$，我们下面用 $C(x,y)$ 来表示这个簇．

3.  内点仅与端点或内点相连．

特别地，对于 $T$ 中的每条边，都各自独立为一个簇（仅包含边自己的信息），这种簇我们称之为 **基簇（Base Cluster）**．对于由 $T$ 收缩到只有一条边的最终的 $T_x$，那条边代表的簇包含除了两个端点之外的整棵 $T$ 的信息，这个簇我们称之为 **根簇（Root Cluster）**．

![](./images/top-tree5.svg)

如图，上文提到的基簇已用红线标出．

从簇的视角来看 Compress/Rake 操作，我们发现这两个操作会将两个簇「合二为一」，剩下一个新簇，所以树收缩的过程也是所有的基簇合并为一个簇的过程．

所以我们也可以得到下图，是对一系列树收缩操作的另一表示．

![](./images/top-tree6.svg)

### Top Tree

我们现在想表示某一棵树进行树收缩的全过程．

我们可以用上文的两种方法来表示这一过程，但这样十分麻烦，如果树收缩进行了 $n$ 步，我们就要用 $n$ 棵树来表示整个树收缩．

考虑一个对某棵树进行某一树收缩的更简便表示，我们引入 **Top Tree**．

![](./images/top-tree7.jpg)

如图，是以上文的收缩方法和原树为基础的一棵 Top Tree．

Top Tree 有以下性质；

1.  一棵 Top Tree 对应一棵原树和一种对其进行树收缩的方法，Top Tree 的每个节点都表示在某个 $T_x$ 中的某一条边，也就是树收缩过程中形成的某一个簇．图中的形如 $N_x$ 的点表示 `compress(x)` 这一操作形成的簇．

2.  Top Tree 中的一个节点有两个儿子（都分别代表一个簇），这个节点代表的簇是这两个簇通过 Compress 或 Rake 操作合并得到的新簇．

3.  Top Tree 的叶子节点是基簇，其根节点是根簇．因此我们按一棵 Top Tree 的拓扑序分层，它的每一层就代表了一棵 $T_x$．

### 用三度化 Self-Adjusting Top Tree 实现信息维护

#### 原理

Top Tree 对树收缩过程的极大简化，使我们看到通过维护树收缩过程来维护树上信息的可能性，SATT 即是通过这一原理来维护树上信息的．

注意到树收缩的过程也是树上信息不断加入的过程，我们执行一次 `compress(x)`，$x$ 点的信息从此刻起就开始在某个簇中出现，影响着我们的统计结果．

假如我们现在用 Top Tree 来维护某棵树 $T$，树上的每个点，边都有权值，我们要维护的是 $T$ 的权值和．

现在我们在维护时要对 $T$ 中某个点 $x$ 的权值进行修改，很明显，我们就需要更改 Top Tree 中所有簇信息包含 $x$ 的节点信息，这样做单次时间复杂度会是 $O(n)$ 级别的．

然而，如果我们选的点它在 Top Tree 中簇信息包含 $x$ 的节点个数很少，也就是说使它的信息尽可能晚地加入簇中，我们单次操作的时间复杂度就会有一个很大的提升．如图．

![](./images/top-tree8.jpg)

SATT 就是通过修改 **某个点/某条路径** 在树收缩过程中信息被加入簇中的先后顺序（以降低其在被修改时的单次时间复杂度）来维护树上信息的．

### 实际结构

我们先将一棵原树 $T$ 分层定根，然后我们考虑对某种树收缩顺序的 Top Tree 的根簇，它有两个端点，我们令这其中一个端点就是原树的根，另一个端点任选．

![](./images/top-tree9.jpg)

如图，给根簇选出一组端点，这里标注簇时将端点也圈进去了．

由树收缩的基本操作可知，簇路径上的点、边 $(j,h,c,jh,hc)$ 的信息最后是通过 Compress 操作才加入 $C(k,g)$ 的，而的非簇路径点 $(a,b,i,f,g,e,ig,\cdots)$ 是通过 Rake 操作才加入 $C(k,g)$ 的．

我们将簇路径单独拿出来，这是一条形态特殊（为链）的树，我们为这棵树建出一棵 top tree（其代表的树收缩顺序任意）．

![](./images/top-tree10.jpg)

我们将这一结构称之为 **Compress Tree**，因为在这棵 Top Tree 中任一个点的两个儿子之间是通过 Compress 操作来合并成它们的父亲．

Compress Tree 里的节点称为 **Compress Node**．只考虑当前这条簇路径，一个非叶子的 Compress Node 就代表一次 compress 过程，表示将左儿子和右儿子信息合并起来，再将这个 `compress(x)` 本身存储的点 $x$ 信息加入．这棵 Compress Tree 就维护了 $C(k,g)$ 簇路径的信息．

另外，在 Compress Tree 中，我们实际上还对使用的 Top Tree 做了一些限制．注意到 Compress Tree 维护的是一个 $T$ 中点的深度两两不同的链，我们规定在 Compress Tree 中基簇的中序遍历顺序与对应的 $T$ 中边的深度是一致的，且中序遍历越小深度越浅．同样，对于每个点 $x$ 对应的 `compress(x)` 的关系也是如此．

现在来维护那些非簇路径的信息，我们假设这些非簇路径上的点、边已经形成了一个个极大簇，而这些极大簇是由这些用蓝线圈出的更小簇之间互相 Rake 形成的，对由一些更小簇合并形成一个极大簇的过程，我们用一个三叉树来表示，类似地，我们称这一结构为 **Rake Tree**，对应地 Rake Tree 里的点就是 **Rake Node**．每个 Rake Node 都代表一个簇，是由其左儿子和右儿子 Rake 到其中儿子代表的更小簇上形成的．具体可见下图，可知 Rake Tree 中的每个点都代表了 $T$ 中具有相同端点的更小簇．

![](./images/top-tree11.jpg)

如图，蓝线圈出的是一个个极大簇，黄线圈出的是一个个更小簇．

对于那些更小簇，我们对它们进行相同处理，给它们选择簇路径、建出 Compress Tree、……如此递归下去，就建出了许多表示树收缩过程的 Compress Tree，Rake Tree．

![](./images/top-tree12.jpg)

上图为原树的 Rake-Compress Tree（因为每个 Rake Node 都连着一棵 Compress Tree，所以表现为一棵 Rake Tree 连着许多 Compress Tree 的形态）和代表根簇路径的 Compress Tree．

考虑将这些树以某种方式拼接在一起，使它们形成一个有序的整体．记一个 Rake Tree 代表的最小簇的集合的公共端点是点 $x$．我们给这些 Rake Node 的中儿子（一个 Compress Tree 集合）都加入非 $x$ 的另一端点，但仍保持其中序遍历和 Top Tree 的基本性质，如图．

![](./images/top-tree13.jpg)

这一步相当于是让 Rake 操作加入某个 $T$ 中点的操作直接发生在 Compress Tree 中，这不仅使我们能正确维护 Rake Node 的信息（只需将三个儿子信息合并即可），还使我们 Compress Tree 的结构更完整．下一步，我们将 Compress Tree 改为三叉树，若某个 Rake Tree 的公共端点是点 $x$，我们就将 Rake Tree 挂在 `compress(x)` 的中儿子处，如图．

![](./images/top-tree14.jpg)

此时经过三叉化的 `compress(x)` 点，它的意义就变成先将其中儿子 Rake 到簇路径上，再统计左右儿子和点 $x$ 的信息．

最后，我们再处理一下根簇路径的那棵 Compress Tree：与其它所有 Compress Tree 一致地，按中序遍历加入它的两个端点，使得它的根储存整棵 $T$ 的信息．

于是我们就实现了用三度化 Self-Adjusting Top Tree 实现一棵树的信息维护．

![](./images/top-tree15.jpg)

总结一下，SATT 有以下性质：

1.  SATT 由 Compress Tree 和 Rake Tree 组成，Compress Tree 是一棵特殊的 Top Tree；Rake Tree 是一个三叉树，它们都对应一棵树进行树收缩的过程．

2.  Compress Tree 里的点最多有三个儿子．Compress Tree 可以做类似于 Splay 树的旋转操作（只需保证其中序遍历不变即可，旋转一个点时保持其中儿子不动）．

3.  Rake Tree 里的点一定有一个中儿子．Rake Tree 可以做类似于 Splay 树的旋转操作（只需保证其中序遍历不变即可，旋转一个点时保持其中儿子不动）．

4.  SATT 的拓扑序反映了原树 $T$ 的树收缩顺序．

我们在上文中提到的「修改某个点/某条路径在树收缩过程中信息被加入簇中的先后顺序」SATT 是否能实现呢，答案是肯定的．

在 SATT 中，有一个 `access(x)` 的操作，它的作用是使某点 $x$ 成为根簇的非根端点，同时在 SATT 中使 `compress(x)` 成为 SATT 的根．

我们可以通过 `access(x)` 操作以均摊 $O(\log n)$ 的复杂度使 SATT 中代表 `compress(x)` 的点旋到整棵 SATT 的树根，根据 SATT 的第四个性质，我们改变了 `compress(x)` 的操作顺序，使得它最晚执行，$x$ 点的信息也就被最晚加入；这样当我们要修改 $x$ 点的信息时，就只需要更新 `compress(x)`．

### 代码实现

#### Push 类函数

首先考虑上传信息，即 `Pushup(x)` 函数．在考虑对 SATT 的某个节点维护信息时，首先分这个点在 Compress Tree 还是在 Rake Tree 进行讨论，原因可见上文，不再赘述，下面以维护某个点的子树大小为例

```cpp
// ls(x) x的左儿子
// rs(x) x的右儿子
// ms(x) x的中儿子
// type==0 是 Compress Node
// type==1 是 Rake Node
void pushup(int x, int type) {
  if (type == 0)
    size[x] = size[rs(x)] + size[ms(x)] + 1;
  else
    size[x] = size[rs(x)] + size[ms(x)] + size[ls(x)];
  return;
}
```

查询点 $x$ 的子树大小，就将其 Access 到 SATT 根，答案是其中儿子的 size $+1$；因为根据上文，在 Access 之后，其中儿子才是它的真子树．

然后考虑下传信息，即 `Pushdown(x)` 函数．我们如果要对原树中的某个子树做整体修改，一个很自然的想法是：将这个节点直接 Access 到 SATT 根节点，给它的中儿子打上一个标记即可．同理，查询子树就直接 Access 后查询中儿子．

我们如果要对原树中的某条路径做整体修改，我们就 expose 路径的两个端点，其中 `expose(x, y)` 是指使点 $x$ 成为 $T$ 的根节点，使点 $y$ 成为根簇的另一个端点．对应在 SATT 上，此时根簇的 Compress Tree 就是 $x$ 到 $y$ 的路径．于是直接给根簇的 Compress Tree 打上一个标记即可．同理查询链 expose 后查询根节点即可．

于是我们就知道问题引入的问题怎么做了．

```cpp
void pushdown(int x, int type) {
  if (type == 0) {
    // 处理链
    chain[ls(x)] += chain[x] chain[rs(x)] += chain[x];
    val[ls(x)] += chain[x];
    val[rs(x)] += chain[x];
    // 处理子树
    subtree[ls(x)] += subtree[x];
    subtree[rs(x)] += subtree[x];
    subtree[ms(x)] += subtree[x];
    val[ls(x)] += subtree[x];
    val[rs(x)] += subtree[x];
    val[ms(x)] += subtree[x];
    subtree[x] = 0;
  } else {
    subtree[ls(x)] += subtree[x];
    subtree[rs(x)] += subtree[x];
    subtree[ms(x)] += subtree[x];
    val[ls(x)] += subtree[x];
    val[rs(x)] += subtree[x];
    val[ms(x)] += subtree[x];
    subtree[x] = 0;
  }
  return;
}

// 下传标记
void pushall(int x, int type) {
  if (!isroot(x)) pushall(father[x], type);
  pushdown(x, type);
  return;
}
```

#### Splay 类函数

我们知道 SATT 中的 Rake Tree 和 Compress Tree 都是可以旋转的，也就是说它们可以用 Splay 来维护．因此我们可以写出以下代码：

```cpp
// 是一个节点的中儿子或无父亲
// ls 一个SATT节点的左儿子
// rs 一个SATT节点的右儿子
// ms 一个SATT节点的中儿子
// type==1 在 Rake Tree中
// type==0 在 Compress Tree中
bool isroot(int x) { return rs(father[x]) != x && ls(father[x]) != x; }

bool direction(int x) { return rs(father[x]) == x; }

void rotate(int x, int type) {
  int y = father[x], z = father[y], d = direction(x), w = son[x][d ^ 1];
  if (z) son[z][ms(z) == y ? 2 : direction(y)] = x;
  son[x][d ^ 1] = y;
  son[y][d] = w;
  if (w) father[w] = y;
  father[y] = x;
  father[x] = z;
  pushup(y, type);
  pushup(x, type);
  return;
}

void splay(int x, int type, int goal = 0) {
  pushall(x, ty);  // 下传标记
  for (int y; y = father[x], (!isroot(x)) && y != goal; rotate(x, ty)) {
    if (father[y] != goal && (!isroot(y))) {
      rotate(direction(x) ^ diretion(y) ? x : y, type);
    }
  }
  return;
}
```

值得注意的是，函数 `direction` 和 `isroot` 与普通 Splay 的不同．因为无论这个点怎么转，这个点的中儿子是不会变的．

#### Access 类函数

`access(x)` 的意义是：将点 $x$ 旋转到整个 SATT 的根处，使点 $x$ 成为根簇的两个端点之一（另一端点即为 $T$ 的根节点），同时不能改变原树的结构和原树的根．

为了实现 `access(x)`，我们先将其旋转到其所在 Compress Tree 的树根，再把点 $x$ 的右儿子去掉，使点 $x$ 成为其所在 Compress Tree 对应簇的端点．

```cpp
if (rs(x)) {
  int y = new_node();
  setfather(ms(x), y, 0);
  setfather(rs(x), y, 2);
  rs(x) = 0;
  setfather(y, x, 2);
  pushup(y, 1);
  pushup(x, 0);
}
```

如果这时点 $x$ 已经到了根部，则退出；若没有，则执行以下步骤，以让它跨过它上面的 Rake Tree：

1.  将其父亲节点（一定是一个 Rake Node），splay 到其 Rake Tree 的树根；

2.  将 $x$ 的爷节点（一定是一个 Compress Node）splay 到其 Compress Tree 根部．

3.  若 $x$ 的爷节点有一个右儿子，则将点 x 和爷节点的右儿子互换，更新信息，然后退出．

4.  若爷节点没有右儿子，则先让点 $x$ 成为爷节点的右儿子，此时点 $x$ 原来的父节点没有中儿子，根据上文 Rake Node 的性质，它不能存在．于是调用 `Delete` 函数，将其删除，然后退出．

1，2 两个步骤合称为 **Local Splay**．3，4 两个步骤合称为 **Splice**．但我们方便起见，将它们都写在 `Splice(x)` 函数里．

上文提到的 `Delete(x)` 函数是这样的：

1.  检视将要删除的点 $x$ 有没有左儿子，若有，则将左儿子的子树后继续旋转到点 $x$ 下方（成为新的左儿子），然后将右儿子（若有）变成左儿子的右儿子，此时点 $x$ 的左儿子就代替了点 $x$．这相当于 Splay 的合并操作．

2.  若没有左儿子，则直接让其右儿子代替点 $x$．

不难发现，`Splice(x)` 改变了原树的一些簇的端点选取．一次 splice 完了之后，我们将点 $x$ 的父亲节点当作新的点 $x$，进行下一次 splice．

最终我们会发现，我们最开始要操作的点 $x$ 一定在根簇的 Compress Tree 最右端．我们只需最后做一次 **Global Splay**，将其旋至 SATT 根部即可．

```cpp
// ls 一个SATT节点的左儿子
// rs 一个SATT节点的右儿子
// ms 一个SATT节点的中儿子
// son[x][0] ls
// son[x][1] rs
// son[x][2] ms
// type==1 在 Rake Tree中
// type==0 在 Compress Tree中
int new_node() {
  if (top) {
    top--;
    return Stack[top + 1];
  }
  return ++tot;
}

void setfather(int x, int fa, int type) {
  if (x) father[x] = fa;
  son[fa][type] = x;
}

void Delete(int x) {
  setfather(ms(x), father[x], 1);
  if (ls(x)) {
    int p = ls(x);
    pushdown(p, 1);
    while (rs(p)) p = rs(p), pushdown(p, 1);
    splay(p, 1, x);
    setfather(rs(x), p, 1);
    setfather(p, father[x], 2);
    pushup(p, 1);
    pushup(father[x], 0);
  } else
    setfather(rs(x), father[x], 2);
  Clear(x);
}

void splice(int x) {
  // local splay
  splay(x, 1);
  int y = father[x];
  splay(y, 0);
  pushdown(x, 1);
  // splice
  if (rs(y)) {
    swap(father[ms(x)], father[rs(y)]);
    swap(ms(x), rs(y));
  } else
    Delete(x);
  pushup(x, 1);
  pushup(y, 0);
}

void access(int x) {
  splay(x, 0);
  if (rs(x)) {
    int y = new_node();
    setfather(ms(x), y, 0);
    setfather(rs(x), y, 2);
    rs(x) = 0;
    setfather(y, x, 2);
    pushup(y, 1);
    pushup(x, 0);
  }
  while (father[x]) {
    splice(father[x]);
    x = father[x];
    pushup(x, 0);
  }
  splay(x, 0)  // global splay
}
```

若要让一个点成为原树的根，那么我们就将点 $x$ Access 到 SATT 的根节点，可知此时点 $x$ 已经是最终状态的簇一个端点．由 Compress Tree 的中序遍历性质可知，将点 $x$ 所在的 Compress Tree 左右颠倒（所有点的左右儿子互换），就使点 $x$ 成为原树的根．在具体实现中，我们通过给点 $x$ 打上一个翻转标记，之后下传来进行这一过程．

```cpp
void makeroot(int x) {
  access(x);
  push_rev(x);
}
```

于是 `expose(x, y)` 就呼之欲出：

```cpp
void expose(int x, int y) {
  makeroot(x);
  access(y);
}
```

### Link & Cut

现在我们要将原树中两个不连通的点之间连一条边，我们先让其中的一个点 $x$ 成为原树的根，再将另一个点 $y$ 旋转到根处，可知此时应该使点 $y$ 成为点 $x$ 的右儿子．然后在点 $y$ 的右儿子上挂上这一条边（在只需维护点的 SATT 中，这一步可省）．

```cpp
void Link(int x, int y, int z) {
  // z代表连接 x, y的边
  access(x);
  makeroot(y);
  setfather(y, x, 1);
  setfather(z, y, 0);
  pushup(x, 0);
  pushup(y, 0);
}
```

`Cut` 跟 `Link` 原理差不多

```cpp
void cut(int x, int y) {
  expose(x, y);
  clear(rs(x));  // 删掉 xy 这一基簇
  father[x] = ls(y) = rs(x);
  pushup(y, 0);
}
```

### 完整代码

??? note "[Luogu P3690【模板】动态树](https://www.luogu.com.cn/problem/P3690)"
    ```cpp
    --8<-- "docs/ds/code/top-tree/top-tree_1.cpp"
    ```

### SATT 的时间复杂度证明

设在一棵 SATT（点数为 $n$）中，其当前状态 $x$ 的势能函数为

$$
\varphi(x)= \sum_{i=1}^{n} r(i)
$$

其中 $r(i) = \lceil \log_2 \text{siz}(i) \rceil$．$\text{siz}(i)$ 为以 $i$ 为根的子树大小．

则 SATT 的 splay 的均摊复杂度显然仍是 $3n\log n + 1$，即使 SATT 是一个三叉树．

因此对于 SATT，我们只要证得 Access 函数复杂度正确，就能证得 SATT 的时间复杂度．

我们逐步分析 Accese 的均摊复杂度．

我们先要将点 $x$ 旋至其所在 Compress Tree 的根，则这一步的均摊复杂度

$$
a \leq  3\log n +1
$$

接着我们要使点 $x$ 无右儿子，则这一步的均摊复杂度

$$
a = 1 + r'(\gamma)- 0 \leq \log n +1
$$

![](./images/top-tree16.jpg)

如图，为去掉点 $x$ 的右儿子过程．

然后是 Local Splay，Splice 交替进行的过程，经过若干次 Splice，点 $x$ 被旋至 SATT 的根．我们对其中一组 Local Splay，Splice 进行分析：

![](./images/top-tree17.jpg)

![](./images/top-tree18.jpg)

![](./images/top-tree19.jpg)

如图，体现了对点 $x$ 做一次 Splice 的过程，不包括最后左旋点 $x$ 的部分．

为表达方便，设 $r_x(i)$ 为点 $i$ 在状态 $x$ 时的 $r$ 值．

由图，易知由状态 1 到状态 2 的操作（将点 $x$ 的父亲旋至其 Rake Tree 的根部的 Local Splay 操作）的均摊复杂度

$$
a \leq  3(r_2(\gamma)- r_1(\gamma))+1
$$

由图，易知由状态 2 到状态 3 的操作（将点 $x$ 的爷节点旋至其 Compress Tree 的根部的 Local Splay 操作）的均摊复杂度

$$
a \leq  3(r_3(B)- r_2(B))+1
$$

重点分析由状态 3 到状态 4 的操作（Splice）

$$
a = r_4(\gamma) -r_3(\gamma) +1
$$

不难发现 $r_4(\gamma) \leq r_3(B)$

故这一次操作的均摊复杂度为

$$
\begin{aligned}
a &\leq r_3(B)- r_3(\gamma)+1\\
&\leq 3(r_3(B)- r_3(\gamma))+1\\
\end{aligned}
$$

综合上述过程，一次 Splice 的复杂度为

$$
a\leq 3r_3(B)+3r_3(B)+3r_2(\gamma)-3r_3(\gamma)-3r_2(B)-3r_1(\gamma)+3
$$

记下一次 Splice 的点 $X$（即状态 4 中的点 $B$）的 $r$ 值为 $r'(X)$，并注意到 $r_3(\gamma),r_1(\gamma) \ge r_1(X)$，$r_3(B),r_2(\gamma) \leq r'(X)$ 且 $r_3(B)=r_2(B)$，所以

$$
a\leq  9(r'(X)-r(X))+3
$$

除了上面这个复杂度以外，在 Splice 中可能还会有因 `delete(x)` 产生的额外均摊复杂度，记这一部分为 $a' \leq 3\log n +1$．

先不管 $a'$ 部分，每次 Splice 的 $r'(X)$ 等于下一次的 $r(X)$，且第一次 Splice 的 $r(X)$ 等于我们一开始旋转点 $x$ 到其 Compress Tree 树根时的 $r(X)$，则对于不计 `delete(x)` 的一次 `access(x)` 复杂度，我们有：

$$
a \leq 9(r'(x)-r(x))+ 3k + 1
$$

其中 $k$ 为 Splice 次数．

看样子 $a$ 会带一个 $3k+1$ 导致均摊复杂度无法分析，但我们有办法来对付它，注意到 zig-zig/zig-zag 的旋转可以这么均摊

$$
\begin{aligned}
a &\leq 3(r'(X)-r(X)) + q\\
&\leq 3(q-1)(r'(X)-r(X))
\end{aligned}
$$

如果我们能找到足够多的 zig-zig，zig-zag 操作，我们就可以将这 $3k+1$ 平摊到这些操作上去，从而消掉这个 $3k+1$．

我们发现 Globel Splay 里面就有这么多的 zig-zig，zag-zig 来给我们使用，因为 Globel Splay 里面点的个数一定大于 $k$，而从点 $x$ 到 Globel Splay 根部路径的点数一定不少于 $k$，也就是说一次 `access(x)` 中一定会至少有 $\dfrac k2$ 个 zig-zag 操作，算上 Globel Splay 的均摊复杂度 $a \leq 3\log n +1$，一次 `access(x)` 不记 `delete(x)` 的均摊复杂度为

$$
\begin{aligned}
a&\leq 9(r'(X)-r(X)) + 3k + 1 + 18(r''(X)-r'(X)) -S+1 +3 \log n +1,S \ge 3k\\
a&\leq 18(r''(X)-r(X)) +2 +3\log n+1\\
a&\leq 21(r''(X)-r(X)) +3
\end{aligned}
$$

现在算上 $a'$，列出进行 $m$ 次 `access(x)` 操作的总式子．

$$
\sum_{i=1}^m a_i' + \sum_{i=1}^m a_i = \sum_{i=1}^m c_i + \varphi(x_n) -\varphi(x_0)
$$

我们要求的是实际复杂度

$$
\begin{aligned}
\sum_{i=1}^m c_i &= \sum_{i=1}^m a_i +\sum_{i=1}^m a_i' - \varphi(x_n) +\varphi(x_0)\\
&\le \sum_{i=1}^m a_i' + 21m\log n +n\log n +3m
\end{aligned}
$$

注意到 `delete(x)` 操作的本质是删掉一个 Rake Node，但我们在 $m$ 次操作中最多只会添加 $m$ 个 Rake Node，由 Rake Node 的定义，我们初始时最多有 $n$ 个 Rake Node，也就是说我们总共只会做 $m+n$ 次 `delete(x)` 操作，由 $a' \leq 3\log n +1$ 可知

$$
\sum_{i=1}^m c_i \leq 3(m+n)\log n + 21m\log n +n\log n +4m +n
$$

所以我们就证明了 Access 的复杂度，而其他函数要么基于 Access 要么单次时间复杂度为常数，所以我们就证明了 SATT 的复杂度．

顺便一提，如果像 LCT 一样省略 Global Splay 的过程，改为在每次 Splice 时直接将要 Access 的点旋转一下，这样做时间复杂度也是对的（实测省略 Global Splay 的版本要快很多，能与 LCT 在 Luogu P3690 跑得不分上下）．

### 例题

#### 例题 1

???+ note "[CEOI 2019 Dynamic Diameter](https://loj.ac/p/3163)"
    给定一棵 $n$ 个节点的树，每条边有边权，有 $q$ 次更新，每次修改一条边的边权，并询问树的直径．强制在线．

维护动态直径，建出 SATT 后，我们只需要在 `Pushup(x)` 里面维护每个点的答案，最后查询根节点的答案（即整棵树的直径）就可以了．

```cpp
void pushup(int x, int op) {
  if (op == 0) {
    // 是 Compress Node
    len[x] = len[ls(x)] + len[rs(x)];
    diam[x] = maxs[ls(x)][1] + maxs[rs(x)][0];
    diam[x] =
        max(diam[x], max(maxs[ls(x)][1], maxs[rs(x)][0]) + maxs[ms(x)][0]);
    diam[x] = max(diam[x], max(max(diam[ls(x)], diam[rs(x)]), diam[ms(x)]));
    maxs[x][0] =
        max(maxs[ls(x)][0], len[ls(x)] + max(maxs[ms(x)][0], maxs[rs(x)][0]));
    maxs[x][1] =
        max(maxs[rs(x)][1], len[rs(x)] + max(maxs[ms(x)][0], maxs[ls(x)][1]));
  } else {
    // 是 Rake Node
    diam[x] = maxs[ls(x)][0] + maxs[rs(x)][0];
    diam[x] =
        max(diam[x], maxs[ms(x)][0] + max(maxs[ls(x)][0], maxs[rs(x)][0]));
    diam[x] = max(max(diam[x], diam[ms(x)]), max(diam[ls(x)], diam[rs(x)]));
    maxs[x][0] = max(maxs[ms(x)][0], max(maxs[ls(x)][0], maxs[rs(x)][0]));
  }
  return;
}
```

其中 $diam$ 是当前点的答案（这个点代表的簇的直径）．$len$ 表示当前 Compress Node 所在簇路径的长度，$maxs_{0/1}$ 表示 Compress Node 到簇内点和端点的不选簇路径儿子/不选父亲的最大距离（如果是 Rake Node 则只存储选取当前簇的上端点到簇内点和端点的最大距离 $maxs_0$）．每次查询 SATT 根节点的 diam 即可，正确性显然．

注意对 `Pushrev(x)` 做一些改动．

```cpp
void pushrev(int x) {
  if (!x) return;
  r[x] ^= 1;
  swap(ls(x), rs(x));
  swap(maxs[x][0], maxs[x][1]);
}
```

#### 例题 2

???+ note "[「CSP-S 2019」树的重心](https://loj.ac/p/3213)"
    给定一棵树，求出单独删去树的每条边后，分裂出的两个子树的重心编号和之和．

假如我们能动态 $O(\log n)$ 维护树的重心，我们就做出这个题了．

SATT 支持动态 $O(\log n)$ 维护树的重心，做到这需要 **非局部搜索（Non-local Search）**．

对于一种树上的性质，如果一个点/一条边在整棵树中有这种性质，且在所有包含它的子树中都包含此种性质，我们就称这个性质是 **局部的（Local）**，否则称它是 **非局部的（Non-local）**．局部信息一般可以通过 `pushup(x)` 来维护

例如，权值最小值是局部的，因为一个点/一条边如果在整棵树中权值最小，那么在所有包含它的子树中它也是权值最小的，而权值第二小显然就是非局部的．

我们上文维护的 $diam$ 也是局部信息．

回到正题，重心显然是一个非局部信息，无法通过简单的 `pushup(x)` 来维护．我们考虑在 SATT 上搜索：

我们的搜索从 SATT 的根节点，即根簇开始．注意到重心有很好的性质：假如有一条边的一侧点的个数大于等于另一侧点的个数，那么边的这一侧一定至少有一个重心（重心可能有两个）．

记 $sum$ 表示某一个簇的点个数，$maxs$ 为一棵 Rake Tree 的所有 Rake Node 中儿子的 $sum$ 最大值．

```cpp
void pushup(int x, int op) {
  if (op == 0) {
    // 是 Compress Node
    sum[x] = sum[ls(x)] + sum[rs(x)] + sum[ms(x)] + 1;
  } else {
    // 是 Rake Node
    maxs[x] = max(maxs[ls(x)], max(maxs[rs(x)], sum[ms(x)]));
    sum[x] = sum[ls(x)] + sum[rs(x)] + sum[ms(x)];
  }
}
```

![](./images/top-tree20.jpg)

如图，为在进行 Non-local Search 时的 SATT 和对应的原树 $T$．

我们做如下比较：

1.  比较簇 $compress(Y)$ 的 $sum$ 值与簇 $compress(Z)$、簇 $A$ 和点 $X$ 的并（我们暂称为簇 $\alpha$）的 $sum$ 值．若 $compress(Y)$ 的 $sum$ 值大于等于后者，说明至少有一个重心在 $compress(Y)$ 的子树中，我们递归到 $compress(Y)$ 搜索．（如果此处取等，点 $X$ 也是一个重心，需要记录）

2.  比较簇 $compress(Z)$ 的 $sum$ 值与簇 $compress(Y)$、簇 $A$ 和点 $X$ 的并（我们暂称为簇 $\beta$）的 $sum$ 值．若 $compress(Z)$ 的 $sum$ 值大于等于后者，说明至少有一个重心在 $compress(Z)$ 的子树中，我们递归到 $compress(Z)$ 搜索．（如果此处取等，点 $X$ 也是一个重心，需要记录）

3.  比较点 $x$ 中儿子 Rake tree 之中 $sum$ 最大的更小簇的 $sum$ 值与簇 $compress(Y)$、簇 $A$、点 $X$ 及其它更小簇的并（我们暂称为簇 $Y$）的 $sum$ 值，若那个更小簇的 $sum$ 值大于等于后者，说明至少有一个重心在那个更小簇的子树中，我们递归到它搜索．如果此处取等，点 $X$ 也是一个重心，需要记录．

4.  若以上比较都不递归，则点 $X$ 一定是一个重心，记录并退出．

第一步的搜索显然正确，之后应该怎么搜呢？

假如我们递归到 $Y$，则现在 $Y$ 储存信息的并不完整，因为 $compress(Y)$ 里面只存储了它自己这个簇的信息，而我们要求的是整棵树的重心．解决方法是，将之前簇的信息记录下来，在点 $Y$ 上比较计算时将上一个簇的信息与点 $Y$ 自己的信息合并处理．具体实现如下：

```cpp
void non_local_search(int x, int lv, int rv, int op) {
  // lv 和 rv 都是搜索的上一个簇的信息
  if (!x) return;
  psd(x, 0);
  if (op == 0) {
    if (maxs[ms(x)] >=
        sum[ms(x)] - maxs[ms(x)] + sum[rs(x)] + sum[ls(x)] + lv + 1 + rv) {
      if (maxs[ms(x)] ==
          sum[ms(x)] - maxs[ms(x)] + sum[rs(x)] + sum[ls(x)] + lv + 1 + rv) {
        if (ans1)
          ans2 = x;
        else
          ans1 = x;
      }
      non_local_search(
          ms(x),
          sum[ms(x)] - maxs[ms(x)] + sum[rs(x)] + sum[ls(x)] + 1 + lv + rv, 0,
          1);
      return;
    }
    if (ss[rs(x)] + rv >= ss[ms(x)] + ss[ls(x)] + lv + 1) {
      if (ss[rs(x)] + rv == ss[ms(x)] + ss[ls(x)] + lv + 1) {
        if (ans1)
          ans2 = x;
        else
          ans1 = x;
      }
      non_local_search(rs(x), sum[ms(x)] + 1 + sum[ls(x)] + lv, rv, 0);
      return;
    }
    if (sum[ls(x)] + lv >= sum[ms(x)] + sum[rs(x)] + 1 + rv) {
      if (sum[ls(x)] + lv == sum[ms(x)] + sum[rs(x)] + 1 + rv) {
        if (ans1)
          ans2 = x;
        else
          ans1 = x;
      }
      non_local_search(ls(x), lv, rv + sum[ms(x)] + 1 + sum[rs(x)], 0);
      return;
    }
  } else {
    if (maxs[ls(x)] == maxs[x]) {
      non_local_search(ls(x), lv, rv, 1);
      return;
    }
    if (maxs[rs(x)] == maxs[x]) {
      non_local_search(rs(x), lv, rv, 1);
      return;
    }
    non_local_search(ms(x), lv, rv, 0);
    return;
  }
  if (ans1)
    ans2 = x;
  else
    ans1 = x;
}
```

??? note "示例代码"
    ```cpp
    --8<-- "docs/ds/code/top-tree/top-tree_2.cpp"
    ```

### Reference

1.  Robert E. Tarjan and Renato F. Werneck. 2005. Self-adjusting top trees. In Proceedings of the sixteenth annual ACM-SIAM symposium on Discrete algorithms (SODA '05). Society for Industrial and Applied Mathematics, USA, 813–822. DOI 10.5555/1070432.1070547

2.  [negiizhao 的博客](https://negiizhao.blog.uoj.ac/blog/4912)


## ds/treap.md

author: Dev-XYS, ttzytt, Sora233, qwqAutomaton

前置知识：[朴素二叉搜索树](./bst.md)，[堆基础](./heap.md)．

## 简介

Treap（树堆）是一种 **弱平衡** 的 **二叉搜索树**．

Treap 的结点除了被维护的 **权值**（$\textit{val}$）之外，还附加了一个随机的 **优先级**（$\textit{priority}$）．其中，权值满足二叉搜索树性质，优先级满足堆性质（小根堆或大根堆）．

其中，二叉搜索树的性质是指：

-   左子树所有节点的权值（$\textit{val}$）比父节点小．
-   右子树所有节点的权值（$\textit{val}$）比父节点大．

堆的性质是：

-   子节点优先级（$\textit{priority}$）比父节点大或小（取决于是小根堆还是大根堆）．

不难看出，如果用的是同一个值，那么这两种数据结构在组合后会变成一条链，所以我们再在搜索树的基础上，引入一个给堆的值 $\textit{priority}$．对于 $\textit{val}$ 值，我们维护搜索树的性质，对于 $\textit{priority}$ 值，我们维护堆的性质．其中 $\textit{priority}$ 这个值是随机给出的．

下图就是一个 Treap 的例子（这里使用的是小根堆，即根节点的优先级最小）．

![一个 Treap 的例子](./images/treap-treap-example.svg)

那我们为什么需要大费周章的去让这个数据结构符合树和堆的性质，并且随机给出堆的值呢？

要理解这个，首先需要理解朴素二叉搜索树的问题．在给朴素搜索树插入一个新节点时，我们需要从这个搜索树的根节点开始递归，如果新节点比当前节点小，那就向左递归，反之亦然．

最后当发现当前节点没有子节点时，就根据新节点的值的大小，让新节点成为当前节点的左或右子节点．

如果插入结点的权值是随机的（换言之，是随机插入的），那这个朴素搜索树的高度较小（接近 $\log n$，其中 $n$ 为结点数），而每一层的节点数较多，即它的形状会非常的「胖」．上图的 Treap 就是一个例子．因此此时的任意操作复杂度都将会是 $O(\log n)$ 左右．

不过，这只是在随机情况下的复杂度，如果我们按照下面这个非常有序的顺序给一个朴素的搜索树插入节点：

```plain
1 2 3 4 5
```

那么这棵树将会退化成链，即变得非常「瘦长」（每次插入的节点都比前面的大，所以都被安排到右子节点了）：

![退化成链的例子](./images/treap-search-tree-chain.svg)

不难看出，查询的复杂度也从 $O(\log n)$ 变成了 $O(n)$.

而 treap 为了解决这个问题、达到一个较为「平衡」的状态，通过维护随机的优先级满足堆性质，「打乱」了节点的插入顺序，从而让二叉搜索树达到了理想的复杂度，避免了退化成链的问题．

## Treap 复杂度的证明

由于 treap 各种操作的复杂度都和所操作的节点的深度有关，我们首先证明，所有节点的期望深度都是 $O(\log n)$．

### 记号约定

为了方便表述，我们约定：

-   $n$ 是节点个数．
-   Treap 节点中满足二叉搜索树性质的称为 **权值**，满足堆性质的（也就是随机的）称为 **优先级**．不妨设优先级满足小根堆性质．
-   $x_k$ 表示权值第 $k$ 小的节点．
-   $X_{i,j}$ 表示集合 $\{x_i,x_{i+1},\cdots,x_{j-1},x_j\}$，即按权值升序排列后第 $i$ 个到第 $j$ 个的节点构成的集合．
-   $\operatorname{dep}(x)$ 表示节点 $x$ 的深度．规定根节点的深度是 $0$．
-   $Y_{i,j}$ 是一个指示器随机变量，当 $x_i$ 是 $x_j$ 的祖先时值为 $1$，否则为 $0$．特别地，$Y_{i,i}=0$．
-   $\Pr(A)$ 表示事件 $A$ 发生的概率．

### 节点期望深度的证明

由于节点 $x_i$ 的深度等于它祖先的个数，因此有

$$
\operatorname{dep}(x_i)=\sum_{k=1}^nY_{k,i}.
$$

那么根据期望的线性性，有

$$
E(\operatorname{dep}(x_i))=E\left(\sum_{k=1}^nY_{k,i}\right)=\sum_{k=1}^nE(Y_{k,i}).
$$

由于 $Y_{k,i}$ 是指示器随机变量，它的期望就等于它为 $1$ 的概率，因此

$$
E(\operatorname{dep}(x_i))=\sum_{k=1}^n\Pr(Y_{k,i}=1).
$$

我们先证明引理：$Y_{i,j}=1$ 当且仅当 $x_i$ 的优先级是 $X_{i,j}$ 中最小的．

??? note "引理的证明"
    考虑分类讨论 $x_i$ 和 $x_j$ 的情况．
    
    1.  若 $x_i$ 是根节点：由于优先级满足小根堆性质，$x_i$ 的优先级最小，并且对于任意的 $x_j$，$x_i$ 都是 $x_j$ 的祖先．
    2.  若 $x_j$ 是根节点：同理，$x_j$ 优先级最小，因此 $x_i$ 不是 $X_{i,j}$ 中优先级最小的；同时 $x_i$ 也不是 $x_j$ 的祖先．
    3.  若 $x_i$ 和 $x_j$ 在根节点的两个子树中（一左一右），那么根节点 $r\in X_{i,j}$. 因此 $x_i$ 的优先级不可能是 $X_{i,j}$ 中最小的（因为根节点的比它小）．同时，由于 $x_i$ 和 $x_j$ 分属两个子树，$x_i$ 也不是 $x_j$ 的祖先．
    4.  若 $x_i$ 和 $x_j$ 在根节点的同一个子树中，此时可以将这个子树单独拿出来作为一棵新的 treap，递归进行上面的证明即可．

那么根据引理，深度的期望可以转化成

$$
E(\operatorname{dep}(x_i))=\sum_{k=1}^n\Pr(x_k=\min X_{i,k}\land k\neq i).
$$

又因为节点的优先级是随机的，我们假定集合 $X_{i,j}$ 中任何一个节点的优先级最小的概率都相同，那么

$$
\begin{aligned}
E(\operatorname{dep}(x_i))&=\sum_{k=1}^n\Pr(x_k=\min X_{i,k}\land k\neq i)\\
&=\sum_{k=1}^{n}\Pr(x_k=\min X_{i,k})-1\\
&=\sum_{k=1}^n\dfrac{1}{|i-k|+1}-1\\
&=\sum_{k=1}^{i-1}\dfrac{1}{i-k+1}+\sum_{k=i+1}^n\dfrac{1}{k-i+1}\\
&=\sum_{j=2}^i\dfrac 1j+\sum_{j=2}^{n-i+1}\dfrac 1j\\
&\le 2\sum_{j=2}^n\dfrac 1j < 2\sum_{j=2}^n\int_{j-1}^j\dfrac 1x\mathrm dx\\
&=2\int_1^n\dfrac 1x\mathrm dx=2\ln n=O(\log n).
\end{aligned}
$$

因此每个节点的期望深度都是 $O(\log n)$．

而朴素的二叉搜索树的操作的复杂度均是 $O(h)$，同时 treap 维护堆性质的复杂度也是 $O(h)$ 的，因此 treap 各种操作的期望复杂度都是 $O(\log n)$．

???+ note "期望复杂度的感性理解"
    首先，我们需要认识到一个节点的 $\textit{priority}$ 属性是和它所在的层数有直接关联的．再回忆堆的性质：
    
    -   子节点值（$\textit{priority}$）比父节点大或小（取决于是小根堆还是大根堆）
    
    我们发现层数低的节点，比如整个树的根节点，它的 $\textit{priority}$ 属性也会更小（在小根堆中）．并且，在朴素的搜索树中，先被插入的节点，也更有可能会有比较小的层数．我们可以把这个 $\textit{priority}$ 属性和被插入的顺序关联起来理解，这样，也就理解了为什么 treap 可以把节点插入的顺序通过 $\textit{priority}$ 打乱．

给 treap 插入新节点时，需要同时维护树和堆的性质．其中，搜索树的性质可以在插入时维护，而堆性质的维护则有两种处理方法，分别是旋转和分裂、合并．使用这两种方法的 treap 被分别称为 **旋转 treap** 和 **无旋 treap**．

## 旋转 treap

**旋转 treap** 维护平衡的方式为旋转，和 AVL 树的旋转操作类似，分为 **左旋** 和 **右旋**．即在满足二叉搜索树的条件下根据堆的优先级对 treap 进行平衡操作．

旋转 treap 在做普通平衡树题的时候，是所有平衡树中常数较小的．

下面的讲解中的代码用指针实现了旋转 treap，文末附有数组形式的完整实现．

???+ info "Info"
    代码中的 `rank` 代表前面讲的优先级（$\textit{priority}$ 属性），该属性满足的是小根堆性质．

### 节点结构

```cpp
struct Node {
  Node *ch[2];  // 两个子节点的地址
  int val, rank;
  int rep_cnt;  // 当前这个值（val）重复出现的次数
  int siz;      // 以当前节点为根的子树大小

  Node(int val) : val(val), rep_cnt(1), siz(1) {
    ch[0] = ch[1] = nullptr;
    rank = rand();
    // 注意初始化的时候，rank 是随机给出的
  }

  void upd_siz() {
    // 用于旋转和删除过后，重新计算 siz 的值
    siz = rep_cnt;
    if (ch[0] != nullptr) siz += ch[0]->siz;
    if (ch[1] != nullptr) siz += ch[1]->siz;
  }
};
```

### 旋转

旋转操作是 treap 的一个非常重要的操作，主要用来在保持 treap 树性质的同时，调整不同节点的层数，以达到维护堆性质的作用．

旋转操作的左旋和右旋可能不是特别容易区分，以下是两个较为明显的特点：

旋转操作的含义：

-   在不影响搜索树性质的前提下，把和旋转方向相反的子树变成根节点（如左旋，就是把右子树变成根节点）
-   不影响性质，并且在旋转过后，跟旋转方向相同的子节点变成了原来的根节点（如左旋，旋转完之后的左子节点是旋转前的根节点）

左旋和右旋操作是相互的，如下图．

![旋转操作](./images/treap-rotate.svg)

```cpp
enum rot_type { LF = 1, RT = 0 };

void _rotate(Node *&cur,
             rot_type dir) {  // dir参数代表旋转的方向 0为右旋，1为左旋
  // 注意传进来的 cur 是指针的引用，也就是改了这个
  // cur，变量是跟着一起改的，如果这个 cur 是别的 树的子节点，根据 ch
  // 找过来的时候，也是会找到这里的

  // 以下的代码解释的均是左旋时的情况
  Node *tmp = cur->ch[dir];  // 让 C 变成根节点，
                             // 这里的 tmp
                             // 是一个临时的节点指针，指向成为新的根节点的节点

  /* 左旋：也就是让右子节点变成根节点
   *         A                 C
   *        / \               / \
   *       B  C    ---->     A   E
   *         / \            / \
   *        D   E          B   D
   */
  cur->ch[dir] = tmp->ch[!dir];    // 让 A 的右子节点变成 D
  tmp->ch[!dir] = cur;             // 让 C 的左子节点变成 A
  cur->upd_siz(), tmp->upd_siz();  // 更新大小信息
  cur = tmp;  // 最后把临时储存 C 树的变量赋值到当前根节点上（注意 cur 是引用）
}
```

### 插入

类似普通二叉搜索树的插入，但是需要在插入的过程中通过旋转来维护优先级的堆性质．

```cpp
void _insert(Node *&cur, int val) {
  if (cur == nullptr) {
    // 没这个节点直接新建
    cur = new Node(val);
    return;
  } else if (val == cur->val) {
    // 如果有这个值相同的节点，就把重复数量加一
    cur->rep_cnt++;
    cur->siz++;
  } else if (val < cur->val) {
    // 维护搜索树性质，val 比当前节点小就插到左边，反之亦然
    _insert(cur->ch[0], val);
    if (cur->ch[0]->rank < cur->rank) {
      // 小根堆中，上面节点的优先级一定更小
      // 因为新插的左子节点比父节点小，现在需要让左子节点变成父节点
      _rotate(cur, RT);  // 注意前面的旋转性质，要把左子节点转上来，需要右旋
    }
    cur->upd_siz();  // 插入之后大小会变化，需要更新
  } else {
    _insert(cur->ch[1], val);
    if (cur->ch[1]->rank < cur->rank) {
      _rotate(cur, LF);
    }
    cur->upd_siz();
  }
}
```

### 删除

主要就是分类讨论，不同的情况有不同的处理方法，删完了树的大小会有变化，要注意更新．并且如果要删的节点有左子树和右子树，就要考虑删除之后让谁来当父节点（维护 rank 小的节点在上面）．

```cpp
void _del(Node *&cur, int val) {
  if (val > cur->val) {
    _del(cur->ch[1], val);
    // 值更大就在右子树，反之亦然
    cur->upd_siz();
  } else if (val < cur->val) {
    _del(cur->ch[0], val);
    cur->upd_siz();
  } else {
    if (cur->rep_cnt > 1) {
      // 如果要删除的节点是重复的，可以直接把重复值减小
      cur->rep_cnt--, cur->siz--;
      return;
    }
    uint8_t state = 0;
    state |= (cur->ch[0] != nullptr);
    state |= ((cur->ch[1] != nullptr) << 1);
    // 00都无，01有左无右，10，无左有右，11都有
    Node *tmp = cur;
    switch (state) {
      case 0:
        delete cur;
        cur = nullptr;
        // 没有任何子节点，就直接把这个节点删了
        break;
      case 1:  // 有左无右
        cur = tmp->ch[0];
        // 把根变成左儿子，然后把原来的根节删了，注意这里的 tmp 是从 cur
        // 复制的，而 cur 是引用
        delete tmp;
        break;
      case 2:  // 有右无左
        cur = tmp->ch[1];
        delete tmp;
        break;
      case 3:
        rot_type dir = cur->ch[0]->rank < cur->ch[1]->rank
                           ? RT
                           : LF;  // dir 是 rank 更小的那个儿子
        _rotate(cur, dir);  // 这里的旋转可以把优先级更小的儿子转上去，rt 是 0，
                            // 而 lf 是 1，刚好跟实际的子树下标反过来
        _del(
            cur->ch[!dir],
            val);  // 旋转完成后原来的根节点就在旋方向那边，所以需要
                   // 继续把这个原来的根节点删掉
                   // 如果说要删的这个节点是在整个树的「上层的」，那我们会一直通过这
                   // 这里的旋转操作，把它转到没有子树了（或者只有一个），再删掉它．
        cur->upd_siz();
        // 删除会造成大小改变
        break;
    }
  }
}
```

### 根据值查询排名

操作含义：查询以 cur 为根节点的子树中，val 这个值的大小的排名（该子树中小于 val 的节点的个数 + 1）

```cpp
int _query_rank(Node *cur, int val) {
  int less_siz = cur->ch[0] == nullptr ? 0 : cur->ch[0]->siz;
  // 这个树中小于 val 的节点的数量
  if (val == cur->val)
    // 如果这个节点就是要查的节点
    return less_siz + 1;
  else if (val < cur->val) {
    if (cur->ch[0] != nullptr)
      return _query_rank(cur->ch[0], val);
    else
      return 1;  // 如果左子树是空的，说比最小的节点还要小，那这个数字就是最小的
  } else {
    if (cur->ch[1] != nullptr)
      // 如果要查的值比这个节点大，那这个节点的左子树以及这个节点自身肯定都比要查的值小
      // 所以要加上这两个值，再加上往右边找的结果
      // （以右子树为根的子树中，val 这个值的大小的排名）
      return less_siz + cur->rep_cnt + _query_rank(cur->ch[1], val);
    else
      return cur->siz + 1;
    // 没有右子树的话直接整个树 + 1 相当于 less_siz + cur->rep_cnt + 1
  }
}
```

### 根据排名查询值

要根据排名查询值，我们首先要知道如何判断要查的节点在树的哪个部分：

以下是一个判断方法的表：

| 左子树         | 根节点/当前节点                           | 右子树                    |
| ----------- | ---------------------------------- | ---------------------- |
| 排名 ≤ 左子树的大小 | 排名 > 左子树的大小，并且 ≤ 左子树的大小 + 根节点的重复次数 | 排名 > 左子树的大小 + 根节点的重复次数 |

注意如果在右子树，递归的时候需要对原来的 `rank` 进行处理．递归的时候就相当去查，在右子树中为这个排名的值，为了把排名转换成基于右子树的，需要把原来的 `rank` 减去左子树的大小和根节点的重复次数．

可以把所有节点想象成一个排好序的数组，或者数轴（如下），

    1 -> |左子树的节点|根节点|右子树的节点| -> n
                               ^
                               要查的排名
                         ⬇转换成基于右子树的排名
    1 -> |右子树的节点| -> n
           ^
           要查的排名

这里的转换方法就是直接把排名减去左子树的大小和根节点的重复数量．

```cpp
int _query_val(Node *cur, int rank) {
  // 查询树中第 rank 大的节点的值
  int less_siz = cur->ch[0] == nullptr ? 0 : cur->ch[0]->siz;
  // less siz 是左子树的大小
  if (rank <= less_siz)
    return _query_val(cur->ch[0], rank);
  else if (rank <= less_siz + cur->rep_cnt)
    return cur->val;
  else
    return _query_val(cur->ch[1], rank - less_siz - cur->rep_cnt);  // 见前文
}
```

### 查询第一个比 val 小的节点

注意这里使用了一个类中的全局变量，`q_prev_tmp`．

这个值是只有在 val 比当前节点值大的时候才会被更改的，所以返回这个变量就是返回 val 最后一次比当前节点的值大，之后就是更小了．

```cpp
int _query_prev(Node *cur, int val) {
  if (val <= cur->val) {
    // 还是比 val 大，所以往左子树找
    if (cur->ch[0] != nullptr) return _query_prev(cur->ch[0], val);
  } else {
    // 只有能进到这个 else 里，才会更新 q_prev_tmp 的值
    q_prev_tmp = cur->val;
    // 当前节点已经比 val，小了，但是不确定是否是最大的，所以要到右子树继续找
    if (cur->ch[1] != nullptr) _query_prev(cur->ch[1], val);
    // 接下来的递归可能不会更改 q_prev_tmp
    // 了，那就直接返回这个值，总之返回的就是最后一次进到 这个 else 中的
    // cur->val
    return q_prev_tmp;
  }
  return NIL;
}
```

### 查询第一个比 val 大的节点

跟前一个很相似，只是大于小于号换了一下．

```cpp
int _query_nex(Node *cur, int val) {
  if (val >= cur->val) {
    if (cur->ch[1] != nullptr) return _query_nex(cur->ch[1], val);
  } else {
    q_nex_tmp = cur->val;
    if (cur->ch[0] != nullptr) _query_nex(cur->ch[0], val);
    return q_nex_tmp;
  }
  return NIL;
}
```

## 无旋 treap

无旋 treap 的操作方式使得它天生支持维护序列、可持久化等特性．

**无旋 treap** 又称分裂合并 treap．它仅有两种核心操作，即为 **分裂** 与 **合并**．通过这两种操作，在很多情况下可以比旋转 treap 更方便的实现别的操作．下面逐一介绍这两种操作．

???+ note "注释"
    讲解无旋 treap 应当提到 **FHQ-Treap**（by 范浩强）．即可持久化，支持区间操作的无旋 Treap．更多内容请参照《范浩强谈数据结构》ppt．

### 分裂（split）

#### 按值分裂

分裂过程接受两个参数：根指针 $\textit{cur}$、关键值 $\textit{key}$．结果为将根指针指向的 treap 分裂为两个 treap，第一个 treap 所有结点的值（$\textit{val}$）小于等于 $\textit{key}$，第二个 treap 所有结点的值大于 $\textit{key}$．

该过程首先判断 $\textit{key}$ 是否小于 $\textit{cur}$ 的值，若小于，则说明 $\textit{cur}$ 及其右子树全部大于 $\textit{key}$，属于第二个 treap．当然，也可能有一部分的左子树的值大于 $\textit{key}$，所以还需要继续向左子树递归地分裂．对于大于 $\textit{key}$ 的那部分左子树，我们把它作为 $\textit{cur}$ 的左子树，这样，整个 $\textit{cur}$ 上的节点都是大于 $\textit{key}$ 的．

相应的，如果 $\textit{key}$ 大于等于 $\textit{cur}$ 的值，说明 $\textit{cur}$ 的整个左子树以及其自身都小于等于 $\textit{key}$，属于分裂后的第一个 treap．并且，$\textit{cur}$ 的部分右子树也可能有部分小于等于 $\textit{key}$，因此我们需要继续递归地分裂右子树．把小于等于 $\textit{key}$ 的那部分作为 $\textit{cur}$ 的右子树，这样，整个 $\textit{cur}$ 上的节点都小于等于 $\textit{key}$．

下图展示了 $\textit{cur}$ 的值小于等于 $\textit{key}$ 时按值分裂的情况．[^ref1]

![按值分裂](./images/treap-none-rot-split-by-val.svg)

```cpp
pair<Node *, Node *> split(Node *cur, int key) {
  if (cur == nullptr) return {nullptr, nullptr};
  if (cur->val <= key) {
    // cur 以及它的左子树一定属于分裂后的第一个树
    auto temp = split(cur->ch[1], key);
    // 但是它可能有部分右子树也比 key 小
    cur->ch[1] = temp.first;
    // 我们把小于 key 的那部分拿出来，作为 cur 的右子树，这样整个 cur 都是小于
    // key 的 剩下的那部分右子树成为分裂后的第二个 treap
    cur->upd_siz();
    // 分裂过后树的大小会变化，需要更新
    return {cur, temp.second};
  } else {
    // 同上
    auto temp = split(cur->ch[0], key);
    cur->ch[0] = temp.second;
    cur->upd_siz();
    return {temp.first, cur};
  }
}
```

#### 按排名分裂

比起按值分裂，这个操作更像是旋转 treap 中的根据排名（某个节点的排名是树中所有小于此节点值的节点的数量 $+ 1$）查询值：

此函数接受两个参数，节点指针 $\textit{cur}$ 和排名 $\textit{rk}$，返回分裂后的三个 treap．

其中，第一个 treap 中每个节点的排名都小于 $\textit{rk}$，第二个的排名等于 $\textit{rk}$，并且第二个 treap 只有一个节点（不可能有多个等于的，如果有的话会增加 `Node` 结构体中的 `cnt`），第三个则是大于．

此操作的重点在于判断排名和 $\textit{cur}$ 相等的节点在树的哪个部分，这也是旋转 treap 根据排名查询值操作时的重要部分，在前文有非常详细的解释，这里不过多讲解．

并且，此操作的递归部分和按值分裂也非常相似，这里不赘述．

```cpp
tuple<Node *, Node *, Node *> split_by_rk(Node *cur, int rk) {
  if (cur == nullptr) return {nullptr, nullptr, nullptr};
  int ls_siz = cur->ch[0] == nullptr ? 0 : cur->ch[0]->siz;
  if (rk <= ls_siz) {
    // 排名和 cur 相等的节点在左子树
    Node *l, *mid, *r;
    tie(l, mid, r) = split_by_rk(cur->ch[0], rk);
    cur->ch[0] = r;  // 返回的第三个 treap 中的排名都大于 rk
    // cur 的左子树被设成 r 后，整个 cur 中节点的排名都大于 rk
    cur->upd_siz();
    return {l, mid, cur};
  } else if (rk <= ls_siz + cur->cnt) {
    // 和 cur 相等的就是当前节点
    Node *lt = cur->ch[0];
    Node *rt = cur->ch[1];
    cur->ch[0] = cur->ch[1] = nullptr;
    // 分裂后第二个 treap 只有一个节点，所有要把它的子树设置为空
    return {lt, cur, rt};
  } else {
    // 排名和 cur 相等的节点在右子树
    // 递归过程同上
    Node *l, *mid, *r;
    tie(l, mid, r) = split_by_rk(cur->ch[1], rk - ls_siz - cur->cnt);
    cur->ch[1] = l;
    cur->upd_siz();
    return {cur, mid, r};
  }
}
```

### 合并（merge）

合并过程接受两个参数：左 treap 的根指针 $\textit{u}$、右 treap 的根指针 $\textit{v}$．必须满足 $\textit{u}$ 中所有结点的值小于等于 $\textit{v}$ 中所有结点的值．一般来说，我们合并的两个 treap 都是原来从一个 treap 中分裂出去的，所以不难满足 $\textit{u}$ 中所有节点的值都小于 $\textit{v}$

在旋转 treap 中，我们借助旋转操作来维护 $\textit{priority}$ 符合堆的性质，同时旋转时还不能改变树的性质．在无旋 treap 中，我们用合并达到相同的效果．

因为两个 treap 已经有序，所以我们在合并的时候只需要考虑把哪个树「放在上面」，把哪个「放在下面」，也就是需要判断将哪个一个树作为子树．显然，根据堆的性质，我们需要把 $\textit{priority}$ 小的放在上面（这里采用小根堆）．

同时，我们还需要满足搜索树的性质，所以若 $\textit{u}$ 的根结点的 $\textit{priority}$ 小于 $\textit{v}$ 的，那么 $\textit{u}$ 即为新根结点，并且 $\textit{v}$ 因为值比 $\textit{u}$ 更大，应与 $\textit{u}$ 的右子树合并；反之，则 $\textit{v}$ 作为新根结点，然后因为 $u$ 的值比 $\textit{v}$ 小，与 $v$ 的左子树合并．

```cpp
Node *merge(Node *u, Node *v) {
  // 传进来的两个树的内部已经符合搜索树的性质了
  // 并且 u 内所有节点的值 < v 内所有节点的值
  // 所以在合并的时候需要维护堆的性质
  // 这里用的是小根堆
  if (u == nullptr && v == nullptr) return nullptr;
  if (u != nullptr && v == nullptr) return u;
  if (v != nullptr && u == nullptr) return v;

  if (u->prio < v->prio) {
    // u 的 prio 比较小，u应该作为父节点
    u->ch[1] = merge(u->ch[1], v);
    // 因为 v 比 u 大，所以把 v 作为 u 的右子树
    u->upd_siz();
    return u;
  } else {
    // v 比较小，v应该作为父节点
    v->ch[0] = merge(u, v->ch[0]);
    // u 比 v 小，所以递归时的参数是这样的
    v->upd_siz();
    return v;
  }
}
```

### 插入

在无旋 treap 中，插入，删除，根据值查询排名等基础操作既可以用普通二叉查找树的方法实现，也可以用分裂和合并来实现．通常来说，使用分裂和合并来实现更加简洁，但是速度会慢一点[^ref2]．为了帮助更好的理解无旋 treap，下面的操作全部使用分裂和合并实现．

在实现插入操作时，我们利用了分裂操作的一些性质．也就是值小于等于 $\textit{val}$ 的节点会被分到第一个 treap．

所以，假设我们根据 $\textit{val}$ 分裂当前这个 treap．会有下面两棵树，并符合以下条件：

$$
\begin{aligned}
T_1 &\le val\\
T_2 &> val
\end{aligned}
$$

其中 $T_1$ 表示分裂后所有被分到第一个 treap 的节点的集合，$T_2$ 则是第二个．

如果我们再按照 $\textit{val} - 1$ 继续分裂 $T_1$，那么会产生下面两棵树，并符合以下条件：

$$
\begin{gathered}
T_{1\ \text{left}} \le val - 1\\
T_{1\ \text{right}} > val - 1 \ \And \ T_{1\ \text{right}} \le val
\end{gathered}
$$

其中 $T_{1\ \text{left}}$ 表示 $T_1$ 分裂后所有被分到第一个 treap 的节点的集合，$T_{1\ \text{right}}$ 则是第二个．并且上面的式子中，后半部分的 $\And \ T_{1\ \text{right}} \le val$ 来自于 $T_1$ 所符合的条件 $T_1 \le val$．

不难发现，只要 $\textit{val}$ 和节点的值是一个整数（大多数使用场景下会使用整数）那么符合 $T_{1\ \text{right}}$ 条件的节点只有一个，也就是值等于 $\textit{val}$ 的节点．

在插入时，如果我们发现符合 $T_{1\ \text{right}}$ 的节点存在，那就可以直接增加重复次数，否则，就新开一个节点．

注意把树分裂好了还需要用合并操作把它「粘」回去，这样下次还能继续使用．并且，还需要注意合并操作的参数顺序是有要求的，第一个树的所有节点的值都需要小于第二个．

```cpp
void insert(int val) {
  auto temp = split(root, val);
  // 根据 val 的值把整个树分成两个
  // 注意 split 的实现，等于 val 的子树是在左子树的
  auto l_tr = split(temp.first, val - 1);
  // l_tr 的左子树 <= val - 1，如果有 = val 的节点，那一定在右子树
  Node *new_node;
  if (l_tr.second == nullptr) {
    // 没有这个节点就新开，否则直接增加重复次数．
    new_node = new Node(val);
  } else {
    l_tr.second->cnt++;
    l_tr.second->upd_siz();
  }
  Node *l_tr_combined =
      merge(l_tr.first, l_tr.second == nullptr ? new_node : l_tr.second);
  // 合并 T_1 left 和 T_1 right
  root = merge(l_tr_combined, temp.second);
  // 合并 T_1 和 T_2
}
```

### 删除

删除操作也使用和插入操作相似的方法，找到值和 $\textit{val}$ 相等的节点，并且删除它．

```cpp
void del(int val) {
  auto temp = split(root, val);
  auto l_tr = split(temp.first, val - 1);
  if (l_tr.second->cnt > 1) {
    // 如果这个节点的重复次数大于 1，减小即可
    l_tr.second->cnt--;
    l_tr.second->upd_siz();
    l_tr.first = merge(l_tr.first, l_tr.second);
  } else {
    if (temp.first == l_tr.second) {
      // 有可能整个 T_1 只有这个节点，所以也需要把这个点设成 null 来标注已经删除
      temp.first = nullptr;
    }
    delete l_tr.second;
    l_tr.second = nullptr;
  }
  root = merge(l_tr.first, temp.second);
}
```

### 根据值查询排名

排名是比这个值小的节点的数量 $+ 1$，所以我们根据 $\textit{val} - 1$ 分裂当前树，那么分裂后的第一个树就符合：

$$
T_1 \le val - 1
$$

如果树的值和 $\textit{val}$ 为整数，那么 $T_1$ 就包含了所有值小于 $\textit{val}$ 的节点．

```cpp
int qrank_by_val(Node* cur, int val) {
  auto temp = split(cur, val - 1);
  int ret = (temp.first == nullptr ? 0 : temp.first->siz) + 1;  // 根据定义 + 1
  root = merge(temp.first, temp.second);  // 拆好了再粘回去
  return ret;
}
```

### 根据排名查询值

调用 `split_by_rk()` 函数后，会返回分裂好的三个 treap，其中第二个只包含一个节点，它的排名等于 $\textit{rk}$，所以我们直接返回这个节点的 $\textit{val}$．

```cpp
int qval_by_rank(Node *cur, int rk) {
  Node *l, *mid, *r;
  tie(l, mid, r) = split_by_rk(cur, rk);
  int ret = mid->val;
  root = merge(merge(l, mid), r);
  return ret;
}
```

### 查询第一个比 val 小的节点

可以把这个问题转化为，在比 $\textit{val}$ 小的所有节点中，找出排名最大的．我们根据 $\textit{val}$ 来分裂这个 treap，返回的第一个 treap 中的节点的值就全部小于 $\textit{val}$，然后我们调用 `qval_by_rank()` 找出这个树中值最大的节点．

```cpp
int qprev(int val) {
  auto temp = split(root, val - 1);
  // temp.first 就是值小于 val 的子树
  int ret = qval_by_rank(temp.first, temp.first->siz);
  // 这里查询的是，所有小于 val 的节点里面，最大的那个的值
  root = merge(temp.first, temp.second);
  return ret;
}
```

### 查询第一个比 val 大的节点

和上个操作类似，可以把这个问题转化为，在比 $\textit{val}$ 大的所有节点中，找出排名最小的．那么根据 $\textit{val}$ 分裂后，返回的第二个 treap 中的所有节点的值就大于 $\textit{val}$．

然后我们去查询这个树中排名为 $1$ 的节点（也就是值最小的节点）的值，就可以成功查到第一个比 $\textit{val}$ 大的节点．

```cpp
int qnex(int val) {
  auto temp = split(root, val);
  int ret = qval_by_rank(temp.second, 1);
  // 查询所有大于 val 的子树里面，值最小的那个
  root = merge(temp.first, temp.second);
  return ret;
}
```

### 建树（build）

将一个有 $n$ 个节点的序列 $\{a_n\}$ 转化为一棵 treap．

可以依次暴力插入这 $n$ 个节点，每次插入一个权值为 $v$ 的节点时，将整棵 treap 按照权值分裂成权值小于等于 $v$ 的和权值大于 $v$ 的两部分，然后新建一个权值为 $v$ 的节点，将两部分和新节点按从小到大的顺序依次合并，单次插入时间复杂度 $O(\log n)$，总时间复杂度 $O(n\log n)$．

在某些题目内，可能会有多次插入一段有序序列的操作，这是就需要在 $O(n)$ 的时间复杂度内完成建树操作．

方法一：在递归建树的过程中，每次选取当前区间的中点作为该区间的树根，并对每个节点钦定合适的优先值，使得新树满足堆的性质．这样能保证树高为 $O(\log n)$．

方法二：在递归建树的过程中，每次选取当前区间的中点作为该区间的树根，然后给每个节点一个随机优先级．这样能保证树高为 $O(\log n)$，但不保证其满足堆的性质．这样也是正确的，因为无旋式 treap 的优先级是用来使 `merge` 操作更加随机一点，而不是用来保证树高的．

方法三：观察到 treap 是笛卡尔树，利用笛卡尔树的 $O(n)$ 建树方法即可，用单调栈维护右链即可．

### 无旋 treap 的区间操作

#### 建树

无旋 treap 相比旋转 treap 的一大好处就是可以实现各种区间操作，下面我们以文艺平衡树的 [模板题](https://loj.ac/problem/105) 为例，介绍 treap 的区间操作．

> 您需要写一种数据结构（可参考题目标题），来维护一个有序数列．
>
> 其中需要提供以下操作：翻转一个区间，例如原有序序列是 $5\ 4\ 3\ 2\ 1$，翻转区间是 $[2,4]$ 的话，结果是 $5\ 2\ 3\ 4\ 1$．
> 对于 $100\%$ 的数据，$1 \le n$（初始区间长度）$m$（翻转次数）$\le 10^5$

在这道题目中，我们需要实现的是区间翻转，那么我们首先需要考虑如何建树，建出来的树需要是初始的区间．

我们只需要把区间的下标依次插入 treap 中，这样在中序遍历（先遍历左子树，然后当前节点，最后右子树）时，就可以得到这个区间[^ref3]．

我们知道在朴素的二叉查找树中按照递增的顺序插入节点，建出来的树是一个长链，按照中序遍历，自然可以得到这个区间．

<div align=center>
  <img style="width: 50%; " src="../images/treap-search-tree-chain.svg" >
</div>

如上图，按照 $1\ 2\ 3\ 4\ 5$ 的顺序给朴素搜索树插入节点，中序遍历时，得到的也是 $1\ 2\ 3\ 4\ 5$．

但是在 treap 中，按增序插入节点后，在合并操作时还会根据 $\textit{priority}$ 调整树的结构，在这样的情况下，如何确保中序遍历一定能正确的输出呢？

可以参考 [笛卡尔树的单调栈建树方法](./cartesian-tree.md) 来理解这个问题．

设新插入的节点为 $\textit{u}$．

首先，因为是递增地插入节点，每一个新插入的节点肯定会被连接到 treap 的右链（即从根结点一直往右子树走，经过的结点形成的链）上．

从根节点开始，右链上的节点的 $\textit{priority}$ 是递增的（小根堆）．那我们可以找到右链上第一个 $\textit{priority}$ 大于 $\textit{u}$ 的节点，我们叫这个节点 $\textit{v}$，并把这个节点换成 $\textit{u}$．

因为 $\textit{u}$ 一定大于这个树上其他的全部节点，我们需要把 $\textit{v}$ 以及它的子树作为 $\textit{u}$ 的左子树．并且此时 $\textit{u}$ 没有右子树．

可以发现，中序遍历时 $\textit{u}$ 一定是最后一个被遍历到的（因为 $\textit{u}$ 是右链中的最后一个，而中序遍历中，右子树是最后被遍历到的）．

下图是一个 treap 根据递增顺序插入 $1 \sim 5$ 号节点时，插入 $5$ 号节点时的变化，可以用这张图更好的理解按照增序插入的过程．

![插入结点](./images/treap-none-rot-seg-build.svg)

#### 区间翻转

翻转 $[l, r]$ 这个区间时，基本思路是将树分裂成 $[1, l - 1],\ [l, r],\ [r + 1, n]$ 三个区间，再对中间的 $[l, r]$ 进行翻转[^ref3]．

翻转的具体操作是把区间内的子树的每一个左，右子节点交换位置．如下图就展示了翻转上图中 treap 的 $[3, 4]$ 和 $[3, 5]$ 区间后的 treap．

![区间翻转](./images/treap-none-rot-seg-flip-ex.svg)

注意如果按照这个方法翻转，那么每次翻转 $[l, r]$ 区间时，就会有 $r - l$ 个节点会被交换位置，这样频繁的操作显然不能满足 $10^5$ 的数据范围，其 $O(n \times \log_2 n)$ 的单次翻转复杂度甚至不如暴力（因为我们除了需要花线性时间交换节点外，还需要在树中花费 $O(\log_2 n)$ 的时间找到需要交换的节点）．

再观察题目要求，可以发现因为只需要最后输出操作完的区间，所以并不需要每次都真的去交换．如此一来，便可以使用线段树中常用的懒标记（lazy tag）来优化复杂度．交换时，只需要在父节点打上标记，代表这个子树下的每个左右子节点都需要交换就行了．

在线段树中，我们一般在更新和查询时下传懒标记．这是因为，在更新和查询时，我们想要更新/查询的范围不一定和懒标记代表的范围重合，所以要先下传标记，确保查到和更新后的值是正确的．

在无旋 treap 中也是一样．具体操作时我们会把 treap 分裂成前文讲到的三个树，然后给中间的树打上懒标记后合并这三棵树．因为我们想要翻转的区间和懒标记代表的区间不一定重合，所以要在分裂时下传标记．并且，分裂和合并操作会造成每个节点及其懒标记所代表的节点发生变动，所以也需要在合并前下传懒标记．

换句话说，是当树的结构发生改变的时候，当我们进行分裂或合并操作时需要改变某一个点的左右儿子信息时之前，应该下放标记，而非之后，因为懒标记是需要下传给儿子节点的，但更改左右儿子信息之后若懒标记还未下放，则懒标记就丢失了下放的对象．[^ref4]

<!-- TODO: 可以加一张图解释为什么需要在分裂和合并时下传标记 -->

以下为代码讲解，代码参考了[^ref3]．

因为区间操作中大部分操作都和普通的无旋 treap 相同，所以这里只讲解和普通无旋 treap 不同的地方．

#### 下传标记

需要注意这里的懒标记代表需要把这个树中的每一个子节点交换位置．所以如果当前节点的子节点也有懒标记，那两次翻转就抵消了．如果子节点不需要翻转，那么这个懒标记就需要继续被下传到子节点上．

```cpp
// 这里这个 pushdown 是 Node 类的成员函数，其中 to_rev 是懒标记
void pushdown() {
  swap(ch[0], ch[1]);
  if (ch[0] != nullptr) ch[0]->to_rev ^= 1;
  if (ch[1] != nullptr) ch[1]->to_rev ^= 1;
  to_rev = false;
}

void check_tag() {
  if (to_rev) pushdown();
}
```

#### 分裂

注意在这个题目中，因为翻转操作，treap 中的 $\textit{val}$ 会不符合二叉搜索树的性质（见区间翻转部分的图），所以我们不能根据 $\textit{val}$ 来判断应该往左子树还是右子树递归．

所以这里的分裂跟普通无旋 treap 中的按排名分裂更相似，是根据当前树的大小判断往左还是右子树递归的，换言之，我们是按照开始时这个节点在树中的位置来判断的．

返回的第一个 treap 中节点的排名全部小于等于 $\textit{sz}$，而第二个 treap 中节点的排名则全部大于 $\textit{sz}$．

```cpp
#define siz(_) (_ == nullptr ? 0 : _->siz)

pair<Node*, Node*> split(Node* cur, int sz) {
  // 按照树的大小判断
  if (cur == nullptr) return {nullptr, nullptr};
  cur->check_tag();
  // 分裂前先下传
  if (sz <= siz(cur->ch[0])) {
    auto temp = split(cur->ch[0], sz);
    cur->ch[0] = temp.second;
    cur->upd_siz();
    return {temp.first, cur};
  } else {
    auto temp =
        split(cur->ch[1],
              sz - siz(cur->ch[0]) -
                  1);  // 这里的转换在有旋 treap 的 「根据排名查询值有讲」
    cur->ch[1] = temp.first;
    cur->upd_siz();
    return {cur, temp.second};
  }
}
```

#### 合并

唯一需要注意的是在合并前下传懒标记

```cpp
Node *merge(Node *sm, Node *bg) {
  // small, big
  if (sm == nullptr && bg == nullptr) return nullptr;
  if (sm != nullptr && bg == nullptr) return sm;
  if (sm == nullptr && bg != nullptr) return bg;
  sm->check_tag(), bg->check_tag();
  if (sm->prio < bg->prio) {
    sm->ch[1] = merge(sm->ch[1], bg);
    sm->upd_siz();
    return sm;
  } else {
    bg->ch[0] = merge(sm, bg->ch[0]);
    bg->upd_siz();
    return bg;
  }
}
```

#### 区间翻转

和前面介绍的一样，分裂出 $[1, l - 1],\ [l, r],\ [r + 1, n]$ 三个区间，然后对中间的区间打上标记后再合并．

```cpp
void seg_rev(int l, int r) {
  // 这里的 less 和 more 是相对于 l 的
  auto less = split(root, l - 1);
  // 所有小于等于 l - 1 的会在 less 的左子树
  auto more = split(less.second, r - l + 1);
  // 从 l 开始的前 r - l + 1 个元素的区间
  more.first->to_rev = true;
  root = merge(less.first, merge(more.first, more.second));
}
```

#### 中序遍历打印

要注意在打印时要下传标记．

```cpp
void print(Node* cur) {
  if (cur == nullptr) return;
  cur->check_tag();
  // 中序遍历 -> 先左子树，再自己，最后右子树
  print(cur->ch[0]);
  cout << cur->val << " ";
  print(cur->ch[1]);
}
```

## 完整代码

### 旋转 treap

#### 指针实现

??? note "完整代码"
    以下是前文讲解的代码的完整版本，是普通平衡树的模板代码．
    
    ```cpp
    // author: (ttzytt)[ttzytt.com]
    #include <cstdint>
    #include <cstdio>
    #include <cstdlib>
    using namespace std;
    
    struct Node {
      Node *ch[2];
      int val, rank;
      int rep_cnt;
      int siz;
    
      Node(int val) : val(val), rep_cnt(1), siz(1) {
        ch[0] = ch[1] = nullptr;
        rank = rand();
      }
    
      void upd_siz() {
        siz = rep_cnt;
        if (ch[0] != nullptr) siz += ch[0]->siz;
        if (ch[1] != nullptr) siz += ch[1]->siz;
      }
    };
    
    class Treap {
     private:
      Node *root;
    
      constexpr static int NIL = -1;  // 用于表示查询的值不存在
    
      enum rot_type { LF = 1, RT = 0 };
    
      int q_prev_tmp = 0, q_nex_tmp = 0;
    
      void _rotate(Node *&cur, rot_type dir) {  // 0为右旋，1为左旋
        Node *tmp = cur->ch[dir];
        cur->ch[dir] = tmp->ch[!dir];
        tmp->ch[!dir] = cur;
        cur->upd_siz(), tmp->upd_siz();
        cur = tmp;
      }
    
      void _insert(Node *&cur, int val) {
        if (cur == nullptr) {
          cur = new Node(val);
          return;
        } else if (val == cur->val) {
          cur->rep_cnt++;
          cur->siz++;
        } else if (val < cur->val) {
          _insert(cur->ch[0], val);
          if (cur->ch[0]->rank < cur->rank) {
            _rotate(cur, RT);
          }
          cur->upd_siz();
        } else {
          _insert(cur->ch[1], val);
          if (cur->ch[1]->rank < cur->rank) {
            _rotate(cur, LF);
          }
          cur->upd_siz();
        }
      }
    
      void _del(Node *&cur, int val) {
        if (val > cur->val) {
          _del(cur->ch[1], val);
          cur->upd_siz();
        } else if (val < cur->val) {
          _del(cur->ch[0], val);
          cur->upd_siz();
        } else {
          if (cur->rep_cnt > 1) {
            cur->rep_cnt--, cur->siz--;
            return;
          }
          uint8_t state = 0;
          state |= (cur->ch[0] != nullptr);
          state |= ((cur->ch[1] != nullptr) << 1);
          // 00都无，01有左无右，10，无左有右，11都有
          Node *tmp = cur;
          switch (state) {
            case 0:
              delete cur;
              cur = nullptr;
              break;
            case 1:  // 有左无右
              cur = tmp->ch[0];
              delete tmp;
              break;
            case 2:  // 有右无左
              cur = tmp->ch[1];
              delete tmp;
              break;
            case 3:
              rot_type dir = cur->ch[0]->rank < cur->ch[1]->rank ? RT : LF;
              _rotate(cur, dir);
              _del(cur->ch[!dir], val);
              cur->upd_siz();
              break;
          }
        }
      }
    
      int _query_rank(Node *cur, int val) {
        int less_siz = cur->ch[0] == nullptr ? 0 : cur->ch[0]->siz;
        if (val == cur->val)
          return less_siz + 1;
        else if (val < cur->val) {
          if (cur->ch[0] != nullptr)
            return _query_rank(cur->ch[0], val);
          else
            return 1;
        } else {
          if (cur->ch[1] != nullptr)
            return less_siz + cur->rep_cnt + _query_rank(cur->ch[1], val);
          else
            return cur->siz + 1;
        }
      }
    
      int _query_val(Node *cur, int rank) {
        int less_siz = cur->ch[0] == nullptr ? 0 : cur->ch[0]->siz;
        if (rank <= less_siz)
          return _query_val(cur->ch[0], rank);
        else if (rank <= less_siz + cur->rep_cnt)
          return cur->val;
        else
          return _query_val(cur->ch[1], rank - less_siz - cur->rep_cnt);
      }
    
      int _query_prev(Node *cur, int val) {
        if (val <= cur->val) {
          if (cur->ch[0] != nullptr) return _query_prev(cur->ch[0], val);
        } else {
          q_prev_tmp = cur->val;
          if (cur->ch[1] != nullptr) _query_prev(cur->ch[1], val);
          return q_prev_tmp;
        }
        return NIL;
      }
    
      int _query_nex(Node *cur, int val) {
        if (val >= cur->val) {
          if (cur->ch[1] != nullptr) return _query_nex(cur->ch[1], val);
        } else {
          q_nex_tmp = cur->val;
          if (cur->ch[0] != nullptr) _query_nex(cur->ch[0], val);
          return q_nex_tmp;
        }
        return NIL;
      }
    
     public:
      void insert(int val) { _insert(root, val); }
    
      void del(int val) { _del(root, val); }
    
      int query_rank(int val) { return _query_rank(root, val); }
    
      int query_val(int rank) { return _query_val(root, rank); }
    
      int query_prev(int val) { return _query_prev(root, val); }
    
      int query_nex(int val) { return _query_nex(root, val); }
    };
    
    Treap tr;
    
    int main() {
      srand(0);
      int t;
      scanf("%d", &t);
      while (t--) {
        int mode;
        int num;
        scanf("%d%d", &mode, &num);
        switch (mode) {
          case 1:
            tr.insert(num);
            break;
          case 2:
            tr.del(num);
            break;
          case 3:
            printf("%d\n", tr.query_rank(num));
            break;
          case 4:
            printf("%d\n", tr.query_val(num));
            break;
          case 5:
            printf("%d\n", tr.query_prev(num));
            break;
          case 6:
            printf("%d\n", tr.query_nex(num));
            break;
        }
      }
    }
    ```

#### 数组实现

以下是 bzoj 普通平衡树模板代码，使用数组实现．

??? note "完整代码"
    ```cpp
    --8<-- "docs/ds/code/treap/treap_1.cpp"
    ```

### 无旋 treap

#### 指针实现

??? note "完整代码"
    以下是前文讲解的代码的完整版本，是普通平衡树的模板代码．
    
    ```cpp
    
    // author: (ttzytt)[ttzytt.com]
    #include <cstdio>
    #include <cstdlib>
    #include <ctime>
    #include <tuple>
    using namespace std;
    
    struct Node {
      Node *ch[2];
      int val, prio;
      int cnt;
      int siz;
    
      Node(int _val) : val(_val), cnt(1), siz(1) {
        ch[0] = ch[1] = nullptr;
        prio = rand();
      }
    
      Node(Node *_node) {
        val = _node->val, prio = _node->prio, cnt = _node->cnt, siz = _node->siz;
      }
    
      void upd_siz() {
        siz = cnt;
        if (ch[0] != nullptr) siz += ch[0]->siz;
        if (ch[1] != nullptr) siz += ch[1]->siz;
      }
    };
    
    struct none_rot_treap {
    #define _3 second.second
    #define _2 second.first
      Node *root;
    
      pair<Node *, Node *> split(Node *cur, int key) {
        if (cur == nullptr) return {nullptr, nullptr};
        if (cur->val <= key) {
          auto temp = split(cur->ch[1], key);
          cur->ch[1] = temp.first;
          cur->upd_siz();
          return {cur, temp.second};
        } else {
          auto temp = split(cur->ch[0], key);
          cur->ch[0] = temp.second;
          cur->upd_siz();
          return {temp.first, cur};
        }
      }
    
      tuple<Node *, Node *, Node *> split_by_rk(Node *cur, int rk) {
        if (cur == nullptr) return {nullptr, nullptr, nullptr};
        int ls_siz = cur->ch[0] == nullptr ? 0 : cur->ch[0]->siz;
        if (rk <= ls_siz) {
          Node *l, *mid, *r;
          tie(l, mid, r) = split_by_rk(cur->ch[0], rk);
          cur->ch[0] = r;
          cur->upd_siz();
          return {l, mid, cur};
        } else if (rk <= ls_siz + cur->cnt) {
          Node *lt = cur->ch[0];
          Node *rt = cur->ch[1];
          cur->ch[0] = cur->ch[1] = nullptr;
          return {lt, cur, rt};
        } else {
          Node *l, *mid, *r;
          tie(l, mid, r) = split_by_rk(cur->ch[1], rk - ls_siz - cur->cnt);
          cur->ch[1] = l;
          cur->upd_siz();
          return {cur, mid, r};
        }
      }
    
      Node *merge(Node *u, Node *v) {
        if (u == nullptr && v == nullptr) return nullptr;
        if (u != nullptr && v == nullptr) return u;
        if (v != nullptr && u == nullptr) return v;
        if (u->prio < v->prio) {
          u->ch[1] = merge(u->ch[1], v);
          u->upd_siz();
          return u;
        } else {
          v->ch[0] = merge(u, v->ch[0]);
          v->upd_siz();
          return v;
        }
      }
    
      void insert(int val) {
        auto temp = split(root, val);
        auto l_tr = split(temp.first, val - 1);
        Node *new_node;
        if (l_tr.second == nullptr) {
          new_node = new Node(val);
        } else {
          l_tr.second->cnt++;
          l_tr.second->upd_siz();
        }
        Node *l_tr_combined =
            merge(l_tr.first, l_tr.second == nullptr ? new_node : l_tr.second);
        root = merge(l_tr_combined, temp.second);
      }
    
      void del(int val) {
        auto temp = split(root, val);
        auto l_tr = split(temp.first, val - 1);
        if (l_tr.second->cnt > 1) {
          l_tr.second->cnt--;
          l_tr.second->upd_siz();
          l_tr.first = merge(l_tr.first, l_tr.second);
        } else {
          if (temp.first == l_tr.second) {
            temp.first = nullptr;
          }
          delete l_tr.second;
          l_tr.second = nullptr;
        }
        root = merge(l_tr.first, temp.second);
      }
    
      int qrank_by_val(Node *cur, int val) {
        auto temp = split(cur, val - 1);
        int ret = (temp.first == nullptr ? 0 : temp.first->siz) + 1;
        root = merge(temp.first, temp.second);
        return ret;
      }
    
      int qval_by_rank(Node *cur, int rk) {
        Node *l, *mid, *r;
        tie(l, mid, r) = split_by_rk(cur, rk);
        int ret = mid->val;
        root = merge(merge(l, mid), r);
        return ret;
      }
    
      int qprev(int val) {
        auto temp = split(root, val - 1);
        int ret = qval_by_rank(temp.first, temp.first->siz);
        root = merge(temp.first, temp.second);
        return ret;
      }
    
      int qnex(int val) {
        auto temp = split(root, val);
        int ret = qval_by_rank(temp.second, 1);
        root = merge(temp.first, temp.second);
        return ret;
      }
    };
    
    none_rot_treap tr;
    
    int main() {
      srand(time(nullptr));
      int t;
      scanf("%d", &t);
      while (t--) {
        int mode;
        int num;
        scanf("%d%d", &mode, &num);
        switch (mode) {
          case 1:
            tr.insert(num);
            break;
          case 2:
            tr.del(num);
            break;
          case 3:
            printf("%d\n", tr.qrank_by_val(tr.root, num));
            break;
          case 4:
            printf("%d\n", tr.qval_by_rank(tr.root, num));
            break;
          case 5:
            printf("%d\n", tr.qprev(num));
            break;
          case 6:
            printf("%d\n", tr.qnex(num));
            break;
        }
      }
    }
    ```

### 无旋 treap 的区间操作

#### 指针实现

??? note "完整代码"
    以下是前文讲解的代码的完整版本，是文艺平衡树题目的模板代码．
    
    ```cpp
    
    // author: (ttzytt)[ttzytt.com]
    #include <cstdlib>
    #include <ctime>
    #include <iostream>
    using namespace std;
    
    // 参考：https://www.cnblogs.com/Equinox-Flower/p/10785292.html
    struct Node {
      Node* ch[2];
      int val, prio;
      int cnt;
      int siz;
      bool to_rev = false;  // 需要把这个子树下的每一个节点都翻转过来
    
      Node(int _val) : val(_val), cnt(1), siz(1) {
        ch[0] = ch[1] = nullptr;
        prio = rand();
      }
    
      int upd_siz() {
        siz = cnt;
        if (ch[0] != nullptr) siz += ch[0]->siz;
        if (ch[1] != nullptr) siz += ch[1]->siz;
        return siz;
      }
    
      void pushdown() {
        swap(ch[0], ch[1]);
        if (ch[0] != nullptr) ch[0]->to_rev ^= 1;
        // 如果原来子节点也要翻转，那两次翻转就抵消了，如果子节点不翻转，那这个
        //  tag 就需要继续被 push 到子节点上
        if (ch[1] != nullptr) ch[1]->to_rev ^= 1;
        to_rev = false;
      }
    
      void check_tag() {
        if (to_rev) pushdown();
      }
    };
    
    struct Seg_treap {
      Node* root;
    #define siz(_) (_ == nullptr ? 0 : _->siz)
    
      pair<Node*, Node*> split(Node* cur, int sz) {
        // 按照树的大小划分
        if (cur == nullptr) return {nullptr, nullptr};
        cur->check_tag();
        if (sz <= siz(cur->ch[0])) {
          // 左边的子树就够了
          auto temp = split(cur->ch[0], sz);
          // 左边的子树不一定全部需要，temp.second 是不需要的
          cur->ch[0] = temp.second;
          cur->upd_siz();
          return {temp.first, cur};
        } else {
          // 左边的加上右边的一部分（当然也包括这个节点本身）
          auto temp = split(cur->ch[1], sz - siz(cur->ch[0]) - 1);
          cur->ch[1] = temp.first;
          cur->upd_siz();
          return {cur, temp.second};
        }
      }
    
      Node* merge(Node* sm, Node* bg) {
        // small, big
        if (sm == nullptr && bg == nullptr) return nullptr;
        if (sm != nullptr && bg == nullptr) return sm;
        if (sm == nullptr && bg != nullptr) return bg;
        sm->check_tag(), bg->check_tag();
        if (sm->prio < bg->prio) {
          sm->ch[1] = merge(sm->ch[1], bg);
          sm->upd_siz();
          return sm;
        } else {
          bg->ch[0] = merge(sm, bg->ch[0]);
          bg->upd_siz();
          return bg;
        }
      }
    
      void insert(int val) {
        auto temp = split(root, val);
        auto l_tr = split(temp.first, val - 1);
        Node* new_node;
        if (l_tr.second == nullptr) new_node = new Node(val);
        Node* l_tr_combined =
            merge(l_tr.first, l_tr.second == nullptr ? new_node : l_tr.second);
        root = merge(l_tr_combined, temp.second);
      }
    
      void seg_rev(int l, int r) {
        // 这里的 less 和 more 是相对于 l 的
        auto less = split(root, l - 1);
        // 所有小于等于 l - 1 的会在 less 的左边
        auto more = split(less.second, r - l + 1);
        // 拿出从 l 开始的前 r - l + 1 个
        more.first->to_rev = true;
        root = merge(less.first, merge(more.first, more.second));
      }
    
      void print(Node* cur) {
        if (cur == nullptr) return;
        cur->check_tag();
        print(cur->ch[0]);
        cout << cur->val << " ";
        print(cur->ch[1]);
      }
    };
    
    Seg_treap tr;
    
    int main() {
      srand(time(nullptr));
      int n, m;
      cin >> n >> m;
      for (int i = 1; i <= n; i++) tr.insert(i);
      while (m--) {
        int l, r;
        cin >> l >> r;
        tr.seg_rev(l, r);
      }
      tr.print(tr.root);
    }
    ```

## 例题

[普通平衡树](https://loj.ac/problem/104)

[文艺平衡树（Splay）](https://loj.ac/problem/105)

[「ZJOI2006」书架](https://www.luogu.com.cn/problem/P2596)

[「NOI2005」维护数列](https://www.luogu.com.cn/problem/P2042)

[CF 702F T-Shirts](http://codeforces.com/problemset/problem/702/F)

## 参考资料与注释

[^ref1]: 本图的设计参考了 [维基百科 treap 词条的配图](https://en.wikipedia.org/wiki/Treap)

[^ref2]: <https://charleswu.site/archives/1051>

[^ref3]: <https://www.cnblogs.com/Equinox-Flower/p/10785292.html>

[^ref4]: <https://www.luogu.com.cn/blog/85514/fhq-treap-xue-xi-bi-ji>


## ds/tree-decompose.md

author: ouuan, Ir1d, Marcythm, Xeonacid

## 树分块的方式

可以参考 [真 - 树上莫队](../misc/mo-algo-on-tree.md)．

也可以参考 [ouuan 的博客/莫队、带修莫队、树上莫队详解/树上莫队](https://ouuan.github.io/莫队、带修莫队、树上莫队详解/#树上莫队)．

树上莫队同样可以参考以上两篇文章．

## 树分块的应用

树分块除了应用于莫队，还可以灵活地运用到某些树上问题中．但可以用树分块解决的题目往往都有更优秀的做法，所以相关的题目较少．

顺带提一句，「gty 的妹子树」的树分块做法可以被菊花图卡掉．

### [BZOJ4763 雪辉](https://hydro.ac/p/bzoj-P4763)

先进行树分块，然后对每个块的关键点，预处理出它到祖先中每个关键点的路径上颜色的 bitset，以及每个关键点的最近关键点祖先，复杂度是 $O(n\sqrt n+\frac{nc}{32})$，其中 $n\sqrt n$ 是暴力从每个关键点向上跳的复杂度，$\frac{nc}{32}$ 是把 $O(n)$ 个 `bitset` 存下来的复杂度．

回答询问的时候，先从路径的端点暴力跳到所在块的关键点，再从所在块的关键点一块一块地向上跳，直到 $lca$ 所在块，然后再暴力跳到 $lca$．关键点之间的 `bitset` 已经预处理了，剩下的在暴力跳的过程中计算．单次询问复杂度是 $O(\sqrt n+\frac c{32})$，其中 $\sqrt n$ 是块内暴力跳以及块直接向上跳的复杂度，$O(\frac c{32})$ 是将预处理的结果与暴力跳的结果合并的复杂度．数颜色个数可以用 `bitset` 的 `count()`，求 $\operatorname{mex}$ 可以用 `bitset` 的 `_Find_first()`．

所以，总复杂度为 $O((n+m)(\sqrt n+\frac c{32}))$．

??? note "参考代码"
    ```cpp
    --8<-- "docs/ds/code/tree-decompose/tree-decompose_1.cpp"
    ```

### [BZOJ4812 由乃打扑克](https://hydro.ac/p/bzoj-P4812)

这题和上一题基本一样，唯一的区别是得到 `bitset` 后如何计算答案．

~~由于 BZOJ 是计算所有测试点总时限，不好卡，所以可以用 `_Find_next()` 水过去．~~

正解是每 $16$ 位一起算，先预处理出 $2^{16}$ 种可能的情况高位连续 $1$ 的个数、低位连续 $1$ 的个数以及中间的贡献．只不过这样要手写 `bitset`，因为标准库的 `bitset` 不能取某 $16$ 位……

代码可以参考 [这篇博客](https://www.cnblogs.com/FallDream/p/bzoj4763.html)．


## ds/wblt.md

author: hsfzLZH1, cesonic, AtomAlpaca, caijianhong, Persdre, aofall, CoelacanthusHex, Marcythm, shuzhouliu, Tiphereth-A

## 引入

**Weight Balanced Leafy Tree**，下称 **WBLT**，是一种平衡树，比起其它平衡树主要有实现简单、常数小的优点．它支持区间操作，而且可持久化．

Weight Balanced Leafy Tree 顾名思义是 Weight Balanced Tree 和 Leafy Tree 的结合．

Weight Balanced Tree 的每个结点储存这个结点下子树的大小，并且通过保持左右子树的大小关系在一定范围来保证树高．

Leafy Tree 维护的原始信息仅存储在树的 **叶子节点** 上，而非叶子节点仅用于维护子节点信息和维持数据结构的形态．我们熟知的线段树就是一种 Leafy Tree．

![](images/leafy-tree-1.svg)

本文的树均指的是二叉的 Leafy Tree，即每个节点的子节点数目只能是 $0$ 或者 $2$．本文中的 $n$，指的是树的叶子节点的数目．叶子节点数目为 $n$ 的树，总的节点数量是 $2n-1$，因此，WBLT 占用的空间是 $\Theta(n)$ 的．

## 基本结构及平衡维护

本节介绍 WBLT 的基本结构，定义树的 $\alpha$‑平衡的概念，并解释如何通过旋转或合并的方式维护树的平衡．

### 节点信息

要实现一个基本的 WBLT，只需要记录每个节点的如下信息：

-   `lc[x]`、`rc[x]`：左、右子节点；
-   `sz[x]`：以 $x$ 为根的子树中的叶子节点的数目．

利用 WBLT 实现平衡树，还需要在每个节点处记录与键值相关的信息：

-   `val[x]`：节点 $x$ 处的键值．

因为只有叶子节点实际存储键值，所以其他节点处存储的信息是由它们的子节点合并得到的，以方便后续查询．

比如，一种常用的合并方式就是将两个子节点的键值中较大的那个存储于该节点．这样，每个节点存储的就是以它为根的子树中，所有叶子节点的键值的最大值．基于此，节点信息的更新方法如下：

???+ example "参考代码"
    ```cpp
    --8<-- "docs/ds/code/wblt/wblt-1.cpp:push-up"
    ```

当然，如果需要，还可以实现相应的 `push_down(x)` 函数．

### 辅助函数

除了基本的节点信息维护外，WBLT 通常还需要实现如下辅助函数，用于内存管理：

-   `new_node()`：新建节点；
-   `del_node(x)`：删除节点 $x$；
-   `new_leaf(v)`：新建以 $v$ 为键值的叶子节点；
-   `join(x, y)`：连接子树，即分别以 $x$、$y$ 为左右子节点，新建节点 $z$；
-   `cut(x)`：拆分子树，即获得节点 $x$ 的两个子节点，并删除节点 $x$．

如果 WBLT 的实现十分依赖于拆分和连接子树，会建立较多的新节点，并释放等量的旧节点．如果不及时回收旧的无用节点，会导致空间不再是线性的．以下是这些辅助函数的数组实现：

???+ example "参考代码"
    ```cpp
    --8<-- "docs/ds/code/wblt/wblt-1.cpp:helper"
    ```

封装好这些辅助函数后，数组实现和指针实现在后续函数中就没有区别了．

### 平衡的概念

对于一个树，可以定义它在一个非叶节点 $x$ 处的 **平衡度** 为

$$
\rho(x) = \dfrac{\min\{w(T_{\operatorname{left}(x)}),w(T_{\operatorname{right}(x)})\}}{w(T_x)}.
$$

其中，$T_x$ 表示以 $x$ 为根的子树，$w(\cdot)$ 表示子树的权重（它的叶子节点的数目），而 $\operatorname{left}(x)$ 和 $\operatorname{right}(x)$ 分别表示 $x$ 的左右叶子节点．特别地，叶子节点处规定 $\rho(x)=1/2$．

对于 $\alpha\in(0,1/2]$，如果某个节点 $x$ 处平衡度 $\rho(x)\ge\alpha$，就称该节点是 **$\alpha$‑平衡** 的．如果树的每个节点处都是 $\alpha$‑平衡的，就称树是 **$\alpha$‑平衡** 的．这样的树的集合记作 $BB[\alpha]$．一个树是 **$\alpha$‑平衡** 的，当且仅当它本身是 $\alpha$‑平衡的，且它的左右子树都是 $\alpha$‑平衡的或者它是叶子节点．

树是 $\alpha$‑平衡的，有一个显然的好处是，它的高度是 $O(\log n)$ 的．这是因为，从叶子节点每向根移动一步，子树所包含的叶子节点数目就至少扩大到原来的 $1/(1-\alpha)$ 倍，因此只能移动 $O(\log_{\frac{1}{1-\alpha}}n) = O(\log n)$ 次．这就保证了在 $\alpha$‑平衡的树中，单次查询的复杂度总是严格 $O(\log n)$ 的，且算法的常数与 $\log(1/(1-\alpha))$（以 $2$ 为底）正相关．当 $\alpha$ 位于下文提供的合理范围内时，这个常数大致为 $2\sim 3.5$．

WBLT 的平衡维护通常可以通过旋转或合并的方式进行．两种方式实现的 WBLT，单次插入、删除等操作，复杂度都是严格 $O(\log n)$ 的．但是，与固定优先级的 [Treap](./treap.md) 不同，WBLT 的结构并不具有唯一性，因此，两种方式维护得到的树的结构并不相同，虽然这并不影响它们的使用．当然，平衡的维护还可以采取类似 [替罪羊树](./sgt.md) 的策略，利用重构达到均摊 $O(\log n)$ 的复杂度，但是这样就失去了 WBLT 可持久化和区间操作等优势，因而并不推荐．

下文分别介绍了通过旋转和合并维护平衡的方法，并实现了相应的平衡维护和合并操作的函数．封装好这些函数后，两种维护树平衡的方式在后续具体的平衡树的实现中再无区别．而且，无论使用哪种方式，单次维护平衡的操作的时间复杂度都是 $O(1)$ 的，单次合并树 $T_1$ 和树 $T_2$ 的复杂度都是 $O\left(\left|\log\dfrac{w(T_1)}{w(T_2)}\right|\right)$ 的．

???+ info "省略权重的记号"
    为了维护树的平衡，只需要保留子树的权重信息．因此，为了表达方便，下面讨论平衡维护的两节将混用树和它的权重的记号．比如，子树 $x$ 的权重也由 $x$ 表示，而不是 $w(x)$．类似地，子树 $x$ 和 $y$ 合并得到的树也用它的权重表示，直接写作树 $x+y$．

### 通过旋转维护

WBLT 的旋转操作和 [Treap 的旋转操作](./treap.md#旋转) 完全相同，可以采取与 Treap 完全一致的旋转策略．当然，旋转本身同样可以看作是重新分配子树权重的过程，因此也可以利用拆分和连接子树完成．两种实现的结果是完全一致的，但是第二种实现更方便 WBLT 的持久化．

???+ example "参考代码"
    === "不依赖连接"
        ```cpp
        --8<-- "docs/ds/code/wblt/wblt-1.cpp:rotate-not-by-joining"
        ```
    
    === "依赖连接"
        ```cpp
        --8<-- "docs/ds/code/wblt/wblt-1.cpp:rotate-by-joining"
        ```

假设在某个树的修改操作后，正在自下而上地恢复树的平衡．现在，左右子树 $x$ 和 $y$ 不再平衡，但是它们自身都是平衡的．不妨设右子树 $y$ 过轻，即 $y<\alpha(x+y)$．此时，树的形态如图中左侧的树所示．

![](images/wblt-balance.svg)

一种朴素的平衡维护策略是将 $x$ 旋转到根节点处，这样它原先的右子节点 $w$ 就和 $y$ 一起成为了新树的右子节点，而它原先的左子节点 $z$ 成为了新树的左子节点．这相当于将原来的树左侧中 $w$ 的权重移动到它的右侧．如果 $w$ 的权重合适，这样的操作就可以恢复树的平衡．这样得到的树如图中右侧的树所示．

但是，如果 $w$ 本身过重，这样的操作可能移动了太多的权重到右子树，从而使得新树中左子树过轻，即 $z<\alpha(x+y)$．对于这种情形，因为子树 $z$ 和子树 $y$ 的权重都太小，只能考虑将 $w$ 分拆为两个子树，分别与 $z$ 和 $y$ 连接，成为新树的两个子树．这相当于首先将节点 $w$ 旋转到节点 $x$ 处，再将它旋转到根节点处．同样，可以期待这样得到的树能够达到平衡，形态如图中上方的树所示．

这两种旋转的策略分别称为单旋和双旋．单旋和双旋策略的选取，主要取决于子树 $w$ 相对于子树 $x$ 的比重，即存在阈值 $\beta$，使得

-   当 $w\le\beta x$ 时，应选取单旋策略；
-   当 $w>\beta x$ 时，应选取双旋策略．

难点在于阈值 $\beta$ 的选择，这就需要做一些具体的计算．Blum 和 Mehlhorn 证明了，对于参数[^wrong-range]

$$
\alpha\in\left(\dfrac{2}{11},1-\dfrac{\sqrt{2}}{2}\right]\approx(0.182,0.292],~\beta=\frac{1}{2-\alpha},
$$

能够通过上述单旋和双旋结合的策略，维护因为单次插入或删除而失衡的 WBLT 的平衡．

??? note "证明"
    需要证明的是，如果树在单次插入或删除后失衡，可以通过上述策略恢复它的平衡．结合上述图示，令
    
    $$
    \rho_1 = \dfrac{y}{x+y}, ~\rho_2 = \dfrac{w}{x}, ~\rho_3 = \dfrac{v}{w}.
    $$
    
    那么，有 $\rho_1<\alpha\le\rho_2,\rho_3\le 1-\alpha$．此处还有一个隐含条件，是关于 $\rho_1$ 的取值范围的：
    
    -   如果失衡是由插入单个元素引起的，那么，应该有
    
        $$
        \dfrac{y}{x-1+y} \ge \alpha \implies \rho_1 \ge \dfrac{\alpha y}{y+\alpha} \ge \dfrac{\alpha}{1+\alpha}.
        $$
    -   如果失衡是由删除单个元素引起的，那么，应该有
    
        $$
        \dfrac{y+1}{x+y+1} \ge \alpha \implies \rho_1 \ge \dfrac{\alpha y}{y+1-\alpha} \ge \dfrac{\alpha}{2-\alpha}.
        $$
    
    因为对于 $0<\alpha<1/2$，总有 $\alpha/(2-\alpha)<\alpha/(1+\alpha)$，所以删除元素会导致比增添元素更严重的失衡，尤其是对于树的规模很小的情形．
    
    接下来，恢复平衡的操作分为两种情形：
    
    ??? note "情形一：$w$ 没有过重，即 $\rho_2\le\beta$ 时，单旋"
        首先，$z$ 和 $w+y$ 平衡．这是因为
        
        $$
        \left(1-\dfrac{\alpha}{2-\alpha}\right)\alpha+\dfrac{\alpha}{2-\alpha} \le \dfrac{w+y}{x+y} = (1-\rho_1)\rho_2+\rho_1 < (1-\alpha)\dfrac{1}{2-\alpha}+\alpha.
        $$
        
        左侧表达式在 $\alpha\in(0,1)$ 时总大于 $\alpha$，右侧表达式在 $\alpha\in(0,1-\sqrt{2}/2]$ 时总不大于 $(1-\alpha)$．
        
        其次，$w$ 和 $y$ 平衡．同样地，考虑
        
        $$
        \dfrac{y}{w+y} = \dfrac{\rho_1}{(1-\rho_1)\rho_2+\rho_1}.
        $$
        
        一方面，对于所有 $\alpha\in(0,(3-\sqrt{5})/2)$，有
        
        $$
        \dfrac{y}{w+y} < \dfrac{\alpha}{(1-\alpha)\alpha+\alpha} < 1-\alpha.
        $$
        
        另一方面，对于所有 $\alpha\in(0,1/3)$，除了删除元素且 $y=1$ 的情形外，都有
        
        $$
        \rho_1 \ge \min\left\{\dfrac{\alpha}{1+\alpha},\dfrac{2\alpha}{3-\alpha}\right\} = \dfrac{2\alpha}{3-\alpha},
        $$
        
        所以，有
        
        $$
        \dfrac{y}{w+y} \ge \dfrac{\dfrac{2\alpha}{3-\alpha}}{\left(1-\dfrac{2\alpha}{3-\alpha}\right)\dfrac{1}{2-\alpha}+\dfrac{2\alpha}{3-\alpha}} > \alpha.
        $$
        
        最后，考虑剩余的情形，即删除元素且 $y=1$ 时．最可能失衡的情形发生在 $x=\lfloor 2/\alpha\rfloor-2$ 且 $w=\lfloor\beta x\rfloor$ 时．树可以恢复平衡，当且仅当
        
        $$
        \dfrac{1}{1+\lfloor\beta x\rfloor}\ge\alpha \iff \lfloor\beta x\rfloor\le\dfrac{1}{\alpha}-1 \iff \beta x < \dfrac{1}{\alpha} \iff x < \dfrac{2}{\alpha}-1.
        $$
        
        而这总是成立的．这就完成了该情形的证明．注意，最后一种情形的证明利用了权重总是整数这一性质，并不能合并到之前的讨论中．
    
    ??? note "情形二：$w$ 过重，即 $\rho_2>\beta$ 时，双旋"
        首先，$z+u$ 和 $v+y$ 平衡．这是因为
        
        $$
        \dfrac{\alpha}{2-\alpha}+\left(1-\dfrac{\alpha}{2-\alpha}\right)\dfrac{1}{2-\alpha}\alpha < \dfrac{z+u}{x+y} = \rho_1+(1-\rho_1)\rho_2\rho_3 <\alpha+(1-\alpha)^3
        $$
        
        左侧表达式在 $\alpha\in(0,1)$ 时总大于 $\alpha$，右侧表达式在 $\alpha\in(0,(3-\sqrt{5})/2)$ 时总小于 $(1-\alpha)$．
        
        然后，$z$ 和 $u$ 平衡．这是因为对于 $\alpha\in(0,1)$，总是成立
        
        $$
        \alpha=\dfrac{\dfrac{1}{2-\alpha}\alpha}{1-\dfrac{1}{2-\alpha}(1-\alpha)}<\dfrac{u}{z} = \dfrac{\rho_2(1-\rho_3)}{1-\rho_2\rho_3} <\dfrac{(1-\alpha)^2}{1-(1-\alpha)\alpha} < 1-\alpha.
        $$
        
        最后，$v$ 和 $y$ 平衡．类似其他的情形，考虑
        
        $$
        \dfrac{y}{v+y} = \dfrac{\rho_1}{\rho_1+(1-\rho_1)\rho_2\rho_3}.
        $$
        
        一方面，对于所有 $\alpha\in(0,1-\sqrt{2}/2]$，都有
        
        $$
        \dfrac{y}{v+y} < \dfrac{\alpha}{\alpha+(1-\alpha)\dfrac{1}{2-\alpha}\alpha} \le 1-\alpha.
        $$
        
        另一方面，
        
        $$
        \dfrac{y}{v+y} \ge \dfrac{\rho_1}{\rho_1+(1-\rho_1)(1-\alpha)^2}.
        $$
        
        右侧表达式不小于 $\alpha$，当且仅当
        
        $$
        \rho_1 \ge \dfrac{\alpha(1-\alpha)}{1+\alpha(1-\alpha)}.
        $$
        
        如果失衡是由插入引起的，那么 $\rho_1\ge \alpha/(1+\alpha)$，显然成立．否则，情形有些复杂：
        
        -   当 $y\ge 3$ 时，$\rho_1\ge 3\alpha/(4-\alpha)$，且 $3\alpha/(4-\alpha)\ge\alpha(1-\alpha)/(1+\alpha(1-\alpha))$ 对于所有 $\alpha\in[1-\sqrt{3}/2,1)$ 都成立；
        -   当 $y=2$ 时，最可能失衡的情形发生在 $x=\lfloor 3/\alpha\rfloor-3$，$w=\lfloor(1-\alpha)x\rfloor$ 且 $v=\lfloor(1-\alpha)w\rfloor$ 时，此时 $v/(v+y)\ge\alpha$ 对于所有 $\alpha\in(3/22,1)$ 都成立；
        -   当 $y=1$ 时，最可能失衡的情形发生在 $x=\lfloor 2/\alpha\rfloor-2$，$w=\lfloor(1-\alpha)x\rfloor$ 且 $v=\lfloor(1-\alpha)w\rfloor$ 时，此时 $v/(v+y)\ge\alpha$ 对于所有 $\alpha\in(2/11,1)$ 都成立．
        
        最后两种情形的讨论，同样利用了所有节点的权重都是整数这一点．
    
    综合两种情形，当 $\alpha\in(2/11,1-\sqrt{2}/2]$ 时，前述单旋和双旋结合的策略可以保证树的平衡．
    
    从这个分析过程中可以看出，最难保持平衡的情形发生在从小规模的树中删除节点时．除了 $\beta=1/(2-\alpha)$ 之外，对于其他参数的选择的正确性证明，同样可以重复上述的过程，只是用到的一些不等式需要相应地调整．

随后，Hirai 和 Yamamoto 通过机器证明完整地确定了所有可行的 $(\alpha,\beta)$ 的范围，结果是一个相当复杂的二维图形：

![](images/wblt-param-range.svg)

他们在文章中推荐使用如下策略维持平衡：

-   当 $x>3y$ 时，判断失衡；
-   当 $w\le 2z$ 时，选取单旋策略，否则，选取双旋策略．

原因是，这是可行的参数范围内唯一可以用简单整数表示的策略，从而避免了浮点数运算造成的效率损失．他们推荐的策略相当于取 $(\alpha,\beta)=(1/4,2/3)$．实践中，可以根据具体情况，选择合适的参数．

参考实现如下：

???+ example "参考代码"
    ```cpp
    --8<-- "docs/ds/code/wblt/wblt-1.cpp:too-heavy"
    --8<-- "docs/ds/code/wblt/wblt-1.cpp:balance"
    ```

实现了维护平衡的策略后，合并两树的算法就非常简单．仍然设 $x>y$，合并的策略如下：

-   如果右子树 $y$ 是空的，直接返回左子树 $x$；
-   如果左右子树 $x$ 和 $y$ 已经平衡，即 $y\ge\alpha(x+y)$，直接连接两子树；
-   否则，将 $x$ 的右子树 $w$ 与 $y$ 合并，将左子树 $z$ 与它们合并的结果连接，并调整新树的平衡．

参考实现如下：

???+ example "参考代码"
    ```cpp
    --8<-- "docs/ds/code/wblt/wblt-1.cpp:merge-by-balancing"
    ```

可以证明，这样可以维持合并后树的平衡，且这样操作的复杂度是 $O(|\log(x/y)|)$ 的．

??? note "平衡和复杂度的证明"
    只需要考虑 $y$ 过轻的情形，即 $y<\alpha(x+y)$．此时，先合并 $w$ 和 $y$，再连接 $z$ 和 $w+y$．需要证明的是，只要在树根处调整树的平衡，就能够保证树的平衡．假设树 $w+y$ 的左、右子树分别是 $c$ 和 $d$，且 $c$ 的左、右子树分别是 $a$ 和 $b$．在树根处调整平衡，可以分为三种情形：
    
    ??? note "情形一：$z$ 和 $w+y$ 已经平衡，无需进一步调整，即 $z\ge\alpha(x+y)$"
        根据平衡的定义，子树 $z$ 和 $w+y$ 都是平衡的，且它们互相也是平衡的，那么整棵树也是平衡的．
    
    ??? note "情形二：$z$ 过轻且 $c$ 没有过重，可以通过单旋恢复平衡，即 $z<\alpha(x+y)$ 且 $c\le\beta(w+y)$"
        此时，因为 $z$ 和 $w$ 平衡，但 $y$ 相较于 $x = z+w$ 过轻，所以，子树 $z$ 的权重满足
        
        $$
        \alpha(1-\alpha)(x+y) <  \alpha(z+w) \le z \le \alpha(x+y) .
        $$
        
        而 $c$ 的权重则满足
        
        $$
        \alpha(w+y) \le c \le \beta(w+y).
        $$
        
        由此，$z$ 和 $c$ 互相平衡，只要
        
        $$
        \dfrac{\alpha}{1-\alpha}<\dfrac{1-\alpha}{\alpha}\alpha<\dfrac{c}{z}=\dfrac{w+y}{z}\dfrac{c}{w+y} < \dfrac{1-\alpha(1-\alpha)}{\alpha(1-\alpha)}\beta\le\dfrac{1-\alpha}{\alpha},
        $$
        
        这要求
        
        $$
        \beta\le \dfrac{(1-\alpha)^2}{1-\alpha(1-\alpha)}.
        $$
        
        以及 $z+c$ 和 $d$ 互相平衡，只要
        
        $$
        \alpha\le (1-\beta)(1-\alpha)\le \dfrac{d}{w+y}\dfrac{w+y}{x+y}  = \dfrac{d}{x+y} < \dfrac{d}{c+d} \le 1-\alpha,
        $$
        
        这要求
        
        $$
        \beta \le \dfrac{1-2\alpha}{1-\alpha}.
        $$
    
    ??? note "情形三：$z$ 过轻且 $c$ 过重，可以通过双旋恢复平衡，即 $z<\alpha(x+y)$ 且 $c>\beta(w+y)$"
        类似情形二，有
        
        $$
        \begin{aligned}
        \alpha(1-\alpha)(x+y) < z &\le \alpha(x+y),\\
        \beta(w+y)<c &\le (1-\alpha)(w+y),\\
        \alpha c\le a,b &\le (1-\alpha)c.
        \end{aligned}
        $$
        
        由此，$z$ 和 $a$ 互相平衡，只要
        
        $$
        \dfrac{\alpha}{1-\alpha}\le\dfrac{1-\alpha}{\alpha}\beta\alpha\le\dfrac{a}{z} = \dfrac{w+y}{z}\dfrac{a}{c+d} < \dfrac{1-\alpha(1-\alpha)}{\alpha(1-\alpha)}(1-\alpha)^2,
        $$
        
        这要求
        
        $$
        \beta\ge\dfrac{\alpha}{(1-\alpha)^2}.
        $$
        
        其次，$b$ 和 $d$ 互相平衡，只要
        
        $$
        \dfrac{\alpha}{1-\alpha}\le\dfrac{\beta}{1-\beta}\alpha \le \dfrac{b}{d} = \dfrac{c}{d}\dfrac{b}{c} \le \dfrac{1-\alpha}{\alpha}(1-\alpha) < \dfrac{1-\alpha}{\alpha},
        $$
        
        这要求
        
        $$
        \beta\ge\dfrac{1}{2-\alpha}.
        $$
        
        最后，$z+a$ 和 $b+d$ 互相平衡，只要
        
        $$
        \alpha<(1-\alpha)(1-(1-\alpha)^2)\le\frac{b+d}{x+y} = \dfrac{w+y}{x+y}\dfrac{b+d}{w+y} < (1-\alpha(1-\alpha))(1-\beta\alpha) \le 1-\alpha,
        $$
        
        这要求
        
        $$
        \beta\ge\dfrac{\alpha}{1-\alpha+\alpha^2}.
        $$
    
    综合三种情形，只要
    
    $$
    0<\alpha\le 1-\dfrac{\sqrt{2}}{2},~\dfrac{1}{2-\alpha}\le\beta\le\dfrac{1-2\alpha}{1-\alpha},
    $$
    
    就能保证合并后的树可以利用单旋和双旋结合的策略调整到平衡．这显然包含正文给出的参数范围．
    
    最后，简单说明一下该算法的复杂度为什么是 $O(|\log(x/y)|)$ 的．合并的流程中，如果 $y$ 相较于 $x$ 过轻，就尝试与 $x$ 的右子树合并，这个过程一直持续到以 $x$ 某个子孙节点为根的子树与 $y$ 平衡为止．因为每向下加深一层，子树权重至少变为原来的 $(1-\alpha)$，所以至多只要 $\log_{\frac{1}{1-\alpha}}(x/y)$ 次迭代，就能找到与 $y$ 平衡的子树．因此，该合并算法调用 $O(\log n)$ 次平衡算法[^merge-complexity-cmp]，复杂度也就是 $O(\log n)$．
    
    虽然并不明显，但是这个论证过程依赖于这样一个结论：不断取右子树的过程中，$y$ 不会在一次迭代前后，从相较于左侧的子树过轻，变为相较于它过重．这是因为能够与 $y$ 平衡的子树权重范围位于 $\alpha y/(1-\alpha)$ 与 $(1-\alpha)y/\alpha$ 之间．因此，如果在一次迭代时，就从 $y$ 过轻变成 $y$ 过重，则 $x$ 的子树的权重在该次迭代过程中至少缩小到了原来的 $\alpha^2/(1-\alpha)^2$ 倍．但是，单次迭代，子树权重至多只能缩小到原来的 $\alpha$ 倍，但是在上述 $\alpha$ 的范围中，$\alpha>\alpha^2/(1-\alpha)^2$．这说明，前设情形是不可能的，某次迭代之后一定会有 $y$ 与 $x$ 的某个子树平衡的情形发生．

### 通过合并维护

合并两子树是指，保证左子树的键值总是不大于右子树的键值的情况下，建立新树，使其所有叶子节点的信息恰为左右子树叶子节点信息的并，且保证树的平衡．

为此，有如下策略[^more-join]：（仍然设 $x>y$）

-   如果右子树 $y$ 是空的，直接返回左子树 $x$；
-   如果左右子树 $x$ 和 $y$ 已经平衡，即 $y\ge\alpha(x+y)$，直接连接两子树；
-   否则，右子树 $y$ 过轻，但如果 $x$ 的左子树 $z$ 和 $w+y$ 可以平衡，即 $z\ge\alpha(x+y)$，就将 $w$ 和 $y$ 先合并，再合并 $z$ 和 $w+y$；
-   否则，$z$ 和 $y$ 都过轻，此时，需要首先合并 $z$ 和 $w$ 的左子树 $u$，再合并 $w$ 的右子树 $v$ 和 $y$，再将两次合并的结果 **合并** 为新树．

将这一策略与前文的平衡策略对比，可以看到后两种情形中节点的组合方式分别和前述平衡策略中单旋和双旋的结果相似，只是将子树的连接换作了合并．

可以证明，当

$$
0<\alpha \le 1-\dfrac{\sqrt{2}}{2}\approx 0.292
$$

时，这样得到的树总是平衡的，且这样操作的复杂度是 $O(|\log(x/y)|)$ 的．也就是说，合并两个树的成本，与两个树的绝对大小无关，而只与它们的相对大小有关．

??? note "平衡和复杂度的证明"
    设合并权重分别为 $x$ 和 $y$ 的两棵子树时，需要直接连接两棵子树的次数为 $\tau(x,y)$．严格来说，需要证明当 $0<\alpha\le 1-\sqrt{2}/2$ 时，存在常数 $C>0$，对于任意 $x>y>0$，都有
    
    $$
    \tau(x,y) \le 1+C\log^+\dfrac{\alpha x}{(1-\alpha)^2y},
    $$
    
    其中，$\log^+ x = \max\{0,\log x\}$；而且，对于所有 $x/y\le(1-\alpha)/\alpha$，都有 $\tau(x,y)=1$．实际上，式子中的常数可以取作
    
    $$
    C = -\dfrac{2}{\log(1-\alpha)}.
    $$
    
    这就说明了合并算法的复杂度是 $O(|\log(x/y)|)$ 的．
    
    为了证明合并算法得到的树总是平衡的，且上述复杂度的表达式成立，需要使用归纳法．对于所有第一象限的格点 $(x,y)\in\mathbf N^2_+$，可以赋以 $(x+y,|x-y|)$ 的字典序，这显然是该集合上的良序，可以沿着该顺序进行归纳．归纳起点是 $(x,y)=(1,1)$，此时，两子树都只有一个叶子节点，直接连接得到的子树必然是平衡的，且 $\tau(x,y)=1$，符合上式．下面假设归纳进行到 $(x,y)$，且结论对于所有 $(x,y)$ 之前的点都成立．这分为三种情形：
    
    ??? note "情形一：树 $x$ 和 $y$ 平衡，即 $y\ge\alpha(x+y)$"
        此时，直接连接得到树也是平衡的，且只调用树的连接算法一次，所以有 $\tau(x,y)=1$．
    
    ??? note "情形二：树 $y$ 过轻，但是 $z$ 并不过轻，即 $y<\alpha(x+y)\le z$"
        此时，首先合并 $w$ 和 $y$，然后合并 $z$ 和 $w+y$，所以
        
        $$
        \tau(x,y) = \tau(w,y) + \tau(z,w+y).
        $$
        
        由归纳假设，子树 $w+y$ 已经是平衡的．对于第二步合并，其实可以直接证明 $z$ 和 $w+y$ 是平衡的：
        
        $$
        \alpha \le \dfrac{z}{z+(w+y)} = \dfrac{z}{x+y} < \dfrac{z}{z+w} \le 1-\alpha.
        $$
        
        因此，合并 $z$ 和 $w+y$ 其实是直接连接两个子树，有 $\tau(z,w+y) = 1$．因此，最后得到的树也是平衡的．
        
        现在估计 $\tau(w,y)$ 的大小．因为 $y>(\alpha/(1-\alpha))x$ 且 $\alpha x\le w\le(1-\alpha)x$，所以，经放缩可知
        
        $$
        \dfrac{\alpha}{1-\alpha}<1-\alpha=\dfrac{\alpha x}{(\alpha/(1-\alpha))x}< \dfrac{w}{y} \le \dfrac{(1-\alpha)x}{y}.
        $$
        
        这说明，$w$ 和 $y$ 不平衡，只出现在 $w>y$ 时，所以，有
        
        $$
        \begin{aligned}
        \tau(w,y) &\le 1+C\log^+\dfrac{\alpha w}{(1-\alpha)^2y} \le 1+C\log^+\dfrac{\alpha x}{(1-\alpha)y} \\
        &= 1 + C\log(1-\alpha) + C\log^+\dfrac{\alpha x}{(1-\alpha)^2y}.
        \end{aligned}
        $$
        
        最后一步的等式成立，是因为 $x/y>(1-\alpha)/\alpha$．
        
        因此，有
        
        $$
        \tau(x,y) \le 2 + C\log(1-\alpha) + C\log^+\dfrac{\alpha x}{(1-\alpha)^2y}.
        $$
    
    ??? note "情形三：树 $y$ 和 $z$ 都过轻，即 $y,z<\alpha(x+y)$"
        此时，首先合并 $z$ 和 $u$，再合并 $v$ 和 $y$，最后合并 $z+u$ 和 $v+y$．因此，
        
        $$
        \tau(x,y) = \tau(z,u) + \tau(v,y) + \tau(z+u,v+y).
        $$
        
        类似前文情形，可以估计每一步合并时两个子树的权重比值．
        
        因为 $z,y<\alpha(x+y)$，所以 $w>(1-2\alpha)(x+y)$．同时，利用平衡条件，有 $\alpha\le z/x,w/x,u/w,v/w\le 1-\alpha$．这说明
        
        $$
        \begin{aligned}
        \dfrac{\alpha}{1-\alpha}<\dfrac{\alpha}{1-\alpha}\frac{1}{1-\alpha}\le \dfrac{z}{u} &= \dfrac{z}{w}\dfrac{w}{u} < \dfrac{\alpha}{1-2\alpha}\dfrac{1}{\alpha} \le \dfrac{1-\alpha}{\alpha},\\
        \dfrac{\alpha}{1-\alpha}\le\alpha\dfrac{1-2\alpha}{\alpha}< \dfrac{v}{y} &= \dfrac{v}{w}\dfrac{w}{y} \le (1-\alpha)\dfrac{(1-\alpha)x}{y} = (1-\alpha)^2\dfrac{x}{y}.
        \end{aligned}
        $$
        
        对于最后一项，有
        
        $$
        \dfrac{z+u}{v+y} = \dfrac{x+y}{v+y}-1 = \dfrac{x+y}{y}\dfrac{y}{v+y} - 1 < (1-\alpha)\left(\dfrac{x}{y}+1\right)-1 < (1-\alpha)\dfrac{x}{y}.
        $$
        
        反过来，有
        
        $$
        \dfrac{z+u}{v+y} = \dfrac{x+y}{v+y}-1 \ge \dfrac{x+y}{(1-\alpha)^2x+y}-1 > \dfrac{1}{(1-\alpha)^3+\alpha}-1 > \dfrac{\alpha}{1-\alpha}.
        $$
        
        利用这些不等式，可以说明最后得到的树必然是平衡的．利用归纳假设可知，$z$ 和 $u$ 合并，$v$ 和 $y$ 合并，都可以保证得到的树是平衡的．而且，其中第一步 $z$ 和 $u$ 合并实际上是直接连接两棵树．对于树 $z+u$ 和树 $v+y$ 的合并，又有两种子情形：
        
        -   如果 $z+u\le v+y$，那么它们的权重比值严格大于 $\alpha/(1-\alpha)$，故而可以直接连接，结果是平衡的；
        -   否则，它们的权重比值必然严格小于 $x/y$，但是 $(z+u)+(v+y)=x+y$，所以 $|(z+u)-(v+y)|<|x-y|$，由前文给出的字典序判断，这种情形也可以应用归纳假设，结果也是平衡的．
        
        进一步应用归纳假设可知：
        
        $$
        \begin{aligned}
        \tau(z,u) &= 1,\\
        \tau(v,y) &\le 1+C\log^+\dfrac{\alpha x}{y},\\
        \tau(z+u,v+y) &\le 1 + C\log^+\dfrac{\alpha x}{(1-\alpha)y}.
        \end{aligned}
        $$
        
        三个不等式直接相加，会导致对数项前面的系数变成 $2C$，无法完成归纳．因此，此处需要更为细致的估计．
        
        当 $\max\{v/y,(z+u)/(v+y)\}\le(1-\alpha)/\alpha$ 时，$\tau(v,y)$ 和 $\tau(z+u,v+y)$ 中必然有一项为 $1$，所以，有
        
        $$
        \begin{aligned}
        \tau(v,y) + \tau(z+u,v+y) &\le 2 + C\log^+\dfrac{\alpha x}{(1-\alpha)y}\\
        &= 2 + C\log(1-\alpha) + C\log^+\dfrac{\alpha x}{(1-\alpha)^2y}.
        \end{aligned}
        $$
        
        否则，应该有
        
        $$
        \begin{aligned}
        \tau(v,y) + \tau(z+u,v+y) 
        &\le 2 + C\log^+\dfrac{\alpha v}{(1-\alpha)^2y} + C\log^+\dfrac{\alpha(z+u)}{(1-\alpha)^2(v+y)}\\
        &= 2 + C\log\dfrac{\alpha}{(1-\alpha)^2} + C\log^+\dfrac{\alpha v(z+u)}{(1-\alpha)^2y(v+y)}.
        \end{aligned}
        $$
        
        对于 $0<\alpha\le 1-\sqrt{2}/2$，有
        
        $$
        \dfrac{\alpha}{(1-\alpha)^2} < 1-\alpha.
        $$
        
        而且，有
        
        $$
        \begin{aligned}
        \dfrac{v(z+u)}{y(v+y)} &= \left(\dfrac{v+y}{y}-1\right)\left(\dfrac{x+y}{y}\dfrac{y}{v+y} - 1\right) \\
        &= \dfrac{x+y}{y} + 1 -\dfrac{x+y}{y}\dfrac{y}{v+y}-\dfrac{v+y}{y} < \dfrac{x}{y}.
        \end{aligned}
        $$
        
        这就说明，对于后面这种情形，也有
        
        $$
        \tau(v,y) + \tau(z+u,v+y) < 2 + C\log(1-\alpha) + C\log^+\dfrac{\alpha x}{(1-\alpha)^2y}.
        $$
        
        整体的合并复杂度为
        
        $$
        \tau(x,y) \le 3 + C\log(1-\alpha) + C\log^+\dfrac{\alpha x}{(1-\alpha)^2y}.
        $$
    
    综合所有情形，有
    
    $$
    \tau(x,y) \le 3 + C\log(1-\alpha) + C\log^+\dfrac{\alpha x}{(1-\alpha)^2y}.
    $$
    
    因此，只要取 $2+C\log(1-\alpha)\le 0$，就可以完成复杂度的归纳．一个显然的选择为
    
    $$
    C = -\dfrac{2}{\log(1-\alpha)}.
    $$
    
    这个常数说明，两个树合并时，直接连接子树的次数大致不会超过树高差值的二倍．

参考实现如下：

???+ example "参考代码"
    ```cpp
    --8<-- "docs/ds/code/wblt/wblt-1.cpp:merge"
    ```

利用该合并策略，同样可以很容易实现树的平衡维护：失衡时，直接合并左右子树即可．

???+ example "参考代码"
    ```cpp
    --8<-- "docs/ds/code/wblt/wblt-1.cpp:balance-by-merging"
    ```

因为需要再平衡的两个树的大小总是近乎平衡的，因此维护平衡的复杂度是 $O(1)$ 的．

## 平衡树基础操作

利用前文实现的函数，WBLT 可以支持平衡树的所有基础操作．本节以可重集为例，讨论 WBLT 实现平衡树的方法．

### 建树

建树操作与线段树十分相似，只需要向下递归二分区间，直至区间长度为 $1$ 时把要维护的信息放叶子节点上，回溯的时候合并区间信息即可．

???+ example "参考代码"
    ```cpp
    --8<-- "docs/ds/code/wblt/wblt-2.cpp:build"
    ```

时间复杂度为 $O(n)$．

### 插入与删除

对于插入操作，需要从根节点开始向下递归，直到找到权值大于等于插入元素的权值最小的叶子节点，再新建两个节点，其中一个用来存储新插入的值，另一个作为两个叶子的新父亲替代这个最小叶子节点的位置，再将这两个叶子连接到这个父亲上．回溯时，需要维护树的平衡．

![](./images/wblt-insert-delete.svg)

如图所示，要向左侧的树中插入值为 $4$ 的元素．首先找到值为 $5$ 的叶子节点，然后新建叶子节点 $4$ 和非叶子节点 $\text{d}$，并将 $4$ 和 $5$ 连接到 $\text{d}$ 上．这就得到右侧的树．

对于删除，考虑上面过程的逆过程．即找到与要删除的值权值相等的一个叶子节点，将它和它的父亲节点删除，并用其父亲的另一个儿子代替父亲的位置．回溯时，同样需要维护树的平衡．

参考实现如下：

???+ example "参考代码"
    ```cpp
    --8<-- "docs/ds/code/wblt/wblt-1.cpp:insert-remove"
    ```

注意空树的处理．如果不想处理空树，可以提前向树内插入 $\infty$ 元素．

两种操作的时间复杂度均为 $O(\log n)$．

### 查询排名

因为 WBLT 的形态和线段树十分相似，因此查询排名可以使用类似线段树上二分的方式：如果左子树的最大值大于等于待查值就往左子节点跳；否则，就向右子节点跳，同时答案加上左子树的权重．

参考实现如下：

???+ example "参考代码"
    ```cpp
    --8<-- "docs/ds/code/wblt/wblt-1.cpp:rank"
    ```

时间复杂度为 $O(\log n)$．

### 根据排名查询

依然是利用线段树上二分的思想，只不过这里比较的是节点的权重．

参考实现如下：

???+ example "参考代码"
    ```cpp
    --8<-- "docs/ds/code/wblt/wblt-1.cpp:kth-element"
    ```

时间复杂度为 $O(\log n)$．

### 查找前驱、后继

以上两种功能结合即可．

参考实现如下：

???+ example "参考代码"
    ```cpp
    --8<-- "docs/ds/code/wblt/wblt-1.cpp:prev-next"
    ```

如果想直接实现，需要注意键值相同的节点可能存储于多个叶子节点．

### 分裂操作

WBLT 的分裂与 [无旋 Treap](./treap.md#分裂split) 类似，根据子树大小或权值决定向下递归分裂左子树或右子树．不同的是，WBLT 需要对分裂出来的子树进行 **合并**，以维护最终分裂的树的平衡．

根据子树大小分裂的参考实现如下：

???+ example "参考代码"
    ```cpp
    --8<-- "docs/ds/code/wblt/wblt-2.cpp:split"
    ```

时间复杂度为 $O(\log n)$．

??? note "复杂度证明"
    向下递归的层数显然不超过树高，是 $O(\log n)$ 的．需要证明的是，将左右两侧分裂出来的子树分别合并起来的复杂度是 $O(\log n)$ 的．不妨仅考虑左侧的子树，因为右侧是对称的．设左侧分裂出来的子树自下而上分别是 $T_1,T_2,\cdots,T_\ell$，这些子树的数量 $\ell\in O(\log n)$．合并的过程可以描述为，自 $T'_1=T_1$ 开始，将 $T'_{i-1}$ 与 $T_i$ 合并得到 $T'_i$，递归地合并完所有子树为止．合并的总复杂度可以表示为
    
    $$
    \sum_{i=2}^\ell \tau(T_i,T'_{i-1}),
    $$
    
    其中，$\tau(T_i,T'_{i-1})$ 是将 $T_i$ 和 $T'_{i-1}$ 合并起来的复杂度．
    
    如果总是有 $w(T_i)\ge w(T'_{i-1})$，那么根据合并两子树的复杂度表达式，有
    
    $$
    \tau(T_i,T'_{i-1}) \in O\left(\log\dfrac{w(T_i)}{w(T'_{i-1})}\right) \subseteq O\left(\log\dfrac{w(T'_i)}{w(T'_{i-1})}\right).
    $$
    
    因为这些大 $O$ 记号中的常数都是一致的，所以可以直接相加，裂项相消．
    
    但是，应该注意的是，$w(T_i)\ge w(T'_{i-1})$ 并不总是成立，因为 $T'_{i-1}$ 是从 $T_i$ 在原来的树中对应的右子树分裂出来的，而这个右子树可能比左子树 $T_i$ 更大．尽管如此，即使 $T'_{i-1}$ 比 $T_i$ 大，作为右子树的一部分，权重 $w(T'_{i-1})$ 也不会超过 $w(T_i)$ 的 $(1-\alpha)/\alpha$ 倍，这意味着，此时 $T'_{i-1}$ 和 $T_i$ 一定是平衡的，合并的复杂度是 $O(1)$ 的．
    
    将这两种情形总结在一起，单次合并的复杂度可以写为
    
    $$
    \tau(T_i,T'_{i-1}) \in O\left(\log\dfrac{w(T'_i)}{w(T'_{i-1})}\right) + O(1).
    $$
    
    由此，合并的总复杂度为
    
    $$
    O\left(\sum_{i=2}^\ell\left( 1+\log\dfrac{w(T'_i)}{w(T'_{i-1})}\right) \right) \subseteq O(\ell+\log w(T'_\ell)) \subseteq O(\log n).
    $$
    
    这也说明，分裂算法的总复杂度是 $O(\log n)$ 的．

## 参考实现

本文介绍了如何利用 WBLT 完成平衡树的基本操作．下面是用 WBLT 实现的 [普通平衡树模板](https://loj.ac/p/104)．

??? example "参考代码"
    ```cpp
    --8<-- "docs/ds/code/wblt/wblt-1.cpp:full-text"
    ```

利用合并和分裂，也可以实现文艺平衡树．下面是用 WBLT 实现的 [文艺平衡树模板](https://loj.ac/p/105)，需要在向下访问节点时下传懒标记．

??? example "参考代码"
    ```cpp
    --8<-- "docs/ds/code/wblt/wblt-2.cpp:full-text"
    ```

注意 WBLT 需要两倍的空间；涉及分裂与合并时，需要注意垃圾回收，及时回收无用的节点，否则空间不是线性的．

## 参考资料与注释

-   [Weight-balanced tree - Wikipedia](https://en.wikipedia.org/wiki/Weight-balanced_tree)
-   Nievergelt, J.; Reingold, E. M. (1973). "Binary Search Trees of Bounded Balance". SIAM Journal on Computing. 2: 33–43.
-   Blum, Norbert; Mehlhorn, Kurt (1980). "On the average number of rebalancing operations in weight-balanced trees". Theoretical Computer Science. 11 (3): 303–320.
-   Hirai, Y.; Yamamoto, K. (2011). "Balancing weight-balanced trees". Journal of Functional Programming. 21 (3): 287.
-   Blelloch, Guy E.; Ferizovic, Daniel; Sun, Yihan (2016), "Just Join for Parallel Ordered Sets", Symposium on Parallel Algorithms and Architectures, Proc. of 28th ACM Symp. Parallel Algorithms and Architectures (SPAA 2016), ACM, pp. 253–264.
-   Straka, Milan. (2011). "Adams’Trees Revisited: Correctness Proof and Efficient Implementation." International Symposium on Trends in Functional Programming. Berlin, Heidelberg: Springer Berlin Heidelberg.

[^wrong-range]: Nievergelt 和 Reingold 的原始论文中给出的参数范围 $\alpha < 1-\dfrac{\sqrt{2}}{2},~\beta=\dfrac{1-2\alpha}{1-\alpha}$ 是错误的．Hirai 和 Yamamoto 的文章中提供了相应的反例，问题主要出现在某些很小的树上，从而导致整个归纳证明失效．当然，实际算法竞赛中，很难造出能卡掉这些错误参数的数据，所以实践中可能并不会有太大影响．

[^merge-complexity-cmp]: 因为单次平衡操作至多相当于连接两次子树，而且最后两子树已经平衡时还需要调用一次连接子树的算法，所以如果以调用连接子树的算法的次数计算，基于平衡实现的合并操作和下文直接合并的平衡操作的算法的常数是一致的．

[^more-join]: 通过稍后的证明可以看出：第三种情形中，$z$ 和 $w+y$ 总是平衡的；第四种情形中，$z$ 和 $u$ 总是平衡的．它们都可以直接连接，而不需要合并．
