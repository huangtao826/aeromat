# aeromat/ui/pages/theory_tutorial.py
"""
理论教程页面
"""
import streamlit as st


def render_theory_tutorial_page():
    """渲染理论教程页面"""

    st.header("📚 材料科学理论教程")

    # 理论主题选择
    theory_topics = {
        "晶体学基础": {
            "icon": "💎",
            "subsections": ["晶系与点群", "布拉维格子", "晶面指数", "倒格子"]
        },
        "量子力学": {
            "icon": "⚛️",
            "subsections": ["薛定谔方程", "氢原子轨道", "能带理论", "态密度"]
        },
        "热力学": {
            "icon": "🌡️",
            "subsections": ["吉布斯自由能", "相图基础", "相变热力学", "杠杆法则"]
        },
        "传热学": {
            "icon": "🔥",
            "subsections": ["导热定律", "对流换热", "辐射换热", "非稳态传热"]
        },
        "力学": {
            "icon": "⚙️",
            "subsections": ["应力应变", "弹性力学", "塑性力学", "有限元基础"]
        },
        "材料化学": {
            "icon": "🧪",
            "subsections": ["化学键", "晶体场理论", "分子轨道", "缺陷化学"]
        }
    }

    selected_topic = st.selectbox(
        "选择理论主题",
        options=list(theory_topics.keys()),
        format_func=lambda x: f"{theory_topics[x]['icon']} {x}"
    )

    topic_info = theory_topics[selected_topic]

    st.markdown(f"## {topic_info['icon']} {selected_topic}")

    # 子主题选择
    selected_subsection = st.selectbox(
        "选择子主题",
        topic_info["subsections"]
    )

    # 显示教学内容
    if selected_topic == "晶体学基础":
        if selected_subsection == "晶系与点群":
            st.markdown("""
            ### 晶体学基础：晶系与点群

            **七大晶系**：

            | 晶系 | 轴长关系 | 轴角关系 | 点群数 |
            |------|---------|---------|-------|
            | 三斜 | a≠b≠c | α≠β≠γ≠90° | 2 |
            | 单斜 | a≠b≠c | α=γ=90°≠β | 3 |
            | 正交 | a≠b≠c | α=β=γ=90° | 3 |
            | 四方 | a=b≠c | α=β=γ=90° | 7 |
            | 三方 | a=b=c | α=β=γ≠90° | 5 |
            | 六方 | a=b≠c | α=β=90°, γ=120° | 7 |
            | 立方 | a=b=c | α=β=γ=90° | 5 |

            **对称元素**：旋转轴（1,2,3,4,6次）、反演中心、镜面
            """)
        elif selected_subsection == "晶面指数":
            st.markdown("""
            ### 晶面指数 (Miller Indices)

            **定义**：晶面与坐标轴的截距的倒数比

            **表示方法**：**(hkl)**

            **步骤**：
            1. 找到晶面与三个坐标轴的截距
            2. 取倒数的最简整数比
            3. 化为 (hkl) 形式

            **示例**：
            - 与 x,y,z 轴截距为 2,3,1 → (1/2, 1/3, 1) → **(632)**
            """)

    elif selected_topic == "量子力学":
        if selected_subsection == "能带理论":
            st.markdown("""
            ### 能带理论

            **核心概念**：
            - **价带**：已占据的电子能级
            - **导带**：未占据的电子能级
            - **带隙**：E_g = E_c - E_v

            **能带形成**：
            原子轨道 → 分子轨道 → 能带（大量原子）

            **分类**：
            - 金属：带隙 = 0（导带与价带重叠）
            - 半导体：0 < E_g < 3 eV
            - 绝缘体：E_g > 3 eV

            **计算方法**：
            - DFT（LDA/GGA）：会系统性低估带隙
            - GW近似：更准确但计算量大
            - 杂化泛函（HSE06）：平衡精度与效率
            """)

    elif selected_topic == "热力学":
        if selected_subsection == "吉布斯自由能":
            st.markdown("""
            ### 吉布斯自由能 (G)

            **定义**：G = H - TS

            **物理意义**：
            - 在恒温恒压条件下，判断反应方向
            - ΔG < 0：自发过程
            - ΔG = 0：平衡状态

            **相变应用**：
            - 固相 vs 液相：ΔG = ΔH - TΔS
            - 凝固驱动力：ΔG ∝ ΔT（过冷度）
            """)

    st.markdown("---")
    st.info("💡 更多教学内容持续更新中...")


if __name__ == "__main__":
    render_theory_tutorial_page()