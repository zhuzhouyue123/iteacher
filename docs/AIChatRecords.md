Q：写一个python程序，要求其可以从google scholar中QS世界排名前60的学校中抓取符合输入条件的研究人员。这些条件包括：研究领域（输入为字符串，不同的领域用逗号隔开），被引用数量限制（类型为int，允许制订上限和下限）。要求最终返回一个列表，其中包括所有在QS排名前60的机构中，至少有一个研究领域和输入的要求重合，且被引用数量在要求范围之内的所有作者在google scholar上的姓名，机构，与被引用次数。

 

A：以下是一个Python程序，用于从Google Scholar抓取QS排名前60大学的研究人员信息，并根据研究领域和引用次数进行筛选：

```python

from scholarly import scholarly

import time

from fuzzywuzzy import fuzz


def get_qs_schools():

    """返回QS前60大学列表（示例数据，需补充完整）"""

    return [

        ​    "Massachusetts Institute of Technology (MIT)",

        ​    "University of Cambridge",

        ​    "Stanford University",

        ​    # 添加其他57所大学...

    ]



def match_affiliation(author_affil, school):

        """使用模糊匹配验证机构隶属关系"""

        return fuzz.token_set_ratio(author_affil.lower(), school.lower()) >= 70



def get_researchers(fields, min_cites, max_cites):

        results = []

        schools = get_qs_schools()



        for idx, school in enumerate(schools):

            ​    print(f"Processing {school} ({idx+1}/{len(schools)})")

            ​    

            ​    try:

                ​      search_query = scholarly.search_author(school)

                ​      while True:

                    ​        try:

                        ​          author = next(search_query)

                        ​          author = scholarly.fill(author)

                        ​          

                        ​          \# 检查机构匹配

                        ​          affil = author.get('affiliation', '')

                        ​          if not affil or not match_affiliation(affil, school):

                            ​            continue

                            ​          

                            ​          \# 检查引用次数

                            ​          cites = author.get('citedby', 0)

                            ​          if not (min_cites <= cites <= max_cites):

                                ​            continue

                                ​          

                                ​          \# 检查研究领域

                                ​          interests = [i.lower() for i in author.get('interests', [])]

                                ​          matched = any(field in interests for field in fields)

                                ​          

                                ​          if matched:

                                    ​            results.append({

                                        ​              'name': author['name'],

                                        ​              'affiliation': affil,

                                        ​              'citations': cites,

                                        ​              'interests': interests

                                        ​            })

                                    ​          

                                    ​          time.sleep(5) # 降低请求频率

                                    ​        

                                    ​        except StopIteration:

                                        ​          break

                                        ​        except Exception as e:

                                            ​          print(f"Error: {e}")

                                            ​          continue

                                            ​    

                                            ​    except Exception as e:

                                                ​      print(f"School {school} error: {e}")

                                                ​    

                                                ​    time.sleep(10) # 学校间间隔



                                                return results


                                            if __name__ == "__main__":

                                                \# 用户输入处理

                                                input_fields = input("Enter research fields (comma-separated): ").lower().split(',')

                                                fields = [f.strip() for f in input_fields]

                                                min_c = int(input("Minimum citations: "))

                                                max_c = int(input("Maximum citations: "))



                                                \# 获取并打印结果

                                                researchers = get_researchers(fields, min_c, max_c)

                                                print(f"\nFound {len(researchers)} researchers:")

                                                for r in researchers:

                                                    ​    print(f"\nName: {r['name']}")

                                                    ​    print(f"Affiliation: {r['affiliation']}")

                                                    ​    print(f"Citations: {r['citations']}")

                                                    ​    print(f"Interests: {', '.join(r['interests'])}")

```

 

写python一个程序，要求其能在google scholar上获取输入的机构里所有人员信息，输入机构的格式如下：["机构1"，"机构2"，(以下省略)]，当找到机构时，以如下字典形成的列表输出人员信息：["姓名1"：["机构名"，[0,"研究领域1"，”研究领域2“......],被引用数（int）]，"姓名2"：["机构名"，[0,"研究领域1"，”研究领域2“......],被引用数（int）]，......]。如果未能找到输入的机构，则跳过，但是要在输出时汇报，如果某人研究领域在google scholar不显示，则包含研究领域的列表只用填[0]，最后要求把列表输出在txt文件中，并且在最后说明未能找到的机构，以及找到的机构中，每个机构中有多少结果


```python
from scholarly import scholarly

import time

from fuzzywuzzy import fuzz

import json



def get_researchers(institutions):

  results = {}

  not_found = []

  institution_counts = {inst:0 for inst in institutions}



  for idx, institution in enumerate(institutions):

​    print(f"\n正在处理 {institution} ({idx+1}/{len(institutions)})")

​    try:

​      \# 搜索机构学者

​      search_query = scholarly.search_author(institution)

​      found_flag = False

​      

​      while True:

​        try:

​          author = next(search_query)

​          author = scholarly.fill(author)

​          

​          \# 验证机构隶属关系

​          affil = author.get('affiliation', '')

​          if fuzz.token_set_ratio(affil.lower(), institution.lower()) < 70:

​            continue

​          

​          \# 解析研究领域

​          interests = [0] # 默认值

​          if 'interests' in author and author['interests']:

​            interests = [0] + [i.strip() for i in author['interests']]

​          

​          \# 构建数据结构

​          researcher_data = [

​            institution,

​            interests,

​            author.get('citedby', 0)

​          ]

​          

​          \# 添加到结果

​          results[author['name']] = researcher_data

​          institution_counts[institution] += 1

​          found_flag = True

​          

​          \# 请求间隔

​          time.sleep(10)

​        

​        except StopIteration:

​          break

​        except Exception as e:

​          print(f"处理学者时出错: {str(e)}")

​          continue

​      

​      if not found_flag:

​        not_found.append(institution)

​      

​    except Exception as e:

​      print(f"处理机构时发生严重错误: {str(e)}")

​      not_found.append(institution)

​    

​    time.sleep(15) # 机构间间隔



  # 清理未找到的机构

for nf in not_found:

​    institution_counts.pop(nf, None)



  return results, not_found, institution_counts



def save_results(data, not_found, counts, filename="scholar_results.txt"):

  	with open(filename, 'w', encoding='utf-8') as f:

​    	# 写入研究人员数据

​    	f.write("研究人员列表:\n")

​    	f.write(json.dumps(data, ensure_ascii=False, indent=2))

​    

​    	# 写入统计信息

​    	f.write("\n\n统计信息:\n")

​   	f.write(f"未找到的机构: {', '.join(not_found) if not_found else '无'}\n")

​    	f.write("各机构结果数:\n")
​		for inst, count in counts.items():
​      		f.write(f"{inst}: {count} 条结果\n")

​      

if __name__ == "__main__":

  # 示例输入（正式使用时可改为用户输入）

  input_institutions = ["Massachusetts Institute of Technology", "清华大学", "虚构测试大学"]



  # 获取数据

  results_data, not_found_list, count_dict = get_researchers(input_institutions)



  # 保存结果

  save_results(results_data, not_found_list, count_dict)



print("程序执行完成，结果已保存到 scholar_results.txt")
```




已知进入google scholar某机构网页后，如果打开网页代码所有我们需要的个人信息都存储在形如<div class = “gsc_lusr”>的语句中，以教授Kaiming He 为例，其对应语句内部，<h3 class=”gs_ai_name”>的下方语句<a href=”/citations?hi=zh-TW&user=DhtAFkwAAAAJ”>Kaiming He</a>中，链接后的“Kaiming He “就是教授名字。同理，被引用次数在<div class="gs_ai_cby">被引用 686634 次</div>中，研究领域在<div class="gs_ai_int"><a class="gs_ai_one_int" href="/citations?hl=zh-TW&amp;view_op=search_authors&amp;mauthors=label:computer_vision">Computer Vision</a> <a class="gs_ai_one_int" href="/citations?hl=zh-TW&amp;view_op=search_authors&amp;mauthors=label:machine_learning">Machine Learning</a> </div>语句中。

现在根据此思路优化代码，要求在找到机构在google scholar的网址后，从首页开始，直接复制网页代码中的所需信息输出到列表（要注意不是所有人都有研究领域的数据，要特殊处理）处理完后翻页，重复当前步骤，直到此机构最后一页。


```python
import requests

from bs4 import BeautifulSoup

import re

import time

import urllib.parse

from tqdm import tqdm



HEADERS = {

  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',

  'Accept-Language': 'en-US,en;q=0.9'

}



def parse_scholar_page(html):

  """解析Google Scholar页面"""

  soup = BeautifulSoup(html, 'lxml')

  researchers = []



  \# 遍历每个学者卡片

  for card in soup.select('div.gsc_1usr'):

​    try:

​      \# 解析姓名

​      name_tag = card.select_one('h3.gs_ai_name a')

​      name = name_tag.text.strip() if name_tag else "Unknown"

​      

​      \# 解析引用次数

​      cites_tag = card.select_one('div.gs_ai_cby')

​      cites = int(re.search(r'\d+', cites_tag.text).group()) if cites_tag else 0

​      

​      \# 解析研究领域

​      interests_tag = card.select_one('div.gs_ai_int')

​      if interests_tag:

​        interests = [0] + [a.text.strip() for a in interests_tag.select('a.gs_ai_one_int')]

​      else:

​        interests = [0]

​        

​      researchers.append({

​        'name': name,

​        'interests': interests,

​        'citations': cites

​      })

​    except Exception as e:

​      print(f"解析错误: {str(e)}")

​      continue

​      

  \# 获取下一页链接

  next_page = soup.select_one('button.gs_btnPR[onclick]')

  next_page_token = None

  if next_page:

​    match = re.search(r'after_author\\x3d(.*?)\\x26', next_page['onclick'])

​    if match:

​      next_page_token = urllib.parse.unquote(match.group(1))

​      

  return researchers, next_page_token



def fetch_institution(institution):

  """抓取单个机构数据"""

  base_url = "https://scholar.google.com/citations"

  params = {

​    'view_op': 'search_authors',

​    'hl': 'en',

​    'mauthors': institution

  }



  all_researchers = []

  retry_count = 0

  session = requests.Session()



  with tqdm(desc=f"抓取 {institution}", unit="页") as pbar:

​    while True:

​      try:

​        \# 发送请求

​        response = session.get(base_url, params=params, headers=HEADERS, timeout=30)

​        response.raise_for_status()

​        

​        \# 解析页面

​        page_researchers, next_token = parse_scholar_page(response.text)

​        all_researchers.extend(page_researchers)

​        

​        \# 更新进度

​        pbar.update(1)

​        pbar.set_postfix({'当前学者数': len(all_researchers)})

​        

​        \# 检查是否还有下一页

​        if not next_token or retry_count >= 3:

​          break

​        

​        \# 更新分页参数

​        params['after_author'] = next_token

​        time.sleep(10) # 重要！防止请求过快

​        retry_count = 0

​        

​      except requests.exceptions.RequestException as e:

​        print(f"请求失败: {str(e)}")

​        retry_count += 1

​        time.sleep(30)

​        if retry_count > 3:

​          break

​          

  return all_researchers



def process_institutions(institutions):

  """处理机构列表"""

  results = {}

  not_found = []

  stats = {}



  for institution in institutions:

​    try:

​      researchers = fetch_institution(institution)

​      if not researchers:

​        not_found.append(institution)

​        continue

​        

​      \# 格式化数据结构

​      stats[institution] = len(researchers)

​      for r in researchers:

​        results[r['name']] = [

​          institution,

​          r['interests'],

​          r['citations']

​        ]

​        

​    except Exception as e:

​      print(f"机构 {institution} 处理失败: {str(e)}")

​      not_found.append(institution)

​      

​    time.sleep(30) # 机构间间隔

​    

  return results, not_found, stats



def save_results(data, not_found, stats):

  """保存结果"""

  with open('scholar_data.txt', 'w', encoding='utf-8') as f:

​    \# 写入学者数据

​    f.write("{\n")

​    for name, info in data.items():

​      line = f'"{name}": {info},\n'

​      f.write(line)

​    f.write("}\n\n")

​    

​    \# 写入统计

​    f.write(f"未找到的机构: {not_found}\n")

​    f.write("各机构结果数:\n")

​    for inst, count in stats.items():

​      f.write(f"{inst}: {count}\n")

 

if __name__ == "__main__":

  \# 输入示例

  input_institutions = [

​    "Massachusetts Institute of Technology",

​    "Stanford University",

​    "虚构测试大学"

  ]



  \# 执行抓取

  final_data, not_found_list, stats_dict = process_institutions(input_institutions)



  \# 保存结果

  save_results(final_data, not_found_list, stats_dict)

print("执行完成，结果已保存到 scholar_data.txt")
```




要求代码最多抓取某个机构前100页的内容


```python
def fetch_institution(institution):

  """抓取单个机构数据（最多100页）"""

  base_url = "https://scholar.google.com/citations"

  params = {

​    'view_op': 'search_authors',

​    'hl': 'en',

​    'mauthors': institution

  }



  all_researchers = []

  retry_count = 0

  page_count = 0 # 新增页数计数器

  max_pages = 100 # 最大页数限制

  session = requests.Session()



  with tqdm(desc=f"抓取 {institution}", total=max_pages, unit="页") as pbar:

​    while page_count < max_pages: # 添加页数限制条件

​      try:

​        \# 发送请求

​        response = session.get(base_url, params=params, headers=HEADERS, timeout=30)

​        response.raise_for_status()

​        

​        \# 解析页面

​        page_researchers, next_token = parse_scholar_page(response.text)

​        all_researchers.extend(page_researchers)

​        

​        \# 更新进度

​        page_count += 1 # 页数递增

​        pbar.update(1)

​        pbar.set_postfix({

​          '当前学者数': len(all_researchers),

​          '当前页数': f"{page_count}/{max_pages}"

​        })

​        

​        \# 检查是否还有下一页

​        if not next_token or retry_count >= 3:

​          break

​        

​        \# 更新分页参数

​        params['after_author'] = next_token

​        time.sleep(10)

​        retry_count = 0

​        

​      except requests.exceptions.RequestException as e:

​        print(f"请求失败: {str(e)}")

​        retry_count += 1

​        time.sleep(30)

​        if retry_count > 3:

​          break

​          

return all_researchers
```




现在我们得到了形如下边的数据，数据来源为名为scholar_.txt的文本
```json
{

"Robert Langer": ['Massachusetts Institute of Technology', [0, 'drug delivery', 'tissue engineering', 'biomaterials', 'nanotechnology', 'chemistry'], 445798],

"Markus Klute": ['Massachusetts Institute of Technology', [0, 'Particle Physics'], 286686],

"John Joannopoulos": ['Massachusetts Institute of Technology', [0], 189379],

"Feng Zhang": ['Massachusetts Institute of Technology', [0, 'neuroscience', 'microbiology', 'optogenetics', 'genome engineering'], 182053],

"Moungi G. Bawendi": ['Massachusetts Institute of Technology', [0], 174134]

}
```

要求写一个程序，能够遍历所有数据，查询并输出符合我们限制条件的数据

限制条件包括：引文数量范围，研究领域（要求允许字符串模糊查询）

 


```python
import json

from fuzzywuzzy import fuzz



def load_data(filename):

  """加载学者数据文件"""

  try:

​    with open(filename, 'r', encoding='utf-8') as f:

​      \# 处理非标准JSON格式（允许单引号）

​      data_str = f.read().replace("'", '"')

​      return json.loads(data_str)

  except FileNotFoundError:

​    print(f"错误：文件 {filename} 未找到")

​    exit()

  except json.JSONDecodeError:

​    print("错误：文件格式不正确")

​    exit()



def fuzzy_match(query, field, threshold=70):

  """执行模糊匹配，返回匹配得分"""

  return fuzz.partial_ratio(query.lower(), field.lower()) >= threshold



def filter_researchers(data, min_cites, max_cites, fields):

  """执行过滤操作"""

  results = []



  for name, details in data.items():

​    institution = details[0]

​    interests = details[1][1:] if len(details[1]) > 1 else [] # 去掉开头的0

​    citations = details[2]

​    

​    \# 检查引用数范围

​    if not (min_cites <= citations <= max_cites):

​      continue

​    

​    \# 检查研究领域匹配

​    field_matched = False

​    if fields: # 如果有指定领域才检查

​      for interest in interests:

​        if any(fuzzy_match(field, interest) for field in fields):

​          field_matched = True

​          break

​    else: # 未指定领域视为匹配

​      field_matched = True

​      

​    if field_matched:

​      results.append({

​        'name': name,

​        'institution': institution,

​        'interests': interests,

​        'citations': citations

​      })



  return results



def main():

  \# 用户输入

  min_c = int(input("请输入最小引用数："))

  max_c = int(input("请输入最大引用数："))

  fields_input = input("请输入研究领域（多个用逗号分隔，留空则不限）：").strip()

  fields = [f.strip() for f in fields_input.split(',')] if fields_input else []



  \# 加载数据

  data = load_data('scholar_.txt')



  \# 执行过滤

  filtered = filter_researchers(data, min_c, max_c, fields)



  \# 输出结果

  print(f"\n找到 {len(filtered)} 位符合条件的学者：")

  for idx, res in enumerate(filtered, 1):

​    print(f"\n【{idx}】{res['name']}")

​    print(f"所属机构：{res['institution']}")

​    print(f"引用次数：{res['citations']:,}")

​    print(f"研究领域：{', '.join(res['interests']) if res['interests'] else '无记录'}")



if __name__ == "__main__":

  \# 安装依赖：pip install fuzzywuzzy python-Levenshtein

  main()
```