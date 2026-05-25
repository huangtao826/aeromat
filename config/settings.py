# aeromat/config/settings.py
import os

# LLM 配置
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "qwen")  # qwen / openai / anthropic / ollama

# 通义千问配置
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY", "")
QWEN_MODEL = os.getenv("QWEN_MODEL", "qwen-plus")

# OpenAI 配置（备选）
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")

# Anthropic 配置（备选）
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")

# Ollama 本地配置（备选）
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:7b")

# 向量数据库配置
VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "./knowledge/vector_db")

# 软件适配器配置
SOFTWARE_ADAPTERS = {
    "material_studio": {
        "name": "Material Studio",
        "modules": ["CASTEP", "DMol3", "Forcite", "Equilibria"],
        "keywords": ["奶昔图", "骰子", "分子结构", "能带", "MS"]
    },
    "vasp": {
        "name": "VASP",
        "modules": ["结构优化", "能带", "DOS", "力学"],
        "keywords": ["INCAR", "POSCAR", "K点", "能带", "vasp"]
    },
    "procast": {
        "name": "Procast",
        "modules": ["铸造仿真", "凝固", "热流"],
        "keywords": ["凝固", "缩孔", "温度梯度", "Procast"]
    },
    "ansys": {
        "name": "Ansys",
        "modules": ["结构力学", "热分析", "流体"],
        "keywords": ["网格", "应力", "变形", "Ansys", "Workbench"]
    },
    "thermo_calc": {
        "name": "Thermo-calc",
        "modules": ["相图", "热力学", "扩散"],
        "keywords": ["相图", "Gibbs", "驱动力", "Thermo-calc", "TC"]
    },
    "abaqus": {
        "name": "Abaqus",
        "modules": ["非线性力学", "塑性", "复合材料"],
        "keywords": ["塑性", "屈服", "本构", "Abaqus", "CAE"]
    }
}

# 理论知识点配置
THEORY_DOMAINS = [
    "晶体学",
    "量子力学",
    "热力学",
    "传热学",
    "力学",
    "材料化学"
]