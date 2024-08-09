"""消息处理文本"""
import random

from datetime import datetime
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.adapters.onebot.v11.message import Message

from .utils import utils

class Config:
    @staticmethod
    async def admin_changer(sub_type, user_id, bot_qq)  -> str: 
        """发送管理员变动消息"""
        admin_msg = ""
        # 根据管理员变动类型选择不同的消息
        if sub_type == "set":
            # 如果用户ID等于机器人的QQ号，返回特定消息
            admin_msg = (
                "我也是管理啦，你们要小心喵~"
                if user_id == bot_qq
                else f"🚔 管理员变动\n恭喜{user_id}喜提本群管理喵~"
            )
        elif sub_type == "unset":
            # 如果用户ID等于机器人的QQ号，返回特定消息
            admin_msg = (
                "呜呜，别下咱管理呀QwQ，喵呜~"
                if user_id == bot_qq
                else f"🚔 管理员变动\n{user_id}痛失本群管理喵~"
            )
            
        return admin_msg

    @staticmethod
    async def del_user_bye(add_time, user_id):
        """发送退群消息"""
        rely = ""
        del_time = datetime.fromtimestamp(add_time)
        # 检查用户ID是否在超级用户列表superusers中
        if user_id in utils.superusers:
            # 如果是超级用户，生成特定的离开消息
            rely = f"⌈{del_time}⌋\n恭送主人离开喵~"
        else:
            # 如果不是超级用户，生成通用的离开消息，包含用户的QQ号和头像图片
            rely = f"✈️ 成员变动 ✈️ \n时间: ⌈{del_time}⌋\nQQ号为：{user_id}的小可爱退群喵~" \
                + MessageSegment.image(f'https://q4.qlogo.cn/headimg_dl?dst_uin={user_id}&spec=640')
                        
            return rely

    @staticmethod
    async def add_user_wecome(add_time, user_id, bot_qq):
        """发送入群消息"""
        # 将时间戳转换为datetime类型的时间add_time
        add_time = datetime.fromtimestamp(add_time) 
        rely = ""
        # 判断用户ID是否等于机器人的QQ号
        if user_id == bot_qq:
            # 如果是机器人自己加入群组，生成特定的欢迎消息
            rely = "本喵被邀进入贵群喵~\n" \
                        "火速上个管理喵~"
        # 判断用户ID是否在超级用户列表superusers中
        elif user_id in utils.superusers:
            # 如果是超级用户加入群组，生成特定的欢迎消息
            rely = "✨ 成员变动 ✨\n欢迎主人进群喵~"
        else:
            # 如果是普通用户加入群组，生成通用的欢迎消息，包含用户ID、加入时间和用户头像图片的链接
            rely = f"✨ 成员变动 ✨\n欢迎{user_id}的加入喵~\n加入时间：⌈{add_time}⌋，请在群内积极发言喵~" \
                    + MessageSegment.image(f'https://q4.qlogo.cn/headimg_dl?dst_uin={user_id}&spec=640')
        return rely

    @staticmethod
    async def monitor_rongyu(honor_type, user_id, bot_qq) -> str:
        """发送群荣誉变化消息"""
        rely = ""  
        # 根据honor_type选择不同的消息
        if honor_type == "emotion":
            # 如果用户ID等于机器人的QQ号，不作任何操作
            if user_id == bot_qq:
                rely = "你们又不行了，本喵喜提快乐源泉🤣~"
            # 如果用户ID在superusers列表中，返回特定消息
            elif user_id in utils.superusers:
                rely = "恭喜主人荣获快乐源泉🤣标识喵~"
            # 否则，返回通用消息
            else:
                rely = "恭喜你荣获快乐源泉🤣标识喵~"
                
        elif honor_type == "performer":
            # 如果用户ID等于机器人的QQ号，不作任何操作
            if user_id == bot_qq:
                rely = "你们又不行了，本喵喜提群聊之火🔥~"
            # 如果用户ID在superusers列表中，返回特定消息
            elif user_id in utils.superusers:
                rely = "恭喜主人荣获群聊之火🔥标识喵~"
            # 否则，返回通用消息
            else:
                rely = "恭喜你荣获群聊之火🔥标识喵~"

        elif honor_type == "talkative":
            # 如果用户ID等于机器人的QQ号，返回特定消息
            if user_id == bot_qq:
                rely = "你们又不行了，本喵喜提龙王🐲~"
            # 如果用户ID在superusers列表中，返回特定消息
            elif user_id in utils.superusers:
                rely = "恭喜主人荣获龙王🐲标识喵~"
            # 否则，返回通用消息
            else:
                rely: str = "恭喜你荣获龙王🐲标识喵~"

        return rely
    
    @staticmethod
    async def rad_package_change(target_id, bot_qq) -> str:
        """发送运气王变化消息"""
        rely = ""
        if target_id == bot_qq:
            rely = "你们又不行了，本喵喜提运气王🧧"
        elif target_id in utils.superusers:
            rely = "恭喜主人获得本次红包的运气王🧧"
        else:
            rely: str = f"恭喜{target_id}获得本次红包的运气王🧧"

        return rely

    @staticmethod
    async def chuo_send_msg() -> str:
        """发送戳一戳消息"""
        rand_num: int = random.randint(0, len(utils.chuo_msg) - 1)  
        return utils.chuo_msg[rand_num]

    @staticmethod
    async def upload_files(user_id) -> Message:
        """发送上传群文件消息"""
        return (
            MessageSegment.image(
                f'https://q4.qlogo.cn/headimg_dl?dst_uin={user_id}&spec=640'
            )
            + '\n上传了新文件，感谢你一直为群里做贡献喵~'
            + MessageSegment.face(175)
        )
      
config = Config()