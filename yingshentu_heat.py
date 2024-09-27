import json
import jieba
import jieba.posseg as pseg

# 1. 读取本地的 JSON 文件
with open('yingshentu.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 2. 使用 Jieba 进行热度值统计
# 初始化热度值
occurrence_count = {data[key]["Name"]: 1 for key in data}  # 默认值为 0

# 定义例外处理
name_mapping = {
    "二郎显圣真君": "二郎神"
}

# 遍历数据以计算出现次数
for key in data:
    unit_story = data[key]["UnitStory"] or ""
    # 使用 Jieba 进行词性标注
    words = pseg.lcut(unit_story)
    
    # 使用集合来跟踪已经计数的角色
    counted_names = set()

    for other_key in data:
        if other_key != key:
            name = data[other_key]["Name"]
            # 处理例外
            mapped_name = name_mapping.get(name, name)  # 如果是例外，则使用映射的名称
            # 检查词性是否为名词
            for word, flag in words:
                if word == mapped_name and flag.startswith('n'):  # 'n'表示名词
                    if name not in counted_names:  # 确保只计数一次
                        occurrence_count[name] += 1  # 使用原始名称增加热度值
                        counted_names.add(name)  # 将角色添加到集合中

# 将热度值写入 JSON 数据中（使用原始名称）
for key in data:
    name = data[key]["Name"]
    data[key]["Heat"] = occurrence_count[name]  # 写入原始名称的热度值

# 保存更新后的 JSON 文件
with open('yingshentu_with_heat.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

# 3. 导出只包含 key、name 和 UnitStory 的 JSON 文件
export_data = {key: {"Name": data[key]["Name"], "UnitStory": data[key]["UnitStory"]} for key in data}

with open('yingshentu_export.json', 'w', encoding='utf-8') as f:
    json.dump(export_data, f, ensure_ascii=False, indent=4)

# 4. 根据热度值排序并打印热度值大于 1 的角色名称
sorted_names = sorted(
    [(name, occurrence_count[name]) for name in occurrence_count if occurrence_count[name] > 1],
    key=lambda x: x[1],
    reverse=True
)

print("热度值大于 1 的角色名称及其热度值：")
for name, heat in sorted_names:
    print(f"{name}: {heat}")
