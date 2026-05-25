"""LLM 客户端模块 - 支持通义千问及其他 API"""
import os
import json
from typing import Optional, List, Dict
from datetime import datetime


class LLMClient:
    """LLM 客户端，支持通义千问(Qwen)、OpenAI、Claude 等"""

    PROVIDER_CONFIGS = {
        "qwen": {
            "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
            "models": ["qwen-plus", "qwen-max", "qwen-turbo"],
        },
        "openai": {
            "base_url": "https://api.openai.com/v1",
            "models": ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"],
        },
        "anthropic": {
            "base_url": "https://api.anthropic.com/v1",
            "models": ["claude-3-5-sonnet-20241022", "claude-3-opus-20240229"],
        },
    }

    def __init__(self, provider: Optional[str] = None, api_key: Optional[str] = None,
                 model: Optional[str] = None, base_url: Optional[str] = None):
        """
        初始化 LLM 客户端

        Args:
            provider: 提供商 "qwen" | "openai" | "anthropic"，默认从环境变量读取
            api_key: API密钥，默认从环境变量 DASHSCOPE_API_KEY / OPENAI_API_KEY 读取
            model: 模型名称，默认 qwen-plus
            base_url: API地址，默认使用官方地址
        """
        self.provider = provider or os.getenv("LLM_PROVIDER", "qwen")
        self.api_key = api_key or self._get_api_key()
        self.model = model or self._get_default_model()
        self.base_url = base_url or self.PROVIDER_CONFIGS.get(self.provider, {}).get("base_url", "")

        self._messages: List[Dict] = []
        self.max_history = 20

    def _get_api_key(self) -> str:
        """获取 API 密钥"""
        if self.provider == "qwen":
            return os.getenv("DASHSCOPE_API_KEY", "")
        elif self.provider == "openai":
            return os.getenv("OPENAI_API_KEY", "")
        elif self.provider == "anthropic":
            return os.getenv("ANTHROPIC_API_KEY", "")
        return ""

    def _get_default_model(self) -> str:
        """获取默认模型"""
        if self.provider == "qwen":
            return os.getenv("QWEN_MODEL", "qwen-plus")
        elif self.provider == "openai":
            return os.getenv("OPENAI_MODEL", "gpt-4o")
        elif self.provider == "anthropic":
            return os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")
        return "qwen-plus"

    def chat(self, message: str, system_prompt: Optional[str] = None,
             temperature: float = 0.7, max_tokens: int = 2000) -> str:
        """
        发送对话请求

        Args:
            message: 用户消息
            system_prompt: 系统提示词
            temperature: 温度参数 (0-1)
            max_tokens: 最大Token数

        Returns:
            AI 回复内容
        """
        # 构建消息列表
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.extend(self._messages)
        messages.append({"role": "user", "content": message})

        # 调用 API
        if self.provider == "qwen":
            return self._call_qwen(messages, temperature, max_tokens)
        elif self.provider == "openai":
            return self._call_openai(messages, temperature, max_tokens)
        elif self.provider == "anthropic":
            return self._call_anthropic(messages, temperature, max_tokens)
        else:
            return f"不支持的 provider: {self.provider}"

    def _call_qwen(self, messages: List[Dict], temperature: float, max_tokens: int) -> str:
        """调用通义千问 API"""
        import requests

        if not self.api_key:
            return "错误：未设置 DASHSCOPE_API_KEY 环境变量"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            result = response.json()

            # 检查返回内容是否有效
            if "choices" not in result or len(result["choices"]) == 0:
                return "错误：API返回内容为空"

            assistant_msg = result["choices"][0]["message"]["content"]
            if not assistant_msg or not isinstance(assistant_msg, str):
                return "错误：API返回内容无效"

            # 记录历史
            self._messages.append({
                "role": "user",
                "content": messages[-1]["content"]
            })
            self._messages.append({
                "role": "assistant",
                "content": assistant_msg
            })
            # 保持历史长度
            if len(self._messages) > self.max_history:
                self._messages = self._messages[-self.max_history:]

            return assistant_msg

        except requests.exceptions.Timeout:
            return "错误：请求超时，请检查网络连接"
        except requests.exceptions.RequestException as e:
            return f"错误：API请求失败 - {str(e)}"
        except (KeyError, ValueError, UnicodeDecodeError) as e:
            return f"错误：处理响应失败 - {str(e)}"

    def _call_openai(self, messages: List[Dict], temperature: float, max_tokens: int) -> str:
        """调用 OpenAI API"""
        import requests

        if not self.api_key:
            return "错误：未设置 OPENAI_API_KEY 环境变量"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            result = response.json()

            self._messages.append({
                "role": "user",
                "content": messages[-1]["content"]
            })
            assistant_msg = result["choices"][0]["message"]["content"]
            self._messages.append({
                "role": "assistant",
                "content": assistant_msg
            })

            if len(self._messages) > self.max_history:
                self._messages = self._messages[-self.max_history:]

            return assistant_msg

        except Exception as e:
            return f"错误：API请求失败 - {str(e)}"

    def _call_anthropic(self, messages: List[Dict], temperature: float, max_tokens: int) -> str:
        """调用 Claude API"""
        import requests

        if not self.api_key:
            return "错误：未设置 ANTHROPIC_API_KEY 环境变量"

        # Anthropic 使用不同的消息格式
        system_content = None
        anthropic_messages = []
        for msg in messages:
            if msg["role"] == "system":
                system_content = msg["content"]
            else:
                anthropic_messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })

        headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }

        payload = {
            "model": self.model,
            "messages": anthropic_messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        if system_content:
            payload["system"] = system_content

        try:
            response = requests.post(
                f"{self.base_url}/messages",
                headers=headers,
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            result = response.json()

            self._messages.append({
                "role": "user",
                "content": messages[-1]["content"]
            })
            assistant_msg = result["content"][0]["text"]
            self._messages.append({
                "role": "assistant",
                "content": assistant_msg
            })

            if len(self._messages) > self.max_history:
                self._messages = self._messages[-self.max_history:]

            return assistant_msg

        except Exception as e:
            return f"错误：API请求失败 - {str(e)}"

    def clear_history(self):
        """清除对话历史"""
        self._messages = []

    def set_system_prompt(self, prompt: str):
        """设置系统提示词"""
        self._system_prompt = prompt