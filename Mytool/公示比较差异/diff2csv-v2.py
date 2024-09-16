# 用于公示的翻译改动表格生成程序
# 输入en_us.json zh_cn-old.json zh_cn.json [en_us-old.json]
# 输出 diff.csv 包含翻译修改， new.csv 包含新增翻译， changes-diff.csv 包含变化

import json
import csv
import os

# 定义一个函数来转义换行符
def escape_newlines(data):
    return {key: value.replace('\n', '\\n') for key, value in data.items()}

# 定义一个函数来写入变化
def write_changes(writer, key, en_us_old_value, en_us_value, zh_cn_old_value, zh_cn_value):
    writer.writerow([key, en_us_old_value, en_us_value, zh_cn_old_value, zh_cn_value])

# 读取JSON文件并比较
def compare_json_files(en_us_file, zh_cn_old_file, zh_cn_file, en_us_old_file=None):
    en_us = escape_newlines(json.load(open(en_us_file, 'r', encoding='utf-8')))
    zh_cn_old = escape_newlines(json.load(open(zh_cn_old_file, 'r', encoding='utf-8')))
    zh_cn = escape_newlines(json.load(open(zh_cn_file, 'r', encoding='utf-8')))

    # 尝试读取 en_us-old.json 文件
    en_us_old = {}
    if en_us_old_file and os.path.exists(en_us_old_file):
        en_us_old = escape_newlines(json.load(open(en_us_old_file, 'r', encoding='utf-8')))

    with open('diff.csv', 'w', newline='', encoding='utf-8') as difffile, \
         open('new.csv', 'w', newline='', encoding='utf-8') as newfile, \
         open('changes-diff.csv', 'w', newline='', encoding='utf-8') as changesfile:

        diff_writer = csv.writer(difffile)
        new_writer = csv.writer(newfile)
        changes_writer = csv.writer(changesfile)

        # 写入标题行
        header = ['Key', 'en_us', 'zh_cn-old', 'zh_cn']
        diff_writer.writerow(header)
        new_writer.writerow(header)
        changes_writer.writerow(['Key', 'en_us-old', 'en_us', 'zh_cn-old', 'zh_cn'])

        # 遍历 en_us 的所有 key
        for key in en_us:
            en_value = en_us[key]
            zh_old_value = zh_cn_old.get(key, '🚫')
            zh_value = zh_cn.get(key, '🚫')
            en_old_value = en_us_old.get(key, '🚫')

            # 写入数据
            if zh_old_value == "🚫" or zh_value == "🚫":
                new_writer.writerow([key, en_value, zh_old_value, zh_value])
            elif zh_old_value != zh_value:
                diff_writer.writerow([key, en_value, zh_old_value, zh_value])

            # 处理en_us-old与en_us的比较
            if en_us_old and en_old_value != '🚫' and en_old_value != en_value:
                write_changes(changes_writer, key, en_old_value, en_value, zh_old_value, zh_value)

        # 遍历 en_us-old 的所有 key
        if en_us_old:
            for key in en_us_old:
                if key not in en_us:
                    en_old_value = en_us_old[key]
                    zh_old_value = zh_cn_old.get(key, '🚫')
                    zh_value = zh_cn.get(key, '🚫')
                    write_changes(changes_writer, key, en_old_value, '', zh_old_value, zh_value)

# 示例用法
compare_json_files('en_us.json', 'zh_cn-old.json', 'zh_cn.json', 'en_us-old.json')