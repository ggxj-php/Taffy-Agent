

## intro/about.md

## 关于本项目

**OI Wiki** 致力于成为一个免费开放且持续更新的 **编程竞赛 (competitive programming)** 知识整合站点．

## 交流方式

本项目主要使用 [Issues](https://github.com/OI-wiki/OI-wiki/issues)/[QQ](https://jq.qq.com/?_wv=1027&k=5EfkM6K)/[Telegram](https://t.me/OI_wiki) 进行交流沟通．

Telegram 群组链接为 [@OI\_wiki](https://t.me/OI_wiki)，QQ 群号码为 [588793226](https://jq.qq.com/?_wv=1027&k=5EfkM6K)，欢迎加入．

???+ note "Note"
    原则上来说，上述群组是 **OI Wiki 讨论群**，所以请尽量不要在群组中发表过多与 **OI Wiki** 无关的内容．

## 项目方针

-   [OI Wiki 不是什么](./what-oi-wiki-is-not.md)


## intro/docker-deploy.md

本页面将介绍使用 Docker 部署 **OI Wiki** 环境的方式．

???+ warning "Warning"
    以下步骤须在 root 用户下或 docker 组用户下执行．

## 拉取 **OI Wiki** 镜像

```bash
# 以下命令在主机中运行其中一个即可
# Docker Hub 镜像（官方镜像仓库）
docker pull 24oi/oi-wiki
# DaoCloud Hub 镜像（国内镜像仓库）
docker pull daocloud.io/sirius/oi-wiki
# Tencent Hub 镜像（国内镜像仓库）
docker pull ccr.ccs.tencentyun.com/oi-wiki/oi-wiki
```

## 自行构建镜像

```bash
# 以下命令在主机中运行
# 克隆 Git 仓库
git clone https://github.com/OI-wiki/OI-wiki.git
cd OI-wiki/
# 构建镜像
docker build -t [name][:tag] . --build-arg [variable1]=[value1] [variable2]=[value2]...
```

-   （必须）设置 `[name]` 以设置镜像名，（可选）设置 `[tag]` 以设置镜像标签（若设置，则运行时镜像名由两部分构成）．
-   可以通过 `--build-arg` 参数设置环境变量．

可以使用的环境变量：

-   可以设置 `WIKI_REPO` 来使用 Wiki 仓库的镜像站点（当未设置时自动使用 GitHub）
-   可以设置 `PYPI_MIRROR` 来使用 PyPI 仓库的镜像站点（当未设置时自动使用官方 PyPI）
    -   在国内建议使用 TUNA 镜像站 `https://pypi.tuna.tsinghua.edu.cn/simple/`
-   可以设置 `LISTEN_IP` 来更改监听 IP（当未设置时为 `0.0.0.0`，即监听所有 IP 的访问）
-   可以设置 `LISTEN_PORT` 来更改监听端口（当未设置时为 `8000`）

示例：

```bash
docker build -t OI_Wiki . --build-arg WIKI_REPO=https://hub.fastgit.xyz/OI-wiki/OI-wiki.git PYPI_MIRROR=https://pypi.tuna.tsinghua.edu.cn/simple/
# 构建一个名为 OI_Wiki （标签默认）的镜像，使用 FastGit 服务加速克隆，使用 TUNA 镜像站．
```

## 运行容器

```bash
# 以下命令在主机中运行
docker run -d -it [image]
```

-   （必须）设置 `[image]` 以设置镜像．例如，从 Docker Hub 拉取的为 `24oi/oi-wiki`；DaoCloud Hub 拉取的则为 `daocloud.io/sirius/oi-wiki`．
-   （必须）设置 `-p [port]:8000` 以映射容器端口至主机端口（不写该语句则默认为不暴露端口．设置时请替换 `[port]` 为主机端口）．设置后可以在主机使用 `http://127.0.0.1:[port]` 访问 **OI Wiki**．
-   设置 `--name [name]` 以设置容器名字．（默认空．设置时请替换 `[name]` 为自定义的容器名字．若想查看容器 id，则输入 `docker ps`）

## 使用容器

???+ note "Note"
    示例基于 Ubuntu latest 部署．

进入容器：

```bash
# 以下命令在主机中运行
docker exec -it [name] /bin/bash
```

若在上述运行容器中去掉 `-d`，则可以直接进入容器 bash，退出后容器停止，加上 `-d` 则后台运行，请手动停止．上述进入容器针对加上 `-d` 的方法运行．

特殊用法：

```bash
# 以下命令在容器中运行
# 更新 git 仓库
wiki-upd

# 使用我们的自定义主题
wiki-theme

# 构建 mkdocs ，会在 site 文件夹下得到静态页面
wiki-bld

# 构建 mkdocs 并渲染 MathJax ，会在 site 文件夹下得到静态页面
wiki-bld-math

# 运行一个服务器，访问容器中 http://127.0.0.1:8000 或访问主机中 http://127.0.0.1:[port] 可以查看效果
wiki-svr

# 修正 Markdown
wiki-o
```

退出容器：

```bash
# 以下命令在容器中运行
# 退出
exit
```

## 停止容器

```bash
# 以下命令在主机中运行
docker stop [name]
```

## 启动容器

```bash
# 以下命令在主机中运行
docker start [name]
```

## 重启容器

```bash
# 以下命令在主机中运行
docker restart [name]
```

## 删除容器

```bash
# 以下命令在主机中运行
# 删除前请先停止容器
docker rm [name]
```

## 更新镜像

重新再 `pull` 一次即可，通常不会更新．

## 删除镜像

```bash
# 以下命令在主机中运行
# 删除前请先删除使用 oi-wiki 镜像构建的容器
docker rmi [image]
```

## 疑问

如果您有疑问，欢迎提出 [issue](https://github.com/OI-wiki/OI-wiki/issues/new/choose)！


## intro/faq.md

本页面主要解答一些常见的问题．

## 我想问点与这个 Wiki 相关的问题

Q：你们是为什么想要做这个 Wiki 的呢？

A：不知道你在学 **OI** 的时候，面对庞大的知识体系，有没有感到过迷茫无助的时候？**OI Wiki** 想要做的事情可能类似于「让更多竞赛资源不充裕的同学能方便地接触到训练资源」．当然这么表述也不完全，做 Wiki 的动机可能也很纯粹，只是简单地想要对 **OI** 的发展做出一点点微小的贡献吧．XD

***

Q：我很感兴趣，怎么参与？

A：**OI Wiki** 现在托管在 GitHub 上，你可以直接访问这个 [repo](https://github.com/OI-wiki/OI-wiki) 来查看最新进展．参与的途径包括在 GitHub 上面开 [Issue](https://github.com/OI-wiki/OI-wiki/issues)、[Pull Request](https://github.com/OI-wiki/OI-wiki/pulls)，或者在交流群中分享你的想法、直接向管理员投稿．目前，我们使用的框架是用 Python 开发的 [MkDocs](https://mkdocs.readthedocs.io)，支持 Markdown 格式（也支持插入数学公式）．

***

Q：可是我比较弱……不知道我能做点什么．

A：一切源于热爱．你可以协助其他人审核修改稿件，帮助我们宣传 **OI Wiki**，为社区营造良好学习交流氛围！

***

Q：现在主要是谁在做这件事啊？感觉这是个大坑，真的能做好吗？

A：最开始主要是一些退役老年选手在做这件事，后来遇到了很多志同道合的小伙伴：有现役选手，退役玩家，也有从未参加过 **OI** 的朋友．目前，这个项目主要是由 **OI Wiki** 项目组来维护（下面是一张合影）．

<a href="https://github.com/OI-wiki/OI-wiki/graphs/contributors"><img src="https://opencollective.com/oi-wiki/contributors.svg?width=890&button=false"/></a>

当然，这个项目只靠我们的力量是很难做得十全十美的，我们诚挚地邀请你一起来完善 **OI Wiki**．

***

Q：你们怎么保证我们添加的内容不会突然消失？

A：我们把内容托管在 [GitHub](https://github.com/OI-wiki/OI-wiki) 上面，即使我们的服务器翻车了，内容也不会丢失．另外，我们也会定期备份大家的心血，即使有一天 GitHub 倒闭了（？），我们的内容也不会丢失．

***

Q：**OI Wiki** 好像有空的页面啊！

A：是的．受限于项目组成员的水平和时间，我们暂时无法完成这些空页面．所以我们在这里进行征稿和招募，希望可以遇到有同样想法的朋友，我们一起把 **OI Wiki** 完善起来．

***

Q：为什么不直接去写 [中文维基百科](https://zh.wikipedia.org/) 呢？

A：因为我们希望可以真正帮到更多的选手或者对这些内容感兴趣的人．而且由于众所周知的原因，中文维基上的内容并不是无门槛就可以获取到的．

## 我想参与进来！

Q：我要怎么与项目组交流？

A：可以通过 [关于本项目里的交流方式](./about.md#交流方式) 联系我们．

***

Q：我要怎么贡献代码或者内容？

请参考 [如何参与](./htc.md) 页面．

***

Q：目录在哪？

A：目录在项目根目录下的 [mkdocs.yml](https://github.com/OI-wiki/OI-wiki/blob/master/mkdocs.yml#L17) 文件中．

***

Q：如何修改一个 topic 的内容？

A：在对应页面右上方有一个编辑按钮<i class="md-icon">edit</i>，点击并确认阅读了 [如何贡献](./htc.md) 之后会跳转到 GitHub 上对应文件的位置．

或者也可以自行阅读目录 [(mkdocs.yml)](https://github.com/OI-wiki/OI-wiki/blob/master/mkdocs.yml) 查找文件位置．

***

Q：如何添加一个 topic？

A：有两种选择：

-   可以开一个 Issue，注明希望能添加的内容．
-   可以开一个 Pull Request，在目录 [(mkdocs.yml)](https://github.com/OI-wiki/OI-wiki/blob/master/mkdocs.yml) 中加上新的 topic，并在 [docs](https://github.com/OI-wiki/OI-wiki/tree/master/docs) 文件夹下对应位置创建一个空的 `.md` 文件．文档的格式细节请参考 [格式手册](./format.md#贡献文档要求)．

***

Q：我尝试访问 GitHub 的时候遇到了困难．

A：推荐在 hosts 文件中加入如下几行[^ref1]：

```text
# GitHub Start
140.82.114.25                 alive.github.com
140.82.113.5                  api.github.com
185.199.110.153               assets-cdn.github.com
185.199.111.133               avatars.githubusercontent.com
185.199.111.133               avatars0.githubusercontent.com
185.199.111.133               avatars1.githubusercontent.com
185.199.111.133               avatars2.githubusercontent.com
185.199.111.133               avatars3.githubusercontent.com
185.199.111.133               avatars4.githubusercontent.com
185.199.111.133               avatars5.githubusercontent.com
185.199.111.133               camo.githubusercontent.com
140.82.112.22                 central.github.com
185.199.111.133               cloud.githubusercontent.com
140.82.114.9                  codeload.github.com
140.82.113.22                 collector.github.com
185.199.111.133               desktop.githubusercontent.com
185.199.111.133               favicons.githubusercontent.com
140.82.112.3                  gist.github.com
52.216.163.147                github-cloud.s3.amazonaws.com
52.217.124.1                  github-com.s3.amazonaws.com
52.216.144.83                 github-production-release-asset-2e65be.s3.amazonaws.com
52.217.121.249                github-production-repository-file-5c1aeb.s3.amazonaws.com
52.217.206.57                 github-production-user-asset-6210df.s3.amazonaws.com
192.0.66.2                    github.blog
140.82.114.4                  github.com
140.82.113.18                 github.community
185.199.110.154               github.githubassets.com
151.101.1.194                 github.global.ssl.fastly.net
185.199.110.153               github.io
185.199.111.133               github.map.fastly.net
185.199.110.153               githubstatus.com
140.82.112.25                 live.github.com
185.199.111.133               media.githubusercontent.com
185.199.111.133               objects.githubusercontent.com
13.107.42.16                  pipelines.actions.githubusercontent.com
185.199.111.133               raw.githubusercontent.com
185.199.111.133               user-images.githubusercontent.com
13.107.253.40                 vscode.dev
140.82.112.21                 education.github.com
# GitHub End
```

可以在 [GitHub520](https://gitee.com/klmahuaw/GitHub520) 上了解到最新内容和更多信息．

Linux 和 macOS 用户可以尝试使用 [依云](https://github.com/lilydjwg/) 的 [gh-check 脚本](https://gist.github.com/lilydjwg/93d33ed04547e1b9f7a86b64ef2ed058) 获取访问最快的 IP，使用 `--hosts` 参数可以直接更新 hosts 文件．使用 `--help` 参数可以获取使用帮助．使用先需要安装 Python3 和 aiohttp（`pip install aiohttp -i https://pypi.tuna.tsinghua.edu.cn/simple/`）．依云博客的介绍：[寻找最快的 GitHub IP](https://blog.lilydjwg.me/2019/8/16/gh-check.214730.html)．

同时，您可以使用 [Gitclone](https://www.gitclone.com/) 服务加速 Clone，可以阅读其首页上的说明．

如果您仅仅是想 Clone **OI Wiki** 的仓库，那么：

```bash
git clone https://gitclone.com/github.com/OI-wiki/OI-wiki
```

如果您需要向 **OI Wiki** 贡献，那么首先 fork **OI Wiki** 的仓库，然后（将 `username` 替换为您的用户名），需要注意的是提供的示例将使您使用 SSH 连接到 GitHub[^only-ssh-connect]：

```bash
git clone https://gitclone.com/github.com/username/OI-wiki
git remote set-url origin git@github.com:username/OI-wiki.git
```

***

Q：我这里 pip 也太慢了！

A：可以选择更换国内源[^ref2]，或者：

```bash
pip install -U -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

***

Q：我在客户端 clone 了这个项目，速度太慢．

A：如果有安装 `git bash`，可以加几个限制来减少下载量．[^ref3]

```bash
git clone https://github.com/OI-wiki/OI-wiki.git --depth=1 -b master
```

***

Q：我没装过 Python 3．

A：可以访问 [Python 官网](https://www.python.org/downloads/) 了解更多信息．

***

Q：好像提示我 pip 版本过低．

A：进入 cmd/shell 之后，执行以下命令：

```bash
python -m pip install --upgrade pip
```

***

Q：我安装依赖失败了．

A：检查一下：网络？权限？查看错误信息？

***

Q：我已经 clone 下来了，为什么部署不了？

A：检查一下是否安装好了依赖？

***

Q：我 clone 了很久之前的 repo，怎么更新到新版本呢？

A：请参考 GitHub 官方的帮助页面 [Syncing a fork - GitHub Docs](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/syncing-a-fork)．

***

Q：如果是装了之前的依赖怎么更新？

A：请输入以下命令：

```bash
pip install -U -r requirements.txt
```

***

Q：为什么我的 markdown 格式乱了？

A：可以查阅 [cyent 的笔记](https://web.archive.org/web/20221103014610/https://cyent.github.io/markdown-with-mkdocs-material/)，或者 [MkDocs 使用说明](https://github.com/ctf-wiki/ctf-wiki/wiki/Mkdocs-%E4%BD%BF%E7%94%A8%E8%AF%B4%E6%98%8E)．

我们目前使用 [remark-lint](https://github.com/remarkjs/remark-lint) 来自动化修正格式，可能还有一些 [配置](https://github.com/OI-wiki/OI-wiki/blob/master/.remarkrc) 不够好的地方，欢迎指出．

***

Q：GitHub 是不是不显示我的数学公式？

A：是的，GitHub 的预览不显示数学公式．但是请放心，MkDocs 是支持数学公式的，可以正常使用，只要是 MathJax 支持的句式都可以使用．

***

Q：我的数学公式怎么乱码了？

A：如果是行间公式（用的 `$$`），目前已知的问题是需要在 `$$` 两侧留有空行，且 `$$` 要 **单独** 放在一行里（且不要在前加空格）．格式如下：

```text
// 空行
$$
a_i
$$
// 空行
```

***

Q：我的公式为什么在目录里没有正常显示？好像双倍了．

A：是的，这个是 python-markdown 的一个 bug，可能近期会修复．

如果想要避免目录中出现双倍公式，可以参考 [string 分类下 SAM 的目录写法](https://github.com/OI-wiki/OI-wiki/blame/master/docs/string/sam.md#L73)．

```text
结束位置 <script type="math/tex">endpos</script>
```

在目录中会变成

```text
结束位置 endpos
```

注：现在请尽量避免在目录中引入 MathJax 公式．

***

Q：如何给一个页面单独声明版权信息？

A：在页面开头加一行即可．[^ref4]

比如：

```text
copyright: SATA
```

注：默认的是 CC BY-SA 4.0 和 SATA．

***

Q：为什么作者信息统计处没有我的名字？

A：如果你发现自己写过一个页面中的部分内容，但是你没有被记录进作者列表，可以把自己的 GitHub ID 加入到文件头的 [author 字段](./htc.md#author-字段)．

***

感谢你看到了最后，我们现在亟需的，就是你的帮助．

**OI Wiki** 项目组

2018.8

## 参考资料与注释

[^ref1]: [GitHub520](https://gitee.com/klmahuaw/GitHub520)

[^ref2]: [更改 pip 源至国内镜像 - L 瑜 - CSDN 博客](https://blog.csdn.net/lambert310/article/details/52412059)

[^ref3]: [GIT--- 看我一步步入门（Windows Git Bash）](https://blog.csdn.net/FreeApe/article/details/46845555)

[^ref4]: [Metadata - Material for MkDocs](https://squidfunk.github.io/mkdocs-material/extensions/metadata/#usage)

[^only-ssh-connect]: GitHub 弃用了基于密码身份验证的 HTTPS 协议，连接必须使用 SSH 或者 Personal Access Token，参见 [我应使用哪个远程 URL？](https://docs.github.com/cn/github/using-git/which-remote-url-should-i-use)，[创建个人访问令牌](https://docs.github.com/cn/github/authenticating-to-github/creating-a-personal-access-token) 和 [使用 SSH 连接到 GitHub](https://docs.github.com/cn/github/authenticating-to-github/connecting-to-github-with-ssh)．


## intro/format.md

在文章开始之前，**OI Wiki** 项目组全体成员十分欢迎您为本项目贡献页面．正因为有了上百位像您一样的人，才有了 **OI Wiki** 的今天！

本页面将列出在 **OI Wiki** 编写过程时推荐使用的格式规范与编辑方针．请您在撰稿或者修正 Wiki 页面以前，仔细阅读以下内容，以帮助您完成更高质量的内容．

如果您已迫不及待，想要快速上手，建议先阅读 [太长不看版](#太长不看版) 与 [图片举例](#图解) 的章节．

??? abstract "Changelog"
    **注意**：只记录和写作、审阅等相关的改动，不记录格式修正等改动．
    
    | 时间         | 主要内容                                                | 相关 Issue/Pull Request 链接                                                                                    |
    | ---------- | --------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
    | 2026-02-22 | 完善引号使用的相关规定                                         | [#6793](https://github.com/OI-wiki/OI-wiki/pull/6793)                                                       |
    | 2026-01-07 | 要求使用全角句点替代中文句号                                      | [#6746](https://github.com/OI-wiki/OI-wiki/pull/6746)                                                       |
    | 2025-08-10 | 添加格式手册的格式要求；<br>代码：补充片段代码相关要求                       | [#6412](https://github.com/OI-wiki/OI-wiki/pull/6412)                                                       |
    | 2025-08-10 | 添加 Changelog 与 TL;DR                                | [#6409](https://github.com/OI-wiki/OI-wiki/pull/6409)                                                       |
    | 2024-10-08 | 代码：为适应全平台测试完善了格式要求                                  | [#5912](https://github.com/OI-wiki/OI-wiki/pull/5912)，[#5924](https://github.com/OI-wiki/OI-wiki/pull/5924) |
    | 2024-03-26 | 引用 OJ 题目链接时使用原链接，而不是镜像链接                            | [#5482](https://github.com/OI-wiki/OI-wiki/pull/5482)                                                       |
    | 2023-10-09 | 主题插件：新增选项卡[^note6]的格式要求                             | [#5152](https://github.com/OI-wiki/OI-wiki/pull/5152)                                                       |
    | 2023-07-23 | 对于工具类内容的下载安装等内容，要求引用官方文档                            | [#5023](https://github.com/OI-wiki/OI-wiki/pull/5023)                                                       |
    | 2023-04-15 | 补充引号的使用规范                                           | [#4792](https://github.com/OI-wiki/OI-wiki/pull/4792)                                                       |
    | 2023-03-28 | LaTeX：数学符号表                                         | [#4587](https://github.com/OI-wiki/OI-wiki/pull/4587)                                                       |
    | 2023-03-02 | 补充全半角标点与连接号的使用规范                                    | [#4726](https://github.com/OI-wiki/OI-wiki/pull/4726)                                                       |
    | 2022-12-13 | 主题插件：移除嵌套折叠框的阴影样式要求                                 | [#4500](https://github.com/OI-wiki/OI-wiki/pull/4500)                                                       |
    | 2022-08-09 | 引用内链的某一节内容时，使用中文标题                                  | [#4057](https://github.com/OI-wiki/OI-wiki/pull/4057)                                                       |
    | 2022-06-12 | 完善目录更改的相关要求[^note4]                                 | [#4043](https://github.com/OI-wiki/OI-wiki/pull/4043)                                                       |
    | 2021-09-09 | 主题插件：补充折叠框相关要求                                      | [#3517](https://github.com/OI-wiki/OI-wiki/pull/3517)                                                       |
    | 2021-09-03 | LaTeX：`\Leftrightarrow` $\to$ `\iff`                | [#3499](https://github.com/OI-wiki/OI-wiki/pull/3499)                                                       |
    | 2021-08-18 | 代码：新增例题代码的格式要求                                      | [#3447](https://github.com/OI-wiki/OI-wiki/pull/3447)                                                       |
    | 2021-08-12 | 图片：动图优先使用 APNG 格式                                   | [#3422](https://github.com/OI-wiki/OI-wiki/pull/3422)                                                       |
    | 2021-06-29 | 图片：建议同时提交源文件                                        | [#3255](https://github.com/OI-wiki/OI-wiki/pull/3255)                                                       |
    | 2021-05-29 | 代码：删除大括号不换行的要求，补充可读性要求                              | [#3197](https://github.com/OI-wiki/OI-wiki/pull/3197)                                                       |
    | 2021-03-15 | 站点维护：规范 Pull Request 的合并方式[^note5]                  | [#3061](https://github.com/OI-wiki/OI-wiki/pull/3061)                                                       |
    | 2021-02-01 | LaTeX：`\lt` $\to$ `<`，`\gt` $\to$ `>`               | [#2950](https://github.com/OI-wiki/OI-wiki/pull/2950)                                                       |
    | 2021-01-27 | 建议在 [互联网档案馆](https://web.archive.org/) 保存外链备份       | [#2918](https://github.com/OI-wiki/OI-wiki/pull/2918)                                                       |
    | 2020-09-19 | 站点维护：Commit Message 与 Pull Request 标题的书写要求[^note4]  | [#2744](https://github.com/OI-wiki/OI-wiki/pull/2744)                                                       |
    | 2020-10-18 | 图片：优先使用 SVG 格式                                      | [#2215](https://github.com/OI-wiki/OI-wiki/pull/2215)                                                       |
    | 2020-08-05 | LaTeX：新增多字母变量的格式要求                                  | [#2502](https://github.com/OI-wiki/OI-wiki/pull/2502)                                                       |
    | 2020-07-28 | LaTeX：`cases` 环境禁止超过两列                              | [#2466](https://github.com/OI-wiki/OI-wiki/pull/2466)                                                       |
    | 2020-07-24 | LaTeX：`{n \choose m}`$\to$ `\dbinom{n}{m}`          | [#2442](https://github.com/OI-wiki/OI-wiki/pull/2442)                                                       |
    | 2020-07-20 | Markdown：禁用删除线语法                                    | [#2422](https://github.com/OI-wiki/OI-wiki/pull/2422)                                                       |
    | 2020-07-19 | 主题插件：要求保留折叠框[^note3]中空行的缩进空格；<br>LaTeX：追加对数学公式的格式要求 | [#2412](https://github.com/OI-wiki/OI-wiki/pull/2412)                                                       |
    | 2020-07-11 | 最初版本                                                | [#2350](https://github.com/OI-wiki/OI-wiki/pull/2350)                                                       |

## 太长不看版

为方便初次阅读本文档的用户，本节列举该手册中的若干重点事项：

-   文件存储：

    -   使用小写文件名，以 `-` 代替空格．详见 [SAVE-1](#SAVE-1)．

    -   不要插入外链图片．详见 [SAVE-2](#SAVE-2)．

    -   图片尽可能使用 SVG 格式，只应使用 SVG 1.1 标准．详见 [SAVE-3](#SAVE-3)．

    -   动图应使用 SVG 或 APNG 格式．详见 [SAVE-4](#SAVE-4)．

    -   有源文件的图片建议同时提交源文件．详见 [SAVE-5](#SAVE-5)．

    -   插入外链时建议同时插入快照链接．详见 [SAVE-6](#SAVE-6)．

    -   不要以插入外链的方式插入内链．详见 [SAVE-7](#SAVE-7)．

-   标点符号：

    -   规范使用标点符号．在每句话的末尾添加 **句号**．详见 [PUNC-1](#PUNC-1) 至 [PUNC-7](#PUNC-7)．

    -   注意区分连接号（hyphen、en dash、em dash）．详见 [PUNC-8](#PUNC-8)．

-   Markdown 语法与主题扩展语法：

    -   只应使用二级、三级、四级标题．不要使用标题替代加粗．不要在标题写 LaTeX 公式．详见 [LINT-1](#LINT-1)、[MDFM-1](#MDFM-1)、[CONT-4](#CONT-4)、[CONT-9](#CONT-9)．

    -   使用折叠框[^note3]语法和选项卡[^note6]语法时，须保持内部缩进一致，**对空行也是如此**．**不要漏掉** 空行的空格缩进．详见 [LINT-6](#LINT-6)、[MDFM-6](#MDFM-6)．

    -   不要使用删除线 `~~foo~~` 语法．详见 [LINT-3](#LINT-3)．

    -   行间公式应写作

        ```text
        $$
        a^{2}=b^{2}+c^{2}
        $$
        ```

        而不是 `$$a^{2}=b^{2}+c^{2}$$`．详见 [LINT-5](#LINT-5)．

    -   使用折叠框而不是块引用（Blockquotes）．详见 [MDFM-5](#MDFM-5)．

    -   代码块只应使用 ` ``` ` 语法，且须标注语言．详见 [LINT-7](#LINT-7)、[MDFM-3](#MDFM-3)．

-   LaTeX 公式：
    -   不应与 [数学符号表](./symbol.md) 相冲突．详见 [MATH-1.1](#MATH-1.1)．

    -   注意字体的使用，详见 [MATH-1.2](#MATH-1.2)、[MATH-1.15](#MATH-1.15)、[MATH-2.6](#MATH-2.6)、[MATH-2.7](#MATH-2.7)．

    -   不要滥用 LaTeX 公式．详见 [MATH-1.14](#MATH-1.14)．

    -   不要 LaTeX 公式里使用程序设计语言的表示方式．（如：不要使用 $a==b$、$a<<1$、$a\%b$．）不要使用中括号连缀（$a[i][j]$）．详见 [MATH-1.9](#MATH-1.9)、[MATH-1.10](#MATH-1.10)．

-   代码：

    -   尽可能简洁易懂，避免压行等不良习惯．尽可能保证可读性，突出算法思想．详见 [CONT-10](#CONT-10)．

    -   不推荐直接把代码插入 Markdown 文档中．详见 [CODE-1.1](#CODE-1.1)、[CODE-1.2](#CODE-1.2)．

## 对本文档的格式要求

-   <span id="FREQ-1">FREQ-1</span>：修订格式手册的条目时需同时补充 Changelog．若只是修正格式，则无需补充 Changelog．
-   <span id="FREQ-2">FREQ-2</span>：除 [太长不看版](#太长不看版) 一节外，格式手册的条目都需要有不重复的编号，编号需要匹配正则表达式 `(?<category>[A-Z]{4})-(?<id>[1-9][0-9]*(?:\.[1-9][0-9]*)*)`，其中 `category` 应具有直观的含义．说明文字不需要有编号．
-   <span id="FREQ-3">FREQ-3</span>：[太长不看版](#太长不看版) 的条目必须来自格式手册其他章节的内容，且需在末尾引用对应的条目编号．
-   <span id="FREQ-4">FREQ-4</span>：条目的编号一旦确定就不应更改．如果确需更改（如删除、合并条目），则应用类似「已废止」、「迁移至 XXXX-id」的文字注明．

## 贡献文档要求

当你打算贡献某部分的内容时，你应该尽量熟悉以下三部分：

-   文档存储的格式
-   文档的合理性
-   remark-lint 和 $\rm{\LaTeX}$ 公式的格式要求

### 文档引用与存储的格式

-   <span id="SAVE-1">SAVE-1</span>：**文件名请务必都小写，以 `-` 分割．** 例如：`file-name.md`．

-   <span id="SAVE-2">SAVE-2</span>：请务必确保文档中引用的 **外链** 图片已经全部转存到了 **本库内** 对应的 `images` 文件夹中（防止触发某些网站的防盗链），建议处理成 `MD 文档名称 + 编号` 的形式（可参考已有文档中图片的处理方式）．例如：本篇文档的文件名称为 format，则文档中引用的第一张图片的名字为 `format1.png`．

-   <span id="SAVE-3">SAVE-3</span>：推荐使用 SVG 格式的图片[^ref4]，以获取较好的清晰度和缩放效果．由于 **OI Wiki** 各组件对 SVG 标准的兼容性不同，所以您的图片应基于 [SVG 1.1](http://www.w3.org/TR/SVG11/) 标准．

-   <span id="SAVE-4">SAVE-4</span>：动图如果无法或者不会制作 SVG 格式的，则推荐使用 APNG 格式[^apng]的文件．Windows 用户可使用 [ScreenToGif](https://www.screentogif.com) 录制，Linux 用户可使用 [Peek](https://github.com/phw/peek) 录制，注意需要在设置里调整为录制 APNG．其他情况则推荐先制作为 MP4 等视频文件再转换为 APNG，如果使用 ffmpeg 则可以使用 `ffmpeg -i filename.mp4 -f apng filename.apng -plays 0` 转换．[^intro-apng]

-   <span id="SAVE-5">SAVE-5</span>：同时具有源文件和导出图像的图片（例如 JPG 文件与 PSD 文件或者 SVG 图像与 TikZ TeX 源代码），建议将源文件以与图片相同的文件名保存于同一目录下．

-   <span id="SAVE-6">SAVE-6</span>：请确保您的文档中的引用链接的稳定性．**不推荐** 引用 **自建** 服务中的资源（如自建 OJ 里的题目）．建议在添加时同时将该外链存于互联网档案馆[^webarchive]，以防无法替代的链接失效．

-   <span id="SAVE-7">SAVE-7</span>：站内链接请去掉网站域名，并且使用相对路径链接对应 `.md` 文件．例如，在本页面（`intro/format`）中链接杂项简介（`misc`），应使用 `[杂项简介](../misc/index.md)`．可以在链接中添加 hash 来链接到某一节，例如 [`[Pull Request 信息格式规范](./htc.md#pull-request-信息格式规范)`](./htc.md#pull-request-信息格式规范)，hash 的值可以通过位于每个标题右侧的按钮或者位于网页右侧的目录中的链接得到．

### 文档的合理性

**合理性**，指所编写的 **内容** 必须具有如下的特性：

-   <span id="STRC-1">STRC-1</span>：由浅入深，内容的难度应该具有渐进性．
-   <span id="STRC-2">STRC-2</span>：逻辑性．

    -   <span id="STRC-2.1">STRC-2.1</span>：对于算法或数学概念类内容的撰写应该尽量包含以下的内容：

        1.  原理：说明该内容对应的原理；
        2.  例子：给出 1 \~ 2 个典型的例子；
        3.  题目：在该标题下，**只需要给出题目名字和题目链接**．对于算法类题目，题目链接 OJ 的优先级为：原 OJ（国外 OJ 要求国内可流畅访问）> UOJ > LOJ > 洛谷．

        示例页面：[IDA\*](../search/idastar.md)

    -   <span id="STRC-2.2">STRC-2.2</span>：对于工具类内容的撰写应该尽量包含以下的内容：

        1.  简介：阐明该工具的背景与用途．
        2.  配置方式：详细给出配置环境与使用的过程，下载与安装方法建议尽量引用官方文档．

        示例页面：[WSL (Windows 10)](../tools/wsl.md)

除现有内容质量较低的情况外，建议尽量从 **补充** 的角度来做贡献，而非采取直接覆盖的方式．如果拿不准主意，可以参考 [关于本项目的交流方式](./about.md#交流方式) 一节，与 **OI Wiki** 项目组联系．

### 文档的基本格式要求

#### Remark-lint 的格式要求

[remark-lint](https://github.com/remarkjs/remark-lint) 可以自动给项目内文件统一风格．**OI Wiki** 现在启用的配置文件托管在 [.remarkrc](https://github.com/OI-wiki/OI-wiki/blob/master/.remarkrc)．

在配置过程中 **OI Wiki** 项目组也遇到了一些 remark-lint 不能很好处理的问题，所以请严格按照下列要求编辑文档：

-   <span id="LINT-1">LINT-1</span>：不要使用如 `<h1>` 或者 `# 标题` 的一级标题．

-   <span id="LINT-2">LINT-2</span>：标题要空一个英文半角空格，例如：`## 简介`．

-   <span id="LINT-3">LINT-3</span>：由于 remark-lint 不能很好地处理删除线，因此请不要使用删除线语法（不使用删除线语法的另外一个原因是，删除线划去的内容大多为「抖机灵」性质，对读者理解帮助不大，不符合下面的「文本内容的格式要求」中 [对内容表述的要求](#CONT-5)）．

-   <span id="LINT-4">LINT-4</span>：列表：
    -   <span id="LINT-4.1">LINT-4.1</span>：列表前要有空行，新开一段．
    -   <span id="LINT-4.2">LINT-4.2</span>：使用有序列表（如 `1. 例子`）时，点号后要有空格．

-   <span id="LINT-5">LINT-5</span>：行间公式前后各要有一行空行，否则会被当做是行内公式．

-   <span id="LINT-6">LINT-6</span>：使用 `???` 或 `!!!` 开头的 Details 语法时，每一行要包括在 Details 语法的文本框的文本，开头必须至少有 4 个空格．

    **即使是空行，也必须保持与其他行一致的缩进．请不要使用编辑器的自动裁剪行末空格功能．**

    ???+ success "示例"
        下面的代码中用 `␣` 表示空格 ` `．
        
        ```text
        ???+ warning
        ␣␣␣␣请记得在文本前面添加 4 个空格．其他的语法还是与 Markdown 语法一致．
        ␣␣␣␣
        ␣␣␣␣不添加 4 个空格的话，文本就不会出现在 Details 文本框里了．
        ␣␣␣␣
        ␣␣␣␣这个`???`是什么的问题会在 [下文](#MDFM-5) 解答．
        ```
        
        ???+ warning "Warning"
            请记得在文本前面添加 4 个空格．其他的语法还是与 Markdown 语法一致．
            
            不添加 4 个空格的话，文本就不会出现在 Details 文本框里了．
            
            这个 `???` 是什么的问题会在 [下文](#MDFM-5) 解答．

-   <span id="LINT-7">LINT-7</span>：代码样式的纯文本块请使用 ` ```text`．直接使用 ` ``` ` 而不指定纯文本块里的语言，可能会导致内容被错误地缩进．

#### 标点符号的使用

-   <span id="PUNC-1">PUNC-1</span>：请在每句话的末尾添加 **句号**．

<!-- scripts.linter.postprocess.fix_full_stop off -->

-   <span id="PUNC-2">PUNC-2</span>：请正确使用 **全角** 标点符号与 **半角** 标点符号．汉语请使用全角符号，英语请使用半角符号．中文中夹用英文时，请参考 [中文出版物夹用英文的编辑规范](https://www.nppa.gov.cn/xxgk/fdzdgknr/hybz/202210/t20221004_445147.html)．特别地，请用全角句点「．」替代中文句号「。」．

<!-- scripts.linter.postprocess.fix_full_stop on -->

<!-- scripts.linter.postprocess.fix_quotation off -->

-   <span id="PUNC-3">PUNC-3</span>：由于 `“……”` 和 `‘……’` 未区分全半角，请使用 `「……」` 作为全角双引号，`"..."` 作为半角双引号，`『……』` 作为全角单引号，`'...'` 作为半角单引号．

<!-- scripts.linter.postprocess.fix_quotation on -->

-   <span id="PUNC-4">PUNC-4</span>：注意区分 **顿号** 与 **逗号** 的使用．
-   <span id="PUNC-5">PUNC-5</span>：注意 **括号** 的位置．句内括号与句外括号的位置不同．
-   <span id="PUNC-6">PUNC-6</span>：通常使用 **分号** 来表示列表环境中各复句之间的关系．
-   <span id="PUNC-7">PUNC-7</span>：对于有序列表，推荐在每一项的后面添加 **分号**，在列表最后一项的后面添加 **句号**；对于无序列表，推荐在每一项的后面添加 **句号**．
-   <span id="PUNC-8">PUNC-8</span>：注意区分各种不同的连接号，如 hyphen（一般使用 U+002D hyphen-minus（-），即键盘上的「减号」代替），U+2013 en dash（–）和 U+2014 em dash（—）．（英文中连接多个人名时，须用 en dash，但是极常误用为 hyphen．其他误用较为罕见，基本上只需记住这一点即可．）详见 [连接号 - 维基百科](https://zh.wikipedia.org/wiki/%E8%BF%9E%E6%8E%A5%E5%8F%B7)．

    ???+ success "示例"
        -   中学生学科竞赛主要包括信息学奥林匹克竞赛、信息学奥林匹克竞赛、信息学奥林匹克竞赛、信息学奥林匹克竞赛和信息学奥林匹克竞赛（谁写的这个示例，建议抬走）．
        -   「你吃了吗？」李四问张三．
        -   我想对你说：「我真是太喜欢你了．」
        -   「苟利国家生死以，岂因祸福避趋之！」
        -   张华考上了大学；李萍进了技校；我当了工人：我们都有美好的前途．[^note1]
        -   以下是这个算法的基本流程：
            1.  初始化到各点的距离为无穷大，将所有点设置为未被访问过，初始化一个队列；
            2.  将起点放入队列，将起点设置为已被访问过，更新到起点的距离为 $0$；
            3.  取出队首元素，将该元素设置为未被访问过；
            4.  遍历所有与此元素相连的边，若到这个点存在更短的距离，则进行松弛操作；
            5.  若这个点未被访问过，则将这个点放入队列，且设置这个点为已经访问过；
            6.  回到第三步，直到队列为空．
        -   KMP 算法（Knuth–Morris–Pratt algorithm, KMP algorithm）由 Knuth、Pratt 和 Morris 在 1977 年共同发布．[^note2]

#### Markdown 格式与主题扩展格式要求

-   <span id="MDFM-1">MDFM-1</span>：表示强调时请使用 `**SOMETHING**` 和 `「」`，而非某级标题，因为使用标题会导致文章结构层次混乱和（或）目录出现问题．

-   <span id="MDFM-2">MDFM-2</span>：当需要引用题目链接时，应尽可能使用原 OJ 题库中的链接而不是镜像链接．

-   <span id="MDFM-3">MDFM-3</span>：请正确使用 Markdown 的区块功能．插入行内代码请使用一对反引号包围代码区块；行间代码请使用一对 ` ``` ` 包围代码区块，其中反引号就是键盘左上角波浪线下面那个符号，行间代码请在第一个 ` ``` ` 的后面加上语言名称（如：` ```cpp`）．

    ???+ success "示例"
        ````text
        ```cpp
        // #include<stdio.h>    //不好的写法
        #include <cstdio>  //好的写法
        ```
        ````
        
        ```cpp
        // #include<stdio.h>    //不好的写法
        #include <cstdio>  //好的写法
        ```

-   <span id="MDFM-4">MDFM-4</span>：「参考资料与注释」使用 Markdown 的脚注功能进行编写．格式为：

    ```markdown
    文本内容．[^脚注名]
    [^脚注名]: 参考资料内容．注意：冒号是英文冒号，冒号后面跟着一个空格．
    ```

    脚注名既可以使用数字也可以使用文本．脚注名摆放的位置与括号的用法一致．为美观起见，建议同一个页面内的脚注名遵循统一的命名规律，如：ref1、ref2、note1……

    脚注的内容统一放在 `## 参考资料与注释` 二级标题下．

    ???+ success "示例"
        ```markdown
        当 `#include <cxxxx>` 可以替代 `#include <xxxx.h>` 时，应使用前者．[^ref1]
        
        2020年1月21日，CCF宣布恢复NOIP．[^ref2]
        
        ## 参考资料与注释
        
        [^ref1]: [cstdio stdio.h namespace](https://stackoverflow.com/questions/10460250/cstdio-stdio-h-namespace)
        
        [^ref2]: [CCF关于恢复NOIP竞赛的公告-中国计算机学会](https://www.ccf.org.cn/c/2020-01-21/694716.shtml)
        ```
        
        当 `#include <cxxxx>` 可以替代 `#include <xxxx.h>` 时，应使用前者．[^ref1]
        
        2020 年 1 月 21 日，CCF 宣布恢复 NOIP．[^ref2]

-   <span id="MDFM-5">MDFM-5</span>：建议使用主题扩展的 `???+note` 格式（即 [Collapsible Blocks](https://squidfunk.github.io/mkdocs-material/reference/admonitions/#collapsible-blocks)）来描述题面和参考代码．也可以用这种格式来展示其他需要补充介绍的内容．

    示例代码（下面的代码中用 `␣` 表示空格 ` `）：

    ```text
    ??? note "标题"
    ␣␣␣␣这个文本框会被默认折叠．
    ␣␣␣␣
    ␣␣␣␣推荐将 **解题代码** 放在折叠文本框内．

    ???+note "[HDOJ 的「A + B Problem」](https://acm.hdu.edu.cn/showproblem.php?pid=1000)"
    ␣␣␣␣标题也可以使用 Markdown 的超链接．这里的超链接是 HDOJ 的「A + B Problem」．
    ␣␣␣␣
    ␣␣␣␣而且推荐以这种方式**标注原题链接**．
    ␣␣␣␣
    ␣␣␣␣注意双引号的位置．
    ```

    效果：

    ??? note "标题"
        这个文本框会被默认折叠．
        
        推荐将 **解题代码** 放在折叠文本框内．

    ???+ note "[HDOJ 的「A + B Problem」](https://acm.hdu.edu.cn/showproblem.php?pid=1000)"
        标题也可以使用 Markdown 的超链接．这里的超链接是 HDOJ 的「A + B Problem」．
        
        而且推荐以这种方式 **标注原题链接**．
        
        注意双引号的位置．

    两种格式的区别是，带 `+` 的会默认保持展开，而不带 `+` 的会默认保持折叠．

    折叠框的标题，即 `???+note` 中 `note` 后的内容应以 `"` 包裹起来．其中的内容支持 Markdown 语法．详见 [Admonition - Changing the title](https://squidfunk.github.io/mkdocs-material/reference/admonitions/#changing-the-title)．（不具备折叠功能的为一般的 Admonitions，参考 [Admonitions - Material for MkDocs](https://squidfunk.github.io/mkdocs-material/reference/admonitions)）

-   <span id="MDFM-6">MDFM-6</span>：当需要添加不同语言的代码时，推荐使用 Content tabs，可以实现不同语言代码的切换．Content tabs 还有其他的用法，详见 [Content tabs](https://squidfunk.github.io/mkdocs-material/reference/content-tabs/#usage)．其使用方法和效果如下．

    ???+ success "示例"
        注意需要在文本前面添加 4 个空格（下面用 `␣` 表示）．其他的语法还是与 Markdown 语法一致．
        
        ````text
        === "C"
        ␣␣␣␣```c
        ␣␣␣␣#include <stdio.h>
        ␣␣␣␣
        ␣␣␣␣int main(void) {
        ␣␣␣␣  printf("Hello world!\n");
        ␣␣␣␣  return 0;
        ␣␣␣␣}
        ␣␣␣␣```
        
        === "C++"
        ␣␣␣␣```cpp
        ␣␣␣␣#include <iostream>
        ␣␣␣␣
        ␣␣␣␣int main(void) {
        ␣␣␣␣  std::cout << "Hello world!" << std::endl;
        ␣␣␣␣  return 0;
        ␣␣␣␣}
        ␣␣␣␣```
        ````
        
        === "C"
            ```c
            #include <stdio.h>
            
            int main(void) {
              printf("Hello world!\n");
              return 0;
            }
            ```
        
        === "C++"
            ```cpp
            #include <iostream>
            
            int main(void) {
              std::cout << "Hello world!" << std::endl;
              return 0;
            }
            ```

如果对 mkdocs-material（我们使用的这个主题）还有什么问题，还可以查阅 [MkDocs 使用说明](https://github.com/ctf-wiki/ctf-wiki/wiki/Mkdocs-%E4%BD%BF%E7%94%A8%E8%AF%B4%E6%98%8E)，其介绍了 mkdocs-material 主题的插件使用方式．

#### 文本内容的格式要求

-   <span id="CONT-1">CONT-1</span>：所有的 **OI Wiki** 文本都应使用粗体标记．

-   <span id="CONT-2">CONT-2</span>：在页面的开头应有一段简短的文字（如「本页面将介绍……」），用于概述页面内容．

    ???+ success "示例"
        本页面将列出在 **OI Wiki** 编写过程时推荐使用的格式规范与编辑方针．

-   <span id="CONT-3">CONT-3</span>：涉及到「前置知识」的页面，请在开头添加一行 **前置知识：……**，放在页面概述前．格式如下：

    `前置知识：[站内页面1](url1)、[站内页面2](url2)和[站内页面3](url3)`

    ???+ success "示例"
        前置知识：[时间复杂度](../basic/complexity.md)
        
        本页面将介绍基础的计算理论的知识．

-   <span id="CONT-4">CONT-4</span>：请注意文档结构．文档结构应当十分条理，层次清晰．请不要让诸如「五级标题」这种事情再次发生了，一篇正常的文章是用不到如此复杂的结构层次的．

-   <span id="CONT-5">CONT-5</span>：请注意内容的表述．作为一个百科网站，**OI Wiki** 使用的语言应该是书面的，客观的．诸如「抖机灵」性质的，对读者理解帮助不大的内容，不应该出现在 **OI Wiki** 当中．

-   <span id="CONT-6">CONT-6</span>：请尽量为链接提供完整的标题、或者可被识别的提示，避免使用裸地址和「这」、「此」之类的模糊不清的描述．每一个超链接都应尽量对其加以清楚明确的描述，方便读者明白该超链接将指向何处．

    建议使用源文章或者标签页的标题．

    ???+ failure "不推荐的写法"
        ```markdown
        请参考[这个页面](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/syncing-a-fork)
        
        请参考 <https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/syncing-a-fork>
        ```
        
        请参考 [这个页面](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/syncing-a-fork)
        
        请参考 <https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/syncing-a-fork>

    ???+ success "推荐的写法"
        ```markdown
        请参考 GitHub 官方的帮助页面 [Syncing a fork - GitHub Docs](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/syncing-a-fork)
        ```
        
        请参考 GitHub 官方的帮助页面 [Syncing a fork - GitHub Docs](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/syncing-a-fork)

-   <span id="CONT-7">CONT-7</span>：受 Markdown 格式限制，`## 参考资料与注释` 二级标题必须放在文末．

-   <span id="CONT-8">CONT-8</span>：所有用作序号的数字建议使用中文．示例：
    -   数列的第一项．
    -   输入文件的第一行．

-   <span id="CONT-9">CONT-9</span>：请尽量避免在标题中使用 MathJax 公式，无论是几级标题．在标题中使用公式有可能会导致目录显示错误．[^ref3]

-   <span id="CONT-10">CONT-10</span>：请注意代码的可读性．

    -   <span id="CONT-10.1.1">CONT-10.1.1</span>：代码应拥有清晰的逻辑，尽可能简洁易懂．不要过度压行，不要引入过多无关代码．尽量避免与算法思想无关的内容．
    -   <span id="CONT-10.1.2">CONT-10.1.2</span>：建议在参考代码中添加适当注释以方便读者理解．

    对 C/C++ 类语言：

    -   <span id="CONT-10.2.1">CONT-10.2.1</span>：尽量避免出现影响阅读的预编译指令和宏定义．

    -   <span id="CONT-10.2.2">CONT-10.2.2</span>：不要用 `0` 代替 `false`/`NULL`/`nullptr` 等，不要用 `1` 代替 `true` 等．

    -   <span id="CONT-10.2.3">CONT-10.2.3</span>：在声明 [类型别名](https://en.cppreference.com/w/cpp/language/type_alias) 时，不推荐使用 `typedef`，推荐使用 `using`．

    -   <span id="CONT-10.2.4">CONT-10.2.4</span>：不推荐用宏定义定义常量，推荐直接使用 `constexpr`/`const` 等关键字定义常量．

    -   <span id="CONT-10.2.5">CONT-10.2.5</span>：不推荐对函数使用 `inline` 关键字，详见 [编译优化](../lang/optimizations.md#inline---内联)．

    -   <span id="CONT-10.2.6">CONT-10.2.6</span>：尽量避免类型萃取、偏特化等复杂的模板元编程技巧．如确需使用，则需添加注释解释含义．

        ???+ failure "不推荐的写法"
            ```cpp
            --8<-- "docs/intro/code/format/format_1.cpp:not-recommended"
            ```
            
            该代码给出了一个求 [最大公约数](../math/number-theory/gcd.md) 的复杂实现，其中：
            
            -   第一个 `gcd` 接受两个无符号整数 `x`，`y`，返回 `x`，`y` 的最大公约数，返回值类型的范围保证能同时包含 `x` 和 `y`．
            -   第二个 `gcd` 接受两个整数 `x`，`y`，其中 `x`，`y` 至少有一个是有符号整数，返回 `x`，`y` 的最大公约数．
            -   第三个 `gcd` 接受超过两个整数，返回这些整数的最大公约数．
            -   第四个 `gcd` 接受一个容器，返回容器中所有数的最大公约数．
            
            对 **OI Wiki** 来说，我们只关注最大公约数这个算法的思想，这份代码涵盖了过多无关且复杂的技术细节，是需要避免的．

        ???+ success "推荐的写法"
            ```cpp
            --8<-- "docs/intro/code/format/format_1.cpp:recommended"
            ```
            
            诸如「添加类型检查」、「处理负数输入」、「让函数支持多参数」等更多是工程上关注的话题，我们的重点始终应该是算法的思想．

#### LaTeX 公式的格式要求

LaTeX 作为公式排版的首选，我们应当正确地使用它．因此对于 LaTeX 的使用我们有严格的要求．如果您想要快速上手，可以阅读本章节末给出的表格．

-   <span id="MATH-1.1">MATH-1.1</span>：您使用的符号不应与 [数学符号表](./symbol.md) 规定的符号冲突．

-   <span id="MATH-1.2">MATH-1.2</span>：使用 Roman 体表示数字、常量、算子和函数．使用 Italic 体表示变量、下标．LaTeX 已经预先定义好了一些常见的常量、函数、运算符等，我们可以直接调用，包括但不限于：

    ```latex
    \log, \ln, \lg, \sin, \cos, \tan, \sec, \csc, \cot, \gcd, \min, \max, \exp, \inf, \mod, \bmod, \pmod
    ```

    所以在输入常量、函数名、运算符等时，请先检查一下是否应该使用 Roman 体或其它字体．LaTeX 符号的书写可参考 [KaTeX 的 Supported Functions 页面](https://katex.org/docs/supported.html)（不是全部），也可以搜索求解．

    由于 LaTeX 书写 Roman 体小写希腊字母较为困难，故小写希腊字母常量、算子和函数可以使用 Italic 体，如 $\pi$ 以及 $\delta x$ 中的 $\delta$.

    如果遇到没有预先定义好的需要使用 Roman 体的 **函数名**，我们可以使用 `$\operatorname{something}$` 来产生，如我们可以使用 `$\operatorname{lcm}$` 产生正体的最小公倍数（函数）符号．同理，产生 Roman 体的 **常量** 应用 `$\mathrm{}$`；产生 Roman 体粗体符号应用 `$\mathbf{}$`；产生 Italic 体粗体符号应用 `$\boldsymbol{}$`（如向量 $\boldsymbol{a}$）．对于多字母的变量，应当使用 `$\textit{}$`．其他非数学内容，包括英文、特殊符号等，一律使用 `$\text{}$`．中文我们则建议不放在 LaTeX 公式中．

-   <span id="MATH-1.3">MATH-1.3</span>：如果表达式须折行（常见于较长的行间公式中），则应遵循如下换行规则：

    -   <span id="MATH-1.3.1">MATH-1.3.1</span>：将换行符放在 $=$，$+$，$-$，$\pm$，$\mp$ 之前，如果有必要，也可放在 $\times$，$\cdot$，$/$ 之前，如：

        $$
        \begin{aligned}
            \mathrm{e}^x &= \sum\limits_{n=0}^{\infty} \frac{x^n}{n!} \\
            &= \phantom{+} 1 + x + \frac{x^2}{2} \\
            & \phantom{=} + \frac{x^3}{6} + \frac{x^4}{24} + \dots \\
        \end{aligned}
        $$

    -   <span id="MATH-1.3.2">MATH-1.3.2</span>：同一运算符不应在换行符前后同时出现，

    -   <span id="MATH-1.3.3">MATH-1.3.3</span>：换行符尽量不要出现在括号内的表达式中．

-   <span id="MATH-1.4">MATH-1.4</span>：在行内使用分数的时候，请使用 `$\dfrac{}{}$`．比如 `$\dfrac{1}{2}$`，效果 $\dfrac{1}{2}$，而不是 `$\frac{1}{2}$`，效果 $\frac{1}{2}$．

-   <span id="MATH-1.5">MATH-1.5</span>：组合数请使用 `\dbinom{n}{m}`，效果 $\dbinom{n}{m}$，而不是 `{n \choose m}`（在 LaTeX 中这种写法已不推荐）；与上一条关于分数的约定相似，请不要使用 `\binom{n}{m}`，效果 $\binom{n}{m}$．

-   <span id="MATH-1.6">MATH-1.6</span>：尽可能避免在行内使用巨运算符（如 $\sum$，$\prod$，$\int$ 等）．

-   <span id="MATH-1.7">MATH-1.7</span>：在不会引起歧义的情况下，请用 `$\times$` 代替星号，叉乘请使用 `$\times$`，点乘请使用 `$\cdot$`．如 $a\times b$，$a\cdot b$，而不是 $a\ast b$．

-   <span id="MATH-1.8">MATH-1.8</span>：请用 `$\cdots$`（居于排版基线与顶线中间），`$\ldots$`（居于排版基线的位置），`$\vdots$`（竖着的省略号）代替 `$...$`．如 $a_1,a_2,\cdots a_n$，而不是 $a_1,a_2,... a_n$．

-   <span id="MATH-1.9">MATH-1.9</span>：请注意，不要在非代码区域使用任何程序设计语言的表示方式，而是使用 LaTeX 公式．例如，使用 `$=$` 而不是 `$==$`（如 $a=b$，而不是 $a==b$）、使用 `` `a<<1` `` 或者 `$a\times 2$` 而不是 `$a<<1$`、使用 `$a\bmod b$` 代替 `$a\%b$`（如 $a\bmod b$，而不是 $a\%b$）等．

-   <span id="MATH-1.10">MATH-1.10</span>：公式中不要使用中括号连缀（即 C++ 高维数组的表示方式）而多使用下标．即 $a_{i,j,k}$ 而不是 $a[i][j][k]$．在公式中下标较复杂的情况下建议改用多元函数（$f(i,j,k)$）或内联代码格式．对于一元简单函数使用 `$f_i$`、`$f(i)$` 或 `$f[i]$` 均可．

-   <span id="MATH-1.11">MATH-1.11</span>：为了统一且书写方便，复杂度分析时大 $O$ 记号请直接使用 `$O()$` 而不是 `$\mathcal O()$`．

-   <span id="MATH-1.12">MATH-1.12</span>：在表示等价关系时，请使用 `$\iff$`，效果 $\iff$，而不是 `$\Leftrightarrow$`，效果 $\Leftrightarrow$．

-   <span id="MATH-1.13">MATH-1.13</span>：分段函数环境 `cases`  **只能有两列**（即一个 `&` 分隔符）．

-   <span id="MATH-1.14">MATH-1.14</span>：请不要滥用 LaTeX 公式．这不仅会造成页面加载缓慢（因为 MathJax 的效率低是出了名的），同时也会导致页面的排版混乱．我们通常使用 LaTeX 公式字体表示变量名称．我们的建议是，如非必要，尽量减少公式与普通正文字体的 **大量** 混合使用，如非必要，尽量不要使用公式，如：

    ```LaTeX
    我们将要学习 $Network-flow$ 中的 $SPFA$ 最小费用流，需要使用 $Edmonds–Karp$ 算法进行增广．
    ```

    就是一个典型的 **滥用公式字体** 的例子．（在页面中使用斜体请用 `*文本*` 表示．）

-   <span id="MATH-1.15">MATH-1.15</span>：请正确使用对应的 LaTeX 符号，尤其是公式中的希腊字母等特殊符号．如欧拉函数请使用 `$\varphi$`，圆的直径请使用 `$\Phi$`，黄金分割请使用 `$\phi$`．这些符号虽然同样表示希腊字母 Phi，但是在不同的环境下有不同的含义．切记 **不要使用输入法的插入特殊符号** 来插入这种符号．

    另外，由于 LaTeX 历史原因，空集的符号应为 `$\varnothing$` 而不是 `$\emptyset$`；其他的符号应参照 [数学符号表](./symbol.md) 书写．

我们可以使用一个表格来总结一下上述内容．注意本表格没有举出所有符号的用法，只给出常见的错误．类似的情况类比即可．

| 不符合规定的用法                     | 渲染效果              | 符合规定的用法                                  | 渲染效果                                |
| ---------------------------- | ----------------- | ---------------------------------------- | ----------------------------------- |
| `$log, ln, lg$`              | $log, ln, lg$     | `$\log$, $\ln$, $\lg$`                   | $\log$，$\ln$，$\lg$                  |
| `$sin, cos, tan$`            | $sin, cos, tan$   | `$\sin$, $\cos$, $\tan$`                 | $\sin$，$\cos$，$\tan$                |
| `$gcd, lcm$`                 | $gcd, lcm$        | `$\gcd$, $\operatorname{lcm}$`           | $\gcd$，$\operatorname{lcm}$         |
| `$e$, $\text{e}$, e`（自然对数的底） | $e$，$\text{e}$, e | `$\mathrm{e}$`                           | $\mathrm{e}$                        |
| `$i$, $\text{i}$, i`（虚数单位）   | $i$，$\text{i}$, i | `$\mathrm{i}$`                           | $\mathrm{i}$                        |
| `$ 小于 a 的质数 $`               | $小于 a 的质数$        | `小于 $a$ 的质数`                             | 小于 $a$ 的质数                          |
| `$...$`                      | $...$             | `$\cdots$, $\ldots$, $\vdots$, $\ddots$` | $\cdots$，$\ldots$，$\vdots$，$\ddots$ |
| `$a*b$`（两个数相乘）               | $a*b$             | `$a\times b$, $a\cdot b$`                | $a\times b$，$a\cdot b$              |
| `$SPFA$`（英文名称）               | $SPFA$            | `SPFA`                                   | SPFA                                |
| `$a==b$`                     | $a==b$            | `$a=b$`                                  | $a=b$                               |
| `$f[i][j][k]$`               | $f[i][j][k]$      | `$f_{i,j,k}$, $f(i,j,k)$`                | $f_{i,j,k}$，$f(i,j,k)$              |
| `$R,N^*$`（集合）                | $R,N^*$           | `$\mathbf{R}$, $\mathbf{N}^*$`           | $\mathbf{R}$，$\mathbf{N}^*$         |
| `$\emptyset$`                | $\emptyset$       | `$\varnothing$`                          | $\varnothing$                       |
| `$size$`                     | $size$            | `$\textit{size}$`                        | $\textit{size}$                     |

#### 对数学公式的附加格式要求

请注意，尽管上述输入公式的语法和真正的 LaTeX 排版系统非常相似，但 **MathJax 和 LaTeX 是两个完全没有关系的东西**，MathJax 仅仅使用了一部分与 LaTeX 非常相似的语法而已．实际上，二者之间有不少细节差别，而这些差别经常导致写出来的公式在二者之间不通用．

由于 **OI Wiki** 使用 LaTeX 排版引擎开发了 PDF 导出工具，因此有必要强调公式在 MathJax 和 LaTeX 之间的兼容性．**请各位在 Wiki 中书写数学公式时注意以下几点．**

这些规则已经向 MathJax 做了尽可能多的妥协．导出工具兼容了一部分原本仅能在 MathJax 中正常输出的写法．

-   <span id="MATH-2.1">MATH-2.1</span>：请使用 `\begin{aligned} ... \end{aligned}` 表示多行对齐的公式；

-   <span id="MATH-2.2">MATH-2.2</span>：如果这些多行对齐的公式需要 **编号**，请用 `align` 或 `equation` 环境；

-   <span id="MATH-2.3">MATH-2.3</span>：不要使用 `split`、`eqnarray` 环境；

-   <span id="MATH-2.4">MATH-2.4</span>：不要使用 `\lt`,`\gt` 来表示大于号和小于号，请直接使用 `<`，`>`；

-   <span id="MATH-2.5">MATH-2.5</span>：不要直接用 `\\` 换行（需要换行的公式，请套在 `aligned` 或其他多行环境下）；

-   <span id="MATH-2.6">MATH-2.6</span>：若要输出 LaTeX 符号 $\rm{\LaTeX}$，请用 `$\rm{\LaTeX}$`，而不是 `mathrm`；（`\LaTeX` 在 TeX 排版系统中是一个不能用于数学模式下的命令，而 `\mathrm` 又不能在普通模式下使用；另外，`\text` 命令虽然在 TeX 上正常输出，但是在 MathJax 中 `\text` 命令的参数会被原样输出，而不是按命令转义）；

-   <span id="MATH-2.7">MATH-2.7</span>：数学公式中的中文文字 **必须置于 `\text{}` 命令之中**，而变量、数字、运算符、函数名称则必须置于 `\text{}` 命令之外．**请不要在 `\text{}` 命令中嵌套数学公式**；

-   <span id="MATH-2.8">MATH-2.8</span>：使用 `array` 环境时请注意 **实际列数与对齐符号的数量保持一致**．例如下面的公式中，数据实际有 3 列（`&` 是列分隔符），因此需要 3 个对齐符号（`l`/`r`/`c` 分别表示左、右、居中对齐）．

    ```latex
    $$
    \begin{array}{lll}
    F_1=\{\frac{0}{1},&&\frac{1}{1}\}\\
    F_2=\{\frac{0}{1},&\frac{1}{2},&\frac{1}{1}\}\\
    \end{array}
    $$
    ```

#### 伪代码格式

伪代码具体格式没有严格要求，请参考算法导论或学术论文．注意不要写成 Python．

<span id="PCOD-1">PCOD-1</span>：Wiki 内使用 LaTeX 书写伪代码，整体处于 array 环境中，缩进使用 `$\qquad$`，文字描述使用 `$\text$`，关键字使用 `$\textbf$`，多字母变量使用 `$\textit$`，赋值使用 `$\gets$`．

参考示例：

$$
\begin{array}{l}
\textbf{Input. } \text{The edges of the graph } e , \text{ where each element in } e \text{ is } (u, v, w) \\
\text{ denoting that there is an edge between } u \text{ and } v \text{ weighted } w . \\
\textbf{Output. } \text{The edges of the MST of the input graph}. \\
\textbf{Method. } \\
\begin{array}{ll} 
1 &  \textit{result} \gets \varnothing \\
2 &  \text{sort } e \text{ into nondecreasing order by weight } w \\ 
3 &  \textbf{for} \text{ each } (u, v, w) \text{ in the sorted } e \\ 
4 &  \qquad \textbf{if } u \text{ and } v \text{ are not connected in the union-find set } \\
5 &  \qquad\qquad \text{connect } u \text{ and } v \text{ in the union-find set} \\
6 &  \qquad\qquad \textit{result} \gets \textit{result}\;\bigcup\ \{(u, v, w)\} \\
7 &  \textbf{return } \textit{result}
\end{array}
\end{array}
$$

```latex
$$
\begin{array}{l}
\textbf{Input. } \text{The edges of the graph } e , \text{ where each element in } e \text{ is } (u, v, w) \\
\text{ denoting that there is an edge between } u \text{ and } v \text{ weighted } w . \\
\textbf{Output. } \text{The edges of the MST of the input graph}. \\
\textbf{Method. } \\
\begin{array}{ll} 
1 &  \textit{result} \gets \varnothing \\
2 &  \text{sort } e \text{ into nondecreasing order by weight } w \\ 
3 &  \textbf{for} \text{ each } (u, v, w) \text{ in the sorted } e \\ 
4 &  \qquad \textbf{if } u \text{ and } v \text{ are not connected in the union-find set } \\
5 &  \qquad\qquad \text{connect } u \text{ and } v \text{ in the union-find set} \\
6 &  \qquad\qquad \textit{result} \gets \textit{result}\;\bigcup\ \{(u, v, w)\} \\
7 &  \textbf{return } \textit{result}
\end{array}
\end{array}
$$
```

#### 代码块的格式要求

代码块目前分为两种：片段和例题．

关于片段代码：

-   <span id="CODE-1.1">CODE-1.1</span>：若代码片段足够短且没有必要测试，可以直接在 Markdown 文档中修改．
-   <span id="CODE-1.2">CODE-1.2</span>：由于 Markdown 文档中内嵌的代码难以实现自动化测试，所以推荐使用例题代码的格式插入片段代码．可以选择 [多文件编译方案](https://github.com/OI-wiki/OI-wiki/pull/5729) 或 [Snippet Sections](https://facelessuser.github.io/pymdown-extensions/extensions/snippets/#snippet-sections) 语法：

    多文件编译方案示例：[冒泡排序](https://github.com/OI-wiki/OI-wiki/blob/c35defebff6cea072d6cfeb359642f6fd84e66c7/docs/basic/bubble-sort.md?plain=1#L48)．正文引用 [bubble-sort\_1.cpp](https://github.com/OI-wiki/OI-wiki/blob/c35defebff6cea072d6cfeb359642f6fd84e66c7/docs/basic/code/bubble-sort/bubble-sort_1.cpp)，测试代码放在 [bubble-sort\_1.aux1.cpp](https://github.com/OI-wiki/OI-wiki/blob/c35defebff6cea072d6cfeb359642f6fd84e66c7/docs/basic/code/bubble-sort/bubble-sort_1.aux1.cpp) 中．

    Snippet Sections 示例：[前缀和](https://github.com/OI-wiki/OI-wiki/blob/c7cf6d6de13b44757f1d0528e952349beb921f8a/docs/basic/prefix-sum.md?plain=1#L37)．正文中不需要引用 [prefix-sum\_1.cpp](https://github.com/OI-wiki/OI-wiki/blob/c7cf6d6de13b44757f1d0528e952349beb921f8a/docs/basic/code/prefix-sum/prefix-sum_1.cpp) 中的测试部分，所以选择插入主要的代码片段．

    **注意**：不要使用 [Snippet Lines](https://facelessuser.github.io/pymdown-extensions/extensions/snippets/#snippet-lines) 语法．

    为了提高代码复用率，您也可以将代码拆分成头文件，测试时在不同的测试代码里引用．如果正文中需要出现完整的测试代码作为例题的参考实现，那么正文中应该另外用 Snippet Sections 语法拼接成单文件代码，以便读者阅读．示例：[红黑树](https://github.com/OI-wiki/OI-wiki/blob/3b721e22ea60d59a2687a9b10555263de7bdc2f0/docs/ds/rbtree.md?plain=1#L218-L231)．

关于例题代码：

-   <span id="CODE-2.1">CODE-2.1</span>：例题代码的表示形式为 `--8<-- "path"`，代码均存储在 `path` 中．路径通常为 `docs/主题/code/内容/内容_编号.cpp`．

-   <span id="CODE-2.2">CODE-2.2</span>：修改例题代码时，请保证你的代码是正确的．例题代码均拥有一组测试数据，存储在 `/docs/主题/examples/内容/内容_编号.in/ans` 中．

如果你需要添加例题：

-   请在 `docs/主题/code/内容` 中添加你的例题代码，并编号．通常，该 `内容` 文件夹中已经有了一个或者多个代码．例子：如果需要修改 `dag.md` 的代码，那么路径为 `docs/dp/code/dag`，其中 `dp` 为主题，而 `dag` 为内容．

-   如果需要在所有例题的最后添加一个例题代码，请顺延目前的编号．比如已经存在了 `code/prefix-sum/prefix-sum_3.cpp`，如果需要在最后一个例题后继续添加一个例题，请将你的代码命名为 `prefix-sum_4.cpp` 并添加到 `docs/basic/code/prefix-sum` 中．

-   如果需要在文章中间添加一个例题代码，请插入并改变原先的编号．比如已经存在了 `prefix-sum_2.cpp` 和 `prefix-sum_3.cpp`，如果你需要在第二个例题和第三个例题中间再添加一个例题，请将你的代码命名为 `prefix-sum_3.cpp` 并将原先的 `prefix-sum_3.cpp` 改名为 `prefix-sum_4.cpp` 同时 **在 Markdown 文档和测试数据存放的文件夹中同步修改编号**．

-   **别忘记，你还要对你的代码添加一组测试数据，以保证这个代码是可以成功运行的．** 你需要在 `docs/主题/examples/内容` 文件夹中添加一组测试数据，将输入数据存储为 `内容_编号.in`，将标准答案存储为 `内容_编号.ans`．

-   最后，可以将代码添加到文档中了．请直接在文档中用添加代码块的格式，并将代码块内部直接写成 `--8<-- "你的代码路径"` 的格式就可以了．

**OI Wiki** 会对例题代码进行全平台测试，为保证您的代码能够顺利通过测试，请遵守如下规则：

-   <span id="CODE-3.1">CODE-3.1</span>：您的代码需要同时支持在 C++14、C++17、C++20 标准下编译和运行．
-   <span id="CODE-3.2">CODE-3.2</span>：不要使用 `<bits/stdc++.h>`、`<bits/extc++.h>` 等非标准头文件．
-   <span id="CODE-3.3">CODE-3.3</span>：标准答案文件不要有多余空格．
-   <span id="CODE-3.4">CODE-3.4</span>：不要使用 [代用记号](https://en.cppreference.com/w/cpp/language/operator_alternative#Alternative_tokens)．
-   <span id="CODE-3.5">CODE-3.5</span>：使用 [聚合初始化](https://en.cppreference.com/w/cpp/language/aggregate_initialization) 时，`object{args}` 不可写成 `(object){args}`．
-   <span id="CODE-3.6">CODE-3.6</span>：使用 [运算符重载](https://en.cppreference.com/w/cpp/language/operators) 时注意格式，如重载比较运算符时，若使用成员函数写法，则不可省略 `const` 限定符．
-   <span id="CODE-3.7">CODE-3.7</span>：不要使用类似 `#define int long long` 的宏定义．
-   <span id="CODE-3.8">CODE-3.8</span>：若您需要使用 C 风格的 [有格式输入/输出](https://en.cppreference.com/w/cpp/io/c#Formatted_input.2Foutput)，请特别留意格式指示符的写法：如 `size_t` 对应 `%zu`，`ptrdiff_t` 对应 `%td`．例如输出某 STL 容器的大小时，代码应类似 `printf("%zu", container.size());`．
-   <span id="CODE-3.9">CODE-3.9</span>：由于当前测试环境 libstdc++ 的 `<chrono>` 库有 [BUG](https://github.com/actions/runner-images/issues/8659)，所以请避免使用 `<chrono>` 库．
-   <span id="CODE-3.10">CODE-3.10</span>：由于 `long` 与 `unsigned long` 在某些测试环境下为 32 位，而在另一些测试环境下为 64 位，为确保各平台代码行为一致，故不推荐使用这两种类型．推荐使用 [定宽整数类型](../lang/var.md#定宽整数类型)．
-   <span id="CODE-3.11">CODE-3.11</span>：不建议使用 `__gcd`、`__int128`、`__builtin_` 系列函数等非标准内容．如果您需要使用，则需确保您的代码能通过全平台测试，如 [此代码](https://github.com/OI-wiki/OI-wiki/blob/4af83d6db6017f4c36db6d4a7583bbc3f6257484/docs/ds/code/tree-decompose/tree-decompose_1.cpp#L24-L47) 提供了 libstdc++ 中 [std::bitset](../lang/csl/bitset.md) 特有成员函数 `_Find_first()` 的全平台实现．

此外，为了提高代码的可读性，建议遵守 [CONT-10](#CONT-10)．

## 图解

可能上述要求把握起来有些困难，接下来我们给出一些图片来具体分析哪种格式应该使用，哪种不该使用：

### 例 1

![](./images/format-1.png)

将复杂的 LaTeX 公式使用行间格式，可以使得页面错落有致．但 **OI Wiki** 作为一个以中文为主体的站点，我们希望大部分纲领性的信息（如标题）尽量使用中文（除英文专有名词）．

### 例 2

![](./images/format-2.png)

较复杂度的 LaTeX 公式请注意等号的对齐，同时可以适当引用 Wiki 的页面 **链接** 来完善内容．

### 例 3

![](./images/format-3.png)

一般情况下，我们建议将引用的资料列在文末的 `##参考资料与注释` 一节，并在原句后面加上脚注，而不是直接给出链接．同时一定要避免使用 LaTeX 公式表达代码，上图中两个中括号就是不规范的写法．我们建议使用 `dp(i,j)` 或者 `dp_{i,j}`．

### 例 4

![](./images/format-4.png)

注意我们描述 **乘法** 的时候一般使用 `\times` 或者 `\cdot`，特殊情况（如卷积）下会使用 `*`（也可以写成 `\ast`）．标题是简洁的词组，但我们不希望正文部分由词组拼凑而成．上图中「两个要素」，建议更改为「动态规划的原理具有以下两个要素」，上下文保持连贯．可取的地方是，适当使用 **有序** 列表可以更有条理地表述内容．再次提醒，在使用列表的时候，每一项如果是一句话，需要在末位添加 **标点符号**．有序列表通常添加分号，在最后一项末位添加句号；无序列表统一添加句号．

### 例 5

![](./images/format-5.png)

适当引用 **图片** 可以增强文章易读性．使用 **伪代码** 的方式表达算法过程可以方便又简洁地描述算法过程，相比于直接贴模板代码更加好懂．

### 例 6

![](./images/format-6.png)

同样的问题，标题使用英文．并且在使用完括号后没有句号．另外，上图中的行间公式虽然没有使用括号，但是由于下标嵌套过多，使得最底层的下标字体很小，整个公式也并不美观．建议将 `son_{now,i}` 更换为 `son(now,i)`，或者把 `f_{now}` 替换为 `f(now)`．我们希望尽量控制上下标嵌套在两层以内（需要多次嵌套上标时建议使用 Knuth 箭头，如用 $2 \uparrow (2 \uparrow (2 \uparrow (2 \uparrow \cdots)))$ 代替 $2^{2^{2^{2^{\cdots}}}}$，《上帝造题的七分钟》）．

### 例 7

![](./images/format-7.png)

使用 MkDocs 扩展语法，让例题题面与算法描述区分开．将代码折叠，可以让文章更紧凑．（毕竟看 Wiki 的大多数是了解思路，除了模板代码需要阅读外，习题的代码大多可以折叠．）在描述函数操作时，使用行内代码和 LaTeX 公式都是不错的选择．

### 例 8

![](./images/format-8.png)

在文末罗列出参考文献，可以使页面的内容更严谨，真实可信．

## 外部链接

-   [标点符号用法（GB/T 15834—2011）](http://www.moe.gov.cn/jyb_sjzl/ziliao/A19/201001/W020190128580990138234.pdf)
-   [维基百科：格式手册/标点符号](https://zh.wikipedia.org/wiki/Wikipedia:%E6%A0%BC%E5%BC%8F%E6%89%8B%E5%86%8C/%E6%A0%87%E7%82%B9%E7%AC%A6%E5%8F%B7)
-   [中文文案排版指北（简体中文版）](https://mazhuang.org/wiki/chinese-copywriting-guidelines/)
-   [中文文案风格指南 - PDFE GUIDELINE](https://pdfe.github.io/GUIDELINE/#/others/copywriter)
-   [一份（不太）简短的 LATEX2ε 介绍或 106 分钟了解 LATEX2ε](https://github.com/CTeX-org/lshort-zh-cn/releases)
-   [中文出版物夹用英文的编辑规范](https://www.nppa.gov.cn/xxgk/fdzdgknr/hybz/202210/t20221004_445147.html)

## 参考资料与注释

[^note1]: （冒号）表示总结上文．

[^note2]: 科学技术名称的英文全称与其缩略形式间，应使用英文逗号．中文句子内夹用了用以注释、补充或说明的英文句子或语段，该英文句子或语段用中文圆括号标示．

[^note3]: 折叠框：参见 [Collapsible Blocks](https://squidfunk.github.io/mkdocs-material/reference/admonitions/#collapsible-blocks)，有时我们也用「Details 语法」指代该语法，因其从功能上与 HTML 中的 [`<details>` 元素](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/details) 功能一致．

[^note4]: 移至 [如何贡献](./htc.md)．

[^note5]: 该规范写入了 [编辑前须知](../edit-landing.md) 并发布了公告，并未写入本文档．

[^note6]: 选项卡：参见 [Content tabs](https://squidfunk.github.io/mkdocs-material/reference/content-tabs)．

[^ref1]: [cstdio stdio.h namespace](https://stackoverflow.com/questions/10460250/cstdio-stdio-h-namespace)

[^ref2]: [CCF 关于恢复 NOIP 竞赛的公告 - 中国计算机学会](https://www.ccf.org.cn/c/2020-01-21/694716.shtml)

[^ref3]: [我的公式为什么在目录里没有正常显示？好像双倍了](faq.md)

[^ref4]: [SVG|MDN](https://developer.mozilla.org/zh-CN/docs/Web/SVG)

[^webarchive]: [Save Page in Internet Archive](https://web.archive.org/save/)

[^apng]: [APNG](https://en.wikipedia.org/wiki/APNG)

[^intro-apng]: [OI-wiki/OI-wiki#3422](https://github.com/OI-wiki/OI-wiki/issues/3422)


## intro/htc.md

在文章开始之前，**OI Wiki** 项目组全体成员十分欢迎您为本项目贡献页面．正因为有了上百位像您一样的人，才有了 **OI Wiki** 的今天！

这篇文章将主要叙述参与 **OI Wiki** 编写的写作过程．请您在撰稿或者修正 Wiki 页面以前，仔细阅读以下内容，以帮助您完成更高质量的内容．

## 贡献指南

请您在编辑前查看 [OI Wiki 贡献指南](https://github.com/OI-wiki/OI-wiki/blob/master/.github/CONTRIBUTING.md) 和 [项目方针](./about.md#项目方针)，以更好地和社区贡献者进行合作、交流．

## 参与协作

???+ warning "Warning"
    在开始编写一段内容之前，请查阅 [Issues](https://github.com/OI-wiki/OI-wiki/issues)，确认没有别人在做相同的工作之后，开个 [新 issue](https://github.com/OI-wiki/OI-wiki/issues/new) 记录待编写的内容．

???+ tip "Tip"
    在 Issues 中也有很多待修复/解决的问题，尤其是我们的迭代计划（Iteration Plan）．从这里获取任务是一个很好的开始！

为了保证条目内容的专业性和准确性，我们建议您在编辑前先考虑以下几点：

1.  **选择您熟悉的领域**：请优先编辑那些与您的专业知识、学习背景或兴趣爱好相关的条目．这有助于您创作出高质量的内容．
2.  **谨慎对待新领域**：如果您对某个主题还处于初学阶段或不太了解，建议您先通过阅读、学习加深理解，待有一定把握后再动手编辑．
3.  **查阅相关资料**：为条目添加内容或进行修订时，建议您先查阅权威文献和资料，确保信息准确无误．也欢迎您在页面评论区或我们的社区提出问题，与其他编者交流讨论．

我们珍惜每位贡献者的热情和付出，也理解大家的专业水平不尽相同．让我们携手合作，共同呵护这个知识的乐园，用准确、专业的内容去帮助更多读者．期待您的贡献！在这里引用维基百科的一句话：

> 不要害怕编辑，勇于更新页面！[^ref1]

### 在 GitHub 上编辑

参与 **OI Wiki** 的编写 **需要** 一个 GitHub 账号（可以前往 [GitHub 的账号注册页面](https://github.com/signup) 页面注册），但 **不需要** 高超的 GitHub 技巧，即使你是一名新手，只要按照下面所述的步骤操作，也能够 **非常出色** 地完成编辑．

???+ tip "Tip"
    在你的更改被合并到 **OI Wiki** 的主仓库之前，你对 **OI Wiki** 的内容所作出的修改均不会出现在 **OI Wiki** 的主站上，所以无需担心你的修改会破坏 **OI Wiki** 上正在显示的内容．
    
    如果还是不放心，可以查看 [GitHub 的官方教程](https://skills.github.com/)．

#### 编辑单个页面内的内容

1.  在 **OI Wiki** 上找到对应页面；
2.  点击正文右上方（目录左侧）的 **「编辑此页」**（<i class="md-icon">edit</i>）按钮，在确认您已经阅读了本页面和 [格式手册](./format.md) 后点击按钮根据提示跳转到 GitHub 进行编辑；
3.  在编辑框内编写你想修改的内容．请注意，在修改和接下来的提交过程中，请 **关闭您的自动翻译软件**，因为它可能产生不必要的麻烦（例如您修改的文件有时会被其错误改名，从而影响目录结构）；
4.  编写完成后滚动到页面下方，按照本文中 [commit 信息格式规范](#commit-信息格式规范) 填写 commit 信息，之后点击 **Propose changes** 按钮提交修改．点击按钮后，GitHub 会自动帮你创建一份 **OI Wiki** 仓库的分支，并将你的提交添加到这个分支仓库．
5.  GitHub 会自动跳转到你的分支仓库的页面，此时页面上方会显示一个绿色的 **Create pull request** 按钮，点击后 GitHub 会跳转到一个创建 Pull Request 页面．向下滚动检查自己所作出的修改没有错误后，按照本文中 [Pull Request 信息格式规范](#pull-request-信息格式规范) 一节中的规范书写 Pull Request 信息，然后点击页面上的绿色的 **Create pull request** 按钮创建 Pull Request．
6.  不出意外的话，你的 Pull Request 就顺利提交到仓库，等待管理员审核并合并到主仓库中即可．

在等待合并的时间里，你可以给他人的 Pull Request 提意见、点赞或者点踩．如果有新消息，会在网页右上角出现提示，并附有邮件提醒（取决于个人设置中配置的通知方式）．

#### 编辑多个页面内的内容

如果你需要同时编辑互相无关联的多个页面的内容，请按照上方的 [编辑单个页面内的内容](#编辑单个页面内的内容) 一节一次修改所有页面．

1.  打开 [OI-Wiki/OI-Wiki](https://github.com/OI-Wiki/OI-Wiki) 仓库，点击键盘上的<kbd>.</kbd>按钮（或者将 URL 中的 `github.com` 更改为 `github.dev`）[^ref2]，进入 GitHub 的网页版 VS Code 编辑器；
2.  在编辑器中作出对页面源文件的更改，可以使用页面右上方的预览按钮（或按下<kbd>Ctrl+K</kbd><kbd>V</kbd>快捷键）在右侧打开预览界面；
3.  修改完成后使用左侧的 Source Control 选项卡，并按照本文中 [commit 信息格式规范](#commit-信息格式规范) 填写 commit 信息并提交，提交时会提示是否创建此仓库的分支，点击绿色的 **Fork Repository** 按钮即可．
4.  提交后会在网页上方的中央弹出一个提示框，在第一次的提示框内填写标题，第二次的提示框内填写此提交要提交到的仓库内分支名称，之后右下角会弹出一个提示框，内容类似于 `Created Pull Request #1 for OI-Wiki/OI-Wiki.`，点击蓝字链接即可查看该 Pull Request．

#### 向 Pull Request 追加更改

1.  打开 [OI-Wiki 的 Pull Request 列表](https://github.com/OI-wiki/OI-wiki/pulls)，找到您提交的 Pull Request 并点击．
2.  Pull Request 页面的标题下方将会有一段例如 `<您的ID> wants to merge x commits into OI-wiki:master from <您的ID>:patch-1` 的文字，点击 `<您的ID>:patch-1` 部分．
3.  您应该会被重定向到您的分支仓库中，而且文件列表左上角的分支名称是你提交 Pull Request 的分支名称（在本示例中应为 `patch-1`）．
4.  进行您需要的更改．
    -   如果您需要编辑单个文件或多个互相无关联的页面的内容，请直接找到你要的文件并进行更改，更改完成后滚动到页面下方，按照本文中 [commit 信息格式规范](#commit-信息格式规范) 填写 commit 信息，之后点击 **Commit changes** 按钮提交修改．
    -   如果您需要编辑多个文件，点击键盘上的<kbd>.</kbd>按钮（或者将 URL 中的 `github.com` 更改为 `github.dev`）[^ref2]，进入 GitHub 的网页版 VS Code 编辑器并作出更改．然后使用左侧的 Source Control 选项卡，并按照本文中 [commit 信息格式规范](#commit-信息格式规范) 填写 commit 信息并提交修改．
5.  这时你的更改会被自动追加在您的 Pull Request 中．

### 使用 Git 在本地进行编辑

???+ warning "Warning"
    对于一般用户，我们更推荐使用上方所述的 GitHub 的 Web 编辑器进行编辑．

虽然大多数情况下您可以直接在 GitHub 上进行编辑，但对于一些较为特殊的情况（如需要使用 GPG 签名），我们更推荐使用 Git 在本地进行编辑．

大致流程如下：

1.  将主仓库 Fork 到自己的仓库中；
2.  将 Fork 后的分支仓库克隆（clone）到本地；
3.  在本地进行修改后提交（commit）这些更改；
4.  将这些更改推送（push）到你克隆的分支仓库；
5.  提交 Pull Request 至主仓库．

详细的操作方式可以参考 [Git](../tools/git.md) 页面．

#### 向 Pull Request 追加更改

在 clone 下来的本地分支仓库中继续进行修改，并提交（commit）以及推送（push）这些更改即可．你的更改会被自动追加在 Pull Request 中．

### 在构建的网页中预览变更

在 Pull Request 页面下方可以找到测试页面，点击 netlify/oi-wiki/deploy-preview 一项的 Details 链接（如下图），可以进入自动构建的，由您变更后的页面供您预览．

![deploy\_preview](./images/deploy_preview.png)

### 对于目录和引用的变更

通常情况下，如果您需要添加一个新页面，或者修改已有页面在目录中的链接，您就需要对 [`mkdocs.yml`](https://github.com/OI-wiki/OI-wiki/blob/master/mkdocs.yml) 文件作出改动．

添加新页面可以参考既有的格式．但除非是进行重构或修正名词，否则 **我们不建议对既有页面的引用链接进行修改**，Pull Requests 中不必要的修改也将被驳回．

如果您坚持要修改链接，请注意更新 author 字段和重定向文件．

### author 字段

GitHub API 在文件目录变更后不能跟踪统计，所以我们在文件头手动维护了一个作者列表来解决这个问题．author 字段位于整个 Markdown 文件的开头，形如 `author: Ir1d, cjsoft`，相邻两个 ID 之间用逗号加空格隔开．这里的 ID 是 GitHub 的用户名，即 GitHub profile 的地址（例如 <https://github.com/Ir1d> 中的 `Ir1d`）．

修改链接时，需要将当前页面中的 contributors 逐一填入 author 字段．

### 重定向文件

在修改链接时，为了避免在站外引用时出现死链，需要修改重定向文件．

[`_redirects`](https://github.com/OI-wiki/OI-wiki/blob/master/docs/_redirects) 文件用于生成 [netlify 的配置](https://docs.netlify.com/routing/redirects/#syntax-for-the-redirects-file) 和 [用于跳转的文件](https://github.com/OI-wiki/OI-wiki/blob/master/scripts/gen_redirect.py)．

每一行表示一个重定向规则，分别写跳转的起点和终点的 url（不包含域名）：

```text
/path/to/src /path/to/desc
```

注：所有跳转均为 301 跳转，只有在修改目录中 url 造成死链的时候需要修改．

### Commit 信息格式规范

对于提交时需要填写的 commit 信息，请遵守以下几点基本要求：

1.  commit 摘要请简要描述这一次 commit 改动的内容．注意 commit 摘要的长度不要超过 50 字符，超出的部分会自动置于正文中．
2.  如果需要进一步描述本次 commit 内容，请在正文中详细说明．

对于 commit 摘要，推荐按照如下格式书写：

```text
<修改类型>(<文件名>): <修改的内容>
```

修改类型分为如下几类：

-   `feat`：用于添加内容的情况．
-   `fix`：用于修正现有内容错误的情况．
-   `refactor`：用于对一个页面进行重构（较大规模的更改）的情况．
-   `revert`：用于回退之前更改的情况．

### Pull Request 信息格式规范

对于 Pull Request，请遵守以下几点要求：

1.  标题请写明本次 PR 的目的（做了 **什么** 工作，修复了 **什么** 问题）．
2.  内容请简要叙述修改的内容．如果修复了一个 issue 的问题，请在内容中添加 `fix #xxxx` 字段，其中 `xxxx` 代表 issue 的编号．
3.  请您仔细阅读 [贡献指南](https://github.com/OI-wiki/OI-wiki/blob/master/.github/CONTRIBUTING.md) 和 [社区公约](https://github.com/OI-wiki/OI-wiki/blob/master/CODE_OF_CONDUCT.md)，并在同意后勾选 PR 模板中的框，表示您同意了以上指南和公约．

对于 Pull Request 的标题，推荐使用如下格式书写：

```plain
<修改类型>(<文件名>): <修改的内容> (<对应 issue 的编号>)
```

修改类型分为如下几类：

-   `feat`：用于添加内容的情况．
-   `fix`：用于修正现有内容错误的情况．
-   `refactor`：用于对一个页面进行重构（较大规模的更改）的情况．
-   `revert`：用于回退之前更改的情况．

示例：

-   `fix(ds/persistent-seg): 修改代码注释使描述更清晰`
-   `fix: tools/judger/index 不在目录中 (#3709)`
-   `feat(math/poly/fft): better proof`
-   `refactor(ds/stack): 整理页面内容`

### 协作流程

1.  在收到一个新的 Pull Request 之后，GitHub 会给 reviewer 发送邮件；
2.  与此同时，在 [GitHub Actions](https://github.com/OI-wiki/OI-wiki/actions) 和 [Netlify](https://app.netlify.com/sites/oi-wiki) 上会运行两组测试，它们会把进度同步在 PR 页面的下方．GitHub Actions 主要用来确认 PR 中内容的修改不会影响到网站构建的进程；Netlify 用来把 PR 中的更新构建出来，方便 reviewer 审核（在测试完成后点击 Details 可以了解更多）；
3.  reviewer 可能会发现问题，并提出 `review` 或 `suggested changes`（建议更改，显示为灰色图标）/`requested changes`（强制更改，显示为红色图标，只会在 reviewer 拥有 repo 写权限时出现）．一般来说，reviewer 也会附上建议和需要进行的更改，在这时，您将会需要继续向 Pull Request 追加其他更改．更改的方法可以参考 `在 GitHub 上编辑` 或者 `使用 Git 在本地进行编辑` 部分的 `向 Pull Request 追加更改` 部分．
4.  在足够多 reviewer 投票通过一个 PR 之后，这个 PR 才可以合并到 master 分支中；
5.  在合并到 master 分支之后，GitHub Actions 会重新构建一遍网站内容，并更新到 gh-pages 分支；
6.  这时服务器才会拉取 gh-pages 分支的更新，并重新部署最新版本的内容．

## 参考资料与注释

[^ref1]: [维基百科：新手入门/编辑](https://zh.wikipedia.org/wiki/Wikipedia:%E6%96%B0%E6%89%8B%E5%85%A5%E9%96%80/%E7%B7%A8%E8%BC%AF)

[^ref2]: [Web-based editor - GitHub Codespaces - GitHub Docs](https://docs.github.com/en/codespaces/developing-in-codespaces/web-based-editor)


## intro/mirrors.md

**OI Wiki** 部署在国外服务器上，有时可能会因为各种原因，出现访问不通畅的情况．

我们搭建了一个状态页：<https://status.oi-wiki.org>，用于监控 **OI Wiki** 站点的在线情况．如果你遇到了无法访问的问题，可以打开状态页，寻找可以连接的镜像站．

以下是一个 **OI Wiki** 的镜像站列表，可供选用：

-   **OI Wiki** 主站，线路：DMIT
    -   <https://oi-wiki.org>

-   维护者：**OI Wiki**，线路：阿里云，同步频率：与主站相同
    -   <http://oi-wiki.com>

-   维护者：**OI Wiki**，线路：Netlify，同步频率：与主站相同
    -   <https://demo.oi-wiki.org>

-   维护者：琴春（[vx.st](https://vx.st)），线路：AWS，同步频率：与主站相同
    -   <https://oi-wiki.net>
    -   <https://oi-wiki.wiki>
    -   <https://oi-wiki.win>
    -   <https://oi-wiki.xyz>
    -   <https://oiwiki.moe>
    -   <https://oiwiki.net>
    -   <https://oiwiki.org>
    -   <https://oiwiki.vx.st>
    -   <https://oiwiki.wiki>
    -   <https://oiwiki.win>
    -   <https://oiwiki.com>

-   维护者：Menci（[men.ci](https://men.ci)），线路：Azure + 阿里云 CDN，同步频率：与主站相同
    -   <https://oi.wiki>


## intro/symbol.md

本文规定了 **OI Wiki** 中数学符号的推荐写法，并给出了一些应用范例．

本文参考了 [GB/T 3102.11-1993](https://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno=3DE79450D562E62D41CB6E79FF411054)、[ISO 80000-2:2019](https://www.iso.org/standard/64973.html) 和《具体数学》的符号表修订，故基本与国内通行教材的符号体系和 OI 场景的惯用符号体系兼容．

符号的 LaTeX 写法请参考 [本文章的源代码](https://github.com/OI-wiki/OI-wiki/blob/master/docs/intro/symbol.md?plain=1)

## 数理逻辑

| 编号                          | 符号，表达式                    | 意义，等同表述                          | 备注与示例                                                                                                                                                                                               |
| --------------------------- | ------------------------- | -------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <span id="n1.1">n1.1</span> | $p \land q$               | $p$ 和 $q$ 的合取                    | $p$ 与 $q$.                                                                                                                                                                                          |
| <span id="n1.2">n1.2</span> | $p \lor q$                | $p$ 和 $q$ 的析取                    | $p$ 或 $q$;<br>此处的 "或" 是包含的，即若 $p$，$q$ 中有一个为真陈述，则 $p \lor q$ 为真．                                                                                                                                     |
| <span id="n1.3">n1.3</span> | $\lnot p$                 | $p$ 的否定                          | 非 $p$.                                                                                                                                                                                              |
| <span id="n1.4">n1.4</span> | $p \implies q$            | $p$ 蕴含 $q$;<br>若 $p$ 为真，则 $q$ 为真 | $q \impliedby p$ 和 $p \implies q$ 同义．                                                                                                                                                               |
| <span id="n1.5">n1.5</span> | $p \iff q$                | $p$ 等价于 $q$                      | $(p \implies q) \land (q \implies p)$ 和 $p \iff q$ 同义．                                                                                                                                              |
| <span id="n1.6">n1.6</span> | $(\forall~x \in A)~~p(x)$ | 对 $A$ 中所有的 $x$, 命题 $p(x)$ 均为真    | 如果从上下文中可以得知考虑的是哪个集合 $A$, 可以使用记号 $(\forall~x)~~p(x)$.<br>$\forall$ 称为全称量词．<br>$x \in A$ 的含义见 [n2.1](#n2.1).                                                                                          |
| <span id="n1.7">n1.7</span> | $(\exists~x \in A)~~p(x)$ | 存在一个属于 $A$ 的 $x$ 使得 $p(x)$ 为真    | 如果从上下文中可以得知考虑的是哪个集合 $A$, 可以使用记号 $(\exists~x)~~p(x)$.<br>$\exists$ 称为存在量词．<br>$x \in A$ 的含义见 [n2.1](#n2.1).<br>$(\exists!~x)~~p(x)$（唯一量词）用来表示恰有一个 $x$ 使得 $p(x)$ 为真．<br>$\exists!$ 也可以写作 $\exists^1$. |

## 集合论

| 编号                            | 符号，表达式                                                | 意义，等同表述                         | 备注与示例                                                                                                                                                                                                                                                                                                                                 |
| ----------------------------- | ----------------------------------------------------- | ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <span id="n2.1">n2.1</span>   | $x \in A$                                             | $x$ 属于 $A$，$x$ 是集合 $A$ 中的元素     | $A \ni x$ 和 $x \in A$ 同义．                                                                                                                                                                                                                                                                                                             |
| <span id="n2.2">n2.2</span>   | $y \notin A$                                          | $y$ 不属于 $A$，$y$ 不是集合 $A$ 中的元素   |                                                                                                                                                                                                                                                                                                                                       |
| <span id="n2.3">n2.3</span>   | $\{x_1, x_2, \dots, x_n\}$                            | 含元素 $x_1, x_2, \dots, x_n$ 的集合  | 也可写作 $\{x_i ~\vert~ i \in I\}$, 其中 $I$ 表示指标集．                                                                                                                                                                                                                                                                                         |
| <span id="n2.4">n2.4</span>   | $\{x \in A ~\vert~ p(x)\}$                            | $A$ 中使命题 $p(x)$ 为真的所有元素组成的集合    | 例如 $\{x \in \textbf{R} ~\vert~ x \geq 5\}$;<br>如果从上下文中可以得知考虑的是哪个集合 $A$，可以使用符号 $\{x ~\vert~ p(x)\}$（如在只考虑实数集时可使用 $\{x ~\vert~ x \geq 5\}$）<br>$\vert$ 也可以使用冒号替代，如 $\{x \in A : p(x)\}$.                                                                                                                                                |
| <span id="n2.5">n2.5</span>   | $\operatorname{card} A$;<br>$\vert A\vert$;<br>$\# A$ | $A$ 中的元素个数，$A$ 的基数              |                                                                                                                                                                                                                                                                                                                                       |
| <span id="n2.6">n2.6</span>   | $\varnothing$                                         | 空集                              | 不应使用 $\emptyset$.                                                                                                                                                                                                                                                                                                                     |
| <span id="n2.7">n2.7</span>   | $B \subseteq A$                                       | $B$ 包含于 $A$ 中，$B$ 是 $A$ 的子集     | $B$ 的每个元素都属于 $A$.<br>$\subset$ 也可用于该含义，但请参阅 [n2.8](#n2.8) 的说明．<br>$A \supseteq B$ 和 $B \subseteq A$ 同义．                                                                                                                                                                                                                               |
| <span id="n2.8">n2.8</span>   | $B \subset A$                                         | $B$ 真包含于 $A$ 中，$B$ 是 $A$ 的真子集   | $B$ 的每个元素都属于 $A$, 且 $A$ 中至少有一个元素不属于 $B$.<br>若 $\subset$ 的含义取 [n2.7](#n2.7), 则 [n2.8](#n2.8) 对应的符号应使用 $\subsetneq$.<br>$A \supset B$ 与 $B \subset A$ 同义．                                                                                                                                                                               |
| <span id="n2.9">n2.9</span>   | $A \cup B$                                            | $A$ 和 $B$ 的并集                   | $A \cup B := \{x ~\vert~ x \in A \lor x \in B\}$;<br>$:=$ 的定义参见 [n4.3](#n4.3)                                                                                                                                                                                                                                                         |
| <span id="n2.10">n2.10</span> | $A \cap B$                                            | $A$ 和 $B$ 的交集                   | $A \cap B := \{x ~\vert~ x \in A \land x \in B\}$;<br>$:=$ 的定义参见 [n4.3](#n4.3)                                                                                                                                                                                                                                                        |
| <span id="n2.11">n2.11</span> | $\displaystyle \bigcup\limits_{i=1}^n A_i$            | 集合 $A_1, A_2, \dots, A_n$ 的并集   | $\displaystyle \bigcup\limits_{i=1}^n A_i=A_1\cup A_2\cup \dots \cup A_n$;<br>也可使用 $\displaystyle \bigcup\nolimits_{i=1}^n$，$\displaystyle \bigcup\limits_{i\in I}$，$\displaystyle \bigcup\nolimits_{i\in I}$, 其中 $I$ 表示指标集；<br>进一步，令 $P(i)$ 为某个与 $i$ 相关的命题，可使用 $\displaystyle \bigcup_{P(i)} A_i$ 表示所有使 $P(i)$ 为真的 $i$ 对应的 $A_i$ 之并集 |
| <span id="n2.12">n2.12</span> | $\displaystyle \bigcap\limits_{i=1}^n A_i$            | 集合 $A_1, A_2, \dots, A_n$ 的交集   | $\displaystyle \bigcap\limits_{i=1}^n A_i=A_1\cap A_2\cap \dots \cap A_n$;<br>也可使用 $\displaystyle \bigcap\nolimits_{i=1}^n$，$\displaystyle \bigcap\limits_{i\in I}$，$\displaystyle \bigcap\nolimits_{i\in I}$, 其中 $I$ 表示指标集；<br>进一步，令 $P(i)$ 为某个与 $i$ 相关的命题，可使用 $\displaystyle \bigcap_{P(i)} A_i$ 表示所有使 $P(i)$ 为真的 $i$ 对应的 $A_i$ 之交集 |
| <span id="n2.13">n2.13</span> | $A \setminus B$                                       | $A$ 和 $B$ 的差集                   | $A \setminus B = \{x ~\vert~ x \in A \land x \notin B\}$;<br>不应使用 $A - B$;<br>当 $B$ 是 $A$ 的子集时也可使用 $\complement_A B$, 如果从上下文中可以得知考虑的是哪个集合 $A$，则 $A$ 可以省略．<br>不引起歧义的情况下也可使用 $\overline{B}$ 表示集合 $B$ 的补集．                                                                                                                               |
| <span id="n2.14">n2.14</span> | $(a, b)$                                              | 有序数对 $a$，$b$;<br>有序偶 $a$，$b$    | $(a, b) = (c, d)$ 当且仅当 $a = c$ 且 $b = d$.                                                                                                                                                                                                                                                                                             |
| <span id="n2.15">n2.15</span> | $(a_1, a_2, \dots, a_n)$                              | 有序 $n$ 元组                       | 参见 [n2.14](#n2.14).                                                                                                                                                                                                                                                                                                                   |
| <span id="n2.16">n2.16</span> | $A \times B$                                          | 集合 $A$ 和 $B$ 的笛卡尔积              | $A \times B = \{(x, y) ~\vert~ x \in A \land y \in B\}$.                                                                                                                                                                                                                                                                              |
| <span id="n2.17">n2.17</span> | $\displaystyle \prod\limits_{i=1}^{n} A_i$            | 集合 $A_1, A_2, \dots, A_n$ 的笛卡尔积 | $\displaystyle \prod\limits_{i=1}^{n} A_i=\{(x_1, x_2, \dots, x_n) ~\vert~ x_1 \in A_1, x_2 \in A_2, \dots, x_n \in A_n\}$;<br>$A \times A \times \dots \times A$ 记为 $A^n$, 其中 $n$ 是乘积中的因子数；<br>该符号的另一种用法参见 [n6.8](#n6.8)                                                                                                             |
| <span id="n2.18">n2.18</span> | $\mathrm{id}_A$                                       | $A\times A$ 的对角集                | $\mathrm{id}_A=\{(x, x)~\vert~x\in A\}$;<br>如果从上下文中可以得知考虑的是哪个集合 $A$, 则 $A$ 可以省略．                                                                                                                                                                                                                                                      |
| <span id="n2.19">n2.19</span> | $\mathbf{1}_A$                                        | 指示函数                            | $\mathbf{1}_A(a)=[a\in A]$，$[\cdot]$ 的定义参见 [n6.24](#n6.24)．                                                                                                                                                                                                                                                                           |
| <span id="n2.20">n2.20</span> | $\mathcal{P}(A)$;<br>$2^A$                            | 幂集                              | $\mathcal{P}(A)=\{S:S\subseteq A\}$                                                                                                                                                                                                                                                                                                   |

## 标准数集和区间

| 编号                            | 符号，表达式       | 意义，等同表述           | 备注与示例                                                                                                                                                                                       |
| ----------------------------- | ------------ | ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <span id="n3.1">n3.1</span>   | $\mathbf{N}$ | 自然数集              | $\mathbf{N} = \{0, 1, 2, 3, \dots\}$;<br>$\mathbf{N}^* = \mathbf{N}_+ = \{1, 2, 3, \dots\}$;<br>可用如下方式添加其他限制：$\mathbf{N}_{> 5} = \{n \in \mathbf{N} ~\vert~ n > 5\}$;<br>也可使用 $\mathbb{N}$. |
| <span id="n3.2">n3.2</span>   | $\mathbf{Z}$ | 整数集               | $\mathbf{Z}^* = \mathbf{Z}_+ = \{n \in \mathbf{Z} ~\vert~ n \ne 0\}$;<br>可用如下方式添加其他限制：$\mathbf{Z}_{> -3} = \{n \in \mathbf{Z} ~\vert~ n > -3\}$;<br>也可使用 $\mathbb{Z}$.                      |
| <span id="n3.3">n3.3</span>   | $\mathbf{Q}$ | 有理数集              | $\mathbf{Q}^* = \mathbf{Q}_+ = \{r \in \mathbf{Q} ~\vert~ r \ne 0\}$;<br>可用如下方式添加其他限制：$\mathbf{Q}_{< 0} = \{r \in \mathbf{Q} ~\vert~ r < 0\}$;<br>也可使用 $\mathbb{Q}$.                        |
| <span id="n3.4">n3.4</span>   | $\mathbf{R}$ | 实数集               | $\mathbf{R}^* = \mathbf{R}_+ = \{x \in \mathbf{R} ~\vert~ x \ne 0\}$;<br>可用如下方式添加其他限制：$\mathbf{R}_{> 0} = \{x \in \mathbf{R} ~\vert~ x > 0\}$;<br>也可使用 $\mathbb{R}$.                        |
| <span id="n3.5">n3.5</span>   | $\mathbf{C}$ | 复数集               | $\mathbf{C}^* = \mathbf{C}_+ = \{z \in \mathbf{C} ~\vert~ z \ne 0\}$;<br>也可使用 $\mathbb{C}$.                                                                                                 |
| <span id="n3.6">n3.6</span>   | $\mathbf{P}$ | （正）素数集            | $\mathbf{P} = \{2, 3, 5, 7, 11, 13, 17, \dots\}$;<br>也可使用 $\mathbb{P}$.                                                                                                                     |
| <span id="n3.7">n3.7</span>   | $[a, b]$     | $a$ 到 $b$ 的闭区间    | $[a, b] = \{x \in \mathbf{R} ~\vert~ a \leq x \leq b\}$.                                                                                                                                    |
| <span id="n3.8">n3.8</span>   | $(a, b]$     | $a$ 到 $b$ 的左开右闭区间 | $(a, b] = \{x \in \mathbf{R} ~\vert~ a < x \leq b\}$;<br>$(-\infty, b] = \{x \in \mathbf{R} ~\vert~ x \leq b\}$.                                                                            |
| <span id="n3.9">n3.9</span>   | $[a, b)$     | $a$ 到 $b$ 的左闭右开区间 | $[a, b) = \{x \in \mathbf{R} ~\vert~ a \leq x < b\}$;<br>$[a, +\infty) = \{x \in \mathbf{R} ~\vert~ a \leq x\}$.                                                                            |
| <span id="n3.10">n3.10</span> | $(a, b)$     | $a$ 到 $b$ 的开区间    | $(a, b) = \{x \in \mathbf{R} ~\vert~ a < x < b\}$;<br>$(-\infty, b) = \{x \in \mathbf{R} ~\vert~ x < b\}$;<br>$(a, +\infty) = \{x \in \mathbf{R} ~\vert~ a < x\}$.                          |

## 关系

| 编号                            | 符号，表达式               | 意义，等同表述            | 备注与示例                                                                                                         |
| ----------------------------- | -------------------- | ------------------ | ------------------------------------------------------------------------------------------------------------- |
| <span id="n4.1">n4.1</span>   | $a = b$              | $a$ 等于 $b$         | $\equiv$ 用于强调某等式是恒等式<br>该符号的另一个含义参见 [n4.18](#n4.18).                                                          |
| <span id="n4.2">n4.2</span>   | $a \ne b$            | $a$ 不等于 $b$        |                                                                                                               |
| <span id="n4.3">n4.3</span>   | $a := b$             | $a$ 定义为 $b$        | 参见 [n2.9](#n2.9),[n2.10](#n2.10)                                                                              |
| <span id="n4.4">n4.4</span>   | $a \approx b$        | $a$ 约等于 $b$        | 不排除相等．                                                                                                        |
| <span id="n4.5">n4.5</span>   | $a \simeq b$         | $a$ 渐近等于 $b$       | 例如：<br>当 $x\to a$ 时，$\dfrac{1}{\sin(x-a)} \simeq \dfrac{1}{x-a}$;<br>$x \to a$ 的含义参见 [n4.15](#n4.15).         |
| <span id="n4.6">n4.6</span>   | $a \propto b$        | $a$ 与 $b$ 成正比      | 也可使用 $a \sim b$.<br>$\sim$ 也用于表示等价关系．                                                                         |
| <span id="n4.7">n4.7</span>   | $M \cong N$          | $M$ 与 $N$ 全等       | 当 $M$ 和 $N$ 是点集（几何图形）时．<br>该符号也用于表示代数结构的同构．                                                                   |
| <span id="n4.8">n4.8</span>   | $a < b$              | $a$ 小于 $b$         |                                                                                                               |
| <span id="n4.9">n4.9</span>   | $b > a$              | $b$ 大于 $a$         |                                                                                                               |
| <span id="n4.10">n4.10</span> | $a \leq b$           | $a$ 小于等于 $b$       |                                                                                                               |
| <span id="n4.11">n4.11</span> | $b \geq a$           | $b$ 大于等于 $a$       |                                                                                                               |
| <span id="n4.12">n4.12</span> | $a \ll b$            | $a$ 远小于 $b$        |                                                                                                               |
| <span id="n4.13">n4.13</span> | $b \gg a$            | $b$ 远大于 $a$        |                                                                                                               |
| <span id="n4.14">n4.14</span> | $\infty$             | 无穷大                | 该符号 **不** 是数字．<br>也可以使用 $+\infty$，$-\infty$.                                                                  |
| <span id="n4.15">n4.15</span> | $x \to a$            | $x$ 趋近于 $a$        | 一般出现在极限表达式中．<br>$a$ 也可以为 $\infty$，$+\infty$，$-\infty$.                                                        |
| <span id="n4.16">n4.16</span> | $m \mid n$           | $m$ 整除 $n$         | 对整数 $m$，$n$:<br>$(\exists~k \in \mathbf{Z})~~m\cdot k = n$.                                                   |
| <span id="n4.17">n4.17</span> | $m \perp n$          | $m$ 与 $n$ 互质       | 对整数 $m$，$n$:<br>$(\nexists~k \in \mathbf{Z}_{>1})~~(k \mid m) \land (k \mid n)$;<br>该符号的另一种用法参见 [n5.2](#n5.2) |
| <span id="n4.18">n4.18</span> | $n \equiv k \pmod m$ | $n$ 模 $m$ 与 $k$ 同余 | 对整数 $n$，$k$，$m$:<br>$m \mid (n - k)$;<br>不要与 [n4.1](#n4.1) 中提到的相混淆．                                           |

## 初等几何学

| 编号                          | 符号，表达式                         | 意义，等同表述                             | 备注与示例                           |
| --------------------------- | ------------------------------ | ----------------------------------- | ------------------------------- |
| <span id="n5.1">n5.1</span> | $\parallel$                    | 平行                                  |                                 |
| <span id="n5.2">n5.2</span> | $\perp$                        | 垂直                                  | 该符号的另一种用法参见 [n4.17](#n4.17)     |
| <span id="n5.3">n5.3</span> | $\angle$                       | （平面）角                               |                                 |
| <span id="n5.4">n5.4</span> | $\overline{\mathrm{AB}}$       | 线段 $\mathrm{AB}$                    |                                 |
| <span id="n5.5">n5.5</span> | $\overrightarrow{\mathrm{AB}}$ | 有向线段 $\mathrm{AB}$                  |                                 |
| <span id="n5.6">n5.6</span> | $d(\mathrm{A}, \mathrm{B})$    | 点 $\mathrm{A}$ 和 $\mathrm{B}$ 之间的距离 | 即 $\overline{\mathrm{AB}}$ 的长度． |

## 运算符

| 编号                            | 符号，表达式                                                      | 意义，等同表述                                     | 备注与示例                                                                                                                                                                                                                                                                                |
| ----------------------------- | ----------------------------------------------------------- | ------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| <span id="n6.1">n6.1</span>   | $a + b$                                                     | $a$ 加 $b$                                   |                                                                                                                                                                                                                                                                                      |
| <span id="n6.2">n6.2</span>   | $a - b$                                                     | $a$ 减 $b$                                   |                                                                                                                                                                                                                                                                                      |
| <span id="n6.3">n6.3</span>   | $a \pm b$                                                   | $a$ 加或减 $b$                                 |                                                                                                                                                                                                                                                                                      |
| <span id="n6.4">n6.4</span>   | $a \mp b$                                                   | $a$ 减或加 $b$                                 | $-(a \pm b) = -a \mp b$.                                                                                                                                                                                                                                                             |
| <span id="n6.5">n6.5</span>   | $a \cdot b$;<br>$a \times b$;<br>$ab$                       | $a$ 乘 $b$                                   | 若出现小数点，则应只使用 $\times$;<br>部分用例参见 [n2.16](#n2.16),[n2.17](#n2.17),[n14.11](#n14.11),[n14.12](#n14.12)                                                                                                                                                                                 |
| <span id="n6.6">n6.6</span>   | $\dfrac{a}{b}$;<br>$a/b$;<br>$a:b$                          | $a$ 除以 $b$                                  | $\dfrac{a}{b}=a\cdot b^{-1}$;<br>可用 $:$ 表示同一量纲的数值的比率．<br>不应使用 $÷$.                                                                                                                                                                                                                   |
| <span id="n6.7">n6.7</span>   | $\displaystyle \sum\limits_{i=1}^n a_i$                     | $a_1 + a_2 + \dots + a_n$                   | 也可使用 $\displaystyle \sum\nolimits_{i=1}^n a_i$，$\displaystyle \sum\limits_i a_i$，$\displaystyle \sum\nolimits_i a_i$，$\displaystyle \sum a_i$；<br>令 $P(i)$ 为某个与 $i$ 相关的命题，可使用 $\displaystyle \sum_{P(i)} a_i$ 表示所有使 $P(i)$ 为真的 $i$ 对应的 $a_i$ 之和．                                     |
| <span id="n6.8">n6.8</span>   | $\displaystyle \prod\limits_{i=1}^n a_i$                    | $a_1 \cdot a_2 \cdot \dots \cdot a_n$       | 也可使用 $\displaystyle \prod\nolimits_{i=1}^n a_i$，$\displaystyle \prod\limits_i a_i$，$\displaystyle \prod\nolimits_i a_i$，$\displaystyle \prod a_i$；<br>令 $P(i)$ 为某个与 $i$ 相关的命题，可使用 $\displaystyle \prod_{P(i)} a_i$ 表示所有使 $P(i)$ 为真的 $i$ 对应的 $a_i$ 之积；<br>该符号的另一种用法参见 [n2.17](#n2.17) |
| <span id="n6.9">n6.9</span>   | $a^p$                                                       | $a$ 的 $p$ 次幂                                |                                                                                                                                                                                                                                                                                      |
| <span id="n6.10">n6.10</span> | $a^{1/2}$;<br>$\sqrt{a}$                                    | $a$ 的 $1/2$ 次方，$a$ 的平方根                     | 应避免使用 $\sqrt{}a$.                                                                                                                                                                                                                                                                    |
| <span id="n6.11">n6.11</span> | $a^{1/n}$;<br>$\sqrt[n]{a}$                                 | $a$ 的 $1/n$ 次幂，$a$ 的 $n$ 次根                 | 应避免使用 $\sqrt[n]{}a$.                                                                                                                                                                                                                                                                 |
| <span id="n6.12">n6.12</span> | $\bar{x}$;<br>$\bar{x}_a$                                   | $x$ 的算数均值                                   | 其他均值有：<br>调和均值 $\bar{x}_h$;<br>几何均值 $\bar{x}_g$;<br>二次均值/均方根 $\bar{x}_q$ 或 $\bar{x}_{rms}$.<br>$\bar{x}$ 也用于表示复数 $x$ 的共轭，参见 [n11.6](#n11.6).                                                                                                                                         |
| <span id="n6.13">n6.13</span> | $\operatorname{sgn} a$                                      | $a$ 的符号函数                                   | 对实数 $a$:<br>$\operatorname{sgn} a=1\quad (a>0)$;<br>$\operatorname{sgn} a=-1\quad (a<0)$;<br>$\operatorname{sgn} 0=0$;<br>参见 [n11.7](#n11.7).                                                                                                                                        |
| <span id="n6.14">n6.14</span> | $\inf M$                                                    | $M$ 的下确界                                    | 非空集合 $M$ 的最大下界．                                                                                                                                                                                                                                                                      |
| <span id="n6.15">n6.15</span> | $\sup M$                                                    | $M$ 的上确界                                    | 非空集合 $M$ 的最小上界．                                                                                                                                                                                                                                                                      |
| <span id="n6.16">n6.16</span> | $\lvert a\rvert$                                            | $a$ 的绝对值                                    | 也可使用 $\operatorname{abs} a$.                                                                                                                                                                                                                                                         |
| <span id="n6.17">n6.17</span> | $\lfloor a\rfloor$                                          | 向下取整<br>小于等于实数 $a$ 的最大整数                    | 例如：<br>$\lfloor 2.4\rfloor = 2$;<br>$\lfloor -2.4\rfloor = -3$.                                                                                                                                                                                                                      |
| <span id="n6.18">n6.18</span> | $\lceil a\rceil$                                            | 向上取整<br>大于等于实数 $a$ 的最小整数                    | 例如：<br>$\lceil 2.4\rceil = 3$;<br>$\lceil -2.4\rceil = -2$.                                                                                                                                                                                                                          |
| <span id="n6.19">n6.19</span> | $\min(a, b)$;<br>$\min\{a, b\}$                             | $a$ 和 $b$ 的最小值                              | 可推广到有限集中．<br>要表示无限集中的最小值建议使用 $\inf$, 参见 [n6.14](#n6.14)                                                                                                                                                                                                                              |
| <span id="n6.20">n6.20</span> | $\max(a, b)$;<br>$\max\{a, b\}$                             | $a$ 和 $b$ 的最大值                              | 可推广到有限集中．<br>要表示无限集中的最大值建议使用 $\sup$, 参见 [n6.15](#n6.15)                                                                                                                                                                                                                              |
| <span id="n6.21">n6.21</span> | $n \bmod m$                                                 | $n$ 模 $m$ 的余数                               | 对正整数 $n$，$m$:<br>$(\exists~q\in\mathbf{N}, r\in[0, m))~~n=qm+r$;<br>其中 $r=n \bmod m$.                                                                                                                                                                                                |
| <span id="n6.22">n6.22</span> | $\gcd(a, b)$;<br>$\gcd\{a, b\}$                             | 整数 $a$ 和 $b$ 的最大公因数                         | 可推广到有限集中．不引起歧义的情况下可写为 $(a, b)$.                                                                                                                                                                                                                                                      |
| <span id="n6.23">n6.23</span> | $\operatorname{lcm}(a, b)$;<br>$\operatorname{lcm}\{a, b\}$ | 整数 $a$ 和 $b$ 的最小公倍数                         | 可推广到有限集中．不引起歧义的情况下可写为 $[a, b]$;<br>$(a, b)[a, b]=\lvert ab\rvert$.                                                                                                                                                                                                                   |
| <span id="n6.24">n6.24</span> | $[P]$                                                       | Iverson 括号                                  | 若命题 $P$ 为真，则 $[P]=1$，否则 $[P]=0$．                                                                                                                                                                                                                                                     |
| <span id="n6.25">n6.25</span> | $a\uparrow b$；<br>$a\uparrow^{n} b$                         | Knuth 箭头                                    | 对非负整数 $a,b,n$：<br>$a\uparrow^{n} b=a~\underbrace{\uparrow\dots\uparrow}_{n \text{ times}}~b$；<br>$a\uparrow^{0} b=ab$；<br>$a\uparrow^{1} b=a\uparrow b=a^b$；<br>$a\uparrow^{n} 0=1\quad(n>0)$；<br>$a\uparrow^{n}b=a\uparrow^{n-1}(a\uparrow^{n}(b-1))$.                              |
| <span id="n6.26">n6.26</span> | $[x^n]f(x)$                                                 | 多项式/形式幂级数/形式 Laurent 级数 $f(x)$ 中 $x^n$ 项的系数 | 若 $\displaystyle f(x)=\sum_{i} a_ix^i$，则 $[x^n]f(x)=a_n$；<br>可推广到多元情况，如若 $\displaystyle f(x,y)=\sum_{i,j}a_{i,j}x^iy^j$，则 $[x^ny^m]f(x,y)=a_{n,m}$.                                                                                                                                  |

## 组合数学

本节中的 $n$ 和 $k$ 是自然数，$a$ 是复数，且 $k\leq n$.

| 编号                          | 符号，表达式                             | 意义，等同表述        | 备注与示例                                                                                                                                         |
| --------------------------- | ---------------------------------- | -------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| <span id="n7.1">n7.1</span> | $n!$                               | 阶乘             | $n!=\prod_{k=1}^n k=1\cdot 2\cdot 3\cdot \dots \cdot n\quad (n>0)$;<br>$0!=1$.                                                                |
| <span id="n7.2">n7.2</span> | $a^{\underline{k}}$;<br>$(a)_{-k}$ | 下降阶乘幂          | $a^{\underline{k}}=a\cdot(a-1)\cdot \dots \cdot(a-k+1)\quad (k>0)$;<br>$a^{\underline{0}}=1$;<br>$n^{\underline{k}}=\dfrac{n!}{(n-k)!}$.      |
| <span id="n7.3">n7.3</span> | $a^{\overline{k}}$;<br>$(a)_{+k}$  | 上升阶乘幂          | $a^{\overline{k}}=a\cdot(a+1)\cdot \dots \cdot(a+k-1)\quad (k>0)$;<br>$a^{\overline{0}}=1$;<br>$n^{\overline{k}}=\dfrac{(n+k-1)!}{(n-1)!}$.   |
| <span id="n7.4">n7.4</span> | $\dbinom{n}{k}$                    | 组合数            | $\dbinom{n}{k}=\dfrac{n!}{k!(n-k)!}$.                                                                                                         |
| <span id="n7.5">n7.5</span> | $\displaystyle{n\brack k}$         | 第一类 Stirling 数 | $\displaystyle{n+1\brack k}=n{n\brack k}+{n\brack k-1}$;<br>$\displaystyle x^{\overline{n}}=\sum_{k=0}^n{n\brack k}x^k$.                      |
| <span id="n7.6">n7.6</span> | $\displaystyle{n\brace k}$         | 第二类 Stirling 数 | $\displaystyle{n\brace k}=\frac{1}{k!}\sum_{i=0}^k(-1)^i\binom{k}{i}(k-i)^n$;<br>$\displaystyle\sum_{k=0}^n{n\brace k}x^{\underline{k}}=x^n$. |

## 函数

| 编号                            | 符号，表达式                                                                    | 意义，等同表述                                                    | 备注与示例                                                                                                                                                                                                                                                                                                                                                       |
| ----------------------------- | ------------------------------------------------------------------------- | ---------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <span id="n8.1">n8.1</span>   | $f$                                                                       | 函数                                                         |                                                                                                                                                                                                                                                                                                                                                             |
| <span id="n8.2">n8.2</span>   | $f(x)$，$f(x_1, \dots, x_n)$                                               | 函数 $f$ 在 $x$ 处的值<br>函数 $f$ 在 $(x_1, \dots, x_n)$ 处的值       |                                                                                                                                                                                                                                                                                                                                                             |
| <span id="n8.3">n8.3</span>   | $\operatorname{dom} f$                                                    | $f$ 的定义域                                                   | 也可使用 $\mathrm{D}(f)$.                                                                                                                                                                                                                                                                                                                                       |
| <span id="n8.4">n8.4</span>   | $\operatorname{ran} f$                                                    | $f$ 的值域                                                    | 也可使用 $\mathrm{R}(f)$.                                                                                                                                                                                                                                                                                                                                       |
| <span id="n8.5">n8.5</span>   | $f:A\to B$                                                                | $f$ 是 $A$ 到 $B$ 的映射                                        | $\operatorname{dom} f=A$ 且 $(\forall~x \in\operatorname{dom} f)~~ f(x) \in B$.                                                                                                                                                                                                                                                                              |
| <span id="n8.6">n8.6</span>   | $x\mapsto T(x), x\in A$                                                   | 将所有 $x\in A$ 映射到 $T(x)$ 的函数                                | $T(x)$ 仅用于定义，用来表示某个参数为 $x\in A$ 的某个函数值．若这个函数为 $f$, 则对所有 $x\in A$ 均有 $f(x)=T(x)$. 因此 $T(x)$ 通常用来定义函数 $f$.<br>例如：<br>$x\mapsto 3x^2y, x\in[0, 2]$;<br>这是由 $3x^2y$ 定义的一个关于 $x$ 的二次函数．若未引入函数符号，则用 $3x^2y$ 表示该函数                                                                                                                                                 |
| <span id="n8.7">n8.7</span>   | $f^{-1}$                                                                  | $f$ 的反函数                                                   | 函数 $f$ 的反函数 $f^{-1}$ 有定义当且仅当 $f$ 是单射．<br>若 $f$ 是单射，则 $\operatorname{dom}\left(f^{-1}\right) = \operatorname{ran} f$，$\operatorname{ran}\left(f^{-1}\right) = \operatorname{dom} f$, 且 $(\forall~x\in\operatorname{dom} f)~~f^{-1}(f(x)) = x$.<br>不要与函数的倒数 $f(x)^{-1}$ 混淆．                                                                                   |
| <span id="n8.8">n8.8</span>   | $g\circ f$                                                                | $f$ 和 $g$ 的复合函数                                            | $(g\circ f)(x)=g(f(x))$.                                                                                                                                                                                                                                                                                                                                    |
| <span id="n8.9">n8.9</span>   | $f:x\mapsto y$                                                            | $f(x)=y$，$f$ 将 $x$ 映射到 $y$                                 |                                                                                                                                                                                                                                                                                                                                                             |
| <span id="n8.10">n8.10</span> | $f\vert_a^b$;<br>$f(\dots, u, \dots)\vert_{u=a}^{u=b}$                    | $f(b)-f(a)$;<br>$f(\dots, b, \dots)-f(\dots, a, \dots)$    | 主要用于定积分的计算中．                                                                                                                                                                                                                                                                                                                                                |
| <span id="n8.11">n8.11</span> | $\displaystyle \lim\limits_{x\to a}f(x)$;<br>$\lim\nolimits_{x\to a}f(x)$ | 当 $x$ 趋近于 $a$ 时 $f(x)$ 的极限                                 | $\lim\nolimits_{x\to a}f(x)=b$ 可以写成 $f(x)\to b\quad (x \to a)$.<br>右极限和左极限的符号分别为 $\lim\nolimits_{x\to a+}f(x)$ 和<br>$\lim\nolimits_{x\to a-}f(x)$.                                                                                                                                                                                                          |
| <span id="n8.12">n8.12</span> | $f(x) = O(g(x))$                                                          | $\lvert f(x)/g(x)\rvert$ 在上下文隐含的限制中有上界，$f(x)$ 的阶不高于 $g(x)$ | 当 $f/g$ 与 $g/f$ 均有界时称 $f$ 与 $g$ 是同阶的．<br>使用符号 "$=$" 是出于历史原因，其在此处不表示等价，因为不满足传递性．<br>例如：<br>$\sin x=O(x)\quad (x\to 0)$.                                                                                                                                                                                                                                      |
| <span id="n8.13">n8.13</span> | $f(x) = o(g(x))$                                                          | 在上下文隐含的限制中有 $f(x)/g(x)\to 0$，$f(x)$ 的阶高于 $g(x)$            | 使用符号 "$=$" 是出于历史原因，其在此处不表示等价，因为不满足传递性．<br>例如：<br>$\cos x=1+o(x)\quad (x\to 0)$.                                                                                                                                                                                                                                                                             |
| <span id="n8.14">n8.14</span> | $\Delta f$                                                                | $f$ 的有限增量                                                  | 上下文隐含的两函数值的差分．例如：<br>$\Delta x=x_2-x_1$;<br>$\Delta f(x)=f(x_2)-f(x_1)$.                                                                                                                                                                                                                                                                                    |
| <span id="n8.15">n8.15</span> | $\dfrac{\mathrm{d}f}{\mathrm{d}x}$;<br>$f'$                               | $f$ 对 $x$ 的导（函）数                                           | 仅用于一元函数．<br>可以显式指明自变量，如 $\dfrac{\mathrm{d}f(x)}{\mathrm{d}x}$，$f'(x)$.                                                                                                                                                                                                                                                                                      |
| <span id="n8.16">n8.16</span> | $\left(\dfrac{\mathrm{d}f}{\mathrm{d}x}\right)_{x=a}$;<br>$f'(a)$         | $f$ 在 $a$ 处的导（函）数值                                         | 参见 [n8.15](#n8.15)                                                                                                                                                                                                                                                                                                                                          |
| <span id="n8.17">n8.17</span> | $\dfrac{\mathrm{d}^n f}{\mathrm{d}x^n}$;<br>$f^{(n)}$                     | $f$ 对 $x$ 的 $n$ 阶导（函）数                                     | 仅用于一元函数．<br>可以显式指明自变量，如 $\dfrac{\mathrm{d}^n f(x)}{\mathrm{d}x^n}$，$f^{(n)}(x)$.<br>可用 $f''$ 和 $f'''$ 分别表示 $f^{(2)}$ 和 $f^{(3)}$.                                                                                                                                                                                                                           |
| <span id="n8.18">n8.18</span> | $\dfrac{\partial f}{\partial x}$;<br>$f_x$                                | $f$ 对 $x$ 的偏导数                                             | 仅用于多元函数．<br>可以显式指明自变量，如 $\dfrac{\partial f(x, y, \dots)}{\partial x}$，$f_x(x, y, \dots)$.<br>可以扩展到高阶，如 $f_{xx}=\dfrac{\partial^2 f}{\partial x^2}=\dfrac{\partial}{\partial x}\left(\dfrac{\partial f}{\partial x}\right)$;<br>$f_{xy}=\dfrac{\partial^2 f}{\partial y\partial x}=\dfrac{\partial}{\partial y}\left(\dfrac{\partial f}{\partial x}\right)$. |
| <span id="n8.19">n8.19</span> | $\dfrac{\partial(f_1, \dots, f_m)}{\partial(x_1, \dots, x_n)}$            | Jacobi 矩阵                                                  | *参见*[^n8.19-ref1]                                                                                                                                                                                                                                                                                                                                           |
| <span id="n8.20">n8.20</span> | $\mathrm{d}f$                                                             | $f$ 的全微分                                                   | $\mathrm{d}f(x, y, \dots)=\dfrac{\partial f}{\partial x}\mathrm{d}x+\dfrac{\partial f}{\partial y}\mathrm{d}y+\dots$.                                                                                                                                                                                                                                       |
| <span id="n8.21">n8.21</span> | $\delta f$                                                                | $f$ 的（无穷小）变分                                               |                                                                                                                                                                                                                                                                                                                                                             |
| <span id="n8.22">n8.22</span> | $\displaystyle \int f(x)\mathrm{d}x$                                      | $f$ 的不定积分                                                  |                                                                                                                                                                                                                                                                                                                                                             |
| <span id="n8.23">n8.23</span> | $\displaystyle \int\limits_a^b f(x)\mathrm{d}x$                           | $f$ 从 $a$ 到 $b$ 的定积分                                       | 也可使用 $\displaystyle \int\nolimits_a^b f(x)\mathrm{d}x$;<br>定积分还可以定义在更一般的域上．如 $\displaystyle\int\limits_C$，$\displaystyle\int\limits_S$，$\displaystyle\int\limits_V$，$\displaystyle\oint$, 分别表示在曲线 $C$, 曲面 $S$, 三维区域 $V$, 和闭曲线或曲面上的定积分．<br>多重积分可写成 $\displaystyle\iint$，$\displaystyle\iiint$ 等．                                                             |
| <span id="n8.24">n8.24</span> | $f*g$                                                                     | 函数 $f$ 和 $g$ 的卷积                                           | $\displaystyle (f*g)(x)=\int\limits_{-\infty}^{\infty}f(y)g(x-y)\mathrm{d}y$.                                                                                                                                                                                                                                                                               |

[^n8.19-ref1]: $\dfrac{\partial(f_1, \dots, f_m)}{\partial(x_1, \dots, x_n)}=\begin{pmatrix}\dfrac{\partial f_1}{\partial x_1}&\cdots&\dfrac{\partial f_1}{\partial x_n}\\\vdots&\ddots&\vdots\\\dfrac{\partial f_m}{\partial x_1}&\cdots&\dfrac{\partial f_m}{\partial x_n}\end{pmatrix}$; 矩阵的定义参见 [n12.1](#n12.1)

## 指数和对数函数

$x$ 可以是复数．

| 编号                          | 符号，表达式                      | 意义，等同表述                      | 备注与示例                                                                                                          |
| --------------------------- | --------------------------- | ---------------------------- | -------------------------------------------------------------------------------------------------------------- |
| <span id="n9.1">n9.1</span> | $\mathrm{e}$                | 自然对数的底                       | $\displaystyle \mathrm{e}=\lim\limits_{n\to\infty}\left(1+\frac{1}{n}\right)^n=2.718~281~8\dots$;<br>不要写成 $e$. |
| <span id="n9.2">n9.2</span> | $a^x$                       | $x$ 的指数函数（以 $a$ 为底）          | 参见 [n6.9](#n6.9).                                                                                              |
| <span id="n9.3">n9.3</span> | $\mathrm{e}^x$;<br>$\exp x$ | $x$ 的指数函数（以 $\mathrm{e}$ 为底） |                                                                                                                |
| <span id="n9.4">n9.4</span> | $\log_a x$                  | $x$ 的以 $a$ 为底的对数             | 当底数不需要指定的时候可以使用 $\log x$.<br>不应用 $\log x$ 替换 $\ln x$，$\lg x$，$\operatorname{lb} x$ 中的任意一个．                     |
| <span id="n9.5">n9.5</span> | $\ln x$                     | $x$ 的自然对数                    | $\ln x = \log_{\mathrm{e}} x$;<br>参见 [n9.4](#n9.4).                                                            |
| <span id="n9.6">n9.6</span> | $\lg x$                     | $x$ 的常用对数                    | $\lg x = \log_{10} x$;<br>参见 [n9.4](#n9.4).                                                                    |
| <span id="n9.7">n9.7</span> | $\operatorname{lb} x$       | $x$ 的以 $2$ 为底的对数             | $\operatorname{lb} x = \log_2 x$;<br>参见 [n9.4](#n9.4).                                                         |

## 三角函数和双曲函数

| 编号                              | 符号，表达式                    | 意义，等同表述    | 备注与示例                                                                                                                                                    |
| ------------------------------- | ------------------------- | ---------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <span id="n10.1">n10.1</span>   | $\pi$                     | 圆周率        | $\pi = 3.141~592~6\dots$.                                                                                                                                |
| <span id="n10.2">n10.2</span>   | $\sin x$                  | $x$ 的正弦    | $\sin x=\dfrac{\mathrm{e}^{\mathrm{i}x}-\mathrm{e}^{-\mathrm{i}x}}{2\mathrm{i}}$;<br>$(\sin x)^n$，$(\cos x)^n$($n\geq 2$) 等通常写为 $\sin^n x$，$\cos^n x$ 等． |
| <span id="n10.3">n10.3</span>   | $\cos x$                  | $x$ 的余弦    | $\cos x = \sin(x + \pi/2)$.                                                                                                                              |
| <span id="n10.4">n10.4</span>   | $\tan x$                  | $x$ 的正切    | $\tan x = \sin x/\cos x$;<br>不可使用 $\operatorname{tg} x$.                                                                                                 |
| <span id="n10.5">n10.5</span>   | $\cot x$                  | $x$ 的余切    | $\cot x = 1/\tan x$;<br>不可使用 $\operatorname{ctg} x$.                                                                                                     |
| <span id="n10.6">n10.6</span>   | $\sec x$                  | $x$ 的正割    | $\sec x = 1/\cos x$.                                                                                                                                     |
| <span id="n10.7">n10.7</span>   | $\csc x$                  | $x$ 的余割    | $\csc x = 1/\sin x$;<br>不可使用 $\operatorname{cosec} x$.                                                                                                   |
| <span id="n10.8">n10.8</span>   | $\arcsin x$               | $x$ 的反正弦   | $y = \arcsin x \iff x = \sin y\quad (-\pi/2 \leq y \leq \pi/2)$.                                                                                         |
| <span id="n10.9">n10.9</span>   | $\arccos x$               | $x$ 的反余弦   | $y = \arccos x \iff x = \cos y\quad (0 \leq y \leq \pi)$.                                                                                                |
| <span id="n10.10">n10.10</span> | $\arctan x$               | $x$ 反正切    | $y = \arctan x \iff x = \tan y\quad (-\pi/2 \leq y \leq \pi/2)$;<br>不可使用 $\operatorname{arctg} x$.                                                       |
| <span id="n10.11">n10.11</span> | $\operatorname{arccot} x$ | $x$ 反余切    | $y = \operatorname{arccot} x \iff x = \cot y\quad (0 \leq y \leq \pi)$;<br>不可使用 $\operatorname{arcctg} x$.                                               |
| <span id="n10.12">n10.12</span> | $\operatorname{arcsec} x$ | $x$ 反正割    | $y = \operatorname{arcsec} x \iff x = \sec y\quad (0\leq y \leq \pi, y\ne \pi/2)$.                                                                       |
| <span id="n10.13">n10.13</span> | $\operatorname{arccsc} x$ | $x$ 的反余割   | $y = \operatorname{arccsc} x \iff x = \csc y\quad (-\pi/2 \leq y \leq \pi/2, y\ne 0)$;<br>不可使用 $\operatorname{arccosec} x$.                              |
| <span id="n10.14">n10.14</span> | $\sinh x$                 | $x$ 的双曲正弦  | $\sinh x=\dfrac{\mathrm{e}^x-\mathrm{e}^{-x}}{2}$;<br>不可使用 $\operatorname{sh} x$.                                                                        |
| <span id="n10.15">n10.15</span> | $\cosh x$                 | $x$ 的双曲余弦  | $\cosh^2 x = \sinh^2 x + 1$;<br>不可使用 $\operatorname{ch} x$.                                                                                              |
| <span id="n10.16">n10.16</span> | $\tanh x$                 | $x$ 的双曲正切  | $\tanh x = \sinh x/\cosh x$;<br>不可使用 $\operatorname{th} x$.                                                                                              |
| <span id="n10.17">n10.17</span> | $\coth x$                 | $x$ 的双曲余切  | $\coth x = 1/\tanh x$.                                                                                                                                   |
| <span id="n10.18">n10.18</span> | $\operatorname{sech} x$   | $x$ 的双曲正割  | $\operatorname{sech} x = 1/\cosh x$.                                                                                                                     |
| <span id="n10.19">n10.19</span> | $\operatorname{csch} x$   | $x$ 的双曲余割  | $\operatorname{csch} x = 1/\sinh x$;<br>不可使用 $\operatorname{cosech} x$.                                                                                  |
| <span id="n10.20">n10.20</span> | $\operatorname{arsinh} x$ | $x$ 的反双曲正弦 | $y = \operatorname{arsinh} x \iff x = \sinh y$;<br>不可使用 $\operatorname{arsh} x$.                                                                         |
| <span id="n10.21">n10.21</span> | $\operatorname{arcosh} x$ | $x$ 的反双曲余弦 | $y = \operatorname{arcosh} x \iff x = \cosh y\quad (y \geq 0)$;<br>不可使用 $\operatorname{arch} x$.                                                         |
| <span id="n10.22">n10.22</span> | $\operatorname{artanh} x$ | $x$ 的反双曲正切 | $y = \operatorname{artanh} x \iff x = \tanh y$;<br>不可使用 $\operatorname{arth} x$.                                                                         |
| <span id="n10.23">n10.23</span> | $\operatorname{arcoth} x$ | $x$ 的反双曲余切 | $y = \operatorname{arcoth} x \iff x = \coth y\quad (y \ne 0)$.                                                                                           |
| <span id="n10.24">n10.24</span> | $\operatorname{arsech} x$ | $x$ 的反双曲正割 | $y = \operatorname{arsech} x \iff x = \operatorname{sech} y\quad (y \geq 0)$.                                                                            |
| <span id="n10.25">n10.25</span> | $\operatorname{arcsch} x$ | $x$ 的反双曲余割 | $y = \operatorname{arcsch} x \iff x = \operatorname{csch} y\quad (y \geq 0)$;<br>不可使用 $\operatorname{arcosech} x$.                                       |

## 复数

| 编号                            | 符号，表达式                 | 意义，等同表述    | 备注与示例                                                                                                                                                                                                  |
| ----------------------------- | ---------------------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| <span id="n11.1">n11.1</span> | $\mathrm{i}$           | 虚数单位       | $\mathrm{i}^2 = -1$;<br>不可使用 $i$ 或 `i`                                                                                                                                                                 |
| <span id="n11.2">n11.2</span> | $\operatorname{Re} z$  | $z$ 的实部    | 参见 [n11.3](#n11.3).                                                                                                                                                                                    |
| <span id="n11.3">n11.3</span> | $\operatorname{Im} z$  | $z$ 的虚部    | 若 $z = x + \mathrm{i} y\quad (x, y\in\mathbf{R})$, 则 $x = \operatorname{Re} z$，$y = \operatorname{Im} z$.                                                                                              |
| <span id="n11.4">n11.4</span> | $\lvert z\rvert$       | $z$ 的模     | $\lvert z\rvert=\sqrt{(\operatorname{Re} z)^2+(\operatorname{Im} z)^2}$.                                                                                                                               |
| <span id="n11.5">n11.5</span> | $\arg z$               | $z$ 的辐角    | 若 $z = r \mathrm{e}^{\mathrm{i}\varphi}$, 其中 $r = \lvert z\rvert$ 且 $-\pi < \varphi \leq \pi$, 则 $\varphi = \arg z$.<br>$\operatorname{Re} z = r \cos \varphi$，$\operatorname{Im} z = r \sin \varphi$. |
| <span id="n11.6">n11.6</span> | $\bar{z}$;<br>$z^*$    | $z$ 的复共轭   | $\bar{z}=\operatorname{Re}z-\mathrm{i}\operatorname{Im}z$.                                                                                                                                             |
| <span id="n11.7">n11.7</span> | $\operatorname{sgn} z$ | $z$ 的单位模函数 | $\operatorname{sgn} z =z / \lvert z\rvert = \exp(\mathrm{i} \arg z)\quad (z \ne 0)$;<br>$\operatorname{sgn} 0 = 0$;<br>参见 [n6.13](#n6.13).                                                             |

## 矩阵

| 编号                              | 符号，表达式                             | 意义，等同表述             | 备注与示例                                                                                         |
| ------------------------------- | ---------------------------------- | ------------------- | --------------------------------------------------------------------------------------------- |
| <span id="n12.1">n12.1</span>   | $A$;<br>*参见*[^n12.1-ref1]          | $m\times n$ 型矩阵 $A$ | $a_{ij} = (A)_{ij}$;<br>也可使用 $A = (a_{ij})$. 其中 $m$ 为行数，$n$ 为列数<br>$m=n$ 时称为方阵<br>可用方括号替代圆括号． |
| <span id="n12.2">n12.2</span>   | $A + B$                            | 矩阵 $A$ 和 $B$ 的和     | $(A + B)_{ij} = (A)_{ij} + (B)_{ij}$;<br>矩阵 $A$ 和 $B$ 的行数和列数必须分别相同．                           |
| <span id="n12.3">n12.3</span>   | $x A$                              | 标量 $x$ 和矩阵 $A$ 的乘积  | $(x A)_{ij} = x (A)_{ij}$.                                                                    |
| <span id="n12.4">n12.4</span>   | $AB$                               | 矩阵 $A$ 和 $B$ 的乘积    | $\displaystyle(AB)_{ik} = \sum\limits_{j}(A)_{ij}(B)_{jk}$;<br>矩阵 $A$ 的列数必须等于矩阵 $B$ 的行数．      |
| <span id="n12.5">n12.5</span>   | $I$;<br>$E$                        | 单位矩阵                | $(I)_{ik} = \delta_{ik}$;<br>$\delta_{ik}$ 的定义参见 [n14.9](#n14.9).                             |
| <span id="n12.6">n12.6</span>   | $A^{-1}$                           | 方阵 $A$ 的逆           | $AA^{-1} = A^{-1}A = I\quad (\det A \ne 0)$.<br>$\det A$ 的定义参见 [n12.10](#n12.10).             |
| <span id="n12.7">n12.7</span>   | $A^{\mathrm{T}}$;<br>$A'$          | $A$ 的转置矩阵           | $(A^{\mathrm{T}})_{ik} = (A)_{ki}$.                                                           |
| <span id="n12.8">n12.8</span>   | $\overline{A}$;<br>$A^*$           | $A$ 的复共轭矩阵          | $\left(\overline{A}\right)_{ik}=\overline{(A)_{ik}}$.                                         |
| <span id="n12.9">n12.9</span>   | $A^{\mathrm{H}}$;<br>$A^{\dagger}$ | $A$ 的 Hermite 共轭矩阵  | $A^{\mathrm{H}} = \left(\overline{A}\right)^{\mathrm{T}}$.                                    |
| <span id="n12.10">n12.10</span> | $\det A$;<br>*参见*[^n12.10-ref1]    | 方阵 $A$ 的行列式         | 也可使用 $\lvert A\rvert$.                                                                        |
| <span id="n12.11">n12.11</span> | $\operatorname{rank}A$             | 矩阵 $A$ 的秩           |                                                                                               |
| <span id="n12.12">n12.12</span> | $\operatorname{tr}A$               | 方阵 $A$ 的迹           | $\displaystyle\operatorname{tr}A=\sum\limits_{i}(A)_{ii}$.                                    |
| <span id="n12.13">n12.13</span> | $\lVert A\rVert$                   | 矩阵 $A$ 的范数          | 满足三角不等式：若 $A + B = C$, 则 $\lVert A\rVert+\lVert B\rVert \geq \lVert C\rVert$.                 |

[^n12.1-ref1]: $\begin{pmatrix}a_{11}&\cdots&a_{1n}\\\vdots&\ddots&\vdots\\a_{m1}&\cdots&a_{mn}\end{pmatrix}$

[^n12.10-ref1]: $\begin{vmatrix}a_{11}&\cdots&a_{1n}\\\vdots& &\vdots\\a_{n1}&\cdots&a_{nn}\end{vmatrix}$

## 坐标系

本节考虑三维空间中的一些坐标系．点 $\mathrm{O}$ 为坐标系的 **原点**．任意点 $\mathrm{P}$ 均由从原点 $\mathrm{O}$ 到点 $\mathrm{P}$ 的 **位置向量** 确定．

| 编号                            | 坐标                        | 位置向量和微分                                                                                                                                                                                                                      | 坐标名   | 备注                                                                                                                                                                                                                                                                     |
| ----------------------------- | ------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <span id="n13.1">n13.1</span> | $x$，$y$，$z$               | $\boldsymbol{r} = x \boldsymbol{e}_x + y \boldsymbol{e}_y + z \boldsymbol{e}_z$;<br>$\mathrm{d}\boldsymbol{r} = \mathrm{d}x~\boldsymbol{e}_x + \mathrm{d}y~\boldsymbol{e}_y + \mathrm{d}z~\boldsymbol{e}_z$                  | 笛卡尔坐标 | 基向量 $\boldsymbol{e}_x$，$\boldsymbol{e}_y$，$\boldsymbol{e}_z$ 构成右手正交系，见 [图 1](#图-1) 和 [图 4](#图-4)．<br>基向量也可用 $\boldsymbol{e}_1$，$\boldsymbol{e}_2$，$\boldsymbol{e}_3$ 或 $\boldsymbol{i}$，$\boldsymbol{j}$，$\boldsymbol{k}$ 表示，坐标也可用 $x_1$，$x_2$，$x_3$ 或 $i$，$j$，$k$ 表示． |
| <span id="n13.2">n13.2</span> | $\rho$，$\varphi$，$z$      | $\boldsymbol{r} = \rho~\boldsymbol{e}_{\rho} + z~\boldsymbol{e}_z$;<br>$\mathrm{d}\boldsymbol{r} = \mathrm{d}\rho~\boldsymbol{e}_{\rho} +\rho~\mathrm{d}\varphi~\boldsymbol{e}_{\varphi} + \mathrm{d}z~\boldsymbol{e}_z$     | 柱坐标   | $\boldsymbol{e}_{\rho}(\varphi)$，$\boldsymbol{e}_{\varphi}(\varphi)$，$\boldsymbol{e}_z$ 组成右手正交系，见 [图 2](#图-2)．<br>若 $z = 0$, 则 $\rho$ 和 $\varphi$ 是平面上的极坐标．                                                                                                            |
| <span id="n13.3">n13.3</span> | $r$，$\vartheta$，$\varphi$ | $\boldsymbol{r} = r \boldsymbol{e}_r$;<br>$\mathrm{d}\boldsymbol{r} = \mathrm{d}r~\boldsymbol{e}_r + r~\mathrm{d}\vartheta~\boldsymbol{e}_{\vartheta} + r~\sin\vartheta~\mathrm{\mathrm{d}}\varphi~\boldsymbol{e}_{\varphi}$ | 球坐标   | $\boldsymbol{e}_r(\vartheta, \varphi)$，$\boldsymbol{e}_{\vartheta}(\vartheta, \varphi)$，$\boldsymbol{e}_{\varphi}(\varphi)$ 组成右手正交系，见 [图 3](#图-3)．                                                                                                                     |

如果不使用 [右手坐标系](#图-4)，而使用 [左手坐标系](#图-5)，则应在之前明确强调，以免符号误用．

![](./images/symbol-1.svg)

<span id="图-1">**图 1**</span>右手笛卡尔坐标系

![](./images/symbol-2.svg)

<span id="图-2">**图 2**</span>右手柱坐标系

![](./images/symbol-3.svg)

<span id="图-3">**图 3**</span>右手球坐标系

![](./images/symbol-4.svg)

<span id="图-4">**图 4**</span>右手坐标系

![](./images/symbol-5.svg)

<span id="图-5">**图 5**</span>左手坐标系

## 标量和向量

本节中，基向量用 $\boldsymbol{e}_1$，$\boldsymbol{e}_2$，$\boldsymbol{e}_3$ 表示．本节中的许多概念都可以推广到 $n$ 维空间．

标量和向量本身与坐标系的选择无关，而向量的每个标量分量与坐标系的选择有关．

对于基向量 $\boldsymbol{e}_1$，$\boldsymbol{e}_2$，$\boldsymbol{e}_3$, 每个向量 $\boldsymbol{a}$ 都可以表示为 $\boldsymbol{a}=a_1\boldsymbol{e}_1+a_2\boldsymbol{e}_2+a_3\boldsymbol{e}_3$, 其中 $a_1$，$a_2$ 和 $a_3$ 是唯一确定的标量值，将其称为向量相对于该组基向量的 "坐标"，$a_1\boldsymbol{e}_1$，$a_2\boldsymbol{e}_2$ 和 $a_3\boldsymbol{e}_3$ 称为向量相对于该组基向量的分向量．

在本节中，只考虑普通空间的笛卡尔（正交）坐标．笛卡尔坐标用 $x$，$y$，$z$ 或 $a_1$，$a_2$，$a_3$ 或 $x_1$，$x_2$，$x_3$ 表示．

本节所有下标 $i$，$j$，$k$ 的范围均为 $1$ 到 $3$.

| 编号                              | 符号，表达式                                                                                                                | 意义，等同表述                                         | 备注与示例                                                                                                                                                                                                                                                                                                                                                                                                |
| ------------------------------- | --------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <span id="n14.1">n14.1</span>   | $\boldsymbol{a}$;<br>$\vec{a}$                                                                                        | 向量 $\boldsymbol{a}$                             |                                                                                                                                                                                                                                                                                                                                                                                                      |
| <span id="n14.2">n14.2</span>   | $\boldsymbol{a} + \boldsymbol{b}$                                                                                     | 向量 $\boldsymbol{a}$ 和 $\boldsymbol{b}$ 的和       | $(\boldsymbol{a} + \boldsymbol{b})_i = a_i + b_i$.                                                                                                                                                                                                                                                                                                                                                   |
| <span id="n14.3">n14.3</span>   | $x\boldsymbol{a}$                                                                                                     | 标量 $x$ 与向量 $\boldsymbol{a}$ 的乘积                 | $(x\boldsymbol{a})_i = xa_i$.                                                                                                                                                                                                                                                                                                                                                                        |
| <span id="n14.4">n14.4</span>   | $\lvert \boldsymbol{a}\rvert$                                                                                         | 向量 $\boldsymbol{a}$ 的大小，向量 $\boldsymbol{a}$ 的范数 | $\lvert \boldsymbol{a}\rvert=\sqrt{a_x^2+a_y^2+a_z^2}$;<br>也可使用 $\lVert a\rVert$.                                                                                                                                                                                                                                                                                                                    |
| <span id="n14.5">n14.5</span>   | $\boldsymbol{0}$;<br>$\vec{0}$                                                                                        | 零向量                                             | 零向量的大小为 $0$.                                                                                                                                                                                                                                                                                                                                                                                         |
| <span id="n14.6">n14.6</span>   | $\boldsymbol{e_a}$                                                                                                    | $\boldsymbol{a}$ 方向的单位向量                        | $\boldsymbol{e_a} = \boldsymbol{a}/\lvert\boldsymbol{a}\rvert\quad (\boldsymbol{a}\ne \boldsymbol{0})$.                                                                                                                                                                                                                                                                                              |
| <span id="n14.7">n14.7</span>   | $\boldsymbol{e}_x$，$\boldsymbol{e}_y$，$\boldsymbol{e}_z$;<br>$\boldsymbol{e}_1$，$\boldsymbol{e}_2$，$\boldsymbol{e}_3$ | 笛卡尔坐标轴方向的单位向量                                   | 也可使用 $\boldsymbol{i}$，$\boldsymbol{j}$，$\boldsymbol{k}$.                                                                                                                                                                                                                                                                                                                                             |
| <span id="n14.8">n14.8</span>   | $a_x$，$a_y$，$a_z$;<br>$a_i$                                                                                           | 向量 $\boldsymbol{a}$ 的笛卡尔分量                      | $\boldsymbol{a} = a_x \boldsymbol{e}_x + a_y \boldsymbol{e}_y + a_z \boldsymbol{e}_z$;<br>如果上下文确定了基向量，则向量可以写为 $\boldsymbol{a} = (a_x, a_y, a_z)$.<br>$a_x = \boldsymbol{a}\cdot \boldsymbol{e}_x$，$a_y = \boldsymbol{a}\cdot \boldsymbol{e}_y$，$a_z = \boldsymbol{a}\cdot \boldsymbol{e}_z$;<br>$\boldsymbol{r} = x\boldsymbol{e}_x + y\boldsymbol{e}_y + z\boldsymbol{e}_z$ 是坐标为 $x$，$y$，$z$ 的位置向量． |
| <span id="n14.9">n14.9</span>   | $\delta_{ik}$                                                                                                         | Kronecker delta 符号                              | $\delta_{ik}=[i=k]$，其中 $[\cdot]$ 的定义参见 [n6.24](#n6.24)，即：<br>$\delta_{ik}=1\quad (i=k)$;<br>$\delta_{ik}=0\quad (i\ne k)$.                                                                                                                                                                                                                                                                           |
| <span id="n14.10">n14.10</span> | $\varepsilon_{ijk}$                                                                                                   | Levi-Civita 符号                                  | $\varepsilon_{123} = \varepsilon_{231} = \varepsilon_{312} = 1$;<br>$\varepsilon_{132} = \varepsilon_{321} = \varepsilon_{213} = -1$;<br>其余的 $\varepsilon_{ijk}$ 均为 $0$.                                                                                                                                                                                                                             |
| <span id="n14.11">n14.11</span> | $\boldsymbol{a}\cdot\boldsymbol{b}$                                                                                   | 向量 $\boldsymbol{a}$ 和 $\boldsymbol{b}$ 的标量积/内积  | $\displaystyle\boldsymbol{a}\cdot\boldsymbol{b}=\sum\limits_i a_ib_i$.                                                                                                                                                                                                                                                                                                                               |
| <span id="n14.12">n14.12</span> | $\boldsymbol{a}\times\boldsymbol{b}$                                                                                  | 向量 $\boldsymbol{a}$ 和 $\boldsymbol{b}$ 的向量积/外积  | 右手笛卡尔坐标系中，$\displaystyle (\boldsymbol{a}\times\boldsymbol{b})_i = \sum\limits_j\sum\limits_k\varepsilon_{ijk}a_jb_k$;<br>$\varepsilon_{ijk}$ 的定义参见 [n14.10](#n14.10).                                                                                                                                                                                                                                |
| <span id="n14.13">n14.13</span> | $\mathbf{\nabla}$                                                                                                     | nabla 算子                                        | $\displaystyle \mathbf{\nabla} = \boldsymbol{e}_x\frac{\partial}{\partial x}+\boldsymbol{e}_y\frac{\partial}{\partial y}+\boldsymbol{e}_z\frac{\partial}{\partial z}=\sum\limits_i\boldsymbol{e}_i\frac{\partial}{\partial x_i}$.                                                                                                                                                                    |
| <span id="n14.14">n14.14</span> | $\mathbf{\nabla}\varphi$;<br>$\operatorname{\mathbf{grad}}\varphi$                                                    | $\varphi$ 的梯度                                   | $\displaystyle \mathbf{\nabla}\varphi=\sum\limits_i\boldsymbol{e}_i\frac{\partial\varphi}{\partial x_i}$;<br>$\operatorname{\mathbf{grad}}$ 应使用 `\operatorname{\mathbf{grad}}`.                                                                                                                                                                                                                      |
| <span id="n14.15">n14.15</span> | $\mathbf{\nabla}\cdot\boldsymbol{a}$;<br>$\operatorname{\mathbf{div}}\boldsymbol{a}$                                  | $\boldsymbol{a}$ 的散度                            | $\displaystyle \mathbf{\nabla}\cdot\boldsymbol{a}=\sum\limits_i\frac{\partial a_i}{\partial x_i}$;<br>$\operatorname{\mathbf{div}}$ 应使用 `\operatorname{\mathbf{div}}`.                                                                                                                                                                                                                               |
| <span id="n14.16">n14.16</span> | $\mathbf{\nabla}\times\boldsymbol{a}$;<br>$\operatorname{\mathbf{rot}}\boldsymbol{a}$                                 | $\boldsymbol{a}$ 的旋度                            | $\displaystyle (\mathbf{\nabla}\times\boldsymbol{a})_i=\sum\limits_j\sum\limits_k\varepsilon_{ijk}\frac{\partial a_k}{\partial x_j}$;<br>$\operatorname{\mathbf{rot}}$ 应使用 `\operatorname{\mathbf{rot}}`.<br>不应使用 $\operatorname{\mathbf{curl}}$.<br>$\varepsilon_{ijk}$ 的定义参见 [n14.10](#n14.10).                                                                                                    |
| <span id="n14.17">n14.17</span> | $\mathbf{\nabla}^2$;<br>$\Delta$                                                                                      | Laplace 算子                                      | $\mathbf{\nabla}^2=\dfrac{\partial^2}{\partial x^2}+\dfrac{\partial^2}{\partial y^2}+\dfrac{\partial^2}{\partial z^2}$.                                                                                                                                                                                                                                                                              |

## 特殊函数

本节中的 $z$，$w$ 是复数，$k$，$n$ 是自然数，且 $k\leq n$．

| 编号                            | 符号，表达式                   | 意义，等同表述             | 备注与示例                                                                                                                                                                                                                                                                           |
| ----------------------------- | ------------------------ | ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <span id="n15.1">n15.1</span> | $\gamma$                 | Euler–Mascheroni 常数 | $\displaystyle \gamma=\lim\limits_{n\to\infty}\left(\sum\limits_{k=1}^n\frac{1}{k}-\ln n\right)= 0.577~215~6 \dots$.                                                                                                                                                            |
| <span id="n15.2">n15.2</span> | $\Gamma(z)$              | gamma 函数            | $\displaystyle\Gamma(z)=\int\limits_0^{\infty}t^{z-1}\mathrm{e}^{-t}\mathrm{d}t\quad (\operatorname{Re}z>0)$;<br>$\Gamma(n+1)=n!$.                                                                                                                                              |
| <span id="n15.3">n15.3</span> | $\zeta(z)$               | Riemann zeta 函数     | $\displaystyle\zeta(z)=\sum\limits_{n=1}^{\infty}\frac{1}{n^z}\quad (\operatorname{Re}z>1)$.                                                                                                                                                                                    |
| <span id="n15.4">n15.4</span> | $\operatorname{B}(z, w)$ | beta 函数             | $\displaystyle\operatorname{B}(z, w)=\int\limits_0^1 t^{z-1}(1-t)^{w-1}\mathrm{d}t\quad (\operatorname{Re} z>0$，$\operatorname{Re} w>0)$;<br>$\operatorname{B}(z, w)=\dfrac{\Gamma(z)\Gamma(w)}{\Gamma(z+w)}$;<br>$\dfrac{1}{(n+1)\operatorname{B}(k+1, n-k+1)}=\dbinom{n}{k}$. |


## intro/thanks.md

disqus:

本项目目前暂不接受捐赠．

所有款项将被用于 **OI Wiki** 的域名、服务器、运维等必需支出．

大额捐赠将会记录在本页面下方或日后更合适的位置来表示感谢．

***

|       id      |  amount |    date    |
| :-----------: | :-----: | :--------: |
|     匿名捐赠者     |   10 元  |  2021.6.20 |
|     匿名捐赠者     |  100 元  |  2021.6.10 |
|     wood3     |  256 元  |  2021.6.4  |
|      海外兔      |  102 元  |  2021.5.12 |
|      逐梦之人     |  80.7 元 |  2021.5.3  |
|    十寸雨 zsg    | 10.24 元 |  2021.2.27 |
|     匿名捐赠者     |   2 元   | 2020.12.10 |
|    吾有一數名之曰誒   | 10.24 元 | 2020.10.19 |
|      Huah     |   66 元  |  2020.9.7  |
|   icedream61  |   66 元  |  2020.9.2  |
|     三鸽酸鸽可爱    |  2.33 元 |  2020.8.31 |
|    Apoi2333   | 23.33 元 |  2020.8.31 |
|      草莓熊      |   50 元  |  2020.7.4  |
|     匿名捐赠者     |  200 元  |  2020.6.29 |
|     Hiroid    |   30 元  |  2020.5.13 |
|     dcmfqw    | 20.48 元 |  2020.5.4  |
|     akira     |   66 元  |  2020.3.30 |
|    Hermione   |   10 元  |  2020.3.26 |
|     Siyuan    |   10 元  |  2020.2.28 |
|      hsh      |   15 元  |  2020.2.21 |
|       陌陌      |   10 元  |  2020.2.6  |
|     匿名捐赠者     |   10 元  |  2020.2.5  |
|     Yisin     |   10 元  |  2020.2.4  |
|    GinRyan    |   50 元  | 2019.11.30 |
|    JuicyMio   |   10 元  | 2019.11.30 |
|     匿名捐赠者     |   10 元  | 2019.11.14 |
|    QQ 联系 12   |   5 元   | 2019.10.28 |
|     匿名捐赠者     |   5 元   | 2019.10.27 |
|     增肥中的小肥    |   50 元  | 2019.10.24 |
|    ianahao    |   10 元  | 2019.10.12 |
|     Sundy     |   10 元  | 2019.10.11 |
|     三鸽最可爱     | 23.33 元 |  2019.8.17 |
|     Fburan    | 10.24 元 |  2019.8.17 |
|     匿名捐赠者     |   30 元  |  2019.8.8  |
| Billchenchina |  100 元  |  2019.8.7  |
|   贷款捐头的匿名入土   |   30 元  |  2019.8.4  |
|     sshwy     |   50 元  |  2019.8.4  |
|     匿名捐赠者     |   10 元  |  2018.9.9  |
|     匿名捐赠者     |   20 元  |  2018.8.31 |
|    Xeonacid   |   30 元  |  2018.8.30 |
|     匿名捐赠者     |  240 元  |  2018.8.29 |
|     Anguei    |   5 元   |  2018.8.29 |


## intro/what-oi-wiki-is-not.md

author: abc1763613206, HeRaNO, NachtgeistW, r-value, Tiphereth-A, wlbksy, YZircon, 0zu-cc, real01bit

???+ warning "注意"
    作为项目方针的一部分，本页面十分重要，每个贡献者都应确保您的贡献满足如下条件．

## OI Wiki 不是发表原创研究的场所

作为一个 Wiki，**OI Wiki** 不是发表 [原创研究](https://en.wikipedia.org/wiki/Wikipedia:No_original_research)（如 **新理论及解法**、**原创观点**、**自创定义或词语** 等）的场所．例如：

-   您发现了某题目的非常规做法，若您不能证明该做法已经被应用于其他题目中，则 **不应** 在 **OI Wiki** 中开设单独的界面．
-   您提出了新的算法或数据结构，若您不能证明该内容已经被用于解决编程竞赛中的某一类问题，则 **不应** 将其提交至 **OI Wiki**．

## OI Wiki 不是新闻的收集处

作为泛中文为主语境之下、以编程竞赛相关内容为主的知识整合站点，**OI Wiki** 侧重于提供 **稳定沉淀并已取得广泛认可** 的信息．

换言之，除非是权威机构发布的信息（如中国计算机学会发布的赛制更新），您所贡献的内容应当是已经经过检验沉淀，获得了广泛认可，且在一段时间内不会产生时效性问题的信息．例如：

-   您发现 X 博士在某个位置发布了新的算法，若您想将其加入 **OI Wiki** 中，此时您应该观察其是否能获得广泛认可（如可作为正式比赛中的泛用优秀解法），且与 **OI Wiki** 中现存的算法有一定的区分性．
-   您发现 **OI Wiki** 中提到的某软件或人物出现了舆情问题，此时请您关注评论区等的相关公告，切勿重复开 issue 等说明问题．**OI Wiki** 的目的在于记载 **可长久流传的信息**，而不是 **带有时效性的临时信息**．

## OI Wiki 不是档案馆

**OI Wiki** 主站不会收录各类 **文献**、**课件**、**讲义**、**说明书** 等资料，若您想提交有关编程竞赛的资料，请移步至 [OI-wiki/libs](https://github.com/OI-wiki/libs)．

## OI Wiki 不是宣传工具

**OI Wiki** 是一个知识整合站点，**不是** 演讲台、论坛、宣传工具等，因此在添加或修改条目时，请勿：

-   发表观点或评论：**OI Wiki** 的内容必须 **客观中立**，如果您想要发表与 **OI Wiki** 有关的观点与评论，请移步至评论区或 issue 页面．如果您想要发表的观点与评论与 **OI Wiki** 无关，请移步至个人博客或论坛；
-   作任何形式的宣传行为：出于知识收录需要，**OI Wiki** 可以接受对「在编程竞赛领域已经 **广为人知** 的网站或软件」的介绍．除此之外，**OI Wiki** 不会接受任何非赞助商提供的任何宣传性质的内容．

## OI Wiki 不是权威机构

作为一个主要依靠用户贡献的社区项目，**OI Wiki** 不具有权威性，不应也没有能力作为一个权威机构．**OI Wiki** 可以作为学习编程竞赛相关知识的参考，而不是标准教科书．作为一个社区维护的参考站点，您不应将 **OI Wiki** 用作最终的权威标准（如作为编程竞赛的「考纲」），也不应盲目采信所有 **OI Wiki** 的内容．**OI Wiki** 不对由使用 **OI Wiki** 的内容而产生的任何后果负责．

## OI Wiki 不是个人博客

**OI Wiki** 基于「Wiki」一词，本质上是依靠用户 **协同编辑内容** 的社区．这就意味着，您所提供的内容应当 **尽量减轻个人色彩**，服务于整个 Wiki，关注您所贡献的相关词条的结构．切勿以撰写个人博客文章的思维对待 Wiki 中的条目．例如：

-   您 **不应** 将 **OI Wiki** 作为您个人博客的导航站点；
-   您 **不应** 在词条的描述中加入条目历史、个人吐槽、冷笑话等无关内容．

以上例子的反面均为撰写个人博客时的常见思维，而这些在提倡客观中立的 **OI Wiki** 中是不受欢迎的．

## OI Wiki 不是译名标准委员会

**OI Wiki** 的目标群体不是历史学家及语言学家，因此在外文名词的翻译中，**OI Wiki** 倾向于使用中文语境下 **已经获得了广泛认同** 的译文，即使它们可能是有瑕疵的．

在译文已经获得了广泛熟知认同的基础上，盲目因「正确性」而修改现有的译文只会引发更大的混淆与混乱，与之引发的文字游戏也会影响沟通效率．

## OI Wiki 不是百科全书

**OI Wiki** 收录的内容应限定在「已经被应用于编程竞赛」的计算机科学、数学等领域的部分知识．其他与编程竞赛无关的领域或知识均不适合收录于 **OI Wiki**．

例如，如下的领域或知识 **不适合** 收录于 **OI Wiki**：

-   历史，艺术等无关领域；
-   [TBN 矩阵](https://learnopengl.com/Advanced-Lighting/Normal-Mapping) 等虽然从属于有关领域但目前不能应用于编程竞赛的知识；
-   [PID 控制](https://en.wikipedia.org/wiki/PID_controller)、[有限元法](https://en.wikipedia.org/wiki/Finite_element_method) 等目前不能应用于编程竞赛的领域算法；
-   [深度学习](https://en.wikipedia.org/wiki/Deep_learning)、[强化学习](https://en.wikipedia.org/wiki/Reinforcement_learning) 等目前不能应用于编程竞赛的通用算法．

## OI Wiki 不是编程语言的文档和学习指南

**OI Wiki** 收录的算法相较于代码实现，应更关心算法本身．算法的具体实现仅作为一种更加细致的理解或者实现提示，而不是给具体的语言学习者以方便．如果您想要学习某种语言，您应该阅读该语言的官方文档等资料．

出于知识收录需要，**OI Wiki** 可以收录编程竞赛常用语言的简单使用指南．除此之外，**OI Wiki** 不会收录诸如「某编程语言的某标准库里某函数的实现细节等」与编程竞赛和算法关系不大的内容．
