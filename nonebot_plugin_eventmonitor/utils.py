"""依赖文件"""
import os
import json
import nonebot

from pathlib import Path

from nonebot.adapters.onebot.v11 import (
    Event,
    PokeNotifyEvent,
    HonorNotifyEvent,
    GroupUploadNoticeEvent,
    GroupDecreaseNoticeEvent,
    GroupIncreaseNoticeEvent,
    GroupAdminNoticeEvent,
    LuckyKingNotifyEvent,

)

class Utils:
    def __init__(self) -> None:
        self.usage = """
            指令1：戳一戳(戳一戳bot获取文案)
            指令2：群荣誉监测(检测群聊中龙王，群聊之火，快乐源泉的获得并发送提示，当 bot获得群荣誉时有特殊消息)
            指令3：群文件检测(检测所有人发送群文件并发送提示)
            指令4：群成员减少检测(当有人退群时，发送退群消息；当主人/superuser退群有特殊回复)
            指令5：群成员增加检测(当有人入群时，发送入群欢迎，当bot首次入群会乞讨管理，当主人/superuser入群会有特殊回复)
            指令6：管理员变动检测(当新增管理员或取消管理员时发送消息提示，当bot自身被上/下管理时有特殊回复)
            指令7：运气王检测(检测抢红包检测后的运气王并发送提示消息)
            指令8：更新插件eventmonitor
            指令9：重启
            指令10：event配置"""
        self.notAllow = '功能未开启'
        self.path = {
            'chuo': ['戳一戳'],
            'honor': ['群荣誉检测'],
            'files': ['群文件检测'],
            'del_user': ['群成员减少检测'],
            'add_user': ['群成员增加检测'],
            'admin': ['管理员变动检测'],
            'red_package': ['运气王检测']
            }
        self.g_temp = {}
        self.chuo_CD_dir = {}
        self.config_path = Path() / 'data/eventmonitor'
        self.address = self.config_path / 'config.json'
        config = nonebot.get_driver().config
        self.superusers: set[int] = {int(uid) for uid in config.superusers}
        self.nickname: str = next(iter(config.nickname), "Bot")
        self.chuo_cd: int = getattr(config, "chuo_cd", 10)
        self.check_bot_update: bool = getattr(config, "isalive", True)
        self.check_txt_img:bool = getattr(config, "event_img", False)
        self.current_version = '0.3.2'
        #戳一戳文案
        self.chuo_msg = [
            f"别戳了，{self.nickname}怕疼QwQ",
            f"呜呜，再戳{self.nickname}脸都要肿了",
            f"戳坏了{self.nickname}，你赔得起吗？",
            f"再戳{self.nickname}，我要叫我主人了",
            f"别老戳{self.nickname}了，您歇会吧~",
            f"再戳{self.nickname}，咬你了嗷~",
            f"请不要戳{self.nickname} >_<",
            f"喂(#`O′) 戳{self.nickname}干嘛！",
            "想好了再戳，(*-`ω´-)✄",
            "喂，110吗，有人老戳我",
            "嗷呜嗷呜...恶龙咆哮┗|｀O′|┛",
            "有事恁叫我，别天天一个劲戳戳戳！",
            "再戳我让你变成女人，嘿嘿",
            "不要戳我了 >_<",
            "不要这样子啦(*/ω＼*)",
            "不要再戳了(害怕ing)",
            "还戳，哼(つд⊂)（生气）",
            "再戳，小心我顺着网线找你.",
            "咱要型气了o(>﹏<)o",
            "嘿嘿，好舒服呀(bushi)",
            "乖，好了好了，别戳了~",
            "我爪巴爪巴，球球别再戳了",
            "别再戳我了，行🐎？！",
            "啊呜，你有什么事吗？",
            "lsp你再戳？",
            "连个可爱美少女都要戳的肥宅真恶心啊。",
            "你再戳！",
            "？再戳试试？",
            "别戳了别戳了再戳就坏了555",
            "我爪巴爪巴，球球别再戳了",
            "你戳你🐎呢？！",
            "放手啦，不给戳QAQ",
            "戳坏了，赔钱！",
            "戳坏了",
            "嗯……不可以……啦……不要乱戳",
            "那...那里...那里不能戳...绝对...",
            "(。´・ω・)ん?",
            "有事恁叫我，别天天一个劲戳戳戳！",
            "欸很烦欸！你戳🔨呢",
            "再戳一下试试？",
            "正在关闭对您的所有服务...关闭成功",
            "啊呜，太舒服刚刚竟然睡着了。什么事？",
            "正在定位您的真实地址...定位成功。轰炸机已起飞"
            "再戳就更大了qwq"
        ]

    async def init(self) -> None:
        """初始化配置文件"""   
        # 如果数据文件路径不存在，则创建目录
        if not os.path.exists(self.config_path):  
            os.makedirs(self.config_path)  
        if os.path.exists(self.address):
            # 如果数据文件路径存在，尝试读取数据文件（config.json）
            try:
                # 如果数据文件路径存在，尝试读取数据文件（config.json）
                with open(self.address, "r", encoding="utf-8") as f:
                    self.g_temp.update(json.load(f))
            except json.decoder.JSONDecodeError:
                # 如果文件为空或包含无效 JSON，则重新初始化配置
                self.g_temp = {}
        else:
            # 如果群数据文件不存在，则初始化g_temp为空字典，并写入对应的文件
            bot = nonebot.get_bot()
            group_list = await bot.get_group_list()
            #从group_list中遍历每个群组
            for group in group_list:
                # 为每个群组创建一个临时字典temp，用于存储群组的配置信息
                snap_temp = {}
                for g_name in self.path:
                    # 将群组的每个配置项设置为默认值True
                    snap_temp[g_name] = True
                    # 特殊情况下（g_name为'red_package'），将该配置项设为False
                    if g_name in ['red_package']:
                        snap_temp[g_name] = False
                # 获取群组ID并转换为字符串类型
                gid = str(group["group_id"])
                # 将临时字典temp作为值，群组ID作为键，添加到g_temp字典中
                self.g_temp[gid] = snap_temp
                # 将更新后的g_temp字典写入群组数据
            self.write_group_data(self.g_temp)

    async def config_check(self) -> None:
        """获取机器人实例"""
        bot = nonebot.get_bot()
        # 获取所有群组的列表
        group_list = await bot.get_group_list()
        # 加载配置文件，得到一个包含配置信息的字典
        with open(self.address, "r", encoding="utf-8") as f:
            config_dict = json.load(f)  
        # 遍历所有群组
        for group in group_list:
            gid = str(group['group_id']) 
            # 如果配置字典中没有该群组的信息，将其添加到配置字典中
            if not config_dict.get(gid):
                config_dict[gid] = {}
                # 遍历配置文件路径中的所有配置项，并初始化为默认值
                for group_name in self.path:
                    config_dict[gid][group_name] = True
                    # 特殊情况下（group_name为'red_package'），将该配置项设为False
                    if group_name in ['red_package']:
                        config_dict[gid][group_name] = False
            else:
                # 如果配置字典中已存在该群组的信息，检查是否有缺失的配置项，并添加默认值
                other_group = config_dict[gid]
                for group_name in self.path:
                    if other_group.get(group_name) is None:
                        other_group[gid][group_name] = True
                        # 特殊情况下（group_name为'red_package'），将该配置项设为False
                        if group_name in ['red_package']:
                            other_group[gid][group_name] = False
        self.g_temp.update(config_dict)
        # 将更新后的配置字典上传到配置文件中
        self.json_upload(self.address, config_dict)

    @staticmethod
    async def check_chuo(g_temp, gid: str) -> bool: 
        """检查戳一戳是否允许"""
        if gid in g_temp and not g_temp[gid]["chuo"]:
            return False
        return g_temp[gid]["chuo"]
    
    @staticmethod
    async def check_honor(g_temp, gid: str) -> bool:
        """检查群荣誉是否允许 """
        if gid in g_temp and not g_temp[gid]["honor"]:
            return False
        return g_temp[gid]["honor"]
    
    @staticmethod
    async def check_file(g_temp, gid: str) -> bool:
        """检查群文件是否允许"""
        if gid in g_temp and not g_temp[gid]["files"]:
            return False
        return g_temp[gid]["files"]
    
    @staticmethod
    async def check_del_user(g_temp, gid: str) -> bool:
        """检查群成员减少是否允许 """
        if gid in g_temp and not g_temp[gid]["del_user"]:
            return False
        return g_temp[gid]["del_user"]
    
    @staticmethod
    async def check_add_user(g_temp, gid: str) -> bool:
        """检查群成员增加是否允许"""
        if gid in g_temp and not g_temp[gid]["add_user"]:
            return False
        return g_temp[gid]["add_user"]
    
    @staticmethod
    async def check_admin(g_temp, gid: str) -> bool:
        """检查管理员是否允许"""
        if gid in g_temp and not g_temp[gid]["admin"]:
            return False
        return g_temp[gid]["admin"]
    
    @staticmethod
    async def check_red_package(g_temp, gid: str) -> bool:
        """检查运气王是否允许"""
        if gid in g_temp and not g_temp[gid]["red_package"]:
            return False
        return g_temp[gid]["red_package"]
    
    @staticmethod
    async def check_txt_to_img(check_txt_img):
        if not utils.check_txt_img:
            return False
        return check_txt_img

    def get_function_name(self, key: str) -> str:
        """根据关键词获取对应功能名称"""
        return self.path[key][0]

    def get_command_type(self, command: str) -> str:
        """根据指令内容获取开关类型"""
        return next(
            (
                key
                for key, keywords in self.path.items()
                if any(keyword in command for keyword in keywords)
            ),
            "",
        )
    
    @staticmethod
    def write_group_data(g_temp) -> None:
        """写入群配置"""
        with open(utils.address, 'w', encoding='utf-8') as f:
            json.dump(g_temp, f, indent=4, ensure_ascii=False)

    @staticmethod
    def json_upload(path, config_dict) -> None:
        """将 JSON 数据上传到指定路径"""
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(config_dict, f, ensure_ascii=False, indent=4)

    @staticmethod
    async def _is_poke(event: Event) -> bool:
        """获取戳一戳状态"""
        return isinstance(event, PokeNotifyEvent) and event.is_tome()
    
    @staticmethod
    async def _is_rongyu(event: Event) -> bool:
        """获取群荣誉变更"""
        return isinstance(event, HonorNotifyEvent)
    
    @staticmethod
    async def _is_checker(event: Event) -> bool:
        """获取文件上传"""
        return isinstance(event, GroupUploadNoticeEvent)
    
    @staticmethod
    async def _is_del_user(event: Event) -> bool:
        """获取群成员减少"""
        return isinstance(event, GroupDecreaseNoticeEvent)
    
    @staticmethod
    async def _is_add_user(event: Event) -> bool:
        """获取群成员增加"""
        return isinstance(event, GroupIncreaseNoticeEvent)
    
    @staticmethod
    async def _is_admin_change(event: Event) -> bool:
        """获取管理员变动"""
        return isinstance(event, GroupAdminNoticeEvent)
    
    @staticmethod
    async def _is_red_packet(event: Event) -> bool:
        """获取红包运气王"""
        return isinstance(event, LuckyKingNotifyEvent)

utils = Utils()