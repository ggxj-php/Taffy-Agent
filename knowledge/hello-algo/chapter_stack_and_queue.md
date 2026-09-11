

## chapter_stack_and_queue / deque

# 双向队列

在队列中，我们仅能删除头部元素或在尾部添加元素。如下图所示，<u>双向队列（double-ended queue）</u>提供了更高的灵活性，允许在头部和尾部执行元素的添加或删除操作。

![双向队列的操作](deque.assets/deque_operations.png)

## 双向队列常用操作

双向队列的常用操作如下表所示，具体的方法名称需要根据所使用的编程语言来确定。

<p align="center"> 表 <id> &nbsp; 双向队列操作效率 </p>

| 方法名         | 描述             | 时间复杂度 |
| -------------- | ---------------- | ---------- |
| `push_first()` | 将元素添加至队首 | $O(1)$     |
| `push_last()`  | 将元素添加至队尾 | $O(1)$     |
| `pop_first()`  | 删除队首元素     | $O(1)$     |
| `pop_last()`   | 删除队尾元素     | $O(1)$     |
| `peek_first()` | 访问队首元素     | $O(1)$     |
| `peek_last()`  | 访问队尾元素     | $O(1)$     |

同样地，我们可以直接使用编程语言中已实现的双向队列类：

=== "Python"

    ```python title="deque.py"
    from collections import deque

    # 初始化双向队列
    deq: deque[int] = deque()

    # 元素入队
    deq.append(2)      # 添加至队尾
    deq.append(5)
    deq.append(4)
    deq.appendleft(3)  # 添加至队首
    deq.appendleft(1)

    # 访问元素
    front: int = deq[0]  # 队首元素
    rear: int = deq[-1]  # 队尾元素

    # 元素出队
    pop_front: int = deq.popleft()  # 队首元素出队
    pop_rear: int = deq.pop()       # 队尾元素出队

    # 获取双向队列的长度
    size: int = len(deq)

    # 判断双向队列是否为空
    is_empty: bool = len(deq) == 0
    ```

=== "C++"

    ```cpp title="deque.cpp"
    /* 初始化双向队列 */
    deque<int> deque;

    /* 元素入队 */
    deque.push_back(2);   // 添加至队尾
    deque.push_back(5);
    deque.push_back(4);
    deque.push_front(3);  // 添加至队首
    deque.push_front(1);

    /* 访问元素 */
    int front = deque.front(); // 队首元素
    int back = deque.back();   // 队尾元素

    /* 元素出队 */
    deque.pop_front();  // 队首元素出队
    deque.pop_back();   // 队尾元素出队

    /* 获取双向队列的长度 */
    int size = deque.size();

    /* 判断双向队列是否为空 */
    bool empty = deque.empty();
    ```

=== "Java"

    ```java title="deque.java"
    /* 初始化双向队列 */
    Deque<Integer> deque = new LinkedList<>();

    /* 元素入队 */
    deque.offerLast(2);   // 添加至队尾
    deque.offerLast(5);
    deque.offerLast(4);
    deque.offerFirst(3);  // 添加至队首
    deque.offerFirst(1);

    /* 访问元素 */
    int peekFirst = deque.peekFirst();  // 队首元素
    int peekLast = deque.peekLast();    // 队尾元素

    /* 元素出队 */
    int popFirst = deque.pollFirst();  // 队首元素出队
    int popLast = deque.pollLast();    // 队尾元素出队

    /* 获取双向队列的长度 */
    int size = deque.size();

    /* 判断双向队列是否为空 */
    boolean isEmpty = deque.isEmpty();
    ```

=== "C#"

    ```csharp title="deque.cs"
    /* 初始化双向队列 */
    // 在 C# 中，将链表 LinkedList 看作双向队列来使用
    LinkedList<int> deque = new();

    /* 元素入队 */
    deque.AddLast(2);   // 添加至队尾
    deque.AddLast(5);
    deque.AddLast(4);
    deque.AddFirst(3);  // 添加至队首
    deque.AddFirst(1);

    /* 访问元素 */
    int peekFirst = deque.First.Value;  // 队首元素
    int peekLast = deque.Last.Value;    // 队尾元素

    /* 元素出队 */
    deque.RemoveFirst();  // 队首元素出队
    deque.RemoveLast();   // 队尾元素出队

    /* 获取双向队列的长度 */
    int size = deque.Count;

    /* 判断双向队列是否为空 */
    bool isEmpty = deque.Count == 0;
    ```

=== "Go"

    ```go title="deque_test.go"
    /* 初始化双向队列 */
    // 在 Go 中，将 list 作为双向队列使用
    deque := list.New()

    /* 元素入队 */
    deque.PushBack(2)      // 添加至队尾
    deque.PushBack(5)
    deque.PushBack(4)
    deque.PushFront(3)     // 添加至队首
    deque.PushFront(1)

    /* 访问元素 */
    front := deque.Front() // 队首元素
    rear := deque.Back()   // 队尾元素

    /* 元素出队 */
    deque.Remove(front)    // 队首元素出队
    deque.Remove(rear)     // 队尾元素出队

    /* 获取双向队列的长度 */
    size := deque.Len()

    /* 判断双向队列是否为空 */
    isEmpty := deque.Len() == 0
    ```

=== "Swift"

    ```swift title="deque.swift"
    /* 初始化双向队列 */
    // Swift 没有内置的双向队列类，可以把 Array 当作双向队列来使用
    var deque: [Int] = []

    /* 元素入队 */
    deque.append(2) // 添加至队尾
    deque.append(5)
    deque.append(4)
    deque.insert(3, at: 0) // 添加至队首
    deque.insert(1, at: 0)

    /* 访问元素 */
    let peekFirst = deque.first! // 队首元素
    let peekLast = deque.last! // 队尾元素

    /* 元素出队 */
    // 使用 Array 模拟时 popFirst 的复杂度为 O(n)
    let popFirst = deque.removeFirst() // 队首元素出队
    let popLast = deque.removeLast() // 队尾元素出队

    /* 获取双向队列的长度 */
    let size = deque.count

    /* 判断双向队列是否为空 */
    let isEmpty = deque.isEmpty
    ```

=== "JS"

    ```javascript title="deque.js"
    /* 初始化双向队列 */
    // JavaScript 没有内置的双端队列，只能把 Array 当作双端队列来使用
    const deque = [];

    /* 元素入队 */
    deque.push(2);
    deque.push(5);
    deque.push(4);
    // 请注意，由于是数组，unshift() 方法的时间复杂度为 O(n)
    deque.unshift(3);
    deque.unshift(1);

    /* 访问元素 */
    const peekFirst = deque[0];
    const peekLast = deque[deque.length - 1];

    /* 元素出队 */
    // 请注意，由于是数组，shift() 方法的时间复杂度为 O(n)
    const popFront = deque.shift();
    const popBack = deque.pop();

    /* 获取双向队列的长度 */
    const size = deque.length;

    /* 判断双向队列是否为空 */
    const isEmpty = size === 0;
    ```

=== "TS"

    ```typescript title="deque.ts"
    /* 初始化双向队列 */
    // TypeScript 没有内置的双端队列，只能把 Array 当作双端队列来使用
    const deque: number[] = [];

    /* 元素入队 */
    deque.push(2);
    deque.push(5);
    deque.push(4);
    // 请注意，由于是数组，unshift() 方法的时间复杂度为 O(n)
    deque.unshift(3);
    deque.unshift(1);

    /* 访问元素 */
    const peekFirst: number = deque[0];
    const peekLast: number = deque[deque.length - 1];

    /* 元素出队 */
    // 请注意，由于是数组，shift() 方法的时间复杂度为 O(n)
    const popFront: number = deque.shift() as number;
    const popBack: number = deque.pop() as number;

    /* 获取双向队列的长度 */
    const size: number = deque.length;

    /* 判断双向队列是否为空 */
    const isEmpty: boolean = size === 0;
    ```

=== "Dart"

    ```dart title="deque.dart"
    /* 初始化双向队列 */
    // 在 Dart 中，Queue 被定义为双向队列
    Queue<int> deque = Queue<int>();

    /* 元素入队 */
    deque.addLast(2);  // 添加至队尾
    deque.addLast(5);
    deque.addLast(4);
    deque.addFirst(3); // 添加至队首
    deque.addFirst(1);

    /* 访问元素 */
    int peekFirst = deque.first; // 队首元素
    int peekLast = deque.last;   // 队尾元素

    /* 元素出队 */
    int popFirst = deque.removeFirst(); // 队首元素出队
    int popLast = deque.removeLast();   // 队尾元素出队

    /* 获取双向队列的长度 */
    int size = deque.length;

    /* 判断双向队列是否为空 */
    bool isEmpty = deque.isEmpty;
    ```

=== "Rust"

    ```rust title="deque.rs"
    /* 初始化双向队列 */
    let mut deque: VecDeque<u32> = VecDeque::new();

    /* 元素入队 */
    deque.push_back(2);  // 添加至队尾
    deque.push_back(5);
    deque.push_back(4);
    deque.push_front(3); // 添加至队首
    deque.push_front(1);

    /* 访问元素 */
    if let Some(front) = deque.front() { // 队首元素
    }
    if let Some(rear) = deque.back() {   // 队尾元素
    }

    /* 元素出队 */
    if let Some(pop_front) = deque.pop_front() { // 队首元素出队
    }
    if let Some(pop_rear) = deque.pop_back() {   // 队尾元素出队
    }

    /* 获取双向队列的长度 */
    let size = deque.len();

    /* 判断双向队列是否为空 */
    let is_empty = deque.is_empty();
    ```

=== "C"

    ```c title="deque.c"
    // C 未提供内置双向队列
    ```

=== "Kotlin"

    ```kotlin title="deque.kt"
    /* 初始化双向队列 */
    val deque = LinkedList<Int>()

    /* 元素入队 */
    deque.offerLast(2)  // 添加至队尾
    deque.offerLast(5)
    deque.offerLast(4)
    deque.offerFirst(3) // 添加至队首
    deque.offerFirst(1)

    /* 访问元素 */
    val peekFirst = deque.peekFirst() // 队首元素
    val peekLast = deque.peekLast()   // 队尾元素

    /* 元素出队 */
    val popFirst = deque.pollFirst() // 队首元素出队
    val popLast = deque.pollLast()   // 队尾元素出队

    /* 获取双向队列的长度 */
    val size = deque.size

    /* 判断双向队列是否为空 */
    val isEmpty = deque.isEmpty()
    ```

=== "Ruby"

    ```ruby title="deque.rb"
    # 初始化双向队列
    # Ruby 没有内直的双端队列，只能把 Array 当作双端队列来使用
    deque = []

    # 元素如队
    deque << 2
    deque << 5
    deque << 4
    # 请注意，由于是数组，Array#unshift 方法的时间复杂度为 O(n)
    deque.unshift(3)
    deque.unshift(1)

    # 访问元素
    peek_first = deque.first
    peek_last = deque.last

    # 元素出队
    # 请注意，由于是数组， Array#shift 方法的时间复杂度为 O(n)
    pop_front = deque.shift
    pop_back = deque.pop

    # 获取双向队列的长度
    size = deque.length

    # 判断双向队列是否为空
    is_empty = size.zero?
    ```

??? pythontutor "可视化运行"

    https://pythontutor.com/render.html#code=from%20collections%20import%20deque%0A%0A%22%22%22Driver%20Code%22%22%22%0Aif%20__name__%20%3D%3D%20%22__main__%22%3A%0A%20%20%20%20%23%20%E5%88%9D%E5%A7%8B%E5%8C%96%E5%8F%8C%E5%90%91%E9%98%9F%E5%88%97%0A%20%20%20%20deq%20%3D%20deque%28%29%0A%0A%20%20%20%20%23%20%E5%85%83%E7%B4%A0%E5%85%A5%E9%98%9F%0A%20%20%20%20deq.append%282%29%20%20%23%20%E6%B7%BB%E5%8A%A0%E8%87%B3%E9%98%9F%E5%B0%BE%0A%20%20%20%20deq.append%285%29%0A%20%20%20%20deq.append%284%29%0A%20%20%20%20deq.appendleft%283%29%20%20%23%20%E6%B7%BB%E5%8A%A0%E8%87%B3%E9%98%9F%E9%A6%96%0A%20%20%20%20deq.appendleft%281%29%0A%20%20%20%20print%28%22%E5%8F%8C%E5%90%91%E9%98%9F%E5%88%97%20deque%20%3D%22,%20deq%29%0A%0A%20%20%20%20%23%20%E8%AE%BF%E9%97%AE%E5%85%83%E7%B4%A0%0A%20%20%20%20front%20%3D%20deq%5B0%5D%20%20%23%20%E9%98%9F%E9%A6%96%E5%85%83%E7%B4%A0%0A%20%20%20%20print%28%22%E9%98%9F%E9%A6%96%E5%85%83%E7%B4%A0%20front%20%3D%22,%20front%29%0A%20%20%20%20rear%20%3D%20deq%5B-1%5D%20%20%23%20%E9%98%9F%E5%B0%BE%E5%85%83%E7%B4%A0%0A%20%20%20%20print%28%22%E9%98%9F%E5%B0%BE%E5%85%83%E7%B4%A0%20rear%20%3D%22,%20rear%29%0A%0A%20%20%20%20%23%20%E5%85%83%E7%B4%A0%E5%87%BA%E9%98%9F%0A%20%20%20%20pop_front%20%3D%20deq.popleft%28%29%20%20%23%20%E9%98%9F%E9%A6%96%E5%85%83%E7%B4%A0%E5%87%BA%E9%98%9F%0A%20%20%20%20print%28%22%E9%98%9F%E9%A6%96%E5%87%BA%E9%98%9F%E5%85%83%E7%B4%A0%20%20pop_front%20%3D%22,%20pop_front%29%0A%20%20%20%20print%28%22%E9%98%9F%E9%A6%96%E5%87%BA%E9%98%9F%E5%90%8E%20deque%20%3D%22,%20deq%29%0A%20%20%20%20pop_rear%20%3D%20deq.pop%28%29%20%20%23%20%E9%98%9F%E5%B0%BE%E5%85%83%E7%B4%A0%E5%87%BA%E9%98%9F%0A%20%20%20%20print%28%22%E9%98%9F%E5%B0%BE%E5%87%BA%E9%98%9F%E5%85%83%E7%B4%A0%20%20pop_rear%20%3D%22,%20pop_rear%29%0A%20%20%20%20print%28%22%E9%98%9F%E5%B0%BE%E5%87%BA%E9%98%9F%E5%90%8E%20deque%20%3D%22,%20deq%29%0A%0A%20%20%20%20%23%20%E8%8E%B7%E5%8F%96%E5%8F%8C%E5%90%91%E9%98%9F%E5%88%97%E7%9A%84%E9%95%BF%E5%BA%A6%0A%20%20%20%20size%20%3D%20len%28deq%29%0A%20%20%20%20print%28%22%E5%8F%8C%E5%90%91%E9%98%9F%E5%88%97%E9%95%BF%E5%BA%A6%20size%20%3D%22,%20size%29%0A%0A%20%20%20%20%23%20%E5%88%A4%E6%96%AD%E5%8F%8C%E5%90%91%E9%98%9F%E5%88%97%E6%98%AF%E5%90%A6%E4%B8%BA%E7%A9%BA%0A%20%20%20%20is_empty%20%3D%20len%28deq%29%20%3D%3D%200%0A%20%20%20%20print%28%22%E5%8F%8C%E5%90%91%E9%98%9F%E5%88%97%E6%98%AF%E5%90%A6%E4%B8%BA%E7%A9%BA%20%3D%22,%20is_empty%29&cumulative=false&curInstr=3&heapPrimitives=nevernest&mode=display&origin=opt-frontend.js&py=311&rawInputLstJSON=%5B%5D&textReferences=false

## 双向队列实现 *

双向队列的实现与队列类似，可以选择链表或数组作为底层数据结构。

### 基于双向链表的实现

回顾上一节内容，我们使用普通单向链表来实现队列，因为它可以方便地删除头节点（对应出队操作）和在尾节点后添加新节点（对应入队操作）。

对于双向队列而言，头部和尾部都可以执行入队和出队操作。换句话说，双向队列需要实现另一个对称方向的操作。为此，我们采用“双向链表”作为双向队列的底层数据结构。

如下图所示，我们将双向链表的头节点和尾节点视为双向队列的队首和队尾，同时实现在两端添加和删除节点的功能。

=== "<1>"
    ![基于链表实现双向队列的入队出队操作](deque.assets/linkedlist_deque_step1.png)

=== "<2>"
    ![linkedlist_deque_push_last](deque.assets/linkedlist_deque_step2_push_last.png)

=== "<3>"
    ![linkedlist_deque_push_first](deque.assets/linkedlist_deque_step3_push_first.png)

=== "<4>"
    ![linkedlist_deque_pop_last](deque.assets/linkedlist_deque_step4_pop_last.png)

=== "<5>"
    ![linkedlist_deque_pop_first](deque.assets/linkedlist_deque_step5_pop_first.png)

实现代码如下所示：

```src
[file]{linkedlist_deque}-[class]{linked_list_deque}-[func]{}
```

### 基于数组的实现

如下图所示，与基于数组实现队列类似，我们也可以使用环形数组来实现双向队列。

=== "<1>"
    ![基于数组实现双向队列的入队出队操作](deque.assets/array_deque_step1.png)

=== "<2>"
    ![array_deque_push_last](deque.assets/array_deque_step2_push_last.png)

=== "<3>"
    ![array_deque_push_first](deque.assets/array_deque_step3_push_first.png)

=== "<4>"
    ![array_deque_pop_last](deque.assets/array_deque_step4_pop_last.png)

=== "<5>"
    ![array_deque_pop_first](deque.assets/array_deque_step5_pop_first.png)

在队列的实现基础上，仅需增加“队首入队”和“队尾出队”的方法：

```src
[file]{array_deque}-[class]{array_deque}-[func]{}
```

## 双向队列应用

双向队列兼具栈与队列的逻辑，**因此它可以实现这两者的所有应用场景，同时提供更高的自由度**。

我们知道，软件的“撤销”功能通常使用栈来实现：系统将每次更改操作 `push` 到栈中，然后通过 `pop` 实现撤销。然而，考虑到系统资源的限制，软件通常会限制撤销的步数（例如仅允许保存 $50$ 步）。当栈的长度超过 $50$ 时，软件需要在栈底（队首）执行删除操作。**但栈无法实现该功能，此时就需要使用双向队列来替代栈**。请注意，“撤销”的核心逻辑仍然遵循栈的先入后出原则，只是双向队列能够更加灵活地实现一些额外逻辑。


## chapter_stack_and_queue / exercises

# 练习

## 知识巩固

### 栈和队列会先取出谁

准备一个空栈 `S` 和一个空队列 `Q`，分别对它们执行下面同一组操作：

步骤 1：加入 `A`；
步骤 2：加入 `B`；
步骤 3：移除一个元素并记录；
步骤 4：加入 `C`；
步骤 5：不断移除并记录，直到容器为空。

请分别写出 `S` 和 `Q` 中元素被移除的顺序，并用“先入后出”或“先入先出”解释差异。

??? success "参考答案"

    栈 `S` 的移除顺序是 `B、C、A`：加入 `A、B` 后先弹出最近加入的 `B`，再加入 `C`，
    此后依次弹出 `C、A`，体现“先入后出”。

    队列 `Q` 的移除顺序是 `A、B、C`：加入 `A、B` 后先移除最早加入的 `A`，
    再加入 `C`，此后依次移除 `B、C`，体现“先入先出”。

### 队尾越过数组末尾怎么办

用长度为 5 的环形数组实现队列，数组索引为 `0～4`。
当前 `front = 3`、`size = 2`，队列中的 `A、B` 分别位于索引 3、4。

<!-- numbered-subquestions -->

1. 执行“`C` 入队”时，`C` 应放在哪个索引？入队后 `size` 是多少？
2. 接着执行一次出队，弹出哪个元素？新的 `front` 和 `size` 分别是多少？
3. 此时从队首到队尾的逻辑顺序是什么？出队时是否需要移动数组中的其他元素？为什么？

??? success "参考答案"

    1. 新元素的位置为
        `(front + size) % 5 = (3 + 2) % 5 = 0`，
        所以 `C` 放在索引 0。入队后 `size = 3`。

    2. 出队弹出当前队首 `A`。新的队首索引为
        `(3 + 1) % 5 = 4`，因此 `front = 4`、`size = 2`。

    3. 有效元素的逻辑顺序为 `B、C`，其中 `B` 位于索引 4，`C` 位于索引 0。
        出队时只需移动 `front` 并修改 `size`，环形数组用取余让索引回到开头，
        因此无须把其他元素整体向前移动。

### 双向队列的两端操作

这里规定：`push_first` 表示从队首加入，`push_last` 表示从队尾加入，
`pop_first` 表示从队首弹出，`pop_last` 表示从队尾弹出。

对一个空的双向队列 `deq` 依次执行：

1. `push_last(A)`
2. `push_last(B)`
3. `push_first(C)`
4. `pop_last()`
5. `push_last(D)`
6. `pop_first()`

<!-- numbered-subquestions -->

1. 两次弹出的元素分别是什么？
2. 全部操作完成后，从队首到队尾还剩哪些元素？
3. 检查这 6 步操作：只允许从队尾加入、从队首删除的队列能否全部完成？如果不能，请指出无法完成的操作；再说明双向队列能否完成及其原因。

??? success "参考答案"

    前三步后，双向队列从队首到队尾为 `[C, A, B]`。

    <!-- numbered-subquestions -->

    1. `pop_last()` 弹出 `B`；加入 `D` 后队列为 `[C, A, D]`，
        `pop_first()` 再弹出 `C`。

    2. 最后剩下 `[A, D]`。

    3. 只允许在队尾添加、在队首删除的队列不能完成全部操作：
        第 3 步 `push_first(C)` 要求从队首加入，第 4 步 `pop_last()` 要求从队尾删除，都超出了这种队列的操作范围。
        双向队列的两端都可以添加和删除，因此能够完成这 6 步操作。

## 编程练习

### 检查括号序列

给定一个只包含 `()`、`[]`、`{}` 这三类括号的字符串 `s`，请使用栈判断它是否合法。

合法序列须同时满足：每个右括号都必须与最近一个尚未配对的左括号类型匹配，
并且遍历结束后没有未配对的左括号。返回布尔值表示判断结果。

??? tip "解题提示"

    1. 可以建立“右括号到对应左括号”的映射
    2. 遇到右括号时，先检查栈是否为空，再检查栈顶是否匹配
    3. 遍历结束后，栈也必须为空

[LeetCode](https://leetcode.cn/problems/valid-parentheses/){ .rounded-button .exercise-button target="_blank" rel="noopener noreferrer" } [题目解析](https://leetcode.cn/problems/valid-parentheses/solutions/9185/valid-parentheses-fu-zhu-zhan-fa-by-jin407891080/){ .rounded-button .exercise-button target="_blank" rel="noopener noreferrer" }


## chapter_stack_and_queue / queue

# 队列

<u>队列（queue）</u>是一种遵循先入先出规则的线性数据结构。顾名思义，队列模拟了排队现象，即新来的人不断加入队列尾部，而位于队列头部的人逐个离开。

如下图所示，我们将队列头部称为“队首”，尾部称为“队尾”，将把元素加入队尾的操作称为“入队”，删除队首元素的操作称为“出队”。

![队列的先入先出规则](queue.assets/queue_operations.png)

## 队列常用操作

队列的常见操作如下表所示。需要注意的是，不同编程语言的方法名称可能会有所不同。我们在此采用与栈相同的方法命名。

<p align="center"> 表 <id> &nbsp; 队列操作效率 </p>

| 方法名   | 描述                         | 时间复杂度 |
| -------- | ---------------------------- | ---------- |
| `push()` | 元素入队，即将元素添加至队尾 | $O(1)$     |
| `pop()`  | 队首元素出队                 | $O(1)$     |
| `peek()` | 访问队首元素                 | $O(1)$     |

我们可以直接使用编程语言中现成的队列类：

=== "Python"

    ```python title="queue.py"
    from collections import deque

    # 初始化队列
    # 在 Python 中，我们一般将双向队列类 deque 当作队列使用
    # 虽然 queue.Queue() 是纯正的队列类，但不太好用，因此不推荐
    que: deque[int] = deque()

    # 元素入队
    que.append(1)
    que.append(3)
    que.append(2)
    que.append(5)
    que.append(4)

    # 访问队首元素
    front: int = que[0]

    # 元素出队
    pop: int = que.popleft()

    # 获取队列的长度
    size: int = len(que)

    # 判断队列是否为空
    is_empty: bool = len(que) == 0
    ```

=== "C++"

    ```cpp title="queue.cpp"
    /* 初始化队列 */
    queue<int> queue;

    /* 元素入队 */
    queue.push(1);
    queue.push(3);
    queue.push(2);
    queue.push(5);
    queue.push(4);

    /* 访问队首元素 */
    int front = queue.front();

    /* 元素出队 */
    queue.pop();

    /* 获取队列的长度 */
    int size = queue.size();

    /* 判断队列是否为空 */
    bool empty = queue.empty();
    ```

=== "Java"

    ```java title="queue.java"
    /* 初始化队列 */
    Queue<Integer> queue = new LinkedList<>();

    /* 元素入队 */
    queue.offer(1);
    queue.offer(3);
    queue.offer(2);
    queue.offer(5);
    queue.offer(4);

    /* 访问队首元素 */
    int peek = queue.peek();

    /* 元素出队 */
    int pop = queue.poll();

    /* 获取队列的长度 */
    int size = queue.size();

    /* 判断队列是否为空 */
    boolean isEmpty = queue.isEmpty();
    ```

=== "C#"

    ```csharp title="queue.cs"
    /* 初始化队列 */
    Queue<int> queue = new();

    /* 元素入队 */
    queue.Enqueue(1);
    queue.Enqueue(3);
    queue.Enqueue(2);
    queue.Enqueue(5);
    queue.Enqueue(4);

    /* 访问队首元素 */
    int peek = queue.Peek();

    /* 元素出队 */
    int pop = queue.Dequeue();

    /* 获取队列的长度 */
    int size = queue.Count;

    /* 判断队列是否为空 */
    bool isEmpty = queue.Count == 0;
    ```

=== "Go"

    ```go title="queue_test.go"
    /* 初始化队列 */
    // 在 Go 中，将 list 作为队列来使用
    queue := list.New()

    /* 元素入队 */
    queue.PushBack(1)
    queue.PushBack(3)
    queue.PushBack(2)
    queue.PushBack(5)
    queue.PushBack(4)

    /* 访问队首元素 */
    peek := queue.Front()

    /* 元素出队 */
    pop := queue.Front()
    queue.Remove(pop)

    /* 获取队列的长度 */
    size := queue.Len()

    /* 判断队列是否为空 */
    isEmpty := queue.Len() == 0
    ```

=== "Swift"

    ```swift title="queue.swift"
    /* 初始化队列 */
    // Swift 没有内置的队列类，可以把 Array 当作队列来使用
    var queue: [Int] = []

    /* 元素入队 */
    queue.append(1)
    queue.append(3)
    queue.append(2)
    queue.append(5)
    queue.append(4)

    /* 访问队首元素 */
    let peek = queue.first!

    /* 元素出队 */
    // 由于是数组，因此 removeFirst 的复杂度为 O(n)
    let pop = queue.removeFirst()

    /* 获取队列的长度 */
    let size = queue.count

    /* 判断队列是否为空 */
    let isEmpty = queue.isEmpty
    ```

=== "JS"

    ```javascript title="queue.js"
    /* 初始化队列 */
    // JavaScript 没有内置的队列，可以把 Array 当作队列来使用
    const queue = [];

    /* 元素入队 */
    queue.push(1);
    queue.push(3);
    queue.push(2);
    queue.push(5);
    queue.push(4);

    /* 访问队首元素 */
    const peek = queue[0];

    /* 元素出队 */
    // 底层是数组，因此 shift() 方法的时间复杂度为 O(n)
    const pop = queue.shift();

    /* 获取队列的长度 */
    const size = queue.length;

    /* 判断队列是否为空 */
    const empty = queue.length === 0;
    ```

=== "TS"

    ```typescript title="queue.ts"
    /* 初始化队列 */
    // TypeScript 没有内置的队列，可以把 Array 当作队列来使用
    const queue: number[] = [];

    /* 元素入队 */
    queue.push(1);
    queue.push(3);
    queue.push(2);
    queue.push(5);
    queue.push(4);

    /* 访问队首元素 */
    const peek = queue[0];

    /* 元素出队 */
    // 底层是数组，因此 shift() 方法的时间复杂度为 O(n)
    const pop = queue.shift();

    /* 获取队列的长度 */
    const size = queue.length;

    /* 判断队列是否为空 */
    const empty = queue.length === 0;
    ```

=== "Dart"

    ```dart title="queue.dart"
    /* 初始化队列 */
    // 在 Dart 中，队列类 Queue 是双向队列，也可作为队列使用
    Queue<int> queue = Queue();

    /* 元素入队 */
    queue.add(1);
    queue.add(3);
    queue.add(2);
    queue.add(5);
    queue.add(4);

    /* 访问队首元素 */
    int peek = queue.first;

    /* 元素出队 */
    int pop = queue.removeFirst();

    /* 获取队列的长度 */
    int size = queue.length;

    /* 判断队列是否为空 */
    bool isEmpty = queue.isEmpty;
    ```

=== "Rust"

    ```rust title="queue.rs"
    /* 初始化双向队列 */
    // 在 Rust 中使用双向队列作为普通队列来使用
    let mut deque: VecDeque<u32> = VecDeque::new();

    /* 元素入队 */
    deque.push_back(1);
    deque.push_back(3);
    deque.push_back(2);
    deque.push_back(5);
    deque.push_back(4);

    /* 访问队首元素 */
    if let Some(front) = deque.front() {
    }

    /* 元素出队 */
    if let Some(pop) = deque.pop_front() {
    }

    /* 获取队列的长度 */
    let size = deque.len();

    /* 判断队列是否为空 */
    let is_empty = deque.is_empty();
    ```

=== "C"

    ```c title="queue.c"
    // C 未提供内置队列
    ```

=== "Kotlin"

    ```kotlin title="queue.kt"
    /* 初始化队列 */
    val queue = LinkedList<Int>()

    /* 元素入队 */
    queue.offer(1)
    queue.offer(3)
    queue.offer(2)
    queue.offer(5)
    queue.offer(4)

    /* 访问队首元素 */
    val peek = queue.peek()

    /* 元素出队 */
    val pop = queue.poll()

    /* 获取队列的长度 */
    val size = queue.size

    /* 判断队列是否为空 */
    val isEmpty = queue.isEmpty()
    ```

=== "Ruby"

    ```ruby title="queue.rb"
    # 初始化队列
    # Ruby 内置的队列（Thread::Queue) 没有 peek 和遍历方法，可以把 Array 当作队列来使用
    queue = []

    # 元素入队
    queue.push(1)
    queue.push(3)
    queue.push(2)
    queue.push(5)
    queue.push(4)

    # 访问队列元素
    peek = queue.first

    # 元素出队
    # 清注意，由于是数组，Array#shift 方法时间复杂度为 O(n)
    pop = queue.shift

    # 获取队列的长度
    size = queue.length

    # 判断队列是否为空
    is_empty = queue.empty?
    ```

??? pythontutor "可视化运行"

    https://pythontutor.com/render.html#code=from%20collections%20import%20deque%0A%0A%22%22%22Driver%20Code%22%22%22%0Aif%20__name__%20%3D%3D%20%22__main__%22%3A%0A%20%20%20%20%23%20%E5%88%9D%E5%A7%8B%E5%8C%96%E9%98%9F%E5%88%97%0A%20%20%20%20%23%20%E5%9C%A8%20Python%20%E4%B8%AD%EF%BC%8C%E6%88%91%E4%BB%AC%E4%B8%80%E8%88%AC%E5%B0%86%E5%8F%8C%E5%90%91%E9%98%9F%E5%88%97%E7%B1%BB%20deque%20%E7%9C%8B%E4%BD%9C%E9%98%9F%E5%88%97%E4%BD%BF%E7%94%A8%0A%20%20%20%20%23%20%E8%99%BD%E7%84%B6%20queue.Queue%28%29%20%E6%98%AF%E7%BA%AF%E6%AD%A3%E7%9A%84%E9%98%9F%E5%88%97%E7%B1%BB%EF%BC%8C%E4%BD%86%E4%B8%8D%E5%A4%AA%E5%A5%BD%E7%94%A8%0A%20%20%20%20que%20%3D%20deque%28%29%0A%0A%20%20%20%20%23%20%E5%85%83%E7%B4%A0%E5%85%A5%E9%98%9F%0A%20%20%20%20que.append%281%29%0A%20%20%20%20que.append%283%29%0A%20%20%20%20que.append%282%29%0A%20%20%20%20que.append%285%29%0A%20%20%20%20que.append%284%29%0A%20%20%20%20print%28%22%E9%98%9F%E5%88%97%20que%20%3D%22,%20que%29%0A%0A%20%20%20%20%23%20%E8%AE%BF%E9%97%AE%E9%98%9F%E9%A6%96%E5%85%83%E7%B4%A0%0A%20%20%20%20front%20%3D%20que%5B0%5D%0A%20%20%20%20print%28%22%E9%98%9F%E9%A6%96%E5%85%83%E7%B4%A0%20front%20%3D%22,%20front%29%0A%0A%20%20%20%20%23%20%E5%85%83%E7%B4%A0%E5%87%BA%E9%98%9F%0A%20%20%20%20pop%20%3D%20que.popleft%28%29%0A%20%20%20%20print%28%22%E5%87%BA%E9%98%9F%E5%85%83%E7%B4%A0%20pop%20%3D%22,%20pop%29%0A%20%20%20%20print%28%22%E5%87%BA%E9%98%9F%E5%90%8E%20que%20%3D%22,%20que%29%0A%0A%20%20%20%20%23%20%E8%8E%B7%E5%8F%96%E9%98%9F%E5%88%97%E7%9A%84%E9%95%BF%E5%BA%A6%0A%20%20%20%20size%20%3D%20len%28que%29%0A%20%20%20%20print%28%22%E9%98%9F%E5%88%97%E9%95%BF%E5%BA%A6%20size%20%3D%22,%20size%29%0A%0A%20%20%20%20%23%20%E5%88%A4%E6%96%AD%E9%98%9F%E5%88%97%E6%98%AF%E5%90%A6%E4%B8%BA%E7%A9%BA%0A%20%20%20%20is_empty%20%3D%20len%28que%29%20%3D%3D%200%0A%20%20%20%20print%28%22%E9%98%9F%E5%88%97%E6%98%AF%E5%90%A6%E4%B8%BA%E7%A9%BA%20%3D%22,%20is_empty%29&cumulative=false&curInstr=3&heapPrimitives=nevernest&mode=display&origin=opt-frontend.js&py=311&rawInputLstJSON=%5B%5D&textReferences=false

## 队列实现

为了实现队列，我们需要一种数据结构，可以在一端添加元素，并在另一端删除元素，链表和数组都符合要求。

### 基于链表的实现

如下图所示，我们可以将链表的“头节点”和“尾节点”分别视为“队首”和“队尾”，规定队尾仅可添加节点，队首仅可删除节点。

=== "<1>"
    ![基于链表实现队列的入队出队操作](queue.assets/linkedlist_queue_step1.png)

=== "<2>"
    ![linkedlist_queue_push](queue.assets/linkedlist_queue_step2_push.png)

=== "<3>"
    ![linkedlist_queue_pop](queue.assets/linkedlist_queue_step3_pop.png)

以下是用链表实现队列的代码：

```src
[file]{linkedlist_queue}-[class]{linked_list_queue}-[func]{}
```

### 基于数组的实现

在数组中删除首元素的时间复杂度为 $O(n)$ ，这会导致出队操作效率较低。然而，我们可以采用以下巧妙方法来避免这个问题。

我们可以使用一个变量 `front` 指向队首元素的索引，并维护一个变量 `size` 用于记录队列长度。定义 `rear = front + size` ，这个公式计算出的 `rear` 指向队尾元素之后的下一个位置。

基于此设计，**数组中包含元素的有效区间为 `[front, rear - 1]`**，各种操作的实现方法如下图所示。

- 入队操作：将输入元素赋值给 `rear` 索引处，并将 `size` 增加 1 。
- 出队操作：只需将 `front` 增加 1 ，并将 `size` 减少 1 。

可以看到，入队和出队操作都只需进行一次操作，时间复杂度均为 $O(1)$ 。

=== "<1>"
    ![基于数组实现队列的入队出队操作](queue.assets/array_queue_step1.png)

=== "<2>"
    ![array_queue_push](queue.assets/array_queue_step2_push.png)

=== "<3>"
    ![array_queue_pop](queue.assets/array_queue_step3_pop.png)

你可能会发现一个问题：在不断进行入队和出队的过程中，`front` 和 `rear` 都在向右移动，**当它们到达数组尾部时就无法继续移动了**。为了解决此问题，我们可以将数组视为首尾相接的“环形数组”。

对于环形数组，我们需要让 `front` 或 `rear` 在越过数组尾部时，直接回到数组头部继续遍历。这种周期性规律可以通过“取余操作”来实现，代码如下所示：

```src
[file]{array_queue}-[class]{array_queue}-[func]{}
```

以上实现的队列仍然具有局限性：其长度不可变。然而，这个问题不难解决，我们可以将数组替换为动态数组，从而引入扩容机制。有兴趣的读者可以尝试自行实现。

两种实现的对比结论与栈一致，在此不再赘述。

## 队列典型应用

- **淘宝订单**。购物者下单后，订单将加入队列中，系统随后会根据顺序处理队列中的订单。在双十一期间，短时间内会产生海量订单，高并发成为工程师们需要重点攻克的问题。
- **各类待办事项**。任何需要实现“先来后到”功能的场景，例如打印机的任务队列、餐厅的出餐队列等，队列在这些场景中可以有效地维护处理顺序。


## chapter_stack_and_queue / stack

# 栈

<u>栈（stack）</u>是一种遵循先入后出逻辑的线性数据结构。

我们可以将栈类比为桌面上的一摞盘子，规定每次只能移动一个盘子，那么想取出底部的盘子，则需要先将上面的盘子依次移走。我们将盘子替换为各种类型的元素（如整数、字符、对象等），就得到了栈这种数据结构。

如下图所示，我们把堆叠元素的顶部称为“栈顶”，底部称为“栈底”。将把元素添加到栈顶的操作叫作“入栈”，删除栈顶元素的操作叫作“出栈”。

![栈的先入后出规则](stack.assets/stack_operations.png)

## 栈的常用操作

栈的常用操作如下表所示，具体的方法名需要根据所使用的编程语言来确定。在此，我们以常见的 `push()`、`pop()`、`peek()` 命名为例。

<p align="center"> 表 <id> &nbsp; 栈的操作效率 </p>

| 方法     | 描述                   | 时间复杂度 |
| -------- | ---------------------- | ---------- |
| `push()` | 元素入栈（添加至栈顶） | $O(1)$     |
| `pop()`  | 栈顶元素出栈           | $O(1)$     |
| `peek()` | 访问栈顶元素           | $O(1)$     |

通常情况下，我们可以直接使用编程语言内置的栈类。然而，某些语言可能没有专门提供栈类，这时我们可以将该语言的“数组”或“链表”当作栈来使用，并在程序逻辑上忽略与栈无关的操作。

=== "Python"

    ```python title="stack.py"
    # 初始化栈
    # Python 没有内置的栈类，可以把 list 当作栈来使用
    stack: list[int] = []

    # 元素入栈
    stack.append(1)
    stack.append(3)
    stack.append(2)
    stack.append(5)
    stack.append(4)

    # 访问栈顶元素
    peek: int = stack[-1]

    # 元素出栈
    pop: int = stack.pop()

    # 获取栈的长度
    size: int = len(stack)

    # 判断是否为空
    is_empty: bool = len(stack) == 0
    ```

=== "C++"

    ```cpp title="stack.cpp"
    /* 初始化栈 */
    stack<int> stack;

    /* 元素入栈 */
    stack.push(1);
    stack.push(3);
    stack.push(2);
    stack.push(5);
    stack.push(4);

    /* 访问栈顶元素 */
    int top = stack.top();

    /* 元素出栈 */
    stack.pop(); // 无返回值

    /* 获取栈的长度 */
    int size = stack.size();

    /* 判断是否为空 */
    bool empty = stack.empty();
    ```

=== "Java"

    ```java title="stack.java"
    /* 初始化栈 */
    Stack<Integer> stack = new Stack<>();

    /* 元素入栈 */
    stack.push(1);
    stack.push(3);
    stack.push(2);
    stack.push(5);
    stack.push(4);

    /* 访问栈顶元素 */
    int peek = stack.peek();

    /* 元素出栈 */
    int pop = stack.pop();

    /* 获取栈的长度 */
    int size = stack.size();

    /* 判断是否为空 */
    boolean isEmpty = stack.isEmpty();
    ```

=== "C#"

    ```csharp title="stack.cs"
    /* 初始化栈 */
    Stack<int> stack = new();

    /* 元素入栈 */
    stack.Push(1);
    stack.Push(3);
    stack.Push(2);
    stack.Push(5);
    stack.Push(4);

    /* 访问栈顶元素 */
    int peek = stack.Peek();

    /* 元素出栈 */
    int pop = stack.Pop();

    /* 获取栈的长度 */
    int size = stack.Count;

    /* 判断是否为空 */
    bool isEmpty = stack.Count == 0;
    ```

=== "Go"

    ```go title="stack_test.go"
    /* 初始化栈 */
    // 在 Go 中，推荐将 Slice 当作栈来使用
    var stack []int

    /* 元素入栈 */
    stack = append(stack, 1)
    stack = append(stack, 3)
    stack = append(stack, 2)
    stack = append(stack, 5)
    stack = append(stack, 4)

    /* 访问栈顶元素 */
    peek := stack[len(stack)-1]

    /* 元素出栈 */
    pop := stack[len(stack)-1]
    stack = stack[:len(stack)-1]

    /* 获取栈的长度 */
    size := len(stack)

    /* 判断是否为空 */
    isEmpty := len(stack) == 0
    ```

=== "Swift"

    ```swift title="stack.swift"
    /* 初始化栈 */
    // Swift 没有内置的栈类，可以把 Array 当作栈来使用
    var stack: [Int] = []

    /* 元素入栈 */
    stack.append(1)
    stack.append(3)
    stack.append(2)
    stack.append(5)
    stack.append(4)

    /* 访问栈顶元素 */
    let peek = stack.last!

    /* 元素出栈 */
    let pop = stack.removeLast()

    /* 获取栈的长度 */
    let size = stack.count

    /* 判断是否为空 */
    let isEmpty = stack.isEmpty
    ```

=== "JS"

    ```javascript title="stack.js"
    /* 初始化栈 */
    // JavaScript 没有内置的栈类，可以把 Array 当作栈来使用
    const stack = [];

    /* 元素入栈 */
    stack.push(1);
    stack.push(3);
    stack.push(2);
    stack.push(5);
    stack.push(4);

    /* 访问栈顶元素 */
    const peek = stack[stack.length-1];

    /* 元素出栈 */
    const pop = stack.pop();

    /* 获取栈的长度 */
    const size = stack.length;

    /* 判断是否为空 */
    const is_empty = stack.length === 0;
    ```

=== "TS"

    ```typescript title="stack.ts"
    /* 初始化栈 */
    // TypeScript 没有内置的栈类，可以把 Array 当作栈来使用
    const stack: number[] = [];

    /* 元素入栈 */
    stack.push(1);
    stack.push(3);
    stack.push(2);
    stack.push(5);
    stack.push(4);

    /* 访问栈顶元素 */
    const peek = stack[stack.length - 1];

    /* 元素出栈 */
    const pop = stack.pop();

    /* 获取栈的长度 */
    const size = stack.length;

    /* 判断是否为空 */
    const is_empty = stack.length === 0;
    ```

=== "Dart"

    ```dart title="stack.dart"
    /* 初始化栈 */
    // Dart 没有内置的栈类，可以把 List 当作栈来使用
    List<int> stack = [];

    /* 元素入栈 */
    stack.add(1);
    stack.add(3);
    stack.add(2);
    stack.add(5);
    stack.add(4);

    /* 访问栈顶元素 */
    int peek = stack.last;

    /* 元素出栈 */
    int pop = stack.removeLast();

    /* 获取栈的长度 */
    int size = stack.length;

    /* 判断是否为空 */
    bool isEmpty = stack.isEmpty;
    ```

=== "Rust"

    ```rust title="stack.rs"
    /* 初始化栈 */
    // 把 Vec 当作栈来使用
    let mut stack: Vec<i32> = Vec::new();

    /* 元素入栈 */
    stack.push(1);
    stack.push(3);
    stack.push(2);
    stack.push(5);
    stack.push(4);

    /* 访问栈顶元素 */
    let top = stack.last().unwrap();

    /* 元素出栈 */
    let pop = stack.pop().unwrap();

    /* 获取栈的长度 */
    let size = stack.len();

    /* 判断是否为空 */
    let is_empty = stack.is_empty();
    ```

=== "C"

    ```c title="stack.c"
    // C 未提供内置栈
    ```

=== "Kotlin"

    ```kotlin title="stack.kt"
    /* 初始化栈 */
    val stack = Stack<Int>()

    /* 元素入栈 */
    stack.push(1)
    stack.push(3)
    stack.push(2)
    stack.push(5)
    stack.push(4)

    /* 访问栈顶元素 */
    val peek = stack.peek()

    /* 元素出栈 */
    val pop = stack.pop()

    /* 获取栈的长度 */
    val size = stack.size

    /* 判断是否为空 */
    val isEmpty = stack.isEmpty()
    ```

=== "Ruby"

    ```ruby title="stack.rb"
    # 初始化栈
    # Ruby 没有内置的栈类，可以把 Array 当作栈来使用
    stack = []

    # 元素入栈
    stack << 1
    stack << 3
    stack << 2
    stack << 5
    stack << 4

    # 访问栈顶元素
    peek = stack.last

    # 元素出栈
    pop = stack.pop

    # 获取栈的长度
    size = stack.length

    # 判断是否为空
    is_empty = stack.empty?
    ```

??? pythontutor "可视化运行"

    https://pythontutor.com/render.html#code=%22%22%22Driver%20Code%22%22%22%0Aif%20__name__%20%3D%3D%20%22__main__%22%3A%0A%20%20%20%20%23%20%E5%88%9D%E5%A7%8B%E5%8C%96%E6%A0%88%0A%20%20%20%20%23%20Python%20%E6%B2%A1%E6%9C%89%E5%86%85%E7%BD%AE%E7%9A%84%E6%A0%88%E7%B1%BB%EF%BC%8C%E5%8F%AF%E4%BB%A5%E6%8A%8A%20list%20%E5%BD%93%E4%BD%9C%E6%A0%88%E6%9D%A5%E4%BD%BF%E7%94%A8%0A%20%20%20%20stack%20%3D%20%5B%5D%0A%0A%20%20%20%20%23%20%E5%85%83%E7%B4%A0%E5%85%A5%E6%A0%88%0A%20%20%20%20stack.append%281%29%0A%20%20%20%20stack.append%283%29%0A%20%20%20%20stack.append%282%29%0A%20%20%20%20stack.append%285%29%0A%20%20%20%20stack.append%284%29%0A%20%20%20%20print%28%22%E6%A0%88%20stack%20%3D%22,%20stack%29%0A%0A%20%20%20%20%23%20%E8%AE%BF%E9%97%AE%E6%A0%88%E9%A1%B6%E5%85%83%E7%B4%A0%0A%20%20%20%20peek%20%3D%20stack%5B-1%5D%0A%20%20%20%20print%28%22%E6%A0%88%E9%A1%B6%E5%85%83%E7%B4%A0%20peek%20%3D%22,%20peek%29%0A%0A%20%20%20%20%23%20%E5%85%83%E7%B4%A0%E5%87%BA%E6%A0%88%0A%20%20%20%20pop%20%3D%20stack.pop%28%29%0A%20%20%20%20print%28%22%E5%87%BA%E6%A0%88%E5%85%83%E7%B4%A0%20pop%20%3D%22,%20pop%29%0A%20%20%20%20print%28%22%E5%87%BA%E6%A0%88%E5%90%8E%20stack%20%3D%22,%20stack%29%0A%0A%20%20%20%20%23%20%E8%8E%B7%E5%8F%96%E6%A0%88%E7%9A%84%E9%95%BF%E5%BA%A6%0A%20%20%20%20size%20%3D%20len%28stack%29%0A%20%20%20%20print%28%22%E6%A0%88%E7%9A%84%E9%95%BF%E5%BA%A6%20size%20%3D%22,%20size%29%0A%0A%20%20%20%20%23%20%E5%88%A4%E6%96%AD%E6%98%AF%E5%90%A6%E4%B8%BA%E7%A9%BA%0A%20%20%20%20is_empty%20%3D%20len%28stack%29%20%3D%3D%200%0A%20%20%20%20print%28%22%E6%A0%88%E6%98%AF%E5%90%A6%E4%B8%BA%E7%A9%BA%20%3D%22,%20is_empty%29&cumulative=false&curInstr=2&heapPrimitives=nevernest&mode=display&origin=opt-frontend.js&py=311&rawInputLstJSON=%5B%5D&textReferences=false

## 栈的实现

为了深入了解栈的运行机制，我们来尝试自己实现一个栈类。

栈遵循先入后出的原则，因此我们只能在栈顶添加或删除元素。然而，数组和链表都可以在任意位置添加和删除元素，**因此栈可以视为一种受限制的数组或链表**。换句话说，我们可以“屏蔽”数组或链表的部分无关操作，使其对外表现的逻辑符合栈的特性。

### 基于链表的实现

使用链表实现栈时，我们可以将链表的头节点视为栈顶，尾节点视为栈底。

如下图所示，对于入栈操作，我们只需将元素插入链表头部，这种节点插入方法被称为“头插法”。而对于出栈操作，只需将头节点从链表中删除即可。

=== "<1>"
    ![基于链表实现栈的入栈出栈操作](stack.assets/linkedlist_stack_step1.png)

=== "<2>"
    ![linkedlist_stack_push](stack.assets/linkedlist_stack_step2_push.png)

=== "<3>"
    ![linkedlist_stack_pop](stack.assets/linkedlist_stack_step3_pop.png)

以下是基于链表实现栈的示例代码：

```src
[file]{linkedlist_stack}-[class]{linked_list_stack}-[func]{}
```

### 基于数组的实现

使用数组实现栈时，我们可以将数组的尾部作为栈顶。如下图所示，入栈与出栈操作分别对应在数组尾部添加元素与删除元素，时间复杂度都为 $O(1)$ 。

=== "<1>"
    ![基于数组实现栈的入栈出栈操作](stack.assets/array_stack_step1.png)

=== "<2>"
    ![array_stack_push](stack.assets/array_stack_step2_push.png)

=== "<3>"
    ![array_stack_pop](stack.assets/array_stack_step3_pop.png)

由于入栈的元素可能会源源不断地增加，因此我们可以使用动态数组，这样就无须自行处理数组扩容问题。以下为示例代码：

```src
[file]{array_stack}-[class]{array_stack}-[func]{}
```

## 两种实现对比

**支持操作**

两种实现都支持栈定义中的各项操作。数组实现额外支持随机访问，但这已超出了栈的定义范畴，因此一般不会用到。

**时间效率**

在基于数组的实现中，入栈和出栈操作都在预先分配好的连续内存中进行，具有很好的缓存本地性，因此效率较高。然而，如果入栈时超出数组容量，会触发扩容机制，导致该次入栈操作的时间复杂度变为 $O(n)$ 。

在基于链表的实现中，链表的扩容非常灵活，不存在上述数组扩容时效率降低的问题。但是，入栈操作需要初始化节点对象并修改指针，因此效率相对较低。不过，如果入栈元素本身就是节点对象，那么可以省去初始化步骤，从而提高效率。

综上所述，当入栈与出栈操作的元素是基本数据类型时，例如 `int` 或 `double` ，我们可以得出以下结论。

- 基于数组实现的栈在触发扩容时效率会降低，但由于扩容是低频操作，因此平均效率更高。
- 基于链表实现的栈可以提供更加稳定的效率表现。

**空间效率**

在初始化列表时，系统会为列表分配“初始容量”，该容量可能超出实际需求；并且，扩容机制通常是按照特定倍率（例如 2 倍）进行扩容的，扩容后的容量也可能超出实际需求。因此，**基于数组实现的栈可能造成一定的空间浪费**。

然而，由于链表节点需要额外存储指针，**因此链表节点占用的空间相对较大**。

综上，我们不能简单地确定哪种实现更加节省内存，需要针对具体情况进行分析。

## 栈的典型应用

- **浏览器中的后退与前进、软件中的撤销与反撤销**。每当我们打开新的网页，浏览器就会对上一个网页执行入栈，这样我们就可以通过后退操作回到上一个网页。后退操作实际上是在执行出栈。如果要同时支持后退和前进，那么需要两个栈来配合实现。
- **程序内存管理**。每次调用函数时，系统都会在栈顶添加一个栈帧，用于记录函数的上下文信息。在递归函数中，向下递推阶段会不断执行入栈操作，而向上回溯阶段则会不断执行出栈操作。


## chapter_stack_and_queue / summary

# 小结

### 重点回顾

- 栈是一种遵循先入后出原则的数据结构，可通过数组或链表来实现。
- 在时间效率方面，栈的数组实现具有较高的平均效率，但在扩容过程中，单次入栈操作的时间复杂度会劣化至 $O(n)$ 。相比之下，栈的链表实现具有更为稳定的效率表现。
- 在空间效率方面，栈的数组实现可能导致一定程度的空间浪费。但需要注意的是，链表节点所占用的内存空间比数组元素更大。
- 队列是一种遵循先入先出原则的数据结构，同样可以通过数组或链表来实现。在时间效率和空间效率的对比上，队列的结论与前述栈的结论相似。
- 双向队列是一种具有更高自由度的队列，它允许在两端进行元素的添加和删除操作。

### Q & A

**Q**：浏览器的前进后退是否是双向链表实现？

浏览器的前进后退功能本质上是“栈”的体现。当用户访问一个新页面时，该页面会被添加到栈顶；当用户点击后退按钮时，该页面会从栈顶弹出。使用双向队列可以方便地实现一些额外操作，这个在“双向队列”章节有提到。

**Q**：在出栈后，是否需要释放出栈节点的内存？

如果后续仍需要使用弹出节点，则不需要释放内存。若之后不需要用到，`Java` 和 `Python` 等语言拥有自动垃圾回收机制，因此不需要手动释放内存；在 `C` 和 `C++` 中需要手动释放内存。

**Q**：双向队列像是两个栈拼接在了一起，它的用途是什么？

双向队列就像是栈和队列的组合或两个栈拼在了一起。它表现的是栈 + 队列的逻辑，因此可以实现栈与队列的所有应用，并且更加灵活。

**Q**：撤销（undo）和反撤销（redo）具体是如何实现的？

使用两个栈，栈 `A` 用于撤销，栈 `B` 用于反撤销。

1. 每当用户执行一个操作，将这个操作压入栈 `A` ，并清空栈 `B` 。
2. 当用户执行“撤销”时，从栈 `A` 中弹出最近的操作，并将其压入栈 `B` 。
3. 当用户执行“反撤销”时，从栈 `B` 中弹出最近的操作，并将其压入栈 `A` 。
