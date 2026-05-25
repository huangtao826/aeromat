# aeromat/adapters/abaqus.py
"""
Abaqus 软件适配器
"""
from typing import Dict, List


class AbaqusAdapter:
    """Abaqus 非线性力学分析适配器"""

    def __init__(self):
        self.name = "Abaqus"
        self.keywords = ["abaqus", "塑性", "屈服", "本构", "非线性", "CAE"]
        self.analysis_types = ["Static", "Dynamic", "Thermal", "Coupled"]

    def parse_inp_file(self, inp_content: str) -> Dict:
        """解析Abaqus输入文件"""
        sections = {}
        current_section = None

        for line in inp_content.split("\n"):
            if line.startswith("*"):
                current_section = line.strip().split(",")[0].replace("*", "")
                sections[current_section] = []
            elif current_section:
                sections[current_section].append(line.strip())

        return {
            "nodes": len(sections.get("NODE", [])),
            "elements": len(sections.get("ELEMENT", [])),
            "materials": self._extract_materials(sections.get("MATERIAL", [])),
            "steps": self._extract_steps(sections.get("STEP", []))
        }

    def _extract_materials(self, material_lines: List[str]) -> List[str]:
        """提取材料名称"""
        materials = []
        for line in material_lines:
            if "Name=" in line:
                name = line.split("Name=")[1].split(",")[0]
                materials.append(name)
        return materials

    def _extract_steps(self, step_lines: List[str]) -> List[str]:
        """提取分析步骤"""
        steps = []
        for line in step_lines:
            if "Step" in line:
                steps.append(line)
        return steps

    def get_theory_correlation(self, analysis_type: str) -> Dict:
        """获取理论关联"""
        correlations = {
            "塑性变形": ["Mises屈服条件", "Prandtl-Reuss理论", "等向强化", "随动强化"],
            "蠕变": ["蠕变定律", "Norton定律", "时间硬化", "应变硬化"],
            "复合材料": ["层合板理论", " Tsai-Wu准则", " Hashin失效判据"],
            "接触": ["Hertz接触", "罚函数法", "拉格朗日乘子法"]
        }
        return correlations.get(analysis_type, {})

    def interpret_plastic_results(self, plastic_data: Dict) -> str:
        """解释塑性分析结果"""
        max_plastic_strain = plastic_data.get("max_plastic_strain", 0)
        equivalent_stress = plastic_data.get("equivalent_stress", 0)

        interpretation = f"""塑性分析结果解读：

**最大塑性应变**：{max_plastic_strain:.4f}
**等效应力**：{equivalent_stress:.2f} MPa

"""
        if max_plastic_strain > 0.2:
            interpretation += "⚠️ 警告：塑性应变较大（>20%），\n"
            interpretation += "可能已进入大变形阶段，建议：\n"
            interpretation += "1. 检查几何非线性设置\n"
            interpretation += "2. 考虑是否需要网格重划分\n"
            interpretation += "3. 验证材料本构模型参数"
        else:
            interpretation += "✓ 塑性变形在可控范围内"

        return interpretation

    def diagnose_convergence_issues(self, msg_file: str) -> List[Dict]:
        """诊断收敛问题"""
        issues = []

        # TODO: 解析.msg文件
        # 常见问题：
        # - 负应变能
        # - 塑性屈服过大
        # - 接触过度穿透

        return issues

    def validate_material_model(self, material_params: Dict) -> List[str]:
        """验证材料模型参数"""
        warnings = []

        if material_params.get("E", 0) <= 0:
            warnings.append("弹性模量必须为正值")

        if material_params.get("poisson_ratio", 0) >= 0.5 or material_params.get("poisson_ratio", 0) < 0:
            warnings.append("泊松比应在0-0.5范围内")

        if material_params.get("yield_strength", 0) <= 0:
            warnings.append("屈服强度必须为正值")

        plastic_data = material_params.get("plastic", [])
        if len(plastic_data) < 2:
            warnings.append("塑性数据点不足，至少需要2个点定义屈服曲线")

        return warnings