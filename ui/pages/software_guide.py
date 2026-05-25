# aeromat/ui/pages/software_guide.py
"""
软件操作指南页面
"""
import streamlit as st


def render_software_guide_page():
    """渲染软件指南页面"""

    st.header("💻 仿真软件操作指南")

    # 软件选择
    software_options = {
        "Material Studio": {
            "icon": "🔬",
            "modules": ["CASTEP", "DMol³", "Forcite", "Equilibria"],
            "description": "BIOVIA开发的材料科学综合平台，支持从原子尺度到宏观尺度的模拟。"
        },
        "VASP": {
            "icon": "⚡",
            "modules": ["结构优化", "能带计算", "态密度", "磁性", "声子"],
            "description": "维也纳大学开发的第一性原理计算软件，基于密度泛函理论。"
        },
        "Procast": {
            "icon": "🔥",
            "modules": ["凝固模拟", "温度场", "缩孔预测", "热应力"],
            "description": "ESI集团的铸造仿真软件，用于优化铸造工艺设计。"
        },
        "Ansys": {
            "icon": "🔧",
            "modules": ["结构力学", "热分析", "流体", "电磁"],
            "description": "通用的有限元分析软件，用于工程仿真和多物理场分析。"
        },
        "Thermo-Calc": {
            "icon": "📊",
            "modules": ["相图计算", "热力学平衡", "驱动力", "扩散"],
            "description": "热力学计算软件，用于材料性质的热力学计算和相图预测。"
        },
        "Abaqus": {
            "icon": "⚙️",
            "modules": ["非线性力学", "塑性", "复合材料", "冲击"],
            "description": "达索系统的高端非线性有限元分析软件。"
        }
    }

    selected_software = st.selectbox(
        "选择软件",
        options=list(software_options.keys()),
        format_func=lambda x: f"{software_options[x]['icon']} {x}"
    )

    software_info = software_options[selected_software]

    # 显示软件信息
    st.markdown(f"## {software_info['icon']} {selected_software}")
    st.markdown(f"**简介**：{software_info['description']}")

    # 模块选择
    st.subheader("选择模块")
    selected_module = st.selectbox(
        "可用模块",
        software_info["modules"]
    )

    # 根据选择显示不同内容
    if selected_software == "Material Studio" and selected_module == "CASTEP":
        st.markdown("""
        ### CASTEP 能带计算步骤

        **1. 结构优化**
        - Task → Geometry Optimization
        - Quality → Fine
        - Functional → GGA-PBE

        **2. 能带计算**
        - Task → Band Structure
        - 设置K点路径

        **3. 结果分析**
        - 识别价带顶、导带底
        - 判断带隙类型
        """)
    elif selected_software == "VASP" and selected_module == "结构优化":
        st.markdown("""
        ### VASP 结构优化

        **INCAR 关键参数**：
        ```
        ENCUT = 520        # 截断能
        EDIFF = 1E-5       # 电子收敛标准
        EDIFFG = -0.02     # 力收敛标准
        IBRION = 2         # 优化算法
        ISIF = 3           # 优化原子和晶格
        ```

        **输入文件**：INCAR, POSCAR, POTCAR, KPOINTS
        """)
    elif selected_software == "Procast" and selected_module == "凝固模拟":
        st.markdown("""
        ### Procast 凝固模拟

        **前处理**：
        - 导入几何模型
        - 定义材料热物性
        - 设置边界条件

        **求解**：
        - 传热+流动耦合
        - 凝固收缩补偿

        **后处理**：
        - 温度场分布
        - 缩孔预测
        """)
    else:
        st.info(f"{selected_software} - {selected_module} 的详细指南正在完善中...")

    # 常见问题
    st.markdown("---")
    st.subheader("❓ 常见问题")

    with st.expander("软件安装问题"):
        st.markdown("""
        **Q**: 安装后无法启动？
        **A**: 检查许可证配置，环境变量设置是否正确。
        """)

    with st.expander("计算收敛问题"):
        st.markdown("""
        **Q**: 计算不收敛怎么办？
        **A**: 1) 检查输入文件格式 2) 调整参数设置 3) 增加计算资源
        """)


if __name__ == "__main__":
    render_software_guide_page()