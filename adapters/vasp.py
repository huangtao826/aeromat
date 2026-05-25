# aeromat/adapters/vasp.py
"""
VASP 软件适配器
"""
from typing import Dict, List, Optional


class VaspAdapter:
    """VASP 适配器"""

    def __init__(self):
        self.name = "VASP"
        self.keywords = ["vasp", "incar", "poscar", "potcar", "outcar", "能带", "dft"]
        self.required_files = ["INCAR", "POSCAR", "POTCAR", "KPOINTS"]

    def parse_incar(self, incar_content: str) -> Dict:
        """解析INCAR文件"""
        params = {}
        for line in incar_content.split("\n"):
            line = line.strip()
            if line and not line.startswith("#"):
                parts = line.split("=")
                if len(parts) == 2:
                    key, value = parts[0].strip(), parts[1].strip()
                    params[key] = value
        return params

    def parse_poscar(self, poscar_content: str) -> Dict:
        """解析POSCAR文件"""
        lines = poscar_content.split("\n")
        try:
            scale = float(lines[0].strip())
            lattice = [
                [float(x) for x in lines[i].split()[:3]] for i in range(1, 4)
            ]
            elements = lines[5].split()
            numbers = [int(x) for x in lines[6].split()]

            return {
                "scale": scale,
                "lattice": lattice,
                "elements": elements,
                "numbers": numbers
            }
        except (IndexError, ValueError):
            return {"error": "POSCAR格式解析失败"}

    def validate_input(self, input_dir: str) -> Dict:
        """验证VASP输入文件"""
        issues = []
        warnings = []

        # TODO: 实现实际的文件检查

        if issues:
            return {"status": "error", "issues": issues}
        elif warnings:
            return {"status": "warning", "warnings": warnings}
        else:
            return {"status": "valid", "message": "输入文件格式正确"}

    def extract_results(self, outcar_path: str) -> Dict:
        """从OUTCAR提取计算结果"""
        # TODO: 实现OUTCAR解析
        return {
            "energy": None,
            "forces": None,
            "stress": None,
            "convergence": None
        }

    def get_theory_correlation(self, task: str) -> Dict:
        """获取理论关联"""
        correlations = {
            "结构优化": ["能量最小化原理", "Hellmann-Feynman力", "BFGS算法"],
            "能带计算": ["Kohn-Sham方程", "密度泛函理论", "平面波基组", "赝势方法"],
            "态密度": ["态密度泛函", "投影波方法", "能带积分"],
            "磁性计算": ["自旋极化", "磁晶各向异性", "Stoner模型"]
        }
        return correlations.get(task, {})

    def diagnose_convergence_issues(self, outcar_path: str) -> List[Dict]:
        """诊断收敛问题"""
        issues = []

        # TODO: 分析OUTCAR中的收敛问题

        return issues

    def interpret_band_structure(self, band_data: Dict) -> str:
        """解释能带结构"""
        band_gap = band_data.get("band_gap", 0)
        band_type = band_data.get("type", "unknown")

        explanation = f"""能带结构分析结果：

**带隙值**：{band_gap:.3f} eV

**带隙类型**：{band_type}

**物理解释**：
"""
        if band_gap == 0:
            explanation += "- 该材料表现为金属特性\n- 费米能级穿过导带，导电性强\n"
        elif band_gap < 3:
            explanation += "- 该材料为窄禁带半导体\n- 在可见光区域可能有光吸收\n"
        else:
            explanation += "- 该材料为宽带隙半导体或绝缘体\n- 电子激发困难，导电性差\n"

        return explanation