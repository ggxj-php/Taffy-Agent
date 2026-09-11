

## edit-landing.md

disqus:

## 编辑前须知

首先，感谢您愿意为 **OI Wiki** 做出自己的贡献．

不过在开始之前，我们需要您了解并熟知 [如何参与](./intro/htc.md) 和 [格式手册](./intro/format.md) 里的内容，以避免在编辑时产生不必要的麻烦．

在阅读完之后，请点击下方的按钮，然后开始编辑．

???+ note "敬请留意"
    -   请您记得在文件头的 author 字段后方按照格式加上您的 GitHub ID；
    -   根据 Issue [#3061](https://github.com/OI-wiki/OI-wiki/issues/3061)，现在您的更改将会视 Commit Message 质量以 Rebase 或 Squash 方式之一合并，且在 Squash 方式下您可能会是该 commit 的 author 而不是 committer，敬请留意．

<a id="btn-startedit" style="padding: 0.75em 1.25em; display: inline-block; line-height: 1; text-decoration: none; white-space: nowrap; cursor: pointer; border: 1px solid #6190e8; border-radius: 5px; background-color: #6190e8; color: #fff; outline: none; font-size: 0.75em;">开始编辑</a>

<script>
    function getQueryVariable(name, dft)
    {
        var reg = new RegExp('(^|&)' + name + '=([^&]*)(&|$)', 'i');
        var r = window.location.search.substr(1).match(reg);
        if (r != null)
        {
            return unescape(r[2]);
        }
        return dft;
    }
    document.getElementById("btn-startedit").href = "https://github.com/OI-wiki/OI-wiki/edit/master/docs" + getQueryVariable("ref", "");
</script>


## index.md

disqus:
pagetime:
title: OI Wiki

## 欢迎来到 **OI Wiki**！[![GitHub watchers](https://img.shields.io/github/watchers/OI-wiki/OI-wiki.svg?style=social&label=Watch)](https://github.com/OI-wiki/OI-wiki)  [![GitHub stars](https://img.shields.io/github/stars/OI-wiki/OI-wiki.svg?style=social&label=Stars)](https://github.com/OI-wiki/OI-wiki)

[![Word Art](images/wordArt.webp)](https://github.com/OI-wiki/OI-wiki)

**OI**（Olympiad in Informatics，信息学奥林匹克竞赛）在中国起源于 1984 年，是五大高中学科竞赛之一．

**ICPC**（International Collegiate Programming Contest，国际大学生程序设计竞赛）由 ICPC 基金会（ICPC Foundation）举办，是最具影响力的大学生计算机竞赛．由于以前 ACM 赞助这个竞赛，也有很多人习惯叫它 ACM 竞赛．

**OI Wiki** 致力于成为一个免费开放且持续更新的 **编程竞赛（competitive programming）** 知识整合站点，大家可以在这里获取与竞赛相关的、有趣又实用的知识．我们为大家准备了竞赛中的基础知识、常见题型、解题思路以及常用工具等内容，帮助大家更快速深入地学习编程竞赛中涉及到的知识．

本项目受 [CTF Wiki](https://ctf-wiki.org/) 的启发，在编写过程中参考了诸多资料，在此一并致谢．

<div align="center">
<a href="https://www.netlify.com/" target="_blank" style="margin-left: 60px;"><img style="height: 40px; " src="images/netlify.png"></a>
</div>

<script>
  // #758
  document.getElementsByClassName('md-nav__title')[1].click()
</script>
