<p align="center">
  <a href="https://nonebot.dev/"><img src="https://nonebot.dev/logo.png" width="200" height="200" alt="nonebot"></a>
</p>

<div align="center">

# nonebot-plugin-eventmonitor

_✨ 基于 NoneBot2 实现的 监测 QQ 群事件，群荣誉事件的插件 ✨_

</div>

<p align="center">
  <a href="https://raw.githubusercontent.com/Reversedeer/nonebot_plugin_eventmonitor/main/LICENSE">
  	<img src="https://img.shields.io/github/license/Reversedeer/nonebot_plugin_eventmonitor" alt="license">
  </a>
  <a href="https://pypi.org/project/nonebot-plugin-eventmonitor">
	<img src="https://img.shields.io/pypi/v/nonebot-plugin-eventmonitor?logo=python&logoColor=edb641" alt="pypi">
  </a>
  	<img src="https://img.shields.io/badge/python-3.9+-blue?logo=python&logoColor=edb641" alt="python">
  <a href="https://nonebot.dev/">
    <img src="https://img.shields.io/badge/NoneBot2-blue?style=flat&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABABAMAAABYR2ztAAAAIVBMVEUAAAAAAAADAwMHBwceHh4UFBQNDQ0ZGRkoKCgvLy8iIiLWSdWYAAAAAXRSTlMAQObYZgAAAQVJREFUSMftlM0RgjAQhV+0ATYK6i1Xb+iMd0qgBEqgBEuwBOxU2QDKsjvojQPvkJ/ZL5sXkgWrFirK4MibYUdE3OR2nEpuKz1/q8CdNxNQgthZCXYVLjyoDQftaKuniHHWRnPh2GCUetR2/9HsMAXyUT4/3UHwtQT2AggSCGKeSAsFnxBIOuAggdh3AKTL7pDuCyABcMb0aQP7aM4AnAbc/wHwA5D2wDHTTe56gIIOUA/4YYV2e1sg713PXdZJAuncdZMAGkAukU9OAn40O849+0ornPwT93rphWF0mgAbauUrEOthlX8Zu7P5A6kZyKCJy75hhw1Mgr9RAUvX7A3csGqZegEdniCx30c3agAAAABJRU5ErkJggg==" alt="Nonebot2">
  </a>
</p>

## 介绍:

> 监测群组的以下变动事件：
>
> 群成员增加、减少时，自动发送通知
>
> 群管理变更时，自动发送通知
>
> 被其他成员戳一戳时，自动回复
>
> 群成员上传文件时，自动发送通知
>
> 群红包被抢完时，自动发送红包运气王
>
> 群成员荣誉变更时，发送变更通知

> [!CAUTION]
>
> ~~从 v0.3.x 开始，自动更新必须满足以下要求：~~
>
> ~~1.使用前请确保插件位置移动至: /xxx/awesome-bot/src/plugins/~~
>
> 弃用了使用指令更新插件的功能（目前仅可手动检查更新)

> [!TIP]
>
> 本插件从 v0.4.0 开始使用 localstore 管理插件数据，若需要使用旧配置，请使用~~迁移脚本~~迁移 config.json
>
> 若想全新开始，插件已初始化并配置好默认值，请使用指令按需修改

> [!IMPORTANT]
>
> **手动迁移方法：**
>
> 原数据目录：/xxx/awesome-bot/data/eventmonitor/config.json
>
> 目标位置请移步[数据存储](https://nonebot.dev/docs/next/best-practice/data-storing)

## 安装方式

### nb-cli

```python
nb plugin install nonebot-plugin-eventmonitor
```

<details>
    <summary><h2>pip</h2></summary>

```python
pip install nonebot-plugin-eventmonitor
```

#### 在’pyproject.toml‘文件中写入

    plugins = ["nonebot_plugin_nonebot_plugin_eventmonitor"]

### 更新：

```python
pip install --upgrade nonebot-plugin-eventmonitor
```

</details>

## 配置(必填)

|          config           |   type   | default  |             example              |                                                usag                                                 |
| :-----------------------: | :------: | :------: | :------------------------------: | :-------------------------------------------------------------------------------------------------: |
|        SUPERUSERS         | set[str] |  set()   |      SUPERUSERS=["114514"]       | 机器人超级用户，可以使用权限 [`SUPERUSER`](https://nonebot.dev/docs/2.0.0/api/permission#SUPERUSER) |
|         NICKNAME          | set[str] | set(Bot) |        NICKNAME=["IKun"]         |                                             机器人昵称                                              |
| event_check_plugin_update |   bool   |   True   | event_check_plugin_update = True |                                        是否启用插件检测更新                                         |
|    event_check_txt_img    |   bool   |  False   |    event_check_txt_img= false    |                                         是否启用文字转图片                                          |
|       event_chuo_cd       |   int    |    10    |        event_chuo_cd= 10         |                                             戳一戳的 cd                                             |

## 指令帮助

```
User: (戳一戳-> bot)
Bot: "请不要戳AI-Md >_<"

SUPERUSER: "/检查event更新"
Bot: "
    ✨插件自动检测更新✨
    插件名称:nonebot-plugin-eventmonitor
    更新日期：xxxx.xx.xx
    版本: 0.3.x -> 0.4.x
	"

SUPERUSER/GROUP_ADMIN/GROUP_OWNER: "/开启 群荣誉检测"
Bot: "群荣誉检测功能已开启喵"

SUPERUSER/GROUP_ADMIN/GROUP_OWNER: "/eventstatus"
Bot: "
	群114514的Event配置状态：
	戳一戳: 开启
	群荣誉检测: 开启
	群文件检测: 开启
	群成员减少检测: 开启
	群成员增加检测: 开启
	管理员变动检测: 开启
	运气王检测: 关闭
	"

SUPERUSER/GROUP_ADMIN/GROUP_OWNER: "/eventhelp"
Bot: "
	指令1：戳一戳(戳一戳bot获取文案)
	指令2：群荣誉监测(检测群聊中龙王，群聊之火，快乐源泉的获得并发送提示，当 bot获得群荣誉时有特殊消息)
	... ...
	"
```

## 指令结构帮助：

```
usage = """
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
    指令11：event指令帮助|eventhelp
    """


json结构(默认值):
{
	"114514": {
        "chuo": true,
        "honor": true,
        "files": true,
        "del_user": true,
        "add_user": true,
        "admin": true,
        "red_package": false
    }
}
```

## TODO

- [x] 更多的事件检测功能
- [x] 事件检测功能开关
- [x] 定时任务
- [x] 文字转图片发送
- [ ] 插件自动更新

<details>
    <summary><h2>更新日志</h2></summary>

- v0.4.8

  - ✨ 使用UTC-8显示时间
- v0.4.6

  - 🐛 修复依赖顺序加载错误

- v0.4.5
  - 🐛 修复依赖缺失的错误
- v0.4.3

  - ✨ 优化入退群消息

  - ✨ 优化了烦人的每天插件更新播报（仅在每次启动 bot 时自动发送）
- v0.4.2

  - 🐛 修复 nickname 未格式化
- v0.4.1

  - 🐛 修复配置文件读取错误
  - 🐛 修复版本号读取错误

  - 🐛 修复配置文件读取错误
  - 🐛 修复版本号读取错误
- v0.4.0

  - ✨ 使用 Localstore 管理插件数据

  - ✨ 重构代码，增加可读性便于维护

  - 💥 弃用插件指令自动更新（仅可手动更新）
- v0.3.2
  - ✨ 新增插件定时任务
  - ✨ 新增消息文字转图片
- v0.3.1

  - ♻ 重构项目
  - ✨ 新增插件自动更新
  - 🐛 修复红包运气王无法检测 bug
  - 🐛 修复自动更新时意外报错 bug
- v0.2.1

  - ✨ 适配插件元数据
  - 🐛 修复 bug
- v0.2.0

  - 🐛 修复 bot 加群 bug[issue6](https://github.com/Reversedeer/nonebot_plugin_eventmonitor/issues/18)
  - ♻️ 优化提示
- v0.1.9
  - ✨ 新增功能开关指令：event 状态/event 配置
  - 🐛 修复群文件不能检测 bug(少写一个字母 qwq)
  - ♻️ 优化目录结构
- v0.1.7

  - ✨ 新增所有功能开关[#issue5](https://github.com/Reversedeer/nonebot_plugin_eventmonitor/issues/9)
  - ✨ 新增权限控制
  - 🐛 修复潜在的 bug
- v0.1.6

  - 🐛 修复 bug
- v0.1.5

  - 🐛 修复获取 superusers 数值 bug
  - ♻️ 优化配置文件 [#issue4](https://github.com/Reversedeer/nonebot_plugin_eventmonitor/issues/6)
  - 💥 删除冗余代码
- v0.1.3

  - 🐛 修复配置文件 bug
- v0.1.2

  - ✨ 增加戳一戳的文案
  - 🐛 修复 bug
- v0.1.1

  - 🐛 修复 bug
- v0.1.0

  - ✨ 新增戳一戳加了 cd（本人觉得功能鸡肋）
  - 🐛 修复管理员变动时 API 报错问题[#issue1](https://github.com/Reversedeer/nonebot_plugin_eventmonitor/issues/1)
  - ♻️ 优化原有的配置模式
- v0.0.6

  - 🐛 修复了大量的 bug
  </details>

## 关于 ISSUE

以下 ISSUE 会被直接关闭

- 提交 BUG 不使用 Template
- 询问已知问题
- 提问找不到重点
- 重复提问

> 请注意, 开发者并没有义务回复您的问题. 您应该具备基本的提问技巧。  
> 有关如何提问，请阅读[《提问的智慧》](https://github.com/ryanhanwu/How-To-Ask-Questions-The-Smart-Way/blob/main/README-zh_CN.md)

## 感谢：

感谢[@cjladmin](https://github.com/cjladmin)的开源代码，在此基础上修改了 bug

以后将持续更新并完善

## 其他插件

[nonebot-plugin-dog(获取舔狗文案，汪！)](https://github.com/Reversedeer/nonebot_plugin_dog)

[nonebot-plugin-hyp(查询 hypixel 玩家数据)](https://github.com/Reversedeer/nonebot_plugin_hyp)
