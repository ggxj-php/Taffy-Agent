# Taffy Agent

一个迷你 Agent，人设是「永雏塔菲」。它不只是聊天——能联网搜资料、打开网页读原文，也能在沙箱里读写文件、编译运行代码，写完自己跑一遍验证，跑不通自己改。

算法与数据结构、计算机组成原理、嵌入式系统、单片机（STM32）、物联网这些方向塔菲也懂：仓库里自带了一个本地知识库，问到就会先翻对应的教材 / 题解原文，再照着原文回答并标出处。

两种用法：**终端**里直接对话，或者起一个**网页版**（手机也能用，聊天记录流式输出、思考过程和工具调用可折叠、代码高亮、还会发塔菲表情包）。

## 目录结构

```
Taffy-Agent/
├── agent.py                 # 终端入口：python agent.py
├── .env                     # 密钥（已 gitignore，不进仓库）
├── taffy/
│   ├── config.py            # 模型、运行参数、人设提示词
│   ├── sandbox.py           # 工作区沙箱：路径越界检查
│   ├── llm.py               # 模型接入层
│   ├── core.py              # TaffyAgent：对话历史 + 工具循环
│   ├── kb/                  # 知识库：文档解析 + BM25 检索
│   │   ├── loader.py        # pdf / docx / html / txt 抽正文
│   │   └── index.py         # 切块、分词、建索引、磁盘缓存
│   ├── tools/
│   │   ├── __init__.py      # 工具注册表（schema 汇总 + 派发）
│   │   ├── basics.py        # get_time
│   │   ├── search.py        # web_search / open_url
│   │   ├── kb.py            # search_knowledge
│   │   ├── files.py         # list_files / read_file / write_file / delete_file
│   │   ├── runner.py        # run_code
│   │   ├── sticker.py       # send_sticker
│   │   ├── _pyguard.py      # Python 运行时审计钩子（子进程里跑）
│   │   └── _codescan.py     # C/C++/Java/JS 跑前静态审查
│   └── web/                 # 网页版
│       ├── app.py           # FastAPI 后端，SSE 推事件流
│       ├── __main__.py      # python -m taffy.web
│       └── static/          # 前端：index.html / app.js / style.css
│           ├── stickers/    # 22 张塔菲表情包
│           └── vendor/      # marked / highlight.js / DOMPurify
├── knowledge/               # 知识库原始文档，Agent 只读（已随仓库提供）
├── .cache/                  # 知识库索引缓存，可随时删掉重建
└── workspace/               # 沙箱根目录，Agent 只能在这里动文件
```

## 环境要求

- Python 3.10+
- 依赖：

```bash
pip install openai requests python-dotenv pypdf python-docx jieba rank_bm25 \
            fastapi uvicorn lxml charset-normalizer
```

| 包 | 用途 |
|---|---|
| `openai` | 调模型 |
| `requests` | 联网搜索 / 打开链接 |
| `python-dotenv` | 读 `.env` |
| `pypdf` / `python-docx` | 知识库解析 PDF / DOCX |
| `jieba` / `rank_bm25` | 中文分词 + BM25 检索 |
| `fastapi` / `uvicorn` | 网页版后端 |
| `lxml` | 网页正文抽取 |
| `charset-normalizer` | 网页编码猜测 |

想跑 C/C++ / Java / Node 还需要 `g++`、`javac`+`java`、`node`（不装的话其它语言照常）。

## 配置

在项目根目录建一个 `.env` 文件：

```
DEEPSEEK_API_KEY=sk-你的key
CXX=g++.exe路径
```

没有 key（或没建这个文件）时，程序启动会直接报错提醒，不会静默失败。

`CXX` 是可选的，只在 `run_code` 跑 `.cpp` / `.c` 时用到：填 g++ 的绝对路径就行，`.c` 会自动用同目录的 `gcc`。不填就按 PATH 里的 `g++` 找。**不用把它加进系统 PATH**——那样会影响全局，还要重启终端才生效，配在项目里更省事。

`-static` 是默认带的，编译出来的临时可执行文件不依赖编译器目录下的 dll。

## 运行

### 终端版

```bash
python agent.py
```

然后直接说话就行。输入 `exit` / `quit` / `退出` / `拜拜` 或者按 `Ctrl+C` 结束。

```
你: 帮我写个脚本算 1 到 100 里的素数，跑一遍确认
[工具] write_file({'path': 'primes.py', ...}) -> 已写入 primes.py（...）
[工具] run_code({'path': 'primes.py'}) -> 退出码 0
2 3 5 ...
塔菲: 跑通啦喵～一共 25 个喵
```

### 网页版

```bash
python -m taffy.web
```

监听 `0.0.0.0:8000`，本机开 http://127.0.0.1:8000 就行；手机连同一个 wifi，访问 `http://<电脑局域网IP>:8000` 也能用。

前端特性：

- **流式输出**：正文一个字一个字往外冒，思考过程和工具调用分成可折叠的卡片，默认只显示一行标题，点开才展开。
- **会话隔离**：会话 id 存在 `sessionStorage` 里，**按标签页隔离**——开两个标签页就是两个独立会话，互不干扰；同一标签页刷新仍保留，关掉标签页才算结束。右上角「新会话」换一个 id 重开。
- **代码高亮**：markdown 渲染走 `marked` + `highlight.js`，渲染前用 `DOMPurify` 过一遍防 XSS，代码块带一键复制。
- **表情包**：塔菲按情绪发真·图片表情包（22 张），不是 emoji 或颜文字。
- **发图片**：点输入框左边的图片按钮选图，先出缩略图、可叉掉。图片在浏览器里读成 base64 随请求上传，**服务端不落盘**；塔菲看完整轮就把图片数据从对话历史里抹掉，后续轮次不会再带、也不会重复上传。
- **回到最底部**：往上翻的时候右下角才浮出一个按钮，点了才回到底部。**不做自动吸底**——内容增长时视图不动，不会被新内容顶回去。
- **输入框**：回车是换行，不会误发；发送点「发送」按钮。

> 改了 `.py`（含 `config.py` 提示词）要重启服务；改 `static/` 下的前端文件刷新页面即可。

## 内置工具

| 工具 | 作用 |
|---|---|
| `get_time` | 当前时间 |
| `search_knowledge` | 检索本地知识库 `knowledge/`，返回原文片段 |
| `web_search` | 联网搜索，返回标题 / 链接 / 摘要 |
| `open_url` | 打开 http/https 链接，抽取网页正文 |
| `list_files` | 列出 workspace 里的目录 |
| `read_file` | 读文本文件 |
| `write_file` | 写文件，父目录自动创建 |
| `delete_file` | 删文件或目录（删目录要 `recursive=True`） |
| `run_code` | 编译运行代码，支持 `.py` / `.js` / `.java` / `.cpp` / `.c` |
| `send_sticker` | 发一张塔菲表情包（网页版渲染成图片） |

## 安全护栏

分三层，从外到内：

### 1. 文件工具：路径硬隔离

所有文件操作都被 `safe_path()` 限制在 `workspace/` 内，`../`、绝对路径、指向外部的符号链接都直接拒绝。

### 2. `run_code`：不经过 shell

只接受**文件名**，解释器和编译命令由扩展名查表决定，全程 `subprocess` 传列表、不经 shell，所以模型拼不出 `rm -rf` 这类命令。带超时（默认 20 秒，上限 60 秒，超时用 `taskkill /T` 杀整个进程树）和输出截断（4000 字符）。

但这只拦住「命令注入」，拦不住「代码本身干坏事」——所以又加了两道：

| 语言 | 机制 | 拦什么 |
|---|---|---|
| `.py` | [_pyguard.py](file:///f:/新建文件夹/Taffy-Agent/taffy/tools/_pyguard.py) 审计钩子（`sys.addaudithook`） | 读写 workspace 外的文件、联网、起进程、`ctypes` 后门；钩子装了就摘不掉 |
| `.js` | Node 权限模型 `--permission --allow-fs-read/write=<workspace>` | 文件读写锁死在 workspace；不给 `--allow-child-process` / `--allow-worker` / `--allow-addons`，这些就用不了 |
| `.c` / `.cpp` / `.java` | [_codescan.py](file:///f:/新建文件夹/Taffy-Agent/taffy/tools/_codescan.py) 跑前静态审查 | 危险头文件（`windows.h` 等）、危险调用（`system`、`Runtime.exec`、`require('net')`…）、绝对路径和 `..` 路径字符串 |

另外**子进程环境变量会被过滤**：名字里含 `KEY` / `TOKEN` / `SECRET` / `PASSWORD` / `AUTH` 的一律抹掉，免得生成的代码把 `.env` 里的 API Key 读出来打印到回话里。

### 3. `open_url`：防 SSRF

只认 http/https；开链接前会解析域名，指向**本机、内网、保留地址**的直接拒绝（服务跑在 `0.0.0.0`，不拦的话能被当成跳板去戳内网服务）。重定向**不交给 requests 自动跟**，而是自己一跳一跳走，每一跳都重新校验一次地址——否则一个公网页面 302 到 `127.0.0.1` 就绕过去了。下载上限 2MB、超时 20 秒、正文截断 6000 字。

判断用的不是「是不是私网」而是「**是不是全球可达**」（`ip.is_global`），顺带把 CGNAT（`100.64.0.0/10`）这类非公网段也挡掉。

### 边界（务必知道）

- **静态审查能被绕过**。C/C++/Java 是跑前扫源码，用宏拼装、函数指针、动态拼路径这类手法可以躲过去，它挡的是「模型手滑写出危险代码」，不是「有人处心积虑」。JS 有 Node 权限模型做真隔离，C/C++/Java 没有——**只在这台自己信任的机器上用，别对公网开放**。
- **网页版没有鉴权**。`/api/chat` 只认 `session_id`，谁拿到 id 谁就能往那个会话里灌消息；而塔菲手里有文件工具和代码执行。uuid4 猜不到，但 id 一旦泄露（截图、日志、共享链接）就等于会话被接管。要真正区分「每个人」得加登录。
- **搜索结果和网页正文是原样进上下文的**，理论上存在提示注入风险（网页里藏指令）。
- **上传的图片不落盘，但会发给 DeepSeek**。图片只在内存里过一趟（不写磁盘、不做 OCR），校验前缀必须是 `data:image/`、长度不超过 8MB；这一轮跑完就从对话历史里换成一句文字说明。但图片内容本身要传给 `api.deepseek.com`，敏感截图别发。
- `_sessions` 是进程内字典，**没有持久化和过期淘汰**，重启就清空，长时间跑会一直涨。

## 知识库

把文档丢进项目根目录的 `knowledge/`（子目录也认），Agent 就能查到。

仓库里已经带了一份知识库（约 105MB），也可以自己再往里加：

| 目录 | 内容 |
|---|---|
| `books/` | 教材 PDF / Markdown：算法（[Algorithms-JeffE](file:///f:/新建文件夹/Taffy-Agent/knowledge/books/Algorithms-JeffE.pdf)、[CPH](file:///f:/新建文件夹/Taffy-Agent/knowledge/books/CompetitiveProgrammersHandbook.pdf)）、数据结构（[OpenDataStructures C++/Python](file:///f:/新建文件夹/Taffy-Agent/knowledge/books/OpenDataStructures-cpp.pdf)）、[计算机组成原理](file:///f:/新建文件夹/Taffy-Agent/knowledge/books/ComputerOrganization-Tarnoff.pdf)、[嵌入式系统](file:///f:/新建文件夹/Taffy-Agent/knowledge/books/EmbeddedSystems-LeeSeshia.pdf)、[物联网](file:///f:/新建文件夹/Taffy-Agent/knowledge/books/IoT-EnablingThingsToTalk.pdf)、[STM32 单片机](file:///f:/新建文件夹/Taffy-Agent/knowledge/books/Microcontrollers-STM32F103.md) |
| `hello-algo/` | 《Hello 算法》中文教程分章 Markdown |
| `leetcode/` | LeetCode 题解（按题号分段） |
| `oi-wiki/` | OI Wiki 各专题 |
| `luogu/` | 洛谷题解 |

`books/` 下的英文教材篇幅大但命中质量低，检索得分统一乘 0.5 降权（见 `KB_SOURCE_WEIGHTS`），避免把中文语料挤下去。

支持的格式：

| 格式 | 说明 |
|---|---|
| `.pdf` | 按页抽取，回答里会标页码 |
| `.docx` | 段落 + 表格（`.doc` 这种老格式不支持） |
| `.html` / `.htm` | 剥掉标签只留正文，`script` / `style` 忽略 |
| `.md` / `.markdown` / `.txt` / `.log` | 直接读，编码按 utf-8 → gbk 回退 |

**工作原理**：文档先解析成纯文本，按段落切成约 500 字的块（相邻块重叠 80 字，避免答案正好被切在边界），中文用 `jieba` 分词，然后建 BM25 索引。检索时返回最相关的几段原文，模型基于原文回答。

**缓存**：解析结果按文件存到 `.cache/kb_index.pkl`，比对修改时间和大小。文件没变就直接复用，只有新增 / 改动的文件才重新解析，所以启动不会每次都啃一遍 PDF。想强制重建就删掉 `.cache/`。

**注意两点**：

- 索引在**第一次检索时**建立，往 `knowledge/` 加了新文档要**重启** Agent 才会生效（进程内缓存）。
- 如果某个文件解析失败（比如加密 PDF），会跳过它继续索引其它文件，不会整个挂掉。

**换成向量检索**：BM25 是关键词匹配，问法和原文用词差太远就搜不到。将来想升级，只需要改 [index.py](file:///f:/新建文件夹/Taffy-Agent/taffy/kb/index.py) 的 `KnowledgeBase.build()` / `search()` 两个方法，工具层和提示词都不用动。

## 版权声明

**本项目的代码**（`taffy/`、`agent.py` 等）版权归仓库作者所有，未附开源许可证。

**`knowledge/` 下的文档全部是第三方作品**，版权归各自的作者 / 出版社 / 社区所有，不属于本项目，本项目也不对其主张任何权利。收录目的仅为本地检索与个人学习，能不能再分发、能不能商用，一律以原出处和自己的授权为准。

| 资料 | 作者 / 来源 | 授权（据文件内声明或上游仓库） |
|---|---|---|
| `books/Algorithms-JeffE.pdf` | Jeff Erickson | CC BY 4.0 |
| `books/CompetitiveProgrammersHandbook.pdf` | Antti Laaksonen（2018-07-03 草稿版，CSES 免费书） | CC BY-NC-SA |
| `books/OpenDataStructures-*.pdf` | Pat Morin | 书正文版权归作者 / 出版社；配套源码为 CC BY |
| `books/ComputerOrganization-Tarnoff.pdf` | David L. Tarnoff | **保留所有权利**（All rights reserved） |
| `books/EmbeddedSystems-LeeSeshia.pdf` | Lee & Seshia | CC BY-NC-ND 4.0 |
| `books/IoT-EnablingThingsToTalk.pdf` | Springer，2013 开放获取 | CC BY-NC |
| `books/Microcontrollers-STM32F103.md` | 野火电子（EmbedFire）官方教程整理 | 版权归野火电子 |
| `hello-algo/` | 靳宇栋（krahets）《Hello 算法》 | CC BY-NC-SA 4.0 |
| `leetcode/` | doocs/leetcode 社区 | CC BY-SA 4.0；题目本身归 LeetCode |
| `oi-wiki/` | OI Wiki 社区 | CC BY-SA 4.0（个别页面另有署名） |
| `luogu/` | 洛谷（luogu.com.cn）题解 | 版权归洛谷及原题解作者 |

注意几点：

- 上表是**各项资料自身的授权**，不是本项目的授权。带 **NC** 的都禁止商用，所以整仓库不能当商用素材用；带 **SA / ND** 的还有「相同方式共享」「禁止演绎」的约束。
- `ComputerOrganization-Tarnoff.pdf` 书内版权页写的是 All rights reserved，是这里面限制最严的一本，随仓库公开只为方便个人学习检索，请不要再分发。
- 权利人若认为收录不妥，提 Issue 或联系仓库作者，会立刻移除。

## 人设提示词

在 [config.py](file:///f:/新建文件夹/Taffy-Agent/taffy/config.py) 的 `SYSTEM_PROMPT`，一共 19 条。除了说话风格，几条硬规矩是：

- 代码必须完整写进回答里（workspace 只是缓存，不是交付物），跑通后删掉临时文件；
- 发题解前必须自己跑测试用例验证；
- 跑代码前自审安全性，代码只准碰 workspace；
- 数学式子不许写 LaTeX 源码，用 × ÷ ≤ √ π 这种一眼能读的写法；
- 情绪优先用表情包图片，别堆 emoji 和颜文字；
- 拿到链接用 `open_url` 读原文再回答，打不开就直说，不许瞎编；
- 除了算法题，嵌入式 / 单片机 / 物联网 / 计算机组成原理也答，这几个方向先查知识库教材原文再回；
- 能看图：雏草姬发的图片当轮有效、看完即清，图里的信息要当轮抄进回答，下一轮不许假装还记得。

## 新增一个工具

1. 在 `taffy/tools/` 下新建模块，写一个 `SPECS` 列表（OpenAI function calling 的 schema）和同名函数：

```python
SPECS = [
    {
        "type": "function",
        "function": {
            "name": "say_hi",
            "description": "打个招呼",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "对方名字"}
                },
                "required": ["name"],
            },
        },
    },
]


def say_hi(name: str) -> str:
    return f"你好 {name} 喵"
```

2. 把它加进 `taffy/tools/__init__.py` 的 `_MODULES`。

注册表按约定工作：**schema 里的 `name` 要和函数名一致**，它会自动把函数挂到 `TOOL_MAP` 上。

## 已知限制

- **C/C++ 编译器很老**：本机用 `CXX` 指的 TDM-GCC 4.9.2（2014 年），只支持到 **C++11**。`std::filesystem`、结构化绑定、`auto` 简写这些 C++14/17 的东西编译不过，所以工具描述里专门提醒了模型别用。换个新一点的 MinGW 把 `CXX` 指过去就能解决。
- **静态审查会误伤**：黑名单写死了，塔菲用了没预料到的库可能被拦下（报错里会说明命中了哪一段）。`std::remove`、字符串里出现 `"system("` 这类已做处理，不会误判。
- `web_search` 用的是 360 搜索的网页解析，**没有官方 API**，页面结构变了就可能失效。而且它走直连、绕开系统代理，换了网络环境可能需要调整。
- `open_url` 的正文抽取是「挑 `<p>` 总字数最多的容器」这种启发式，不是 Readability，遇到结构奇怪的页面可能抓不准。
- 对话历史只存在内存里，退出就清空，没有持久化，也没有超长上下文的裁剪。

## 参考

模型名 `deepseek-v4-flash`、接口地址 `https://api.deepseek.com/v1`，都在 `taffy/config.py` 里，换模型改那里就行。
