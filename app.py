# aeromat/app.py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aeromat AI - 材料科学智能教学助手
连接理论分析与仿真软件操作的AI Agent
"""

import streamlit as st

# 页面配置
st.set_page_config(
    page_title="Aeromat AI - 材料科学智能助手",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 导入Agent和UI组件
import sys
from pathlib import Path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from aeromat.agents import CoreAgent
from aeromat.ui.components.software_selector import (
    render_software_selector,
    render_software_badge,
    render_software_icon_large,
    get_all_software_list
)

# 初始化Agent
if "core_agent" not in st.session_state:
    st.session_state.core_agent = CoreAgent()
    st.session_state.messages = []
    st.session_state.selected_software = None

# 侧边栏 - 软件选择器
st.sidebar.markdown("---")
st.sidebar.subheader("🖥️ 软件选择")

# 渲染软件选择器
selected = render_software_selector("software_selector")

if selected:
    st.sidebar.success(f"已选择: {render_software_badge(selected)}")
    st.session_state.selected_software = selected

st.sidebar.markdown("---")
st.sidebar.markdown("""
**功能说明**

🤖 **智能对话**：解释理论、指导操作、分析结果

📚 **软件支持**：
- Material Studio
- VASP
- Procast
- Ansys
- Thermo-Calc
- Abaqus

💡 **使用提示**：
直接描述您遇到的问题，我会帮您分析原因并提供解决方案。
""")

st.sidebar.markdown("---")
st.sidebar.markdown("""
**相关链接**

- [Materials Project](https://materialsproject.org)
- [VASP Wiki](https://www.vasp.at/wiki/)
- [Ansys Learning](https://www.ansys.com/academic)
""")

# 主界面
st.title("🧪 Aeromat AI - 材料科学智能教学助手")

# 显示当前选择的软件上下文和大图标
if st.session_state.get("selected_software"):
    software = st.session_state.selected_software
    col1, col2 = st.columns([1, 5])
    with col1:
        st.markdown(render_software_icon_large(software), unsafe_allow_html=True)
    with col2:
        st.info(f"📖 当前学习：{render_software_badge(software)}")

st.markdown("""
欢迎使用 **Aeromat AI** 智能助手。

我可以帮助您：
- 📖 理解材料科学理论原理
- 💻 掌握仿真软件操作技巧
- 📊 分析仿真计算结果
- 🔧 优化工艺参数

**请在下方输入您的问题：**
""")

# 对话历史显示
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 用户输入
user_input = st.chat_input("请输入您的问题...")

if user_input:
    # 显示用户消息
    with st.chat_message("user"):
        st.markdown(user_input)

    # 添加到历史
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 获取Agent响应
    agent = st.session_state.core_agent
    intent = agent.recognize_intent(user_input)
    software_context = st.session_state.get("selected_software")
    response = agent.route_to_sub_agents(intent, user_input, software_context)

    # 显示助手响应
    with st.chat_message("assistant"):
        st.markdown(response)

    # 添加到历史
    st.session_state.messages.append({"role": "assistant", "content": response})

# 清空对话按钮
if st.sidebar.button("🗑️ 清空对话"):
    st.session_state.messages = []
    st.session_state.core_agent.clear_history()
    st.rerun()

# 底部信息
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>Aeromat AI - 材料科学理论与仿真软件桥梁</p>
    <p>帮助学生建立"理论 → 仿真 → 现象 → 原理"的完整认知闭环</p>
</div>
""", unsafe_allow_html=True)