import json
import ast
from collections import OrderedDict


def convert_txt_to_json(input_file, output_file):
    """
    将类字典文本转换为结构化JSON
    功能包括：
    1. 自动修复常见格式错误
    2. 转换数据结构
    3. 移除研究领域中的占位符0
    """
    try:
        # 读取原始文件
        with open(input_file, 'r', encoding='utf-8') as f:
            raw_data = f.read().strip()

        # 预处理数据（关键修复步骤）
        raw_data = raw_data.replace('\n', '')  # 移除换行符
        raw_data = raw_data.replace('", [', '", [')  # 统一空格
        raw_data = raw_data.replace('], ', '],\n')  # 增加可读性分隔符

        # 安全解析数据结构
        parsed_data = ast.literal_eval(raw_data)

        # 数据清洗与结构转换
        structured_data = OrderedDict()
        for name, details in parsed_data.items():
            # 验证数据结构
            if len(details) != 3:
                raise ValueError(f"'{name}' 数据结构不完整")

            institution = details[0]
            interests = [i for i in details[1] if isinstance(i, str)]  # 过滤数字0
            citations = details[2]

            # 构建新结构
            structured_data[name] = {
                "institution": institution,
                "research_fields": interests,
                "citation_count": citations,
                "metadata": {
                    "original_format": details  # 保留原始数据以供参考
                }
            }

        # 生成标准JSON
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(structured_data, f,
                      indent=2,
                      ensure_ascii=False,
                      separators=(',', ': '))

        print(f"转换成功！结果已保存至 {output_file}")
        print(f"共处理 {len(structured_data)} 位学者数据")

    except FileNotFoundError:
        print(f"错误：输入文件 {input_file} 不存在")
    except SyntaxError as e:
        print(f"格式错误：{e}\n请检查以下位置附近的语法：")
        print(raw_data[max(0, e.offset - 50):e.offset + 50])
    except Exception as e:
        print(f"处理过程中发生错误：{str(e)}")


if __name__ == "__main__":
    # 配置参数
    input_filename = "scholar_data1-10fixed.txt"
    output_filename = "structured_scholar_data1-10fixed.json"

    # 执行转换
    convert_txt_to_json(input_filename, output_filename)