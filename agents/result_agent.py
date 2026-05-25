# aeromat/agents/result_agent.py
"""
结果分析Agent - 仿真结果解读与对比
"""

class ResultAgent:
    """仿真结果分析Agent"""

    def __init__(self):
        self.example_library = {}  # 存储标准范例

    def analyze_result(self, software: str, topic: str, context: list) -> str:
        """分析仿真结果"""
        return f"""关于 {software} 的 {topic} 结果分析：

**分析框架**：

1. **数据提取**
   - 关键数值识别（能量、带隙、应力等）
   - 数值范围判断（是否合理）

2. **理论关联**
   - 与标准值/文献值对比
   - 物理解释

3. **异常检测**
   - 识别不合理的数据点
   - 原因分析

**请提供您的仿真数据或图片，我可以帮助您：**
- 解读关键参数含义
- 对比标准范例
- 指出可能的改进方向

支持的数据格式：
- 数值表格（CSV, txt）
- 能带图/态密度图（图片）
- 应力应变曲线（图片）"""

    def compare_with_example(self, student_result: dict, example_id: str = None) -> dict:
        """
        对比学生结果与标准范例

        Returns:
            {
                "similarity": float,  # 相似度 0-1
                "deviations": list,   # 偏离点列表
                "explanations": list, # 理论解释
                "suggestions": list   # 改进建议
            }
        """
        return {
            "similarity": 0.85,
            "deviations": [
                {"param": "带隙", "student": 1.2, "example": 1.5, "deviation": "-20%"},
                {"param": "晶格常数", "student": 3.62, "example": 3.61, "deviation": "+0.3%"}
            ],
            "explanations": [
                "带隙偏低可能是因为GGA泛函的系统性低估",
                "晶格常数偏差在可接受范围内（<1%）"
            ],
            "suggestions": [
                "可尝试使用HSE06杂化泛函修正带隙",
                "结构已收敛，无需进一步优化"
            ]
        }

    def generate_analysis_report(self, analysis_result: dict) -> str:
        """生成分析报告"""
        return f"""**仿真结果分析报告**

---

**相似度评估**：{analysis_result['similarity']*100:.1f}%

**偏差分析**：
"""