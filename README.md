<p align="center">
  <a href="https://nonebot.dev">
    <img src="https://nonebot.dev/logo.png" width="180" height="180" alt="NoneBot">
  </a>
</p>

<div align="center">
# nonebot_plugin_eventmonitor

✨ 基于 NoneBot2 实现的 监测 QQ 群事件，群荣誉事件的插件 ✨

</div>

<p align="center">
  <a href="https://raw.githubusercontent.com/Reversedeer/nonebot_plugin_eventmonitor/main/LICENSE">
    <img src="https://img.shields.io/github/license/Reversedeer/nonebot_plugin_eventmonitor" alt="license">
  </a>
  <a href="https://camo.githubusercontent.com/c5bfbde247cd10e93ff50a518b0f5e441a6e9959495f6bf0f1a1913d2b1b7a8d/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f707974686f6e2d332e382b2d626c75652e737667">
    <img src="https://img.shields.io/badge/python-3.8+-green.svg" alt="python">
  </a>
  <a href="https://github.com/howmanybots/onebot/blob/master/README.md">
    <img src="https://img.shields.io/badge/NoneBot2-blue?style=flat&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABABAMAAABYR2ztAAAAIVBMVEUAAAAAAAADAwMHBwceHh4UFBQNDQ0ZGRkoKCgvLy8iIiLWSdWYAAAAAXRSTlMAQObYZgAAAQVJREFUSMftlM0RgjAQhV+0ATYK6i1Xb+iMd0qgBEqgBEuwBOxU2QDKsjvojQPvkJ/ZL5sXkgWrFirK4MibYUdE3OR2nEpuKz1/q8CdNxNQgthZCXYVLjyoDQftaKuniHHWRnPh2GCUetR2/9HsMAXyUT4/3UHwtQT2AggSCGKeSAsFnxBIOuAggdh3AKTL7pDuCyABcMb0aQP7aM4AnAbc/wHwA5D2wDHTTe56gIIOUA/4YYV2e1sg713PXdZJAuncdZMAGkAukU9OAn40O849+0ornPwT93rphWF0mgAbauUrEOthlX8Zu7P5A6kZyKCJy75hhw1Mgr9RAUvX7A3csGqZegEdniCx30c3agAAAABJRU5ErkJggg==" alt="cqhttp">
  </a>
</p>

## 介绍：求 Star✨

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

> [!WARNING]
>
> 从v0.3.x开始，自动更新必须满足以下要求：
>
> 1.使用前请确保插件位置移动至: /xxx/awesome-bot/src/plugins/
>
> 2.请确保所有依赖正常加载
>
> 3.使用nb-cli或nb plugin install 方式安装插件的，pyproject.toml修改参考：
>
> ```
> plugins = ["nonebot_plugin_apscheduler"]
> plugin_dirs = ["src/plugins"]
> ```

## 安装方式

### nb-cli

```
nb plugin install nonebot_plugin_eventmonitor
```

<details>
    <summary><h3>pip</h3></summary>

    pip install nonebot-plugin-eventmonitor

在’pyproject.toml‘文件中写入

    "nonebot_plugin_eventmonitor"

</details>

### 更新：

```
pip install --upgrade nonebot-plugin-eventmonitor
```

## 配置

|   config   |   type   | default  |        example        |                                                 usage                                                 |
| :--------: | :------: | :------: | :-------------------: | :---------------------------------------------------------------------------------------------------: |
|  chuo_cd   |   int    |    10    |     chuo_cd = 10      |                                              戳一戳的 cd                                              |
| SUPERUSERS | set[str] |  set()   | SUPERUSERS=["114514"] |  机器人超级用户，可以使用权限 [`SUPERUSER`](https://nonebot.dev/docs/2.0.0/api/permission#SUPERUSER)  |
|  NICKNAME  | set[str] | set(Bot) |   NICKNAME=["IKun"]   | 机器人昵称，通常协议适配器会根据用户是否 @user 或者是否以机器人昵称开头来判断是否是向机器人发送的消息 |
|  isalive   |   bool   |   True   |    isalive = True     |                                         是否启用插件自动更新                                          |

## 指令帮助

```
User: (戳一戳-> bot)
Bot: "请不要戳AI-Md >_<"

SUPERUSER/GROUP_ADMIN/GROUP_OWNER: "/检查检查eventr更新"
Bot: "
    ✨插件自动检测更新✨
    插件名称:nonebot-plugin-eventmonitor
    更新日期：xxxx.xx.xx
    版本: 0.2.x -> 0.3.x
	"

SUPERUSER/GROUP_ADMIN/GROUP_OWNER: "/开启 群荣誉检测"
Bot: "群荣誉检测功能已开启喵"

SUPERUSER/GROUP_ADMIN/GROUP_OWNER: "/event配置"
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
    指令8：检查event更新
    指令9：重启
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
- [ ] 文字转图片发送

<details>
    <summary><h2>更新日志</h2></summary>

- v0.3.1

  - ♻ 重构项目
  - 🚨 新增插件自动更新
  - 🐛 修复红包运气王无法检测 bug
  - 🐛 修复自动更新时意外保存

- v0.2.1

  - ✨适配插件元数据

  - 🐛 修复 bug

- v0.2.0

  - 🐛 修复 bot 加群 bug[issue6](https://github.com/Reversedeer/nonebot_plugin_eventmonitor/issues/18)

  - ✅优化提示

- v0.1.9
  - 🚨 新增功能开关指令：event 状态/event 配置
  - 🐛 修复群文件不能检测 bug(少写一个字母 qwq)
  - ✅优化目录结构
- v0.1.7

  - 🚨 新增所有功能开关[#issue5](https://github.com/Reversedeer/nonebot_plugin_eventmonitor/issues/9)

  - 🚨 新增权限控制
  - 🐛 修复潜在的 bug

- v0.1.6
  - 🐛 修复 bug
- v0.1.5
  - 🐛 修复获取 superusers 数值 bug
  - ✅优化配置文件 [#issue4](https://github.com/Reversedeer/nonebot_plugin_eventmonitor/issues/6)
  - ✅删除冗余代码
- v0.1.3
  - 🐛 修复配置文件 bug
- v0.1.2

  - 🚨 增加戳一戳的文案

  - 🐛 修复 bug

- v0.1.1

  - 🐛 修复 bug

- v0.1.0
  - 🚨 新增戳一戳加了 cd（本人觉得功能鸡肋）
  - 🐛 修复管理员变动时 API 报错问题[#issue1](https://github.com/Reversedeer/nonebot_plugin_eventmonitor/issues/1)
  - ✅抛弃原有的配置模式
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

