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

    # 遍历每个学者卡片
    for card in soup.select('div.gsc_1usr'):
        try:
            # 解析姓名
            name_tag = card.select_one('h3.gs_ai_name a')
            name = name_tag.text.strip() if name_tag else "Unknown"

            # 解析引用次数
            cites_tag = card.select_one('div.gs_ai_cby')
            cites = int(re.search(r'\d+', cites_tag.text).group()) if cites_tag else 0

            # 解析研究领域
            interests_tag = card.select_one('div.gs_ai_int')
            if interests_tag:
                interests = [0] + [a.text.strip() for a in interests_tag.select('a.gs_ai_one_int')]
            else:
                interests = [0]

            researchers.append({
                'name': name,
                'interests': interests,
                'citations': cites
            })
        except Exception as e:
            print(f"解析错误: {str(e)}")
            continue

    # 获取下一页链接
    next_page = soup.select_one('button.gs_btnPR[onclick]')
    next_page_token = None
    if next_page:
        match = re.search(r'after_author\\x3d(.*?)\\x26', next_page['onclick'])
        if match:
            next_page_token = urllib.parse.unquote(match.group(1))

    return researchers, next_page_token


def fetch_institution(institution):
    """抓取单个机构数据（最多100页）"""
    base_url = "https://scholar.google.com/citations"
    params = {
        'view_op': 'search_authors',
        'hl': 'en',
        'mauthors': institution
    }

    all_researchers = []
    retry_count = 0
    page_count = 0  # 新增页数计数器
    max_pages = 100  # 最大页数限制
    session = requests.Session()

    with tqdm(desc=f"抓取 {institution}", total=max_pages, unit="页") as pbar:
        while page_count < max_pages:  # 添加页数限制条件
            try:
                # 发送请求
                response = session.get(base_url, params=params, headers=HEADERS, timeout=30)
                response.raise_for_status()

                # 解析页面
                page_researchers, next_token = parse_scholar_page(response.text)
                all_researchers.extend(page_researchers)

                # 更新进度
                page_count += 1  # 页数递增
                pbar.update(1)
                pbar.set_postfix({
                    '当前学者数': len(all_researchers),
                    '当前页数': f"{page_count}/{max_pages}"
                })

                # 检查是否还有下一页
                if not next_token or retry_count >= 3:
                    break

                # 更新分页参数
                params['after_author'] = next_token
                time.sleep(10)
                retry_count = 0

            except requests.exceptions.RequestException as e:
                print(f"请求失败: {str(e)}")
                retry_count += 1
                time.sleep(30)
                if retry_count > 3:
                    break

    return all_researchers
# def fetch_institution(institution):
#     """抓取单个机构数据"""
#     base_url = "https://scholar.google.com/citations"
#     params = {
#         'view_op': 'search_authors',
#         'hl': 'en',
#         'mauthors': institution
#     }
#
#     all_researchers = []
#     retry_count = 0
#     session = requests.Session()
#
#     with tqdm(desc=f"抓取 {institution}", unit="页") as pbar:
#         while True:
#             try:
#                 # 发送请求
#                 response = session.get(base_url, params=params, headers=HEADERS, timeout=30)
#                 response.raise_for_status()
#
#                 # 解析页面
#                 page_researchers, next_token = parse_scholar_page(response.text)
#                 all_researchers.extend(page_researchers)
#
#                 # 更新进度
#                 pbar.update(1)
#                 pbar.set_postfix({'当前学者数': len(all_researchers)})
#
#                 # 检查是否还有下一页
#                 if not next_token or retry_count >= 3:
#                     break
#
#                 # 更新分页参数
#                 params['after_author'] = next_token
#                 time.sleep(10)  # 重要！防止请求过快
#                 retry_count = 0
#
#             except requests.exceptions.RequestException as e:
#                 print(f"请求失败: {str(e)}")
#                 retry_count += 1
#                 time.sleep(30)
#                 if retry_count > 3:
#                     break
#
#     return all_researchers


def process_institutions(institutions):
    """处理机构列表"""
    results = {}
    not_found = []
    stats = {}

    for institution in institutions:
        try:
            researchers = fetch_institution(institution)
            if not researchers:
                not_found.append(institution)
                continue

            # 格式化数据结构
            stats[institution] = len(researchers)
            for r in researchers:
                results[r['name']] = [
                    institution,
                    r['interests'],
                    r['citations']
                ]

        except Exception as e:
            print(f"机构 {institution} 处理失败: {str(e)}")
            not_found.append(institution)

        time.sleep(15)  # 机构间间隔

    return results, not_found, stats


def save_results(data, not_found, stats):
    """保存结果"""
    with open('scholar_data1-10.txt', 'w', encoding='utf-8') as f:
        # 写入学者数据
        f.write("{\n")
        for name, info in data.items():
            line = f'"{name}": {info},\n'
            f.write(line)
        f.write("}\n\n")

        # 写入统计
        f.write(f"未找到的机构: {not_found}\n")
        f.write("各机构结果数:\n")
        for inst, count in stats.items():
            f.write(f"{inst}: {count}\n")


if __name__ == "__main__":
    # 输入示例
    input_institutions = ["Massachusetts Institute of Technology","Imperial College London","University of Oxford","Harvard University","University of Cambridge","Stanford University","ETH Zurich - Swiss Federal Institute of Technology Zurich","National University of Singapore (NUS)","University College London (UCL)","California Institute of Technology (Caltech)"]

    # 执行抓取
    final_data, not_found_list, stats_dict = process_institutions(input_institutions)

    # 保存结果
    save_results(final_data, not_found_list, stats_dict)
    print("执行完成，结果已保存到 scholar_data.txt")