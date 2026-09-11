

## chapter_heap / build_heap

# 建堆操作

在某些情况下，我们希望使用一个列表的所有元素来构建一个堆，这个过程被称为“建堆操作”。

## 借助入堆操作实现

我们首先创建一个空堆，然后遍历列表，依次对每个元素执行“入堆操作”，即先将元素添加至堆的尾部，再对该元素执行“从底至顶”堆化。

每当一个元素入堆，堆的长度就加一。由于节点是从顶到底依次被添加进二叉树的，因此堆是“自上而下”构建的。

设元素数量为 $n$ ，每个元素的入堆操作使用 $O(\log{n})$ 时间，因此该建堆方法的时间复杂度为 $O(n \log n)$ 。

## 通过遍历堆化实现

实际上，我们可以实现一种更为高效的建堆方法，共分为两步。

1. 将列表所有元素原封不动地添加到堆中，此时堆的性质尚未得到满足。
2. 倒序遍历堆（层序遍历的倒序），依次对每个非叶节点执行“从顶至底堆化”。

**每当堆化一个节点后，以该节点为根节点的子树就形成一个合法的子堆**。而由于是倒序遍历，因此堆是“自下而上”构建的。

之所以选择倒序遍历，是因为这样能够保证当前节点之下的子树已经是合法的子堆，这样堆化当前节点才是有效的。

值得说明的是，**由于叶节点没有子节点，因此它们天然就是合法的子堆，无须堆化**。如以下代码所示，最后一个非叶节点是最后一个节点的父节点，我们从它开始倒序遍历并执行堆化：

```src
[file]{my_heap}-[class]{max_heap}-[func]{__init__}
```

## 复杂度分析

下面，我们来尝试推算第二种建堆方法的时间复杂度。

- 假设完全二叉树的节点数量为 $n$ ，则叶节点数量为 $(n + 1) / 2$ ，其中 $/$ 为向下整除。因此需要堆化的节点数量为 $n / 2$ 。
- 在从顶至底堆化的过程中，每个节点最多堆化到叶节点，因此最大迭代次数为二叉树高度 $\log n$ 。

将上述两者相乘，可得到建堆过程的时间复杂度为 $O(n \log n)$ 。**但这个估算结果并不准确，因为我们没有考虑到二叉树底层节点数量远多于顶层节点的性质**。

接下来我们来进行更为准确的计算。为了降低计算难度，假设给定一个节点数量为 $n$ 、高度为 $h$ 的“完美二叉树”，该假设不会影响计算结果的正确性。

![完美二叉树的各层节点数量](build_heap.assets/heapify_operations_count.png)

如上图所示，节点“从顶至底堆化”的最大迭代次数等于该节点到叶节点的距离，而该距离正是“节点高度”。因此，我们可以对各层的“节点数量 $\times$ 节点高度”求和，**得到所有节点的堆化迭代次数的总和**。

$$
T(h) = 2^0h + 2^1(h-1) + 2^2(h-2) + \dots + 2^{(h-1)}\times1
$$

化简上式需要借助中学的数列知识，先将 $T(h)$ 乘以 $2$ ，得到：

$$
\begin{aligned}
T(h) & = 2^0h + 2^1(h-1) + 2^2(h-2) + \dots + 2^{h-1}\times1 \newline
2 T(h) & = 2^1h + 2^2(h-1) + 2^3(h-2) + \dots + 2^{h}\times1 \newline
\end{aligned}
$$

使用错位相减法，用下式 $2 T(h)$ 减去上式 $T(h)$ ，可得：

$$
2T(h) - T(h) = T(h) = -2^0h + 2^1 + 2^2 + \dots + 2^{h-1} + 2^h
$$

观察上式，发现 $T(h)$ 是一个等比数列，可直接使用求和公式，得到时间复杂度为：

$$
\begin{aligned}
T(h) & = 2 \frac{1 - 2^h}{1 - 2} - h \newline
& = 2^{h+1} - h - 2 \newline
& = O(2^h)
\end{aligned}
$$

进一步，高度为 $h$ 的完美二叉树的节点数量为 $n = 2^{h+1} - 1$ ，易得复杂度为 $O(2^h) = O(n)$ 。以上推算表明，**输入列表并建堆的时间复杂度为 $O(n)$ ，非常高效**。


## chapter_heap / exercises

# 练习

## 知识巩固

### 数字 10 入堆后怎样调整

数组 `[9, 7, 8, 3, 5]` 表示一个大顶堆。现在将数字 10 入堆。

<!-- numbered-subquestions -->

1. 先把 10 添加到数组末尾，它的父节点值是多少？
2. 从新节点开始向上堆化，写出每次交换后的数组。
3. 最终的堆顶元素是什么？一共交换了几次？

??? success "参考答案"

    1. 10 添加后的索引为 5，其父节点索引为
        $\lfloor(5-1)/2\rfloor=2$，父节点值为 8。

    2. 10 大于 8，第一次交换后为 `[9, 7, 10, 3, 5, 8]`；
        10 又大于父节点 9，第二次交换后为 `[10, 7, 9, 3, 5, 8]`。
        此时 10 已到达根节点，堆化结束。

    3. 最终堆顶为 10，共交换 2 次。

### 检查小顶堆的父子关系

数组 `[1, 4, 3, 7, 6, 2]` 表示一棵完全二叉树。小顶堆要求每个父节点都不大于它的孩子。
对索引 $i$，左、右孩子索引分别为 $2i+1$ 和 $2i+2$。

<!-- numbered-subquestions -->

1. 索引 2 的孩子索引和值分别是什么？
2. 索引 2 处的节点值为 3，它与孩子节点之间是否违反小顶堆规则？如果违反，应交换哪两个元素？
3. 根据第 2 问的判断：若违反规则，写出交换后的数组；若不违反，说明无须交换。最后检查其余父子关系。

??? success "参考答案"

    1. 索引 2 的左孩子索引是 5、值为 2；右孩子索引是 6，但数组长度为 6，因此右孩子不存在。

    2. 父节点值 3 大于孩子值 2，违反小顶堆规则，应交换索引 2 和索引 5 的元素。

    3. 交换后得到 `[1, 4, 2, 7, 6, 3]`。逐一检查：
        `1 ≤ 4`、`1 ≤ 2`；`4 ≤ 7`、`4 ≤ 6`；`2 ≤ 3`。
        所有父节点都不大于自己的孩子，因此现在满足小顶堆规则。

### 用小顶堆保留最大的三个数

要从数据流 `[4, 1, 7, 3, 8]` 中保留最大的 3 个数，可以维护一个大小不超过 3 的小顶堆。

先把前 3 个数依次放入小顶堆。堆满后，每读入一个新数：
如果它大于堆顶，就删除堆顶并放入新数；否则堆保持不变。

请写出每次读入数字后堆中保留的数字和堆顶。
只需把保留的数字写成集合，不要求写出它们在堆数组中的排列。

??? success "参考答案"

    每次读入数字后的结果如下：

    | 读入数字 | 保留的数字 | 堆顶 |
    | --- | --- | --- |
    | 4 | `{4}` | 4 |
    | 1 | `{1, 4}` | 1 |
    | 7 | `{1, 4, 7}` | 1 |
    | 3 | `{3, 4, 7}` | 3 |
    | 8 | `{4, 7, 8}` | 4 |

    堆满后，堆顶是当前保留数字中最小的一个。只有新数字大于堆顶时，
    才用新数字替换堆顶。最终保留的 `{4, 7, 8}` 正是最大的 3 个数。

## 编程练习

### 寻找数组中的第 k 大元素

给定整数数组 `nums` 和整数 $k$，其中 $1 \le k \le n$，$n$ 是数组长度。把数组按从大到小排列后，请返回第 $k$ 个位置上的元素。

重复元素需要分别计数。例如，`[5, 5, 2]` 的第 2 大元素仍是 5。请使用一个大小不超过 $k$ 的小顶堆完成。

??? tip "解题提示"

    1. 第 k 大元素是最大的 k 个数中最小的那个
    2. 每个数先入小顶堆，大小超过 k 时弹出最小值
    3. 遍历结束时堆中保留最大的 k 个数，堆顶就是答案

[LeetCode](https://leetcode.cn/problems/kth-largest-element-in-an-array/){ .rounded-button .exercise-button target="_blank" rel="noopener noreferrer" } [题目解析](https://leetcode.cn/problems/kth-largest-element-in-an-array/solutions/2361969/215-shu-zu-zhong-de-di-k-ge-zui-da-yuan-d786p/){ .rounded-button .exercise-button target="_blank" rel="noopener noreferrer" }

> **说明：** 链接中的题解讲解了快速排序和快速选择，没有使用堆；本练习请按照正文 8.3 节使用大小不超过 k 的小顶堆完成


## chapter_heap / heap

# 堆

<u>堆（heap）</u>是一种满足特定条件的完全二叉树，主要可分为两种类型，如下图所示。

- <u>小顶堆（min heap）</u>：任意节点的值 $\leq$ 其子节点的值。
- <u>大顶堆（max heap）</u>：任意节点的值 $\geq$ 其子节点的值。

![小顶堆与大顶堆](heap.assets/min_heap_and_max_heap.png)

堆作为完全二叉树的一个特例，具有以下特性。

- 最底层节点靠左填充，其他层的节点都被填满。
- 我们将二叉树的根节点称为“堆顶”，将底层最靠右的节点称为“堆底”。
- 对于大顶堆（小顶堆），堆顶元素（根节点）的值是最大（最小）的。

## 堆的常用操作

需要指出的是，许多编程语言提供的是<u>优先队列（priority queue）</u>，这是一种抽象的数据结构，定义为具有优先级排序的队列。

实际上，**堆通常用于实现优先队列，大顶堆相当于元素按从大到小的顺序出队的优先队列**。从使用角度来看，我们可以将“优先队列”和“堆”看作等价的数据结构。因此，本书对两者不做特别区分，统一称作“堆”。

堆的常用操作见下表，方法名需要根据编程语言来确定。

<p align="center"> 表 <id> &nbsp; 堆的操作效率 </p>

| 方法名      | 描述                                             | 时间复杂度  |
| ----------- | ------------------------------------------------ | ----------- |
| `push()`    | 元素入堆                                         | $O(\log n)$ |
| `pop()`     | 堆顶元素出堆                                     | $O(\log n)$ |
| `peek()`    | 访问堆顶元素（对于大 / 小顶堆分别为最大 / 小值） | $O(1)$      |
| `size()`    | 获取堆的元素数量                                 | $O(1)$      |
| `isEmpty()` | 判断堆是否为空                                   | $O(1)$      |

在实际应用中，我们可以直接使用编程语言提供的堆类（或优先队列类）。

类似于排序算法中的“从小到大排列”和“从大到小排列”，我们可以通过设置一个 `flag` 或修改 `Comparator` 实现“小顶堆”与“大顶堆”之间的转换。代码如下所示：

=== "Python"

    ```python title="heap.py"
    # 初始化小顶堆
    min_heap, flag = [], 1
    # 初始化大顶堆
    max_heap, flag = [], -1

    # Python 的 heapq 模块默认实现小顶堆
    # 考虑将“元素取负”后再入堆，这样就可以将大小关系颠倒，从而实现大顶堆
    # 在本示例中，flag = 1 时对应小顶堆，flag = -1 时对应大顶堆

    # 元素入堆
    heapq.heappush(max_heap, flag * 1)
    heapq.heappush(max_heap, flag * 3)
    heapq.heappush(max_heap, flag * 2)
    heapq.heappush(max_heap, flag * 5)
    heapq.heappush(max_heap, flag * 4)

    # 获取堆顶元素
    peek: int = flag * max_heap[0] # 5

    # 堆顶元素出堆
    # 出堆元素会形成一个从大到小的序列
    val = flag * heapq.heappop(max_heap) # 5
    val = flag * heapq.heappop(max_heap) # 4
    val = flag * heapq.heappop(max_heap) # 3
    val = flag * heapq.heappop(max_heap) # 2
    val = flag * heapq.heappop(max_heap) # 1

    # 获取堆大小
    size: int = len(max_heap)

    # 判断堆是否为空
    is_empty: bool = not max_heap

    # 输入列表并建堆
    min_heap: list[int] = [1, 3, 2, 5, 4]
    heapq.heapify(min_heap)
    ```

=== "C++"

    ```cpp title="heap.cpp"
    /* 初始化堆 */
    // 初始化小顶堆
    priority_queue<int, vector<int>, greater<int>> minHeap;
    // 初始化大顶堆
    priority_queue<int, vector<int>, less<int>> maxHeap;

    /* 元素入堆 */
    maxHeap.push(1);
    maxHeap.push(3);
    maxHeap.push(2);
    maxHeap.push(5);
    maxHeap.push(4);

    /* 获取堆顶元素 */
    int peek = maxHeap.top(); // 5

    /* 堆顶元素出堆 */
    // 出堆元素会形成一个从大到小的序列
    maxHeap.pop(); // 5
    maxHeap.pop(); // 4
    maxHeap.pop(); // 3
    maxHeap.pop(); // 2
    maxHeap.pop(); // 1

    /* 获取堆大小 */
    int size = maxHeap.size();

    /* 判断堆是否为空 */
    bool isEmpty = maxHeap.empty();

    /* 输入列表并建堆 */
    vector<int> input{1, 3, 2, 5, 4};
    priority_queue<int, vector<int>, greater<int>> minHeap(input.begin(), input.end());
    ```

=== "Java"

    ```java title="heap.java"
    /* 初始化堆 */
    // 初始化小顶堆
    Queue<Integer> minHeap = new PriorityQueue<>();
    // 初始化大顶堆（使用 lambda 表达式修改 Comparator 即可）
    Queue<Integer> maxHeap = new PriorityQueue<>((a, b) -> b - a);

    /* 元素入堆 */
    maxHeap.offer(1);
    maxHeap.offer(3);
    maxHeap.offer(2);
    maxHeap.offer(5);
    maxHeap.offer(4);

    /* 获取堆顶元素 */
    int peek = maxHeap.peek(); // 5

    /* 堆顶元素出堆 */
    // 出堆元素会形成一个从大到小的序列
    peek = maxHeap.poll(); // 5
    peek = maxHeap.poll(); // 4
    peek = maxHeap.poll(); // 3
    peek = maxHeap.poll(); // 2
    peek = maxHeap.poll(); // 1

    /* 获取堆大小 */
    int size = maxHeap.size();

    /* 判断堆是否为空 */
    boolean isEmpty = maxHeap.isEmpty();

    /* 输入列表并建堆 */
    minHeap = new PriorityQueue<>(Arrays.asList(1, 3, 2, 5, 4));
    ```

=== "C#"

    ```csharp title="heap.cs"
    /* 初始化堆 */
    // 初始化小顶堆
    PriorityQueue<int, int> minHeap = new();
    // 初始化大顶堆（使用 lambda 表达式修改 Comparer 即可）
    PriorityQueue<int, int> maxHeap = new(Comparer<int>.Create((x, y) => y.CompareTo(x)));

    /* 元素入堆 */
    maxHeap.Enqueue(1, 1);
    maxHeap.Enqueue(3, 3);
    maxHeap.Enqueue(2, 2);
    maxHeap.Enqueue(5, 5);
    maxHeap.Enqueue(4, 4);

    /* 获取堆顶元素 */
    int peek = maxHeap.Peek();//5

    /* 堆顶元素出堆 */
    // 出堆元素会形成一个从大到小的序列
    peek = maxHeap.Dequeue();  // 5
    peek = maxHeap.Dequeue();  // 4
    peek = maxHeap.Dequeue();  // 3
    peek = maxHeap.Dequeue();  // 2
    peek = maxHeap.Dequeue();  // 1

    /* 获取堆大小 */
    int size = maxHeap.Count;

    /* 判断堆是否为空 */
    bool isEmpty = maxHeap.Count == 0;

    /* 输入列表并建堆 */
    minHeap = new PriorityQueue<int, int>([(1, 1), (3, 3), (2, 2), (5, 5), (4, 4)]);
    ```

=== "Go"

    ```go title="heap.go"
    // Go 语言中可以通过实现 heap.Interface 来构建整数大顶堆
    // 实现 heap.Interface 需要同时实现 sort.Interface
    type intHeap []any

    // Push heap.Interface 的方法，实现推入元素到堆
    func (h *intHeap) Push(x any) {
        // Push 和 Pop 使用 pointer receiver 作为参数
        // 因为它们不仅会对切片的内容进行调整，还会修改切片的长度。
        *h = append(*h, x.(int))
    }

    // Pop heap.Interface 的方法，实现弹出堆顶元素
    func (h *intHeap) Pop() any {
        // 待出堆元素存放在最后
        last := (*h)[len(*h)-1]
        *h = (*h)[:len(*h)-1]
        return last
    }

    // Len sort.Interface 的方法
    func (h *intHeap) Len() int {
        return len(*h)
    }

    // Less sort.Interface 的方法
    func (h *intHeap) Less(i, j int) bool {
        // 如果实现小顶堆，则需要调整为小于号
        return (*h)[i].(int) > (*h)[j].(int)
    }

    // Swap sort.Interface 的方法
    func (h *intHeap) Swap(i, j int) {
        (*h)[i], (*h)[j] = (*h)[j], (*h)[i]
    }

    // Top 获取堆顶元素
    func (h *intHeap) Top() any {
        return (*h)[0]
    }

    /* Driver Code */
    func TestHeap(t *testing.T) {
        /* 初始化堆 */
        // 初始化大顶堆
        maxHeap := &intHeap{}
        heap.Init(maxHeap)
        /* 元素入堆 */
        // 调用 heap.Interface 的方法，来添加元素
        heap.Push(maxHeap, 1)
        heap.Push(maxHeap, 3)
        heap.Push(maxHeap, 2)
        heap.Push(maxHeap, 4)
        heap.Push(maxHeap, 5)

        /* 获取堆顶元素 */
        top := maxHeap.Top()
        fmt.Printf("堆顶元素为 %d\n", top)

        /* 堆顶元素出堆 */
        // 调用 heap.Interface 的方法，来移除元素
        heap.Pop(maxHeap) // 5
        heap.Pop(maxHeap) // 4
        heap.Pop(maxHeap) // 3
        heap.Pop(maxHeap) // 2
        heap.Pop(maxHeap) // 1

        /* 获取堆大小 */
        size := len(*maxHeap)
        fmt.Printf("堆元素数量为 %d\n", size)

        /* 判断堆是否为空 */
        isEmpty := len(*maxHeap) == 0
        fmt.Printf("堆是否为空 %t\n", isEmpty)
    }
    ```

=== "Swift"

    ```swift title="heap.swift"
    /* 初始化堆 */
    // Swift 的 Heap 类型同时支持最大堆和最小堆，且需要引入 swift-collections
    var heap = Heap<Int>()

    /* 元素入堆 */
    heap.insert(1)
    heap.insert(3)
    heap.insert(2)
    heap.insert(5)
    heap.insert(4)

    /* 获取堆顶元素 */
    var peek = heap.max()!

    /* 堆顶元素出堆 */
    peek = heap.removeMax() // 5
    peek = heap.removeMax() // 4
    peek = heap.removeMax() // 3
    peek = heap.removeMax() // 2
    peek = heap.removeMax() // 1

    /* 获取堆大小 */
    let size = heap.count

    /* 判断堆是否为空 */
    let isEmpty = heap.isEmpty

    /* 输入列表并建堆 */
    let heap2 = Heap([1, 3, 2, 5, 4])
    ```

=== "JS"

    ```javascript title="heap.js"
    // JavaScript 未提供内置 Heap 类
    ```

=== "TS"

    ```typescript title="heap.ts"
    // TypeScript 未提供内置 Heap 类
    ```

=== "Dart"

    ```dart title="heap.dart"
    // Dart 未提供内置 Heap 类
    ```

=== "Rust"

    ```rust title="heap.rs"
    use std::collections::BinaryHeap;
    use std::cmp::Reverse;

    /* 初始化堆 */
    // 初始化小顶堆
    let mut min_heap = BinaryHeap::<Reverse<i32>>::new();
    // 初始化大顶堆
    let mut max_heap = BinaryHeap::new();

    /* 元素入堆 */
    max_heap.push(1);
    max_heap.push(3);
    max_heap.push(2);
    max_heap.push(5);
    max_heap.push(4);

    /* 获取堆顶元素 */
    let peek = max_heap.peek().unwrap();  // 5

    /* 堆顶元素出堆 */
    // 出堆元素会形成一个从大到小的序列
    let peek = max_heap.pop().unwrap();   // 5
    let peek = max_heap.pop().unwrap();   // 4
    let peek = max_heap.pop().unwrap();   // 3
    let peek = max_heap.pop().unwrap();   // 2
    let peek = max_heap.pop().unwrap();   // 1

    /* 获取堆大小 */
    let size = max_heap.len();

    /* 判断堆是否为空 */
    let is_empty = max_heap.is_empty();

    /* 输入列表并建堆 */
    let min_heap = BinaryHeap::from(vec![Reverse(1), Reverse(3), Reverse(2), Reverse(5), Reverse(4)]);
    ```

=== "C"

    ```c title="heap.c"
    // C 未提供内置 Heap 类
    ```

=== "Kotlin"

    ```kotlin title="heap.kt"
    /* 初始化堆 */
    // 初始化小顶堆
    var minHeap = PriorityQueue<Int>()
    // 初始化大顶堆（使用 lambda 表达式修改 Comparator 即可）
    val maxHeap = PriorityQueue { a: Int, b: Int -> b - a }

    /* 元素入堆 */
    maxHeap.offer(1)
    maxHeap.offer(3)
    maxHeap.offer(2)
    maxHeap.offer(5)
    maxHeap.offer(4)

    /* 获取堆顶元素 */
    var peek = maxHeap.peek() // 5

    /* 堆顶元素出堆 */
    // 出堆元素会形成一个从大到小的序列
    peek = maxHeap.poll() // 5
    peek = maxHeap.poll() // 4
    peek = maxHeap.poll() // 3
    peek = maxHeap.poll() // 2
    peek = maxHeap.poll() // 1

    /* 获取堆大小 */
    val size = maxHeap.size

    /* 判断堆是否为空 */
    val isEmpty = maxHeap.isEmpty()

    /* 输入列表并建堆 */
    minHeap = PriorityQueue(mutableListOf(1, 3, 2, 5, 4))
    ```

=== "Ruby"

    ```ruby title="heap.rb"
    # Ruby 未提供内置 Heap 类
    ```

??? pythontutor "可视化运行"

    https://pythontutor.com/render.html#code=import%20heapq%0A%0A%22%22%22Driver%20Code%22%22%22%0Aif%20__name__%20%3D%3D%20%22__main__%22%3A%0A%20%20%20%20%23%20%E5%88%9D%E5%A7%8B%E5%8C%96%E5%B0%8F%E9%A1%B6%E5%A0%86%0A%20%20%20%20min_heap,%20flag%20%3D%20%5B%5D,%201%0A%20%20%20%20%23%20%E5%88%9D%E5%A7%8B%E5%8C%96%E5%A4%A7%E9%A1%B6%E5%A0%86%0A%20%20%20%20max_heap,%20flag%20%3D%20%5B%5D,%20-1%0A%20%20%20%20%0A%20%20%20%20%23%20Python%20%E7%9A%84%20heapq%20%E6%A8%A1%E5%9D%97%E9%BB%98%E8%AE%A4%E5%AE%9E%E7%8E%B0%E5%B0%8F%E9%A1%B6%E5%A0%86%0A%20%20%20%20%23%20%E8%80%83%E8%99%91%E5%B0%86%E2%80%9C%E5%85%83%E7%B4%A0%E5%8F%96%E8%B4%9F%E2%80%9D%E5%90%8E%E5%86%8D%E5%85%A5%E5%A0%86%EF%BC%8C%E8%BF%99%E6%A0%B7%E5%B0%B1%E5%8F%AF%E4%BB%A5%E5%B0%86%E5%A4%A7%E5%B0%8F%E5%85%B3%E7%B3%BB%E9%A2%A0%E5%80%92%EF%BC%8C%E4%BB%8E%E8%80%8C%E5%AE%9E%E7%8E%B0%E5%A4%A7%E9%A1%B6%E5%A0%86%0A%20%20%20%20%23%20%E5%9C%A8%E6%9C%AC%E7%A4%BA%E4%BE%8B%E4%B8%AD%EF%BC%8Cflag%20%3D%201%20%E6%97%B6%E5%AF%B9%E5%BA%94%E5%B0%8F%E9%A1%B6%E5%A0%86%EF%BC%8Cflag%20%3D%20-1%20%E6%97%B6%E5%AF%B9%E5%BA%94%E5%A4%A7%E9%A1%B6%E5%A0%86%0A%20%20%20%20%0A%20%20%20%20%23%20%E5%85%83%E7%B4%A0%E5%85%A5%E5%A0%86%0A%20%20%20%20heapq.heappush%28max_heap,%20flag%20*%201%29%0A%20%20%20%20heapq.heappush%28max_heap,%20flag%20*%203%29%0A%20%20%20%20heapq.heappush%28max_heap,%20flag%20*%202%29%0A%20%20%20%20heapq.heappush%28max_heap,%20flag%20*%205%29%0A%20%20%20%20heapq.heappush%28max_heap,%20flag%20*%204%29%0A%20%20%20%20%0A%20%20%20%20%23%20%E8%8E%B7%E5%8F%96%E5%A0%86%E9%A1%B6%E5%85%83%E7%B4%A0%0A%20%20%20%20peek%20%3D%20flag%20*%20max_heap%5B0%5D%20%23%205%0A%20%20%20%20%0A%20%20%20%20%23%20%E5%A0%86%E9%A1%B6%E5%85%83%E7%B4%A0%E5%87%BA%E5%A0%86%0A%20%20%20%20%23%20%E5%87%BA%E5%A0%86%E5%85%83%E7%B4%A0%E4%BC%9A%E5%BD%A2%E6%88%90%E4%B8%80%E4%B8%AA%E4%BB%8E%E5%A4%A7%E5%88%B0%E5%B0%8F%E7%9A%84%E5%BA%8F%E5%88%97%0A%20%20%20%20val%20%3D%20flag%20*%20heapq.heappop%28max_heap%29%20%23%205%0A%20%20%20%20val%20%3D%20flag%20*%20heapq.heappop%28max_heap%29%20%23%204%0A%20%20%20%20val%20%3D%20flag%20*%20heapq.heappop%28max_heap%29%20%23%203%0A%20%20%20%20val%20%3D%20flag%20*%20heapq.heappop%28max_heap%29%20%23%202%0A%20%20%20%20val%20%3D%20flag%20*%20heapq.heappop%28max_heap%29%20%23%201%0A%20%20%20%20%0A%20%20%20%20%23%20%E8%8E%B7%E5%8F%96%E5%A0%86%E5%A4%A7%E5%B0%8F%0A%20%20%20%20size%20%3D%20len%28max_heap%29%0A%20%20%20%20%0A%20%20%20%20%23%20%E5%88%A4%E6%96%AD%E5%A0%86%E6%98%AF%E5%90%A6%E4%B8%BA%E7%A9%BA%0A%20%20%20%20is_empty%20%3D%20not%20max_heap%0A%20%20%20%20%0A%20%20%20%20%23%20%E8%BE%93%E5%85%A5%E5%88%97%E8%A1%A8%E5%B9%B6%E5%BB%BA%E5%A0%86%0A%20%20%20%20min_heap%20%3D%20%5B1,%203,%202,%205,%204%5D%0A%20%20%20%20heapq.heapify%28min_heap%29&cumulative=false&curInstr=3&heapPrimitives=nevernest&mode=display&origin=opt-frontend.js&py=311&rawInputLstJSON=%5B%5D&textReferences=false

## 堆的实现

下文实现的是大顶堆。若要将其转换为小顶堆，只需将所有大小逻辑判断进行逆转（例如，将 $\geq$ 替换为 $\leq$ ）。感兴趣的读者可以自行实现。

### 堆的存储与表示

“二叉树”章节讲过，完全二叉树非常适合用数组来表示。由于堆正是一种完全二叉树，**因此我们将采用数组来存储堆**。

当使用数组表示二叉树时，元素代表节点值，索引代表节点在二叉树中的位置。**节点指针通过索引映射公式来实现**。

如下图所示，给定索引 $i$ ，其左子节点的索引为 $2i + 1$ ，右子节点的索引为 $2i + 2$ ，父节点的索引为 $(i - 1) / 2$（向下整除）。当索引越界时，表示空节点或节点不存在。

![堆的表示与存储](heap.assets/representation_of_heap.png)

我们可以将索引映射公式封装成函数，方便后续使用：

```src
[file]{my_heap}-[class]{max_heap}-[func]{parent}
```

### 访问堆顶元素

堆顶元素即为二叉树的根节点，也就是列表的首个元素：

```src
[file]{my_heap}-[class]{max_heap}-[func]{peek}
```

### 元素入堆

给定元素 `val` ，我们首先将其添加到堆底。添加之后，由于 `val` 可能大于堆中其他元素，堆的成立条件可能已被破坏，**因此需要修复从插入节点到根节点的路径上的各个节点**，这个操作被称为<u>堆化（heapify）</u>。

考虑从入堆节点开始，**从底至顶执行堆化**。如下图所示，我们比较插入节点与其父节点的值，如果插入节点更大，则将它们交换。然后继续执行此操作，从底至顶修复堆中的各个节点，直至越过根节点或遇到无须交换的节点时结束。

=== "<1>"
    ![元素入堆步骤](heap.assets/heap_push_step1.png)

=== "<2>"
    ![heap_push_step2](heap.assets/heap_push_step2.png)

=== "<3>"
    ![heap_push_step3](heap.assets/heap_push_step3.png)

=== "<4>"
    ![heap_push_step4](heap.assets/heap_push_step4.png)

=== "<5>"
    ![heap_push_step5](heap.assets/heap_push_step5.png)

=== "<6>"
    ![heap_push_step6](heap.assets/heap_push_step6.png)

=== "<7>"
    ![heap_push_step7](heap.assets/heap_push_step7.png)

=== "<8>"
    ![heap_push_step8](heap.assets/heap_push_step8.png)

=== "<9>"
    ![heap_push_step9](heap.assets/heap_push_step9.png)

设节点总数为 $n$ ，则树的高度为 $O(\log n)$ 。由此可知，堆化操作的循环轮数最多为 $O(\log n)$ ，**元素入堆操作的时间复杂度为 $O(\log n)$** 。代码如下所示：

```src
[file]{my_heap}-[class]{max_heap}-[func]{sift_up}
```

### 堆顶元素出堆

堆顶元素是二叉树的根节点，即列表首元素。如果我们直接从列表中删除首元素，那么二叉树中所有节点的索引都会发生变化，这将使得后续使用堆化进行修复变得困难。为了尽量减少元素索引的变动，我们采用以下操作步骤。

1. 交换堆顶元素与堆底元素（交换根节点与最右叶节点）。
2. 交换完成后，将堆底从列表中删除（注意，由于已经交换，因此实际上删除的是原来的堆顶元素）。
3. 从根节点开始，**从顶至底执行堆化**。

如下图所示，**“从顶至底堆化”的操作方向与“从底至顶堆化”相反**，我们将根节点的值与其两个子节点的值进行比较，将最大的子节点与根节点交换。然后循环执行此操作，直到越过叶节点或遇到无须交换的节点时结束。

=== "<1>"
    ![堆顶元素出堆步骤](heap.assets/heap_pop_step1.png)

=== "<2>"
    ![heap_pop_step2](heap.assets/heap_pop_step2.png)

=== "<3>"
    ![heap_pop_step3](heap.assets/heap_pop_step3.png)

=== "<4>"
    ![heap_pop_step4](heap.assets/heap_pop_step4.png)

=== "<5>"
    ![heap_pop_step5](heap.assets/heap_pop_step5.png)

=== "<6>"
    ![heap_pop_step6](heap.assets/heap_pop_step6.png)

=== "<7>"
    ![heap_pop_step7](heap.assets/heap_pop_step7.png)

=== "<8>"
    ![heap_pop_step8](heap.assets/heap_pop_step8.png)

=== "<9>"
    ![heap_pop_step9](heap.assets/heap_pop_step9.png)

=== "<10>"
    ![heap_pop_step10](heap.assets/heap_pop_step10.png)

与元素入堆操作相似，堆顶元素出堆操作的时间复杂度也为 $O(\log n)$ 。代码如下所示：

```src
[file]{my_heap}-[class]{max_heap}-[func]{sift_down}
```

## 堆的常见应用

- **优先队列**：堆通常作为实现优先队列的首选数据结构，其入队和出队操作的时间复杂度均为 $O(\log n)$ ，而建堆操作为 $O(n)$ ，这些操作都非常高效。
- **堆排序**：给定一组数据，我们可以用它们建立一个堆，然后不断地执行元素出堆操作，从而得到有序数据。然而，我们通常会使用一种更优雅的方式实现堆排序，详见“堆排序”章节。
- **获取最大的 $k$ 个元素**：这是一个经典的算法问题，同时也是一种典型应用，例如选择热度前 10 的新闻作为微博热搜，选取销量前 10 的商品等。


## chapter_heap / summary

# 小结

### 重点回顾

- 堆是一棵完全二叉树，根据成立条件可分为大顶堆和小顶堆。大（小）顶堆的堆顶元素是最大（小）的。
- 优先队列的定义是具有出队优先级的队列，通常使用堆来实现。
- 堆的常用操作及其对应的时间复杂度包括：元素入堆 $O(\log n)$、堆顶元素出堆 $O(\log n)$ 和访问堆顶元素 $O(1)$ 等。
- 完全二叉树非常适合用数组表示，因此我们通常使用数组来存储堆。
- 堆化操作用于维护堆的性质，在入堆和出堆操作中都会用到。
- 输入 $n$ 个元素并建堆的时间复杂度可以优化至 $O(n)$ ，非常高效。
- Top-k 是一个经典算法问题，可以使用堆数据结构高效解决，时间复杂度为 $O(n \log k)$ 。

### Q & A

**Q**：数据结构的“堆”与内存管理的“堆”是同一个概念吗？

两者不是同一个概念，只是碰巧都叫“堆”。计算机系统内存中的堆是动态内存分配的一部分，程序在运行时可以使用它来存储数据。程序可以请求一定量的堆内存，用于存储如对象和数组等复杂结构。当这些数据不再需要时，程序需要释放这些内存，以防止内存泄漏。相较于栈内存，堆内存的管理和使用需要更谨慎，使用不当可能会导致内存泄漏和野指针等问题。


## chapter_heap / top_k

# Top-k 问题

!!! question

    给定一个长度为 $n$ 的无序数组 `nums` ，请返回数组中最大的 $k$ 个元素。

对于该问题，我们先介绍两种思路比较直接的解法，再介绍效率更高的堆解法。

## 方法一：遍历选择

我们可以进行下图所示的 $k$ 轮遍历，分别在每轮中提取第 $1$、$2$、$\dots$、$k$ 大的元素，时间复杂度为 $O(nk)$ 。

此方法只适用于 $k \ll n$ 的情况，因为当 $k$ 与 $n$ 比较接近时，其时间复杂度趋向于 $O(n^2)$ ，非常耗时。

![遍历寻找最大的 k 个元素](top_k.assets/top_k_traversal.png)

!!! tip

    当 $k = n$ 时，我们可以得到完整的有序序列，此时等价于“选择排序”算法。

## 方法二：排序

如下图所示，我们可以先对数组 `nums` 进行排序，再返回最右边的 $k$ 个元素，时间复杂度为 $O(n \log n)$ 。

显然，该方法“超额”完成任务了，因为我们只需找出最大的 $k$ 个元素即可，而不需要排序其他元素。

![排序寻找最大的 k 个元素](top_k.assets/top_k_sorting.png)

## 方法三：堆

我们可以基于堆更加高效地解决 Top-k 问题，流程如下图所示。

1. 初始化一个小顶堆，其堆顶元素最小。
2. 先将数组的前 $k$ 个元素依次入堆。
3. 从第 $k + 1$ 个元素开始，若当前元素大于堆顶元素，则将堆顶元素出堆，并将当前元素入堆。
4. 遍历完成后，堆中保存的就是最大的 $k$ 个元素。

=== "<1>"
    ![基于堆寻找最大的 k 个元素](top_k.assets/top_k_heap_step1.png)

=== "<2>"
    ![top_k_heap_step2](top_k.assets/top_k_heap_step2.png)

=== "<3>"
    ![top_k_heap_step3](top_k.assets/top_k_heap_step3.png)

=== "<4>"
    ![top_k_heap_step4](top_k.assets/top_k_heap_step4.png)

=== "<5>"
    ![top_k_heap_step5](top_k.assets/top_k_heap_step5.png)

=== "<6>"
    ![top_k_heap_step6](top_k.assets/top_k_heap_step6.png)

=== "<7>"
    ![top_k_heap_step7](top_k.assets/top_k_heap_step7.png)

=== "<8>"
    ![top_k_heap_step8](top_k.assets/top_k_heap_step8.png)

=== "<9>"
    ![top_k_heap_step9](top_k.assets/top_k_heap_step9.png)

示例代码如下：

```src
[file]{top_k}-[class]{}-[func]{top_k_heap}
```

总共执行了 $n$ 轮入堆和出堆，堆的最大长度为 $k$ ，因此时间复杂度为 $O(n \log k)$ 。该方法的效率很高，当 $k$ 较小时，时间复杂度趋向 $O(n)$ ；当 $k$ 较大时，时间复杂度不会超过 $O(n \log n)$ 。

另外，该方法适用于动态数据流的使用场景。在不断加入数据时，我们可以持续维护堆内的元素，从而实现最大的 $k$ 个元素的动态更新。
