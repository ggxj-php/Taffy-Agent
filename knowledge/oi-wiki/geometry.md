

## geometry/2d.md

我们将需要解决的几何问题的范围限制在二维平面内，这样就涉及到二维计算几何的基本知识．在研究时，通常把图形放在平面直角坐标系或极坐标系下，这样解决问题就会方便很多．

## 前置技能

如并不了解：

-   几何基础
-   平面直角坐标系
-   向量（包括向量积）
-   极坐标与极坐标系

请先阅读 [向量](../math/linear-algebra/vector.md) 和 [极坐标](../math/coordinate.md#平面极坐标系)．

## 图形的记录

### 点

在平面直角坐标系下，点用横纵坐标表示，比如点 $(5,2)$，点 $(-1,0)$ 等．由于坐标是有序数对，因此可以利用 [`std::pair`](https://en.cppreference.com/w/cpp/utility/pair.html) 存储，也可以定义结构体存储．

在极坐标系下，点用极径与极角表示，使用类似于直角坐标系的存储方式进行存储即可．

### 向量

由于向量的坐标表示与点相同，所以只需要像点一样存储向量即可．

在极坐标系下，与点同理．

### 线

在极坐标系中表示线是较为困难的，因此我们仅讨论直角坐标系中的情况．

#### 直线与射线

一般在求解数学问题时，我们用解析式表示一条直线．直线的解析式有一般式 $Ax+By+C=0$、斜截式 $y=kx+b$、截距式 $\dfrac{x}{a}+\dfrac{y}{b}=1$ 等多种形式，但其形式最终服务于方程求解析解．在解决一些计算几何问题中，使用解析式表示直线会增加解决问题的难度．

在计算几何中，通常使用直线上一点与直线的方向向量表示一条直线，用射线的端点与射线的方向向量表示一条射线．方向向量是一个与直线平行的非零向量，通常情况下取单位向量．与一条直线平行的单位向量有两个，可以根据题目选择任意一个；而对于射线，方向向量通常取方向与射线延伸方向相同的那个．

#### 线段

记录一条线段只需要记录其左右端点即可．

### 多边形

使用数组按一定顺序记录多边形的每个顶点即可．对于简单多边形，一般按顺时针或逆时针顺序记录各个顶点．

特殊地，记录矩形时，如果矩形的各边均与坐标轴平行，只需记录其对角线上的两个顶点．

### 曲线图形

一些特殊曲线，如函数图像等一般记录其解析式．对于圆，直接记录其圆心和半径即可．

## 基本公式

### 正弦定理

在 $\triangle \text{ABC}$ 中，若角 $A,B,C$ 所对边分别为 $a,b,c$，则有：

$$
\frac{a}{\sin A}=\frac{b}{\sin B}=\frac{c}{\sin C}=2R
$$

其中，$R$ 为 $\triangle \text{ABC}$ 的外接圆半径．

### 余弦定理

在 $\triangle \text{ABC}$ 中，若角 $A,B,C$ 所对边分别为 $a,b,c$，则有：

$$
\begin{aligned}
a^2&=b^2+c^2-2bc\cos A\\
b^2&=a^2+c^2-2ac\cos B\\
c^2&=a^2+b^2-2ab\cos C
\end{aligned}
$$

上述公式的证明略．均为人教版高中数学 A 版必修二内容（旧教材为必修五）．

## 基本操作

### 判断一个点在直线的哪边

我们有直线上的一点 $P$ 的直线的方向向量 $\mathbf v$，想知道某个点 $Q$ 在直线的哪边．这里所指的「哪边」是相对于方向向量的，也就是说，判断时我们面朝方向向量所指的方向进行判断．

我们利用向量积的性质，算出 $\mathbf v\times \overrightarrow {PQ}$．根据右手定则，如果向量积为负，则 $Q$ 在直线右侧；如果向量积为 $0$，则 $Q$ 在直线上；如果向量积为正，则 $Q$ 在直线左侧．

### 快速排斥实验与跨立实验

我们现在想判断两条线段是否相交．

首先特判一些特殊情况．如果两线段平行，自然不能相交．这种情况通过判断线段所在直线的斜率是否相等即可．

当然，如果两线段重合或部分重合，或者两线段的交点为其中一条线段的端点，只需要判断是否有三点共线的情况即可．

还有些显然不相交的情况，我们口头上称之为「两条线段离着太远了」．规定「一条线段的区域」为以这条线段为对角线的，各边均与某一坐标轴平行的矩形所占的区域，那么可以发现，如果两条线段没有公共区域，则这两条线段一定不相交．

比如有以下两条线段：

![Seg1](./images/2d-seg1.svg)

它们占用的区域是这样的：

![Seg2](./images/2d-seg2.svg)

于是可以快速地判断出来这两条线段不相交．

这就是 **快速排斥实验**．上述情况称作 **未通过快速排斥实验**．

未通过快速排斥实验是两线段无交点的 **充分不必要条件**，我们还需要进一步判断．

因为两线段 $a,b$ 相交，$b$ 线段的两个端点一定分布在 $a$ 线段所在直线两侧；同理，$a$ 线段的两个端点一定分布在 $b$ 线段所在直线两侧．我们可以直接判断一条线段的两个端点相对于另一线段所在直线的位置关系，如果不同，则两线段相交，反之则不相交．如上一节所说，直线与点的位置关系我们可以利用向量积判断．

这就是 **跨立实验**，如果对于两线段 $a,b$，$b$ 线段的两个端点分布在 $a$ 线段所在直线的两侧，**且**  $a$ 线段的两个端点分布在 $b$ 线段所在直线的两侧，我们就说 $a,b$ 两线段 **通过了跨立实验**，即两线段相交．

注意到当两条线段共线但不相交时也可以通过跨立实验，因此想要准确判断还需要与快速排斥实验结合．

### 判断一点是否在多边形内部

在计算几何中，这个问题被称为 [PIP 问题](https://en.wikipedia.org/wiki/Point_in_polygon)，已经有一些成熟的解决方法，下面依次介绍．

#### 光线投射算法 (Ray casting algorithm)

在 [这里](https://wrfranklin.org/Research/Short_Notes/pnpoly.html) 可以看到最原始的思路．

我们先特判一些特殊情况，比如「这个点离多边形太远了」．类似判断两条线段相交，考虑一个能够完全覆盖该多边形的最小矩形，如果这个点不在这个矩形范围内，那么这个点一定不在多边形内．这样的矩形很好求，只需要知道多边形横坐标与纵坐标的最小值和最大值，坐标两两组合成四个点，就是这个矩形的四个顶点了．

还有点在多边形的某一边或某顶点上，同样十分容易判断．对于每条边，检查点是否在边上或顶点上即可．

我们考虑以该点为端点引出一条射线，如果这条射线与多边形有奇数个交点，则该点在多边形内部，否则该点在多边形外部，我们简记为 **奇内偶外**．这个算法同样被称为奇偶规则 (Even-odd rule)．

由于 [Jordan curve theorem](https://en.wikipedia.org/wiki/Jordan_curve_theorem)，我们知道，这条射线每次与多边形的一条边相交，就切换一次与多边形的内外关系，所以统计交点数的奇偶即可．

对于选取的射线，可以随机选取这条射线所在直线的斜率，建议为无理数以避免出现射线与多边形某边重合的情况．

在原版代码中，使用的是记录多边形的数组中最后一个点作为射线上一点，这样统计时，如果出现射线过多边形某边或某顶点时，可以规定射线经过的点同在射线一侧，进而做跨立实验即可．

???+ warning "注意"
    光线投射算法只适用于简单多边形．对于边自交的多边形并不适用 Jordan curve theorem，因此无法判断．

#### 回转数算法 (Winding number algorithm)

回转数是数学上的概念，是平面内闭合曲线逆时针绕过该点的总次数．很容易发现，当回转数等于 $0$ 的时候，点在曲线外部．这个算法同样被称为非零规则 (Nonzero-rule)．

如何计算呢？我们把该点与多边形的所有顶点连接起来，计算相邻两边夹角的和．注意这里的夹角是 **有方向的**．如果夹角和为 $0$，则这个点在多边形外，否则在多边形内．

### 求两条直线的交点

首先，我们需要确定两条直线相交，只需判断一下两条直线的方向向量是否平行即可．如果方向向量平行，则两条直线平行，交点个数为 $0$．进一步地，若两条直线平行且过同一点，则两直线重合．

那么，问题简化为我们有直线 $AB,CD$ 交于一点，想求出交点 $E$．

如果两直线相交，则交点只有一个，我们记录了直线上的一个点和直线的方向向量，所以我们只需要知道这个点与交点的距离 $l$，再将这个点沿方向向量平移 $l$ 个单位长度即可．

考虑构造三角形，利用正弦定理求解 $l$，可以利用向量积构造出正弦定理．

![Intersection](./images/2d-intersection.svg)

由上图可知，$|\mathbf a\times \mathbf b|=|\mathbf a||\mathbf b|\sin \beta$，$|\mathbf u\times \mathbf b|=|\mathbf u||\mathbf b|\sin \theta$．

作商得：

$$
T=\frac{|\mathbf u\times \mathbf b|}{|\mathbf a\times \mathbf b|}=\frac{|\mathbf u|\sin \theta}{|\mathbf a|\sin \beta}
$$

可以看出，$\left|\dfrac{|\mathbf u|\sin \theta}{\sin \beta}\right|=l$．若绝对值内部式子取值为正，代表沿 $\mathbf a$ 方向平移，反之则为反方向．

同时，我们将 $T$ 直接乘上 $\mathbf a$，就自动出现了直线的单位向量，不需要进行其他消去操作了．

于是，只需要将点 $B$ 减去 $T\mathbf a$ 即可得出交点．

### 求任意多边形的周长和面积

#### 求任意多边形的周长

直接计算即可，简洁即美德．

#### 求任意多边形的面积

考虑向量积的模的几何意义，我们可以利用向量积完成．

将多边形上的点逆时针标记为 $p_1,p_2,\cdots ,p_n$，再任选一个辅助点 $O$，记向量 $\mathbf v_i=p_i-O$，那么这个多边形面积 $S$ 可以表示为：

$$
S=\frac{1}{2}\left|\sum_{i=1}^n \mathbf v_i\times \mathbf v_{(i\bmod n)+1}\right|
$$

### 圆与直线相关

#### 求直线与圆的交点

首先判断直线与圆的位置关系．如果直线与圆相离则无交点，若相切则可以利用切线求出切点与半径所在直线，之后转化为求两直线交点．

若有两交点，则可以利用勾股定理求出两交点的中点，然后沿直线方向加上半弦长即可．

#### 求两圆交点

首先我们判断一下两个圆的位置关系，如果外离或内含则无交点，如果相切，可以算出两圆心连线的方向向量，然后利用两圆半径计算出平移距离，最后将圆心沿这个方向向量进行平移即可．

如果两圆相交，则必有两个交点，并且关于两圆心连线对称．因此下面只说明一个交点的求法，另一个交点可以用类似方法求出．

我们先将一圆圆心与交点相连，求出两圆心连线与该连线所成角．这样，将两圆心连线的方向向量旋转这个角度，就是圆心与交点相连形成的半径的方向向量了．沿方向向量方向将圆心平移半径长度即可得到一个交点．

## 极角序

一般来说，这类题需要先枚举一个极点，然后计算出其他点的极坐标，在极坐标系下按极角的顺序解决问题．

???+ example "[「JOISC 2014 Day4」两个人的星座](https://loj.ac/p/2882)"
    平面内有 $n$ 个点，有三种颜色，每个点的颜色是三种中的一种．求不相交的三色三角形对数．$6\le n\le 3000$．

??? note "题解"
    如果两个三角形不相交，则一定可以做出两条内公切线，如果相交或内含是做不出内公切线的．三角形的公切线可以类比圆的公切线．
    
    先枚举一个原点，记为 $O$，以这个点为极点，过这个点且与 $x$ 轴平行的直线作为极轴，建立极坐标系，把剩余点按极角由小到大排序．然后统计出在极轴上方和下方的每种点的个数．
    
    然后根据点枚举公切线，记枚举到的点为 $P$，初始时公切线为极轴．开始统计．那么一定存在一条公切线过点 $O$ 和点 $P$．因为公切线与三角形不相交，所以一方选择公切线上方的点，另一方一定选择下方的点．然后利用乘法原理统计方案数即可．
    
    统计完后旋转公切线，那么点 $P$ 一定改变了相对于公切线的上下位置，而其他点不动，应该只将它的位置信息改变．这样，可以发现，同一对三角形最终被统计了 $4$ 次，就是同一条公切线会被枚举两次，最后做出的答案应除以 $4$．
    
    分析一下算法复杂度．我们枚举了一个原点，然后对于每一个原点将剩余点排序后线性统计，因此时间复杂度为 $O(n^2\log n)$．

## 代码编写注意事项

由于计算几何经常进行 `double` 类型的浮点数计算，因此带来了精度问题和时间问题．

有些问题，例如求点坐标均为整数的三角形面积，可以利用其特殊性进行纯整数计算，避免用浮点数影响精度．

由于浮点数的读入与计算都比整数慢，所以需要注意程序的常数因子给时间带来的影响．


## geometry/3d.md

author: shuzhouliu

三维几何的很多概念与 [二维几何](./2d.md) 是相通的，我们可以用与解决二维几何问题相同的方法来解决三维几何问题．

## 基本概念

点，向量，直线这些概念和二维几何是相似的，这里不再展开．

### 平面

我们可以用平面上的一点 $P_0(x_0,y_0,z_0)$ 和该平面的法向量（即垂直于该平面的向量）$\boldsymbol{n}$ 来表示一个平面．

因为 $\boldsymbol{n}$ 垂直于平面，所以 $\boldsymbol{n}$ 垂直于该平面内的所有直线．换句话说，设 $\boldsymbol{n}=(A,B,C)$，则该平面上的点 $P(x,y,z)$ 都满足 $\boldsymbol{n} \cdot \overrightarrow{PP_0} = 0$．

根据向量点积的定义，上式等价于：

$$
A(x-x_0)+B(y-y_0)+C(z-z_0)=0
$$

整理后得到：

$$
Ax+By+Cz-(Ax_0+By_0+Cz_0)=0
$$

令 $D=-(Ax_0+By_0+Cz_0)$，则上式变成 $Ax+By+Cz+D=0$．我们称这个式子为平面的 **一般式**．

## 基本操作

### 直线、平面之间的夹角

运用空间向量的知识，空间中直线、平面之间的夹角可以很快求出．

对于两条异面直线 $a$，$b$，过空间中一点 $P$，作 $a' \parallel a$，$b' \parallel b'$，则 $a'$ 与 $b'$ 所成的锐角或直角被称为 $a$ 和 $b$ 两条 **异面直线所成的角**．

对于直线 $a$ 和平面 $\alpha$，若 $a$ 与 $\alpha$ 相交于 $A$，过 $a$ 上一点 $P$ 引平面 $\alpha$ 的垂线交 $\alpha$ 于 $O$，则 $a$ 与 $PO$ 所成角的余角被称为 **直线与平面所成的角**．特别地，若 $a \parallel \alpha$ 或 $a \subset \alpha$，则它们之间的夹角为 $0^\circ$．

对于两个平面 $\alpha$，$\beta$，它们的夹角被定义为与两条平面的交线 $l$ 垂直的两条直线 $a,b$（其中 $a \subset \alpha$，$b \subset \beta$）所成的角．

#### 两直线夹角定义与关系充要条件

-   两直线的方向向量的夹角，叫做两直线的夹角．

有了这个命题，我们就可以得出以下结论：已知两条直线 $l_1, l_2$，它们的方向向量分别是 $s_1 (m_1, n_1, p_1)$，$s_2 (m_2, n_2, p_2)$，设 $\varphi$ 为两直线夹角，我们可以得到 $\cos \varphi = \dfrac{\left | m_1m_2+n_1n_2+p_1p_2 \right |}{\sqrt{m_1^2+n_1^2+p_1^2}\sqrt{m_2^2+n_2^2+p_2^2}}$.

-   $l_1 \perp l_2 \iff m_1m_2 + n_1n_2 + p_1p_2 = 0$

-   $l_1 \parallel l_2 \iff \dfrac{m_1}{m_2} = \dfrac{n_1}{n_2} = \dfrac{p_1}{p_2}$.

### 三维向量与平面的夹角

当直线与平面不垂直时，直线和它在平面上的投影直线的夹角 $\varphi$（$\varphi \in [0, \frac{\pi}{2}]$）称为直线与平面的夹角．

设直线向量 $s(m, n, p)$，平面法线向量 $f(a, b, c)$，那么以下命题成立：

-   角度的正弦值：$\sin\varphi = \dfrac{\left | am + bn + cp \right |}{\sqrt{a^2+b^2+c^2}\sqrt{m^2+n^2+p^2}}$

-   直线与平面平行 $\iff am+bn+cp = 0$

-   直线与平面垂直 $\iff \dfrac{a}{m} = \dfrac{b}{n} = \dfrac{c}{p}$

### 点到平面的距离

### 直线与平面的交点

直接联立直线方程和平面方程即可．

## 立体几何定理

### 三正弦定理

设二面角 $M－AB－N$ 的度数为 $\alpha$，在平面 $M$ 上有一条射线 $AC$，它和棱 $AB$ 所成角为 $\beta$，和平面 $N$ 所成的角为 $\gamma$，则 $\sin\gamma = \sin\alpha\cdot\sin\beta$．

### 三余弦定理

设 $O$ 为平面上一点，过平面外一点 $B$ 的直线 $BO$ 在面上的射影为 $AO$，$OC$ 为面上的一条直线，那么 $\angle COB，\angle AOC，\angle AOB$ 三角的余弦关系为：$\cos\angle BOC=\cos\angle AOB\cdot\cos\angle AOC$（$\angle AOC$，$\angle AOB$ 只能是锐角）．

## 参考资料

-   [3D 空间基础概念之一：点、向量（矢量）和齐次坐标](https://www.cnblogs.com/CodeBlove/articles/1319563.html)


## geometry/convex-hull.md

## 二维凸包

### 定义

#### 凸多边形

凸多边形是指所有内角大小都在 $[0,\pi]$ 范围内的 **简单多边形**．

#### 凸包

在平面上能包含所有给定点的最小凸多边形叫做凸包．

其定义为：对于给定集合 $X$，所有包含 $X$ 的凸集的交集 $S$ 被称为 $X$ 的 **凸包**．

实际上可以理解为用一个橡皮筋包含住所有给定点的形态．

凸包用最小的周长围住了给定的所有点．如果一个凹多边形围住了所有的点，它的周长一定不是最小，如下图．根据三角不等式，凸多边形在周长上一定是最优的．

![](./images/ch.png)

### Andrew 算法求凸包

常用的求法有 Graham 扫描法和 Andrew 算法，这里主要介绍 Andrew 算法．

#### 性质

该算法的时间复杂度为 $O(n\log n)$，其中 $n$ 为待求凸包点集的大小，复杂度的瓶颈在于对所有点坐标的双关键字排序．

#### 过程

首先把所有点以横坐标为第一关键字，纵坐标为第二关键字排序．

显然排序后最小的元素和最大的元素一定在凸包上．而且因为是凸多边形，我们如果从一个点出发逆时针走，轨迹总是「左拐」的，一旦出现右拐，就说明这一段不在凸包上．因此我们可以用一个单调栈来维护上下凸壳．

因为从左向右看，上下凸壳所旋转的方向不同，为了让单调栈起作用，我们首先 **升序枚举** 求出下凸壳，然后 **降序** 求出上凸壳．

求凸壳时，一旦发现即将进栈的点（$P$）和栈顶的两个点（$S_1,S_2$，其中 $S_1$ 为栈顶）行进的方向向右旋转，即叉积小于 $0$：$\overrightarrow{S_2S_1}\times \overrightarrow{S_1P}<0$，则弹出栈顶，回到上一步，继续检测，直到 $\overrightarrow{S_2S_1}\times \overrightarrow{S_1P}\ge 0$ 或者栈内仅剩一个元素为止．

通常情况下不需要保留位于凸包边上的点，因此上面一段中 $\overrightarrow{S_2S_1}\times \overrightarrow{S_1P}<0$ 这个条件中的「$<$」可以视情况改为 $\le$，同时后面一个条件应改为 $>$．

![Andrew](./images/andrew.svg)

#### 实现

???+ note "代码实现"
    === "C++"
        ```cpp
        // stk[] 是整型，存的是下标
        // p[] 存储向量或点
        tp = 0;                       // 初始化栈
        std::sort(p + 1, p + 1 + n);  // 对点进行排序
        stk[++tp] = 1;
        // 栈内添加第一个元素，且不更新 used，使得 1 在最后封闭凸包时也对单调栈更新
        for (int i = 2; i <= n; ++i) {
          while (tp >= 2  // 下一行 * 操作符被重载为叉积
                 && (p[stk[tp]] - p[stk[tp - 1]]) * (p[i] - p[stk[tp]]) <= 0)
            used[stk[tp--]] = 0;
          used[i] = 1;  // used 表示在凸壳上
          stk[++tp] = i;
        }
        int tmp = tp;  // tmp 表示下凸壳大小
        for (int i = n - 1; i > 0; --i)
          if (!used[i]) {
            // ↓求上凸壳时不影响下凸壳
            while (tp > tmp && (p[stk[tp]] - p[stk[tp - 1]]) * (p[i] - p[stk[tp]]) <= 0)
              used[stk[tp--]] = 0;
            used[i] = 1;
            stk[++tp] = i;
          }
        for (int i = 1; i <= tp; ++i)  // 复制到新数组中去
          h[i] = p[stk[i]];
        int ans = tp - 1;
        ```
    
    === "Python"
        ```python
        stk = []  # 是整型，存的是下标
        p = []  # 存储向量或点
        tp = 0  # 初始化栈
        p.sort()  # 对点进行排序
        tp = tp + 1
        stk[tp] = 1
        # 栈内添加第一个元素，且不更新 used，使得 1 在最后封闭凸包时也对单调栈更新
        for i in range(2, n + 1):
            while tp >= 2 and (p[stk[tp]] - p[stk[tp - 1]]) * (p[i] - p[stk[tp]]) <= 0:
                # 下一行 * 操作符被重载为叉积
                used[stk[tp]] = 0
                tp = tp - 1
            used[i] = 1  # used 表示在凸壳上
            tp = tp + 1
            stk[tp] = i
        tmp = tp  # tmp 表示下凸壳大小
        for i in range(n - 1, 0, -1):
            if used[i] == False:
                #      ↓求上凸壳时不影响下凸壳
                while tp > tmp and (p[stk[tp]] - p[stk[tp - 1]]) * (p[i] - p[stk[tp]]) <= 0:
                    used[stk[tp]] = 0
                    tp = tp - 1
                used[i] = 1
                tp = tp + 1
                stk[tp] = i
        for i in range(1, tp + 1):
            h[i] = p[stk[i]]
        ans = tp - 1
        ```

根据上面的代码，最后凸包上有 $\textit{ans}$ 个元素（额外存储了 $1$ 号点，因此 $h$ 数组中有 $\textit{ans}+1$ 个元素），并且按逆时针方向排序．周长就是

$$
\sum_{i=1}^{\textit{ans}}\left|\overrightarrow{h_ih_{i+1}}\right|
$$

### Graham 扫描法

#### 性质

与 Andrew 算法相同，Graham 扫描法的时间复杂度为 $O(n\log n)$，复杂度瓶颈也在于对所有点排序．

#### 过程

首先找到所有点中，纵坐标最小的一个点 $P$．根据凸包的定义我们知道，这个点一定在凸包上．然后将所有的点以相对于点 P 的极角大小为关键字进行排序．

![](./images/ch1.svg)

和 Andrew 算法类似地，我们考虑从点 $P$ 出发，在凸包上逆时针走，那么我们经过的所有节点一定都是「左拐」的．形式化地说，对于凸包逆时针方向上任意连续经过的三个点 $P_1, P_2, P_3$，一定满足 $\overrightarrow{P_1 P_2} \times \overrightarrow{P_2 P_3} \ge 0$．

新建一个栈用于存储凸包的信息，先将 $P$ 压入栈中，然后按照极角序依次尝试加入每一个点．如果进栈的点 $P_0$ 和栈顶的两个点 $P_1, P_2$（其中 $P_1$ 为栈顶）行进的方向「右拐」了，那么就弹出栈顶的 $P_1$，不断重复上述过程直至进栈的点与栈顶的两个点满足条件，或者栈中仅剩下一个元素，再将 $P_0$ 压入栈中．

![](./images/ch2.svg)

![](./images/ch3.svg)

???+ note "代码实现"
    ```cpp
    struct Point {
      double x, y, ang;
    
      Point operator-(const Point& p) const { return {x - p.x, y - p.y, 0}; }
    } p[MAXN];
    
    double dis(Point p1, Point p2) {
      return sqrt((p1.x - p2.x) * (p1.x - p2.x) + (p1.y - p2.y) * (p1.y - p2.y));
    }
    
    bool cmp(Point p1, Point p2) {
      if (p1.ang == p2.ang) {
        return dis(p1, p[1]) < dis(p2, p[1]);
      }
      return p1.ang < p2.ang;
    }
    
    double cross(Point p1, Point p2) { return p1.x * p2.y - p1.y * p2.x; }
    
    int main() {
      for (int i = 2; i <= n; ++i) {
        if (p[i].y < p[1].y || (p[i].y == p[1].y && p[i].x < p[1].x)) {
          std::swap(p[1], p[i]);
        }
      }
      for (int i = 2; i <= n; ++i) {
        p[i].ang = atan2(p[i].y - p[1].y, p[i].x - p[1].x);
      }
      std::sort(p + 2, p + n + 1, cmp);
      sta[++top] = 1;
      for (int i = 2; i <= n; ++i) {
        while (top >= 2 &&
               cross(p[sta[top]] - p[sta[top - 1]], p[i] - p[sta[top]]) < 0) {
          top--;
        }
        sta[++top] = i;
      }
      return 0;
    }
    ```

## 闵可夫斯基和

### 定义

点集 $P$ 和点集 $Q$ 的闵可夫斯基和 $P+Q$ 定义为 $P+Q=\{a+b|a\in P,b\in Q\}$，即把点集 $Q$ 中的每个点看做一个向量，将点集 $P$ 中每个点沿这些向量平移，最终得到的结果的集合就是点集 $P+Q$．此处仅讨论 **凸包** 的闵可夫斯基和．

例如：对于点集 $P=\{(0,0),(-3,3),(2,1)\}$ 和 点集 $Q=\{(0,0),(-1,3),(1,4),(2,2)\}$，

![](./images/convex-hull1.svg)

将 $P$ 沿 $Q$ 的每个向量平移：

![](./images/convex-hull2.svg)

不难发现新图形也是一个 **凸包**：

![](./images/convex-hull3.svg)

### 性质

1.  若点集合 $P$，$Q$ 为凸集，则其闵可夫斯基和 $P+Q$ 也是凸集．

    ??? note "证明"
        设 $e,f\in P+Q$，有 $a,b \in P$，$c,d\in Q$ 且 $e=a+c,f=b+d$，则对任意 $t\in[0,1]$ 均有：
        
        $$
        \begin{aligned}
        te + (1-t)f &= t(a+c)+(1-t)(b+d)\\
        &=(ta+(1-t)b)+(tc+(1-t)d)\\
        &\in P+Q.
        \end{aligned}
        $$
        
        证毕．
2.  若点集 $P$，$Q$ 为凸集，则其闵可夫斯基和 $P+Q$ 的边集是由凸集 $P$，$Q$ 的边按极角排序后连接的结果．

    ??? note "证明"
        不妨假设凸集 $P$ 中任意一条边的斜率与 $Q$ 中任意一条边的斜率均不相同．将坐标系进行旋转，使得 $P$ 上的一条边 $XY$ 与 $x$ 轴平行且在最下方．
        
        设此时 $Q$ 中最低的点 $U$，$P+Q$ 的 **最低** 且 **靠左** 的点 $A$．
        
        可知 $\vec{A} = \vec{X} + \vec{U}$，所以 $A$ 必然在 $P+Q$ 的边界上．
        
        同理，$P+Q$ 中 **最低** 且 **靠右** 的点 $B$ 有 $\vec{B} = \vec{Y} + \vec{U}$，也必然在 $P+Q$ 的边界上．
        
        因此，有 $\vec{AB} = \vec{XY} + \vec{U}$．
        
        若按顺序进行旋转，则结果连续的构成了 $P+Q$ 中的每条边．
        
        证毕．

### 实现

我们可以根据性质 2，将凸集 $P,Q$ 极角排序，得到它们在 $P+Q$ 上的出现顺序，把 $P_1+Q_1$ 看做 $P+Q$ 的起点，然后用类似 **归并** 的做法依次放边即可．

时间复杂度：$O(n+m)$

???+ note "实现"
    ```cpp
    template <class T>
    struct Point {
      T x, y;
    
      Point(T x = 0, T y = 0) : x(x), y(y) {}
    
      friend Point operator+(const Point &a, const Point &b) {
        return {a.x + b.x, a.y + b.y};
      }
    
      friend Point operator-(const Point &a, const Point &b) {
        return {a.x - b.x, a.y - b.y};
      }
    
      // 点乘
      friend T operator*(const Point &a, const Point &b) {
        return a.x * b.x + a.y * b.y;
      }
    
      // 叉乘
      friend T operator^(const Point &a, const Point &b) {
        return a.x * b.y - a.y * b.x;
      }
    };
    
    template <class T>
    vector<Point<T>> minkowski_sum(vector<Point<T>> a, vector<Point<T>> b) {
      vector<Point<T>> c{a[0] + b[0]};
      for (usz i = 0; i + 1 < a.size(); ++i) a[i] = a[i + 1] - a[i];
      for (usz i = 0; i + 1 < b.size(); ++i) b[i] = b[i + 1] - b[i];
      a.pop_back(), b.pop_back();
      c.resize(a.size() + b.size() + 1);
      merge(a.begin(), a.end(), b.begin(), b.end(), c.begin() + 1,
            [](const Point<T> &a, const Point<T> &b) { return (a ^ b) < 0; });
      for (usz i = 1; i < c.size(); ++i) c[i] = c[i] + c[i - 1];
      return c;
    }
    ```

### 例题

???+ note "[例题 \[JSOI2018\] 战争](https://loj.ac/p/2549)"
    有两个凸包 $P,Q$，平移 $q$ 次 $Q$，问每次移动后是否有交点．$1\le n,m\le 10^5,1\le q\le 10^5$．

??? note "实现"
    ```cpp
    --8<-- "docs/geometry/code/convex-hull/convex-hull_1.cpp"
    ```

## 三维凸包

### 基础知识

> 圆的反演：反演中心为 $O$，反演半径为 $R$，若经过 $O$ 的直线经过 $P$,$P'$，且 $OP\times OP'=R^{2}$，则称 $P$、$P'$ 关于 $O$ 互为反演．

### 过程

求凸包的过程如下：

-   首先对其微小扰动，避免出现四点共面的情况．
-   对于一个已知凸包，新增一个点 $P$，将 $P$ 视作一个点光源，向凸包做射线，可以知道，光线的可见面和不可见面一定是由若干条棱隔开的．
-   将光的可见面删去，并新增由其分割棱与 $P$ 构成的平面．
    重复此过程即可，由 [Pick 定理](./pick.md)、欧拉公式（在凸多面体中，其顶点 $V$、边数 $E$ 及面数 $F$ 满足 $V−E+F=2$）和圆的反演，复杂度 $O(n^2)$．[^3d-v]

### 模板题

[P4724【模板】三维凸包](https://www.luogu.com.cn/problem/P4724)

重复上述过程即可得到答案．

???+ note "代码实现"
    ```cpp
    --8<-- "docs/geometry/code/3d/3d_1.cpp"
    ```

## 练习

-   [UVa11626 Convex Hull](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&category=78&page=show_problem&problem=2673)

-   [「USACO5.1」圈奶牛 Fencing the Cows](https://www.luogu.com.cn/problem/P2742)

-   [POJ1873 The Fortified Forest](http://poj.org/problem?id=1873)

-   [POJ1113 Wall](http://poj.org/problem?id=1113)

-   [USACO22JAN Multiple Choice Test P](https://www.luogu.com.cn/problem/P8101)

-   [「SHOI2012」信用卡凸包](https://www.luogu.com.cn/problem/P3829)

## 参考资料与注释

[^3d-v]: [三维凸包学习小记](https://www.cnblogs.com/xzyxzy/p/10225804.html)


## geometry/distance.md

author: Chrogeek, frank-xjh, ChungZH, hsfzLZH1, Marcythm, Planet6174, partychicken, i-Yirannn

## 欧氏距离

### 二维空间

#### 定义

欧氏距离，一般也称作欧几里得距离．在平面直角坐标系中，设点 $A,B$ 的坐标分别为 $A(x_1,y_1),B(x_2,y_2)$，则两点间的欧氏距离为：

$$
\left | AB \right | = \sqrt{\left ( x_2 - x_1 \right )^2 + \left ( y_2 - y_1 \right )^2}
$$

#### 解释

举个例子，若在平面直角坐标系中，有两点 $A(6,5),B(2,2)$，通过公式，我们很容易得到 $A,B$ 两点间的欧氏距离：

$$
\left | AB \right | = \sqrt{\left ( 2 - 6 \right )^2 + \left ( 2 - 5 \right )^2} = \sqrt{4^2+3^2} = 5
$$

除此之外，$P(x,y)$ 到原点的欧氏距离可以用公式表示为：

$$
|P| = \sqrt{x^2+y^2}
$$

### n 维空间

#### 引入

那么，三维空间中两点的欧氏距离公式呢？我们来观察下图．

![dis-3-dimensional](./images/distance-0.png)

我们很容易发现，在 $\triangle ADC$ 中，$\angle ADC = 90^\circ$；在 $\triangle ACB$ 中，$\angle ACB = 90^\circ$．

$$
\begin{aligned}
\therefore ~ |AB| &= \sqrt{|AC|^2+|BC|^2} \\
&= \sqrt{|AD|^2+|CD|^2+|BC|^2}
\end{aligned}
$$

#### 定义

由此可得，三维空间中欧氏距离的距离公式为：

$$
\begin{gathered}
\left | AB \right | = \sqrt{\left ( x_2 - x_1 \right )^2 + \left ( y_2 - y_1 \right )^2 + \left ( z_2 - z_1 \right )^2} \\
|P| = \sqrt{x^2+y^2+z^2}
\end{gathered}
$$

#### 解释

[NOIP2017 提高组 奶酪](https://uoj.ac/problem/332) 就运用了这一知识，可以作为欧氏距离的例题．

以此类推，我们就得到了 $n$ 维空间中欧氏距离的距离公式：对于 $\vec A(x_{11}, x_{12}, \cdots,x_{1n}) ,~ \vec B(x_{21}, x_{22}, \cdots,x_{2n})$，有

$$
\begin{aligned}
\lVert\overrightarrow{AB}\rVert &= \sqrt{\left ( x_{11} - x_{21} \right )^2 + \left ( x_{12} - x_{22} \right )^2 + \cdot \cdot \cdot +\left ( x_{1n} - x_{2n} \right )^2}\\
&= \sqrt{\sum_{i = 1}^{n}(x_{1i} - x_{2i})^2}
\end{aligned}
$$

欧氏距离虽然很有用，但也有明显的缺点．两个整点计算其欧氏距离时，往往答案是浮点型，会存在一定误差．

## 曼哈顿距离

### 定义

在二维空间内，两个点之间的曼哈顿距离（Manhattan distance）为它们横坐标之差的绝对值与纵坐标之差的绝对值之和．设点 $A(x_1,y_1),B(x_2,y_2)$，则 $A,B$ 之间的曼哈顿距离用公式可以表示为：

$$
d(A,B) = |x_1 - x_2| + |y_1 - y_2|
$$

### 解释

观察下图：

![manhattan-dis-diff](./images/distance-1.png)

在 $A,B$ 间，黄线、橙线都表示曼哈顿距离，而红线、蓝线表示等价的曼哈顿距离，绿线表示欧氏距离．

同样的例子，在下图中 $A,B$ 的坐标分别为 $A(25,20),B(10,10)$．

![manhattan-dis](./images/distance-2.svg)

通过公式，我们很容易得到 $A,B$ 两点间的曼哈顿距离：

$$
d(A,B) = |20 - 10| + |25 - 10| = 10 + 15 = 25
$$

经过推导，我们得到 $n$ 维空间的曼哈顿距离公式为：

$$
\begin{aligned}
d(A,B) &= |x_1 - y_1| + |x_2 - y_2| + \cdot \cdot \cdot + |x_n - y_n|\\
&= \sum_{i = 1}^{n}|x_i - y_i|
\end{aligned}
$$

### 性质

除了公式之外，曼哈顿距离还具有以下数学性质：

-   非负性：曼哈顿距离是一个非负数，即 $d(i,j)\geq 0$．
-   统一性：一个点到自身的曼哈顿距离为 $0$，即 $d(i,i) = 0$．
-   对称性：$A$ 到 $B$ 与 $B$ 到 $A$ 的曼哈顿距离相等，即 $d(i,j) = d(j,i)$．
-   三角不等式：从点 $i$ 到 $j$ 的直接距离不会大于途经的任何其它点 $k$ 的距离，即 $d(i,j)\leq d(i,k)+d(k,j)$．

### 例题

[P5098「USACO04OPEN」Cave Cows 3](https://www.luogu.com.cn/problem/P5098)

根据题意，对于式子 $|x_1-x_2|+|y_1-y_2|$，我们可以假设 $x_1 - x_2 \geq 0$，根据 $y_1 - y_2$ 的符号分成两种情况：

-   $(y_1 - y_2 \geq 0)\rightarrow |x_1-x_2|+|y_1-y_2|=x_1 + y_1 - (x_2 + y_2)$

-   $(y_1 - y_2 < 0)\rightarrow |x_1-x_2|+|y_1-y_2|=x_1 - y_1 - (x_2 - y_2)$

只要分别求出 $x+y, x-y$ 的最大值和最小值即能得出答案．

??? note "参考代码"
    === "C++"
        ```cpp
        #include <algorithm>
        #include <cstdio>
        using namespace std;
        
        int main() {
          int n, x, y, minx = 0x7fffffff, maxx = 0, miny = 0x7fffffff, maxy = 0;
          scanf("%d", &n);
          for (int i = 1; i <= n; i++) {
            scanf("%d%d", &x, &y);
            minx = min(minx, x + y), maxx = max(maxx, x + y);
            miny = min(miny, x - y), maxy = max(maxy, x - y);
          }
          printf("%d\n", max(maxx - minx, maxy - miny));
          return 0;
        }
        ```
    
    === "Python"
        ```python
        minx = 0x7FFFFFFF
        maxx = 0
        miny = 0x7FFFFFFF
        maxy = 0
        n = int(input())
        for i in range(1, n + 1):
            x, y = map(lambda x: int(x), input().split())
            minx = min(minx, x + y)
            maxx = max(maxx, x + y)
            miny = min(miny, x - y)
            maxy = max(maxy, x - y)
        print(max(maxx - minx, maxy - miny))
        ```

其实还有第二种做法，那就是把曼哈顿距离转化为切比雪夫距离求解，最后部分会讲到．

## 切比雪夫距离

### 定义

切比雪夫距离（Chebyshev distance）是向量空间中的一种度量，二个点之间的距离定义为其各坐标数值差的最大值．[^ref1]

在二维空间内，两个点之间的切比雪夫距离为它们横坐标之差的绝对值与纵坐标之差的绝对值的最大值．设点 $A(x_1,y_1),B(x_2,y_2)$，则 $A,B$ 之间的切比雪夫距离用公式可以表示为：

$$
d(A,B) = \max(|x_1 - x_2|, |y_1 - y_2|)
$$

$n$ 维空间中切比雪夫距离的距离公式可以表示为：

$$
\begin{aligned}
d(x,y) &= \max\begin{Bmatrix} |x_1 - y_1|,|x_2 - y_2|,\cdot \cdot \cdot,|x_n - y_n|\end{Bmatrix} \\
&= \max\begin{Bmatrix} |x_i - y_i|\end{Bmatrix}(i \in [1, n])\end{aligned}
$$

### 解释

仍然是这个例子，下图中 $A,B$ 的坐标分别为 $A(25,20),B(10,10)$．

![Chebyshev-dis](./images/distance-2.svg)

$$
d(A,B) = \max(|20 - 10|, |25 - 10|) = \max(10, 15) = 15
$$

## 曼哈顿距离与切比雪夫距离的相互转化

### 过程

首先，我们考虑画出平面直角坐标系上所有到原点的曼哈顿距离为 $1$ 的点．

通过公式，我们很容易得到方程 $|x| + |y| = 1$．

将绝对值展开，得到 $4$ 个 一次函数，分别是：

$$
\begin{aligned}
&y = -x + 1 &(x \geq 0, y \geq 0) \\
&y = x + 1 &(x \leq 0, y \geq 0) \\
&y = x - 1  &(x \geq 0, y \leq 0)  \\
&y = -x - 1  &(x \leq 0, y \leq 0) \\
\end{aligned}
$$

将这 $4$ 个函数画到平面直角坐标系上，得到一个边长为 $\sqrt{2}$ 的正方形，如下图所示：

![dis-diff-square-1](./images/distance-3.svg)

正方形边界上所有的点到原点的 曼哈顿距离 都是 $1$．

同理，我们再考虑画出平面直角坐标系上所有到原点的 切比雪夫距离 为 $1$ 的点．

通过公式，我们知道 $\max(|x|,|y|)=1$．

我们将式子展开，也同样可以得到 $4$ 条线段，分别是：

$$
\begin{aligned}
&y = 1&(-1\leq x \leq 1) \\
&y = -1&(-1\leq x \leq 1) \\
&x = 1,&(-1\leq y \leq 1) \\
&x = -1,&(-1\leq y \leq 1) \\
\end{aligned}
$$

画到平面直角坐标系上，可以得到一个边长为 $2$ 的正方形，如下图所示：

![dis-diff-square-2](./images/distance-4.svg)

正方形边界上所有的点到原点的切比雪夫距离都是 $1$．

将这两幅图对比，我们会神奇地发现：

这 $2$ 个正方形是相似图形．

### 证明

所以，曼哈顿距离与切比雪夫距离之间会不会有联系呢？

接下来我们简略证明一下：

假设 $A(x_1,y_1),B(x_2,y_2)$，

我们把曼哈顿距离中的绝对值拆开，能够得到四个值，这四个值中的最大值是两个非负数之和，即曼哈顿距离．则 $A,B$ 两点的曼哈顿距离为：

$$
\begin{aligned}
d(A,B)&=|x_1 - x_2| + |y_1 - y_2|\\
&=\max\begin{Bmatrix} x_1 - x_2 + y_1 - y_2, x_1 - x_2 + y_2 - y_1,x_2 - x_1 + y_1 - y_2, x_2 - x_1 + y_2 - y_1\end{Bmatrix}\\
&= \max(|(x_1 + y_1) - (x_2 + y_2)|, |(x_1 - y_1) - (x_2 - y_2)|)
\end{aligned}
$$

我们很容易发现，这就是 $(x_1 + y_1,x_1 - y_1), (x_2 + y_2,x_2 - y_2)$ 两点之间的切比雪夫距离．

所以将每一个点 $(x,y)$ 转化为 $(x + y, x - y)$，新坐标系下的切比雪夫距离即为原坐标系下的曼哈顿距离．

同理，$A,B$ 两点的切比雪夫距离为：

$$
\begin{aligned}
d(A,B)&=\max\begin{Bmatrix} |x_1 - x_2|,|y_1 - y_2|\end{Bmatrix}\\
&=\max\begin{Bmatrix} \left|\dfrac{x_1 + y_1}{2}-\dfrac{x_2 + y_2}{2}\right|+\left|\dfrac{x_1 - y_1}{2}-\dfrac{x_2 - y_2}{2}\right|\end{Bmatrix}
\end{aligned}
$$

而这就是 $(\dfrac{x_1 + y_1}{2},\dfrac{x_1 - y_1}{2}), (\dfrac{x_2 + y_2}{2},\dfrac{x_2 - y_2}{2})$ 两点之间的曼哈顿距离．

所以将每一个点 $(x,y)$ 转化为 $(\dfrac{x + y}{2},\dfrac{x - y}{2})$，新坐标系下的曼哈顿距离即为原坐标系下的切比雪夫距离．

### 结论

-   曼哈顿坐标系是通过切比雪夫坐标系旋转 $45^\circ$ 后，再缩小到原来的一半得到的．
-   将一个点 $(x,y)$ 的坐标变为 $(x + y, x - y)$ 后，原坐标系中的曼哈顿距离等于新坐标系中的切比雪夫距离．
-   将一个点 $(x,y)$ 的坐标变为 $(\dfrac{x + y}{2},\dfrac{x - y}{2})$ 后，原坐标系中的切比雪夫距离等于新坐标系中的曼哈顿距离．

碰到求切比雪夫距离或曼哈顿距离的题目时，我们往往可以相互转化来求解．两种距离在不同的题目中有不同的优缺点，应该灵活运用．

### 例题

[P4648「IOI2007」pairs 动物对数](https://www.luogu.com.cn/problem/P4648)（曼哈顿距离转切比雪夫距离）

[P3964「TJOI2013」松鼠聚会](https://www.luogu.com.cn/problem/P3964)（切比雪夫距离转曼哈顿距离）

最后给出 [P5098「USACO04OPEN」Cave Cows 3](https://www.luogu.com.cn/problem/P5098) 的第二种解法：

我们考虑将题目所求的曼哈顿距离转化为切比雪夫距离，即把每个点的坐标 $(x,y)$ 变为 $(x + y, x - y)$．

所求的答案就变为 $\max\limits_{i,j\in n}\begin{Bmatrix} \max\begin{Bmatrix} |x_i - x_j|,|y_i - y_j|\end{Bmatrix}\end{Bmatrix}$．

现要使得横坐标之差和纵坐标之差最大，只需要预处理出 $x,y$ 的最大值和最小值即可．

??? note "参考代码"
    === "C++"
        ```cpp
        #include <algorithm>
        #include <cstdio>
        using namespace std;
        
        int main() {
          int n, x, y, a, b, minx = 0x7fffffff, maxx = 0, miny = 0x7fffffff, maxy = 0;
          scanf("%d", &n);
          for (int i = 1; i <= n; i++) {
            scanf("%d%d", &a, &b);
            x = a + b, y = a - b;
            minx = min(minx, x), maxx = max(maxx, x);
            miny = min(miny, y), maxy = max(maxy, y);
          }
          printf("%d\n", max(maxx - minx, maxy - miny));
          return 0;
        }
        ```
    
    === "Python"
        ```python
        minx = 0x7FFFFFFF
        maxx = 0
        miny = 0x7FFFFFFF
        maxy = 0
        n = int(input())
        for i in range(1, n + 1):
            a, b = map(lambda x: int(x), input().split())
            x = a + b
            y = a - b
            minx = min(minx, x)
            maxx = max(maxx, x)
            miny = min(miny, y)
            maxy = max(maxy, y)
        print(max(maxx - minx, maxy - miny))
        ```

对比两份代码，我们又能够发现，两种不同的思路，写出来的代码却是完全等价的，是不是很神奇呢？当然，更高深的东西需要大家另行研究．

## 闵可夫斯基距离

我们定义 $n$ 维空间中两点 $X(x_1, x_2, \dots, x_n)$，$Y(y_1, y_2, \dots, y_n)$ 之间的闵可夫斯基距离为：

$$
D(X, Y) = \left(\sum_{i=1}^n \left\vert x_i - y_i \right\vert ^p\right)^{\frac{1}{p}}.
$$

特别的：

1.  当 $p=1$ 时，$D(X, Y) = \sum_{i=1}^n \left\vert x_i - y_i \right\vert$ 即为曼哈顿距离；
2.  当 $p=2$ 时，$D(X, Y) = \left(\sum_{i=1}^n (x_i - y_i)^2\right)^{1/2}$ 即为欧几里得距离；
3.  当 $p \to \infty$ 时，$D(X, Y) = \lim_{p \to \infty}\left(\sum_{i=1}^n \left\vert x_i - y_i \right\vert ^p\right) ^{1/p} = \max\limits_{i=1}^n \left\vert x_i - y_i \right\vert$ 即为切比雪夫距离．

注意：当 $p \ge 1$ 时，闵可夫斯基距离才是度量，具体证明参见 [Minkowski distance - Wikipedia](https://en.wikipedia.org/wiki/Minkowski_distance)．

## 参考资料与链接

1.  [浅谈三种常见的距离算法](https://www.luogu.com.cn/blog/xuxing/Distance-Algorithm)，感谢作者 xuxing 的授权．

[^ref1]: [切比雪夫距离 - 维基百科，自由的百科全书](https://zh.wikipedia.org/wiki/%E5%88%87%E6%AF%94%E9%9B%AA%E5%A4%AB%E8%B7%9D%E7%A6%BB)


## geometry/half-plane.md

author: wjy-yy, Ir1d, Xeonacid

## 定义

### 半平面

一条直线和直线的一侧．半平面是一个点集，因此是一条直线和直线的一侧构成的点集．当包含直线时，称为闭半平面；当不包含直线时，称为开半平面．

解析式一般为 $Ax+By+C\ge 0$．

在计算几何中用向量表示，整个题统一以向量的左侧或右侧为半平面．

![半平面](./images/hpi1.svg)

### 半平面交

半平面交是指多个半平面的交集．因为半平面是点集，所以点集的交集仍然是点集．在平面直角坐标系围成一个区域．

这就很像普通的线性规划问题了，得到的半平面交就是线性规划中的可行域．一般情况下半平面交是有限的，经常考察面积等问题的解决．

它可以理解为向量集中每一个向量的右侧的交，或者是下面方程组的解．

$$
\begin{cases}
A_1x+B_1y+C\ge 0\\
A_2x+B_2y+C\ge 0\\
\cdots
\end{cases}
$$

### 多边形的核

如果一个点集中的点与多边形上任意一点的连线与多边形没有其他交点，那么这个点集被称为多边形的核．

把多边形的每条边看成是首尾相连的向量，那么这些向量在多边形内部方向的半平面交就是多边形的核．

## 解法 - S&I 算法

### 极角排序

C 语言有一个库函数叫做 `atan2(double y,double x)`，可以返回 $\theta\in (-\pi,\pi]$，$\theta =\arctan \frac{y}{x}$．

直接以向量为自变量，调用这个函数，以返回值为关键字排序，得到新的边（向量）集．

排序时，如果遇到共线向量（且方向相同），则取靠近可行域的一个．比如两个向量的极角相同，而我们要的是向量的左侧半平面，那么我们只需要保留左侧的向量．判断方法是取其中一个向量的起点或终点与另一个比较，检查是在左边还是在右边．

### 维护单调队列

因为半平面交是一个凸多边形，所以需要维护一个凸壳．因为后来加入的只可能会影响最开始加入的或最后加入的边（此时凸壳连通），只需要删除队首和队尾的元素，所以需要用单调队列．

我们遍历排好序了的向量，并维护另一个交点数组．当单队中元素超过 2 个时，他们之间就会产生交点．

对于当前向量，如果上一个交点在这条向量表示的半平面交的 **异侧**，那么上一条边就没有意义了．

![单调队列](./images/hpi2.svg)

如上图，假设取向量左侧半平面．极角排序后，遍历顺序应该是 $\vec a\to\vec b\to\vec c$．当 $\vec a$ 和 $\vec b$ 入队时，在交点数组里会产生一个点 $D$（交点数组保存队列中相同下标的向量与前一向量的交点）．

接下来枚举到 $\vec c$ 时，发现 $D$ 在 $\vec c$ 的右侧．而因为 **产生**  $D$  **的向量的极角一定比** $\vec c$  **要小**，所以产生 $D$ 的向量（指 $\vec b$）就对半平面交没有影响了．

还有一种可能的情况是快结束的时候，新加入的向量会从队首开始造成影响．

![队首影响](./images/hpi7.svg)

仍然假设取向量左侧半平面．加入向量 $\vec f$ 之后，第一个交点 $G$ 就在 $\vec f$ 的右侧，我们把上面的判断标准逆过来看，就知道此时应该删除向量 $\vec a$，也即 **队首** 的向量．

最后用队首的向量排除一下队尾多余的向量．因为队首的向量会被后面的约束，而队尾的向量不会．此时它们围成了一个环，因此队首的向量就可以约束队尾的向量．

### 得到半平面交

如果半平面交是一个凸 $n$ 边形，最后在交点数组里会得到 $n$ 个点．我们再把它们首尾相连，就是一个统一方向（顺或逆时针）的 $n$ 多边形．

此时就可以用三角剖分求面积了．（求面积是最基础的考法）

偶尔会出现半平面交不存在或面积为 0 的情况，注意考虑边界．

### 注意事项

当出现一个可以把队列里的点全部弹出去的向量（即所有队列里的点都在该向量的右侧），则我们 **必须** 先处理队尾，再处理队首．因此在循环中，我们先枚举 `--r;` 的部分，再枚举 `++l;` 的部分，才不会错．原因如下．

![](./images/hpi4.svg)

一般情况下，我们在队列（队列顺序为 $\left\{\vec{u},\vec{v}\right\}$）后面加一条边（向量 $\vec w$），会产生一个交点 $N$，缩小 $\vec{v}$ 后面的范围．

![](./images/hpi5.svg)

但是毕竟每次操作都是一般的，因此可能会有把 $M$ 点「挤出去」的情况．

![](./images/hpi6.svg)

如果此时出现了向量 $\vec a$，使得 $M$ 在 $\vec a$ 的右侧，那么 $M$ 就要出队了．此时如果从队首枚举 `++l`，显然是扩大了范围．实际上 $M$ 点是由 $\vec u$ 和 $\vec v$ 共同构成的，因此需要考虑影响到现有进程的是 $\vec u$ 还是 $\vec v$．而因为我们在极角排序后，向量是逆时针顺序，所以 $\vec v$ 的影响要更大一些．

就如上图，如果 $M$ 确认在 $\vec a$ 的右侧，那么此时 $\vec v$ 的影响一定不会对半平面交的答案作出任何贡献．

而我们排除队首的原因是 **当前向量的限制比队首向量要大**，这个条件的前提是队列里有不止两个线段（向量），不然就会出现上面的情况．

所以一定要先排除队尾再排除队首．

???+ note "代码 - 比较部分"
    ```cpp
    friend bool operator<(seg x, seg y) {
      db t1 = atan2((x.b - x.a).y, (x.b - x.a).x);
      db t2 = atan2((y.b - y.a).y, (y.b - y.a).x);  // 求极角
      if (fabs(t1 - t2) > eps)                      // 如果极角不等
        return t1 < t2;
      return (y.a - x.a) * (y.b - x.a) >
             eps;  // 判断向量x在y的哪边，令最靠左的排在最左边
    }
    ```

???+ note "代码 - 增量部分"
    ```cpp
    // pnt its(seg a,seg b)表示求线段a,b的交点
    // s[]是极角排序后的向量
    // q[]是向量队列
    // t[i]是s[i-1]与s[i]的交点
    // 【码风】队列的范围是(l,r]
    // 求的是向量左侧的半平面
    int l = 0, r = 0;
    for (int i = 1; i <= n; ++i)
      if (s[i] != s[i - 1]) {
        // 注意要先检查队尾
        while (r - l > 1 && (s[i].b - t[r]) * (s[i].a - t[r]) >
                                eps)  // 如果上一个交点在向量右侧则弹出队尾
          --r;
        while (r - l > 1 && (s[i].b - t[l + 2]) * (s[i].a - t[l + 2]) >
                                eps)  // 如果第一个交点在向量右侧则弹出队首
          ++l;
        q[++r] = s[i];
        if (r - l > 1) t[r] = its(q[r], q[r - 1]);  // 求新交点
      }
    while (r - l > 1 &&
           (q[l + 1].b - t[r]) * (q[l + 1].a - t[r]) > eps)  // 注意删除多余元素
      --r;
    t[r + 1] = its(q[l + 1], q[r]);  // 再求出新的交点
    ++r;
    // 这里不能在t里面++r需要注意一下……
    ```

## 练习

[POJ 2451 Uyuw's Concert](http://poj.org/problem?id=2451) 注意边界

[POJ 1279 Art Gallery](http://poj.org/problem?id=1279) 求多边形的核

[「CQOI2006」凸多边形](https://www.luogu.com.cn/problem/P4196)


## geometry/inverse.md

author: hyp1231, 383494

## 引入

反演变换适用于题目中存在多个圆/直线之间的相切关系的情况．利用反演变换的性质，在反演空间求解问题，可以大幅简化计算．

## 定义

给定反演中心点 $O$ 和反演半径 $R$．若平面上点 $P$ 和 $P'$ 满足：

-   点 $P'$ 在射线 $\overrightarrow{OP}$ 上
-   $|OP| \cdot |OP'| = R^2$

则称点 $P$ 和点 $P'$ 互为反演点．

## 解释

下图所示即为平面上一点 $P$ 的反演：

![Inv1](./images/inverse1.png)

## 性质

1.  圆 $O$ 外的点的反演点在圆 $O$ 内，反之亦然；圆 $O$ 上的点的反演点为其自身．

2.  不过点 $O$ 的圆 $A$，其反演图形也是不过点 $O$ 的圆．

    ![Inv2](./images/inverse2.png)

    -   记圆 $A$ 半径为 $r_1$，其反演图形圆 $B$ 半径为 $r_2$，则有：

        $$
        r_2 = \frac{1}{2}\left(\frac{1}{|OA| - r_1} - \frac{1}{|OA| + r_1}\right) R^2
        $$

    ???+ note "证明"
        ![Inv3](./images/inverse3.png)
        
        根据反演变换定义：
        
        $$
        \begin{aligned}
        |OC|\cdot|OC'| &= (|OA|+r_1)\cdot(|OB|-r_2) = R^2 \\
        |OD|\cdot|OD'| &= (|OA|-r_1)\cdot(|OB|+r_2) = R^2
        \end{aligned}
        $$
        
        消掉 $|OB|$，解方程即可．

    -   记点 $O$ 坐标为 $(x_0, y_0)$，点 $A$ 坐标为 $x_1, y_1$，点 $B$ 坐标为 $x_2, y_2$，则有：

        $$
        \begin{aligned}
        x_2 &= x_0 + \frac{|OB|}{|OA|} (x_1 - x_0) \\
        y_2 &= y_0 + \frac{|OB|}{|OA|} (y_1 - y_0)
        \end{aligned}
        $$

        其中 $|OB|$ 可在上述求 $r_2$ 的过程中计算得到．

3.  过点 $O$ 的圆 $A$，其反演图形是不过点 $O$ 的直线．因为圆 $A$ 上无限接近点 $O$ 的一点，其反演点离点 $O$ 无限远．

    ![Inv4](./images/inverse4.png)

4.  两个图形相切且存在不为点 $O$ 的切点，则他们的反演图形也相切．

## 例题

### [「ICPC 2013 杭州赛区」Problem of Apollonius](https://acm.hdu.edu.cn/showproblem.php?pid=4773)

#### 题目大意

求过两圆外一点，且与两圆相切的所有的圆．

#### 解法

首先考虑解析几何解法，似乎很难求解．

考虑以需要经过的点为反演中心进行反演（反演半径任意），所求的圆的反演图形是一条直线（应用性质 $3$），且与题目给出两圆的反演图形（性质 $2$）相切（性质 $4$）．

于是题目经过反演变换后转变为：求两圆的所有公切线．

求出公切线后，反演回原平面即可．

??? note "示例代码"
    ```cpp
    #include <algorithm>
    #include <cmath>
    #include <cstdio>
    #include <cstring>
    #include <iostream>
    #include <vector>
    using namespace std;
    
    constexpr double EPS = 1e-8;   // 精度系数
    const double PI = acos(-1.0);  // π
    constexpr int N = 4;
    
    // 点的定义
    struct Point {
      double x, y;
    
      Point(double x = 0, double y = 0) : x(x), y(y) {}
    
      bool operator<(Point A) const { return x == A.x ? y < A.y : x < A.x; }
    };
    
    // 向量的定义
    using Vector = Point;
    
    // 向量加法
    Vector operator+(Vector A, Vector B) { return Vector(A.x + B.x, A.y + B.y); }
    
    // 向量减法
    Vector operator-(Vector A, Vector B) { return Vector(A.x - B.x, A.y - B.y); }
    
    // 向量数乘
    Vector operator*(Vector A, double p) { return Vector(A.x * p, A.y * p); }
    
    // 向量数除
    Vector operator/(Vector A, double p) { return Vector(A.x / p, A.y / p); }
    
    // 与0的关系
    int dcmp(double x) {
      if (fabs(x) < EPS) return 0;
      return x < 0 ? -1 : 1;
    }
    
    // 向量点乘
    double Dot(Vector A, Vector B) { return A.x * B.x + A.y * B.y; }
    
    // 向量长度
    double Length(Vector A) { return sqrt(Dot(A, A)); }
    
    // 向量叉乘
    double Cross(Vector A, Vector B) { return A.x * B.y - A.y * B.x; }
    
    // 点在直线上投影
    Point GetLineProjection(Point P, Point A, Point B) {
      Vector v = B - A;
      return A + v * (Dot(v, P - A) / Dot(v, v));
    }
    
    // 圆
    struct Circle {
      Point c;
      double r;
    
      Circle() : c(Point(0, 0)), r(0) {}
    
      Circle(Point c, double r = 0) : c(c), r(r) {}
    
      // 输入极角返回点坐标
      Point point(double a) { return Point(c.x + cos(a) * r, c.y + sin(a) * r); }
    };
    
    // 两圆公切线 返回切线的条数，-1表示无穷多条切线
    // a[i] 和 b[i] 分别是第i条切线在圆A和圆B上的切点
    int getTangents(Circle A, Circle B, Point* a, Point* b) {
      int cnt = 0;
      if (A.r < B.r) {
        swap(A, B);
        swap(a, b);
      }
      double d2 =
          (A.c.x - B.c.x) * (A.c.x - B.c.x) + (A.c.y - B.c.y) * (A.c.y - B.c.y);
      double rdiff = A.r - B.r;
      double rsum = A.r + B.r;
      if (dcmp(d2 - rdiff * rdiff) < 0) return 0;  // 内含
    
      double base = atan2(B.c.y - A.c.y, B.c.x - A.c.x);
      if (dcmp(d2) == 0 && dcmp(A.r - B.r) == 0) return -1;  // 无限多条切线
      if (dcmp(d2 - rdiff * rdiff) == 0) {  // 内切，一条切线
        a[cnt] = A.point(base);
        b[cnt] = B.point(base);
        ++cnt;
        return 1;
      }
      // 有外公切线
      double ang = acos(rdiff / sqrt(d2));
      a[cnt] = A.point(base + ang);
      b[cnt] = B.point(base + ang);
      ++cnt;
      a[cnt] = A.point(base - ang);
      b[cnt] = B.point(base - ang);
      ++cnt;
      if (dcmp(d2 - rsum * rsum) == 0) {  // 一条内公切线
        a[cnt] = A.point(base);
        b[cnt] = B.point(PI + base);
        ++cnt;
      } else if (dcmp(d2 - rsum * rsum) > 0) {  // 两条内公切线
        double ang = acos(rsum / sqrt(d2));
        a[cnt] = A.point(base + ang);
        b[cnt] = B.point(PI + base + ang);
        ++cnt;
        a[cnt] = A.point(base - ang);
        b[cnt] = B.point(PI + base - ang);
        ++cnt;
      }
      return cnt;
    }
    
    // 点 O 在圆 A 外，求圆 A 的反演圆 B，R 是反演半径
    Circle Inversion_C2C(Point O, double R, Circle A) {
      double OA = Length(A.c - O);
      double RB = 0.5 * ((1 / (OA - A.r)) - (1 / (OA + A.r))) * R * R;
      double OB = OA * RB / A.r;
      double Bx = O.x + (A.c.x - O.x) * OB / OA;
      double By = O.y + (A.c.y - O.y) * OB / OA;
      return Circle(Point(Bx, By), RB);
    }
    
    // 直线反演为过 O 点的圆 B，R 是反演半径
    Circle Inversion_L2C(Point O, double R, Point A, Vector v) {
      Point P = GetLineProjection(O, A, A + v);
      double d = Length(O - P);
      double RB = R * R / (2 * d);
      Vector VB = (P - O) / d * RB;
      return Circle(O + VB, RB);
    }
    
    // 返回 true 如果 A B 两点在直线同侧
    bool theSameSideOfLine(Point A, Point B, Point S, Vector v) {
      return dcmp(Cross(A - S, v)) * dcmp(Cross(B - S, v)) > 0;
    }
    
    int main() {
      int T;
      scanf("%d", &T);
      while (T--) {
        Circle A, B;
        Point P;
        scanf("%lf%lf%lf", &A.c.x, &A.c.y, &A.r);
        scanf("%lf%lf%lf", &B.c.x, &B.c.y, &B.r);
        scanf("%lf%lf", &P.x, &P.y);
        Circle NA = Inversion_C2C(P, 10, A);
        Circle NB = Inversion_C2C(P, 10, B);
        Point LA[N], LB[N];
        Circle ansC[N];
        int q = getTangents(NA, NB, LA, LB), ans = 0;
        for (int i = 0; i < q; ++i)
          if (theSameSideOfLine(NA.c, NB.c, LA[i], LB[i] - LA[i])) {
            if (!theSameSideOfLine(P, NA.c, LA[i], LB[i] - LA[i])) continue;
            ansC[ans++] = Inversion_L2C(P, 10, LA[i], LB[i] - LA[i]);
          }
        printf("%d\n", ans);
        for (int i = 0; i < ans; ++i) {
          printf("%.8f %.8f %.8f\n", ansC[i].c.x, ansC[i].c.y, ansC[i].r);
        }
      }
    
      return 0;
    }
    ```

## 练习

[「ICPC 2017 南宁赛区网络赛」Finding the Radius for an Inserted Circle](https://vjudge.net/problem/%E8%AE%A1%E8%92%9C%E5%AE%A2-A1283)

[「CCPC 2017 网络赛」The Designer](https://acm.hdu.edu.cn/showproblem.php?pid=6158)

## 参考资料与拓展阅读

-   [Inversive geometry - Wikipedia](https://en.wikipedia.org/wiki/Inversive_geometry)

-   [圆的反演变换 - ACdreamers 的博客](https://blog.csdn.net/acdreamers/article/details/16966369)


## geometry/nearest-points.md

## 引入

给定 $n$ 个二维平面上的点，求一组欧几里得距离最近的点对．

下面我们介绍一种时间复杂度为 $O(n\log n)$ 的分治算法来解决这个问题．该算法在 1975 年由 [Franco P. Preparata](https://en.wikipedia.org/wiki/Franco_P._Preparata) 提出，Preparata 和 [Michael Ian Shamos](https://en.wikipedia.org/wiki/Michael_Ian_Shamos) 证明了该算法在决策树模型下是最优的．

## 过程

与常规的分治算法一样，我们将这个有 $n$ 个点的集合拆分成两个大小相同的集合 $S_1, S_2$，并不断递归下去．但是我们遇到了一个难题：如何合并？即如何求出一个点在 $S_1$ 中，另一个点在 $S_2$ 中的最近点对？这里我们先假设合并操作的时间复杂度为 $O(n)$，可知算法总复杂度为 $T(n) = 2T(\frac{n}{2}) + O(n) = O(n\log n)$．

我们先将所有点按照 $x_i$ 为第一关键字、$y_i$ 为第二关键字排序，并以点 $p_m (m = \lfloor \frac{n}{2} \rfloor)$ 为分界点，拆分点集为 $A_1,A_2$：

$$
\begin{aligned}
A_1 &= \{p_i \ \big | \ i = 0 \ldots m \}\\
A_2 &= \{p_i \ \big | \ i = m + 1 \ldots n-1 \}
\end{aligned}
$$

并递归下去，求出两点集各自内部的最近点对，设距离为 $h_1,h_2$，取较小值设为 $h$．

现在该合并了！我们试图找到这样的一组点对，其中一个属于 $A_1$，另一个属于 $A_2$，且二者距离小于 $h$．因此我们将所有横坐标与 $x_m$ 的差小于 $h$ 的点放入集合 $B$：

$$
B = \{ p_i \ \big | \ \lvert x_i - x_m \rvert < h \}
$$

结合图像，直线 $m$ 将点分成了两部分．$m$ 左侧为 $A_1$ 点集，右侧为 $A_2$ 点集．

再根据 $B = \{ p_i \ \big | \ \lvert x_i - x_m \rvert < h \}$ 规则，得到绿色点组成的 $B$ 点集．![nearest-points1](./images/nearest-points1.png)

对于 $B$ 中的每个点 $p_i$，我们当前目标是找到一个同样在 $B$ 中、且到其距离小于 $h$ 的点．为了避免两个点之间互相考虑，我们只考虑那些纵坐标小于 $y_i$ 的点．显然对于一个合法的点 $p_j$，$y_i - y_j$ 必须小于 $h$．于是我们获得了一个集合 $C(p_i)$：

$$
C(p_i) = \{ p_j\ \big |\ p_j \in B,\ y_i - h < y_j \le y_i \}
$$

在点集 $B$ 中选一点 $p_i$，根据 $C(p_i) = \{ p_j\ \big |\ p_j \in B,\ y_i - h < y_j \le y_i \}$ 的规则，得到了由红色方框内的黄色点组成的 $C$ 点集．

![nearest-points2](./images/nearest-points2.png)

如果我们将 $B$ 中的点按照 $y_i$ 排序，$C(p_i)$ 将很容易得到，即紧邻 $p_i$ 的连续几个点．

由此我们得到了合并的步骤：

1.  构建集合 $B$．
2.  将 $B$ 中的点按照 $y_i$ 排序．通常做法是 $O(n\log n)$，但是我们可以改变策略优化到 $O(n)$（下文讲解）．
3.  对于每个 $p_i \in B$ 考虑 $p_j \in C(p_i)$，对于每对 $(p_i,p_j)$ 计算距离并更新答案（当前所处集合的最近点对）．

注意到我们上文提到了两次排序，因为点坐标全程不变，第一次排序可以只在分治开始前进行一次．我们令每次递归返回当前点集按 $y_i$ 排序的结果，对于第二次排序，上层直接使用下层的两个分别排序过的点集归并即可．

似乎这个算法仍然不优，$|C(p_i)|$ 将处于 $O(n)$ 数量级，导致总复杂度不对．其实不然，其最大大小为 $7$，我们给出它的证明：

## 复杂度证明

我们已经了解到，$C(p_i)$ 中的所有点的纵坐标都在 $(y_i-h,y_i]$ 范围内；且 $C(p_i)$ 中的所有点，和 $p_i$ 本身，横坐标都在 $(x_m-h,x_m+h)$ 范围内．这构成了一个 $2h \times h$ 的矩形．

我们再将这个矩形拆分为两个 $h \times h$ 的正方形，不考虑 $p_i$，其中一个正方形中的点为 $C(p_i) \cap A_1$，另一个为 $C(p_i) \cap A_2$，且两个正方形内的任意两点间距离大于 $h$．（因为它们来自同一下层递归）

我们将一个 $h \times h$ 的正方形拆分为四个 $\frac{h}{2} \times \frac{h}{2}$ 的小正方形．可以发现，每个小正方形中最多有 $1$ 个点：因为该小正方形中任意两点最大距离是对角线的长度，即 $\frac{h}{\sqrt 2}$，该数小于 $h$．

![nearest-points3](./images/nearest-points3.png)

由此，每个正方形中最多有 $4$ 个点，矩形中最多有 $8$ 个点，去掉 $p_i$ 本身，$\max(C(p_i))=7$．

???+ example "参考实现"
    ```cpp
    --8<-- "docs/geometry/code/nearest-points/nearest-points_1.cpp"
    ```

## 推广：平面最小周长三角形

上述算法有趣地推广到这个问题：在给定的一组点中，选择三个点，使得它们两两的距离之和最小．

算法大体保持不变，每次尝试找到一个比当前答案周长 $d$ 更小的三角形，将所有横坐标与 $x_m$ 的差小于 $\frac{d}{2}$ 的点放入集合 $B$，尝试更新答案．（周长为 $d$ 的三角形的最长边小于 $\frac{d}{2}$）

## 非分治算法

其实，除了上面提到的分治算法，还有另一种时间复杂度同样是 $O(n \log n)$ 的非分治算法．

我们可以考虑一种常见的统计序列的思想：对于每一个元素，将它和它的左边所有元素的贡献加入到答案中．平面最近点对问题同样可以使用这种思想．

具体地，我们把所有点按照 $x_i$ 为第一关键字、$y_i$ 为第二关键字排序，并建立一个以 $y_i$ 为关键字的 multiset．对于每一个位置 $i$，我们执行以下操作：

1.  将所有满足 $x_i - x_j \ge d$ 的点从集合中删除．它们不会再对答案有贡献．
2.  对于集合内满足 $\lvert y_i - y_j \rvert < d$ 的所有点，统计它们和 $p_i$ 的距离．
3.  将 $p_i$ 插入到集合中．

由于每个点最多会被插入和删除一次，所以插入和删除点的时间复杂度为 $O(n \log n)$，而统计答案部分的时间复杂度证明与分治算法的时间复杂度证明方法类似，读者不妨一试．

??? example "参考实现"
    ```cpp
    --8<-- "docs/geometry/code/nearest-points/nearest-points_2.cpp"
    ```

## 期望线性做法

其实，除了上面提到的时间复杂度为 $O(n \log n)$ 的做法，还有一种 **期望** 复杂度为 $O(n)$ 的算法．

首先将点对 [随机打乱](../misc/random.md#shuffle)，我们将维护前缀点集的答案．考虑从前 $i - 1$ 个点求出第 $i$ 个点的答案．

记前 $i - 1$ 个点的最近点对距离为 $s$，我们将平面以 $s$ 为边长划分为若干个网格，并存下每个网格内的点（使用 [哈希表](../ds/hash.md)），然后检查第 $i$ 个点所在网格的周围九个网格中的所有点，并更新答案．注意到需检查的点的个数是 $O(1)$ 的，因为前 $i - 1$ 个点的最近点对距离为 $s$，从而每个网格不超过 $4$ 个点．

如果这一过程中，答案被更新，我们就重构网格图，否则不重构．在前 $i$ 个点中，最近点对包含 $i$ 的概率为 $O\left(\frac{1}{i}\right)$，而重构网格的代价为 $O(i)$，从而第 $i$ 个点的期望代价为 $O(1)$．于是对于 $n$ 个点，该算法期望为 $O(n)$．

## 习题

-   [UVa 10245 "The Closest Pair Problem"\[难度：低\]](https://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=1186)
-   [SPOJ #8725 CLOPPAIR "Closest Point Pair"\[难度：低\]](https://www.spoj.com/problems/CLOPPAIR/)
-   [CODEFORCES Team Olympiad Saratov - 2011 "Minimum amount"\[难度：中\]](http://codeforces.com/contest/120/problem/J)
-   [SPOJ #7029 CLOSEST "Closest Triple"\[难度：中\]](https://www.spoj.com/problems/CLOSEST/)
-   [Google Code Jam 2009 Final "Min Perimeter"\[难度：中\]](https://github.com/google/coding-competitions-archive/blob/main/codejam/2009/world_finals/min_perimeter/statement.pdf)

## 参考资料与拓展阅读

**本页面中的分治算法部分主要译自博文 [Нахождение пары ближайших точек](http://e-maxx.ru/algo/nearest_points) 与其英文翻译版 [Finding the nearest pair of points](https://github.com/e-maxx-eng/e-maxx-eng/blob/master/src/geometry/nearest_points.md)．其中俄文版版权协议为 Public Domain + Leave a Link；英文版版权协议为 CC-BY-SA 4.0．**

[知乎专栏：计算几何 - 最近点对问题](https://zhuanlan.zhihu.com/p/74905629)


## geometry/pick.md

## Pick 定理

Pick 定理：给定顶点均为整点的简单多边形，皮克定理说明了其面积 ${\displaystyle A}$ 和内部格点数目 ${\displaystyle i}$、边上格点数目 ${\displaystyle b}$ 的关系：${\displaystyle A=i+{\frac {b}{2}}-1}$．

具体证明：[Pick's theorem](https://en.wikipedia.org/wiki/Pick%27s_theorem)

它有以下推广：

-   取格点的组成图形的面积为一单位．在平行四边形格点，皮克定理依然成立．套用于任意三角形格点，皮克定理则是 ${\displaystyle A=2 \times i+b-2}$．
-   对于非简单的多边形 ${\displaystyle P}$，皮克定理 ${\displaystyle A=i+{\frac {b}{2}}-\chi (P)}$，其中 ${\displaystyle \chi (P)}$ 表示 ${\displaystyle P}$ 的 **欧拉特征数**．
-   高维推广：Ehrhart 多项式
-   皮克定理和 **欧拉公式**（${\displaystyle V-E+F=2}$）等价．

## 一道例题 ([POJ 1265](http://poj.org/problem?id=1265))

### 题目大意

在直角坐标系中，一个机器人从任意点出发进行 $\textit{n}$ 次移动，每次向右移动 $\textit{dx}$，向上移动 $\textit{dy}$，最后会形成一个平面上的封闭简单多边形，求边上的点的数量，多边形内的点的数量，多边形面积．

### 题解

这道题目其实用了以下三个知识：

-   以整点为顶点的线段，如果边 $\textit{dx}$ 和 $\textit{dy}$ 都不为 $0$，经过的格点数是 $\gcd(\textit{dx}, \textit{dy}) + 1$，当然，如果要算一整个图形的，多加的点会被上一条边计算，也就不需要加了．那么一条边覆盖的点的个数为 $\gcd(\textit{dx},\textit{dy})$，其中，$\textit{dx},\textit{dy}$ 分别为线段横向占的点数和纵向占的点数．如果 $\textit{dx}$ 或 $\textit{dy}$ 为 $0$，则覆盖的点数为 $\textit{dy}$ **或** $\textit{dx}$．
-   Pick 定理：平面上以整点为顶点的简单多边形的面积 = 边上的点数/2 + 内部的点数 - 1．
-   任意一个多边形的面积等于按顺序求相邻两个点与原点组成的向量的叉积之和的一半（这个也可以通过顺时针定积分求得）．

??? note "参考代码"
    ```cpp
    --8<-- "docs/geometry/code/pick/pick_1.cpp"
    ```


## geometry/random-incremental.md

author: Ir1d, TianyiQ

## 引入

随机增量算法是计算几何的一个重要算法，它对理论知识要求不高，算法时间复杂度低，应用范围广大．

增量法 (Incremental Algorithm) 的思想与第一数学归纳法类似，它的本质是将一个问题化为规模刚好小一层的子问题．解决子问题后加入当前的对象．写成递归式是：

$$
T(n)=T(n-1)+g(n)
$$

增量法形式简洁，可以应用于许多的几何题目中．

增量法往往结合随机化，可以避免最坏情况的出现．

## 最小圆覆盖问题

### 题意描述

在一个平面上有 $n$ 个点，求一个半径最小的圆，能覆盖所有的点．

### 过程

假设圆 $O$ 是前 $i-1$ 个点的最小覆盖圆，加入第 $i$ 个点，如果在圆内或边上则什么也不做．否则，新得到的最小覆盖圆肯定经过第 $i$ 个点．

然后以第 $i$ 个点为基础（半径为 $0$），重复以上过程依次加入第 $j$ 个点，若第 $j$ 个点在圆外，则最小覆盖圆必经过第 $j$ 个点．

重复以上步骤．（因为最多需要三个点来确定这个最小覆盖圆，所以重复三次）

遍历完所有点之后，所得到的圆就是覆盖所有点得最小圆．

### 性质

**时间复杂度**  $O(n)$，证明详见参考资料．

**空间复杂度**  $O(n)$

### 实现

??? note "代码实现"
    ```cpp
    #include <cmath>
    #include <cstdio>
    #include <cstdlib>
    #include <cstring>
    #include <iostream>
    
    using namespace std;
    
    int n;
    double r;
    
    struct point {
      double x, y;
    } p[100005], o;
    
    double sqr(double x) { return x * x; }
    
    double dis(point a, point b) { return sqrt(sqr(a.x - b.x) + sqr(a.y - b.y)); }
    
    bool cmp(double a, double b) { return fabs(a - b) < 1e-8; }
    
    point geto(point a, point b, point c) {
      double a1, a2, b1, b2, c1, c2;
      point ans;
      a1 = 2 * (b.x - a.x), b1 = 2 * (b.y - a.y),
      c1 = sqr(b.x) - sqr(a.x) + sqr(b.y) - sqr(a.y);
      a2 = 2 * (c.x - a.x), b2 = 2 * (c.y - a.y),
      c2 = sqr(c.x) - sqr(a.x) + sqr(c.y) - sqr(a.y);
      if (cmp(a1, 0)) {
        ans.y = c1 / b1;
        ans.x = (c2 - ans.y * b2) / a2;
      } else if (cmp(b1, 0)) {
        ans.x = c1 / a1;
        ans.y = (c2 - ans.x * a2) / b2;
      } else {
        ans.x = (c2 * b1 - c1 * b2) / (a2 * b1 - a1 * b2);
        ans.y = (c2 * a1 - c1 * a2) / (b2 * a1 - b1 * a2);
      }
      return ans;
    }
    
    int main() {
      scanf("%d", &n);
      for (int i = 1; i <= n; i++) scanf("%lf%lf", &p[i].x, &p[i].y);
      for (int i = 1; i <= n; i++) swap(p[rand() % n + 1], p[rand() % n + 1]);
      o = p[1];
      for (int i = 1; i <= n; i++) {
        if (dis(o, p[i]) < r || cmp(dis(o, p[i]), r)) continue;
        o.x = (p[i].x + p[1].x) / 2;
        o.y = (p[i].y + p[1].y) / 2;
        r = dis(p[i], p[1]) / 2;
        for (int j = 2; j < i; j++) {
          if (dis(o, p[j]) < r || cmp(dis(o, p[j]), r)) continue;
          o.x = (p[i].x + p[j].x) / 2;
          o.y = (p[i].y + p[j].y) / 2;
          r = dis(p[i], p[j]) / 2;
          for (int k = 1; k < j; k++) {
            if (dis(o, p[k]) < r || cmp(dis(o, p[k]), r)) continue;
            o = geto(p[i], p[j], p[k]);
            r = dis(o, p[i]);
          }
        }
      }
      printf("%.10lf\n%.10lf %.10lf", r, o.x, o.y);
      return 0;
    }
    ```

## 练习

[最小圆覆盖](https://www.luogu.com.cn/problem/P1742)

[「HNOI2012」射箭](https://www.luogu.com.cn/problem/P3222)

[CodeForces 442E](https://codeforces.com/problemset/problem/442/E)

## 参考资料与扩展阅读

[随机增量算法 - 解轶伦](https://github.com/hzwer/shareOI/blob/master/%E8%AE%A1%E7%AE%97%E5%87%A0%E4%BD%95/%E9%9A%8F%E6%9C%BA%E5%A2%9E%E9%87%8F%E7%AE%97%E6%B3%95_%E8%A7%A3%E8%BD%B6%E4%BC%A6.pdf)

<https://www.cnblogs.com/aininot260/p/9635757.html>

<https://www.cise.ufl.edu/~sitharam/COURSES/CG/kreveldnbhd.pdf>

<https://blog.csdn.net/u014609452/article/details/62039612>


## geometry/rotating-calipers.md

本页面将主要介绍旋转卡壳．

## 引入

旋转卡壳（Rotating Calipers，也称「旋转卡尺」）算法，在凸包算法的基础上，通过枚举凸包上某一条边的同时维护其他需要的点，能够在线性时间内求解如凸包直径、最小矩形覆盖等和凸包性质相关的问题．

???+ note "算法中文名称"
    该算法比较常见的中文名是「旋转卡壳」．可以理解为：根据我们枚举的边，可以从每个维护的点画出一条或平行或垂直的直线，为了确保对于当前枚举的边的最优性，我们的任务就是使这些直线能将凸包正好卡住．而边通常是按照向某一方向旋转的顺序来枚举，所以整个过程就是在边「旋转」，边「卡壳」．
    
    其英文名「rotating calipers」的直译应为「旋转卡尺」，其中「calipers」的意思是「卡尺」．第一次提出该术语的论文[^ref1]原意为：使用一个可动态调整的「卡尺」夹住凸包后，绕凸包「旋转」该「卡尺」．

## 求凸包直径

???+ note "例题 1 :[Luogu P1452 Beauty Contest G](https://www.luogu.com.cn/problem/P1452)"
    给定平面上 $n$ 个点，求所有点对之间的最长距离．（$2\leq n \leq 50000,|x|,|y| \leq 10^4$）

### 过程

首先使用任何一种凸包算法求出给定所有点的凸包，有着最长距离的点对一定在凸包上．而由于凸包的形状，我们发现，逆时针地遍历凸包上的边，对于每条边都找到离这条边最远的点，那么这时随着边的转动，对应的最远点也在逆时针旋转，不会有反向的情况，这意味着我们可以在逆时针枚举凸包上的边时，记录并维护一个当前最远点，并不断计算、更新答案．

求出凸包后的数组自然地是按照逆时针旋转的顺序排列，不过要记得提前将最左下角的 1 节点补到数组最后，这样在挨个枚举边 $(i,i+1)$ 时，才能把所有边都枚举到．

![](images/rotating-calipers1.png)

枚举过程中，对于每条边，都检查 $j+1$ 和边 $(i,i+1)$ 的距离是不是比 $j$ 更大，如果是就将 $j$ 加一，否则说明 $j$ 是此边的最优点．判断点到边的距离大小时可以用叉积分别算出两个三角形的面积（如图，黄、蓝两个同底三角形的面积）并直接比较．

### 实现

???+ note "核心代码"
    === "C++"
        ```cpp
        int sta[N], top;  // 将凸包上的节点编号存在栈里，第一个和最后一个节点编号相同
        
        ll pf(ll x) { return x * x; }
        
        ll dis(int p, int q) { return pf(a[p].x - a[q].x) + pf(a[p].y - a[q].y); }
        
        ll sqr(int p, int q, int y) { return abs((a[q] - a[p]) * (a[y] - a[q])); }
        
        ll mx;
        
        void get_longest() {  // 求凸包直径
          int j = 3;
          if (top < 4) {
            mx = dis(sta[1], sta[2]);
            return;
          }
          for (int i = 1; i < top; ++i) {
            while (sqr(sta[i], sta[i + 1], sta[j]) <=
                   sqr(sta[i], sta[i + 1], sta[j % top + 1]))
              j = j % top + 1;
            mx = max(mx, max(dis(sta[i + 1], sta[j]), dis(sta[i], sta[j])));
          }
        }
        ```
    
    === "Python"
        ```python
        sta = [0] * N
        top = 0  # 将凸包上的节点编号存在栈里，第一个和最后一个节点编号相同
        
        
        def pf(x):
            return x * x
        
        
        def dis(p, q):
            return pf(a[p].x - a[q].x) + pf(a[p].y - a[q].y)
        
        
        def sqr(p, q, y):
            return abs((a[q] - a[p]) * (a[y] - a[q]))
        
        
        def get_longest():  # 求凸包直径
            j = 3
            if top < 4:
                mx = dis(sta[1], sta[2])
                return
            for i in range(1, top):
                while sqr(sta[i], sta[i + 1], sta[j]) <= sqr(
                    sta[i], sta[i + 1], sta[j % top + 1]
                ):
                    j = j % top + 1
                mx = max(mx, max(dis(sta[i + 1], sta[j]), dis(sta[i], sta[j])))
        ```

## 求最小矩形覆盖

[Luogu P3187 最小矩形覆盖](https://www.luogu.com.cn/problem/P3187)

给定一些点的坐标，求能够覆盖所有点的最小面积的矩形．（$3\leq n \leq 50000$）

### 过程

有了上一道题做铺垫，这道题比较直观的想法仍然是使用旋转卡壳法，不过这次要求的是面积，像上一题一样只维护一个最优点就只能找到一对距离最小的平行线，我们还需要确定矩形的左右边界．所以这次我们需要维护三个点：一个在所枚举的直线对面的点、两个在不同侧面的点．对面的最优点仍然是用叉积算面积来比较，此时比较面积就是在比较这个矩形的一个边长．侧面的最优点则是用点积来比较，因为比较点积就是比较投影的长度，左右两个投影长度相加可以代表这个矩形的另一个边长．这两个边长的最优性相互独立，因此找到三个最优点的位置就能够确定以当前边所在直线为矩阵的一条边时，能覆盖所有点的矩形最小面积．

![](images/rotating-calipers2.png)

最后统计答案时，如果题目没有要求将四个顶点都求出来，其实有一种较为巧妙的利用叉积和点积的方式直接算出矩阵的面积．设紫色部分面积的两倍为 $S$，最后的面积就是

$$
S\times (|\overrightarrow{AD}\cdot \overrightarrow{AB}|+|\overrightarrow{BC}\cdot \overrightarrow{BA}|-|\overrightarrow{AB}\cdot \overrightarrow{BA}|)/|\overrightarrow{AB}\cdot \overrightarrow{BA}|
$$

### 实现

必要的求凸包过程略去，这里贴出本题核心代码：

???+ note "核心代码"
    === "C++"
        ```cpp
        void get_biggest() {
          int j = 3, l = 2, r = 2;
          double t1, t2, t3, ans = 2e10;
          for (int i = 1; i < top; ++i) {
            while (sqr(sta[i], sta[i + 1], sta[j]) <=
                   sqr(sta[i], sta[i + 1], sta[j % top + 1]))
              j = j % top + 1;
            while (dot(sta[i + 1], sta[r % top + 1], sta[i]) >=
                   dot(sta[i + 1], sta[r], sta[i]))
              r = r % top + 1;
            if (i == 1) l = r;
            while (dot(sta[i + 1], sta[l % top + 1], sta[i]) <=
                   dot(sta[i + 1], sta[l], sta[i]))
              l = l % top + 1;
            t1 = sqr(sta[i], sta[i + 1], sta[j]);
            t2 = dot(sta[i + 1], sta[r], sta[i]) + dot(sta[i + 1], sta[l], sta[i]);
            t3 = dot(sta[i + 1], sta[i + 1], sta[i]);
            ans = min(ans, t1 * t2 / t3);
          }
        }
        ```
    
    === "Python"
        ```python
        def get_biggest():
            j = 3
            l = 2
            r = 2
            ans = 2e10
            for i in range(1, top):
                while sqr(sta[i], sta[i + 1], sta[j]) <= sqr(
                    sta[i], sta[i + 1], sta[j % top + 1]
                ):
                    j = j % top + 1
                while dot(sta[i + 1], sta[r % top + 1], sta[i]) >= dot(
                    sta[i + 1], sta[r], sta[i]
                ):
                    r = r % top + 1
                if i == 1:
                    l = r
                while dot(sta[i + 1], sta[l % top + 1], sta[i]) <= dot(
                    sta[i + 1], sta[l], sta[i]
                ):
                    l = l % top + 1
                t1 = sqr(sta[i], sta[i + 1], sta[j])
                t2 = dot(sta[i + 1], sta[r], sta[i]) + dot(sta[i + 1], sta[l], sta[i])
                t3 = dot(sta[i + 1], sta[i + 1], sta[i])
                ans = min(ans, t1 * t2 / t3)
        ```

## 练习

-   [POJ 3608. Bridge Across Islands](http://poj.org/problem?id=3608)
-   [2011 ACM-ICPC World Finals, Problem K. Trash Removal](https://codeforces.com/gym/101175)
-   [ICPC WF Moscow Invitational Contest - Online Mirror, Problem F. Framing Pictures](https://codeforces.com/contest/1578/problem/F)

## 参考资料与注释

[^ref1]: Toussaint, Godfried T. (1983). "Solving geometric problems with the rotating calipers". Proc. MELECON '83, Athens. CiteSeerX 10.1.1.155.5671

-   <https://en.wikipedia.org/wiki/Rotating_calipers>

-   <http://www-cgrl.cs.mcgill.ca/~godfried/research/calipers.html>

-   Shamos, Michael (1978). "Computational Geometry" (PDF). Yale University. pp. 76–81.


## geometry/scanning.md

## 引入

扫描线一般运用在图形上面，它和它的字面意思十分相似，就是一条线在整个图上扫来扫去，它一般被用来解决图形面积，周长，以及二维数点等问题．

## 二维矩形面积并问题

在二维坐标系上，给出多个矩形的左下以及右上坐标，求出所有矩形构成的图形的面积．

### 过程

根据图片可知总面积可以直接暴力即可求出面积，如果数据大了怎么办？这时就需要讲到 **扫描线** 算法．

现在假设我们有一根线，从下往上开始扫描：

![](./images/scanning.svg)

如图所示，把整个矩形分成如图各个颜色不同的小矩形，小矩形的高是扫过的距离，然而矩形的水平宽一直在变化．

给每一个矩形的上下边进行标记，下面的边标记为 1，上面的边标记为 -1．每遇到一个水平边时，让这条边（在横轴投影区间）的权值加上这条边的标记．

???+ note "Note"
    这个操作类似遍历括号序列：开括号加 1，闭括号减 1，「权值」对应当前位置的深度，「权值」是否大于 0，对应当前在不在括号里，也就是这段区间是否记入小矩形的宽度．

小矩形（不一定只有一个）的宽度就是整个数轴上权值大于 0 的区间总长度．

### 实现

用线段树维护矩形的长，也就是整个数轴上覆盖次数大于 0 的点．需求列举如下：

-   一段区间权值加 1、减 1．
-   统计整个数轴上，区间权值大于 0 的「区间长度和」．

如果你尝试直接用普通线段树模板来实现的话，也许会遇到些挫折．具体地，由于在区间加时，即使修改区间和节点管理区间重合，我们还是不能常数时间知道覆盖次数如何变化．这是因为我们不能直接知道：管理范围里有多长的区间会从 1 变成 0（从 0 变成 1）．

这道题只需要朴素的分治就能实现：维护每个节点管理区间中「完全覆盖区间的次数 `v[]`」（类似不用下放的懒惰标记）和「已覆盖的长度 `w[]`」两个信息．

需要 [离散化](../misc/discrete.md)．

??? note "[洛谷 P5490【模板】扫描线 & 矩形面积并](https://www.luogu.com.cn/problem/P5490) 参考代码"
    ```cpp
    --8<-- "docs/geometry/code/scanning/scanning_1.cpp"
    ```

??? note "[「POJ 1151」Atlantis](http://poj.org/problem?id=1151) 参考代码"
    ```cpp
    --8<-- "docs/geometry/code/scanning/scanning_2.cpp"
    ```

### 练习

-   [「POJ1177」Picture](http://poj.org/problem?id=1177)
-   [「POJ3832」Posters](http://poj.org/problem?id=3832)
-   [洛谷 P1856 \[IOI1998\] \[USACO5.5\] 矩形周长 Picture](https://www.luogu.com.cn/problem/P1856)
    -   横边贡献就是覆盖长度变化量．
    -   两个方向分别算一次可以避免竖直边的讨论．
    -   操作排序时注意考虑两个矩形边重合的情况．
    -   数据范围允许不用线段树，直接平方时间模拟．

## B 维正交范围

B 维正交范围指在一个 B 维直角坐标系下，第 $i$ 维坐标在一个整数范围 $[l_i,r_i]$ 间，内部的点集．

一般来说，一维正交范围简称区间，二维正交范围简称矩形，三维正交范围简称立方体（我们常说的二维数点就是二维正交范围）．

对于一个静态的二维问题，我们可以使用扫描线扫一维，数据结构维护另一维．
在扫描线从左到右扫的过程中，会在数据结构维护的那一维上产生一些修改与查询．
如果查询的信息可差分的话直接使用差分，否则需要使用分治．差分一般用树状数组和线段树维护，但因为树状数组好写而且常数小，所以大部分人会选择用树状数组来维护．分治一般是 CDQ 分治（但是这里不涉及分治）．

另一种比较容易理解的看待问题的角度是站在序列角度，而不站在二维平面角度．如果我们这样看待问题，则扫描线实际上是枚举了右端点 $r=1\cdots n$，维护一个数据结构，支持查询对于当前的 $r$，给定一个值 $l$，$l$ 到 $r$ 的答案是什么．即扫描线扫询问右端点，数据结构维护所有左端点的答案，或者说遍历一维，数据结果维护另一维．

复杂度一般为 $O((n+m)\log n)$．

## 二维数点

给一个长为 $n$ 的序列，有 $m$ 次查询，每次查区间 $[l,r]$ 中值在 $[x,y]$ 内的元素个数．

这个问题就叫做二维数点．我们可以发现等价于我们要查询一个二维平面上矩形内的点的数量和．这里讲一下这个问题最简单的处理方法，扫描线 + 树状数组．

很显然，这个问题是一个静态的二维问题，我们通过扫描线可以将静态的二维问题转换为动态的一维问题．维护动态的一维问题就使用数据结构维护序列，这里可以使用树状数组．

先将所有的询问离散化，用树状数组维护权值，对于每次询问的 $l$ 和 $r$，我们在枚举到 $l-1$ 时统计当前位于区间 $[x,y]$ 内的数的数量 $a$，继续向后枚举，枚举到 $r$ 时统计当前位于区间 $[x,y]$ 内的数的数量 $b$，$b-a$ 即为该次询问的答案．

### 例题

???+ note "[洛谷 P2163 \[SHOI2007\] 园丁的烦恼](https://www.luogu.com.cn/problem/P2163)"
    首先离散化．设一个左下角为 $(0, 0)$，右上角为 $(x, y)$ 的矩形内包含 $ans_{x, y}$ 个点．则询问的答案可以被差分为 $ans_{c, d} - ans_{a - 1, d} - ans_{c, b - 1} + ans_{a - 1, b - 1}$．
    
    ??? note "代码"
        ```cpp
        --8<-- "docs/geometry/code/scanning/scanning_3.cpp"
        ```

???+ note "[洛谷 P1908 逆序对](https://www.luogu.com.cn/problem/P1908)"
    没错，逆序对也可以用扫描线的思维来做．考虑将求逆序对的个数转化为从后向前枚举每个位置 $i$，求在区间 $[i+1,n]$ 中，大小在区间 $[0,a_i]$ 中的点的个数．题目中数据范围为 $10^9$，很显然要先进行离散化，我们可以考虑从后向前遍历数组，每次遍历到一个数时更新树状数组（线段树），之后统计当前一共有多少个数小于当前枚举的数，因为我们是从后向前遍历的，所以比当前值小的数的个数就是他的逆序对的个数，可以用树状数组或线段树进行单点修改和区间查询．
    
    ??? note "代码"
        ```cpp
        --8<-- "docs/geometry/code/scanning/scanning_4.cpp"
        ```

???+ note "[洛谷 P1972 \[SDOI2009\] HH 的项链](https://www.luogu.com.cn/problem/P1972)"
    简要题意：给定一个序列，多次询问区间 $[l,r]$ 中有多少种不同的数．
    
    这类问题我们可以考虑推导性质，之后使用扫描线枚举所有右端点，数据结构维护每个左端点的答案的方法来实现，我们也可以将问题转换到二维平面上，变为一个矩形查询信息的问题．
    
    在本题中，我们设序列中 $a_i$ 上一次出现的位置为 $pre_i$，如果 $a_i$ 没有出现过，则 $pre_i = 0$．根据题意，如果一种数在区间中出现多次，只会产生一次贡献．不妨认为每种数产生贡献的位置是区间中第一次出现的位置，这时可以发现，产生的总贡献即为 $pre_x \le l - 1$ 的个数，反证法易证．
    
    现在问题即为：给定一个序列 $pre$，多次查询区间 $[l,r]$ 中有多少个 $pre_i \le l - 1$．
    
    我们可以把 $pre_i$ 看成二维平面的点：$i$ 是横坐标，$pre_i$ 是纵坐标，问题就转化为了二维数点问题：每次询问左下角为 $(l,0)$，右上角为 $(r,l - 1)$ 的矩形中有几个点．
    
    注意到这个询问是可差分的，我们可以将询问差分为左下角为 $(0,0)$，右上角为 $(r,l - 1)$ 的矩形减去左下角为 $(0,0)$，右上角为 $(l - 1,l - 1)$ 的矩形有几个点，这样方便我们使用扫描线思想．
    
    单次操作复杂度 $O(\log n)$，共有 $n$ 次加点操作和 $2m$ 次查询操作，总时间复杂度 $O((n + m) \log n)$．
    
    ??? note "代码"
        ```cpp
        --8<-- "docs/geometry/code/scanning/scanning_5.cpp"
        ```

### 练习

-   [洛谷 P8593「KDOI-02」一个弹的投](https://www.luogu.com.cn/problem/P8593) 逆序对的应用．
-   [AcWing 4709. 三元组](https://www.acwing.com/problem/content/4712/) 上题的弱化版，同样为逆序对的应用．
-   [洛谷 P8773 \[蓝桥杯 2022 省 A\] 选数异或](https://www.luogu.com.cn/problem/P8773) HH 的项链魔改版．
-   [洛谷 P8844 \[传智杯 #4 初赛\] 小卡与落叶](https://www.luogu.com.cn/problem/P8844) 树上问题转序列问题然后进行二维数点．

总而言之，二维数点的主要思路就是数据结构维护一维，然后枚举另一维．

## 参考资料

-   [cnblogs/Yang1208：扫描线讲解，动态开点版线段树](https://www.cnblogs.com/yangsongyi/p/8378629.html)
-   [csdn/riba2534：POJ1151 Atlantis 题解](https://blog.csdn.net/riba2534/article/details/76851233)
-   [csdn/刀刀狗 0102：POJ1151 Atlantis 题解](https://blog.csdn.net/winddreams/article/details/38495093)
-   [浅谈扫描线](https://www.luogu.com.cn/article/f8q5bmnz)


## geometry/triangulation.md

author: xehoth

在几何中，三角剖分是指将平面对象细分为三角形，并且通过扩展将高维几何对象细分为单纯形．
对于一个给定的点集，有很多种三角剖分，如：

![三种三角剖分](./images/triangulation-0.svg)

OI 中的三角剖分主要指二维几何中的完美三角剖分（二维 Delaunay 三角剖分，简称 DT）．

## Delaunay 三角剖分

### 定义

在数学和计算几何中，对于给定的平面中的离散点集 $P$，其 Delaunay 三角剖分 DT($P$) 满足：

1.  空圆性：DT($P$) 是 **唯一** 的（任意四点不能共圆），在 DT($P$) 中，**任意** 三角形的外接圆范围内不会有其它点存在．
2.  最大化最小角：在点集 $P$ 可能形成的三角剖分中，DT($P$) 所形成的三角形的最小角最大．从这个意义上讲，DT($P$) 是 **最接近于规则化** 的三角剖分．具体的说是在两个相邻的三角形构成凸四边形的对角线，在相互交换后，两个内角的最小角不再增大．

![一个显示了外接圆的 Delaunay 三角剖分](./images/triangulation-1.png)

### 性质

1.  最接近：以最接近的三点形成三角形，且各线段（三角形的边）皆不相交．
2.  唯一性：不论从区域何处开始构建，最终都将得到一致的结果（点集中任意四点不能共圆）．
3.  最优性：任意两个相邻三角形构成的凸四边形的对角线如果可以互换的话，那么两个三角形六个内角中最小角度不会变化．
4.  最规则：如果将三角剖分中的每个三角形的最小角进行升序排列，则 Delaunay 三角剖分的排列得到的数值最大．
5.  区域性：新增、删除、移动某一个顶点只会影响邻近的三角形．
6.  具有凸边形的外壳：三角剖分最外层的边界形成一个凸多边形的外壳．

## 构造 DT 的分治算法

DT 有很多种构造算法，在 $O(n \log n)$ 的构造算法中，分治算法是最易于理解和实现的．

分治构造 DT 的第一步是将给定点集按照 $x$ 坐标 **升序** 排列，如下图是排好序的大小为 $10$ 的点集．

![排好序的大小为 10 的点集](./images/triangulation-2.svg)

一旦点集有序，我们就可以不断地将其分成两个部分（分治），直到子点集大小不超过 $3$．然后这些子点集可以立刻剖分为一个三角形或线段．

![分治为包含 2 或 3 个点的点集](./images/triangulation-3.svg)

然后在分治回溯的过程中，已经剖分好的左右子点集可以依次合并．合并后的剖分包含 LL-edge（左侧子点集的边）．RR-edge（右侧子点集的边），LR-edge（连接左右剖分产生的新的边），如图 LL-edge（灰色），RR-edge（红色），LR-edge（蓝色）．对于合并后的剖分，为了维持 DT 性质，我们 **可能** 需要删除部分 LL-edge 和 RR-edge，但我们在合并时 **不会** 增加 LL-edge 和 RR-edge．

![edge](./images/triangulation-4.svg)

合并左右两个剖分的第一步是插入 base LR-edge，base LR-edge 是 **最底部** 的不与 **任何** LL-edge 及 RR-edge 相交的 LR-edge．

![合并左右剖分](./images/triangulation-5.svg)

然后，我们需要确定下一条 **紧接在** base LR-edge 之上的 LR-edge．比如对于右侧点集，下一条 LR-edge 的可能端点（右端点）为与 base LR-edge 右端点相连的 RR-edge 的另一端点（$6, 7, 9$ 号点），左端点即为 $2$ 号点．

![下一条 LR-edge](./images/triangulation-6.svg)

对于可能的端点，我们需要按以下两个标准检验：

1.  其对应 RR-edge 与 base LR-edge 的夹角小于 $180$ 度．
2.  base LR-edge 两端点和这个可能点三点构成的圆内不包含任何其它 **可能点**．

![检验可能点](./images/triangulation-7.svg)

如上图，$6$ 号可能点所对应的绿色圆包含了 $9$ 号可能点，而 $7$ 号可能点对应的紫色圆则不包含任何其它可能点，故 $7$ 号点为下一条 LR-edge 的右端点．

对于左侧点集，我们做镜像处理即可．

![检验左侧可能点](./images/triangulation-8.svg)

当左右点集都不再含有符合标准的可能点时，合并即完成．当一个可能点符合标准，一条 LR-edge 就需要被添加，对于与需要添加的 LR-edge 相交的 LL-edge 和 RR-edge，将其删除．

当左右点集均存在可能点时，判断左边点所对应圆是否包含右边点，若包含则不符合；对于右边点也是同样的判断．一般只有一个可能点符合标准（除非四点共圆）．

![下一条 LR-edge](./images/triangulation-9.svg)

当这条 LR-edge 添加好后，将其作为 base LR-edge 重复以上步骤，继续添加下一条，直到合并完成．

![合并](./images/triangulation-10.svg)

## 代码

??? note "实现"
    ```cpp
    #include <algorithm>
    #include <cmath>
    #include <cstring>
    #include <list>
    #include <utility>
    #include <vector>
    
    constexpr double EPS = 1e-8;
    constexpr int MAXV = 10000;
    
    struct Point {
      double x, y;
      int id;
    
      Point(double a = 0, double b = 0, int c = -1) : x(a), y(b), id(c) {}
    
      bool operator<(const Point &a) const {
        return x < a.x || (fabs(x - a.x) < EPS && y < a.y);
      }
    
      bool operator==(const Point &a) const {
        return fabs(x - a.x) < EPS && fabs(y - a.y) < EPS;
      }
    
      double dist2(const Point &b) {
        return (x - b.x) * (x - b.x) + (y - b.y) * (y - b.y);
      }
    };
    
    struct Point3D {
      double x, y, z;
    
      Point3D(double a = 0, double b = 0, double c = 0) : x(a), y(b), z(c) {}
    
      Point3D(const Point &p) { x = p.x, y = p.y, z = p.x * p.x + p.y * p.y; }
    
      Point3D operator-(const Point3D &a) const {
        return Point3D(x - a.x, y - a.y, z - a.z);
      }
    
      double dot(const Point3D &a) { return x * a.x + y * a.y + z * a.z; }
    };
    
    struct Edge {
      int id;
      std::list<Edge>::iterator c;
    
      Edge(int id = 0) { this->id = id; }
    };
    
    int cmp(double v) { return fabs(v) > EPS ? (v > 0 ? 1 : -1) : 0; }
    
    double cross(const Point &o, const Point &a, const Point &b) {
      return (a.x - o.x) * (b.y - o.y) - (a.y - o.y) * (b.x - o.x);
    }
    
    Point3D cross(const Point3D &a, const Point3D &b) {
      return Point3D(a.y * b.z - a.z * b.y, -a.x * b.z + a.z * b.x,
                     a.x * b.y - a.y * b.x);
    }
    
    int inCircle(const Point &a, Point b, Point c, const Point &p) {
      if (cross(a, b, c) < 0) std::swap(b, c);
      Point3D a3(a), b3(b), c3(c), p3(p);
      b3 = b3 - a3, c3 = c3 - a3, p3 = p3 - a3;
      Point3D f = cross(b3, c3);
      return cmp(p3.dot(f));  // check same direction, in: < 0, on: = 0, out: > 0
    }
    
    int intersection(const Point &a, const Point &b, const Point &c,
                     const Point &d) {  // seg(a, b) and seg(c, d)
      return cmp(cross(a, c, b)) * cmp(cross(a, b, d)) > 0 &&
             cmp(cross(c, a, d)) * cmp(cross(c, d, b)) > 0;
    }
    
    class Delaunay {
     public:
      std::list<Edge> head[MAXV];  // graph
      Point p[MAXV];
      int n, rename[MAXV];
    
      void init(int n, Point p[]) {
        memcpy(this->p, p, sizeof(Point) * n);
        std::sort(this->p, this->p + n);
        for (int i = 0; i < n; i++) rename[p[i].id] = i;
        this->n = n;
        divide(0, n - 1);
      }
    
      void addEdge(int u, int v) {
        head[u].push_front(Edge(v));
        head[v].push_front(Edge(u));
        head[u].begin()->c = head[v].begin();
        head[v].begin()->c = head[u].begin();
      }
    
      void divide(int l, int r) {
        if (r - l <= 2) {  // #point <= 3
          for (int i = l; i <= r; i++)
            for (int j = i + 1; j <= r; j++) addEdge(i, j);
          return;
        }
        int mid = (l + r) / 2;
        divide(l, mid);
        divide(mid + 1, r);
    
        std::list<Edge>::iterator it;
        int nowl = l, nowr = r;
    
        for (int update = 1; update;) {
          // find left and right convex, lower common tangent
          update = 0;
          Point ptL = p[nowl], ptR = p[nowr];
          for (it = head[nowl].begin(); it != head[nowl].end(); it++) {
            Point t = p[it->id];
            double v = cross(ptR, ptL, t);
            if (cmp(v) > 0 || (cmp(v) == 0 && ptR.dist2(t) < ptR.dist2(ptL))) {
              nowl = it->id, update = 1;
              break;
            }
          }
          if (update) continue;
          for (it = head[nowr].begin(); it != head[nowr].end(); it++) {
            Point t = p[it->id];
            double v = cross(ptL, ptR, t);
            if (cmp(v) < 0 || (cmp(v) == 0 && ptL.dist2(t) < ptL.dist2(ptR))) {
              nowr = it->id, update = 1;
              break;
            }
          }
        }
    
        addEdge(nowl, nowr);  // add tangent
    
        for (int update = 1; true;) {
          update = 0;
          Point ptL = p[nowl], ptR = p[nowr];
          int ch = -1, side = 0;
          for (it = head[nowl].begin(); it != head[nowl].end(); it++) {
            if (cmp(cross(ptL, ptR, p[it->id])) > 0 &&
                (ch == -1 || inCircle(ptL, ptR, p[ch], p[it->id]) < 0)) {
              ch = it->id, side = -1;
            }
          }
          for (it = head[nowr].begin(); it != head[nowr].end(); it++) {
            if (cmp(cross(ptR, p[it->id], ptL)) > 0 &&
                (ch == -1 || inCircle(ptL, ptR, p[ch], p[it->id]) < 0)) {
              ch = it->id, side = 1;
            }
          }
          if (ch == -1) break;  // upper common tangent
          if (side == -1) {
            for (it = head[nowl].begin(); it != head[nowl].end();) {
              if (intersection(ptL, p[it->id], ptR, p[ch])) {
                head[it->id].erase(it->c);
                head[nowl].erase(it++);
              } else {
                it++;
              }
            }
            nowl = ch;
            addEdge(nowl, nowr);
          } else {
            for (it = head[nowr].begin(); it != head[nowr].end();) {
              if (intersection(ptR, p[it->id], ptL, p[ch])) {
                head[it->id].erase(it->c);
                head[nowr].erase(it++);
              } else {
                it++;
              }
            }
            nowr = ch;
            addEdge(nowl, nowr);
          }
        }
      }
    
      std::vector<std::pair<int, int>> getEdge() {
        std::vector<std::pair<int, int>> ret;
        ret.reserve(n);
        std::list<Edge>::iterator it;
        for (int i = 0; i < n; i++) {
          for (it = head[i].begin(); it != head[i].end(); it++) {
            if (it->id < i) continue;
            ret.push_back(std::make_pair(p[i].id, p[it->id].id));
          }
        }
        return ret;
      }
    };
    ```

## Voronoi 图

Voronoi 图由一组由连接两邻点直线的垂直平分线组成的连续多边形组成，根据 $n$ 个在平面上不重合种子点，把平面分成 $n$ 个区域，使得每个区域内的点到它所在区域的种子点的距离比到其它区域种子点的距离近．

Voronoi 图是 Delaunay 三角剖分的对偶图，可以使用构造 Delaunay 三角剖分的分治算法求出三角网，再使用最左转线算法求出其对偶图实现在 $O(n \log n)$ 的时间复杂度下构造 Voronoi 图．

## 题目

[SGU 383 Caravans](https://codeforces.com/problemsets/acmsguru/problem/99999/383) 三角剖分 + 倍增

[ContestHunter. 无尽的毁灭](http://noi-test.zzstep.com/contest/Beta%20Round%20%EF%BC%832%20%28%E6%96%B0%E7%96%86%E7%9C%81%E9%98%9F%E4%BA%92%E6%B5%8BWeek1-Day2%29/%E6%97%A0%E5%B0%BD%E7%9A%84%E6%AF%81%E7%81%AD) 三角剖分求对偶图建 Voronoi 图

[Codeforces Gym 103485M. Constellation collection](https://codeforces.com/gym/103485/problem/M) 三角剖分之后建图进行 Floodfill

## 参考资料与拓展阅读

1.  [Wikipedia - Triangulation (geometry)](https://en.wikipedia.org/wiki/Triangulation_%28geometry%29)
2.  [Wikipedia - Delaunay triangulation](https://en.wikipedia.org/wiki/Delaunay_triangulation)
3.  Samuel Peterson -[Computing Constrained Delaunay Triangulations in 2-D (1997-98)](http://www.geom.uiuc.edu/~samuelp/del_project.html)
