import nonebot

chuo_CD_dir = {}   #戳一戳cd,感觉很鸡肋，自行调整

try:
    chuo_cd = nonebot.get_driver().config.chuo_cd
except Exception:
    chuo_cd = 0    #戳一戳cd默认值
  
config = nonebot.get_driver().config #从 配置文件中获取SUPERUSER, NICKNAME

superusers = {int(uid) for uid in config.superusers}

nickname = next(iter(config.nickname))