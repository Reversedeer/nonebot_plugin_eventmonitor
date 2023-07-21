import os
import nonebot
import json


g_temp = {}

async def init(g_temp):
    """
    初始化配置文件
    :return:
    """  
    if not os.path.exists("data/eventmonitor/config.json"):  # 读取用户数据
        os.makedirs("data/eventmonitor")  # 创建文件夹

        bot = nonebot.get_bot()
        group_list = (await bot.get_group_list())
        
        for group in group_list:
            gid = str(group["group_id"])
            temp = {}
            for g_name in path:
                temp[g_name] = True
                if g_name in ['red_package']:
                    temp[g_name] = False
            g_temp[gid] = temp

            with open('data/eventmonitor/config.json', 'w', encoding='utf-8') as f:  # 将更新后的配置信息写回配置文件 JSON
                json.dump(g_temp, f, indent=4)

    if os.path.exists("data/eventmonitor/config.json"):
        with open('data/eventmonitor/config.json', 'r', encoding='utf-8') as f:
            g_temp.update(json.load(f))

    
    #  # 设置数据文件路径
    # self.date_path = "./data/eventmonitor"  

    # # 如果数据文件路径不存在，则创建目录，并初始化群组数据为空字典，并写入对应的文件
    # if not os.path.exists(self.date_path):  
    #     os.makedirs(self.date_path)  
    #     self.g_temp = {}
    #     self.write_group_data()
        
    #     bot = nonebot.get_bot()
    #     group_list = (await bot.get_group_list())
        
    #     for group in group_list:
    #         temp = {}
    #         for g_name in path:
    #             temp[g_name] = True
    #             if g_name in ['red_package']:
    #                 temp[g_name] = False
    #         gid = str(group["group_id"])
    #         g_temp[gid] = temp
    #     write_group_data(g_temp)

    # elif os.path.exists(f"{self.data_path}/config.json"):
    #     # 如果数据文件路径存在，尝试读取数据文件（config.json）
    #     with open(f"{self.data_path}/config.json", "r", encoding="utf-8") as f:
    #         self.g_temp = json.load(f)
    # else:
    #         # 如果群数据文件不存在，则初始化self.g_temp为空字典，并写入对应的文件
    #     self.g_temp = {}
    #     self.write_group_data()

async def check_chuo(g_temp, gid: str) -> bool: #检查戳一戳是否允许
    if gid in g_temp and not g_temp[gid]["chuo"]:
        return False
    return g_temp[gid]["chuo"]

async def check_honor(g_temp, gid: str) -> bool:#检查群荣誉是否允许 
    if gid in g_temp and not g_temp[gid]["honor"]:
        return False
    return g_temp[gid]["honor"]

async def check_file(g_temp, gid: str) -> bool:#检查群文件是否允许 
    if gid in g_temp and not g_temp[gid]["file"]:
        return False
    return g_temp[gid]["file"]

async def check_del_user(g_temp, gid: str) -> bool:#检查群成员减少是否允许 
    if gid in g_temp and not g_temp[gid]["del_user"]:
        return False
    return g_temp[gid]["del_user"]

async def check_add_user(g_temp, gid: str) -> bool:#检查群成员增加是否允许 
    if gid in g_temp and not g_temp[gid]["add_user"]:
        return False
    return g_temp[gid]["add_user"]

async def check_admin(g_temp, gid: str) -> bool:#检查管理员是否允许 
    if gid in g_temp and not g_temp[gid]["admin"]:
        return False
    return g_temp[gid]["admin"]

async def check_red_package(g_temp, gid: str) -> bool:#检查运气王是否允许 
    if gid in g_temp and not g_temp[gid]["red_package"]:
        return False
    return g_temp[gid]["red_package"]

try:
    chuo_cd = nonebot.get_driver().config.chuo_cd
except Exception:
    chuo_cd = 0    #戳一戳cd默认值
  
config = nonebot.get_driver().config #从 配置文件中获取SUPERUSER, NICKNAME
superusers = {int(uid) for uid in config.superusers}
nickname = next(iter(config.nickname))
chuo_CD_dir = {}   #戳一戳cd,感觉很鸡肋，自行调整
driver = nonebot.get_driver()


path = {
    'chuo': ['戳一戳'],
    'honor': ['群荣誉'],
    'files': ['群文件'],
    'del_user': ['群成员减少'],
    'add_user': ['群成员增加'],
    'admin': ['管理员变动'],
    'red_package': ['运气王变动']
}

notAllow = "功能未开启"




        


