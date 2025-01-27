"""依赖文件"""

import json
from pathlib import Path

import nonebot
from nonebot import get_plugin_config
from pydantic import BaseModel
import nonebot_plugin_localstore as store
from nonebot.adapters.onebot.v11 import (
    Event,
    PokeNotifyEvent,
    HonorNotifyEvent,
    LuckyKingNotifyEvent,
    GroupAdminNoticeEvent,
    GroupUploadNoticeEvent,
    GroupDecreaseNoticeEvent,
    GroupIncreaseNoticeEvent,
)


class Config(BaseModel):
    """配置文件"""

    chuo_cd: int = 10
    check_bot_update: bool = True
    check_txt_img: bool = False
    nickname: list[str] = []
    superusers: list[int] = []


config_data: Config = get_plugin_config(Config)


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
            指令8：检查event更新|checkeventupdate
            指令9：event配置|eventstatus
            指令10：开启|关闭文案
            指令11：event指令帮助|eventhelp"""
        self.path = {
            'chuo': ['戳一戳'],
            'honor': ['群荣誉检测'],
            'files': ['群文件检测'],
            'del_user': ['群成员减少检测'],
            'add_user': ['群成员增加检测'],
            'admin': ['管理员变动检测'],
            'red_package': ['运气王检测'],
        }
        self.notAllow = '功能未开启'
        self.g_temp = {}
        self.chuo_CD_dir = {}
        self.current_version = '0.4.0'
        self.config_path: Path = store.get_plugin_config_dir()
        self.data_address: Path = self.config_path / 'config.json'
        self.release_url = 'https://api.github.com/repos/Reversedeer/nonebot_plugin_eventmonitor/releases/latest'

    async def init(self) -> None:
        """初始化主入口"""
        await self.ensure_config_path()
        await self.init_or_update_config()

    async def ensure_config_path(self) -> None:
        """确保配置文件路径存在"""
        if not self.config_path.exists():
            self.config_path.mkdir(parents=True)

    async def init_or_update_config(self) -> None:
        """初始化或更新配置文件"""
        if self.data_address.exists():
            await self.load_and_validate_config()
        else:
            await self.create_new_config()

    async def load_and_validate_config(self) -> None:
        """加载并验证现有配置"""
        try:
            with self.data_address.open('r', encoding='utf-8') as f:
                loaded_config = json.load(f)
            self.g_temp.update(loaded_config)
        except (json.decoder.JSONDecodeError, FileNotFoundError):
            await self.create_new_config()

    async def create_new_config(self) -> None:
        """创建全新配置文件"""
        self.g_temp: dict = await self.generate_default_config()
        await self.write_group_data(self.g_temp)

    async def generate_default_config(self) -> dict:
        """生成默认配置模板"""
        bot = nonebot.get_bot()
        group_list = await bot.get_group_list()
        default_config = {}

        for group in group_list:
            gid = str(group['group_id'])
            default_config[gid] = self.create_group_template()

        return default_config

    def create_group_template(self) -> dict:
        """创建单个群组的配置模板"""
        template = {}
        for g_name in self.path:
            template[g_name] = True
            if g_name in ['red_package']:
                template[g_name] = False
        return template

    async def config_check(self) -> None:
        """配置完整性检查"""
        current_config = await self.load_current_config()
        updated_config = await self.update_missing_config(current_config)
        await self.json_upload(updated_config)

    async def load_current_config(self) -> dict:
        """加载当前配置"""
        try:
            with self.data_address.open('r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            return {}

    async def update_missing_config(self, config: dict) -> dict:
        """更新缺失的配置项"""
        bot = nonebot.get_bot()
        group_list = await bot.get_group_list()

        for group in group_list:
            gid = str(group['group_id'])
            if gid not in config:
                config[gid] = self.create_group_template()
                continue
            current_group = config[gid]
            template = self.create_group_template()
            # 同步新增配置项
            for key in template:
                if key not in current_group:
                    current_group[key] = template[key]
            # 移除废弃配置项
            for key in list(current_group.keys()):
                if key not in template:
                    del current_group[key]
        return config

    @staticmethod
    async def check_chuo(g_temp: dict, gid: str) -> bool:
        """检查戳一戳是否允许"""
        if gid in g_temp and not g_temp[gid]['chuo']:
            return False
        return g_temp[gid]['chuo']

    @staticmethod
    async def check_honor(g_temp: dict, gid: str) -> bool:
        """检查群荣誉是否允许"""
        if gid in g_temp and not g_temp[gid]['honor']:
            return False
        return g_temp[gid]['honor']

    @staticmethod
    async def check_file(g_temp: dict, gid: str) -> bool:
        """检查群文件是否允许"""
        if gid in g_temp and not g_temp[gid]['files']:
            return False
        return g_temp[gid]['files']

    @staticmethod
    async def check_del_user(g_temp: dict, gid: str) -> bool:
        """检查群成员减少是否允许"""
        if gid in g_temp and not g_temp[gid]['del_user']:
            return False
        return g_temp[gid]['del_user']

    @staticmethod
    async def check_add_user(g_temp: dict, gid: str) -> bool:
        """检查群成员增加是否允许"""
        if gid in g_temp and not g_temp[gid]['add_user']:
            return False
        return g_temp[gid]['add_user']

    @staticmethod
    async def check_admin(g_temp: dict, gid: str) -> bool:
        """检查管理员是否允许"""
        if gid in g_temp and not g_temp[gid]['admin']:
            return False
        return g_temp[gid]['admin']

    @staticmethod
    async def check_red_package(g_temp: dict, gid: str) -> bool:
        """检查运气王是否允许"""
        if gid in g_temp and not g_temp[gid]['red_package']:
            return False
        return g_temp[gid]['red_package']

    @staticmethod
    async def check_txt_to_img(enable_check: bool) -> bool:  # noqa: FBT001
        """检查文本转图片是否允许"""
        if not config_data.check_txt_img:
            return False
        return enable_check

    def get_function_name(self, key: str) -> str:
        """根据关键词获取对应功能名称"""
        return self.path[key][0]

    def get_command_type(self, command: str) -> str:
        """根据指令内容获取开关类型"""
        return next(
            (key for key, keywords in self.path.items() if any(keyword in command for keyword in keywords)),
            '',
        )

    async def write_group_data(self, g_temp: dict) -> None:
        """写入群配置"""
        with self.data_address.open('w', encoding='utf-8') as f:
            json.dump(g_temp, f, ensure_ascii=False, indent=4)

    async def json_upload(self, updated_config: dict) -> None:
        """将 JSON 数据上传到指定路径"""
        with self.data_address.open('w', encoding='utf-8') as f:
            json.dump(updated_config, f, ensure_ascii=False, indent=4)

    @staticmethod
    async def poke(event: Event) -> bool:
        """获取戳一戳状态"""
        return isinstance(event, PokeNotifyEvent) and event.is_tome()

    @staticmethod
    async def rongyu(event: Event) -> bool:
        """获取群荣誉变更"""
        return isinstance(event, HonorNotifyEvent)

    @staticmethod
    async def checker(event: Event) -> bool:
        """获取文件上传"""
        return isinstance(event, GroupUploadNoticeEvent)

    @staticmethod
    async def del_user(event: Event) -> bool:
        """获取群成员减少"""
        return isinstance(event, GroupDecreaseNoticeEvent)

    @staticmethod
    async def add_user(event: Event) -> bool:
        """获取群成员增加"""
        return isinstance(event, GroupIncreaseNoticeEvent)

    @staticmethod
    async def admin_change(event: Event) -> bool:
        """获取管理员变动"""
        return isinstance(event, GroupAdminNoticeEvent)

    @staticmethod
    async def red_packet(event: Event) -> bool:
        """获取红包运气王"""
        return isinstance(event, LuckyKingNotifyEvent)


utils = Utils()
