<p align="center">
  <a href="https://v2.nonebot.dev/"><img src="https://avatars.githubusercontent.com/u/53791401?v=4" width="200" height="200" alt="nonebot"></a>
</p>

<div align="center">
# Monitor_Groups

_✨ 基于NoneBot2实现的 监测QQ群事件 插件 ✨_

</div>

## 具体功能：
 - 监测群组的以下变动事件：
     - 群成员增加、减少时，自动发送通知
     - 群管理变更时，自动发送通知
     - 被其他成员戳一戳时，自动回复
     - 群成员上传文件时，自动发送通知
     - 群红包被抢完时，自动发送红包运气王
     - 群成员荣誉变更时，发送变更通知(测试时没反应QwQ)


## 配置说明：

> 1.把下载后的文件夹`nonebot_plugin_monitoring`放在`src/plugins/`目录下

> 2.修改`admin.py`
> > bot_qq：改为机器人的QQ号
> > super_qq：添加或新增管理员的QQ号

> 3.修改`chuoyichuo.py`
> > bot_name：设置机器人的昵称

> 4.修改`rongyu.py`
> > bot_qq：改为机器人的QQ号
> > super_qq：添加或新增管理员的QQ号
