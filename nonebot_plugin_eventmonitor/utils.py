import os
import nonebot
import json
from pathlib import Path
from typing import Optional

g_temp = {}
config_path = Path() / 'data/eventmonitor'
address = config_path / 'config.json'

async def init(g_temp):
    """
    初始化配置文件
    :return:
    """   
    # 如果数据文件路径不存在，则创建目录，并初始化群组数据为空字典，并写入对应的文件
    if not os.path.exists(config_path):  
        os.makedirs(config_path)  
    if os.path.exists(address):
        # 如果数据文件路径存在，尝试读取数据文件（config.json）
        with open(address, "r", encoding="utf-8") as f:
            g_temp.update(json.load(f))
    else:
        # 如果群数据文件不存在，则初始化g_temp为空字典，并写入对应的文件
        bot = nonebot.get_bot()
        group_list = (await bot.get_group_list())
            
        for group in group_list:
            temp = {}
            for g_name in path:
                temp[g_name] = True
                if g_name in ['red_package']:
                    temp[g_name] = False
            gid = str(group["group_id"])
            g_temp[gid] = temp
            write_group_data(g_temp)


async def config_check():
    bot = nonebot.get_bot()
    group_list = (await bot.get_group_list())
    config_dict = json_load(address)
    for group in group_list:
        gid = str(group['group_id'])
        if not config_dict.get(gid):
            config_dict[gid] = {}
            for group_name in path:
                config_dict[gid][group_name] = True
                if group_name in ['red_package']:
                    config_dict[gid][group_name] = False
        else:
            other_group = config_dict[gid]
            for group_name in path:
                if other_group.get(group_name) is None:
                    other_group[gid][group_name] = True
                    if group_name in ['red_package']:
                        other_group[gid][group_name] = False
    json_upload(address, config_dict)


def json_load(path) -> Optional[dict]:
    """
    加载json文件
    :return: Optional[dict]
    """
    try:
        with open(path, mode='r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return None


def json_upload(path, dict_content) -> None:
    """
    更新json文件
    :param path: 路径
    :param dict_content: python对象，字典
    """
    with open(path, mode='w', encoding='utf-8') as c:
        c.write(json.dumps(dict_content, ensure_ascii=False, indent=4))

#写入群配置
def write_group_data(g_temp):
    with open('data/eventmonitor/config.json', 'w', encoding='utf-8') as f:
        json.dump(g_temp, f, indent=4, ensure_ascii=False)

#检查戳一戳是否允许
async def check_chuo(g_temp, gid: str) -> bool: 
    if gid in g_temp and not g_temp[gid]["chuo"]:
        return False
    return g_temp[gid]["chuo"]
#检查群荣誉是否允许 
async def check_honor(g_temp, gid: str) -> bool:
    if gid in g_temp and not g_temp[gid]["honor"]:
        return False
    return g_temp[gid]["honor"]
#检查群文件是否允许 
async def check_file(g_temp, gid: str) -> bool:
    if gid in g_temp and not g_temp[gid]["file"]:
        return False
    return g_temp[gid]["file"]
#检查群成员减少是否允许 
async def check_del_user(g_temp, gid: str) -> bool:
    if gid in g_temp and not g_temp[gid]["del_user"]:
        return False
    return g_temp[gid]["del_user"]
#检查群成员增加是否允许
async def check_add_user(g_temp, gid: str) -> bool:
    if gid in g_temp and not g_temp[gid]["add_user"]:
        return False
    return g_temp[gid]["add_user"]
#检查管理员是否允许
async def check_admin(g_temp, gid: str) -> bool:
    if gid in g_temp and not g_temp[gid]["admin"]:
        return False
    return g_temp[gid]["admin"]
#检查运气王是否允许
async def check_red_package(g_temp, gid: str) -> bool:
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
notAllow = "功能未开启"

path = {
    'chuo': ['戳一戳'],
    'honor': ['群荣誉检测'],
    'files': ['群文件检测'],
    'del_user': ['群成员减少检测'],
    'add_user': ['群成员增加检测'],
    'admin': ['管理员变动检测'],
    'red_package': ['运气王检测']
}