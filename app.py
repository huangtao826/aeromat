#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aeromat AI - 材料科学智能教学助手
Streamlit 主应用 - v2.0 完整版
"""

import os
import sys
import base64

# 将项目根目录加入路径（兼容开发和打包环境）
if getattr(sys, "frozen", False):
    project_root = sys._MEIPASS
else:
    project_root = os.path.dirname(os.path.abspath(__file__))

if project_root not in sys.path:
    sys.path.insert(0, project_root)

import streamlit as st
from aeromat.agents import CoreAgent
from aeromat.core import LLMClient

# ==================== 页面配置 ====================
st.set_page_config(
    page_title="Aeromat AI - 材料科学助手",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== 图片路径处理 ====================
def get_image_path(filename="aeromat_banner.png"):
    """获取图片路径（兼容开发和打包环境）"""
    possible_paths = [
        os.path.join(project_root, filename),
        os.path.join(project_root, "assets", filename),
        os.path.join(project_root, "_internal", filename),
        os.path.join(os.path.dirname(sys.executable), filename),
    ]
    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None

def get_image_base64(image_path):
    """将图片转为 base64"""
    if not image_path or not os.path.exists(image_path):
        return None
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# ==================== 自定义样式 ====================
def set_custom_style():
    """设置自定义样式"""
    img_path = get_image_path("aeromat_banner.png")
    img_base64 = get_image_base64(img_path)

    css = """
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    }
    .main-header-container {
        background: linear-gradient(135deg, #1e3a8a 0%, #0f172a 100%);
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        border: 1px solid #3b82f6;
        box-shadow: 0 0 20px rgba(59, 130, 246, 0.3);
    }
    .main-title {
        font-size: 2.8rem;
        font-weight: bold;
        color: #60a5fa;
        text-align: center;
        margin-bottom: 5px;
        text-shadow: 0 0 10px rgba(96, 165, 250, 0.5);
    }
    .sub-title {
        font-size: 1.2rem;
        color: #94a3b8;
        text-align: center;
        margin-bottom: 15px;
    }
    .stChatMessage {
        background: rgba(30, 41, 59, 0.8) !important;
        border-radius: 10px;
        border: 1px solid #334155;
        margin-bottom: 10px;
    }
    .stChatMessage[data-testid="stChatMessageUser"] {
        border-left: 3px solid #3b82f6;
    }
    .stChatMessage[data-testid="stChatMessageAssistant"] {
        border-left: 3px solid #10b981;
    }
    .stButton>button {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        box-shadow: 0 0 15px rgba(59, 130, 246, 0.5);
        transform: translateY(-2px);
    }
    .api-status-connected {
        background: linear-gradient(135deg, #059669 0%, #047857 100%);
        color: white;
        padding: 10px;
        border-radius: 8px;
        text-align: center;
        font-weight: bold;
    }
    .api-status-disconnected {
        background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
        color: white;
        padding: 10px;
        border-radius: 8px;
        text-align: center;
        font-weight: bold;
    }
    .feature-card {
        background: rgba(30, 41, 59, 0.9);
        border: 1px solid #475569;
        border-radius: 12px;
        padding: 20px;
        height: 100%;
        transition: all 0.3s ease;
    }
    .feature-card:hover {
        border-color: #3b82f6;
        box-shadow: 0 0 15px rgba(59, 130, 246, 0.2);
    }
    </style>
    """

    if img_base64:
        css += f"""
        <style>
        .banner-bg {{
            background-image: url("data:image/png;base64,{img_base64}");
            background-size: cover;
            background-position: center;
            border-radius: 15px;
            height: 300px;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
            overflow: hidden;
            margin-bottom: 20px;
        }}
        .banner-bg::before {{
            content: "";
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.85) 0%, rgba(30, 41, 59, 0.75) 100%);
            z-index: 1;
        }}
        .banner-content {{
            position: relative;
            z-index: 2;
            text-align: center;
            padding: 20px;
        }}
        </style>
        """

    st.markdown(css, unsafe_allow_html=True)

# ==================== Session State ====================
def init_session_state():
    defaults = {
        "messages": [],
        "core_agent": None,
        "api_key": os.getenv("DASHSCOPE_API_KEY", ""),
        "api_provider": os.getenv("LLM_PROVIDER", "qwen"),
        "api_model": os.getenv("QWEN_MODEL", "qwen-plus"),
        "api_connected": False,
        "conversation_started": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# ==================== API 测试 ====================
def test_api_connection(api_key, provider, model):
    if not api_key:
        return False, "API Key 为空"
    try:
        client = LLMClient(provider=provider, api_key=api_key, model=model)
        response = client.chat("你好，请回复'连接成功'", system_prompt="测试助手", temperature=0.1, max_tokens=50)
        if "错误" in response or "失败" in response:
            return False, response
        return True, "连接成功"
    except Exception as e:
        return False, f"连接异常: {str(e)}"

# ==================== 侧边栏 ====================
def render_sidebar():
    with st.sidebar:
        st.markdown("### ⚙️ 系统配置")

        provider = st.selectbox(
            "选择 LLM 提供商",
            options=["qwen", "openai", "anthropic"],
            format_func=lambda x: {"qwen": "🟢 通义千问", "openai": "🔵 OpenAI", "anthropic": "🟣 Claude"}.get(x, x),
            index=["qwen", "openai", "anthropic"].index(st.session_state.api_provider) if st.session_state.api_provider in ["qwen", "openai", "anthropic"] else 0,
        )
        st.session_state.api_provider = provider

        model_options = {
            "qwen": ["qwen-plus", "qwen-max", "qwen-turbo", "qwen-long"],
            "openai": ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"],
            "anthropic": ["claude-3-5-sonnet-20241022", "claude-3-opus-20240229"]
        }
        available_models = model_options.get(provider, ["qwen-plus"])
        current_model = st.session_state.api_model
        if current_model not in available_models:
            current_model = available_models[0]

        model = st.selectbox("选择模型", options=available_models, index=available_models.index(current_model))
        st.session_state.api_model = model

        st.markdown("### 🔑 API 密钥")
        api_key = st.text_input("API Key", type="password", value=st.session_state.api_key, placeholder="请输入 API Key")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🚀 连接测试", type="primary", use_container_width=True):
                if not api_key:
                    st.error("❌ 请输入 API Key")
                else:
                    with st.spinner("连接中..."):
                        success, msg = test_api_connection(api_key, provider, model)
                        if success:
                            st.session_state.api_key = api_key
                            st.session_state.api_connected = True
                            os.environ["DASHSCOPE_API_KEY"] = api_key if provider == "qwen" else ""
                            os.environ["OPENAI_API_KEY"] = api_key if provider == "openai" else ""
                            os.environ["ANTHROPIC_API_KEY"] = api_key if provider == "anthropic" else ""
                            st.session_state.core_agent = CoreAgent()
                            st.success(f"✅ {msg}")
                        else:
                            st.session_state.api_connected = False
                            st.error(f"❌ {msg}")

        with col2:
            if st.button("🗑️ 清除", use_container_width=True):
                st.session_state.api_key = ""
                st.session_state.api_connected = False
                st.session_state.core_agent = CoreAgent()
                st.info("已切换为本地模式")
                st.rerun()

        st.markdown("---")
        if st.session_state.api_connected:
            st.markdown(f'<div class="api-status-connected">✅ 已连接: {provider}/{model}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="api-status-disconnected">⚠️ 未连接: 本地模式</div>', unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 🛠️ 快捷操作")
        if st.button("🗑️ 清除对话", use_container_width=True):
            st.session_state.messages = []
            if st.session_state.core_agent:
                st.session_state.core_agent.clear_history()
            st.session_state.conversation_started = False
            st.rerun()

        with st.expander("📖 使用说明"):
            st.markdown("""
            **1. 配置 API**：选择提供商 → 输入 Key → 连接测试
            **2. 开始对话**：输入材料科学相关问题
            **3. 支持软件**：Material Studio, VASP, ProCAST, ANSYS, Abaqus, Thermo-Calc
            **4. 本地模式**：不配置 Key 时使用预设知识库
            """)

        st.markdown("---")
        st.caption("Aeromat AI v2.0 | 西安航空学院")

# ==================== 主界面 ====================
def render_header():
    img_path = get_image_path("aeromat_banner.png")
    if img_path:
        st.markdown("""
        <div class="banner-bg">
            <div class="banner-content">
                <div class="main-title">🧪 Aeromat AI</div>
                <div class="sub-title">材料科学智能教学助手</div>
                <div style="color: #cbd5e1; font-size: 1rem;">理论讲解 · 软件指导 · 结果分析 · ML驱动设计</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="main-header-container">
            <div class="main-title">🧪 Aeromat AI</div>
            <div class="sub-title">材料科学智能教学助手</div>
            <div style="color: #cbd5e1; text-align: center;">理论讲解 · 软件指导 · 结果分析 · ML驱动设计</div>
        </div>
        """, unsafe_allow_html=True)
        with st.expander("💡 如何添加背景图片？"):
            st.info("将图片命名为 aeromat_banner.png，放在与 exe 同级目录或项目根目录")

def render_features():
    if st.session_state.conversation_started:
        return
    st.markdown("### 🎯 核心功能")
    cols = st.columns(3)
    features = [
        ("📚", "理论讲解", "材料科学原理深度解析\n结构优化、能带分析\n热力学、力学基础"),
        ("💻", "软件指导", "Material Studio操作\nVASP计算设置\nProCAST铸造模拟"),
        ("📊", "结果分析", "能带图解读\n态密度分析\n应力应变解释"),
    ]
    for i, (icon, title, desc) in enumerate(features):
        with cols[i]:
            st.markdown(f'<div class="feature-card"><div style="font-size:2.5rem">{icon}</div><div style="font-size:1.2rem;font-weight:bold;color:#60a5fa;margin:10px 0">{title}</div><div style="color:#94a3b8;font-size:0.95rem">{desc}</div></div>', unsafe_allow_html=True)

def render_examples():
    if st.session_state.conversation_started:
        return
    st.markdown("---")
    st.markdown("### 💡 快速示例")
    examples = [
        "Material Studio 怎么做结构优化？",
        "能带图怎么看带隙大小？",
        "VASP计算不收敛怎么办？",
        "铸造缩孔怎么优化？",
        "什么是态密度（DOS）？"
    ]
    cols = st.columns(len(examples))
    for i, example in enumerate(examples):
        with cols[i]:
            if st.button(example, key=f"ex_{i}", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": example})
                st.session_state.conversation_started = True
                st.rerun()

def render_chat():
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("请输入你的问题..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.conversation_started = True

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("🤔 思考中..."):
                try:
                    intent = st.session_state.core_agent.recognize_intent(prompt)
                    response = st.session_state.core_agent.route_to_sub_agents(intent=intent, user_input=prompt)
                except Exception as e:
                    response = f"❌ 处理出错: {str(e)}\n\n请检查 API 配置或尝试重新连接。"
            st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})

# ==================== 入口 ====================
def main():
    set_custom_style()
    render_sidebar()
    if st.session_state.core_agent is None:
        st.session_state.core_agent = CoreAgent()
    render_header()
    render_features()
    render_examples()
    render_chat()

if __name__ == "__main__":
    main()
