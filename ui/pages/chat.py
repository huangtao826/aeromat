# aeromat/ui/pages/chat.py
"""
智能对话页面
"""
import streamlit as st
from aeromat.agents import CoreAgent


def render_chat_page():
    """渲染智能对话页面"""
    st.header("💬 智能对话")

    # 初始化Agent
    if "core_agent" not in st.session_state:
        st.session_state.core_agent = CoreAgent()

    # 对话历史
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # 显示历史消息
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # 用户输入
    user_input = st.chat_input("请输入您的问题...")

    if user_input:
        # 处理用户输入
        agent = st.session_state.core_agent
        intent = agent.recognize_intent(user_input)
        response = agent.route_to_sub_agents(intent, user_input)

        # 记录对话
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        st.session_state.chat_history.append({"role": "assistant", "content": response})

        # 刷新页面显示新消息
        st.rerun()

    # 清空按钮
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("🗑️ 清空对话"):
            st.session_state.chat_history = []
            st.session_state.core_agent.clear_history()
            st.rerun()


if __name__ == "__main__":
    render_chat_page()