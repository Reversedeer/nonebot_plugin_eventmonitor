from nonebug import App
from nonebot.adapters.onebot.v11 import Bot
from nonebot.adapters.onebot.v11.event import (
    GroupIncreaseNoticeEvent,
    GroupDecreaseNoticeEvent,
    NotifyEvent,
    LuckyKingNotifyEvent,
)


# 测试戳一戳事件
async def test_poke_event(app: App) -> None:
    async with app.test_matcher() as ctx:
        bot = ctx.create_bot(base=Bot)

        event = NotifyEvent(
            time=1629876543,
            self_id=123456,
            post_type="notice",
            notice_type="notify",
            sub_type="poke",
            user_id=654321,
            group_id=10000,
        )

        ctx.receive_event(bot, event)

        ctx.should_call_api(
            "send_msg",
            **{
                "message": "检测到戳一戳",
                "user_id": 654321,
                "group_id": 10000,
            },
        )


# 测试新成员入群事件
async def test_member_increase(app: App) -> None:
    async with app.test_matcher() as ctx:
        bot = ctx.create_bot(base=Bot)

        event = GroupIncreaseNoticeEvent(
            time=1629876543,
            self_id=123456,
            post_type="notice",
            notice_type="group_increase",
            sub_type="approve",
            group_id=10000,
            operator_id=123456,
            user_id=987654,
        )

        ctx.receive_event(bot, event)

        ctx.should_call_api(
            "send_msg",
            **{
                "message": "欢迎新成员",
                "group_id": 10000,
            },
        )


# 测试群成员离开事件
async def test_member_decrease(app: App) -> None:
    async with app.test_matcher() as ctx:
        bot = ctx.create_bot(base=Bot)

        event = GroupDecreaseNoticeEvent(
            time=1629876543,
            self_id=123456,
            post_type="notice",
            notice_type="group_decrease",
            sub_type="leave",
            group_id=10000,
            operator_id=987654,
            user_id=987654,
        )

        ctx.receive_event(bot, event)

        ctx.should_call_api(
            "send_msg",
            **{
                "message": "离开了群聊",
                "group_id": 10000,
            },
        )


# 测试运气王事件
async def test_lucky_king(app: App) -> None:
    async with app.test_matcher() as ctx:
        bot = ctx.create_bot(base=Bot)

        event = LuckyKingNotifyEvent(
            time=1629876543,
            self_id=123456,
            post_type="notice",
            notice_type="notify",
            sub_type="lucky_king",
            group_id=10000,
            user_id=123456,
            target_id=654321,
        )

        ctx.receive_event(bot, event)

        ctx.should_call_api(
            "send_msg",
            **{
                "message": "新的运气王",
                "group_id": 10000,
            },
        )
    import nonebot_plugin_eventmonitor

    assert hasattr(nonebot_plugin_eventmonitor, "__plugin_meta__")
    assert nonebot_plugin_eventmonitor.__plugin_meta__.name == "群事件监控"
