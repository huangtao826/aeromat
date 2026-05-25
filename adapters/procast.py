# aeromat/adapters/procast.py
"""
Procast 软件适配器
"""
from typing import Dict, List


class ProcastAdapter:
    """Procast 铸造仿真适配器"""

    def __init__(self):
        self.name = "Procast"
        self.keywords = ["procast", "铸造", "凝固", "缩孔", "温度梯度", "热流"]
        self.modules = ["mesh", "precast", "cast", "post"]

    def parse_simulation_results(self, result_path: str) -> Dict:
        """解析仿真结果"""
        return {
            "temperature_field": None,
            "solidification_time": None,
            "porosity": None,
            "hot_spots": []
        }

    def get_theory_correlation(self, result_type: str) -> Dict:
        """获取理论关联"""
        correlations = {
            "温度场": ["傅里叶传热定律", "边界条件", "初始条件"],
            "凝固时间": ["凝固潜热", "形核理论", "枝晶生长"],
            "缩孔": ["凝固收缩", "补缩通道", "压力传导"],
            "应力": ["热应力", "弹性力学", "塑性变形"]
        }
        return correlations.get(result_type, {})

    def diagnose_defects(self, results: Dict) -> List[Dict]:
        """缺陷诊断"""
        defects = []

        # 缩孔检测
        if results.get("porosity", 0) > 0.05:
            defects.append({
                "type": "缩孔",
                "severity": "high",
                "location": "待确定",
                "cause": "凝固收缩导致的体积缺失",
                "solution": "优化冒口设计，增加冷却速率"
            })

        # 热裂纹检测
        if results.get("stress_concentration", 0) > 0.8:
            defects.append({
                "type": "热裂纹",
                "severity": "medium",
                "location": "待确定",
                "cause": "凝固后期热应力超过材料强度",
                "solution": "降低冷却速率，优化模具设计"
            })

        return defects

    def suggest_optimization(self, current_params: Dict, defects: List) -> List[Dict]:
        """建议优化方案"""
        suggestions = []

        for defect in defects:
            if defect["type"] == "缩孔":
                suggestions.append({
                    "parameter": "冷却速率",
                    "current": current_params.get("cooling_rate", "未知"),
                    "suggested": "提高20-30%",
                    "theory": "加快冷却可以减小枝晶间距，减少微观缩孔"
                })
                suggestions.append({
                    "parameter": "冒口尺寸",
                    "current": "待确定",
                    "suggested": "增加10-15%",
                    "theory": "更大的冒口提供更充足的液态金属补缩"
                })
            elif defect["type"] == "热裂纹":
                suggestions.append({
                    "parameter": "浇注温度",
                    "current": current_params.get("pouring_temp", "未知"),
                    "suggested": "降低20-30°C",
                    "theory": "降低过热度可以减少凝固收缩量"
                })

        return suggestions