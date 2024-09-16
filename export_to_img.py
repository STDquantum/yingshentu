from PIL import Image
import os
import json
import numpy as np

path = r"D:\download\fmodel工具包解压密码dauercom\FModel\Output\Exports\b1\Content\00MainHZ\UIDev\TravelNotes\MBookPicture"

p = os.listdir(path)
data: dict = json.load(open("yingshentu.json", "r", encoding="utf-8"))

yingshentu_shunxu = ["小妖", "狼斥候", "狼剑客", "狼校卫", "狼力士", "狼弓手", "狼侍卫", "狼刺客", "小呱呱", "鸦香客", "山匪头子", "骨嶙峋", "蛇巡司", "小菌君", "小人参精", "鼠弩手", "鼠校卫", "鼠司空", "鼠都尉", "鼠禁卫", "石磷磷", "石苍苍", "石双双", "骨灵精", "骨悚然", "疾蝠", "干尸", "鼬侍郎", "狸侍长", "小灵芝精", "支应僧", "戒刀僧", "提炉僧", "迎客僧", "监院僧", "双刀僧", "青蝠", "雪僵尸", "巡山鬼", "穿云鬼", "冻饿鬼", "赤发鬼", "掌灯狱使", "夜叉奴", "隼居士", "狼护法", "鳖宝", "雷长老", "焦面鬼王", "泥塑金刚", "地莲精", "巫山小妖", "傀蛛士", "儡蜱士", "幽灯鬼", "蜢虫精", "蜻蜓精", "蚂蜂精", "虫校尉", "石蛛", "琴螂幼虫", "利爪茧", "蝎太子", "御剑道士", "拂尘道士", "执杖道士", "蛇司药", "蛇捕头", "虫羽士", "青冉冉", "阴兵·力士", "阴兵·弓手", "阴兵·火牛", "阴兵·焦尸", "阴兵·黑脸鬼", "焰蝠", "牛侍长", "牛校卫", "牛力士", "火烈烈", "炎赫赫", "火灵童子", "行什", "地罗刹", "海罗刹", "火长老", "牯都督", "鹰天兵", "犬天兵", "豺天兵", "天将", "头目", "牯护院", "广智", "广谋", "波里个浪", "浪里个波", "地狼", "沙国王父子", "沙大郎", "石母", "虎伥", "百目真人", "疯虎", "“虎先锋”", "魔将·莲眼", "魔将·妄相", "魔将·劫波", "无量蝠", "浪里个浪", "老人参精", "不白", "不净", "不能", "不空", "海上僧", "赤尻马猴", "六妹", "五妹", "四姐", "三姐", "二姐", "大姐", "琴螂仙", "百足虫", "右手虫", "波里个波", "虫总兵", "靡道人", "五行战车", "石父", "急如火、快如风", "云里雾、雾里云", "兴烘掀、掀烘兴", "燧统领", "燧先锋", "火灵元母", "波浪浪", "石子", "毒统领", "水木兽", "跳浪蛟", "浪波波", "金甲犀", "步云鹿", "凤翅将军", "碧臂螂", "妖王", "灵虚子", "赤髯龙", "金池长老", "黑风大王", "黑熊精", "虎先锋", "石先锋", "石敢当", "小骊龙", "蝜蝂", "黄风大圣", "亢金龙", "亢金星君", "魔将·妙音", "青背龙", "黄眉", "紫蛛儿", "小黄龙", "毒敌大王", "晦月魔君", "百眼魔君", "阴阳鱼", "璧水金睛兽", "红孩儿", "夜叉王", "大石敢当", "人物", "白衣秀士", "黑风山土地", "石中人", "黄袍员外", "无头僧", "灵吉菩萨", "龟将", "灵狐", "翠笠武师", "小张太子", "小西天土地", "猪八戒", "黑手道人", "鹤仙人", "红依", "火焰山土地", "马天霸", "皓斧力士", "萍萍", "铁扇公主", "牛魔王", "王灵官", "通臂猿猴", "寅虎", "辰龙", "申猴", "戌狗", "老猴子", "弥勒", "二郎显圣真君", "大圣残躯", "袁守诚"]
# data_keys = sorted(list(data.keys()), key=lambda x: int(x))
data_keys = sorted(list(data.keys()), key=lambda x: yingshentu_shunxu.index(data[x]["Name"]))
print([data[i]["Name"] for i in data_keys])


def combine():
    for uid in data_keys:
        # if data[uid]["Name"] != "波里个浪" and data[uid]["Name"] != "虎先锋":
        #     continue
        print(f"{uid}_{data[uid]['Name']}")
        # 读取文件
        ori_image = Image.open(f"{path}\\T_book_{uid}_t.png")
        mask_image = Image.open(f"{path}\\T_book_{uid}_mask.png")
        mask_image = mask_image.resize(ori_image.size)  # 1024x1024 -> 2048x2048
        # ori_image = ori_image.resize(mask_image.size)  # 2048x2048 -> 1024x1024

        # 去掉绿色
        r, g, b, a = mask_image.split()
        black_channel = Image.new("L", mask_image.size, 0)
        mask_image = Image.merge("RGBA", (r, black_channel, b, a))

        blue_circle = (
            f"T_book_{uid}_stroke.png" in p
            and data[uid]["Name"] != "波里个浪"
            and data[uid]["Name"] != "虎先锋"
        )
        mask_data = mask_image.getdata()
        new_data = []
        for item in mask_data:
            if item[:3] == (0, 0, 0):  # 如果是黑色像素
                new_data.append((0, 0, 0, 0))  # 替换为透明
            elif blue_circle and item[2]:  # 如果是蓝圈
                new_data.append((91, 16, 0, item[2]))  # 替换为灰度
            elif not blue_circle and item[0]:  # 红圈
                new_data.append((91, 16, 0, item[0]))  # 替换为灰度
            elif blue_circle and item[0]:  # 如果是红诗或者描边
                new_data.append((40, 40, 40, item[0]))  # 替换为灰度
            elif not blue_circle and item[2]:  # 如果是蓝诗
                new_data.append((40, 40, 40, item[2]))  # 替换为灰度
            else:
                new_data.append((0, 0, 0, item[3]))
        mask_image.putdata(tuple(new_data))
        # mask_image.save("test\\1.png")

        # result_name = f"result\\{uid}_{data[uid]['Name']}.png"
        # result_image = Image.alpha_composite(ori_image, mask_image)
        # result_image = result_image.resize((2048, 3072))
        # result_image.save(result_name)

        # result_name = f"full\\{uid}_{data[uid]['Name']}.png"
        # result_image = Image.alpha_composite(ori_image, mask_image)
        # result_image = result_image.resize((2048, 3072))
        # bg = Image.open("T_PSD_ShuJi_01_D.png").resize((2048, 3072))
        # result_image = Image.alpha_composite(bg, result_image)
        # result_image.save(result_name)

        result_name = f"result_comp\\{uid}_{data[uid]['Name']}.png"
        result_image = Image.alpha_composite(ori_image, mask_image)
        result_image = result_image.resize((600, 900))
        result_image.save(result_name)


def export():
    md_text = "# 影神图\n\n"
    md_text += "[TOC]\n\n"
    for uid in data_keys:
        md_text += f"## {data[uid]['Name']}\n\n"
        if "Poetry" in data[uid]:
            poetry = data[uid]["Poetry"].replace("\r\n", "\n\n")
            md_text += f"诗曰：\n\n{poetry}\n\n"
        md_text += f"![](./result/{uid}_{data[uid]['Name']}.png)\n\n"
        # md_text += f"<img alt=\"\" style=\"height:600;\" data-src=\".\\result_comp\\{uid}_{data[uid]['Name']}.png\" />\n\n"
        md_text += data[uid]["UnitStory"].replace("\r\n", "\n")
        md_text += "\n\n"

    open("yingshentu.md", "w", encoding="utf-8").write(md_text)
    open("README.md", "w", encoding="utf-8").write(md_text.replace("result", "result_comp"))


# import markdown

# html = markdown.markdown(md_text)
# open("index.html", "w", encoding="utf-8").write(html)
if __name__ == "__main__":
    combine()
    export()
