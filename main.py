# coding:utf-8
from pkg.plugin.models import *
from pkg.plugin.host import EventContext, PluginHost
import logging


class ImageProcessor:
    """图片消息处理器"""
    def __init__(self):
        self.default_prompt = "解读一下这张图片"
    
    def process(self, event: EventContext) -> dict:
        """处理图片消息
        
        Args:
            event: 事件上下文
            
        Returns:
            dict: 处理结果
        """
        try:
            # 检查是否是纯图片消息
            if not self._is_image_only_message(event):
                return {"status": 0, "message": "不是纯图片消息"}
            
            # 处理消息
            return {
                "status": 200,
                "content": {
                    "prompt": self.default_prompt,
                    "image_count": len(event.event.image_list)
                }
            }
        except Exception as e:
            logging.error(f"处理图片消息时出错: {str(e)}")
            return {"status": 500, "message": f"处理失败: {str(e)}"}

    def _is_image_only_message(self, event: EventContext) -> bool:
        """检查是否为纯图片消息"""
        return (not event.event.text_message or event.event.text_message.strip() == "") and event.event.image_list


@register(name="BlankImageHandler", 
         description="处理只发送图片的情况，自动添加解读提示", 
         version="0.5", 
         author="Nothingness-Void")
class BlankImagePlugin(Plugin):
    """处理纯图片消息的插件"""

    def __init__(self, plugin_host: PluginHost):
        self.processor = ImageProcessor()
        self.logger = logging.getLogger(__name__)

    @on(NormalMessageReceived)
    def handle_message(self, event: EventContext, **kwargs):
        """处理接收到的消息"""
        # 处理消息
        result = self.processor.process(event)
        
        # 检查处理结果
        if result["status"] == 200:
            # 添加提示文本
            event.event.text_message = result["content"]["prompt"]
            self.logger.debug(
                f"已处理图片消息 - 图片数量: {result['content']['image_count']}, "
                f"添加提示: {result['content']['prompt']}"
            )
        elif result["status"] == 0:
            # 不是纯图片消息，忽略
            pass
        else:
            # 处理失败
            self.logger.error(f"处理图片消息失败: {result['message']}")

    def __del__(self):
        """插件卸载时触发"""
        pass
