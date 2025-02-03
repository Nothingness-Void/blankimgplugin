# coding:utf-8
from pkg.plugin.models import *
from pkg.plugin.host import EventContext, PluginHost


@register(name="BlankImageHandler", description="处理只发送图片的情况，自动添加解读提示", version="0.5", author="Nothingness-Void")
class BlankImagePlugin(Plugin):

    # 插件加载时触发
    def __init__(self, plugin_host: PluginHost):
        self.default_prompt = "解读一下这张图片"

    @on(NormalMessageReceived)
    def handle_message(self, event: EventContext, **kwargs):
        # 检查是否是纯图片消息（没有文本但有图片）
        if (not event.event.text_message or event.event.text_message.strip() == "") and event.event.image_list:
            # 添加默认提示文本
            event.event.text_message = self.default_prompt
            self.ap.logger.debug(f"为消息添加解读提示: {self.default_prompt}")

    # 插件卸载时触发
    def __del__(self):
        pass
