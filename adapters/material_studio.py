# aeromat/adapters/material_studio.py
"""
Material Studio 软件适配器
"""
from typing import Dict, List, Optional


class MaterialStudioAdapter:
    """Material Studio 适配器"""

    def __init__(self):
        self.name = "Material Studio"
        self.modules = ["CASTEP", "DMol3", "Forcite", "Equilibria"]
        self.keywords = ["奶昔图", "骰子", "分子结构", "能带", "MS", "castep", "dmol3", "forcite"]

    def parse_input_file(self, file_path: str) -> Dict:
        """解析MS输入文件"""
        # TODO: 实现文件解析
        return {"status": "pending", "message": "文件解析功能开发中"}

    def extract_result(self, output: Dict) -> Dict:
        """提取MS计算结果"""
        return {
            "energy": output.get("energy", None),
            "lattice": output.get("lattice", None),
            "band_gap": output.get("band_gap", None),
            "structure": output.get("structure", None)
        }

    def get_theory_correlation(self, module: str, task: str) -> Dict:
        """获取与理论知识的关联"""
        correlations = {
            "CASTEP": {
                "结构优化": ["原子位置弛豫", "能量最小化原理", "Hellmann-Feynman力"],
                "能带计算": ["能带理论", "Bloch定理", "布里渊区", "赝势方法"],
                "态密度": ["态密度泛函理论", "投影波方法", "带间跃迁"]
            },
            "DMol3": {
                "几何优化": ["分子轨道理论", "密度泛函", "基组"],
                "红外光谱": ["振动模式", "频率计算", "红外活性"]
            },
            "Forcite": {
                "能量最小化": ["分子力学", "力场", "非键相互作用"],
                "动力学": ["牛顿运动方程", "系综理论", "时间步长"]
            }
        }
        return correlations.get(module, {}).get(task, {})

    def validate_parameters(self, module: str, params: Dict) -> List[str]:
        """验证参数设置是否合理"""
        warnings = []

        if module == "CASTEP":
            if params.get("cut_off_energy", 0) < 300:
                warnings.append("截断能过低，可能影响计算精度")
            if params.get("k_points", []) == []:
                warnings.append("建议设置K点以提高计算效率")

        return warnings

    def interpret_result(self, result_type: str, data: Dict) -> str:
        """解释结果的理论意义"""
        interpretations = {
            "energy": "能量越低表示结构越稳定，应为负值（相对于孤立原子）",
            "band_gap": "带隙>0为半导体/绝缘体，带隙=0为金属",
            "lattice_constant": "晶格常数反映晶体结构尺度，与实验值对比可验证计算可靠性"
        }
        return interpretations.get(result_type, "该指标需结合具体上下文理解")