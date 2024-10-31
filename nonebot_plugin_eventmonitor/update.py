"""插件更新"""
import os
import httpx
import nonebot
import platform

from pathlib import Path
from nonebot.log import logger
from nonebot.adapters.onebot.v11 import Bot, Message

from .utils import utils

class Update:
    def __init__(self) -> None:

        self.release_url = "https://api.github.com/repos/Reversedeer/nonebot_plugin_eventmonitor/releases/latest"
        self.config_path = Path() / "data/eventmonitor"
        self.latest_tar_gz = self.config_path / "latest_file.tar.gz"
        self.temp_dir = self.config_path / "temp"
        self.backup_dir = self.config_path / "backup"
        self.version_file = self.config_path / "new_version"
        self.destination_directory = 'src/plugins/nonebot_plugin_eventmonitor'  # 目标文件夹

    async def remind(self, bot: Bot) -> None:
        system = platform.system()
        if system != 'windows':
            restart = self.config_path / "restart.sh"
            if not restart.exists():
                with open(restart, "w", encoding="utf8") as f:
                    f.write(
                        (
                            f"pid=$(netstat -tunlp | grep {str(bot.config.port)}"
                            + " | awk '{print $7}')\n"
                            "pid=${pid%/*}\n"
                            "kill -9 $pid\n"
                            "sleep 3\n"
                            "python3 bot.py"
                        )
                    )
                os.system("chmod +x ./restart.sh")
                logger.info("已自动生成 restart.sh(重启) 文件，请检查脚本是否与本地指令符合...")
            Version = self.version_file
            if Version.exists():
                await bot.send_private_msg(
                user_id=int(list(bot.config.superusers)[0]),
                message="插件更新成功"
                )
                Version.unlink()

    async def get_latest_version_data(self) -> dict:
        for _ in range(3):
            try:
                async with httpx.AsyncClient() as client:
                    res = await client.get(self.release_url)
                    if res.status_code == 200:
                        return res.json()
            except TimeoutError:
                pass
            except Exception as e:
                logger.error("检查最新版本失败")
        return {}
    
    @staticmethod
    async def fetch_data(tar_gz_url):
        async with httpx.AsyncClient() as client:
            return await client.get(tar_gz_url)
        
    @staticmethod
    async def download_file(tar_gz_url, latest_tar_gz):
        async with httpx.AsyncClient() as client:
            response = await client.get(tar_gz_url)
            if response.status_code == 200:
                with open(latest_tar_gz, "wb") as f:
                    f.write(response.content)
                    return True
            else:
                return False

    @staticmethod
    async def auto_check_bot_update() -> None:
        if utils.check_bot_update:
            await Update.auto_check()

    @staticmethod
    async def auto_check() -> None:
        bot = nonebot.get_bot()
        if utils.check_bot_update:
            data = await update.get_latest_version_data()
            latest_version = data["name"]
            if utils.current_version != latest_version:
                if utils.current_version == latest_version:
                    pass
                elif utils.current_version < latest_version:
                    await bot.send_private_msg(user_id=int(list(bot.config.superusers)[0]), message=Message(
                        "✨插件自动检测更新✨\n"
                        "插件名称: nonebot-plugin-eventmonitor\n"
                        f"更新日期：{data['published_at']}\n"
                        f"版本: {utils.current_version} -> {latest_version}\n"
                        "主人可使用'检查event更新'指令自动更新插件"
                        )
                    )
                else:
                    await bot.send_private_msg(user_id=int(list(bot.config.superusers)[0]), message=Message(
                        f"获取到当前版本{utils.current_version} > {latest_version}\n"
                        "请检查是否有报错并核查版本号"
                        )
                    )

update = Update()