import json
import re

o = json.load(open("1.txt", "r", encoding="utf-8"))["StringKVMapDesc"]
data = {}
for i in o:
    if i.startswith("CardDesc."):
        uid = i[9:15]
        data[uid] = {}
        data[uid]["Name"] = o[f"CardDesc.{uid}.UnitName"]
        try:
            data[uid]["Poetry"] = o[f"CardDesc.{uid}.UnitPoetry"]
        except:
            print(o[f"CardDesc.{uid}.UnitName"])
        data[uid]["StoryBrief"] = o[f"CardDesc.{uid}.StoryBrief"]
        data[uid]["UnitStory"] = o[f"CardDesc.{uid}.CardStory__0.UnitStory"]

json.dump(data, open("yingshentu.json", "w", encoding="utf-8"), indent=4, ensure_ascii=False)

for uid in data:
    pass