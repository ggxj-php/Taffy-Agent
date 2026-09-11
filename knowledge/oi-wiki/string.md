

## string/ac-automaton.md

author: Ir1d, Tiphereth-A, sshwy, ksyx, Marcythm, orzAtalod, Xeonacid, Enter-tainer, GavinZhengOI, Henry-ZHR, iamtwz, 383494, abc1763613206, aofall, Chrogeek, CoelacanthusHex, Dafenghh, DanJoshua, Gesrua, kenlig, lyccrius, Menci, opsiff, ouuan, partychicken, Persdre, Ruakker, shuzhouliu, StudyingFather, szdytom, XuYueming520, ZXyaang, alphagocc, c-forrest, Early0v0, GoodCoder666, HeRaNO, liangbob2023, qq2964, r-value, rickyxrc, Rickyxrc, shawlleyw, Unnamed2964, zica87, ZnPdCo, sun2snow

## 概述

AC（Aho–Corasick）自动机是 **以 Trie 的结构为基础**，结合 **KMP 的思想** 建立的自动机，用于解决多模式匹配等任务．

AC 自动机本质上是 Trie 上的自动机．

在阅读本文之前，请先阅读 [KMP](./kmp.md) 和 [Trie](./trie.md)．

## 解释

简单来说，建立一个 AC 自动机有两个步骤：

1.  基础的 Trie 结构：将所有的模式串构成一棵 Trie；
2.  KMP 的思想：对 Trie 树上所有的结点构造失配指针．

建立完毕后，就可以利用它进行多模式匹配．

## 字典树构建

AC 自动机在初始时会将若干个模式串插入到一个 Trie 里，然后在 Trie 上建立 AC 自动机．这个 Trie 就是普通的 Trie，按照 Trie 原本的建树方法建树即可．

需要注意的是，Trie 中的结点表示的是某个模式串的前缀．我们在后文也将其称作状态．一个结点表示一个状态，Trie 的边就是状态的转移．

形式化地说，对于若干个模式串 $s_1,s_2,\cdots,s_n$，将它们构建一棵字典树后的所有状态的集合记作 $Q$．

## 失配指针

AC 自动机利用一个 fail 指针来辅助多模式串的匹配．

状态 $u$ 的 fail 指针指向另一个状态 $v$，其中 $v\in Q$，且 $v$ 是 $u$ 的最长后缀（即在若干个后缀状态中取最长的一个作为 fail 指针）．

fail 指针与 [KMP](./kmp.md) 中的 next 指针相比：

1.  共同点：两者同样是在失配的时候用于跳转的指针．
2.  不同点：next 指针求的是最长 Border（即最长的相同前后缀），而 fail 指针指向所有模式串的前缀中匹配当前状态的最长后缀．

因为 KMP 只对一个模式串做匹配，而 AC 自动机要对多个模式串做匹配．有可能 fail 指针指向的结点对应着另一个模式串，两者前缀不同．

总结下来，AC 自动机的失配指针指向当前状态的最长后缀状态．

注意：AC 自动机在做匹配时，同一位上可匹配多个模式串．

### 构建指针

下面介绍构建 fail 指针的 **基础思想**：

构建 fail 指针，可以参考 KMP 中构造 next 指针的思想．

考虑字典树中当前的结点 $u$，$u$ 的父结点是 $p$，$p$ 通过字符 $c$ 的边指向 $u$，即 $\operatorname{trie}(p, c)=u$．假设深度小于 $u$ 的所有结点的 fail 指针都已求得．

1.  如果 $\operatorname{trie}(\operatorname{fail}(p), c)$ 存在：则让 $u$ 的 fail 指针指向 $\operatorname{trie}(\operatorname{fail}(p), c)$．相当于在 $p$ 和 $\operatorname{fail}(p)$ 后面加一个字符 $c$，分别对应 $u$ 和 $\operatorname{fail}(u)$；
2.  如果 $\operatorname{trie}(\operatorname{fail}(p), c)$ 不存在：那么我们继续找到 $\operatorname{trie}(\operatorname{fail}(\operatorname{fail}(p)), c)$．重复判断过程，一直跳 fail 指针直到根结点；
3.  如果依然不存在，就让 fail 指针指向根结点．

如此即完成了 $\operatorname{fail}(u)$ 的构建．

### 例子

下面将使用若干张 GIF 动图来演示对字符串 $\mathtt{i}$、$\mathtt{he}$、$\mathtt{his}$、$\mathtt{she}$、$\mathtt{hers}$ 组成的字典树构建 fail 指针的过程：

1.  黄色结点：当前的结点 $u$．
2.  绿色结点：表示已经 BFS 遍历完毕的结点．
3.  橙色的边：fail 指针．
4.  红色的边：当前求出的 fail 指针．

![AC\_automation\_gif\_b\_3.gif](./images/ac-automaton1.gif)

我们重点分析结点 $6$ 的 fail 指针构建：

![AC\_automation\_6\_9.png](./images/ac-automaton1.png)

找到 $6$ 的父结点 $5$，$\operatorname{fail}(5)=10$．然而结点 $10$ 没有字母 $\mathtt{s}$ 连出的边；继续跳到 $10$ 的 fail 指针，$\operatorname{fail}(10)=0$．发现 $0$ 结点有字母 $\mathtt{s}$ 连出的边，指向 $7$ 结点；所以 $\operatorname{fail}(6)=7$．

下图展示了构建完毕的状态：

![finish](./images/ac-automaton4.png)

## 字典树与字典图

关注构建函数 `build`，该函数的目标有两个，一个是构建 fail 指针，一个是构建自动机．相关变量定义如下：

1.  `tr[u].son[c]`：有两种理解方式．我们可以简单理解为字典树上的一条边，即 $\operatorname{trie}(u, c)$；也可以理解为从状态（结点）$u$ 后加一个字符 $c$ 到达的状态（结点），即一个状态转移函数 $\operatorname{trans}(u, c)$．为了方便，下文中我们将用第二种理解方式．
2.  队列 `q`：用于 BFS 遍历字典树．
3.  `tr[u].fail`：结点 $u$ 的 fail 指针．

???+ note "实现"
    === "C++"
        ```cpp
        void build() {
          queue<int> q;
          for (int i = 0; i < 26; i++)
            if (tr[0].son[i]) q.push(tr[0].son[i]);
          while (!q.empty()) {
            int u = q.front();
            q.pop();
            for (int i = 0; i < 26; i++) {
              if (tr[u].son[i]) {
                tr[tr[u].son[i]].fail = tr[tr[u].fail].son[i];
                q.push(tr[u].son[i]);
              } else
                tr[u].son[i] = tr[tr[u].fail].son[i];
            }
          }
        }
        ```
    
    === "Python"
        ```python
        def build():
            for i in range(0, 26):
                if tr[0][i] != 0:
                    q.append(tr[0][i])
            while q:
                u = q.pop(0)
                for i in range(0, 26):
                    if tr[u][i] != 0:
                        fail[tr[u][i]] = tr[fail[u]][i]
                        q.append(tr[u][i])
                    else:
                        tr[u][i] = tr[fail[u]][i]
        ```

### 解释

`build` 函数将结点按 BFS 顺序入队，依次求 fail 指针．这里的字典树根结点为 $0$，我们将根结点的子结点一一入队．若将根结点入队，则在第一次 BFS 的时候，会将根结点儿子的 fail 指针标记为本身．因此我们将根结点的儿子一一入队，而不是将根结点入队．

然后开始 BFS：每次取出队首的结点 $u$（$\operatorname{fail}(u)$ 在之前的 BFS 过程中已求得），然后遍历字符集（这里是 $0 \sim 25$，对应 $\mathtt{a} \sim \mathtt{z}$，即 $u$ 的各个子结点）：

1.  如果 $\operatorname{trans}(u, c)$ 存在，我们就将 $\operatorname{trans}(u, c)$ 的 fail 指针赋值为 $\operatorname{trans}(\operatorname{fail}(u), c)$．根据之前的描述，我们应该用 `while` 循环，不停地跳 fail 指针，判断是否存在字符 $c$ 对应的结点，然后赋值，但此处通过特殊处理简化了这些代码，将在下文说明；
2.  否则，令 $\operatorname{trans}(u, c)$ 指向 $\operatorname{trans}(\operatorname{fail}(u), c)$ 的状态．

这里的处理是，通过 `else` 语句的代码修改字典树的结构，将不存在的字典树的状态链接到了失配指针的对应状态．在原字典树中，每一个结点代表一个字符串 $S$，是某个模式串的前缀．而在修改字典树结构后，尽管增加了许多转移关系，但结点（状态）所代表的字符串是不变的．

而 $\operatorname{trans}(S, c)$ 相当于是在 $S$ 后添加一个字符 $c$ 变成另一个状态 $S'$．如果 $S'$ 存在，说明存在一个模式串的前缀是 $S'$，否则我们让 $\operatorname{trans}(S, c)$ 指向 $\operatorname{trans}(\operatorname{fail}(S), c)$．由于 $\operatorname{fail}(S)$ 对应的字符串是 $S$ 的后缀，因此 $\operatorname{trans}(\operatorname{fail}(S), c)$ 对应的字符串也是 $S'$ 的后缀．

换言之在 Trie 上跳转的时候，我们只会从 $S$ 跳转到 $S'$，相当于匹配了一个 $S'$；但在 AC 自动机上跳转的时候，我们会从 $S$ 跳转到 $S'$ 的后缀，也就是说我们匹配一个字符 $c$，然后舍弃 $S$ 的部分前缀．舍弃前缀显然是能匹配的．同时如果文本串能匹配 $S$，显然它也能匹配 $S$ 的后缀，所以 fail 指针同样在舍弃前缀．所谓的 fail 指针其实就是 $S$ 的一个后缀集合．

Trie 的结点的孩子数组 `son` 还有另一种比较简单的理解方式：如果在位置 $u$ 失配，我们会跳转到 $\operatorname{fail}(u)$ 的位置．注意这会导致我们可能沿着 fail 数组跳转多次才能来到下一个能匹配的位置．所以我们可以用 `son` 直接记录下一个能匹配的位置，这样保证了程序的时间复杂度．

此处对字典树结构的修改，可以使得匹配转移更加完善．同时它将 fail 指针跳转的路径做了压缩，使得本来需要跳很多次 fail 指针变成跳一次．

### 过程

这里依然用若干张 GIF 动图展示构建过程：

![AC\_automation\_gif\_b\_pro3.gif](./images/ac-automaton2.gif)

1.  蓝色结点：BFS 遍历到的结点 $u$．
2.  蓝色的边：当前结点下，AC 自动机修改字典树结构连出的边．
3.  黑色的边：AC 自动机修改字典树结构连出的边．
4.  红色的边：当前结点求出的 fail 指针．
5.  黄色的边：fail 指针．
6.  灰色的边：字典树的边．

可以发现，众多交错的黑色边将字典树变成了 **字典图**．图中省略了连向根结点的黑边（否则会更乱）．我们重点分析一下结点 $5$ 遍历时的情况．我们求 $\operatorname{trans}(5, \mathtt{s})=6$ 的 fail 指针：

![AC\_automation\_b\_7.png](./images/ac-automaton2.png)

本来的策略是找 fail 指针，于是我们跳到 $\operatorname{fail}(5)=10$ 发现没有 $\mathtt{s}$ 连出的字典树的边，于是跳到 $\operatorname{fail}(10)=0$，发现有 $\operatorname{trie}(0, \mathtt{s})=7$，于是 $\operatorname{fail}(6)=7$；但是有了黑边、蓝边，我们跳到 $\operatorname{fail}(5)=10$ 之后直接走 $\operatorname{trans}(10, \mathtt{s})=7$ 就走到 $7$ 号结点了．

这就是 `build` 完成的两件事：构建 fail 指针和建立字典图．这个字典图也会在查询的时候起到关键作用．

## 多模式匹配

接下来分析匹配函数 `query`：

???+ note "实现"
    === "C++"
        ```cpp
        int query(const char t[]) {
          int u = 0, res = 0;
          for (int i = 1; t[i]; i++) {
            u = tr[u].son[t[i] - 'a'];
            for (int j = u; j && tr[j].cnt != -1; j = tr[j].fail) {
              res += tr[j].cnt, tr[j].cnt = -1;
            }
          }
          return res;
        }
        ```
    
    === "Python"
        ```python
        def query(t: str) -> int:
            u, res = 0, 0
            for c in t:
                u = tr[u][c - ord("a")]
                j = u
                while j and e[j] != -1:
                    res += e[j]
                    e[j] = -1
                    j = fail[j]
            return res
        ```

### 解释

这里 $u$ 作为字典树上当前匹配到的结点，`res` 即返回的答案．循环遍历匹配串，$u$ 在字典树上跟踪当前字符．利用 fail 指针找出所有匹配的模式串，并累加到答案中．然后将匹配到的串的出现次数清零，这样就不会重复统计同一个串．在上文中我们分析过，字典树的结构其实就是一个 trans 函数，而构建好这个函数后，在匹配字符串的过程中，我们会舍弃部分前缀达到最低限度的匹配．fail 指针则指向了更多的匹配状态．最后上一份图．对于刚才的自动机：

![AC\_automation\_b\_13.png](./images/ac-automaton3.png)

我们从根结点开始尝试匹配 $\mathtt{ushersheishis}$，那么 $p$ 的变化将是：

![AC\_automation\_gif\_c.gif](./images/ac-automaton3.gif)

1.  红色结点：$p$ 结点．
2.  粉色箭头：$p$ 在自动机上的跳转．
3.  蓝色的边：成功匹配的模式串．
4.  蓝色结点：示跳 fail 指针时的结点（状态）．

## 效率优化

题目请参考洛谷 [P5357【模板】AC 自动机](https://www.luogu.com.cn/problem/P5357)．

因为我们的 AC 自动机中，每次匹配，会一直向 fail 边跳来找到所有的匹配，但是这样的效率较低，在某些题目中会超时．

那么需要如何优化呢？首先需要了解到 fail 指针的一个性质：一个 AC 自动机中，如果只保留 fail 边，那么剩余的图一定是一棵树．

这是显然的，因为 fail 不会成环，且深度一定比现在低，所以得证．

这样 AC 自动机的匹配就可以转化为在 fail 树上的链求和问题，只需要优化一下该部分就可以了．

这里提供两种思路．

### 拓扑排序优化

观察到时间主要浪费在每次都要跳 fail．如果我们可以预先记录，最后一并求和，那么效率就会优化．

于是我们按照 fail 树，做一次内向树上的拓扑排序，就能一次性求出所有模式串的出现次数．

`build` 函数在原先的基础上，增加了入度统计一部分，为拓扑排序做准备．

???+ note "构建"
    ```cpp
    void build() {
      queue<int> q;
      for (int i = 0; i < 26; i++)
        if (tr[0].son[i]) q.push(tr[0].son[i]);
      while (!q.empty()) {
        int u = q.front();
        q.pop();
        for (int i = 0; i < 26; i++) {
          if (tr[u].son[i]) {
            tr[tr[u].son[i]].fail = tr[tr[u].fail].son[i];
            tr[tr[tr[u].fail].son[i]].du++;  // 入度计数
            q.push(tr[u].son[i]);
          } else
            tr[u].son[i] = tr[tr[u].fail].son[i];
        }
      }
    }
    ```

然后我们在查询的时候就可以只为找到结点的 `ans` 打上标记，在最后再用拓扑排序求出答案．

???+ note "查询"
    ```cpp
    void query(const char t[]) {
      int u = 0;
      for (int i = 1; t[i]; i++) {
        u = tr[u].son[t[i] - 'a'];
        tr[u].ans++;
      }
    }
    
    void topu() {
      queue<int> q;
      for (int i = 0; i <= tot; i++)
        if (tr[i].du == 0) q.push(i);
      while (!q.empty()) {
        int u = q.front();
        q.pop();
        ans[tr[u].idx] = tr[u].ans;
        int v = tr[u].fail;
        tr[v].ans += tr[u].ans;
        if (!--tr[v].du) q.push(v);
      }
    }
    ```

最后是主函数：

???+ note "主函数"
    ```cpp
    int main() {
      // do_something();
      AC::build();
      scanf("%s", s + 1);
      AC::query(s);
      AC::topu();
      for (int i = 1; i <= n; i++) printf("%d\n", AC::ans[idx[i]]);
      // do_another_thing();
    }
    ```

??? note "模板题 [Luogu P5357「模板」AC 自动机](https://www.luogu.com.cn/problem/P5357) 拓扑排序优化参考代码"
    ```cpp
    --8<-- "docs/string/code/ac-automaton/ac-automaton_topu.cpp"
    ```

### DFS 优化

和拓扑排序的思路接近，不过我们使用 DFS 来代替拓扑排序．其实这两种方法本质上是相同的，都是将 fail 树的子树求和．

完整代码请见总结模板 3．

## AC 自动机上 DP

这部分将以 [P2292 \[HNOI2004\] L 语言](https://www.luogu.com.cn/problem/P2292) 为例题讲解．

不难想到一个朴素的思路：建立 AC 自动机，在 AC 自动机上对于所有 fail 指针的子串转移，最后取最大值得到答案．

主要代码如下．若不熟悉代码中的类型定义，可以先看末尾的完整代码：

???+ note "查询部分主要代码"
    ```cpp
    int query(const char t[]) {
      int u = 0, len = strlen(t + 1);
      for (int i = 1; i <= len; i++) dp[i] = 0;
      for (int i = 1; i <= len; i++) {
        u = tr[u].son[t[i] - 'a'];
        for (int j = u; j; j = tr[j].fail) {
          if (tr[j].idx && (dp[i - tr[j].depth] || i - tr[j].depth == 0)) {
            dp[i] = dp[i - tr[j].depth] + tr[j].depth;
          }
        }
      }
      int ans = 0;
      for (int i = 1; i <= len; i++) ans = std::max(ans, dp[i]);
      return ans;
    }
    ```

但是这样的思路复杂度不是线性（因为要跳每个结点的 fail），会在第二个子任务中超时，所以我们需要进行优化．

我们再看看题目的特殊性质，我们发现所有单词的长度只有 $20$，所以可以想到状态压缩优化．

我们发现，目前的时间瓶颈主要在跳 fail 这一步，如果我们可以将这一步优化到 $O(1)$，就可以保证整个问题在严格线性的时间内被解出．

我们可以将前 $20$ 位字母中，可能的子串长度存下来，并压缩到状态中，存在每个子结点中．

那么我们在 `build` 的时候就可以这么写：

???+ note "构建 fail 指针"
    ```cpp
    void build() {
      queue<int> q;
      for (int i = 0; i < 26; i++)
        if (tr[0].son[i]) {
          q.push(tr[0].son[i]);
          tr[tr[0].son[i]].depth = 1;
        }
      while (!q.empty()) {
        int u = q.front();
        q.pop();
        int v = tr[u].fail;
        // 对状态的更新在这里
        tr[u].stat = tr[v].stat;
        if (tr[u].idx) tr[u].stat |= 1 << tr[u].depth;
        for (int i = 0; i < 26; i++) {
          if (tr[u].son[i]) {
            tr[tr[u].son[i]].fail = tr[tr[u].fail].son[i];
            tr[tr[u].son[i]].depth = tr[u].depth + 1;  // 记录深度
            q.push(tr[u].son[i]);
          } else
            tr[u].son[i] = tr[tr[u].fail].son[i];
        }
      }
    }
    ```

然后查询时就可以去掉跳 fail 的循环，将代码简化如下：

???+ note "查询"
    ```cpp
    int query(const char t[]) {
      int u = 0, mx = 0;
      unsigned st = 1;
      for (int i = 1; t[i]; i++) {
        u = tr[u].son[t[i] - 'a'];
        st <<= 1;  // 往下跳了一位每一位的长度都+1
        if (tr[u].stat & st) st |= 1, mx = i;
      }
      return mx;
    }
    ```

我们的 `tr[u].stat` 维护的是从结点 $u$ 开始，整条 fail 链上的长度集（因为长度集小于 $32$ 所以不影响），而 `st` 则维护的是查询字符串走到现在，前 $32$ 位（因为状态压缩自然溢出）的长度集．

`&` 运算后结果不为 $0$，则代表两个长度集的交集非空，我们此时就找到了一个匹配．

??? note "[P2292 \[HNOI2004\] L 语言](https://www.luogu.com.cn/problem/P2292) 完整代码"
    ```cpp
    --8<-- "docs/string/code/ac-automaton/ac_automaton_luoguP2292.cpp"
    ```

## 总结

时间复杂度：定义 $|s_i|$ 是模板串的长度，$|S|$ 是文本串的长度，$|\Sigma|$ 是字符集的大小（常数，一般为 $26$）．如果连了 trie 图，时间复杂度就是 $O(\sum|s_i|+n|\Sigma|+|S|)$，其中 $n$ 是 AC 自动机中结点的数目，并且最大可以达到 $O(\sum|s_i|)$．如果不连 trie 图，并且在构建 fail 指针的时候避免遍历到空儿子，时间复杂度就是 $O(\sum|s_i|+|S|)$．

??? note "模板题 [Luogu P3808 AC 自动机（简单版）](https://www.luogu.com.cn/problem/P3808) 参考代码"
    ```cpp
    --8<-- "docs/string/code/ac-automaton/ac-automaton_1.cpp"
    ```

??? note "模板题 [Luogu P3796 AC 自动机（简单版 II）](https://www.luogu.com.cn/problem/P3796) 参考代码"
    ```cpp
    --8<-- "docs/string/code/ac-automaton/ac-automaton_2.cpp"
    ```

??? note "模板题 [Luogu P5357「模板」AC 自动机](https://www.luogu.com.cn/problem/P5357) DFS 优化参考代码"
    ```cpp
    --8<-- "docs/string/code/ac-automaton/ac-automaton_3.cpp"
    ```


## string/basic.md

author: Ir1d, ouuan, qinggniq, i-Yirannn, minghu6

## 定义

### 字符集

一个 **字符集** $\Sigma$ 是一个建立了 [全序](../math/order-theory.md#偏序集) 关系的集合，也就是说，$\Sigma$ 中的任意两个不同的元素 $\alpha$ 和 $\beta$ 都可以比较大小，要么 $\alpha<\beta$，要么 $\beta<\alpha$．字符集 $\Sigma$ 中的元素称为字符．

### 字符串

一个 **字符串**  $S$ 是将 $n\ (n\ge 0)$ 个字符顺次排列形成的序列，$n$ 称为 $S$ 的长度，表示为 $|S|$．特别地，$n=0$ 时 $S$ 不含任何字符，称为 **空串**，记作 $\varepsilon$．

如果字符串下标从 $1$ 开始计算，$S$ 的第 $i$ 个字符表示为 $S[i]$；

如果字符串下标从 $0$ 开始计算，$S$ 的第 $i$ 个字符表示为 $S[i-1]$．

### 子串

字符串 $S$ 的 **子串**  $S[i..j]，i≤j$，表示 $S$ 串中从 $i$ 到 $j$ 这一段，也就是顺次排列 $S[i],S[i+1],\ldots,S[j]$ 形成的字符串．

有时也会用 $S[i..j]$，$i>j$ 来表示空串 $\varepsilon$．

### 子序列

字符串 $S$ 的 **子序列** 是从 $S$ 中将若干元素提取出来并不改变相对位置形成的序列，即 $S[p_1],S[p_2],\ldots,S[p_k]$，$1\le p_1< p_2<\cdots< p_k\le|S|$，$k\ge 0$．

### 后缀

**后缀** 是指从某个位置 $i$ 开始到整个串末尾结束的一个特殊子串．字符串 $S$ 的从 $i$ 开头的后缀表示为 $\textit{Suffix(S,i)}$，也就是 $\textit{Suffix(S,i)}=S[i..|S|-1]$．

**真后缀** 指除了 $S$ 本身的 $S$ 的后缀．

举例来说，字符串 `abcabcd` 的所有后缀为 `{ε, d, cd, bcd, abcd, cabcd, bcabcd, abcabcd}`，而它的真后缀为 `{ε, d, cd, bcd, abcd, cabcd, bcabcd}`．

### 前缀

**前缀** 是指从串首开始到某个位置 $i$ 结束的一个特殊子串．字符串 $S$ 的以 $i$ 结尾的前缀表示为 $\textit{Prefix(S,i)}$，也就是 $\textit{Prefix(S,i)}=S[0..i]$．

**真前缀** 指除了 $S$ 本身的 $S$ 的前缀．

举例来说，字符串 `abcabcd` 的所有前缀为 `{ε, a, ab, abc, abca, abcab, abcabc, abcabcd}`, 而它的真前缀为 `{ε, a, ab, abc, abca, abcab, abcabc}`．

### 字典序

以第 $i$ 个字符作为第 $i$ 关键字进行大小比较，空字符小于字符集内任何字符（即：$a< aa$）．

### 回文串

**回文串** 是正着写和倒着写相同的字符串，即满足 $\forall 1\le i\le|s|, s[i]=s[|s|+1-i]$ 的 $s$．

### 汉明距离

**汉明距离** 是两个等长字符串之间的距离，它表示两个长度相同的字符串对应位字符不同的数量．

我们可以简单的认为对两个串进行异或运算，结果为 $1$ 的数量就是两个串的汉明距离．

## 字符串的存储

-   使用 `char` 数组存储，用空字符 `\0` 表示字符串的结尾（C 风格字符串）．
-   使用 C++ 标准库提供的 [`string` 类](../lang/csl/string.md)．
-   字符串常量可以用字符串字面量（用双引号括起来的字符串）表示．


## string/bm.md

author: minghu6

前置知识：[前缀函数与 KMP 算法](./kmp.md)．

KMP 算法将前缀匹配的信息用到了极致，

而 BM 算法背后的基本思想是通过后缀匹配获得比前缀匹配更多的信息来实现更快的字符跳转．

## 引入

想象一下，如果我们的模式字符串 $pat$，被放在文本字符串 $string$ 的左手起头部，使它们的第一个字符对齐．

$$
\begin{aligned}
\textit{pat}:\qquad\qquad &\texttt{EXAMPLE} \\
\textit{string}:\qquad\quad &\texttt{HERE IS A SIMPLE EXAMPLE} \dots \\
&\qquad\ \ \ \, \, \Uparrow
\end{aligned}
$$

在这里做定义，往后不赘述：

$pat$ 的长度为 $patlen$，特别地对于从 0 开始的串来说，规定 $patlastpos=patlen-1$ 为 $pat$ 串最后一个字符的位置；

$string$ 的长度 $stringlen$，$stringlastpos = stringlen-1$．

假如我们知道了 $string$ 的第 $patlen$ 个字符 $char$（与 $pat$ 的最后一个字符对齐）考虑我们能得到什么信息：

### 观察 1

如果我们知道 $char$ 这个字符不在 $pat$ 中，我们就不用考虑 $pat$ 从 $string$ 的第 $1$ 个、第 $2$ 个……第 $patlen$ 个字符起出现的情况，而可以直接将 $pat$ 向下滑动 $patlen$ 个字符．

### 观察 2

更一般地，**如果出现在 $pat$ 最末尾（也就是最右边）的那一个 $char$ 字符的位置是离末尾端差了 $delta_1$ 个字符**，

那么就可以不用匹配，直接将 $pat$ 向后滑动 $delta_1$ 个字符：如果滑动距离少于 $delta_1$，那么仅就 $char$ 这个字符就无法被匹配，当然模式字符串 $pat$ 也就不会被匹配．

因此除非 $char$ 字符可以和 $pat$ 末尾的那个字符匹配，否则 $string$ 要跳过 $delta_1$ 个字符（相当于 $pat$ 向后滑动了 $delta_1$ 个字符）．并且我们可以得到一个计算 $delta_1$ 的函数 $delta_1(char)$：

$$
\begin{array}{ll}
\textbf{int}\ delta1(\textbf{char}\ char) \\
\qquad \textbf{if}\ \text{char不在pat中 || char是pat上最后一个字符} \\
\qquad\qquad\textbf{return}\ patlen \\
\qquad \textbf{else} \\
\qquad\qquad\textbf{return}\ patlastpos-i\quad\textbf{//}\ \text{i为出现在pat最末尾的那一个char出现的位置，即pat[i]=char}
\end{array}
$$

需要注意，显然这个表只需计算到 $patlastpos-1$ 的位置．

现在假设 $char$ 和 $pat$ 最后一个字符匹配到了，那我们就看看 $char$ 前一个字符和 $pat$ 的倒数第二个字符是否匹配：

如果是，就继续回退直到整个模式串 $pat$ 完成匹配（这时我们就在 $string$ 上成功得到了一个 $pat$ 的匹配）；

或者，我们也可能会在匹配完 $pat$ 的倒数第 $m$ 个字符后，在倒数第 $m+1$ 个字符上失配，这时我们就希望把 $pat$ 向后滑动到下一个可能会实现匹配的位置，当然我们希望滑动得越远越好．

### 观察 3(a)

在 **观察 2** 中提到，当匹配完 $pat$ 的倒数 $m$ 个字符后，如果在倒数第 $m+1$ 个字符失配，为了使得 $string$ 中的失配字符与 $pat$ 上对应字符对齐，

需要把 $pat$ 向后滑动 $k$ 个字符，也就是说我们应该把注意力看向之后的 $k+m$ 个字符（也就是看向 $pat$ 滑动 k 之后，末段与 $string$ 对齐的那个字符）．

而 $k=delta_1-m$，

所以我们的注意力应该沿着 $string$ 向后跳 $delta_1-m+m = delta_1$ 个字符．

然而，我们有机会跳过更多的字符，请继续看下去．

### 观察 3(b)

如果我们知道 $string$ 接下来的 $m$ 个字符和 $pat$ 的最后 $m$ 个字符匹配，假设这个子串为 $subpat$，

我们还知道在 $string$ 失配字符 $char$ 后面是与 $subpat$ 相匹配的子串，而假如 $pat$ 对应失配字符前面存在 $subpat$，我们可以将 $pat$ 向下滑动一段距离，

使得失配字符 $char$ 在 $pat$ 上对应的字符前面出现的 $subpat$（合理重现，plausible reoccurrence，以下也简称 pr）与 $string$ 的 $subpat$ 对齐．如果 $pat$ 上有多个 $subpat$，按照从右到左的后缀匹配顺序，取第一个（rightmost plausible reoccurrence，以下也简称 rpr）．

假设此时 $pat$ 向下滑动的 $k$ 个字符（也即 $pat$ 末尾端的 $subpat$ 与其最右边的合理重现的距离），这样我们的注意力应该沿着 $string$ 向后滑动 $k+m$ 个字符，这段距离我们称之为 $delta_2(j)$：

假定 $rpr(j)$ 为 $subpat=pat[j+1\dots patlastpos]$ 在 $pat[j]$ 上失配时的最右边合理重现的位置，$rpr(j) < j$（这里只给出简单定义，在下文的算法设计章节里会有更精确的讨论），那么显然 $k=j-rpr(j),\ m=patlastpos-j$．

所以有：

$$
\begin{array}{ll}
\textbf{int}\ delta2(\textbf{int}\ j) \quad\textbf{//}\ \text{j为失配字符在pat上对应字符的位置} \\
\qquad\qquad\textbf{return}\ patlastpos-rpr(j) \\
\end{array}
$$

于是我们在失配时，可以把 $string$ 上的注意力往后跳过 $\max(delta_1,delta_2)$ 个字符

## 过程

箭头指向失配字符 $char$：

$$
\begin{aligned}
\textit{pat}:\qquad\qquad &\texttt{AT-THAT} \\
\textit{string}:\ \ \ \dots\ &\texttt{WHICH-FINALLY-HALTS.--AT-THAT-POINT} \dots \\
&\qquad\ \ \ \, \, \Uparrow
\end{aligned}
$$

$\texttt{F}$ 没有出现 $pat$ 中，根据 **观察 1**，$pat$ 直接向下移动 $patlen$ 个字符，也就是 7 个字符：

$$
\begin{aligned}
\textit{pat}:\qquad\qquad &\qquad\quad\ \ \, \texttt{AT-THAT} \\
\textit{string}:\ \ \ \dots\ &\texttt{WHICH-FINALLY-HALTS.--AT-THAT-POINT} \dots \\
&\qquad\ \ \ \, \, \qquad\quad\ \ \ \Uparrow
\end{aligned}
$$

根据 **观察 2**，我们需要将 $pat$ 向下移动 4 个字符使得短横线字符对齐：

$$
\begin{aligned}
\textit{pat}:\qquad\qquad &\qquad\qquad\quad\ \ \, \texttt{AT-THAT} \\
\textit{string}:\ \ \ \dots\ &\texttt{WHICH-FINALLY-HALTS.--AT-THAT-POINT} \dots \\
&\qquad\ \ \ \; \qquad\qquad\qquad \Uparrow
\end{aligned}
$$

现在*char*:$\texttt{T}$ 匹配了，把 $string$ 上的指针左移一步继续匹配：

$$
\begin{aligned}
\textit{pat}:\qquad\qquad &\qquad\qquad\quad\ \ \, \texttt{AT-THAT} \\
\textit{string}:\ \ \ \dots\ &\texttt{WHICH-FINALLY-HALTS.--AT-THAT-POINT} \dots \\
&\qquad\ \ \ \; \qquad\qquad\quad\ \, \Uparrow
\end{aligned}
$$

根据 **观察 3(a)**，$\texttt{L}$ 失配，因为 $\texttt{L}$ 不在 $pat$ 中，所以 $pat$ 向下移动 $k=delta_1-m=7-1=6$ 个字符，而 $string$ 上指针向下移动 $delta_1=7$ 个字符：

$$
\begin{aligned}
\textit{pat}:\qquad\qquad &\qquad\qquad\qquad\qquad\ \ \,\, \texttt{AT-THAT} \\
\textit{string}:\ \ \ \dots\ &\texttt{WHICH-FINALLY-HALTS.--AT-THAT-POINT} \dots \\
&\qquad\ \ \ \; \qquad\qquad\qquad\qquad\ \ \ \, \, \Uparrow
\end{aligned}
$$

这时 $char$ 又一次匹配到了 $pat$ 的最后一个字符 $\texttt{T}$，$string$ 上的指针向左匹配，匹配到了 $\texttt{A}$，继续向左匹配，发现在字符 $\texttt{-}$ 失配：

$$
\begin{aligned}
\textit{pat}:\qquad\qquad &\qquad\qquad\qquad\qquad\ \ \,\, \texttt{AT-THAT} \\
\textit{string}:\ \ \ \dots\ &\texttt{WHICH-FINALLY-HALTS.--AT-THAT-POINT} \dots \\
&\qquad\ \ \ \; \qquad\qquad\qquad\quad\ \ \ \,\, \Uparrow
\end{aligned}
$$

显然直观上看，此时根据 **观察 3(b)**，将 $pat$ 向下移动 $k=5$ 个字符，使得后缀 $\texttt{AT}$ 对齐，这种滑动可以获得 $string$ 指针最大的滑动距离，此时 $delta_2=k+patlastpos-j=5+6-4=7$，即 $string$ 上指针向下滑动 7 个字符．

而从形式化逻辑看，此时，$delta_1=7-1-2=4,\ delta_2=7, \max(delta_1,delta_2)= 7$，
这样从形式逻辑上支持了进行 **观察 3(b)** 的跳转：

$$
\begin{aligned}
\textit{pat}:\qquad\qquad &\qquad\qquad\qquad\qquad\qquad\quad \;\, \texttt{AT-THAT} \\
\textit{string}:\ \ \ \dots\ &\texttt{WHICH-FINALLY-HALTS.--AT-THAT-POINT} \dots \\
&\qquad\ \ \ \; \qquad\qquad\qquad\qquad\qquad\quad \ \ \; \Uparrow
\end{aligned}
$$

现在我们发现了 $pat$ 上每一个字符都和 $string$ 上对应的字符相等，我们在 $string$ 上找到了一个 $pat$ 的匹配．而只花费了 14 次对 $string$ 的引用，其中 7 次是完成一个成功的匹配所必需的比较次数（$patlen=7$），另外 7 次让我们跳过了 22 个字符．

## 算法设计

### 最初的匹配算法

#### 解释

现在看这样一个利用 $delta_1$ 和 $delta_2$ 进行字符串匹配的算法：

$$
\begin{array}{ll}
i \gets patlastpos. \\
j \gets patlastpos. \\
\textbf{loop}\\
\qquad \textbf{if}\ j < 0 \\
\qquad \qquad \textbf{return}\ i+1 \\
\\
\qquad \textbf{if}\ string[i]=pat[j] \\
\qquad \qquad j \gets j-1 \\
\qquad \qquad i \gets i-1 \\
\qquad \qquad \textbf{continue} \\
\\
\qquad i \gets i+max(delta_1(string[i]), delta_2(j)) \\
\\
\qquad \textbf{if}\ i > stringlastpos \\
\qquad \qquad \textbf{return}\ false \\
\qquad j \gets patlastpos \\
\end{array}
$$

如果上面的算法 $\textbf{return}\ false$，表明 $pat$ 不在 $string$ 中；如果返回一个数字，表示 $pat$ 在 $string$ 左起第一次出现的位置．

然后让我们更精细地描述下计算 $delta_2$，所依靠的 $rpr(j)$ 函数．

根据前文定义，$rpr(j)$ 表示在 $pat(j)$ 失配时，子串 $subpat=pat[j+1\dots patlastpos]$ 在 $pat[j]$ 最右边合理重现的位置．

也就是说需要找到一个最好的 $k$, 使得 $pat[k\dots k+patlastpos-j-1]=pat[j+1\dots patlastpos]$，另外要考虑两种特殊情况：

1.  当 $k<0$ 时，相当于在 $pat$ 前面补充了一段虚拟的前缀，实际上也符合 $delta_2$ 跳转的原理．
2.  当 $k>0$ 时，如果 $pat[k-1]=pat[j]$，则这个 $pat[k\dots k+patlastpos-j-1]$ 不能作为 $subpat$ 的合理重现．
    原因是 $pat[j]$ 本身是失配字符，所以 $pat$ 向下滑动 $k$ 个字符后，在后缀匹配过程中仍然会在 $pat[k-1]$ 处失配．

还要注意两个限制条件：

1.  $k < j$．因为当 $k=j$ 时，有 $pat[k]=pat[j]$，在 $pat[j]$ 上失配的字符也会在 $pat[k]$ 上失配．
2.  考虑到 $delta_2(patlastpos)= 0$，所以规定 $rpr(patlastpos) = patlastpos$．

#### 过程

由于理解 $rpr(j)$ 是实现 BoyerMoore 算法的核心，所以我们使用如下两个例子进行详细说明：

$$
\begin{aligned}
\textit{j}:\qquad\qquad\quad\ \ &\texttt{0 1 2 3 4 5 6 7 8} \\
\textit{pat}:\qquad\qquad\ \  &\texttt{A B C X X X A B C} \\
\textit{rpr(j)}:\qquad\quad\  \  &\texttt{5 4 3 2 1 0 2 1 8} \\
\textit{sgn}:\qquad\qquad\ \   &\texttt{- - - - - - - - +}
\end{aligned}
$$

对于 $rpr(0)$，$subpat$ 为 $\texttt{BCXXXABC}$，在 $pat[0]$ 之前的最右边合理重现只能是 $\texttt{[(BCXXX)ABC]XXXABC}$，也就是最右边合理重现位置为 -5，即 $rpr(j)=-5$；

对于 $rpr(1)$，$subpat$ 为 $\texttt{CXXXABC}$，在 $pat[1]$ 之前的最右边的合理重现是 $\texttt{[(CXXX)ABC]XXXABC}$，所以 $rpr(j)=-4$；

对于 $rpr(2)$，$subpat$ 为 $\texttt{XXXABC}$，在 $pat[2]$ 之前的最右边的合理重现是 $\texttt{[(XXX)ABC]XXXABC}$，所以 $rpr(j)=-3$；

对于 $rpr(3)$，$subpat$ 为 $\texttt{XXABC}$，在 $pat[3]$ 之前的最右边的合理重现是 $\texttt{[(XX)ABC]XXXABC}$，所以 $rpr(j)=-2$；

对于 $rpr(4)$，$subpat$ 为 $\texttt{XABC}$，在 $pat[4]$ 之前的最右边的合理重现是 $\texttt{[(X)ABC]XXXABC}$，所以 $rpr(j)=-1$；

对于 $rpr(5)$，$subpat$ 为 $\texttt{ABC}$，在 $pat[5]$ 之前的最右边的合理重现是 $\texttt{[ABC]XXXABC}$，所以 $rpr(j)=0$；

对于 $rpr(6)$，$subpat$ 为 $\texttt{BC}$，又因为 $string[0]=string[6]$，即 $string[0]$ 等于失配字符 $string[6]$，所以 $string[0\dots 2]$ 并不是符合条件的 $subpat$ 的合理重现，所以在最右边的合理重现是 $\texttt{[(BC)]ABCXXXABC}$，所以 $rpr(j)=-2$；

对于 $rpr(7)$，$subpat$ 为 $\texttt{C}$，同理又因为 $string[7]=string[1]$，所以 $string[1\dots 2]$ 并不是符合条件的 $subpat$ 的合理重现，在最右边的合理重现是 $\texttt{[(C)]ABCXXXABC}$，所以 $rpr(j)=-1$；

对于 $rpr(8)$，根据 $delta_2$ 定义，$rpr(patlastpos)=patlastpos$，得到 $rpr(8)=8$．

现在再看一下另一个例子：

$$
\begin{aligned}
\textit{j}:\qquad\qquad\quad\ \ &\texttt{0 1 2 3 4 5 6 7 8} \\
\textit{pat}:\qquad\qquad\ \ &\texttt{A B Y X C D E Y X} \\
\textit{rpr(j)}:\qquad\quad\  \  &\texttt{8 7 6 5 4 3 2 1 8} \\
\textit{sgn}:\qquad\qquad\ \   &\texttt{- - - - - - + - +}
\end{aligned}
$$

对于 $rpr(0)$，$subpat$ 为 $\texttt{BYXCDEYX}$，在 $pat[0]$ 之前的最右边合理重现只能是 $\texttt{[(BYXCDEYX)]ABYXCDEYX}$，也就是最右边合理重现位置为 -8，即 $rpr(j)=-8$；

对于 $rpr(1)$，$subpat$ 为 $\texttt{YXCDEYX}$，在 $pat[1]$ 之前的最右边合理重现只能是 $\texttt{[(YXCDEYX)]ABYXCDEYX}$，$rpr(j)=-7$；

对于 $rpr(2)$，$subpat$ 为 $\texttt{XCDEYX}$，在 $pat[2]$ 之前的最右边合理重现只能是 $\texttt{[(XCDEYX)]ABYXCDEYX}$，$rpr(j)=-6$；

对于 $rpr(3)$，$subpat$ 为 $\texttt{CDEYX}$，在 $pat[3]$ 之前的最右边合理重现只能是 $\texttt{[(CDEYX)]ABYXCDEYX}$，$rpr(j)=-5$；

对于 $rpr(4)$，$subpat$ 为 $\texttt{DEYX}$，在 $pat[4]$ 之前的最右边合理重现只能是 $\texttt{[(DEYX)]ABYXCDEYX}$，$rpr(j)=-4$；

对于 $rpr(5)$，$subpat$ 为 $\texttt{EYX}$，在 $pat[5]$ 之前的最右边合理重现只能是 $\texttt{[(EYX)]ABYXCDEYX}$，$rpr(j)=-3$；

对于 $rpr(6)$，$subpat$ 为 $\texttt{YX}$，因为 $string[2\dots 3]=string[7\dots 8]$ 并且有 $string[6]\neq string[1]$，所以在 $pat[6]$ 之前的最右边的合理重现是 $\texttt{AB[YX]CDEYX}$，$rpr(j)=2$；

对于 $rpr(7)$，$subpat$ 为 $\texttt{X}$，虽然 $string[3]=string[8]$ 但是因为 $string[2] = string[7]$，所以在 $pat[7]$ 之前的最右边的合理重现是 $\texttt{[X]ABYXCDEYX}$，$rpr(j)=-1$;

对于 $rpr(8)$，根据 $delta_2$ 定义，$rpr(patlastpos)=patlastpos$，得到 $rpr(8)=8$．

### 对匹配算法的一个改进

最后，实践过程中考虑到搜索过程中估计有 80% 的时间用在了 **观察 1** 的跳转上，也就是 $string[i]$ 和 $pat[patlastpos]$ 不匹配，然后跳跃整个 $patlen$ 进行下一次匹配的过程．

于是，可以为此进行特别的优化：

我们定义一个 $delta0$：

$$
\begin{array}{ll}
\textbf{int}\ delta0(\textbf{char}\ char) \\
\qquad \textbf{if}\ char=pat[patlastpos] \\
\qquad\qquad \textbf{return}\ large\ \ \text{// large为一个整数，需要满足large>stringlastpos+patlen} \\
\qquad \textbf{return}\ delta1(char)
\end{array}
$$

用 $delta0$ 代替 $delta_1$，得到改进后的匹配算法：

$$
\begin{array}{ll}
i \gets patlastpos \\
\textbf{loop} \\
\qquad\textbf{if} \ i > stringlastpos \\
\qquad\qquad\textbf{return}\ false\\
\\
\qquad\textbf{while}\ i < stringlen \\
\qquad\qquad i \gets i+delta0(string(i)) \ \ \text{// 除非string[i]和pat末尾字符匹配，否则至多向下滑动patlen }\\\
\qquad\textbf{if}\ i \leqslant\ large \qquad\qquad\qquad\qquad \text{//此时表示string上没有一个字符和pat末尾字符匹配}\ \\
\qquad\qquad\textbf{return}\ false\\
\\
\qquad i \gets i-large \\
\qquad j \gets patlastpos. \\
\qquad\textbf{while}\ j \geqslant\ 0 \ and \  string[i]=pat[j]\\
\qquad \qquad j \gets j-1 \\
\qquad \qquad i \gets i-1 \\
\\
\qquad \textbf{if}\ j < 0 \\
\qquad \qquad \textbf{return}\ i+1 \\
\qquad i \gets i+max(delta_1(string[i]), delta_2(j)) \\
\\
\end{array}
$$

其中 $large$ 起到多重作用，一是类似后面介绍的 Horspool 算法进行快速的坏字符跳转，二是辅助检测字符串搜索是否完成．

经过改进，比起原算法，在做 **观察 1** 跳转时不必每次进行 $delta_2$ 的多余计算，使得在通常字符集下搜索字符串的性能有了明显的提升．

## delta2 构建细节

### 引入

在 1977 年 10 月的*Communications of the ACM*上，Boyer、Moor 的论文[^bm]中只描述了 $delta_2$ 静态表，

构造 $delta_2$ 的具体实现的讨论出现在 1977 年 6 月 Knuth、Morris、Pratt 在*SIAM Journal on Computing*上正式联合发表的 KMP 算法的论文[^kmp]．

### 朴素算法

在介绍 Knuth 的 $delta_2$ 构建算法之前，根据定义，我们会有一个适用于小规模问题的朴素算法：

1.  对于 `[0, patlen)` 区间的每一个位置 `i`，根据 `subpat` 的长度确定其重现位置的区间，也就是 `[-subpatlen, i]`；
2.  可能的重现位置按照从右到左进行逐字符比较，寻找符合 $delta_2$ 要求的最右边 $subpat$ 的重现位置；
3.  最后别忘了令 $delta_2(lastpos)= 0$．

???+ note "实现"
    ```Rust
    use std::cmp::PartialEq;
    
    pub fn build_delta_2_table_naive(p: &[impl PartialEq]) -> Vec<usize> {
        let patlen = p.len();
        let lastpos = patlen - 1;
        let mut delta_2 = vec![];
        
        for i in 0..patlen {
            let subpatlen = (lastpos - i) as isize;
            
            if subpatlen == 0 {
                delta_2.push(0);
                break;
            }
            
            for j in (-subpatlen..(i + 1) as isize).rev() {
                // subpat 匹配
                if (j..j + subpatlen)
                .zip(i + 1..patlen)
                .all(|(rpr_index, subpat_index)| {
                    if rpr_index < 0 {
                        return true;
                    }
                    
                    if p[rpr_index as usize] == p[subpat_index] {
                        return true;
                    }
                    
                    false
                })
                && (j <= 0 || p[(j - 1) as usize] != p[i])
                {
                    delta_2.push((lastpos as isize - j) as usize);
                    break;
                }
            }
        }
        
        delta_2
    }
    ```

特别地，对 Rust 语言特性进行必要地解释，下不赘述：

-   `usize` 和 `isize` 是和内存指针同字节数的无符号整数和有符号整数，在 32 位机上相当于 `u32` 和 `i32`，64 位机上相当于 `u64` 和 `i64`．
-   索引数组、向量、分片时使用 `usize` 类型的数字（因为在做内存上的随机访问并且下标不能为负值），所以如果需要处理负值要用 `isize`，而进行索引时又要用 `usize`，这就看到使用 `as` 关键字进行二者之间的显式转换．
-   `impl PartialEq` 只是用作泛型，可以同时支持 `Unicode` 编码的 `char` 和二进制的 `u8`．

显然，该暴力算法的时间复杂度为 $O(n^3)$．

### 高效算法

下面我们要介绍的是时间复杂度为 $O(n)$，但是需要额外 $O(n)$ 空间复杂度的高效算法．

虽然 1977 年 Knuth 提出了这个构建方法，然而他的原始版本的构建算法存在一个缺陷，实际上对于某些 $pat$ 产生不出符合定义的 $delta_2$．

Rytter 在 1980 年*SIAM Journal on Computing*上发表的文章[^rytter]对此提出了修正，以下是 $delta_2$ 的构建算法：

首先考虑到 $delta_2$ 的定义比较复杂，我们按照 $subpat$ 的重现位置进行分类，每一类进行单独处理，这是高效实现的关键思路．

按照重现位置由远到近，也就是偏移量由大到小，分成如下几类：

1.  整个 $subpat$ 重现位置完全在 $pat$ 左边的，比如 $\texttt{[(EYX)]ABYXCDEYX}$，此时 $delta_2(j) = patlastpos\times 2 - j$；

2.  $subpat$ 的重现有一部分在 $pat$ 左边，有一部分是 $pat$ 头部，比如 $\texttt{[(XX)ABC]XXXABC}$，此时 $patlastpos < delta_2(j) < patlastpos\times 2 - j$；
    我们把 $subpat$ 完全在 $pat$ 头部的边际情况也归类在这里（当然根据实现也可以归类在下边），比如 $\texttt{[ABC]XXXABC}$，此时 $patlastpos = delta_2(j)$；

3.  $subpat$ 的重现完全在 $pat$ 中，比如 $\texttt{AB[YX]CDEYX}$，此时 $delta_2(j) < patlastpos$．

现在来讨论如何高效地计算这三种情况：

#### 第一种情况

这是最简单的情况，只需一次遍历并且可以顺便将 $delta_2$ 初始化．

#### 第二种情况

我们观察什么时候会出现 $subpat$ 的重现一部分在 $pat$ 左边，一部分是 $pat$ 的头部的情况呢？应该是 $subpat$ 的某个后缀和 $pat$ 的某个前缀相等，

比如之前的例子：

$$
\begin{aligned}
\textit{j}:\qquad\qquad\quad\ \ &\texttt{0 1 2 3 4 5 6 7 8} \\
\textit{pat}:\qquad\qquad\ \  &\texttt{A B C X X X A B C} \\
\end{aligned}
$$

$delta_2(3)$ 的重现 $\texttt{[(XX)ABC]XXXABC}$，$subpat$ $\texttt{XXABC}$ 的后缀与 pat 前缀中，有相等的，是 $\texttt{ABC}$．

实际上，对第二种和第三种情况的计算的关键都需要前缀函数的计算和和应用．

那么只要 $j$ 取值使得 $subpat$ 包含这个相等的后缀，那么就可以得到第二种情况的 $subpat$ 的重现，对于例子，我们只需要使得 $j \leqslant 5$，

而当 $j = 5$ 时，就是 $subpat$ 完全在 $pat$ 头部的边际情况．

可以计算此时的 $delta_2(j)$：

设此时这对相等的前后缀长度为 $\textit{prefixlen}$，可知 $subpatlen = patlastpos - j$，那么在 $pat$ 左边的部分长度是 $subpatlen-\textit{prefixlen}$，

而 $rpr(j) = -(subpatlen-\textit{prefixlen})$，所以得到 $delta_2(j) = patlastpos - rpr(j) = patlastpos \times 2 - j - \textit{prefixlen}$．

其后面可能会有多对相等的前缀和后缀，比如：

$$
\begin{aligned}
\textit{j}:\qquad\qquad\quad\ \ &\texttt{0 1 2 3 4 5 6 7 8 9} \\
\textit{pat}:\qquad\qquad\ \  &\texttt{A B A A B A A B A A} \\
\end{aligned}
$$

在 $j\leq2$ 处有 $\texttt{ABAABAA}$，$2< j \leq 5$ 处有 $\texttt{ABAA}$，在 $5<j\leq8$ 处有 $\texttt{A}$

Knuth 算法的缺陷是只考虑了最长的那一对的情况，但实际上我们要考虑所有 $subpat$ 后缀与 $pat$ 前缀相等的情况，等同于计算 $pat$ 所有真后缀和真前缀相等的情况，并按照长度从大到小，$j$ 分区间计算不同的 $delta_2(j)$．

利用前缀函数和逆向运用计算前缀函数的状态转移方程：$j^{(n)} = \pi[j^{(n-1)}-1]$，以得到 $pat$ 所有相等的真前缀和真后缀长度．从 $\pi[patlastpos]$ 开始作为最长一对的长度，然后通过逆向运行状态转移方程，得到下一个次长相等真前缀和真后缀的长度．

如此就完成了第二种情况的 $delta_2$ 的计算．

#### 第三种情况

$subpat$ 的重现恰好就在 $pat$ 中（不包括 $pat$ 的头部），也就是按照从右到左的顺序，在 $pat[0\dots patlastpos-1]$ 中寻找 $subpat$．

如果用 BM 算法解决，我们就得到了一个 BM 的递归实现的第三种情况，结束条件是 $patlen \leqslant  2$．

而且根据 $delta_2$ 的定义，找到的 $subpat$ 的重现的下一个（也就是左边一个）字符和作为 $pat$ 后缀的 $subpat$ 的下一个字符不能一样．

这就很好地启发了我们，可以使用类似于计算前缀函数的过程计算第三种情况，只不过是左右反过来的前缀函数：

-   两个指针分别指向子串的左端点和子串最长公共前后缀的「前缀」位置，从右向左移动，在发现指向的两个字符相等时继续移动，此时相当于「前缀」变大；
-   当两个字符不相等时，之前相等的部分就满足了 $delta_2$ 对重现的要求，并且回退指向「前缀」位置的指针直到构成新的字符相等或者出界．

同前缀函数一样，需要一个辅助数组，用于回退，可以使用之前计算第二种情况所生成的前缀数组的空间．

### 实现

??? note "上述实现"
    ```rust
    use std::cmp::PartialEq;
    use std::cmp::min;
    
    pub fn build_delta_2_table_improved_minghu6(p: &[impl PartialEq]) -> Vec<usize> {
        let patlen = p.len();
        let lastpos = patlen - 1;
        let mut delta_2 = Vec::with_capacity(patlen);
        
        // 第一种情况
        // delta_2[j] = lastpos * 2 - j
        for i in 0..patlen {
            delta_2.push(lastpos * 2 - i);
        }
        
        // 第二种情况
        // lastpos <= delata2[j] = lastpos * 2 - j
        let pi = compute_pi(p);  // 计算前缀函数
        let mut i = lastpos;
        let mut last_i = lastpos; // 只是为了初始化
        while pi[i] > 0 {
            let start;
            let end;
            
            if i == lastpos {
                start = 0;
            } else {
                start = patlen - pi[last_i];
            }
            
            end = patlen - pi[i];
            
            for j in start..end {
                delta_2[j] = lastpos * 2 - j - pi[i];
            }
            
            last_i = i;
            i = pi[i] - 1;
        }
        
        // 第三种情况
        // delata2[j] < lastpos
        let mut j = lastpos;
        let mut t = patlen;
        let mut f = pi;
        loop {
            f[j] = t;
            while t < patlen && p[j] != p[t] {
                // 使用min函数保证后面可能的回退不会覆盖前面的数据
                delta_2[t] = min(delta_2[t], lastpos - 1 - j);
                t = f[t];
            }
            
            t -= 1;
            if j == 0 {
                break;
            }
            j -= 1;
        }
        
        // 没有实际意义，只是为了完整定义
        delta_2[lastpos] = 0;
        
        delta_2
    }
    ```

## Galil 规则对多次匹配时最坏情况的改善

### 关于后缀匹配算法的多次匹配问题

之前的搜索算法只涉及到在 $string$ 中寻找第一次 $pat$ 匹配的情况，而对与在 $string$ 中寻找全部 $pat$ 的匹配的情况有很多不同的算法思路，这个问题的核心关注点是：如何利用之前匹配成功的字符的信息，将最坏情况下的时间复杂度降为线性．

在原始的成功匹配后，简单的 $string$ 的指针向后滑动 $patlen$ 距离后重新开始后缀匹配，这会导致最坏情况下回到 $O(mn)$ 的时间复杂度（按照惯例，$m$ 为 $patlen$，$n$ 为 $stringlen$，下同）．

比如一个极端的例子：$pat$：$\texttt{AAA}$，$string$：$\texttt{AAAAA}\dots$．

对此 Knuth 提出来的一个方法是用一个「数量有限」的状态的集合来记录 $patlen$ 长度的字符，这种算法保证 $string$ 上每一个字符最多比较一次，但代价是这个「数量有限」的状态可能规模并不小，对于一个字符彼此不相等的 $pat$，需要 $\dfrac{1}{2}m^{2}+m$ 个状态．

下面介绍的思路简单且不需要额外预处理开销的 Galil 算法[^galil-rule]．

### Galil 规则

假定一个 $pat$，它是某个子串 $U$ 重复 n 次构成的字符串 $UUUU\dots$ 的前缀，那么我们称 $U$ 为 $pat$ 的一个周期．

比如，$pat: \texttt{ABCABCAB}$，是 $\texttt{ABC}$ 的重复 $\texttt{ABCABCABC}$ 的前缀，所以 $\texttt{ABC}$ 的长度 $3$ 就是这个 $pat$ 的周期长度，也即 $pat$ 满足 $pat[i] = pat[i+3]$．

$pat$ 至少拥有一个长度为它自身的周期，我们规定最短的周期为 $k$，$k\leq patlen$．

在搜索过程中，假如我们的 $pat$ 成功地完成了一次匹配，那么依照周期的特点，实际上只需将 $string$ 向后滑动 $k$ 个字符，比较这 $k$ 个字符是否对应相等就可以直接判断是否存在 $pat$ 的又一个匹配．

为计算这个最短周期的长度，我们假设已知 $pat$ 的相等的一对前缀 - 后缀，设它们的长度为 $\textit{prefixlen}$，那么有 $pat[i] = pat[i+(patlen-\textit{prefixlen})]$．从而得到长度为 $patlen-\textit{prefixlen}$ 的周期，

当我们知道 $pat$ 最长的那一对相等的前缀 - 后缀，我们就得到了 $pat$ 最短的周期．

而最长相等的前后缀长度，$\pi[patlastpos]$，已经在我们在计算 $delta_2$ 的过程中，所以实际不需要额外的预处理时间和空间，就能将后缀匹配算法最坏情况的时间复杂度改善成线性．

??? note "结合上述优化的 BM 的搜索算法最终实现"
    ```rust
    #[cfg(target_pointer_width = "64")]
    const LARGE: usize = 10_000_000_000_000_000_000;
    
    #[cfg(not(target_pointer_width = "64"))]
    const LARGE: usize = 2_000_000_000;
    
    pub struct BMPattern<'a> {
        pat_bytes: &'a [u8],
        delta_1: [usize; 256],
        delta_2: Vec<usize>,
        k: usize  // pat的最短周期长度
    }
    
    impl<'a> BMPattern<'a> {
        // ...
        
        pub fn find_all(&self, string: &str) -> Vec<usize> {
            let mut result = vec![];
            let string_bytes = string.as_bytes();
            let stringlen = string_bytes.len();
            let patlen = self.pat_bytes.len();
            let pat_last_pos = patlen - 1;
            let mut string_index = pat_last_pos;
            let mut pat_index;
            let l0 =  patlen - self.k;
            let mut l = 0;
            
            while string_index < stringlen {
                let old_string_index = string_index;
                
                while string_index < stringlen {
                    string_index += self.delta0(string_bytes[string_index]);
                }
                if string_index < LARGE {
                    break;
                }
                
                string_index -= LARGE;
                
                // 如果string_index发生移动，意味着自从上次成功匹配后发生了至少一次的失败匹配．
                // 此时需要将Galil规则的二次匹配的偏移量归零．
                if old_string_index < string_index {
                    l = 0;
                }
                
                pat_index = pat_last_pos;
                
                while pat_index > l && string_bytes[string_index] == self.pat_bytes[pat_index] {
                    string_index -= 1;
                    pat_index -= 1;
                }
                
                if pat_index == l && string_bytes[string_index] == self.pat_bytes[pat_index] {
                    result.push(string_index - l);
                    
                    string_index += pat_last_pos - l + self.k;
                    l = l0;
                } else {
                    l = 0;
                    string_index += max(
                        self.delta_1[string_bytes[string_index] as usize],
                        self.delta_2[pat_index],
                    );
                }
            }
            
            result
        }
    }
    ```

### 最坏情况在实践中性能影响

从实践的角度上说，理论上的最坏情况并不容易影响性能表现，哪怕是很小的只有 4 的字符集的随机文本测试下这种最坏情况的影响也小到难以观察．

也因此如果没有很好地设计，使用 Galil 法则会拖累一点平均的性能表现，但对于一些极端特殊的 $pat$ 和 $string$ 比如例子中的：$pat$：$\texttt{AAA}$，$string$：$\texttt{AAAAA}\dots$，Galil 规则的应用确实会使得性能表现提高数倍．

## 改进算法

### Simplified Boyer–Moore 算法

BM 算法最复杂的地方就在于 $delta_2$ 表（也就是好后缀表）的构建，而实践中发现，在一般的字符集上的匹配性能主要依靠 $delta_1$ 表（也就是坏字符表），于是出现了仅仅使用 $delta_1$ 表的简化版 BM 算法，通常性能和原版差距很小．

### Boyer–Moore–Horspol 算法

Horspol 算法同样是基于坏字符的规则，在与 $pat$ 尾部对齐的字符上应用 $delta_1$．效果类似于对原版匹配算法的改进，通常性能优于原版本．

???+ note "实现"
    ```rust
    pub struct HorspoolPattern<'a> {
        pat_bytes: &'a [u8],
        bm_bc: [usize; 256],
    }
    
    impl<'a> HorspoolPattern<'a> {
        // ...
        pub fn find_all(&self, string: &str) -> Vec<usize> {
            let mut result = vec![];
            let string_bytes = string.as_bytes();
            let stringlen = string_bytes.len();
            let pat_last_pos = self.pat_bytes.len() - 1;
            let mut string_index = pat_last_pos;
            
            while string_index < stringlen {
                if &string_bytes[string_index-pat_last_pos..string_index+1] == self.pat_bytes {
                    result.push(string_index-pat_last_pos);
                }
                
                string_index += self.bm_bc[string_bytes[string_index] as usize];
            }
            
            result
        }
    }
    ```

### Boyer–Moore–Sunday 算法

Sunday 算法同样是利用坏字符规则，只不过相比 Horspool 它更进一步，直接关注 $pat$ 尾部对齐的那个字符的下一个字符．

实现它只需要稍微修改 $delta_1$ 表，相当于在 $patlen+1$ 长度的 $pat$ 上进行构建．

Sunday 算法通常用作一般情况下实现最简单而且平均表现最好之一的实用算法，通常性能比 Horspool 和 BM 要好一点．

???+ note "实现"
    ```rust
    pub struct SundayPattern<'a> {
        pat_bytes: &'a [u8],
        sunday_bc: [usize; 256],
    }
    
    impl<'a> SundayPattern<'a> {
        // ...
        fn build_sunday_bc(p: &'a [u8]) -> [usize; 256] {
            let mut sunday_bc_table = [p.len() + 1; 256];
            
            for i in 0..p.len() {
                sunday_bc_table[p[i] as usize] = p.len() - i;
            }
            
            sunday_bc_table
        }
        
        pub fn find_all(&self, string: &str) -> Vec<usize> {
            let mut result = vec![];
            let string_bytes = string.as_bytes();
            let pat_last_pos = self.pat_bytes.len() - 1;
            let stringlen = string_bytes.len();
            let mut string_index = pat_last_pos;
            
            while string_index < stringlen {
                if &string_bytes[string_index - pat_last_pos..string_index+1] == self.pat_bytes {
                    result.push(string_index - pat_last_pos);
                }
                
                if string_index + 1 == stringlen {
                    break;
                }
                
                string_index += self.sunday_bc[string_bytes[string_index + 1] as usize];
            }
            
            result
        }
    }
    ```

### BMHBNFS 算法

该算法结合了 Horspool 和 Sunday，是 CPython 实现 `stringlib` 模块时用到的 `find` 的算法[^b5s]，以下简称 B5S．

B5S 基本思路是：

1.  按照后缀匹配的思路，首先比较 $patlastpos$ 位置对应的字符是否相等，如果相等就比较 $0\dots patlastpos-1$ 对应位置的字符是否相等，如果仍然相等，那么就发现一个匹配；

2.  如果任何一个阶段发生不匹配，就进入跳转阶段；

3.  在跳转阶段，首先观察 $patlastpos$ 位置的下一个字符是否在 $pat$ 中，如果不在，直接向右滑动 $patlen+1$，这是 Sunday 算法的最大利用；

    如果这个字符在 $pat$ 中，对 $patlastpos$ 处的字符利用 $delta_1$ 进行 Horspool 跳转．

而根据时间节省还是空间节省为第一目标，算法会有差别巨大的不同实现．

#### 时间节省版本

???+ note "实现"
    ```rust
    pub struct B5STimePattern<'a> {
        pat_bytes: &'a [u8],
        alphabet: [bool;256],
        bm_bc: [usize;256],
        k: usize
    }
    
    impl<'a> B5STimePattern<'a> {
        pub fn new(pat: &'a str) -> Self {
            assert_ne!(pat.len(), 0);
            
            let pat_bytes = pat.as_bytes();
            let (alphabet, bm_bc, k) = B5STimePattern::build(pat_bytes);
            
            B5STimePattern { pat_bytes, alphabet, bm_bc, k }
        }
        
        fn build(p: &'a [u8]) -> ([bool;256], [usize;256], usize)  {
            let mut alphabet = [false;256];
            let mut bm_bc = [p.len(); 256];
            let lastpos = p.len() - 1;
            
            for i in 0..lastpos {
                alphabet[p[i] as usize] = true;
                bm_bc[p[i] as usize] = lastpos - i;
            }
            
            alphabet[p[lastpos] as usize] = true;
            
            (alphabet, bm_bc, compute_k(p))
        }
        
        pub fn find_all(&self, string: &str) -> Vec<usize> {
            let mut result = vec![];
            let string_bytes = string.as_bytes();
            let pat_last_pos = self.pat_bytes.len() - 1;
            let patlen = self.pat_bytes.len();
            let stringlen = string_bytes.len();
            let mut string_index = pat_last_pos;
            let mut offset = pat_last_pos;
            let offset0 = self.k - 1;
            
            while string_index < stringlen {
                if string_bytes[string_index] == self.pat_bytes[pat_last_pos] {
                    if &string_bytes[string_index-offset..string_index] == &self.pat_bytes[pat_last_pos-offset..pat_last_pos] {
                        result.push(string_index-pat_last_pos);
                        
                        offset = offset0;
                        
                        // Galil rule
                        string_index += self.k;
                        continue;
                    }
                }
                
                if string_index + 1 == stringlen {
                    break;
                }
                
                offset = pat_last_pos;
                
                if !self.alphabet[string_bytes[string_index+1] as usize] {
                    string_index += patlen + 1;  // sunday
                } else {
                    string_index += self.bm_bc[string_bytes[string_index] as usize];  // horspool
                }
            }
            
            result
        }
    }
    ```

该版本的 B5S 性能表现非常理想，在目前介绍的后缀匹配系列算法中是通常情况下是最快的．

#### 空间节省版本

同样在 CPython `stringlib` 中实现，使用了两个整数近似取代了字符表和 $delta_1$ 的作用，极大地节省了空间：

1.  用一个简单的 Bloom 过滤器取代字符表（alphabet）

    ???+ note "实现"
        ```rust
        pub struct BytesBloomFilter {
            mask: u64,
        }
        
        impl BytesBloomFilter {
            pub fn new() -> Self {
                SimpleBloomFilter {
                    mask: 0,
                }
            }
            
            fn insert(&mut self, byte: &u8) {
                (self.mask) |= 1u64 << (byte & 63);
            }
            
            fn contains(&self, char: &u8) -> bool {
                (self.mask & (1u64 << (byte & 63))) != 0
            }
        }
        ```

    Bloom 过滤器设设计通过牺牲准确率（实际还有运行时间）来极大地节省存储空间的 `Set` 类型的数据结构，它的特点是会将集合中不存在的项误判为存在（False Positives，简称 FP），但不会把集合中存在的项判断为不存在（False Negatives，简称 FN），因此使用它可能会因为 FP 而没有得到最大的字符跳转，但不会因为 FN 而跳过本应匹配的字符．

    理论上分析，上述「Bloom 过滤器」的实现在 $pat$ 长度在 50 个 Bytes 时，FP 概率约为 0.5，而 $pat$ 长度在 10 个 Bytes 时，FP 概率约为 0.15．

    虽然这不是一个标准的 Bloom 过滤器，首先它实际上没有使用一个真正的哈希函数，实际上它只是一个字符映射，将 0-255 的字节映射为它的前六位构成的数．

    但考虑到我们在内存上的进行字符搜索，这种简化就非常重要，即使用目前已知最快的非加密哈希算法 [xxHash](https://cyan4973.github.io/xxHash/)，计算所需要的时间仍比它高一个数量级．

    另外当 pat 在 30 字节以下时，为了达到最佳的 FP 概率，需要不止一个哈希函数．但这么做意义不大，因为用装有两个 `u128` 数字的数组就已经可以构建字符表的全字符集．

2.  使用 $delta_1(pat[patlastpos])$ 代替整个 $delta_1$

    观察 $delta_1$，最常使用处就是后缀匹配时第一个字符就不匹配是最常见的不匹配的情况，于是令 `skip = delta1(pat[patlastpos])`，

    在第一阶段不匹配时，直接向下滑动 `skip` 个字符；但当第二阶段不配时，因为缺乏整个 $delta_1$ 的信息，只能向下滑动一个字符．

    ???+ note "实现"
        ```rust
        pub struct B5SSpacePattern<'a> {
            pat_bytes: &'a [u8],
            alphabet: BytesBloomFilter,
            skip: usize,
        }
        
        impl<'a> B5SSpacePattern<'a> {
            pub fn new(pat: &'a str) -> Self {
                assert_ne!(pat.len(), 0);
                
                let pat_bytes = pat.as_bytes();
                let (alphabet, skip) = B5SSpacePattern::build(pat_bytes);
                
                B5SSpacePattern { pat_bytes, alphabet, skip}
            }
            
            fn build(p: &'a [u8]) -> (BytesBloomFilter, usize)  {
                let mut alphabet = BytesBloomFilter::new();
                let lastpos = p.len() - 1;
                let mut skip = p.len();
                
                for i in 0..p.len()-1 {
                    alphabet.insert(&p[i]);
                    
                    if p[i] == p[lastpos] {
                        skip = lastpos - i;
                    }
                }
                
                alphabet.insert(&p[lastpos]);
                
                (alphabet, skip)
            }
            
            pub fn find_all(&self, string: &'a str) -> Vec<usize> {
                let mut result = vec![];
                let string_bytes = string.as_bytes();
                let pat_last_pos = self.pat_bytes.len() - 1;
                let patlen = self.pat_bytes.len();
                let stringlen = string_bytes.len();
                let mut string_index = pat_last_pos;
                
                while string_index < stringlen {
                    if string_bytes[string_index] == self.pat_bytes[pat_last_pos] {
                        if &string_bytes[string_index-pat_last_pos..string_index] == &self.pat_bytes[..patlen-1] {
                            result.push(string_index-pat_last_pos);
                        }
                        
                        if string_index + 1 == stringlen {
                            break;
                        }
                        
                        if !self.alphabet.contains(&string_bytes[string_index+1]) {
                            string_index += patlen + 1;  // sunday
                        } else {
                            string_index += self.skip;  // horspool
                        }
                    } else {
                        if string_index + 1 == stringlen {
                            break;
                        }
                        
                        if !self.alphabet.contains(&string_bytes[string_index+1]) {
                            string_index += patlen + 1;  // sunday
                        } else {
                            string_index += 1;
                        }
                    }
                
                }
                
                result
            }
        }
        ```

    这个版本的算法相较于前面的后缀匹配算法不够快，但差距不大，性能仍然优于 KMP，得益于它至多两个 `u64` 的整数的优秀空间复杂度．

## 理论分析

以下是一般字符集下各算法的表现，纵坐标类似于执行开销（cost 指匹配成功 m 个字符后失配时的代价，skip 指发生失配时向下滑动 k 个字符的概率），越小性能越好．横坐标为模式字符串 pat 的长度：

![字符串搜索算法性能对比图](./images/BM/plot256.svg)

在较小字符集（DNA {A, C, T, G} 碱基对序列）中的表现：

![小字符集下字符串搜索算法性能对比图](./images/BM/plot4.svg)

综上，在较大的字符集，比如日常搜索的过程中，BoyerMoore 系列算法的优越表现，其中主要依赖 $delta_1$ 表实现字符跳转；

另一方面，在较小的字符集里，$delta_1$ 的作用下降，而 $delta_2$ 的作用得到了体现．

如果有一定富裕空间的情况下，完整的空间复杂度为 $O(m)$ 的 BoyerMoore 算法更加通用，综合表现最优．

## 参考资料与注释

[^bm]: [1977 年 Boyer–Moore 算法论文](https://dl.acm.org/doi/10.1145/359842.359859)

[^kmp]: [1977 年 KMP 算法论文](https://epubs.siam.org/doi/abs/10.1137/0206024)

[^rytter]: [1980 年 Rytter 纠正 Knuth 的论文](https://epubs.siam.org/doi/10.1137/0209037)

[^galil-rule]: [1979 年介绍 Galil 算法的论文](https://doi.org/10.1145%2F359146.359148)

[^b5s]: [B5S 算法的介绍](http://effbot.org/zone/stringlib.htm#BMHBNFS)


## string/general-sam.md

## 前置知识

广义后缀自动机基于下面的知识点

-   [字典树（Trie 树）](./trie.md)
-   [后缀自动机](./sam.md)

请务必对上述两个知识点非常熟悉之后，再来阅读本文，特别是对于 **后缀自动机** 中的 **后缀链接** 能够有一定的理解

## 引入

### 起源

广义后缀自动机是由刘研绎在其 2015 国家队论文《后缀自动机在字典树上的拓展》上提出的一种结构，即将后缀自动机直接建立在字典树上．

> 大部分可以用后缀自动机处理的字符串的问题均可扩展到 Trie 树上．——刘研绎

### 约定

参考 [字符串约定](./basic.md)

字符串个数为 $k$ 个，即 $S_1, S_2, S_3 \dots S_k$

约定字典树和广义后缀自动机的根节点为 $0$ 号节点

### 概述

后缀自动机 (suffix automaton, SAM) 是用于处理单个字符串的子串问题的强力工具．

而广义后缀自动机 (General Suffix Automaton) 则是将后缀自动机整合到字典树中来解决对于多个字符串的子串问题

## 常见的伪广义后缀自动机

1.  通过用特殊符号将多个串直接连接后，再建立 SAM
2.  对每个串，重复在同一个 SAM 上进行建立，每次建立前，将 `last` 指针置零

方法 1 和方法 2 的实现方式简单，而且在面对题目时通常可以达到和广义后缀自动机一样的正确性．所以在网络上很多人会选择此类写法，例如在后缀自动机一文中最后一个应用，便使用了方法 1 [（原文链接）](./sam.md)

但是无论方法 1 还是方法 2，其时间复杂度较为危险

## 构造广义后缀自动机

根据原论文的描述，应当在多个字符串上先建立字典树，然后在字典树的基础上建立广义后缀自动机．

### 字典树的使用

首先应对多个串创建一棵字典树，这不是什么难事，如果你已经掌握了前置知识的前提下，可以很快的建立完毕．这里为了统一上下文的代码，给出一个可能的字典树代码．

??? note "实现"
    ```cpp
    constexpr int MAXN = 2000000;
    constexpr int CHAR_NUM = 30;
    
    struct Trie {
      int next[MAXN][CHAR_NUM];  // 转移
      int tot;                   // 节点总数：[0, tot)
    
      void init() { tot = 1; }
    
      int insertTrie(int cur, int c) {
        if (next[cur][c]) return next[cur][c];
        return next[cur][c] = tot++;
      }
    
      void insert(const string &s) {
        int root = 0;
        for (auto ch : s) root = insertTrie(root, ch - 'a');
      }
    };
    ```

这里我们得到了一棵依赖于 `next` 数组建立的一棵字典树．

### 后缀自动机的建立

如果我们把这样一棵树直接认为是一个后缀自动机，则我们可以得到如下结论

-   对于节点 `i`，其 `len[i]` 和它在字典树中的深度相同
-   如果我们对字典树进行拓扑排序，我们可以得到一串根据 `len` 不递减的序列．BFS 的结果相同

而后缀自动机在建立的过程中，可以视为不断的插入 `len` 严格递增的值，且差值为 $1$．所以我们可以将对字典树进行拓扑排序后的结果做为一个队列，然后按照这个队列的顺序不断地插入到后缀自动机中．

由于在普通后缀自动机上，其前一个节点的 `len` 值为固定值，即为 `last` 节点的 `len`．但是在广义后缀自动机中，插入的队列是一个不严格递增的数列．所以对于每一个值，对于它的 `last` 应该是已知而且固定的，在字典树上，即为其父亲节点．

由于在字典树中，已经建立了一个近似的后缀自动机，所以只需要对整个字典树的结构进行一定的处理即可转化为广义后缀自动机．我们可以按照前面提出的队列顺序来对整个字典树上的每一个节点进行更新操作．最终我们可以得到广义后缀自动机．

对于每个点的更新操作，我们可以稍微修改一下 SAM 中的插入操作来得到．

对于整个插入的过程，需要注意的是，由于插入是按照 `len` 不递减的顺序插入，在进行 `clone` 后的数据复制过程中，不可以复制其 `len` 小于当前 `len` 的数据．

### 过程

根据上述的逻辑，可以将整个构建过程描述为如下操作

1.  将所有字符串插入到字典树中
2.  从字典树的根节点开始进行 BFS，记录下顺序以及每个节点的父亲节点
3.  将得到的 BFS 序列按照顺序，对每个节点在原字典树上进行构建，注意不能将 `len` 小于当前 `len` 的数据进行操作

### 对操作次数为线性的证明

由于仅处理 BFS 得到的序列，可以保证字典树上所有节点仅经过一次．

对于最坏情况，考虑字典树本身节点个数最多的情况，即任意两个字符串没有相同的前缀，则节点个数为 $\sum_{i=1}^{k}|S_i|$，即所有的字符串长度之和．

而在后缀自动机的更新操作的复杂度已经在 [后缀自动机](./sam.md) 中证明

所以可以证明其最坏复杂度为线性

而通常伪广义后缀自动机的平均复杂度等同于广义后缀自动机的最差复杂度，面对大量的字符串时，伪广义后缀自动机的效率远不如标准的广义后缀自动机

### 实现

对插入函数进行少量必要的修改即可得到所需要的函数

??? note "参考代码"
    ```cpp
    struct GSA {
      int len[MAXN];             // 节点长度
      int link[MAXN];            // 后缀链接，link
      int next[MAXN][CHAR_NUM];  // 转移
      int tot;                   // 节点总数：[0, tot)
    
      int insertSAM(int last, int c) {
        int cur = next[last][c];
        len[cur] = len[last] + 1;
        int p = link[last];
        while (p != -1) {
          if (!next[p][c])
            next[p][c] = cur;
          else
            break;
          p = link[p];
        }
        if (p == -1) {
          link[cur] = 0;
          return cur;
        }
        int q = next[p][c];
        if (len[p] + 1 == len[q]) {
          link[cur] = q;
          return cur;
        }
        int clone = tot++;
        for (int i = 0; i < CHAR_NUM; ++i)
          next[clone][i] = len[next[q][i]] != 0 ? next[q][i] : 0;
        len[clone] = len[p] + 1;
        while (p != -1 && next[p][c] == q) {
          next[p][c] = clone;
          p = link[p];
        }
        link[clone] = link[q];
        link[cur] = clone;
        link[q] = clone;
        return cur;
      }
    
      void build() {
        queue<pair<int, int>> q;
        for (int i = 0; i < CHAR_NUM; ++i)
          if (next[0][i]) q.push({i, 0});
        while (!q.empty()) {
          auto item = q.front();
          q.pop();
          auto last = insertSAM(item.second, item.first);
          for (int i = 0; i < CHAR_NUM; ++i)
            if (next[last][i]) q.push({i, last});
        }
      }
    }
    ```

-   由于整个 BFS 的过程得到的顺序，其父节点始终在变化，所以并不需要保存 `last` 指针．
-   插入操作中，`int cur = next[last][c];` 与正常后缀自动机的 `int cur = tot++;` 有差异，因为我们插入的节点已经在树型结构中完成了，所以只需要直接获取即可
-   在 `clone` 后的数据拷贝中，有这样的判断 `next[clone][i] = len[next[q][i]] != 0 ? next[q][i] : 0;` 这与正常的后缀自动机的直接赋值 `next[clone][i] = next[q][i];` 有一定差异，此次是为了避免更新了 `len` 大于当前节点的值．由于数组中 `len` 当且仅当这个值被 BFS 遍历并插入到后缀自动机后才会被赋值

## 性质

1.  广义后缀自动机与后缀自动机的结构一致，在后缀自动机上的性质绝大部分均可在广义后缀自动机上生效（[后缀自动机的性质](./sam.md)）
2.  当广义后缀自动机建立后，通常字典树结构将会被破坏，即通常不可以用广义后缀自动机来解决字典树问题．当然也可以选择准备双倍的空间，将后缀自动机建立在另外一个空间上．

## 应用

### 所有字符中不同子串个数

可以根据后缀自动机的性质得到，以点 $i$ 为结束节点的子串个数等于 $len[i] - len[link[i]]$

所以可以遍历所有的节点求和得到

例题：[【模板】广义后缀自动机（广义 SAM）](https://www.luogu.com.cn/problem/P6139)

??? note "参考代码"
    ```cpp
    --8<-- "docs/string/code/general-sam/general-sam_1.cpp"
    ```

### 多个字符串间的最长公共子串

我们需要对每个节点建立一个长度为 $k$ 的数组 `flag`（对于本题而言，可以仅为标记数组，若需要求出此子串的个数，则需要改成计数数组）

在字典树插入字符串时，对所有节点进行计数，保存在当前字符串所在的数组

然后按照 `len` 递减的顺序遍历，通过后缀链接将当前节点的 `flag` 与其他节点的合并

遍历所有的节点，找到一个 `len` 最大且满足对于所有的 `k`，其 `flag` 的值均为非 $0$ 的节点，此节点的 $len$ 即为解

例题：[SPOJ Longest Common Substring II](https://www.spoj.com/problems/LCS2/)

??? note "参考代码"
    ```cpp
    --8<-- "docs/string/code/general-sam/general-sam_2.cpp"
    ```


## string/hash.md

## 定义

我们定义一个把字符串映射到整数的函数 $f$，这个 $f$ 称为是 Hash 函数．

我们希望这个函数 $f$ 可以方便地帮我们判断两个字符串是否相等．

## Hash 的思想

Hash 的核心思想在于，将输入映射到一个值域较小、可以方便比较的范围．

??? warning "Warning"
    这里的「值域较小」在不同情况下意义不同．
    
    在 [哈希表](../ds/hash.md) 中，值域需要小到能够接受线性的空间与时间复杂度．
    
    在字符串哈希中，值域需要小到能够快速比较（$10^9$、$10^{18}$ 都是可以快速比较的）．
    
    同时，为了降低哈希冲突率，值域也不能太小．

## 性质

具体来说，哈希函数最重要的性质可以概括为下面两条：

1.  在 Hash 函数值不一样的时候，两个字符串一定不一样；

2.  在 Hash 函数值一样的时候，两个字符串不一定一样（但有大概率一样，且我们当然希望它们总是一样的）．

    我们将 Hash 函数值一样但原字符串不一样的现象称为哈希碰撞．

## 解释

我们需要关注的是什么？

时间复杂度和 Hash 的准确率．

通常我们采用的是多项式 Hash 的方法，对于一个长度为 $l$ 的字符串 $s$ 来说，我们可以这样定义多项式 Hash 函数：$f(s) = \sum_{i=1}^{l} s[i] \times b^{l-i} \pmod M$．例如，对于字符串 $xyz$，其哈希函数值为 $xb^2+yb+z$．

特别要说明的是，也有很多人使用的是另一种 Hash 函数的定义，即 $f(s) = \sum_{i=1}^{l} s[i] \times b^{i-1} \pmod M$，这种定义下，同样的字符串 $xyz$ 的哈希值就变为了 $x+yb+zb^2$ 了．

显然，上面这两种哈希函数的定义函数都是可行的，但二者在之后会讲到的计算子串哈希值时所用的计算式是不同的，因此千万注意 **不要弄混了这两种不同的 Hash 方式**．

由于前者的 Hash 定义计算更简便、使用人数更多、且可以类比为一个 $b$ 进制数来帮助理解，所以本文下面所将要讨论的都是使用 $f(s) = \sum_{i=1}^{l} s[i] \times b^{l-i} \pmod M$ 来定义的 Hash 函数．

还有，有时为了方便和扩大模数，我们在 C++ 中我们会使用 `unsigned long long` 来定义 Hash 函数的结果．由于 C++ 的特性，我们相当于把模数 $M$ 定为 $2^{64}$，也是一个不错的选择．

准确率会在后面讨论．

## Hash 的错误率分析

### Hash 冲突

Hash 冲突是指两个不同的字符串映射到相同的 Hash 值．

我们设 Hash 的取值空间（所有可能出现的字符串的数量）为 $d$，计算次数（要计算的字符串数量）为 $n$．

则 Hash 冲突的概率为：

$$
p(n,d) = 1 - \frac{d!}{d^n\left(d-n\right)!} \approx 1 - \exp(-\frac{n(n-1)}{2d} )
$$

??? note "证明"
    当 Hash 中每个值生成概率相同时，Hash 不冲突的概率为：
    
    $$
    \overline{p}(n,d) = 1 \cdot \left (1 - \frac{1}{d} \right) \cdot \left ( 1- \frac{2}{d}\right) \cdots \left ( 1- \frac{n-1}{d}\right)
    $$
    
    化简得到：
    
    $$
    \begin{aligned}
    \overline{p}(n,d) 
    & = \frac{d}{d}\cdot \frac{d-1}{d}\cdot \frac{d-2}{d} \cdots \frac{d-n+1}{d}\\
    & = \frac{d\cdot (d-1)\cdot (d-2)\cdots(d-n+1)}{d^n}\\
    & = \frac{d!}{d^n\left(d-n\right)!}
    \end{aligned}
    $$
    
    则 Hash 冲突的概率为：
    
    $$
    p(n,d) = 1 - \frac{d!}{d^n\left(d-n\right)!}
    $$
    
    这个公式还是太复杂了，我们进一步化简．
    
    根据泰勒公式：
    
    $$
    \exp(x) = \sum_{k=0}^{\infty}\frac{x^k}{k!}=1+x+\frac{x^2}{2}+\frac{x^3}{6}+\frac{x^4}{24}+\cdots
    $$
    
    当 $x$ 为一个极小值时，$\exp(x)$ 趋近于 $1+x$．
    
    将它带入 Hash 不冲突的原始公式：
    
    $$
    \overline{p}(n,d) \approx 1 \cdot \exp(-\frac{1}{d}) \cdot \exp(-\frac{2}{d}) \cdots \exp(-\frac{n-1}{d})
    $$
    
    化简：
    
    $$
    \begin{aligned}
    \overline{p}(n,d) & \approx \exp(-\frac{1}{d} - \frac{2}{d} - \cdots -\frac{n-1}{d})\\
    &=\exp(-\frac{n(n-1)}{2d} )
    \end{aligned}
    $$
    
    则 Hash 冲突的概率为：
    
    $$
    p(n,d) \approx 1 - \exp(-\frac{n(n-1)}{2d})
    $$

### 卡大模数 Hash

注意到这个公式：

$$
p(n,d) \approx 1 - \exp(-\frac{n(n-1)}{2d} )
$$

为了卡掉 Hash，我们要满足以下条件：

1.  $d$ 要大于模数．
2.  $1-p(d,n)$ 要尽量小．

举个例子：

若字符集为 **大小写字母和数字**，模数为 $10^9+7$ 时：

$\log_{62}10^9+7\approx 6$

$p(10^6,62^{6}) \approx 0.9$

所以对于这个范围，我们随机生成 $10^6$ 个长度为 $6$ 的字符串，它们 Hash 值相同的概率高达 $90\%$．

### 卡自然溢出 Hash

这种 Hash 由于模数太大，用上面的方法卡不了，所以我们需要另一种方法．

首先，这种 Hash 是形如 $f(s) = \sum_{i=1}^{l} s[i] \times b^{l-i}$，我们根据 $b$ 来分类讨论．

#### b 为偶数

此时 $f(s) = s_1\cdot b^l + s_2\cdot b^{l-1} + \cdots + s_l\cdot b \pmod M$，其中 $M$ 为 $2^{64}$．

容易发现若 $l \ge 64$，$s_i\cdot b^l \equiv 0 \pmod M$．

所以我们只要构造形如：

`aaa...a`

`baa...a`

且长度大于 $64$ 的字符串就能冲突．

#### b 为奇数

定义 $!s_i$ 为把 $s_i$ 中所有字符反转．

例：

$s_i = abaab$

$!s_i = babba$

即把 `a` 变成 `b`，把 `b` 变成 `a`．

再定义 $hash_i$ 为 $s_i$ 的 Hash 值，$!hash_i$ 为 $!s_i$ 的 Hash 值．

不断构造 $s_i = s_{i-1} + !s_{i-1}$．

$s_{12}$ 和 $!s_{12}$ 就是我们要的两个字符串．

??? note "推导"
    首先，有：
    
    $$
    \begin{aligned}
    hash_i = hash_{i-1}\cdot base^{2^{i-2}} + !hash_{i-1}\\
    !hash_{i} = !hash_{i-1}\cdot base^{2^{i-2}}+hash_{i-1}
    \end{aligned}
    $$
    
    尝试相减：
    
    $$
    \begin{aligned}
    &hash_i - !hash_i\\
    =\ &hash_{i-1}\cdot base^{2^{i-2}} + !hash_{i-1}-(!hash_{i-1}\cdot base^{2^{i-2}}+hash_{i-1})\\
    =\ &(hash_{i-1}-!hash_{i-1})\cdot (base^{2^{i-2}}-1)
    \end{aligned}
    $$
    
    发现出现了 $2^i$，但是原式太复杂，尝试换元：
    
    设：
    
    $$
    \begin{aligned}
    f_i = hash_i - !hash_i\\
    g_i = base^{2^{i-2}}-1
    \end{aligned}
    $$
    
    根据原式得：
    
    $$
    \begin{aligned}
    f_i &= f_{i-1} \cdot g_i\\
        &=f_1 \cdot g_1 \cdot g_2 \cdots g_{i-1}\\
    \end{aligned}
    $$
    
    因为 $base^{2^{i-2}}$ 一定是奇数，所以 $g_i$ 一定是偶数．
    
    所以：
    
    $$
    2^{i-1} | f_i
    $$
    
    但这样太大了，$i-1\ge 64$ 才能卡掉，继续化简：
    
    $$
    g_i = base^{2^{i-2}}-1 = (base^{2^{i-3}}-1)\cdot(base^{2^{i-3}}+1)\\
    $$
    
    即 $g_i$ 为 $g_{i-1} \cdot c\ (c \equiv 0 \pmod 2)$ 的形式．
    
    所以 $2 | s_1$，$4 | s_2$，……，即
    
    $$
    \begin{aligned}
    & 2^i &| g_i\\
    &2^1\cdot2^2\cdot2^3\cdots2^{i-1} &| f_i\\
    &2^{i(i-1)/2} &| f_i
    \end{aligned}
    $$
    
    即当 $i=12$ 时就可以使 $2^{64} | hash_i - !hash_i$ 达到要求．

### 例题

???+ note "[例题：BZOJ 3097 Hash Killer I](https://hydro.ac/p/bzoj-P3097)"
    给定一个用 **自然溢出** 实现的 Hash，要求构造一个字符串来卡掉它．

???+ note "[例题：BZOJ 3097 Hash Killer II](https://hydro.ac/p/bzoj-P3098)"
    给定一个用 **大模数** 实现的 Hash，要求构造一个字符串来卡掉它．

???+ note "[例题：洛谷 U461211 字符串 Hash（数据加强）](https://www.luogu.com.cn/problem/U461211)"
    给定 $n$ 个字符串，判断不同的字符串有多少个．

## Hash 的改进

### 多值 Hash

看了上面这么多的卡法，当然也有解决办法．

多值 Hash，就是有多个 Hash 函数，每个 Hash 函数的模数不一样，这样就能解决 Hash 冲突的问题．

判断时只要有其中一个的 Hash 值不同，就认为两个字符串不同，若 Hash 值都相同，则认为两个字符串相同．

一般来说，双值 Hash 就够用了．

### 多次询问子串哈希

单次计算一个字符串的哈希值复杂度是 $O(n)$，其中 $n$ 为串长，与暴力匹配没有区别，如果需要多次询问一个字符串的子串的哈希值，每次重新计算效率非常低下．

一般采取的方法是对整个字符串先预处理出每个前缀的哈希值，将哈希值看成一个 $b$ 进制的数对 $M$ 取模的结果，这样的话每次就能快速求出子串的哈希了：

令 $f_i(s)$ 表示 $f(s[1..i])$，即原串长度为 $i$ 的前缀的哈希值，那么按照定义有 $f_i(s)=s[1]\cdot b^{i-1}+s[2]\cdot b^{i-2}+\dots+s[i-1]\cdot b+s[i]$

现在，我们想要用类似前缀和的方式快速求出 $f(s[l..r])$，按照定义有字符串 $s[l..r]$ 的哈希值为 $f(s[l..r])=s[l]\cdot b^{r-l}+s[l+1]\cdot b^{r-l-1}+\dots+s[r-1]\cdot b+s[r]$

对比观察上述两个式子，我们发现 $f(s[l..r])=f_r(s)-f_{l-1}(s) \times b^{r-l+1}$ 成立（可以手动代入验证一下），因此我们用这个式子就可以快速得到子串的哈希值．其中 $b^{r-l+1}$ 可以 $O(n)$ 的预处理出来然后 $O(1)$ 的回答每次询问（当然也可以快速幂 $O(\log n)$ 的回答每次询问）．

## 实现

### 模数 Hash：

注：效率较低，实际使用中不推荐．

=== "C++"
    ```cpp
    using std::string;
    
    constexpr int M = 1e9 + 7;
    constexpr int B = 233;
    
    using ll = long long;
    
    int get_hash(const string& s) {
      int res = 0;
      for (int i = 0; i < s.size(); ++i) {
        res = ((ll)res * B + s[i]) % M;
      }
      return res;
    }
    
    bool cmp(const string& s, const string& t) {
      return get_hash(s) == get_hash(t);
    }
    ```

=== "Python"
    ```python
    M = int(1e9 + 7)
    B = 233
    
    
    def get_hash(s):
        res = 0
        for char in s:
            res = (res * B + ord(char)) % M
        return res
    
    
    def cmp(s, t):
        return get_hash(s) == get_hash(t)
    ```

### 双值 Hash：

=== "C++"
    ```cpp
    using ull = unsigned long long;
    ull base = 131;
    ull mod1 = 212370440130137957, mod2 = 1e9 + 7;
    
    ull get_hash1(std::string s) {
      int len = s.size();
      ull ans = 0;
      for (int i = 0; i < len; i++) ans = (ans * base + (ull)s[i]) % mod1;
      return ans;
    }
    
    ull get_hash2(std::string s) {
      int len = s.size();
      ull ans = 0;
      for (int i = 0; i < len; i++) ans = (ans * base + (ull)s[i]) % mod2;
      return ans;
    }
    
    bool cmp(const std::string s, const std::string t) {
      bool f1 = get_hash1(s) != get_hash1(t);
      bool f2 = get_hash2(s) != get_hash2(t);
      return f1 || f2;
    }
    ```

=== "Python"
    ```python
    def get_hash1(s: str) -> int:
        base = 131
        mod1 = 212370440130137957
        ans = 0
        for char in s:
            ans = (ans * base + ord(char)) % mod1
        return ans
    
    
    def get_hash2(s: str) -> int:
        base = 131
        mod2 = 1000000007
        ans = 0
        for char in s:
            ans = (ans * base + ord(char)) % mod2
        return ans
    
    
    def cmp(s: str, t: str) -> bool:
        f1 = get_hash1(s) != get_hash1(t)
        f2 = get_hash2(s) != get_hash2(t)
        return f1 or f2
    ```

## Hash 的应用

### 字符串匹配

求出模式串的哈希值后，求出文本串每个长度为模式串长度的子串的哈希值，分别与模式串的哈希值比较即可．

### 允许 $k$ 次失配的字符串匹配

问题：给定长为 $n$ 的源串 $s$，以及长度为 $m$ 的模式串 $p$，要求查找源串中有多少子串与模式串匹配．$s'$ 与 $s$ 匹配，当且仅当 $s'$ 与 $s$ 长度相同，且最多有 $k$ 个位置字符不同．其中 $1\leq n,m\leq 10^6$，$0\leq k\leq 5$．

这道题无法使用 KMP 解决，但是可以通过哈希 + 二分来解决．

枚举所有可能匹配的子串，假设现在枚举的子串为 $s'$，通过哈希 + 二分可以快速找到 $s'$ 与 $p$ 第一个不同的位置．之后将 $s'$ 与 $p$ 在这个失配位置及之前的部分删除掉，继续查找下一个失配位置．这样的过程最多发生 $k$ 次．

总的时间复杂度为 $O(m+kn\log_2m)$．

### 最长回文子串

二分答案，判断是否可行时枚举回文中心（对称轴），哈希判断两侧是否相等．需要分别预处理正着和倒着的哈希值．时间复杂度 $O(n\log n)$．

这个问题可以使用 [manacher 算法](./manacher.md) 在 $O(n)$ 的时间内解决．

通过哈希同样可以 $O(n)$ 解决这个问题，具体方法就是记 $R_i$ 表示以 $i$ 作为结尾的最长回文的长度，那么答案就是 $\max_{i=1}^nR_i$．考虑到 $R_i\leq R_{i-1}+2$，因此我们只需要暴力从 $R_{i-1}+2$ 开始递减，直到找到第一个回文即可．记变量 $z$ 表示当前枚举的 $R_i$，初始时为 $0$，则 $z$ 在每次 $i$ 增大的时候都会增大 $2$，之后每次暴力循环都会减少 $1$，故暴力循环最多发生 $2n$ 次，总的时间复杂度为 $O(n)$．

### 最长公共子字符串

问题：给定 $m$ 个总长不超过 $n$ 的非空字符串，查找所有字符串的最长公共子字符串，如果有多个，任意输出其中一个．其中 $1\leq m, n\leq 10^6$．

很显然如果存在长度为 $k$ 的最长公共子字符串，那么 $k-1$ 的公共子字符串也必定存在．因此我们可以二分最长公共子字符串的长度．假设现在的长度为 $k$，`check(k)` 的逻辑为我们将所有字符串的长度为 $k$ 的子串分别进行哈希，将哈希值放入 $n$ 个哈希表中存储．之后求交集即可．

时间复杂度为 $O(m+n\log n)$．

### 确定字符串中不同子字符串的数量

问题：给定长为 $n$ 的字符串，仅由小写英文字母组成，查找该字符串中不同子串的数量．

为了解决这个问题，我们遍历了所有长度为 $l=1,\cdots ,n$ 的子串．对于每个长度为 $l$，我们将其 Hash 值乘以相同的 $b$ 的幂次方，并存入一个数组中．数组中不同元素的数量等于字符串中长度不同的子串的数量，并此数字将添加到最终答案中．

为了方便起见，我们将使用 $h [i]$ 作为 Hash 的前缀字符，并定义 $h[0]=0$．

??? note "参考代码"
    ```cpp
    int count_unique_substrings(string const& s) {
      int n = s.size();
    
      constexpr static int b = 31;
      constexpr static int m = 1e9 + 9;
      vector<long long> b_pow(n);
      b_pow[0] = 1;
      for (int i = 1; i < n; i++) b_pow[i] = (b_pow[i - 1] * b) % m;
    
      vector<long long> h(n + 1, 0);
      for (int i = 0; i < n; i++)
        h[i + 1] = (h[i] + (s[i] - 'a' + 1) * b_pow[i]) % m;
    
      int cnt = 0;
      for (int l = 1; l <= n; l++) {
        set<long long> hs;
        for (int i = 0; i <= n - l; i++) {
          long long cur_h = (h[i + l] + m - h[i]) % m;
          cur_h = (cur_h * b_pow[n - i - 1]) % m;
          hs.insert(cur_h);
        }
        cnt += hs.size();
      }
      return cnt;
    }
    ```

### 例题

???+ note "[CF1200E Compress Words](http://codeforces.com/contest/1200/problem/E)"
    给你若干个字符串，答案串初始为空．第 $i$ 步将第 $i$ 个字符串加到答案串的后面，但是尽量地去掉重复部分（即去掉一个最长的、是原答案串的后缀、也是第 $i$ 个串的前缀的字符串），求最后得到的字符串．
    
    字符串个数不超过 $10^5$，总长不超过 $10^6$．
    
    ??? note "题解"
        每次需要求最长的、是原答案串的后缀、也是第 $i$ 个串的前缀的字符串．枚举这个串的长度，哈希比较即可．
        
        当然，这道题也可以使用 [KMP 算法](./kmp.md) 解决．
    
    ??? note "参考代码"
        ```cpp
        --8<-- "docs/string/code/hash/hash_1.cpp"
        ```

**本页面部分内容译自博文 [строковый хеш](https://github.com/e-maxx-eng/e-maxx-eng/blob/61aff51f658644424c5e1b717f14fb7bf054ae80/src/string/string-hashing.md) 与其英文翻译版 [String Hashing](https://cp-algorithms.com/string/string-hashing.html)．其中俄文版版权协议为 Public Domain + Leave a Link；英文版版权协议为 CC-BY-SA 4.0．**


## string/kmp.md

author: Ir1d, LeoJacob, Xeonacid, greyqz, StudyingFather, Marcythm, minghu6, Backl1ght

## 字符串前缀和后缀定义

关于字符串前缀、真前缀，后缀、真后缀的定义详见 [字符串基础](./basic.md)

## 前缀函数

### 定义

给定一个长度为 $n$ 的字符串 $s$，其 **前缀函数** 被定义为一个长度为 $n$ 的数组 $\pi$．
其中 $\pi[i]$ 的定义是：

1.  如果子串 $s[0\dots i]$ 有一对相等的真前缀与真后缀：$s[0\dots k-1]$ 和 $s[i - (k - 1) \dots i]$，那么 $\pi[i]$ 就是这个相等的真前缀（或者真后缀，因为它们相等）的长度，也就是 $\pi[i]=k$；
2.  如果不止有一对相等的，那么 $\pi[i]$ 就是其中最长的那一对的长度；
3.  如果没有相等的，那么 $\pi[i]=0$．

简单来说 $\pi[i]$ 就是，子串 $s[0\dots i]$ 最长的相等的真前缀与真后缀的长度．

用数学语言描述如下：

$$
\pi[i] = \max_{k = 0 \dots i}\{k: s[0 \dots k - 1] = s[i - (k - 1) \dots i]\}
$$

特别地，规定 $\pi[0]=0$．

### 过程

举例来说，对于字符串 `abcabcd`，

$\pi[0]=0$，因为 `a` 没有真前缀和真后缀，根据规定为 0

$\pi[1]=0$，因为 `ab` 无相等的真前缀和真后缀

$\pi[2]=0$，因为 `abc` 无相等的真前缀和真后缀

$\pi[3]=1$，因为 `abca` 只有一对相等的真前缀和真后缀：`a`，长度为 1

$\pi[4]=2$，因为 `abcab` 相等的真前缀和真后缀只有 `ab`，长度为 2

$\pi[5]=3$，因为 `abcabc` 相等的真前缀和真后缀只有 `abc`，长度为 3

$\pi[6]=0$，因为 `abcabcd` 无相等的真前缀和真后缀

同理可以计算字符串 `aabaaab` 的前缀函数为 $[0, 1, 0, 1, 2, 2, 3]$．

## 计算前缀函数的朴素算法

### 过程

一个直接按照定义计算前缀函数的算法流程：

-   在一个循环中以 $i = 1\to n - 1$ 的顺序计算前缀函数 $\pi[i]$ 的值（$\pi[0]$ 被赋值为 $0$）．
-   为了计算当前的前缀函数值 $\pi[i]$，我们令变量 $j$ 从最大的真前缀长度 $i$ 开始尝试．
-   如果当前长度下真前缀和真后缀相等，则此时长度为 $\pi[i]$，否则令 j 自减 1，继续匹配，直到 $j=0$．
-   如果 $j = 0$ 并且仍没有任何一次匹配，则置 $\pi[i] = 0$ 并移至下一个下标 $i + 1$．

???+ note "实现"
    具体实现如下：
    
    === "C++"
        ```cpp
        // 注：
        // string substr (size_t pos = 0, size_t len = npos) const;
        vector<int> prefix_function(string s) {
          int n = (int)s.length();
          vector<int> pi(n);
          for (int i = 1; i < n; i++)
            for (int j = i; j >= 0; j--)
              if (s.substr(0, j) == s.substr(i - j + 1, j)) {
                pi[i] = j;
                break;
              }
          return pi;
        }
        ```
    
    === "Python"
        ```python
        def prefix_function(s):
            n = len(s)
            pi = [0] * n
            for i in range(1, n):
                for j in range(i, -1, -1):
                    if s[0:j] == s[i - j + 1 : i + 1]:
                        pi[i] = j
                        break
            return pi
        ```
    
    === "Java"
        ```java
        static int[] prefix_function(String s) {
            int n = s.length();
            int[] pi = new int[n];
            for (int i = 1; i < n; i++) {
                for (int j = i; j >= 0; j--) {
                    if (s.substring(0, j).equals(s.substring(i - j + 1, i + 1))) {
                        pi[i] = j;
                        break;
                    }
                }
            }
            return pi;
        }
        ```

显见该算法的时间复杂度为 $O(n^3)$，具有很大的改进空间．

## 计算前缀函数的高效算法

### 第一个优化

第一个重要的观察是 **相邻的前缀函数值至多增加 $1$**．

参照下图所示，只需如此考虑：当取一个尽可能大的 $\pi[i+1]$ 时，必然要求新增的 $s[i+1]$ 也与之对应的字符匹配，即 $s[i+1]=s[\pi[i]]$, 此时 $\pi[i+1] = \pi[i]+1$．

$$
\underbrace{\overbrace{s_0 ~ s_1 ~ s_2}^{\pi[i] = 3} ~ s_3}_{\pi[i+1] = 4} ~ \dots ~ \underbrace{\overbrace{s_{i-2} ~ s_{i-1} ~ s_{i}}^{\pi[i] = 3} ~ s_{i+1}}_{\pi[i+1] = 4}
$$

所以当移动到下一个位置时，前缀函数的值要么增加一，要么维持不变，要么减少．

???+ note "实现"
    此时的改进的算法为：
    
    === "C++"
        ```cpp
        vector<int> prefix_function(string s) {
          int n = (int)s.length();
          vector<int> pi(n);
          for (int i = 1; i < n; i++)
            for (int j = pi[i - 1] + 1; j >= 0; j--)  // improved: j=i => j=pi[i-1]+1
              if (s.substr(0, j) == s.substr(i - j + 1, j)) {
                pi[i] = j;
                break;
              }
          return pi;
        }
        ```
    
    === "Python"
        ```python
        def prefix_function(s):
            n = len(s)
            pi = [0] * n
            for i in range(1, n):
                for j in range(pi[i - 1] + 1, -1, -1):
                    if s[0:j] == s[i - j + 1 : i + 1]:
                        pi[i] = j
                        break
            return pi
        ```
    
    === "Java"
        ```java
        static int[] prefix_function(String s) {
            int n = s.length();
            int[] pi = new int[n];
            for (int i = 1; i < n; i++) {
                for (int j = pi[i - 1] + 1; j >= 0; j--) {
                    if (s.substring(0, j).equals(s.substring(i - j + 1, i + 1))) {
                        pi[i] = j;
                        break;
                    }
                }
            }
            return pi;
        }
        ```

在这个初步改进的算法中，在计算每个 $\pi[i]$ 时，最好的情况是第一次字符串比较就完成了匹配，也就是说基础的字符串比较次数是 $n-1$ 次．

而由于存在 `j = pi[i-1]+1`（`pi[0]=0`）对于最大字符串比较次数的限制，可以看出每次只有在最好情况才会为字符串比较次数的上限积累 $1$，而每次超过一次的字符串比较消耗的是之后次数的增长空间．

由此我们可以得出字符串比较次数最多的一种情况：至少 $1$ 次字符串比较次数的消耗和最多 $n-2$ 次比较次数的积累，此时字符串比较次数为 $n-1 + n-2 = 2n-3$．

可见经过此次优化，计算前缀函数只需要进行 $O(n)$ 次字符串比较，总复杂度降为了 $O(n^2)$．

### 第二个优化

在第一个优化中，我们讨论了计算 $\pi[i+1]$ 时的最好情况：$s[i+1]=s[\pi[i]]$，此时 $\pi[i+1] = \pi[i]+1$．现在让我们沿着这个思路走得更远一点：讨论当 $s[i+1] \neq s[\pi[i]]$ 时如何跳转．

![](images/prefix_str_1.svg)

如上图所示，失配时，我们希望找到对于子串 $s[0\dots i]$，仅次于 $\pi[i]$ 的第二长度 $j$，使得在位置 $i$ 的前缀性质仍得以保持，也即 $s[0 \dots j - 1] = s[i - j + 1 \dots i]$：

$$
\overbrace{\underbrace{s_0 ~ s_1}_j ~ s_2 ~ s_3}^{\pi[i]} ~ \dots ~ \overbrace{s_{i-3} ~ s_{i-2} ~ \underbrace{s_{i-1} ~ s_{i}}_j}^{\pi[i]} ~ s_{i+1}
$$

如果我们找到了这样的长度 $j$，那么仅需要再次比较 $s[i + 1]$ 和 $s[j]$．如果它们相等，那么就有 $\pi[i + 1] = j + 1$．否则，我们需要找到子串 $s[0\dots i]$ 仅次于 $j$ 的第二长度 $j^{(2)}$，使得前缀性质得以保持，如此反复，直到 $j = 0$．如果 $s[i + 1] \neq s[0]$，则 $\pi[i + 1] = 0$．第二次比较的示意图如下所示

![](images/prefix_str_2.svg)

观察上图可以发现，因为 $s[0\dots \pi[i]-1] = s[i-\pi[i]+1\dots i]$，所以对于 $s[0\dots i]$ 的第二长度 $j$，有这样的性质：

$$
s[0 \dots j - 1] = s[i - j + 1 \dots i]= s[\pi[i]-j\dots \pi[i]-1]
$$

该公式的示意图如下所示：

![](images/prefix_str_3.svg)

也就是说 $j$ 等价于子串 $s[\pi[i]-1]$ 的前缀函数值，对应于上图下半部分，即 $j=\pi[\pi[i]-1]$．同理，次于 $j$ 的第二长度等价于 $s[j-1]$ 的前缀函数值，$j^{(2)}=\pi[j-1]$.

显然我们可以得到一个关于 $j$ 的状态转移方程：$j^{(n)}=\pi[j^{(n-1)}-1], \ \ (j^{(n-1)}>0)$

### 最终算法

所以最终我们可以构建一个不需要进行任何字符串比较，并且只进行 $O(n)$ 次操作的算法．

而且该算法的实现出人意料的短且直观：

???+ note "实现"
    === "C++"
        ```cpp
        vector<int> prefix_function(string s) {
          int n = (int)s.length();
          vector<int> pi(n);
          for (int i = 1; i < n; i++) {
            int j = pi[i - 1];
            while (j > 0 && s[i] != s[j]) j = pi[j - 1];
            if (s[i] == s[j]) j++;
            pi[i] = j;
          }
          return pi;
        }
        ```
    
    === "Python"
        ```python
        def prefix_function(s):
            n = len(s)
            pi = [0] * n
            for i in range(1, n):
                j = pi[i - 1]
                while j > 0 and s[i] != s[j]:
                    j = pi[j - 1]
                if s[i] == s[j]:
                    j += 1
                pi[i] = j
            return pi
        ```
    
    === "Java"
        ```java
        static int[] prefix_function(String s) {
            int n = s.length();
            int[] pi = new int[n];
            for (int i = 1; i < n; i++) {
                int j = pi[i - 1];
                while (j > 0 && s.charAt(i) != s.charAt(j)) {
                    j = pi[j - 1];
                }
                if (s.charAt(i) == s.charAt(j)) {
                    j++;
                }
                pi[i] = j;
            }
            return pi;
        }
        ```

这是一个 **在线** 算法，即其当数据到达时处理它——举例来说，你可以一个字符一个字符的读取字符串，立即处理它们以计算出每个字符的前缀函数值．该算法仍然需要存储字符串本身以及先前计算过的前缀函数值，但如果我们已经预先知道该字符串前缀函数的最大可能取值 $M$，那么我们仅需要存储该字符串的前 $M + 1$ 个字符以及对应的前缀函数值．

## 应用

### 在字符串中查找子串：Knuth–Morris–Pratt 算法

该算法由 Knuth、Pratt 和 Morris 在 1977 年共同发布[^kmp]．该任务是前缀函数的一个典型应用．

#### 过程

给定一个文本 $t$ 和一个字符串 $s$，我们尝试找到并展示 $s$ 在 $t$ 中的所有出现（occurrence）．

为了简便起见，我们用 $n$ 表示字符串 $s$ 的长度，用 $m$ 表示文本 $t$ 的长度．

我们构造一个字符串 $s + \# + t$，其中 $\#$ 为一个既不出现在 $s$ 中也不出现在 $t$ 中的分隔符．接下来计算该字符串的前缀函数．现在考虑该前缀函数除去最开始 $n + 1$ 个值（即属于字符串 $s$ 和分隔符的函数值）后其余函数值的意义．根据定义，$\pi[i]$ 为右端点在 $i$ 且同时为一个前缀的最长真子串的长度，具体到我们的这种情况下，其值为与 $s$ 的前缀相同且右端点位于 $i$ 的最长子串的长度．由于分隔符的存在，该长度不可能超过 $n$．而如果等式 $\pi[i] = n$ 成立，则意味着 $s$ 完整出现在该位置（即其右端点位于位置 $i$）．注意该位置的下标是对字符串 $s + \# + t$ 而言的．

因此如果在某一位置 $i$ 有 $\pi[i] = n$ 成立，则字符串 $s$ 在字符串 $t$ 的 $i - (n - 1) - (n + 1) = i - 2n$ 处出现．下图所示为索引的示意图．

![](./images/strstr_kmp_indices.svg)

正如在前缀函数的计算中已经提到的那样，如果我们知道前缀函数的值永远不超过一特定值，那么我们不需要存储整个字符串以及整个前缀函数，而只需要二者开头的一部分．在我们这种情况下这意味着只需要存储字符串 $s + \#$ 以及相应的前缀函数值即可．我们可以一次读入字符串 $t$ 的一个字符并计算当前位置的前缀函数值．

因此 Knuth–Morris–Pratt 算法（简称 KMP 算法）用 $O(n + m)$ 的时间以及 $O(n)$ 的内存解决了该问题．

???+ note "实现"
    === "C++"
        ```cpp
        vector<int> find_occurrences(string text, string pattern) {
          string cur = pattern + '#' + text;
          int sz1 = text.size(), sz2 = pattern.size();
          vector<int> v;
          vector<int> lps = prefix_function(cur);
          for (int i = sz2 + 1; i <= sz1 + sz2; i++) {
            if (lps[i] == sz2) v.push_back(i - 2 * sz2);
          }
          return v;
        }
        ```
    
    === "Python"
        ```python
        def find_occurrences(t, s):
            cur = s + "#" + t
            sz1, sz2 = len(t), len(s)
            ret = []
            lps = prefix_function(cur)
            for i in range(sz2 + 1, sz1 + sz2 + 1):
                if lps[i] == sz2:
                    ret.append(i - 2 * sz2)
            return ret
        ```
    
    === "Java"
        ```java
        static List<Integer> find_occurrences(String text, String pattern) {
            String cur = pattern + '#' + text;
            int sz1 = text.length(), sz2 = pattern.length();
            List<Integer> v = new ArrayList<>();
            int[] lps = prefix_function(cur);
            for (int i = sz2 + 1; i <= sz1 + sz2; i++) {
                if (lps[i] == sz2) {
                    v.add(i - 2 * sz2);
                }
            }
            return v;
        }
        ```

### 字符串的周期

对字符串 $s$ 和 $0 < p \le |s|$，若 $s[i] = s[i+p]$ 对所有 $i \in [0, |s| - p - 1]$ 成立，则称 $p$ 是 $s$ 的周期．

对字符串 $s$ 和 $0 \le r < |s|$，若 $s$ 长度为 $r$ 的前缀和长度为 $r$ 的后缀相等，就称 $s$ 长度为 $r$ 的前缀是 $s$ 的 border．

由 $s$ 有长度为 $r$ 的 border 可以推导出 $|s|-r$ 是 $s$ 的周期．

根据前缀函数的定义，可以得到 $s$ 所有的 border 长度，即 $\pi[n-1],\pi[\pi[n-1]-1], \ldots$．[^ref1]

所以根据前缀函数可以在 $O(n)$ 的时间内计算出 $s$ 所有的周期．其中，由于 $\pi[n-1]$ 是 $s$ 最长 border 的长度，所以 $n - \pi[n-1]$ 是 $s$ 的最小周期．

### 统计每个前缀的出现次数

在该节我们将同时讨论两个问题．给定一个长度为 $n$ 的字符串 $s$，在问题的第一个变种中我们希望统计每个前缀 $s[0 \dots i]$ 在同一个字符串的出现次数，在问题的第二个变种中我们希望统计每个前缀 $s[0 \dots i]$ 在另一个给定字符串 $t$ 中的出现次数．

首先让我们来解决第一个问题．考虑位置 $i$ 的前缀函数值 $\pi[i]$．根据定义，其意味着字符串 $s$ 一个长度为 $\pi[i]$ 的前缀在位置 $i$ 出现并以 $i$ 为右端点，同时不存在一个更长的前缀满足前述定义．与此同时，更短的前缀可能以该位置为右端点．容易看出，我们遇到了在计算前缀函数时已经回答过的问题：给定一个长度为 $j$ 的前缀，同时其也是一个右端点位于 $i$ 的后缀，下一个更小的前缀长度 $k < j$ 是多少？该长度的前缀需同时也是一个右端点为 $i$ 的后缀．因此以位置 $i$ 为右端点，有长度为 $\pi[i]$ 的前缀，有长度为 $\pi[\pi[i] - 1]$ 的前缀，有长度为 $\pi[\pi[\pi[i] - 1] - 1]$ 的前缀，等等，直到长度变为 $0$．故而我们可以通过下述方式计算答案．

???+ note "实现"
    === "C++"
        ```cpp
        vector<int> ans(n + 1);
        for (int i = 0; i < n; i++) ans[pi[i]]++;
        for (int i = n - 1; i > 0; i--) ans[pi[i - 1]] += ans[i];
        for (int i = 0; i <= n; i++) ans[i]++;
        ```
    
    === "Python"
        ```python
        ans = [0] * (n + 1)
        for i in range(0, n):
            ans[pi[i]] += 1
        for i in range(n - 1, 0, -1):
            ans[pi[i - 1]] += ans[i]
        for i in range(0, n + 1):
            ans[i] += 1
        ```

#### 解释

在上述代码中我们首先统计每个前缀函数值在数组 $\pi$ 中出现了多少次，然后再计算最后答案：如果我们知道长度为 $i$ 的前缀出现了恰好 $\text{ans}[i]$ 次，那么该值必须被叠加至其最长的既是后缀也是前缀的子串的出现次数中．在最后，为了统计原始的前缀，我们对每个结果加 $1$．

现在考虑第二个问题．我们应用来自 Knuth–Morris–Pratt 的技巧：构造一个字符串 $s + \# + t$ 并计算其前缀函数．与第一个问题唯一的不同之处在于，我们只关心与字符串 $t$ 相关的前缀函数值，即 $i \ge n + 1$ 的 $\pi[i]$．有了这些值之后，我们可以同样应用在第一个问题中的算法来解决该问题．

### 一个字符串中本质不同子串的数目

给定一个长度为 $n$ 的字符串 $s$，我们希望计算其本质不同子串的数目．

我们将迭代的解决该问题．换句话说，在知道了当前的本质不同子串的数目的情况下，我们要找出一种在 $s$ 末尾添加一个字符后重新计算该数目的方法．

令 $k$ 为当前 $s$ 的本质不同子串数量．我们添加一个新的字符 $c$ 至 $s$．显然，会有一些新的子串以字符 $c$ 结尾．我们希望对这些以该字符结尾且我们之前未曾遇到的子串计数．

构造字符串 $t = s + c$ 并将其反转得到字符串 $t^{\sim}$．现在我们的任务变为计算有多少 $t^{\sim}$ 的前缀未在 $t^{\sim}$ 的其余任何地方出现．如果我们计算了 $t^{\sim}$ 的前缀函数最大值 $\pi_{\max}$，那么最长的出现在 $s$ 中的前缀其长度为 $\pi_{\max}$．自然的，所有更短的前缀也出现了．

因此，当添加了一个新字符后新出现的子串数目为 $|s| + 1 - \pi_{\max}$．

所以对于每个添加的字符，我们可以在 $O(n)$ 的时间内计算新子串的数目，故最终复杂度为 $O(n^2)$．

值得注意的是，我们也可以重新计算在头部添加一个字符，或者从尾或者头移除一个字符时的本质不同子串数目．

### 字符串压缩

给定一个长度为 $n$ 的字符串 $s$，我们希望找到其最短的「压缩」表示，也即我们希望寻找一个最短的字符串 $t$，使得 $s$ 可以被 $t$ 的一份或多份拷贝的拼接表示．

显然，我们只需要找到 $t$ 的长度即可．知道了该长度，该问题的答案即为长度为该值的 $s$ 的前缀．

让我们计算 $s$ 的前缀函数．通过使用该函数的最后一个值 $\pi[n - 1]$，我们定义值 $k = n - \pi[n - 1]$．我们将证明，如果 $k$ 整除 $n$，那么 $k$ 就是答案，否则不存在一个有效的压缩，故答案为 $n$．

假定 $n$ 可被 $k$ 整除．那么字符串可被划分为长度为 $k$ 的若干块．根据前缀函数的定义，该字符串长度为 $n - k$ 的前缀等于其后缀．但是这意味着最后一个块同倒数第二个块相等，并且倒数第二个块同倒数第三个块相等，等等．作为其结果，所有块都是相等的，因此我们可以将字符串 $s$ 压缩至长度 $k$．

???+ note "证明"
    诚然，我们仍需证明该值为最优解．实际上，如果有一个比 $k$ 更小的压缩表示，那么前缀函数的最后一个值 $\pi[n - 1]$ 必定比 $n - k$ 要大．因此 $k$ 就是答案．
    
    现在假设 $n$ 不可以被 $k$ 整除，我们将通过反证法证明这意味着答案为 $n$[^1]．假设其最小压缩表示 $r$ 的长度为 $p$（$p$ 整除 $n$），字符串 $s$ 被划分为 $n / p \ge 2$ 块．那么前缀函数的最后一个值 $\pi[n - 1]$ 必定大于 $n - p$（如果等于则 $n$ 可被 $k$ 整除），也即其所表示的后缀将部分的覆盖第一个块．现在考虑字符串的第二个块．该块有两种解释：第一种为 $r_0 r_1 \dots r_{p - 1}$，另一种为 $r_{p - k} r_{p - k + 1} \dots r_{p - 1} r_0 r_1 \dots r_{p - k - 1}$．由于两种解释对应同一个字符串，因此可得到 $p$ 个方程组成的方程组，该方程组可简写为 $r_{(i + k) \bmod p} = r_{i \bmod p}$，其中 $\cdot \bmod p$ 表示模 $p$ 意义下的最小非负剩余．
    
    $$
    \begin{gathered}
    \overbrace{r_0 ~ r_1 ~ r_2 ~ r_3 ~ r_4 ~ r_5}^p ~ \overbrace{r_0 ~ r_1 ~ r_2 ~ r_3 ~ r_4 r_5}^p \\
    r_0 ~ r_1 ~ r_2 ~ r_3 ~ \underbrace{\overbrace{r_0 ~ r_1 ~ r_2 ~ r_3 ~ r_4 ~ r_5}^p ~ r_0 ~ r_1}_{\pi[11] = 8}
    \end{gathered}
    $$
    
    根据扩展欧几里得算法我们可以得到一组 $x$ 和 $y$ 使得 $xk + yp = \gcd(k, p)$．通过与等式 $pk - kp = 0$ 适当叠加我们可以得到一组 $x' > 0$ 和 $y' < 0$ 使得 $x'k + y'p = \gcd(k, p)$．这意味着通过不断应用前述方程组中的方程我们可以得到新的方程组 $r_{(i + \gcd(k, p)) \bmod p} = r_{i \bmod p}$．
    
    由于 $\gcd(k, p)$ 整除 $p$，这意味着 $\gcd(k, p)$ 是 $r$ 的一个周期．又因为 $\pi[n - 1] > n - p$，故有 $n - \pi[n - 1] = k < p$，所以 $\gcd(k, p)$ 是一个比 $p$ 更小的 $r$ 的周期．因此字符串 $s$ 有一个长度为 $\gcd(k, p) < p$ 的压缩表示，同 $p$ 的最小性矛盾．
    
    综上所述，不存在一个长度小于 $k$ 的压缩表示，因此答案为 $k$．

[^1]: 在俄文版及英文版中该部分证明均疑似有误．本文章中的该部分证明由作者自行添加．

### 根据前缀函数构建一个自动机

让我们重新回到通过一个分隔符将两个字符串拼接的新字符串．对于字符串 $s$ 和 $t$ 我们计算 $s + \# + t$ 的前缀函数．显然，因为 $\#$ 是一个分隔符，前缀函数值永远不会超过 $|s|$．因此我们只需要存储字符串 $s + \#$ 和其对应的前缀函数值，之后就可以动态计算对于之后所有字符的前缀函数值：

$$
\underbrace{s_0 ~ s_1 ~ \dots ~ s_{n-1} ~ \#}_{\text{need to store}} ~ \underbrace{t_0 ~ t_1 ~ \dots ~ t_{m-1}}_{\text{do not need to store}}
$$

实际上在这种情况下，知道 $t$ 的下一个字符 $c$ 以及之前位置的前缀函数值便足以计算下一个位置的前缀函数值，而不需要用到任何其它 $t$ 的字符和对应的前缀函数值．

换句话说，我们可以构造一个 **自动机**（一个有限状态机）：其状态为当前的前缀函数值，而从一个状态到另一个状态的转移则由下一个字符确定．

因此，即使没有字符串 $t$，我们同样可以应用构造转移表的算法构造一个转移表 $( \text { old } \pi , c ) \rightarrow \text { new } _ { - } \pi$：

???+ note "实现"
    ```cpp
    void compute_automaton(string s, vector<vector<int>>& aut) {
      s += '#';
      int n = s.size();
      vector<int> pi = prefix_function(s);
      aut.assign(n, vector<int>(26));
      for (int i = 0; i < n; i++) {
        for (int c = 0; c < 26; c++) {
          int j = i;
          while (j > 0 && 'a' + c != s[j]) j = pi[j - 1];
          if ('a' + c == s[j]) j++;
          aut[i][c] = j;
        }
      }
    }
    ```

然而在这种形式下，对于小写字母表，算法的时间复杂度为 $O(|\Sigma|n^2)$．注意到我们可以应用动态规划来利用表中已计算过的部分．只要我们从值 $j$ 变化到 $\pi[j - 1]$，那么我们实际上在说转移 $(j, c)$ 所到达的状态同转移 $(\pi[j - 1], c)$ 一样，但该答案我们之前已经精确计算过了．

???+ note "实现"
    ```cpp
    void compute_automaton(string s, vector<vector<int>>& aut) {
      s += '#';
      int n = s.size();
      vector<int> pi = prefix_function(s);
      aut.assign(n, vector<int>(26));
      for (int i = 0; i < n; i++) {
        for (int c = 0; c < 26; c++) {
          if (i > 0 && 'a' + c != s[i])
            aut[i][c] = aut[pi[i - 1]][c];
          else
            aut[i][c] = i + ('a' + c == s[i]);
        }
      }
    }
    ```

最终我们可在 $O(|\Sigma|n)$ 的时间复杂度内构造该自动机．

该自动机在什么时候有用呢？首先，记得大部分时候我们为了一个目的使用字符串 $s + \# + t$ 的前缀函数：寻找字符串 $s$ 在字符串 $t$ 中的所有出现．

因此使用该自动机的最直接的好处是 **加速计算字符串 $s + \# + t$ 的前缀函数**．

通过构建 $s + \#$ 的自动机，我们不再需要存储字符串 $s$ 以及其对应的前缀函数值．所有转移已经在表中计算过了．

但除此以外，还有第二个不那么直接的应用．我们可以在字符串 $t$ 是 **某些通过一些规则构造的巨型字符串** 时，使用该自动机加速计算．Gray 字符串，或者一个由一些短的输入串的递归组合所构造的字符串都是这种例子．

出于完整性考虑，我们来解决这样一个问题：给定一个数 $k \le 10^5$，以及一个长度 $\le 10^5$ 的字符串 $s$，我们需要计算 $s$ 在第 $k$ 个 Gray 字符串中的出现次数．回想起 Gray 字符串以下述方式定义：

$$
\begin{aligned}
g_1 &= \mathtt{a}\\
g_2 &= \mathtt{aba}\\
g_3 &= \mathtt{abacaba}\\
g_4 &= \mathtt{abacabadabacaba}
\end{aligned}
$$

由于其天文数字般的长度，在这种情况下即使构造字符串 $t$ 都是不可能的：第 $k$ 个 Gray 字符串有 $2^k - 1$ 个字符．然而我们可以在仅仅知道开头若干前缀函数值的情况下，有效计算该字符串末尾的前缀函数值．

除了自动机之外，我们同时需要计算值 $G[i][j]$：在从状态 $j$ 开始处理 $g_i$ 后的自动机的状态，以及值 $K[i][j]$：当从状态 $j$ 开始处理 $g_i$ 后，$s$ 在 $g_i$ 中的出现次数．实际上 $K[i][j]$ 为在执行操作时前缀函数取值为 $|s|$ 的次数．易得问题的答案为 $K[k][0]$．

我们该如何计算这些值呢？首先根据定义，初始条件为 $G[0][j] = j$ 以及 $K[0][j] = 0$．之后所有值可以通过先前的值以及使用自动机计算得到．为了对某个 $i$ 计算相应值，回想起字符串 $g_i$ 由 $g_{i - 1}$，字母表中第 $i$ 个字符，以及 $g_{i - 1}$ 三者拼接而成．因此自动机会途径下列状态：

$$
\begin{gathered}
\text{mid} = \text{aut}[G[i - 1][j]][i] \\
G[i][j] = G[i - 1][\text{mid}]
\end{gathered}
$$

$K[i][j]$ 的值同样可被简单计算．

$$
K[i][j] = K[i - 1][j] + [\text{mid} == |s|] + K[i - 1][\text{mid}]
$$

其中 $[\cdot]$ 当其中表达式取值为真时值为 $1$，否则为 $0$．综上，我们已经可以解决关于 Gray 字符串的问题，以及一大类与之类似的问题．举例来说，应用同样的方法可以解决下列问题：给定一个字符串 $s$ 以及一些模式 $t_i$，其中每个模式以下列方式给出：该模式由普通字符组成，当中可能以 $t_{k}^{\text{cnt}}$ 的形式递归插入先前的字符串，也即在该位置我们必须插入字符串 $t_k$ $\text{cnt}$ 次．以下是这些模式的一个例子：

$$
\begin{aligned}
t_1 &= \mathtt{abdeca} \\
t_2 &= \mathtt{abc} + t_1^{30} + \mathtt{abd} \\
t_3 &= t_2^{50} + t_1^{100} \\
t_4 &= t_2^{10} + t_3^{100}
\end{aligned}
$$

递归代入会使字符串长度爆炸式增长，他们的长度甚至可以达到 $100^{100}$ 的数量级．而我们必须找到字符串 $s$ 在每个字符串中的出现次数．

该问题同样可通过构造前缀函数的自动机解决．同之前一样，我们利用先前计算过的结果对每个模式计算其转移然后相应统计答案即可．

## 练习题目

-   [UVa 455 "Periodic Strings"](http://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=396)
-   [UVa 11022 "String Factoring"](http://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=1963)
-   [UVa 11452 "Dancing the Cheeky-Cheeky"](http://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=2447)
-   [UVa 12604 - Caesar Cipher](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=4282)
-   [UVa 12467 - Secret Word](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=3911)
-   [UVa 11019 - Matrix Matcher](https://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=1960)
-   [SPOJ - Pattern Find](http://www.spoj.com/problems/NAJPF/)
-   [Codeforces - Anthem of Berland](http://codeforces.com/contest/808/problem/G)
-   [Codeforces - MUH and Cube Walls](http://codeforces.com/problemset/problem/471/D)

## 参考资料与注释

**本页面主要译自博文 [Префикс-функция. Алгоритм Кнута-Морриса-Пратта](http://e-maxx.ru/algo/prefix_function) 与其英文翻译版 [Prefix function. Knuth–Morris–Pratt algorithm](https://cp-algorithms.com/string/prefix-function.html)．其中俄文版版权协议为 Public Domain + Leave a Link；英文版版权协议为 CC-BY-SA 4.0．**

[^ref1]: [金策 - 字符串算法选讲](https://github.com/hzwer/shareOI/blob/master/%E5%AD%97%E7%AC%A6%E4%B8%B2/%E5%AD%97%E7%AC%A6%E4%B8%B2%E7%AE%97%E6%B3%95%E9%80%89%E8%AE%B2_%E9%87%91%E7%AD%96.pdf)

[^kmp]: Knuth, Donald E., James H. Morris, Jr, and Vaughan R. Pratt. "Fast pattern matching in strings." SIAM journal on computing 6.2 (1977): 323-350.[doi: 10.1137/0206024](https://epubs.siam.org/doi/abs/10.1137/0206024)


## string/lib-func.md

author: Frankaiyou, henrytbtrue, zymooll

## C 标准库

C 标准库操作字符数组 `char[]`/`const char*`．

参见：[fprintf](https://zh.cppreference.com/w/c/io/fprintf)、[fscanf](https://zh.cppreference.com/w/c/io/fscanf)、[空终止字节字符串](https://zh.cppreference.com/w/c/string/byte)

-   `printf("%s", s)`：用 `%s` 来输出一个字符串（字符数组）．
-   `scanf("%s", &s)`：用 `%s` 来读入一个字符串（字符数组）．
-   `sscanf(const char *__source, const char *__format, ...)`：从字符串 `__source` 里读取变量，比如 `sscanf(str,"%d",&a)`．
-   `sprintf(char *__stream, const char *__format, ...)`：将 `__format` 字符串里的内容输出到 `__stream` 中，比如 `sprintf(str,"%d",i)`．
-   `strlen(const char *str)`：返回从 `str[0]` 开始直到 `'\0'` 的字符数．注意，未开启 O2 优化时，该操作写在循环条件中复杂度是 $\Theta(N)$ 的．
-   `strcmp(const char *str1, const char *str2)`：按照字典序比较 `str1 str2` 若 `str1` 字典序小返回负值，两者一样返回 `0`，`str1` 字典序更大则返回正值．请注意，不要简单的认为返回值只有 `0`、`1`、`-1` 三种，在不同平台下的返回值都遵循正负，但并非都是 `0`、`1`、`-1`．
-   `strcpy(char *str, const char *src)`: 把 `src` 中的字符复制到 `str` 中，`str`  `src` 均为字符数组头指针，返回值为 `str` 包含空终止符号 `'\0'`．
-   `strncpy(char *str, const char *src, int cnt)`：复制至多 `cnt` 个字符到 `str` 中，若 `src` 终止而数量未达 `cnt` 则写入空字符到 `str` 直至写入总共 `cnt` 个字符．
-   `strcat(char *str1, const char *str2)`: 将 `str2` 接到 `str1` 的结尾，用 `*str2` 替换 `str1` 末尾的 `'\0'` 返回 `str1`．
-   `strstr(char *str1, const char *str2)`：若 `str2` 是 `str1` 的子串，则返回 `str2` 在 `str1` 的首次出现的地址；如果 `str2` 不是 `str1` 的子串，则返回 `NULL`．
-   `strchr(const char *str, int c)`：找到在字符串 `str` 中第一次出现字符 `c` 的位置，并返回这个位置的地址．如果未找到该字符则返回 `NULL`．
-   `strrchr(const char *str, int c)`：找到在字符串 `str` 中最后一次出现字符 `c` 的位置，并返回这个位置的地址．如果未找到该字符则返回 `NULL`．

## C++ 标准库

C++ 标准库操作字符串对象 [`std::string`](../lang/csl/string.md)，同时也提供对字符数组的兼容．

参见：[std::basic\_string](https://zh.cppreference.com/w/cpp/string/basic_string)、[std::basic\_string\_view](https://zh.cppreference.com/w/cpp/string/basic_string_view)

-   重载了赋值运算符 `+`，当 `+` 两边是 `string/char/char[]/const char*` 类型时，可以将这两个变量连接，返回连接后的字符串（`string`）．
-   赋值运算符 `=` 右侧可以是 `const string/string/const char*/char*`．
-   访问运算符 `[cur]` 返回 `cur` 位置的引用．
-   访问函数 `data()/c_str()` 返回一个 `const char*` 指针，内容与该 `string` 相同．
-   容量函数 `size()` 返回字符串字符个数．
-   `find(ch, start = 0)` 查找并返回从 `start` 开始的字符 `ch` 的位置；`rfind(ch)` 从末尾开始，查找并返回第一个找到的字符 `ch` 的位置（皆从 `0` 开始）（如果查找不到，返回 `-1`）．
-   `substr(start, len)` 可以从字符串的 `start`（从 `0` 开始）截取一个长度为 `len` 的字符串（缺省 `len` 时代码截取到字符串末尾）．
-   `append(s)` 将 `s` 添加到字符串末尾．
-   `append(s, pos, n)` 将字符串 `s` 中，从 `pos` 开始的 `n` 个字符连接到当前字符串结尾．
-   `replace(pos, n, s)` 删除从 `pos` 开始的 `n` 个字符，然后在 `pos` 处插入串 `s`．
-   `erase(pos, n)` 删除从 `pos` 开始的 `n` 个字符．
-   `insert(pos, s)` 在 `pos` 位置插入字符串 `s`．
-   `std::string` 重载了比较逻辑运算符，复杂度是 $\Theta(N)$ 的．


## string/lyndon.md

author: sshwy, StudyingFather, orzAtalod

## 定义

首先我们介绍 Lyndon 分解的概念．

Lyndon 串：对于字符串 $s$，如果 $s$ 的字典序严格小于 $s$ 的所有后缀的字典序，我们称 $s$ 是简单串，或者 **Lyndon 串**．举一些例子，`a`,`b`,`ab`,`aab`,`abb`,`ababb`,`abcd` 都是 Lyndon 串．当且仅当 $s$ 的字典序严格小于它的所有非平凡的（非平凡：非空且不同于自身）循环同构串时，$s$ 才是 Lyndon 串．

Lyndon 分解：串 $s$ 的 Lyndon 分解记为 $s=w_1w_2\cdots w_k$，其中所有 $w_i$ 为简单串，并且他们的字典序按照非严格单减排序，即 $w_1\ge w_2\ge\cdots\ge w_k$．可以发现，这样的分解存在且唯一．

## Duval 算法

### 解释

Duval 可以在 $O(n)$ 的时间内求出一个串的 Lyndon 分解．

首先我们介绍另外一个概念：如果一个字符串 $t$ 能够分解为 $t=ww\cdots\overline{w}$ 的形式，其中 $w$ 是一个 Lyndon 串，而 $\overline{w}$ 是 $w$ 的前缀（$\overline{w}$ 可能是空串），那么称 $t$ 是近似简单串（pre-simple），或者近似 Lyndon 串．一个 Lyndon 串也是近似 Lyndon 串．

Duval 算法运用了贪心的思想．算法过程中我们把串 $s$ 分成三个部分 $s=s_1s_2s_3$，其中 $s_1$ 是一个 Lyndon 串，它的 Lyndon 分解已经记录；$s_2$ 是一个近似 Lyndon 串；$s_3$ 是未处理的部分．

### 过程

整体描述一下，该算法每一次尝试将 $s_3$ 的首字符添加到 $s_2$ 的末尾．如果 $s_2$ 不再是近似 Lyndon 串，那么我们就可以将 $s_2$ 截出一部分前缀（即 Lyndon 分解）接在 $s_1$ 末尾．

我们来更详细地解释一下算法的过程．定义一个指针 $i$ 指向 $s_2$ 的首字符，则 $i$ 从 $1$ 遍历到 $n$（字符串长度）．在循环的过程中我们定义另一个指针 $j$ 指向 $s_3$ 的首字符，指针 $k$ 指向 $s_2$ 中我们当前考虑的字符（意义是 $j$ 在 $s_2$ 的上一个循环节中对应的字符）．我们的目标是将 $s[j]$ 添加到 $s_2$ 的末尾，这就需要将 $s[j]$ 与 $s[k]$ 做比较：

1.  如果 $s[j]=s[k]$，则将 $s[j]$ 添加到 $s_2$ 末尾不会影响它的近似简单性．于是我们只需要让指针 $j,k$ 自增（移向下一位）即可．
2.  如果 $s[j]>s[k]$，那么 $s_2s[j]$ 就变成了一个 Lyndon 串，于是我们将指针 $j$ 自增，而让 $k$ 指向 $s_2$ 的首字符，这样 $s_2$ 就变成了一个循环次数为 1 的新 Lyndon 串了．
3.  如果 $s[j]<s[k]$，则 $s_2s[j]$ 就不是一个近似简单串了，那么我们就要把 $s_2$ 分解出它的一个 Lyndon 子串，这个 Lyndon 子串的长度将是 $j-k$，即它的一个循环节．然后把 $s_2$ 变成分解完以后剩下的部分，继续循环下去（注意，这个情况下我们没有改变指针 $j,k$），直到循环节被截完．对于剩余部分，我们只需要将进度「回退」到剩余部分的开头即可．

### 实现

下面的代码返回串 $s$ 的 Lyndon 分解方案．

=== "C++"
    ```cpp
    // duval_algorithm
    vector<string> duval(string const& s) {
      int n = s.size(), i = 0;
      vector<string> factorization;
      while (i < n) {
        int j = i + 1, k = i;
        while (j < n && s[k] <= s[j]) {
          if (s[k] < s[j])
            k = i;
          else
            k++;
          j++;
        }
        while (i <= k) {
          factorization.push_back(s.substr(i, j - k));
          i += j - k;
        }
      }
      return factorization;
    }
    ```

=== "Python"
    ```python
    # duval_algorithm
    def duval(s):
        n, i = len(s), 0
        factorization = []
        while i < n:
            j, k = i + 1, i
            while j < n and s[k] <= s[j]:
                if s[k] < s[j]:
                    k = i
                else:
                    k += 1
                j += 1
            while i <= k:
                factorization.append(s[i : i + j - k])
                i += j - k
        return factorization
    ```

### 复杂度分析

接下来我们证明一下这个算法的复杂度．

外层的循环次数不超过 $n$，因为每一次 $i$ 都会增加．第二个内层循环也是 $O(n)$ 的，因为它只记录 Lyndon 分解的方案．接下来我们分析一下内层循环．很容易发现，每一次在外层循环中找到的 Lyndon 串是比我们所比较过的剩余的串要长的，因此剩余的串的长度和要小于 $n$，于是我们最多在内层循环 $O(n)$ 次．事实上循环的总次数不超过 $4n-3$，时间复杂度为 $O(n)$．

## 最小表示法（Finding the smallest cyclic shift）

对于长度为 $n$ 的串 $s$，我们可以通过上述算法寻找该串的最小表示法．

我们构建串 $ss$ 的 Lyndon 分解，然后寻找这个分解中的一个 Lyndon 串 $t$，使得它的起点小于 $n$ 且终点大于等于 $n$．可以很容易地使用 Lyndon 分解的性质证明，子串 $t$ 的首字符就是 $s$ 的最小表示法的首字符，即我们沿着 $t$ 的开头往后 $n$ 个字符组成的串就是 $s$ 的最小表示法．

于是我们在分解的过程中记录每一次的近似 Lyndon 串的开头即可．

=== "C++"
    ```cpp
    // smallest_cyclic_string
    string min_cyclic_string(string s) {
      s += s;
      int n = s.size();
      int i = 0, ans = 0;
      while (i < n / 2) {
        ans = i;
        int j = i + 1, k = i;
        while (j < n && s[k] <= s[j]) {
          if (s[k] < s[j])
            k = i;
          else
            k++;
          j++;
        }
        while (i <= k) i += j - k;
      }
      return s.substr(ans, n / 2);
    }
    ```

=== "Python"
    ```python
    # smallest_cyclic_string
    def min_cyclic_string(s):
        s += s
        n = len(s)
        i, ans = 0, 0
        while i < n / 2:
            ans = i
            j, k = i + 1, i
            while j < n and s[k] <= s[j]:
                if s[k] < s[j]:
                    k = i
                else:
                    k += 1
                j += 1
            while i <= k:
                i += j - k
        return s[ans : ans + n / 2]
    ```

## 习题

-   [UVa #719 - Glass Beads](https://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=660)

    **本页面主要译自博文 [Декомпозиция Линдона. Алгоритм Дюваля. Нахождение наименьшего циклического сдвига](http://e-maxx.ru/algo/duval_algorithm) 与其英文翻译版 [Lyndon factorization](https://cp-algorithms.com/string/lyndon_factorization.html)．其中俄文版版权协议为 Public Domain + Leave a Link；英文版版权协议为 CC-BY-SA 4.0．**


## string/main-lorentz.md

## 重串

### 定义

给定一个长度为 $n$ 的字符串 $s$．

我们将一个字符串连续写两遍所产生的新字符串称为 **重串 (tandem repetition)**．下文中，为了表述精准，我们将被重复的这个字符串称为原串．换言之，一个重串等价于一对下标 $(i, j)$，其使得 $s[i \dots j]$ 是两个相同字符串拼接而成的．

你的目标是找出给定的字符串 $s$ 中所有的重串．或者，解决一个较为简单的问题：找到字符串 $s$ 中任意重串或者最长的一个重串．

下文的算法由 Michael Main 和 Richard J. Lorentz 在 1982 年提出．

???+ note "约定"
    下文所有的字符串下标从 $0$ 开始．
    
    下文中，记 $\overline{s}$ 为 $s$ 的反串．如 $\overline{\tt abc} = \tt cba$．

### 解释

考虑字符串 $\tt acababaee$，这个字符串包括三个重串，分别是：

-   $s[2 \dots 5] = \tt abab$
-   $s[3 \dots 6] = \tt baba$
-   $s[7 \dots 8] = \tt ee$

下面是另一个例子，考虑字符串 $\tt abaaba$，这个字符串只有两个重串：

-   $s[0 \dots 5] = \tt abaaba$
-   $s[2 \dots 3] = \tt aa$

### 重串的个数

一个长度为 $n$ 的字符串可能有高达 $O(n^2)$ 个重串，一个显然的例子就是 $n$ 个字母全部相同的字符串，这种情况下，只要其子串长度为偶数，这个子串就是重串．多数情况下，一个周期比较小的周期字符串会有很多重串．

但这并不影响我们在 $O(n \log n)$ 的时间内计算出重串数量．因为这个算法通过某种压缩形式来表达一个重串，使得我们可以将多个重串压缩为一个．

这里有一些关于重串数量的有趣结论：

-   如果一个重串的原串不是重串，则我们称这个重串为 **本原重串 (primitive repetition)**．可以证明，本原重串最多有 $O(n \log n)$ 个．
-   如果我们把一个重串用 Crochemore 三元组 $(i, p, r)$ 进行压缩，其中 $i$ 是重串的起始位置，$p$ 是该重串某个循环节的长度（注意不是原串长度！），$r$ 为这个循环节重复的次数．则某字符串的所有重串可以被 $O(n \log n)$ 个 Crochemore 三元组表示．
-   Fibonacci 字符串定义如下：

$$
\begin{align} t_0 &= a, \\ t_1 &= b, \\ t_i &= t_{i-1} + t_{i-2}, \end{align}
$$

可以发现 Fibonacci 字符串具有高度的周期性．对于长度为 $f_i$ 的 Fibonacci 字符串 $t_i$，即使用 Crochemore 三元组压缩，也有 $O(f_i \log f_i)$ 个三元组．其本原重串的数量也有 $O(f_i \log f_i)$ 个．

## Main–Lorentz 算法

### 解释

Main–Lorentz 算法的核心思想是 **分治**．

这个算法将字符串分为左、右两部分，首先计算完全处于字符串左部（或右部）的重串数量，然后计算起始位置在左部，终止在右部的重串数量．（下文中，我们将这种重串称为 **交叉重串**）

计算交叉重串的数量是 Main–Lorentz 算法的关键点，我们将在下文详细探讨．

### 过程

#### 寻找交叉重串

我们记某字符串的左部为 $u$，右部为 $v$．则 $s = u + v$，且 $u, v$ 的长度大约等于 $s$ 长度的一半．

对于任意一个重串，我们考虑其中间字符．此处我们将一个重串右半边的第一个字符称为其中间字符，换言之，若 $s[i...j]$ 为重串，则其中间字符为 $s[(i + j + 1)/2]$．如果一个重串的中间字符在 $u$ 中，则称这个重串 **左偏 (left)**，反之则称其 **右偏 (right)**．

接下来，我们将会探讨如何找到所有的左偏重串．

我们记一个左边重串的长度为 $2l$．考虑该重串第一个落入 $v$ 的字符（即 $s[|u|]$），这个字符一定与 $u$ 中的某个字符 $u[\textit{cntr}]$ 一致．

我们考虑固定 $\textit{cntr}$，并找到所有符合条件的重串．举个例子：对于字符串 $\tt c \; \underset{\textit{cntr}}{a} \; c \; | \; a \; d \; a$（这个 $\tt |$ 是用于分辨左右两部分的），固定 $cntr = 1$，则我们可以发现重串 $\tt caca$ 符合要求．

显然，我们一旦固定了 $\textit{cntr}$，那我们同时也固定了 $l$ 的取值．我们一旦知道如何找到所有重串，我们就可以从 $0$ 到 $|u| - 1$ 枚举 $\textit{cntr}$ 的取值，然后找到所有符合条件的重串．

#### 左偏重串的判定

即使固定 $\textit{cntr}$ 后，仍然可能会有多个符合条件的重串，我们怎么找到所有符合条件的重串呢？

我们再来举一个例子，对于字符串 $\tt abcabcac$ 中的重串 $\overbrace{\tt a}^{l_1} \overbrace{\underset{\textit{cntr}}{\tt b} \tt c}^{l_2} \overbrace{\tt a}^{l_1}  \; | \; \overbrace{\tt b \; \tt c}^{l_2}$，我们记 $l_1$ 为该重串的首字符到 $s[\textit{cntr} - 1]$ 所组成的子串的长度，记 $l_2$ 为 $s[\textit{cntr}]$ 到该重串左边原串的末字符所组成的子串的长度．

于是，我们可以给出某个长度为 $2l = 2(l_1 + l_2) = 2(|u| - \textit{cntr})$ 的子串是重串的 **充分必要条件**：

记 $k_1$ 为满足 $u[\textit{cntr} - k_1 \dots \textit{cntr} - 1] = u[|u| - k_1 \dots |u| - 1]$ 的最大整数，记 $k_2$ 为满足 $u[\textit{cntr} \dots \textit{cntr} + k_2 - 1] = v[0 \dots k_2 - 1]$ 的最大整数．则对于任意满足 $l_1 \leq k_1$，$l_2 \leq k_2$ 的二元组 $(l_1, l_2)$，我们都能恰好找到一个与之对应的重串．

总结一下，即有：

-   固定一个 $\textit{cntr}$．
-   那么我们此时要找的重串长度均为 $2l = 2(|u| - \textit{cntr})$．此时可能仍有多个符合条件的重串，取决于 $l_1$ 与 $l_2$ 的取值．
-   计算上文提到的 $k_1$，$k_2$．
-   则所有符合条件的重串符合条件：

$$
\begin{align} l_1 + l_2 &= l = |u| - \textit{cntr} \\ l_1 &\le k_1, \\ l_2 &\le k_2. \\ \end{align}
$$

接下来，只需要考虑如何快速算出 $k_1$ 与 $k_2$ 了．借助 [Z 函数](./z-func.md)，我们可以 $O(1)$ 计算它们：

-   计算 $k_1$：只需计算 $\overline{u}$ 的 Z 函数即可．
-   计算 $k_2$：只需计算 $v + \# + u$ 的 Z 函数即可，其中 $\#$ 是一个 $u$，$v$ 中均没有的字符．

#### 右偏重串

计算右偏重串的方法与计算左偏重串的方法几乎一致．考虑该重串第一个落入 $u$ 的字符（即 $s[|u| - 1]$），则其一定与 $v$ 中的某个字符一致，记这个字符在 $v$ 中的位置为 $\textit{cntr}$．

令 $k_1$ 为满足 $v[\textit{cntr} - k_1 + 1 \dots \textit{cntr}] = u[|u| - k_1 \dots |u| - 1]$ 的最大整数，$k_2$ 为满足 $v[\textit{cntr} + 1 \dots \textit{cntr} + k_2] = v[0 \dots k_2 - 1]$ 的最大整数．则我们可以分别通过计算 $\overline{u} + \# + \overline{v}$ 和 $v$ 的 Z 函数来得出 $k_1$ 与 $k_2$．

枚举 $\textit{cntr}$，用相仿的方法寻找右偏重串即可．

### 实现

Main–Lorentz 算法以四元组 $(\textit{cntr}, l, k_1, k_2)$ 的形式给出所有重串．如果你只需要计算重串的数量，或者只需要找到最长的一个重串，这个四元组给的信息是足够的．由 [主定理](../basic/complexity.md#主定理-master-theorem) 可得，Main–Lorentz 算法的时间复杂度为 $O(n \log n)$．

请注意，如果你想通过这些四元组来找到所有重串的起始位置与终止位置，则最坏时间复杂度会达到 $O(n^2)$．我们在下面的程序中实现了这一点，将所有重串的起始位置与终止位置存于 `repetitions` 中．

```cpp
vector<int> z_function(string const& s) {
  int n = s.size();
  vector<int> z(n);
  for (int i = 1, l = 0, r = 0; i < n; i++) {
    if (i <= r) z[i] = min(r - i + 1, z[i - l]);
    while (i + z[i] < n && s[z[i]] == s[i + z[i]]) z[i]++;
    if (i + z[i] - 1 > r) {
      l = i;
      r = i + z[i] - 1;
    }
  }
  return z;
}

int get_z(vector<int> const& z, int i) {
  if (0 <= i && i < (int)z.size())
    return z[i];
  else
    return 0;
}

vector<pair<int, int>> repetitions;

void convert_to_repetitions(int shift, bool left, int cntr, int l, int k1,
                            int k2) {
  for (int l1 = max(1, l - k2); l1 <= min(l, k1); l1++) {
    if (left && l1 == l) break;
    int l2 = l - l1;
    int pos = shift + (left ? cntr - l1 : cntr - l - l1 + 1);
    repetitions.emplace_back(pos, pos + 2 * l - 1);
  }
}

void find_repetitions(string s, int shift = 0) {
  int n = s.size();
  if (n == 1) return;

  int nu = n / 2;
  int nv = n - nu;
  string u = s.substr(0, nu);
  string v = s.substr(nu);
  string ru(u.rbegin(), u.rend());
  string rv(v.rbegin(), v.rend());

  find_repetitions(u, shift);
  find_repetitions(v, shift + nu);

  vector<int> z1 = z_function(ru);
  vector<int> z2 = z_function(v + '#' + u);
  vector<int> z3 = z_function(ru + '#' + rv);
  vector<int> z4 = z_function(v);

  for (int cntr = 0; cntr < n; cntr++) {
    int l, k1, k2;
    if (cntr < nu) {
      l = nu - cntr;
      k1 = get_z(z1, nu - cntr);
      k2 = get_z(z2, nv + 1 + cntr);
    } else {
      l = cntr - nu + 1;
      k1 = get_z(z3, nu + 1 + nv - 1 - (cntr - nu));
      k2 = get_z(z4, (cntr - nu) + 1);
    }
    if (k1 + k2 >= l) convert_to_repetitions(shift, cntr < nu, cntr, l, k1, k2);
  }
}
```

**本页面主要译自博文 [Поиск всех тандемных повторов в строке. Алгоритм Мейна-Лоренца](http://e-maxx.ru/algo/string_tandems) 与其英文翻译版 [Finding repetitions](https://cp-algorithms.com/string/main_lorentz.html)．其中俄文版版权协议为 Public Domain + Leave a Link；英文版版权协议为 CC-BY-SA 4.0．**


## string/manacher.md

## 描述

给定一个长度为 $n$ 的字符串 $s$，请找到所有对 $(i, j)$ 使得子串 $s[i \dots j]$ 为一个回文串．当 $t = t_{\text{rev}}$ 时，字符串 $t$ 是一个回文串（$t_{\text{rev}}$ 是 $t$ 的反转字符串）．

## 解释

显然在最坏情况下可能有 $O(n^2)$ 个回文串，因此似乎一眼看过去该问题并没有线性算法．

但是关于回文串的信息可用 **一种更紧凑的方式** 表达：对于每个位置 $i = 0 \dots n - 1$，我们找出值 $d_1[i]$ 和 $d_2[i]$．二者分别表示以位置 $i$ 为中心的长度为奇数和长度为偶数的回文串个数．换个角度，二者也表示了以位置 $i$ 为中心的最长回文串的半径长度（半径长度 $d_1[i]$，$d_2[i]$ 均为从位置 $i$ 到回文串最右端位置包含的字符个数）．

举例来说，字符串 $s = \mathtt{abababc}$ 以 $s[3] = b$ 为中心有三个奇数长度的回文串，最长回文串半径为 $3$，也即 $d_1[3] = 3$：

$$
a\ \overbrace{b\ a\ \underset{s_3}{b}\ a\ b}^{d_1[3]=3}\ c
$$

字符串 $s = \mathtt{cbaabd}$ 以 $s[3] = a$ 为中心有两个偶数长度的回文串，最长回文串半径为 $2$，也即 $d_2[3] = 2$：

$$
c\ \overbrace{b\ a\ \underset{s_3}{a}\ b}^{d_2[3]=2}\ d
$$

因此关键思路是，如果以某个位置 $i$ 为中心，我们有一个长度为 $l$ 的回文串，那么我们有以 $i$ 为中心的长度为 $l - 2$，$l - 4$，等等的回文串．所以 $d_1[i]$ 和 $d_2[i]$ 两个数组已经足够表示字符串中所有子回文串的信息．

一个令人惊讶的事实是，存在一个复杂度为线性并且足够简单的算法计算上述两个「回文性质数组」$d_1[]$ 和 $d_2[]$．在这篇文章中我们将详细的描述该算法．

## 解法

总的来说，该问题具有多种解法：应用字符串哈希，该问题可在 $O(n \log n)$ 时间内解决，而使用后缀数组和快速 LCA 该问题可在 $O(n)$ 时间内解决．

但是这里描述的算法 **压倒性** 的简单，并且在时间和空间复杂度上具有更小的常数．该算法由 **Glenn K. Manacher** 在 1975 年提出．

## 朴素算法

为了避免在之后的叙述中出现歧义，这里我们指出什么是「朴素算法」．

该算法通过下述方式工作：对每个中心位置 $i$，在比较一对对应字符后，只要可能，该算法便尝试将答案加 $1$．

该算法是比较慢的：它只能在 $O(n^2)$ 的时间内计算答案．

该朴素算法的实现如下：

???+ note "实现"
    === "C++"
        ```cpp
        vector<int> d1(n), d2(n);
        for (int i = 0; i < n; i++) {
          d1[i] = 1;
          while (0 <= i - d1[i] && i + d1[i] < n && s[i - d1[i]] == s[i + d1[i]]) {
            d1[i]++;
          }
        
          d2[i] = 0;
          while (0 <= i - d2[i] - 1 && i + d2[i] < n &&
                 s[i - d2[i] - 1] == s[i + d2[i]]) {
            d2[i]++;
          }
        }
        ```
    
    === "Python"
        ```python
        d1 = [0] * n
        d2 = [0] * n
        for i in range(0, n):
            d1[i] = 1
            while 0 <= i - d1[i] and i + d1[i] < n and s[i - d1[i]] == s[i + d1[i]]:
                d1[i] += 1
        
            d2[i] = 0
            while 0 <= i - d2[i] - 1 and i + d2[i] < n and s[i - d2[i] - 1] == s[i + d2[i]]:
                d2[i] += 1
        ```

## Manacher 算法

这里我们将只描述算法中寻找所有奇数长度子回文串的情况，即只计算 $d_1[]$；寻找所有偶数长度子回文串的算法（即计算数组 $d_2[]$）将只需对奇数情况下的算法进行一些小修改．

为了快速计算，我们维护已找到的最靠右的子回文串的 **边界 $[l, r]$**（即具有最大 $r$ 值的回文串，其中 $l$ 和 $r$ 分别为该回文串左右边界的位置）．初始时，我们置 $l = 0$ 和 $r = -1$（*-1*需区别于倒序索引位置，这里可为任意负数，仅为了循环初始时方便）．

### 过程

现在假设我们要对下一个 $i$ 计算 $d_1[i]$，而之前所有 $d_1[]$ 中的值已计算完毕．我们将通过下列方式计算：

-   如果 $i$ 位于当前子回文串之外，即 $i > r$，那么我们调用朴素算法．

    因此我们将连续地增加 $d_1[i]$，同时在每一步中检查当前的子串 $[i - d_1[i] \dots i + d_1[i]]$（$d_1[i]$ 表示半径长度，下同）是否为一个回文串．如果我们找到了第一处对应字符不同，又或者碰到了 $s$ 的边界，则算法停止．在两种情况下我们均已计算完 $d_1[i]$．此后，仍需记得更新 $(l, r)$．

-   现在考虑 $i \le r$ 的情况．我们将尝试从已计算过的 $d_1[]$ 的值中获取一些信息．首先在子回文串 $(l, r)$ 中反转位置 $i$，即我们得到 $j = l + (r - i)$．现在来考察值 $d_1[j]$．因为位置 $j$ 同位置 $i$ 对称，我们 **几乎总是** 可以置 $d_1[i] = d_1[j]$．该想法的图示如下（可认为以 $j$ 为中心的回文串被「拷贝」至以 $i$ 为中心的位置上）：

    $$
    \ldots\
    \overbrace{
        s_l\ \ldots\
        \underbrace{
            s_{j-d_1[j]+1}\ \ldots\ s_j\ \ldots\ s_{j+d_1[j]-1}
        }_\text{palindrome}\
        \ldots\
        \underbrace{
            s_{i-d_1[j]+1}\ \ldots\ s_i\ \ldots\ s_{i+d_1[j]-1}
        }_\text{palindrome}\
        \ldots\ s_r
    }^\text{palindrome}\
    \ldots
    $$

    然而有一个 **棘手的情况** 需要被正确处理：当「内部」的回文串到达「外部」回文串的边界时，即 $j - d_1[j] + 1 \le l$（或者等价的说，$i + d_1[j] - 1 \ge r$）．因为在「外部」回文串范围以外的对称性没有保证，因此直接置 $d_1[i] = d_1[j]$ 将是不正确的：我们没有足够的信息来断言在位置 $i$ 的回文串具有同样的长度．

    实际上，为了正确处理这种情况，我们应该「截断」回文串的长度，即置 $d_1[i] = r - i + 1$．之后我们将运行朴素算法以尝试尽可能增加 $d_1[i]$ 的值．

    该种情况的图示如下（以 $j$ 为中心的回文串已经被截断以落在「外部」回文串内）：

    $$
    \ldots\
    \overbrace{
        \underbrace{
            s_l\ \ldots\ s_j\ \ldots\ s_{j+(j-l)}
        }_\text{palindrome}\
        \ldots\
        \underbrace{
            s_{i-(r-i)}\ \ldots\ s_i\ \ldots\ s_r
        }_\text{palindrome}
    }^\text{palindrome}\
    \underbrace{
        \ldots \ldots \ldots \ldots \ldots
    }_\text{try moving here}
    $$

    该图示显示出，尽管以 $j$ 为中心的回文串可能更长，以致于超出「外部」回文串，但在位置 $i$，我们只能利用其完全落在「外部」回文串内的部分．然而位置 $i$ 的答案可能比这个值更大，因此接下来我们将运行朴素算法来尝试将其扩展至「外部」回文串之外，也即标识为 "try moving here" 的区域．

最后，仍有必要提醒的是，我们应当记得在计算完每个 $d_1[i]$ 后更新值 $(l, r)$．

同时，再让我们重复一遍：计算偶数长度回文串数组 $d_2[]$ 的算法同上述计算奇数长度回文串数组 $d_1[]$ 的算法十分类似．

## Manacher 算法的复杂度

因为在计算一个特定位置的答案时我们总会运行朴素算法，所以一眼看去该算法的时间复杂度为线性的事实并不显然．

然而更仔细的分析显示出该算法具有线性复杂度．此处我们需要指出，[计算 Z 函数的算法](./z-func.md) 和该算法较为类似，并同样具有线性时间复杂度．

实际上，注意到朴素算法的每次迭代均会使 $r$ 增加 $1$，以及 $r$ 在算法运行过程中从不减小．这两个观察告诉我们朴素算法总共会进行 $O(n)$ 次迭代．

Manacher 算法的另一部分显然也是线性的，因此总复杂度为 $O(n)$．

## Manacher 算法的实现

### 分类讨论

为了计算 $d_1[]$，我们有以下代码：

=== "C++"
    ```cpp
    vector<int> d1(n);
    for (int i = 0, l = 0, r = -1; i < n; i++) {
      int k = (i > r) ? 1 : min(d1[l + r - i], r - i + 1);
      while (0 <= i - k && i + k < n && s[i - k] == s[i + k]) {
        k++;
      }
      d1[i] = k--;
      if (i + k > r) {
        l = i - k;
        r = i + k;
      }
    }
    ```

=== "Python"
    ```python
    d1 = [0] * n
    l, r = 0, -1
    for i in range(0, n):
        k = 1 if i > r else min(d1[l + r - i], r - i + 1)
        while 0 <= i - k and i + k < n and s[i - k] == s[i + k]:
            k += 1
        d1[i] = k
        k -= 1
        if i + k > r:
            l = i - k
            r = i + k
    ```

计算 $d_2[]$ 的代码十分类似，但是在算术表达式上有些许不同：

=== "C++"
    ```cpp
    vector<int> d2(n);
    for (int i = 0, l = 0, r = -1; i < n; i++) {
      int k = (i > r) ? 0 : min(d2[l + r - i + 1], r - i + 1);
      while (0 <= i - k - 1 && i + k < n && s[i - k - 1] == s[i + k]) {
        k++;
      }
      d2[i] = k--;
      if (i + k > r) {
        l = i - k - 1;
        r = i + k;
      }
    }
    ```

=== "Python"
    ```python
    d2 = [0] * n
    l, r = 0, -1
    for i in range(0, n):
        k = 0 if i > r else min(d2[l + r - i + 1], r - i + 1)
        while 0 <= i - k - 1 and i + k < n and s[i - k - 1] == s[i + k]:
            k += 1
        d2[i] = k
        k -= 1
        if i + k > r:
            l = i - k - 1
            r = i + k
    ```

### 统一处理

虽然在讲解过程及上述实现中我们将 $d_1[]$ 和 $d_2[]$ 的计算分开考虑，但实际上可以通过一个技巧将二者的计算统一为 $d_1[]$ 的计算．

给定一个长度为 $n$ 的字符串 $s$，我们在其 $n + 1$ 个空中插入分隔符 $\#$，从而构造一个长度为 $2n + 1$ 的字符串 $s'$．举例来说，对于字符串 $s = \mathtt{abababc}$，其对应的 $s' = \mathtt{\#a\#b\#a\#b\#a\#b\#c\#}$．

对于字母间的 $\#$，其实际意义为 $s$ 中对应的「空」．而两端的 $\#$ 则是为了实现的方便．

注意到，在对 $s'$ 计算 $d_1[]$ 后，对于一个位置 $i$，$d_1[i]$ 所描述的最长的子回文串必定以 $\#$ 结尾（若以字母结尾，由于字母两侧必定各有一个 $\#$，因此可向外扩展一个得到一个更长的）．因此，对于 $s$ 中一个以字母为中心的极大子回文串，设其长度为 $m + 1$，则其在 $s'$ 中对应一个以相应字母为中心，长度为 $2m + 3$ 的极大子回文串；而对于 $s$ 中一个以空为中心的极大子回文串，设其长度为 $m$，则其在 $s'$ 中对应一个以相应表示空的 $\#$ 为中心，长度为 $2m + 1$ 的极大子回文串（上述两种情况下的 $m$ 均为偶数，但该性质成立与否并不影响结论）．综合以上观察及少许计算后易得，在 $s'$ 中，$d_1[i]$ 表示在 $s$ 中以对应位置为中心的极大子回文串的 **总长度加一**．

上述结论建立了 $s'$ 的 $d_1[]$ 同 $s$ 的 $d_1[]$ 和 $d_2[]$ 间的关系．

由于该统一处理本质上即求 $s'$ 的 $d_1[]$，因此在得到 $s'$ 后，代码同上节计算 $d_1[]$ 的一样．

## 练习题目

-   [UVa #11475 "Extend to Palindrome"](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=2470)
-   [「国家集训队」最长双回文串](https://www.luogu.com.cn/problem/P4555)
-   [CF1326D2. Labyrinth](https://codeforces.com/contest/1326/problem/D2)

**本页面主要译自博文 [Нахождение всех подпалиндромов](http://e-maxx.ru/algo/palindromes_count) 与其英文翻译版 [Finding all sub-palindromes in $O(N)$](https://cp-algorithms.com/string/manacher.html)．其中俄文版版权协议为 Public Domain + Leave a Link；英文版版权协议为 CC-BY-SA 4.0．**


## string/match.md

本页面将简述字符串匹配问题以及它的解法．

## 字符串匹配问题

### 定义

又称模式匹配（pattern matching）．该问题可以概括为「给定字符串 $S$ 和 $T$，在主串 $S$ 中寻找子串 $T$」．字符 $T$ 称为模式串 (pattern)．

### 类型

-   单串匹配：给定一个模式串和一个待匹配串，找出前者在后者中的所有位置．
-   多串匹配：给定多个模式串和一个待匹配串，找出这些模式串在后者中的所有位置．
    -   出现多个待匹配串时，将它们直接连起来便可作为一个待匹配串处理．
    -   可以直接当做单串匹配，但是效率不够高．
-   其他类型：例如匹配一个串的任意后缀，匹配多个串的任意后缀……

## 暴力做法

简称 BF (Brute Force) 算法．该算法的基本思想是从主串 $S$ 的第一个字符开始和模式串 $T$ 的第一个字符进行比较，若相等，则继续比较二者的后续字符；否则，模式串 $T$ 回退到第一个字符，重新和主串 $S$ 的第二个字符进行比较．如此往复，直到 $S$ 或 $T$ 中所有字符比较完毕．

### 实现

=== "C++"
    ```cpp
    /*
     * s：待匹配的主串
     * t：模式串
     * n：主串的长度
     * m：模式串的长度
     */
    std::vector<int> match(char *s, char *t, int n, int m) {
      std::vector<int> ans;
      int i, j;
      for (i = 0; i < n - m + 1; i++) {
        for (j = 0; j < m; j++) {
          if (s[i + j] != t[j]) break;
        }
        if (j == m) ans.push_back(i);
      }
      return ans;
    }
    ```

=== "Python"
    ```python
    def match(s, t, n, m):
        if m < 1:
            return []
    
        ans = []
        for i in range(0, n - m + 1):
            for j in range(0, m):
                if s[i + j] != t[j]:
                    break
            else:
                ans.append(i)
        return ans
    ```

### 时间复杂度

设 $n$ 为主串的长度，$m$ 为模式串的长度．默认 $m\ll n$．

BF 算法匹配成功时，在最好情况下，只有一趟匹配成功，此趟比较次数为 $m$，而其余每趟不成功的匹配都发生在模式串的第一个字符，还需要 $n-m$ 次比较，总比较次数为 $n$，故时间复杂度为 $O(n)$；在最坏情况下，匹配成功的趟数为 $n-m+1$，每趟比较次数为 $m$，总比较次数为 $m(n-m+1)$，故时间复杂度为 $O(mn)$．

BF 算法匹配失败时，在最好情况下，每趟不成功的匹配都发生在模式串的第一个字符，BF 算法要执行 $n-m+1$ 次比较，时间复杂度为 $O(n)$；在最坏情况下，每趟不成功的匹配都发生在模式串的最后一个字符，BF 算法要执行 $m(n-m+1)$ 次比较，时间复杂度为 $O(mn)$．

如果模式串有至少两个不同的字符，则 BF 算法的平均时间复杂度为 $O(n)$．但是在 OI 题目中，给出的字符串一般都不是纯随机的．

## Hash 的方法

参见：[字符串哈希](./hash.md)

## KMP 算法

参见：[前缀函数与 KMP 算法](./kmp.md)


## string/minimal-string.md

## 定义

最小表示法是用于解决字符串最小表示问题的方法．

## 字符串的最小表示

### 循环同构

当字符串 $S$ 中可以选定一个位置 $i$ 满足

$$
S[i\cdots n]+S[1\cdots i-1]=T
$$

则称 $S$ 与 $T$ 循环同构

### 最小表示

字符串 $S$ 的最小表示为与 $S$ 循环同构的所有字符串中字典序最小的字符串

## simple 的暴力

我们每次比较 $i$ 和 $j$ 开始的循环同构，把当前比较到的位置记作 $k$，每次遇到不一样的字符时便把大的跳过，最后剩下的就是最优解．

### 实现

=== "C++"
    ```cpp
    int k = 0, i = 0, j = 1;
    while (k < n && i < n && j < n) {
      if (sec[(i + k) % n] == sec[(j + k) % n]) {
        ++k;
      } else {
        if (sec[(i + k) % n] > sec[(j + k) % n])
          ++i;
        else
          ++j;
        k = 0;
        if (i == j) i++;
      }
    }
    i = min(i, j);
    ```

=== "Python"
    ```python
    k, i, j = 0, 0, 1
    while k < n and i < n and j < n:
        if sec[(i + k) % n] == sec[(j + k) % n]:
            k += 1
        else:
            if sec[(i + k) % n] > sec[(j + k) % n]:
                i += 1
            else:
                j += 1
            k = 0
            if i == j:
                i += 1
    i = min(i, j)
    ```

### 解释

该实现方法随机数据下表现良好，但是可以构造特殊数据卡掉．

例如：对于 $\texttt{aaa}\cdots\texttt{aab}$, 不难发现这个算法的复杂度退化为 $O(n^2)$．

我们发现，当字符串中出现多个连续重复子串时，此算法效率降低，我们考虑优化这个过程．

## 最小表示法

### 算法核心

考虑对于一对字符串 $A,B$, 它们在原字符串 $S$ 中的起始位置分别为 $i,j$, 且它们的前 $k$ 个字符均相同，即

$$
S[i \cdots i+k-1]=S[j \cdots j+k-1]
$$

不妨先考虑 $S[i+k]>S[j+k]$ 的情况，我们发现起始位置下标 $l$ 满足 $i\le l\le i+k$ 的字符串均不能成为答案．因为对于任意一个字符串 $S_{i+p}$（表示以 $i+p$ 为起始位置的字符串，$p \in [0, k]$）一定存在字符串 $S_{j+p}$ 比它更优．

所以我们比较时可以跳过下标 $l\in [i,i+k]$, 直接比较 $S_{i+k+1}$

这样，我们就完成了对于上文暴力的优化．

### 时间复杂度

$O(n)$

### 过程

1.  初始化指针 $i$ 为 $0$，$j$ 为 $1$；初始化匹配长度 $k$ 为 $0$
2.  比较第 $k$ 位的大小，根据比较结果跳转相应指针．若跳转后两个指针相同，则随意选一个加一以保证比较的两个字符串不同
3.  重复上述过程，直到比较结束
4.  答案为 $i,j$ 中较小的一个

### 实现

=== "C++"
    ```cpp
    int k = 0, i = 0, j = 1;
    while (k < n && i < n && j < n) {
      if (sec[(i + k) % n] == sec[(j + k) % n]) {
        k++;
      } else {
        sec[(i + k) % n] > sec[(j + k) % n] ? i = i + k + 1 : j = j + k + 1;
        if (i == j) i++;
        k = 0;
      }
    }
    i = min(i, j);
    ```

=== "Python"
    ```python
    k, i, j = 0, 0, 1
    while k < n and i < n and j < n:
        if sec[(i + k) % n] == sec[(j + k) % n]:
            k += 1
        else:
            if sec[(i + k) % n] > sec[(j + k) % n]:
                i = i + k + 1
            else:
                j = j + k + 1
            if i == j:
                i += 1
            k = 0
    i = min(i, j)
    ```


## string/pam.md

## 定义

回文树（EER Tree，Palindromic Tree，也被称为回文自动机）是一种可以存储一个串中所有回文子串的高效数据结构．最初由 Mikhail Rubinchik 和 Arseny M. Shur 在 2015 年发表．它的灵感来源于后缀树等字符串后缀数据结构，使用回文树可以简单高效地解决一系列涉及回文串的问题．

## 结构

回文树大概长这样

![](./images/pam1.png)

和其它自动机类似的，回文树也是由转移边和后缀链接（fail 指针）组成，每个节点都可以代表一个回文子串．

因为回文串长度分为奇数和偶数，我们可以像 manacher 那样加入一个不在字符集中的字符（如 '#'）作为分隔符来将所有回文串的长度都变为奇数，但是这样过于麻烦了．有没有更好的办法呢？

答案自然是有．更好的办法就是建两棵树，一棵树中的节点对应的回文子串长度均为奇数，另一棵树中的节点对应的回文子串长度均为偶数．

和其它的自动机一样，一个节点的 fail 指针指向的是这个节点所代表的回文串的最长回文后缀所对应的节点，但是转移边并非代表在原节点代表的回文串后加一个字符，而是表示在原节点代表的回文串前后各加一个相同的字符（不难理解，因为要保证存的是回文串）．

我们还需要在每个节点上维护此节点对应回文子串的长度 len，这个信息保证了我们可以轻松地构造出回文树．

## 建造

回文树有两个初始状态，分别代表长度为 $-1,0$ 的回文串．我们可以称它们为奇根，偶根．它们不表示任何实际的字符串，仅作为初始状态存在，这与其他自动机的根节点是异曲同工的．

偶根的 fail 指针指向奇根，而我们并不关心奇根的 fail 指针，因为奇根不可能失配（奇根转移出的下一个状态长度为 $1$，即单个字符．一定是回文子串）

类似后缀自动机，我们增量构造回文树．

考虑构造完前 $p-1$ 个字符的回文树后，向自动机中添加在原串里位置为 $p$ 的字符．

我们从以上一个字符结尾的最长回文子串对应的节点开始，不断沿着 fail 指针走，直到找到一个节点满足 $s_{p}=s_{p-len-1}$，即满足此节点所对应回文子串的上一个字符与待添加字符相同．

这里贴出论文中的那张图

![](./images/pam2.png)

我们通过跳 fail 指针找到 A 所对应的节点，然后两边添加 `X` 就到了现在的回文串了（即 `XAX`），很显然，这个节点就是以 $p$ 结尾的最长回文子串对应的树上节点．（同时，这个时候长度 $-1$ 节点优势出来了，如果没有 `X` 能匹配条件就是同一个位置的 $s_p=s_p$，就自然得到了代表字符 `X` 的节点．）此时要判断一下：没有这个节点，就需要新建．

然后我们还需要求出新建的节点的 fail 指针．具体方法与上面的过程类似，不断跳转 fail 指针，从 `A` 出发，即可找到 `XAX` 的最长回文后缀 `XBX`，将对应节点设为 fail 指针所指的对象即可．

显然，这个节点是不需新建的，`A` 的前 $len_B$ 位和后 $len_B$ 位相同，都是 `B`，前 $len_B$ 位的两端根据回文串对应关系，都是 `X`，后面被钦定了是 `X`，于是这个节点 `XBX` 肯定已经被包含了．

如果 fail 没匹配到，那么将它连向长度为 $0$ 的那个节点，显然这是可行的（因为这是所有节点的后缀）．

## 线性状态数证明

### 定理

对于一个字符串 $s$，它的本质不同回文子串个数最多只有 $|s|$ 个．

### 证明

考虑使用数学归纳法．

-   当 $|s| =1$ 时，$s$ 只有一个字符，同时也只有一个子串，并且这个子串是回文的，因此结论成立．

-   当 $|s| >1$ 时，设 $t=sc$，其中 $t$ 表示 $s$ 最后增加一个字符 $c$ 后形成的字符串，假设结论对 $s$ 串成立．考虑以最后一个字符 $c$ 结尾的回文子串，假设它们的左端点由小到大排序为 $l_1,l_2,\dots,l_k$．由于 $t[l_1..|t|]$ 是回文串，因此对于所有位置 $l_1 \le p \le |t|$，有 $t[p..|t|]=t[l_1..l_1+|t|-p]$．所以，对于 $1 < i \le k$，$t[l_i..|t|]$ 已经在 $t[1..|t|-1]$ 中出现过．因此，每次增加一个字符，本质不同的回文子串个数最多增加 $1$ 个．

由数学归纳法，可知该定理成立．

因此回文树状态数是 $O(|s|)$ 的．对于每一个状态，它实际只代表一个本质不同的回文子串，即转移到该节点的状态唯一，因此总转移数也是 $O(|s|)$ 的．

## 正确性证明

以上图为例，增加当前字符 `X`，由线性状态数的证明，我们只需要找到包含最后一个字符 `X` 的最长回文后缀，也就是 `XAX`．继续寻找 `XAX` 的最长回文后缀 `XBX`，建立后缀链接．`XBX` 对应状态已经在回文树中出现，包含最后一个字符的回文后缀就是 `XAX`，`XBX` 本身及其对应状态在 fail 树上的所有祖先．

对于 $s$ 回文树的构造，令 $n=|s|$，显然除了跳 fail 指针的其他操作都是 $O(n)$ 的．

加入字符时，在上一次的基础上，每次跳 fail 后对应节点在 fail 树的深度 $-1$，而连接 fail 后，仅为深度 + 1（但 fail 为 $0$ 时（即到 $-1$ 才符合），深度相当于在 $-1$ 的基础上 $+2$）．

因为只加入 $n$ 个字符，所以只会加 $n$ 次深度，最多也只会跳 $2n$ 次 fail．

因此，构造 $s$ 的回文树的时间复杂度是 $O(|s|)$．

## 应用

### 本质不同回文子串个数

由线性状态数的证明，容易知道一个串的本质不同回文子串个数等于回文树的状态数（排除奇根和偶根两个状态）．

### 回文子串出现次数

建出回文树，使用类似后缀自动机统计出现次数的方法．

由于回文树的构造过程中，节点本身就是按照拓扑序插入，因此只需要逆序枚举所有状态，将当前状态的出现次数加到其 fail 指针对应状态的出现次数上即可．

例题：[「APIO2014」回文串](https://www.luogu.com.cn/problem/P3649)

定义 $s$ 的一个子串的存在值为这个子串在 $s$ 中出现的次数乘以这个子串的长度．对于给定的字符串 $s$，求所有回文子串中的最大存在值．

??? note "参考代码"
    ```cpp
    --8<-- "docs/string/code/pam/pam_1.cpp"
    ```

### 最小回文划分

> 给定一个字符串 $s(1\le |s| \le 10^5)$，求最小的 $k$，使得存在 $s_1,s_2,\dots,s_k$，满足 $s_i(1\le i \le k)$ 均为回文串，且 $s_1,s_2, \dots ,s_k$ 依次连接后得到的字符串等于 $s$．

考虑动态规划，记 $dp[i]$ 表示 $s$ 长度为 $i$ 的前缀的最小划分数，转移只需要枚举以第 $i$ 个字符结尾的所有回文串

$$
dp[i]=1+\min_{ s[j+1..i] \text{ 为回文串} } dp[j]
$$

由于一个字符串最多会有 $O(n^2)$ 个回文子串，因此上述算法的时间复杂度为 $O(n^2)$，无法接受，为了优化转移过程，下面给出一些引理．

记字符串 $s$ 长度为 $i$ 的前缀为 $pre(s,i)$，长度为 $i$ 的后缀为 $suf(s,i)$．

周期：若 $0< p \le |s|$，$\forall 1 \le i \le |s|-p,s[i]=s[i+p]$，就称 $p$ 是 $s$ 的周期．

border：若 $0 \le r < |s|$，$pre(s,r)=suf(s,r)$，就称 $pre(s,r)$ 是 $s$ 的 border．

周期和 border 的关系：$t$ 是 $s$ 的 border，当且仅当 $|s|-|t|$ 是 $s$ 的周期．

???+ note "证明"
    若 $t$ 是 $s$ 的 border，那么 $pre(s,|t|)=suf(s,|t|)$，因此 $\forall 1\le i \le |t|, s[i]=s[|s|-|t|+i]$，所以 $|s|-|t|$ 就是 $s$ 的周期．
    
    若 $|s|-|t|$ 为 $s$ 周期，则 $\forall 1 \le i \le |s|-(|s|-|t|)=|t|,s[i]=s[|s|-|t|+i]$，因此 $pre(s,|t|)=suf(s,|t|)$，所以 $t$ 是 $s$ 的 border．

#### 引理一

$t$ 是回文串 $s$ 的后缀，$t$ 是 $s$ 的 border 当且仅当 $t$ 是回文串．

???+ note "证明"
    对于 $1 \le i \le |t|$，由 $s$ 和 $t$ 为回文串，因此有 $s[i]=s[|s|-i+1]=s[|s|-|t|+i]$，所以 $t$ 是 $s$ 的 border．
    
    对于 $1 \le i \le |t|$，由 $t$ 是 $s$ 的 border，有 $s[i]=s[|s|-|t|+i]$，由 $s$ 是回文串，有 $s[i]=s[|s|-i+1]$，因此 $s[|s|-i+1]=s[|s|-|t|+i]$，所以 $t$ 是回文串．

下图中，相同颜色的位置表示字符对应相同．

![](./images/pam3.png)

#### 引理二

$t$ 是串 $s$ 的 border ($|s|\le 2|t|$)，$s$ 是回文串当且仅当 $t$ 是回文串．

???+ note "证明"
    若 $s$ 是回文串，由引理 $1$，$t$ 也是回文串．
    
    若 $t$ 是回文串，由 $t$ 是 $s$ 的 border，因此 $\forall 1 \le i \le |t|, s[i]=s[|s|-|t|+i]=s[|s|-i+1]$，因为 $|s| \le 2|t|$，所以 $s$ 也是回文串．

#### 引理三

$t$ 是回文串 $s$ 的 border，则 $|s|-|t|$ 是 $s$ 的周期，$|s|-|t|$ 为 $s$ 的最小周期，当且仅当 $t$ 是 $s$ 的最长回文真后缀．

#### 引理四

$x$ 是一个回文串，$y$ 是 $x$ 的最长回文真后缀，$z$ 是 $y$ 的最长回文真后缀．令 $u,v$ 分别为满足 $x=uy,y=vz$ 的字符串，则有下面三条性质

1.  $|u| \ge |v|$；

2.  如果 $|u| > |v|$，那么 $|u| > |z|$；

3.  如果 $|u| = |v|$，那么 $u=v$．

![](./images/pam4.png)

???+ note "证明"
    1.  由引理 $3$ 的推论，$|u|=|x|-|y|$ 是 $x$ 的最小周期，$|v|=|y|-|z|$ 是 $y$ 的最小周期．考虑反证法，假设 $|u| < |v|$，因为 $y$ 是 $x$ 的后缀，所以 $u$ 既是 $x$ 的周期，也是 $y$ 的周期，而 $|v|$ 是 $y$ 的最小周期，矛盾．所以 $|u| \ge |v|$．
    2.  因为 $y$ 是 $x$ 的 border，所以 $v$ 是 $x$ 的前缀，设字符串 $w$，满足 $x=vw$（如下图所示），其中 $z$ 是 $w$ 的 border．考虑反证法，假设 $|u| \le |z|$，那么 $|zu| \le 2|z|$，所以由引理 $2$，$w$ 是回文串，由引理 $1$，$w$ 是 $x$ 的 border，又因为 $|u| > |v|$，所以 $|w| > |y|$，矛盾．所以 $|u| > |z|$．
    3.  $u,v$ 都是 $x$ 的前缀，$|u|=|v|$，所以 $u=v$．
    
    ![](./images/pam5.png)

#### 推论

$s$ 的所有回文后缀按照长度排序后，可以划分成 $\log |s|$ 段等差数列．

???+ note "证明"
    设 $s$ 的所有回文后缀长度从小到大排序为 $l_1,l_2,\dots,l_k$．对于任意 $2 \le i \le k-1$，若 $l_{i}-l_{i-1}=l_{i+1}-l_{i}$，则 $l_{i-1},l_{i},l_{i+1}$ 构成一个等差数列．否则 $l_{i}-l_{i-1}\neq l_{i+1}-l_{i}$，由引理 $4$，有 $l_{i+1}-l_{i}>l_{i}-l_{i-1}$，且 $l_{i+1}-l_{i}>l_{i-1}$，$l_{i+1}>2l_{i-1}$．因此，若相邻两对回文后缀的长度之差发生变化，那么这个最大长度一定会相对于最小长度翻一倍．显然，长度翻倍最多只会发生 $O(\log |s|)$ 次，也就是 $s$ 的回文后缀长度可以划分成 $\log |s|$ 段等差数列．

该推论也可以通过使用弱周期引理，对 $s$ 的最长回文后缀的所有 border 按照长度 $x$ 分类，$x \in [2^0,2^1),[2^1,2^2),\dots,[2^k,n)$，考虑这 $\log |s|$ 组内每组的最长 border 进行证明．详细证明可以参考金策的《字符串算法选讲》和陈孙立的 2019 年 IOI 国家候选队论文《子串周期查询问题的相关算法及其应用》．

有了这个结论后，我们现在可以考虑如何优化 $dp$ 的转移．

#### 优化

回文树上的每个节点 $u$ 需要多维护两个信息，$diff[u]$ 和 $slink[u]$．$diff[u]$ 表示节点 $u$ 和 $fail[u]$ 所代表的回文串的长度差，即 $len[u]-len[fail[u]]$．$slink[u]$ 表示 $u$ 一直沿着 fail 向上跳到第一个节点 $v$，使得 $diff[v] \neq diff[u]$，也就是 $u$ 所在等差数列中长度最小的那个节点．

根据上面证明的结论，如果使用 $slink$ 指针向上跳的话，每向后填加一个字符，只需要向上跳 $O(\log |s|)$ 次．因此，可以考虑将一个等差数列表示的所有回文串的 $dp$ 值之和（在原问题中指 $\min$），记录到最长的那一个回文串对应节点上．

$g[v]$ 表示 $v$ 所在等差数列的 $dp$ 值之和，且 $v$ 是这个等差数列中长度最长的节点，则 $g[v]=\sum_{slink[x]=slink[v]} dp[i-len[x]]$，这里 $i$ 是当前枚举到的下标．

下面我们考虑如何更新 $g$ 数组和 $dp$ 数组．以下图为例，假设当前枚举到第 $i$ 个字符，回文树上对应节点为 $x$．$g[x]$ 为橙色三个位置的 $dp$ 值之和（最短的回文串 $slink[x]$ 算在下一个等差数列中）．$fail[x]$ 上一次出现位置是 $i-diff[x]$（在 $i-diff[x]$ 处结束），$g[fail[x]]$ 包含的 $dp$ 值是蓝色位置．因此，$g[x]$ 实际上等于 $g[fail[x]]$ 和多出来一个位置的 $dp$ 值之和，多出来的位置是 $i-(len[slink[x]]+diff[x])$．最后再用 $g[x]$ 去更新 $dp[i]$，这部分等差数列的贡献就计算完毕了，不断跳 $slink[x]$，重复这个过程即可．具体实现方式可参考例题代码．

![](./images/pam6.png)

最后，上述做法的正确性依赖于：如果 $x$ 和 $fail[x]$ 属于同一个等差数列，那么 $fail[x]$ 上一次出现位置是 $i-diff[x]$．

???+ note "证明"
    根据引理 $1$，$fail[x]$ 是 $x$ 的 border，因此其在 $i-diff[x]$ 处出现．
    
    假设 $fail[x]$ 在 $(i-diff[x],i)$ 中的 $j$ 位置出现．由于 $x$ 和 $fail[x]$ 属于同一个等差数列，因此 $2|fail[x]| \ge x$．多余的 $fail[x]$ 和 $i-diff[x]$ 处的 $fail[x]$ 有交集，记交集为 $w$，设串 $u$ 满足 $uw=fail[x]$．用类似引理 $1$ 的方式可以证明，$w$ 是回文串，而 $x$ 的前缀 $s[i-len[x]+1..j]=uwu$ 也是回文串，这与 $fail[x]$ 是 $x$ 的最长回文前缀（后缀）矛盾．

例题：[Codeforces 932G Palindrome Partition](https://codeforces.com/problemset/problem/932/G)

给定一个字符串 $s$，要求将 $s$ 划分为 $t_1, t_2, \dots, t_k$，其中 $k$ 是偶数，且 $t_i=t_{k-i+1}$，求这样的划分方案数．

??? note "题解"
    构造字符串 $t= s[0]s[n - 1]s[1]s[n - 2]s[2]s[n - 3] \dots s[n / 2 - 1]s[n / 2]$，问题等价于求 $t$ 的偶回文划分方案数，把上面的转移方程改成求和形式并且只在偶数位置更新 $dp$ 数组即可．时间复杂度 $O(n \log n)$，空间复杂度 $O(n)$．

??? note "参考代码"
    ```cpp
    --8<-- "docs/string/code/pam/pam_2.cpp"
    ```

## 例题

-   [最长双回文串](https://www.luogu.com.cn/problem/P4555)

-   [拉拉队排练](https://www.luogu.com.cn/problem/P1659)

-   [「SHOI2011」双倍回文](https://www.luogu.com.cn/problem/P4287)

-   [HDU 5421 Victor and String](https://acm.hdu.edu.cn/showproblem.php?pid=5421)

-   [CodeChef Palindromeness](https://www.codechef.com/LTIME23/problems/PALPROB)

## 相关资料

-   [EERTREE: An Efficient Data Structure for Processing Palindromes in Strings](https://arxiv.org/pdf/1506.04862)

-   [Palindromic tree](http://adilet.org/blog/palindromic-tree/)

-   2017 年 IOI 国家候选队论文集 回文树及其应用 翁文涛

-   2019 年 IOI 国家候选队论文集 子串周期查询问题的相关算法及其应用 陈孙立

-   字符串算法选讲 金策

-   [A bit more about palindromes](https://codeforces.com/blog/entry/19193)

-   [A Subquadratic Algorithm for Minimum Palindromic Factorization](https://arxiv.org/pdf/1403.2431.pdf)


## string/sa-optimal-inplace.md

本章介绍线性时间复杂度的后缀排序的就地算法[^in-place-sa-sort]（Optimal In-Place Suffix Sorting）．

???+ warning "Warning"
    本章 **只建议** 在 **非常非常熟悉** SA-IS[^nzc09a][^sa-is介绍]的前提下阅读．

## 全局设定

目标字符串 $\texttt{Pat}$，后缀数组 $\texttt{SA}$，串的序号从 0 开始，结尾字符是警戒哨，不妨设为 0．

## 在整形字母表上的后缀排序

事实上这一部分可以看成是原地版本的 SA-IS 算法．

因为是原文中细节相对最清楚，实现也较为简单的算法，也是了解后续算法的基础，是本文介绍的重点．

原地化的原理是用重命名的 $\texttt{Pat}$ 代替 S、L 桶，用额外 $O(n)$ 的操作代替类型桶．

### 重命名目标串 Pat

简单来说，我们会在不改变后缀大小的相对顺序的前提下，重命名 $\texttt{Pat}$，用重命名后的 $\texttt{Pat}$ 来取代原来 S、L 桶，来指明桶头或者桶尾．

重命名的方法是将 $\texttt{Pat}$ 中的 S 型字符替换为所在桶的桶尾索引，L  型字符替换为所在桶的桶头索引．

如下图所示：

$$
\begin{aligned}
\texttt{Index}:\qquad&\texttt{ 0   1   2   3   4   5   6   7   8   9  10  11  12} \\
\texttt{Pat}:\qquad&\texttt{ 2   1   1   3   3   1   1   3   3   1   2   1   0} \\
\texttt{Type}:\qquad&\texttt{ L   S   S   L   L   S   S   L   L   S   L   L   S} \\
\texttt{Bucket}:\qquad&\texttt{(0)}\texttt{ }\texttt{(1}\texttt{ }\texttt{ }\texttt{ 1 }\texttt{ }\texttt{ 1 }\texttt{ }\texttt{ 1 }\texttt{ }\texttt{ 1 }\texttt{ }
\texttt{ 1) }\texttt{(2 }\texttt{ }\texttt{ 2) }\texttt{(3}\texttt{ }\texttt{ }\texttt{ 3 }\texttt{ }\texttt{ 3 }\texttt{ }\texttt{ 3)}
\end{aligned}
$$

重命名后的 $\texttt{Pat'}$（之后直接将重命名后的 $\texttt{Pat'}$ 称做 $\texttt{Pat}$）：

$$
\begin{aligned}
\texttt{Index}:\qquad&\texttt{ 0   1   2   3   4   5   6   7   8   9  10  11  12} \\
\texttt{Pat'}:\qquad&\texttt{ 7   6   6   9   9   6   6   9   9   6   7   1   0}
\end{aligned}
$$

由于桶内的字符，L 型字符后缀小，作为桶头；而 S 型字符后缀大，作为桶尾，因此保持了后缀大小的相对顺序．

描述一下重命名的具体步骤：

1.  和 SA-IS 一样，对 $\texttt{Pat}$ 中每个字符计数，计算其前缀和（计数排序），来构建 S/L 桶，只不过这里用 $\texttt{SA}$ 盛放这个前缀和；
2.  从尾到头，扫描 $\texttt{Pat}$ 的每个字符，这样只需记录上一个字符的类型，就可以动态地判断每个字符的类型，然后依据前缀和将其重命名．

### 对 LMS 字符排序

这里重点是使用了一个内部计数器的技巧．

#### 初始化

初始的时候将 $\texttt{SA}$ 每一项设为 E（EMPTY）．

从尾到头扫描 $\texttt{Pat}$，如果发现是 LMS 字符，$\texttt{Pat[i]}$，那么就设置 $\texttt{SA[Pat[i]]}$ 的标记：

如果 $\texttt{SA[Pat[i]]}$ 是 E，就将其设为 U（UNIQUE）；

如果 $\texttt{SA[Pat[i]]}$ 是 U，就将其设为 M（MULTIPLE）；

其他情况，不做处理．

结果如下图所示：

$$
\begin{aligned}
\texttt{Index}:\qquad&\texttt{ 0   1   2   3   4   5   6   7   8   9  10  11  12} \\
\texttt{Pat}:\qquad&\texttt{ 7   6   6   9   9   6   6   9   9   6   7   1   0} \\
\texttt{LMS}:\qquad&\texttt{ }\texttt{ }\texttt{ }\texttt{ }\texttt{ ∗ }\texttt{ }\texttt{ }\texttt{ }\texttt{ }\texttt{ }\texttt{ }\texttt{ }\texttt{ }\texttt{ }\texttt{ }\texttt{ }\texttt{ }\texttt{ }\texttt{ * }\texttt{ }\texttt{ }\texttt{ }\texttt{ }\texttt{ }\texttt{ }\texttt{ }\texttt{ }\texttt{ }\texttt{ }\texttt{ }\texttt{ }\texttt{ }\texttt{ * }\texttt{ }\texttt{ }\texttt{ }\texttt{ }\texttt{ }\texttt{ }\texttt{ }\texttt{ }\texttt{ }\texttt{ * } \\
\texttt{SA}:\qquad&\texttt{(}\underline{\color{red}{\texttt{U}}}\texttt{) }\texttt{(E)}\texttt{ }\texttt{(E }\texttt{ }\texttt{ E }\texttt{ }\texttt{ E }\texttt{ }\texttt{ E }\texttt{ }\texttt{ }\underline{\color{red}{\texttt{M}}}\texttt{) }\texttt{(E }\texttt{ }\texttt{ E) }\texttt{(E}\texttt{ }\texttt{ }\texttt{ E }\texttt{ }\texttt{ E }\texttt{ }\texttt{ E)}
\end{aligned}
$$

#### 把 LMS 字符的索引放入 SA

从尾到头扫描 $\texttt{Pat}$，对于 LMS 字符 $\texttt{Pat[i]}$，根据 $\texttt{SA[Pat[i]]}$ 的符号进行分类讨论：

U：直接让 $\texttt{SA[Pat[i]] = i}$

M：意味着桶中有至少两个 LMS 字符．

1.  如果桶中有至少三个 LMS 字符：
    就把桶中倒数第二个位置作为临时计数器，标志桶中已填充的 LMS 字符数（桶中倒数第一位就是标志 M）
    将新的 LMS 字符从倒数第三个位置开始插入，让临时计数器自增 1．
    如果发现桶已经满了，就把桶中从桶头到倒数第三个的所有元素向右平移 2 个位置，然后把新元素插入到桶中第二个位置（桶中第一个位置填为 E）

2.  如果桶中有且只有 2 个 LMS 字符，显然不需要计数器，直接从右到左顺序插入即可．

正常的值：

    根据我们之前的讨论，此时不管桶中有两个还是两个以上的 LMS 字符，这都意味着 $\texttt{i}$ 是桶中最后一个待插入的 LMS 字符的位置，

    只需要从桶头开始向左扫描，找到第一个标记为 E 的位置，将其设为 $\texttt{i}$．

最后要从尾到头扫描一遍 $\texttt{SA}$，清除可能残余的特殊符号 M（桶中未被填满，所以 M 和计数器未被覆盖）．

方法是将桶中 LMS 字符如上述步骤一样向右平移 2 位，将左边空出来的位置填为 E．

如下图所示：

$$
\begin{aligned}
\texttt{Index}:\qquad&\texttt{ }\texttt{ 0   1   2   3   4   5   6   7   8   9  10  11  12} \\
\texttt{Pat}:\qquad&\texttt{ }\texttt{ 7   6   6   9   9   6   6   9   9   6   7   1   0} \\
\texttt{SA}:\qquad&\texttt{(}\underline{\color{red}{\texttt{12}}}\texttt{)}\texttt{ (E)}\texttt{ (E }\texttt{ }\texttt{ E }\texttt{ }\texttt{ E }\texttt{ }\texttt{ E }\texttt{ }\texttt{ M}\texttt{) }\texttt{(E }\texttt{ }
\texttt{ E) }\texttt{(E}\texttt{ }\texttt{ }\texttt{ E }\texttt{ }\texttt{ E }\texttt{ }\texttt{ E)}\\
\texttt{SA}:\qquad&\texttt{(12) }\texttt{(E)}\texttt{ (E }\texttt{ }\texttt{ E }\texttt{ }
\texttt{ }\underline{\color{red}{\texttt{9}}}\texttt{ }\texttt{ }{\color{red}{\texttt{ 1 }}}\texttt{ }\texttt{ }
{\color{red}{\texttt{M}}}\texttt{) }\texttt{(E }\texttt{ }\texttt{ E) }\texttt{(E}\texttt{ }\texttt{ }\texttt{ E }
\texttt{ }\texttt{ E }\texttt{ }\texttt{ E)} \\
\texttt{SA}:\qquad&\texttt{(12) }\texttt{(E)}\texttt{ (E }\texttt{ }\texttt{ }{\underline{\color{red}{\texttt{5}}}}
\texttt{ }\texttt{ }\texttt{ }{\texttt{9}}\texttt{ }\texttt{ }{\color{red}{\texttt{ 2 }}}\texttt{ }\texttt{ }
{\color{red}{\texttt{M}}}\texttt{) }\texttt{(E }\texttt{ }\texttt{ E) }\texttt{(E}\texttt{ }\texttt{ }\texttt{ E }
\texttt{ }\texttt{ E }\texttt{ }\texttt{ E)}\\
\texttt{SA}:\qquad&\texttt{(12) }\texttt{(E)}\texttt{ (}\underline{\color{red}{\texttt{1}}}\texttt{ }\texttt{ }{\texttt{ 5}}\texttt{ }\texttt{ }\texttt{ }{\texttt{9}}\texttt{ }\texttt{ }{\color{red}{\texttt{ 3 }}}\texttt{ }\texttt{ }{\color{red}{\texttt{M}}}\texttt{) }\texttt{(E }\texttt{ }\texttt{ E) }\texttt{(E}\texttt{ }\texttt{ }\texttt{ E }\texttt{ }\texttt{ E }\texttt{ }\texttt{ E)}\\
\texttt{SA}:\qquad&\texttt{(12) }\texttt{(E)}\texttt{ (}\texttt{E }\texttt{ }\texttt{ E }\texttt{ }{\color{red}{\texttt{ 1 }}\texttt{ }{\texttt{ 5 }}\texttt{ }\texttt{ }{\texttt{9}}}\texttt{) }\texttt{(E }\texttt{ }\texttt{ E) }\texttt{(E}\texttt{ }\texttt{ }\texttt{ E }\texttt{ }\texttt{ E }\texttt{ }\texttt{ E)}
\end{aligned}
$$

这个阶段，由于每个桶只需要被移动和扫描一次，所以时间复杂度是 $O(n)$．

### 诱导排序 LMS 子串

#### 诱导排序 LMS 前缀

将 LMS 前缀进行诱导排序，同 SA-IS 一样，这部分同后面对后缀的诱导排序完全一样（使用同一个函数），因此这里直接跳过．

这里直接给出排序结果：

$$
\begin{aligned}
\texttt{Index}:\qquad&\texttt{ }\texttt{ 0   1   2   3   4   5   6   7   8   9  10  11  12} \\
\texttt{SA}:\qquad&\texttt{(}\texttt{12}\texttt{)}\texttt{(11)}\texttt{ (1 }\texttt{ }\texttt{ 5 }\texttt{ }\texttt{ 9 }\texttt{ }\texttt{ 2 }\texttt{ }\texttt{ 6}\texttt{) }\texttt{(10 }\texttt{ }\texttt{ 0) }\texttt{(4}\texttt{ }\texttt{ }\texttt{ 8 }\texttt{ }\texttt{ 3 }\texttt{ }\texttt{ 7)}
\end{aligned}
$$

#### 将已排序的 LMS 子串放到 SA 尾部

$$
\begin{aligned}
\texttt{Index}:\qquad&\texttt{ 0   1   2   3   4   5   6   7   8   9  10  11  12} \\
\texttt{SA}:\qquad&\texttt{ }\texttt{E }\texttt{ }\texttt{ E }\texttt{ }\texttt{ E }\texttt{ }\texttt{ E }\texttt{ }\texttt{ E }\texttt{ }\texttt{ E }\texttt{ }\texttt{ E }\texttt{ }\texttt{ E }\texttt{ }\texttt{ E }\texttt{ }{\underline{\color{red}{\texttt{12}}}}\texttt{ }\texttt{ }\texttt{ }{\underline{\color{red}{\texttt{1}}}}\texttt{ }\texttt{ }\texttt{ }{\underline{\color{red}{\texttt{5}}}}\texttt{ }\texttt{ }\texttt{ }{\underline{\color{red}{\texttt{9}}}}
\end{aligned}
$$

### 构建规模缩减的子目标串 Pat1

从左到右扫描 $\texttt{SA}$ 尾部的 LMS 子串，确定其大小关系「重命名」，将 $\texttt{SA[i]}$ 重命名的值存储在 $\texttt{SA}\left[\left\lfloor\frac{\texttt{SA}[i]}{2} \right\rfloor\right]$．

因为 LMS 字符并不相邻，所以不会有冲突，这样做是将重命名后的值按照所代表的子串在 $\texttt{Pat}$ 中的原顺序放置：

$$
\begin{aligned}
\texttt{Index}:\qquad&\texttt{ 0   1   2   3   4   5   6   7   8   9  10  11  12} \\
\texttt{SA}:\qquad&\texttt{ }\underline{\color{red}{\texttt{1}}}\texttt{ }\texttt{ }\texttt{ E }\texttt{ }\texttt{ }\underline{\color{red}{\texttt{1}}}\texttt{ }\texttt{ }\texttt{ E }\texttt{ }\texttt{ }\underline{\color{red}{\texttt{2}}}\texttt{ }\texttt{ }\texttt{ E }\texttt{ }\texttt{ }\underline{\color{red}{\texttt{0}}}\texttt{ }\texttt{ }\texttt{ E }\texttt{ }\texttt{ E }\texttt{ 12 }\texttt{ }\texttt{ 1 }\texttt{ }\texttt{ 5 }\texttt{ }\texttt{ 9 }
\end{aligned}
$$

然后扫描 $\texttt{SA}$，收集这些重命名的值到 $\texttt{SA}$ 头部：

$$
\begin{aligned}
\texttt{Index}:\qquad&\texttt{ 0   1   2   3   4   5   6   7   8   9  10  11  12} \\
\texttt{SA}:\qquad&\texttt{ }\underline{\color{red}{\texttt{1}}}\texttt{ }\texttt{ }\texttt{ }\underline{\color{red}{\texttt{1}}}\texttt{ }\texttt{ }\texttt{ }\underline{\color{red}{\texttt{2}}}\texttt{ }\texttt{ }\texttt{ }\underline{\color{red}{\texttt{0}}}\texttt{ }\texttt{ }\texttt{ E }\texttt{ }\texttt{ E }\texttt{ }\texttt{ E }\texttt{ }\texttt{ E }\texttt{ }\texttt{ E }\texttt{ 12 }\texttt{ }\texttt{ 1 }\texttt{ }\texttt{ 5 }\texttt{ }\texttt{ 9 }
\end{aligned}
$$

### 通过递归解决 Pat1，完成对 LMS 后缀的排序

同 SA-IS 一样，递归解决 $\texttt{SA}$ 头部的规模缩减的 $\texttt{Pat1}$ 的后缀排序，结果存到 $\texttt{SA}$ 尾部：

$$
\begin{aligned}
\texttt{Index}:\qquad&\texttt{ 0   1   2   3   4   5   6   7   8   9  10  11  12} \\
\texttt{SA}:\qquad&\texttt{ }\texttt{1 }\texttt{ }\texttt{ 1 }\texttt{ }\texttt{ 2 }\texttt{ }\texttt{ 0 }\texttt{ }\texttt{ E }\texttt{ }\texttt{ E }\texttt{ }\texttt{ E }\texttt{ }\texttt{ E }\texttt{ }\texttt{ E }\texttt{ }\texttt{ }{\underline{\color{red}{\texttt{3}}}}\texttt{ }\texttt{ }\texttt{ }{\underline{\color{red}{\texttt{0}}}}\texttt{ }\texttt{ }\texttt{ }{\underline{\color{red}{\texttt{1}}}}\texttt{ }\texttt{ }\texttt{ }{\underline{\color{red}{\texttt{2}}}}
\end{aligned}
$$

将 $\texttt{SA}$ 尾部的 $\texttt{SA1}$ 挪到 $\texttt{SA}$ 头部，重新从尾到头扫描 $\texttt{Pat}$，将其中 LMS 字符按照在 $\texttt{Pat}$ 中的顺序放到 $\texttt{SA}$ 尾部：

$$
\begin{aligned}
\texttt{Index}:\qquad&\texttt{ 0   1   2   3   4   5   6   7   8   9  10  11  12} \\
\texttt{SA}:\qquad&\texttt{ }{\underline{\color{red}{\texttt{3}}}}\texttt{ }\texttt{ }\texttt{ }{\underline{\color{red}{\texttt{0}}}}\texttt{ }\texttt{ }\texttt{ }{\underline{\color{red}{\texttt{1}}}}\texttt{ }\texttt{ }\texttt{ }{\underline{\color{red}{\texttt{2}}}}\texttt{ }\texttt{ }\texttt{ E }\texttt{ }\texttt{ E }\texttt{ }\texttt{ E }\texttt{ }\texttt{ E }\texttt{ }\texttt{ E }\texttt{ }\texttt{ }{\underline{\color{red}{\texttt{1}}}}\texttt{ }\texttt{ }\texttt{ }{\underline{\color{red}{\texttt{5}}}}\texttt{ }\texttt{ }\texttt{ }{\underline{\color{red}{\texttt{9}}}}\texttt{ }\texttt{ }{\underline{\color{red}{\texttt{12}}}}
\end{aligned}
$$

依照 $\texttt{SA}$ 尾部的「对照表」，将 $\texttt{SA1}$ 头部的 $\texttt{SA}$ 还原为 $\texttt{Pat}$ 中对应的 LMS 后缀的索引位置：

$$
\begin{aligned}
\texttt{Index}:\qquad&\texttt{ 0   1   2   3   4   5   6   7   8   9  10  11  12} \\
\texttt{SA}:\qquad&{\underline{\color{red}{\texttt{12}}}}\texttt{ }\texttt{ }\texttt{ }{\underline{\color{red}{\texttt{1}}}}\texttt{ }\texttt{ }\texttt{ }{\underline{\color{red}{\texttt{5}}}}\texttt{ }\texttt{ }\texttt{ }{\underline{\color{red}{\texttt{9}}}}\texttt{ }\texttt{ }\texttt{ E }\texttt{ }\texttt{ E }\texttt{ }\texttt{ E }\texttt{ }\texttt{ E }\texttt{ }\texttt{ E }\texttt{ }\texttt{ 1 }\texttt{ }\texttt{ 5 }\texttt{ }\texttt{ 9 }\texttt{ 12 }
\end{aligned}
$$

将 $\texttt{SA}$ 头部的排好序的 LMS 后缀按顺序放入到对应的桶中（从尾部开始放）：

$$
\begin{aligned}
\texttt{Index}:\qquad&\texttt{ }\texttt{ 0   1   2   3   4   5   6   7   8   9  10  11  12} \\
\texttt{SA}:\qquad&\texttt{(}{\underline{\color{red}{\texttt{12}}}}\texttt{)}\texttt{ }\texttt{(E)}\texttt{ (}\texttt{E }\texttt{ }\texttt{ E }\texttt{ }\texttt{ }{\underline{\color{red}{\texttt{1}}}}\texttt{ }\texttt{ }\texttt{ }{\underline{\color{red}{\texttt{5}}}}\texttt{ }\texttt{ }\texttt{ }{\underline{\color{red}{\texttt{9}}}}\texttt{)}\texttt{ }\texttt{(E }\texttt{ }\texttt{ E) }\texttt{(E}\texttt{ }\texttt{ }\texttt{ E }\texttt{ }\texttt{ E }\texttt{ }\texttt{ E)}
\end{aligned}
$$

### 对 Pat1 中所有的后缀进行诱导排序

这一部分就是利用前面用过的内部计数器技巧，进行原地版的诱导排序．

假如我们已经有排好序的 LMS 后缀（在桶尾），来诱导 L 型后缀[^诱导顺序]：

$$
\begin{aligned}
\texttt{Index}:\qquad&\texttt{ }\texttt{ 0   1   2   3   4   5   6   7   8   9  10  11  12} \\
\texttt{Pat}:\qquad&\texttt{ }\texttt{ 7   6   6   9   9   6   6   9   9   6   7   1   0} \\
\texttt{SA}:\qquad&\texttt{(12) }\texttt{(E)}\texttt{ (}\texttt{E }\texttt{ }\texttt{ E }\texttt{ }{\texttt{ 1 }\texttt{ }{\texttt{ 5 }}\texttt{ }\texttt{ }{\texttt{9}}}\texttt{) }\texttt{(E }\texttt{ }\texttt{ E) }\texttt{(E}\texttt{ }\texttt{ }\texttt{ E }\texttt{ }\texttt{ E }\texttt{ }\texttt{ E)}
\end{aligned}
$$

如同排序 LMS 字符一样，先对 L 型字符用特殊符号计数：

$$
\begin{aligned}
\texttt{Index}:\qquad&\texttt{ }\texttt{ 0   1   2   3   4   5   6   7   8   9  10  11  12} \\
\texttt{Pat}:\qquad&\texttt{ }\texttt{ 7   6   6   9   9   6   6   9   9   6   7   1   0} \\
\texttt{SA}:\qquad&\texttt{(}{{\texttt{12}}}\texttt{)}\texttt{ }\texttt{(}{\underline{\color{red}{\texttt{U}}}}\texttt{)}\texttt{ }\texttt{(E }\texttt{ }\texttt{ E }\texttt{ }\texttt{ 1 }\texttt{ }\texttt{ 5 }\texttt{ }{\texttt{ 9}}\texttt{) }\texttt{(}{\underline{\color{red}{\texttt{M}}}}\texttt{ }\texttt{ }\texttt{ E) }\texttt{(}{\underline{\color{red}{\texttt{M}}}}\texttt{ }\texttt{ }\texttt{ E }\texttt{ }\texttt{ E }\texttt{ }\texttt{ E)}
\end{aligned}
$$

从左到右扫描 SA，同对 LMS 字符排序一样，复杂一点的是判断 $\texttt{suf[SA[i] - 1]}$ 的类型，需要分类讨论（详情参考代码）：

$$
\begin{aligned}
\texttt{Index}:\qquad&\texttt{ }\texttt{ 0   1   2   3   4   5   6   7   8   9  10  11  12} \\
\texttt{SA}:\qquad&\texttt{(}{\overrightarrow{\color{red}{\texttt{12}}}\texttt{)}\texttt{(}{\underline{\color{red}{\texttt{11}}}}}\texttt{)}\texttt{  (E   E   1   5   9) (M   E) (M   E   E   E)}\\
\texttt{SA}:\qquad&\texttt{(}\texttt{12}\texttt{)}\texttt{(}{\overrightarrow{\color{red}{\texttt{11}}}}\texttt{)}\texttt{  (E   E   1   5   9)}\texttt{(}{\underline{\color{red}{\texttt{10}}}}\texttt{ }\texttt{ }\texttt{ E)}\texttt{ (M   E   E   E)}\\
\texttt{SA}:\qquad&\texttt{(12)(11)}\texttt{  (E   E  }\texttt{ }\texttt{ } {\overrightarrow{\color{red}{\texttt{1}}}}\texttt{ }\texttt{  5   9)}\texttt{(10 }\texttt{ }\texttt{ }{\underline{\color{red}{\texttt{0}}}}\texttt{)}\texttt{ (M   E   E   E)}\\
\texttt{SA}:\qquad&\texttt{(12)(11)}\texttt{  (E   E   1 }\texttt{ }\texttt{ } {\overrightarrow{\color{red}{\texttt{5}}}}\texttt{ }\texttt{  9)}\texttt{(10   0)}\texttt{ (}{\color{red}{\texttt{M   1}}}\texttt{ }\texttt{ }\texttt{ }{\underline{\color{red}{\texttt{4}}}}\texttt{ }\texttt{ }\texttt{ E)}\\
\texttt{SA}:\qquad&\texttt{(12)(11)}\texttt{  (E   E   1   5}\texttt{ }\texttt{ } {\overrightarrow{\color{red}{\texttt{9}}}}\texttt{)}\texttt{(10   0)}\texttt{ (}{\color{red}{\texttt{M   2}}}\texttt{ }\texttt{ }\texttt{ 4 }\texttt{ }\texttt{ }{\underline{\color{red}{\texttt{8}}}}\texttt{)}\\
\texttt{SA}:\qquad&\texttt{(12)(11)}\texttt{  (E   E   1   5   9)(10   0)}\texttt{ (}{\overrightarrow{\color{red}{\texttt{4}}}}\texttt{ }\texttt{ 8 }\texttt{ }\texttt{ }{\underline{\color{red}{\texttt{3}}}}\texttt{ }\texttt{ }\texttt{ E}\texttt{)}\\
\texttt{SA}:\qquad&\texttt{(12)(11)}\texttt{  (E   E   1   5   9)(10   0)}\texttt{ (4 }\texttt{ }\texttt{ }{\overrightarrow{\color{red}{\texttt{8}}}}\texttt{ }\texttt{ 3 }\texttt{ }\texttt{ }{\underline{\color{red}{\texttt{7}}}}\texttt{)}
\end{aligned}
$$

区别于 SA-IS 的是，对一个类型字符诱导排序后，需要清理 LMS 字符以免对后面的原地诱导排序：

$$
\begin{aligned}
\texttt{Index}:\qquad&\texttt{ }\texttt{ 0   1   2   3   4   5   6   7   8   9  10  11  12} \\
\texttt{SA}:\qquad&\texttt{(12)(11)}\texttt{  (E   E  }\texttt{ }\texttt{ }{\underline{\color{red}{\texttt{E}}}}\texttt{ }\texttt{ }\texttt{ }{\underline{\color{red}{\texttt{E}}}}\texttt{ }\texttt{ }\texttt{ }{\underline{\color{red}{\texttt{E}}}}\texttt{)}\texttt{(10   0)}\texttt{ (4   8   3   7)}
\end{aligned}
$$

至于从 L 后缀诱导 S 后缀与从 LMS 后缀诱导 L 后缀完全对称，这里就不做多余介绍．

到这儿为止，诱导排序就完成了．

#### 实现

时间性能上和 SA-IS 没有显著差别，空间占用变为不到原来的 $\dfrac{1}{3}$（代码量多 1 倍），算是不愧为原文 Optimal In-Place Suffix Sorting[^in-place-sa-sort]的标题．

??? note "参考代码"
    ```rust
    use std::cmp::max;
    use std::cmp::Ordering;
    use std::slice::from_raw_parts_mut;
    
    
    const LTYPE: bool = false;
    const STYPE: bool = true;
    const MAX_SA_VALUE: usize = usize::MAX / 2;
    const EMPTY: usize = MAX_SA_VALUE + 1;
    const UNIQUE: usize = MAX_SA_VALUE + 2;
    const MULTI: usize = MAX_SA_VALUE + 3;  // >= 258
    
    
    fn lms_str_cmp<E: Ord>(l1: &[E], l2: &[E]) -> Ordering {
        for (x, y) in l1.iter().zip(l2.iter()) {
            let cmp_res = x.cmp(&y);
            
            if cmp_res != Ordering::Equal { return cmp_res; }
        }
        
        Ordering::Equal
    }
    
    #[inline]
    fn pat_char_type(cur: usize, prev: usize, last_scanned_type: bool) -> bool {
        if cur < prev || cur == prev && last_scanned_type == STYPE { STYPE }
        else { LTYPE }
    }
    
    
    fn rename_pat(pat: &mut [usize], sa: &mut [usize]) {
        let patlastpos = pat.len() - 1;
        // 全部刷成bucket head
        //sa.fill(0);
        for i in 0..sa.len() { sa[i] = 0 }
        
        for i in 0..pat.len() { sa[pat[i]] += 1 }
        for i in 1..sa.len() { sa[i] += sa[i - 1] }
        
        for i in 0..pat.len() - 1 {
            pat[i] = sa[pat[i]] - 1;
        };
        // 将L-suffix刷成bucket head
        //sa.fill(0);
        for i in 0..sa.len() { sa[i] = 0 }
        
        for i in 0..pat.len() { sa[pat[i]] += 1 }
        let mut last_scanned_type = STYPE;
        pat[patlastpos] = 0;
        for i in (0..pat.len() - 1).rev() {
            if pat_char_type(pat[i], pat[i + 1], last_scanned_type) == STYPE {
                last_scanned_type = STYPE;
            } else {
                pat[i] -= sa[pat[i]] - 1;
                last_scanned_type = LTYPE;
            }
        }
    
    }
    
    
    fn sort_lms_char(pat: &mut [usize], sa: &mut [usize]) -> usize {
        //sa.fill(EMPTY);
        for i in 0..sa.len() { sa[i] = EMPTY }
        
        let mut last_scanned_type = STYPE;
        for i in (0..pat.len() - 1).rev() {
            if pat_char_type(pat[i], pat[i + 1], last_scanned_type) == STYPE {
                last_scanned_type = STYPE;
            } else {
                if last_scanned_type == STYPE {  // pat[i + 1] is LMS type
                    sa[pat[i + 1]] += 1;
                }
                
                last_scanned_type = LTYPE;
            }
        }
        
        let mut lms_cnt = 0;
        last_scanned_type = STYPE;
        for i in (0..pat.len() - 1).rev() {
            if pat_char_type(pat[i], pat[i + 1], last_scanned_type) == STYPE {
                last_scanned_type = STYPE;
            } else {
                let e_i = i + 1;
                let e = pat[e_i];
                
                if last_scanned_type == STYPE {  // pat[i + 1] is LMS type
                    lms_cnt += 1;
                    if sa[e] == UNIQUE {
                        sa[e] = e_i;
                    } else if sa[e] >= MULTI && sa[e - 1] == EMPTY {
                        if sa[e - 2] == EMPTY {
                            sa[e - 2] = e_i;
                            sa[e - 1] = 1;  // set counter
                        } else {  // MUL = 2
                            sa[e] = e_i;
                            sa[e - 1] = EMPTY;
                        }
                    } else if sa[e] >= MULTI && sa[e - 1] != EMPTY {
                        let c = sa[e - 1];  // get counter
                        
                        if sa[e - 2 - c] == EMPTY {
                            sa[e - 2 - c] = e_i;
                            sa[e - 1] += 1;  // update counter
                        } else {
                            for j in (1..c + 1).rev() {
                                sa[e - c + j] = sa[e - 2 - c + j]
                            }
                            sa[e - c] = e_i;
                            sa[e - c - 1] = EMPTY;
                        }
                    } else if sa[e] < EMPTY {
                        for j in (0..e).rev() {
                            if sa[j] == EMPTY {
                                sa[j] = e_i;
                                break;
                            }
                        }
                    }
                }
                
                last_scanned_type = LTYPE;
            }
        }
        
        for i in (0..pat.len()).rev() {
            if sa[i] >= MULTI {
                let c = sa[i - 1];
                for j in (1..c + 1).rev() {  // 逆序防止前面的覆盖后面的
                    sa[i - c + j] = sa[i - 2 - c + j];
                }
                sa[i - c - 1] = EMPTY;
                sa[i - c] = EMPTY;
            }
        }
        
        lms_cnt
    }
    
    
    fn sort_lms_substr(pat: &mut [usize], sa: &mut [usize]) {
        // step 1
        induced_sort(pat, sa);
        
        // step 2
        let pat_last_pos = pat.len() - 1;
        let mut lms_cnt = 0;
        let mut i = pat_last_pos;
        let mut bucket_tail_ptr = pat_last_pos + 1;  // for renamed bucket ver
        let mut bucket = EMPTY;  // 可以省略，但是为了书写代码方便
        let mut num = 0;  // S type number of bucket
        while i > 0 {
            if pat[sa[i]] != bucket {  // reach new bucket
                num = 0;
                
                let mut l = 0;
                while pat[sa[i - l]] == pat[sa[i]] {  // 扫描桶来计算桶中S字符数量，根据定义 当l=i时循环必然终止
                    let pat_i = sa[i - l];             // l < i, 即 i - l > 0, 0 <= pat_i < patlen - 1
                    if pat[pat_i] < pat[pat_i + 1] {
                        let mut k = pat_i;
                        while k > 0 && pat[k - 1] == pat[pat_i] { k -= 1 }
                        num += pat_i - k + 1;
                    } else {
                        break;   // bucket不含S字符，结束扫描
                    }
                    
                    l += 1;
                }
                
                bucket_tail_ptr = i;
                bucket = pat[sa[bucket_tail_ptr]];
            }
            
            if num > 0
            && i > bucket_tail_ptr - num
            && sa[i] > 0
            && pat[sa[i]] < pat[sa[i] - 1]  {
                sa[pat_last_pos - lms_cnt] = sa[i];
                lms_cnt += 1;
            }
            
            i -= 1;
        }
        
        sa[pat_last_pos - lms_cnt ] = sa[i];  // i = 0
        lms_cnt += 1;
        //sa[0..pat_last_pos - lms_cnt + 1].fill(EMPTY);
        for i in 0..pat_last_pos - lms_cnt + 1 { sa[i] = EMPTY }
    }
    
    
    fn construct_pat1(pat: &mut [usize], sa: &mut [usize], lms_cnt: usize) -> bool {
        let patlen = pat.len();
        
        let mut prev_lms_str_len = 1;
        let mut rank = 0;
        sa[(patlen - 1) / 2] = rank;
        let mut has_duplicated_char = false;
        for i in patlen - lms_cnt + 1..patlen {  // 从警戒哨字符的下一个字符开始
            let mut j = sa[i];
            while pat[j] <= pat[j + 1] { j += 1 } // 寻找suf(sa[i])右边第一个L字符，因为排除了警戒哨这个LMS后缀，所以必然不会越界
            let mut k = j;
            while k + 1 < patlen && pat[k] >= pat[k + 1] { k += 1 }  // 找到suf(sa[i])右边第一个LMS字符
            let cur_lms_str_len = k + 1 - sa[i];
            let cmp_res = lms_str_cmp(&pat[sa[i]..sa[i] + cur_lms_str_len], &pat[sa[i - 1]..sa[i - 1] + prev_lms_str_len]);
            
            if  cmp_res != Ordering::Equal {
                rank += 1
            }
            
            if rank == sa[sa[i - 1] / 2] {
                has_duplicated_char = true;
            }
            let rank_index = sa[i] / 2;
            sa[rank_index] = rank;  // 整除
            
            prev_lms_str_len = cur_lms_str_len;
        }
        
        // move to head of sa
        let mut j = 0;
        for i in 0..patlen - lms_cnt {
            if sa[i] != EMPTY {
                sa[j] = sa[i];
                if i > j {
                    sa[i] = EMPTY;
                }
                j += 1;
            }
        }
        //sa[lms_cnt..patlen].fill(EMPTY);
        for i in lms_cnt..patlen { sa[i] = EMPTY }
        
        has_duplicated_char
    }
    
    fn sort_lms_suf(pat: &mut [usize], sa: &mut [usize], lms_cnt: usize, has_duplicated_char: bool) {
        // solve T1 recursively
        let patlen = pat.len();
        let salen = sa.len();
        unsafe {
            let sa_ptr = sa.as_mut_ptr();
            let mut pat1 = from_raw_parts_mut(sa_ptr, lms_cnt);
            let mut sa1 = from_raw_parts_mut(sa_ptr.offset((patlen - lms_cnt) as isize), salen - (patlen - lms_cnt));
            
            if has_duplicated_char {
                _compute_suffix_array_16_1(&mut pat1, &mut sa1);
            } else {
                for i in 0..lms_cnt { sa1[pat1[i]] = i }
            }
        }
        
        // move SA1 to SA[0...n1-1]
        for i in 0..lms_cnt {
            sa[i] = sa[patlen- lms_cnt + i];
        }
        
        // put all LMS-suffixes in SA tail
        let mut last_scanned_type = STYPE;
        let mut j = 0;
        for i in (0..pat.len() - 1).rev() {
            if pat[i] < pat[i + 1] || pat[i] == pat[i + 1] && last_scanned_type == STYPE {
                last_scanned_type = STYPE;
            } else {
                if last_scanned_type == STYPE {
                    sa[patlen - 1 - j] = i + 1;
                    j += 1;
                }
                
                last_scanned_type = LTYPE;
            }
        }
        
        // backward map the LMS-suffixes rank
        for i in 0..lms_cnt {
            let relative_rank = sa[i];
            sa[i] = sa[patlen - lms_cnt + relative_rank];
            sa[patlen - lms_cnt + relative_rank] = EMPTY;
        }
        
        let mut tail = EMPTY;
        let mut rfp = EMPTY;
        for i in (1..lms_cnt).rev() { // sa[0] 保持原位
            if pat[sa[i]] != tail {
                tail = pat[sa[i]];
                rfp = tail;
            }
            
            sa[rfp] = sa[i];
            if rfp != i { sa[i] = EMPTY }
            rfp -= 1;
        }
    }
    
    // PASS!
    fn induced_sort(pat: &mut [usize], sa: &mut [usize]) {
        let patlen = pat.len();
        
        // place L-suff in SA
        // init
        let mut last_scanned_type = STYPE;
        for i in (0..patlen - 1).rev() {
            if pat_char_type(pat[i], pat[i + 1], last_scanned_type) == LTYPE {
                sa[pat[i]] += 1;  // >= EMPTY
                last_scanned_type = LTYPE;
            } else {
                last_scanned_type = STYPE;
            }
        }
        //place
        let mut i = 0;
        while i < patlen {
            if sa[i] < EMPTY && sa[i] > 0 {
                let j = sa[i] - 1;
                let mut is_ltype = false;
                if pat[j] > pat[j + 1] {
                    is_ltype = true;
                } else if pat[j] == pat[j + 1] {  // 判断sa[i]是否是L后缀的编号
                    let next_i = sa[pat[sa[i]]];
                    if next_i >= MULTI {
                        is_ltype = true;
                    } else if next_i < EMPTY && pat[sa[i]] + 1 < patlen {
                        if sa[pat[sa[i]] + 1] == EMPTY {
                            is_ltype = true;
                        } else if sa[pat[sa[i]] + 1] < EMPTY {
                            if pat[sa[pat[sa[i]] + 1]] == pat[sa[i]] {
                                is_ltype = true;
                            }
                        }
                    }
                }
                
                if is_ltype {
                    if sa[pat[j]] == UNIQUE {
                        sa[pat[j]] = j;
                    } else if sa[pat[j]] >= MULTI && sa[pat[j] + 1] == EMPTY {
                        if sa[pat[j]] - EMPTY > 2 {
                            sa[pat[j] + 2] = j;
                            sa[pat[j] + 1] = 1;  // set counter
                        } else {
                            sa[pat[j]] = j;
                        }
                    } else if sa[pat[j]] >= MULTI && sa[pat[j] + 1] != EMPTY {
                        let e = pat[j];
                        let c = sa[e + 1];
                        let lfp = e + c + 2;
                        if  c + 2 < sa[pat[j]] - EMPTY {  // 没到bucket尾部
                            sa[lfp] = j;
                            sa[e + 1] += 1;  // update counter
                        } else {
                            for k in 1..c + 1 {
                                sa[e + k - 1] = sa[e + k + 1];
                            }
                            sa[e + c] = j;
                            sa[e + c + 1] = EMPTY;
                            if i >= e + 2 && i <= e + c + 1 {
                                i -= 2;
                            }
                        }
                    } else if sa[pat[j]] < EMPTY {
                        for k in pat[j]..patlen {
                            if sa[k] == EMPTY {
                                sa[k] = j;
                                break;
                            }
                        }
                    }
                }
            } else if sa[i] >= MULTI {
                i += 1;
            }
            
            i += 1;
        }
        
        // remove LMS-suff form SA, 一个桶里可能有多个LMS后缀
        last_scanned_type = STYPE;
        for i in (0..pat.len() - 1).rev() {
            if pat_char_type(pat[i], pat[i + 1], last_scanned_type) == STYPE {
                last_scanned_type = STYPE;
            } else {
                if last_scanned_type == STYPE {  // pat[i + 1] is LMS type
                    if sa[pat[i + 1]] <= EMPTY {
                        sa[pat[i + 1]] = UNIQUE;
                    } else {
                        sa[pat[i + 1]] += 1;
                    }
                }
                
                last_scanned_type = LTYPE;
            }
        }
        i = patlen - 1;
        while i > 0 {
            if sa[i] > EMPTY {
                let c = sa[i] - EMPTY;
                for k in 0..c {
                    sa[i - k] = EMPTY;
                }
                i -= c - 1;
            }
            
            i -= 1;
        }
        sa[0] = pat.len() - 1;
        
        // place S-suff in SA
        // init
        let mut last_scanned_type = STYPE;
        for i in (0..patlen - 1).rev() {
            if pat_char_type(pat[i], pat[i + 1], last_scanned_type) == STYPE {
                if sa[pat[i]] >= EMPTY {
                    sa[pat[i]] += 1;
                } else {
                    sa[pat[i]] = UNIQUE;
                }
                last_scanned_type = STYPE;
            } else {
                last_scanned_type = LTYPE;
            }
        }
        i = patlen - 1;
        while i > 0 {
            if sa[i] < EMPTY && sa[i] > 0 {
                let j = sa[i] - 1;
                let mut is_stype = false;
                if pat[j] < pat[j + 1] {
                    is_stype = true;
                } else if pat[j] == pat[j + 1] {  // 判断sa[i]是否是S后缀的编号
                    let next_i = sa[pat[sa[i]]];
                    if next_i >= MULTI {
                        is_stype = true;
                    } else if next_i < EMPTY && pat[sa[i]] - 1 > 0 {
                        if sa[pat[sa[i]] - 1] == EMPTY {
                            is_stype = true;
                        } else if sa[pat[sa[i]] - 1] < EMPTY {
                            if pat[sa[pat[sa[i]] - 1]] == pat[sa[i]] {
                                is_stype = true;
                            }
                        }
                    }
                }
                
                if is_stype {
                    if sa[pat[j]] == UNIQUE {
                        sa[pat[j]] = j;
                    } else if sa[pat[j]] >= MULTI && sa[pat[j] - 1] == EMPTY {
                        if sa[pat[j]] - EMPTY > 2 {
                            sa[pat[j] - 2] = j;
                            sa[pat[j] - 1] = 1;  // set counter
                        } else {
                            sa[pat[j]] = j;
                        }
                    } else if sa[pat[j]] >= MULTI && sa[pat[j] - 1] != EMPTY {
                        let e = pat[j];
                        let c = sa[e - 1];
                        let num = sa[pat[j]] - EMPTY;
                        if c + 2 < num {  // 没到bucket头部
                            let rfp = e - c - 2;
                            sa[rfp] = j;
                            sa[e - 1] += 1;
                        } else {
                            for k in 1..c + 1 {
                                sa[e - k + 1] = sa[e - k - 1];
                            }
                            sa[e - c] = j;
                            sa[e - c - 1] = EMPTY;
                            if i >= e - num + 1 && i <= e - 2 {
                                i += 2;
                            }
                        }
                    } else if sa[pat[j]] < EMPTY {
                        for k in (0..pat[j]).rev() {
                            if sa[k] == EMPTY {
                                sa[k] = j;
                                break;
                            }
                        }
                    }
                }
            } else if sa[i] >= MULTI {
                i -= 1;
            }
            i -= 1;
        }
    }
    
    fn _compute_suffix_array_16_1(pat: &mut [usize], sa: &mut [usize]) {
        rename_pat(pat, sa);
        let lms_cnt = sort_lms_char(pat, sa);
        sort_lms_substr(pat, sa);
        let has_duplicated_char = construct_pat1(pat, sa, lms_cnt);
        sort_lms_suf(pat, sa, lms_cnt, has_duplicated_char);
        induced_sort(pat, sa);
    }
    
    pub fn suffix_array_16(pat: &[u8]) -> Vec<usize> {
        let mut pat = pat.into_iter().map(|x| *x as usize).collect::<Vec<usize>>();
        pat.push(0);
        let mut sa = vec![0; max(pat.len(), 256) * 1];
        _compute_suffix_array_16_1(&mut pat[..], &mut sa[..]);
        
        sa
    }
    
    fn input() -> String {
        use std::io;
        
        let mut input = String::new();
        io::stdin().read_line(&mut input).unwrap();
        String::from(input.trim())
    }
    
    
    fn main() {
        let pat = input();
        
        let sa_16 = suffix_array_16(pat.as_bytes());
        
        for i in 1..pat.len() + 1 { print!("{} ", sa_16[i] + 1) }
    }
    ```

## 在只读的整形字母表上的后缀排序

使用复杂方法解决复杂问题，通过分治，解决空间紧张的问题．

算法实现的难点在于在 $\texttt{SA}$ 上构建 BitMaps[^np12]，来替代本来由重命名后的 T 所指示的指示桶尾/桶头的位置．

这里的 BitMaps 指得是使用比特向量（bit vector）表示的有序字典（multiset），是一种紧凑型结构（compact data structure）．

有兴趣了解的暂时只能阅读原文以及本文引用的 BitMaps 的有关论文自行了解．

## 在只读的一般字母表上的后缀排序

前置知识是归并排序和堆排序．

由于笔者对于其中确定字符类型的方法的时间复杂度有疑问，这里也不再介绍，建议阅读原文自行了解．

## 注解

[^in-place-sa-sort]: Li, Zhize; Li, Jian; Huo, Hongwei (2016).*Optimal In-Place Suffix Sorting*. Proceedings of the 25th International Symposium on String Processing and Information Retrieval (SPIRE). Lecture Notes in Computer Science. 11147. Springer. pp. 268–284. arXiv:1610.08305. doi:10.1007/978-3-030-00479-8\_22. ISBN:978-3-030-00478-1.

[^nzc09a]: Ge Nong, Sen Zhang, and Wai Hong Chan. Linear suffix array construction by almost pure induced-sorting. In Data Compression Conference (DCC), pages 193–202. IEEE, 2009.

[^sa-is介绍]: 推荐阅读 [博文](https://riteme.site/blog/2016-6-19/sais.html) 和它的 [issue 列表](https://github.com/riteme/riteme.github.io/issues/28)

[^诱导顺序]: 如果是 LML 后缀，就先诱导 S 型后缀，唯一区别是计算 LML 后缀时需要将警戒哨也算进去．

[^np12]: Gonzalo Navarro and Eliana Providel. Fast, small, simple rank/select on bitmaps. In Proc. 11th International Symposium on Experimental Algorithms (SEA), pages 295–306, 2012.


## string/sa.md

## 一些约定

字符串相关的定义请参考 [字符串基础](./basic.md)．

字符串下标从 $1$ 开始．

字符串 $s$ 的长度为 $n$．

" 后缀 $i$" 代指以第 $i$ 个字符开头的后缀，存储时用 $i$ 代表字符串 $s$ 的后缀 $s[i\dots n]$．

## 后缀数组是什么？

后缀数组（Suffix Array）主要关系到两个数组：$sa$ 和 $rk$．

其中，$sa[i]$ 表示将所有后缀排序后第 $i$ 小的后缀的编号，也是所说的后缀数组，后文也称编号数组 $sa$；

$rk[i]$ 表示后缀 $i$ 的排名，是重要的辅助数组，后文也称排名数组 $rk$．

这两个数组满足性质：$sa[rk[i]]=rk[sa[i]]=i$．

### 解释

后缀数组示例：

[![](./images/sa1.png)][2]

## 后缀数组怎么求？

### O(n^2logn) 做法

相信这个做法大家还是能自己想到的：将盛有全部后缀字符串的数组进行 `sort` 排序，由于排序进行 $O(n\log n)$ 次字符串比较，每次字符串比较要 $O(n)$ 次字符比较，所以这个排序是 $O(n^2\log n)$ 的时间复杂度．

### O(nlog^2n) 做法

这个做法要用到倍增的思想．

首先对字符串 $s$ 的所有长度为 $1$ 的子串，即每个字符进行排序，得到排序后的编号数组 $sa_1$ 和排名数组 $rk_1$．

倍增过程：

1.  用两个长度为 $1$ 的子串的排名，即 $rk_1[i]$ 和 $rk_1[i+1]$，作为排序的第一第二关键字，就可以对字符串 $s$ 的每个长度为 $2$ 的子串：$\{s[i\dots \min(i+1, n)]\ |\ i \in [1,\ n]\}$ 进行排序，得到 $sa_2$ 和 $rk_2$；

2.  之后用两个长度为 $2$ 的子串的排名，即 $rk_2[i]$ 和 $rk_2[i+2]$，作为排序的第一第二关键字，就可以对字符串 $s$ 的每个长度为 $4$ 的子串：$\{s[i\dots \min(i+3, n)]\ |\ i \in [1,\ n]\}$ 进行排序，得到 $sa_4$ 和 $rk_4$；

3.  以此倍增，用长度为 $w/2$ 的子串的排名，即 $rk_{w/2}[i]$ 和 $rk_{w/2}[i+w/2]$，作为排序的第一第二关键字，就可以对字符串 $s$ 的每个长度为 $w$ 的子串 $s[i\dots \min(i+w-1,\ n)]$ 进行排序，得到 $sa_w$ 和 $rk_w$．其中，类似字母序排序规则，当 $i+w>n$ 时，$rk_w[i+w]$ 视为无穷小；

4.  $rk_w[i]$ 即是子串 $s[i\dots i + w - 1]$ 的排名，这样当 $w \geqslant n$ 时，得到的编号数组 $sa_w$，也就是我们需要的后缀数组．

#### 过程

倍增排序示意图：

[![](./images/sa2.png)][2]

显然倍增的过程是 $O(\log n)$，而每次倍增用 `sort` 对子串进行排序是 $O(n\log n)$，而每次子串的比较花费 $2$ 次字符比较；

除此之外，每次倍增在 `sort` 排序完后，还有额外的 $O(n)$ 时间复杂度的，更新 $rk$ 的操作，但是相对于 $O(n\log n)$ 被忽略不计；

所以这个算法的时间复杂度就是 $O(n\log^2n)$．

??? note "实现"
    ```cpp
    #include <algorithm>
    #include <cstdio>
    #include <cstring>
    #include <iostream>
    
    using namespace std;
    
    constexpr int N = 1000010;
    
    char s[N];
    int n, w, sa[N], rk[N << 1], oldrk[N << 1];
    
    // 为了防止访问 rk[i+w] 导致数组越界，开两倍数组．
    // 当然也可以在访问前判断是否越界，但直接开两倍数组方便一些．
    
    int main() {
      int i, p;
    
      scanf("%s", s + 1);
      n = strlen(s + 1);
      for (i = 1; i <= n; ++i) sa[i] = i, rk[i] = s[i];
    
      for (w = 1; w < n; w <<= 1) {
        sort(sa + 1, sa + n + 1, [](int x, int y) {
          return rk[x] == rk[y] ? rk[x + w] < rk[y + w] : rk[x] < rk[y];
        });  // 这里用到了 lambda
        memcpy(oldrk, rk, sizeof(rk));
        // 由于计算 rk 的时候原来的 rk 会被覆盖，要先复制一份
        // 若两个子串相同，它们对应的 rk 也需要相同，所以要去重
        for (p = 0, i = 1; i <= n; ++i) {
          if (oldrk[sa[i]] == oldrk[sa[i - 1]] &&
              oldrk[sa[i] + w] == oldrk[sa[i - 1] + w]) {
            rk[sa[i]] = p;
          } else {
            rk[sa[i]] = ++p;
          }
        }
      }
    
      for (i = 1; i <= n; ++i) printf("%d ", sa[i]);
    
      return 0;
    }
    ```

### O(nlogn) 做法

在刚刚的 $O(n\log^2n)$ 做法中，单次排序是 $O(n\log n)$ 的，如果能 $O(n)$ 排序，就能 $O(n\log n)$ 计算后缀数组了．

前置知识：[计数排序](../basic/counting-sort.md)，[基数排序](../basic/radix-sort.md)．

由于计算后缀数组的过程中排序的关键字是排名，值域为 $O(n)$，并且是一个双关键字的排序，可以使用基数排序优化至 $O(n)$．

??? note "实现"
    ```cpp
    #include <algorithm>
    #include <cstdio>
    #include <cstring>
    #include <iostream>
    
    using namespace std;
    
    constexpr int N = 1000010;
    
    char s[N];
    int n, sa[N], rk[N << 1], oldrk[N << 1], id[N], cnt[N];
    
    int main() {
      int i, m, p, w;
    
      scanf("%s", s + 1);
      n = strlen(s + 1);
      m = 127;
      for (i = 1; i <= n; ++i) ++cnt[rk[i] = s[i]];
      for (i = 1; i <= m; ++i) cnt[i] += cnt[i - 1];
      for (i = n; i >= 1; --i) sa[cnt[rk[i]]--] = i;
      memcpy(oldrk + 1, rk + 1, n * sizeof(int));
      for (p = 0, i = 1; i <= n; ++i) {
        if (oldrk[sa[i]] == oldrk[sa[i - 1]]) {
          rk[sa[i]] = p;
        } else {
          rk[sa[i]] = ++p;
        }
      }
    
      for (w = 1; w < n; w <<= 1, m = n) {
        // 对第二关键字：id[i] + w进行计数排序
        memset(cnt, 0, sizeof(cnt));
        memcpy(id + 1, sa + 1,
               n * sizeof(int));  // id保存一份儿sa的拷贝，实质上就相当于oldsa
        for (i = 1; i <= n; ++i) ++cnt[rk[id[i] + w]];
        for (i = 1; i <= m; ++i) cnt[i] += cnt[i - 1];
        for (i = n; i >= 1; --i) sa[cnt[rk[id[i] + w]]--] = id[i];
    
        // 对第一关键字：id[i]进行计数排序
        memset(cnt, 0, sizeof(cnt));
        memcpy(id + 1, sa + 1, n * sizeof(int));
        for (i = 1; i <= n; ++i) ++cnt[rk[id[i]]];
        for (i = 1; i <= m; ++i) cnt[i] += cnt[i - 1];
        for (i = n; i >= 1; --i) sa[cnt[rk[id[i]]]--] = id[i];
    
        memcpy(oldrk + 1, rk + 1, n * sizeof(int));
        for (p = 0, i = 1; i <= n; ++i) {
          if (oldrk[sa[i]] == oldrk[sa[i - 1]] &&
              oldrk[sa[i] + w] == oldrk[sa[i - 1] + w]) {
            rk[sa[i]] = p;
          } else {
            rk[sa[i]] = ++p;
          }
        }
      }
    
      for (i = 1; i <= n; ++i) printf("%d ", sa[i]);
    
      return 0;
    }
    ```

### 一些常数优化

如果你把上面那份代码交到 [LOJ #111: 后缀排序](https://loj.ac/problem/111) 上：

![](./images/sa3.png)

这是因为，上面那份代码的常数的确很大．

#### 第二关键字无需计数排序

思考一下第二关键字排序的实质，其实就是把超出字符串范围（即 $sa[i] + w > n$）的 $sa[i]$ 放到 $sa$ 数组头部，然后把剩下的依原顺序放入：

```cpp
int cur = 0;
for (int i = n - w + 1; i <= n; i++) id[++cur] = i;
for (int i = 1; i <= n; i++)
  if (sa[i] > w) id[++cur] = sa[i] - w;
```

#### 优化计数排序的值域

每次对 $rk$ 进行更新之后，我们都计算了一个 $p$，这个 $p$ 即是 $rk$ 的值域，将值域改成它即可．

#### 若排名都不相同可直接生成后缀数组

考虑新的 $rk$ 数组，若其值域为 $[1,n]$ 那么每个排名都不同，此时无需再排序．

??? note "实现"
    ```cpp
    #include <algorithm>
    #include <cstdio>
    #include <cstring>
    #include <iostream>
    
    using namespace std;
    
    constexpr int N = 1000010;
    
    char s[N];
    int n;
    int m, p, rk[N * 2], oldrk[N], sa[N * 2], id[N], cnt[N];
    
    int main() {
      scanf("%s", s + 1);
      n = strlen(s + 1);
      m = 128;
    
      for (int i = 1; i <= n; i++) cnt[rk[i] = s[i]]++;
      for (int i = 1; i <= m; i++) cnt[i] += cnt[i - 1];
      for (int i = n; i >= 1; i--) sa[cnt[rk[i]]--] = i;
    
      for (int w = 1;; w <<= 1, m = p) {  // m = p 即为值域优化
        int cur = 0;
        for (int i = n - w + 1; i <= n; i++) id[++cur] = i;
        for (int i = 1; i <= n; i++)
          if (sa[i] > w) id[++cur] = sa[i] - w;
    
        memset(cnt, 0, sizeof(cnt));
        for (int i = 1; i <= n; i++) cnt[rk[i]]++;
        for (int i = 1; i <= m; i++) cnt[i] += cnt[i - 1];
        for (int i = n; i >= 1; i--) sa[cnt[rk[id[i]]]--] = id[i];
    
        p = 0;
        memcpy(oldrk, rk, sizeof(oldrk));
        for (int i = 1; i <= n; i++) {
          if (oldrk[sa[i]] == oldrk[sa[i - 1]] &&
              oldrk[sa[i] + w] == oldrk[sa[i - 1] + w])
            rk[sa[i]] = p;
          else
            rk[sa[i]] = ++p;
        }
    
        if (p == n) break;  // p = n 时无需再排序
      }
    
      for (int i = 1; i <= n; i++) printf("%d ", sa[i]);
    
      return 0;
    }
    ```

### O(n) 做法

在一般的题目中，常数较小的倍增求后缀数组是完全够用的，求后缀数组以外的部分也经常有 $O(n\log n)$ 的复杂度，倍增求解后缀数组不会成为瓶颈．

但如果遇到特殊题目、时限较紧的题目，或者是你想追求更短的用时，就需要学习 $O(n)$ 求后缀数组的方法．

#### SA-IS

可以参考 [诱导排序与 SA-IS 算法](https://riteme.site/blog/2016-6-19/sais.html)，另外它的 [评论页面](https://github.com/riteme/riteme.github.io/issues/28) 也有参考价值．

#### DC3

可以参考[\[2009\] 后缀数组——处理字符串的有力工具 by. 罗穗骞][2]．

## 后缀数组的应用

### 寻找最小的循环移动位置

将字符串 $S$ 复制一份变成 $SS$ 就转化成了后缀排序问题．

例题：[「JSOI2007」字符加密](https://www.luogu.com.cn/problem/P4051)．

### 在字符串中找子串

任务是在线地在主串 $T$ 中寻找模式串 $S$．在线的意思是，我们已经预先知道主串 $T$，但是当且仅当询问时才知道模式串 $S$．我们可以先构造出 $T$ 的后缀数组，然后查找子串 $S$．若子串 $S$ 在 $T$ 中出现，它必定是 $T$ 的一些后缀的前缀．因为我们已经将所有后缀排序了，我们可以通过在 $p$ 数组中二分 $S$ 来实现．比较子串 $S$ 和当前后缀的时间复杂度为 $O(|S|)$，因此找子串的时间复杂度为 $O(|S|\log |T|)$．注意，如果该子串在 $T$ 中出现了多次，每次出现都是在 $p$ 数组中相邻的．因此出现次数可以通过再次二分找到，输出每次出现的位置也很轻松．

### 从字符串首尾取字符最小化字典序

例题：[「USACO07DEC」Best Cow Line](https://www.luogu.com.cn/problem/P2870)．

题意：给你一个字符串，每次从首或尾取一个字符组成字符串，问所有能够组成的字符串中字典序最小的一个．

??? note "题解"
    暴力做法就是每次最坏 $O(n)$ 地判断当前应该取首还是尾（即比较取首得到的字符串与取尾得到的反串的大小），只需优化这一判断过程即可．
    
    由于需要在原串后缀与反串后缀构成的集合内比较大小，可以将反串拼接在原串后，并在中间加上一个没出现过的字符（如 `#`，代码中可以直接使用空字符），求后缀数组，即可 $O(1)$ 完成这一判断．

??? note "参考代码"
    ```cpp
    --8<-- "docs/string/code/sa/sa_1.cpp"
    ```

## height 数组

### LCP（最长公共前缀）

两个字符串 $S$ 和 $T$ 的 LCP 就是最大的 $x$($x\le \min(|S|, |T|)$) 使得 $S_i=T_i\ (\forall\ 1\le i\le x)$．

下文中以 $lcp(i,j)$ 表示后缀 $i$ 和后缀 $j$ 的最长公共前缀（的长度）．

### height 数组的定义

$height[i]=lcp(sa[i],sa[i-1])$，即第 $i$ 名的后缀与它前一名的后缀的最长公共前缀．

$height[1]$ 可以视作 $0$．

### O(n) 求 height 数组需要的一个引理

$height[rk[i]]\ge height[rk[i-1]]-1$

???+ note "证明"
    当 $height[rk[i-1]]\le1$ 时，上式显然成立（右边小于等于 $0$）．
    
    当 $height[rk[i-1]]>1$ 时：
    
    根据 $height$ 定义，有 $lcp(sa[rk[i-1]], sa[rk[i-1]-1]) = height[rk[i-1]] > 1$．
    
    既然后缀 $i-1$ 和后缀 $sa[rk[i-1]-1]$ 有长度为 $height[rk[i-1]]$ 的最长公共前缀，
    
    那么不妨用 $aA$ 来表示这个最长公共前缀．（其中 $a$ 是一个字符，$A$ 是长度为 $height[rk[i-1]]-1$ 的字符串，非空）
    
    那么后缀 $i-1$ 可以表示为 $aAD$，后缀 $sa[rk[i-1]-1]$ 可以表示为 $aAB$．（$B < D$，$B$ 可能为空串，$D$ 非空）
    
    进一步地，后缀 $i$ 可以表示为 $AD$，存在后缀（$sa[rk[i-1]-1]+1$）$AB$．
    
    因为后缀 $sa[rk[i]-1]$ 在大小关系的排名上仅比后缀 $sa[rk[i]]$ 也就是后缀 $i$，小一位，而 $AB < AD$．
    
    所以 $AB \leqslant$ 后缀 $sa[rk[i]-1] < AD$，显然后缀 $i$ 和后缀 $sa[rk[i]-1]$ 有公共前缀 $A$．
    
    于是就可以得出 $lcp(i,sa[rk[i]-1])$ 至少是 $height[rk[i-1]]-1$，也即 $height[rk[i]]\ge height[rk[i-1]]-1$．

### O(n) 求 height 数组的代码实现

利用上面这个引理暴力求即可：

```cpp
for (i = 1, k = 0; i <= n; ++i) {
  if (rk[i] == 0) continue;
  if (k) --k;
  while (s[i + k] == s[sa[rk[i] - 1] + k]) ++k;
  height[rk[i]] = k;
}
```

$k$ 不会超过 $n$，最多减 $n$ 次，所以最多加 $2n$ 次，总复杂度就是 $O(n)$．

## height 数组的应用

### 两子串最长公共前缀

$lcp(sa[i],sa[j])=\min\{height[i+1..j]\}$

感性理解：如果 $height$ 一直大于某个数，前这么多位就一直没变过；反之，由于后缀已经排好序了，不可能变了之后变回来．

严格证明可以参考[\[2004\] 后缀数组 by. 许智磊][1]．

有了这个定理，求两子串最长公共前缀就转化为了 [RMQ 问题](../topic/rmq.md)．

### 比较一个字符串的两个子串的大小关系

假设需要比较的是 $A=S[a..b]$ 和 $B=S[c..d]$ 的大小关系．

若 $lcp(a, c)\ge\min(|A|, |B|)$，$A<B\iff |A|<|B|$．

否则，$A<B\iff rk[a]< rk[c]$．

### 不同子串的数目

子串就是后缀的前缀，所以可以枚举每个后缀，计算前缀总数，再减掉重复．

「前缀总数」其实就是子串个数，为 $n(n+1)/2$．

如果按后缀排序的顺序枚举后缀，每次新增的子串就是除了与上一个后缀的 LCP 剩下的前缀．这些前缀一定是新增的，否则会破坏 $lcp(sa[i],sa[j])=\min\{height[i+1..j]\}$ 的性质．只有这些前缀是新增的，因为 LCP 部分在枚举上一个前缀时计算过了．

所以答案为：

$\frac{n(n+1)}{2}-\sum\limits_{i=2}^nheight[i]$

### 出现至少 k 次的子串的最大长度

例题：[「USACO06DEC」Milk Patterns](https://www.luogu.com.cn/problem/P2852)．

??? note "题解"
    出现至少 $k$ 次意味着后缀排序后有至少连续 $k$ 个后缀以这个子串作为公共前缀．
    
    所以，求出每相邻 $k-1$ 个 $height$ 的最小值，再求这些最小值的最大值就是答案．
    
    可以使用单调队列 $O(n)$ 解决，但使用其它方式也足以 AC．

??? note "参考代码"
    ```cpp
    --8<-- "docs/string/code/sa/sa_2.cpp"
    ```

### 是否有某字符串在文本串中至少不重叠地出现了两次

可以二分目标串的长度 $|s|$，将 $h$ 数组划分成若干个连续 LCP 大于等于 $|s|$ 的段，利用 RMQ 对每个段求其中出现的数中最大和最小的下标，若这两个下标的距离满足条件，则一定有长度为 $|s|$ 的字符串不重叠地出现了两次．

### 连续的若干个相同子串

我们可以枚举连续串的长度 $|s|$，按照 $|s|$ 对整个串进行分块，对相邻两块的块首进行 LCP 与 LCS 查询，具体可见[\[2009\] 后缀数组——处理字符串的有力工具][2]．

例题：[「NOI2016」优秀的拆分](https://loj.ac/p/2083)．

### 结合并查集

某些题目求解时要求你将后缀数组划分成若干个连续 LCP 长度大于等于某一值的段，亦即将 $h$ 数组划分成若干个连续最小值大于等于某一值的段并统计每一段的答案．如果有多次询问，我们可以将询问离线．观察到当给定值单调递减的时候，满足条件的区间个数总是越来越少，而新区间都是两个或多个原区间相连所得，且新区间中不包含在原区间内的部分的 $h$ 值都为减少到的这个值．我们只需要维护一个并查集，每次合并相邻的两个区间，并维护统计信息即可．

经典题目：[「NOI2015」品酒大会](https://uoj.ac/problem/131)

### 结合线段树

某些题目让你求满足条件的前若干个数，而这些数又在后缀排序中的一个区间内．这时我们可以用归并排序的性质来合并两个结点的信息，利用线段树维护和查询区间答案．

### 结合单调栈

例题：[「AHOI2013」差异](https://loj.ac/problem/2377)

??? note "题解"
    被加数的前两项很好处理，为 $n(n-1)(n+1)/2$（每个后缀都出现了 $n-1$ 次，后缀总长是 $n(n+1)/2$），关键是最后一项，即后缀的两两 LCP．
    
    我们知道 $lcp(i,j)=k$ 等价于 $\min\{height[i+1..j]\}=k$．所以，可以把 $lcp(i,j)$ 记作 $\min\{x|i+1\le x\le j, height[x]=lcp(i,j)\}$ 对答案的贡献．
    
    考虑每个位置对答案的贡献是哪些后缀的 LCP，其实就是从它开始向左若干个连续的 $height$ 大于它的后缀中选一个，再从向右若干个连续的 $height$ 不小于它的后缀中选一个．这个东西可以用 [单调栈](../ds/monotonic-stack.md) 计算．
    
    单调栈部分类似于 [Luogu P2659 美丽的序列](https://www.luogu.com.cn/problem/P2659) 以及 [悬线法](../misc/hoverline.md)．

??? note "参考代码"
    ```cpp
    --8<-- "docs/string/code/sa/sa_3.cpp"
    ```

类似的题目：[「HAOI2016」找相同字符](https://loj.ac/problem/2064)．

## 习题

-   [UVa 760 - DNA Sequencing](http://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&category=24&page=show_problem&problem=701)
-   [UVa 1223 - Editor](http://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&category=24&page=show_problem&problem=3664)
-   [Codechef - Tandem](https://www.codechef.com/problems/TANDEM)
-   [Codechef - Substrings and Repetitions](https://www.codechef.com/problems/ANUSAR)
-   [Codechef - Entangled Strings](https://www.codechef.com/problems/TANGLED)
-   [Codeforces - Martian Strings](http://codeforces.com/problemset/problem/149/E)
-   [Codeforces - Little Elephant and Strings](http://codeforces.com/problemset/problem/204/E)
-   [SPOJ - Ada and Terramorphing](http://www.spoj.com/problems/ADAPHOTO/)
-   [SPOJ - Ada and Substring](http://www.spoj.com/problems/ADASTRNG/)
-   [UVa - 1227 - The longest constant gene](https://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=3668)
-   [SPOJ - Longest Common Substring](http://www.spoj.com/problems/LCS/en/)
-   [UVa 11512 - GATTACA](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=2507)
-   [QOJ 11240 - Suffixes and Palindromes](https://qoj.ac/problem/11240)
-   [GYM - Por Costel and the Censorship Committee](http://codeforces.com/gym/100923/problem/D)
-   [UVa 1254 - Top 10](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=3695)
-   [UVa 12191 - File Recover](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=3343)
-   [UVa 12206 - Stammering Aliens](https://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=3358)
-   [Codechef - Jarvis and LCP](https://www.codechef.com/problems/INSQ16F)
-   [洛谷 P8617 - 重复模式](https://www.luogu.com.cn/problem/P8617)
-   [UVa 11107 - Life Forms](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=2048)
-   [UVa 12974 - Exquisite Strings](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&category=862&page=show_problem&problem=4853)
-   [UVa 10526 - Intellectual Property](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=1467)
-   [UVa 12338 - Anti-Rhyme Pairs](https://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=3760)
-   [DevSkills Reconstructing Blue Print of Life](https://devskill.com/CodingProblems/ViewProblem/328)
-   [UVa 12191 - File Recover](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=3343)
-   [SPOJ - Suffix Array](http://www.spoj.com/problems/SARRAY/)
-   [Gym 102470J - Stammering Aliens](https://codeforces.com/gym/102470/problem/J)
-   [SPOJ - LCS2](http://www.spoj.com/problems/LCS2/)
-   [Codeforces - Fake News (hard)](http://codeforces.com/contest/802/problem/I)
-   [SPOJ - Longest Commong Substring](http://www.spoj.com/problems/LONGCS/)
-   [SPOJ - Lexicographical Substring Search](http://www.spoj.com/problems/SUBLEX/)
-   [Codeforces - Forbidden Indices](http://codeforces.com/contest/873/problem/F)
-   [Codeforces - Tricky and Clever Password](http://codeforces.com/contest/30/problem/E)
-   [Gym 101470B - Circle of digits](https://codeforces.com/gym/101470/problem/B)

## 参考资料

本页面中（[4070a9b](https://github.com/OI-wiki/OI-wiki/pull/950/commits/4070a9b3db8576db16c74d3ec33806ad10476eef) 引入的部分）主要译自博文 [Суффиксный массив](http://e-maxx.ru/algo/suffix_array) 与其英文翻译版 [Suffix Array](https://cp-algorithms.com/string/suffix-array.html)．其中俄文版版权协议为 Public Domain + Leave a Link；英文版版权协议为 CC-BY-SA 4.0．

论文：

1.  [\[2004\] 后缀数组 by. 许智磊][1]

2.  [\[2009\] 后缀数组——处理字符串的有力工具 by. 罗穗骞][2]

[1]: https://github.com/OI-wiki/libs/blob/master/%E9%9B%86%E8%AE%AD%E9%98%9F%E5%8E%86%E5%B9%B4%E8%AE%BA%E6%96%87/%E5%9B%BD%E5%AE%B6%E9%9B%86%E8%AE%AD%E9%98%9F2004%E8%AE%BA%E6%96%87%E9%9B%86/%E8%AE%B8%E6%99%BA%E7%A3%8A--%E5%90%8E%E7%BC%80%E6%95%B0%E7%BB%84.pdf "[2004] 后缀数组 by. 许智磊"

[2]: https://github.com/OI-wiki/libs/blob/master/%E9%9B%86%E8%AE%AD%E9%98%9F%E5%8E%86%E5%B9%B4%E8%AE%BA%E6%96%87/%E5%9B%BD%E5%AE%B6%E9%9B%86%E8%AE%AD%E9%98%9F2009%E8%AE%BA%E6%96%87%E9%9B%86/11.%E7%BD%97%E7%A9%97%E9%AA%9E%E3%80%8A%E5%90%8E%E7%BC%80%E6%95%B0%E7%BB%84%E2%80%94%E2%80%94%E5%A4%84%E7%90%86%E5%AD%97%E7%AC%A6%E4%B8%B2%E7%9A%84%E6%9C%89%E5%8A%9B%E5%B7%A5%E5%85%B7%E3%80%8B/%E5%90%8E%E7%BC%80%E6%95%B0%E7%BB%84%E2%80%94%E2%80%94%E5%A4%84%E7%90%86%E5%AD%97%E7%AC%A6%E4%B8%B2%E7%9A%84%E6%9C%89%E5%8A%9B%E5%B7%A5%E5%85%B7.pdf "[2009] 后缀数组——处理字符串的有力工具 by. 罗穗骞"


## string/sam.md

author: GoodCoder666, abc1763613206, ksyx

## 一些记号

-   $\Sigma$：字符集．字符集大小 $|\Sigma| = k$．
-   $s$：字符串．字符串长 $|s| = n$，标号自 $0$ 开始．
-   $t_0$：初始状态．
-   $\operatorname{endpos}(t)$：字符串 $s$ 中子串 $t$ 的结束位置的集合．
-   $\operatorname{link}(v)$：状态 $v$ 的后缀链接．
-   $\operatorname{len}(v)$：状态 $v$ 对应的最长子串的长度．
-   $\operatorname{longest}(v)$：状态 $v$ 对应的最长子串．
-   $\operatorname{minlen}(v)$：状态 $v$ 对应的最短子串的长度．
-   $\operatorname{shortest}(v)$：状态 $v$ 对应的最短子串．

## 后缀自动机概述

**后缀自动机**（suffix automaton, SAM）是一个能解决许多字符串相关问题的有力的数据结构．

举个例子，以下的字符串问题都可以在线性时间内通过 SAM 解决：

-   在另一个字符串中搜索一个字符串的所有出现位置；
-   计算给定的字符串中有多少个不同的子串．

直观上，字符串的 SAM 可以理解为给定字符串的 **所有子串** 的压缩形式．值得注意的事实是，SAM 将所有的这些信息以高度压缩的形式储存．对于一个长度为 $n$ 的字符串，它的空间复杂度仅为 $O(n)$．而且，构造 SAM 的时间复杂度也仅为 $O(n)$．准确地说，一个 SAM 最多有 $2n-1$ 个结点和 $3n-4$ 条转移边．

## 定义

字符串 $s$ 的 SAM 是一个接受 $s$ 的所有后缀的最小 [DFA](../misc/fsm.md#确定性有限状态自动机)．

换句话说：

-   SAM 是一张有向无环图．结点被称作 **状态**，边被称作状态间的 **转移**．
-   图存在一个源点 $t_0$，称作 **初始状态**，其它各结点均可从 $t_0$ 出发到达．
-   每个 **转移** 都标有某个字符．从一个结点出发的所有转移均 **不同**．
-   存在一个或多个 **终止状态**．如果我们从初始状态 $t_0$ 出发，最终转移到了一个终止状态，则路径上的所有转移的标号连接起来一定是字符串 $s$ 的一个后缀．反过来，$s$ 的每个后缀均可用一条从 $t_0$ 到某个终止状态的路径构成．
-   在所有满足上述条件的自动机中，SAM 的结点数是最少的．

SAM 的关键恰在于这个最小性．实际上，直接对字符串 $s$ 的所有后缀建立 [AC 自动机](./ac-automaton.md) 同样可以得到一个接受 $s$ 的所有后缀的 DFA．但是，最差情况下，这样得到的自动机有 $\Theta(n^2)$ 个结点，复杂度难以接受．从下面的例子可以看出，对所有后缀建立 AC 自动机得到的 DFA 中很多结点是重复的，因而可以合并．SAM 正是将结点的合并做到了极致，故而将得到的 DFA 的规模控制在 $O(n)$．从这个意义上，SAM 是字符串的全体后缀的「压缩」的 AC 自动机．

### 子串和路径

SAM 最简单、也最重要的性质是，它包含关于字符串 $s$ 的所有子串的信息．任意从初始状态 $t_0$ 开始的路径，如果我们将路径上的所有转移的标号写下来，都会形成 $s$ 的一个 **子串**．反之，每个 $s$ 的子串都对应从 $t_0$ 开始的某条路径．

为了简化表达，我们称子串 **对应** 这条（从 $t_0$ 出发且它上面所有转移的标号构成这个子串的）路径．反过来，我们说任意一条路径都 **对应** 它的标号构成的字符串．

到达某个状态的路径可能不止一条，因此我们说一个状态对应一些字符串的集合，这个集合中的字符串分别对应着这些路径．

### 简单例子

我们将会在这里展示一些简单的字符串的后缀自动机．

我们用蓝色表示初始状态，用绿色表示终止状态．

对于字符串 $s=\varnothing$：

![](./images/SAM/SA.svg)

对于字符串 $s=\texttt{a}$：

![](./images/SAM/SAa.svg)

对于字符串 $s=\texttt{aa}$：

![](./images/SAM/SAaa.svg)

对于字符串 $s=\texttt{ab}$：

![](./images/SAM/SAab.svg)

对于字符串 $s=\texttt{abb}$：

![](./images/SAM/SAabb.svg)

对于字符串 $s=\texttt{abbb}$：

![](./images/SAM/SAabbb.svg)

在最后这个例子中可以看到，如果直接建立它的所有后缀的 AC 自动机，路径 $\texttt{bbb}$ 和路径 $\texttt{abbb}$ 应当导向不同的结点，但是这两个结点都是终止状态，且无论再添加任何字符，都不会得到更长的匹配串，这说明两个结点在自动机的转移上表现出同样的性质，因而可以合并成同一个结点．这样就得到了如图所示的 SAM．下面的讨论会将合并结点这一想法拓展到所有的情形，并说明，只要合理地合并结点，最后得到的 SAM 只有 $O(n)$ 个结点和转移．

## 线性复杂度的构造算法

在我们描述线性时间内构造 SAM 的算法之前，我们需要引入两个对理解构造过程非常重要的概念，并对其性质进行简单证明．其中，结束位置 $\operatorname{endpos}$ 定义了 SAM 中的结点（亦即指出了结点可以合并的充要条件），而后缀链接 $\operatorname{link}$ 不过是 AC 自动机中的 [失配指针](./ac-automaton.md#失配指针) 在 SAM 中的自然对应．

### 结束位置 `endpos`

考虑字符串 $s$ 的任意非空子串 $t$，我们记 $\operatorname{endpos}(t)$ 为在字符串 $s$ 中 $t$ 的所有结束位置的集合（假设对字符串中字符的编号从零开始）．例如，对于字符串 $\texttt{abcbc}$，我们有 $\operatorname{endpos}(\texttt{bc})=\{2,4\}$．

两个子串 $t_1$ 与 $t_2$ 的结束位置可能完全相同：$\operatorname{endpos}(t_1)=\operatorname{endpos}(t_2)$．这定义了字符串 $s$ 的子串之间的等价关系．字符串 $s$ 的所有非空子串可以根据它们的结束位置集合 $\operatorname{endpos}$ 分为若干 **等价类**．

一个事实是，每个这样的等价类都对应 SAM 的一个状态[^state-endpos]．也就是说，只要两个子串的结束位置相同，它们在 SAM 中的路径就对应着同一个状态．换句话说，SAM 中的每个非初始状态都对应一个或多个 $\operatorname{endpos}$ 相同的非空子串．总之，SAM 中的状态就是所有非空子串的等价类，再加上初始状态．

暂且接受这个事实，我们将基于它介绍构造 SAM 的算法．我们还将说明，SAM 需要满足的所有性质，除了最小性以外都满足了；而最小性可以由 [Myhill–Nerode 定理](../misc/fsm.md#myhillnerode-定理) 得出．

由 $\operatorname{endpos}$ 的值我们可以得到一些重要结论，它们解释了同一个状态对应的不同的子串之间的关系．

???+ note "引理 1"
    字符串 $s$ 的两个非空子串 $u$ 和 $w$（假设 $\left|u\right|\le \left|w\right|$）的 $\operatorname{endpos}$ 相同，当且仅当字符串 $u$ 在 $s$ 中每次出现时，都是以 $w$ 后缀的形式存在的．

??? note "证明"
    引理显然成立．如果 $u$ 和 $w$ 的 $\operatorname{endpos}$ 相同，则 $u$ 是 $w$ 的一个后缀，且在 $s$ 中只以 $w$ 的后缀的形式出现．反过来，根据定义，如果 $u$ 为 $w$ 的一个后缀，且只以 $w$ 的后缀的形式在 $s$ 中出现，那么两个子串的 $\operatorname{endpos}$ 相同．

???+ note "引理 2"
    考虑两个非空子串 $u$ 和 $w$（假设 $\left|u\right|\le \left|w\right|$）．那么，要么 $\operatorname{endpos}(u)\cap \operatorname{endpos}(w)=\varnothing$，要么 $\operatorname{endpos}(w)\subseteq \operatorname{endpos}(u)$，取决于 $u$ 是否为 $w$ 的一个后缀：
    
    $$
    \begin{cases}
    \operatorname{endpos}(w) \subseteq \operatorname{endpos}(u), & \text{if } u \text{ is a suffix of } w, \\
    \operatorname{endpos}(w) \cap \operatorname{endpos}(u) = \varnothing, & \text{otherwise}.
    \end{cases}
    $$

??? note "证明"
    如果集合 $\operatorname{endpos}(u)$ 与 $\operatorname{endpos}(w)$ 有至少一个公共元素，那么由于字符串 $u$ 与 $w$ 在相同位置结束，$u$ 是 $w$ 的一个后缀．所以在每次 $w$ 出现的位置，子串 $u$ 也会出现．所以 $\operatorname{endpos}(w)\subseteq \operatorname{endpos}(u)$．

???+ note "引理 3"
    考虑一个 $\operatorname{endpos}$ 相同的子串等价类，将类中的所有子串按长度非递增的顺序排序．那么，每个子串都不会比它前一个子串长，与此同时每个子串也是它前一个子串的后缀．换句话说，对于同一等价类的任意两子串，较短者为较长者的后缀，且该等价类中的子串长度是连续的，取遍某个区间内的所有整数值．

??? note "证明"
    如果等价类中只包含一个子串，引理显然成立．现在我们来讨论子串元素个数大于 $1$ 的等价类．
    
    由引理 1，$\operatorname{endpos}$ 相同的两个不同字符串中，必定一长一短，且较短者总是较长者的真后缀．也就是说，等价类中没有等长的字符串．
    
    记 $w$ 为等价类中最长的字符串，$u$ 为等价类中最短的字符串．由引理 1，字符串 $u$ 是字符串 $w$ 的真后缀．现在考虑长度在区间 $[\left|u\right|,\left|w\right|]$ 中的 $w$ 的任意后缀．容易看出，这个后缀也在同一等价类中，因为这个后缀只能在字符串 $s$ 中以 $w$ 的一个后缀的形式存在（这是因为较短的后缀 $u$ 在 $s$ 中只以 $w$ 的后缀的形式存在）．因此，由引理 1，这个后缀和字符串 $w$ 的 $\operatorname{endpos}$ 相同．

一句话概括，同一个状态对应的子串的长度各不相同，而且是连续的若干自然数，其中较短的总是较长的子串的后缀．

### 后缀链接 `link`

考虑 SAM 中某个状态 $v\neq t_0$．我们已经知道，状态 $v$ 对应于具有相同 $\operatorname{endpos}$ 的子串等价类．我们如果定义 $w$ 为这些字符串中最长的一个，则所有其它的字符串都是 $w$ 的后缀．

我们还知道字符串 $w$ 的前几个后缀（按长度降序考虑）全部属于这个等价类，且其它后缀（至少有一个——空后缀）在别的等价类中．我们记 $t$ 为其它后缀中最长的，然后将 $v$ 的后缀链接连到 $t$ 所属等价类对应的状态上．

换句话说，$v$ 的 **后缀链接** $\operatorname{link}(v)$ 连接到的状态，对应于 $w$ 的后缀中与它的 $\operatorname{endpos}$ 集合不同且最长的那个，也是 $w$ 的后缀中在 $s$ 中的出现次数比 $w$ 更多且最长的那个．

为方便讨论，我们规定初始状态 $t_0$ 对应的等价类，只包含一个空字符串，而且 $\operatorname{endpos}(t_0)=\{-1,0,\ldots,\left|S\right|-1\}$．

???+ note "引理 4"
    所有后缀链接构成一棵根节点为 $t_0$ 的树．

??? note "证明"
    考虑任意状态 $v\neq t_0$，后缀链接 $\operatorname{link}(v)$ 连接到的状态对应于严格更短的字符串（后缀链接的定义、引理 3）．因此，沿后缀链接移动，我们总是能到达对应空串的初始状态 $t_0$．

???+ note "引理 5"
    以 $\operatorname{endpos}$ 集合为结点、集合的包含关系作为边，这样构造的树（即每个子节点的 $\operatorname{endpos}$ 集合都包含在父节点的 $\operatorname{endpos}$ 集合中）与通过后缀链接 $\operatorname{link}$ 构造的树相同．

??? note "证明"
    由引理 2，任意一个 SAM 的 $\operatorname{endpos}$ 集合形成了一棵树（因为两个集合要么完全没有交集要么其中一个是另一个的子集）．
    
    我们现在考虑任意状态 $v\neq t_0$ 及后缀链接 $\operatorname{link}(v)$，由后缀链接和引理 2，我们可以得到
    
    $$
    \operatorname{endpos}(v)\subsetneq \operatorname{endpos}(\operatorname{link}(v)).
    $$
    
    注意这里应该是 $\subsetneq$ 而不是 $\subseteq$，因为若 $\operatorname{endpos}(v)=\operatorname{endpos}(\operatorname{link}(v))$，那么 $v$ 和 $\operatorname{link}(v)$ 应该被合并为一个结点．

结合前面的引理有：后缀链接构成的树本质上是 $\operatorname{endpos}$ 集合构成的一棵树．

以下是对字符串 $\texttt{abcbc}$ 构造 SAM 时产生的后缀链接树的一个 **例子**，结点被标记为对应等价类中最长的子串．

![](./images/SAM/SA_suffix_links.svg)

结合图示，如果能够形成一些对于后缀自动机的认识，将对下文理解其构造算法和应用都有所帮助．

???+ example "对图示的解释"
    -   SAM 上存在一条最长的路径，其标号恰好为字符串 $\texttt{abcbc}$ 本身．该路径从初始状态开始，经过的每个状态都对应着字符串 $\texttt{abcbc}$ 的前缀（$\varnothing,\texttt{a},\texttt{ab},\texttt{abc},\texttt{abcb},\texttt{abcbc}$）．这些状态在后续 [应用](#后缀链接树) 中至关重要．
    -   后缀链接树可以看做是将这些「前缀状态」沿着后缀链接移动到根节点（即初始状态）的路径「压缩」得到．
    
        -   沿着每条路径，结点对应的字符串集合构成了相应的前缀的所有后缀的分划．例如，标记为 $\texttt{abcbc}$ 的状态沿着后缀链接移动到根节点的路径为 $\texttt{abcbc}\rightarrow\texttt{bc}\rightarrow\varnothing$．其中，结点 $\texttt{abcbc}$ 实际对应着字符串集合 $\{\texttt{abcbc},\texttt{bcbc},\texttt{cbc}\}$，结点 $\texttt{bc}$ 实际对应着字符串集合 $\{\texttt{bc},\texttt{c}\}$，结点 $\varnothing$ 就对应空字符串．
        -   不同的路径可能共用同一个结点，这就是为什么会有「压缩」．例如，路径 $\texttt{abc}\rightarrow\texttt{bc}\rightarrow\varnothing$ 和路径 $\texttt{abcbc}\rightarrow\texttt{bc}\rightarrow\varnothing$ 共用了结点 $\texttt{bc}$．这是因为 $\operatorname{endpos}(\texttt{bc})=\{2,4\}$，而结束在位置 $2$ 的字符串 $\texttt{bc}$ 前紧接着字符 $\texttt{a}$ 而结束在位置 $4$ 的字符串 $\texttt{bc}$ 前紧接着字符 $\texttt{c}$，因此，当在前方添加字符（即逆着后缀链接移动）时，结束位置集合（即状态）会分裂．
        -   后缀链接树只需要将这些后缀路径合理地「压缩」在一起即可，而不需要考虑别的结点．这是因为，所有子串都是某个前缀的后缀，故而必然出现在某个这样的路径中．后文的构造算法本质上就是逐个添加字符，并为每个新增加的前缀，构造这样一条后缀路径，并使其合理地「压缩」到之前已有的路径中（即不重复构造已经存在的状态和转移）．
        -   终止状态恰为字符串 $\texttt{abcbc}$ 本身所在的后缀路径上的所有结点．
    -   到达同一个状态的转移必然具有相同的标号，而且这些转移的起点一定是位于后缀链接树上的某条（连续的）路径．比如，转移到状态 $\texttt{abcb}$ 的状态就有两个：$\texttt{abc}$ 和 $\texttt{bc}$．它们位于后缀树上的路径 $\texttt{abc}\rightarrow\texttt{bc}$ 上．注意，它们分别对应于字符串集合 $\{\texttt{abc}\}$ 和 $\{\texttt{bc},\texttt{c}\}$，这些字符串在后面添加字符 $\texttt{b}$，就得到状态 $\texttt{abcb}$ 对应的字符串集合 $\{\texttt{abcb},\texttt{bcb},\texttt{cb}\}$．
    
        -   添加字符后，不同状态可能转移到同一个状态，是因为新添加的字符使得结束位置的增加更为困难．
    -   后缀链接树上，每个结点的 $\operatorname{endpos}$ 集合都是其子节点的 $\operatorname{endpos}$ 集合的并集，至多再增加一个位置．而且，这个新位置存在，当且仅当该结点恰好对应着结束在该位置的原字符串的前缀．因为图示中，后缀链接树的非根非叶的结点都不对应着字符串 $\texttt{abcbc}$ 的前缀，所以不存在这种情形．

后缀自动机中存储着字符串全部子串的信息．这件事可以通过两个角度理解：

-   SAM 本身可以看作是字符串全体后缀的 AC 自动机的压缩版本．因此，它存储了字符串的全体后缀的所有前缀的信息，这就相当于存储了字符串全体子串的信息．
-   SAM 的后缀链接树可以看做是字符串全体前缀的后缀路径的压缩版本．因此，它存储了字符串的全体前缀的所有后缀的信息，这也相当于存储了字符串全体子串的信息．

这两种思考的角度在处理不同问题时都是有用的．

### 小结

在进一步讨论算法本身前，我们总结一下之前的内容，并引入一些辅助记号．

-   $s$ 的子串可以根据它们的结束位置集合 $\operatorname{endpos}$ 划分为多个等价类；

-   SAM 由初始状态 $t_0$ 和与每一个（非空子串的）$\operatorname{endpos}$ 等价类对应的每个状态组成；

-   每一个状态 $v$ 都匹配一个或多个子串．我们记 $\operatorname{longest}(v)$ 为其中最长的一个字符串，记 $\operatorname{len}(v)$ 为它的长度．类似地，记 $\operatorname{shortest}(v)$ 为最短的子串，它的长度为 $\operatorname{minlen}(v)$．那么对应这个状态的所有字符串都是字符串 $\operatorname{longest}(v)$ 的不同的后缀，且所有字符串的长度恰好取遍区间 $[\operatorname{minlen}(v),\operatorname{len}(v)]$ 中的每一个整数．

-   对于任意状态 $v\neq t_0$，定义后缀链接为连接到对应字符串 $\operatorname{longest}(v)$ 的长度为 $\operatorname{minlen}(v)-1$ 的后缀的一条边．从根节点 $t_0$ 出发的后缀链接可以形成一棵树．这棵树也表示 $\operatorname{endpos}$ 集合间的包含关系．

-   对于任意状态 $v\neq t_0$，可用后缀链接 $\operatorname{link}(v)$ 表达 $\operatorname{minlen}(v)$：

    $$
    \operatorname{minlen}(v)=\operatorname{len}(\operatorname{link}(v))+1.
    $$

-   如果我们从任意状态 $v_0$ 开始顺着后缀链接遍历，总会到达初始状态 $t_0$．这种情况下我们可以得到一个互不相交的区间 $[\operatorname{minlen}(v_i),\operatorname{len}(v_i)]$ 的序列，且它们的并集形成了连续的区间 $[0,\operatorname{len}(v_0)]$．

### 算法

现在我们可以讨论构造 SAM 的算法了．这个算法是 **在线** 算法，我们可以逐个加入字符串中的每个字符，并且在每一步中对应地维护 SAM．

在讨论详细的实现之前，首先通过图示初步感受一下增加新字符 $c$ 时，SAM 可能发生的变化．

???+ note "简单理解增量构造过程"
    在字符串 $s$ 的 SAM 的基础上，可以构造字符串 $s+c$ 的 SAM．根据前文对图示的解释，只需要构造出新增加的前缀（即 $s+c$）的后缀路径，并压缩到现有的路径上即可．而且，根据前文的描述，新的后缀路径上的结点必然都可以通过原字符串 $s$ 的后缀路径上的结点经由字符 $c$ 转移而来．
    
    我们首先考虑在添加新字符 $c$ 之前，原来的字符串 $s$ 的后缀路径可能具有什么形式，而且会怎样经由字符 $c$ 转移．最一般的情形，如下图示：
    
    ![](./images/SAM/sam-suffix-path-1.svg)
    
    图中，原字符串 $s$ 的后缀路径为 $p_0\rightarrow p_1\rightarrow\cdots\rightarrow p_6\rightarrow t_0$，后缀链接由红色箭头表示．其中部分结点（即 $p_2\sim p_6$）已经存在经由字符 $c$ 的转移；因为将连续的后缀串添加同一个字符会同样得到连续的后缀，所以这些转移的终点组成另一串后缀路径 $q_1\rightarrow q_2\rightarrow q_3\rightarrow t_0$．此时，有两点观察：
    
    -   原字符串 $s$ 的后缀路径上，没有经由 $c$ 的转移的结点一定是最初的几个结点．只要从某个结点（图中的 $p_2$）开始，存在经由 $c$ 的转移，后续经过的结点也一定存在经由 $c$ 的转移．
    
        **解释**：设 $s_2=\operatorname{longest}(p_2)$，那么后续经过的所有结点都对应 $s_2$ 的后缀，因而如果 $s_2+c$ 也出现在 $s$ 中，那么 $s_2$ 的后缀再加 $c$ 的结果也一定出现在 $s$ 中，因此这些结点都有经由 $c$ 的转移．
    -   虽然经由字符 $c$ 能够到达结点 $q_i$ 的结点一定是后缀链接树上的连续段，但是这个连续段未必全体都位于自 $p_0$ 到根的后缀路径上．特别地，只有第一个结点 $q_1$ 对应的连续段中起始的若干个结点 **可能** 不在这个后缀路径上．例如图中的结点 $q_1$ 就对应结点 $p_1'\rightarrow p_2\rightarrow p_3$，其中，$p_1'$ 不在 $p_0$ 的后缀路径上．
    
        **解释**：设 $s_2=\operatorname{longest}(p_2)$，则 $s_2+c$ 对应着 $q_1$，但是图中显然有 $s_2+c\neq\operatorname{longest}(q_1)$，因为后者是 $\operatorname{longest}(p'_1)+c$．这就说明，$q_1$ 对应的部分字符串不能由 $s_2$ 及其后缀转移来．反过来，$q_2$ 中的字符串必然是 $s_2+c$ 的后缀，因此删去末尾的 $c$ 后必然是 $s_2$ 的后缀．也就是说，经由 $c$ 转移到 $q_2$ 的结点必然在 $p_2$ 起始的后缀路径上．这也是为什么只有起始的 $q_1$ 对应的连续段中的部分结点可能不在 $p_0$ 的后缀路径上．
    
    对于这个图示，如果要在原字符串 $s$ 的末尾添加一个字符 $c$，并构造出相应的后缀路径，会发生什么变化呢？答案是如下图所示：
    
    ![](./images/SAM/sam-suffix-path-2.svg)
    
    因为结点 $q_0$ 由原字符串 $s$ 对应结点 $p_0$ 经由字符 $c$ 转移而来，它就对应新字符串 $s+c$．所以，它的后缀路径 $q_0\rightarrow q_1''\rightarrow q_2\rightarrow q_3\rightarrow t_0$ 就是新增的后缀路径．如果原来的后缀路径上的结点 $p_i$ 本就有经由 $c$ 的转移，那么新的后缀路径也必然会经过这些转移到达的结点，因此可以直接复用旧有的结点．新的后缀路径上有且只有一个完全新建的节点 $q_0$，用于接受原来的后缀路径上起始的那些没有经由 $c$ 的转移的结点的转移．
    
    除了这些显然的事实外，还可以注意到，原来的结点 $q_1$ 也经过了一次复制，或者说是分裂成了两个结点 $q'_1\rightarrow q_1''$．这是因为新增的后缀路径只是与现有路径部分重合：原来的结点 $q_1$ 对应的字符串中，只有较短的那些（即结点 $p_2$ 和 $p_3$ 能够转移到的那些）才会出现在新增的后缀路径上，而较长的那些（即结点 $p_1'$ 能够转移到的那些）并不会出现在新增的后缀路径上，因此新增的后缀路径只能经过结点 $q_1$ 的一部分，后者只能分裂成两个结点用于表示这种情形．同样的道理，前面已经解释过，$q_1$ 之后的结点 $q_2$ 和 $q_3$ 都无法由不在 $p_0$ 的后缀路径上的结点转移，因此这些结点对应的所有字符串都会出现在新增的后缀路径上，也就不需要分裂了．
    
    从 SAM 中状态代表的含义看，每个状态都是一个 $\operatorname{endpos}$ 集合．设延长字符串时，新增的结束位置为 $i$，那么新增的结点 $q_0$ 就是结束位置集合 $\{i\}$，而分裂的结点 $q_1'$ 和 $q_1''$ 分别对应集合 $\operatorname{endpos}(q_1)$ 和 $\operatorname{endpos}(q_1)\cup\{i\}$，之后的结点 $q_2$ 和 $q_3$ 其实都在原有的结束位置集合上新增了 $i$．也就是说，虽然 $q_2$ 和 $q_3$ 及其相关的转移没有发生变化，但是它们对应的 $\operatorname{endpos}$ 集合的确扩大了．
    
    以上说明的是最复杂、最一般的情形（即下文的 **情形三**）．实际操作时，可能并不存在结点 $p'_1$，因而也就不需要分裂（即下文的 **情形二**）．要判断这种情形，只需要判断 $\operatorname{longest}(q_1)=\operatorname{longest}(p_2)+c$ 即可，亦即 $\operatorname{len}(q_1)=\operatorname{len}(p_2)+1$．也有可能 $p_0$ 的后缀路径上的所有结点都没有经由 $c$ 的转移，此时，只要新建 $q_0$ 就好了（即下文的 **情形一**）．

掌握了新增后缀路径的思想后，现在讨论增量构造的具体步骤．

#### 过程

为了保证线性的空间复杂度，我们将只保存 $\operatorname{len}$ 和 $\operatorname{link}$ 的值和每个状态的转移列表，我们不会标记终止状态（但是我们稍后会展示在构造 SAM 后如何分配这些标记）．

一开始 SAM 只包含一个状态 $t_0$，编号为 $0$（其它状态的编号为 $1,2,\ldots$）．为了方便，对于状态 $t_0$ 我们指定 $\operatorname{len}(t_0)=0$，$\operatorname{link}(t_0)=-1$（$-1$ 表示虚拟状态）．

现在，只需要实现给当前字符串添加一个字符 $c$ 的过程．算法流程如下：

???+ note "SAM 增量构造过程"
    -   令 $\textit{last}$ 为添加字符 $c$ 之前，整个字符串对应的状态（一开始我们设 $\textit{last}=0$，算法的最后一步更新 $\textit{last}$）．
    -   创建一个新的状态 $\textit{cur}$，并将 $\operatorname{len}(\textit{cur})$ 赋值为 $\operatorname{len}(\textit{last})+1$，在这时 $\operatorname{link}(\textit{cur})$ 的值还未知．
    -   现在我们进行如下流程：从状态 $\textit{last}$ 开始，如果当前状态还没有标号为字符 $c$ 的转移，我们就添加一个经字符 $c$ 到状态 $\textit{cur}$ 的转移，并将当前状态沿后缀链接移动．如果过程中遇到某个状态已经存在到字符 $c$ 的转移，我们就停下来，并将这个状态标记为 $p$．
    -   **情况一**：如果没有找到这样的状态 $p$，我们就到达了虚拟状态 $-1$，我们将 $\operatorname{link}(\textit{cur})$ 赋值为 $0$ 并退出．
    -   假设现在我们找到了一个状态 $p$，它可以通过字符 $c$ 转移．我们将转移到的状态标记为 $q$．此时，要么 $\operatorname{len}(p)+1=\operatorname{len}(q)$，要么 $\operatorname{len}(p)+1<\operatorname{len}(q)$．
    -   **情况二**：如果 $\operatorname{len}(p)+1=\operatorname{len}(q)$，我们只要将 $\operatorname{link}(\textit{cur})$ 赋值为 $q$ 并退出．
    -   **情况三**：否则就会有些复杂，需要 **复制** 状态 $q$：我们创建一个新的状态 $\textit{clone}$，复制 $q$ 的除了 $\operatorname{len}$ 的值以外的所有信息（后缀链接和转移）．我们将 $\operatorname{len}(\textit{clone})$ 赋值为 $\operatorname{len}(p)+1$．
    
        复制之后，我们将后缀链接从 $\textit{cur}$ 指向 $\textit{clone}$，也从 $q$ 指向 $\textit{clone}$．
    
        最终我们需要沿着后缀链接从状态 $p$ 往回走，只要经过的状态存在指向状态 $q$ 的转移，就将该转移重新连接到状态 $\textit{clone}$．
    -   处理完以上三种情况后，我们都需要将 $\textit{last}$ 的值更新为状态 $\textit{cur}$．

如果我们还想知道哪些状态是 **终止状态** 而哪些不是，我们可以在为字符串 $s$ 构造完完整的 SAM 后找到所有的终止状态．为此，我们从对应整个字符串的状态（存储在变量 $\textit{last}$ 中），遍历它的后缀链接，直到到达初始状态．我们将所有遍历到的状态都标记为终止状态．容易理解这样做我们会准确地标记字符串 $s$ 的所有后缀，这些状态都是终止状态．

因为我们只为 $s$ 的每个字符创建一个或两个新状态，所以 SAM 只包含 **线性个** 状态．而 SAM 只有线性规模的转移个数，以及算法总体的线性运行时间，都还没有说清楚，将在后文说明．

#### 解释

我们详细解释算法每一步的细节，并说明它的 **正确性**．

???+ note "对算法的详细解释"
    -   若一个转移 $(p,q)$ 满足 $\operatorname{len}(p)+1=\operatorname{len}(q)$，则我们称这个转移是 **连续的**．否则，即当 $\operatorname{len}(p)+1<\operatorname{len}(q)$ 时，这个转移被称为 **不连续的**．
    
        从算法描述中可以看出，连续的和不连续的转移，在算法中的处理也并不相同．连续的转移是固定的，我们不会再改变了．与此相反，当向字符串中插入一个新的字符时，不连续的转移可能会改变（转移边的端点可能会改变）．
    -   为了避免引起歧义，我们记向 SAM 中插入当前字符 $c$ 之前的字符串为 $s$．
    -   算法从创建一个新状态 $\textit{cur}$ 开始，对应于整个字符串 $s+c$．我们创建一个新的节点的原因很清楚．与此同时我们也创建了一个新的字符和一个新的等价类．
    -   在创建一个新的状态之后，我们会从对应整个字符串 $s$ 的状态 $\textit{last}$ 沿着后缀链接进行移动．对于经过的每一个状态，我们尝试添加一个通过字符 $c$ 到新状态 $\textit{cur}$ 的转移．
    
        然而我们只能添加与原有转移不冲突的转移．因此我们只要找到已存在的 $c$ 的转移，我们就必须停止．
    -   最简单的情况是我们到达了虚拟状态 $-1$，这意味着我们为所有 $s$ 的后缀添加了 $c$ 的转移．这也意味着，字符 $c$ 从未在字符串 $s$ 中出现过．因此 $\textit{cur}$ 的后缀链接为状态 $0$．
    -   第二种情况下，我们找到了现有的转移 $(p,q)$．这意味着我们尝试向自动机内添加一个 **已经存在的** 字符串 $x+c$（其中 $x$ 为 $s$ 的一个后缀，且字符串 $x+c$ 已经作为 $s$ 的一个子串出现过了）．因为我们假设字符串 $s$ 的自动机的构造是正确的，我们不应该在这里添加一个新的转移．
    
        然而，难点在于，从状态 $\textit{cur}$ 出发的后缀链接应该连接到哪个状态呢？我们要把后缀链接连到一个状态上，且对应的最长的字符串恰好是 $x+c$，即这个状态的 $\operatorname{len}$ 应该是 $\operatorname{len}(p)+1$．然而这样的状态有可能并不存在，即 $\operatorname{len}(q)>\operatorname{len}(p)+1$．这种情况下，我们必须通过拆开状态 $q$ 来创建一个这样的状态．
    -   当然，如果转移 $(p,\,q)$ 是连续的，那么 $\operatorname{len}(q)=\operatorname{len}(p)+1$．在这种情况下一切都很简单．我们只需要将 $\textit{cur}$ 的后缀链接指向状态 $q$．
    -   否则转移是不连续的，即 $\operatorname{len}(q)>\operatorname{len}(p)+1$，这意味着状态 $q$ 不只对应于长度为 $\operatorname{len}(p)+1$ 的后缀 $s+c$，还对应于 $s$ 的更长的子串．除了将状态 $q$ 拆成两个子状态以外我们别无他法，所以第一个子状态的长度就是 $\operatorname{len}(p)+1$ 了．
    
        我们如何拆开一个状态呢？我们 **复制** 状态 $q$，产生一个状态 $\textit{clone}$，我们将 $\operatorname{len}(\textit{clone})$ 赋值为 $\operatorname{len}(p)+1$．由于我们不想改变经过 $q$ 的路径，我们将 $q$ 的所有转移复制到 $\textit{clone}$．我们也将从 $\textit{clone}$ 出发的后缀链接设置为 $q$ 的后缀链接的目标，并设置 $q$ 的后缀链接为 $\textit{clone}$．
    
        在拆开状态后，我们将从 $\textit{cur}$ 出发的后缀链接设置为 $\textit{clone}$．
    
        最后一步我们将一些原本指向 $q$ 的转移重新连接到 $\textit{clone}$．我们需要修改哪些转移呢？只重新连接相当于所有字符串 $w+c$（其中 $w$ 是状态 $p$ 对应的最长字符串）的后缀就够了．也就是说，我们需要继续沿着后缀链接移动，从结点 $p$ 直到虚拟状态 $-1$，或者当前状态经 $c$ 的转移不再指向状态 $q$．

### 线性时间复杂度

我们假设字符集大小为 **常数**，即每次对一个字符搜索转移、添加转移、查找下一个转移这些操作的时间复杂度都为 $O(1)$ 的．如果将每个结点的转移分别存储为一个长度为 $\left|\Sigma\right|$ 的数组（用于快速查询给定标号的转移）和一个动态列表（用于快速遍历所有可用转移），以空间换时间，那么算法的时间复杂度[^time-complexity]为 $O(n)$，空间复杂度为 $O(n\left|\Sigma\right|)$．

??? note "证明"
    如果我们考虑算法的各个部分，算法中有三处时间复杂度不明显是线性的：
    
    -   第一处是遍历所有状态 $\textit{last}$ 的后缀链接，添加字符 $c$ 的转移．
    -   第二处是当状态 $q$ 被复制到一个新的状态 $\textit{clone}$ 时复制转移的过程．
    -   第三处是修改指向 $q$ 的转移，将它们重新连接到 $\textit{clone}$ 的过程．
    
    我们使用 SAM 的大小（状态数和转移数）为 **线性的** 的事实（对状态数是线性的的证明就是算法本身，对转移数为线性的的证明将在稍后实现算法后给出）．
    
    因此上述 **第一处和第二处** 的总复杂度显然为线性的，因为单次操作均摊只为自动机添加了一个新转移．
    
    还需为 **第三处** 估计总复杂度，我们将最初指向 $q$ 的转移重新连接到 $\textit{clone}$．我们记 $v=\operatorname{longest}(p)$，这是字符串 $s$ 的一个后缀．每迭代一次，$v$ 的长度都减小，因而 $v$ 作为 $s$ 的后缀的起始位置必然在后移．因此，循环中 $p$ 沿后缀链接移动的次数，不超过 $v$ 作为 $s$ 的后缀的起始位置向后移动的距离．因为 $p$ 至少要向后移动一次，才能终止循环，而且 $p$ 至少是 $last$ 沿后缀链接移动一次的结果，因此循环终止时，$v$ 作为 $s$ 的后缀的起始位置并不比字符串 $\operatorname{longest}(\operatorname{link}(\operatorname{link}(\textit{last}))$ 更靠前．而且，循环终止时，字符串 $v$ 作为 $s$ 的后缀的起始位置将恰好是 $v+c$ 作为 $s+c$ 的后缀的起始位置，而作为 $s+c$ 的后缀，字符串 $v+c$ 恰好是字符串 $\operatorname{longest}(\operatorname{link}(\operatorname{link}(\textit{cur}))$．因为 $cur$ 是更新后的 $last$ 的值，所以循环中移动的次数不会超过更新前后 $\operatorname{longest}(\operatorname{link}(\operatorname{link}(\textit{last}))$ 作为当前字符串后缀的起始位置向后移动的距离，再加一（即为了终止循环必须移动的次数）．
    
    因为作为当前字符串后缀的字符串 $\operatorname{longest}(\operatorname{link}(\operatorname{link}(\textit{last}))$ 的位置在整个 SAM 构造过程中单调递增[^monotone-loc]，它的总移动距离必然不超过 $n$．这就说明，需要修改指向 $q$ 的转移的循环中，迭代次数不超过 $2n$．这正是我们需要证明的．

当然，如果字符集大小不是常数，SAM 的时间复杂度就不是线性的．从一个结点出发的转移需要存储在支持快速查询和插入的平衡树中．因此如果我们记 $\Sigma$ 为字符集，$\left|\Sigma\right|$ 为字符集大小，则算法的渐近时间复杂度为 $O(n\log\left|\Sigma\right|)$，空间复杂度为 $O(n)$．

### 实现

首先，我们实现一种存储一个转移的全部信息的数据结构．如果需要的话，你可以在这里加入一个终止标记，也可以是一些其它信息．我们将用一个 `map` 存储转移的列表，允许我们在总计 $O(n)$ 的空间复杂度和 $O(n\log\left|\Sigma\right|)$ 的时间复杂度内处理整个字符串．当然，在字符集大小为较小的常数 $K$（比如 26）时，将 `next` 声明为 `int[K]` 更方便．

```cpp
struct state {
  int len, link;
  std::map<char, int> next;
};
```

SAM 本身将会存储在一个 `state` 结构体数组中．我们记录当前自动机的大小 `sz` 和变量 `last`，当前整个字符串对应的状态．

```cpp
constexpr int MAXLEN = 100000;
state st[MAXLEN * 2];
int sz, last;
```

我们定义一个函数来初始化 SAM（创建一个只有初始状态的 SAM）．

```cpp
void sam_init() {
  st[0].len = 0;
  st[0].link = -1;
  sz++;
  last = 0;
}
```

最终我们给出主函数的实现：给当前行末增加一个字符，对应地在之前的基础上建造自动机．

???+ note "实现"
    ```cpp
    void sam_extend(char c) {
      int cur = sz++;
      st[cur].len = st[last].len + 1;
      int p = last;
      while (p != -1 && !st[p].next.count(c)) {
        st[p].next[c] = cur;
        p = st[p].link;
      }
      if (p == -1) {
        st[cur].link = 0;
      } else {
        int q = st[p].next[c];
        if (st[p].len + 1 == st[q].len) {
          st[cur].link = q;
        } else {
          int clone = sz++;
          st[clone].len = st[p].len + 1;
          st[clone].next = st[q].next;
          st[clone].link = st[q].link;
          while (p != -1 && st[p].next[c] == q) {
            st[p].next[c] = clone;
            p = st[p].link;
          }
          st[q].link = st[cur].link = clone;
        }
      }
      last = cur;
    }
    ```

正如之前提到的一样，如果你用内存换时间（空间复杂度为 $O(n\left|\Sigma\right|)$，其中 $\left|\Sigma\right|$ 为字符集大小），你可以在 $O(n)$ 的时间[^time-complexity]内构造字符集大小任意的 SAM．但是这样你需要为每一个状态储存一个大小为 $\left|\Sigma\right|$ 的数组（用于快速根据字符找到相应的转移）以及一个包含所有可用转移的列表（用于快速遍历所有可用的转移）．

## 更多性质

### 状态数

对于一个长度为 $n$ 的字符串 $s$，它的 SAM 中的状态数 **不会超过**  $2n-1$（假设 $n\ge 2$）．

??? note "证明"
    算法本身即可证明该结论．一开始，自动机含有一个状态，第一次和第二次迭代中只会创建一个节点，剩余的 $n-2$ 步中每步会创建至多 $2$ 个状态．
    
    然而我们也能在 **不借助这个算法** 的情况下 **证明** 这个估计值．我们回忆一下状态数等于不同的 $\operatorname{endpos}$ 集合个数．这些 $\operatorname{endpos}$ 集合形成了一棵树（父节点的 $\operatorname{endpos}$ 集合包含子节点的 $\operatorname{endpos}$ 集合）．考虑将这棵树稍微变形一下：只要它有一个只有一个子节点的内部节点（这意味着该子节点的集合至少遗漏了它的父节点的集合中的一个位置），我们就创建一个含有这些遗漏位置的集合作为它的子节点．最后我们可以获得一棵每一个内部结点的度数都大于一的树，且叶子节点的个数不超过 $n$．这样的树里有不超过 $2n-1$ 个节点，因此，原来的不同的 $\operatorname{endpos}$ 集合个数也不超过 $2n-1$．
    
    字符串 $\texttt{abbb} \cdots \texttt{bbb}$ 的状态数达到了该上界：从第三次迭代后的每次迭代，算法都会拆开一个状态，最终产生恰好 $2n-1$ 个状态．

### 转移数

对于一个长度为 $n$ 的字符串 $s$，它的 SAM 中的转移数 **不会超过**  $3n-4$（假设 $n\ge 3$）．

??? note "证明"
    我们首先估计连续的转移的数量．考虑自动机中由从状态 $t_0$ 开始到达所有状态的最长路径组成的生成树．生成树只包含连续的边，因此数量少于状态数，即边数不会超过 $2n-2$．
    
    现在我们来估计不连续的转移的数量．令当前不连续转移为 $(p,\,q)$，其字符为 $c$．我们取它的对应字符串 $u+c+w$，其中字符串 $u$ 对应于初始状态到 $p$ 的最长路径，$w$ 对应于从 $q$ 到任意终止状态的最长路径．一方面，每个不完整的字符串所对应的形如 $u+c+w$ 的字符串是不同的（因为字符串 $u$ 和 $w$ 仅由完整的转移组成）．另一方面，由终止状态的定义，每个形如 $u+c+w$ 的字符串都是整个字符串 $s$ 的后缀．因为 $s$ 只有 $n$ 个非空后缀，且形如 $u+c+w$ 的字符串都不包含 $s$（因为整个字符串只包含完整的转移），所以非完整的转移的总数不会超过 $n-1$．
    
    将以上两个估计值相加，我们可以得到上界 $3n-3$．然而，最大的状态数只能在类似于 $\texttt{abbb} \cdots \texttt{bbb}$ 的情况中产生，而此时转移数量显然少于 $3n-3$．
    
    因此我们可以获得更为紧确的 SAM 的转移数的上界：$3n-4$．字符串 $\texttt{abbb} \cdots \texttt{bbbc}$ 就达到了这个上界．

### 后缀链接树

尽管构造 SAM 是为了得到它的状态和转移的信息，但是构造过程中记录的后缀链接 $\operatorname{link}$ 和该状态对应的最长子串长度 $\operatorname{len}$ 在应用中常常比 SAM 的转移更为重要，甚至可以抛开转移单独使用．

在构建 SAM 的过程中，需要更新 $\textit{last}$ 状态的值．它对应的是每次添加字符前（后）的字符串，也就是整个字符串 $s$ 的所有前缀．将第 $i$ 个前缀对应的状态记为 $v_i$，这样就得到 $v_0,v_1,\cdots,v_{n-1}$ 共计 $n$ 个状态．另外，规定初始状态 $t_0$ 为 $v_{-1}$，对应着空前缀．这些状态姑且称为「前缀节点」．

引理 4 中提及，所有状态和所有后缀链接构成根为 $t_0$ 的根向树，这个树也称为 **后缀链接树**（国内 OI 选手也常称它为 **parent 树**）．它记录了字符串全体前缀的所有后缀的信息，亦即全体子串的信息．

后缀链接树有如下性质：

-   祖先节点对应的字符串总是子孙节点对应的字符串的后缀．
-   每个节点处的 $\operatorname{endpos}$ 集合就是它的子树内的所有「前缀节点」$v_i$ 的下标 $i$ 的集合．
-   后缀链接树的祖先节点的 $\operatorname{endpos}$ 集合总是严格包含子孙节点的 $\operatorname{endpos}$ 集合．
-   每个节点处的 $\operatorname{len}$ 的值就是它的子树内的所有「前缀节点」$v_i$ 对应前缀的最长公共后缀的长度．
-   除根节点 $t_0$ 外，每个节点对应的不同子串的数目，就是它的 $\operatorname{len}$ 值，减去它的父节点的 $\operatorname{len}$ 值，即 $\operatorname{len}(v)-\operatorname{len}(\operatorname{link}(v))$．

这些性质有很多应用．比如，第 $i$ 个前缀和第 $j$ 个前缀的最长公共后缀对应的字符串就是 $v_i$ 和 $v_j$ 的 LCA 对应的最长字符串．

最后，对字符串 $s$ 建立的后缀链接树与对它的翻转 $s_R$ 建立的 [后缀树](./suffix-tree.md) 有相同的结构．这一点常常用于离线构造后缀树．

## 应用

下面我们来看一些可以用 SAM 解决的问题．简单起见，假设字符集的大小 $k$ 为常数．这允许我们认为增加一个字符和遍历的复杂度为常数．

### 检查字符串是否出现

???+ example "问题"
    给一个文本串 $T$ 和多个模式串 $P$，我们要检查字符串 $P$ 是否作为 $T$ 的一个子串出现．

??? note "解法"
    我们在 $O(\left|T\right|)$ 的时间内对文本串 $T$ 构造后缀自动机．为了检查模式串 $P$ 是否在 $T$ 中出现，我们沿转移（边）从 $t_0$ 开始根据 $P$ 的字符进行转移．如果在某个点无法转移下去，则模式串 $P$ 不是 $T$ 的一个子串．如果我们能够这样处理完整个字符串 $P$，那么模式串在 $T$ 中出现过．
    
    对于每个字符串 $P$，算法的时间复杂度为 $O(\left|P\right|)$．此外，这个算法还找到了模式串 $P$ 在文本串中出现的最大前缀长度．

### 不同子串个数

???+ example "问题"
    给一个字符串 $S$，计算不同子串的个数．

??? note "解法一"
    对字符串 $S$ 构造后缀自动机．
    
    每个 $S$ 的子串都相当于自动机中的一些路径．因此不同子串的个数等于自动机中以 $t_0$ 为起点的不同路径的条数．
    
    考虑到 SAM 为有向无环图，不同路径的条数可以通过动态规划计算．即令 $d_{v}$ 为从状态 $v$ 开始的路径数量（包括长度为零的路径），则我们有如下递推方程：
    
    $$
    d_{v}=1+\sum_{w:(v,w,c)\in DAWG}d_{w}
    $$
    
    即，$d_{v}$ 可以表示为所有 $v$ 的转移的末端的和，$DAWG$ 中的三元组 $(v,w,c)$ 表示后缀自动机中存在自 $v$ 经 $c$ 至 $w$ 的转移．
    
    所以不同子串的个数为 $d_{t_0}-1$（因为要去掉空子串）．
    
    总时间复杂度为：$O(\left|S\right|)$．

??? note "解法二"
    另一种方法是在构造完后缀自动机后，利用得到的后缀链接树的信息．每个节点对应的子串数量是 $\operatorname{len}(v)-\operatorname{len}(\operatorname{link}(v))$，对自动机所有节点求和即可．
    
    总时间复杂度仍然为：$O(\left|S\right|)$．

例题：[【模板】后缀自动机](https://www.luogu.com.cn/problem/P3804)，[SDOI2016 生成魔咒](https://loj.ac/problem/2033)

### 所有不同子串的总长度

???+ example "问题"
    给定一个字符串 $S$，计算所有不同子串的总长度．

??? note "解法一"
    本题做法与上一题类似，只是现在我们需要考虑分两部分进行动态规划：不同子串的数量 $d_{v}$ 和它们的总长度 $ans_{v}$．
    
    我们已经在上一题中介绍了如何计算 $d_{v}$．$ans_{v}$ 的值可以通过以下递推式计算：
    
    $$
    ans_{v}=\sum_{w:(v,w,c)\in DAWG}d_{w}+ans_{w}
    $$
    
    我们取每个邻接结点 $w$ 的答案，并加上 $d_{w}$（因为从状态 $v$ 出发的子串都增加了一个字符）．
    
    算法的时间复杂度仍然是 $O(\left|S\right|)$．

??? note "解法二"
    同样可以利用后缀链接树的信息．每个节点对应的最长子串的所有后缀长度是
    
    $$
    \dfrac{\operatorname{len}(v)\times (\operatorname{len}(v)+1)}{2},
    $$
    
    减去其 $\operatorname{link}$ 节点的对应值就是该节点的净贡献，对自动机所有节点求和即可．
    
    总时间复杂度仍然为：$O(\left|S\right|)$．

### 字典序第 k 大子串

???+ example "问题"
    给定一个字符串 $S$．多组询问，每组询问给定一个数 $K_i$，查询 $S$ 的所有子串中字典序第 $K_i$ 大的子串．

??? note "解法"
    解决这个问题的思路可以从解决前两个问题的思路发展而来．字典序第 $k$ 大的子串对应于 SAM 中字典序第 $k$ 大的路径，因此在计算每个状态的路径数后，我们可以很容易地从 SAM 的根开始找到第 $k$ 大的路径．
    
    预处理的时间复杂度为 $O(\left|S\right|)$，单次查询的复杂度为 $O(\left|ans\right|\cdot\left|\Sigma\right|)$（其中 $ans$ 是查询的答案，$\left|\Sigma\right|$ 为字符集的大小）．

??? info "另注"
    虽然该题是后缀自动机的经典题，但实际上这题由于涉及字典序，用后缀数组做最方便．

例题：[SPOJ - SUBLEX](https://www.spoj.com/problems/SUBLEX/)，[TJOI2015 弦论](https://loj.ac/problem/2102)

### 最小循环移位

???+ example "问题"
    给定一个字符串 $S$．找出字典序最小的循环移位．

??? note "解法"
    容易发现字符串 $S+S$ 包含字符串 $S$ 的所有循环移位作为子串．
    
    所以问题简化为在 $S+S$ 对应的后缀自动机上寻找最小的长度为 $\left|S\right|$ 的路径，这可以通过平凡的方法做到：我们从初始状态开始，贪心地访问最小的字符即可．
    
    总的时间复杂度为 $O(\left|S\right|)$．

### 出现次数

???+ example "问题"
    对于一个给定的文本串 $T$，有多组询问，每组询问给一个模式串 $P$，回答模式串 $P$ 在字符串 $T$ 中作为子串出现了多少次．

??? note "解法一"
    利用后缀链接树的信息，进行 dfs 即可预处理每个节点的 $\operatorname{endpos}$ 集合的大小．
    
    所有「前缀节点」的初始集合大小为 $1$，非「前缀节点」的初始集合大小为 $0$．然后，沿着后缀链接自下向上回溯时，每个父节点的集合大小都加上它的所有子节点的集合大小（不要遗漏父节点本身的初始值）．这样得到的每个节点处的值，就是该节点的 $\operatorname{endpos}$ 集合的大小．不同子节点的集合大小可以直接相加的理由是，同一个 $v_i$ 只会出现在一个子树内，故而相加不会重复．
    
    查询时，在自动机上查找模式串 $P$ 对应的节点，如果存在，则答案就是该节点的 $\operatorname{endpos}$ 集合的大小；如果不存在，则答案为 $0$．
    
    预处理时间复杂度为 $O(|T|)$．单次查询的时间复杂度为 $O(|P|)$．

??? note "解法二"
    对文本串 $T$ 构造后缀自动机．
    
    接下来做预处理：对于自动机中的每个状态 $v$，预处理 $cnt_{v}$，使之等于 $\operatorname{endpos}(v)$ 集合的大小．事实上，对应同一状态 $v$ 的所有子串在文本串 $T$ 中的出现次数相同，这相当于集合 $\operatorname{endpos}$ 中的位置数．
    
    然而我们不能明确的构造集合 $\operatorname{endpos}$，因此我们只考虑它们的大小 $cnt$．
    
    为了计算这些值，我们进行以下操作．对于每个状态，如果它不是通过复制创建的（且它不是初始状态 $t_0$），我们将它的 $cnt$ 初始化为 1．然后我们按它们的长度 $\operatorname{len}$ 降序遍历所有状态，并将当前的 $cnt_{v}$ 的值加到后缀链接指向的状态上，即：
    
    $$
    cnt_{\operatorname{link}(v)}+=cnt_{v}
    $$
    
    这样做每个状态的答案都是正确的．
    
    为什么这是正确的？不是通过复制获得的状态，恰好有 $\left|T\right|$ 个，并且它们中的前 $i$ 个在我们插入前 $i$ 个字符时产生．因此对于每个这样的状态，我们在它被处理时计算它们所对应的位置的数量．因此我们初始将这些状态的 $cnt$ 的值赋为 $1$，其它状态的 $cnt$ 值赋为 $0$．
    
    接下来我们对每一个 $v$ 执行以下操作：$cnt_{\operatorname{link}(v)}+=cnt_{v}$．其背后的含义是，如果有一个字符串 $v$ 出现了 $cnt_{v}$ 次，那么它的所有后缀也在完全相同的地方结束，即也出现了 $cnt_{v}$ 次．
    
    为什么我们在这个过程中不会重复计数（即把某些位置数了两次）呢？因为我们只将一个状态的位置添加到 **一个** 其它的状态上，所以一个状态不可能以两种不同的方式将其位置重复地指向另一个状态．
    
    因此，我们可以在 $O(\left|T\right|)$ 的时间内计算出所有状态的 $cnt$ 的值．
    
    最后回答询问只需要查找值 $cnt_{t}$，其中 $t$ 为模式串对应的状态，如果该模式串不存在答案就为 $0$．单次查询的时间复杂度为 $O(\left|P\right|)$．

### 第一次出现的位置

???+ example "问题"
    给定一个文本串 $T$，多组查询．每次查询字符串 $P$ 在字符串 $T$ 中第一次出现的位置（$P$ 的开头位置）．

??? note "解法一"
    利用后缀链接树的信息，进行 dfs 即可预处理每个节点的 $\operatorname{endpos}$ 集合中的最小值．
    
    所有「前缀节点」$v_i$ 的初始值为 $i$，非「前缀节点」的初始值为 $\infty$．然后，沿着后缀链接自下向上回溯时，每个父节点的值都与它的所有子节点的值比较，取最小值（不要遗漏父节点本身的初始值）．这样得到的每个节点处的值，就是该节点的 $\operatorname{endpos}$ 集合中的最小值．
    
    查询时，在自动机上查找模式串 $P$ 对应的节点，如果存在，则答案就是该节点的值，减去 $|P|-1$；如果不存在，则答案不存在．
    
    预处理时间复杂度为 $O(|T|)$．单次查询的时间复杂度为 $O(|P|)$．

??? note "解法二"
    我们构造一个后缀自动机．我们对 SAM 中的所有状态预处理位置 $\operatorname{firstpos}$．即，对每个状态 $v$ 我们想要找到第一次出现这个状态的末端的位置 $\operatorname{firstpos}[v]$．换句话说，我们希望先找到每个集合 $\operatorname{endpos}$ 中的最小的元素（显然我们不能显式地维护所有 $\operatorname{endpos}$ 集合）．
    
    为了维护 $\operatorname{firstpos}$ 这些位置，我们对函数 `sam_extend()` 进行扩展．当我们创建新状态 $\textit{cur}$ 时，我们令：
    
    $$
    \operatorname{firstpos}(\textit{cur})=\operatorname{len}(\textit{cur})-1.
    $$
    
    当我们将结点 $q$ 复制到 $\textit{clone}$ 时，我们令：
    
    $$
    \operatorname{firstpos}(\textit{clone})=\operatorname{firstpos}(q).
    $$
    
    （因为值的唯一的其它选项 $\operatorname{firstpos}(\textit{cur})$ 显然太大了）．
    
    那么查询的答案就是 $\operatorname{firstpos}(t)-\left|P\right|+1$，其中 $t$ 为对应字符串 $P$ 的状态．单次查询只需要 $O(\left|P\right|)$ 的时间．

### 所有出现的位置

???+ example "问题"
    问题同上，这一次需要查询文本串 $T$ 中模式串 $P$ 出现的所有位置．

??? note "解法一"
    找到模式串 $P$ 对应的节点后，利用后缀链接树的信息，遍历子树，一旦发现终点节点就输出．
    
    单次查询复杂度为 $O(|P|)+O(\textit{answer}(P))$，其中，$\textit{answer}(P)$ 为本次询问的答案．仿照 [状态数为线性的证明](#状态数) 可以说明，后缀链接树的子树大小不会超过该节点的 $\operatorname{endpos}$ 集合的大小的二倍，因此遍历子树的复杂度是 $O(\textit{answer}(P))$ 的．

??? note "解法二"
    我们还是对文本串 $T$ 构造后缀自动机．与上一个问题相似，我们为所有状态计算位置 $\operatorname{firstpos}$．
    
    如果 $t$ 为对应于模式串 $P$ 的状态，显然 $\operatorname{firstpos}(t)$ 为答案之一．我们已经找到了自动机中对应于 $P$ 的状态．还需要找到其它哪些位置？正是那些对应于以 $P$ 为后缀的字符串的状态．换句话说，我们要找到所有可以通过后缀链接到达状态 $t$ 的状态．
    
    因此为了解决这个问题，我们需要为每一个状态保存一个指向它的后缀连接列表．查询的答案就包含了对于每个我们能从状态 $t$ 只使用反向的后缀链接进行 DFS 或 BFS 找到的所有状态的 $\operatorname{firstpos}$ 值．
    
    预处理的复杂度为 $O(|T|)$，单次查询的复杂度为 $O(|P|+\textit{answer}(P))$．
    
    我们不会重复访问一个状态（因为对于仅有一个后缀链接指向一个状态，所以不存在两条不同的路径指向同一状态）．
    
    我们只需要考虑两个可能有相同 $\operatorname{firstpos}$ 值的不同状态．这种情形只在一个状态是由另一个状态复制而来时发生．然而，这并不会对复杂度分析造成影响．仿照 [状态数为线性的证明](#状态数)，所有这种后缀为 $P$ 的状态数目不会超过 $2\textit{answer}(P)$．
    
    此外，我们可以通过不考虑复制而来的节点的 $\operatorname{firstpos}$ 值来去除重复的位置．事实上对于一个状态，如果经过被复制状态可以到达，则经过原状态也可以到达．因此，如果我们给每个状态记录标记 `is_clone` 来代表这个状态是不是被复制出来的，我们就可以简单地忽略掉被复制的状态，只输出其它所有状态的 $firstpos$ 的值．
    
    以下是大致的实现：
    
    ```cpp
    struct state {
      bool is_clone;
      int first_pos;
      std::vector<int> inv_link;
      // some other variables
    };
    
    // 在构造 SAM 后
    for (int v = 1; v < sz; v++) st[st[v].link].inv_link.push_back(v);
    
    // 输出所有出现位置
    void output_all_occurrences(int v, int P_length) {
      if (!st[v].is_clone) cout << st[v].first_pos - P_length + 1 << endl;
      for (int u : st[v].inv_link) output_all_occurrences(u, P_length);
    }
    ```

### 最短的没有出现的字符串

???+ example "问题"
    给定一个字符串 $S$ 和一个特定的字符集，我们要找一个长度最短的没有在 $S$ 中出现过的字符串．

??? note "解法"
    我们在字符串 $S$ 的后缀自动机上做动态规划．
    
    假定我们已经处理完了子串的一部分，当前在状态 $v$，想找到不连续的转移需要添加的最小字符数量，将节点 $v$ 处的这个数量记作 $d_v$．
    
    计算 $d_{v}$ 非常简单．如果不存在使用字符集中至少一个字符的转移，则 $d_{v}=1$．否则添加一个字符是不够的，我们需要求出所有转移中的最小值：
    
    $$
    d_{v}=1+\min_{w:(v,w,c)\in SAM}d_{w}
    $$
    
    问题的答案就是 $d_{t_0}$，字符串可以通过计算过的数组 $d$ 逆推回去．

### 两个字符串的最长公共子串

???+ example "问题"
    给定两个字符串 $S$ 和 $T$，求出最长公共子串，公共子串定义为在 $S$ 和 $T$ 中都作为子串出现过的字符串 $X$．

??? note "解法"
    我们对字符串 $S$ 构造后缀自动机．
    
    我们现在处理字符串 $T$，对于每一个前缀，都在 $S$ 中寻找这个前缀的最长后缀．换句话说，对于每个字符串 $T$ 中的位置，我们想要找到这个位置结束的 $S$ 和 $T$ 的最长公共子串的长度．
    
    为了达到这一目的，我们使用两个变量，**当前状态**  $v$ 和 **当前长度**  $l$．这两个变量描述当前匹配的部分：它的长度和它们对应的状态．
    
    一开始 $v=t_0$ 且 $l=0$，即，匹配为空串．
    
    现在我们来描述如何添加一个字符 $T_{i}$ 并为其重新计算答案：
    
    -   如果存在一个从 $v$ 到字符 $T_{i}$ 的转移，我们只需要转移并让 $l$ 自增一．
    -   如果不存在这样的转移，我们需要缩短当前匹配的部分，这意味着我们需要按照后缀链接进行转移：
    
        $$
        v=\operatorname{link}(v)
        $$
    
        与此同时，需要缩短当前长度．显然我们需要将 $l$ 赋值为 $\operatorname{len}(v)$，因为经过这个后缀链接后我们到达的状态所对应的最长字符串是一个子串．
    -   如果仍然没有使用这一字符的转移，我们继续重复经过后缀链接并减小 $l$，直到我们找到一个转移或到达虚拟状态 $-1$（这意味着字符 $T_{i}$ 根本没有在 $S$ 中出现过，所以我们设置 $v=l=0$）．
    
    显然问题的答案就是所有 $l$ 的最大值．
    
    这一部分的时间复杂度为 $O(\left|T\right|)$，因为每次移动我们要么可以使 $l$ 增加一，要么可以在后缀链接间移动几次，每次都减小 $l$ 的值．
    
    代码实现：
    
    ```cpp
    string lcs(const string &S, const string &T) {
      sam_init();
      for (int i = 0; i < S.size(); i++) sam_extend(S[i]);
    
      int v = 0, l = 0, best = 0, bestpos = 0;
      for (int i = 0; i < T.size(); i++) {
        while (v && !st[v].next.count(T[i])) {
          v = st[v].link;
          l = st[v].length;
        }
        if (st[v].next.count(T[i])) {
          v = st[v].next[T[i]];
          l++;
        }
        if (l > best) {
          best = l;
          bestpos = i;
        }
      }
      return T.substr(bestpos - best + 1, best);
    }
    ```

例题：[SPOJ Longest Common Substring](https://www.spoj.com/problems/LCS/en/)

### 多个字符串间的最长公共子串

???+ example "问题"
    给定 $k$ 个字符串 $S_i$．我们需要找到它们的最长公共子串，即作为子串出现在每个字符串中的字符串 $X$．

??? note "解法一"
    我们将所有的子串连接成一个较长的字符串 $T$，以特殊字符 $D_i$ 分开每个字符串（一个字符对应一个字符串）：
    
    $$
    T=S_1+D_1+S_2+D_2+\cdots+S_k+D_k.
    $$
    
    然后对字符串 $T$ 构造后缀自动机．
    
    现在我们需要在自动机中找到存在于所有字符串 $S_i$ 中的一个字符串，为此可以利用添加的特殊字符．如果 $S_j$ 包含了一个子串 $X$，则从子串 $X$ 对应的节点 $t$ 出发，必然存在一条到达 $D_j$ 但是不经过任何其它特殊字符 $D_1,\cdots,D_{j-1},D_{j+1},\cdots,D_k$ 的路径．对于公共子串 $X$，应当对每个特殊字符 $D_j$ 都存在这样的路径．
    
    因此我们需要计算可达性，即对于自动机中的每个状态和每个字符 $D_i$，是否存在这样的一条路径．这可以容易地通过 DFS 或 BFS 及动态规划计算．这之后，问题的答案就是所有能够达到所有特殊字符的状态 $v$ 对应的最长子串 $\operatorname{longest}(v)$ 中最长的那个．

??? note "解法二"
    不妨设 **最短** 的字符串为 $S_1$，对它构造 SAM．利用解决两个字符串最长公共子串的算法，计算剩余的每个字符串与 $S_1$ 的最长公共子串长度．在匹配过程中，每添加一个要匹配的字符串 $S_j$ 中的字符，就相应地在 SAM 上移动，因此，可以直接记录 **在匹配过程中** SAM 每个状态能够匹配上的 $S_j$ 的最长子串的长度．
    
    因为匹配过程中，每次匹配到 SAM 的一个状态时，必然同时匹配到了它在后缀链接树上的所有祖先节点，但是祖先节点的匹配长度的信息并没有更新．所以，在完成对字符串 $S_j$ 的匹配后，需要自下而上地沿着后缀链接更新，将子节点匹配到的最长子串的信息更新到父节点．此时，需要注意父节点记录的最长匹配长度不能超过它自身的 $\operatorname{len}$ 值．这样，就得到了 $S_1$ 的 SAM 上每个状态 **实际能够匹配到** 的 $S_j$ 的最长字串长度．
    
    最后，只需要对每个 $S_2,\cdots,S_k$ 都匹配一遍，再对 SAM 上每个状态记录的实际匹配到的长度取最小值，就得到 SAM 上每个状态实际能够匹配到的 $S_2,\cdots,S_k$ 的最长公共子串的长度．然后，遍历 SAM 所有状态，取最大值就是这 $k$ 个串的最长公共子串长度．
    
    算法时间复杂度是 $O(\sum_i |S_i|)$ 的．字符串 $S_1$ 的 SAM 虽然遍历了 $k$ 遍，但是因为 $|S_1|$ 是最小的，所以 $k|S_1|\le \sum_i |S_i|$，复杂度的主要项依然是匹配过程遍历所有子串．

例题：[SPOJ Longest Common Substring II](https://www.spoj.com/problems/LCS2/)

## 习题

-   [【模板】后缀自动机](https://www.luogu.com.cn/problem/P3804)
-   [SDOI2016 生成魔咒](https://loj.ac/problem/2033)
-   [SPOJ - SUBLEX](https://www.spoj.com/problems/SUBLEX/)
-   [TJOI2015 弦论](https://loj.ac/problem/2102)
-   [SPOJ Longest Common Substring](https://www.spoj.com/problems/LCS/en/)
-   [SPOJ Longest Common Substring II](https://www.spoj.com/problems/LCS2/)
-   [Codeforces 1037H Security](https://codeforces.com/problemset/problem/1037/H)
-   [Codeforces 666E Forensic Examination](https://codeforces.com/problemset/problem/666/E)
-   [HDU4416 Good Article Good sentence](https://acm.hdu.edu.cn/showproblem.php?pid=4416)
-   [HDU4436 str2int](https://acm.hdu.edu.cn/showproblem.php?pid=4436)
-   [HDU6583 Typewriter](https://acm.hdu.edu.cn/showproblem.php?pid=6583)
-   [Codeforces 235C Cyclical Quest](https://codeforces.com/problemset/problem/235/C)
-   [CTSC2012 熟悉的文章](https://www.luogu.com.cn/problem/P4022)
-   [NOI2018 你的名字](https://uoj.ac/problem/395)

## 相关资料

我们先给出与 SAM 有关的最初的一些文献：

-   A. Blumer, J. Blumer, A. Ehrenfeucht, D. Haussler, R. McConnell. Linear Size Finite Automata for the Set of All Subwords of a Word. An Outline of Results. \[1983]
-   A. Blumer, J. Blumer, A. Ehrenfeucht, D. Haussler. The Smallest Automaton Recognizing the Subwords of a Text. \[1984]
-   Maxime Crochemore. Optimal Factor Transducers. \[1985]
-   Maxime Crochemore. Transducers and Repetitions. \[1986]
-   A. Nerode. Linear automaton transformations. \[1958]

另外，在更新的一些资源以及很多关于字符串算法的书中，都能找到这个主题：

-   Maxime Crochemore, Rytter Wowjcieh. Jewels of Stringology. \[2002]
-   Bill Smyth. Computing Patterns in Strings. \[2003]
-   Bill Smith. Methods and algorithms of calculations on lines. \[2006]

另外，还有一些资料：

-   《后缀自动机》，陈立杰．
-   《后缀自动机在字典树上的拓展》，刘研绎．
-   《后缀自动机及其应用》，张天扬．
-   <https://www.cnblogs.com/zinthos/p/3899679.html>
-   <https://codeforces.com/blog/entry/20861>
-   <https://zhuanlan.zhihu.com/p/25948077>

**本页面主要译自博文 [Суффиксный автомат](http://e-maxx.ru/algo/suffix_automata) 与其英文翻译版 [Suffix Automaton](https://cp-algorithms.com/string/suffix-automaton.html)．其中俄文版版权协议为 Public Domain + Leave a Link；英文版版权协议为 CC-BY-SA 4.0．**

[^state-endpos]: 需要将每个状态都取作一个 $\operatorname{endpos}$ 等价类的原因，其实就是本段提到的 Myhill–Nerode 定理．简单来说，如果两个字符串 $t$ 和 $u$ 的 $\operatorname{endpos}$ 集合不同，那么它们不能对应于 SAM 的同一个状态：同一个状态到达终止状态的路径总是一样的，这意味着在 $t$ 和 $u$ 末尾添加字符到达 $s$ 的结尾的方式也是一样的，而这正说明 $t$ 和 $u$ 在字符串 $s$ 中的结束位置一样．反过来，只要两个字符串 $t$ 和 $u$ 的 $\operatorname{endpos}$ 集合相同，就可以将它们对应到 SAM 的同一个状态．这样做可行，就是 Nerode 定理的证明的内容，在此不多讨论．但是，此处的讨论至少可以相信，将 $\operatorname{endpos}$ 集合相同的字符串放到同一个状态，这样得到的 SAM 一定是最小的，因为进一步合并节点是不可能的．

[^time-complexity]: 如果不额外使用列表记录当前状态的可用转移，只用数组存储所有可能的转移（无论是否存在）并在复制节点时直接复制，那么时间复杂度也是 $O(n\left|\Sigma\right|)$ 的．

[^monotone-loc]: 此处正文没有解释的是，在第一种和第二种情况中，$\operatorname{longest}(\operatorname{link}(\operatorname{link}(\textit{last})))$ 的位置是否也是单调（弱）递增的．第一种情况容易验证，因为更新后 $\operatorname{longest}(\operatorname{link}(\operatorname{link}(\textit{last})))$ 是空串，起止位置在字符串 $s$ 的末尾．第二种情况，转移是连续的，说明 $\operatorname{longest}(q) = \operatorname{longest}(p)+c$．然而，向子串的末尾添加新的字符只会使得该子串更难以出现在字符串中，也就是说，当字符串 $\operatorname{longest}(p)$ 的长度为 $\operatorname{len}(\operatorname{link}(p))$ 的后缀的结束位置集合严格包含 $\operatorname{endpos}(p)$ 时，字符串 $\operatorname{longest}(q)$ 的长度为 $\operatorname{len}(\operatorname{link}(p))+1$ 的后缀的结束位置集合可能仍然与 $\operatorname{endpos}(q)$ 相同．故而，$\operatorname{len}(\operatorname{link}(q))<\operatorname{len}(\operatorname{link}(p))+1$，亦即 $\operatorname{longest}(\operatorname{link}(p))$ 作为 $s$ 的后缀的起始位置必然不大于 $\operatorname{longest}(\operatorname{link}(q))$ 作为 $s+c$ 的后缀的起始位置．而当一次找到状态 $p$ 使得存在经由 $c$ 的转移时，必定移动了至少一次，这说明 $\operatorname{longest}(\operatorname{link}(p))$ 作为 $s$ 的后缀的起始位置不小于 $\operatorname{longest}(\operatorname{link}(\operatorname{link}(\textit{last})))$ 作为 $s$ 的后缀的起始位置．最后，$\operatorname{longest}(\operatorname{link}(q))=\operatorname{longest}(\operatorname{link}(\operatorname{link}(\textit{cur})))$．这就说明，在第二种情况中，$\operatorname{longest}(\operatorname{link}(\operatorname{link}(\textit{last})))$ 的位置也是单调递增的．


## string/seq-automaton.md

在阅读本文之前，请先阅读 [自动机](../misc/fsm.md)．

## 定义

序列自动机是接受且仅接受一个字符串的子序列的自动机．

本文中用 $s$ 代指这个字符串．

### 状态

若 $s$ 包含 $n$ 个字符，那么序列自动机包含 $n+1$ 个状态．

令 $t$ 是 $s$ 的一个子序列，那么 $\delta(start, t)$ 是 $t$ 在 $s$ 中第一次出现时末端的位置．

也就是说，一个状态 $i$ 表示前缀 $s[1..i]$ 的子序列与前缀 $s[1..i-1]$ 的子序列的差集．

序列自动机上的所有状态都是接受状态．

### 转移

由状态定义可以得到，$\delta(u, c)=\min\{i|i>u,s[i]=c\}$，也就是字符 $c$ 下一次出现的位置．

为什么是「下一次」出现的位置呢？因为若 $i>j$，后缀 $s[i..|s|]$ 的子序列是后缀 $s[j..|s|]$ 的子序列的子集，一定是选尽量靠前的最优．

## 实现

从后向前扫描，过程中维护每个字符最前的出现位置：

$$
\begin{array}{ll}
1 & \textbf{Input. } \text{A string } S\\
2 & \textbf{Output. } \text{The state transition of the sequence automaton of }S \\
3 & \textbf{Method. }  \\
4 & \textbf{for }c\in\Sigma\\
5 & \qquad next[c]\gets null\\
6 & \textbf{for }i\gets|S|\textbf{ downto }1\\
7 & \qquad next[S[i]]\gets i\\
8 & \qquad \textbf{for }c\in\Sigma\\
9 & \qquad\qquad \delta(i-1,c)\gets next[c]\\
10 & \textbf{return }\delta
\end{array}
$$

这样构建的复杂度是 $O(n|\Sigma|)$．

## 例题

???+ example "[「HEOI2015」最短不公共子串](https://loj.ac/problem/2123)"
    给你两个由小写英文字母组成的串 $A$ 和 $B$（$1\le |A|, |B|\le 2000$），求：
    
    1.  $A$ 的一个最短的子串，它不是 $B$ 的子串；
    2.  $A$ 的一个最短的子串，它不是 $B$ 的子序列；
    3.  $A$ 的一个最短的子序列，它不是 $B$ 的子串；
    4.  $A$ 的一个最短的子序列，它不是 $B$ 的子序列．

??? note "题解"
    题目的 1 和 3 两问需要后缀自动机，而且做法类似，在这里只讲解 2 和 4 两问．
    
    第 2 问比较简单，枚举 A 的子串输入进 B 的序列自动机，若不接受则计入答案．
    
    第 4 问需要 DP．令 $f(i, j)$ 表示在 A 的序列自动机中处于状态 $i$，在 B 的序列自动机中处于状态 $j$，需要再添加多少个字符能够不是公共子序列．状态转移方程为：
    
    $$
    f(i, j)=\min_{\delta_A(i,c)\ne \textit{null}}f(\delta_A(i, c), \delta_B(j, c))+1.
    $$
    
    转移起点为 $f(i, \textit{null})=0$．

??? note "参考代码"
    ```cpp
    --8<-- "docs/string/code/seq-automaton/seq-automaton_1.cpp"
    ```


## string/suffix-bst.md

## 定义

后缀之间的大小由字典序定义，后缀平衡树就是一个维护这些后缀顺序的平衡树，即字符串 $T$ 的后缀平衡树是 $T$ 所有后缀的有序集合．后缀平衡树上的一个节点相当于原字符串的一个后缀．

特别地，后缀平衡树的中序遍历即为后缀数组．

## 构造过程

对长度为 $n$ 的字符串 $T$ 建立其后缀平衡树，考虑逆序将其后缀加入后缀平衡树．

记后缀平衡树维护的集合为 $X$，当前添加的后缀为 $S$，则添加下一个后缀就是向 $X$ 中加入 $\texttt{c}S$（亦可理解为后缀平衡树维护的字符串为 $S$，下一步往 $S$ 前加入一个字符 $\texttt{c}$）．这一操作其实就是向平衡树中插入节点．

这里使用期望树高为 $O(\log n)$ 的平衡树，例如替罪羊树或 Treap 等．

### 做法 1

插入时，暴力比较两个后缀之间的大小关系，从而判断之后是往哪一个子树添加．这样子，单次插入至多比较 $O(\log n)$ 次，单次比较的时间复杂度至多为 $O(n)$，一共 $O(n\log n)$．

一共会插入 $n$ 次，所以该做法的时间复杂度存在上界 $O(n^2 \log n)$．

### 做法 2

注意到 $\texttt{c}S$ 与 $S$ 的区别仅在于 $\texttt{c}$，且 $S$ 已经属于 $X$ 了，可以利用这一点来优化插入操作．

假设当前要比较 $\texttt{c}S$ 与 $A$ 两个字符串的大小，且 $A, S \in X$．每次比较时，首先比较两串的首字符．若首字符不等，则两串的大小关系就已经确定了；若首字符相等，那么就只需要判断去除首字符后两字符串的大小关系．而两串去除首字符后都已经属于 $X$ 了，这时候可以借助平衡树 $O(\log n)$ 求排名的操作来完成后续的比较．这样，单次插入的操作至多 $O(\log^2 n)$．

一共会插入 $n$ 次，所以该做法的时间复杂度存在上界 $O(n \log^2 n)$．

### 做法 3

根据做法 2，如果能够 $O(1)$ 判断平衡树中两个节点之间的大小关系，那么就可以在 $O(n \log n)$ 的时间内完成后缀平衡树的构造．

记 $val_i$ 表示节点 $i$ 的值．如果在建平衡树时，每个节点多维护一个标记 $tag_i$，使得若 $tag_i > tag_j \iff val_i > val_j$，那么就可以根据 $tag_i$ 的大小 $O(1)$ 判断平衡树中两个节点的大小．

不妨令平衡树中每个节点对应一个实数区间，令根节点对应 $(0, 1)$．对于节点 $i$，记其对应的实数区间为 $(l, r)$，则 $tag_i = \frac{l + r}{2}$，其左子树对应实数区间 $(l, tag_i)$，其右子树对应实数区间 $(tag_i, r)$．易证 $tag_i$ 满足上述要求．

由于使用了期望树高为 $O(\log n)$ 的平衡树，所以精度是有一定保证的．实际实现时也可以用一个较大的区间来做，例如让根对应 $(0, 10^{18})$．

### 做法 4

其实可以先构建出后缀数组，然后再根据后缀数组构建后缀平衡树．这样做的复杂度瓶颈在于后缀数组的构建复杂度或者所用平衡树一次性插入 $n$ 个元素的复杂度．

## 删除操作

假设当前添加的后缀为 $\texttt{c}S$，上一个添加的后缀为 $S$．后缀平衡树还支持删除后缀 $\texttt{c}S$ 的操作（亦可理解为后缀平衡树维护的字符串为 $\texttt{c}S$，将开头的 $\texttt{c}$ 删除）．

类似于插入操作，借助平衡树的删除节点操作可以完成删除 $\texttt{c}S$ 的操作．

## 后缀平衡树的优点

-   后缀平衡树的思路比较清晰，相比后缀自动机等后缀结构更好理解，会写平衡树就能写．
-   后缀平衡树的复杂度不依赖于字符集的大小
-   后缀平衡树支持在字符串开头删除一个字符
-   如果使用支持可持久化的平衡树，那么后缀平衡树也能可持久化

## 例题

### [P3809【模板】后缀排序](https://www.luogu.com.cn/problem/P3809)

后缀数组的模板题，建出后缀平衡树之后，通过中序遍历得到后缀数组．

??? note "SGT 版本的参考代码"
    ```cpp
    --8<-- "docs/string/code/suffix-bst/suffix-bst_1.cpp"
    ```

### [P6164【模板】后缀平衡树](https://www.luogu.com.cn/problem/P6164)

???+ note "题意"
    给定初始字符串 $s$ 和 $q$ 个操作：
    
    1.  在当前字符串的后面插入若干个字符．
    2.  在当前字符串的后面删除若干个字符．
    3.  询问字符串 $t$ 作为连续子串在当前字符串中出现了几次？
    
    题目 **强制在线**，字符串变化长度以及初始长度 $\le 8 \times 10^5$，$q \le 10^5$，询问的总长度 $\le 3 \times 10^6$．

对于操作 1 和操作 2，由于后缀平衡树维护头插和头删操作比较方便，所以想到把尾插和尾删操作搞成头插和头删．这里如果维护 $s$ 的反串的后缀平衡树，而非 $s$ 的后缀平衡树，就可以完成上述转换．平衡树的添加和删除都是 $O(\log n)$ 的，所以添加或者删除一个字符的时间复杂度为 $O(\log n)$．记添加和删除的总字符数为 $N$，那么这一部分总的时间复杂度为 $O(N \log n)$．

对于操作 3，$t$ 的出现次数等于以 $t$ 为前缀的后缀数量，而以 $t$ 为前缀的后缀数量等于其后继的排名减去其前驱的排名．在 $t$ 后面加入一个极大的字符，就可以构造出 $t$ 的一个后继．将 $t$ 的最后一个字符减小 1，就可以构造出 $t$ 的一个前驱．

现在要查询某一个串 $t$ 在后缀平衡树中排名，由于不能保证 $t$ 在后缀平衡树中出现过，所以每次只能暴力比较字符串大小．单次比较的时间复杂度为 $O(|t|)$，每次查询至多比较 $O(\log n)$ 次，所以单次查询的复杂度为 $O(|t|\log n)$．记所有询问串的长度和为 $L$，那么这一部分总的时间复杂度为 $O(L \log n)$．

??? note "SGT 版本的参考代码"
    ```cpp
    --8<-- "docs/string/code/suffix-bst/suffix-bst_2.cpp"
    ```

## 参考资料

-   陈立杰 -《重量平衡树和后缀平衡树在信息学奥赛中的应用》


## string/suffix-tree.md

后缀树是一种维护一个字符串所有后缀的数据结构．

## 一些记号

记构建后缀树的母串为 $S$，长度为 $n$，字符集为 $\Sigma$．

令 $S[i]$ 表示 $S$ 中的第 $i$ 个字符，其中 $1 \le i \le n$．

令 $S [l, r]$ 表示 $S$ 中第 $l$ 个字符至第 $r$ 个字符组成的字符串，称为 $S$ 的一个子串．

记 $S [i, n]$ 为 $S$ 的以 $i$ 开头的后缀，$S [1, i]$ 为 $S$ 的以 $i$ 结尾的前缀．

## 定义

定义字符串 $S$ 的 **后缀 trie** 为将 S 的所有后缀插入至 trie 树中得到的字典树．在后缀 trie 中，节点 x 对应的字符串为从根节点走到 x 的路径上经过的字符拼接而成的字符串．记后
缀 trie 中所有对应 $S$ 的某个后缀的节点为后缀节点．

容易看出后缀 trie 的优越性质：它的非根节点恰好能接受 $S$ 的所有本质不同非空子串．但构建后缀 trie 的时空复杂度均为 $O(n^2)$，在很多情况下不能接受，所以我们引入后缀树的概念．

如果令后缀 trie 中所有拥有多于一个儿子的节点和后缀节点为关键点，定义只保留关键点，将非关键点形成的链压缩成一条边形成的压缩 trie 树为 **后缀树 (Suffix Tree)**．如果仅令后缀 trie 中所有拥有多于一个儿子的节点和叶结点为关键点，定义只保留关键点形成的压缩 trie 树为 **隐式后缀树 (Implicit Suffix Tree)**．容易看出隐式后缀树为后缀树进一步压缩后得到的结果．

在后缀树和隐式后缀树中，每条边对应一个字符串；每个非根节点 $x$ 对应了一个字符串集合，为从根节点走到 $x$ 的父亲节点 $fa_x$ 经过的字符串，拼接上 $fa_x$ 至 $x$ 的树边对应的字符串的任意一个非空前缀，称为 $str_x$．同时，在隐式后缀树中，称一个没有对应任何节点的后缀为 **隐式后缀**．

下图从左至右分别为以字符串 $\texttt{cabab}$ 为母串构建的后缀 trie、后缀树和隐式后缀树．

![suffix-tree\_cabab1.png](./images/suffix-tree1.png)

考虑将 $S$ 的后缀逐个插入至后缀 trie 中．从第二次插入开始，每次最多新增一个拥有多于一个儿子的节点和一个后缀节点，所以后缀树中节点个数最多为 $2n$ 个，十分优秀．

## 后缀树的建立

### 支持前端动态添加字符的算法

反串建 SAM 建出的 parent 树就是这个串的后缀树，所以我们将反串的字符逐个加入 SAM 即可．

???+ note "参考实现"
    ```cpp
    struct SuffixAutomaton {
      int tot, lst;
      int siz[N << 1];
      int buc[N], id[N << 1];
    
      struct Node {
        int len, link;
        int ch[26];
      } st[N << 1];
    
      SuffixAutomaton() : tot(1), lst(1) {}
    
      void extend(int ch) {
        int cur = ++tot, p = lst;
        lst = cur;
        siz[cur] = 1, st[cur].len = st[p].len + 1;
        for (; p && !st[p].ch[ch]; p = st[p].link) st[p].ch[ch] = cur;
        if (!p)
          st[cur].link = 1;
        else {
          int q = st[p].ch[ch];
          if (st[q].len == st[p].len + 1)
            st[cur].link = q;
          else {
            int pp = ++tot;
            st[pp] = st[q];
            st[pp].len = st[p].len + 1;
            st[cur].link = st[q].link = pp;
            for (; p && st[p].ch[ch] == q; p = st[p].link) st[p].ch[ch] = pp;
          }
        }
      }
    } SAM;
    ```

### 支持后端动态添加字符的算法

Ukkonen 算法是一种增量构造算法．我们依次向树中插入串 $S$ 的每一个字符，并在每一次插入之后正确地维护当前的后缀树．

#### 朴素算法

首先介绍一下一种较为暴力的构建方式，我们用字符串 $\texttt {abbbc}$ 来演示一下构建的过程．

初始建立一个根节点，称为 $0$ 号节点．同时每条边我们维护一个区间 $[l,r]$ 表示这条边上的字符串为 $S[l,r]$．另外，维护已经插入的字符个数 $m$，初始为 $0$．

首先插入字符 $\texttt a$，直接从 $0$ 号节点伸出一条边，标为 $[1,\infty]$，指向一个新建的节点．这里的 $\infty$ 是一个极大值，可理解为串的结尾，这样在插入新字符时，这条边会自动的包含新的字符．

![suffix-tree\_a.webp](./images/suffix-tree2.webp)

接下来我们插入字符 $\texttt b$，同样从 $0$ 伸出一条边，标为 $[2,\infty⁡]$．注意到之前延伸出的边 $[1,\infty]$ 的意义自动地发生了变化，随着串结尾的改变，其表示的串从 $\texttt a$ 变为了 $\texttt {ab}$．这样是正确的，因为之前所有后缀都已经以一个叶节点的形式出现在树中，只需要向所有叶节点的末端插入一个当前字符即可．

![suffix-tree\_ab.webp](./images/suffix-tree3.webp)

接下来，我们要再次插入一个字符 $\texttt b$，但是 $\texttt b$ 是之前已经插入的字符串的一个子串，因此原树已经包含 $\texttt b$，此时，我们什么都不做，记录一个 $k$ 表示 $S[k,m]$ 是当前最长的隐式后缀．

![suffix-tree\_abb.webp](./images/suffix-tree4.webp)

接下来我们插入另一个 $\texttt b$．因为前一个 $\texttt b$ 没有插入成功，此时 $k=3$，代表要插入的后缀为 $\texttt {bb}$．我们从根开始向下寻找 $\texttt {bb}$，发现也在原树之中．同样，我们还是什么都不做．

![suffix-tree\_abbb.webp](./images/suffix-tree5.webp)

注意到我们没有管 $k$ 之后的后缀．因为如果 $S[k,m]$ 是一个隐式后缀，那么对于 $l>k$，$S[l,m]$ 都是隐式后缀．因为由 $S[k,m]$ 为隐式后缀可知，存在字符 $c$ 使得 $S[k, m] + c$ 为 $S$ 的子串，所以 $S [ l, m] + c$ 也为 $S$ 的子串，由隐式后缀树的定义可知 $S[ l, m]$ 也不作为叶结点出现．

接下来我们插入 $\texttt c$，此时 $k=3$，因此我们需要沿着根向下寻找 $\texttt {bbc}$，发现不在原树中．我们需要在 $\texttt {bb}$ 处代表的节点延伸出一条为 $[5,\infty]$ 的出边．但发现这个节点其实不存在，而是包含在一条边中，因此我们需要分裂这条边，创建一个新节点，再在创建的节点处伸展出我们要创建的出边．此时成功插入，令 $k\to k+1$，因为 $S[k,m]$ 不再是隐式后缀．

![suffix-tree\_abbbc1.webp](./images/suffix-tree6.webp)

接下来，因为 $k$ 变化了，我们重复这个过程，直到再次出现隐式后缀，或 $k>m$（在这个例子中，是后者）．

![suffix-tree\_abbbc2.webp](./images/suffix-tree7.webp)

构建过程结束．

该算法每次暴力从根向下寻找并插入的复杂度最坏为 $O(n)$，所以总的复杂度为 $O(n^2)$．

#### 后缀链接

朴素算法慢主要是因为每次 extend 都要从根找到最长隐式后缀的插入位置．所以考虑把这个位置记下来．首先，我们采用一个二元组 $(now,rem)$ 来描述当前这个最长的被隐式包含的后缀 $S[k,m]$．沿着节点 $now$ 的开头为 $S[m-rem+1]$ 的出边走长度 $rem$ 到达的位置应该唯一表示一个字符串，每次插入新的字符时，我们只需要从 $now$ 和 $rem$ 描述的位置查找即可．

现在，我们只需要在 $k\to k + 1$ 时更新 $(now,rem)$．此时如果 $now=0$，只需要让 $rem \to rem-1$，因为下一个要插入的后缀是刚才插入的长度 $-1$．否则，设 $str_{now}$ 对应的子串为 $S[l,r]$，我们需要找到一个节点 $now'$ 对应 $S[l+1,r]$，令 $now\to now'$ 即可．

首先有引理：对隐式后缀树中任意非叶非根节点 $x$，在树中存在另一非叶节点 $y$，使得 $str_y$ 是 $str_x$ 对应的子串删去开头的字符．

证明．令 $s$ 表示 $str_x$ 删去开头字符形成的字符串．由隐式后缀树的定义可知，存在两个不同的字符 $c_1,c_2$，满足 $str_x + c1$ 与 $str_x + c_2$ 均为 $S$ 的子串．所以，$s + c_1$ 与 $s + c_2$ 也为 $S$ 的子串，所以 $s$ 在后缀 trie 中也对应了一个有分叉的关键点，即在隐式后缀 trie 中存在 $y$ 使得 $str_y=s$．证毕．

由该引理，我们定义 $\operatorname{Link}(x)=y$，称为 x 的 **后缀链接 (Suffix Link)**．于是 $now'=\operatorname{Link}(now)$ 一定存在．现在我们只要能求出隐式后缀树中所有非根非叶节点的 $\operatorname{Link}$ 即可．

#### Ukkonen 算法

Ukkonen 算法的整体流程如下：

为了构建隐式后缀树，我们从前往后加入 $S$ 中的字符．假设根节点为 $0$，且当前已经建出 $S[1, m]$ 的隐式后缀树且维护好了后缀链接．$S [1, m]$ 的最长隐式后缀为 $S [k, m]$，在树中的位置为 $(now, rem)$．设 $S [m + 1] = x$, 现在我们需要加入字符 $x$．此时，$S [1, m]$ 的每一个后缀都需要在末尾添加字符 $x$．由于所有显式后缀都对应树中某个叶结点，它们父边右端点为 $\infty$，无需维护．所以，现在我们只用考虑隐式后缀末尾添加 x 对树的形态产生的影响．首先考虑 $S [k, m]$，有两种情况：

1.  $(now, rem)$ 位置已经存在 $x$ 的转移．此时后缀树形态不会发生变化．由于 $S [k, m+1]$ 已经在后缀树中出现，所以对于 $l > k$，$S [ l, m + 1]$ 也会在后缀树中出现，此时只需将 $rem\to rem + 1$，不需做任何修改．
2.  $(now, rem)$ 不存在 $x$ 的转移．如果 $(now, rem)$ 恰好为树中的节点，则此节点新增一条出边 $x$；否则需要对节点进行分裂，在此位置新增一个节点，并在新增节处添加出边 $x$．此时对于 $l > k$，我们并不知道 $S [ l, m]$ 会对后缀树形态造成什么影响，所以我们还需继续考虑 $S [k + 1, m]$．考虑怎么求出 $S [k + 1, m]$ 在后缀树中的位置：如果 $now$ 不为 $0$，可以利用后缀链接，令 $now = \operatorname{Link}(now)$；否则，令 $rem\to rem − 1$．最后令 $k\to k + 1$，再次重复这个过程．

每一步都只消耗常数时间，而算法在插入全部的字符后停止，所以时间复杂度为 $O(n)$．

由于 Ukkonen 算法只能处理出 $S$ 的隐式后缀树，而隐式后缀树在一些问题中的功能可能不如后缀树强大，所以在需要时，可以在 $S$ 的末端添加一个从未出现过的字符，这时 S 的所有后缀可以和树的所有叶子一一对应．

???+ note "参考实现"
    ```cpp
    struct SuffixTree {
      int ch[M + 5][RNG + 1], st[M + 5], len[M + 5], link[M + 5];
      int s[N + 5];
      int now{1}, rem{0}, n{0}, tot{1};
    
      SuffixTree() { len[0] = inf; }
    
      int new_node(int s, int le) {
        ++tot;
        st[tot] = s;
        len[tot] = le;
        return tot;
      }
    
      void extend(int x) {
        s[++n] = x;
        ++rem;
        for (int lst{1}; rem;) {
          while (rem > len[ch[now][s[n - rem + 1]]])
            rem -= len[now = ch[now][s[n - rem + 1]]];
          int &v{ch[now][s[n - rem + 1]]}, c{s[st[v] + rem - 1]};
          if (!v || x == c) {
            lst = link[lst] = now;
            if (!v)
              v = new_node(n, inf);
            else
              break;
          } else {
            int u{new_node(st[v], rem - 1)};
            ch[u][c] = v;
            ch[u][x] = new_node(n, inf);
            st[v] += rem - 1;
            len[v] -= rem - 1;
            lst = link[lst] = v = u;
          }
          if (now == 1)
            --rem;
          else
            now = link[now];
        }
      }
    } Tree;
    ```

## 作用

后缀树上每一个节点到根的路径都是 $S$ 的一个非空子串，这在处理很多字符串问题时都很有用．

后缀树的 DFS 序就是后缀数组．后缀树的一个子树也就对应到后缀数组上的一个区间．后缀树上两个后缀的最长公共前缀是它们对应的叶节点的 LCA，因此，后缀数组的 height 的结论可以理解为树上若干个节点的 LCA 等于 DFS 序最小的和最大的节点的 LCA．

## 例题

### [洛谷 P3804【模板】后缀自动机（SAM）](https://www.luogu.com.cn/problem/P3804)

题意：

给定一个只包含小写字母的字符串 $S$．

请你求出 $S$ 的所有出现次数不为 $1$ 的子串的出现次数乘上该子串长度的最大值．

??? note "解法"
    建出插入一个终止符的隐式后缀树．树上每条从根出发的路径都构成子串．一个显示后缀的出现次数即为对应节点子树内的叶子节点个数，隐式后缀不用考虑，因为一个隐式后缀的出现次数等于向下走到的第一个节点对应显示后缀的出现次数，而且一定没有该显示后缀长．所以遍历整棵树，求出每个节点子树内叶子个数和每个节点到根的路径长度．如果叶子个数 $>1$ 则更新答案．复杂度 $O(|S||\Sigma|)$．

??? note "参考代码"
    ```cpp
    --8<-- "docs/string/code/suffix-tree/suffix-tree_1.cpp"
    ```

### [CF235C Cyclical Quest](https://codeforces.com/problemset/problem/235/C)

题意：给定一个小写字母主串 $S$ 和 $n$ 个询问串，求每个询问串 $x_i$ 的所有循环同构在主串中出现的次数总和．

??? note "解法"
    建立插入终止符的隐式后缀树．
    
    枚举当前在那个循环节，记录在树上能查找到多长的前缀．
    
    重复类似 Ukkonen 算法的过程，记录当前能匹配到的位置 $(now,rem)$．每次尝试插入下一个字符，如果成功则继续插入，否则跳出循环．
    
    如果某一个次成功匹配了当前的循环节，且该循环节之前没出现过，则更新答案．
    
    然后切换到下个循环节的时候，我们要删去当前匹配的子串开头的字符：这正好就相当于令 $now \to \operatorname{Link}(now)$．当然，如果 $now=1$ 则直接让 $rem\to rem-1$ 就行了．
    
    复杂度 $O(|S||\Sigma|+\sum|x_i|)$

??? note "参考代码"
    ```cpp
    --8<-- "docs/string/code/suffix-tree/suffix-tree_2.cpp"
    ```

## 参考文献

1.  2021 国家集训队论文《后缀树的构建》代晨昕
2.  [炫酷后缀树魔术 - EternalAlexander 的博客](https://www.luogu.com.cn/blog/EternalAlexander/xuan-ku-hou-zhui-shu-mo-shu)


## string/trie.md

## 定义

字典树，英文名 trie．顾名思义，就是一个像字典一样的树．

## 引入

先放一张图：

![trie1](./images/trie1.png)

可以发现，这棵字典树用边来代表字母，而从根结点到树上某一结点的路径就代表了一个字符串．举个例子，$1\to4\to 8\to 12$ 表示的就是字符串 `caa`．

trie 的结构非常好懂，我们用 $\delta(u,c)$ 表示结点 $u$ 的 $c$ 字符指向的下一个结点，或者说是结点 $u$ 代表的字符串后面添加一个字符 $c$ 形成的字符串的结点．（$c$ 的取值范围和字符集大小有关，不一定是 $0\sim 26$．）

有时需要标记插入进 trie 的是哪些字符串，每次插入完成时在这个字符串所代表的节点处打上标记即可．

## 实现

放一个结构体封装的模板：

=== "C++"
    ```cpp
    struct trie {
      int nex[100000][26], cnt;
      bool exist[100000];  // 该结点结尾的字符串是否存在
    
      void insert(char *s, int l) {  // 插入字符串
        int p = 0;
        for (int i = 0; i < l; i++) {
          int c = s[i] - 'a';
          if (!nex[p][c]) nex[p][c] = ++cnt;  // 如果没有，就添加结点
          p = nex[p][c];
        }
        exist[p] = true;
      }
    
      bool find(char *s, int l) {  // 查找字符串
        int p = 0;
        for (int i = 0; i < l; i++) {
          int c = s[i] - 'a';
          if (!nex[p][c]) return 0;
          p = nex[p][c];
        }
        return exist[p];
      }
    };
    ```

=== "Python"
    ```python
    class trie:
        def __init__(self):
            self.nex = [[0 for i in range(26)] for j in range(100000)]
            self.cnt = 0
            self.exist = [False] * 100000  # 该结点结尾的字符串是否存在
    
        def insert(self, s):  # 插入字符串
            p = 0
            for i in s:
                c = ord(i) - ord("a")
                if not self.nex[p][c]:
                    self.cnt += 1
                    self.nex[p][c] = self.cnt  # 如果没有，就添加结点
                p = self.nex[p][c]
            self.exist[p] = True
    
        def find(self, s):  # 查找字符串
            p = 0
            for i in s:
                c = ord(i) - ord("a")
                if not self.nex[p][c]:
                    return False
                p = self.nex[p][c]
            return self.exist[p]
    ```

=== "Java"
    ```java
    public class Trie {
        int[][] tree = new int[10000][26];
        int cnt = 0;
        boolean[] end = new boolean[10000];
        
        public void insert(String word) {
            int p = 0;
            char[] chars = word.toCharArray();
            for (int i = 0; i < chars.length; i++) {
                int c = chars[i] - 'a';
                if (tree[p][c] == 0) {
                    tree[p][c] = ++cnt;
                }
                p = tree[p][c];
            }
            end[p] = true;
        }
        
        public boolean find(String word) {
            int p = 0;
            char[] chars = word.toCharArray();
            for (int i = 0; i < chars.length; i++) {
                int c = chars[i] - 'a';
                if (tree[p][c] == 0) {
                    return false;
                }
                p = tree[p][c];
            }
            return end[p];
        }
    }
    ```

## 应用

### 检索字符串

字典树最基础的应用——查找一个字符串是否在「字典」中出现过．

???+ note "[于是他错误的点名开始了](https://www.luogu.com.cn/problem/P2580)"
    给你 $n$ 个名字串，然后进行 $m$ 次点名，每次你需要回答「名字不存在」、「第一次点到这个名字」、「已经点过这个名字」之一．
    
    $1\le n\le 10^4$，$1\le m\le 10^5$，所有字符串长度不超过 $50$．
    
    ??? note "题解"
        对所有名字建 trie，再在 trie 中查询字符串是否存在、是否已经点过名，第一次点名时标记为点过名．
    
    ??? note "参考代码"
        ```cpp
        --8<-- "docs/string/code/trie/trie_1.cpp"
        ```

### AC 自动机

trie 是 [AC 自动机](./ac-automaton.md) 的一部分．

### 维护异或极值

将数的二进制表示看做一个字符串，就可以建出字符集为 $\{0,1\}$ 的 trie 树．

???+ note "[BZOJ1954 最长异或路径](https://hydro.ac/p/bzoj-P1954)"
    给你一棵带边权的树，求 $(u, v)$ 使得 $u$ 到 $v$ 的路径上的边权异或和最大，输出这个最大值．这里的异或和指的是所有边权的异或．
    
    点数不超过 $10^5$，边权在 $[0,2^{31})$ 内．
    
    ??? note "题解"
        随便指定一个根 $root$，用 $T(u, v)$ 表示 $u$ 和 $v$ 之间的路径的边权异或和，那么 $T(u,v)=T(root, u)\oplus T(root,v)$，因为 [LCA](../graph/lca.md) 以上的部分异或两次抵消了．
        
        那么，如果将所有 $T(root, u)$ 插入到一棵 trie 中，就可以对每个 $T(root, u)$ 快速求出和它异或和最大的 $T(root, v)$：
        
        从 trie 的根开始，如果能向和 $T(root, u)$ 的当前位不同的子树走，就向那边走，否则没有选择．
        
        贪心的正确性：如果这么走，这一位为 $1$；如果不这么走，这一位就会为 $0$．而高位是需要优先尽量大的．
    
    ??? note "参考代码"
        ```cpp
        --8<-- "docs/string/code/trie/trie_2.cpp"
        ```

### 维护异或和

01-trie 是指字符集为 $\{0,1\}$ 的 trie．01-trie 可以用来维护一些数字的异或和，支持修改（删除 + 重新插入），和全局加一（即：让其所维护所有数值递增 `1`，本质上是一种特殊的修改操作）．

如果要维护异或和，需要按值从低位到高位建立 trie．

**一个约定**：文中说当前节点 **往上** 指当前节点到根这条路径，当前节点 **往下** 指当前结点的子树．

#### 插入 & 删除

如果要维护异或和，我们 **只需要** 知道某一位上 `0` 和 `1` 个数的 **奇偶性** 即可，也就是对于数字 `1` 来说，当且仅当这一位上数字 `1` 的个数为奇数时，这一位上的数字才是 `1`，请时刻记住这段文字：如果只是维护异或和，我们只需要知道某一位上 `1` 的数量即可，而不需要知道 trie 到底维护了哪些数字．

对于每一个节点，我们需要记录以下三个量：

-   `ch[o][0/1]` 指节点 `o` 的两个儿子，`ch[o][0]` 指下一位是 `0`，同理 `ch[o][1]` 指下一位是 `1`．
-   `w[o]` 指节点 `o` 到其父亲节点这条边上数值的数量（权值）．每插入一个数字 `x`，`x` 二进制拆分后在 trie 上 路径的权值都会 `+1`．
-   `xorv[o]` 指以 `o` 为根的子树维护的异或和．

具体维护结点的代码如下所示．

```cpp
void maintain(int o) {
  w[o] = xorv[o] = 0;
  if (ch[o][0]) {
    w[o] += w[ch[o][0]];
    xorv[o] ^= xorv[ch[o][0]] << 1;
  }
  if (ch[o][1]) {
    w[o] += w[ch[o][1]];
    xorv[o] ^= (xorv[ch[o][1]] << 1) | (w[ch[o][1]] & 1);
  }
  // w[o] = w[o] & 1;
  // 只需知道奇偶性即可，不需要具体的值．当然这句话删掉也可以，因为上文就只利用了他的奇偶性．
}
```

插入和删除的代码非常相似．

需要注意的地方就是：

-   这里的 `MAXH` 指 trie 的深度，也就是强制让每一个叶子节点到根的距离为 `MAXH`．对于一些比较小的值，可能有时候不需要建立这么深（例如：如果插入数字 `4`，分解成二进制后为 `100`，从根开始插入 `001` 这三位即可），但是我们强制插入 `MAXH` 位．这样做的目的是为了便于全局 `+1` 时处理进位．例如：如果原数字是 `3`（`11`），递增之后变成 `4`（`100`），如果当初插入 `3` 时只插入了 `2` 位，那这里的进位就没了．

-   插入和删除，只需要修改叶子节点的 `w[]` 即可，在回溯的过程中一路维护即可．

???+ note "实现"
    ```cpp
    namespace trie {
    constexpr int MAXH = 21;
    int ch[_ * (MAXH + 1)][2], w[_ * (MAXH + 1)], xorv[_ * (MAXH + 1)];
    int tot = 0;
    
    int mknode() {
      ++tot;
      ch[tot][1] = ch[tot][0] = w[tot] = xorv[tot] = 0;
      return tot;
    }
    
    void maintain(int o) {
      w[o] = xorv[o] = 0;
      if (ch[o][0]) {
        w[o] += w[ch[o][0]];
        xorv[o] ^= xorv[ch[o][0]] << 1;
      }
      if (ch[o][1]) {
        w[o] += w[ch[o][1]];
        xorv[o] ^= (xorv[ch[o][1]] << 1) | (w[ch[o][1]] & 1);
      }
      w[o] = w[o] & 1;
    }
    
    void insert(int &o, int x, int dp) {
      if (!o) o = mknode();
      if (dp > MAXH) return (void)(w[o]++);
      insert(ch[o][x & 1], x >> 1, dp + 1);
      maintain(o);
    }
    
    void erase(int o, int x, int dp) {
      if (dp > 20) return (void)(w[o]--);
      erase(ch[o][x & 1], x >> 1, dp + 1);
      maintain(o);
    }
    }  // namespace trie
    ```

#### 全局加一

所谓全局加一就是指，让这棵 trie 中所有的数值 `+1`．

形式化的讲，设 trie 中维护的数值有 $V_1, V_2, V_3 \dots V_n$, 全局加一后 其中维护的值应该变成 $V_1+1, V_2+1, V_3+1 \dots V_n+1$

```cpp
void addall(int o) {
  swap(ch[o][0], ch[o][1]);
  if (ch[o][0]) addall(ch[o][0]);
  maintain(o);
}
```

##### 过程

我们思考一下二进制意义下 `+1` 是如何操作的．

我们只需要从低位到高位开始找第一个出现的 `0`，把它变成 `1`，然后这个位置后面的 `1` 都变成 `0` 即可．

下面给出几个例子感受一下：（括号内的数字表示其对应的十进制数字）

    1000(8)  + 1 = 1001(9)  ;
    10011(19) + 1 = 10100(20) ;
    11111(31) + 1 = 100000(32);
    10101(21) + 1 = 10110(22) ;
    100000000111111(16447) + 1 = 100000001000000(16448);

对应 trie 的操作，其实就是交换其左右儿子，顺着 **交换后** 的 `0` 边往下递归操作即可．

回顾一下 `w[o]` 的定义：`w[o]` 指节点 `o` 到其父亲节点这条边上数值的数量（权值）．

有没有感觉这个定义有点怪呢？如果在父亲结点存储到两个儿子的这条边的边权也许会更接近于习惯．但是在这里，在交换左右儿子的时候，在儿子结点存储到父亲这条边的距离，显然更加方便．

### 01-trie 合并

指的是将上述的两个 01-trie 进行合并，同时合并维护的信息．

可能关于合并 trie 的文章比较少，其实合并 trie 和合并线段树的思路非常相似，可以搜索「合并线段树」来学习如何合并 trie．

其实合并 trie 非常简单，就是考虑一下我们有一个 `int merge(int a, int b)` 函数，这个函数传入两个 trie 树位于同一相对位置的结点编号，然后合并完成后返回合并完成的结点编号．

#### 过程

考虑怎么实现？

分三种情况：

-   如果 `a` 没有这个位置上的结点，新合并的结点就是 `b`
-   如果 `b` 没有这个位置上的结点，新合并的结点就是 `a`
-   如果 `a`,`b` 都存在，那就把 `b` 的信息合并到 `a` 上，新合并的结点就是 `a`，然后递归操作处理 a 的左右儿子．

    **提示**：如果需要的合并是将 a，b 合并到一棵新树上，这里可以新建结点，然后合并到这个新结点上，这里的代码实现仅仅是将 b 的信息合并到 a 上．

#### 实现

```cpp
int merge(int a, int b) {
  if (!a) return b;  // 如果 a 没有这个位置上的结点，返回 b
  if (!b) return a;  // 如果 b 没有这个位置上的结点，返回 a
  /*
    如果 `a`, `b` 都存在，
    那就把 `b` 的信息合并到 `a` 上．
  */
  w[a] = w[a] + w[b];
  xorv[a] ^= xorv[b];
  /* 不要使用 maintain()，
    maintain() 是合并a的两个儿子的信息
    而这里需要 a b 两个节点进行信息合并
   */
  ch[a][0] = merge(ch[a][0], ch[b][0]);
  ch[a][1] = merge(ch[a][1], ch[b][1]);
  return a;
}
```

其实 trie 都可以合并，换句话说，trie 合并不仅仅限于 01-trie．

???+ note "[【luogu-P6018】【Ynoi2010】Fusion tree](https://www.luogu.com.cn/problem/P6018)"
    给你一棵 $n$ 个结点的树，每个结点有权值．$m$ 次操作．
    需要支持以下操作．
    
    -   将树上与一个节点 $x$ 距离为 $1$ 的节点上的权值 $+1$．这里树上两点间的距离定义为从一点出发到另外一点的最短路径上边的条数．
    
    -   在一个节点 $x$ 上的权值 $-v$．
    
    -   询问树上与一个节点 $x$ 距离为 $1$ 的所有节点上的权值的异或和．
        对于 $100\%$ 的数据，满足 $1\le n \le 5\times 10^5$，$1\le m \le 5\times 10^5$，$0\le a_i \le 10^5$，$1 \le x \le n$，$opt\in\{1,2,3\}$．
        保证任意时刻每个节点的权值非负．
    
    ??? note "题解"
        每个结点建立一棵 trie 维护其儿子的权值，trie 应该支持全局加一．
        可以使用在每一个结点上设置懒标记来标记儿子的权值的增加量．
    
    ??? note "参考代码"
        ```cpp
        --8<-- "docs/string/code/trie/trie_3.cpp"
        ```

???+ note "[【luogu-P6623】【省选联考 2020 A 卷】树](https://www.luogu.com.cn/problem/P6623)"
    给定一棵 $n$ 个结点的有根树 $T$，结点从 $1$ 开始编号，根结点为 $1$ 号结点，每个结点有一个正整数权值 $v_i$．
    设 $x$ 号结点的子树内（包含 $x$ 自身）的所有结点编号为 $c_1,c_2,\dots,c_k$，定义 $x$ 的价值为：  
    $val(x)=(v_{c_1}+d(c_1,x)) \oplus (v_{c_2}+d(c_2,x)) \oplus \cdots \oplus (v_{c_k}+d(c_k, x))$ 其中 $d(x,y)$．  
    表示树上 $x$ 号结点与 $y$ 号结点间唯一简单路径所包含的边数，$d(x,x) = 0$．$\oplus$ 表示异或运算．
    请你求出 $\sum\limits_{i=1}^n val(i)$ 的结果．
    
    ??? note "题解"
        考虑每个结点对其所有祖先的贡献．
        每个结点建立 trie，初始先只存这个结点的权值，然后从底向上合并每个儿子结点上的 trie，然后再全局加一，完成后统计答案．
    
    ??? note "参考代码"
        ```cpp
        constexpr int _ = 526010;
        int n;
        int V[_];
        int debug = 0;
        
        namespace trie {
        constexpr int MAXH = 21;
        int ch[_ * (MAXH + 1)][2], w[_ * (MAXH + 1)], xorv[_ * (MAXH + 1)];
        int tot = 0;
        
        int mknode() {
          ++tot;
          ch[tot][1] = ch[tot][0] = w[tot] = xorv[tot] = 0;
          return tot;
        }
        
        void maintain(int o) {
          w[o] = xorv[o] = 0;
          if (ch[o][0]) {
            w[o] += w[ch[o][0]];
            xorv[o] ^= xorv[ch[o][0]] << 1;
          }
          if (ch[o][1]) {
            w[o] += w[ch[o][1]];
            xorv[o] ^= (xorv[ch[o][1]] << 1) | (w[ch[o][1]] & 1);
          }
          w[o] = w[o] & 1;
        }
        
        void insert(int &o, int x, int dp) {
          if (!o) o = mknode();
          if (dp > MAXH) return (void)(w[o]++);
          insert(ch[o][x & 1], x >> 1, dp + 1);
          maintain(o);
        }
        
        int merge(int a, int b) {
          if (!a) return b;
          if (!b) return a;
          w[a] = w[a] + w[b];
          xorv[a] ^= xorv[b];
          ch[a][0] = merge(ch[a][0], ch[b][0]);
          ch[a][1] = merge(ch[a][1], ch[b][1]);
          return a;
        }
        
        void addall(int o) {
          swap(ch[o][0], ch[o][1]);
          if (ch[o][0]) addall(ch[o][0]);
          maintain(o);
        }
        }  // namespace trie
        
        int rt[_];
        long long Ans = 0;
        vector<int> E[_];
        
        void dfs0(int o) {
          for (int i = 0; i < E[o].size(); i++) {
            int node = E[o][i];
            dfs0(node);
            rt[o] = trie::merge(rt[o], rt[node]);
          }
          trie::addall(rt[o]);
          trie::insert(rt[o], V[o], 0);
          Ans += trie::xorv[rt[o]];
        }
        
        int main() {
          n = read();
          for (int i = 1; i <= n; i++) V[i] = read();
          for (int i = 2; i <= n; i++) E[read()].push_back(i);
          dfs0(1);
          printf("%lld", Ans);
          return 0;
        }
        ```

### 可持久化字典树

参见 [可持久化字典树](../ds/persistent-trie.md)．


## string/z-func.md

author: LeoJacob, Marcythm, minghu6

约定：字符串下标以 $0$ 为起点．

## 定义

对于一个长度为 $n$ 的字符串 $s$，定义函数 $z[i]$ 表示 $s$ 和 $s[i,n-1]$（即以 $s[i]$ 开头的后缀）的最长公共前缀（LCP）的长度，则 $z$ 被称为 $s$ 的 **Z 函数**．特别地，$z[0] = 0$．

国外一般将计算该数组的算法称为 **Z Algorithm**，而国内则称其为 **扩展 KMP**（exKMP）．

这篇文章介绍在 $O(n)$ 时间复杂度内计算 Z 函数的算法以及其各种应用．

## 解释

下面若干样例展示了对于不同字符串的 Z 函数：

-   $z(\mathtt{aaaaa}) = [0, 4, 3, 2, 1]$
-   $z(\mathtt{aaabaab}) = [0, 2, 1, 0, 2, 1, 0]$
-   $z(\mathtt{abacaba}) = [0, 0, 1, 0, 3, 0, 1]$

## 朴素算法

Z 函数的朴素算法复杂度为 $O(n^2)$：

???+ note "实现"
    === "C++"
        ```cpp
        vector<int> z_function_trivial(string s) {
          int n = (int)s.length();
          vector<int> z(n);
          for (int i = 1; i < n; ++i)
            while (i + z[i] < n && s[z[i]] == s[i + z[i]]) ++z[i];
          return z;
        }
        ```
    
    === "Python"
        ```python
        def z_function_trivial(s):
            n = len(s)
            z = [0] * n
            for i in range(1, n):
                while i + z[i] < n and s[z[i]] == s[i + z[i]]:
                    z[i] += 1
            return z
        ```

## 线性算法

如同大多数字符串主题所介绍的算法，其关键在于，运用自动机的思想寻找限制条件下的状态转移函数，使得可以借助之前的状态来加速计算新的状态．

在该算法中，我们从 $1$ 到 $n-1$ 顺次计算 $z[i]$ 的值（$z[0]=0$）．在计算 $z[i]$ 的过程中，我们会利用已经计算好的 $z[0],\ldots,z[i-1]$．

对于 $i$，我们称区间 $[i,i+z[i]-1]$ 是 $i$ 的 **匹配段**，也可以叫 Z-box．

算法的过程中我们维护右端点最靠右的匹配段．为了方便，记作 $[l,r]$．根据定义，$s[l,r]$ 是 $s$ 的前缀．在计算 $z[i]$ 时我们保证 $l\le i$．初始时 $l=r=0$．

在计算 $z[i]$ 的过程中：

-   如果 $i\le r$，那么根据 $[l,r]$ 的定义有 $s[i,r] = s[i-l,r-l]$，因此 $z[i]\ge \min(z[i-l],r-i+1)$．这时：
    -   若 $z[i-l] < r-i+1$，则 $z[i] = z[i-l]$．
    -   否则 $z[i-l]\ge r-i+1$，这时我们令 $z[i] = r-i+1$，然后暴力枚举下一个字符扩展 $z[i]$ 直到不能扩展为止．
-   如果 $i>r$，那么我们直接按照朴素算法，从 $s[i]$ 开始比较，暴力求出 $z[i]$．
-   在求出 $z[i]$ 后，如果 $i+z[i]-1>r$，我们就需要更新 $[l,r]$，即令 $l=i, r=i+z[i]-1$．

可以访问 [这个网站](https://personal.utdallas.edu/~besp/demo/John2010/z-algorithm.htm) 来看 Z 函数的模拟过程．

### 实现

=== "C++"
    ```cpp
    vector<int> z_function(string s) {
      int n = (int)s.length();
      vector<int> z(n);
      for (int i = 1, l = 0, r = 0; i < n; ++i) {
        if (i <= r && z[i - l] < r - i + 1) {
          z[i] = z[i - l];
        } else {
          z[i] = max(0, r - i + 1);
          while (i + z[i] < n && s[z[i]] == s[i + z[i]]) ++z[i];
        }
        if (i + z[i] - 1 > r) l = i, r = i + z[i] - 1;
      }
      return z;
    }
    ```

=== "Python"
    ```python
    def z_function(s):
        n = len(s)
        z = [0] * n
        l, r = 0, 0
        for i in range(1, n):
            if i <= r and z[i - l] < r - i + 1:
                z[i] = z[i - l]
            else:
                z[i] = max(0, r - i + 1)
                while i + z[i] < n and s[z[i]] == s[i + z[i]]:
                    z[i] += 1
            if i + z[i] - 1 > r:
                l = i
                r = i + z[i] - 1
        return z
    ```

## 复杂度分析

对于内层 `while` 循环，每次执行都会使得 $r$ 向后移至少 $1$ 位，而 $r< n-1$，所以总共只会执行 $n$ 次．

对于外层循环，只有一遍线性遍历．

总复杂度为 $O(n)$．

## 应用

我们现在来考虑在若干具体情况下 Z 函数的应用．

这些应用在很大程度上同 [前缀函数](./kmp.md) 的应用类似．

### 匹配所有子串

为了避免混淆，我们将 $t$ 称作 **文本**，将 $p$ 称作 **模式**．所给出的问题是：寻找在文本 $t$ 中模式 $p$ 的所有出现（occurrence）．

为了解决该问题，我们构造一个新的字符串 $s = p + \diamond + t$，也即我们将 $p$ 和 $t$ 连接在一起，但是在中间放置了一个分割字符 $\diamond$（我们将如此选取 $\diamond$ 使得其必定不出现在 $p$ 和 $t$ 中）．

首先计算 $s$ 的 Z 函数．接下来，对于在区间 $[0,|t| - 1]$ 中的任意 $i$，我们考虑以 $t[i]$ 为开头的后缀在 $s$ 中的 Z 函数值 $k = z[i + |p| + 1]$．如果 $k = |p|$，那么我们知道有一个 $p$ 的出现位于 $t$ 的第 $i$ 个位置，否则没有 $p$ 的出现位于 $t$ 的第 $i$ 个位置．

其时间复杂度（同时也是其空间复杂度）为 $O(|t| + |p|)$．

### 本质不同子串数

给定一个长度为 $n$ 的字符串 $s$，计算 $s$ 的本质不同子串的数目．

考虑计算增量，即在知道当前 $s$ 的本质不同子串数的情况下，计算出在 $s$ 末尾添加一个字符后的本质不同子串数．

令 $k$ 为当前 $s$ 的本质不同子串数．我们添加一个新的字符 $c$ 至 $s$ 的末尾．显然，会出现一些以 $c$ 结尾的新的子串（以 $c$ 结尾且之前未出现过的子串）．

设串 $t$ 是 $s + c$ 的反串（反串指将原字符串的字符倒序排列形成的字符串）．我们的任务是计算有多少 $t$ 的前缀未在 $t$ 的其他地方出现．考虑计算 $t$ 的 Z 函数并找到其最大值 $z_{\max}$．则 $t$ 的长度小于等于 $z_{\max}$ 的前缀的反串在 $s$ 中是已经出现过的以 $c$ 结尾的子串．

所以，将字符 $c$ 添加至 $s$ 后新出现的子串数目为 $|t| - z_{\max}$．

算法时间复杂度为 $O(n^2)$．

值得注意的是，我们可以用同样的方法在 $O(n)$ 时间内，重新计算在端点处添加一个字符或者删除一个字符（从尾或者头）后的本质不同子串数目．

### 字符串整周期

给定一个长度为 $n$ 的字符串 $s$，找到其最短的整周期，即寻找一个最短的字符串 $t$，使得 $s$ 可以被若干个 $t$ 拼接而成的字符串表示．

考虑计算 $s$ 的 Z 函数，则其整周期的长度为最小的 $n$ 的因数 $i$，满足 $i+z[i]=n$．

该事实的证明同应用 [前缀函数](./kmp.md) 的证明一样．

## 练习题目

-   [luogu P5410【模板】扩展 KMP/exKMP（Z 函数）](https://www.luogu.com.cn/problem/P5410)
-   [luogu P7114【NOIP2020】字符串匹配](https://www.luogu.com.cn/problem/P7114)
-   [CF126B Password](http://codeforces.com/problemset/problem/126/B)
-   [UVa # 455 Periodic Strings](http://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=396)
-   [UVa # 11022 String Factoring](http://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=1963)
-   [UVa 11475 - Extend to Palindrome](http://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&category=24&page=show_problem&problem=2470)
-   [Codechef - Chef and Strings](https://www.codechef.com/problems/CHSTR)
-   [Codeforces - Prefixes and Suffixes](http://codeforces.com/problemset/problem/432/D)
-   [Leetcode 2223 - Sum of Scores of Built Strings](https://leetcode.com/problems/sum-of-scores-of-built-strings/)

**本页面主要译自博文 [Z-функция строки и её вычисление](http://e-maxx.ru/algo/z_function) 与其英文翻译版 [Z-function and its calculation](https://cp-algorithms.com/string/z-function.html)．其中俄文版版权协议为 Public Domain + Leave a Link；英文版版权协议为 CC-BY-SA 4.0．**
