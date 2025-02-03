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

    # 检查消息链是否只包含图片
    def is_image_only_message(self, message_chain):
        has_image = False
        has_text = False
        
        # 遍历消息链中的每个组件
        for component in message_chain:
            if component.get('type') == 'Image':
                has_image = True
            elif component.get('type') in ['Plain', 'Quote', 'AtAll', 'At']:
                has_text = True
                
        # 只有当消息中包含图片且不包含文本时返回True
        return has_image and not has_text

    # 当收到个人消息时触发
    @handler(PersonNormalMessageReceived)
    async def person_normal_message_received(self, ctx: EventContext):
        # 获取消息链
        message_chain = ctx.event.message_chain
        
        # 检查是否为纯图片消息
        if self.is_image_only_message(message_chain):
            # 输出调试信息
            self.ap.logger.debug("检测到纯图片消息，添加默认文本")
            
            # 在消息链开头添加默认文本
            default_text = {"type": "Plain", "text": "请根据上下文解读一下这张图片"}
            message_chain.insert(0, default_text)
            
            # 更新消息链
            ctx.event.message_chain = message_chain

    # 当收到群消息时触发
    @handler(GroupNormalMessageReceived)
    async def group_normal_message_received(self, ctx: EventContext):
        # 获取消息链
        message_chain = ctx.event.message_chain
        
        # 检查是否为纯图片消息
        if self.is_image_only_message(message_chain):
            # 输出调试信息
            self.ap.logger.debug("检测到纯图片消息，添加默认文本")
            
            # 在消息链开头添加默认文本
            default_text = {"type": "Plain", "text": "请根据上下文解读一下这张图片"}
            message_chain.insert(0, default_text)
            
            # 更新消息链
            ctx.event.message_chain = message_chain

    # 插件卸载时触发
    def __del__(self):
        pass
