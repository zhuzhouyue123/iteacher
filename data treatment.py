import json
from fuzzywuzzy import fuzz


def load_data(filename):
    """加载学者数据文件"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            # 处理非标准JSON格式（允许单引号）
            data_str = f.read().replace("'", '"')
            return json.loads(data_str)
    except FileNotFoundError:
        print(f"错误：文件 {filename} 未找到")
        exit()
    except json.JSONDecodeError:
        print("错误：文件格式不正确")
        exit()


def fuzzy_match(query, field, threshold=70):
    """执行模糊匹配，返回匹配得分"""
    return fuzz.partial_ratio(query.lower(), field.lower()) >= threshold


def filter_researchers(data, min_cites, max_cites, fields):
    """执行过滤操作"""
    results = []

    for name, details in data.items():
        institution = details[0]
        interests = details[1][1:] if len(details[1]) > 1 else []  # 去掉开头的0
        citations = details[2]

        # 检查引用数范围
        if not (min_cites <= citations <= max_cites):
            continue

        # 检查研究领域匹配
        field_matched = False
        if fields:  # 如果有指定领域才检查
            for interest in interests:
                if any(fuzzy_match(field, interest) for field in fields):
                    field_matched = True
                    break
        else:  # 未指定领域视为匹配
            field_matched = True

        if field_matched:
            results.append({
                'name': name,
                'institution': institution,
                'interests': interests,
                'citations': citations
            })

    return results


def main():
    # 用户输入
    min_c = int(input("请输入最小引用数："))
    max_c = int(input("请输入最大引用数："))
    fields_input = input("请输入研究领域（多个用逗号分隔，留空则不限）：").strip()
    fields = [f.strip() for f in fields_input.split(',')] if fields_input else []

    # 加载数据
    data = load_data('scholar_data1-10fixed.txt')

    # 执行过滤
    filtered = filter_researchers(data, min_c, max_c, fields)

    # 输出结果
    print(f"\n找到 {len(filtered)} 位符合条件的学者：")
    for idx, res in enumerate(filtered, 1):
        print(f"\n【{idx}】{res['name']}")
        print(f"所属机构：{res['institution']}")
        print(f"引用次数：{res['citations']:,}")
        print(f"研究领域：{', '.join(res['interests']) if res['interests'] else '无记录'}")


if __name__ == "__main__":
    # 安装依赖：pip install fuzzywuzzy python-Levenshtein
    main()












