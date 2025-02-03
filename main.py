from pkg.plugin.context import register, handler, llm_func, BasePlugin, APIHost, EventContext
from pkg.plugin.events import *  # 导入事件类


# 注册插件
@register(name="BlankImageHandler", description="处理只发送图片的情况，自动添加解读提示", version="0.1", author="Nothingness-Void")
class BlankImagePlugin(BasePlugin):

    # 插件加载时触发
    def __init__(self, host: APIHost):
        self.default_prompt = "解读一下这张图片"  # 可以在这里设置默认的提示语

    # 异步初始化
    async def initialize(self):
        pass

    # 当收到个人消息时触发
    @handler(PersonNormalMessageReceived)
    async def person_normal_message_received(self, ctx: EventContext):
        # 检查消息是否只包含图片
        if (not ctx.event.text_message or ctx.event.text_message.strip() == "") and ctx.event.image_list:
            # 添加默认的解读提示
            ctx.event.text_message = self.default_prompt
            self.ap.logger.debug(f"为用户 {ctx.event.sender_id} 的图片添加解读提示")

    # 当收到群消息时触发
    @handler(GroupNormalMessageReceived)
    async def group_normal_message_received(self, ctx: EventContext):
        # 检查消息是否只包含图片
        if (not ctx.event.text_message or ctx.event.text_message.strip() == "") and ctx.event.image_list:
            # 添加默认的解读提示
            ctx.event.text_message = self.default_prompt
            self.ap.logger.debug(f"为群 {ctx.event.group_id} 中用户 {ctx.event.sender_id} 的图片添加解读提示")

    # 插件卸载时触发
    def __del__(self):
        pass
