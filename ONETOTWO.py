def convert_quotes(input_file, output_file):
    """安全替换单引号（不处理转义字符）"""
    try:
        with open(input_file, 'r', encoding='utf-8') as f_in:
            content = f_in.read()

        # 只替换单独出现的单引号（非转义字符）
        converted = content.replace("'", '"')

        with open(output_file, 'w', encoding='utf-8') as f_out:
            f_out.write(converted)
        print(f"替换完成 → {output_file}")

    except Exception as e:
        print(f"错误：{str(e)}")


# 使用示例
convert_quotes('scholar_data1-10.txt', 'scholar_data1-10fixed.txt')