"""软件选择器组件"""
import streamlit as st
from pathlib import Path
from typing import Optional


# 图标目录
ICONS_DIR = Path(__file__).parent.parent / "icons"


def get_software_icon_html(software: str, size: int = 48) -> str:
    """获取软件图标（支持本地图片或emoji）"""
    icon_map = {
        "material_studio": ("ms.png", "🔬"),
        "vasp": ("vasp.png", "⚡"),
        "procast": ("procast.png", "🏭"),
        "ansys": ("ansys.png", "🔧"),
        "thermo_calc": ("thermo.png", "📊"),
        "abaqus": ("abaqus.png", "🎯")
    }

    icon_file, emoji = icon_map.get(software, (None, "❓"))
    icon_path = ICONS_DIR / icon_file

    if icon_file and icon_path.exists():
        # 使用本地图片
        import base64
        with open(icon_path, "rb") as f:
            img_data = base64.b64encode(f.read()).decode()
        return f'<img src="data:image/png;base64,{img_data}" width="{size}" height="{size}" style="border-radius:8px;">'
    else:
        # 回退到 emoji
        return f'<span style="font-size:{size}px;">{emoji}</span>'


def render_software_selector(key: str = "software_selector") -> Optional[str]:
    """渲染软件选择器组件，返回选中的软件名称"""

    software_options = {
        "material_studio": {
            "name": "Materials Studio",
            "icon": "🔬",
            "description": "材料科学综合平台（CASTEP, DMol³, Forcite）",
            "color": "#4A90D9"
        },
        "vasp": {
            "name": "VASP",
            "icon": "⚡",
            "description": "第一性原理计算软件（能带、结构优化）",
            "color": "#E74C3C"
        },
        "procast": {
            "name": "Procast",
            "icon": "🏭",
            "description": "铸造凝固仿真软件",
            "color": "#27AE60"
        },
        "ansys": {
            "name": "Ansys",
            "icon": "🔧",
            "description": "通用有限元分析软件",
            "color": "#8E44AD"
        },
        "thermo_calc": {
            "name": "Thermo-Calc",
            "icon": "📊",
            "description": "热力学相图计算软件",
            "color": "#F39C12"
        },
        "abaqus": {
            "name": "Abaqus",
            "icon": "🎯",
            "description": "非线性力学分析软件",
            "color": "#16A085"
        }
    }

    if key not in st.session_state:
        st.session_state[key] = None

    selected = st.selectbox(
        "🖥️ 请选择您要学习的软件：",
        options=[""] + list(software_options.keys()),
        format_func=lambda x: software_options[x]["name"] + " " + software_options[x]["icon"] if x else "选择一个软件...",
        key=f"{key}_select"
    )

    if selected:
        info = software_options[selected]
        icon_html = get_software_icon_html(selected, size=48)
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, {info['color']}22, {info['color']}11);
            border-left: 4px solid {info['color']};
            padding: 12px 16px;
            border-radius: 8px;
            margin: 12px 0;
            display: flex;
            align-items: center;
            gap: 12px;
        ">
            <div>{icon_html}</div>
            <div style="font-size: 14px; color: #666;">
                📖 <strong>{info['name']}</strong> - {info['description']}
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.session_state[key] = selected
        return selected

    return None


def render_software_badge(software: str) -> str:
    """渲染软件徽章"""
    badges = {
        "material_studio": "🔬 Materials Studio",
        "vasp": "⚡ VASP",
        "procast": "🏭 Procast",
        "ansys": "🔧 Ansys",
        "thermo_calc": "📊 Thermo-Calc",
        "abaqus": "🎯 Abaqus"
    }
    return badges.get(software, software)


def render_software_icon_large(software: str) -> str:
    """渲染大图标（用于主界面展示）"""
    return get_software_icon_html(software, size=64)


def get_all_software_list() -> list:
    """获取所有软件列表"""
    return ["material_studio", "vasp", "procast", "ansys", "thermo_calc", "abaqus"]