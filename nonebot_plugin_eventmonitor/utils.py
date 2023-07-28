import os
import nonebot
import json
from pathlib import Path
from typing import Optional

g_temp = {}
chuo_CD_dir = {}

config_path = Path() / 'data/eventmonitor'
address = config_path / 'config.json'

driver = nonebot.get_driver()
#从 配置文件中获取SUPERUSER, NICKNAME
config = nonebot.get_driver().config
superusers = {int(uid) for uid in config.superusers}
nickname = next(iter(config.nickname))
#戳一戳cd,感觉很鸡肋，自行调整

notAllow = "功能未开启"


async def init(g_temp):
    """
    初始化配置文件
    :return:
    """   
    # 如果数据文件路径不存在，则创建目录
    if not os.path.exists(config_path):  
        os.makedirs(config_path)  
    if os.path.exists(address):
        # 如果数据文件路径存在，尝试读取数据文件（config.json）
        with open(address, "r", encoding="utf-8") as f:
            g_temp.update(json.load(f))
    else:
        # 如果群数据文件不存在，则初始化g_temp为空字典，并写入对应的文件
        bot = nonebot.get_bot()
        group_list = await bot.get_group_list()
        #从group_list中遍历每个群组
        for group in group_list:
            # 为每个群组创建一个临时字典temp，用于存储群组的配置信息
            temp = {}
            for g_name in path:
                # 将群组的每个配置项设置为默认值True
                temp[g_name] = True
                # 特殊情况下（g_name为'red_package'），将该配置项设为False
                if g_name in ['red_package']:
                    temp[g_name] = False
            # 获取群组ID并转换为字符串类型
            gid = str(group["group_id"])
            # 将临时字典temp作为值，群组ID作为键，添加到g_temp字典中
            g_temp[gid] = temp
            # 将更新后的g_temp字典写入群组数据
            write_group_data(g_temp)


async def config_check():
    global g_temp
    # 获取机器人实例
    bot = nonebot.get_bot()
    # 获取所有群组的列表
    group_list = await bot.get_group_list()
    # 加载配置文件，得到一个包含配置信息的字典
    with open(address, "r", encoding="utf-8") as f:
        config_dict = json.load(f)  
    # 遍历所有群组
    for group in group_list:
        gid = str(group['group_id']) 
        # 如果配置字典中没有该群组的信息，将其添加到配置字典中
        if not config_dict.get(gid):
            config_dict[gid] = {}
            # 遍历配置文件路径中的所有配置项，并初始化为默认值
            for group_name in path:
                config_dict[gid][group_name] = True
                # 特殊情况下（group_name为'red_package'），将该配置项设为False
                if group_name in ['red_package']:
                    config_dict[gid][group_name] = False
        else:
            # 如果配置字典中已存在该群组的信息，检查是否有缺失的配置项，并添加默认值
            other_group = config_dict[gid]
            for group_name in path:
                if other_group.get(group_name) is None:
                    other_group[gid][group_name] = True
                    # 特殊情况下（group_name为'red_package'），将该配置项设为False
                    if group_name in ['red_package']:
                        other_group[gid][group_name] = False
    g_temp.update(config_dict)
    # 将更新后的配置字典上传到配置文件中
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
        print(g_temp)
        return False
    return g_temp[gid]["honor"]

#检查群文件是否允许 
async def check_file(g_temp, gid: str) -> bool:
    if gid in g_temp and not g_temp[gid]["files"]:
        return False
    return g_temp[gid]["files"]

#检查群成员减少是否允许 
async def check_del_user(g_temp, gid: str) -> bool:
    if gid in g_temp and not g_temp[gid]["del_user"]:
        return False
    print(g_temp)
    return g_temp[gid]["del_user"]

#检查群成员增加是否允许
async def check_add_user(g_temp, gid: str) -> bool:
    if gid in g_temp and not g_temp[gid]["add_user"]:
        return False
    print(g_temp)
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

#根据关键词获取对应功能名称
def get_function_name(key: str) -> str:
    return path[key][0]

#根据指令内容获取开关类型
def get_command_type(command: str) -> str:
    return next(
        (
            key
            for key, keywords in path.items()
            if any(keyword in command for keyword in keywords)
        ),
        "",
    )

#戳一戳cd默认值    
try:
    chuo_cd = nonebot.get_driver().config.chuo_cd
except Exception:
    chuo_cd = 0   
 

path = {
    'chuo': ['戳一戳'],
    'honor': ['群荣誉检测'],
    'files': ['群文件检测'],
    'del_user': ['群成员减少检测'],
    'add_user': ['群成员增加检测'],
    'admin': ['管理员变动检测'],
    'red_package': ['运气王检测']
}

class Utils:
    usage = """
    指令1：戳一戳(戳一戳bot获取文案)
    指令2：群荣誉监测(检测群聊中龙王，群聊之火，快乐源泉的获得并发送提示，当 bot获得群荣誉时有特殊消息)
    指令3：群文件检测(检测所有人发送群文件并发送提示)
    指令4：群成员减少检测(当有人退群时，发送退群消息；当主人/superuser退群有特殊回复)
    指令5：群成员增加检测(当有人入群时，发送入群欢迎，当bot首次入群会乞讨管理，当主人/superuser入群会有特殊回复)
    指令6：管理员变动检测(当新增管理员或取消管理员时发送消息提示，当bot自身被上/下管理时有特殊回复)
    指令7：运气王检测(检测抢红包检测后的运气王并发送提示消息)
    """
utils = Utils()