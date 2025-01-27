"""事件处理"""

import json
from typing import NoReturn
import asyncio

from httpx import AsyncClient, ConnectError, RequestError, HTTPStatusError
from nonebot import get_bot
from nonebot.log import logger
from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11 import (
    Bot,
    Message,
    MessageSegment,
    PokeNotifyEvent,
    HonorNotifyEvent,
    GroupMessageEvent,
    LuckyKingNotifyEvent,
    GroupAdminNoticeEvent,
    GroupUploadNoticeEvent,
    GroupDecreaseNoticeEvent,
    GroupIncreaseNoticeEvent,
)

from .config import utils, config_data
from .matcher import message
from .txt2img import txt_to_img


class Eventmonitor:
    async def chuo(
        self,
        matcher: Matcher,
        event: PokeNotifyEvent,
    ) -> None:
        """戳一戳"""
        if not (await utils.check_chuo(utils.g_temp, str(event.group_id))):
            await matcher.finish(utils.notAllow)
        # 获取用户id
        uid: str = event.get_user_id()
        try:
            cd = event.time - utils.chuo_CD_dir[uid]
        except KeyError:
            # 没有记录则cd为cd_time+1
            cd: int = config_data.chuo_cd + 1
        if cd > config_data.chuo_cd or event.get_user_id() in config_data.superusers:
            utils.chuo_CD_dir.update({uid: event.time})
            rely_msg: str = await message.chuo_send_msg()
            if not (await utils.check_txt_to_img(config_data.check_txt_img)):
                await matcher.finish(rely_msg)
            else:
                await matcher.send(MessageSegment.image(await txt_to_img.txt_to_img(rely_msg)))

    async def qrongyu(
        self,
        matcher: Matcher,
        event: HonorNotifyEvent,
        bot: Bot,
    ) -> None:
        """群荣誉事件"""
        if not (await utils.check_honor(utils.g_temp, str(event.group_id))):
            return
        bot_qq = int(bot.self_id)
        rely_msg: str = await message.monitor_rongyu(
            event.honor_type,
            event.user_id,
            bot_qq,
        )
        if not (await utils.check_txt_to_img(config_data.check_txt_img)):
            await matcher.finish(rely_msg)
        else:
            await matcher.send(
                MessageSegment.image(await txt_to_img.txt_to_img(rely_msg)),
                at_sender=True,
            )

    async def files(
        self,
        matcher: Matcher,
        event: GroupUploadNoticeEvent,
    ) -> None:
        """群文件事件"""
        if not (await utils.check_file(utils.g_temp, str(event.group_id))):
            return
        rely_msg = await message.upload_files(event.user_id)
        if not (await utils.check_txt_to_img(config_data.check_txt_img)):
            await matcher.finish(rely_msg)
        else:
            await matcher.send(
                MessageSegment.image(await txt_to_img.txt_to_img(str(rely_msg))),
                at_sender=True,
            )

    async def del_user(
        self,
        matcher: Matcher,
        event: GroupDecreaseNoticeEvent,
    ) -> None:
        """退群事件"""
        if not (await utils.check_del_user(utils.g_temp, str(event.group_id))):
            return
        rely_msg = await message.del_user_bye(event.time, event.user_id)
        if not (await utils.check_txt_to_img(config_data.check_txt_img)):
            await matcher.finish(rely_msg)
        else:
            await matcher.send(
                MessageSegment.image(await txt_to_img.txt_to_img(str(rely_msg))),
                at_sender=True,
            )

    async def add_user(
        self,
        matcher: Matcher,
        event: GroupIncreaseNoticeEvent,
        bot: Bot,
    ) -> None:
        """入群事件"""
        await utils.config_check()
        if not (await utils.check_add_user(utils.g_temp, str(event.group_id))):
            return
        bot_qq = int(bot.self_id)
        rely_msg = await message.add_user_wecome(event.time, event.user_id, bot_qq)
        if not (await utils.check_txt_to_img(config_data.check_txt_img)):
            await matcher.finish(rely_msg)
        else:
            await matcher.send(
                MessageSegment.image(await txt_to_img.txt_to_img(str(rely_msg))),
                at_sender=True,
            )

    async def admin_chance(
        self,
        matcher: Matcher,
        event: GroupAdminNoticeEvent,
        bot: Bot,
    ) -> None:
        """管理员变动事件"""
        if not (await utils.check_admin(utils.g_temp, str(event.group_id))):
            return
        bot_qq = int(bot.self_id)
        rely_msg: str = await message.admin_changer(
            event.sub_type,
            event.user_id,
            bot_qq,
        )
        if not (await utils.check_txt_to_img(config_data.check_txt_img)):
            await matcher.finish(rely_msg)
        else:
            await matcher.send(
                MessageSegment.image(await txt_to_img.txt_to_img(rely_msg)),
                at_sender=True,
            )

    async def hongbao(
        self,
        matcher: Matcher,
        event: LuckyKingNotifyEvent,
        bot: Bot,
    ) -> None:
        """红包运气王事件"""
        if not (await utils.check_red_package(utils.g_temp, str(event.group_id))):
            return
        bot_qq = int(bot.self_id)
        rely_msg = await message.rad_package_change(event.target_id, bot_qq)
        if not (await utils.check_txt_to_img(config_data.check_txt_img)):
            await matcher.finish(rely_msg)
        else:
            await matcher.send(
                MessageSegment.image(await txt_to_img.txt_to_img(rely_msg)),
                at_sender=True,
            )

    async def switch(
        self,
        matcher: Matcher,
        event: GroupMessageEvent,
    ) -> None:
        """获取开关指令的参数，即用户输入的指令内容"""
        command = str(event.get_message()).strip()
        # 获取群组ID
        gid = str(event.group_id)
        # 判断指令是否包含"开启"或"关闭"关键字
        if '开启' in command or '开始' in command:
            if key := utils.get_command_type(command):
                utils.g_temp[gid][key] = True
                await utils.write_group_data(utils.g_temp)
                name = utils.get_function_name(key)
                if not (await utils.check_txt_to_img(config_data.check_txt_img)):
                    await matcher.finish(f'{name}功能已开启喵')
                else:
                    await matcher.send(MessageSegment.image(await txt_to_img.txt_to_img(f'{name}功能已开启喵')))
        elif ('禁止' in command or '关闭' in command) and (key := utils.get_command_type(command)):
            utils.g_temp[gid][key] = False
            await utils.write_group_data(utils.g_temp)
            name = utils.get_function_name(key)
            if not (await utils.check_txt_to_img(config_data.check_txt_img)):
                await matcher.finish(f'{name}功能已关闭喵')
            else:
                await matcher.send(MessageSegment.image(await txt_to_img.txt_to_img(f'{name}功能已关闭喵')))

    async def usage(self, matcher: Matcher) -> NoReturn:
        """获取指令帮助"""
        await matcher.finish(utils.usage)

    async def state(self, matcher: Matcher, event: GroupMessageEvent) -> None:
        """指令开关"""
        gid = str(event.group_id)
        with utils.data_address.open('r', encoding='utf-8') as f:
            group_status = json.load(f)
        if gid not in group_status:
            await utils.config_check()
            with utils.data_address.open('r', encoding='utf-8') as f:
                group_status = json.load(f)
        rely_msg = f'群{gid}的Event配置状态：\n' + '\n'.join(
            [f'{utils.path[func][0]}: {"开启" if group_status[gid][func] else "关闭"}' for func in utils.path]
        )
        if not (await utils.check_txt_to_img(config_data.check_txt_img)):
            await matcher.finish(rely_msg)
        else:
            await matcher.send(MessageSegment.image(await txt_to_img.txt_to_img(rely_msg)))

    async def check_plugin(self, matcher: Matcher) -> None:
        """检测插件更新"""
        try:
            if await self.check_plugin_update():
                await matcher.finish('插件已是最新版本')
        except (HTTPStatusError, ConnectError, RequestError, TimeoutError, json.JSONDecodeError) as e:
            logger.exception('检查更新时发生未处理的异常')
            await matcher.finish(f'检查更新失败: {str(e)}')

    @staticmethod
    async def get_latest_version_data() -> dict:
        """获取最新版本数据"""
        testtime = 2
        async with AsyncClient(timeout=10) as client:
            for attempt in range(3):
                try:
                    response = await client.get(utils.release_url)
                    return response.json()
                except HTTPStatusError as e:
                    logger.warning(f'HTTP 错误 [尝试 {attempt + 1}/3]: {e.response.status_code}')
                    if attempt == testtime:
                        raise
                except (ConnectError, TimeoutError, RequestError) as e:
                    logger.warning(f'网络错误 [尝试 {attempt + 1}/3]: {str(e)}')
                    if attempt == testtime:
                        raise
                except json.JSONDecodeError as e:
                    logger.error(f'JSON 解析失败: {e.doc}')
                    raise
                await asyncio.sleep(2**attempt)
        return {}

    async def check_plugin_update(self) -> bool:
        """检查更新核心逻辑"""
        if not config_data.check_bot_update:
            return False
        try:
            data: dict = await self.get_latest_version_data()
            if not data or 'name' not in data:
                logger.error('获取版本数据无效')
                return False
        except (HTTPStatusError, ConnectError, RequestError, TimeoutError, json.JSONDecodeError) as e:
            logger.error(f'获取版本数据失败: {str(e)}')
            return False
        current = utils.current_version
        latest = data['name']
        if current != latest:
            if current == latest:
                pass
            elif current < latest:
                message_template = (
                    '✨插件自动检测更新✨\n'
                    '插件名称: nonebot-plugin-eventmonitor\n'
                    f'更新日期：{data["published_at"]}\n'
                    f'版本: {utils.current_version} -> {data["name"]}\n'
                    "主人可使用'检查event更新'指令自动更新插件"
                )
                message = message_template
            else:
                message = f'获取到当前版本{utils.current_version} > {data["name"]}\n请检查是否有报错并核查版本号'
            bot = get_bot()
            await bot.send_private_msg(user_id=int(list(bot.config.superusers)[0]), message=Message(message))
        return True


eventmonitor = Eventmonitor()
