# aeromat/adapters/ansys.py
"""
Ansys 软件适配器
"""
from typing import Dict, List


class AnsysAdapter:
    """Ansys 有限元分析适配器"""

    def __init__(self):
        self.name = "Ansys"
        self.keywords = ["ansys", "workbench", "网格", "应力", "变形", "热分析", "fem"]
        self.modules = ["Mechanical", "Thermal", "Fluid", "Structural"]

    def parse_mesh_info(self, mesh_data: Dict) -> Dict:
        """解析网格信息"""
        return {
            "element_type": mesh_data.get("type", "unknown"),
            "node_count": mesh_data.get("nodes", 0),
            "element_count": mesh_data.get("elements", 0),
            "quality": mesh_data.get("quality", 0),
            "warnings": []
        }

    def validate_mesh(self, mesh_data: Dict) -> List[str]:
        """验证网格质量"""
        warnings = []

        if mesh_data.get("quality", 1) < 0.3:
            warnings.append("网格质量偏低（<0.3），可能导致计算不收敛")

        if mesh_data.get("skewness", 0) > 0.8:
            warnings.append("网格歪斜度偏高，部分区域可能需要加密")

        if mesh_data.get("aspect_ratio", 0) > 10:
            warnings.append("长宽比过大，建议优化网格")

        return warnings

    def get_theory_correlation(self, analysis_type: str) -> Dict:
        """获取理论关联"""
        correlations = {
            "结构静力学": ["胡克定律", "平衡方程", "边界条件"],
            "结构动力学": ["模态分析", "响应谱", "谐响应"],
            "热分析": ["傅里叶定律", "热容", "对流换热"],
            "非线性": ["塑性理论", "大变形", "接触"]
        }
        return correlations.get(analysis_type, {})

    def interpret_stress_results(self, stress_data: Dict) -> str:
        """解释应力结果"""
        max_stress = stress_data.get("max_von_mises", 0)
        yield_strength = stress_data.get("material_yield", 250)  # MPa

        interpretation = f"""应力分析结果解读：

**最大等效应力（Von-Mises）**：{max_stress:.2f} MPa
**材料屈服强度**：{yield_strength} MPa
**安全系数**：{yield_strength/max_stress:.2f}

"""
        if max_stress > yield_strength:
            interpretation += "⚠️ 警告：最大应力超过材料屈服强度，\n"
            interpretation += "建议：\n1. 优化几何形状避免应力集中\n2. 增加圆角过渡\n3. 考虑使用更高强度材料"
        else:
            interpretation += "✓ 最大应力在安全范围内"

        return interpretation

    def diagnose_convergence_issues(self, solver_output: Dict) -> List[Dict]:
        """诊断收敛问题"""
        issues = []

        if solver_output.get("energy_ratio", 1) > 1e5:
            issues.append({
                "type": "能量比过大",
                "cause": "可能存在过约束或材料模型问题",
                "solution": "检查边界条件，降低网格畸形度"
            })

        if solver_output.get("penetration", 0) > 0.1:
            issues.append({
                "type": "接触穿透过大",
                "cause": "接触刚度不足或网格太粗",
                "solution": "增加接触刚度，细化接触区域网格"
            })

        return issues