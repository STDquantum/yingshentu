import requests
import json
import re

# 读取 README 文件
url = "https://raw.githubusercontent.com/meethigher/black-wukong-youji/refs/heads/master/%E9%BB%91%E7%A5%9E%E8%AF%9D%E6%82%9F%E7%A9%BA%E5%A6%96%E6%80%AA%E5%B9%B3%E7%94%9F%E5%BD%95.md"
response = requests.get(url)
content = response.text

# 初始化角色字典
roles = {
    "小妖": [],
    "头目": [],
    "妖王": [],
    "人物": []
}

# 解析内容
current_category = None

for line in content.splitlines():
    line = line.strip()
    if line.startswith("# "):  # 一级目录
        current_category = line[2:]  # 获取分类名称
        # 去掉数字前缀
        if "、" in current_category:
            current_category = current_category.split("、")[1]  
        print(f"当前分类: {current_category}")
        if current_category not in roles:
            roles[current_category] = []
    elif line.startswith("## "):  # 二级目录
        match = re.match(r"## \d+\.\d+ (.+)", line)
        if match:
            role_name = match.group(1)  # 获取角色名称
            print(f"角色名称: {role_name}")
            roles[current_category].append(role_name)
            print(f"添加角色: {role_name} 到 {current_category}")





# 输出为 JSON 文件
print("角色分类结果:", roles)  # Debug 输出
with open('category.json', 'w', encoding='utf-8') as json_file:
    json.dump(roles, json_file, ensure_ascii=False, indent=4)

print("JSON 文件已生成：roles.json")
