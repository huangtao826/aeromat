# aeromat/adapters/thermo_calc.py
"""
Thermo-Calc 软件适配器
"""
from typing import Dict, List


class ThermoCalcAdapter:
    """Thermo-Calc 热力学计算适配器"""

    def __init__(self):
        self.name = "Thermo-Calc"
        self.keywords = ["thermo-calc", "tc", "相图", "gibbs", "驱动力", "热力学"]
        self.databases = ["TCFE", "SGTE", "TCOX", "TCNI"]

    def parse_phase_diagram(self, diagram_data: Dict) -> Dict:
        """解析相图数据"""
        return {
            "phases": diagram_data.get("phases", []),
            "phase_boundaries": diagram_data.get("boundaries", []),
            "invariant_points": diagram_data.get("invariants", [])
        }

    def calculate_driving_force(self, composition: Dict, temperature: float) -> Dict:
        """计算相变驱动力"""
        # ΔG = G_matrix - G_precipitate
        return {
            "driving_force": None,  # J/mol
            "nucleation_barrier": None,
            "critical_radius": None
        }

    def get_theory_correlation(self, property_type: str) -> Dict:
        """获取理论关联"""
        correlations = {
            "相图": ["吉布斯自由能", "相平衡条件", "杠杆法则", "相变热力学"],
            "驱动力": ["形核理论", "相变动力学", "界面能", "过冷度"],
            "活度": ["化学势", "理想溶液模型", "规则溶液模型"],
            "热容": ["杜隆-珀替定律", "爱因斯坦模型", "德拜模型"]
        }
        return correlations.get(property_type, {})

    def explain_phase_transformation(self, phase_data: Dict) -> str:
        """解释相变"""
        phase_type = phase_data.get("type", "unknown")
        temperature = phase_data.get("temperature", 0)

        explanations = {
            "solidification": f"""凝固是液相到固相的转变。

**相变特征**：
- 潜热释放：L = ΔH_fus
- 温度：恒定（理论上）直到潜热完全释放
- 驱动力：过冷度 ΔT

**在Thermo-Calc中**：
- 使用相图计算凝固路径
- 预测相组成随温度变化""",

            "precipitation": f"""析出是固溶体中形成新相的过程。

**驱动力**：
- ΔG = G_matrix - G_precipitate < 0

**经典形核理论**：
- 形核功：ΔG* = 16πγ³/3ΔG²
- 临界半径：r* = -2γ/ΔG

**在Thermo-Calc中**：
- 计算驱动力（Driving Force）
- 预测析出相的成分和体积分数""",

            "order_disorder": f"""有序-无序转变是原子占位的有序度变化。

**理论**：
- 有序度参数 S = (p_A - x_A) / (1 - x_A)
- 临界温度：Tc 与交换能相关

**在Thermo-Calc中**：
- 使用子晶格模型描述有序相
- 计算有序化驱动力"""
        }

        return explanations.get(phase_type, "该相变类型分析正在完善中...")

    def validate_calculation(self, calc_params: Dict) -> List[str]:
        """验证计算参数"""
        warnings = []

        if calc_params.get("temperature", 0) < 0:
            warnings.append("温度不能为负值（热力学温度）")

        if not calc_params.get("database"):
            warnings.append("未指定数据库，建议明确使用TCFE或SGTE")

        if not calc_params.get("composition"):
            warnings.append("未指定成分，无法进行计算")

        return warnings