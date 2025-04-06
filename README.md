# iteacher

## 介绍

需要对部分文档进行说明：和AI对话文档包含程序的思路，程序在思路是我指定的，AI写的那个实在太慢，我指定思路了之后快了20倍，Deepseek完成了代码，里边包含了Deepseek详细的设计思路。
程序的优势与设计背景里讲述了这个程序的优势，简单来说，如果顺利，可能几分钟轻松找到100个符合我们要求的老师。并且这个暂时很有问题的程序已经可以帮助我快速找到google scholar难以搜到，但是又很对口的老师了，而且有室友的使用反馈。
程序现在有很大问题，我自己的代码基础很差，难以解决，所以需要帮助。
google scholar 网页结构和代码密切相关，代码就是读取了网页的特定信息来输出。

### 关于代码概述：

1. 首先运行，GOOGLEBASEDONWEB.py，爬到指定机构数据，但是为了保证教授质量，每个机构最多爬1000人。
- 机构指定方法：

  - main函数中以列表表示要爬的机构

    `input_institutions = ["Massachusetts Institute of Technology","Imperial College London","University of Oxford"]`

  - 爬下的数据包括：人名，机构名，被引次数，研究领域，以如下方式存储在文本文档中：


```json
{
"Robert Langer": ['Massachusetts Institute of Technology', [0, 'drug delivery', 'tissue engineering', 'biomaterials', 'nanotechnology', 'chemistry'], 445798],
}
```

- 指定输出文件名的方法：
  在函数 `save_results(data, not_found, stats)`中，
  语句为：
  `with open('scholar_data1-10.txt', 'w', encoding='utf-8') as f:`
  这个`scholar_data1-10.txt`就是输出的文件，已经存储在了文件夹里，此文件已经删掉了最后为了应对未找到机构的报错信息，实际运行时，文档的最后会附带一些文字，告诉你在每个你输入的机构里找到了多少学者，哪些机构没有找到。

2. 当输出完成后，运行`TOJSON.py`文件，因为发现处理数据的文档无法直接处理`.txt`文件，所以又设计了代码`ONETOTWO.py`，`scholar_data1-10.txt`经过此代码输出了文件`scholar_data1-10fixed.txt`，修复后的文件把所有单引号变成了双引号，但是依旧无法被`TOJSON.py`处理

`data_treatment.py`设计出来是为了处理爬到的数据，以实现高度自由，没有延迟的搜索。暂时设计了指定引文数和关键词的功能，并且要支持字符串模糊匹配。但是由于完全打不开爬下来的数据，暂时无法派上用场。

*** 我们希望这个程序最终支持指定机构，或者指定某个国家的学校去搜索。或者其它更方便的搜索功能。***

### 关于其它文件的概述：

`scholar_data1-10.txt`存储了某年世界QS前10大学里，每所学校引文前1000的教授，用于初步测试（但是实际上漏了很多教授，实际可能到了前2000左右）


最终目的是给用户一个`scholar_data`文件和`data treatment.py`文件，不必了解google scholar 的搜索方式，就能实现极其高效的搜索，轻松找到被google scholar漏掉的结果，并且找到的任何结果，在google scholar上都有迹可循，一天投100封不是梦

## 其他文档

-  [AIChatRecords.md](docs/AIChatRecords.md) AI聊天记录（代码部分缩进混乱）
-  [Bugs.md](docs/Bugs.md) 目前遇到的问题
-  [Design.md](docs/Design.md) 设计思路等
-  [QS60.md](docs/QS60.md) QS前60排名
-  [StrctureOfGoogleScholar.md](docs/StrctureOfGoogleScholar.md) 谷歌学术的HTML解析指南

## 作者

- 原作者：Yuyuan Wang
- 整理：Zhouyue Zhu