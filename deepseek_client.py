"""
DeepSeek API客户端
支持流式输出
"""
import httpx
import json
from typing import AsyncIterator
from config import DEEPSEEK_API_KEY, DEEPSEEK_API_URL, MODEL_NAME, MAX_TOKENS, TEMPERATURE


class DeepSeekClient:
    """DeepSeek API客户端"""
    
    def __init__(self):
        self.api_key = DEEPSEEK_API_KEY
        self.api_url = DEEPSEEK_API_URL
        self.model = MODEL_NAME
        self.max_tokens = MAX_TOKENS
        self.temperature = TEMPERATURE
        
        if not self.api_key:
            raise ValueError("请设置DEEPSEEK_API_KEY环境变量")
    
    async def chat_stream(
        self, 
        messages: list, 
        model: str = None,
        temperature: float = None
    ) -> AsyncIterator[str]:
        """
        流式调用DeepSeek API
        
        Args:
            messages: 消息列表
            model: 模型名称，默认使用配置的模型
            temperature: 温度参数，默认使用配置的值
            
        Yields:
            流式返回的文本片段
        """
        if model is None:
            model = self.model
        if temperature is None:
            temperature = self.temperature
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": model,
            "messages": messages,
            "stream": True,
            "max_tokens": self.max_tokens,
            "temperature": temperature
        }
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            async with client.stream("POST", self.api_url, headers=headers, json=data) as response:
                if response.status_code != 200:
                    error_text = await response.aread()
                    raise Exception(f"API调用失败: {response.status_code}, {error_text.decode()}")
                
                async for line in response.aiter_lines():
                    if not line.strip():
                        continue
                    
                    if line.startswith("data: "):
                        data_str = line[6:]  # 移除 "data: " 前缀
                        
                        if data_str == "[DONE]":
                            break
                        
                        try:
                            data_json = json.loads(data_str)
                            choices = data_json.get("choices", [])
                            if choices:
                                delta = choices[0].get("delta", {})
                                content = delta.get("content", "")
                                if content:
                                    yield content
                        except json.JSONDecodeError:
                            continue
    
    async def chat(
        self,
        messages: list,
        model: str = None,
        temperature: float = None
    ) -> str:
        """
        非流式调用DeepSeek API（用于测试）
        
        Args:
            messages: 消息列表
            model: 模型名称
            temperature: 温度参数
            
        Returns:
            完整的回复文本
        """
        result = ""
        async for chunk in self.chat_stream(messages, model, temperature):
            result += chunk
        return result

