import json
from pypinyin import pinyin, lazy_pinyin

def load_mappings(file_path):
    with open(file_path, 'r',encoding="utf-8") as file:
        data = json.load(file)
    return data

# 加载数据
mappings = load_mappings('name_mappings.json')

# 别名映射
name_mapping = mappings['name_mapping']

# 名称改名（避免歧义）
rename_mapping = mappings['rename_mapping']

# 读取角色分类 JSON 文件
with open('category.json', 'r', encoding='utf-8') as f:
    roles_data = json.load(f)

# 创建角色名称到分类的映射
role_mapping = {}
for category, names in roles_data.items():
    for name in names:
        role_mapping[name] = category

# 读取 yingshentu.json 文件
with open('yingshentu.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 获取所有名称
names = {key: value["Name"] for key, value in data.items()}

# 创建 related_from 和 related_to 列表
for key, value in data.items():
    value["related_from"] = []
    value["related_to"] = []

# 逐个分析 UnitStory
for key, value in data.items():
    unit_story = value["UnitStory"]
    current_name = value["Name"]

    # 添加例外名称
    related_names = [current_name] + name_mapping.get(current_name, [])

    # 处理重命名映射
    renamed_current_names = rename_mapping.get(current_name, [current_name])
    
    for other_key, other_value in data.items():
        if other_key != key:  # 不比较自己
            other_name = other_value["Name"]

            # 检查 UnitStory 是否包含其他名称
            if any(name in unit_story for name in [other_name] + name_mapping.get(other_name, [])):
                # 在 related_to 中添加重命名后的名称
                if other_name in rename_mapping:
                    other_name_renamed = rename_mapping[other_name][0]
                    if other_name_renamed in unit_story:
                        value["related_to"].append(other_name)
                else:
                    # 如果没有在 rename_mapping 中，使用原始名称进行匹配
                    value["related_to"].append(other_name)

            # 使用重命名名称进行匹配
            if any(name in other_value["UnitStory"] for name in renamed_current_names):
                value["related_from"].append(other_name)

            # 检查重命名映射以添加相关角色
            for renamed_name in rename_mapping.get(other_name, []):
                if renamed_name in unit_story:
                    value["related_to"].append(other_name)

# 去重并排序
for key, value in data.items():
    value["related_from"] = sorted(set(value["related_from"]), key=lazy_pinyin)
    value["related_to"] = sorted(set(value["related_to"]), key=lazy_pinyin)


# 计算 heat
for key, value in data.items():
    value["heat"] = 1 + len(value["related_from"]) + len(value["related_to"])

# 打印 heat > 1 的角色名称
heat_filtered = {v["Name"]: v["heat"] for v in data.values() if v["heat"] > 1}
sorted_heat = sorted(heat_filtered.items(), key=lambda x: x[1], reverse=True)

print("Heat > 1 的角色名称及其 heat 值:")
for name, heat in sorted_heat:
    print(f"{name}: {heat}")



# 为每个角色添加 role 字段
for key, value in data.items():
    name = value["Name"]
    # 找到对应的 role
    value["category"] = role_mapping.get(name, None)

for key, value in data.items():
    category = value["category"]
    if not category:
        print(value["Name"])
        

# 输出到新的 JSON 文件
with open('yingshentu_with_heat.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("处理完成，结果已保存到 'yingshentu_with_heat.json'。")

# # 输出到新的 JSON 文件
# with open('yingshentu_with_heat.json', 'w', encoding='utf-8') as f:
#     json.dump(data, f, ensure_ascii=False, indent=4)

# print("处理完成，结果已保存到 'yingshentu_with_heat.json'。")
