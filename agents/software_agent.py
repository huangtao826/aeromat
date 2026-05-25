# aeromat/agents/software_agent.py
"""
软件Agent - 仿真软件操作指导
"""
from pathlib import Path
from aeromat.knowledge import KnowledgeRetriever


class SoftwareAgent:
    """软件操作指导Agent"""

    def __init__(self):
        self.knowledge_dir = Path(__file__).parent.parent / "knowledge"
        self.retriever = KnowledgeRetriever(self.knowledge_dir)

    SOFTWARE_GUIDES = {
        "material_studio": {
            "structure_optimization": {
                "basic": """**Materials Studio 结构优化步骤**：

1. **导入结构**：File → Import → 选择结构文件（cif, pdb等）

2. **构建奶昔图**：
   - 使用"建造"工具构建表面、界面
   - 奶昔图（Debye-Scherrer）用于XRD模拟

3. **选择计算引擎**：
   - CASTEP：量子力学计算（能带、态密度）
   - DMol³：量子化学计算
   - Forcite：分子力学（力场优化）

4. **设置计算参数**：
   - Task → Geometry Optimization
   - Quality → Medium/Fine
   - Functional → GGA-PBE

5. **运行与监控**：
   - 运行计算
   - 查看输出：能量曲线、力收敛""",
                "common_issues": [
                    ("不收敛", "增加SCF迭代次数，检查自旋极化设置"),
                    ("能量过高", "检查原子位置是否合理，检查电荷"),
                    ("对称性错误", "适当降低对称性（More Properties → Modify symmetry）")
                ]
            },
            "band_structure": {
                "basic": """**CASTEP能带结构计算**：

1. **结构优化**：先进行几何优化获得基态结构

2. **能带计算设置**：
   - Task → Band Structure
   - K点路径：使用Brillouin区高对称性路径

3. **计算参数**：
   ```
   k-point set : Fine
   Use as fitted potential : No (关联赝势)
   ```

4. **结果分析**：
   - 使用View → Band Structure查看
   - 识别价带顶、导带底位置
   - 判断带隙类型（直接/间接）

5. **禁带宽度**：
   - 半导体：0-6 eV
   - 绝缘体：>6 eV
   - 金属：无带隙（费米能级穿过能带）""",
                "common_issues": [
                    ("带隙为0", "可能使用了不适合的泛函，尝试LDA→GGA→HSE06"),
                    ("K点不连续", "检查K点路径设置，确保使用相同的k点集"),
                    ("对称性过高", "适当增加k点密度或降低对称性")
                ]
            }
        },

        "vasp": {
            "structure_optimization": {
                "basic": """**VASP 结构优化（relaxation）**:

**INCAR 关键参数**：
```
ENCUT = 520        # 截断能，通常为材料最大ENMAX的1.2-1.3倍
EDIFF = 1E-5       # 电子自治收敛标准
EDIFFG = -0.02     # 力收敛标准（eV/Å）
IBRION = 2         # 2=共轭梯度法，1=准牛顿，3=分子动力学
ISIF = 3           # 2=只优化原子，3=同时优化原子和晶格
NSW = 100          # 最大离子步数
ISMEAR = 0         # 0=Gaussian用于绝缘体，1=Methfessel-Paxton用于金属
SIGMA = 0.05       # broadening宽度
```

**POSCAR 格式**：
```
元素名
缩放因子
晶格矢量（a1, a2, a3）
原子位置（Direct/Cartesian）
可选：动力学约束

**KPOINTS 文件**：
```
Monkhorst-Pack
3 3 3
0
Grid shift 0 0 0
```""",
                "common_issues": [
                    ("SCF不收敛", "增加ENCUT，调整ISMEAR/SIGMA，增加NELM"),
                    ("力不收敛", "降低IBRION的步长，检查POSCAR格式"),
                    ("内存不足", "降低K点密度，减少平面波数量")
                ]
            },
            "band_structure": {
                "basic": """**VASP 能带计算**：

**两步法**：
1. **自洽计算**：
   - CHGCAR = T（保存电荷密度）
   - NBANDS = 适当增加

2. **非自洽计算**：
   - ICHARG = 11（从电荷密度读取）
   - KPOINTS：沿高对称性路径（手动设置）

**能带路径（以FCC为例）**：
```
G L K G X W X
```

**使用VASPKIT或pymatgen自动生成K点路径**

**结果可视化**：
- 使用P4Vasp、VASPView、pyprocar等
- 标注费米能级、价带顶、导带底""",
                "common_issues": [
                    ("能带平滑但费米能级不确定", "增加NBANDS，延长计算时间"),
                    ("能带图有伪折叠", "增加K点密度"),
                    ("带隙明显低估", "使用HSE06杂化泛函或GW近似")
                ]
            }
        },

        "procast": {
            "solidification": {
                "basic": """**Procast 铸造凝固模拟**：

**主要步骤**：
1. **前处理**：
   - 导入几何（Mesh模块）
   - 定义材料属性（热物性、粘度）
   - 设置边界条件（换热系数）

2. **边界条件类型**：
   - 模具-铸件界面：Heat Transfer Coefficient (HTC)
   - 环境：辐射+对流换热

3. **求解器设置**：
   - 凝固模型：热传导+流体流动（可选）
   - 网格类型：四面体/六面体

4. **后处理**：
   - 温度场分布
   - 凝固时间
   - 缩孔预测（Porosity）

**关键参数**：
- 液相线、固相线温度
- 潜热（L = ΔH）
- 热传导系数（导热系数k）""",
                "common_issues": [
                    ("温度梯度异常", "检查网格质量，界面接触条件"),
                    ("缩孔预测不准确", "校准HTC，优化冒口设计"),
                    ("计算不收敛", "减小时间步长，检查材料属性范围")
                ]
            }
        },

        "ansys": {
            "structural_analysis": {
                "basic": """**Ansys Workbench 结构分析**：

**基本流程**：
1. **几何建模/导入**：
   - DM或SpaceClaim创建几何
   - 支持CAD格式（STP, IGES）

2. **网格划分**：
   - Mesh模块
   - 网格方法：四面体（Tet）/六面体主导（Hex）
   - 局部加密：接触区域、应力集中区

3. **边界条件**：
   - 固定约束（Fixed Support）
   - 位移加载（Displacement）
   - 力/压力（Force/Pressure）

4. **求解设置**：
   - 静态结构分析（Static Structural）
   - 分析类型：线性/非线性

5. **结果后处理**：
   - 等效应力（Equivalent Von-Mises Stress）
   - 总变形（Total Deformation）
   - 安全系数（Factor of Safety）""",
                "common_issues": [
                    ("网格不收敛", "改善网格质量，降低畸形单元比例"),
                    ("应力奇异", "避免尖角、添加圆角过渡"),
                    ("结果与预期不符", "检查边界条件、单位制、材料属性")
                ]
            }
        },

        "thermo_calc": {
            "phase_diagram": {
                "basic": """**Thermo-Calc 相图计算**：

**POLY模块基本命令**：
```
STEP                                # 逐步计算
MAP                                 # 相图映射

定义温度范围：
TC-Temperature 500 1500            # 500K-1500K

定义成分范围（以Fe-C为例）：
TC-Component C                       # 添加C作为变量
TC-Composition 0 0.02               # C含量0-2wt%

计算平衡：
Gibbs Energy System                  # 计算热力学平衡
```

**Post处理**：
- phase_diagram查看二元相图
- THERMO-CALC自动标注相边界

**数据库选择**：
- TCFE：钢铁材料
- SGTE：一般材料
- TCOX：氧化物""",
                "common_issues": [
                    ("相图与文献不符", "检查数据库选择，验证热力学参数"),
                    ("计算不收敛", "使用START命令设置初始猜测值"),
                    ("缺少相", "检查数据库是否包含该相，确认PO条件")
                ]
            }
        },

        "abaqus": {
            "plastic_deformation": {
                "basic": """**Abaqus 塑性变形分析**：

**材料模型设置**：
1. **弹塑性本构**：
   - Property → Material → Mechanical → Elastic（E, ν）
   - Plastic → 定义屈服应力-塑性应变数据

2. **强化模型**：
   - 等向强化（Isotropic）：各向同性扩大
   - 随动强化（Kinematic）：Bauschinger效应

**分析步骤**：
1. **Part建模**
2. **Assembly组装**
3. **Step设置**：
   - 静力分析（Static, General）
   - 时间/载荷曲线

4. **相互作用**：
   - 接触对定义
   - 摩擦系数

5. **载荷与边界**：
   - 施加载荷
   - 固定约束

6. **网格划分**：
   - 单元类型：C3D8R（二阶减缩积分）

7. **Job提交与后处理**：
   - Mises应力、塑性应变""",
                "common_issues": [
                    ("不收敛", "细化网格，减小时间步长，调整本构模型"),
                    ("负应变能", "检查单位制、载荷方向"),
                    ("结果异常", "验证材料参数、检查约束是否过约束")
                ]
            }
        }
    }

    def guide_operation(self, software: str, topic: str, difficulty: str, user_query: str = "") -> str:
        """提供软件操作指导"""
        # 先检索知识库
        knowledge_results = []
        if user_query:
            knowledge_results = self.retriever.retrieve(user_query, top_k=2)

        if software not in self.SOFTWARE_GUIDES:
            # 无内置指南，尝试从知识库回答
            if knowledge_results:
                kb_content = self.retriever.format_results(knowledge_results)
                return f"""根据知识库资料，我找到了以下相关信息：

{kb_content}

如果无法解决您的问题，请提供更详细的描述。"""
            return f"抱歉，暂不支持 {software} 的详细指导。请提供更多具体问题。"

        software_guides = self.SOFTWARE_GUIDES[software]

        # 尝试精确匹配topic
        if topic in software_guides:
            guide = software_guides[topic]
            guide_text = guide.get("basic", "")

            # 如果知识库有相关内容，附加在后面
            if knowledge_results:
                kb_content = self.retriever.format_results(knowledge_results)
                guide_text += f"\n\n---\n\n**📚 知识库参考：**\n{kb_content}"

            return guide_text

        # 模糊匹配
        for key, guide in software_guides.items():
            if topic in key or key in topic:
                guide_text = guide.get("basic", "")

                if knowledge_results:
                    kb_content = self.retriever.format_results(knowledge_results)
                    guide_text += f"\n\n---\n\n**📚 知识库参考：**\n{kb_content}"

                return guide_text

        # 返回软件概述
        overview = self._get_software_overview(software)

        # 如果知识库有相关内容，附加在后面
        if knowledge_results:
            kb_content = self.retriever.format_results(knowledge_results)
            overview += f"\n\n---\n\n**📚 知识库参考：**\n{kb_content}"

        return overview

    def _get_software_overview(self, software: str) -> str:
        """获取软件概述"""
        overview = {
            "material_studio": "**Materials Studio** 是BIOVIA开发的材料科学综合平台，包含多个计算模块：\n- CASTEP：DFT能带计算\n- DMol³：量子化学\n- Forcite：分子力学\n- Equilibria：热力学\n\n请告诉我您具体想做什么操作？",
            "vasp": "**VASP** 是维也纳大学开发的第一性原理计算软件，主要用于：\n- 电子结构计算\n- 结构优化\n- 磁性计算\n- 声子谱\n\n请告诉我您具体想做什么操作？",
            "procast": "**Procast** 是ESI集团的铸造仿真软件，主要用于：\n- 凝固模拟\n- 温度场分析\n- 缩孔预测\n\n请告诉我您具体想做什么操作？",
            "ansys": "**Ansys** 是通用的有限元分析软件，主要用于：\n- 结构力学分析\n- 热分析\n- 流体分析\n\n请告诉我您具体想做什么操作？",
            "thermo_calc": "**Thermo-Calc** 是热力学计算软件，主要用于：\n- 相图计算\n- 热力学平衡\n- 扩散模拟\n\n请告诉我您具体想做什么操作？",
            "abaqus": "**Abaqus** 是达索系统的非线性力学分析软件，主要用于：\n- 塑性变形\n- 复合材料\n- 冲击动力学\n\n请告诉我您具体想做什么操作？"
        }
        return overview.get(software, "该软件信息正在完善中...")

    def resolve_error(self, software: str, error_message: str) -> str:
        """解决软件错误"""
        # 这里应该根据具体的错误信息进行诊断
        return f"""我看到您在使用 {software} 时遇到了问题。

错误信息：{error_message[:100]}...

**一般性排查步骤**：
1. 检查输入文件格式是否正确
2. 确认参数设置在合理范围内
3. 查看软件的错误日志（通常在输出目录）
4. 参考官方文档的错误代码说明

如果能提供更详细的错误信息，我可以给出更针对性的解决方案。
"""