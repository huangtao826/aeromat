# aeromat/ui/pages/result_compare.py
"""
结果对比页面
"""
import streamlit as st
import pandas as pd


def render_result_compare_page():
    """渲染结果对比页面"""

    st.header("📊 仿真结果对比")

    st.markdown("""
    **功能说明**：
    上传您的仿真结果，与标准范例进行对比，获取理论解释和改进建议。
    """)

    # 软件选择
    software = st.selectbox(
        "选择仿真软件",
        ["VASP", "Material Studio", "Procast", "Ansys", "Thermo-Calc", "Abaqus"]
    )

    # 结果类型
    result_type = st.selectbox(
        "选择结果类型",
        ["能带结构", "态密度", "结构优化", "凝固模拟", "应力分析", "相图"]
    )

    # 文件上传
    st.subheader("上传仿真结果")
    uploaded_file = st.file_uploader(
        "拖拽或点击上传文件",
        type=["csv", "txt", "dat", "png", "jpg"],
        help="支持表格数据和图像文件"
    )

    if uploaded_file:
        st.success(f"已上传：{uploaded_file.name}")

        # 模拟对比结果
        st.markdown("---")
        st.subheader("对比分析结果")

        # 创建示例对比数据
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**您的结果**")
            if result_type == "能带结构":
                st.metric("带隙值", "1.23 eV", "间接带隙")
                st.metric("价带顶位置", "Γ点")
                st.metric("导带底位置", "K点")
            else:
                st.info("正在解析数据...")

        with col2:
            st.markdown("**标准范例**")
            if result_type == "能带结构":
                st.metric("带隙值", "1.50 eV", "间接带隙")
                st.metric("价带顶位置", "Γ点")
                st.metric("导带底位置", "K点")

        # 偏差分析
        st.markdown("---")
        st.subheader("📈 偏差分析")

        deviation_data = {
            "参数": ["带隙", "晶格常数a", "晶格常数c"],
            "您的结果": [1.23, 3.62, 3.62],
            "标准值": [1.50, 3.61, 3.61],
            "偏差": ["-18%", "+0.3%", "+0.3%"]
        }
        df = pd.DataFrame(deviation_data)
        st.table(df)

        # 理论解释
        st.markdown("---")
        st.subheader("💡 理论解释")

        st.markdown("""
        **带隙偏低原因分析**：

        1. **泛函选择**：GGA-PGA泛函系统性低估带隙（约30-50%）
        2. **自旋轨道耦合**：对于重元素，SOC效应显著影响价带

        **建议改进方案**：

        | 方案 | 精度 | 计算时间 | 适用场景 |
        |------|------|---------|---------|
        | 继续使用GGA | 低 | 短 | 初步筛选 |
        | HSE06杂化泛函 | 中 | 中 | 半导体材料 |
        | GW近似 | 高 | 长 | 精确计算 |
        """)

        # 按钮
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                "📥 下载分析报告",
                data="分析报告内容",
                file_name="analysis_report.txt"
            )
        with col2:
            st.button("🔄 重新对比")


if __name__ == "__main__":
    render_result_compare_page()