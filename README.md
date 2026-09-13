# Taffy Agent

一个迷你 Agent，人设是「永雏塔菲」。它不只是聊天——能联网搜资料、打开网页读原文，也能在沙箱里读写文件、编译运行代码，写完自己跑一遍验证，跑不通自己改。

算法与数据结构、计算机组成原理、嵌入式系统、单片机（STM32）、物联网、数字取证这些方向塔菲也懂：仓库里自带了一个本地知识库，问到就会先翻对应的教材 / 题解原文，再照着原文回答并标出处。

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
│   │   ├── forensics.py     # 数字取证：哈希 / 类型识别 / 字符串 / 雕复 / 元数据
│   │   ├── asm_sim.py       # asm_sim：小型 16 位 CPU 模拟器
│   │   ├── asm86.py         # asm86：8086/8088 实模式汇编仿真器
│   │   ├── mcu.py           # mcu_calc：单片机外设计算 + 校验
│   │   ├── logic.py         # logic_sim：数字逻辑仿真（门电路 / 真值表 / D 触发器）
│   │   ├── numconv.py       # number_convert：进制 / 补码 / IEEE754 / 位运算
│   │   ├── calc.py          # sci_calc：超高精度科学计算器
│   │   ├── text.py          # regex_test / diff_text / json_tool：正则 / 差异 / JSON
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
pip install openai requests python-dotenv pypdf python-docx jieba numpy \
            lxml charset-normalizer fastapi uvicorn
```

| 包 | 用途 |
|---|---|
| `openai` | 调模型 |
| `requests` | 联网搜索 / 打开链接 |
| `python-dotenv` | 读 `.env` |
| `pypdf` / `python-docx` | 知识库解析 PDF / DOCX |
| `jieba` | 中文分词 |
| `numpy` | 知识库的 BM25 打分（向量化的倒排索引） |
| `fastapi` / `uvicorn` | 网页版后端 |
| `lxml` | 网页正文抽取 |
| `charset-normalizer` | 网页编码猜测 |

另外可选装 `fonttools`（`pip install fonttools`）：让 `pypdf` 能解析 PDF 里嵌入的 CFF 字体编码。不装也能跑，只是碰到非常规编码的 PDF 可能抽出乱码，索引时会刷 `fontTools is required to…` 的警告。

想跑 C/C++ / Java / Node 还需要 `g++`、`javac`+`java`、`node`（不装的话其它语言照常）。

## 配置

在项目根目录建一个 `.env` 文件：

```
DEEPSEEK_API_KEY=sk-你的key
CXX=g++.exe路径
```

没有 key（或没建这个文件）时，程序启动会直接报错提醒，不会静默失败。

`CXX` 是可选的，只在 `run_code` 跑 `.cpp` / `.c` 时用到：填 g++ 的绝对路径就行，`.c` 会自动用同目录的 `gcc`。不填就按 PATH 里的 `g++` 找。**不用把它加进系统 PATH**——那样会影响全局，还要重启终端才生效，配在项目里更省事。

`SEARCH_PROXY` 也是可选的，控制 `web_search` 走不走代理，默认**直连**（百度这类国内引擎走代理反而容易被拒）。部署到别的机器上搜不出东西时，先看工具返回的提示，它会写明每家引擎是「连不上」还是「没抠到结果（页面 xx 字节）」：如果各家都连不上，说明是网络出不去，把这项设成 `system`（跟随系统 / 环境变量里的代理）或者直接填地址就行。

```
SEARCH_PROXY=system                      # 或者
SEARCH_PROXY=http://127.0.0.1:7897
```

`-static` 是默认带的，编译出来的临时可执行文件不依赖编译器目录下的 dll。

单次回复最多输出多少 token，在 `taffy/config.py` 里的 `MAX_TOKENS` 调，默认 **2048**。模型不设这个值时官方会一路放到 4096，压一下能省不少钱；2048 对日常问答和中等长度的代码都够，太长了塔菲会分几次写。想上 8K 得把 `BASE_URL` 换成 beta 接口。

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
| `open_url` | 打开 http/https 链接，跟完跳转后抽取网页正文 |
| `list_files` | 列出 workspace 里的目录 |
| `read_file` | 读文本文件 |
| `write_file` | 写文件，父目录自动创建 |
| `delete_file` | 删文件或目录（删目录要 `recursive=True`） |
| `run_code` | 编译运行代码，支持 `.py` / `.js` / `.java` / `.cpp` / `.c` |
| `send_sticker` | 发一张塔菲表情包（网页版渲染成图片） |
| `hash_file` | 算 MD5 / SHA1 / SHA256，可跟已知哈希比对 |
| `identify_file` | 按魔数判断真实类型（能揭穿改后缀伪装的），并算熵值 |
| `extract_strings` | 从二进制里提取 ASCII / UTF-16 / 中文字符串，带偏移量 |
| `carve_files` | 按文件头尾签名雕复出内嵌 / 被删的图片、PDF、压缩包 |
| `file_metadata` | MACB 时间线 + PDF / JPEG EXIF 元数据 |
| `asm_sim` | 在小型 16 位 CPU 上跑汇编，看寄存器 / 标志位 / 内存，可出逐步 trace |
| `asm86` | 8086 / 8088 实模式汇编仿真：跑 MASM 风格源码，看寄存器 / 标志位 / 内存 / 输出 / 总线周期 |
| `mcu_calc` | 单片机外设计算：波特率、定时器、ADC、分压、PWM、I2C 地址、CRC、RC |
| `logic_sim` | 数字逻辑仿真：门级网表算输出 / 列真值表，D 触发器按时钟跑周期 |
| `number_convert` | 进制互转、补码、IEEE754 位型、位运算置位 / 清位 / 测位 |
| `sci_calc` | 高精度科学计算器：表达式一次算到几十上百位有效数字 |
| `regex_test` | 正则调试：列出每处匹配的位置 / 内容 / 分组，可做替换 |
| `diff_text` | 两段文本 / 代码的 unified diff + 新增删除行数 |
| `json_tool` | JSON 缩进美化 / 压成一行 / 按路径取值 / 校验（错在哪行哪列） |

## 工程计算与教学仿真

这六个工具（`asm_sim` / `asm86` / `mcu_calc` / `logic_sim` / `number_convert` / `sci_calc`）都是纯标准库、纯算术，不联网、不起子进程，跨平台，专门覆盖塔菲会的那几个方向。

**`asm_sim`**——自带的 16 位 CPU。寄存器 `R0`~`R7`，标志位 `Z/N/C`，内存 256 个字（指令和数据共用），数值按 16 位回绕。指令集：

```
LI Rd,imm      MOV Rd,Rs       LOAD Rd,addr    STORE Rs,addr
ADD/SUB/MUL/AND/OR/XOR Rd,Ra,Rb
ADDI/SUBI Rd,Ra,imm            NOT Rd,Ra
SHL/SHR Rd,Ra,imm              INC/DEC Rd      CMP Ra,Rb
JMP/JZ/JNZ/JC/JNC/JGT/JLT 标签  HALT            NOP
DW 1,2,3       DS 4
```

一行一条，`;` / `#` 后面是注释，`loop:` 定义标签，数支持十进制和 `0x` / `0b` / `0o`。数据写在 `HALT` 后面，免得被当指令执行。`trace=true` 会给逐步执行过程（每步的寄存器变化）。

**`asm86`**——8086 / 8088 实模式汇编仿真器，跟上面那个自带 CPU 不是一回事：这个认的是真·x86 汇编。喂一段 MASM 风格的源码，它两遍汇编后直接跑，返回寄存器（`AX`~`DI`、`CS`/`DS`/`SS`/`ES`/`IP`/`SP`）、九个标志位（`CF`/`PF`/`AF`/`ZF`/`SF`/`OF`/`IF`/`DF`/`TF`）、有内容的和改过的内存、程序输出，以及**估算的总线周期**（说明这是估算值，不是精确机器码长度）。

- 认 MASM 常见写法：`SEGMENT`/`ENDS`、`ASSUME`、`PROC`/`ENDP`、`END 入口`、`DB`/`DW`/`DD`、`DUP`、`EQU`、`ORG`，段名还能用 `@DATA` 这么引；也支持完全不带段的裸程序，`.MODEL` / `.STACK` / `.DATA` / `.CODE` 会被忽略。
- 数字字面量认 `123` / `0FFH` / `1010B` / `0x1F` 这几种写法；指令覆盖 `MOV`/算术/逻辑/移位/乘除、`CMP`/`TEST` 和各种条件跳转、`LOOP`、`CALL`/`RET`、`PUSH`/`POP`、`CBW`/`CWD`/`XLAT`，以及 `MOVSB`/`CMPSB`/`SCASB` 这类字符串指令（带 `REP`/`REPE`/`REPNE`）。
- 寻址支持 `[BX+SI+4]`、`NUMS[BX+SI]`、`BYTE PTR`/`WORD PTR`、段超越前缀 `DS:`/`ES:`。
- 中断内置实现：`INT 21H`（`09H` 打印 `$` 结尾串、`02H` 打字符、`01H` 读键、`0AH` 读行、`4CH` 退出）和 `INT 10H` 的几个功能；没实现的中断会明确说没实现，不会瞎猜。
- `cpu` 选 `"8088"` 就按 8 位外部数据总线折算取指周期（`8086` 是 16 位总线），指令集两者完全一样。`stdin` 可以喂给 `01H` / `0AH`，`trace=true` 出逐步执行过程。

```asm
; 8086 Hello World（MASM 全框架写法）
.MODEL SMALL
.STACK 100H
DATA SEGMENT
    MSG DB 'Hello, Taffy!$'
DATA ENDS
CODE SEGMENT
    ASSUME CS:CODE, DS:@DATA
START:
    MOV AX, @DATA
    MOV DS, AX
    MOV AH, 09H
    LEA DX, MSG
    INT 21H
    MOV AX, 4C00H
    INT 21H
CODE ENDS
END START
```

**`logic_sim`**——门级网表，一行一个门：

```
A = INPUT
B = INPUT
n1 = AND A B
Y = XOR n1 B
```

门型 `AND` / `OR` / `NOT` / `NAND` / `NOR` / `XOR` / `XNOR` / `BUF` / `DFF`。不给 `inputs` 就列真值表（纯组合电路，最多 6 个输入）；给了 `inputs` 就按值算一遍。网表里有 `DFF` 就变成时序仿真，按时钟跑 `cycles` 个周期——`inputs` 可以给 `"0101"` 这样的序列来驱动，时钟端口叫 `CLK` 时在上升沿采样。

**`sci_calc`**——超高精度科学计算器。丢一个表达式进去，一次算到指定有效数字（默认 50 位，最多 1000 位），不用再为了让模型算个数而去 `write_file` + `run_code` 绕一圈。`decimal` 底子 + 自己实现的 π（Machin 公式）和三角函数级数，整数的加减乘幂走 Python 大整数，**一位不差**：

```
(1+2)**100 / sqrt(3)          2**100            factorial(50)
1/7                           pi                1e6*sqrt(2)
sin(pi/6)  cos(1.234)  tan(pi/4)  atan2(1,1)
ln(2)  log(1000,10)  lg(1000)  log2(1024)  exp(1)
comb(52,5)  perm(10,3)  gcd(1071,462)  isqrt(2**100)
```

`0.1 + 0.2` 在这里就是 `0.3`（数字字面量按原文读，不过二进制浮点那一手）；一次可以给多个式子，换行或分号隔开。结果太大（超过 1500 位）会直接拒绝，免得又慢又占地方。

展开看个例子：

```
你: 帮我算一下 72MHz 主频、115200 波特率的串口分频对不对，再跑个 1+2+...+10 的汇编，顺便 π 算到 50 位
[工具] mcu_calc({'op': 'uart', 'f_cpu': 72000000, 'baud': 115200})
     -> USARTDIV=39.0625，BRR=0x0271，实际 115384.6 bps，误差 +0.160%
[工具] asm_sim({'source': 'LI R1,0 ...', 'trace': True})
     -> R1=45，执行到 HALT，共 41 步
[工具] sci_calc({'expression': 'pi', 'precision': 50})
     -> 3.1415926535897932384626433832795028841971693993751
塔菲: 波特率误差 +0.16%，能放心用喵～汇编那边跑出来是 45，对的喵
```

## 文本与数据解析

**`regex_test`**——正则调试器。给正则和文本，列出每一处匹配的位置（偏移）、内容和各个分组（命名分组会标出组名）；再给 `replace` 就顺带做替换，支持 `\1` 和 `\g<name>` 反向引用。`flags` 可以传 `i` / `m` / `s` / `x` 的组合。

`re` 模块没法给匹配设超时，所以它先扫一遍正则，把 `(a+)+`、`(.*)*` 这种**嵌套量词**（灾难性回溯的典型形状）拦下来报错，免得一个写错的正则把整个服务卡死。正常的 `(a|b)+`、`(\d{4}-)+`、`(a+)?` 不会误伤。

**`diff_text`**——两段文本 / 代码的 unified diff，带「X 行 → Y 行；新增 N 行，删除 M 行」的统计，`context` 控制差异上下显示几行（默认 3）。

**`json_tool`**——`op=format` 缩进美化（默认，中文不转义成 `\uXXXX`）、`op=minify` 压成一行、`op=get` 按路径取值、`op=validate` 只校验。语法错会指到第几行第几列并画出那一行：

```
JSON 不合法：Expecting ':' delimiter（第 3 行第 7 列）
>   3 |   "b" 2
     |       ^
```

取值路径支持 `data.items[0].name`、`items[-1]`、`["名字"]` 这几种写法，走错了会分清是「键不存在（附上现有键名）」「下标越界（附上长度）」还是「这一层不是对象 / 数组」。

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

只认 http/https；开链接前会解析域名，指向**本机、内网、链路本地、运营商级 NAT** 的直接拒绝（服务跑在 `0.0.0.0`，不拦的话能被当成跳板去戳内网服务）。重定向**不交给 requests 自动跟**，而是自己一跳一跳走，每一跳都重新校验一次地址——否则一个公网页面 302 到 `127.0.0.1` 就绕过去了。下载上限 2MB、超时 20 秒、正文截断 6000 字。

「跳转」认三种：HTTP 的 `301/302/303/307/308`、页面里的 `<meta http-equiv="refresh">`、以及 JS 里的 `location.href = ...` / `location.replace()` / `location.assign()`（不少站点先给一个空白中转页，再用 JS 把人送到真地址）。最多跟 8 跳；跳回走过的地址就停下并说明是在哪几个地址之间来回跳，不会死循环（常见于要先登录、或先同意 Cookie 的中间页）。

判断用的是**一张明确的内网段清单**（`0.0.0.0/8`、`10/8`、`100.64/10`、`127/8`、`169.254/16`、`172.16/12`、`192.168/16`，以及 `::1`、`fc00::/7`、`fe80::/10`），外加组播，而不是 `ip.is_global` 一票否决。

> **别改回 `is_global`。** 手机上挂透明代理（Clash 之类）时 DNS 会被劫持成假 IP，Clash 默认就拿 `198.18.0.0/15` 当 fake-ip 池，于是**所有域名都解析到这个段**。而 `198.18.0.0/15` 在 Python 里既不算 global 也不算 reserved，用 `is_global` 会把每一条外链都判成内网，`open_url` 直接全废（手机上表现为「不管什么网址都说指向本机或内网」）。

### 边界（务必知道）

- **静态审查能被绕过**。C/C++/Java 是跑前扫源码，用宏拼装、函数指针、动态拼路径这类手法可以躲过去，它挡的是「模型手滑写出危险代码」，不是「有人处心积虑」。JS 有 Node 权限模型做真隔离，C/C++/Java 没有——**只在这台自己信任的机器上用，别对公网开放**。
- **网页版没有鉴权**。`/api/chat` 只认 `session_id`，谁拿到 id 谁就能往那个会话里灌消息；而塔菲手里有文件工具和代码执行。uuid4 猜不到，但 id 一旦泄露（截图、日志、共享链接）就等于会话被接管。要真正区分「每个人」得加登录。
- **搜索结果和网页正文是原样进上下文的**，理论上存在提示注入风险（网页里藏指令）。
- **上传的图片不落盘，但会发给 DeepSeek**。图片只在内存里过一趟（不写磁盘、不做 OCR），校验前缀必须是 `data:image/`、长度不超过 8MB；这一轮跑完就从对话历史里换成一句文字说明。但图片内容本身要传给 `api.deepseek.com`，敏感截图别发。
- `_sessions` 是进程内字典，**没有持久化和过期淘汰**，重启就清空，长时间跑会一直涨。

## 知识库

把文档丢进项目根目录的 `knowledge/`（子目录也认），Agent 就能查到。

仓库里已经带了一份知识库（约 117MB），也可以自己再往里加：

| 目录 | 内容 |
|---|---|
| `books/` | 教材 PDF / Markdown：算法（[Algorithms-JeffE](file:///f:/新建文件夹/Taffy-Agent/knowledge/books/Algorithms-JeffE.pdf)、[CPH](file:///f:/新建文件夹/Taffy-Agent/knowledge/books/CompetitiveProgrammersHandbook.pdf)）、数据结构（[OpenDataStructures C++/Python](file:///f:/新建文件夹/Taffy-Agent/knowledge/books/OpenDataStructures-cpp.pdf)）、[计算机组成原理](file:///f:/新建文件夹/Taffy-Agent/knowledge/books/ComputerOrganization-Tarnoff.pdf)、[嵌入式系统](file:///f:/新建文件夹/Taffy-Agent/knowledge/books/EmbeddedSystems-LeeSeshia.pdf)、[物联网](file:///f:/新建文件夹/Taffy-Agent/knowledge/books/IoT-EnablingThingsToTalk.pdf)、[STM32 单片机](file:///f:/新建文件夹/Taffy-Agent/knowledge/books/Microcontrollers-STM32F103.md) |
| `books/` 数字取证 | [数字取证教材（UOU）](file:///f:/新建文件夹/Taffy-Agent/knowledge/books/DigitalForensics-UOU.pdf)、[NIST SP 800-86 取证技术融入应急响应](file:///f:/新建文件夹/Taffy-Agent/knowledge/books/NIST-SP800-86-ForensicTechniques.pdf)、[NIST SP 800-101r1 移动设备取证](file:///f:/新建文件夹/Taffy-Agent/knowledge/books/NIST-SP800-101r1-MobileDeviceForensics.pdf)、[NIJ 数字证据检验指南](file:///f:/新建文件夹/Taffy-Agent/knowledge/books/NIJ-ForensicExaminationOfDigitalEvidence.pdf)、论文：[DFRWS 内存取证（Go 恶意样本）](file:///f:/新建文件夹/Taffy-Agent/knowledge/books/DFRWS2026-MemoryForensics-GoMalware.pdf)、[DFRWS Deepfake 取证](file:///f:/新建文件夹/Taffy-Agent/knowledge/books/DFRWS2026-DeepfakePolicing.pdf) |
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
| `books/DigitalForensics-UOU.pdf` | Jeetendra Pande、Ajay Prasad，Uttarakhand Open University 2016 | CC BY-SA 4.0 |
| `books/NIST-SP800-86-ForensicTechniques.pdf` | NIST（美国国家标准与技术研究院） | 美国政府作品，公有领域 |
| `books/NIST-SP800-101r1-MobileDeviceForensics.pdf` | NIST | 美国政府作品，公有领域 |
| `books/NIJ-ForensicExaminationOfDigitalEvidence.pdf` | 美国司法部 NIJ（NCJ 199408） | 美国政府作品，公有领域 |
| `books/DFRWS2026-MemoryForensics-GoMalware.pdf` | DFRWS USA 2026，Hala Ali / Andrew Case / Irfan Ahmed | 文件为 Elsevier 投稿预印本，内部未声明许可；DFRWS 官网公开提供 |
| `books/DFRWS2026-DeepfakePolicing.pdf` | DFRWS EU 2026，Áine MacDermott | CC BY-NC-ND（Elsevier 开放获取） |
| `hello-algo/` | 靳宇栋（krahets）《Hello 算法》 | CC BY-NC-SA 4.0 |
| `leetcode/` | doocs/leetcode 社区 | CC BY-SA 4.0；题目本身归 LeetCode |
| `oi-wiki/` | OI Wiki 社区 | CC BY-SA 4.0（个别页面另有署名） |
| `luogu/` | 洛谷（luogu.com.cn）题解 | 版权归洛谷及原题解作者 |

注意几点：

- 上表是**各项资料自身的授权**，不是本项目的授权。带 **NC** 的都禁止商用，所以整仓库不能当商用素材用；带 **SA / ND** 的还有「相同方式共享」「禁止演绎」的约束。
- `ComputerOrganization-Tarnoff.pdf` 书内版权页写的是 All rights reserved，是这里面限制最严的一本，随仓库公开只为方便个人学习检索，请不要再分发。
- 权利人若认为收录不妥，提 Issue 或联系仓库作者，会立刻移除。

## 人设提示词

在 [config.py](file:///f:/新建文件夹/Taffy-Agent/taffy/config.py) 的 `SYSTEM_PROMPT`，一共 25 条。除了说话风格，几条硬规矩是：

- 代码必须完整写进回答里（workspace 只是缓存，不是交付物），跑通后删掉临时文件；
- 需求落在她会的那几个方向（含写代码 / 调试 / 排错 / 选型）时，先 `search_knowledge` 查知识库里有没有现成的方案、题解、模板、教材写法，有就参考着来并标出处，实在沾不上边才从零想；
- 发题解前必须自己跑测试用例验证；
- 跑代码前自审安全性，代码只准碰 workspace；
- 数学式子不许写 LaTeX 源码，用 × ÷ ≤ √ π 这种一眼能读的写法；
- 情绪优先用表情包图片，别堆 emoji 和颜文字；
- 拿到链接用 `open_url` 读原文再回答，打不开就直说，不许瞎编；
- 除了算法题，嵌入式 / 单片机 / 物联网 / 计算机组成原理 / 数字取证也答，这几个方向先查知识库教材原文再回（取证那几本是英文的，提示里让它用英文关键词检索）；
- 数字取证有专门工具：先 `identify_file` 看是什么、`hash_file` 固定哈希，再按需 `extract_strings` / `carve_files` / `file_metadata` 深挖，结论要带上偏移量 / 哈希 / 时间戳；分析完不许删雏草姬放进来的样本；
- 工程计算和教学仿真别硬算，该用 `asm_sim` / `asm86` / `mcu_calc` / `logic_sim` / `number_convert` 就用（寄存器怎么配、位型长什么样、电路输出是几、汇编跑出来什么，都直接算给雏草姬看；8086 / 8088 汇编用 `asm86` 实跑）；
- 纯数学运算别硬算、也别为算个数去 `write_file` + `run_code` 绕一圈，直接交给 `sci_calc`（默认 50 位有效数字，最多 1000 位，整数是精确大数）；
- 正则 / 差异 / JSON 这类文本活儿也别专门写代码，用 `regex_test` / `diff_text` / `json_tool`（写正则、抠日志、比配置、取值、校验都用它们；`regex_test` 会拦嵌套量词防回溯卡死）；
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
- `web_search` 是抓搜索结果页来解析的，**没有官方 API**。它按 百度 → 必应 → 360 → DuckDuckGo 的顺序试，一家抠不到就换下一家，所以单家被风控或者换模板不会整个失效；但全都没结果的情况依旧可能发生。失败时会带上每家的原因（连不上 / 没抠到结果 + 页面字节数），照着就能判断是网络出不去还是被挡下来了。中文查询优先走百度：必应碰上中文长句会把查询拆散（「数字取证 内存取证 volatility」这种复合词，它退化成只搜「数字」，返回一堆无关结果），而 360 现在会甩验证页、DuckDuckGo 在境内直连不通。
- `open_url` 的正文抽取是「挑 `<p>` 总字数最多的容器」这种启发式，不是 Readability，遇到结构奇怪的页面可能抓不准。
- 纯前端渲染（正文完全由 JS 拉接口后再画上去）、要登录、或者有强反爬的站点，`open_url` 还是抓不到正文：它不跑 JS，只能顺带从内嵌 JSON（`__NEXT_DATA__` / `ld+json` / `__NUXT__` 之类）里捞一份，捞不到就只能如实说「抓不到」，不会瞎编。
- 对话历史只存在内存里，退出就清空，没有持久化，也没有超长上下文的裁剪。

## 参考

模型名 `deepseek-v4-flash`、接口地址 `https://api.deepseek.com/v1`，都在 `taffy/config.py` 里，换模型改那里就行。
