<p align="center">
  <a href="https://v2.nonebot.dev/"><img src="https://v2.nonebot.dev/logo.png" width="200" height="200" alt="nonebot"></a>
</p>


<div align="center">
# Monitor_Groups

_✨ 基于NoneBot2实现的 监测QQ群事件 插件 ✨_

</div>

## 介绍：点点Star✨
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

## 安装方式

### nb-cli安装(推荐)

```
nb plugin install nonebot_plugin_eventmonitor
```

<details><summary><h3>pip</h3></summary>

    pip install nonebot-plugin-eventmonitor
在’pyproject.toml‘文件中写入


    "nonebot_plugin_eventmonitor"

</details>

<details><summary><h3>git clone</h3></summary>

```
git clone https://github.com/Reversedeer/nonebot_piugin_eventmonitor.git
```

</details>

### 更新

```
pip install --upgrade nonebot-plugin-eventmonitor
```

## 配置

| config  | type | default |   example    |       usage        |
| :-----: | :--: | :-----: | :----------: | :----------------: |
| chuo_cd | int  |    0    | chuo_cd = 10 | 戳一戳的cd（选填） |

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
    """
```

<details>
    <summary><h2>更新日志</h2></summary>

- v0.1.8

  - 🚨增加功能开关指令：event状态/event配置 
  - 🐛修复群文件不能检测bug(少写一个字母qwq)
  - 优化目录结构
  
- v0.1.7
  - 🚨新增所有功能开关[#issue5](https://github.com/Reversedeer/nonebot_plugin_eventmonitor/issues/9)

  - 🚨新增权限控制
  - 🐛修复潜在的bug
- v0.1.6
  - 🐛修复bug
- v0.1.5
  - 🐛修复获取superusers数值bug
  - 优化配置文件 [#issue4](https://github.com/Reversedeer/nonebot_plugin_eventmonitor/issues/6)
  - 删除冗余代码
- v0.1.3
  - 🐛修复配置文件bug
- v0.1.2
  - 🚨增加戳一戳的文案

  - 🐛修复bug
- v0.1.1

  - 🐛修复bug
- v0.1.0
  - 🚨新增戳一戳加了cd（本人觉得功能鸡肋）
  - 🐛修复管理员变动时API报错问题[#issue1](https://github.com/Reversedeer/nonebot_plugin_eventmonitor/issues/1)
  - 抛弃原有的配置模式
- v0.0.6
  - 🐛修复了大量的bug
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

感谢[@cjladmin](https://github.com/cjladmin)的开源代码，在此基础上修改了bug

以后将持续更新并完善

## 其他插件

[舔狗日记](https://github.com/Reversedeer/nonebot_plugin_dog)

[使用API的chatGPTQQ聊天机器人](https://github.com/Reversedeer/nonebot_plugin_chatGPT_openai)

