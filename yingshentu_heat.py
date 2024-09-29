import json

# 定义例外处理
name_mapping = {
    "二郎显圣真君": ["二郎神"],
    "猪八戒": ["八戒"],
    "大圣残躯": ["悟空", "斗战神佛", "齐天大圣"],
    "魔将·妙音": ["魔将", "一将"],
    "魔将·劫波": ["魔将", "四将"],
    "魔将·妄相": ["魔将", "三将"],
    "魔将·莲眼": ["魔将", "二将"],
}

# 新增重命名映射
rename_mapping = {
    "不能": ["二师兄不能"]
}

# 读取 JSON 文件
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
                value["related_to"].append(other_name)

            # 使用重命名名称进行匹配
            if any(name in other_value["UnitStory"] for name in renamed_current_names):
                value["related_from"].append(other_name)

# 去重
for key, value in data.items():
    value["related_from"] = list(set(value["related_from"]))
    value["related_to"] = list(set(value["related_to"]))

# 计算 heat
for key, value in data.items():
    value["heat"] = 1 + len(value["related_from"]) + len(value["related_to"])

# 打印 heat > 1 的角色名称
heat_filtered = {v["Name"]: v["heat"] for v in data.values() if v["heat"] > 1}
sorted_heat = sorted(heat_filtered.items(), key=lambda x: x[1], reverse=True)

print("Heat > 1 的角色名称及其 heat 值:")
for name, heat in sorted_heat:
    print(f"{name}: {heat}")

# 输出到新的 JSON 文件
with open('yingshentu_with_heat.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("处理完成，结果已保存到 'yingshentu_with_heat.json'。")
