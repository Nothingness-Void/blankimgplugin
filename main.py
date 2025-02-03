from pkg.plugin.context import register, handler, llm_func, BasePlugin, APIHost, EventContext
from pkg.plugin.events import *  # 导入事件类


# 注册插件
@register(name="BlankImageHandler", description="处理只发送图片的情况，自动添加解读提示", version="0.3", author="Nothingness-Void")
class BlankImagePlugin(BasePlugin):

    # 插件加载时触发
    def __init__(self, host: APIHost):
        self.default_prompt = "解读一下这张图片"  # 可以在这里设置默认的提示语
        self.host = host

    # 异步初始化
    async def initialize(self):
        pass

    async def _handle_image_message(self, ctx: EventContext, is_group=False):
        """统一处理图片消息的方法"""
        if ctx.event.image_list and (not ctx.event.text_message or ctx.event.text_message.strip() == ""):
            try:
                # 创建新的消息内容
                ctx.event.message_chain = [
                    {
                        "type": "text",
                        "content": self.default_prompt
                    }
                ]
                # 确保图片信息被保留
                for img in ctx.event.image_list:
                    ctx.event.message_chain.append({
                        "type": "image",
                        "content": img
                    })
                
                # 更新文本消息
                ctx.event.text_message = self.default_prompt
                
                # 记录日志
                source = f"群 {ctx.event.group_id} 中的用户 {ctx.event.sender_id}" if is_group else f"用户 {ctx.event.sender_id}"
                self.host.logger.info(f"为{source}的图片添加解读提示: {self.default_prompt}")
                
            except Exception as e:
                self.host.logger.error(f"处理图片消息时出错: {str(e)}")
                return

    # 当收到个人消息时触发
    @handler(PersonNormalMessageReceived)
    async def person_normal_message_received(self, ctx: EventContext):
        await self._handle_image_message(ctx, is_group=False)

    # 当收到群消息时触发
    @handler(GroupNormalMessageReceived)
    async def group_normal_message_received(self, ctx: EventContext):
        await self._handle_image_message(ctx, is_group=True)

    # 插件卸载时触发
    def __del__(self):
        pass
