from pkg.plugin.context import register, handler, llm_func, BasePlugin, APIHost, EventContext
from pkg.plugin.events import *  # 导入事件类


@register(name="BlankImage", description="为纯图片消息添加默认文本", version="0.1", author="Nothingness-Void")
class BlankImagePlugin(BasePlugin):

    # 插件加载时触发
    def __init__(self, host: APIHost):
        pass

    # 异步初始化
    async def initialize(self):
        pass

    # 检查消息是否只包含图片
    def is_image_only_message(self, text_message, images):
        # 检查是否有图片且没有文本消息
        return len(images) > 0 and (text_message is None or text_message.strip() == '')

    # 当收到个人消息时触发
    @handler(PersonNormalMessageReceived)
    async def person_normal_message_received(self, ctx: EventContext):
        # 获取文本消息和图片
        text_message = ctx.event.text_message
        images = ctx.event.image_list if hasattr(ctx.event, 'image_list') else []
        
        # 检查是否为纯图片消息
        if self.is_image_only_message(text_message, images):
            # 输出调试信息
            self.ap.logger.debug("检测到纯图片消息，添加默认文本")
            
            # 设置默认文本
            ctx.event.text_message = "请根据上下文解读一下这张图片"
            
            # 记录修改
            self.ap.logger.debug(f"已添加默认文本：{ctx.event.text_message}")

    # 当收到群消息时触发
    @handler(GroupNormalMessageReceived)
    async def group_normal_message_received(self, ctx: EventContext):
        # 获取文本消息和图片
        text_message = ctx.event.text_message
        images = ctx.event.image_list if hasattr(ctx.event, 'image_list') else []
        
        # 检查是否为纯图片消息
        if self.is_image_only_message(text_message, images):
            # 输出调试信息
            self.ap.logger.debug("检测到纯图片消息，添加默认文本")
            
            # 设置默认文本
            ctx.event.text_message = "请根据上下文解读一下这张图片"
            
            # 记录修改
            self.ap.logger.debug(f"已添加默认文本：{ctx.event.text_message}")

    # 插件卸载时触发
    def __del__(self):
        pass
