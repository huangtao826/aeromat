# aeromat/agents/core_agent.py
"""
核心Agent - 意图识别与Agent调度
"""
import os
from typing import Dict, List, Optional, Tuple
from .theory_agent import TheoryAgent
from .software_agent import SoftwareAgent
from .result_agent import ResultAgent


class CoreAgent:
    """核心Agent，负责意图识别和多Agent调度"""

    def __init__(self):
        self.theory_agent = TheoryAgent()
        self.software_agent = SoftwareAgent()
        self.result_agent = ResultAgent()
        self.conversation_history = []
        self._llm_client = None

        # 初始化LLM客户端（如果配置了API key）
        self._init_llm()

    def _init_llm(self):
        """初始化LLM客户端"""
        api_key = os.getenv("DASHSCOPE_API_KEY") or os.getenv("OPENAI_API_KEY")
        if api_key:
            try:
                from aeromat.core import LLMClient
                self._llm_client = LLMClient()
            except Exception as e:
                print(f"LLM初始化失败: {e}")

    @property
    def llm_available(self) -> bool:
        """检查LLM是否可用"""
        return self._llm_client is not None

    def recognize_intent(self, user_input: str, context: Optional[Dict] = None) -> Dict:
        """
        识别用户意图

        Returns:
            {
                "intent": "operation_help" | "result_analysis" | "theory_explain" | "optimization",
                "software": "material_studio" | "vasp" | ... | None,
                "topic": str,
                "difficulty": "basic" | "intermediate" | "advanced",
                "emotional_state": "confused" | "frustrated" | "curious"
            }
        """
        intent_patterns = {
            "operation_help": ["怎么", "如何", "操作", "设置", "步骤", "教程", "不会", "不知道"],
            "result_analysis": ["分析", "结果", "看不懂", "解释", "含义", "什么意思"],
            "theory_explain": ["为什么", "原理", "理论", "为什么", "什么原理", "不懂"],
            "optimization": ["优化", "改进", "提高", "降低", "调整", "参数"],
            "error_resolve": ["错误", "报错", "失败", "不对", "有问题"]
        }

        software_patterns = {
            "material_studio": ["material studio", "ms", "奶昔图", "castep", "dmol3", "forcite"],
            "vasp": ["vasp", "incar", "poscar", "能带", "dft"],
            "procast": ["procast", "铸造", "凝固", "缩孔"],
            "ansys": ["ansys", "workbench", "网格", "应力", "热分析"],
            "thermo_calc": ["thermo-calc", "tc", "相图", "热力学"],
            "abaqus": ["abaqus", "塑性", "屈服", "本构"]
        }

        # 意图识别
        intent = "general"
        for intent_name, patterns in intent_patterns.items():
            if any(p in user_input.lower() for p in patterns):
                intent = intent_name
                break

        # 软件识别
        software = None
        for sw_name, patterns in software_patterns.items():
            if any(p in user_input.lower() for p in patterns):
                software = sw_name
                break

        # 难度评估（基于上下文）
        difficulty = "basic"
        if any(kw in user_input.lower() for kw in ["高级", "复杂", "深入", "详细"]):
            difficulty = "advanced"
        elif any(kw in user_input.lower() for kw in ["一些", "继续", "更多"]):
            difficulty = "intermediate"

        # 情感状态
        emotional_state = "neutral"
        if any(kw in user_input.lower() for kw in ["不会", "不懂", "看不懂", "困惑", "难"]):
            emotional_state = "confused"
        elif any(kw in user_input.lower() for kw in ["不对", "错误", "失败", "报错"]):
            emotional_state = "frustrated"

        return {
            "intent": intent,
            "software": software,
            "topic": self._extract_topic(user_input),
            "difficulty": difficulty,
            "emotional_state": emotional_state
        }

    def _extract_topic(self, user_input: str) -> str:
        """提取关键话题"""
        topic_keywords = [
            "结构优化", "能带", "态密度", "力学", "热力学",
            "凝固", "相图", "应力", "应变", "塑性",
            "收敛", "带隙", "相变", "扩散"
        ]
        for topic in topic_keywords:
            if topic in user_input:
                return topic
        return "general"

    def route_to_sub_agents(self, intent: Dict, user_input: str, software_context: Optional[str] = None) -> str:
        """根据意图调度到子Agent"""
        # 优先使用intent中的software，其次使用上下文中的software
        software = intent.get("software") or software_context
        intent_type = intent.get("intent")

        # 记录对话
        self.conversation_history.append({
            "role": "user",
            "content": user_input
        })

        response = ""

        if intent_type == "operation_help" and software:
            # 软件操作指导
            response = self.software_agent.guide_operation(
                software=software,
                topic=intent.get("topic", ""),
                difficulty=intent.get("difficulty", "basic"),
                user_query=user_input
            )

        elif intent_type == "result_analysis" and software:
            # 结果分析
            response = self.result_agent.analyze_result(
                software=software,
                topic=intent.get("topic", ""),
                context=self.conversation_history
            )

        elif intent_type in ["theory_explain", "optimization"]:
            # 理论解释或优化建议
            response = self.theory_agent.explain(
                topic=intent.get("topic", ""),
                intent=intent_type,
                difficulty=intent.get("difficulty", "basic"),
                context=user_input
            )

        elif intent_type == "error_resolve" and software:
            # 错误解决
            response = self.software_agent.resolve_error(
                software=software,
                error_message=user_input
            )

        else:
            # 一般对话 - 优先使用LLM
            response = self._general_response(user_input, intent)

        self.conversation_history.append({
            "role": "assistant",
            "content": response
        })

        return response

    def _general_response(self, user_input: str, intent: Dict) -> str:
        """通用回复（当无法明确分类时）"""
        # 如果LLM可用，使用LLM生成回复
        if self._llm_client:
            return self._llm_response(user_input, intent)

        return f"""我理解了您的问题。

您目前询问的是关于「{intent.get('topic', '材料科学')}」的话题。

我可以帮您：
- 📚 解释相关理论原理
- 💻 指导软件操作步骤
- 📊 分析仿真结果
- 🔧 提供优化建议

请详细描述您遇到的具体问题，我会针对性地帮助您。
"""

    def _llm_response(self, user_input: str, intent: Dict) -> str:
        """使用LLM生成回复"""
        software_context = intent.get("software", "")
        topic = intent.get("topic", "")

        system_prompt = """你是一个专业的材料科学教学助手，名为Aeromat AI。
你的任务是帮助学生学习材料科学理论和仿真软件操作。
请用中文回答，语言简洁专业，适当使用emoji增加可读性。
如果用户询问软件操作，提供具体的步骤和参数建议。"""

        user_message = user_input
        if software_context:
            user_message = f"[当前软件上下文: {software_context}] {user_message}"
        if topic and topic != "general":
            user_message = f"[相关话题: {topic}] {user_message}"

        try:
            return self._llm_client.chat(user_message, system_prompt=system_prompt)
        except Exception as e:
            return f"LLM调用失败: {str(e)}\n\n请切换到本地模式或检查API配置。"

    def get_conversation_context(self, window: int = 5) -> List[Dict]:
        """获取对话上下文"""
        return self.conversation_history[-window:]

    def clear_history(self):
        """清除对话历史"""
        self.conversation_history = []